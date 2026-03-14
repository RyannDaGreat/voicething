"""CRT Terminal style - green phosphor monitor aesthetic.

Simulates a VT100/Apple II green phosphor CRT with authentic effects:
scanlines, phosphor glow, screen curvature vignette, phosphor dot texture,
and a dark plastic bezel. Pure monochrome green on black.
"""

import numpy as np
from PyQt6.QtCore import Qt, QRectF, QPointF
from PyQt6.QtGui import (
    QColor, QLinearGradient, QRadialGradient, QBrush, QImage, QPixmap,
    QPainterPath, QPen,
)

from .base import BaseStyle, get_cached_texture


# === Phosphor green palette ===
PHOSPHOR_BRIGHT = QColor(51, 255, 51)       # #33FF33 — lit phosphor
PHOSPHOR_CSS = "rgb(51,255,51)"
PHOSPHOR_MID = QColor(34, 204, 34)          # #22CC22 — dim phosphor
PHOSPHOR_DIM = QColor(17, 102, 17)          # #116611 — very dim
PHOSPHOR_FAINT = QColor(8, 48, 8)           # #083008 — barely visible
PHOSPHOR_GLOW = QColor(51, 255, 51, 100)    # Glow overlay

# CRT screen black (slight green tint, not too dark for readability)
CRT_BLACK = "rgb(8,14,8)"
CRT_BLACK_Q = QColor(8, 14, 8)

# Bezel / housing colors
BEZEL_DARK = QColor(18, 20, 18)             # Dark plastic
BEZEL_MID = QColor(30, 33, 30)              # Mid bezel
BEZEL_EDGE = QColor(40, 44, 40)             # Inner bezel highlight

# Error/warning — amber phosphor (different CRT type)
AMBER = "rgb(255,170,0)"
AMBER_Q = QColor(255, 170, 0)

# Text CSS — slightly desaturated green for readability
TEXT_BRIGHT = "rgb(80,255,80)"
TEXT_DIM = "rgb(55,210,55)"
TEXT_MUTED = "rgb(30,120,30)"
TEXT_DISABLED = "rgb(15,65,15)"


