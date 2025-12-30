#!/usr/bin/env /opt/homebrew/opt/python@3.10/bin/python3.10
"""Voice transcription: double-tap Option to record, transcribe, and type."""

import io
import os
import signal
import subprocess
import sys
import tempfile
import threading
import time
from datetime import datetime
from functools import partial

import numpy as np
import rp


class TeeOutput:
    """Captures stdout/stderr including C output via fd redirection."""

    def __init__(self):
        self._buf = []
        self._orig_fd = os.dup(1)
        self._pipe_r, self._pipe_w = os.pipe()

    def __enter__(self):
        os.dup2(self._pipe_w, 1)
        os.dup2(self._pipe_w, 2)
        threading.Thread(target=self._read, daemon=True).start()
        return self

    def _read(self):
        while True:
            data = os.read(self._pipe_r, 16)
            if not data:
                break
            self._buf.append(data.decode('utf-8', errors='replace'))
            os.write(self._orig_fd, data)

    @property
    def text(self):
        return ''.join(self._buf)
import scipy.io.wavfile
import sounddevice as sd
from AppKit import NSWorkspace, NSApplicationActivateIgnoringOtherApps
from pynput import keyboard
from pynput.keyboard import Controller as KeyboardController, Key
from PyQt6.QtCore import Qt, QTimer, pyqtSignal, QSize, QPoint
from PyQt6.QtGui import QPainter, QColor, QPen, QIcon, QPixmap, QFontDatabase, QPolygon
from PyQt6.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QSystemTrayIcon,
    QMenu,
    QPushButton,
    QStackedWidget,
    QTextEdit,
    QDialog,
    QFileDialog,
)

APP_NAME = "VoiceThing"
SAMPLE_RATE = 16000
BLOCKSIZE = 256
WHISPER_MODEL = "large-v3"
ICON_COLOR = QColor(255, 255, 255, 255)
ACCENT = QColor(100, 200, 255)
RECORDINGS_DIR = os.path.join(tempfile.gettempdir(), APP_NAME)

# Shared styling for buttons and tabs
BTN_CSS = (
    "QPushButton { color: rgba(255,255,255,0.6); background: rgba(255,255,255,0.1); "
    "border: 1px solid rgb(100,100,100); border-radius: 3px; padding: 1px 2px; font-size: 10px; }"
    "QPushButton:hover { background: rgba(255,255,255,0.2); }"
    "QPushButton:disabled { color: rgba(255,255,255,0.2); background: transparent; }"
    "QPushButton:checked { background: rgba(100,200,255,0.3); }"
)

def quiet_sampler(f=None, T=None, samplerate=None):
    return rp.triangle_tone_sampler(f, T, samplerate) * 0.25

chime = partial(rp.play_chords, gap=0, sampler=quiet_sampler, block=True)


