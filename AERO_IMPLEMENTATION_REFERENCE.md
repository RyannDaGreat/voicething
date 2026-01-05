# AERO IMPLEMENTATION QUICK REFERENCE CARD

## The 3-Layer Shadow System (Foundation)

Every Aero element uses this shadow combination:

```css
box-shadow:
  inset 0 1px 0 rgba(255,255,255,0.4),    /* LAYER 1: Top highlight - creates light reflection */
  inset 0 -2px 0 rgba(0,0,0,0.1),          /* LAYER 2: Bottom shadow - creates depth */
  0 2px 4px rgba(0,0,0,0.2);               /* LAYER 3: Drop shadow - floating effect */
```

**Why this works:**
- Layer 1 (top light): Shows light bouncing off surface → wetness
- Layer 2 (bottom dark): Creates dimension → 3D appearance
- Layer 3 (drop): Separates from background → floating/elevated

---

## The Gradient Formula

```css
/* Always 135° angle (top-left to bottom-right) */
background: linear-gradient(135deg, LIGHTER_COLOR 0%, DARKER_COLOR 100%);
```

**Examples:**
```css
/* Sky Blue */
linear-gradient(135deg, #87CEEB 0%, #0087BE 100%)

/* Water Teal */
linear-gradient(135deg, #40E0D0 0%, #00A896 100%)

/* Grass Green */
linear-gradient(135deg, #90EE90 0%, #228B22 100%)
```

**Key principle:** Top-left is always lighter (light source direction)

---

## The Glossy Shine Layer

The trademark white teardrop highlight at the top:

```css
.element::before {
  content: '';
  position: absolute;

  /* Position: top-left area */
  top: 0;
  left: 20%;
  width: 25%;
  height: 50%;

  /* Radial gradient for sphere appearance */
  background: radial-gradient(
    ellipse at center,
    rgba(255, 255, 255, 0.6),  /* center bright */
    transparent                  /* edges fade out */
  );

  /* Shape and blur */
  border-radius: 50%;
  filter: blur(3px);

  pointer-events: none;
}
```

**Opacity values:**
- Default: 0.4-0.6 (subtle but visible)
- Hover: 0.8+ (more prominent)
- Active: 0.2-0.3 (less visible, pressed)

---

## Color Swatches (Actual Values)

### Primary Blues (Use Most)
```
#87CEEB - Light Sky Blue (button top)
#0087BE - Dark Blue (button bottom)
```

### Water Teals (Modern Alternative)
```
#40E0D0 - Bright Turquoise (button top)
#00A896 - Dark Teal (button bottom)
```

### Greens (Positive Actions)
```
#90EE90 - Light Green (button top)
#228B22 - Dark Green (button bottom)
```

### Purples (Aurora/Special)
```
#DDA0DD - Plum (background/accent)
#87CEEB - Sky Blue (complementary)
```

### Grays (Backgrounds)
```
#FFFFFF - Pure White (main background)
#F5F5F5 - Off-white (subtle panels)
#E8E8E8 - Light gray (section dividers)
```

---

## Button States (Copy-Paste Ready)

### DEFAULT STATE
```css
.button {
  background: linear-gradient(135deg, #87CEEB 0%, #0087BE 100%);
  box-shadow:
    inset 0 1px 0 rgba(255,255,255,0.4),
    inset 0 -2px 0 rgba(0,0,0,0.1),
    0 2px 4px rgba(0,0,0,0.2);
}
```

### HOVER STATE
```css
.button:hover {
  background: linear-gradient(135deg, #99D9FF 0%, #0099D9 100%);
  box-shadow:
    inset 0 1px 0 rgba(255,255,255,0.5),
    inset 0 -2px 0 rgba(0,0,0,0.15),
    0 4px 8px rgba(0,0,0,0.25);
}
```

### ACTIVE STATE
```css
.button:active {
  background: linear-gradient(135deg, #0087BE 0%, #005A8B 100%);
  box-shadow:
    inset 0 2px 4px rgba(0,0,0,0.3),
    0 1px 2px rgba(0,0,0,0.15);
}
```

### DISABLED STATE
```css
.button:disabled {
  background: linear-gradient(135deg, #C0C0C0 0%, #808080 100%);
  opacity: 0.6;
  cursor: not-allowed;
}
```

---

## Element Properties (Always Use)

### Corners
```css
border-radius: 8px;   /* minimum */
border-radius: 12px;  /* standard */
border-radius: 16px;  /* large buttons */
border-radius: 50%;   /* circles/bubbles */
```

### Transitions
```css
transition: all 0.3s cubic-bezier(0.25, 0.46, 0.45, 0.94);
```

### Font
```css
font-family: "Segoe UI", "Frutiger", "Helvetica Neue", sans-serif;
```

### Spacing
```css
padding: 10px 20px;     /* buttons */
margin: 8px 0;          /* between elements */
gap: 12px;              /* between flex items */
```

---

## Glass Panel Template

```css
.glass-panel {
  /* Frosted glass appearance */
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);

  /* Border with gradient */
  border: 1px solid rgba(255, 255, 255, 0.2);

  /* Rounded corners */
  border-radius: 12px;

  /* Padding and spacing */
  padding: 20px;

  /* Depth shadows */
  box-shadow:
    inset 0 1px 0 rgba(255, 255, 255, 0.3),
    0 4px 8px rgba(0, 0, 0, 0.1);
}
```

---

## Bubble/Sphere Template

```css
.bubble {
  width: 80px;
  height: 80px;
  border-radius: 50%;

  /* 3D sphere gradient */
  background:
    radial-gradient(circle at 35% 35%, rgba(255,255,255,0.4), transparent),
    radial-gradient(circle, #87CEEB 0%, #0087BE 100%);

  /* Depth shadows */
  box-shadow:
    inset -10px -10px 20px rgba(0,0,0,0.3),
    inset 5px 5px 10px rgba(255,255,255,0.5),
    0 10px 20px rgba(0,0,0,0.2);
}
```

