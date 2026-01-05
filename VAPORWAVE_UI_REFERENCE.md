# Vaporwave UI Design Reference for PyQt6

## Overview
Vaporwave is a retro-futuristic aesthetic rooted in 1980s-90s nostalgia, characterized by pastel neon colors, gradient overlays, geometric shapes, and surreal imagery. For **desktop app UI**, prioritize readability with proper contrast while maintaining the aesthetic's signature dreamy, nostalgic quality.

---

## 1. COLOR PALETTE

### Primary Vaporwave Colors (Hex & RGB)

| Name | Hex | RGB | Usage |
|------|-----|-----|-------|
| Hot Pink | `#FF71CE` | rgb(255, 113, 206) | Primary accent, buttons, highlights |
| Cyan / Electric Blue | `#01CDFE` | rgb(1, 205, 254) | Secondary accent, borders, contrast |
| Mint Green | `#05FFA1` | rgb(5, 255, 161) | Tertiary accent, highlights |
| Purple / Lavender | `#B967FF` | rgb(185, 103, 255) | Text, elements, accents |
| Pale Yellow | `#FFFB96` | rgb(255, 251, 150) | Warm accent, subtle backgrounds |
| Magenta | `#FF06C1` | rgb(255, 6, 193) | Bold emphasis |
| Deep Purple | `#8705E4` | rgb(135, 5, 228) | Dark accents, borders |
| Sky Blue | `#11B4F5` | rgb(17, 180, 245) | Light accent |
| Aqua | `#0DFDF9` | rgb(13, 253, 249) | Bright accent |
| Warm Orange | `#F9AB53` | rgb(249, 171, 83) | Softer accent |

### Background & Neutral Colors

| Name | Hex | RGB | Usage |
|------|-----|-----|-------|
| Dark Plum (Background) | `#300350` | rgb(48, 3, 80) | Main background |
| Deep Magenta | `#94157F` | rgb(148, 21, 127) | Darker background option |
| Off-white / Pale | `#F5F5F5` | rgb(245, 245, 245) | Light mode option |
| Light Lavender | `#E8E0FF` | rgb(232, 224, 255) | Light mode background |

### Color Usage Guidelines for Readability

**IMPORTANT**: Avoid the mistake of cyan text on gray backgrounds (unreadable).

- **Text on Dark Backgrounds**: Use pale yellow, mint green, or white for maximum contrast
- **Text on Light Backgrounds**: Use deep purple, dark plum, or navy for maximum contrast
- **Interactive Elements**: Hot pink, bright magenta (255,6,193) for button hover/active states
- **Borders**: Use cyan or purple at full saturation
- **Disabled States**: Use muted purples or grays (reduce saturation/brightness)

---

## 2. TYPOGRAPHY

### Recommended Fonts for Vaporwave UI

The key: **blend retro with readability**. Don't use full-width characters or heavily pixelated fonts for body text.

#### Primary Fonts (Headings & Titles)

1. **Futura** (system available on macOS)
   - Clean, geometric, 1980s feel
   - Use for main titles and section headers
   - Weight: Bold, Semi-Bold

2. **Helvetica Neue / Helvetica**
   - Classic 80s sans-serif
   - Modern enough for UI readability
   - Weight: Regular, Bold

3. **Avant Garde** (if available)
   - Geometric, ultra-modern feel
   - Great for accent text

#### Secondary Fonts (Body & UI Text)

1. **SF Pro Display** or **San Francisco** (macOS default)
   - System default, guaranteed readability
   - Modern alternative to retro fonts
   - Use for all body text and UI labels

2. **Segoe UI** (Windows)
   - Clean sans-serif for cross-platform compatibility
   - Default choice for accessibility

#### Accent Fonts (Optional, Limited Use)

1. **Courier New** or monospace
   - For "retro computer" feeling in status bars or data displays
   - Use sparingly, only where retro feel enhances rather than hinders

### Font Sizing & Weight Strategy

- **Main Titles**: 32-48px, Bold
- **Section Headers**: 18-24px, Semi-Bold
- **Labels & UI**: 12-14px, Regular
- **Body Text**: 11-13px, Regular
- **Captions**: 10-11px, Regular

### Typography Color Pairing Examples

```
Header (on dark background):
  - Text: #FFFB96 (pale yellow) or #FF71CE (hot pink)
  - Larger scale (32px+) can use brighter colors

UI Labels (on dark background):
  - Text: #E8E0FF (light lavender) or #FFFB96
  - Size: 12-14px

Interactive Text (buttons):
  - Hover state text: #FFFB96 or white
  - Disabled text: #94157F at 70% opacity

Code/Status (monospace):
  - Text: #05FFA1 (mint green) or #01CDFE (cyan)
  - Background: rgba(48, 3, 80, 0.5) or slightly lighter
```

---

## 3. GRADIENT STYLES

### Primary Gradient Combinations

