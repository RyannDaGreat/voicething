"""Filigree style - Hollow Knight-inspired composite theme.

Gothic arches, calligraphic flourishes, dreamcatcher webs, and wrought iron
filigree layered into one cohesive dark void aesthetic. Mauve ornaments on
deep purple-black, with bilateral symmetry and spiral terminations throughout.
"""

import math
import numpy as np
from PyQt6.QtCore import Qt, QRectF, QPointF
from PyQt6.QtGui import (
    QColor, QLinearGradient, QRadialGradient, QBrush, QImage, QPixmap,
    QPainterPath, QPen, QPainterPathStroker,
)

from .base import BaseStyle, get_cached_texture

# --- Color palette (NO GOLD) ---
VOID_BLACK = "rgb(15, 15, 27)"
VOID_DEEP = "rgb(20, 20, 35)"
SLATE_DARK = "rgb(55, 58, 75)"
SLATE_MID = "rgb(86, 90, 117)"
MAUVE = "rgb(198, 183, 190)"
OFF_WHITE = "rgb(250, 251, 246)"
DEEP_PURPLE = "rgb(45, 0, 78)"

# QColor versions for painting
_MAUVE = QColor(198, 183, 190)
_VOID = QColor(15, 15, 27)
_VOID_DEEP = QColor(20, 20, 35)
_SLATE_DARK = QColor(55, 58, 75)
_SLATE_MID = QColor(86, 90, 117)
_DEEP_PURPLE = QColor(45, 0, 78)


def _spiral_points(cx, cy, start_radius, end_radius, start_angle, turns, num_points=40):
    """
    Pure function, general. Generate points along an Archimedean spiral.

    Returns a list of (x, y) tuples tracing a spiral from start_radius
    to end_radius, beginning at start_angle and rotating through the
    given number of turns.

    Args:
        cx (float): Center x
        cy (float): Center y
        start_radius (float): Radius at beginning of spiral
        end_radius (float): Radius at end of spiral
        start_angle (float): Starting angle in radians
        turns (float): Number of full rotations
        num_points (int): Number of sample points

    Returns:
        list[tuple[float, float]]: Points along the spiral

    Examples:
        >>> pts = _spiral_points(0, 0, 10, 0, 0, 1.5, num_points=5)
        >>> len(pts)
        5
        >>> abs(pts[0][0] - 10.0) < 0.01  # starts at radius 10 on x-axis
        True
    """
    points = []
    for i in range(num_points):
        t = i / max(1, num_points - 1)
        r = start_radius + (end_radius - start_radius) * t
        angle = start_angle + turns * 2 * math.pi * t
        points.append((cx + r * math.cos(angle), cy + r * math.sin(angle)))
    return points


def _path_from_points(points):
    """
    Pure function, general. Build a smooth QPainterPath through a list of (x, y) points.

    Uses quadratic Bezier segments with midpoint averaging for smoothness.

    Args:
        points (list[tuple[float, float]]): At least 2 points

    Returns:
        QPainterPath

    Examples:
        >>> p = _path_from_points([(0, 0), (10, 5), (20, 0)])
        >>> p.elementCount() > 0
        True
    """
    if len(points) < 2:
        path = QPainterPath()
        if points:
            path.moveTo(QPointF(*points[0]))
        return path
    path = QPainterPath()
    path.moveTo(QPointF(*points[0]))
    for i in range(1, len(points)):
        path.lineTo(QPointF(*points[i]))
    return path


