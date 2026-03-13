"""Test that the refactored _get_menubar_icon produces valid icons."""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# /// script
# requires-python = ">=3.10"
# dependencies = ["PyQt6"]
# ///

from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QPixmap

app = QApplication(sys.argv)

from voice_thing import _get_menubar_icon

# Test template icon (hue=None)
icon = _get_menubar_icon(hue=None)
sizes = icon.availableSizes()
assert len(sizes) > 0, "Template icon has no sizes"
print(f"Template icon: {sizes[0].width()}x{sizes[0].height()}")

# Test hue icons at several angles
for hue in [0, 60, 120, 180, 240, 300]:
    icon = _get_menubar_icon(hue=hue)
    sizes = icon.availableSizes()
    assert len(sizes) > 0, f"Hue {hue} icon has no sizes"
    # Check it's not empty
    pixmap = icon.pixmap(sizes[0])
    assert not pixmap.isNull(), f"Hue {hue} pixmap is null"
    print(f"Hue {hue}: {sizes[0].width()}x{sizes[0].height()} OK")

# Test rapid cycling (mimics tray_icon_timer at 20 FPS)
import time
t0 = time.time()
for i in range(200):
    hue = (i * 2) % 360
    icon = _get_menubar_icon(hue=hue)
elapsed = time.time() - t0
print(f"200 icon cycles in {elapsed:.3f}s ({elapsed/200*1000:.1f}ms/icon)")

print("\nAll menubar icon tests passed.")
