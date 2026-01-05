# Advanced Rounded Scrollbar Customization

Advanced techniques and edge cases for Qt scrollbar customization.

---

## 1. Hover Effects

### Using QProxyStyle with State Detection

```python
from PyQt5.QtWidgets import QProxyStyle, QStyle
from PyQt5.QtGui import QPainter, QBrush, QColor, QPen

class InteractiveScrollBarStyle(QProxyStyle):
    """Scrollbar with hover and pressed states."""

    def drawComplexControl(self, control, option, painter, widget=None):
        if control == QStyle.CC_ScrollBar:
            painter.setRenderHint(QPainter.Antialiasing)

            # Track
            painter.fillRect(option.rect, QColor(240, 240, 240))

            # Handle with state-based color
            handle_rect = self.subControlRect(
                control, option, QStyle.SC_ScrollBarSlider, widget
            )

            if handle_rect.isValid():
                # State detection
                if option.state & QStyle.State_Sunken:
                    color = QColor(40, 40, 40)  # Pressed
                elif option.state & QStyle.State_MouseOver:
                    color = QColor(70, 70, 70)  # Hovered
                else:
                    color = QColor(110, 110, 110)  # Normal

                painter.setBrush(QBrush(color))
                painter.setPen(QPen(Qt.NoPen))
                painter.drawRoundedRect(handle_rect, 4, 4)
        else:
            super().drawComplexControl(control, option, painter, widget)
```

### Using QScrollBar Subclass with Event Tracking

```python
from PyQt5.QtWidgets import QScrollBar
from PyQt5.QtGui import QPainter, QBrush, QColor, QPen
from PyQt5.QtCore import Qt, QRect

class InteractiveRoundedScrollBar(QScrollBar):
    """Scrollbar with hover effect."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.is_hovered = False

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # Track
        painter.fillRect(self.rect(), QColor(240, 240, 240))

        # Handle with hover color
        opt = self.initStyleOption()
        handle_rect = self.style().subControlRect(
            QStyle.CC_ScrollBar, opt, QStyle.SC_ScrollBarSlider, self
        )

        if handle_rect.isValid():
            color = QColor(70, 70, 70) if self.is_hovered else QColor(120, 120, 120)
            painter.setBrush(QBrush(color))
            painter.setPen(QPen(Qt.NoPen))
            painter.drawRoundedRect(handle_rect, 4, 4)

    def enterEvent(self, event):
        self.is_hovered = True
        self.update()
        super().enterEvent(event)

    def leaveEvent(self, event):
        self.is_hovered = False
        self.update()
        super().leaveEvent(event)
```

---

## 2. Gradient Handle

### Subtle Gradient for Depth

```python
from PyQt5.QtGui import QLinearGradient

class GradientScrollBar(QScrollBar):
    """Scrollbar with gradient-filled handle."""

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # Track
        painter.fillRect(self.rect(), QColor(240, 240, 240))

        # Get handle rect
        opt = self.initStyleOption()
        handle_rect = self.style().subControlRect(
            QStyle.CC_ScrollBar, opt, QStyle.SC_ScrollBarSlider, self
        )

        if handle_rect.isValid():
            # Create gradient
            gradient = QLinearGradient(
                handle_rect.topLeft(),
                handle_rect.bottomRight()
            )
            gradient.setColorAt(0.0, QColor(150, 150, 150))
            gradient.setColorAt(1.0, QColor(80, 80, 80))

            # Draw with gradient
            painter.setBrush(gradient)
            painter.setPen(QPen(Qt.NoPen))
            painter.drawRoundedRect(handle_rect, 4, 4)
```

---

## 3. Shadow/Blur Effect

### Soft Shadow Around Handle

