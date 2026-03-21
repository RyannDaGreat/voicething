# VoiceThing — Manifest

## Overview

VoiceThing is a keyboard-driven voice transcription app for macOS built with PyQt6. It uses Whisper (with Metal GPU acceleration) to transcribe speech to text and paste it into the active app. Features include wake word detection, LLM post-processing, tmux integration, notification chimes via MIDI, pet companions, and themeable UI.

## Glossary

- **tray icon cycling**: During recording, the menu bar icon animates by cycling through hue values at 20 FPS (every 50ms via QTimer)
- **tray icon stripes**: During transcription/model loading, the menu bar icon shows animated horizontal stripes moving downward at 20 FPS
- **DraggableResizableMixin**: Mixin class providing frameless window drag/resize via mouse events; changes cursor shape at window edges
- **ImageIO**: macOS system framework for image encoding/decoding. Qt on macOS uses it internally for PNG decoding (`QPixmap.loadFromData`) and cursor bundle loading (`setCursorFromBundle`)
- **DYLD_LIBRARY_PATH**: macOS environment variable that overrides the dynamic linker's library search path. When it includes `/opt/homebrew/lib`, Homebrew's libpng gets loaded instead of Apple's private copy, causing ImageIO SIGBUS crashes. VoiceThing has a startup guard that moves this to `DYLD_FALLBACK_LIBRARY_PATH` and re-execs.
- **DYLD_FALLBACK_LIBRARY_PATH**: Searched *after* framework rpaths. Safe for Homebrew libs — ImageIO loads Apple's libpng first, FluidSynth still finds its dylib as a fallback.
- **0xBAD4007**: The crash address in the SIGBUS bug. It's a corrupted function pointer in ImageIO's `PNGReadPlugin` vtable, caused by Homebrew libpng ABI mismatch.
- **TRANSCRIPTION_SHORTCUTS**: Settings key storing a list of action keys (e.g. `['L', 'C']`) that appear as quick-access buttons on each transcription row. Configurable via toggle buttons in the actions dialog.
- **ACTION_INFO**: Module-level dict mapping action keys to `(icon_name, label, signal_name)` tuples. Used by both `TranscriptionActionsDialog` and `TranscriptionRow` to dynamically build shortcut buttons.
- **Append Copy**: Action that appends transcription text to the clipboard (with newline separator) rather than replacing it. Key: B, icon: clipboard-plus.
- **command phrases**: Voice-triggered actions. Say a phrase → run an internal command or shell command, with no recording. Only works with macOS native engine (arbitrary phrase support). Toolbar slot: H key.
- **internal commands**: Command phrases that toggle app settings via `S.set()` instead of running shell commands. Defined in `_INTERNAL_COMMANDS` dict. Checked before shell commands.
- **control server**: HTTP server on localhost for remote-controlling VoiceThing. Endpoint: `/cmd?phrase=...`. Started automatically on a random port. Port shown in Preferences.

## Key Files

| File | Purpose |
|------|---------|
| `voice_thing.py` | Main app — UI, recording, transcription, settings (~10k+ lines). Has DYLD_LIBRARY_PATH startup guard at top. |
| `pet_companion.py` | Animated pet widgets (Emmy etc.) |
| `piano.py` | Piano keyboard widget for chime preview |
| `synth.py` | MIDI synthesizer for notification chimes |
| `tts_server.py` | Text-to-speech server integration |
| `styles/` | Theme implementations (neon_sign, cyberpunk_metal, etc.) |
| `tests/test_sigbus_repro.py` | Reproduces the SIGBUS crash via subprocess with DYLD_LIBRARY_PATH |
| `tests/test_cursor_crash.py` | Verifies ImageIO is bypassed in icon pipeline + cursor dedup |
| `tests/test_menubar_icon.py` | Verifies menubar icon at all hue values |
| `assets/clipboard-plus.svg` | Copy icon with plus symbol for "Append Copy" action |

## Known Crash: macOS ImageIO SIGBUS (Reproduced & Fixed 2026-03-13)

**Symptom**: App crashes with `EXC_BAD_ACCESS (SIGBUS)` at address `0x0BAD4007`. Crash trace goes through `IIOReadPlugin::callInitialize()` in ImageIO — either via `QPixmap.loadFromData` or AppKit's `_edgeResizingCursorUpdate` → `setCursorFromBundle`.

**Root cause**: `DYLD_LIBRARY_PATH="/opt/homebrew/lib"` in the user's shell profile causes the dynamic linker to load Homebrew's libpng 1.6.50 for ImageIO's PNG plugin instead of Apple's private copy. The ABI mismatch corrupts `PNGReadPlugin`'s vtable. Same bug as wxWidgets #23547, Electron #48025, dotnet/sdk #44425, Tauri #7351.

**Reproduced**: `DYLD_LIBRARY_PATH=/opt/homebrew/lib python3.10 stress_test.py` → SIGBUS 3/3 runs. Without it: 0 crashes in 500k+ operations. User confirmed resizing windows (especially to zero size) triggers the crash.

**Fix (three layers)**:
1. **DYLD_LIBRARY_PATH startup guard** (top of voice_thing.py): Moves `/opt/homebrew/lib` from `DYLD_LIBRARY_PATH` to `DYLD_FALLBACK_LIBRARY_PATH` and `os.execv()` re-execs. FALLBACK is searched after framework rpaths, so ImageIO loads Apple's libpng first but FluidSynth still resolves.
2. **`_get_menubar_icon`**: QImage + QPainter compositing instead of PIL→PNG→loadFromData. No ImageIO involved. (Defense-in-depth.)
3. **Cursor deduplication**: `_current_edge` in `mouseMoveEvent`, `_table_ibeam` in `eventFilter`. (Defense-in-depth.)

