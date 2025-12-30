"""UI components for voice transcription."""

import tempfile
import threading
import time

import numpy as np
import scipy.io.wavfile
import sounddevice as sd
import rp
from pynput.keyboard import Controller as KeyboardController, Key
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QScrollArea, QSystemTrayIcon, QMenu
from PyQt6.QtCore import Qt, QTimer, pyqtSignal
from PyQt6.QtGui import QPainter, QColor, QPen, QIcon, QPixmap, QFontDatabase
import os

SAMPLE_RATE = 16000


class RoundedScrollArea(QScrollArea):
    """ScrollArea with properly rounded corners via custom painting."""

    def __init__(self, border_color=None):
        super().__init__()
        self.border_color = border_color
        self.setWidgetResizable(True)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setStyleSheet(
            "QScrollArea { background: transparent; border: none; }"
            "QScrollBar:vertical { width: 6px; background: transparent; }"
            "QScrollBar::handle:vertical { background: rgba(255,255,255,0.2); border-radius: 3px; min-height: 20px; }"
            "QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical { height: 0; }"
        )

    def set_border_color(self, color):
        self.border_color = color
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self.viewport())
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        # Background
        painter.setBrush(QColor(20, 20, 30, 200))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawRoundedRect(self.viewport().rect(), 8, 8)

        # Border if set
        if self.border_color:
            painter.setBrush(Qt.BrushStyle.NoBrush)
            painter.setPen(QPen(self.border_color, 2))
            r = self.viewport().rect().adjusted(1, 1, -1, -1)
            painter.drawRoundedRect(r, 7, 7)

        painter.end()
        super().paintEvent(event)