---

## Hover Effects

### Glow Effect
```css
.element:hover {
  box-shadow: /* ... existing shadows ..., */
              0 6px 12px rgba(0, 135, 190, 0.3);  /* colored glow */
}
```

### Brightness Boost
```css
.element:hover {
  filter: brightness(1.1);
}
```

### Combination
```css
.element:hover {
  background: linear-gradient(135deg, #99D9FF 0%, #0099D9 100%);
  filter: brightness(1.05);
  box-shadow: /* ... with larger shadows */;
}
```

---

## Text on Aero Elements

### On Light Background
```css
color: #333333;
text-shadow: 0 1px 0 rgba(255, 255, 255, 0.8);
```

### On Colored Button
```css
color: #333333;
text-shadow: 0 1px 0 rgba(255, 255, 255, 0.5);
```

### On Dark/Saturated Background
```css
color: #FFFFFF;
text-shadow: 0 1px 3px rgba(0, 0, 0, 0.3);
```

### On Glass
```css
color: rgba(0, 0, 0, 0.8);
text-shadow: 0 1px 3px rgba(255, 255, 255, 0.7);
```

---

## Common Mistakes & Fixes

### ❌ Buttons look flat
**Fix:** Add the 3-layer shadow system + glossy shine layer

### ❌ Colors look oversaturated
**Fix:** Use lighter tints - #87CEEB instead of pure #0000FF

### ❌ Highlights look harsh
**Fix:** Increase blur filter: `filter: blur(5px)` instead of 3px

### ❌ Light direction inconsistent
**Fix:** Always use 135° gradients, highlights always at top-left

### ❌ Looks too plasticky
**Fix:** Reduce shine opacity to 0.3-0.4 range, add subtle texture

### ❌ No depth feeling
**Fix:** Use drop shadow: `0 2px 4px rgba(0,0,0,0.2)` minimum

### ❌ Text hard to read on glass
**Fix:** Add text-shadow: `0 1px 3px rgba(255,255,255,0.7)`

---

## Quick Decision Tree

**Need a button?**
→ Use blue (#87CEEB/#0087BE) + 3-layer shadows + glossy shine

**Need a positive/success action?**
→ Use green (#90EE90/#228B22)

**Need something fresh/modern?**
→ Use teal (#40E0D0/#00A896)

**Need a special/premium element?**
→ Use aurora gradient + glass panel

**Need a background?**
→ Use off-white (#F5F5F5) or light gradient

**Need to show depth?**
→ Use drop shadow + inset shadows + highlight

**Need to show wetness?**
→ Use white glossy shine layer + multiple shadows

**Need glass effect?**
→ Use backdrop-filter: blur(10px) + semi-transparent background

---

## Minimum Viable Aero Button

Absolute bare minimum that still looks Aero:

```css
.button {
  background: linear-gradient(135deg, #87CEEB, #0087BE);
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.2);
  padding: 10px 20px;
  font-family: "Segoe UI", sans-serif;
}
```

**Enhanced (Recommended):**

```css
.button {
  background: linear-gradient(135deg, #87CEEB, #0087BE);
  border-radius: 12px;
  box-shadow:
    inset 0 1px 0 rgba(255,255,255,0.4),
    0 2px 4px rgba(0,0,0,0.2);
  padding: 10px 20px;
  font-family: "Segoe UI", "Frutiger", sans-serif;
  transition: all 0.3s cubic-bezier(0.25, 0.46, 0.45, 0.94);
  position: relative;
  overflow: hidden;
}

.button::before {
  content: '';
  position: absolute;
  top: 0;
  left: 20%;
  width: 25%;
  height: 50%;
  background: radial-gradient(ellipse, rgba(255,255,255,0.6), transparent);
  border-radius: 50%;
  filter: blur(3px);
}
```

---

## CSS Custom Properties Set

```css
:root {
  --aero-radius: 12px;
  --aero-easing: cubic-bezier(0.25, 0.46, 0.45, 0.94);
  --aero-shadow-drop: 0 2px 4px rgba(0,0,0,0.2);
  --aero-shadow-top: inset 0 1px 0 rgba(255,255,255,0.4);
  --aero-shadow-bottom: inset 0 -2px 0 rgba(0,0,0,0.1);

  --color-blue-light: #87CEEB;
  --color-blue-dark: #0087BE;
  --color-teal-light: #40E0D0;
  --color-teal-dark: #00A896;
  --color-green-light: #90EE90;
  --color-green-dark: #228B22;
}
```

Use with:
```css
.button {
  background: linear-gradient(135deg, var(--color-blue-light), var(--color-blue-dark));
  border-radius: var(--aero-radius);
  box-shadow: var(--aero-shadow-top), var(--aero-shadow-bottom), var(--aero-shadow-drop);
  transition: all 0.3s var(--aero-easing);
}
```

---

## Testing Checklist

- [ ] Buttons have visible white highlight at top-left
- [ ] Buttons have darker shading at bottom-right
- [ ] Colors are natural-looking (not neon)
- [ ] All corners are rounded (min 8px)
- [ ] Hover state is noticeably different
- [ ] Active state shows depression/pressed
- [ ] Text is readable on all backgrounds
- [ ] Transitions are smooth (0.3s)
- [ ] Light source is consistent across all elements
- [ ] Spacing is generous (not cramped)
- [ ] No harsh edges or sharp angles
- [ ] Accessibility: sufficient color contrast

---

That's everything you need. Copy, paste, customize, and build beautiful Aero interfaces!
