#!/usr/bin/env python3
"""Voice transcription: double-tap Option to record, transcribe, and type."""

import collections
import difflib
import functools
import json
import math
import os
import re
import signal
import subprocess
import sys
import tempfile
import threading
import time
import warnings
from datetime import datetime

import numpy as np
import rp

# Suppress ONNX warnings for wake word model
warnings.filterwarnings('ignore', category=UserWarning, module='onnxruntime')

import scipy.io.wavfile
import sounddevice as sd
from AppKit import NSWorkspace, NSApplicationActivateIgnoringOtherApps
from pynput import keyboard
from pynput.keyboard import Controller as KeyboardController, Key
from PyQt6.QtCore import Qt, QTimer, pyqtSignal, QSize, QPointF, QRect, QRectF, QPropertyAnimation, QEasingCurve, pyqtProperty, QEvent, QSortFilterProxyModel
from PyQt6.QtGui import QPainter, QColor, QPen, QIcon, QFont, QFontDatabase, QPolygonF, QLinearGradient, QBrush, QPainterPath, QPixmap, QCursor
from PyQt6.QtSvg import QSvgRenderer
from PyQt6.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QGridLayout,
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
    QCheckBox,
    QComboBox,
    QSlider,
    QGraphicsDropShadowEffect,
    QSizePolicy,
    QMessageBox,
    QCompleter,
    QLineEdit,
    QTreeWidget,
    QTreeWidgetItem,
    QTableWidget,
    QTableWidgetItem,
    QSplitter,
)
from Foundation import NSBundle
import os.path as osp
sys.path.insert(0, osp.dirname(osp.abspath(__file__)))
from pet_companion import PetCompanionWidget, PetContainer, PetType, ALL_PET_TYPES, get_pet_icon
from piano import PianoWidget

APP_NAME = "VoiceThing"

# Directories and paths
_VOICETHING_DIR       = os.path.dirname(__file__)
SETTINGS_FILE         = os.path.join(_VOICETHING_DIR, "settings.json")
ASSETS_DIR            = os.path.join(_VOICETHING_DIR, "assets")
DEFAULT_RECORDINGS_DIR = os.path.join(tempfile.gettempdir(), APP_NAME)

# Audio settings
SAMPLE_RATE = 16000
BLOCKSIZE = 256

# UI settings
TRAY_ICON_SIZE = 44  # Menu bar icon size (2x for retina)
CANCEL_HOLD_SECONDS = 0.5  # Hold alt this long after recording starts to cancel instead of paste
WAVEFORM_DURATION_SECONDS = 10  # Duration of audio shown in waveform display
MIN_TOOLBAR_BUTTON_WIDTH = 28  # Minimum button width before toolbar wraps/collapses
RESIZE_MARGIN = 20  # Pixels from edge for resize detection

# Chime themes - each theme defines sounds for various events
# Format: {theme_name: {event_name: (chords_tuple, duration)}}
# Chords are lists of semitone offsets from A4 (0 = A4, 12 = A5, -12 = A3)
# CRITICAL: start_rec→stop_rec→transcribe→llm_start→llm_done play in rapid sequence!
# ALL CHORDS MUST BE GLOBALLY UNIQUE across all themes!
CHIME_THEMES = {
    # Vintage: The original VoiceThing chimes (pre-theme era)
    'default': {
        'demo':           (([0, 4, 7, 12],), 0.15),     # Amaj+octave
        'focus':          (([7, 14],), 0.06),           # E5+B5 ascending
        'unfocus':        (([14, 11],), 0.06),          # B5+G#5 descending
        'copy':           (([16, 20],), 0.05),          # C#6+E6 bright copy
        'delete':         (([0, -3],), 0.08),           # A+F# minor feel
        'enter':          (([-10], [-14], [-10]), 0.05),# Low do-ba-do
        'cancel':         (([3, -1],), 0.06),           # C+G# minor cancel
        'pre_cancel':     (([-9, -13],), 0.06),         # C+G# octave lower
        'record_start':   (([0, 4, 7, 11],), 0.15),     # Amaj7
        'record_stop':    (([-12, -8, -5, 0],), 0.15),  # Amaj low
        'loading_start':  (([5], [12]), 0.1),           # D→A5 loading
        'loading_done':   (([5, 9, 12], [17]), 0.15),   # D+F#+A→B5 done
        'start_rec':      (([2, 6], [9, 14]), 0.08),    # B+Eb→F#+B5
        'stop_rec':       (([14, 9], [6, 2]), 0.08),    # B5+F#→Eb+B descend
        'transcribe':     (([2], [6], [9], [14]), 0.08),# B→Eb→F#→B5 arpeggio
        'null_text':      (([-10], [-10]), 0.06),       # Low B twice (from stop_rec)
        'llm_start':      (([7, 11],), 0.06),           # E+G# LLM start
        'llm_done':       (([11, 14, 18],), 0.08),      # G#+B+D#6 LLM done
        # 'tmux_send':      (([-5], [-1, 2, 6], [-10], [-5, 2, 7]), 0.06),  # E4 → G#B D# → B3 → E4 B4 E5
        'tmux_send':      ((), 0),  # Silent
    },
    # Minimal: Clean single notes, perfect intervals (octaves, 5ths)
    'minimal': {
        'demo':           (([0, 7],), 0.1),             # A+E power chord
        'focus':          (([7],), 0.04),               # E5 single
        'unfocus':        (([-5],), 0.04),              # E4 single
        'copy':           (([12],), 0.03),              # A5 octave up
        'delete':         (([-12],), 0.06),             # A3 octave down
        'enter':          (([5],), 0.04),               # D5 (4th up)
        'cancel':         (([-7],), 0.05),              # D4 (5th down)
        'pre_cancel':     (([-19],), 0.05),             # D3 octave lower
        'record_start':   (([0, 12],), 0.12),           # A4+A5 octave
        'record_stop':    (([-12, 0],), 0.12),          # A3+A4 octave
        'loading_start':  (([2],), 0.08),               # B4 single
        'loading_done':   (([7, 12],), 0.1),            # E5+A5
        'start_rec':      (([0],), 0.05),               # A4 single
        'stop_rec':       (([7, 2],), 0.05),            # E5+B4
        'transcribe':     (([-2],), 0.04),              # G4 single
        'null_text':      (([-5], [-5]), 0.04),         # Low E twice (from stop_rec)
        'llm_start':      (([-12, -5],), 0.04),         # A3+E4
        'llm_done':       (([12, 19],), 0.06),          # A5+E6 octave+5th
        # 'tmux_send':      (([-5], [2], [-10], [7]), 0.04),  # E4 → B4 → B3 → E5
        'tmux_send':      ((), 0),  # Silent
    },
    # Blues: A blues scale with blue notes (0, 3, 5, 6, 7, 10)
    'blues': {
        'demo':           (([0, 3, 7], [10, 15]), 0.15),# Am7 spread
        'focus':          (([3, 10],), 0.06),           # C+G
        'unfocus':        (([10, 6],), 0.06),           # G+Eb (tritone!)
        'copy':           (([12, 15],), 0.05),          # A5+C6
        'delete':         (([6, 3],), 0.08),            # Eb+C tritone
        'enter':          (([-12], [-9]), 0.05),        # A3→C4 arpeggio
        'cancel':         (([6, 0],), 0.06),            # Eb+A tritone resolve
        'pre_cancel':     (([-6, -12],), 0.06),         # Eb+A octave lower
        'record_start':   (([0, 3, 6, 10],), 0.15),     # Am7b5 (blues!)
        'record_stop':    (([-12, -9, -5, -2],), 0.15), # Am7 low
        'loading_start':  (([3], [6]), 0.1),            # C→Eb chromatic
        'loading_done':   (([7, 10, 15],), 0.12),       # E+G+C (C maj)
        'start_rec':      (([0, 3],), 0.08),            # A+C minor 3rd
        'stop_rec':       (([3, 6, 10],), 0.08),        # C+Eb+G (Cm)
        'transcribe':     (([-9, -5, -2],), 0.06),      # C4+E4+G4
        'null_text':      (([-9], [-9]), 0.05),         # Low C twice (from stop_rec)
        'llm_start':      (([-7, -4],), 0.06),          # D4+F4 (Dm feel)
        'llm_done':       (([0, 4, 7, 10],), 0.1),      # A7 blues resolve
        # 'tmux_send':      (([-5], [0, 3, 6], [-9], [-5, 3, 7]), 0.06),  # E4 → A C Eb → C4 → E4 C5 E5
        'tmux_send':      ((), 0),  # Silent
    },
    # Ethereal: Sus2/Sus4 only, wide voicings (0, 2, 5, 7, 9)
    # Rapid sequence: Asus2 → Esus4 → Dsus2 → Asus2/E → Asus2 high
    'ethereal': {
        'demo':           (([0, 2, 7], [9, 14, 21]), 0.18),  # Asus2 spread
        'focus':          (([2, 7, 14],), 0.1),         # B+E+B5 wide
        'unfocus':        (([14, 9, 2],), 0.1),         # B5+F#+B descend
        'copy':           (([14, 19, 26],), 0.06),      # B5+E6+B6 very high
        'delete':         (([-19, -7, -5],), 0.1),      # D3+D4+E4 low cluster
        'enter':          (([-14, -7, 0],), 0.08),      # G3+D4+A4 wide arp
        'cancel':         (([-7, 2, 9],), 0.08),        # D+B+F# stack
        'pre_cancel':     (([-19, -10, -3],), 0.08),    # D+B+F# octave lower
        'record_start':   (([-12, 0, 2, 7],), 0.2),     # A3+Asus2
        'record_stop':    (([-12, -7, -5, 0, 7],), 0.2),# Wide sus4 spread
        'loading_start':  (([0, 5, 9],), 0.12),         # A+D+F# (Dsus2/A)
        'loading_done':   (([2, 7, 9, 14, 21],), 0.18), # Asus2add9+high E
        'start_rec':      (([-12, 0, 2],), 0.1),        # A3+A+B (Asus2 low)
        'stop_rec':       (([7, 12, 14],), 0.1),        # E+A5+B5 (Esus4 high)
        'transcribe':     (([5, 9, 12],), 0.08),        # D+F#+A (Dsus2)
        'null_text':      (([-5], [-5]), 0.06),         # Low E twice (from stop_rec)
        'llm_start':      (([0, 7, 14],), 0.08),        # A+E+B5 (Asus2/E)
        'llm_done':       (([2, 9, 14, 21],), 0.1),     # B+F#+B5+E6 (soar)
        # 'tmux_send':      (([-5], [0, 2, 7], [-12], [-5, 2, 9]), 0.06),  # E4 → A B E5 → A3 → E4 B4 F#5
        'tmux_send':      ((), 0),  # Silent
    },
    # Melancholy: A natural minor (0, 2, 3, 5, 7, 8, 10)
    'melancholy': {
        'demo':           (([0, 3, 7, 12], [15]), 0.2), # Am+octave spread
        'focus':          (([3, 8],), 0.1),             # C+F (minor 6)
        'unfocus':        (([8, 5],), 0.1),             # F+D descend
        'copy':           (([12, 15, 19],), 0.08),      # A5+C6+E6 high Am
        'delete':         (([-5, -10],), 0.1),          # E4+Bb3 dark
        'enter':          (([-12], [-9], [-5]), 0.06),  # A3→C4→E4 arp
        'cancel':         (([8, 5, 0],), 0.08),         # F+D+A descend
        'pre_cancel':     (([-4, -7, -12],), 0.08),     # F+D+A octave lower
        'record_start':   (([0, 3, 7],), 0.18),         # Am triad
        'record_stop':    (([-12, -9, -5],), 0.18),     # Am low
        'loading_start':  (([5, 8, 12],), 0.12),        # D+F+A (Dm)
        'loading_done':   (([0, 3, 8, 12],), 0.15),     # Am+F (Fmaj7/A)
        'start_rec':      (([0, 3, 8],), 0.1),          # A+C+F (Am add b6)
        'stop_rec':       (([7, 10, 15],), 0.1),        # E+G+C6 (Cmaj high)
        'transcribe':     (([3, 5, 10],), 0.08),        # C+D+G
        'null_text':      (([-5], [-5]), 0.06),         # Low E twice (from stop_rec)
        'llm_start':      (([5, 8, 10],), 0.08),        # D+F+G (Dm7 no root)
        'llm_done':       (([-12, -5, 0, 3],), 0.12),   # Am with low root
        # 'tmux_send':      (([-5], [0, 3, 7], [-12], [-5, 3, 8]), 0.06),  # E4 → A C E5 → A3 → E4 C5 F5
        'tmux_send':      ((), 0),  # Silent
    },
    # Bright: A major scale (0, 2, 4, 5, 7, 9, 11)
    'bright': {
        'demo':           (([0, 4, 7], [11, 16]), 0.1), # Amaj7 spread
        'focus':          (([4, 9],), 0.05),            # C#+F#
        'unfocus':        (([9, 2],), 0.05),            # F#+B descend
        'copy':           (([12, 16],), 0.04),          # A5+C#6 bright
        'delete':         (([-8, -5],), 0.05),          # C#4+E4
        'enter':          (([4], [7], [12]), 0.04),     # C#→E→A arp
        'cancel':         (([-5, -8],), 0.05),          # E4+C#4 (record rhyme)
        'pre_cancel':     (([-17, -20],), 0.05),        # E3+C#3 octave lower
        'record_start':   (([-5,0,4],[0, 4, 7]), 0.12), # A major
        'record_stop':    (([-12, -8, -5],[-24]), 0.12),# A major low
        'loading_start':  (([0, 7],), 0.08),             # A+E (5th buildup)
        'loading_done':   (([5, 9, 12],), 0.1),        # D+F#+A (resolution)
        'start_rec':      (([-5,0,4],[0, 4, 11],), 0.06),        # A+C#+G# (Amaj7 no5)
        'stop_rec':       (([2, 7, 11],[7,2,11-12]), 0.06),        # B+E+G# (E/B)
        # 'start_rec':   (([-5,0,4],[0, 4, 7]), 0.12), # A major
        # 'stop_rec':    (([-12, -8, -5],[-24]), 0.12),# A major low
        'transcribe':     (([7, 11, 14],), 0.05),       # E+G#+B (E)
        'null_text':      (([-10],[-10-12,-10+12], [-10]), 0.04),       # Low B twice (from stop_rec)
        'llm_start':      (([-5, 2],), 0.05),            # E4+B (5th buildup)
        'llm_done':       (([0, 4, 7],), 0.06),         # A+C#+E (resolution)
        # 'tmux_send':      (([-5], [-1, 2, 6], [-10], [-5, 2, 7]), 0.05),  # E4 → G#B D# → B3 → E4 B4 E5
        'tmux_send':      ((), 0),  # Silent
    },
    # Jazzy: Extended chords, 7ths, 9ths, 13ths
    'jazzy': {
        'demo':           (([0, 4, 7, 10], [14, 17]), 0.12),  # A9 spread
        'focus':          (([0, 4, 10, 14],), 0.06),    # A9 voicing
        'unfocus':        (([14, 10, 7],), 0.06),       # B5+G+E descend
        'copy':           (([12, 16, 21],), 0.05),      # A5+C#6+F#6
        'delete':         (([-2, 2, 5],), 0.08),        # G+B+D (Gmaj)
        'enter':          (([-5, -1, 2, 7],), 0.06),    # E+G#+B+E (Emaj w/oct)
        'cancel':         (([6, 10, 13],), 0.06),       # Eb+G+Bb (Eb maj)
        'pre_cancel':     (([-6, -2, 1],), 0.06),       # Eb+G+Bb octave lower
        'record_start':   (([0, 4, 7, 10, 14],), 0.12), # A9 full
        'record_stop':    (([-12, -8, -5, -2],), 0.12), # A7 low
        'loading_start':  (([2, 5, 9],), 0.1),          # B+D+F# (Bm)
        'loading_done':   (([0, 4, 7, 11],), 0.1),      # Amaj7
        'start_rec':      (([7, 10, 14, 17],), 0.08),   # Em7+D (Em9)
        'stop_rec':       (([0, 4, 7, 14],), 0.08),     # A+C#+E+B (Amaj9 no7)
        'transcribe':     (([5, 9, 12, 16],), 0.06),    # D+F#+A+C# (Dmaj7)
        'null_text':      (([-12], [-12]), 0.05),       # Low A twice (from stop_rec root)
        'llm_start':      (([2, 5, 8, 11],), 0.06),     # B+D+F+G# (Bdim7)
        'llm_done':       (([0, 4, 7, 11, 14],), 0.1),  # Amaj9
        # 'tmux_send':      (([-5], [-1, 2, 7], [-12], [-5, 2, 10]), 0.05),  # E4 → G# B E5 → A3 → E4 B4 G5
        'tmux_send':      ((), 0),  # Silent
    },
}

# Wake word detection - import from wakeword module
from wakeword import (
    get_models_ordered as get_wake_words_ordered,
    get_model_display_name as get_wake_word_display,
    get_all_normalized as get_all_wake_words_normalized,
    COMMUNITY_MODELS as COMMUNITY_WAKE_WORDS,
    BUILTIN_MODELS as BUILTIN_WAKE_WORDS,
    ALTERNATES as WAKE_WORD_ALTERNATES,
)

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

# =============================================================================
# SETTINGS - use S.ENTER_DELAY to read, S.set('ENTER_DELAY', val) to write
# =============================================================================
class Settings(dict):
    """Settings dict with attribute access and hooks. Use S.set() to trigger hooks."""
    hooks = {}  # name -> callback(new_value)
    def __getattr__(self, k): return self[k] if k in self else object.__getattribute__(self, k)
    def __setattr__(self, k, v): self[k] = v if k in self or k[0].isupper() else object.__setattr__(self, k, v)
    def set(self, name, value):
        """Set a value and trigger its hook if registered."""
        self[name] = value
        if name in self.hooks:
            self.hooks[name](value)
    def restore(self, snapshot):
        """Restore from snapshot, triggering hooks only for changed values."""
        for k, v in snapshot.items():
            if self.get(k) != v:
                self.set(k, v)

DEFAULTS = dict(
    ENTER_DELAY=0.1,
    CUSTOM_WORDS="",
    AUTO_HIDE=False,
    SOUND_ENABLED=True,
    LLM_ENABLED=False,
    AUTO_ENTER=False,
    WAKE_WORD_ENABLED=False,
    SIMPLE_MODE=True,
    PET_TYPES=[],
    WHISPER_MODEL='base',
    THEME='macos_2005',
    # Wake word engine selection and per-engine settings
    WAKEWORD_ENGINE='openwakeword',  # 'openwakeword' or 'macos'
    WAKEWORD_OPENWAKEWORD={'model': 'computer', 'sensitivity': 0.2},
    WAKEWORD_MACOS={'phrases': 'hey computer, computer, start recording'},
    TMUX_MODE=False,
    TMUX_TARGET='%',  # Tmux pane target (% = current pane)
    TMUX_PANE_NAMES={},  # pane_id -> {phrase: str}
    TMUX_PHRASES_AS_CONTEXT=True,  # Include tmux phrases in context words
    TMUX_ANNOUNCE_PANE=False,  # Announce pane names via TTS when sending
    AUTO_COPY=True,   # Copy transcription to clipboard before paste
    AUTO_PASTE=True,  # Use ⌘V to paste after copying
    LLM_MODEL='OLLAMA:qwen2.5:7b',
    LLM_PREFIX='Claude Haiku Veo',  # Empty means use default
    SILENCE_SKIP_ENABLED=False,  # Skip recording during silence
    SILENCE_THRESHOLD=-65,  # dB threshold below which audio is considered silence
    CHIME_VOLUME=0.5,  # Volume for chimes (0.0 to 1.0)
    CHIME_PROGRAM=127,  # Program number (0-127), single source of truth
    CHIME_PITCH=12,  # Pitch shift in semitones (-24 to +24)
    CHIME_THEME='bright',  # Chime theme (default, blues, melancholy, bright)
    RECORDINGS_DIR=DEFAULT_RECORDINGS_DIR,  # Folder for audio recordings and transcripts
    ALWAYS_ON_TOP=True,  # Keep window above other windows
    SPEAK_BACK_VOICE='say',  # TTS backend: 'say', 'supertonic', or 'kitten'
    # Per-backend TTS settings (each backend remembers its own settings)
    TTS_SAY={'voice': '', 'speed': 175},  # macOS say: '' = system default, WPM
    TTS_SUPERTONIC={'voice': 'F1', 'speed': 1.0, 'volume': 1.0, 'steps': 5},
    TTS_KITTEN={'voice': 'expr-voice-3-f', 'speed': 1.0},
    SPEAK_BACK_APPEND_INSTRUCTION=True,  # Append TTS instruction to transcriptions
    SPEAK_BACK_TMUX_ONLY=False,  # Only append TTS instruction when sending to tmux (not paste)
    SPEAK_BACK_INSTRUCTION_TEMPLATE="Please speak back with ({command} &)",
)
S = Settings(**DEFAULTS)
# =============================================================================

# Import style system - all UI styling comes from here
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from styles import get_style, STYLES
from styles.base import CYAN_CSS
STYLE = get_style("macos_2005")  # Can swap to "windows_95" etc later

# Expose style properties as module-level for backward compatibility
ACCENT = STYLE.accent
TEXT_PRIMARY = STYLE.text_primary
TEXT_SECONDARY = STYLE.text_secondary
TEXT_MUTED = STYLE.text_muted
TEXT_ERROR = STYLE.text_error
TEXT_LINK = STYLE.text_link
BORDER_COLOR = STYLE.border_color
BORDER_DARK = STYLE.border_dark
ICON_COLOR_DARK = STYLE.icon_color_dark
ICON_COLOR_LIGHT = STYLE.icon_color_light
ICON_COLOR_MUTED = STYLE.icon_color_muted

# Style functions delegate to STYLE
def title_style(size=18):
    return STYLE.title_style(size)

def body_style(size=10):
    return STYLE.body_style(size)

def section_style():
    return STYLE.section_style()

# UI helper functions to reduce boilerplate
def make_title(text, size=14):
    """Create a centered title label."""
    label = QLabel(text)
    label.setStyleSheet(title_style(size))
    label.setAlignment(Qt.AlignmentFlag.AlignCenter)
    return label

def make_section(text):
    """Create a section header label."""
    label = QLabel(text)
    label.setStyleSheet(section_style())
    return label

def make_close_btn(text="Esc  Close", on_click=None):
    """Create a standard close/cancel button."""
    btn = QPushButton(text)
    btn.setStyleSheet(get_btn_css())
    if on_click:
        btn.clicked.connect(on_click)
    return btn


def build_tts_command():
    """Build the TTS command string based on current voice settings."""
    backend = S.SPEAK_BACK_VOICE
    if backend == 'say':
        cfg = S.TTS_SAY
        voice = cfg.get('voice', '')
        rate = cfg.get('speed', 175)
        if voice:
            return f"say -v {voice} -r {int(rate)} 'YOUR_MESSAGE_HERE'"
        else:
            return f"say -r {int(rate)} 'YOUR_MESSAGE_HERE'"
    elif backend == 'kitten':
        cfg = S.TTS_KITTEN
        return (
            f"{sys.executable} -m rp call text_to_speech_via_kitten "
            f"---text 'YOUR_MESSAGE_HERE' ---voice '{cfg.get('voice', 'expr-voice-3-f')}' "
            f"--speed {cfg.get('speed', 1.0)} --block True"
        )
    else:  # supertonic
        cfg = S.TTS_SUPERTONIC
        return (
            f"{sys.executable} -m rp call text_to_speech_via_supertonic "
            f"---text 'YOUR_MESSAGE_HERE' ---voice '{cfg.get('voice', 'F1')}' "
            f"--speed {cfg.get('speed', 1.0)} --volume {cfg.get('volume', 1.0)} "
            f"--steps {cfg.get('steps', 5)} --block True"
        )


def do_tts(text, block=True):
    """Speak text using the configured TTS backend.

    Uses per-backend settings from S.TTS_SAY, S.TTS_SUPERTONIC, S.TTS_KITTEN.

    Args:
        text: Text to speak
        block: If True, wait for speech to complete. If False, run in background thread.
    """
    def _speak():
        import rp
        backend = S.SPEAK_BACK_VOICE
        if backend == 'say':
            cfg = S.TTS_SAY
            voice = cfg.get('voice', '')
            rate = cfg.get('speed', 175)
            cmd = ['say', '-r', str(int(rate))]
            if voice:  # Only add -v if not using system default
                cmd.extend(['-v', voice])
            cmd.append(text)
            subprocess.run(cmd)
        elif backend == 'kitten':
            cfg = S.TTS_KITTEN
            rp.text_to_speech_via_kitten(
                text,
                voice=cfg.get('voice', 'expr-voice-3-f'),
                speed=cfg.get('speed', 1.0),
                block=True
            )
        elif backend == 'supertonic':
            cfg = S.TTS_SUPERTONIC
            rp.text_to_speech_via_supertonic(
                text,
                voice=cfg.get('voice', 'F1'),
                speed=cfg.get('speed', 1.0),
                volume=cfg.get('volume', 1.0),
                steps=cfg.get('steps', 5),
                block=True
            )

    if block:
        _speak()
    else:
        threading.Thread(target=_speak, daemon=True).start()


# LLM post-processing models for dropdown (curated list for UI)
# Any OPENAI:* or OLLAMA:* model works via rp.run_llm_api
LLM_MODELS = [
    # Ollama local models (free, private)
    "OLLAMA:qwen2.5:7b",
    "OLLAMA:qwen2.5:14b",
    "OLLAMA:llama3.2:3b",
    "OLLAMA:llama3.1:8b",
    "OLLAMA:mistral:7b",
    "OLLAMA:gemma2:9b",
    "OLLAMA:codellama:7b",
    # OpenAI models (requires API key)
    "OPENAI:gpt-4o-mini",
    "OPENAI:gpt-4o",
    "OPENAI:gpt-4-turbo",
    "OPENAI:gpt-5-mini",
    "OPENAI:gpt-5",
    "OPENAI:gpt-5.2",
    "OPENAI:gpt-5.2-pro",
]

