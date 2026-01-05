# Windows-Style Title Bars in PyQt6 - Complete Research Summary

## Overview

This document consolidates research on creating authentic Windows-style title bars in PyQt6, covering multiple Windows eras from Win95 through Win11. The research covers three main approaches:
1. Classic Win95/98 beveled style
2. Vista/Win7 Aero glass effect
3. Modern Win10/11 flat design

---

## Part 1: Color Specifications by Windows Version

### Windows 95/98 (1995-1998)

**Active Title Bar Gradient:**
- Top: `#000080` (navy blue)
- Bottom: `#1084d7` (bright blue)
- Height: 19 pixels
- Font: MS Sans Serif 11pt Bold
- Text Color: White

**Inactive Title Bar:**
- Top: `#808080` (gray)
- Bottom: `#c0c0c0` (light gray)
- Text Color: White

**System Buttons:**
- Size: 16x14 pixels
- Normal Background: `#c0c0c0` (gray)
- Hover Background: `#e8e8e8` (lighter gray)
- Pressed Background: `#a0a0a0` (darker gray)
- Border: 3D beveled (highlight `#e0e0e0`, shadow `#808080`)
- Symbols: Black

**Button Symbols:**
- Minimize: `─` (horizontal line, U+2500)
- Maximize: `□` (square, U+25A1)
- Close: `✕` (X symbol, U+2715)

---

### Windows 98 (1998)

**Active Title Bar Gradient (3-stop):**
- 0%: `#0a246a` (dark blue)
- 33%: `#0052c3` (medium blue)
- 66%: `#1084d7` (bright blue)
- 100%: `#0a246a` (dark blue)

More sophisticated than Win95 with better color transitions and slightly refined appearance.

---

### Windows 2000 (2000)

Similar to Win95 with:
- Smoother antialiasing
- More refined typography
- Same title bar colors: `#000080` → `#1084d7`
- Polished feel overall

---

### Windows XP Luna (2001-2006)

**Active Title Bar Gradient:**
- Top: `#336699` (dusty blue)
- Middle: `#4488cc` (medium blue)
- Bottom: `#0066cc` (brighter blue)

**Buttons:**
- Less aggressive 3D beveling
- More gradient-based appearance
- Rounder appearance where possible
- Softer visual style

---

### Windows Vista Aero Glass (2006-2007)

**Title Bar Height:** 30 pixels

**Active Title Bar Gradient (with transparency):**
- Top: `rgba(232, 244, 248, 100)` - nearly white, very transparent
- Upper-mid: `rgba(232, 244, 248, 120)` - light cyan
- Mid: `rgba(176, 208, 224, 140)` - light cyan-blue
- Lower-mid: `rgba(100, 200, 220, 160)` - medium cyan-blue
- Bottom: `rgba(0, 120, 200, 200)` - medium blue, more opaque

**Appearance:**
- Semi-transparent glass effect
- Colors appear over blurred background
- Glossy wet appearance
- Subtle light reflection at top
- Soft shadow at bottom

**Inactive Title Bar:**
- Much darker, nearly opaque gray
- `rgba(180, 180, 180, 200)`

**System Buttons:**
- Size: 16x14 pixels
- Normal: `rgba(255, 255, 255, 60)` (very transparent white)
- Hover (standard): `rgba(176, 208, 224, 160)` (light cyan-blue)
- Hover (close): `rgba(255, 100, 100, 180)` (red tint)
- Pressed: `rgba(0, 120, 200, 200)` (medium blue)
- Text on hover/pressed: White

---

### Windows 7 Aero (2009-2015)

**Title Bar Height:** 27-28 pixels

**Active Title Bar Gradient:**
- Top: `rgba(232, 244, 248, 80)` - very light
- Upper-mid: `rgba(176, 208, 224, 110)` - light cyan
- Mid: `rgba(100, 200, 220, 120)` - cyan
- Lower-mid: `rgba(50, 150, 200, 140)` - medium blue
- Bottom: `rgba(0, 120, 200, 180)` - blue

