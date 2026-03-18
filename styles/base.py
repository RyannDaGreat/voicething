"""Base style - just a plain class with defaults. Override what you need."""

import os
import re
from pathlib import Path


def _mirror_scrollbar_css(vertical_css):
    """
    Pure function. Convert vertical scrollbar CSS to horizontal equivalent.

    Swaps orientation keywords and dimensional properties so that a single
    vertical scrollbar definition produces matching horizontal rules.

    Args:
        vertical_css (str): CSS containing QScrollBar:vertical rules

    Returns:
        str: CSS with equivalent QScrollBar:horizontal rules

    Examples:
        >>> 'horizontal' in _mirror_scrollbar_css('QScrollBar:vertical { width: 14px; }')
        True
        >>> 'height: 14px' in _mirror_scrollbar_css('QScrollBar:vertical { width: 14px; }')
        True
    """
    h = vertical_css
    h = h.replace(':vertical', ':horizontal')
    h = h.replace('vertical', 'horizontal')
    # Swap width↔height for the scrollbar track dimensions
    h = re.sub(r'(?<![-])\bwidth:', '_W_PLACEHOLDER_:', h)
    h = re.sub(r'(?<![-])\bheight:', 'width:', h)
    h = h.replace('_W_PLACEHOLDER_:', 'height:')
    # Swap min-width↔min-height for handle minimum size
    h = h.replace('min-height:', '_MH_PLACEHOLDER_:')
    h = h.replace('min-width:', 'min-height:')
    h = h.replace('_MH_PLACEHOLDER_:', 'min-width:')
    # Rotate gradients 90°: x2:1,y2:0 → x2:0,y2:1
    h = re.sub(r'x2:\s*1\s*,\s*y2:\s*0', 'x2:0, y2:1', h)
    h = re.sub(r'x2:\s*0\s*,\s*y2:\s*1(?!\.)', 'x2:0, y2:1', h)
    return h

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor, QPixmap

# Texture cache directory - inside assets/textures/
_TEXTURE_CACHE_DIR = Path(__file__).parent.parent / "assets" / "textures"


def get_cached_texture(name, width, height, generator_func):
    """Load texture from PNG cache, or generate and cache it.

    Args:
        name: Unique texture name (e.g. "rust_512", "mahogany_512")
        width: Texture width
        height: Texture height
        generator_func: Callable that returns QPixmap when cache miss

    Returns:
        QPixmap of the texture
    """
    _TEXTURE_CACHE_DIR.mkdir(parents=True, exist_ok=True)
    cache_path = _TEXTURE_CACHE_DIR / f"{name}_{width}x{height}.png"

    if cache_path.exists():
        pixmap = QPixmap(str(cache_path))
        if not pixmap.isNull():
            return pixmap

    # Cache miss - generate texture
    pixmap = generator_func()
    pixmap.save(str(cache_path), "PNG")
    return pixmap


# Named colors for light themes (macOS 2005, etc.)
CHARCOAL = "rgb(40,40,45)"
SLATE = "rgb(60,60,65)"
GRAY = "rgb(120,120,130)"
SILVER = "rgb(160,160,170)"
PEWTER = "rgb(140,140,150)"
LIGHT_GRAY = "#b0b0b0"

ICON_DARK = '#505055'  # Dark icons for light backgrounds
ICON_LIGHT = '#ffffff'  # Light icons for dark backgrounds
ICON_MUTED_LIGHT = '#606068'  # Muted dark icons

# Accent colors
CYAN = QColor(100, 200, 255)
CYAN_CSS = "rgb(100,200,255)"
CYAN_MUTED = "rgba(130,150,170,0.7)"
BLUE_LINK = "rgb(40,100,180)"
RED_ERROR = "rgb(255,80,80)"

# Semi-transparent for dark themes
WHITE_5 = "rgba(255,255,255,0.05)"
WHITE_8 = "rgba(255,255,255,0.08)"
WHITE_15 = "rgba(255,255,255,0.15)"
WHITE_40 = "rgba(255,255,255,0.40)"
CYAN_40 = "rgba(100,200,255,0.4)"