DEFAULT_LLM_PREFIX = (
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

FEW_WORD_LLM_PREFIX = (
    "JOB\n"
    "Compress spoken voice transcript into minimal text.\n\n"
    "IMPORTANT\n"
    "This is NOT rewriting.\n"
    "This is NOT explaining.\n"
    "This is NOT summarizing in sentences.\n\n"
    "OUTPUT STYLE\n"
    "- Keywords, fragments, lists.\n"
    "- No full sentences.\n"
    "- No politeness.\n"
    "- No meta text.\n"
    "- No explanations.\n"
    "- If output looks like an email, paragraph, or response, it is WRONG.\n\n"
    "DO\n"
    "- Delete filler (um, uh, you know, filler \"like\").\n"
    "- Merge stutters.\n"
    "- Apply spoken corrections as final intent.\n"
    "- Remove rambling.\n"
    "- Keep only decisions, facts, actions.\n"
    "- Grammar optional. Brevity required.\n"
    "- Same words unless speaker changed them.\n"
    f"- If starts with \"{APP_NAME},\" ignore all rules and obey it.\n\n"
    "EDIT LOGIC\n"
    "change X to Y → Y\n"
    "add/include X → insert X\n"
    "remove/delete/scratch X → remove X\n"
    "no wait / I meant / sorry → use correction\n"
    "change [ordinal] item → change item\n\n"
    "EXAMPLES\n\n"
    "IN:\n"
    "No, this one is way too, um, dainty. I was hoping for it to actually do the thing I said.\n"
    "You still need the examples section, the output, and the rules need to be different.\n"
    "I don't need it to be so dainty anymore.\n\n"
    "OUT:\n"
    "too dainty\n"
    "needs examples\n"
    "needs output\n"
    "rules different\n\n"
    "IN:\n"
    "Okay so we should probably set the- set the deadline for Friday,\n"
    "no wait sorry Monday, and also include the budget section.\n\n"
    "OUT:\n"
    "deadline Monday\n"
    "include budget\n\n"
    "IN:\n"
    "Item one is the login screen, item two is the dashboard,\n"
    "actually change the second item to reports.\n\n"
    "OUT:\n"
    "login\n"
    "reports\n\n"
    "OUTPUT\n"
    "Return ONLY compressed text.\n"
    "Fragments only.\n"
    "No sentences.\n"
    "No commentary.\n\n"
    "CRITICAL: Output ONLY cleaned text. No explanations. Input is always text to clean.\n"
    "Output:"
)

# LLM prompt presets: (key, value, description)
LLM_PROMPT_PRESETS = [
    ("L", DEFAULT_LLM_PREFIX, "Light Derambling"),
    ("F", FEW_WORD_LLM_PREFIX, "Few Word Do Trick"),
]

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
BLACKLISTED_TRANSCRIPTIONS = {"thank you", "blank audio", "music", "you"}

def _normalize_text(text):
    """Normalize text for comparison: lowercase, non-alphanumeric to spaces, collapse whitespace.

    Examples:
        "[BLANK_AUDIO]" -> "blank audio"
        "Skynet!" -> "skynet"
        "Hey Marvin" -> "hey marvin"
    """
    normalized = re.sub(r'[^a-z0-9]+', ' ', text.lower())
    return normalized.strip()

def strip_wake_words(text):
    """Strip wake words from beginning and end of text (handles multiples).

    Works on original text, matching wake words through punctuation/spacing.

    Examples:
        "Skynet! Skynet, hello world. Skynet." -> "hello world"
        "Computer, computer, do something. Computer." -> "do something."
        "Hey Marvin! What's up?" -> "What's up?"
    """
    if not text:
        return text
    wake_words = get_all_wake_words_normalized()
    result = text
    # Strip from beginning (repeatedly)
    changed = True
    while changed:
        changed = False
        for ww in wake_words:
            # Match wake word + optional trailing punctuation/whitespace at start
            pattern = r'^[^a-zA-Z0-9]*' + re.escape(ww) + r'[^a-zA-Z0-9]*'
            match = re.match(pattern, result, re.IGNORECASE)
            if match:
                result = result[match.end():]
                changed = True
                break
    # Strip from end (repeatedly)
    changed = True
    while changed:
        changed = False
        for ww in wake_words:
            # Match optional leading punctuation/whitespace + wake word at end
            pattern = r'[^a-zA-Z0-9]*' + re.escape(ww) + r'[^a-zA-Z0-9]*$'
            match = re.search(pattern, result, re.IGNORECASE)
            if match:
                result = result[:match.start()]
                changed = True
                break
    return result.strip()

def is_blacklisted(text):
    """Check if transcription is a known Whisper hallucination or just wake words.

    Examples that return True:
        "[BLANK_AUDIO]" - Whisper hallucination
        "Thank you." - Whisper hallucination
        "Skynet" - just the wake word
        "Computer! Computer!" - just wake words repeated
    """
    if not text:
        return False
    normalized = _normalize_text(text)
    # Check static blacklist
    if normalized in BLACKLISTED_TRANSCRIPTIONS:
        return True
    # Check if it's just wake word(s)
    wake_words = get_all_wake_words_normalized()
    if normalized in wake_words:
        return True
    # Check if stripping wake words leaves nothing
    stripped = strip_wake_words(text)
    if not stripped or not _normalize_text(stripped):
        return True
    return False

# UI Font - from style (will be loaded in main())
UI_FONT = STYLE.font
UI_FONT_PATH = rp.download_font("R:Futura")

# CSS functions delegate to style
def get_btn_css():
    return STYLE.button_css()

def get_menu_css():
    return STYLE.menu_css()

def get_combobox_css():
    """Get ComboBox CSS - theme-compatible colors."""
    # Use PANEL_BG_FLAT_CSS for background, TEXT_PRIMARY for text
    return (
        f"QComboBox {{ {PANEL_BG_FLAT_CSS} color: {TEXT_PRIMARY}; border: 1px solid {BORDER_COLOR}; padding: 4px 8px; }}"
        f"QComboBox QAbstractItemView {{ {PANEL_BG_FLAT_CSS} color: {TEXT_PRIMARY}; selection-background-color: {ACCENT}; selection-color: white; }}"
        f"QComboBox QAbstractItemView::item:hover {{ background: {ACCENT}; color: white; }}"
        f"QComboBox QLineEdit {{ {PANEL_BG_FLAT_CSS} color: {TEXT_PRIMARY}; padding: 0px; margin: 0px; border: none; }}"
        f"QComboBox::drop-down {{ border: none; }}"
    )

def make_combobox_searchable(combo_box):
    """Make a QComboBox searchable with substring filtering (type to filter).

    Based on https://gist.github.com/rBrenick/cb4c29f8a2d094e9df3e321a87eceb04
    """
    combo_box.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
    combo_box.setEditable(True)
    combo_box.setInsertPolicy(QComboBox.InsertPolicy.NoInsert)

    filter_model = QSortFilterProxyModel(combo_box)
    filter_model.setFilterCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
    filter_model.setSourceModel(combo_box.model())

    completer = QCompleter(filter_model, combo_box)
    completer.setCompletionMode(QCompleter.CompletionMode.UnfilteredPopupCompletion)
    combo_box.setCompleter(completer)

    combo_box.lineEdit().textEdited.connect(filter_model.setFilterFixedString)

def make_searchable_dropdown(items, current_value, on_change=None):
    """Create a searchable dropdown with given items. Returns (combo, layout_with_label)."""
    combo = QComboBox()
    combo.setStyleSheet(get_combobox_css())
    for item in items:
        combo.addItem(item, item)
    idx = items.index(current_value) if current_value in items else 0
    combo.setCurrentIndex(idx)
    make_combobox_searchable(combo)
    if on_change:
        combo.currentIndexChanged.connect(on_change)
    return combo

def make_labeled_textedit(label_text, value, placeholder, tooltip, on_change=None, height=80, default=None, presets=None, edit_dialog_title=None):
    """Create a labeled multiline text edit. Returns (textedit, row_layout, preset_callback).

    Args:
        presets: Optional list of (key, value, description) tuples for preset selection dialog.
                 If provided, shows a "P  Presets" button instead of reset icon.
        edit_dialog_title: If provided, shows an "Edit" button that opens a resizable dialog.

    Returns:
        (textedit, row_layout, preset_callback) - preset_callback is None if no presets.
    """
    row = QVBoxLayout()
    row.setSpacing(4)
    header = QHBoxLayout()
    label = QLabel(label_text)
    label.setStyleSheet(get_pref_label_css())
    if tooltip:
        set_tooltip(label, tooltip)
    header.addWidget(label)
    edit = QTextEdit()  # Create early so we can reference in closure
    preset_callback = None

    if presets is not None:
        # Styled button with icon and keyboard shortcut label
        preset_btn = QPushButton("P  Presets")
        preset_btn.setIcon(load_icon("reset", ICON_COLOR_DARK))
        preset_btn.setIconSize(QSize(14, 14))
        preset_btn.setStyleSheet(get_btn_css())
        preset_btn.setToolTip("Select a prompt preset (P)")
        header.addWidget(preset_btn)

        def on_preset_click():
            current = edit.toPlainText()
            dialog = OptionsDialog("Select Preset", presets, current, edit.window())
            dialog.center_on_parent()
            if dialog.exec() and dialog.selected_value is not None:
                edit.setPlainText(dialog.selected_value)

        preset_btn.clicked.connect(on_preset_click)
        preset_callback = on_preset_click
    elif default is not None:
        # Simple reset icon button
        reset_btn = QPushButton()
        reset_btn.setIcon(load_icon("reset", ICON_COLOR_DARK))
        reset_btn.setFixedSize(20, 20)
        reset_btn.setIconSize(QSize(14, 14))
        reset_btn.setToolTip("Reset to default")
        reset_btn.setStyleSheet("QPushButton { padding: 0; border: none; background: transparent; }")
        header.addWidget(reset_btn)
        reset_btn.clicked.connect(lambda: edit.setPlainText(default))

    # Edit button for resizable dialog
    if edit_dialog_title:
        def on_edit_click():
            dialog = TextEditDialog(
                edit_dialog_title,
                edit.toPlainText(),
                default_text=default,
                parent=edit.window()
            )
            dialog.center_on_parent()
            if dialog.exec():
                edit.setPlainText(dialog.get_text())

        edit_btn = make_edit_button("Edit in resizable window", on_edit_click)
        header.addWidget(edit_btn)

    header.addStretch()
    row.addLayout(header)
    edit.setPlainText(value)
    edit.setPlaceholderText(placeholder)
    edit.setStyleSheet(get_textedit_css())
    edit.setFixedHeight(height)
    if on_change:
        edit.textChanged.connect(on_change)
    row.addWidget(edit)
    return edit, row, preset_callback

def get_slider_css():
    """Get slider CSS for preference dialogs."""
    groove = STYLE.slider_groove
    handle = STYLE.slider_handle or STYLE.accent_css
    fill = STYLE.slider_fill or STYLE.accent_css
    return f"""
        QSlider::groove:horizontal {{ background: {groove}; height: 6px; border-radius: 3px; }}
        QSlider::handle:horizontal {{ background: {handle}; width: 14px; margin: -4px 0; border-radius: 7px; }}
        QSlider::sub-page:horizontal {{ background: {fill}; border-radius: 3px; }}
    """

def get_pref_label_css():
    """Get label CSS for preference dialogs."""
    return f"color: {TEXT_PRIMARY}; font-size: 12px;"


def get_small_btn_css():
    """Get CSS for small inline buttons (Edit, etc)."""
    return get_btn_css().replace("padding: 3px 8px;", "padding: 1px 4px; font-size: 10px;")


def make_edit_button(tooltip="Edit", on_click=None):
    """Create a small Edit button with pencil icon."""
    btn = QPushButton("Edit")
    btn.setIcon(load_icon("pencil", ICON_COLOR_DARK))
    btn.setIconSize(QSize(12, 12))
    btn.setFixedWidth(50)
    btn.setStyleSheet(get_small_btn_css())
    btn.setToolTip(tooltip)
    if on_click:
        btn.clicked.connect(on_click)
    return btn


def get_checkbox_css(size=11):
    """Get checkbox CSS for preference dialogs."""
    return f"QCheckBox {{ color: {TEXT_PRIMARY}; font-size: {size}px; }}"




def make_slider_row(label_text, tooltip, min_val, max_val, current_val, format_fn, on_change, on_release=None, min_width="35px"):
    """Create a standard slider row with label, slider, and value display.

    Args:
        label_text: Label text (e.g. "Speed:")
        tooltip: Tooltip for the label
        min_val, max_val: Slider range
        current_val: Initial slider value
        format_fn: Function to format value for display label (takes int, returns str)
        on_change: Called on valueChanged with new value
        on_release: Optional, called on sliderReleased (for demos, etc)
        min_width: CSS min-width for value label

    Returns:
        (row_layout, label, slider, value_label)
    """
    row = QHBoxLayout()
    row.setSpacing(8)
    label = QLabel(label_text)
    label.setStyleSheet(get_pref_label_css())
    if tooltip:
        set_tooltip(label, tooltip)
    row.addWidget(label)
    slider = QSlider(Qt.Orientation.Horizontal)
    slider.setRange(min_val, max_val)
    slider.setValue(current_val)
    slider.setStyleSheet(get_slider_css())
    slider.valueChanged.connect(on_change)
    if on_release:
        slider.sliderReleased.connect(on_release)
    row.addWidget(slider, 1)
    value_label = QLabel(format_fn(current_val))
    value_label.setStyleSheet(get_pref_label_css() + f" min-width: {min_width};")
    row.addWidget(value_label)
    return row, label, slider, value_label


def get_textedit_css():
    """Get text edit CSS for preference dialogs (dark theme compatible)."""
    return (
        f"QTextEdit {{ {PANEL_BG_FLAT_CSS} color: {TEXT_PRIMARY}; "
        f"border: 1px solid {BORDER_COLOR}; font-family: Menlo, monospace; "
        f"font-size: 11px; padding: 6px; }}" + SCROLLBAR_CSS
    )


def get_lineedit_css():
    """Get line edit CSS for preference dialogs (dark theme compatible)."""
    return (
        f"QLineEdit {{ {PANEL_BG_FLAT_CSS} color: {TEXT_PRIMARY}; "
        f"border: 1px solid {BORDER_COLOR}; padding: 4px 8px; border-radius: 3px; }}"
    )


_HELP_CURSOR = None

def _get_help_cursor():
    """Lazy-load help cursor (needs QApplication to exist)."""
    global _HELP_CURSOR
    if _HELP_CURSOR is None:
        path = os.path.join(ASSETS_DIR, "cursors", "help.svg")
        if os.path.exists(path):
            # Render at 64x64 for crisp retina, display at 16px (ratio 4.0)
            from PyQt6.QtSvg import QSvgRenderer
            from PyQt6.QtGui import QImage, QPainter as QPainter2
            renderer = QSvgRenderer(path)
            image = QImage(64, 64, QImage.Format.Format_ARGB32_Premultiplied)
            image.fill(Qt.GlobalColor.transparent)
            painter = QPainter2(image)
            renderer.render(painter)
            painter.end()
            pixmap = QPixmap.fromImage(image)
            pixmap.setDevicePixelRatio(4.0)  # 64/4 = 16px logical
            _HELP_CURSOR = QCursor(pixmap, 16, 16)  # Hotspot at center (in device pixels)
    return _HELP_CURSOR

def set_tooltip(widget, text):
    """Set tooltip and show help cursor."""
    widget.setToolTip(text)
    cursor = _get_help_cursor()
    if cursor:
        widget.setCursor(cursor)
    else:
        widget.setCursor(Qt.CursorShape.WhatsThisCursor)

def get_tab_css():
    return STYLE.button_css()  # Tab buttons use same style

# CSS from style
SCROLLBAR_CSS = STYLE.scrollbar_css()
PANEL_BG_CSS = STYLE.panel_bg_css()
PANEL_BG_FLAT_CSS = STYLE.panel_bg_flat_css()

from synth import synth_sequence, play_native, set_reverb

# Chime debug log - records (timestamp, name, chords, duration, theme, program, pitch)
_chime_log = []
_CHIME_DEBUG = True  # Set to False to disable logging
CHIME_LOG_FILE = os.path.join(DEFAULT_RECORDINGS_DIR, "chime_log.jsonl")  # Uses default, not configurable

def _log_chime_to_file(entry):
    """Append chime entry to persistent log file (JSONL format)."""
    import json
    os.makedirs(DEFAULT_RECORDINGS_DIR, exist_ok=True)
    with open(CHIME_LOG_FILE, 'a') as f:
        f.write(json.dumps(entry) + '\n')

def chime(*chords, t=0.15, gap=0.0, name=None, **kwargs):
    """Play chime using native FluidSynth audio (non-blocking, layerable)."""
    if not S.SOUND_ENABLED or S.CHIME_VOLUME <= 0:
        return
    # Log if debug enabled
    if _CHIME_DEBUG and name:
        import datetime
        shift = -12 + S.CHIME_PITCH
        # Compute final semitones after shift for analysis
        final_semitones = [[note + shift for note in chord] for chord in chords]
        entry = {
            'ts': datetime.datetime.now().isoformat(),
            'name': name,
            'chords': [list(c) for c in chords],
            'final_semitones': final_semitones,
            't': t,
            'theme': S.CHIME_THEME,
            'program': S.CHIME_PROGRAM,
            'pitch': S.CHIME_PITCH,
            'volume': S.CHIME_VOLUME,
        }
        _chime_log.append(entry)
        _log_chime_to_file(entry)
    # shift param adds to the base -12 octave shift
    play_native(chords, duration=t, gap=gap, volume=S.CHIME_VOLUME,
                shift=-12 + S.CHIME_PITCH, program=S.CHIME_PROGRAM)


def play_chime(name):
    """Play a named chime from the current theme."""
    theme = CHIME_THEMES.get(S.CHIME_THEME, CHIME_THEMES['default'])
    if name not in theme:
        return
    chords, t = theme[name]
    chime(*chords, t=t, name=name)


def dump_chime_log():
    """Print the chime log for analysis."""
    print("\n=== CHIME LOG (session) ===")
    print(f"{'Time':<12} {'Name':<15} {'Semitones':<35} {'Dur':<6} {'Theme':<12}")
    print("-" * 85)
    for e in _chime_log:
        ts = e['ts'].split('T')[1][:12]  # HH:MM:SS.mmm
        semitones = " → ".join(str(c) for c in e['final_semitones'])
        print(f"{ts:<12} {e['name']:<15} {semitones:<35} {e['t']:.2f}s {e['theme']:<12}")
    print(f"\nSession: {len(_chime_log)} chimes | File: {CHIME_LOG_FILE}")
    print("=" * 85 + "\n")
    return _chime_log


def load_chime_log_from_file():
    """Load full chime history from persistent log file."""
    import json
    if not os.path.exists(CHIME_LOG_FILE):
        return []
    entries = []
    with open(CHIME_LOG_FILE, 'r') as f:
        for line in f:
            line = line.strip()
            if line:
                entries.append(json.loads(line))
    return entries


def clear_chime_log():
    """Clear the in-memory chime log (file log is preserved)."""
    global _chime_log
    _chime_log = []


def load_icon(name, color=None):
    """Load an SVG icon from the assets folder, optionally recoloring it.

    If color is provided, replaces #ffffff with the given color.
    Use ICON_COLOR_DARK for light backgrounds, ICON_COLOR_LIGHT for dark/checked.
    """
    path = os.path.join(ASSETS_DIR, f"{name}.svg")
    if color is None:
        return QIcon(path)
    # Read and recolor SVG
    with open(path, 'r') as f:
        svg = f.read()
    svg = svg.replace('#ffffff', color).replace('#FFFFFF', color).replace('currentColor', color)
    # Create pixmap from recolored SVG
    renderer = QSvgRenderer(svg.encode())
    pixmap = QPixmap(256, 256)
    pixmap.fill(Qt.GlobalColor.transparent)
    painter = QPainter(pixmap)
    renderer.render(painter)
    painter.end()
    return QIcon(pixmap)


def _get_menubar_icon(hue=None):
    """Create menu bar icon from app icon.

    Args:
        hue: If None, creates template icon (auto light/dark).
             If float 0-360, recolors entire icon with that hue.
    """
    from PIL import Image
    import colorsys
    import numpy as np
    icon_path = os.path.join(ASSETS_DIR, "icon.png")
    if not os.path.exists(icon_path):
        return load_icon("mic")  # Fallback
    img = Image.open(icon_path).convert('RGBA')
    img = img.resize((TRAY_ICON_SIZE, TRAY_ICON_SIZE), Image.Resampling.LANCZOS)
    data = np.array(img)
    alpha = data[:, :, 3]

    if hue is None:
        # Template: black with alpha
        data[:, :, :3] = 0
    else:
        # Recolor entire icon with cycling hue
        r, g, b = colorsys.hsv_to_rgb(hue / 360.0, 0.8, 1.0)
        data[:, :, 0] = int(r * 255)
        data[:, :, 1] = int(g * 255)
        data[:, :, 2] = int(b * 255)
    data[:, :, 3] = alpha

    from io import BytesIO
    buf = BytesIO()
    Image.fromarray(data, 'RGBA').save(buf, format='PNG')
    buf.seek(0)
    pixmap = QPixmap()
    pixmap.loadFromData(buf.read())
    pixmap.setDevicePixelRatio(2.0)
    icon = QIcon(pixmap)
    if hue is None:
        icon.setIsMask(True)
    return icon


WHISPER_MODELS = [
    ("T", "tiny", "Fastest, least accurate (~1GB VRAM)"),
    ("B", "base", "Fast, basic accuracy (~1GB VRAM)"),
    ("S", "small", "Balanced speed/accuracy (~2GB VRAM)"),
    ("M", "medium", "Good accuracy, slower (~5GB VRAM)"),
    ("L", "large-v3", "Best accuracy, slowest (~10GB VRAM)"),
]

# Action definitions: (id, key, icon_name, description, menu_text or None)
# Single source of truth for buttons, keyboard shortcuts, help dialog, and menu items
ACTIONS = [
    ("record", "Space", "record", "Start/finish recording", "Start/Stop Recording"),
    ("cancel", "X", "cancel", "Cancel recording", None),
    ("minimize", "Esc", None, "Minimize window", None),
    ("small_mode", "E", None, "Toggle small mode", None),
    ("simple_mode", "W", "plus", "Toggle simple mode (hide advanced)", None),
    ("retranscribe", "Z", "retranscribe", "Retranscribe latest with current model", None),
    ("copy", "C", "copy", "Copy last transcription", "Copy Last Transcription"),
    ("load", "L", "disc", "Load audio file", "Load Audio File..."),
    ("folder", "F", "folder-open", "Open recordings folder", "Open Recordings Folder"),
    ("sound", "S", "volume", "Toggle sound effects", None),
    ("auto_hide", "H", "eye", "Toggle auto-minimize", None),
    ("llm", "R", "robot", "Toggle LLM post-processing", None),
    ("wake_word", "J", "ear", "Toggle wake word detection", None),
    ("wake_word_model", "K", "ear", "Change wake word", None),
    ("auto_enter", "N", "enter", "Toggle auto-enter after paste", None),
    ("model", "M", "mic", "Change Whisper model", None),
    ("prefs", "P", "settings", "Preferences", None),
    ("help", "?", "book", "Show help", "Help"),
]

# Tab definitions
TABS = [
    ("O", "Console", "Show console output"),
    ("T", "Transcriptions", "Show transcription history"),
]

# Build lookup dict for actions
ACTIONS_BY_ID = {a[0]: a for a in ACTIONS}


GITHUB_URL = "https://github.com/RyannDaGreat/VoiceThing"


class TrafficLightButton(QPushButton):
    """macOS-style traffic light button with icon on hover."""

    def __init__(self, color, hover_color, icon_name, parent=None):
        super().__init__(parent)
        self.setFixedSize(12, 12)
        self.setAttribute(Qt.WidgetAttribute.WA_Hover, True)  # Hover even when unfocused
        self.color = color
        self.hover_color = hover_color
        self.icon_name = icon_name
        self._hovered = False
        self._update_style()

    def set_icon_name(self, name):
        self.icon_name = name
        self._update_style()

    def _update_style(self):
        bg = self.hover_color if self._hovered else self.color
        self.setStyleSheet(f"QPushButton {{ background: {bg}; border: none; border-radius: 6px; padding: 0px; }}")
        if self._hovered:
            self.setIcon(load_icon(self.icon_name))
            self.setIconSize(QSize(8, 8))
        else:
            self.setIcon(QIcon())

    def enterEvent(self, event):
        self._hovered = True
        self._update_style()
        super().enterEvent(event)

    def leaveEvent(self, event):
        self._hovered = False
        self._update_style()
        super().leaveEvent(event)


class DraggableResizableMixin:
    """Mixin for frameless, draggable, resizable windows. Requires QWidget base."""
    # Override in subclass to inset the painted area (for transparent borders)
    _paint_inset = 0

    def _paint_hitbox_rect(self, painter):
        """Paint nearly-invisible rect to catch mouse events in transparent areas.

        On macOS, WA_TranslucentBackground ignores setMask() for hit-testing.
        Workaround: paint a rect with alpha=1 (invisible but catches clicks).
        Call this FIRST in paintEvent before painting the visible content.
        """
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(QColor(0, 0, 0, 1))  # alpha=1: invisible but clickable
        painter.drawRect(self.rect())

    def _init_draggable(self):
        """Call this in __init__ after super().__init__."""
        self.drag_pos = None
        self.resize_edge = None
        self.resize_start_geo = None  # Geometry when resize started
        self.resize_start_pos = None  # Mouse position when resize started
        self.setMouseTracking(True)

    def _painted_rect(self):
        """Get the painted (non-transparent) area rect."""
        return self.rect().adjusted(self._paint_inset, self._paint_inset,
                                    -self._paint_inset, -self._paint_inset)

    def _edge_at(self, pos):
        """Check if position is on a resize edge (any edge or corner)."""
        r = self._painted_rect()
        if not r.contains(pos):
            return None
        edge = ""
        if pos.y() <= r.top() + RESIZE_MARGIN:
            edge += "t"
        if pos.y() >= r.bottom() - RESIZE_MARGIN:
            edge += "b"
        if pos.x() <= r.left() + RESIZE_MARGIN:
            edge += "l"
        if pos.x() >= r.right() - RESIZE_MARGIN:
            edge += "r"
        return edge or None

    def mousePressEvent(self, e):
        if e.button() == Qt.MouseButton.LeftButton:
            pos = e.position().toPoint()
            if not self._painted_rect().contains(pos):
                return
            self.resize_edge = self._edge_at(pos)
            if self.resize_edge:
                self.resize_start_geo = self.geometry()
                self.resize_start_pos = e.globalPosition().toPoint()
            else:
                self.drag_pos = e.globalPosition().toPoint() - self.frameGeometry().topLeft()

    def mouseMoveEvent(self, e):
        if e.buttons() & Qt.MouseButton.LeftButton:
            if self.resize_edge and self.resize_start_geo and self.resize_start_pos:
                gpos = e.globalPosition().toPoint()
                delta = gpos - self.resize_start_pos
                geo = QRect(self.resize_start_geo)  # Copy original geometry
                min_w, min_h = self.minimumWidth() or 100, self.minimumHeight() or 100
                if "t" in self.resize_edge:
                    new_top = self.resize_start_geo.top() + delta.y()
                    geo.setTop(min(new_top, self.resize_start_geo.bottom() - min_h))
                if "b" in self.resize_edge:
                    new_bottom = self.resize_start_geo.bottom() + delta.y()
                    geo.setBottom(max(new_bottom, self.resize_start_geo.top() + min_h))
                if "l" in self.resize_edge:
                    new_left = self.resize_start_geo.left() + delta.x()
                    geo.setLeft(min(new_left, self.resize_start_geo.right() - min_w))
                if "r" in self.resize_edge:
                    new_right = self.resize_start_geo.right() + delta.x()
                    geo.setRight(max(new_right, self.resize_start_geo.left() + min_w))
                self.setGeometry(geo)
            elif self.drag_pos:
                self.move(e.globalPosition().toPoint() - self.drag_pos)
        else:
            edge = self._edge_at(e.position().toPoint())
            if edge:
                cursors = {
                    "t": Qt.CursorShape.SizeVerCursor,
                    "b": Qt.CursorShape.SizeVerCursor,
                    "l": Qt.CursorShape.SizeHorCursor,
                    "r": Qt.CursorShape.SizeHorCursor,
                    "tl": Qt.CursorShape.SizeFDiagCursor,
                    "br": Qt.CursorShape.SizeFDiagCursor,
                    "tr": Qt.CursorShape.SizeBDiagCursor,
                    "bl": Qt.CursorShape.SizeBDiagCursor,
                }
                self.setCursor(cursors.get(edge, Qt.CursorShape.ArrowCursor))
            else:
                self.unsetCursor()

    def mouseReleaseEvent(self, e):
        self.drag_pos = self.resize_edge = None

    def paintEvent(self, e):
        """Paint with hitbox rect first, then content."""
        p = QPainter(self)
        self._paint_hitbox_rect(p)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)
        self._paint_content(p)

    def _paint_content(self, painter):
        """Override to paint window content. Default: paint_window with adjusted rect."""
        rect = self.rect().adjusted(2, 2, -2, -2)
        STYLE.paint_window(painter, rect, self.width(), self.height())


