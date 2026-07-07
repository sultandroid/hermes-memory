# Samaya Formal Plan — Exhibition Design System (Naval/Sky/Green)

**Source of truth:** `OneDrive/Samaya/Technical Office/_Style-Guides/Samaya-Formal-Plan-A4-Style-Guide.md`
**Reference template:** `OneDrive/Samaya/Technical Office/_Style-Guides/_A4-print-template.html`

This design system applies to ALL Type B (Exhibition/Museum) HTML technical proposals. Do NOT use the older red/factory design system or the deprecated bronze/gold palette for exhibition work.

## Color Palette

| Token | Hex | Usage |
|-------|-----|-------|
| `--primary` | `#0F172A` | Navy — table headers, section headings, cover bg, RACI-R, cat-row |
| `--secondary` | `#0284C7` | Sky blue — h2-bar, RACI-A, section numbers, accent icons |
| `--accent` | `#16A34A` | Green — cover keyline, pass badges, RACI-C |
| `--fail` | `#B91C1C` | Red — critical badges, reject loops in SVGs |
| `--warn` | `#92400E` | Amber — medium-risk badges, high-risk card borders |
| `--pass` | `#15803D` | Dark green — low-risk badge, pass disposition |
| `--text-main` | `#1E293B` | Body text |
| `--text-muted` | `#64748B` | Captions, metadata, footnotes, footer |
| `--border` | `#E2E8F0` | Table grid, hairline dividers, strip borders |
| `--bg-light` | `#F8FAFC` | Zebra stripes, strip backgrounds, muted fills |
| White | `#FFFFFF` | Page background, table text on navy headers |

## Font Stack

| Purpose | Family | Weight(s) |
|---------|--------|-----------|
| EN headings | `'Montserrat', sans-serif` | 700, 800, 900 (UPPERCASE) |
| EN body | `'Inter', sans-serif` | 400, 500, 600, 700, 800 |
| AR text | `'IBM Plex Sans Arabic', sans-serif` | 500, 600 |
| Metadata / mono | `'Menlo', 'Monaco', monospace` | (system defaults) |

## CSS Component Classes

### Page Layout
```css
.page { width:210mm; height:297mm; padding:12mm 16mm; overflow:hidden; margin:6mm auto }
@page { size:A4 portrait; margin:0 }
```

### Page Header
```html
<header class="page-header">
  <div class="header-info">PROJECT · TP REV 01 · SECTION N</div>
  <div class="header-logo">SAMAYA</div>
</header>
```
- `border-bottom: 2px solid var(--primary)`
- Breadcrumb on left, logo on right

### Page Footer
```html
<footer class="pg-footer">
  <span class="dc">DOC-REF · Rev 01</span>
  <span class="ctx">Section Title</span>
  <span class="pg-num">PAGE N / TOTAL</span>
</footer>
```
- Positioned `absolute; bottom:10mm; left/right:16mm`
- Grid with 3 columns: doc ref, context, page number
- Mono font, uppercase, muted text

### Section Header Row
```html
<div class="h2-row">
  <div class="h2-bar"></div>
  <h2>Section Title</h2>
  <span class="disposition-chip">CHIP · REV 01</span>
</div>
```
- `h2-bar`: 10px × 32px sky-blue vertical strip
- `disposition-chip`: mono uppercase bordered label, auto-margin-left

### Banner (Sub-Section)
```html
<div class="banner">
  <b>N.1 Sub-Section Title</b>
  <span>Arabic translation</span>
</div>
```
- Flex align-baseline row with border-bottom

### Engineering Strip
```html
<div class="strip">
  <div class="strip-hdr">SECTION LABEL</div>
  <div class="strip-grid">
    <span class="strip-tag">Key</span><span>Value</span>
    ...
  </div>
</div>
```
- `border-left: 3.5px solid var(--primary)`, 1px border around

### Snapshot Cards (Metrics)
```html
<div class="snapshot">
  <div class="snapshot-card">
    <div class="lbl">LABEL</div>
    <div class="val">VALUE</div>
    <div class="cap">Caption</div>
  </div>
  <div class="snapshot-card snapshot-card--pass">...</div>
  <div class="snapshot-card snapshot-card--high">...</div>
</div>
```
- Top border color variants: default (navy), `--pass` (green), `--high` (amber)