class WaveformWidget(QWidget):
    """Displays last 10 seconds of audio waveform with smooth amplitude."""

    def __init__(self):
        super().__init__()
        self.samples = np.array([])
        self.display_max = 0.01  # Current display amplitude (smoothed)
        self.setMinimumHeight(100)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

    def set_samples(self, samples: np.ndarray):
        max_samples = 10 * SAMPLE_RATE
        self.samples = samples[-max_samples:] if len(samples) > max_samples else samples

        # Symmetric exponential smoothing for amplitude (same speed up and down)
        if len(self.samples) > 0:
            current_max = max(np.max(np.abs(self.samples)), 0.01)
            # Smooth towards target (~1.5 sec at 120hz, same for louder and quieter)
            self.display_max += (current_max - self.display_max) * 0.04

        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        # Transparent background
        painter.fillRect(self.rect(), Qt.GlobalColor.transparent)

        if len(self.samples) == 0:
            return

        w, h = self.width(), self.height()
        center_y = h // 2
        chunk_size = max(1, len(self.samples) // w)
        n = len(self.samples) // chunk_size
        peaks = np.max(np.abs(self.samples[:n * chunk_size].reshape(n, chunk_size)), axis=1)

        # Gradient density waveform - draw multiple layers with decreasing alpha
        max_bar = int(h // 2 * 0.9)
        for x, peak in enumerate(peaks):
            bar = int((peak / self.display_max) * max_bar)
            if bar < 1:
                continue
            # Draw gradient: bright at center, fading outward
            for y_offset in range(bar):
                # Alpha decreases as we move away from center
                alpha = int(200 * (1 - y_offset / max_bar))
                painter.setPen(QPen(QColor(100, 200, 255, alpha), 1))
                painter.drawPoint(x, center_y - y_offset)
                painter.drawPoint(x, center_y + y_offset)


class VoiceThingWindow(QWidget):
    """Main window: draggable, shows waveform and status."""

    update_signal = pyqtSignal()
    hide_signal = pyqtSignal()
    toggle_signal = pyqtSignal()
    paste_signal = pyqtSignal(str)
    log_signal = pyqtSignal(str)

    def __init__(self, whisper_model_name="large-v3"):
        super().__init__()
        self.whisper_model_name = whisper_model_name
        self.recording = False
        self.audio_chunks = []
        self.stream = None
        self.drag_pos = None
        self.tee = None
        self.tee_last_len = 0
        self.scroll_locked = False
        self.is_focused = False

        self.setWindowTitle("Voice Thing")
        self.setWindowFlags(Qt.WindowType.WindowStaysOnTopHint | Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        # Load 7-segment font
        font_path = os.path.join(os.path.dirname(__file__), "fonts", "DSEG7Classic-Regular.ttf")
        QFontDatabase.addApplicationFont(font_path)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)

        self.status_label = QLabel("Double-tap Option to record")
        self.status_label.setStyleSheet(
            "color: rgba(255,255,255,0.7); font-size: 14px; font-weight: 500; "
            "background: transparent; padding: 4px 12px;"
        )
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.status_label)

        self.timer_label = QLabel("")
        self.timer_label.setStyleSheet(
            "color: rgba(100,200,255,0.9); font-size: 28px; font-family: 'DSEG7 Classic'; "
            "background: transparent; padding: 0px;"
        )
        self.timer_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.timer_label.hide()
        layout.addWidget(self.timer_label)

        self.waveform = WaveformWidget()
        layout.addWidget(self.waveform)

        self.log_output = QLabel("")
        self.log_output.setStyleSheet(
            "color: #b0b0b0; font-size: 11px; font-family: 'SF Mono', Menlo, monospace; "
            "background: transparent; padding: 8px; line-height: 1.4;"
        )
        self.log_output.setWordWrap(True)
        self.log_output.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)

        self.scroll_area = RoundedScrollArea()
        self.scroll_area.setWidget(self.log_output)
        self.scroll_area.verticalScrollBar().valueChanged.connect(self._on_scroll)
        layout.addWidget(self.scroll_area)

        self.setFixedSize(400, 350)

        self.update_signal.connect(self._update_display)
        self.hide_signal.connect(self._maybe_hide)
        self.toggle_signal.connect(self.toggle_recording)
        self.paste_signal.connect(self._do_paste)
        self.log_signal.connect(self._append_log)

        self.update_timer = QTimer()
        self.update_timer.timeout.connect(self._update_display)

        self._setup_tray()

    def _setup_tray(self):
        self.tray = QSystemTrayIcon(self)
        # Create simple mic icon
        pixmap = QPixmap(22, 22)
        pixmap.fill(Qt.GlobalColor.transparent)
        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setBrush(QColor(100, 200, 255))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawEllipse(6, 2, 10, 14)
        painter.drawRect(9, 14, 4, 4)
        painter.end()
        self.tray.setIcon(QIcon(pixmap))

        menu = QMenu()
        menu.addAction("Show", self.show)
        menu.addAction("Quit", QApplication.quit)
        self.tray.setContextMenu(menu)
        self.tray.setToolTip("Voice Thing")
        self.tray.show()

    def _maybe_hide(self):
        if not self.is_focused and not self.scroll_locked:
            QTimer.singleShot(2000, self.hide)

    def _on_scroll(self):
        scrollbar = self.scroll_area.verticalScrollBar()
        at_bottom = scrollbar.value() >= scrollbar.maximum() - 10
        was_locked = self.scroll_locked
        self.scroll_locked = not at_bottom

        if self.scroll_locked != was_locked:
            color = QColor(255, 150, 50, 150) if self.scroll_locked else None
            self.scroll_area.set_border_color(color)

    def _append_log(self, text: str):
        current = self.log_output.text()
        self.log_output.setText((current + "\n" + text).strip())
        if not self.scroll_locked:
            QTimer.singleShot(10, lambda: self.scroll_area.verticalScrollBar().setValue(
                self.scroll_area.verticalScrollBar().maximum()))

    def _do_paste(self, text: str):
        rp.string_to_clipboard(text)
        if self.is_focused:
            # Don't paste into our own window
            return
        time.sleep(0.1)
        kb = KeyboardController()
        with kb.pressed(Key.cmd):
            kb.tap('v')
        time.sleep(0.1)

    def _update_display(self):
        if self.audio_chunks:
            audio = np.concatenate(self.audio_chunks)
            self.waveform.set_samples(audio)
            secs = len(audio) / SAMPLE_RATE
            mins = int(secs // 60)
            secs_remaining = secs % 60
            self.timer_label.setText(f"{mins}:{secs_remaining:05.2f}")
        if self.tee and len(self.tee.text) > self.tee_last_len:
            new_text = self.tee.text[self.tee_last_len:]
            for line in new_text.split("\n"):
                if line.strip():
                    self.log_signal.emit(line)
            self.tee_last_len = len(self.tee.text)

    def mousePressEvent(self, e):
        if e.button() == Qt.MouseButton.LeftButton:
            self.drag_pos = e.globalPosition().toPoint() - self.frameGeometry().topLeft()

    def mouseMoveEvent(self, e):
        if self.drag_pos and e.buttons() & Qt.MouseButton.LeftButton:
            self.move(e.globalPosition().toPoint() - self.drag_pos)

    def mouseReleaseEvent(self, e):
        self.drag_pos = None

    def focusInEvent(self, e):
        self.is_focused = True
        self.update()
        super().focusInEvent(e)

    def focusOutEvent(self, e):
        self.is_focused = False
        self.update()
        super().focusOutEvent(e)

    def changeEvent(self, e):
        if e.type() == e.Type.ActivationChange:
            self.is_focused = self.isActiveWindow()
            self.update()
        super().changeEvent(e)

    def paintEvent(self, e):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        # Background
        painter.setBrush(QColor(30, 30, 40, 220))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawRoundedRect(self.rect().adjusted(2, 2, -2, -2), 12, 12)

        # Glow border when focused
        if self.is_focused:
            painter.setBrush(Qt.BrushStyle.NoBrush)
            pen = QPen(QColor(100, 200, 255, 100), 3)
            painter.setPen(pen)
            painter.drawRoundedRect(self.rect().adjusted(2, 2, -2, -2), 12, 12)

        painter.end()

    def toggle_recording(self):
        print(f"toggle_recording called, recording={self.recording}")
        self.stop_recording() if self.recording else self.start_recording()

    def start_recording(self):
        self.recording = True
        self.audio_chunks = []
        self.tee = rp.TeeStdout()
        self.tee.__enter__()
        self.tee_last_len = 0
        self.show()
        screen = QApplication.primaryScreen().geometry()
        self.move((screen.width() - self.width()) // 2, screen.height() // 4)
        self.status_label.setText("Recording")
        self.timer_label.setText("0:00.00")
        self.timer_label.show()

        rp.play_chords([0, 4], [7, 12], gap=0, t=0.08)
        print("Recording started...")

        def callback(indata, frames, time, status):
            if status:
                print(f"Audio callback status: {status}")
            self.audio_chunks.append(indata[:, 0].copy())

        self.stream = sd.InputStream(samplerate=SAMPLE_RATE, channels=1, dtype=np.float32, callback=callback)
        self.stream.start()
        self.update_timer.start(8)  # ~120hz for smooth waveform

    def stop_recording(self):
        self.recording = False

        if self.stream:
            self.stream.stop()
            self.stream.close()
            self.stream = None

        rp.play_chords([12, 7], [4, 0], gap=0, t=0.08)
        print("Recording stopped.")
        self.timer_label.hide()
        self.status_label.setText("Transcribing...")

        audio = np.concatenate(self.audio_chunks) if self.audio_chunks else np.array([])
        self.waveform.set_samples(audio)

        threading.Thread(target=self._transcribe_and_type, args=(audio,), daemon=True).start()

    def _log(self, msg: str):
        print(msg)
        self.log_signal.emit(msg)

    def _transcribe_and_type(self, audio: np.ndarray):
        self._log(f"Audio: {len(audio)} samples")
        if len(audio) == 0:
            self._log("No audio recorded.")
            self.hide_signal.emit()
            return

        self._log(f"Recorded {len(audio) / SAMPLE_RATE:.2f}s")

        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as f:
            # Convert float32 to int16 for pywhispercpp compatibility
            audio_int16 = (audio * 32767).astype(np.int16)
            scipy.io.wavfile.write(f.name, SAMPLE_RATE, audio_int16)
            self._log(f"Saved: {f.name}")

            self._log("Transcribing...")
            result = rp.transcribe_audio_file_via_whisper(f.name, model=self.whisper_model_name, show_progress=True)
            text = result.text

        self._log(f"Result: {text!r}")

        if text:
            print("Emitting paste signal...")
            self.paste_signal.emit(text)

        if self.tee:
            self.tee.__exit__(None, None, None)
            self.tee = None
        self.update_timer.stop()

        self.hide_signal.emit()
