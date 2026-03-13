"""Rust Grunge style - broken-down car aesthetic with real rust textures and bolts."""

import numpy as np
from PyQt6.QtCore import Qt, QRectF, QPointF
from PyQt6.QtGui import (
    QColor, QLinearGradient, QRadialGradient, QBrush, QImage, QPixmap,
    QPainterPath, QPen
)

from .base import BaseStyle, get_cached_texture


# Rust color palette - earthy, corroded metal
RUST_DARK = "rgb(80, 40, 25)"
RUST_MID = "rgb(140, 65, 35)"
RUST_BRIGHT = "rgb(180, 85, 45)"
RUST_ORANGE = "rgb(200, 100, 50)"
RUST_ACCENT = "rgb(220, 120, 60)"

# Dark metal base (unpainted areas)
METAL_DARK = "rgb(35, 32, 30)"
METAL_MID = "rgb(55, 50, 45)"
METAL_LIGHT = "rgb(75, 68, 60)"

# Text colors - industrial stencil look
TEXT_BRIGHT = "rgb(220, 210, 195)"
TEXT_DIM = "rgba(180, 170, 155, 0.9)"
TEXT_MUTED = "rgb(130, 120, 105)"
TEXT_DISABLED = "rgb(70, 65, 58)"

# Borders - rusted metal edges
BORDER_RUST = "rgb(100, 55, 35)"
BORDER_DARK = "rgb(45, 40, 35)"
BORDER_LIGHT = "rgb(90, 80, 70)"

# Accent - hazard orange/amber
HAZARD_ORANGE = QColor(255, 140, 40)
HAZARD_ORANGE_CSS = "rgb(255, 140, 40)"
HAZARD_DIM = "rgba(200, 110, 40, 0.7)"


