"""Synthwave/Outrun 80s style - intense neon, sunset gradients, chrome, speed.

Think: Drive (2011), Kavinsky, Perturbator, Far Cry 3: Blood Dragon, Tron.
Distinct from vaporwave: where vaporwave is pastel/dreamy/ironic,
synthwave is INTENSE/chrome/sunset/energetic.

Color palette:
- Background: near-black navy with purple undertones (#0a0618)
- Hot magenta neon accent: #FF0080
- Sunset gradient: orange (#FF6B00) -> hot magenta (#FF0080) -> deep purple (#4A0040)
- Chrome highlight: #C0C8E0 (cool steel blue-white)
- Grid lines: magenta-tinted (#FF0080 at low alpha)
"""

from PyQt6.QtCore import Qt, QRectF
from PyQt6.QtGui import QColor, QLinearGradient, QBrush, QPen, QPainterPath

from .base import BaseStyle


# Synthwave palette - intense neon, NOT pastel
SYNTH_MAGENTA = QColor(255, 0, 128)       # #FF0080 - hot magenta (primary accent)
SYNTH_ORANGE = QColor(255, 107, 0)        # #FF6B00 - sunset orange
SYNTH_PURPLE = QColor(74, 0, 64)          # #4A0040 - deep purple (sunset bottom)
SYNTH_CYAN = QColor(0, 230, 255)          # #00E6FF - electric cyan (secondary)

# Background tones - near-black navy with purple undertone
BG_VOID = QColor(10, 6, 24)              # #0A0618 - deepest void
BG_DARK = QColor(14, 8, 32)              # #0E0820 - dark navy-purple
BG_MID = QColor(22, 12, 48)              # #160C30 - visible purple tint

# Chrome / metallic text tones
CHROME = "rgb(192,200,224)"               # Cool steel white
CHROME_DIM = "rgb(150,155,180)"           # Dimmed chrome
CHROME_MUTED = "rgb(90,85,110)"           # Muted chrome
TEXT_DISABLED = "rgb(55,45,70)"

# Accent CSS strings
MAGENTA_CSS = "rgb(255,0,128)"
ORANGE_CSS = "rgb(255,107,0)"

# Border tones - dark with magenta tint
BORDER_DARK = "rgb(40,15,50)"
BORDER_MID = "rgb(65,20,70)"


