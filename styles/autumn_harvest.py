"""Autumn Harvest style - warm amber/orange dark theme with fall colors."""

from PyQt6.QtCore import Qt, QRectF
from PyQt6.QtGui import QColor, QLinearGradient, QRadialGradient, QBrush, QPen, QPainterPath

from .base import BaseStyle, RED_ERROR, LIGHT_GRAY


# White/cream with alpha
CREAM_90 = "rgba(255,240,220,0.9)"
CREAM_70 = "rgba(255,235,210,0.7)"
CREAM_60 = "rgba(255,230,200,0.6)"
CREAM_40 = "rgba(255,225,190,0.4)"
CREAM_20 = "rgba(255,220,180,0.2)"
CREAM_8 = "rgba(255,220,180,0.08)"

# Amber accent colors
AMBER = QColor(220, 160, 50)
AMBER_CSS = "rgb(220,160,50)"
AMBER_MUTED = "rgba(180,140,80,0.7)"
AMBER_90 = "rgba(220,160,50,0.9)"
AMBER_60 = "rgba(220,160,50,0.6)"
AMBER_35 = "rgba(220,160,50,0.35)"
AMBER_20 = "rgba(200,150,60,0.2)"
AMBER_8 = "rgba(200,150,60,0.08)"

# Glass effect borders - warm browns
GLASS_BORDER = "rgb(100,75,50)"
GLASS_BORDER_DARK = "rgb(70,52,35)"
GLASS_BORDER_HOVER = "rgb(220,160,50)"
PANEL_BORDER = "rgb(85,65,45)"
PANEL_BORDER_DARK = "rgb(70,55,38)"