More refined than Vista, less intense glass effect.

**System Buttons:**
- Size: 18x16 pixels (slightly larger than Vista)
- Better antialiasing
- More refined look
- Same color scheme as Vista but optimized

---

### Windows 10/11 (Modern)

**Title Bar Height:** 32-36 pixels

**Active Title Bar:**
- Solid color (usually system accent, typically blue)
- No gradient
- Fully opaque
- Examples: `#3c3c3c` or system accent color

**System Buttons:**
- Size: 20x20 pixels
- Flat design, no beveling
- System accent color with transparency
- Subtle hover effects

**Appearance:**
- Flat, minimalist
- Clean, modern
- Less personality
- Functional over aesthetic

---

## Part 2: PyQt6 Implementation Techniques

### Core Approach: Frameless Window

```python
# Remove native window frame
self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
```

This removes:
- Native title bar
- Window borders
- System buttons (minimize, maximize, close)
- System context menu on right-click

Must implement all of these manually.

---

### Step 1: Create Custom Title Bar Widget

The title bar should be a custom `QWidget` that:
1. Fills the top 19-30 pixels of the window
2. Handles custom painting (gradients, effects)
3. Responds to mouse events for window dragging
4. Responds to double-click for maximize

```python
class CustomTitleBar(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setHeight(28)  # Adjust for desired style
        self.pressed_pos = None

    def paintEvent(self, event):
        # Draw gradient and custom appearance
        painter = QPainter(self)
        gradient = QLinearGradient(0, 0, 0, self.height())
        # Set color stops based on style
        painter.fillRect(self.rect(), gradient)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.pressed_pos = event.position().toPoint()

    def mouseMoveEvent(self, event):
        if self.pressed_pos is not None:
            delta = event.position().toPoint() - self.pressed_pos
            window = self.window()
            window.move(window.pos() + delta)

    def mouseReleaseEvent(self, event):
        self.pressed_pos = None
```

---

### Step 2: Implement System Buttons

Create custom button class for minimize, maximize, restore, and close:

```python
class SystemButton(QPushButton):
    def __init__(self, button_type="close", parent=None):
        super().__init__(parent)
        self.button_type = button_type
        self.setFixedSize(20, 14)
        self.setFlat(True)

    def paintEvent(self, event):
        painter = QPainter(self)
        # Determine colors based on state
        if self.isDown():
            bg_color = QColor(160, 160, 160)
        elif self.underMouse():
            if self.button_type == "close":
                bg_color = QColor(255, 100, 100)
            else:
                bg_color = QColor(224, 224, 224)
        else:
            bg_color = QColor(192, 192, 192)

        painter.fillRect(self.rect(), bg_color)

        # Draw button symbol
        painter.setPen(QColor(0, 0, 0))
        if self.button_type == "minimize":
            painter.drawLine(4, 7, 16, 7)
        elif self.button_type == "maximize":
            painter.drawRect(3, 3, 14, 10)
        elif self.button_type == "close":
            painter.drawLine(4, 3, 16, 11)
            painter.drawLine(16, 3, 4, 11)
```

---

### Step 3: Handle Window Dragging

The title bar needs to support dragging:

```python
def mousePressEvent(self, event):
    self.pressed_pos = event.position().toPoint()

def mouseMoveEvent(self, event):
    if self.pressed_pos is not None:
        delta = event.position().toPoint() - self.pressed_pos
        window = self.window()
        new_pos = window.pos() + delta
        window.move(new_pos)

def mouseReleaseEvent(self, event):
    self.pressed_pos = None
```

---

### Step 4: Double-Click to Maximize

Implement double-click detection on title bar:

```python
def mouseDoubleClickEvent(self, event):
    if event.y() < self.height():
        window = self.window()
        if window.isMaximized():
            window.showNormal()
        else:
            window.showMaximized()
```

