"""Windows Vista Aero Glass style - dark dramatic translucent glass (2006-2009).

Vista's Aero Glass was darker and more dramatic than Windows 7's lighter, airier
glass. Deep blue-black translucency with strong frosted blur, glossy pill buttons
with bright white shine lines, and the characteristic blue-purple tinted glass.

Color references:
  - Vista brand blue: #29599B (41, 89, 155)
  - Vista default ColorizationColor: 0xC40078D7 (deep blue with ~77% alpha)
  - DWM glass: dark translucent panels with blue tint over blurred background
  - Vista title bar: darker gradient glass, not the airy white of Win7
  - Buttons: blue glow on hover (min/max), red glow for close

Key differences from frutiger_aero (Win7):
  - Much darker overall - near-black glass vs Win7's light blue-white
  - More dramatic tinting and opacity
  - No aquatic bubbles - pure glass/frost aesthetic
  - Stronger specular highlights on top edge (sharper gloss)
  - LCD-style timer (Vista's digital clock had this feel)
"""

from PyQt6.QtCore import Qt, QPointF
from PyQt6.QtGui import QColor, QLinearGradient, QRadialGradient, QBrush, QPen

from .base import BaseStyle


# ── Vista Aero color palette ────────────────────────────────────────────────
# Drawn from Vista's deep blue-black glass, distinctly darker than Win7's airy pastels.

# Vista glass blue - the deep blue-purple tint of the default DWM glass
VISTA_BLUE = QColor(41, 89, 155)          # #29599B - Vista brand blue
VISTA_BLUE_LIGHT = QColor(0, 120, 215)    # #0078D7 - default ColorizationColor RGB
VISTA_BLUE_GLOW = QColor(80, 140, 220)    # Blue hover glow
VISTA_BLUE_BRIGHT = QColor(100, 170, 255) # Bright accent for active elements

# Glass panel tones - dark translucent blue-black (the hallmark Vista look)
GLASS_DARK = "rgba(15, 20, 35, 0.92)"        # Near-black glass base
GLASS_MID = "rgba(25, 35, 55, 0.88)"         # Dark blue-gray glass
GLASS_LIGHT = "rgba(40, 55, 80, 0.85)"       # Lighter glass edge
GLASS_HIGHLIGHT = "rgba(120, 160, 220, 0.25)" # Top-edge specular shine

# Text on dark glass
TEXT_WHITE = "rgba(255, 255, 255, 0.95)"
TEXT_WHITE_DIM = "rgba(255, 255, 255, 0.72)"
TEXT_WHITE_MUTED = "rgba(255, 255, 255, 0.45)"
TEXT_WHITE_FAINT = "rgba(255, 255, 255, 0.22)"
TEXT_DISABLED = "rgba(255, 255, 255, 0.18)"

# Vista accent blues for interactive elements
ACCENT_BLUE = "rgba(0, 120, 215, 0.9)"        # Default blue
ACCENT_BLUE_DIM = "rgba(0, 120, 215, 0.6)"
ACCENT_BLUE_GLOW = "rgba(80, 150, 230, 0.35)"
ACCENT_BLUE_FAINT = "rgba(60, 120, 200, 0.12)"

# Glass borders - crisp outlines characteristic of Vista chrome
BORDER_GLASS = "rgb(60, 75, 105)"         # Standard glass border
BORDER_GLASS_DARK = "rgb(35, 45, 70)"     # Deeper border
BORDER_GLASS_HOVER = "rgb(80, 140, 220)"  # Hover highlight
BORDER_GLASS_BRIGHT = "rgb(100, 170, 255)" # Active/focus

# Panel borders
PANEL_BORDER = "rgb(50, 60, 85)"
PANEL_BORDER_DARK = "rgb(35, 45, 65)"


