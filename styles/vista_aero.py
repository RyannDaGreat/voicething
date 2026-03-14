"""Vista Aero style - Windows Vista glossy glass with prominent reflections.

Key glossy technique (from Illustrator tutorial): a white-to-transparent gradient
overlay on the top ~40% of surfaces creates the characteristic 'screen blend'
glass reflection. Every surface has this split: bright highlight top, darker
base bottom.
"""

from PyQt6.QtCore import Qt, QRectF
from PyQt6.QtGui import QColor, QLinearGradient, QRadialGradient, QBrush, QPen

from .base import BaseStyle, RED_ERROR, LIGHT_GRAY


# Vista Aero blue palette
VISTA_BLUE = QColor(40, 100, 180)         # Primary accent
VISTA_BLUE_CSS = "rgb(40,100,180)"
VISTA_BLUE_LIGHT = QColor(100, 170, 240)  # Lighter variant
VISTA_BLUE_GLOW = QColor(80, 160, 255)    # Glow color

# Glass surface colors — Vista's DWM glass is a semi-transparent blue-tinted panel
GLASS_BG_TOP = QColor(62, 80, 110, 230)       # Top of glass panel
GLASS_BG_MID = QColor(38, 52, 78, 235)        # Mid
GLASS_BG_BOTTOM = QColor(24, 36, 58, 240)     # Bottom (darkest)

# Text
WHITE_95 = "rgba(255,255,255,0.95)"
WHITE_85 = "rgba(255,255,255,0.85)"
WHITE_70 = "rgba(255,255,255,0.7)"
WHITE_50 = "rgba(255,255,255,0.5)"
WHITE_30 = "rgba(255,255,255,0.3)"
WHITE_15 = "rgba(255,255,255,0.15)"
WHITE_8 = "rgba(255,255,255,0.08)"

# Blue accent alpha variants
BLUE_90 = "rgba(40,100,180,0.9)"
BLUE_60 = "rgba(40,100,180,0.6)"
BLUE_40 = "rgba(80,160,255,0.4)"
BLUE_25 = "rgba(80,160,255,0.25)"
BLUE_12 = "rgba(80,160,255,0.12)"

# Borders — glossy panels have subtle bright edges
GLASS_BORDER = "rgb(80,100,140)"
GLASS_BORDER_DARK = "rgb(50,65,95)"
GLASS_BORDER_HOVER = "rgb(100,170,240)"
PANEL_BORDER = "rgb(60,80,115)"
PANEL_BORDER_DARK = "rgb(45,60,90)"


