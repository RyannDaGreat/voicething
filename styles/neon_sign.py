"""Neon Sign style - glowing neon tubes on a dark brick wall at night."""

import numpy as np
from PyQt6.QtCore import Qt, QRectF, QPointF
from PyQt6.QtGui import (
    QColor, QLinearGradient, QRadialGradient, QBrush, QImage, QPixmap,
    QPainterPath, QPen,
)

from .base import BaseStyle, get_cached_texture


# Neon colors - the tubes themselves
NEON_PINK = QColor(255, 20, 147)         # #FF1493 - deep pink
NEON_PINK_CSS = "rgb(255, 20, 147)"
NEON_BLUE = QColor(0, 191, 255)          # #00BFFF - deep sky blue
NEON_BLUE_CSS = "rgb(0, 191, 255)"
NEON_GREEN = QColor(57, 255, 20)         # #39FF14 - neon green (accent)
NEON_YELLOW = QColor(255, 255, 50)       # Yellow accent

# Brick wall tones
BRICK_DARK = "rgb(42, 26, 26)"           # #2A1A1A
BRICK_DEEPER = "rgb(26, 16, 16)"         # #1A1010
MORTAR = "rgb(26, 18, 16)"              # #1A1210

# Text - warm incandescent whites
TEXT_WARM = "rgb(255, 245, 232)"          # #FFF5E8
TEXT_DIM = "rgb(221, 208, 192)"           # #DDD0C0
TEXT_MUTED = "rgb(138, 126, 112)"         # #8A7E70
TEXT_DISABLED = "rgb(70, 60, 52)"

# Borders
BORDER_MORTAR = "rgb(26, 18, 16)"
BORDER_GLOW = "rgb(120, 20, 80)"