class CRTTerminalStyle(BaseStyle):
    name = "crt_terminal"
    font = "Menlo"
    corner_radius = 4

    _phosphor_cache = None

    # Accent — phosphor green
    accent = PHOSPHOR_BRIGHT
    accent_css = PHOSPHOR_CSS
    text_primary = TEXT_BRIGHT
    text_secondary = TEXT_DIM
    text_muted = TEXT_MUTED
    text_error = AMBER
    text_link = "rgb(68,255,68)"
    border_color = "rgb(26,29,26)"
    border_dark = "rgb(10,21,10)"
    icon_color_dark = '#33ff33'
    icon_color_light = '#33ff33'
    icon_color_muted = '#116611'

    # Slider — green on dark
    slider_groove = "rgba(17,102,17,0.6)"
    slider_handle = PHOSPHOR_CSS
    slider_fill = "rgb(34,204,34)"

    # Rotary knob — heavy industrial gauge (old hardware)
    knob_style = "industrial"
    knob_body_dark = "#050A05"
    knob_body_light = "#0A1A0A"
    knob_notch_style = "line"
    knob_tickmarks = True
    knob_glow = True
    knob_track_color = "#33ff33"
    knob_label_color = "#22cc22"

    # Waveform — phosphor oscilloscope
    waveform_color = PHOSPHOR_BRIGHT
    waveform_glow = True
    waveform_glow_radius = 22
    waveform_glow_alpha = 180
    waveform_center_line = QColor(51, 255, 51, 35)
    waveform_panel = "crt"

    # Timer — phosphor LCD
    timer_use_lcd = True
    timer_color = PHOSPHOR_BRIGHT
    timer_font_size = 28
    timer_panel_size = (160, 40)

    # Transcription panel
    transcription_text = TEXT_BRIGHT
    transcription_text_dimmed = "rgba(34,204,34,0.7)"
    transcription_panel_bg = CRT_BLACK
    transcription_panel_border = "rgb(10,21,10)"
    transcription_row_hover = "rgba(51,255,51,0.07)"
    transcription_row_btn_bg = "rgba(51,255,51,0.08)"
    transcription_row_btn_hover = "rgba(51,255,51,0.18)"
    transcription_row_btn_pressed = "rgba(51,255,51,0.30)"

    # Input fields — dark with green text
    input_bg = "rgb(5,10,5)"
    input_text = "rgb(51,255,51)"

    # Chime editor — phosphor green on CRT black
    chime_grid_bg = QColor(5, 10, 5)
    chime_grid_line = QColor(17, 40, 17)
    chime_cell_inactive = QColor(10, 20, 10)
    chime_cell_active = PHOSPHOR_BRIGHT
    chime_cell_highlight = QColor(51, 255, 51, 80)
    chime_piano_white = QColor(34, 204, 34)
    chime_piano_black = QColor(5, 15, 5)
    chime_piano_label_white = QColor(8, 48, 8)
    chime_piano_label_black = QColor(51, 255, 51)

    # ── Texture generation ──────────────────────────────────────

    def _get_phosphor_texture(self, width=126, height=126):
        """Get (or generate and cache) the tileable phosphor dot texture."""
        if CRTTerminalStyle._phosphor_cache is not None:
            return CRTTerminalStyle._phosphor_cache

        CRTTerminalStyle._phosphor_cache = get_cached_texture(
            "crt_phosphor", width, height,
            lambda: self._generate_phosphor_texture(width, height),
        )
        return CRTTerminalStyle._phosphor_cache

    def _generate_phosphor_texture(self, width, height):
        """
        Generate a seamlessly tileable phosphor dot grid texture.

        Each "phosphor" is a tiny bright spot on a 3-pixel grid with slight
        falloff, creating the authentic CRT subpixel look. Very dark between
        dots, faint green on dots. Position-keyed hash ensures tiling.
        """
        img = np.zeros((height, width, 4), dtype=np.uint8)

        spacing = 3
        for y in range(height):
            for x in range(width):
                # Distance to nearest grid point
                gy = y % spacing
                gx = x % spacing
                # Center of cell is the phosphor dot
                dy = min(gy, spacing - gy)
                dx = min(gx, spacing - gx)
                dist = (dx * dx + dy * dy) ** 0.5

                # Position-keyed hash for tileable per-pixel variation
                cell_y, cell_x = y // spacing, x // spacing
                h = ((cell_x * 73856093) ^ (cell_y * 19349663)) & 0xFFFFFFFF

                if dist < 0.8:
                    # Phosphor dot center
                    brightness = 14 + (h % 4)
                    img[y, x] = [0, brightness, 0, 18]
                elif dist < 1.5:
                    # Phosphor falloff
                    brightness = 5 + ((h >> 8) % 3)
                    img[y, x] = [0, brightness, 0, 10]
                else:
                    # Dark gap between phosphors
                    img[y, x] = [0, 0, 0, 4]

        qimg = QImage(img.data, width, height, width * 4, QImage.Format.Format_RGBA8888).copy()
        return QPixmap.fromImage(qimg)

    # ── Helper drawing methods ──────────────────────────────────

    def _draw_scanlines(self, painter, rect, width, height, spacing=2, alpha=18):
        """
        Draw CRT scanlines — alternating bright/dark horizontal lines.

        Args:
            painter: QPainter
            rect: QRect of drawing area
            width: int
            height: int
            spacing: Pixel gap between scanlines
            alpha: Darkness of the dark line (higher = more visible scanlines)
        """
        # Dark scanlines (the gap between electron beam passes)
        painter.setPen(QPen(QColor(0, 0, 0, alpha), 1))
        y = rect.top()
        while y < rect.top() + height:
            painter.drawLine(rect.left(), y, rect.left() + width, y)
            y += spacing

    def _draw_screen_glow(self, painter, rect, width, height, alpha_mult=1.0):
        """
        Draw radial green glow from center — phosphor light emission.

        Brighter at the center, falling off toward edges. Suggests the
        phosphor coating is emitting light outward.
        """
        cx = rect.left() + width / 2
        cy = rect.top() + height / 2
        radius = max(width, height) * 0.7

        glow = QRadialGradient(QPointF(cx, cy), radius)
        glow.setColorAt(0.0, QColor(15, 50, 15, int(35 * alpha_mult)))
        glow.setColorAt(0.3, QColor(10, 38, 10, int(25 * alpha_mult)))
        glow.setColorAt(0.6, QColor(5, 20, 5, int(12 * alpha_mult)))
        glow.setColorAt(1.0, QColor(0, 0, 0, 0))

        painter.setBrush(QBrush(glow))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawRect(rect)

    def _draw_crt_vignette(self, painter, rect, width, height):
        """
        Draw heavy corner darkening simulating curved CRT glass.

        Not a simple linear vignette — uses a radial gradient from center
        that darkens aggressively at corners (which are furthest from the
        center of the curved tube).
        """
        cx = rect.left() + width / 2
        cy = rect.top() + height / 2
        # Radius that just covers the center area — corners will be outside
        radius = min(width, height) * 0.65

        vignette = QRadialGradient(QPointF(cx, cy), radius)
        vignette.setColorAt(0.0, QColor(0, 0, 0, 0))
        vignette.setColorAt(0.6, QColor(0, 0, 0, 0))
        vignette.setColorAt(0.75, QColor(0, 0, 0, 15))
        vignette.setColorAt(0.85, QColor(0, 0, 0, 40))
        vignette.setColorAt(0.95, QColor(0, 0, 0, 80))
        vignette.setColorAt(1.0, QColor(0, 0, 0, 120))

        painter.setBrush(QBrush(vignette))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawRect(rect)

    def _draw_bezel(self, painter, rect, width, height, focused=True):
        """
        Draw the CRT housing bezel around the screen area.

        Thick dark border suggesting plastic/metal housing. When focused,
        the inner edge gets a faint green glow from the screen light.
        """
        radius = self.corner_radius
        bezel_width = 6

        painter.setBrush(Qt.BrushStyle.NoBrush)

        # Outer bezel edge — darkest
        painter.setPen(QPen(BEZEL_DARK, bezel_width))
        painter.drawRoundedRect(
            rect.adjusted(bezel_width // 2, bezel_width // 2,
                          -bezel_width // 2, -bezel_width // 2),
            radius, radius,
        )

        # Bezel inner highlight — slight bevel
        painter.setPen(QPen(BEZEL_EDGE, 1))
        painter.drawRoundedRect(rect.adjusted(bezel_width, bezel_width,
                                              -bezel_width, -bezel_width),
                                max(0, radius - 2), max(0, radius - 2))

        # Screen light hitting the bezel inner edge (when focused/powered on)
        if focused:
            painter.setPen(QPen(QColor(20, 80, 20, 60), 2))
            painter.drawRoundedRect(
                rect.adjusted(bezel_width - 1, bezel_width - 1,
                              -(bezel_width - 1), -(bezel_width - 1)),
                max(0, radius - 1), max(0, radius - 1),
            )

    def _draw_static_noise(self, painter, rect, width, height, alpha=6):
        """
        Draw very faint random noise overlay — analog signal interference.

        Uses a sparse approach: only draws a fraction of pixels to keep
        it subtle and performant.
        """
        np.random.seed(13)
        # Sparse noise — draw ~3% of pixels
        n_dots = max(100, (width * height) // 35)
        xs = np.random.randint(0, width, size=n_dots)
        ys = np.random.randint(0, height, size=n_dots)
        brightnesses = np.random.randint(0, 30, size=n_dots)

        for i in range(n_dots):
            a = int(alpha + brightnesses[i] * 0.3)
            painter.setPen(QPen(QColor(20, 60, 20, a), 1))
            painter.drawPoint(rect.left() + int(xs[i]), rect.top() + int(ys[i]))

    # ── Main painting methods ───────────────────────────────────

    def paint_window(self, painter, rect, width, height, focused=True):
        """
        Paint CRT terminal window with all authentic effects.

        Layers (bottom to top):
        1. CRT black base with green tint
        2. Phosphor dot texture
        3. Screen glow (radial green from center)
        4. Scanlines
        5. CRT curvature vignette (heavy corner darkening)
        6. Static noise
        7. Bezel (housing border)
        """
        radius = self.corner_radius
        alpha_mult = 1.0 if focused else 0.6

        # Clip to rounded rect
        path = QPainterPath()
        path.addRoundedRect(QRectF(rect), radius, radius)
        painter.setClipPath(path)

        # 1. CRT black base
        painter.setBrush(QColor(5, 10, 5, int(255 * alpha_mult)))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawRect(rect)

        # 2. Phosphor dot texture (tileable)
        phosphor = self._get_phosphor_texture()
        painter.setOpacity(alpha_mult)
        painter.drawTiledPixmap(rect, phosphor)
        painter.setOpacity(1.0)

        # 3. Screen glow — radial green from center
        self._draw_screen_glow(painter, rect, width, height, alpha_mult)

        # 4. Scanlines (subtle — every 3px, low alpha to keep text readable)
        self._draw_scanlines(painter, rect, width, height, spacing=3,
                             alpha=int(12 * alpha_mult))

        # 5. CRT curvature vignette
        self._draw_crt_vignette(painter, rect, width, height)

        # 6. Subtle static noise (very faint)
        self._draw_static_noise(painter, rect, width, height,
                                alpha=int(3 * alpha_mult))

        # End clipping for bezel
        painter.setClipping(False)

        # 7. Bezel
        self._draw_bezel(painter, rect, width, height, focused)

    def paint_waveform_panel(self, painter, rect, w, h, cy):
        """
        Paint oscilloscope-style waveform panel.

        This is the "active" part of the CRT screen — slightly brighter
        phosphor glow, oscilloscope grid lines, and the scanlines continue
        through it for consistency.
        """
        # Dark base (slightly brighter than main background)
        panel_grad = QLinearGradient(0, 0, 0, h)
        panel_grad.setColorAt(0.0, QColor(6, 14, 6))
        panel_grad.setColorAt(0.3, QColor(5, 12, 5))
        panel_grad.setColorAt(0.7, QColor(4, 10, 4))
        panel_grad.setColorAt(1.0, QColor(3, 8, 3))
        painter.setBrush(QBrush(panel_grad))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawRoundedRect(rect, 4, 4)

        # Oscilloscope grid — dim green lines
        painter.setPen(QPen(QColor(17, 50, 17, 40), 1))
        # Horizontal grid
        for i in range(1, 4):
            y = int(h * i / 4)
            painter.drawLine(0, y, w, y)
        # Vertical grid
        for i in range(1, 8):
            x = int(w * i / 8)
            painter.drawLine(x, 0, x, h)

        # Brighter phosphor glow at center of panel (persistence effect)
        glow_cx = w / 2
        glow_cy = h / 2
        glow_radius = max(w, h) * 0.5
        panel_glow = QRadialGradient(QPointF(glow_cx, glow_cy), glow_radius)
        panel_glow.setColorAt(0.0, QColor(15, 60, 15, 45))
        panel_glow.setColorAt(0.4, QColor(10, 40, 10, 25))
        panel_glow.setColorAt(1.0, QColor(0, 0, 0, 0))
        painter.setBrush(QBrush(panel_glow))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawRect(rect)

        # Scanlines continue through the panel (subtle)
        self._draw_scanlines(painter, rect, w, h, spacing=3, alpha=8)

        # Center line — brighter green with bloom
        # Bloom layer (wider, dimmer)
        painter.setPen(QPen(QColor(51, 255, 51, 25), 5))
        painter.drawLine(0, int(cy), w, int(cy))
        # Core line
        painter.setPen(QPen(QColor(51, 255, 51, 50), 1))
        painter.drawLine(0, int(cy), w, int(cy))

        # Panel border — recessed edge
        painter.setBrush(Qt.BrushStyle.NoBrush)
        # Dark inset shadow (top/left)
        painter.setPen(QPen(QColor(0, 0, 0, 120), 1))
        painter.drawLine(rect.left(), rect.top(), rect.right(), rect.top())
        painter.drawLine(rect.left(), rect.top(), rect.left(), rect.bottom())
        # Light edge (bottom/right)
        painter.setPen(QPen(QColor(30, 40, 30, 80), 1))
        painter.drawLine(rect.left(), rect.bottom(), rect.right(), rect.bottom())
        painter.drawLine(rect.right(), rect.top(), rect.right(), rect.bottom())
        # Faint green glow on border from screen
        painter.setPen(QPen(QColor(20, 80, 20, 40), 1))
        painter.drawRoundedRect(rect.adjusted(1, 1, -1, -1), 3, 3)

    # ── CSS methods ─────────────────────────────────────────────

    def title_style(self, size=18):
        return (
            f"color: {PHOSPHOR_CSS}; font-size: {size}px; "
            f"font-family: {self.font};"
        )

    def body_style(self, size=10):
        return f"color: {TEXT_DIM}; font-size: {size}px; font-family: {self.font};"

    def section_style(self):
        return (
            f"color: rgb(68,255,68); font-size: 12px; "
            f"font-family: {self.font};"
        )

    def button_css(self):
        return (
            # Normal — dark with faint green border
            f"QPushButton {{ color: {TEXT_DIM}; "
            f"background: qlineargradient(x1:0, y1:0, x2:0, y2:1, "
            f"stop:0 rgb(12,22,12), stop:0.5 rgb(8,16,8), stop:1 rgb(12,22,12)); "
            f"border: 1px solid rgb(17,50,17); "
            f"border-radius: 3px; padding: 3px 8px; "
            f"font-size: 11px; font-family: {self.font}; text-align: left; }}"
            # Hover — phosphor brightens
            f"QPushButton:hover {{ color: {PHOSPHOR_CSS}; "
            f"background: qlineargradient(x1:0, y1:0, x2:0, y2:1, "
            f"stop:0 rgb(15,35,15), stop:0.5 rgb(10,25,10), stop:1 rgb(15,35,15)); "
            f"border: 1px solid rgb(34,120,34); }}"
            # Pressed — inset
            f"QPushButton:pressed {{ color: {PHOSPHOR_CSS}; "
            f"background: qlineargradient(x1:0, y1:0, x2:0, y2:1, "
            f"stop:0 rgb(5,12,5), stop:0.5 rgb(8,18,8), stop:1 rgb(5,12,5)); "
            f"border: 1px solid rgb(17,80,17); }}"
            # Disabled — phosphor burned out
            f"QPushButton:disabled {{ color: {TEXT_DISABLED}; "
            f"background: rgb(5,8,5); border: 1px solid rgb(10,20,10); }}"
            # Checked — phosphor fully lit
            f"QPushButton:checked {{ color: rgb(200,255,200); "
            f"background: qlineargradient(x1:0, y1:0, x2:0, y2:1, "
            f"stop:0 rgb(10,60,10), stop:0.5 rgb(8,45,8), stop:1 rgb(10,60,10)); "
            f"border: 1px solid {PHOSPHOR_CSS}; }}"
            f"QPushButton:checked:hover {{ "
            f"background: qlineargradient(x1:0, y1:0, x2:0, y2:1, "
            f"stop:0 rgb(12,70,12), stop:0.5 rgb(10,55,10), stop:1 rgb(12,70,12)); }}"
        )

    def menu_css(self):
        return (
            f"QMenu {{ background: rgb(5,10,5); color: {TEXT_BRIGHT}; "
            f"border: 1px solid rgb(17,80,17); border-radius: 3px; "
            f"padding: 4px; font-family: {self.font}; font-size: 12px; }}"
            "QMenu::item { padding: 4px 16px; border-radius: 2px; }"
            f"QMenu::item:selected {{ color: rgb(200,255,200); "
            f"background: rgb(10,50,10); }}"
            f"QMenu::separator {{ height: 1px; background: rgb(17,50,17); "
            f"margin: 4px 8px; }}"
        )

    def _scrollbar_vertical_css(self):
        return (
            f"QScrollBar:vertical {{ width: 12px; background: rgb(5,10,5); "
            f"border: 1px solid rgb(10,21,10); border-radius: 6px; margin: 0px; }}"
            # Handle — phosphor green bar
            "QScrollBar::handle:vertical { "
            "background: qlineargradient(x1:0, y1:0, x2:1, y2:0, "
            "stop:0.0 rgb(10,60,10), stop:0.3 rgb(17,90,17), "
            "stop:0.5 rgb(22,110,22), stop:0.7 rgb(17,90,17), stop:1.0 rgb(10,60,10)); "
            "border: 1px solid rgb(10,40,10); border-radius: 5px; "
            "min-height: 30px; margin: 1px; }"
            # Handle hover — brighter phosphor
            "QScrollBar::handle:vertical:hover { "
            "background: qlineargradient(x1:0, y1:0, x2:1, y2:0, "
            "stop:0.0 rgb(17,90,17), stop:0.3 rgb(26,140,26), "
            "stop:0.5 rgb(34,170,34), stop:0.7 rgb(26,140,26), stop:1.0 rgb(17,90,17)); "
            "border: 1px solid rgb(17,70,17); }"
            # Handle pressed
            "QScrollBar::handle:vertical:pressed { "
            "background: qlineargradient(x1:0, y1:0, x2:1, y2:0, "
            "stop:0.0 rgb(8,40,8), stop:0.3 rgb(12,60,12), "
            "stop:0.5 rgb(17,80,17), stop:0.7 rgb(12,60,12), stop:1.0 rgb(8,40,8)); "
            "border: 1px solid rgb(8,30,8); }"
            "QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical { "
            "height: 0; width: 0; background: none; border: none; }"
            "QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical { "
            "background: transparent; }"
        )

    def panel_bg_css(self):
        return (
            f"background: qlineargradient(x1:0, y1:0, x2:0, y2:1, "
            f"stop:0 rgb(8,16,8), stop:0.02 rgb(5,10,5), "
            f"stop:0.98 rgb(5,10,5), stop:1 rgb(3,6,3)); "
            f"border: 1px solid rgb(10,21,10); border-radius: 3px;"
        )

    def panel_bg_flat_css(self):
        return (
            f"background: rgb(5,10,5); border: 1px solid rgb(10,21,10); "
            f"border-radius: 3px;"
        )
