"""Style modules for VoiceThing UI themes."""

from .macos_2005 import MacOS2005Style
from .dark_minimal import DarkMinimalStyle
from .dark_gradient import DarkGradientStyle
from .frutiger_aero import FrutigerAeroStyle
from .vaporwave import VaporwaveStyle
from .windows_95 import Windows95Style
from .cyberpunk_metal import CyberpunkMetalStyle
from .rust_grunge import RustGrungeStyle
from .supervillain import SupervillainStyle
from .barbie_jelly import BarbieJellyStyle
from .mahogany_wood import MahoganyWoodStyle

STYLES = {
    "macos_2005": MacOS2005Style,
    "dark_minimal": DarkMinimalStyle,
    "dark_gradient": DarkGradientStyle,
    "frutiger_aero": FrutigerAeroStyle,
    "vaporwave": VaporwaveStyle,
    "windows_95": Windows95Style,
    "cyberpunk_metal": CyberpunkMetalStyle,
    "rust_grunge": RustGrungeStyle,
    "supervillain": SupervillainStyle,
    "barbie_jelly": BarbieJellyStyle,
    "mahogany_wood": MahoganyWoodStyle,
}

def get_style(name="macos_2005"):
    return STYLES[name]()
