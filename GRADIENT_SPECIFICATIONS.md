# Windows Aero Gradient Specifications - Complete Reference

Precise gradient definitions for recreating authentic Aero UI components.

## Gradient Definition Format

All gradients defined in multiple formats:
- **CSS**: For Qt stylesheets (qlineargradient syntax)
- **Python**: For QLinearGradient/QRadialGradient
- **Hex/RGB**: Color values for reference

---

## COMPONENT GRADIENTS

### 1. VISTA GLASS PANEL (Default Gray)

**CSS Stylesheet:**
```css
background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
    stop: 0.0 #B5B9BC,
    stop: 0.2 #F0F0F0,
    stop: 0.5 #D8D8D8,
    stop: 1.0 #D3D3D3);
```

**Python Code:**
```python
gradient = QLinearGradient(QPointF(0, 0), QPointF(0, height))
gradient.setColorAt(0.0, QColor(181, 185, 188))   # #B5B9BC
gradient.setColorAt(0.2, QColor(240, 240, 240))   # #F0F0F0
gradient.setColorAt(0.5, QColor(216, 216, 216))   # #D8D8D8
gradient.setColorAt(1.0, QColor(211, 211, 211))   # #D3D3D3
```

**Color Breakdown:**
| Stop | Hex     | RGB             | Purpose             |
|------|---------|-----------------|---------------------|
| 0.0% | #B5B9BC | rgb(181,185,188)| Highlight/top edge  |
| 20%  | #F0F0F0 | rgb(240,240,240)| Bright upper zone   |
| 50%  | #D8D8D8 | rgb(216,216,216)| Mid-tone transition |
| 100% | #D3D3D3 | rgb(211,211,211)| Shadow/bottom edge  |

---

### 2. GLOSSY BUTTON (Gray Aero)

**CSS Stylesheet:**
```css
background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
    stop: 0 #FFFFFF,
    stop: 0.4 #F0F0F0,
    stop: 0.5 #E0E0E0,
    stop: 1.0 #D0D0D0);
border: 1px solid #888888;
border-top: 1px solid rgba(255, 255, 255, 0.8);
border-radius: 4px;
padding: 5px 15px;
```

**Python Code:**
```python
gradient = QLinearGradient(QPointF(0, 0), QPointF(0, height))
gradient.setColorAt(0.0, QColor(255, 255, 255))   # #FFFFFF
gradient.setColorAt(0.4, QColor(240, 240, 240))   # #F0F0F0
gradient.setColorAt(0.5, QColor(224, 224, 224))   # #E0E0E0
gradient.setColorAt(1.0, QColor(208, 208, 208))   # #D0D0D0
```

**Color Breakdown:**
| Stop | Hex     | RGB             | Purpose              |
|------|---------|-----------------|----------------------|
| 0%   | #FFFFFF | rgb(255,255,255)| Bright top shine     |
| 40%  | #F0F0F0 | rgb(240,240,240)| Upper gradient zone  |
| 50%  | #E0E0E0 | rgb(224,224,224)| Center transition    |
| 100% | #D0D0D0 | rgb(208,208,208)| Bottom shadow        |

**With Inner Glow:**
```
border-top: 1px solid rgba(255, 255, 255, 204);  /* 80% opaque white */
border-left: 1px solid rgba(255, 255, 255, 102); /* 40% opaque white */
```

---

### 3. BLUE AERO BUTTON (Primary Theme)

**CSS Stylesheet:**
```css
background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
    stop: 0 #FFFFFF,
    stop: 0.3 #C9EBF5,
    stop: 0.7 #0689E4,
    stop: 1.0 #003C78);
border: 1px solid #0050A0;
border-top: 1px solid rgba(255, 255, 255, 0.8);
border-radius: 5px;
padding: 6px 16px;
color: #FFFFFF;
```

**Python Code:**
```python
gradient = QLinearGradient(QPointF(0, 0), QPointF(0, height))
gradient.setColorAt(0.0, QColor(255, 255, 255))   # #FFFFFF
gradient.setColorAt(0.3, QColor(201, 235, 245))   # #C9EBF5
gradient.setColorAt(0.7, QColor(6, 137, 228))     # #0689E4
gradient.setColorAt(1.0, QColor(0, 60, 120))      # #003C78
```

