#!/usr/bin/env python3
"""
Terminal widget demo using termqt library.
termqt is a more complete terminal emulator than pyte.

Run with: python3.10 termqt_demo.py
"""

import os
import sys

# Set Qt API before importing
os.environ["QT_API"] = "pyqt6"

from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from PyQt6.QtCore import Qt
from termqt import Terminal, TerminalPOSIXExecIO


class TerminalWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("termqt Terminal Demo")
        self.resize(800, 500)

        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)
        layout.setContentsMargins(0, 0, 0, 0)

        # Create terminal widget (width, height in pixels, font_size)
        self.terminal = Terminal(800, 500, font_size=13)
        layout.addWidget(self.terminal)

        # Create IO backend for shell
        shell = os.environ.get("SHELL", "/bin/bash")
        # TerminalPOSIXExecIO(cols, rows, cmd)
        self.terminal_io = TerminalPOSIXExecIO(
            self.terminal.row_len,  # columns
            self.terminal.col_len,  # rows
            shell
        )

        # Connect terminal widget to IO backend:
        # - stdout_callback receives bytes from shell, send to terminal.stdout()
        # - terminal.input is set to write bytes to shell
        self.terminal_io.stdout_callback = self.terminal.stdout

        # Wrapper to handle both bytes and int (ControlChar values)
        def write_input(data):
            if isinstance(data, int):
                data = bytes([data])
            self.terminal_io.write(data)

        self.terminal.input = write_input

        # Connect terminal resize to PTY resize
        def on_terminal_resize(rows, cols):
            if self.terminal_io.running:
                self.terminal_io.resize(rows, cols)

        self.terminal.resize_callback = on_terminal_resize

        # Spawn the shell process
        self.terminal_io.spawn()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        # Terminal resize is handled by resize_callback

    def closeEvent(self, event):
        self.terminal_io.terminate()
        super().closeEvent(event)


def main():
    app = QApplication(sys.argv)
    window = TerminalWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
