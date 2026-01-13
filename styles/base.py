"""Base style - just a plain class with defaults. Override what you need."""

import os
from pathlib import Path

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

    def title_style(self, size=18):
        return f"color: {self.text_primary}; font-size: {size}px; font-family: {self.font};"

    def body_style(self, size=10):
        return f"color: {self.text_secondary}; font-size: {size}px;"

    def section_style(self):
        return f"color: {self.text_link}; font-size: 12px; font-family: {self.font};"

    # Subclasses override these
    def button_css(self): return ""
    def menu_css(self): return ""
    def scrollbar_css(self): return ""
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
