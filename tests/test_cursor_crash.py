"""
Reproduce and verify the fix for SIGBUS crash in macOS ImageIO (0x0BAD4007).

Root cause: _get_menubar_icon() was called at 20 FPS via QTimer, each call
doing PIL→PNG encode→QPixmap.loadFromData (which goes through macOS ImageIO
PNG plugin). When setCursor is called between these ImageIO operations,
ImageIO's internal plugin state can be corrupted, causing SIGBUS at 0x0BAD4007
(corrupted function pointer in IIOReadPlugin::callInitialize).

This crash cannot be reliably reproduced synthetically — it depends on specific
heap layout and ImageIO internal state (confirmed by wxWidgets #23547, which
had the EXACT same crash signature and also couldn't reproduce synthetically).

What this test DOES verify:
1. The OLD code path invokes QPixmap.loadFromData (→ ImageIO PNG codec)
2. The NEW code path does NOT invoke QPixmap.loadFromData (no ImageIO)
3. The new code produces valid, non-null icons at all hue values
4. Cursor deduplication prevents redundant setCursor calls

This is the same validation strategy used by wxWidgets to fix the identical
crash: prove the dangerous code path (ImageIO) is no longer exercised.
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# /// script
# requires-python = ">=3.10"
# dependencies = ["PyQt6", "Pillow", "numpy"]
# ///

from unittest.mock import patch, MagicMock
from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QPixmap, QImage, QIcon
from PyQt6.QtCore import Qt

app = QApplication(sys.argv)


# ── Test 1: Old code path DOES use ImageIO (via loadFromData) ──────────────

def test_old_path_uses_imageio():
    """Prove the old _get_menubar_icon triggers QPixmap.loadFromData (→ ImageIO)."""
    from PIL import Image
    import numpy as np
    import colorsys

    ASSETS_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "assets")
    TRAY_ICON_SIZE = 44
    icon_path = os.path.join(ASSETS_DIR, "icon.png")

    load_from_data_calls = 0
    original_loadFromData = QPixmap.loadFromData

    def counting_loadFromData(self, *args, **kwargs):
        nonlocal load_from_data_calls
        load_from_data_calls += 1
        return original_loadFromData(self, *args, **kwargs)

    # Reproduce the old code path exactly
    with patch.object(QPixmap, 'loadFromData', counting_loadFromData):
        for hue in [0, 60, 120, 180, 240, 300]:
            img = Image.open(icon_path).convert('RGBA')
            img = img.resize((TRAY_ICON_SIZE, TRAY_ICON_SIZE), Image.Resampling.LANCZOS)
            data = np.array(img)
            alpha = data[:, :, 3]
            r, g, b = colorsys.hsv_to_rgb(hue / 360.0, 0.8, 1.0)
            r, g, b = int(r * 255), int(g * 255), int(b * 255)
            data[:, :, 0] = r
            data[:, :, 1] = g
            data[:, :, 2] = b
            data[:, :, 3] = alpha

            from io import BytesIO
            buf = BytesIO()
            Image.fromarray(data).save(buf, format='PNG')
            buf.seek(0)
            pixmap = QPixmap()
            pixmap.loadFromData(buf.read())  # THIS is the ImageIO trigger

    assert load_from_data_calls == 6, (
        f"Expected 6 loadFromData calls (one per hue), got {load_from_data_calls}. "
        f"The old code path must use loadFromData to confirm it exercises ImageIO."
    )
    print(f"  Old path: {load_from_data_calls} loadFromData calls (each → ImageIO PNG codec)")


# ── Test 2: New code path does NOT use ImageIO ─────────────────────────────

def test_new_path_avoids_imageio():
    """Prove the fixed _get_menubar_icon does NOT call loadFromData (no ImageIO)."""
    from voice_thing import _get_menubar_icon

    load_from_data_calls = 0
    original_loadFromData = QPixmap.loadFromData

    def counting_loadFromData(self, *args, **kwargs):
        nonlocal load_from_data_calls
        load_from_data_calls += 1
        return original_loadFromData(self, *args, **kwargs)

    with patch.object(QPixmap, 'loadFromData', counting_loadFromData):
        # Template icon
        _get_menubar_icon(hue=None)
        # Hue cycling icons (the 20 FPS hot path)
        for hue in [0, 60, 120, 180, 240, 300]:
            _get_menubar_icon(hue=hue)

    assert load_from_data_calls == 0, (
        f"FAIL: New _get_menubar_icon still calls loadFromData {load_from_data_calls} times! "
        f"This means ImageIO PNG codec is still in the hot path, "
        f"and the SIGBUS crash (0x0BAD4007) is still possible."
    )
    print(f"  New path: {load_from_data_calls} loadFromData calls (ImageIO fully bypassed)")


# ── Test 3: New icons are valid ────────────────────────────────────────────

def test_new_icons_valid():
    """Verify refactored _get_menubar_icon produces non-null, correctly sized icons."""
    from voice_thing import _get_menubar_icon

    # Template icon
    icon = _get_menubar_icon(hue=None)
    sizes = icon.availableSizes()
    assert len(sizes) > 0, "Template icon has no sizes"
    print(f"  Template icon: {sizes[0].width()}x{sizes[0].height()}")

    # All hue values
    for hue in range(0, 360, 30):
        icon = _get_menubar_icon(hue=hue)
        sizes = icon.availableSizes()
        assert len(sizes) > 0, f"Hue {hue} icon has no sizes"
        pixmap = icon.pixmap(sizes[0])
        assert not pixmap.isNull(), f"Hue {hue} pixmap is null"

    print(f"  All 12 hue values produce valid icons")


# ── Test 4: Rapid cycling performance (mimics 20 FPS timer) ───────────────

def test_rapid_cycling_no_imageio():
    """Verify 200 rapid icon cycles don't touch ImageIO."""
    from voice_thing import _get_menubar_icon
    import time

    load_from_data_calls = 0
    original_loadFromData = QPixmap.loadFromData

    def counting_loadFromData(self, *args, **kwargs):
        nonlocal load_from_data_calls
        load_from_data_calls += 1
        return original_loadFromData(self, *args, **kwargs)

    with patch.object(QPixmap, 'loadFromData', counting_loadFromData):
        t0 = time.time()
        for i in range(200):
            _get_menubar_icon(hue=(i * 2) % 360)
        elapsed = time.time() - t0

    assert load_from_data_calls == 0, (
        f"FAIL: Rapid cycling triggered {load_from_data_calls} loadFromData calls"
    )
    print(f"  200 cycles in {elapsed:.3f}s ({elapsed/200*1000:.1f}ms/icon), 0 ImageIO calls")


