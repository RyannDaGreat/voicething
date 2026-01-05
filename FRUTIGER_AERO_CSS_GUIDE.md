# FRUTIGER AERO CSS IMPLEMENTATION GUIDE

## Ready-to-Use CSS Snippets & Techniques

---

## 1. THE GLOSSY BUTTON (Most Important Element)

### Basic Structure
```html
<button class="aero-button">Click Me</button>
```

### Complete CSS
```css
.aero-button {
  /* Structure */
  padding: 10px 20px;
  border: none;
  border-radius: 12px;
  cursor: pointer;
  position: relative;
  overflow: hidden;

  /* Base Color Gradient - Sky Blue to Darker Blue */
  background: linear-gradient(135deg, #87CEEB 0%, #0087BE 100%);

  /* Shadows & Depth */
  box-shadow:
    inset 0 1px 0 rgba(255, 255, 255, 0.4),  /* top highlight */
    inset 0 -2px 0 rgba(0, 0, 0, 0.1),       /* bottom shadow */
    0 2px 4px rgba(0, 0, 0, 0.2);            /* drop shadow */

  /* Typography */
  font-family: "Segoe UI", "Frutiger", "Helvetica Neue", sans-serif;
  font-size: 14px;
  font-weight: 500;
  color: #333;
  text-shadow: 0 1px 0 rgba(255, 255, 255, 0.5);

  /* Smooth Transitions */
  transition: all 0.3s cubic-bezier(0.25, 0.46, 0.45, 0.94);
}

/* Glossy Shine Overlay using ::before */
.aero-button::before {
  content: '';
  position: absolute;
  top: 0;
  left: 20%;
  width: 25%;
  height: 50%;
  background: radial-gradient(ellipse at center, rgba(255, 255, 255, 0.6), transparent);
  border-radius: 50%;
  filter: blur(3px);
  pointer-events: none;
}

/* Hover State - Brighter and More Prominent */
.aero-button:hover {
  background: linear-gradient(135deg, #99D9FF 0%, #0099D9 100%);
  box-shadow:
    inset 0 1px 0 rgba(255, 255, 255, 0.5),
    inset 0 -2px 0 rgba(0, 0, 0, 0.15),
    0 4px 8px rgba(0, 0, 0, 0.25);
}

.aero-button:hover::before {
  background: radial-gradient(ellipse at center, rgba(255, 255, 255, 0.8), transparent);
}

/* Active State - Pressed Down */
.aero-button:active {
  background: linear-gradient(135deg, #0087BE 0%, #005A8B 100%);
  box-shadow:
    inset 0 2px 4px rgba(0, 0, 0, 0.3),
    0 1px 2px rgba(0, 0, 0, 0.15);
}

.aero-button:active::before {
  background: radial-gradient(ellipse at center, rgba(255, 255, 255, 0.3), transparent);
}

/* Disabled State - Desaturated */
.aero-button:disabled {
  background: linear-gradient(135deg, #C0C0C0 0%, #808080 100%);
  opacity: 0.6;
  cursor: not-allowed;
}
```

---

## 2. ALTERNATIVE BUTTON COLORS (Nature Palette)

### Teal/Water Button
```css
.aero-button-teal {
  background: linear-gradient(135deg, #40E0D0 0%, #00A896 100%);
}

.aero-button-teal:hover {
  background: linear-gradient(135deg, #5FFFDD 0%, #00BBA6 100%);
}
```

### Green/Grass Button
```css
.aero-button-green {
  background: linear-gradient(135deg, #90EE90 0%, #228B22 100%);
}

.aero-button-green:hover {
  background: linear-gradient(135deg, #AAFFAA 0%, #2CB826 100%);
}
```

### Purple/Aurora Button
```css
.aero-button-purple {
  background: linear-gradient(135deg, #DDA0DD 0%, #9932CC 100%);
}

.aero-button-purple:hover {
  background: linear-gradient(135deg, #EEC0EE 0%, #BB3FDE 100%);
}
```

---

## 3. GLOSSY PANELS & CONTAINERS

### Glass Panel with Frost Effect
```css
.aero-panel {
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 12px;
  padding: 20px;

  box-shadow:
    inset 0 1px 0 rgba(255, 255, 255, 0.3),
    0 4px 8px rgba(0, 0, 0, 0.1);
}
```

