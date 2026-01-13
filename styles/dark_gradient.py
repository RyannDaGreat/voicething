"""Dark gradient style - glass pills with drop shadows."""

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor, QLinearGradient, QBrush, QPen

from .base import BaseStyle, CYAN, RED_ERROR, LIGHT_GRAY, CYAN_MUTED


# White/black with alpha
WHITE_90 = "rgba(255,255,255,0.9)"
WHITE_70 = "rgba(255,255,255,0.7)"
WHITE_60 = "rgba(255,255,255,0.6)"
WHITE_40 = "rgba(255,255,255,0.4)"
WHITE_20 = "rgba(255,255,255,0.2)"
WHITE_8 = "rgba(255,255,255,0.08)"

# Cyan accent colors
CYAN_90 = "rgba(100,200,255,0.9)"
CYAN_60 = "rgba(100,200,255,0.6)"
CYAN_35 = "rgba(100,200,255,0.35)"
CYAN_20 = "rgba(100,180,230,0.2)"
CYAN_8 = "rgba(100,180,230,0.08)"

# Glass effect borders
GLASS_BORDER = "rgba(90,90,105,0.8)"
GLASS_BORDER_DARK = "rgba(60,60,70,0.6)"
GLASS_BORDER_HOVER = "rgba(100,180,230,0.4)"
PANEL_BORDER = "rgba(70,75,90,0.7)"
PANEL_BORDER_DARK = "rgba(60,65,80,0.6)"

# Gradient definitions kept inline since they're complex multi-stop


