"""Weathered Copper style - aged patina aesthetic like the Statue of Liberty.

Procedural copper surface with brushed metal base, verdigris patina overlay,
tarnish patches, drip stains, and copper rivets. The sister theme to rust_grunge
but in copper/verdigris tones instead of rust/metal.
"""

import math
import numpy as np
from PyQt6.QtCore import Qt, QRectF, QPointF
from PyQt6.QtGui import (
    QColor, QLinearGradient, QRadialGradient, QBrush, QImage, QPixmap,
    QPainterPath, QPen
)

from .base import BaseStyle, get_cached_texture


# Copper color palette
COPPER_FRESH = "rgb(212, 128, 90)"
COPPER_MID = "rgb(139, 90, 58)"
COPPER_DARK = "rgb(90, 56, 37)"
COPPER_DEEP = "rgb(58, 36, 24)"

# Verdigris (patina) colors
VERDIGRIS_LIGHT = "rgb(124, 196, 170)"
VERDIGRIS_MID = "rgb(74, 158, 136)"
VERDIGRIS_DARK = "rgb(42, 110, 90)"
VERDIGRIS_DEEP = "rgb(26, 56, 48)"

# Text colors - warm cream on dark copper
TEXT_CREAM = "rgb(255, 245, 224)"
TEXT_WARM = "rgb(232, 220, 200)"
TEXT_TARNISHED = "rgb(160, 144, 128)"
TEXT_DISABLED = "rgb(90, 78, 66)"

# Borders
BORDER_PATINA = "rgb(26, 56, 48)"
BORDER_COPPER = "rgb(42, 24, 16)"
BORDER_LIGHT = "rgb(120, 80, 55)"

# Accent - verdigris green IS the accent
VERDIGRIS_ACCENT = QColor(46, 196, 182)
VERDIGRIS_ACCENT_CSS = "rgb(46, 196, 182)"
VERDIGRIS_DIM = "rgba(80, 200, 176, 0.7)"


