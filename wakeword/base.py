"""Base class for wake word detection engines."""

from abc import ABC, abstractmethod
from typing import Callable, Optional
import numpy as np

# Callback signature: (pre_buffer: np.ndarray) -> None
# pre_buffer contains audio samples captured before the wake word
WakeWordCallback = Callable[[np.ndarray], None]

# Callback for stop signal (wake word said while recording)
StopCallback = Callable[[], None]

# Callback for cancel signal (cancel phrase said while recording)
CancelCallback = Callable[[], None]


class WakeWordEngine(ABC):
    """Abstract base class for wake word detection engines."""

    # Engine metadata (override in subclasses)
    name: str = "base"
    display_name: str = "Base Engine"

    def __init__(
        self,
        on_wake: WakeWordCallback,
        on_stop: Optional[StopCallback] = None,
        on_cancel: Optional[CancelCallback] = None,
    ):
        """
        Initialize engine with callbacks.

        Args:
            on_wake: Called when wake word detected (receives pre-buffer audio)
            on_stop: Called when wake word detected during recording (stop signal)
            on_cancel: Called when cancel phrase detected during recording
        """
        self.on_wake = on_wake
        self.on_stop = on_stop
        self.on_cancel = on_cancel
        self._running = False

    @abstractmethod
    def start(self) -> None:
        """Start listening for wake words."""
        pass

    @abstractmethod
    def stop(self) -> None:
        """Stop listening."""
        pass

    @abstractmethod
    def pause(self) -> None:
        """Temporarily pause listening (e.g., during recording)."""
        pass

    @abstractmethod
    def resume(self) -> None:
        """Resume listening after pause."""
        pass

    @property
    def is_running(self) -> bool:
        """Check if engine is currently listening."""
        return self._running

    @abstractmethod
    def reset(self) -> None:
        """Reset internal state (clear buffers, etc.)."""
        pass

    @classmethod
    @abstractmethod
    def get_available_models(cls) -> list:
        """Get list of available wake word models/phrases."""
        pass

    @classmethod
    def get_model_display_name(cls, model: str) -> str:
        """Get display name for a model (default: title case)."""
        return model.replace('_', ' ').title()
