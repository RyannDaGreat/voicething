# FRUTIGER AERO - VISUAL CHEAT SHEET

## The Perfect Button (Copy This)

```css
.aero-button {
  /* Core Styling */
  padding: 10px 20px;
  border: none;
  border-radius: 12px;
  cursor: pointer;
  position: relative;
  overflow: hidden;

  /* The Magic: Gradient 135° */
  background: linear-gradient(135deg, #87CEEB 0%, #0087BE 100%);

  /* The Magic: 3-Layer Shadows */
  box-shadow:
    inset 0 1px 0 rgba(255,255,255,0.4),    /* ← Light top */
    inset 0 -2px 0 rgba(0,0,0,0.1),         /* ← Dark bottom */
    0 2px 4px rgba(0,0,0,0.2);              /* ← Drop shadow */

  /* Typography */
  font-family: "Segoe UI", "Frutiger", "Helvetica Neue", sans-serif;
  font-weight: 500;
  color: #333;

  /* Smooth Transition */
  transition: all 0.3s cubic-bezier(0.25, 0.46, 0.45, 0.94);
}

/* The Glossy Shine (White Teardrop) */
.aero-button::before {
  content: '';
  position: absolute;
  top: 0;
  left: 20%;
  width: 25%;
  height: 50%;
  background: radial-gradient(ellipse at center, rgba(255,255,255,0.6), transparent);
  border-radius: 50%;
  filter: blur(3px);
  pointer-events: none;
}

/* Hover: Brighter & More Prominent */
.aero-button:hover {
  background: linear-gradient(135deg, #99D9FF 0%, #0099D9 100%);
  box-shadow:
    inset 0 1px 0 rgba(255,255,255,0.5),
    inset 0 -2px 0 rgba(0,0,0,0.15),
    0 4px 8px rgba(0,0,0,0.25);
}

.aero-button:hover::before {
  background: radial-gradient(ellipse at center, rgba(255,255,255,0.8), transparent);
}

/* Active: Pressed Down */
.aero-button:active {
  background: linear-gradient(135deg, #0087BE 0%, #005A8B 100%);
  box-shadow:
    inset 0 2px 4px rgba(0,0,0,0.3),
    0 1px 2px rgba(0,0,0,0.15);
}

/* Disabled: Desaturated */
.aero-button:disabled {
  background: linear-gradient(135deg, #C0C0C0 0%, #808080 100%);
  opacity: 0.6;
  cursor: not-allowed;
}
```

---

## One-Line Color Swatches

```
SKY BLUE       #87CEEB ────────────→ #0087BE
WATER TEAL     #40E0D0 ────────────→ #00A896
GRASS GREEN    #90EE90 ────────────→ #228B22
AURORA PURPLE  #FFB6C1 ────────────→ #87CEEB
NEUTRAL WHITE  #FFFFFF ────────────→ #D3D3D3
```

---

## The 3 Key Gradients

### 1. Sky Blue (Most Used)
```css
linear-gradient(135deg, #87CEEB 0%, #0087BE 100%)
```

### 2. Water Teal (Fresh Alternative)
```css
linear-gradient(135deg, #40E0D0 0%, #00A896 100%)
```

### 3. Grass Green (Positive Actions)
```css
linear-gradient(135deg, #90EE90 0%, #228B22 100%)
```

---

## The Shadow Layers (Always Use These)

```css
/* Top Highlight - Creates Light Reflection */
inset 0 1px 0 rgba(255,255,255,0.4)

/* Bottom Shadow - Creates Depth */
inset 0 -2px 0 rgba(0,0,0,0.1)

/* Drop Shadow - Creates Floating Effect */
0 2px 4px rgba(0,0,0,0.2)
```

All three together:
```css
box-shadow:
  inset 0 1px 0 rgba(255,255,255,0.4),
  inset 0 -2px 0 rgba(0,0,0,0.1),
  0 2px 4px rgba(0,0,0,0.2);
```

---

## The Glossy Shine (Make It Wet)