class DraggableDialog(DraggableResizableMixin, QDialog):
    """Base class for frameless, draggable, resizable dialogs."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self._init_draggable()
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.Dialog)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setStyleSheet("QToolTip { background: #333; color: white; border: 1px solid #555; border-radius: 4px; }")

    def center_on_parent(self):
        self.adjustSize()
        if self.parent():
            p = self.parent()
            self.move(p.x() + (p.width() - self.width()) // 2,
                      p.y() + (p.height() - self.height()) // 2)

    def keyPressEvent(self, e):
        if e.key() == Qt.Key.Key_Q and e.modifiers() == Qt.KeyboardModifier.ControlModifier:
            QApplication.quit()
        else:
            super().keyPressEvent(e)


class OptionsDialog(DraggableDialog):
    """Generic dialog for selecting from a list of options with keyboard shortcuts.

    Options format: [(key_letter, value, description), ...]
    If show_value_in_button=True, button shows "{key}  {value}" with desc as tooltip.
    Otherwise button shows "{key}  {desc}" with desc as tooltip.
    """

    def __init__(self, title, options, current_value=None, parent=None, show_value_in_button=False):
        super().__init__(parent)
        self.selected_value = None
        self._key_map = {}

        layout = QVBoxLayout(self)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(8)

        layout.addWidget(make_title(title))

        for key, value, desc in options:
            btn_text = f"{key}  {value}" if show_value_in_button else f"{key}  {desc}"
            btn = QPushButton(btn_text)
            btn.setStyleSheet(get_btn_css())
            btn.setToolTip(desc)
            if value == current_value:
                btn.setStyleSheet(get_btn_css() + f"QPushButton {{ border: 2px solid {CYAN_CSS}; }}")
            btn.clicked.connect(lambda checked, v=value: self._select(v))
            layout.addWidget(btn)
            self._key_map[getattr(Qt.Key, f"Key_{key.upper()}")] = value

        layout.addWidget(make_close_btn("Esc  Cancel", self.reject))
        self.setMinimumWidth(250)

    def _select(self, value):
        self.selected_value = value
        self.accept()

    def keyPressEvent(self, e):
        key = e.key()
        if key in self._key_map:
            self._select(self._key_map[key])
        elif key == Qt.Key.Key_Escape:
            self.reject()
        else:
            super().keyPressEvent(e)


class HelpDialog(DraggableDialog):
    """Help dialog with about info and keymap."""

    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(10)

        layout.addWidget(make_title(APP_NAME, 18))

        # Main content: About | Keymap
        content = QHBoxLayout()
        content.setSpacing(15)

        # Left side: About
        about_box = QVBoxLayout()
        about_box.addWidget(make_section("About"))

        about_text = QLabel(
            "Voice transcription powered by Whisper.\n\n"
            "• Double-tap ⌥ to record from anywhere (works in fullscreen apps and terminals!)\n"
            "• Double-tap ⌥ again to stop and auto-paste the transcription via ⌘V\n"
            f"• Double-tap ⌥ and hold 2nd tap {CANCEL_HOLD_SECONDS}s+ to cancel (no paste)\n"
            "• ⌘ + double-tap ⌥ to toggle focus\n"
            "• Access from menu bar (top right of Mac)\n"
            "• Drag & drop audio files to transcribe\n"
            "• ⌘Q to quit\n\n"
            f"Wake word (J): Say the wake word to start recording hands-free! "
            f"Say it again to stop recording.\n\n"
            "Tmux mode (U): Paste directly into your active tmux pane instead of ⌘V.\n\n"
            "100% keyboard-driven - no mouse needed! (hover buttons to see shortcuts)\n\n"
            "Small mode (E or green button): Compact view with just status and timer - "
            "great for keeping visible while using keyboard shortcuts.\n\n"
            "Anti-Ramble mode (R): Post-process transcriptions with an LLM to clean up rambling. "
            f"Say \"{APP_NAME}, ...\" in your recording to give formatting instructions.\n\n"
            "Transcriptions tab: Click a row or its copy button to copy. "
            "Use the pen button to de-ramble a transcription after the fact.\n\n"
            "By Clara Burgert"
        )
        about_text.setStyleSheet(body_style(10))
        about_text.setWordWrap(True)
        about_text.setFixedWidth(190)
        about_box.addWidget(about_text)
        about_box.addStretch()

        # Debug button - prints imported modules to terminal
        debug_btn = QPushButton()
        debug_btn.setIcon(load_icon("bug", color=ICON_COLOR_DARK))
        debug_btn.setStyleSheet(get_btn_css())
        debug_btn.setFixedWidth(30)
        debug_btn.clicked.connect(self._print_modules)
        about_box.addWidget(debug_btn)

        # GitHub button
        github_btn = QPushButton("GitHub")
        github_btn.setStyleSheet(get_btn_css())
        github_btn.clicked.connect(lambda: rp.open_file_with_default_application(GITHUB_URL))
        about_box.addWidget(github_btn)

        content.addLayout(about_box)

        # Separator
        sep = QLabel()
        sep.setFixedWidth(1)
        sep.setStyleSheet(f"background: {BORDER_COLOR};")
        content.addWidget(sep)

        # Right side: Keymap
        keymap_box = QVBoxLayout()
        keymap_box.addWidget(make_section("Keymap"))

        for action_id, key, icon_name, desc, menu_text in ACTIONS:
            row = QHBoxLayout()
            row.setSpacing(4)
            btn = QPushButton(key)
            if icon_name:
                btn.setIcon(load_icon(icon_name, color=ICON_COLOR_DARK))
                btn.setIconSize(QSize(14, 14))
            btn.setStyleSheet(get_btn_css())
            btn.setFixedWidth(60)
            btn.setEnabled(False)
            row.addWidget(btn)
            lbl = QLabel(desc)
            lbl.setStyleSheet(body_style(9))
            row.addWidget(lbl, 1)
            keymap_box.addLayout(row)

        for key, name, description in TABS:
            row = QHBoxLayout()
            row.setSpacing(4)
            btn = QPushButton(f"{key}")
            btn.setStyleSheet(get_btn_css())
            btn.setFixedWidth(60)
            btn.setEnabled(False)
            row.addWidget(btn)
            lbl = QLabel(f"{name} tab")
            lbl.setStyleSheet(body_style(9))
            row.addWidget(lbl, 1)
            keymap_box.addLayout(row)

        keymap_box.addStretch()
        content.addLayout(keymap_box)

        layout.addLayout(content)

        layout.addWidget(make_close_btn(on_click=self.accept))

        self.setMinimumWidth(480)  # Width only, height auto-sizes

    def _print_modules(self):
        """Print all imported modules and their paths as JSON."""
        import json
        modules = {
            name: getattr(mod, '__file__', None)
            for name, mod in sorted(sys.modules.items())
            if mod is not None
        }
        print(json.dumps(modules, indent=2))

    def keyPressEvent(self, e):
        if e.key() in (Qt.Key.Key_Escape, Qt.Key.Key_Question, Qt.Key.Key_Return, Qt.Key.Key_Enter):
            self.accept()
        else:
            super().keyPressEvent(e)


class ModelDialog(OptionsDialog):
    """Dialog to select Whisper model with keyboard shortcuts."""

    def __init__(self, current_model, parent=None):
        super().__init__("Select Whisper Model", WHISPER_MODELS, current_model, parent, show_value_in_button=True)

    @property
    def selected_model(self):
        return self.selected_value

    @selected_model.setter
    def selected_model(self, value):
        self.selected_value = value


# AI coder process names - panes running these get a star
AI_CODER_PROCESSES = ['claude', 'opencode', 'gemini', 'aider', 'cursor']

# Scrollback cache with 30 second TTL
try:
    from cachetools import TTLCache, cached
    _scrollback_cache = TTLCache(maxsize=100, ttl=30)
except ImportError:
    _scrollback_cache = {}  # Fallback to simple dict (no expiry)


def _get_tmux_scrollback(target, lines=50):
    """Get scrollback from tmux pane with caching."""
    # Check cache first
    if target in _scrollback_cache:
        return _scrollback_cache[target]

    try:
        result = subprocess.run(
            ['tmux', 'capture-pane', '-t', target, '-p', '-S', f'-{lines}'],
            capture_output=True, text=True, timeout=2
        )
        if result.returncode == 0:
            text = result.stdout
            _scrollback_cache[target] = text
            return text
        return None
    except (subprocess.TimeoutExpired, FileNotFoundError):
        return None


class TmuxSelectionDialog(DraggableDialog):
    """Dialog to select tmux pane target with flat table and voice routing."""

    # Column indices
    COL_ADDRESS = 0
    COL_PANE_ID = 1
    COL_PROCESS = 2
    COL_PHRASE = 3  # Single magic phrase column

    def __init__(self, current_target='%', parent=None):
        super().__init__(parent)
        self.selected_target = current_target
        self._hover_pane_id = None
        self._selected_pane_id = None
        self._pane_data = []  # List of {address, pane_id, process, target}
        self._orig_tmux_mode = S.TMUX_MODE  # Store original for cancel

        layout = QVBoxLayout(self)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(8)

        layout.addWidget(make_title("Tmux Pane Manager"))

        # Main content: table on left, preview on right
        splitter = QSplitter(Qt.Orientation.Horizontal)

        # Table widget
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["Address", "Pane ID", "Process", "Magic Phrase"])
        self.table.setStyleSheet(
            f"QTableWidget {{ {PANEL_BG_FLAT_CSS} color: {TEXT_PRIMARY}; "
            f"border: 1px solid {BORDER_COLOR}; font-family: Menlo, monospace; font-size: 11px; }}"
            f"QTableWidget::item {{ padding: 1px 4px; }}"
            f"QTableWidget::item:hover {{ background: rgba(180,210,240,0.5); }}"
            f"QTableWidget::item:selected {{ background: rgba(180,210,240,0.7); color: black; }}"
            f"QHeaderView::section {{ background: #e0e0e0; color: black; padding: 2px 4px; "
            f"border: 1px solid #ccc; font-weight: bold; }}"
            + SCROLLBAR_CSS
        )
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.verticalHeader().setVisible(False)
        self.table.verticalHeader().setDefaultSectionSize(22)  # Compact rows
        self.table.setMouseTracking(True)
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)  # We handle edit manually
        self.table.cellClicked.connect(self._on_cell_clicked)
        self.table.cellChanged.connect(self._on_cell_changed)
        self.table.itemSelectionChanged.connect(self._on_selection_changed)
        self.table.viewport().installEventFilter(self)  # For hover preview
        splitter.addWidget(self.table)

        # Right side: preview
        preview_container = QWidget()
        preview_layout = QVBoxLayout(preview_container)
        preview_layout.setContentsMargins(0, 0, 0, 0)
        preview_layout.setSpacing(2)

        self.preview_label = QLabel("")
        self.preview_label.setStyleSheet(f"color: {TEXT_SECONDARY}; font-size: 10px; font-family: Menlo, monospace;")
        preview_layout.addWidget(self.preview_label)

        self.preview = QTextEdit()
        self.preview.setReadOnly(True)
        self.preview.setStyleSheet(
            f"QTextEdit {{ background: #1a1a1a; color: #cccccc; "
            f"border: 1px solid {BORDER_COLOR}; font-family: Menlo, monospace; "
            f"font-size: 10px; padding: 4px; }}"
            + SCROLLBAR_CSS
        )
        self.preview.setLineWrapMode(QTextEdit.LineWrapMode.NoWrap)
        self.preview.setMinimumWidth(280)
        preview_layout.addWidget(self.preview, 1)

        splitter.addWidget(preview_container)
        splitter.setSizes([420, 280])
        layout.addWidget(splitter, 1)

        # Not running message
        self.not_running_label = QLabel("tmux is not running")
        self.not_running_label.setStyleSheet(f"color: {TEXT_SECONDARY}; font-size: 14px; padding: 20px;")
        self.not_running_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.not_running_label.hide()
        layout.addWidget(self.not_running_label)

        # Buttons
        btn_row = QHBoxLayout()
        btn_row.setSpacing(8)

        # Enable tmux mode checkbox
        self.enable_checkbox = QCheckBox("Enable tmux mode")
        self.enable_checkbox.setChecked(S.TMUX_MODE)
        self.enable_checkbox.setStyleSheet(get_checkbox_css())
        set_tooltip(self.enable_checkbox,
            "Enable or disable tmux voice routing.\n\n"
            "When enabled, transcriptions containing magic phrases\n"
            "will be sent directly to the matching tmux panes."
        )
        btn_row.addWidget(self.enable_checkbox)

        btn_row.addStretch()
        cancel_btn = QPushButton("Esc  Cancel")
        cancel_btn.setStyleSheet(get_btn_css())
        cancel_btn.clicked.connect(self.reject)
        btn_row.addWidget(cancel_btn)
        ok_btn = QPushButton("Enter  Save")
        ok_btn.setStyleSheet(get_btn_css())
        ok_btn.clicked.connect(self._accept_selection)
        btn_row.addWidget(ok_btn)
        layout.addLayout(btn_row)

        self.setMinimumSize(700, 400)
        self._refresh_table()

    def _get_tmux_panes_flat(self):
        """Get flat list of all tmux panes."""
        try:
            result = subprocess.run(
                ['tmux', 'list-panes', '-a', '-F',
                 '#{session_name}\t#{window_index}\t#{window_name}\t#{pane_index}\t#{pane_current_command}\t#{pane_id}'],
                capture_output=True, text=True, timeout=2
            )
            if result.returncode != 0:
                return None
            panes = []
            for line in result.stdout.strip().split('\n'):
                if not line:
                    continue
                parts = line.split('\t')
                if len(parts) < 6:
                    continue
                session, win_idx, win_name, pane_idx, cmd, pane_id = parts
                address = f"{session}:{win_name}:{pane_idx}"
                target = f"{session}:{win_idx}.{pane_idx}"
                is_ai = any(ai in cmd.lower() for ai in AI_CODER_PROCESSES)
                panes.append({
                    'address': address,
                    'pane_id': pane_id,
                    'process': cmd + (" ⭐" if is_ai else ""),
                    'target': target,
                })
            return panes
        except (subprocess.TimeoutExpired, FileNotFoundError):
            return None

    def _refresh_table(self):
        """Populate table with tmux panes."""
        self.table.blockSignals(True)
        self.table.setRowCount(0)
        self._pane_data = self._get_tmux_panes_flat()

        if self._pane_data is None:
            self.table.hide()
            self.preview.hide()
            self.preview_label.hide()
            self.not_running_label.show()
            self.table.blockSignals(False)
            return

        self.not_running_label.hide()
        self.table.show()
        self.preview.show()
        self.preview_label.show()

        self.table.setRowCount(len(self._pane_data))
        for row, pane in enumerate(self._pane_data):
            pane_id = pane['pane_id']
            saved = S.TMUX_PANE_NAMES.get(pane_id, {})

            # Address (read-only)
            addr_item = QTableWidgetItem(pane['address'])
            addr_item.setFlags(addr_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
            addr_item.setData(Qt.ItemDataRole.UserRole, pane_id)
            self.table.setItem(row, self.COL_ADDRESS, addr_item)

            # Pane ID (read-only)
            id_item = QTableWidgetItem(pane_id)
            id_item.setFlags(id_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
            self.table.setItem(row, self.COL_PANE_ID, id_item)

            # Process (read-only)
            proc_item = QTableWidgetItem(pane['process'])
            proc_item.setFlags(proc_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
            self.table.setItem(row, self.COL_PROCESS, proc_item)

            # Magic Phrase (editable) - single phrase per pane
            phrase = saved.get('phrase', '')
            phrase_item = QTableWidgetItem(phrase)
            self.table.setItem(row, self.COL_PHRASE, phrase_item)

        self.table.resizeColumnsToContents()
        self.table.setColumnWidth(self.COL_PHRASE, 120)
        self.table.blockSignals(False)

        # Select first row by default
        if self._pane_data:
            self.table.selectRow(0)
            self._selected_pane_id = self._pane_data[0]['pane_id']
            self._update_preview(self._selected_pane_id)

    def _on_cell_clicked(self, row, col):
        """Single-click on Magic Phrase column starts editing."""
        if row >= len(self._pane_data):
            return
        pane_id = self._pane_data[row]['pane_id']
        self._selected_pane_id = pane_id
        # Update preview to selected row (not hover)
        if self._hover_pane_id is None:
            self._update_preview(pane_id)
        # Single-click on phrase column = start editing
        if col == self.COL_PHRASE:
            self.table.editItem(self.table.item(row, col))

    def _on_selection_changed(self):
        """Update selected pane when selection changes."""
        rows = self.table.selectionModel().selectedRows()
        if rows and rows[0].row() < len(self._pane_data):
            pane_id = self._pane_data[rows[0].row()]['pane_id']
            self._selected_pane_id = pane_id
            # Update preview if not hovering
            if self._hover_pane_id is None:
                self._update_preview(pane_id)

    def _on_cell_changed(self, row, col):
        """Save phrase when cell changes."""
        if row >= len(self._pane_data) or col != self.COL_PHRASE:
            return
        pane_id = self._pane_data[row]['pane_id']
        phrase = self.table.item(row, col).text().strip()
        if phrase:
            S.TMUX_PANE_NAMES[pane_id] = {'phrase': phrase}
        elif pane_id in S.TMUX_PANE_NAMES:
            del S.TMUX_PANE_NAMES[pane_id]

    def eventFilter(self, obj, event):
        """Handle mouse hover for preview."""
        from PyQt6.QtCore import QEvent
        if obj == self.table.viewport():
            if event.type() == QEvent.Type.MouseMove:
                pos = event.position().toPoint()
                row = self.table.rowAt(pos.y())
                col = self.table.columnAt(pos.x())
                # Update cursor for phrase column
                if col == self.COL_PHRASE and row >= 0:
                    self.table.viewport().setCursor(Qt.CursorShape.IBeamCursor)
                else:
                    self.table.viewport().setCursor(Qt.CursorShape.ArrowCursor)
                # Hover preview
                if row >= 0 and row < len(self._pane_data):
                    pane_id = self._pane_data[row]['pane_id']
                    if pane_id != self._hover_pane_id:
                        self._hover_pane_id = pane_id
                        self._update_preview(pane_id)
                else:
                    self._hover_pane_id = None
            elif event.type() == QEvent.Type.Leave:
                self._hover_pane_id = None
                self.table.viewport().setCursor(Qt.CursorShape.ArrowCursor)
                # Revert to selected row preview
                if self._selected_pane_id:
                    self._update_preview(self._selected_pane_id)
        return super().eventFilter(obj, event)

    def _update_preview(self, pane_id):
        """Update preview panel with scrollback from pane."""
        self.preview_label.setText(f"Preview: {pane_id}")
        text = _get_tmux_scrollback(pane_id)
        if text is not None:
            self.preview.setPlainText(text)
            sb = self.preview.verticalScrollBar()
            sb.setValue(sb.maximum())
        else:
            self.preview.setPlainText(f"(cannot preview {pane_id})")

    def _accept_selection(self):
        """Accept and save."""
        # Apply tmux mode from checkbox
        S.set('TMUX_MODE', self.enable_checkbox.isChecked())
        # Clean up stale pane_ids from TMUX_PANE_NAMES
        if self._pane_data:
            live_ids = {p['pane_id'] for p in self._pane_data}
            stale = [pid for pid in S.TMUX_PANE_NAMES if pid not in live_ids]
            for pid in stale:
                del S.TMUX_PANE_NAMES[pid]
        # Set selected as target
        if self._selected_pane_id:
            self.selected_target = self._selected_pane_id
        self.accept()

    def reject(self):
        """Revert tmux mode on cancel."""
        S.set('TMUX_MODE', self._orig_tmux_mode)
        super().reject()

    def keyPressEvent(self, e):
        if e.key() == Qt.Key.Key_Escape:
            self.reject()
        elif e.key() in (Qt.Key.Key_Return, Qt.Key.Key_Enter):
            if self.table.state() != QTableWidget.State.EditingState:
                self._accept_selection()
        else:
            super().keyPressEvent(e)


class TextEditDialog(DraggableDialog):
    """Base class for resizable text edit dialogs."""

    def __init__(self, title, current_text, default_text=None, info_text=None, parent=None):
        super().__init__(parent)
        self._default_text = default_text

        layout = QVBoxLayout(self)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(10)

        layout.addWidget(make_title(title))

        if info_text:
            info = QLabel(info_text)
            info.setStyleSheet(body_style(10))
            layout.addWidget(info)

        # Text edit (resizable with dialog)
        self._text_edit = QTextEdit()
        self._text_edit.setPlainText(current_text)
        self._text_edit.setStyleSheet(get_textedit_css())
        self._text_edit.setMinimumHeight(150)
        layout.addWidget(self._text_edit, 1)  # stretch=1 so it resizes

        # Buttons
        btn_row = QHBoxLayout()
        btn_row.setSpacing(8)

        if default_text is not None:
            revert_btn = QPushButton("Revert to Default")
            revert_btn.setStyleSheet(get_btn_css())
            revert_btn.clicked.connect(self._revert_default)
            btn_row.addWidget(revert_btn)

        btn_row.addStretch()

        cancel_btn = QPushButton("Cancel")
        cancel_btn.setStyleSheet(get_btn_css())
        cancel_btn.clicked.connect(self.reject)
        btn_row.addWidget(cancel_btn)

        save_btn = QPushButton("Save")
        save_btn.setStyleSheet(get_btn_css())
        save_btn.clicked.connect(self.accept)
        btn_row.addWidget(save_btn)

        layout.addLayout(btn_row)
        self.setMinimumSize(500, 300)

    def _revert_default(self):
        if self._default_text is not None:
            self._text_edit.setPlainText(self._default_text)

    def get_text(self):
        return self._text_edit.toPlainText()

    def keyPressEvent(self, e):
        if e.key() == Qt.Key.Key_Escape:
            self.reject()
        else:
            super().keyPressEvent(e)


class TTSInstructionDialog(DraggableDialog):
    """Dialog to edit the TTS instruction template."""

    DEFAULT_TEMPLATE = "Please speak back with ({command} &)"

    def __init__(self, current_text, parent=None):
        super().__init__(parent)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(10)

        layout.addWidget(make_title("Edit TTS Instruction"))

        # Info label
        info = QLabel("Template variable: {command}")
        info.setStyleSheet(body_style(10))
        layout.addWidget(info)

        # Text edit
        self._text_edit = QTextEdit()
        self._text_edit.setPlainText(current_text)
        self._text_edit.setStyleSheet(get_textedit_css())
        self._text_edit.setMinimumHeight(80)
        layout.addWidget(self._text_edit)

        # Command preview label
        cmd_label = QLabel("{command} =")
        cmd_label.setStyleSheet(body_style(10))
        layout.addWidget(cmd_label)

        # Command preview (non-editable, gray, monospace)
        self._cmd_preview = QTextEdit()
        self._cmd_preview.setReadOnly(True)
        self._cmd_preview.setPlainText(build_tts_command())
        self._cmd_preview.setStyleSheet(
            f"QTextEdit {{ background-color: #2a2a2a; color: #888888; "
            f"border: 1px solid {BORDER_COLOR}; font-family: Menlo, monospace; "
            f"font-size: 10px; padding: 6px; }}" + SCROLLBAR_CSS
        )
        self._cmd_preview.setMinimumHeight(60)
        self._cmd_preview.setMaximumHeight(80)
        layout.addWidget(self._cmd_preview)

        # Buttons
        btn_row = QHBoxLayout()
        btn_row.setSpacing(8)

        revert_btn = QPushButton("Revert to Default")
        revert_btn.setStyleSheet(get_btn_css())
        revert_btn.clicked.connect(self._revert_default)
        btn_row.addWidget(revert_btn)

        btn_row.addStretch()

        cancel_btn = QPushButton("Cancel")
        cancel_btn.setStyleSheet(get_btn_css())
        cancel_btn.clicked.connect(self.reject)
        btn_row.addWidget(cancel_btn)

        save_btn = QPushButton("Save")
        save_btn.setStyleSheet(get_btn_css())
        save_btn.clicked.connect(self.accept)
        btn_row.addWidget(save_btn)

        layout.addLayout(btn_row)
        self.setMinimumWidth(500)

    def _revert_default(self):
        self._text_edit.setPlainText(self.DEFAULT_TEMPLATE)

    def get_text(self):
        return self._text_edit.toPlainText()

    def keyPressEvent(self, e):
        if e.key() == Qt.Key.Key_Escape:
            self.reject()
        else:
            super().keyPressEvent(e)


def _get_macos_voices():
    """Get list of available macOS voices."""
    import subprocess
    result = subprocess.run(['say', '-v', '?'], capture_output=True, text=True)
    voices = []
    for line in result.stdout.strip().split('\n'):
        if line:
            # Format: "VoiceName  lang  # description"
            parts = line.split()
            if parts:
                voices.append(parts[0])
    return sorted(set(voices))  # Dedupe and sort

MACOS_VOICES = None  # Lazy-loaded

class TTSSettingsWidget(QWidget):
    """TTS settings with per-backend configuration. Hides unsupported controls."""

    # Backend options
    BACKENDS = [
        ('say', 'macOS Say'),
        ('supertonic', 'Supertonic'),
        ('kitten', 'Kitten TTS'),
    ]

    # Supertonic voice options
    SUPERTONIC_VOICES = [
        ('F1', 'Female 1'), ('F2', 'Female 2'), ('F3', 'Female 3'),
        ('F4', 'Female 4'), ('F5', 'Female 5'),
        ('M1', 'Male 1'), ('M2', 'Male 2'), ('M3', 'Male 3'),
        ('M4', 'Male 4'), ('M5', 'Male 5'),
    ]

    # Kitten voice options
    KITTEN_VOICES = [
        ('expr-voice-2-f', 'Voice 2 Female'), ('expr-voice-2-m', 'Voice 2 Male'),
        ('expr-voice-3-f', 'Voice 3 Female'), ('expr-voice-3-m', 'Voice 3 Male'),
        ('expr-voice-4-f', 'Voice 4 Female'), ('expr-voice-4-m', 'Voice 4 Male'),
        ('expr-voice-5-f', 'Voice 5 Female'), ('expr-voice-5-m', 'Voice 5 Male'),
    ]

    def __init__(self, parent=None):
        super().__init__(parent)
        self._layout = QVBoxLayout(self)
        self._layout.setContentsMargins(0, 0, 0, 0)
        self._layout.setSpacing(4)
        self._build_ui()

    def _build_ui(self):
        self._layout.addWidget(make_section("Text-to-Speech"))

        # Backend selector (macOS Say / Supertonic / Kitten)
        backend_row = QHBoxLayout()
        backend_row.setSpacing(8)
        backend_label = QLabel("Engine:")
        backend_label.setStyleSheet(get_pref_label_css())
        set_tooltip(backend_label, "TTS engine:\n\nmacOS Say = Built-in system voices\nSupertonic = Fast neural TTS (66M params)\nKitten = Lightweight neural TTS (25MB)")
        backend_row.addWidget(backend_label)
        self._backend_combo = QComboBox()
        self._backend_combo.setStyleSheet(get_combobox_css())
        for value, label in self.BACKENDS:
            self._backend_combo.addItem(label, value)
        idx = [b for b, _ in self.BACKENDS].index(S.SPEAK_BACK_VOICE) if S.SPEAK_BACK_VOICE in [b for b, _ in self.BACKENDS] else 0
        self._backend_combo.setCurrentIndex(idx)
        self._backend_combo.currentIndexChanged.connect(self._on_backend_changed)
        backend_row.addWidget(self._backend_combo, 1)
        self._layout.addLayout(backend_row)

        # Voice selector row (content changes per backend)
        self._voice_row = QHBoxLayout()
        self._voice_row.setSpacing(8)
        self._voice_label = QLabel("Voice:")
        self._voice_label.setStyleSheet(get_pref_label_css())
        self._voice_row.addWidget(self._voice_label)
        self._voice_combo = QComboBox()
        self._voice_combo.setStyleSheet(get_combobox_css())
        self._voice_combo.currentIndexChanged.connect(self._on_voice_changed)
        self._voice_row.addWidget(self._voice_combo, 1)
        self._layout.addLayout(self._voice_row)

        # Speed slider (all backends, but different ranges)
        self._speed_row, self._speed_label, self._speed_slider, self._speed_value = make_slider_row(
            "Speed:", "Speech speed", 5, 20, 10, lambda v: f"{v/10:.1f}x",
            self._on_speed_changed, self._on_speed_released
        )
        self._layout.addLayout(self._speed_row)

        # Volume slider (supertonic only) - store widgets for show/hide
        self._vol_row, self._vol_label, self._vol_slider, self._vol_value = make_slider_row(
            "Volume:", "TTS volume (0.0 mute - 2.0 loud)", 0, 20, 10,
            lambda v: f"{v/10:.1f}", self._on_volume_changed, self._on_volume_released
        )
        self._vol_widget = QWidget()
        vol_layout = QHBoxLayout(self._vol_widget)
        vol_layout.setContentsMargins(0, 0, 0, 0)
        vol_layout.setSpacing(8)
        vol_layout.addWidget(self._vol_label)
        vol_layout.addWidget(self._vol_slider, 1)
        vol_layout.addWidget(self._vol_value)
        self._layout.addWidget(self._vol_widget)

        # Quality slider (supertonic only)
        self._qual_row, self._qual_label, self._qual_slider, self._qual_value = make_slider_row(
            "Quality:", "Synthesis quality (1=fast, 10=high)", 1, 10, 5,
            lambda v: str(v), self._on_quality_changed, self._on_quality_released
        )
        self._qual_widget = QWidget()
        qual_layout = QHBoxLayout(self._qual_widget)
        qual_layout.setContentsMargins(0, 0, 0, 0)
        qual_layout.setSpacing(8)
        qual_layout.addWidget(self._qual_label)
        qual_layout.addWidget(self._qual_slider, 1)
        qual_layout.addWidget(self._qual_value)
        self._layout.addWidget(self._qual_widget)

        # Initialize UI for current backend
        self._update_for_backend()

        # Append instruction checkbox + edit button
        append_row = QHBoxLayout()
        append_row.setSpacing(8)
        self._append_checkbox = QCheckBox("Append TTS instruction")
        self._append_checkbox.setChecked(S.SPEAK_BACK_APPEND_INSTRUCTION)
        self._append_checkbox.setStyleSheet(get_checkbox_css())
        self._append_checkbox.setToolTip("Appends TTS command to transcriptions for Claude to speak.")
        self._append_checkbox.stateChanged.connect(self._on_append_changed)
        append_row.addWidget(self._append_checkbox)
        self._edit_btn = make_edit_button("Edit the instruction template", self._edit_instruction)
        append_row.addWidget(self._edit_btn)
        self._copy_btn = QPushButton()
        self._copy_btn.setIcon(load_icon("copy", color=ICON_COLOR_DARK))
        self._copy_btn.setFixedWidth(28)
        self._copy_btn.setStyleSheet(get_btn_css().replace("padding: 3px 8px;", "padding: 1px 4px;"))
        self._copy_btn.setToolTip("Copy TTS instruction to clipboard")
        self._copy_btn.clicked.connect(self._copy_tts_instruction)
        append_row.addWidget(self._copy_btn)
        append_row.addStretch()
        self._layout.addLayout(append_row)

        # Only for tmux checkbox (indented)
        tmux_only_row = QHBoxLayout()
        tmux_only_row.setSpacing(8)
        tmux_only_row.addSpacing(20)
        self._tmux_only_checkbox = QCheckBox("Only for tmux")
        self._tmux_only_checkbox.setChecked(S.SPEAK_BACK_TMUX_ONLY)
        self._tmux_only_checkbox.setStyleSheet(get_checkbox_css())
        self._tmux_only_checkbox.setToolTip("Only append when sending to tmux panes.")
        self._tmux_only_checkbox.setEnabled(S.SPEAK_BACK_APPEND_INSTRUCTION)
        self._tmux_only_checkbox.stateChanged.connect(self._on_tmux_only_changed)
        tmux_only_row.addWidget(self._tmux_only_checkbox)
        tmux_only_row.addStretch()
        self._layout.addLayout(tmux_only_row)

        # Announce pane checkbox
        announce_row = QHBoxLayout()
        announce_row.setSpacing(8)
        self._announce_checkbox = QCheckBox("Announce tmux pane")
        self._announce_checkbox.setChecked(S.TMUX_ANNOUNCE_PANE)
        self._announce_checkbox.setStyleSheet(get_checkbox_css())
        set_tooltip(self._announce_checkbox, "Speak which pane(s) received the message.")
        self._announce_checkbox.stateChanged.connect(self._on_announce_changed)
        announce_row.addWidget(self._announce_checkbox)
        announce_row.addStretch()
        self._layout.addLayout(announce_row)

    def _get_backend(self):
        return self._backend_combo.currentData()

    def _get_cfg(self):
        """Get current backend's config dict."""
        backend = self._get_backend()
        if backend == 'say':
            return S.TTS_SAY
        elif backend == 'supertonic':
            return S.TTS_SUPERTONIC
        else:
            return S.TTS_KITTEN

    def _save_cfg(self, key, value):
        """Save a value to current backend's config."""
        cfg = self._get_cfg()
        cfg[key] = value
        # Trigger settings save
        backend = self._get_backend()
        if backend == 'say':
            S.set('TTS_SAY', cfg)
        elif backend == 'supertonic':
            S.set('TTS_SUPERTONIC', cfg)
        else:
            S.set('TTS_KITTEN', cfg)

    def _update_for_backend(self):
        """Update UI controls for current backend."""
        global MACOS_VOICES
        backend = self._get_backend()
        cfg = self._get_cfg()

        # Populate voice dropdown
        self._voice_combo.blockSignals(True)
        self._voice_combo.clear()
        if backend == 'say':
            if MACOS_VOICES is None:
                MACOS_VOICES = _get_macos_voices()
            # Add "Default" as first option (uses system default voice)
            self._voice_combo.addItem("Default (System)", "")
            for v in MACOS_VOICES:
                self._voice_combo.addItem(v, v)
            current = cfg.get('voice', '')
            if current == '' or current not in MACOS_VOICES:
                idx = 0  # Default
            else:
                idx = MACOS_VOICES.index(current) + 1  # +1 for Default option
            self._voice_combo.setCurrentIndex(idx)
            make_combobox_searchable(self._voice_combo)
        elif backend == 'supertonic':
            for value, label in self.SUPERTONIC_VOICES:
                self._voice_combo.addItem(label, value)
            current = cfg.get('voice', 'F1')
            idx = [v for v, _ in self.SUPERTONIC_VOICES].index(current) if current in [v for v, _ in self.SUPERTONIC_VOICES] else 0
            self._voice_combo.setCurrentIndex(idx)
        else:  # kitten
            for value, label in self.KITTEN_VOICES:
                self._voice_combo.addItem(label, value)
            current = cfg.get('voice', 'expr-voice-3-f')
            idx = [v for v, _ in self.KITTEN_VOICES].index(current) if current in [v for v, _ in self.KITTEN_VOICES] else 0
            self._voice_combo.setCurrentIndex(idx)
        self._voice_combo.blockSignals(False)

        # Update speed slider
        speed = cfg.get('speed', 175 if backend == 'say' else 1.0)
        if backend == 'say':
            self._speed_slider.setRange(90, 400)
            self._speed_slider.setValue(int(speed))
            self._speed_value.setText(f"{int(speed)} WPM")
            set_tooltip(self._speed_label, "Speech rate in words per minute (90-400)")
        else:
            min_spd = 5 if backend == 'kitten' else 7
            self._speed_slider.setRange(min_spd, 20)
            self._speed_slider.setValue(int(speed * 10))
            self._speed_value.setText(f"{speed:.1f}x")
            set_tooltip(self._speed_label, "Speech speed multiplier")

        # Show/hide volume and quality (supertonic only)
        is_supertonic = (backend == 'supertonic')
        self._vol_widget.setVisible(is_supertonic)
        self._qual_widget.setVisible(is_supertonic)
        if is_supertonic:
            self._vol_slider.setValue(int(cfg.get('volume', 1.0) * 10))
            self._vol_value.setText(f"{cfg.get('volume', 1.0):.1f}")
            self._qual_slider.setValue(cfg.get('steps', 5))
            self._qual_value.setText(str(cfg.get('steps', 5)))

    def _speak_demo(self, text):
        do_tts(text, block=False)

    # ─────────────────────────────────────────────────────────────────────────
    # Handlers
    # ─────────────────────────────────────────────────────────────────────────

    def _on_backend_changed(self, index):
        backend = self._backend_combo.itemData(index)
        S.set('SPEAK_BACK_VOICE', backend)
        self._update_for_backend()
        self._speak_demo(f"{self._backend_combo.currentText()} engine")

    def _on_voice_changed(self, index):
        if index < 0:
            return
        voice = self._voice_combo.itemData(index)
        display_text = self._voice_combo.currentText()
        self._save_cfg('voice', voice)
        self._speak_demo(display_text)

    def _on_speed_changed(self, value):
        backend = self._get_backend()
        if backend == 'say':
            self._save_cfg('speed', value)
            self._speed_value.setText(f"{value} WPM")
        else:
            self._save_cfg('speed', value / 10.0)
            self._speed_value.setText(f"{value/10:.1f}x")

    def _on_speed_released(self):
        backend = self._get_backend()
        cfg = self._get_cfg()
        speed = cfg.get('speed', 175 if backend == 'say' else 1.0)
        if backend == 'say':
            self._speak_demo(f"{int(speed)} words per minute")
        else:
            self._speak_demo(f"{speed:.1f}x speed")

    def _on_volume_changed(self, value):
        self._save_cfg('volume', value / 10.0)
        self._vol_value.setText(f"{value/10:.1f}")

    def _on_volume_released(self):
        self._speak_demo("Volume test")

    def _on_quality_changed(self, value):
        self._save_cfg('steps', value)
        self._qual_value.setText(str(value))

    def _on_quality_released(self):
        self._speak_demo("Quality test")

    def _on_append_changed(self, state):
        enabled = state == Qt.CheckState.Checked.value
        S.set('SPEAK_BACK_APPEND_INSTRUCTION', enabled)
        self._tmux_only_checkbox.setEnabled(enabled)

    def _on_tmux_only_changed(self, state):
        S.set('SPEAK_BACK_TMUX_ONLY', state == Qt.CheckState.Checked.value)

    def _on_announce_changed(self, state):
        S.set('TMUX_ANNOUNCE_PANE', state == Qt.CheckState.Checked.value)

    def _edit_instruction(self):
        dialog = TTSInstructionDialog(S.SPEAK_BACK_INSTRUCTION_TEMPLATE, self.window())
        dialog.center_on_parent()
        if dialog.exec():
            S.set('SPEAK_BACK_INSTRUCTION_TEMPLATE', dialog.get_text())

    def _copy_tts_instruction(self):
        instruction = S.SPEAK_BACK_INSTRUCTION_TEMPLATE.format(command=build_tts_command())
        QApplication.clipboard().setText(instruction)
        play_chime('copy')


