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

from .base import WakeWordEngine, WakeWordCallback, StopCallback, CancelCallback

# Create the delegate class once at module level to avoid ObjC class redefinition errors
_SpeechDelegateClass = None
_delegate_engine = None  # Reference to current engine for callback


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

                # Check phrase types
                phrase_lower = phrase.lower()
                is_tmux_phrase = phrase_lower in _delegate_engine._tmux_phrases_lower
                is_cancel_phrase = phrase_lower in _delegate_engine._cancel_phrases_lower

                if _delegate_engine._is_recording:
                    # Cancel phrases cancel the recording
                    if is_cancel_phrase:
                        print(f"[wakeword] Cancel phrase detected: '{phrase}'")
                        if _delegate_engine.on_cancel:
                            _delegate_engine.on_cancel()
                        return
                    # Tmux phrases can't stop recording, only regular phrases can
                    if is_tmux_phrase:
                        print(f"[wakeword] Ignoring tmux phrase during recording")
                        return
                    if _delegate_engine.on_stop:
                        _delegate_engine.on_stop()
                else:
                    # Cancel phrases do nothing when not recording
                    if is_cancel_phrase:
                        print(f"[wakeword] Ignoring cancel phrase (not recording)")
                        return
                    # Store the detected phrase (for tmux routing prefix)
                    _delegate_engine.last_detected_phrase = phrase if is_tmux_phrase else None
                    # macOS doesn't have a pre-buffer, pass empty array
                    _delegate_engine.on_wake(np.array([], dtype=np.float32))

        _SpeechDelegateClass = SpeechDelegate
    return _SpeechDelegateClass


class MacOSWakeWordEngine(WakeWordEngine):
    """Native macOS speech recognition for wake word detection.

    Supports two types of phrases:
    - Regular phrases: Can start AND stop recording
    - Tmux phrases: Can ONLY start recording (not stop), and prepend to transcription
    """

    name = "macos"
    display_name = "macOS Native"

    # Default phrases if none specified
    DEFAULT_PHRASES = ["hey computer", "computer", "start recording"]

    def __init__(
        self,
        on_wake: WakeWordCallback,
        on_stop: Optional[StopCallback] = None,
        on_cancel: Optional[CancelCallback] = None,
        phrases: Optional[List[str]] = None,
        tmux_phrases: Optional[List[str]] = None,
        cancel_phrases: Optional[List[str]] = None,
    ):
        """
        Initialize macOS wake word engine.

        Args:
            on_wake: Callback when wake word detected
            on_stop: Callback when wake word detected during recording
            on_cancel: Callback when cancel phrase detected during recording
            phrases: List of phrases to listen for (comma-separated string also accepted)
            tmux_phrases: Tmux pane phrases (start only, not stop)
            cancel_phrases: Phrases that cancel recording (comma-separated string also accepted)
        """
        super().__init__(on_wake, on_stop, on_cancel)

        # Parse phrases (accept string or list)
        if phrases is None:
            self._phrases = self.DEFAULT_PHRASES.copy()
        elif isinstance(phrases, str):
            self._phrases = [p.strip() for p in phrases.split(',') if p.strip()]
            if not self._phrases:
                self._phrases = self.DEFAULT_PHRASES.copy()
        else:
            self._phrases = list(phrases) if phrases else self.DEFAULT_PHRASES.copy()

        # Parse tmux phrases (start only, not stop)
        if tmux_phrases is None:
            self._tmux_phrases = []
        elif isinstance(tmux_phrases, str):
            self._tmux_phrases = [p.strip() for p in tmux_phrases.split(',') if p.strip()]
        else:
            self._tmux_phrases = list(tmux_phrases) if tmux_phrases else []

        # Parse cancel phrases
        if cancel_phrases is None:
            self._cancel_phrases = []
        elif isinstance(cancel_phrases, str):
            self._cancel_phrases = [p.strip() for p in cancel_phrases.split(',') if p.strip()]
        else:
            self._cancel_phrases = list(cancel_phrases) if cancel_phrases else []

        # Lowercase sets for quick lookup
        self._tmux_phrases_lower = {p.lower() for p in self._tmux_phrases}
        self._cancel_phrases_lower = {p.lower() for p in self._cancel_phrases}

        self._recognizer = None
        self._delegate = None
        self._thread = None
        self._is_recording = False
        self._should_stop = threading.Event()
        self.last_detected_phrase = None  # Stores tmux phrase that triggered wake (for prefix)

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
            AppHelper.runConsoleEventLoop(stopAfterFirstRun=False, installInterrupt=False)
        except Exception as e:
            if not self._should_stop.is_set():
                print(f"[wakeword] macOS event loop error: {e}")

    def start(self) -> None:
        """Start listening for wake phrases."""
        if self._running:
            return

        # Always start fresh - not in recording state
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
            # Combine regular phrases + tmux phrases + cancel phrases
            all_phrases = self._phrases + self._tmux_phrases + self._cancel_phrases
            self._recognizer.setCommands_(all_phrases)
            self._recognizer.setBlocksOtherRecognizers_(True)
            self._recognizer.setListensInForegroundOnly_(False)  # Listen even when app not focused
            self._recognizer.startListening()

            # Run event loop in background thread
            self._should_stop.clear()
            self._thread = threading.Thread(target=self._run_event_loop, daemon=True)
            self._thread.start()

            self._running = True
            print(f"[wakeword] macOS listening for: {self._phrases}")

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

        # Clear global reference to prevent stale callbacks from firing
        # after stop() but before a new engine is created
        if _delegate_engine is self:
            _delegate_engine = None

        self._should_stop.set()
        # Don't join thread - it may be blocked in event loop

        self._running = False
        self._is_recording = False  # Reset in case we're stopped mid-recording
        print("[wakeword] macOS stopped")

    def pause(self) -> None:
        """Pause during recording."""
        self._is_recording = True
        print(f"[wakeword] macOS paused (_is_recording=True)")
        # macOS recognizer keeps running but we track state

    def resume(self) -> None:
        """Resume after recording."""
        self._is_recording = False
        print(f"[wakeword] macOS resumed (_is_recording=False)")

    def reset(self) -> None:
        """Reset state (no-op for macOS)."""
        pass

    def set_phrases(self, phrases: List[str]) -> None:
        """Update the phrases to listen for."""
        if isinstance(phrases, str):
            self._phrases = [p.strip() for p in phrases.split(',') if p.strip()]
        else:
            self._phrases = list(phrases) if phrases else self.DEFAULT_PHRASES.copy()

        # Update recognizer if running
        if self._recognizer is not None:
            self._recognizer.setCommands_(self._phrases)
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
