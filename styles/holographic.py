"""Holographic style - dark brushed metal with iridescent rainbow film overlay.

Like a holographic sticker or credit card hologram: dark metallic base with
prismatic light bands, thin-film interference patterns, and rainbow sparkle
glints. Premium and tasteful, not garish. Shimmer animation during repaints.
"""

import time

import numpy as np
from PyQt6.QtCore import Qt, QRectF, QPointF
from PyQt6.QtGui import (
    QColor, QLinearGradient, QRadialGradient, QBrush, QImage, QPixmap,
    QPainterPath, QPen,
)

from .base import BaseStyle, get_cached_texture


# Holographic accent - iridescent cyan
HOLO_CYAN = QColor(0, 229, 255)
HOLO_CYAN_CSS = "rgb(0,229,255)"
HOLO_CYAN_MUTED = "rgba(0,200,230,0.7)"
HOLO_CYAN_GLOW = "rgba(0,229,255,0.4)"

# Dark metallic base
BG_DEEPEST = "rgb(12,14,20)"
BG_DARK = "rgb(18,20,26)"
BG_MID = "rgb(30,33,42)"
BG_LIGHT = "rgb(50,55,68)"

# Text - silver/white on dark
TEXT_BRIGHT = "rgb(230,235,245)"
TEXT_DIM = "rgba(200,210,225,0.85)"
TEXT_MUTED = "rgb(130,140,160)"
TEXT_DISABLED = "rgb(70,75,90)"

# Borders - dark with subtle rainbow tint
BORDER_DARK = "rgb(35,38,50)"
BORDER_MID = "rgb(50,55,70)"
BORDER_LIGHT = "rgb(70,78,95)"

# Button surfaces
BTN_DARK = "rgb(22,25,35)"
BTN_MID = "rgb(35,40,52)"
BTN_LIGHT = "rgb(50,56,70)"


def _hsv_to_rgb(h, s, v):
    """
    Pure function. Convert HSV (all 0-1 floats) to RGB (0-255 uint8 arrays).

    Args:
        h: Hue array, 0-1
        s: Saturation, scalar or array
        v: Value, scalar or array

    Returns:
        Tuple of (r, g, b) uint8 arrays

    Examples:
        >>> r, g, b = _hsv_to_rgb(np.array([0.0]), 1.0, 1.0)
        >>> int(r[0]), int(g[0]), int(b[0])
        (255, 0, 0)
    """
    h6 = (h * 6.0) % 6.0
    i = h6.astype(np.int32)
    f = h6 - i
    p = v * (1.0 - s)
    q = v * (1.0 - s * f)
    t = v * (1.0 - s * (1.0 - f))

    # Build RGB based on hue sector
    r = np.where(i == 0, v, np.where(i == 1, q, np.where(i == 2, p, np.where(i == 3, p, np.where(i == 4, t, v)))))
    g = np.where(i == 0, t, np.where(i == 1, v, np.where(i == 2, v, np.where(i == 3, q, np.where(i == 4, p, p)))))
    b = np.where(i == 0, p, np.where(i == 1, p, np.where(i == 2, t, np.where(i == 3, v, np.where(i == 4, v, q)))))

    return (r * 255).astype(np.uint8), (g * 255).astype(np.uint8), (b * 255).astype(np.uint8)