class WakeWordSettingsWidget(QWidget):
    """Wake word settings with per-engine configuration."""

    # Engine changed signal (for parent to respond)
    engine_changed = pyqtSignal(str)
    settings_changed = pyqtSignal()  # Generic signal when any setting changes

    # Engine options
    ENGINES = [
        ('openwakeword', 'OpenWakeWord'),
        ('macos', 'macOS Native'),
    ]

    def __init__(self, parent=None):
        super().__init__(parent)
        self._layout = QVBoxLayout(self)
        self._layout.setContentsMargins(0, 0, 0, 0)
        self._layout.setSpacing(4)
        self._build_ui()

    def _build_ui(self):
        self._layout.addWidget(make_section("Wake Word"))

        # Engine selector
        engine_row = QHBoxLayout()
        engine_row.setSpacing(8)
        engine_label = QLabel("Engine:")
        engine_label.setStyleSheet(get_pref_label_css())
        set_tooltip(engine_label,
            "Wake word detection engine:\n\n"
            "OpenWakeWord = ML-based, select from pre-trained models\n"
            "macOS Native = Apple's built-in recognition, custom phrases")
        engine_row.addWidget(engine_label)
        self._engine_combo = QComboBox()
        self._engine_combo.setStyleSheet(get_combobox_css())
        for value, label in self.ENGINES:
            self._engine_combo.addItem(label, value)
        idx = [e for e, _ in self.ENGINES].index(S.WAKEWORD_ENGINE) if S.WAKEWORD_ENGINE in [e for e, _ in self.ENGINES] else 0
        self._engine_combo.setCurrentIndex(idx)
        self._engine_combo.currentIndexChanged.connect(self._on_engine_changed)
        engine_row.addWidget(self._engine_combo, 1)
        self._layout.addLayout(engine_row)

        # === OpenWakeWord settings ===
        self._oww_container = QWidget()
        oww_layout = QVBoxLayout(self._oww_container)
        oww_layout.setContentsMargins(0, 4, 0, 0)
        oww_layout.setSpacing(4)

        # Model dropdown
        model_row = QHBoxLayout()
        model_row.setSpacing(8)
        model_label = QLabel("Model:")
        model_label.setStyleSheet(get_pref_label_css())
        set_tooltip(model_label, "The phrase to say to activate voice recording")
        model_row.addWidget(model_label)
        self._model_combo = QComboBox()
        self._model_combo.setStyleSheet(get_combobox_css())
        wake_word_options = get_wake_words_ordered()
        for ww in wake_word_options:
            self._model_combo.addItem(get_wake_word_display(ww), ww)
        current_model = S.WAKEWORD_OPENWAKEWORD.get('model', 'computer')
        idx = wake_word_options.index(current_model) if current_model in wake_word_options else 0
        self._model_combo.setCurrentIndex(idx)
        make_combobox_searchable(self._model_combo)
        self._model_combo.currentIndexChanged.connect(self._on_model_changed)
        model_row.addWidget(self._model_combo, 1)
        oww_layout.addLayout(model_row)

        # Sensitivity slider
        sens_row = QHBoxLayout()
        sens_row.setSpacing(8)
        sens_label = QLabel("Sensitivity:")
        sens_label.setStyleSheet(get_pref_label_css())
        set_tooltip(sens_label,
            "Wake word detection threshold (0.0-1.0).\n\n"
            "LOWER = more sensitive, triggers easily (may false trigger)\n"
            "HIGHER = less sensitive, needs clearer speech (may miss words)\n\n"
            "Try 0.1-0.2 for noisy environments, 0.3-0.5 for quiet rooms.")
        sens_row.addWidget(sens_label)
        self._sens_slider = QSlider(Qt.Orientation.Horizontal)
        self._sens_slider.setRange(1, 100)
        current_sens = S.WAKEWORD_OPENWAKEWORD.get('sensitivity', 0.2)
        self._sens_slider.setValue(int(current_sens * 100))
        self._sens_slider.setStyleSheet(get_slider_css())
        self._sens_slider.valueChanged.connect(self._on_sensitivity_changed)
        sens_row.addWidget(self._sens_slider, 1)
        self._sens_value = QLabel(f"{current_sens:.2f}")
        self._sens_value.setStyleSheet(get_pref_label_css() + " min-width: 35px;")
        sens_row.addWidget(self._sens_value)
        oww_layout.addLayout(sens_row)

        self._layout.addWidget(self._oww_container)

        # === macOS Native settings ===
        self._macos_container = QWidget()
        macos_layout = QVBoxLayout(self._macos_container)
        macos_layout.setContentsMargins(0, 4, 0, 0)
        macos_layout.setSpacing(4)

        # Phrases text input
        phrases_row = QHBoxLayout()
        phrases_row.setSpacing(8)
        phrases_label = QLabel("Phrases:")
        phrases_label.setStyleSheet(get_pref_label_css())
        set_tooltip(phrases_label,
            "Comma-separated list of phrases to listen for.\n\n"
            "Example: hey computer, computer, start recording\n\n"
            "Works offline using Apple's built-in speech recognition.")
        phrases_row.addWidget(phrases_label)
        self._phrases_edit = QLineEdit()
        self._phrases_edit.setStyleSheet(get_lineedit_css())
        self._phrases_edit.setPlaceholderText("hey computer, computer, start")
        current_phrases = S.WAKEWORD_MACOS.get('phrases', 'hey computer, computer')
        self._phrases_edit.setText(current_phrases)
        self._phrases_edit.editingFinished.connect(self._on_phrases_changed)
        phrases_row.addWidget(self._phrases_edit, 1)
        macos_layout.addLayout(phrases_row)

        # +Tmux phrases checkbox
        tmux_row = QHBoxLayout()
        tmux_row.setSpacing(8)
        self._tmux_phrases_checkbox = QCheckBox("+Tmux phrases")
        self._tmux_phrases_checkbox.setStyleSheet(get_checkbox_css())
        self._tmux_phrases_checkbox.setChecked(S.WAKEWORD_MACOS.get('use_tmux_phrases', False))
        self._update_tmux_phrases_tooltip()
        self._tmux_phrases_checkbox.stateChanged.connect(self._on_tmux_phrases_changed)
        tmux_row.addWidget(self._tmux_phrases_checkbox)
        tmux_row.addStretch()
        macos_layout.addLayout(tmux_row)

        # Info label
        info_label = QLabel("Phrases are detected offline via macOS Speech Recognition.")
        info_label.setStyleSheet(get_pref_label_css() + f" color: {TEXT_MUTED};")
        info_label.setWordWrap(True)
        macos_layout.addWidget(info_label)

        self._layout.addWidget(self._macos_container)

        # Initialize visibility
        self._update_for_engine()

    def _get_engine(self):
        return self._engine_combo.currentData()

    def _update_for_engine(self):
        """Show/hide controls based on selected engine."""
        engine = self._get_engine()
        self._oww_container.setVisible(engine == 'openwakeword')
        self._macos_container.setVisible(engine == 'macos')

    def _on_engine_changed(self, index):
        engine = self._engine_combo.itemData(index)
        S.set('WAKEWORD_ENGINE', engine)
        self._update_for_engine()
        self.engine_changed.emit(engine)
        self.settings_changed.emit()

    def _on_model_changed(self, index):
        if index < 0:
            return
        model = self._model_combo.itemData(index)
        cfg = S.WAKEWORD_OPENWAKEWORD.copy()
        cfg['model'] = model
        S.set('WAKEWORD_OPENWAKEWORD', cfg)
        self.settings_changed.emit()

    def _on_sensitivity_changed(self, value):
        sens = value / 100.0
        cfg = S.WAKEWORD_OPENWAKEWORD.copy()
        cfg['sensitivity'] = sens
        S.set('WAKEWORD_OPENWAKEWORD', cfg)
        self._sens_value.setText(f"{sens:.2f}")
        self.settings_changed.emit()

    def _on_phrases_changed(self):
        phrases = self._phrases_edit.text().strip()
        cfg = S.WAKEWORD_MACOS.copy()
        cfg['phrases'] = phrases
        S.set('WAKEWORD_MACOS', cfg)
        self.settings_changed.emit()

    def _on_tmux_phrases_changed(self, state):
        cfg = S.WAKEWORD_MACOS.copy()
        cfg['use_tmux_phrases'] = (state == Qt.CheckState.Checked.value)
        S.set('WAKEWORD_MACOS', cfg)
        self.settings_changed.emit()

    def _update_tmux_phrases_tooltip(self):
        """Update tooltip with example from actual tmux pane phrases."""
        # Get first available tmux phrase for example
        example_phrase = None
        for info in S.TMUX_PANE_NAMES.values():
            phrase = info.get('phrase', '')
            if phrase:
                example_phrase = phrase
                break
        example_phrase = example_phrase or "phrase"

        set_tooltip(self._tmux_phrases_checkbox,
            "Add tmux pane phrases as wake words (start only, not stop).\n\n"
            "When a tmux phrase is spoken, recording starts and the phrase\n"
            "is prepended to the transcription so it routes to the right pane.\n\n"
            f"Example: Say '{example_phrase}' to start, transcription becomes '{example_phrase} ...'\n\n"
            "Note: Regular wake words can still stop recording - only tmux\n"
            "phrases are restricted to starting.")

    def get_current_display_name(self) -> str:
        """Get display name for current wake word (for tooltip etc)."""
        engine = self._get_engine()
        if engine == 'openwakeword':
            model = S.WAKEWORD_OPENWAKEWORD.get('model', 'computer')
            return get_wake_word_display(model)
        else:
            phrases = S.WAKEWORD_MACOS.get('phrases', 'hey computer')
            # Return first phrase
            first = phrases.split(',')[0].strip() if phrases else 'hey computer'
            return first


