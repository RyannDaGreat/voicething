"""Filigree style - wrought iron scrollwork and insect wing venation on void black.

Inspired by Hollow Knight's aesthetic: ornate iron gates, gothic cathedral
metalwork, and the branching patterns of butterfly wings. The palette is
cold purples and mauves against near-black, with no gold whatsoever.
"""

import math
from PyQt6.QtCore import Qt, QRectF, QPointF
from PyQt6.QtGui import (
    QColor, QLinearGradient, QRadialGradient, QBrush,
    QPainterPath, QPen,
)

from .base import BaseStyle

# ── Palette ──────────────────────────────────────────────────────────────────
VOID_BLACK = "rgb(15, 15, 27)"
VOID_DEEP  = "rgb(20, 20, 35)"
SLATE_DARK = "rgb(55, 58, 75)"
SLATE_MID  = "rgb(86, 90, 117)"
MAUVE      = "rgb(198, 183, 190)"
OFF_WHITE  = "rgb(250, 251, 246)"
DEEP_PURPLE = "rgb(45, 0, 78)"

# QColor versions for painter operations
_MAUVE_Q    = QColor(198, 183, 190)
_VOID_Q     = QColor(15, 15, 27)
_SLATE_MID_Q = QColor(86, 90, 117)
_DEEP_PURPLE_Q = QColor(45, 0, 78)


# ── Drawing helpers ──────────────────────────────────────────────────────────

def _draw_s_scroll(painter, cx, cy, w, h, alpha, flip_x=False, flip_y=False):
    """
    Command, specific. Draw a single S-scroll (the classic wrought iron motif).

    The scroll is a pair of opposing arcs that form an S-shape, centered at
    (cx, cy) within a bounding box of (w, h). flip_x/flip_y mirror it.

    Args:
        painter: QPainter
        cx (float): Center x
        cy (float): Center y
        w (float): Bounding width
        h (float): Bounding height
        alpha (int): Opacity 0-255
        flip_x (bool): Mirror horizontally
        flip_y (bool): Mirror vertically
    """
    sx = -1 if flip_x else 1
    sy = -1 if flip_y else 1
    hw, hh = w / 2, h / 2

    # Build the S-curve path once, draw it twice (shadow + main)
    def _make_s_path():
        """Near-pure function (creates QPainterPath objects). Build the S-scroll path pair."""
        upper = QPainterPath()
        upper.moveTo(cx - sx * hw * 0.1, cy - sy * hh)
        upper.cubicTo(
            cx - sx * hw,       cy - sy * hh * 0.6,
            cx - sx * hw * 0.6, cy - sy * hh * 0.1,
            cx,                 cy,
        )
        lower = QPainterPath()
        lower.moveTo(cx, cy)
        lower.cubicTo(
            cx + sx * hw * 0.6, cy + sy * hh * 0.1,
            cx + sx * hw,       cy + sy * hh * 0.6,
            cx + sx * hw * 0.1, cy + sy * hh,
        )
        return upper, lower

    upper, lower = _make_s_path()

    # Shadow/glow pass -- slightly thicker, lower alpha
    glow_pen = QPen(QColor(198, 183, 190, int(alpha * 0.3)), 3.0)
    glow_pen.setCapStyle(Qt.PenCapStyle.RoundCap)
    painter.setPen(glow_pen)
    painter.setBrush(Qt.BrushStyle.NoBrush)
    painter.drawPath(upper)
    painter.drawPath(lower)

    # Main pass
    main_pen = QPen(QColor(198, 183, 190, alpha), 1.5)
    main_pen.setCapStyle(Qt.PenCapStyle.RoundCap)
    painter.setPen(main_pen)
    painter.drawPath(upper)
    painter.drawPath(lower)

    # Terminal spirals at ends
    _draw_spiral_rosette(painter, cx - sx * hw * 0.1, cy - sy * hh, w * 0.12, alpha * 0.8)
    _draw_spiral_rosette(painter, cx + sx * hw * 0.1, cy + sy * hh, w * 0.12, alpha * 0.8)


