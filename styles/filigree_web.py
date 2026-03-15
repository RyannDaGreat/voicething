"""Filigree style - dreamcatcher web patterns, Hollow Knight-inspired ethereal void aesthetic."""

import math
import numpy as np
from PyQt6.QtCore import Qt, QRectF, QPointF
from PyQt6.QtGui import (
    QColor, QLinearGradient, QRadialGradient, QBrush, QImage, QPixmap,
    QPainterPath, QPen
)

from .base import BaseStyle, get_cached_texture


# Void / deep dark backgrounds
VOID_BLACK = "rgb(15, 15, 27)"
VOID_DEEP = "rgb(20, 20, 35)"
SLATE_DARK = "rgb(55, 58, 75)"
SLATE_MID = "rgb(86, 90, 117)"

# Accent / ornament
MAUVE = "rgb(198, 183, 190)"
OFF_WHITE = "rgb(250, 251, 246)"
DEEP_PURPLE = "rgb(45, 0, 78)"

# Text colors
TEXT_MAUVE = "rgb(198, 183, 190)"
TEXT_OFF_WHITE = "rgb(250, 251, 246)"
TEXT_SLATE = "rgb(130, 133, 155)"
TEXT_MUTED = "rgb(86, 90, 117)"
TEXT_DISABLED = "rgb(50, 52, 65)"

# Borders
BORDER_VOID = "rgb(12, 12, 22)"
BORDER_DARK = "rgb(30, 30, 48)"
BORDER_MID = "rgb(55, 58, 75)"
BORDER_LIGHT = "rgb(86, 90, 117)"


