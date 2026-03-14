"""Art Nouveau style - deep forest green with gold filigree, inspired by Mucha and Klimt."""

import math
import numpy as np
from PyQt6.QtCore import Qt, QRectF, QPointF
from PyQt6.QtGui import (
    QColor, QLinearGradient, QRadialGradient, QBrush, QImage, QPixmap,
    QPainterPath, QPen
)

from .base import BaseStyle, get_cached_texture


# Deep forest / dark teal backgrounds
FOREST_DEEP = "rgb(18, 32, 26)"
FOREST_DARK = "rgb(24, 42, 34)"
FOREST_MID = "rgb(34, 56, 44)"
FOREST_LIGHT = "rgb(48, 72, 56)"
FOREST_BRIGHT = "rgb(62, 88, 68)"

# Gold / amber accents (antique gold, not bright yellow)
GOLD_DARK = "rgb(140, 115, 45)"
GOLD_MID = "rgb(180, 148, 60)"
GOLD_LIGHT = "rgb(200, 169, 81)"  # #C8A951
GOLD_BRIGHT = "rgb(220, 190, 105)"
GOLD_GLOW = "rgba(200, 169, 81, 0.5)"

# Text colors - cream/ivory on dark forest
TEXT_CREAM = "rgb(243, 234, 214)"   # #F3EAD6 warm parchment
TEXT_IVORY = "rgb(230, 220, 195)"
TEXT_TAN = "rgb(195, 180, 150)"
TEXT_MUTED = "rgb(140, 130, 110)"
TEXT_DISABLED = "rgb(85, 80, 68)"

# Borders - dark organic edges
BORDER_DEEP = "rgb(12, 22, 18)"
BORDER_DARK = "rgb(22, 36, 28)"
BORDER_MID = "rgb(38, 58, 46)"
BORDER_LIGHT = "rgb(55, 78, 60)"

# Jewel accents
EMERALD = "rgb(45, 120, 80)"
EMERALD_DIM = "rgb(30, 80, 55)"
BURGUNDY = "rgb(120, 40, 50)"


