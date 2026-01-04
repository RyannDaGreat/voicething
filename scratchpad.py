#!/usr/bin/env /opt/homebrew/opt/python@3.10/bin/python3.10
"""Test if QIcon can load SVG directly"""
from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QIcon

app = QApplication([])

# Can we just do this?
icon = QIcon("/opt/homebrew/lib/python3.10/site-packages/rp/git/voicething/assets/mic.svg")
print(f"Icon is null: {icon.isNull()}")
print(f"Available sizes: {icon.availableSizes()}")
