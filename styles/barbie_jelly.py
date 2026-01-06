"""Barbie Jelly style - hot pink shiny 3D plastic like mid-2000s jelly accessories."""

import numpy as np
from PyQt6.QtCore import Qt, QRectF, QPointF
from PyQt6.QtGui import (
    QColor, QLinearGradient, QRadialGradient, QBrush, QImage, QPixmap,
    QPainterPath, QPen
)

from .base import BaseStyle


# Hot pink Barbie colors
HOT_PINK = QColor(255, 20, 147)
HOT_PINK_CSS = "rgb(255, 20, 147)"
BARBIE_PINK = "rgb(255, 105, 180)"
BARBIE_LIGHT = "rgb(255, 182, 193)"
BARBIE_GLOW = "rgba(255, 105, 180, 0.5)"
BARBIE_DARK = "rgb(219, 48, 130)"
MAGENTA = "rgb(255, 0, 128)"

# Jelly plastic surface colors
JELLY_HIGHLIGHT = "rgb(255, 220, 235)"  # Almost white pink
JELLY_MID = "rgb(255, 130, 180)"
JELLY_DEEP = "rgb(200, 40, 120)"
JELLY_SHADOW = "rgb(150, 20, 90)"

# Text colors - white/light on pink
TEXT_BRIGHT = "rgb(255, 255, 255)"
TEXT_LIGHT = "rgb(255, 230, 240)"
TEXT_DIM = "rgb(255, 180, 200)"
TEXT_DISABLED = "rgb(200, 120, 150)"

# Borders - glossy pink edges
BORDER_LIGHT = "rgb(255, 180, 210)"
BORDER_PINK = "rgb(255, 80, 150)"
BORDER_DARK = "rgb(180, 40, 100)"