```python
from PyQt5.QtGui import QColor

class ShadowScrollBar(QScrollBar):
    """Scrollbar with subtle shadow effect."""

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # Track
        painter.fillRect(self.rect(), QColor(245, 245, 245))

        # Handle
        opt = self.initStyleOption()
        handle_rect = self.style().subControlRect(
            QStyle.CC_ScrollBar, opt, QStyle.SC_ScrollBarSlider, self
        )

        if handle_rect.isValid():
            # Shadow pass - offset and semi-transparent
            shadow_rect = handle_rect.adjusted(-1, -1, 1, 1)
            painter.setBrush(QBrush(QColor(0, 0, 0, 30)))
            painter.setPen(QPen(Qt.NoPen))
            painter.drawRoundedRect(shadow_rect, 5, 5)

            # Main handle
            painter.setBrush(QBrush(QColor(120, 120, 120)))
            painter.setPen(QPen(Qt.NoPen))
            painter.drawRoundedRect(handle_rect, 4, 4)

            # Optional highlight - top-left edge
            highlight_color = QColor(255, 255, 255, 60)
            painter.setBrush(QBrush(highlight_color))
            painter.drawRoundedRect(
                handle_rect.adjusted(0, 0, 0, handle_rect.height() // 2),
                4, 4
            )
```

---

## 4. Horizontal Scrollbar

### Adding Horizontal Support

```python
class FullRoundedScrollBar(QScrollBar):
    """Works for both vertical and horizontal."""

    HANDLE_COLOR = QColor(120, 120, 120)
    TRACK_COLOR = QColor(240, 240, 240)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # Track
        painter.fillRect(self.rect(), self.TRACK_COLOR)

        # Handle - works for both orientations
        opt = self.initStyleOption()
        handle_rect = self.style().subControlRect(
            QStyle.CC_ScrollBar, opt, QStyle.SC_ScrollBarSlider, self
        )

        if handle_rect.isValid():
            painter.setBrush(QBrush(self.HANDLE_COLOR))
            painter.setPen(QPen(Qt.NoPen))
            painter.drawRoundedRect(handle_rect, 4, 4)

# Usage:
text_edit = QTextEdit()
text_edit.setVerticalScrollBar(FullRoundedScrollBar(Qt.Vertical))
text_edit.setHorizontalScrollBar(FullRoundedScrollBar(Qt.Horizontal))
```

---

## 5. Custom Colors Per Direction

### Different Colors for V and H Scrollbars

```python
class ColorfulScrollBar(QScrollBar):
    """Vertical and horizontal scrollbars with different colors."""

    COLORS = {
        Qt.Vertical: QColor(100, 150, 200),      # Blue
        Qt.Horizontal: QColor(200, 100, 150),    # Pink
    }

    def __init__(self, orientation, parent=None):
        super().__init__(orientation, parent)
        self.orientation = orientation

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # Track
        painter.fillRect(self.rect(), QColor(240, 240, 240))

        # Handle
        opt = self.initStyleOption()
        handle_rect = self.style().subControlRect(
            QStyle.CC_ScrollBar, opt, QStyle.SC_ScrollBarSlider, self
        )

        if handle_rect.isValid():
            color = self.COLORS.get(self.orientation, QColor(120, 120, 120))
            painter.setBrush(QBrush(color))
            painter.setPen(QPen(Qt.NoPen))
            painter.drawRoundedRect(handle_rect, 4, 4)
```

---

## 6. Thin Scrollbar (macOS-like)

### Minimal Scrollbar that Expands on Hover

```python
class ThinScrollBar(QScrollBar):
    """Thin scrollbar that grows on hover (macOS-like)."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.is_hovered = False
        self.setMinimumWidth(5)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # No track - just handle
        opt = self.initStyleOption()
        handle_rect = self.style().subControlRect(
            QStyle.CC_ScrollBar, opt, QStyle.SC_ScrollBarSlider, self
        )

        if handle_rect.isValid():
            # Expand if hovered
            if self.is_hovered:
                handle_rect = handle_rect.adjusted(-2, 0, 2, 0)
                color = QColor(100, 100, 100)
            else:
                color = QColor(150, 150, 150)

            painter.setBrush(QBrush(color))
            painter.setPen(QPen(Qt.NoPen))
            painter.drawRoundedRect(handle_rect, 3, 3)

    def enterEvent(self, event):
        self.is_hovered = True
        self.update()

    def leaveEvent(self, event):
        self.is_hovered = False
        self.update()
```

---

## 7. Animated Scrollbar (Advanced)

### Fade-in/Out Animation