### Solid Glossy Panel
```css
.aero-panel-solid {
  background: linear-gradient(135deg, #F5F5F5 0%, #E8E8E8 100%);
  border: 1px solid rgba(200, 200, 200, 0.5);
  border-radius: 12px;
  padding: 20px;

  box-shadow:
    inset 0 1px 0 rgba(255, 255, 255, 0.6),
    inset 0 -1px 0 rgba(0, 0, 0, 0.05),
    0 2px 4px rgba(0, 0, 0, 0.1);
}
```

### Colored Panel (Blue)
```css
.aero-panel-blue {
  background: linear-gradient(135deg, #E0F6FF 0%, #B3E5FC 100%);
  border: 1px solid rgba(0, 150, 200, 0.2);
  border-radius: 12px;
  padding: 20px;

  box-shadow:
    inset 0 1px 0 rgba(255, 255, 255, 0.5),
    0 2px 4px rgba(0, 0, 0, 0.08);
}
```

---

## 4. WATER DROPLETS & BUBBLES

### Bubble Element (3D Sphere)
```html
<div class="aero-bubble"></div>
```

```css
.aero-bubble {
  width: 80px;
  height: 80px;
  border-radius: 50%;

  /* Base color with inner shadow for 3D sphere effect */
  background: radial-gradient(circle at 35% 35%, rgba(255, 255, 255, 0.4), transparent),
              radial-gradient(circle, #87CEEB 0%, #0087BE 100%);

  /* Depth and shine */
  box-shadow:
    inset -10px -10px 20px rgba(0, 0, 0, 0.3),  /* inner shadow bottom */
    inset 5px 5px 10px rgba(255, 255, 255, 0.5), /* inner highlight top */
    0 10px 20px rgba(0, 0, 0, 0.2);              /* drop shadow */
}
```

### Multiple Bubble Cluster
```html
<div class="bubble-cluster">
  <div class="aero-bubble bubble-1"></div>
  <div class="aero-bubble bubble-2"></div>
  <div class="aero-bubble bubble-3"></div>
</div>
```

```css
.bubble-cluster {
  position: relative;
  width: 300px;
  height: 200px;
}

.bubble-cluster .aero-bubble {
  position: absolute;
  opacity: 0.7;
}

.bubble-cluster .bubble-1 {
  width: 100px;
  top: 10px;
  left: 20px;
}

.bubble-cluster .bubble-2 {
  width: 60px;
  top: 80px;
  left: 150px;
  opacity: 0.5;
}

.bubble-cluster .bubble-3 {
  width: 80px;
  bottom: 20px;
  right: 40px;
}
```

### Water Droplet
```html
<div class="aero-droplet"></div>
```

```css
.aero-droplet {
  width: 40px;
  height: 50px;
  background: radial-gradient(circle at 35% 30%, rgba(255, 255, 255, 0.6), transparent),
              radial-gradient(ellipse, #87CEEB 0%, #0087BE 100%);

  border-radius: 50% 50% 50% 0;
  transform: rotate(-45deg);

  box-shadow:
    inset -5px -8px 10px rgba(0, 0, 0, 0.2),
    0 5px 10px rgba(0, 0, 0, 0.15);
}
```

---

## 5. AURORA GRADIENT BACKGROUND

### Aurora Effect (for backgrounds or panels)
```css
.aero-aurora {
  background:
    linear-gradient(135deg,
      #FFB6C1 0%,      /* Pink */
      #DDA0DD 30%,     /* Purple */
      #B19CD9 60%,     /* Lavender */
      #87CEEB 100%     /* Sky Blue */
    );

  /* Optional: Add soft blur for ethereal effect */
  filter: blur(1px);
}
```

### Aurora with Multiple Layers
```css
.aero-aurora-layered {
  background:
    linear-gradient(135deg, rgba(255, 182, 193, 0.3) 0%, transparent 50%),
    linear-gradient(225deg, rgba(221, 160, 221, 0.3) 0%, transparent 50%),
    linear-gradient(90deg, #87CEEB 0%, #00CED1 100%);

  position: relative;
}

.aero-aurora-layered::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: radial-gradient(ellipse at center, rgba(255, 255, 255, 0.1), transparent);
}
```