class RustGrungeStyle(BaseStyle):
    name = "rust_grunge"
    font = "Impact"  # Industrial stencil font

    _rust_cache = None
    _bolt_cache = None

    # Industrial dark theme
    accent = HAZARD_ORANGE
    accent_css = HAZARD_ORANGE_CSS
    text_primary = TEXT_BRIGHT
    text_secondary = TEXT_DIM
    text_muted = TEXT_MUTED
    text_error = "rgb(255, 100, 80)"
    text_link = HAZARD_ORANGE_CSS
    border_color = BORDER_RUST
    border_dark = BORDER_DARK
    icon_color_dark = '#ff8c28'  # Hazard orange icons
    icon_color_light = '#ffaa44'
    icon_color_muted = '#8b5a2b'

    # Slider - rust-colored groove on dark metal
    slider_groove = "rgba(140,65,35,0.6)"

    # Rotary knob - industrial gauge style
    knob_style = "industrial"
    knob_body_dark = "#302820"
    knob_body_light = "#5a4a38"
    knob_notch_style = "arrow"
    knob_tickmarks = True
    knob_glow = False
    knob_track_color = "#ff8c28"  # Hazard orange track
    knob_label_color = "#dcd0c0"  # Light tan text

    # Waveform - amber/orange on dark
    waveform_color = HAZARD_ORANGE
    waveform_glow = False  # Gritty, not glowy
    waveform_center_line = QColor(255, 140, 40, 50)
    waveform_panel = "dark"

    # Timer - amber LCD
    timer_use_lcd = True
    timer_color = HAZARD_ORANGE

    # Transcription - grungy panel
    transcription_text = TEXT_BRIGHT
    transcription_text_dimmed = HAZARD_DIM
    transcription_panel_bg = METAL_DARK
    transcription_panel_border = BORDER_DARK
    transcription_row_hover = "rgba(255, 140, 40, 0.1)"
    transcription_row_btn_bg = "rgba(255, 140, 40, 0.12)"
    transcription_row_btn_hover = "rgba(255, 140, 40, 0.22)"
    transcription_row_btn_pressed = "rgba(255, 140, 40, 0.35)"

    # Chime editor - rusty metal
    chime_grid_bg = QColor(45, 35, 30)  # Dark rust
    chime_grid_line = QColor(80, 60, 50)  # Rust border
    chime_cell_inactive = QColor(60, 45, 38)  # Medium rust
    chime_cell_active = QColor(255, 140, 60)  # Orange rust
    chime_cell_highlight = QColor(255, 140, 60, 90)  # Orange glow
    chime_piano_white = QColor(210, 195, 180)  # Aged ivory
    chime_piano_black = QColor(50, 40, 35)  # Dark rust
    chime_piano_label_white = QColor(80, 60, 50)  # Rust text
    chime_piano_label_black = QColor(200, 170, 150)  # Light rust text

    def button_css(self):
        # Industrial buttons - raised metal with rust
        return (
            f"QPushButton {{ color: {TEXT_DIM}; "
            f"background: qlineargradient(x1:0, y1:0, x2:0, y2:1, "
            f"stop:0 {METAL_LIGHT}, stop:0.3 {METAL_MID}, stop:0.7 {METAL_DARK}, stop:1 {METAL_MID}); "
            f"border: 2px solid {BORDER_DARK}; border-top-color: {BORDER_LIGHT}; "
            f"border-radius: 3px; padding: 3px 8px; font-size: 11px; font-family: {self.font}; "
            f"text-transform: uppercase; text-align: left; }}"
            # Hover: amber glow from behind
            f"QPushButton:hover {{ color: {HAZARD_ORANGE_CSS}; "
            f"background: qlineargradient(x1:0, y1:0, x2:0, y2:1, "
            f"stop:0 rgb(95, 75, 55), stop:0.3 rgb(75, 58, 42), stop:0.7 rgb(55, 42, 32), stop:1 rgb(75, 58, 42)); "
            f"border: 2px solid rgb(180, 100, 50); }}"
            # Pressed: deeper, more worn
            f"QPushButton:pressed {{ color: {TEXT_BRIGHT}; "
            f"background: qlineargradient(x1:0, y1:0, x2:0, y2:1, "
            f"stop:0 rgb(40, 35, 30), stop:0.3 rgb(50, 42, 35), stop:0.7 rgb(60, 50, 40), stop:1 rgb(50, 42, 35)); "
            f"border: 2px solid rgb(140, 75, 40); }}"
            # Disabled - heavily corroded
            f"QPushButton:disabled {{ color: {TEXT_DISABLED}; "
            f"background: {METAL_DARK}; border: 2px solid {BORDER_DARK}; }}"
            # Checked - active hazard
            f"QPushButton:checked {{ color: {TEXT_BRIGHT}; "
            f"background: qlineargradient(x1:0, y1:0, x2:0, y2:1, "
            f"stop:0 rgb(180, 90, 40), stop:0.3 rgb(150, 75, 35), stop:0.7 rgb(120, 60, 30), stop:1 rgb(150, 75, 35)); "
            f"border: 2px solid {HAZARD_ORANGE_CSS}; }}"
            f"QPushButton:checked:hover {{ "
            f"background: qlineargradient(x1:0, y1:0, x2:0, y2:1, "
            f"stop:0 rgb(200, 100, 45), stop:0.3 rgb(170, 85, 40), stop:0.7 rgb(140, 70, 35), stop:1 rgb(170, 85, 40)); }}"
        )

    def menu_css(self):
        return (
            f"QMenu {{ background: {METAL_DARK}; color: {TEXT_BRIGHT}; "
            f"border: 2px solid {BORDER_RUST}; border-radius: 4px; padding: 4px; "
            f"font-family: {self.font}; font-size: 12px; text-transform: uppercase; }}"
            "QMenu::item { padding: 4px 16px; border-radius: 2px; }"
            f"QMenu::item:selected {{ color: {TEXT_BRIGHT}; "
            f"background: qlineargradient(x1:0, y1:0, x2:0, y2:1, "
            f"stop:0 rgb(160, 80, 40), stop:0.5 rgb(140, 70, 35), stop:1 rgb(120, 60, 30)); }}"
            f"QMenu::separator {{ height: 2px; background: {BORDER_DARK}; margin: 4px 8px; }}"
        )

    def _scrollbar_vertical_css(self):
        # Rusty pipe scrollbar
        return (
            f"QScrollBar:vertical {{ width: 16px; background: {METAL_DARK}; "
            f"border: 1px solid {BORDER_DARK}; border-radius: 4px; margin: 0px; }}"
            # Handle - corroded metal
            "QScrollBar::handle:vertical { "
            "background: qlineargradient(x1:0, y1:0, x2:1, y2:0, "
            "stop:0.0 rgb(100, 55, 35), stop:0.2 rgb(140, 70, 40), "
            "stop:0.5 rgb(160, 80, 45), stop:0.8 rgb(140, 70, 40), stop:1.0 rgb(100, 55, 35)); "
            f"border: 1px solid rgb(80, 45, 28); border-radius: 4px; min-height: 40px; margin: 2px; }}"
            # Handle hover - warmer
            "QScrollBar::handle:vertical:hover { "
            "background: qlineargradient(x1:0, y1:0, x2:1, y2:0, "
            "stop:0.0 rgb(140, 75, 45), stop:0.2 rgb(180, 95, 55), "
            "stop:0.5 rgb(200, 105, 60), stop:0.8 rgb(180, 95, 55), stop:1.0 rgb(140, 75, 45)); "
            "border: 1px solid rgb(120, 65, 38); }"
            # Handle pressed
            "QScrollBar::handle:vertical:pressed { "
            "background: qlineargradient(x1:0, y1:0, x2:1, y2:0, "
            "stop:0.0 rgb(80, 45, 28), stop:0.2 rgb(110, 60, 35), "
            "stop:0.5 rgb(130, 70, 40), stop:0.8 rgb(110, 60, 35), stop:1.0 rgb(80, 45, 28)); "
            "border: 1px solid rgb(60, 35, 22); }"
            "QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical { "
            "height: 0; width: 0; background: none; border: none; }"
            "QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical { background: transparent; }"
        )

    def panel_bg_css(self):
        return (
            f"background: qlineargradient(x1:0, y1:0, x2:0, y2:1, "
            f"stop:0 {METAL_LIGHT}, stop:0.02 {METAL_DARK}, "
            f"stop:0.98 {METAL_DARK}, stop:1 rgb(25, 22, 20)); "
            f"border: 2px solid {BORDER_DARK}; border-radius: 4px;"
        )

    def panel_bg_flat_css(self):
        return (
            f"background: {METAL_DARK}; border: 2px solid {BORDER_DARK}; border-radius: 4px;"
        )

    def get_background_pixmap(self, height=512):
        """Procedural rust texture with corrosion, brushed metal, and seamless tiling."""
        if RustGrungeStyle._rust_cache is not None:
            return RustGrungeStyle._rust_cache

        width = 256
        RustGrungeStyle._rust_cache = get_cached_texture(
            "rust", width, height, lambda: self._generate_rust_texture(width, height)
        )
        return RustGrungeStyle._rust_cache

    def _generate_rust_texture(self, width, height):
        """Generate the rust texture (called on cache miss)."""
        from scipy.ndimage import gaussian_filter, uniform_filter1d

        np.random.seed(1337)

        # === SEAMLESS FRACTAL NOISE (tileable) ===
        def seamless_fractal_noise(h, w, octaves=4, persistence=0.5):
            """Generate seamless tileable fractal noise."""
            noise = np.zeros((h, w), dtype=np.float32)
            amplitude = 1.0
            for octave in range(octaves):
                freq = 2 ** octave
                # Create seamless base layer using modular coordinates
                layer = np.zeros((h, w), dtype=np.float32)
                # Generate small tileable seed
                seed_h, seed_w = max(2, h // freq), max(2, w // freq)
                seed = np.random.random((seed_h, seed_w)).astype(np.float32)
                # Tile and interpolate
                for y in range(h):
                    for x in range(w):
                        # Bilinear interpolation with wrapping
                        sy = (y / h) * seed_h
                        sx = (x / w) * seed_w
                        y0, x0 = int(sy) % seed_h, int(sx) % seed_w
                        y1, x1 = (y0 + 1) % seed_h, (x0 + 1) % seed_w
                        fy, fx = sy - int(sy), sx - int(sx)
                        layer[y, x] = (seed[y0, x0] * (1-fx) * (1-fy) +
                                      seed[y0, x1] * fx * (1-fy) +
                                      seed[y1, x0] * (1-fx) * fy +
                                      seed[y1, x1] * fx * fy)
                noise += layer * amplitude
                amplitude *= persistence
            return (noise - noise.min()) / (noise.max() - noise.min() + 1e-6)

        organic_noise = seamless_fractal_noise(height, width, octaves=5, persistence=0.6)

        # === BRUSHED METAL BASE (seamless horizontal streaks) ===
        # Use wrap mode for seamless tiling
        base_noise = np.random.randint(0, 40, size=(height, width)).astype(np.float32)
        metal_streaks = uniform_filter1d(base_noise, size=80, axis=1, mode='wrap')
        # Add finer detail streaks
        fine_streaks = uniform_filter1d(np.random.randint(0, 25, size=(height, width)).astype(np.float32),
                                        size=30, axis=1, mode='wrap')
        metal_streaks = metal_streaks * 0.7 + fine_streaks * 0.3

        # === SPECULAR HIGHLIGHTS for brushed metal ===
        highlight_noise = np.random.random((height, width))
        highlights = uniform_filter1d(highlight_noise, size=100, axis=1, mode='wrap')
        highlights = (highlights > 0.7).astype(np.float32) * 20  # Bright streaks

        # === DEEP PITTING / CORROSION HOLES (seamless) ===
        pits = seamless_fractal_noise(height, width, octaves=2, persistence=0.3)
        pits = (pits > 0.85).astype(np.float32)
        pits = gaussian_filter(pits, sigma=1.5, mode='wrap') * 40

        # === RUST PATCHES - organic shapes from fractal noise ===
        rust_threshold = 0.45 + organic_noise * 0.25
        rust_blobs = (organic_noise > rust_threshold).astype(np.float32)
        rust_blobs = gaussian_filter(rust_blobs, sigma=4, mode='wrap')

        # === PAINT PEELING EDGES - where rust meets metal ===
        rust_edges = gaussian_filter(rust_blobs, sigma=2, mode='wrap')
        paint_peel = np.abs(rust_edges - 0.5) < 0.15
        paint_peel = paint_peel.astype(np.float32) * 0.7

        # === OXIDATION STAINS - drip patterns (seamless vertically) ===
        stain_seeds = seamless_fractal_noise(height, width, octaves=1, persistence=0.5) > 0.95
        stain_pattern = np.zeros((height, width), dtype=np.float32)
        for y in range(1, height):
            stain_pattern[y] = stain_pattern[y-1] * 0.92 + stain_seeds[y] * 0.8
        # Wrap stain pattern for seamlessness
        stain_pattern = (stain_pattern + np.roll(stain_pattern, height//2, axis=0)) * 0.5
        stain_pattern = gaussian_filter(stain_pattern, sigma=(1, 4), mode='wrap')

        # === SCRATCHES AND WEAR (seamless) ===
        scratches = seamless_fractal_noise(height, width, octaves=2, persistence=0.4)
        scratches = uniform_filter1d(scratches, size=20, axis=1, mode='wrap')
        scratches = (scratches > 0.75).astype(np.float32) * 15

        # Combine rust layers with organic variation
        rust_intensity = rust_blobs + stain_pattern * 0.4 + organic_noise * 0.2
        rust_mask = np.clip(rust_intensity, 0, 1)

        # Create RGB channels
        img = np.zeros((height, width, 4), dtype=np.uint8)

        # Base metal color (dark gray-brown) with brushed metal variation
        metal_var = organic_noise * 15
        metal_r = np.clip(38 + metal_streaks + metal_var + highlights - pits, 20, 75).astype(np.uint8)
        metal_g = np.clip(35 + metal_streaks * 0.9 + metal_var * 0.8 + highlights * 0.9 - pits, 18, 68).astype(np.uint8)
        metal_b = np.clip(32 + metal_streaks * 0.8 + metal_var * 0.6 + highlights * 0.8 - pits, 15, 58).astype(np.uint8)

        # Rust color with organic variation (orange-brown, more varied)
        rust_var = organic_noise * 40
        rust_r = np.clip(130 + rust_var + scratches, 90, 200).astype(np.uint8)
        rust_g = np.clip(60 + rust_var * 0.5 + paint_peel * 30, 40, 110).astype(np.uint8)
        rust_b = np.clip(30 + rust_var * 0.25, 20, 60).astype(np.uint8)

        # Blend metal and rust based on mask
        img[:, :, 0] = (metal_r * (1 - rust_mask) + rust_r * rust_mask).astype(np.uint8)
        img[:, :, 1] = (metal_g * (1 - rust_mask) + rust_g * rust_mask).astype(np.uint8)
        img[:, :, 2] = (metal_b * (1 - rust_mask) + rust_b * rust_mask).astype(np.uint8)
        img[:, :, 3] = 255

        qimg = QImage(img.data, width, height, width * 4, QImage.Format.Format_RGBA8888).copy()
        return QPixmap.fromImage(qimg)

    def _draw_bolt(self, painter, x, y, size=12):
        """Draw a hexagonal bolt/rivet."""
        # Bolt head - hexagonal
        path = QPainterPath()
        import math
        for i in range(6):
            angle = math.pi / 3 * i - math.pi / 6
            px = x + size * 0.5 * math.cos(angle)
            py = y + size * 0.5 * math.sin(angle)
            if i == 0:
                path.moveTo(px, py)
            else:
                path.lineTo(px, py)
        path.closeSubpath()

        # Gradient for 3D effect
        grad = QRadialGradient(QPointF(x - size * 0.15, y - size * 0.15), size * 0.6)
        grad.setColorAt(0, QColor(120, 110, 95))
        grad.setColorAt(0.5, QColor(80, 72, 62))
        grad.setColorAt(1, QColor(50, 45, 38))

        painter.setBrush(QBrush(grad))
        painter.setPen(QPen(QColor(35, 32, 28), 1))
        painter.drawPath(path)

        # Slot in center
        painter.setPen(QPen(QColor(25, 22, 18), 2))
        painter.drawLine(int(x - size * 0.25), int(y), int(x + size * 0.25), int(y))

    def _draw_corner_bolts(self, painter, rect, margin=15, size=10):
        """Draw bolts in corners of a rectangle."""
        x, y, w, h = rect.x(), rect.y(), rect.width(), rect.height()
        corners = [
            (x + margin, y + margin),
            (x + w - margin, y + margin),
            (x + margin, y + h - margin),
            (x + w - margin, y + h - margin),
        ]
        for bx, by in corners:
            self._draw_bolt(painter, bx, by, size)

    def _draw_vignette(self, painter, rect, width, height, radius=12):
        """Dark corroded edges."""
        for horizontal, alpha_mult in [(True, 0.7), (False, 1.0)]:
            grad = QLinearGradient(0, 0, width if horizontal else 0, 0 if horizontal else height)
            # Heavier vignette - more worn at edges
            for pos, alpha in [(0, 180), (0.08, 100), (0.2, 40), (0.8, 40), (0.92, 100), (1, 180)]:
                grad.setColorAt(pos, QColor(0, 0, 0, int(alpha * alpha_mult)))
            painter.setBrush(QBrush(grad))
            painter.setPen(Qt.PenStyle.NoPen)
            painter.drawRoundedRect(rect, radius, radius)

    def _draw_rust_drip(self, painter, x, y, length, width_base=4):
        """Draw a rust drip/streak running down."""
        path = QPainterPath()
        path.moveTo(x - width_base / 2, y)
        path.lineTo(x + width_base / 2, y)
        path.lineTo(x + width_base / 4, y + length * 0.6)
        path.lineTo(x, y + length)
        path.lineTo(x - width_base / 4, y + length * 0.6)
        path.closeSubpath()

        grad = QLinearGradient(0, y, 0, y + length)
        grad.setColorAt(0, QColor(120, 60, 35, 200))
        grad.setColorAt(0.5, QColor(100, 50, 30, 150))
        grad.setColorAt(1, QColor(80, 40, 25, 50))

        painter.setBrush(QBrush(grad))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawPath(path)

    def paint_window(self, painter, rect, width, height, focused=True):
        """Paint rust texture background with bolts and drips."""
        radius = self.corner_radius

        # Clip to rounded rect
        path = QPainterPath()
        path.addRoundedRect(QRectF(rect), radius, radius)
        painter.setClipPath(path)

        # Draw rust texture
        rust = self.get_background_pixmap(max(512, height))
        painter.drawTiledPixmap(rect, rust)
        painter.setClipping(False)

        # Heavy vignette for worn edges
        self._draw_vignette(painter, rect, width, height, radius)

        # Rust drips from top
        np.random.seed(42)
        for i in range(5):
            drip_x = 30 + i * 60 + np.random.randint(-10, 10)
            drip_len = 20 + np.random.randint(10, 40)
            if drip_x < width - 20:
                self._draw_rust_drip(painter, drip_x, 2, drip_len)

        # Corner bolts
        self._draw_corner_bolts(painter, rect, margin=18, size=11)

        # Additional bolts along top edge
        for i in range(1, 4):
            bx = rect.x() + width * i / 4
            if abs(bx - rect.x() - 18) > 15 and abs(bx - (rect.x() + width - 18)) > 15:
                self._draw_bolt(painter, bx, rect.y() + 18, 9)

        # Border - rusty edge
        if focused:
            painter.setBrush(Qt.BrushStyle.NoBrush)
            painter.setPen(QPen(QColor(100, 55, 35, 180), 2))
            painter.drawRoundedRect(rect, radius, radius)
        else:
            painter.setBrush(Qt.BrushStyle.NoBrush)
            painter.setPen(QPen(QColor(60, 50, 42, 120), 1.5))
            painter.drawRoundedRect(rect, radius, radius)

    def paint_waveform_panel(self, painter, rect, w, h, cy):
        """Industrial gauge panel with rivets."""
        # Dark recessed panel
        panel_grad = QLinearGradient(0, 0, 0, h)
        panel_grad.setColorAt(0, QColor(25, 22, 20))
        panel_grad.setColorAt(0.1, QColor(35, 32, 28))
        panel_grad.setColorAt(0.9, QColor(30, 27, 24))
        panel_grad.setColorAt(1, QColor(20, 18, 16))
        painter.setBrush(QBrush(panel_grad))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawRoundedRect(rect, 6, 6)

        # Engraved shadows (deep industrial look)
        for grad, adj in [
            (QLinearGradient(0, 0, 0, 15), rect.adjusted(1, 1, -1, -h + 16)),
            (QLinearGradient(0, 0, 12, 0), rect.adjusted(1, 1, -w + 13, -1)),
            (QLinearGradient(w, 0, w - 12, 0), rect.adjusted(w - 13, 1, -1, -1)),
        ]:
            grad.setColorAt(0, QColor(0, 0, 0, 200))
            grad.setColorAt(1, QColor(0, 0, 0, 0))
            painter.setBrush(QBrush(grad))
            painter.setPen(Qt.PenStyle.NoPen)
            painter.drawRoundedRect(adj, 5, 5)

        # Grid lines - industrial gauge marks
        painter.setPen(QPen(QColor(255, 140, 40, 30), 1))
        for i in range(1, 4):
            y = int(h * i / 4)
            painter.drawLine(5, y, w - 5, y)

        # Panel border - raised metal edge
        painter.setBrush(Qt.BrushStyle.NoBrush)
        painter.setPen(QPen(QColor(70, 62, 55), 2))
        painter.drawRoundedRect(rect, 6, 6)

        # Inner highlight
        painter.setPen(QPen(QColor(90, 80, 70, 100), 1))
        painter.drawRoundedRect(rect.adjusted(2, 2, -2, -2), 4, 4)

        # Small rivets in corners of waveform panel
        for corner in [(8, 8), (w - 8, 8), (8, h - 8), (w - 8, h - 8)]:
            self._draw_bolt(painter, corner[0], corner[1], 6)

        # Center line - amber
        painter.setPen(QPen(QColor(255, 140, 40, 60), 1))
        painter.drawLine(0, int(cy), w, int(cy))
