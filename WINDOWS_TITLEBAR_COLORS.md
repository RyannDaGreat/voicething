# Windows Title Bar Colors - Complete Reference

## Color Values by Windows Version

### Windows 95 / 98

```
ACTIVE WINDOW
=============
Title Bar Gradient (Top to Bottom):
  - Top:    #000080 (Dark Blue, Navy)
  - Bottom: #1084d7 (Bright Blue)

Title Bar Height: 19 pixels
Title Bar Font: MS Sans Serif 11pt Bold
Title Text Color: #ffffff (White)

System Buttons:
  - Normal Background:   #c0c0c0 (System Gray)
  - Hover Background:    #e8e8e8 (Light Gray)
  - Pressed Background:  #a0a0a0 (Dark Gray)
  - Border Highlight:    #e0e0e0 (Light - 3D effect)
  - Border Shadow:       #808080 (Dark - 3D effect)
  - Symbol Color:        #000000 (Black)
  - Button Size:         16x14 pixels
  - Button Spacing:      2 pixels

INACTIVE WINDOW
===============
Title Bar Gradient (Top to Bottom):
  - Top:    #808080 (Gray)
  - Bottom: #c0c0c0 (Light Gray)

Title Text Color: #ffffff (White)
System Buttons: Same colors as active
```

**Hex to RGB Conversion:**
- `#000080` = rgb(0, 0, 128)
- `#1084d7` = rgb(16, 132, 215)
- `#c0c0c0` = rgb(192, 192, 192)
- `#e8e8e8` = rgb(232, 232, 232)
- `#a0a0a0` = rgb(160, 160, 160)

**PyQt6 Implementation:**
```python
gradient.setColorAt(0.0, QColor(0, 0, 128))
gradient.setColorAt(1.0, QColor(16, 132, 215))
```

---

### Windows 2000

```
ACTIVE WINDOW
=============
Title Bar Gradient (Top to Bottom):
  - Top:    #000080 (Dark Blue, Navy)
  - Bottom: #1084d7 (Bright Blue)

(Same as Win95/98, but with smoother antialiasing)

Title Bar Height: 19 pixels
Title Bar Font: MS Sans Serif 11pt Bold
Title Text Color: #ffffff (White)

System Buttons: Same as Win95/98 but with better rendering
```

---

### Windows XP Luna Theme

```
ACTIVE WINDOW
=============
Title Bar Gradient (Top to Bottom):
  - Top:    #336699 (Dusty Blue)
  - Middle: #4488cc (Medium Blue)
  - Bottom: #0066cc (Bright Blue)

Title Bar Height: 21 pixels
Title Bar Font: MS Sans Serif 11pt
Title Text Color: #ffffff (White)

System Buttons:
  - Normal Background:   #c0c0c0 (Gray)
  - Hover Background:    #e8e8e8 (Light Gray)
  - Pressed Background:  #a0a0a0 (Dark Gray)
  - Symbol Color:        #000000 (Black)
  - Button Size:         16x14 pixels
  - Less aggressive 3D beveling, more gradient

INACTIVE WINDOW
===============
Title Bar Gradient:
  - Top:    #999999 (Medium Gray)
  - Bottom: #cccccc (Light Gray)

Title Text Color: #ffffff (White)
```

**Hex to RGB:**
- `#336699` = rgb(51, 102, 153)
- `#4488cc` = rgb(68, 136, 204)
- `#0066cc` = rgb(0, 102, 204)

---

### Windows Vista Aero

```
ACTIVE WINDOW
=============
Title Bar Height: 30 pixels
Title Bar Font: Segoe UI 11pt
Title Text Color: #000000 or #333333 (Dark)

Title Bar Gradient (Top to Bottom, with transparency):
  - 0%:   rgba(232, 244, 248, 100) - Nearly white, very transparent
  - 25%:  rgba(232, 244, 248, 120) - Light cyan, semi-transparent
  - 50%:  rgba(176, 208, 224, 140) - Light cyan-blue
  - 75%:  rgba(100, 200, 220, 160) - Medium cyan-blue
  - 100%: rgba(0, 120, 200, 200)   - Medium blue

Additional Effects:
  - Top highlight: rgba(255, 255, 255, 200) at 0-6 pixels (glossy effect)
  - Bottom shadow: rgba(0, 0, 0, 60) at bottom 4 pixels

System Buttons (Size 16x14):
  - Normal:          rgba(255, 255, 255, 60) (very transparent white)
  - Hover (normal):  rgba(176, 208, 224, 160) (light cyan-blue)
  - Hover (close):   rgba(255, 100, 100, 180) (red tint)
  - Pressed:         rgba(0, 120, 200, 200) (medium blue)
  - Symbol:          #000000 or #ffffff depending on background

INACTIVE WINDOW
===============
Title Bar Background:
  - Solid: rgba(180, 180, 180, 200) (Gray, nearly opaque)
  - OR Gradient: Gray to slightly darker gray

Title Text Color: #666666 (Medium gray)

System Buttons: Grayed out, less visible
```

