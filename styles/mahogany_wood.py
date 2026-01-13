"""Mahogany Wood style - warm brown wood grain with classic rich textures."""

import numpy as np
from PyQt6.QtCore import Qt, QRectF
from PyQt6.QtGui import (
    QColor, QLinearGradient, QBrush, QImage, QPixmap,
    QPainterPath, QPen
)

from .base import BaseStyle, get_cached_texture


# Mahogany wood colors
MAHOGANY_DARK = "rgb(62, 34, 24)"
MAHOGANY_MID = "rgb(92, 52, 36)"
MAHOGANY_LIGHT = "rgb(128, 72, 50)"
MAHOGANY_HIGHLIGHT = "rgb(158, 92, 64)"
MAHOGANY_GLOW = "rgb(180, 110, 75)"

# Panel/accent colors - warm gold/amber
AMBER_DARK = "rgb(140, 90, 40)"
AMBER_MID = "rgb(180, 120, 55)"
AMBER_LIGHT = "rgb(210, 150, 70)"
AMBER_GLOW = "rgba(210, 150, 70, 0.5)"

# Text colors - cream/ivory on dark wood
TEXT_CREAM = "rgb(255, 248, 235)"
TEXT_IVORY = "rgb(240, 230, 210)"
TEXT_TAN = "rgb(200, 180, 150)"
TEXT_MUTED = "rgb(160, 140, 115)"
TEXT_DISABLED = "rgb(100, 85, 70)"

# Borders - dark wood grain
BORDER_DARK = "rgb(45, 25, 18)"
BORDER_MID = "rgb(70, 42, 30)"
BORDER_LIGHT = "rgb(100, 62, 44)"


