"""Vaporwave style - pink/purple/cyan aesthetic.

Color reference verified from color-hex.com/color-palette/10221:
- Hot Pink: #ff71ce (255,113,206)
- Cyan: #01cdfe (1,205,254)
- Mint Green: #05ffa1 (5,255,161)
- Purple: #b967ff (185,103,255)
- Pale Yellow: #fffb96 (255,251,150)
"""

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor, QLinearGradient, QBrush, QPen

from .base import BaseStyle


# Verified Vaporwave palette from color-hex.com/color-palette/10221
VAPOR_PINK = QColor(255, 113, 206)      # #ff71ce - hot pink
VAPOR_CYAN = QColor(1, 205, 254)        # #01cdfe - cyan
VAPOR_MINT = QColor(5, 255, 161)        # #05ffa1 - mint green
VAPOR_PURPLE = QColor(185, 103, 255)    # #b967ff - purple
VAPOR_YELLOW = QColor(255, 251, 150)    # #fffb96 - pale yellow

# Dark purple background (from schemecolor.com vaporwave)
VAPOR_BG_DARK = QColor(48, 3, 80)       # #300350 - russian violet / dark plum
VAPOR_BG_MID = QColor(60, 20, 90)       # Slightly lighter purple

# Text colors - high contrast on dark backgrounds
TEXT_WHITE = "rgb(255,255,255)"
TEXT_YELLOW = "rgb(255,251,150)"        # Pale yellow for good contrast
TEXT_PINK = "rgb(255,113,206)"          # Hot pink for accents
TEXT_DISABLED = "rgb(120,80,140)"