**Color Breakdown:**
| Stop | Hex     | RGB             | Purpose           |
|------|---------|-----------------|-------------------|
| 0%   | #FFFFFF | rgb(255,255,255)| White top shine   |
| 30%  | #C9EBF5 | rgb(201,235,245)| Light cyan zone   |
| 70%  | #0689E4 | rgb(6,137,228)  | Primary Aero blue |
| 100% | #003C78 | rgb(0,60,120)   | Dark Aero blue    |

---

### 4. BLUE AERO BUTTON - HOVER STATE

**CSS Stylesheet:**
```css
background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
    stop: 0 #FFFACD,
    stop: 0.3 #D4F1FF,
    stop: 0.7 #1299CA,
    stop: 1.0 #004A8C);
```

**Python Code:**
```python
gradient = QLinearGradient(QPointF(0, 0), QPointF(0, height))
gradient.setColorAt(0.0, QColor(255, 250, 205))   # #FFFACD - warmer
gradient.setColorAt(0.3, QColor(212, 241, 255))   # #D4F1FF - brighter
gradient.setColorAt(0.7, QColor(18, 153, 202))    # #1299CA - lighter
gradient.setColorAt(1.0, QColor(0, 74, 140))      # #004A8C - lighter dark
```

**Key Differences from Normal:**
- Top: Warmer (#FFFACD vs #FFFFFF)
- Mid: Brighter cyan (#D4F1FF vs #C9EBF5)
- Main: Lighter blue (#1299CA vs #0689E4)
- Bottom: Lighter dark (#004A8C vs #003C78)

---

### 5. BLUE AERO BUTTON - PRESSED STATE (Inverted)

**CSS Stylesheet:**
```css
background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
    stop: 0 #D8D8D8,
    stop: 0.5 #0050A0,
    stop: 1.0 #FFFFFF);
border: 1px solid #003C78;
```

**Python Code:**
```python
gradient = QLinearGradient(QPointF(0, 0), QPointF(0, height))
gradient.setColorAt(0.0, QColor(216, 216, 216))   # #D8D8D8 - gray top
gradient.setColorAt(0.5, QColor(0, 80, 160))      # #0050A0 - dark mid
gradient.setColorAt(1.0, QColor(255, 255, 255))   # #FFFFFF - bright bottom
```

**Key Difference:**
Gradient is inverted (dark top, bright bottom) to create pressed/inset effect.

---

### 6. SCROLLBAR HANDLE (Glossy Gray)

**CSS Stylesheet:**
```css
background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
    stop: 0 #CCCCCC,
    stop: 0.5 #AAAAAA,
    stop: 1.0 #888888);
border: 1px solid #666666;
border-radius: 5px;
```

**Python Code:**
```python
# Note: For scrollbar, gradient direction differs (x-axis for vertical bar)
gradient = QLinearGradient(QPointF(0, 0), QPointF(width, 0))
gradient.setColorAt(0.0, QColor(204, 204, 204))   # #CCCCCC
gradient.setColorAt(0.5, QColor(170, 170, 170))   # #AAAAAA
gradient.setColorAt(1.0, QColor(136, 136, 136))   # #888888
```

**Color Breakdown:**
| Stop | Hex     | RGB             | Purpose      |
|------|---------|-----------------|--------------|
| 0%   | #CCCCCC | rgb(204,204,204)| Left highlight |
| 50%  | #AAAAAA | rgb(170,170,170)| Mid-tone     |
| 100% | #888888 | rgb(136,136,136)| Right shadow |

---

### 7. SCROLLBAR HANDLE - HOVER STATE

**CSS Stylesheet:**
```css
background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
    stop: 0 #DDDDDD,
    stop: 0.5 #BBBBBB,
    stop: 1.0 #999999);
```

**Python Code:**
```python
gradient = QLinearGradient(QPointF(0, 0), QPointF(width, 0))
gradient.setColorAt(0.0, QColor(221, 221, 221))   # #DDDDDD
gradient.setColorAt(0.5, QColor(187, 187, 187))   # #BBBBBB
gradient.setColorAt(1.0, QColor(153, 153, 153))   # #999999
```

**Pattern:** All values lightened by +17 from normal state.

---

### 8. SCROLLBAR HANDLE - PRESSED STATE

**CSS Stylesheet:**
```css
background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
    stop: 0 #999999,
    stop: 0.5 #777777,
    stop: 1.0 #555555);
```

**Python Code:**
```python
gradient = QLinearGradient(QPointF(0, 0), QPointF(width, 0))
gradient.setColorAt(0.0, QColor(153, 153, 153))   # #999999
gradient.setColorAt(0.5, QColor(119, 119, 119))   # #777777
gradient.setColorAt(1.0, QColor(85, 85, 85))      # #555555
```

**Pattern:** All values darkened by -51 from normal state.

---

### 9. ORB BUTTON (Blue Sphere - Radial)

**Python Code (QRadialGradient):**
```python
# Focal point at 40% from top-left for 3D sphere effect
rad_grad = QRadialGradient(
    QPointF(width * 0.4, height * 0.4),  # Focal point
    max(width, height) / 2                # Radius to edge
)

# Color stops (center white → edge dark blue)
rad_grad.setColorAt(0.0, QColor(255, 255, 255))   # #FFFFFF
rad_grad.setColorAt(0.2, QColor(200, 230, 255))   # #C8E6FF
rad_grad.setColorAt(0.4, QColor(100, 200, 255))   # #64C8FF
rad_grad.setColorAt(0.6, QColor(50, 150, 200))    # #3296C8
rad_grad.setColorAt(0.8, QColor(20, 100, 150))    # #146496
rad_grad.setColorAt(1.0, QColor(5, 40, 80))       # #0A2850
```

**Color Breakdown:**
| Stop | Hex     | RGB             | Purpose          |
|------|---------|-----------------|------------------|
| 0%   | #FFFFFF | rgb(255,255,255)| Bright center    |
| 20%  | #C8E6FF | rgb(200,230,255)| Pale blue zone   |
| 40%  | #64C8FF | rgb(100,200,255)| Light blue       |
| 60%  | #3296C8 | rgb(50,150,200) | Medium blue      |
| 80%  | #146496 | rgb(20,100,150) | Dark blue        |
| 100% | #0A2850 | rgb(5,40,80)    | Very dark edge   |

**Critical Settings:**
- Focal point: (0.4 * width, 0.4 * height) ← Creates top-left highlight
- Radius: max(width, height) / 2
- Minimum 6 stops for smooth sphere appearance

---

## TRANSPARENCY SPECIFICATIONS

### Glass Panel RGBA

**Background:**
```
rgba(200, 220, 240, 191)  /* 75% opaque light blue */
or equivalently:
rgba(200, 220, 240, 75%)
```

**Border:**
```
rgba(173, 216, 230, 100)   /* 40% opaque cyan */
or equivalently:
rgba(173, 216, 230, 40%)
```

**Inner Border (Top Glow):**
```
rgba(255, 255, 255, 204)   /* 80% opaque white */
or equivalently:
rgba(255, 255, 255, 0.8)
```

### Alpha Value Chart

| Decimal | Percent | Effect               |
|---------|---------|----------------------|
| 255     | 100%    | Fully opaque         |
| 204     | 80%     | Strong glow/highlight|
| 191     | 75%     | Light transparency   |
| 127     | 50%     | Moderate transparent |
| 102     | 40%     | Subtle border        |
| 64      | 25%     | Highly transparent   |
| 1       | 0.4%    | Nearly transparent   |

---

## BORDER STYLING REFERENCE

### Inset/Outset Beveled Effect

**Raised (Outset):**
```css
border: 2px outset #CCCCCC;
border-top-color: #FFFFFF;     /* Lighter on top */
border-left-color: #FFFFFF;
border-bottom-color: #808080;  /* Darker on bottom */
border-right-color: #808080;
```

**Pressed (Inset):**
```css
border: 2px inset #999999;
border-top-color: #808080;     /* Darker on top (reversed) */
border-left-color: #808080;
border-bottom-color: #FFFFFF;  /* Lighter on bottom */
border-right-color: #FFFFFF;
```

### Complete Glossy Button with Borders

```css
QPushButton {
    background: qlineargradient(...);
    border: 1px solid #888888;           /* Outer dark edge */
    border-top: 1px solid rgba(255, 255, 255, 0.8);  /* Inner glow */
    border-radius: 4px;
}
```

---

## COMPLETE COMPONENT STYLESHEET TEMPLATE

```css
/* GLASS PANELS */
.glass-panel {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
        stop: 0.0 #B5B9BC,
        stop: 0.2 #F0F0F0,
        stop: 0.5 #D8D8D8,
        stop: 1.0 #D3D3D3);
    border: 1px solid #888888;
    border-radius: 4px;
}

/* GLOSSY BUTTONS - GRAY */
.button-gray {
    background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
        stop: 0 #FFFFFF,
        stop: 0.4 #F0F0F0,
        stop: 0.5 #E0E0E0,
        stop: 1.0 #D0D0D0);
    border: 1px solid #888888;
    border-top: 1px solid rgba(255, 255, 255, 0.8);
}

.button-gray:hover {
    background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
        stop: 0 #FFFACD,
        stop: 0.4 #F5F5F0,
        stop: 0.5 #E8E8DC,
        stop: 1.0 #D8D8C8);
}

.button-gray:pressed {
    background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
        stop: 0 #D8D8D8,
        stop: 0.5 #B0B0B0,
        stop: 1.0 #FFFFFF);
}

/* GLOSSY BUTTONS - BLUE AERO */
.button-aero {
    background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
        stop: 0 #FFFFFF,
        stop: 0.3 #C9EBF5,
        stop: 0.7 #0689E4,
        stop: 1.0 #003C78);
    border: 1px solid #0050A0;
    border-top: 1px solid rgba(255, 255, 255, 0.8);
}

.button-aero:hover {
    background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
        stop: 0 #FFFACD,
        stop: 0.3 #D4F1FF,
        stop: 0.7 #1299CA,
        stop: 1.0 #004A8C);
}

.button-aero:pressed {
    background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
        stop: 0 #D8D8D8,
        stop: 0.5 #0050A0,
        stop: 1.0 #FFFFFF);
}

/* SCROLLBARS */
QScrollBar:vertical {
    background: #F0F0F0;
    width: 12px;
}

QScrollBar::handle:vertical {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
        stop: 0 #CCCCCC,
        stop: 0.5 #AAAAAA,
        stop: 1.0 #888888);
    border: 1px solid #666666;
    border-radius: 5px;
    min-height: 20px;
}

QScrollBar::handle:vertical:hover {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
        stop: 0 #DDDDDD,
        stop: 0.5 #BBBBBB,
        stop: 1.0 #999999);
}
```

---

## DEBUGGING GRADIENT ISSUES

**Glossy effect looks flat:**
- Verify you have 4+ gradient stops
- Ensure top stop is light (#FFFFFF or #FFFACD)
- Check gradient direction: y1:0 → y2:1 for vertical

**Colors don't match reference:**
- Verify exact hex values (copy-paste carefully)
- Check for typos in rgb() values
- Test on target platform (colors vary by monitor)

**Border doesn't show:**
- Minimum 1px visible (2px recommended)
- Use high-contrast colors
- Ensure border-radius < half the width

**Transparency not working:**
- Use rgba() format, not rgb()
- Set alpha value 0-255 or 0-100%
- Enable WA_TranslucentBackground attribute

---

## TESTING CHECKLIST

- [ ] All gradient stops render smoothly (no banding)
- [ ] Top highlight appears glossy (bright white visible)
- [ ] Hover state is noticeably different
- [ ] Pressed state inverts gradient
- [ ] Borders render at correct width
- [ ] Scrollbar handles have proper radius (< W/2)
- [ ] Orb buttons appear spherical (3D effect)
- [ ] Transparency shows background clearly
- [ ] Inner glow (top border) visible and subtle

---

