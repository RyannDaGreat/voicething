"""
Wake word detection module with pluggable engine backends.

Engines:
- openwakeword: ML-based detection, select from pre-trained models
- macos: Native macOS NSSpeechRecognizer, custom phrases via text input
"""

from .base import WakeWordEngine, WakeWordCallback
from .openwakeword_engine import (
    OpenWakeWordEngine,
    BUILTIN_MODELS,
    COMMUNITY_MODELS,
    FEATURED_MODELS,
    ALTERNATES,
    get_models_ordered,
    get_model_display_name,
    get_all_normalized,
    download_model,
)
from .macos_engine import MacOSWakeWordEngine

# Engine registry
ENGINES = {
    'openwakeword': OpenWakeWordEngine,
    'macos': MacOSWakeWordEngine,
}


def get_engine(name: str) -> type:
    """Get engine class by name."""
    if name not in ENGINES:
        raise ValueError(f"Unknown wake word engine: {name}. Options: {list(ENGINES.keys())}")
    return ENGINES[name]


def create_engine(name: str, callback: WakeWordCallback, **config) -> WakeWordEngine:
    """Create and configure an engine instance."""
    engine_class = get_engine(name)
    return engine_class(callback, **config)


__all__ = [
    'WakeWordEngine',
    'WakeWordCallback',
    'OpenWakeWordEngine',
    'MacOSWakeWordEngine',
    'ENGINES',
    'get_engine',
    'create_engine',
    # OpenWakeWord data exports
    'BUILTIN_MODELS',
    'COMMUNITY_MODELS',
    'FEATURED_MODELS',
    'ALTERNATES',
    'get_models_ordered',
    'get_model_display_name',
    'get_all_normalized',
    'download_model',
]
