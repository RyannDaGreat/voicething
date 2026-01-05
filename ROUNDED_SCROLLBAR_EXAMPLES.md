# Qt Rounded Scrollbar Handle Examples

## Overview
Three main approaches to implement rounded scrollbar handles in Qt/PyQt:

1. **Qt Stylesheets (CSS-like)** - Simplest, limited customization
2. **QScrollBar Subclass with paintEvent** - Custom painting with full control
3. **QProxyStyle with drawComplexControl** - Style-level customization for app-wide control

---

## Approach 1: Qt Stylesheets (Easiest)

### How It Works
Use CSS-like stylesheets with `border-radius` on the handle. The key constraint: **border-radius and scrollbar width must be proportional** for rounded appearance.

### PyQt5/6 Implementation

```python
from PyQt5.QtWidgets import QApplication, QTextEdit, QVBoxLayout, QMainWindow

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Define stylesheet with rounded scrollbar handle
        stylesheet = """
        QScrollBar:vertical {
            border: 0px solid #999999;
            background: white;
            width: 10px;
            margin: 0px 0px 0px 0px;
        }

        QScrollBar::handle:vertical {
            min-height: 20px;
            border: 0px solid red;
            border-radius: 4px;
            background-color: #555555;
        }

        QScrollBar::add-line:vertical {
            height: 0px;
            subcontrol-position: bottom;
            subcontrol-origin: margin;
        }

        QScrollBar::sub-line:vertical {
            height: 0px;
            subcontrol-position: top;
            subcontrol-origin: margin;
        }

        QScrollBar::sub-page:vertical {
            background: none;
        }

        QScrollBar::add-page:vertical {
            background: none;
        }
        """

        text_edit = QTextEdit("Some content...\n" * 100)
        text_edit.setStyleSheet(stylesheet)

        layout = QVBoxLayout()
        layout.addWidget(text_edit)

        central_widget = self.centralWidget() or QWidget()
        central_widget.setLayout(layout)
```

### Critical Notes
- `width: 10px` and `border-radius: 4px` should be proportional
- Hide sub-page/add-page backgrounds to reveal actual colors
- Works in most Qt versions but has style-specific limitations
- Cannot use background-image on scrollbars with stylesheets

### Pros/Cons
✓ Simple, no C++/complex code needed
✓ Works in modern PyQt5/6
✗ Limited customization options
✗ May have platform-specific rendering issues
✗ Cannot fully customize all scrollbar elements

---

## Approach 2: QScrollBar Subclass with paintEvent

### How It Works
Subclass QScrollBar and override `paintEvent()` to draw the handle and other elements with `QPainter.drawRoundedRect()`. You get full control over appearance.

### PyQt5/6 Implementation

```python
from PyQt5.QtWidgets import QScrollBar, QApplication, QTextEdit, QVBoxLayout, QMainWindow
from PyQt5.QtGui import QPainter, QBrush, QColor, QPen
from PyQt5.QtCore import Qt

class RoundedScrollBar(QScrollBar):
    """Custom scrollbar with rounded handle."""

    def __init__(self, orientation=Qt.Vertical, parent=None):
        super().__init__(orientation, parent)
        self.handle_color = QColor(100, 100, 100)
        self.track_color = QColor(230, 230, 230)

    def paintEvent(self, event):
        """Override paint to draw rounded corners."""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # Draw track background
        painter.fillRect(self.rect(), self.track_color)

        # Get handle geometry using style information
        opt = self.initStyleOption()
        handle_rect = self.style().subControlRect(
            self.style().CC_ScrollBar,
            opt,
            self.style().SC_ScrollBarSlider,
            self
        )

        if not handle_rect.isEmpty():
            # Draw rounded handle
            painter.setBrush(QBrush(self.handle_color))
            painter.setPen(QPen(Qt.NoPen))
            # Corner radius: 4 pixels (half the width for truly round)
            painter.drawRoundedRect(handle_rect, 4, 4)

        painter.end()

# Usage
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        text_edit = QTextEdit("Some content...\n" * 100)

        # Replace default scrollbar with custom rounded one
        custom_scrollbar = RoundedScrollBar(Qt.Vertical)
        text_edit.setVerticalScrollBar(custom_scrollbar)

        layout = QVBoxLayout()
        layout.addWidget(text_edit)

        central_widget = self.centralWidget() or QWidget()
        central_widget.setLayout(layout)
```

### Key Details
- `initStyleOption()` initializes QStyleOptionSlider with current state
- `style().subControlRect()` gets handle bounds in logical coordinates
- `drawRoundedRect(rect, xRadius, yRadius)` draws the rounded rectangle
- Both xRadius and yRadius should be ~half the scrollbar width for circular corners

