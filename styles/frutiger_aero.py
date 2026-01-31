"""Frutiger Aero style - Windows Vista/7 glossy glass aesthetic (2004-2013).

Enhanced with aquatic effects: softer gradients, bubble decorations, wet look.
Color reference from 7.css and Windows Aero design guidelines.
"""

from PyQt6.QtCore import Qt, QPointF
from PyQt6.QtGui import QColor, QLinearGradient, QRadialGradient, QBrush, QPen

from .base import BaseStyle


# Frutiger Aero color palette - more aquatic/cyan tones
# Primary blues (from 7.css and Windows Aero)
AERO_BLUE = QColor(69, 128, 196)        # #4580C4 - Win7 title bar blue
AERO_BLUE_LIGHT = QColor(135, 206, 235) # #87CEEB - sky blue
AERO_BLUE_DARK = QColor(0, 60, 120)     # #003C78 - dark blue
AERO_CYAN = QColor(0, 200, 255)         # #00C8FF - aquatic cyan
AERO_TURQUOISE = QColor(64, 224, 208)   # #40E0D0 - turquoise accent

# Glass panel colors - softer, more aquatic
GLASS_TOP = "rgb(200,220,240)"          # Light blue-tinted top
GLASS_MID = "rgb(230,240,250)"          # Very light cyan-white
GLASS_BOTTOM = "rgb(180,200,220)"       # Soft blue-gray

# Text colors
TEXT_DARK = "rgb(30,30,35)"
TEXT_MID = "rgb(60,60,70)"
TEXT_LIGHT = "rgb(255,255,255)"
TEXT_DISABLED = "rgb(140,140,150)"

# Borders
BORDER_GRAY = "rgb(136,136,136)"        # #888888
BORDER_BLUE = "rgb(0,80,160)"           # #0050A0

# Button gradients - from 7.css Windows 7 style
BTN_TOP = "rgb(242,249,252)"            # #F2F9FC - very light cyan-white
BTN_MID_LIGHT = "rgb(234,246,253)"      # #EAF6FD - light blue tint
BTN_MID = "rgb(190,230,253)"            # #BEE6FD - soft sky blue
BTN_BOTTOM = "rgb(167,217,245)"         # #A7D9F5 - medium sky blue

# Hover state - cyan/aqua tones (from 7.css hover)
BTN_HOVER_TOP = "rgb(234,246,253)"      # #EAF6FD
BTN_HOVER_MID = "rgb(190,230,253)"      # #BEE6FD
BTN_HOVER_BOTTOM = "rgb(135,206,235)"   # #87CEEB - sky blue

# Scrollbar
SCROLL_BG = "rgb(240,240,240)"          # #F0F0F0
SCROLL_HANDLE = "rgb(170,170,170)"      # #AAAAAA
SCROLL_HANDLE_EDGE = "rgb(204,204,204)" # #CCCCCC

# Transcription panel (glassy light)
TRANS_BG = "rgba(200,220,240,230)"      # Light blue glass
TRANS_BORDER = "rgb(173,216,230)"       # Light blue border
TRANS_HOVER = "rgba(100,180,230,0.15)"
TRANS_BTN_BG = "rgba(0,0,0,0.05)"
TRANS_BTN_HOVER = "rgba(6,137,228,0.2)"
TRANS_BTN_PRESSED = "rgba(6,137,228,0.35)"