class VistaAeroStyle(BaseStyle):
    name = "vista_aero"
    font = "Segoe UI"  # Vista introduced Segoe UI as the system font

    # ── Core colors ──────────────────────────────────────────────────────
    accent = VISTA_BLUE
    accent_css = "rgb(41, 89, 155)"
    text_primary = TEXT_WHITE
    text_secondary = TEXT_WHITE_DIM
    text_muted = TEXT_WHITE_MUTED
    text_error = "rgb(255, 90, 90)"
    text_link = "rgba(100, 170, 255, 0.95)"
    border_color = BORDER_GLASS
    border_dark = BORDER_GLASS_DARK
    icon_color_dark = '#ffffff'
    icon_color_light = '#ffffff'
    icon_color_muted = '#8090aa'

    # ── Input fields ─────────────────────────────────────────────────────
    input_bg = '#1a2240'
    input_text = '#c8d8f0'

    # ── Slider ───────────────────────────────────────────────────────────
    slider_groove = "rgba(0, 120, 215, 0.30)"

    # ── Rotary knob - glass style with Vista blue ────────────────────────
    knob_style = "glass"
    knob_body_dark = "#141e30"
    knob_body_light = "#2a3c5c"
    knob_notch_style = "line"
    knob_tickmarks = False
    knob_glow = True
    knob_track_color = "#0078d7"
    knob_label_color = "#80a8d0"

    # ── Waveform ─────────────────────────────────────────────────────────
    waveform_color = VISTA_BLUE_LIGHT
    waveform_glow = True
    waveform_glow_radius = 20
    waveform_glow_alpha = 180
    waveform_center_line = QColor(0, 120, 215, 30)
    waveform_panel = "dark"
    waveform_bubbles = False  # No bubbles - pure glass, not aquatic

    # ── Timer - LCD style ────────────────────────────────────────────────
    timer_use_lcd = True
    timer_color = VISTA_BLUE_LIGHT

    # ── Transcription ────────────────────────────────────────────────────
    transcription_text = TEXT_WHITE_DIM
    transcription_text_dimmed = "rgba(80, 130, 190, 0.7)"
    transcription_panel_bg = (
        "qlineargradient(x1:0, y1:0, x2:0, y2:1, "
        "stop:0 rgba(20, 28, 48, 0.95), stop:1 rgba(12, 16, 30, 0.95))"
    )
    transcription_panel_border = PANEL_BORDER_DARK
    transcription_row_hover = ACCENT_BLUE_FAINT
    transcription_row_btn_bg = "rgba(255, 255, 255, 0.06)"
    transcription_row_btn_hover = "rgba(0, 120, 215, 0.20)"
    transcription_row_btn_pressed = "rgba(0, 120, 215, 0.40)"

    # ── Chime editor - deep blue glass ───────────────────────────────────
    chime_grid_bg = QColor(14, 18, 32)
    chime_grid_line = QColor(40, 55, 80)
    chime_cell_inactive = QColor(22, 30, 50)
    chime_cell_active = QColor(0, 120, 215)
    chime_cell_highlight = QColor(0, 120, 215, 80)
    chime_piano_white = QColor(180, 200, 225)
    chime_piano_black = QColor(18, 24, 40)
    chime_piano_label_white = QColor(40, 55, 85)
    chime_piano_label_black = QColor(130, 170, 220)

    # ── CSS methods ──────────────────────────────────────────────────────

    def button_css(self):
        """Vista glossy pill buttons - dark glass with bright white shine line on top."""
        return (
            # Normal state: dark glass pill with specular highlight
            f"QPushButton {{ "
            f"color: {TEXT_WHITE_DIM}; "
            f"background: qlineargradient(x1:0, y1:0, x2:0, y2:1, "
            f"stop:0 rgba(70, 85, 120, 0.92), "
            f"stop:0.05 rgba(55, 70, 100, 0.90), "
            f"stop:0.5 rgba(30, 40, 65, 0.88), "
            f"stop:1 rgba(18, 24, 42, 0.92)); "
            f"border: 1px solid {BORDER_GLASS}; "
            f"border-top: 1px solid rgba(140, 170, 220, 0.5); "
            f"border-radius: 4px; padding: 2px 4px; "
            f"font-size: 10px; font-family: {self.font}; text-align: left; }}"

            # Hover: blue glow (Vista's characteristic button hover)
            f"QPushButton:hover {{ "
            f"background: qlineargradient(x1:0, y1:0, x2:0, y2:1, "
            f"stop:0 rgba(80, 110, 160, 0.95), "
            f"stop:0.05 rgba(65, 95, 145, 0.92), "
            f"stop:0.5 rgba(40, 60, 100, 0.90), "
            f"stop:1 rgba(25, 35, 60, 0.92)); "
            f"border: 1px solid {BORDER_GLASS_HOVER}; "
            f"border-top: 1px solid rgba(160, 200, 255, 0.6); }}"

            # Pressed: inverted gradient (top darker)
            f"QPushButton:pressed {{ "
            f"background: qlineargradient(x1:0, y1:0, x2:0, y2:1, "
            f"stop:0 rgba(15, 22, 40, 0.95), "
            f"stop:0.5 rgba(25, 38, 65, 0.92), "
            f"stop:1 rgba(40, 60, 95, 0.90)); "
            f"border: 1px solid {ACCENT_BLUE_DIM}; "
            f"border-top: 1px solid rgba(100, 140, 200, 0.3); }}"

            # Disabled
            f"QPushButton:disabled {{ "
            f"color: {TEXT_DISABLED}; "
            f"background: rgba(25, 30, 45, 0.4); "
            f"border: 1px solid rgba(50, 60, 80, 0.3); }}"

            # Checked: active blue glow state
            f"QPushButton:checked {{ "
            f"background: qlineargradient(x1:0, y1:0, x2:0, y2:1, "
            f"stop:0 rgba(30, 80, 150, 0.6), "
            f"stop:0.05 rgba(25, 65, 130, 0.55), "
            f"stop:0.5 rgba(15, 50, 110, 0.5), "
            f"stop:1 rgba(10, 35, 80, 0.55)); "
            f"border: 1px solid {ACCENT_BLUE_DIM}; "
            f"border-top: 1px solid rgba(120, 180, 255, 0.5); }}"

            # Checked + hover
            f"QPushButton:checked:hover {{ "
            f"background: qlineargradient(x1:0, y1:0, x2:0, y2:1, "
            f"stop:0 rgba(40, 95, 170, 0.65), "
            f"stop:0.05 rgba(35, 80, 150, 0.60), "
            f"stop:0.5 rgba(25, 65, 130, 0.55), "
            f"stop:1 rgba(15, 45, 100, 0.60)); "
            f"border-top: 1px solid rgba(140, 200, 255, 0.6); }}"
        )

    def menu_css(self):
        """Dark frosted glass context menu with Vista blue highlight."""
        return (
            f"QMenu {{ "
            f"background: qlineargradient(x1:0, y1:0, x2:0, y2:1, "
            f"stop:0 rgba(30, 40, 60, 0.96), stop:1 rgba(15, 20, 35, 0.96)); "
            f"color: white; "
            f"border: 1px solid {BORDER_GLASS}; "
            f"border-radius: 6px; padding: 6px; font-family: {self.font}; }}"

            "QMenu::item { padding: 6px 14px; border-radius: 4px; }"

            "QMenu::item:selected { "
            "background: qlineargradient(x1:0, y1:0, x2:0, y2:1, "
            "stop:0 rgba(0, 120, 215, 0.45), stop:1 rgba(0, 80, 160, 0.45)); }"

            f"QMenu::separator {{ height: 1px; "
            f"background: rgba(80, 100, 140, 0.4); margin: 4px 8px; }}"
        )

    def _scrollbar_vertical_css(self):
        """Dark glass scrollbar with blue-tinted handle."""
        return (
            "QScrollBar:vertical { width: 10px; background: transparent; "
            "margin: 2px; border: none; }"

            "QScrollBar::handle:vertical { "
            "background: qlineargradient(x1:0, y1:0, x2:1, y2:0, "
            "stop:0 rgba(50, 65, 100, 0.6), "
            "stop:0.5 rgba(65, 85, 125, 0.7), "
            "stop:1 rgba(50, 65, 100, 0.6)); "
            "border-radius: 5px; min-height: 30px; margin: 0px; }"

            "QScrollBar::handle:vertical:hover { "
            "background: qlineargradient(x1:0, y1:0, x2:1, y2:0, "
            "stop:0 rgba(60, 110, 180, 0.55), "
            "stop:0.5 rgba(80, 140, 220, 0.65), "
            "stop:1 rgba(60, 110, 180, 0.55)); }"

            "QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical "
            "{ height: 0; }"
            "QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical "
            "{ background: transparent; }"
        )

    def panel_bg_css(self):
        """Dark blue-glass panel background."""
        return (
            "background: qlineargradient(x1:0, y1:0, x2:0, y2:1, "
            "stop:0 rgba(28, 38, 60, 0.94), stop:1 rgba(14, 18, 32, 0.94)); "
            f"border: 1px solid {PANEL_BORDER}; "
            "border-radius: 8px;"
        )

    def panel_bg_flat_css(self):
        """Flatter dark glass panel (recessed look)."""
        return (
            "background: qlineargradient(x1:0, y1:0, x2:0, y2:1, "
            "stop:0 rgba(20, 28, 48, 0.95), stop:1 rgba(10, 14, 26, 0.95)); "
            f"border: 1px solid {PANEL_BORDER_DARK}; "
            "border-radius: 8px;"
        )

    # ── Paint methods ────────────────────────────────────────────────────

    def paint_window(self, painter, rect, width, height, focused=True):
        """Paint Vista Aero dark glass background with frosted gradient.

        Vista's glass was distinctly darker than Win7 - deep blue-black with
        a strong frosted translucency. The top edge has a bright specular
        highlight (the "shine line"), and the focused state adds a blue glow
        border instead of Win7's cyan.
        """
        radius = self.corner_radius
        alpha_mult = 1.0 if focused else 0.82

        # Main gradient: deep blue-black glass (darker than dark_gradient,
        # distinctly blue-tinted unlike the neutral gray of dark_gradient)
        grad = QLinearGradient(0, rect.top(), 0, rect.bottom())
        grad.setColorAt(0.0, QColor(35, 45, 70, int(240 * alpha_mult)))
        grad.setColorAt(0.08, QColor(25, 35, 58, int(235 * alpha_mult)))
        grad.setColorAt(0.4, QColor(18, 24, 42, int(230 * alpha_mult)))
        grad.setColorAt(0.85, QColor(12, 16, 30, int(235 * alpha_mult)))
        grad.setColorAt(1.0, QColor(8, 10, 22, int(240 * alpha_mult)))
        painter.setBrush(QBrush(grad))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawRoundedRect(rect, radius, radius)

        # Specular shine line at top (Vista's signature bright frost edge).
        # Sharper and brighter than Win7's soft glow.
        inner = rect.adjusted(2, 1, -2, -1)
        shine = QLinearGradient(0, rect.top(), 0, rect.top() + 28)
        shine.setColorAt(0.0, QColor(180, 210, 255, int(55 * alpha_mult)))
        shine.setColorAt(0.3, QColor(120, 160, 220, int(28 * alpha_mult)))
        shine.setColorAt(1.0, QColor(80, 120, 180, 0))
        painter.setBrush(QBrush(shine))
        painter.drawRoundedRect(inner, radius - 1, radius - 1)

        # Subtle inner shadow at very top (depth/inset bevel)
        shadow = QLinearGradient(0, rect.top(), 0, rect.top() + 6)
        shadow.setColorAt(0.0, QColor(0, 0, 0, int(50 * alpha_mult)))
        shadow.setColorAt(1.0, QColor(0, 0, 0, 0))
        painter.setBrush(QBrush(shadow))
        painter.drawRoundedRect(
            rect.adjusted(0, 0, 0, -rect.height() + 10), radius, radius
        )

        # Frosted noise simulation: a faint mid-band to suggest blur depth
        frost_band = QLinearGradient(0, rect.top() + height * 0.3,
                                     0, rect.top() + height * 0.5)
        frost_band.setColorAt(0.0, QColor(60, 80, 120, int(8 * alpha_mult)))
        frost_band.setColorAt(0.5, QColor(80, 100, 150, int(12 * alpha_mult)))
        frost_band.setColorAt(1.0, QColor(60, 80, 120, int(8 * alpha_mult)))
        painter.setBrush(QBrush(frost_band))
        painter.drawRoundedRect(rect, radius, radius)

        # Glass border - crisp dark blue edge
        painter.setBrush(Qt.BrushStyle.NoBrush)
        painter.setPen(QPen(QColor(50, 65, 100, int(200 * alpha_mult)), 1))
        painter.drawRoundedRect(rect, radius, radius)

        # Focus: Vista blue glow (not cyan like dark_gradient)
        if focused:
            for i in range(3):
                glow_alpha = int(35 - i * 10)
                painter.setPen(QPen(
                    QColor(41, 89, 155, glow_alpha), 3 + i * 2
                ))
                painter.drawRoundedRect(
                    rect.adjusted(-i, -i, i, i), radius + i, radius + i
                )
            # Inner accent border
            painter.setPen(QPen(QColor(41, 89, 155), 1.5))
            painter.drawRoundedRect(rect, radius, radius)

    def paint_waveform_panel(self, painter, rect, w, h, cy):
        """Dark frosted glass waveform panel with Vista blue grid.

        Deeper and more opaque than Win7's light glass panel, with a subtle
        blue-tinted grid and no decorative bubbles.
        """
        # Deep blue-black glass background
        panel_grad = QLinearGradient(0, 0, 0, h)
        panel_grad.setColorAt(0.0, QColor(22, 30, 50, 240))
        panel_grad.setColorAt(0.5, QColor(16, 22, 38, 235))
        panel_grad.setColorAt(1.0, QColor(10, 14, 26, 240))
        painter.setBrush(QBrush(panel_grad))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawRoundedRect(rect, 8, 8)

        # Top-edge specular highlight (frosted glass shine)
        shine = QLinearGradient(0, 0, 0, h * 0.2)
        shine.setColorAt(0.0, QColor(100, 140, 200, 30))
        shine.setColorAt(1.0, QColor(80, 120, 180, 0))
        painter.setBrush(QBrush(shine))
        painter.drawRoundedRect(rect.adjusted(1, 1, -1, -int(h * 0.8)), 7, 7)

        # Subtle blue-tinted grid (Vista blue, not cyan)
        grid_pen = QPen(QColor(41, 89, 155, 18), 1)
        painter.setPen(grid_pen)
        for i in range(1, 4):
            y = int(h * i / 4)
            painter.drawLine(0, y, w, y)
        num_sections = 8
        for i in range(1, num_sections):
            x = int(w * i / num_sections)
            painter.drawLine(x, 0, x, h)

        # Panel border - crisp dark glass edge
        painter.setBrush(Qt.BrushStyle.NoBrush)
        painter.setPen(QPen(QColor(40, 55, 80, 160), 1))
        painter.drawRoundedRect(rect, 8, 8)

        # Center line (muted Vista blue)
        painter.setPen(QPen(QColor(41, 89, 155, 40), 1))
        painter.drawLine(0, int(cy), w, int(cy))