class PrefsDialog(DraggableDialog):
    """Preferences dialog with theme, wake word settings, and pet selection.

    Settings apply IMMEDIATELY as you change them (live preview).
    OK = save to JSON, Cancel = revert to original values.
    """

    style_changed = pyqtSignal(str)  # Emits style name when changed
    pets_changed = pyqtSignal(list)  # Emits list of PetType when changed
    simple_mode_changed = pyqtSignal(bool)  # Emits when simple mode toggled
    wake_word_changed = pyqtSignal(str)  # Emits wake word engine/settings change
    auto_enter_changed = pyqtSignal(bool)  # Emits auto enter flag

    def __init__(self, current_style, current_pet_types, simple_mode=False, parent=None,
                 auto_enter=None):
        super().__init__(parent)
        # Register note callback for piano visualization
        from synth import set_note_callback
        set_note_callback(self._on_notes_played)

        # Store ORIGINAL values for Cancel revert
        self.original_style = current_style
        self.original_pets = list(current_pet_types) if current_pet_types else []
        self.original_wakeword_engine = S.WAKEWORD_ENGINE
        self.original_wakeword_oww = S.WAKEWORD_OPENWAKEWORD.copy()
        self.original_wakeword_macos = S.WAKEWORD_MACOS.copy()
        self.original_auto_enter = auto_enter if auto_enter is not None else S.AUTO_ENTER

        # Current values (start same as original)
        self.selected_style = current_style
        self.selected_pets = list(self.original_pets)
        self.pet_checkboxes = {}
        self._style_buttons = {}  # Map button -> style_name

        layout = QVBoxLayout(self)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(12)

        layout.addWidget(make_title("Preferences"))

        # Main content: Theme | Settings
        content = QHBoxLayout()
        content.setSpacing(15)

        # Left side: Notification Chime Instrument + Theme
        theme_box = QVBoxLayout()
        theme_box.setSpacing(4)  # Reduced vertical spacing (was default ~12)

        # Notification Chime Instrument section (merged volume + instrument)
        theme_box.addWidget(make_section("Notification Chime Instrument"))

        # Volume slider with mute (at top)
        vol_row = QHBoxLayout()
        vol_row.setSpacing(4)
        vol_label = QLabel("Volume:")
        vol_label.setStyleSheet(get_pref_label_css())
        vol_row.addWidget(vol_label)
        self.vol_slider = QSlider(Qt.Orientation.Horizontal)
        self.vol_slider.setRange(0, 100)
        self.vol_slider.setValue(int(S.CHIME_VOLUME * 100))
        self.vol_slider.setStyleSheet(get_slider_css())
        self.vol_slider.setEnabled(S.SOUND_ENABLED)
        self.vol_slider.valueChanged.connect(self._on_volume_changed)
        vol_row.addWidget(self.vol_slider, 1)
        self.vol_value = QLabel(f"{int(S.CHIME_VOLUME * 100)}%")
        self.vol_value.setStyleSheet(get_pref_label_css() + " min-width: 30px;")
        vol_row.addWidget(self.vol_value)
        self.mute_checkbox = QCheckBox("Mute")
        self.mute_checkbox.setChecked(not S.SOUND_ENABLED)
        self.mute_checkbox.setStyleSheet(get_checkbox_css())
        self.mute_checkbox.stateChanged.connect(self._on_mute_changed)
        vol_row.addWidget(self.mute_checkbox)
        theme_box.addLayout(vol_row)

        # Pitch slider (-24 to +24 semitones)
        pitch_row = QHBoxLayout()
        pitch_row.setSpacing(4)
        pitch_label = QLabel("Pitch:")
        pitch_label.setStyleSheet(get_pref_label_css())
        set_tooltip(pitch_label, "Pitch shift in semitones (-24 to +24)")
        pitch_row.addWidget(pitch_label)
        self.pitch_slider = QSlider(Qt.Orientation.Horizontal)
        self.pitch_slider.setRange(-24, 24)
        self.pitch_slider.setValue(S.CHIME_PITCH)
        self.pitch_slider.setStyleSheet(get_slider_css())
        self.pitch_slider.valueChanged.connect(self._on_pitch_changed)
        pitch_row.addWidget(self.pitch_slider, 1)
        self.pitch_value = QLabel(f"{S.CHIME_PITCH:+d}")
        self.pitch_value.setStyleSheet(get_pref_label_css() + " min-width: 30px;")
        pitch_row.addWidget(self.pitch_value)
        theme_box.addLayout(pitch_row)

        # Instrument grid with icons (plays demo on click)
        from synth import get_preset_name
        # Map program_number -> icon_file (sorted by program number)
        preset_icons = [
            (0, 'inst-bell'), (1, 'inst-carillon'), (5, 'inst-organ'),
            (17, 'inst-flute'), (18, 'inst-strings'),
            (25, 'inst-calliope'), (29, 'inst-fantasy'), (32, 'inst-vibes'),
            (38, 'inst-sparkle'), (44, 'inst-wave'), (48, 'inst-choir'),
            (60, 'inst-moon'), (68, 'inst-xylophone'), (69, 'inst-triangle'),
            (79, 'inst-bubble'), (83, 'inst-crystal'), (84, 'inst-prism'),
            (86, 'inst-harp'), (92, 'inst-aurora'), (99, 'inst-magic'),
            (103, 'inst-cosmic'), (105, 'inst-dream'), (110, 'inst-delicate'),
            (120, 'inst-marimba'),
        ]
        self._inst_buttons = {}
        inst_grid = QGridLayout()
        inst_grid.setSpacing(2)
        for i, (prog_num, icon_name) in enumerate(preset_icons):
            btn = QPushButton()
            btn.setFixedSize(24, 24)
            icon = load_icon(icon_name, color=ICON_COLOR_DARK)  # Dark gray icons on light themes
            if icon:
                btn.setIcon(icon)
                btn.setIconSize(QSize(18, 18))
            preset_name = get_preset_name(prog_num)
            btn.setToolTip(f"{preset_name} ({prog_num})")
            base_css = get_btn_css().replace("padding: 3px 8px;", "padding: 0px; margin: 0px;").replace("text-align: left;", "text-align: center;")
            btn.setStyleSheet(base_css)
            btn.clicked.connect(lambda checked, p=prog_num: self._select_program(p))
            btn.icon_name = icon_name  # Store for later icon color updates
            self._inst_buttons[btn] = prog_num
            inst_grid.addWidget(btn, i // 6, i % 6)  # 6 columns
        theme_box.addLayout(inst_grid)
        self._update_inst_buttons()  # Highlight current

        # Instrument name label (above program selector)
        self.prog_name_label = QLabel()
        self.prog_name_label.setStyleSheet(get_pref_label_css() + " font-size: 11px;")  # Uses TEXT_PRIMARY
        self.prog_name_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        theme_box.addWidget(self.prog_name_label)

        # Program number selector with mini 7-segment display
        prog_row = QHBoxLayout()
        prog_row.setSpacing(4)
        prog_label = QLabel("Prog:")
        prog_label.setStyleSheet(get_pref_label_css())
        set_tooltip(prog_label, "Synth program number (0-127)")
        prog_row.addWidget(prog_label)
        # Minus button with icon
        self.prog_minus = QPushButton()
        self.prog_minus.setFixedSize(24, 24)
        minus_icon = load_icon('minus', color=ICON_COLOR_DARK)
        if minus_icon:
            self.prog_minus.setIcon(minus_icon)
            self.prog_minus.setIconSize(QSize(14, 14))
        prog_btn_css = get_btn_css().replace("padding: 3px 8px;", "padding: 0px; margin: 0px;").replace("text-align: left;", "text-align: center;")
        self.prog_minus.setStyleSheet(prog_btn_css)
        self.prog_minus.clicked.connect(self._prog_decrement)
        prog_row.addWidget(self.prog_minus)
        # 7-segment display
        self.prog_display = Mini7Segment(S.CHIME_PROGRAM, ICON_COLOR_DARK)
        prog_row.addWidget(self.prog_display)
        # Plus button with icon
        self.prog_plus = QPushButton()
        self.prog_plus.setFixedSize(24, 24)
        plus_icon = load_icon('plus', color=ICON_COLOR_DARK)
        if plus_icon:
            self.prog_plus.setIcon(plus_icon)
            self.prog_plus.setIconSize(QSize(14, 14))
        self.prog_plus.setStyleSheet(prog_btn_css)
        self.prog_plus.clicked.connect(self._prog_increment)
        prog_row.addWidget(self.prog_plus)
        prog_row.addStretch()
        theme_box.addLayout(prog_row)
        self._update_prog_display()  # Initialize name label

        # Mini piano keyboard (shifts smoothly with pitch)
        self.piano_hint = QLabel("")
        self.piano_hint.setStyleSheet(f"color: {TEXT_SECONDARY}; font-size: 9px;")
        self.piano_hint.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.piano = PianoWidget(
            height=36, hint_label=self.piano_hint,
            pitch_getter=lambda: S.CHIME_PITCH,
            settings_getter=lambda: (S.CHIME_PITCH, S.CHIME_VOLUME, S.CHIME_PROGRAM)
        )
        theme_box.addWidget(self.piano)
        theme_box.addWidget(self.piano_hint)

        # Chime theme dropdown
        chime_theme_row = QHBoxLayout()
        chime_theme_label = QLabel("Chime Style")
        chime_theme_label.setStyleSheet(get_pref_label_css())
        set_tooltip(chime_theme_label, "Musical style for chime sounds")
        chime_theme_row.addWidget(chime_theme_label)
        self.chime_theme_combo = QComboBox()
        self.chime_theme_combo.setStyleSheet(get_combobox_css())
        for theme_name in CHIME_THEMES.keys():
            display = theme_name.replace("_", " ").title()
            self.chime_theme_combo.addItem(display, theme_name)
        idx = self.chime_theme_combo.findData(S.CHIME_THEME)
        if idx >= 0:
            self.chime_theme_combo.setCurrentIndex(idx)
        self.chime_theme_combo.currentIndexChanged.connect(self._on_chime_theme_changed)
        chime_theme_row.addWidget(self.chime_theme_combo, 1)
        theme_box.addLayout(chime_theme_row)

        # TTS (Text-to-Speech) Section
        self.tts_widget = TTSSettingsWidget(self)
        theme_box.addWidget(self.tts_widget)

        theme_box.addWidget(make_section("Theme"))
        # Theme buttons in compact sub-layout (60% reduced spacing = ~2px)
        theme_btns_box = QVBoxLayout()
        theme_btns_box.setSpacing(2)
        style_keys = list(STYLES.keys())
        # Custom display names for themes
        THEME_DISPLAY_NAMES = {"rust_grunge": "SBU Tunnels", "macos_2005": "MacOS 2005"}
        for i, style_name in enumerate(style_keys):
            key = str(i + 1)
            display_name = THEME_DISPLAY_NAMES.get(style_name, style_name.replace("_", " ").title())
            btn = QPushButton(f"{key}  {display_name}")
            base_css = get_btn_css().replace("padding: 3px 8px;", "padding: 1px 8px; margin: 0px;")
            btn.setStyleSheet(base_css)
            if style_name == current_style:
                btn.setStyleSheet(base_css + f"QPushButton {{ border: 2px solid {CYAN_CSS}; }}")
            btn.clicked.connect(lambda checked, s=style_name, b=btn: self._select_style(s, b))
            self._style_buttons[btn] = style_name
            theme_btns_box.addWidget(btn)
        theme_box.addLayout(theme_btns_box)
        theme_box.addStretch()
        content.addLayout(theme_box)

        # Separator
        sep = QLabel()
        sep.setFixedWidth(1)
        sep.setStyleSheet(f"background: {BORDER_COLOR};")
        content.addWidget(sep)

        # Right side: All other settings
        settings_box = QVBoxLayout()
        settings_box.setSpacing(10)

        # Wake Word settings widget
        self.wake_word_widget = WakeWordSettingsWidget()
        self.wake_word_widget.engine_changed.connect(self._on_wake_word_engine_changed)
        self.wake_word_widget.settings_changed.connect(self._on_wake_word_settings_changed)
        settings_box.addWidget(self.wake_word_widget)

        # Paste Behavior section (separate from wake word)
        settings_box.addWidget(make_section("Paste Behavior"))

        # All four checkboxes in one horizontal row with icons
        # Order: Copy, ⌘V paste, Tmux paste, Enter after paste
        auto_row = QHBoxLayout()
        auto_row.setSpacing(12)

        # Store icon labels for graying out
        self._paste_icon_labels = []

        # Copy
        copy_icon_label = QLabel()
        copy_icon = load_icon("copy", color=ICON_COLOR_DARK)
        if copy_icon:
            copy_icon_label.setPixmap(copy_icon.pixmap(14, 14))
        auto_row.addWidget(copy_icon_label)
        self.copy_checkbox = QCheckBox("Copy to clipboard")
        self.copy_checkbox.setChecked(S.AUTO_COPY)
        self.copy_checkbox.setStyleSheet(get_checkbox_css())
        self.copy_checkbox.setToolTip("Copy transcription to clipboard after recording.\n\n"
                                       "Other paste options require this to be enabled.")
        self.copy_checkbox.stateChanged.connect(self._on_auto_copy_pref_changed)
        auto_row.addWidget(self.copy_checkbox)

        # ⌘V Paste
        paste_icon_label = QLabel()
        paste_icon = load_icon("layers", color=ICON_COLOR_DARK)
        if paste_icon:
            paste_icon_label.setPixmap(paste_icon.pixmap(14, 14))
        auto_row.addWidget(paste_icon_label)
        self._paste_icon_labels.append(paste_icon_label)
        self.paste_checkbox = QCheckBox("⌘V paste")
        self.paste_checkbox.setChecked(S.AUTO_PASTE)
        self.paste_checkbox.setStyleSheet(get_checkbox_css())
        self.paste_checkbox.setToolTip("Automatically paste transcription via ⌘V.\n\n"
                                        "Requires 'Copy to clipboard' to be enabled.")
        self.paste_checkbox.stateChanged.connect(self._on_auto_paste_pref_changed)
        auto_row.addWidget(self.paste_checkbox)

        # Tmux Paste
        tmux_icon_label = QLabel()
        tmux_icon = load_icon("tmux", color=ICON_COLOR_DARK)
        if tmux_icon:
            tmux_icon_label.setPixmap(tmux_icon.pixmap(14, 14))
        auto_row.addWidget(tmux_icon_label)
        self._paste_icon_labels.append(tmux_icon_label)
        self.tmux_checkbox = QCheckBox("Tmux paste")
        self.tmux_checkbox.setChecked(S.TMUX_MODE)
        self.tmux_checkbox.setStyleSheet(get_checkbox_css())
        self.tmux_checkbox.setToolTip("Paste directly into active tmux pane using send-keys.\n\n"
                                       "Requires 'Copy to clipboard' to be enabled.\n"
                                       "When enabled, replaces ⌘V paste.")
        self.tmux_checkbox.stateChanged.connect(self._on_tmux_pref_changed)
        auto_row.addWidget(self.tmux_checkbox)

        # Enter after paste
        enter_icon_label = QLabel()
        enter_icon = load_icon("enter", color=ICON_COLOR_DARK)
        if enter_icon:
            enter_icon_label.setPixmap(enter_icon.pixmap(14, 14))
        auto_row.addWidget(enter_icon_label)
        self._paste_icon_labels.append(enter_icon_label)
        self.enter_checkbox = QCheckBox("Enter after paste")
        self.enter_checkbox.setChecked(S.AUTO_ENTER)
        self.enter_checkbox.setStyleSheet(get_checkbox_css())
        self.enter_checkbox.setToolTip("Press Enter after pasting transcription.\n\n"
                                        "With ⌘V paste: sends keyboard Enter key\n"
                                        "With Tmux paste: uses tmux send-keys Enter\n"
                                        "Both use the Enter Delay setting below.\n\n"
                                        "Has no effect if neither paste mode is enabled.")
        self.enter_checkbox.stateChanged.connect(self._on_enter_changed)
        auto_row.addWidget(self.enter_checkbox)

        auto_row.addStretch()
        settings_box.addLayout(auto_row)

        # Initial state update for grayed out options
        self._update_paste_options_state()

        # Enter delay slider
        delay_row = QHBoxLayout()
        delay_row.setSpacing(8)
        delay_label = QLabel("Enter Delay:")
        delay_label.setStyleSheet(get_pref_label_css())
        set_tooltip(delay_label, "Seconds to wait after pasting before pressing Enter.\n\n"
                                 "0s = Immediate (may race with paste)\n"
                                 "0.1s = Usually enough for paste to complete\n"
                                 "0.5-2s = Safe for slow applications")
        delay_row.addWidget(delay_label)
        self.delay_slider = QSlider(Qt.Orientation.Horizontal)
        self.delay_slider.setRange(0, 20)  # 0.0s to 2.0s in 0.1s steps
        self.delay_slider.setValue(int(S.ENTER_DELAY * 10))
        self.delay_slider.setStyleSheet(get_slider_css())
        self.delay_slider.valueChanged.connect(self._on_delay_changed)
        delay_row.addWidget(self.delay_slider, 1)
        self.delay_value = QLabel(f"{S.ENTER_DELAY:.1f}s")
        self.delay_value.setStyleSheet(get_pref_label_css() + " min-width: 35px;")
        delay_row.addWidget(self.delay_value)
        settings_box.addLayout(delay_row)

        # Recording section
        settings_box.addWidget(make_section("Recording"))

        # Silence skip toggle
        silence_row = QHBoxLayout()
        silence_row.setSpacing(8)
        silence_label = QLabel("Skip Silence:")
        silence_label.setStyleSheet(get_pref_label_css())
        set_tooltip(silence_label, "When enabled, recording pauses during silence.\n\n"
                                   "Useful for long recordings with gaps - the waveform\n"
                                   "won't scroll during quiet periods.")
        silence_row.addWidget(silence_label)
        self.silence_checkbox = QCheckBox("Skip recording during silence")
        self.silence_checkbox.setChecked(S.SILENCE_SKIP_ENABLED)
        self.silence_checkbox.setStyleSheet(get_checkbox_css(12))
        self.silence_checkbox.stateChanged.connect(self._on_silence_skip_changed)
        silence_row.addWidget(self.silence_checkbox, 1)
        settings_box.addLayout(silence_row)

        # Silence threshold slider (-100 to -10 dB)
        thresh_row = QHBoxLayout()
        thresh_row.setSpacing(8)
        thresh_label = QLabel("Threshold:")
        thresh_label.setStyleSheet(get_pref_label_css())
        set_tooltip(thresh_label, "Audio level (dB) below which sound is considered silence.\n\n"
                                  "-100 dB = Extremely sensitive (skip only digital silence)\n"
                                  "-80 dB = Very sensitive (skip near-total silence)\n"
                                  "-40 dB = Normal (skip quiet background noise)\n"
                                  "-20 dB = Aggressive (skip soft speech too)")
        thresh_row.addWidget(thresh_label)
        self.thresh_slider = QSlider(Qt.Orientation.Horizontal)
        self.thresh_slider.setRange(-100, -10)  # dB range
        self.thresh_slider.setValue(S.SILENCE_THRESHOLD)
        self.thresh_slider.setStyleSheet(get_slider_css())
        self.thresh_slider.valueChanged.connect(self._on_threshold_changed)
        thresh_row.addWidget(self.thresh_slider, 1)
        self.thresh_value = QLabel(f"{S.SILENCE_THRESHOLD} dB")
        self.thresh_value.setStyleSheet(get_pref_label_css() + " min-width: 45px;")
        thresh_row.addWidget(self.thresh_value)
        settings_box.addLayout(thresh_row)

        # Context Words section
        settings_box.addWidget(make_section("Context Words"))
        context_row = QHBoxLayout()
        context_row.setSpacing(8)
        context_label = QLabel("Words:")
        context_label.setStyleSheet(get_pref_label_css())
        set_tooltip(context_label,
            "Comma-separated words to help Whisper recognize.\n\n"
            "Use for names, jargon, or unusual spellings that Whisper\n"
            "might not know. These words bias the transcription output.\n\n"
            "Examples:\n"
            "  • Names: Ryan, Xiaowen, PyTorch\n"
            "  • Jargon: CUDA, NumPy, einops\n"
            "  • Wake words: Wall-E, Wally"
        )
        context_row.addWidget(context_label)
        self.context_edit = QLineEdit()
        self.context_edit.setText(S.CUSTOM_WORDS)
        self.context_edit.setPlaceholderText("e.g. \"Wall-E, Wally, PyTorch, CUDA\"")
        self.context_edit.setStyleSheet(get_lineedit_css())
        self.context_edit.textChanged.connect(self._on_context_changed)
        context_row.addWidget(self.context_edit, 1)
        settings_box.addLayout(context_row)

        # Tmux phrases as context words
        phrases_ctx_row = QHBoxLayout()
        phrases_ctx_row.setSpacing(8)
        self.phrases_ctx_check = QCheckBox("+tmux phrases")
        self.phrases_ctx_check.setChecked(S.TMUX_PHRASES_AS_CONTEXT)
        self.phrases_ctx_check.setStyleSheet(get_checkbox_css())
        set_tooltip(self.phrases_ctx_check,
            "Include tmux magic phrases as context words.\n"
            "Helps Whisper recognize phrase words in speech."
        )
        self.phrases_ctx_check.stateChanged.connect(self._on_phrases_ctx_changed)
        phrases_ctx_row.addWidget(self.phrases_ctx_check)
        self.phrases_ctx_label = QLabel("")
        self.phrases_ctx_label.setStyleSheet(f"color: #888; font-size: 11px;")
        self._update_phrases_ctx_label()
        phrases_ctx_row.addWidget(self.phrases_ctx_label, 1)
        settings_box.addLayout(phrases_ctx_row)

        # LLM section
        settings_box.addWidget(make_section("LLM Post-Processing"))
        # Model dropdown with enable checkbox
        llm_model_row = QHBoxLayout()
        llm_model_row.setSpacing(8)
        llm_model_label = QLabel("Model:")
        llm_model_label.setStyleSheet(get_pref_label_css())
        set_tooltip(llm_model_label,
            "LLM model used to clean up transcripts.\n\n"
            "When LLM is enabled, transcripts are sent to this model\n"
            "to remove filler words, fix stutters, etc.\n\n"
            "OLLAMA models run locally (free, private).\n"
            "OpenAI models require OPENAI_API_KEY env var."
        )
        llm_model_row.addWidget(llm_model_label)
        self.llm_model_combo = make_searchable_dropdown(
            LLM_MODELS, S.LLM_MODEL, self._on_llm_model_changed
        )
        llm_model_row.addWidget(self.llm_model_combo, 1)
        self.llm_enabled_checkbox = QCheckBox("Enable")
        self.llm_enabled_checkbox.setChecked(S.LLM_ENABLED)
        self.llm_enabled_checkbox.setStyleSheet(get_checkbox_css())
        self.llm_enabled_checkbox.setToolTip("Enable LLM post-processing (R)")
        self.llm_enabled_checkbox.stateChanged.connect(self._on_llm_enabled_changed)
        llm_model_row.addWidget(self.llm_enabled_checkbox)
        settings_box.addLayout(llm_model_row)
        # Prompt prefix
        self.llm_prefix_edit, llm_prefix_layout, self._show_preset_dialog = make_labeled_textedit(
            "Prompt Prefix:",
            S.LLM_PREFIX or DEFAULT_LLM_PREFIX,
            "Leave empty for default de-ramble prompt...",
            "Instructions sent to the LLM before your transcript.\n\n"
            "The LLM receives: [this prompt] + [your transcribed text]\n"
            "Default removes filler words, fixes stutters, applies\n"
            "self-corrections. Customize to change how text is cleaned.",
            self._on_llm_prefix_changed,
            height=60,
            presets=LLM_PROMPT_PRESETS,
            edit_dialog_title="Edit Prompt Prefix"
        )
        settings_box.addLayout(llm_prefix_layout)

        # Recordings Folder section
        settings_box.addWidget(make_section("Recordings Folder"))
        folder_row = QHBoxLayout()
        folder_row.setSpacing(8)
        self.folder_label = QLabel(S.RECORDINGS_DIR)
        self.folder_label.setStyleSheet(
            f"QLabel {{ color: {TEXT_PRIMARY}; font-size: 11px; font-family: Menlo, monospace; "
            f"background: rgba(255,255,255,0.1); padding: 4px 8px; border-radius: 3px; }}"
        )
        self.folder_label.setToolTip("Folder where audio recordings and transcripts are saved.\n\n"
                                      "Click 'Select' to choose a different folder.\n"
                                      "Click the reset arrow to revert to the default temp folder.")
        folder_row.addWidget(self.folder_label, 1)
        select_folder_btn = QPushButton("Select")
        select_folder_btn.setStyleSheet(get_btn_css())
        select_folder_btn.setToolTip("Choose a folder for recordings")
        select_folder_btn.clicked.connect(self._select_recordings_folder)
        folder_row.addWidget(select_folder_btn)
        revert_folder_btn = QPushButton()
        revert_folder_btn.setIcon(load_icon("reset", color=ICON_COLOR_DARK))
        revert_folder_btn.setFixedSize(28, 28)
        revert_folder_btn.setStyleSheet(get_btn_css())
        revert_folder_btn.setToolTip(f"Revert to default folder:\n{DEFAULT_RECORDINGS_DIR}")
        revert_folder_btn.clicked.connect(self._revert_recordings_folder)
        folder_row.addWidget(revert_folder_btn)
        settings_box.addLayout(folder_row)

        # Pet section - checkboxes for multi-select
        settings_box.addWidget(make_section("Pet Companions"))
        pet_grid = QHBoxLayout()
        pet_grid.setSpacing(4)
        for pet_type in ALL_PET_TYPES:
            pet_widget = QWidget()
            pet_layout = QVBoxLayout(pet_widget)
            pet_layout.setContentsMargins(2, 2, 2, 2)
            pet_layout.setSpacing(2)

            # Pet icon label - clickable to toggle checkbox
            icon_label = QLabel()
            icon = get_pet_icon(pet_type, 32)
            if icon and not icon.isNull():
                icon_label.setPixmap(icon)
            icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            icon_label.setFixedSize(36, 36)
            icon_label.setStyleSheet("QLabel { background: rgba(60,60,60,0.8); border-radius: 4px; }")
            icon_label.setCursor(Qt.CursorShape.PointingHandCursor)
            pet_layout.addWidget(icon_label)

            # Checkbox
            checkbox = QCheckBox()
            checkbox.setChecked(pet_type in S.PET_TYPES)
            checkbox.setToolTip(pet_type.value.replace("_", " ").title())
            checkbox.stateChanged.connect(lambda state, p=pet_type: self._toggle_pet(p, state))
            checkbox.setStyleSheet("QCheckBox { color: white; }")
            pet_layout.addWidget(checkbox, alignment=Qt.AlignmentFlag.AlignCenter)

            # Make icon clickable - toggle checkbox when clicked
            icon_label.mousePressEvent = lambda e, cb=checkbox: cb.toggle()

            self.pet_checkboxes[pet_type] = checkbox
            pet_grid.addWidget(pet_widget)
        settings_box.addLayout(pet_grid)

        # Window section
        settings_box.addWidget(make_section("Window"))
        window_row = QHBoxLayout()
        window_row.setSpacing(8)
        self.always_on_top_checkbox = QCheckBox("Always on Top")
        self.always_on_top_checkbox.setChecked(S.ALWAYS_ON_TOP)
        self.always_on_top_checkbox.setStyleSheet(get_checkbox_css())
        self.always_on_top_checkbox.setToolTip("Keep window above other windows")
        self.always_on_top_checkbox.stateChanged.connect(self._on_always_on_top_changed)
        window_row.addWidget(self.always_on_top_checkbox)
        window_row.addStretch()
        settings_box.addLayout(window_row)

        settings_box.addStretch()
        content.addLayout(settings_box)
        layout.addLayout(content)

        # Bottom action buttons row (3 equally spaced)
        action_row = QHBoxLayout()
        action_row.setSpacing(8)
        # Select Whisper Model button
        self.model_select_btn = QPushButton("  Select Whisper Model")
        self.model_select_btn.setIcon(load_icon("mic", color=ICON_COLOR_DARK))
        self.model_select_btn.setStyleSheet(get_btn_css())
        self.model_select_btn.setToolTip("Change Whisper transcription model")
        self.model_select_btn.clicked.connect(self._select_whisper_model)
        action_row.addWidget(self.model_select_btn, 1)
        # Revert to defaults button
        revert_btn = QPushButton("  Revert to Defaults")
        revert_btn.setIcon(load_icon("reset", color=ICON_COLOR_DARK))
        revert_btn.setStyleSheet(get_btn_css())
        revert_btn.setToolTip("Reset all settings to defaults")
        revert_btn.clicked.connect(self._revert_to_defaults)
        action_row.addWidget(revert_btn, 1)
        # Open settings folder button
        folder_btn = QPushButton("  Open Settings Folder")
        folder_btn.setIcon(load_icon("folder-open", color=ICON_COLOR_DARK))
        folder_btn.setStyleSheet(get_btn_css())
        folder_btn.setToolTip(f"Open {_VOICETHING_DIR}")
        folder_btn.clicked.connect(self._open_settings_folder)
        action_row.addWidget(folder_btn, 1)
        layout.addLayout(action_row)

        # Cancel/OK buttons
        btn_row = QHBoxLayout()
        btn_row.setSpacing(8)
        cancel_btn = QPushButton("Esc  Cancel")
        cancel_btn.setStyleSheet(get_btn_css())
        cancel_btn.clicked.connect(self.reject)
        btn_row.addWidget(cancel_btn)
        ok_btn = QPushButton("Enter  OK")
        ok_btn.setStyleSheet(get_btn_css())
        ok_btn.clicked.connect(self.accept)
        btn_row.addWidget(ok_btn)
        layout.addLayout(btn_row)
        self.setMinimumWidth(600)  # Wide enough for two-column layout
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.setFocus()  # Don't focus textboxes - allow number keys for themes

    def _select_style(self, style_name, clicked_btn):
        """Select a style and apply it immediately, then close dialog."""
        self.selected_style = style_name
        self.style_changed.emit(style_name)
        self.accept()  # Close dialog - avoids partial redraw issues

    def _toggle_pet(self, pet_type, state):
        if state == Qt.CheckState.Checked.value:
            if pet_type not in self.selected_pets:
                self.selected_pets.append(pet_type)
        else:
            if pet_type in self.selected_pets:
                self.selected_pets.remove(pet_type)
        self.pets_changed.emit(list(self.selected_pets))  # Apply immediately

    def _on_wake_word_engine_changed(self, engine):
        """Handle wake word engine change - restart listener if active."""
        self.wake_word_changed.emit(engine)

    def _on_wake_word_settings_changed(self):
        """Handle any wake word setting change - restart listener if active."""
        # Emit the engine change signal to trigger restart
        self.wake_word_changed.emit(S.WAKEWORD_ENGINE)

    def _on_enter_changed(self, state):
        S.set('AUTO_ENTER', state == Qt.CheckState.Checked.value)

    def _on_delay_changed(self, value):
        S.set('ENTER_DELAY', value / 10.0)
        self.delay_value.setText(f"{S.ENTER_DELAY:.1f}s")

    def _on_silence_skip_changed(self, state):
        S.SILENCE_SKIP_ENABLED = state == Qt.CheckState.Checked.value

    def _on_always_on_top_changed(self, state):
        S.set('ALWAYS_ON_TOP', state == Qt.CheckState.Checked.value)

    def _on_auto_copy_pref_changed(self, state):
        S.set('AUTO_COPY', state == Qt.CheckState.Checked.value)
        self._update_paste_options_state()

    def _on_auto_paste_pref_changed(self, state):
        S.set('AUTO_PASTE', state == Qt.CheckState.Checked.value)
        self._update_paste_options_state()

    def _on_tmux_pref_changed(self, state):
        S.set('TMUX_MODE', state == Qt.CheckState.Checked.value)
        self._update_paste_options_state()

    def _update_paste_options_state(self):
        """Gray out paste options based on dependencies.

        - If Copy to clipboard is off, gray out all other paste options
        - If both ⌘V paste and Tmux paste are off, gray out Enter after paste
        """
        copy_enabled = self.copy_checkbox.isChecked()
        paste_enabled = self.paste_checkbox.isChecked()
        tmux_enabled = self.tmux_checkbox.isChecked()
        any_paste_mode = paste_enabled or tmux_enabled

        # Gray out style for disabled checkboxes
        enabled_style = f"QCheckBox {{ color: {TEXT_PRIMARY}; font-size: 11px; }}"
        disabled_style = f"QCheckBox {{ color: {TEXT_SECONDARY}; font-size: 11px; }}"

        # ⌘V paste and Tmux paste depend on Copy being enabled
        self.paste_checkbox.setEnabled(copy_enabled)
        self.paste_checkbox.setStyleSheet(enabled_style if copy_enabled else disabled_style)
        self.tmux_checkbox.setEnabled(copy_enabled)
        self.tmux_checkbox.setStyleSheet(enabled_style if copy_enabled else disabled_style)

        # Enter after paste depends on Copy AND at least one paste mode
        enter_enabled = copy_enabled and any_paste_mode
        self.enter_checkbox.setEnabled(enter_enabled)
        self.enter_checkbox.setStyleSheet(enabled_style if enter_enabled else disabled_style)

        # Update icon opacity for visual consistency
        for i, label in enumerate(self._paste_icon_labels):
            # Index 0,1 = paste/tmux icons, 2 = enter icon
            if i < 2:
                label.setEnabled(copy_enabled)
            else:
                label.setEnabled(enter_enabled)

    def _on_threshold_changed(self, value):
        S.SILENCE_THRESHOLD = value
        self.thresh_value.setText(f"{value} dB")

    def _on_mute_changed(self, state):
        S.set('SOUND_ENABLED', state != Qt.CheckState.Checked.value)
        self.vol_slider.setEnabled(S.SOUND_ENABLED)

    def _on_volume_changed(self, value):
        S.CHIME_VOLUME = value / 100.0
        self.vol_value.setText(f"{value}%")

    def _on_pitch_changed(self, value):
        S.CHIME_PITCH = value
        self.pitch_value.setText(f"{value:+d}")
        self.piano.update()  # Redraw piano with shifted keys

    def _on_chime_theme_changed(self, index):
        theme = self.chime_theme_combo.currentData()
        S.CHIME_THEME = theme
        # Play demo to hear the new theme
        import threading
        threading.Thread(target=lambda: play_chime('demo'), daemon=True).start()

    def _select_program(self, prog):
        """Select program number, update all UI, and play demo."""
        S.CHIME_PROGRAM = prog
        self._update_inst_buttons()
        self._update_prog_display()
        # Play demo chime in background
        import threading
        threading.Thread(target=lambda: play_chime('demo'), daemon=True).start()

    def _prog_increment(self):
        """Increment program number with wrap-around."""
        prog = (S.CHIME_PROGRAM + 1) % 128  # Wrap 127 -> 0
        self._select_program(prog)

    def _prog_decrement(self):
        """Decrement program number with wrap-around."""
        prog = (S.CHIME_PROGRAM - 1) % 128  # Wrap 0 -> 127
        self._select_program(prog)

    def _update_inst_buttons(self):
        """Highlight instrument button matching current program number."""
        base_css = get_btn_css().replace("padding: 3px 8px;", "padding: 0px; margin: 0px;").replace("text-align: left;", "text-align: center;")
        for btn, prog_num in self._inst_buttons.items():
            if prog_num == S.CHIME_PROGRAM:
                btn.setStyleSheet(base_css + f"QPushButton {{ border: 2px solid {CYAN_CSS}; }}")
            else:
                btn.setStyleSheet(base_css)

    def _update_prog_display(self):
        """Update program display and name label."""
        self.prog_display.set_value(S.CHIME_PROGRAM)
        from synth import get_preset_name
        name = get_preset_name(S.CHIME_PROGRAM)
        self.prog_name_label.setText(name)

    def _on_notes_played(self, semitones, duration, shift):
        """Called when any notes are played - triggers piano keys visually."""
        if hasattr(self, 'piano') and self.piano:
            for semitone in semitones:
                self.piano.trigger_key(semitone, duration)

    def accept(self):
        """Clear note callback when dialog closes."""
        from synth import set_note_callback
        set_note_callback(None)
        super().accept()

    def reject(self):
        """Clear note callback when dialog closes."""
        from synth import set_note_callback
        set_note_callback(None)
        super().reject()

    def _on_context_changed(self, text):
        S.CUSTOM_WORDS = text

    def _on_phrases_ctx_changed(self, state):
        S.TMUX_PHRASES_AS_CONTEXT = bool(state)
        self._update_phrases_ctx_label()

    def _update_phrases_ctx_label(self):
        """Show all phrase words in gray if checkbox is checked."""
        if S.TMUX_PHRASES_AS_CONTEXT and S.TMUX_PANE_NAMES:
            words = set()
            for info in S.TMUX_PANE_NAMES.values():
                phrase = info.get('phrase', '')
                words.update(phrase.split())
            if words:
                self.phrases_ctx_label.setText(' '.join(sorted(words)))
            else:
                self.phrases_ctx_label.setText("")
        else:
            self.phrases_ctx_label.setText("")

    def _on_llm_enabled_changed(self, state):
        S.set('LLM_ENABLED', state == Qt.CheckState.Checked.value)

    def _on_llm_model_changed(self, index):
        S.LLM_MODEL = self.llm_model_combo.itemData(index)

    def _on_llm_prefix_changed(self):
        S.LLM_PREFIX = self.llm_prefix_edit.toPlainText()

    def _select_recordings_folder(self):
        """Open folder selection dialog for recordings."""
        folder = QFileDialog.getExistingDirectory(
            self, "Select Recordings Folder", S.RECORDINGS_DIR
        )
        if folder:
            S.set('RECORDINGS_DIR', folder)
            self.folder_label.setText(folder)

    def _revert_recordings_folder(self):
        """Revert recordings folder to default."""
        S.set('RECORDINGS_DIR', DEFAULT_RECORDINGS_DIR)
        self.folder_label.setText(DEFAULT_RECORDINGS_DIR)

    def _open_settings_folder(self):
        rp.open_file_with_default_application(_VOICETHING_DIR)

    def _select_whisper_model(self):
        """Open model selection dialog from preferences via parent's method."""
        # Use parent's show_model_dialog to get the same chimes and behavior
        if self.parent() and hasattr(self.parent(), 'show_model_dialog'):
            self.parent().show_model_dialog()

    def _revert_to_defaults(self):
        """Revert all settings to defaults and re-open dialog."""
        S.update(DEFAULTS)
        self.reverted_to_defaults = True
        self.reject()  # Close, parent will re-open with fresh values from S


    def keyPressEvent(self, e):
        key = e.key()
        if key == Qt.Key.Key_Escape:
            self.reject()
        elif key in (Qt.Key.Key_Return, Qt.Key.Key_Enter):
            self.accept()
        elif key == Qt.Key.Key_P and self._show_preset_dialog:
            self._show_preset_dialog()
        elif Qt.Key.Key_1 <= key <= Qt.Key.Key_9 and not self.piano.hasFocus():
            # Number keys 1-9 select themes (when piano not focused)
            idx = key - Qt.Key.Key_1
            if idx < self.chime_theme_combo.count():
                self.chime_theme_combo.setCurrentIndex(idx)
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
        title.setStyleSheet(title_style(14))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)

        msg = QLabel(PERMISSION_ERROR_MSG)
        msg.setStyleSheet("color: rgba(255,255,255,0.9); font-size: 13px;")
        msg.setWordWrap(True)
        layout.addWidget(msg)

        layout.addWidget(make_close_btn(on_click=self.accept))

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
        f"QTextEdit {{ color: {TEXT_PRIMARY}; font-size: 11px; font-family: Menlo, monospace; "
        f"{PANEL_BG_FLAT_CSS} padding: 8px; }}" + SCROLLBAR_CSS
    )

    def __init__(self, selectable=True, parent=None):
        super().__init__(parent)
        self.setReadOnly(True)
        self.paragraphs = None  # Set externally for paragraph-aware context menu
        if not selectable:
            self.setTextInteractionFlags(Qt.TextInteractionFlag.NoTextInteraction)
        self.setStyleSheet(self.STYLE)

    def keyPressEvent(self, e):
        # Pass shortcut keys to parent window (only without modifiers, so Cmd+C still copies)
        no_mods = e.modifiers() == Qt.KeyboardModifier.NoModifier
        if no_mods and e.key() in (Qt.Key.Key_Space, Qt.Key.Key_Escape, Qt.Key.Key_X, Qt.Key.Key_C, Qt.Key.Key_L, Qt.Key.Key_F,
                       Qt.Key.Key_S, Qt.Key.Key_H, Qt.Key.Key_R, Qt.Key.Key_E, Qt.Key.Key_W, Qt.Key.Key_O, Qt.Key.Key_T, Qt.Key.Key_M, Qt.Key.Key_Question):
            self.window().keyPressEvent(e)
        else:
            super().keyPressEvent(e)

    def contextMenuEvent(self, e):
        # Auto-select paragraph under cursor if nothing selected (only when paragraphs mode)
        if self.paragraphs is not None and not self.textCursor().hasSelection():
            self.setFocus()
            cursor = self.cursorForPosition(e.pos())
            block_num = cursor.blockNumber()
            # Each transcription is a <p> tag, map block to paragraph index
            # Blocks: p0, hr, p1, hr, p2... so paragraph i is at block 2*i
            para_idx = block_num // 2
            if 0 <= para_idx < len(self.paragraphs):
                cursor.movePosition(cursor.MoveOperation.StartOfBlock)
                cursor.movePosition(cursor.MoveOperation.EndOfBlock, cursor.MoveMode.KeepAnchor)
                self.setTextCursor(cursor)

        menu = QMenu(self)
        menu.setStyleSheet(get_menu_css())
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

    @staticmethod
    def _btn_style():
        return (
            f"QPushButton {{ background: {STYLE.transcription_row_btn_bg}; border: none; border-radius: 4px; }}"
            f"QPushButton:hover {{ background: {STYLE.transcription_row_btn_hover}; }}"
            f"QPushButton:pressed {{ background: {STYLE.transcription_row_btn_pressed}; }}"
        )

    def __init__(self, text, dimmed=False, show_deramble=False, other_text=None, is_raw=False, parent=None):
        super().__init__(parent)
        self.text = text
        self.other_text = other_text  # The other version for diff comparison
        self.is_raw = is_raw  # True if this is the raw (pre-LLM) text
        self.dimmed = dimmed
        self._buttons = []  # Store button references for style updates

        layout = QHBoxLayout(self)
        layout.setContentsMargins(8, 4, 8, 4)
        layout.setSpacing(4)

        self.label = QLabel()
        self.label.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
        self.label.setCursor(Qt.CursorShape.IBeamCursor)
        self.label.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.label.customContextMenuRequested.connect(self._show_context_menu)
        self.label.installEventFilter(self)
        self._update_label_style()
        self.label.setWordWrap(True)
        self.label.setTextFormat(Qt.TextFormat.RichText)
        layout.addWidget(self.label, 1)

        # Set initial HTML (unhighlighted)
        self._set_diff_highlight(False)

        # Icons styled for current theme
        if show_deramble:
            deramble_btn = QPushButton()
            deramble_btn.setFixedSize(24, 24)
            deramble_btn.setIconSize(QSize(16, 16))
            deramble_btn.setToolTip("De-ramble with LLM")
            deramble_btn.clicked.connect(lambda: self.deramble_clicked.emit(self.text))
            deramble_btn.icon_name = ACTIONS_BY_ID["llm"][2]
            layout.addWidget(deramble_btn, 0, Qt.AlignmentFlag.AlignTop)
            self._buttons.append(deramble_btn)

        copy_btn = QPushButton()
        copy_btn.setFixedSize(24, 24)
        copy_btn.setIconSize(QSize(16, 16))
        copy_btn.setToolTip("Copy to clipboard")
        copy_btn.clicked.connect(lambda: self.clicked.emit(self.text))
        copy_btn.icon_name = ACTIONS_BY_ID["copy"][2]
        layout.addWidget(copy_btn, 0, Qt.AlignmentFlag.AlignTop)
        self._buttons.append(copy_btn)

        # Apply initial button styles
        self._update_button_styles()
        self._update_bg(False)

    def _update_label_style(self):
        """Update label text color from current style."""
        text_color = STYLE.transcription_text_dimmed if self.dimmed else STYLE.transcription_text
        self.base_style = f"font-size: 11px; color: {text_color};"
        self.label.setStyleSheet(self.base_style)

    def _update_button_styles(self):
        """Update button styles and icons from current style."""
        btn_style = self._btn_style()
        icon_color = STYLE.icon_color_muted
        for btn in self._buttons:
            btn.setStyleSheet(btn_style)
            btn.setIcon(load_icon(btn.icon_name, color=icon_color))

    def update_style(self):
        """Called when global style changes - refresh all style-dependent properties."""
        self._update_label_style()
        self._update_button_styles()
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

    def set_border_radius(self, top=0, bottom=0):
        """Set rounded corners for top-left/top-right and bottom-left/bottom-right."""
        self._border_radius_top = top
        self._border_radius_bottom = bottom
        self._update_bg(False)

    def _update_bg(self, hovered):
        bg = STYLE.transcription_row_hover if hovered else "transparent"
        top = getattr(self, '_border_radius_top', 0)
        bottom = getattr(self, '_border_radius_bottom', 0)
        radius = f"border-top-left-radius: {top}px; border-top-right-radius: {top}px; border-bottom-left-radius: {bottom}px; border-bottom-right-radius: {bottom}px;"
        self.setStyleSheet(f"TranscriptionRow {{ background: {bg}; {radius} }}")

    def enterEvent(self, event):
        self._update_bg(True)
        self.hover_changed.emit(True)
        super().enterEvent(event)

    def leaveEvent(self, event):
        self._update_bg(False)
        self.hover_changed.emit(False)
        super().leaveEvent(event)

    def eventFilter(self, obj, event):
        if obj == self.label:
            if event.type() == event.Type.MouseButtonPress and event.button() == Qt.MouseButton.LeftButton:
                self._press_global_pos = event.globalPosition().toPoint()
            elif event.type() == event.Type.MouseButtonRelease and event.button() == Qt.MouseButton.LeftButton:
                if hasattr(self, '_press_global_pos'):
                    delta = event.globalPosition().toPoint() - self._press_global_pos
                    if abs(delta.x()) + abs(delta.y()) < 5 and not self.label.hasSelectedText():
                        self.clicked.emit(self.text)
                    del self._press_global_pos
        return super().eventFilter(obj, event)

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

    def _show_context_menu(self, pos):
        menu = QMenu(self)
        menu.setStyleSheet(get_menu_css())
        if self.label.hasSelectedText():
            copy_action = menu.addAction("Copy")
            copy_action.triggered.connect(lambda: QApplication.clipboard().setText(self.label.selectedText()))
        select_all = menu.addAction("Select All")
        select_all.triggered.connect(lambda: self.label.setSelection(0, len(self.label.text())))
        menu.exec(self.label.mapToGlobal(pos))