class ArtNouveauStyle(BaseStyle):
    name = "art_nouveau"
    font = "Palatino"

    _texture_cache = None

    # Antique gold accent on dark forest
    accent = QColor(200, 169, 81)  # #C8A951
    accent_css = "rgb(200,169,81)"
    text_primary = TEXT_CREAM
    text_secondary = TEXT_IVORY
    text_muted = TEXT_TAN
    text_error = "rgb(200, 85, 75)"
    text_link = GOLD_LIGHT
    border_color = BORDER_MID
    border_dark = BORDER_DARK
    icon_color_dark = '#3e5840'
    icon_color_light = '#f3ead6'
    icon_color_muted = '#8c7a3c'

    # Dropdown input fields - dark forest bg, cream text
    input_bg = '#142a20'
    input_text = '#f3ead6'

    # Slider - dark forest groove, gold handle/fill
    slider_groove = "rgba(18,32,26,0.85)"
    slider_handle = "rgb(200,169,81)"
    slider_fill = "rgb(180,148,60)"

    # Rotary knob - polished brass
    knob_style = "brass"
    knob_body_dark = "#8c7328"
    knob_body_light = "#c8a951"
    knob_notch_style = "needle"
    knob_tickmarks = True
    knob_glow = False
    knob_track_color = "#c8a951"
    knob_label_color = "#f3ead6"

    # Waveform - gold/amber
    waveform_color = QColor(200, 169, 81)
    waveform_glow = True
    waveform_center_line = QColor(200, 169, 81, 55)
    waveform_panel = "dark"

    # Timer - gold LCD
    timer_use_lcd = True
    timer_color = QColor(200, 169, 81)

    # Transcription - dark forest panel
    transcription_text = TEXT_CREAM
    transcription_text_dimmed = TEXT_TAN
    transcription_panel_bg = FOREST_DEEP
    transcription_panel_border = BORDER_DEEP
    transcription_row_hover = "rgba(200, 169, 81, 0.10)"
    transcription_row_btn_bg = "rgba(200, 169, 81, 0.12)"
    transcription_row_btn_hover = "rgba(200, 169, 81, 0.22)"
    transcription_row_btn_pressed = "rgba(200, 169, 81, 0.38)"

    # Chime editor - emerald and gold on dark forest
    chime_grid_bg = QColor(20, 35, 28)
    chime_grid_line = QColor(36, 56, 42)
    chime_cell_inactive = QColor(28, 46, 36)
    chime_cell_active = QColor(180, 148, 60)      # Gold
    chime_cell_highlight = QColor(200, 169, 81, 90)
    chime_piano_white = QColor(240, 232, 210)      # Ivory keys
    chime_piano_black = QColor(22, 38, 30)         # Dark forest keys
    chime_piano_label_white = QColor(50, 70, 52)   # Forest text on ivory
    chime_piano_label_black = QColor(200, 190, 160) # Cream text on dark

    def button_css(self):
        return (
            # Normal - dark forest with gold border, subtle gradient
            f"QPushButton {{ color: {TEXT_TAN}; "
            f"background: qlineargradient(x1:0, y1:0, x2:0, y2:1, "
            f"stop:0 {FOREST_LIGHT}, stop:0.08 {FOREST_MID}, "
            f"stop:0.92 {FOREST_DARK}, stop:1 {BORDER_DEEP}); "
            f"border: 1px solid {BORDER_MID}; border-top-color: {BORDER_LIGHT}; "
            f"border-radius: 5px; padding: 3px 8px; font-size: 11px; "
            f"font-family: {self.font}; text-align: left; }}"
            # Hover - gold border glow
            f"QPushButton:hover {{ color: {TEXT_CREAM}; "
            f"background: qlineargradient(x1:0, y1:0, x2:0, y2:1, "
            f"stop:0 {FOREST_BRIGHT}, stop:0.08 {FOREST_LIGHT}, "
            f"stop:0.92 {FOREST_MID}, stop:1 {FOREST_DARK}); "
            f"border: 1px solid {GOLD_DARK}; border-top-color: {GOLD_MID}; }}"
            # Pressed - deeper inset
            f"QPushButton:pressed {{ color: {GOLD_LIGHT}; "
            f"background: qlineargradient(x1:0, y1:0, x2:0, y2:1, "
            f"stop:0 {FOREST_DARK}, stop:0.08 {FOREST_MID}, "
            f"stop:0.92 {FOREST_LIGHT}, stop:1 {FOREST_MID}); "
            f"border: 1px solid {BORDER_DARK}; }}"
            # Disabled
            f"QPushButton:disabled {{ color: {TEXT_DISABLED}; "
            f"background: {FOREST_DEEP}; border: 1px solid {BORDER_DARK}; }}"
            # Checked - gold highlight
            f"QPushButton:checked {{ color: {TEXT_CREAM}; "
            f"background: qlineargradient(x1:0, y1:0, x2:0, y2:1, "
            f"stop:0 {GOLD_MID}, stop:0.08 {GOLD_DARK}, "
            f"stop:0.92 rgb(110, 90, 35), stop:1 rgb(80, 65, 25)); "
            f"border: 1px solid {GOLD_DARK}; }}"
            f"QPushButton:checked:hover {{ "
            f"background: qlineargradient(x1:0, y1:0, x2:0, y2:1, "
            f"stop:0 {GOLD_LIGHT}, stop:0.08 {GOLD_MID}, "
            f"stop:0.92 {GOLD_DARK}, stop:1 rgb(100, 80, 30)); }}"
        )

    def menu_css(self):
        return (
            f"QMenu {{ background: {FOREST_DEEP}; color: {TEXT_CREAM}; "
            f"border: 2px solid {BORDER_MID}; border-radius: 4px; padding: 4px; "
            f"font-family: {self.font}; font-size: 11px; }}"
            "QMenu::item { padding: 4px 16px; border-radius: 2px; }"
            f"QMenu::item:selected {{ color: {TEXT_CREAM}; "
            f"background: qlineargradient(x1:0, y1:0, x2:0, y2:1, "
            f"stop:0 {GOLD_MID}, stop:0.5 {GOLD_DARK}, stop:1 rgb(110, 90, 35)); }}"
            f"QMenu::separator {{ height: 2px; background: {BORDER_MID}; margin: 4px 8px; }}"
        )

    def _scrollbar_vertical_css(self):
        return (
            f"QScrollBar:vertical {{ width: 14px; background: {FOREST_DEEP}; "
            f"border: 1px solid {BORDER_DARK}; border-radius: 5px; margin: 0px; }}"
            # Handle - forest with gold-ish tint
            "QScrollBar::handle:vertical { "
            "background: qlineargradient(x1:0, y1:0, x2:1, y2:0, "
            f"stop:0.0 {FOREST_MID}, stop:0.2 {FOREST_LIGHT}, "
            f"stop:0.5 {FOREST_BRIGHT}, stop:0.8 {FOREST_LIGHT}, stop:1.0 {FOREST_MID}); "
            f"border: 1px solid {BORDER_MID}; border-radius: 4px; min-height: 40px; margin: 2px; }}"
            # Handle hover - gold tinge
            "QScrollBar::handle:vertical:hover { "
            "background: qlineargradient(x1:0, y1:0, x2:1, y2:0, "
            f"stop:0.0 {FOREST_LIGHT}, stop:0.2 {FOREST_BRIGHT}, "
            f"stop:0.5 rgb(75, 100, 78), stop:0.8 {FOREST_BRIGHT}, stop:1.0 {FOREST_LIGHT}); "
            f"border: 1px solid {BORDER_LIGHT}; }}"
            # Handle pressed
            "QScrollBar::handle:vertical:pressed { "
            "background: qlineargradient(x1:0, y1:0, x2:1, y2:0, "
            f"stop:0.0 {FOREST_DARK}, stop:0.2 {FOREST_MID}, "
            f"stop:0.5 {FOREST_LIGHT}, stop:0.8 {FOREST_MID}, stop:1.0 {FOREST_DARK}); "
            f"border: 1px solid {BORDER_DARK}; }}"
            "QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical { "
            "height: 0; width: 0; background: none; border: none; }"
            "QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical { background: transparent; }"
        )

    def panel_bg_css(self):
        return (
            f"background: qlineargradient(x1:0, y1:0, x2:0, y2:1, "
            f"stop:0 {FOREST_LIGHT}, stop:0.02 {FOREST_MID}, "
            f"stop:0.98 {FOREST_DARK}, stop:1 {BORDER_DEEP}); "
            f"border: 1px solid {BORDER_MID}; border-radius: 4px;"
        )

    def panel_bg_flat_css(self):
        return (
            f"background: {FOREST_DEEP}; border: 1px solid {BORDER_DARK}; border-radius: 4px;"
        )

    def get_background_pixmap(self, height=512):
        """Generate dark forest texture with subtle organic grain."""
        if ArtNouveauStyle._texture_cache is not None:
            return ArtNouveauStyle._texture_cache

        width = 256
        ArtNouveauStyle._texture_cache = get_cached_texture(
            "art_nouveau", width, height, lambda: self._generate_texture(width, height)
        )
        return ArtNouveauStyle._texture_cache

    def _generate_texture(self, width, height):
        """Generate dark forest texture with organic swirl pattern (seamlessly tileable)."""
        from scipy.ndimage import gaussian_filter

        np.random.seed(1890)  # Art Nouveau birth decade

        def seamless_fractal_noise(h, w, octaves=4, persistence=0.5):
            """Generate seamless tileable fractal noise via modular coordinate wrapping."""
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

        # Dark forest green base
        base_r, base_g, base_b = 22, 38, 30

        # Seamless noise layer for organic grain
        grain_noise = seamless_fractal_noise(height, width, octaves=4, persistence=0.5)

        # Coordinate grids for tileable sine swirls (2*pi*x/w wraps seamlessly)
        xs = np.arange(width)[None, :].astype(np.float64)
        ys = np.arange(height)[:, None].astype(np.float64)
        tau_x = 2 * math.pi * xs / width
        tau_y = 2 * math.pi * ys / height

        # Organic swirl — sine interference at tileable frequencies
        # ALL frequency multipliers MUST be integers for seamless tiling
        swirl = (
            np.sin(tau_x * 2 + tau_y * 1) * 0.3
            + np.sin(tau_y * 2 - tau_x * 1 + 1.7) * 0.25
            + np.sin(tau_x * 1 + tau_y * 1) * 0.15
        )

        grain = 0.5 + swirl + grain_noise * 0.1
        variation = 0.75 + grain * 0.5

        img[:, :, 0] = np.clip(base_r * variation, 12, 50).astype(np.uint8)
        img[:, :, 1] = np.clip(base_g * variation, 22, 68).astype(np.uint8)
        img[:, :, 2] = np.clip(base_b * variation, 16, 52).astype(np.uint8)
        img[:, :, 3] = 255

        # Smooth for organic feel (mode='wrap' for seamless tiling)
        for c in range(3):
            img[:, :, c] = gaussian_filter(img[:, :, c].astype(float), sigma=1.2, mode='wrap').astype(np.uint8)

        qimg = QImage(img.data, width, height, width * 4, QImage.Format.Format_RGBA8888).copy()
        return QPixmap.fromImage(qimg)

    def _draw_vine_tendril(self, painter, start, ctrl1, ctrl2, end, pen):
        """Draw a single flowing cubic Bezier curve — an Art Nouveau vine tendril.

        Command, specific. Draws a decorative curve on the given painter.

        Args:
            painter: QPainter to draw on
            start (QPointF): Start point
            ctrl1 (QPointF): First control point
            ctrl2 (QPointF): Second control point
            end (QPointF): End point
            pen (QPen): Pen style for the curve
        """
        path = QPainterPath()
        path.moveTo(start)
        path.cubicTo(ctrl1, ctrl2, end)
        painter.setBrush(Qt.BrushStyle.NoBrush)
        painter.setPen(pen)
        painter.drawPath(path)

    def _draw_corner_vines(self, painter, width, height, alpha=40):
        """Draw flowing vine-like curves at all four corners.

        Command, specific. Paints Art Nouveau ornamental curves
        at the corners of the window. Each corner gets a primary curve
        and a lighter echo curve for layered depth.

        Args:
            painter: QPainter to draw on
            width (int): Window width
            height (int): Window height
            alpha (int): Base opacity for gold curves (0-255)
        """
        gold_pen = QPen(QColor(200, 169, 81, alpha), 1.5)
        gold_pen.setCapStyle(Qt.PenCapStyle.RoundCap)
        echo_pen = QPen(QColor(200, 169, 81, alpha // 3), 1.0)
        echo_pen.setCapStyle(Qt.PenCapStyle.RoundCap)

        vine_reach = min(width, height) * 0.35  # How far vines extend from corner

        # Top-left corner
        self._draw_vine_tendril(
            painter,
            QPointF(0, vine_reach * 0.6),
            QPointF(8, vine_reach * 0.25),
            QPointF(vine_reach * 0.25, 8),
            QPointF(vine_reach * 0.6, 0),
            gold_pen,
        )
        self._draw_vine_tendril(
            painter,
            QPointF(0, vine_reach * 0.8),
            QPointF(12, vine_reach * 0.4),
            QPointF(vine_reach * 0.4, 12),
            QPointF(vine_reach * 0.8, 0),
            echo_pen,
        )

        # Top-right corner
        self._draw_vine_tendril(
            painter,
            QPointF(width - vine_reach * 0.6, 0),
            QPointF(width - vine_reach * 0.25, 8),
            QPointF(width - 8, vine_reach * 0.25),
            QPointF(width, vine_reach * 0.6),
            gold_pen,
        )
        self._draw_vine_tendril(
            painter,
            QPointF(width - vine_reach * 0.8, 0),
            QPointF(width - vine_reach * 0.4, 12),
            QPointF(width - 12, vine_reach * 0.4),
            QPointF(width, vine_reach * 0.8),
            echo_pen,
        )

        # Bottom-left corner
        self._draw_vine_tendril(
            painter,
            QPointF(0, height - vine_reach * 0.6),
            QPointF(8, height - vine_reach * 0.25),
            QPointF(vine_reach * 0.25, height - 8),
            QPointF(vine_reach * 0.6, height),
            gold_pen,
        )
        self._draw_vine_tendril(
            painter,
            QPointF(0, height - vine_reach * 0.8),
            QPointF(12, height - vine_reach * 0.4),
            QPointF(vine_reach * 0.4, height - 12),
            QPointF(vine_reach * 0.8, height),
            echo_pen,
        )

        # Bottom-right corner
        self._draw_vine_tendril(
            painter,
            QPointF(width - vine_reach * 0.6, height),
            QPointF(width - vine_reach * 0.25, height - 8),
            QPointF(width - 8, height - vine_reach * 0.25),
            QPointF(width, height - vine_reach * 0.6),
            gold_pen,
        )
        self._draw_vine_tendril(
            painter,
            QPointF(width - vine_reach * 0.8, height),
            QPointF(width - vine_reach * 0.4, height - 12),
            QPointF(width - 12, height - vine_reach * 0.4),
            QPointF(width, height - vine_reach * 0.8),
            echo_pen,
        )

    def _draw_vignette(self, painter, rect, width, height, radius=12):
        """Dark forest vignette — deeper at edges for enclosure."""
        for horizontal, alpha_mult in [(True, 0.6), (False, 0.8)]:
            grad = QLinearGradient(0, 0, width if horizontal else 0, 0 if horizontal else height)
            for pos, alpha in [(0, 160), (0.1, 80), (0.25, 30), (0.75, 30), (0.9, 80), (1, 160)]:
                grad.setColorAt(pos, QColor(8, 16, 12, int(alpha * alpha_mult)))
            painter.setBrush(QBrush(grad))
            painter.setPen(Qt.PenStyle.NoPen)
            painter.drawRoundedRect(rect, radius, radius)

    def _draw_gold_glow(self, painter, rect, width, height, radius=12):
        """Faint warm gold glow from top edge, like candlelight on gilt."""
        top_glow = QLinearGradient(0, 0, 0, 50)
        top_glow.setColorAt(0, QColor(200, 169, 81, 25))
        top_glow.setColorAt(1, QColor(200, 169, 81, 0))
        painter.setBrush(QBrush(top_glow))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawRoundedRect(QRectF(rect.x(), rect.y(), width, 50), radius, radius)

        bottom_glow = QLinearGradient(0, height - 30, 0, height)
        bottom_glow.setColorAt(0, QColor(200, 169, 81, 0))
        bottom_glow.setColorAt(1, QColor(200, 169, 81, 15))
        painter.setBrush(QBrush(bottom_glow))
        painter.drawRoundedRect(QRectF(rect.x(), rect.y() + height - 30, width, 30), radius, radius)

    def paint_window(self, painter, rect, width, height, focused=True):
        """Paint deep forest background with gold vine ornaments at corners."""
        radius = self.corner_radius

        # Clip to rounded rect
        clip = QPainterPath()
        clip.addRoundedRect(QRectF(rect), radius, radius)
        painter.setClipPath(clip)

        # Draw organic forest texture
        texture = self.get_background_pixmap(max(512, height))
        painter.drawTiledPixmap(rect, texture)
        painter.setClipping(False)

        # Dark vignette for depth
        self._draw_vignette(painter, rect, width, height, radius)

        # Gold glow when focused
        if focused:
            self._draw_gold_glow(painter, rect, width, height, radius)

        # Clip again for vine tendrils so they don't bleed past rounded corners
        painter.setClipPath(clip)
        vine_alpha = 45 if focused else 25
        self._draw_corner_vines(painter, width, height, alpha=vine_alpha)
        painter.setClipping(False)

        # Border — gold when focused, dark when not
        painter.setBrush(Qt.BrushStyle.NoBrush)
        if focused:
            painter.setPen(QPen(QColor(200, 169, 81, 120), 1.5))
        else:
            painter.setPen(QPen(QColor(55, 78, 60, 90), 1.0))
        painter.drawRoundedRect(rect, radius, radius)

    def paint_waveform_panel(self, painter, rect, w, h, cy):
        """Waveform panel — dark recessed panel with gold border and inset shadows."""
        # Dark recessed background
        panel_grad = QLinearGradient(0, 0, 0, h)
        panel_grad.setColorAt(0, QColor(14, 26, 20))
        panel_grad.setColorAt(0.3, QColor(20, 36, 28))
        panel_grad.setColorAt(0.7, QColor(18, 32, 25))
        panel_grad.setColorAt(1, QColor(12, 22, 17))
        painter.setBrush(QBrush(panel_grad))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawRoundedRect(rect, 6, 6)

        # Subtle gold glow from top
        top_glow = QLinearGradient(0, 0, 0, h * 0.2)
        top_glow.setColorAt(0, QColor(200, 169, 81, 20))
        top_glow.setColorAt(1, QColor(200, 169, 81, 0))
        painter.setBrush(QBrush(top_glow))
        painter.drawRoundedRect(rect.adjusted(2, 2, -2, -int(h * 0.8)), 4, 4)

        # Carved inset shadows along edges
        for grad, adj in [
            (QLinearGradient(0, 0, 0, 14), rect.adjusted(1, 1, -1, -h + 15)),
            (QLinearGradient(0, 0, 10, 0), rect.adjusted(1, 1, -w + 11, -1)),
            (QLinearGradient(w, 0, w - 10, 0), rect.adjusted(w - 11, 1, -1, -1)),
        ]:
            grad.setColorAt(0, QColor(6, 12, 8, 160))
            grad.setColorAt(1, QColor(6, 12, 8, 0))
            painter.setBrush(QBrush(grad))
            painter.setPen(Qt.PenStyle.NoPen)
            painter.drawRoundedRect(adj, 5, 5)

        # Border — antique gold edge
        painter.setBrush(Qt.BrushStyle.NoBrush)
        painter.setPen(QPen(QColor(140, 115, 45, 180), 1.5))
        painter.drawRoundedRect(rect, 6, 6)

        # Center line — faint gold
        painter.setPen(QPen(QColor(200, 169, 81, 60), 1))
        painter.drawLine(0, int(cy), w, int(cy))
