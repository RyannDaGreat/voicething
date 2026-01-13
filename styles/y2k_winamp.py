"""Y2K/Vaporwave/Winamp style - retro-futuristic aesthetic."""

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor, QLinearGradient, QBrush, QPen

from .base import BaseStyle


# Winamp classic colors
WINAMP_GREEN = QColor(0, 255, 0)        # #00FF00 - lime green waveform
WINAMP_DARK = QColor(26, 26, 26)        # #1a1a1a - deep dark background
WINAMP_DARKER = QColor(18, 18, 18)      # #121212 - even darker

# Windows 95 system colors
WIN95_FACE = "rgb(192,192,192)"         # #C0C0C0 - ButtonFace
WIN95_HIGHLIGHT = "rgb(255,255,255)"    # #FFFFFF - top/left bevel
WIN95_SHADOW = "rgb(128,128,128)"       # #808080 - bottom/right bevel
WIN95_DARK_SHADOW = "rgb(0,0,0)"        # #000000 - deep shadow

# Vaporwave colors
VAPOR_PINK = "rgb(255,113,206)"         # #FF71CE - hot pink
VAPOR_CYAN = "rgb(1,205,254)"           # #01CDFE - cyan/aqua
VAPOR_PURPLE = "rgb(185,103,255)"       # #B967FF - purple
VAPOR_MINT = "rgb(5,255,161)"           # #05FFA1 - mint green

# Y2K metallic
Y2K_CHROME = "rgb(192,192,192)"         # #C0C0C0 - chrome base
Y2K_SILVER = "rgb(232,232,232)"         # #E8E8E8 - bright silver
Y2K_GOLD = "rgb(255,215,0)"             # #FFD700 - gold accents

# Text colors
TEXT_LIGHT = "rgb(255,255,255)"
TEXT_GOLD = "rgb(255,215,0)"
TEXT_GREEN = "rgb(0,255,0)"
TEXT_DARK = "rgb(0,0,0)"
TEXT_DISABLED = "rgb(100,100,100)"

# Panel colors
PANEL_DARK = "rgb(26,26,26)"            # Winamp dark
PANEL_MID = "rgb(51,51,51)"             # #333333


