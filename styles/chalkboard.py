"""Chalkboard style - real classroom blackboard with chalk dust, eraser smudges, and wood frame."""

import math
import numpy as np
from PyQt6.QtCore import Qt, QRectF, QPointF
from PyQt6.QtGui import (
    QColor, QLinearGradient, QRadialGradient, QBrush, QImage, QPixmap,
    QPainterPath, QPen
)

from .base import BaseStyle, get_cached_texture


# Chalkboard surface colors
BOARD_DARK = "rgb(30, 43, 30)"
BOARD_MID = "rgb(40, 55, 40)"
BOARD_LIGHT = "rgb(50, 68, 50)"

# Wood frame colors
FRAME_DARK = "rgb(50, 30, 18)"
FRAME_MID = "rgb(72, 44, 26)"
FRAME_LIGHT = "rgb(95, 60, 38)"
FRAME_HIGHLIGHT = "rgb(115, 75, 48)"

# Chalk text colors
CHALK_WHITE = "rgb(240, 234, 214)"
CHALK_DIM = "rgb(212, 205, 184)"
CHALK_FAINT = "rgb(138, 132, 114)"
CHALK_DISABLED = "rgb(80, 78, 68)"

# Accent - teacher's chalk yellow
CHALK_YELLOW = QColor(255, 228, 160)
CHALK_YELLOW_CSS = "rgb(255, 228, 160)"
CHALK_YELLOW_DIM = "rgba(255, 228, 160, 0.7)"

# Colored chalk
CHALK_RED = "rgb(255, 155, 155)"
CHALK_BLUE = "rgb(142, 200, 232)"
CHALK_PINK = "rgb(255, 180, 200)"

# Borders
BORDER_FRAME = "rgb(62, 44, 30)"
BORDER_DARK = "rgb(38, 24, 14)"


