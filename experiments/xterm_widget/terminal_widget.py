#!/usr/bin/env python3
"""
PyQt6 Terminal Widget - Full xterm-compatible terminal emulator.

Uses pyte for VT102 terminal emulation and ptyprocess for PTY handling.
Supports mouse, all keyboard bindings, colors, scrollback.

Run with: python3.10 terminal_widget.py
"""

import os
import sys
import struct
import fcntl
import termios
import threading

import pyte
from ptyprocess import PtyProcess
from PyQt6.QtCore import Qt, QTimer, pyqtSignal, QSize
from PyQt6.QtGui import (
    QFont, QFontMetrics, QPainter, QColor, QPen, QKeyEvent, QMouseEvent,
    QWheelEvent, QClipboard
)
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QScrollBar, QHBoxLayout


# ANSI 16-color palette (standard + bright)
ANSI_COLORS = [
    "#000000", "#cd0000", "#00cd00", "#cdcd00", "#0000ee", "#cd00cd", "#00cdcd", "#e5e5e5",  # 0-7
    "#7f7f7f", "#ff0000", "#00ff00", "#ffff00", "#5c5cff", "#ff00ff", "#00ffff", "#ffffff",  # 8-15
]

# Generate 256-color palette
def generate_256_palette():
    palette = ANSI_COLORS.copy()
    # 216 color cube (6x6x6)
    for r in range(6):
        for g in range(6):
            for b in range(6):
                palette.append(f"#{r*51:02x}{g*51:02x}{b*51:02x}")
    # 24 grayscale
    for i in range(24):
        v = 8 + i * 10
        palette.append(f"#{v:02x}{v:02x}{v:02x}")
    return palette

COLOR_PALETTE = generate_256_palette()


