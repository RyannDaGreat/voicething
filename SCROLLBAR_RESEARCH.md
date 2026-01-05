# PyQt6 Rounded Scrollbar Handles - Research Findings

## Summary

Rounded scrollbar handles in PyQt6 **DO work** using Qt stylesheets, but require precise matching of `border-radius` to the scrollbar `width`. The key is understanding that:

1. **CRITICAL**: `border-radius` must be proportional to scrollbar width
2. **Common Fix**: Set `sub-page` and `add-page` backgrounds to `none` to prevent checkered appearance
3. **Remove Arrows**: Hide scroll arrows (add-line/sub-line) for cleaner pill shapes

## Working Stylesheet Syntax

### Minimal Working Example

```css
QScrollBar:vertical {
    border: none;
    background: #f0f0f0;
    width: 10px;
    margin: 0px;
}

QScrollBar::handle:vertical {
    background: #888888;
    min-height: 20px;
    border-radius: 5px;
}

QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
    height: 0px;
}

QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
    background: none;
}
```

### Full Customizable Example

```css
QScrollBar:vertical {
    border: 0px solid #999999;
    background: white;
    width: 10px;
    margin: 0px 0px 0px 0px;
}

QScrollBar::handle:vertical {
    min-height: 0px;
    border: 0px solid red;
    border-radius: 4px;
    background-color: black;
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

QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
    background: none;
}
```

### Pill/Capsule Shape (Recommended)

For a clean pill-shaped handle with margins:

```css
QScrollBar:vertical {
    border: none;
    background: transparent;
    width: 12px;
    margin: 0px;
}

QScrollBar::handle:vertical {
    background-color: #666666;
    border-radius: 6px;
    min-height: 20px;
    margin: 0px 2px 0px 2px;
}

QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
    height: 0px;
}

QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
    background: none;
}
```

## Horizontal Scrollbar Example

```css
QScrollBar:horizontal {
    border: none;
    background: #f0f0f0;
    height: 10px;
    margin: 0px;
}

QScrollBar::handle:horizontal {
    background: #888888;
    min-width: 20px;
    border-radius: 5px;
}

QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {
    width: 0px;
}

QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal {
    background: none;
}
```

## PyQt6 Implementation Pattern

### Pattern 1: Direct StyleSheet on ScrollBar

```python
from PyQt6.QtWidgets import QScrollArea, QWidget, QVBoxLayout, QLabel
from PyQt6.QtCore import Qt

scroll_area = QScrollArea()
widget = QWidget()
layout = QVBoxLayout()

# Add content
for i in range(100):
    layout.addWidget(QLabel(f"Item {i}"))

widget.setLayout(layout)
scroll_area.setWidget(widget)
scroll_area.setWidgetResizable(True)

# Apply rounded scrollbar
scroll_area.verticalScrollBar().setStyleSheet("""
    QScrollBar:vertical {
        border: none;
        background: #f0f0f0;
        width: 10px;
        margin: 0px;
    }
    QScrollBar::handle:vertical {
        background: #888888;
        min-height: 20px;
        border-radius: 5px;
    }
    QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
        height: 0px;
    }
    QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
        background: none;
    }
""")
```

### Pattern 2: Custom ScrollBar Class

```python
from PyQt6.QtWidgets import QScrollBar

class RoundedScrollBar(QScrollBar):
    def __init__(self, orientation, parent=None):
        super().__init__(orientation, parent)
        self.setStyleSheet("""
            QScrollBar:vertical {
                border: none;
                background: #f0f0f0;
                width: 10px;
                margin: 0px;
            }
            QScrollBar::handle:vertical {
                background: #888888;
                min-height: 20px;
                border-radius: 5px;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                height: 0px;
            }
            QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
                background: none;
            }
        """)
```

## Critical Tips & Troubleshooting

### Problem: Checkered/Transparent Background

**Solution**: Add `sub-page` and `add-page` with `background: none;`

```css
QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
    background: none;
}
```

### Problem: Handle Doesn't Look Rounded

**Solutions**:
1. Ensure `border-radius` is less than half the width (e.g., width: 10px → border-radius: 5px)
2. Verify `min-height` is set (minimum handle size)
3. Avoid setting borders that interfere with rounding

### Problem: Gray Scrollbar Arrows Visible

**Solution**: Hide them entirely with `height: 0px;`

```css
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
    height: 0px;
}
```

### Dimension Recommendations

- **Width**: 10-12px for scrollbar track
- **Border-radius**: 5-6px (roughly half of width)
- **Min-height**: 20px minimum handle size
- **Margin**: 0-2px on sides for spacing from edges

## Limitations

1. **Images don't scale well**: Using `border-image` on scrollbars can cause distortion
2. **No custom painting with stylesheets**: Complex shapes require subclassing and paint event
3. **Platform differences**: macOS may render slightly differently than Linux/Windows
4. **Pseudo-states**: Use `:pressed` and `:hover` for interactive states

```css
QScrollBar::handle:vertical:pressed {
    background: #555555;
}

QScrollBar::handle:vertical:hover {
    background: #999999;
}
```

## Sources

- [Qt Forum: Scrollbar handle with rounded edges](https://forum.qt.io/topic/101931/scrollbar-handle-with-rounded-edges)
- [Qt Style Sheets Examples](https://doc.qt.io/qt-6/stylesheet-examples.html)
- [Creating scrollable GUIs with QScrollArea in PyQt6](https://www.pythonguis.com/tutorials/pyqt6-qscrollarea/)
- [Qt Center: QScrollbar stylesheet](https://www.qtcentre.org/threads/10569-QScrollbar-stylesheet)
- [QScrollBar Class Documentation](https://doc.qt.io/qt-6/qscrollbar.html)