**Hex to RGB:**
- `#e8f4f8` = rgb(232, 244, 248)
- `#b0d0e0` = rgb(176, 208, 224)
- `#64c8dc` = rgb(100, 200, 220)
- `#0078c8` = rgb(0, 120, 200)
- `#0050a0` = rgb(0, 80, 160)

**PyQt6 Implementation:**
```python
gradient = QLinearGradient(0, 0, 0, 30)
gradient.setColorAt(0.0, QColor(232, 244, 248, 100))
gradient.setColorAt(0.25, QColor(232, 244, 248, 120))
gradient.setColorAt(0.5, QColor(176, 208, 224, 140))
gradient.setColorAt(0.75, QColor(100, 200, 220, 160))
gradient.setColorAt(1.0, QColor(0, 120, 200, 200))
painter.fillRect(self.rect(), gradient)
```

---

### Windows 7 Aero (Refined)

```
ACTIVE WINDOW
=============
Title Bar Height: 27-28 pixels
Title Bar Font: Segoe UI 11pt
Title Text Color: #000000 (Black)

Title Bar Gradient (Top to Bottom, with transparency):
  - 0%:   rgba(232, 244, 248, 80)  - Very light
  - 25%:  rgba(176, 208, 224, 110) - Light cyan
  - 50%:  rgba(100, 200, 220, 120) - Cyan
  - 75%:  rgba(50, 150, 200, 140)  - Medium blue
  - 100%: rgba(0, 120, 200, 180)   - Blue

Additional Effects:
  - Top highlight: rgba(255, 255, 255, 180) at 0-6 pixels
  - Bottom shadow: rgba(0, 0, 0, 50) at bottom 3 pixels

System Buttons (Size 18x16, slightly larger):
  - Normal:          rgba(255, 255, 255, 50)
  - Hover (normal):  rgba(176, 208, 224, 150)
  - Hover (close):   rgba(255, 100, 100, 170)
  - Pressed:         rgba(0, 120, 200, 190)
  - Symbol:          #000000

INACTIVE WINDOW
===============
Title Bar Gradient:
  - Similar to above but all opacity values -30%

Title Text Color: #808080 (Gray)
```

**Difference from Vista:**
- Slightly lighter overall (lower opacity)
- Less intense glass effect
- More refined appearance
- Better optimization

---

### Windows 10 / 11 (Modern)

```
ACTIVE WINDOW
=============
Title Bar Height: 32-36 pixels
Title Bar Font: Segoe UI 11pt
Title Text Color: #ffffff (White) or #000000 (Dark)

Title Bar Color:
  Option 1 - Solid Accent Color (system dependent):
    - Default: rgba(0, 120, 215, 255) (System Blue)
    - Can be customized per system settings

  Option 2 - Dark Theme:
    - #2d2d2d (Dark Gray)

  Option 3 - Light Theme:
    - #f3f3f3 (Light Gray)

System Buttons (Size 20x20):
  - Normal:          Transparent (no background)
  - Hover (normal):  rgba(0, 0, 0, 0.06) (barely visible overlay)
  - Hover (close):   #c42b1c (Red background)
  - Pressed:         Darker version of hover

Symbol Color:
  - Normal/Hover:    #000000 or system accent
  - Close button:    #ffffff (White on red)

INACTIVE WINDOW
===============
Title Bar Color:
  - Very subtle gray, nearly same as active
  - Often indistinguishable

Title Text Color: Slightly grayed
System Buttons: Slightly dimmed
```

---

## Quick Color Selection Guide

### For Nostalgic/Retro Appearance
**Use Windows 95/98:**
```python
# Top
gradient.setColorAt(0.0, QColor(0, 0, 128))

# Bottom
gradient.setColorAt(1.0, QColor(16, 132, 215))
```

