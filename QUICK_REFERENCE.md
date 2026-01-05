# Frutiger Aero Quick Reference
## Color Codes, Gradients & Design Elements

---

## CORE COLOR PALETTE

```
PRIMARY BLUES (Use These 80% of the Time)
┌─────────────────────────────────────────┐
│ #003c78  Azure Dragon       [0, 60, 120]   - Darkest, shadows
│ #0050a0  Princess Blue      [0, 80, 160]   - Dark accents
│ #0064b4  Cobalt Stone       [0, 100, 180]  - Mid-tone
│ #0078c8  Science Blue       [0, 120, 200]  - Bright primary
│ #64c8dc  Rushing Stream     [100, 200, 220]- Light cyan
└─────────────────────────────────────────┘

BACKGROUNDS & NEUTRALS
┌─────────────────────────────────────────┐
│ #ffffff   White              - Main background
│ #f0f8ff   Alice Blue         - Soft background
│ #e8f4f8   Soft Cyan          - Panel backgrounds
│ #1a2a3a   Dark Blue (Dark)   - Dark theme background
└─────────────────────────────────────────┘

ACCENTS & SPECIAL
┌─────────────────────────────────────────┐
│ #71ab23   Grass Green        - Positive/eco
│ #d55e0f   Burnt Orange       - Warning/record
│ #fbb905   Golden Yellow      - Highlight
│ #35bcde   Scooter (Aqua)     - Alternative light
└─────────────────────────────────────────┘
```

---

## STANDARD GRADIENTS

### GLOSSY BUTTON (Vertical Top → Bottom)
```
0%:   #ffffff (white) + 70% alpha
10%:  #b0d0e0 (light cyan)
50%:  #0078c8 (science blue)
90%:  #0050a0 (princess blue)
100%: #003c78 (azure)

Use for: All buttons in normal state
```

### GLOSSY BUTTON - HOVER STATE
```
0%:   #e8f4f8 (soft cyan)
50%:  #0078c8 (science blue)
100%: #0050a0 (princess blue)

Use for: When mouse hovers over button
```

### GLOSSY BUTTON - PRESSED STATE
```
0%:   #0064b4 (cobalt)
50%:  #003c78 (azure)
100%: #1a2a3a (very dark blue)

Use for: When button is clicked/held down
```

### WAVEFORM GRADIENT (Vertical)
```
0%:   #003c78 (azure - high amplitude)
25%:  #0050a0 (princess blue)
50%:  #0078c8 (science blue - peak)
75%:  #64c8dc (cyan)
100%: #64c8dc (rushing stream - silent)

Use for: Waveform fill colors
```

### GLASS PANEL EFFECT
```
0%:   #ffffff + 70% alpha (white transparent)
30%:  #b0d0e0 + 50% alpha (light cyan)
60%:  #64c8dc + 40% alpha (cyan)
100%: #0078c8 + 30% alpha (blue transparent)

Use for: Panel backgrounds, glass effect
```

### INSET SHADOW (Top to 10px down)
```
0%:   rgba(135, 135, 135, 25)
100%: rgba(135, 135, 135, 0)

Use for: Depth on glossy surfaces (inset shadow only)
```

---

## UI COMPONENT COLORS

### BUTTONS BY TYPE
```
Play Button:
  - Gradient: Glossy Button (normal)
  - Icon Color: White
  - Border: #0050a0

Record Button:
  - Background: #d55e0f (burnt orange)
  - Text: White
  - Hover: #ff6e2f (lighter orange)

Stop Button:
  - Gradient: Glossy Button (normal)
  - Icon: White
  - Border: #003c78

Settings/Options:
  - Gradient: Glossy Button (normal)
  - Icon: White
  - Border: #0050a0
```

### TEXT COLORS
```
Primary Text:       #003c78 (dark blue)
Secondary Text:     #0050a0 (medium blue)
Interactive Text:   #0078c8 (bright blue)
Hover Links:        #0064b4 (cobalt)
Disabled Text:      #b0d0e0 (light gray-blue)
Tooltip Text:       #ffffff on #003c78 background
```

### BORDERS
```
Normal Border:      #64c8dc (cyan) - 1px
Focus/Active:       #0078c8 (science blue) - 2px
Disabled:           #e8f4f8 (soft cyan) - 1px
Shadow/Depth:       rgba(0,0,0,0.2) - drop shadow
```

### SLIDERS & PROGRESS
```
Track Background:   Linear gradient #e8f4f8 → #64c8dc
Handle/Thumb:       Glossy Button gradient
Active Fill:        #0078c8 → #0050a0
Completed Bar:      Glossy gradient #0078c8 → #003c78
```

---

## DESIGN SPECIFICATIONS