class FiligreeWebStyle(BaseStyle):
    name = "filigree_web"
    font = "Palatino"

    _texture_cache = None

    accent = QColor(198, 183, 190)
    accent_css = "rgb(198,183,190)"
    text_primary = TEXT_OFF_WHITE
    text_secondary = TEXT_MAUVE
    text_muted = TEXT_SLATE
    text_error = "rgb(220, 80, 90)"
    text_link = MAUVE
    border_color = BORDER_MID
    border_dark = BORDER_DARK
    icon_color_dark = '#373a4b'
    icon_color_light = '#fafbf6'
    icon_color_muted = '#565a75'

    input_bg = '#14141f'
    input_text = '#fafbf6'

    slider_groove = "rgba(15,15,27,0.85)"
    slider_handle = "rgb(198,183,190)"
    slider_fill = "rgb(150,140,155)"

    knob_style = "vintage"
    knob_body_dark = "#2d2d40"
    knob_body_light = "#565a75"
    knob_notch_style = "needle"
    knob_tickmarks = True
    knob_glow = False
    knob_track_color = "#c6b7be"
    knob_label_color = "#fafbf6"

    waveform_color = QColor(198, 183, 190)
    waveform_glow = True
    waveform_glow_radius = 14
    waveform_glow_alpha = 120
    waveform_center_line = QColor(198, 183, 190, 40)
    waveform_panel = "dark"

    timer_use_lcd = True
    timer_color = QColor(198, 183, 190)

    transcription_text = TEXT_OFF_WHITE
    transcription_text_dimmed = TEXT_SLATE
    transcription_panel_bg = "rgba(15, 15, 27, 128)"
    transcription_panel_border = "rgba(12, 12, 22, 160)"
    transcription_row_hover = "rgba(198, 183, 190, 0.08)"
    transcription_row_btn_bg = "rgba(198, 183, 190, 0.10)"
    transcription_row_btn_hover = "rgba(198, 183, 190, 0.18)"
    transcription_row_btn_pressed = "rgba(198, 183, 190, 0.32)"

    chime_grid_bg = QColor(18, 18, 30)
    chime_grid_line = QColor(40, 40, 58)
    chime_cell_inactive = QColor(28, 28, 42)
    chime_cell_active = QColor(198, 183, 190)
    chime_cell_highlight = QColor(198, 183, 190, 70)
    chime_piano_white = QColor(240, 238, 232)
    chime_piano_black = QColor(20, 20, 32)
    chime_piano_label_white = QColor(55, 58, 75)
    chime_piano_label_black = QColor(198, 183, 190)

    def button_css(self):
        return (
            # Normal - void background, thin slate border
            f"QPushButton {{ color: {TEXT_MAUVE}; "
            f"background: qlineargradient(x1:0, y1:0, x2:0, y2:1, "
            f"stop:0 rgb(35, 35, 52), stop:0.08 rgb(25, 25, 40), "
            f"stop:0.92 rgb(18, 18, 30), stop:1 rgb(12, 12, 22)); "
            f"border: 1px solid {BORDER_MID}; "
            f"border-radius: 3px; padding: 3px 8px; font-size: 11px; "
            f"font-family: {self.font}; text-align: left; }}"
            # Hover - mauve border, off-white text
            f"QPushButton:hover {{ color: {TEXT_OFF_WHITE}; "
            f"background: qlineargradient(x1:0, y1:0, x2:0, y2:1, "
            f"stop:0 rgb(45, 45, 65), stop:0.08 rgb(35, 35, 52), "
            f"stop:0.92 rgb(25, 25, 40), stop:1 rgb(18, 18, 30)); "
            f"border: 1px solid {MAUVE}; }}"
            # Pressed
            f"QPushButton:pressed {{ color: {TEXT_OFF_WHITE}; "
            f"background: qlineargradient(x1:0, y1:0, x2:0, y2:1, "
            f"stop:0 rgb(18, 18, 30), stop:0.08 rgb(25, 25, 40), "
            f"stop:0.92 rgb(35, 35, 52), stop:1 rgb(25, 25, 40)); "
            f"border: 1px solid {BORDER_DARK}; }}"
            # Disabled
            f"QPushButton:disabled {{ color: {TEXT_DISABLED}; "
            f"background: {VOID_BLACK}; border: 1px solid {BORDER_DARK}; }}"
            # Checked - mauve highlight
            f"QPushButton:checked {{ color: {TEXT_OFF_WHITE}; "
            f"background: qlineargradient(x1:0, y1:0, x2:0, y2:1, "
            f"stop:0 rgb(120, 110, 118), stop:0.08 rgb(100, 92, 98), "
            f"stop:0.92 rgb(70, 64, 70), stop:1 rgb(50, 45, 52)); "
            f"border: 1px solid {MAUVE}; }}"
            f"QPushButton:checked:hover {{ "
            f"background: qlineargradient(x1:0, y1:0, x2:0, y2:1, "
            f"stop:0 rgb(140, 130, 138), stop:0.08 rgb(120, 110, 118), "
            f"stop:0.92 rgb(86, 78, 85), stop:1 rgb(60, 55, 62)); }}"
        )

    def menu_css(self):
        return (
            f"QMenu {{ background: {VOID_BLACK}; color: {TEXT_OFF_WHITE}; "
            f"border: 2px solid {BORDER_MID}; border-radius: 4px; padding: 4px; "
            f"font-family: {self.font}; font-size: 11px; }}"
            "QMenu::item { padding: 4px 16px; border-radius: 2px; }"
            f"QMenu::item:selected {{ color: {TEXT_OFF_WHITE}; "
            f"background: qlineargradient(x1:0, y1:0, x2:0, y2:1, "
            f"stop:0 rgb(100, 92, 98), stop:0.5 rgb(70, 64, 70), stop:1 rgb(50, 45, 52)); }}"
            f"QMenu::separator {{ height: 2px; background: {BORDER_MID}; margin: 4px 8px; }}"
        )

    def _scrollbar_vertical_css(self):
        return (
            f"QScrollBar:vertical {{ width: 14px; background: {VOID_BLACK}; "
            f"border: 1px solid {BORDER_DARK}; border-radius: 5px; margin: 0px; }}"
            "QScrollBar::handle:vertical { "
            "background: qlineargradient(x1:0, y1:0, x2:1, y2:0, "
            f"stop:0.0 rgb(40, 40, 58), stop:0.2 rgb(55, 58, 75), "
            f"stop:0.5 rgb(70, 72, 90), stop:0.8 rgb(55, 58, 75), stop:1.0 rgb(40, 40, 58)); "
            f"border: 1px solid {BORDER_MID}; border-radius: 4px; min-height: 40px; margin: 2px; }}"
            "QScrollBar::handle:vertical:hover { "
            "background: qlineargradient(x1:0, y1:0, x2:1, y2:0, "
            f"stop:0.0 rgb(55, 58, 75), stop:0.2 rgb(70, 72, 90), "
            f"stop:0.5 rgb(86, 90, 117), stop:0.8 rgb(70, 72, 90), stop:1.0 rgb(55, 58, 75)); "
            f"border: 1px solid {BORDER_LIGHT}; }}"
            "QScrollBar::handle:vertical:pressed { "
            "background: qlineargradient(x1:0, y1:0, x2:1, y2:0, "
            f"stop:0.0 rgb(30, 30, 45), stop:0.2 rgb(40, 40, 58), "
            f"stop:0.5 rgb(55, 58, 75), stop:0.8 rgb(40, 40, 58), stop:1.0 rgb(30, 30, 45)); "
            f"border: 1px solid {BORDER_DARK}; }}"
            "QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical { "
            "height: 0; width: 0; background: none; border: none; }"
            "QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical { background: transparent; }"
        )

    def panel_bg_css(self):
        return (
            f"background: qlineargradient(x1:0, y1:0, x2:0, y2:1, "
            f"stop:0 rgba(35, 35, 52, 128), stop:0.02 rgba(25, 25, 40, 128), "
            f"stop:0.98 rgba(18, 18, 30, 128), stop:1 rgba(12, 12, 22, 128)); "
            f"border: 1px solid {BORDER_MID}; border-radius: 4px;"
        )

    def panel_bg_flat_css(self):
        return (
            f"background: rgba(15, 15, 27, 128); border: 1px solid {BORDER_DARK}; border-radius: 4px;"
        )

    def get_background_pixmap(self, height=512):
        """Generate void texture with faint particulate grain.

        Command, specific. Generates and caches a tileable dark texture.
        """
        if FiligreeWebStyle._texture_cache is not None:
            return FiligreeWebStyle._texture_cache

        width = 256
        FiligreeWebStyle._texture_cache = get_cached_texture(
            "filigree", width, height, lambda: self._generate_texture(width, height)
        )
        return FiligreeWebStyle._texture_cache

    def _generate_texture(self, width, height):
        """Generate dark void texture with subtle purple-tinted grain (seamlessly tileable).

        Command, specific. Creates a QPixmap with organic noise.
        """
        from scipy.ndimage import gaussian_filter

        np.random.seed(2017)  # Hollow Knight release year

        def seamless_fractal_noise(h, w, octaves=4, persistence=0.5):
            """Generate seamless tileable fractal noise.

            Pure function, general.

            Args:
                h (int): Height
                w (int): Width
                octaves (int): Number of noise octaves
                persistence (float): Amplitude falloff per octave

            Returns:
                np.ndarray: (h, w) float32, normalized 0-1

            Examples:
                >>> # seamless_fractal_noise(64, 64).shape == (64, 64)
            """
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

        img = np.zeros((height, width, 4), dtype=np.uint8)

        # Dark void base with slight purple tint
        base_r, base_g, base_b = 17, 17, 30

        grain_noise = seamless_fractal_noise(height, width, octaves=4, persistence=0.5)

        xs = np.arange(width)[None, :].astype(np.float64)
        ys = np.arange(height)[:, None].astype(np.float64)
        tau_x = 2 * math.pi * xs / width
        tau_y = 2 * math.pi * ys / height

        # Subtle interference pattern — very dark swirls
        swirl = (
            np.sin(tau_x * 2 + tau_y * 1) * 0.15
            + np.sin(tau_y * 3 - tau_x * 1 + 0.8) * 0.1
            + np.sin(tau_x * 1 + tau_y * 2) * 0.08
        )

        grain = 0.5 + swirl + grain_noise * 0.08
        variation = 0.8 + grain * 0.4

        img[:, :, 0] = np.clip(base_r * variation, 10, 30).astype(np.uint8)
        img[:, :, 1] = np.clip(base_g * variation, 10, 28).astype(np.uint8)
        img[:, :, 2] = np.clip(base_b * variation, 18, 45).astype(np.uint8)
        img[:, :, 3] = 255

        for c in range(3):
            img[:, :, c] = gaussian_filter(img[:, :, c].astype(float), sigma=1.0, mode='wrap').astype(np.uint8)

        qimg = QImage(img.data, width, height, width * 4, QImage.Format.Format_RGBA8888).copy()
        return QPixmap.fromImage(qimg)

    def _draw_dreamcatcher(self, painter, cx, cy, radius, spokes=12, rings=5, alpha=25):
        """Draw a dreamcatcher web pattern centered at (cx, cy).

        Command, specific. Draws radiating spokes with curved connecting
        threads forming concentric web rings, plus a spiral center.

        Args:
            painter: QPainter to draw on
            cx (float): Center x
            cy (float): Center y
            radius (float): Outer radius
            spokes (int): Number of radiating spokes
            rings (int): Number of concentric web rings
            alpha (int): Base opacity (0-255)
        """
        pen = QPen(QColor(198, 183, 190, alpha), 1.0)
        pen.setCapStyle(Qt.PenCapStyle.RoundCap)
        painter.setBrush(Qt.BrushStyle.NoBrush)

        # Draw spokes
        painter.setPen(pen)
        for i in range(spokes):
            angle = 2 * math.pi * i / spokes
            ex = cx + radius * math.cos(angle)
            ey = cy + radius * math.sin(angle)
            painter.drawLine(QPointF(cx, cy), QPointF(ex, ey))

        # Draw concentric web rings with curved connections between spokes
        for ring in range(1, rings + 1):
            r = radius * ring / rings
            # Alternate pulling inward/outward slightly for organic feel
            inward_factor = 0.82 + 0.04 * (ring % 3)
            path = QPainterPath()
            for i in range(spokes):
                angle1 = 2 * math.pi * i / spokes
                angle2 = 2 * math.pi * ((i + 1) % spokes) / spokes
                x1 = cx + r * math.cos(angle1)
                y1 = cy + r * math.sin(angle1)
                x2 = cx + r * math.cos(angle2)
                y2 = cy + r * math.sin(angle2)
                if i == 0:
                    path.moveTo(QPointF(x1, y1))
                mid_angle = (angle1 + angle2) / 2
                cr = r * inward_factor
                cx2 = cx + cr * math.cos(mid_angle)
                cy2 = cy + cr * math.sin(mid_angle)
                path.quadTo(QPointF(cx2, cy2), QPointF(x2, y2))

            # Slightly dimmer for inner rings, heavier for outer
            ring_alpha = max(10, alpha - (rings - ring) * 2)
            ring_pen = QPen(QColor(198, 183, 190, ring_alpha), 0.8)
            ring_pen.setCapStyle(Qt.PenCapStyle.RoundCap)
            painter.setPen(ring_pen)
            painter.drawPath(path)

        # Outer bounding circle
        outer_pen = QPen(QColor(198, 183, 190, alpha + 3), 1.0)
        outer_pen.setCapStyle(Qt.PenCapStyle.RoundCap)
        painter.setPen(outer_pen)
        painter.drawEllipse(QPointF(cx, cy), radius, radius)

        # Spiral center
        spiral_pen = QPen(QColor(198, 183, 190, alpha + 8), 0.6)
        spiral_pen.setCapStyle(Qt.PenCapStyle.RoundCap)
        painter.setPen(spiral_pen)
        spiral_turns = 3
        spiral_points = 60
        spiral_path = QPainterPath()
        spiral_max_r = radius * 0.15
        for i in range(spiral_points):
            t = i / spiral_points
            angle = t * spiral_turns * 2 * math.pi
            r = spiral_max_r * t
            sx = cx + r * math.cos(angle)
            sy = cy + r * math.sin(angle)
            if i == 0:
                spiral_path.moveTo(QPointF(sx, sy))
            else:
                spiral_path.lineTo(QPointF(sx, sy))
        painter.drawPath(spiral_path)

    def _draw_corner_webs(self, painter, width, height, alpha=20):
        """Draw quarter-circle dreamcatcher fragments at each corner.

        Command, specific. Each corner gets a partial web as if a large
        dreamcatcher extends beyond the window edge.

        Args:
            painter: QPainter to draw on
            width (int): Window width
            height (int): Window height
            alpha (int): Opacity for the web lines (0-255)
        """
        corner_radius = min(width, height) * 0.28
        corner_spokes = 8

        pen = QPen(QColor(198, 183, 190, alpha), 0.8)
        pen.setCapStyle(Qt.PenCapStyle.RoundCap)
        painter.setBrush(Qt.BrushStyle.NoBrush)
        painter.setPen(pen)

        corners = [
            (0, 0, 0, math.pi / 2),                           # top-left
            (width, 0, math.pi / 2, math.pi),                 # top-right
            (0, height, -math.pi / 2, 0),                     # bottom-left
            (width, height, math.pi, 3 * math.pi / 2),        # bottom-right
        ]

        for cx, cy, angle_start, angle_end in corners:
            # Spokes from corner
            for i in range(corner_spokes + 1):
                angle = angle_start + (angle_end - angle_start) * i / corner_spokes
                ex = cx + corner_radius * math.cos(angle)
                ey = cy + corner_radius * math.sin(angle)
                painter.drawLine(QPointF(cx, cy), QPointF(ex, ey))

            # Outer arc bounding the corner web
            arc_pen = QPen(QColor(198, 183, 190, alpha + 2), 0.8)
            arc_pen.setCapStyle(Qt.PenCapStyle.RoundCap)
            painter.setPen(arc_pen)
            arc_path = QPainterPath()
            arc_steps = corner_spokes * 4
            for j in range(arc_steps + 1):
                a = angle_start + (angle_end - angle_start) * j / arc_steps
                px = cx + corner_radius * math.cos(a)
                py = cy + corner_radius * math.sin(a)
                if j == 0:
                    arc_path.moveTo(QPointF(px, py))
                else:
                    arc_path.lineTo(QPointF(px, py))
            painter.drawPath(arc_path)
            painter.setPen(pen)

            # Arced web rings
            ring_count = 4
            for ring in range(1, ring_count + 1):
                r = corner_radius * ring / ring_count
                path = QPainterPath()
                for i in range(corner_spokes):
                    a1 = angle_start + (angle_end - angle_start) * i / corner_spokes
                    a2 = angle_start + (angle_end - angle_start) * (i + 1) / corner_spokes
                    x1 = cx + r * math.cos(a1)
                    y1 = cy + r * math.sin(a1)
                    x2 = cx + r * math.cos(a2)
                    y2 = cy + r * math.sin(a2)
                    if i == 0:
                        path.moveTo(QPointF(x1, y1))
                    mid_a = (a1 + a2) / 2
                    cr = r * 0.85
                    cx2 = cx + cr * math.cos(mid_a)
                    cy2 = cy + cr * math.sin(mid_a)
                    path.quadTo(QPointF(cx2, cy2), QPointF(x2, y2))

                ring_pen = QPen(QColor(198, 183, 190, max(10, alpha - (ring_count - ring) * 2)), 0.7)
                ring_pen.setCapStyle(Qt.PenCapStyle.RoundCap)
                painter.setPen(ring_pen)
                painter.drawPath(path)
                painter.setPen(pen)

    def _draw_border_filigree(self, painter, width, height, alpha=18):
        """Draw vine-like filigree curves along left and right edges.

        Command, specific. Thin organic curves with spiral terminations,
        like delicate metalwork framing the window content.

        Args:
            painter: QPainter to draw on
            width (int): Window width
            height (int): Window height
            alpha (int): Opacity (0-255)
        """
        pen = QPen(QColor(198, 183, 190, alpha), 0.8)
        pen.setCapStyle(Qt.PenCapStyle.RoundCap)
        painter.setBrush(Qt.BrushStyle.NoBrush)
        painter.setPen(pen)

        margin = 10
        vine_amplitude = 14
        vine_segments = 10

        # Left edge vine
        for i in range(vine_segments):
            t0 = i / vine_segments
            t1 = (i + 1) / vine_segments
            y0 = height * 0.1 + height * 0.8 * t0
            y1 = height * 0.1 + height * 0.8 * t1
            x_off = vine_amplitude * math.sin(t0 * math.pi * 2)
            x_off2 = vine_amplitude * math.sin(t1 * math.pi * 2)
            path = QPainterPath()
            path.moveTo(QPointF(margin + x_off, y0))
            ctrl_y = (y0 + y1) / 2
            path.cubicTo(
                QPointF(margin + vine_amplitude * 1.5, ctrl_y - 10),
                QPointF(margin - vine_amplitude * 0.5, ctrl_y + 10),
                QPointF(margin + x_off2, y1)
            )
            painter.drawPath(path)

        # Right edge vine
        for i in range(vine_segments):
            t0 = i / vine_segments
            t1 = (i + 1) / vine_segments
            y0 = height * 0.1 + height * 0.8 * t0
            y1 = height * 0.1 + height * 0.8 * t1
            x_off = vine_amplitude * math.sin(t0 * math.pi * 2 + math.pi)
            x_off2 = vine_amplitude * math.sin(t1 * math.pi * 2 + math.pi)
            path = QPainterPath()
            path.moveTo(QPointF(width - margin + x_off, y0))
            ctrl_y = (y0 + y1) / 2
            path.cubicTo(
                QPointF(width - margin + vine_amplitude * 1.5, ctrl_y - 10),
                QPointF(width - margin - vine_amplitude * 0.5, ctrl_y + 10),
                QPointF(width - margin + x_off2, y1)
            )
            painter.drawPath(path)

        # Small spiral terminations at the top and bottom of each vine
        spiral_pen = QPen(QColor(198, 183, 190, alpha + 5), 0.5)
        painter.setPen(spiral_pen)
        for x_center in [margin, width - margin]:
            for y_center in [height * 0.1, height * 0.9]:
                spiral_r = 5
                spiral_pts = 20
                sp = QPainterPath()
                for j in range(spiral_pts):
                    t = j / spiral_pts
                    a = t * 2 * math.pi
                    r = spiral_r * t
                    sx = x_center + r * math.cos(a)
                    sy = y_center + r * math.sin(a)
                    if j == 0:
                        sp.moveTo(QPointF(sx, sy))
                    else:
                        sp.lineTo(QPointF(sx, sy))
                painter.drawPath(sp)

    def _draw_dangling_beads(self, painter, width, height, alpha=22):
        """Draw dangling bead elements at the bottom center.

        Command, specific. Short hanging lines with small circles at their
        ends, like beads hanging from a dreamcatcher's bottom rim.

        Args:
            painter: QPainter to draw on
            width (int): Window width
            height (int): Window height
            alpha (int): Opacity (0-255)
        """
        pen = QPen(QColor(198, 183, 190, alpha), 0.8)
        pen.setCapStyle(Qt.PenCapStyle.RoundCap)
        painter.setPen(pen)
        painter.setBrush(Qt.BrushStyle.NoBrush)

        center_x = width / 2
        bead_count = 7
        bead_spacing = 14
        bead_start_y = height - 14

        for i in range(bead_count):
            offset = (i - bead_count // 2) * bead_spacing
            bx = center_x + offset
            # Varying dangle lengths — longer in center, shorter at edges
            dist_from_center = abs(i - bead_count // 2)
            dangle_len = 18 - dist_from_center * 2.5 + 4 * abs(math.sin(i * 1.7))
            by_end = bead_start_y + dangle_len

            # Dangle line
            painter.drawLine(QPointF(bx, bead_start_y), QPointF(bx, by_end))

            # Bead circle at end — slightly larger for center beads
            bead_radius = 2.5 - dist_from_center * 0.2
            painter.drawEllipse(QPointF(bx, by_end + bead_radius), bead_radius, bead_radius)

    def _draw_top_ornament(self, painter, width, alpha=30):
        """Draw a small dreamcatcher ornament at the top center.

        Command, specific. A miniature dreamcatcher decorating the top edge.

        Args:
            painter: QPainter to draw on
            width (int): Window width
            alpha (int): Opacity (0-255)
        """
        ornament_radius = 20
        cx = width / 2
        cy = 22
        self._draw_dreamcatcher(painter, cx, cy, ornament_radius, spokes=10, rings=3, alpha=alpha)

        # Connecting arcs above — like a hanger
        pen = QPen(QColor(198, 183, 190, alpha), 0.7)
        painter.setPen(pen)
        painter.setBrush(Qt.BrushStyle.NoBrush)
        path = QPainterPath()
        path.moveTo(QPointF(cx - ornament_radius - 15, 3))
        path.quadTo(QPointF(cx, 12), QPointF(cx + ornament_radius + 15, 3))
        painter.drawPath(path)
        # Inner echo arc
        pen2 = QPen(QColor(198, 183, 190, alpha - 8), 0.5)
        painter.setPen(pen2)
        path2 = QPainterPath()
        path2.moveTo(QPointF(cx - ornament_radius - 5, 5))
        path2.quadTo(QPointF(cx, 14), QPointF(cx + ornament_radius + 5, 5))
        painter.drawPath(path2)

    def _draw_bottom_ornament(self, painter, width, height, alpha=25):
        """Draw a small dreamcatcher ornament at the bottom center.

        Command, specific. Miniature dreamcatcher at the bottom edge,
        with dangling beads below.

        Args:
            painter: QPainter to draw on
            width (int): Window width
            height (int): Window height
            alpha (int): Opacity (0-255)
        """
        ornament_radius = 16
        cx = width / 2
        cy = height - 32
        self._draw_dreamcatcher(painter, cx, cy, ornament_radius, spokes=8, rings=3, alpha=alpha)

    def _draw_vignette(self, painter, rect, width, height, radius=12):
        """Dark void vignette — deeper at edges for ethereal enclosure.

        Command, specific. Paints semi-transparent gradients along all
        four edges to darken the window perimeter.

        Args:
            painter: QPainter to draw on
            rect (QRectF): Window rectangle
            width (int): Window width
            height (int): Window height
            radius (int): Corner radius for the gradient overlay
        """
        for horizontal, alpha_mult in [(True, 0.35), (False, 0.5)]:
            grad = QLinearGradient(0, 0, width if horizontal else 0, 0 if horizontal else height)
            for pos, alpha in [(0, 120), (0.06, 50), (0.18, 15), (0.82, 15), (0.94, 50), (1, 120)]:
                grad.setColorAt(pos, QColor(10, 8, 20, int(alpha * alpha_mult)))
            painter.setBrush(QBrush(grad))
            painter.setPen(Qt.PenStyle.NoPen)
            painter.drawRoundedRect(rect, radius, radius)

    def _draw_center_glow(self, painter, rect, width, height, radius=12):
        """Subtle radial glow from center — slightly lighter, ethereal.

        Command, specific. A faint radial gradient making the center of the
        window feel slightly luminous compared to the edges.

        Args:
            painter: QPainter to draw on
            rect (QRectF): Window rectangle
            width (int): Window width
            height (int): Window height
            radius (int): Corner radius
        """
        center_glow = QRadialGradient(width / 2, height / 2, max(width, height) * 0.5)
        center_glow.setColorAt(0, QColor(198, 183, 190, 15))
        center_glow.setColorAt(0.3, QColor(198, 183, 190, 8))
        center_glow.setColorAt(0.6, QColor(198, 183, 190, 3))
        center_glow.setColorAt(1, QColor(198, 183, 190, 0))
        painter.setBrush(QBrush(center_glow))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawRoundedRect(rect, radius, radius)

    def paint_window(self, painter, rect, width, height, focused=True):
        """Paint void background with dreamcatcher web ornaments.

        Command, specific. The full window background: tiled void texture,
        large centered dreamcatcher, corner web fragments, edge filigree,
        top/bottom ornaments, dangling beads, vignette, and center glow.

        Args:
            painter: QPainter to draw on
            rect (QRectF): Window rectangle
            width (int): Window width
            height (int): Window height
            focused (bool): Whether the window is focused
        """
        radius = self.corner_radius

        # Clip to rounded rect
        clip = QPainterPath()
        clip.addRoundedRect(QRectF(rect), radius, radius)
        painter.setClipPath(clip)

        # Draw void texture
        texture = self.get_background_pixmap(max(512, height))
        painter.drawTiledPixmap(rect, texture)
        painter.setClipping(False)

        # Dark vignette
        self._draw_vignette(painter, rect, width, height, radius)

        # Subtle center glow when focused
        if focused:
            self._draw_center_glow(painter, rect, width, height, radius)

        # Unclip to allow ornaments to extend beyond window edges
        painter.setClipping(False)

        base_alpha = 38 if focused else 20

        # Large background dreamcatcher — ghostly watermark
        bg_catcher_radius = min(width, height) * 0.38
        self._draw_dreamcatcher(
            painter, width / 2, height / 2,
            bg_catcher_radius, spokes=16, rings=6, alpha=base_alpha
        )

        # Faint ethereal glow around the central dreamcatcher
        catcher_glow = QRadialGradient(width / 2, height / 2, bg_catcher_radius * 1.1)
        catcher_glow.setColorAt(0.7, QColor(198, 183, 190, 0))
        catcher_glow.setColorAt(0.88, QColor(198, 183, 190, 6))
        catcher_glow.setColorAt(1.0, QColor(198, 183, 190, 0))
        painter.setBrush(QBrush(catcher_glow))
        painter.setPen(Qt.PenStyle.NoPen)
        glow_r = bg_catcher_radius * 1.1
        painter.drawEllipse(QPointF(width / 2, height / 2), glow_r, glow_r)

        # Corner web fragments
        self._draw_corner_webs(painter, width, height, alpha=base_alpha + 2)

        # Border filigree vines
        self._draw_border_filigree(painter, width, height, alpha=base_alpha - 5)

        # Top ornament
        self._draw_top_ornament(painter, width, alpha=base_alpha + 12)

        # Bottom ornament + dangling beads
        self._draw_bottom_ornament(painter, width, height, alpha=base_alpha + 8)
        self._draw_dangling_beads(painter, width, height, alpha=base_alpha + 10)

        painter.setClipping(False)

        # Border — mauve when focused, dark slate when not
        painter.setBrush(Qt.BrushStyle.NoBrush)
        if focused:
            painter.setPen(QPen(QColor(198, 183, 190, 90), 1.2))
        else:
            painter.setPen(QPen(QColor(55, 58, 75, 70), 1.0))
        painter.drawRoundedRect(rect, radius, radius)

    def paint_waveform_panel(self, painter, rect, w, h, cy):
        """Waveform panel — dark recessed void with subtle web pattern behind.

        Command, specific. Dark panel with inset shadows and a faint
        dreamcatcher web pattern behind the waveform area.

        Args:
            painter: QPainter to draw on
            rect (QRectF): Panel rectangle
            w (int): Panel width
            h (int): Panel height
            cy (float): Vertical center (for center line)
        """
        # Dark recessed background
        panel_grad = QLinearGradient(0, 0, 0, h)
        panel_grad.setColorAt(0, QColor(12, 12, 22))
        panel_grad.setColorAt(0.3, QColor(18, 18, 30))
        panel_grad.setColorAt(0.7, QColor(16, 16, 26))
        panel_grad.setColorAt(1, QColor(10, 10, 18))
        painter.setBrush(QBrush(panel_grad))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawRoundedRect(rect, 6, 6)

        # Subtle web pattern behind waveform
        panel_cx = w / 2
        panel_cy = h / 2
        panel_r = min(w, h) * 0.35
        self._draw_dreamcatcher(painter, panel_cx, panel_cy, panel_r, spokes=8, rings=3, alpha=10)

        # Subtle mauve glow from top
        top_glow = QLinearGradient(0, 0, 0, h * 0.2)
        top_glow.setColorAt(0, QColor(198, 183, 190, 12))
        top_glow.setColorAt(1, QColor(198, 183, 190, 0))
        painter.setBrush(QBrush(top_glow))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawRoundedRect(rect.adjusted(2, 2, -2, -int(h * 0.8)), 4, 4)

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
            painter.drawRoundedRect(adj, 5, 5)

        # Border — faint mauve
        painter.setBrush(Qt.BrushStyle.NoBrush)
        painter.setPen(QPen(QColor(86, 90, 117, 140), 1.2))
        painter.drawRoundedRect(rect, 6, 6)

        # Center line — faint mauve
        painter.setPen(QPen(QColor(198, 183, 190, 35), 1))
        painter.drawLine(0, int(cy), w, int(cy))