def _draw_branching_vine(painter, start_x, start_y, angle, length, depth, alpha,
                         branch_angle_deg=35, length_decay=0.65, max_depth=5):
    """
    Command, specific. Recursively draw a branching vine pattern
    (insect wing venation / wrought iron scrollwork).

    Each segment is a slightly curved line that branches into two children
    at decreasing scale. The result resembles wing venation or forked ironwork.

    Args:
        painter: QPainter
        start_x (float): Starting x coordinate
        start_y (float): Starting y coordinate
        angle (float): Direction in radians
        length (float): Segment length in pixels
        depth (int): Current recursion depth (0 = deepest)
        alpha (int): Base opacity 0-255
        branch_angle_deg (float): Angle between child branches in degrees
        length_decay (float): Length multiplier per depth level
        max_depth (int): Maximum recursion depth
    """
    if depth <= 0 or length < 2:
        return

    # Compute endpoint
    end_x = start_x + math.cos(angle) * length
    end_y = start_y + math.sin(angle) * length

    # Slight curve via a control point offset perpendicular to the direction
    curve_amount = length * 0.15 * (1 if depth % 2 == 0 else -1)
    perp_angle = angle + math.pi / 2
    ctrl_x = (start_x + end_x) / 2 + math.cos(perp_angle) * curve_amount
    ctrl_y = (start_y + end_y) / 2 + math.sin(perp_angle) * curve_amount

    # Thicker for main branches, thinner for tips
    thickness = max(0.4, 0.4 + (depth / max_depth) * 1.2)
    line_alpha = int(alpha * (0.4 + 0.6 * depth / max_depth))
    pen = QPen(QColor(198, 183, 190, line_alpha), thickness)
    pen.setCapStyle(Qt.PenCapStyle.RoundCap)
    painter.setPen(pen)
    painter.setBrush(Qt.BrushStyle.NoBrush)

    path = QPainterPath()
    path.moveTo(start_x, start_y)
    path.quadTo(ctrl_x, ctrl_y, end_x, end_y)
    painter.drawPath(path)

    # Branch into two children
    branch_rad = math.radians(branch_angle_deg)
    child_len = length * length_decay
    _draw_branching_vine(painter, end_x, end_y, angle - branch_rad * 0.6,
                         child_len, depth - 1, alpha, branch_angle_deg,
                         length_decay, max_depth)
    _draw_branching_vine(painter, end_x, end_y, angle + branch_rad * 0.6,
                         child_len, depth - 1, alpha, branch_angle_deg,
                         length_decay, max_depth)

    # Add a smaller center continuation for richer branching
    if depth > 2:
        _draw_branching_vine(painter, end_x, end_y, angle + branch_rad * 0.1,
                             child_len * 0.8, depth - 2, alpha, branch_angle_deg,
                             length_decay, max_depth)


def _draw_spiral_rosette(painter, cx, cy, radius, alpha):
    """
    Command, specific. Draw a small spiral rosette at intersection points.

    A tight inward spiral of ~1.5 turns that looks like a coiled iron terminal.

    Args:
        painter: QPainter
        cx (float): Center x
        cy (float): Center y
        radius (float): Outer radius of the spiral
        alpha (float): Opacity 0-255 (float, will be clamped to int)
    """
    if radius < 1.5:
        return
    clamped_alpha = int(max(0, min(255, alpha)))
    pen = QPen(QColor(198, 183, 190, clamped_alpha), max(0.6, radius * 0.15))
    pen.setCapStyle(Qt.PenCapStyle.RoundCap)
    painter.setPen(pen)
    painter.setBrush(Qt.BrushStyle.NoBrush)

    num_points = 30
    total_angle = math.pi * 4  # 2 full turns for tighter coil
    path = QPainterPath()
    for i in range(num_points + 1):
        t = i / num_points
        a = t * total_angle
        r = radius * (1 - t * 0.88)  # Spiral inward tightly
        x = cx + math.cos(a) * r
        y = cy + math.sin(a) * r
        if i == 0:
            path.moveTo(x, y)
        else:
            path.lineTo(x, y)
    painter.drawPath(path)


