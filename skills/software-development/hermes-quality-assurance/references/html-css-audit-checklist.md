# HTML/CSS Quality Audit Checklist (merged from html-css-audit skill)

## 1. Fetch Raw Source
Never trust rendered summaries — fetch raw HTML source via `curl -sL` and read in sections.

## 2. Tag Balance Check
Count opening vs closing tags for ALL container elements. Generate mismatch table.

**CRITICAL: Every page file must have exactly 1 `<section>` and 1 `</section>`.** A missing `</section>` causes the assembler to swallow ALL subsequent files.

```python
for f in page_files:
    sections = open(f).read().count('<section')
    closes = open(f).read().count('</section>')
    assert sections == closes == 1, f'{f}: {sections} opens vs {closes} closes'
```

Also verify each file has exactly 1 `<footer>` and 1 `</footer>`.

## 3. Section Numbering Drift
HTML comment markers (`<!-- SECTION N: -->`) should match visible `<h2>N.</h2>` numbers. Flag first mismatch.

## 4. Inline Style Audit
Count `style="` occurrences. High count (>50) means CSS classes bypassed. Cross-check for properties duplicated in both CSS class and inline style.

## 5. Duplicate ID Check
Parse all `id="..."` values and flag duplicates with Python `Counter`. Breaks anchor linking.

## 6. CSS Structure
- All `<style>` blocks in `<head>`, never `<body>`
- CSS comments consistent
- No unused CSS classes
- Print rules exist: `@page`, `@media print`, `break-inside`, `page-break-inside`
- CSS custom properties actually consumed, not orphaned

## 7. Print CSS Correctness
- `@page { size: A4 portrait; margin: 10mm }`
- `break-after:page` on each page section
- `break-inside:avoid` on tables, cards, badges, strips
- `thead { display: table-header-group }` for repeating table headers
- `a[href]:after { content: "" }` to suppress link URLs in print
- `-webkit-print-color-adjust: exact` for background colors
- Absolute-positioned footers need `bottom: Xmm` + sufficient page padding-bottom

## 8. Performance
- Single HTML file >200KB — flag it
- Repeated base64 data URIs (logos repeated per page)
- Inline SVG with hundreds of path nodes
- Multiple Google Fonts with many weight variants

## 9. Accessibility Basics
- `<html lang="..."` and `dir="..."` set correctly
- Semantic landmarks: `<main>`, `<nav>`, `<article>`, `<aside>`
- No interactive elements without accessible names
- RTL documents: `dir="rtl"` on parent, `dir="ltr"` on embedded English/numeric content

## 10. RTL Edge Cases
- Numeric content (prices, model numbers, specs) in RTL context needs `dir="ltr"` wrapping
- Mixed Arabic/English abbreviations need `unicode-bidi: embed` or explicit dir

## Pitfalls
- `html.count('class="page"')` overcounts — "page" also matches "page-header", "pg-footer". Use regex with word boundary.
- Self-closing SVG elements — `<path d="..." />` works in HTML5 but `<path d="..." >` without `/>` does NOT close properly.
- Base64 in CSS counts differently — a CSS class with base64 background appears once in CSS but renders N times.
- Section numbering drift — once a PART divider page (no numbered h2) breaks the sequence, ALL subsequent sections can shift by 1.