### Complete Working Example

```python
from PyQt5.QtWidgets import QScrollBar, QApplication, QTextEdit, QMainWindow, QWidget, QVBoxLayout
from PyQt5.QtGui import QPainter, QBrush, QColor, QPen, QStyleOptionSlider
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QStyle

class RoundedScrollBar(QScrollBar):
    """Scrollbar with truly rounded corners on the handle."""

    HANDLE_COLOR = QColor(120, 120, 120)
    TRACK_COLOR = QColor(240, 240, 240)
    CORNER_RADIUS = 4

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing, True)

        # Draw track
        painter.fillRect(self.rect(), self.TRACK_COLOR)

        # Get handle position
        opt = QStyleOptionSlider()
        self.initStyleOption(opt)
        handle_rect = self.style().subControlRect(
            QStyle.CC_ScrollBar, opt, QStyle.SC_ScrollBarSlider, self
        )

        # Draw handle with rounded corners
        if handle_rect.isValid():
            painter.setBrush(QBrush(self.HANDLE_COLOR))
            painter.setPen(QPen(Qt.NoPen))
            painter.drawRoundedRect(
                handle_rect,
                self.CORNER_RADIUS,
                self.CORNER_RADIUS
            )

# Example app
if __name__ == '__main__':
    app = QApplication([])

    window = QMainWindow()
    text_edit = QTextEdit("Example content\n" * 50)
    text_edit.setVerticalScrollBar(RoundedScrollBar())

    window.setCentralWidget(text_edit)
    window.show()
    app.exec_()
```

### Pros/Cons
✓ Full control over appearance
✓ Can customize colors, radius, padding independently
✓ Works consistently across platforms
✗ More code than stylesheet approach
✗ Need to handle both vertical and horizontal separately
✗ Must manage all painting yourself

---

## Approach 3: QProxyStyle with drawComplexControl

### How It Works
Create a custom QProxyStyle that intercepts scrollbar drawing at the style level. Allows app-wide customization without modifying individual widgets.

### PyQt5/6 Implementation

```python
from PyQt5.QtWidgets import (
    QApplication, QProxyStyle, QStyle, QTextEdit, QMainWindow,
    QWidget, QVBoxLayout
)
from PyQt5.QtGui import QPainter, QBrush, QColor, QPen
from PyQt5.QtCore import Qt

class RoundedScrollBarStyle(QProxyStyle):
    """Custom style that draws scrollbars with rounded handles."""

    HANDLE_COLOR = QColor(100, 100, 100)
    HANDLE_HOVER_COLOR = QColor(80, 80, 80)
    TRACK_COLOR = QColor(240, 240, 240)
    CORNER_RADIUS = 4

    def drawComplexControl(self, control, option, painter, widget=None):
        """Override scrollbar drawing."""

        if control == QStyle.CC_ScrollBar:
            # We're drawing a scrollbar
            painter.setRenderHint(QPainter.Antialiasing)

            # Draw the track (background)
            painter.fillRect(option.rect, self.TRACK_COLOR)

            # Get the handle sub-control rectangle
            handle_rect = self.subControlRect(
                control, option, QStyle.SC_ScrollBarSlider, widget
            )

            if handle_rect.isValid():
                # Determine if handle is hovered
                hover_color = self.HANDLE_HOVER_COLOR \
                    if option.state & QStyle.State_MouseOver else self.HANDLE_COLOR

                # Draw rounded handle
                painter.setBrush(QBrush(hover_color))
                painter.setPen(QPen(Qt.NoPen))
                painter.drawRoundedRect(
                    handle_rect,
                    self.CORNER_RADIUS,
                    self.CORNER_RADIUS
                )

            # Handle other scrollbar elements (arrows, etc.)
            for sub_control in [
                QStyle.SC_ScrollBarAddLine,
                QStyle.SC_ScrollBarSubLine,
                QStyle.SC_ScrollBarAddPage,
                QStyle.SC_ScrollBarSubPage
            ]:
                sub_rect = self.subControlRect(control, option, sub_control, widget)
                if sub_rect.isValid():
                    # Optionally hide arrows by not drawing them
                    pass
        else:
            # For all other controls, use the base style
            super().drawComplexControl(control, option, painter, widget)

# Usage
if __name__ == '__main__':
    app = QApplication([])

    # Apply the custom style to the entire application
    app.setStyle(RoundedScrollBarStyle())

    window = QMainWindow()
    text_edit = QTextEdit("Example content\n" * 100)
    window.setCentralWidget(text_edit)
    window.show()

    app.exec_()
```