def _draw_ornate_frame(painter, width, height, focused):
    """
    Command, specific. Draw the full ornamental wrought iron frame.

    Layers (back to front):
      1. Structural double-border bars
      2. Large S-scroll lyre at top/bottom center
      3. Elaborate corner scrollwork with multiple curls
      4. Wing venation on left/right (dense branching)
      5. Decorative finials (top) and hanging drops (bottom)
      6. Fine connecting bars and rosettes throughout

    Args:
        painter: QPainter
        width (int): Window width
        height (int): Window height
        focused (bool): Whether the window has focus (affects alpha)
    """
    alpha_base = 90 if focused else 45
    margin = 5  # Distance from window edge to outer frame bar

    # ── Layer 1: Structural double-border bars ───────────────────────────
    # Outer frame
    outer_pen = QPen(QColor(198, 183, 190, int(alpha_base * 1.1)), 2.2)
    outer_pen.setCapStyle(Qt.PenCapStyle.RoundCap)
    painter.setPen(outer_pen)
    painter.setBrush(Qt.BrushStyle.NoBrush)
    corner_r = 10
    frame_rect = QRectF(margin, margin, width - margin * 2, height - margin * 2)
    frame_path = QPainterPath()
    frame_path.addRoundedRect(frame_rect, corner_r, corner_r)
    painter.drawPath(frame_path)

    # Inner parallel frame (thinner)
    inner_gap = 7
    inner_m = margin + inner_gap
    inner_pen = QPen(QColor(198, 183, 190, int(alpha_base * 0.45)), 1.0)
    inner_pen.setCapStyle(Qt.PenCapStyle.RoundCap)
    painter.setPen(inner_pen)
    inner_rect = QRectF(inner_m, inner_m, width - inner_m * 2, height - inner_m * 2)
    inner_path = QPainterPath()
    inner_path.addRoundedRect(inner_rect, corner_r - 3, corner_r - 3)
    painter.drawPath(inner_path)

    # Thin cross-bars connecting outer to inner at regular intervals (top/bottom)
    cross_pen = QPen(QColor(198, 183, 190, int(alpha_base * 0.3)), 0.7)
    cross_pen.setCapStyle(Qt.PenCapStyle.RoundCap)
    painter.setPen(cross_pen)
    num_crosses = 12
    for i in range(num_crosses):
        x = width * (0.1 + 0.8 * i / (num_crosses - 1))
        # Top cross-bars
        painter.drawLine(QPointF(x, margin), QPointF(x, inner_m))
        # Bottom cross-bars
        painter.drawLine(QPointF(x, height - margin), QPointF(x, height - inner_m))

    # Side cross-bars
    num_side_crosses = 8
    for i in range(num_side_crosses):
        y = height * (0.1 + 0.8 * i / (num_side_crosses - 1))
        painter.drawLine(QPointF(margin, y), QPointF(inner_m, y))
        painter.drawLine(QPointF(width - margin, y), QPointF(width - inner_m, y))

    # ── Layer 2: Top center lyre (large mirrored S-scrolls) ──────────────
    top_cx = width / 2
    scroll_w = min(width * 0.35, 160)
    scroll_h = min(height * 0.18, 70)

    # Large lyre - two S-scrolls mirrored, wider apart
    lyre_alpha = int(alpha_base * 0.95)
    _draw_s_scroll(painter, top_cx - scroll_w * 0.3, margin + scroll_h * 0.45,
                   scroll_w * 0.6, scroll_h, lyre_alpha)
    _draw_s_scroll(painter, top_cx + scroll_w * 0.3, margin + scroll_h * 0.45,
                   scroll_w * 0.6, scroll_h, lyre_alpha, flip_x=True)

    # Smaller inner lyre pair for layered depth
    inner_lyre_alpha = int(alpha_base * 0.6)
    _draw_s_scroll(painter, top_cx - scroll_w * 0.15, margin + scroll_h * 0.38,
                   scroll_w * 0.32, scroll_h * 0.75, inner_lyre_alpha)
    _draw_s_scroll(painter, top_cx + scroll_w * 0.15, margin + scroll_h * 0.38,
                   scroll_w * 0.32, scroll_h * 0.75, inner_lyre_alpha, flip_x=True)

    # Central vertical finial rising from lyre -- tall spire with pronounced spiral
    finial_pen = QPen(QColor(198, 183, 190, int(alpha_base * 0.9)), 1.6)
    finial_pen.setCapStyle(Qt.PenCapStyle.RoundCap)
    painter.setPen(finial_pen)
    painter.setBrush(Qt.BrushStyle.NoBrush)
    spire_h = 30
    p = QPainterPath()
    p.moveTo(top_cx, margin)
    p.cubicTo(top_cx - 5, margin - spire_h * 0.35,
              top_cx + 5, margin - spire_h * 0.7,
              top_cx, margin - spire_h)
    painter.drawPath(p)
    _draw_spiral_rosette(painter, top_cx, margin - spire_h, 6, alpha_base * 0.8)

    # Flanking finials -- progressively shorter toward edges
    for offset, fin_h in [(-scroll_w * 0.18, 22), (scroll_w * 0.18, 22),
                           (-scroll_w * 0.35, 16), (scroll_w * 0.35, 16),
                           (-scroll_w * 0.5, 10), (scroll_w * 0.5, 10)]:
        x = top_cx + offset
        fp = QPainterPath()
        fp.moveTo(x, margin)
        fp.cubicTo(x - 3, margin - fin_h * 0.4,
                   x + 3, margin - fin_h * 0.75,
                   x, margin - fin_h)
        fin_alpha = alpha_base * 0.7 if abs(offset) < scroll_w * 0.3 else alpha_base * 0.5
        thinner_pen = QPen(QColor(198, 183, 190, int(fin_alpha)), 1.1)
        thinner_pen.setCapStyle(Qt.PenCapStyle.RoundCap)
        painter.setPen(thinner_pen)
        painter.drawPath(fp)
        _draw_spiral_rosette(painter, x, margin - fin_h, 4, fin_alpha * 0.7)

    # ── Layer 2b: Bottom center lyre with hanging drops ──────────────────
    bot_lyre_alpha = int(alpha_base * 0.85)
    _draw_s_scroll(painter, top_cx - scroll_w * 0.28, height - margin - scroll_h * 0.42,
                   scroll_w * 0.55, scroll_h * 0.95, bot_lyre_alpha, flip_y=True)
    _draw_s_scroll(painter, top_cx + scroll_w * 0.28, height - margin - scroll_h * 0.42,
                   scroll_w * 0.55, scroll_h * 0.95, bot_lyre_alpha, flip_x=True, flip_y=True)
    # Inner bottom lyre pair
    _draw_s_scroll(painter, top_cx - scroll_w * 0.14, height - margin - scroll_h * 0.35,
                   scroll_w * 0.3, scroll_h * 0.7, int(alpha_base * 0.5), flip_y=True)
    _draw_s_scroll(painter, top_cx + scroll_w * 0.14, height - margin - scroll_h * 0.35,
                   scroll_w * 0.3, scroll_h * 0.7, int(alpha_base * 0.5), flip_x=True, flip_y=True)

    # Hanging drops from bottom
    drop_pen = QPen(QColor(198, 183, 190, int(alpha_base * 0.65)), 1.2)
    drop_pen.setCapStyle(Qt.PenCapStyle.RoundCap)
    painter.setPen(drop_pen)
    for offset, dh in [(0, 20), (-scroll_w * 0.2, 14), (scroll_w * 0.2, 14),
                        (-scroll_w * 0.38, 8), (scroll_w * 0.38, 8)]:
        x = top_cx + offset
        dp = QPainterPath()
        dp.moveTo(x, height - margin)
        dp.cubicTo(x - 2, height - margin + dh * 0.35,
                   x + 2, height - margin + dh * 0.65,
                   x, height - margin + dh)
        painter.drawPath(dp)
        _draw_spiral_rosette(painter, x, height - margin + dh, 3, alpha_base * 0.45)

    # ── Layer 3: Elaborate corner scrollwork ─────────────────────────────
    cs = min(width, height) * 0.18  # Corner scroll reach
    corners = [
        (margin, margin, 1, 1),
        (width - margin, margin, -1, 1),
        (margin, height - margin, 1, -1),
        (width - margin, height - margin, -1, -1),
    ]
    for cx, cy, sx, sy in corners:
        # Primary flowing C-scroll from one edge to the other
        c_pen = QPen(QColor(198, 183, 190, int(alpha_base * 0.8)), 1.5)
        c_pen.setCapStyle(Qt.PenCapStyle.RoundCap)
        painter.setPen(c_pen)
        painter.setBrush(Qt.BrushStyle.NoBrush)

        # Main arc curving from horizontal to vertical
        p1 = QPainterPath()
        p1.moveTo(cx + sx * cs, cy)
        p1.cubicTo(cx + sx * cs * 0.7, cy + sy * cs * 0.05,
                   cx + sx * cs * 0.3, cy + sy * cs * 0.4,
                   cx + sx * cs * 0.15, cy + sy * cs * 0.7)
        p1.cubicTo(cx + sx * cs * 0.1, cy + sy * cs * 0.85,
                   cx + sx * cs * 0.05, cy + sy * cs * 0.95,
                   cx, cy + sy * cs)
        painter.drawPath(p1)

        # Secondary inner C-scroll (tighter)
        c2_pen = QPen(QColor(198, 183, 190, int(alpha_base * 0.55)), 1.0)
        c2_pen.setCapStyle(Qt.PenCapStyle.RoundCap)
        painter.setPen(c2_pen)
        p2 = QPainterPath()
        p2.moveTo(cx + sx * cs * 0.7, cy)
        p2.cubicTo(cx + sx * cs * 0.5, cy + sy * cs * 0.1,
                   cx + sx * cs * 0.25, cy + sy * cs * 0.35,
                   cx + sx * cs * 0.12, cy + sy * cs * 0.55)
        painter.drawPath(p2)

        # Tight spiral curl at the inner terminus
        p3 = QPainterPath()
        p3.moveTo(cx + sx * cs * 0.12, cy + sy * cs * 0.55)
        p3.cubicTo(cx + sx * cs * 0.18, cy + sy * cs * 0.5,
                   cx + sx * cs * 0.22, cy + sy * cs * 0.42,
                   cx + sx * cs * 0.18, cy + sy * cs * 0.38)
        p3.cubicTo(cx + sx * cs * 0.14, cy + sy * cs * 0.35,
                   cx + sx * cs * 0.1, cy + sy * cs * 0.4,
                   cx + sx * cs * 0.12, cy + sy * cs * 0.45)
        painter.drawPath(p3)

        # Third inner curl -- tightest, for depth
        c3_pen = QPen(QColor(198, 183, 190, int(alpha_base * 0.35)), 0.7)
        c3_pen.setCapStyle(Qt.PenCapStyle.RoundCap)
        painter.setPen(c3_pen)
        p4 = QPainterPath()
        p4.moveTo(cx + sx * cs * 0.45, cy + sy * cs * 0.05)
        p4.cubicTo(cx + sx * cs * 0.3, cy + sy * cs * 0.15,
                   cx + sx * cs * 0.18, cy + sy * cs * 0.28,
                   cx + sx * cs * 0.12, cy + sy * cs * 0.38)
        painter.drawPath(p4)

        # Rosettes at key points
        _draw_spiral_rosette(painter, cx + sx * cs * 0.12, cy + sy * cs * 0.55,
                             5.5, alpha_base * 0.65)
        _draw_spiral_rosette(painter, cx + sx * cs * 0.5, cy + sy * cs * 0.05,
                             4, alpha_base * 0.45)
        _draw_spiral_rosette(painter, cx + sx * cs * 0.8, cy + sy * 1,
                             3, alpha_base * 0.35)

        # Branching vine from corner diagonal
        vine_angle = math.atan2(sy, sx) + math.pi / 4
        _draw_branching_vine(painter, cx + sx * cs * 0.15, cy + sy * cs * 0.15,
                             vine_angle, cs * 0.4, 3, int(alpha_base * 0.45),
                             branch_angle_deg=28, length_decay=0.55, max_depth=3)

    # ── Layer 4: Wing venation on left and right sides ───────────────────
    vine_alpha = int(alpha_base * 0.55)
    vine_length = min(height * 0.16, 55)
    vine_depth = 5

    # Left side - wing-like branching patterns
    left_x = inner_m + 2
    num_vines = 6
    for i in range(num_vines):
        frac = 0.18 + 0.64 * i / max(1, num_vines - 1)
        vy = height * frac
        # Alternate slight up/down angle for organic feel
        angle = -0.25 + 0.1 * math.sin(i * 1.5)
        _draw_branching_vine(painter, left_x, vy, angle, vine_length,
                             vine_depth, vine_alpha, branch_angle_deg=25,
                             length_decay=0.58, max_depth=vine_depth)
        _draw_spiral_rosette(painter, left_x - 1, vy, 3, vine_alpha * 0.7)

    # Right side - mirrored wing venation
    right_x = width - inner_m - 2
    for i in range(num_vines):
        frac = 0.18 + 0.64 * i / max(1, num_vines - 1)
        vy = height * frac
        angle = math.pi + 0.25 - 0.1 * math.sin(i * 1.5)
        _draw_branching_vine(painter, right_x, vy, angle, vine_length,
                             vine_depth, vine_alpha, branch_angle_deg=25,
                             length_decay=0.58, max_depth=vine_depth)
        _draw_spiral_rosette(painter, right_x + 1, vy, 3, vine_alpha * 0.7)

    # ── Layer 5: Mid-height side scrollwork ──────────────────────────────
    mid_y = height / 2
    side_scroll_w = min(width * 0.1, 40)
    side_scroll_h = min(height * 0.08, 28)
    side_alpha = int(alpha_base * 0.6)

    # Left mid S-scroll pair
    _draw_s_scroll(painter, inner_m + side_scroll_w * 0.5, mid_y,
                   side_scroll_w, side_scroll_h, side_alpha)
    # Right mid S-scroll pair (mirrored)
    _draw_s_scroll(painter, width - inner_m - side_scroll_w * 0.5, mid_y,
                   side_scroll_w, side_scroll_h, side_alpha, flip_x=True)

    # Quarter-height side scrolls
    for y_frac in [0.3, 0.7]:
        y = height * y_frac
        sm_w = side_scroll_w * 0.7
        sm_h = side_scroll_h * 0.6
        sm_alpha = int(alpha_base * 0.4)
        _draw_s_scroll(painter, inner_m + sm_w * 0.4, y,
                       sm_w, sm_h, sm_alpha)
        _draw_s_scroll(painter, width - inner_m - sm_w * 0.4, y,
                       sm_w, sm_h, sm_alpha, flip_x=True)

    # ── Layer 6: Fine horizontal accent bars ─────────────────────────────
    fine_pen = QPen(QColor(198, 183, 190, int(alpha_base * 0.25)), 0.6)
    fine_pen.setCapStyle(Qt.PenCapStyle.RoundCap)
    painter.setPen(fine_pen)
    painter.setBrush(Qt.BrushStyle.NoBrush)

    # Decorative horizontal bars connecting top/bottom scrollwork to corners
    for y in [margin + scroll_h + 5, height - margin - scroll_h - 5]:
        bar_inset = width * 0.12
        painter.drawLine(QPointF(bar_inset, y), QPointF(width - bar_inset, y))
        # Rosettes at endpoints
        _draw_spiral_rosette(painter, bar_inset, y, 2.5, alpha_base * 0.3)
        _draw_spiral_rosette(painter, width - bar_inset, y, 2.5, alpha_base * 0.3)
        # Mid rosette
        _draw_spiral_rosette(painter, width / 2, y, 3, alpha_base * 0.35)

    # ── Layer 7: Wing venation along top and bottom edges ──────────────
    top_vine_alpha = int(alpha_base * 0.4)
    top_vine_len = min(height * 0.1, 38)
    # Top edge: denser branching pointing downward
    for i in range(7):
        vx = width * (0.15 + 0.7 * i / 6)
        _draw_branching_vine(painter, vx, inner_m + 2,
                             math.pi / 2 + 0.12 * (i - 3),
                             top_vine_len, 4, top_vine_alpha,
                             branch_angle_deg=28, length_decay=0.55, max_depth=4)

    # Bottom edge: denser branching pointing upward
    for i in range(7):
        vx = width * (0.15 + 0.7 * i / 6)
        _draw_branching_vine(painter, vx, height - inner_m - 2,
                             -math.pi / 2 + 0.12 * (i - 3),
                             top_vine_len, 4, top_vine_alpha,
                             branch_angle_deg=28, length_decay=0.55, max_depth=4)

    # ── Layer 8: Faint interior filigree arcs (wing membrane suggestion) ──
    # Very subtle arcing curves in the interior, suggesting wing membrane
    membrane_alpha = int(alpha_base * 0.18)
    membrane_pen = QPen(QColor(198, 183, 190, membrane_alpha), 0.5)
    membrane_pen.setCapStyle(Qt.PenCapStyle.RoundCap)
    painter.setPen(membrane_pen)
    painter.setBrush(Qt.BrushStyle.NoBrush)

    # Sweeping arcs from corners toward center (wing membrane)
    for sx_sign, sy_sign in [(1, 1), (-1, 1), (1, -1), (-1, -1)]:
        base_x = width / 2 + sx_sign * width * 0.35
        base_y = height / 2 + sy_sign * height * 0.35
        for arc_i in range(4):
            arc_frac = 0.3 + arc_i * 0.18
            arc = QPainterPath()
            arc.moveTo(base_x, base_y - sy_sign * height * arc_frac * 0.3)
            arc.cubicTo(
                base_x - sx_sign * width * arc_frac * 0.15,
                base_y - sy_sign * height * arc_frac * 0.15,
                base_x - sx_sign * width * arc_frac * 0.3,
                base_y + sy_sign * height * arc_frac * 0.1,
                base_x - sx_sign * width * arc_frac * 0.15,
                base_y + sy_sign * height * arc_frac * 0.25,
            )
            painter.drawPath(arc)

    # ── Layer 9: Connecting arcs (wrought iron gate top rail) ────────────
    # Graceful arcs connecting top corners through the top center lyre
    arc_pen = QPen(QColor(198, 183, 190, int(alpha_base * 0.3)), 0.7)
    arc_pen.setCapStyle(Qt.PenCapStyle.RoundCap)
    painter.setPen(arc_pen)
    painter.setBrush(Qt.BrushStyle.NoBrush)

    # Top sweeping arc from left corner scrollwork to right
    top_arc = QPainterPath()
    top_arc.moveTo(margin + cs * 0.5, margin + 3)
    top_arc.cubicTo(width * 0.3, margin + scroll_h * 0.6,
                    width * 0.7, margin + scroll_h * 0.6,
                    width - margin - cs * 0.5, margin + 3)
    painter.drawPath(top_arc)

    # Bottom sweeping arc
    bot_arc = QPainterPath()
    bot_arc.moveTo(margin + cs * 0.5, height - margin - 3)
    bot_arc.cubicTo(width * 0.3, height - margin - scroll_h * 0.5,
                    width * 0.7, height - margin - scroll_h * 0.5,
                    width - margin - cs * 0.5, height - margin - 3)
    painter.drawPath(bot_arc)

    # ── Layer 10: Center diamond motif ───────────────────────────────────
    # A subtle diamond/lozenge shape at the very center -- like a keystone
    diamond_alpha = int(alpha_base * 0.2)
    diamond_pen = QPen(QColor(198, 183, 190, diamond_alpha), 0.6)
    diamond_pen.setCapStyle(Qt.PenCapStyle.RoundCap)
    painter.setPen(diamond_pen)

    center_x = width / 2
    center_y = height / 2
    dw = min(width * 0.06, 25)
    dh = min(height * 0.06, 20)
    diamond = QPainterPath()
    diamond.moveTo(center_x, center_y - dh)
    diamond.lineTo(center_x + dw, center_y)
    diamond.lineTo(center_x, center_y + dh)
    diamond.lineTo(center_x - dw, center_y)
    diamond.closeSubpath()
    painter.drawPath(diamond)

    # Rosette at diamond center
    _draw_spiral_rosette(painter, center_x, center_y, 4, diamond_alpha * 1.2)


