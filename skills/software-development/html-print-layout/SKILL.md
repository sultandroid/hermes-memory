---
name: html-print-layout
description: "Fix HTML for A4 print: measure rendered page overflow, split content across pages, and verify every page fits before reporting done. For dense tabular deliverable trees, registers, and specification schedules."
triggers:
  - "pages overflow / content exceeds A4"
  - "print layout is broken / text clipped"
  - "need to split a large HTML table across multiple pages"
  - "page sizes not accurate"
  - "A4 formatting for deliverables"
  - "proposal HTML / tender document / RTL proposal"
  - "TOC needs icons and category groups"
  - "page anchors for navigation"
  - "table / card spacing too large / compact design"
  - "formal design style / no extra colors / Samaya HTML style"
  - "steel spec conventions / galvanizing vs epoxy"
  - "cement board 12mm / material datasheet page"
  - "print PDF from React app / createPortal / print button in modal"
  - "A4 landscape with photos"
  - "raw HTML fragment / bare <section> with no document structure"
  - "HTML snippet exported from another tool, needs wrapping as print document"
  - "restructure monolithic HTML into build pipeline / partials / manifest"
  - "break apart a huge HTML file into separate section files"
  - "build pipeline for A4 document with section numbers and page numbering"
---

# HTML Print Layout — Fixing Page Overflow

## MANDATORY — Load Samaya Document & Engineering-Chart Framework

Before creating ANY formal HTML engineering document for Samaya, you MUST load the **Samaya Document & Engineering-Chart Framework v1.0** (`skill_view(name='html-print-layout')` alone is not sufficient). The framework defines:

- **CSS design tokens** (`--primary`, `--secondary`, `--accent`, chart colors)
- **Auto-engine** for page numbers, multi-level numbering, TOC/LoF/LoT, cross-references (§4)
- **Chart library** — SVG line/spline/area/radial/ring/gauge + CSS bars/KPI/range (§5)
- **100+ page architecture** — parts, chapters, sections, sub-sections (§3)
- **Page anatomy** — every page is `<section class="page">` with header/body/footer (§2)

**Framework location:** `~/Library/CloudStorage/OneDrive-SAMAYAINVESTMENT/Samaya/Technical Office/_Style-Guides/Samaya-Document-Engineering-Chart-Framework-v1.0.md`

**GOLDEN RULES (§0):**
1. One page = one `<section class="page">` — independent blocks
2. Nothing numbered by hand — engine computes from `data-*` attributes
3. All color from `:root` tokens — never hard-code hex (except `--c1…--c8`)
4. Charts are SVG/CSS only — no external libs, no canvas
5. Bilingual: EN baseline, AR as sub-titles + RTL blocks
6. This framework is the single source of truth

**Legacy resources** (for backward compat with existing docs):
- Engineering Template v2.0 style guide at `_Style-Guides/`
- Samaya HTML print template at `references/samaya-html-print-template.md`

> **For ALL NEW documents, use the Framework v1.0 above. Only fall back to legacy resources when patching existing documents that predate v1.0.**

## When to Use

Any HTML document that renders larger than A4 in print preview or browser, especially:
- Raw HTML fragments exported from design/BIM tools — bare `<section>` or `<div>` with no `<html>`, `<head>`, or CSS
- Single unbroken HTML blocks that need splitting across multiple A4 pages
- Tabular deliverable trees / registers with 50+ rows
- Dense specification schedules
- Multi-page A4 reports built as stacked <div class="sheet"> elements
- Any HTML where `min-height: 297mm` is set but content exceeds it

## Prerequisite: Set Correct Print CSS

Before measuring or splitting, **ensure the `@media print` / `@page` rules are correct**. Missing `size:A4` is the #1 cause of print distortion.

### Print CSS Pattern

```css
@media print {
  @page { size: A4 portrait; margin: 10mm 12mm; }
  body { padding: 0 !important; background: #fff !important; }
  .page, .sheet {
    width: 100% !important;
    min-height: auto !important;
    margin: 0 !important;
    border: none !important;
    box-shadow: none !important;
    border-radius: 0 !important;
    overflow: visible !important;
    page-break-after: always !important;
    padding: 10mm 12mm !important;
  }
  .deck { gap: 0 !important; width: 100% !important; }
}
```

Key rules:
- `size:A4 portrait` tells the browser the paper target
- `overflow:visible` prevents content clipping on print
- `background:#fff` strips decorative gradients
- `width:100%` overrides fixed-px widths that break on print
- Always pair with `!important` to beat inline styles

## Quick Estimation: Line-Equivalent Density Check

Before browser rendering, estimate page density with a Python scan:

```python
import re
text = re.sub(r'<[^>]+>', ' ', page_html)
text = re.sub(r'\s+', ' ', text).strip()
lines_est = len(text) / 60  # ~60 chars per line at 0.5rem
# A4 portrait usable area ~52 line-equivalents at normal density
# Flag if >52:
if lines_est > 52:
    print(f'OVERFLOW: ~{int(lines_est)} line-equivalents')
```

**Accuracy note:** This is a ballpark filter. Line-equivalents ≠ rendered lines (tables with many columns wrap differently, SVGs compress text, images take space). Use as triage before browser measurement. 50-52 is borderline, >52 almost always overflows.

**From this session:** page 4 had 81 line-equivalents and indeed overflowed. After splitting at table boundaries (Tier 1 / Tier 2 / Specialist), each sub-page dropped to ≤45.

## Core Technique: Browser-Based Measurement

Never guess page fit. Use `browser_console` to measure actual rendered sheet heights:

```javascript
// Measure all sheets — supports both .sheet and <section class="page"> patterns
const pages = document.querySelectorAll('.sheet, section.page');
Array.from(pages).map((s, i) => {
  const h = s.offsetHeight;
  const expected = Math.round(297 / 25.4 * 96); // ~1123px for A4 at 96dpi
  const status = h > expected + 5 ? 'OVERFLOW +' + (h - expected)
    : h < expected - 5 ? 'UNDERFLOW -' + (expected - h) : 'OK';
  return `Page ${i+1}: ${h}px ${status}`;
}).join('\\n')
```

This is the ONLY reliable detection method. Do NOT estimate from line counts, byte sizes, or hardcoded mm-per-row values — rendered text wraps unpredictably per font/browser.

### A4 Reference Dimensions

| Property | Portrait (mm) | Portrait (px @96dpi) | Landscape (mm) | Landscape (px @96dpi) |
|----------|--------------|---------------------|----------------|----------------------|
| Page width | 210mm | ~794px | **297mm** | **~1123px** |
| Page height | 297mm | ~1123px | **210mm** | **~794px** |
| Header overhead (compact) | ~24mm | ~91px | ~20mm | ~76px |
| Footer bar | ~14mm | ~53px | ~14mm | ~53px |
| **Usable height for content** | **~259mm** | **~979px** | **~176mm** | **~665px** |
| Usable height with 5mm @page margin | ~245mm | ~925px | ~166mm | ~627px |
| Image max-height (A4 landscape print) | — | — | **~110mm** | ~417px |
| **Image max-height (A3 landscape print)** | — | — | **~200mm** | ~756px |

### When A4 Can't Fit — Switch to A3

If the content (image + header + footer + labels) exceeds A4 landscape's ~166mm usable height, switch to **A3 landscape** (420×297mm, usable ~245mm). This doubles the available space with no CSS structure changes:

```css
@media print {
  @page { size: A3 landscape; margin: 5mm; }
  .print-page { width: 100%; box-sizing: border-box; page-break-after: always; }
}
```

**Trade-offs:** A3 requires the user to print on A3 paper or scale to fit when printing on A4. Most PDF viewers handle A3 → A4 scaling gracefully. Update the print wrapper `maxWidth` accordingly:

```tsx
<div className="print-wrapper" style={{ width: '100%', maxWidth: '420mm' }}>  {/* was 297mm */}
```

**Image containers** can be `height: 200mm` with `object-fit: contain` — image fits without cropping. Hotspot pins stay aligned because `contain` centers the image and both pages use identical dimensions.

## React Print with createPortal

For apps using React with Vite, the print overlay can be a React component rendered via `createPortal` directly to `document.body`. This keeps the print content outside the app's stacking context and simplifies CSS scoping.

### Pattern

```tsx
// PrintView.tsx
import { useEffect, useRef } from 'react';
import { createPortal } from 'react-dom';

export default function PrintView({ ... }) {
  const imgRef = useRef<HTMLImageElement>(null);
  const printedRef = useRef(false);

  useEffect(() => {
    if (printedRef.current) return;
    printedRef.current = true;
    const img = imgRef.current;
    if (img) {
      img.onload = () => { setTimeout(() => window.print(), 400); };
      if (img.complete) { setTimeout(() => window.print(), 400); }
    } else {
      setTimeout(() => window.print(), 400);
    }
  }, []);

  useEffect(() => {
    const afterPrint = () => onClose();
    window.addEventListener('afterprint', afterPrint);
    return () => window.removeEventListener('afterprint', afterPrint);
  }, [onClose]);

  return createPortal(
    <>
      <style>{`
        @media print {
          body > :not(.print-wrapper):not(style) { display: none !important; }
          .print-wrapper { display: block !important; }
          @page { size: A4 landscape; margin: 0; }
          .print-page { page-break-after: always; }
          .print-page:last-child { page-break-after: auto; }
        }
      `}</style>
      <div className="print-wrapper">
        {pages.map(p => (
          <div key={p} className="print-page">/* page content */</div>
        ))}
      </div>
    </>,
    document.body
  );
}
```

### Key rules

1. **No `position: fixed` on `.print-wrapper`** — browser can't paginate fixed elements across pages
2. **Each page is a plain `<div>`**, not a flex container — `page-break-after` works only on block-level elements
3. **`page-break-after` goes in a CSS class**, not inline — CSS class selectors are more reliable in `@media print`
4. **Portal to `document.body`** — ensures print content is a direct child of `<body>` so `body > :not(.print-wrapper)` selectors work
5. **Trigger `window.print()` after image load** — use `img.onload` + `setTimeout(400)` fallback
6. **Close overlay with `afterprint` event** — `window.addEventListener('afterprint', onClose)` to restore the app after printing
7. **Image max-height** — constrain with `maxHeight: '16cm'` for landscape, `maxHeight: '24cm'` for portrait. `height: 'auto'` alone causes overflow

### Wiring in the parent component

```tsx
// In the gallery/modal component:
const [showPrint, setShowPrint] = useState(false);

// Overlay div wrapping PrintView:
{showPrint && (
  <div style={{ position:'fixed', inset:0, zIndex:10000, background:'#fff' }}>
    <PrintView
      viewTitle={gallery.title}
      imageSrc={view.filename}
      hotspots={displayHotspots}
      materials={matMap}
      rev="A"
      date={new Date().toLocaleDateString('en-GB',{day:'2-digit',month:'short',year:'numeric'})}
      onClose={()=>setShowPrint(false)}
    />
  </div>
)}
```

The outer fixed overlay ensures the print content covers the screen before `window.print()` fires. The `@media print` CSS then hides everything except `.print-wrapper`.

### Real-World Row Heights (Aseer Museum, 279-row deliverable tree)

| Content type | Avg row px | Max rows per A4 page |
|---|---|---|
| C-category children (long descriptions) | ~46px | ~20 |
| C-category parents (short descriptions) | ~39px | ~23 |
| Stage 5-6 (short descriptions) | ~33px | ~27 |
| Stage 5-6 parents (one-liners) | ~28px | ~32 |

Formula: `max_rows = 920 / measured_avg_row_height`

## Step-by-Step Workflow

### 0. Diagnose — is this a proper document or a bare fragment?