---

### Step 5: Connect Button Signals

Connect button clicks to window actions:

```python
minimize_btn.clicked.connect(self.window().showMinimized)
maximize_btn.clicked.connect(self.toggle_maximize)
close_btn.clicked.connect(self.window().close)
```

---

## Part 3: Button Icons and Glyphs

### Unicode Characters (Recommended)

**Minimize:**
- Primary: `─` (U+2500, BOX DRAWINGS LIGHT HORIZONTAL)
- Alternative: `▁` (U+2581, LOWER ONE EIGHTH BLOCK)
- Simple: `_` (underscore)

**Maximize:**
- Primary: `□` (U+25A1, WHITE SQUARE)
- Alternative: `▢` (U+25A2, WHITE SQUARE WITH ROUNDED CORNERS)
- Alternative: `⬜` (U+2B1C, WHITE LARGE SQUARE)

**Restore (Window):**
- `▢` (U+25A2, WHITE SQUARE WITH ROUNDED CORNERS)
- Visual: Two overlapping squares

**Close:**
- Primary: `✕` (U+2715, MULTIPLICATION SIGN)
- Common: `✖` (U+2716, HEAVY MULTIPLICATION X)
- Simple: `X` (letter X, most common)

### Font Recommendations

**Best fonts for rendering:**
- Segoe UI Symbol (modern Windows)
- Arial Unicode MS (older Windows)
- MS Sans Serif (Win95-XP era)
- Segoe MDL2 Assets (modern icons)
- Consolas (monospace)

**Rendering tips:**
- Use font size 9-12pt for 16x14 buttons
- Use high contrast (black on gray or white on blue)
- Enable antialiasing for smoothness
- Use bold weight for visibility

### SVG Alternative (if needed)

```svg
<!-- Minimize -->
<svg width="16" height="14" viewBox="0 0 16 14">
  <line x1="2" y1="7" x2="14" y2="7" stroke="black" stroke-width="2" stroke-linecap="round"/>
</svg>

<!-- Maximize -->
<svg width="16" height="14" viewBox="0 0 16 14">
  <rect x="2" y="2" width="12" height="10" fill="none" stroke="black" stroke-width="2"/>
</svg>

<!-- Close -->
<svg width="16" height="14" viewBox="0 0 16 14">
  <line x1="3" y1="2" x2="13" y2="12" stroke="black" stroke-width="2" stroke-linecap="round"/>
  <line x1="13" y1="2" x2="3" y2="12" stroke="black" stroke-width="2" stroke-linecap="round"/>
</svg>
```

---

## Part 4: Complete Implementation Examples

### Win95-Style Title Bar

```python
class Win95TitleBar(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setHeight(19)
        self.pressed_pos = None

    def paintEvent(self, event):
        painter = QPainter(self)

        # Win95 gradient
        gradient = QLinearGradient(0, 0, 0, self.height())
        gradient.setColorAt(0.0, QColor(0, 0, 128))
        gradient.setColorAt(1.0, QColor(16, 132, 215))

        painter.fillRect(self.rect(), gradient)

        # Title text
        painter.setPen(QColor(255, 255, 255))
        painter.setFont(QFont("MS Sans Serif", 11, QFont.Weight.Bold))
        painter.drawText(5, 0, self.width() - 70, self.height(),
                        Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter,
                        self.window().windowTitle())

        painter.end()

    def mousePressEvent(self, event):
        self.pressed_pos = event.position().toPoint()

    def mouseMoveEvent(self, event):
        if self.pressed_pos:
            delta = event.position().toPoint() - self.pressed_pos
            self.window().move(self.window().pos() + delta)

    def mouseReleaseEvent(self, event):
        self.pressed_pos = None
```

### Aero Glass Title Bar