```css
.element::before {
  content: '';
  position: absolute;
  top: 0;
  left: 20%;
  width: 25%;
  height: 50%;
  background: radial-gradient(ellipse at center,
              rgba(255,255,255,0.6),    /* ← 60% opaque white */
              transparent);
  border-radius: 50%;
  filter: blur(3px);                    /* ← Soft edges */
  pointer-events: none;
}
```

---

## Everything at 135°

```
Light Source
(top-left)
    ↘ 135°
    ╔═════════╗
    ║ Lighter ║
    ║ at top  ║
    ║ Darker  ║
    ║ at bot  ║
    ╚═════════╝
          ↙
    Shadow
(bottom-right)
```

Always use: `linear-gradient(135deg, LIGHT_COLOR 0%, DARK_COLOR 100%)`

---

## Quick Element Templates

### Glossy Button
```css
background: linear-gradient(135deg, #87CEEB, #0087BE);
box-shadow: inset 0 1px 0 rgba(255,255,255,0.4), inset 0 -2px 0 rgba(0,0,0,0.1), 0 2px 4px rgba(0,0,0,0.2);
border-radius: 12px;
```

### Glass Panel
```css
background: rgba(255,255,255,0.1);
backdrop-filter: blur(10px);
border: 1px solid rgba(255,255,255,0.2);
border-radius: 12px;
box-shadow: inset 0 1px 0 rgba(255,255,255,0.3), 0 4px 8px rgba(0,0,0,0.1);
```

### Bubble/Sphere
```css
border-radius: 50%;
background: radial-gradient(circle at 35% 35%, rgba(255,255,255,0.4), transparent), radial-gradient(circle, #87CEEB, #0087BE);
box-shadow: inset -10px -10px 20px rgba(0,0,0,0.3), inset 5px 5px 10px rgba(255,255,255,0.5), 0 10px 20px rgba(0,0,0,0.2);
```

---

## Colors by Purpose

```
BUTTONS          → Sky Blue (#87CEEB/#0087BE)
SECONDARY        → Water Teal (#40E0D0/#00A896)
SUCCESS/POSITIVE → Grass Green (#90EE90/#228B22)
BACKGROUNDS      → White/Off-white (#FFFFFF/#F5F5F5)
SPECIAL/PREMIUM  → Aurora/Glass effects
DISABLED         → Gray (#C0C0C0/#808080) at 60% opacity
TEXT (light bg)  → #333 with text-shadow
TEXT (dark bg)   → #FFFFFF with dark text-shadow
```

---

## Hover Effects (Pick One or Combine)

### Brightness Boost
```css
.element:hover {
  filter: brightness(1.1);
}
```

### Glow Effect
```css
.element:hover {
  box-shadow: /* existing */, 0 6px 12px rgba(0,135,190,0.3);
}
```

### Shadow Expansion
```css
.element:hover {
  box-shadow: /* existing */ 0 4px 8px rgba(0,0,0,0.25);
}
```

### Highlight Increase
```css
.element:hover::before {
  background: radial-gradient(ellipse at center, rgba(255,255,255,0.8), transparent);
}
```

---

## Animation Easing

```css
/* Use This For All Transitions */
transition: all 0.3s cubic-bezier(0.25, 0.46, 0.45, 0.94);

/* Duration */
0.2s - quick interactions
0.3s - standard
0.5s - slower, emphasized

/* Combine with transforms */
.element:hover {
  transform: translateY(-2px);
  transition: all 0.3s cubic-bezier(0.25, 0.46, 0.45, 0.94);
}
```

---

## Rounded Corners (Go Bigger!)

```
MIN:  8px    (small elements)
STD:  12px   (buttons, panels)
MAX:  16px   (large buttons)
CIRC: 50%    (circles, bubbles)
```

---

## Common Opacity Values

```
Glossy Shine Top     → 0.4 - 0.6
Inner Light Shadow   → 0.3 - 0.5
Inner Dark Shadow    → 0.1 - 0.15
Drop Shadow          → 0.2 - 0.25
Text Shadow (light)  → 0.5 - 0.8
Text Shadow (dark)   → 0.3 - 0.5
Disabled Element     → 0.6 (reduced)
Glass Background     → 0.1 (very transparent)
```