```python
from PyQt5.QtCore import QTimer, QPropertyAnimation
from PyQt5.QtWidgets import QScrollBar

class AnimatedScrollBar(QScrollBar):
    """Scrollbar with fade animation."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.is_hovered = False
        self.opacity = 0.5
        self.animation = None

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        opt = self.initStyleOption()
        handle_rect = self.style().subControlRect(
            QStyle.CC_ScrollBar, opt, QStyle.SC_ScrollBarSlider, self
        )

        if handle_rect.isValid():
            # Color with opacity
            color = QColor(120, 120, 120)
            color.setAlphaF(self.opacity)

            painter.setBrush(QBrush(color))
            painter.setPen(QPen(Qt.NoPen))
            painter.drawRoundedRect(handle_rect, 4, 4)

    def enterEvent(self, event):
        self.is_hovered = True
        self._animate_opacity(1.0)

    def leaveEvent(self, event):
        self.is_hovered = False
        self._animate_opacity(0.3)

    def _animate_opacity(self, target):
        if self.animation:
            self.animation.stop()

        self.animation = QPropertyAnimation(self, b"opacity")
        self.animation.setDuration(200)
        self.animation.setEndValue(target)
        self.animation.start()
```

---

## 8. Disabled State

### Show Different Appearance When Disabled

```python
class SmartScrollBar(QScrollBar):
    """Scrollbar aware of disabled state."""

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # Track
        track_color = QColor(200, 200, 200) if not self.isEnabled() else QColor(240, 240, 240)
        painter.fillRect(self.rect(), track_color)

        # Handle
        opt = self.initStyleOption()
        handle_rect = self.style().subControlRect(
            QStyle.CC_ScrollBar, opt, QStyle.SC_ScrollBarSlider, self
        )

        if handle_rect.isValid():
            if not self.isEnabled():
                color = QColor(180, 180, 180)
                alpha = 0.4
            else:
                color = QColor(120, 120, 120)
                alpha = 1.0

            color.setAlphaF(alpha)
            painter.setBrush(QBrush(color))
            painter.setPen(QPen(Qt.NoPen))
            painter.drawRoundedRect(handle_rect, 4, 4)
```

---

## 9. Minimal Padding Style

### Hide Empty Space Between Handle and Arrows

```python
class CompactScrollBar(QScrollBar):
    """Scrollbar with no padding."""

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # Use full rect (no margins)
        painter.fillRect(self.rect(), QColor(245, 245, 245))

        # Full-height handle
        opt = self.initStyleOption()
        handle_rect = self.style().subControlRect(
            QStyle.CC_ScrollBar, opt, QStyle.SC_ScrollBarSlider, self
        )

        if handle_rect.isValid():
            painter.setBrush(QBrush(QColor(110, 110, 110)))
            painter.setPen(QPen(Qt.NoPen))
            # Minimal radius for compact look
            painter.drawRoundedRect(handle_rect, 2, 2)
```

---

## 10. Platform-Specific Styling

### Different Look for Windows/Mac/Linux

```python
import sys
from PyQt5.QtGui import QColor

class PlatformScrollBar(QScrollBar):
    """Platform-aware scrollbar styling."""

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # Platform-specific colors
        if sys.platform == "darwin":  # macOS
            track_color = QColor(235, 235, 235)
            handle_color = QColor(140, 140, 140)
        elif sys.platform == "win32":  # Windows
            track_color = QColor(240, 240, 240)
            handle_color = QColor(120, 120, 120)
        else:  # Linux
            track_color = QColor(245, 245, 245)
            handle_color = QColor(100, 100, 100)

        painter.fillRect(self.rect(), track_color)

        opt = self.initStyleOption()
        handle_rect = self.style().subControlRect(
            QStyle.CC_ScrollBar, opt, QStyle.SC_ScrollBarSlider, self
        )

        if handle_rect.isValid():
            painter.setBrush(QBrush(handle_color))
            painter.setPen(QPen(Qt.NoPen))
            painter.drawRoundedRect(handle_rect, 4, 4)
```

---

## 11. Combining Stylesheet + Subclass

### Hybrid Approach - Best of Both Worlds

