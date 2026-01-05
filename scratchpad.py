"""Test progressive button collapse at narrow widths."""
import sys
import os

from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QTimer

sys.path.insert(0, "/opt/homebrew/lib/python3.10/site-packages/rp/git/voicething")
from voice_thing import VoiceThingWindow

app = QApplication(sys.argv)

window = VoiceThingWindow()
window.show()

def test_widths():
    """Test button modes at different widths."""
    print("=== Testing Button Width Modes ===")

    # Wide mode (400px) - should show text+icon
    window.resize(400, 300)
    print(f"\n1. Wide (400px): record_btn text = '{window.record_btn.text()}'")
    print(f"   prefs_btn visible = {window.prefs_btn.isVisible()}")

    # Icon-only mode (300px) - should show icon only
    window.resize(300, 300)
    QTimer.singleShot(100, test_icon_mode)

def test_icon_mode():
    print(f"\n2. Icon-only (300px): record_btn text = '{window.record_btn.text()}'")
    print(f"   prefs_btn visible = {window.prefs_btn.isVisible()}")

    # Minimal mode (200px) - should show only 4 buttons
    window.resize(200, 300)
    QTimer.singleShot(100, test_minimal_mode)

def test_minimal_mode():
    print(f"\n3. Minimal (200px): record_btn text = '{window.record_btn.text()}'")
    print(f"   record_btn visible = {window.record_btn.isVisible()}")
    print(f"   copy_btn visible = {window.copy_btn.isVisible()}")
    print(f"   prefs_btn visible = {window.prefs_btn.isVisible()}")
    print(f"   help_btn visible = {window.help_btn.isVisible()}")

    print("\n=== Test Complete ===")
    QTimer.singleShot(500, app.quit)

QTimer.singleShot(500, test_widths)

sys.exit(app.exec())