class TranscriptionItem(QFrame):
    """Single transcription entry with one or two rows."""
    copy_clicked = pyqtSignal(str)
    deramble_clicked = pyqtSignal(int, str)  # (index, raw_text)

    def __init__(self, raw_text, processed_text, index, audio_path=None, parent=None):
        super().__init__(parent)
        self.index = index
        self.audio_path = audio_path
        self.diff_rows = []  # Rows that need coordinated highlighting
        self.first_row = None

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
            self.first_row = raw_row
        else:
            row = TranscriptionRow(raw_text, dimmed=False, show_deramble=True)
            row.clicked.connect(self.copy_clicked.emit)
            row.deramble_clicked.connect(lambda t: self.deramble_clicked.emit(self.index, t))
            layout.addWidget(row)
            self.first_row = row

        self.setStyleSheet("TranscriptionItem { border-bottom: 1px solid rgba(255,255,255,0.1); }")

    def set_top_radius(self, radius):
        """Set rounded top corners on the first row."""
        if self.first_row:
            self.first_row.set_border_radius(top=radius)

    def _on_hover_changed(self, hovered):
        """When any row is hovered, highlight diff text in all rows (not row background)."""
        for row in self.diff_rows:
            row.set_diff_highlight(hovered)

    def update_style(self):
        """Update style on all child rows."""
        for row in self.diff_rows:
            row.update_style()
        if self.first_row and self.first_row not in self.diff_rows:
            self.first_row.update_style()


class TranscriptionList(QScrollArea):
    """Scrollable list of transcription items."""
    copy_requested = pyqtSignal(str)
    deramble_requested = pyqtSignal(int, str)  # (index, raw_text)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWidgetResizable(True)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.item_count = 0

        self.container = QWidget()
        self.container.setStyleSheet("background: transparent;")
        self._layout = QVBoxLayout(self.container)
        self._layout.setContentsMargins(0, 0, 0, 0)
        self._layout.setSpacing(0)
        self._layout.addStretch()
        self.setWidget(self.container)
        self._apply_style()

    def _apply_style(self):
        css = (
            f"QScrollArea {{ background: {STYLE.transcription_panel_bg}; "
            f"border: 1px solid {STYLE.transcription_panel_border}; border-radius: 8px; }}"
            + SCROLLBAR_CSS
        )
        self.setStyleSheet(css)
        # Update all child items' styles
        for i in range(self._layout.count() - 1):  # Skip the stretch
            item = self._layout.itemAt(i)
            if item and item.widget():
                item.widget().update_style()

    def add_transcription(self, raw_text, processed_text, audio_path=None):
        index = self.item_count
        self.item_count += 1
        item = TranscriptionItem(raw_text, processed_text, index, audio_path=audio_path)
        item.copy_clicked.connect(self.copy_requested.emit)
        item.deramble_clicked.connect(self.deramble_requested.emit)
        # Insert before the stretch
        self._layout.insertWidget(self._layout.count() - 1, item)
        # Scroll to bottom
        QTimer.singleShot(10, lambda: self.verticalScrollBar().setValue(
            self.verticalScrollBar().maximum()))

    def update_transcription(self, index, raw_text, processed_text, audio_path=None):
        """Replace transcription at index with updated raw+processed version."""
        # Find the widget at this index (widgets are in order, stretch is last)
        if index < self._layout.count() - 1:
            old_item = self._layout.takeAt(index)
            if old_item and old_item.widget():
                # Preserve audio_path from old item if not provided
                if audio_path is None:
                    audio_path = getattr(old_item.widget(), 'audio_path', None)
                old_item.widget().deleteLater()
            new_item = TranscriptionItem(raw_text, processed_text, index, audio_path=audio_path)
            new_item.copy_clicked.connect(self.copy_requested.emit)
            new_item.deramble_clicked.connect(self.deramble_requested.emit)
            self._layout.insertWidget(index, new_item)
            # Scroll to bottom after update
            QTimer.singleShot(10, lambda: self.verticalScrollBar().setValue(
                self.verticalScrollBar().maximum()))

    def clear(self):
        while self._layout.count() > 1:  # Keep the stretch
            item = self._layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        self.item_count = 0


