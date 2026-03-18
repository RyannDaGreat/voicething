# VoiceThing — Concerns

Historical record of bugs, mistakes, and lessons learned.

---

## 2026-03-13: SIGBUS crash in macOS ImageIO during setCursor

### The Bug

App repeatedly crashed with `EXC_BAD_ACCESS (SIGBUS)` at `0x0BAD4007` on macOS 14.5 + Qt 6.9.0. Crash occurred on main thread in `IIOReadPlugin::callInitialize()`, called from `setCursorFromBundle` → `CGImageSourceCreateImageAtIndex`. The address `0x0BAD4007` is a corrupted function pointer (note "BAD" in the hex) — ImageIO's PNG plugin vtable was corrupted.

### Investigation Timeline

**Phase 1: Wrong hypotheses**
1. Initial hypothesis: wake-from-sleep GPU state corruption. **Wrong** — user confirmed it happens repeatedly, not just after wake.
2. Examined all 19 `setCursor` calls in the codebase. All use standard `Qt.CursorShape` enums or one custom SVG cursor. No obvious bugs.
3. Wrote a synthetic test hammering `setCursor` with 500k calls — couldn't reproduce. The crash requires real ImageIO plugin state corruption, not just rapid cursor changes.

**Phase 2: Partial root cause (ImageIO interleaving)**
4. Found `_get_menubar_icon()` was doing `PIL→PNG encode→QPixmap.loadFromData(PNG)` on a 50ms QTimer (20 FPS during recording). `loadFromData` routes through macOS ImageIO's PNG plugin. `setCursor` also routes through ImageIO for cursor bundle loading.
5. Applied first fix: replaced `_get_menubar_icon` with QPainter compositing (no ImageIO), added cursor deduplication via `_current_edge` and `_table_ibeam`. All tests passed.
6. **First fix failed** — user reported crash again. Second crash log showed a different code path: AppKit's `_edgeResizingCursorUpdate:atLocation:` → `setCursorFromBundle` → ImageIO. This is internal to AppKit, not our code.

**Phase 3: Failed reproduction attempts**
7. Tried synthetic reproduction: 500k `setCursor` calls in a loop. No crash. The corruption requires specific heap layout and timing.
8. Tried interleaving `loadFromData` + `setCursor` in QTimer callbacks without `DYLD_LIBRARY_PATH`. No crash even after 600k+ operations over 15 seconds.
9. Researched wxWidgets #23547 — they also couldn't reproduce synthetically. Their fix: avoid ImageIO entirely.

**Phase 4: True root cause discovered**
10. Research agent found that `0xBAD4007` crashes are caused by **Homebrew libpng ABI mismatch** when `DYLD_LIBRARY_PATH` includes `/opt/homebrew/lib`. This is documented in wxWidgets #23547, Electron #48025, dotnet/sdk #44425, Tauri #7351.
11. Checked user's shell profile: `~/.zshrc` contains `export DYLD_LIBRARY_PATH="/opt/homebrew/lib"` (added for fluidsynth). Homebrew libpng 1.6.50 exists at `/opt/homebrew/lib/libpng.dylib`.
12. **Reproduction succeeded**: `DYLD_LIBRARY_PATH="/opt/homebrew/lib" python3.10 stress_test.py` → Bus error 3/3 runs. Without it: 0 crashes in 500k+ operations.
13. Isolated the crash trigger: neither `loadFromData` alone nor `setCursor` alone crashes — the crash requires BOTH interleaving AND the libpng ABI mismatch. `loadFromData` alone survived 600k+ ops; `setCursor` alone survived 664k+ ops; but interleaved, the crash occurs within seconds.
14. User confirmed: manually resizing the test windows (especially to zero size) reliably triggers the crash when `DYLD_LIBRARY_PATH` is set.

### Root Cause (Updated — original diagnosis was incomplete)

**Primary cause: Homebrew libpng ABI mismatch.**

The user's `~/.zshrc` contains `export DYLD_LIBRARY_PATH="/opt/homebrew/lib"` (added for fluidsynth). This causes macOS's dynamic linker to load Homebrew's `libpng 1.6.50` for ImageIO's internal PNG plugin instead of Apple's private copy. The ABI mismatch between Homebrew libpng and Apple's internal ImageIO libpng corrupts `PNGReadPlugin::InitializePluginData()`, causing SIGBUS at `0x0BAD4007`.

This is the exact same root cause as:
- **wxWidgets #23547** — identical crash signature at `0xbad4007`
- **Electron #48025** — `0xBAD4007` in ImageIO during glyph rasterization
- **dotnet/sdk #44425** — crash when libpng is installed on macOS Sequoia
- **Tauri #7351** — app crashes on M1 Mac