```python
class HybridScrollBar(QScrollBar):
    """Use stylesheet for basic structure, subclass for rounded painting."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Stylesheet handles size and adds padding
        self.setStyleSheet("""
            QScrollBar:vertical {
                width: 12px;
                background: #f5f5f5;
            }
            QScrollBar::add-line:vertical { height: 0px; }
            QScrollBar::sub-line:vertical { height: 0px; }
        """)

    def paintEvent(self, event):
        # Let stylesheet paint first
        # super().paintEvent(event)  # Uncomment to layer on top

        # Add custom rounded painting
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        opt = self.initStyleOption()
        handle_rect = self.style().subControlRect(
            QStyle.CC_ScrollBar, opt, QStyle.SC_ScrollBarSlider, self
        )

        if handle_rect.isValid():
            painter.setBrush(QBrush(QColor(120, 120, 120)))
            painter.setPen(QPen(Qt.NoPen))
            painter.drawRoundedRect(handle_rect, 4, 4)
```

---

## 12. Testing Multiple Widgets

### Test Harness for Comparison

```python
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel, QTextEdit

class ScrollBarTestWindow(QMainWindow):
    """Compare different scrollbar styles side-by-side."""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Scrollbar Comparison")
        self.resize(800, 600)

        layout = QVBoxLayout()

        # Test different implementations
        styles = [
            ("Gradient", GradientScrollBar),
            ("Shadow", ShadowScrollBar),
            ("Hover", InteractiveRoundedScrollBar),
            ("Thin", ThinScrollBar),
        ]

        for name, scrollbar_class in styles:
            label = QLabel(name)
            text = QTextEdit("Content\n" * 50)
            text.setVerticalScrollBar(scrollbar_class(Qt.Vertical))
            layout.addWidget(label)
            layout.addWidget(text)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)
```

---

## Performance Optimization

### Caching Style Option

```python
class OptimizedScrollBar(QScrollBar):
    """Optimized version with cached operations."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._cached_handle_rect = None
        self._last_value = 0

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        painter.fillRect(self.rect(), QColor(240, 240, 240))

        # Recompute handle rect only if value changed
        if self.value() != self._last_value:
            opt = self.initStyleOption()
            self._cached_handle_rect = self.style().subControlRect(
                QStyle.CC_ScrollBar, opt, QStyle.SC_ScrollBarSlider, self
            )
            self._last_value = self.value()

        if self._cached_handle_rect and self._cached_handle_rect.isValid():
            painter.setBrush(QBrush(QColor(120, 120, 120)))
            painter.setPen(QPen(Qt.NoPen))
            painter.drawRoundedRect(self._cached_handle_rect, 4, 4)
```

---

## Troubleshooting Advanced Scenarios

### Issue: Scrollbar Repaints Too Often

**Solution:** Use `update()` only when necessary, not on every mouse event.

```python
def mouseMoveEvent(self, event):
    # Don't call update() on every mouse move
    # Only update when entering/leaving
    super().mouseMoveEvent(event)
```

### Issue: Gradient Doesn't Look Right

**Solution:** Ensure gradient endpoints match handle rect:

```python
# WRONG - gradient endpoints hardcoded
gradient = QLinearGradient(0, 0, 0, 100)

# CORRECT - use actual rect dimensions
gradient = QLinearGradient(
    handle_rect.topLeft(),
    handle_rect.bottomRight()
)
```

### Issue: Rounded Corners Get Clipped

**Solution:** Ensure handle rect has space for corner radius:

```python
# The corner radius must fit within the rect
corner_radius = 4
if handle_rect.width() < 2 * corner_radius:
    # Handle too small, draw without radius
    painter.drawRect(handle_rect)
else:
    painter.drawRoundedRect(handle_rect, corner_radius, corner_radius)
```

---

## Integration with Existing Code

Quick way to add rounded scrollbars to existing widgets:

```python
# For a single QTextEdit
text_edit.setVerticalScrollBar(RoundedScrollBar(Qt.Vertical))

# For all widgets in a layout
for widget in layout.widgets():
    if hasattr(widget, 'setVerticalScrollBar'):
        widget.setVerticalScrollBar(RoundedScrollBar(Qt.Vertical))

# For entire application
app.setStyle(RoundedScrollBarStyle())
```

---

## Summary

Advanced techniques covered:
- Hover/pressed states
- Gradients and shadows
- Horizontal support
- Custom colors
- Animations
- Platform-specific styling
- Hybrid stylesheet+subclass
- Performance optimization
- Troubleshooting

Choose the technique that fits your use case. Start simple, add complexity only as needed.