class VistaAeroStyle(BaseStyle):
    name = "vista_aero"
    font = "Segoe UI"

    # Colors — bright blue accent on dark glass
    accent = VISTA_BLUE
    accent_css = VISTA_BLUE_CSS
    text_primary = WHITE_95
    text_secondary = WHITE_85
    text_muted = WHITE_50
    text_error = RED_ERROR
    text_link = "rgba(100,170,240,0.95)"
    border_color = GLASS_BORDER
    border_dark = GLASS_BORDER_DARK
    icon_color_dark = '#ffffff'
    icon_color_light = '#ffffff'
    icon_color_muted = '#8899bb'

    # Input fields — dark glass
    input_bg = '#1e2a40'
    input_text = '#d8e4f0'

    # Slider — blue glow groove
    slider_groove = "rgba(80,160,255,0.2)"

    # Rotary knob — Aero glass style
    knob_style = "aero"
    knob_body_dark = "#1a2840"
    knob_body_light = "#3a5880"
    knob_notch_style = "needle"
    knob_tickmarks = True
    knob_glow = True
    knob_track_color = "#50a0f0"
    knob_label_color = "#90b8e0"

    # Waveform — blue with glow
    waveform_color = VISTA_BLUE
    waveform_glow = True
    waveform_glow_alpha = 180
    waveform_center_line = QColor(80, 160, 255, 30)
    waveform_panel = "dark"

    # Timer — LCD with blue
    timer_use_lcd = True
    timer_color = VISTA_BLUE

    # Transcription panel — dark glass
    transcription_text = LIGHT_GRAY
    transcription_text_dimmed = "rgba(120,160,200,0.7)"
    transcription_panel_bg = (
        "qlineargradient(x1:0, y1:0, x2:0, y2:1, "
        "stop:0 rgba(35,50,75,0.95), stop:1 rgba(20,30,50,0.95))"
    )
    transcription_panel_border = PANEL_BORDER_DARK
    transcription_row_hover = BLUE_12
    transcription_row_btn_bg = WHITE_8
    transcription_row_btn_hover = BLUE_25
    transcription_row_btn_pressed = BLUE_40

    # Chime editor — dark blue glass
    chime_grid_bg = QColor(20, 30, 50)
    chime_grid_line = QColor(50, 70, 100)
    chime_cell_inactive = QColor(30, 45, 70)
    chime_cell_active = QColor(80, 160, 255)
    chime_cell_highlight = QColor(80, 160, 255, 80)
    chime_piano_white = QColor(190, 210, 230)
    chime_piano_black = QColor(25, 35, 55)
    chime_piano_label_white = QColor(40, 60, 90)
    chime_piano_label_black = QColor(140, 175, 210)

    def button_css(self):
        # Glossy pill button: gradient with a visible bright top-half "reflection"
        # The gloss is the stop:0→stop:0.45 being much brighter than stop:0.5→stop:1
        return (
            f"QPushButton {{ "
            f"color: {WHITE_85}; "
            f"background: qlineargradient(x1:0, y1:0, x2:0, y2:1, "
            f"stop:0 rgba(120,145,185,0.95), "      # Bright top (gloss)
            f"stop:0.42 rgba(80,110,155,0.9), "      # Still bright
            f"stop:0.5 rgba(45,65,100,0.9), "        # Sharp transition (the gloss edge)
            f"stop:0.52 rgba(38,55,85,0.9), "        # Dark bottom
            f"stop:1 rgba(30,45,72,0.9)); "          # Darkest
            f"border: 1px solid {GLASS_BORDER}; "
            f"border-top: 1px solid rgba(180,200,230,0.5); "  # Bright top edge
            f"border-radius: 4px; padding: 2px 4px; font-size: 10px; "
            f"font-family: {self.font}; text-align: left; }}"

            f"QPushButton:hover {{ "
            f"background: qlineargradient(x1:0, y1:0, x2:0, y2:1, "
            f"stop:0 rgba(140,170,210,0.95), "
            f"stop:0.42 rgba(100,140,190,0.95), "
            f"stop:0.5 rgba(60,90,135,0.95), "
            f"stop:0.52 rgba(50,75,115,0.95), "
            f"stop:1 rgba(40,60,95,0.95)); "
            f"border: 1px solid {GLASS_BORDER_HOVER}; "
            f"border-top: 1px solid rgba(200,220,245,0.6); }}"

            f"QPushButton:pressed {{ "
            f"background: qlineargradient(x1:0, y1:0, x2:0, y2:1, "
            f"stop:0 rgba(25,38,62,0.95), "          # Inverted — dark top (pressed in)
            f"stop:0.48 rgba(35,52,82,0.95), "
            f"stop:0.5 rgba(55,80,120,0.95), "
            f"stop:1 rgba(80,115,165,0.95)); "
            f"border: 1px solid {BLUE_60}; }}"

            f"QPushButton:disabled {{ color: {WHITE_30}; "
            f"background: rgba(30,40,60,0.3); border: 1px solid rgba(50,65,95,0.3); }}"

            f"QPushButton:checked {{ "
            f"background: qlineargradient(x1:0, y1:0, x2:0, y2:1, "
            f"stop:0 rgba(100,160,220,0.7), "
            f"stop:0.42 rgba(70,130,190,0.65), "
            f"stop:0.5 rgba(40,90,150,0.6), "
            f"stop:1 rgba(30,70,130,0.55)); "
            f"border: 1px solid {BLUE_60}; "
            f"border-top: 1px solid rgba(160,200,240,0.5); }}"

            f"QPushButton:checked:hover {{ "
            f"background: qlineargradient(x1:0, y1:0, x2:0, y2:1, "
            f"stop:0 rgba(120,175,235,0.75), "
            f"stop:0.42 rgba(85,145,205,0.7), "
            f"stop:0.5 rgba(55,105,170,0.65), "
            f"stop:1 rgba(40,85,145,0.6)); }}"
        )

    def menu_css(self):
        # Glossy glass menu — bright top, dark bottom, white top edge
        return (
            f"QMenu {{ "
            f"background: qlineargradient(x1:0, y1:0, x2:0, y2:1, "
            f"stop:0 rgba(75,95,130,0.96), "
            f"stop:0.35 rgba(55,75,110,0.96), "
            f"stop:0.5 rgba(40,55,85,0.96), "
            f"stop:1 rgba(28,40,65,0.96)); "
            f"color: white; border: 1px solid rgba(90,110,145,0.7); "
            f"border-top: 1px solid rgba(180,200,230,0.4); "
            f"border-radius: 6px; padding: 6px; font-family: {self.font}; }}"
            "QMenu::item { padding: 6px 14px; border-radius: 4px; }"
            "QMenu::item:selected { "
            "background: qlineargradient(x1:0, y1:0, x2:0, y2:1, "
            "stop:0 rgba(100,170,240,0.4), stop:1 rgba(60,120,200,0.3)); }"
            f"QMenu::separator {{ height: 1px; background: {WHITE_15}; margin: 4px 8px; }}"
        )

    def _scrollbar_vertical_css(self):
        return (
            "QScrollBar:vertical { width: 10px; background: transparent; margin: 2px; border: none; }"
            "QScrollBar::handle:vertical { "
            "background: qlineargradient(x1:0, y1:0, x2:1, y2:0, "
            "stop:0 rgba(60,85,120,0.6), stop:0.3 rgba(90,120,165,0.7), "
            "stop:0.5 rgba(100,135,180,0.75), stop:0.7 rgba(90,120,165,0.7), "
            "stop:1 rgba(60,85,120,0.6)); "
            "border-radius: 5px; min-height: 30px; margin: 0px; }"
            "QScrollBar::handle:vertical:hover { "
            "background: qlineargradient(x1:0, y1:0, x2:1, y2:0, "
            "stop:0 rgba(80,140,210,0.6), stop:0.5 rgba(100,170,240,0.7), "
            "stop:1 rgba(80,140,210,0.6)); }"
            "QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical { height: 0; }"
            "QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical { background: transparent; }"
        )

    def panel_bg_css(self):
        return (
            "background: qlineargradient(x1:0, y1:0, x2:0, y2:1, "
            "stop:0 rgba(55,75,110,0.95), stop:0.4 rgba(42,58,88,0.95), "
            "stop:0.5 rgba(35,50,78,0.95), stop:1 rgba(25,38,62,0.95)); "
            f"border: 1px solid {PANEL_BORDER}; "
            "border-top: 1px solid rgba(140,170,210,0.3); "
            "border-radius: 8px;"
        )

    def panel_bg_flat_css(self):
        return (
            "background: qlineargradient(x1:0, y1:0, x2:0, y2:1, "
            "stop:0 rgba(35,50,78,0.95), stop:1 rgba(22,32,55,0.95)); "
            f"border: 1px solid {PANEL_BORDER_DARK}; "
            "border-radius: 8px;"
        )

    def paint_window(self, painter, rect, width, height, focused=True):
        """Paint Vista Aero glass with glossy reflection and bottom glow.

        Four-layer glossy effect (from Illustrator tutorial):
        1. Base glass gradient (dark blue, semi-transparent)
        2. Bright white-to-transparent overlay on top ~38% (specular 'screen blend' gloss)
        3. Soft diffused bottom glow (the blurred ambient light below the gloss)
        4. Inner shadow at very top for depth
        """
        radius = self.corner_radius
        alpha_mult = 1.0 if focused else 0.85

        # Layer 1: Base glass gradient — dark blue-tinted
        grad = QLinearGradient(0, rect.top(), 0, rect.bottom())
        grad.setColorAt(0, QColor(55, 75, 110, int(235 * alpha_mult)))
        grad.setColorAt(0.15, QColor(42, 60, 92, int(240 * alpha_mult)))
        grad.setColorAt(0.5, QColor(32, 48, 75, int(242 * alpha_mult)))
        grad.setColorAt(0.85, QColor(24, 36, 60, int(245 * alpha_mult)))
        grad.setColorAt(1, QColor(18, 28, 48, int(248 * alpha_mult)))
        painter.setBrush(QBrush(grad))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawRoundedRect(rect, radius, radius)

        # Layer 2: THE GLOSS — bright white-to-transparent in top ~38%
        # Sharp specular reflection highlight (the defining Vista look)
        gloss_height = int(height * 0.38)
        gloss_rect = QRectF(
            rect.left() + 1, rect.top() + 1,
            rect.width() - 2, gloss_height
        )
        gloss_grad = QLinearGradient(0, rect.top(), 0, rect.top() + gloss_height)
        gloss_grad.setColorAt(0, QColor(255, 255, 255, int(90 * alpha_mult)))
        gloss_grad.setColorAt(0.3, QColor(255, 255, 255, int(55 * alpha_mult)))
        gloss_grad.setColorAt(0.7, QColor(200, 220, 255, int(25 * alpha_mult)))
        gloss_grad.setColorAt(1, QColor(255, 255, 255, 0))
        painter.setBrush(QBrush(gloss_grad))
        painter.drawRoundedRect(gloss_rect, radius - 1, radius - 1)

        # Layer 3: BOTTOM GLOW — soft diffused blue-white glow in lower portion
        # This is the blurred ambient light from the tutorial's blend step:
        # transparent at mid-height, building to a soft blue-white glow at bottom
        glow_top = rect.top() + int(height * 0.55)
        glow_rect = QRectF(
            rect.left() + 2, glow_top,
            rect.width() - 4, rect.bottom() - glow_top - 1
        )
        glow_grad = QLinearGradient(0, glow_top, 0, rect.bottom())
        glow_grad.setColorAt(0, QColor(100, 160, 240, 0))
        glow_grad.setColorAt(0.3, QColor(80, 140, 220, int(12 * alpha_mult)))
        glow_grad.setColorAt(0.6, QColor(100, 170, 240, int(28 * alpha_mult)))
        glow_grad.setColorAt(0.85, QColor(120, 185, 250, int(40 * alpha_mult)))
        glow_grad.setColorAt(1, QColor(140, 200, 255, int(50 * alpha_mult)))
        painter.setBrush(QBrush(glow_grad))
        painter.drawRoundedRect(glow_rect, radius - 2, radius - 2)

        # Layer 4: Inner shadow at very top (thin dark line for recessed glass look)
        shadow_grad = QLinearGradient(0, rect.top(), 0, rect.top() + 6)
        shadow_grad.setColorAt(0, QColor(0, 0, 0, int(30 * alpha_mult)))
        shadow_grad.setColorAt(1, QColor(0, 0, 0, 0))
        painter.setBrush(QBrush(shadow_grad))
        painter.drawRoundedRect(
            rect.adjusted(0, 0, 0, -rect.height() + 10), radius, radius
        )

        # Glass border — bright top edge, darker sides/bottom
        painter.setBrush(Qt.BrushStyle.NoBrush)
        # Bottom/side border
        painter.setPen(QPen(QColor(60, 80, 120, int(180 * alpha_mult)), 1))
        painter.drawRoundedRect(rect, radius, radius)
        # Bright top edge highlight (the rim of the glass)
        top_highlight = QLinearGradient(rect.left(), rect.top(), rect.right(), rect.top())
        top_highlight.setColorAt(0, QColor(255, 255, 255, 0))
        top_highlight.setColorAt(0.2, QColor(180, 210, 240, int(100 * alpha_mult)))
        top_highlight.setColorAt(0.5, QColor(200, 225, 250, int(120 * alpha_mult)))
        top_highlight.setColorAt(0.8, QColor(180, 210, 240, int(100 * alpha_mult)))
        top_highlight.setColorAt(1, QColor(255, 255, 255, 0))
        painter.setPen(QPen(QBrush(top_highlight), 1))
        painter.drawLine(
            rect.left() + radius, rect.top(),
            rect.right() - radius, rect.top()
        )

        # Focus glow — blue Aero ring
        if focused:
            for i in range(3):
                glow_alpha = int(50 - i * 15)
                painter.setPen(QPen(QColor(80, 160, 255, glow_alpha), 2 + i * 2))
                painter.drawRoundedRect(
                    rect.adjusted(-i, -i, i, i), radius + i, radius + i
                )
            painter.setPen(QPen(VISTA_BLUE_GLOW, 2))
            painter.drawRoundedRect(rect, radius, radius)

    def paint_waveform_panel(self, painter, rect, w, h, cy):
        """Dark glass panel with glossy highlight and bottom glow."""
        # Dark glass background
        panel_grad = QLinearGradient(0, 0, 0, h)
        panel_grad.setColorAt(0, QColor(35, 50, 78, 240))
        panel_grad.setColorAt(0.5, QColor(25, 38, 60, 240))
        panel_grad.setColorAt(1, QColor(18, 28, 48, 240))
        painter.setBrush(QBrush(panel_grad))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawRoundedRect(rect, 8, 8)

        # Glossy highlight on top ~30%
        gloss_h = int(h * 0.3)
        gloss_rect = QRectF(rect.left() + 1, rect.top() + 1, w - 2, gloss_h)
        gloss = QLinearGradient(0, 0, 0, gloss_h)
        gloss.setColorAt(0, QColor(255, 255, 255, 40))
        gloss.setColorAt(0.5, QColor(200, 220, 255, 15))
        gloss.setColorAt(1, QColor(255, 255, 255, 0))
        painter.setBrush(QBrush(gloss))
        painter.drawRoundedRect(gloss_rect, 7, 7)

        # Bottom glow — soft diffused blue in lower portion
        glow_top = int(h * 0.6)
        glow_rect = QRectF(rect.left() + 1, glow_top, w - 2, h - glow_top - 1)
        bottom_glow = QLinearGradient(0, glow_top, 0, h)
        bottom_glow.setColorAt(0, QColor(80, 140, 220, 0))
        bottom_glow.setColorAt(0.5, QColor(80, 150, 230, 15))
        bottom_glow.setColorAt(1, QColor(100, 170, 245, 30))
        painter.setBrush(QBrush(bottom_glow))
        painter.drawRoundedRect(glow_rect, 7, 7)

        # Subtle blue grid
        painter.setPen(QPen(QColor(80, 160, 255, 15), 1))
        for i in range(1, 4):
            y = int(h * i / 4)
            painter.drawLine(0, y, w, y)
        num_sections = 8
        for i in range(1, num_sections):
            painter.drawLine(int(w * i / num_sections), 0, int(w * i / num_sections), h)

        # Panel border
        painter.setBrush(Qt.BrushStyle.NoBrush)
        painter.setPen(QPen(QColor(50, 70, 100, 150), 1))
        painter.drawRoundedRect(rect, 8, 8)
