"""Base style - just a plain class with defaults. Override what you need."""

from PyQt6.QtGui import QColor


class BaseStyle:
    name = "base"
    font = "sans-serif"
    corner_radius = 12

    # Colors
    accent = QColor(100, 200, 255)
    text_primary = "rgb(40,40,45)"
    text_secondary = "rgb(60,60,65)"
    text_muted = "rgb(120,120,130)"
    text_error = "rgb(255,80,80)"
    text_link = "rgb(40,100,180)"
    border_color = "rgb(160,160,170)"
    border_dark = "rgb(140,140,150)"
    icon_color_dark = '#505055'
    icon_color_light = '#ffffff'
    icon_color_muted = '#606068'

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
    def get_background_pixmap(self, height=512): return None
    def draw_vignette(self, painter, rect, width, height, radius=12): pass
