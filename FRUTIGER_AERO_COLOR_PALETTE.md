# FRUTIGER AERO COLOR PALETTE & GRADIENTS

## Complete Color Reference

### Sky Blue Palette
```
Light Sky:       #87CEEB   RGB(135, 206, 235)
Medium Sky:      #00B8E6   RGB(0, 184, 230)
Metallic Sky:    #87DDED   RGB(135, 221, 237)
Dark Sky:        #0087BE   RGB(0, 135, 190)
Very Dark Sky:   #005A8B   RGB(0, 90, 139)
```

### Water Teal Palette
```
Cyan:            #00CED1   RGB(0, 206, 209)
Turquoise:       #40E0D0   RGB(64, 224, 208)
Bright Cyan:     #0AFAFE   RGB(10, 250, 254)
Dark Turquoise:  #00A896   RGB(0, 168, 150)
Medium Teal:     #20B2AA   RGB(32, 178, 170)
```

### Grass Green Palette
```
Light Green:     #90EE90   RGB(144, 238, 144)
Pale Green:      #98FB98   RGB(152, 251, 152)
Medium Green:    #3CB371   RGB(60, 179, 113)
Dark Green:      #228B22   RGB(34, 139, 34)
Forest Green:    #1a6b1a   RGB(26, 107, 26)
```

### Aurora Palette
```
Light Pink:      #FFB6C1   RGB(255, 182, 193)
Hot Pink:        #FF69B4   RGB(255, 105, 180)
Plum/Purple:     #DDA0DD   RGB(221, 160, 221)
Lavender:        #B19CD9   RGB(177, 156, 217)
Soft Purple:     #D8BFD8   RGB(216, 191, 216)
```

### Neutral Palette
```
White:           #FFFFFF   RGB(255, 255, 255)
Off-White:       #F5F5F5   RGB(245, 245, 245)
Very Light Gray: #FAFAFA   RGB(250, 250, 250)
Light Gray:      #E8E8E8   RGB(232, 232, 232)
Medium Gray:     #D3D3D3   RGB(211, 211, 211)
Silver:          #C0C0C0   RGB(192, 192, 192)
Dark Gray:       #808080   RGB(128, 128, 128)
```

---

## Pre-Made Gradient Combinations

### Sky-to-Ocean (Water Transition)
```css
background: linear-gradient(135deg, #87CEEB 0%, #00CED1 100%);
```
**Use for**: Buttons, panels, backgrounds suggesting water and sky

### Grass-to-Sky (Landscape)
```css
background: linear-gradient(135deg, #90EE90 0%, #87CEEB 100%);
```
**Use for**: Nature-themed sections, alternative button set

### Aurora Effect (Northern Lights)
```css
background: linear-gradient(135deg, #FFB6C1 0%, #DDA0DD 50%, #87CEEB 100%);
```
**Use for**: Special sections, premium panels, accent backgrounds

### Metallic Glass (Silver-Blue)
```css
background: linear-gradient(135deg, #FFFFFF 0%, #D3D3D3 50%, #87DDED 100%);
```
**Use for**: Glossy panels, metallic-looking elements

### Fresh Green
```css
background: linear-gradient(135deg, #90EE90 0%, #228B22 100%);
```
**Use for**: Action buttons (positive actions), success states

### Teal Vibrancy (Water Focus)
```css
background: linear-gradient(135deg, #40E0D0 0%, #00A896 100%);
```
**Use for**: Modern, fresh buttons, premium features

### Deep Ocean
```css
background: linear-gradient(135deg, #00B8E6 0%, #005A8B 100%);
```
**Use for**: Darker theme, main actions, prominent buttons

### Soft Aurora (Subtle)
```css
background: linear-gradient(135deg, #E0D7FF 0%, #FFE0EE 50%, #E0F6FF 100%);
```
**Use for**: Light backgrounds, subtle panel distinctions

### Purple Aurora (Focus)
```css
background: linear-gradient(135deg, #DDA0DD 0%, #87CEEB 100%);
```
**Use for**: Secondary actions, highlighted elements

---

## Shine/Highlight Colors

### For Blue Buttons
```css
/* Primary highlight (on top of blue gradient) */
background: radial-gradient(ellipse at 35% 35%, rgba(255, 255, 255, 0.4), transparent);

/* Alternative: warm highlight for glossiness */
background: radial-gradient(ellipse at 35% 35%, rgba(255, 250, 205, 0.3), transparent);
```

### For Green Buttons
```css
/* White shine */
background: radial-gradient(ellipse at 35% 35%, rgba(255, 255, 255, 0.5), transparent);
```

### For Teal Buttons
```css
/* Bright cyan shine */
background: radial-gradient(ellipse at 35% 35%, rgba(200, 255, 255, 0.4), transparent);
```

---

## Shadow Colors (Depth)

### Standard Dark Shadow
```css
box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
```

### Blue-Tinted Shadow (Underwater)
```css
box-shadow: 0 4px 8px rgba(0, 135, 190, 0.2);
```

### Green-Tinted Shadow (Natural)
```css
box-shadow: 0 4px 8px rgba(34, 139, 34, 0.15);
```

### Soft Inner Shadow (Inset Depth)
```css
box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.4);  /* highlight top */
box-shadow: inset 0 -1px 0 rgba(0, 0, 0, 0.1);       /* shadow bottom */
```

---

## Text Colors (On Different Backgrounds)

### Dark Text (Default)
```
Color: #333333   RGB(51, 51, 51)
```
Use on light backgrounds

