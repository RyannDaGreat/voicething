#!/usr/bin/env /opt/homebrew/opt/python@3.10/bin/python3.10
"""Voice transcription app: double-tap Option to record, transcribe, and type."""

import signal
import time

import whisper
import rp
from pynput import keyboard
from PyQt6.QtWidgets import QApplication

from ui import VoiceThingWindow

WHISPER_MODEL = None


def get_whisper_model():
    global WHISPER_MODEL
    if WHISPER_MODEL is None:
        print("Loading Whisper model (large-v3)...")
        WHISPER_MODEL = whisper.load_model("large-v3")
        print("Whisper model loaded.")
    return WHISPER_MODEL


def main():
    signal.signal(signal.SIGINT, signal.SIG_DFL)  # Allow Ctrl+C to kill app

    print("Starting app...")
    app = QApplication([])
    print("QApplication created")
    window = VoiceThingWindow(get_whisper_model)
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

    get_whisper_model()
    rp.play_chords([0, 4, 7], [12], gap=0, t=0.15)  # Ready chime
    print("Voice Thing running. Double-tap Option to record.")
    app.exec()


if __name__ == "__main__":
    main()