class FiligreeStyle(BaseStyle):
    """Command, specific. Hollow Knight-inspired composite filigree theme."""

    name = "filigree"
    font = "Palatino"

    _texture_cache = None

    # Mauve accent on deep void
    accent = _MAUVE
    accent_css = MAUVE
    text_primary = OFF_WHITE
    text_secondary = MAUVE
    text_muted = SLATE_MID
    text_error = "rgb(200, 85, 95)"
    text_link = MAUVE
    border_color = SLATE_DARK
    border_dark = VOID_DEEP
    icon_color_dark = '#565a75'
    icon_color_light = '#fafbf6'
    icon_color_muted = '#c6b7be'

    # Input fields
    input_bg = '#14141f'
    input_text = '#fafbf6'

    # Slider
    slider_groove = "rgba(15, 15, 27, 0.85)"
    slider_handle = MAUVE
    slider_fill = SLATE_MID

    # Rotary knob - wrought iron feel
    knob_style = "industrial"
    knob_body_dark = "#1a1a2a"
    knob_body_light = "#565a75"
    knob_notch_style = "needle"
    knob_tickmarks = True
    knob_glow = False
    knob_track_color = "#c6b7be"
    knob_label_color = "#fafbf6"

    # Waveform
    waveform_color = _MAUVE
    waveform_glow = True
    waveform_glow_radius = 14
    waveform_glow_alpha = 150
    waveform_center_line = QColor(198, 183, 190, 45)
    waveform_panel = "dark"

    # Timer
    timer_use_lcd = True
    timer_color = _MAUVE

    # Transcription
    transcription_text = OFF_WHITE
    transcription_text_dimmed = SLATE_MID
    transcription_panel_bg = "rgba(15, 15, 27, 128)"  # 50% transparent so filigree shows through
    transcription_panel_border = "rgba(20, 20, 35, 160)"
    transcription_row_hover = "rgba(198, 183, 190, 0.08)"
    transcription_row_btn_bg = "rgba(198, 183, 190, 0.10)"
    transcription_row_btn_hover = "rgba(198, 183, 190, 0.18)"
    transcription_row_btn_pressed = "rgba(198, 183, 190, 0.35)"

    # Chime editor
    chime_grid_bg = QColor(18, 18, 30)
    chime_grid_line = QColor(40, 40, 58)
    chime_cell_inactive = QColor(30, 30, 48)
    chime_cell_active = QColor(198, 183, 190)
    chime_cell_highlight = QColor(198, 183, 190, 80)
    chime_piano_white = QColor(240, 238, 235)
    chime_piano_black = QColor(22, 22, 36)
    chime_piano_label_white = QColor(60, 58, 70)
    chime_piano_label_black = QColor(198, 183, 190)

    # --- CSS ---

    def button_css(self):
        """Command, specific. Returns CSS for filigree-themed buttons."""
        return (
            # Normal
            f"QPushButton {{ color: {MAUVE}; "
            f"background: qlineargradient(x1:0, y1:0, x2:0, y2:1, "
            f"stop:0 rgb(30, 30, 48), stop:0.06 rgb(22, 22, 38), "
            f"stop:0.94 rgb(18, 18, 32), stop:1 rgb(12, 12, 22)); "
            f"border: 1px solid {SLATE_DARK}; "
            f"border-top-color: {SLATE_MID}; "
            f"border-radius: 3px; padding: 3px 8px; font-size: 11px; "
            f"font-family: {self.font}; text-align: left; }}"
            # Hover
            f"QPushButton:hover {{ color: {OFF_WHITE}; "
            f"background: qlineargradient(x1:0, y1:0, x2:0, y2:1, "
            f"stop:0 rgb(40, 38, 58), stop:0.06 rgb(30, 28, 48), "
            f"stop:0.94 rgb(24, 22, 40), stop:1 rgb(16, 14, 28)); "
            f"border: 1px solid {SLATE_MID}; }}"
            # Pressed
            f"QPushButton:pressed {{ color: {OFF_WHITE}; "
            f"background: qlineargradient(x1:0, y1:0, x2:0, y2:1, "
            f"stop:0 rgb(16, 14, 28), stop:0.06 rgb(22, 20, 36), "
            f"stop:0.94 rgb(30, 28, 46), stop:1 rgb(24, 22, 38)); "
            f"border: 1px solid rgb(40, 38, 55); }}"
            # Disabled
            f"QPushButton:disabled {{ color: {SLATE_DARK}; "
            f"background: {VOID_BLACK}; border: 1px solid rgb(30, 30, 42); }}"
            # Checked - deep purple tint
            f"QPushButton:checked {{ color: {OFF_WHITE}; "
            f"background: qlineargradient(x1:0, y1:0, x2:0, y2:1, "
            f"stop:0 rgb(55, 20, 85), stop:0.06 rgb(42, 10, 68), "
            f"stop:0.94 rgb(32, 5, 55), stop:1 rgb(24, 2, 42)); "
            f"border: 1px solid rgb(70, 30, 100); }}"
            f"QPushButton:checked:hover {{ "
            f"background: qlineargradient(x1:0, y1:0, x2:0, y2:1, "
            f"stop:0 rgb(65, 28, 98), stop:0.06 rgb(50, 18, 78), "
            f"stop:0.94 rgb(38, 8, 62), stop:1 rgb(28, 4, 48)); }}"
        )

    def menu_css(self):
        """Command, specific. Returns CSS for context menus."""
        return (
            f"QMenu {{ background: {VOID_BLACK}; color: {OFF_WHITE}; "
            f"border: 2px solid {SLATE_DARK}; border-radius: 3px; padding: 4px; "
            f"font-family: {self.font}; font-size: 11px; }}"
            "QMenu::item { padding: 4px 16px; border-radius: 2px; }"
            f"QMenu::item:selected {{ color: {OFF_WHITE}; "
            f"background: qlineargradient(x1:0, y1:0, x2:0, y2:1, "
            f"stop:0 rgb(55, 20, 85), stop:0.5 rgb(42, 10, 68), stop:1 rgb(32, 5, 55)); }}"
            f"QMenu::separator {{ height: 2px; background: {SLATE_DARK}; margin: 4px 8px; }}"
        )

    def _scrollbar_vertical_css(self):
        """Command, specific. Returns vertical scrollbar CSS."""
        return (
            f"QScrollBar:vertical {{ width: 14px; background: {VOID_BLACK}; "
            f"border: 1px solid rgb(30, 30, 42); border-radius: 5px; margin: 0px; }}"
            "QScrollBar::handle:vertical { "
            "background: qlineargradient(x1:0, y1:0, x2:1, y2:0, "
            f"stop:0.0 rgb(35, 35, 52), stop:0.2 rgb(50, 50, 68), "
            f"stop:0.5 rgb(60, 62, 80), stop:0.8 rgb(50, 50, 68), stop:1.0 rgb(35, 35, 52)); "
            f"border: 1px solid {SLATE_DARK}; border-radius: 4px; min-height: 40px; margin: 2px; }}"
            "QScrollBar::handle:vertical:hover { "
            "background: qlineargradient(x1:0, y1:0, x2:1, y2:0, "
            f"stop:0.0 rgb(50, 50, 68), stop:0.2 rgb(65, 65, 85), "
            f"stop:0.5 rgb(80, 82, 105), stop:0.8 rgb(65, 65, 85), stop:1.0 rgb(50, 50, 68)); "
            f"border: 1px solid {SLATE_MID}; }}"
            "QScrollBar::handle:vertical:pressed { "
            "background: qlineargradient(x1:0, y1:0, x2:1, y2:0, "
            f"stop:0.0 rgb(28, 28, 44), stop:0.2 rgb(40, 40, 58), "
            f"stop:0.5 rgb(50, 50, 68), stop:0.8 rgb(40, 40, 58), stop:1.0 rgb(28, 28, 44)); "
            f"border: 1px solid rgb(40, 40, 55); }}"
            "QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical { "
            "height: 0; width: 0; background: none; border: none; }"
            "QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical { background: transparent; }"
        )

    def panel_bg_css(self):
        """Command, specific. Returns panel background CSS — 50% transparent so filigree shows through."""
        return (
            f"background: qlineargradient(x1:0, y1:0, x2:0, y2:1, "
            f"stop:0 rgba(30, 30, 48, 128), stop:0.02 rgba(22, 22, 38, 128), "
            f"stop:0.98 rgba(18, 18, 32, 128), stop:1 rgba(12, 12, 22, 128)); "
            f"border: 1px solid {SLATE_DARK}; border-radius: 3px;"
        )

    def panel_bg_flat_css(self):
        """Command, specific. Returns flat panel background CSS — 50% transparent."""
        return (
            f"background: rgba(15, 15, 27, 128); border: 1px solid rgba(30, 30, 42, 160); border-radius: 3px;"
        )

    # --- Texture ---

    def get_background_pixmap(self, height=512):
        """Command, specific. Generate or retrieve cached void texture."""
        if FiligreeStyle._texture_cache is not None:
            return FiligreeStyle._texture_cache
        width = 256
        FiligreeStyle._texture_cache = get_cached_texture(
            "filigree", width, height, lambda: self._generate_texture(width, height)
        )
        return FiligreeStyle._texture_cache

    def _generate_texture(self, width, height):
        """Command, specific. Generate dark void texture with subtle grain."""
        from scipy.ndimage import gaussian_filter

        np.random.seed(1312)

        img = np.zeros((height, width, 4), dtype=np.uint8)
        base_r, base_g, base_b = 15, 15, 27

        # Fine noise
        noise = np.random.random((height, width)).astype(np.float32)
        noise = gaussian_filter(noise, sigma=2.0, mode='wrap')
        noise = (noise - noise.min()) / (noise.max() - noise.min() + 1e-6)

        variation = 0.85 + noise * 0.3
        img[:, :, 0] = np.clip(base_r * variation, 10, 28).astype(np.uint8)
        img[:, :, 1] = np.clip(base_g * variation, 10, 28).astype(np.uint8)
        img[:, :, 2] = np.clip(base_b * variation, 18, 42).astype(np.uint8)
        img[:, :, 3] = 255

        for c in range(3):
            img[:, :, c] = gaussian_filter(img[:, :, c].astype(float), sigma=1.0, mode='wrap').astype(np.uint8)

        qimg = QImage(img.data, width, height, width * 4, QImage.Format.Format_RGBA8888).copy()
        return QPixmap.fromImage(qimg)

    # --- Painting helpers ---

    def _mauve_pen(self, alpha, width=1.2):
        """
        Pure function, general. Create a mauve QPen with round cap.

        Args:
            alpha (int): Opacity 0-255
            width (float): Pen width

        Returns:
            QPen

        Examples:
            >>> p = FiligreeStyle()._mauve_pen(40, 1.5)
            >>> p.color().alpha() == 40
            True
        """
        pen = QPen(QColor(198, 183, 190, alpha), width)
        pen.setCapStyle(Qt.PenCapStyle.RoundCap)
        pen.setJoinStyle(Qt.PenJoinStyle.RoundJoin)
        return pen

    def _draw_spiral(self, painter, cx, cy, start_r, end_r, start_angle, turns, alpha=30, pen_width=1.0):
        """
        Command, specific. Draw a spiral ornament at the given position.

        Args:
            painter: QPainter
            cx, cy (float): Center of spiral
            start_r (float): Starting radius
            end_r (float): Ending radius (spirals inward when < start_r)
            start_angle (float): Starting angle in radians
            turns (float): Number of rotations
            alpha (int): Opacity
            pen_width (float): Line width
        """
        pts = _spiral_points(cx, cy, start_r, end_r, start_angle, turns, num_points=30)
        if len(pts) < 2:
            return
        path = _path_from_points(pts)
        painter.setPen(self._mauve_pen(alpha, pen_width))
        painter.setBrush(Qt.BrushStyle.NoBrush)
        painter.drawPath(path)

    def _draw_beetle_emblem(self, painter, cx, cy, size, alpha=40):
        """
        Command, specific. Draw an abstract beetle/shield shape at top center.

        This is Hollow Knight's signature motif: a pointed oval with wing lines
        and antennae, rendered as delicate filigree.

        Args:
            painter: QPainter
            cx, cy (float): Center of emblem
            size (float): Overall size scale
            alpha (int): Opacity
        """
        pen = self._mauve_pen(alpha, 2.0)
        painter.setPen(pen)
        painter.setBrush(Qt.BrushStyle.NoBrush)

        # Main body - pointed oval (outer shell)
        path = QPainterPath()
        path.moveTo(QPointF(cx, cy - size))  # Top point
        path.cubicTo(
            QPointF(cx + size * 0.65, cy - size * 0.5),
            QPointF(cx + size * 0.55, cy + size * 0.3),
            QPointF(cx, cy + size * 0.85),  # Bottom point
        )
        path.moveTo(QPointF(cx, cy - size))
        path.cubicTo(
            QPointF(cx - size * 0.65, cy - size * 0.5),
            QPointF(cx - size * 0.55, cy + size * 0.3),
            QPointF(cx, cy + size * 0.85),
        )
        # Center line (wing division)
        path.moveTo(QPointF(cx, cy - size * 0.7))
        path.lineTo(QPointF(cx, cy + size * 0.65))
        painter.drawPath(path)

        # Inner shell echo (slightly smaller, fainter -- gives depth)
        inner_shrink = 0.82
        inner_pen = self._mauve_pen(max(10, alpha - 20), 0.8)
        painter.setPen(inner_pen)
        inner = QPainterPath()
        inner.moveTo(QPointF(cx, cy - size * inner_shrink))
        inner.cubicTo(
            QPointF(cx + size * 0.55 * inner_shrink, cy - size * 0.4 * inner_shrink),
            QPointF(cx + size * 0.45 * inner_shrink, cy + size * 0.25),
            QPointF(cx, cy + size * 0.7),
        )
        inner.moveTo(QPointF(cx, cy - size * inner_shrink))
        inner.cubicTo(
            QPointF(cx - size * 0.55 * inner_shrink, cy - size * 0.4 * inner_shrink),
            QPointF(cx - size * 0.45 * inner_shrink, cy + size * 0.25),
            QPointF(cx, cy + size * 0.7),
        )
        painter.drawPath(inner)

        # Wing detail lines - horizontal cross marks
        wing_alpha = max(20, alpha - 5)
        wing_pen = self._mauve_pen(wing_alpha, 0.9)
        painter.setPen(wing_pen)
        for wy_frac in [-0.1, 0.15, 0.35]:
            wy = cy - size * 0.3 + size * wy_frac
            t = (wy - (cy - size)) / (size * 1.85)
            half_w = size * 0.5 * math.sin(max(0, min(1, t)) * math.pi) * 0.7
            if half_w > 1:
                painter.drawLine(
                    QPointF(cx - half_w, wy),
                    QPointF(cx + half_w, wy),
                )

        # "Eyes" - two small dots on the head area
        eye_y = cy - size * 0.55
        eye_x_offset = size * 0.18
        eye_r = max(1.2, size * 0.06)
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(QColor(198, 183, 190, alpha))
        painter.drawEllipse(QPointF(cx - eye_x_offset, eye_y), eye_r, eye_r)
        painter.drawEllipse(QPointF(cx + eye_x_offset, eye_y), eye_r, eye_r)
        painter.setBrush(Qt.BrushStyle.NoBrush)

        # Antennae - curved lines from top
        ant_pen = self._mauve_pen(wing_alpha, 0.9)
        painter.setPen(ant_pen)
        ant = QPainterPath()
        ant.moveTo(QPointF(cx, cy - size * 0.85))
        ant.cubicTo(
            QPointF(cx + size * 0.15, cy - size * 1.3),
            QPointF(cx + size * 0.5, cy - size * 1.35),
            QPointF(cx + size * 0.55, cy - size * 1.15),
        )
        ant.moveTo(QPointF(cx, cy - size * 0.85))
        ant.cubicTo(
            QPointF(cx - size * 0.15, cy - size * 1.3),
            QPointF(cx - size * 0.5, cy - size * 1.35),
            QPointF(cx - size * 0.55, cy - size * 1.15),
        )
        painter.drawPath(ant)

        # Spiral terminations on antennae tips
        self._draw_spiral(painter, cx + size * 0.55, cy - size * 1.15,
                          size * 0.08, size * 0.01, math.pi * 0.5, 1.2,
                          alpha=wing_alpha, pen_width=0.7)
        self._draw_spiral(painter, cx - size * 0.55, cy - size * 1.15,
                          size * 0.08, size * 0.01, math.pi * 0.5, -1.2,
                          alpha=wing_alpha, pen_width=0.7)

    def _draw_dreamcatcher_web(self, painter, cx, cy, radius, alpha=12):
        """
        Command, specific. Draw a faint dreamcatcher-like circular web pattern.

        Concentric irregular circles with curved connecting threads, rendered
        as a ghostly background watermark.

        Args:
            painter: QPainter
            cx, cy (float): Center of web
            radius (float): Outer radius
            alpha (int): Opacity (should be very low, 10-15)
        """
        pen = self._mauve_pen(alpha, 0.7)
        painter.setPen(pen)
        painter.setBrush(Qt.BrushStyle.NoBrush)

        # Concentric rings with slight wobble
        ring_count = 7
        for i in range(1, ring_count + 1):
            r = radius * i / ring_count
            path = QPainterPath()
            wobble_points = 24
            first = True
            for j in range(wobble_points + 1):
                angle = j * 2 * math.pi / wobble_points
                # Slight organic wobble
                wobble = 1.0 + 0.03 * math.sin(angle * 5 + i * 1.7)
                wr = r * wobble
                px = cx + wr * math.cos(angle)
                py = cy + wr * math.sin(angle)
                if first:
                    path.moveTo(QPointF(px, py))
                    first = False
                else:
                    path.lineTo(QPointF(px, py))
            painter.drawPath(path)

        # Radial threads with slight curves
        spoke_count = 12
        inner_pen = self._mauve_pen(max(8, alpha), 0.5)
        painter.setPen(inner_pen)
        for i in range(spoke_count):
            angle = i * 2 * math.pi / spoke_count
            ix = cx + radius * 0.08 * math.cos(angle)
            iy = cy + radius * 0.08 * math.sin(angle)
            ox = cx + radius * math.cos(angle)
            oy = cy + radius * math.sin(angle)
            # Slight curve to each spoke
            ctrl_angle = angle + 0.15
            ctrl_r = radius * 0.55
            ctrl_x = cx + ctrl_r * math.cos(ctrl_angle)
            ctrl_y = cy + ctrl_r * math.sin(ctrl_angle)
            path = QPainterPath()
            path.moveTo(QPointF(ix, iy))
            path.quadTo(QPointF(ctrl_x, ctrl_y), QPointF(ox, oy))
            painter.drawPath(path)

    def _draw_flourish_curve(self, painter, points, alpha=35, pen_width=1.2):
        """
        Command, specific. Draw a smooth flourish curve through control points.

        Args:
            painter: QPainter
            points: List of (x, y) tuples defining the curve
            alpha (int): Opacity
            pen_width (float): Line width
        """
        if len(points) < 2:
            return
        path = QPainterPath()
        path.moveTo(QPointF(*points[0]))
        if len(points) == 3:
            path.quadTo(QPointF(*points[1]), QPointF(*points[2]))
        elif len(points) == 4:
            path.cubicTo(QPointF(*points[1]), QPointF(*points[2]), QPointF(*points[3]))
        elif len(points) >= 5:
            # Multiple cubic segments
            i = 1
            while i + 2 < len(points):
                path.cubicTo(QPointF(*points[i]), QPointF(*points[i + 1]), QPointF(*points[i + 2]))
                i += 3
            # Handle remaining points
            while i < len(points):
                path.lineTo(QPointF(*points[i]))
                i += 1
        else:
            path.lineTo(QPointF(*points[1]))
        painter.setPen(self._mauve_pen(alpha, pen_width))
        painter.setBrush(Qt.BrushStyle.NoBrush)
        painter.drawPath(path)

    def _draw_border_frame(self, painter, width, height, alpha=35):
        """
        Command, specific. Draw the ornamental border frame (Layer 3).

        Top/bottom horizontal flourishes with spiral terminations,
        gothic arch at top center, vertical side ornaments, and
        elaborate corner compositions.

        Args:
            painter: QPainter
            width, height (int): Window dimensions
            alpha (int): Base opacity
        """
        cx = width / 2.0
        margin = 14.0  # Distance from edge

        # --- Top border: horizontal flourish with gothic gable at center ---
        top_y = margin
        gable_height = 24.0  # Height of the pointed arch
        gable_width = 55.0

        # Left half of top border: from left spiral to center gable
        left_start = margin + 12
        left_end = cx - gable_width

        # Main horizontal line with slight upward bow
        self._draw_flourish_curve(painter, [
            (left_start, top_y),
            (left_start + (left_end - left_start) * 0.33, top_y - 3),
            (left_start + (left_end - left_start) * 0.66, top_y - 1.5),
            (left_end, top_y),
        ], alpha=alpha, pen_width=1.5)

        # Right half (mirror)
        right_start = cx + gable_width
        right_end = width - margin - 12
        self._draw_flourish_curve(painter, [
            (right_start, top_y),
            (right_start + (right_end - right_start) * 0.33, top_y - 1.5),
            (right_start + (right_end - right_start) * 0.66, top_y - 3),
            (right_end, top_y),
        ], alpha=alpha, pen_width=1.5)

        # Gothic pointed gable at top center
        path = QPainterPath()
        path.moveTo(QPointF(cx - gable_width, top_y))
        path.cubicTo(
            QPointF(cx - gable_width * 0.4, top_y),
            QPointF(cx - gable_width * 0.15, top_y - gable_height * 0.7),
            QPointF(cx, top_y - gable_height),
        )
        path.cubicTo(
            QPointF(cx + gable_width * 0.15, top_y - gable_height * 0.7),
            QPointF(cx + gable_width * 0.4, top_y),
            QPointF(cx + gable_width, top_y),
        )
        painter.setPen(self._mauve_pen(alpha + 10, 1.5))
        painter.setBrush(Qt.BrushStyle.NoBrush)
        painter.drawPath(path)

        # Echo line (inner) for wrought iron double-line effect
        echo_offset = 4.0
        echo_alpha = max(10, alpha - 20)
        self._draw_flourish_curve(painter, [
            (left_start + 8, top_y + echo_offset),
            (left_start + 8 + (left_end - left_start - 8) * 0.33, top_y + echo_offset - 2),
            (left_start + 8 + (left_end - left_start - 8) * 0.66, top_y + echo_offset - 1),
            (left_end, top_y + echo_offset),
        ], alpha=echo_alpha, pen_width=0.6)
        self._draw_flourish_curve(painter, [
            (right_start, top_y + echo_offset),
            (right_start + (right_end - 8 - right_start) * 0.33, top_y + echo_offset - 1),
            (right_start + (right_end - 8 - right_start) * 0.66, top_y + echo_offset - 2),
            (right_end - 8, top_y + echo_offset),
        ], alpha=echo_alpha, pen_width=0.6)

        # Spiral terminations at top-left and top-right ends
        self._draw_spiral(painter, left_start, top_y, 12, 2.0,
                          math.pi, 1.8, alpha=alpha, pen_width=1.1)
        self._draw_spiral(painter, right_end, top_y, 12, 2.0,
                          0, -1.8, alpha=alpha, pen_width=1.1)

        # --- Bottom border: matching flourish with dangling elements ---
        bot_y = height - margin
        self._draw_flourish_curve(painter, [
            (left_start, bot_y),
            (left_start + (left_end - left_start) * 0.33, bot_y + 2),
            (left_start + (left_end - left_start) * 0.66, bot_y + 3),
            (cx, bot_y),
        ], alpha=alpha, pen_width=1.3)
        self._draw_flourish_curve(painter, [
            (cx, bot_y),
            (cx + (right_end - cx) * 0.33, bot_y + 3),
            (cx + (right_end - cx) * 0.66, bot_y + 2),
            (right_end, bot_y),
        ], alpha=alpha, pen_width=1.3)

        # Bottom echo line (inner)
        self._draw_flourish_curve(painter, [
            (left_start + 8, bot_y - echo_offset),
            (left_start + 8 + (cx - left_start - 8) * 0.33, bot_y - echo_offset + 1),
            (left_start + 8 + (cx - left_start - 8) * 0.66, bot_y - echo_offset + 2),
            (cx, bot_y - echo_offset),
        ], alpha=echo_alpha, pen_width=0.6)
        self._draw_flourish_curve(painter, [
            (cx, bot_y - echo_offset),
            (cx + (right_end - 8 - cx) * 0.33, bot_y - echo_offset + 2),
            (cx + (right_end - 8 - cx) * 0.66, bot_y - echo_offset + 1),
            (right_end - 8, bot_y - echo_offset),
        ], alpha=echo_alpha, pen_width=0.6)

        # Bottom spiral terminations
        self._draw_spiral(painter, left_start, bot_y, 10, 2.0,
                          math.pi, -1.8, alpha=alpha, pen_width=1.0)
        self._draw_spiral(painter, right_end, bot_y, 10, 2.0,
                          0, 1.8, alpha=alpha, pen_width=1.0)

        # Dangling elements at bottom center
        dangle_alpha = max(15, alpha - 5)
        for dx in [-35, -18, 0, 18, 35]:
            dangle_len = 8 if dx == 0 else 6
            self._draw_flourish_curve(painter, [
                (cx + dx, bot_y),
                (cx + dx - 2, bot_y + dangle_len * 0.5),
                (cx + dx + 2, bot_y + dangle_len),
            ], alpha=dangle_alpha, pen_width=0.8)
            self._draw_spiral(painter, cx + dx + 2, bot_y + dangle_len, 3.5, 0.5,
                              0, 1.0, alpha=dangle_alpha, pen_width=0.6)
        # Small dot at bottom center dangle tip
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(QColor(198, 183, 190, dangle_alpha))
        painter.drawEllipse(QPointF(cx + 2, bot_y + 8 + 3.5), 1.5, 1.5)
        painter.setBrush(Qt.BrushStyle.NoBrush)

        # --- Vertical side borders with spiral ornaments ---
        side_alpha = max(10, alpha - 8)
        ornament_count = max(2, int((height - 2 * margin) / 60))

        for side_x in [margin, width - margin]:
            # Vertical line
            painter.setPen(self._mauve_pen(side_alpha, 0.9))
            painter.drawLine(
                QPointF(side_x, top_y + 15),
                QPointF(side_x, bot_y - 15),
            )
            # Spirals at intervals along side
            for i in range(ornament_count):
                t = (i + 1) / (ornament_count + 1)
                oy = top_y + 15 + t * (bot_y - top_y - 30)
                direction = 1.0 if side_x < cx else -1.0
                self._draw_spiral(painter, side_x, oy, 7, 1.0,
                                  math.pi * 0.5 * direction, direction * 1.5,
                                  alpha=side_alpha, pen_width=0.8)

        # --- Corner pieces: elaborate spiral compositions ---
        corner_alpha = alpha + 5
        corner_size = 26.0
        for (corner_x, corner_y, xdir, ydir) in [
            (margin, margin, 1, 1),
            (width - margin, margin, -1, 1),
            (margin, height - margin, 1, -1),
            (width - margin, height - margin, -1, -1),
        ]:
            # Primary corner spiral
            self._draw_spiral(
                painter, corner_x, corner_y,
                corner_size, 2.5,
                math.pi * (0.25 if xdir * ydir > 0 else 0.75),
                xdir * 2.2,
                alpha=corner_alpha, pen_width=1.3,
            )
            # Secondary smaller spiral, offset
            self._draw_spiral(
                painter, corner_x + xdir * 12, corner_y + ydir * 12,
                corner_size * 0.5, 1.5,
                math.pi * (0.75 if xdir * ydir > 0 else 0.25),
                xdir * 1.5,
                alpha=corner_alpha - 10, pen_width=0.9,
            )
            # Tertiary tiny spiral, further offset
            self._draw_spiral(
                painter, corner_x + xdir * 22, corner_y + ydir * 4,
                corner_size * 0.3, 1.0,
                math.pi * 0.5,
                xdir * 1.2,
                alpha=corner_alpha - 15, pen_width=0.6,
            )
            # Connecting S-curve from corner to border
            self._draw_flourish_curve(painter, [
                (corner_x, corner_y),
                (corner_x + xdir * 22, corner_y + ydir * 6),
                (corner_x + xdir * 6, corner_y + ydir * 22),
            ], alpha=corner_alpha - 5, pen_width=1.0)
            # Small dot at spiral center (wrought iron rivet)
            painter.setPen(Qt.PenStyle.NoPen)
            painter.setBrush(QColor(198, 183, 190, corner_alpha))
            painter.drawEllipse(QPointF(corner_x, corner_y), 2.0, 2.0)
            painter.setBrush(Qt.BrushStyle.NoBrush)

        # Decorative dots along top and bottom borders
        dot_alpha = max(15, alpha - 10)
        dot_spacing = 30
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(QColor(198, 183, 190, dot_alpha))
        for bx in range(int(left_start + 25), int(left_end), dot_spacing):
            painter.drawEllipse(QPointF(bx, top_y), 1.2, 1.2)
            painter.drawEllipse(QPointF(bx, bot_y), 1.2, 1.2)
        for bx in range(int(right_start), int(right_end - 10), dot_spacing):
            painter.drawEllipse(QPointF(bx, top_y), 1.2, 1.2)
            painter.drawEllipse(QPointF(bx, bot_y), 1.2, 1.2)
        painter.setBrush(Qt.BrushStyle.NoBrush)

    def _draw_focal_ornaments(self, painter, width, height, alpha=35):
        """
        Command, specific. Draw Layer 4 focal ornaments (emblem + flourishes).

        The beetle emblem at top center with flowing S-curve flourishes,
        and a smaller matching motif at bottom center.

        Args:
            painter: QPainter
            width, height (int): Window dimensions
            alpha (int): Base opacity
        """
        cx = width / 2.0
        margin = 14.0

        # Beetle emblem at top center -- THE focal point
        emblem_y = margin + 48
        emblem_size = min(width, height) * 0.09
        emblem_size = max(26, min(emblem_size, 42))

        # Subtle halo glow behind the emblem
        halo_r = emblem_size * 1.6
        halo = QRadialGradient(QPointF(cx, emblem_y), halo_r)
        halo.setColorAt(0, QColor(45, 0, 78, 18))
        halo.setColorAt(0.6, QColor(45, 0, 78, 6))
        halo.setColorAt(1.0, QColor(45, 0, 78, 0))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(QBrush(halo))
        painter.drawEllipse(QPointF(cx, emblem_y), halo_r, halo_r)

        self._draw_beetle_emblem(painter, cx, emblem_y, emblem_size, alpha=min(255, alpha + 35))

        # S-curve flourishes spreading left and right below the emblem
        flourish_y = emblem_y + emblem_size * 0.9
        spread = min(width * 0.32, 160)

        # Left S-curve (primary + echo)
        for pw, a_off, y_off in [(1.3, 0, 0), (0.7, -15, 3)]:
            self._draw_flourish_curve(painter, [
                (cx, flourish_y + y_off),
                (cx - spread * 0.25, flourish_y + 6 + y_off),
                (cx - spread * 0.5, flourish_y - 5 + y_off),
                (cx - spread * 0.75, flourish_y + 4 + y_off),
                (cx - spread, flourish_y + y_off),
            ], alpha=alpha + a_off, pen_width=pw)
        # Spiral at left terminus
        self._draw_spiral(painter, cx - spread, flourish_y, 8, 1.5,
                          math.pi, 1.5, alpha=alpha, pen_width=0.9)

        # Right S-curve (mirror, primary + echo)
        for pw, a_off, y_off in [(1.3, 0, 0), (0.7, -15, 3)]:
            self._draw_flourish_curve(painter, [
                (cx, flourish_y + y_off),
                (cx + spread * 0.25, flourish_y + 6 + y_off),
                (cx + spread * 0.5, flourish_y - 5 + y_off),
                (cx + spread * 0.75, flourish_y + 4 + y_off),
                (cx + spread, flourish_y + y_off),
            ], alpha=alpha + a_off, pen_width=pw)
        self._draw_spiral(painter, cx + spread, flourish_y, 8, 1.5,
                          0, -1.5, alpha=alpha, pen_width=0.9)

        # Small connecting tendrils from S-curve ends toward border corners
        tendril_alpha = max(15, alpha - 10)
        for sign in [-1, 1]:
            # Tendril curving from S-curve end downward along border
            sx = cx + sign * spread
            self._draw_flourish_curve(painter, [
                (sx, flourish_y),
                (sx + sign * 10, flourish_y + 15),
                (sx + sign * 5, flourish_y + 30),
            ], alpha=tendril_alpha, pen_width=0.6)
            self._draw_spiral(painter, sx + sign * 5, flourish_y + 30, 3, 0.5,
                              math.pi * 0.5, sign * 1.0, alpha=tendril_alpha, pen_width=0.5)

        # Bottom center: smaller matching motif (inverted half-beetle)
        bot_y = height - margin - 16
        small_size = emblem_size * 0.5
        # Small inverted arch
        path = QPainterPath()
        path.moveTo(QPointF(cx - small_size * 1.2, bot_y))
        path.cubicTo(
            QPointF(cx - small_size * 0.4, bot_y),
            QPointF(cx - small_size * 0.15, bot_y - small_size * 0.8),
            QPointF(cx, bot_y - small_size),
        )
        path.cubicTo(
            QPointF(cx + small_size * 0.15, bot_y - small_size * 0.8),
            QPointF(cx + small_size * 0.4, bot_y),
            QPointF(cx + small_size * 1.2, bot_y),
        )
        painter.setPen(self._mauve_pen(alpha - 5, 0.9))
        painter.setBrush(Qt.BrushStyle.NoBrush)
        painter.drawPath(path)

    def _draw_fine_detail(self, painter, width, height, alpha=12):
        """
        Command, specific. Draw Layer 5 fine detail (rosettes, vines, corner fill).

        Tiny spiral rosettes at structural intersections, thin vine extensions
        growing inward from the border, and very faint filigree corner fill.

        Args:
            painter: QPainter
            width, height (int): Window dimensions
            alpha (int): Base opacity (very low for subtlety)
        """
        margin = 14.0
        cx = width / 2.0
        cy = height / 2.0

        # Tiny rosettes at border-border intersections
        rosette_positions = [
            # Where top border meets side borders
            (margin, margin + 15),
            (width - margin, margin + 15),
            # Where bottom border meets side borders
            (margin, height - margin - 15),
            (width - margin, height - margin - 15),
            # Side border midpoints
            (margin, cy),
            (width - margin, cy),
            # Top and bottom center
            (cx, margin),
            (cx, height - margin),
        ]
        for (rx, ry) in rosette_positions:
            # Each rosette is 4 tiny spirals arranged in a cross
            for a_offset in range(4):
                angle = a_offset * 2 * math.pi / 4 + math.pi / 4
                sr = 4.0
                sx = rx + sr * math.cos(angle)
                sy = ry + sr * math.sin(angle)
                self._draw_spiral(painter, sx, sy, 3.5, 0.5, angle, 1.0,
                                  alpha=alpha + 5, pen_width=0.6)

        # Thin vine extensions from border into interior
        vine_alpha = max(10, alpha)
        vine_len = min(width, height) * 0.1

        # Vines from top border
        for vx in [cx - 80, cx + 80]:
            if margin + 20 < vx < width - margin - 20:
                self._draw_flourish_curve(painter, [
                    (vx, margin),
                    (vx + 5, margin + vine_len * 0.4),
                    (vx - 3, margin + vine_len * 0.7),
                    (vx + 2, margin + vine_len),
                ], alpha=vine_alpha, pen_width=0.5)
                self._draw_spiral(painter, vx + 2, margin + vine_len, 2.5, 0.5,
                                  math.pi * 0.5, 1.0, alpha=vine_alpha, pen_width=0.4)

        # Vines from side borders toward center
        for (side_x, direction) in [(margin, 1), (width - margin, -1)]:
            vy = cy - 30
            self._draw_flourish_curve(painter, [
                (side_x, vy),
                (side_x + direction * vine_len * 0.4, vy + 4),
                (side_x + direction * vine_len * 0.7, vy - 2),
                (side_x + direction * vine_len, vy + 1),
            ], alpha=vine_alpha, pen_width=0.5)

        # Very faint corner fill filigree
        fill_alpha = max(10, alpha + 3)
        fill_size = min(width, height) * 0.15
        for (corner_x, corner_y, xdir, ydir) in [
            (margin + 5, margin + 20, 1, 1),
            (width - margin - 5, margin + 20, -1, 1),
            (margin + 5, height - margin - 20, 1, -1),
            (width - margin - 5, height - margin - 20, -1, -1),
        ]:
            # Gentle curved fill lines
            for i in range(3):
                offset = (i + 1) * fill_size * 0.25
                self._draw_flourish_curve(painter, [
                    (corner_x, corner_y + ydir * offset),
                    (corner_x + xdir * offset * 0.6, corner_y + ydir * offset * 0.6),
                    (corner_x + xdir * offset, corner_y),
                ], alpha=fill_alpha, pen_width=0.4)

    def _draw_vignette(self, painter, rect, width, height, radius=12):
        """Command, specific. Dark vignette at edges for enclosure depth."""
        for horizontal, alpha_mult in [(True, 0.7), (False, 0.9)]:
            grad = QLinearGradient(0, 0, width if horizontal else 0, 0 if horizontal else height)
            for pos, a in [(0, 180), (0.08, 100), (0.2, 40), (0.8, 40), (0.92, 100), (1, 180)]:
                grad.setColorAt(pos, QColor(10, 10, 18, int(a * alpha_mult)))
            painter.setBrush(QBrush(grad))
            painter.setPen(Qt.PenStyle.NoPen)
            painter.drawRoundedRect(rect, radius, radius)

    def _draw_center_glow(self, painter, rect, width, height, radius=12):
        """Command, specific. Very faint radial warmth from center (barely perceptible)."""
        center = QPointF(width / 2.0, height * 0.4)
        glow_radius = max(width, height) * 0.5
        glow = QRadialGradient(center, glow_radius)
        glow.setColorAt(0, QColor(45, 0, 78, 20))  # Faint deep purple
        glow.setColorAt(0.4, QColor(45, 0, 78, 10))
        glow.setColorAt(1.0, QColor(45, 0, 78, 0))
        painter.setBrush(QBrush(glow))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawRoundedRect(rect, radius, radius)

    # --- Main paint ---

    def paint_window(self, painter, rect, width, height, focused=True):
        """
        Command, specific. Paint the filigree window with 5 ornamental layers.

        Layer 1: Dark void background with texture and vignette
        Layer 2: Faint dreamcatcher web watermark
        Layer 3: Ornamental border frame with spirals and gothic arch
        Layer 4: Beetle emblem and S-curve flourishes
        Layer 5: Fine detail rosettes, vines, and corner fill
        """
        radius = self.corner_radius

        # Clip to rounded rect
        clip = QPainterPath()
        clip.addRoundedRect(QRectF(rect), radius, radius)
        painter.setClipPath(clip)

        # Layer 1 - Background
        texture = self.get_background_pixmap(max(512, height))
        painter.drawTiledPixmap(rect, texture)

        # Vignette
        self._draw_vignette(painter, rect, width, height, radius)

        # Subtle center glow
        if focused:
            self._draw_center_glow(painter, rect, width, height, radius)

        # Layer 2 - Dreamcatcher web (ghostly watermark)
        web_radius = min(width, height) * 0.38
        web_alpha = 20 if focused else 12
        self._draw_dreamcatcher_web(
            painter, width / 2.0, height * 0.45, web_radius, alpha=web_alpha
        )

        # Remove clip so ornamental elements extend BEYOND window edges
        # (spirals, finials, hanging drops, corner scrollwork float outside)
        painter.setClipping(False)

        # Ornament alpha: brighter when focused
        orn_alpha = 65 if focused else 30

        # Layer 3 - Border frame (ornaments can now extend beyond edges)
        self._draw_border_frame(painter, width, height, alpha=orn_alpha)

        # Layer 4 - Focal ornaments
        self._draw_focal_ornaments(painter, width, height, alpha=orn_alpha)

        # Layer 5 - Fine detail
        self._draw_fine_detail(painter, width, height, alpha=max(14, orn_alpha - 30))

        # Double border -- outer + inner for wrought iron frame look
        painter.setBrush(Qt.BrushStyle.NoBrush)
        if focused:
            painter.setPen(QPen(QColor(198, 183, 190, 100), 1.3))
            painter.drawRoundedRect(rect, radius, radius)
            # Inner border echo
            painter.setPen(QPen(QColor(198, 183, 190, 35), 0.6))
            painter.drawRoundedRect(rect.adjusted(4, 4, -4, -4), radius - 2, radius - 2)
        else:
            painter.setPen(QPen(QColor(86, 90, 117, 60), 0.9))
            painter.drawRoundedRect(rect, radius, radius)

    def paint_waveform_panel(self, painter, rect, w, h, cy):
        """
        Command, specific. Waveform panel: dark recessed with mauve border and arch.

        Dark void background with inset shadow, thin mauve border, and
        a subtle arch motif at top of panel frame.
        """
        # Dark recessed background
        panel_grad = QLinearGradient(0, 0, 0, h)
        panel_grad.setColorAt(0, QColor(10, 10, 20))
        panel_grad.setColorAt(0.3, QColor(14, 14, 26))
        panel_grad.setColorAt(0.7, QColor(12, 12, 23))
        panel_grad.setColorAt(1, QColor(8, 8, 17))
        painter.setBrush(QBrush(panel_grad))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawRoundedRect(rect, 5, 5)

        # Inset shadows
        for grad, adj in [
            (QLinearGradient(0, 0, 0, 12), rect.adjusted(1, 1, -1, -h + 13)),
            (QLinearGradient(0, 0, 10, 0), rect.adjusted(1, 1, -w + 11, -1)),
            (QLinearGradient(w, 0, w - 10, 0), rect.adjusted(w - 11, 1, -1, -1)),
        ]:
            grad.setColorAt(0, QColor(4, 4, 10, 160))
            grad.setColorAt(1, QColor(4, 4, 10, 0))
            painter.setBrush(QBrush(grad))
            painter.setPen(Qt.PenStyle.NoPen)
            painter.drawRoundedRect(adj, 4, 4)

        # Mauve border
        painter.setBrush(Qt.BrushStyle.NoBrush)
        painter.setPen(QPen(QColor(198, 183, 190, 70), 1.0))
        painter.drawRoundedRect(rect, 5, 5)

        # Subtle arch at top of panel
        panel_cx = rect.x() + w / 2.0
        arch_w = min(w * 0.3, 60)
        arch_h = 6
        arch = QPainterPath()
        arch.moveTo(QPointF(panel_cx - arch_w, rect.y()))
        arch.cubicTo(
            QPointF(panel_cx - arch_w * 0.3, rect.y()),
            QPointF(panel_cx - arch_w * 0.1, rect.y() - arch_h),
            QPointF(panel_cx, rect.y() - arch_h),
        )
        arch.cubicTo(
            QPointF(panel_cx + arch_w * 0.1, rect.y() - arch_h),
            QPointF(panel_cx + arch_w * 0.3, rect.y()),
            QPointF(panel_cx + arch_w, rect.y()),
        )
        painter.setPen(QPen(QColor(198, 183, 190, 40), 0.8))
        painter.drawPath(arch)

        # Center line
        painter.setPen(QPen(QColor(198, 183, 190, 30), 1))
        painter.drawLine(0, int(cy), w, int(cy))
