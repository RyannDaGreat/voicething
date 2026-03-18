"""Desert Filigree style — desert sunset palette with calligraphic flourish ornaments.

Merges the warm sunset gradient background and orange accent palette from
DesertSunsetStyle with the Hollow Knight-inspired calligraphic spirals,
gable motifs, and tapered curves from FiligreeFlourishStyle.
"""

import math
from PyQt6.QtCore import Qt, QRectF, QPointF
from PyQt6.QtGui import (
    QColor, QLinearGradient, QRadialGradient, QBrush,
    QPainterPath, QPen
)

from .base import BaseStyle, RED_ERROR, LIGHT_GRAY


# Desert sunset palette (from desert_sunset.py)
SUNSET_ORANGE = QColor(255, 140, 66)
SUNSET_AMBER = QColor(230, 120, 50)
DESERT_PURPLE = QColor(90, 40, 80)
DESERT_ROSE = QColor(196, 107, 107)

BG_GROUND = QColor(30, 18, 14)
BG_WARM = QColor(38, 22, 18)
BG_SKY = QColor(26, 14, 30)

CREAM = "rgb(240,220,200)"
CREAM_DIM = "rgb(200,175,155)"
CREAM_MUTED = "rgb(130,105,90)"
TEXT_DISABLED = "rgb(70,55,45)"

ORANGE_CSS = "rgb(255,140,66)"
ORANGE_DIM_CSS = "rgba(255,140,66,0.6)"

BORDER_DARK = "rgb(55,35,28)"
BORDER_MID = "rgb(80,50,40)"
BORDER_HOVER = "rgb(255,140,66)"

ORANGE_90 = "rgba(255,140,66,0.9)"
ORANGE_60 = "rgba(255,140,66,0.6)"
ORANGE_35 = "rgba(255,140,66,0.35)"
ORANGE_20 = "rgba(255,140,66,0.2)"
ORANGE_12 = "rgba(255,140,66,0.12)"
ORANGE_8 = "rgba(255,140,66,0.08)"
WARM_WHITE_8 = "rgba(255,230,200,0.08)"

# Ornament color — warm amber instead of mauve, to match the desert palette
ORNAMENT = QColor(230, 165, 100)  # Warm amber-gold for filigree on sunset