Before doing anything, check if the file has the scaffolding needed for print:
- `<html>` tag present?
- `<head>` with `<style>` containing `@page` or `@media print` rules?
- Page wrapper elements (`.sheet`, `<section class="page">`, `.page`)?

**Detection script:**
```python
import re
with open(filepath) as f: c = f.read()
report = {
    'has_html_tag': '<html' in c,
    'has_head_tag': '<head>' in c,
    'has_atpage': '@page' in c,
    'has_media_print': '@media print' in c,
    'has_sheets': '.sheet' in c or '.page' in c,
    'has_section_page': '<section class="page"' in c,
    'has_page_break': 'page-break-after' in c or 'break-after' in c,
    'has_overflow_rule': 'overflow' in c,
}
```

**If the file is a bare fragment** (no `<html>`, no `<head>`, no print CSS):
1. Do NOT try to patch or re-wrap inline — the file is not a page-structured document
2. Build the full document from scratch: wrap content in `<!DOCTYPE html><html><head>...</head><body>...</body></html>`
3. Add print CSS with `@page { size: A4 portrait; margin: 0; }`, `.sheet` wrapper class, and `@media print` rules
4. Identify natural split points in the content (group markers, category headers, table sections) — there are no `.sheet` divs to measure
5. Split content into sheets at those boundaries, one `class="sheet"` per split
6. Add doc-strip footer with page numbering, `page-break-after: always`, and `overflow: hidden` on each sheet
7. Verify div balance, card/element count, and sequential page numbers

**Key difference:** With a bare fragment, you are *authoring the structure* not *repairing overflow*. The overflow is a consequence of no structure existing. Every `.sheet` is a new creation, not a resize.

### 1. Parse the document structure

Identify all `.sheet` divs (or their equivalent `.page` sections). Each represents one A4 page in the printed output.

Find natural split boundaries within overflowing sheets:
- Category headers (`<!-- ===== CATEGORY X ===== -->`)
- Parent rows (`<tr class="cat-header">`)
- Individual data groups (e.g., `C01`, `C02` parent rows)

### 2. Measure rendered row heights per section type

Run in browser console, targeting each overflowing sheet:

```javascript
function measureRows(sheetIndex) {
  const s = document.querySelectorAll('.sheet')[sheetIndex];
  const t = s.querySelector('table');
  const rows = Array.from(t.querySelectorAll('tr'));
  const dataRows = rows.filter(r => r.cells[0]?.textContent?.trim().match(/^[A-Z]\d/));
  const avg = dataRows.reduce((s,r) => s+r.offsetHeight, 0) / dataRows.length;
  return { total: rows.length, data: dataRows.length, avg: Math.round(avg) };
}
```

Use the measured avg to compute max_rows per page for that section type.

### 3. Split at natural boundaries

**Category trees (e.g., Cat C with C01-C15 sub-items):**
- Parse each `<tr><td class="ref">C{xx}</td>` parent row as split point
- **IMPORTANT — include the full `<tr>` tag:** search for `<tr><td class="ref">C{xx}</td>`, not just `C{xx}</td>` or the opening tag is lost
- Group adjacent chunks so each sheet ≤ computed max rows
- Combine small adjacent groups when total fits (e.g., C07+C08 = 18 rows)

**Stage sheets with multiple categories (Stage 5 H-K, Stage 6 L-O):**
- Find `<!-- ===== CATEGORY X ===== -->` HTML comments
- Group categories: H+I, J+K, L+M, N+O (each ~15-21 rows)
- Each group gets its own sheet with distinct h2 title

**Cover pages with dense info boxes:**
- When the cover overflows by 30-55px, add CSS targeting `.sheet:first-of-type`
- Use `[style*=...]` attribute selectors with `!important` to override inline styles:

```css
.sheet:first-of-type > div[style*="border"],
.sheet:first-of-type > div[style*="background"] {
  font-size: 5.5pt !important;
  line-height: 1.15 !important;
  padding: 0.6mm 1mm !important;
}
```

Use broad `[style*="border"]` rather than `[style*="border:.4pt"]` — inline style formatting varies. Always pair with `!important` against inline styles.

### 4. Rebuild each sheet

Each new sheet needs:
1. `<!-- ===== SHEET N - Title ===== -->` comment
2. `<div class="sheet">` wrapper
3. Docstrip header (`<div class="doc-strip">...</div>`)
4. `<h2>` title
5. `<table>` with proper `<thead>` and `<tbody>`
6. Category header row(s) if applicable
7. Data rows
8. `</tbody></table>`
9. Footer with correct page number (`SHEET N/TOTAL`)
10. `</div>`

**Critical: strip existing wrapper before re-wrapping** (content extracted from already-processed files may carry old wrappers):

```python
def strip_wrapper(html):
    html = re.sub(r'<div class="doc-strip">.*?</div>', '', html, count=1, flags=re.DOTALL)
    html = re.sub(r'<div class="doc-strip".*?SHEET.*?</div>', '', html, count=1, flags=re.DOTALL)
    html = re.sub(r'^<div class="sheet">', '', html.strip())
    html = re.sub(r'</div>\s*$', '', html.strip())
    return html.strip()
```

### 5. Renumber all pages

Update every footer to `SHEET {n}/{total}`. Strip entire old footer divs — don't just replace numbers, or stale `/10` or `/6` remains inside the old tag.

### 6. Verify in browser

```javascript
const allOk = Array.from(document.querySelectorAll('.sheet'))
  .every(s => s.offsetHeight <= 1124);
console.log(allOk ? 'ALL SHEETS FIT A4' : 'OVERFLOW REMAINS');
```

## Definition of Done — DO NOT skip

Never report "fixed" or "done" from estimates. Before claiming completion, you MUST:

1. **Render** the final HTML in a real browser (or print-to-PDF).
2. **Measure** every `.sheet` with the verification snippet below — not just the ones you edited.
3. **Confirm zero overflow:** every sheet `offsetHeight <= 1124px`. If any sheet overflows, it is NOT done — split further and re-measure.
4. **Visually inspect each page** (PDF preview) for clipped text, dangling rows, or blank pages.
5. **Renumber** all footers `SHEET n/total` and confirm the count matches the actual sheet count.

```javascript
// Final gate — paste in browser console on the rendered document
const pages = document.querySelectorAll('.sheet, section.page');
const bad = Array.from(pages).map((s,i) => ({i:i+1, h:s.offsetHeight}))
                  .filter(x => x.h > 1124);
console.log(bad.length === 0
  ? `ALL ${pages.length} PAGES FIT A4`
  : 'OVERFLOW: ' + bad.map(b => `Page ${b.i} (${b.h}px)`).join(', '));
```

Only after this gate prints `ALL N SHEETS FIT A4` may you report the task complete.

## Pitfalls

