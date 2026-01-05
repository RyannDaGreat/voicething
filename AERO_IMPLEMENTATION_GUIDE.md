# Windows Aero UI Implementation Guide for PyQt6

Technical reference for recreating the Frutiger Aero visual style in PyQt6.

## 1. DWM Glass Effect and Transparency Layers

### Desktop Window Manager (DWM) Overview
- Windows Vista/7 introduced the Desktop Window Manager, which composites all windows in video memory before presenting to display
- DWM enables off-screen rendering surfaces, allowing intermediate composition processing
- Applications no longer draw directly to screen; DWM handles final compositing

### Glass Effect Technical Foundation
The "glass" effect consists of:
- **Translucent window borders** with gentle blur
- **Dynamic colorization** allowing users to tint UI
- **Reflections and subtle shadows** for depth perception
- **Frosted glass appearance** created by blurring background content

### Implementation in PyQt6

#### Window-level Translucency
```python
from PyQt6.QtWidgets import QMainWindow
from PyQt6.QtCore import Qt

class AeroWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        # Enable translucent background
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        # Create frameless window for custom chrome
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
```

#### Glass Panel Effect with RGBA
```css
/* Glass panel background - light blue with transparency */
background: rgba(173, 216, 230, 60%);
border: 1px solid rgba(255, 255, 255, 40%);
border-radius: 4px;
```

**RGBA Color Format Explanation:**
- RGBA values: (Red, Green, Blue, Alpha 0-255 or 0-100%)
- For glass effect: use 60-80% opacity with light blue base
- Alternative: `rgba(0,0,0,1)` creates near-transparency with different windowing system treatment

---

## 2. QLinearGradient Specifications for Glassy Panels

### Basic Vertical Glass Gradient
Characteristic Vista glass uses a 4-color gradient pattern:

```python
from PyQt6.QtGui import QLinearGradient, QColor
from PyQt6.QtCore import QPointF

# Create gradient from top (light) to bottom (dark)
gradient = QLinearGradient(QPointF(0, 0), QPointF(0, height))

# Vista glass gradient stops (top highlight to shadow)
gradient.setColorAt(0.0, QColor(181, 185, 188))    # #B5B9BC - top highlight
gradient.setColorAt(0.2, QColor(240, 240, 240))    # #F0F0F0 - bright zone
gradient.setColorAt(0.5, QColor(216, 216, 216))    # #D8D8D8 - mid-tone
gradient.setColorAt(1.0, QColor(211, 211, 211))    # #D3D3D3 - subtle shadow
```

### CSS Stylesheet Equivalent
```css
background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
    stop: 0.0 #B5B9BC,
    stop: 0.2 #F0F0F0,
    stop: 0.5 #D8D8D8,
    stop: 1.0 #D3D3D3);
```

### Frutiger Aero Blue Variants
For Aero-style colored glass panels:

**Primary Aero Blue:**
- Hex: `#0689E4` | RGB: (6, 137, 228)
- Used for active buttons and selected states

**Secondary Aero Cyan:**
- Hex: `#1299CA` | RGB: (18, 153, 202)
- Lighter variant for hover states

**Light Aero Cyan:**
- Hex: `#6FD7EC` | RGB: (111, 215, 236)
- Brightest highlight tone

**Deep Aero Blue:**
- Hex: `#003C78` | RGB: (0, 60, 120)
- Shadow/depth tone

**Example: Blue Glass Gradient**
```python
gradient = QLinearGradient(QPointF(0, 0), QPointF(0, height))
gradient.setColorAt(0.0, QColor(6, 137, 228))      # #0689E4 - top
gradient.setColorAt(0.3, QColor(111, 215, 236))    # #6FD7EC - mid highlight
gradient.setColorAt(0.7, QColor(18, 153, 202))     # #1299CA - mid shadow
gradient.setColorAt(1.0, QColor(0, 60, 120))       # #003C78 - bottom dark
```