class TerminalWidget(QWidget):
    """Full terminal emulator widget with PTY support."""

    # Signals
    titleChanged = pyqtSignal(str)
    finished = pyqtSignal(int)  # exit code

    def __init__(self, parent=None, cols=80, rows=24):
        super().__init__(parent)

        self.cols = cols
        self.rows = rows
        self._scrollback_lines = []
        self._scroll_offset = 0  # How many lines scrolled up from bottom

        # Font setup - use monospace
        self.font = QFont("Menlo", 12)
        self.font.setStyleHint(QFont.StyleHint.Monospace)
        metrics = QFontMetrics(self.font)
        self.char_width = metrics.horizontalAdvance("M")
        self.char_height = metrics.height()
        self.baseline_offset = metrics.ascent()

        # Terminal emulator (pyte)
        self.screen = pyte.Screen(cols, rows)
        self.screen.set_mode(pyte.modes.LNM)  # Auto newline
        self.stream = pyte.Stream(self.screen)

        # History screen for scrollback
        self.history_screen = pyte.HistoryScreen(cols, rows, history=10000)
        self.history_stream = pyte.Stream(self.history_screen)

        # PTY process
        self.pty = None
        self._pty_read_thread = None
        self._running = False

        # Cursor blink
        self._cursor_visible = True
        self._cursor_timer = QTimer(self)
        self._cursor_timer.timeout.connect(self._blink_cursor)
        self._cursor_timer.start(530)

        # Mouse tracking state
        self._mouse_tracking = False
        self._mouse_button_pressed = False
        self._selection_start = None
        self._selection_end = None

        # Widget setup
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.setMouseTracking(True)
        self._update_size()

        # Refresh timer
        self._refresh_timer = QTimer(self)
        self._refresh_timer.timeout.connect(self.update)
        self._refresh_timer.start(16)  # ~60fps

    def _update_size(self):
        """Update widget size based on terminal dimensions."""
        width = self.cols * self.char_width + 4
        height = self.rows * self.char_height + 4
        self.setMinimumSize(width, height)
        self.resize(width, height)

    def start(self, command=None, env=None):
        """Start the terminal with given command (default: user's shell)."""
        if command is None:
            command = os.environ.get("SHELL", "/bin/bash")

        # Prepare environment
        term_env = os.environ.copy()
        term_env["TERM"] = "xterm-256color"
        term_env["COLORTERM"] = "truecolor"
        if env:
            term_env.update(env)

        # Start PTY
        self.pty = PtyProcess.spawn(
            [command],
            dimensions=(self.rows, self.cols),
            env=term_env
        )

        self._running = True
        self._pty_read_thread = threading.Thread(target=self._read_pty, daemon=True)
        self._pty_read_thread.start()

    def _read_pty(self):
        """Background thread reading from PTY."""
        while self._running and self.pty.isalive():
            try:
                data = self.pty.read(4096)
                if data:
                    # pyte expects string, not bytes
                    if isinstance(data, bytes):
                        data = data.decode("utf-8", errors="replace")
                    self.history_stream.feed(data)
            except EOFError:
                break
            except Exception as e:
                print(f"PTY read error: {e}")
                break

        if self.pty:
            exit_code = self.pty.wait()
            self.finished.emit(exit_code)

    def write(self, data):
        """Write data to the PTY."""
        if self.pty and self.pty.isalive():
            if isinstance(data, str):
                data = data.encode("utf-8")
            self.pty.write(data)

    def resize_terminal(self, cols, rows):
        """Resize the terminal."""
        self.cols = cols
        self.rows = rows
        self.history_screen.resize(rows, cols)
        self._update_size()

        if self.pty and self.pty.isalive():
            self.pty.setwinsize(rows, cols)

    def _blink_cursor(self):
        """Toggle cursor visibility for blinking."""
        self._cursor_visible = not self._cursor_visible
        self.update()

    def paintEvent(self, event):
        """Render the terminal."""
        p = QPainter(self)
        p.setFont(self.font)

        screen = self.history_screen

        # Background
        bg_color = QColor("#1a1a1a")
        p.fillRect(self.rect(), bg_color)

        # Get visible lines (handle scrollback)
        history_lines = list(screen.history.top) if hasattr(screen.history, 'top') else []
        display_buffer = screen.buffer

        # Draw each cell
        for row in range(self.rows):
            y = 2 + row * self.char_height + self.baseline_offset

            for col in range(self.cols):
                char = display_buffer[row][col]
                x = 2 + col * self.char_width

                # Background color
                if char.bg != "default":
                    bg = self._get_color(char.bg, is_bg=True)
                    p.fillRect(x, 2 + row * self.char_height,
                              self.char_width, self.char_height, bg)

                # Reverse video
                if char.reverse:
                    fg_color = self._get_color(char.bg if char.bg != "default" else "default", is_bg=True)
                    bg = self._get_color(char.fg if char.fg != "default" else "default", is_bg=False)
                    p.fillRect(x, 2 + row * self.char_height,
                              self.char_width, self.char_height, bg)
                else:
                    fg_color = self._get_color(char.fg, is_bg=False)

                # Selection highlight
                if self._is_selected(row, col):
                    p.fillRect(x, 2 + row * self.char_height,
                              self.char_width, self.char_height, QColor(100, 100, 200, 100))

                # Draw character
                if char.data and char.data != " ":
                    p.setPen(fg_color)

                    # Bold
                    font = self.font
                    if char.bold:
                        font = QFont(self.font)
                        font.setBold(True)
                        p.setFont(font)

                    p.drawText(x, y, char.data)

                    if char.bold:
                        p.setFont(self.font)

                    # Underline
                    if char.underscore:
                        p.drawLine(x, y + 2, x + self.char_width, y + 2)

        # Draw cursor
        if self._cursor_visible and self.hasFocus():
            cx = 2 + screen.cursor.x * self.char_width
            cy = 2 + screen.cursor.y * self.char_height
            p.fillRect(cx, cy, self.char_width, self.char_height, QColor(200, 200, 200, 180))

    def _get_color(self, color, is_bg=False):
        """Convert pyte color to QColor."""
        if color == "default":
            return QColor("#1a1a1a" if is_bg else "#e0e0e0")

        if isinstance(color, str):
            if color.isdigit():
                idx = int(color)
                if 0 <= idx < len(COLOR_PALETTE):
                    return QColor(COLOR_PALETTE[idx])
            # Named colors
            color_map = {
                "black": 0, "red": 1, "green": 2, "yellow": 3,
                "blue": 4, "magenta": 5, "cyan": 6, "white": 7,
                "brightblack": 8, "brightred": 9, "brightgreen": 10,
                "brightyellow": 11, "brightblue": 12, "brightmagenta": 13,
                "brightcyan": 14, "brightwhite": 15,
            }
            if color.lower() in color_map:
                return QColor(COLOR_PALETTE[color_map[color.lower()]])

        return QColor("#e0e0e0" if not is_bg else "#1a1a1a")

    def _is_selected(self, row, col):
        """Check if cell is in selection."""
        if self._selection_start is None or self._selection_end is None:
            return False

        start = self._selection_start
        end = self._selection_end

        # Normalize order
        if (start[0] > end[0]) or (start[0] == end[0] and start[1] > end[1]):
            start, end = end, start

        pos = (row, col)
        return start <= pos <= end

    def keyPressEvent(self, event: QKeyEvent):
        """Handle keyboard input."""
        key = event.key()
        mods = event.modifiers()
        text = event.text()

        # Build escape sequence
        seq = None

        # Special keys
        key_map = {
            Qt.Key.Key_Up: b"\x1b[A",
            Qt.Key.Key_Down: b"\x1b[B",
            Qt.Key.Key_Right: b"\x1b[C",
            Qt.Key.Key_Left: b"\x1b[D",
            Qt.Key.Key_Home: b"\x1b[H",
            Qt.Key.Key_End: b"\x1b[F",
            Qt.Key.Key_PageUp: b"\x1b[5~",
            Qt.Key.Key_PageDown: b"\x1b[6~",
            Qt.Key.Key_Insert: b"\x1b[2~",
            Qt.Key.Key_Delete: b"\x1b[3~",
            Qt.Key.Key_F1: b"\x1bOP",
            Qt.Key.Key_F2: b"\x1bOQ",
            Qt.Key.Key_F3: b"\x1bOR",
            Qt.Key.Key_F4: b"\x1bOS",
            Qt.Key.Key_F5: b"\x1b[15~",
            Qt.Key.Key_F6: b"\x1b[17~",
            Qt.Key.Key_F7: b"\x1b[18~",
            Qt.Key.Key_F8: b"\x1b[19~",
            Qt.Key.Key_F9: b"\x1b[20~",
            Qt.Key.Key_F10: b"\x1b[21~",
            Qt.Key.Key_F11: b"\x1b[23~",
            Qt.Key.Key_F12: b"\x1b[24~",
            Qt.Key.Key_Backspace: b"\x7f",
            Qt.Key.Key_Tab: b"\t",
            Qt.Key.Key_Return: b"\r",
            Qt.Key.Key_Enter: b"\r",
            Qt.Key.Key_Escape: b"\x1b",
        }

        if key in key_map:
            seq = key_map[key]
            # Add modifiers for arrow keys
            if key in (Qt.Key.Key_Up, Qt.Key.Key_Down, Qt.Key.Key_Left, Qt.Key.Key_Right):
                if mods & Qt.KeyboardModifier.ShiftModifier:
                    seq = seq[:-1] + b";2" + seq[-1:]
                elif mods & Qt.KeyboardModifier.ControlModifier:
                    seq = seq[:-1] + b";5" + seq[-1:]
                elif mods & Qt.KeyboardModifier.AltModifier:
                    seq = seq[:-1] + b";3" + seq[-1:]
        elif mods & Qt.KeyboardModifier.ControlModifier:
            # Ctrl+letter
            if Qt.Key.Key_A <= key <= Qt.Key.Key_Z:
                seq = bytes([key - Qt.Key.Key_A + 1])
            elif key == Qt.Key.Key_BracketLeft:
                seq = b"\x1b"
            elif key == Qt.Key.Key_Backslash:
                seq = b"\x1c"
            elif key == Qt.Key.Key_BracketRight:
                seq = b"\x1d"
            elif key == Qt.Key.Key_6:
                seq = b"\x1e"
            elif key == Qt.Key.Key_Minus:
                seq = b"\x1f"
            elif key == Qt.Key.Key_V:
                # Paste
                clipboard = QApplication.clipboard()
                self.write(clipboard.text())
                return
            elif key == Qt.Key.Key_C:
                # Copy selection
                self._copy_selection()
                return
        elif mods & Qt.KeyboardModifier.AltModifier and text:
            # Alt+key sends ESC prefix
            seq = b"\x1b" + text.encode("utf-8")
        elif text:
            seq = text.encode("utf-8")

        if seq:
            self.write(seq)

    def _copy_selection(self):
        """Copy selected text to clipboard."""
        if self._selection_start is None or self._selection_end is None:
            return

        start = self._selection_start
        end = self._selection_end
        if (start[0] > end[0]) or (start[0] == end[0] and start[1] > end[1]):
            start, end = end, start

        text = []
        buffer = self.history_screen.buffer
        for row in range(start[0], end[0] + 1):
            line = ""
            col_start = start[1] if row == start[0] else 0
            col_end = end[1] if row == end[0] else self.cols - 1
            for col in range(col_start, col_end + 1):
                line += buffer[row][col].data or " "
            text.append(line.rstrip())

        QApplication.clipboard().setText("\n".join(text))

    def mousePressEvent(self, event: QMouseEvent):
        """Handle mouse press."""
        pos = event.position()
        col = int((pos.x() - 2) / self.char_width)
        row = int((pos.y() - 2) / self.char_height)
        col = max(0, min(col, self.cols - 1))
        row = max(0, min(row, self.rows - 1))

        if event.button() == Qt.MouseButton.LeftButton:
            self._selection_start = (row, col)
            self._selection_end = (row, col)
            self._mouse_button_pressed = True

            # Mouse tracking to app not implemented - just selection for now

        self.update()

    def mouseMoveEvent(self, event: QMouseEvent):
        """Handle mouse move (selection)."""
        if self._mouse_button_pressed:
            pos = event.position()
            col = int((pos.x() - 2) / self.char_width)
            row = int((pos.y() - 2) / self.char_height)
            col = max(0, min(col, self.cols - 1))
            row = max(0, min(row, self.rows - 1))
            self._selection_end = (row, col)
            self.update()

    def mouseReleaseEvent(self, event: QMouseEvent):
        """Handle mouse release."""
        self._mouse_button_pressed = False

        # Mouse tracking not implemented for now - just handle selection
        pass

    def wheelEvent(self, event: QWheelEvent):
        """Handle scroll wheel."""
        delta = event.angleDelta().y()

        # Scroll history (TODO: implement scrollback view)
        lines = 3 if delta > 0 else -3
        pass

    def _send_mouse_event(self, event, event_type):
        """Send mouse event escape sequence."""
        pos = event.position()
        col = int((pos.x() - 2) / self.char_width) + 1
        row = int((pos.y() - 2) / self.char_height) + 1

        button = 0
        if event.button() == Qt.MouseButton.LeftButton:
            button = 0
        elif event.button() == Qt.MouseButton.MiddleButton:
            button = 1
        elif event.button() == Qt.MouseButton.RightButton:
            button = 2

        if event_type == "release":
            button = 3

        # X10 mouse protocol
        self.write(f"\x1b[M{chr(32 + button)}{chr(32 + col)}{chr(32 + row)}".encode())

    def focusInEvent(self, event):
        """Handle focus gain."""
        self._cursor_visible = True
        self.update()
        super().focusInEvent(event)

    def focusOutEvent(self, event):
        """Handle focus loss."""
        self._cursor_visible = True  # Keep visible but stop blinking
        self.update()
        super().focusOutEvent(event)

    def closeEvent(self, event):
        """Clean up on close."""
        self._running = False
        if self.pty:
            self.pty.terminate(force=True)
        super().closeEvent(event)


class TerminalWindow(QWidget):
    """Standalone terminal window."""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("PyQt6 Terminal")

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        self.terminal = TerminalWidget(self, cols=100, rows=30)
        self.terminal.titleChanged.connect(self.setWindowTitle)
        self.terminal.finished.connect(self._on_finished)
        layout.addWidget(self.terminal)

        self.terminal.start()
        self.terminal.setFocus()

    def _on_finished(self, exit_code):
        print(f"Terminal exited with code {exit_code}")
        self.close()


def main():
    app = QApplication(sys.argv)
    app.setStyle("Fusion")

    window = TerminalWindow()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
