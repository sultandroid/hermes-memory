#!/usr/bin/env python3
"""Copy only HTML/CSS-referenced assets for Surge deployment."""
import re, os, shutil
from urllib.parse import unquote

ASSETS_ROOT = "/Users/mohamedessa/Library/CloudStorage/OneDrive-SAMAYAINVESTMENT/Samaya/Technical Office/samaya-profile/assets"
DEST_ROOT = "/tmp/samaya-profile-deploy/assets"
INDEX_PATH = "/tmp/samaya-profile-deploy/index.html"

with open(INDEX_PATH) as f:
    html = f.read()

refs = set()
for m in re.findall(r'url\("?assets/([^"\)]+)"?\)', html): refs.add(m)
for m in re.findall(r"url\('?assets/([^'\)]+)'?\)", html): refs.add(m)
for m in re.findall(r'src="assets/([^"]+)"', html): refs.add(m)
for m in re.findall(r"src='assets/([^']+)'", html): refs.add(m)

ok = 0
miss = 0
for ref in sorted(refs):
    # Destination must be URL-decoded — Surge stores files decoded but serves URLs encoded
    dst = os.path.join(DEST_ROOT, unquote(ref))
    src = os.path.join(ASSETS_ROOT, ref)
    src_decoded = os.path.join(ASSETS_ROOT, unquote(ref))
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    if os.path.isfile(src):
        shutil.copy2(src, dst); ok += 1
    elif os.path.isfile(src_decoded):
        shutil.copy2(src_decoded, dst); ok += 1
    else:
        print(f"MISS: {ref}"); miss += 1

print(f"OK: {ok}  MISS: {miss}  TOTAL: {len(refs)}")