```python
class AeroGlassTitleBar(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setHeight(30)
        self.pressed_pos = None

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        # Base color (simulates blurred background)
        painter.fillRect(self.rect(), QColor(200, 220, 240, 60))

        # Glass gradient overlay
        glass_gradient = QLinearGradient(0, 0, 0, self.height())
        glass_gradient.setColorAt(0.0, QColor(255, 255, 255, 100))
        glass_gradient.setColorAt(0.25, QColor(232, 244, 248, 110))
        glass_gradient.setColorAt(0.5, QColor(176, 208, 224, 130))
        glass_gradient.setColorAt(0.75, QColor(100, 180, 220, 140))
        glass_gradient.setColorAt(1.0, QColor(0, 120, 200, 160))

        painter.fillRect(self.rect(), glass_gradient)

        # Top highlight for glossy effect
        highlight = QLinearGradient(0, 0, 0, 6)
        highlight.setColorAt(0.0, QColor(255, 255, 255, 200))
        highlight.setColorAt(1.0, QColor(255, 255, 255, 0))
        painter.fillRect(0, 0, self.width(), 6, highlight)

        # Bottom shadow
        shadow = QLinearGradient(0, self.height() - 4, 0, self.height())
        shadow.setColorAt(0.0, QColor(0, 0, 0, 0))
        shadow.setColorAt(1.0, QColor(0, 0, 0, 60))
        painter.fillRect(0, self.height() - 4, self.width(), 4, shadow)

        painter.end()

    def mousePressEvent(self, event):
        if event.position().x() < self.width() - 60:
            self.pressed_pos = event.position().toPoint()

    def mouseMoveEvent(self, event):
        if self.pressed_pos:
            delta = event.position().toPoint() - self.pressed_pos
            self.window().move(self.window().pos() + delta)

    def mouseReleaseEvent(self, event):
        self.pressed_pos = None

    def mouseDoubleClickEvent(self, event):
        if event.position().x() < self.width() - 60:
            window = self.window()
            if window.isMaximized():
                window.showNormal()
            else:
                window.showMaximized()
```

---

## Part 5: Window Resizing

Since `FramelessWindowHint` removes the resize handles, you must implement them manually:

```python
class ResizableWindow(QMainWindow):
    BORDER_WIDTH = 5

    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.resize_edge = None

    def mouseMoveEvent(self, event):
        pos = event.position().toPoint()
        self.resize_edge = self.get_resize_edge(pos)

        if self.resize_edge:
            self.update_cursor(pos)
        else:
            super().mouseMoveEvent(event)

    def get_resize_edge(self, pos):
        rect = self.rect()
        b = self.BORDER_WIDTH

        # Corners (priority)
        if pos.x() < b and pos.y() < b:
            return "top-left"
        elif pos.x() > rect.width() - b and pos.y() < b:
            return "top-right"
        elif pos.x() < b and pos.y() > rect.height() - b:
            return "bottom-left"
        elif pos.x() > rect.width() - b and pos.y() > rect.height() - b:
            return "bottom-right"

        # Edges
        elif pos.x() < b:
            return "left"
        elif pos.x() > rect.width() - b:
            return "right"
        elif pos.y() < b:
            return "top"
        elif pos.y() > rect.height() - b:
            return "bottom"

        return None

    def update_cursor(self, pos):
        edge = self.get_resize_edge(pos)
        cursor_map = {
            "left": Qt.CursorShape.SizeHorCursor,
            "right": Qt.CursorShape.SizeHorCursor,
            "top": Qt.CursorShape.SizeVerCursor,
            "bottom": Qt.CursorShape.SizeVerCursor,
            "top-left": Qt.CursorShape.SizeFDiagCursor,
            "top-right": Qt.CursorShape.SizeBDiagCursor,
            "bottom-left": Qt.CursorShape.SizeBDiagCursor,
            "bottom-right": Qt.CursorShape.SizeFDiagCursor,
        }

        if edge in cursor_map:
            self.setCursor(cursor_map[edge])
        else:
            self.setCursor(Qt.CursorShape.ArrowCursor)
```

