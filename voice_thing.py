#!/usr/bin/env /opt/homebrew/opt/python@3.10/bin/python3.10
"""Voice transcription: double-tap Option to record, transcribe, and type."""

import difflib
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
from PyQt6.QtCore import Qt, QTimer, pyqtSignal, QSize, QPoint, QPointF
from PyQt6.QtGui import QPainter, QColor, QPen, QIcon, QPixmap, QFontDatabase, QPolygonF
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
    QScrollArea,
    QFrame,
)

APP_NAME = "VoiceThing"
SAMPLE_RATE = 16000
BLOCKSIZE = 256
WHISPER_MODEL = "large-v3"
TRAY_ICON_SIZE = 44  # Menu bar icon size (2x for retina)

# UI Colors
ICON_COLOR = QColor(255, 255, 255, 255)
ACCENT = QColor(100, 200, 255)
ACCENT_BG = "rgba(100,200,255,0.3)"  # For selected/checked states

# LLM post-processing settings
LLM_MODEL = "OLLAMA:qwen2.5:7b"

# # Original prompt (commented out):
# LLM_PREFIX = (
#     "The following text is a voice transcription, starting on the next line onward. "
#     "Your job is to take that voice transcription and make it coherent - or potentially "
#     "don't touch it. We touch it if there is rambling involved - if the user backtracks "
#     "and says \"no wait actually\" etc - but leave it alone if it's coherent as is. "
#     "Use bullet points only when the user is clearly dictating a list of distinct items, steps, or tasks. "
#     "Regular sentences and prose should never be bullet points. "
#     "Your output should STRICTLY be the formatted text, with no chitchat or conversation "
#     "from your side. No escaping the output - you return it raw. If the user has any "
#     "instructions for how to format his text, follow them - but make sure he's talking to "
#     f"YOU - this will be done exclusively by referring to you by your name \"{APP_NAME}\" - "
#     "so saying \"make this into a bullet point list\" for example does NOT mean they are "
#     f"talking to you, but \"{APP_NAME}, format this into a bullet point list\" does. "
#     "Ok here is the voice transcription:\n"
# )

LLM_PREFIX = (
    "Task: Clean up voice transcript.\n\n"
    "Rules:\n"
    "1. Remove filler words (um, uh, \"you know\", filler \"like\")\n"
    "2. Collapse stutters: \"set the- set the-\" → \"set the\"\n"
    "3. Apply retrospective edits when speaker self-corrects:\n"
    "   - \"actually change X to Y\" / \"make X into Y\" → apply change\n"
    "   - \"add X to the list\" / \"also include X\" → add X seamlessly (remove \"add\")\n"
    "   - \"remove X\" / \"scratch X\" / \"delete X\" → remove X\n"
    "   - \"no wait\" / \"I meant\" / \"sorry,\" → use the correction\n"
    "   - \"change the [ordinal] item to X\" → modify that item\n"
    "4. NEVER alter grammar, tense, or word forms. Preserve exact words.\n"
    "5. Filler removal is SURGICAL: remove ONLY the filler, keep surrounding content.\n"
    f"6. EXCEPTION: \"{APP_NAME},\" prefix → ignore rules 1-5, follow that instruction\n\n"
    "Examples:\n"
    "INPUT: \"You know, stop worrying. Get to commit things.\"\n"
    "OUTPUT: \"Stop worrying. Get to commit things.\"\n\n"
    "INPUT: \"Apples, oranges... oh and also add grapes.\"\n"
    "OUTPUT: \"Apples, oranges, grapes.\"\n\n"
    "CRITICAL: Output ONLY cleaned text. No explanations. Input is always text to clean.\n\n"
    "Output:\n"
)

# Accessibility permission error message
PERMISSION_ERROR_TITLE = "Accessibility Permission Required"
PERMISSION_ERROR_MSG = (
    "This process is not trusted for input monitoring.\n\n"
    "Global keyboard shortcuts (double-tap ⌥) will not work until "
    "accessibility permissions are granted.\n\n"
    "To fix this:\n"
    "1. Open System Settings → Privacy & Security → Accessibility\n"
    "2. Add your terminal app (Terminal.app, iTerm, etc.)\n"
    "3. Restart this application\n\n"
    "Note: Some terminals (like Alacritty) may not work - try the default Terminal.app.\n\n"
    "Recording via the Space button and copy to clipboard (⌘V) will still work."
)

# Whisper hallucinations when given silence/noise - normalized (lowercase, no punctuation)
BLACKLISTED_TRANSCRIPTIONS = {"thank you"}

def is_blacklisted(text):
    """Check if transcription is a known Whisper hallucination."""
    if not text:
        return False
    import re
    normalized = re.sub(r'[^\w\s]', '', text.lower()).strip()
    return normalized in BLACKLISTED_TRANSCRIPTIONS

RECORDINGS_DIR = os.path.join(tempfile.gettempdir(), APP_NAME)

# Shared styling for buttons and tabs
BTN_CSS = (
    "QPushButton { color: rgba(255,255,255,0.6); background: rgba(255,255,255,0.1); "
    "border: 1px solid rgb(100,100,100); border-radius: 3px; padding: 1px 2px; font-size: 10px; }"
    "QPushButton:hover { background: rgba(255,255,255,0.2); }"
    "QPushButton:pressed { background: rgba(100,200,255,0.4); }"
    "QPushButton:disabled { color: rgba(255,255,255,0.2); background: transparent; }"
    f"QPushButton:checked {{ background: {ACCENT_BG}; }}"
)
BTN_CHECKED_CSS = BTN_CSS + f"QPushButton {{ background: {ACCENT_BG}; }}"