def _generate_holographic_texture(width, height):
    """
    Generate dark brushed metal texture with baked-in iridescent rainbow noise.

    The base is horizontal motion-blurred noise (brushed metal look) in dark
    gray tones, with a subtle layer of rainbow-tinted noise mixed in at low
    opacity for the holographic film grain effect.

    Args:
        width: Texture width in pixels
        height: Texture height in pixels

    Returns:
        QPixmap of the generated texture

    Examples:
        >>> # pm = _generate_holographic_texture(256, 512)
    """
    from scipy.ndimage import uniform_filter1d, gaussian_filter

    np.random.seed(777)

    # --- Layer 1: Brushed dark metal ---
    metal_noise = np.random.randint(0, 40, size=(height, width)).astype(np.float32)
    metal_blurred = uniform_filter1d(metal_noise, size=50, axis=1, mode='wrap')
    # Dark metal base: values around 25-50
    metal = np.clip(25 + metal_blurred - 15, 18, 52).astype(np.float32)

    # --- Layer 2: Rainbow holographic grain ---
    holo_noise = np.random.random((height, width)).astype(np.float32)
    holo_smooth = gaussian_filter(holo_noise, sigma=2.0)
    # Normalize to 0-1 for hue
    holo_hue = (holo_smooth - holo_smooth.min()) / (holo_smooth.max() - holo_smooth.min())

    # Convert hue to RGB rainbow colors at low saturation and value
    r_holo, g_holo, b_holo = _hsv_to_rgb(holo_hue, 0.6, 0.15)

    # --- Layer 3: Diagonal iridescent bands (coarse) ---
    yy, xx = np.mgrid[0:height, 0:width]
    # Diagonal coordinate: top-left to bottom-right
    diag = (xx.astype(np.float32) + yy.astype(np.float32) * 0.7) / 80.0
    band_hue = (diag % 1.0).astype(np.float32)
    r_band, g_band, b_band = _hsv_to_rgb(band_hue, 0.5, 0.08)

    # --- Combine: metal grayscale + rainbow grain + diagonal bands ---
    img = np.zeros((height, width, 4), dtype=np.uint8)
    metal_u8 = metal.astype(np.uint8)
    img[:, :, 0] = np.clip(metal_u8.astype(np.int16) + r_holo + r_band, 0, 255).astype(np.uint8)
    img[:, :, 1] = np.clip(metal_u8.astype(np.int16) + g_holo + g_band, 0, 255).astype(np.uint8)
    img[:, :, 2] = np.clip(metal_u8.astype(np.int16) + b_holo + b_band, 0, 255).astype(np.uint8)
    img[:, :, 3] = 255

    qimg = QImage(img.data, width, height, width * 4, QImage.Format.Format_RGBA8888).copy()
    return QPixmap.fromImage(qimg)


