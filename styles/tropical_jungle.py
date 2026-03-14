"""Tropical Jungle style - dark rainforest floor with lush green accents."""

import math

from PyQt6.QtCore import Qt, QPointF, QRectF
from PyQt6.QtGui import QColor, QLinearGradient, QRadialGradient, QBrush, QPen, QPainterPath

from .base import BaseStyle, RED_ERROR, LIGHT_GRAY


# -- Accent: bright lime-emerald (warm yellow-green, like sunlit leaves) ------
LEAF_GREEN = QColor(100, 210, 60)
LEAF_GREEN_CSS = "rgb(100,210,60)"

# -- White/alpha for text on dark backgrounds --------------------------------
WHITE_90 = "rgba(255,255,255,0.9)"
WHITE_70 = "rgba(255,255,255,0.7)"
WHITE_40 = "rgba(255,255,255,0.4)"
WHITE_20 = "rgba(255,255,255,0.2)"
WHITE_8 = "rgba(255,255,255,0.08)"

# -- Green accent with alpha -------------------------------------------------
GREEN_90 = "rgba(100,210,60,0.9)"
GREEN_60 = "rgba(100,210,60,0.6)"
GREEN_40 = "rgba(100,210,60,0.4)"
GREEN_35 = "rgba(100,210,60,0.35)"
GREEN_20 = "rgba(80,180,50,0.2)"
GREEN_8 = "rgba(80,180,50,0.08)"
GREEN_MUTED = "rgba(120,170,100,0.7)"

# -- Borders: dark mossy tones -----------------------------------------------
VINE_BORDER = "rgb(60,72,48)"
VINE_BORDER_DARK = "rgb(42,52,35)"
VINE_BORDER_HOVER = "rgb(100,210,60)"
PANEL_BORDER = "rgb(55,65,42)"
PANEL_BORDER_DARK = "rgb(45,55,35)"


