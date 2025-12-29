"""UI components for voice transcription."""

import tempfile
import threading
import time

import numpy as np
import scipy.io.wavfile
import sounddevice as sd
import rp
from pynput.keyboard import Controller as KeyboardController, Key
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QScrollArea
from PyQt6.QtCore import Qt, QTimer, pyqtSignal
from PyQt6.QtGui import QPainter, QColor, QPen

SAMPLE_RATE = 16000


class WaveformWidget(QWidget):
    """Displays last 10 seconds of audio waveform."""

    def __init__(self):
        super().__init__()
        self.samples = np.array([])
        self.setMinimumHeight(100)

    def set_samples(self, samples: np.ndarray):
        max_samples = 10 * SAMPLE_RATE
        self.samples = samples[-max_samples:] if len(samples) > max_samples else samples
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.fillRect(self.rect(), QColor(30, 30, 40))

        if len(self.samples) == 0:
            return

        w, h = self.width(), self.height()
        chunk_size = max(1, len(self.samples) // w)
        n = len(self.samples) // chunk_size
        peaks = np.max(np.abs(self.samples[:n * chunk_size].reshape(n, chunk_size)), axis=1)
        max_peak = max(np.max(peaks), 1e-6)

        painter.setPen(QPen(QColor(100, 200, 255), 2))
        for x, peak in enumerate(peaks):
            bar = int((peak / max_peak) * h // 2 * 0.9)
            painter.drawLine(x, h // 2 - bar, x, h // 2 + bar)


class VoiceThingWindow(QWidget):
    """Main window: draggable, shows waveform and status."""

    update_signal = pyqtSignal()
    hide_signal = pyqtSignal()
    toggle_signal = pyqtSignal()
    paste_signal = pyqtSignal(str)
    log_signal = pyqtSignal(str)

    def __init__(self, get_whisper_model):
        super().__init__()
        self.get_whisper_model = get_whisper_model
        self.recording = False
        self.audio_chunks = []
        self.stream = None
        self.drag_pos = None
        self.expanded = False
        self.tee = None
        self.tee_last_len = 0

        self.setWindowTitle("Voice Thing")
        self.setWindowFlags(Qt.WindowType.WindowStaysOnTopHint | Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)

        self.status_label = QLabel("Double-tap Option to record")
        self.status_label.setStyleSheet(
            "color: white; font-size: 14px; background: rgba(30,30,40,200); padding: 5px; border-radius: 5px;"
        )
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.status_label.mousePressEvent = lambda e: self._toggle_expand()
        layout.addWidget(self.status_label)

        self.waveform = WaveformWidget()
        layout.addWidget(self.waveform)

        self.log_output = QLabel("")
        self.log_output.setStyleSheet(
            "color: #aaa; font-size: 11px; font-family: monospace; background: rgba(20,20,30,220); padding: 8px;"
        )
        self.log_output.setWordWrap(True)
        self.log_output.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidget(self.log_output)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setStyleSheet("background: rgba(20,20,30,220); border: none; border-radius: 5px;")
        layout.addWidget(self.scroll_area)

        self.expanded = True
        self._update_size()

        self.update_signal.connect(self._update_display)
        self.hide_signal.connect(lambda: QTimer.singleShot(2000, self.hide))
        self.toggle_signal.connect(self.toggle_recording)
        self.paste_signal.connect(self._do_paste)
        self.log_signal.connect(self._append_log)

        self.update_timer = QTimer()
        self.update_timer.timeout.connect(self._update_display)

    def _toggle_expand(self):
        self.expanded = not self.expanded
        self.scroll_area.setVisible(self.expanded)
        self._update_size()

    def _update_size(self):
        self.setFixedSize(400, 350 if self.expanded else 150)

    def _append_log(self, text: str):
        current = self.log_output.text()
        self.log_output.setText((current + "\n" + text).strip())
        self.scroll_area.verticalScrollBar().setValue(self.scroll_area.verticalScrollBar().maximum())

    def _do_paste(self, text: str):
        print(f"_do_paste on main thread: {text!r}")
        rp.string_to_clipboard(text)
        time.sleep(0.1)
        kb = KeyboardController()
        with kb.pressed(Key.cmd):
            kb.tap('v')
        time.sleep(0.1)
        print("Paste done.")

    def _update_display(self):
        if self.audio_chunks:
            audio = np.concatenate(self.audio_chunks)
            self.waveform.set_samples(audio)
            self.status_label.setText(f"Recording... {len(audio) / SAMPLE_RATE:.1f}s")
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
        self.status_label.setText("Recording... 0.0s")

        rp.play_chords([0, 4], [7, 12], gap=0, t=0.08)
        print("Recording started...")

        def callback(indata, frames, time, status):
            if status:
                print(f"Audio callback status: {status}")
            self.audio_chunks.append(indata[:, 0].copy())

        self.stream = sd.InputStream(samplerate=SAMPLE_RATE, channels=1, dtype=np.float32, callback=callback)
        self.stream.start()
        self.update_timer.start(50)

    def stop_recording(self):
        self.recording = False

        if self.stream:
            self.stream.stop()
            self.stream.close()
            self.stream = None

        rp.play_chords([12, 7], [4, 0], gap=0, t=0.08)
        print("Recording stopped.")

        audio = np.concatenate(self.audio_chunks) if self.audio_chunks else np.array([])
        self.waveform.set_samples(audio)
        self.status_label.setText("Transcribing...")

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
            scipy.io.wavfile.write(f.name, SAMPLE_RATE, audio)
            self._log(f"Saved: {f.name}")

            self._log("Transcribing...")
            result = self.get_whisper_model().transcribe(f.name, verbose=True)
            text = result["text"].strip()

        self._log(f"Result: {text!r}")

        if text:
            print("Emitting paste signal...")
            self.paste_signal.emit(text)

        if self.tee:
            self.tee.__exit__(None, None, None)
            self.tee = None
        self.update_timer.stop()

        self.hide_signal.emit()