class Y2KWinampStyle(BaseStyle):
    name = "y2k_winamp"
    font = "Verdana"  # Era-appropriate font

    # Colors
    accent = WINAMP_GREEN
    accent_css = "rgb(0,255,0)"
    text_primary = TEXT_LIGHT
    text_secondary = "rgba(255,255,255,0.8)"
    text_muted = "rgba(255,255,255,0.5)"
    text_error = VAPOR_PINK
    text_link = VAPOR_CYAN
    border_color = WIN95_SHADOW
    border_dark = WIN95_DARK_SHADOW
    icon_color_dark = '#00ff00'   # Lime green icons
    icon_color_light = '#ffffff'
    icon_color_muted = '#00cc00'  # Slightly darker green

    # Slider - lime green groove on dark Winamp panel
    slider_groove = "rgba(0,255,0,0.25)"

    # Waveform - classic Winamp lime green on dark
    waveform_color = WINAMP_GREEN
    waveform_glow = True
    waveform_center_line = QColor(0, 255, 0, 30)
    waveform_panel = "winamp"  # New panel type - dark with subtle grid

    # Timer - LCD style with green
    timer_use_lcd = True
    timer_color = WINAMP_GREEN

    # Transcription - dark panel with vaporwave accents
    transcription_text = TEXT_LIGHT
    transcription_text_dimmed = "rgba(255,255,255,0.6)"
    transcription_panel_bg = PANEL_DARK
    transcription_panel_border = WIN95_SHADOW
    transcription_row_hover = "rgba(1,205,254,0.1)"  # Cyan hover
    transcription_row_btn_bg = "rgba(255,255,255,0.08)"
    transcription_row_btn_hover = "rgba(0,255,0,0.2)"  # Green hover
    transcription_row_btn_pressed = "rgba(0,255,0,0.35)"

    def button_css(self):
        # Windows 95 beveled button with Y2K metallic gradient
        return (
            f"QPushButton {{ color: {TEXT_DARK}; "
            f"background: qlineargradient(x1:0, y1:0, x2:0, y2:1, "
            f"stop:0 {Y2K_SILVER}, stop:0.5 {Y2K_CHROME}, stop:1 rgb(160,160,160)); "
            f"border: 2px outset {Y2K_CHROME}; "
            f"border-top-color: {WIN95_HIGHLIGHT}; border-left-color: {WIN95_HIGHLIGHT}; "
            f"border-bottom-color: {WIN95_SHADOW}; border-right-color: {WIN95_SHADOW}; "
            f"border-radius: 0px; padding: 3px 8px; font-size: 11px; font-family: {self.font}; text-align: left; }}"
            f"QPushButton:hover {{ "
            f"background: qlineargradient(x1:0, y1:0, x2:0, y2:1, "
            f"stop:0 rgb(245,245,245), stop:0.5 {Y2K_SILVER}, stop:1 {Y2K_CHROME}); }}"
            f"QPushButton:pressed {{ "
            f"background: qlineargradient(x1:0, y1:0, x2:0, y2:1, "
            f"stop:0 rgb(160,160,160), stop:0.5 {Y2K_CHROME}, stop:1 {Y2K_SILVER}); "
            f"border: 2px inset {Y2K_CHROME}; "
            f"border-top-color: {WIN95_SHADOW}; border-left-color: {WIN95_SHADOW}; "
            f"border-bottom-color: {WIN95_HIGHLIGHT}; border-right-color: {WIN95_HIGHLIGHT}; }}"
            f"QPushButton:disabled {{ color: {TEXT_DISABLED}; "
            f"background: rgb(200,200,200); border: 2px outset rgb(180,180,180); }}"
            f"QPushButton:checked {{ color: {TEXT_LIGHT}; "
            f"background: qlineargradient(x1:0, y1:0, x2:0, y2:1, "
            f"stop:0 rgb(0,180,0), stop:0.5 rgb(0,220,0), stop:1 rgb(0,180,0)); "
            f"border: 2px inset rgb(0,150,0); "
            f"border-top-color: rgb(0,100,0); border-left-color: rgb(0,100,0); "
            f"border-bottom-color: rgb(0,255,0); border-right-color: rgb(0,255,0); }}"
            f"QPushButton:checked:hover {{ "
            f"background: qlineargradient(x1:0, y1:0, x2:0, y2:1, "
            f"stop:0 rgb(0,200,0), stop:0.5 rgb(0,255,0), stop:1 rgb(0,200,0)); }}"
        )

    def menu_css(self):
        return (
            f"QMenu {{ "
            f"background: {WIN95_FACE}; "
            f"color: {TEXT_DARK}; "
            f"border: 2px outset {Y2K_CHROME}; "
            f"border-top-color: {WIN95_HIGHLIGHT}; border-left-color: {WIN95_HIGHLIGHT}; "
            f"border-bottom-color: {WIN95_SHADOW}; border-right-color: {WIN95_SHADOW}; "
            f"padding: 2px; font-family: {self.font}; }}"
            "QMenu::item { padding: 4px 20px; }"
            f"QMenu::item:selected {{ color: {TEXT_LIGHT}; "
            f"background: qlineargradient(x1:0, y1:0, x2:1, y2:0, "
            f"stop:0 {VAPOR_CYAN}, stop:1 {VAPOR_PURPLE}); }}"
            f"QMenu::separator {{ height: 2px; "
            f"background: qlineargradient(x1:0, y1:0, x2:0, y2:1, "
            f"stop:0 {WIN95_SHADOW}, stop:1 {WIN95_HIGHLIGHT}); margin: 2px 4px; }}"
        )

    def scrollbar_css(self):
        return (
            f"QScrollBar:vertical {{ width: 16px; background: {WIN95_FACE}; margin: 0; "
            f"border: 1px solid {WIN95_SHADOW}; }}"
            f"QScrollBar::handle:vertical {{ "
            f"background: qlineargradient(x1:0, y1:0, x2:1, y2:0, "
            f"stop:0 {Y2K_SILVER}, stop:0.5 {Y2K_CHROME}, stop:1 rgb(160,160,160)); "
            f"border: 2px outset {Y2K_CHROME}; "
            f"border-top-color: {WIN95_HIGHLIGHT}; border-left-color: {WIN95_HIGHLIGHT}; "
            f"border-bottom-color: {WIN95_SHADOW}; border-right-color: {WIN95_SHADOW}; "
            f"min-height: 20px; }}"
            f"QScrollBar::handle:vertical:hover {{ "
            f"background: qlineargradient(x1:0, y1:0, x2:1, y2:0, "
            f"stop:0 rgb(1,205,254), stop:0.5 rgb(100,220,250), stop:1 rgb(1,180,230)); }}"
            f"QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{ height: 16px; "
            f"background: {WIN95_FACE}; border: 2px outset {Y2K_CHROME}; "
            f"border-top-color: {WIN95_HIGHLIGHT}; border-left-color: {WIN95_HIGHLIGHT}; "
            f"border-bottom-color: {WIN95_SHADOW}; border-right-color: {WIN95_SHADOW}; }}"
            "QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical { background: transparent; }"
        )

    def panel_bg_css(self):
        return (
            f"background: {WIN95_FACE}; "
            f"border: 2px inset {Y2K_CHROME}; "
            f"border-top-color: {WIN95_SHADOW}; border-left-color: {WIN95_SHADOW}; "
            f"border-bottom-color: {WIN95_HIGHLIGHT}; border-right-color: {WIN95_HIGHLIGHT};"
        )

    def panel_bg_flat_css(self):
        return (
            f"background: {PANEL_DARK}; "
            f"border: 2px inset rgb(60,60,60); "
            f"border-top-color: rgb(40,40,40); border-left-color: rgb(40,40,40); "
            f"border-bottom-color: rgb(80,80,80); border-right-color: rgb(80,80,80);"
        )

    def paint_window(self, painter, rect, width, height, focused=True):
        """Paint Windows 95 style background with vaporwave gradient overlay."""
        radius = 0  # No rounded corners for Win95 style
        alpha_mult = 1.0 if focused else 0.9

        # Base Win95 gray
        painter.setBrush(QColor(192, 192, 192, int(255 * alpha_mult)))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawRect(rect)

        # Subtle vaporwave gradient overlay at bottom
        overlay_rect = rect.adjusted(0, int(height * 0.7), 0, 0)
        vapor_grad = QLinearGradient(0, overlay_rect.top(), 0, overlay_rect.bottom())
        vapor_grad.setColorAt(0, QColor(1, 205, 254, 0))  # Transparent at top
        vapor_grad.setColorAt(0.5, QColor(185, 103, 255, int(30 * alpha_mult)))  # Purple
        vapor_grad.setColorAt(1, QColor(255, 113, 206, int(50 * alpha_mult)))  # Pink
        painter.setBrush(QBrush(vapor_grad))
        painter.drawRect(overlay_rect)

        # Win95 beveled border
        # Top/left highlight
        painter.setPen(QPen(QColor(255, 255, 255, int(255 * alpha_mult)), 2))
        painter.drawLine(rect.left(), rect.top(), rect.right(), rect.top())
        painter.drawLine(rect.left(), rect.top(), rect.left(), rect.bottom())

        # Bottom/right shadow
        painter.setPen(QPen(QColor(128, 128, 128, int(255 * alpha_mult)), 2))
        painter.drawLine(rect.right(), rect.top(), rect.right(), rect.bottom())
        painter.drawLine(rect.left(), rect.bottom(), rect.right(), rect.bottom())

        # Inner dark shadow
        painter.setPen(QPen(QColor(0, 0, 0, int(180 * alpha_mult)), 1))
        painter.drawLine(rect.right() - 1, rect.top() + 1, rect.right() - 1, rect.bottom() - 1)
        painter.drawLine(rect.left() + 1, rect.bottom() - 1, rect.right() - 1, rect.bottom() - 1)

        # Focus indicator - green glow
        if focused:
            painter.setPen(QPen(QColor(0, 255, 0, 100), 3))
            painter.setBrush(Qt.BrushStyle.NoBrush)
            painter.drawRect(rect.adjusted(1, 1, -1, -1))
