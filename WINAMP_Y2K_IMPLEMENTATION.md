# Winamp Visualizer & Y2K UI Implementation Guide for PyQt6

## 1. WAVEFORM VISUALIZATION (Oscilloscope Display)

### Type: LINE SEGMENTS (not dots, not bars)
- Winamp's iconic oscilloscope connected audio samples with LINE segments
- **Rendering**: QPainter.drawLines() with array of connected points
- **Samples per frame**: 576 (standard FFT size from audio)
- **Update rate**: 60 FPS (0.016s per frame)
- **Screen mapping**: X = normalized sample position, Y = audio amplitude mapped to screen height

### Implementation Code Sketch
```python
from PyQt6.QtGui import QPainter, QPen, QColor
from PyQt6.QtWidgets import QWidget

class OscilloscopeWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.waveform_points = []
    
    def paintEvent(self, event):
        painter = QPainter(self)
        
        # Black background - maximum contrast
        painter.fillRect(self.rect(), QColor("#000000"))
        
        # Lime green waveform - main line
        painter.setPen(QPen(QColor("#00FF00"), 1))
        painter.drawLines(self.waveform_points)
        
        # Optional glow effect: semi-transparent second pass
        painter.setPen(QPen(QColor(0, 255, 0, 80), 2))
        painter.drawLines(self.waveform_points)
        
        painter.end()
    
    def update_waveform(self, audio_samples):
        """
        audio_samples: list of float values (-1.0 to 1.0)
        """
        width = self.width()
        height = self.height()
        
        self.waveform_points = []
        for i, sample in enumerate(audio_samples):
            x = (i / len(audio_samples)) * width
            y = (height / 2) - (sample * height / 2)
            self.waveform_points.append((int(x), int(y)))
        
        self.update()
```

---

## 2. COLOR PALETTE - EXACT VALUES

### Neon Colors (RGB + Hex)
| Color | Hex | RGB | Usage |
|-------|-----|-----|-------|
| Lime Green | #00FF00 | (0, 255, 0) | Waveform, text, primary accent |
| Cyan | #00FFFF | (0, 255, 255) | Y2K gradients, secondary accent |
| Magenta | #FF00FF | (255, 0, 255) | Y2K gradients, alternative neon |
| Yellow | #FFFF00 | (255, 255, 0) | Spectrum gradient end, vaporwave |

### Backgrounds
| Color | Hex | RGB | Usage |
|-------|-----|-----|-------|
| Pure Black | #000000 | (0, 0, 0) | Visualization background |
| Dark Gray | #0a0a0a | (10, 10, 10) | Panel backdrop |
| Medium Gray | #1a1a1a | (26, 26, 26) | Main panel background |
| Light Gray | #333333 | (51, 51, 51) | Subtle highlights |

### UI Controls
| Color | Hex | RGB | Usage |
|-------|-----|-----|-------|
| White Highlight | #FFFFFF | (255, 255, 255) | Bevel top/left edge |
| Gray Shadow | #808080 | (128, 128, 128) | Bevel bottom/right edge |
| Button Face | #C0C0C0 | (192, 192, 192) | Windows 95 default button |
| Red Peak | #FF0000 | (255, 0, 0) | Peak meter indicator |

---

## 3. WINDOWS 95 BEVELED 3D BUTTON EFFECT

### CSS/QSS Implementation
```css
QPushButton {
    background-color: #C0C0C0;
    border: 2px solid;
    border-top-color: #FFFFFF;      /* Bright white highlight */
    border-left-color: #FFFFFF;     /* Bright white highlight */
    border-bottom-color: #808080;   /* Gray shadow */
    border-right-color: #808080;    /* Gray shadow */
    color: #000000;                 /* Black text */
    padding: 4px;
    font: 10px "MS Sans Serif";
}

QPushButton:pressed {
    border-top-color: #808080;      /* Invert for pressed effect */
    border-left-color: #808080;
    border-bottom-color: #FFFFFF;
    border-right-color: #FFFFFF;
}

QPushButton:hover {
    background-color: #D0D0D0;      /* Slight highlight on hover */
}
```