---

## 3. Glossy Button Styling with Top Highlight

### Multi-Stop Gradient Pattern
Glossy buttons require at least 4 gradient stops to create the characteristic shine:

```css
QPushButton {
    background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
        stop: 0 #FFFFFF,        /* Top shine - white highlight */
        stop: 0.4 #F0F0F0,      /* Upper mid - very light gray */
        stop: 0.5 #E0E0E0,      /* Center transition point */
        stop: 1.0 #D0D0D0);     /* Bottom shadow */
    border: 1px solid #888888;
    border-radius: 4px;
    padding: 5px 15px;
    color: #000000;
    font-weight: bold;
}
```

### Glossy Button with Inner Glow (Aero Blue variant)
```css
QPushButton {
    background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
        stop: 0 #FFFFFF,        /* Bright top shine */
        stop: 0.3 #C9EBF5,      /* Light blue zone */
        stop: 0.7 #0689E4,      /* Main Aero blue */
        stop: 1.0 #003C78);     /* Dark bottom shadow */
    border: 1px solid #0050A0;
    border-top: 1px solid rgba(255, 255, 255, 0.8);  /* Inner glow */
    border-radius: 5px;
    padding: 6px 16px;
}

QPushButton:hover {
    background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
        stop: 0 #FFFACD,        /* Slightly warmer highlight on hover */
        stop: 0.3 #D4F1FF,
        stop: 0.7 #1299CA,      /* Brighter Aero blue */
        stop: 1.0 #004A8C);
}

QPushButton:pressed {
    background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
        stop: 0 #D8D8D8,        /* Inverted gradient for pressed state */
        stop: 0.5 #0050A0,
        stop: 1.0 #FFFFFF);     /* Bright bottom for inset effect */
    border: 1px solid #003C78;
}
```

### Programmatic Glossy Button (Python)
```python
from PyQt6.QtWidgets import QPushButton
from PyQt6.QtGui import QLinearGradient, QColor, QBrush
from PyQt6.QtCore import QPointF
from PyQt6.QtCore import Qt

class GlossyButton(QPushButton):
    def paintEvent(self, event):
        # Create gradient brush
        grad = QLinearGradient(QPointF(0, 0), QPointF(0, self.height()))
        grad.setColorAt(0.0, QColor(255, 255, 255))    # #FFFFFF
        grad.setColorAt(0.4, QColor(240, 240, 240))    # #F0F0F0
        grad.setColorAt(0.5, QColor(224, 224, 224))    # #E0E0E0
        grad.setColorAt(1.0, QColor(208, 208, 208))    # #D0D0D0

        # Paint button using gradient
        painter = QPainter(self)
        painter.fillRect(self.rect(), QBrush(grad))

        # Draw border
        painter.drawRect(self.rect())

        # Draw text
        painter.drawText(self.rect(), Qt.AlignmentFlag.AlignCenter, self.text())
```

---

## 4. Border Styling with Inner Glow and Beveled Effects

### Inset Border Effect (Beveled Look)
```css
/* Raised button effect */
QPushButton {
    border: 2px outset #CCCCCC;  /* Outset creates raised appearance */
    border-top-color: #FFFFFF;   /* Lighter on top */
    border-left-color: #FFFFFF;
    border-bottom-color: #808080;  /* Darker on bottom */
    border-right-color: #808080;
}

/* Pressed/active button effect */
QPushButton:pressed {
    border: 2px inset #999999;   /* Inset creates depressed appearance */
    border-top-color: #808080;
    border-left-color: #808080;
    border-bottom-color: #FFFFFF;
    border-right-color: #FFFFFF;
}
```

### Inner Glow Border (Glass Effect)
```css
/* Subtle glass edge with inner highlight */
QWidget {
    border: 1px solid #888888;           /* Outer dark edge */
    border-top: 1px solid rgba(255, 255, 255, 0.6);  /* Inner light top */
    border-left: 1px solid rgba(255, 255, 255, 0.4);
    background: rgba(200, 220, 240, 0.85);
}
```

