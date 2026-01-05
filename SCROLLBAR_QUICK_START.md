# Qt Rounded Scrollbar - Quick Start Guide

## TL;DR - Copy & Paste Solutions

### Option 1: Fastest - Use Stylesheet (3 lines)

```python
stylesheet = """
QScrollBar:vertical { width: 10px; }
QScrollBar::handle:vertical { border-radius: 4px; background-color: #555; }
"""
text_edit.setStyleSheet(stylesheet)
```

**Best for:** Simple projects, don't need hover effects
**Works immediately:** Yes
**Customization:** Limited

---

### Option 2: Recommended - Custom Scrollbar Class (20 lines)

```python
from PyQt5.QtWidgets import QScrollBar
from PyQt5.QtGui import QPainter, QBrush, QColor, QPen
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QStyle

class RoundedScrollBar(QScrollBar):
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.fillRect(self.rect(), QColor(240, 240, 240))  # Track

        opt = self.initStyleOption()
        handle_rect = self.style().subControlRect(
            QStyle.CC_ScrollBar, opt, QStyle.SC_ScrollBarSlider, self
        )
        if handle_rect.isValid():
            painter.setBrush(QBrush(QColor(120, 120, 120)))
            painter.setPen(QPen(Qt.NoPen))
            painter.drawRoundedRect(handle_rect, 4, 4)

# Usage:
text_edit.setVerticalScrollBar(RoundedScrollBar(Qt.Vertical))
```

**Best for:** Single widget customization, full control
**Works immediately:** Yes
**Customization:** Full control over appearance

---

### Option 3: Professional - App-Wide Style (25 lines)

```python
from PyQt5.QtWidgets import QProxyStyle, QStyle
from PyQt5.QtGui import QPainter, QBrush, QColor, QPen

class RoundedScrollBarStyle(QProxyStyle):
    def drawComplexControl(self, control, option, painter, widget=None):
        if control == QStyle.CC_ScrollBar:
            painter.setRenderHint(QPainter.Antialiasing)
            painter.fillRect(option.rect, QColor(240, 240, 240))

            handle_rect = self.subControlRect(
                control, option, QStyle.SC_ScrollBarSlider, widget
            )
            if handle_rect.isValid():
                painter.setBrush(QBrush(QColor(100, 100, 100)))
                painter.setPen(QPen(Qt.NoPen))
                painter.drawRoundedRect(handle_rect, 4, 4)
        else:
            super().drawComplexControl(control, option, painter, widget)

# Usage:
app = QApplication([])
app.setStyle(RoundedScrollBarStyle())
```

**Best for:** App-wide scrollbar styling
**Works immediately:** Yes
**Customization:** Full control, affects all scrollbars

---

## Critical Implementation Details

### 1. The Magic Number: Corner Radius

For truly round corners, the corner radius should be **half the scrollbar width**:

```python
width = 10  # pixels
corner_radius = width // 2  # 5 pixels
painter.drawRoundedRect(rect, corner_radius, corner_radius)
```

If the radius is too large relative to width, you won't get a smooth rounded appearance.

### 2. Getting the Handle Rectangle

The handle rectangle must come from the style system, not calculated manually:

```python
# CORRECT - Use style system
opt = self.initStyleOption()
handle_rect = self.style().subControlRect(
    QStyle.CC_ScrollBar,
    opt,
    QStyle.SC_ScrollBarSlider,
    self
)

# WRONG - Don't hardcode or guess
# handle_rect = QRect(0, 10, self.width(), 50)  # DON'T DO THIS
```

### 3. Antialiasing Required

Always enable antialiasing for smooth rounded corners:

```python
painter = QPainter(self)
painter.setRenderHint(QPainter.Antialiasing)  # REQUIRED
```

### 4. Track vs Handle

For clean appearance, paint the track (background) and handle separately:

```python
# Track - full scrollbar background
painter.fillRect(self.rect(), track_color)

# Handle - the movable slider part
painter.drawRoundedRect(handle_rect, radius, radius)
```

### 5. Hide Arrow Buttons

Most rounded scrollbar designs hide up/down arrows with stylesheets:

```css
QScrollBar::add-line:vertical {
    height: 0px;  /* This hides the button */
}
QScrollBar::sub-line:vertical {
    height: 0px;  /* This hides the button */
}
```

---

## Testing Your Implementation

Create a test window with lots of content:

```python
from PyQt5.QtWidgets import QApplication, QMainWindow, QTextEdit

app = QApplication([])
window = QMainWindow()
text = QTextEdit("Line\n" * 200)  # Lots of content to scroll

# Apply your scrollbar implementation here
# ...

window.setCentralWidget(text)
window.resize(400, 600)
window.show()
app.exec_()
```

