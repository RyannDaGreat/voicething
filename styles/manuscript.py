"""Paper & Ink / Manuscript style - warm parchment with calligraphic ink accents."""

import numpy as np
from PyQt6.QtCore import Qt, QRectF
from PyQt6.QtGui import (
    QColor, QLinearGradient, QBrush, QImage, QPixmap,
    QPainterPath, QPen
)

from .base import BaseStyle, get_cached_texture


# Parchment / paper colors (warm cream-beige palette)
PARCHMENT_LIGHT = "rgb(245, 235, 218)"
PARCHMENT_MID = "rgb(235, 222, 200)"
PARCHMENT_WARM = "rgb(228, 212, 188)"
PARCHMENT_DARK = "rgb(215, 198, 172)"
PARCHMENT_SHADOW = "rgb(195, 178, 152)"

# Ink colors - deep navy blue (fountain pen ink)
INK_DARK = "rgb(22, 42, 72)"
INK_MID = "rgb(27, 63, 110)"
INK_BRIGHT = "rgb(38, 82, 140)"
INK_LIGHT = "rgb(55, 100, 158)"
INK_FADED = "rgba(27, 63, 110, 0.6)"

# Text colors - dark sepia/brown ink
TEXT_INK = "rgb(52, 38, 28)"
TEXT_INK_DIM = "rgba(62, 48, 35, 0.85)"
TEXT_INK_MUTED = "rgb(120, 100, 78)"
TEXT_INK_DISABLED = "rgb(170, 155, 135)"

# Borders - ruled lines like notebook paper
RULE_DARK = "rgb(160, 142, 118)"
RULE_MID = "rgb(185, 168, 145)"
RULE_LIGHT = "rgb(210, 195, 172)"

# Accent QColor for waveform, timer, etc.
INK_BLUE = QColor(27, 63, 110)
INK_BLUE_CSS = "rgb(27, 63, 110)"

# Subtle tints for hover/selection (ink wash)
INK_WASH_HOVER = "rgba(27, 63, 110, 0.08)"
INK_WASH_BTN = "rgba(27, 63, 110, 0.10)"
INK_WASH_BTN_HOVER = "rgba(27, 63, 110, 0.18)"
INK_WASH_BTN_PRESSED = "rgba(27, 63, 110, 0.30)"