### CSS Border-Style Properties
- `outset` - Simulates raised/embossed effect (light on top/left)
- `inset` - Simulates pressed/depressed effect (dark on top/left)
- `groove` - Creates a sunken effect
- `ridge` - Creates a raised effect
- Recommended minimum width: **2px** for beveled effects to display clearly

---

## 5. Transparency and Blur Effects in PyQt6

### Glass Morphism with Backdrop Blur (CSS approach)
Modern CSS equivalent for web/Qt hybrid:

```css
/* Frosted glass card/panel */
background: rgba(255, 255, 255, 0.25);
backdrop-filter: blur(10px);
-webkit-backdrop-filter: blur(10px);  /* Safari support */
border: 1px solid rgba(255, 255, 255, 0.25);
border-radius: 4px;
```

### PyQt6 Translucent Window Implementation
```python
from PyQt6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QLabel
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor

class TranslucentGlassPanel(QWidget):
    def __init__(self):
        super().__init__()
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        # Set semi-transparent glass background
        self.setStyleSheet("""
            QWidget {
                background-color: rgba(255, 255, 255, 191);
                border: 1px solid rgba(173, 216, 230, 100);
                border-radius: 4px;
            }
        """)
```

### Transparency Alpha Values
- **255 (100%)** - Fully opaque
- **191 (75%)** - Lightly transparent (good for glass panels)
- **127 (50%)** - Moderately transparent
- **64 (25%)** - Highly transparent (subtle overlay)
- **0 (0%)** - Fully transparent

### Alternative RGBA Formats
- Percentage: `rgba(255, 255, 255, 75%)`
- Decimal: `rgba(255, 255, 255, 0.75)`
- Integer: `rgba(255, 255, 255, 191)` (0-255 scale)

### Special Transparency Trick
```python
# Use rgba(0,0,0,1) instead of rgba(0,0,0,0) for edge case transparency
# The value 1 (extremely low but non-zero) is treated differently by windowing system
# Results in near-transparency with better compositing behavior
background: rgba(0, 0, 0, 1);
```

---

## 6. Scrollbar Styling for Aero Look

### Complete Vertical Scrollbar Stylesheet
```css
/* Main scrollbar background */
QScrollBar:vertical {
    background: #F0F0F0;
    width: 12px;
    margin: 0px;
}

/* Scrollbar handle (thumb) - glossy style */
QScrollBar::handle:vertical {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
        stop: 0 #CCCCCC,
        stop: 0.5 #AAAAAA,
        stop: 1.0 #888888);
    border: 1px solid #666666;
    border-radius: 5px;
    min-height: 20px;
    margin: 0px 2px 0px 2px;
}

/* Scrollbar handle on hover */
QScrollBar::handle:vertical:hover {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
        stop: 0 #DDDDDD,
        stop: 0.5 #BBBBBB,
        stop: 1.0 #999999);
}

/* Scrollbar handle when pressed */
QScrollBar::handle:vertical:pressed {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
        stop: 0 #999999,
        stop: 0.5 #777777,
        stop: 1.0 #555555);
}

/* Up/down arrow buttons */
QScrollBar::up-arrow:vertical, QScrollBar::down-arrow:vertical {
    width: 0px;
    height: 0px;
}

/* Remove button backgrounds */
QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
    background: none;
}

QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
    background: none;
}
```

### Horizontal Scrollbar
```css
QScrollBar:horizontal {
    background: #F0F0F0;
    height: 12px;
}

QScrollBar::handle:horizontal {
    background: qlineargradient(y1:0, x1:0, y2:1, x2:0,
        stop: 0 #CCCCCC,
        stop: 0.5 #AAAAAA,
        stop: 1.0 #888888);
    border: 1px solid #666666;
    border-radius: 5px;
    min-width: 20px;
    margin: 2px 0px 2px 0px;
}
```

