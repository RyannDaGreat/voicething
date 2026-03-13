# VoiceThing — Manifest

## Overview

VoiceThing is a keyboard-driven voice transcription app for macOS built with PyQt6. It uses Whisper (with Metal GPU acceleration) to transcribe speech to text and paste it into the active app. Features include wake word detection, LLM post-processing, tmux integration, notification chimes via MIDI, pet companions, and themeable UI.

## Glossary

- **tray icon cycling**: During recording, the menu bar icon animates by cycling through hue values at 20 FPS (every 50ms via QTimer)
- **DraggableResizableMixin**: Mixin class providing frameless window drag/resize via mouse events; changes cursor shape at window edges
- **ImageIO**: macOS system framework for image encoding/decoding. Qt on macOS uses it internally for PNG decoding (`QPixmap.loadFromData`) and cursor bundle loading (`setCursorFromBundle`)
- **DYLD_LIBRARY_PATH**: macOS environment variable that overrides the dynamic linker's library search path. When it includes `/opt/homebrew/lib`, Homebrew's libpng gets loaded instead of Apple's private copy, causing ImageIO SIGBUS crashes. VoiceThing has a startup guard that strips this and re-execs.
- **0xBAD4007**: The crash address in the SIGBUS bug. It's a corrupted function pointer in ImageIO's `PNGReadPlugin` vtable, caused by Homebrew libpng ABI mismatch.

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

## Known Crash: macOS ImageIO SIGBUS (Reproduced & Fixed 2026-03-13)

**Symptom**: App crashes with `EXC_BAD_ACCESS (SIGBUS)` at address `0x0BAD4007`. Crash trace goes through `IIOReadPlugin::callInitialize()` in ImageIO — either via `QPixmap.loadFromData` or AppKit's `_edgeResizingCursorUpdate` → `setCursorFromBundle`.

**Root cause**: `DYLD_LIBRARY_PATH="/opt/homebrew/lib"` in the user's shell profile causes the dynamic linker to load Homebrew's libpng 1.6.50 for ImageIO's PNG plugin instead of Apple's private copy. The ABI mismatch corrupts `PNGReadPlugin`'s vtable. Same bug as wxWidgets #23547, Electron #48025, dotnet/sdk #44425, Tauri #7351.

**Reproduced**: `DYLD_LIBRARY_PATH=/opt/homebrew/lib python3.10 stress_test.py` → SIGBUS 3/3 runs. Without it: 0 crashes in 500k+ operations. User confirmed resizing windows (especially to zero size) triggers the crash.

**Fix (three layers)**:
1. **DYLD_LIBRARY_PATH startup guard** (top of voice_thing.py): Strips `/opt/homebrew/lib` from `DYLD_LIBRARY_PATH` and `os.execv()` re-execs before any libraries load. This is the primary fix.
2. **`_get_menubar_icon`**: QImage + QPainter compositing instead of PIL→PNG→loadFromData. No ImageIO involved. (Defense-in-depth.)
3. **Cursor deduplication**: `_current_edge` in `mouseMoveEvent`, `_table_ibeam` in `eventFilter`. (Defense-in-depth.)

**Verification**: `tests/test_sigbus_repro.py` reproduces the actual SIGBUS crash in a subprocess, then verifies the guard prevents it. `tests/test_cursor_crash.py` verifies ImageIO is bypassed in the icon pipeline.

## Constraints

- macOS only (uses AppKit, Metal, CoreMIDI)
- Python 3.10 via Homebrew
- PyQt6 (not PyQt5)
- Qt 6.9.0 on macOS 14.5