### Advanced QProxyStyle Example with State Handling

```python
from PyQt5.QtWidgets import QProxyStyle, QStyle, QApplication
from PyQt5.QtGui import QPainter, QBrush, QColor, QPen
from PyQt5.QtCore import Qt

class AdvancedRoundedScrollBarStyle(QProxyStyle):
    """Advanced scrollbar style with states and animations-ready."""

    def drawComplexControl(self, control, option, painter, widget=None):
        if control == QStyle.CC_ScrollBar:
            painter.setRenderHint(QPainter.Antialiasing)

            # Track background
            track_color = QColor(245, 245, 245)
            painter.fillRect(option.rect, track_color)

            # Handle rectangle
            handle_rect = self.subControlRect(
                control, option, QStyle.SC_ScrollBarSlider, widget
            )

            if handle_rect.isValid():
                # Color based on state
                if option.state & QStyle.State_Sunken:
                    color = QColor(60, 60, 60)  # Pressed
                elif option.state & QStyle.State_MouseOver:
                    color = QColor(90, 90, 90)  # Hovered
                else:
                    color = QColor(110, 110, 110)  # Normal

                # Draw with shadow effect (optional)
                shadow_rect = handle_rect.adjusted(-1, -1, 1, 1)
                painter.setBrush(QBrush(QColor(0, 0, 0, 20)))
                painter.setPen(QPen(Qt.NoPen))
                painter.drawRoundedRect(shadow_rect, 5, 5)

                # Draw main handle
                painter.setBrush(QBrush(color))
                painter.drawRoundedRect(handle_rect, 4, 4)
        else:
            super().drawComplexControl(control, option, painter, widget)
```

### Key Details
- Override `drawComplexControl()` to intercept CC_ScrollBar drawing
- `subControlRect()` returns rectangles for sub-elements (slider, arrows, etc.)
- Check `option.state` for State_MouseOver, State_Sunken, etc.
- Apply style app-wide with `QApplication.setStyle()`
- Always call `super().drawComplexControl()` for non-scrollbar controls

### Pros/Cons
✓ App-wide effect - affects all scrollbars automatically
✓ Can check widget state (hover, pressed, etc.)
✓ Elegant architecture for style-level customization
✗ Slightly more complex than subclassing QScrollBar
✗ State handling requires understanding QStyle option flags
✗ Harder to apply style only to specific widgets

---

## Comparison Table

| Feature | Stylesheet | QScrollBar Subclass | QProxyStyle |
|---------|-----------|-------------------|------------|
| Ease of Implementation | ✓✓✓ | ✓✓ | ✓ |
| Customization Control | ✓ | ✓✓✓ | ✓✓ |
| App-wide Effect | ✓ (if set globally) | ✗ (per-widget) | ✓✓ |
| Platform Consistency | ✓✓ | ✓✓✓ | ✓✓✓ |
| Code Complexity | Low | Medium | Medium-High |
| Hover/Press States | Limited | Possible (manual) | Built-in |
| Recommended For | Simple cases | Widget-specific control | App-wide styling |

---

## Testing Your Implementation

```python
# Simple test app for any approach
from PyQt5.QtWidgets import QApplication, QMainWindow, QTextEdit

if __name__ == '__main__':
    app = QApplication([])

    # Apply style/scrollbar here

    window = QMainWindow()
    text = QTextEdit("Line\n" * 200)
    window.setCentralWidget(text)
    window.resize(400, 600)
    window.show()

    app.exec_()
```

**Visual indicators to check:**
- Handle corners are rounded (not sharp)
- Handle moves smoothly as you scroll
- Handle size adjusts with content
- No rendering artifacts on hover
- Cross-platform appearance is consistent

---

## Sources

- [Qt Forum: Scrollbar handle with rounded edges](https://forum.qt.io/topic/101931/scrollbar-handle-with-rounded-edges)
- [Qt Forum: Customized QScrollBar](https://forum.qt.io/topic/98781/customized-qscrollbar)
- [PyQt Forum: Custom Scrollbar design](https://forum.qt.io/topic/41040/pyqt-custom-scrollbar-design-solved)
- [Qt Documentation: QProxyStyle Class](https://doc.qt.io/qt-6/qproxystyle.html)
- [Qt Documentation: QScrollBar Class](https://doc.qt.io/qt-5/qscrollbar.html)
- [Qt for Python: Styles and Style Aware Widgets](https://doc.qt.io/qtforpython-6.5/PySide6/QtWidgets/QProxyStyle.html)
- [Qt Documentation: QStyle Class](https://doc.qt.io/qt-6/qstyle.html)