Vaporwave gradients work best when:
- Transitioning between complementary neon colors
- Applied to backgrounds, not critical text
- Subtle enough not to obscure content

#### Recommended Gradients (Top to Bottom)

1. **Soft Pastel Sunrise**
   ```css
   linear-gradient(180deg, #FF71CE 0%, #01CDFE 100%)
   /* Hot Pink → Cyan */
   ```

2. **Purple Dream**
   ```css
   linear-gradient(180deg, #B967FF 0%, #8705E4 100%)
   /* Light Purple → Deep Purple */
   ```

3. **Tropical Neon**
   ```css
   linear-gradient(180deg, #FF06C1 0%, #05FFA1 100%)
   /* Magenta → Mint */
   ```

4. **Sunset to Sky**
   ```css
   linear-gradient(180deg, #F9AB53 0%, #11B4F5 100%)
   /* Warm Orange → Sky Blue */
   ```

5. **Cyan-to-Plum (Subtle)**
   ```css
   linear-gradient(135deg, #0DFDF9 0%, #300350 100%)
   /* Aqua → Dark Plum (diagonal) */
   ```

### Gradient Application Rules

- **Backgrounds**: Use 45-degree or 135-degree angles for less harsh appearance
- **Opacity Variant**: Apply gradients with 0.05-0.15 opacity over solid backgrounds for subtlety
- **Text Overlays**: Never place important text directly on gradient backgrounds—add a semi-transparent overlay first
- **Buttons/Controls**: Gradients on hover states work well; keep base state solid for clarity

#### Example Gradient Overlay for Text Clarity
```css
/* Semi-transparent dark overlay on gradient background */
background: linear-gradient(180deg, #FF71CE 0%, #01CDFE 100%),
            rgba(48, 3, 80, 0.3);
background-blend-mode: multiply;
```

---

## 4. VISUAL ELEMENTS & PATTERNS

### Core Vaporwave Elements for UI

1. **Geometric Shapes**
   - Squares, circles, triangles in grid layouts
   - Isometric cubes for depth
   - Heavy black/colored outlines for retro feel

2. **Grids & Patterns**
   - Fine horizontal/vertical grid overlay (low opacity, 20-40%)
   - Grid color: lighter purple or cyan at 10-20% opacity
   - Dot patterns or checkerboard in subtle areas

3. **Glitch Effects** (Use Sparingly)
   - Color channel misalignment (R/G/B offset by 2-4px)
   - Best for accent elements, not core UI
   - Example: Duplicate text layer, offset in pink and cyan

4. **Imagery Integration** (Optional)
   - Greek statue busts as decorative elements in corners
   - Palm tree silhouettes in background
   - Sunset gradients behind text elements
   - These work as background decorations, not interactive elements

5. **Scan Lines & Texture** (Optional)
   - Subtle horizontal scan line overlay (1px lines, 3px spacing, 5% opacity)
   - Grainy noise texture layer (3-5% opacity)
   - Only on backgrounds, not text

### Pattern Examples for PyQt6

#### Simple Grid Overlay
```python
# Transparent grid as background
"QWidget { background: #300350 url('grid-pattern.svg') repeat; }"
```

#### Glitch Effect (CSS/Stylesheet)
```css
QLabel#glitch {
    color: #FF71CE;
    text-shadow: -2px 0 #01CDFE, 2px 0 #05FFA1;
}
```

---

## 5. COMPONENT-SPECIFIC GUIDANCE

### Main Window Background
- **Color**: #300350 (dark plum) or #1A1A2E (near-black alternative)
- **Opacity**: Solid (100%)
- **Accent**: Subtle grid overlay at 10% opacity or none

### Button Styles

#### Default Button
```python
background-color: #B967FF;  # Purple
color: #FFFB96;             # Pale yellow text
border: 2px solid #8705E4;  # Darker purple border
padding: 8px 16px;
```

#### Hover State
```python
background-color: #FF71CE;  # Hot pink
color: #FFFB96;
border: 2px solid #FF06C1;  # Magenta border
```

#### Pressed/Active State
```python
background-color: #FF06C1;  # Magenta
color: #FFFB96;
border: 2px solid #FF71CE;  # Hot pink border
```

### Text Input Fields
```python
background-color: rgba(255, 251, 150, 0.05);  # Pale yellow, very subtle
color: #E8E0FF;                               # Light lavender text
border: 1px solid #B967FF;                    # Purple border
selection-background-color: #B967FF;          # Purple selection
```

### Status Bar / Indicators
- **Active/Success**: #05FFA1 (mint green)
- **Warning**: #F9AB53 (warm orange)
- **Error**: #FF71CE (hot pink)
- **Neutral**: #11B4F5 (sky blue)

### Disabled States
Reduce opacity of color to 40-50% or use muted version:
```python
color: rgba(184, 103, 255, 0.5);  # Muted purple
```

---

## 6. PRACTICAL READABILITY CHECKLIST

