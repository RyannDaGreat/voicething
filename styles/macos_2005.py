"""Mid-2000s macOS Aqua brushed metal style."""

import numpy as np
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor, QLinearGradient, QBrush, QImage, QPixmap

from .base import BaseStyle

class MacOS2005Style(BaseStyle):
    name = "macos_2005"
    font = "Futura"

    _metal_cache = None  # Class-level texture cache

    # Waveform - green oscilloscope with glow and Aqua panel
    waveform_color = QColor(100, 255, 100)
    waveform_glow = True
    waveform_center_line = None  # No center line with glow style
    waveform_panel = "aqua"  # Aqua-style blue panel background

    # Timer - LCD panel style
    timer_use_lcd = True
    timer_color = QColor(100, 200, 255)

    # Transcription - light background style
    transcription_text = "rgb(60,60,70)"
    transcription_text_dimmed = "rgba(80,90,100,0.8)"
    transcription_panel_bg = "rgb(255,255,255)"
    transcription_panel_border = "rgb(160,160,170)"
    transcription_row_hover = (
        "qlineargradient(x1:0, y1:0, x2:0, y2:1, "
        "stop:0 rgb(230,240,250), stop:0.5 rgb(220,235,250), stop:1 rgb(230,240,250))"
    )
    transcription_row_btn_hover = (
        "qlineargradient(x1:0, y1:0, x2:0, y2:1, "
        "stop:0 rgba(100,180,230,0.2), stop:1 rgba(80,150,200,0.15))"
    )
    transcription_row_btn_pressed = (
        "qlineargradient(x1:0, y1:0, x2:0, y2:1, "
        "stop:0 rgba(80,160,210,0.35), stop:1 rgba(100,200,255,0.4))"
    )

    def button_css(self):
        # Aqua "jelly" button with horizon line for 3D bulge
        return (
            f"QPushButton {{ color: {self.text_primary}; "
            f"background: qlineargradient(x1:0, y1:0, x2:0, y2:1, "
            f"stop:0 rgb(255,255,255), stop:0.08 rgb(250,250,252), "
            f"stop:0.4 rgb(225,225,230), stop:0.48 rgb(210,210,218), "
            f"stop:0.52 rgb(180,180,192), stop:0.6 rgb(175,175,188), "
            f"stop:1 rgb(195,195,205)); "
            f"border: 1px solid rgb(140,140,152); border-top-color: rgb(190,190,200); "
            f"border-bottom-color: rgb(110,110,125); border-radius: 5px; "
            f"padding: 3px 8px; font-size: 11px; font-family: {self.font}; text-align: left; }}"
            "QPushButton:hover { background: qlineargradient(x1:0, y1:0, x2:0, y2:1, "
            "stop:0 rgb(255,255,255), stop:0.08 rgb(252,252,255), stop:0.4 rgb(230,238,250), "
            "stop:0.48 rgb(215,225,242), stop:0.52 rgb(175,195,230), stop:0.6 rgb(170,192,228), "
            "stop:1 rgb(190,210,240)); border: 1px solid rgb(100,130,175); }"
            "QPushButton:pressed { background: qlineargradient(x1:0, y1:0, x2:0, y2:1, "
            "stop:0 rgb(190,190,200), stop:0.48 rgb(170,170,185), stop:0.52 rgb(160,160,175), "
            "stop:1 rgb(185,185,198)); border: 1px solid rgb(100,100,115); "
            "border-top-color: rgb(100,100,115); border-bottom-color: rgb(160,160,175); }"
            "QPushButton:disabled { color: rgb(140,140,148); background: qlineargradient(x1:0, y1:0, x2:0, y2:1, "
            "stop:0 rgb(235,235,238), stop:0.48 rgb(215,215,220), stop:0.52 rgb(200,200,208), "
            "stop:1 rgb(215,215,222)); border: 1px solid rgb(165,165,175); }"
            "QPushButton:checked { color: rgb(255,255,255); background: qlineargradient(x1:0, y1:0, x2:0, y2:1, "
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
            f"stop:0 rgb(250,250,252), stop:1 rgb(230,230,235)); "
            f"color: rgb(30,30,35); border: 1px solid {self.border_color}; "
            f"border-radius: 6px; padding: 4px; font-family: {self.font}; font-size: 12px; }}"
            "QMenu::item { padding: 4px 16px; border-radius: 4px; }"
            "QMenu::item:selected { color: white; background: qlineargradient(x1:0, y1:0, x2:0, y2:1, "
            "stop:0 rgb(100,160,230), stop:0.5 rgb(60,130,210), stop:1 rgb(40,110,190)); }"
            "QMenu::separator { height: 1px; background: rgb(200,200,205); margin: 4px 8px; }"
        )

    def scrollbar_css(self):
        return (
            "QScrollBar:vertical { width: 12px; background: rgb(220,220,225); margin: 2px; border-radius: 6px; }"
            "QScrollBar::handle:vertical { background: qlineargradient(x1:0, y1:0, x2:1, y2:0, "
            "stop:0 rgb(180,180,185), stop:0.3 rgb(200,200,205), stop:0.7 rgb(200,200,205), "
            "stop:1 rgb(180,180,185)); border: 1px solid rgb(140,140,150); border-radius: 5px; min-height: 20px; }"
            "QScrollBar::handle:vertical:hover { background: qlineargradient(x1:0, y1:0, x2:1, y2:0, "
            "stop:0 rgb(130,170,210), stop:0.5 rgb(160,200,240), stop:1 rgb(130,170,210)); "
            "border: 1px solid rgb(80,120,170); }"
            "QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical { height: 0; }"
            "QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical { background: transparent; }"
        )

    def panel_bg_css(self):
        return (
            "background: qlineargradient(x1:0, y1:0, x2:0, y2:1, "
            "stop:0 rgb(240,240,245), stop:0.02 rgb(250,250,252), "
            "stop:0.98 rgb(250,250,252), stop:1 rgb(235,235,240)); "
            f"border: 1px solid {self.border_color}; border-top-color: rgb(120,120,130); "
            "border-bottom-color: rgb(200,200,205); border-radius: 6px;"
        )

    def panel_bg_flat_css(self):
        return (
            f"background: rgb(255,255,255); border: 1px solid {self.border_color}; "
            "border-top-color: rgb(120,120,130); border-radius: 6px;"
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
        from PyQt6.QtGui import QPainterPath
        from PyQt6.QtCore import QRectF
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
