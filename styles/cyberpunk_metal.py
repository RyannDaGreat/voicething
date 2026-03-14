"""Cyberpunk brushed metal style - 'Evil Mac OS' dark mode with cyan glow."""

import numpy as np
from PyQt6.QtCore import Qt, QRectF
from PyQt6.QtGui import QColor, QLinearGradient, QBrush, QImage, QPixmap, QPainterPath, QPen

from .base import BaseStyle


# Cyberpunk colors
CYAN = QColor(0, 255, 255)  # Pure cyberpunk cyan
CYAN_CSS = "rgb(0,255,255)"
CYAN_GLOW = "rgba(0,255,255,0.4)"
CYAN_DARK = "rgb(0,180,180)"
CYAN_MUTED = "rgba(0,200,200,0.7)"

# Dark base colors
BLACK = "rgb(15,15,20)"
NEAR_BLACK = "rgb(20,22,28)"
DARK_GRAY = "rgb(35,38,45)"
MID_GRAY = "rgb(60,65,75)"
LIGHT_GRAY = "rgb(120,125,135)"

# Text colors (light on dark)
TEXT_BRIGHT = "rgb(230,235,245)"
TEXT_DIM = "rgba(180,185,195,0.85)"
TEXT_DISABLED = "rgb(80,85,95)"

# Borders - darker with subtle cyan tint
BORDER_DARK = "rgb(40,45,55)"
BORDER_MID = "rgb(55,60,70)"
BORDER_LIGHT = "rgb(70,75,85)"

# Button grays with cyan undertone
BTN_DARK = "rgb(30,35,42)"
BTN_MID = "rgb(45,50,58)"
BTN_LIGHT = "rgb(60,65,75)"