**Contributing factor: high-frequency ImageIO usage.** The `_get_menubar_icon()` PIL→PNG→loadFromData pipeline exercised ImageIO 20x/sec during recording, and `setCursor` in `mouseMoveEvent`/AppKit's `_edgeResizingCursorUpdate` also routes through ImageIO for cursor bundle loading. The interleaving increases crash probability.

**Why the first fix was insufficient:** The first fix eliminated `loadFromData` from `_get_menubar_icon` and added cursor deduplication. This reduced ImageIO usage but didn't fix the root cause — the libpng ABI mismatch. The second crash log showed the crash in AppKit's own `_edgeResizingCursorUpdate:atLocation:`, which we have no control over. Any ImageIO PNG operation with Homebrew's libpng loaded can crash.

### Second Crash Log Analysis

The second crash occurred via a completely different code path:
```
_edgeResizingCursorUpdate:atLocation:  (AppKit internal)
  → _routeCursorUpdateEvent
  → setCursorFromBundle
  → CGImageSourceCreateImageAtIndex
  → IIOReadPlugin::callInitialize  → SIGBUS at 0x0BAD4007
```
This is AppKit's own cursor management, triggered during window resize. Our cursor deduplication is irrelevant to this path. The user confirmed: "once size goes to 0 it fails" — resizing the window down triggers AppKit's edge-resize cursor update, which loads cursor PNGs through the corrupted ImageIO.

### Fix (Complete — three layers of defense)

1. **`DYLD_LIBRARY_PATH` startup guard** (PRIMARY FIX): At the very top of `voice_thing.py`, before any imports, move `/opt/homebrew/lib` from `DYLD_LIBRARY_PATH` to `DYLD_FALLBACK_LIBRARY_PATH` and `os.execv()` re-exec the process. `FALLBACK` is searched after framework rpaths, so ImageIO loads Apple's private libpng first, but FluidSynth etc. still find their `.dylib` files. DYLD vars are only read at process start, so the re-exec ensures clean library resolution. (Initial version deleted the var entirely, which broke FluidSynth on the other laptop — WOM bug.)
2. **`_get_menubar_icon`**: Eliminated ImageIO entirely. Base icon loaded once via `QImage(path)` and cached in `_tray_icon_base`. Hue cycling done via `QPainter` with `CompositionMode_SourceAtop` — pure Qt compositor, no PNG encode/decode. Also ~100x faster per call. (Defense-in-depth.)
3. **Cursor deduplication**: `DraggableResizableMixin.mouseMoveEvent` tracks `_current_edge`, `TmuxSelectionDialog.eventFilter` tracks `_table_ibeam` — skip redundant `setCursor` calls. (Defense-in-depth.)

### External Corroboration

- **wxWidgets #23547**: Exact same crash signature (`PNGReadPlugin::InitializePluginData` at `0xbad4007`). Root cause was bitmap lifetime issue causing ImageIO memory corruption. Fix: avoid PNG/ImageIO entirely (switched to XPM format).
- **Qt forum Apple Silicon thread**: Crashes in ImageIO during `setCursorFromBundle` caused by data races exposed by ARM's stricter memory ordering model.
- Both confirm: the fix is to eliminate the ImageIO code path, not to add synchronization.

### How to Reproduce

**Prerequisites**: Homebrew libpng must be installed (`/opt/homebrew/lib/libpng.dylib`).

**Method 1: Automated stress test** (`tests/test_sigbus_repro.py`)
```bash
python3.10 tests/test_sigbus_repro.py
# Test 1: Launches subprocess with DYLD_LIBRARY_PATH=/opt/homebrew/lib
#          that interleaves QPixmap.loadFromData(PNG) + setCursor in QTimer
#          → Bus error: 10 (SIGBUS), 2-3/3 runs crash
# Test 2: Same stress test WITHOUT DYLD_LIBRARY_PATH → 0 crashes
# Test 3: Verifies the startup guard strips the env var via os.execv
```

