"""Honeycomb style - warm golden amber on dark honey."""

import math

from PyQt6.QtCore import Qt, QPointF, QRectF
from PyQt6.QtGui import QColor, QLinearGradient, QBrush, QPen, QPainterPath, QPolygonF

from .base import BaseStyle, RED_ERROR, LIGHT_GRAY


# Golden accent with alpha variants
GOLD = QColor(255, 200, 50)
GOLD_CSS = "rgb(255,200,50)"
GOLD_MUTED = "rgba(200,170,100,0.7)"
GOLD_90 = "rgba(255,200,50,0.9)"
GOLD_60 = "rgba(255,200,50,0.6)"
GOLD_35 = "rgba(255,200,50,0.35)"
GOLD_20 = "rgba(200,170,80,0.2)"
GOLD_8 = "rgba(200,170,80,0.08)"

# White/black with alpha (warm-shifted)
CREAM_90 = "rgba(255,245,220,0.9)"
CREAM_70 = "rgba(255,240,200,0.7)"
CREAM_60 = "rgba(255,235,190,0.6)"
CREAM_40 = "rgba(255,230,180,0.4)"
CREAM_20 = "rgba(255,225,170,0.2)"
CREAM_8 = "rgba(255,220,160,0.08)"

# Glass effect borders - warm amber tones
HONEY_BORDER = "rgb(100,80,45)"
HONEY_BORDER_DARK = "rgb(75,60,35)"
HONEY_BORDER_HOVER = "rgb(220,175,50)"
PANEL_BORDER = "rgb(85,70,40)"
PANEL_BORDER_DARK = "rgb(70,58,32)"