class TropicalJungleStyle(BaseStyle):
    name = "tropical_jungle"
    font = "Futura"

    # Accent: bright lime-emerald leaf green
    accent = LEAF_GREEN
    accent_css = LEAF_GREEN_CSS
    text_primary = WHITE_90
    text_secondary = WHITE_70
    text_muted = WHITE_40
    text_error = RED_ERROR
    text_link = GREEN_90
    border_color = VINE_BORDER
    border_dark = VINE_BORDER_DARK
    icon_color_dark = '#ffffff'
    icon_color_light = '#ffffff'
    icon_color_muted = '#8a9a78'

    # Input fields: dark forest floor
    input_bg = '#1e2a18'
    input_text = '#d0e8c0'

    # Slider: green-tinted groove
    slider_groove = "rgba(100,210,60,0.25)"

    # Rotary knob: earthy green
    knob_style = "modern"
    knob_body_dark = "#1a2412"
    knob_body_light = "#3a4e2a"
    knob_notch_style = "line"
    knob_tickmarks = False
    knob_glow = True
    knob_track_color = "#64d23c"
    knob_label_color = "#a0c890"

    # Waveform: green glow on dark panel
    waveform_color = LEAF_GREEN
    waveform_glow = True
    waveform_glow_radius = 18
    waveform_glow_alpha = 180
    waveform_center_line = QColor(100, 210, 60, 25)
    waveform_panel = "dark"

    # Timer: LCD style, green
    timer_use_lcd = True
    timer_color = LEAF_GREEN

    # Transcription panel: dark canopy
    transcription_text = LIGHT_GRAY
    transcription_text_dimmed = GREEN_MUTED
    transcription_panel_bg = (
        "qlineargradient(x1:0, y1:0, x2:0, y2:1, "
        "stop:0 rgba(28,38,22,0.95), stop:1 rgba(18,26,14,0.95))"
    )
    transcription_panel_border = PANEL_BORDER_DARK
    transcription_row_hover = GREEN_8
    transcription_row_btn_bg = WHITE_8
    transcription_row_btn_hover = GREEN_20
    transcription_row_btn_pressed = GREEN_35

    # Chime editor: dark soil with leaf-green highlights
    chime_grid_bg = QColor(22, 30, 18)
    chime_grid_line = QColor(45, 58, 38)
    chime_cell_inactive = QColor(32, 42, 26)
    chime_cell_active = QColor(100, 210, 60)
    chime_cell_highlight = QColor(100, 210, 60, 70)
    chime_piano_white = QColor(200, 215, 190)
    chime_piano_black = QColor(28, 36, 22)
    chime_piano_label_white = QColor(45, 55, 38)
    chime_piano_label_black = QColor(150, 175, 140)

    def button_css(self):
        return (
            f"QPushButton {{ "
            f"color: {WHITE_70}; "
            f"background: qlineargradient(x1:0, y1:0, x2:0, y2:1, "
            f"stop:0 rgba(48,62,38,0.9), stop:0.1 rgba(38,52,30,0.9), "
            f"stop:0.9 rgba(24,36,20,0.9), stop:1 rgba(20,30,16,0.9)); "
            f"border: 1px solid {VINE_BORDER}; "
            f"border-radius: 4px; padding: 2px 4px; font-size: 10px; font-family: {self.font}; text-align: left; }}"
            f"QPushButton:hover {{ "
            f"background: qlineargradient(x1:0, y1:0, x2:0, y2:1, "
            f"stop:0 rgba(58,78,45,0.95), stop:0.1 rgba(48,66,38,0.95), "
            f"stop:0.9 rgba(34,50,28,0.95), stop:1 rgba(28,42,22,0.95)); "
            f"border: 1px solid {VINE_BORDER_HOVER}; }}"
            f"QPushButton:pressed {{ "
            f"background: qlineargradient(x1:0, y1:0, x2:0, y2:1, "
            f"stop:0 rgba(20,30,16,0.95), stop:0.1 rgba(24,36,20,0.95), "
            f"stop:0.9 rgba(34,50,28,0.95), stop:1 rgba(42,58,34,0.95)); "
            f"border: 1px solid {GREEN_60}; }}"
            f"QPushButton:disabled {{ color: {WHITE_20}; background: rgba(28,36,22,0.3); border: 1px solid rgba(42,52,35,0.3); }}"
            f"QPushButton:checked {{ "
            f"background: qlineargradient(x1:0, y1:0, x2:0, y2:1, "
            f"stop:0 rgba(60,140,40,0.5), stop:0.1 rgba(50,120,35,0.5), "
            f"stop:0.9 rgba(40,100,30,0.5), stop:1 rgba(35,90,25,0.5)); "
            f"border: 1px solid {GREEN_60}; }}"
            f"QPushButton:checked:hover {{ "
            f"background: qlineargradient(x1:0, y1:0, x2:0, y2:1, "
            f"stop:0 rgba(70,160,48,0.6), stop:0.1 rgba(60,140,40,0.6), "
            f"stop:0.9 rgba(50,120,35,0.6), stop:1 rgba(45,110,30,0.6)); }}"
        )

    def menu_css(self):
        return (
            f"QMenu {{ "
            f"background: qlineargradient(x1:0, y1:0, x2:0, y2:1, "
            f"stop:0 rgba(38,50,30,0.95), stop:1 rgba(22,32,18,0.95)); "
            f"color: white; border: 1px solid rgba(65,80,50,0.6); "
            f"border-radius: 8px; padding: 6px; font-family: {self.font}; }}"
            "QMenu::item { padding: 6px 14px; border-radius: 5px; }"
            "QMenu::item:selected { "
            "background: qlineargradient(x1:0, y1:0, x2:0, y2:1, "
            "stop:0 rgba(80,180,50,0.3), stop:1 rgba(60,150,35,0.3)); }"
            f"QMenu::separator {{ height: 1px; background: {WHITE_20}; margin: 4px 8px; }}"
        )

    def _scrollbar_vertical_css(self):
        return (
            "QScrollBar:vertical { width: 10px; background: transparent; margin: 2px; border: none; }"
            "QScrollBar::handle:vertical { "
            "background: qlineargradient(x1:0, y1:0, x2:1, y2:0, "
            "stop:0 rgba(55,75,42,0.6), stop:0.5 rgba(70,95,52,0.7), stop:1 rgba(55,75,42,0.6)); "
            "border-radius: 5px; min-height: 30px; margin: 0px; }"
            "QScrollBar::handle:vertical:hover { "
            "background: qlineargradient(x1:0, y1:0, x2:1, y2:0, "
            "stop:0 rgba(80,180,50,0.5), stop:0.5 rgba(100,210,60,0.6), stop:1 rgba(80,180,50,0.5)); }"
            "QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical { height: 0; }"
            "QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical { background: transparent; }"
        )

    def panel_bg_css(self):
        return (
            "background: qlineargradient(x1:0, y1:0, x2:0, y2:1, "
            "stop:0 rgba(32,44,26,0.95), stop:1 rgba(20,30,16,0.95)); "
            f"border: 1px solid {PANEL_BORDER}; "
            "border-radius: 8px;"
        )

    def panel_bg_flat_css(self):
        return (
            "background: qlineargradient(x1:0, y1:0, x2:0, y2:1, "
            "stop:0 rgba(28,38,22,0.95), stop:1 rgba(18,26,14,0.95)); "
            f"border: 1px solid {PANEL_BORDER_DARK}; "
            "border-radius: 8px;"
        )

    def paint_window(self, painter, rect, width, height, focused=True):
        """Paint dark rainforest with dappled sunlight and vine tendrils."""
        radius = self.corner_radius
        alpha_mult = 1.0 if focused else 0.88

        # Clip to window shape
        clip = QPainterPath()
        clip.addRoundedRect(QRectF(rect), radius, radius)
        painter.setClipPath(clip)

        # Main gradient: dark forest floor
        grad = QLinearGradient(0, rect.top(), 0, rect.bottom())
        grad.setColorAt(0, QColor(34, 44, 28, int(255 * alpha_mult)))
        grad.setColorAt(0.15, QColor(26, 36, 22, int(255 * alpha_mult)))
        grad.setColorAt(0.85, QColor(16, 24, 14, int(255 * alpha_mult)))
        grad.setColorAt(1, QColor(12, 18, 10, int(255 * alpha_mult)))
        painter.setBrush(QBrush(grad))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawRect(rect)

        # Dappled sunlight: radial light spots (like sunbeams through canopy gaps)
        # Positions chosen to avoid the center (where text lives)
        dapple_spots = [
            (0.12, 0.08, 35),   # upper-left
            (0.85, 0.06, 28),   # upper-right
            (0.08, 0.65, 22),   # lower-left
            (0.92, 0.72, 25),   # lower-right
            (0.45, 0.03, 40),   # top-center
            (0.70, 0.90, 20),   # bottom-right
        ]
        for fx, fy, r in dapple_spots:
            cx = rect.left() + width * fx
            cy = rect.top() + height * fy
            spot = QRadialGradient(QPointF(cx, cy), r)
            spot.setColorAt(0, QColor(180, 220, 100, int(30 * alpha_mult)))
            spot.setColorAt(0.4, QColor(140, 200, 60, int(15 * alpha_mult)))
            spot.setColorAt(1, QColor(100, 180, 40, 0))
            painter.setBrush(QBrush(spot))
            painter.drawEllipse(QPointF(cx, cy), r, r)

        # Vine tendrils along left and right edges
        painter.setPen(QPen(QColor(60, 90, 40, int(35 * alpha_mult)), 2))
        painter.setBrush(Qt.BrushStyle.NoBrush)
        # Left vine: sinuous curve down the left edge
        vine_path = QPainterPath()
        vine_path.moveTo(rect.left() + 5, rect.top())
        for i in range(6):
            y1 = rect.top() + height * (i * 2 + 1) / 12
            y2 = rect.top() + height * (i * 2 + 2) / 12
            vine_path.cubicTo(
                rect.left() + 18, y1,
                rect.left() + 3, y2 - 15,
                rect.left() + 8, y2
            )
        painter.drawPath(vine_path)
        # Right vine
        vine_r = QPainterPath()
        vine_r.moveTo(rect.right() - 6, rect.top() + 20)
        for i in range(5):
            y1 = rect.top() + 20 + height * (i * 2 + 1) / 11
            y2 = rect.top() + 20 + height * (i * 2 + 2) / 11
            vine_r.cubicTo(
                rect.right() - 20, y1,
                rect.right() - 4, y2 - 12,
                rect.right() - 9, y2
            )
        painter.drawPath(vine_r)

        painter.setClipping(False)

        # Border
        painter.setBrush(Qt.BrushStyle.NoBrush)
        painter.setPen(QPen(QColor(55, 68, 42, int(180 * alpha_mult)), 1))
        painter.drawRoundedRect(rect, radius, radius)

        # Green glow when focused
        if focused:
            for i in range(3):
                glow_alpha = int(35 - i * 10)
                painter.setPen(QPen(QColor(100, 210, 60, glow_alpha), 3 + i * 2))
                painter.drawRoundedRect(rect.adjusted(-i, -i, i, i), radius + i, radius + i)
            painter.setPen(QPen(self.accent, 2))
            painter.drawRoundedRect(rect, radius, radius)

    def paint_waveform_panel(self, painter, rect, w, h, cy):
        """Dark undergrowth panel with faint green grid lines."""
        # Dark gradient background with green undertone
        panel_grad = QLinearGradient(0, 0, 0, h)
        panel_grad.setColorAt(0, QColor(26, 36, 22, 240))
        panel_grad.setColorAt(0.5, QColor(18, 28, 16, 240))
        panel_grad.setColorAt(1, QColor(12, 20, 10, 240))
        painter.setBrush(QBrush(panel_grad))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawRoundedRect(rect, 8, 8)

        # Faint green grid lines (like light filtering through leaves)
        painter.setPen(QPen(QColor(100, 210, 60, 12), 1))
        for i in range(1, 4):
            y = int(h * i / 4)
            painter.drawLine(0, y, w, y)
        num_sections = 8
        for i in range(1, num_sections):
            painter.drawLine(int(w * i / num_sections), 0, int(w * i / num_sections), h)

        # Mossy border
        painter.setBrush(Qt.BrushStyle.NoBrush)
        painter.setPen(QPen(QColor(45, 58, 38, 150), 1))
        painter.drawRoundedRect(rect, 8, 8)