def draw_mic(p, s):
    p.setBrush(ICON_COLOR)
    p.setPen(Qt.PenStyle.NoPen)
    p.drawEllipse(s // 3, s // 6, s // 3, s // 2)
    p.drawRect(s * 5 // 12, s // 2, s // 6, s // 6)
    p.setBrush(Qt.BrushStyle.NoBrush)
    p.setPen(QPen(ICON_COLOR, 2))
    p.drawArc(s // 4, s // 3, s // 2, s // 2, 0, -180 * 16)


def draw_stop(p, s):
    p.setBrush(ICON_COLOR)
    p.setPen(Qt.PenStyle.NoPen)
    m = s // 4
    p.drawRect(m, m, s - 2 * m, s - 2 * m)


def draw_x(p, s):
    p.setPen(QPen(ICON_COLOR, 2))
    m = s // 4
    p.drawLine(m, m, s - m, s - m)
    p.drawLine(s - m, m, m, s - m)


def draw_help(p, s):
    """Open book icon - viewed from above with curved pages."""
    from PyQt6.QtGui import QPainterPath
    p.setPen(QPen(ICON_COLOR, 1.5))
    p.setBrush(Qt.BrushStyle.NoBrush)
    cx, cy = s // 2, s * 2 // 3
    # Left page (curved)
    left = QPainterPath()
    left.moveTo(cx, cy)
    left.quadTo(s // 4, s // 3, s // 6, s // 4)
    left.lineTo(s // 8, s * 3 // 5)
    left.quadTo(s // 3, s // 2, cx, cy)
    p.drawPath(left)
    # Right page (curved)
    right = QPainterPath()
    right.moveTo(cx, cy)
    right.quadTo(s * 3 // 4, s // 3, s * 5 // 6, s // 4)
    right.lineTo(s * 7 // 8, s * 3 // 5)
    right.quadTo(s * 2 // 3, s // 2, cx, cy)
    p.drawPath(right)


def draw_folder(p, s):
    p.setBrush(ICON_COLOR)
    p.setPen(Qt.PenStyle.NoPen)
    m = s // 6
    p.drawRoundedRect(m, s // 3, s - 2 * m, s // 2, 2, 2)
    p.drawRoundedRect(m, s // 4, s // 3, s // 6, 2, 2)


def draw_load(p, s):
    """Draw a CD icon."""
    cx, cy = s // 2, s // 2
    r = s // 3
    # Outer circle
    p.setBrush(Qt.BrushStyle.NoBrush)
    p.setPen(QPen(ICON_COLOR, 2))
    p.drawEllipse(cx - r, cy - r, r * 2, r * 2)
    # Inner hole
    hole_r = s // 10
    p.drawEllipse(cx - hole_r, cy - hole_r, hole_r * 2, hole_r * 2)


def draw_copy(p, s):
    p.setBrush(Qt.BrushStyle.NoBrush)
    p.setPen(QPen(ICON_COLOR, 2))
    m = s // 5
    p.drawRoundedRect(m, m, s // 2, s // 2, 2, 2)
    p.drawRoundedRect(s // 3, s // 3, s // 2, s // 2, 2, 2)


def draw_eye(p, s, open=True):
    """Draw an eye icon - open when visible, closed/slashed when auto-hide."""
    cx, cy = s // 2, s // 2
    # Eye outline (almond shape)
    p.setBrush(Qt.BrushStyle.NoBrush)
    p.setPen(QPen(ICON_COLOR, 2))
    # Draw eye shape using arcs
    p.drawEllipse(s // 6, s // 3, s * 2 // 3, s // 3)
    if open:
        # Pupil
        p.setBrush(ICON_COLOR)
        p.setPen(Qt.PenStyle.NoPen)
        p.drawEllipse(cx - s // 8, cy - s // 8, s // 4, s // 4)
    else:
        # Slash through eye
        p.setPen(QPen(ICON_COLOR, 2))
        p.drawLine(s // 4, s * 3 // 4, s * 3 // 4, s // 4)


def draw_sound(p, s, enabled=True):
    """Draw a speaker icon, with slash when muted."""
    p.setBrush(ICON_COLOR)
    p.setPen(Qt.PenStyle.NoPen)
    # Speaker body
    m = s // 4
    p.drawRect(m, s * 3 // 8, s // 6, s // 4)
    # Speaker cone
    pts = QPolygon([
        QPoint(m + s // 6, s * 3 // 8),
        QPoint(m + s // 3, s // 4),
        QPoint(m + s // 3, s * 3 // 4),
        QPoint(m + s // 6, s * 5 // 8),
    ])
    p.drawPolygon(pts)
    # Sound waves
    if enabled:
        p.setBrush(Qt.BrushStyle.NoBrush)
        p.setPen(QPen(ICON_COLOR, 2))
        p.drawArc(s // 2, s // 3, s // 5, s // 3, 45 * 16, -90 * 16)
        p.drawArc(s // 2 + s // 8, s // 4, s // 4, s // 2, 45 * 16, -90 * 16)
    else:
        # Mute slash
        p.setPen(QPen(ICON_COLOR, 2))
        p.drawLine(s * 3 // 4, s // 4, s // 4, s * 3 // 4)


def draw_model(p, s):
    """Draw a robot head icon."""
    p.setBrush(Qt.BrushStyle.NoBrush)
    p.setPen(QPen(ICON_COLOR, 2))
    m = s // 6
    # Head (rounded rectangle)
    p.drawRoundedRect(m, m + s // 8, s - 2 * m, s - 2 * m - s // 8, 3, 3)
    # Antenna
    p.drawLine(s // 2, m + s // 8, s // 2, m)
    p.setBrush(ICON_COLOR)
    p.drawEllipse(s // 2 - 2, m - 2, 4, 4)
    # Eyes
    p.drawEllipse(s // 3 - 2, s // 2 - 2, 5, 5)
    p.drawEllipse(s * 2 // 3 - 3, s // 2 - 2, 5, 5)


def make_icon(draw_fn, size=64):
    px = QPixmap(size, size)
    px.fill(Qt.GlobalColor.transparent)
    p = QPainter(px)
    p.setRenderHint(QPainter.RenderHint.Antialiasing)
    draw_fn(p, size)
    p.end()
    return QIcon(px)


WHISPER_MODELS = [
    ("T", "tiny", "Fastest, least accurate (~1GB VRAM)"),
    ("B", "base", "Fast, basic accuracy (~1GB VRAM)"),
    ("S", "small", "Balanced speed/accuracy (~2GB VRAM)"),
    ("M", "medium", "Good accuracy, slower (~5GB VRAM)"),
    ("L", "large-v3", "Best accuracy, slowest (~10GB VRAM)"),
]

# Button definitions: (key, icon_fn, description)
# Used for creating buttons and help dialog (DRY)
BUTTONS = [
    ("Space", draw_mic, "Start/finish recording"),
    ("X", draw_x, "Cancel recording"),
    ("Esc", None, "Minimize window"),
    ("C", draw_copy, "Copy last transcription to clipboard"),
    ("L", draw_load, "Load audio file to transcribe"),
    ("F", draw_folder, "Open recordings folder"),
    ("S", draw_sound, "Toggle sound effects"),
    ("V", draw_eye, "Toggle auto-minimize after transcription"),
    ("M", draw_model, "Change Whisper model"),
    ("?", draw_help, "Show this help"),
]

# Tab definitions
TABS = [
    ("O", "Output", "Show console output"),
    ("T", "Transcriptions", "Show transcription history"),
]


GITHUB_URL = "https://github.com/RyannDaGreat/VoiceThing"


class HelpDialog(QDialog):
    """Help dialog with about info and keymap."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.drag_pos = None
        self.setWindowTitle("Help")
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.Dialog)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(10)

        # Title
        title = QLabel(APP_NAME)
        title.setStyleSheet("color: white; font-size: 18px; font-weight: bold;")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)

        # Main content: About | Keymap
        content = QHBoxLayout()
        content.setSpacing(15)

        # Left side: About
        about_box = QVBoxLayout()
        about_label = QLabel("About")
        about_label.setStyleSheet("color: rgb(100,200,255); font-size: 12px; font-weight: bold;")
        about_box.addWidget(about_label)

        about_text = QLabel(
            "Voice transcription powered by Whisper.\n\n"
            "• Double-tap Option to record from anywhere (works in fullscreen apps and terminals!)\n"
            "• Double-tap Option again to stop and auto-paste the transcription via Cmd+V\n"
            "• Cmd + double-tap Option to toggle focus\n"
            "• Access from menu bar (top right of Mac)\n"
            "• Drag & drop audio files to transcribe\n"
            "• Cmd+Q to quit\n\n"
            "100% keyboard-driven - no mouse needed! (hover buttons to see shortcuts)\n\n"
            "Pro tip: Right-click in Transcriptions tab to copy a single transcription.\n\n"
            "By Clara Burgert"
        )
        about_text.setStyleSheet("color: rgba(255,255,255,0.7); font-size: 10px;")
        about_text.setWordWrap(True)
        about_text.setFixedWidth(190)
        about_box.addWidget(about_text)
        about_box.addStretch()

        # GitHub button
        github_btn = QPushButton("GitHub")
        github_btn.setStyleSheet(BTN_CSS)
        github_btn.clicked.connect(lambda: subprocess.run(["open", GITHUB_URL]))
        about_box.addWidget(github_btn)

        content.addLayout(about_box)

        # Separator
        sep = QLabel()
        sep.setFixedWidth(1)
        sep.setStyleSheet("background: rgba(255,255,255,0.2);")
        content.addWidget(sep)

        # Right side: Keymap
        keymap_box = QVBoxLayout()
        keymap_label = QLabel("Keymap")
        keymap_label.setStyleSheet("color: rgb(100,200,255); font-size: 12px; font-weight: bold;")
        keymap_box.addWidget(keymap_label)

        for key, icon_fn, description in BUTTONS:
            row = QHBoxLayout()
            row.setSpacing(4)
            btn = QPushButton(key)
            if icon_fn:
                btn.setIcon(make_icon(icon_fn))
                btn.setIconSize(QSize(14, 14))
            btn.setStyleSheet(BTN_CSS)
            btn.setFixedWidth(60)
            btn.setEnabled(False)
            row.addWidget(btn)
            lbl = QLabel(description)
            lbl.setStyleSheet("color: rgba(255,255,255,0.7); font-size: 9px;")
            row.addWidget(lbl, 1)
            keymap_box.addLayout(row)

        for key, name, description in TABS:
            row = QHBoxLayout()
            row.setSpacing(4)
            btn = QPushButton(f"{key}")
            btn.setStyleSheet(BTN_CSS)
            btn.setFixedWidth(60)
            btn.setEnabled(False)
            row.addWidget(btn)
            lbl = QLabel(f"{name} tab")
            lbl.setStyleSheet("color: rgba(255,255,255,0.7); font-size: 9px;")
            row.addWidget(lbl, 1)
            keymap_box.addLayout(row)

        keymap_box.addStretch()
        content.addLayout(keymap_box)

        layout.addLayout(content)

        # Close button
        close_btn = QPushButton("Esc  Close")
        close_btn.setStyleSheet(BTN_CSS)
        close_btn.clicked.connect(self.accept)
        layout.addWidget(close_btn)

        self.setFixedWidth(480)

    def keyPressEvent(self, e):
        if e.key() in (Qt.Key.Key_Escape, Qt.Key.Key_Question):
            self.accept()
        else:
            super().keyPressEvent(e)

    def mousePressEvent(self, e):
        if e.button() == Qt.MouseButton.LeftButton:
            self.drag_pos = e.globalPosition().toPoint() - self.frameGeometry().topLeft()

    def mouseMoveEvent(self, e):
        if self.drag_pos and e.buttons() & Qt.MouseButton.LeftButton:
            self.move(e.globalPosition().toPoint() - self.drag_pos)

    def mouseReleaseEvent(self, e):
        self.drag_pos = None

    def paintEvent(self, e):
        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)
        p.setBrush(QColor(30, 30, 40, 255))
        p.setPen(QPen(QColor(100, 100, 100), 1))
        p.drawRoundedRect(self.rect().adjusted(1, 1, -1, -1), 10, 10)


class ModelDialog(QDialog):
    """Dialog to select Whisper model with keyboard shortcuts."""

    def __init__(self, current_model, parent=None):
        super().__init__(parent)
        self.selected_model = None
        self.setWindowTitle("Select Model")
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.Dialog)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(8)

        title = QLabel("Select Whisper Model")
        title.setStyleSheet("color: white; font-size: 14px; font-weight: bold;")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)

        for key, model, desc in WHISPER_MODELS:
            btn = QPushButton(f"{key}  {model}")
            btn.setStyleSheet(BTN_CSS)
            btn.setToolTip(desc)
            if model == current_model:
                btn.setStyleSheet(BTN_CSS + "QPushButton { border: 2px solid rgb(100,200,255); }")
            btn.clicked.connect(lambda checked, m=model: self._select(m))
            layout.addWidget(btn)

        cancel_btn = QPushButton("Esc  Cancel")
        cancel_btn.setStyleSheet(BTN_CSS)
        cancel_btn.clicked.connect(self.reject)
        layout.addWidget(cancel_btn)

        self.setFixedWidth(250)

    def _select(self, model):
        self.selected_model = model
        self.accept()

    def keyPressEvent(self, e):
        key = e.key()
        key_map = {Qt.Key.Key_T: "tiny", Qt.Key.Key_B: "base", Qt.Key.Key_S: "small",
                   Qt.Key.Key_M: "medium", Qt.Key.Key_L: "large-v3"}
        if key in key_map:
            self._select(key_map[key])
        elif key == Qt.Key.Key_Escape:
            self.reject()
        else:
            super().keyPressEvent(e)

    def paintEvent(self, e):
        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)
        p.setBrush(QColor(30, 30, 40, 240))
        p.setPen(QPen(QColor(100, 100, 100), 1))
        p.drawRoundedRect(self.rect().adjusted(1, 1, -1, -1), 10, 10)


class TextPanel(QTextEdit):
    """Read-only text panel."""

    STYLE = (
        "QTextEdit { color: #b0b0b0; font-size: 11px; font-family: Menlo, monospace;"
        "background: rgba(20,20,30,200); border: none; border-radius: 8px; padding: 8px; }"
        "QScrollBar:vertical { width: 6px; background: transparent; }"
        "QScrollBar::handle:vertical { background: rgba(255,255,255,0.2); border-radius: 3px; }"
        "QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical { height: 0; }"
    )

    def __init__(self, selectable=True, parent=None):
        super().__init__(parent)
        self.setReadOnly(True)
        self.paragraphs = None  # Set externally for paragraph-aware context menu
        if not selectable:
            self.setTextInteractionFlags(Qt.TextInteractionFlag.NoTextInteraction)
        self.setStyleSheet(self.STYLE)

    def keyPressEvent(self, e):
        # Pass shortcut keys to parent window
        if e.key() in (Qt.Key.Key_Space, Qt.Key.Key_Escape, Qt.Key.Key_X, Qt.Key.Key_C, Qt.Key.Key_L, Qt.Key.Key_F,
                       Qt.Key.Key_S, Qt.Key.Key_V, Qt.Key.Key_O, Qt.Key.Key_T, Qt.Key.Key_M, Qt.Key.Key_Question):
            self.window().keyPressEvent(e)
        else:
            super().keyPressEvent(e)

    def contextMenuEvent(self, e):
        if self.paragraphs is None:
            super().contextMenuEvent(e)
            return
        # Auto-select paragraph under cursor if nothing selected
        if not self.textCursor().hasSelection():
            self.setFocus()  # Ensure proper selection highlighting
            cursor = self.cursorForPosition(e.pos())
            block_num = cursor.blockNumber()
            # Each transcription is a <p> tag, map block to paragraph index
            # Blocks: p0, hr, p1, hr, p2... so paragraph i is at block 2*i
            para_idx = block_num // 2
            if self.paragraphs and 0 <= para_idx < len(self.paragraphs):
                # Select the entire block (paragraph)
                cursor.movePosition(cursor.MoveOperation.StartOfBlock)
                cursor.movePosition(cursor.MoveOperation.EndOfBlock, cursor.MoveMode.KeepAnchor)
                self.setTextCursor(cursor)

        menu = QMenu(self)
        menu.setStyleSheet(
            "QMenu { background: rgb(40,40,50); color: white; border: 1px solid rgb(80,80,80); }"
            "QMenu::item:selected { background: rgb(60,60,70); }"
        )
        if self.textCursor().hasSelection():
            copy_action = menu.addAction("Copy")
            copy_action.triggered.connect(self.copy)
        select_all = menu.addAction("Select All")
        select_all.triggered.connect(self.selectAll)
        menu.exec(e.globalPos())


class WaveformWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.peaks = np.array([])
        self.display_max = 0.01
        self.setMinimumHeight(100)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

    def set_samples(self, samples):
        max_samples = 10 * SAMPLE_RATE
        samples = samples[-max_samples:] if len(samples) > max_samples else samples
        if len(samples) > 0:
            chunk = max(1, len(samples) // 400)
            n = len(samples) // chunk
            self.peaks = np.max(np.abs(samples[:n * chunk].reshape(n, chunk)), axis=1)
            self.display_max += (max(np.max(self.peaks), 0.01) - self.display_max) * 0.04
        self.update()

    def paintEvent(self, event):
        if len(self.peaks) == 0:
            return
        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)
        w, h = self.width(), self.height()
        cy = h // 2
        p.setPen(QPen(ACCENT, 2))
        scale = w / len(self.peaks)
        for i, peak in enumerate(self.peaks):
            x = int(i * scale)
            bar = int((peak / self.display_max) * h // 2 * 0.9)
            p.drawLine(x, cy - bar, x, cy + bar)


class VoiceThingWindow(QWidget):
    hide_signal = pyqtSignal()
    toggle_signal = pyqtSignal()
    focus_signal = pyqtSignal()
    paste_signal = pyqtSignal(str)
    add_transcription_signal = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.state = "idle"
        self.audio_chunks = []
        self.stream = None
        self.tee = TeeOutput()
        self.tee.__enter__()
        self.drag_pos = None
        self.resize_edge = None
        self.is_focused = False
        self.first_show = True
        self.last_audio_path = None
        self.last_transcription = None
        self.transcriptions = []  # List of transcription strings
        self.auto_hide = True  # Whether to auto-hide after transcription
        self._prev_app = None  # For restoring focus when toggling window
        self.sound_enabled = True  # Whether to play chimes
        self.current_model = WHISPER_MODEL  # Current Whisper model

        self.setWindowTitle(APP_NAME)
        self.setWindowFlags(
            Qt.WindowType.WindowStaysOnTopHint | Qt.WindowType.FramelessWindowHint
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setAcceptDrops(True)

        font_id = QFontDatabase.addApplicationFont(rp.download_font("R:DSEG7"))
        if font_id < 0:
            raise RuntimeError("Failed to load 7-segment font")
        seg_font = QFontDatabase.applicationFontFamilies(font_id)[0]

        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(4)

        # Status row with minimize button on left
        status_row = QHBoxLayout()
        status_row.setContentsMargins(0, 0, 0, 0)
        self.minimize_btn = QPushButton()
        self.minimize_btn.setFixedSize(12, 12)
        self.minimize_btn.setStyleSheet(
            "QPushButton { background: rgb(255, 189, 68); border: none; border-radius: 6px; }"
            "QPushButton:hover { background: rgb(255, 210, 100); }"
        )
        self.minimize_btn.setToolTip("Minimize window")
        self.minimize_btn.clicked.connect(self.hide)
        status_row.addWidget(self.minimize_btn)
        self.status_label = QLabel("Double-tap Option to record")
        self.status_label.setStyleSheet(
            "color: rgba(255,255,255,0.7); font-size: 14px;"
        )
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        status_row.addWidget(self.status_label, 1)
        # Spacer to balance the minimize button
        status_row.addSpacing(12)
        layout.addLayout(status_row)

        self.timer_label = QLabel("0:00.0")
        self.seg_font = seg_font
        self.timer_label.setStyleSheet(
            f"color: rgba(100,200,255,0.3); font-size: 28px; font-family: '{seg_font}';"
        )
        self.timer_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.timer_label)

        btn_row = QHBoxLayout()
        btn_row.setSpacing(8)

        def make_btn(text, icon_fn, handler):
            btn = QPushButton(text)
            btn.setIcon(make_icon(icon_fn))
            btn.setIconSize(QSize(16, 16))
            btn.setStyleSheet(BTN_CSS)
            btn.clicked.connect(handler)
            btn.setEnabled(False)
            btn_row.addWidget(btn)
            return btn

        self.record_btn = make_btn("Space", draw_mic, self.toggle_recording)
        self.record_btn.setToolTip("Start/stop recording")
        self.record_btn.setEnabled(True)
        self.cancel_btn = make_btn("X", draw_x, self.cancel_recording)
        self.cancel_btn.setToolTip("Cancel recording")
        self.copy_btn = make_btn("C", draw_copy, self.copy_transcription)
        self.copy_btn.setToolTip("Copy last transcription to clipboard")
        self.load_btn = make_btn("L", draw_load, self.load_audio_file)
        self.load_btn.setToolTip("Load audio file to transcribe")
        self.load_btn.setEnabled(True)
        self.folder_btn = make_btn("F", draw_folder, self.open_folder)
        self.folder_btn.setToolTip("Open recordings folder")
        self.sound_btn = make_btn("S", draw_sound, self.toggle_sound)
        self.sound_btn.setToolTip("Toggle sound effects")
        self.sound_btn.setEnabled(True)
        self.eye_btn = make_btn("V", lambda p, s: draw_eye(p, s, open=False), self.toggle_auto_hide)
        self.eye_btn.setToolTip("Toggle auto-minimize after transcription")
        self.eye_btn.setEnabled(True)
        self.model_btn = make_btn("M", draw_model, self.show_model_dialog)
        self.model_btn.setToolTip("Change Whisper model")
        self.model_btn.setEnabled(True)
        self.help_btn = make_btn("?", draw_help, self.show_help)
        self.help_btn.setToolTip("Show help")
        self.help_btn.setEnabled(True)
        layout.addLayout(btn_row)

        self.waveform = WaveformWidget()
        layout.addWidget(self.waveform)

        # Tab bar for Output/Transcriptions
        tab_row = QHBoxLayout()
        tab_row.setSpacing(4)
        tab_row.setContentsMargins(0, 4, 0, 0)
        self.output_tab = QPushButton("O  Output")
        self.output_tab.setCheckable(True)
        self.output_tab.setChecked(True)
        self.output_tab.setStyleSheet(BTN_CSS)
        self.output_tab.setToolTip("Show console output")
        self.output_tab.clicked.connect(lambda: self._switch_tab(0))
        tab_row.addWidget(self.output_tab, 1)

        self.transcriptions_tab = QPushButton("T  Transcriptions")
        self.transcriptions_tab.setCheckable(True)
        self.transcriptions_tab.setStyleSheet(BTN_CSS)
        self.transcriptions_tab.setToolTip("Show transcription history")
        self.transcriptions_tab.clicked.connect(lambda: self._switch_tab(1))
        tab_row.addWidget(self.transcriptions_tab, 1)
        layout.addLayout(tab_row)

        # Stacked widget for tab content
        self.tab_stack = QStackedWidget()
        self.output_panel = TextPanel(selectable=True)
        self.transcriptions_panel = TextPanel(selectable=True)
        self.tab_stack.addWidget(self.output_panel)
        self.tab_stack.addWidget(self.transcriptions_panel)

        layout.addWidget(self.tab_stack)

        self.setMinimumSize(300, 250)
        self.resize(400, 350)
        self.hide_signal.connect(self._maybe_hide)
        self.toggle_signal.connect(self.toggle_recording)
        self.focus_signal.connect(self._focus_window)
        self.paste_signal.connect(self._do_paste)
        self.add_transcription_signal.connect(self._add_transcription)

        self.update_timer = QTimer()
        self.update_timer.timeout.connect(self._update_display)

        self.log_timer = QTimer()
        self.log_timer.timeout.connect(self._update_log)
        self.log_timer.start(100)  # Update log output 10x/sec

        self._setup_tray()

    def _setup_tray(self):
        self.tray = QSystemTrayIcon(self)
        self.tray.setIcon(make_icon(draw_mic, 22))
        menu = QMenu()
        menu.addAction("Show", self.show)
        menu.addAction("Quit", QApplication.quit)
        self.tray.setContextMenu(menu)
        self.tray.setToolTip(APP_NAME)
        self.tray.show()

    def _maybe_hide(self):
        if not self.auto_hide:
            return
        if not self.is_focused:
            self.hide()

    def _focus_window(self):
        if self.isActiveWindow():
            self.hide()
            # Restore previous app
            if self._prev_app:
                self._prev_app.activateWithOptions_(NSApplicationActivateIgnoringOtherApps)
                self._prev_app = None
            self._chime([7, 0], t=0.06)  # Descending: unfocus
        else:
            # Remember current app before stealing focus
            self._prev_app = NSWorkspace.sharedWorkspace().frontmostApplication()
            self.show()
            self.raise_()
            self.activateWindow()
            self._chime([0, 7], t=0.06)  # Ascending: focus

    def _switch_tab(self, index):
        self.tab_stack.setCurrentIndex(index)
        self.output_tab.setChecked(index == 0)
        self.transcriptions_tab.setChecked(index == 1)

    def _add_transcription(self, text):
        self.transcriptions.append(text)
        self._update_transcriptions_display()
        self._switch_tab(1)

    def _update_transcriptions_display(self):
        html = "<hr>".join(f"<p style='margin:4px 0;'>{t}</p>" for t in self.transcriptions)
        self.transcriptions_panel.setHtml(html)
        self.transcriptions_panel.paragraphs = self.transcriptions  # For right-click copy
        # Scroll to bottom for new transcription
        sb = self.transcriptions_panel.verticalScrollBar()
        sb.setValue(sb.maximum())

    def _copy_to_clipboard(self, text):
        rp.string_to_clipboard(text)
        self._chime([12, 16], t=0.05)

    def _do_paste(self, text):
        self._copy_to_clipboard(text)
        if self.is_focused:
            return
        time.sleep(0.1)
        kb = KeyboardController()
        with kb.pressed(Key.cmd):
            kb.tap("v")

    def _update_display(self):
        if self.audio_chunks:
            audio = np.concatenate(self.audio_chunks)
            self.waveform.set_samples(audio)
            secs = len(audio) / SAMPLE_RATE
            self.timer_label.setText(f"{int(secs // 60)}:{secs % 60:04.1f}")

    def _update_log(self):
        new_text = rp.strip_ansi_escapes(self.tee.text)
        if new_text != self.output_panel.toPlainText():
            self.output_panel.setPlainText(new_text)

    def _edge_at(self, pos):
        m, r = 8, self.rect()
        edge = ""
        if pos.y() >= r.height() - m:
            edge += "b"
        if pos.x() >= r.width() - m:
            edge += "r"
        return edge or None

    def mousePressEvent(self, e):
        if e.button() == Qt.MouseButton.LeftButton:
            self.resize_edge = self._edge_at(e.position().toPoint())
            if not self.resize_edge:
                self.drag_pos = (
                    e.globalPosition().toPoint() - self.frameGeometry().topLeft()
                )

    def mouseMoveEvent(self, e):
        if e.buttons() & Qt.MouseButton.LeftButton:
            if self.resize_edge:
                gpos, geo = e.globalPosition().toPoint(), self.geometry()
                if "r" in self.resize_edge:
                    geo.setRight(gpos.x())
                if "b" in self.resize_edge:
                    geo.setBottom(gpos.y())
                self.setGeometry(geo)
            elif self.drag_pos:
                self.move(e.globalPosition().toPoint() - self.drag_pos)
        else:
            cursors = {
                "br": Qt.CursorShape.SizeFDiagCursor,
                "r": Qt.CursorShape.SizeHorCursor,
                "b": Qt.CursorShape.SizeVerCursor,
            }
            self.setCursor(
                cursors.get(
                    self._edge_at(e.position().toPoint()), Qt.CursorShape.ArrowCursor
                )
            )

    def mouseReleaseEvent(self, e):
        self.drag_pos = self.resize_edge = None

    def changeEvent(self, e):
        if e.type() == e.Type.ActivationChange:
            self.is_focused = self.isActiveWindow()
            self.update()  # Repaint for opacity change
        super().changeEvent(e)

    def dragEnterEvent(self, e):
        if e.mimeData().hasUrls() and self.state == "idle":
            e.acceptProposedAction()

    def dropEvent(self, e):
        if self.state != "idle":
            return
        for url in e.mimeData().urls():
            path = url.toLocalFile()
            if path.lower().endswith(('.wav', '.mp3', '.m4a', '.flac', '.ogg', '.aac')):
                self._transcribe_file(path)
                break

    def keyPressEvent(self, e):
        key = e.key()
        if key == Qt.Key.Key_Escape:
            self.hide()
        elif key == Qt.Key.Key_X and self.state == "recording":
            self.cancel_recording()
        elif key == Qt.Key.Key_Space:
            self.toggle_recording()
        elif key == Qt.Key.Key_C:
            self.copy_transcription()
        elif key == Qt.Key.Key_F:
            self.open_folder()
        elif key == Qt.Key.Key_L:
            self.load_audio_file()
        elif key == Qt.Key.Key_S:
            self.toggle_sound()
        elif key == Qt.Key.Key_V:
            self.toggle_auto_hide()
        elif key == Qt.Key.Key_O:
            self._switch_tab(0)
        elif key == Qt.Key.Key_T:
            self._switch_tab(1)
        elif key == Qt.Key.Key_M:
            self.show_model_dialog()
        elif key == Qt.Key.Key_Question:
            self.show_help()
        else:
            super().keyPressEvent(e)

    def paintEvent(self, e):
        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)
        alpha = 255 if self.is_focused else 220
        p.setBrush(QColor(30, 30, 40, alpha))
        p.setPen(Qt.PenStyle.NoPen)
        p.drawRoundedRect(self.rect().adjusted(2, 2, -2, -2), 12, 12)
        if self.is_focused:
            p.setBrush(Qt.BrushStyle.NoBrush)
            p.setPen(QPen(ACCENT, 3))
            p.drawRoundedRect(self.rect().adjusted(2, 2, -2, -2), 12, 12)

    def _cleanup(self):
        if self.stream:
            self.stream.stop()
            self.stream.close()
            self.stream = None
        self.update_timer.stop()

    def _update_buttons(self):
        recording = self.state == "recording"
        idle = self.state == "idle"
        self.record_btn.setIcon(make_icon(draw_stop if recording else draw_mic))
        self.record_btn.setEnabled(self.state != "transcribing")
        self.cancel_btn.setEnabled(recording)
        self.copy_btn.setEnabled(self.last_transcription is not None)
        self.folder_btn.setEnabled(True)
        self.load_btn.setEnabled(idle)
        self.model_btn.setEnabled(idle)

    def toggle_recording(self):
        if self.state == "idle":
            self.start_recording()
        elif self.state == "recording":
            self.stop_recording()
        else:
            self._chime([3, 0], t=0.08)

    def cancel_recording(self):
        if self.state != "recording":
            return
        self._cleanup()
        self._set_state("idle", "Cancelled")
        self.audio_chunks = []
        self.waveform.set_samples(np.array([]))
        self._chime([7, 3], t=0.06)
        self.hide_signal.emit()

    def _set_state(self, state, status):
        self.state = state
        self.status_label.setText(status)
        opacity = 0.9 if state == "recording" else 0.3
        self.timer_label.setStyleSheet(
            f"color: rgba(100,200,255,{opacity}); font-size: 28px; font-family: '{self.seg_font}';"
        )
        self._update_buttons()

    def toggle_auto_hide(self):
        self.auto_hide = not self.auto_hide
        # Eye open = stays visible (no auto-hide), eye slashed = auto-hide enabled
        self.eye_btn.setIcon(make_icon(lambda p, s: draw_eye(p, s, not self.auto_hide)))

    def toggle_sound(self):
        self.sound_enabled = not self.sound_enabled
        self.sound_btn.setIcon(make_icon(lambda p, s: draw_sound(p, s, self.sound_enabled)))

    def _chime(self, *args, **kwargs):
        """Play chime only if sound is enabled."""
        if self.sound_enabled:
            chime(*args, **kwargs)

    def _play_waiting_chime(self):
        """Play low bump-a-bump sound while waiting."""
        self._chime([-20], [-19], [-20], t=0.066)

    def show_help(self):
        """Show help dialog."""
        dialog = HelpDialog(self)
        dialog.adjustSize()  # Ensure size is computed
        dialog.move(self.x() + (self.width() - dialog.width()) // 2,
                    self.y() + (self.height() - dialog.height()) // 2)
        dialog.exec()

    def show_model_dialog(self):
        """Show dialog to select Whisper model."""
        if self.state != "idle":
            return
        dialog = ModelDialog(self.current_model, self)
        dialog.move(self.x() + (self.width() - dialog.width()) // 2,
                    self.y() + (self.height() - dialog.height()) // 2)
        if dialog.exec() and dialog.selected_model and dialog.selected_model != self.current_model:
            self._change_model(dialog.selected_model)

    def _change_model(self, new_model):
        """Load a new Whisper model in background thread."""
        self._set_state("transcribing", f"Loading {new_model}...")
        self._switch_tab(0)

        def load():
            self._chime([0], [7], t=0.1)  # Rising "marco"
            # Start waiting chime timer
            waiting_timer = [True]
            def chime_loop():
                while waiting_timer[0]:
                    time.sleep(3)
                    if waiting_timer[0]:
                        self._play_waiting_chime()
            chime_thread = threading.Thread(target=chime_loop, daemon=True)
            chime_thread.start()

            print(f"Loading model: {new_model}")
            rp.r._get_pywhispercpp_model(new_model)
            self.current_model = new_model
            print(f"Model {new_model} loaded")

            waiting_timer[0] = False
            self._chime([0, 4, 7], [12], t=0.15)
            self._set_state("idle", "Double-tap Option to record")

        threading.Thread(target=load, daemon=True).start()

    def copy_transcription(self):
        if self.last_transcription:
            self._copy_to_clipboard(self.last_transcription)

    def open_folder(self):
        os.makedirs(RECORDINGS_DIR, exist_ok=True)
        if self.last_audio_path and os.path.exists(self.last_audio_path):
            subprocess.run(["open", "-R", self.last_audio_path])
        else:
            subprocess.run(["open", RECORDINGS_DIR])

    def load_audio_file(self):
        """Open file dialog to load an audio file for transcription."""
        if self.state != "idle":
            return
        path, _ = QFileDialog.getOpenFileName(
            self, "Load Audio File", "",
            "Audio Files (*.wav *.mp3 *.m4a *.flac *.ogg *.aac);;All Files (*)"
        )
        if path:
            self._transcribe_file(path)

    def _transcribe_file(self, path):
        """Transcribe an audio file."""
        self.show()
        self._set_state("transcribing", "Transcribing...")
        self._switch_tab(0)
        self._chime([0, 4], [7, 12], t=0.08)
        self.last_audio_path = path
        threading.Thread(target=self._transcribe_file_thread, args=(path,), daemon=True).start()

    def _transcribe_file_thread(self, path):
        print(f"Transcribing file: {path}")
        result = rp.transcribe_audio_file_via_whisper(
            path, model=self.current_model, show_progress=True
        )
        print(f"Result: {result.text!r}")
        if result.text:
            self.last_transcription = result.text
            self.paste_signal.emit(result.text)
            self.add_transcription_signal.emit(result.text)
        self._chime([0], [4], [7], [12], t=0.08)
        self._finish()

    def start_recording(self):
        self.audio_chunks = []
        self.show()
        if self.first_show:
            screen = QApplication.primaryScreen().geometry()
            self.move((screen.width() - self.width()) // 2, screen.height() // 4)
            self.first_show = False
        self.timer_label.setText("0:00.0")
        self._set_state("recording", "Recording")
        self._chime([0, 4], [7, 12], t=0.08)

        def callback(indata, frames, time_info, status):
            self.audio_chunks.append(indata[:, 0].copy())

        self.stream = sd.InputStream(
            samplerate=SAMPLE_RATE,
            channels=1,
            dtype=np.float32,
            callback=callback,
            blocksize=BLOCKSIZE,
        )
        self.stream.start()
        self.update_timer.start(8)

    def stop_recording(self):
        if self.stream:
            self.stream.stop()
            self.stream.close()
            self.stream = None
        self._set_state("transcribing", "Transcribing...")
        self._switch_tab(0)  # Switch to Output tab during transcription
        self._chime([12, 7], [4, 0], t=0.08)
        audio = np.concatenate(self.audio_chunks) if self.audio_chunks else np.array([])
        self.waveform.set_samples(audio)
        threading.Thread(target=self._transcribe, args=(audio,), daemon=True).start()

    def _transcribe(self, audio):
        if len(audio) == 0:
            print("No audio.")
            self._finish()
            return
        print(f"Recorded {len(audio) / SAMPLE_RATE:.2f}s")

        os.makedirs(RECORDINGS_DIR, exist_ok=True)
        ts = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        wav_path = os.path.join(RECORDINGS_DIR, f"{ts}.wav")
        txt_path = os.path.join(RECORDINGS_DIR, f"{ts}.txt")

        scipy.io.wavfile.write(wav_path, SAMPLE_RATE, (audio * 32767).astype(np.int16))
        self.last_audio_path = wav_path
        result = rp.transcribe_audio_file_via_whisper(
            wav_path, model=self.current_model, show_progress=True
        )

        print(f"Result: {result.text!r}")
        if result.text:
            with open(txt_path, "w") as f:
                f.write(result.text)
            self.last_transcription = result.text
            self.paste_signal.emit(result.text)
            self.add_transcription_signal.emit(result.text)

        self._chime([0], [4], [7], [12], t=0.08)
        self._finish()

    def _finish(self):
        self._cleanup()
        self._set_state("idle", "Double-tap Option to record")
        self.hide_signal.emit()


def main():
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    app = QApplication([])
    app.setStyleSheet("QToolTip { background: #333; color: white; border: 1px solid #555; }")
    window = VoiceThingWindow()

    tap_state = [0.0, 0]  # [last_tap_time, tap_count]
    pressed = set()
    CMD_KEYS = (keyboard.Key.cmd, keyboard.Key.cmd_l, keyboard.Key.cmd_r)
    ALT_KEYS = (keyboard.Key.alt, keyboard.Key.alt_l, keyboard.Key.alt_r)

    def on_press(key):
        pressed.add(key)
        # Reset tap count if non-modifier key pressed
        if key not in ALT_KEYS and key not in CMD_KEYS:
            tap_state[1] = 0

    def on_release(key):
        pressed.discard(key)
        if key in ALT_KEYS:
            now = time.time()
            cmd_held = any(k in pressed for k in CMD_KEYS)
            if now - tap_state[0] < 0.3:
                tap_state[1] += 1
                if tap_state[1] == 2:
                    if cmd_held:
                        window.focus_signal.emit()
                    else:
                        window.toggle_signal.emit()
                    tap_state[1] = 0
            else:
                tap_state[1] = 1
            tap_state[0] = now

    keyboard.Listener(on_press=on_press, on_release=on_release).start()

    # Show window on boot
    screen = QApplication.primaryScreen().geometry()
    window.move((screen.width() - window.width()) // 2, screen.height() // 4)
    window.show()
    window.first_show = False

    print(f"Loading Whisper ({WHISPER_MODEL})...")
    rp.r._get_pywhispercpp_model(WHISPER_MODEL)
    chime([0, 4, 7], [12], t=0.15)
    print(f"{APP_NAME} ready. Double-tap Option to record.")
    app.exec()


if __name__ == "__main__":
    main()