class HoneycombStyle(BaseStyle):
    name = "honeycomb"
    font = "Futura"

    # Dark honey theme colors
    accent = GOLD
    accent_css = GOLD_CSS
    text_primary = CREAM_90
    text_secondary = CREAM_70
    text_muted = CREAM_40
    text_error = RED_ERROR
    text_link = GOLD_90
    border_color = HONEY_BORDER
    border_dark = HONEY_BORDER_DARK
    icon_color_dark = '#ffffff'
    icon_color_light = '#ffffff'
    icon_color_muted = '#a08860'

    # Dropdown input fields - dark warm brown
    input_bg = '#2a2218'
    input_text = '#f0e0c0'

    # Slider - semi-transparent gold groove on dark background
    slider_groove = "rgba(255,200,50,0.25)"

    # Rotary knob - glass style with golden track
    knob_style = "glass"
    knob_body_dark = "#1e1810"
    knob_body_light = "#4a3c28"
    knob_notch_style = "line"
    knob_tickmarks = False
    knob_glow = True
    knob_track_color = "#ffc832"
    knob_label_color = "#d0b880"

    # Waveform - golden with glow and dark panel with grid
    waveform_color = GOLD
    waveform_glow = True
    waveform_center_line = QColor(255, 200, 50, 30)
    waveform_panel = "dark"

    # Timer - LCD panel style with golden color
    timer_use_lcd = True
    timer_color = GOLD

    # Transcription colors (dark honey theme)
    transcription_text = LIGHT_GRAY
    transcription_text_dimmed = GOLD_MUTED
    transcription_panel_bg = (
        "qlineargradient(x1:0, y1:0, x2:0, y2:1, "
        "stop:0 rgba(45,36,22,0.95), stop:1 rgba(30,24,14,0.95))"
    )
    transcription_panel_border = PANEL_BORDER_DARK
    transcription_row_hover = GOLD_8
    transcription_row_btn_bg = CREAM_8
    transcription_row_btn_hover = GOLD_20
    transcription_row_btn_pressed = GOLD_35

    # Chime editor - dark honey with golden accents
    chime_grid_bg = QColor(35, 28, 18)
    chime_grid_line = QColor(65, 52, 32)
    chime_cell_inactive = QColor(48, 40, 26)
    chime_cell_active = QColor(255, 200, 50)
    chime_cell_highlight = QColor(255, 200, 50, 70)
    chime_piano_white = QColor(220, 200, 170)
    chime_piano_black = QColor(40, 32, 20)
    chime_piano_label_white = QColor(60, 48, 30)
    chime_piano_label_black = QColor(180, 160, 120)

    def button_css(self):
        # Glass pill button with warm amber gradient
        return (
            f"QPushButton {{ "
            f"color: {CREAM_70}; "
            f"background: qlineargradient(x1:0, y1:0, x2:0, y2:1, "
            f"stop:0 rgba(80,65,38,0.9), stop:0.1 rgba(65,52,30,0.9), "
            f"stop:0.9 rgba(42,34,20,0.9), stop:1 rgba(35,28,16,0.9)); "
            f"border: 1px solid {HONEY_BORDER}; "
            f"border-radius: 4px; padding: 2px 4px; font-size: 10px; font-family: {self.font}; text-align: left; }}"
            f"QPushButton:hover {{ "
            f"background: qlineargradient(x1:0, y1:0, x2:0, y2:1, "
            f"stop:0 rgba(100,82,48,0.95), stop:0.1 rgba(82,68,40,0.95), "
            f"stop:0.9 rgba(58,48,28,0.95), stop:1 rgba(50,40,24,0.95)); "
            f"border: 1px solid {HONEY_BORDER_HOVER}; }}"
            f"QPushButton:pressed {{ "
            f"background: qlineargradient(x1:0, y1:0, x2:0, y2:1, "
            f"stop:0 rgba(35,28,16,0.95), stop:0.1 rgba(42,34,20,0.95), "
            f"stop:0.9 rgba(58,48,28,0.95), stop:1 rgba(68,56,34,0.95)); "
            f"border: 1px solid {GOLD_60}; }}"
            f"QPushButton:disabled {{ color: {CREAM_20}; background: rgba(45,38,25,0.3); border: 1px solid rgba(70,58,35,0.3); }}"
            f"QPushButton:checked {{ "
            f"background: qlineargradient(x1:0, y1:0, x2:0, y2:1, "
            f"stop:0 rgba(160,130,40,0.5), stop:0.1 rgba(140,110,35,0.5), "
            f"stop:0.9 rgba(110,88,28,0.5), stop:1 rgba(95,76,24,0.5)); "
            f"border: 1px solid {GOLD_60}; }}"
            f"QPushButton:checked:hover {{ "
            f"background: qlineargradient(x1:0, y1:0, x2:0, y2:1, "
            f"stop:0 rgba(180,145,45,0.6), stop:0.1 rgba(155,125,40,0.6), "
            f"stop:0.9 rgba(125,100,32,0.6), stop:1 rgba(110,88,28,0.6)); }}"
        )

    def menu_css(self):
        # Frosted glass menu with warm amber gradient
        return (
            f"QMenu {{ "
            f"background: qlineargradient(x1:0, y1:0, x2:0, y2:1, "
            f"stop:0 rgba(65,52,32,0.95), stop:1 rgba(40,32,20,0.95)); "
            f"color: white; border: 1px solid rgba(110,90,50,0.6); "
            f"border-radius: 8px; padding: 6px; font-family: {self.font}; }}"
            "QMenu::item { padding: 6px 14px; border-radius: 5px; }"
            "QMenu::item:selected { "
            "background: qlineargradient(x1:0, y1:0, x2:0, y2:1, "
            "stop:0 rgba(200,160,40,0.3), stop:1 rgba(160,128,30,0.3)); }"
            f"QMenu::separator {{ height: 1px; background: {CREAM_20}; margin: 4px 8px; }}"
        )

    def _scrollbar_vertical_css(self):
        return (
            "QScrollBar:vertical { width: 10px; background: transparent; margin: 2px; border: none; }"
            "QScrollBar::handle:vertical { "
            "background: qlineargradient(x1:0, y1:0, x2:1, y2:0, "
            "stop:0 rgba(90,72,40,0.6), stop:0.5 rgba(110,90,50,0.7), stop:1 rgba(90,72,40,0.6)); "
            "border-radius: 5px; min-height: 30px; margin: 0px; }"
            "QScrollBar::handle:vertical:hover { "
            "background: qlineargradient(x1:0, y1:0, x2:1, y2:0, "
            "stop:0 rgba(200,160,40,0.5), stop:0.5 rgba(255,200,50,0.6), stop:1 rgba(200,160,40,0.5)); }"
            "QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical { height: 0; }"
            "QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical { background: transparent; }"
        )

    def panel_bg_css(self):
        return (
            "background: qlineargradient(x1:0, y1:0, x2:0, y2:1, "
            "stop:0 rgba(55,44,26,0.95), stop:1 rgba(35,28,16,0.95)); "
            f"border: 1px solid {PANEL_BORDER}; "
            "border-radius: 8px;"
        )

    def panel_bg_flat_css(self):
        return (
            "background: qlineargradient(x1:0, y1:0, x2:0, y2:1, "
            "stop:0 rgba(42,34,20,0.95), stop:1 rgba(28,22,12,0.95)); "
            f"border: 1px solid {PANEL_BORDER_DARK}; "
            "border-radius: 8px;"
        )

    def _draw_hex_grid(self, painter, rect, width, height, alpha_mult):
        """Draw a flat-top hexagonal grid overlay across the window."""
        hex_r = 22  # Hex radius (center to vertex)
        hex_w = hex_r * 2               # Width of flat-top hex
        hex_h = hex_r * math.sqrt(3)    # Height of flat-top hex
        col_step = hex_w * 0.75         # Horizontal spacing between columns
        row_step = hex_h                # Vertical spacing between rows

        painter.setPen(QPen(QColor(200, 170, 60, int(18 * alpha_mult)), 1))
        painter.setBrush(Qt.BrushStyle.NoBrush)

        col = 0
        cx = rect.left() - hex_r
        while cx < rect.right() + hex_r:
            cy_offset = hex_h * 0.5 if col % 2 else 0
            cy = rect.top() - hex_r + cy_offset
            while cy < rect.bottom() + hex_r:
                # Flat-top hexagon: vertices at 0, 60, 120, 180, 240, 300 degrees
                points = []
                for angle_deg in range(0, 360, 60):
                    angle_rad = math.radians(angle_deg)
                    px = cx + hex_r * math.cos(angle_rad)
                    py = cy + hex_r * math.sin(angle_rad)
                    points.append(QPointF(px, py))
                painter.drawPolygon(QPolygonF(points))
                cy += row_step
            cx += col_step
            col += 1

    def paint_window(self, painter, rect, width, height, focused=True):
        """Paint dark honey background with hexagonal grid overlay."""
        radius = self.corner_radius
        alpha_mult = 1.0 if focused else 0.88

        # Clip to window
        clip = QPainterPath()
        clip.addRoundedRect(QRectF(rect), radius, radius)
        painter.setClipPath(clip)

        # Main gradient: dark honey brown
        grad = QLinearGradient(0, rect.top(), 0, rect.bottom())
        grad.setColorAt(0, QColor(58, 46, 28, int(255 * alpha_mult)))
        grad.setColorAt(0.15, QColor(46, 37, 22, int(255 * alpha_mult)))
        grad.setColorAt(0.85, QColor(30, 24, 14, int(255 * alpha_mult)))
        grad.setColorAt(1, QColor(24, 19, 10, int(255 * alpha_mult)))
        painter.setBrush(QBrush(grad))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawRect(rect)

        # Hexagonal grid — THE defining visual element
        self._draw_hex_grid(painter, rect, width, height, alpha_mult)

        # Golden highlight at top
        inner_rect = rect.adjusted(1, 1, -1, -1)
        highlight_grad = QLinearGradient(0, rect.top(), 0, rect.top() + 25)
        highlight_grad.setColorAt(0, QColor(255, 210, 100, int(22 * alpha_mult)))
        highlight_grad.setColorAt(1, QColor(255, 200, 80, 0))
        painter.setBrush(QBrush(highlight_grad))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawRect(inner_rect.adjusted(0, 0, 0, -inner_rect.height() + 25))

        painter.setClipping(False)

        # Border
        painter.setBrush(Qt.BrushStyle.NoBrush)
        painter.setPen(QPen(QColor(100, 80, 45, int(180 * alpha_mult)), 1))
        painter.drawRoundedRect(rect, radius, radius)

        # Golden glow when focused
        if focused:
            for i in range(3):
                glow_alpha = int(40 - i * 12)
                painter.setPen(QPen(QColor(255, 200, 50, glow_alpha), 3 + i * 2))
                painter.drawRoundedRect(rect.adjusted(-i, -i, i, i), radius + i, radius + i)
            painter.setPen(QPen(self.accent, 2))
            painter.drawRoundedRect(rect, radius, radius)

    def paint_waveform_panel(self, painter, rect, w, h, cy):
        """Dark gradient panel with golden grid."""
        # Dark warm gradient background
        panel_grad = QLinearGradient(0, 0, 0, h)
        panel_grad.setColorAt(0, QColor(42, 34, 20, 240))
        panel_grad.setColorAt(0.5, QColor(32, 26, 15, 240))
        panel_grad.setColorAt(1, QColor(24, 19, 10, 240))
        painter.setBrush(QBrush(panel_grad))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawRoundedRect(rect, 8, 8)

        # Subtle golden grid
        painter.setPen(QPen(QColor(255, 200, 50, 15), 1))
        for i in range(1, 4):
            y = int(h * i / 4)
            painter.drawLine(0, y, w, y)
        num_sections = 8
        for i in range(1, num_sections):
            painter.drawLine(int(w * i / num_sections), 0, int(w * i / num_sections), h)

        # Subtle warm border
        painter.setBrush(Qt.BrushStyle.NoBrush)
        painter.setPen(QPen(QColor(70, 56, 32, 150), 1))
        painter.drawRoundedRect(rect, 8, 8)