### Python/Painter Alternative
```python
def draw_beveled_button(painter, rect, pressed=False):
    painter.fillRect(rect, QColor("#C0C0C0"))
    
    if not pressed:
        # Top/left highlight
        painter.setPen(QPen(QColor("#FFFFFF"), 2))
        painter.drawLine(rect.topLeft(), rect.topRight())
        painter.drawLine(rect.topLeft(), rect.bottomLeft())
        
        # Bottom/right shadow
        painter.setPen(QPen(QColor("#808080"), 2))
        painter.drawLine(rect.topRight(), rect.bottomRight())
        painter.drawLine(rect.bottomLeft(), rect.bottomRight())
    else:
        # Inverted for pressed state
        painter.setPen(QPen(QColor("#808080"), 2))
        painter.drawLine(rect.topLeft(), rect.topRight())
        painter.drawLine(rect.topLeft(), rect.bottomLeft())
        
        painter.setPen(QPen(QColor("#FFFFFF"), 2))
        painter.drawLine(rect.topRight(), rect.bottomRight())
        painter.drawLine(rect.bottomLeft(), rect.bottomRight())
```

### Key Principle
- **Light source from top-left**: White highlight on top/left edges simulates light reflection
- **Shadow on bottom-right**: Dark shadow simulates depth/recession
- **Inverted when pressed**: Highlights and shadows swap to create depression effect
- **Face color**: #C0C0C0 is THE Windows 95 gray (not pure gray)

---

## 4. METALLIC/CHROME GRADIENT TECHNIQUES

### Chrome Gradient using QLinearGradient
```python
from PyQt6.QtGui import QLinearGradient, QColor, QBrush

def create_chrome_gradient(height):
    """Create realistic metallic chrome gradient"""
    gradient = QLinearGradient(0, 0, 0, height)
    
    # Bright highlight (light reflection)
    gradient.setColorAt(0.0, QColor("#FFFFFF"))
    
    # Light gray transition
    gradient.setColorAt(0.2, QColor("#E0E0E0"))
    
    # Mid-tone (main metallic color)
    gradient.setColorAt(0.5, QColor("#808080"))
    
    # Dark gray (shadow transition)
    gradient.setColorAt(0.8, QColor("#404040"))
    
    # Deep shadow
    gradient.setColorAt(1.0, QColor("#000000"))
    
    return gradient

# Usage
painter = QPainter(...)
brush = QBrush(create_chrome_gradient(widget_height))
painter.fillRect(rect, brush)
```

### Y2K Vaporwave Gradient (Cyan → Magenta → Yellow)
```python
def create_vaporwave_gradient(width, height):
    """Y2K aesthetic with cyan-magenta-yellow transition"""
    gradient = QLinearGradient(0, 0, width, height)
    
    gradient.setColorAt(0.0, QColor("#00FFFF"))    # Cyan
    gradient.setColorAt(0.5, QColor("#FF00FF"))    # Magenta
    gradient.setColorAt(1.0, QColor("#FFFF00"))    # Yellow
    
    return gradient
```

### Metallic Text Effect
```python
def draw_metallic_text(painter, text, x, y):
    """Chrome-effect text with depth"""
    # Main text with chrome gradient
    font = QFont("Arial", 14, QFont.Weight.Bold)
    painter.setFont(font)
    painter.setPen(QColor("#FFFFFF"))
    painter.drawText(x, y, text)
    
    # Shadow pass (offset, darker)
    painter.setPen(QColor("#404040"))
    painter.drawText(x+1, y+1, text)
    
    # Highlight pass (offset opposite, bright)
    painter.setPen(QColor("#E0E0E0"))
    painter.drawText(x-1, y-1, text)
```

---

## 5. SPECTRUM ANALYZER BARS (Frequency Visualization)

