"""Windows 95 style - authentic beveled UI aesthetic.

Color reference from Windows 95 system colors:
- ButtonFace: #C0C0C0 (192,192,192)
- ButtonHighlight: #FFFFFF (255,255,255) - top/left bevel
- ButtonShadow: #808080 (128,128,128) - bottom/right inner bevel
- ButtonDkShadow: #000000 (0,0,0) - bottom/right outer bevel
- ButtonLight: #DFDFDF (223,223,223) - inner highlight
- Window: #FFFFFF (255,255,255)
- WindowText: #000000 (0,0,0)
- ActiveTitle: #000080 (0,0,128) - navy blue title bar
- TitleText: #FFFFFF (255,255,255)
"""

import os

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor, QLinearGradient, QBrush, QPen

from .base import BaseStyle

# Asset paths for scrollbar arrows
_STYLE_DIR = os.path.dirname(__file__)
_ASSETS_DIR = os.path.join(os.path.dirname(_STYLE_DIR), "assets")


# Windows 95 system colors (exact values)
WIN95_FACE = QColor(192, 192, 192)       # #C0C0C0 - ButtonFace
WIN95_HIGHLIGHT = QColor(255, 255, 255)  # #FFFFFF - top/left highlight
WIN95_LIGHT = QColor(223, 223, 223)      # #DFDFDF - inner highlight
WIN95_SHADOW = QColor(128, 128, 128)     # #808080 - inner shadow
WIN95_DARK = QColor(0, 0, 0)             # #000000 - outer shadow
WIN95_TITLE = QColor(0, 0, 128)          # #000080 - navy blue title bar

# CSS string versions
FACE_CSS = "rgb(192,192,192)"
HIGHLIGHT_CSS = "rgb(255,255,255)"
LIGHT_CSS = "rgb(223,223,223)"
SHADOW_CSS = "rgb(128,128,128)"
DARK_CSS = "rgb(0,0,0)"

# Text colors
TEXT_BLACK = "rgb(0,0,0)"
TEXT_WHITE = "rgb(255,255,255)"
TEXT_DISABLED = "rgb(128,128,128)"

# Waveform colors - classic green LCD
LCD_GREEN = QColor(0, 255, 0)            # #00FF00 - lime green
LCD_GREEN_DIM = QColor(0, 64, 0)         # #004000 - dim green for segments
LCD_BG = QColor(0, 0, 0)                 # Black background

# Panel background - slightly darker gray for recessed areas
PANEL_DARK = "rgb(64,64,64)"