class WeatheredCopperStyle(BaseStyle):
    name = "weathered_copper"
    font = "Palatino"

    _copper_cache = None

    # Verdigris accent
    accent = VERDIGRIS_ACCENT
    accent_css = VERDIGRIS_ACCENT_CSS
    text_primary = TEXT_CREAM
    text_secondary = TEXT_WARM
    text_muted = TEXT_TARNISHED
    text_error = "rgb(224, 96, 64)"
    text_link = "rgb(80, 200, 176)"
    border_color = BORDER_COPPER
    border_dark = BORDER_COPPER
    icon_color_dark = '#2ec4b6'
    icon_color_light = '#7cc4aa'
    icon_color_muted = '#4a6e5a'

    # Input fields
    input_bg = '#2a1810'
    input_text = '#fff5e0'

    # Slider - verdigris groove on dark copper
    slider_groove = "rgba(42, 110, 90, 0.6)"
    slider_handle = "rgb(46, 196, 182)"
    slider_fill = "rgb(74, 158, 136)"

    # Rotary knob - polished brass (matches copper metallic surface)
    knob_style = "brass"
    knob_body_dark = "#3a2418"
    knob_body_light = "#8b5a3a"
    knob_notch_style = "needle"
    knob_tickmarks = True
    knob_glow = False
    knob_track_color = "#2ec4b6"
    knob_label_color = "#fff5e0"

    # Waveform - verdigris green
    waveform_color = VERDIGRIS_ACCENT
    waveform_glow = False
    waveform_center_line = QColor(210, 170, 100, 60)
    waveform_panel = "dark"

    # Timer - amber on copper
    timer_use_lcd = True
    timer_color = QColor(210, 170, 100)

    # Transcription - dark copper panel
    transcription_text = TEXT_CREAM
    transcription_text_dimmed = VERDIGRIS_DIM
    transcription_panel_bg = COPPER_DEEP
    transcription_panel_border = BORDER_COPPER
    transcription_row_hover = "rgba(46, 196, 182, 0.1)"
    transcription_row_btn_bg = "rgba(46, 196, 182, 0.12)"
    transcription_row_btn_hover = "rgba(46, 196, 182, 0.22)"
    transcription_row_btn_pressed = "rgba(46, 196, 182, 0.35)"

    # Chime editor - copper/patina
    chime_grid_bg = QColor(45, 28, 20)
    chime_grid_line = QColor(70, 50, 40)
    chime_cell_inactive = QColor(55, 38, 28)
    chime_cell_active = QColor(46, 196, 182)
    chime_cell_highlight = QColor(46, 196, 182, 90)
    chime_piano_white = QColor(235, 225, 205)
    chime_piano_black = QColor(42, 28, 20)
    chime_piano_label_white = QColor(70, 50, 38)
    chime_piano_label_black = QColor(200, 190, 165)

    def button_css(self):
        return (
            f"QPushButton {{ color: {TEXT_WARM}; "
            f"background: qlineargradient(x1:0, y1:0, x2:0, y2:1, "
            f"stop:0 {COPPER_MID}, stop:0.3 {COPPER_DARK}, stop:0.7 {COPPER_DEEP}, stop:1 {COPPER_DARK}); "
            f"border: 2px solid {BORDER_COPPER}; border-top-color: {BORDER_LIGHT}; "
            f"border-radius: 3px; padding: 3px 8px; font-size: 11px; font-family: {self.font}; "
            f"text-align: left; }}"
            # Hover: verdigris glow
            f"QPushButton:hover {{ color: {VERDIGRIS_ACCENT_CSS}; "
            f"background: qlineargradient(x1:0, y1:0, x2:0, y2:1, "
            f"stop:0 rgb(85, 75, 55), stop:0.3 rgb(65, 55, 40), stop:0.7 rgb(48, 42, 32), stop:1 rgb(65, 55, 40)); "
            f"border: 2px solid {VERDIGRIS_DARK}; }}"
            # Pressed: deeper, tarnished
            f"QPushButton:pressed {{ color: {TEXT_CREAM}; "
            f"background: qlineargradient(x1:0, y1:0, x2:0, y2:1, "
            f"stop:0 rgb(38, 30, 22), stop:0.3 rgb(48, 38, 28), stop:0.7 rgb(55, 42, 32), stop:1 rgb(48, 38, 28)); "
            f"border: 2px solid rgb(60, 90, 80); }}"
            # Disabled
            f"QPushButton:disabled {{ color: {TEXT_DISABLED}; "
            f"background: {COPPER_DEEP}; border: 2px solid {BORDER_COPPER}; }}"
            # Checked - verdigris active
            f"QPushButton:checked {{ color: {TEXT_CREAM}; "
            f"background: qlineargradient(x1:0, y1:0, x2:0, y2:1, "
            f"stop:0 rgb(50, 120, 105), stop:0.3 rgb(40, 100, 88), stop:0.7 rgb(32, 80, 70), stop:1 rgb(40, 100, 88)); "
            f"border: 2px solid {VERDIGRIS_ACCENT_CSS}; }}"
            f"QPushButton:checked:hover {{ "
            f"background: qlineargradient(x1:0, y1:0, x2:0, y2:1, "
            f"stop:0 rgb(60, 140, 120), stop:0.3 rgb(50, 120, 105), stop:0.7 rgb(40, 100, 88), stop:1 rgb(50, 120, 105)); }}"
        )

    def menu_css(self):
        return (
            f"QMenu {{ background: {COPPER_DEEP}; color: {TEXT_CREAM}; "
            f"border: 2px solid {BORDER_PATINA}; border-radius: 4px; padding: 4px; "
            f"font-family: {self.font}; font-size: 11px; }}"
            "QMenu::item { padding: 4px 16px; border-radius: 2px; }"
            f"QMenu::item:selected {{ color: {TEXT_CREAM}; "
            f"background: qlineargradient(x1:0, y1:0, x2:0, y2:1, "
            f"stop:0 rgb(50, 120, 105), stop:0.5 rgb(40, 100, 88), stop:1 rgb(32, 80, 70)); }}"
            f"QMenu::separator {{ height: 2px; background: {BORDER_COPPER}; margin: 4px 8px; }}"
        )

    def _scrollbar_vertical_css(self):
        return (
            f"QScrollBar:vertical {{ width: 14px; background: {COPPER_DEEP}; "
            f"border: 1px solid {BORDER_COPPER}; border-radius: 5px; margin: 0px; }}"
            # Handle - copper pipe
            "QScrollBar::handle:vertical { "
            "background: qlineargradient(x1:0, y1:0, x2:1, y2:0, "
            "stop:0.0 rgb(100, 60, 40), stop:0.2 rgb(140, 85, 55), "
            "stop:0.5 rgb(170, 105, 70), stop:0.8 rgb(140, 85, 55), stop:1.0 rgb(100, 60, 40)); "
            f"border: 1px solid rgb(80, 50, 32); border-radius: 4px; min-height: 40px; margin: 2px; }}"
            # Handle hover - brighter copper
            "QScrollBar::handle:vertical:hover { "
            "background: qlineargradient(x1:0, y1:0, x2:1, y2:0, "
            "stop:0.0 rgb(140, 85, 55), stop:0.2 rgb(180, 110, 75), "
            "stop:0.5 rgb(210, 130, 90), stop:0.8 rgb(180, 110, 75), stop:1.0 rgb(140, 85, 55)); "
            "border: 1px solid rgb(120, 75, 48); }"
            # Handle pressed
            "QScrollBar::handle:vertical:pressed { "
            "background: qlineargradient(x1:0, y1:0, x2:1, y2:0, "
            "stop:0.0 rgb(75, 45, 30), stop:0.2 rgb(100, 60, 40), "
            "stop:0.5 rgb(120, 75, 50), stop:0.8 rgb(100, 60, 40), stop:1.0 rgb(75, 45, 30)); "
            "border: 1px solid rgb(55, 35, 22); }"
            "QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical { "
            "height: 0; width: 0; background: none; border: none; }"
            "QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical { background: transparent; }"
        )

    def panel_bg_css(self):
        return (
            f"background: qlineargradient(x1:0, y1:0, x2:0, y2:1, "
            f"stop:0 {COPPER_DARK}, stop:0.02 {COPPER_DEEP}, "
            f"stop:0.98 {COPPER_DEEP}, stop:1 rgb(30, 18, 12)); "
            f"border: 2px solid {BORDER_COPPER}; border-radius: 4px;"
        )

    def panel_bg_flat_css(self):
        return (
            f"background: {COPPER_DEEP}; border: 2px solid {BORDER_COPPER}; border-radius: 4px;"
        )

    # ── Texture generation ───────────────────────────────────────────

    def get_background_pixmap(self, height=512):
        """Procedural copper texture with verdigris patina and tarnish."""
        if WeatheredCopperStyle._copper_cache is not None:
            return WeatheredCopperStyle._copper_cache

        width = 256
        WeatheredCopperStyle._copper_cache = get_cached_texture(
            "weathered_copper", width, height,
            lambda: self._generate_copper_texture(width, height)
        )
        return WeatheredCopperStyle._copper_cache

    def _generate_copper_texture(self, width, height):
        """Generate procedural copper texture with verdigris patina overlay.

        Layers (bottom to top):
        1. Brushed copper metal base with specular highlights
        2. Tarnish darkening from fractal noise
        3. Verdigris patina overlay with organic edges
        4. Patina drip stain patterns (vertical accumulation)
        """
        from scipy.ndimage import gaussian_filter, uniform_filter1d

        np.random.seed(1886)  # Statue of Liberty dedication year

        # === SEAMLESS FRACTAL NOISE (tileable) ===
        def seamless_fractal_noise(h, w, octaves=4, persistence=0.5):
            """Generate seamless tileable fractal noise.

            Pure function (given fixed RNG state).

            Args:
                h (int): Height in pixels
                w (int): Width in pixels
                octaves (int): Number of noise octaves
                persistence (float): Amplitude decay per octave

            Returns:
                np.ndarray: Normalized noise array shape (h, w), range [0, 1]

            Examples:
                >>> # seamless_fractal_noise(64, 64).shape
                # (64, 64)
            """
            noise = np.zeros((h, w), dtype=np.float32)
            amplitude = 1.0
            for octave in range(octaves):
                freq = 2 ** octave
                layer = np.zeros((h, w), dtype=np.float32)
                seed_h, seed_w = max(2, h // freq), max(2, w // freq)
                seed = np.random.random((seed_h, seed_w)).astype(np.float32)
                for y in range(h):
                    for x in range(w):
                        sy = (y / h) * seed_h
                        sx = (x / w) * seed_w
                        y0, x0 = int(sy) % seed_h, int(sx) % seed_w
                        y1, x1 = (y0 + 1) % seed_h, (x0 + 1) % seed_w
                        fy, fx = sy - int(sy), sx - int(sx)
                        layer[y, x] = (seed[y0, x0] * (1 - fx) * (1 - fy) +
                                       seed[y0, x1] * fx * (1 - fy) +
                                       seed[y1, x0] * (1 - fx) * fy +
                                       seed[y1, x1] * fx * fy)
                noise += layer * amplitude
                amplitude *= persistence
            return (noise - noise.min()) / (noise.max() - noise.min() + 1e-6)

        organic_noise = seamless_fractal_noise(height, width, octaves=5, persistence=0.6)

        # === BRUSHED COPPER BASE (horizontal streaks in warm tones) ===
        base_noise = np.random.randint(0, 35, size=(height, width)).astype(np.float32)
        copper_streaks = uniform_filter1d(base_noise, size=70, axis=1, mode='wrap')
        fine_streaks = uniform_filter1d(
            np.random.randint(0, 20, size=(height, width)).astype(np.float32),
            size=25, axis=1, mode='wrap'
        )
        copper_streaks = copper_streaks * 0.7 + fine_streaks * 0.3

        # === SPECULAR HIGHLIGHTS (bright reflective streaks on polished copper) ===
        highlight_noise = np.random.random((height, width))
        highlights = uniform_filter1d(highlight_noise, size=90, axis=1, mode='wrap')
        highlights = (highlights > 0.68).astype(np.float32) * 25

        # === DEEP PITTING (corrosion holes in the copper) ===
        pits = seamless_fractal_noise(height, width, octaves=2, persistence=0.3)
        pits = (pits > 0.87).astype(np.float32)
        pits = gaussian_filter(pits, sigma=1.2, mode='wrap') * 35

        # === TARNISH PATCHES (darker oxidized copper, pre-verdigris stage) ===
        tarnish_noise = seamless_fractal_noise(height, width, octaves=3, persistence=0.5)
        tarnish_threshold = 0.4 + organic_noise * 0.2
        tarnish_blobs = (tarnish_noise > tarnish_threshold).astype(np.float32)
        tarnish_blobs = gaussian_filter(tarnish_blobs, sigma=5, mode='wrap')

        # === VERDIGRIS PATINA MASK (the green oxidation layer) ===
        patina_noise = seamless_fractal_noise(height, width, octaves=4, persistence=0.55)
        # Patina heavier at top (rain weathers top more) and at edges
        y_gradient = np.linspace(0.7, 0.3, height)[:, None] * np.ones((1, width))
        edge_x = np.minimum(
            np.arange(width)[None, :],
            (width - 1 - np.arange(width))[None, :]
        ).astype(np.float32) / (width * 0.3)
        edge_bias = np.clip(1.0 - edge_x, 0, 0.3)

        patina_mask = patina_noise * 0.6 + organic_noise * 0.3 + y_gradient * 0.1 + edge_bias * 0.15
        patina_threshold = 0.52
        patina_blobs = (patina_mask > patina_threshold).astype(np.float32)
        patina_blobs = gaussian_filter(patina_blobs, sigma=4, mode='wrap')

        # === PATINA EDGE TRANSITIONS (where green meets copper) ===
        patina_edges = gaussian_filter(patina_blobs, sigma=2, mode='wrap')
        transition_zone = np.abs(patina_edges - 0.45) < 0.18
        transition_zone = transition_zone.astype(np.float32) * 0.6

        # === DRIP STAIN PATTERNS (verdigris drips running down) ===
        drip_seeds = seamless_fractal_noise(height, width, octaves=1, persistence=0.5) > 0.93
        drip_pattern = np.zeros((height, width), dtype=np.float32)
        for y in range(1, height):
            drip_pattern[y] = drip_pattern[y - 1] * 0.94 + drip_seeds[y] * 0.7
        # Wrap for seamlessness
        drip_pattern = (drip_pattern + np.roll(drip_pattern, height // 2, axis=0)) * 0.5
        drip_pattern = gaussian_filter(drip_pattern, sigma=(1, 3), mode='wrap')

        # === SCRATCHES AND WEAR ===
        scratches = seamless_fractal_noise(height, width, octaves=2, persistence=0.4)
        scratches = uniform_filter1d(scratches, size=18, axis=1, mode='wrap')
        scratches = (scratches > 0.76).astype(np.float32) * 18

        # === COMBINE: copper base colors ===
        metal_var = organic_noise * 12
        # Polished copper base: warm orange-pink (~180, 120, 80)
        copper_r = np.clip(155 + copper_streaks + metal_var + highlights - pits, 100, 215).astype(np.float32)
        copper_g = np.clip(95 + copper_streaks * 0.65 + metal_var * 0.7 + highlights * 0.7 - pits, 60, 140).astype(np.float32)
        copper_b = np.clip(65 + copper_streaks * 0.4 + metal_var * 0.4 + highlights * 0.5 - pits, 35, 100).astype(np.float32)

        # Apply tarnish darkening
        tarnish_factor = 1.0 - tarnish_blobs * 0.35
        copper_r *= tarnish_factor
        copper_g *= tarnish_factor
        copper_b *= tarnish_factor

        # Add scratches (bright exposed copper underneath)
        copper_r = np.clip(copper_r + scratches, 0, 220)
        copper_g = np.clip(copper_g + scratches * 0.6, 0, 145)
        copper_b = np.clip(copper_b + scratches * 0.35, 0, 105)

        # === VERDIGRIS COLORS (green-blue-turquoise with variation) ===
        patina_var = organic_noise * 30
        verd_r = np.clip(55 + patina_var * 0.4 + transition_zone * 40, 35, 130).astype(np.float32)
        verd_g = np.clip(140 + patina_var * 0.8, 100, 200).astype(np.float32)
        verd_b = np.clip(120 + patina_var * 0.6, 85, 175).astype(np.float32)

        # Combine patina layers: direct patina + drip stains
        total_patina = np.clip(patina_blobs + drip_pattern * 0.5, 0, 1)

        # === FINAL BLEND ===
        img = np.zeros((height, width, 4), dtype=np.uint8)
        img[:, :, 0] = np.clip(copper_r * (1 - total_patina) + verd_r * total_patina, 0, 255).astype(np.uint8)
        img[:, :, 1] = np.clip(copper_g * (1 - total_patina) + verd_g * total_patina, 0, 255).astype(np.uint8)
        img[:, :, 2] = np.clip(copper_b * (1 - total_patina) + verd_b * total_patina, 0, 255).astype(np.uint8)
        img[:, :, 3] = 255

        qimg = QImage(img.data, width, height, width * 4, QImage.Format.Format_RGBA8888).copy()
        return QPixmap.fromImage(qimg)

    # ── Drawing helpers ──────────────────────────────────────────────

    def _draw_copper_bolt(self, painter, x, y, size=12):
        """Draw a hexagonal copper bolt with verdigris patina spots.

        Args:
            painter: QPainter instance
            x (float): Center x coordinate
            y (float): Center y coordinate
            size (int): Bolt diameter in pixels
        """
        # Hexagonal bolt head
        path = QPainterPath()
        for i in range(6):
            angle = math.pi / 3 * i - math.pi / 6
            px = x + size * 0.5 * math.cos(angle)
            py = y + size * 0.5 * math.sin(angle)
            if i == 0:
                path.moveTo(px, py)
            else:
                path.lineTo(px, py)
        path.closeSubpath()

        # Copper gradient for 3D effect
        grad = QRadialGradient(QPointF(x - size * 0.15, y - size * 0.15), size * 0.6)
        grad.setColorAt(0, QColor(195, 130, 85))   # Bright polished copper
        grad.setColorAt(0.4, QColor(150, 95, 60))   # Mid copper
        grad.setColorAt(0.8, QColor(100, 62, 40))   # Dark copper
        grad.setColorAt(1, QColor(65, 40, 28))       # Shadow

        painter.setBrush(QBrush(grad))
        painter.setPen(QPen(QColor(45, 28, 18), 1))
        painter.drawPath(path)

        # Verdigris patina spot on bolt (small green patch)
        patina_grad = QRadialGradient(QPointF(x + size * 0.12, y + size * 0.1), size * 0.25)
        patina_grad.setColorAt(0, QColor(70, 150, 130, 160))
        patina_grad.setColorAt(0.6, QColor(55, 130, 110, 100))
        patina_grad.setColorAt(1, QColor(55, 130, 110, 0))
        painter.setBrush(QBrush(patina_grad))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawEllipse(QPointF(x + size * 0.12, y + size * 0.1), size * 0.25, size * 0.22)

        # Slot in center (Phillips-style cross for copper bolts)
        painter.setPen(QPen(QColor(35, 22, 14), 1.5))
        painter.drawLine(int(x - size * 0.2), int(y), int(x + size * 0.2), int(y))
        painter.drawLine(int(x), int(y - size * 0.2), int(x), int(y + size * 0.2))

    def _draw_corner_bolts(self, painter, rect, margin=15, size=10):
        """Draw copper bolts in the four corners of a rectangle.

        Args:
            painter: QPainter instance
            rect: QRectF defining the area
            margin (int): Distance from corner to bolt center
            size (int): Bolt diameter
        """
        x, y, w, h = rect.x(), rect.y(), rect.width(), rect.height()
        for bx, by in [
            (x + margin, y + margin),
            (x + w - margin, y + margin),
            (x + margin, y + h - margin),
            (x + w - margin, y + h - margin),
        ]:
            self._draw_copper_bolt(painter, bx, by, size)

    def _draw_patina_drip(self, painter, x, y, length, width_base=5):
        """Draw a verdigris drip streak running downward.

        Like rain-carried patina running down a copper gutter.

        Args:
            painter: QPainter instance
            x (float): Top center x of the drip
            y (float): Top y of the drip
            length (float): Drip length in pixels
            width_base (int): Width at the drip origin
        """
        path = QPainterPath()
        path.moveTo(x - width_base / 2, y)
        path.lineTo(x + width_base / 2, y)
        # Slight wobble for organic feel
        path.quadTo(x + width_base / 3, y + length * 0.35,
                    x + width_base / 5, y + length * 0.6)
        path.lineTo(x, y + length)
        path.quadTo(x - width_base / 5, y + length * 0.55,
                    x - width_base / 3, y + length * 0.3)
        path.closeSubpath()

        grad = QLinearGradient(0, y, 0, y + length)
        grad.setColorAt(0, QColor(60, 145, 125, 180))
        grad.setColorAt(0.3, QColor(55, 135, 115, 140))
        grad.setColorAt(0.6, QColor(50, 125, 105, 90))
        grad.setColorAt(1, QColor(45, 115, 95, 25))

        painter.setBrush(QBrush(grad))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawPath(path)

    def _draw_vignette(self, painter, rect, width, height, radius=12):
        """Warm copper-toned edge darkening.

        Darker at edges like tarnish accumulating where copper meets frame.

        Args:
            painter: QPainter instance
            rect: QRectF for the area
            width (int): Rect width
            height (int): Rect height
            radius (int): Corner radius for rounded rect
        """
        for horizontal, alpha_mult in [(True, 0.7), (False, 1.0)]:
            grad = QLinearGradient(0, 0, width if horizontal else 0, 0 if horizontal else height)
            # Dark warm brown at edges (like tarnish in crevices)
            for pos, alpha in [(0, 200), (0.08, 110), (0.22, 45), (0.78, 45), (0.92, 110), (1, 200)]:
                grad.setColorAt(pos, QColor(25, 15, 8, int(alpha * alpha_mult)))
            painter.setBrush(QBrush(grad))
            painter.setPen(Qt.PenStyle.NoPen)
            painter.drawRoundedRect(rect, radius, radius)

    # ── Main paint methods ───────────────────────────────────────────

    def paint_window(self, painter, rect, width, height, focused=True):
        """Paint weathered copper background with patina, drips, and bolts."""
        radius = self.corner_radius

        # Clip to rounded rect
        path = QPainterPath()
        path.addRoundedRect(QRectF(rect), radius, radius)
        painter.setClipPath(path)

        # Draw copper texture (tiled)
        copper = self.get_background_pixmap(max(512, height))
        painter.drawTiledPixmap(rect, copper)
        painter.setClipping(False)

        # Warm copper vignette (tarnish at edges)
        self._draw_vignette(painter, rect, width, height, radius)

        # Verdigris drips from top edge (where rain collects)
        np.random.seed(1886)
        for i in range(6):
            drip_x = 25 + i * 55 + np.random.randint(-12, 12)
            drip_len = 18 + np.random.randint(12, 45)
            if drip_x < width - 20:
                self._draw_patina_drip(painter, drip_x, 2, drip_len)

        # A couple of drips from bottom of waveform area (mid-height)
        for i in range(3):
            drip_x = 60 + i * 90 + np.random.randint(-15, 15)
            drip_len = 12 + np.random.randint(8, 25)
            if drip_x < width - 20:
                self._draw_patina_drip(painter, drip_x, height * 0.35, drip_len, width_base=3)

        # Corner bolts
        self._draw_corner_bolts(painter, rect, margin=18, size=11)

        # Additional bolts along top edge
        for i in range(1, 4):
            bx = rect.x() + width * i / 4
            if abs(bx - rect.x() - 18) > 15 and abs(bx - (rect.x() + width - 18)) > 15:
                self._draw_copper_bolt(painter, bx, rect.y() + 18, 9)

        # Border - dark copper edge with patina tint
        if focused:
            painter.setBrush(Qt.BrushStyle.NoBrush)
            painter.setPen(QPen(QColor(65, 95, 85, 180), 2))
            painter.drawRoundedRect(rect, radius, radius)
        else:
            painter.setBrush(Qt.BrushStyle.NoBrush)
            painter.setPen(QPen(QColor(50, 40, 32, 120), 1.5))
            painter.drawRoundedRect(rect, radius, radius)

    def paint_waveform_panel(self, painter, rect, w, h, cy):
        """Dark recessed copper panel for waveform display.

        Features verdigris-tinted grid, engraved shadows where patina collects,
        and small copper corner bolts.
        """
        # Dark recessed copper panel
        panel_grad = QLinearGradient(0, 0, 0, h)
        panel_grad.setColorAt(0, QColor(30, 20, 14))
        panel_grad.setColorAt(0.1, QColor(40, 28, 20))
        panel_grad.setColorAt(0.9, QColor(35, 24, 17))
        panel_grad.setColorAt(1, QColor(25, 16, 11))
        painter.setBrush(QBrush(panel_grad))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawRoundedRect(rect, 6, 6)

        # Engraved shadows (patina accumulates in shadows/crevices)
        for grad, adj in [
            (QLinearGradient(0, 0, 0, 15), rect.adjusted(1, 1, -1, -h + 16)),
            (QLinearGradient(0, 0, 12, 0), rect.adjusted(1, 1, -w + 13, -1)),
            (QLinearGradient(w, 0, w - 12, 0), rect.adjusted(w - 13, 1, -1, -1)),
        ]:
            grad.setColorAt(0, QColor(0, 0, 0, 190))
            grad.setColorAt(1, QColor(0, 0, 0, 0))
            painter.setBrush(QBrush(grad))
            painter.setPen(Qt.PenStyle.NoPen)
            painter.drawRoundedRect(adj, 5, 5)

        # Verdigris-tinted grid lines
        painter.setPen(QPen(QColor(46, 196, 182, 25), 1))
        for i in range(1, 4):
            y = int(h * i / 4)
            painter.drawLine(5, y, w - 5, y)

        # Panel border - copper edge with slight green tint
        painter.setBrush(Qt.BrushStyle.NoBrush)
        painter.setPen(QPen(QColor(75, 58, 42), 2))
        painter.drawRoundedRect(rect, 6, 6)

        # Inner highlight - subtle patina shimmer
        painter.setPen(QPen(QColor(70, 110, 95, 60), 1))
        painter.drawRoundedRect(rect.adjusted(2, 2, -2, -2), 4, 4)

        # Small copper rivets in corners
        for corner in [(8, 8), (w - 8, 8), (8, h - 8), (w - 8, h - 8)]:
            self._draw_copper_bolt(painter, corner[0], corner[1], 6)

        # Center line - warm amber (exposed copper glow)
        painter.setPen(QPen(QColor(210, 170, 100, 60), 1))
        painter.drawLine(0, int(cy), w, int(cy))
