#!/usr/bin/env /opt/homebrew/opt/python@3.10/bin/python3.10
"""Download additional icons from Iconify API"""
import os
import urllib.request

ASSETS_DIR = "/opt/homebrew/lib/python3.10/site-packages/rp/git/voicething/assets"
BASE_URL = "https://api.iconify.design"

ICONS = {
    "terminal": "tabler/terminal.svg",
    "scroll": "lucide/scroll.svg",
}

PARAMS = "?color=%23ffffff&height=256"

for name, path in ICONS.items():
    url = f"{BASE_URL}/{path}{PARAMS}"
    output_path = os.path.join(ASSETS_DIR, f"{name}.svg")
    print(f"Downloading {name} from {url}")
    urllib.request.urlretrieve(url, output_path)
    print(f"  -> Saved to {output_path}")

print("\nDone!")
