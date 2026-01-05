"""Mid-2000s macOS Aqua brushed metal style."""

import numpy as np
from PyQt6.QtCore import Qt, QRectF
from PyQt6.QtGui import QColor, QLinearGradient, QBrush, QImage, QPixmap, QPainterPath

from .base import BaseStyle, CYAN


# Aqua theme colors
GREEN_OSCILLOSCOPE = QColor(100, 255, 100)
WHITE = "rgb(255,255,255)"
NEAR_WHITE = "rgb(250,250,252)"
OFF_WHITE = "rgb(240,240,245)"
LIGHT_BLUE_BG = "rgb(235,235,240)"

# Text colors (dark on light)
TEXT_DARK = "rgb(60,60,70)"
TEXT_DARK_DIMMED = "rgba(80,90,100,0.8)"
TEXT_MENU = "rgb(30,30,35)"
TEXT_DISABLED = "rgb(140,140,148)"

# Borders
AQUA_BORDER = "rgb(140,140,152)"
AQUA_BORDER_TOP = "rgb(190,190,200)"
AQUA_BORDER_BOTTOM = "rgb(110,110,125)"
AQUA_BORDER_LIGHT = "rgb(160,160,170)"
AQUA_BORDER_DARK = "rgb(120,120,130)"
SCROLLBAR_BORDER = "rgb(140,140,150)"

# Button/scrollbar grays
BTN_GRAY_LIGHT = "rgb(225,225,230)"
BTN_GRAY_MID = "rgb(210,210,218)"
BTN_GRAY_DARK = "rgb(180,180,192)"
SCROLLBAR_BG = "rgb(220,220,225)"
SCROLLBAR_HANDLE = "rgb(200,200,205)"
SCROLLBAR_HANDLE_EDGE = "rgb(180,180,185)"

# Menu/selection blues
MENU_SEPARATOR = "rgb(200,200,205)"

# Subtle button bg for light theme
BTN_SUBTLE_BG = "rgba(0,0,0,0.06)"