| Pitfall | Consequence | Fix |
|---|---|---|
| **Raw HTML fragment — no document structure** | File is just a bare `<section class="page">` or `<div>` with inline styles — no `<html>`, `<head>`, `@page`, or print CSS. Browser shows one unbroken page. | Run Step 0 detection first. If it's a fragment, build full document from scratch with `<!DOCTYPE html>`, `@page A4 portrait`, `.sheet` wrappers, and page breaks. Do NOT try to patch CSS onto a file that has no structure. |
| Hardcoding row height (e.g., 4mm) | Every sheet overflows | Measure actual rendered heights in browser |
| Searching for `C{xx}</td>` without `<tr>` prefix | Parent row loses opening tag, whole sheet HTML breaks | Search for `<tr><td class="ref">C{xx}</td>` |
| Re-wrapping content with existing wrapper | Double `<div class="sheet">`, broken layout | Strip old wrapper before re-adding |
| Using specific `[style*="border:.4pt"]` selector | Doesn't match if inline style formatting differs | Use broad `[style*="border"]` with `!important` |
| Replacing footer numbers instead of stripping footer | Stale page number remains in old footer text | Strip entire docstrip footer div |
| Regex `<!-- ===== SHEET \d` (single digit) | Misses 2-digit sheet numbers (10+) | Use `<!-- ===== SHEET \d+` |
| Ignoring cat-header row height in budget | Sheets with many category headers overflow | Add ~20px per cat-header to overhead |
| Dangling `<tr>` at end of slice | Broken HTML in the next section | End slice at the start of the next `<tr>`, not mid-tag |
| **Orphaned doc cards after page split** | Rogue `<div class="doc-card">` without wrapping `<div class="docs-grid">` appears on wrong page — breaks layout | Always remove the entire grid block (heading + grid wrapper + cards) together. Strip old wrapper before re-inserting. |
| **Clientsig moved to last page** | الطرف الأول still exists on old page AND new page — duplicate | After moving, verify `content.count('الطرف الأول') == 1` across the entire file |
| **Closing block duplicated** | وتفضلوا بقبول appears twice (once on old page, once on new page) | After moving, verify `content.count('وتفضلوا بقبول') == 1` |
| **`.sign` div without closing `</div>`** | Footer starts before sign-block is closed | Every `<div class="sign">` must be matched by a `</div>` before the `<footer>` |
| **CSS custom property with url() on HTML inline style** | `--v3-img:url('../path.jpg')` defined as HTML inline style on `<section>` but resolved relative to the CSS file when used via `var(--v3-img)` — browser resolves the URL from the CSS file directory, not the HTML file. Works in some browsers, breaks in others (especially print/PDF rendering). | Set `background-image` directly via inline `style` on the target element. Avoid CSS custom properties containing `url()` that cross between HTML and CSS files. |
| **Subagent creates SVG placeholder images instead of using real photos** | SVG placeholders are 1-color blocks that look broken. User notices immediately and asks to replace. | Always tell subagents explicitly: "Use ONLY real existing photos from the assets directory. Do NOT create placeholder or SVG images." Add this to every design delegation prompt. |
| **Section-split page renumbering cascade** | When splitting a `<section class="page">` into two, all subsequent page numbers shift by 1. Simple `replace()` loops cascade — replacing PAGE 05 to 06, then 06 to 07, eventually all become the last number. | Renumber in **reverse order** (highest page number first) or use a single-pass regex substitution per page. After renumbering, verify all footers are sequential 1..N with no gaps and the total matches. |
| **Rewriting sourced content in disposition tables** | User explicitly flagged: "dont rewrite cg comment should be as is." When updating a CG Comment Disposition Matrix or similar table, the source comment text (from CG, consultant, authority) must never be summarized, shortened, or rephrased. Only the disposition/action column (your response) may be updated. | **Never modify the comment/requirement column** in disposition tables. Only change the disposition, status, or ref columns. Compare against the original (Rev 03 or earlier) to verify comment text is unchanged. |
| **Column width balancing before page splitting** | Jumping straight to page-split when a table overflows creates unnecessary extra pages and breaks page flow. Often the overflow is caused by uneven column widths — e.g. the CG Comment column at 132px when it should be the widest column. | Before splitting, try **adjusting column widths** first. The content/comment column should be the widest (2x the others), the disposition/action column narrower. Swap widths so the column with the longest text gets the most space. Verify fit again before splitting. |
| **Verbose status notes in registers** | User flagged verbose text like "TBC · Target: CP-2 Decision · Per KP Register Rev C02" as too wordy. | Keep it short: "TBC · CP-2 Decision" is sufficient. Drop redundant register references when the context is clear. |
| **Subagent overwrites source file during audit** | Delegate_task subagent wrote test HTML over the actual source file (289KB → 31KB) while performing a TOC audit. The file had no git backup and no local copy. | **Always create a backup before delegating file manipulation.** Before calling delegate_task on any file, do: `cp <file> <file>.bak`. If the file is critical, also add: Restoring from OneDrive version history or a prior Rev file is possible but loses all unsaved changes. |
| **`crossorigin` on both `<script>` AND `<link>` tags breaks on Hostinger/LiteSpeed** | Vite builds add `crossorigin` attribute by default on `<script type="module">` and `<link rel="stylesheet">` tags. Hostinger (LiteSpeed) does not send `Access-Control-Allow-Origin` headers. With `crossorigin`, the browser silently refuses to execute the module script AND may fail to load the stylesheet. The error is silent — no console error message, just a generic `js_errors: [{message: "", source: "exception"}]` in the accessibility snapshot. | Regenerate `dist/index.html` and remove ALL `crossorigin` attributes from BOTH `<script>` AND `<link>` tags before deploying: `sed 's/ crossorigin//g' dist/index.html`. Test locally with `python3 -m http.server`. The app works correctly without `crossorigin` on same-origin assets. |
| **Inline `<style>` tag via `createPortal` doesn't always apply `@media print` rules** | The print dialog may open before the browser processes the dynamically-inserted `<style>` tag, causing unstyled print output. | Place ALL `@media print` rules in the app's main CSS file (`index.css`), loaded at page start. Remove the inline `<style>` tag from the portal component entirely. |
| **Not setting `@page { size: ...; margin: 0 }`** | Browser defaults override A4 dimensions, causing inconsistent layouts and unexpected page breaks. | Always set explicit `@page { size: A4 portrait; margin: 10mm; }` or `size: A4 landscape; margin: 0;` in the `@media print` block. |
| **React flex containers block `page-break-after`** | Browsers cannot split CSS flex containers across printed pages. `page-break-after: always` is ignored when the parent uses `display: flex` with `minHeight` or `flex: 1`. | Use pure block-level `<div>` elements for page sections. Move `page-break-after` to a CSS class applied via `@media print` rather than inline. |
| **Image `height: auto` causes page overflow in print** | Images with `height: auto` (default) use their natural dimensions, which can exceed the printable area and cause additional unwanted pages. | Constrain with `maxHeight: 16cm` (A4 landscape) or `maxHeight: 24cm` (A4 portrait) to account for header/footer height. Always pair with `object-fit: contain`. |
| **`object-fit: contain` on annotated image breaks hotspot pin alignment (screen view)** | When hotspot pins use percentage-based positioning (`left: ${x}%, top: ${y}%`) over a **dynamically-sized image** (screen modal with `max-width: 75vw`), `object-fit: contain` adds letterboxing that shifts the image's visible area relative to the container. Pins appear at wrong locations. | Use `object-fit: cover` on annotated/hotspot images for **screen tooltip/modal views**. The image fills the container completely (cropped if needed), so percentage-based pin positions align with the visible area. |
| **`object-fit: cover` on annotated image for PRINT breaks pin alignment (opposite!)** | In **print view** (fixed-height container, e.g. `height: 155mm; overflow: hidden`), `object-fit: cover` crops the image differently than what the user sees on screen, causing percentage-based pins to drift. | Use `object-fit: contain` for **print pages**. The image scales to fit within the fixed container without cropping, so pin positions stay consistent. The container `overflow: hidden` clips any letterbox spill. |
| **Not setting `print-color-adjust` causes colored elements to print as white/blank** | Browsers omit background colors and dark elements in print mode by default. Samaya's dark header bar, gold pins, and table row highlights print as white. | Add `* { -webkit-print-color-adjust: exact; print-color-adjust: exact; }` in the `@media print` block. |
| **Vite build hangs / times out when project lives on OneDrive (large JSON data files)** | `npm run build` (which runs `tsc -b && vite build`) times out because TypeScript or Rollup tries to read/process large JSON files in `src/data/` hosted on OneDrive's cloud sync layer. The files are valid data, not git-ignored. | Use Vite's JavaScript API directly: create a `build.mjs` file (`import { build } from 'vite'; await build(); console.log('done');`) and run `node build.mjs`. This bypasses the `tsc -b` step entirely (which is fine — `noEmit: true` in tsconfig means tsc only type-checks, not produces output). The API build also avoids the CLI's extra file scanning. |\n| **OneDrive file locking blocks all write operations** | When OneDrive is running, files in `~/Library/CloudStorage/OneDrive-*/` can return `Operation not permitted` on `open()`, `cp`, `ls`, and all terminal/file tools. Killing OneDrive processes (`killall -9 OneDrive`) may not release the lock — the File Provider extension re-locks immediately. | Quit OneDrive from the menu bar icon (right-click → Quit). If that doesn't work, ask the user to manually copy the folder to `/tmp/` or Desktop using Finder, work there, then copy back. If the user has a micro SD card mounted at `/Volumes/MIcro/`, copy to `/Volumes/MIcro/Temp/` instead — it doesn't have OneDrive's lock issues. Do NOT keep retrying the same failing path — it won't unblock. |
| **Not checking companion documents for same data** | Updating SMP specialist data but not the Resource Plan leaves stale info live. Same data (Graphics vendor, Structural CV status, ICT Security Integrator) appears in both. | Before deploying any plan update, grep companion documents for the same terms. If they exist, update both. |
| **Overflow estimation from line-count alone is fuzzy** | 50 line-equivalents can fit or overflow depending on table column count, SVG height, and card grids. Stripped text at 60 chars/line ignores image heights and multi-column tables. | Use line-equivalents only as triage (>52 = almost certainly overflow). For definitive check, render in browser and measure with `element.offsetHeight`. |
| **Splitting at mid-table breaks the table** | Cutting a table between rows requires rebuilding both halves with proper `<thead>` headers and `<tbody>` tags. The split point must be at a `<tr>` boundary. | Split at natural boundaries: between tables (each table is independent), not inside one. If a single table is too big, consider compacting fonts or merging with adjacent content instead. |\n| **`page-break-inside: avoid` on page wrapper + `page-break-after: always` creates blank pages** | Content barely overflows → browser pushes ENTIRE block to next page (can't break inside), then `page-break-after: always` adds another break → blank page appears. | Remove `page-break-inside: avoid` from outer page container. Apply `break-inside: avoid` to INNER groups (`.print-page > div { break-inside: avoid }`) instead. Let the page wrapper break naturally at page boundaries. |
| **Table column widths collapse without `table-layout: fixed`** | Tables with many columns (5+) auto-size columns based on content, causing narrow columns to be too wide and wide columns to be too narrow. Text wraps unpredictably, causing page overflow. | Always set `table-layout: fixed` on the `<table>` and define explicit `width` percentages via `<colgroup><col style="width:XX%">...</colgroup>`. Sum must equal 100%. Apply to ALL tables in the document, not just overflowing ones. |
| **Section page breaks missing** | Sections flow continuously without page breaks, causing content from different sections to share a page. | Every `<section class="page">` must have `page-break-before: always` (or `break-before: page`). The first page (cover) and TOC should NOT have page-break-before — use `:first-child` or manual class to skip. |
| **Tables split across page boundaries** | A tall table starts on one page and continues on the next, splitting rows mid-content. | Set `page-break-inside: avoid` on `<table>` elements. For tables that are genuinely too tall for one page, split the table at a natural `<tr>` boundary into two separate tables, each with its own `<thead>`. Never let a single `<table>` span a page break. |\n| **Fixed `mm`/`px` column widths overflow on print pages** | Using fixed widths like `width: '50mm'` or `width: 120px` for table columns can overflow the printable width when the page size changes (A3 vs A4) or margins differ. | Use **percentage-based** column widths instead: `#: 3%`, Code: `18%`, Description: `flex: 1`, Finish: `15%`, Colour: `14%`, Supplier: `12%`. Total = 100% — never overflows. Header and data rows must use identical percentages. |\n| **Footer `position:absolute;width:100%;left:16mm;right:16mm` overflows** | Width computes to page width + offset = 210mm + 16mm = 226mm. The `width:100%` overrides the auto-width from `left+right`. | Remove `width:100%` from footer rule. `position:absolute` with `left+right` already computes the correct width. |\n| **RTL footer text overflows left** | Arabic text (`المكتب الفني`, `محدود`) in an LTR footer grid pushes past the left boundary. | Add `direction:ltr` to each footer span. Set `text-align:left` for first span, `text-align:center` for middle, `text-align:right` for last. Add `overflow:hidden` to the footer container. |\n| **Extra filler rows in legend/register tables waste space and cause overflow** | Adding placeholder rows with alternating backgrounds to "fill" the page pushes actual data rows down and can exceed the page height. | Render ONLY actual data rows. Let the page background (`#F5F1EB`) fill the remaining space naturally. Remove all `minHeight`, flex fillers, and fake row loops. The alternating row background pattern stops with the last data row — the user prefers this over forced empty rows. |\n| **`minHeight` on page wrapper exceeds printable area** | Setting `minHeight: 260mm` (or similar) on a page's flex container forces the content to be taller than the available A3/A4 space minus header/footer/labels. The page overflows and creates blank trailing pages. The `minHeight` was intended to fill the page background but instead pushes content past the page boundary. | Remove `minHeight` entirely. Let content grow naturally. The page background (`#F5F1EB` or `#E8E3DB`) in the `@media print` CSS already fills the full @page area — no flex hacks needed. |
| **`position:absolute` + `width:100%` on footer overflows page** | Footer has `position:absolute; left:16mm; right:16mm` (auto-width = page width minus offsets) plus `width:100%` (overrides auto-width to equal containing block width). Result: footer width = 210mm (parent) + 16mm left offset = 226mm, overflows page by 16mm right. Happens when two CSS rules define the same selector — first rule sets `left/right`, second adds `width:100%` without removing the offsets. | Remove `width:100%` from the footer rule. `position:absolute` with `left` + `right` already computes the correct width between those bounds. Never add `width:100%` on top. Search for duplicate `.pg-footer` or `footer` CSS rules and merge into one definition. |
| **Node.js `fs.readFileSync` times out on macOS with multi-file concat** | When reading 49+ HTML files (one per page, total >600KB) in a Node.js loop, `fs.readFileSync` can take 45+ seconds on macOS — far slower than Python's `open()`. The terminal tool timeout (30s) kills the process before it finishes. | Use Python for all file-I/O-heavy build scripts. Python's `open()` reads the same files in <1 second. Switch assemble scripts from `scripts/assemble.js` → `scripts/assemble.py`. Update `package.json` to run `python3 scripts/assemble.py`. |
| **Pixel-based column widths break on A4** | Using `width:60px` or `width:22px` for table columns works in screen view but can overflow or misalign on A4 print where the page width is fixed at 210mm. | Convert all pixel widths to percentages (e.g., `60px` → `8%`, `30px` → `5%`). Percentages always sum to 100% and never overflow the printable area. This is especially important when adding `table-layout:fixed` — unwidthed columns split equally, which is rarely desired. |
| **Pre-existing h2-row split across page boundary** | Original HTML has `<div class="h2-row"><div class="h2-bar"></div>` opening on page N but `<h2>...</h2><span>chip</span></div>` closing on page N+1 outside any `<section>` tag. Mechanical splitting by `<section>` boundaries produces: page N = empty with orphaned div start; page N+1 = bare `</div>` + h2 with no section wrapper. | Before splitting, scan for incomplete structural divs near `</section>` boundaries. Reconstruct: page N gets its own complete h2-row with a proper title; page N+1 gets a fresh `<section class="page">` wrapper with its own header + h2-row. |
| **SECTION comment numbering drift survives splitting** | Source HTML has `<!-- SECTION 17: ... -->` comment but the matching `<h2>` says `16. Title`. The comment-to-h2 mapping is off-by-N due to earlier edits or skipped section numbers. Splitting by `<section>` boundaries preserves the drift — the comment number stays wrong in the partial. | After splitting, renumber all SECTION comments to match the h2 text number before writing partials. Find each `<!-- SECTION N: -->`, check the next `<h2>M.` — if M != N, fix the comment to read M. |
| **SVG `width="auto"` causes browser console error** | `<svg width="auto" height="40">` — SVG `width` attribute expects a length (e.g. `100%`, `40px`), not `auto`. Chrome logs: `Error: <svg> attribute width: Expected length, "auto".` The attribute has no effect; the browser defaults to 300x150. | Remove `width="auto"` entirely. Use CSS for sizing: `style="width:auto;height:40px"` or a numeric width value. Grep for `width="auto"` before final validation — expect zero occurrences. |
| **Literals `§` in SVG `<text>` elements survives `&sect;` replacement** | Python `str.replace('&sect;', 'Sec.')` only catches HTML entity `&sect;`. Literal Unicode `§` characters inside SVG `<text>` elements (e.g. `SoW §5.5`) are NOT caught because they are raw Unicode, not HTML entities. After bulk replacement, 5+ literal `§` can remain in SVG text nodes, producing mixed output like `SoW Sec.5.1.2 - ER §2.6.B`. | After `&sect;` → `Sec.` replacement, grep for literal `§` (Unicode U+00A7) in the file. These are typically in SVG `<text>` elements. Replace each with `Sec.` individually. Verify with `grep -c '§' file.html` — must be 0. |
| **Over-compacting pages that have space** | Applying `xtight` to every page makes sparse pages look cramped and hard to read. The user explicitly rejected uniform compaction across all pages. | Measure each page's content density (`table_rows * 12 + text_len * 0.03 + svgs * 100`). Only apply `xtight` to pages at >75% usage. Use `compact tight` (less aggressive) for pages at 50-75%. Use no compaction classes (or just `compact`) for pages under 50%. Check each page individually — never blanket-apply xtight. |
| **Verbose internal notes in stakeholder descriptions** | User rejected details like "CV submitted", "PQD under submission", "PO issued Jun 21", "Fee 40,527 approved", "Target: CP-2 Decision", "Per KP Register Rev C02", "waiting object research from client" in stakeholder registers. These are internal tracking notes CG doesn't need. | Stakeholder descriptions should state only: role title, person/firm name, and status if relevant (e.g. "TBD", "Approved", "Vacant"). Drop all procurement/fee/register-reference detail. If CG needs the detail, it goes in the external CR sheet or procurement register, not the plan itself. |
| **CG comment disposition belongs in external CR sheet** | Embedding full CG comment-by-comment disposition in the plan wastes 2+ pages and goes stale immediately. User explicitly said: "CR sheet we make it excel file only." | Replace the full disposition table with a 4-row summary spec-strip: Round 1 count, Round 2 count, CG Approval reference, and a note saying "Full disposition per attached CR sheet." Do NOT include the 2-page comment table in the plan. |

## Merging Pages and Compacting Content

When the user asks to reduce page count — whether a document "has a lot of white space" or they ask "why can't pages X and Y be on one page" — the fix involves either: (a) moving content off a sparse page and deleting it, or (b) compacting the denser table on a content-bearing page to fit alongside content from an adjacent page.

### Merging Two Content-Bearing Pages by Compacting

When both pages have unique content (not just a sparse signature block), the approach is different from the sparse-page workflow:

1. **Identify the denser content block.** Usually one page has a large table (e.g. 14-row neighbors list) and the other has a smaller table (e.g. 8-row support equipment list). The denser block is the one that needs compacting.

2. **Compress the dense table's font size.** Reduce font size by ~35–40% to create room:
   - Table: `font-size: 0.76rem → 0.48rem` (works for 14 rows of 4-column text)
   - Intro paragraph above table: `font-size: 0.84rem → 0.5rem`
   - Reduce margins around the table: `margin: 3px 0 6px 0 → 2px 0 4px 0`

3. **Remove the page break between the two sheets:**
   - Delete the first page's footer (`<footer>`) and closing `</div>`
   - Delete the second page's opening `<div class="sheet">` and `<header>`
   - Merge into one `<div class="sheet">` with a combined header title
   - Keep the second page's footer with updated page number

4. **Renumber all subsequent pages.** Use index-based footer replacement (see Renumbering section below) — do NOT use simple forward or reverse `str.replace()`.

5. **Update all cross-references:**
   - TOC page numbers (e.g. `p. 07 → p. 06`, `p. 08 → p. 07`, etc.)
   - Cover/title page total (e.g. `Page 01 of 20 → Page 01 of 19`)
   - All footer page totals (`/20 → /19`)
   - HTML comment headers (`<!-- PAGE 07 ... --> → <!-- PAGE 06 ... -->`)

6. **Verify in browser** that the merged page renders without overflow.

**Trade-off:** Compacting a dense table to 0.48rem makes it harder to read but eliminates a whole page. The user explicitly prefers this over wasted white space. If the dense table has very long text (e.g. "Prince Faisal Bin Khalid Cardiac Center"), the text wraps within narrower cells and remains legible.

### Removing Unwanted Blocks and Deleting Sparse Pages

### Typical sparse-page candidates

- Signature / approval continuation pages with only a few signature cells
- Appendix pages that are just one image + caption
- Short subsections that spilled onto their own sheet because of an earlier split
- Blocks that are not client-facing (e.g. source attribution, internal acceptance grids)

### Workflow

1. **Remove the unwanted block first.** Patch it out of the HTML and verify the page still renders.
2. **Identify whether the remaining content on that page fits on an adjacent page.** Use the browser measurement snippet above. If the combined height is ≤ usable A4 height, merge.
3. **Move the content** before the footer of the target page (usually the preceding page in the same section).
4. **Delete the now-empty `<div class="sheet">`** and its header/footer.
5. **Renumber without cascade errors.** Simple forward or reverse `str.replace()` loops on page numbers do **not** work: replacing `PAGE 10 → 09`, then `11 → 10`, then `12 → 11` collapses every later page into `09`. Use an index-based replacement over the actual footer elements instead. Example:

   ```python
   import re
   target_pages = {i: f'PAGE {i+2:02d} / 20' for i in range(19)}
   target_pages[19] = 'PAGE B1 / B1'

   def replace_footers(match):
       replace_footers.counter += 1
       idx = replace_footers.counter
       inner = match.group(1)
       if idx in target_pages:
           inner = re.sub(r'<span class="pg-num">PAGE [\dB]+ / [\dB]+</span>',
                          f'<span class="pg-num">{target_pages[idx]}</span>', inner)
       return '<footer class="pg-footer">' + inner + '</footer>'
   replace_footers.counter = -1

   html = re.sub(r'<footer class="pg-footer">(.*?)</footer>', replace_footers, html, flags=re.DOTALL)
   ```

6. **Update the cover doc-strip total** (e.g. `Page 01 of 22` → `Page 01 of 21`).
7. **Update the TOC page ranges** (e.g. Approval p. 18–19 → p. 18; Appendix A p. 20–22 → p. 19–21).
8. **Regenerate page comments** so there is exactly one comment per `<div class="sheet">`. Strip all existing `<!-- ================= PAGE ... ================= -->` comments first, then insert a clean comment before each sheet opening.
9. **Verify:** every sheet should have exactly one footer, page numbers should be sequential, and all sheets must fit A4.

### Renumbering pitfalls

| Pitfall | Why it breaks | Fix |
|---|---|---|
| Reverse `replace()` loop on `PAGE N / total` | Replacing 21→20, then 20→19, etc., turns every page into the lowest number | Use index-based footer replacement |
| Forward `replace()` loop | Replacing 10→9, then 11→10 also collapses pages | Use index-based footer replacement |
| Only updating footers, not comments | Sheets and comments get out of sync | Strip and regenerate comments by sheet index |
| Only updating numbers, not cover/TOC totals | Cover says "of 22" while footers say "/ 21" | Update cover doc-strip and every TOC page range |
| Leaving an orphaned page comment after deleting a sheet | Comments > sheets | Regenerate comments after structural changes |
| **Global `/20` → `/19` replacement matches base64 image data** | The pattern `/20` appears in base64-encoded image strings, corrupting embedded images when using a blanket `str.replace()` or `sed` substitution across the entire file. | Use targeted replacement only on footer page numbers. For total updates, either: (a) update each footer individually, or (b) use regex anchored to `PAGE XX /` context, or (c) use index-based footer replacement. After any global string replacement, verify no image rendering regressions. |

### Client-facing cleanup

If a block exposes internal process or data sources (e.g. "Neighbors located from ... using OpenStreetMap data"), replace it with client-facing wording ("site context") and remove source attribution from the deliverable body. Keep the actual data (neighbors, coordinates) if it is relevant to the scope.

## Page Content Balancing Between Pages

When a CG disposition table (or similar wide content) spans two pages, the split point must be chosen for visual balance, not just page-fullness.

Technique:
1. Measure line-count per comment — longer comments need more space.
2. Move the split boundary so each page has roughly equal visual weight.
3. Extract <tr> blocks from page A's </tbody> and insert before page B's first data <tr>.
4. Re-measure both pages after each adjustment.

Example — CG CRS Table:
- P4: 8 Round 1 + CRS-01 to CRS-08 (cramped) → Move CRS-07/08 to P5
- P5: CRS-09 to CRS-17 (light) → Becomes CRS-07 to CRS-17 (balanced)

## Compact + Tight + XTight CSS Class Pattern

For dense register/specification pages, cascade three classes:
<section class="page compact tight xtight">

- compact = reduces internal padding/margins (~15% height save)
- tight = further reduces font size: 0.34rem on register tables
- xtight = maximum compaction: 0.38rem table font, 1px cell padding, 0.7rem h2, 20px h2-bar, 3px header margin

Font reduction ladder:
- (none) 0.42rem → compact 0.39rem → compact tight 0.37-0.34rem → xtight 0.38rem (table) + 0.7rem (h2)

For 20+ rows, also reduce the role/scope column font.

### xtight CSS definition
```css
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

Apply to pages with 25+ table rows or heavy content that overflows even with compact+tight. Place the CSS in the document's `<style>` block and add the class to the `<section>` tag.

### Progressive Compaction — Don't Over-Compact Sparse Pages

When pages have different content densities, apply compaction proportionally:
- **>75% usage**: `compact tight xtight` (maximum compaction)
- **50-75% usage**: `compact tight` (moderate compaction)
- **<50% usage**: `compact` only (light compaction) or no class

Check each page individually — never blanket-apply xtight to all pages. The user will notice and reject over-compacted pages with plenty of space.

```python
# Python check for per-page compaction
table_rows = len(re.findall(r'<tr', page_content))
text_len = len(page_content)
svgs = len(re.findall(r'<svg', page_content))
est_height = text_len * 0.03 + table_rows * 12 + svgs * 100
available = 1972  # A4 usable px
pct = est_height / available * 100

if pct > 75:
    classes = 'compact tight xtight'
elif pct > 50:
    classes = 'compact tight'
else:
    classes = 'compact'
```

### Progressive Padding Cascade for Mixed-Content Pages

When a page has multiple content blocks (intro text + card grid + table + text box), use a **progressive padding cascade** that gets tighter for denser content:

```
Block type        Outer padding    Inner padding     mb
─────────────────────────────────────────────────────────
Group-level       4px  8px         2px               4px
Tier 1 / cards    6px 10px         3px  6px (card)   5px
Tier 2 / table    4px  6px         1px  4px (cell)   4px
Tier 3 / text     3px  7px         —                 4px
Page itself      10mm 14mm         —                 —
```

Pattern: as content density increases, reduce both outer padding and spacing to the next block. Cards get 3px 6px, table cells get 1px 4px (via `!important` override — see below), plain text blocks get 3px 7px.

### Page-Specific Table Cell Override with !important

When global CSS sets `td { padding:4px 7px }` but a specific table has 17+ rows and needs to fit A4, use a page-local `<style>` block with `!important` to override only that page's cells:

```html
<section class="page" style="padding:10mm 14mm;">
  <style>
    .page-sectionX td { padding:1px 4px !important; line-height:1.25 !important; }
    .page-sectionX th { padding:2px 4px !important; }
  </style>
  ...
  <div class="page-sectionX">
    <table>...</table>
  </div>
  ...
</section>
```

The `!important` is necessary because inline styles on individual `<td>` elements would otherwise be required to beat the global CSS rule — a `<style>` block is cleaner. The class `.page-sectionX` scopes the override so it doesn't leak to other pages.

### Intro Text Condensation

When the page has an italic introductory paragraph that's too long:
- Remove date stamps ("Updated Jun 2026. Org chart showing..." → "Three tiers active throughout...")
- Drop filler words ("The org chart shows the" → just state the fact)
- Keep the regulatory anchor (SoW §5.5, MoC approval requirement)
- Reduce font size: 0.5rem → 0.48rem
- Reduce line-height: 1.4 → 1.35

### Card Grid Compaction for Varying Content Heights

When cards in a grid have unequal content (e.g., 3 short cards + 1 with an extra sub-line):

**Before (4-column, breaks alignment):**
```html
grid-template-columns: 1fr 1fr 1fr 1fr; gap: 8px;
padding: 5px 8px; font: 0.5rem labels / 0.6rem names
```

**After (2x2, all same height):**
```html
grid-template-columns: 1fr 1fr; gap: 4px;
padding: 3px 6px; font: 0.42rem labels / 0.55rem names
```

The 2x2 layout gives each card ~2× the horizontal space at A4 width, preventing text wrapping in the role labels. The BIM Manager card with an extra sub-line (Arch. BIM Lead) no longer makes a single column taller than its peers.

## CG Disposition Table Conventions

When building or fixing CG comment disposition matrices in A4 HTML, follow these rules:

### Column Width Priority
The comment column must be the widest since it carries the longest text:
- Round: 65px (for "R2 · 2-Jun" without clipping)
- CG Comment: 250px (the widest — 2x the disposition column)
- Disposition: 120px (short responses)
- Status: 65px
- Route / Scope: 90px

### Never Rewrite Sourced Text
The comment/requirement column must be preserved verbatim - even typos are part of the original CG record. Only update the disposition/action, status, or ref columns.

### Reference Attached CR Sheet for Approved Rounds
When a CG comment disposition matrix has been previously approved, do NOT repeat the full comment-by-comment table in the new revision. Replace with a summary box showing round count, closure status, CG approval reference, and a note that the full CRS spreadsheet is attached. This saves 2+ pages and avoids stale comment text.

### Remove Explanatory Blocks
Do NOT include Status Legend, Route/Scope definitions, Outstanding Submittals, or Notes blocks below the CG disposition matrix. The column headers and status badges are self-explanatory. These blocks add clutter and risk page overflow.

### Standardize Across Tables
Ensure # columns are 40px, Date columns 80px, and Status columns 90px across all tables in the same document for visual consistency.

### Document-Level Conventions for SMP-Style Plans

These rules apply when building or updating any Stakeholder Management Plan, CG-facing document, or similar A4 report. See `references/aseer-smp-conventions.md` for the full conventions reference including document numbering, revision history rules, QC sign-off chain, name format, CG disposition table standards, stakeholder count update checklist, and abbreviation definitions.

**Revision History — Formal Submissions Only**
Only include revisions formally submitted to CG. Internal drafts and iterative refinements between submissions must not appear in the revision history table. Each entry must have real names in Prepared/Approved columns — not "Samaya PMO" or "Per live KPR."

**QC Sign-off — Real Names, Clear Chain**
QC sign-off tables must use real names, not "Per live KPR." Structure as: Prepare → Register → Review → Approve. Every role gets an actual person's name.

**Name Reference Pattern**
For roles where an approved name exists in the live register, use: **Name · Per live KPR** (e.g. "Eng. Mohamed Ahmed · Per live KPR"). For vacant/TBC roles, state the status without the register reference.

**Register Total Count Updates**
When adding or removing roles, update all occurrence counts across the document: TOC chip, tier coverage summaries, and register total lines. There are typically 3-4 count locations.

**TOC Cleanliness**
The TOC snapshot chip should show sections, pages, and roles only — not CG comment counts or other metadata. Keep it focused on what the document contains.

**COVERED vs CLOSED**
- CLOSED = CG confirmed resolution (use for Round 1, historically closed items)
- COVERED = addressed in this revision but CG hasn't reviewed (use for Round 2 SMP-scope items)
- SUBMITTAL-PENDING = depends on external submittals (use for items needing DS/PQD)
- Items needing external submittals must NOT be marked CLOSED/COVERED

## Sub-Task Approach for Page Redesigns

When the user asks to redesign a page with specific sub-tasks, do NOT apply all changes in one large edit. Break into small controlled sub-tasks with verification after each step.

### Pattern

```
Sub-Task 01 — Page identity (header, title, footer)
Sub-Task 02 — Fix section order / layout
Sub-Task 03 — Improve specific component
...
Sub-Task N — Final QA checklist
```

After each sub-task: visually review the page, confirm alignment and readability, then continue. The user specifically requested this workflow for page redesigns.

## Cover Photo Reliability

### Problem: CSS custom properties with url() don't cross file boundaries reliably

When a cover photo is set via `--v3-img:url('../assets/img/photo.jpg')` on an HTML element and consumed via `background-image: var(--v3-img)` in a CSS file, the URL resolves relative to the CSS file, not the HTML file. This causes the image to not load in some rendering contexts.

### Fix: Direct inline style

```html
<div class="v3-photo-img" style="background-image:url('assets/img/photo.jpg');"></div>
```

Also update the CSS fallback to match the same image:

```css
background-image: var(--v3-img, url('../../assets/img/photo.jpg'));
```

This ensures the primary render path (inline style) works everywhere, while the CSS variable path serves as a fallback for any CSS-only overrides.

## TOC Categories & Page Anchors

For multi-page A4 proposals, categorize the TOC into logical groups with icons:

**4 standard groups:** Project Introduction · Technical Scope · Execution Plan · Company & Commercial

Each group gets a `<div class="toc-group-label">` with a dashed border-top separator. Each `.toc-item` gets a Unicode icon span before the number.

### Page Anchor IDs

Every page section gets a sequential `id="page-N"` for TOC anchor links:

```python
import re
page_num = 0
for i, line in enumerate(lines):
    if '<section class="page' in line:
        page_num += 1
        line = re.sub(r'\s+id="[^"]*"', '', line)  # strip stale id
        lines[i] = line.replace('<section class="page',
            f'<section class="page" id="page-{page_num}"')
```

TOC items link to `#page-N` via `<a href="#page-N" style="text-decoration:none;color:inherit">` — the inline style preserves visual appearance.

**Watch for double-quote bugs:** `id="page-7""` (extra "). Always strip existing id before inserting.

### TOC Grouping Rules

1. Merge "Technical Specifications" + "Material Datasheets" into ONE TOC entry — datasheets are sub-pages under specs, not a separate section.
2. After merging, TOC goes from 12 items to 11 items.
3. TOC count excludes the Cover (page 1) and the TOC itself (page 2).
4. See `references/technical-proposal-structure.md` for full CSS and icon map.

## General Conditions List Compacting

When the terms list (`<div class="terms"><ol><li>...</li></ol></div>`) takes too much vertical space on A4:

```css
.terms ol li {
  padding: 3px 0;         /* down from 7px */
  font-size: 9px;          /* down from 11px */
  line-height: 1.4;        /* down from 1.55 */
  display: grid;
  grid-template-columns: 26px 1fr;  /* narrower counter column */
  gap: 6px;                /* down from 10px */
}
.terms ol li::before {
  font-size: 8px;          /* counter size */
  padding: 1px 4px;        /* counter badge padding */
}
```

This reduces the vertical footprint by ~40% while remaining readable for Arabic legal text.

## Spec-Table Tightening

When a spec table on an A4 page looks too spacious:

```css
.spec-table th, .spec-table td {
  padding: 2px 8px;  /* down from 3px 10px — viable for dense AR/EN tables */
}
```

Tighter than 2px risks readability. For even more space, reduce the inner `<span style="font-size:10.5px">` font size. Pair with `.ds-table` at 4px 10px and `.gantt-row` at 6px 14px for consistent density (see `references/technical-proposal-structure.md` for the full batch).

## Surge.sh Deployment Workflow

### Deploy from a temp directory — never from OneDrive

```bash
rm -rf /tmp/surge-deploy
mkdir -p /tmp/surge-deploy/proposal_assets
cp index.html /tmp/surge-deploy/
cp proposal_assets/* /tmp/surge-deploy/proposal_assets/
surge /tmp/surge-deploy/ 'project-name.surge.sh'
```

OneDrive paths cause unreliable CDN behavior (504 errors). Always stage in `/tmp/`.

### Credential management

`surge whoami` to check auth. If token is invalidated (e.g. by accidentally running `surge --logout`), use two-argument form to redeploy — it reauthenticates. **Never run `surge --logout`** — it breaks all future deployments until the user re-enters their password.

### CDN propagation delay

After "Success! Published to domain.surge.sh", the site may return 504 for 10-30s while CDN edge nodes propagate. This is normal — wait and retry. Do NOT redeploy or teardown.

### URL-encoded filenames in deployment

When HTML references files with URL-encoded spaces (`Oddy%20Test_Lab.jpg`) but the actual file on disk uses literal spaces (`Oddy Test_Lab.jpg`), the deploy script must decode the destination path, not just the source:

```python
c = rp.replace("../", "", 1)          # "../assets/img/file.jpg" → "assets/img/file.jpg"
sp = os.path.join(src, c)             # source path on disk
dc = unquote(c)                        # DECODE the RELATIVE path — turns %20 into space
dp = os.path.join(dst, dc)            # use decoded path as destination

# Source might also need decoding
if not os.path.isfile(sp):
    sp = unquote(sp)                   # also try decoding source

os.makedirs(os.path.dirname(dp), exist_ok=True)
shutil.copy2(sp, dp)
```

The key: Surge decodes URL paths before file lookup. If the file is stored with `%20` in the filename, Surge looks for the literal-space version and returns 404. Always deploy with **decoded** filenames.

### Verify deploy (reliable method)

`tail -n` or `tail -3` may miss the Success message due to Node.js stderr noise. Use:

```bash
surge /tmp/dir/ --domain x.surge.sh 2>&1 | grep -E 'Success|Published|error'
curl -s -o /dev/null -w "%{http_code}" "https://x.surge.sh/"
```

### Duplicate image detection after bulk replacements

After replacing multiple images (e.g., bulk HQ photo swap), verify no image appears more than once:

```python
import re
from collections import Counter
with open("index.html") as f:
    html = f.read()
refs = Counter(re.findall(r'\.\./assets/img/[^"\')\s]+', html))
dupes = {k:v for k,v in refs.items() if v > 1}
assert len(dupes) == 0, f"{len(dupes)} duplicate images remain"
```

### Creating PDFs from deployed HTML

Browser print (Ctrl+P) → Save as PDF with A4, margins set to "None" in print settings. The `@media print{@page{size:A4 portrait}}` rule handles the rest.

## A4 Height Enforcement (Critical) — NO FLEX ON .page

Do NOT use `display:flex; flex-direction:column` on `.page` containers. Flex layout distributes leftover vertical space, pushing content DOWN from the title and creating white space between the title and body content. The user explicitly rejected this across multiple iterations.

**Use block layout only:**
```css
.page { position: relative; width: 210mm; height: 297mm; ... }
```
Content flows naturally from top to bottom. The `.h2-row` has `margin-bottom:6px` which provides sufficient spacing after the section title.

**If a page has too little content to fill A4:** add more content (KPIs, data tables, detail paragraphs) rather than using flex to stretch. The user prefers real content over artificial spacing.

The #1 cause of overflow in flex-based A4 pages:

### Rule: every `flex: 1` child needs `min-height: 0`

```html
<div style="display:flex;flex-direction:column;flex:1;min-height:0">
  <div style="flex:1;min-height:0">
    <img src="..." style="width:100%;height:100%;object-fit:contain">
  </div>
</div>
```

Without `min-height:0` on flex children, `flex:1` sub-flex-items grow past the parent's A4 boundary.

### Rule 2: every `.content` block needs explicit `height`

Many page types use `overflow: hidden` but have no `height` constraint. **Always add:**

```css
.page-type .content {
  height: calc(210mm - 22mm - 14mm);  /* A4 landscape height minus header/footer */
  overflow: hidden;
}
```

### Image containment within A4

- Use `height:100%` not `height:auto` (auto uses natural dimensions, causing overflow)
- Always pair with `object-fit:contain` to preserve aspect ratio
- The img's parent needs `flex:1;min-height:0;display:flex`

### Standalone figure images (no flex parent)

For standalone `<div class="figure">` images (not inside a flex container), use a combined max-width + max-height constraint:

```css
.figure img {
  max-width: 100%;
  max-height: 130mm;
  height: auto;
  width: auto;
}
```

This prevents large base64 embedded images from exceeding either the page width (178mm printable) or taking more than ~half the page height. Tested on inline JPEGs up to 2000px native width in A4 portrait layout. For landscape, adjust max-height to ~145mm.

## Multi-Agent Delegation for Samaya HTML Proposals

User established a clear agent routing pattern for Samaya HTML proposal work. Follow this routing for all substantial HTML document tasks:

| Work Type | Delegate To | Rationale |
|-----------|-------------|-----------|
| **SVG charts, timeline graphics, data visualizations** | **Claude** (`claude -p` or delegate_task) | User explicitly said "always delegate charts to claude" |
| **Logo design, branding elements, cover graphics** | **Codex** (`codex exec`) | "fix the cover page logos consult codex on it" |
| **QC review / structural audit** | **Kimie** (`kimi -p`) | "let kimi work as qc in this task" — run structural checks (div balance, page numbers, number accuracy) |
| **Major page redesign, cover from scratch** | **Pi** (`pi -p "high-level prompt"`) | User preference — Pi handles full-page redesigns (covers, complex layouts). Feed it the task spec with all brand colors and constraints. |

### Delegation Protocol

1. **Back up the file first (MANDATORY)** before any delegate_task call: `cp <file> <file>.bak-<date>`. This is not optional — sub-agents can corrupt HTML structure, overwrite logos with placeholders, or duplicate page numbers. After all edits, run final structural verification.
2. **Claude for charts**: Pass the exact file path, current SVG snippet, clear before-after description. Include CSS variables. Claude uses patch() operations.
3. **Codex for logos**: Download official SVG logos from company websites via `curl -o` (not placeholder/created SVGs). Embed with `filter:brightness(0) invert(1)` for dark covers. Verify real SVGs have actual path data, not text-based placeholders.
4. **Kimie for QC**: Check in this order:
   - HTML structure: open vs close `<section>` and `<div>` counts
   - Page numbering: sequential 02-N without duplicates or gaps
   - Numbers: equipment quantities, furniture counts, programme weeks
   - Logos: verify against official sources (not fake/CSS-only SVGs)
   - Report PASS/FAIL in table format with exact evidence
5. **Final structural verification after ALL edits**: Run a Python script checking `<div>` balance, `<section>` balance, page number sequence 02-N. Verify no stale references remain (e.g. "36 أسبوع" when updated to 52).

### Page Number Renumbering Pattern (proven for 44+ footer HTML docs)

Use a `re.sub()` with a closure-based counter for single-pass renumbering:

```python
import re
current_page = 2
def renumber(match):
    global current_page
    result = f'{match.group(1)}صفحة {current_page} / {total}'
    current_page += 1
    return result
html = re.sub(r'(<span class="pg-num">)صفحة \d+ / \d+', renumber, html)
```

This avoids cascade errors from forward/reverse `str.replace()` loops that collapse page numbers (replacing 10→9 then 11→10 turns everything into 9). Works for both Arabic `صفحة` and English `PAGE` patterns.

### Pitfalls from this session

- **Codex may replace official SVGs with fake ones** — after Codex logo delegation, always verify RCRC, BMA, and Samaya logos are the actual SVG paths from the company websites, not placeholder circles/rectangles. Cross-check against `curl` downloads from official URLs.
- **Page numbers fragment after multi-agent edits** — when Claude (charts) + Codex (logos) both modify the file, pages can duplicate or gap. Always run page-number audit as final step.
- **Div balance degrades across sequential delegate_task calls** — each sub-agent may add/remove divs unevenly. Always verify div balance at the end.
- **BMA logo**: official source is `https://www.borismicka.com/images/logo-white.svg` (375x30 viewBox, full Boris Micka wordmark in white paths)
- **RCRC logo**: official source is `https://www.rcrc.gov.sa/wp-content/uploads/2026/06/RCRC-logo-2.svg` (189x41 viewBox, tree/plant emblem in dark green #1D8649)

## Base64 Image Deduplication
### Samaya Logo Base64 Deduplication
When a file embeds the **same base64 image 45+ times** (e.g., Samaya PNG logo in every page header), the file swells to 3-4 MB which causes slow rendering and potential page overflow during print.

**Fix: Move to a single CSS class definition.**

1. Extract the base64 string from one `<img src="data:image/png;base64,...">`
2. Define a CSS class once:
   ```css
   .my-repeated-logo{width:90px;height:14px;display:inline-block;vertical-align:middle;background:url(data:image/png;base64,<b64>) no-repeat center/contain}
   ```
3. Replace every `<img src="data:image/png;base64,...">` with `<div class="my-repeated-logo"></div>`
4. Result: 1 instance of base64 instead of 45 → file drops from ~3.5 MB to ~660 KB

**When to use:** Any HTML document with the same embedded image on every page of a multi-page print document.

**Pitfall:** The base64 may contain characters (`/`, `+`) that break string delimiters. Use raw string literals. Verify the CSS declaration compiles by rendering the page in a browser.

### CSS Rendering as Visible Text — Diagnosis Workflow

When a browser shows CSS code as page content (raw `.class{...}` rules visible), the HTML structure has a tag-boundary error that prevents the browser from properly closing the `<style>` or `<head>` element.

**Three most common causes:**

1. **`</style></head><body>` wrapped in HTML comments** — The sequence `<!-- </style>\n</head>\n<body> -->` looks like valid closing tags to a human but the browser treats everything from `<style>` onward as invisible comment content. Result: the `<style>` tag is NEVER closed, everything after it is inside `<head>`, ALL CSS render as visible text.
   - **Fix:** Uncomment the tags. Remove `<!--` before `</style>` and `-->` after `<body>`. Verify with `grep -n '</head>' file.html` and count exactly 1 occurrence.

2. **CSS text outside any `<style>` element** — When a file has been concatenated (e.g., Part 01 + Part 02 of a proposal), the second copy's CSS may sit raw in the `<body>` without `<style>` wrappers. The browser renders it as text.
   - **Fix:** Wrap the orphan CSS in `<style>...</style>`. Most reliable detection: search for text that starts with `@page{...}`, `.page-cover{...}`, or any CSS rule pattern that appears BEFORE the first `<section>` but AFTER `</head>`. Use `grep -n '^\.[a-z]' file.html | head -20` to find rule text outside style blocks.

3. **Duplicate `</style></head><body>` in file body** — A second copy of these closing tags at some point in the body causes the browser to close the style/head early, with the remaining CSS rules sitting as raw text between the first close and the second close.
   - **Fix:** Delete the SECOND occurrence (the one in the body, not the real head). Verify by counting: `<head>` == `</head>` == 1, `<body>` == `</body>` == 1. If any > 1, the file has duplication.

**Key detection script:**
```python
# Check for all critical HTML boundary tags
counts = {
    '<head>': html.count('<head>'),
    '</head>': html.count('</head>'),
    '<body': html.count('<body'),
    '</body>': html.count('</body>'),
    '<style': html.count('<style'),
    '</style>': html.count('</style>'),
}
# If any count != count of its counterpart, structure is broken
```

**Recovery order after fixing:** fix style/head/body boundary → count `<section>`/`</section>` → count `<div>`/`</div>` → verify SVG charts still render → verify page numbers sequential.

### Duplicate HTML Head/Body Block Fix
When a file has been concatenated (e.g., Part 01 + Part 02) and contains TWO `</style>\n</head>\n<body>` sequences, the browser treats ALL CSS between the first `</style>` (line ~183) and the second `</style>` (line ~771) as raw visible text — the entire CSS block shows as page content.

**Detection:** Count `<head>` vs `</head>` vs `<body>` — if any > 1, there's duplication. Also check `<style>` vs `</style>` balance.

**Fix:**
1. Find the SECOND `</style></head><body>` (usually preceded by `.cover-party-icon` CSS rule)
2. Delete it — the real head/body is the first one
3. Verify: `<head>` == `</head>` == 1, `<body>` == `</body>` == 1
4. Verify: `<style>` opens == `</style>` closes after the fix
5. Verify: `<section>` opens == `<section>` closes

### Cover Party Logos — Transparency on Dark Backgrounds
When placing client/contractor logos on a dark (navy) cover, the `.cover-party-icon` container must NOT have a background color, and the images need inversion to show white:

```css
.cover-party-icon{background:transparent}
.cover-party-icon img{filter:brightness(0) invert(1)}
```

The `filter:brightness(0) invert(1)` converts any image (SVG or PNG) from dark-on-transparent to white-on-transparent — visible on any dark background. Works for both SVG paths and PNG bitmap images.

## Cover Party Logos — Transparency on Dark Backgrounds

When placing client/contractor logos on a dark (navy) cover, the `.cover-party-icon` container must NOT have a background color, and the images need inversion to show white:

```css
.cover-party-icon{background:transparent}  /* was rgba(255,255,255,0.15) */
.cover-party-icon img{filter:brightness(0) invert(1)}
```

The `filter:brightness(0) invert(1)` converts any image (SVG or PNG) from dark-on-transparent to white-on-transparent — visible on any dark background. Works for both SVG paths and PNG bitmap images.

## SVG Title Overflow — Two-Line Titles

When an SVG chart title is too long for its viewBox (e.g. "البرنامج الزمني — 52 أسبوعاً (12 شهراً) · Programme Timeline — 52 Weeks (12 Months)" at 840px viewBox):

**Fix:** Split into two `<text>` elements — Arabic line + English line:

```svg
<text x="420" y="11" text-anchor="middle" font-size="9.5" font-weight="700">البرنامج الزمني — 52 أسبوعاً (12 شهراً)</text>
<text x="420" y="22" text-anchor="middle" font-size="7.5" fill="#475569">Programme Timeline — 52 Weeks (12 Months)</text>
<line x1="25" y1="26" x2="815" y2="26" stroke="#0F172A" stroke-width="0.5" stroke-opacity="0.15"/>
```

Then shift ALL subsequent SVG y-coordinates (month labels, tick marks, week labels, milestone elements) down by the same amount as the gap between the old single-line y and the new divider line y.

**Checklist after title change:**
- Month tick marks (`y1/y2`) shifted
- Month text labels (`y="21"` → `y="31"`) shifted  
- English month labels shifted
- Week labels shifted
- Milestone diamonds/labels shifted
- viewBox height increased to accommodate added vertical space

## Post-Claude-Redesign Overflow Check

After delegating a visual section redesign to Claude Code, always check for **content density overflow**:

1. Claude's redesigned sections are often more detailed than the originals — the BIM integration paragraph, factory capability strip, and spec tables can each be 2-3x longer
2. On a single A4 page, a section with >4500 chars of text content almost always overflows
3. Fix by **trimming verbosity** (not shrinking fonts):
   - Factory strip: remove parenthetical translations, condense equipment lists, drop duplicate qualifiers
   - BIM paragraphs: shorten from 4 numbered steps to a single sentence with arrows (→)
   - Spec tables: reduce from 5+ columns with full material specs to 4 columns with condensed descriptions
   - QC tables: trim standard list to acronyms only (ISO 18916 instead of "PAT (ISO 18916)")
4. After trimming, re-measure in browser (see browser-based measurement section above)

**Rule of thumb:** If a section has >3500 chars of plain text (stripped HTML), it will overflow A4. Aim for <3000 chars after trimming.

- Page visual redesign (e.g., turning a bland card layout into an architectural drawing sheet)
- Logo/header/footer restructuring
- Color and typography refinements
- Icon and badge placement
- **SVG chart creation and fixing** — Gantt timelines, bar charts, progress diagrams (user preference: always Claude for charts)

When delegating: pass the exact file path, current HTML snippet, and a clear "before after" description. Include the CSS variables in use. Claude Code will use patch() operations. **Always back up the file before delegating** (`cp file.html file.html.bak`). After Claude returns, verify page numbering and div balance — Claude's patches can shift div counts or create page number duplicates.

## Monolithic HTML → Maintainable Build Pipeline

When a single HTML file has grown to 700KB+ (49+ A4 pages, inlined CSS, base64 images), patching inline becomes fragile and error-prone. Restructure into a partials + manifest + build-script pipeline.

### Signals
- Single HTML file >300KB with all content inlined
- Page numbers hard-coded as `صفحة N / M` instead of computed
- Section numbering drift visible between comments and h2 tags
- Multiple rounds of patch() already applied and structure is fragile
- User asks for "maintainable" or "restructure"

### Workflow

1. **Backup first.** Copy the live file to a timestamped `.BACKUP-YYYYMMDD/` folder. Include any linked CSS/image assets.

2. **Define a manifest** (`manifest.json`) listing every section/page with:
   - `id` — unique slug for the partial filename
   - `type` — `"cover"`, `"content"`, `"divider"`
   - `title_ar`, `title_en`
   - `short_title_ar` — used in footer context
   - `continued: true` — for multi-page sections that share a number
   - `children` — for subsections (e.g. gallery-level breakdowns)

3. **Extract section content** from the monolithic HTML file into individual partials under `sections/{id}.html`. Each partial must:
   - Be wrapped in `<section class="page">` (or `page-cover` / `page-divider`)
   - Use `{{placeholder}}` tokens for: `section_number`, `page_number`, `total_pages`, `doc_code`, `rev`, `date`, `title_ar`, `title_en`, `short_title_ar`, `chip_text`
   - NEVER hard-code section numbers, page numbers, or totals
   - Include a `<footer class="pg-footer">` with `{{page_number}} / {{total_pages}}`

4. **Design a template** (`template.html`) wrapping the full document:
   - `<!DOCTYPE html>`, `<html lang="ar" dir="rtl">`
   - `<meta charset="UTF-8">`, `<meta name="viewport">`, `<meta name="description">`
   - Google Fonts link
   - `<link rel="stylesheet" href="styles/a4.css">`
   - `<main>{{body}}</main>` — one placeholder for all assembled sections

5. **External CSS** (`styles/a4.css`) — NOT inline `<style>`:
   - `@page { size: A4; margin: 0; }` (NOT `A4 portrait` — Safari-incompatible)
   - `.page { width:210mm; height:297mm; box-sizing:border-box; overflow:hidden; page-break-after:always; }`
   - `print-color-adjust: exact`, `-webkit-print-color-adjust: exact`
   - CSS variables for brand colors
   - Screen-only `box-shadow` for preview, removed in print

6. **Build script** — **Python over Node.js for file I/O**:
   - On macOS, Node.js `fs.readFileSync()` on 300K+ files can timeout due to filesystem monitoring. Python's `open()` is more reliable.
   - **Simple concat approach** (preferred over two-pass build — less fragile):
     - One `base.html` file with DOCTYPE + `<head>` + CSS + closing `</body></html>`, containing `{{BODY}}` placeholder
     - Page partials in `pages/{NN}-title.html`, each a complete `<section class="page">...</section>`
     - `scripts/assemble.py`: read `base.html`, read all page files sorted, join with `\n\n`, replace `{{BODY}}`, write `dist/index.html`
     - Run: `python3 scripts/assemble.py`
   - **Two-pass alternative** (only if dynamic numbering is required):

7. **Validation script** (`scripts/validate.js`) checking at minimum:
   - File exists and size < 800KB
   - All critical HTML structure tags present
   - At least 1 `<h1>`, 1 `<h2>`, `<header>`, `<footer>`, `<section>`
   - `@page` uses `A4` not `A4 portrait`
   - No `SVG width="auto"` anywhere
   - No unfilled `{{placeholder}}` tokens
   - Tag balance for `<div>`, `<section>`, `<svg>`, `<span>`
   - Footer page numbers sequential (skipping cover + dividers)
   - Last footer page number matches total
   - No duplicate page numbers

   See `references/a4-pipeline-build-script.md` and `references/a4-pipeline-validate-script.md` for canonical script patterns.

### Pitfalls specific to this pattern

| Pitfall | Why it breaks | Fix |
|---------|--------------|------|
| **Pre-existing HTML malformations survive page splitting** | The source HTML may have malformed tags where content split across pages (e.g., `<div class="h2-row">` opens on page N but its `<h2>` and `</div>` are on page N+1 outside any `<section>`). Mechanical splitting by `<section>` boundaries produces an empty page N and broken content on page N+1. | Before splitting, scan for pages where the h2-row or other structural divs are incomplete. Manually reconstruct: (1) give page N a proper h2-row with its own title, (2) give page N+1 its own section wrapper + header + h2-row. The original may need structural repair that mechanical splitting cannot handle. |
| **Hard-coded page numbers inside extracted content** | SVG base64 data or old footers retain stale numbers. Build's `{{total_pages}}` replacement never reaches them. | Before build: search all partials for `صفحة \\d+ / \\d+` and `/ \\d+` patterns. Replace every occurrence. |
| **Multi-page sections merged with `<!-- PAGE BREAK -->`** | All sub-pages in one `<section>` → build assigns one page number → duplicate footers. | Split at page-break markers into separate partials. Register each as a child or sequential entry. |
| **Divider pages counted in total but have no footers** | Total includes dividers, footers count only content pages. | Validation must accept gaps for non-footer pages. |
| **Page-number cascade with simple replace()** | Replacing page 5→6 then 6→7 collapses all pages to the last number. | Use closure-based counter in single-pass `re.sub()`. Never use sequential `str.replace()` loops. |
| **Regex tag replacement omits closing `>`** | A regex like `/<section[^>]*class="[^"]*page[^"]*"/g` matches `<section ... class="page">` only up to the final `"` of class — not including `>`. Result: `<section class="page"` with no closing `>`. Browser treats next line as attributes, producing `ection class="page">` as visible text. The leftover `>` from original tag plus replacement's `>` creates `>>` (double angle). | Consume entire opening tag: `/<section[^>]*class="[^"]*page[^"]*"[^>]*>/g`. Replacement must end with `>`. Verify: zero `ection class="page"` AND zero `class="page">>` in output. |

### Standard Section Template (for ALL content pages)

Every regular content page (not cover, not divider) must follow this exact structure:

```html
<section class="page">
  <header class="page-header">
    <div class="header-info">RCRC EXHIBITION | TP {{rev}}</div>
    <div class="header-logo"><div class="samaya-header-logo"></div></div>
  </header>
  <div class="h2-row">
    <div class="h2-bar"></div>
    <h2>{{number}}. {{title_ar}} <span>— {{title_en}}</span></h2>
    <span class="disposition-chip">{{chip}}</span>
  </div>
  <!-- CONTENT: strips, .ar divs, tables, SVGs -->
  <footer class="pg-footer">
    <span class="dc">{{doc_code}} · Rev {{rev}}</span>
    <span class="ctx"><span dir="rtl" style="display:inline">القسم {{n}} · {{short_title}}</span></span>
    <span class="pg-num">صفحة {{page}} / {{total}}</span>
  </footer>
</section>
```

Mandatory elements:
- `<div class="h2-bar">` — the blue accent bar before the heading
- `<span class="disposition-chip">` — label/badge in the top-right
- Arabic text wrapped in `<div class="ar">` for font-family scoping
- Footer with three spans: `.dc` (doc code), `.ctx` (section context), `.pg-num` (page number)

### Simple concat approach (PREFERRED — replaces two-pass build)

**Do NOT use two-pass builds** with Puppeteer, placeholder replacement, and post-processing. These introduce brittle failure modes (timeouts on `file://` URLs, regex `>` stripping, page-count miscounts, section number drift).

**Use the simple concat approach instead:**

1. **`base.html`** — single template with DOCTYPE + `<head>` + inline CSS + closing `</body></html>`, containing `{{BODY}}` placeholder
2. **`pages/{NN}-title.html`** — pre-numbered page files, each a complete `<section class="page">...</section>` with static page numbers already correct
3. **`scripts/assemble.py`** — Python assemble script (NOT Node.js — Python is more reliable for file I/O on macOS; `fs.readFileSync` on Node.js can timeout on macOS with 300K+ files):

```python
#!/usr/bin/env python3
import os, glob
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PAGES = os.path.join(ROOT, 'pages')
DIST = os.path.join(ROOT, 'dist')
files = sorted(glob.glob(os.path.join(PAGES, '*.html')))
body = '\n\n'.join(open(f, encoding='utf-8').read().strip() for f in files)
base = open(os.path.join(ROOT, 'base.html'), encoding='utf-8').read()
output = base.replace('{{BODY}}', body)
os.makedirs(DIST, exist_ok=True)
open(os.path.join(DIST, 'index.html'), 'w', encoding='utf-8').write(output)
```

4. **Why it works:** Since A4 pages use `page-break-after: always`, editing content within a page never changes its page number. Pre-numbered files stay valid. The TOC stays valid. No placeholders, no Puppeteer, no post-processing.

**When to NOT use this approach:** If page content regularly shifts page boundaries (dynamic tables that grow/shrink), use the two-pass build with placeholder tokens. Otherwise, static concat is simpler and more reliable.

### Divider page handling

When splitting a monolithic document, part-divider pages (الجزء الثاني, الثالث, etc.) need distinct rendering from content pages:

- Use `<section class="page page-divider">` with `background: var(--primary)` (dark navy)
- Add corresponding CSS: `.page-divider { background: var(--primary); display: flex; flex-direction: column; }`
- Header logo needs inversion: `.page-divider .samaya-header-logo { filter: brightness(0) invert(1); }`
- Content structure: `<div class="divider-body"><div class="divider-ar">Arabic title</div><div class="divider-en">English title</div></div>`
- `.divider-ar`: large bold Arabic font; `.divider-en`: smaller uppercase English
- No h2 needed — divider pages have no section number
- No footer — dividers are "un-numbered" pages that count toward total but display no page number in footer

### Pre-existing HTML malformation during splitting

Before mechanically splitting a monolithic HTML by `<section class="page">` boundaries, check for pages where a structural block (h2-row, container div) opens on one page but closes on the next. The original HTML may have:

```html
<section class="page">
  <header>...</header>
  <div class="h2-row"><div class="h2-bar"></div>
  <footer>...</footer>
</section>
<h2>17. Title...</h2><span class="disposition-chip">CHIP</span></div>
```

Here the `<div class="h2-row">` opens inside page N but its `<h2>` and `</div>` are outside on page N+1. Splitting at `<section>` boundaries produces:
- Page N: empty section with orphaned h2-row start
- Page N+1: content with `</div>` closure and no section wrapper

**Fix:** Manually reconstruct both pages:
1. Page N gets its own complete h2-row + proper title + own content
2. Page N+1 gets a `<section class="page">` wrapper with its own header + h2-row

### File layout

```
project-v2/
├── manifest.json
├── template.html
├── sections/
│   ├── cover.html
│   ├── part2-divider.html
│   └── document-control.html
├── styles/
│   └── a4.css
├── scripts/
│   ├── build.js
│   └── validate.js
├── dist/
│   └── index.html
└── package.json
```

## Adding Print CSS to Existing (Screen-First) Web Pages

When the task is "make this page print-ready" on an already-deployed screen-first page (not building a print document from scratch), the workflow differs from the dense-register overflow-fixing approach in this skill.

### When This Pattern Applies

- User hands you a URL or HTML file of a **produced page** and says "make it print-ready"
- The page has responsive/flex/grid layout for screen but no `@media print` rules
- Content fits one A4 page naturally (no overflow splitting needed)
- Goal: preserve screen appearance, add clean A4 print output

### Workflow

1. **Get the full HTML.** Use `browser_navigate` + `browser_console` with `document.querySelector('html').outerHTML` or `curl -s <URL>` to capture the full source. For embedded base64 images, `curl` preserves the full inline data.

2. **Identify what needs overriding for print:**
   - Flex/grid layouts (`display:flex`, `display:grid`) — browsers can't paginate these; override to `display:block`
   - Fixed-width containers with `box-shadow`, `border-radius` — replace with thin solid borders
   - Dark/colored backgrounds — need `print-color-adjust: exact` to render
   - Hover effects, transitions — disable
   - Button links — keep as styled text (print doesn't need interactive states)
   - Font sizes — scale down ~30% for A4 readability

3. **Write the `@media print` block** at the end of the existing `<style>`:

```css
@media print {
  @page { size:A4; margin:10mm 12mm; }
  * { -webkit-print-color-adjust:exact; print-color-adjust:exact; }
  body { background:#fff; font-size:10pt; color:#000; }

  /* Override flex/grid to block */
  .flex-container, .grid { display:block !important; }
  .flex-item { min-width:auto !important; }

  /* Stack photo-top, details-below */
  .photo { width:70%; max-width:350px; margin:0 auto 16px; }
  .photo img { box-shadow:none; border:0.5pt solid #ccc; border-radius:0; }

  /* Cards → borders instead of shadows */
  .card {
    box-shadow:none !important; border:0.5pt solid #ddd !important;
    border-radius:0 !important; padding:12px 16px; margin-bottom:10px;
  }

  /* Interactive elements */
  .downloads a {
    padding:6px 14px; font-size:9pt; border-radius:0;
    background:var(--navy,#13151A) !important; color:#fff !important;
  }
  .downloads a:hover { background:var(--navy,#13151A) !important; }

  /* Remove screen-only decorations */
  .hover-effect, .transition { display:none !important; }

  /* Footer */
  footer { padding:10px; border-top:0.5pt solid #ddd; font-size:8pt; }

  /* Suppress URL preview after links */
  a[href]:after { content:none !important; }
}
```

4. **Preserve the screen layout unchanged.** Do NOT modify existing CSS or HTML — only append the `@media print` block. The page must still look identical on screen.

5. **Deploy** by replacing the existing file on the server (FTP/SSH/sFTP to the hosting root).

### Real-World Pattern: Material Sample Landing Page (SAM-FIN-PB-001)

Example from Samaya Material Sample Library: a screen-first page with dark navy header, photo+details flex layout, download buttons, and QR/datasheet section. The `@media print` block added:

1. **`@page { size: A4; margin: 15mm 12mm 18mm 12mm; }`** — explicit A4 with comfortable margins
2. **Header override** — `.top` changes from `background:var(--navy)` to `#fff`, text to `#000`, padding shrinks to 10px, title to 20px, tags to `#eee` background
3. **Photo+details flex → inline-block** — `.grid` goes from `flex-wrap:wrap` to `flex-wrap:nowrap` with photo at `flex:0 0 42%`, details auto-fill
4. **Card border/shadow removal** — `.card` loses border-radius and box-shadow, gets thin `1px solid #ddd` border, font shrinks to 8-9px
5. **Download links show URLs** — `a[href]::after { content: \" (\" attr(href) \")\"; font-size:7px; color:#666; }` so datasheet filenames print with their full path
6. **QR section compacted** — QR shrinks to 40px, font to 8px, datasheet buttons become inline with border
7. **Footer** — thin top border, 8px text
8. **`print-color-adjust: exact`** — ensures colored tags and borders render

**Key CSS excerpt:**
```css
@media print {
  @page { size:A4; margin:15mm 12mm 18mm 12mm; }
  * { -webkit-print-color-adjust:exact; print-color-adjust:exact; }
  body { background:#fff; color:#000; }
  .top { background:#fff; color:#000; padding:10px 0; border-bottom:2px solid #333; }
  .top h1 { font-size:20px; color:#000; }
  .grid { display:flex; flex-wrap:nowrap; gap:10px; }
  .photo { flex:0 0 42%; min-width:0; }
  .photo img { border-radius:0; box-shadow:none; }
  .card { background:transparent; border-radius:0; border:1px solid #ddd; padding:6px 10px; box-shadow:none; }
  .card h2 { font-size:8px; color:#333; }
  .card p, .card li { font-size:9px; }
  .bottom { background:transparent; border:1px solid #ddd; padding:8px 10px; }
  .bottom img { width:40px; height:40px; }
  .downloads a { display:inline; background:none; color:#000; padding:2px 6px; border:1px solid #ccc; font-size:8px; }
  a[href]::after { content:\" (\" attr(href) \")\"; font-size:7px; color:#666; }
  footer { border-top:1px solid #ddd; padding:8px; font-size:8px; color:#888; }
}
```

### URL-After-Links Decision

When retrofitting print CSS, decide per-page whether links should show their URL:

- **Datasheet/PDF links** — show URL (`a[href]::after { content: \" (\" attr(href) \")\"; }`) so the printed page documents the file path
- **Navigation/action links** — suppress URL (`a[href]::after { content:none !important; }`) to avoid visual noise
- **Anchor links (#)** — always suppress

Add `a[href*=\"#\"], a[href*=\"javascript\"]::after { content:none !important; }` as a safety filter if mixing both patterns.

### Key Differences from Print-First Document Building

| Aspect | Print-First (skill default) | Retrofitting (this section) |
|--------|---------------------------|---------------------------|
| Starting point | Build from scratch or bare fragment | Existing deployed page with screen CSS |
| Challenge | Content overflow, page splits | Flex/grid → block override, color rendering |
| Measurement | Browser-based offsetHeight check | Usually not needed (1-page content) |
| CSS changes | Write full CSS from scratch | Add `@media print` block only |
| Screen layout | Not the priority | MUST preserve unchanged |
| Deployment | Surge.sh / local file | FTP/SSH replace on hosting server |

### Reference Files

- `references/modal-print-pattern.md` — Pattern for printing individual records (lessons, risks, submittals) as A4 documents from a modal overlay in a single-file HTML app. Covers CSS `@media print` rules, `.print-mode` class toggling, and fixed confidentiality footers.

## Related Skills

- `samaya-proposals` — full lifecycle for bilingual Samaya tender proposals (research, build, deploy, iterate). This skill handles overflow fixing and print tuning; `samaya-proposals` covers the complete proposal workflow.
- `sketch` — throwaway HTML mockups (different purpose — one-off creative prototypes)
- `claude-design` — design artifacts (also different — standalone landing pages and decks)
- `aseer-document-control` — SMP/CG-facing document conventions (CG comments disposition, revision history rules, column width standards)
- `samaya-factory-deploy` — deploy the built `dist/index.html` to shared hosting after build completes

## Rebuild-from-Base Strategy (When Patching Becomes Too Messy)

When the current file has undergone multiple rounds of patching and the HTML structure is becoming fragile (orphaned tags, duplicated sections, cross-contamination from `replace_all=True`):

1. **Identify the last clean base version.** For Samaya plans, this is usually Rev C00 (the first CG submission draft, stored beside the current file).
2. **Read the full C00 file** — use `read_file` with `limit` and pagination to capture all content.
3. **Apply ALL changes to C00 in one pass** — write the complete file with:
   - Cover updates (logos, ref, date, Arabic title)
   - CSS improvements (table-layout:fixed, word-wrap, hyphens, base font)
   - Section 3 redesign (tiers as formal tables)
   - All table column widths
   - Revision history entries
   - QC sign-off signature lines
   - Authority basis additions
   - Location matrix standardization
   - Page counter update
4. **Save as a new Rev** — e.g. `RevC02_CG_REVIEW.html`
5. **Verify** — count sections, check all section headers present, confirm page count matches counter

**When to use this:** After 3+ structural patch operations on the same file, or when a single `replace_all=True` has caused visible cross-section contamination.

## Reference Files

- `references/samaya-print-header-pattern.md` — Samaya-branded print header layout...
- `references/samaya-formal-html-style.md` — Samaya formal document style: minimal color palette, no gradients, clean table design. **Read before starting ANY Samaya HTML document.**
- `references/aseer-tier-crossref.md` — Aseer Museum tier-to-Appendix B cross-reference table. Use when validating Section 3 (Organization Structure) against the actual subcontractor listing. Includes per-tier role counts and common audit gaps.
- `references/stacked-area-chart-pattern.md` — SVG stacked area chart pattern for headcount loading curves. Data points, color scheme, callout annotations, legend box, gate markers. Used in Section 5.1 of the Resource Management Plan.
- `references/company-profile-design.md` — full workflow for bilingual Arabic-led company profile HTML...
- `references/boq-excel-alignment.md` — full 8-section BOQ template, OH&P loading display, common mismatch patterns, and key quantities. Always read this before building or patching a BOQ.
- `references/html-to-excel-export.md` — downstream Excel export: parsing HTML tables, RAG color mapping, category aggregation
- `references/technical-proposal-structure.md` — standard 15-page technical proposal template: page order, TOC design, steel spec conventions (epoxy not galvanized, generic HSS), compact design adjustments, page renumbering, BOQ consolidation, footer QR, surge deployment
- `references/aseer-riba-overflow-fix.md` — full split strategy, measurements, and Python rebuild pattern from the Aseer Museum RIBA tree (279 rows to 22 sheets)\n- `references/aseer-plan-content-conventions.md` — Content rules for Aseer Museum plan HTML deliverables: no brand names, no unapproved consultants, no self-incriminating language, staff role mappings, cover page rules. Read before creating or updating any Aseer Museum plan document.\n- `references/samaya-html-proposal-branding.md` — Samaya brand conventions for HTML proposals: official logo URLs, header wordmark pattern, brand colors, timeline chart design.
- `references/lidar-mos-conventions.md` — LiDAR / reality-capture Method of Statement conventions for the Aseer Museum and similar projects: Faro Focus Premium settings, scan-station overlap vs registration confidence, spherical targets, client-facing wording, and source-attribution cleanup.
- `references/2026-06-28-rcrc-restructure-lessons.md` — lessons from the RCRC Exhibition Technical Proposal restructuring: simple Python concat vs two-pass build, flexbox content stretching for sparse A4 pages, divider-to-banner merging, regex >> bug, filesystem slowness on macOS.
- `references/html-audit-workflow.md` — systematic QA workflow for auditing A4 HTML plan documents: page overflow measurement, data accuracy checks, style error detection, bulk fix patterns, and verification steps. Use when performing a comprehensive audit of any formal project plan HTML.
