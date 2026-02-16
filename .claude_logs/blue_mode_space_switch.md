# Blue Mode Space Switch Bug — Concerns Log

## Problem
Opening PrefsDialog in blue mode (tmux fullscreen) causes macOS to switch away from the fullscreen Space. Opening ChimeEditorDialog does NOT.

## Root Cause (confirmed via git bisect)
Commit `2e27fffe` ("stylefix") introduced the bug. The commit before it has NO window issue.

### What that commit changed:
1. **`_make_styled_listview()` + `combo_box.setView()`** — Replaced default QComboBox view with custom QListView, eagerly creating `QComboBoxPrivateContainer` (Qt::Popup native window) during construction
2. **`_enter_delay_container = QWidget()`** — Wrapped enter delay slider in QWidget container (was plain QHBoxLayout before)
3. **`_silence_thresh_container = QWidget()`** — Wrapped silence threshold slider in QWidget container
4. **`_wakeword_options = QWidget()`** — Wrapped all wakeword settings in QWidget container
5. Also: tmux_toggle shortcut, improved tooltips, "Auto" label (these are fine)

## Investigation Timeline

### Session 1 (prior conversation)
- 5-agent frenzy identified suspects (setView, QWidget containers, completer.popup())
- Pre-cached macOS voices at startup (Fix 1)
- Deferred make_combobox_searchable internals (Fix 2)
- Status: waiting for test

### Session 2 (this conversation, 2026-02-21)
Exhaustive bisection of right column:

| Test | Result |
|------|--------|
| Empty right column | WORKS |
| 30 QLabels + wide text | WORKS |
| Single QComboBox | WORKS |
| Two searchable QComboBoxes | WORKS |
| WakeWordSettingsWidget alone | WORKS |
| Paste section alone | WORKS |
| WakeWord + Paste together | WORKS |
| Enter Delay bare slider (no container) | WORKS |
| Enter Delay in QWidget container | **FAILS** |
| Empty QWidget() | WORKS |
| QWidget() with empty QHBoxLayout | WORKS |
| QWidget() with QHBoxLayout + child | **FAILS** |
| Sections 1-6 (top half) | **FAILS** |
| Sections 7-11 (bottom half) | **FAILS** |
| Sections 1-3 | **FAILS** |

Key finding: QWidget with layout + child widget = FAILS. Bare widgets = WORKS.

### Fixes attempted (all FAILED):
1. **WidgetGroup class** — Replace QWidget containers with show/hide of individual widgets. Did NOT fix.
2. **Qt.WindowType.Tool** — Use NSPanel instead of NSWindow. FAILED.
3. **AA_DontCreateNativeWidgetSiblings** — App-level attribute. FAILED.
4. **WA_DontCreateNativeAncestors** — Widget-level attribute. FAILED.
5. **Remove activateWindow()** — FAILED.
6. **All combined** — FAILED.
7. **Convert pet QWidgets to nested layouts** — FAILED.
8. **Manual revert of 2e27fff's 3 problematic changes** — Still FAILED (single switch instead of 5-7 flails, but still switches).

### Symptom detail
- The Space switch isn't a single switch — it rapidly flails 6-7 times before settling on a different desktop
- This count was consistent across many tests
- After manual partial revert: reduced to single switch but still fails

### Current state (2026-02-21)
- Full file replacement with known-good version from `2e27fffe~1` (pre-bug)
- This loses 9 commits of features (boot chime, refactors, settings, autoyes, etc.)
- Waiting for user test to confirm this baseline works
- If confirmed: need to surgically re-apply non-problematic changes from those 9 commits

### Later commits that may also contribute:
- `indented_widget()` calls in TTSSettingsWidget create QWidget containers (added after 2e27fff)
- `_ntfy_curl_widget` and `_ntfy_topic_widget` are QWidget containers in left column
- These are in the LEFT column which works alone, but may contribute when combined with right column

## Lessons Learned
- Git bisect should have been done FIRST instead of spending hours on manual widget-by-widget bisection
- The 6-7 rapid Space switches corresponded to multiple native window creation events
- Manual partial reverts can miss interactions between changes
- QWidget containers with children create native NSView backing on macOS that can trigger Space switching in fullscreen
