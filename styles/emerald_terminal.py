"""Emerald Terminal style - sleek green-on-dark terminal aesthetic.

Modern hacker terminal with emerald green accents on near-black backgrounds.
Differentiates from CRT Terminal by being clean, minimal, and modern rather
than retro phosphor. Think Matrix-inspired but refined -- no scanlines, no
phosphor dots, no CRT curvature. Just crisp emerald on dark with subtle glow.
"""

from PyQt6.QtCore import Qt, QPointF, QRectF
from PyQt6.QtGui import QColor, QLinearGradient, QRadialGradient, QBrush, QPen, QPainterPath

from .base import BaseStyle, RED_ERROR, LIGHT_GRAY


# === Emerald palette ===
# Primary emerald accent -- bright, modern green (not retro phosphor green)
EMERALD = QColor(0, 255, 136)               # #00FF88
EMERALD_CSS = "rgb(0,255,136)"

# Text colors -- desaturated emerald for comfortable reading
TEXT_BRIGHT = "rgba(180,255,210,0.95)"       # Near-white with green tint
TEXT_MID = "rgba(120,220,160,0.85)"          # Readable mid-tone
TEXT_MUTED = "rgba(60,140,90,0.6)"           # Dim labels
TEXT_DISABLED = "rgba(35,80,50,0.4)"         # Nearly invisible

# Background tones -- near-black with green undertone
BG_DARKEST = "rgb(8,12,10)"                 # Deepest background
BG_DARK = "rgb(14,20,16)"                   # Standard dark
BG_MID = "rgb(22,30,25)"                    # Elevated surfaces
BG_LIGHT = "rgb(30,42,34)"                  # Hover/active surfaces

# Border colors
BORDER_DIM = "rgb(25,40,30)"                # Subtle border
BORDER_MID = "rgb(35,60,42)"               # Standard border
BORDER_BRIGHT = "rgb(0,200,110)"            # Focus/hover border

# Emerald with alpha variants
EMERALD_90 = "rgba(0,255,136,0.9)"
EMERALD_60 = "rgba(0,255,136,0.6)"
EMERALD_35 = "rgba(0,255,136,0.35)"
EMERALD_20 = "rgba(0,255,136,0.2)"
EMERALD_12 = "rgba(0,255,136,0.12)"
EMERALD_8 = "rgba(0,255,136,0.08)"
EMERALD_5 = "rgba(0,255,136,0.05)"

# Panel borders -- solid for crisp outlines
PANEL_BORDER = "rgb(30,50,38)"
PANEL_BORDER_DARK = "rgb(20,35,26)"


