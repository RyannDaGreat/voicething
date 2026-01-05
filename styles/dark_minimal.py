"""Dark minimal style - the original VoiceThing look before skeuomorphism."""

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor, QPixmap

from .base import BaseStyle


class DarkMinimalStyle(BaseStyle):
    name = "dark_minimal"
    font = "Futura"

    # Dark theme colors
    accent = QColor(100, 200, 255)
    text_primary = "rgba(255,255,255,0.9)"
    text_secondary = "rgba(255,255,255,0.7)"
    text_muted = "rgba(255,255,255,0.4)"
    text_error = "rgb(255,80,80)"
    text_link = "rgba(100,200,255,0.9)"
    border_color = "rgb(100,100,100)"
    border_dark = "rgb(80,80,80)"
    icon_color_dark = '#ffffff'  # White icons on dark bg
    icon_color_light = '#ffffff'
    icon_color_muted = 'rgba(255,255,255,0.6)'

    # Dark solid background color
    bg_color = QColor(30, 30, 40)
    bg_alpha_focused = 255
    bg_alpha_unfocused = 220

    def button_css(self):
        return (
            "QPushButton { color: rgba(255,255,255,0.6); background: rgba(255,255,255,0.1); "
            f"border: 1px solid {self.border_color}; border-radius: 3px; "
            "padding: 3px 8px; font-size: 11px; text-align: left; }"
            "QPushButton:hover { background: rgba(255,255,255,0.2); }"
            "QPushButton:pressed { background: rgba(100,200,255,0.4); }"
            "QPushButton:disabled { color: rgba(255,255,255,0.2); background: transparent; }"
            "QPushButton:checked { background: rgba(100,200,255,0.3); }"
            "QPushButton:checked:hover { background: rgba(100,200,255,0.4); }"
        )

    def menu_css(self):
        return (
            "QMenu { background: rgb(40,40,50); color: white; "
            f"border: 1px solid {self.border_dark}; border-radius: 6px; padding: 4px; }}"
            "QMenu::item { padding: 4px 16px; border-radius: 4px; }"
            "QMenu::item:selected { background: rgb(60,60,70); }"
            "QMenu::separator { height: 1px; background: rgba(255,255,255,0.2); margin: 4px 8px; }"
        )

    def scrollbar_css(self):
        return (
            "QScrollBar:vertical { width: 10px; background: rgba(255,255,255,0.05); margin: 2px; border-radius: 5px; }"
            "QScrollBar::handle:vertical { background: rgba(255,255,255,0.2); border-radius: 4px; min-height: 20px; }"
            "QScrollBar::handle:vertical:hover { background: rgba(100,200,255,0.4); }"
            "QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical { height: 0; }"
            "QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical { background: transparent; }"
        )

    def panel_bg_css(self):
        return (
            "background: rgba(255,255,255,0.05); "
            f"border: 1px solid {self.border_color}; border-radius: 6px;"
        )

    def panel_bg_flat_css(self):
        return (
            "background: rgba(0,0,0,0.3); "
            f"border: 1px solid {self.border_color}; border-radius: 6px;"
        )

    def paint_window(self, painter, rect, width, height, focused=True):
        """Paint solid dark background with optional focus glow."""
        from PyQt6.QtGui import QPen
        radius = self.corner_radius
        alpha = self.bg_alpha_focused if focused else self.bg_alpha_unfocused
        painter.setBrush(QColor(self.bg_color.red(), self.bg_color.green(), self.bg_color.blue(), alpha))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawRoundedRect(rect, radius, radius)
        if focused:
            painter.setBrush(Qt.BrushStyle.NoBrush)
            painter.setPen(QPen(self.accent, 2))
            painter.drawRoundedRect(rect, radius, radius)
