"""Dark minimal style - the original VoiceThing look before skeuomorphism."""

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor, QPen

from .base import BaseStyle, CYAN, RED_ERROR


# Dark theme named colors
DARK_BG = QColor(30, 30, 40)
DARK_GRAY = "rgb(100,100,100)"
DARKER_GRAY = "rgb(80,80,80)"
MENU_BG = "rgb(40,40,50)"
MENU_HOVER = "rgb(60,60,70)"

# White with alpha
WHITE_90 = "rgba(255,255,255,0.9)"
WHITE_70 = "rgba(255,255,255,0.7)"
WHITE_60 = "rgba(255,255,255,0.6)"
WHITE_40 = "rgba(255,255,255,0.4)"
WHITE_20 = "rgba(255,255,255,0.2)"
WHITE_10 = "rgba(255,255,255,0.1)"
WHITE_5 = "rgba(255,255,255,0.05)"
BLACK_30 = "rgba(0,0,0,0.3)"

# Cyan with alpha
CYAN_90 = "rgba(100,200,255,0.9)"
CYAN_40 = "rgba(100,200,255,0.4)"
CYAN_30 = "rgba(100,200,255,0.3)"


class DarkMinimalStyle(BaseStyle):
    name = "dark_minimal"
    font = "Futura"

    # Dark theme colors
    accent = CYAN
    text_primary = WHITE_90
    text_secondary = WHITE_70
    text_muted = WHITE_40
    text_error = RED_ERROR
    text_link = CYAN_90
    border_color = DARK_GRAY
    border_dark = DARKER_GRAY
    icon_color_dark = '#ffffff'  # White icons on dark bg
    icon_color_light = '#ffffff'
    icon_color_muted = '#999999'  # Solid gray for SVG compatibility

    # Dark solid background color
    bg_color = DARK_BG
    bg_alpha_focused = 255
    bg_alpha_unfocused = 220

    def button_css(self):
        return (
            f"QPushButton {{ color: {WHITE_60}; background: {WHITE_10}; "
            f"border: 1px solid {self.border_color}; border-radius: 3px; "
            "padding: 3px 8px; font-size: 11px; text-align: left; }"
            f"QPushButton:hover {{ background: {WHITE_20}; }}"
            f"QPushButton:pressed {{ background: {CYAN_40}; }}"
            f"QPushButton:disabled {{ color: {WHITE_20}; background: transparent; }}"
            f"QPushButton:checked {{ background: {CYAN_30}; }}"
            f"QPushButton:checked:hover {{ background: {CYAN_40}; }}"
        )

    def menu_css(self):
        return (
            f"QMenu {{ background: {MENU_BG}; color: white; "
            f"border: 1px solid {self.border_dark}; border-radius: 6px; padding: 4px; }}"
            "QMenu::item { padding: 4px 16px; border-radius: 4px; }"
            f"QMenu::item:selected {{ background: {MENU_HOVER}; }}"
            f"QMenu::separator {{ height: 1px; background: {WHITE_20}; margin: 4px 8px; }}"
        )

    def scrollbar_css(self):
        return (
            f"QScrollBar:vertical {{ width: 10px; background: {WHITE_5}; margin: 2px; border-radius: 5px; }}"
            f"QScrollBar::handle:vertical {{ background: {WHITE_20}; border-radius: 4px; min-height: 20px; }}"
            f"QScrollBar::handle:vertical:hover {{ background: {CYAN_40}; }}"
            "QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical { height: 0; }"
            "QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical { background: transparent; }"
        )

    def panel_bg_css(self):
        return (
            f"background: {WHITE_5}; "
            f"border: 1px solid {self.border_color}; border-radius: 6px;"
        )

    def panel_bg_flat_css(self):
        return (
            f"background: {BLACK_30}; "
            f"border: 1px solid {self.border_color}; border-radius: 6px;"
        )

    def paint_window(self, painter, rect, width, height, focused=True):
        """Paint solid dark background with optional focus glow."""
        radius = self.corner_radius
        alpha = self.bg_alpha_focused if focused else self.bg_alpha_unfocused
        painter.setBrush(QColor(self.bg_color.red(), self.bg_color.green(), self.bg_color.blue(), alpha))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawRoundedRect(rect, radius, radius)
        if focused:
            painter.setBrush(Qt.BrushStyle.NoBrush)
            painter.setPen(QPen(self.accent, 2))
            painter.drawRoundedRect(rect, radius, radius)
