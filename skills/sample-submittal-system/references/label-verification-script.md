# Label HTML Verification Script

Use this as a template for ad-hoc verification after editing any label HTML file.

```python
#!/usr/bin/env python3
"""Ad-hoc verification: label.html print-ready quality checks"""
import os, re, base64, sys

path = "/path/to/label.html"  # update
with open(path) as f:
    html = f.read()

errors = []

# 1. DOCTYPE
if not html.startswith("<!DOCTYPE html>"):
    errors.append("Missing DOCTYPE")

# 2. Tag balance
for tag in ["section", "div", "main", "footer", "ul", "li"]:
    opens = len(re.findall(f'<{tag}[\\s>]', html))
    closes = len(re.findall(f'</{tag}>', html))
    if opens != closes:
        errors.append(f"<{tag}> mismatch: {opens} open, {closes} close")

# 3. Base64 integrity
b64s = re.findall(r'data:image/(?:png|jpeg);base64,([A-Za-z0-9+/=]+)', html)
for i, b64 in enumerate(b64s):
    rem = len(b64) % 4
    if rem != 0:
        errors.append(f"B64 block {i}: len={len(b64)} mod4={rem}")
    try:
        decoded = base64.b64decode(b64)
        if len(decoded) < 100:
            errors.append(f"B64 block {i}: only {len(decoded)}B")
    except Exception as e:
        errors.append(f"B64 block {i}: {e}")

# 4. Print spec
spec_checks = {
    "bleed: 3mm": "Missing bleed",
    "marks: crop cross": "Missing crop marks",
    "print-color-adjust: exact": "Missing print-color-adjust",
}
for pattern, msg in spec_checks.items():
    if pattern not in html:
        errors.append(msg)

# 5. No stray px (allow pt and -webkit-)
for i, line in enumerate(html.split("\n"), 1):
    s = line.strip()
    if "px" in s and "pt" not in s and "-webkit-" not in s:
        errors.append(f"Line {i}: px value — {s[:55]}")

# 6. @media print block
if "@media print" not in html:
    errors.append("Missing @media print block")

print(f"File: {path}")
print(f"  {len(html)/1024:.0f}KB, {len(b64s)} base64 images, "
      f"{len(re.findall(r'--[a-z-]+:', html))} CSS vars")
if errors:
    print(f"  FAIL — {len(errors)} issue(s):")
    for e in errors:
        print(f"    ✗ {e}")
    sys.exit(1)
else:
    print("  PASS — all checks OK, print-ready")
    sys.exit(0)
```

## How to run

Write to a temp path, chmod, execute, then clean up:

```bash
cat > /tmp/hermes-verify-label.py << 'SCRIPT'
# ... paste script content ...
SCRIPT
chmod +x /tmp/hermes-verify-label.py
python3 /tmp/hermes-verify-label.py
rm /tmp/hermes-verify-label.py
```

Or run inline from `execute_code` which handles temp files automatically.
