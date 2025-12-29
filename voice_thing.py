#!/usr/bin/env /opt/homebrew/opt/python@3.10/bin/python3.10
"""Voice transcription app: double-tap Option to record, transcribe, and type."""

import tempfile
import threading
import time

import numpy as np
import scipy.io.wavfile
import sounddevice as sd
import whisper
import rp
from pynput import keyboard
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel
from PyQt6.QtCore import Qt, QTimer, pyqtSignal
from PyQt6.QtGui import QPainter, QColor, QPen

SAMPLE_RATE = 16000
WHISPER_MODEL = None


def get_whisper_model():
    global WHISPER_MODEL
    if WHISPER_MODEL is None:
        print("Loading Whisper model (base)...")
        WHISPER_MODEL = whisper.load_model("base")
        print("Whisper model loaded.")
    return WHISPER_MODEL


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

    def __init__(self):
        super().__init__()
        self.recording = False
        self.audio_chunks = []
        self.stream = None
        self.drag_pos = None

        self.setWindowTitle("Voice Thing")
        self.setFixedSize(400, 150)
        self.setWindowFlags(Qt.WindowType.WindowStaysOnTopHint | Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)

        self.status_label = QLabel("Double-tap Option to record")
        self.status_label.setStyleSheet(
            "color: white; font-size: 14px; background: rgba(30,30,40,200); padding: 5px; border-radius: 5px;"
        )
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.status_label)

        self.waveform = WaveformWidget()
        layout.addWidget(self.waveform)

        self.update_signal.connect(self._update_display)
        self.hide_signal.connect(lambda: QTimer.singleShot(2000, self.hide))
        self.toggle_signal.connect(self.toggle_recording)

        self.update_timer = QTimer()
        self.update_timer.timeout.connect(self._update_display)

    def _update_display(self):
        if self.audio_chunks:
            audio = np.concatenate(self.audio_chunks)
            self.waveform.set_samples(audio)
            self.status_label.setText(f"Recording... {len(audio) / SAMPLE_RATE:.1f}s")

    def mousePressEvent(self, e):
        if e.button() == Qt.MouseButton.LeftButton:
            self.drag_pos = e.globalPosition().toPoint() - self.frameGeometry().topLeft()

    def mouseMoveEvent(self, e):
        if self.drag_pos and e.buttons() & Qt.MouseButton.LeftButton:
            self.move(e.globalPosition().toPoint() - self.drag_pos)

    def mouseReleaseEvent(self, e):
        self.drag_pos = None

    def toggle_recording(self):
        self.stop_recording() if self.recording else self.start_recording()

    def start_recording(self):
        self.recording = True
        self.audio_chunks = []
        self.show()
        screen = QApplication.primaryScreen().geometry()
        self.move((screen.width() - self.width()) // 2, screen.height() // 4)
        self.status_label.setText("Recording... 0.0s")

        rp.play_chords([0, 4], [7, 12], gap=0, t=0.08)  # Rising major
        print("Recording started...")

        def callback(indata, frames, time, status):
            self.audio_chunks.append(indata[:, 0].copy())

        self.stream = sd.InputStream(samplerate=SAMPLE_RATE, channels=1, dtype=np.float32, callback=callback)
        self.stream.start()
        self.update_timer.start(50)

    def stop_recording(self):
        self.recording = False
        self.update_timer.stop()

        if self.stream:
            self.stream.stop()
            self.stream.close()
            self.stream = None

        rp.play_chords([12, 7], [4, 0], gap=0, t=0.08)  # Falling major
        print("Recording stopped.")

        audio = np.concatenate(self.audio_chunks) if self.audio_chunks else np.array([])
        self.waveform.set_samples(audio)
        self.status_label.setText("Transcribing...")

        threading.Thread(target=self._transcribe_and_type, args=(audio,), daemon=True).start()

    def _transcribe_and_type(self, audio: np.ndarray):
        if len(audio) == 0:
            print("No audio recorded.")
            self.hide_signal.emit()
            return

        print(f"Recorded {len(audio) / SAMPLE_RATE:.2f}s of audio.")

        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as f:
            scipy.io.wavfile.write(f.name, SAMPLE_RATE, audio)
            print(f"Saved to {f.name}")

            print("Transcribing...")
            text = get_whisper_model().transcribe(f.name, verbose=True)["text"].strip()

        print(f"Transcription: {text!r}")

        if text:
            print("Typing text...")
            rp.type_string_with_keyboard(text)
            print("Done typing.")

        self.hide_signal.emit()


def main():
    app = QApplication([])
    window = VoiceThingWindow()

    # Double-tap Option (only if no other keys pressed)
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

    get_whisper_model()
    print("Voice Thing running. Double-tap Option to record.")
    app.exec()


if __name__ == "__main__":
    main()