**Verification**: `tests/test_sigbus_repro.py` reproduces the actual SIGBUS crash in a subprocess, then verifies the guard prevents it. `tests/test_cursor_crash.py` verifies ImageIO is bypassed in the icon pipeline.

## Tray Icon Animation States

The menu bar tray icon has three visual states:

| State | Visual | Timer |
|-------|--------|-------|
| Idle | Static template icon (auto light/dark via `setIsMask`) | Stopped |
| Recording | Hue cycling rainbow animation (2°/frame at 20 FPS) | Running (50ms) |
| Transcribing | Horizontal stripes moving downward | Running (50ms) |

`_is_menubar_dark()` uses a hidden `NSStatusItem` probe to detect the actual menu bar appearance (wallpaper-dependent), not the system-wide dark mode setting.

## Transcription Actions & Shortcuts

Actions available per transcription item (via hamburger menu):

| Key | Icon | Action |
|-----|------|--------|
| C | copy | Copy to clipboard |
| B | clipboard-plus | Append to clipboard |
| T | tmux | Send to tmux pane |
| P | play | Play audio recording |
| R | refresh | Re-transcribe with current model |
| L | robot | Run LLM de-ramble |
| A | file-audio | Open audio file in Finder |
| O | file-text | Open transcript file in Finder |
| H | eye-off | Hide/remove from list |

Users can toggle which actions appear as **shortcut buttons** on each transcription row (next to the hamburger menu). Toggle controls are in the actions dialog. Stored in `S.TRANSCRIPTION_SHORTCUTS` (default: `['L']`).

## Command Phrases

Voice-triggered commands — say a phrase, run an action, no recording involved. Only works with the macOS native wake word engine (NSSpeechRecognizer supports arbitrary phrases).

**Two types of command phrases**:
1. **Shell commands**: phrase → bash command (stored in `S.COMMAND_PHRASES` dict). For external actions like Spotify control, volume, brightness.
2. **Internal commands**: phrase → `S.set()` call (hardcoded in `VoiceThingWindow._INTERNAL_COMMANDS`). For toggling app settings with bidirectional UI updates. Currently: `reply on`/`reply off` (SPEAK_BACK_APPEND_INSTRUCTION), `enter on`/`enter off` (AUTO_ENTER).

Internal commands are checked first in `_on_command_phrase_detected`; if no match, falls through to shell commands. Both types are registered with the macOS speech engine.

**Architecture**:
- Settings: `COMMAND_PHRASES_ENABLED` (bool), `COMMAND_PHRASES` (dict of phrase→bash_command)
- Default phrases: app-specific media controls (Spotify, Music.app), brightness/volume, key simulation (press enter key). Generic media key simulation was removed — `MRMediaRemoteSendCommand` silently fails on macOS 15.4+ (entitlement-gated), and `CGEventPost` only reaches the frontmost app.
- `COMMAND_PHRASES_MUTE_WHILE_RECORDING` (bool, default True): suppresses command phrase callbacks during recording
- `wakeword/base.py`: `on_command` callback in `WakeWordEngine.__init__`
- `wakeword/macos_engine.py`: `command_phrases` param, `_command_phrases_lower` lookup set. In delegate: when not recording and command phrase detected → `on_command(phrase)` and return (skip recording)
- `VoiceThingWindow._on_command_phrase_detected`: checks internal commands first (via `_handle_control_cmd`), then falls through to shell commands. Plays `command_phrase` chime on match.
- `CommandPhrasesDialog`: editable table (phrase|command), +/- row buttons, enable checkbox. Emits `phrases_changed` signal which triggers engine restart

**Toolbar**: H key slot (replaced auto-minimize/eye button). H opens dialog, Shift+H toggles on/off. Auto-minimize moved to Preferences → Window section as a checkbox.

**Chime**: `command_phrase` — two-chord confirmation (`[A,E,A5], [D,A5,G6]`). Listed in all chime themes and CHIME_DESCRIPTIONS.

## HTTP Control Server

Lightweight HTTP server for remote-controlling VoiceThing from any program (curl, Claude Code, scripts).

**Startup**: Started automatically in `VoiceThingWindow.__init__` via `_start_control_server()`. Binds to `127.0.0.1` on a random free port (starting from 8222). Port is displayed in Preferences dialog (bottom, selectable text with tooltip showing curl examples).

**Endpoints**:
- `GET /health` → `{"status": "ok", "app": "voicething"}`
- `GET /cmd?phrase=...` → dispatches to `_handle_control_cmd`. For known internal commands, calls `S.set()` and returns `{"ok": true, "phrase": "...", "result": "..."}`. Unknown phrases return a result string saying so.

**Design**: Intentionally simple string→action dispatch for now. The `/cmd` endpoint is the extension point — future commands can add new phrases without changing the server. All received commands are printed to console via `[control]` prefix.

**Example usage**: `curl 'http://localhost:8222/cmd?phrase=reply+off'`

## Constraints

- macOS only (uses AppKit, Metal, CoreMIDI)
- Python 3.10 via Homebrew
- PyQt6 (not PyQt5)
- Qt 6.9.0 on macOS 14.5