### BUTTON DIMENSIONS
```
Standard Button:    75px wide × 23px tall
Padding:            12px horizontal, 4px vertical
Border Radius:      2-3px
Font Size:          11px, Bold
Font Family:        Frutiger, Segoe UI, sans-serif
Min Touch Target:   44px × 44px
```

### PANEL/WINDOW
```
Border:             1px solid #0078c8
Border Radius:      4px
Drop Shadow:        0 2px 8px rgba(0,0,0,0.15)
Padding:            8-12px
Background:         White or light gradient
```

### WAVEFORM DISPLAY
```
Height:             120px minimum
Background:         Linear gradient #f0f8ff → #e8f4f8
Line Width:         2-3px
Line Color:         #0078c8 (science blue)
Anti-alias:         Enabled
Border:             1px #0078c8
Border Radius:      2px
```

### TYPOGRAPHY
```
App Title:          18px, Bold, #003c78
Section Headers:    14px, Bold, #003c78
Body Text:          11px, Regular, #003c78
Small Labels:       9px, Regular, #0050a0
Disabled Text:      11px, Regular, #b0d0e0
```

---

## QUICK COPY-PASTE GRADIENTS

### For QSS (Qt Style Sheet):
```css
/* Glossy Button */
qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 #b0d0e0, stop:0.5 #0078c8, stop:1 #003c78)

/* Waveform */
qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 #003c78, stop:0.5 #0078c8, stop:1 #64c8dc)

/* Glass Panel */
qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 rgba(255,255,255,179), stop:0.5 #64c8dc,
                stop:1 rgba(0,120,200,77))
```

### For Python QPainter:
```python
gradient = QLinearGradient(0, 0, 0, height)
gradient.setColorAt(0.0, QColor(176, 208, 224))
gradient.setColorAt(0.5, QColor(0, 120, 200))
gradient.setColorAt(1.0, QColor(0, 60, 120))
```

### For CSS (Web/HTML):
```css
background: linear-gradient(to bottom,
    #b0d0e0 0%,
    #0078c8 50%,
    #003c78 100%);
```

---

## AESTHETIC PRINCIPLES CHECKLIST

When designing with Frutiger Aero, ask yourself:

- [ ] Is this glossy/shiny or flat? (Should be glossy)
- [ ] Does it have depth? (Use gradients + shadows)
- [ ] Are colors cool? (Blue, cyan, green - not warm)
- [ ] Is text legible? (Good contrast, humanist font)
- [ ] Does it feel 2000s? (Skeuomorphic, not minimalist)
- [ ] Is there a highlight band? (Top gradient lighter)
- [ ] Are corners slightly rounded? (2-4px radius)
- [ ] Is there soft shadow? (Drop shadow, inset shadow)
- [ ] Nature imagery included? (Optional but authentic)
- [ ] Translucent layers? (Glass effect, semi-transparency)

---

## COLOR SWATCHES (Easy Reference)

```
████████ #003c78  Azure Dragon
████████ #0050a0  Princess Blue
████████ #0064b4  Cobalt Stone
████████ #0078c8  Science Blue ← PRIMARY
████████ #64c8dc  Rushing Stream
████████ #ffffff  White
████████ #f0f8ff  Alice Blue
████████ #e8f4f8  Soft Cyan
████████ #71ab23  Grass Green
████████ #d55e0f  Burnt Orange
████████ #fbb905  Golden Yellow
```

---

## FILE REFERENCES

- **Main Design Document**: `FRUTIGER_AERO_DESIGN_REPORT.md`
- **Implementation Code**: `PYQT6_IMPLEMENTATION_GUIDE.md`
- **Resources**: https://frutigeraeroarchive.org/
- **Palettes**: https://colorswall.com/palette/271665
- **Winamp Skins**: https://skins.webamp.org/

---

## DARK AERO VARIANT

For a dark theme, swap:

```
#ffffff      → #1a2a3a  (dark blue background)
#f0f8ff      → #1a2a3a  (alice blue → dark)
#e8f4f8      → #2a3a4a  (soft cyan → dark surface)
#003c78      → #ffffff  (dark blue → white text)
#64c8dc      → #b0d0e0  (cyan → light blue)
```

Keep the bright blues (#0078c8, #0050a0) the same for contrast.

---

## WAVEFORM IDEAS

### Gradient Fill (Most Authentic)
- Fill from bottom with gradient
- Colors: Cyan (quiet) → Blue (mid) → Dark Blue (loud)
- Semi-transparent (30-40% opacity)

### Peak Indicators
- Small circles or triangles
- Color: #0078c8 or #fbb905
- Update in real-time
- Optional glow effect

### Spectrum Analyzer
- Multiple bars/columns
- Gradient from cyan (low freq) to dark blue (high freq)
- Smooth animation

### Bokeh Background
- Semi-transparent circles
- Color: #64c8dc or #0078c8
- Opacity: 20-30%
- Sizes: 20px to 100px
- Optional floating animation

