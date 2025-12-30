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
from PyQt6.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QScrollArea,
    QSystemTrayIcon,
    QMenu,
    QPushButton,
)

APP_NAME = "VoiceThing"
SAMPLE_RATE = 16000
BLOCKSIZE = 1024
WHISPER_MODEL = "large-v3"
ICON_COLOR = QColor(255, 255, 255, 180)
ACCENT = QColor(100, 200, 255)
RECORDINGS_DIR = os.path.join(tempfile.gettempdir(), APP_NAME)


def quiet_sampler(f=None, T=None, samplerate=None):
    return rp.triangle_tone_sampler(f, T, samplerate) * 0.25


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


def draw_folder(p, s):
    p.setBrush(ICON_COLOR)
    p.setPen(Qt.PenStyle.NoPen)
    m = s // 6
    p.drawRoundedRect(m, s // 3, s - 2 * m, s // 2, 2, 2)
    p.drawRoundedRect(m, s // 4, s // 3, s // 6, 2, 2)


def draw_copy(p, s):
    p.setBrush(Qt.BrushStyle.NoBrush)
    p.setPen(QPen(ICON_COLOR, 2))
    m = s // 5
    p.drawRoundedRect(m, m, s // 2, s // 2, 2, 2)
    p.drawRoundedRect(s // 3, s // 3, s // 2, s // 2, 2, 2)


def make_icon(draw_fn, size=64):
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
        p.setPen(QPen(QColor(ACCENT.red(), ACCENT.green(), ACCENT.blue(), 180), 2))
        scale = w / len(self.peaks)
        for i, peak in enumerate(self.peaks):
            x = int(i * scale)
            bar = int((peak / self.display_max) * h // 2 * 0.9)
            p.drawLine(x, cy - bar, x, cy + bar)


class VoiceThingWindow(QWidget):
    hide_signal = pyqtSignal()
    toggle_signal = pyqtSignal()
    paste_signal = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.state = "idle"
        self.audio_chunks = []
        self.stream = None
        self.tee = None
        self.tee_last_len = 0
        self.drag_pos = None
        self.resize_edge = None
        self.scroll_locked = False
        self.is_focused = False
        self.first_show = True
        self.last_audio_path = None
        self.last_transcription = None

        self.setWindowTitle(APP_NAME)
        self.setWindowFlags(
            Qt.WindowType.WindowStaysOnTopHint | Qt.WindowType.FramelessWindowHint
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        font_id = QFontDatabase.addApplicationFont(rp.download_font("R:DSEG7"))
        if font_id < 0:
            raise RuntimeError("Failed to load 7-segment font")
        seg_font = QFontDatabase.applicationFontFamilies(font_id)[0]

        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)

        self.status_label = QLabel("Double-tap Option to record")
        self.status_label.setStyleSheet(
            "color: rgba(255,255,255,0.7); font-size: 14px;"
        )
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.status_label)

        self.timer_label = QLabel("0:00.0")
        self.seg_font = seg_font
        self.timer_label.setStyleSheet(
            f"color: rgba(100,200,255,0.3); font-size: 28px; font-family: '{seg_font}';"
        )
        self.timer_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.timer_label)

        btn_row = QHBoxLayout()
        btn_row.setSpacing(8)
        btn_css = (
            "QPushButton { color: rgba(255,255,255,0.6); background: rgba(255,255,255,0.1); "
            "border: 1px solid rgba(255,255,255,0.2); border-radius: 3px; padding: 1px 2px; font-size: 10px; }"
            "QPushButton:hover { background: rgba(255,255,255,0.2); }"
            "QPushButton:disabled { color: rgba(255,255,255,0.2); background: transparent; }"
        )

        def make_btn(text, icon_fn, handler):
            btn = QPushButton(text)
            btn.setIcon(make_icon(icon_fn))
            btn.setIconSize(QSize(16, 16))
            btn.setStyleSheet(btn_css)
            btn.clicked.connect(handler)
            btn.setEnabled(False)
            btn_row.addWidget(btn)
            return btn

        self.record_btn = make_btn("Space", draw_mic, self.toggle_recording)
        self.record_btn.setEnabled(True)
        self.cancel_btn = make_btn("Esc", draw_x, self.cancel_recording)
        self.copy_btn = make_btn("C", draw_copy, self.copy_transcription)
        self.folder_btn = make_btn("F", draw_folder, self.open_folder)
        layout.addLayout(btn_row)

        self.waveform = WaveformWidget()
        layout.addWidget(self.waveform)

        self.log_output = QLabel("")
        self.log_output.setStyleSheet(
            "color: #b0b0b0; font-size: 11px; font-family: Menlo, monospace;"
            "background: transparent; padding: 8px;"
        )
        self.log_output.setWordWrap(True)
        self.log_output.setAlignment(
            Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft
        )

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidget(self.log_output)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setHorizontalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOff
        )
        self.scroll_area.verticalScrollBar().valueChanged.connect(self._on_scroll)
        self._update_scroll_border()
        layout.addWidget(self.scroll_area)

        self.setMinimumSize(300, 250)
        self.resize(400, 350)
        self.hide_signal.connect(self._maybe_hide)
        self.toggle_signal.connect(self.toggle_recording)
        self.paste_signal.connect(self._do_paste)

        self.update_timer = QTimer()
        self.update_timer.timeout.connect(self._update_display)
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
        if not self.is_focused and not self.scroll_locked:
            self.hide()

    def _on_scroll(self):
        sb = self.scroll_area.verticalScrollBar()
        was_locked = self.scroll_locked
        self.scroll_locked = sb.value() < sb.maximum() - 10
        if self.scroll_locked != was_locked:
            self._update_scroll_border()

    def _update_scroll_border(self):
        border = "2px solid rgba(255,150,50,0.6)" if self.scroll_locked else "none"
        self.scroll_area.setStyleSheet(
            f"QScrollArea {{ background: rgba(20,20,30,200); border: {border}; border-radius: 8px; }}"
            "QScrollBar:vertical { width: 6px; background: transparent; }"
            "QScrollBar::handle:vertical { background: rgba(255,255,255,0.2); border-radius: 3px; }"
            "QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical { height: 0; }"
        )

    def _append_log(self, text):
        self.log_output.setText((self.log_output.text() + "\n" + text).strip())
        if not self.scroll_locked:
            QTimer.singleShot(
                10,
                lambda: self.scroll_area.verticalScrollBar().setValue(
                    self.scroll_area.verticalScrollBar().maximum()
                ),
            )

    def _copy_to_clipboard(self, text):
        rp.string_to_clipboard(text)
        rp.play_chords([12, 16], gap=0, t=0.05, sampler=quiet_sampler)

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
        if self.tee and len(self.tee.text) > self.tee_last_len:
            for line in self.tee.text[self.tee_last_len :].split("\n"):
                if line.strip():
                    self._append_log(line)
            self.tee_last_len = len(self.tee.text)

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
        super().changeEvent(e)

    def keyPressEvent(self, e):
        key = e.key()
        if key == Qt.Key.Key_Escape and self.state == "recording":
            self.cancel_recording()
        elif key == Qt.Key.Key_Space:
            self.toggle_recording()
        elif key == Qt.Key.Key_C:
            self.copy_transcription()
        elif key == Qt.Key.Key_F:
            self.open_folder()
        else:
            super().keyPressEvent(e)

    def paintEvent(self, e):
        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)
        p.setBrush(QColor(30, 30, 40, 220))
        p.setPen(Qt.PenStyle.NoPen)
        p.drawRoundedRect(self.rect().adjusted(2, 2, -2, -2), 12, 12)
        if self.is_focused:
            p.setBrush(Qt.BrushStyle.NoBrush)
            p.setPen(QPen(QColor(100, 200, 255, 100), 3))
            p.drawRoundedRect(self.rect().adjusted(2, 2, -2, -2), 12, 12)

    def _cleanup(self):
        if self.stream:
            self.stream.stop()
            self.stream.close()
            self.stream = None
        if self.tee:
            self.tee.__exit__(None, None, None)
            self.tee = None
        self.update_timer.stop()

    def _update_buttons(self):
        recording = self.state == "recording"
        self.record_btn.setIcon(make_icon(draw_stop if recording else draw_mic))
        self.record_btn.setEnabled(self.state != "transcribing")
        self.cancel_btn.setEnabled(recording)
        self.copy_btn.setEnabled(self.last_transcription is not None)
        self.folder_btn.setEnabled(True)

    def toggle_recording(self):
        if self.state == "idle":
            self.start_recording()
        elif self.state == "recording":
            self.stop_recording()
        else:
            rp.play_chords([3, 0], gap=0, t=0.08, sampler=quiet_sampler)

    def cancel_recording(self):
        if self.state != "recording":
            return
        self._cleanup()
        self._set_state("idle", "Cancelled")
        self.audio_chunks = []
        self.waveform.set_samples(np.array([]))
        rp.play_chords([7, 3], gap=0, t=0.06, sampler=quiet_sampler)
        self.hide_signal.emit()

    def _set_state(self, state, status):
        self.state = state
        self.status_label.setText(status)
        opacity = 0.9 if state == "recording" else 0.3
        self.timer_label.setStyleSheet(
            f"color: rgba(100,200,255,{opacity}); font-size: 28px; font-family: '{self.seg_font}';"
        )
        self._update_buttons()

    def copy_transcription(self):
        if self.last_transcription:
            self._copy_to_clipboard(self.last_transcription)

    def open_folder(self):
        os.makedirs(RECORDINGS_DIR, exist_ok=True)
        if self.last_audio_path and os.path.exists(self.last_audio_path):
            subprocess.run(["open", "-R", self.last_audio_path])
        else:
            subprocess.run(["open", RECORDINGS_DIR])

    def start_recording(self):
        self.audio_chunks = []
        self.tee = rp.TeeStdout()
        self.tee.__enter__()
        self.tee_last_len = 0
        self.show()
        if self.first_show:
            screen = QApplication.primaryScreen().geometry()
            self.move((screen.width() - self.width()) // 2, screen.height() // 4)
            self.first_show = False
        self.timer_label.setText("0:00.0")
        self._set_state("recording", "Recording")
        rp.play_chords([0, 4], [7, 12], gap=0, t=0.08, sampler=quiet_sampler)

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
        rp.play_chords([12, 7], [4, 0], gap=0, t=0.08, sampler=quiet_sampler)
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
            wav_path, model=WHISPER_MODEL, show_progress=True
        )

        print(f"Result: {result.text!r}")
        if result.text:
            with open(txt_path, "w") as f:
                f.write(result.text)
            self.last_transcription = result.text
            self.paste_signal.emit(result.text)

        rp.play_chords([0], [4], [7], [12], gap=0, t=0.08, sampler=quiet_sampler)
        self._finish()

    def _finish(self):
        self._cleanup()
        self._set_state("idle", "Double-tap Option to record")
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
        if (
            key in (keyboard.Key.alt, keyboard.Key.alt_l, keyboard.Key.alt_r)
            and len(pressed) == 0
        ):
            now = time.time()
            if now - last_tap[0] < 0.3:
                window.toggle_signal.emit()
                last_tap[0] = 0.0
            else:
                last_tap[0] = now

    keyboard.Listener(on_press=on_press, on_release=on_release).start()

    print(f"Loading Whisper ({WHISPER_MODEL})...")
    rp.r._get_pywhispercpp_model(WHISPER_MODEL)
    rp.play_chords([0, 4, 7], [12], gap=0, t=0.15, sampler=quiet_sampler)
    print(f"{APP_NAME} ready. Double-tap Option to record.")
    app.exec()


if __name__ == "__main__":
    main()
