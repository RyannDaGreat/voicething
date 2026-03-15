"""Filigree style - gothic cathedral architecture inspired by Hollow Knight's City of Tears.

Pointed arches, stone tracery, pillar capitals, and rain-weathered elegance.
All ornaments in mauve on deep blue-black void.
"""

import math
import numpy as np
from PyQt6.QtCore import Qt, QRectF, QPointF
from PyQt6.QtGui import (
    QColor, QLinearGradient, QBrush, QImage, QPixmap,
    QPainterPath, QPen
)

from .base import BaseStyle, get_cached_texture

# --- Hollow Knight palette (no gold) ---
VOID_BLACK = "rgb(15, 15, 27)"
VOID_DEEP = "rgb(20, 20, 35)"
SLATE_DARK = "rgb(55, 58, 75)"
SLATE_MID = "rgb(86, 90, 117)"
MAUVE_ORNAMENT = "rgb(198, 183, 190)"
OFF_WHITE = "rgb(250, 251, 246)"
DEEP_PURPLE = "rgb(45, 0, 78)"

# Derived alpha variants
MAUVE_Q = QColor(198, 183, 190)
VOID_BLACK_Q = QColor(15, 15, 27)
VOID_DEEP_Q = QColor(20, 20, 35)
SLATE_DARK_Q = QColor(55, 58, 75)
SLATE_MID_Q = QColor(86, 90, 117)


