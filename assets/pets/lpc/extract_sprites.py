"""Extract individual animation frames from LPC sprite sheet.

LPC Cats & Dogs sprite layout (512x256 for dog):
- 4 color variants horizontally (white, tan, golden, black)
- Each variant is 128x256
- Within each variant:
  - Row 0: Walking down (4 frames)
  - Row 1: Walking left (4 frames)
  - Row 2: Walking right (4 frames)
  - Row 3: Walking up (4 frames)
  - Row 4: Sleeping (2 frames) + Eating (2 frames)
  - Row 5: More poses
- Each frame is 32x32 pixels
"""

import os
from pathlib import Path
from PIL import Image

PETS_DIR = Path(__file__).parent


def extract_lpc_dog():
    """Extract dog animations from LPC sprite sheet."""
    img = Image.open(PETS_DIR / "lpc_dog.png")

    # 4 color variants, each 128px wide
    colors = ["white", "tan", "golden", "black"]
    variant_width = 128
    frame_size = 32

    for i, color in enumerate(colors):
        out_dir = PETS_DIR / f"lpc_dog_{color}"
        out_dir.mkdir(exist_ok=True)

        base_x = i * variant_width

        # Extract walking animations (rows 0-3, 4 frames each)
        directions = ["down", "left", "right", "up"]
        for row, direction in enumerate(directions):
            frames = []
            for col in range(4):
                x = base_x + col * frame_size
                y = row * frame_size
                frame = img.crop((x, y, x + frame_size, y + frame_size))
                frames.append(frame)

            # Save as animated GIF
            gif_path = out_dir / f"walk_{direction}.gif"
            frames[0].save(
                gif_path,
                save_all=True,
                append_images=frames[1:],
                duration=150,
                loop=0,
                disposal=2,
            )
            print(f"Created {gif_path}")

        # Extract sleeping (row 4, first 2 frames)
        sleep_frames = []
        for col in range(2):
            x = base_x + col * frame_size
            y = 4 * frame_size
            frame = img.crop((x, y, x + frame_size, y + frame_size))
            sleep_frames.append(frame)

        gif_path = out_dir / "sleep.gif"
        sleep_frames[0].save(
            gif_path,
            save_all=True,
            append_images=sleep_frames[1:],
            duration=500,
            loop=0,
            disposal=2,
        )
        print(f"Created {gif_path}")

        # Extract eating (row 4, frames 2-3)
        eat_frames = []
        for col in range(2, 4):
            x = base_x + col * frame_size
            y = 4 * frame_size
            frame = img.crop((x, y, x + frame_size, y + frame_size))
            eat_frames.append(frame)

        gif_path = out_dir / "eat.gif"
        eat_frames[0].save(
            gif_path,
            save_all=True,
            append_images=eat_frames[1:],
            duration=300,
            loop=0,
            disposal=2,
        )
        print(f"Created {gif_path}")

        # Create idle animation (use walk_down frame 0)
        idle_frame = img.crop((base_x, 0, base_x + frame_size, frame_size))
        idle_path = out_dir / "idle.png"
        idle_frame.save(idle_path)
        print(f"Created {idle_path}")


def extract_lpc_cat():
    """Extract cat animations from LPC sprite sheet."""
    img = Image.open(PETS_DIR / "lpc_cat.png")

    # 4 color variants
    colors = ["white", "orange", "gray", "black"]
    variant_width = 128
    frame_size = 32

    for i, color in enumerate(colors):
        out_dir = PETS_DIR / f"lpc_cat_{color}"
        out_dir.mkdir(exist_ok=True)

        base_x = i * variant_width

        # Extract walking animations
        directions = ["down", "left", "right", "up"]
        for row, direction in enumerate(directions):
            frames = []
            for col in range(4):
                x = base_x + col * frame_size
                y = row * frame_size
                frame = img.crop((x, y, x + frame_size, y + frame_size))
                frames.append(frame)

            gif_path = out_dir / f"walk_{direction}.gif"
            frames[0].save(
                gif_path,
                save_all=True,
                append_images=frames[1:],
                duration=150,
                loop=0,
                disposal=2,
            )
            print(f"Created {gif_path}")

        # Extract sleeping
        sleep_frames = []
        for col in range(2):
            x = base_x + col * frame_size
            y = 4 * frame_size
            frame = img.crop((x, y, x + frame_size, y + frame_size))
            sleep_frames.append(frame)

        gif_path = out_dir / "sleep.gif"
        sleep_frames[0].save(
            gif_path,
            save_all=True,
            append_images=sleep_frames[1:],
            duration=500,
            loop=0,
            disposal=2,
        )
        print(f"Created {gif_path}")

        # Extract eating
        eat_frames = []
        for col in range(2, 4):
            x = base_x + col * frame_size
            y = 4 * frame_size
            frame = img.crop((x, y, x + frame_size, y + frame_size))
            eat_frames.append(frame)

        gif_path = out_dir / "eat.gif"
        eat_frames[0].save(
            gif_path,
            save_all=True,
            append_images=eat_frames[1:],
            duration=300,
            loop=0,
            disposal=2,
        )
        print(f"Created {gif_path}")

        # Create idle
        idle_frame = img.crop((base_x, 0, base_x + frame_size, frame_size))
        idle_path = out_dir / "idle.png"
        idle_frame.save(idle_path)
        print(f"Created {idle_path}")


if __name__ == "__main__":
    print("Extracting LPC dog sprites...")
    extract_lpc_dog()
    print("\nExtracting LPC cat sprites...")
    extract_lpc_cat()
    print("\nDone!")