# ── Style class ──────────────────────────────────────────────────────────────

class FiligreeIronStyle(BaseStyle):
    """Wrought iron filigree and insect wing venation on void black.

    Command, specific. PyQt6 theme inspired by Hollow Knight's ornate ironwork,
    gothic cathedral gates, and butterfly wing patterns.
    """

    name = "filigree_iron"
    font = "Palatino"

    # Mauve accent on void black
    accent = _MAUVE_Q
    accent_css = MAUVE
    text_primary = OFF_WHITE
    text_secondary = MAUVE
    text_muted = SLATE_MID
    text_error = "rgb(200, 85, 95)"
    text_link = MAUVE
    border_color = SLATE_MID
    border_dark = SLATE_DARK
    icon_color_dark = '#565a75'
    icon_color_light = '#fafbf6'
    icon_color_muted = '#8a8698'

    # Input fields
    input_bg = '#0f0f1b'
    input_text = '#fafbf6'

    # Slider
    slider_groove = "rgba(15,15,27,0.85)"
    slider_handle = MAUVE
    slider_fill = SLATE_MID

    # Rotary knob - dark iron
    knob_style = "industrial"
    knob_body_dark = "#1a1a2e"
    knob_body_light = "#373a4b"
    knob_notch_style = "needle"
    knob_tickmarks = True
    knob_glow = False
    knob_track_color = "#c6b7be"
    knob_label_color = "#fafbf6"

    # Waveform - mauve
    waveform_color = _MAUVE_Q
    waveform_glow = True
    waveform_center_line = QColor(198, 183, 190, 40)
    waveform_panel = "dark"

    # Timer
    timer_use_lcd = True
    timer_color = _MAUVE_Q

    # Transcription
    transcription_text = OFF_WHITE
    transcription_text_dimmed = SLATE_MID
    transcription_panel_bg = "rgba(15, 15, 27, 128)"  # 50% transparent so filigree shows through
    transcription_panel_border = "rgba(10, 10, 20, 160)"
    transcription_row_hover = "rgba(198, 183, 190, 0.08)"
    transcription_row_btn_bg = "rgba(198, 183, 190, 0.10)"
    transcription_row_btn_hover = "rgba(198, 183, 190, 0.18)"
    transcription_row_btn_pressed = "rgba(198, 183, 190, 0.30)"

    # Chime editor
    chime_grid_bg = QColor(18, 18, 30)
    chime_grid_line = QColor(40, 40, 55)
    chime_cell_inactive = QColor(28, 28, 42)
    chime_cell_active = _MAUVE_Q
    chime_cell_highlight = QColor(198, 183, 190, 70)
    chime_piano_white = QColor(240, 238, 230)
    chime_piano_black = QColor(20, 20, 32)
    chime_piano_label_white = QColor(55, 55, 70)
    chime_piano_label_black = QColor(190, 180, 185)

    def button_css(self):
        """Command, specific. CSS for buttons: void-dark with slate/mauve borders."""
        return (
            # Normal
            f"QPushButton {{ color: {SLATE_MID}; "
            f"background: qlineargradient(x1:0, y1:0, x2:0, y2:1, "
            f"stop:0 rgb(26, 26, 46), stop:0.08 rgb(20, 20, 35), "
            f"stop:0.92 {VOID_BLACK}, stop:1 rgb(10, 10, 20)); "
            f"border: 1px solid {SLATE_DARK}; border-top-color: {SLATE_MID}; "
            f"border-radius: 5px; padding: 3px 8px; font-size: 11px; "
            f"font-family: {self.font}; text-align: left; }}"
            # Hover - mauve border
            f"QPushButton:hover {{ color: {OFF_WHITE}; "
            f"background: qlineargradient(x1:0, y1:0, x2:0, y2:1, "
            f"stop:0 rgb(32, 32, 55), stop:0.08 rgb(26, 26, 46), "
            f"stop:0.92 {VOID_DEEP}, stop:1 {VOID_BLACK}); "
            f"border: 1px solid {MAUVE}; border-top-color: {MAUVE}; }}"
            # Pressed
            f"QPushButton:pressed {{ color: {MAUVE}; "
            f"background: qlineargradient(x1:0, y1:0, x2:0, y2:1, "
            f"stop:0 {VOID_BLACK}, stop:0.08 {VOID_DEEP}, "
            f"stop:0.92 rgb(26, 26, 46), stop:1 {VOID_DEEP}); "
            f"border: 1px solid {SLATE_DARK}; }}"
            # Disabled
            f"QPushButton:disabled {{ color: {SLATE_DARK}; "
            f"background: {VOID_BLACK}; border: 1px solid rgb(35, 35, 50); }}"
            # Checked - deep purple tint
            f"QPushButton:checked {{ color: {OFF_WHITE}; "
            f"background: qlineargradient(x1:0, y1:0, x2:0, y2:1, "
            f"stop:0 rgb(55, 20, 85), stop:0.08 rgb(45, 0, 78), "
            f"stop:0.92 rgb(30, 0, 55), stop:1 rgb(22, 0, 42)); "
            f"border: 1px solid {SLATE_MID}; }}"
            f"QPushButton:checked:hover {{ "
            f"background: qlineargradient(x1:0, y1:0, x2:0, y2:1, "
            f"stop:0 rgb(65, 25, 100), stop:0.08 rgb(55, 10, 88), "
            f"stop:0.92 rgb(40, 0, 68), stop:1 rgb(30, 0, 55)); }}"
        )

    def menu_css(self):
        """Command, specific. CSS for context menus."""
        return (
            f"QMenu {{ background: {VOID_BLACK}; color: {OFF_WHITE}; "
            f"border: 2px solid {SLATE_DARK}; border-radius: 4px; padding: 4px; "
            f"font-family: {self.font}; font-size: 11px; }}"
            "QMenu::item { padding: 4px 16px; border-radius: 2px; }"
            f"QMenu::item:selected {{ color: {OFF_WHITE}; "
            f"background: qlineargradient(x1:0, y1:0, x2:0, y2:1, "
            f"stop:0 {DEEP_PURPLE}, stop:0.5 rgb(35, 0, 60), stop:1 rgb(25, 0, 45)); }}"
            f"QMenu::separator {{ height: 2px; background: {SLATE_DARK}; margin: 4px 8px; }}"
        )

    def _scrollbar_vertical_css(self):
        """Command, specific. Dark void scrollbar with mauve handle."""
        return (
            f"QScrollBar:vertical {{ width: 14px; background: {VOID_BLACK}; "
            f"border: 1px solid rgb(25, 25, 40); border-radius: 5px; margin: 0px; }}"
            "QScrollBar::handle:vertical { "
            "background: qlineargradient(x1:0, y1:0, x2:1, y2:0, "
            f"stop:0.0 {SLATE_DARK}, stop:0.2 {SLATE_MID}, "
            f"stop:0.5 rgb(100, 104, 130), stop:0.8 {SLATE_MID}, stop:1.0 {SLATE_DARK}); "
            f"border: 1px solid {SLATE_DARK}; border-radius: 4px; min-height: 40px; margin: 2px; }}"
            "QScrollBar::handle:vertical:hover { "
            "background: qlineargradient(x1:0, y1:0, x2:1, y2:0, "
            f"stop:0.0 {SLATE_MID}, stop:0.5 {MAUVE}, stop:1.0 {SLATE_MID}); "
            f"border: 1px solid {SLATE_MID}; }}"
            "QScrollBar::handle:vertical:pressed { "
            "background: qlineargradient(x1:0, y1:0, x2:1, y2:0, "
            f"stop:0.0 {SLATE_DARK}, stop:0.5 {SLATE_MID}, stop:1.0 {SLATE_DARK}); "
            f"border: 1px solid {SLATE_DARK}; }}"
            "QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical { "
            "height: 0; width: 0; background: none; border: none; }"
            "QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical { background: transparent; }"
        )

    def panel_bg_css(self):
        """Command, specific. CSS for panel backgrounds — 50% transparent."""
        return (
            f"background: qlineargradient(x1:0, y1:0, x2:0, y2:1, "
            f"stop:0 rgba(26, 26, 46, 128), stop:0.02 rgba(20, 20, 35, 128), "
            f"stop:0.98 rgba(15, 15, 27, 128), stop:1 rgba(10, 10, 20, 128)); "
            f"border: 1px solid {SLATE_DARK}; border-radius: 4px;"
        )

    def panel_bg_flat_css(self):
        """Command, specific. CSS for flat panel backgrounds — 50% transparent."""
        return (
            f"background: rgba(15, 15, 27, 128); border: 1px solid rgba(25, 25, 40, 160); border-radius: 4px;"
        )

    def paint_window(self, painter, rect, width, height, focused=True):
        """
        Command, specific. Paint void-black window with ornate wrought iron filigree.

        Draws a deep void-black gradient background, then overlays a vignette
        for depth, a faint purple glow when focused, and the elaborate ornamental
        iron frame with S-scrolls, branching vines, and spiral rosettes.

        Args:
            painter: QPainter (with antialiasing enabled by caller)
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

        # ── Background: void-black gradient ──────────────────────────────
        bg_grad = QLinearGradient(0, 0, 0, height)
        bg_grad.setColorAt(0, QColor(20, 20, 38))
        bg_grad.setColorAt(0.15, QColor(15, 15, 27))
        bg_grad.setColorAt(0.85, QColor(12, 12, 22))
        bg_grad.setColorAt(1, QColor(18, 18, 32))
        painter.setBrush(QBrush(bg_grad))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawRoundedRect(rect, radius, radius)

        # ── Vignette: dark edges ─────────────────────────────────────────
        for horizontal in [True, False]:
            grad = QLinearGradient(0, 0, width if horizontal else 0, 0 if horizontal else height)
            for pos, alpha in [(0, 140), (0.08, 70), (0.2, 20), (0.8, 20), (0.92, 70), (1, 140)]:
                grad.setColorAt(pos, QColor(5, 5, 12, alpha))
            painter.setBrush(QBrush(grad))
            painter.setPen(Qt.PenStyle.NoPen)
            painter.drawRoundedRect(rect, radius, radius)

        # ── Focused purple glow ──────────────────────────────────────────
        if focused:
            # Top edge glow
            top_glow = QLinearGradient(0, 0, 0, 60)
            top_glow.setColorAt(0, QColor(45, 0, 78, 20))
            top_glow.setColorAt(1, QColor(45, 0, 78, 0))
            painter.setBrush(QBrush(top_glow))
            painter.setPen(Qt.PenStyle.NoPen)
            painter.drawRoundedRect(QRectF(rect.x(), rect.y(), width, 60), radius, radius)

            # Bottom edge glow
            bot_glow = QLinearGradient(0, height - 40, 0, height)
            bot_glow.setColorAt(0, QColor(45, 0, 78, 0))
            bot_glow.setColorAt(1, QColor(45, 0, 78, 15))
            painter.setBrush(QBrush(bot_glow))
            painter.drawRoundedRect(QRectF(rect.x(), rect.y() + height - 40, width, 40), radius, radius)

            # Center radial glow (very subtle)
            center_glow = QRadialGradient(width / 2, height / 2, max(width, height) * 0.5)
            center_glow.setColorAt(0, QColor(45, 0, 78, 12))
            center_glow.setColorAt(0.5, QColor(45, 0, 78, 6))
            center_glow.setColorAt(1, QColor(45, 0, 78, 0))
            painter.setBrush(QBrush(center_glow))
            painter.drawRoundedRect(rect, radius, radius)

        # Remove clip so ornamental elements extend BEYOND window edges
        painter.setClipping(False)

        # ── Ornate wrought iron frame (unclipped — spirals/finials extend beyond!) ──
        _draw_ornate_frame(painter, width, height, focused)

        # ── Border line ──────────────────────────────────────────────────
        painter.setBrush(Qt.BrushStyle.NoBrush)
        if focused:
            painter.setPen(QPen(QColor(198, 183, 190, 90), 1.2))
        else:
            painter.setPen(QPen(QColor(86, 90, 117, 60), 0.8))
        painter.drawRoundedRect(rect, radius, radius)

    def paint_waveform_panel(self, painter, rect, w, h, cy):
        """
        Command, specific. Waveform panel: dark recessed void with mauve border.

        Args:
            painter: QPainter
            rect (QRectF): Panel rectangle
            w (int): Panel width
            h (int): Panel height
            cy (float): Center y for the waveform center line
        """
        # Dark recessed background
        panel_grad = QLinearGradient(0, 0, 0, h)
        panel_grad.setColorAt(0, QColor(12, 12, 22))
        panel_grad.setColorAt(0.3, QColor(16, 16, 28))
        panel_grad.setColorAt(0.7, QColor(14, 14, 25))
        panel_grad.setColorAt(1, QColor(10, 10, 18))
        painter.setBrush(QBrush(panel_grad))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawRoundedRect(rect, 6, 6)

        # Subtle purple glow from top
        top_glow = QLinearGradient(0, 0, 0, h * 0.2)
        top_glow.setColorAt(0, QColor(45, 0, 78, 15))
        top_glow.setColorAt(1, QColor(45, 0, 78, 0))
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

        # Border - mauve edge
        painter.setBrush(Qt.BrushStyle.NoBrush)
        painter.setPen(QPen(QColor(86, 90, 117, 160), 1.2))
        painter.drawRoundedRect(rect, 6, 6)

        # Center line
        painter.setPen(QPen(QColor(198, 183, 190, 40), 1))
        painter.drawLine(0, int(cy), w, int(cy))
