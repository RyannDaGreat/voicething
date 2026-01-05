# Windows Aero UI - PyQt6 Quick Reference

Fast lookup for the most essential Aero styling values and implementations.

## Color Values Cheat Sheet

### Gray Aero (Default)
```
Top highlight:    #B5B9BC  rgb(181, 185, 188)
Bright mid:       #F0F0F0  rgb(240, 240, 240)
Mid-tone:         #D8D8D8  rgb(216, 216, 216)
Bottom shadow:    #D3D3D3  rgb(211, 211, 211)
Border:           #888888  rgb(136, 136, 136)
```

### Blue Aero Theme
```
Primary blue:     #0689E4  rgb(6, 137, 228)
Secondary blue:   #1299CA  rgb(18, 153, 202)
Light cyan:       #6FD7EC  rgb(111, 215, 236)
Dark blue:        #003C78  rgb(0, 60, 120)
```

## Copy-Paste Stylesheets

### Glossy Button (Gray)
```css
QPushButton {
    background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
        stop: 0 #FFFFFF,
        stop: 0.4 #F0F0F0,
        stop: 0.5 #E0E0E0,
        stop: 1.0 #D0D0D0);
    border: 1px solid #888888;
    border-top: 1px solid rgba(255, 255, 255, 0.8);
    border-radius: 4px;
    padding: 5px 15px;
}

QPushButton:hover {
    background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
        stop: 0 #FFFACD,
        stop: 0.4 #F5F5F0,
        stop: 0.5 #E8E8DC,
        stop: 1.0 #D8D8C8);
}

QPushButton:pressed {
    background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
        stop: 0 #D8D8D8,
        stop: 0.5 #B0B0B0,
        stop: 1.0 #FFFFFF);
}
```

### Glossy Button (Blue Aero)
```css
QPushButton {
    background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
        stop: 0 #FFFFFF,
        stop: 0.3 #C9EBF5,
        stop: 0.7 #0689E4,
        stop: 1.0 #003C78);
    border: 1px solid #0050A0;
    border-top: 1px solid rgba(255, 255, 255, 0.8);
    border-radius: 5px;
    padding: 6px 16px;
    color: #FFFFFF;
}
```

### Glass Panel
```css
QWidget {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
        stop: 0.0 #B5B9BC,
        stop: 0.2 #F0F0F0,
        stop: 0.5 #D8D8D8,
        stop: 1.0 #D3D3D3);
    border: 1px solid #888888;
    border-radius: 4px;
}
```

### Scrollbar (Aero)
```css
QScrollBar:vertical {
    background: #F0F0F0;
    width: 12px;
}

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

QScrollBar::handle:vertical:hover {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
        stop: 0 #DDDDDD,
        stop: 0.5 #BBBBBB,
        stop: 1.0 #999999);
}
```

### Beveled Button (3D Effect)
```css
QPushButton {
    background-color: #D0D0D0;
    border: 2px outset #CCCCCC;
    border-top-color: #FFFFFF;
    border-left-color: #FFFFFF;
    border-bottom-color: #808080;
    border-right-color: #808080;
    padding: 4px 12px;
}

QPushButton:pressed {
    border: 2px inset #999999;
    border-top-color: #808080;
    border-left-color: #808080;
    border-bottom-color: #FFFFFF;
    border-right-color: #FFFFFF;
}
```

### Translucent Glass Panel
```css
QWidget {
    background-color: rgba(200, 220, 240, 191);
    border: 1px solid rgba(173, 216, 230, 100);
    border-top: 1px solid rgba(255, 255, 255, 0.6);
    border-radius: 4px;
}
```

## Python Code Snippets

### QLinearGradient (Gray Glass)
```python
from PyQt6.QtGui import QLinearGradient, QColor
from PyQt6.QtCore import QPointF

gradient = QLinearGradient(QPointF(0, 0), QPointF(0, height))
gradient.setColorAt(0.0, QColor(181, 185, 188))    # #B5B9BC
gradient.setColorAt(0.2, QColor(240, 240, 240))    # #F0F0F0
gradient.setColorAt(0.5, QColor(216, 216, 216))    # #D8D8D8
gradient.setColorAt(1.0, QColor(211, 211, 211))    # #D3D3D3
```

