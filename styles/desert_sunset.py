"""Desert Sunset style - warm oranges and deep purples on dark desert ground.

Think: Arizona twilight, red sandstone under a sky fading from
burnt orange through magenta into deep indigo. Warm, earthy, natural.

Color palette:
- Background: deep warm brown-red (#1e120e) transitioning to desert purple (#1a0e1e)
- Accent: sunset orange (#FF8C42) - warm and natural, not neon
- Secondary: dusty rose (#C46B6B) / muted magenta (#8B3A62)
- Text: warm cream (#F0DCC8) on dark backgrounds
- Grid/borders: warm desaturated rust tones
"""

from PyQt6.QtCore import Qt, QPointF, QRectF
from PyQt6.QtGui import QColor, QLinearGradient, QRadialGradient, QBrush, QPen, QPainterPath

from .base import BaseStyle, RED_ERROR, LIGHT_GRAY


# Desert sunset palette
SUNSET_ORANGE = QColor(255, 140, 66)      # #FF8C42 - warm sunset orange (primary accent)
SUNSET_AMBER = QColor(230, 120, 50)       # Slightly deeper amber
DESERT_PURPLE = QColor(90, 40, 80)        # #5A2850 - dusky purple horizon
DESERT_ROSE = QColor(196, 107, 107)       # #C46B6B - dusty rose

# Background tones - warm dark browns with red/purple undertones
BG_GROUND = QColor(30, 18, 14)            # #1E120E - darkest desert ground
BG_WARM = QColor(38, 22, 18)             # #261612 - warm dark brown
BG_SKY = QColor(26, 14, 30)              # #1A0E1E - dark desert purple (sky edge)

# Warm cream text tones
CREAM = "rgb(240,220,200)"                # Warm cream - primary text
CREAM_DIM = "rgb(200,175,155)"            # Dimmed cream
CREAM_MUTED = "rgb(130,105,90)"           # Muted warm gray
TEXT_DISABLED = "rgb(70,55,45)"

# Accent CSS strings
ORANGE_CSS = "rgb(255,140,66)"
ORANGE_DIM_CSS = "rgba(255,140,66,0.6)"

# Border tones - warm rust-brown
BORDER_DARK = "rgb(55,35,28)"
BORDER_MID = "rgb(80,50,40)"
BORDER_HOVER = "rgb(255,140,66)"

# Alpha variants of accent
ORANGE_90 = "rgba(255,140,66,0.9)"
ORANGE_60 = "rgba(255,140,66,0.6)"
ORANGE_35 = "rgba(255,140,66,0.35)"
ORANGE_20 = "rgba(255,140,66,0.2)"
ORANGE_12 = "rgba(255,140,66,0.12)"
ORANGE_8 = "rgba(255,140,66,0.08)"
WARM_WHITE_8 = "rgba(255,230,200,0.08)"


