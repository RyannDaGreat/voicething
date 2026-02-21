# Blue Mode Space Switch Bug — Concerns Log

## Problem
Opening PrefsDialog in blue mode (tmux fullscreen) causes macOS to switch away from the fullscreen Space.

## STATUS: FIXED (2026-02-21)

## Root Cause
Two interacting issues across multiple commits:

1. **Commit `2e27fffe`** added native-window-creating code:
   - `combo_box.setView(_make_styled_listview())` — eagerly creates Qt::Popup native windows
   - `_wakeword_options = QWidget()` container
   - `_enter_delay_container = QWidget()` container
   - `_silence_thresh_container = QWidget()` container

2. **Commit `22e14fb`** removed the compensating blue mode code:
   - Removed `WindowStaysOnTopHint` block from `center_on_parent()`
   - Removed blue mode parenting in `show_prefs()` (dialog parented to `self` instead of tmux dialog)

3. **Commit `6f403d1`** added another QWidget container:
   - `_ntfy_curl_widget` via `indented_widget()` (QWidget-based)

## Fix Applied (7 surgical changes)
Starting from `22e14fb` (all features), applied:

1. **Removed** `_make_styled_listview()` function and `setView()` call
2. **Added back** blue mode `WindowStaysOnTopHint` block in `center_on_parent()`
3. **Added back** blue mode parenting in `show_prefs()` (parent to tmux dialog)
4. **Removed** `_wakeword_options` QWidget container — items go directly on `self._layout`
5. **Removed** `_enter_delay_container` QWidget — plain QHBoxLayout
6. **Removed** `_silence_thresh_container` QWidget — plain QHBoxLayout
7. **Replaced** `_ntfy_curl_widget` (`indented_widget`/QWidget) with `indented_row` (layout-only)

## Critical Code (DO NOT REMOVE — comments in source)

### `DraggableDialog.center_on_parent()` — blue mode block
Sets `WindowStaysOnTopHint` and positions dialog on fullscreen Space.

### `VoiceThingWindow.show_prefs()` — blue mode parenting
Parents PrefsDialog to tmux dialog (not self) when in blue mode.

### `make_combobox_searchable()` — NO setView()
Do NOT call `combo_box.setView()` — creates native popup windows.

## Rules for Future Changes
- **Never wrap PrefsDialog widgets in QWidget containers** for show/hide — use individual widget `.setVisible()` or layout-based approaches (`indented_row` not `indented_widget`)
- **Never call `setView()` on QComboBox** — use stylesheet-only approach
- **Never remove the blue mode block** from `center_on_parent()` or the parenting from `show_prefs()`
- Use `indented_row()` (returns QHBoxLayout) instead of `indented_widget()` (returns QWidget) for new indented UI elements in PrefsDialog

## Lessons Learned
- Git bisect should be done FIRST — would have saved hours of manual widget bisection
- Multiple commits can interact: one adds the problem, another removes the compensation
- QWidget containers with children create native NSView backing on macOS
- `WindowStaysOnTopHint` is essential for keeping Qt dialogs on macOS fullscreen Spaces
- When partially reverting, always check what LATER commits removed from BEFORE the bug commit