class NeonSignStyle(BaseStyle):
    name = "neon_sign"
    font = "Futura"

    _brick_cache = None

    # Neon pink accent
    accent = NEON_PINK
    accent_css = NEON_PINK_CSS
    text_primary = TEXT_WARM
    text_secondary = TEXT_DIM
    text_muted = TEXT_MUTED
    text_error = "rgb(255, 51, 51)"
    text_link = NEON_BLUE_CSS
    border_color = BORDER_GLOW
    border_dark = BORDER_MORTAR
    icon_color_dark = '#ff1493'
    icon_color_light = '#ff69b4'
    icon_color_muted = '#803060'

    # Input fields - dark with warm text
    input_bg = '#1A1010'
    input_text = '#FFF5E8'

    # Slider - neon pink on dark
    slider_groove = "rgba(255, 20, 147, 0.3)"

    # Rotary knob - neon glow style
    knob_style = "neon"
    knob_body_dark = "#1A1010"
    knob_body_light = "#3A2020"
    knob_notch_style = "dot"
    knob_tickmarks = False
    knob_glow = True
    knob_track_color = "#FF1493"
    knob_label_color = "#FFF5E8"

    # Waveform - neon blue (different tube color from border)
    waveform_color = NEON_BLUE
    waveform_glow = True
    waveform_glow_radius = 22
    waveform_glow_alpha = 180
    waveform_center_line = QColor(255, 20, 147, 80)
    waveform_panel = "dark"

    # Timer - neon pink LCD
    timer_use_lcd = True
    timer_color = NEON_PINK

    # Transcription - dark brick panel
    transcription_text = TEXT_WARM
    transcription_text_dimmed = TEXT_DIM
    transcription_panel_bg = BRICK_DEEPER
    transcription_panel_border = BORDER_MORTAR
    transcription_row_hover = "rgba(255, 20, 147, 0.12)"
    transcription_row_btn_bg = "rgba(255, 20, 147, 0.10)"
    transcription_row_btn_hover = "rgba(255, 20, 147, 0.22)"
    transcription_row_btn_pressed = "rgba(255, 20, 147, 0.38)"

    # Chime editor - neon on dark brick
    chime_grid_bg = QColor(26, 16, 16)
    chime_grid_line = QColor(60, 35, 35)
    chime_cell_inactive = QColor(42, 26, 26)
    chime_cell_active = QColor(255, 20, 147)
    chime_cell_highlight = QColor(255, 20, 147, 90)
    chime_piano_white = QColor(255, 230, 240)
    chime_piano_black = QColor(35, 20, 20)
    chime_piano_label_white = QColor(100, 50, 70)
    chime_piano_label_black = QColor(255, 150, 200)

    def button_css(self):
        return (
            # Normal - dark brick with subtle neon pink border
            f"QPushButton {{ color: {TEXT_DIM}; "
            f"background: qlineargradient(x1:0, y1:0, x2:0, y2:1, "
            f"stop:0 rgb(55, 30, 30), stop:0.4 rgb(38, 22, 22), "
            f"stop:0.6 rgb(32, 18, 18), stop:1 rgb(42, 24, 24)); "
            f"border: 1px solid rgb(100, 30, 60); "
            f"border-radius: 4px; padding: 4px 10px; font-size: 11px; "
            f"font-family: {self.font}; text-align: left; }}"
            # Hover - neon glow activates
            f"QPushButton:hover {{ color: {NEON_PINK_CSS}; "
            f"background: qlineargradient(x1:0, y1:0, x2:0, y2:1, "
            f"stop:0 rgb(70, 25, 45), stop:0.4 rgb(50, 18, 35), "
            f"stop:0.6 rgb(42, 14, 28), stop:1 rgb(55, 20, 38)); "
            f"border: 1px solid rgb(255, 20, 147); }}"
            # Pressed - brighter core
            f"QPushButton:pressed {{ color: {TEXT_WARM}; "
            f"background: qlineargradient(x1:0, y1:0, x2:0, y2:1, "
            f"stop:0 rgb(90, 30, 55), stop:0.4 rgb(70, 22, 42), "
            f"stop:0.6 rgb(60, 18, 35), stop:1 rgb(75, 25, 48)); "
            f"border: 1px solid rgb(255, 100, 180); }}"
            # Disabled - dead tube
            f"QPushButton:disabled {{ color: {TEXT_DISABLED}; "
            f"background: rgb(26, 16, 16); border: 1px solid rgb(45, 28, 28); }}"
            # Checked - tube fully on
            f"QPushButton:checked {{ color: {TEXT_WARM}; "
            f"background: qlineargradient(x1:0, y1:0, x2:0, y2:1, "
            f"stop:0 rgb(120, 20, 70), stop:0.4 rgb(90, 15, 55), "
            f"stop:0.6 rgb(75, 10, 45), stop:1 rgb(100, 18, 60)); "
            f"border: 1px solid {NEON_PINK_CSS}; }}"
            f"QPushButton:checked:hover {{ "
            f"background: qlineargradient(x1:0, y1:0, x2:0, y2:1, "
            f"stop:0 rgb(140, 25, 80), stop:0.4 rgb(110, 20, 65), "
            f"stop:0.6 rgb(95, 15, 55), stop:1 rgb(120, 22, 70)); }}"
        )

    def menu_css(self):
        return (
            f"QMenu {{ background: rgb(26, 16, 16); color: {TEXT_WARM}; "
            f"border: 1px solid rgb(255, 20, 147); "
            f"border-radius: 4px; padding: 4px; font-family: {self.font}; }}"
            "QMenu::item { padding: 5px 20px; border-radius: 3px; }"
            f"QMenu::item:selected {{ color: {TEXT_WARM}; "
            f"background: qlineargradient(x1:0, y1:0, x2:1, y2:0, "
            f"stop:0 rgb(255, 20, 147), stop:1 rgb(180, 15, 100)); }}"
            f"QMenu::separator {{ height: 1px; background: rgb(80, 30, 50); margin: 4px 8px; }}"
        )

    def _scrollbar_vertical_css(self):
        return (
            f"QScrollBar:vertical {{ width: 12px; background: rgb(26, 16, 16); "
            f"margin: 2px; border: none; border-radius: 6px; }}"
            # Handle - neon pink tube
            f"QScrollBar::handle:vertical {{ "
            f"background: qlineargradient(x1:0, y1:0, x2:1, y2:0, "
            f"stop:0 rgb(180, 15, 100), stop:0.4 rgb(255, 60, 160), "
            f"stop:0.5 rgb(255, 180, 220), "
            f"stop:0.6 rgb(255, 60, 160), stop:1 rgb(180, 15, 100)); "
            f"border-radius: 6px; min-height: 30px; margin: 0px; }}"
            # Hover - brighter glow
            f"QScrollBar::handle:vertical:hover {{ "
            f"background: qlineargradient(x1:0, y1:0, x2:1, y2:0, "
            f"stop:0 rgb(200, 20, 120), stop:0.4 rgb(255, 80, 180), "
            f"stop:0.5 rgb(255, 210, 240), "
            f"stop:0.6 rgb(255, 80, 180), stop:1 rgb(200, 20, 120)); }}"
            # Pressed
            f"QScrollBar::handle:vertical:pressed {{ "
            f"background: qlineargradient(x1:0, y1:0, x2:1, y2:0, "
            f"stop:0 rgb(140, 10, 75), stop:0.4 rgb(200, 40, 130), "
            f"stop:0.5 rgb(255, 140, 200), "
            f"stop:0.6 rgb(200, 40, 130), stop:1 rgb(140, 10, 75)); }}"
            "QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical { height: 0; }"
            "QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical { background: transparent; }"
        )

    def panel_bg_css(self):
        return (
            f"background: qlineargradient(x1:0, y1:0, x2:0, y2:1, "
            f"stop:0 rgb(50, 28, 28), stop:0.02 rgb(26, 16, 16), "
            f"stop:0.98 rgb(26, 16, 16), stop:1 rgb(18, 10, 10)); "
            f"border: 1px solid rgb(80, 30, 50); border-radius: 4px;"
        )

    def panel_bg_flat_css(self):
        return (
            f"background: rgb(26, 16, 16); "
            f"border: 1px solid rgb(60, 25, 35); border-radius: 4px;"
        )

    # ── Texture generation ────────────────────────────────────────────

    def get_brick_pixmap(self, height=512):
        """Procedural brick wall texture with running bond pattern."""
        if NeonSignStyle._brick_cache is not None:
            return NeonSignStyle._brick_cache

        width = 512
        NeonSignStyle._brick_cache = get_cached_texture(
            "neon_brick", width, height,
            lambda: self._generate_brick_texture(width, height),
        )
        return NeonSignStyle._brick_cache

    def _generate_brick_texture(self, width, height):
        """
        Generate a dark brick wall texture with running bond layout.

        Produces standard running bond bricks with per-brick color variation,
        dark mortar lines, surface noise for roughness, and weathering.
        """
        from scipy.ndimage import gaussian_filter

        np.random.seed(7742)

        # Brick dimensions
        brick_w = 64
        brick_h = 28
        mortar = 3

        # Base image - mortar color everywhere first
        img = np.zeros((height, width, 4), dtype=np.uint8)
        # Mortar: dark gray-brown
        img[:, :, 0] = 22
        img[:, :, 1] = 16
        img[:, :, 2] = 14
        img[:, :, 3] = 255

        # Surface noise for roughness (tileable)
        noise_fine = np.random.random((height, width)).astype(np.float32)
        noise_fine = gaussian_filter(noise_fine, sigma=1.2, mode='wrap')
        noise_coarse = np.random.random((height, width)).astype(np.float32)
        noise_coarse = gaussian_filter(noise_coarse, sigma=4.0, mode='wrap')

        # Aging / stain noise - large scale for patches of discoloration
        stain_noise = np.random.random((height, width)).astype(np.float32)
        stain_noise = gaussian_filter(stain_noise, sigma=12.0, mode='wrap')

        # Per-brick color assignment: precompute a grid of brick colors
        rows = height // (brick_h + mortar) + 2
        cols = width // (brick_w + mortar) + 2
        np.random.seed(7742)
        brick_hues = np.random.random((rows, cols)).astype(np.float32)
        brick_dark = np.random.random((rows, cols)).astype(np.float32)

        # Draw bricks row by row
        for row_i in range(rows):
            y0 = row_i * (brick_h + mortar)
            y1 = y0 + brick_h
            if y0 >= height:
                break
            y1 = min(y1, height)

            # Running bond offset: every other row shifts by half a brick
            offset = (brick_w + mortar) // 2 if row_i % 2 == 1 else 0

            for col_i in range(cols + 1):
                x0 = col_i * (brick_w + mortar) - offset
                x1 = x0 + brick_w
                # Wrap for seamless tiling
                if x1 < 0 or x0 >= width:
                    continue

                # Brick base color: dark red-brown with variation
                hue_var = brick_hues[row_i % rows, col_i % cols]
                dark_var = brick_dark[row_i % rows, col_i % cols]

                # Base brick: dark red-brown with reduced variation for readability
                base_r = 48 + int(hue_var * 16) + int(dark_var * 8)
                base_g = 24 + int(hue_var * 7) + int(dark_var * 4)
                base_b = 18 + int(hue_var * 5) + int(dark_var * 3)

                # Some bricks slightly darker/lighter (subtle weathering)
                if dark_var < 0.15:
                    base_r = int(base_r * 0.8)
                    base_g = int(base_g * 0.8)
                    base_b = int(base_b * 0.8)
                elif dark_var > 0.9:
                    base_r = min(base_r + 10, 80)
                    base_g = min(base_g + 3, 38)

                # Clamp pixel ranges for this brick
                px0 = max(x0, 0)
                px1 = min(x1, width)
                py0 = max(y0, 0)
                py1 = min(y1, height)
                if px0 >= px1 or py0 >= py1:
                    continue

                # Per-pixel variation from noise
                region_fine = noise_fine[py0:py1, px0:px1]
                region_coarse = noise_coarse[py0:py1, px0:px1]
                region_stain = stain_noise[py0:py1, px0:px1]

                # Combine: fine roughness + coarse variation + stain (halved)
                variation = (
                    (region_fine - 0.5) * 9
                    + (region_coarse - 0.5) * 6
                    + (region_stain - 0.5) * 4
                )

                img[py0:py1, px0:px1, 0] = np.clip(base_r + variation, 25, 85).astype(np.uint8)
                img[py0:py1, px0:px1, 1] = np.clip(base_g + variation * 0.5, 12, 40).astype(np.uint8)
                img[py0:py1, px0:px1, 2] = np.clip(base_b + variation * 0.35, 10, 30).astype(np.uint8)

                # Subtle edge shading on brick (halved for readability)
                # Top edge highlight (1px)
                if py0 == y0 and py1 > py0 + 1:
                    img[py0, px0:px1, 0] = np.clip(img[py0, px0:px1, 0].astype(np.int16) + 6, 0, 90).astype(np.uint8)
                    img[py0, px0:px1, 1] = np.clip(img[py0, px0:px1, 1].astype(np.int16) + 3, 0, 45).astype(np.uint8)
                    img[py0, px0:px1, 2] = np.clip(img[py0, px0:px1, 2].astype(np.int16) + 2, 0, 35).astype(np.uint8)
                # Bottom edge shadow (1px)
                if py1 == y1 and py1 > py0 + 1:
                    img[py1-1, px0:px1, 0] = np.clip(img[py1-1, px0:px1, 0].astype(np.int16) - 5, 0, 255).astype(np.uint8)
                    img[py1-1, px0:px1, 1] = np.clip(img[py1-1, px0:px1, 1].astype(np.int16) - 3, 0, 255).astype(np.uint8)
                    img[py1-1, px0:px1, 2] = np.clip(img[py1-1, px0:px1, 2].astype(np.int16) - 2, 0, 255).astype(np.uint8)

        # Add mortar line noise - mortar isn't perfectly smooth
        mortar_mask = img[:, :, 0] < 30  # Mortar pixels are darker
        mortar_noise = (np.random.random((height, width)) * 6 - 3).astype(np.int16)
        for c in range(3):
            channel = img[:, :, c].astype(np.int16)
            channel[mortar_mask] += mortar_noise[mortar_mask]
            img[:, :, c] = np.clip(channel, 0, 255).astype(np.uint8)

        qimg = QImage(img.data, width, height, width * 4, QImage.Format.Format_RGBA8888).copy()
        return QPixmap.fromImage(qimg)

    # ── Neon glow drawing helpers ─────────────────────────────────────

    def _draw_neon_glow(self, painter, path, core_color, glow_color, core_width=2, num_layers=6, max_spread=14, alpha_mult=1.0):
        """
        Draw a neon tube effect along a QPainterPath.

        Renders multiple layers of decreasing opacity at increasing widths
        to simulate the bloom of a real neon tube, with a bright white-hot
        core on top.

        Args:
            painter: QPainter
            path: QPainterPath defining the tube shape
            core_color: QColor for the bright tube core
            glow_color: QColor for the colored glow
            core_width: Width of the central bright line
            num_layers: Number of glow layers
            max_spread: Maximum glow width in pixels
            alpha_mult: Multiplier for all alpha values (0.0-1.0, for dimming)
        """
        painter.setBrush(Qt.BrushStyle.NoBrush)

        # Outer glow layers - widest and dimmest first
        for i in range(num_layers, 0, -1):
            t = i / num_layers
            width = core_width + max_spread * t
            alpha = int(glow_color.alpha() * (0.08 + 0.12 * (1 - t)) * alpha_mult)
            alpha = max(1, min(alpha, 255))
            color = QColor(glow_color.red(), glow_color.green(), glow_color.blue(), alpha)
            painter.setPen(QPen(color, width, Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap, Qt.PenJoinStyle.RoundJoin))
            painter.drawPath(path)

        # Inner bright glow - slightly wider than core
        inner_alpha = int(min(255, glow_color.alpha() * 0.6 * alpha_mult))
        inner_color = QColor(
            min(255, glow_color.red() + 60),
            min(255, glow_color.green() + 60),
            min(255, glow_color.blue() + 60),
            inner_alpha,
        )
        painter.setPen(QPen(inner_color, core_width + 3, Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap, Qt.PenJoinStyle.RoundJoin))
        painter.drawPath(path)

        # Core line - white-hot center of the tube
        core_alpha = int(min(255, 240 * alpha_mult))
        white_core = QColor(
            min(255, core_color.red() + 80),
            min(255, core_color.green() + 80),
            min(255, core_color.blue() + 80),
            core_alpha,
        )
        painter.setPen(QPen(white_core, core_width, Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap, Qt.PenJoinStyle.RoundJoin))
        painter.drawPath(path)

    def _draw_neon_rect_glow(self, painter, rect, color, radius=12, core_width=2, num_layers=6, max_spread=14, alpha_mult=1.0):
        """
        Draw a neon tube glow along the edges of a rounded rectangle.

        Args:
            painter: QPainter
            rect: QRectF
            color: QColor for the neon tube
            radius: Corner radius
            core_width: Tube thickness
            num_layers: Number of glow bloom layers
            max_spread: Maximum glow pixel spread
            alpha_mult: Brightness multiplier (for focus/unfocus dimming)
        """
        path = QPainterPath()
        path.addRoundedRect(rect, radius, radius)
        glow_color = QColor(color.red(), color.green(), color.blue(), 200)
        self._draw_neon_glow(painter, path, color, glow_color, core_width, num_layers, max_spread, alpha_mult)

    def _draw_neon_line(self, painter, x1, y1, x2, y2, color, core_width=1.5, num_layers=4, max_spread=8, alpha_mult=1.0):
        """Draw a single neon-glowing line segment."""
        path = QPainterPath()
        path.moveTo(x1, y1)
        path.lineTo(x2, y2)
        glow_color = QColor(color.red(), color.green(), color.blue(), 180)
        self._draw_neon_glow(painter, path, color, glow_color, core_width, num_layers, max_spread, alpha_mult)

    # ── Vignette ──────────────────────────────────────────────────────

    def _draw_vignette(self, painter, rect, width, height, radius=12, strength=1.0):
        """Dark vignette - neon light fades at edges, corners are very dark."""
        for horizontal, alpha_mult in [(True, 0.6 * strength), (False, 1.0 * strength)]:
            grad = QLinearGradient(
                0, 0,
                width if horizontal else 0,
                0 if horizontal else height,
            )
            for pos, alpha in [(0, 200), (0.1, 120), (0.25, 40), (0.75, 40), (0.9, 120), (1, 200)]:
                grad.setColorAt(pos, QColor(0, 0, 0, int(alpha * alpha_mult)))
            painter.setBrush(QBrush(grad))
            painter.setPen(Qt.PenStyle.NoPen)
            painter.drawRoundedRect(rect, radius, radius)

    def _draw_neon_wash(self, painter, rect, width, height, radius=12, alpha_mult=1.0):
        """
        Overlay a soft neon glow wash on the brick wall.

        Simulates neon light bouncing off the wall: a radial gradient
        of pink/magenta light concentrated in the upper center area.
        """
        # Primary pink wash from center-top (where a neon sign would hang)
        cx = width * 0.5
        cy = height * 0.3
        rad = max(width, height) * 0.7
        wash = QRadialGradient(QPointF(cx, cy), rad)
        wash.setColorAt(0.0, QColor(255, 20, 147, int(45 * alpha_mult)))
        wash.setColorAt(0.3, QColor(255, 20, 147, int(25 * alpha_mult)))
        wash.setColorAt(0.6, QColor(200, 10, 100, int(10 * alpha_mult)))
        wash.setColorAt(1.0, QColor(0, 0, 0, 0))
        painter.setBrush(QBrush(wash))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawRoundedRect(rect, radius, radius)

        # Secondary blue wash from bottom-right (second neon tube)
        cx2 = width * 0.7
        cy2 = height * 0.7
        rad2 = max(width, height) * 0.5
        wash2 = QRadialGradient(QPointF(cx2, cy2), rad2)
        wash2.setColorAt(0.0, QColor(0, 191, 255, int(25 * alpha_mult)))
        wash2.setColorAt(0.4, QColor(0, 120, 200, int(10 * alpha_mult)))
        wash2.setColorAt(1.0, QColor(0, 0, 0, 0))
        painter.setBrush(QBrush(wash2))
        painter.drawRoundedRect(rect, radius, radius)

    # ── Paint methods ─────────────────────────────────────────────────

    def paint_window(self, painter, rect, width, height, focused=True):
        """
        Paint dark brick wall with neon glow wash and neon tube border.

        Layers:
        1. Brick wall texture (procedural, cached)
        2. Neon glow wash (pink + blue radial gradients on brick)
        3. Vignette (dark edges)
        4. Neon tube border (multi-layer glow with white-hot core)
        """
        radius = self.corner_radius
        alpha_mult = 1.0 if focused else 0.45

        # Clip to rounded rect
        path = QPainterPath()
        path.addRoundedRect(QRectF(rect), radius, radius)
        painter.setClipPath(path)

        # 1. Draw brick texture
        bricks = self.get_brick_pixmap(max(512, height))
        painter.drawTiledPixmap(rect, bricks)

        # 2. Neon glow wash on the bricks
        self._draw_neon_wash(painter, rect, width, height, radius, alpha_mult)

        # 3. Vignette - dark edges
        self._draw_vignette(painter, rect, width, height, radius)

        painter.setClipping(False)

        # 4. Neon tube border
        border_rect = QRectF(rect).adjusted(2, 2, -2, -2)
        self._draw_neon_rect_glow(
            painter, border_rect, NEON_PINK,
            radius=radius - 1,
            core_width=1.5,
            num_layers=7,
            max_spread=16,
            alpha_mult=alpha_mult,
        )

    def paint_waveform_panel(self, painter, rect, w, h, cy):
        """
        Neon-lit waveform panel: dark recessed brick with blue neon accents.

        The panel is a darker section of wall, as if in shadow, with neon blue
        grid lines and a neon pink center line.
        """
        # Dark recessed panel gradient
        panel_grad = QLinearGradient(0, 0, 0, h)
        panel_grad.setColorAt(0.0, QColor(18, 10, 10))
        panel_grad.setColorAt(0.1, QColor(22, 14, 14))
        panel_grad.setColorAt(0.9, QColor(20, 12, 12))
        panel_grad.setColorAt(1.0, QColor(14, 8, 8))
        painter.setBrush(QBrush(panel_grad))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawRoundedRect(rect, 6, 6)

        # Subtle blue neon wash on the panel
        wash = QRadialGradient(QPointF(w * 0.5, h * 0.5), max(w, h) * 0.6)
        wash.setColorAt(0.0, QColor(0, 100, 180, 20))
        wash.setColorAt(0.5, QColor(0, 60, 120, 8))
        wash.setColorAt(1.0, QColor(0, 0, 0, 0))
        painter.setBrush(QBrush(wash))
        painter.drawRoundedRect(rect, 6, 6)

        # Deep engraved inset shadows
        for grad, adj in [
            (QLinearGradient(0, 0, 0, 18), rect.adjusted(1, 1, -1, -h + 19)),
            (QLinearGradient(0, 0, 14, 0), rect.adjusted(1, 1, -w + 15, -1)),
            (QLinearGradient(w, 0, w - 14, 0), rect.adjusted(w - 15, 1, -1, -1)),
        ]:
            grad.setColorAt(0, QColor(0, 0, 0, 200))
            grad.setColorAt(1, QColor(0, 0, 0, 0))
            painter.setBrush(QBrush(grad))
            painter.setPen(Qt.PenStyle.NoPen)
            painter.drawRoundedRect(adj, 5, 5)

        # Grid lines with neon blue glow
        for i in range(1, 4):
            y = int(h * i / 4)
            self._draw_neon_line(
                painter, 6, y, w - 6, y,
                NEON_BLUE,
                core_width=0.5,
                num_layers=3,
                max_spread=5,
                alpha_mult=0.3,
            )

        # Panel border - neon blue tube, subtle
        border_path = QPainterPath()
        border_path.addRoundedRect(QRectF(rect).adjusted(1, 1, -1, -1), 5, 5)
        glow_blue = QColor(0, 191, 255, 160)
        self._draw_neon_glow(
            painter, border_path, NEON_BLUE, glow_blue,
            core_width=1.0, num_layers=4, max_spread=8, alpha_mult=0.5,
        )

        # Center line - neon pink
        self._draw_neon_line(
            painter, 0, int(cy), w, int(cy),
            NEON_PINK,
            core_width=1.0,
            num_layers=4,
            max_spread=6,
            alpha_mult=0.6,
        )
