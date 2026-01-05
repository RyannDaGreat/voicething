"""Style modules for VoiceThing UI themes."""

from .macos_2005 import MacOS2005Style

STYLES = {
    "macos_2005": MacOS2005Style,
    # "windows_95": Windows95Style,  # TODO
}

def get_style(name="macos_2005"):
    return STYLES[name]()