### For Professional/Modern Retro
**Use Windows XP:**
```python
# Top
gradient.setColorAt(0.0, QColor(51, 102, 153))

# Middle
gradient.setColorAt(0.5, QColor(68, 136, 204))

# Bottom
gradient.setColorAt(1.0, QColor(0, 102, 204))
```

### For Elegant/Sophisticated
**Use Windows Vista/7 Aero:**
```python
# Recommended for your Frutiger Aero app
gradient = QLinearGradient(0, 0, 0, 30)
gradient.setColorAt(0.0, QColor(232, 244, 248, 100))
gradient.setColorAt(0.25, QColor(232, 244, 248, 120))
gradient.setColorAt(0.5, QColor(176, 208, 224, 140))
gradient.setColorAt(0.75, QColor(100, 200, 220, 160))
gradient.setColorAt(1.0, QColor(0, 120, 200, 200))
```

### For Minimal/Clean
**Use Windows 10 Solid:**
```python
painter.fillRect(self.rect(), QColor(0, 120, 215))
```

---

## System Button Colors by Windows Version

### Windows 95/98/2000/XP

| State | Background | Symbol |
|-------|-----------|--------|
| Normal | `#c0c0c0` | `#000000` |
| Hover | `#e8e8e8` | `#000000` |
| Pressed | `#a0a0a0` | `#000000` |
| Close Hover | `#e8e8e8` | `#000000` |

### Windows Vista/7 Aero

| State | Minimize/Max | Close |
|-------|--------------|-------|
| Normal | `rgba(255,255,255,60)` | `rgba(255,255,255,60)` |
| Hover | `rgba(176,208,224,160)` | `rgba(255,100,100,180)` |
| Pressed | `rgba(0,120,200,200)` | `rgba(200,60,60,200)` |

### Windows 10/11

| State | Minimize/Max | Close |
|-------|--------------|-------|
| Normal | Transparent | Transparent |
| Hover | `rgba(0,0,0,15)` | `#c42b1c` |
| Pressed | `rgba(0,0,0,25)` | `#a01810` |

---

## Color Matching Tips

1. **Test on actual Windows**
   - Colors may vary based on monitor calibration
   - Display settings affect perception
   - Test on different hardware when possible

2. **Account for Transparency**
   - Semi-transparent colors appear different based on background
   - Always test over different backgrounds
   - Account for anti-aliasing effects

3. **Font Color Contrast**
   - White text on Windows 95 blue: Good contrast
   - Dark text on Vista glass: Good contrast
   - Ensure WCAG AA compliance (4.5:1 ratio minimum)

4. **Button Hover States**
   - Must be visually distinct from normal state
   - Close button should stand out most
   - Recommend red for close button (universal convention)

5. **Inactive Window**
   - Colors should be noticeably different (less saturated)
   - Indicates window is not focused
   - Typically achieved by reducing opacity or desaturating

---

## PyQt6 Color Functions

```python
# From hex string
color = QColor("#1084d7")

# From RGB integers
color = QColor(16, 132, 215)

# From RGB with alpha (transparency)
color = QColor(16, 132, 215, 200)  # 200/255 opacity

# From RGBA named
color = QColor()
color.setRgb(16, 132, 215, 200)

# Named colors
color = QColor("blue")
```

---

## Reference Colors Used in Your App

From your Frutiger Aero implementation:

```python
AZURE_DRAGON = "#003c78"
PRINCESS_BLUE = "#0050a0"
COBALT_STONE = "#0064b4"
MYSTERY_OCEANS = "#003c8c"
SCIENCE_BLUE = "#0078c8"
RUSHING_STREAM = "#64c8dc"
ELECTRIC_BLUE = "#0689e4"
EASTERN_BLUE = "#1299ca"
SCOOTER = "#35bcde"
SKY_BLUE = "#6fd7ec"
```

**Recommendation:** Use these blues alongside Vista/7 Aero gradient for consistency with your existing design language.

---

## Common Color Mistakes

1. **Using opaque colors instead of transparent**
   - Makes buttons look flat, not glass-like
   - Fix: Use rgba() with 100-200 alpha values

2. **Wrong gradient direction**
   - Make sure gradient goes top-to-bottom (y1:0, y2:height)
   - Not left-to-right

3. **Too many gradient stops**
   - Can make appearance muddy
   - Stick to 3-5 color stops maximum

4. **Not updating button colors on hover**
   - Users expect visual feedback
   - Must change color when mouse hovers

5. **Close button same color as other buttons**
   - Should stand out, typically red
   - Helps prevent accidental clicks

---

**Color Reference Updated:** January 5, 2026
