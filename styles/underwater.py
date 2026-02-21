"""Underwater / Deep Sea style - procedural caustic light, bioluminescence, bubbles.

Like peering down through ocean water at the sea floor. Caustic light networks
ripple across deep blue-green gradients, scattered bubbles rise from below,
and bioluminescent accents glow in the abyss.
"""

import numpy as np
from PyQt6.QtCore import Qt, QPointF, QRectF
from PyQt6.QtGui import (
    QColor, QLinearGradient, QRadialGradient, QBrush, QImage, QPixmap,
    QPainterPath, QPen,
)

from .base import BaseStyle, get_cached_texture


# --- Deep ocean palette ---------------------------------------------------

# Water column gradient (top=near surface, bottom=abyss)
SURFACE_BLUE   = QColor(21, 48, 74)     # #15304A - lighter deep blue near top
ABYSS_BLUE     = QColor(10, 24, 40)     # #0A1828 - near-black at depth

# Bioluminescent accent
BIOLUM_CYAN      = QColor(0, 229, 204)    # #00E5CC
BIOLUM_CYAN_CSS  = "rgb(0,229,204)"
BIOLUM_BRIGHT    = QColor(64, 255, 224)   # #40FFE0

# Text
TEXT_AQUA_WHITE  = "rgb(232,255,248)"      # #E8FFF8
TEXT_AQUA_SOFT   = "rgb(184,232,224)"      # #B8E8E0
TEXT_DEEP_GRAY   = "rgb(106,138,138)"      # #6A8A8A

# Error / accent extras
CORAL_ERROR      = "rgb(255,119,102)"      # #FF7766
CORAL_WARM       = QColor(255, 140, 100)   # kelp/coral hint

# Borders
BORDER_DEEP      = "rgb(8,18,42)"          # #08122A
BORDER_MID       = "rgb(18,40,65)"

# Translucent helpers
CYAN_TRANS_15    = "rgba(0,229,204,0.15)"
CYAN_TRANS_10    = "rgba(0,229,204,0.10)"
CYAN_TRANS_25    = "rgba(0,229,204,0.25)"
CYAN_TRANS_40    = "rgba(0,229,204,0.40)"

# Panel
PANEL_BG         = "rgba(8,18,34,220)"
PANEL_BORDER     = "rgb(12,28,50)"


