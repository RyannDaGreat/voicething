"""Resize Emmy sprites to match LPC pet size (~32x32)."""
from pathlib import Path
from PIL import Image

EMMY_DIR = Path(__file__).parent
TARGET_SIZE = 32  # Match LPC pets

# Files to resize
FILES = [
    'idle.png',
    'hover.gif',
    'record.gif',
    'toast.gif',
    'gramophone.gif',
    'rolling.gif',
    'button.gif',
    'bark.gif',
]

def resize_image(img, target_size):
    """Resize image maintaining aspect ratio."""
    w, h = img.size
    scale = target_size / max(w, h)
    new_w = int(w * scale)
    new_h = int(h * scale)
    return img.resize((new_w, new_h), Image.Resampling.NEAREST)

def resize_gif(path, target_size):
    """Resize all frames of a GIF."""
    img = Image.open(path)
    frames = []
    durations = []

    try:
        while True:
            frame = img.copy().convert('RGBA')
            resized = resize_image(frame, target_size)
            frames.append(resized)
            durations.append(img.info.get('duration', 100))
            img.seek(img.tell() + 1)
    except EOFError:
        pass

    # Save resized GIF
    frames[0].save(
        path,
        save_all=True,
        append_images=frames[1:],
        duration=durations,
        loop=0,
        disposal=2,
    )
    print(f"Resized {path.name}: {frames[0].size}")

def resize_png(path, target_size):
    """Resize a PNG."""
    img = Image.open(path).convert('RGBA')
    resized = resize_image(img, target_size)
    resized.save(path)
    print(f"Resized {path.name}: {resized.size}")

for filename in FILES:
    path = EMMY_DIR / filename
    if not path.exists():
        print(f"Skipping {filename} (not found)")
        continue

    if filename.endswith('.gif'):
        resize_gif(path, TARGET_SIZE)
    else:
        resize_png(path, TARGET_SIZE)

print("Done!")
