#!/usr/bin/env /opt/homebrew/opt/python@3.10/bin/python3.10
"""Download traffic light hover icons"""
import urllib.request
import os

ASSETS_DIR = "/opt/homebrew/lib/python3.10/site-packages/rp/git/voicething/assets"
BASE_URL = "https://api.iconify.design"

# Traffic light icons - need dark color for visibility on colored buttons
# Using a dark gray that works on red, yellow, and green backgrounds
ICONS = {
    "xmark": "heroicons:x-mark-20-solid.svg",
    "minus": "tabler/minus.svg",
    "expand": "bi/arrows-expand.svg",
}

# Dark color for visibility on bright backgrounds
PARAMS = "?color=%23333333&height=256"

for name, path in ICONS.items():
    url = f"{BASE_URL}/{path}{PARAMS}"
    output_path = os.path.join(ASSETS_DIR, f"{name}.svg")
    print(f"Downloading {name} from {url}")
    urllib.request.urlretrieve(url, output_path)
    print(f"  -> Saved to {output_path}")

print("\nDone!")
