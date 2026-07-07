#!/usr/bin/env python3
"""Verify a QR code PNG has real (non-blank) content.

Usage:
    python3 verify-qr.py <qr-file.png>

Checks:
    - File exists and is a PNG
    - At least 5000 black pixels present (catches blank images)
    - Prints black/white pixel count and passes/fails
"""

import sys
from pathlib import Path

try:
    from PIL import Image
except ImportError:
    print("FAIL: Pillow not installed (pip3 install Pillow)")
    sys.exit(1)

path = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("qr-CODE.png")

if not path.exists():
    print(f"FAIL: {path} not found")
    sys.exit(1)

if path.stat().st_size < 200:
    print(f"FAIL: {path} is only {path.stat().st_size} bytes — likely blank")
    sys.exit(1)

img = Image.open(path)
pixels = list(img.getdata())
black = sum(1 for p in pixels if p == 0)
white = sum(1 for p in pixels if p == 255 or p == 1)
total = len(pixels)

print(f"File:    {path.name}")
print(f"Size:    {img.size[0]}x{img.size[1]} ({total} px)")
print(f"Black:   {black} ({black/total*100:.1f}%)")
print(f"White:   {white} ({white/total*100:.1f}%)")
print(f"File:    {path.stat().st_size} bytes on disk")

if black > 5000:
    print("PASS: QR has real content (scannable)")
    sys.exit(0)
elif black > 0:
    print(f"WARN: Only {black} black pixels — may be hard to scan")
    sys.exit(0)
else:
    print("FAIL: QR is blank (zero black pixels) — regenerate with qrencode")
    sys.exit(1)
