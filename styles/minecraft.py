"""Minecraft style - blocky stone and grass aesthetic.

Dark stone backgrounds with grass-green accents. Low border-radius for the
blocky feel. Colors from the Minecraft palette: stone gray, dirt brown,
grass green. Keeps backgrounds muted for text readability.
"""

from PyQt6.QtCore import Qt, QRectF
from PyQt6.QtGui import QColor, QLinearGradient, QBrush, QPen

from .base import BaseStyle, RED_ERROR, LIGHT_GRAY


# Minecraft palette
GRASS_GREEN = QColor(91, 140, 42)           # #5B8C2A - Minecraft grass top
GRASS_GREEN_CSS = "rgb(91,140,42)"
CREEPER_GREEN = QColor(70, 120, 35)         # Darker variant

# Stone grays — dark cobblestone tones
STONE_DARK = QColor(48, 48, 48)             # Dark stone
STONE_MID = QColor(62, 62, 62)              # Mid stone
STONE_LIGHT = QColor(78, 78, 78)            # Lighter stone

# Dirt browns — warm undertone
DIRT_DARK = QColor(52, 40, 28)              # Dark dirt
DIRT_MID = QColor(68, 52, 36)               # Mid dirt

# Text
WHITE_90 = "rgba(255,255,255,0.9)"
WHITE_75 = "rgba(255,255,255,0.75)"
WHITE_50 = "rgba(255,255,255,0.5)"
WHITE_30 = "rgba(255,255,255,0.3)"
WHITE_15 = "rgba(255,255,255,0.15)"
WHITE_8 = "rgba(255,255,255,0.08)"

# Green accent alpha variants
GREEN_90 = "rgba(91,140,42,0.9)"
GREEN_60 = "rgba(91,140,42,0.6)"
GREEN_35 = "rgba(91,140,42,0.35)"
GREEN_20 = "rgba(91,140,42,0.2)"
GREEN_10 = "rgba(91,140,42,0.1)"

# Borders — stone edges
STONE_BORDER = "rgb(72,72,72)"
STONE_BORDER_DARK = "rgb(52,52,52)"
STONE_BORDER_HOVER = "rgb(91,140,42)"
PANEL_BORDER = "rgb(60,60,60)"
PANEL_BORDER_DARK = "rgb(48,48,48)"