---

## Text Treatment

### Light Background
```css
color: #333333;
text-shadow: 0 1px 0 rgba(255,255,255,0.8);
```

### Dark/Colored Background
```css
color: #FFFFFF;
text-shadow: 0 1px 3px rgba(0,0,0,0.3);
```

### On Glass
```css
color: rgba(0,0,0,0.8);
text-shadow: 0 1px 3px rgba(255,255,255,0.7);
```

---

## Font Stack

```css
font-family: "Segoe UI", "Frutiger", "Helvetica Neue", system-ui, sans-serif;
```

Or just:
```css
font-family: "Segoe UI", sans-serif;
```

---

## CSS Variables (Optional but Recommended)

```css
:root {
  --aero-blue-light: #87CEEB;
  --aero-blue-dark: #0087BE;
  --aero-teal-light: #40E0D0;
  --aero-teal-dark: #00A896;
  --aero-green-light: #90EE90;
  --aero-green-dark: #228B22;
  --aero-radius: 12px;
  --aero-easing: cubic-bezier(0.25, 0.46, 0.45, 0.94);
  --aero-shadow: 0 2px 4px rgba(0,0,0,0.2);
  --aero-shadow-inset-top: inset 0 1px 0 rgba(255,255,255,0.4);
  --aero-shadow-inset-bottom: inset 0 -2px 0 rgba(0,0,0,0.1);
}
```

---

## Before vs After

### BEFORE (Flat, Plain)
```css
.button {
  background: #87CEEB;
  border-radius: 4px;
  padding: 10px 20px;
}
```

### AFTER (Glossy, Aero)
```css
.button {
  background: linear-gradient(135deg, #87CEEB 0%, #0087BE 100%);
  border-radius: 12px;
  padding: 10px 20px;
  box-shadow:
    inset 0 1px 0 rgba(255,255,255,0.4),
    inset 0 -2px 0 rgba(0,0,0,0.1),
    0 2px 4px rgba(0,0,0,0.2);
  position: relative;
  overflow: hidden;
}

.button::before {
  content: '';
  position: absolute;
  top: 0; left: 20%;
  width: 25%; height: 50%;
  background: radial-gradient(ellipse, rgba(255,255,255,0.6), transparent);
  border-radius: 50%;
  filter: blur(3px);
}
```

---

## Common Mistakes

| ❌ Mistake | ✓ Fix |
|-----------|-------|
| Single shadow only | Use 3-layer system |
| No glossy highlight | Add ::before shine |
| Sharp corners | Use 8-12px border-radius |
| Gradient 180° | Use 135° angle |
| Oversaturated colors | Use lighter, more natural tones |
| Hard-edged shine | Add blur: filter: blur(3px) |
| No transitions | Use 0.3s cubic-bezier |
| Linear easing | Use cubic-bezier(0.25, 0.46, 0.45, 0.94) |
| Monochromatic | Use nature colors (sky, water, grass) |
| Cramped layout | Increase padding & margins |

---

## Print This Page!

Keep this cheat sheet nearby while coding. The key sections:
- The Perfect Button
- One-Line Color Swatches
- The 3 Key Gradients
- The Shadow Layers
- The Glossy Shine
- Colors by Purpose

---

## Final Checklist

Before considering done:
- [ ] Button has white glossy shine at top-left
- [ ] Button has 135° gradient (light to dark)
- [ ] Button has 3-layer shadow system
- [ ] Button has rounded corners (12px+)
- [ ] Hover state is noticeably different
- [ ] Active state looks pressed
- [ ] Disabled state is desaturated
- [ ] Typography uses Segoe UI or Frutiger
- [ ] Colors are nature-inspired
- [ ] All transitions smooth (0.3s)
- [ ] Text is readable on all backgrounds
- [ ] Layout has generous whitespace

---

That's everything you need to make beautiful Aero interfaces!

Copy the button code, pick your colors, apply the shadows, and you're done.

Good luck! 🎨
