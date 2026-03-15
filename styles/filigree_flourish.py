"""Filigree style - Hollow Knight-inspired calligraphic flourishes with spiral terminations."""

import math
import numpy as np
from PyQt6.QtCore import Qt, QRectF, QPointF
from PyQt6.QtGui import (
    QColor, QLinearGradient, QRadialGradient, QBrush, QImage, QPixmap,
    QPainterPath, QPen
)

from .base import BaseStyle, get_cached_texture


# Hollow Knight void palette — NO GOLD
VOID_BLACK = "rgb(15, 15, 27)"
VOID_DEEP = "rgb(20, 20, 35)"
SLATE_DARK = "rgb(55, 58, 75)"
SLATE_MID = "rgb(86, 90, 117)"
MAUVE = "rgb(198, 183, 190)"
OFF_WHITE = "rgb(250, 251, 246)"
DEEP_PURPLE = "rgb(45, 0, 78)"

# Derived colors
MAUVE_DIM = "rgb(140, 130, 140)"
MAUVE_FAINT = "rgb(110, 105, 115)"
VOID_PANEL = "rgb(25, 25, 42)"
BORDER_VOID = "rgb(35, 35, 55)"
BORDER_SLATE = "rgb(65, 68, 88)"


class FiligreeFlourishStyle(BaseStyle):
    name = "filigree_flourish"
    font = "Palatino"

    _texture_cache = None

    # Mauve accent on void
    accent = QColor(198, 183, 190)
    accent_css = "rgb(198,183,190)"
    text_primary = OFF_WHITE
    text_secondary = MAUVE
    text_muted = MAUVE_DIM
    text_error = "rgb(220, 100, 100)"
    text_link = MAUVE
    border_color = BORDER_SLATE
    border_dark = BORDER_VOID
    icon_color_dark = '#373a4b'
    icon_color_light = '#fafbf6'
    icon_color_muted = '#8b8590'

    # Input fields
    input_bg = '#14141f'
    input_text = '#fafbf6'

    # Slider
    slider_groove = "rgba(20,20,35,0.85)"
    slider_handle = "rgb(198,183,190)"
    slider_fill = "rgb(140,130,140)"

    # Rotary knob - pewter/silver
    knob_style = "vintage"
    knob_body_dark = "#373a4b"
    knob_body_light = "#8b8590"
    knob_notch_style = "needle"
    knob_tickmarks = True
    knob_glow = False
    knob_track_color = "#c6b7be"
    knob_label_color = "#fafbf6"

    # Waveform - mauve on void
    waveform_color = QColor(198, 183, 190)
    waveform_glow = True
    waveform_center_line = QColor(198, 183, 190, 40)
    waveform_panel = "dark"

    # Timer - mauve LCD
    timer_use_lcd = True
    timer_color = QColor(198, 183, 190)

    # Transcription
    transcription_text = OFF_WHITE
    transcription_text_dimmed = MAUVE_DIM
    transcription_panel_bg = "rgba(15, 15, 27, 128)"
    transcription_panel_border = "rgba(35, 35, 55, 160)"
    transcription_row_hover = "rgba(198, 183, 190, 0.08)"
    transcription_row_btn_bg = "rgba(198, 183, 190, 0.10)"
    transcription_row_btn_hover = "rgba(198, 183, 190, 0.18)"
    transcription_row_btn_pressed = "rgba(198, 183, 190, 0.35)"

    # Chime editor
    chime_grid_bg = QColor(18, 18, 30)
    chime_grid_line = QColor(40, 40, 58)
    chime_cell_inactive = QColor(30, 30, 48)
    chime_cell_active = QColor(198, 183, 190)
    chime_cell_highlight = QColor(198, 183, 190, 70)
    chime_piano_white = QColor(240, 238, 232)
    chime_piano_black = QColor(22, 22, 36)
    chime_piano_label_white = QColor(55, 58, 75)
    chime_piano_label_black = QColor(198, 183, 190)

    def button_css(self):
        return (
            # Normal
            "QPushButton { color: " + MAUVE_DIM + "; "
            "background: qlineargradient(x1:0, y1:0, x2:0, y2:1, "
            "stop:0 " + SLATE_DARK + ", stop:0.08 " + VOID_DEEP + ", "
            "stop:0.92 " + VOID_BLACK + ", stop:1 rgb(10,10,20)); "
            "border: 1px solid " + BORDER_SLATE + "; border-top-color: " + SLATE_MID + "; "
            "border-radius: 5px; padding: 3px 8px; font-size: 11px; "
            "font-family: " + self.font + "; text-align: left; }"
            # Hover
            "QPushButton:hover { color: " + OFF_WHITE + "; "
            "background: qlineargradient(x1:0, y1:0, x2:0, y2:1, "
            "stop:0 " + SLATE_MID + ", stop:0.08 " + SLATE_DARK + ", "
            "stop:0.92 " + VOID_DEEP + ", stop:1 " + VOID_BLACK + "); "
            "border: 1px solid " + MAUVE_DIM + "; border-top-color: " + MAUVE + "; }"
            # Pressed
            "QPushButton:pressed { color: " + MAUVE + "; "
            "background: qlineargradient(x1:0, y1:0, x2:0, y2:1, "
            "stop:0 " + VOID_BLACK + ", stop:0.08 " + VOID_DEEP + ", "
            "stop:0.92 " + SLATE_DARK + ", stop:1 " + VOID_DEEP + "); "
            "border: 1px solid " + BORDER_VOID + "; }"
            # Disabled
            "QPushButton:disabled { color: rgb(60,60,75); "
            "background: " + VOID_BLACK + "; border: 1px solid " + BORDER_VOID + "; }"
            # Checked
            "QPushButton:checked { color: " + OFF_WHITE + "; "
            "background: qlineargradient(x1:0, y1:0, x2:0, y2:1, "
            "stop:0 " + MAUVE_DIM + ", stop:0.08 rgb(110,105,115), "
            "stop:0.92 " + SLATE_DARK + ", stop:1 " + VOID_DEEP + "); "
            "border: 1px solid " + MAUVE_DIM + "; }"
            "QPushButton:checked:hover { "
            "background: qlineargradient(x1:0, y1:0, x2:0, y2:1, "
            "stop:0 " + MAUVE + ", stop:0.08 " + MAUVE_DIM + ", "
            "stop:0.92 " + SLATE_DARK + ", stop:1 " + VOID_DEEP + "); }"
        )

    def menu_css(self):
        return (
            "QMenu { background: " + VOID_BLACK + "; color: " + OFF_WHITE + "; "
            "border: 2px solid " + BORDER_SLATE + "; border-radius: 4px; padding: 4px; "
            "font-family: " + self.font + "; font-size: 11px; }"
            "QMenu::item { padding: 4px 16px; border-radius: 2px; }"
            "QMenu::item:selected { color: " + OFF_WHITE + "; "
            "background: qlineargradient(x1:0, y1:0, x2:0, y2:1, "
            "stop:0 " + SLATE_MID + ", stop:0.5 " + SLATE_DARK + ", stop:1 " + VOID_DEEP + "); }"
            "QMenu::separator { height: 2px; background: " + BORDER_SLATE + "; margin: 4px 8px; }"
        )

    def _scrollbar_vertical_css(self):
        return (
            "QScrollBar:vertical { width: 14px; background: " + VOID_BLACK + "; "
            "border: 1px solid " + BORDER_VOID + "; border-radius: 5px; margin: 0px; }"
            "QScrollBar::handle:vertical { "
            "background: qlineargradient(x1:0, y1:0, x2:1, y2:0, "
            "stop:0.0 " + SLATE_DARK + ", stop:0.5 " + SLATE_MID + ", stop:1.0 " + SLATE_DARK + "); "
            "border: 1px solid " + BORDER_SLATE + "; border-radius: 4px; min-height: 40px; margin: 2px; }"
            "QScrollBar::handle:vertical:hover { "
            "background: qlineargradient(x1:0, y1:0, x2:1, y2:0, "
            "stop:0.0 " + SLATE_MID + ", stop:0.5 " + MAUVE_DIM + ", stop:1.0 " + SLATE_MID + "); "
            "border: 1px solid " + MAUVE_DIM + "; }"
            "QScrollBar::handle:vertical:pressed { "
            "background: qlineargradient(x1:0, y1:0, x2:1, y2:0, "
            "stop:0.0 " + VOID_DEEP + ", stop:0.5 " + SLATE_DARK + ", stop:1.0 " + VOID_DEEP + "); "
            "border: 1px solid " + BORDER_VOID + "; }"
            "QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical { "
            "height: 0; width: 0; background: none; border: none; }"
            "QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical { background: transparent; }"
        )

    def panel_bg_css(self):
        return (
            "background: qlineargradient(x1:0, y1:0, x2:0, y2:1, "
            "stop:0 rgba(55,58,75,128), stop:0.02 rgba(20,20,35,128), "
            "stop:0.98 rgba(15,15,27,128), stop:1 rgba(10,10,20,128)); "
            "border: 1px solid " + BORDER_SLATE + "; border-radius: 4px;"
        )

    def panel_bg_flat_css(self):
        return (
            "background: rgba(15, 15, 27, 128); border: 1px solid " + BORDER_VOID + "; border-radius: 4px;"
        )

    def get_background_pixmap(self, height=512):
        """Generate void texture with subtle noise grain.

        Command, specific. Returns cached QPixmap of tileable dark texture.
        """
        if FiligreeFlourishStyle._texture_cache is not None:
            return FiligreeFlourishStyle._texture_cache

        width = 256
        FiligreeFlourishStyle._texture_cache = get_cached_texture(
            "filigree", width, height, lambda: self._generate_texture(width, height)
        )
        return FiligreeFlourishStyle._texture_cache

    def _generate_texture(self, width, height):
        """Generate dark void texture with faint purple-tinged noise.

        Command, specific. Returns QPixmap.
        """
        from scipy.ndimage import gaussian_filter

        np.random.seed(2017)  # Hollow Knight release year

        img = np.zeros((height, width, 4), dtype=np.uint8)

        # Very dark void base with slight purple tint
        base_r, base_g, base_b = 17, 17, 30

        # Fine noise grain
        noise = np.random.random((height, width)).astype(np.float32)
        noise = gaussian_filter(noise, sigma=1.5, mode='wrap')
        noise = (noise - noise.min()) / (noise.max() - noise.min() + 1e-6)

        variation = 0.85 + noise * 0.3

        img[:, :, 0] = np.clip(base_r * variation, 10, 28).astype(np.uint8)
        img[:, :, 1] = np.clip(base_g * variation, 10, 28).astype(np.uint8)
        img[:, :, 2] = np.clip(base_b * variation, 20, 42).astype(np.uint8)
        img[:, :, 3] = 255

        for c in range(3):
            img[:, :, c] = gaussian_filter(img[:, :, c].astype(float), sigma=1.0, mode='wrap').astype(np.uint8)

        qimg = QImage(img.data, width, height, width * 4, QImage.Format.Format_RGBA8888).copy()
        return QPixmap.fromImage(qimg)

    # ── Calligraphic drawing primitives ──────────────────────────────

    def _draw_spiral(self, painter, cx, cy, start_radius, turns=1.5, direction=1, start_angle=0.0, pen=None):
        """Draw a tight inward spiral using connected quadratic beziers.

        Command, specific. Renders a fiddlehead-fern spiral termination.

        Args:
            painter: QPainter to draw on
            cx (float): Center x of spiral
            cy (float): Center y of spiral
            start_radius (float): Outer radius where spiral begins
            turns (float): Number of spiral revolutions
            direction (int): 1 or -1 for CW/CCW
            start_angle (float): Starting angle in radians
            pen (QPen): Pen to use; if None, uses painter's current pen
        """
        if pen is not None:
            painter.setPen(pen)
        painter.setBrush(Qt.BrushStyle.NoBrush)

        path = QPainterPath()
        angle = start_angle
        r = start_radius
        x = cx + r * math.cos(angle)
        y = cy + r * math.sin(angle) * direction
        path.moveTo(QPointF(x, y))

        SEGMENTS_PER_TURN = 8
        SHRINK_FACTOR = 0.80
        steps = int(turns * SEGMENTS_PER_TURN)
        for _ in range(steps):
            angle += math.pi / (SEGMENTS_PER_TURN / 2)
            r *= SHRINK_FACTOR
            ex = cx + r * math.cos(angle)
            ey = cy + r * math.sin(angle) * direction
            # Control point offset for smooth curvature
            cr = r * 1.15
            ca = angle - math.pi / SEGMENTS_PER_TURN
            ctrl_x = cx + cr * math.cos(ca)
            ctrl_y = cy + cr * math.sin(ca) * direction
            path.quadTo(QPointF(ctrl_x, ctrl_y), QPointF(ex, ey))

        painter.drawPath(path)

    def _draw_tapered_curve(self, painter, points, base_width, tip_width, color):
        """Draw a curve with thick-to-thin tapering by rendering parallel strokes.

        Command, specific. Approximates calligraphic width variation by drawing
        the curve in segments with decreasing pen width.

        Args:
            painter: QPainter to draw on
            points (list[QPointF]): Sequence of points along the curve
            base_width (float): Pen width at the start (thick end)
            tip_width (float): Pen width at the end (thin end)
            color (QColor): Stroke color
        """
        if len(points) < 2:
            return
        n = len(points) - 1
        for i in range(n):
            t = i / max(n, 1)
            w = base_width + (tip_width - base_width) * t
            pen = QPen(color, w)
            pen.setCapStyle(Qt.PenCapStyle.RoundCap)
            painter.setPen(pen)
            painter.setBrush(Qt.BrushStyle.NoBrush)
            path = QPainterPath()
            path.moveTo(points[i])
            path.lineTo(points[i + 1])
            painter.drawPath(path)

    def _sample_cubic(self, p0, p1, p2, p3, num_samples=20):
        """Sample points along a cubic bezier curve.

        Pure function, general.

        Args:
            p0 (QPointF): Start point
            p1 (QPointF): Control point 1
            p2 (QPointF): Control point 2
            p3 (QPointF): End point
            num_samples (int): Number of sample points

        Returns:
            list[QPointF]: Sampled points along the curve

        Examples:
            >>> # Straight line from (0,0) to (10,0)
            >>> pts = FiligreeStyle._sample_cubic(None, QPointF(0,0), QPointF(3,0), QPointF(7,0), QPointF(10,0), 3)
            >>> len(pts)
            3
        """
        points = []
        for i in range(num_samples):
            t = i / max(num_samples - 1, 1)
            u = 1 - t
            x = u**3 * p0.x() + 3 * u**2 * t * p1.x() + 3 * u * t**2 * p2.x() + t**3 * p3.x()
            y = u**3 * p0.y() + 3 * u**2 * t * p1.y() + 3 * u * t**2 * p2.y() + t**3 * p3.y()
            points.append(QPointF(x, y))
        return points

    def _draw_tapered_cubic(self, painter, p0, p1, p2, p3, base_width, tip_width, color):
        """Draw a tapered cubic bezier — thick at start, thin at end.

        Command, specific. The core calligraphic stroke primitive.

        Args:
            painter: QPainter to draw on
            p0 (QPointF): Start
            p1 (QPointF): Control 1
            p2 (QPointF): Control 2
            p3 (QPointF): End
            base_width (float): Width at p0
            tip_width (float): Width at p3
            color (QColor): Stroke color
        """
        NUM_SAMPLES = 24
        points = self._sample_cubic(p0, p1, p2, p3, NUM_SAMPLES)
        self._draw_tapered_curve(painter, points, base_width, tip_width, color)

    def _draw_gable_motif(self, painter, cx, cy, scale, color, mirror=False):
        """Draw a single gable motif — an upward-curving line terminating in spirals.

        Command, specific. The primary ornamental building block from French Gothic
        architecture as seen in Hollow Knight. A line curves upward from center and
        terminates in tight inward spirals at both ends.

        Args:
            painter: QPainter to draw on
            cx (float): Horizontal center of the motif
            cy (float): Vertical base of the motif
            scale (float): Size multiplier (1.0 = ~80px wide)
            color (QColor): Mauve-family color to use
            mirror (bool): If True, flip vertically (curves downward)
        """
        s = scale
        flip = -1 if mirror else 1

        # Left arm: curves up-left and terminates in a spiral
        self._draw_tapered_cubic(
            painter,
            QPointF(cx, cy),
            QPointF(cx - 15 * s, cy - 28 * s * flip),
            QPointF(cx - 32 * s, cy - 40 * s * flip),
            QPointF(cx - 45 * s, cy - 30 * s * flip),
            3.0 * s, 0.7 * s, color
        )
        self._draw_spiral(
            painter, cx - 45 * s, cy - 30 * s * flip,
            start_radius=7 * s, turns=1.5, direction=flip,
            start_angle=math.pi * 0.8,
            pen=QPen(color, 0.9 * s, cap=Qt.PenCapStyle.RoundCap)
        )

        # Right arm: mirror of left
        self._draw_tapered_cubic(
            painter,
            QPointF(cx, cy),
            QPointF(cx + 15 * s, cy - 28 * s * flip),
            QPointF(cx + 32 * s, cy - 40 * s * flip),
            QPointF(cx + 45 * s, cy - 30 * s * flip),
            3.0 * s, 0.7 * s, color
        )
        self._draw_spiral(
            painter, cx + 45 * s, cy - 30 * s * flip,
            start_radius=7 * s, turns=1.5, direction=-flip,
            start_angle=math.pi * 0.2,
            pen=QPen(color, 0.9 * s, cap=Qt.PenCapStyle.RoundCap)
        )

    def _draw_flourish_line(self, painter, x1, y1, x2, y2, color, width=1.5):
        """Draw a straight decorative line with spiral terminations at both ends.

        Command, specific.

        Args:
            painter: QPainter to draw on
            x1, y1: Start point
            x2, y2: End point
            color (QColor): Stroke color
            width (float): Line width
        """
        pen = QPen(color, width)
        pen.setCapStyle(Qt.PenCapStyle.RoundCap)
        painter.setPen(pen)
        painter.setBrush(Qt.BrushStyle.NoBrush)
        painter.drawLine(QPointF(x1, y1), QPointF(x2, y2))

        # Spiral at each end
        spiral_r = width * 3
        spiral_pen = QPen(color, max(0.5, width * 0.5))
        spiral_pen.setCapStyle(Qt.PenCapStyle.RoundCap)

        angle = math.atan2(y2 - y1, x2 - x1)
        self._draw_spiral(painter, x1, y1, spiral_r, turns=1.0, direction=1,
                          start_angle=angle + math.pi, pen=spiral_pen)
        self._draw_spiral(painter, x2, y2, spiral_r, turns=1.0, direction=-1,
                          start_angle=angle, pen=spiral_pen)

    def _draw_top_flourish(self, painter, width, height, alpha):
        """Draw an elaborate horizontal flourish along the top edge.

        Command, specific. Features a central gable motif flanked by sweeping
        curves with spiral terminations, inspired by Hollow Knight title framing.
        Three nested scales of ornament for visual richness.

        Args:
            painter: QPainter to draw on
            width (int): Window width
            height (int): Window height
            alpha (int): Base opacity (0-255)
        """
        cx = width / 2
        color = QColor(198, 183, 190, alpha)
        color_mid = QColor(198, 183, 190, int(alpha * 0.7))
        color_dim = QColor(198, 183, 190, alpha // 2)
        color_faint = QColor(198, 183, 190, alpha // 3)
        TOP_Y = 18

        # ── Layer 0: Thin horizontal spine across the top ──
        line_extent = width * 0.46
        painter.setPen(QPen(color_faint, 0.8, cap=Qt.PenCapStyle.RoundCap))
        painter.setBrush(Qt.BrushStyle.NoBrush)
        painter.drawLine(QPointF(cx - line_extent, TOP_Y + 15), QPointF(cx + line_extent, TOP_Y + 15))

        # ── Layer 1: Central gable — LARGE and prominent ──
        self._draw_gable_motif(painter, cx, TOP_Y + 38, scale=1.5, color=color)

        # A second smaller gable nested inside the first for depth
        self._draw_gable_motif(painter, cx, TOP_Y + 30, scale=0.8, color=color_mid)

        # Tiny innermost gable for triple-nested effect
        self._draw_gable_motif(painter, cx, TOP_Y + 25, scale=0.4, color=color_dim)

        # ── Layer 2: Flanking gables ──
        gable_offset = width * 0.25
        self._draw_gable_motif(painter, cx - gable_offset, TOP_Y + 26, scale=0.65, color=color_dim)
        self._draw_gable_motif(painter, cx + gable_offset, TOP_Y + 26, scale=0.65, color=color_dim)

        # ── Layer 3: Long sweeping S-curves from center outward ──
        for sign in [-1, 1]:
            # Primary sweep — bold
            self._draw_tapered_cubic(
                painter,
                QPointF(cx + sign * 55, TOP_Y + 15),
                QPointF(cx + sign * 110, TOP_Y + 4),
                QPointF(cx + sign * (width * 0.33), TOP_Y + 24),
                QPointF(cx + sign * (width * 0.45), TOP_Y + 12),
                2.8, 0.5, color_mid
            )
            # Spiral termination at outer end
            self._draw_spiral(
                painter,
                cx + sign * (width * 0.45), TOP_Y + 12,
                start_radius=8, turns=1.5, direction=sign,
                start_angle=0,
                pen=QPen(color_mid, 0.8, cap=Qt.PenCapStyle.RoundCap)
            )

            # Secondary thinner sweep, slightly below
            self._draw_tapered_cubic(
                painter,
                QPointF(cx + sign * 60, TOP_Y + 22),
                QPointF(cx + sign * 120, TOP_Y + 14),
                QPointF(cx + sign * (width * 0.32), TOP_Y + 28),
                QPointF(cx + sign * (width * 0.42), TOP_Y + 20),
                1.4, 0.3, color_dim
            )

        # ── Layer 4: Tiny spiral clusters at the spine endpoints ──
        for sign in [-1, 1]:
            self._draw_spiral(
                painter, cx + sign * line_extent, TOP_Y + 15,
                start_radius=4, turns=1.2, direction=sign,
                start_angle=math.pi if sign == -1 else 0,
                pen=QPen(color_dim, 0.6, cap=Qt.PenCapStyle.RoundCap)
            )
            # A second spiral curling the other way for a double-curl motif
            self._draw_spiral(
                painter, cx + sign * line_extent, TOP_Y + 15,
                start_radius=3, turns=0.8, direction=-sign,
                start_angle=(math.pi if sign == -1 else 0) + math.pi * 0.3,
                pen=QPen(color_faint, 0.4, cap=Qt.PenCapStyle.RoundCap)
            )

    def _draw_bottom_flourish(self, painter, width, height, alpha):
        """Draw a matching flourish along the bottom edge — slightly different from top.

        Command, specific. Features inverted gable motifs and upward-curling spirals.
        Simpler than the top (visual hierarchy: top is primary, bottom is secondary).

        Args:
            painter: QPainter to draw on
            width (int): Window width
            height (int): Window height
            alpha (int): Base opacity (0-255)
        """
        cx = width / 2
        color = QColor(198, 183, 190, alpha)
        color_mid = QColor(198, 183, 190, int(alpha * 0.7))
        color_dim = QColor(198, 183, 190, alpha // 2)
        color_faint = QColor(198, 183, 190, alpha // 3)
        BOT_Y = height - 18

        # Thin horizontal spine
        line_extent = width * 0.40
        painter.setPen(QPen(color_faint, 0.7, cap=Qt.PenCapStyle.RoundCap))
        painter.setBrush(Qt.BrushStyle.NoBrush)
        painter.drawLine(QPointF(cx - line_extent, BOT_Y - 12), QPointF(cx + line_extent, BOT_Y - 12))

        # Central inverted gable
        self._draw_gable_motif(painter, cx, BOT_Y - 28, scale=1.0, color=color, mirror=True)

        # Nested smaller gable
        self._draw_gable_motif(painter, cx, BOT_Y - 22, scale=0.55, color=color_mid, mirror=True)

        # Sweeping curves outward
        for sign in [-1, 1]:
            self._draw_tapered_cubic(
                painter,
                QPointF(cx + sign * 40, BOT_Y - 10),
                QPointF(cx + sign * 80, BOT_Y - 4),
                QPointF(cx + sign * (width * 0.30), BOT_Y - 16),
                QPointF(cx + sign * (width * 0.42), BOT_Y - 8),
                1.8, 0.4, color_mid
            )
            self._draw_spiral(
                painter,
                cx + sign * (width * 0.42), BOT_Y - 8,
                start_radius=5, turns=1.3, direction=-sign,
                start_angle=math.pi,
                pen=QPen(color_mid, 0.6, cap=Qt.PenCapStyle.RoundCap)
            )

        # Double-curl at spine endpoints
        for sign in [-1, 1]:
            self._draw_spiral(
                painter, cx + sign * line_extent, BOT_Y - 12,
                start_radius=3.5, turns=1.0, direction=-sign,
                start_angle=math.pi if sign == -1 else 0,
                pen=QPen(color_dim, 0.5, cap=Qt.PenCapStyle.RoundCap)
            )

    def _draw_corner_spirals(self, painter, width, height, alpha):
        """Draw tight spiraling curves at all 4 corners curling inward.

        Command, specific. Each corner gets a primary curve sweeping along
        the edge and terminating in a tight spiral, plus a fainter echo curve.

        Args:
            painter: QPainter to draw on
            width (int): Window width
            height (int): Window height
            alpha (int): Base opacity (0-255)
        """
        color = QColor(198, 183, 190, alpha)
        color_dim = QColor(198, 183, 190, int(alpha * 0.7))
        color_echo = QColor(198, 183, 190, alpha // 3)
        reach = min(width, height) * 0.32

        corners = [
            # (start_x, start_y, curve_dir_x, curve_dir_y, spiral_dir, spiral_start_angle)
            (0, 0, 1, 1, 1, math.pi * 1.5),      # top-left
            (width, 0, -1, 1, -1, math.pi * 1.5), # top-right
            (0, height, 1, -1, -1, math.pi * 0.5), # bottom-left
            (width, height, -1, -1, 1, math.pi * 0.5), # bottom-right
        ]

        for sx, sy, dx, dy, sdir, sa in corners:
            # Primary sweeping curve along the edge — thick and tapered
            self._draw_tapered_cubic(
                painter,
                QPointF(sx + dx * 8, sy + dy * reach * 0.7),
                QPointF(sx + dx * 14, sy + dy * reach * 0.35),
                QPointF(sx + dx * reach * 0.35, sy + dy * 14),
                QPointF(sx + dx * reach * 0.7, sy + dy * 8),
                2.8, 0.6, color
            )
            # Spiral termination at the curve end
            self._draw_spiral(
                painter,
                sx + dx * reach * 0.7, sy + dy * 8,
                start_radius=8, turns=1.6, direction=sdir,
                start_angle=sa,
                pen=QPen(color_dim, 0.8, cap=Qt.PenCapStyle.RoundCap)
            )
            # Echo curve — wider arc, fainter
            self._draw_tapered_cubic(
                painter,
                QPointF(sx + dx * 5, sy + dy * reach * 0.9),
                QPointF(sx + dx * 18, sy + dy * reach * 0.5),
                QPointF(sx + dx * reach * 0.5, sy + dy * 18),
                QPointF(sx + dx * reach * 0.9, sy + dy * 5),
                1.5, 0.3, color_echo
            )
            # Double spiral at echo start — curling inward from the edge
            self._draw_spiral(
                painter,
                sx + dx * 5, sy + dy * reach * 0.9,
                start_radius=5, turns=1.2, direction=-sdir,
                start_angle=sa + math.pi,
                pen=QPen(color_echo, 0.5, cap=Qt.PenCapStyle.RoundCap)
            )
            # Innermost fine filigree curl
            self._draw_spiral(
                painter,
                sx + dx * reach * 0.45, sy + dy * reach * 0.45,
                start_radius=4, turns=1.0, direction=sdir,
                start_angle=sa + math.pi * 0.5,
                pen=QPen(color_echo, 0.4, cap=Qt.PenCapStyle.RoundCap)
            )

    def _draw_side_filigree(self, painter, width, height, alpha):
        """Draw decorative spiral pairs along the left and right edges.

        Command, specific. Provides the 'nested repetition at small scale' element.
        Each side gets paired curling spirals that face inward, connected by a
        thin vertical line segment.

        Args:
            painter: QPainter to draw on
            width (int): Window width
            height (int): Window height
            alpha (int): Base opacity (0-255)
        """
        color = QColor(198, 183, 190, int(alpha * 0.45))
        color_faint = QColor(198, 183, 190, alpha // 4)
        MOTIF_SPACING = 50
        MARGIN = 12

        y_start = height * 0.28
        y_end = height * 0.72
        n_motifs = max(1, int((y_end - y_start) / MOTIF_SPACING))

        # Thin vertical lines along edges
        painter.setPen(QPen(color_faint, 0.5, cap=Qt.PenCapStyle.RoundCap))
        painter.setBrush(Qt.BrushStyle.NoBrush)
        painter.drawLine(QPointF(MARGIN + 4, y_start), QPointF(MARGIN + 4, y_end))
        painter.drawLine(QPointF(width - MARGIN - 4, y_start), QPointF(width - MARGIN - 4, y_end))

        for i in range(n_motifs):
            y = y_start + i * MOTIF_SPACING + MOTIF_SPACING / 2

            # Left side — paired spirals curling inward (toward center)
            self._draw_spiral(
                painter, MARGIN + 6, y - 5,
                start_radius=5, turns=1.1, direction=1,
                start_angle=0,
                pen=QPen(color, 0.6, cap=Qt.PenCapStyle.RoundCap)
            )
            self._draw_spiral(
                painter, MARGIN + 6, y + 5,
                start_radius=5, turns=1.1, direction=-1,
                start_angle=0,
                pen=QPen(color, 0.6, cap=Qt.PenCapStyle.RoundCap)
            )

            # Right side — mirror
            self._draw_spiral(
                painter, width - MARGIN - 6, y - 5,
                start_radius=5, turns=1.1, direction=1,
                start_angle=math.pi,
                pen=QPen(color, 0.6, cap=Qt.PenCapStyle.RoundCap)
            )
            self._draw_spiral(
                painter, width - MARGIN - 6, y + 5,
                start_radius=5, turns=1.1, direction=-1,
                start_angle=math.pi,
                pen=QPen(color, 0.6, cap=Qt.PenCapStyle.RoundCap)
            )

    def _draw_vignette(self, painter, rect, width, height, radius=12):
        """Dark void vignette — deeper at edges for enclosure.

        Command, specific.
        """
        for horizontal, alpha_mult in [(True, 0.6), (False, 0.8)]:
            grad = QLinearGradient(0, 0, width if horizontal else 0, 0 if horizontal else height)
            for pos, a in [(0, 180), (0.08, 100), (0.2, 40), (0.8, 40), (0.92, 100), (1, 180)]:
                grad.setColorAt(pos, QColor(10, 10, 20, int(a * alpha_mult)))
            painter.setBrush(QBrush(grad))
            painter.setPen(Qt.PenStyle.NoPen)
            painter.drawRoundedRect(rect, radius, radius)

    def _draw_mauve_glow(self, painter, rect, width, height, radius=12):
        """Faint mauve glow from top and bottom edges.

        Command, specific.
        """
        # Top glow
        top_glow = QLinearGradient(0, 0, 0, 45)
        top_glow.setColorAt(0, QColor(198, 183, 190, 18))
        top_glow.setColorAt(1, QColor(198, 183, 190, 0))
        painter.setBrush(QBrush(top_glow))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawRoundedRect(QRectF(rect.x(), rect.y(), width, 45), radius, radius)

        # Bottom glow
        bottom_glow = QLinearGradient(0, height - 25, 0, height)
        bottom_glow.setColorAt(0, QColor(198, 183, 190, 0))
        bottom_glow.setColorAt(1, QColor(198, 183, 190, 12))
        painter.setBrush(QBrush(bottom_glow))
        painter.drawRoundedRect(QRectF(rect.x(), rect.y() + height - 25, width, 25), radius, radius)

    def paint_window(self, painter, rect, width, height, focused=True):
        """Paint void background with calligraphic flourishes and spiral terminations.

        Command, specific. Main window rendering method.
        """
        radius = self.corner_radius

        # Clip to rounded rect
        clip = QPainterPath()
        clip.addRoundedRect(QRectF(rect), radius, radius)
        painter.setClipPath(clip)

        # Void texture background
        texture = self.get_background_pixmap(max(512, height))
        painter.drawTiledPixmap(rect, texture)
        painter.setClipping(False)

        # Subtle deep purple radial glow in center — adds depth
        center_glow = QRadialGradient(QPointF(width / 2, height / 2), max(width, height) * 0.5)
        center_glow.setColorAt(0, QColor(45, 0, 78, 25))
        center_glow.setColorAt(0.5, QColor(30, 0, 50, 12))
        center_glow.setColorAt(1, QColor(0, 0, 0, 0))
        painter.setBrush(QBrush(center_glow))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawRoundedRect(rect, radius, radius)

        # Vignette
        self._draw_vignette(painter, rect, width, height, radius)

        # Mauve glow when focused
        if focused:
            self._draw_mauve_glow(painter, rect, width, height, radius)

        # Unclip to allow ornaments to extend beyond window edges
        painter.setClipping(False)

        ornament_alpha = 110 if focused else 50

        # Layer 1: Side filigree (smallest scale — background)
        self._draw_side_filigree(painter, width, height, ornament_alpha)

        # Layer 2: Corner spirals (medium scale)
        self._draw_corner_spirals(painter, width, height, ornament_alpha)

        # Layer 3: Top and bottom flourishes (largest scale — foreground)
        self._draw_top_flourish(painter, width, height, ornament_alpha)
        self._draw_bottom_flourish(painter, width, height, ornament_alpha)

        painter.setClipping(False)

        # Border — mauve when focused, dim slate when not
        painter.setBrush(Qt.BrushStyle.NoBrush)
        if focused:
            painter.setPen(QPen(QColor(198, 183, 190, 90), 1.5))
        else:
            painter.setPen(QPen(QColor(86, 90, 117, 70), 1.0))
        painter.drawRoundedRect(rect, radius, radius)

    def paint_waveform_panel(self, painter, rect, w, h, cy):
        """Waveform panel — dark recessed void with mauve border.

        Command, specific.
        """
        # Dark recessed background
        panel_grad = QLinearGradient(0, 0, 0, h)
        panel_grad.setColorAt(0, QColor(12, 12, 22))
        panel_grad.setColorAt(0.3, QColor(18, 18, 32))
        panel_grad.setColorAt(0.7, QColor(16, 16, 28))
        panel_grad.setColorAt(1, QColor(10, 10, 18))
        painter.setBrush(QBrush(panel_grad))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawRoundedRect(rect, 6, 6)

        # Subtle mauve glow from top
        top_glow = QLinearGradient(0, 0, 0, h * 0.2)
        top_glow.setColorAt(0, QColor(198, 183, 190, 15))
        top_glow.setColorAt(1, QColor(198, 183, 190, 0))
        painter.setBrush(QBrush(top_glow))
        painter.drawRoundedRect(rect.adjusted(2, 2, -2, -int(h * 0.8)), 4, 4)

        # Inset shadows
        for grad, adj in [
            (QLinearGradient(0, 0, 0, 14), rect.adjusted(1, 1, -1, -h + 15)),
            (QLinearGradient(0, 0, 10, 0), rect.adjusted(1, 1, -w + 11, -1)),
            (QLinearGradient(w, 0, w - 10, 0), rect.adjusted(w - 11, 1, -1, -1)),
        ]:
            grad.setColorAt(0, QColor(5, 5, 12, 160))
            grad.setColorAt(1, QColor(5, 5, 12, 0))
            painter.setBrush(QBrush(grad))
            painter.setPen(Qt.PenStyle.NoPen)
            painter.drawRoundedRect(adj, 5, 5)

        # Border — mauve
        painter.setBrush(Qt.BrushStyle.NoBrush)
        painter.setPen(QPen(QColor(140, 130, 140, 140), 1.5))
        painter.drawRoundedRect(rect, 6, 6)

        # Center line
        painter.setPen(QPen(QColor(198, 183, 190, 40), 1))
        painter.drawLine(0, int(cy), w, int(cy))