### Rounded Handle Important Note
When using `border-radius` on scrollbar handles, set radius to **less than half the width**:
- Width: 10px → max border-radius: 4px
- Width: 12px → max border-radius: 5px
- Higher values cause the handle to appear flat

---

## 7. "Wet Floor" Reflection Effect

### Gradient-Based Reflection
The classic Vista/Aero reflection creates an illusion of an object hovering over a reflective surface:

```css
/* Main element */
background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
    stop: 0 #FFFFFF,
    stop: 0.6 #6FD7EC,
    stop: 1.0 #0689E4);

/* Pseudo-reflection below (using ::after) */
QWidget::after {
    content: "";
    position: absolute;
    top: 100%;
    left: 0;
    width: 100%;
    height: 50%;
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
        stop: 0 rgba(106, 215, 236, 0.5),
        stop: 1 rgba(6, 137, 228, 0.0));
    opacity: 0.4;
    transform: scaleY(-1);  /* Flip reflection */
}
```

### Mathematical Basis
The wet floor reflection uses:
1. **Mirrored/flipped copy** of the element
2. **Gradient fade-out** (opaque at top to transparent at bottom)
3. **Vertical offset** creating distance illusion
4. **Reduced opacity** (typically 30-50%) for authenticity

### Two-Pass Rendering Approach
For 3D graphics implementations:
```
Pass 1: Render element normally to viewing position
Pass 2: Render element reflected (inverted coordinates) with stencil masking
        Result: reflection appears only on planar surface below object
```

### CSS Implementation
```css
.element {
    position: relative;
    background: linear-gradient(to bottom,
        #FFFFFF 0%,
        #6FD7EC 60%,
        #0689E4 100%);
}

.element::after {
    content: "";
    position: absolute;
    top: 100%;
    left: 0;
    right: 0;
    height: 40%;
    background: linear-gradient(to bottom,
        rgba(111, 215, 236, 0.5),
        transparent);
    opacity: 0.35;
    transform: scaleY(-1);
    filter: blur(1px);
}
```

---

## 8. Bubble/Orb Button Styling

### Radial Gradient (Spherical 3D Effect)
Orb buttons use **radial gradients** with offset focal points to create 3D appearance:

```python
from PyQt6.QtGui import QRadialGradient, QColor, QBrush
from PyQt6.QtCore import QPointF
from PyQt6.QtWidgets import QPushButton

class OrbButton(QPushButton):
    def paintEvent(self, event):
        painter = QPainter(self)

        # Create radial gradient with offset center for 3D effect
        # Center point: (40%, 40%) creates top-left highlight
        grad = QRadialGradient(
            QPointF(self.width() * 0.4, self.height() * 0.4),  # Focal point (light)
            self.width() / 2  # Radius to edge
        )

        # Color stops: bright center to dark edges
        grad.setColorAt(0.0, QColor(255, 255, 255))        # Center: white
        grad.setColorAt(0.3, QColor(200, 230, 255))        # Mid-light: pale blue
        grad.setColorAt(0.7, QColor(70, 180, 230))         # Mid: bright blue
        grad.setColorAt(1.0, QColor(20, 100, 150))         # Edge: dark blue

        # Paint circular button
        painter.setBrush(QBrush(grad))
        painter.drawEllipse(self.rect())

        # Draw text in center
        painter.drawText(self.rect(), Qt.AlignmentFlag.AlignCenter, self.text())
```

### Radial Gradient QGradient Types
Qt supports three radial gradient modes:
1. **Simple Radial** - colors from focal point to circle edge
2. **Extended Radial** - colors from center to focal circle
3. **Conical** - colors around center point

### CSS Radial Gradient (Limited Support)
Qt stylesheets support radial-gradient via URL references or limited inline syntax:

```css
/* Standard approach using QGradient with setColorAt in code */
/* CSS has limited radial gradient support in Qt stylesheets */
```

