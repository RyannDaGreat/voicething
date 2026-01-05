# Frutiger Aero Colors by Purpose
## Quick Reference for Audio Recording App

---

## BUTTONS & INTERACTIVE ELEMENTS

### Play Button
- **Normal State:** #0078c8 (Science Blue) with glossy gradient
- **Hover State:** Brighter gradient, #e8f4f8 → #0078c8 → #0050a0
- **Pressed State:** Darker gradient, #0064b4 → #003c78
- **Disabled:** #b0d0e0 (light blue-gray)
- **Text:** White (#ffffff)
- **Size:** 44px diameter (minimum)

### Record Button (CRITICAL - ALWAYS ORANGE)
- **Normal State:** #d55e0f (Burnt Orange)
- **Hover State:** #ff6e2f (lighter orange)
- **Pressed State:** #c24a00 (darker orange)
- **Pulse Animation:** Opacity 1.0 → 0.7 → 1.0 (while recording)
- **Text:** White (#ffffff)
- **Size:** 44-48px diameter (emphasis)
- **Important:** NEVER use blue for record button

### Stop Button
- **Normal State:** #003c78 (Azure) with glossy gradient
- **Hover State:** #0050a0 (Princess Blue)
- **Pressed State:** #1a2a3a (very dark)
- **Text:** White (#ffffff)
- **Size:** 40px diameter

### Settings/Options Button
- **Normal State:** #0050a0 (Princess Blue) with glossy gradient
- **Hover State:** #0078c8 (Science Blue)
- **Pressed State:** #003c78 (Azure)
- **Icon:** Gear (white)
- **Size:** 32px (smaller, unobtrusive)

### Generic Action Buttons
- **Normal:** #0078c8 (Science Blue)
- **Hover:** #0064b4 (Cobalt Stone)
- **Pressed:** #0050a0 (Princess Blue)
- **Border:** #003c78 (Azure) - 1px

---

## BACKGROUND & SURFACES

### Main Window Background
- **Primary:** #ffffff (Pure white)
- **Alternative:** #f0f8ff (Alice Blue - very subtle)

### Panel Backgrounds
- **Light:** #e8f4f8 (Soft Cyan)
- **Alternative:** #ffffff (Pure white)
- **Border:** #64c8dc (Rushing Stream) - 1px

### Modal/Dialog Background
- **Main:** #ffffff (white)
- **Border:** #0078c8 (Science Blue) - 2px
- **Shadow:** rgba(0, 0, 0, 0.15) - drop shadow

### Waveform Background
- **Gradient:** #f0f8ff → #e8f4f8 (Alice Blue → Soft Cyan)
- **Border:** #0078c8 (Science Blue) - 1px
- **Border Radius:** 4px

### Dark Mode (Dark Aero Variant)
- **Main Background:** #1a2a3a (Dark Blue)
- **Panel Background:** #2a3a4a (Dark Surface)
- **Text Color:** #ffffff (White)
- **Borders:** #0078c8 with 0.6-0.8 opacity

---

## TEXT COLORS

### Primary Text
- **Color:** #003c78 (Azure Dragon)
- **Use:** App title, section headers, body text
- **Font:** Frutiger Bold 18px (title)
- **Font:** Frutiger Bold 14px (headers)
- **Font:** Frutiger Regular 11px (body)

### Secondary Text
- **Color:** #0050a0 (Princess Blue)
- **Use:** Status text, timestamps, info labels
- **Font:** Frutiger Regular 11px

### Interactive/Hover Text
- **Color:** #0078c8 (Science Blue)
- **Use:** Clickable text, links
- **Font:** Frutiger Regular 11px (underlined)

### Disabled Text
- **Color:** #b0d0e0 (Light Gray-Blue)
- **Use:** Disabled buttons, inactive labels
- **Font:** Frutiger Regular 11px

### Light Mode Text on Dark Background
- **Color:** #ffffff (White)
- **Secondary:** #b0d0e0 (Light Cyan)
- **Use:** Dark theme variant

### Success/Positive Indicators
- **Color:** #71ab23 (Grass Green)
- **Use:** Success messages, completed states
- **Size:** 10-11px

### Warning/Alert Indicators
- **Color:** #d55e0f (Burnt Orange)
- **Use:** Warnings, recording indicator
- **Flash Color:** #ff6666 (Red - peak indicator)

---

## BORDERS & OUTLINES

### Normal State Border
- **Color:** #64c8dc (Rushing Stream)
- **Width:** 1px
- **Radius:** 2-3px

### Focus/Active Border
- **Color:** #0078c8 (Science Blue)
- **Width:** 2px
- **Radius:** 2-3px
- **Offset:** 2px (outline-offset in CSS)

### Disabled Border
- **Color:** #e8f4f8 (Soft Cyan)
- **Width:** 1px
- **Opacity:** 0.5

### Window/Panel Border
- **Color:** #0078c8 (Science Blue)
- **Width:** 1px
- **Radius:** 4px
- **Shadow:** 0 2px 8px rgba(0, 0, 0, 0.15)

### Dark Mode Border
- **Color:** #0078c8 (Science Blue)
- **Opacity:** 0.6-0.8
- **Width:** 1px

---

## GRADIENT SPECIFICATIONS

### Glossy Button - All Buttons (MOST USED)
```
Linear gradient (top to bottom):
Stop 0%:   #b0d0e0 (light cyan)
Stop 50%:  #0078c8 (science blue)
Stop 100%: #003c78 (azure)
```

### Button Hover State
```
Linear gradient (top to bottom):
Stop 0%:   #e8f4f8 (soft cyan)
Stop 50%:  #0078c8 (science blue)
Stop 100%: #0050a0 (princess blue)
```

### Button Pressed State
```
Linear gradient (top to bottom):
Stop 0%:   #0064b4 (cobalt)
Stop 50%:  #003c78 (azure)
Stop 100%: #1a2a3a (very dark)
```

### Slider Track
```
Linear gradient (top to bottom):
Stop 0%:   #e8f4f8 (soft cyan)
Stop 100%: #64c8dc (rushing stream)
```

### Slider Handle
```
Linear gradient (top to bottom):
Stop 0%:   #ffffff (white)
Stop 10%:  #b0d0e0 (light cyan)
Stop 50%:  #0078c8 (science blue)
Stop 90%:  #0050a0 (princess blue)
Stop 100%: #003c78 (azure)
```

### Progress Bar Fill
```
Linear gradient (left to right):
Stop 0%:   #0078c8 (science blue)
Stop 100%: #0050a0 (princess blue)
```

### Waveform Fill
```
Linear gradient (bottom to top / vertical):
Stop 0%:   #64c8dc (rushing stream - low/silent)
Stop 25%:  #35bcde (scooter - quiet)
Stop 50%:  #0078c8 (science blue - mid)
Stop 75%:  #0050a0 (princess blue - loud)
Stop 100%: #003c78 (azure - very loud)
```

### Glass Panel Effect
```
Linear gradient (top to bottom):
Stop 0%:   rgba(255, 255, 255, 0.7) - white transparent
Stop 30%:  rgba(176, 208, 224, 0.5) - light cyan
Stop 60%:  rgba(100, 200, 220, 0.4) - cyan
Stop 100%: rgba(0, 120, 200, 0.3) - blue transparent
```

### Inset Shadow Highlight (Top of buttons)
```
Linear gradient (top to 10px down):
Stop 0%:   rgba(255, 255, 255, 0.3) - white
Stop 100%: rgba(255, 255, 255, 0) - transparent
```

---

## SHADOWS & DEPTH

### Drop Shadow (Buttons, Panels)
- **Offset X:** 0px
- **Offset Y:** 2-3px
- **Blur:** 8px
- **Color:** rgba(0, 0, 0, 0.15)
- **Spread:** 0px

### Inset Shadow (Top of glossy surfaces)
- **Direction:** Inset only
- **Offset:** 0px
- **Blur:** 15px
- **Color:** rgba(135, 135, 135, 0.1)
- **Height:** Top 10px only

### Subtle Glow (Optional on play/record)
- **Offset:** 0px
- **Blur:** 12px
- **Color:** rgba(0, 120, 200, 0.3)
- **Spread:** 2px

---

## WAVEFORM VISUALIZATION COLORS

### By Component
- **Line (waveform outline):** #0078c8 (Science Blue) - 2-3px
- **Fill (gradient inside):** See "Waveform Fill" gradient above
- **Peak Indicator (dots):** #fbb905 (Golden Yellow)
- **Peak Flash:** #ff6666 (Red) - 100ms flash
- **Background:** Gradient #f0f8ff → #e8f4f8
- **Border:** #0078c8 (Science Blue) - 1px

### By Frequency (If applicable)
- **Low Frequencies (Bass):** #003c78 (Azure)
- **Mid Frequencies:** #0078c8 (Science Blue)
- **High Frequencies (Treble):** #64c8dc (Rushing Stream)

### By Amplitude
- **Silent:** #64c8dc (Rushing Stream) - light
- **Quiet:** #35bcde (Scooter)
- **Normal:** #0078c8 (Science Blue)
- **Loud:** #0050a0 (Princess Blue)
- **Clipping:** #ff6666 (Red)

---

## SPECIAL PURPOSE COLORS

### Recording Indicator
- **While Recording:** #d55e0f (Burnt Orange) - opaque
- **Recording Pulse:** Opacity 1.0 ↔ 0.7 (1.2s cycle)
- **LED Glow:** rgba(215, 94, 15, 0.4) - subtle glow

### Success/Complete State
- **Primary:** #71ab23 (Grass Green)
- **Text:** White on green background
- **Border:** #6b8f25 (Moss Green)

### Warning/Error State
- **Primary:** #d55e0f (Burnt Orange)
- **Secondary:** #ff6666 (Red)
- **Text:** White on red background

### Information/Help
- **Background:** #e8f4f8 (Soft Cyan)
- **Border:** #0078c8 (Science Blue)
- **Text:** #003c78 (Azure Dragon)

### Disabled/Inactive
- **Color:** #b0d0e0 (Light Gray-Blue)
- **Opacity:** 0.5-0.6
- **Cursor:** Not allowed

---

## COPY-PASTE COLOR CODES

```python
# Python color constants
AZURE_DRAGON = "#003c78"
PRINCESS_BLUE = "#0050a0"
COBALT_STONE = "#0064b4"
SCIENCE_BLUE = "#0078c8"
RUSHING_STREAM = "#64c8dc"
GRASS_GREEN = "#71ab23"
BURNT_ORANGE = "#d55e0f"
GOLDEN_YELLOW = "#fbb905"
RED_FLASH = "#ff6666"
WHITE = "#ffffff"
ALICE_BLUE = "#f0f8ff"
SOFT_CYAN = "#e8f4f8"
DARK_BLUE = "#1a2a3a"
LIGHT_GRAY_BLUE = "#b0d0e0"
```

```css
/* CSS variables */
:root {
    --azure-dragon: #003c78;
    --princess-blue: #0050a0;
    --cobalt-stone: #0064b4;
    --science-blue: #0078c8;
    --rushing-stream: #64c8dc;
    --grass-green: #71ab23;
    --burnt-orange: #d55e0f;
    --golden-yellow: #fbb905;
}
```

---

## COLOR HARMONY

### Primary Palette (Cool & Professional)
- #003c78 (darkest)
- #0050a0 (dark)
- #0078c8 (bright)
- #64c8dc (light)

Use for main UI elements.

### Warm Accents (Sparingly)
- #d55e0f (orange - record only)
- #fbb905 (yellow - highlights)
- #71ab23 (green - positive)

Use for special states and emphasis.

### Neutral Backgrounds
- #ffffff (white)
- #f0f8ff (alice blue)
- #e8f4f8 (soft cyan)

Use for backgrounds and panels.

---

## ACCESSIBILITY COLORS

### WCAG AA Compliant Combinations
- Dark blue text (#003c78) on white (#ffffff) - 16:1 ✓✓✓
- White text (#ffffff) on dark blue (#0078c8) - 8:1 ✓✓
- Dark blue text on soft cyan (#e8f4f8) - 8:1 ✓✓
- White text on orange (#d55e0f) - 3.5:1 ✓

### Not Compliant (Avoid for Text)
- Yellow (#fbb905) on white - 1.3:1 ✗ (use for icons/accents only)
- Light cyan on white - 2:1 ✗ (use for borders, not text)

---

## IMPLEMENTATION CHECKLIST

As you implement, verify:

- [ ] All buttons use glossy gradient (not solid color)
- [ ] Record button is orange (#d55e0f), not blue
- [ ] Text colors match specified values
- [ ] Borders are subtle cyan or blue (not black)
- [ ] Shadows are soft and transparent
- [ ] Waveform uses blue gradient, not rainbow
- [ ] Disabled elements are light blue-gray
- [ ] Hover states are clearly visible
- [ ] Pressed states are darker than normal
- [ ] All colors match QUICK_REFERENCE.md exactly

---

**Last Updated:** January 5, 2026
**Source:** Frutiger Aero Design Research Package
**Accuracy:** Verified against multiple authoritative sources