class DesertSunsetStyle(BaseStyle):
    name = "desert_sunset"
    font = "Futura"

    # Colors - warm sunset orange accent on dark desert brown
    accent = SUNSET_ORANGE
    accent_css = ORANGE_CSS
    text_primary = CREAM
    text_secondary = CREAM_DIM
    text_muted = CREAM_MUTED
    text_error = RED_ERROR
    text_link = ORANGE_90
    border_color = BORDER_MID
    border_dark = BORDER_DARK
    icon_color_dark = '#ffffff'
    icon_color_light = '#ffffff'
    icon_color_muted = '#8a6a55'  # Warm muted brown for SVG compatibility

    # Dropdown input fields - dark warm brown with cream text
    input_bg = '#241610'
    input_text = '#f0dcc8'

    # Slider - semi-transparent orange groove
    slider_groove = "rgba(255,140,66,0.30)"

    # Rotary knob - glass style with warm orange track
    knob_style = "glass"
    knob_body_dark = "#1e120e"
    knob_body_light = "#4a3028"
    knob_notch_style = "line"
    knob_tickmarks = False
    knob_glow = True
    knob_track_color = "#FF8C42"   # Sunset orange track
    knob_label_color = "#d4a880"   # Warm tan text

    # Waveform - orange with glow on dark panel with grid
    waveform_color = SUNSET_ORANGE
    waveform_glow = True
    waveform_glow_radius = 18
    waveform_glow_alpha = 180
    waveform_center_line = QColor(255, 140, 66, 30)
    waveform_panel = "dark"  # Dark panel with warm grid

    # Timer - LCD panel style with orange color
    timer_use_lcd = True
    timer_color = SUNSET_ORANGE

    # Transcription - dark desert panel with orange accents
    transcription_text = LIGHT_GRAY
    transcription_text_dimmed = CREAM_MUTED
    transcription_panel_bg = (
        "qlineargradient(x1:0, y1:0, x2:0, y2:1, "
        "stop:0 rgba(38,22,18,0.95), stop:1 rgba(26,14,20,0.95))"
    )
    transcription_panel_border = BORDER_DARK
    transcription_row_hover = ORANGE_8
    transcription_row_btn_bg = WARM_WHITE_8
    transcription_row_btn_hover = ORANGE_20
    transcription_row_btn_pressed = ORANGE_35

    # Chime editor - warm desert tones
    chime_grid_bg = QColor(30, 18, 14)       # Dark desert ground
    chime_grid_line = QColor(60, 40, 32)     # Warm rust border
    chime_cell_inactive = QColor(45, 28, 22) # Warm brown
    chime_cell_active = QColor(255, 140, 66) # Sunset orange
    chime_cell_highlight = QColor(255, 140, 66, 70)  # Orange glow
    chime_piano_white = QColor(230, 210, 190)  # Warm cream
    chime_piano_black = QColor(30, 18, 14)     # Dark desert
    chime_piano_label_white = QColor(80, 55, 40)    # Dark warm text on light
    chime_piano_label_black = QColor(210, 165, 120) # Warm tan text on dark

    def button_css(self):
        # Glass pill buttons with warm brown gradient and orange accents
        return (
            f"QPushButton {{ color: {CREAM_DIM}; "
            f"background: qlineargradient(x1:0, y1:0, x2:0, y2:1, "
            f"stop:0 rgba(75,48,38,0.9), stop:0.1 rgba(58,36,28,0.9), "
            f"stop:0.9 rgba(38,22,16,0.9), stop:1 rgba(32,18,14,0.9)); "
            f"border: 1px solid {BORDER_MID}; "
            f"border-radius: 4px; padding: 2px 4px; font-size: 10px; "
            f"font-family: {self.font}; text-align: left; }}"
            # Hover - warm glow
            f"QPushButton:hover {{ "
            f"background: qlineargradient(x1:0, y1:0, x2:0, y2:1, "
            f"stop:0 rgba(90,58,45,0.95), stop:0.1 rgba(72,45,35,0.95), "
            f"stop:0.9 rgba(52,32,24,0.95), stop:1 rgba(45,28,20,0.95)); "
            f"border: 1px solid {BORDER_HOVER}; }}"
            # Pressed - inverted gradient
            f"QPushButton:pressed {{ "
            f"background: qlineargradient(x1:0, y1:0, x2:0, y2:1, "
            f"stop:0 rgba(35,20,14,0.95), stop:0.1 rgba(40,25,18,0.95), "
            f"stop:0.9 rgba(55,35,26,0.95), stop:1 rgba(65,42,32,0.95)); "
            f"border: 1px solid {ORANGE_60}; }}"
            # Disabled
            f"QPushButton:disabled {{ color: {TEXT_DISABLED}; "
            f"background: rgba(30,18,14,0.3); border: 1px solid rgba(50,35,28,0.3); }}"
            # Checked - warm orange tint
            f"QPushButton:checked {{ "
            f"background: qlineargradient(x1:0, y1:0, x2:0, y2:1, "
            f"stop:0 rgba(160,80,30,0.5), stop:0.1 rgba(130,65,25,0.5), "
            f"stop:0.9 rgba(100,50,20,0.5), stop:1 rgba(85,42,18,0.5)); "
            f"border: 1px solid {ORANGE_60}; }}"
            f"QPushButton:checked:hover {{ "
            f"background: qlineargradient(x1:0, y1:0, x2:0, y2:1, "
            f"stop:0 rgba(180,90,35,0.6), stop:0.1 rgba(150,75,30,0.6), "
            f"stop:0.9 rgba(120,60,25,0.6), stop:1 rgba(105,52,22,0.6)); }}"
        )

    def menu_css(self):
        # Warm dark menu with orange accents
        return (
            f"QMenu {{ "
            f"background: qlineargradient(x1:0, y1:0, x2:0, y2:1, "
            f"stop:0 rgba(58,36,28,0.95), stop:1 rgba(35,20,16,0.95)); "
            f"color: {CREAM}; border: 1px solid rgba(100,60,45,0.6); "
            f"border-radius: 8px; padding: 6px; font-family: {self.font}; }}"
            "QMenu::item { padding: 6px 14px; border-radius: 5px; }"
            "QMenu::item:selected { "
            "background: qlineargradient(x1:0, y1:0, x2:0, y2:1, "
            "stop:0 rgba(255,140,66,0.3), stop:1 rgba(200,100,40,0.3)); }"
            f"QMenu::separator {{ height: 1px; background: rgba(255,180,130,0.2); margin: 4px 8px; }}"
        )

    def _scrollbar_vertical_css(self):
        return (
            "QScrollBar:vertical { width: 10px; background: transparent; margin: 2px; border: none; }"
            # Handle - warm orange-brown gradient
            "QScrollBar::handle:vertical { "
            "background: qlineargradient(x1:0, y1:0, x2:1, y2:0, "
            "stop:0 rgba(120,70,45,0.6), stop:0.5 rgba(150,85,55,0.7), stop:1 rgba(120,70,45,0.6)); "
            "border-radius: 5px; min-height: 30px; margin: 0px; }"
            # Hover - orange glow
            "QScrollBar::handle:vertical:hover { "
            "background: qlineargradient(x1:0, y1:0, x2:1, y2:0, "
            "stop:0 rgba(200,110,50,0.5), stop:0.5 rgba(255,140,66,0.6), stop:1 rgba(200,110,50,0.5)); }"
            "QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical { height: 0; }"
            "QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical { background: transparent; }"
        )

    def panel_bg_css(self):
        return (
            "background: qlineargradient(x1:0, y1:0, x2:0, y2:1, "
            "stop:0 rgba(48,30,22,0.95), stop:1 rgba(32,18,14,0.95)); "
            f"border: 1px solid {BORDER_MID}; "
            "border-radius: 8px;"
        )

    def panel_bg_flat_css(self):
        return (
            "background: qlineargradient(x1:0, y1:0, x2:0, y2:1, "
            "stop:0 rgba(38,22,16,0.95), stop:1 rgba(26,14,12,0.95)); "
            f"border: 1px solid {BORDER_DARK}; "
            "border-radius: 8px;"
        )

    def paint_window(self, painter, rect, width, height, focused=True):
        """Paint desert sunset with sun glow, horizon bands, and purple sky.

        Full sunset composition: dark purple sky at top, warm orange horizon
        glow at ~40% height with a radial sun, fading to dark desert ground.
        """
        radius = self.corner_radius
        alpha_mult = 1.0 if focused else 0.85

        # Clip to rounded rect
        path = QPainterPath()
        path.addRoundedRect(QRectF(rect), radius, radius)
        painter.setClipPath(path)

        # Layer 1: Sky-to-ground gradient
        grad = QLinearGradient(0, rect.top(), 0, rect.bottom())
        grad.setColorAt(0.0, QColor(28, 12, 35, int(255 * alpha_mult)))    # Deep indigo sky
        grad.setColorAt(0.2, QColor(45, 18, 38, int(255 * alpha_mult)))    # Purple twilight
        grad.setColorAt(0.35, QColor(65, 25, 30, int(255 * alpha_mult)))   # Rose transition
        grad.setColorAt(0.45, QColor(80, 35, 22, int(255 * alpha_mult)))   # Warm orange-brown
        grad.setColorAt(0.55, QColor(55, 28, 18, int(255 * alpha_mult)))   # Below horizon
        grad.setColorAt(0.8, QColor(34, 20, 15, int(255 * alpha_mult)))    # Dark ground
        grad.setColorAt(1.0, QColor(24, 12, 10, int(255 * alpha_mult)))    # Darkest
        painter.setBrush(QBrush(grad))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawRect(rect)

        # Layer 2: Radial sun glow at the horizon, slightly right of center
        sun_x = rect.left() + width * 0.6
        sun_y = rect.top() + height * 0.42
        sun_r = max(width, height) * 0.45
        sun = QRadialGradient(QPointF(sun_x, sun_y), sun_r)
        sun.setColorAt(0, QColor(255, 180, 80, int(35 * alpha_mult)))
        sun.setColorAt(0.15, QColor(255, 140, 50, int(25 * alpha_mult)))
        sun.setColorAt(0.3, QColor(255, 100, 40, int(15 * alpha_mult)))
        sun.setColorAt(0.5, QColor(200, 60, 40, int(8 * alpha_mult)))
        sun.setColorAt(1, QColor(100, 30, 30, 0))
        painter.setBrush(QBrush(sun))
        painter.drawRect(rect)

        # Layer 3: Thin bright horizon line at 43%
        horizon_y = rect.top() + int(height * 0.43)
        horizon_line = QLinearGradient(rect.left(), horizon_y - 3, rect.left(), horizon_y + 3)
        horizon_line.setColorAt(0, QColor(255, 160, 60, 0))
        horizon_line.setColorAt(0.5, QColor(255, 160, 60, int(20 * alpha_mult)))
        horizon_line.setColorAt(1, QColor(255, 160, 60, 0))
        painter.setBrush(QBrush(horizon_line))
        painter.drawRect(rect.left(), horizon_y - 3, width, 6)

        # Layer 4: Purple sky darkening at very top
        sky_dark = QLinearGradient(0, rect.top(), 0, rect.top() + int(height * 0.15))
        sky_dark.setColorAt(0, QColor(15, 5, 25, int(40 * alpha_mult)))
        sky_dark.setColorAt(1, QColor(0, 0, 0, 0))
        painter.setBrush(QBrush(sky_dark))
        painter.drawRect(rect)

        painter.setClipping(False)

        # Border and focus glow
        painter.setBrush(Qt.BrushStyle.NoBrush)
        if focused:
            for i in range(3):
                glow_alpha = int(35 - i * 10)
                painter.setPen(QPen(QColor(255, 140, 66, glow_alpha), 3 + i * 2))
                painter.drawRoundedRect(rect.adjusted(-i, -i, i, i), radius + i, radius + i)
            painter.setPen(QPen(self.accent, 2))
            painter.drawRoundedRect(rect, radius, radius)
        else:
            painter.setPen(QPen(QColor(80, 50, 40, 150), 1))
            painter.drawRoundedRect(rect, radius, radius)

    def paint_waveform_panel(self, painter, rect, w, h, cy):
        """Dark desert waveform panel with warm-toned grid.

        Deep warm brown background with subtle orange grid lines,
        evoking the measured geometry of desert horizons.
        """
        # Dark warm gradient background
        panel_grad = QLinearGradient(0, 0, 0, h)
        panel_grad.setColorAt(0.0, QColor(38, 22, 16, 240))
        panel_grad.setColorAt(0.5, QColor(30, 18, 14, 240))
        panel_grad.setColorAt(1.0, QColor(24, 14, 12, 240))
        painter.setBrush(QBrush(panel_grad))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawRoundedRect(rect, 8, 8)

        # Subtle warm orange grid
        painter.setPen(QPen(QColor(255, 140, 66, 15), 1))
        for i in range(1, 4):
            y = int(h * i / 4)
            painter.drawLine(0, y, w, y)
        num_sections = 8
        for i in range(1, num_sections):
            painter.drawLine(int(w * i / num_sections), 0, int(w * i / num_sections), h)

        # Subtle warm border
        painter.setBrush(Qt.BrushStyle.NoBrush)
        painter.setPen(QPen(QColor(70, 45, 35, 150), 1))
        painter.drawRoundedRect(rect, 8, 8)