class BaseStyle:
    name = "base"
    font = "Futura"
    corner_radius = 12
    scanlines = False  # If True, draw CRT-style horizontal scanlines on panels
    text_shadow = None  # If set, (QColor, x_offset, y_offset, blur) for title/section label shadows

    # Colors
    accent = CYAN
    accent_css = CYAN_CSS  # CSS string version for stylesheets
    text_primary = CHARCOAL
    text_secondary = SLATE
    text_muted = GRAY
    text_error = RED_ERROR
    text_link = BLUE_LINK
    border_color = SILVER
    border_dark = PEWTER
    icon_color_dark = ICON_DARK
    icon_color_light = ICON_LIGHT
    icon_color_muted = ICON_MUTED_LIGHT

    # Waveform - flat by default (transparent background, accent color)
    waveform_color = CYAN
    waveform_glow = False
    waveform_glow_radius = 18
    waveform_glow_alpha = 200
    waveform_center_line = QColor(255, 255, 255, 40)
    waveform_panel = None  # None=transparent, "aqua"=blue macOS panel, "dark"=dark gradient panel
    waveform_bubbles = False  # True for Frutiger Aero aquatic effects

    # Transcription panel background
    transcription_panel_bg = "rgba(20,20,30,200)"
    transcription_panel_border = "rgb(30,30,40)"

    # Transcription row hover/button styling (dark theme defaults)
    transcription_row_hover = WHITE_5
    transcription_row_btn_bg = WHITE_8
    transcription_row_btn_hover = WHITE_15
    transcription_row_btn_pressed = CYAN_40

    # Timer - flat by default
    timer_use_lcd = False  # If True, draw recessed LCD panel
    timer_color = CYAN
    timer_font_size = 28
    timer_panel_size = (160, 40)

    # Transcription colors
    transcription_text = LIGHT_GRAY
    transcription_text_dimmed = CYAN_MUTED

    # Slider colors (groove is the track, handle/sub-page use accent by default)
    slider_groove = "rgba(60,60,60,0.9)"  # Dark groove for light themes
    slider_handle = None  # None = use accent_css
    slider_fill = None  # None = use accent_css

    # Rotary knob style: "modern", "aqua", "industrial", "cyber", "vintage"
    knob_style = "modern"
    knob_body_dark = "#282828"  # Knob body gradient dark
    knob_body_light = "#505050"  # Knob body gradient light
    knob_notch_style = "line"  # "line", "dot", "needle", "arrow"
    knob_tickmarks = False  # Show tick marks around arc
    knob_glow = False  # Glow on value arc

    # Input field background (for QLineEdit, QComboBox dropdowns, etc.)
    input_bg = '#ffffff'
    input_text = '#000000'

    # Chime editor colors
    chime_grid_bg = QColor(30, 30, 35)
    chime_grid_line = QColor(50, 50, 55)
    chime_cell_inactive = QColor(45, 45, 50)
    chime_cell_active = None  # None = use accent
    chime_cell_highlight = None  # None = use accent with alpha
    chime_piano_white = QColor(240, 240, 240)
    chime_piano_black = QColor(40, 40, 45)
    chime_piano_label_white = QColor(60, 60, 60)
    chime_piano_label_black = QColor(180, 180, 180)

    def title_style(self, size=18):
        return f"color: {self.text_primary}; font-size: {size}px; font-family: {self.font};"

    def body_style(self, size=10):
        return f"color: {self.text_secondary}; font-size: {size}px;"

    def section_style(self):
        return f"color: {self.text_link}; font-size: 12px; font-family: {self.font};"

    # Subclasses override these
    def button_css(self): return ""
    def menu_css(self): return ""

    def scrollbar_css(self):
        """Return scrollbar CSS for both orientations.

        Subclasses override _scrollbar_vertical_css() with vertical-only rules.
        This method mirrors them to horizontal automatically.
        """
        vertical = self._scrollbar_vertical_css()
        if not vertical:
            return ""
        horizontal = _mirror_scrollbar_css(vertical)
        return vertical + horizontal

    def _scrollbar_vertical_css(self):
        """Override in subclasses. Return vertical scrollbar CSS only."""
        return ""
    def panel_bg_css(self): return ""
    def panel_bg_flat_css(self): return ""

    def paint_window(self, painter, rect, width, height, focused=True):
        """Paint the entire window background. Subclasses implement this."""
        pass

    def paint_waveform_panel(self, painter, rect, w, h, cy):
        """Paint the waveform panel background. Subclasses implement this.

        Default: transparent (no painting). Override in style subclasses.
        """
        pass

    def draw_bubble(self, painter, x, y, radius, alpha_mult=1.0):
        """Draw a single decorative water bubble with radial gradient.

        Shared utility for styles that want aquatic bubble effects.
        """
        from PyQt6.QtCore import QPointF
        from PyQt6.QtGui import QRadialGradient, QBrush
        center = QPointF(x + radius * 0.3, y + radius * 0.3)
        bubble_grad = QRadialGradient(center, radius * 1.2)
        bubble_grad.setColorAt(0.0, QColor(255, 255, 255, int(200 * alpha_mult)))
        bubble_grad.setColorAt(0.3, QColor(200, 240, 255, int(180 * alpha_mult)))
        bubble_grad.setColorAt(0.6, QColor(100, 200, 255, int(120 * alpha_mult)))
        bubble_grad.setColorAt(1.0, QColor(50, 150, 200, int(60 * alpha_mult)))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(QBrush(bubble_grad))
        painter.drawEllipse(int(x), int(y), int(radius * 2), int(radius * 2))