class CyberpunkMetalStyle(BaseStyle):
    name = "cyberpunk_metal"
    font = "Futura"

    _metal_cache = None  # Class-level dark metal texture cache

    # Dark theme colors
    accent = CYAN
    accent_css = CYAN_CSS
    text_primary = TEXT_BRIGHT
    text_secondary = TEXT_DIM
    text_muted = LIGHT_GRAY
    text_error = "rgb(255,80,100)"
    text_link = CYAN_CSS
    border_color = BORDER_MID
    border_dark = BORDER_DARK
    icon_color_dark = '#00ffff'  # Cyan icons
    icon_color_light = '#00ffff'
    icon_color_muted = '#008888'

    # Dropdown input fields - dark metal to match theme
    input_bg = '#0f1218'
    input_text = '#c0e8ff'

    # Slider - bright cyan groove on dark metal
    slider_groove = "rgba(0,255,255,0.3)"

    # Rotary knob - cyberpunk style with cyan glow
    knob_style = "cyber"
    knob_body_dark = "#101820"
    knob_body_light = "#203040"
    knob_notch_style = "line"
    knob_tickmarks = True
    knob_glow = True
    knob_track_color = "#00ffff"  # Cyan track
    knob_label_color = "#80ffff"  # Cyan text

    # Waveform - cyan oscilloscope with glow
    waveform_color = CYAN
    waveform_glow = True
    waveform_center_line = QColor(0, 255, 255, 60)
    waveform_panel = "dark"

    # Timer - cyan LCD
    timer_use_lcd = True
    timer_color = CYAN

    # Transcription - dark panel
    transcription_text = TEXT_BRIGHT
    transcription_text_dimmed = CYAN_MUTED
    transcription_panel_bg = NEAR_BLACK
    transcription_panel_border = BORDER_DARK
    transcription_row_hover = "rgba(0,255,255,0.08)"
    transcription_row_btn_bg = "rgba(0,255,255,0.1)"
    transcription_row_btn_hover = "rgba(0,255,255,0.2)"
    transcription_row_btn_pressed = "rgba(0,255,255,0.35)"

    # Chime editor - dark metal with cyan glow
    chime_grid_bg = QColor(20, 22, 28)  # Near black
    chime_grid_line = QColor(40, 45, 55)  # Dark border
    chime_cell_inactive = QColor(30, 35, 42)  # Dark button color
    chime_cell_active = QColor(0, 255, 255)  # Pure cyan
    chime_cell_highlight = QColor(0, 255, 255, 80)  # Cyan glow
    chime_piano_white = QColor(180, 185, 195)  # Light metal gray
    chime_piano_black = QColor(25, 28, 35)  # Dark metal
    chime_piano_label_white = QColor(35, 38, 45)  # Dark text on light
    chime_piano_label_black = QColor(0, 200, 200)  # Cyan text on dark

    def button_css(self):
        # Dark buttons with cyan glow on hover
        return (
            f"QPushButton {{ color: {TEXT_DIM}; "
            f"background: qlineargradient(x1:0, y1:0, x2:0, y2:1, "
            f"stop:0 {BTN_LIGHT}, stop:0.4 {BTN_MID}, stop:0.6 {BTN_DARK}, stop:1 {BTN_MID}); "
            f"border: 1px solid {BORDER_DARK}; border-top-color: {BORDER_LIGHT}; "
            f"border-radius: 5px; padding: 3px 8px; font-size: 11px; font-family: {self.font}; text-align: left; }}"
            # Hover: cyan glow
            f"QPushButton:hover {{ color: {CYAN_CSS}; "
            f"background: qlineargradient(x1:0, y1:0, x2:0, y2:1, "
            f"stop:0 rgb(50,70,80), stop:0.4 rgb(35,55,65), stop:0.6 rgb(25,45,55), stop:1 rgb(35,55,65)); "
            f"border: 1px solid rgb(0,180,180); }}"
            # Pressed: deeper cyan
            f"QPushButton:pressed {{ color: {TEXT_BRIGHT}; "
            f"background: qlineargradient(x1:0, y1:0, x2:0, y2:1, "
            f"stop:0 rgb(20,40,50), stop:0.4 rgb(15,35,45), stop:0.6 rgb(10,30,40), stop:1 rgb(15,35,45)); "
            f"border: 1px solid rgb(0,150,150); }}"
            # Disabled
            f"QPushButton:disabled {{ color: {TEXT_DISABLED}; "
            f"background: {BTN_DARK}; border: 1px solid {BORDER_DARK}; }}"
            # Checked: cyan active state
            f"QPushButton:checked {{ color: {TEXT_BRIGHT}; "
            f"background: qlineargradient(x1:0, y1:0, x2:0, y2:1, "
            f"stop:0 rgb(0,100,100), stop:0.4 rgb(0,80,80), stop:0.6 rgb(0,60,60), stop:1 rgb(0,80,80)); "
            f"border: 1px solid {CYAN_CSS}; }}"
            f"QPushButton:checked:hover {{ "
            f"background: qlineargradient(x1:0, y1:0, x2:0, y2:1, "
            f"stop:0 rgb(0,120,120), stop:0.4 rgb(0,100,100), stop:0.6 rgb(0,80,80), stop:1 rgb(0,100,100)); }}"
        )

    def menu_css(self):
        return (
            f"QMenu {{ background: {NEAR_BLACK}; color: {TEXT_BRIGHT}; "
            f"border: 1px solid {BORDER_MID}; border-radius: 6px; padding: 4px; "
            f"font-family: {self.font}; font-size: 12px; }}"
            "QMenu::item { padding: 4px 16px; border-radius: 4px; }"
            f"QMenu::item:selected {{ color: {TEXT_BRIGHT}; "
            f"background: qlineargradient(x1:0, y1:0, x2:0, y2:1, "
            f"stop:0 rgb(0,100,100), stop:0.5 rgb(0,80,80), stop:1 rgb(0,60,60)); }}"
            f"QMenu::separator {{ height: 1px; background: {BORDER_DARK}; margin: 4px 8px; }}"
        )

    def _scrollbar_vertical_css(self):
        # Dark scrollbar with cyan handle
        return (
            f"QScrollBar:vertical {{ width: 14px; background: {DARK_GRAY}; "
            f"border: 1px solid {BORDER_DARK}; border-radius: 7px; margin: 0px; }}"
            # Handle - dark with cyan tint
            "QScrollBar::handle:vertical { "
            "background: qlineargradient(x1:0, y1:0, x2:1, y2:0, "
            "stop:0.0 rgb(0,80,80), stop:0.2 rgb(0,100,100), "
            "stop:0.5 rgb(0,120,120), stop:0.8 rgb(0,100,100), stop:1.0 rgb(0,80,80)); "
            f"border: 1px solid rgb(0,60,60); border-radius: 5px; min-height: 40px; margin: 2px; }}"
            # Handle hover - brighter cyan
            "QScrollBar::handle:vertical:hover { "
            "background: qlineargradient(x1:0, y1:0, x2:1, y2:0, "
            "stop:0.0 rgb(0,120,120), stop:0.2 rgb(0,150,150), "
            "stop:0.5 rgb(0,180,180), stop:0.8 rgb(0,150,150), stop:1.0 rgb(0,120,120)); "
            "border: 1px solid rgb(0,100,100); }"
            # Handle pressed
            "QScrollBar::handle:vertical:pressed { "
            "background: qlineargradient(x1:0, y1:0, x2:1, y2:0, "
            "stop:0.0 rgb(0,60,60), stop:0.2 rgb(0,80,80), "
            "stop:0.5 rgb(0,100,100), stop:0.8 rgb(0,80,80), stop:1.0 rgb(0,60,60)); "
            "border: 1px solid rgb(0,50,50); }"
            "QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical { "
            "height: 0; width: 0; background: none; border: none; }"
            "QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical { background: transparent; }"
        )

    def panel_bg_css(self):
        return (
            f"background: qlineargradient(x1:0, y1:0, x2:0, y2:1, "
            f"stop:0 {DARK_GRAY}, stop:0.02 {NEAR_BLACK}, "
            f"stop:0.98 {NEAR_BLACK}, stop:1 {BLACK}); "
            f"border: 1px solid {BORDER_DARK}; border-radius: 6px;"
        )

    def panel_bg_flat_css(self):
        return (
            f"background: {NEAR_BLACK}; border: 1px solid {BORDER_DARK}; border-radius: 6px;"
        )

    def get_background_pixmap(self, height=512):
        """Dark brushed metal via noise + motion blur."""
        if CyberpunkMetalStyle._metal_cache is not None:
            return CyberpunkMetalStyle._metal_cache

        from scipy.ndimage import uniform_filter1d
        width = 256
        np.random.seed(42)
        noise = np.random.randint(0, 40, size=(height, width)).astype(np.float32)
        blurred = uniform_filter1d(noise, size=40, axis=1, mode='wrap')
        # Dark metal: base around 35-55 (much darker than light metal's 145-195)
        values = np.clip(35 + blurred - 20, 25, 55).astype(np.uint8)

        img = np.zeros((height, width, 4), dtype=np.uint8)
        img[:, :, :3] = values[:, :, None]
        img[:, :, 3] = 255

        qimg = QImage(img.data, width, height, width * 4, QImage.Format.Format_RGBA8888).copy()
        CyberpunkMetalStyle._metal_cache = QPixmap.fromImage(qimg)
        return CyberpunkMetalStyle._metal_cache

    def _draw_vignette(self, painter, rect, width, height, radius=12):
        """Dark edges with cyan hint at center."""
        for horizontal, alpha_mult in [(True, 0.6), (False, 1.0)]:
            grad = QLinearGradient(0, 0, width if horizontal else 0, 0 if horizontal else height)
            # Darker vignette than light theme
            for pos, alpha in [(0, 120), (0.1, 60), (0.2, 20), (0.8, 20), (0.9, 60), (1, 120)]:
                grad.setColorAt(pos, QColor(0, 0, 0, int(alpha * alpha_mult)))
            painter.setBrush(QBrush(grad))
            painter.setPen(Qt.PenStyle.NoPen)
            painter.drawRoundedRect(rect, radius, radius)

    def _draw_cyan_edge_glow(self, painter, rect, width, height, radius=12):
        """Subtle cyan glow at edges - cyberpunk accent."""
        # Top edge cyan glow
        top_glow = QLinearGradient(0, 0, 0, 30)
        top_glow.setColorAt(0, QColor(0, 255, 255, 25))
        top_glow.setColorAt(1, QColor(0, 255, 255, 0))
        painter.setBrush(QBrush(top_glow))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawRoundedRect(QRectF(rect.x(), rect.y(), width, 30), radius, radius)

    def paint_window(self, painter, rect, width, height, focused=True):
        """Paint dark brushed metal background with cyan accents."""
        radius = self.corner_radius

        # Clip to rounded rect
        path = QPainterPath()
        path.addRoundedRect(QRectF(rect), radius, radius)
        painter.setClipPath(path)

        # Draw dark metal texture
        metal = self.get_background_pixmap(max(512, height))
        painter.drawTiledPixmap(rect, metal)
        painter.setClipping(False)

        # Dark vignette overlay
        self._draw_vignette(painter, rect, width, height, radius)

        # Cyan edge glow when focused
        if focused:
            self._draw_cyan_edge_glow(painter, rect, width, height, radius)

        # Cyan border glow when focused
        if focused:
            painter.setBrush(Qt.BrushStyle.NoBrush)
            painter.setPen(QPen(QColor(0, 255, 255, 80), 1.5))
            painter.drawRoundedRect(rect, radius, radius)

    def paint_waveform_panel(self, painter, rect, w, h, cy):
        """Dark panel with cyan accents - industrial look."""
        # Dark gradient background
        panel_grad = QLinearGradient(0, 0, 0, h)
        panel_grad.setColorAt(0, QColor(15, 25, 30))
        panel_grad.setColorAt(0.3, QColor(10, 20, 25))
        panel_grad.setColorAt(0.7, QColor(8, 15, 20))
        panel_grad.setColorAt(1, QColor(5, 12, 15))
        painter.setBrush(QBrush(panel_grad))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawRoundedRect(rect, 8, 8)

        # Subtle top highlight (industrial)
        highlight = QLinearGradient(0, 0, 0, h * 0.15)
        highlight.setColorAt(0, QColor(0, 255, 255, 30))
        highlight.setColorAt(1, QColor(0, 255, 255, 0))
        painter.setBrush(QBrush(highlight))
        painter.drawRoundedRect(rect.adjusted(2, 2, -2, -int(h * 0.85)), 6, 6)

        # Grid lines - cyan tinted
        self._draw_cyber_grid(painter, w, h)

        # Engraved shadows (deeper than light theme)
        for grad, adj in [
            (QLinearGradient(0, 0, 0, 12), rect.adjusted(1, 1, -1, -h + 14)),
            (QLinearGradient(0, 0, 10, 0), rect.adjusted(1, 1, -w + 12, -1)),
            (QLinearGradient(w, 0, w - 10, 0), rect.adjusted(w - 12, 1, -1, -1)),
        ]:
            grad.setColorAt(0, QColor(0, 0, 0, 150))
            grad.setColorAt(1, QColor(0, 0, 0, 0))
            painter.setBrush(QBrush(grad))
            painter.setPen(Qt.PenStyle.NoPen)
            painter.drawRoundedRect(adj, 7, 7)

        # Panel border - cyan tinted
        painter.setBrush(Qt.BrushStyle.NoBrush)
        painter.setPen(QPen(QColor(0, 80, 80), 1.5))
        painter.drawRoundedRect(rect, 8, 8)

        # Center line - cyan
        painter.setPen(QPen(QColor(0, 255, 255, 80), 1))
        painter.drawLine(0, int(cy), w, int(cy))

    def _draw_cyber_grid(self, painter, w, h):
        """Draw a subtle cyan grid over the panel."""
        painter.setPen(QPen(QColor(0, 255, 255, 20), 1))
        # Horizontal lines
        for i in range(1, 4):
            y = int(h * i / 4)
            painter.drawLine(0, y, w, y)
        # Vertical lines
        for i in range(1, 8):
            x = int(w * i / 8)
            painter.drawLine(x, 0, x, h)