**Verify these work:**
- [ ] Handle has rounded corners (not sharp)
- [ ] Handle moves smoothly as you scroll
- [ ] Handle resizes correctly with content length
- [ ] No visual artifacts or flicker
- [ ] Looks consistent on Windows/Mac/Linux

---

## Common Pitfalls

### Pitfall 1: Sharp Corners Instead of Rounded

**Symptom:** Handle corners still look sharp
**Cause:** Corner radius too small or antialiasing disabled

```python
# FIX
painter.setRenderHint(QPainter.Antialiasing)  # Must have this
painter.drawRoundedRect(rect, 5, 5)  # Must have both radii
```

### Pitfall 2: Handle Rectangle Is Wrong Size

**Symptom:** Handle is tiny or full-size regardless of content
**Cause:** Not using style's subControlRect()

```python
# WRONG
handle_rect = QRect(0, 0, 10, 50)

# CORRECT
opt = self.initStyleOption()
handle_rect = self.style().subControlRect(
    QStyle.CC_ScrollBar, opt, QStyle.SC_ScrollBarSlider, self
)
```

### Pitfall 3: Stylesheet Border-Radius Not Working

**Symptom:** Stylesheet radius has no effect
**Cause:** Width and radius mismatch

```css
/* WRONG - width too small for radius */
QScrollBar:vertical {
    width: 4px;
}
QScrollBar::handle:vertical {
    border-radius: 4px;  /* Won't work */
}

/* CORRECT - width and radius proportional */
QScrollBar:vertical {
    width: 10px;
}
QScrollBar::handle:vertical {
    border-radius: 5px;  /* width/2 */
}
```

### Pitfall 4: Handle Hidden or Invisible

**Symptom:** Scrollbar background is visible but no handle
**Cause:** Handle color matches background or pen is wrong

```python
# WRONG
painter.setBrush(QBrush(QColor(240, 240, 240)))  # Same as background!
painter.drawRoundedRect(handle_rect, 4, 4)

# CORRECT
painter.setBrush(QBrush(QColor(100, 100, 100)))  # Visible
painter.setPen(QPen(Qt.NoPen))  # No outline
painter.drawRoundedRect(handle_rect, 4, 4)
```

### Pitfall 5: Stylesheet Hides Handle Background

**Symptom:** Scrollbar appears checkered or with pattern
**Cause:** sub-page and add-page not hidden

```css
/* MUST ADD THESE */
QScrollBar::sub-page:vertical {
    background: none;
}
QScrollBar::add-page:vertical {
    background: none;
}
```

---

## Performance Considerations

Scrollbar painting happens frequently (on every mouse movement), so:

1. **Keep paintEvent() fast** - avoid complex calculations
2. **Cache colors** - use class constants, not QColor() every frame
3. **Minimal antialiasing** - only on handle, not the entire rect
4. **Reuse QStyleOptionSlider** - don't create new one each paint

```python
class RoundedScrollBar(QScrollBar):
    # Cache colors as class variables
    HANDLE_COLOR = QColor(120, 120, 120)
    TRACK_COLOR = QColor(240, 240, 240)

    def paintEvent(self, event):
        # Fast implementation
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.fillRect(self.rect(), self.TRACK_COLOR)

        # Minimal operations
        opt = self.initStyleOption()
        handle_rect = self.style().subControlRect(...)
        painter.setBrush(QBrush(self.HANDLE_COLOR))
        painter.drawRoundedRect(handle_rect, 4, 4)
```

---

## Which Approach Should I Use?

| Use Case | Recommended |
|----------|-------------|
| Quick prototype, simple styling | **Stylesheet** |
| Single widget with custom look | **QScrollBar subclass** |
| App-wide consistent styling | **QProxyStyle** |
| Complex animations/states | **QProxyStyle** |
| Minimal code, no customization | **Stylesheet** |

---

## Complete Runnable Example

See `scrollbar_examples.py` in this directory for complete working code with all three approaches.

Run any approach:
```bash
python scrollbar_examples.py stylesheet
python scrollbar_examples.py subclass
python scrollbar_examples.py proxystyle
```

---

## References

- Qt Documentation: [QScrollBar](https://doc.qt.io/qt-5/qscrollbar.html)
- Qt Documentation: [QProxyStyle](https://doc.qt.io/qt-6/qproxystyle.html)
- Qt Documentation: [QStyle](https://doc.qt.io/qt-6/qstyle.html)
- PyQt5 Documentation: [QtWidgets](https://www.riverbankcomputing.com/static/Docs/PyQt5/api/qtwidgets/index.html)