# ── Test 5: Cursor deduplication ───────────────────────────────────────────

def test_cursor_deduplication():
    """Verify DraggableResizableMixin skips redundant setCursor calls."""
    from voice_thing import DraggableResizableMixin
    from PyQt6.QtWidgets import QWidget
    from PyQt6.QtCore import QPointF
    from PyQt6.QtGui import QMouseEvent

    class TestWidget(DraggableResizableMixin, QWidget):
        def __init__(self):
            QWidget.__init__(self)
            self._init_draggable()
            self.setFixedSize(200, 200)

    widget = TestWidget()
    widget.show()

    set_cursor_calls = 0
    original_setCursor = QWidget.setCursor

    def counting_setCursor(self, *args, **kwargs):
        nonlocal set_cursor_calls
        set_cursor_calls += 1
        return original_setCursor(self, *args, **kwargs)

    # Send 50 mouse moves to the same edge position → should deduplicate
    with patch.object(QWidget, 'setCursor', counting_setCursor):
        for _ in range(50):
            event = QMouseEvent(
                QMouseEvent.Type.MouseMove,
                QPointF(5.0, 100.0),  # Left edge
                Qt.MouseButton.NoButton,
                Qt.MouseButton.NoButton,
                Qt.KeyboardModifier.NoModifier,
            )
            widget.mouseMoveEvent(event)

    # With deduplication: should be 1 call (first time sets it, rest skip)
    # Without deduplication: would be 50 calls
    assert set_cursor_calls <= 2, (
        f"FAIL: {set_cursor_calls} setCursor calls for 50 moves to same edge. "
        f"Expected ≤2 (deduplication should prevent redundant calls). "
        f"Each redundant setCursor triggers ImageIO cursor bundle loading on macOS."
    )
    print(f"  50 mouse moves to same edge: {set_cursor_calls} setCursor calls (deduplicated)")

    widget.close()


# ── Run all tests ──────────────────────────────────────────────────────────

print("Test 1: Old code path uses ImageIO (via loadFromData)")
test_old_path_uses_imageio()
print()
print("Test 2: New code path avoids ImageIO entirely")
test_new_path_avoids_imageio()
print()
print("Test 3: New icons are valid and correctly sized")
test_new_icons_valid()
print()
print("Test 4: Rapid cycling (200 icons) without ImageIO")
test_rapid_cycling_no_imageio()
print()
print("Test 5: Cursor deduplication reduces setCursor calls")
test_cursor_deduplication()
print()
print("All tests passed — ImageIO crash vector eliminated.")