### Implementation with Gradient
```python
class SpectrumWidget(QWidget):
    def paintEvent(self, event):
        painter = QPainter(self)
        
        # Black background
        painter.fillRect(self.rect(), QColor("#000000"))
        
        # Draw bars for each frequency band
        width = self.width()
        height = self.height()
        bar_width = width // len(self.spectrum_data)
        
        for i, magnitude in enumerate(self.spectrum_data):
            # Normalize magnitude to 0.0-1.0
            norm_mag = min(magnitude / 32768.0, 1.0)
            bar_height = norm_mag * height
            
            # Gradient from lime green to yellow
            gradient = QLinearGradient(0, height, 0, height - bar_height)
            gradient.setColorAt(0.0, QColor("#00FF00"))    # Green at bottom
            gradient.setColorAt(1.0, QColor("#FFFF00"))    # Yellow at top
            
            # Draw bar
            bar_rect = QRect(i * bar_width, height - int(bar_height), bar_width - 1, int(bar_height))
            painter.fillRect(bar_rect, QBrush(gradient))
            
            # Smooth falloff: decay previous value toward current
            self.spectrum_data[i] = self.spectrum_data[i] * 0.85 + magnitude * 0.15
```

---

## 6. CRT/LCD/LED DISPLAY EFFECTS

### Scanline Effect (CRT Monitor)
```python
def draw_scanlines(painter, width, height, line_spacing=2):
    """Add horizontal scanlines to simulate CRT monitor"""
    painter.setPen(QPen(QColor(0, 0, 0, 25)))  # Semi-transparent black
    for y in range(0, height, line_spacing):
        painter.drawLine(0, y, width, y)
```

### LED Display Styling
```css
/* 7-segment LED style */
QLabel {
    font-family: "VT323", monospace;
    font-size: 14px;
    color: #00FF00;          /* Lime green */
    background-color: #0a0a0a;
    padding: 4px;
    border: 1px solid #1a1a1a;
}

QLabel.led-off {
    color: #003300;          /* Dark green (off) */
}
```

### Glow/Bloom Effect (Neon)
```python
def draw_glowing_text(painter, text, x, y, color):
    """Create neon glow effect"""
    font = QFont("VT323", 12)
    painter.setFont(font)
    
    # Main text (full opacity)
    painter.setPen(QColor(color))
    painter.drawText(x, y, text)
    
    # Glow layers (decreasing opacity)
    for offset in range(1, 4):
        alpha = 100 - (offset * 30)
        glow_color = QColor(color)
        glow_color.setAlpha(alpha)
        painter.setPen(glow_color)
        painter.drawText(x-offset, y-offset, text)
        painter.drawText(x+offset, y+offset, text)
```

---

## 7. PANEL BACKGROUNDS WITH TEXTURE

### Win95/Y2K Blend
```python
def create_panel_gradient():
    """Create modern dark panel with retro character"""
    gradient = QLinearGradient(0, 0, 0, panel_height)
    
    # Dark gray gradient
    gradient.setColorAt(0.0, QColor("#1a1a1a"))
    gradient.setColorAt(1.0, QColor("#0a0a0a"))
    
    return gradient

# Apply with subtle vaporwave overlay
def paint_panel(painter, rect, height):
    painter.fillRect(rect, QBrush(create_panel_gradient()))
    
    # Optional: Add very subtle vaporwave tint (5-10% opacity)
    vape_gradient = create_vaporwave_gradient(rect.width(), rect.height())
    vape_brush = QBrush(vape_gradient)
    painter.setOpacity(0.08)  # Very subtle
    painter.fillRect(rect, vape_brush)
    painter.setOpacity(1.0)
```

### Beveled Panel Border
```python
def draw_panel_border(painter, rect):
    """Inset panel with 3D bevel"""
    # Top/left highlight
    painter.setPen(QPen(QColor("#FFFFFF"), 1))
    painter.drawLine(rect.topLeft(), rect.topRight())
    painter.drawLine(rect.topLeft(), rect.bottomLeft())
    
    # Bottom/right shadow
    painter.setPen(QPen(QColor("#333333"), 1))
    painter.drawLine(rect.topRight(), rect.bottomRight())
    painter.drawLine(rect.bottomLeft(), rect.bottomRight())
```

---

## 8. FONT RECOMMENDATIONS

### Primary Font Stack
1. **Pixel/Retro Style**: `VT323` (monospace pixel font) - BEST for Winamp aesthetic
2. **System Fallback**: `Verdana` 11px (universal across OS)
3. **Y2K Alternative**: `Orbitron` (geometric, futuristic)

### Font Sizes
| Element | Font | Size | Weight |
|---------|------|------|--------|
| Window Title | VT323 or Verdana | 12px | Bold |
| Buttons | VT323 or Verdana | 10px | Normal |
| Display Numbers | VT323 | 14px | Bold (monospace) |
| Panel Labels | VT323 | 11px | Normal |
| Headings | Orbitron | 16px | Bold |