**Method 2: Manual one-liner**
```bash
DYLD_LIBRARY_PATH="/opt/homebrew/lib" python3.10 -c "
from PyQt6.QtWidgets import QApplication, QWidget; from PyQt6.QtGui import QPixmap, QImage, QColor
from PyQt6.QtCore import Qt, QTimer, QBuffer, QIODevice; import sys
app = QApplication(sys.argv)
img = QImage(44, 44, QImage.Format.Format_ARGB32); img.fill(QColor(255,0,0,255))
buf = QBuffer(); buf.open(QIODevice.OpenModeFlag.WriteOnly); img.save(buf, 'PNG')
d = bytes(buf.data()); w = QWidget(); w.show()
def f():
    for i in range(50):
        p = QPixmap(); p.loadFromData(d); w.setCursor([Qt.CursorShape.ArrowCursor, Qt.CursorShape.SizeVerCursor][i%2])
t = QTimer(); t.timeout.connect(f); t.start(1); app.exec()
"
# → Bus error: 10 within seconds
```

**Method 3: Manual interaction**
Launch any PyQt6 app with `DYLD_LIBRARY_PATH="/opt/homebrew/lib"` and resize the window aggressively (especially toward zero size). AppKit's `_edgeResizingCursorUpdate` triggers ImageIO → crash.

**What does NOT crash** (controls):
- `loadFromData` alone (no cursor changes): survived 600k+ operations
- `setCursor` alone (no PNG loading): survived 664k+ operations
- Interleaved WITHOUT `DYLD_LIBRARY_PATH`: survived 500k+ operations
- All three require BOTH the libpng ABI mismatch AND interleaved ImageIO usage

### Lessons

- **Check `DYLD_LIBRARY_PATH` FIRST for any macOS ImageIO crash.** Homebrew's libpng in `/opt/homebrew/lib` has an ABI mismatch with Apple's internal copy. This is the #1 cause of `0xBAD4007` crashes across Qt, wxWidgets, Electron, .NET, and Tauri.
- **Never round-trip through PNG for rapid image updates.** The PIL→PNG→loadFromData pattern exercises ImageIO. For recoloring, use QPainter compositing instead.
- **`setCursor` on macOS goes through ImageIO** via `setCursorFromBundle`. Deduplicate calls.
- **The first fix was incomplete** because it reduced ImageIO usage but didn't address the root cause (libpng ABI mismatch). Always look for environmental causes before optimizing code paths.
- **AppKit's own cursor management also crashes** — `_edgeResizingCursorUpdate` is internal to AppKit and cannot be controlled from application code. The only fix is to prevent the bad library from loading.

### Files Changed

- `voice_thing.py`: DYLD_LIBRARY_PATH startup guard (top of file), `_get_menubar_icon`, `DraggableResizableMixin.mouseMoveEvent`, `eventFilter` in `TmuxSelectionDialog`

### Test Files

- `tests/test_sigbus_repro.py`: **Reproduces the actual SIGBUS crash** via subprocess with `DYLD_LIBRARY_PATH=/opt/homebrew/lib`. 3 tests: (1) crash WITH libpng mismatch, (2) no crash WITHOUT, (3) startup guard strips the env var.
- `tests/test_cursor_crash.py`: Proves old code uses ImageIO (loadFromData), new code avoids it entirely. Also verifies cursor deduplication and icon validity. 5 test cases.
- `tests/test_menubar_icon.py`: Verifies refactored `_get_menubar_icon` produces valid icons at all hue values with correct sizing.

---

## 2026-03-13: Menu bar dark mode detection wrong — using app appearance instead of status item

### The Bug

`_is_menubar_dark()` used `NSApplication.sharedApplication().effectiveAppearance()` which returns the system-wide dark mode setting, not the actual menu bar appearance. On macOS, the menu bar can be light even when the system is in dark mode — this happens when the desktop wallpaper behind the menu bar area is light. The result: tray icon colors were wrong (too bright/dark) when the menu bar appearance differed from the system setting.

### Root Cause

macOS Big Sur+ makes the menu bar translucent and determines its appearance (light/dark) based on the wallpaper brightness behind it, per display. `NSApplication.effectiveAppearance` only reflects the system-wide setting.

### Fix

Use a hidden `NSStatusItem` probe: `NSStatusBar.systemStatusBar().statusItemWithLength_(NSVariableStatusItemLength)` with `setVisible_(False)`. Its `button().effectiveAppearance()` reflects the actual menu bar appearance. Cached globally in `_menubar_appearance_probe`. Falls back to the old method if PyObjC fails.

### External References

