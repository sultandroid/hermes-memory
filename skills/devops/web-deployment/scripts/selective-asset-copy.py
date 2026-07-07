#!/usr/bin/env python3
"""
Selective asset copier for Surge.sh deployment.

Reads an HTML file, extracts all referenced asset paths (from url(), src=),
resolves them against a source assets root, and copies only those files
to a deploy target directory — preserving directory structure.

Usage:
    python3 selective-asset-copy.py <index.html> <src_root> <dst_root> [--strip-prefix ../]

Example:
    python3 selective-asset-copy.py \
        /tmp/deploy/index.html \
        /path/to/source/assets \
        /tmp/deploy/assets \
        --strip-prefix ../
"""

import re, os, shutil, sys

def extract_asset_refs(html: str) -> set[str]:
    """Extract all asset-relative paths from HTML src= and url() attributes."""
    refs: set[str] = set()
    # url("path") or url('path')
    for m in re.finditer(r'url\(\"?([^"\)]+)\"?\)', html):
        refs.add(m.group(1))
    for m in re.finditer(r"url\('?([^'\)]+)'?\)", html):
        refs.add(m.group(1))
    # src="path" or src='path'
    for m in re.finditer(r'src="([^"]+)"', html):
        refs.add(m.group(1))
    for m in re.finditer(r"src='([^']+)'", html):
        refs.add(m.group(1))
    return refs

def main():
    if len(sys.argv) < 4:
        print(__doc__)
        sys.exit(1)

    html_path = sys.argv[1]
    src_root = sys.argv[2]
    dst_root = sys.argv[3]
    strip_prefix = None
    extra_args = sys.argv[4:]
    for i, a in enumerate(extra_args):
        if a == '--strip-prefix' and i+1 < len(extra_args):
            strip_prefix = extra_args[i+1]

    with open(html_path) as f:
        html = f.read()

    refs = extract_asset_refs(html)
    refs = {r for r in refs if r.startswith(('assets/', '../assets/', './assets/'))}

    if not refs:
        print("No assets/ references found in HTML.")
        return

    ok = 0
    miss = 0
    for ref in sorted(refs):
        clean = ref
        if strip_prefix and clean.startswith(strip_prefix):
            clean = clean[len(strip_prefix):]
        clean = clean.lstrip('./')
        src = os.path.join(src_root, clean)
        dst = os.path.join(dst_root, clean)
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        if os.path.exists(src):
            shutil.copy2(src, dst)
            ok += 1
        else:
            from urllib.parse import unquote
            decoded = unquote(src)
            if decoded != src and os.path.exists(decoded):
                shutil.copy2(decoded, dst)
                ok += 1
            else:
                print(f"MISS: {ref}")
                miss += 1

    print(f"Copied {ok} assets, {miss} missing")

if __name__ == "__main__":
    main()