class EmeraldTerminalStyle(BaseStyle):
    name = "emerald_terminal"
    font = "Menlo"
    corner_radius = 8

    # Accent -- emerald green
    accent = EMERALD
    accent_css = EMERALD_CSS
    text_primary = TEXT_BRIGHT
    text_secondary = TEXT_MID
    text_muted = TEXT_MUTED
    text_error = RED_ERROR
    text_link = EMERALD_90
    border_color = BORDER_MID
    border_dark = BORDER_DIM
    icon_color_dark = '#00ff88'
    icon_color_light = '#00ff88'
    icon_color_muted = '#2a6b45'

    # Dropdown input fields -- dark with emerald text
    input_bg = '#0a100c'
    input_text = '#b0ffd2'

    # Slider -- emerald groove on dark
    slider_groove = "rgba(0,255,136,0.25)"
    slider_handle = EMERALD_CSS
    slider_fill = "rgb(0,200,110)"

    # Rotary knob -- cyber style with emerald glow
    knob_style = "cyber"
    knob_body_dark = "#080e0a"
    knob_body_light = "#1a2e22"
    knob_notch_style = "line"
    knob_tickmarks = False
    knob_glow = True
    knob_track_color = "#00ff88"
    knob_label_color = "#80ffbb"

    # Waveform -- emerald with glow, dark panel with grid
    waveform_color = EMERALD
    waveform_glow = True
    waveform_glow_radius = 20
    waveform_glow_alpha = 190
    waveform_center_line = QColor(0, 255, 136, 30)
    waveform_panel = "dark"

    # Timer -- LCD style with emerald color
    timer_use_lcd = True
    timer_color = EMERALD
    timer_font_size = 28
    timer_panel_size = (160, 40)

    # Transcription panel
    transcription_text = LIGHT_GRAY
    transcription_text_dimmed = "rgba(0,200,110,0.7)"
    transcription_panel_bg = (
        "qlineargradient(x1:0, y1:0, x2:0, y2:1, "
        "stop:0 rgba(14,20,16,0.95), stop:1 rgba(8,12,10,0.95))"
    )
    transcription_panel_border = PANEL_BORDER_DARK
    transcription_row_hover = EMERALD_5
    transcription_row_btn_bg = EMERALD_8
    transcription_row_btn_hover = EMERALD_20
    transcription_row_btn_pressed = EMERALD_35

    # Chime editor -- emerald on dark
    chime_grid_bg = QColor(10, 16, 12)
    chime_grid_line = QColor(25, 45, 32)
    chime_cell_inactive = QColor(16, 24, 18)
    chime_cell_active = EMERALD
    chime_cell_highlight = QColor(0, 255, 136, 70)
    chime_piano_white = QColor(140, 220, 170)
    chime_piano_black = QColor(8, 14, 10)
    chime_piano_label_white = QColor(20, 50, 32)
    chime_piano_label_black = QColor(0, 255, 136)

    def button_css(self):
        # Clean dark buttons with emerald accents
        return (
            # Normal -- dark with subtle emerald border
            f"QPushButton {{ color: {TEXT_MID}; "
            f"background: qlineargradient(x1:0, y1:0, x2:0, y2:1, "
            f"stop:0 rgba(22,32,26,0.9), stop:0.1 rgba(18,26,20,0.9), "
            f"stop:0.9 rgba(12,18,14,0.9), stop:1 rgba(10,16,12,0.9)); "
            f"border: 1px solid {BORDER_MID}; "
            f"border-radius: 4px; padding: 2px 4px; "
            f"font-size: 10px; font-family: {self.font}; text-align: left; }}"
            # Hover -- emerald border brightens
            f"QPushButton:hover {{ color: {TEXT_BRIGHT}; "
            f"background: qlineargradient(x1:0, y1:0, x2:0, y2:1, "
            f"stop:0 rgba(28,42,32,0.95), stop:0.1 rgba(24,36,28,0.95), "
            f"stop:0.9 rgba(18,28,22,0.95), stop:1 rgba(14,22,16,0.95)); "
            f"border: 1px solid {BORDER_BRIGHT}; }}"
            # Pressed -- inset
            f"QPushButton:pressed {{ color: {EMERALD_CSS}; "
            f"background: qlineargradient(x1:0, y1:0, x2:0, y2:1, "
            f"stop:0 rgba(10,16,12,0.95), stop:0.1 rgba(12,18,14,0.95), "
            f"stop:0.9 rgba(18,26,20,0.95), stop:1 rgba(22,30,24,0.95)); "
            f"border: 1px solid {EMERALD_60}; }}"
            # Disabled
            f"QPushButton:disabled {{ color: {TEXT_DISABLED}; "
            f"background: rgba(10,14,12,0.3); "
            f"border: 1px solid rgba(20,30,24,0.3); }}"
            # Checked -- emerald tinted
            f"QPushButton:checked {{ color: rgba(200,255,220,0.95); "
            f"background: qlineargradient(x1:0, y1:0, x2:0, y2:1, "
            f"stop:0 rgba(0,100,55,0.45), stop:0.1 rgba(0,80,44,0.45), "
            f"stop:0.9 rgba(0,60,33,0.45), stop:1 rgba(0,50,28,0.45)); "
            f"border: 1px solid {EMERALD_60}; }}"
            # Checked hover
            f"QPushButton:checked:hover {{ "
            f"background: qlineargradient(x1:0, y1:0, x2:0, y2:1, "
            f"stop:0 rgba(0,120,66,0.55), stop:0.1 rgba(0,100,55,0.55), "
            f"stop:0.9 rgba(0,80,44,0.55), stop:1 rgba(0,65,36,0.55)); }}"
        )

    def menu_css(self):
        # Dark menu with emerald highlights
        return (
            f"QMenu {{ "
            f"background: qlineargradient(x1:0, y1:0, x2:0, y2:1, "
            f"stop:0 rgba(18,26,20,0.95), stop:1 rgba(10,16,12,0.95)); "
            f"color: {TEXT_BRIGHT}; "
            f"border: 1px solid {BORDER_MID}; "
            f"border-radius: 6px; padding: 6px; font-family: {self.font}; }}"
            "QMenu::item { padding: 6px 14px; border-radius: 4px; }"
            "QMenu::item:selected { "
            "background: qlineargradient(x1:0, y1:0, x2:0, y2:1, "
            "stop:0 rgba(0,255,136,0.18), stop:1 rgba(0,200,110,0.18)); }"
            f"QMenu::separator {{ height: 1px; background: {BORDER_MID}; margin: 4px 8px; }}"
        )

    def _scrollbar_vertical_css(self):
        return (
            "QScrollBar:vertical { width: 10px; background: transparent; margin: 2px; border: none; }"
            "QScrollBar::handle:vertical { "
            "background: qlineargradient(x1:0, y1:0, x2:1, y2:0, "
            "stop:0 rgba(0,120,66,0.4), stop:0.5 rgba(0,160,88,0.55), stop:1 rgba(0,120,66,0.4)); "
            "border-radius: 5px; min-height: 30px; margin: 0px; }"
            "QScrollBar::handle:vertical:hover { "
            "background: qlineargradient(x1:0, y1:0, x2:1, y2:0, "
            "stop:0 rgba(0,200,110,0.5), stop:0.5 rgba(0,255,136,0.6), stop:1 rgba(0,200,110,0.5)); }"
            "QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical { height: 0; }"
            "QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical { background: transparent; }"
        )

    def panel_bg_css(self):
        return (
            "background: qlineargradient(x1:0, y1:0, x2:0, y2:1, "
            "stop:0 rgba(18,26,20,0.95), stop:1 rgba(10,16,12,0.95)); "
            f"border: 1px solid {PANEL_BORDER}; "
            "border-radius: 8px;"
        )

    def panel_bg_flat_css(self):
        return (
            "background: qlineargradient(x1:0, y1:0, x2:0, y2:1, "
            "stop:0 rgba(14,20,16,0.95), stop:1 rgba(8,12,10,0.95)); "
            f"border: 1px solid {PANEL_BORDER_DARK}; "
            "border-radius: 8px;"
        )

    def paint_window(self, painter, rect, width, height, focused=True):
        """Paint terminal background with scanlines and corner vignette."""
        radius = self.corner_radius
        alpha_mult = 1.0 if focused else 0.85

        # Clip to window
        clip = QPainterPath()
        clip.addRoundedRect(QRectF(rect), radius, radius)
        painter.setClipPath(clip)

        # Main gradient: near-black with green undertone
        grad = QLinearGradient(0, rect.top(), 0, rect.bottom())
        grad.setColorAt(0, QColor(16, 22, 18, int(255 * alpha_mult)))
        grad.setColorAt(0.15, QColor(12, 18, 14, int(255 * alpha_mult)))
        grad.setColorAt(0.85, QColor(8, 13, 10, int(255 * alpha_mult)))
        grad.setColorAt(1, QColor(6, 10, 8, int(255 * alpha_mult)))
        painter.setBrush(QBrush(grad))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawRect(rect)

        # Scanlines: subtle horizontal lines every 3px
        scanline_spacing = 3
        scanline_pen = QPen(QColor(0, 0, 0, int(20 * alpha_mult)), 1)
        painter.setPen(scanline_pen)
        y = rect.top()
        while y < rect.bottom():
            painter.drawLine(rect.left(), y, rect.right(), y)
            y += scanline_spacing

        # Vignette: dark radial gradient from corners inward
        cx = rect.left() + width / 2
        cy_pos = rect.top() + height / 2
        vignette_r = max(width, height) * 0.75
        vignette = QRadialGradient(QPointF(cx, cy_pos), vignette_r)
        vignette.setColorAt(0, QColor(0, 0, 0, 0))
        vignette.setColorAt(0.6, QColor(0, 0, 0, 0))
        vignette.setColorAt(0.85, QColor(0, 0, 0, int(40 * alpha_mult)))
        vignette.setColorAt(1, QColor(0, 0, 0, int(80 * alpha_mult)))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(QBrush(vignette))
        painter.drawRect(rect)

        # Faint emerald glow at center (screen phosphor bloom)
        bloom = QRadialGradient(QPointF(cx, cy_pos), max(width, height) * 0.5)
        bloom.setColorAt(0, QColor(0, 255, 136, int(8 * alpha_mult)))
        bloom.setColorAt(0.5, QColor(0, 200, 100, int(4 * alpha_mult)))
        bloom.setColorAt(1, QColor(0, 0, 0, 0))
        painter.setBrush(QBrush(bloom))
        painter.drawRect(rect)

        painter.setClipping(False)

        # Border
        painter.setBrush(Qt.BrushStyle.NoBrush)
        painter.setPen(QPen(QColor(25, 45, 32, int(180 * alpha_mult)), 1))
        painter.drawRoundedRect(rect, radius, radius)

        # Focus glow
        if focused:
            for i in range(3):
                glow_alpha = int(35 - i * 10)
                painter.setPen(QPen(QColor(0, 255, 136, glow_alpha), 3 + i * 2))
                painter.drawRoundedRect(rect.adjusted(-i, -i, i, i), radius + i, radius + i)
            painter.setPen(QPen(self.accent, 2))
            painter.drawRoundedRect(rect, radius, radius)

    def paint_waveform_panel(self, painter, rect, w, h, cy):
        """Dark gradient panel with emerald grid lines."""
        # Dark gradient background
        panel_grad = QLinearGradient(0, 0, 0, h)
        panel_grad.setColorAt(0, QColor(14, 20, 16, 240))
        panel_grad.setColorAt(0.5, QColor(10, 15, 12, 240))
        panel_grad.setColorAt(1, QColor(7, 11, 9, 240))
        painter.setBrush(QBrush(panel_grad))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawRoundedRect(rect, 8, 8)

        # Emerald grid lines
        painter.setPen(QPen(QColor(0, 255, 136, 15), 1))
        for i in range(1, 4):
            y = int(h * i / 4)
            painter.drawLine(0, y, w, y)
        num_sections = 8
        for i in range(1, num_sections):
            painter.drawLine(int(w * i / num_sections), 0, int(w * i / num_sections), h)

        # Subtle border
        painter.setBrush(Qt.BrushStyle.NoBrush)
        painter.setPen(QPen(QColor(25, 45, 32, 150), 1))
        painter.drawRoundedRect(rect, 8, 8)