---

## 6. GLOSSY TEXT EFFECTS

### Text with Glow
```css
.aero-text-glow {
  font-family: "Segoe UI", "Frutiger", "Helvetica Neue", sans-serif;
  font-size: 24px;
  font-weight: 500;
  color: #0066CC;

  text-shadow:
    0 1px 0 rgba(255, 255, 255, 0.8),  /* highlight */
    0 2px 4px rgba(0, 0, 0, 0.2);       /* shadow */
}
```

### Text on Glass Background
```css
.aero-text-on-glass {
  font-family: "Segoe UI", "Frutiger", "Helvetica Neue", sans-serif;
  color: rgba(0, 0, 0, 0.8);

  text-shadow:
    0 1px 3px rgba(255, 255, 255, 0.7);  /* bright shadow for readability */
}
```

### Heading with Shine
```css
.aero-heading {
  font-family: "Segoe UI", "Frutiger", "Helvetica Neue", sans-serif;
  font-size: 32px;
  font-weight: 300;
  color: #0087BE;

  background: linear-gradient(135deg, #0087BE 0%, #0066CC 50%, #0087BE 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;

  text-shadow: none; /* gradient text doesn't work with text-shadow */
}
```

---

## 7. INTERACTIVE ELEMENTS

### Hover Glow Effect
```css
.aero-element {
  transition: all 0.3s cubic-bezier(0.25, 0.46, 0.45, 0.94);
}

.aero-element:hover {
  box-shadow:
    inset 0 1px 0 rgba(255, 255, 255, 0.4),
    0 6px 12px rgba(0, 150, 200, 0.3);  /* colored glow */

  filter: brightness(1.1);
}
```

### Floating Animation
```css
@keyframes aero-float {
  0%, 100% {
    transform: translateY(0px);
  }
  50% {
    transform: translateY(-3px);
  }
}

.aero-floating {
  animation: aero-float 3s cubic-bezier(0.25, 0.46, 0.45, 0.94) infinite;
}
```

### Pulse Glow
```css
@keyframes aero-pulse-glow {
  0%, 100% {
    box-shadow: 0 0 0 0 rgba(0, 150, 200, 0.3);
  }
  50% {
    box-shadow: 0 0 0 8px rgba(0, 150, 200, 0);
  }
}

.aero-pulse {
  animation: aero-pulse-glow 2s cubic-bezier(0.25, 0.46, 0.45, 0.94) infinite;
}
```

---

## 8. ROUNDED FORM ELEMENTS

### Input Field
```css
.aero-input {
  padding: 10px 12px;
  border: 1px solid rgba(0, 150, 200, 0.3);
  border-radius: 8px;
  background: rgba(255, 255, 255, 0.9);

  font-family: "Segoe UI", "Frutiger", "Helvetica Neue", sans-serif;
  font-size: 14px;
  color: #333;

  box-shadow: inset 0 1px 3px rgba(0, 0, 0, 0.05);

  transition: all 0.3s cubic-bezier(0.25, 0.46, 0.45, 0.94);
}

.aero-input:focus {
  outline: none;
  border-color: #0087BE;
  background: #FFFFFF;
  box-shadow:
    inset 0 1px 3px rgba(0, 0, 0, 0.05),
    0 0 8px rgba(0, 135, 190, 0.3);
}
```

### Checkbox
```css
.aero-checkbox {
  width: 18px;
  height: 18px;
  appearance: none;
  background: linear-gradient(135deg, #FFFFFF 0%, #E8E8E8 100%);
  border: 1px solid rgba(0, 0, 0, 0.2);
  border-radius: 3px;
  cursor: pointer;

  box-shadow:
    inset 0 1px 0 rgba(255, 255, 255, 0.5),
    0 1px 2px rgba(0, 0, 0, 0.1);

  transition: all 0.2s cubic-bezier(0.25, 0.46, 0.45, 0.94);
}

.aero-checkbox:checked {
  background: linear-gradient(135deg, #87CEEB 0%, #0087BE 100%);
  border-color: #0066CC;
}

.aero-checkbox:checked::after {
  content: '✓';
  display: block;
  color: white;
  text-align: center;
  line-height: 18px;
  font-size: 12px;
  font-weight: bold;
}
```