class ManuscriptStyle(BaseStyle):
    name = "manuscript"
    font = "Palatino"

    _parchment_cache = None

    # Warm light theme — ink on parchment
    accent = INK_BLUE
    accent_css = INK_BLUE_CSS
    text_primary = TEXT_INK
    text_secondary = TEXT_INK_DIM
    text_muted = TEXT_INK_MUTED
    text_error = "rgb(160, 45, 35)"
    text_link = INK_MID
    border_color = RULE_MID
    border_dark = RULE_DARK
    icon_color_dark = '#34261c'   # Dark ink on light parchment
    icon_color_light = '#1b3f6e'  # Ink blue for emphasis
    icon_color_muted = '#8a7458'  # Faded sepia

    # Input fields — cream background, dark ink text
    input_bg = '#f5ece0'
    input_text = '#34261c'

    # Slider — ink-colored groove on parchment
    slider_groove = "rgba(27, 63, 110, 0.35)"
    slider_handle = INK_BLUE_CSS
    slider_fill = INK_MID

    # Rotary knob — vintage brass compass dial
    knob_style = "vintage"
    knob_body_dark = "#c8b898"
    knob_body_light = "#e8dcc8"
    knob_notch_style = "needle"
    knob_tickmarks = True
    knob_glow = False
    knob_track_color = "#1b3f6e"  # Ink blue track
    knob_label_color = "#34261c"  # Dark ink text

    # Waveform — ink blue on parchment panel
    waveform_color = INK_BLUE
    waveform_glow = False
    waveform_center_line = QColor(27, 63, 110, 50)
    waveform_panel = "dark"

    # Timer — ink-colored, NOT LCD
    timer_use_lcd = False
    timer_color = INK_BLUE

    # Transcription — parchment panel with ink text
    transcription_text = TEXT_INK
    transcription_text_dimmed = TEXT_INK_DIM
    transcription_panel_bg = PARCHMENT_LIGHT
    transcription_panel_border = RULE_MID
    transcription_row_hover = INK_WASH_HOVER
    transcription_row_btn_bg = INK_WASH_BTN
    transcription_row_btn_hover = INK_WASH_BTN_HOVER
    transcription_row_btn_pressed = INK_WASH_BTN_PRESSED

    # Chime editor — parchment grid with ink cells
    chime_grid_bg = QColor(240, 230, 212)       # Light parchment
    chime_grid_line = QColor(200, 185, 160)      # Ruled line
    chime_cell_inactive = QColor(228, 215, 195)  # Slightly darker parchment
    chime_cell_active = QColor(27, 63, 110)      # Ink blue
    chime_cell_highlight = QColor(27, 63, 110, 70)
    chime_piano_white = QColor(248, 240, 228)    # Ivory/cream keys
    chime_piano_black = QColor(52, 38, 28)       # Dark sepia keys
    chime_piano_label_white = QColor(90, 70, 52)  # Brown text on cream
    chime_piano_label_black = QColor(225, 210, 188)  # Cream text on dark

    def button_css(self):
        # Parchment buttons with ink borders — embossed stationery look
        return (
            f"QPushButton {{ color: {TEXT_INK}; "
            f"background: qlineargradient(x1:0, y1:0, x2:0, y2:1, "
            f"stop:0 rgb(248,240,226), stop:0.1 rgb(242,232,215), "
            f"stop:0.5 rgb(235,222,200), stop:0.9 rgb(228,215,192), "
            f"stop:1 rgb(222,208,185)); "
            f"border: 1px solid {RULE_DARK}; border-top-color: {RULE_LIGHT}; "
            f"border-bottom-color: rgb(145,128,105); "
            f"border-radius: 4px; padding: 3px 8px; font-size: 11px; "
            f"font-family: {self.font}; text-align: left; }}"
            # Hover — ink wash tint
            f"QPushButton:hover {{ color: {INK_DARK}; "
            f"background: qlineargradient(x1:0, y1:0, x2:0, y2:1, "
            f"stop:0 rgb(238,232,222), stop:0.1 rgb(230,222,210), "
            f"stop:0.5 rgb(220,212,198), stop:0.9 rgb(212,202,185), "
            f"stop:1 rgb(205,195,178)); "
            f"border: 1px solid {INK_MID}; }}"
            # Pressed — deeper inset
            f"QPushButton:pressed {{ color: {INK_DARK}; "
            f"background: qlineargradient(x1:0, y1:0, x2:0, y2:1, "
            f"stop:0 rgb(215,200,178), stop:0.1 rgb(222,208,188), "
            f"stop:0.5 rgb(230,218,198), stop:0.9 rgb(235,222,202), "
            f"stop:1 rgb(232,218,195)); "
            f"border: 1px solid rgb(120,105,82); }}"
            # Disabled — washed-out parchment
            f"QPushButton:disabled {{ color: {TEXT_INK_DISABLED}; "
            f"background: rgb(238,230,218); "
            f"border: 1px solid rgb(195,182,162); }}"
            # Checked — ink blue fill
            f"QPushButton:checked {{ color: rgb(245,238,225); "
            f"background: qlineargradient(x1:0, y1:0, x2:0, y2:1, "
            f"stop:0 rgb(55,100,158), stop:0.1 rgb(38,82,140), "
            f"stop:0.5 {INK_MID}, stop:0.9 rgb(22,52,92), "
            f"stop:1 {INK_DARK}); "
            f"border: 1px solid {INK_DARK}; }}"
            f"QPushButton:checked:hover {{ "
            f"background: qlineargradient(x1:0, y1:0, x2:0, y2:1, "
            f"stop:0 rgb(70,115,172), stop:0.1 rgb(50,95,152), "
            f"stop:0.5 rgb(38,82,140), stop:0.9 rgb(27,63,110), "
            f"stop:1 rgb(22,52,92)); }}"
        )

    def menu_css(self):
        return (
            f"QMenu {{ background: qlineargradient(x1:0, y1:0, x2:0, y2:1, "
            f"stop:0 {PARCHMENT_LIGHT}, stop:1 {PARCHMENT_MID}); "
            f"color: {TEXT_INK}; border: 1px solid {RULE_DARK}; "
            f"border-radius: 4px; padding: 4px; "
            f"font-family: {self.font}; font-size: 11px; }}"
            "QMenu::item { padding: 4px 16px; border-radius: 3px; }"
            f"QMenu::item:selected {{ color: rgb(245,238,225); "
            f"background: qlineargradient(x1:0, y1:0, x2:0, y2:1, "
            f"stop:0 {INK_BRIGHT}, stop:0.5 {INK_MID}, stop:1 {INK_DARK}); }}"
            f"QMenu::separator {{ height: 1px; background: {RULE_MID}; margin: 4px 8px; }}"
        )

    def _scrollbar_vertical_css(self):
        # Parchment-toned scrollbar with ink handle
        return (
            f"QScrollBar:vertical {{ width: 14px; "
            f"background: qlineargradient(x1:0, y1:0, x2:1, y2:0, "
            f"stop:0 rgb(230,218,198), stop:0.3 rgb(238,228,210), "
            f"stop:0.7 rgb(238,228,210), stop:1 rgb(230,218,198)); "
            f"border: 1px solid {RULE_MID}; border-radius: 5px; margin: 0px; }}"
            # Handle — ink blue capsule
            "QScrollBar::handle:vertical { "
            "background: qlineargradient(x1:0, y1:0, x2:1, y2:0, "
            "stop:0.0 rgb(45,78,120), stop:0.2 rgb(55,95,145), "
            "stop:0.5 rgb(65,108,160), stop:0.8 rgb(55,95,145), stop:1.0 rgb(45,78,120)); "
            f"border: 1px solid {INK_DARK}; border-radius: 4px; min-height: 40px; margin: 2px; }}"
            # Handle hover
            "QScrollBar::handle:vertical:hover { "
            "background: qlineargradient(x1:0, y1:0, x2:1, y2:0, "
            "stop:0.0 rgb(55,90,135), stop:0.2 rgb(65,108,160), "
            "stop:0.5 rgb(78,122,175), stop:0.8 rgb(65,108,160), stop:1.0 rgb(55,90,135)); "
            "border: 1px solid rgb(30,55,90); }"
            # Handle pressed
            "QScrollBar::handle:vertical:pressed { "
            "background: qlineargradient(x1:0, y1:0, x2:1, y2:0, "
            "stop:0.0 rgb(30,55,88), stop:0.2 rgb(38,68,105), "
            "stop:0.5 rgb(45,78,120), stop:0.8 rgb(38,68,105), stop:1.0 rgb(30,55,88)); "
            f"border: 1px solid {INK_DARK}; }}"
            "QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical { "
            "height: 0; width: 0; background: none; border: none; }"
            "QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical { background: transparent; }"
        )

    def panel_bg_css(self):
        return (
            f"background: qlineargradient(x1:0, y1:0, x2:0, y2:1, "
            f"stop:0 {PARCHMENT_LIGHT}, stop:0.02 {PARCHMENT_MID}, "
            f"stop:0.98 {PARCHMENT_MID}, stop:1 {PARCHMENT_DARK}); "
            f"border: 1px solid {RULE_DARK}; border-radius: 4px;"
        )

    def panel_bg_flat_css(self):
        return (
            f"background: {PARCHMENT_MID}; border: 1px solid {RULE_DARK}; border-radius: 4px;"
        )

    def get_background_pixmap(self, height=512):
        """Procedural parchment texture with paper fiber grain."""
        if ManuscriptStyle._parchment_cache is not None:
            return ManuscriptStyle._parchment_cache

        width = 256
        ManuscriptStyle._parchment_cache = get_cached_texture(
            "parchment", width, height, lambda: self._generate_parchment_texture(width, height)
        )
        return ManuscriptStyle._parchment_cache

    def _generate_parchment_texture(self, width, height):
        """Generate seamless parchment/vellum texture with paper fiber detail."""
        from scipy.ndimage import gaussian_filter, uniform_filter1d

        np.random.seed(1455)  # Gutenberg's printing press year

        # === SEAMLESS FRACTAL NOISE (tileable) ===
        def seamless_fractal_noise(h, w, octaves=4, persistence=0.5):
            """Generate seamless tileable fractal noise."""
            noise = np.zeros((h, w), dtype=np.float32)
            amplitude = 1.0
            for octave in range(octaves):
                freq = 2 ** octave
                seed_h, seed_w = max(2, h // freq), max(2, w // freq)
                seed = np.random.random((seed_h, seed_w)).astype(np.float32)
                layer = np.zeros((h, w), dtype=np.float32)
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

        # Large-scale parchment variation — warm tonal undulation
        organic = seamless_fractal_noise(height, width, octaves=5, persistence=0.55)

        # Fine-scale paper fiber texture — directional noise
        fiber_noise = np.random.randint(0, 30, size=(height, width)).astype(np.float32)
        # Horizontal fiber streaks (paper grain direction)
        fibers_h = uniform_filter1d(fiber_noise, size=25, axis=1, mode='wrap')
        # Finer cross-grain fibers
        fibers_v = uniform_filter1d(
            np.random.randint(0, 15, size=(height, width)).astype(np.float32),
            size=12, axis=0, mode='wrap'
        )
        # Combine: mostly horizontal grain with some cross-grain
        fibers = fibers_h * 0.7 + fibers_v * 0.3

        # Age spots / foxing — subtle brown specks on old paper
        foxing = seamless_fractal_noise(height, width, octaves=2, persistence=0.3)
        foxing_spots = (foxing > 0.82).astype(np.float32)
        foxing_spots = gaussian_filter(foxing_spots, sigma=2.5, mode='wrap') * 0.4

        # Water stain edges — very faint, like old document water damage
        stain = seamless_fractal_noise(height, width, octaves=3, persistence=0.4)
        stain_ring = np.abs(stain - 0.55) < 0.08
        stain_ring = gaussian_filter(stain_ring.astype(np.float32), sigma=3, mode='wrap') * 0.15

        # === BUILD RGB (warm cream-beige parchment) ===
        img = np.zeros((height, width, 4), dtype=np.uint8)

        # Base parchment color: warm cream (235, 222, 200)
        base_r, base_g, base_b = 235, 222, 200

        # Organic tonal variation (subtle warm shifts)
        tone_shift = organic * 18 - 9   # +/-9 variation

        # Fiber texture adds fine grain
        fiber_var = fibers * 0.35

        # Foxing darkens slightly with a yellow-brown tint
        foxing_darken = foxing_spots * 25

        # Water stain edges — slightly darker ring
        stain_darken = stain_ring * 15

        # Compose channels
        r = np.clip(base_r + tone_shift * 1.0 + fiber_var - foxing_darken * 0.8 - stain_darken, 210, 250)
        g = np.clip(base_g + tone_shift * 0.9 + fiber_var * 0.85 - foxing_darken * 1.0 - stain_darken, 195, 240)
        b = np.clip(base_b + tone_shift * 0.7 + fiber_var * 0.65 - foxing_darken * 1.2 - stain_darken, 170, 220)

        img[:, :, 0] = r.astype(np.uint8)
        img[:, :, 1] = g.astype(np.uint8)
        img[:, :, 2] = b.astype(np.uint8)
        img[:, :, 3] = 255

        # Light smoothing for natural paper feel
        for c in range(3):
            img[:, :, c] = gaussian_filter(img[:, :, c].astype(float), sigma=0.6).astype(np.uint8)

        qimg = QImage(img.data, width, height, width * 4, QImage.Format.Format_RGBA8888).copy()
        return QPixmap.fromImage(qimg)

    def _draw_vignette(self, painter, rect, width, height, radius=12):
        """Warm sepia vignette — darkened/aged edges like old paper."""
        for horizontal, alpha_mult in [(True, 0.5), (False, 0.8)]:
            grad = QLinearGradient(0, 0, width if horizontal else 0, 0 if horizontal else height)
            # Sepia-brown darkening at edges
            for pos, alpha in [(0, 85), (0.08, 35), (0.18, 0), (0.82, 0), (0.92, 35), (1, 85)]:
                grad.setColorAt(pos, QColor(80, 55, 30, int(alpha * alpha_mult)))
            painter.setBrush(QBrush(grad))
            painter.setPen(Qt.PenStyle.NoPen)
            painter.drawRoundedRect(rect, radius, radius)

    def _draw_ruled_lines(self, painter, rect, width, height):
        """Draw faint ruled lines like manuscript guidelines."""
        # Horizontal ruled lines — thin, evenly spaced
        line_spacing = 28
        pen = QPen(QColor(180, 162, 135, 55), 1)
        painter.setPen(pen)
        y = rect.y() + line_spacing
        while y < rect.y() + height - line_spacing:
            painter.drawLine(int(rect.x() + 12), int(y), int(rect.x() + width - 12), int(y))
            y += line_spacing

        # Left margin rule — slightly stronger, like a red/ink margin line
        margin_x = rect.x() + 35
        margin_pen = QPen(QColor(140, 80, 60, 45), 1)
        painter.setPen(margin_pen)
        painter.drawLine(int(margin_x), int(rect.y() + 8), int(margin_x), int(rect.y() + height - 8))

    def paint_window(self, painter, rect, width, height, focused=True):
        """Paint parchment texture background with vignette and ruled lines."""
        radius = self.corner_radius

        # Clip to rounded rect
        path = QPainterPath()
        path.addRoundedRect(QRectF(rect), radius, radius)
        painter.setClipPath(path)

        # Draw parchment texture
        parchment = self.get_background_pixmap(max(512, height))
        painter.drawTiledPixmap(rect, parchment)
        painter.setClipping(False)

        # Sepia vignette for aged-paper edges
        self._draw_vignette(painter, rect, width, height, radius)

        # Faint ruled lines
        self._draw_ruled_lines(painter, rect, width, height)

        # Border — thin ruled line, like the edge of a page
        if focused:
            painter.setBrush(Qt.BrushStyle.NoBrush)
            painter.setPen(QPen(QColor(145, 125, 98, 160), 1.5))
            painter.drawRoundedRect(rect, radius, radius)
        else:
            painter.setBrush(Qt.BrushStyle.NoBrush)
            painter.setPen(QPen(QColor(170, 152, 128, 100), 1))
            painter.drawRoundedRect(rect, radius, radius)

    def paint_waveform_panel(self, painter, rect, w, h, cy):
        """Waveform panel — recessed parchment inset like a tipped-in plate."""
        # Slightly darker parchment background — like an inset page
        panel_grad = QLinearGradient(0, 0, 0, h)
        panel_grad.setColorAt(0, QColor(225, 212, 190))
        panel_grad.setColorAt(0.15, QColor(232, 218, 198))
        panel_grad.setColorAt(0.85, QColor(228, 215, 192))
        panel_grad.setColorAt(1, QColor(218, 202, 178))
        painter.setBrush(QBrush(panel_grad))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawRoundedRect(rect, 6, 6)

        # Inset shadow at top — like paper curling into a recess
        top_shadow = QLinearGradient(0, 0, 0, 14)
        top_shadow.setColorAt(0, QColor(100, 75, 50, 65))
        top_shadow.setColorAt(1, QColor(100, 75, 50, 0))
        painter.setBrush(QBrush(top_shadow))
        painter.drawRoundedRect(rect.adjusted(1, 1, -1, -h + 15), 5, 5)

        # Left inset shadow
        left_shadow = QLinearGradient(0, 0, 12, 0)
        left_shadow.setColorAt(0, QColor(100, 75, 50, 55))
        left_shadow.setColorAt(1, QColor(100, 75, 50, 0))
        painter.setBrush(QBrush(left_shadow))
        painter.drawRoundedRect(rect.adjusted(1, 1, -w + 13, -1), 5, 5)

        # Right inset shadow
        right_shadow = QLinearGradient(w, 0, w - 12, 0)
        right_shadow.setColorAt(0, QColor(100, 75, 50, 45))
        right_shadow.setColorAt(1, QColor(100, 75, 50, 0))
        painter.setBrush(QBrush(right_shadow))
        painter.drawRoundedRect(rect.adjusted(w - 13, 1, -1, -1), 5, 5)

        # Subtle ruled grid — manuscript guidelines
        painter.setPen(QPen(QColor(27, 63, 110, 25), 1))
        for i in range(1, 4):
            y = int(h * i / 4)
            painter.drawLine(5, y, w - 5, y)

        # Border — inked ruled edge
        painter.setBrush(Qt.BrushStyle.NoBrush)
        painter.setPen(QPen(QColor(145, 128, 105), 1.5))
        painter.drawRoundedRect(rect, 6, 6)

        # Inner highlight — slight cream glow at top
        painter.setPen(QPen(QColor(248, 240, 225, 80), 1))
        painter.drawRoundedRect(rect.adjusted(2, 2, -2, -2), 4, 4)

        # Center line — faint ink rule
        painter.setPen(QPen(QColor(27, 63, 110, 55), 1))
        painter.drawLine(0, int(cy), w, int(cy))