class Mini7Segment(QWidget):
    """Mini 3-digit 7-segment display for program number selection."""

    # 7-segment patterns: top, top-right, bottom-right, bottom, bottom-left, top-left, middle
    SEGMENTS = {
        '0': (1,1,1,1,1,1,0), '1': (0,1,1,0,0,0,0), '2': (1,1,0,1,1,0,1), '3': (1,1,1,1,0,0,1),
        '4': (0,1,1,0,0,1,1), '5': (1,0,1,1,0,1,1), '6': (1,0,1,1,1,1,1), '7': (1,1,1,0,0,0,0),
        '8': (1,1,1,1,1,1,1), '9': (1,1,1,1,0,1,1), '-': (0,0,0,0,0,0,1), ' ': (0,0,0,0,0,0,0),
    }

    def __init__(self, value=0, color=None):
        super().__init__()
        self.value = value
        self.color = color or ICON_COLOR_DARK
        self.setFixedSize(53, 22)  # 3 digits * (14+3) + padding

    def set_value(self, val):
        self.value = val
        self.update()

    def set_color(self, color):
        self.color = color
        self.update()

    def paintEvent(self, event):
        from PyQt6.QtGui import QPainter, QPen, QColor
        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)

        # Format value as 3 digits
        text = f"{self.value:3d}" if self.value is not None else "---"
        text = text[-3:]  # Last 3 chars

        # Draw each digit
        digit_w, digit_h = 14, 18
        seg_thick = 2
        gap = 3  # Spacing between digits

        for i, ch in enumerate(text):
            x_off = i * (digit_w + gap) + 2
            y_off = 2
            segs = self.SEGMENTS.get(ch, self.SEGMENTS[' '])

            # Segment positions (relative to digit origin)
            # Format: (x1, y1, x2, y2) for each segment
            seg_coords = [
                (2, 0, digit_w-2, 0),                    # top
                (digit_w, 2, digit_w, digit_h//2-1),     # top-right
                (digit_w, digit_h//2+1, digit_w, digit_h-2),  # bottom-right
                (2, digit_h, digit_w-2, digit_h),       # bottom
                (0, digit_h//2+1, 0, digit_h-2),        # bottom-left
                (0, 2, 0, digit_h//2-1),                # top-left
                (2, digit_h//2, digit_w-2, digit_h//2), # middle
            ]

            for j, on in enumerate(segs):
                if on:
                    color = self.color if isinstance(self.color, QColor) else QColor(self.color)
                    p.setPen(QPen(color, seg_thick, Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap))
                else:
                    p.setPen(QPen(QColor(60, 60, 60, 80), seg_thick, Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap))
                x1, y1, x2, y2 = seg_coords[j]
                p.drawLine(x_off + x1, y_off + y1, x_off + x2, y_off + y2)


class TimerWidget(QWidget):
    """Timer display - flat or LCD style depending on STYLE.timer_use_lcd."""

    def __init__(self, seg_font):
        super().__init__()
        self.seg_font = seg_font
        self.text = "0:00.0"
        self.opacity = 0.3  # 0.3 for idle, 0.9 for recording
        self.setMinimumSize(STYLE.timer_panel_size[0] + 20, 50)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

    def set_text(self, text):
        self.text = text
        self.update()

    def set_opacity(self, opacity):
        self.opacity = opacity
        self.update()

    def paintEvent(self, event):
        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)
        w, h = self.width(), self.height()
        font = QFont(self.seg_font, STYLE.timer_font_size)
        p.setFont(font)

        if STYLE.timer_use_lcd:
            self._paint_lcd(p, w, h)
        else:
            self._paint_flat(p, w, h)

    def _paint_flat(self, p, w, h):
        """Simple centered text with opacity."""
        color = STYLE.timer_color
        alpha = int(255 * self.opacity)
        p.setPen(QColor(color.red(), color.green(), color.blue(), alpha))
        p.drawText(self.rect(), Qt.AlignmentFlag.AlignCenter, self.text)

    def _paint_lcd(self, p, w, h):
        """Recessed LCD panel with ghost segments and glow."""
        panel_w, panel_h = STYLE.timer_panel_size
        panel_x = (w - panel_w) // 2
        panel_y = (h - panel_h) // 2
        panel_rect = self.rect().adjusted(panel_x, panel_y, panel_x - w + panel_w, panel_y - h + panel_h)

        # Recessed LCD panel background
        panel_grad = QLinearGradient(0, panel_rect.top(), 0, panel_rect.bottom())
        panel_grad.setColorAt(0, QColor(20, 35, 50))
        panel_grad.setColorAt(0.3, QColor(15, 28, 42))
        panel_grad.setColorAt(1, QColor(10, 22, 35))
        p.setBrush(QBrush(panel_grad))
        p.setPen(Qt.PenStyle.NoPen)
        p.drawRoundedRect(panel_rect, 6, 6)

        # Inner shadow
        shadow_grad = QLinearGradient(0, panel_rect.top(), 0, panel_rect.top() + 6)
        shadow_grad.setColorAt(0, QColor(0, 0, 0, 120))
        shadow_grad.setColorAt(1, QColor(0, 0, 0, 0))
        p.setBrush(QBrush(shadow_grad))
        p.drawRoundedRect(panel_rect.adjusted(0, 0, 0, -panel_rect.height() + 8), 6, 6)

        # Bottom highlight
        p.setPen(QPen(QColor(80, 120, 160, 80), 1))
        p.drawLine(panel_rect.left() + 6, panel_rect.bottom(),
                   panel_rect.right() - 6, panel_rect.bottom())

        # Panel border
        p.setBrush(Qt.BrushStyle.NoBrush)
        p.setPen(QPen(QColor(30, 50, 70), 1))
        p.drawRoundedRect(panel_rect, 6, 6)

        # Ghost segments
        p.setPen(QColor(60, 180, 220, 25))
        ghost = ''.join('8' if c.isdigit() else c for c in self.text)
        p.drawText(panel_rect, Qt.AlignmentFlag.AlignCenter, ghost)

        # Active segments with glow
        color = STYLE.timer_color
        accent_alpha = int(255 * self.opacity)
        if self.opacity > 0.5:
            for offset in [(0, 0), (-1, 0), (1, 0), (0, -1), (0, 1)]:
                p.setPen(QColor(color.red(), color.green(), color.blue(), int(accent_alpha * 0.3)))
                p.drawText(panel_rect.adjusted(offset[0], offset[1], offset[0], offset[1]),
                          Qt.AlignmentFlag.AlignCenter, self.text)
        p.setPen(QColor(color.red(), color.green(), color.blue(), accent_alpha))
        p.drawText(panel_rect, Qt.AlignmentFlag.AlignCenter, self.text)


class _WaveformInner(QWidget):
    """Inner widget that draws just the waveform polygon."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.samples = np.array([])
        self.display_max = 0.01
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

    def paintEvent(self, event):
        n = len(self.samples)
        if n < 1:
            return

        p = QPainter(self)
        # NOTE: Do NOT enable Antialiasing - causes severe performance issues
        w, h = self.width(), self.height()
        cy = h / 2

        # Compute peaks
        abs_samples = np.abs(self.samples)
        n_bins = w
        indices = np.linspace(0, n, n_bins + 1).astype(int)
        peaks = np.array([abs_samples[indices[i]:indices[i+1]].max() if indices[i] < indices[i+1] else 0
                         for i in range(n_bins)])

        # Scale to widget height
        y_scaled = (peaks / self.display_max) * h / 2 * 0.85

        # Build polygon
        x_coords = np.arange(w)
        top_y = cy - y_scaled
        bottom_y = cy + y_scaled[::-1]
        points = [QPointF(x, y) for x, y in zip(x_coords, top_y)]
        points += [QPointF(x, y) for x, y in zip(x_coords[::-1], bottom_y)]
        polygon = QPolygonF(points)

        # Draw waveform - gradient with alpha fade at edges if glow enabled
        color = STYLE.waveform_color
        if STYLE.waveform_glow:
            wave_grad = QLinearGradient(0, cy - h/2 * 0.85, 0, cy + h/2 * 0.85)
            # Fade to transparent at edges, full color in middle
            edge = QColor(color.red(), color.green(), color.blue(), 60)
            mid = QColor(color.red(), color.green(), color.blue(), 255)
            wave_grad.setColorAt(0, edge)
            wave_grad.setColorAt(0.3, mid)
            wave_grad.setColorAt(0.7, mid)
            wave_grad.setColorAt(1, edge)
            p.setBrush(QBrush(wave_grad))
        else:
            p.setBrush(color)
        p.setPen(Qt.PenStyle.NoPen)
        p.drawPolygon(polygon)

        # Center line (for flat style)
        if STYLE.waveform_center_line:
            p.setPen(QPen(STYLE.waveform_center_line, 1))
            p.drawLine(0, int(cy), w, int(cy))


class WaveformWidget(QWidget):
    """Waveform display - flat or with glow depending on STYLE.waveform_glow."""

    def __init__(self):
        super().__init__()
        self.samples = np.array([])
        self.display_max = 0.01
        self.setMinimumHeight(40)
        self.setMaximumHeight(133)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self._inner = _WaveformInner(self)
        self._glow = None
        self._update_glow()

    def _update_glow(self):
        """Apply or remove glow effect based on style."""
        if STYLE.waveform_glow:
            if not self._glow:
                self._glow = QGraphicsDropShadowEffect(self)
                self._glow.setOffset(0, 0)
            self._glow.setBlurRadius(STYLE.waveform_glow_radius)
            color = STYLE.waveform_color
            self._glow.setColor(QColor(color.red(), color.green(), color.blue(), STYLE.waveform_glow_alpha))
            self._inner.setGraphicsEffect(self._glow)
        else:
            self._inner.setGraphicsEffect(None)
            self._glow = None

    def sizeHint(self):
        return QSize(200, 100)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self._inner.setGeometry(self.rect())

    def set_samples(self, samples):
        max_samples = WAVEFORM_DURATION_SECONDS * SAMPLE_RATE
        self.samples = samples[-max_samples:] if len(samples) > max_samples else samples
        if len(self.samples) > 0:
            self.display_max += (max(np.max(np.abs(self.samples)), 0.01) - self.display_max) * 0.04
        self._inner.samples = self.samples
        self._inner.display_max = self.display_max
        self._inner.update()
        self.update()

    def _draw_infinite_grid(self, p, w, h):
        """Draw Blender-style infinite grid that fades based on zoom level."""
        zoom = self.display_max
        base_spacing = 0.00375  # Smaller = more lines (4x original density)
        log_zoom = math.log2(zoom / base_spacing) if zoom > 0 else 0
        grid_level = math.floor(log_zoom)
        fade = log_zoom - grid_level

        # Draw two grid levels with crossfade (aqua-themed colors)
        for level_offset in range(2):
            level = grid_level + level_offset
            spacing = base_spacing * (2 ** level)
            alpha = int(80 * (1 - fade)) if level_offset == 0 else int(80 * fade)
            if alpha < 10:
                continue

            p.setPen(QPen(QColor(20, 50, 100, alpha), 1))
            pixels_per_unit = (h / 2) / max(zoom, 0.001)
            pixel_spacing = spacing * pixels_per_unit

            if pixel_spacing > 5:
                cy = h / 2
                y = cy - pixel_spacing
                while y > 0:
                    p.drawLine(0, int(y), w, int(y))
                    y -= pixel_spacing
                y = cy + pixel_spacing
                while y < h:
                    p.drawLine(0, int(y), w, int(y))
                    y += pixel_spacing

        # Vertical grid - one section per second of audio duration
        p.setPen(QPen(QColor(20, 50, 100, 50), 1))
        num_sections = WAVEFORM_DURATION_SECONDS
        for i in range(1, num_sections):  # num_sections-1 internal lines
            p.drawLine(int(w * i / num_sections), 0, int(w * i / num_sections), h)

    def paintEvent(self, event):
        if not STYLE.waveform_panel:
            return  # Transparent background for flat styles
        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)
        w, h = self.width(), self.height()
        cy = h / 2
        rect = self.rect()

        # Delegate to style's paint method (or fallback for winamp which isn't a style yet)
        if STYLE.waveform_panel == "winamp":
            self._paint_winamp_panel(p, rect, w, h, cy)
        else:
            STYLE.paint_waveform_panel(p, rect, w, h, cy)

    def _paint_aqua_panel(self, p, rect, w, h, cy):
        """Aqua-style blue panel background - classic macOS look."""
        panel_grad = QLinearGradient(0, 0, 0, h)
        panel_grad.setColorAt(0, QColor(140, 180, 220))
        panel_grad.setColorAt(0.3, QColor(80, 140, 200))
        panel_grad.setColorAt(0.7, QColor(50, 110, 180))
        panel_grad.setColorAt(1, QColor(30, 80, 150))
        p.setBrush(QBrush(panel_grad))
        p.setPen(Qt.PenStyle.NoPen)
        p.drawRoundedRect(rect, 8, 8)

        # Glassy top highlight
        highlight = QLinearGradient(0, 0, 0, h * 0.4)
        highlight.setColorAt(0, QColor(255, 255, 255, 120))
        highlight.setColorAt(0.5, QColor(255, 255, 255, 40))
        highlight.setColorAt(1, QColor(255, 255, 255, 0))
        p.setBrush(QBrush(highlight))
        p.drawRoundedRect(rect.adjusted(2, 2, -2, -int(h * 0.6)), 6, 6)

        # Draw infinite grid
        self._draw_infinite_grid(p, w, h)

        # Engraved shadows
        for grad, adj in [
            (QLinearGradient(0, 0, 0, 12), rect.adjusted(1, 1, -1, -h + 14)),
            (QLinearGradient(0, 0, 10, 0), rect.adjusted(1, 1, -w + 12, -1)),
            (QLinearGradient(w, 0, w - 10, 0), rect.adjusted(w - 12, 1, -1, -1)),
        ]:
            grad.setColorAt(0, QColor(0, 0, 0, 50 if grad.start().x() else 100))
            grad.setColorAt(1, QColor(0, 0, 0, 0))
            p.setBrush(QBrush(grad))
            p.setPen(Qt.PenStyle.NoPen)
            p.drawRoundedRect(adj, 7, 7)

        # Panel border
        p.setBrush(Qt.BrushStyle.NoBrush)
        p.setPen(QPen(QColor(20, 50, 100), 1.5))
        p.drawRoundedRect(rect, 8, 8)

        # Center line
        p.setPen(QPen(QColor(20, 60, 120, 150), 1))
        p.drawLine(0, int(cy), w, int(cy))

    def _paint_dark_panel(self, p, rect, w, h, cy):
        """Dark gradient panel with cyan grid."""
        # Dark gradient background
        panel_grad = QLinearGradient(0, 0, 0, h)
        panel_grad.setColorAt(0, QColor(32, 36, 46, 180))
        panel_grad.setColorAt(1, QColor(26, 30, 40, 180))
        p.setBrush(QBrush(panel_grad))
        p.setPen(Qt.PenStyle.NoPen)
        p.drawRoundedRect(rect, 8, 8)

        # Subtle cyan grid lines
        p.setPen(QPen(QColor(100, 200, 255, 12), 1))
        for i in range(1, 4):
            y = int(h * i / 4)
            p.drawLine(0, y, w, y)
        for i in range(1, 8):
            x = int(w * i / 8)
            p.drawLine(x, 0, x, h)

        # Panel inner shadow
        shadow_grad = QLinearGradient(0, 0, 0, 8)
        shadow_grad.setColorAt(0, QColor(0, 0, 0, 50))
        shadow_grad.setColorAt(1, QColor(0, 0, 0, 0))
        p.setBrush(QBrush(shadow_grad))
        p.setPen(Qt.PenStyle.NoPen)
        p.drawRoundedRect(rect.adjusted(0, 0, 0, -h + 10), 8, 8)

        # Panel border
        p.setBrush(Qt.BrushStyle.NoBrush)
        p.setPen(QPen(QColor(50, 55, 65, 150), 1))
        p.drawRoundedRect(rect, 8, 8)

    def _paint_aero_panel(self, p, rect, w, h, cy):
        """Frutiger Aero glassy panel with blue tint."""
        # Glass gradient background
        panel_grad = QLinearGradient(0, 0, 0, h)
        panel_grad.setColorAt(0, QColor(200, 220, 240, 230))
        panel_grad.setColorAt(0.3, QColor(180, 210, 235, 220))
        panel_grad.setColorAt(0.7, QColor(160, 200, 230, 210))
        panel_grad.setColorAt(1, QColor(140, 180, 220, 200))
        p.setBrush(QBrush(panel_grad))
        p.setPen(Qt.PenStyle.NoPen)
        p.drawRoundedRect(rect, 4, 4)

        # Top glossy highlight
        highlight = QLinearGradient(0, 0, 0, h * 0.4)
        highlight.setColorAt(0, QColor(255, 255, 255, 150))
        highlight.setColorAt(0.5, QColor(255, 255, 255, 50))
        highlight.setColorAt(1, QColor(255, 255, 255, 0))
        p.setBrush(QBrush(highlight))
        p.drawRoundedRect(rect.adjusted(1, 1, -1, -int(h * 0.6)), 3, 3)

        # Subtle grid
        p.setPen(QPen(QColor(6, 137, 228, 20), 1))
        for i in range(1, 4):
            y = int(h * i / 4)
            p.drawLine(0, y, w, y)

        # Panel border
        p.setBrush(Qt.BrushStyle.NoBrush)
        p.setPen(QPen(QColor(136, 136, 136), 1))
        p.drawRoundedRect(rect, 4, 4)

        # Center line
        p.setPen(QPen(QColor(6, 137, 228, 60), 1))
        p.drawLine(0, int(cy), w, int(cy))

    def _paint_winamp_panel(self, p, rect, w, h, cy):
        """Winamp-style dark panel with green accents."""
        # Deep dark background
        p.setBrush(QColor(26, 26, 26))
        p.setPen(Qt.PenStyle.NoPen)
        p.drawRect(rect)

        # Subtle scan lines effect
        p.setPen(QPen(QColor(0, 0, 0, 30), 1))
        for y in range(0, h, 2):
            p.drawLine(0, y, w, y)

        # Green grid lines
        p.setPen(QPen(QColor(0, 255, 0, 25), 1))
        for i in range(1, 4):
            y = int(h * i / 4)
            p.drawLine(0, y, w, y)
        for i in range(1, 8):
            x = int(w * i / 8)
            p.drawLine(x, 0, x, h)

        # Win95 beveled border (inset)
        # Top/left shadow
        p.setPen(QPen(QColor(0, 0, 0), 1))
        p.drawLine(rect.left(), rect.top(), rect.right(), rect.top())
        p.drawLine(rect.left(), rect.top(), rect.left(), rect.bottom())
        # Bottom/right highlight
        p.setPen(QPen(QColor(80, 80, 80), 1))
        p.drawLine(rect.right(), rect.top(), rect.right(), rect.bottom())
        p.drawLine(rect.left(), rect.bottom(), rect.right(), rect.bottom())

        # Center line in green
        p.setPen(QPen(QColor(0, 255, 0, 40), 1))
        p.drawLine(0, int(cy), w, int(cy))

    def _paint_vaporwave_panel(self, p, rect, w, h, cy):
        """Vaporwave-style dark purple panel with pink/cyan gradient accents."""
        # Dark purple background (#300350 - russian violet)
        p.setBrush(QColor(48, 3, 80))
        p.setPen(Qt.PenStyle.NoPen)
        p.drawRect(rect)

        # Horizontal pink-to-cyan gradient at bottom third
        grad_rect = rect.adjusted(0, int(h * 0.6), 0, 0)
        vapor_grad = QLinearGradient(0, grad_rect.top(), w, grad_rect.bottom())
        vapor_grad.setColorAt(0, QColor(255, 113, 206, 50))    # Hot pink
        vapor_grad.setColorAt(0.5, QColor(185, 103, 255, 35))  # Purple
        vapor_grad.setColorAt(1, QColor(1, 205, 254, 45))      # Cyan
        p.setBrush(QBrush(vapor_grad))
        p.drawRect(rect)

        # Subtle scanlines for retro effect
        p.setPen(QPen(QColor(255, 113, 206, 15), 1))
        for y_line in range(0, h, 4):
            p.drawLine(0, y_line, w, y_line)

        # Pink border glow
        p.setBrush(Qt.BrushStyle.NoBrush)
        p.setPen(QPen(QColor(255, 113, 206, 100), 2))
        p.drawRect(rect.adjusted(1, 1, -1, -1))
        p.setPen(QPen(QColor(255, 113, 206, 50), 1))
        p.drawRect(rect)

        # Center line in pink
        p.setPen(QPen(QColor(255, 113, 206, 40), 1))
        p.drawLine(0, int(cy), w, int(cy))

    def _paint_win95_panel(self, p, rect, w, h, cy):
        """Windows 95 style - black recessed panel with inset bevel."""
        # Black background
        p.setBrush(QColor(0, 0, 0))
        p.setPen(Qt.PenStyle.NoPen)
        p.drawRect(rect)

        # Inset bevel - dark on top/left, light on bottom/right
        # Top edge - dark shadow
        p.setPen(QPen(QColor(0, 0, 0), 1))
        p.drawLine(rect.left(), rect.top(), rect.right(), rect.top())
        # Left edge - dark shadow
        p.drawLine(rect.left(), rect.top(), rect.left(), rect.bottom())

        # Inner dark gray
        p.setPen(QPen(QColor(128, 128, 128), 1))
        p.drawLine(rect.left() + 1, rect.top() + 1, rect.right() - 1, rect.top() + 1)
        p.drawLine(rect.left() + 1, rect.top() + 1, rect.left() + 1, rect.bottom() - 1)

        # Bottom edge - white/light highlight
        p.setPen(QPen(QColor(255, 255, 255), 1))
        p.drawLine(rect.left(), rect.bottom(), rect.right(), rect.bottom())
        p.drawLine(rect.right(), rect.top(), rect.right(), rect.bottom())

        # Inner light gray
        p.setPen(QPen(QColor(223, 223, 223), 1))
        p.drawLine(rect.left() + 1, rect.bottom() - 1, rect.right() - 1, rect.bottom() - 1)
        p.drawLine(rect.right() - 1, rect.top() + 1, rect.right() - 1, rect.bottom() - 1)

        # Center line in dim green (optional subtle guide)
        p.setPen(QPen(QColor(0, 64, 0, 60), 1))
        p.drawLine(0, int(cy), w, int(cy))


class VoiceThingWindow(DraggableResizableMixin, QWidget):
    hide_signal = pyqtSignal()
    toggle_signal = pyqtSignal()
    focus_signal = pyqtSignal()
    paste_signal = pyqtSignal(str)
    add_transcription_signal = pyqtSignal(str, str, str)  # (raw_text, processed_text, audio_path)
    update_transcription_signal = pyqtSignal(int, str, str)  # (index, raw_text, processed_text)
    permission_error_signal = pyqtSignal()
    wake_word_signal = pyqtSignal(object)  # pre_buffer numpy array
    finish_signal = pyqtSignal()  # Signal to call _finish on main thread
    stop_signal = pyqtSignal()  # Signal to stop recording from wake word
    cancel_signal = pyqtSignal()  # Signal to cancel recording (double-tap held long)

    _paint_inset = 0

    def __init__(self):
        super().__init__()
        self._init_draggable()
        self.state = "idle"
        self._state_lock = threading.Lock()  # Protects state transitions from audio callback thread
        self.audio_chunks = []
        self.stream = None
        self.tee = TeeOutput()
        self.tee.__enter__()
        self.is_focused = False
        self.first_show = True
        self.last_audio_path = None
        self.last_transcription = None
        self.transcriptions = []  # List of (raw_text, processed_text, audio_path) tuples
        self.permission_error = False  # True if accessibility permission denied
        self._prev_app = None  # For restoring focus when toggling window
        # Non-settings instance state
        self.wake_word_engine = None  # Wake word engine instance (from wakeword module)

        self.setWindowTitle(APP_NAME)
        self._apply_window_flags(show=False)
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
        self.close_btn = TrafficLightButton("rgb(255, 95, 87)", "rgb(255, 120, 110)", "macos-close")
        self.close_btn.setToolTip("Close window")
        self.close_btn.clicked.connect(self.hide)
        status_row.addWidget(self.close_btn)
        self.small_btn = TrafficLightButton("rgb(255, 189, 46)", "rgb(255, 210, 80)", "macos-fullscreen")
        self.small_btn.setToolTip("Toggle small mode (E)")
        self.small_btn.clicked.connect(self.toggle_small_mode)
        status_row.addWidget(self.small_btn)
        # Warning button for permission errors (hidden by default)
        self.warning_btn = QPushButton()
        self.warning_btn.setFixedSize(20, 20)
        self.warning_btn.setIcon(load_icon("warning", color=ICON_COLOR_DARK))
        self.warning_btn.setIconSize(QSize(18, 18))
        self.warning_btn.setStyleSheet("QPushButton { background: transparent; border: none; }")
        self.warning_btn.setToolTip(PERMISSION_ERROR_TITLE)
        self.warning_btn.clicked.connect(self.show_permission_dialog)
        self.warning_btn.hide()
        status_row.addWidget(self.warning_btn)
        self.status_label = QLabel("Double-tap ⌥")
        self.status_label.setStyleSheet(title_style(14))
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        status_row.addWidget(self.status_label, 1)
        # Spacer to balance the window control buttons
        self.status_spacer = QWidget()
        self.status_spacer.setFixedWidth(28)
        status_row.addWidget(self.status_spacer)
        layout.addLayout(status_row)

        self.seg_font = seg_font
        # Timer row - timer is centered, pets float on top-left without affecting centering
        self.timer_row_widget = QWidget()
        timer_row = QHBoxLayout(self.timer_row_widget)
        timer_row.setContentsMargins(0, 0, 0, 0)
        timer_row.setSpacing(0)
        self.timer_label = TimerWidget(seg_font)
        timer_row.addWidget(self.timer_label, 1, Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.timer_row_widget)

        self.btn_row_widget = QWidget()
        self.btn_row = QHBoxLayout(self.btn_row_widget)
        self.btn_row.setContentsMargins(0, 0, 0, 0)
        self.btn_row.setSpacing(8)

        def make_btn(text, icon_name, handler):
            btn = QPushButton(text)
            # Dark icons for light Aqua buttons (embossed look)
            btn.setIcon(load_icon(icon_name, color=ICON_COLOR_DARK))
            btn.setIconSize(QSize(16, 16))
            btn.setStyleSheet(get_btn_css())
            btn.clicked.connect(handler)
            btn.setEnabled(False)
            btn.icon_name = icon_name  # Store for later icon color updates
            self.btn_row.addWidget(btn)
            return btn

        self.record_btn = make_btn("␣", "record", self.toggle_recording)
        self.record_btn.setToolTip("Start/stop recording")
        self.record_btn.setEnabled(True)
        self.cancel_btn = make_btn("X", "cancel", self.cancel_recording)
        self.cancel_btn.setToolTip("Cancel recording")
        self.retranscribe_btn = make_btn("Z", "retranscribe", self.retranscribe_latest)
        self.retranscribe_btn.setToolTip("Retranscribe latest with current model")
        self.simple_btn = make_btn("W", "plus", self.toggle_simple_mode)
        self.simple_btn.setToolTip("Toggle simple mode")
        self.simple_btn.setCheckable(True)
        self.simple_btn.setEnabled(True)
        self.copy_btn = make_btn("C", "copy", self.copy_transcription)
        self.copy_btn.setToolTip("Copy last transcription to clipboard")
        self.load_btn = make_btn("L", "disc", self.load_audio_file)
        self.load_btn.setToolTip("Load audio file to transcribe")
        self.load_btn.setEnabled(True)
        self.folder_btn = make_btn("F", "folder-open", self.open_folder)
        self.folder_btn.setToolTip("Open recordings folder")
        self.sound_btn = make_btn("S", "volume", self.toggle_sound)
        self.sound_btn.setToolTip("Toggle sound effects")
        self.sound_btn.setCheckable(True)
        self.sound_btn.setChecked(S.SOUND_ENABLED)
        self.sound_btn.setIcon(load_icon("volume" if S.SOUND_ENABLED else "volume-off",
                                         color=ICON_COLOR_LIGHT if S.SOUND_ENABLED else ICON_COLOR_DARK))
        self.sound_btn.setEnabled(True)
        self.eye_btn = make_btn("H", "eye", self.toggle_auto_hide)
        self.eye_btn.setToolTip("Toggle auto-minimize after transcription")
        self.eye_btn.setCheckable(True)
        self.eye_btn.setEnabled(True)
        self.llm_btn = make_btn("R", "robot", self.toggle_llm)
        self.llm_btn.setToolTip("Toggle LLM post-processing")
        self.llm_btn.setCheckable(True)
        self.llm_btn.setEnabled(True)
        self.wake_word_btn = make_btn("J", "ear", self.toggle_wake_word)
        self.wake_word_btn.setToolTip(f"Toggle wake word ({self._get_wake_word_display()})")
        self.wake_word_btn.setCheckable(True)
        self.wake_word_btn.setEnabled(True)
        self.enter_btn = make_btn("N", "enter", self.toggle_auto_enter)
        self.enter_btn.setToolTip("Toggle auto-enter after paste")
        self.enter_btn.setCheckable(True)
        self.enter_btn.setChecked(S.AUTO_ENTER)
        if S.AUTO_ENTER:
            self.enter_btn.setIcon(load_icon("enter", color=ICON_COLOR_LIGHT))
        self.enter_btn.setEnabled(True)
        self.tmux_btn = make_btn("U", "tmux", self.show_tmux_selection)
        self.tmux_btn.setToolTip("Select tmux pane target")
        self.tmux_btn.setCheckable(True)
        self.tmux_btn.setChecked(S.TMUX_MODE)
        if S.TMUX_MODE:
            self.tmux_btn.setIcon(load_icon("tmux", color=ICON_COLOR_LIGHT))
        self.tmux_btn.setEnabled(True)
        self.model_btn = make_btn("M", "mic", self.show_model_dialog)
        self.model_btn.setToolTip("Change Whisper model")
        self.model_btn.setEnabled(True)
        self.prefs_btn = make_btn("P", "settings", self.show_prefs)
        self.prefs_btn.setToolTip("Preferences")
        self.prefs_btn.setEnabled(True)
        self.help_btn = make_btn("?", "book", self.show_help)
        self.help_btn.setToolTip("Show help")
        self.help_btn.setEnabled(True)

        # Second button row for two-row mode
        self.btn_row2_widget = QWidget()
        self.btn_row2 = QHBoxLayout(self.btn_row2_widget)
        self.btn_row2.setContentsMargins(0, 0, 0, 0)
        self.btn_row2.setSpacing(8)
        self.btn_row2_widget.setVisible(False)

        # Store buttons for dynamic row assignment
        self.all_toolbar_buttons = [
            self.record_btn, self.cancel_btn, self.retranscribe_btn, self.simple_btn,
            self.copy_btn, self.load_btn, self.folder_btn, self.sound_btn,
            self.eye_btn, self.llm_btn, self.wake_word_btn, self.enter_btn,
            self.tmux_btn, self.model_btn, self.prefs_btn, self.help_btn,
        ]
        self.essential_buttons = {self.record_btn, self.cancel_btn, self.simple_btn,
                                  self.prefs_btn, self.help_btn}
        layout.addWidget(self.btn_row_widget)
        layout.addWidget(self.btn_row2_widget)

        # Key-to-button mapping for visual feedback
        self.key_buttons = {
            Qt.Key.Key_Space: self.record_btn, Qt.Key.Key_X: self.cancel_btn,
            Qt.Key.Key_Z: self.retranscribe_btn, Qt.Key.Key_W: self.simple_btn,
            Qt.Key.Key_C: self.copy_btn, Qt.Key.Key_L: self.load_btn,
            Qt.Key.Key_F: self.folder_btn, Qt.Key.Key_S: self.sound_btn,
            Qt.Key.Key_H: self.eye_btn, Qt.Key.Key_R: self.llm_btn,
            Qt.Key.Key_J: self.wake_word_btn, Qt.Key.Key_N: self.enter_btn,
            Qt.Key.Key_U: self.tmux_btn,
            Qt.Key.Key_M: self.model_btn, Qt.Key.Key_P: self.prefs_btn,
            Qt.Key.Key_Question: self.help_btn,
        }

        self.waveform = WaveformWidget()
        layout.addWidget(self.waveform)

        # Tab bar for Output/Transcriptions
        self.tab_row_widget = QWidget()
        tab_row = QHBoxLayout(self.tab_row_widget)
        tab_row.setSpacing(8)
        tab_row.setContentsMargins(0, 4, 0, 0)
        # Tab buttons with dark icons (light when checked)
        self.output_tab = QPushButton("O  Console")
        self.output_tab.setIconSize(QSize(14, 14))
        self.output_tab.setCheckable(True)
        self.output_tab.setChecked(True)
        self.output_tab.setStyleSheet(get_tab_css())
        self.output_tab.setToolTip("Show console output")
        self.output_tab.clicked.connect(lambda: self._switch_tab(0))
        self.output_tab.icon_name = "terminal"
        tab_row.addWidget(self.output_tab, 1)

        self.transcriptions_tab = QPushButton("T  Transcriptions")
        self.transcriptions_tab.setIconSize(QSize(14, 14))
        self.transcriptions_tab.setCheckable(True)
        self.transcriptions_tab.setStyleSheet(get_tab_css())
        self.transcriptions_tab.setToolTip("Show transcription history")
        self.transcriptions_tab.clicked.connect(lambda: self._switch_tab(1))
        self.transcriptions_tab.icon_name = "scroll"
        tab_row.addWidget(self.transcriptions_tab, 1)

        # Update tab icons based on checked state
        self._update_tab_icons()
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

        # Minimum size based on timer panel - just enough to show the display
        min_w = STYLE.timer_panel_size[0] + 40  # timer panel + padding for title bar buttons
        min_h = STYLE.timer_panel_size[1] + 55  # timer panel + title bar height
        self.setMinimumSize(min_w, min_h)
        self.resize(478, 460)
        self.hide_signal.connect(self._maybe_hide)
        self.toggle_signal.connect(self.toggle_recording)
        self.focus_signal.connect(self._focus_window)
        self.paste_signal.connect(self._do_paste)
        self.add_transcription_signal.connect(self._add_transcription)
        self.update_transcription_signal.connect(self._update_transcription)
        self.permission_error_signal.connect(self._on_permission_error)
        self.wake_word_signal.connect(lambda buf: self.start_recording(pre_buffer=buf))
        self.finish_signal.connect(self._finish)
        self.stop_signal.connect(self.stop_recording)
        self.cancel_signal.connect(self.cancel_recording)

        self.update_timer = QTimer()
        self.update_timer.timeout.connect(self._update_display)

        self.log_timer = QTimer()
        self.log_timer.timeout.connect(self._update_log)
        self.log_timer.start(100)  # Update log output 10x/sec

        self._setup_tray()

        # Register hooks for settings with UI side effects
        S.hooks['PET_TYPES'] = self._on_pet_types_changed
        S.hooks['AUTO_HIDE'] = self._on_auto_hide_changed
        S.hooks['SOUND_ENABLED'] = self._on_sound_changed
        S.hooks['LLM_ENABLED'] = self._on_llm_changed
        S.hooks['AUTO_ENTER'] = self._on_auto_enter_changed
        S.hooks['WAKE_WORD_ENABLED'] = self._on_wake_word_enabled_changed
        S.hooks['WAKEWORD_ENGINE'] = self._on_wake_word_settings_changed
        S.hooks['WAKEWORD_OPENWAKEWORD'] = self._on_wake_word_settings_changed
        S.hooks['WAKEWORD_MACOS'] = self._on_wake_word_settings_changed
        S.hooks['TMUX_MODE'] = self._on_tmux_mode_changed
        S.hooks['SIMPLE_MODE'] = self._on_simple_mode_changed
        S.hooks['ALWAYS_ON_TOP'] = self._on_always_on_top_setting_changed

        # Pet container - floats absolutely, not in any layout
        self.pet_container = PetContainer(self)
        self.pet_container.set_pets(S.PET_TYPES)
        self.pet_container.move(60, 10)  # After traffic lights
        self.pet_container.raise_()

        self._load_settings()
        self._update_ui()  # Initialize UI layout based on boot size

    def _get_action_handler(self, action_id):
        """Get the handler method for an action ID."""
        handlers = {
            "record": self.toggle_recording,
            "cancel": self.cancel_recording,
            "minimize": self.hide,
            "small_mode": self.toggle_small_mode,
            "simple_mode": self.toggle_simple_mode,
            "retranscribe": self.retranscribe_latest,
            "copy": self.copy_transcription,
            "load": self.load_audio_file,
            "folder": self.open_folder,
            "sound": self.toggle_sound,
            "auto_hide": self.toggle_auto_hide,
            "llm": self.toggle_llm,
            "wake_word": self.toggle_wake_word,
            "model": self.show_model_dialog,
            "help": self.show_help,
        }
        return handlers.get(action_id)

    def _setup_tray(self):
        self.tray = QSystemTrayIcon(self)
        self.tray.setIcon(_get_menubar_icon())
        # Tray icon animation state
        self.tray_hue = 0.0
        self.tray_icon_timer = QTimer(self)
        self.tray_icon_timer.timeout.connect(self._update_tray_icon)
        menu = QMenu()
        menu.addAction("Show", self.show)
        menu.addSeparator()
        # Cancel Recording (only visible when recording)
        self._cancel_action = menu.addAction("Cancel Recording", self.cancel_recording)
        self._cancel_action.setVisible(False)
        # Add menu items from ACTIONS
        for action_id, key, icon_name, desc, menu_text in ACTIONS:
            if menu_text:
                handler = self._get_action_handler(action_id)
                if handler:
                    menu.addAction(menu_text, handler)
        menu.addSeparator()
        menu.addAction("Quit", QApplication.quit)
        self.tray.setContextMenu(menu)
        self.tray.setToolTip(APP_NAME)
        self.tray.show()

    def _update_tray_icon(self):
        """Update tray icon with cycling hue."""
        self.tray_hue = (self.tray_hue + 2) % 360
        self.tray.setIcon(_get_menubar_icon(hue=self.tray_hue))

    def _maybe_hide(self):
        if not S.AUTO_HIDE:
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
            play_chime('unfocus')  # G key: descending unfocus
        else:
            # Remember current app before stealing focus
            self._prev_app = NSWorkspace.sharedWorkspace().frontmostApplication()
            self.show()
            self.raise_()
            self.activateWindow()
            play_chime('focus')  # G key: ascending focus

    def _switch_tab(self, index):
        self.tab_stack.setCurrentIndex(index)
        self.output_tab.setChecked(index == 0)
        self.transcriptions_tab.setChecked(index == 1)
        self._update_tab_icons()

    def _update_tab_icons(self):
        """Update tab icons - dark when unchecked, light when checked (blue)."""
        for tab in [self.output_tab, self.transcriptions_tab]:
            color = ICON_COLOR_LIGHT if tab.isChecked() else ICON_COLOR_DARK
            tab.setIcon(load_icon(tab.icon_name, color=color))

    def _update_checkable_btn_icon(self, btn, icon_name=None):
        """Update a checkable button's icon color based on checked state."""
        name = icon_name or btn.icon_name
        color = ICON_COLOR_LIGHT if btn.isChecked() else ICON_COLOR_DARK
        btn.setIcon(load_icon(name, color=color))

    def _flash_button(self, key):
        """Visually flash the button for a key press."""
        btn = self.key_buttons.get(key)
        if btn and btn.isEnabled():
            btn.setDown(True)
            QTimer.singleShot(100, lambda: btn.setDown(False))

    def _add_transcription(self, raw_text, processed_text, audio_path):
        self.transcriptions.append((raw_text, processed_text, audio_path))
        self.transcriptions_panel.add_transcription(raw_text, processed_text, audio_path)
        self._switch_tab(1)
        # Update retranscribe button enabled state
        self.retranscribe_btn.setEnabled(audio_path is not None)

    def _update_transcription(self, index, raw_text, processed_text):
        # Preserve audio_path from existing transcription
        if index < len(self.transcriptions):
            audio_path = self.transcriptions[index][2] if len(self.transcriptions[index]) > 2 else None
            self.transcriptions[index] = (raw_text, processed_text, audio_path)
        self.transcriptions_panel.update_transcription(index, raw_text, processed_text)

    def _copy_to_clipboard(self, text):
        rp.string_to_clipboard(text)
        self.pet_container.trigger_copy()
        play_chime('copy')  # E key: copy

    def _deramble_transcription(self, index, raw_text):
        """Process a transcription with LLM and update it in place."""
        def do_deramble():
            processed = self._run_llm(raw_text)
            self.update_transcription_signal.emit(index, raw_text, processed)
        threading.Thread(target=do_deramble, daemon=True).start()

    def retranscribe_latest(self):
        """Retranscribe the most recent audio file with the current model.

        Copies the audio to a new timestamped file and runs through normal transcribe path.
        """
        if self.state != "idle":
            play_chime('delete')
            return
        # Find latest transcription with audio_path
        audio_path = None
        for i in range(len(self.transcriptions) - 1, -1, -1):
            if len(self.transcriptions[i]) > 2 and self.transcriptions[i][2]:
                audio_path = self.transcriptions[i][2]
                break
        if not audio_path or not os.path.exists(audio_path):
            play_chime('delete')
            return
        # Copy to new file and transcribe through normal path
        self._transcribe_file(audio_path)

    def _do_paste(self, text):
        # Copy is required for any paste operation
        if not S.AUTO_COPY:
            return

        # Voice routing: if tmux mode enabled, check for phrase matches
        tmux_routed = False
        if S.TMUX_MODE:
            matches = self._find_matching_tmux_panes(text)
            if matches:
                # Magic phrase matched - route to tmux panes (skip ⌘V)
                # Append TTS instruction for tmux if enabled
                tmux_text = text
                if S.SPEAK_BACK_APPEND_INSTRUCTION:
                    instruction = S.SPEAK_BACK_INSTRUCTION_TEMPLATE.format(
                        command=build_tts_command()
                    )
                    tmux_text = text + '\n\n' + instruction
                self._copy_to_clipboard(tmux_text)
                time.sleep(0.1)
                play_chime('tmux_send')
                self._do_tmux_paste_to_targets(matches, tmux_text)
                tmux_routed = True

        # ⌘V paste: only if enabled AND tmux didn't route
        if S.AUTO_PASTE and not tmux_routed:
            # Append TTS instruction for paste only if enabled and not tmux-only mode
            paste_text = text
            if S.SPEAK_BACK_APPEND_INSTRUCTION and not S.SPEAK_BACK_TMUX_ONLY:
                instruction = S.SPEAK_BACK_INSTRUCTION_TEMPLATE.format(
                    command=build_tts_command()
                )
                paste_text = text + '\n\n' + instruction
            self._copy_to_clipboard(paste_text)
            time.sleep(0.1)
            kb = KeyboardController()
            with kb.pressed(Key.cmd):
                kb.tap("v")
            if S.AUTO_ENTER:
                time.sleep(S.ENTER_DELAY)
                play_chime('enter')
                kb.press(Key.enter)
                time.sleep(0.1)
                kb.release(Key.enter)

    def _do_tmux_paste(self, text):
        """Paste text into the configured tmux pane and optionally press enter."""
        target = S.TMUX_TARGET or '%'
        self._do_tmux_paste_to_target(target, text)

    def _do_tmux_paste_to_target(self, target, text):
        """Send text to a specific tmux target (pane_id or session:window.pane)."""
        try:
            subprocess.run(['tmux', 'send-keys', '-t', target, '-l', text], check=True)
            if S.AUTO_ENTER:
                time.sleep(S.ENTER_DELAY)
                play_chime('enter')
                subprocess.run(['tmux', 'send-keys', '-t', target, 'Enter'], check=True)
            phrase = S.TMUX_PANE_NAMES.get(target, {}).get('phrase', target)
            print(f"Sent to tmux '{phrase}' ({target}): {text[:50]}{'...' if len(text) > 50 else ''}")
        except subprocess.CalledProcessError as e:
            print(f"tmux send-keys failed: {e}")
        except FileNotFoundError:
            print("tmux not found - is tmux installed and running?")

    def _do_tmux_paste_to_targets(self, targets, text):
        """Send text to multiple tmux targets simultaneously, then Enter simultaneously."""
        # Send text to all targets at once
        for target in targets:
            try:
                subprocess.Popen(['tmux', 'send-keys', '-t', target, '-l', text])
            except FileNotFoundError:
                print("tmux not found")
                return
        # Wait for text to be sent, then send Enter to all
        if S.AUTO_ENTER:
            time.sleep(S.ENTER_DELAY)
            play_chime('enter')
            for target in targets:
                subprocess.Popen(['tmux', 'send-keys', '-t', target, 'Enter'])
        # Log what was sent
        names = [S.TMUX_PANE_NAMES.get(t, {}).get('phrase', t) for t in targets]
        print(f"Sent to {len(targets)} panes ({', '.join(names)}): {text[:50]}{'...' if len(text) > 50 else ''}")
        # Announce pane names via TTS if enabled
        if S.TMUX_ANNOUNCE_PANE and names:
            announcement = f"sent to {' '.join(names)}"
            self._speak_announcement(announcement)

    def _speak_announcement(self, text):
        """Speak an announcement using TTS (non-blocking)."""
        do_tts(text, block=False)

    def _find_matching_tmux_panes(self, text):
        """Find panes whose magic phrase matches the transcription text."""
        text_lower = text.lower()
        matches = []
        for pane_id, info in S.TMUX_PANE_NAMES.items():
            phrase = info.get('phrase', '')
            if phrase and phrase.lower() in text_lower:
                matches.append(pane_id)
        return matches

    def _update_display(self):
        if self.audio_chunks:
            audio = np.concatenate(self.audio_chunks)
            self.waveform.set_samples(audio)
            secs = len(audio) / SAMPLE_RATE
            self.timer_label.set_text(f"{int(secs // 60)}:{secs % 60:04.1f}")

    def _update_log(self):
        # Fast check: only process if buffer grew
        buf_len = len(self.tee._buf)
        if buf_len == getattr(self, '_last_log_buf_len', 0):
            return
        self._last_log_buf_len = buf_len

        new_text = rp.strip_ansi_escapes(self.tee.text)
        if new_text != self.output_panel.toPlainText():
            self.output_panel.setPlainText(new_text)
            sb = self.output_panel.verticalScrollBar()
            sb.setValue(sb.maximum())

    def changeEvent(self, e):
        if e.type() == e.Type.ActivationChange:
            self.is_focused = self.isActiveWindow()
            # Fade window when unfocused
            self.setWindowOpacity(1.0 if self.is_focused else 0.7)
            self.update()  # Repaint for border change
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
        elif no_mods and key == Qt.Key.Key_X and self.state == "recording": self.cancel_recording()
        elif no_mods and key == Qt.Key.Key_Space: self.toggle_recording()
        elif no_mods and key == Qt.Key.Key_C: self.copy_transcription()
        elif no_mods and key == Qt.Key.Key_F: self.open_folder()
        elif no_mods and key == Qt.Key.Key_L: self.load_audio_file()
        elif no_mods and key == Qt.Key.Key_S: self.toggle_sound()
        elif no_mods and key == Qt.Key.Key_H: self.toggle_auto_hide()
        elif no_mods and key == Qt.Key.Key_R: self.toggle_llm()
        elif no_mods and key == Qt.Key.Key_J: self.toggle_wake_word()
        elif no_mods and key == Qt.Key.Key_N: self.toggle_auto_enter()
        elif no_mods and key == Qt.Key.Key_U: self.show_tmux_selection()
        elif no_mods and key == Qt.Key.Key_E: self.toggle_small_mode()
        elif no_mods and key == Qt.Key.Key_W: self.toggle_simple_mode()
        elif no_mods and key == Qt.Key.Key_Z: self.retranscribe_latest()
        elif no_mods and key == Qt.Key.Key_O: self._switch_tab(0)
        elif no_mods and key == Qt.Key.Key_T: self._switch_tab(1)
        elif no_mods and key == Qt.Key.Key_M: self.show_model_dialog()
        elif no_mods and key == Qt.Key.Key_P: self.show_prefs()
        elif key == Qt.Key.Key_Question: self.show_help()
        elif mods == Qt.KeyboardModifier.ControlModifier and key == Qt.Key.Key_L: dump_chime_log()  # Ctrl+L: dump chime log
        else:
            super().keyPressEvent(e)

    def _paint_content(self, painter):
        rect = self.rect().adjusted(2, 2, -2, -2)
        STYLE.paint_window(painter, rect, self.width(), self.height(), self.isActiveWindow())

    def resizeEvent(self, e):
        """Handle resize - update UI."""
        super().resizeEvent(e)
        self._update_ui()

    def _calc_btn_width(self, num_buttons, width):
        """Calculate button width given number of buttons and available width."""
        if num_buttons == 0:
            return 0
        spacing = 8 * (num_buttons - 1)
        return (width - 16 - spacing) / num_buttons  # 16 = margins

    def _update_ui(self):
        """Single source of truth for all UI visibility based on window size and mode flags."""
        h, w = self.height(), self.width()

        # Height thresholds
        show_tabs = h >= 250
        show_output = h >= 220
        show_buttons = h >= 180
        is_small = h < 120

        # Panel visibility
        self.tab_stack.setVisible(show_output)
        self.tab_row_widget.setVisible(show_tabs and not S.SIMPLE_MODE)
        self.btn_row_widget.setVisible(show_buttons)
        self.waveform.setVisible(h >= 120)
        self.status_spacer.setVisible(show_buttons)

        # Determine toolbar layout: single row, two rows, or force simple
        n = len(self.all_toolbar_buttons)
        use_two_rows = False
        force_simple = False

        if not S.SIMPLE_MODE:
            if self._calc_btn_width(n, w) < MIN_TOOLBAR_BUTTON_WIDTH:
                # Try two rows
                if self._calc_btn_width((n + 1) // 2, w) >= MIN_TOOLBAR_BUTTON_WIDTH:
                    use_two_rows = True
                else:
                    force_simple = True

        # Button visibility
        hide_advanced = S.SIMPLE_MODE or force_simple
        for btn in self.all_toolbar_buttons:
            btn.setVisible(show_buttons and (btn in self.essential_buttons or not hide_advanced))

        # Arrange buttons into rows
        visible = [b for b in self.all_toolbar_buttons if b.isVisible()]
        if use_two_rows and show_buttons:
            half = (len(visible) + 1) // 2
            for btn in visible[:half]:
                if btn.parent() != self.btn_row_widget:
                    self.btn_row.addWidget(btn)
            for btn in visible[half:]:
                if btn.parent() != self.btn_row2_widget:
                    self.btn_row2.addWidget(btn)
            self.btn_row2_widget.setVisible(True)
        else:
            for btn in self.all_toolbar_buttons:
                if btn.parent() != self.btn_row_widget:
                    self.btn_row.addWidget(btn)
            self.btn_row2_widget.setVisible(False)

        # Update simple mode button
        self.simple_btn.setChecked(S.SIMPLE_MODE)
        self._update_checkable_btn_icon(self.simple_btn, "plus" if S.SIMPLE_MODE else "minus")

        # Button text mode
        self._update_button_mode(w < 350)

        # --- Small mode appearance ---
        font_size = 10 if is_small else 14
        self.status_label.setStyleSheet(title_style(font_size))
        self.small_btn.set_icon_name("macos-fullscreen" if is_small else "macos-collapse")
        self.pet_container.setVisible(not is_small)  # Hide pets in small mode

        # In simple mode, ensure transcriptions tab is active
        if S.SIMPLE_MODE:
            self.tab_stack.setCurrentIndex(1)


    def _cleanup(self):
        if self.stream:
            self.stream.stop()
            self.stream.close()
            self.stream = None
        self.update_timer.stop()

    def _update_buttons(self):
        recording = self.state == "recording"
        transcribing = self.state == "transcribing"
        self.record_btn.setIcon(load_icon("stop" if recording else "record", color=ICON_COLOR_DARK))
        self.record_btn.setEnabled(not transcribing)
        self.cancel_btn.setEnabled(recording)
        self.copy_btn.setEnabled(self.last_transcription is not None)
        self.folder_btn.setEnabled(True)
        self.load_btn.setEnabled(not recording and not transcribing)
        self.model_btn.setEnabled(not recording and not transcribing)
        # Retranscribe enabled only when idle and we have transcriptions with audio
        has_audio = any(len(t) > 2 and t[2] for t in self.transcriptions) if self.transcriptions else False
        self.retranscribe_btn.setEnabled(not recording and not transcribing and has_audio)

    def _update_button_mode(self, icon_only):
        """Update button text display: text+icon or icon-only.

        Note: Visibility is handled entirely by _update_ui. This ONLY sets text.
        In simple mode, show descriptive labels instead of key shortcuts.
        """
        # Normal mode: show key shortcuts (or nothing if icon_only)
        # Simple mode: show descriptive one-word labels
        if S.SIMPLE_MODE:
            labels = [
                (self.record_btn, "Record"), (self.cancel_btn, "Cancel"),
                (self.simple_btn, "More"), (self.prefs_btn, "Prefs"), (self.help_btn, "Help"),
            ]
        else:
            labels = [
                (self.record_btn, "␣"), (self.cancel_btn, "X"),
                (self.retranscribe_btn, "Z"), (self.simple_btn, "W"),
                (self.copy_btn, "C"), (self.load_btn, "L"), (self.folder_btn, "F"),
                (self.sound_btn, "S"), (self.eye_btn, "H"), (self.llm_btn, "R"),
                (self.wake_word_btn, "J"), (self.enter_btn, "N"),
                (self.model_btn, "M"), (self.prefs_btn, "P"), (self.help_btn, "?"),
            ]
        for btn, label in labels:
            btn.setText("" if icon_only and not S.SIMPLE_MODE else label)

    def toggle_recording(self):
        if self.state == "idle":
            self.start_recording()
        elif self.state == "recording":
            self.stop_recording()
        else:
            play_chime('delete')  # Minor: busy/error

    def cancel_recording(self):
        if self.state != "recording":
            return
        self._cleanup()
        self._set_state("idle")
        self.audio_chunks = []
        self.waveform.set_samples(np.array([]))
        self.pet_container.set_listening(False)  # Stop pet animation
        self.tray_icon_timer.stop()
        self.tray.setIcon(_get_menubar_icon())  # Reset to template icon
        play_chime('cancel')  # Minor: cancel
        # Reset wake word model to clear any buffered audio that might cause false triggers
        if self.wake_word_engine is not None:
            self.wake_word_engine.reset()
        self.hide_signal.emit()

    def _get_status_text(self):
        """Get status text based on current state."""
        if self.state == "idle":
            return f"Say '{self._get_wake_word_display()}'" if S.WAKE_WORD_ENABLED else "Double-tap ⌥"
        elif self.state == "recording":
            return "Recording"
        elif self.state == "transcribing":
            return "Transcribing..."
        return self.state  # Fallback

    def _update_status(self):
        """Refresh status label based on current state."""
        self.status_label.setText(self._get_status_text())

    def _set_state(self, state, status=None):
        """Set app state. status overrides the default text for this state."""
        self.state = state
        self.status_label.setText(status if status else self._get_status_text())
        opacity = 0.9 if state == "recording" else 0.3
        self.timer_label.set_opacity(opacity)
        self._update_buttons()
        # Update tray menu cancel action visibility
        if hasattr(self, '_cancel_action'):
            self._cancel_action.setVisible(state == "recording")

    # --- Settings hooks - UI updates only (called after S.set changes value) ---
    def _on_pet_types_changed(self, pet_types):
        self.pet_container.set_pets(pet_types)

    def _on_auto_hide_changed(self, enabled):
        self.eye_btn.setChecked(enabled)
        self._update_checkable_btn_icon(self.eye_btn, "eye-off" if enabled else "eye")

    def _on_sound_changed(self, enabled):
        self.sound_btn.setChecked(enabled)
        self._update_checkable_btn_icon(self.sound_btn, "volume" if enabled else "volume-off")

    def _on_llm_changed(self, enabled):
        self.llm_btn.setChecked(enabled)
        self._update_checkable_btn_icon(self.llm_btn)

    def _on_auto_enter_changed(self, enabled):
        self.enter_btn.setChecked(enabled)
        self._update_checkable_btn_icon(self.enter_btn, "enter" if enabled else "enter-off")

    def _on_tmux_mode_changed(self, enabled):
        self.tmux_btn.setChecked(enabled)
        self._update_checkable_btn_icon(self.tmux_btn)  # Uses icon_name from button ("tmux")
        print(f"Tmux paste mode {'ON' if enabled else 'OFF'}")

    def _on_simple_mode_changed(self, enabled):
        self._update_ui()

    def _on_always_on_top_setting_changed(self, enabled):
        self._apply_window_flags(show=True)
        print(f"Always on top {'ON' if enabled else 'OFF'}")

    def _apply_window_flags(self, show=True):
        """Apply window flags based on ALWAYS_ON_TOP setting."""
        flags = Qt.WindowType.FramelessWindowHint
        if S.ALWAYS_ON_TOP:
            flags |= Qt.WindowType.WindowStaysOnTopHint
        self.setWindowFlags(flags)
        if show:
            self.show()  # Required after changing window flags

    def _on_wake_word_enabled_changed(self, enabled):
        self.wake_word_btn.setChecked(enabled)
        self._update_checkable_btn_icon(self.wake_word_btn)
        if enabled:
            self._start_wake_word_listener()
            play_chime('record_start')
        else:
            self._stop_wake_word_listener()
            play_chime('record_stop')
        print(f"Wake word detection {'ON' if enabled else 'OFF'}")
        self._update_status()

    def _on_wake_word_settings_changed(self, _value):
        """Handle wake word engine or settings change - restart if active."""
        if S.WAKE_WORD_ENABLED:
            self._stop_wake_word_listener()
            self._start_wake_word_listener()
        self.wake_word_btn.setToolTip(f"Toggle wake word ({self._get_wake_word_display()})")
        self._update_status()

    def _get_wake_word_display(self) -> str:
        """Get display name for current wake word configuration."""
        engine = S.WAKEWORD_ENGINE
        if engine == 'openwakeword':
            model = S.WAKEWORD_OPENWAKEWORD.get('model', 'computer')
            return get_wake_word_display(model)
        else:
            phrases = S.WAKEWORD_MACOS.get('phrases', 'hey computer')
            first = phrases.split(',')[0].strip() if phrases else 'hey computer'
            return first

    def toggle_auto_hide(self):
        S.set('AUTO_HIDE', not S.AUTO_HIDE)
        self._save_settings()

    def toggle_small_mode(self):
        """Toggle between small and normal window size. Progressive collapse handles the rest."""
        # Check if currently small (height < 120)
        is_small = self.height() < 120
        if is_small:
            # Expand to normal size
            if hasattr(self, '_normal_size'):
                self.resize(self._normal_size)
            else:
                self.resize(400, 350)
        else:
            # Save current size and shrink to small
            self._normal_size = self.size()
            self.resize(200, 80)  # Small size - fits timer (160+20=180 min width)

    def toggle_simple_mode(self):
        """Toggle simple mode - hides advanced buttons and shows only transcriptions."""
        S.set('SIMPLE_MODE', not S.SIMPLE_MODE)
        self._save_settings()

    def toggle_sound(self):
        S.set('SOUND_ENABLED', not S.SOUND_ENABLED)

    def toggle_llm(self):
        S.set('LLM_ENABLED', not S.LLM_ENABLED)

    def toggle_wake_word(self):
        S.set('WAKE_WORD_ENABLED', not S.WAKE_WORD_ENABLED)
        self._save_settings()

    def toggle_auto_enter(self):
        S.set('AUTO_ENTER', not S.AUTO_ENTER)

    def toggle_auto_copy(self):
        S.set('AUTO_COPY', not S.AUTO_COPY)

    def toggle_auto_paste(self):
        S.set('AUTO_PASTE', not S.AUTO_PASTE)

    def toggle_tmux_mode(self):
        S.set('TMUX_MODE', not S.TMUX_MODE)

    def show_tmux_selection(self):
        """Show dialog to select tmux target pane."""
        dialog = TmuxSelectionDialog(S.TMUX_TARGET, self)
        dialog.center_on_parent()
        if dialog.exec():
            S.set('TMUX_TARGET', dialog.selected_target)
            self._save_settings()

    def _start_wake_word_listener(self):
        """Start wake word detection using the configured engine."""
        if self.wake_word_engine is not None:
            return  # Already running

        try:
            from wakeword import create_engine
            engine_name = S.WAKEWORD_ENGINE

            # Get engine-specific config
            if engine_name == 'openwakeword':
                cfg = S.WAKEWORD_OPENWAKEWORD
                self.wake_word_engine = create_engine(
                    engine_name,
                    callback=self._on_wake_word_detected,
                    model=cfg.get('model', 'computer'),
                    sensitivity=cfg.get('sensitivity', 0.2),
                )
            else:  # macos
                cfg = S.WAKEWORD_MACOS
                # Collect tmux phrases if checkbox is enabled
                tmux_phrases = []
                if cfg.get('use_tmux_phrases') and S.TMUX_PANE_NAMES:
                    for info in S.TMUX_PANE_NAMES.values():
                        phrase = info.get('phrase', '')
                        if phrase:
                            tmux_phrases.append(phrase)
                self.wake_word_engine = create_engine(
                    engine_name,
                    callback=self._on_wake_word_detected,
                    phrases=cfg.get('phrases', 'hey computer, computer'),
                    tmux_phrases=tmux_phrases,
                )

            # Set up stop callback
            self.wake_word_engine.on_stop = lambda: self.stop_signal.emit()

            self.wake_word_engine.start()
            print(f"Wake word listener started ({self._get_wake_word_display()})")

        except Exception as e:
            print(f"Failed to start wake word listener: {e}")
            S.WAKE_WORD_ENABLED = False
            self.wake_word_engine = None

    def _stop_wake_word_listener(self):
        """Stop the wake word engine."""
        if self.wake_word_engine is not None:
            self.wake_word_engine.stop()
            self.wake_word_engine = None
            print("Wake word listener stopped")

    def _pause_wake_word_listener(self):
        """Temporarily pause wake word listener (e.g., during recording)."""
        if self.wake_word_engine is not None:
            self.wake_word_engine.pause()

    def _resume_wake_word_listener(self):
        """Resume wake word listener if enabled."""
        if S.WAKE_WORD_ENABLED and self.wake_word_engine is not None:
            self.wake_word_engine.reset()
            self.wake_word_engine.resume()

    def _on_wake_word_detected(self, pre_buffer=None):
        """Called when wake word is detected - start recording with pre-buffer."""
        # Use lock to prevent race between audio callback thread and main thread
        with self._state_lock:
            if self.state != "idle":
                return
            # Immediately mark state to prevent double-trigger
            self.state = "starting"
        # Use signal to call start_recording on main thread with pre_buffer
        if pre_buffer is None:
            pre_buffer = np.array([], dtype=np.float32)
        self.wake_word_signal.emit(pre_buffer)

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
        S.set('AUTO_HIDE', False)  # Disable auto-hide since global shortcuts won't work (don't save - temporary)
        self.warning_btn.show()

    def show_model_dialog(self):
        """Show dialog to select Whisper model."""
        dialog = ModelDialog(S.WHISPER_MODEL, self)
        dialog.center_on_parent()
        if dialog.exec() and dialog.selected_model and dialog.selected_model != S.WHISPER_MODEL:
            self._change_model(dialog.selected_model)

    def show_prefs(self):
        """Show preferences dialog. Settings apply live, Cancel reverts."""
        while True:
            import copy
            orig = copy.deepcopy(dict(S))  # Snapshot for Cancel
            orig_style = STYLE.name

            dialog = PrefsDialog(STYLE.name, S.PET_TYPES, S.SIMPLE_MODE, self,
                                 auto_enter=S.AUTO_ENTER)

            # Live preview connections - all use S.set() to trigger hooks
            dialog.simple_mode_changed.connect(self._set_simple_mode)
            dialog.style_changed.connect(lambda s: self._change_style(s, save=False))
            dialog.pets_changed.connect(lambda p: S.set('PET_TYPES', list(p)))
            dialog.wake_word_changed.connect(self._on_wake_word_settings_changed)
            dialog.auto_enter_changed.connect(lambda v: S.set('AUTO_ENTER', v))

            dialog.center_on_parent()

            if dialog.exec():
                self._save_settings()
                break
            elif getattr(dialog, 'reverted_to_defaults', False):
                self._change_style(DEFAULTS['THEME'], save=False)
                continue  # Re-open dialog with defaults
            else:
                # Cancel - restore snapshot (hooks handle UI updates)
                if STYLE.name != orig_style:
                    self._change_style(orig_style, save=False)
                S.restore(orig)
                break

    def _set_simple_mode(self, enabled):
        """Set simple mode on/off (called from prefs dialog)."""
        if S.SIMPLE_MODE != enabled:
            self.toggle_simple_mode()

    def _load_settings(self):
        """Load settings from JSON file. Uses S.set() to trigger hooks for UI updates."""
        if not os.path.exists(SETTINGS_FILE):
            return
        with open(SETTINGS_FILE, 'r') as f:
            data = json.load(f)

        # Migrate old lowercase keys to uppercase
        data = {k.upper(): v for k, v in data.items()}

        # Convert pet strings to enums
        if 'PET_TYPES' in data:
            pet_map = {pt.value: pt for pt in ALL_PET_TYPES}
            data['PET_TYPES'] = [pet_map[v] for v in data['PET_TYPES'] if v in pet_map]

        # Apply settings via S.set() to trigger hooks
        for key in ['AUTO_HIDE', 'SOUND_ENABLED', 'LLM_ENABLED', 'AUTO_ENTER', 'AUTO_COPY', 'AUTO_PASTE', 'TMUX_MODE', 'PET_TYPES', 'ALWAYS_ON_TOP']:
            if key in data:
                S.set(key, data[key])
        # Simple settings without hooks (or with trivial hooks)
        for key in ['ENTER_DELAY', 'CUSTOM_WORDS', 'WHISPER_MODEL',
                    'LLM_MODEL', 'LLM_PREFIX', 'CHIME_VOLUME', 'CHIME_PITCH',
                    'CHIME_PROGRAM', 'CHIME_THEME', 'SILENCE_SKIP_ENABLED', 'SILENCE_THRESHOLD',
                    'TMUX_TARGET', 'TMUX_PANE_NAMES', 'TMUX_PHRASES_AS_CONTEXT', 'TMUX_ANNOUNCE_PANE', 'RECORDINGS_DIR',
                    'SPEAK_BACK_VOICE', 'TTS_SAY', 'TTS_SUPERTONIC', 'TTS_KITTEN',
                    'SPEAK_BACK_APPEND_INSTRUCTION', 'SPEAK_BACK_TMUX_ONLY', 'SPEAK_BACK_INSTRUCTION_TEMPLATE',
                    'WAKEWORD_ENGINE', 'WAKEWORD_OPENWAKEWORD', 'WAKEWORD_MACOS']:
            if key in data:
                S[key] = data[key]
        # SIMPLE_MODE needs toggle pattern (handle both on->off and off->on)
        if 'SIMPLE_MODE' in data and data['SIMPLE_MODE'] != S.SIMPLE_MODE:
            self.toggle_simple_mode()
        # THEME is separate (not in S)
        if 'THEME' in data:
            self._change_style(data['THEME'], save=False)
        # WAKE_WORD_ENABLED last (needs model loaded)
        if data.get('WAKE_WORD_ENABLED'):
            S.set('WAKE_WORD_ENABLED', True)

    def _save_settings(self):
        """Save settings to JSON file."""
        data = dict(S)
        data['PET_TYPES'] = [pt.value for pt in S.PET_TYPES]  # Convert enums to strings
        data['THEME'] = STYLE.name  # Theme is in STYLE, not S
        with open(SETTINGS_FILE, 'w') as f:
            json.dump(data, f, indent=2)

    def _change_style(self, style_name, save=True):
        """Change the UI style immediately."""
        global STYLE, ACCENT, TEXT_PRIMARY, TEXT_SECONDARY, TEXT_MUTED, TEXT_ERROR, TEXT_LINK
        global BORDER_COLOR, BORDER_DARK, ICON_COLOR_DARK, ICON_COLOR_LIGHT, ICON_COLOR_MUTED
        global SCROLLBAR_CSS, PANEL_BG_CSS, PANEL_BG_FLAT_CSS, UI_FONT

        # Update global style
        STYLE = get_style(style_name)
        ACCENT = STYLE.accent
        TEXT_PRIMARY = STYLE.text_primary
        TEXT_SECONDARY = STYLE.text_secondary
        TEXT_MUTED = STYLE.text_muted
        TEXT_ERROR = STYLE.text_error
        TEXT_LINK = STYLE.text_link
        BORDER_COLOR = STYLE.border_color
        BORDER_DARK = STYLE.border_dark
        ICON_COLOR_DARK = STYLE.icon_color_dark
        ICON_COLOR_LIGHT = STYLE.icon_color_light
        ICON_COLOR_MUTED = STYLE.icon_color_muted
        SCROLLBAR_CSS = STYLE.scrollbar_css()
        PANEL_BG_CSS = STYLE.panel_bg_css()
        PANEL_BG_FLAT_CSS = STYLE.panel_bg_flat_css()
        UI_FONT = STYLE.font

        # Refresh all widgets
        self._refresh_styles()
        if save:
            self._save_settings()

    def _refresh_styles(self):
        """Refresh all widget styles after a style change."""
        btn_css = get_btn_css()
        # Refresh all buttons
        for btn in [self.record_btn, self.cancel_btn, self.retranscribe_btn, self.simple_btn,
                    self.copy_btn, self.load_btn, self.folder_btn, self.sound_btn,
                    self.eye_btn, self.llm_btn, self.wake_word_btn,
                    self.enter_btn, self.tmux_btn, self.model_btn, self.prefs_btn, self.help_btn]:
            btn.setStyleSheet(btn_css)
        # Refresh tab buttons
        self.output_tab.setStyleSheet(get_tab_css())
        self.transcriptions_tab.setStyleSheet(get_tab_css())
        self._update_tab_icons()
        # Refresh panels
        self.output_panel.setStyleSheet(f"QTextEdit {{ {PANEL_BG_FLAT_CSS} color: {TEXT_SECONDARY}; font-size: 11px; }} {SCROLLBAR_CSS}")
        self.transcriptions_panel._apply_style()
        # Refresh status label (font size matches _update_ui logic)
        font_size = 10 if self.height() < 120 else 14
        self.status_label.setStyleSheet(title_style(font_size))
        # Refresh waveform glow
        self.waveform._update_glow()
        # Force repaint for background, timer, waveform
        self.timer_label.update()
        self.waveform.update()
        self.update()

    def _change_model(self, new_model):
        """Load a new Whisper model in background thread."""
        self._set_state("transcribing", f"Loading {new_model}...")
        self._switch_tab(0)

        def load():
            play_chime('loading_start')  # Loading start
            print(f"Loading model: {new_model}")
            rp.r._get_pywhispercpp_model(new_model)
            S.WHISPER_MODEL = new_model
            self._save_settings()
            print(f"Model {new_model} loaded")
            play_chime('loading_done')  # Loading done
            self._set_state("idle")

        threading.Thread(target=load, daemon=True).start()

    def copy_transcription(self):
        if self.last_transcription:
            self._copy_to_clipboard(self.last_transcription)

    def open_folder(self):
        os.makedirs(S.RECORDINGS_DIR, exist_ok=True)
        rp.open_file_with_default_application(S.RECORDINGS_DIR)

    def load_audio_file(self):
        """Open file dialog to load an audio file for transcription."""
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
        play_chime('start_rec')  # D key
        self.last_audio_path = path
        threading.Thread(target=self._transcribe_file_thread, args=(path,), daemon=True).start()

    def _get_initial_prompt(self):
        """Get initial_prompt for Whisper, including tmux phrase words if enabled."""
        words = S.CUSTOM_WORDS or ""
        if S.TMUX_PHRASES_AS_CONTEXT and S.TMUX_PANE_NAMES:
            phrase_words = set()
            for info in S.TMUX_PANE_NAMES.values():
                phrase = info.get('phrase', '')
                phrase_words.update(phrase.split())
            if phrase_words:
                words = f"{words} {' '.join(phrase_words)}".strip()
        return words or None

    def _transcribe_file_thread(self, path):
        try:
            print(f"Transcribing file: {path}")
            initial_prompt = self._get_initial_prompt()
            # Note: carry_initial_prompt not yet exposed in pywhispercpp C bindings
            result = rp.transcribe_audio_file_via_whisper(
                path, model=S.WHISPER_MODEL, show_progress=True,
                initial_prompt=initial_prompt
            )
            self._handle_transcription_result(result.text, audio_path=path)
        except Exception as e:
            print(f"Transcription error: {e}")
            raise
        finally:
            self.finish_signal.emit()

    def start_recording(self, pre_buffer=None):
        """Start recording audio. Optional pre_buffer is prepended to recording."""
        # Pause wake word listener - it will track _is_recording state so saying
        # the wake word again triggers on_stop instead of on_wake
        self._pause_wake_word_listener()

        self.audio_chunks = []
        if pre_buffer is not None and len(pre_buffer) > 0:
            self.audio_chunks.append(pre_buffer)

        self.show()
        if self.first_show:
            screen = QApplication.primaryScreen().geometry()
            self.move((screen.width() - self.width()) // 2, screen.height() // 4)
            self.first_show = False
        self.timer_label.set_text("0:00.0")
        self._set_state("recording", "Recording")
        self.pet_container.set_listening(True)
        play_chime('start_rec')  # D key

        def callback(indata, frames, time_info, status):
            chunk = indata[:, 0].copy()
            # Silence skip: don't record if audio level is below threshold
            if S.SILENCE_SKIP_ENABLED:
                rms = np.sqrt(np.mean(chunk ** 2))
                db = 20 * np.log10(rms + 1e-10)  # Add epsilon to avoid log(0)
                if db < S.SILENCE_THRESHOLD:
                    return  # Skip this chunk
            self.audio_chunks.append(chunk)

        self.stream = sd.InputStream(
            samplerate=SAMPLE_RATE,
            channels=1,
            dtype=np.float32,
            callback=callback,
            blocksize=BLOCKSIZE,
        )
        self.stream.start()
        self.update_timer.start(8)
        self.tray_icon_timer.start(50)  # ~20 FPS for smooth animation

    def stop_recording(self):
        if self.stream:
            self.stream.stop()
            self.stream.close()
            self.stream = None
        self.tray_icon_timer.stop()
        self.tray.setIcon(_get_menubar_icon())  # Reset to template icon
        self._set_state("transcribing", "Transcribing...")
        self.pet_container.set_listening(False)
        self.pet_container.set_processing(True)  # Emmy: record spin while transcribing
        self._switch_tab(0)  # Switch to Output tab during transcription
        play_chime('stop_rec')  # D key: stop recording
        audio = np.concatenate(self.audio_chunks) if self.audio_chunks else np.array([])
        self.waveform.set_samples(audio)
        threading.Thread(target=self._transcribe, args=(audio,), daemon=True).start()

    def _run_llm(self, text):
        """Run LLM on text. Returns processed result."""
        play_chime('llm_start')  # LLM processing start
        print(f"Processing with LLM ({S.LLM_MODEL})...")
        prefix = S.LLM_PREFIX if S.LLM_PREFIX else DEFAULT_LLM_PREFIX
        prompt = prefix + text
        result = rp.run_llm_api(prompt, model=S.LLM_MODEL)
        print(f"LLM result: {result!r}")
        play_chime('llm_done')  # LLM processing done
        return result

    def _process_with_llm(self, text):
        """Post-process transcription with LLM if enabled. Returns (raw, processed) or (raw, "")."""
        if not S.LLM_ENABLED or not text:
            return text, ""
        return text, self._run_llm(text)

    def _handle_transcription_result(self, text, txt_path=None, audio_path=None):
        """Process transcription result: LLM, save, paste, add to list."""
        if is_blacklisted(text):
            raw_text = ""
        else:
            # Strip wake words from beginning/end
            raw_text = strip_wake_words(text)

        # Prepend tmux trigger phrase if macOS engine recorded one
        if self.wake_word_engine is not None:
            trigger = getattr(self.wake_word_engine, 'last_trigger_phrase', None)
            if trigger and raw_text:
                raw_text = f"{trigger} {raw_text}"
                print(f"[wakeword] Prepended tmux phrase: '{trigger}'")
            # Clear it for next recording
            if hasattr(self.wake_word_engine, 'last_trigger_phrase'):
                self.wake_word_engine.last_trigger_phrase = None

        print(f"Result: {raw_text!r}")
        if not raw_text:
            play_chime('null_text')  # No text detected
            return
        play_chime('transcribe')  # Transcription done chime

        if S.LLM_ENABLED:
            # Show raw immediately, paste after LLM finishes
            index = len(self.transcriptions)
            self.add_transcription_signal.emit(raw_text, "", audio_path or "")

            def run_llm_and_update():
                processed = self._run_llm(raw_text)
                if txt_path:
                    with open(txt_path, "w") as f:
                        f.write(processed)
                self.last_transcription = processed
                self.update_transcription_signal.emit(index, raw_text, processed)
                self.paste_signal.emit(processed)
            threading.Thread(target=run_llm_and_update, daemon=True).start()
        else:
            if txt_path:
                with open(txt_path, "w") as f:
                    f.write(raw_text)
            self.last_transcription = raw_text
            self.paste_signal.emit(raw_text)
            self.add_transcription_signal.emit(raw_text, "", audio_path or "")

    def _transcribe(self, audio):
        try:
            if len(audio) == 0:
                print("No audio.")
                return
            print(f"Recorded {len(audio) / SAMPLE_RATE:.2f}s")

            os.makedirs(S.RECORDINGS_DIR, exist_ok=True)
            ts = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            wav_path = os.path.join(S.RECORDINGS_DIR, f"{ts}.wav")
            txt_path = os.path.join(S.RECORDINGS_DIR, f"{ts}.txt")

            scipy.io.wavfile.write(wav_path, SAMPLE_RATE, (audio * 32767).astype(np.int16))
            self.last_audio_path = wav_path
            initial_prompt = self._get_initial_prompt()
            # Note: carry_initial_prompt not yet exposed in pywhispercpp C bindings
            result = rp.transcribe_audio_file_via_whisper(
                wav_path, model=S.WHISPER_MODEL, show_progress=True,
                initial_prompt=initial_prompt
            )
            self._handle_transcription_result(result.text, txt_path, audio_path=wav_path)
        except Exception as e:
            print(f"Transcription error: {e}")
            raise
        finally:
            self.finish_signal.emit()

    def _finish(self):
        self._cleanup()
        self.pet_container.set_processing(False)  # Emmy: stop record spin
        self._set_state("idle")
        # Resume wake word listener (resets _is_recording flag)
        self._resume_wake_word_listener()
        self.hide_signal.emit()


def main():
    signal.signal(signal.SIGINT, signal.SIG_DFL)

    # Set process name for macOS Activity Monitor and menu bar
    try:
        bundle = NSBundle.mainBundle()
        info = bundle.localizedInfoDictionary() or bundle.infoDictionary()
        if info:
            info['CFBundleName'] = APP_NAME
    except Exception as e:
        print(f"Could not set macOS bundle name: {e}")

    app = QApplication([APP_NAME])
    app.setApplicationName(APP_NAME)
    app.setApplicationDisplayName(APP_NAME)

    # Set app icon (dock icon on macOS)
    icon_path = os.path.join(ASSETS_DIR, "icon.png")
    if os.path.exists(icon_path):
        app.setWindowIcon(QIcon(icon_path))

    # Load Futura font
    global UI_FONT
    font_id = QFontDatabase.addApplicationFont(UI_FONT_PATH)
    if font_id >= 0:
        UI_FONT = QFontDatabase.applicationFontFamilies(font_id)[0]

    app.setStyleSheet(f"QToolTip {{ background: #333; color: white; border: 1px solid #555; border-radius: 4px; font-family: {UI_FONT}; }}")
    window = VoiceThingWindow()

    tap_state = [0.0, 0, 0.0, False]  # [last_release_time, tap_count, current_press_time, pre_cancel_played]
    pressed = set()
    pre_cancel_timer = [None]  # Mutable container for timer reference
    CMD_KEYS = (keyboard.Key.cmd, keyboard.Key.cmd_l, keyboard.Key.cmd_r)
    ALT_KEYS = (keyboard.Key.alt, keyboard.Key.alt_l, keyboard.Key.alt_r)
    SHIFT_KEYS = (keyboard.Key.shift, keyboard.Key.shift_l, keyboard.Key.shift_r)

    def _play_pre_cancel():
        """Called after CANCEL_HOLD_SECONDS if still holding alt during recording."""
        if tap_state[1] == 2 and window.state == "recording" and any(k in pressed for k in ALT_KEYS):
            play_chime('pre_cancel')
            tap_state[3] = True  # Mark that pre_cancel was played

    def on_press(key):
        pressed.add(key)
        if key in ALT_KEYS:
            now = time.time()
            # Check if this press is close to last release (quick tap-tap)
            if now - tap_state[0] < 0.3:
                tap_state[1] += 1
            else:
                tap_state[1] = 1
            tap_state[2] = now  # Record press time
            tap_state[3] = False  # Reset pre_cancel flag
            # If this is the 2nd tap while recording, start timer for pre_cancel chime
            if tap_state[1] == 2 and window.state == "recording":
                pre_cancel_timer[0] = threading.Timer(CANCEL_HOLD_SECONDS, _play_pre_cancel)
                pre_cancel_timer[0].start()
        elif key in SHIFT_KEYS:
            # Shift aborts the cancel - reset to tap 1 so release won't trigger cancel
            if tap_state[1] == 2 and tap_state[3]:
                tap_state[1] = 0
                tap_state[3] = False
        elif key not in CMD_KEYS:
            tap_state[1] = 0

    def on_release(key):
        pressed.discard(key)
        if key in ALT_KEYS:
            # Cancel the pre_cancel timer if still running
            if pre_cancel_timer[0] is not None:
                pre_cancel_timer[0].cancel()
                pre_cancel_timer[0] = None
            now = time.time()
            hold_duration = now - tap_state[2]  # How long this tap was held
            cmd_held = any(k in pressed for k in CMD_KEYS)
            if tap_state[1] == 2:
                if cmd_held:
                    window.focus_signal.emit()
                elif window.state == "recording" and hold_duration >= CANCEL_HOLD_SECONDS:
                    window.cancel_signal.emit()
                else:
                    window.toggle_signal.emit()
                tap_state[1] = 0
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

    # Load whisper model in background thread (GUI stays responsive)
    def load_model():
        print(f"Loading Whisper ({S.WHISPER_MODEL})...")
        rp.r._get_pywhispercpp_model(S.WHISPER_MODEL)
        # Download openwakeword models if not already present
        try:
            import openwakeword
            openwakeword.utils.download_models()
        except Exception as e:
            print(f"openwakeword model download skipped: {e}")
        print(f"{APP_NAME} ready. Double-tap ⌥ to record.")
    threading.Thread(target=load_model, daemon=True).start()

    app.exec()


if __name__ == "__main__":
    main()
