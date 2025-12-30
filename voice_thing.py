#!/usr/bin/env /opt/homebrew/opt/python@3.10/bin/python3.10
"""Voice transcription: double-tap Option to record, transcribe, and type."""

import os
import signal
import subprocess
import tempfile
import threading
import time
from datetime import datetime

import numpy as np
import rp
import scipy.io.wavfile
import sounddevice as sd
from pynput import keyboard
from pynput.keyboard import Controller as KeyboardController, Key
from PyQt6.QtCore import Qt, QTimer, pyqtSignal, QSize, QPoint
from PyQt6.QtGui import QPainter, QColor, QPen, QIcon, QPixmap, QFontDatabase, QPolygon
from PyQt6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout,
                              QLabel, QScrollArea, QSystemTrayIcon, QMenu, QPushButton)

APP_NAME = "VoiceThing"
SAMPLE_RATE = 16000
WHISPER_MODEL = "large-v3"
ICON_COLOR = QColor(255, 255, 255, 180)
ACCENT_COLOR = QColor(100, 200, 255)
ICON_SIZE = 64
RECORDINGS_DIR = os.path.join(tempfile.gettempdir(), APP_NAME)

STATE_IDLE = "idle"
STATE_RECORDING = "recording"
STATE_TRANSCRIBING = "transcribing"