✓ **DO:**
- Use high contrast text: dark text on light, light text on dark
- Reserve cyan (#01CDFE) for borders, accents, not body text
- Use full saturation colors for interactive elements
- Apply semi-transparent overlays under gradient backgrounds before placing text
- Test color combinations for WCAG AA compliance (4.5:1 contrast minimum)
- Use hot pink and mint green for primary accent text
- Pair pastels with darker backgrounds

✗ **DON'T:**
- Place cyan text on gray or medium-tone backgrounds
- Use gradients for body text backgrounds without overlay
- Mix too many neon colors in one UI element
- Use full-width Unicode characters for regular UI text
- Apply glitch effects to critical UI elements
- Put important content over busy background patterns

---

## 7. EXAMPLE COLOR SCHEMES FOR UI

### Dark Mode (Recommended for Vaporwave)

| Element | Color | Hex |
|---------|-------|-----|
| Background | Dark Plum | `#300350` |
| Text | Pale Yellow | `#FFFB96` |
| Primary Button | Hot Pink | `#FF71CE` |
| Secondary Button | Purple | `#B967FF` |
| Accent | Cyan | `#01CDFE` |
| Border | Deep Purple | `#8705E4` |
| Hover State | Magenta | `#FF06C1` |
| Success | Mint Green | `#05FFA1` |
| Warning | Orange | `#F9AB53` |

### Light Mode (Alternative)

| Element | Color | Hex |
|---------|-------|-----|
| Background | Off-white | `#F5F5F5` |
| Text | Deep Purple | `#300350` |
| Primary Button | Hot Pink | `#FF71CE` |
| Secondary Button | Purple | `#B967FF` |
| Accent | Cyan | `#01CDFE` |
| Border | Light Lavender | `#E8E0FF` |
| Hover State | Magenta | `#FF06C1` |
| Success | Mint Green | `#05FFA1` |

---

## 8. RESOURCES & EXAMPLES

### Reference Websites
- **Nightwave Plaza**: Excellent Vaporwave UI example (radio streaming interface)
- **Dribbble**: 2,000+ vaporwave design examples
- **Color-Hex**: Specific vaporwave color palettes and hex codes
- **Adobe Express**: Design tips and tutorials

### Gradient Tools
- CSS Gradient Generator (for fine-tuning exact gradients)
- Coolors.co (color palette building)

### Font Recommendations for macOS
- System fonts: SF Pro Display, Helvetica Neue, Futura
- Free: Google Fonts has good retro-futuristic options

---

## 9. IMPLEMENTATION TIPS FOR PyQT6

### Color Constants in Python
```python
# Define as module constants
VAPORWAVE_COLORS = {
    'hot_pink': '#FF71CE',
    'cyan': '#01CDFE',
    'mint': '#05FFA1',
    'purple': '#B967FF',
    'pale_yellow': '#FFFB96',
    'magenta': '#FF06C1',
    'deep_purple': '#8705E4',
    'dark_plum': '#300350',
    'warm_orange': '#F9AB53',
    'sky_blue': '#11B4F5',
}
```

### Stylesheet Template
```python
VAPORWAVE_STYLESHEET = """
    QMainWindow {
        background-color: #300350;
    }

    QLabel {
        color: #FFFB96;
        font-family: 'Helvetica Neue';
        font-size: 12px;
    }

    QPushButton {
        background-color: #B967FF;
        color: #FFFB96;
        border: 2px solid #8705E4;
        border-radius: 4px;
        padding: 8px 16px;
        font-weight: bold;
    }

    QPushButton:hover {
        background-color: #FF71CE;
        border: 2px solid #FF06C1;
    }

    QLineEdit {
        background-color: rgba(255, 251, 150, 0.05);
        color: #E8E0FF;
        border: 1px solid #B967FF;
        padding: 6px;
    }
"""
```

### Testing Contrast
Before deploying, verify contrast ratios using:
- WebAIM Contrast Checker
- Python: `colorsys` or custom contrast calculation
- WCAG AAA minimum: 7:1 contrast ratio

---

## Summary: The Vaporwave Aesthetic for Pretty, Readable UI

**Key Principles:**
1. Dark plum background (#300350) is your foundation
2. Hot pink (#FF71CE) and cyan (#01CDFE) are your heroes—use them for buttons and highlights
3. Pale yellow (#FFFB96) is your primary text color—high contrast and readable
4. Mint green (#05FFA1) for success/active states
5. Purple (#B967FF) for secondary buttons and subtle accents
6. Never put cyan text on ambiguous backgrounds—always pair with dark/light
7. Gradients work best at 45° angle, subtle and in backgrounds
8. System fonts (Helvetica, Futura, San Francisco) over decorative fonts for UI readability
9. Glitch and nostalgia elements are accents, not foundations

**The Sweet Spot**: Nostalgic 80s/90s vibes with clean, modern readability. Think "vaporwave music playlist" UI, not "album cover."