### QRadialGradient (Orb Button)
```python
from PyQt6.QtGui import QRadialGradient, QColor
from PyQt6.QtCore import QPointF

grad = QRadialGradient(
    QPointF(width * 0.4, height * 0.4),  # Focal point (40% from top-left)
    max(width, height) / 2                # Radius to edge
)

grad.setColorAt(0.0, QColor(255, 255, 255))     # White center
grad.setColorAt(0.2, QColor(200, 230, 255))     # Pale blue
grad.setColorAt(0.4, QColor(100, 200, 255))     # Light blue
grad.setColorAt(0.6, QColor(50, 150, 200))      # Medium blue
grad.setColorAt(0.8, QColor(20, 100, 150))      # Dark blue
grad.setColorAt(1.0, QColor(5, 40, 80))         # Very dark edge
```

### Enable Window Translucency
```python
from PyQt6.QtCore import Qt

widget.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
widget.setWindowFlags(Qt.WindowType.FramelessWindowHint)
```

## Key Implementation Rules

1. **Gradient Stops**: Always use 4+ stops for smooth glossy effect
   - Stop 0: Bright highlight (white or light)
   - Stop 0.3-0.4: Mid-bright transition
   - Stop 0.5-0.7: Main color
   - Stop 1.0: Shadow/dark edge

2. **Border-radius Limits**: Max value = half the element width
   - Width 10px → max radius 4px or 5px
   - Width 12px → max radius 5px
   - Higher values cause flat appearance

3. **RGBA Transparency Scales**:
   - 255 = 100% (fully opaque)
   - 191 = 75% (lightly transparent, good for glass)
   - 127 = 50% (moderately transparent)
   - 64 = 25% (highly transparent)

4. **Inner Glow Effect**: Use semi-transparent white top border
   ```
   border-top: 1px solid rgba(255, 255, 255, 0.6);  /* 60% white */
   ```

5. **Hover/Pressed States**: Invert gradient or brighten colors
   - Hover: brighten highlights, shift colors warmer
   - Pressed: invert gradient (dark top, bright bottom)

## Gradient Direction Reference

### Vertical (Top to Bottom)
```
qlineargradient(x1:0, y1:0, x2:0, y2:1, ...)
               [top-left]      [bottom-right]
```

### Horizontal (Left to Right)
```
qlineargradient(x1:0, y1:0, x2:1, y2:0, ...)
               [top-left]      [top-right]
```

### Diagonal (Top-left to Bottom-right)
```
qlineargradient(x1:0, y1:0, x2:1, y2:1, ...)
```

## Troubleshooting

### Glossy effect looks flat
- Check if you have 4+ gradient stops
- Ensure top stop is light (#FFFFFF or #FFFACD)
- Verify gradient direction (y1:0 to y2:1 for vertical)

### Scrollbar handle looks square
- Reduce border-radius (must be < half width)
- Width 12px: try border-radius 4px or 5px

### Border-style inset/outset not visible
- Increase border-width to minimum 2px
- Adjust colors for better contrast

### Transparency not working
- Set `WA_TranslucentBackground` attribute
- Use `rgba()` format, not `rgb()`
- Set background opacity 0-255 or 0-100%

### Radial gradients not rendering in SVG
- Add `r="0.5"` attribute to SVG radialGradient element

## File Locations

- **Full Implementation Guide**: `AERO_IMPLEMENTATION_GUIDE.md`
- **Code Examples**: `aero_pyqt6_examples.py`
- **This Quick Reference**: `AERO_QUICK_REFERENCE.md`

Run examples with:
```bash
python3 aero_pyqt6_examples.py
```

## Essential References

- [Qt Stylesheet Reference](https://doc.qt.io/qt-6/stylesheet-reference.html)
- [QLinearGradient Docs](https://doc.qt.io/qt-6/qlineargradient.html)
- [7.css Framework](https://khang-nd.github.io/7.css/) - For CSS comparison