---

## Part 6: Style Comparison Summary

| Feature | Win95/98 | WinXP | Vista | Win7 | Win10 |
|---------|----------|-------|-------|------|-------|
| Title Height | 19px | 21px | 30px | 28px | 32px |
| Gradient | 2-stop | 3-stop | 5-stop | 5-stop | Solid |
| Top Color | `#000080` | `#336699` | `#e8f4f8` | `#e8f4f8` | Accent |
| Bottom Color | `#1084d7` | `#0066cc` | `#0078c8` | `#0078c8` | Accent |
| Button Size | 16x14 | 16x14 | 16x14 | 18x16 | 20x20 |
| Button Style | Beveled | Beveled | Flat glass | Flat glass | Flat |
| Button Hover | Gray | Blue | Blue | Blue | Subtle |
| Close Hover | Gray | Blue | Red | Red | Accent |

---

## Part 7: Recommendations

### For Your Retro Audio App

Given that your app already uses Frutiger Aero colors, I recommend:

**Option: Aero Glass (Vista/Win7) Style**

**Why:**
1. Aligns with existing Frutiger Aero aesthetic
2. Uses your existing blue color palette
3. More sophisticated than Win95
4. Scales well to modern displays
5. Less jarring to modern users
6. Complements existing glossy button styling

**Implementation:**
- Use Aero glass title bar with semi-transparent gradients
- Use Win95-style system buttons for consistency
- Title height: 28-30 pixels
- Top color: `rgba(232, 244, 248, 100)` to `rgba(0, 120, 200, 160)` gradient
- Glossy highlight at top
- Subtle shadow at bottom

This creates a unique hybrid style that respects retro aesthetics while being modern and professional.

---

## Part 8: Testing Checklist

- [ ] Resize from all edges
- [ ] Resize from all corners
- [ ] Cursor changes on resize areas
- [ ] Minimum size respected
- [ ] Maximum size respected
- [ ] Maximize button works
- [ ] Restore button works
- [ ] Double-click on title bar maximizes
- [ ] Window doesn't go off-screen
- [ ] Smooth performance (no lag)
- [ ] Works on multiple monitors
- [ ] High DPI displays handled
- [ ] Title bar updates when window title changes
- [ ] Button hover states work correctly
- [ ] Button press states work correctly
- [ ] Close button changes color on hover
- [ ] Window dragging is smooth
- [ ] Minimize to taskbar works
- [ ] Window appears at correct size on restore

---

## Part 9: Common Pitfalls

1. **Not implementing window resizing** - Users expect resize handles
2. **Not updating cursor** - Resize areas should show resize cursor
3. **Buttons too small/hard to click** - Test on different DPI
4. **Gradient colors look wrong** - Verify exact hex values
5. **No hover feedback** - Users need visual feedback
6. **Performance lag during resize** - Minimize repaints
7. **Window goes off-screen** - Implement bounds checking
8. **Inactive window styling missing** - Different colors when unfocused
9. **Font rendering poor** - Use high quality fonts
10. **Close button not obvious on hover** - Make red tint clear

---

## Files Created During Research

- `agent_3_findings.txt` - Windows title bar colors by version
- `agent_5_findings.txt` - Button icons and glyphs (Unicode and SVG)
- `agent_6_findings.txt` - Complete Win95 frameless implementation
- `agent_7_findings.txt` - Aero glass technical details
- `agent_8_findings.txt` - Window resizing implementation
- `agent_9_findings.txt` - Style comparison table
- `agent_10_findings.txt` - Complete Aero glass production code

---

**Research completed:** January 5, 2026
**Research method:** Multi-agent frenzy with specialized focus areas
**Total agents deployed:** 9 (analyzing design, implementation, colors, buttons, effects, resizing, styling)
