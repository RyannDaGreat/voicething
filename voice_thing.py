#!/usr/bin/env /opt/homebrew/opt/python@3.10/bin/python3.10
"""Voice transcription app: double-tap Option to record, transcribe, and type."""

import signal
import time

import rp
from pynput import keyboard
from PyQt6.QtWidgets import QApplication

from ui import VoiceThingWindow

WHISPER_MODEL_NAME = "large-v3"


def preload_whisper_model():
    """Preload the whisper model (rp.r caches it via @memoized)."""
    print(f"Loading Whisper model ({WHISPER_MODEL_NAME}) with Metal GPU...")
    rp.r._get_pywhispercpp_model(WHISPER_MODEL_NAME)
    print("Whisper model loaded.")


def main():
    signal.signal(signal.SIGINT, signal.SIG_DFL)  # Allow Ctrl+C to kill app

    print("Starting app...")
    app = QApplication([])
    print("QApplication created")
    window = VoiceThingWindow(WHISPER_MODEL_NAME)
    print("Window created")

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

    preload_whisper_model()
    rp.play_chords([0, 4, 7], [12], gap=0, t=0.15)  # Ready chime
    print("Voice Thing running. Double-tap Option to record.")
    app.exec()


if __name__ == "__main__":
    main()