class Windows95Style(BaseStyle):
    name = "windows_95"
    font = "MS Sans Serif"  # Authentic Win95 font (falls back to system sans)
    corner_radius = 0  # No rounded corners in Win95

    # Colors
    accent = LCD_GREEN
    text_primary = TEXT_BLACK
    text_secondary = TEXT_WHITE  # White for output panel (dark bg)
    text_muted = "rgb(80,80,80)"
    text_error = "rgb(255,0,0)"
    text_link = "rgb(0,0,128)"
    border_color = SHADOW_CSS
    border_dark = DARK_CSS
    icon_color_dark = '#000000'   # Black icons on gray bg
    icon_color_light = '#00ff00'  # Green for dark areas
    icon_color_muted = '#808080'  # Gray muted icons

    # Slider - dark groove on Win95 gray, green handle/fill
    slider_groove = "rgb(64,64,64)"
    slider_handle = "rgb(0,255,0)"
    slider_fill = "rgb(0,200,0)"

    # Rotary knob - classic Win95 beveled style
    knob_style = "win95"
    knob_body_dark = "#808080"
    knob_body_light = "#c0c0c0"
    knob_notch_style = "line"
    knob_tickmarks = True
    knob_glow = False

    # Waveform - green on black (classic Winamp/oscilloscope look)
    waveform_color = LCD_GREEN
    waveform_glow = True
    waveform_glow_radius = 12
    waveform_glow_alpha = 150
    waveform_center_line = QColor(0, 255, 0, 30)
    waveform_panel = "win95"  # Recessed black panel

    # Timer - LCD style with green 7-segment display
    timer_use_lcd = True
    timer_color = LCD_GREEN
    timer_font_size = 28
    timer_panel_size = (160, 40)

    # Transcription - dark recessed panel
    transcription_text = TEXT_WHITE
    transcription_text_dimmed = "rgba(255,255,255,0.6)"
    transcription_panel_bg = PANEL_DARK
    transcription_panel_border = DARK_CSS
    transcription_row_hover = "rgba(0,255,0,0.1)"
    transcription_row_btn_bg = "rgba(255,255,255,0.08)"
    transcription_row_btn_hover = "rgba(0,255,0,0.2)"
    transcription_row_btn_pressed = "rgba(0,255,0,0.35)"

    def button_css(self):
        # Authentic Windows 95 3D beveled button
        # Raised: white/light on top-left, shadow/dark on bottom-right
        # Pressed: inverted bevels (inset appearance)
        return (
            f"QPushButton {{ color: {TEXT_BLACK}; "
            f"background: {FACE_CSS}; "
            f"border: 2px solid; "
            f"border-top-color: {HIGHLIGHT_CSS}; "
            f"border-left-color: {HIGHLIGHT_CSS}; "
            f"border-bottom-color: {DARK_CSS}; "
            f"border-right-color: {DARK_CSS}; "
            f"border-radius: 0px; padding: 2px 8px; "
            f"font-size: 11px; font-family: {self.font}; text-align: left; }}"
            f"QPushButton:hover {{ "
            f"background: rgb(200,200,200); }}"
            f"QPushButton:pressed {{ "
            f"background: {FACE_CSS}; "
            f"border-top-color: {DARK_CSS}; "
            f"border-left-color: {DARK_CSS}; "
            f"border-bottom-color: {HIGHLIGHT_CSS}; "
            f"border-right-color: {HIGHLIGHT_CSS}; "
            f"padding-left: 10px; padding-top: 4px; }}"  # Shift content on press
            f"QPushButton:disabled {{ color: {TEXT_DISABLED}; "
            f"background: {FACE_CSS}; }}"
            f"QPushButton:checked {{ color: {TEXT_BLACK}; "
            f"background: rgb(180,180,180); "
            f"border-top-color: {DARK_CSS}; "
            f"border-left-color: {DARK_CSS}; "
            f"border-bottom-color: {HIGHLIGHT_CSS}; "
            f"border-right-color: {HIGHLIGHT_CSS}; }}"
            f"QPushButton:checked:hover {{ "
            f"background: rgb(170,170,170); }}"
        )

    def menu_css(self):
        return (
            f"QMenu {{ "
            f"background: {FACE_CSS}; "
            f"color: {TEXT_BLACK}; "
            f"border: 2px solid; "
            f"border-top-color: {HIGHLIGHT_CSS}; "
            f"border-left-color: {HIGHLIGHT_CSS}; "
            f"border-bottom-color: {DARK_CSS}; "
            f"border-right-color: {DARK_CSS}; "
            f"padding: 2px; font-family: {self.font}; }}"
            "QMenu::item { padding: 4px 20px; }"
            f"QMenu::item:selected {{ color: {TEXT_WHITE}; "
            f"background: rgb(0,0,128); }}"  # Navy blue selection
            f"QMenu::separator {{ height: 2px; "
            f"background: qlineargradient(x1:0, y1:0, x2:0, y2:1, "
            f"stop:0 {SHADOW_CSS}, stop:1 {HIGHLIGHT_CSS}); margin: 2px 2px; }}"
        )

    def scrollbar_css(self):
        # Authentic Windows 95 scrollbar - gray beveled, no rounded corners
        return (
            # Track - gray with inset bevel
            f"QScrollBar:vertical {{ "
            f"width: 16px; "
            f"background: {FACE_CSS}; "
            f"border: none; "
            f"margin: 16px 0 16px 0; }}"
            # Handle - raised gray button with 3D bevel
            f"QScrollBar::handle:vertical {{ "
            f"background: {FACE_CSS}; "
            f"border: 2px solid; "
            f"border-top-color: {HIGHLIGHT_CSS}; "
            f"border-left-color: {HIGHLIGHT_CSS}; "
            f"border-bottom-color: {DARK_CSS}; "
            f"border-right-color: {DARK_CSS}; "
            f"min-height: 20px; }}"
            f"QScrollBar::handle:vertical:hover {{ "
            f"background: rgb(200,200,200); }}"
            # Up arrow button - raised gray with bevel
            f"QScrollBar::sub-line:vertical {{ "
            f"height: 16px; "
            f"subcontrol-position: top; "
            f"subcontrol-origin: margin; "
            f"background: {FACE_CSS}; "
            f"border: 2px solid; "
            f"border-top-color: {HIGHLIGHT_CSS}; "
            f"border-left-color: {HIGHLIGHT_CSS}; "
            f"border-bottom-color: {DARK_CSS}; "
            f"border-right-color: {DARK_CSS}; }}"
            f"QScrollBar::sub-line:vertical:hover {{ background: rgb(200,200,200); }}"
            f"QScrollBar::sub-line:vertical:pressed {{ "
            f"border-top-color: {DARK_CSS}; "
            f"border-left-color: {DARK_CSS}; "
            f"border-bottom-color: {HIGHLIGHT_CSS}; "
            f"border-right-color: {HIGHLIGHT_CSS}; }}"
            # Down arrow button - raised gray with bevel
            f"QScrollBar::add-line:vertical {{ "
            f"height: 16px; "
            f"subcontrol-position: bottom; "
            f"subcontrol-origin: margin; "
            f"background: {FACE_CSS}; "
            f"border: 2px solid; "
            f"border-top-color: {HIGHLIGHT_CSS}; "
            f"border-left-color: {HIGHLIGHT_CSS}; "
            f"border-bottom-color: {DARK_CSS}; "
            f"border-right-color: {DARK_CSS}; }}"
            f"QScrollBar::add-line:vertical:hover {{ background: rgb(200,200,200); }}"
            f"QScrollBar::add-line:vertical:pressed {{ "
            f"border-top-color: {DARK_CSS}; "
            f"border-left-color: {DARK_CSS}; "
            f"border-bottom-color: {HIGHLIGHT_CSS}; "
            f"border-right-color: {HIGHLIGHT_CSS}; }}"
            # Arrow icons - use image-based arrows for authentic Win95 look
            # The CSS border trick doesn't work well in Qt, so use images
            f"QScrollBar::up-arrow:vertical {{ "
            f"image: url({os.path.join(_ASSETS_DIR, 'scroll-up.svg')}); "
            f"width: 8px; height: 4px; }}"
            f"QScrollBar::down-arrow:vertical {{ "
            f"image: url({os.path.join(_ASSETS_DIR, 'scroll-down.svg')}); "
            f"width: 8px; height: 4px; }}"
            # Track page areas - gray
            f"QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {{ "
            f"background: {FACE_CSS}; }}"
        )

    def panel_bg_css(self):
        # Raised panel (outset bevel)
        return (
            f"background: {FACE_CSS}; "
            f"border: 2px solid; "
            f"border-top-color: {HIGHLIGHT_CSS}; "
            f"border-left-color: {HIGHLIGHT_CSS}; "
            f"border-bottom-color: {DARK_CSS}; "
            f"border-right-color: {DARK_CSS};"
        )

    def panel_bg_flat_css(self):
        # Recessed panel (inset bevel) for display areas
        return (
            f"background: {PANEL_DARK}; "
            f"border: 2px solid; "
            f"border-top-color: {DARK_CSS}; "
            f"border-left-color: {DARK_CSS}; "
            f"border-bottom-color: {HIGHLIGHT_CSS}; "
            f"border-right-color: {HIGHLIGHT_CSS};"
        )

    def paint_window(self, painter, rect, width, height, focused=True):
        """Paint Windows 95 style background with beveled edges."""
        # No rounded corners
        alpha_mult = 1.0 if focused else 0.95

        # Main gray background
        painter.setBrush(QColor(192, 192, 192, int(255 * alpha_mult)))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawRect(rect)

        # Outer bevel - raised appearance
        # Top edge - white highlight
        painter.setPen(QPen(QColor(255, 255, 255, int(255 * alpha_mult)), 1))
        painter.drawLine(rect.left(), rect.top(), rect.right() - 1, rect.top())
        # Left edge - white highlight
        painter.drawLine(rect.left(), rect.top(), rect.left(), rect.bottom() - 1)

        # Inner highlight (second line)
        painter.setPen(QPen(QColor(223, 223, 223, int(255 * alpha_mult)), 1))
        painter.drawLine(rect.left() + 1, rect.top() + 1, rect.right() - 2, rect.top() + 1)
        painter.drawLine(rect.left() + 1, rect.top() + 1, rect.left() + 1, rect.bottom() - 2)

        # Bottom edge - dark shadow (outer)
        painter.setPen(QPen(QColor(0, 0, 0, int(255 * alpha_mult)), 1))
        painter.drawLine(rect.left(), rect.bottom(), rect.right(), rect.bottom())
        painter.drawLine(rect.right(), rect.top(), rect.right(), rect.bottom())

        # Inner shadow
        painter.setPen(QPen(QColor(128, 128, 128, int(255 * alpha_mult)), 1))
        painter.drawLine(rect.left() + 1, rect.bottom() - 1, rect.right() - 1, rect.bottom() - 1)
        painter.drawLine(rect.right() - 1, rect.top() + 1, rect.right() - 1, rect.bottom() - 1)

        # Focus indicator - subtle blue inner glow when focused
        if focused:
            painter.setPen(QPen(QColor(0, 0, 128, 40), 2))
            painter.setBrush(Qt.BrushStyle.NoBrush)
            painter.drawRect(rect.adjusted(3, 3, -3, -3))

    def paint_waveform_panel(self, painter, rect, w, h, cy):
        """Windows 95 style - black recessed panel with inset bevel."""
        # Black background
        painter.setBrush(QColor(0, 0, 0))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawRect(rect)

        # Inset bevel - dark on top/left, light on bottom/right
        # Top edge - dark shadow
        painter.setPen(QPen(QColor(0, 0, 0), 1))
        painter.drawLine(rect.left(), rect.top(), rect.right(), rect.top())
        # Left edge - dark shadow
        painter.drawLine(rect.left(), rect.top(), rect.left(), rect.bottom())

        # Inner dark gray
        painter.setPen(QPen(QColor(128, 128, 128), 1))
        painter.drawLine(rect.left() + 1, rect.top() + 1, rect.right() - 1, rect.top() + 1)
        painter.drawLine(rect.left() + 1, rect.top() + 1, rect.left() + 1, rect.bottom() - 1)

        # Bottom edge - white/light highlight
        painter.setPen(QPen(QColor(255, 255, 255), 1))
        painter.drawLine(rect.left(), rect.bottom(), rect.right(), rect.bottom())
        painter.drawLine(rect.right(), rect.top(), rect.right(), rect.bottom())

        # Inner light gray
        painter.setPen(QPen(QColor(223, 223, 223), 1))
        painter.drawLine(rect.left() + 1, rect.bottom() - 1, rect.right() - 1, rect.bottom() - 1)
        painter.drawLine(rect.right() - 1, rect.top() + 1, rect.right() - 1, rect.bottom() - 1)

        # Center line in dim green (optional subtle guide)
        painter.setPen(QPen(QColor(0, 64, 0, 60), 1))
        painter.drawLine(0, int(cy), w, int(cy))