CHIME_SHIFT = -12  # Shift all chimes (semitones, -12 = 1 octave lower)

def quiet_sampler(f=None, T=None, samplerate=None):
    return rp.triangle_tone_sampler(f, T, samplerate) * 0.25

def chime(*chords, **kwargs):
    shifted = [[n + CHIME_SHIFT for n in chord] for chord in chords]
    rp.play_chords(*shifted, gap=0, sampler=quiet_sampler, block=True, **kwargs)


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
    """Circle with slash (cancel/prohibit icon)."""
    p.setPen(QPen(ICON_COLOR, 2))
    m = s // 5
    p.drawEllipse(m, m, s - 2 * m, s - 2 * m)
    p.drawLine(m + 2, s - m - 2, s - m - 2, m + 2)


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
    pts = QPolygonF([
        QPointF(m + s / 6, s * 3 / 8),
        QPointF(m + s / 3, s / 4),
        QPointF(m + s / 3, s * 3 / 4),
        QPointF(m + s / 6, s * 5 / 8),
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


def draw_pen(p, s):
    """Draw a fountain pen nib icon for LLM editing."""
    p.setBrush(ICON_COLOR)
    p.setPen(Qt.PenStyle.NoPen)
    # Nib shape - pointed at top (writing position), wider at bottom
    pts = QPolygonF([
        QPointF(s / 2, s / 6),           # Top point (tip)
        QPointF(s / 4, s * 3 / 4),       # Bottom left
        QPointF(s / 2, s * 5 / 6),       # Bottom center notch
        QPointF(s * 3 / 4, s * 3 / 4),   # Bottom right
    ])
    p.drawPolygon(pts)
    # Center slit
    p.setPen(QPen(QColor(30, 30, 40), 2))
    p.drawLine(s // 2, s // 3, s // 2, s * 2 // 3)


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


def draw_warning(p, s):
    """Draw a filled warning triangle with exclamation mark."""
    bg = QColor(255, 80, 80)  # Red background
    fg = QColor(30, 30, 40)  # Dark foreground for contrast
    # Filled triangle
    p.setBrush(bg)
    p.setPen(Qt.PenStyle.NoPen)
    pts = QPolygonF([QPointF(s / 2, s / 8), QPointF(s / 8, s * 7 / 8), QPointF(s * 7 / 8, s * 7 / 8)])
    p.drawPolygon(pts)
    # Exclamation mark (dark on red)
    p.setPen(QPen(fg, max(2, s // 8)))
    p.drawLine(s // 2, s * 3 // 10, s // 2, s * 11 // 20)
    p.setBrush(fg)
    p.setPen(Qt.PenStyle.NoPen)
    dot_r = max(2, s // 10)
    p.drawEllipse(s // 2 - dot_r // 2, s * 13 // 20, dot_r, dot_r)


def make_icon(draw_fn):
    px = QPixmap(64, 64)
    px.fill(Qt.GlobalColor.transparent)
    p = QPainter(px)
    p.setRenderHint(QPainter.RenderHint.Antialiasing)
    draw_fn(p, 64)
    p.end()
    return QIcon(px)


def make_icon_sized(draw_fn, size):
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

# Action definitions: (id, key, icon_fn, description, menu_text or None)
# Single source of truth for buttons, keyboard shortcuts, help dialog, and menu items
ACTIONS = [
    ("record", "Space", draw_mic, "Start/finish recording", "Start/Stop Recording"),
    ("cancel", "X", draw_x, "Cancel recording", None),
    ("minimize", "Esc", None, "Minimize window", None),
    ("small_mode", "E", None, "Toggle small mode", None),
    ("copy", "C", draw_copy, "Copy last transcription", "Copy Last Transcription"),
    ("load", "L", draw_load, "Load audio file", "Load Audio File..."),
    ("folder", "F", draw_folder, "Open recordings folder", "Open Recordings Folder"),
    ("sound", "S", draw_sound, "Toggle sound effects", None),
    ("auto_hide", "V", draw_eye, "Toggle auto-minimize", None),
    ("llm", "R", draw_pen, "Toggle LLM post-processing", None),
    ("model", "M", draw_model, "Change Whisper model", None),
    ("help", "?", draw_help, "Show help", "Help"),
]

# Tab definitions
TABS = [
    ("O", "Output", "Show console output"),
    ("T", "Transcriptions", "Show transcription history"),
]

# Build lookup dict for actions
ACTIONS_BY_ID = {a[0]: a for a in ACTIONS}


GITHUB_URL = "https://github.com/RyannDaGreat/VoiceThing"


class DraggableDialog(QDialog):
    """Base class for frameless, draggable dialogs."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.drag_pos = None
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.Dialog)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

    def center_on_parent(self):
        self.adjustSize()
        if self.parent():
            p = self.parent()
            self.move(p.x() + (p.width() - self.width()) // 2,
                      p.y() + (p.height() - self.height()) // 2)

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


class HelpDialog(DraggableDialog):
    """Help dialog with about info and keymap."""

    def __init__(self, parent=None):
        super().__init__(parent)
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
            "• Double-tap ⌥ to record from anywhere (works in fullscreen apps and terminals!)\n"
            "• Double-tap ⌥ again to stop and auto-paste the transcription via ⌘V\n"
            "• ⌘ + double-tap ⌥ to toggle focus\n"
            "• Access from menu bar (top right of Mac)\n"
            "• Drag & drop audio files to transcribe\n"
            "• ⌘Q to quit\n\n"
            "100% keyboard-driven - no mouse needed! (hover buttons to see shortcuts)\n\n"
            "Small mode (E or green button): Compact view with just status and timer - "
            "great for keeping visible while using keyboard shortcuts.\n\n"
            "Anti-Ramble mode (R): Post-process transcriptions with an LLM to clean up rambling."
            f"Say \"{APP_NAME}, ...\" in your recording to give formatting instructions.\n\n"
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

        for action_id, key, icon_fn, desc, menu_text in ACTIONS:
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
            lbl = QLabel(desc)
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
        if e.key() in (Qt.Key.Key_Escape, Qt.Key.Key_Question, Qt.Key.Key_Return, Qt.Key.Key_Enter):
            self.accept()
        else:
            super().keyPressEvent(e)


class ModelDialog(DraggableDialog):
    """Dialog to select Whisper model with keyboard shortcuts."""

    def __init__(self, current_model, parent=None):
        super().__init__(parent)
        self.selected_model = None

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


class PermissionDialog(DraggableDialog):
    """Dialog explaining accessibility permission requirements."""

    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(12)

        title = QLabel(PERMISSION_ERROR_TITLE)
        title.setStyleSheet("color: rgb(255,80,80); font-size: 16px; font-weight: bold;")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)

        msg = QLabel(PERMISSION_ERROR_MSG)
        msg.setStyleSheet("color: rgba(255,255,255,0.9); font-size: 13px;")
        msg.setWordWrap(True)
        layout.addWidget(msg)

        close_btn = QPushButton("Esc  Close")
        close_btn.setStyleSheet(BTN_CSS)
        close_btn.clicked.connect(self.accept)
        layout.addWidget(close_btn)

        # Auto-size to fit content
        self.adjustSize()

    def keyPressEvent(self, e):
        if e.key() == Qt.Key.Key_Escape:
            self.accept()
        else:
            super().keyPressEvent(e)


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
                       Qt.Key.Key_S, Qt.Key.Key_V, Qt.Key.Key_R, Qt.Key.Key_E, Qt.Key.Key_O, Qt.Key.Key_T, Qt.Key.Key_M, Qt.Key.Key_Question):
            self.window().keyPressEvent(e)
        else:
            super().keyPressEvent(e)

    def contextMenuEvent(self, e):
        if self.paragraphs is None:
            super().contextMenuEvent(e)
            return
        # Auto-select paragraph under cursor if nothing selected
        if not self.textCursor().hasSelection():
            self.setFocus()
            cursor = self.cursorForPosition(e.pos())
            block_num = cursor.blockNumber()
            # Each transcription is a <p> tag, map block to paragraph index
            # Blocks: p0, hr, p1, hr, p2... so paragraph i is at block 2*i
            para_idx = block_num // 2
            if self.paragraphs and 0 <= para_idx < len(self.paragraphs):
                cursor.movePosition(cursor.MoveOperation.StartOfBlock)
                cursor.movePosition(cursor.MoveOperation.EndOfBlock, cursor.MoveMode.KeepAnchor)
                self.setTextCursor(cursor)

        menu = QMenu(self)
        menu.setStyleSheet(
            "QMenu { background: rgb(40,40,50); color: white; border: 1px solid rgb(80,80,80); border-radius: 6px; padding: 4px; }"
            "QMenu::item { padding: 4px 12px; border-radius: 4px; }"
            "QMenu::item:selected { background: rgb(60,60,70); }"
        )
        if self.textCursor().hasSelection():
            copy_action = menu.addAction("Copy")
            copy_action.triggered.connect(self.copy)
        select_all = menu.addAction("Select All")
        select_all.triggered.connect(self.selectAll)
        menu.exec(e.globalPos())


def word_diff_html(old_text, new_text, is_old, highlight=False):
    """Generate HTML with word-level diff highlighting.

    is_old=True: show deletions (red) for words removed from old_text
    is_old=False: show additions (green) for words added in new_text
    highlight=False: return plain text wrapped in spans (no color)
    highlight=True: return text with diff colors
    """
    old_words = old_text.split()
    new_words = new_text.split()

    matcher = difflib.SequenceMatcher(None, old_words, new_words)
    result = []

    # Use invisible highlight when not hovering to maintain consistent sizing
    red_bg = "background:rgba(180,60,60,0.4);" if highlight else ""
    green_bg = "background:rgba(60,140,60,0.4);" if highlight else ""

    for op, i1, i2, j1, j2 in matcher.get_opcodes():
        if op == 'equal':
            words = old_words[i1:i2] if is_old else new_words[j1:j2]
            result.extend(words)
        elif op == 'replace':
            if is_old:
                for w in old_words[i1:i2]:
                    result.append(f'<span style="{red_bg}">{w}</span>')
            else:
                for w in new_words[j1:j2]:
                    result.append(f'<span style="{green_bg}">{w}</span>')
        elif op == 'delete' and is_old:
            for w in old_words[i1:i2]:
                result.append(f'<span style="{red_bg}">{w}</span>')
        elif op == 'insert' and not is_old:
            for w in new_words[j1:j2]:
                result.append(f'<span style="{green_bg}">{w}</span>')

    return ' '.join(result)


class TranscriptionRow(QFrame):
    """Clickable row for a single transcription text."""
    clicked = pyqtSignal(str)
    deramble_clicked = pyqtSignal(str)
    hover_changed = pyqtSignal(bool)  # Emitted when hover state changes

    BTN_STYLE = (
        "QPushButton { background: transparent; border: none; border-radius: 4px; }"
        "QPushButton:hover { background: rgba(255,255,255,0.15); }"
        "QPushButton:pressed { background: rgba(100,200,255,0.4); }"
    )

    def __init__(self, text, dimmed=False, show_deramble=False, other_text=None, is_raw=False, parent=None):
        super().__init__(parent)
        self.text = text
        self.other_text = other_text  # The other version for diff comparison
        self.is_raw = is_raw  # True if this is the raw (pre-LLM) text
        self.dimmed = dimmed
        self.setCursor(Qt.CursorShape.PointingHandCursor)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(8, 4, 8, 4)
        layout.setSpacing(4)

        self.label = QLabel()
        if dimmed:
            self.base_style = "font-size: 11px; color: rgba(130,150,170,0.7);"
        else:
            self.base_style = "font-size: 11px; color: #b0b0b0;"
        self.label.setStyleSheet(self.base_style)
        self.label.setWordWrap(True)
        self.label.setTextFormat(Qt.TextFormat.RichText)
        layout.addWidget(self.label, 1)

        # Set initial HTML (unhighlighted)
        self._set_diff_highlight(False)

        if show_deramble:
            deramble_btn = QPushButton()
            deramble_btn.setFixedSize(24, 24)
            deramble_btn.setIcon(make_icon(draw_pen))
            deramble_btn.setIconSize(QSize(16, 16))
            deramble_btn.setStyleSheet(self.BTN_STYLE)
            deramble_btn.setToolTip("De-ramble with LLM")
            deramble_btn.clicked.connect(lambda: self.deramble_clicked.emit(self.text))
            layout.addWidget(deramble_btn, 0, Qt.AlignmentFlag.AlignTop)

        copy_btn = QPushButton()
        copy_btn.setFixedSize(24, 24)
        copy_btn.setIcon(make_icon(draw_copy))
        copy_btn.setIconSize(QSize(16, 16))
        copy_btn.setStyleSheet(self.BTN_STYLE)
        copy_btn.setToolTip("Copy to clipboard")
        copy_btn.clicked.connect(lambda: self.clicked.emit(self.text))
        layout.addWidget(copy_btn, 0, Qt.AlignmentFlag.AlignTop)

        self._update_bg(False)

    def _set_diff_highlight(self, highlight):
        """Update the label with diff HTML, optionally highlighted."""
        if self.other_text:
            # For raw: old=self.text, new=other_text, show deletions
            # For processed: old=other_text, new=self.text, show additions
            if self.is_raw:
                html = word_diff_html(self.text, self.other_text, is_old=True, highlight=highlight)
            else:
                html = word_diff_html(self.other_text, self.text, is_old=False, highlight=highlight)
            self.label.setText(html)
        else:
            self.label.setText(self.text)

    def set_diff_highlight(self, highlight):
        """Called by parent to set diff highlight state (not row background)."""
        self._set_diff_highlight(highlight)

    def _update_bg(self, hovered):
        bg = "rgba(255,255,255,0.05)" if hovered else "transparent"
        self.setStyleSheet(f"TranscriptionRow {{ background: {bg}; }}")

    def enterEvent(self, event):
        self._update_bg(True)
        self.hover_changed.emit(True)
        super().enterEvent(event)

    def leaveEvent(self, event):
        self._update_bg(False)
        self.hover_changed.emit(False)
        super().leaveEvent(event)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self._press_global_pos = event.globalPosition().toPoint()
        super().mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton and hasattr(self, '_press_global_pos'):
            delta = event.globalPosition().toPoint() - self._press_global_pos
            if abs(delta.x()) + abs(delta.y()) < 5:
                self.clicked.emit(self.text)
            del self._press_global_pos
        super().mouseReleaseEvent(event)


class TranscriptionItem(QFrame):
    """Single transcription entry with one or two rows."""
    copy_clicked = pyqtSignal(str)
    deramble_clicked = pyqtSignal(int, str)  # (index, raw_text)

    def __init__(self, raw_text, processed_text, index, parent=None):
        super().__init__(parent)
        self.index = index
        self.diff_rows = []  # Rows that need coordinated highlighting

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        if processed_text:
            raw_row = TranscriptionRow(raw_text, dimmed=True, other_text=processed_text, is_raw=True)
            raw_row.clicked.connect(self.copy_clicked.emit)
            raw_row.hover_changed.connect(self._on_hover_changed)
            layout.addWidget(raw_row)

            proc_row = TranscriptionRow(processed_text, dimmed=False, other_text=raw_text, is_raw=False)
            proc_row.clicked.connect(self.copy_clicked.emit)
            proc_row.hover_changed.connect(self._on_hover_changed)
            layout.addWidget(proc_row)

            self.diff_rows = [raw_row, proc_row]
        else:
            row = TranscriptionRow(raw_text, dimmed=False, show_deramble=True)
            row.clicked.connect(self.copy_clicked.emit)
            row.deramble_clicked.connect(lambda t: self.deramble_clicked.emit(self.index, t))
            layout.addWidget(row)

        self.setStyleSheet("TranscriptionItem { border-bottom: 1px solid rgba(255,255,255,0.1); }")

    def _on_hover_changed(self, hovered):
        """When any row is hovered, highlight diff text in all rows (not row background)."""
        for row in self.diff_rows:
            row.set_diff_highlight(hovered)


class TranscriptionList(QScrollArea):
    """Scrollable list of transcription items with copy buttons."""
    copy_requested = pyqtSignal(str)
    deramble_requested = pyqtSignal(int, str)  # (index, raw_text)

    STYLE = (
        "QScrollArea { background: rgba(20,20,30,200); border: none; border-radius: 8px; }"
        "QScrollBar:vertical { width: 6px; background: transparent; }"
        "QScrollBar::handle:vertical { background: rgba(255,255,255,0.2); border-radius: 3px; }"
        "QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical { height: 0; }"
    )

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet(self.STYLE)
        self.setWidgetResizable(True)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.item_count = 0

        self.container = QWidget()
        self.container.setStyleSheet("background: transparent;")
        self.layout = QVBoxLayout(self.container)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)
        self.layout.addStretch()
        self.setWidget(self.container)

    def add_transcription(self, raw_text, processed_text):
        index = self.item_count
        self.item_count += 1
        item = TranscriptionItem(raw_text, processed_text, index)
        item.copy_clicked.connect(self.copy_requested.emit)
        item.deramble_clicked.connect(self.deramble_requested.emit)
        # Insert before the stretch
        self.layout.insertWidget(self.layout.count() - 1, item)
        # Scroll to bottom
        QTimer.singleShot(10, lambda: self.verticalScrollBar().setValue(
            self.verticalScrollBar().maximum()))

    def update_transcription(self, index, raw_text, processed_text):
        """Replace transcription at index with updated raw+processed version."""
        # Find the widget at this index (widgets are in order, stretch is last)
        if index < self.layout.count() - 1:
            old_item = self.layout.takeAt(index)
            if old_item and old_item.widget():
                old_item.widget().deleteLater()
            new_item = TranscriptionItem(raw_text, processed_text, index)
            new_item.copy_clicked.connect(self.copy_requested.emit)
            new_item.deramble_clicked.connect(self.deramble_requested.emit)
            self.layout.insertWidget(index, new_item)

    def clear(self):
        while self.layout.count() > 1:  # Keep the stretch
            item = self.layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        self.item_count = 0


class WaveformWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.samples = np.array([])
        self.display_max = 0.01
        self.setMinimumHeight(100)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

    def set_samples(self, samples):
        max_samples = 10 * SAMPLE_RATE
        self.samples = samples[-max_samples:] if len(samples) > max_samples else samples
        if len(self.samples) > 0:
            self.display_max += (max(np.max(np.abs(self.samples)), 0.01) - self.display_max) * 0.04
        self.update()

    def paintEvent(self, event):
        n = len(self.samples)
        if n < 1:
            return
        p = QPainter(self)
        w, h = self.width(), self.height()
        cy = h / 2

        # Compute peaks - fixed number of bins based on width
        abs_samples = np.abs(self.samples)
        n_bins = w
        # Use linspace indices to get exactly n_bins peaks covering all samples
        indices = np.linspace(0, n, n_bins + 1).astype(int)
        peaks = np.array([abs_samples[indices[i]:indices[i+1]].max() if indices[i] < indices[i+1] else 0
                         for i in range(n_bins)])
        y_vals = peaks

        # Scale to widget height
        y_scaled = (y_vals / self.display_max) * h / 2 * 0.9

        # Build polygon: left-to-right along top edge, right-to-left along bottom edge
        x_coords = np.arange(w)
        top_y = cy - y_scaled
        bottom_y = cy + y_scaled[::-1]
        points = [QPointF(x, y) for x, y in zip(x_coords, top_y)]
        points += [QPointF(x, y) for x, y in zip(x_coords[::-1], bottom_y)]
        polygon = QPolygonF(points)

        # Draw filled waveform
        p.setPen(Qt.PenStyle.NoPen)
        p.setBrush(ACCENT)
        p.drawPolygon(polygon)

        # Center line
        p.setPen(QPen(QColor(255, 255, 255, 40), 1))
        p.drawLine(0, int(cy), w, int(cy))


class VoiceThingWindow(QWidget):
    hide_signal = pyqtSignal()
    toggle_signal = pyqtSignal()
    focus_signal = pyqtSignal()
    paste_signal = pyqtSignal(str)
    add_transcription_signal = pyqtSignal(str, str)  # (raw_text, processed_text or "")
    update_transcription_signal = pyqtSignal(int, str, str)  # (index, raw_text, processed_text)
    permission_error_signal = pyqtSignal()

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
        self.permission_error = False  # True if accessibility permission denied
        self.auto_hide = False  # Whether to auto-hide after transcription
        self._prev_app = None  # For restoring focus when toggling window
        self.sound_enabled = True  # Whether to play chimes
        self.llm_enabled = False  # Whether to use LLM post-processing
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

        # Status row with window control buttons on left (macOS order: close, minimize, zoom)
        status_row = QHBoxLayout()
        status_row.setContentsMargins(0, 0, 0, 0)
        status_row.setSpacing(8)
        self.small_mode = False  # Track small mode state
        self.minimize_btn = QPushButton()
        self.minimize_btn.setFixedSize(12, 12)
        self.minimize_btn.setStyleSheet(
            "QPushButton { background: rgb(255, 189, 68); border: none; border-radius: 6px; }"
            "QPushButton:hover { background: rgb(255, 210, 100); }"
        )
        self.minimize_btn.setToolTip("Minimize window (Esc)")
        self.minimize_btn.clicked.connect(self.hide)
        status_row.addWidget(self.minimize_btn)
        self.small_btn = QPushButton()
        self.small_btn.setFixedSize(12, 12)
        self.small_btn.setStyleSheet(
            "QPushButton { background: rgb(52, 199, 89); border: none; border-radius: 6px; }"
            "QPushButton:hover { background: rgb(80, 220, 110); }"
        )
        self.small_btn.setToolTip("Toggle small mode (E)")
        self.small_btn.clicked.connect(self.toggle_small_mode)
        status_row.addWidget(self.small_btn)
        # Warning button for permission errors (hidden by default)
        self.warning_btn = QPushButton()
        self.warning_btn.setFixedSize(20, 20)
        self.warning_btn.setIcon(make_icon(draw_warning))
        self.warning_btn.setIconSize(QSize(18, 18))
        self.warning_btn.setStyleSheet("QPushButton { background: transparent; border: none; }")
        self.warning_btn.setToolTip(PERMISSION_ERROR_TITLE)
        self.warning_btn.clicked.connect(self.show_permission_dialog)
        self.warning_btn.hide()
        status_row.addWidget(self.warning_btn)
        self.status_label = QLabel("Double-tap ⌥")
        self.status_label.setStyleSheet(
            "color: rgba(255,255,255,0.7); font-size: 14px;"
        )
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        status_row.addWidget(self.status_label, 1)
        # Spacer to balance the window control buttons
        self.status_spacer = QWidget()
        self.status_spacer.setFixedWidth(28)
        status_row.addWidget(self.status_spacer)
        layout.addLayout(status_row)

        self.timer_label = QLabel("0:00.0")
        self.seg_font = seg_font
        self.timer_label.setStyleSheet(
            f"color: rgba(100,200,255,0.3); font-size: 28px; font-family: '{seg_font}';"
        )
        self.timer_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.timer_label)

        self.btn_row_widget = QWidget()
        btn_row = QHBoxLayout(self.btn_row_widget)
        btn_row.setContentsMargins(0, 0, 0, 0)
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
        self.eye_btn = make_btn("V", lambda p, s: draw_eye(p, s, open=True), self.toggle_auto_hide)
        self.eye_btn.setToolTip("Toggle auto-minimize after transcription")
        self.eye_btn.setEnabled(True)
        self.llm_btn = make_btn("R", draw_pen, self.toggle_llm)
        self.llm_btn.setToolTip("Toggle LLM post-processing")
        self.llm_btn.setCheckable(True)
        self.llm_btn.setEnabled(True)
        self.model_btn = make_btn("M", draw_model, self.show_model_dialog)
        self.model_btn.setToolTip("Change Whisper model")
        self.model_btn.setEnabled(True)
        self.help_btn = make_btn("?", draw_help, self.show_help)
        self.help_btn.setToolTip("Show help")
        self.help_btn.setEnabled(True)
        layout.addWidget(self.btn_row_widget)

        # Key-to-button mapping for visual feedback
        self.key_buttons = {
            Qt.Key.Key_Space: self.record_btn, Qt.Key.Key_X: self.cancel_btn,
            Qt.Key.Key_C: self.copy_btn, Qt.Key.Key_L: self.load_btn,
            Qt.Key.Key_F: self.folder_btn, Qt.Key.Key_S: self.sound_btn,
            Qt.Key.Key_V: self.eye_btn, Qt.Key.Key_R: self.llm_btn,
            Qt.Key.Key_M: self.model_btn, Qt.Key.Key_Question: self.help_btn,
        }

        self.waveform = WaveformWidget()
        layout.addWidget(self.waveform)

        # Tab bar for Output/Transcriptions
        self.tab_row_widget = QWidget()
        tab_row = QHBoxLayout(self.tab_row_widget)
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
        layout.addWidget(self.tab_row_widget)

        # Add tab buttons to key mapping
        self.key_buttons[Qt.Key.Key_O] = self.output_tab
        self.key_buttons[Qt.Key.Key_T] = self.transcriptions_tab

        # Stacked widget for tab content
        self.tab_stack = QStackedWidget()
        self.output_panel = TextPanel(selectable=True)
        self.transcriptions_panel = TranscriptionList()
        self.transcriptions_panel.copy_requested.connect(self._copy_to_clipboard)
        self.transcriptions_panel.deramble_requested.connect(self._deramble_transcription)
        self.tab_stack.addWidget(self.output_panel)
        self.tab_stack.addWidget(self.transcriptions_panel)

        layout.addWidget(self.tab_stack)

        self.setMinimumSize(360, 250)
        self.resize(460, 350)
        self.hide_signal.connect(self._maybe_hide)
        self.toggle_signal.connect(self.toggle_recording)
        self.focus_signal.connect(self._focus_window)
        self.paste_signal.connect(self._do_paste)
        self.add_transcription_signal.connect(self._add_transcription)
        self.update_transcription_signal.connect(self._update_transcription)
        self.permission_error_signal.connect(self._on_permission_error)

        self.update_timer = QTimer()
        self.update_timer.timeout.connect(self._update_display)

        self.log_timer = QTimer()
        self.log_timer.timeout.connect(self._update_log)
        self.log_timer.start(100)  # Update log output 10x/sec

        self._setup_tray()

    def _get_action_handler(self, action_id):
        """Get the handler method for an action ID."""
        handlers = {
            "record": self.toggle_recording,
            "cancel": self.cancel_recording,
            "minimize": self.hide,
            "small_mode": self.toggle_small_mode,
            "copy": self.copy_transcription,
            "load": self.load_audio_file,
            "folder": self.open_folder,
            "sound": self.toggle_sound,
            "auto_hide": self.toggle_auto_hide,
            "llm": self.toggle_llm,
            "model": self.show_model_dialog,
            "help": self.show_help,
        }
        return handlers.get(action_id)

    def _setup_tray(self):
        self.tray = QSystemTrayIcon(self)
        self.tray.setIcon(make_icon_sized(draw_mic, TRAY_ICON_SIZE))
        menu = QMenu()
        menu.addAction("Show", self.show)
        menu.addSeparator()
        # Add menu items from ACTIONS
        for action_id, key, icon_fn, desc, menu_text in ACTIONS:
            if menu_text:
                handler = self._get_action_handler(action_id)
                if handler:
                    menu.addAction(menu_text, handler)
        menu.addSeparator()
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
            self._chime([14, 7], t=0.06)  # G key: descending unfocus
        else:
            # Remember current app before stealing focus
            self._prev_app = NSWorkspace.sharedWorkspace().frontmostApplication()
            self.show()
            self.raise_()
            self.activateWindow()
            self._chime([7, 14], t=0.06)  # G key: ascending focus

    def _switch_tab(self, index):
        self.tab_stack.setCurrentIndex(index)
        self.output_tab.setChecked(index == 0)
        self.transcriptions_tab.setChecked(index == 1)

    def _flash_button(self, key):
        """Visually flash the button for a key press."""
        btn = self.key_buttons.get(key)
        if btn and btn.isEnabled():
            btn.setDown(True)
            QTimer.singleShot(100, lambda: btn.setDown(False))

    def _add_transcription(self, raw_text, processed_text):
        self.transcriptions.append((raw_text, processed_text))
        self.transcriptions_panel.add_transcription(raw_text, processed_text)
        self._switch_tab(1)

    def _update_transcription(self, index, raw_text, processed_text):
        self.transcriptions[index] = (raw_text, processed_text)
        self.transcriptions_panel.update_transcription(index, raw_text, processed_text)

    def _copy_to_clipboard(self, text):
        rp.string_to_clipboard(text)
        self._chime([16, 20], t=0.05)  # E key: copy

    def _deramble_transcription(self, index, raw_text):
        """Process a transcription with LLM and update it in place."""
        def do_deramble():
            processed = self._run_llm(raw_text)
            self.update_transcription_signal.emit(index, raw_text, processed)
        threading.Thread(target=do_deramble, daemon=True).start()

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
            sb = self.output_panel.verticalScrollBar()
            sb.setValue(sb.maximum())

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
        mods = e.modifiers()
        no_mods = mods == Qt.KeyboardModifier.NoModifier
        self._flash_button(key)
        if key == Qt.Key.Key_Escape:
            self.hide()
        elif no_mods and key == Qt.Key.Key_X and self.state == "recording":
            self.cancel_recording()
        elif no_mods and key == Qt.Key.Key_Space:
            self.toggle_recording()
        elif no_mods and key == Qt.Key.Key_C:
            self.copy_transcription()
        elif no_mods and key == Qt.Key.Key_F:
            self.open_folder()
        elif no_mods and key == Qt.Key.Key_L:
            self.load_audio_file()
        elif no_mods and key == Qt.Key.Key_S:
            self.toggle_sound()
        elif no_mods and key == Qt.Key.Key_V:
            self.toggle_auto_hide()
        elif no_mods and key == Qt.Key.Key_R:
            self.toggle_llm()
        elif no_mods and key == Qt.Key.Key_E:
            self.toggle_small_mode()
        elif no_mods and key == Qt.Key.Key_O:
            self._switch_tab(0)
        elif no_mods and key == Qt.Key.Key_T:
            self._switch_tab(1)
        elif no_mods and key == Qt.Key.Key_M:
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
            self._chime([0, -3], t=0.08)  # Minor: busy/error

    def cancel_recording(self):
        if self.state != "recording":
            return
        self._cleanup()
        self._set_state("idle", "Cancelled")
        self.audio_chunks = []
        self.waveform.set_samples(np.array([]))
        self._chime([3, -1], t=0.06)  # Minor: cancel
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

    def toggle_small_mode(self):
        self.small_mode = not self.small_mode
        self.btn_row_widget.setVisible(not self.small_mode)
        self.waveform.setVisible(not self.small_mode)
        self.tab_row_widget.setVisible(not self.small_mode)
        self.tab_stack.setVisible(not self.small_mode)
        self.status_spacer.setVisible(not self.small_mode)
        # Adjust status label font size for small mode
        font_size = 10 if self.small_mode else 14
        self.status_label.setStyleSheet(f"color: rgba(255,255,255,0.7); font-size: {font_size}px;")
        if self.small_mode:
            self._normal_size = self.size()
            self.setMinimumSize(0, 0)
            self.setMaximumSize(16777215, 16777215)
            self.adjustSize()
            # Use fixed small mode width
            small_width = 143
            small_height = self.sizeHint().height()
            self.setFixedSize(small_width, small_height)
        else:
            self.setMinimumSize(300, 250)
            self.setMaximumSize(16777215, 16777215)  # Reset to default max
            if hasattr(self, '_normal_size'):
                self.resize(self._normal_size)

    def toggle_sound(self):
        self.sound_enabled = not self.sound_enabled
        self.sound_btn.setIcon(make_icon(lambda p, s: draw_sound(p, s, self.sound_enabled)))

    def toggle_llm(self):
        self.llm_enabled = not self.llm_enabled
        self.llm_btn.setChecked(self.llm_enabled)

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
        dialog.center_on_parent()
        dialog.exec()

    def show_permission_dialog(self):
        """Show permission error dialog."""
        dialog = PermissionDialog(self)
        dialog.center_on_parent()
        dialog.exec()

    def _on_permission_error(self):
        """Handle accessibility permission error."""
        self.permission_error = True
        self.auto_hide = False  # Disable auto-hide since global shortcuts won't work
        self.eye_btn.setIcon(make_icon(lambda p, s: draw_eye(p, s, True)))
        self.warning_btn.show()

    def show_model_dialog(self):
        """Show dialog to select Whisper model."""
        if self.state != "idle":
            return
        dialog = ModelDialog(self.current_model, self)
        dialog.center_on_parent()
        if dialog.exec() and dialog.selected_model and dialog.selected_model != self.current_model:
            self._change_model(dialog.selected_model)

    def _change_model(self, new_model):
        """Load a new Whisper model in background thread."""
        self._set_state("transcribing", f"Loading {new_model}...")
        self._switch_tab(0)

        def load():
            self._chime([5], [12], t=0.1)  # F key: model loading start
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
            self._chime([5, 9, 12], [17], t=0.15)  # F key: model loaded
            self._set_state("idle", "Double-tap ⌥")

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
        self._chime([2, 6], [9, 14], t=0.08)  # D key
        self.last_audio_path = path
        threading.Thread(target=self._transcribe_file_thread, args=(path,), daemon=True).start()

    def _transcribe_file_thread(self, path):
        print(f"Transcribing file: {path}")
        result = rp.transcribe_audio_file_via_whisper(
            path, model=self.current_model, show_progress=True
        )
        self._handle_transcription_result(result.text)
        self._chime([2], [6], [9], [14], t=0.08)  # D key: transcription done
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
        self._chime([2, 6], [9, 14], t=0.08)  # D key

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
        self._chime([14, 9], [6, 2], t=0.08)  # D key: stop recording
        audio = np.concatenate(self.audio_chunks) if self.audio_chunks else np.array([])
        self.waveform.set_samples(audio)
        threading.Thread(target=self._transcribe, args=(audio,), daemon=True).start()

    def _run_llm(self, text):
        """Run LLM on text. Returns processed result."""
        self._chime([7, 11], t=0.06)  # LLM processing start
        print("Processing with LLM...")
        prompt = LLM_PREFIX + text
        result = rp.run_llm_api(prompt, model=LLM_MODEL)
        print(f"LLM result: {result!r}")
        self._chime([11, 14, 18], t=0.08)  # LLM processing done
        return result

    def _process_with_llm(self, text):
        """Post-process transcription with LLM if enabled. Returns (raw, processed) or (raw, "")."""
        if not self.llm_enabled or not text:
            return text, ""
        return text, self._run_llm(text)

    def _handle_transcription_result(self, text, txt_path=None):
        """Process transcription result: LLM, save, paste, add to list."""
        raw_text = "" if is_blacklisted(text) else text
        print(f"Result: {raw_text!r}")
        if not raw_text:
            return

        if self.llm_enabled:
            # Show raw immediately, then update when LLM finishes
            index = len(self.transcriptions)
            self.add_transcription_signal.emit(raw_text, "")
            self.last_transcription = raw_text
            self.paste_signal.emit(raw_text)

            def run_llm_and_update():
                processed = self._run_llm(raw_text)
                if txt_path:
                    with open(txt_path, "w") as f:
                        f.write(processed)
                self.last_transcription = processed
                self.update_transcription_signal.emit(index, raw_text, processed)
            threading.Thread(target=run_llm_and_update, daemon=True).start()
        else:
            if txt_path:
                with open(txt_path, "w") as f:
                    f.write(raw_text)
            self.last_transcription = raw_text
            self.paste_signal.emit(raw_text)
            self.add_transcription_signal.emit(raw_text, "")

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
        self._handle_transcription_result(result.text, txt_path)
        self._chime([2], [6], [9], [14], t=0.08)  # D key: transcription done
        self._finish()

    def _finish(self):
        self._cleanup()
        self._set_state("idle", "Double-tap ⌥")
        self.hide_signal.emit()


def main():
    signal.signal(signal.SIGINT, signal.SIG_DFL)

    # Set process name for macOS Activity Monitor and menu bar
    try:
        from Foundation import NSBundle
        bundle = NSBundle.mainBundle()
        info = bundle.localizedInfoDictionary() or bundle.infoDictionary()
        if info:
            info['CFBundleName'] = APP_NAME
    except Exception:
        pass

    app = QApplication([APP_NAME])
    app.setApplicationName(APP_NAME)
    app.setApplicationDisplayName(APP_NAME)
    app.setStyleSheet("QToolTip { background: #333; color: white; border: 1px solid #555; border-radius: 4px; }")
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

    listener = keyboard.Listener(on_press=on_press, on_release=on_release)
    listener.start()

    # Check for permission error after listener starts
    def check_permission():
        time.sleep(0.5)  # Give listener time to print error
        if "not trusted" in window.tee.text.lower():
            window.permission_error_signal.emit()

    threading.Thread(target=check_permission, daemon=True).start()

    # Show window on boot
    screen = QApplication.primaryScreen().geometry()
    window.move((screen.width() - window.width()) // 2, screen.height() // 4)
    window.show()
    window.first_show = False

    print(f"Loading Whisper ({WHISPER_MODEL})...")
    rp.r._get_pywhispercpp_model(WHISPER_MODEL)
    chime([0, 4, 7], [12], t=0.15)
    print(f"{APP_NAME} ready. Double-tap ⌥ to record.")
    app.exec()


if __name__ == "__main__":
    main()