class DarkGradientStyle(BaseStyle):
    name = "dark_gradient"
    font = "Futura"

    # Dark theme colors
    accent = CYAN
    text_primary = WHITE_90
    text_secondary = WHITE_70
    text_muted = WHITE_40
    text_error = RED_ERROR
    text_link = CYAN_90
    border_color = GLASS_BORDER
    border_dark = GLASS_BORDER_DARK
    icon_color_dark = '#ffffff'
    icon_color_light = '#ffffff'
    icon_color_muted = '#999999'  # Solid gray for SVG compatibility

    # Slider - semi-transparent cyan groove on dark gradient
    slider_groove = "rgba(100,200,255,0.25)"

    # Waveform - cyan with glow and dark panel with grid
    waveform_color = CYAN
    waveform_glow = True
    waveform_center_line = QColor(100, 200, 255, 30)
    waveform_panel = "dark"  # Dark gradient panel with cyan grid

    # Timer - LCD panel style (dark gradient has the LCD look)
    timer_use_lcd = True
    timer_color = CYAN

    # Transcription colors (dark theme)
    transcription_text = LIGHT_GRAY
    transcription_text_dimmed = CYAN_MUTED
    transcription_panel_bg = (
        "qlineargradient(x1:0, y1:0, x2:0, y2:1, "
        "stop:0 rgba(35,38,48,0.95), stop:1 rgba(25,27,35,0.95))"
    )
    transcription_panel_border = PANEL_BORDER_DARK
    transcription_row_hover = CYAN_8
    transcription_row_btn_bg = WHITE_8
    transcription_row_btn_hover = CYAN_20
    transcription_row_btn_pressed = CYAN_35

    def button_css(self):
        # Glass pill button with gradient - uniform border color
        return (
            f"QPushButton {{ "
            f"color: {WHITE_70}; "
            f"background: qlineargradient(x1:0, y1:0, x2:0, y2:1, "
            f"stop:0 rgba(70,70,85,0.9), stop:0.1 rgba(55,55,70,0.9), "
            f"stop:0.9 rgba(35,35,48,0.9), stop:1 rgba(30,30,42,0.9)); "
            f"border: 1px solid {GLASS_BORDER}; "
            f"border-radius: 4px; padding: 2px 4px; font-size: 10px; font-family: {self.font}; text-align: left; }}"
            f"QPushButton:hover {{ "
            f"background: qlineargradient(x1:0, y1:0, x2:0, y2:1, "
            f"stop:0 rgba(85,85,105,0.95), stop:0.1 rgba(70,70,88,0.95), "
            f"stop:0.9 rgba(50,50,65,0.95), stop:1 rgba(42,42,55,0.95)); "
            f"border: 1px solid {GLASS_BORDER_HOVER}; }}"
            f"QPushButton:pressed {{ "
            f"background: qlineargradient(x1:0, y1:0, x2:0, y2:1, "
            f"stop:0 rgba(30,30,42,0.95), stop:0.1 rgba(35,35,48,0.95), "
            f"stop:0.9 rgba(50,50,65,0.95), stop:1 rgba(60,60,75,0.95)); "
            f"border: 1px solid {CYAN_60}; }}"
            f"QPushButton:disabled {{ color: {WHITE_20}; background: rgba(40,40,50,0.3); border: 1px solid rgba(60,60,70,0.3); }}"
            f"QPushButton:checked {{ "
            f"background: qlineargradient(x1:0, y1:0, x2:0, y2:1, "
            f"stop:0 rgba(60,140,180,0.5), stop:0.1 rgba(50,120,160,0.5), "
            f"stop:0.9 rgba(40,100,140,0.5), stop:1 rgba(35,90,130,0.5)); "
            f"border: 1px solid {CYAN_60}; }}"
            f"QPushButton:checked:hover {{ "
            f"background: qlineargradient(x1:0, y1:0, x2:0, y2:1, "
            f"stop:0 rgba(70,150,190,0.6), stop:0.1 rgba(60,130,170,0.6), "
            f"stop:0.9 rgba(50,110,150,0.6), stop:1 rgba(45,100,140,0.6)); }}"
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
            f"QMenu::separator {{ height: 1px; background: {WHITE_20}; margin: 4px 8px; }}"
        )

    def scrollbar_css(self):
        return (
            "QScrollBar:vertical { width: 10px; background: transparent; margin: 2px; border: none; }"
            "QScrollBar::handle:vertical { "
            "background: qlineargradient(x1:0, y1:0, x2:1, y2:0, "
            "stop:0 rgba(80,90,110,0.6), stop:0.5 rgba(100,110,130,0.7), stop:1 rgba(80,90,110,0.6)); "
            "border-radius: 5px; min-height: 30px; margin: 0px; }"
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
            f"border: 1px solid {PANEL_BORDER}; "
            "border-radius: 8px;"
        )

    def panel_bg_flat_css(self):
        return (
            "background: qlineargradient(x1:0, y1:0, x2:0, y2:1, "
            "stop:0 rgba(35,38,48,0.95), stop:1 rgba(25,27,35,0.95)); "
            f"border: 1px solid {PANEL_BORDER_DARK}; "
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

    def paint_waveform_panel(self, painter, rect, w, h, cy):
        """Dark gradient panel with cyan grid."""
        # Dark gradient background
        panel_grad = QLinearGradient(0, 0, 0, h)
        panel_grad.setColorAt(0, QColor(35, 38, 48, 240))
        panel_grad.setColorAt(0.5, QColor(28, 30, 38, 240))
        panel_grad.setColorAt(1, QColor(22, 24, 32, 240))
        painter.setBrush(QBrush(panel_grad))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawRoundedRect(rect, 8, 8)

        # Subtle cyan grid
        painter.setPen(QPen(QColor(100, 200, 255, 15), 1))
        for i in range(1, 4):
            y = int(h * i / 4)
            painter.drawLine(0, y, w, y)
        num_sections = 8
        for i in range(1, num_sections):
            painter.drawLine(int(w * i / num_sections), 0, int(w * i / num_sections), h)

        # Subtle border
        painter.setBrush(Qt.BrushStyle.NoBrush)
        painter.setPen(QPen(QColor(50, 55, 65, 150), 1))
        painter.drawRoundedRect(rect, 8, 8)
