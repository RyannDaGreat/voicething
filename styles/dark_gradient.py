"""Dark gradient style - glass pills with drop shadows."""

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor, QLinearGradient, QBrush, QPen

from .base import BaseStyle


class DarkGradientStyle(BaseStyle):
    name = "dark_gradient"
    font = "Futura"

    # Dark theme colors
    accent = QColor(100, 200, 255)
    text_primary = "rgba(255,255,255,0.9)"
    text_secondary = "rgba(255,255,255,0.7)"
    text_muted = "rgba(255,255,255,0.4)"
    text_error = "rgb(255,80,80)"
    text_link = "rgba(100,200,255,0.9)"
    border_color = "rgba(90,90,105,0.8)"
    border_dark = "rgba(60,60,70,0.6)"
    icon_color_dark = '#ffffff'
    icon_color_light = '#ffffff'
    icon_color_muted = 'rgba(255,255,255,0.6)'

    # Waveform - cyan with glow and dark panel with grid
    waveform_color = QColor(100, 200, 255)
    waveform_glow = True
    waveform_center_line = QColor(100, 200, 255, 30)
    waveform_panel = "dark"  # Dark gradient panel with cyan grid

    # Timer - LCD panel style (dark gradient has the LCD look)
    timer_use_lcd = True
    timer_color = QColor(100, 200, 255)

    # Transcription colors (dark theme)
    transcription_text = "#b0b0b0"
    transcription_text_dimmed = "rgba(130,150,170,0.7)"
    transcription_panel_bg = (
        "qlineargradient(x1:0, y1:0, x2:0, y2:1, "
        "stop:0 rgba(35,38,48,0.95), stop:1 rgba(25,27,35,0.95))"
    )
    transcription_panel_border = "rgba(60,65,80,0.6)"
    transcription_row_hover = "rgba(100,180,230,0.08)"
    transcription_row_btn_hover = (
        "qlineargradient(x1:0, y1:0, x2:0, y2:1, "
        "stop:0 rgba(85,85,105,0.8), stop:1 rgba(55,55,70,0.8))"
    )
    transcription_row_btn_pressed = (
        "qlineargradient(x1:0, y1:0, x2:0, y2:1, "
        "stop:0 rgba(60,140,180,0.6), stop:1 rgba(40,100,140,0.6))"
    )

    def button_css(self):
        # Glass pill button with gradient and subtle glow
        return (
            f"QPushButton {{ "
            f"color: rgba(255,255,255,0.7); "
            f"background: qlineargradient(x1:0, y1:0, x2:0, y2:1, "
            f"stop:0 rgba(70,70,85,0.9), stop:0.1 rgba(55,55,70,0.9), "
            f"stop:0.9 rgba(35,35,48,0.9), stop:1 rgba(30,30,42,0.9)); "
            f"border: 1px solid rgba(90,90,105,0.8); "
            f"border-top: 1px solid rgba(120,120,140,0.5); "
            f"border-radius: 4px; padding: 2px 4px; font-size: 10px; font-family: {self.font}; text-align: left; }}"
            "QPushButton:hover { "
            "background: qlineargradient(x1:0, y1:0, x2:0, y2:1, "
            "stop:0 rgba(85,85,105,0.95), stop:0.1 rgba(70,70,88,0.95), "
            "stop:0.9 rgba(50,50,65,0.95), stop:1 rgba(42,42,55,0.95)); "
            "border: 1px solid rgba(100,180,230,0.4); }"
            "QPushButton:pressed { "
            "background: qlineargradient(x1:0, y1:0, x2:0, y2:1, "
            "stop:0 rgba(30,30,42,0.95), stop:0.1 rgba(35,35,48,0.95), "
            "stop:0.9 rgba(50,50,65,0.95), stop:1 rgba(60,60,75,0.95)); "
            "border: 1px solid rgba(100,200,255,0.6); "
            "border-top: 1px solid rgba(60,60,75,0.8); }"
            "QPushButton:disabled { color: rgba(255,255,255,0.2); background: rgba(40,40,50,0.3); border: 1px solid rgba(60,60,70,0.3); }"
            "QPushButton:checked { "
            "background: qlineargradient(x1:0, y1:0, x2:0, y2:1, "
            "stop:0 rgba(60,140,180,0.5), stop:0.1 rgba(50,120,160,0.5), "
            "stop:0.9 rgba(40,100,140,0.5), stop:1 rgba(35,90,130,0.5)); "
            "border: 1px solid rgba(100,200,255,0.6); }"
            "QPushButton:checked:hover { "
            "background: qlineargradient(x1:0, y1:0, x2:0, y2:1, "
            "stop:0 rgba(70,150,190,0.6), stop:0.1 rgba(60,130,170,0.6), "
            "stop:0.9 rgba(50,110,150,0.6), stop:1 rgba(45,100,140,0.6)); }"
        )

    def menu_css(self):
        # Frosted glass menu with gradient
        return (
            f"QMenu {{ "
            f"background: qlineargradient(x1:0, y1:0, x2:0, y2:1, "
            f"stop:0 rgba(55,55,68,0.95), stop:1 rgba(35,35,45,0.95)); "
            f"color: white; border: 1px solid rgba(100,100,115,0.6); "
            f"border-radius: 8px; padding: 6px; font-family: {self.font}; }}"
            "QMenu::item { padding: 6px 14px; border-radius: 5px; }"
            "QMenu::item:selected { "
            "background: qlineargradient(x1:0, y1:0, x2:0, y2:1, "
            "stop:0 rgba(100,180,230,0.3), stop:1 rgba(80,150,200,0.3)); }"
            "QMenu::separator { height: 1px; background: rgba(255,255,255,0.2); margin: 4px 8px; }"
        )

    def scrollbar_css(self):
        return (
            "QScrollBar:vertical { width: 8px; background: transparent; margin: 2px; }"
            "QScrollBar::handle:vertical { "
            "background: qlineargradient(x1:0, y1:0, x2:1, y2:0, "
            "stop:0 rgba(80,90,110,0.6), stop:0.5 rgba(100,110,130,0.7), stop:1 rgba(80,90,110,0.6)); "
            "border-radius: 4px; min-height: 20px; }"
            "QScrollBar::handle:vertical:hover { "
            "background: qlineargradient(x1:0, y1:0, x2:1, y2:0, "
            "stop:0 rgba(100,180,230,0.5), stop:0.5 rgba(100,200,255,0.6), stop:1 rgba(100,180,230,0.5)); }"
            "QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical { height: 0; }"
            "QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical { background: transparent; }"
        )

    def panel_bg_css(self):
        return (
            "background: qlineargradient(x1:0, y1:0, x2:0, y2:1, "
            "stop:0 rgba(45,48,58,0.95), stop:1 rgba(30,32,40,0.95)); "
            "border: 1px solid rgba(70,75,90,0.7); "
            "border-top: 1px solid rgba(90,95,110,0.5); "
            "border-radius: 8px;"
        )

    def panel_bg_flat_css(self):
        return (
            "background: qlineargradient(x1:0, y1:0, x2:0, y2:1, "
            "stop:0 rgba(35,38,48,0.95), stop:1 rgba(25,27,35,0.95)); "
            "border: 1px solid rgba(60,65,80,0.6); "
            "border-top: 1px solid rgba(40,45,55,0.9); "
            "border-radius: 8px;"
        )

    def paint_window(self, painter, rect, width, height, focused=True):
        """Paint gradient background with drop shadow and highlight."""
        radius = self.corner_radius
        alpha_mult = 1.0 if focused else 0.88

        # Main gradient background (top lighter, bottom darker)
        grad = QLinearGradient(0, rect.top(), 0, rect.bottom())
        grad.setColorAt(0, QColor(52, 52, 66, int(255 * alpha_mult)))
        grad.setColorAt(0.15, QColor(42, 42, 54, int(255 * alpha_mult)))
        grad.setColorAt(0.85, QColor(28, 28, 38, int(255 * alpha_mult)))
        grad.setColorAt(1, QColor(22, 22, 30, int(255 * alpha_mult)))
        painter.setBrush(QBrush(grad))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawRoundedRect(rect, radius, radius)

        # Inner highlight at top (subtle bevel effect)
        inner_rect = rect.adjusted(1, 1, -1, -1)
        highlight_grad = QLinearGradient(0, rect.top(), 0, rect.top() + 20)
        highlight_grad.setColorAt(0, QColor(255, 255, 255, int(18 * alpha_mult)))
        highlight_grad.setColorAt(1, QColor(255, 255, 255, 0))
        painter.setBrush(QBrush(highlight_grad))
        painter.drawRoundedRect(inner_rect, radius - 1, radius - 1)

        # Inner shadow at top edge (inset effect)
        shadow_grad = QLinearGradient(0, rect.top(), 0, rect.top() + 8)
        shadow_grad.setColorAt(0, QColor(0, 0, 0, int(40 * alpha_mult)))
        shadow_grad.setColorAt(1, QColor(0, 0, 0, 0))
        painter.setBrush(QBrush(shadow_grad))
        painter.drawRoundedRect(rect.adjusted(0, 0, 0, -rect.height() + 12), radius, radius)

        # Subtle border
        painter.setBrush(Qt.BrushStyle.NoBrush)
        painter.setPen(QPen(QColor(80, 80, 95, int(180 * alpha_mult)), 1))
        painter.drawRoundedRect(rect, radius, radius)

        # Focus glow effect
        if focused:
            # Outer glow
            for i in range(3):
                glow_alpha = int(40 - i * 12)
                painter.setPen(QPen(QColor(100, 200, 255, glow_alpha), 3 + i * 2))
                painter.drawRoundedRect(rect.adjusted(-i, -i, i, i), radius + i, radius + i)
            # Inner accent border
            painter.setPen(QPen(self.accent, 2))
            painter.drawRoundedRect(rect, radius, radius)
