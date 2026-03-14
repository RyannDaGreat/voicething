"""Star Trek LCARS style - Library Computer Access/Retrieval System.

Recreates the iconic LCARS interface designed by Michael Okuda for Star Trek:
The Next Generation, Deep Space Nine, and Voyager. Characterized by pure black
backgrounds, colored horizontal bars with rounded end caps (pill shapes),
"elbow" corner pieces, and a distinctive palette of orange/tan, lavender/purple,
blue, and occasional alert reds.

Color palette sourced from thelcars.com and trekcolors (canonical LCARS hex values).
Font uses Helvetica Neue as the closest widely-available match to the
Swiss 911 Ultra Compressed / "Okuda" typeface used on the show.
"""

from PyQt6.QtCore import Qt, QRectF
from PyQt6.QtGui import QColor, QLinearGradient, QBrush, QPainterPath, QPen

from .base import BaseStyle


# ── LCARS canonical palette (from thelcars.com / trekcolors) ────────────
# Primary orange/tan family
LCARS_ORANGE = QColor(0xFF, 0x99, 0x00)          # #FF9900 — golden-orange (primary accent)
LCARS_ORANGE_CSS = "rgb(255,153,0)"
LCARS_BUTTERSCOTCH = QColor(0xFF, 0x99, 0x66)    # #FF9966 — butterscotch / orange-peel
LCARS_SUNFLOWER = QColor(0xFF, 0xCC, 0x99)       # #FFCC99 — sunflower (light tan)
LCARS_GOLD = QColor(0xFF, 0xAA, 0x00)            # #FFAA00 — gold

# Lavender/purple family
LCARS_VIOLET = QColor(0xCC, 0x99, 0xFF)          # #CC99FF — african-violet (primary purple)
LCARS_VIOLET_CSS = "rgb(204,153,255)"
LCARS_VIOLET_CREME = QColor(0xDD, 0xBB, 0xFF)    # #DDBBFF — violet-creme
LCARS_LILAC = QColor(0xCC, 0x55, 0xFF)           # #CC55FF — lilac (saturated purple)

# Blue family
LCARS_ICE = QColor(0x99, 0xCC, 0xFF)             # #99CCFF — ice / anakiwa
LCARS_ICE_CSS = "rgb(153,204,255)"
LCARS_SKY = QColor(0xAA, 0xAA, 0xFF)             # #AAAAFF — sky
LCARS_BLUE = QColor(0x99, 0x99, 0xFF)            # #9999FF — melrose
LCARS_MARINER = QColor(0x33, 0x66, 0xCC)         # #3366CC — mariner (deep blue)

# Alert / status
LCARS_RED = QColor(0xFF, 0x22, 0x00)             # #FF2200 — mars (red alert)
LCARS_RED_CSS = "rgb(255,34,0)"
LCARS_TOMATO = QColor(0xFF, 0x55, 0x55)          # #FF5555 — tomato
LCARS_PEACH = QColor(0xFF, 0x88, 0x66)           # #FF8866 — peach

# Neutrals
LCARS_BLACK = "rgb(0,0,0)"                       # Pure black background
LCARS_BLACK_Q = QColor(0, 0, 0)
LCARS_GRAY = QColor(0x66, 0x66, 0x88)            # #666688 — gray (muted blue-gray)
LCARS_SPACE_WHITE = "rgb(245,246,250)"            # #F5F6FA — space-white (text)
LCARS_SPACE_WHITE_Q = QColor(0xF5, 0xF6, 0xFA)

# CSS text colors
TEXT_BRIGHT = "rgb(245,246,250)"      # Space-white
TEXT_DIM = "rgb(204,204,230)"         # Slightly dimmed lavender-white
TEXT_MUTED = "rgb(102,102,136)"       # Blue-gray muted
TEXT_DISABLED = "rgb(50,50,68)"       # Dark muted

# Bar/border CSS
BORDER_DARK = "rgb(40,30,10)"        # Very dark warm edge
BORDER_MID = "rgb(102,80,30)"        # Mid-tone orange-brown

# Button shades (dark with orange tint)
BTN_DARK = "rgb(25,18,5)"
BTN_MID = "rgb(50,38,12)"
BTN_LIGHT = "rgb(75,58,20)"

# Pill-cap radius for LCARS bar end-caps
PILL_RADIUS = 12