class MacOS2005Style(BaseStyle):
    name = "macos_2005"
    font = "Futura"

    _metal_cache = None  # Class-level texture cache

    # Waveform - green oscilloscope with glow and Aqua panel
    waveform_color = GREEN_OSCILLOSCOPE
    waveform_glow = True
    waveform_center_line = None  # No center line with glow style
    waveform_panel = "aqua"  # Aqua-style blue panel background

    # Timer - LCD panel style
    timer_use_lcd = True
    timer_color = CYAN

    # Transcription - light background style
    transcription_text = TEXT_DARK
    transcription_text_dimmed = TEXT_DARK_DIMMED
    transcription_panel_bg = WHITE
    transcription_panel_border = AQUA_BORDER_LIGHT
    transcription_row_hover = (
        "qlineargradient(x1:0, y1:0, x2:0, y2:1, "
        "stop:0 rgb(230,240,250), stop:0.5 rgb(220,235,250), stop:1 rgb(230,240,250))"
    )
    transcription_row_btn_bg = BTN_SUBTLE_BG
    transcription_row_btn_hover = (
        "qlineargradient(x1:0, y1:0, x2:0, y2:1, "
        "stop:0 rgba(100,180,230,0.2), stop:1 rgba(80,150,200,0.15))"
    )
    transcription_row_btn_pressed = (
        "qlineargradient(x1:0, y1:0, x2:0, y2:1, "
        "stop:0 rgba(80,160,210,0.35), stop:1 rgba(100,200,255,0.4))"
    )

    def button_css(self):
        # Aqua "jelly" button with horizon line for 3D bulge (macOS allowed to have multi-color borders)
        return (
            f"QPushButton {{ color: {self.text_primary}; "
            f"background: qlineargradient(x1:0, y1:0, x2:0, y2:1, "
            f"stop:0 {WHITE}, stop:0.08 {NEAR_WHITE}, "
            f"stop:0.4 {BTN_GRAY_LIGHT}, stop:0.48 {BTN_GRAY_MID}, "
            f"stop:0.52 {BTN_GRAY_DARK}, stop:0.6 rgb(175,175,188), "
            f"stop:1 rgb(195,195,205)); "
            f"border: 1px solid {AQUA_BORDER}; border-top-color: {AQUA_BORDER_TOP}; "
            f"border-bottom-color: {AQUA_BORDER_BOTTOM}; border-radius: 5px; "
            f"padding: 3px 8px; font-size: 11px; font-family: {self.font}; text-align: left; }}"
            "QPushButton:hover { background: qlineargradient(x1:0, y1:0, x2:0, y2:1, "
            f"stop:0 {WHITE}, stop:0.08 rgb(252,252,255), stop:0.4 rgb(230,238,250), "
            "stop:0.48 rgb(215,225,242), stop:0.52 rgb(175,195,230), stop:0.6 rgb(170,192,228), "
            "stop:1 rgb(190,210,240)); border: 1px solid rgb(100,130,175); }"
            "QPushButton:pressed { background: qlineargradient(x1:0, y1:0, x2:0, y2:1, "
            "stop:0 rgb(190,190,200), stop:0.48 rgb(170,170,185), stop:0.52 rgb(160,160,175), "
            "stop:1 rgb(185,185,198)); border: 1px solid rgb(100,100,115); "
            "border-top-color: rgb(100,100,115); border-bottom-color: rgb(160,160,175); }"
            f"QPushButton:disabled {{ color: {TEXT_DISABLED}; background: qlineargradient(x1:0, y1:0, x2:0, y2:1, "
            "stop:0 rgb(235,235,238), stop:0.48 rgb(215,215,220), stop:0.52 rgb(200,200,208), "
            "stop:1 rgb(215,215,222)); border: 1px solid rgb(165,165,175); }"
            f"QPushButton:checked {{ color: {WHITE}; background: qlineargradient(x1:0, y1:0, x2:0, y2:1, "
            "stop:0 rgb(180,215,255), stop:0.08 rgb(160,200,250), stop:0.4 rgb(110,170,240), "
            "stop:0.48 rgb(90,150,230), stop:0.52 rgb(50,120,210), stop:0.6 rgb(45,115,205), "
            "stop:1 rgb(70,140,220)); border: 1px solid rgb(35,85,155); "
            "border-top-color: rgb(100,160,220); border-bottom-color: rgb(25,70,135); }"
            "QPushButton:checked:hover { background: qlineargradient(x1:0, y1:0, x2:0, y2:1, "
            "stop:0 rgb(195,225,255), stop:0.08 rgb(175,212,252), stop:0.4 rgb(125,185,248), "
            "stop:0.48 rgb(105,165,240), stop:0.52 rgb(65,135,220), stop:0.6 rgb(60,130,215), "
            "stop:1 rgb(85,155,230)); }"
            "QPushButton:checked:pressed { background: qlineargradient(x1:0, y1:0, x2:0, y2:1, "
            "stop:0 rgb(50,110,190), stop:0.48 rgb(40,100,180), stop:0.52 rgb(35,95,175), "
            "stop:1 rgb(60,120,195)); border: 1px solid rgb(25,65,125); }"
        )

    def menu_css(self):
        return (
            f"QMenu {{ background: qlineargradient(x1:0, y1:0, x2:0, y2:1, "
            f"stop:0 {NEAR_WHITE}, stop:1 rgb(230,230,235)); "
            f"color: {TEXT_MENU}; border: 1px solid {self.border_color}; "
            f"border-radius: 6px; padding: 4px; font-family: {self.font}; font-size: 12px; }}"
            "QMenu::item { padding: 4px 16px; border-radius: 4px; }"
            f"QMenu::item:selected {{ color: white; background: qlineargradient(x1:0, y1:0, x2:0, y2:1, "
            "stop:0 rgb(100,160,230), stop:0.5 rgb(60,130,210), stop:1 rgb(40,110,190)); }"
            f"QMenu::separator {{ height: 1px; background: {MENU_SEPARATOR}; margin: 4px 8px; }}"
        )

    def scrollbar_css(self):
        return (
            f"QScrollBar:vertical {{ width: 12px; background: {SCROLLBAR_BG}; margin: 2px; border-radius: 6px; }}"
            f"QScrollBar::handle:vertical {{ background: qlineargradient(x1:0, y1:0, x2:1, y2:0, "
            f"stop:0 {SCROLLBAR_HANDLE_EDGE}, stop:0.3 {SCROLLBAR_HANDLE}, stop:0.7 {SCROLLBAR_HANDLE}, "
            f"stop:1 {SCROLLBAR_HANDLE_EDGE}); border: 1px solid {SCROLLBAR_BORDER}; border-radius: 5px; min-height: 20px; }}"
            "QScrollBar::handle:vertical:hover { background: qlineargradient(x1:0, y1:0, x2:1, y2:0, "
            "stop:0 rgb(130,170,210), stop:0.5 rgb(160,200,240), stop:1 rgb(130,170,210)); "
            "border: 1px solid rgb(80,120,170); }"
            "QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical { height: 0; }"
            "QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical { background: transparent; }"
        )

    def panel_bg_css(self):
        # macOS allowed to have multi-color borders
        return (
            f"background: qlineargradient(x1:0, y1:0, x2:0, y2:1, "
            f"stop:0 {OFF_WHITE}, stop:0.02 {NEAR_WHITE}, "
            f"stop:0.98 {NEAR_WHITE}, stop:1 {LIGHT_BLUE_BG}); "
            f"border: 1px solid {self.border_color}; border-top-color: {AQUA_BORDER_DARK}; "
            f"border-bottom-color: {MENU_SEPARATOR}; border-radius: 6px;"
        )

    def panel_bg_flat_css(self):
        # macOS allowed to have multi-color borders
        return (
            f"background: {WHITE}; border: 1px solid {self.border_color}; "
            f"border-top-color: {AQUA_BORDER_DARK}; border-radius: 6px;"
        )

    def get_background_pixmap(self, height=512):
        """Brushed metal via noise + motion blur."""
        if MacOS2005Style._metal_cache is not None:
            return MacOS2005Style._metal_cache

        from scipy.ndimage import uniform_filter1d
        width = 256
        np.random.seed(42)
        noise = np.random.randint(0, 60, size=(height, width)).astype(np.float32)
        blurred = uniform_filter1d(noise, size=40, axis=1, mode='wrap')
        values = np.clip(168 + blurred - 30, 145, 195).astype(np.uint8)

        img = np.zeros((height, width, 4), dtype=np.uint8)
        img[:, :, :3] = values[:, :, None]
        img[:, :, 3] = 255

        qimg = QImage(img.data, width, height, width * 4, QImage.Format.Format_RGBA8888).copy()
        MacOS2005Style._metal_cache = QPixmap.fromImage(qimg)
        return MacOS2005Style._metal_cache

    def _draw_vignette(self, painter, rect, width, height, radius=12):
        """Dark edges, clear middle."""
        for horizontal, alpha_mult in [(True, 0.5), (False, 1.0)]:
            grad = QLinearGradient(0, 0, width if horizontal else 0, 0 if horizontal else height)
            for pos, alpha in [(0, 70), (0.08, 25), (0.15, 0), (0.85, 0), (0.92, 30), (1, 60)]:
                grad.setColorAt(pos, QColor(0, 0, 0, int(alpha * alpha_mult)))
            painter.setBrush(QBrush(grad))
            painter.setPen(Qt.PenStyle.NoPen)
            painter.drawRoundedRect(rect, radius, radius)

    def paint_window(self, painter, rect, width, height, focused=True):
        """Paint brushed metal background with vignette."""
        radius = self.corner_radius

        # Clip to rounded rect
        path = QPainterPath()
        path.addRoundedRect(QRectF(rect), radius, radius)
        painter.setClipPath(path)

        # Draw metal texture
        metal = self.get_background_pixmap(max(512, height))
        painter.drawTiledPixmap(rect, metal)
        painter.setClipping(False)

        # Vignette overlay
        self._draw_vignette(painter, rect, width, height, radius)
