# Samaya HTML Template — Compact/Tight/Xtight Overflow Management

## Problem
A4 print HTML pages (210mm x 297mm) with `overflow: hidden` clip content that exceeds the page. Different pages have different content densities — a dense table needs tighter spacing, while a sparse page should breathe.

## Solution: Three-level CSS class hierarchy

Apply these classes to the `<section class="page">` tag based on content density:

| Class | When to use | What it does |
|-------|-------------|--------------|
| `compact` | All content pages (base) | Reduces card padding, shrinks snapshot values, tightens sec-banner margins |
| `tight` | Pages with moderate density | Smaller heading font, tighter h2-row, reduced page-header padding |
| `xtight` | Pages with high density (overflow risk) | Smallest table font (0.38rem), minimal cell padding (1px/3px), smallest h2 (0.7rem), reduced spec-strip and snapshot-card padding |

### CSS definitions

```css
.compact .sec-banner { margin: 4px 0 2px 0; }
.compact .sec-banner b { font-size: 0.54rem; }
.compact .eng-table td { padding: 2px 5px; }
.compact .eng-table th { padding: 2px 5px; }
.compact .spec-strip { padding: 3px 7px; margin: 0 0 4px 0; }
.compact .snapshot-card { padding: 3px 5px; }
.compact .snapshot-val { font-size: 0.62rem; }
.compact .page-header { margin-bottom: 4px; padding-bottom: 2px; }
.compact .h2-row { margin-bottom: 3px; margin-top: 0; }
.compact h2 { font-size: 0.82rem; }
.compact .h2-bar { height: 26px; }
.compact .raci-badge { width: 14px; height: 14px; line-height: 14px; font-size: 0.36rem; }

.tight .sec-banner { margin: 3px 0 1px 0; }
.tight .sec-banner b { font-size: 0.48rem; }
.tight .eng-table td { padding: 1.5px 4px; font-size: 0.42rem; line-height: 1.25; }
.tight .eng-table th { padding: 1.5px 4px; font-size: 0.42rem; }
.tight .spec-strip { padding: 2px 6px; margin: 0 0 3px 0; }
.tight .snapshot-card { padding: 2px 4px; }
.tight h2 { font-size: 0.78rem; }
.tight .h2-bar { height: 24px; }
.tight .page-header { margin-bottom: 3px; padding-bottom: 2px; }
.tight .h2-row { margin-bottom: 2px; margin-top: 0; }
.tight .sec-banner svg { width: 12px; height: 12px; }

.xtight .sec-banner { margin: 2px 0 1px 0; }
.xtight .sec-banner b { font-size: 0.48rem; }
.xtight .eng-table td { padding: 1px 3px; font-size: 0.38rem; line-height: 1.2; }
.xtight .eng-table th { padding: 1px 3px; font-size: 0.38rem; }
.xtight .spec-strip { padding: 1px 4px; margin: 0 0 2px 0; }
.xtight .snapshot-card { padding: 2px 4px; }
.xtight .snapshot-val { font-size: 0.55rem; }
.xtight h2 { font-size: 0.7rem; }
.xtight .h2-bar { height: 20px; }
.xtight .page-header { margin-bottom: 3px; padding-bottom: 2px; }
.xtight .h2-row { margin-bottom: 2px; margin-top: 0; }
.xtight .sec-banner svg { width: 12px; height: 12px; }
```

### How to apply

1. Add the CSS block above to the document's `<style>` section
2. Set the base class on every page section tag:
   ```html
   <section class="page compact">  <!-- or compact tight, or compact tight xtight -->
   ```
3. Measure content density and adjust per page

### Density estimation formula

```python
def estimate_density(page_content):
    table_rows = len(re.findall(r'<tr', page_content))
    text_len = len(page_content)
    svgs = len(re.findall(r'<svg', page_content))
    est_height = text_len * 0.03 + table_rows * 10 + svgs * 100
    available = 1972  # pixels approx for A4
    pct = est_height / available * 100
    if pct > 75:  return 'compact tight xtight'
    if pct > 50:  return 'compact tight'
    return 'compact'
```

### Balance rule
Do NOT apply `xtight` to pages that have plenty of space. Pages under 60% usage should use `compact` or `compact tight` only — the content should breathe. Only use `xtight` on pages that measurably need it (over 75% estimated usage).
