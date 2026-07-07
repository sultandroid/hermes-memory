#!/usr/bin/env python3
"""HTML QA checker — counts SVG, img, base64 elements and validates images.
Fugu-generated. Reusable for any HTML proposal/document audit.
Usage: python3 check_proposal_assets.py FILE.html
"""
import json, sys, re, base64
from pathlib import Path
from html.parser import HTMLParser

class QAChecker(HTMLParser):
    def __init__(self):
        super().__init__()
        self.tag_counts = {}
        self.svg_depth = 0
        self.svg_root_count = 0
        self.img_count = 0
        self.data_img_count = 0
        self.data_img_srcs = []  # (offset, mime, b64)
        
    def handle_starttag(self, tag, attrs):
        self.tag_counts[tag] = self.tag_counts.get(tag, 0) + 1
        if tag == 'svg':
            if self.svg_depth == 0:
                self.svg_root_count += 1
            self.svg_depth += 1
        if tag == 'img':
            self.img_count += 1
            for k, v in attrs:
                if k == 'src' and v and v.startswith('data:image/'):
                    self.data_img_count += 1
                    m = re.match(r'data:image/(\w+);base64,([A-Za-z0-9+/=]+)', v)
                    if m:
                        self.data_img_srcs.append((m.group(1), m.group(2)))
        
    def handle_endtag(self, tag):
        if tag == 'svg':
            self.svg_depth -= 1

def validate_b64(mime, data):
    """Validate base64 string and check image signature bytes."""
    try:
        raw = base64.b64decode(data)
    except Exception as e:
        return False, str(e)
    sigs = {
        'png': b'\x89PNG',
        'jpeg': b'\xff\xd8',
        'gif': b'GIF8',
        'webp': b'RIFF',
        'svg': b'<svg',
    }
    expected = sigs.get(mime)
    if expected and raw[:len(expected)] != expected:
        return False, f"Signature mismatch: expected {expected!r}, got {raw[:4]!r}"
    return True, "OK"

def main():
    if len(sys.argv) < 2:
        print("Usage: check_proposal_assets.py FILE.html")
        sys.exit(2)
    
    path = Path(sys.argv[1])
    html = path.read_text(encoding='utf-8')
    
    checker = QAChecker()
    checker.feed(html)
    
    # Validate base64 images
    b64_results = []
    for mime, data in checker.data_img_srcs:
        ok, msg = validate_b64(mime, data)
        b64_results.append({
            "mime": mime,
            "base64_chars": len(data),
            "base64_ok": ok,
            "error": None if ok else msg,
        })
    
    result = {
        "file": path.name,
        "file_size_bytes": len(html.encode()),
        "counts": {
            "svg_root_tags": checker.svg_root_count,
            "img_tags": checker.img_count,
            "data_image_base64_occurrences": len(checker.data_img_srcs),
        },
        "svg_tag_breakdown": {k: v for k, v in sorted(checker.tag_counts.items()) if v > 0},
        "base64_validation": {
            "valid_count": sum(1 for b in b64_results if b["base64_ok"]),
            "invalid_count": sum(1 for b in b64_results if not b["base64_ok"]),
            "items": b64_results,
        },
    }
    
    print(json.dumps(result, indent=2))
    
    if result["base64_validation"]["invalid_count"] > 0:
        print(f"\n⚠ {result['base64_validation']['invalid_count']} broken base64 image(s) found", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
