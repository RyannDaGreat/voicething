"""Supervillain style - EVIL black/red theme with angry glowing text and metal."""

import numpy as np
from PyQt6.QtCore import Qt, QRectF, QPointF
from PyQt6.QtGui import (
    QColor, QLinearGradient, QRadialGradient, QBrush, QImage, QPixmap,
    QPainterPath, QPen
)

from .base import BaseStyle


# EVIL colors - blood red and black
BLOOD_RED = QColor(200, 20, 20)
BLOOD_RED_CSS = "rgb(200, 20, 20)"
BLOOD_BRIGHT = "rgb(255, 40, 40)"
BLOOD_GLOW = "rgba(255, 40, 40, 0.5)"
BLOOD_DARK = "rgb(140, 15, 15)"

# Pure evil black
BLACK_VOID = "rgb(5, 5, 8)"
BLACK_DEEP = "rgb(12, 10, 15)"
BLACK_MID = "rgb(25, 20, 28)"
BLACK_LIGHT = "rgb(40, 35, 45)"

# Angry text - glowing red
TEXT_FURY = "rgb(255, 60, 60)"
TEXT_RAGE = "rgb(255, 100, 100)"
TEXT_DIM = "rgb(180, 80, 80)"
TEXT_DISABLED = "rgb(80, 40, 40)"

# Borders - dark with red tinge
BORDER_BLOOD = "rgb(100, 20, 25)"
BORDER_DARK = "rgb(40, 15, 20)"
BORDER_LIGHT = "rgb(70, 30, 35)"