class AutumnHarvestStyle(BaseStyle):
    name = "autumn_harvest"
    font = "Futura"

    # Dark warm theme colors
    accent = AMBER
    accent_css = AMBER_CSS
    text_primary = CREAM_90
    text_secondary = CREAM_70
    text_muted = CREAM_40
    text_error = RED_ERROR
    text_link = AMBER_90
    border_color = GLASS_BORDER
    border_dark = GLASS_BORDER_DARK
    icon_color_dark = '#ffffff'
    icon_color_light = '#ffffff'
    icon_color_muted = '#a08860'

    # Dropdown input fields - dark warm brown
    input_bg = '#2e2218'
    input_text = '#f0dcc0'

    # Slider - semi-transparent amber groove
    slider_groove = "rgba(220,160,50,0.25)"

    # Rotary knob - glass pill style with amber
    knob_style = "glass"
    knob_body_dark = "#28200a"
    knob_body_light = "#50401a"
    knob_notch_style = "line"
    knob_tickmarks = False
    knob_glow = True
    knob_track_color = "#dca032"
    knob_label_color = "#c8a878"

    # Waveform - amber with glow and dark panel with grid
    waveform_color = AMBER
    waveform_glow = True
    waveform_center_line = QColor(220, 160, 50, 30)
    waveform_panel = "dark"

    # Timer - LCD panel style with amber
    timer_use_lcd = True
    timer_color = AMBER

    # Transcription colors (dark warm theme)
    transcription_text = LIGHT_GRAY
    transcription_text_dimmed = AMBER_MUTED
    transcription_panel_bg = (
        "qlineargradient(x1:0, y1:0, x2:0, y2:1, "
        "stop:0 rgba(48,35,22,0.95), stop:1 rgba(32,24,14,0.95))"
    )
    transcription_panel_border = PANEL_BORDER_DARK
    transcription_row_hover = AMBER_8
    transcription_row_btn_bg = CREAM_8
    transcription_row_btn_hover = AMBER_20
    transcription_row_btn_pressed = AMBER_35

    # Chime editor - dark brown with amber accents
    chime_grid_bg = QColor(35, 28, 18)
    chime_grid_line = QColor(65, 50, 32)
    chime_cell_inactive = QColor(48, 38, 24)
    chime_cell_active = QColor(220, 160, 50)
    chime_cell_highlight = QColor(220, 160, 50, 70)
    chime_piano_white = QColor(215, 200, 175)
    chime_piano_black = QColor(40, 32, 20)
    chime_piano_label_white = QColor(60, 48, 30)
    chime_piano_label_black = QColor(170, 145, 110)

    def button_css(self):
        # Glass pill button with warm gradient
        return (
            f"QPushButton {{ "
            f"color: {CREAM_70}; "
            f"background: qlineargradient(x1:0, y1:0, x2:0, y2:1, "
            f"stop:0 rgba(85,65,40,0.9), stop:0.1 rgba(68,50,30,0.9), "
            f"stop:0.9 rgba(45,33,18,0.9), stop:1 rgba(38,28,15,0.9)); "
            f"border: 1px solid {GLASS_BORDER}; "
            f"border-radius: 4px; padding: 2px 4px; font-size: 10px; font-family: {self.font}; text-align: left; }}"
            f"QPushButton:hover {{ "
            f"background: qlineargradient(x1:0, y1:0, x2:0, y2:1, "
            f"stop:0 rgba(105,80,48,0.95), stop:0.1 rgba(88,65,38,0.95), "
            f"stop:0.9 rgba(62,46,26,0.95), stop:1 rgba(52,40,22,0.95)); "
            f"border: 1px solid {GLASS_BORDER_HOVER}; }}"
            f"QPushButton:pressed {{ "
            f"background: qlineargradient(x1:0, y1:0, x2:0, y2:1, "
            f"stop:0 rgba(38,28,15,0.95), stop:0.1 rgba(45,33,18,0.95), "
            f"stop:0.9 rgba(62,46,26,0.95), stop:1 rgba(72,55,32,0.95)); "
            f"border: 1px solid {AMBER_60}; }}"
            f"QPushButton:disabled {{ color: {CREAM_20}; background: rgba(45,35,20,0.3); border: 1px solid rgba(70,52,35,0.3); }}"
            f"QPushButton:checked {{ "
            f"background: qlineargradient(x1:0, y1:0, x2:0, y2:1, "
            f"stop:0 rgba(160,110,30,0.5), stop:0.1 rgba(140,95,25,0.5), "
            f"stop:0.9 rgba(120,80,20,0.5), stop:1 rgba(105,72,18,0.5)); "
            f"border: 1px solid {AMBER_60}; }}"
            f"QPushButton:checked:hover {{ "
            f"background: qlineargradient(x1:0, y1:0, x2:0, y2:1, "
            f"stop:0 rgba(175,125,35,0.6), stop:0.1 rgba(155,108,30,0.6), "
            f"stop:0.9 rgba(135,92,25,0.6), stop:1 rgba(120,82,22,0.6)); }}"
        )

    def menu_css(self):
        # Frosted glass menu with warm gradient
        return (
            f"QMenu {{ "
            f"background: qlineargradient(x1:0, y1:0, x2:0, y2:1, "
            f"stop:0 rgba(68,52,32,0.95), stop:1 rgba(42,32,18,0.95)); "
            f"color: white; border: 1px solid rgba(110,85,55,0.6); "
            f"border-radius: 8px; padding: 6px; font-family: {self.font}; }}"
            "QMenu::item { padding: 6px 14px; border-radius: 5px; }"
            "QMenu::item:selected { "
            "background: qlineargradient(x1:0, y1:0, x2:0, y2:1, "
            "stop:0 rgba(200,150,60,0.3), stop:1 rgba(170,120,40,0.3)); }"
            f"QMenu::separator {{ height: 1px; background: {CREAM_20}; margin: 4px 8px; }}"
        )

    def _scrollbar_vertical_css(self):
        return (
            "QScrollBar:vertical { width: 10px; background: transparent; margin: 2px; border: none; }"
            "QScrollBar::handle:vertical { "
            "background: qlineargradient(x1:0, y1:0, x2:1, y2:0, "
            "stop:0 rgba(100,75,45,0.6), stop:0.5 rgba(120,90,55,0.7), stop:1 rgba(100,75,45,0.6)); "
            "border-radius: 5px; min-height: 30px; margin: 0px; }"
            "QScrollBar::handle:vertical:hover { "
            "background: qlineargradient(x1:0, y1:0, x2:1, y2:0, "
            "stop:0 rgba(200,150,50,0.5), stop:0.5 rgba(220,160,50,0.6), stop:1 rgba(200,150,50,0.5)); }"
            "QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical { height: 0; }"
            "QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical { background: transparent; }"
        )

    def panel_bg_css(self):
        return (
            "background: qlineargradient(x1:0, y1:0, x2:0, y2:1, "
            "stop:0 rgba(55,42,26,0.95), stop:1 rgba(36,28,16,0.95)); "
            f"border: 1px solid {PANEL_BORDER}; "
            "border-radius: 8px;"
        )

    def panel_bg_flat_css(self):
        return (
            "background: qlineargradient(x1:0, y1:0, x2:0, y2:1, "
            "stop:0 rgba(45,35,20,0.95), stop:1 rgba(30,24,12,0.95)); "
            f"border: 1px solid {PANEL_BORDER_DARK}; "
            "border-radius: 8px;"
        )

    def _draw_leaf(self, painter, cx, cy, size, angle, alpha_mult):
        """Draw a simple leaf silhouette at the given position and rotation."""
        painter.save()
        painter.translate(cx, cy)
        painter.rotate(angle)
        leaf = QPainterPath()
        # Simple leaf shape: two cubic curves forming an eye/leaf
        s = size
        leaf.moveTo(0, -s)
        leaf.cubicTo(s * 0.6, -s * 0.6, s * 0.5, s * 0.3, 0, s)
        leaf.cubicTo(-s * 0.5, s * 0.3, -s * 0.6, -s * 0.6, 0, -s)
        painter.setBrush(QBrush(QColor(180, 120, 30, int(18 * alpha_mult))))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawPath(leaf)
        painter.restore()

    def paint_window(self, painter, rect, width, height, focused=True):
        """Paint warm autumn scene with diagonal light shaft and falling leaves."""
        radius = self.corner_radius
        alpha_mult = 1.0 if focused else 0.88

        # Clip to window
        clip = QPainterPath()
        clip.addRoundedRect(QRectF(rect), radius, radius)
        painter.setClipPath(clip)

        # Main gradient: dark chocolate brown
        grad = QLinearGradient(0, rect.top(), 0, rect.bottom())
        grad.setColorAt(0, QColor(58, 42, 24, int(255 * alpha_mult)))
        grad.setColorAt(0.15, QColor(46, 34, 18, int(255 * alpha_mult)))
        grad.setColorAt(0.85, QColor(32, 24, 12, int(255 * alpha_mult)))
        grad.setColorAt(1, QColor(25, 18, 8, int(255 * alpha_mult)))
        painter.setBrush(QBrush(grad))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawRect(rect)

        # Diagonal warm light shaft from upper-right corner
        # Simulated with a diagonal linear gradient overlay
        shaft = QLinearGradient(
            rect.right() - width * 0.15, rect.top(),
            rect.left() + width * 0.4, rect.bottom()
        )
        shaft.setColorAt(0, QColor(255, 200, 100, int(20 * alpha_mult)))
        shaft.setColorAt(0.3, QColor(255, 180, 80, int(12 * alpha_mult)))
        shaft.setColorAt(0.5, QColor(255, 160, 60, int(5 * alpha_mult)))
        shaft.setColorAt(1, QColor(0, 0, 0, 0))
        painter.setBrush(QBrush(shaft))
        painter.drawRect(rect)

        # Scattered leaf silhouettes along edges (avoiding center text area)
        leaves = [
            (0.08, 0.12, 8, -30),
            (0.88, 0.08, 7, 45),
            (0.05, 0.80, 6, -60),
            (0.92, 0.85, 9, 20),
            (0.15, 0.92, 7, -15),
            (0.82, 0.40, 5, 70),
            (0.95, 0.60, 6, -45),
            (0.03, 0.45, 5, 35),
        ]
        for fx, fy, size, angle in leaves:
            lx = rect.left() + width * fx
            ly = rect.top() + height * fy
            self._draw_leaf(painter, lx, ly, size, angle, alpha_mult)

        painter.setClipping(False)

        # Border
        painter.setBrush(Qt.BrushStyle.NoBrush)
        painter.setPen(QPen(QColor(95, 72, 42, int(180 * alpha_mult)), 1))
        painter.drawRoundedRect(rect, radius, radius)

        # Amber glow when focused
        if focused:
            for i in range(3):
                glow_alpha = int(40 - i * 12)
                painter.setPen(QPen(QColor(220, 160, 50, glow_alpha), 3 + i * 2))
                painter.drawRoundedRect(rect.adjusted(-i, -i, i, i), radius + i, radius + i)
            painter.setPen(QPen(self.accent, 2))
            painter.drawRoundedRect(rect, radius, radius)

    def paint_waveform_panel(self, painter, rect, w, h, cy):
        """Dark warm panel with amber grid."""
        # Dark gradient background
        panel_grad = QLinearGradient(0, 0, 0, h)
        panel_grad.setColorAt(0, QColor(42, 32, 18, 240))
        panel_grad.setColorAt(0.5, QColor(34, 26, 14, 240))
        panel_grad.setColorAt(1, QColor(26, 20, 10, 240))
        painter.setBrush(QBrush(panel_grad))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawRoundedRect(rect, 8, 8)

        # Subtle amber grid
        painter.setPen(QPen(QColor(220, 160, 50, 15), 1))
        for i in range(1, 4):
            y = int(h * i / 4)
            painter.drawLine(0, y, w, y)
        num_sections = 8
        for i in range(1, num_sections):
            painter.drawLine(int(w * i / num_sections), 0, int(w * i / num_sections), h)

        # Subtle border
        painter.setBrush(Qt.BrushStyle.NoBrush)
        painter.setPen(QPen(QColor(70, 55, 35, 150), 1))
        painter.drawRoundedRect(rect, 8, 8)