class MinecraftStyle(BaseStyle):
    name = "minecraft"
    font = "Menlo"  # Monospace for blocky feel
    corner_radius = 3  # Blocky! Almost no rounding

    # Colors
    accent = GRASS_GREEN
    accent_css = GRASS_GREEN_CSS
    text_primary = WHITE_90
    text_secondary = WHITE_75
    text_muted = WHITE_50
    text_error = RED_ERROR
    text_link = GREEN_90
    border_color = STONE_BORDER
    border_dark = STONE_BORDER_DARK
    icon_color_dark = '#ffffff'
    icon_color_light = '#ffffff'
    icon_color_muted = '#888888'

    # Input fields — dark stone
    input_bg = '#2a2a2a'
    input_text = '#d0d0d0'

    # Slider — green groove on stone
    slider_groove = "rgba(91,140,42,0.2)"

    # Rotary knob — industrial/blocky
    knob_style = "industrial"
    knob_body_dark = "#282828"
    knob_body_light = "#484848"
    knob_notch_style = "line"
    knob_tickmarks = True
    knob_glow = False
    knob_track_color = "#5b8c2a"
    knob_label_color = "#a0b090"

    # Waveform — grass green
    waveform_color = GRASS_GREEN
    waveform_glow = False
    waveform_center_line = QColor(91, 140, 42, 30)
    waveform_panel = "dark"

    # Timer — flat, green
    timer_use_lcd = False
    timer_color = GRASS_GREEN

    # Transcription panel — dark stone
    transcription_text = LIGHT_GRAY
    transcription_text_dimmed = "rgba(140,160,130,0.7)"
    transcription_panel_bg = (
        "qlineargradient(x1:0, y1:0, x2:0, y2:1, "
        "stop:0 rgba(42,42,42,0.95), stop:1 rgba(30,30,30,0.95))"
    )
    transcription_panel_border = PANEL_BORDER_DARK
    transcription_row_hover = GREEN_10
    transcription_row_btn_bg = WHITE_8
    transcription_row_btn_hover = GREEN_20
    transcription_row_btn_pressed = GREEN_35

    # Chime editor — stone and green
    chime_grid_bg = QColor(32, 32, 32)
    chime_grid_line = QColor(52, 52, 52)
    chime_cell_inactive = QColor(42, 42, 42)
    chime_cell_active = QColor(91, 140, 42)
    chime_cell_highlight = QColor(91, 140, 42, 60)
    chime_piano_white = QColor(180, 180, 180)
    chime_piano_black = QColor(32, 32, 32)
    chime_piano_label_white = QColor(50, 50, 50)
    chime_piano_label_black = QColor(150, 150, 150)

    def button_css(self):
        # Stone slab button with subtle gradient — very low border-radius
        return (
            f"QPushButton {{ "
            f"color: {WHITE_75}; "
            f"background: qlineargradient(x1:0, y1:0, x2:0, y2:1, "
            f"stop:0 rgba(78,78,78,0.9), stop:0.05 rgba(68,68,68,0.9), "
            f"stop:0.95 rgba(48,48,48,0.9), stop:1 rgba(42,42,42,0.9)); "
            f"border: 2px solid {STONE_BORDER}; "
            f"border-top: 2px solid rgb(90,90,90); "
            f"border-bottom: 2px solid rgb(38,38,38); "
            f"border-radius: 2px; padding: 2px 4px; font-size: 10px; "
            f"font-family: {self.font}; text-align: left; }}"

            f"QPushButton:hover {{ "
            f"background: qlineargradient(x1:0, y1:0, x2:0, y2:1, "
            f"stop:0 rgba(88,100,72,0.95), stop:0.05 rgba(75,88,60,0.95), "
            f"stop:0.95 rgba(55,65,45,0.95), stop:1 rgba(48,58,38,0.95)); "
            f"border: 2px solid {STONE_BORDER_HOVER}; "
            f"border-top: 2px solid rgb(110,150,70); "
            f"border-bottom: 2px solid rgb(50,75,25); }}"

            f"QPushButton:pressed {{ "
            f"background: qlineargradient(x1:0, y1:0, x2:0, y2:1, "
            f"stop:0 rgba(38,38,38,0.95), stop:0.05 rgba(42,42,42,0.95), "
            f"stop:0.95 rgba(58,58,58,0.95), stop:1 rgba(65,65,65,0.95)); "
            f"border: 2px solid rgb(38,38,38); "
            f"border-top: 2px solid rgb(38,38,38); "
            f"border-bottom: 2px solid rgb(90,90,90); }}"

            f"QPushButton:disabled {{ color: {WHITE_30}; "
            f"background: rgba(40,40,40,0.3); border: 2px solid rgba(52,52,52,0.3); }}"

            f"QPushButton:checked {{ "
            f"background: qlineargradient(x1:0, y1:0, x2:0, y2:1, "
            f"stop:0 rgba(65,100,35,0.7), stop:0.05 rgba(55,85,30,0.65), "
            f"stop:0.95 rgba(40,65,22,0.6), stop:1 rgba(35,55,18,0.55)); "
            f"border: 2px solid {GREEN_60}; "
            f"border-top: 2px solid rgb(100,140,55); "
            f"border-bottom: 2px solid rgb(35,55,18); }}"

            f"QPushButton:checked:hover {{ "
            f"background: qlineargradient(x1:0, y1:0, x2:0, y2:1, "
            f"stop:0 rgba(75,115,42,0.75), stop:0.05 rgba(65,100,35,0.7), "
            f"stop:0.95 rgba(50,80,28,0.65), stop:1 rgba(42,65,22,0.6)); }}"
        )

    def menu_css(self):
        # Stone slab menu
        return (
            f"QMenu {{ "
            f"background: qlineargradient(x1:0, y1:0, x2:0, y2:1, "
            f"stop:0 rgba(68,68,68,0.96), stop:1 rgba(42,42,42,0.96)); "
            f"color: white; border: 2px solid rgb(78,78,78); "
            f"border-top: 2px solid rgb(90,90,90); "
            f"border-bottom: 2px solid rgb(35,35,35); "
            f"border-radius: 2px; padding: 4px; font-family: {self.font}; }}"
            "QMenu::item { padding: 5px 12px; border-radius: 1px; }"
            "QMenu::item:selected { "
            "background: qlineargradient(x1:0, y1:0, x2:0, y2:1, "
            "stop:0 rgba(91,140,42,0.4), stop:1 rgba(70,110,30,0.35)); }"
            f"QMenu::separator {{ height: 2px; background: rgb(52,52,52); margin: 3px 6px; }}"
        )

    def _scrollbar_vertical_css(self):
        return (
            "QScrollBar:vertical { width: 10px; background: rgb(35,35,35); margin: 0px; "
            "border: 1px solid rgb(52,52,52); border-radius: 0px; }"
            "QScrollBar::handle:vertical { "
            "background: qlineargradient(x1:0, y1:0, x2:1, y2:0, "
            "stop:0 rgb(68,68,68), stop:0.5 rgb(78,78,78), stop:1 rgb(68,68,68)); "
            "border: 1px solid rgb(58,58,58); border-radius: 0px; min-height: 30px; }"
            "QScrollBar::handle:vertical:hover { "
            "background: qlineargradient(x1:0, y1:0, x2:1, y2:0, "
            "stop:0 rgb(70,95,50), stop:0.5 rgb(80,110,55), stop:1 rgb(70,95,50)); }"
            "QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical { height: 0; }"
            "QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical { background: rgb(35,35,35); }"
        )

    def panel_bg_css(self):
        return (
            "background: qlineargradient(x1:0, y1:0, x2:0, y2:1, "
            "stop:0 rgba(58,58,58,0.95), stop:1 rgba(38,38,38,0.95)); "
            f"border: 2px solid {PANEL_BORDER}; "
            "border-top: 2px solid rgb(72,72,72); "
            "border-bottom: 2px solid rgb(35,35,35); "
            "border-radius: 2px;"
        )

    def panel_bg_flat_css(self):
        return (
            "background: qlineargradient(x1:0, y1:0, x2:0, y2:1, "
            "stop:0 rgba(42,42,42,0.95), stop:1 rgba(30,30,30,0.95)); "
            f"border: 2px solid {PANEL_BORDER_DARK}; "
            "border-radius: 2px;"
        )

    def paint_window(self, painter, rect, width, height, focused=True):
        """Paint dark stone background with subtle grass-green tint at top."""
        radius = self.corner_radius
        alpha_mult = 1.0 if focused else 0.88

        # Stone gradient — dark gray with very subtle warm brown undertone
        grad = QLinearGradient(0, rect.top(), 0, rect.bottom())
        grad.setColorAt(0, QColor(56, 54, 52, int(255 * alpha_mult)))
        grad.setColorAt(0.08, QColor(48, 46, 44, int(255 * alpha_mult)))
        grad.setColorAt(0.5, QColor(38, 37, 36, int(255 * alpha_mult)))
        grad.setColorAt(0.85, QColor(30, 29, 28, int(255 * alpha_mult)))
        grad.setColorAt(1, QColor(24, 23, 22, int(255 * alpha_mult)))
        painter.setBrush(QBrush(grad))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawRoundedRect(rect, radius, radius)

        # Subtle grass-green tint at the very top (like a grass block top)
        grass_height = int(height * 0.04)
        grass_rect = QRectF(
            rect.left(), rect.top(),
            rect.width(), grass_height
        )
        grass_grad = QLinearGradient(0, rect.top(), 0, rect.top() + grass_height)
        grass_grad.setColorAt(0, QColor(91, 140, 42, int(35 * alpha_mult)))
        grass_grad.setColorAt(1, QColor(91, 140, 42, 0))
        painter.setBrush(QBrush(grass_grad))
        painter.drawRoundedRect(grass_rect, radius, radius)

        # Highlight at top (stone bevel — bright edge)
        bevel_grad = QLinearGradient(0, rect.top(), 0, rect.top() + 3)
        bevel_grad.setColorAt(0, QColor(255, 255, 255, int(20 * alpha_mult)))
        bevel_grad.setColorAt(1, QColor(255, 255, 255, 0))
        painter.setBrush(QBrush(bevel_grad))
        painter.drawRoundedRect(
            rect.adjusted(0, 0, 0, -rect.height() + 5), radius, radius
        )

        # Stone border — bright top/left, dark bottom/right (embossed)
        painter.setBrush(Qt.BrushStyle.NoBrush)
        painter.setPen(QPen(QColor(72, 70, 68, int(200 * alpha_mult)), 2))
        painter.drawRoundedRect(rect, radius, radius)

        # Focus: green accent border (like selection highlight)
        if focused:
            painter.setPen(QPen(QColor(91, 140, 42, int(120 * alpha_mult)), 2))
            painter.drawRoundedRect(rect, radius, radius)

    def paint_waveform_panel(self, painter, rect, w, h, cy):
        """Dark stone panel with green grid."""
        # Dark stone background
        panel_grad = QLinearGradient(0, 0, 0, h)
        panel_grad.setColorAt(0, QColor(42, 40, 38, 240))
        panel_grad.setColorAt(0.5, QColor(34, 33, 32, 240))
        panel_grad.setColorAt(1, QColor(26, 25, 24, 240))
        painter.setBrush(QBrush(panel_grad))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawRoundedRect(rect, 2, 2)

        # Subtle green grid
        painter.setPen(QPen(QColor(91, 140, 42, 15), 1))
        for i in range(1, 4):
            y = int(h * i / 4)
            painter.drawLine(0, y, w, y)
        num_sections = 8
        for i in range(1, num_sections):
            painter.drawLine(int(w * i / num_sections), 0, int(w * i / num_sections), h)

        # Stone border
        painter.setBrush(Qt.BrushStyle.NoBrush)
        painter.setPen(QPen(QColor(52, 50, 48, 180), 2))
        painter.drawRoundedRect(rect, 2, 2)