class ChalkboardStyle(BaseStyle):
    name = "chalkboard"
    font = "Chalkduster"  # macOS chalk font, falls back to Marker Felt / Comic Sans MS
    corner_radius = 6  # Chalkboards are boxy, not rounded

    _board_cache = None

    # Chalk theme colors
    accent = CHALK_YELLOW
    accent_css = CHALK_YELLOW_CSS
    text_primary = CHALK_WHITE
    text_secondary = CHALK_DIM
    text_muted = CHALK_FAINT
    text_error = CHALK_RED
    text_link = CHALK_BLUE
    border_color = BORDER_FRAME
    border_dark = BORDER_DARK
    icon_color_dark = '#f0ead6'   # Chalk white icons
    icon_color_light = '#f0ead6'
    icon_color_muted = '#8a8472'

    # Slider - chalky groove on dark green
    slider_groove = "rgba(20, 35, 20, 0.9)"
    slider_handle = CHALK_YELLOW_CSS
    slider_fill = "rgb(220, 200, 140)"

    # Rotary knob - vintage classroom style
    knob_style = "vintage"
    knob_body_dark = "#1e2b1e"
    knob_body_light = "#3a4e3a"
    knob_notch_style = "line"
    knob_tickmarks = True
    knob_glow = False
    knob_track_color = "#ffe4a0"
    knob_label_color = "#f0ead6"

    # Waveform - chalk white on dark board
    waveform_color = QColor(240, 234, 214)
    waveform_glow = False  # Chalk is matte, not glowy
    waveform_center_line = QColor(255, 228, 160, 60)
    waveform_panel = "dark"

    # Timer - chalk style, not LCD
    timer_use_lcd = False
    timer_color = CHALK_YELLOW
    timer_font_size = 28

    # Transcription - slightly lighter board area
    transcription_text = CHALK_WHITE
    transcription_text_dimmed = CHALK_YELLOW_DIM
    transcription_panel_bg = BOARD_DARK
    transcription_panel_border = BORDER_DARK
    transcription_row_hover = "rgba(240, 234, 214, 0.08)"
    transcription_row_btn_bg = "rgba(240, 234, 214, 0.10)"
    transcription_row_btn_hover = "rgba(255, 228, 160, 0.18)"
    transcription_row_btn_pressed = "rgba(255, 228, 160, 0.30)"

    # Input fields - dark board surface
    input_bg = '#2a3d2a'
    input_text = '#f0ead6'

    # Chime editor - chalkboard cells
    chime_grid_bg = QColor(30, 43, 30)
    chime_grid_line = QColor(55, 72, 55)
    chime_cell_inactive = QColor(38, 52, 38)
    chime_cell_active = QColor(255, 228, 160)
    chime_cell_highlight = QColor(255, 228, 160, 80)
    chime_piano_white = QColor(230, 224, 204)   # Chalk-dusted ivory
    chime_piano_black = QColor(30, 43, 30)       # Board green
    chime_piano_label_white = QColor(60, 78, 60)
    chime_piano_label_black = QColor(212, 205, 184)

    def button_css(self):
        return (
            f"QPushButton {{ color: {CHALK_DIM}; "
            f"background: qlineargradient(x1:0, y1:0, x2:0, y2:1, "
            f"stop:0 {BOARD_LIGHT}, stop:0.15 {BOARD_MID}, "
            f"stop:0.85 {BOARD_DARK}, stop:1 rgb(24, 36, 24)); "
            f"border: 2px solid {BORDER_FRAME}; border-top-color: {FRAME_MID}; "
            f"border-radius: 3px; padding: 3px 8px; font-size: 11px; "
            f"font-family: {self.font}; text-align: left; }}"
            # Hover - chalk highlight
            f"QPushButton:hover {{ color: {CHALK_WHITE}; "
            f"background: qlineargradient(x1:0, y1:0, x2:0, y2:1, "
            f"stop:0 rgb(60, 78, 60), stop:0.15 rgb(50, 66, 50), "
            f"stop:0.85 {BOARD_MID}, stop:1 {BOARD_DARK}); "
            f"border: 2px solid {FRAME_MID}; }}"
            # Pressed - deeper inset
            f"QPushButton:pressed {{ color: {CHALK_YELLOW_CSS}; "
            f"background: qlineargradient(x1:0, y1:0, x2:0, y2:1, "
            f"stop:0 {BOARD_DARK}, stop:0.15 {BOARD_MID}, "
            f"stop:0.85 {BOARD_LIGHT}, stop:1 {BOARD_MID}); "
            f"border: 2px solid {BORDER_DARK}; }}"
            # Disabled
            f"QPushButton:disabled {{ color: {CHALK_DISABLED}; "
            f"background: {BOARD_DARK}; border: 2px solid {BORDER_DARK}; }}"
            # Checked - chalk yellow underline effect
            f"QPushButton:checked {{ color: {CHALK_WHITE}; "
            f"background: qlineargradient(x1:0, y1:0, x2:0, y2:1, "
            f"stop:0 rgb(70, 80, 55), stop:0.15 rgb(55, 68, 45), "
            f"stop:0.85 rgb(40, 52, 35), stop:1 rgb(35, 46, 30)); "
            f"border: 2px solid {CHALK_YELLOW_CSS}; }}"
            f"QPushButton:checked:hover {{ "
            f"background: qlineargradient(x1:0, y1:0, x2:0, y2:1, "
            f"stop:0 rgb(80, 90, 62), stop:0.15 rgb(65, 78, 52), "
            f"stop:0.85 rgb(48, 60, 40), stop:1 rgb(40, 52, 35)); }}"
        )

    def menu_css(self):
        return (
            f"QMenu {{ background: {BOARD_DARK}; color: {CHALK_WHITE}; "
            f"border: 2px solid {BORDER_FRAME}; border-radius: 3px; padding: 4px; "
            f"font-family: {self.font}; font-size: 11px; }}"
            "QMenu::item { padding: 4px 16px; border-radius: 2px; }"
            f"QMenu::item:selected {{ color: {CHALK_YELLOW_CSS}; "
            f"background: qlineargradient(x1:0, y1:0, x2:0, y2:1, "
            f"stop:0 rgb(55, 70, 55), stop:0.5 {BOARD_MID}, stop:1 {BOARD_DARK}); }}"
            f"QMenu::separator {{ height: 2px; background: {BORDER_FRAME}; margin: 4px 8px; }}"
        )

    def scrollbar_css(self):
        return (
            f"QScrollBar:vertical {{ width: 14px; background: {BOARD_DARK}; "
            f"border: 1px solid {BORDER_DARK}; border-radius: 4px; margin: 0px; }}"
            # Handle - lighter chalkboard green
            "QScrollBar::handle:vertical { "
            "background: qlineargradient(x1:0, y1:0, x2:1, y2:0, "
            f"stop:0.0 {BOARD_MID}, stop:0.2 {BOARD_LIGHT}, "
            f"stop:0.5 rgb(60, 78, 60), stop:0.8 {BOARD_LIGHT}, stop:1.0 {BOARD_MID}); "
            f"border: 1px solid {BORDER_FRAME}; border-radius: 4px; min-height: 40px; margin: 2px; }}"
            # Handle hover
            "QScrollBar::handle:vertical:hover { "
            "background: qlineargradient(x1:0, y1:0, x2:1, y2:0, "
            f"stop:0.0 {BOARD_LIGHT}, stop:0.2 rgb(65, 82, 65), "
            f"stop:0.5 rgb(75, 92, 75), stop:0.8 rgb(65, 82, 65), stop:1.0 {BOARD_LIGHT}); "
            f"border: 1px solid {FRAME_MID}; }}"
            # Handle pressed
            "QScrollBar::handle:vertical:pressed { "
            "background: qlineargradient(x1:0, y1:0, x2:1, y2:0, "
            f"stop:0.0 {BOARD_DARK}, stop:0.2 {BOARD_MID}, "
            f"stop:0.5 {BOARD_LIGHT}, stop:0.8 {BOARD_MID}, stop:1.0 {BOARD_DARK}); "
            f"border: 1px solid {BORDER_DARK}; }}"
            "QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical { "
            "height: 0; width: 0; background: none; border: none; }"
            "QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical { background: transparent; }"
        )

    def panel_bg_css(self):
        return (
            f"background: qlineargradient(x1:0, y1:0, x2:0, y2:1, "
            f"stop:0 {BOARD_LIGHT}, stop:0.02 {BOARD_MID}, "
            f"stop:0.98 {BOARD_DARK}, stop:1 rgb(22, 34, 22)); "
            f"border: 2px solid {BORDER_FRAME}; border-radius: 3px;"
        )

    def panel_bg_flat_css(self):
        return (
            f"background: {BOARD_DARK}; border: 2px solid {BORDER_FRAME}; border-radius: 3px;"
        )

    # ------------------------------------------------------------------
    # Procedural texture generation
    # ------------------------------------------------------------------

    def get_background_pixmap(self, height=512):
        """Procedural chalkboard texture with dust, eraser smudges, and ghost marks."""
        if ChalkboardStyle._board_cache is not None:
            return ChalkboardStyle._board_cache

        width = 256
        ChalkboardStyle._board_cache = get_cached_texture(
            "chalkboard", width, height,
            lambda: self._generate_chalkboard_texture(width, height),
        )
        return ChalkboardStyle._board_cache

    def _generate_chalkboard_texture(self, width, height):
        """
        Generate a realistic chalkboard surface texture.

        Layers:
            1. Base matte green with fibrous grain
            2. Worn areas (lighter patches from years of use)
            3. Chalk dust residue (gaussian-blurred white noise patches)
            4. Eraser smudge streaks (horizontal blurred lighter bands)
            5. Ghost marks (very faint remnants of old chalk writing)
        """
        from scipy.ndimage import gaussian_filter, uniform_filter1d

        np.random.seed(1885)  # Chalkboards in schools since ~1800s

        # --- Seamless fractal noise utility ---
        def seamless_noise(h, w, octaves=4, persistence=0.5):
            """
            Pure function. Generate seamless tileable fractal noise.

            Args:
                h (int): Height
                w (int): Width
                octaves (int): Number of noise octaves
                persistence (float): Amplitude decay per octave

            Returns:
                np.ndarray: Normalized noise in [0, 1]

            Examples:
                >>> # seamless_noise(64, 64).shape == (64, 64)
            """
            noise = np.zeros((h, w), dtype=np.float32)
            amplitude = 1.0
            for octave in range(octaves):
                freq = 2 ** octave
                seed_h, seed_w = max(2, h // freq), max(2, w // freq)
                seed = np.random.random((seed_h, seed_w)).astype(np.float32)
                # Bilinear interpolation with wrapping for seamless tiling
                ys = np.arange(h, dtype=np.float32) / h * seed_h
                xs = np.arange(w, dtype=np.float32) / w * seed_w
                y0 = np.floor(ys).astype(int) % seed_h
                x0 = np.floor(xs).astype(int) % seed_w
                y1 = (y0 + 1) % seed_h
                x1 = (x0 + 1) % seed_w
                fy = (ys - np.floor(ys))[:, None]
                fx = (xs - np.floor(xs))[None, :]
                layer = (
                    seed[y0][:, x0] * (1 - fx) * (1 - fy)
                    + seed[y0][:, x1] * fx * (1 - fy)
                    + seed[y1][:, x0] * (1 - fx) * fy
                    + seed[y1][:, x1] * fx * fy
                )
                noise += layer * amplitude
                amplitude *= persistence
            lo, hi = noise.min(), noise.max()
            return (noise - lo) / (hi - lo + 1e-6)

        # === Layer 1: Base green surface with fibrous grain ===
        grain = seamless_noise(height, width, octaves=5, persistence=0.55)
        # Fine micro-texture (like the matte surface of a real board)
        micro = np.random.random((height, width)).astype(np.float32)
        micro = gaussian_filter(micro, sigma=0.8, mode='wrap')

        # Base RGB: dark matte green (#2D3A2D area)
        base_r = 38 + grain * 12 + micro * 6
        base_g = 54 + grain * 16 + micro * 8
        base_b = 38 + grain * 12 + micro * 6

        # === Layer 2: Worn areas - lighter patches from heavy use ===
        wear = seamless_noise(height, width, octaves=3, persistence=0.4)
        wear_mask = np.clip(wear * 0.5, 0, 0.4)

        # Apply wear: lighten the surface
        base_r += wear_mask * 18
        base_g += wear_mask * 22
        base_b += wear_mask * 16

        # === Layer 3: Chalk dust residue ===
        # Random patches of white dust from erasing
        dust_noise = seamless_noise(height, width, octaves=2, persistence=0.3)
        dust_spots = (dust_noise > 0.65).astype(np.float32)
        dust_spots = gaussian_filter(dust_spots, sigma=6, mode='wrap')
        dust_intensity = dust_spots * 0.35

        base_r += dust_intensity * 45
        base_g += dust_intensity * 42
        base_b += dust_intensity * 38

        # === Layer 4: Eraser smudge streaks ===
        # Horizontal streaks where someone wiped with an eraser
        eraser_base = np.random.random((height, width)).astype(np.float32)
        # Strong horizontal blur to create streak direction
        eraser_streaks = uniform_filter1d(eraser_base, size=60, axis=1, mode='wrap')
        # Slight vertical blur so they're not razor-thin
        eraser_streaks = gaussian_filter(eraser_streaks, sigma=(3, 1), mode='wrap')
        # Threshold to create distinct streak bands
        eraser_mask = np.clip((eraser_streaks - 0.45) * 4, 0, 1)
        # Only apply in certain vertical bands (not the whole surface)
        eraser_bands = seamless_noise(height, width, octaves=1, persistence=0.5)
        eraser_bands = (eraser_bands > 0.55).astype(np.float32)
        eraser_bands = gaussian_filter(eraser_bands, sigma=(12, 3), mode='wrap')
        eraser_combined = eraser_mask * eraser_bands * 0.25

        base_r += eraser_combined * 30
        base_g += eraser_combined * 28
        base_b += eraser_combined * 24

        # === Layer 5: Ghost marks (faint remnants of old writing) ===
        # Small squiggly shapes - simulate with high-frequency noise patches
        ghost = seamless_noise(height, width, octaves=6, persistence=0.65)
        ghost_marks = (ghost > 0.72).astype(np.float32)
        # Thin them out with slight blur
        ghost_marks = gaussian_filter(ghost_marks, sigma=1.2, mode='wrap')
        # Very faint
        ghost_marks *= 0.12

        base_r += ghost_marks * 40
        base_g += ghost_marks * 38
        base_b += ghost_marks * 35

        # Edge darkening is done in paint_window as a gradient overlay,
        # not in the texture, so tiling remains seamless.

        # === Assemble RGBA image ===
        img = np.zeros((height, width, 4), dtype=np.uint8)
        img[:, :, 0] = np.clip(base_r, 15, 90).astype(np.uint8)
        img[:, :, 1] = np.clip(base_g, 25, 110).astype(np.uint8)
        img[:, :, 2] = np.clip(base_b, 15, 90).astype(np.uint8)
        img[:, :, 3] = 255

        qimg = QImage(img.data, width, height, width * 4, QImage.Format.Format_RGBA8888).copy()
        return QPixmap.fromImage(qimg)

    # ------------------------------------------------------------------
    # Paint methods
    # ------------------------------------------------------------------

    def _draw_wood_frame(self, painter, rect, width, height, radius, thickness=8):
        """
        Draw a wooden frame border around the chalkboard with 3D depth.

        Uses layered gradients to simulate beveled wood molding: highlight on
        the outer edge facing light, shadow on the inner edge facing the board.
        """
        # Outer frame edge (dark shadow)
        painter.setBrush(Qt.BrushStyle.NoBrush)
        painter.setPen(QPen(QColor(30, 18, 10), thickness + 2))
        painter.drawRoundedRect(rect, radius, radius)

        # Main frame body - brown wood
        painter.setPen(QPen(QColor(72, 44, 26), thickness))
        painter.drawRoundedRect(rect, radius, radius)

        # Inner highlight (light catches the edge closest to the board)
        painter.setPen(QPen(QColor(95, 60, 38, 160), 1.5))
        painter.drawRoundedRect(
            rect.adjusted(thickness // 2, thickness // 2, -thickness // 2, -thickness // 2),
            max(1, radius - 2), max(1, radius - 2),
        )

        # Outer highlight on top-left edges (3D bevel)
        # Top edge highlight
        top_grad = QLinearGradient(0, rect.y(), 0, rect.y() + thickness)
        top_grad.setColorAt(0, QColor(115, 75, 48, 120))
        top_grad.setColorAt(1, QColor(50, 30, 18, 0))
        painter.setBrush(QBrush(top_grad))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawRect(QRectF(rect.x(), rect.y(), width, thickness))

        # Left edge highlight
        left_grad = QLinearGradient(rect.x(), 0, rect.x() + thickness, 0)
        left_grad.setColorAt(0, QColor(115, 75, 48, 80))
        left_grad.setColorAt(1, QColor(50, 30, 18, 0))
        painter.setBrush(QBrush(left_grad))
        painter.drawRect(QRectF(rect.x(), rect.y(), thickness, height))

        # Bottom/right shadow (darker underside)
        bot_grad = QLinearGradient(0, rect.y() + height - thickness, 0, rect.y() + height)
        bot_grad.setColorAt(0, QColor(20, 12, 6, 0))
        bot_grad.setColorAt(1, QColor(20, 12, 6, 140))
        painter.setBrush(QBrush(bot_grad))
        painter.drawRect(QRectF(rect.x(), rect.y() + height - thickness, width, thickness))

        right_grad = QLinearGradient(rect.x() + width - thickness, 0, rect.x() + width, 0)
        right_grad.setColorAt(0, QColor(20, 12, 6, 0))
        right_grad.setColorAt(1, QColor(20, 12, 6, 100))
        painter.setBrush(QBrush(right_grad))
        painter.drawRect(QRectF(rect.x() + width - thickness, rect.y(), thickness, height))

    def _draw_chalk_tray_shadow(self, painter, rect, width, height):
        """
        Draw a subtle shadow at the bottom of the board, as if cast by a chalk tray.

        Real chalkboards have a narrow wooden ledge at the bottom for chalk and erasers.
        The shadow it casts is a soft dark gradient on the board surface above it.
        """
        tray_height = 18
        shadow_height = 25
        y_base = rect.y() + height - tray_height

        # The tray itself - slightly lighter wood strip
        tray_grad = QLinearGradient(0, y_base, 0, y_base + tray_height)
        tray_grad.setColorAt(0, QColor(62, 38, 22))
        tray_grad.setColorAt(0.3, QColor(82, 52, 32))
        tray_grad.setColorAt(0.7, QColor(72, 44, 26))
        tray_grad.setColorAt(1, QColor(50, 30, 18))
        painter.setBrush(QBrush(tray_grad))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawRect(QRectF(rect.x() + 6, y_base, width - 12, tray_height))

        # Top lip of tray (bright edge catching light)
        painter.setPen(QPen(QColor(100, 65, 42, 180), 1))
        painter.drawLine(
            int(rect.x() + 8), int(y_base),
            int(rect.x() + width - 8), int(y_base),
        )

        # Shadow cast upward onto the board from the tray
        shadow_grad = QLinearGradient(0, y_base, 0, y_base - shadow_height)
        shadow_grad.setColorAt(0, QColor(0, 0, 0, 80))
        shadow_grad.setColorAt(1, QColor(0, 0, 0, 0))
        painter.setBrush(QBrush(shadow_grad))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawRect(QRectF(rect.x() + 6, y_base - shadow_height, width - 12, shadow_height))

    def _draw_chalk_dust_overlay(self, painter, rect, width, height, radius):
        """
        Paint scattered chalk dust particles on the board surface using the painter.

        Places small semi-transparent white/cream circles at deterministic random
        positions, concentrated more toward the bottom (dust settles).
        """
        np.random.seed(777)
        painter.setPen(Qt.PenStyle.NoPen)
        num_particles = 40
        for _ in range(num_particles):
            px = rect.x() + np.random.randint(10, width - 10)
            # Bias particles toward lower half (gravity/settling)
            py = rect.y() + int(np.random.beta(2, 1.2) * (height - 20)) + 10
            size = 1 + np.random.randint(0, 3)
            alpha = 15 + np.random.randint(0, 25)
            painter.setBrush(QBrush(QColor(240, 234, 214, alpha)))
            painter.drawEllipse(QPointF(px, py), size, size)

    def paint_window(self, painter, rect, width, height, focused=True):
        """
        Paint the full chalkboard window background.

        Layers (back to front):
            1. Chalkboard texture (tiled procedural green surface)
            2. Chalk dust particle overlay
            3. Chalk tray shadow at bottom
            4. Wood frame border
        """
        radius = self.corner_radius

        # Clip to rounded rect
        path = QPainterPath()
        path.addRoundedRect(QRectF(rect), radius, radius)
        painter.setClipPath(path)

        # 1. Chalkboard texture
        board = self.get_background_pixmap(max(512, height))
        painter.drawTiledPixmap(rect, board)

        # 2. Edge darkening (less chalk use at edges — subtle vignette)
        for horizontal, alpha_mult in [(True, 0.4), (False, 0.6)]:
            grad = QLinearGradient(
                0, 0,
                width if horizontal else 0,
                0 if horizontal else height,
            )
            for pos, alpha in [(0, 80), (0.1, 30), (0.25, 5), (0.75, 5), (0.9, 30), (1, 80)]:
                grad.setColorAt(pos, QColor(15, 22, 15, int(alpha * alpha_mult)))
            painter.setBrush(QBrush(grad))
            painter.setPen(Qt.PenStyle.NoPen)
            painter.drawRoundedRect(rect, radius, radius)

        # 3. Chalk dust particles (on the surface, before frame)
        self._draw_chalk_dust_overlay(painter, rect, width, height, radius)

        # 4. Chalk tray shadow at bottom
        self._draw_chalk_tray_shadow(painter, rect, width, height)

        painter.setClipping(False)

        # 5. Wood frame
        frame_thickness = 7 if focused else 6
        self._draw_wood_frame(painter, rect, width, height, radius, frame_thickness)

    def paint_waveform_panel(self, painter, rect, w, h, cy):
        """
        Paint the waveform panel as a freshly-cleaned section of the chalkboard.

        Features:
            - Slightly darker recessed area (freshly wiped)
            - Chalk-drawn grid lines with sine-wave wobble (hand-drawn feel)
            - Chalk dust smudges at panel edges
            - Yellow chalk center line
        """
        # Dark recessed panel - freshly cleaned area
        panel_grad = QLinearGradient(0, 0, 0, h)
        panel_grad.setColorAt(0, QColor(22, 34, 22))
        panel_grad.setColorAt(0.15, QColor(28, 42, 28))
        panel_grad.setColorAt(0.85, QColor(25, 38, 25))
        panel_grad.setColorAt(1, QColor(18, 30, 18))
        painter.setBrush(QBrush(panel_grad))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawRoundedRect(rect, 4, 4)

        # Subtle eraser smudge over the whole panel (freshly wiped look)
        smudge_grad = QLinearGradient(0, 0, w, 0)
        smudge_grad.setColorAt(0, QColor(200, 195, 180, 0))
        smudge_grad.setColorAt(0.3, QColor(200, 195, 180, 12))
        smudge_grad.setColorAt(0.5, QColor(200, 195, 180, 8))
        smudge_grad.setColorAt(0.7, QColor(200, 195, 180, 14))
        smudge_grad.setColorAt(1, QColor(200, 195, 180, 0))
        painter.setBrush(QBrush(smudge_grad))
        painter.drawRoundedRect(rect, 4, 4)

        # Chalk dust at edges (lighter smudges where eraser stopped)
        for edge_grad, edge_rect in [
            (QLinearGradient(0, 0, 0, 12), rect.adjusted(2, 0, -2, -h + 14)),
            (QLinearGradient(0, h - 12, 0, h), rect.adjusted(2, h - 14, -2, 0)),
        ]:
            edge_grad.setColorAt(0, QColor(220, 214, 195, 20))
            edge_grad.setColorAt(1, QColor(220, 214, 195, 0))
            painter.setBrush(QBrush(edge_grad))
            painter.setPen(Qt.PenStyle.NoPen)
            painter.drawRect(edge_rect)

        # Chalk-drawn grid lines with hand-drawn wobble
        chalk_pen = QPen(QColor(200, 195, 180, 30), 1)
        painter.setPen(chalk_pen)
        for i in range(1, 4):
            y = int(h * i / 4)
            # Draw line segment by segment with sine-wave offset for wobble
            prev_x = 5
            prev_y = y
            segments = 16
            for seg in range(1, segments + 1):
                sx = int(5 + (w - 10) * seg / segments)
                # Wobble: small sine offset unique to each grid line
                wobble = math.sin(sx * 0.08 + i * 2.1) * 1.5
                sy = int(y + wobble)
                painter.drawLine(prev_x, prev_y, sx, sy)
                prev_x, prev_y = sx, sy

        # Panel border - subtle chalk-drawn rectangle (not perfectly straight)
        border_pen = QPen(QColor(100, 120, 100, 80), 1.5)
        painter.setPen(border_pen)
        painter.setBrush(Qt.BrushStyle.NoBrush)
        painter.drawRoundedRect(rect.adjusted(1, 1, -1, -1), 3, 3)

        # Center line - drawn in yellow chalk with slight thickness variation
        yellow_pen = QPen(QColor(255, 228, 160, 70), 1.5)
        painter.setPen(yellow_pen)
        # Wobble the center line too
        cy_int = int(cy)
        prev_x = 0
        prev_y = cy_int
        segments = 20
        for seg in range(1, segments + 1):
            sx = int(w * seg / segments)
            wobble = math.sin(sx * 0.06 + 0.7) * 0.8
            sy = int(cy_int + wobble)
            painter.drawLine(prev_x, prev_y, sx, sy)
            prev_x, prev_y = sx, sy