### Blue Sphere/Orb Color Palette
```python
# Highlight zone (top-left 40% of button)
highlight = QColor(255, 255, 255)           # #FFFFFF
light_blue = QColor(200, 230, 255)          # #C8E6FF

# Mid-tone zones
mid_bright = QColor(70, 180, 230)           # #46B4E6
mid_dark = QColor(50, 150, 200)             # #3296C8

# Shadow zones (bottom-right 60% of button)
dark_blue = QColor(20, 100, 150)            # #146496
very_dark = QColor(10, 50, 100)             # #0A3264
```

### Multi-Stop Orb Gradient
```python
grad = QRadialGradient(QPointF(0.4 * width, 0.4 * height), width/2)
grad.setColorAt(0.0, QColor(255, 255, 255))    # 0% - bright white
grad.setColorAt(0.2, QColor(200, 230, 255))    # 20% - pale blue
grad.setColorAt(0.4, QColor(100, 200, 255))    # 40% - light blue
grad.setColorAt(0.6, QColor(50, 150, 200))     # 60% - medium blue
grad.setColorAt(0.8, QColor(20, 100, 150))     # 80% - dark blue
grad.setColorAt(1.0, QColor(5, 40, 80))        # 100% - very dark
```

### PyQt6 Radial Gradient SVG Issue
**Note:** SVG rendering in PyQt6 requires explicit `r` attribute for radial gradients:
```xml
<!-- SVG radial gradient for PyQt6 compatibility -->
<radialGradient id="orbGrad" r="0.5">
    <stop offset="0%" style="stop-color:#FFFFFF;stop-opacity:1" />
    <stop offset="50%" style="stop-color:#46B4E6;stop-opacity:1" />
    <stop offset="100%" style="stop-color:#146496;stop-opacity:1" />
</radialGradient>
```

---

## Summary Implementation Checklist

### Core Components
- [x] **Glass Panels**: RGBA transparency + subtle borders (rgba with 60-80% opacity)
- [x] **Glossy Buttons**: 4+ gradient stops with white top highlight
- [x] **Beveled Borders**: Inset/outset border-style or manual top/bottom colors
- [x] **Scrollbars**: Horizontal gradient handle with rounded corners (radius < half width)
- [x] **Inner Glow**: Semi-transparent white top border (rgba(255,255,255, 0.4-0.8))
- [x] **Orb Buttons**: Radial gradients with offset focal point at 40% top-left
- [x] **Reflections**: Flipped gradient with fade-out and reduced opacity

### Color Palettes
**Gray Scale (Default Aero):**
- Top: `#B5B9BC` | Mid: `#F0F0F0` | Bottom: `#D3D3D3`

**Blue Aero Theme:**
- Primary: `#0689E4` | Cyan: `#6FD7EC` | Deep: `#003C78`

### Key Technical Details
1. **Gradient Coordinate Systems**: Use QPointF(x, y) with pixel or normalized coords
2. **Transparency**: Use RGBA with alpha 0-255 or 0-100%
3. **Blur Effects**: Limited in Qt; use window attributes for translucency
4. **CSS Priority**: Stylesheets work better than programmatic for consistency
5. **Border Radius**: Never exceed half the element's width for proper rounding

---

## References and Resources

- [7.css Framework](https://khang-nd.github.io/7.css/) - Windows 7 CSS recreation
- [Qt Style Sheets Reference](https://doc.qt.io/qt-6/stylesheet-reference.html)
- [QLinearGradient Documentation](https://doc.qt.io/qt-6/qlineargradient.html)
- [Windows Aero Glass Effects (Archive)](https://learn.microsoft.com/en-us/archive/msdn-magazine/2007/april/aero-glass-create-special-effects-with-the-desktop-window-manager)
- [Glassmorphism CSS Tutorial](https://daily-dev-tips.com/posts/css-frosted-glass-credit-card/)