- [yujitach/nsstatusitem-lightdark-detect](https://github.com/yujitach/nsstatusitem-lightdark-detect)
- [wxWidgets #19269](https://github.com/wxWidgets/wxWidgets/issues/19269)
- [Apple Developer Forums thread 652540](https://developer.apple.com/forums/thread/652540)

---

## 2026-03-13: Clear transcriptions/console — items reappear after clearing

### The Bug

When clearing transcriptions via Preferences > "Clear Transcriptions", items reappeared as soon as a new transcription was added. Same issue with "Clear Console".

### Root Cause

- **Transcriptions**: `TranscriptionList.clear()` removed widgets from the UI but did not clear `VoiceThingWindow.transcriptions` list (the in-memory data). When `add_transcription_signal` fired, the UI was rebuilt from this still-populated list.
- **Console**: `output_panel.clear()` cleared the QTextEdit text, but `_update_log()` (called on a timer) immediately repopulated it from `TeeOutput._buf` — the captured stdout buffer was never cleared.

### Fix

- `_clear_transcriptions`: now also clears `MAIN_WINDOW.transcriptions = []`
- `_clear_console`: now also clears `MAIN_WINDOW.tee._buf.clear()` and resets `MAIN_WINDOW._last_log_buf_len = 0`

### Lesson

UI clear operations must also clear the backing data source, not just the display widgets. Otherwise any refresh/update cycle will repopulate from stale data.

---

## 2026-03-13: Wrong rp function name — `clipboard_to_string` doesn't exist

### The Bug

`_append_to_clipboard` called `rp.clipboard_to_string()` which doesn't exist. The correct function is `rp.string_from_clipboard()`.

### Lesson

Always check actual rp API with grep before guessing function names. The rp clipboard convention is `string_to_clipboard` / `string_from_clipboard`, not the reverse naming.

---

## 2026-03-15: QTableWidget `::item:hover` CSS incompatible with cell widget columns

### The Bug

In the Tmux Pane Manager, the Voice column uses `setCellWidget` to place QComboBox dropdowns in each row. With `QTableWidget::item:hover { background: ... }` in the stylesheet, hovering over any cell — including over a QComboBox — causes the row's highlight to jump around visually. The user sees the highlighted row change just by moving the mouse over the voice dropdowns, which is distracting and feels broken.

### Root Cause

Qt's `::item:hover` pseudo-state applies to table items at the widget level. When a cell contains a cell widget (QComboBox), mouse events on that widget still propagate hover state to the underlying QTableWidgetItem. Combined with `setMouseTracking(True)`, every pixel of mouse movement triggers hover recalculation across all items. The result: the visual highlight follows the cursor even when the user is just trying to interact with a dropdown.

### Fix

Removed `QTableWidget::item:hover` CSS rule from the tmux pane table. Also removed `setMouseTracking(True)` and the viewport eventFilter (which were originally for hover-to-switch-preview, already removed). Selection highlight (`::item:selected`) still works on click.

### Lesson

`QTableWidget::item:hover` and `setCellWidget` don't mix well. If a table has interactive cell widgets (combo boxes, buttons), avoid hover CSS on the table items — hover state bleeds through the widget boundary. Use `::item:selected` for visual feedback instead.

---

## 2026-03-15: Whisper initial_prompt parroting on near-silent audio

### The Bug

User recorded ~0.4s of near-silence and got "muse workbench local" as transcription — words from tmux pane names that were nowhere in the audio.

### Root Cause

`_get_initial_prompt()` concatenates `S.CUSTOM_WORDS` + tmux pane phrase words and passes them to Whisper as `initial_prompt`. On near-silent audio (-47.8 dB, above the energy gate threshold), Whisper large-v3 hallucinates the prompt words back verbatim. Reproduced 10/10 times: without initial_prompt → returns "."; with initial_prompt → returns "muse workbench local".

### Fix

Added prompt parroting detection after Whisper transcription: if all result words are a subset of the initial_prompt words, the transcription is discarded as a hallucination.

### Lesson (also added to CLAUDE.md)

**No speculative fixes.** The initial attempt was an energy gate fix that wouldn't have caught this bug (-47.8 dB was above the threshold). Always reproduce and prove root cause before writing any fix.

---

## 2026-03-15: Speculative energy gate fix — unnecessary code shipped

### The Bug

After seeing the "muse workbench local" hallucination, a speculative energy gate was added to `_transcribe()` before the root cause was proven. The gate checked if audio energy was below -70 dB and skipped transcription. The actual audio was -47.8 dB — well above the threshold — so the gate would never have caught the real bug.

### Root Cause

Guessing before investigating. The energy gate was a reasonable hypothesis but was never tested against the actual failing audio before being committed.

### Fix

Removed the speculative energy gate after proving the real root cause (prompt parroting). Added CLAUDE.md rule: "No speculative fixes."

### Lesson

If you already wrote a speculative fix and later find the real cause, re-evaluate and remove anything that doesn't address it. Don't keep dead code just because it was already written.