class VaporwaveStyle(BaseStyle):
    name = "vaporwave"
    font = "Futura"  # Vaporwave aesthetic font

    # Colors - pink accent on dark purple background
    accent = VAPOR_PINK
    accent_css = "rgb(255,113,206)"
    text_primary = TEXT_WHITE
    text_secondary = "rgba(255,255,255,0.85)"
    text_muted = "rgba(255,255,255,0.6)"
    text_error = "rgb(255,100,100)"
    text_link = TEXT_PINK
    border_color = "rgb(100,60,140)"
    border_dark = "rgb(60,20,90)"
    icon_color_dark = '#ff9cdd'   # Lighter hot pink icons (more readable on dark)
    icon_color_light = '#ffffff'
    icon_color_muted = '#ffccea'  # Lighter pink for disabled (more visible)

    # Slider - cyan groove on dark purple (contrasts with pink accent)
    slider_groove = "rgba(1,205,254,0.4)"  # Cyan with transparency

    # Rotary knob - neon vaporwave style with cyan track
    knob_style = "neon"
    knob_body_dark = "#301050"
    knob_body_light = "#502078"
    knob_notch_style = "dot"
    knob_tickmarks = False
    knob_glow = True
    knob_track_color = "#01cdfe"  # Cyan track (vaporwave cyan)
    knob_label_color = "#ff71ce"  # Hot pink text

    # Waveform - pink on dark purple
    waveform_color = VAPOR_PINK
    waveform_glow = True
    waveform_center_line = QColor(255, 113, 206, 40)
    waveform_panel = "vaporwave"  # Custom panel type

    # Timer - pink LCD style
    timer_use_lcd = True
    timer_color = VAPOR_PINK

    # Transcription - dark purple panel with pink accents
    transcription_text = TEXT_WHITE
    transcription_text_dimmed = "rgba(255,255,255,0.7)"
    transcription_panel_bg = "rgb(48,3,80)"
    transcription_panel_border = "rgb(100,60,140)"
    transcription_row_hover = "rgba(255,113,206,0.15)"  # Pink hover
    transcription_row_btn_bg = "rgba(255,255,255,0.08)"
    transcription_row_btn_hover = "rgba(255,113,206,0.25)"
    transcription_row_btn_pressed = "rgba(255,113,206,0.4)"

    # Chime editor - vaporwave pink/purple aesthetic
    chime_grid_bg = QColor(48, 3, 80)  # Deep purple
    chime_grid_line = QColor(100, 60, 140)  # Purple border
    chime_cell_inactive = QColor(70, 30, 110)  # Medium purple
    chime_cell_active = QColor(255, 113, 206)  # Hot pink
    chime_cell_highlight = QColor(255, 113, 206, 100)  # Pink glow
    chime_piano_white = QColor(255, 220, 240)  # Light pink
    chime_piano_black = QColor(60, 20, 90)  # Dark purple
    chime_piano_label_white = QColor(100, 50, 130)  # Purple text on pink
    chime_piano_label_black = QColor(255, 180, 230)  # Light pink text

    def button_css(self):
        # Pink/purple gradient buttons with glow
        return (
            f"QPushButton {{ color: {TEXT_WHITE}; "
            f"background: qlineargradient(x1:0, y1:0, x2:0, y2:1, "
            f"stop:0 rgb(185,103,255), stop:0.5 rgb(150,80,200), stop:1 rgb(120,60,170)); "
            f"border: 1px solid rgb(255,113,206); "
            f"border-radius: 4px; padding: 4px 10px; font-size: 11px; font-family: {self.font}; text-align: left; }}"
            f"QPushButton:hover {{ "
            f"background: qlineargradient(x1:0, y1:0, x2:0, y2:1, "
            f"stop:0 rgb(200,120,255), stop:0.5 rgb(170,100,220), stop:1 rgb(140,80,190)); "
            f"border: 1px solid rgb(255,150,220); }}"
            f"QPushButton:pressed {{ "
            f"background: qlineargradient(x1:0, y1:0, x2:0, y2:1, "
            f"stop:0 rgb(100,50,150), stop:0.5 rgb(130,70,180), stop:1 rgb(160,90,200)); "
            f"border: 1px solid rgb(200,80,180); }}"
            f"QPushButton:disabled {{ color: {TEXT_DISABLED}; "
            f"background: rgb(60,30,80); border: 1px solid rgb(80,50,100); }}"
            f"QPushButton:checked {{ color: {TEXT_WHITE}; "
            f"background: qlineargradient(x1:0, y1:0, x2:0, y2:1, "
            f"stop:0 rgb(255,130,220), stop:0.5 rgb(255,113,206), stop:1 rgb(220,90,180)); "
            f"border: 1px solid rgb(255,150,230); }}"
            f"QPushButton:checked:hover {{ "
            f"background: qlineargradient(x1:0, y1:0, x2:0, y2:1, "
            f"stop:0 rgb(255,150,230), stop:0.5 rgb(255,130,220), stop:1 rgb(240,110,200)); }}"
        )

    def menu_css(self):
        return (
            f"QMenu {{ "
            f"background: rgb(48,3,80); "
            f"color: {TEXT_WHITE}; "
            f"border: 1px solid rgb(255,113,206); "
            f"border-radius: 4px; padding: 4px; font-family: {self.font}; }}"
            "QMenu::item { padding: 5px 20px; border-radius: 3px; }"
            f"QMenu::item:selected {{ color: {TEXT_WHITE}; "
            f"background: qlineargradient(x1:0, y1:0, x2:1, y2:0, "
            f"stop:0 rgb(255,113,206), stop:1 rgb(185,103,255)); }}"
            f"QMenu::separator {{ height: 1px; background: rgb(100,60,140); margin: 4px 8px; }}"
        )

    def _scrollbar_vertical_css(self):
        return (
            f"QScrollBar:vertical {{ width: 12px; background: rgb(48,3,80); margin: 2px; border: none; border-radius: 6px; }}"
            f"QScrollBar::handle:vertical {{ "
            f"background: qlineargradient(x1:0, y1:0, x2:1, y2:0, "
            f"stop:0 rgb(185,103,255), stop:1 rgb(255,113,206)); "
            f"border-radius: 6px; min-height: 30px; margin: 0px; }}"
            f"QScrollBar::handle:vertical:hover {{ "
            f"background: qlineargradient(x1:0, y1:0, x2:1, y2:0, "
            f"stop:0 rgb(200,120,255), stop:1 rgb(255,140,220)); }}"
            "QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical { height: 0; }"
            "QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical { background: transparent; }"
        )

    def panel_bg_css(self):
        return (
            f"background: rgb(48,3,80); "
            f"border: 1px solid rgb(100,60,140); border-radius: 4px;"
        )

    def panel_bg_flat_css(self):
        return (
            f"background: rgb(60,20,90); "
            f"border: 1px solid rgb(80,40,120); border-radius: 4px;"
        )

    def paint_window(self, painter, rect, width, height, focused=True):
        """Paint vaporwave dark purple background with pink/cyan gradient."""
        radius = self.corner_radius
        alpha_mult = 1.0 if focused else 0.85

        # Dark purple base
        painter.setBrush(QColor(48, 3, 80, int(255 * alpha_mult)))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawRoundedRect(rect, radius, radius)

        # Horizontal pink-to-cyan gradient at bottom
        grad_rect = rect.adjusted(0, int(height * 0.6), 0, 0)
        vapor_grad = QLinearGradient(0, grad_rect.top(), width, grad_rect.bottom())
        vapor_grad.setColorAt(0, QColor(255, 113, 206, int(60 * alpha_mult)))  # Pink
        vapor_grad.setColorAt(0.5, QColor(185, 103, 255, int(40 * alpha_mult)))  # Purple
        vapor_grad.setColorAt(1, QColor(1, 205, 254, int(50 * alpha_mult)))  # Cyan
        painter.setBrush(QBrush(vapor_grad))
        painter.drawRoundedRect(rect, radius, radius)

        # Subtle top highlight
        highlight_rect = rect.adjusted(1, 1, -1, -int(height * 0.85))
        highlight_grad = QLinearGradient(0, rect.top(), 0, rect.top() + 40)
        highlight_grad.setColorAt(0, QColor(255, 255, 255, int(25 * alpha_mult)))
        highlight_grad.setColorAt(1, QColor(255, 255, 255, 0))
        painter.setBrush(QBrush(highlight_grad))
        painter.drawRoundedRect(highlight_rect, radius - 1, radius - 1)

        # Pink glow border when focused
        if focused:
            painter.setBrush(Qt.BrushStyle.NoBrush)
            for i in range(2):
                glow_alpha = int(60 - i * 25)
                painter.setPen(QPen(QColor(255, 113, 206, glow_alpha), 2 + i * 2))
                painter.drawRoundedRect(rect.adjusted(-i, -i, i, i), radius + i, radius + i)
            painter.setPen(QPen(QColor(255, 113, 206, 180), 1))
            painter.drawRoundedRect(rect, radius, radius)
        else:
            painter.setPen(QPen(QColor(100, 60, 140, 150), 1))
            painter.drawRoundedRect(rect, radius, radius)

    def paint_waveform_panel(self, painter, rect, w, h, cy):
        """Vaporwave-style dark purple panel with pink/cyan gradient accents."""
        # Dark purple background (#300350 - russian violet)
        painter.setBrush(QColor(48, 3, 80))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawRect(rect)

        # Horizontal pink-to-cyan gradient at bottom third
        grad_rect = rect.adjusted(0, int(h * 0.6), 0, 0)
        vapor_grad = QLinearGradient(0, grad_rect.top(), w, grad_rect.bottom())
        vapor_grad.setColorAt(0, QColor(255, 113, 206, 50))    # Hot pink
        vapor_grad.setColorAt(0.5, QColor(185, 103, 255, 35))  # Purple
        vapor_grad.setColorAt(1, QColor(1, 205, 254, 45))      # Cyan
        painter.setBrush(QBrush(vapor_grad))
        painter.drawRect(rect)

        # Subtle scanlines for retro effect
        painter.setPen(QPen(QColor(255, 113, 206, 15), 1))
        for y_line in range(0, h, 4):
            painter.drawLine(0, y_line, w, y_line)

        # Pink border glow
        painter.setBrush(Qt.BrushStyle.NoBrush)
        painter.setPen(QPen(QColor(255, 113, 206, 100), 2))
        painter.drawRect(rect.adjusted(1, 1, -1, -1))
        painter.setPen(QPen(QColor(255, 113, 206, 50), 1))
        painter.drawRect(rect)

        # Center line in pink
        painter.setPen(QPen(QColor(255, 113, 206, 40), 1))
        painter.drawLine(0, int(cy), w, int(cy))
