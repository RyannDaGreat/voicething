"""Style modules for VoiceThing UI themes."""

from .macos_2005 import MacOS2005Style
from .dark_minimal import DarkMinimalStyle
from .dark_gradient import DarkGradientStyle
from .frutiger_aero import FrutigerAeroStyle
from .vaporwave import VaporwaveStyle
from .windows_95 import Windows95Style

STYLES = {
    "macos_2005": MacOS2005Style,
    "dark_minimal": DarkMinimalStyle,
    "dark_gradient": DarkGradientStyle,
    "frutiger_aero": FrutigerAeroStyle,
    "vaporwave": VaporwaveStyle,
    "windows_95": Windows95Style,
}

def get_style(name="macos_2005"):
    return STYLES[name]()
