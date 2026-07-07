#!/usr/bin/env python3
"""Scan all .py scripts in a directory for icon/emoji characters.
Usage: python3 scan_icons.py [path_to_scripts]
Default: scans current directory ./_scripts/ then ./scripts/"""

import os, sys

ICON_RANGES = [
    (0x25A0, 0x25FF), (0x2600, 0x26FF), (0x2700, 0x27BF),
    (0x2B00, 0x2BFF), (0x1F000, 0x1FFFF), (0x2300, 0x23FF),
    (0x2500, 0x257F), (0x2580, 0x259F), (0xFE00, 0xFE0F),
    (0x200D, 0x200D),
]

def scan(path):
    found = 0
    for fname in sorted(os.listdir(path)):
        if not fname.endswith('.py'):
            continue
        fp = os.path.join(path, fname)
        with open(fp) as fh:
            lines = fh.readlines()
        for ln, line in enumerate(lines, 1):
            for c in line:
                cp = ord(c)
                for lo, hi in ICON_RANGES:
                    if lo <= cp <= hi:
                        print(f'{fname}:{ln} U+{cp:04X} = {repr(c)}')
                        found += 1
                        break
    return found

if __name__ == '__main__':
    paths = sys.argv[1:] if len(sys.argv) > 1 else ['_scripts', 'scripts']
    total = 0
    for p in paths:
        if os.path.isdir(p):
            total += scan(p)
    print(f'\nTotal icons found: {total}')
    sys.exit(0 if total == 0 else 1)