### Medium Text (Secondary)
```
Color: #666666   RGB(102, 102, 102)
```
Use for less important information

### Blue Text (Links/Emphasis)
```
Color: #0087BE   RGB(0, 135, 190)
```
Use for clickable or emphasized text

### White Text (On Colored Backgrounds)
```
Color: #FFFFFF   RGB(255, 255, 255)
Text-shadow: 0 1px 2px rgba(0, 0, 0, 0.3);
```
Use on dark or saturated backgrounds

### Light Gray Text (Subtle/Disabled)
```
Color: #999999   RGB(153, 153, 153)
Opacity: 0.7;
```
Use for disabled or secondary text

---

## Complete CSS Palette Declaration

```css
:root {
  /* Sky Blues */
  --sky-light: #87CEEB;
  --sky-medium: #00B8E6;
  --sky-metallic: #87DDED;
  --sky-dark: #0087BE;
  --sky-very-dark: #005A8B;

  /* Water Teals */
  --water-cyan: #00CED1;
  --water-turquoise: #40E0D0;
  --water-bright: #0AFAFE;
  --water-dark: #00A896;
  --water-medium: #20B2AA;

  /* Grass Greens */
  --grass-light: #90EE90;
  --grass-pale: #98FB98;
  --grass-medium: #3CB371;
  --grass-dark: #228B22;
  --grass-very-dark: #1a6b1a;

  /* Aurora Palette */
  --aurora-pink: #FFB6C1;
  --aurora-hot-pink: #FF69B4;
  --aurora-plum: #DDA0DD;
  --aurora-lavender: #B19CD9;
  --aurora-soft-purple: #D8BFD8;

  /* Neutrals */
  --neutral-white: #FFFFFF;
  --neutral-off-white: #F5F5F5;
  --neutral-very-light: #FAFAFA;
  --neutral-light-gray: #E8E8E8;
  --neutral-medium-gray: #D3D3D3;
  --neutral-silver: #C0C0C0;
  --neutral-dark-gray: #808080;

  /* Text Colors */
  --text-primary: #333333;
  --text-secondary: #666666;
  --text-accent: #0087BE;
  --text-white: #FFFFFF;
  --text-disabled: #999999;

  /* Gradient Stops */
  --gradient-sky-to-water: linear-gradient(135deg, var(--sky-light) 0%, var(--water-cyan) 100%);
  --gradient-grass-to-sky: linear-gradient(135deg, var(--grass-light) 0%, var(--sky-light) 100%);
  --gradient-aurora: linear-gradient(135deg, var(--aurora-pink) 0%, var(--aurora-plum) 50%, var(--sky-light) 100%);
  --gradient-teal: linear-gradient(135deg, var(--water-turquoise) 0%, var(--water-dark) 100%);
  --gradient-green: linear-gradient(135deg, var(--grass-light) 0%, var(--grass-dark) 100%);
  --gradient-deep: linear-gradient(135deg, var(--sky-medium) 0%, var(--sky-very-dark) 100%);

  /* Shadows */
  --shadow-drop: 0 2px 4px rgba(0, 0, 0, 0.2);
  --shadow-drop-large: 0 4px 8px rgba(0, 0, 0, 0.15);
  --shadow-inset-top: inset 0 1px 0 rgba(255, 255, 255, 0.4);
  --shadow-inset-bottom: inset 0 -1px 0 rgba(0, 0, 0, 0.1);
  --shadow-glow-blue: 0 4px 8px rgba(0, 135, 190, 0.2);
  --shadow-glow-green: 0 4px 8px rgba(34, 139, 34, 0.15);

  /* Transitions */
  --easing-aero: cubic-bezier(0.25, 0.46, 0.45, 0.94);
  --transition-smooth: all 0.3s var(--easing-aero);
}
```

---

## Usage Examples

### Use Sky Blue for:
- Main action buttons
- Primary UI elements
- Default state elements
- Primary navigation

### Use Teal/Water for:
- Secondary actions
- Alternative button sets
- Progressive/flowing elements
- Nature-themed sections

### Use Green for:
- Positive/success actions
- Affirmative buttons
- Growth-oriented features

### Use Aurora for:
- Premium/special sections
- Backgrounds
- Accent highlights
- Special effects

### Use Neutral Gray for:
- Backgrounds (off-white/light gray)
- Secondary panels
- Disabled states
- Subtle elements

---

## Color Accessibility Notes

- All primary text on light backgrounds maintains sufficient contrast
- All buttons with white text maintain WCAG AA compliance
- Avoid using Aurora pink/purple for text (insufficient contrast)
- Always test contrast ratios for text on gradients
- Use `text-shadow` for white text on light backgrounds

---

## Mixing & Matching Guide

**Harmonious Combinations:**
- Sky Blue + White backgrounds (classic)
- Teal + Off-white backgrounds (modern water)
- Green + Light gray backgrounds (natural)
- Aurora + White backgrounds (premium)
- Multiple color buttons on neutral background (playful)

**Color Temperature:**
- Warm (pinks, purples, peachy tones): Use on cool backgrounds
- Cool (blues, teals, greens): Use on warm/neutral backgrounds
- Light (pastels): Use with darker text
- Dark (forest, navy): Use with light text

**Visual Weight:**
- Darker colors = heavier/more important
- Lighter colors = lighter/secondary
- Saturated colors = emphasis
- Desaturated colors = subtle

This palette ensures authentic Frutiger Aero aesthetics while maintaining modern web standards and accessibility.
