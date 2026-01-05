"""Style modules for VoiceThing UI themes."""

from .macos_2005 import MacOS2005Style
from .dark_minimal import DarkMinimalStyle
from .dark_gradient import DarkGradientStyle

STYLES = {
    "macos_2005": MacOS2005Style,
    "dark_minimal": DarkMinimalStyle,
    "dark_gradient": DarkGradientStyle,
}

def get_style(name="macos_2005"):
    return STYLES[name]()
