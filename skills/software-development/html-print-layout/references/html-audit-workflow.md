# HTML Audit Workflow — Systematic QA for A4 Plan Documents

## When to Use

When auditing an existing A4 HTML document (SMP, BEP, PEP, or any formal project plan) for:
- Page overflow (content exceeding A4 boundary)
- Data accuracy (stale numbers, wrong names, mismatched counts)
- Style errors (special characters, AI fingerprints, forbidden symbols)
- CSS issues (missing print rules, broken layout)

## Audit Checklist (in order)

### 1. Page Overflow — Browser Measurement

```javascript
// Run in browser console on the rendered document
Array.from(document.querySelectorAll('section.page')).map((s, i) => {
  const h = s.offsetHeight;
  const expected = Math.round(297 / 25.4 * 96); // ~1123px for A4 at 96dpi
  const status = h > expected + 5 ? 'OVERFLOW +' + (h - expected)
    : h < expected - 5 ? 'UNDERFLOW -' + (expected - h) : 'OK';
  return `Page ${i+1}: ${h}px ${status}`;
}).join('\\n')
```

### 2. Data Accuracy Checks

| Check | Method |
|-------|--------|
| TOC page count vs actual pages | Count `<section class="page">` elements, compare to TOC chip |
| Footer page numbers | Extract all `PAGE X / Y` — Y must be consistent across all pages |
| Stale role counts | Search for old numbers (e.g. "55 roles" when document now has 61) |
| Personnel names | Cross-check against specialist register, KP register, PROJECT_MEMORY |
| Revision history | Verify dates, status codes, approver names against known project facts |
| Cover vs internal revision | Cover, TOC, section chips, and footers must all agree on Rev number |

### 3. Style Error Checks

| Check | Method | Target |
|-------|--------|--------|
| En-dash `&ndash;` | `grep -c '&ndash;'` | 0 |
| Middle dot `&middot;` | `grep -c '&middot;'` | 0 |
| Section symbol `&sect;` | `grep -c '&sect;'` | 0 |
| Literal `§` in SVG text | `grep -c '§'` | 0 |
| Accented characters | `grep -c '[éèêëàâäùûüôöîïç]'` | 0 |
| HTML entity icons | `grep -c '&#9888;\|&#127963;\|&#9989;\|&#10003;\|&#128209;'` | 0 |
| AI fingerprints | `grep -ci 'seamlessly\|synergistic\|cutting-edge\|holistic\|leverage\|robust\|innovative\|bespoke'` | 0 |
| Meta-commentary | `grep -ci 'this document outlines\|the following sections'` | 0 |

### 4. CSS Issues

| Check | Method |
|-------|--------|
| `@page { size: A4 portrait; margin: 0; }` present | grep for `@page` |
| `print-color-adjust: exact` in @media print | grep for `print-color-adjust` |
| `page-break-after: always` on `.page` | grep for `page-break-after` |
| `overflow: hidden` on `.page` | grep for `overflow` in .page CSS |
| No `display: flex` on `.page` (causes white space) | grep for `display: flex` in .page rules |

### 5. Bulk Fix Pattern (Python)

```python
import re

with open(path, 'r') as f:
    content = f.read()

# Replace HTML entities
content = content.replace('&ndash;', '-')
content = content.replace('&middot;', '-')
content = content.replace('&sect;', 'Sec.')

# Replace HTML entity icons
replacements = {
    '&#127963;': '[STRATEGY]',
    '&#9888;': '[WARNING]',
    '&#9989;': '[OK]',
    '&#10003;': '[OK]',
    '&#128209;': '[DOC]',
}
for entity, text in replacements.items():
    content = content.replace(entity, text)

# Fix accented characters
content = content.replace('Glassbühne', 'Glassbuhne')

with open(path, 'w') as f:
    f.write(content)

# Verify — must all be 0
import subprocess
for pattern in ['&ndash;', '&middot;', '&sect;', '§', 'Glassbühne']:
    result = subprocess.run(['grep', '-c', pattern, path], capture_output=True, text=True)
    count = int(result.stdout.strip())
    if count > 0:
        print(f'WARNING: {count} occurrences of "{pattern}" remain')
```

### 6. Verification After Fixes

```bash
# Re-check all style errors
grep -c '&ndash;' file.html    # must be 0
grep -c '&middot;' file.html   # must be 0
grep -c '&sect;' file.html     # must be 0
grep -c '§' file.html          # must be 0
grep -c '[éèêëàâäùûüôöîïç]' file.html  # must be 0

# Re-check page overflow in browser
# Run the browser measurement snippet again
```
