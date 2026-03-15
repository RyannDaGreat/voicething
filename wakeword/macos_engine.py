"""
macOS native wake word detection using NSSpeechRecognizer.

This engine uses Apple's built-in speech recognition which:
- Works completely offline
- Requires no training or model downloads
- Supports any custom phrases you specify
- Runs in the background with low CPU usage
"""

import threading
from typing import Optional, List

import numpy as np

from .base import WakeWordEngine, WakeWordCallback, StopCallback, CancelCallback, CommandCallback

# Create the delegate class once at module level to avoid ObjC class redefinition errors
_SpeechDelegateClass = None
_delegate_engine = None  # Reference to current engine for callback


def _parse_phrases(raw):
    """Parse a string or list into a list of stripped phrases."""
    if raw is None:
        return []
    if isinstance(raw, str):
        return [p.strip() for p in raw.split(',') if p.strip()]
    return list(raw) if raw else []


def _get_delegate_class():
    """Get or create the SpeechDelegate class (only once per process)."""
    global _SpeechDelegateClass
    if _SpeechDelegateClass is None:
        import objc
        from Foundation import NSObject

        class SpeechDelegate(NSObject):
            def speechRecognizer_didRecognizeCommand_(self, sender, command):
                global _delegate_engine
                if _delegate_engine is None:
                    print(f"[wakeword] macOS recognized but no engine (ignoring)")
                    return
                phrase = str(command)
                print(f"[wakeword] macOS recognized: '{phrase}' (recording={_delegate_engine._is_recording})")

                phrase_lower = phrase.lower()
                is_tmux_phrase = phrase_lower in _delegate_engine._tmux_phrases_lower
                is_cancel_phrase = phrase_lower in _delegate_engine._cancel_phrases_lower
                is_stop_phrase = phrase_lower in _delegate_engine._stop_phrases_lower
                is_start_phrase = phrase_lower in _delegate_engine._start_phrases_lower

                is_command_phrase = phrase_lower in _delegate_engine._command_phrases_lower

                if _delegate_engine._is_recording:
                    if is_cancel_phrase:
                        print(f"[wakeword] Cancel phrase detected: '{phrase}'")
                        _delegate_engine._is_recording = False  # Prevent double-trigger
                        if _delegate_engine.on_cancel:
                            _delegate_engine.on_cancel()
                        return
                    if is_stop_phrase:
                        print(f"[wakeword] Stop phrase detected: '{phrase}'")
                        _delegate_engine._is_recording = False  # Prevent double-trigger
                        if _delegate_engine.on_stop:
                            _delegate_engine.on_stop()
                        return
                    # Allow command phrases through during recording if mute is off
                    if is_command_phrase and not _delegate_engine._mute_commands_while_recording:
                        print(f"[wakeword] Command phrase during recording: '{phrase}'")
                        if _delegate_engine.on_command:
                            _delegate_engine.on_command(phrase)
                        return
                    # Start/tmux phrases are ignored during recording
                    print(f"[wakeword] Ignoring phrase during recording: '{phrase}'")
                else:
                    # Command phrases take priority when not recording
                    if is_command_phrase and not (is_start_phrase or is_tmux_phrase):
                        print(f"[wakeword] Command phrase detected: '{phrase}'")
                        if _delegate_engine.on_command:
                            _delegate_engine.on_command(phrase)
                        return
                    if (is_cancel_phrase or is_stop_phrase) and not (is_start_phrase or is_tmux_phrase):
                        print(f"[wakeword] Ignoring stop/cancel phrase (not recording)")
                        return
                    if is_start_phrase or is_tmux_phrase:
                        _delegate_engine.last_detected_phrase = phrase
                        _delegate_engine.on_wake(np.array([], dtype=np.float32))

        _SpeechDelegateClass = SpeechDelegate
    return _SpeechDelegateClass


