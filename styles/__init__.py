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
from .holographic import HolographicStyle
from .chalkboard import ChalkboardStyle
from .neon_sign import NeonSignStyle
from .weathered_copper import WeatheredCopperStyle
from .crt_terminal import CRTTerminalStyle
from .underwater import UnderwaterStyle
from .synthwave import SynthwaveStyle
from .manuscript import ManuscriptStyle
from .art_nouveau import ArtNouveauStyle
from .midnight_glass import MidnightGlassStyle
from .vista_aero import VistaAeroStyle
from .tropical_jungle import TropicalJungleStyle
from .autumn_harvest import AutumnHarvestStyle
from .honeycomb import HoneycombStyle
from .emerald_terminal import EmeraldTerminalStyle
from .desert_sunset import DesertSunsetStyle
from .minecraft import MinecraftStyle
from .filigree import FiligreeStyle
from .filigree_gothic import FiligreeGothicStyle
from .filigree_flourish import FiligreeFlourishStyle
from .filigree_web import FiligreeWebStyle
from .filigree_iron import FiligreeIronStyle
from .desert_filigree import DesertFiligreeStyle

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
    "holographic": HolographicStyle,
    "chalkboard": ChalkboardStyle,
    "neon_sign": NeonSignStyle,
    "weathered_copper": WeatheredCopperStyle,
    "crt_terminal": CRTTerminalStyle,
    "underwater": UnderwaterStyle,
    "synthwave": SynthwaveStyle,
    "manuscript": ManuscriptStyle,
    "art_nouveau": ArtNouveauStyle,
    "midnight_glass": MidnightGlassStyle,
    "vista_aero": VistaAeroStyle,
    "tropical_jungle": TropicalJungleStyle,
    "autumn_harvest": AutumnHarvestStyle,
    "honeycomb": HoneycombStyle,
    "emerald_terminal": EmeraldTerminalStyle,
    "desert_sunset": DesertSunsetStyle,
    "minecraft": MinecraftStyle,
    "filigree": FiligreeStyle,
    "filigree_gothic": FiligreeGothicStyle,
    "filigree_flourish": FiligreeFlourishStyle,
    "filigree_web": FiligreeWebStyle,
    "filigree_iron": FiligreeIronStyle,
    "desert_filigree": DesertFiligreeStyle,
}

def get_style(name="macos_2005"):
    return STYLES[name]()
