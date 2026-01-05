# Qt Rounded Scrollbar - Complete Documentation Index

Comprehensive guide to implementing rounded scrollbar handles in Qt/PyQt.

## Quick Navigation

### For Beginners
1. **Start here:** [Quick Start Guide](SCROLLBAR_QUICK_START.md)
2. **Copy-paste solutions** (3 options, pick the best one)
3. **Runnable examples** in `scrollbar_examples.py`

### For Detailed Understanding
1. **Read:** [Complete Examples Documentation](ROUNDED_SCROLLBAR_EXAMPLES.md)
2. **Understand:** All three approaches with pros/cons
3. **Test:** Run each example from the command line

### For Advanced Implementation
1. **Study:** [Advanced Customization](SCROLLBAR_ADVANCED.md)
2. **Choose technique:** Hover effects, gradients, animations, etc.
3. **Integrate:** Combine techniques for your needs

---

## Three Main Approaches

### 1. Qt Stylesheet (Fastest)
**File:** See [SCROLLBAR_QUICK_START.md - Option 1](SCROLLBAR_QUICK_START.md)

**Pros:**
- Only 3 lines of code
- Works immediately
- No class definitions needed

**Cons:**
- Limited customization
- No hover/press effects
- May have platform-specific issues

**Best for:** Simple projects, quick prototypes

```python
stylesheet = "QScrollBar::handle:vertical { border-radius: 4px; }"
text_edit.setStyleSheet(stylesheet)
```

---