---

## 9. COMPLETE PAGE EXAMPLE

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Frutiger Aero Aesthetic</title>
  <style>
    * {
      margin: 0;
      padding: 0;
      box-sizing: border-box;
    }

    body {
      font-family: "Segoe UI", "Frutiger", "Helvetica Neue", sans-serif;
      background: linear-gradient(135deg, #FFFFFF 0%, #F0F8FF 100%);
      color: #333;
      padding: 40px 20px;
      min-height: 100vh;
    }

    .container {
      max-width: 800px;
      margin: 0 auto;
    }

    h1 {
      color: #0087BE;
      font-size: 36px;
      margin-bottom: 10px;
      text-shadow: 0 1px 0 rgba(255, 255, 255, 0.8);
    }

    .intro-panel {
      background: linear-gradient(135deg, #E0F6FF 0%, #B3E5FC 100%);
      border: 1px solid rgba(0, 150, 200, 0.2);
      border-radius: 12px;
      padding: 24px;
      margin-bottom: 30px;

      box-shadow:
        inset 0 1px 0 rgba(255, 255, 255, 0.5),
        0 2px 4px rgba(0, 0, 0, 0.08);
    }

    .button-group {
      display: flex;
      gap: 12px;
      margin-top: 24px;
    }

    .aero-button {
      /* (use the CSS from section 1 above) */
    }

    .bubble-decoration {
      width: 100px;
      height: 100px;
      border-radius: 50%;
      background: radial-gradient(circle at 35% 35%, rgba(255, 255, 255, 0.4), transparent),
                  radial-gradient(circle, #87CEEB 0%, #0087BE 100%);

      box-shadow:
        inset -10px -10px 20px rgba(0, 0, 0, 0.3),
        inset 5px 5px 10px rgba(255, 255, 255, 0.5),
        0 10px 20px rgba(0, 0, 0, 0.2);

      margin: 30px auto;
      animation: aero-float 3s cubic-bezier(0.25, 0.46, 0.45, 0.94) infinite;
    }
  </style>
</head>
<body>
  <div class="container">
    <h1>Frutiger Aero Design</h1>

    <div class="intro-panel">
      <p>Experience authentic 2000s technology aesthetic with glossy buttons, nature-inspired colors, and that distinctive "wet" appearance.</p>

      <div class="button-group">
        <button class="aero-button">Primary Action</button>
        <button class="aero-button">Secondary</button>
      </div>
    </div>

    <div class="bubble-decoration"></div>
  </div>
</body>
</html>
```

---

## 10. COLOR PALETTE QUICK REFERENCE

```css
:root {
  /* Sky Blues */
  --sky-light: #87CEEB;
  --sky-medium: #00B8E6;
  --sky-dark: #0087BE;

  /* Water Teals */
  --water-light: #40E0D0;
  --water-medium: #00CED1;
  --water-dark: #00A896;

  /* Grass Greens */
  --grass-light: #90EE90;
  --grass-medium: #228B22;
  --grass-dark: #1a6b1a;

  /* Aurora Purples */
  --aurora-pink: #FFB6C1;
  --aurora-purple: #DDA0DD;
  --aurora-lavender: #B19CD9;

  /* Neutrals */
  --white: #FFFFFF;
  --off-white: #F5F5F5;
  --light-gray: #E8E8E8;
  --medium-gray: #D3D3D3;
  --silver: #C0C0C0;
}
```

---

## IMPLEMENTATION NOTES

1. **Light Source Direction**: Always from top-left (135-degree angle)
2. **Rounded Corners**: Use 8-12px for UI elements, 50% for circles
3. **Shadows**: Multiple layers (inset highlight + inset shadow + drop shadow)
4. **Transitions**: Use `cubic-bezier(0.25, 0.46, 0.45, 0.94)` for natural feel
5. **Opacity**: Highlights at 20-40%, shadows at 10-20%
6. **Filters**: Blur 3-5px for shine, 10px for glass effect
7. **Colors**: Desaturated naturals, not Web 2.0 bright

All snippets are production-ready and can be directly applied to your project.
