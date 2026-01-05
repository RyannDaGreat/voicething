"""Base style - just a plain class with defaults. Override what you need."""

from PyQt6.QtGui import QColor


class BaseStyle:
    name = "base"
    font = "Futura"
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

    # Waveform - flat by default (transparent background, accent color)
    waveform_color = QColor(100, 200, 255)
    waveform_glow = False
    waveform_glow_radius = 18
    waveform_glow_alpha = 200
    waveform_center_line = QColor(255, 255, 255, 40)  # Center line color
    waveform_panel = None  # None=transparent, "aqua"=blue macOS panel, "dark"=dark gradient panel

    # Transcription panel background
    transcription_panel_bg = "rgba(20,20,30,200)"
    transcription_panel_border = "rgb(30,30,40)"

    # Transcription row hover/button styling (dark theme defaults)
    transcription_row_hover = "rgba(255,255,255,0.05)"
    transcription_row_btn_hover = "rgba(255,255,255,0.15)"
    transcription_row_btn_pressed = "rgba(100,200,255,0.4)"

    # Timer - flat by default
    timer_use_lcd = False  # If True, draw recessed LCD panel
    timer_color = QColor(100, 200, 255)
    timer_font_size = 28
    timer_panel_size = (160, 40)

    # Transcription colors
    transcription_text = "#b0b0b0"
    transcription_text_dimmed = "rgba(130,150,170,0.7)"

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