class SupervillainStyle(BaseStyle):
    name = "supervillain"
    font = "Copperplate Gothic Bold"  # EVIL supervillain font

    _metal_cache = None

    # EVIL theme colors
    accent = BLOOD_RED
    accent_css = BLOOD_RED_CSS
    text_primary = TEXT_FURY
    text_secondary = TEXT_RAGE
    text_muted = TEXT_DIM
    text_error = "rgb(255, 0, 0)"
    text_link = BLOOD_BRIGHT
    border_color = BORDER_BLOOD
    border_dark = BORDER_DARK
    icon_color_dark = '#ff2020'
    icon_color_light = '#ff4040'
    icon_color_muted = '#801010'

    # Dropdown input fields - evil dark to match theme
    input_bg = '#0c080c'
    input_text = '#ff8080'

    # Slider - blood red groove on black void
    slider_groove = "rgba(200,20,20,0.4)"

    # Rotary knob - EVIL dark style with red glow
    knob_style = "evil"
    knob_body_dark = "#280808"
    knob_body_light = "#401818"
    knob_notch_style = "arrow"
    knob_tickmarks = True
    knob_glow = True
    knob_track_color = "#ff2828"  # Blood red track
    knob_label_color = "#ff6060"  # Red text

    # Waveform - blood red pulse
    waveform_color = BLOOD_RED
    waveform_glow = True
    waveform_center_line = QColor(255, 40, 40, 80)
    waveform_panel = "dark"

    # Timer - red LED countdown to doom
    timer_use_lcd = True
    timer_color = BLOOD_RED

    # Transcription - dark evil panel
    transcription_text = TEXT_FURY
    transcription_text_dimmed = TEXT_DIM
    transcription_panel_bg = BLACK_DEEP
    transcription_panel_border = BORDER_DARK
    transcription_row_hover = "rgba(255, 40, 40, 0.15)"
    transcription_row_btn_bg = "rgba(255, 40, 40, 0.15)"
    transcription_row_btn_hover = "rgba(255, 40, 40, 0.25)"
    transcription_row_btn_pressed = "rgba(255, 40, 40, 0.4)"

    # Chime editor - evil purple/green
    chime_grid_bg = QColor(15, 12, 20)  # Near black purple
    chime_grid_line = QColor(50, 40, 60)  # Dark purple
    chime_cell_inactive = QColor(30, 25, 40)  # Dark purple
    chime_cell_active = QColor(100, 255, 100)  # Toxic green
    chime_cell_highlight = QColor(100, 255, 100, 80)  # Green glow
    chime_piano_white = QColor(180, 170, 200)  # Pale purple
    chime_piano_black = QColor(25, 20, 35)  # Very dark purple
    chime_piano_label_white = QColor(60, 50, 80)  # Purple text
    chime_piano_label_black = QColor(100, 255, 100)  # Green text

    def button_css(self):
        # EVIL buttons with red glow on hover
        return (
            f"QPushButton {{ color: {TEXT_DIM}; "
            f"background: qlineargradient(x1:0, y1:0, x2:0, y2:1, "
            f"stop:0 {BLACK_LIGHT}, stop:0.3 {BLACK_MID}, stop:0.7 {BLACK_DEEP}, stop:1 {BLACK_MID}); "
            f"border: 2px solid {BORDER_DARK}; border-top-color: {BORDER_LIGHT}; "
            f"border-radius: 4px; padding: 3px 8px; font-size: 11px; "
            f"font-family: {self.font}; text-transform: uppercase; text-align: left; }}"
            # Hover: ANGRY red glow
            f"QPushButton:hover {{ color: {TEXT_FURY}; "
            f"background: qlineargradient(x1:0, y1:0, x2:0, y2:1, "
            f"stop:0 rgb(70, 25, 30), stop:0.3 rgb(50, 18, 22), stop:0.7 rgb(35, 12, 16), stop:1 rgb(50, 18, 22)); "
            f"border: 2px solid rgb(180, 30, 35); }}"
            # Pressed: deeper evil
            f"QPushButton:pressed {{ color: {BLOOD_BRIGHT}; "
            f"background: qlineargradient(x1:0, y1:0, x2:0, y2:1, "
            f"stop:0 rgb(30, 10, 14), stop:0.3 rgb(45, 15, 20), stop:0.7 rgb(55, 20, 25), stop:1 rgb(45, 15, 20)); "
            f"border: 2px solid rgb(140, 25, 30); }}"
            # Disabled - dead
            f"QPushButton:disabled {{ color: {TEXT_DISABLED}; "
            f"background: {BLACK_DEEP}; border: 2px solid {BORDER_DARK}; }}"
            # Checked - ACTIVATED EVIL
            f"QPushButton:checked {{ color: {BLOOD_BRIGHT}; "
            f"background: qlineargradient(x1:0, y1:0, x2:0, y2:1, "
            f"stop:0 rgb(140, 20, 25), stop:0.3 rgb(110, 15, 20), stop:0.7 rgb(80, 10, 15), stop:1 rgb(110, 15, 20)); "
            f"border: 2px solid {BLOOD_RED_CSS}; }}"
            f"QPushButton:checked:hover {{ "
            f"background: qlineargradient(x1:0, y1:0, x2:0, y2:1, "
            f"stop:0 rgb(160, 25, 30), stop:0.3 rgb(130, 20, 25), stop:0.7 rgb(100, 15, 20), stop:1 rgb(130, 20, 25)); }}"
        )

    def menu_css(self):
        return (
            f"QMenu {{ background: {BLACK_DEEP}; color: {TEXT_FURY}; "
            f"border: 2px solid {BORDER_BLOOD}; border-radius: 4px; padding: 4px; "
            f"font-family: {self.font}; font-size: 11px; text-transform: uppercase; }}"
            "QMenu::item { padding: 4px 16px; border-radius: 2px; }"
            f"QMenu::item:selected {{ color: {BLOOD_BRIGHT}; "
            f"background: qlineargradient(x1:0, y1:0, x2:0, y2:1, "
            f"stop:0 rgb(120, 20, 25), stop:0.5 rgb(100, 15, 20), stop:1 rgb(80, 10, 15)); }}"
            f"QMenu::separator {{ height: 2px; background: {BORDER_BLOOD}; margin: 4px 8px; }}"
        )

    def _scrollbar_vertical_css(self):
        # Blood-red scrollbar
        return (
            f"QScrollBar:vertical {{ width: 14px; background: {BLACK_DEEP}; "
            f"border: 1px solid {BORDER_DARK}; border-radius: 5px; margin: 0px; }}"
            # Handle - blood red
            "QScrollBar::handle:vertical { "
            "background: qlineargradient(x1:0, y1:0, x2:1, y2:0, "
            "stop:0.0 rgb(100, 15, 20), stop:0.2 rgb(140, 25, 30), "
            "stop:0.5 rgb(160, 30, 35), stop:0.8 rgb(140, 25, 30), stop:1.0 rgb(100, 15, 20)); "
            f"border: 1px solid rgb(80, 15, 20); border-radius: 4px; min-height: 40px; margin: 2px; }}"
            # Handle hover - brighter blood
            "QScrollBar::handle:vertical:hover { "
            "background: qlineargradient(x1:0, y1:0, x2:1, y2:0, "
            "stop:0.0 rgb(140, 25, 30), stop:0.2 rgb(180, 35, 40), "
            "stop:0.5 rgb(200, 40, 45), stop:0.8 rgb(180, 35, 40), stop:1.0 rgb(140, 25, 30)); "
            "border: 1px solid rgb(120, 25, 30); }"
            # Handle pressed
            "QScrollBar::handle:vertical:pressed { "
            "background: qlineargradient(x1:0, y1:0, x2:1, y2:0, "
            "stop:0.0 rgb(80, 10, 15), stop:0.2 rgb(110, 18, 23), "
            "stop:0.5 rgb(130, 22, 27), stop:0.8 rgb(110, 18, 23), stop:1.0 rgb(80, 10, 15)); "
            "border: 1px solid rgb(60, 10, 15); }"
            "QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical { "
            "height: 0; width: 0; background: none; border: none; }"
            "QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical { background: transparent; }"
        )

    def panel_bg_css(self):
        return (
            f"background: qlineargradient(x1:0, y1:0, x2:0, y2:1, "
            f"stop:0 {BLACK_LIGHT}, stop:0.02 {BLACK_DEEP}, "
            f"stop:0.98 {BLACK_DEEP}, stop:1 {BLACK_VOID}); "
            f"border: 2px solid {BORDER_DARK}; border-radius: 4px;"
        )

    def panel_bg_flat_css(self):
        return (
            f"background: {BLACK_DEEP}; border: 2px solid {BORDER_DARK}; border-radius: 4px;"
        )

    def get_background_pixmap(self, height=512):
        """Dark evil brushed metal with red undertones (seamlessly tileable)."""
        if SupervillainStyle._metal_cache is not None:
            return SupervillainStyle._metal_cache

        from scipy.ndimage import uniform_filter1d

        width = 256
        np.random.seed(666)  # Evil seed

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

        # Seamless dark metal noise
        noise = seamless_fractal_noise(height, width, octaves=3, persistence=0.5) * 25
        blurred = uniform_filter1d(noise, size=45, axis=1, mode='wrap')

        # Very dark with slight red tinge
        img = np.zeros((height, width, 4), dtype=np.uint8)
        base = np.clip(15 + blurred - 12, 8, 30).astype(np.float32)

        # Add slight red tint
        img[:, :, 0] = np.clip(base * 1.3, 10, 40).astype(np.uint8)  # R - slightly more
        img[:, :, 1] = np.clip(base * 0.9, 6, 28).astype(np.uint8)   # G - less
        img[:, :, 2] = np.clip(base * 1.0, 8, 32).astype(np.uint8)   # B - slight purple
        img[:, :, 3] = 255

        qimg = QImage(img.data, width, height, width * 4, QImage.Format.Format_RGBA8888).copy()
        SupervillainStyle._metal_cache = QPixmap.fromImage(qimg)
        return SupervillainStyle._metal_cache

    def _draw_vignette(self, painter, rect, width, height, radius=12):
        """DARK vignette - pure evil darkness at edges."""
        for horizontal, alpha_mult in [(True, 0.8), (False, 1.0)]:
            grad = QLinearGradient(0, 0, width if horizontal else 0, 0 if horizontal else height)
            # Heavy dark vignette
            for pos, alpha in [(0, 220), (0.1, 150), (0.25, 60), (0.75, 60), (0.9, 150), (1, 220)]:
                grad.setColorAt(pos, QColor(0, 0, 0, int(alpha * alpha_mult)))
            painter.setBrush(QBrush(grad))
            painter.setPen(Qt.PenStyle.NoPen)
            painter.drawRoundedRect(rect, radius, radius)

    def _draw_evil_glow(self, painter, rect, width, height, radius=12):
        """Red glow emanating from edges - sinister."""
        # Top edge red glow
        top_glow = QLinearGradient(0, 0, 0, 50)
        top_glow.setColorAt(0, QColor(255, 30, 30, 40))
        top_glow.setColorAt(1, QColor(255, 30, 30, 0))
        painter.setBrush(QBrush(top_glow))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawRoundedRect(QRectF(rect.x(), rect.y(), width, 50), radius, radius)

        # Bottom edge glow (like lava)
        bottom_glow = QLinearGradient(0, height - 40, 0, height)
        bottom_glow.setColorAt(0, QColor(255, 30, 30, 0))
        bottom_glow.setColorAt(1, QColor(255, 30, 30, 30))
        painter.setBrush(QBrush(bottom_glow))
        painter.drawRoundedRect(QRectF(rect.x(), rect.y() + height - 40, width, 40), radius, radius)

    def paint_window(self, painter, rect, width, height, focused=True):
        """Paint EVIL dark background with red glow."""
        radius = self.corner_radius

        # Clip to rounded rect
        path = QPainterPath()
        path.addRoundedRect(QRectF(rect), radius, radius)
        painter.setClipPath(path)

        # Draw evil dark metal
        metal = self.get_background_pixmap(max(512, height))
        painter.drawTiledPixmap(rect, metal)
        painter.setClipping(False)

        # Heavy dark vignette
        self._draw_vignette(painter, rect, width, height, radius)

        # Evil red glow when focused
        if focused:
            self._draw_evil_glow(painter, rect, width, height, radius)

        # Blood red border glow
        if focused:
            painter.setBrush(Qt.BrushStyle.NoBrush)
            painter.setPen(QPen(QColor(200, 30, 30, 120), 2))
            painter.drawRoundedRect(rect, radius, radius)
        else:
            painter.setBrush(Qt.BrushStyle.NoBrush)
            painter.setPen(QPen(QColor(80, 20, 25, 80), 1.5))
            painter.drawRoundedRect(rect, radius, radius)

    def paint_waveform_panel(self, painter, rect, w, h, cy):
        """Evil waveform panel - dark pit with red glow."""
        # Dark void gradient
        panel_grad = QLinearGradient(0, 0, 0, h)
        panel_grad.setColorAt(0, QColor(12, 8, 12))
        panel_grad.setColorAt(0.3, QColor(8, 5, 8))
        panel_grad.setColorAt(0.7, QColor(5, 3, 5))
        panel_grad.setColorAt(1, QColor(3, 2, 3))
        painter.setBrush(QBrush(panel_grad))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawRoundedRect(rect, 6, 6)

        # Red glow from top
        top_glow = QLinearGradient(0, 0, 0, h * 0.3)
        top_glow.setColorAt(0, QColor(255, 30, 30, 40))
        top_glow.setColorAt(1, QColor(255, 30, 30, 0))
        painter.setBrush(QBrush(top_glow))
        painter.drawRoundedRect(rect.adjusted(2, 2, -2, -int(h * 0.7)), 4, 4)

        # Deep inset shadows
        for grad, adj in [
            (QLinearGradient(0, 0, 0, 18), rect.adjusted(1, 1, -1, -h + 19)),
            (QLinearGradient(0, 0, 14, 0), rect.adjusted(1, 1, -w + 15, -1)),
            (QLinearGradient(w, 0, w - 14, 0), rect.adjusted(w - 15, 1, -1, -1)),
        ]:
            grad.setColorAt(0, QColor(0, 0, 0, 200))
            grad.setColorAt(1, QColor(0, 0, 0, 0))
            painter.setBrush(QBrush(grad))
            painter.setPen(Qt.PenStyle.NoPen)
            painter.drawRoundedRect(adj, 5, 5)

        # Subtle grid - blood red
        painter.setPen(QPen(QColor(255, 40, 40, 20), 1))
        for i in range(1, 4):
            y = int(h * i / 4)
            painter.drawLine(5, y, w - 5, y)

        # Evil border - blood red
        painter.setBrush(Qt.BrushStyle.NoBrush)
        painter.setPen(QPen(QColor(100, 20, 25), 2))
        painter.drawRoundedRect(rect, 6, 6)

        # Center line - blood red pulse
        painter.setPen(QPen(QColor(255, 40, 40, 100), 1))
        painter.drawLine(0, int(cy), w, int(cy))