class SynthwaveStyle(BaseStyle):
    name = "synthwave"
    font = "Futura"

    # Colors - hot magenta accent on near-black navy
    accent = SYNTH_MAGENTA
    accent_css = MAGENTA_CSS
    text_primary = CHROME
    text_secondary = CHROME_DIM
    text_muted = CHROME_MUTED
    text_error = "rgb(255,60,60)"
    text_link = MAGENTA_CSS
    border_color = BORDER_MID
    border_dark = BORDER_DARK
    icon_color_dark = '#ff0080'   # Hot magenta icons
    icon_color_light = '#ff4da6'  # Lighter magenta
    icon_color_muted = '#802060'  # Dim magenta

    # Dropdown input fields - deep navy with neon text
    input_bg = '#0c0620'
    input_text = '#ff80c0'

    # Slider - magenta groove
    slider_groove = "rgba(255,0,128,0.35)"

    # Rotary knob - neon synthwave style
    knob_style = "neon"
    knob_body_dark = "#0a0618"
    knob_body_light = "#1a0c38"
    knob_notch_style = "dot"
    knob_tickmarks = False
    knob_glow = True
    knob_track_color = "#FF0080"   # Hot magenta track
    knob_label_color = "#ff4da6"   # Lighter magenta text

    # Waveform - hot magenta with glow
    waveform_color = SYNTH_MAGENTA
    waveform_glow = True
    waveform_glow_radius = 20
    waveform_glow_alpha = 200
    waveform_center_line = QColor(255, 0, 128, 40)
    waveform_panel = "synthwave"  # Custom panel type

    # Timer - neon magenta LCD
    timer_use_lcd = True
    timer_color = SYNTH_MAGENTA

    # Transcription - dark navy panel with magenta accents
    transcription_text = CHROME
    transcription_text_dimmed = CHROME_DIM
    transcription_panel_bg = "rgb(10,6,24)"
    transcription_panel_border = BORDER_DARK
    transcription_row_hover = "rgba(255,0,128,0.12)"
    transcription_row_btn_bg = "rgba(255,0,128,0.08)"
    transcription_row_btn_hover = "rgba(255,0,128,0.22)"
    transcription_row_btn_pressed = "rgba(255,0,128,0.38)"

    # Chime editor - synthwave neon on void
    chime_grid_bg = QColor(10, 6, 24)       # Deep void
    chime_grid_line = QColor(40, 15, 50)     # Dark magenta border
    chime_cell_inactive = QColor(22, 12, 48) # Navy-purple
    chime_cell_active = QColor(255, 0, 128)  # Hot magenta
    chime_cell_highlight = QColor(255, 0, 128, 90)  # Magenta glow
    chime_piano_white = QColor(220, 200, 230)  # Cool lavender white
    chime_piano_black = QColor(14, 8, 32)      # Dark navy
    chime_piano_label_white = QColor(80, 40, 90)  # Purple text on light
    chime_piano_label_black = QColor(255, 100, 170)  # Pink text on dark

    def button_css(self):
        # Dark buttons with neon magenta borders - chrome-like highlight on top
        return (
            f"QPushButton {{ color: {CHROME_DIM}; "
            f"background: qlineargradient(x1:0, y1:0, x2:0, y2:1, "
            f"stop:0 rgb(35,18,55), stop:0.08 rgb(22,12,40), "
            f"stop:0.92 rgb(16,8,32), stop:1 rgb(22,12,40)); "
            f"border: 1px solid rgb(255,0,128); "
            f"border-radius: 4px; padding: 4px 10px; font-size: 11px; "
            f"font-family: {self.font}; text-align: left; }}"
            # Hover - magenta glow intensifies
            f"QPushButton:hover {{ color: {MAGENTA_CSS}; "
            f"background: qlineargradient(x1:0, y1:0, x2:0, y2:1, "
            f"stop:0 rgb(55,10,50), stop:0.08 rgb(40,5,38), "
            f"stop:0.92 rgb(30,2,28), stop:1 rgb(40,5,38)); "
            f"border: 1px solid rgb(255,60,160); }}"
            # Pressed - deeper
            f"QPushButton:pressed {{ color: {CHROME}; "
            f"background: qlineargradient(x1:0, y1:0, x2:0, y2:1, "
            f"stop:0 rgb(70,0,55), stop:0.08 rgb(50,0,40), "
            f"stop:0.92 rgb(40,0,30), stop:1 rgb(50,0,40)); "
            f"border: 1px solid rgb(255,100,180); }}"
            # Disabled
            f"QPushButton:disabled {{ color: {TEXT_DISABLED}; "
            f"background: rgb(14,8,28); border: 1px solid rgb(30,15,40); }}"
            # Checked - active magenta state
            f"QPushButton:checked {{ color: {CHROME}; "
            f"background: qlineargradient(x1:0, y1:0, x2:0, y2:1, "
            f"stop:0 rgb(100,0,65), stop:0.5 rgb(80,0,50), stop:1 rgb(60,0,38)); "
            f"border: 1px solid {MAGENTA_CSS}; }}"
            f"QPushButton:checked:hover {{ "
            f"background: qlineargradient(x1:0, y1:0, x2:0, y2:1, "
            f"stop:0 rgb(120,0,75), stop:0.5 rgb(100,0,60), stop:1 rgb(80,0,48)); }}"
        )

    def menu_css(self):
        return (
            f"QMenu {{ background: rgb(10,6,24); color: {CHROME}; "
            f"border: 1px solid rgb(255,0,128); "
            f"border-radius: 4px; padding: 4px; font-family: {self.font}; }}"
            "QMenu::item { padding: 5px 20px; border-radius: 3px; }"
            f"QMenu::item:selected {{ color: {CHROME}; "
            f"background: qlineargradient(x1:0, y1:0, x2:1, y2:0, "
            f"stop:0 rgb(255,0,128), stop:1 rgb(180,0,90)); }}"
            f"QMenu::separator {{ height: 1px; background: rgb(65,20,70); margin: 4px 8px; }}"
        )

    def _scrollbar_vertical_css(self):
        return (
            f"QScrollBar:vertical {{ width: 12px; background: rgb(10,6,24); "
            f"margin: 2px; border: none; border-radius: 6px; }}"
            # Handle - magenta neon
            f"QScrollBar::handle:vertical {{ "
            f"background: qlineargradient(x1:0, y1:0, x2:1, y2:0, "
            f"stop:0 rgb(180,0,90), stop:0.5 rgb(255,0,128), stop:1 rgb(180,0,90)); "
            f"border-radius: 6px; min-height: 30px; margin: 0px; }}"
            # Hover - brighter
            f"QScrollBar::handle:vertical:hover {{ "
            f"background: qlineargradient(x1:0, y1:0, x2:1, y2:0, "
            f"stop:0 rgb(200,0,110), stop:0.5 rgb(255,60,160), stop:1 rgb(200,0,110)); }}"
            "QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical { height: 0; }"
            "QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical { background: transparent; }"
        )

    def panel_bg_css(self):
        return (
            f"background: rgb(10,6,24); "
            f"border: 1px solid rgb(65,20,70); border-radius: 4px;"
        )

    def panel_bg_flat_css(self):
        return (
            f"background: rgb(14,8,32); "
            f"border: 1px solid rgb(40,15,50); border-radius: 4px;"
        )

    def paint_window(self, painter, rect, width, height, focused=True):
        """Paint synthwave background: dark void with sunset gradient at bottom.

        The sunset gradient rises from the bottom: deep purple -> hot magenta -> orange,
        like a retrowave horizon. The top is near-black void with faint stars.
        """
        radius = self.corner_radius
        alpha_mult = 1.0 if focused else 0.8

        # Clip to rounded rect
        path = QPainterPath()
        path.addRoundedRect(QRectF(rect), radius, radius)
        painter.setClipPath(path)

        # Layer 1: Dark void base
        painter.setBrush(QColor(10, 6, 24, int(255 * alpha_mult)))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawRect(rect)

        # Layer 2: Sunset gradient at bottom portion (bottom 45% of window)
        # Gradient direction: bottom to top (orange at very bottom, magenta mid, fading to transparent)
        sunset_top = int(height * 0.55)
        sunset_rect = rect.adjusted(0, sunset_top, 0, 0)
        sunset = QLinearGradient(0, height, 0, sunset_top)
        sunset.setColorAt(0.0, QColor(255, 107, 0, int(55 * alpha_mult)))    # Orange at bottom
        sunset.setColorAt(0.3, QColor(255, 0, 128, int(50 * alpha_mult)))    # Hot magenta
        sunset.setColorAt(0.6, QColor(120, 0, 80, int(35 * alpha_mult)))     # Deep magenta
        sunset.setColorAt(1.0, QColor(74, 0, 64, 0))                         # Fade to transparent
        painter.setBrush(QBrush(sunset))
        painter.drawRect(rect)

        # Layer 3: Subtle horizontal glow line at "horizon" (60% down)
        horizon_y = int(height * 0.65)
        horizon_grad = QLinearGradient(0, horizon_y - 15, 0, horizon_y + 15)
        horizon_grad.setColorAt(0.0, QColor(255, 0, 128, 0))
        horizon_grad.setColorAt(0.5, QColor(255, 60, 140, int(30 * alpha_mult)))
        horizon_grad.setColorAt(1.0, QColor(255, 0, 128, 0))
        painter.setBrush(QBrush(horizon_grad))
        painter.drawRect(rect)

        painter.setClipping(False)

        # Border - magenta neon glow when focused
        if focused:
            painter.setBrush(Qt.BrushStyle.NoBrush)
            # Outer glow layers
            for i in range(2):
                glow_alpha = int(50 - i * 20)
                painter.setPen(QPen(QColor(255, 0, 128, glow_alpha), 2 + i * 2))
                painter.drawRoundedRect(rect.adjusted(-i, -i, i, i), radius + i, radius + i)
            # Crisp inner border
            painter.setPen(QPen(QColor(255, 0, 128, 180), 1))
            painter.drawRoundedRect(rect, radius, radius)
        else:
            painter.setPen(QPen(QColor(65, 20, 70, 150), 1))
            painter.drawRoundedRect(rect, radius, radius)

    def paint_waveform_panel(self, painter, rect, w, h, cy):
        """Synthwave waveform panel: dark void with perspective grid lines.

        Features the classic Outrun perspective grid below the center line,
        neon magenta grid lines, and a dark-to-purple gradient background.
        """
        # Dark gradient background with slight purple at bottom
        panel_grad = QLinearGradient(0, 0, 0, h)
        panel_grad.setColorAt(0.0, QColor(8, 4, 18))
        panel_grad.setColorAt(0.5, QColor(10, 6, 22))
        panel_grad.setColorAt(1.0, QColor(18, 8, 32))
        painter.setBrush(QBrush(panel_grad))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawRect(rect)

        # Subtle sunset glow at bottom third
        glow_rect = rect.adjusted(0, int(h * 0.6), 0, 0)
        glow_grad = QLinearGradient(0, h, 0, int(h * 0.6))
        glow_grad.setColorAt(0.0, QColor(255, 0, 128, 25))
        glow_grad.setColorAt(0.5, QColor(120, 0, 80, 12))
        glow_grad.setColorAt(1.0, QColor(0, 0, 0, 0))
        painter.setBrush(QBrush(glow_grad))
        painter.drawRect(rect)

        # Perspective grid lines below center (the classic Outrun grid)
        grid_color = QColor(255, 0, 128, 25)
        painter.setPen(QPen(grid_color, 1))

        # Horizontal grid lines - spaced closer together near horizon (center)
        grid_line_count = 6
        for i in range(1, grid_line_count + 1):
            # Exponential spacing: lines bunch up near center, spread at bottom
            t = i / grid_line_count
            y = int(cy + (h - cy) * (t * t))
            painter.drawLine(0, y, w, y)

        # Vertical grid lines - converging toward center (perspective)
        vert_count = 9
        vanish_x = w / 2  # Vanishing point at horizontal center
        for i in range(vert_count):
            # Spread across bottom edge
            bottom_x = w * i / (vert_count - 1)
            # Lines converge toward vanishing point at the horizon
            painter.drawLine(int(bottom_x), h, int(vanish_x), int(cy))

        # Magenta border glow
        painter.setBrush(Qt.BrushStyle.NoBrush)
        painter.setPen(QPen(QColor(255, 0, 128, 80), 2))
        painter.drawRect(rect.adjusted(1, 1, -1, -1))
        painter.setPen(QPen(QColor(255, 0, 128, 40), 1))
        painter.drawRect(rect)

        # Center line - magenta
        painter.setPen(QPen(QColor(255, 0, 128, 40), 1))
        painter.drawLine(0, int(cy), w, int(cy))