class MacOSWakeWordEngine(WakeWordEngine):
    """Native macOS speech recognition for wake word detection.

    Supports four types of phrases:
    - Start phrases: Can only START recording
    - Stop phrases: Can only STOP recording
    - Tmux phrases: Can only START recording, and prepend to transcription
    - Cancel phrases: Cancel recording in progress
    """

    name = "macos"
    display_name = "macOS Native"

    DEFAULT_PHRASES = ["jarvis", "roger"]

    def __init__(
        self,
        on_wake: WakeWordCallback,
        on_stop: Optional[StopCallback] = None,
        on_cancel: Optional[CancelCallback] = None,
        on_command: Optional[CommandCallback] = None,
        phrases: Optional[List[str]] = None,
        stop_phrases: Optional[List[str]] = None,
        tmux_phrases: Optional[List[str]] = None,
        cancel_phrases: Optional[List[str]] = None,
        command_phrases: Optional[List[str]] = None,
        mute_commands_while_recording: bool = True,
    ):
        """
        Initialize macOS wake word engine.

        Args:
            on_wake: Callback when wake word detected
            on_stop: Callback when stop phrase detected during recording
            on_cancel: Callback when cancel phrase detected during recording
            on_command: Callback when command phrase detected (receives phrase string)
            phrases: Start phrases (comma-separated string or list)
            stop_phrases: Stop phrases that end recording (comma-separated string or list)
            tmux_phrases: Tmux pane phrases (start only, prepend to transcription)
            cancel_phrases: Phrases that cancel recording (comma-separated string or list)
            command_phrases: Command phrases that trigger bash commands (list of phrase strings)
        """
        super().__init__(on_wake, on_stop, on_cancel, on_command)

        # Parse start phrases
        self._phrases = _parse_phrases(phrases) or self.DEFAULT_PHRASES.copy()

        # Parse stop phrases (end recording)
        self._stop_phrases = _parse_phrases(stop_phrases)

        # Parse tmux phrases (start only)
        self._tmux_phrases = _parse_phrases(tmux_phrases)

        # Parse cancel phrases
        self._cancel_phrases = _parse_phrases(cancel_phrases)

        # Parse command phrases
        self._command_phrases = _parse_phrases(command_phrases)
        self._mute_commands_while_recording = mute_commands_while_recording

        # Lowercase sets for quick lookup
        self._start_phrases_lower = {p.lower() for p in self._phrases}
        self._stop_phrases_lower = {p.lower() for p in self._stop_phrases}
        self._tmux_phrases_lower = {p.lower() for p in self._tmux_phrases}
        self._cancel_phrases_lower = {p.lower() for p in self._cancel_phrases}
        self._command_phrases_lower = {p.lower() for p in self._command_phrases}

        self._recognizer = None
        self._delegate = None
        self._thread = None
        self._is_recording = False
        self._should_stop = threading.Event()
        self.last_detected_phrase = None

    def _all_phrases(self):
        """Return all phrases the recognizer should listen for."""
        return self._phrases + self._stop_phrases + self._tmux_phrases + self._cancel_phrases + self._command_phrases

    def _create_delegate(self):
        """Create the Objective-C delegate instance."""
        global _delegate_engine
        _delegate_engine = self
        DelegateClass = _get_delegate_class()
        return DelegateClass.alloc().init()

    def _run_event_loop(self):
        """Run the macOS event loop in a background thread."""
        try:
            from PyObjCTools import AppHelper
            AppHelper.runConsoleEventLoop(installInterrupt=False)
        except Exception as e:
            if not self._should_stop.is_set():
                print(f"[wakeword] macOS event loop error: {e}")

    def start(self) -> None:
        """Start listening for wake phrases."""
        if self._running:
            return

        self._is_recording = False

        try:
            from AppKit import NSSpeechRecognizer

            self._recognizer = NSSpeechRecognizer.alloc().init()
            if self._recognizer is None:
                raise RuntimeError(
                    "Failed to create NSSpeechRecognizer. "
                    "Enable 'Enhanced Dictation' in System Preferences > Keyboard > Dictation."
                )

            self._delegate = self._create_delegate()
            self._recognizer.setDelegate_(self._delegate)
            self._recognizer.setCommands_(self._all_phrases())
            self._recognizer.setBlocksOtherRecognizers_(True)
            self._recognizer.setListensInForegroundOnly_(False)
            self._recognizer.startListening()

            self._should_stop.clear()
            self._thread = threading.Thread(target=self._run_event_loop, daemon=True)
            self._thread.start()

            self._running = True
            print(f"[wakeword] macOS listening — start: {self._phrases}, stop: {self._stop_phrases}")

        except ImportError as e:
            raise RuntimeError(f"PyObjC not available: {e}")
        except Exception as e:
            raise RuntimeError(f"Failed to start macOS wake word: {e}")

    def stop(self) -> None:
        """Stop listening."""
        global _delegate_engine

        if self._recognizer is not None:
            self._recognizer.stopListening()
            self._recognizer = None
            self._delegate = None

        if _delegate_engine is self:
            _delegate_engine = None

        self._should_stop.set()
        self._running = False
        self._is_recording = False
        print("[wakeword] macOS stopped")

    def pause(self) -> None:
        """Pause during recording."""
        self._is_recording = True
        print(f"[wakeword] macOS paused (_is_recording=True)")

    def resume(self) -> None:
        """Resume after recording."""
        self._is_recording = False
        print(f"[wakeword] macOS resumed (_is_recording=False)")

    def reset(self) -> None:
        """Reset state (no-op for macOS)."""
        pass

    def set_phrases(self, phrases: List[str]) -> None:
        """Update the start phrases to listen for."""
        self._phrases = _parse_phrases(phrases) or self.DEFAULT_PHRASES.copy()
        self._start_phrases_lower = {p.lower() for p in self._phrases}

        if self._recognizer is not None:
            self._recognizer.setCommands_(self._all_phrases())
            print(f"[wakeword] macOS phrases updated: {self._phrases}")

    @classmethod
    def get_available_models(cls) -> list:
        """Return empty list - macOS uses custom phrases, not models."""
        return []

    @classmethod
    def get_model_display_name(cls, model: str) -> str:
        """Return the phrase as-is."""
        return model

    @classmethod
    def get_all_normalized(cls) -> set:
        """Return empty set - phrases are user-defined."""
        return set()
