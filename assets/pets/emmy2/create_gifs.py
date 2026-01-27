"""Create animation GIFs for Emmy from extracted sprites.

=== SPRITE MAPPING (verified with VLM) ===

RECORD [0-3]: Dog spinning on vinyl record
  00: facing left on record
  01: sitting center on record
  02: facing right on record
  03: sitting back view on record

IDLE [5-7]: Dog sitting (blink/wag)
  05: sitting happy face
  06: sitting normal
  07: sitting slight variation

TOAST [8-11]: Dog eating toast/bread
  08: sniffing/approaching toast
  09: eating toast bent down
  10: holding toast walking
  11: holding toast sitting front

GRAMOPHONE [12-15]: Dog listening to gramophone
  12: ear up
  13: sitting back
  14: looking at gramophone
  15: sitting near

ROLLING [16-19]: Dog belly rub/rolling
  16: on back belly up
  17: rolling on side
  18: crawling/getting up
  19: on back legs up

BUTTON [20-23]: Dog pushing red button
  20: walking toward button
  21: sitting near button
  22: paw on button
  23: pressing button

BARK [24]: Dog barking
  24: mouth open barking

IDLE_EXTRA [25-27]: More sitting poses
  25: sitting side view
  26: sitting front calm
  27: sitting looking down
"""

from pathlib import Path
from PIL import Image

EMMY_DIR = Path(__file__).parent
PREFIX = "ThsS8zt4ct_"

# NEVER scale sprites - use UI scaling instead to preserve pixel art

# Animation groups
GROUPS = {
    'record':     [0, 1, 2, 3],
    'hover':      [5, 6, 7],       # Blink/tilt on mouse hover only
    'toast':      [8, 9, 10, 11],
    'gramophone': [12, 13, 14, 15],
    'rolling':    [16, 17, 18, 19],
    'button':     [20, 21, 22, 23],
    'bark':       [24, 24, 24, 24],  # Single frame repeated for timing
}

# Single frame for idle (still image)
SINGLE_FRAMES = {
    'idle': 6,  # Sitting normal - STILL, not animated
}

DURATIONS = {
    'record': 150,
    'hover': 400,  # Blink/tilt on hover
    'toast': 250,
    'gramophone': 200,
    'rolling': 200,
    'button': 200,
    'bark': 150,
}


def load_sprite(idx):
    path = EMMY_DIR / f"{PREFIX}{idx:05d}.png"
    return Image.open(path).convert("RGBA")


def create_gifs():
    # Create animated GIFs
    for name, indices in GROUPS.items():
        frames = [load_sprite(i) for i in indices]
        duration = DURATIONS.get(name, 200)

        gif_path = EMMY_DIR / f"{name}.gif"
        frames[0].save(
            gif_path,
            save_all=True,
            append_images=frames[1:],
            duration=duration,
            loop=0,
            disposal=2,
        )
        print(f"Created {gif_path}")

    # Create single-frame PNGs (idle is STILL, not animated)
    for name, idx in SINGLE_FRAMES.items():
        sprite = load_sprite(idx)
        png_path = EMMY_DIR / f"{name}.png"
        sprite.save(png_path)
        print(f"Created {png_path}")


if __name__ == "__main__":
    create_gifs()
    print("Done!")
