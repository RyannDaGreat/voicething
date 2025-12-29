#!/usr/bin/env /opt/homebrew/opt/python@3.10/bin/python3.10
"""Voice transcription app with hotkey, waveform display, and auto-typing."""

import tempfile
import threading
import numpy as np
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
    """Load whisper model once and cache it."""
    global WHISPER_MODEL
    if WHISPER_MODEL is None:
        print("Loading Whisper model (base)...")
        WHISPER_MODEL = whisper.load_model("base")
        print("Whisper model loaded.")
    return WHISPER_MODEL


BEEP_DURATION = 0.08
BEEP_FREQ_HIGH = 880
BEEP_FREQ_LOW = 440


def make_beep(freq: float, duration: float = BEEP_DURATION) -> np.ndarray:
    """Generate a beep tone."""
    t = np.linspace(0, duration, int(SAMPLE_RATE * duration), False)
    return (0.3 * np.sin(2 * np.pi * freq * t)).astype(np.float32)


def play_boop_beep():
    """Play low-high sound (start recording)."""
    sound = np.concatenate([make_beep(BEEP_FREQ_LOW), make_beep(BEEP_FREQ_HIGH)])
    sd.play(sound, SAMPLE_RATE)
    sd.wait()


def play_beep_boop():
    """Play high-low sound (stop recording)."""
    sound = np.concatenate([make_beep(BEEP_FREQ_HIGH), make_beep(BEEP_FREQ_LOW)])
    sd.play(sound, SAMPLE_RATE)
    sd.wait()


class WaveformWidget(QWidget):
    """Widget displaying audio waveform."""

    def __init__(self):
        super().__init__()
        self.samples = np.array([])
        self.setMinimumHeight(100)

    def set_samples(self, samples: np.ndarray):
        self.samples = samples
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        # Background
        painter.fillRect(self.rect(), QColor(30, 30, 40))

        if len(self.samples) == 0:
            return

        # Downsample for display
        width = self.width()
        height = self.height()
        center_y = height // 2

        chunk_size = max(1, len(self.samples) // width)
        display_samples = self.samples[: chunk_size * width].reshape(-1, chunk_size)
        peaks = np.max(np.abs(display_samples), axis=1)

        # Draw waveform
        pen = QPen(QColor(100, 200, 255))
        pen.setWidth(2)
        painter.setPen(pen)

        max_peak = np.max(peaks) if np.max(peaks) > 0 else 1
        for x, peak in enumerate(peaks):
            bar_height = int((peak / max_peak) * center_y * 0.9)
            painter.drawLine(x, center_y - bar_height, x, center_y + bar_height)


class VoiceThingWindow(QWidget):
    """Main window for voice transcription."""

    update_signal = pyqtSignal()
    hide_signal = pyqtSignal()
    toggle_signal = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.recording = False
        self.audio_chunks = []
        self.stream = None

        self.setWindowTitle("Voice Thing")
        self.setFixedSize(400, 150)
        self.setWindowFlags(
            Qt.WindowType.WindowStaysOnTopHint | Qt.WindowType.FramelessWindowHint
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)

        self.status_label = QLabel("Double-tap Option to record")
        self.status_label.setStyleSheet(
            "color: white; font-size: 14px; background: rgba(30,30,40,200); "
            "padding: 5px; border-radius: 5px;"
        )
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.status_label)

        self.waveform = WaveformWidget()
        self.waveform.setStyleSheet("border-radius: 5px;")
        layout.addWidget(self.waveform)

        self.update_signal.connect(self._update_waveform)
        self.hide_signal.connect(self._delayed_hide)
        self.toggle_signal.connect(self.toggle_recording)

        self.update_timer = QTimer()
        self.update_timer.timeout.connect(self._refresh_waveform)

    def _update_waveform(self):
        if self.audio_chunks:
            all_audio = np.concatenate(self.audio_chunks)
            self.waveform.set_samples(all_audio)

    def _refresh_waveform(self):
        self.update_signal.emit()

    def _delayed_hide(self):
        QTimer.singleShot(2000, self.hide)

    def toggle_recording(self):
        if not self.recording:
            self.start_recording()
        else:
            self.stop_recording()

    def start_recording(self):
        self.recording = True
        self.audio_chunks = []
        self.show()
        self.center_on_screen()
        self.status_label.setText("Recording... (double-tap Option to stop)")

        play_boop_beep()
        print("Recording started...")

        def audio_callback(indata, frames, time, status):
            self.audio_chunks.append(indata[:, 0].copy())

        self.stream = sd.InputStream(
            samplerate=SAMPLE_RATE,
            channels=1,
            dtype=np.float32,
            callback=audio_callback,
        )
        self.stream.start()
        self.update_timer.start(50)

    def stop_recording(self):
        self.recording = False
        self.update_timer.stop()

        if self.stream:
            self.stream.stop()
            self.stream.close()
            self.stream = None

        play_beep_boop()
        print("Recording stopped.")

        self.status_label.setText("Transcribing...")
        self._update_waveform()

        threading.Thread(target=self._transcribe_and_type, daemon=True).start()

    def _transcribe_and_type(self):
        if not self.audio_chunks:
            print("No audio recorded.")
            self.hide_signal.emit()
            return

        audio = np.concatenate(self.audio_chunks)
        duration = len(audio) / SAMPLE_RATE
        print(f"Recorded {duration:.2f} seconds of audio.")

        # Save to temp file
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as f:
            tmp_path = f.name
            import scipy.io.wavfile

            scipy.io.wavfile.write(tmp_path, SAMPLE_RATE, audio)

        print(f"Saved to {tmp_path}")
        model = get_whisper_model()
        print("Transcribing...")
        result = model.transcribe(tmp_path, verbose=True)
        text = result["text"]
        text = text.strip()

        print(f"Transcription: {text!r}")

        if text:
            print("Typing text...")
            rp.type_string_with_keyboard(text)
            print("Done typing.")
        else:
            print("No text to type.")

        self.hide_signal.emit()

    def center_on_screen(self):
        screen = QApplication.primaryScreen().geometry()
        x = (screen.width() - self.width()) // 2
        y = screen.height() // 4
        self.move(x, y)


def main():
    app = QApplication([])
    window = VoiceThingWindow()

    # Global hotkey via pynput - double-tap option key
    import time
    last_option_time = [0.0]
    DOUBLE_TAP_THRESHOLD = 0.3  # seconds

    def is_option(key):
        return key in (keyboard.Key.alt, keyboard.Key.alt_l, keyboard.Key.alt_r)

    def on_release(key):
        if is_option(key):
            now = time.time()
            if now - last_option_time[0] < DOUBLE_TAP_THRESHOLD:
                window.toggle_signal.emit()
                last_option_time[0] = 0.0  # reset to avoid triple-tap
            else:
                last_option_time[0] = now

    listener = keyboard.Listener(on_release=on_release)
    listener.start()

    # Preload model at startup
    get_whisper_model()

    print("Voice Thing running. Double-tap Option to record.")
    app.exec()


if __name__ == "__main__":
    main()
