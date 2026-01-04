#!/usr/bin/env /opt/homebrew/opt/python@3.10/bin/python3.10
"""Restore pen icon"""
import urllib.request

url = "https://api.iconify.design/ph/pen-nib-fill.svg?color=%23ffffff&height=256"
output_path = "/opt/homebrew/lib/python3.10/site-packages/rp/git/voicething/assets/pen.svg"
urllib.request.urlretrieve(url, output_path)
print(f"Restored {output_path}")
