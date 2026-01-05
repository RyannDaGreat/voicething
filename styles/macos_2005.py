"""Mid-2000s macOS Aqua brushed metal style."""

import numpy as np
from PyQt6.QtCore import Qt, QRectF
from PyQt6.QtGui import QColor, QLinearGradient, QBrush, QImage, QPixmap, QPainterPath, QPen

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
        # Aqua gel button - smooth gradients with glassy highlights (no harsh white bar)
        return (
            f"QPushButton {{ color: {self.text_primary}; "
            f"background: qlineargradient(x1:0, y1:0, x2:0, y2:1, "
            f"stop:0 rgb(245,245,250), stop:0.15 rgb(235,235,242), "
            f"stop:0.42 rgb(218,218,228), stop:0.5 rgb(195,195,210), "
            f"stop:0.58 rgb(180,180,198), stop:0.85 rgb(200,200,215), "
            f"stop:1 rgb(210,210,222)); "
            f"border: 1px solid {AQUA_BORDER}; border-top-color: {AQUA_BORDER_TOP}; "
            f"border-bottom-color: {AQUA_BORDER_BOTTOM}; border-radius: 5px; "
            f"padding: 3px 8px; font-size: 11px; font-family: {self.font}; text-align: left; }}"
            "QPushButton:hover { background: qlineargradient(x1:0, y1:0, x2:0, y2:1, "
            "stop:0 rgb(240,248,255), stop:0.15 rgb(225,238,252), "
            "stop:0.42 rgb(200,225,248), stop:0.5 rgb(170,205,240), "
            "stop:0.58 rgb(150,190,235), stop:0.85 rgb(175,210,245), "
            "stop:1 rgb(195,220,250)); border: 1px solid rgb(100,140,185); }"
            "QPushButton:pressed { background: qlineargradient(x1:0, y1:0, x2:0, y2:1, "
            "stop:0 rgb(175,175,190), stop:0.42 rgb(160,160,178), "
            "stop:0.5 rgb(145,145,165), stop:0.58 rgb(155,155,175), "
            "stop:1 rgb(180,180,198)); border: 1px solid rgb(100,100,115); "
            "border-top-color: rgb(90,90,105); border-bottom-color: rgb(150,150,165); }"
            f"QPushButton:disabled {{ color: {TEXT_DISABLED}; background: qlineargradient(x1:0, y1:0, x2:0, y2:1, "
            "stop:0 rgb(235,235,238), stop:0.5 rgb(215,215,222), "
            "stop:1 rgb(225,225,230)); border: 1px solid rgb(165,165,175); }"
            f"QPushButton:checked {{ color: {WHITE}; background: qlineargradient(x1:0, y1:0, x2:0, y2:1, "
            "stop:0 rgb(160,205,255), stop:0.15 rgb(130,185,250), "
            "stop:0.42 rgb(90,155,235), stop:0.5 rgb(55,125,215), "
            "stop:0.58 rgb(45,115,205), stop:0.85 rgb(65,135,220), "
            "stop:1 rgb(85,150,230)); border: 1px solid rgb(30,75,145); "
            "border-top-color: rgb(90,155,215); border-bottom-color: rgb(20,60,125); }"
            "QPushButton:checked:hover { background: qlineargradient(x1:0, y1:0, x2:0, y2:1, "
            "stop:0 rgb(175,218,255), stop:0.15 rgb(145,198,252), "
            "stop:0.42 rgb(105,170,245), stop:0.5 rgb(70,140,228), "
            "stop:0.58 rgb(60,130,218), stop:0.85 rgb(80,148,232), "
            "stop:1 rgb(100,165,242)); }"
            "QPushButton:checked:pressed { background: qlineargradient(x1:0, y1:0, x2:0, y2:1, "
            "stop:0 rgb(45,105,185), stop:0.42 rgb(35,90,170), "
            "stop:0.5 rgb(30,80,160), stop:0.58 rgb(35,88,168), "
            "stop:1 rgb(55,115,190)); border: 1px solid rgb(20,55,115); }"
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
        # Authentic macOS Aqua scrollbar - glossy blue capsule pill, no arrows
        # Reference: Image 2 - white track, blue glossy cylindrical handle
        return (
            # Track - white capsule with very subtle gray border, fully rounded ends
            "QScrollBar:vertical { "
            "width: 14px; "
            "background: qlineargradient(x1:0, y1:0, x2:1, y2:0, "
            "stop:0 rgb(245,245,248), stop:0.3 rgb(255,255,255), "
            "stop:0.7 rgb(255,255,255), stop:1 rgb(245,245,248)); "
            "border: 1px solid rgb(190,190,195); "
            "border-radius: 7px; "
            "margin: 0px; }"
            # Handle - glossy blue Aqua capsule with cylindrical 3D gradient
            # Darker blue at edges, bright highlight in center (like a glass rod)
            "QScrollBar::handle:vertical { "
            "background: qlineargradient(x1:0, y1:0, x2:1, y2:0, "
            "stop:0.0 rgb(70,130,195), "
            "stop:0.08 rgb(95,160,220), "
            "stop:0.2 rgb(130,190,245), "
            "stop:0.35 rgb(160,210,255), "
            "stop:0.5 rgb(180,225,255), "
            "stop:0.65 rgb(160,210,255), "
            "stop:0.8 rgb(130,190,245), "
            "stop:0.92 rgb(95,160,220), "
            "stop:1.0 rgb(70,130,195)); "
            "border: 1px solid rgb(50,100,160); "
            "border-radius: 5px; "
            "min-height: 40px; "
            "margin: 2px; }"
            # Handle hover - brighter version
            "QScrollBar::handle:vertical:hover { "
            "background: qlineargradient(x1:0, y1:0, x2:1, y2:0, "
            "stop:0.0 rgb(80,145,210), "
            "stop:0.08 rgb(110,175,235), "
            "stop:0.2 rgb(145,205,255), "
            "stop:0.35 rgb(175,225,255), "
            "stop:0.5 rgb(200,240,255), "
            "stop:0.65 rgb(175,225,255), "
            "stop:0.8 rgb(145,205,255), "
            "stop:0.92 rgb(110,175,235), "
            "stop:1.0 rgb(80,145,210)); "
            "border: 1px solid rgb(40,90,150); }"
            # Handle pressed - darker version
            "QScrollBar::handle:vertical:pressed { "
            "background: qlineargradient(x1:0, y1:0, x2:1, y2:0, "
            "stop:0.0 rgb(55,110,170), "
            "stop:0.08 rgb(75,135,195), "
            "stop:0.2 rgb(105,165,220), "
            "stop:0.35 rgb(130,185,235), "
            "stop:0.5 rgb(150,200,245), "
            "stop:0.65 rgb(130,185,235), "
            "stop:0.8 rgb(105,165,220), "
            "stop:0.92 rgb(75,135,195), "
            "stop:1.0 rgb(55,110,170)); "
            "border: 1px solid rgb(35,75,130); }"
            # No arrow buttons - Aqua style uses only the pill
            "QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical { "
            "height: 0; width: 0; background: none; border: none; }"
            # Track areas - transparent
            "QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical { "
            "background: transparent; }"
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

    def paint_waveform_panel(self, painter, rect, w, h, cy):
        """Aqua-style blue panel background - classic macOS look."""
        panel_grad = QLinearGradient(0, 0, 0, h)
        panel_grad.setColorAt(0, QColor(140, 180, 220))
        panel_grad.setColorAt(0.3, QColor(80, 140, 200))
        panel_grad.setColorAt(0.7, QColor(50, 110, 180))
        panel_grad.setColorAt(1, QColor(30, 80, 150))
        painter.setBrush(QBrush(panel_grad))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawRoundedRect(rect, 8, 8)

        # Glassy top highlight
        highlight = QLinearGradient(0, 0, 0, h * 0.4)
        highlight.setColorAt(0, QColor(255, 255, 255, 120))
        highlight.setColorAt(0.5, QColor(255, 255, 255, 40))
        highlight.setColorAt(1, QColor(255, 255, 255, 0))
        painter.setBrush(QBrush(highlight))
        painter.drawRoundedRect(rect.adjusted(2, 2, -2, -int(h * 0.6)), 6, 6)

        # Infinite grid
        self._draw_infinite_grid(painter, w, h)

        # Engraved shadows
        for grad, adj in [
            (QLinearGradient(0, 0, 0, 12), rect.adjusted(1, 1, -1, -h + 14)),
            (QLinearGradient(0, 0, 10, 0), rect.adjusted(1, 1, -w + 12, -1)),
            (QLinearGradient(w, 0, w - 10, 0), rect.adjusted(w - 12, 1, -1, -1)),
        ]:
            grad.setColorAt(0, QColor(0, 0, 0, 50 if grad.start().x() else 100))
            grad.setColorAt(1, QColor(0, 0, 0, 0))
            painter.setBrush(QBrush(grad))
            painter.setPen(Qt.PenStyle.NoPen)
            painter.drawRoundedRect(adj, 7, 7)

        # Panel border
        painter.setBrush(Qt.BrushStyle.NoBrush)
        painter.setPen(QPen(QColor(20, 50, 100), 1.5))
        painter.drawRoundedRect(rect, 8, 8)

        # Center line
        painter.setPen(QPen(QColor(20, 60, 120, 150), 1))
        painter.drawLine(0, int(cy), w, int(cy))

    def _draw_infinite_grid(self, painter, w, h):
        """Draw a subtle grid over the panel."""
        painter.setPen(QPen(QColor(255, 255, 255, 15), 1))
        # Horizontal lines
        for i in range(1, 4):
            y = int(h * i / 4)
            painter.drawLine(0, y, w, y)
        # Vertical lines
        for i in range(1, 8):
            x = int(w * i / 8)
            painter.drawLine(x, 0, x, h)