class MahoganyWoodStyle(BaseStyle):
    name = "mahogany_wood"
    font = "Palatino"  # Classic serif font for wood aesthetic

    _wood_cache = None
    _pine_cache = None
    _blue_noise_cache = None

    # Warm wood theme colors
    accent = QColor(210, 150, 70)  # Amber/gold
    accent_css = "rgb(210,150,70)"
    text_primary = TEXT_CREAM
    text_secondary = TEXT_IVORY
    text_muted = TEXT_TAN
    text_error = "rgb(255, 100, 80)"
    text_link = AMBER_LIGHT
    border_color = BORDER_MID
    border_dark = BORDER_DARK
    icon_color_dark = '#3e2218'
    icon_color_light = '#fff8eb'
    icon_color_muted = '#a08060'

    # Slider - dark wood groove, amber handle/fill
    slider_groove = "rgba(45,25,18,0.8)"
    slider_handle = "rgb(210,150,70)"
    slider_fill = "rgb(180,120,55)"

    # Waveform - warm amber glow
    waveform_color = QColor(210, 150, 70)
    waveform_glow = True
    waveform_center_line = QColor(210, 150, 70, 60)
    waveform_panel = "dark"

    # Timer - warm amber LCD
    timer_use_lcd = True
    timer_color = QColor(210, 150, 70)

    # Transcription - dark wood panel
    transcription_text = TEXT_CREAM
    transcription_text_dimmed = TEXT_TAN
    transcription_panel_bg = MAHOGANY_DARK
    transcription_panel_border = BORDER_DARK
    transcription_row_hover = "rgba(210, 150, 70, 0.12)"
    transcription_row_btn_bg = "rgba(210, 150, 70, 0.15)"
    transcription_row_btn_hover = "rgba(210, 150, 70, 0.25)"
    transcription_row_btn_pressed = "rgba(210, 150, 70, 0.4)"

    def button_css(self):
        # Wood-grain buttons with carved inset look
        return (
            f"QPushButton {{ color: {TEXT_TAN}; "
            f"background: qlineargradient(x1:0, y1:0, x2:0, y2:1, "
            f"stop:0 {MAHOGANY_LIGHT}, stop:0.1 {MAHOGANY_MID}, "
            f"stop:0.9 {MAHOGANY_DARK}, stop:1 {BORDER_DARK}); "
            f"border: 2px solid {BORDER_DARK}; border-top-color: {BORDER_LIGHT}; "
            f"border-radius: 4px; padding: 3px 8px; font-size: 11px; "
            f"font-family: {self.font}; text-align: left; }}"
            # Hover: warm glow
            f"QPushButton:hover {{ color: {TEXT_CREAM}; "
            f"background: qlineargradient(x1:0, y1:0, x2:0, y2:1, "
            f"stop:0 {MAHOGANY_HIGHLIGHT}, stop:0.1 {MAHOGANY_LIGHT}, "
            f"stop:0.9 {MAHOGANY_MID}, stop:1 {MAHOGANY_DARK}); "
            f"border: 2px solid {BORDER_MID}; border-top-color: {MAHOGANY_HIGHLIGHT}; }}"
            # Pressed: deeper inset
            f"QPushButton:pressed {{ color: {AMBER_LIGHT}; "
            f"background: qlineargradient(x1:0, y1:0, x2:0, y2:1, "
            f"stop:0 {MAHOGANY_DARK}, stop:0.1 {MAHOGANY_MID}, "
            f"stop:0.9 {MAHOGANY_LIGHT}, stop:1 {MAHOGANY_MID}); "
            f"border: 2px solid {BORDER_DARK}; }}"
            # Disabled
            f"QPushButton:disabled {{ color: {TEXT_DISABLED}; "
            f"background: {MAHOGANY_DARK}; border: 2px solid {BORDER_DARK}; }}"
            # Checked - amber highlight
            f"QPushButton:checked {{ color: {TEXT_CREAM}; "
            f"background: qlineargradient(x1:0, y1:0, x2:0, y2:1, "
            f"stop:0 {AMBER_MID}, stop:0.1 {AMBER_DARK}, "
            f"stop:0.9 rgb(120, 75, 35), stop:1 rgb(90, 55, 25)); "
            f"border: 2px solid {AMBER_DARK}; }}"
            f"QPushButton:checked:hover {{ "
            f"background: qlineargradient(x1:0, y1:0, x2:0, y2:1, "
            f"stop:0 {AMBER_LIGHT}, stop:0.1 {AMBER_MID}, "
            f"stop:0.9 {AMBER_DARK}, stop:1 rgb(100, 65, 30)); }}"
        )

    def menu_css(self):
        return (
            f"QMenu {{ background: {MAHOGANY_DARK}; color: {TEXT_CREAM}; "
            f"border: 2px solid {BORDER_MID}; border-radius: 4px; padding: 4px; "
            f"font-family: {self.font}; font-size: 11px; }}"
            "QMenu::item { padding: 4px 16px; border-radius: 2px; }"
            f"QMenu::item:selected {{ color: {TEXT_CREAM}; "
            f"background: qlineargradient(x1:0, y1:0, x2:0, y2:1, "
            f"stop:0 {AMBER_MID}, stop:0.5 {AMBER_DARK}, stop:1 rgb(110, 70, 32)); }}"
            f"QMenu::separator {{ height: 2px; background: {BORDER_MID}; margin: 4px 8px; }}"
        )

    def scrollbar_css(self):
        # Wood-grain scrollbar
        return (
            f"QScrollBar:vertical {{ width: 14px; background: {MAHOGANY_DARK}; "
            f"border: 1px solid {BORDER_DARK}; border-radius: 5px; margin: 0px; }}"
            # Handle - lighter wood
            "QScrollBar::handle:vertical { "
            "background: qlineargradient(x1:0, y1:0, x2:1, y2:0, "
            f"stop:0.0 {MAHOGANY_MID}, stop:0.2 {MAHOGANY_LIGHT}, "
            f"stop:0.5 {MAHOGANY_HIGHLIGHT}, stop:0.8 {MAHOGANY_LIGHT}, stop:1.0 {MAHOGANY_MID}); "
            f"border: 1px solid {BORDER_MID}; border-radius: 4px; min-height: 40px; margin: 2px; }}"
            # Handle hover
            "QScrollBar::handle:vertical:hover { "
            "background: qlineargradient(x1:0, y1:0, x2:1, y2:0, "
            f"stop:0.0 {MAHOGANY_LIGHT}, stop:0.2 {MAHOGANY_HIGHLIGHT}, "
            f"stop:0.5 {MAHOGANY_GLOW}, stop:0.8 {MAHOGANY_HIGHLIGHT}, stop:1.0 {MAHOGANY_LIGHT}); "
            f"border: 1px solid {BORDER_LIGHT}; }}"
            # Handle pressed
            "QScrollBar::handle:vertical:pressed { "
            "background: qlineargradient(x1:0, y1:0, x2:1, y2:0, "
            f"stop:0.0 {MAHOGANY_DARK}, stop:0.2 {MAHOGANY_MID}, "
            f"stop:0.5 {MAHOGANY_LIGHT}, stop:0.8 {MAHOGANY_MID}, stop:1.0 {MAHOGANY_DARK}); "
            f"border: 1px solid {BORDER_DARK}; }}"
            "QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical { "
            "height: 0; width: 0; background: none; border: none; }"
            "QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical { background: transparent; }"
        )

    def panel_bg_css(self):
        return (
            f"background: qlineargradient(x1:0, y1:0, x2:0, y2:1, "
            f"stop:0 {MAHOGANY_LIGHT}, stop:0.02 {MAHOGANY_MID}, "
            f"stop:0.98 {MAHOGANY_DARK}, stop:1 {BORDER_DARK}); "
            f"border: 2px solid {BORDER_DARK}; border-radius: 4px;"
        )

    def panel_bg_flat_css(self):
        return (
            f"background: {MAHOGANY_DARK}; border: 2px solid {BORDER_DARK}; border-radius: 4px;"
        )

    def get_background_pixmap(self, height=512):
        """Generate procedural mahogany wood grain texture."""
        if MahoganyWoodStyle._wood_cache is not None:
            return MahoganyWoodStyle._wood_cache

        width = 256
        MahoganyWoodStyle._wood_cache = get_cached_texture(
            "mahogany", width, height, lambda: self._generate_wood_texture(width, height)
        )
        return MahoganyWoodStyle._wood_cache

    def _generate_wood_texture(self, width, height):
        """Generate the mahogany wood texture (called on cache miss)."""
        from scipy.ndimage import gaussian_filter

        np.random.seed(1842)  # Mahogany discovery year-ish

        # Create wood grain pattern
        img = np.zeros((height, width, 4), dtype=np.uint8)

        # Base wood color (mahogany RGB roughly 92, 52, 36)
        base_r, base_g, base_b = 82, 48, 34

        # Create vertical grain lines with variation
        for x in range(width):
            # Grain intensity varies across width
            grain_phase = np.sin(x * 0.15) * 0.3 + np.sin(x * 0.4 + 1.2) * 0.2
            grain_intensity = 0.5 + grain_phase

            for y in range(height):
                # Vertical grain with subtle waviness
                wave = np.sin(y * 0.02 + x * 0.1) * 8
                grain_line = np.sin((x + wave) * 0.3) * 0.4 + 0.5

                # Add some noise for natural texture
                noise = np.random.random() * 0.15

                # Combine for final grain value
                grain = grain_line * grain_intensity + noise

                # Apply to base color with variation
                variation = 0.7 + grain * 0.6
                img[y, x, 0] = int(np.clip(base_r * variation, 40, 140))
                img[y, x, 1] = int(np.clip(base_g * variation, 25, 85))
                img[y, x, 2] = int(np.clip(base_b * variation, 18, 60))
                img[y, x, 3] = 255

        # Add horizontal ring patterns (growth rings visible on quarter-sawn wood)
        ring_noise = np.random.random((height, width)) * 20 - 10
        ring_noise = gaussian_filter(ring_noise, sigma=3)

        for y in range(height):
            ring_intensity = (np.sin(y * 0.05) * 0.5 + 0.5) * 0.3
            for x in range(width):
                ring_val = ring_intensity + ring_noise[y, x] / 255
                img[y, x, 0] = int(np.clip(img[y, x, 0] * (1 + ring_val * 0.15), 0, 255))
                img[y, x, 1] = int(np.clip(img[y, x, 1] * (1 + ring_val * 0.12), 0, 255))
                img[y, x, 2] = int(np.clip(img[y, x, 2] * (1 + ring_val * 0.1), 0, 255))

        # Smooth slightly for natural look
        for c in range(3):
            img[:, :, c] = gaussian_filter(img[:, :, c].astype(float), sigma=0.8).astype(np.uint8)

        qimg = QImage(img.data, width, height, width * 4, QImage.Format.Format_RGBA8888).copy()
        return QPixmap.fromImage(qimg)

    def get_pine_texture(self, width=128, height=32):
        """Generate pine wood horizontal grain texture for buttons - yellowy, smaller grain."""
        if MahoganyWoodStyle._pine_cache is not None:
            cached_w, cached_h = MahoganyWoodStyle._pine_cache.width(), MahoganyWoodStyle._pine_cache.height()
            if cached_w >= width and cached_h >= height:
                return MahoganyWoodStyle._pine_cache

        MahoganyWoodStyle._pine_cache = get_cached_texture(
            "pine", width, height, lambda: self._generate_pine_texture(width, height)
        )
        return MahoganyWoodStyle._pine_cache

    def _generate_pine_texture(self, width, height):
        """Generate the pine wood texture (called on cache miss)."""
        from scipy.ndimage import gaussian_filter

        np.random.seed(3141)
        img = np.zeros((height, width, 4), dtype=np.uint8)

        # Pine wood colors - yellowy/tan base
        base_r, base_g, base_b = 180, 140, 85

        for y in range(height):
            # Horizontal grain lines - tight and frequent
            grain_phase = np.sin(y * 0.8) * 0.25 + np.sin(y * 2.1 + 0.5) * 0.15
            grain_intensity = 0.6 + grain_phase

            for x in range(width):
                # Subtle vertical waviness
                wave = np.sin(x * 0.03 + y * 0.15) * 3
                grain_line = np.sin((y + wave) * 0.6) * 0.3 + 0.6

                # Fine noise for natural texture
                noise = np.random.random() * 0.12

                grain = grain_line * grain_intensity + noise
                variation = 0.75 + grain * 0.5

                img[y, x, 0] = int(np.clip(base_r * variation, 120, 220))
                img[y, x, 1] = int(np.clip(base_g * variation, 95, 175))
                img[y, x, 2] = int(np.clip(base_b * variation, 55, 115))
                img[y, x, 3] = 255

        # Light smoothing
        for c in range(3):
            img[:, :, c] = gaussian_filter(img[:, :, c].astype(float), sigma=0.5).astype(np.uint8)

        qimg = QImage(img.data, width, height, width * 4, QImage.Format.Format_RGBA8888).copy()
        return QPixmap.fromImage(qimg)

    def get_blue_noise(self, width=64, height=64):
        """Generate blue noise texture for gritty/tactile feel on text areas."""
        if MahoganyWoodStyle._blue_noise_cache is not None:
            cached_w, cached_h = MahoganyWoodStyle._blue_noise_cache.width(), MahoganyWoodStyle._blue_noise_cache.height()
            if cached_w >= width and cached_h >= height:
                return MahoganyWoodStyle._blue_noise_cache

        MahoganyWoodStyle._blue_noise_cache = get_cached_texture(
            "blue_noise", width, height, lambda: self._generate_blue_noise(width, height)
        )
        return MahoganyWoodStyle._blue_noise_cache

    def _generate_blue_noise(self, width, height):
        """Generate the blue noise texture (called on cache miss)."""
        from scipy.ndimage import gaussian_filter

        np.random.seed(2718)
        # Generate white noise
        noise = np.random.random((height, width))

        # High-pass filter to create blue noise effect (subtract blurred from original)
        blurred = gaussian_filter(noise, sigma=1.5)
        blue_noise = noise - blurred
        blue_noise = (blue_noise - blue_noise.min()) / (blue_noise.max() - blue_noise.min())

        # Create grayscale image with alpha for overlay
        img = np.zeros((height, width, 4), dtype=np.uint8)
        # Neutral gray noise that can be blended
        gray_val = (blue_noise * 60 + 30).astype(np.uint8)  # Range ~30-90
        img[:, :, 0] = gray_val
        img[:, :, 1] = gray_val
        img[:, :, 2] = gray_val
        img[:, :, 3] = 35  # Subtle alpha

        qimg = QImage(img.data, width, height, width * 4, QImage.Format.Format_RGBA8888).copy()
        return QPixmap.fromImage(qimg)

    def _draw_vignette(self, painter, rect, width, height, radius=12):
        """Warm vignette - darker at edges for depth."""
        for horizontal, alpha_mult in [(True, 0.7), (False, 0.9)]:
            grad = QLinearGradient(0, 0, width if horizontal else 0, 0 if horizontal else height)
            for pos, alpha in [(0, 180), (0.1, 100), (0.25, 40), (0.75, 40), (0.9, 100), (1, 180)]:
                grad.setColorAt(pos, QColor(30, 18, 12, int(alpha * alpha_mult)))
            painter.setBrush(QBrush(grad))
            painter.setPen(Qt.PenStyle.NoPen)
            painter.drawRoundedRect(rect, radius, radius)

    def _draw_warm_glow(self, painter, rect, width, height, radius=12):
        """Warm amber glow from edges - like lamp light on wood."""
        # Top warm glow
        top_glow = QLinearGradient(0, 0, 0, 60)
        top_glow.setColorAt(0, QColor(210, 150, 70, 35))
        top_glow.setColorAt(1, QColor(210, 150, 70, 0))
        painter.setBrush(QBrush(top_glow))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawRoundedRect(QRectF(rect.x(), rect.y(), width, 60), radius, radius)

        # Bottom subtle glow
        bottom_glow = QLinearGradient(0, height - 40, 0, height)
        bottom_glow.setColorAt(0, QColor(210, 150, 70, 0))
        bottom_glow.setColorAt(1, QColor(210, 150, 70, 20))
        painter.setBrush(QBrush(bottom_glow))
        painter.drawRoundedRect(QRectF(rect.x(), rect.y() + height - 40, width, 40), radius, radius)

    def paint_window(self, painter, rect, width, height, focused=True):
        """Paint warm mahogany wood background."""
        radius = self.corner_radius

        # Clip to rounded rect
        path = QPainterPath()
        path.addRoundedRect(QRectF(rect), radius, radius)
        painter.setClipPath(path)

        # Draw wood grain texture
        wood = self.get_background_pixmap(max(512, height))
        painter.drawTiledPixmap(rect, wood)
        painter.setClipping(False)

        # Warm vignette
        self._draw_vignette(painter, rect, width, height, radius)

        # Warm glow when focused
        if focused:
            self._draw_warm_glow(painter, rect, width, height, radius)

        # Border - dark wood edge
        if focused:
            painter.setBrush(Qt.BrushStyle.NoBrush)
            painter.setPen(QPen(QColor(140, 90, 50, 150), 2))
            painter.drawRoundedRect(rect, radius, radius)
        else:
            painter.setBrush(Qt.BrushStyle.NoBrush)
            painter.setPen(QPen(QColor(80, 50, 35, 100), 1.5))
            painter.drawRoundedRect(rect, radius, radius)

    def paint_waveform_panel(self, painter, rect, w, h, cy):
        """Waveform panel - inset carved wood look."""
        # Dark recessed gradient
        panel_grad = QLinearGradient(0, 0, 0, h)
        panel_grad.setColorAt(0, QColor(35, 20, 14))
        panel_grad.setColorAt(0.3, QColor(45, 28, 20))
        panel_grad.setColorAt(0.7, QColor(40, 24, 17))
        panel_grad.setColorAt(1, QColor(30, 18, 12))
        painter.setBrush(QBrush(panel_grad))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawRoundedRect(rect, 6, 6)

        # Warm glow from top
        top_glow = QLinearGradient(0, 0, 0, h * 0.25)
        top_glow.setColorAt(0, QColor(210, 150, 70, 30))
        top_glow.setColorAt(1, QColor(210, 150, 70, 0))
        painter.setBrush(QBrush(top_glow))
        painter.drawRoundedRect(rect.adjusted(2, 2, -2, -int(h * 0.75)), 4, 4)

        # Carved inset shadows
        for grad, adj in [
            (QLinearGradient(0, 0, 0, 16), rect.adjusted(1, 1, -1, -h + 17)),
            (QLinearGradient(0, 0, 12, 0), rect.adjusted(1, 1, -w + 13, -1)),
            (QLinearGradient(w, 0, w - 12, 0), rect.adjusted(w - 13, 1, -1, -1)),
        ]:
            grad.setColorAt(0, QColor(20, 12, 8, 180))
            grad.setColorAt(1, QColor(20, 12, 8, 0))
            painter.setBrush(QBrush(grad))
            painter.setPen(Qt.PenStyle.NoPen)
            painter.drawRoundedRect(adj, 5, 5)

        # Subtle horizontal grain lines
        painter.setPen(QPen(QColor(210, 150, 70, 15), 1))
        for i in range(1, 4):
            y = int(h * i / 4)
            painter.drawLine(5, y, w - 5, y)

        # Border - carved wood edge
        painter.setBrush(Qt.BrushStyle.NoBrush)
        painter.setPen(QPen(QColor(70, 42, 30), 2))
        painter.drawRoundedRect(rect, 6, 6)

        # Center line - warm amber
        painter.setPen(QPen(QColor(210, 150, 70, 80), 1))
        painter.drawLine(0, int(cy), w, int(cy))