class FiligreeGothicStyle(BaseStyle):
    """Command, specific. Gothic cathedral theme for VoiceThing."""

    name = "filigree_gothic"
    font = "Palatino"

    _texture_cache = None

    accent = MAUVE_Q
    accent_css = MAUVE_ORNAMENT
    text_primary = OFF_WHITE
    text_secondary = MAUVE_ORNAMENT
    text_muted = SLATE_MID
    text_error = "rgb(200, 85, 75)"
    text_link = MAUVE_ORNAMENT
    border_color = SLATE_MID
    border_dark = SLATE_DARK
    icon_color_dark = '#373a4b'
    icon_color_light = '#fafbf6'
    icon_color_muted = '#565a75'

    input_bg = '#14141f'
    input_text = '#fafbf6'

    slider_groove = "rgba(15,15,27,0.85)"
    slider_handle = MAUVE_ORNAMENT
    slider_fill = SLATE_MID

    knob_style = "vintage"
    knob_body_dark = "#373a4b"
    knob_body_light = "#565a75"
    knob_notch_style = "needle"
    knob_tickmarks = True
    knob_glow = False
    knob_track_color = "#c6b7be"
    knob_label_color = "#fafbf6"

    waveform_color = MAUVE_Q
    waveform_glow = True
    waveform_glow_radius = 14
    waveform_glow_alpha = 140
    waveform_center_line = QColor(198, 183, 190, 40)
    waveform_panel = "dark"

    timer_use_lcd = True
    timer_color = MAUVE_Q

    transcription_text = OFF_WHITE
    transcription_text_dimmed = SLATE_MID
    transcription_panel_bg = "rgba(15, 15, 27, 128)"
    transcription_panel_border = "rgba(12, 12, 22, 160)"
    transcription_row_hover = "rgba(198, 183, 190, 0.08)"
    transcription_row_btn_bg = "rgba(198, 183, 190, 0.10)"
    transcription_row_btn_hover = "rgba(198, 183, 190, 0.18)"
    transcription_row_btn_pressed = "rgba(198, 183, 190, 0.32)"

    chime_grid_bg = QColor(18, 18, 30)
    chime_grid_line = QColor(40, 42, 58)
    chime_cell_inactive = QColor(28, 28, 42)
    chime_cell_active = MAUVE_Q
    chime_cell_highlight = QColor(198, 183, 190, 70)
    chime_piano_white = QColor(240, 238, 232)
    chime_piano_black = QColor(20, 20, 32)
    chime_piano_label_white = QColor(55, 58, 75)
    chime_piano_label_black = QColor(198, 183, 190)

    # ── Button CSS ──────────────────────────────────────────────────

    def button_css(self):
        """Command, specific. Returns gothic-styled button CSS."""
        return (
            # Normal - void background, slate border
            f"QPushButton {{ color: {SLATE_MID}; "
            f"background: qlineargradient(x1:0, y1:0, x2:0, y2:1, "
            f"stop:0 rgb(35,36,52), stop:0.06 rgb(25,26,40), "
            f"stop:0.94 rgb(18,18,30), stop:1 rgb(12,12,22)); "
            f"border: 1px solid {SLATE_DARK}; border-top-color: rgb(65,68,85); "
            f"border-radius: 2px; padding: 3px 8px; font-size: 11px; "
            f"font-family: {self.font}; text-align: left; }}"
            # Hover - mauve text, lighter border
            f"QPushButton:hover {{ color: {MAUVE_ORNAMENT}; "
            f"background: qlineargradient(x1:0, y1:0, x2:0, y2:1, "
            f"stop:0 rgb(42,44,62), stop:0.06 rgb(32,34,50), "
            f"stop:0.94 rgb(22,22,36), stop:1 rgb(15,15,27)); "
            f"border: 1px solid {SLATE_MID}; border-top-color: rgb(110,114,140); }}"
            # Pressed - inset
            f"QPushButton:pressed {{ color: {OFF_WHITE}; "
            f"background: qlineargradient(x1:0, y1:0, x2:0, y2:1, "
            f"stop:0 rgb(15,15,27), stop:0.06 rgb(22,22,36), "
            f"stop:0.94 rgb(32,34,50), stop:1 rgb(25,26,40)); "
            f"border: 1px solid rgb(40,42,58); }}"
            # Disabled
            f"QPushButton:disabled {{ color: rgb(50,52,65); "
            f"background: {VOID_BLACK}; border: 1px solid rgb(30,30,45); }}"
            # Checked - cool mauve highlight (no warm brown)
            f"QPushButton:checked {{ color: {OFF_WHITE}; "
            f"background: qlineargradient(x1:0, y1:0, x2:0, y2:1, "
            f"stop:0 rgb(108,100,115), stop:0.06 rgb(82,76,92), "
            f"stop:0.94 rgb(55,50,68), stop:1 rgb(40,36,52)); "
            f"border: 1px solid rgb(130,122,138); }}"
            f"QPushButton:checked:hover {{ "
            f"background: qlineargradient(x1:0, y1:0, x2:0, y2:1, "
            f"stop:0 rgb(128,118,135), stop:0.06 rgb(100,92,110), "
            f"stop:0.94 rgb(68,62,82), stop:1 rgb(50,44,62)); }}"
        )

    def menu_css(self):
        """Command, specific. Returns gothic-styled context menu CSS."""
        return (
            f"QMenu {{ background: {VOID_BLACK}; color: {OFF_WHITE}; "
            f"border: 2px solid {SLATE_DARK}; border-radius: 3px; padding: 4px; "
            f"font-family: {self.font}; font-size: 11px; }}"
            "QMenu::item { padding: 4px 16px; border-radius: 2px; }"
            f"QMenu::item:selected {{ color: {OFF_WHITE}; "
            f"background: qlineargradient(x1:0, y1:0, x2:0, y2:1, "
            f"stop:0 rgb(100,94,100), stop:0.5 rgb(75,68,76), stop:1 rgb(55,50,58)); }}"
            f"QMenu::separator {{ height: 2px; background: {SLATE_DARK}; margin: 4px 8px; }}"
        )

    def _scrollbar_vertical_css(self):
        """Command, specific. Vertical scrollbar in void/slate tones."""
        return (
            f"QScrollBar:vertical {{ width: 14px; background: {VOID_BLACK}; "
            f"border: 1px solid rgb(30,30,45); border-radius: 5px; margin: 0px; }}"
            "QScrollBar::handle:vertical { "
            "background: qlineargradient(x1:0, y1:0, x2:1, y2:0, "
            f"stop:0.0 rgb(45,48,65), stop:0.2 rgb(60,63,80), "
            f"stop:0.5 rgb(72,75,95), stop:0.8 rgb(60,63,80), stop:1.0 rgb(45,48,65)); "
            f"border: 1px solid {SLATE_DARK}; border-radius: 4px; min-height: 40px; margin: 2px; }}"
            "QScrollBar::handle:vertical:hover { "
            "background: qlineargradient(x1:0, y1:0, x2:1, y2:0, "
            f"stop:0.0 rgb(60,63,80), stop:0.2 rgb(75,78,98), "
            f"stop:0.5 rgb(90,93,115), stop:0.8 rgb(75,78,98), stop:1.0 rgb(60,63,80)); "
            f"border: 1px solid {SLATE_MID}; }}"
            "QScrollBar::handle:vertical:pressed { "
            "background: qlineargradient(x1:0, y1:0, x2:1, y2:0, "
            f"stop:0.0 rgb(35,36,52), stop:0.2 rgb(45,48,65), "
            f"stop:0.5 rgb(55,58,75), stop:0.8 rgb(45,48,65), stop:1.0 rgb(35,36,52)); "
            f"border: 1px solid rgb(40,42,58); }}"
            "QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical { "
            "height: 0; width: 0; background: none; border: none; }"
            "QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical { background: transparent; }"
        )

    def panel_bg_css(self):
        """Command, specific. Returns CSS for raised panel backgrounds."""
        return (
            f"background: qlineargradient(x1:0, y1:0, x2:0, y2:1, "
            f"stop:0 rgba(32,34,50,128), stop:0.02 rgba(24,25,40,128), "
            f"stop:0.98 rgba(18,18,30,128), stop:1 rgba(12,12,22,128)); "
            f"border: 1px solid {SLATE_DARK}; border-radius: 3px;"
        )

    def panel_bg_flat_css(self):
        """Command, specific. Returns CSS for flat panel backgrounds."""
        return (
            f"background: rgba(15, 15, 27, 128); border: 1px solid rgb(30,30,45); border-radius: 3px;"
        )

    # ── Texture generation ──────────────────────────────────────────

    def get_background_pixmap(self, height=512):
        """Command, specific. Returns tiled void texture pixmap (cached)."""
        if FiligreeGothicStyle._texture_cache is not None:
            return FiligreeGothicStyle._texture_cache

        width = 256
        FiligreeGothicStyle._texture_cache = get_cached_texture(
            "filigree", width, height, lambda: self._generate_texture(width, height)
        )
        return FiligreeGothicStyle._texture_cache

    def _generate_texture(self, width, height):
        """Command, specific. Generates dark blue-black void texture with subtle noise.

        Returns:
            QPixmap: (width x height) RGBA tileable texture
        """
        from scipy.ndimage import gaussian_filter

        np.random.seed(1093)  # Gothic era

        img = np.zeros((height, width, 4), dtype=np.uint8)
        base_r, base_g, base_b = 16, 16, 28

        # Subtle fractal noise for stone-like grain
        noise = np.random.random((height, width)).astype(np.float32)
        noise = gaussian_filter(noise, sigma=3.0, mode='wrap')
        noise = (noise - noise.min()) / (noise.max() - noise.min() + 1e-6)

        # Slow tileable sine variation for depth
        xs = np.arange(width)[None, :].astype(np.float64)
        ys = np.arange(height)[:, None].astype(np.float64)
        tau_x = 2 * math.pi * xs / width
        tau_y = 2 * math.pi * ys / height
        wave = (
            np.sin(tau_x * 2 + tau_y * 1) * 0.15
            + np.sin(tau_y * 3 - tau_x * 1 + 0.8) * 0.10
        )

        variation = 0.85 + wave + noise * 0.15

        img[:, :, 0] = np.clip(base_r * variation, 10, 30).astype(np.uint8)
        img[:, :, 1] = np.clip(base_g * variation, 10, 30).astype(np.uint8)
        img[:, :, 2] = np.clip(base_b * variation, 18, 45).astype(np.uint8)
        img[:, :, 3] = 255

        for c in range(3):
            img[:, :, c] = gaussian_filter(
                img[:, :, c].astype(float), sigma=1.0, mode='wrap'
            ).astype(np.uint8)

        qimg = QImage(img.data, width, height, width * 4, QImage.Format.Format_RGBA8888).copy()
        return QPixmap.fromImage(qimg)

    # ── Gothic ornament drawing helpers ─────────────────────────────

    def _draw_pointed_arch(self, painter, cx, base_y, arch_width, arch_height, pen):
        """Command, specific. Draws a single pointed Gothic arch (lancet arch).

        The arch apex is at (cx, base_y - arch_height). The two sides curve
        outward from the base corners and meet at the apex in a pointed tip.

        Args:
            painter: QPainter
            cx (float): Center x of the arch
            base_y (float): Y coordinate of the arch base (bottom)
            arch_width (float): Full width at the base
            arch_height (float): Height from base to apex
            pen (QPen): Pen to draw with
        """
        half_w = arch_width / 2.0
        apex = QPointF(cx, base_y - arch_height)
        left_base = QPointF(cx - half_w, base_y)
        right_base = QPointF(cx + half_w, base_y)

        # Control points: each side bulges outward, then converges sharply at apex
        # The "pointedness" comes from control points being close to the apex vertically
        bulge = half_w * 0.35
        ctrl_height = arch_height * 0.55

        path = QPainterPath()
        path.moveTo(left_base)
        path.cubicTo(
            QPointF(cx - half_w - bulge, base_y - ctrl_height),
            QPointF(cx - half_w * 0.15, base_y - arch_height * 0.92),
            apex,
        )
        path.cubicTo(
            QPointF(cx + half_w * 0.15, base_y - arch_height * 0.92),
            QPointF(cx + half_w + bulge, base_y - ctrl_height),
            right_base,
        )

        painter.setBrush(Qt.BrushStyle.NoBrush)
        painter.setPen(pen)
        painter.drawPath(path)

    def _draw_trefoil(self, painter, cx, cy, radius, pen):
        """Command, specific. Draws a trefoil (three-lobed) motif inside a circle.

        Common in Gothic tracery windows. Three overlapping circles arranged
        120 degrees apart, inscribed in a bounding circle of the given radius.

        Args:
            painter: QPainter
            cx, cy (float): Center of the trefoil
            radius (float): Bounding radius
            pen (QPen): Pen to draw with
        """
        painter.setBrush(Qt.BrushStyle.NoBrush)
        painter.setPen(pen)
        lobe_r = radius * 0.52
        lobe_offset = radius * 0.42
        for angle_deg in [90, 210, 330]:
            angle_rad = math.radians(angle_deg)
            lx = cx + lobe_offset * math.cos(angle_rad)
            ly = cy - lobe_offset * math.sin(angle_rad)
            painter.drawEllipse(QPointF(lx, ly), lobe_r, lobe_r)

    def _draw_tracery_circle(self, painter, cx, cy, radius, pen):
        """Command, specific. Draws a Gothic tracery rosette: outer circle + inner trefoil.

        Args:
            painter: QPainter
            cx, cy (float): Center
            radius (float): Outer circle radius
            pen (QPen): Pen to draw with
        """
        painter.setBrush(Qt.BrushStyle.NoBrush)
        painter.setPen(pen)
        painter.drawEllipse(QPointF(cx, cy), radius, radius)
        self._draw_trefoil(painter, cx, cy, radius * 0.85, pen)

    def _draw_finial(self, painter, cx, base_y, finial_height, pen):
        """Command, specific. Draws an upward-pointing Gothic finial (decorative spike tip).

        A narrow pointed shape tapering from base to a sharp apex,
        with slight bulges on the sides like a crocket.

        Args:
            painter: QPainter
            cx (float): Center x
            base_y (float): Bottom of the finial
            finial_height (float): Height of the finial
            pen (QPen): Pen to draw with
        """
        apex = QPointF(cx, base_y - finial_height)
        path = QPainterPath()
        half_base = finial_height * 0.18
        path.moveTo(QPointF(cx - half_base, base_y))
        path.cubicTo(
            QPointF(cx - half_base * 1.6, base_y - finial_height * 0.4),
            QPointF(cx - half_base * 0.3, base_y - finial_height * 0.75),
            apex,
        )
        path.cubicTo(
            QPointF(cx + half_base * 0.3, base_y - finial_height * 0.75),
            QPointF(cx + half_base * 1.6, base_y - finial_height * 0.4),
            QPointF(cx + half_base, base_y),
        )
        painter.setBrush(Qt.BrushStyle.NoBrush)
        painter.setPen(pen)
        painter.drawPath(path)

    def _draw_pillar(self, painter, x, top_y, bottom_y, pen, cap_pen):
        """Command, specific. Draws a vertical pillar line with an ornamental capital at top.

        The capital is a small flared bracket shape above the pillar shaft.

        Args:
            painter: QPainter
            x (float): X position of the pillar
            top_y (float): Top of the pillar shaft (capital sits above this)
            bottom_y (float): Bottom of the pillar
            pen (QPen): Pen for the shaft
            cap_pen (QPen): Pen for the capital ornament
        """
        # Shaft
        painter.setPen(pen)
        painter.drawLine(QPointF(x, top_y), QPointF(x, bottom_y))

        # Capital — small flared bracket
        cap_h = 8
        cap_w = 6
        cap_top = top_y - 2
        path = QPainterPath()
        path.moveTo(QPointF(x - cap_w, cap_top + cap_h))
        path.cubicTo(
            QPointF(x - cap_w, cap_top + cap_h * 0.3),
            QPointF(x - cap_w * 0.3, cap_top),
            QPointF(x, cap_top),
        )
        path.cubicTo(
            QPointF(x + cap_w * 0.3, cap_top),
            QPointF(x + cap_w, cap_top + cap_h * 0.3),
            QPointF(x + cap_w, cap_top + cap_h),
        )
        painter.setBrush(Qt.BrushStyle.NoBrush)
        painter.setPen(cap_pen)
        painter.drawPath(path)

    def _draw_cathedral_window(self, painter, width, height):
        """Command, specific. Draws a large faint pointed arch as a background motif.

        Creates the impression of a massive Gothic cathedral window behind
        the UI content. Very low alpha — atmospheric, not competing with UI.

        Args:
            painter: QPainter
            width (int): Window width
            height (int): Window height
        """
        # Large central pointed arch spanning most of the window
        cx = width / 2.0
        arch_w = width * 0.65
        arch_h = height * 0.75
        base_y = height * 0.88

        # Outermost arch — very subtle
        outer_pen = QPen(QColor(198, 183, 190, 14), 1.2)
        outer_pen.setCapStyle(Qt.PenCapStyle.RoundCap)
        self._draw_pointed_arch(painter, cx, base_y, arch_w, arch_h, outer_pen)

        # Inner arch — even fainter
        inner_pen = QPen(QColor(198, 183, 190, 9), 0.8)
        inner_pen.setCapStyle(Qt.PenCapStyle.RoundCap)
        self._draw_pointed_arch(
            painter, cx, base_y - 4, arch_w * 0.82, arch_h * 0.86, inner_pen
        )

    # ── Main painting ───────────────────────────────────────────────

    def _draw_vignette(self, painter, rect, width, height, radius=12):
        """Command, specific. Draws dark vignette overlay for depth framing."""
        for horizontal, alpha_mult in [(True, 0.55), (False, 0.75)]:
            grad = QLinearGradient(
                0, 0,
                width if horizontal else 0,
                0 if horizontal else height,
            )
            for pos, alpha in [(0, 160), (0.06, 80), (0.20, 25), (0.80, 25), (0.94, 80), (1, 160)]:
                grad.setColorAt(pos, QColor(10, 10, 20, int(alpha * alpha_mult)))
            painter.setBrush(QBrush(grad))
            painter.setPen(Qt.PenStyle.NoPen)
            painter.drawRoundedRect(rect, radius, radius)

    def _draw_top_arches(self, painter, width):
        """Command, specific. Draws a row of pointed Gothic arches along the top edge.

        Creates a railing-like pattern reminiscent of City of Tears architecture.
        Arches are evenly spaced with finials at each apex. Three layers:
        outer arch, inner echo, and tiny trefoil at center.

        Args:
            painter: QPainter
            width (int): Window width
        """
        arch_count = max(4, int(width / 75))
        arch_spacing = width / arch_count
        arch_w = arch_spacing * 0.82
        arch_h = 38
        base_y = 26

        # Primary arches — most visible layer
        primary_pen = QPen(QColor(198, 183, 190, 90), 1.5)
        primary_pen.setCapStyle(Qt.PenCapStyle.RoundCap)
        # Echo arches (ghostly inner)
        echo_pen = QPen(QColor(198, 183, 190, 40), 1.0)
        echo_pen.setCapStyle(Qt.PenCapStyle.RoundCap)
        # Finial pen
        finial_pen = QPen(QColor(198, 183, 190, 65), 1.2)
        finial_pen.setCapStyle(Qt.PenCapStyle.RoundCap)
        # Tiny trefoil pen
        trefoil_pen = QPen(QColor(198, 183, 190, 30), 0.7)
        trefoil_pen.setCapStyle(Qt.PenCapStyle.RoundCap)

        # Connecting horizontal line at arch base
        painter.setPen(QPen(QColor(198, 183, 190, 50), 1.0))
        painter.drawLine(QPointF(6, base_y), QPointF(width - 6, base_y))
        # Second thinner line just below
        painter.setPen(QPen(QColor(198, 183, 190, 25), 0.6))
        painter.drawLine(QPointF(6, base_y + 3), QPointF(width - 6, base_y + 3))

        # Cusp dot pen — small dots at arch base junctions
        cusp_pen = QPen(QColor(198, 183, 190, 60), 1.0)

        for i in range(arch_count):
            cx = arch_spacing * (i + 0.5)
            self._draw_pointed_arch(painter, cx, base_y, arch_w, arch_h, primary_pen)
            # Inner echo arch
            self._draw_pointed_arch(
                painter, cx, base_y - 1, arch_w * 0.58, arch_h * 0.65, echo_pen
            )
            # Finial at apex — taller
            self._draw_finial(painter, cx, base_y - arch_h + 3, 14, finial_pen)
            # Tiny trefoil in the spandrel area between arches
            trefoil_y = base_y - arch_h * 0.35
            self._draw_trefoil(painter, cx, trefoil_y, 4, trefoil_pen)

            # Cusp dots at base of each arch (where arch feet meet the base line)
            painter.setPen(Qt.PenStyle.NoPen)
            painter.setBrush(QColor(198, 183, 190, 50))
            dot_r = 1.8
            painter.drawEllipse(QPointF(cx - arch_w / 2, base_y), dot_r, dot_r)
            painter.drawEllipse(QPointF(cx + arch_w / 2, base_y), dot_r, dot_r)

        # Diamond lozenges between arch pairs along the base line
        lozenge_pen = QPen(QColor(198, 183, 190, 40), 0.8)
        lozenge_pen.setCapStyle(Qt.PenCapStyle.RoundCap)
        loz_size = 3.5
        for i in range(arch_count - 1):
            junction_x = arch_spacing * (i + 1)
            path = QPainterPath()
            path.moveTo(QPointF(junction_x, base_y - loz_size))
            path.lineTo(QPointF(junction_x + loz_size, base_y))
            path.lineTo(QPointF(junction_x, base_y + loz_size))
            path.lineTo(QPointF(junction_x - loz_size, base_y))
            path.closeSubpath()
            painter.setBrush(Qt.BrushStyle.NoBrush)
            painter.setPen(lozenge_pen)
            painter.drawPath(path)

    def _draw_bottom_arches(self, painter, width, height):
        """Command, specific. Draws inverted pointed arches along the bottom edge.

        Mirrors the top arch pattern but inverted (pointing downward).
        Slightly smaller than top arches for visual hierarchy.

        Args:
            painter: QPainter
            width (int): Window width
            height (int): Window height
        """
        arch_count = max(3, int(width / 100))
        arch_spacing = width / arch_count
        arch_w = arch_spacing * 0.65
        arch_h = 22
        base_y = height - 16

        pen = QPen(QColor(198, 183, 190, 55), 1.2)
        pen.setCapStyle(Qt.PenCapStyle.RoundCap)
        echo_pen = QPen(QColor(198, 183, 190, 25), 0.8)
        echo_pen.setCapStyle(Qt.PenCapStyle.RoundCap)

        # Connecting line
        painter.setPen(QPen(QColor(198, 183, 190, 40), 0.8))
        painter.drawLine(QPointF(6, base_y), QPointF(width - 6, base_y))

        for i in range(arch_count):
            cx = arch_spacing * (i + 0.5)
            # Inverted arch: flip by drawing base_y upward and arch going down
            half_w = arch_w / 2.0
            apex = QPointF(cx, base_y + arch_h)
            left_base = QPointF(cx - half_w, base_y)
            right_base = QPointF(cx + half_w, base_y)
            bulge = half_w * 0.35
            ctrl_depth = arch_h * 0.55

            path = QPainterPath()
            path.moveTo(left_base)
            path.cubicTo(
                QPointF(cx - half_w - bulge, base_y + ctrl_depth),
                QPointF(cx - half_w * 0.15, base_y + arch_h * 0.92),
                apex,
            )
            path.cubicTo(
                QPointF(cx + half_w * 0.15, base_y + arch_h * 0.92),
                QPointF(cx + half_w + bulge, base_y + ctrl_depth),
                right_base,
            )
            painter.setBrush(Qt.BrushStyle.NoBrush)
            painter.setPen(pen)
            painter.drawPath(path)

            # Inner echo
            inner_half_w = half_w * 0.55
            inner_h = arch_h * 0.6
            inner_apex = QPointF(cx, base_y + inner_h)
            path2 = QPainterPath()
            path2.moveTo(QPointF(cx - inner_half_w, base_y))
            path2.cubicTo(
                QPointF(cx - inner_half_w - inner_half_w * 0.3, base_y + inner_h * 0.55),
                QPointF(cx - inner_half_w * 0.15, base_y + inner_h * 0.92),
                inner_apex,
            )
            path2.cubicTo(
                QPointF(cx + inner_half_w * 0.15, base_y + inner_h * 0.92),
                QPointF(cx + inner_half_w + inner_half_w * 0.3, base_y + inner_h * 0.55),
                QPointF(cx + inner_half_w, base_y),
            )
            painter.setPen(echo_pen)
            painter.drawPath(path2)

    def _draw_side_pillars(self, painter, width, height):
        """Command, specific. Draws pillar-like vertical ornaments on left and right edges.

        Each side gets two pillars (inner and outer) with ornamental capitals,
        plus small connecting arch motifs between them.
        Bilateral symmetry is maintained.

        Args:
            painter: QPainter
            width (int): Window width
            height (int): Window height
        """
        shaft_pen = QPen(QColor(198, 183, 190, 65), 1.3)
        shaft_pen.setCapStyle(Qt.PenCapStyle.RoundCap)
        cap_pen = QPen(QColor(198, 183, 190, 80), 1.5)
        cap_pen.setCapStyle(Qt.PenCapStyle.RoundCap)
        inner_shaft_pen = QPen(QColor(198, 183, 190, 35), 0.9)
        inner_shaft_pen.setCapStyle(Qt.PenCapStyle.RoundCap)
        inner_cap_pen = QPen(QColor(198, 183, 190, 48), 1.0)
        inner_cap_pen.setCapStyle(Qt.PenCapStyle.RoundCap)

        top_margin = 30
        bottom_margin = height - 20

        # Outer pillars
        for x in [10, width - 10]:
            self._draw_pillar(painter, x, top_margin, bottom_margin, shaft_pen, cap_pen)
        # Inner pillars (fainter)
        for x in [20, width - 20]:
            self._draw_pillar(
                painter, x, top_margin + 8, bottom_margin - 6,
                inner_shaft_pen, inner_cap_pen,
            )

        # Small connecting arches between inner and outer pillar pairs (at top)
        connecting_pen = QPen(QColor(198, 183, 190, 35), 0.8)
        connecting_pen.setCapStyle(Qt.PenCapStyle.RoundCap)
        for left_x, right_x in [(10, 20), (width - 20, width - 10)]:
            cx = (left_x + right_x) / 2
            self._draw_pointed_arch(
                painter, cx, top_margin + 10, (right_x - left_x) * 1.2, 12, connecting_pen
            )

    def _draw_tracery_band(self, painter, width, y_center):
        """Command, specific. Draws a horizontal band of tracery rosettes.

        A decorative divider line with trefoil-inscribed circles and connecting
        pointed arches between them, like the tracery in a Gothic window.

        Args:
            painter: QPainter
            width (int): Window width
            y_center (float): Y position for the band center
        """
        rosette_pen = QPen(QColor(198, 183, 190, 55), 1.0)
        rosette_pen.setCapStyle(Qt.PenCapStyle.RoundCap)

        # Horizontal lines flanking the rosettes — double line
        line_pen = QPen(QColor(198, 183, 190, 30), 0.8)
        painter.setPen(line_pen)
        painter.drawLine(QPointF(26, y_center - 12), QPointF(width - 26, y_center - 12))
        painter.drawLine(QPointF(26, y_center + 12), QPointF(width - 26, y_center + 12))

        # Rosettes — larger
        rosette_count = max(3, int(width / 120))
        spacing = (width - 60) / max(1, rosette_count - 1) if rosette_count > 1 else 0
        start_x = 30 if rosette_count > 1 else width / 2.0
        rosette_r = 11

        for i in range(rosette_count):
            cx = start_x + spacing * i
            self._draw_tracery_circle(painter, cx, y_center, rosette_r, rosette_pen)

        # Small pointed arches connecting the rosettes
        arch_pen = QPen(QColor(198, 183, 190, 25), 0.7)
        arch_pen.setCapStyle(Qt.PenCapStyle.RoundCap)
        if rosette_count > 1:
            for i in range(rosette_count - 1):
                left_cx = start_x + spacing * i
                right_cx = start_x + spacing * (i + 1)
                mid_x = (left_cx + right_cx) / 2
                gap = right_cx - left_cx - rosette_r * 2
                if gap > 10:
                    self._draw_pointed_arch(
                        painter, mid_x, y_center + 10, gap * 0.7, 16, arch_pen
                    )

    def _draw_corner_arches(self, painter, width, height, alpha=50):
        """Command, specific. Draws small pointed arch motifs at each corner.

        These create visual brackets at the window corners, reinforcing
        the gothic framing. Bilateral symmetry across both axes.

        Args:
            painter: QPainter
            width (int): Window width
            height (int): Window height
            alpha (int): Base opacity for the ornaments
        """
        pen = QPen(QColor(198, 183, 190, alpha), 1.2)
        pen.setCapStyle(Qt.PenCapStyle.RoundCap)
        arch_size = min(width, height) * 0.10
        margin = 5

        # Top-left
        path = QPainterPath()
        path.moveTo(QPointF(margin, margin + arch_size))
        path.cubicTo(
            QPointF(margin, margin + arch_size * 0.3),
            QPointF(margin + arch_size * 0.3, margin),
            QPointF(margin + arch_size, margin),
        )
        painter.setBrush(Qt.BrushStyle.NoBrush)
        painter.setPen(pen)
        painter.drawPath(path)

        # Top-right (mirror)
        path = QPainterPath()
        path.moveTo(QPointF(width - margin, margin + arch_size))
        path.cubicTo(
            QPointF(width - margin, margin + arch_size * 0.3),
            QPointF(width - margin - arch_size * 0.3, margin),
            QPointF(width - margin - arch_size, margin),
        )
        painter.drawPath(path)

        # Bottom-left
        path = QPainterPath()
        path.moveTo(QPointF(margin, height - margin - arch_size))
        path.cubicTo(
            QPointF(margin, height - margin - arch_size * 0.3),
            QPointF(margin + arch_size * 0.3, height - margin),
            QPointF(margin + arch_size, height - margin),
        )
        painter.drawPath(path)

        # Bottom-right
        path = QPainterPath()
        path.moveTo(QPointF(width - margin, height - margin - arch_size))
        path.cubicTo(
            QPointF(width - margin, height - margin - arch_size * 0.3),
            QPointF(width - margin - arch_size * 0.3, height - margin),
            QPointF(width - margin - arch_size, height - margin),
        )
        painter.drawPath(path)

    def paint_window(self, painter, rect, width, height, focused=True):
        """Command, specific. Paints gothic cathedral window background with ornaments.

        Layers (back to front):
        1. Tiled void texture
        2. Vignette overlay
        3. Subtle purple glow when focused
        4. Gothic arch row along top
        5. Inverted arch row along bottom
        6. Side pillars with capitals
        7. Corner arch brackets
        8. Tracery band at ~40% height
        9. Border frame

        Args:
            painter: QPainter
            rect (QRectF): Window rectangle
            width (int): Window width
            height (int): Window height
            focused (bool): Whether window has focus
        """
        radius = self.corner_radius

        # Clip to rounded rect
        clip = QPainterPath()
        clip.addRoundedRect(QRectF(rect), radius, radius)
        painter.setClipPath(clip)

        # 1. Tiled void texture
        texture = self.get_background_pixmap(max(512, height))
        painter.drawTiledPixmap(rect, texture)

        # 2. Vignette
        self._draw_vignette(painter, rect, width, height, radius)

        # 3. Focused glow — faint purple from top
        if focused:
            top_glow = QLinearGradient(0, 0, 0, 60)
            top_glow.setColorAt(0, QColor(45, 0, 78, 22))
            top_glow.setColorAt(1, QColor(45, 0, 78, 0))
            painter.setBrush(QBrush(top_glow))
            painter.setPen(Qt.PenStyle.NoPen)
            painter.drawRoundedRect(QRectF(rect.x(), rect.y(), width, 60), radius, radius)

        # Unclip to allow ornaments to extend beyond window edges
        painter.setClipping(False)

        ornament_alpha_mult = 1.0 if focused else 0.55

        # 4. Cathedral window background motif (deepest layer)
        painter.save()
        painter.setOpacity(ornament_alpha_mult)
        self._draw_cathedral_window(painter, width, height)
        painter.restore()

        # 5. Top arches
        painter.save()
        painter.setOpacity(ornament_alpha_mult)
        self._draw_top_arches(painter, width)
        painter.restore()

        # 6. Bottom arches
        painter.save()
        painter.setOpacity(ornament_alpha_mult)
        self._draw_bottom_arches(painter, width, height)
        painter.restore()

        # 7. Side pillars
        painter.save()
        painter.setOpacity(ornament_alpha_mult)
        self._draw_side_pillars(painter, width, height)
        painter.restore()

        # 8. Corner arch brackets
        painter.save()
        painter.setOpacity(ornament_alpha_mult)
        self._draw_corner_arches(painter, width, height)
        painter.restore()

        # 9. Tracery bands — two at different heights for layered depth
        painter.save()
        painter.setOpacity(ornament_alpha_mult)
        self._draw_tracery_band(painter, width, height * 0.56)
        painter.restore()

        # 9b. Second fainter tracery band lower down
        painter.save()
        painter.setOpacity(ornament_alpha_mult * 0.5)
        self._draw_tracery_band(painter, width, height * 0.78)
        painter.restore()

        painter.setClipping(False)

        # 10. Border
        painter.setBrush(Qt.BrushStyle.NoBrush)
        if focused:
            painter.setPen(QPen(QColor(198, 183, 190, 90), 1.2))
        else:
            painter.setPen(QPen(QColor(86, 90, 117, 60), 0.8))
        painter.drawRoundedRect(rect, radius, radius)

    def paint_waveform_panel(self, painter, rect, w, h, cy):
        """Command, specific. Paints waveform panel with gothic arch frame.

        Dark recessed panel with a pointed arch border motif at the top.

        Args:
            painter: QPainter
            rect (QRectF): Panel rectangle
            w (int): Panel width
            h (int): Panel height
            cy (float): Center Y for the waveform line
        """
        # Dark recessed background
        panel_grad = QLinearGradient(0, 0, 0, h)
        panel_grad.setColorAt(0, QColor(12, 12, 22))
        panel_grad.setColorAt(0.3, QColor(16, 16, 28))
        panel_grad.setColorAt(0.7, QColor(14, 14, 25))
        panel_grad.setColorAt(1, QColor(10, 10, 18))
        painter.setBrush(QBrush(panel_grad))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawRoundedRect(rect, 5, 5)

        # Inset shadows
        for grad, adj in [
            (QLinearGradient(0, 0, 0, 12), rect.adjusted(1, 1, -1, -h + 13)),
            (QLinearGradient(0, 0, 8, 0), rect.adjusted(1, 1, -w + 9, -1)),
            (QLinearGradient(w, 0, w - 8, 0), rect.adjusted(w - 9, 1, -1, -1)),
        ]:
            grad.setColorAt(0, QColor(5, 5, 12, 150))
            grad.setColorAt(1, QColor(5, 5, 12, 0))
            painter.setBrush(QBrush(grad))
            painter.setPen(Qt.PenStyle.NoPen)
            painter.drawRoundedRect(adj, 4, 4)

        # Border — mauve
        painter.setBrush(Qt.BrushStyle.NoBrush)
        painter.setPen(QPen(QColor(86, 90, 117, 160), 1.2))
        painter.drawRoundedRect(rect, 5, 5)

        # Small pointed arch motif centered at top of panel
        arch_pen = QPen(QColor(198, 183, 190, 50), 1.0)
        arch_pen.setCapStyle(Qt.PenCapStyle.RoundCap)
        arch_w = min(w * 0.25, 60)
        self._draw_pointed_arch(
            painter, w / 2.0, rect.y() + 4, arch_w, 14, arch_pen
        )

        # Center line — faint mauve
        painter.setPen(QPen(QColor(198, 183, 190, 35), 1))
        painter.drawLine(0, int(cy), w, int(cy))
