"""Extract Emmy sprites from the spritesheet.

=== EMMY SPRITE SHEET (429x320) - VERIFIED GROUPINGS ===

Row 1: RECORD (4) + DISCARD (2)
  0-3: Dog spinning on vinyl record (animation frames)
  4-5: Standing poses - DISCARDED

Row 2: IDLE (2) + TOAST (4)
  6: Dog sitting normally - IDLE frame 1
  7: Dog sitting happy - IDLE frame 2
  8: Dog sniffing toast - TOAST frame 1
  9: Dog eating toast bent down - TOAST frame 2
  10: Dog walking away from toast - TOAST frame 3
  11: Dog holding toast in mouth - TOAST frame 4

Row 3: GRAMOPHONE (4) + ROLLING (2)
  12-15: Dog with gramophone, ear flapping animation
  16-17: Dog rolling/lying frames 1-2

Row 4: ROLLING (2) + BUTTON (4)
  18-19: Dog rolling frames 3-4
  20-23: Dog pushing red button animation

Row 5: BARK (4) + IDLE (1)
  24: Dog barking frame 1 (mouth open)
  25: Dog sitting calm - IDLE frame 3
  26: Dog barking frame 2
  27: Dog barking frame 3
  28: Dog barking frame 4

=== ANIMATION GROUPS (VERIFIED) ===

RECORD:     [0, 1, 2, 3]      - Dog spinning on vinyl (4 frames)
TOAST:      [8, 9, 10, 11]    - Dog eating toast (4 frames)
GRAMOPHONE: [12, 13, 14, 15]  - Dog listening, ear flap (4 frames)
ROLLING:    [16, 17, 18, 19]  - Dog belly rub/rolling (4 frames)
BUTTON:     [20, 21, 22, 23]  - Dog pushing red button (4 frames)
IDLE:       [6, 7, 25]        - Dog sitting, blink/wag (3 frames)
BARK:       [24, 26, 27, 28]  - Dog barking (4 frames)
DISCARD:    [4, 5]            - Not used

=== BEHAVIOR RULES ===

IDLE STATE:
  - Default: IDLE[0] (sprite 6, sitting normally)
  - Occasionally: blink/wag using IDLE[1] (sprite 7) or IDLE[2] (sprite 25)
  - Animation is infrequent - mostly static

CLICKED (50/50 chance):
  - Option A: Belly rub roll (ROLLING animation)
  - Option B: Fed bread (TOAST animation)

RECORDING START (50/50 chance):
  - Option A: Spin on record (RECORD loop)
  - Option B: Listen to gramophone (GRAMOPHONE loop)

PROCESSING:
  - Spin on record (RECORD continuous loop)

DONE/COMPLETE (50/50 chance):
  - Option A: Bark (BARK animation, play once)
  - Option B: Push red button (BUTTON animation, play once)
"""

from pathlib import Path
from PIL import Image

ASSETS_DIR = Path(__file__).parent.parent.parent  # assets/
EMMY_SHEET = ASSETS_DIR / "emmy_sprites.png"
OUT_DIR = Path(__file__).parent  # assets/pets/emmy/

# Sprite bounding boxes (x, y, w, h) - manually verified
SPRITES = {
    # Row 1 - RECORD + DISCARD
    0: (0, 0, 70, 65),
    1: (70, 0, 70, 65),
    2: (140, 0, 70, 65),
    3: (210, 0, 65, 65),
    4: (275, 0, 65, 65),
    5: (350, 0, 60, 65),

    # Row 2 - IDLE + TOAST
    6: (0, 65, 55, 65),
    7: (55, 65, 70, 65),
    8: (125, 65, 75, 65),
    9: (200, 65, 65, 65),
    10: (265, 65, 60, 65),
    11: (325, 65, 75, 65),

    # Row 3 - GRAMOPHONE + ROLLING
    12: (0, 130, 80, 65),
    13: (80, 130, 75, 65),
    14: (155, 130, 75, 65),
    15: (230, 130, 70, 65),
    16: (300, 130, 65, 65),
    17: (365, 130, 64, 65),

    # Row 4 - ROLLING + BUTTON
    18: (0, 195, 60, 65),
    19: (60, 195, 60, 65),
    20: (120, 195, 70, 70),
    21: (190, 195, 70, 70),
    22: (260, 195, 75, 70),
    23: (335, 195, 80, 70),

    # Row 5 - BARK + IDLE
    24: (0, 260, 60, 60),
    25: (60, 260, 55, 60),
    26: (115, 260, 60, 60),
    27: (175, 260, 65, 60),
    28: (240, 260, 80, 60),
}

# Animation groups - VERIFIED
GROUPS = {
    'record':     [0, 1, 2, 3],
    'toast':      [8, 9, 10, 11],
    'gramophone': [12, 13, 14, 15],
    'rolling':    [16, 17, 18, 19],
    'button':     [20, 21, 22, 23],
    'idle':       [6, 7, 25],
    'bark':       [24, 26, 27, 28],
}

DISCARD = [4, 5]


def extract_sprites():
    """Extract individual sprites from the sheet."""
    img = Image.open(EMMY_SHEET).convert("RGBA")
    OUT_DIR.mkdir(exist_ok=True)

    for idx, (x, y, w, h) in SPRITES.items():
        if idx in DISCARD:
            continue
        x2 = min(x + w, img.width)
        y2 = min(y + h, img.height)
        sprite = img.crop((x, y, x2, y2))
        sprite.save(OUT_DIR / f"sprite_{idx:02d}.png")
        print(f"Extracted sprite_{idx:02d}.png")


def create_animation_gifs():
    """Create animated GIFs for each animation group."""
    for name, indices in GROUPS.items():
        frames = []
        for idx in indices:
            path = OUT_DIR / f"sprite_{idx:02d}.png"
            if path.exists():
                frames.append(Image.open(path))

        if not frames:
            continue

        # Determine duration based on animation type
        if name == 'idle':
            duration = 500  # Slow blink/wag
        elif name in ('record', 'gramophone'):
            duration = 150  # Medium speed loop
        else:
            duration = 200  # Standard animation

        gif_path = OUT_DIR / f"{name}.gif"
        frames[0].save(
            gif_path,
            save_all=True,
            append_images=frames[1:],
            duration=duration,
            loop=0,
            disposal=2,
        )
        print(f"Created {gif_path}")


if __name__ == "__main__":
    print("Extracting Emmy sprites...")
    extract_sprites()
    print("\nCreating animation GIFs...")
    create_animation_gifs()
    print("\nDone!")