class StarTrekLCARSStyle(BaseStyle):
    """Command, specific. Star Trek LCARS interface theme for VoiceThing."""

    name = "star_trek_lcars"
    font = "Helvetica Neue"
    corner_radius = 0  # LCARS windows have sharp outer corners (bars provide shape)

    # Accent — LCARS golden-orange
    accent = LCARS_ORANGE
    accent_css = LCARS_ORANGE_CSS
    text_primary = TEXT_BRIGHT
    text_secondary = TEXT_DIM
    text_muted = TEXT_MUTED
    text_error = LCARS_RED_CSS
    text_link = LCARS_ICE_CSS
    border_color = BORDER_MID
    border_dark = BORDER_DARK
    icon_color_dark = '#ff9900'
    icon_color_light = '#ff9900'
    icon_color_muted = '#996600'

    # Dropdown input fields — black with orange text
    input_bg = '#0a0a0a'
    input_text = '#ff9900'

    # Slider — orange groove on black
    slider_groove = "rgba(255,153,0,0.3)"
    slider_handle = LCARS_ORANGE_CSS
    slider_fill = "rgb(255,170,0)"

    # Rotary knob — LCARS console style
    knob_style = "cyber"
    knob_body_dark = "#0a0800"
    knob_body_light = "#1a1508"
    knob_notch_style = "line"
    knob_tickmarks = True
    knob_glow = True
    knob_track_color = "#ff9900"
    knob_label_color = "#ffcc99"

    # Waveform — LCARS ice blue
    waveform_color = LCARS_ICE
    waveform_glow = True
    waveform_glow_radius = 16
    waveform_glow_alpha = 160
    waveform_center_line = QColor(153, 204, 255, 50)
    waveform_panel = "dark"

    # Timer — orange LCD on black
    timer_use_lcd = True
    timer_color = LCARS_ORANGE
    timer_font_size = 28
    timer_panel_size = (160, 40)

    # Transcription panel
    transcription_text = TEXT_BRIGHT
    transcription_text_dimmed = "rgba(255,153,0,0.7)"
    transcription_panel_bg = LCARS_BLACK
    transcription_panel_border = BORDER_DARK
    transcription_row_hover = "rgba(255,153,0,0.08)"
    transcription_row_btn_bg = "rgba(255,153,0,0.10)"
    transcription_row_btn_hover = "rgba(255,153,0,0.20)"
    transcription_row_btn_pressed = "rgba(255,153,0,0.35)"

    # Chime editor — LCARS palette on black
    chime_grid_bg = QColor(5, 5, 5)
    chime_grid_line = QColor(40, 30, 10)
    chime_cell_inactive = QColor(20, 15, 5)
    chime_cell_active = LCARS_ORANGE
    chime_cell_highlight = QColor(255, 153, 0, 80)
    chime_piano_white = QColor(255, 204, 153)   # Sunflower
    chime_piano_black = QColor(10, 8, 2)
    chime_piano_label_white = QColor(40, 30, 10)
    chime_piano_label_black = QColor(255, 153, 0)

    # ── CSS methods ──────────────────────────────────────────────

    def title_style(self, size=18):
        """Command, specific. LCARS title in orange."""
        return (
            f"color: {LCARS_ORANGE_CSS}; font-size: {size}px; "
            f"font-family: {self.font}; font-weight: bold; "
            f"text-transform: uppercase; letter-spacing: 1px;"
        )

    def body_style(self, size=10):
        """Command, specific. Body text in dim lavender-white."""
        return f"color: {TEXT_DIM}; font-size: {size}px; font-family: {self.font};"

    def section_style(self):
        """Command, specific. Section headers in LCARS ice blue."""
        return (
            f"color: {LCARS_ICE_CSS}; font-size: 12px; "
            f"font-family: {self.font}; text-transform: uppercase;"
        )

    def button_css(self):
        """Command, specific. LCARS-style buttons with orange/tan palette."""
        return (
            # Normal — dark with warm orange border, rounded pill caps
            f"QPushButton {{ color: {TEXT_DIM}; "
            f"background: qlineargradient(x1:0, y1:0, x2:0, y2:1, "
            f"stop:0 {BTN_LIGHT}, stop:0.5 {BTN_MID}, stop:1 {BTN_DARK}); "
            f"border: 1px solid rgb(102,80,30); "
            f"border-radius: {PILL_RADIUS}px; padding: 3px 12px; "
            f"font-size: 11px; font-family: {self.font}; text-align: left; "
            f"text-transform: uppercase; }}"
            # Hover — orange glow
            f"QPushButton:hover {{ color: {LCARS_ORANGE_CSS}; "
            f"background: qlineargradient(x1:0, y1:0, x2:0, y2:1, "
            f"stop:0 rgb(120,90,20), stop:0.5 rgb(90,68,15), stop:1 rgb(60,45,10)); "
            f"border: 1px solid rgb(200,140,20); }}"
            # Pressed — deeper
            f"QPushButton:pressed {{ color: {TEXT_BRIGHT}; "
            f"background: qlineargradient(x1:0, y1:0, x2:0, y2:1, "
            f"stop:0 rgb(40,30,8), stop:0.5 rgb(30,22,5), stop:1 rgb(20,15,3)); "
            f"border: 1px solid rgb(150,110,15); }}"
            # Disabled
            f"QPushButton:disabled {{ color: {TEXT_DISABLED}; "
            f"background: rgb(15,12,3); border: 1px solid rgb(30,24,8); }}"
            # Checked — lit orange (active LCARS button)
            f"QPushButton:checked {{ color: rgb(0,0,0); "
            f"background: qlineargradient(x1:0, y1:0, x2:0, y2:1, "
            f"stop:0 rgb(255,180,50), stop:0.5 rgb(255,153,0), stop:1 rgb(200,120,0)); "
            f"border: 1px solid rgb(255,200,80); }}"
            f"QPushButton:checked:hover {{ "
            f"background: qlineargradient(x1:0, y1:0, x2:0, y2:1, "
            f"stop:0 rgb(255,200,80), stop:0.5 rgb(255,170,20), stop:1 rgb(220,140,0)); }}"
        )

    def menu_css(self):
        """Command, specific. LCARS dropdown menu on black with orange highlight."""
        return (
            f"QMenu {{ background: rgb(5,5,5); color: {TEXT_BRIGHT}; "
            f"border: 2px solid rgb(102,80,30); border-radius: 4px; "
            f"padding: 4px; font-family: {self.font}; font-size: 12px; }}"
            "QMenu::item { padding: 4px 16px; border-radius: 4px; }"
            f"QMenu::item:selected {{ color: rgb(0,0,0); "
            f"background: {LCARS_ORANGE_CSS}; }}"
            f"QMenu::separator {{ height: 2px; background: rgb(102,80,30); "
            f"margin: 4px 8px; }}"
        )

    def _scrollbar_vertical_css(self):
        """Command, specific. LCARS-colored scrollbar — orange handle on black."""
        return (
            f"QScrollBar:vertical {{ width: 14px; background: rgb(5,5,5); "
            f"border: 1px solid rgb(40,30,10); border-radius: 7px; margin: 0px; }}"
            # Handle — LCARS orange bar with pill shape
            "QScrollBar::handle:vertical { "
            "background: qlineargradient(x1:0, y1:0, x2:1, y2:0, "
            "stop:0.0 rgb(180,110,0), stop:0.3 rgb(220,140,0), "
            "stop:0.5 rgb(255,153,0), stop:0.7 rgb(220,140,0), stop:1.0 rgb(180,110,0)); "
            "border: 1px solid rgb(140,90,0); border-radius: 5px; "
            "min-height: 40px; margin: 2px; }"
            # Handle hover — brighter orange
            "QScrollBar::handle:vertical:hover { "
            "background: qlineargradient(x1:0, y1:0, x2:1, y2:0, "
            "stop:0.0 rgb(220,150,20), stop:0.3 rgb(255,180,40), "
            "stop:0.5 rgb(255,200,80), stop:0.7 rgb(255,180,40), stop:1.0 rgb(220,150,20)); "
            "border: 1px solid rgb(200,140,0); }"
            # Handle pressed — dimmer
            "QScrollBar::handle:vertical:pressed { "
            "background: qlineargradient(x1:0, y1:0, x2:1, y2:0, "
            "stop:0.0 rgb(120,80,0), stop:0.3 rgb(150,100,0), "
            "stop:0.5 rgb(180,120,0), stop:0.7 rgb(150,100,0), stop:1.0 rgb(120,80,0)); "
            "border: 1px solid rgb(100,70,0); }"
            "QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical { "
            "height: 0; width: 0; background: none; border: none; }"
            "QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical { "
            "background: transparent; }"
        )

    def panel_bg_css(self):
        """Command, specific. Near-black panel with warm border."""
        return (
            f"background: qlineargradient(x1:0, y1:0, x2:0, y2:1, "
            f"stop:0 rgb(12,10,5), stop:0.02 rgb(5,4,2), "
            f"stop:0.98 rgb(5,4,2), stop:1 rgb(2,2,1)); "
            f"border: 1px solid rgb(40,30,10); border-radius: 4px;"
        )

    def panel_bg_flat_css(self):
        """Command, specific. Flat black panel with warm border."""
        return (
            f"background: rgb(5,4,2); border: 1px solid rgb(40,30,10); "
            f"border-radius: 4px;"
        )

    # ── Painting methods ─────────────────────────────────────────

    def _draw_lcars_bar(self, painter, x, y, w, h, color, cap_left=True, cap_right=True):
        """
        Pure function, specific. Draw a single LCARS horizontal bar with
        optional pill-shaped end caps.

        The characteristic LCARS bar: a rectangle with semicircular caps on
        one or both ends. Cap radius is half the bar height.

        Args:
            painter: QPainter
            x, y: Top-left corner of bar
            w: Total width including caps
            h: Bar height
            color: QColor for the bar fill
            cap_left: If True, left end is rounded (pill cap)
            cap_right: If True, right end is rounded (pill cap)
        """
        cap_r = h / 2  # Semicircle radius = half bar height
        path = QPainterPath()

        if cap_left and cap_right:
            # Full pill shape
            path.addRoundedRect(QRectF(x, y, w, h), cap_r, cap_r)
        elif cap_left:
            # Rounded left, flat right
            path.moveTo(x + cap_r, y)
            path.lineTo(x + w, y)
            path.lineTo(x + w, y + h)
            path.lineTo(x + cap_r, y + h)
            path.arcTo(QRectF(x, y, h, h), 270, -180)
            path.closeSubpath()
        elif cap_right:
            # Flat left, rounded right
            path.moveTo(x, y)
            path.lineTo(x + w - cap_r, y)
            path.arcTo(QRectF(x + w - h, y, h, h), 90, -180)
            path.lineTo(x, y + h)
            path.closeSubpath()
        else:
            # No caps — plain rectangle
            path.addRect(QRectF(x, y, w, h))

        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(QBrush(color))
        painter.drawPath(path)

    def _draw_lcars_elbow(self, painter, x, y, outer_w, outer_h, bar_h, bar_w, color, corner="top-left"):
        """
        Pure function, specific. Draw an LCARS elbow — the L-shaped corner piece
        where a horizontal bar meets a vertical bar, with a rounded inner cutout.

        The elbow is the most distinctive LCARS element: a quarter-circle cutout
        at the inner corner where horizontal meets vertical.

        Args:
            painter: QPainter
            x, y: Top-left corner of the bounding box
            outer_w: Width of the bounding box
            outer_h: Height of the bounding box
            bar_h: Thickness of the horizontal arm
            bar_w: Thickness of the vertical arm
            color: QColor for the fill
            corner: Which corner ("top-left", "top-right", "bottom-left", "bottom-right")
        """
        inner_radius = min(outer_w - bar_w, outer_h - bar_h)
        path = QPainterPath()

        if corner == "top-left":
            # Outer boundary
            path.moveTo(x, y)
            path.lineTo(x + outer_w, y)                          # Top edge right
            path.lineTo(x + outer_w, y + bar_h)                  # Down to bar bottom
            path.lineTo(x + bar_w + inner_radius, y + bar_h)     # Left to arc start
            # Inner arc (quarter circle from bar bottom to vertical bar right edge)
            path.arcTo(
                QRectF(x + bar_w, y + bar_h, inner_radius * 2, inner_radius * 2),
                90, 90
            )
            path.lineTo(x + bar_w, y + outer_h)                  # Down along vertical bar
            path.lineTo(x, y + outer_h)                          # Left edge bottom
            path.closeSubpath()
        elif corner == "top-right":
            path.moveTo(x, y)
            path.lineTo(x + outer_w, y)
            path.lineTo(x + outer_w, y + outer_h)
            path.lineTo(x + outer_w - bar_w, y + outer_h)
            path.lineTo(x + outer_w - bar_w, y + bar_h + inner_radius)
            path.arcTo(
                QRectF(x + outer_w - bar_w - inner_radius * 2, y + bar_h,
                       inner_radius * 2, inner_radius * 2),
                0, 90
            )
            path.lineTo(x, y + bar_h)
            path.lineTo(x, y)
            path.closeSubpath()
        elif corner == "bottom-left":
            path.moveTo(x, y)
            path.lineTo(x + bar_w, y)
            path.lineTo(x + bar_w, y + outer_h - bar_h - inner_radius)
            path.arcTo(
                QRectF(x + bar_w, y + outer_h - bar_h - inner_radius * 2,
                       inner_radius * 2, inner_radius * 2),
                180, 90
            )
            path.lineTo(x + outer_w, y + outer_h - bar_h)
            path.lineTo(x + outer_w, y + outer_h)
            path.lineTo(x, y + outer_h)
            path.closeSubpath()
        elif corner == "bottom-right":
            path.moveTo(x + outer_w, y)
            path.lineTo(x + outer_w, y + outer_h)
            path.lineTo(x, y + outer_h)
            path.lineTo(x, y + outer_h - bar_h)
            path.lineTo(x + outer_w - bar_w - inner_radius, y + outer_h - bar_h)
            path.arcTo(
                QRectF(x + outer_w - bar_w - inner_radius * 2,
                       y + outer_h - bar_h - inner_radius * 2,
                       inner_radius * 2, inner_radius * 2),
                270, 90
            )
            path.lineTo(x + outer_w - bar_w, y)
            path.closeSubpath()

        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(QBrush(color))
        painter.drawPath(path)

    def paint_window(self, painter, rect, width, height, focused=True):
        """
        Command, specific. Paint LCARS window with characteristic bars and elbows.

        Layout:
        - Pure black background
        - Top-left elbow (orange) connecting top bar to left sidebar
        - Bottom-left elbow (violet) connecting bottom bar to left sidebar
        - Top horizontal bar segments in orange/sunflower/ice
        - Bottom horizontal bar segments in violet/blue/butterscotch
        - Left vertical sidebar between elbows in sunflower
        - Small colored accent segments along the top and bottom bars
        """
        alpha_mult = 1.0 if focused else 0.6

        # Clip to window rect (no rounded corners for LCARS - bars provide the shape)
        path = QPainterPath()
        path.addRect(QRectF(rect))
        painter.setClipPath(path)

        # 1. Pure black background
        painter.setBrush(LCARS_BLACK_Q)
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawRect(rect)

        if not focused:
            painter.setOpacity(alpha_mult)

        # ── Dimensions ──
        sidebar_w = 28         # Width of left vertical sidebar
        bar_h = 14             # Height of horizontal bars
        elbow_h = 40           # Height of elbow bounding box
        elbow_w = 80           # Width of elbow bounding box
        gap = 3                # Gap between bar segments

        top_y = 0
        bottom_y = height - bar_h

        # ── Top-left elbow (orange) ──
        self._draw_lcars_elbow(
            painter, 0, top_y, elbow_w, elbow_h,
            bar_h, sidebar_w, LCARS_ORANGE, "top-left"
        )

        # ── Top horizontal bar segments (right of elbow) ──
        bar_start_x = elbow_w + gap
        remaining_w = width - bar_start_x

        # Segment 1: sunflower (wide)
        seg1_w = remaining_w * 0.35
        self._draw_lcars_bar(
            painter, bar_start_x, top_y, seg1_w, bar_h,
            LCARS_SUNFLOWER, cap_left=False, cap_right=False,
        )
        # Segment 2: ice blue (medium)
        seg2_x = bar_start_x + seg1_w + gap
        seg2_w = remaining_w * 0.25
        self._draw_lcars_bar(
            painter, seg2_x, top_y, seg2_w, bar_h,
            LCARS_ICE, cap_left=False, cap_right=False,
        )
        # Segment 3: violet (medium, pill-capped right end)
        seg3_x = seg2_x + seg2_w + gap
        seg3_w = remaining_w * 0.38
        self._draw_lcars_bar(
            painter, seg3_x, top_y, seg3_w, bar_h,
            LCARS_VIOLET, cap_left=False, cap_right=True,
        )

        # ── Left vertical sidebar (sunflower, between elbows) ──
        sidebar_top = elbow_h + gap
        sidebar_bottom = height - elbow_h - gap
        sidebar_h = sidebar_bottom - sidebar_top
        if sidebar_h > 0:
            # Main sidebar segment
            main_sidebar_h = sidebar_h * 0.6
            self._draw_lcars_bar(
                painter, 0, sidebar_top, sidebar_w, main_sidebar_h,
                LCARS_SUNFLOWER, cap_left=False, cap_right=False,
            )
            # Small accent segment (violet)
            accent_y = sidebar_top + main_sidebar_h + gap
            accent_h = sidebar_h * 0.15
            self._draw_lcars_bar(
                painter, 0, accent_y, sidebar_w, accent_h,
                LCARS_VIOLET, cap_left=False, cap_right=False,
            )
            # Remaining segment (ice blue)
            remain_y = accent_y + accent_h + gap
            remain_h = sidebar_bottom - remain_y
            if remain_h > 0:
                self._draw_lcars_bar(
                    painter, 0, remain_y, sidebar_w, remain_h,
                    LCARS_ICE, cap_left=False, cap_right=False,
                )

        # ── Bottom-left elbow (violet) ──
        self._draw_lcars_elbow(
            painter, 0, height - elbow_h, elbow_w, elbow_h,
            bar_h, sidebar_w, LCARS_VIOLET, "bottom-left"
        )

        # ── Bottom horizontal bar segments ──
        # Segment 1: butterscotch (wide)
        self._draw_lcars_bar(
            painter, bar_start_x, bottom_y, seg1_w, bar_h,
            LCARS_BUTTERSCOTCH, cap_left=False, cap_right=False,
        )
        # Segment 2: blue/sky (medium)
        self._draw_lcars_bar(
            painter, seg2_x, bottom_y, seg2_w, bar_h,
            LCARS_SKY, cap_left=False, cap_right=False,
        )
        # Segment 3: orange (pill-capped right)
        self._draw_lcars_bar(
            painter, seg3_x, bottom_y, seg3_w, bar_h,
            LCARS_ORANGE, cap_left=False, cap_right=True,
        )

        if not focused:
            painter.setOpacity(1.0)

        painter.setClipping(False)

    def paint_waveform_panel(self, painter, rect, w, h, cy):
        """
        Command, specific. Paint LCARS-style waveform panel with bordered display.

        Black interior with a thin LCARS-colored border frame, evoking the
        sensor readout displays on the Enterprise bridge. Subtle grid lines
        in dark blue suggest a tactical/sensor display.
        """
        # Black interior
        panel_grad = QLinearGradient(0, 0, 0, h)
        panel_grad.setColorAt(0.0, QColor(5, 5, 8))
        panel_grad.setColorAt(0.3, QColor(2, 2, 5))
        panel_grad.setColorAt(0.7, QColor(2, 2, 5))
        panel_grad.setColorAt(1.0, QColor(5, 5, 8))
        painter.setBrush(QBrush(panel_grad))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawRoundedRect(rect, 4, 4)

        # Subtle grid lines — dark blue (sensor display feel)
        painter.setPen(QPen(QColor(30, 40, 80, 40), 1))
        for i in range(1, 4):
            y = int(h * i / 4)
            painter.drawLine(0, y, w, y)
        for i in range(1, 8):
            x = int(w * i / 8)
            painter.drawLine(x, 0, x, h)

        # Center line — LCARS ice blue
        # Bloom layer (wide, dim)
        painter.setPen(QPen(QColor(153, 204, 255, 20), 5))
        painter.drawLine(0, int(cy), w, int(cy))
        # Core line
        painter.setPen(QPen(QColor(153, 204, 255, 60), 1))
        painter.drawLine(0, int(cy), w, int(cy))

        # LCARS-style frame border: orange top/bottom, violet left/right
        border_thickness = 2
        # Top border — orange
        painter.setPen(QPen(LCARS_ORANGE, border_thickness))
        painter.drawLine(rect.left() + 4, rect.top(), rect.right() - 4, rect.top())
        # Bottom border — butterscotch
        painter.setPen(QPen(LCARS_BUTTERSCOTCH, border_thickness))
        painter.drawLine(rect.left() + 4, rect.bottom(), rect.right() - 4, rect.bottom())
        # Left border — violet
        painter.setPen(QPen(LCARS_VIOLET, border_thickness))
        painter.drawLine(rect.left(), rect.top() + 4, rect.left(), rect.bottom() - 4)
        # Right border — ice blue
        painter.setPen(QPen(LCARS_ICE, border_thickness))
        painter.drawLine(rect.right(), rect.top() + 4, rect.right(), rect.bottom() - 4)

        # Corner dots — small colored squares at the four corners
        dot_size = 3
        for corner_x, corner_y, color in [
            (rect.left(), rect.top(), LCARS_ORANGE),
            (rect.right() - dot_size, rect.top(), LCARS_ICE),
            (rect.left(), rect.bottom() - dot_size, LCARS_VIOLET),
            (rect.right() - dot_size, rect.bottom() - dot_size, LCARS_BUTTERSCOTCH),
        ]:
            painter.setPen(Qt.PenStyle.NoPen)
            painter.setBrush(QBrush(color))
            painter.drawRect(corner_x, corner_y, dot_size, dot_size)