### Engineering Table
```html
<table class="eng-table">
  <thead><tr><th>Header</th>...</tr></thead>
  <tbody>
    <tr><td>...</td>...</tr>
    <tr class="cat-row"><td colspan="N">CATEGORY</td></tr>
  </tbody>
</table>
```
- Navy header row with white text
- Zebra stripes on even rows
- `cat-row`: navy full-width with white mono text

### Badges
```html
<span class="badge badge-pass">COMPLIANT</span>
<span class="badge badge-critical">HIGH</span>
<span class="badge badge-high">MED</span>
<span class="badge badge-warn">ADVISORY</span>
<span class="badge badge-low">LOW</span>
```
- Mono font, 2px border-radius, compact padding
- Colored backgrounds matching semantic meaning

### RACI Badges
```html
<span class="raci raci-r">R</span>  <!-- navy bg -->
<span class="raci raci-a">A</span>  <!-- sky bg -->
<span class="raci raci-c">C</span>  <!-- green bg -->
<span class="raci raci-i">I</span>  <!-- muted bg + border -->
```
- 16×16px squares, mono font, 2px radius

### SVG Wrapper
```html
<div class="svg-wrap">
  <svg viewBox="0 0 680 300">...</svg>
</div>
```
- `border: 1px solid var(--border); border-radius: 2px; padding: 4px`

### Cover Page
```html
<section class="page page-cover">
```
- Navy `#0F172A` full-bleed background
- White text throughout
- Green `var(--accent)` keyline on title left border
- Document ref in top-right corner (mono, green text)
- Client/project meta strip with navy-tinged white bg
- Bottom strip with party icons + Samaya company info

### Dense Variant
```html
<section class="page compact">
```
- Use `.compact` on the class when tables risk overflowing A4
- Reduces internal padding/spacing further

## Required SVG Charts (6 minimum)

1. **Execution Workflow** — phases 1-7 with concurrent overlap bars + reject loop
2. **Issue Escalation** — 3-level pyramid (Site → PM → Steering) with resolved/close-out branches
3. **Quality Control Workflow** — review gates with reject loop
4. **Organisation Chart** — 14+ positions in hierarchy (Project Director → PM → Discipline Managers → Site)
5. **Master Gantt Chart** — 7 phases + 4 long-lead procurement bars, 9-month timeline
6. **Risk Probability×Impact Heatmap** — 5×5 matrix with green/yellow/red cells + top risks table

## Verification After Build

```python
checks = {
    "Navy primary": "#0F172A" in html,
    "Sky secondary": "#0284C7" in html,
    "Green accent": "#16A34A" in html,
    "Montserrat heading": "'Montserrat'" in html,
    "Inter body": "'Inter'" in html,
    "IBM Plex Arabic": "'IBM Plex Sans Arabic'" in html,
    "Menlo mono": "'Menlo'" in html,
    "A4 page model": "210mm" in html and "297mm" in html,
    "pg-footer class": "pg-footer" in html,
    "page-header class": "page-header" in html,
    "h2-bar class": "h2-bar" in html,
    "disposition-chip": "disposition-chip" in html,
    "eng-table class": "eng-table" in html,
    "SVG count >= 6": html.count("<svg") >= 6,
    "Section count >= 14": html.count('<section class="page') >= 14,
}
# Check forbidden elements
forbidden = ["Playfair", "Tajawal", "#C4A265", "#8B7355"]
for f in forbidden:
    assert f not in html, f"FORBIDDEN: {f} still in file"
```

## Pitfalls

- **CSS @import must be FIRST** inside `<style>` — before `@page` and any selector
- **No Playfair Display** — use Montserrat for headings
- **No Tajawal** — use IBM Plex Sans Arabic for Arabic
- **No bronze/gold palette** — the deprecated exhibition design system used `#8B7355`/`#C4A265`. These are WRONG for HTML formal plans
- **No box-shadow on content** — screen-only allowed for context
- **Border-radius max 2px** — not 4px, 6px, or 8px
- **Footer numbers must match section IDs** — after any structural change, verify all page numbers
- **Zero financial data in technical proposals** — no SAR, $, price, cost, pricing anywhere