class BarbieJellyStyle(BaseStyle):
    name = "barbie_jelly"
    font = "Comic Sans MS"  # Fun bubbly font

    _jelly_cache = None

    # Barbie theme colors
    accent = HOT_PINK
    text_primary = TEXT_BRIGHT
    text_secondary = TEXT_LIGHT
    text_muted = TEXT_DIM
    text_error = "rgb(255, 80, 80)"
    text_link = BARBIE_LIGHT
    border_color = BORDER_PINK
    border_dark = BORDER_DARK
    icon_color_dark = '#ff69b4'
    icon_color_light = '#ffb6c1'
    icon_color_muted = '#db3082'

    # Waveform - pink pulse
    waveform_color = HOT_PINK
    waveform_glow = True
    waveform_center_line = QColor(255, 105, 180, 80)
    waveform_panel = "dark"

    # Timer - pink LCD
    timer_use_lcd = True
    timer_color = HOT_PINK

    # Transcription - pink jelly panel
    transcription_text = TEXT_BRIGHT
    transcription_text_dimmed = TEXT_DIM
    transcription_panel_bg = JELLY_DEEP
    transcription_panel_border = BORDER_DARK
    transcription_row_hover = "rgba(255, 105, 180, 0.15)"
    transcription_row_btn_bg = "rgba(255, 105, 180, 0.15)"
    transcription_row_btn_hover = "rgba(255, 105, 180, 0.25)"
    transcription_row_btn_pressed = "rgba(255, 105, 180, 0.4)"

    def button_css(self):
        # Shiny jelly 3D buttons with glossy highlights
        return (
            f"QPushButton {{ color: {TEXT_BRIGHT}; "
            f"background: qlineargradient(x1:0, y1:0, x2:0, y2:1, "
            f"stop:0 {BARBIE_LIGHT}, stop:0.3 {BARBIE_PINK}, stop:0.5 {BARBIE_DARK}, stop:1 {JELLY_DEEP}); "
            f"border: 2px solid {BORDER_PINK}; border-top-color: {BARBIE_LIGHT}; "
            f"border-radius: 10px; padding: 4px 10px; font-size: 11px; "
            f"font-family: {self.font}; text-align: left; }}"
            # Hover: brighter glossy pink
            f"QPushButton:hover {{ color: {TEXT_BRIGHT}; "
            f"background: qlineargradient(x1:0, y1:0, x2:0, y2:1, "
            f"stop:0 {JELLY_HIGHLIGHT}, stop:0.25 {BARBIE_LIGHT}, stop:0.5 {BARBIE_PINK}, stop:1 {BARBIE_DARK}); "
            f"border: 2px solid {HOT_PINK_CSS}; }}"
            # Pressed: inverted depth
            f"QPushButton:pressed {{ color: {TEXT_LIGHT}; "
            f"background: qlineargradient(x1:0, y1:0, x2:0, y2:1, "
            f"stop:0 {JELLY_DEEP}, stop:0.4 {BARBIE_DARK}, stop:0.7 {BARBIE_PINK}, stop:1 {BARBIE_LIGHT}); "
            f"border: 2px solid {BORDER_DARK}; }}"
            # Disabled
            f"QPushButton:disabled {{ color: {TEXT_DISABLED}; "
            f"background: {JELLY_SHADOW}; border: 2px solid {BORDER_DARK}; }}"
            # Checked - extra shiny
            f"QPushButton:checked {{ color: {TEXT_BRIGHT}; "
            f"background: qlineargradient(x1:0, y1:0, x2:0, y2:1, "
            f"stop:0 {JELLY_HIGHLIGHT}, stop:0.2 {MAGENTA}, stop:0.6 {HOT_PINK_CSS}, stop:1 {BARBIE_DARK}); "
            f"border: 2px solid {MAGENTA}; }}"
            f"QPushButton:checked:hover {{ "
            f"background: qlineargradient(x1:0, y1:0, x2:0, y2:1, "
            f"stop:0 rgb(255, 240, 250), stop:0.2 {BARBIE_LIGHT}, stop:0.6 {MAGENTA}, stop:1 {BARBIE_DARK}); }}"
        )

    def menu_css(self):
        return (
            f"QMenu {{ background: qlineargradient(x1:0, y1:0, x2:0, y2:1, "
            f"stop:0 {BARBIE_PINK}, stop:1 {JELLY_DEEP}); color: {TEXT_BRIGHT}; "
            f"border: 2px solid {BORDER_PINK}; border-radius: 8px; padding: 4px; "
            f"font-family: {self.font}; font-size: 11px; }}"
            "QMenu::item { padding: 5px 16px; border-radius: 4px; }"
            f"QMenu::item:selected {{ color: {TEXT_BRIGHT}; "
            f"background: qlineargradient(x1:0, y1:0, x2:0, y2:1, "
            f"stop:0 {JELLY_HIGHLIGHT}, stop:0.5 {HOT_PINK_CSS}, stop:1 {BARBIE_DARK}); }}"
            f"QMenu::separator {{ height: 2px; background: {BORDER_PINK}; margin: 4px 8px; }}"
        )

    def scrollbar_css(self):
        # Pink jelly scrollbar
        return (
            f"QScrollBar:vertical {{ width: 16px; "
            f"background: qlineargradient(x1:0, y1:0, x2:1, y2:0, "
            f"stop:0 {JELLY_SHADOW}, stop:0.5 {JELLY_DEEP}, stop:1 {JELLY_SHADOW}); "
            f"border: 1px solid {BORDER_DARK}; border-radius: 8px; margin: 0px; }}"
            # Handle - shiny jelly pink
            "QScrollBar::handle:vertical { "
            "background: qlineargradient(x1:0, y1:0, x2:1, y2:0, "
            f"stop:0.0 {BARBIE_DARK}, stop:0.2 {BARBIE_PINK}, "
            f"stop:0.5 {BARBIE_LIGHT}, stop:0.8 {BARBIE_PINK}, stop:1.0 {BARBIE_DARK}); "
            f"border: 1px solid {BORDER_PINK}; border-radius: 6px; min-height: 40px; margin: 2px; }}"
            # Handle hover - brighter
            "QScrollBar::handle:vertical:hover { "
            "background: qlineargradient(x1:0, y1:0, x2:1, y2:0, "
            f"stop:0.0 {BARBIE_PINK}, stop:0.2 {BARBIE_LIGHT}, "
            f"stop:0.5 {JELLY_HIGHLIGHT}, stop:0.8 {BARBIE_LIGHT}, stop:1.0 {BARBIE_PINK}); "
            f"border: 1px solid {HOT_PINK_CSS}; }}"
            # Handle pressed
            "QScrollBar::handle:vertical:pressed { "
            "background: qlineargradient(x1:0, y1:0, x2:1, y2:0, "
            f"stop:0.0 {JELLY_DEEP}, stop:0.2 {BARBIE_DARK}, "
            f"stop:0.5 {BARBIE_PINK}, stop:0.8 {BARBIE_DARK}, stop:1.0 {JELLY_DEEP}); "
            f"border: 1px solid {BORDER_DARK}; }}"
            "QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical { "
            "height: 0; width: 0; background: none; border: none; }"
            "QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical { background: transparent; }"
        )

    def panel_bg_css(self):
        return (
            f"background: qlineargradient(x1:0, y1:0, x2:0, y2:1, "
            f"stop:0 {BARBIE_PINK}, stop:0.02 {JELLY_DEEP}, "
            f"stop:0.98 {JELLY_DEEP}, stop:1 {JELLY_SHADOW}); "
            f"border: 2px solid {BORDER_DARK}; border-radius: 8px;"
        )

    def panel_bg_flat_css(self):
        return (
            f"background: {JELLY_DEEP}; border: 2px solid {BORDER_DARK}; border-radius: 8px;"
        )

    def get_background_pixmap(self, height=512):
        """Shiny pink jelly plastic texture with cellular gel-cap pattern and glitter."""
        if BarbieJellyStyle._jelly_cache is not None:
            return BarbieJellyStyle._jelly_cache

        from scipy.ndimage import gaussian_filter, distance_transform_edt

        width = 256
        np.random.seed(2000)  # Y2K era

        # === CELLULAR GEL-CAP PATTERN (FilterForge-style Voronoi) ===
        # Create cell centers for organic blob pattern
        n_cells = 80
        cell_x = np.random.randint(0, width, n_cells)
        cell_y = np.random.randint(0, height, n_cells)

        # Calculate distance to nearest cell center for each pixel
        yy, xx = np.mgrid[0:height, 0:width]
        cell_dist = np.full((height, width), np.inf)
        for cx, cy in zip(cell_x, cell_y):
            dist = np.sqrt((xx - cx)**2 + (yy - cy)**2)
            cell_dist = np.minimum(cell_dist, dist)

        # Normalize and create soft cell edges (gel capsule look)
        cell_pattern = gaussian_filter(cell_dist, sigma=3)
        cell_pattern = (cell_pattern - cell_pattern.min()) / (cell_pattern.max() - cell_pattern.min())
        cell_highlight = np.clip(1.0 - cell_pattern * 2, 0, 1) * 30  # Bright at cell centers

        # === GLOSSY PLASTIC STREAKS ===
        base = np.random.randint(0, 25, size=(height, width)).astype(np.float32)
        smooth = gaussian_filter(base, sigma=6)
        streaks = np.random.randint(0, 20, size=(height, width)).astype(np.float32)
        streaks = gaussian_filter(streaks, sigma=(2, 40))  # Horizontal injection-mold streaks

        # === GLITTER SPARKLE LAYER ===
        glitter = np.random.random((height, width))
        glitter = (glitter > 0.992).astype(np.float32) * 60  # Sparse bright sparkles
        glitter = gaussian_filter(glitter, sigma=0.8)  # Tiny soft glow

        # === SUBSURFACE DEPTH BLOBS ===
        depth_blobs = np.random.random((height, width)).astype(np.float32)
        depth_blobs = gaussian_filter(depth_blobs, sigma=15)
        depth_blobs = (depth_blobs - 0.5) * 20  # Creates depth variation

        # Combine all layers
        combined = smooth + streaks * 0.4 + cell_highlight + glitter + depth_blobs * 0.5

        img = np.zeros((height, width, 4), dtype=np.uint8)

        # Base pink color with variations
        r_base = 220
        g_base = 60
        b_base = 140

        img[:, :, 0] = np.clip(r_base + combined - 10, 180, 255).astype(np.uint8)
        img[:, :, 1] = np.clip(g_base + combined * 0.25, 30, 110).astype(np.uint8)
        img[:, :, 2] = np.clip(b_base + combined * 0.4, 100, 185).astype(np.uint8)
        img[:, :, 3] = 255

        qimg = QImage(img.data, width, height, width * 4, QImage.Format.Format_RGBA8888).copy()
        BarbieJellyStyle._jelly_cache = QPixmap.fromImage(qimg)
        return BarbieJellyStyle._jelly_cache

    def _draw_glossy_highlight(self, painter, rect, width, height, radius=12):
        """Draw glossy plastic shine overlay at top."""
        # Main gloss highlight - wide arc at top
        gloss = QLinearGradient(0, 0, 0, height * 0.4)
        gloss.setColorAt(0, QColor(255, 255, 255, 120))
        gloss.setColorAt(0.3, QColor(255, 220, 235, 80))
        gloss.setColorAt(0.6, QColor(255, 180, 210, 30))
        gloss.setColorAt(1, QColor(255, 105, 180, 0))
        painter.setBrush(QBrush(gloss))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawRoundedRect(QRectF(rect.x(), rect.y(), width, height * 0.45), radius, radius)

        # Sharp specular highlight - small bright spot
        spec_x = width * 0.25
        spec_y = height * 0.12
        spec_radius = min(width, height) * 0.15
        specular = QRadialGradient(QPointF(spec_x, spec_y), spec_radius)
        specular.setColorAt(0, QColor(255, 255, 255, 180))
        specular.setColorAt(0.5, QColor(255, 240, 250, 80))
        specular.setColorAt(1, QColor(255, 200, 220, 0))
        painter.setBrush(QBrush(specular))
        painter.drawEllipse(QPointF(spec_x, spec_y), spec_radius, spec_radius * 0.6)

    def _draw_pink_vignette(self, painter, rect, width, height, radius=12):
        """Subtle dark pink vignette at edges."""
        for horizontal, alpha_mult in [(True, 0.5), (False, 0.8)]:
            grad = QLinearGradient(0, 0, width if horizontal else 0, 0 if horizontal else height)
            for pos, alpha in [(0, 100), (0.15, 40), (0.85, 40), (1, 100)]:
                grad.setColorAt(pos, QColor(100, 20, 60, int(alpha * alpha_mult)))
            painter.setBrush(QBrush(grad))
            painter.setPen(Qt.PenStyle.NoPen)
            painter.drawRoundedRect(rect, radius, radius)

    def _draw_jelly_sparkle(self, painter, x, y, size):
        """Draw a small sparkle/glint like on shiny plastic."""
        # Star-shaped sparkle
        sparkle = QRadialGradient(QPointF(x, y), size)
        sparkle.setColorAt(0, QColor(255, 255, 255, 255))
        sparkle.setColorAt(0.3, QColor(255, 240, 250, 200))
        sparkle.setColorAt(0.7, QColor(255, 180, 210, 50))
        sparkle.setColorAt(1, QColor(255, 105, 180, 0))
        painter.setBrush(QBrush(sparkle))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawEllipse(QPointF(x, y), size, size)

    def paint_window(self, painter, rect, width, height, focused=True):
        """Paint shiny pink jelly plastic background."""
        radius = self.corner_radius

        # Clip to rounded rect
        path = QPainterPath()
        path.addRoundedRect(QRectF(rect), radius, radius)
        painter.setClipPath(path)

        # Draw pink jelly texture
        jelly = self.get_background_pixmap(max(512, height))
        painter.drawTiledPixmap(rect, jelly)
        painter.setClipping(False)

        # Dark pink vignette
        self._draw_pink_vignette(painter, rect, width, height, radius)

        # Glossy highlight overlay
        if focused:
            self._draw_glossy_highlight(painter, rect, width, height, radius)

        # Add sparkles when focused
        if focused:
            np.random.seed(42)  # Consistent sparkle positions
            for _ in range(5):
                sx = np.random.randint(20, width - 20)
                sy = np.random.randint(10, int(height * 0.3))
                self._draw_jelly_sparkle(painter, sx, sy, 3 + np.random.randint(0, 4))

        # Pink border with highlight
        if focused:
            painter.setBrush(Qt.BrushStyle.NoBrush)
            painter.setPen(QPen(QColor(255, 105, 180, 150), 2))
            painter.drawRoundedRect(rect, radius, radius)
            # Inner highlight at top
            painter.setPen(QPen(QColor(255, 200, 230, 80), 1))
            painter.drawRoundedRect(rect.adjusted(2, 2, -2, -height + 20), radius - 2, radius - 2)
        else:
            painter.setBrush(Qt.BrushStyle.NoBrush)
            painter.setPen(QPen(QColor(180, 60, 100, 100), 1.5))
            painter.drawRoundedRect(rect, radius, radius)

    def paint_waveform_panel(self, painter, rect, w, h, cy):
        """Pink jelly waveform panel - shiny plastic."""
        # Gradient pink background
        panel_grad = QLinearGradient(0, 0, 0, h)
        panel_grad.setColorAt(0, QColor(180, 50, 110))
        panel_grad.setColorAt(0.3, QColor(150, 35, 90))
        panel_grad.setColorAt(0.7, QColor(120, 25, 70))
        panel_grad.setColorAt(1, QColor(100, 20, 60))
        painter.setBrush(QBrush(panel_grad))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawRoundedRect(rect, 8, 8)

        # Glossy top highlight
        gloss = QLinearGradient(0, 0, 0, h * 0.35)
        gloss.setColorAt(0, QColor(255, 200, 220, 80))
        gloss.setColorAt(0.5, QColor(255, 150, 180, 30))
        gloss.setColorAt(1, QColor(255, 100, 150, 0))
        painter.setBrush(QBrush(gloss))
        painter.drawRoundedRect(rect.adjusted(2, 2, -2, -int(h * 0.65)), 6, 6)

        # Deep inset shadows
        for grad, adj in [
            (QLinearGradient(0, 0, 0, 15), rect.adjusted(1, 1, -1, -h + 16)),
            (QLinearGradient(0, 0, 12, 0), rect.adjusted(1, 1, -w + 13, -1)),
            (QLinearGradient(w, 0, w - 12, 0), rect.adjusted(w - 13, 1, -1, -1)),
        ]:
            grad.setColorAt(0, QColor(80, 15, 50, 180))
            grad.setColorAt(1, QColor(80, 15, 50, 0))
            painter.setBrush(QBrush(grad))
            painter.setPen(Qt.PenStyle.NoPen)
            painter.drawRoundedRect(adj, 7, 7)

        # Subtle grid lines - pink tinted
        painter.setPen(QPen(QColor(255, 150, 180, 25), 1))
        for i in range(1, 4):
            y = int(h * i / 4)
            painter.drawLine(5, y, w - 5, y)

        # Border - pink plastic edge
        painter.setBrush(Qt.BrushStyle.NoBrush)
        painter.setPen(QPen(QColor(200, 60, 120), 2))
        painter.drawRoundedRect(rect, 8, 8)

        # Center line - hot pink
        painter.setPen(QPen(QColor(255, 80, 150, 100), 1))
        painter.drawLine(0, int(cy), w, int(cy))
