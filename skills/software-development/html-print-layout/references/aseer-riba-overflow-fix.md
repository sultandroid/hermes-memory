# Aseer Museum RIBA Tree — Page Overflow Fix Reference

## Document
A4 portrait HTML deliverable tree: 279 data rows, 15 categories (A-O), RIBA Stages 4-6. Museum exhibition fit-out in Abha, KSA.

## Evolution

| Attempt | Sheets | Overflow | Approach |
|---|---|---|---|
| Original | 6 | Sheet 2: +1734px, Sheet 3-5 moderate | N/A — author crammed 189 rows on one page |
| First fix | 10 | C-section sheets still overflow (+500-1700px) | Split Cat C into 3 groups (C01-C05, C06-C10, C11-C15) — not granular enough |
| Final fix | **22** | **Zero overflow** | Split Cat C into individual Cxx sheets (most carry 9-18 rows each) |

## Row Height Measurements (from browser_console)

| Row type | Avg px | Notes |
|----------|--------|-------|
| C parent rows | 39px | Short one-line description |
| C child rows | 51px | Long descriptions wrap to 2-3 lines |
| C category header | 35px | Colspan row |
| Stage 5 data rows | 33px | Shorter descriptions |
| Stage 6 data rows | 32px | Shorter descriptions |
| Table head (thead) | 17px | |
| Cat-header row | ~20px | |
| Docstrip + h2 | ~40px | |
| Footer | ~20px | |

## Per-Page Budget
- Sheet total: 1123px (297mm @ 96dpi)
- Padding: ~106px (28mm)
- Inner available: ~1017px
- Overhead: ~97px (thead + cat-hdr + docstrip + h2 + footer)
- **Available for rows: ~920px**
- **Practical max: 20 C-rows / 27 Stage-rows**

## Final Split Strategy

| Sheet | Content | Rows | Fits? |
|---|---|---|---|
| 1/22 | Cover | 0 | Squeezed via CSS |
| 2/22 | A+B | 18 | ✓ |
| 3/22 | C01 Showcase | 13 | ✓ |
| 4/22 | C02 Setworks | 13 | ✓ |
| 5/22 | C03 Graphics | 10 | ✓ |
| 6/22 | C04 Models | 9 | ✓ |
| 7/22 | C05 AV/IT | 12 | ✓ |
| 8/22 | C06 Lighting | 11 | ✓ |
| 9/22 | C07+C08 Acoustics+Rigging | 18 | ✓ combined |
| 10/22 | C09 FF&E | 9 | ✓ |
| 11/22 | C10 MEP | 15 | ✓ |
| 12/22 | C11 Fire/Life Safety | 12 | ✓ |
| 13/22 | C12 Structural | 10 | ✓ |
| 14/22 | C13+C14 Glazing+Lifts | 18 | ✓ combined |
| 15/22 | C15 Materials Testing | 9 | ✓ |
| 16/22 | D Specs & Certs | 12 | ✓ |
| 17/22 | E-G Compliance/BIM/H&S | 22 | ✓ |
| 18/22 | H+I Pre-Con+Specialist | 21 | ✓ |
| 19/22 | J+K Quality+Commissioning | 15 | ✓ |
| 20/22 | L+M Handover | 20 | ✓ |
| 21/22 | N+O Aftercare+Close-Out | 12 | ✓ |
| 22/22 | Summary Dashboard | 0 | ✓ |

## Cover Page Fix

The cover overflowed by +55px initially. Solution: CSS rules targeting the first sheet's info-box divs with `!important` to override inline `style=` attributes. Key technique — use broad `[style*="border"]` selectors because the exact formatting of inline styles varies and `[style*="border:.4pt"]` may not match.

```css
.sheet:first-of-type > div[style*="border"],
.sheet:first-of-type > div[style*="background"] {
  font-size: 5.5pt !important;
  line-height: 1.15 !important;
  padding: 0.6mm 1mm !important;
}
```

## Python Rebuild Pattern

Key functions that prevent common bugs:

```python
# Strip old wrapper before re-wrapping (avoids double-wrapping)
def strip_wrapper(html):
    html = re.sub(r'<div class="doc-strip">.*?</div>', '', html, count=1, flags=re.DOTALL)
    html = re.sub(r'<div class="doc-strip".*?SHEET.*?</div>', '', html, count=1, flags=re.DOTALL)
    html = re.sub(r'^<div class="sheet">', '', html.strip())
    html = re.sub(r'</div>\s*$', '', html.strip())
    return html.strip()

# Find parent row INCLUDING its <tr> tag
def find_parent_row(html, code):
    pattern = f'<tr><td class="ref">C{code}</td>'
    pos = html.find(pattern)
    if pos < 0: return None
    # Find next parent row or end
    next_code = int(code) + 1
    next_pattern = f'<tr><td class="ref">C{next_code:02d}</td>'
    end = html.find(next_pattern, pos + 1)
    if end < 0: end = len(html)
    return html[pos:end]
```

## Verification Snippet

```javascript
Array.from(document.querySelectorAll('.sheet')).every(s => s.offsetHeight <= 1124)
// true = ALL SHEETS FIT A4
```
