---
name: html-css-audit
title: HTML/CSS Quality Audit
description: Systematic checklist for auditing HTML and CSS code quality — tag balance, section numbering consistency, inline style proliferation, print CSS correctness, accessibility landmarks, and performance. Use when asked to review, audit, or check the quality of any HTML/CSS document.
category: software-development
---

# HTML/CSS Quality Audit

Produce a ranked table: critical issues at top, minor at bottom, with severity markers (🔴🟡🟢). Each row: #, Issue, Severity, Detail.

## Systematic Checklist

### 1. Fetch Raw Source
Never trust rendered summaries — fetch the raw HTML source:
```
curl -sL -o /tmp/page.html '<URL>'
```
Read in sections with `read_file(offset, limit)`. For bulk analysis, pipe to Python:
```
curl -sL '<URL>' | python3 -c "import sys, re; html = sys.stdin.read(); ..."
```

### 2. Tag Balance Check
Count opening vs closing tags for ALL container elements. Generate a mismatch table showing `opens, closes, diff`.

Run per-FILE (not just assembled output). A missing closing tag in one file swallows subsequent files in concatenated assembly.

| Tag pattern | HTML5 rules |
|-------------|-------------|
| `div`, `section`, `span`, `p`, `table`, `tr`, `td`, `th`, `header`, `footer`, `ul`, `ol`, `li`, `a`, `b`, `strong` | Must have closing tag |
| `img`, `br`, `hr`, `input`, `meta`, `link` | Void — no close needed |
| `path`, `rect`, `g`, `clipPath`, `defs` (SVG) | Self-closing OK with `/>` |

**CRITICAL: Every page file must have exactly 1 `</section>` tag.** A missing `</section>` causes the assembler to swallow ALL subsequent files into the unclosed section, doubling content and corrupting structure. After any edit, verify:
```python
for f in page_files:
    sections = open(f).read().count('<section')
    closes = open(f).read().count('</section>')
    assert sections == closes == 1, f'{f}: {sections} opens vs {closes} closes'
```

Also verify each file has exactly 1 `<footer>` and 1 `</footer>` — missing footers break page layout.

### 3. Section Numbering Drift
HTML comment markers (`<!-- SECTION N: -->`) should match visible `<h2>N.</h2>` numbers. Scan for drift — once it shifts, all subsequent sections are misaligned. Flag the first mismatch.

### 4. Inline Style Audit
Count `style="` occurrences. High count (>50) means CSS classes are being bypassed. Cross-check:
- Properties duplicated in both CSS class and inline style
- Critical layout values set inline that should be in CSS
- CSS custom properties (`var(--x)`) defined but overridden inline

### 5. Duplicate ID Check
Parse all `id="..."` values and flag duplicates with Python `Counter`. Breaks anchor linking.

### 6. CSS Structure
- All `<style>` blocks belong in `<head>`, never `<body>`
- CSS comments consistent (`=====` not `=***`)
- No unused CSS classes (spot-check HTML for each selector)
- Print rules exist: `@page`, `@media print`, `break-inside`, `page-break-inside`
- CSS custom properties are actually consumed, not orphaned

### 7. Print CSS Correctness
- `@page { size: A4 portrait; margin: 10mm }` — printer margin reserves
- `break-after:page` on each page section
- `break-inside:avoid` on tables, cards, badges, strips
- `thead { display: table-header-group }` for repeating table headers
- `a[href]:after { content: "" }` to suppress link URLs in print
- `-webkit-print-color-adjust: exact` for background colors
- Absolute-positioned footers need `bottom: Xmm` + sufficient page padding-bottom

### 8. Performance
- Single HTML file >200KB is large — flag it
- Repeated base64 data URIs (logos repeated per page = wasted bandwidth)
- Inline SVG with hundreds of path nodes — suggest simplification
- Multiple Google Fonts with many weight variants → FOUT/FOIT on load

### 9. Accessibility Basics
- `<html lang="...">` and `dir="..."` set correctly
- Semantic landmarks: `<main>`, `<nav>`, `<article>`, `<aside>` preferred over bare `<div>`/`<section>`
- No interactive elements without accessible names
- RTL documents: `dir="rtl"` on parent, `dir="ltr"` explicitly on embedded English/numeric content (specs, model numbers, prices)

### 10. RTL Edge Cases
- Numeric content (prices, model numbers, specs) in RTL context needs `dir="ltr"` wrapping for correct rendering
- Mixed Arabic/English abbreviations (ISO 9001, QSC AD-C6T-HC) need `unicode-bidi: embed` or explicit dir

## Reference Script
The `references/check.py` file contains the Python analysis templates used in this session — tag balance, section drift, inline style count, duplicate IDs. Load it with `skill_view('html-css-audit', file_path='references/check.py')`.

## Pitfalls
- **`html.count('class=\"page\"')` overcounts** — "page" also matches "page-header", "pg-footer", "page-cover". Use regex with word boundary.
- **Self-closing SVG elements** — `<path d="..." />` works in HTML5 but `<path d="..." >` without `/>` does NOT close properly.
- **Base64 in CSS counts differently** — a CSS class with base64 background appears once in CSS but renders N times. Check both definition count and usage count.
- **Section numbering drift** — once a PART divider page (no numbered h2) breaks the sequence, ALL subsequent sections can shift by 1 without a matching adjustment in HTML comments.