class DesertFiligreeStyle(BaseStyle):
    """Desert sunset background with calligraphic flourish ornaments.

    Specific. Combines DesertSunsetStyle's warm gradient painting with
    FiligreeFlourishStyle's spiral/gable/tapered-curve drawing primitives.
    """

    name = "desert_filigree"
    font = "Futura"
    text_shadow = (QColor(0, 0, 0, 220), 0, 2, 5)  # 2px dark engrave, stronger blur

    accent = SUNSET_ORANGE
    accent_css = ORANGE_CSS
    text_primary = CREAM
    text_secondary = CREAM_DIM
    text_muted = CREAM_MUTED
    text_error = RED_ERROR
    text_link = ORANGE_90
    border_color = BORDER_MID
    border_dark = BORDER_DARK
    icon_color_dark = '#ffffff'
    icon_color_light = '#ffffff'
    icon_color_muted = '#8a6a55'

    input_bg = '#241610'
    input_text = '#f0dcc8'

    slider_groove = "rgba(255,140,66,0.30)"

    knob_style = "glass"
    knob_body_dark = "#1e120e"
    knob_body_light = "#4a3028"
    knob_notch_style = "line"
    knob_tickmarks = False
    knob_glow = True
    knob_track_color = "#FF8C42"
    knob_label_color = "#d4a880"

    waveform_color = SUNSET_ORANGE
    waveform_glow = True
    waveform_glow_radius = 18
    waveform_glow_alpha = 180
    waveform_center_line = QColor(255, 140, 66, 30)
    waveform_panel = "dark"

    timer_use_lcd = True
    timer_color = SUNSET_ORANGE

    transcription_text = LIGHT_GRAY
    transcription_text_dimmed = CREAM_MUTED
    transcription_panel_bg = "rgba(30, 18, 14, 128)"
    transcription_panel_border = BORDER_DARK
    transcription_row_hover = ORANGE_8
    transcription_row_btn_bg = WARM_WHITE_8
    transcription_row_btn_hover = ORANGE_20
    transcription_row_btn_pressed = ORANGE_35

    chime_grid_bg = QColor(30, 18, 14)
    chime_grid_line = QColor(60, 40, 32)
    chime_cell_inactive = QColor(45, 28, 22)
    chime_cell_active = QColor(255, 140, 66)
    chime_cell_highlight = QColor(255, 140, 66, 70)
    chime_piano_white = QColor(230, 210, 190)
    chime_piano_black = QColor(30, 18, 14)
    chime_piano_label_white = QColor(80, 55, 40)
    chime_piano_label_black = QColor(210, 165, 120)

    def button_css(self):
        """Command, specific. Glass pill buttons with warm brown gradient and orange accents."""
        return (
            f"QPushButton {{ color: {CREAM_DIM}; "
            f"background: qlineargradient(x1:0, y1:0, x2:0, y2:1, "
            f"stop:0 rgba(75,48,38,0.9), stop:0.1 rgba(58,36,28,0.9), "
            f"stop:0.9 rgba(38,22,16,0.9), stop:1 rgba(32,18,14,0.9)); "
            f"border: 1px solid {BORDER_MID}; "
            f"border-radius: 4px; padding: 2px 4px; font-size: 10px; "
            f"font-family: {self.font}; text-align: left; }}"
            f"QPushButton:hover {{ "
            f"background: qlineargradient(x1:0, y1:0, x2:0, y2:1, "
            f"stop:0 rgba(90,58,45,0.95), stop:0.1 rgba(72,45,35,0.95), "
            f"stop:0.9 rgba(52,32,24,0.95), stop:1 rgba(45,28,20,0.95)); "
            f"border: 1px solid {BORDER_HOVER}; }}"
            f"QPushButton:pressed {{ "
            f"background: qlineargradient(x1:0, y1:0, x2:0, y2:1, "
            f"stop:0 rgba(35,20,14,0.95), stop:0.1 rgba(40,25,18,0.95), "
            f"stop:0.9 rgba(55,35,26,0.95), stop:1 rgba(65,42,32,0.95)); "
            f"border: 1px solid {ORANGE_60}; }}"
            f"QPushButton:disabled {{ color: {TEXT_DISABLED}; "
            f"background: rgba(30,18,14,0.3); border: 1px solid rgba(50,35,28,0.3); }}"
            f"QPushButton:checked {{ "
            f"background: qlineargradient(x1:0, y1:0, x2:0, y2:1, "
            f"stop:0 rgba(160,80,30,0.5), stop:0.1 rgba(130,65,25,0.5), "
            f"stop:0.9 rgba(100,50,20,0.5), stop:1 rgba(85,42,18,0.5)); "
            f"border: 1px solid {ORANGE_60}; }}"
            f"QPushButton:checked:hover {{ "
            f"background: qlineargradient(x1:0, y1:0, x2:0, y2:1, "
            f"stop:0 rgba(180,90,35,0.6), stop:0.1 rgba(150,75,30,0.6), "
            f"stop:0.9 rgba(120,60,25,0.6), stop:1 rgba(105,52,22,0.6)); }}"
        )

    def menu_css(self):
        """Command, specific. Warm dark menu with orange accents."""
        return (
            f"QMenu {{ "
            f"background: qlineargradient(x1:0, y1:0, x2:0, y2:1, "
            f"stop:0 rgba(58,36,28,0.95), stop:1 rgba(35,20,16,0.95)); "
            f"color: {CREAM}; border: 1px solid rgba(100,60,45,0.6); "
            f"border-radius: 8px; padding: 6px; font-family: {self.font}; }}"
            "QMenu::item { padding: 6px 14px; border-radius: 5px; }"
            "QMenu::item:selected { "
            "background: qlineargradient(x1:0, y1:0, x2:0, y2:1, "
            "stop:0 rgba(255,140,66,0.3), stop:1 rgba(200,100,40,0.3)); }"
            f"QMenu::separator {{ height: 1px; background: rgba(255,180,130,0.2); margin: 4px 8px; }}"
        )

    def _scrollbar_vertical_css(self):
        """Command, specific."""
        return (
            "QScrollBar:vertical { width: 10px; background: transparent; margin: 2px; border: none; }"
            "QScrollBar::handle:vertical { "
            "background: qlineargradient(x1:0, y1:0, x2:1, y2:0, "
            "stop:0 rgba(120,70,45,0.6), stop:0.5 rgba(150,85,55,0.7), stop:1 rgba(120,70,45,0.6)); "
            "border-radius: 5px; min-height: 30px; margin: 0px; }"
            "QScrollBar::handle:vertical:hover { "
            "background: qlineargradient(x1:0, y1:0, x2:1, y2:0, "
            "stop:0 rgba(200,110,50,0.5), stop:0.5 rgba(255,140,66,0.6), stop:1 rgba(200,110,50,0.5)); }"
            "QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical { height: 0; }"
            "QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical { background: transparent; }"
        )

    def panel_bg_css(self):
        """Command, specific."""
        return (
            "background: qlineargradient(x1:0, y1:0, x2:0, y2:1, "
            "stop:0 rgba(48,30,22,0.5), stop:1 rgba(32,18,14,0.5)); "
            f"border: 1px solid {BORDER_MID}; "
            "border-radius: 8px;"
        )

    def panel_bg_flat_css(self):
        """Command, specific."""
        return (
            "background: qlineargradient(x1:0, y1:0, x2:0, y2:1, "
            "stop:0 rgba(38,22,16,0.5), stop:1 rgba(26,14,12,0.5)); "
            f"border: 1px solid {BORDER_DARK}; "
            "border-radius: 8px;"
        )

    # ── Calligraphic drawing primitives (from filigree_flourish.py) ──────

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
            cr = r * 1.15
            ca = angle - math.pi / SEGMENTS_PER_TURN
            ctrl_x = cx + cr * math.cos(ca)
            ctrl_y = cy + cr * math.sin(ca) * direction
            path.quadTo(QPointF(ctrl_x, ctrl_y), QPointF(ex, ey))

        painter.drawPath(path)

    def _draw_tapered_curve(self, painter, points, base_width, tip_width, color):
        """Draw a curve with thick-to-thin tapering by rendering parallel strokes.

        Command, specific.

        Args:
            painter: QPainter to draw on
            points (list[QPointF]): Points along the curve
            base_width (float): Pen width at the start
            tip_width (float): Pen width at the end
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
            list[QPointF]
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
        """
        NUM_SAMPLES = 24
        points = self._sample_cubic(p0, p1, p2, p3, NUM_SAMPLES)
        self._draw_tapered_curve(painter, points, base_width, tip_width, color)

    def _draw_gable_motif(self, painter, cx, cy, scale, color, mirror=False):
        """Draw a gable motif — upward-curving line terminating in spirals.

        Command, specific. Primary ornamental building block.

        Args:
            painter: QPainter to draw on
            cx (float): Horizontal center
            cy (float): Vertical base
            scale (float): Size multiplier (1.0 = ~80px wide)
            color (QColor): Stroke color
            mirror (bool): If True, flip vertically
        """
        s = scale
        flip = -1 if mirror else 1

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

    def _draw_top_flourish(self, painter, width, height, alpha):
        """Draw elaborate horizontal flourish along the top edge.

        Command, specific. Gable motifs + sweeping S-curves with spiral terminations.
        """
        cx = width / 2
        color = QColor(ORNAMENT.red(), ORNAMENT.green(), ORNAMENT.blue(), alpha)
        color_mid = QColor(ORNAMENT.red(), ORNAMENT.green(), ORNAMENT.blue(), int(alpha * 0.7))
        color_dim = QColor(ORNAMENT.red(), ORNAMENT.green(), ORNAMENT.blue(), alpha // 2)
        color_faint = QColor(ORNAMENT.red(), ORNAMENT.green(), ORNAMENT.blue(), alpha // 3)
        TOP_Y = 18

        # Thin horizontal spine
        line_extent = width * 0.46
        painter.setPen(QPen(color_faint, 0.8, cap=Qt.PenCapStyle.RoundCap))
        painter.setBrush(Qt.BrushStyle.NoBrush)
        painter.drawLine(QPointF(cx - line_extent, TOP_Y + 15), QPointF(cx + line_extent, TOP_Y + 15))

        # Central gable — triple-nested
        self._draw_gable_motif(painter, cx, TOP_Y + 38, scale=1.5, color=color)
        self._draw_gable_motif(painter, cx, TOP_Y + 30, scale=0.8, color=color_mid)
        self._draw_gable_motif(painter, cx, TOP_Y + 25, scale=0.4, color=color_dim)

        # Flanking gables
        gable_offset = width * 0.25
        self._draw_gable_motif(painter, cx - gable_offset, TOP_Y + 26, scale=0.65, color=color_dim)
        self._draw_gable_motif(painter, cx + gable_offset, TOP_Y + 26, scale=0.65, color=color_dim)

        # Long sweeping S-curves from center outward
        for sign in [-1, 1]:
            self._draw_tapered_cubic(
                painter,
                QPointF(cx + sign * 55, TOP_Y + 15),
                QPointF(cx + sign * 110, TOP_Y + 4),
                QPointF(cx + sign * (width * 0.33), TOP_Y + 24),
                QPointF(cx + sign * (width * 0.45), TOP_Y + 12),
                2.8, 0.5, color_mid
            )
            self._draw_spiral(
                painter,
                cx + sign * (width * 0.45), TOP_Y + 12,
                start_radius=8, turns=1.5, direction=sign,
                start_angle=0,
                pen=QPen(color_mid, 0.8, cap=Qt.PenCapStyle.RoundCap)
            )
            self._draw_tapered_cubic(
                painter,
                QPointF(cx + sign * 60, TOP_Y + 22),
                QPointF(cx + sign * 120, TOP_Y + 14),
                QPointF(cx + sign * (width * 0.32), TOP_Y + 28),
                QPointF(cx + sign * (width * 0.42), TOP_Y + 20),
                1.4, 0.3, color_dim
            )

        # Tiny spiral clusters at spine endpoints
        for sign in [-1, 1]:
            self._draw_spiral(
                painter, cx + sign * line_extent, TOP_Y + 15,
                start_radius=4, turns=1.2, direction=sign,
                start_angle=math.pi if sign == -1 else 0,
                pen=QPen(color_dim, 0.6, cap=Qt.PenCapStyle.RoundCap)
            )
            self._draw_spiral(
                painter, cx + sign * line_extent, TOP_Y + 15,
                start_radius=3, turns=0.8, direction=-sign,
                start_angle=(math.pi if sign == -1 else 0) + math.pi * 0.3,
                pen=QPen(color_faint, 0.4, cap=Qt.PenCapStyle.RoundCap)
            )

    def _draw_bottom_flourish(self, painter, width, height, alpha):
        """Draw matching flourish along the bottom edge.

        Command, specific. Inverted gable motifs, simpler than top.
        """
        cx = width / 2
        color = QColor(ORNAMENT.red(), ORNAMENT.green(), ORNAMENT.blue(), alpha)
        color_mid = QColor(ORNAMENT.red(), ORNAMENT.green(), ORNAMENT.blue(), int(alpha * 0.7))
        color_dim = QColor(ORNAMENT.red(), ORNAMENT.green(), ORNAMENT.blue(), alpha // 2)
        color_faint = QColor(ORNAMENT.red(), ORNAMENT.green(), ORNAMENT.blue(), alpha // 3)
        BOT_Y = height - 18

        # Thin horizontal spine
        line_extent = width * 0.40
        painter.setPen(QPen(color_faint, 0.7, cap=Qt.PenCapStyle.RoundCap))
        painter.setBrush(Qt.BrushStyle.NoBrush)
        painter.drawLine(QPointF(cx - line_extent, BOT_Y - 12), QPointF(cx + line_extent, BOT_Y - 12))

        # Central inverted gable + nested
        self._draw_gable_motif(painter, cx, BOT_Y - 28, scale=1.0, color=color, mirror=True)
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

        Command, specific.
        """
        color = QColor(ORNAMENT.red(), ORNAMENT.green(), ORNAMENT.blue(), alpha)
        color_dim = QColor(ORNAMENT.red(), ORNAMENT.green(), ORNAMENT.blue(), int(alpha * 0.7))
        color_echo = QColor(ORNAMENT.red(), ORNAMENT.green(), ORNAMENT.blue(), alpha // 3)
        reach = min(width, height) * 0.32

        corners = [
            (0, 0, 1, 1, 1, math.pi * 1.5),
            (width, 0, -1, 1, -1, math.pi * 1.5),
            (0, height, 1, -1, -1, math.pi * 0.5),
            (width, height, -1, -1, 1, math.pi * 0.5),
        ]

        for sx, sy, dx, dy, sdir, sa in corners:
            self._draw_tapered_cubic(
                painter,
                QPointF(sx + dx * 8, sy + dy * reach * 0.7),
                QPointF(sx + dx * 14, sy + dy * reach * 0.35),
                QPointF(sx + dx * reach * 0.35, sy + dy * 14),
                QPointF(sx + dx * reach * 0.7, sy + dy * 8),
                2.8, 0.6, color
            )
            self._draw_spiral(
                painter,
                sx + dx * reach * 0.7, sy + dy * 8,
                start_radius=8, turns=1.6, direction=sdir,
                start_angle=sa,
                pen=QPen(color_dim, 0.8, cap=Qt.PenCapStyle.RoundCap)
            )
            self._draw_tapered_cubic(
                painter,
                QPointF(sx + dx * 5, sy + dy * reach * 0.9),
                QPointF(sx + dx * 18, sy + dy * reach * 0.5),
                QPointF(sx + dx * reach * 0.5, sy + dy * 18),
                QPointF(sx + dx * reach * 0.9, sy + dy * 5),
                1.5, 0.3, color_echo
            )
            self._draw_spiral(
                painter,
                sx + dx * 5, sy + dy * reach * 0.9,
                start_radius=5, turns=1.2, direction=-sdir,
                start_angle=sa + math.pi,
                pen=QPen(color_echo, 0.5, cap=Qt.PenCapStyle.RoundCap)
            )
            self._draw_spiral(
                painter,
                sx + dx * reach * 0.45, sy + dy * reach * 0.45,
                start_radius=4, turns=1.0, direction=sdir,
                start_angle=sa + math.pi * 0.5,
                pen=QPen(color_echo, 0.4, cap=Qt.PenCapStyle.RoundCap)
            )

    def _draw_side_filigree(self, painter, width, height, alpha):
        """Draw decorative spiral pairs along left and right edges.

        Command, specific.
        """
        color = QColor(ORNAMENT.red(), ORNAMENT.green(), ORNAMENT.blue(), int(alpha * 0.45))
        color_faint = QColor(ORNAMENT.red(), ORNAMENT.green(), ORNAMENT.blue(), alpha // 4)
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

            for x, angle_base in [(MARGIN + 6, 0), (width - MARGIN - 6, math.pi)]:
                self._draw_spiral(
                    painter, x, y - 5,
                    start_radius=5, turns=1.1, direction=1,
                    start_angle=angle_base,
                    pen=QPen(color, 0.6, cap=Qt.PenCapStyle.RoundCap)
                )
                self._draw_spiral(
                    painter, x, y + 5,
                    start_radius=5, turns=1.1, direction=-1,
                    start_angle=angle_base,
                    pen=QPen(color, 0.6, cap=Qt.PenCapStyle.RoundCap)
                )

    # ── Main painting ────────────────────────────────────────────────────

    def paint_window(self, painter, rect, width, height, focused=True):
        """Paint desert sunset background with calligraphic flourish ornaments.

        Command, specific. Layers: sunset gradient → sun glow → horizon →
        sky darkening → unclipped filigree ornaments → border.
        """
        radius = self.corner_radius
        alpha_mult = 1.0 if focused else 0.85

        # Clip to rounded rect for background painting
        path = QPainterPath()
        path.addRoundedRect(QRectF(rect), radius, radius)
        painter.setClipPath(path)

        # Layer 1: Sky-to-ground gradient (from desert_sunset)
        grad = QLinearGradient(0, rect.top(), 0, rect.bottom())
        grad.setColorAt(0.0, QColor(28, 12, 35, int(255 * alpha_mult)))
        grad.setColorAt(0.2, QColor(45, 18, 38, int(255 * alpha_mult)))
        grad.setColorAt(0.35, QColor(65, 25, 30, int(255 * alpha_mult)))
        grad.setColorAt(0.45, QColor(80, 35, 22, int(255 * alpha_mult)))
        grad.setColorAt(0.55, QColor(55, 28, 18, int(255 * alpha_mult)))
        grad.setColorAt(0.8, QColor(34, 20, 15, int(255 * alpha_mult)))
        grad.setColorAt(1.0, QColor(24, 12, 10, int(255 * alpha_mult)))
        painter.setBrush(QBrush(grad))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawRect(rect)

        # Layer 2: Radial sun glow at the horizon
        sun_x = rect.left() + width * 0.6
        sun_y = rect.top() + height * 0.42
        sun_r = max(width, height) * 0.45
        sun = QRadialGradient(QPointF(sun_x, sun_y), sun_r)
        sun.setColorAt(0, QColor(255, 180, 80, int(35 * alpha_mult)))
        sun.setColorAt(0.15, QColor(255, 140, 50, int(25 * alpha_mult)))
        sun.setColorAt(0.3, QColor(255, 100, 40, int(15 * alpha_mult)))
        sun.setColorAt(0.5, QColor(200, 60, 40, int(8 * alpha_mult)))
        sun.setColorAt(1, QColor(100, 30, 30, 0))
        painter.setBrush(QBrush(sun))
        painter.drawRect(rect)

        # Layer 3: Thin bright horizon line
        horizon_y = rect.top() + int(height * 0.43)
        horizon_line = QLinearGradient(rect.left(), horizon_y - 3, rect.left(), horizon_y + 3)
        horizon_line.setColorAt(0, QColor(255, 160, 60, 0))
        horizon_line.setColorAt(0.5, QColor(255, 160, 60, int(20 * alpha_mult)))
        horizon_line.setColorAt(1, QColor(255, 160, 60, 0))
        painter.setBrush(QBrush(horizon_line))
        painter.drawRect(rect.left(), horizon_y - 3, width, 6)

        # Layer 4: Purple sky darkening at top
        sky_dark = QLinearGradient(0, rect.top(), 0, rect.top() + int(height * 0.15))
        sky_dark.setColorAt(0, QColor(15, 5, 25, int(40 * alpha_mult)))
        sky_dark.setColorAt(1, QColor(0, 0, 0, 0))
        painter.setBrush(QBrush(sky_dark))
        painter.drawRect(rect)

        # Unclip for filigree ornaments extending beyond borders
        painter.setClipping(False)

        ornament_alpha = 110 if focused else 50

        # Layer 5: Filigree ornaments (from filigree_flourish)
        self._draw_side_filigree(painter, width, height, ornament_alpha)
        self._draw_corner_spirals(painter, width, height, ornament_alpha)
        self._draw_top_flourish(painter, width, height, ornament_alpha)
        self._draw_bottom_flourish(painter, width, height, ornament_alpha)

        painter.setClipping(False)

        # Border and focus glow
        painter.setBrush(Qt.BrushStyle.NoBrush)
        if focused:
            for i in range(3):
                glow_alpha = int(35 - i * 10)
                painter.setPen(QPen(QColor(255, 140, 66, glow_alpha), 3 + i * 2))
                painter.drawRoundedRect(rect.adjusted(-i, -i, i, i), radius + i, radius + i)
            painter.setPen(QPen(self.accent, 2))
            painter.drawRoundedRect(rect, radius, radius)
        else:
            painter.setPen(QPen(QColor(80, 50, 40, 150), 1))
            painter.drawRoundedRect(rect, radius, radius)

    def paint_waveform_panel(self, painter, rect, w, h, cy):
        """Dark desert waveform panel with warm-toned grid.

        Command, specific.
        """
        panel_grad = QLinearGradient(0, 0, 0, h)
        panel_grad.setColorAt(0.0, QColor(38, 22, 16, 240))
        panel_grad.setColorAt(0.5, QColor(30, 18, 14, 240))
        panel_grad.setColorAt(1.0, QColor(24, 14, 12, 240))
        painter.setBrush(QBrush(panel_grad))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawRoundedRect(rect, 8, 8)

        # Subtle warm orange grid
        painter.setPen(QPen(QColor(255, 140, 66, 15), 1))
        for i in range(1, 4):
            y = int(h * i / 4)
            painter.drawLine(0, y, w, y)
        num_sections = 8
        for i in range(1, num_sections):
            painter.drawLine(int(w * i / num_sections), 0, int(w * i / num_sections), h)

        # Subtle warm border
        painter.setBrush(Qt.BrushStyle.NoBrush)
        painter.setPen(QPen(QColor(70, 45, 35, 150), 1))
        painter.drawRoundedRect(rect, 8, 8)