class HolographicStyle(BaseStyle):
    name = "holographic"
    font = "Futura"
    corner_radius = 12

    _texture_cache = None

    # Accent: iridescent cyan
    accent = HOLO_CYAN
    accent_css = HOLO_CYAN_CSS
    text_primary = TEXT_BRIGHT
    text_secondary = TEXT_DIM
    text_muted = TEXT_MUTED
    text_error = "rgb(255,80,100)"
    text_link = HOLO_CYAN_CSS
    border_color = BORDER_MID
    border_dark = BORDER_DARK
    icon_color_dark = '#00e5ff'
    icon_color_light = '#b0f0ff'
    icon_color_muted = '#406880'

    # Slider - holographic cyan
    slider_groove = "rgba(0,229,255,0.25)"

    # Rotary knob - glossy glass (reflective, matches holographic sheen)
    knob_style = "glass"
    knob_body_dark = "#0e1018"
    knob_body_light = "#252838"
    knob_notch_style = "line"
    knob_tickmarks = True
    knob_glow = True
    knob_track_color = "#00e5ff"
    knob_label_color = "#80f0ff"

    # Waveform - cyan with glow on dark panel
    waveform_color = HOLO_CYAN
    waveform_glow = True
    waveform_glow_radius = 20
    waveform_glow_alpha = 180
    waveform_center_line = QColor(0, 229, 255, 50)
    waveform_panel = "dark"

    # Timer - cyan LCD
    timer_use_lcd = True
    timer_color = HOLO_CYAN

    # Transcription
    transcription_text = TEXT_BRIGHT
    transcription_text_dimmed = HOLO_CYAN_MUTED
    transcription_panel_bg = BG_DARK
    transcription_panel_border = BORDER_DARK
    transcription_row_hover = "rgba(0,229,255,0.07)"
    transcription_row_btn_bg = "rgba(0,229,255,0.08)"
    transcription_row_btn_hover = "rgba(0,229,255,0.18)"
    transcription_row_btn_pressed = "rgba(0,229,255,0.32)"

    # Chime editor - dark metallic with holographic accents
    chime_grid_bg = QColor(18, 20, 26)
    chime_grid_line = QColor(40, 45, 58)
    chime_cell_inactive = QColor(28, 32, 42)
    chime_cell_active = QColor(0, 229, 255)
    chime_cell_highlight = QColor(0, 229, 255, 70)
    chime_piano_white = QColor(200, 210, 225)
    chime_piano_black = QColor(22, 25, 35)
    chime_piano_label_white = QColor(40, 45, 58)
    chime_piano_label_black = QColor(0, 200, 230)

    # Input fields - dark
    input_bg = '#151720'
    input_text = '#e0e8f0'

    def button_css(self):
        return (
            # Normal: dark metallic button
            f"QPushButton {{ color: {TEXT_DIM}; "
            f"background: qlineargradient(x1:0, y1:0, x2:0, y2:1, "
            f"stop:0 {BTN_LIGHT}, stop:0.4 {BTN_MID}, stop:0.6 {BTN_DARK}, stop:1 {BTN_MID}); "
            f"border: 1px solid {BORDER_DARK}; border-top-color: {BORDER_LIGHT}; "
            f"border-radius: 5px; padding: 3px 8px; font-size: 11px; "
            f"font-family: {self.font}; text-align: left; }}"
            # Hover: holographic cyan tint
            f"QPushButton:hover {{ color: {HOLO_CYAN_CSS}; "
            f"background: qlineargradient(x1:0, y1:0, x2:0, y2:1, "
            f"stop:0 rgb(40,65,75), stop:0.4 rgb(28,50,60), stop:0.6 rgb(20,40,50), stop:1 rgb(28,50,60)); "
            f"border: 1px solid rgb(0,180,200); }}"
            # Pressed: deeper
            f"QPushButton:pressed {{ color: {TEXT_BRIGHT}; "
            f"background: qlineargradient(x1:0, y1:0, x2:0, y2:1, "
            f"stop:0 rgb(15,30,40), stop:0.4 rgb(12,25,35), stop:0.6 rgb(10,20,30), stop:1 rgb(12,25,35)); "
            f"border: 1px solid rgb(0,140,160); }}"
            # Disabled
            f"QPushButton:disabled {{ color: {TEXT_DISABLED}; "
            f"background: {BTN_DARK}; border: 1px solid {BORDER_DARK}; }}"
            # Checked: active holographic cyan
            f"QPushButton:checked {{ color: {TEXT_BRIGHT}; "
            f"background: qlineargradient(x1:0, y1:0, x2:0, y2:1, "
            f"stop:0 rgb(0,90,100), stop:0.4 rgb(0,70,80), stop:0.6 rgb(0,50,60), stop:1 rgb(0,70,80)); "
            f"border: 1px solid {HOLO_CYAN_CSS}; }}"
            f"QPushButton:checked:hover {{ "
            f"background: qlineargradient(x1:0, y1:0, x2:0, y2:1, "
            f"stop:0 rgb(0,110,120), stop:0.4 rgb(0,90,100), stop:0.6 rgb(0,70,80), stop:1 rgb(0,90,100)); }}"
        )

    def menu_css(self):
        return (
            f"QMenu {{ background: {BG_DARK}; color: {TEXT_BRIGHT}; "
            f"border: 1px solid {BORDER_MID}; border-radius: 6px; padding: 4px; "
            f"font-family: {self.font}; font-size: 12px; }}"
            "QMenu::item { padding: 4px 16px; border-radius: 4px; }"
            f"QMenu::item:selected {{ color: {TEXT_BRIGHT}; "
            f"background: qlineargradient(x1:0, y1:0, x2:0, y2:1, "
            f"stop:0 rgb(0,90,100), stop:0.5 rgb(0,70,80), stop:1 rgb(0,50,60)); }}"
            f"QMenu::separator {{ height: 1px; background: {BORDER_DARK}; margin: 4px 8px; }}"
        )

    def scrollbar_css(self):
        return (
            f"QScrollBar:vertical {{ width: 14px; background: {BG_MID}; "
            f"border: 1px solid {BORDER_DARK}; border-radius: 7px; margin: 0px; }}"
            "QScrollBar::handle:vertical { "
            "background: qlineargradient(x1:0, y1:0, x2:1, y2:0, "
            "stop:0.0 rgb(0,70,80), stop:0.2 rgb(0,90,100), "
            "stop:0.5 rgb(0,110,120), stop:0.8 rgb(0,90,100), stop:1.0 rgb(0,70,80)); "
            f"border: 1px solid rgb(0,55,65); border-radius: 5px; min-height: 40px; margin: 2px; }}"
            "QScrollBar::handle:vertical:hover { "
            "background: qlineargradient(x1:0, y1:0, x2:1, y2:0, "
            "stop:0.0 rgb(0,110,120), stop:0.2 rgb(0,140,155), "
            "stop:0.5 rgb(0,170,190), stop:0.8 rgb(0,140,155), stop:1.0 rgb(0,110,120)); "
            "border: 1px solid rgb(0,90,100); }"
            "QScrollBar::handle:vertical:pressed { "
            "background: qlineargradient(x1:0, y1:0, x2:1, y2:0, "
            "stop:0.0 rgb(0,50,60), stop:0.2 rgb(0,65,75), "
            "stop:0.5 rgb(0,85,95), stop:0.8 rgb(0,65,75), stop:1.0 rgb(0,50,60)); "
            "border: 1px solid rgb(0,40,50); }"
            "QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical { "
            "height: 0; width: 0; background: none; border: none; }"
            "QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical { background: transparent; }"
        )

    def panel_bg_css(self):
        return (
            f"background: qlineargradient(x1:0, y1:0, x2:0, y2:1, "
            f"stop:0 {BG_MID}, stop:0.02 {BG_DARK}, "
            f"stop:0.98 {BG_DARK}, stop:1 {BG_DEEPEST}); "
            f"border: 1px solid {BORDER_DARK}; border-radius: 6px;"
        )

    def panel_bg_flat_css(self):
        return (
            f"background: {BG_DARK}; border: 1px solid {BORDER_DARK}; border-radius: 6px;"
        )

    # --- Texture generation and caching ---

    def _get_holographic_texture(self, height=512):
        """Load or generate the holographic metal texture, with disk caching."""
        if HolographicStyle._texture_cache is not None:
            return HolographicStyle._texture_cache

        width = 256
        HolographicStyle._texture_cache = get_cached_texture(
            "holographic_metal", width, height,
            lambda: _generate_holographic_texture(width, height),
        )
        return HolographicStyle._texture_cache

    # --- Painting helpers ---

    def _draw_vignette(self, painter, rect, width, height, radius=12):
        """Dark edges to frame the holographic surface."""
        for horizontal, alpha_mult in [(True, 0.6), (False, 1.0)]:
            grad = QLinearGradient(
                0, 0,
                width if horizontal else 0,
                0 if horizontal else height,
            )
            for pos, alpha in [(0, 130), (0.1, 60), (0.2, 15), (0.8, 15), (0.9, 60), (1, 130)]:
                grad.setColorAt(pos, QColor(0, 0, 5, int(alpha * alpha_mult)))
            painter.setBrush(QBrush(grad))
            painter.setPen(Qt.PenStyle.NoPen)
            painter.drawRoundedRect(rect, radius, radius)

    def _draw_holographic_film(self, painter, rect, width, height, radius=12):
        """
        Overlay diagonal rainbow gradient bands -- the core holographic effect.

        Two diagonal gradients at different angles create the thin-film
        interference look. The stop positions shift slowly with time, creating
        a subtle shimmer during recording (when repaints run at ~125fps).
        At idle the effect is static since no repaints occur.
        """
        # Slow time-based offset for shimmer (cycles every ~8 seconds)
        t = (time.time() % 8.0) / 8.0

        # --- Primary diagonal rainbow bands (top-left to bottom-right) ---
        primary = QLinearGradient(0, 0, width, height)
        spectrum_colors = [
            QColor(255,  50,  50, 22),   # Red
            QColor(255, 140,  30, 25),   # Orange
            QColor(255, 230,  50, 20),   # Yellow
            QColor( 80, 255,  80, 22),   # Green
            QColor( 30, 220, 220, 28),   # Cyan
            QColor( 60, 100, 255, 25),   # Blue
            QColor(160,  60, 255, 22),   # Purple
            QColor(255,  60, 180, 20),   # Magenta
            QColor(255, 100,  80, 22),   # Red-orange
            QColor(255,  50,  50, 18),   # Red (loop)
        ]
        n = len(spectrum_colors)
        # Shift stops and sort for monotonic positions
        shifted_primary = sorted(
            [((i / (n - 1) + t) % 1.0, c) for i, c in enumerate(spectrum_colors)],
            key=lambda x: x[0],
        )
        for pos, color in shifted_primary:
            primary.setColorAt(pos, color)
        painter.setBrush(QBrush(primary))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawRoundedRect(rect, radius, radius)

        # --- Secondary finer interference bands (bottom-left to top-right) ---
        # Offset in opposite direction for parallax shimmer
        t2 = (1.0 - t * 0.7) % 1.0
        secondary = QLinearGradient(0, height, width * 0.7, 0)
        interference_colors = [
            QColor(  0, 255, 200, 12),
            QColor(100,  80, 255, 15),
            QColor(255,  50, 150, 12),
            QColor(255, 200,  40, 10),
            QColor( 40, 255, 120, 14),
            QColor(  0, 180, 255, 16),
            QColor(200,  50, 255, 12),
            QColor(  0, 255, 200, 10),
        ]
        n2 = len(interference_colors)
        # Shift stops and sort so QLinearGradient gets monotonic positions
        shifted = sorted(
            [((i / (n2 - 1) + t2) % 1.0, c) for i, c in enumerate(interference_colors)],
            key=lambda x: x[0],
        )
        for pos, color in shifted:
            secondary.setColorAt(pos, color)
        painter.setBrush(QBrush(secondary))
        painter.drawRoundedRect(rect, radius, radius)

    def _draw_sheen(self, painter, rect, width, height, radius=12):
        """Metallic sheen highlight at the top -- like light hitting brushed metal."""
        sheen = QLinearGradient(0, 0, 0, height * 0.35)
        sheen.setColorAt(0.0, QColor(255, 255, 255, 35))
        sheen.setColorAt(0.3, QColor(200, 220, 240, 15))
        sheen.setColorAt(0.7, QColor(180, 200, 220, 5))
        sheen.setColorAt(1.0, QColor(150, 170, 190, 0))
        painter.setBrush(QBrush(sheen))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawRoundedRect(
            QRectF(rect.x(), rect.y(), width, height * 0.4),
            radius, radius,
        )

    def _draw_rainbow_sparkle(self, painter, x, y, size, hue):
        """
        Draw a single rainbow-tinted sparkle glint at the given position.

        Args:
            painter: QPainter instance
            x: Center X
            y: Center Y
            size: Radius of the sparkle
            hue: 0-1 float, determines the sparkle's tint color
        """
        # Convert hue to a QColor
        r_arr, g_arr, b_arr = _hsv_to_rgb(np.array([hue]), 0.7, 1.0)
        tint = QColor(int(r_arr[0]), int(g_arr[0]), int(b_arr[0]))

        sparkle = QRadialGradient(QPointF(x, y), size)
        sparkle.setColorAt(0.0, QColor(255, 255, 255, 240))
        sparkle.setColorAt(0.25, QColor(tint.red(), tint.green(), tint.blue(), 180))
        sparkle.setColorAt(0.6, QColor(tint.red(), tint.green(), tint.blue(), 50))
        sparkle.setColorAt(1.0, QColor(tint.red(), tint.green(), tint.blue(), 0))
        painter.setBrush(QBrush(sparkle))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawEllipse(QPointF(x, y), size, size)

    def _draw_rainbow_border(self, painter, rect, width, height, radius=12):
        """
        Draw a cycling rainbow border glow -- holographic edge effect when focused.

        Uses four linear gradients (one per edge) each cycling through spectrum
        colors, creating the effect of rainbow light refracting along the frame.
        """
        painter.setBrush(Qt.BrushStyle.NoBrush)

        # Outer glow layer (wider, more transparent)
        outer_grad = QLinearGradient(0, 0, width, height)
        glow_stops = [
            (0.00, QColor(255,  60,  60, 40)),
            (0.17, QColor(255, 200,  40, 45)),
            (0.33, QColor( 60, 255,  80, 40)),
            (0.50, QColor(  0, 229, 255, 50)),
            (0.67, QColor( 80,  60, 255, 40)),
            (0.83, QColor(255,  60, 200, 45)),
            (1.00, QColor(255,  60,  60, 40)),
        ]
        for pos, color in glow_stops:
            outer_grad.setColorAt(pos, color)
        painter.setPen(QPen(QBrush(outer_grad), 3.0))
        painter.drawRoundedRect(rect.adjusted(-1, -1, 1, 1), radius + 1, radius + 1)

        # Inner crisp border
        inner_grad = QLinearGradient(0, 0, width, height)
        border_stops = [
            (0.00, QColor(255, 100, 100, 100)),
            (0.14, QColor(255, 200,  60, 110)),
            (0.28, QColor(100, 255, 100, 100)),
            (0.42, QColor( 60, 240, 240, 120)),
            (0.57, QColor(100, 100, 255, 100)),
            (0.71, QColor(200,  80, 255, 110)),
            (0.85, QColor(255, 100, 200, 100)),
            (1.00, QColor(255, 100, 100, 100)),
        ]
        for pos, color in border_stops:
            inner_grad.setColorAt(pos, color)
        painter.setPen(QPen(QBrush(inner_grad), 1.5))
        painter.drawRoundedRect(rect, radius, radius)

    # --- Main paint methods ---

    def paint_window(self, painter, rect, width, height, focused=True):
        """Paint dark brushed metal background with holographic film overlay."""
        radius = self.corner_radius

        # Clip to rounded rect
        path = QPainterPath()
        path.addRoundedRect(QRectF(rect), radius, radius)
        painter.setClipPath(path)

        # Layer 1: Dark brushed metal texture
        metal = self._get_holographic_texture(max(512, height))
        painter.drawTiledPixmap(rect, metal)
        painter.setClipping(False)

        # Layer 2: Dark vignette for depth
        self._draw_vignette(painter, rect, width, height, radius)

        # Layer 3: Holographic rainbow film overlay
        self._draw_holographic_film(painter, rect, width, height, radius)

        # Layer 4: Metallic sheen highlight
        if focused:
            self._draw_sheen(painter, rect, width, height, radius)

        # Layer 5: Rainbow sparkle glints
        if focused:
            np.random.seed(314)
            for _ in range(8):
                sx = np.random.randint(15, width - 15)
                sy = np.random.randint(8, int(height * 0.5))
                s_size = 2.5 + np.random.random() * 3.5
                s_hue = np.random.random()
                self._draw_rainbow_sparkle(painter, sx, sy, s_size, s_hue)

        # Layer 6: Border
        if focused:
            self._draw_rainbow_border(painter, rect, width, height, radius)
        else:
            painter.setBrush(Qt.BrushStyle.NoBrush)
            painter.setPen(QPen(QColor(60, 65, 80, 120), 1.0))
            painter.drawRoundedRect(rect, radius, radius)

    def paint_waveform_panel(self, painter, rect, w, h, cy):
        """Dark recessed panel with rainbow-tinted grid lines and iridescent top."""
        # Dark gradient background with slight blue-teal tint
        panel_grad = QLinearGradient(0, 0, 0, h)
        panel_grad.setColorAt(0.0, QColor(14, 22, 28))
        panel_grad.setColorAt(0.3, QColor(10, 17, 22))
        panel_grad.setColorAt(0.7, QColor(8, 14, 18))
        panel_grad.setColorAt(1.0, QColor(5, 10, 14))
        painter.setBrush(QBrush(panel_grad))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawRoundedRect(rect, 8, 8)

        # Iridescent top highlight - rainbow shimmer across the top edge
        top_holo = QLinearGradient(0, 0, w, 0)
        top_holo_stops = [
            (0.00, QColor(255,  80,  80, 20)),
            (0.20, QColor(255, 220,  60, 25)),
            (0.40, QColor( 60, 255, 120, 22)),
            (0.60, QColor(  0, 220, 255, 28)),
            (0.80, QColor(140,  80, 255, 22)),
            (1.00, QColor(255,  80, 180, 20)),
        ]
        for pos, color in top_holo_stops:
            top_holo.setColorAt(pos, color)
        painter.setBrush(QBrush(top_holo))
        top_highlight_rect = QRectF(rect.x() + 2, rect.y() + 2, w - 4, min(h * 0.12, 18))
        painter.drawRoundedRect(top_highlight_rect, 6, 6)

        # Fade the top highlight downward
        top_fade = QLinearGradient(0, 0, 0, h * 0.15)
        top_fade.setColorAt(0.0, QColor(200, 230, 255, 18))
        top_fade.setColorAt(1.0, QColor(200, 230, 255, 0))
        painter.setBrush(QBrush(top_fade))
        painter.drawRoundedRect(QRectF(rect.x() + 2, rect.y() + 2, w - 4, h * 0.18), 6, 6)

        # Rainbow-tinted grid lines -- each line a different hue
        # Horizontal lines
        h_lines = 4
        for i in range(1, h_lines):
            t = i / h_lines
            # Cycle hue across horizontal lines
            hue = t * 0.6  # Spread across part of spectrum
            r_arr, g_arr, b_arr = _hsv_to_rgb(np.array([hue]), 0.5, 0.8)
            line_color = QColor(int(r_arr[0]), int(g_arr[0]), int(b_arr[0]), 18)
            painter.setPen(QPen(line_color, 1))
            y_pos = int(h * t)
            painter.drawLine(5, y_pos, w - 5, y_pos)

        # Vertical lines
        v_lines = 8
        for i in range(1, v_lines):
            t = i / v_lines
            hue = 0.5 + t * 0.5  # Different hue range than horizontals
            r_arr, g_arr, b_arr = _hsv_to_rgb(np.array([hue % 1.0]), 0.5, 0.8)
            line_color = QColor(int(r_arr[0]), int(g_arr[0]), int(b_arr[0]), 14)
            painter.setPen(QPen(line_color, 1))
            x_pos = int(w * t)
            painter.drawLine(x_pos, 5, x_pos, h - 5)

        # Engraved inset shadows for depth
        for grad, adj in [
            (QLinearGradient(0, 0, 0, 14), rect.adjusted(1, 1, -1, -h + 15)),
            (QLinearGradient(0, 0, 12, 0), rect.adjusted(1, 1, -w + 13, -1)),
            (QLinearGradient(w, 0, w - 12, 0), rect.adjusted(w - 13, 1, -1, -1)),
        ]:
            grad.setColorAt(0, QColor(0, 0, 0, 160))
            grad.setColorAt(1, QColor(0, 0, 0, 0))
            painter.setBrush(QBrush(grad))
            painter.setPen(Qt.PenStyle.NoPen)
            painter.drawRoundedRect(adj, 7, 7)

        # Panel border - dark with subtle rainbow tint
        painter.setBrush(Qt.BrushStyle.NoBrush)
        border_grad = QLinearGradient(0, 0, w, 0)
        border_grad.setColorAt(0.0, QColor(0, 100, 120, 80))
        border_grad.setColorAt(0.5, QColor(80, 60, 140, 80))
        border_grad.setColorAt(1.0, QColor(120, 40, 100, 80))
        painter.setPen(QPen(QBrush(border_grad), 1.5))
        painter.drawRoundedRect(rect, 8, 8)

        # Center line - cyan
        painter.setPen(QPen(QColor(0, 229, 255, 60), 1))
        painter.drawLine(0, int(cy), w, int(cy))