### 2. QScrollBar Subclass (Recommended)
**File:** See [ROUNDED_SCROLLBAR_EXAMPLES.md - Approach 2](ROUNDED_SCROLLBAR_EXAMPLES.md#approach-2-qscrollbar-subclass-with-paintevent)

**Pros:**
- Full visual control
- Custom colors/radius easily
- Works per-widget
- Straightforward to understand

**Cons:**
- ~20 lines of code
- Must apply to each widget
- Need to handle both V and H separately

**Best for:** Single widget customization

```python
class RoundedScrollBar(QScrollBar):
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        # ... custom painting code
```

---

### 3. QProxyStyle (Professional)
**File:** See [ROUNDED_SCROLLBAR_EXAMPLES.md - Approach 3](ROUNDED_SCROLLBAR_EXAMPLES.md#approach-3-qproxystyle-with-drawcomplexcontrol)

**Pros:**
- App-wide effect
- Handles all scrollbars automatically
- Can detect hover/press states
- Professional architecture

**Cons:**
- ~25 lines of code
- Slightly more complex
- Need to understand style system

**Best for:** App-wide consistent styling

```python
class RoundedScrollBarStyle(QProxyStyle):
    def drawComplexControl(self, control, option, painter, widget=None):
        if control == QStyle.CC_ScrollBar:
            # ... custom painting code
```

---

## Files in This Package

| File | Purpose | Audience |
|------|---------|----------|
| [SCROLLBAR_QUICK_START.md](SCROLLBAR_QUICK_START.md) | TL;DR with copy-paste code | Everyone |
| [ROUNDED_SCROLLBAR_EXAMPLES.md](ROUNDED_SCROLLBAR_EXAMPLES.md) | Complete working examples | Learners |
| [SCROLLBAR_ADVANCED.md](SCROLLBAR_ADVANCED.md) | Advanced techniques | Advanced users |
| `scrollbar_examples.py` | Runnable test code | Testers |
| SCROLLBAR_INDEX.md (this file) | Navigation guide | Everyone |

---

## Running the Examples

### Prerequisites
```bash
pip install PyQt5
```

### Run Any Example

```bash
# Stylesheet approach
python scrollbar_examples.py stylesheet

# QScrollBar subclass approach (default)
python scrollbar_examples.py subclass

# QProxyStyle approach
python scrollbar_examples.py proxystyle
```

All three windows will look visually identical - test them side-by-side to understand the implementation differences.

---

## Key Concepts

### The Handle Rectangle
The scrollbar handle position and size must come from the style system, not manual calculations:

```python
opt = self.initStyleOption()
handle_rect = self.style().subControlRect(
    QStyle.CC_ScrollBar, opt, QStyle.SC_ScrollBarSlider, self
)
```

**Never hardcode the handle rectangle!** It needs to:
- Update as content size changes
- Move as user scrolls
- Resize based on visible content ratio

### Corner Radius Formula
For truly round corners, use:
```python
corner_radius = scrollbar_width // 2
painter.drawRoundedRect(rect, corner_radius, corner_radius)
```

Example:
- Width 10px → radius 5px (perfect circle)
- Width 12px → radius 6px (perfect circle)
- Width 4px → radius 2px (minimal radius)

### Antialiasing (Critical!)
Always enable antialiasing for smooth corners:
```python
painter.setRenderHint(QPainter.Antialiasing)
```

Without this, rounded corners will look pixelated/jagged.

### State Detection
QProxyStyle lets you detect interaction states:
```python
if option.state & QStyle.State_MouseOver:
    # Handle is hovered
if option.state & QStyle.State_Sunken:
    # Handle is being pressed/dragged
```

---

## Decision Tree: Which Approach?

```
Do you need app-wide scrollbar styling?
├─ YES → Use QProxyStyle (Approach 3)
│
└─ NO → Do you need hover effects?
    ├─ YES → Use QScrollBar subclass (Approach 2)
    │
    └─ NO → Use Stylesheet (Approach 1)
```

---

## Common Issues & Solutions

### Issue: Corners Still Look Sharp

**Diagnosis:**
- Check if antialiasing is enabled
- Verify corner radius > 1

**Fix:**
```python
painter.setRenderHint(QPainter.Antialiasing)
painter.drawRoundedRect(rect, 4, 4)  # Not 0, 0 or 1, 1
```

See [SCROLLBAR_QUICK_START.md - Pitfall 1](SCROLLBAR_QUICK_START.md#pitfall-1-sharp-corners-instead-of-rounded)

---

### Issue: Handle Rectangle Wrong Size

**Diagnosis:**
- Handle is tiny or full-size
- Size doesn't change with content

**Fix:**
```python
# Use style's subControlRect, not manual calculation
opt = self.initStyleOption()
handle_rect = self.style().subControlRect(
    QStyle.CC_ScrollBar, opt, QStyle.SC_ScrollBarSlider, self
)
```

See [SCROLLBAR_QUICK_START.md - Pitfall 2](SCROLLBAR_QUICK_START.md#pitfall-2-handle-rectangle-is-wrong-size)

---

### Issue: Handle Not Visible

**Diagnosis:**
- Handle color matches background
- No pen style set

**Fix:**
```python
painter.setBrush(QBrush(QColor(100, 100, 100)))  # Contrasting color
painter.setPen(QPen(Qt.NoPen))  # No outline
painter.drawRoundedRect(handle_rect, 4, 4)
```

See [SCROLLBAR_QUICK_START.md - Pitfall 4](SCROLLBAR_QUICK_START.md#pitfall-4-handle-hidden-or-invisible)

---

## Advanced Techniques

| Technique | File | Complexity |
|-----------|------|------------|
| Hover effects | [SCROLLBAR_ADVANCED.md - #1](SCROLLBAR_ADVANCED.md#1-hover-effects) | Easy |
| Gradient fill | [SCROLLBAR_ADVANCED.md - #2](SCROLLBAR_ADVANCED.md#2-gradient-handle) | Easy |
| Shadow effect | [SCROLLBAR_ADVANCED.md - #3](SCROLLBAR_ADVANCED.md#3-shadowblur-effect) | Medium |
| Horizontal support | [SCROLLBAR_ADVANCED.md - #4](SCROLLBAR_ADVANCED.md#4-horizontal-scrollbar) | Easy |
| Custom colors | [SCROLLBAR_ADVANCED.md - #5](SCROLLBAR_ADVANCED.md#5-custom-colors-per-direction) | Easy |
| macOS-like thin | [SCROLLBAR_ADVANCED.md - #6](SCROLLBAR_ADVANCED.md#6-thin-scrollbar-macos-like) | Medium |
| Animation | [SCROLLBAR_ADVANCED.md - #7](SCROLLBAR_ADVANCED.md#7-animated-scrollbar-advanced) | Hard |
| Disabled state | [SCROLLBAR_ADVANCED.md - #8](SCROLLBAR_ADVANCED.md#8-disabled-state) | Easy |
| Platform-specific | [SCROLLBAR_ADVANCED.md - #10](SCROLLBAR_ADVANCED.md#10-platform-specific-styling) | Medium |

---

## Testing Checklist

When implementing rounded scrollbars, verify:

- [ ] Handle corners are rounded (not sharp)
- [ ] Handle moves smoothly when scrolling
- [ ] Handle size adjusts with content length
- [ ] No visual artifacts or flicker
- [ ] Works on Windows/Mac/Linux (if needed)
- [ ] Scrollbar width and corner radius are proportional
- [ ] Handle is visible against track background
- [ ] Hover effects work (if implemented)
- [ ] Disabled state looks appropriate (if needed)

---

## Performance Tips

1. **Enable antialiasing only on handle, not entire rect**
   ```python
   painter.setRenderHint(QPainter.Antialiasing)  # Essential
   # Keep it simple, avoid complex operations in paintEvent
   ```

2. **Cache colors as class constants**
   ```python
   class MyScrollBar(QScrollBar):
       HANDLE_COLOR = QColor(120, 120, 120)  # Don't create per-paint
   ```

3. **Minimize paintEvent() complexity**
   - Get handle rect once, paint once
   - Avoid loops or conditionals if possible

4. **Only repaint when necessary**
   - Don't call `update()` on every mouse move
   - Only update on state changes (hover on/off)

See [SCROLLBAR_ADVANCED.md - Performance Optimization](SCROLLBAR_ADVANCED.md#performance-optimization)

---

## Integration Examples

### Single Widget
```python
text_edit.setVerticalScrollBar(RoundedScrollBar(Qt.Vertical))
```

### Multiple Widgets
```python
for widget in [text_edit1, text_edit2, text_edit3]:
    widget.setVerticalScrollBar(RoundedScrollBar(Qt.Vertical))
    widget.setHorizontalScrollBar(RoundedScrollBar(Qt.Horizontal))
```

### App-Wide
```python
app = QApplication([])
app.setStyle(RoundedScrollBarStyle())
```

---

## Learning Path

### Phase 1: Understanding (30 min)
1. Read [SCROLLBAR_QUICK_START.md](SCROLLBAR_QUICK_START.md)
2. Pick an approach (likely QScrollBar subclass)
3. Run `python scrollbar_examples.py subclass`
4. Modify colors/radius in the running example

### Phase 2: Implementation (30 min)
1. Copy code from examples
2. Apply to your widget
3. Test that it looks right
4. Adjust colors/size as needed

### Phase 3: Customization (1-2 hours)
1. Choose advanced technique from [SCROLLBAR_ADVANCED.md](SCROLLBAR_ADVANCED.md)
2. Understand the pattern
3. Implement in your code
4. Test thoroughly

---

## References

### Official Documentation
- [Qt QScrollBar](https://doc.qt.io/qt-5/qscrollbar.html)
- [Qt QProxyStyle](https://doc.qt.io/qt-6/qproxystyle.html)
- [Qt QStyle](https://doc.qt.io/qt-6/qstyle.html)
- [Qt QPainter](https://doc.qt.io/qt-5/qpainter.html)

### PyQt Documentation
- [PyQt5 QtWidgets](https://www.riverbankcomputing.com/static/Docs/PyQt5/api/qtwidgets/index.html)
- [PyQt5 QtGui](https://www.riverbankcomputing.com/static/Docs/PyQt5/api/qtgui/index.html)

### Community Resources
- [Qt Forum - Scrollbar Discussions](https://forum.qt.io/)
- Stack Overflow `qt` and `pyqt5` tags

---

## Troubleshooting

### The scrollbar doesn't look rounded
→ [SCROLLBAR_QUICK_START.md - Pitfall 1](SCROLLBAR_QUICK_START.md#pitfall-1-sharp-corners-instead-of-rounded)

### The handle is wrong size
→ [SCROLLBAR_QUICK_START.md - Pitfall 2](SCROLLBAR_QUICK_START.md#pitfall-2-handle-rectangle-is-wrong-size)

### Handle position is wrong
→ Use `initStyleOption()` and `subControlRect()`

### Stylesheet border-radius doesn't work
→ [SCROLLBAR_QUICK_START.md - Pitfall 3](SCROLLBAR_QUICK_START.md#pitfall-3-stylesheet-border-radius-not-working)

### Handle is invisible/hidden
→ [SCROLLBAR_QUICK_START.md - Pitfall 4](SCROLLBAR_QUICK_START.md#pitfall-4-handle-hidden-or-invisible)

### Stylesheet shows checkered pattern
→ [SCROLLBAR_QUICK_START.md - Pitfall 5](SCROLLBAR_QUICK_START.md#pitfall-5-stylesheet-hides-handle-background)

### Performance issues / excessive repainting
→ [SCROLLBAR_ADVANCED.md - Performance Optimization](SCROLLBAR_ADVANCED.md#performance-optimization)

---

## Summary

You have **three proven approaches** to create rounded scrollbar handles:

1. **Stylesheet** - Fastest, simplest, limited
2. **QScrollBar Subclass** - Best balance, recommended
3. **QProxyStyle** - Most professional, app-wide

All three are documented with:
- ✓ Working code examples
- ✓ Pros and cons
- ✓ Integration instructions
- ✓ Troubleshooting guides

**Start here:** [SCROLLBAR_QUICK_START.md](SCROLLBAR_QUICK_START.md)

**Then run:** `python scrollbar_examples.py`

**Questions?** Check [SCROLLBAR_QUICK_START.md - Common Pitfalls](SCROLLBAR_QUICK_START.md#common-pitfalls)
