# Full-Profile Audit Checklist

Run before and after any batch of changes to the Samaya Factory profile.

## 1. Page Structure Audit

```python
import re
with open("v6/index.html") as f: html = f.read()

# Count section tags balance
opens = [m.start() for m in re.finditer('<section ', html)]
closes = [m.start() for m in re.finditer('</section>', html)]
print(f"Open: {len(opens)}, Close: {len(closes)}")
if len(opens) != len(closes): print("⚠ MISMATCH!")
```

## 2. Missing Images Audit

```python
import os, re
from urllib.parse import unquote

base = "/path/to/samaya-profile"
all_refs = set()
with open(base + "/v6/index.html") as f:
    for m in re.finditer(r'\.\./assets/[^"\')\s]+', f.read()):
        all_refs.add(m.group())
for cf in os.listdir(base + "/v6/css"):
    if cf.endswith('.css'):
        with open(base + "/v6/css/" + cf) as f:
            for m in re.finditer(r'\.\./assets/[^"\')\s]+', f.read()):
                all_refs.add(m.group())

for ref in sorted(all_refs):
    path = ref.replace("../", "", 1)
    decoded = unquote(os.path.join(base, path))
    if not os.path.isfile(decoded):
        print(f"  MISSING: {ref}")
```

Note: References with spaces in the filesystem (e.g. `APPROVED VENEER SAMPLE` without extension, `Oddy Test_Lab.jpg`) will show as `APPROVED` and `Oddy` in the regex — these are false positives from the regex stopping at spaces. Verify by checking if the full (unquoted) path exists.

## 3. Duplicate Images Audit

```python
from collections import Counter
refs = []
for m in re.finditer(r'\.\./assets/img/[^"\')\s]+', html):
    refs.append(m.group())
for img, count in Counter(refs).most_common():
    if count > 1:
        print(f"  {img} ({count}x)")
```

Most duplicates are intentional (same project photo in gallery + flagship detail). Investigate only when count > 2 or photo is process-01.jpg (should be unique per process step).

## 4. Overflow Risk Audit

Check page sections with content > 10K chars:

Range|Risk
---|---
< 6K chars|✓ OK
6K-10K chars|✓ OK (fits A4)
10K-15K chars|⚠ Check (may overflow if image-heavy)
15K+ chars|⚠ HIGH RISK — overflow likely

Common high-char pages: #p24a (sectorial index), #p24a-2 (sectorial II), #p26 (org chart)

When overflowing: reduce image heights, tighten gaps, reduce font sizes. For sectorial index specifically, reduce card image height from 28mm to 24mm and gap from 2mm to 1.5mm.

## 5. Brand Slogan Check

```bash
grep -c 'صناعة الإرث. هندسة الفنّ.' v6/index.html  # should be 1 (cover)
grep -c 'Crafting Legacy. Engineering Art.' v6/index.html  # should be 1 (cover)
```

These must NEVER change. If 0, Claude or a subagent rewrote them — revert immediately.

## 6. Aseer Museum Check

```bash
grep -c 'متحف عسير\|Aseer Museum\|ASEER MUSEUM' v6/index.html
```

Should be 0 in the final profile. Aseer Museum is a separate project, not for Samaya prequalification.

## 7. TOC Page Numbers vs Actual IDs

Extract all `id="p..."` from sections and compare to TOC `href="#p..."` entries. Every section ID should have a matching TOC entry, and vice versa.
