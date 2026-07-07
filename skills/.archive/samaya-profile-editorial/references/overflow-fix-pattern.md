# Overflow Fix Pattern — Samaya Profile

## Current Approach (Post-v6.1)

The profile is A4 print-ready. Pages that should fit on one sheet use:

```css
height: calc(210mm - 22mm - 14mm);  /* = 174mm content area */
overflow: hidden;
```

This clips content that exceeds 174mm — the correct behavior for a print profile. CSS classes that have this constraint:

- `.proj-sectorial .content` — sectorial index pages
- `.proj-org .content` — org chart
- `.v4-replica-gallery .content` — replica gallery
- `.v4-cmyk .content` — CMYK/print pages (grid-based, 8-row)
- `.v3-toc .content` — table of contents
- `.v3-method .content` — QA/QC method
- Various `.proj-flagship .content`, `.ed-spread .content`

## When Content Overflows

If a page has more content than fits 174mm, choose ONE of:

1. **Compact** — reduce font sizes, padding, gaps (preferred)
2. **Curate** — remove weaker elements (photos, cards) 
3. **Split** — add a second page for remaining content
4. **Let clip** — if the overflow is footer/marginal content, let `overflow:hidden` handle it

Do NOT remove the height constraint unless the page intentionally spans multiple A4 sheets (currently: none — all pages are single-sheet).

## Verify Page Sizes

```bash
# Check which pages have height constraints
grep -rn 'height: calc(210mm' v6/css/*.css
grep -rn '210mm' v6/css/*.css | head -20
```

## Common Overflow Causes

- **Too many project cards** (sectorial index: 24K chars, 105 SVGs, 29 images)
- **Large SVG content** (org chart: 14K chars in SVG alone)
- **Dense photo grids with inline captions** (replica gallery)
- **Font size too large for content density** (TOC entries: reduce from 12pt→9pt, 9.5pt→8pt)