class UnderwaterStyle(BaseStyle):
    name = "underwater"
    font = "Futura"

    _caustic_cache = None

    # --- Aquatic effects flags ---
    waveform_bubbles = True

    # --- Colors ---
    accent         = BIOLUM_CYAN
    accent_css     = BIOLUM_CYAN_CSS
    text_primary   = TEXT_AQUA_WHITE
    text_secondary = TEXT_AQUA_SOFT
    text_muted     = TEXT_DEEP_GRAY
    text_error     = CORAL_ERROR
    text_link      = "rgb(64,255,224)"
    border_color   = BORDER_MID
    border_dark    = BORDER_DEEP
    icon_color_dark  = '#40ffe0'
    icon_color_light = '#e8fff8'
    icon_color_muted = '#4a7a7a'

    # --- Waveform ---
    waveform_color       = BIOLUM_CYAN
    waveform_glow        = True
    waveform_glow_radius = 22
    waveform_glow_alpha  = 180
    waveform_center_line = QColor(0, 229, 204, 50)
    waveform_panel       = "dark"

    # --- Timer ---
    timer_use_lcd  = True
    timer_color    = BIOLUM_CYAN

    # --- Slider ---
    slider_groove  = "rgba(8,18,42,0.8)"
    slider_handle  = BIOLUM_CYAN_CSS
    slider_fill    = "rgb(0,180,160)"

    # --- Knob ---
    knob_style       = "glass"
    knob_body_dark   = "#0a1828"
    knob_body_light  = "#15304a"
    knob_notch_style = "line"
    knob_tickmarks   = True
    knob_glow        = True

    # --- Input ---
    input_bg   = '#0c1e34'
    input_text = '#e8fff8'

    # --- Transcription ---
    transcription_text        = TEXT_AQUA_WHITE
    transcription_text_dimmed = TEXT_AQUA_SOFT
    transcription_panel_bg    = PANEL_BG
    transcription_panel_border = PANEL_BORDER
    transcription_row_hover      = CYAN_TRANS_10
    transcription_row_btn_bg     = CYAN_TRANS_15
    transcription_row_btn_hover  = CYAN_TRANS_25
    transcription_row_btn_pressed = CYAN_TRANS_40

    # --- Chime editor ---
    chime_grid_bg          = QColor(10, 24, 40)
    chime_grid_line        = QColor(20, 50, 70)
    chime_cell_inactive    = QColor(15, 35, 55)
    chime_cell_active      = QColor(0, 229, 204)
    chime_cell_highlight   = QColor(0, 229, 204, 90)
    chime_piano_white      = QColor(200, 235, 230)
    chime_piano_black      = QColor(10, 28, 44)
    chime_piano_label_white = QColor(30, 70, 80)
    chime_piano_label_black = QColor(160, 220, 210)

    # ------------------------------------------------------------------
    #  CSS overrides
    # ------------------------------------------------------------------

    def button_css(self):
        return (
            f"QPushButton {{ color: {TEXT_AQUA_SOFT}; "
            f"background: qlineargradient(x1:0, y1:0, x2:0, y2:1, "
            f"stop:0 rgb(22,52,78), stop:0.5 rgb(14,36,58), stop:1 rgb(10,24,40)); "
            f"border: 1px solid rgb(18,40,65); border-top-color: rgba(0,229,204,0.25); "
            f"border-radius: 5px; padding: 3px 8px; font-size: 11px; "
            f"font-family: {self.font}; text-align: left; }}"
            # Hover
            f"QPushButton:hover {{ color: {TEXT_AQUA_WHITE}; "
            f"background: qlineargradient(x1:0, y1:0, x2:0, y2:1, "
            f"stop:0 rgb(28,62,90), stop:0.5 rgb(18,46,70), stop:1 rgb(12,30,50)); "
            f"border: 1px solid rgba(0,229,204,0.45); }}"
            # Pressed
            f"QPushButton:pressed {{ color: rgb(64,255,224); "
            f"background: qlineargradient(x1:0, y1:0, x2:0, y2:1, "
            f"stop:0 rgb(8,20,34), stop:0.5 rgb(12,28,46), stop:1 rgb(16,38,58)); "
            f"border: 1px solid rgba(0,229,204,0.6); }}"
            # Disabled
            f"QPushButton:disabled {{ color: {TEXT_DEEP_GRAY}; "
            f"background: rgb(10,24,40); border: 1px solid rgb(14,30,48); }}"
            # Checked
            f"QPushButton:checked {{ color: {TEXT_AQUA_WHITE}; "
            f"background: qlineargradient(x1:0, y1:0, x2:0, y2:1, "
            f"stop:0 rgb(0,60,60), stop:0.5 rgb(0,44,48), stop:1 rgb(0,30,38)); "
            f"border: 1px solid rgba(0,229,204,0.55); }}"
            f"QPushButton:checked:hover {{ "
            f"background: qlineargradient(x1:0, y1:0, x2:0, y2:1, "
            f"stop:0 rgb(0,72,72), stop:0.5 rgb(0,54,58), stop:1 rgb(0,38,46)); }}"
        )

    def menu_css(self):
        return (
            f"QMenu {{ background: rgb(10,24,40); color: {TEXT_AQUA_WHITE}; "
            f"border: 1px solid rgb(18,40,65); border-radius: 5px; padding: 4px; "
            f"font-family: {self.font}; font-size: 11px; }}"
            "QMenu::item { padding: 5px 20px; border-radius: 3px; }"
            f"QMenu::item:selected {{ color: {TEXT_AQUA_WHITE}; "
            f"background: qlineargradient(x1:0, y1:0, x2:0, y2:1, "
            f"stop:0 rgb(0,70,65), stop:0.5 rgb(0,50,50), stop:1 rgb(0,35,40)); }}"
            f"QMenu::separator {{ height: 1px; background: rgb(18,40,65); margin: 4px 8px; }}"
        )

    def scrollbar_css(self):
        return (
            f"QScrollBar:vertical {{ width: 12px; background: rgb(10,24,40); "
            f"border: none; border-radius: 6px; margin: 2px; }}"
            "QScrollBar::handle:vertical { "
            "background: qlineargradient(x1:0, y1:0, x2:1, y2:0, "
            "stop:0 rgb(18,50,65), stop:0.5 rgb(0,80,75), stop:1 rgb(18,50,65)); "
            "border: 1px solid rgb(12,35,52); border-radius: 6px; min-height: 30px; margin: 0px; }"
            "QScrollBar::handle:vertical:hover { "
            "background: qlineargradient(x1:0, y1:0, x2:1, y2:0, "
            "stop:0 rgb(22,60,78), stop:0.5 rgb(0,110,100), stop:1 rgb(22,60,78)); }"
            "QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical { height: 0; }"
            "QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical { background: transparent; }"
        )

    def panel_bg_css(self):
        return (
            f"background: qlineargradient(x1:0, y1:0, x2:0, y2:1, "
            f"stop:0 rgb(21,48,74), stop:0.5 rgb(14,34,54), stop:1 rgb(10,24,40)); "
            f"border: 1px solid {BORDER_DEEP}; border-radius: 5px;"
        )

    def panel_bg_flat_css(self):
        return (
            f"background: rgba(10,24,40,230); "
            f"border: 1px solid {BORDER_DEEP}; border-radius: 5px;"
        )

    # ------------------------------------------------------------------
    #  Procedural caustic texture generation
    # ------------------------------------------------------------------

    def _get_caustic_texture(self, width=256, height=256):
        """Return cached caustic light texture as QPixmap."""
        if UnderwaterStyle._caustic_cache is not None:
            return UnderwaterStyle._caustic_cache
        UnderwaterStyle._caustic_cache = get_cached_texture(
            "underwater_caustic", width, height,
            lambda: self._generate_caustic_texture(width, height),
        )
        return UnderwaterStyle._caustic_cache

    def _generate_caustic_texture(self, width, height):
        """
        Generate tileable caustic light network texture.

        Caustics form when light refracts through a wavy water surface and
        concentrates along bright web-like ridges on the sea floor. We use
        axis-aligned sine gratings at integer frequencies (guaranteeing seamless
        tiling) multiplied together, then a power curve to concentrate
        brightness into thin bright ridges.

        Returns:
            QPixmap -- RGBA image: bright cyan-white caustic pattern on
            transparent black, suitable for additive blending.
        """
        from scipy.ndimage import gaussian_filter

        np.random.seed(7777)

        # Coordinate grids (0..2pi, seamless when freq is integer)
        ys = np.linspace(0, 2 * np.pi, height, endpoint=False)
        xs = np.linspace(0, 2 * np.pi, width,  endpoint=False)
        xg, yg = np.meshgrid(xs, ys)

        # Axis-aligned gratings at integer frequencies tile perfectly.
        # Mix of horizontal and vertical waves at different frequencies
        # creates a convincing caustic web pattern.
        layers = [
            (np.sin(xg * 3 + 0.0) + 1.0) * 0.5,
            (np.sin(yg * 3 + 1.1) + 1.0) * 0.5,
            (np.sin(xg * 5 + 2.3) + 1.0) * 0.5,
            (np.sin(yg * 4 + 0.7) + 1.0) * 0.5,
            (np.sin((xg + yg) * 2 + 0.5) + 1.0) * 0.5,  # diagonal (tiles: integer freq on sum)
            (np.sin((xg - yg) * 3 + 1.8) + 1.0) * 0.5,  # other diagonal
        ]

        combined = layers[0]
        for layer in layers[1:]:
            combined = combined * layer

        combined = (combined - combined.min()) / (combined.max() - combined.min() + 1e-9)

        # Power curve concentrates brightness into thin bright ridges
        caustic = combined ** 0.35

        # Detail pass — finer web lines using higher integer frequencies
        detail = (
            ((np.sin(xg * 7) + 1.0) * 0.5)
            * ((np.sin(yg * 6) + 1.0) * 0.5)
            * ((np.sin((xg + yg) * 4 + 1.0) + 1.0) * 0.5)
        )
        detail = (detail - detail.min()) / (detail.max() - detail.min() + 1e-9)
        detail = detail ** 0.4

        # Blend primary and detail
        caustic = caustic * 0.7 + detail * 0.3
        caustic = (caustic - caustic.min()) / (caustic.max() - caustic.min() + 1e-9)

        # Soft gaussian blur (wrap mode for seamless edges)
        caustic = gaussian_filter(caustic, sigma=1.2, mode='wrap')

        caustic = (caustic - caustic.min()) / (caustic.max() - caustic.min() + 1e-9)

        # Build RGBA: cyan-white bright areas on transparent dark
        img = np.zeros((height, width, 4), dtype=np.uint8)
        brightness = (caustic * 255).astype(np.uint8)
        img[:, :, 0] = np.clip(brightness * 0.75 + 40, 0, 255).astype(np.uint8)
        img[:, :, 1] = np.clip(brightness * 0.95 + 20, 0, 255).astype(np.uint8)
        img[:, :, 2] = brightness
        img[:, :, 3] = np.clip(brightness * 0.85, 0, 255).astype(np.uint8)

        qimg = QImage(img.data, width, height, width * 4, QImage.Format.Format_RGBA8888).copy()
        return QPixmap.fromImage(qimg)

    # ------------------------------------------------------------------
    #  Drawing helpers
    # ------------------------------------------------------------------

    def _draw_bubble(self, painter, x, y, radius, alpha_mult=1.0):
        """
        Draw a deep-sea bubble with specular highlight and blue-green tint.

        More elaborate than the base version: adds a distinct specular dot
        offset to the upper-left and a subtle rim glow.
        """
        # Main body gradient
        center = QPointF(x + radius, y + radius)
        highlight_center = QPointF(x + radius * 0.55, y + radius * 0.55)
        grad = QRadialGradient(highlight_center, radius * 1.4)
        grad.setColorAt(0.0, QColor(255, 255, 255, int(220 * alpha_mult)))
        grad.setColorAt(0.15, QColor(180, 240, 235, int(160 * alpha_mult)))
        grad.setColorAt(0.4, QColor(80, 200, 220, int(100 * alpha_mult)))
        grad.setColorAt(0.7, QColor(30, 120, 160, int(60 * alpha_mult)))
        grad.setColorAt(1.0, QColor(10, 60, 100, int(20 * alpha_mult)))

        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(QBrush(grad))
        painter.drawEllipse(int(x), int(y), int(radius * 2), int(radius * 2))

        # Rim highlight (thin bright edge at bottom-right suggesting refraction)
        if radius >= 4:
            rim = QRadialGradient(
                QPointF(x + radius * 1.3, y + radius * 1.3),
                radius * 0.6,
            )
            rim.setColorAt(0.0, QColor(200, 255, 255, int(80 * alpha_mult)))
            rim.setColorAt(1.0, QColor(200, 255, 255, 0))
            painter.setBrush(QBrush(rim))
            painter.drawEllipse(int(x), int(y), int(radius * 2), int(radius * 2))

        # Specular dot (upper-left)
        if radius >= 3:
            spec_r = max(1.5, radius * 0.25)
            spec = QRadialGradient(
                QPointF(x + radius * 0.6, y + radius * 0.5),
                spec_r,
            )
            spec.setColorAt(0.0, QColor(255, 255, 255, int(255 * alpha_mult)))
            spec.setColorAt(1.0, QColor(255, 255, 255, 0))
            painter.setBrush(QBrush(spec))
            painter.drawEllipse(
                int(x + radius * 0.4), int(y + radius * 0.3),
                int(spec_r * 2), int(spec_r * 2),
            )

    def _draw_caustic_overlay(self, painter, rect, width, height,
                               alpha_top=0.38, alpha_bottom=0.05):
        """
        Tile the caustic texture over rect with vertical alpha fade.

        Light is strongest near the surface (top) and fades with depth (bottom).
        """
        caustic = self._get_caustic_texture()
        if caustic.isNull():
            return

        # Clip to the target rect
        painter.save()
        clip = QPainterPath()
        clip.addRoundedRect(QRectF(rect), self.corner_radius, self.corner_radius)
        painter.setClipPath(clip)

        # Draw tiled caustic texture at reduced opacity
        # We paint in horizontal strips with decreasing alpha from top to bottom
        strips = 12
        strip_h = max(1, height // strips)
        for i in range(strips):
            t = i / (strips - 1) if strips > 1 else 0
            alpha = alpha_top + (alpha_bottom - alpha_top) * t
            painter.setOpacity(alpha)
            strip_rect = QRectF(rect.x(), rect.y() + i * strip_h,
                                width, strip_h + 1)
            painter.drawTiledPixmap(strip_rect.toAlignedRect(), caustic)

        painter.setOpacity(1.0)
        painter.setClipping(False)
        painter.restore()

    def _draw_bioluminescence(self, painter, positions, alpha_mult=1.0):
        """
        Draw small bioluminescent glow spots at given (x, y, radius) positions.

        Each spot is a soft radial glow of cyan-teal, like a tiny deep-sea
        organism pulsing light.
        """
        painter.setPen(Qt.PenStyle.NoPen)
        for x, y, r in positions:
            glow = QRadialGradient(QPointF(x, y), r)
            glow.setColorAt(0.0, QColor(0, 229, 204, int(90 * alpha_mult)))
            glow.setColorAt(0.3, QColor(0, 200, 180, int(50 * alpha_mult)))
            glow.setColorAt(0.7, QColor(0, 140, 130, int(18 * alpha_mult)))
            glow.setColorAt(1.0, QColor(0, 80, 80, 0))
            painter.setBrush(QBrush(glow))
            painter.drawEllipse(QPointF(x, y), r, r)

    def _draw_vignette(self, painter, rect, width, height, radius=12):
        """Dark vignette -- deeper blue-black at edges and especially bottom."""
        # Horizontal vignette
        hgrad = QLinearGradient(0, 0, width, 0)
        for pos, alpha in [(0, 160), (0.12, 60), (0.3, 10), (0.7, 10), (0.88, 60), (1, 160)]:
            hgrad.setColorAt(pos, QColor(4, 10, 20, alpha))
        painter.setBrush(QBrush(hgrad))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawRoundedRect(rect, radius, radius)

        # Vertical vignette -- heavier at bottom (deeper = darker)
        vgrad = QLinearGradient(0, 0, 0, height)
        for pos, alpha in [(0, 40), (0.15, 10), (0.5, 20), (0.8, 80), (1, 200)]:
            vgrad.setColorAt(pos, QColor(4, 8, 16, alpha))
        painter.setBrush(QBrush(vgrad))
        painter.drawRoundedRect(rect, radius, radius)

    # ------------------------------------------------------------------
    #  paint_window
    # ------------------------------------------------------------------

    def paint_window(self, painter, rect, width, height, focused=True):
        """
        Paint deep ocean background with caustic light, bubbles, and
        bioluminescent glow.
        """
        radius = self.corner_radius
        alpha_mult = 1.0 if focused else 0.85

        # --- 1. Deep ocean gradient (top=surface blue, bottom=abyss) ---
        grad = QLinearGradient(0, rect.top(), 0, rect.bottom())
        grad.setColorAt(0.0, QColor(24, 58, 88, int(255 * alpha_mult)))   # near-surface
        grad.setColorAt(0.15, QColor(18, 44, 72, int(255 * alpha_mult)))
        grad.setColorAt(0.5, QColor(12, 32, 54, int(255 * alpha_mult)))
        grad.setColorAt(0.85, QColor(8, 22, 38, int(255 * alpha_mult)))
        grad.setColorAt(1.0, QColor(6, 14, 28, int(255 * alpha_mult)))    # deep abyss
        painter.setBrush(QBrush(grad))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawRoundedRect(rect, radius, radius)

        # --- 2. Surface shimmer at top (lighter band suggesting surface) ---
        shimmer = QLinearGradient(0, rect.top(), 0, rect.top() + 40)
        shimmer.setColorAt(0.0, QColor(60, 130, 160, int(55 * alpha_mult)))
        shimmer.setColorAt(0.4, QColor(40, 100, 140, int(30 * alpha_mult)))
        shimmer.setColorAt(1.0, QColor(20, 60, 100, 0))
        painter.setBrush(QBrush(shimmer))
        painter.drawRoundedRect(rect, radius, radius)

        # --- 3. Caustic light overlay (tileable, stronger at top) ---
        self._draw_caustic_overlay(
            painter, rect, width, height,
            alpha_top=0.32 * alpha_mult, alpha_bottom=0.04 * alpha_mult,
        )

        # --- 4. Bioluminescent glow spots ---
        np.random.seed(2049)
        biolum_spots = []
        for _ in range(6):
            bx = rect.x() + np.random.randint(20, max(21, width - 20))
            by = rect.y() + np.random.randint(int(height * 0.3), max(int(height * 0.3) + 1, height - 15))
            br = 8 + np.random.random() * 18
            biolum_spots.append((bx, by, br))
        self._draw_bioluminescence(painter, biolum_spots, alpha_mult)

        # --- 5. Decorative bubbles (various sizes, clustered near edges) ---
        np.random.seed(8888)
        bubble_defs = [
            # (x_offset_from_left, y_offset_from_bottom, radius)
            (14, 55, 11),
            (32, 32, 7),
            (48, 70, 5),
            (width - 40, 50, 10),
            (width - 22, 28, 6),
            (width - 55, 68, 4),
            # A few mid-field rising bubbles
            (int(width * 0.3), int(height * 0.6), 5),
            (int(width * 0.6), int(height * 0.45), 3),
            (int(width * 0.45), int(height * 0.75), 8),
            (int(width * 0.7), int(height * 0.8), 4),
        ]
        for bx, by_from_bottom, br in bubble_defs[:6]:
            self._draw_bubble(
                painter,
                rect.x() + bx,
                rect.bottom() - by_from_bottom,
                br, alpha_mult * 0.85,
            )
        for bx, by, br in bubble_defs[6:]:
            self._draw_bubble(
                painter, rect.x() + bx, rect.y() + by,
                br, alpha_mult * 0.6,
            )

        # --- 6. Vignette (darker at edges and bottom) ---
        self._draw_vignette(painter, rect, width, height, radius)

        # --- 7. Border ---
        painter.setBrush(Qt.BrushStyle.NoBrush)
        if focused:
            # Outer bioluminescent glow rings
            for i in range(3):
                ga = int((45 - i * 14) * alpha_mult)
                painter.setPen(QPen(QColor(0, 200, 190, ga), 2 + i * 2))
                painter.drawRoundedRect(rect.adjusted(-i, -i, i, i), radius + i, radius + i)
            painter.setPen(QPen(QColor(0, 229, 204, int(140 * alpha_mult)), 1.5))
            painter.drawRoundedRect(rect, radius, radius)
        else:
            painter.setPen(QPen(QColor(15, 40, 60, 120), 1))
            painter.drawRoundedRect(rect, radius, radius)

    # ------------------------------------------------------------------
    #  paint_waveform_panel
    # ------------------------------------------------------------------

    def paint_waveform_panel(self, painter, rect, w, h, cy):
        """
        Waveform panel -- deeper underwater grotto with faint caustics,
        bioluminescent grid lines, and decorative bubbles.
        """
        # --- Dark deep-water gradient ---
        panel_grad = QLinearGradient(0, 0, 0, h)
        panel_grad.setColorAt(0.0, QColor(8, 20, 34))
        panel_grad.setColorAt(0.3, QColor(6, 16, 28))
        panel_grad.setColorAt(0.7, QColor(5, 14, 24))
        panel_grad.setColorAt(1.0, QColor(4, 10, 18))
        painter.setBrush(QBrush(panel_grad))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawRoundedRect(rect, 6, 6)

        # --- Faint caustic overlay (light barely reaches this depth) ---
        caustic = self._get_caustic_texture()
        if not caustic.isNull():
            painter.save()
            clip = QPainterPath()
            clip.addRoundedRect(QRectF(rect), 6, 6)
            painter.setClipPath(clip)
            painter.setOpacity(0.06)
            painter.drawTiledPixmap(rect, caustic)
            painter.setOpacity(1.0)
            painter.setClipping(False)
            painter.restore()

        # --- Engraved shadows (underwater cave depth) ---
        for grad, adj in [
            (QLinearGradient(0, 0, 0, 14), rect.adjusted(1, 1, -1, -h + 15)),
            (QLinearGradient(0, 0, 10, 0), rect.adjusted(1, 1, -w + 11, -1)),
            (QLinearGradient(w, 0, w - 10, 0), rect.adjusted(w - 11, 1, -1, -1)),
        ]:
            grad.setColorAt(0, QColor(2, 6, 12, 200))
            grad.setColorAt(1, QColor(2, 6, 12, 0))
            painter.setBrush(QBrush(grad))
            painter.setPen(Qt.PenStyle.NoPen)
            painter.drawRoundedRect(adj, 5, 5)

        # --- Bioluminescent grid lines ---
        painter.setPen(QPen(QColor(0, 180, 165, 22), 1))
        for i in range(1, 4):
            y = int(h * i / 4)
            painter.drawLine(4, y, w - 4, y)

        # --- Small bioluminescent glow spots in corners ---
        corner_biolum = [
            (12, h - 12, 6),
            (w - 12, 12, 5),
        ]
        self._draw_bioluminescence(painter, corner_biolum, 0.5)

        # --- Decorative bubbles ---
        self._draw_bubble(painter, 6, h - 20, 5, 0.6)
        self._draw_bubble(painter, 18, h - 12, 3, 0.5)
        self._draw_bubble(painter, w - 24, h - 18, 4, 0.55)
        self._draw_bubble(painter, w - 12, h - 8, 2.5, 0.45)

        # --- Panel border ---
        painter.setBrush(Qt.BrushStyle.NoBrush)
        painter.setPen(QPen(QColor(12, 35, 55), 1.5))
        painter.drawRoundedRect(rect, 6, 6)

        # --- Inner subtle highlight at top ---
        painter.setPen(QPen(QColor(0, 160, 150, 30), 1))
        painter.drawLine(rect.x() + 4, rect.y() + 1, rect.x() + w - 4, rect.y() + 1)

        # --- Center line in bioluminescent cyan ---
        painter.setPen(QPen(QColor(0, 229, 204, 55), 1))
        painter.drawLine(0, int(cy), w, int(cy))