def draw_mic(p, size):
    p.setBrush(ICON_COLOR)
    p.setPen(Qt.PenStyle.NoPen)
    p.drawEllipse(size // 3, size // 6, size // 3, size // 2)
    p.drawRect(size * 5 // 12, size // 2, size // 6, size // 6)
    p.setBrush(Qt.BrushStyle.NoBrush)
    p.setPen(QPen(ICON_COLOR, 2))
    p.drawArc(size // 4, size // 3, size // 2, size // 2, 0, -180 * 16)


def draw_stop(p, size):
    p.setBrush(ICON_COLOR)
    p.setPen(Qt.PenStyle.NoPen)
    m = size // 4
    p.drawRect(m, m, size - 2 * m, size - 2 * m)


def draw_x(p, size):
    p.setPen(QPen(ICON_COLOR, 2))
    m = size // 4
    p.drawLine(m, m, size - m, size - m)
    p.drawLine(size - m, m, m, size - m)


def draw_folder(p, size):
    p.setBrush(ICON_COLOR)
    p.setPen(Qt.PenStyle.NoPen)
    m = size // 6
    # Folder body
    p.drawRoundedRect(m, size // 3, size - 2 * m, size // 2, 2, 2)
    # Folder tab
    p.drawRoundedRect(m, size // 4, size // 3, size // 6, 2, 2)


def make_icon(draw_fn, size=ICON_SIZE):
    px = QPixmap(size, size)
    px.fill(Qt.GlobalColor.transparent)
    p = QPainter(px)
    p.setRenderHint(QPainter.RenderHint.Antialiasing)
    draw_fn(p, size)
    p.end()
    return QIcon(px)


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
        if len(self.samples) == 0:
            return
        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)
        w, h = self.width(), self.height()
        cy = h // 2
        chunk = max(1, len(self.samples) // w)
        n = len(self.samples) // chunk
        peaks = np.max(np.abs(self.samples[:n * chunk].reshape(n, chunk)), axis=1)
        p.setPen(QPen(QColor(ACCENT_COLOR.red(), ACCENT_COLOR.green(), ACCENT_COLOR.blue(), 180), 2))
        for x, peak in enumerate(peaks):
            bar = int((peak / self.display_max) * h // 2 * 0.9)
            p.drawLine(x, cy - bar, x, cy + bar)


class VoiceThingWindow(QWidget):
    hide_signal = pyqtSignal()
    toggle_signal = pyqtSignal()
    paste_signal = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.state = STATE_IDLE
        self.audio_chunks = []
        self.stream = None
        self.tee = None
        self.tee_last_len = 0
        self.drag_pos = None
        self.scroll_locked = False
        self.is_focused = False
        self.first_show = True
        self.last_audio_path = None

        self.setWindowTitle(APP_NAME)
        self.setWindowFlags(Qt.WindowType.WindowStaysOnTopHint | Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        font_id = QFontDatabase.addApplicationFont(rp.download_font('R:DSEG7'))
        if font_id < 0:
            raise RuntimeError("Failed to load 7-segment font")
        seg_font = QFontDatabase.applicationFontFamilies(font_id)[0]

        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)

        self.status_label = QLabel("Double-tap Option to record")
        self.status_label.setStyleSheet("color: rgba(255,255,255,0.7); font-size: 14px;")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.status_label)

        self.timer_label = QLabel("")
        self.timer_label.setStyleSheet(f"color: rgba(100,200,255,0.9); font-size: 28px; font-family: '{seg_font}';")
        self.timer_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.timer_label.hide()
        layout.addWidget(self.timer_label)

        btn_row = QHBoxLayout()
        btn_row.setSpacing(8)
        btn_css = (
            "QPushButton { color: rgba(255,255,255,0.6); background: rgba(255,255,255,0.1); "
            "border: 1px solid rgba(255,255,255,0.2); border-radius: 4px; padding: 4px 8px; font-size: 11px; }"
            "QPushButton:hover { background: rgba(255,255,255,0.2); }"
            "QPushButton:disabled { color: rgba(255,255,255,0.2); background: transparent; }"
        )

        def make_btn(text, icon_fn, handler):
            btn = QPushButton(text)
            btn.setIcon(make_icon(icon_fn))
            btn.setIconSize(QSize(24, 24))
            btn.setStyleSheet(btn_css)
            btn.clicked.connect(handler)
            btn.setEnabled(False)
            btn_row.addWidget(btn)
            return btn

        self.record_btn = make_btn("", draw_mic, self.toggle_recording)
        self.record_btn.setEnabled(True)
        self.cancel_btn = make_btn("Esc", draw_x, self.cancel_recording)
        self.folder_btn = make_btn("", draw_folder, self.open_recordings_folder)
        layout.addLayout(btn_row)

        self.waveform = WaveformWidget()
        layout.addWidget(self.waveform)

        self.log_output = QLabel("")
        self.log_output.setStyleSheet(
            "color: #b0b0b0; font-size: 11px; font-family: 'SF Mono', Menlo, monospace; "
            "background: rgba(20,20,30,200); padding: 8px; border-radius: 8px;")
        self.log_output.setWordWrap(True)
        self.log_output.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidget(self.log_output)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.scroll_area.setStyleSheet(
            "QScrollArea { background: transparent; border: none; }"
            "QScrollBar:vertical { width: 6px; background: transparent; }"
            "QScrollBar::handle:vertical { background: rgba(255,255,255,0.2); border-radius: 3px; }"
            "QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical { height: 0; }"
        )
        self.scroll_area.verticalScrollBar().valueChanged.connect(self._on_scroll)
        layout.addWidget(self.scroll_area)

        self.setFixedSize(400, 350)
        self.hide_signal.connect(self._maybe_hide)
        self.toggle_signal.connect(self.toggle_recording)
        self.paste_signal.connect(self._do_paste)

        self.update_timer = QTimer()
        self.update_timer.timeout.connect(self._update_display)
        self._setup_tray()

    def _setup_tray(self):
        self.tray = QSystemTrayIcon(self)
        px = QPixmap(22, 22)
        px.fill(Qt.GlobalColor.transparent)
        p = QPainter(px)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)
        p.setBrush(ACCENT_COLOR)
        p.setPen(Qt.PenStyle.NoPen)
        p.drawEllipse(6, 2, 10, 14)
        p.drawRect(9, 14, 4, 4)
        p.end()
        self.tray.setIcon(QIcon(px))
        menu = QMenu()
        menu.addAction("Show", self.show)
        menu.addAction("Quit", QApplication.quit)
        self.tray.setContextMenu(menu)
        self.tray.setToolTip(APP_NAME)
        self.tray.show()

    def _maybe_hide(self):
        if not self.is_focused and not self.scroll_locked:
            self.hide()

    def _on_scroll(self):
        sb = self.scroll_area.verticalScrollBar()
        was_locked = self.scroll_locked
        self.scroll_locked = sb.value() < sb.maximum() - 10
        if self.scroll_locked != was_locked:
            self.update()

    def _append_log(self, text):
        self.log_output.setText((self.log_output.text() + "\n" + text).strip())
        if not self.scroll_locked:
            QTimer.singleShot(10, lambda: self.scroll_area.verticalScrollBar().setValue(
                self.scroll_area.verticalScrollBar().maximum()))

    def _do_paste(self, text):
        rp.string_to_clipboard(text)
        if self.is_focused:
            return
        rp.play_chords([12, 16], gap=0, t=0.05)
        time.sleep(0.1)
        kb = KeyboardController()
        with kb.pressed(Key.cmd):
            kb.tap('v')

    def _update_display(self):
        if self.audio_chunks:
            audio = np.concatenate(self.audio_chunks)
            self.waveform.set_samples(audio)
            secs = len(audio) / SAMPLE_RATE
            self.timer_label.setText(f"{int(secs // 60)}:{secs % 60:05.2f}")
        if self.tee and len(self.tee.text) > self.tee_last_len:
            for line in self.tee.text[self.tee_last_len:].split("\n"):
                if line.strip():
                    self._append_log(line)
            self.tee_last_len = len(self.tee.text)

    def mousePressEvent(self, e):
        if e.button() == Qt.MouseButton.LeftButton:
            self.drag_pos = e.globalPosition().toPoint() - self.frameGeometry().topLeft()

    def mouseMoveEvent(self, e):
        if self.drag_pos and e.buttons() & Qt.MouseButton.LeftButton:
            self.move(e.globalPosition().toPoint() - self.drag_pos)

    def mouseReleaseEvent(self, e):
        self.drag_pos = None

    def changeEvent(self, e):
        if e.type() == e.Type.ActivationChange:
            self.is_focused = self.isActiveWindow()
        super().changeEvent(e)

    def keyPressEvent(self, e):
        if e.key() == Qt.Key.Key_Escape and self.state == STATE_RECORDING:
            self.cancel_recording()
        else:
            super().keyPressEvent(e)

    def paintEvent(self, e):
        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)
        p.setBrush(QColor(30, 30, 40, 220))
        p.setPen(Qt.PenStyle.NoPen)
        p.drawRoundedRect(self.rect().adjusted(2, 2, -2, -2), 12, 12)
        if self.is_focused or self.scroll_locked:
            color = QColor(255, 150, 50, 150) if self.scroll_locked else QColor(100, 200, 255, 100)
            p.setBrush(Qt.BrushStyle.NoBrush)
            p.setPen(QPen(color, 3))
            p.drawRoundedRect(self.rect().adjusted(2, 2, -2, -2), 12, 12)

    def _cleanup_stream(self):
        if self.stream:
            self.stream.stop()
            self.stream.close()
            self.stream = None

    def _cleanup_tee(self):
        if self.tee:
            self.tee.__exit__(None, None, None)
            self.tee = None
        self.update_timer.stop()

    def toggle_recording(self):
        if self.state == STATE_IDLE:
            self.start_recording()
        elif self.state == STATE_RECORDING:
            self.stop_recording()
        else:
            # Transcribing - play "no" chime
            rp.play_chords([3, 0], gap=0, t=0.08)

    def cancel_recording(self):
        if self.state != STATE_RECORDING:
            return
        self.state = STATE_IDLE
        self._cleanup_stream()
        self._cleanup_tee()
        self._update_buttons()
        self.timer_label.hide()
        self.audio_chunks = []
        self.waveform.set_samples(np.array([]))
        self.status_label.setText("Cancelled")
        rp.play_chords([7, 3], gap=0, t=0.06)
        self.hide_signal.emit()

    def _update_buttons(self):
        if self.state == STATE_IDLE:
            self.record_btn.setIcon(make_icon(draw_mic))
            self.record_btn.setEnabled(True)
            self.cancel_btn.setEnabled(False)
        elif self.state == STATE_RECORDING:
            self.record_btn.setIcon(make_icon(draw_stop))
            self.record_btn.setEnabled(True)
            self.cancel_btn.setEnabled(True)
        else:  # STATE_TRANSCRIBING
            self.record_btn.setEnabled(False)
            self.cancel_btn.setEnabled(False)

    def open_recordings_folder(self):
        os.makedirs(RECORDINGS_DIR, exist_ok=True)
        if self.last_audio_path and os.path.exists(self.last_audio_path):
            subprocess.run(["open", "-R", self.last_audio_path])
        else:
            subprocess.run(["open", RECORDINGS_DIR])

    def start_recording(self):
        self.state = STATE_RECORDING
        self.audio_chunks = []
        self.tee = rp.TeeStdout()
        self.tee.__enter__()
        self.tee_last_len = 0
        self.show()
        if self.first_show:
            screen = QApplication.primaryScreen().geometry()
            self.move((screen.width() - self.width()) // 2, screen.height() // 4)
            self.first_show = False
        self.status_label.setText("Recording")
        self.timer_label.setText("0:00.00")
        self.timer_label.show()
        self._update_buttons()
        rp.play_chords([0, 4], [7, 12], gap=0, t=0.08)

        def callback(indata, frames, time_info, status):
            self.audio_chunks.append(indata[:, 0].copy())

        self.stream = sd.InputStream(samplerate=SAMPLE_RATE, channels=1, dtype=np.float32, callback=callback)
        self.stream.start()
        self.update_timer.start(8)

    def stop_recording(self):
        self.state = STATE_TRANSCRIBING
        self._cleanup_stream()
        self._update_buttons()
        rp.play_chords([12, 7], [4, 0], gap=0, t=0.08)
        self.timer_label.hide()
        self.status_label.setText("Transcribing...")
        audio = np.concatenate(self.audio_chunks) if self.audio_chunks else np.array([])
        self.waveform.set_samples(audio)
        threading.Thread(target=self._transcribe, args=(audio,), daemon=True).start()

    def _transcribe(self, audio):
        if len(audio) == 0:
            print("No audio.")
            self._finish_transcription()
            return
        print(f"Recorded {len(audio) / SAMPLE_RATE:.2f}s")

        os.makedirs(RECORDINGS_DIR, exist_ok=True)
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        wav_path = os.path.join(RECORDINGS_DIR, f"{timestamp}.wav")
        txt_path = os.path.join(RECORDINGS_DIR, f"{timestamp}.txt")

        scipy.io.wavfile.write(wav_path, SAMPLE_RATE, (audio * 32767).astype(np.int16))
        self.last_audio_path = wav_path
        result = rp.transcribe_audio_file_via_whisper(wav_path, model=WHISPER_MODEL, show_progress=True)

        print(f"Result: {result.text!r}")
        if result.text:
            with open(txt_path, 'w') as f:
                f.write(result.text)
            self.paste_signal.emit(result.text)

        rp.play_chords([0], [4], [7], [12], gap=0, t=0.08)
        self.folder_btn.setEnabled(True)
        self._finish_transcription()

    def _finish_transcription(self):
        self._cleanup_tee()
        self.state = STATE_IDLE
        self._update_buttons()
        self.status_label.setText("Double-tap Option to record")
        self.hide_signal.emit()


def main():
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    app = QApplication([])
    window = VoiceThingWindow()

    last_tap = [0.0]
    pressed = set()

    def on_press(key):
        pressed.add(key)

    def on_release(key):
        pressed.discard(key)
        if key in (keyboard.Key.alt, keyboard.Key.alt_l, keyboard.Key.alt_r) and len(pressed) == 0:
            now = time.time()
            if now - last_tap[0] < 0.3:
                window.toggle_signal.emit()
                last_tap[0] = 0.0
            else:
                last_tap[0] = now

    keyboard.Listener(on_press=on_press, on_release=on_release).start()

    print(f"Loading Whisper ({WHISPER_MODEL})...")
    rp.r._get_pywhispercpp_model(WHISPER_MODEL)
    rp.play_chords([0, 4, 7], [12], gap=0, t=0.15)
    print(f"{APP_NAME} ready. Double-tap Option to record.")
    app.exec()


if __name__ == "__main__":
    main()