### CSS Font Application
```css
QMainWindow, QWidget {
    font-family: "VT323", Verdana, monospace;
    font-size: 11px;
}

QLabel.title {
    font-family: "VT323", Verdana, monospace;
    font-size: 12px;
    font-weight: bold;
}

QLabel.numeric {
    font-family: "VT323", monospace;
    font-size: 14px;
    font-weight: bold;
}
```

---

## 9. COMPLETE IMPLEMENTATION CHECKLIST

### Visualization Components
- [ ] Oscilloscope widget using QPainter.drawLines()
- [ ] Spectrum analyzer with gradient bars (#00FF00 → #FFFF00)
- [ ] Black (#000000) backgrounds for all visualizations
- [ ] Lime green (#00FF00) as primary color

### UI Controls
- [ ] Windows 95 beveled buttons (white highlight, gray shadow)
- [ ] Pressed state with inverted bevels
- [ ] Hover states with slightly lighter background

### Panels & Containers
- [ ] Dark background gradient (#1a1a1a → #0a0a0a)
- [ ] Inset border with bevels (white top-left, gray bottom-right)
- [ ] Optional scanlines for CRT effect

### Typography
- [ ] VT323 font family (fallback to Verdana)
- [ ] Green text (#00FF00) on dark backgrounds
- [ ] Proper sizing for readability

### Color Consistency
- [ ] Use color constants to maintain palette
- [ ] Neon colors: #00FF00, #00FFFF, #FF00FF, #FFFF00
- [ ] Background colors: #000000, #1a1a1a, #2a2a2a
- [ ] Control colors: #FFFFFF (highlight), #808080 (shadow), #C0C0C0 (face)

---

## 10. QUICK START CODE

```python
from PyQt6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QPushButton, QLabel
from PyQt6.QtGui import QPainter, QPen, QColor, QLinearGradient, QBrush
from PyQt6.QtCore import Qt

# Color constants
COLORS = {
    'GREEN': '#00FF00',
    'CYAN': '#00FFFF',
    'BLACK': '#000000',
    'BUTTON_FACE': '#C0C0C0',
    'HIGHLIGHT': '#FFFFFF',
    'SHADOW': '#808080',
}

class OscilloscopeWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.waveform_points = []
    
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.fillRect(self.rect(), QColor(COLORS['BLACK']))
        painter.setPen(QPen(QColor(COLORS['GREEN']), 1))
        painter.drawLines(self.waveform_points)
    
    def set_waveform(self, samples):
        width, height = self.width(), self.height()
        self.waveform_points = [
            (i * width // len(samples), 
             height // 2 - int(s * height // 2))
            for i, s in enumerate(samples)
        ]
        self.update()

# Apply stylesheet
STYLESHEET = """
QMainWindow {
    background-color: #1a1a1a;
}

QPushButton {
    background-color: #C0C0C0;
    border: 2px solid;
    border-top-color: #FFFFFF;
    border-left-color: #FFFFFF;
    border-bottom-color: #808080;
    border-right-color: #808080;
    color: #000000;
    font: 10px "Verdana";
    padding: 4px;
}

QPushButton:pressed {
    border-top-color: #808080;
    border-bottom-color: #FFFFFF;
}

QLabel {
    color: #00FF00;
    font-family: "VT323", monospace;
    font-size: 12px;
}
"""
```

---

## TECHNICAL SUMMARY

| Aspect | Value | Implementation |
|--------|-------|-----------------|
| **Waveform Type** | Line segments | QPainter.drawLines() |
| **Primary Color** | #00FF00 | QColor("#00FF00") |
| **Background** | #000000 | fillRect() with black |
| **Button Bevel** | White top/left, gray bottom/right | QSS border or QPainter |
| **Gradient** | QLinearGradient | Multi-stop color transitions |
| **Font** | VT323 (pixel) / Verdana (system) | QFont class |
| **Panel** | #1a1a1a → #0a0a0a | Linear gradient |
| **CRT Effect** | Scanlines at 2-4px spacing | QPainter.drawLine() loop |