class FrutigerAeroStyle(BaseStyle):
    name = "frutiger_aero"
    font = "Segoe UI"  # Authentic Aero font

    # Aquatic effects - enable bubbles on waveform panel
    waveform_bubbles = True

    # Colors
    accent = AERO_BLUE
    accent_css = "rgb(69,128,196)"  # CSS version for sliders
    text_primary = TEXT_DARK
    text_secondary = TEXT_MID
    text_muted = "rgb(100,100,110)"
    text_error = "rgb(200,50,50)"
    text_link = "rgb(0,102,204)"
    border_color = BORDER_GRAY
    border_dark = "rgb(100,100,100)"
    icon_color_dark = '#404045'   # Dark icons on light bg
    icon_color_light = '#ffffff'
    icon_color_muted = '#606068'

    # Slider - dark groove on light glass, blue accent
    slider_groove = "rgba(60,60,70,0.5)"

    # Rotary knob - glossy Aero glass style
    knob_style = "aero"
    knob_body_dark = "#b0c8e0"
    knob_body_light = "#e8f4ff"
    knob_notch_style = "needle"
    knob_tickmarks = True
    knob_glow = False

    # Waveform - blue oscilloscope with glow on glass panel
    waveform_color = AERO_BLUE
    waveform_glow = True
    waveform_center_line = QColor(6, 137, 228, 40)
    waveform_panel = "aero"  # New panel type for glass look

    # Timer
    timer_use_lcd = False  # Flat style for Aero
    timer_color = AERO_BLUE

    # Transcription - glassy light panel
    transcription_text = TEXT_DARK
    transcription_text_dimmed = TEXT_MID
    transcription_panel_bg = TRANS_BG
    transcription_panel_border = TRANS_BORDER
    transcription_row_hover = TRANS_HOVER
    transcription_row_btn_bg = TRANS_BTN_BG
    transcription_row_btn_hover = TRANS_BTN_HOVER
    transcription_row_btn_pressed = TRANS_BTN_PRESSED

    # Chime editor - Aero glass blue style
    chime_grid_bg = QColor(20, 40, 60)  # Deep blue
    chime_grid_line = QColor(60, 100, 140)  # Blue border
    chime_cell_inactive = QColor(40, 70, 100)  # Medium blue
    chime_cell_active = QColor(100, 200, 255)  # Bright aqua
    chime_cell_highlight = QColor(100, 200, 255, 100)  # Aqua glow
    chime_piano_white = QColor(220, 235, 250)  # Light blue-white
    chime_piano_black = QColor(30, 50, 70)  # Dark blue
    chime_piano_label_white = QColor(50, 80, 110)  # Blue text
    chime_piano_label_black = QColor(180, 220, 255)  # Light aqua text

    def button_css(self):
        # Soft Aero button - subtle light-to-slightly-darker gradient
        # No harsh dark blue, just gentle silver/white transitions
        return (
            f"QPushButton {{ color: {TEXT_DARK}; "
            f"background: qlineargradient(x1:0, y1:0, x2:0, y2:1, "
            f"stop:0 rgb(250,250,250), stop:0.5 rgb(240,240,242), stop:1 rgb(225,225,230)); "
            f"border: 1px solid rgb(160,160,165); "
            f"border-top: 1px solid rgba(255,255,255,0.9); "
            f"border-radius: 4px; padding: 3px 8px; font-size: 11px; font-family: {self.font}; text-align: left; }}"
            f"QPushButton:hover {{ "
            f"background: qlineargradient(x1:0, y1:0, x2:0, y2:1, "
            f"stop:0 rgb(252,252,255), stop:0.5 rgb(235,245,255), stop:1 rgb(210,230,250)); "
            f"border: 1px solid rgb(120,170,210); }}"
            f"QPushButton:pressed {{ "
            f"background: qlineargradient(x1:0, y1:0, x2:0, y2:1, "
            f"stop:0 rgb(215,215,220), stop:0.5 rgb(225,225,230), stop:1 rgb(235,235,238)); "
            f"border: 1px solid rgb(140,140,145); }}"
            f"QPushButton:disabled {{ color: {TEXT_DISABLED}; "
            f"background: rgb(235,235,235); border: 1px solid rgb(180,180,180); }}"
            f"QPushButton:checked {{ color: {TEXT_DARK}; "
            f"background: qlineargradient(x1:0, y1:0, x2:0, y2:1, "
            f"stop:0 rgb(220,240,255), stop:0.5 rgb(180,220,250), stop:1 rgb(150,200,240)); "
            f"border: 1px solid rgb(80,140,200); "
            f"border-top: 1px solid rgba(255,255,255,0.7); }}"
            f"QPushButton:checked:hover {{ "
            f"background: qlineargradient(x1:0, y1:0, x2:0, y2:1, "
            f"stop:0 rgb(230,245,255), stop:0.5 rgb(190,230,255), stop:1 rgb(160,210,250)); }}"
        )

    def menu_css(self):
        return (
            f"QMenu {{ "
            f"background: qlineargradient(x1:0, y1:0, x2:0, y2:1, "
            f"stop:0 rgb(250,250,252), stop:1 rgb(235,235,240)); "
            f"color: {TEXT_DARK}; border: 1px solid {BORDER_GRAY}; "
            f"border-radius: 4px; padding: 4px; font-family: {self.font}; }}"
            "QMenu::item { padding: 5px 20px; border-radius: 3px; }"
            f"QMenu::item:selected {{ color: {TEXT_LIGHT}; "
            f"background: qlineargradient(x1:0, y1:0, x2:0, y2:1, "
            f"stop:0 rgb(111,215,236), stop:0.5 rgb(6,137,228), stop:1 rgb(0,60,120)); }}"
            f"QMenu::separator {{ height: 1px; background: rgb(200,200,205); margin: 4px 8px; }}"
        )

    def scrollbar_css(self):
        return (
            f"QScrollBar:vertical {{ width: 12px; background: {SCROLL_BG}; margin: 2px; border: none; border-radius: 6px; }}"
            f"QScrollBar::handle:vertical {{ "
            f"background: qlineargradient(x1:0, y1:0, x2:1, y2:0, "
            f"stop:0 {SCROLL_HANDLE_EDGE}, stop:0.5 {SCROLL_HANDLE}, stop:1 rgb(136,136,136)); "
            f"border: 1px solid rgb(102,102,102); border-radius: 6px; min-height: 30px; margin: 0px; }}"
            f"QScrollBar::handle:vertical:hover {{ "
            f"background: qlineargradient(x1:0, y1:0, x2:1, y2:0, "
            f"stop:0 rgb(221,221,221), stop:0.5 rgb(187,187,187), stop:1 rgb(153,153,153)); }}"
            "QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical { height: 0; }"
            "QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical { background: transparent; }"
        )

    def panel_bg_css(self):
        return (
            f"background: qlineargradient(x1:0, y1:0, x2:0, y2:1, "
            f"stop:0 {GLASS_TOP}, stop:0.2 {GLASS_MID}, "
            f"stop:0.5 rgb(216,216,216), stop:1 {GLASS_BOTTOM}); "
            f"border: 1px solid {BORDER_GRAY}; border-radius: 4px;"
        )

    def panel_bg_flat_css(self):
        return (
            f"background: rgba(200,220,240,230); "
            f"border: 1px solid {TRANS_BORDER}; "
            f"border-top: 1px solid rgba(255,255,255,0.6); border-radius: 4px;"
        )

    def paint_window(self, painter, rect, width, height, focused=True):
        """Paint glossy glass Aero background with aquatic effects."""
        radius = self.corner_radius
        alpha_mult = 1.0 if focused else 0.92

        # Aquatic glass gradient (soft blue tones)
        grad = QLinearGradient(0, rect.top(), 0, rect.bottom())
        grad.setColorAt(0, QColor(200, 220, 240, int(255 * alpha_mult)))    # Light blue top
        grad.setColorAt(0.15, QColor(230, 240, 250, int(255 * alpha_mult))) # Very light cyan
        grad.setColorAt(0.5, QColor(220, 235, 250, int(255 * alpha_mult)))  # Soft blue
        grad.setColorAt(1, QColor(180, 200, 220, int(255 * alpha_mult)))    # Deeper blue-gray
        painter.setBrush(QBrush(grad))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawRoundedRect(rect, radius, radius)

        # Top highlight (glossy wet shine)
        inner_rect = rect.adjusted(1, 1, -1, -1)
        highlight_grad = QLinearGradient(0, rect.top(), 0, rect.top() + 35)
        highlight_grad.setColorAt(0, QColor(255, 255, 255, int(150 * alpha_mult)))
        highlight_grad.setColorAt(0.5, QColor(200, 230, 255, int(80 * alpha_mult)))
        highlight_grad.setColorAt(1, QColor(255, 255, 255, 0))
        painter.setBrush(QBrush(highlight_grad))
        painter.drawRoundedRect(inner_rect, radius - 1, radius - 1)

        # Decorative bubbles (static, in corners)
        self._draw_bubble(painter, rect.left() + 15, rect.bottom() - 50, 12, alpha_mult)
        self._draw_bubble(painter, rect.left() + 35, rect.bottom() - 30, 8, alpha_mult)
        self._draw_bubble(painter, rect.right() - 45, rect.bottom() - 45, 10, alpha_mult)
        self._draw_bubble(painter, rect.right() - 25, rect.bottom() - 25, 6, alpha_mult)

        # Border - soft blue tint
        painter.setBrush(Qt.BrushStyle.NoBrush)
        painter.setPen(QPen(QColor(100, 150, 180, int(180 * alpha_mult)), 1))
        painter.drawRoundedRect(rect, radius, radius)

        # Focus glow - cyan Aero accent
        if focused:
            for i in range(3):
                glow_alpha = int(60 - i * 18)
                painter.setPen(QPen(QColor(0, 200, 255, glow_alpha), 2 + i * 2))
                painter.drawRoundedRect(rect.adjusted(-i, -i, i, i), radius + i, radius + i)
            painter.setPen(QPen(AERO_CYAN, 2))
            painter.drawRoundedRect(rect, radius, radius)

    def _draw_bubble(self, painter, x, y, radius, alpha_mult=1.0):
        """Draw a single decorative water bubble with radial gradient."""
        # Bubble gradient - white/cyan center fading to blue edge
        center = QPointF(x + radius * 0.3, y + radius * 0.3)
        bubble_grad = QRadialGradient(center, radius * 1.2)
        bubble_grad.setColorAt(0.0, QColor(255, 255, 255, int(200 * alpha_mult)))
        bubble_grad.setColorAt(0.3, QColor(200, 240, 255, int(180 * alpha_mult)))
        bubble_grad.setColorAt(0.6, QColor(100, 200, 255, int(120 * alpha_mult)))
        bubble_grad.setColorAt(1.0, QColor(50, 150, 200, int(60 * alpha_mult)))

        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(QBrush(bubble_grad))
        painter.drawEllipse(int(x), int(y), int(radius * 2), int(radius * 2))

    def paint_waveform_panel(self, painter, rect, w, h, cy):
        """Frutiger Aero glassy panel with aquatic bubbles."""
        # Glass gradient background
        panel_grad = QLinearGradient(0, 0, 0, h)
        panel_grad.setColorAt(0, QColor(200, 220, 240, 230))
        panel_grad.setColorAt(0.3, QColor(180, 210, 235, 220))
        panel_grad.setColorAt(0.7, QColor(160, 200, 230, 210))
        panel_grad.setColorAt(1, QColor(140, 180, 220, 200))
        painter.setBrush(QBrush(panel_grad))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawRoundedRect(rect, 4, 4)

        # Top glossy highlight
        highlight = QLinearGradient(0, 0, 0, h * 0.4)
        highlight.setColorAt(0, QColor(255, 255, 255, 150))
        highlight.setColorAt(0.5, QColor(255, 255, 255, 50))
        highlight.setColorAt(1, QColor(255, 255, 255, 0))
        painter.setBrush(QBrush(highlight))
        painter.drawRoundedRect(rect.adjusted(1, 1, -1, -int(h * 0.6)), 3, 3)

        # Subtle grid
        painter.setPen(QPen(QColor(6, 137, 228, 20), 1))
        for i in range(1, 4):
            y = int(h * i / 4)
            painter.drawLine(0, y, w, y)

        # Decorative bubbles (static, corners only)
        self._draw_bubble(painter, 8, h - 22, 6, 0.7)
        self._draw_bubble(painter, 20, h - 14, 4, 0.6)
        self._draw_bubble(painter, w - 28, h - 20, 5, 0.65)
        self._draw_bubble(painter, w - 15, h - 10, 3, 0.5)

        # Panel border
        painter.setBrush(Qt.BrushStyle.NoBrush)
        painter.setPen(QPen(QColor(136, 136, 136), 1))
        painter.drawRoundedRect(rect, 4, 4)

        # Center line
        painter.setPen(QPen(QColor(6, 137, 228, 60), 1))
        painter.drawLine(0, int(cy), w, int(cy))
