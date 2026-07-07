# Aseer HTML Document Standard

## Template Source

The canonical HTML template for ALL Aseer Museum project documents is the **CV Submittal Pack template**:

`Docs/09_Registers/Key_Personnel_Register/CVs/_archive/HTML/ASR-SAM-KP-CV-PACK-SUST-001.html`

This template was explicitly designated by Mohamed Essa as the standard for all Aseer documents ("use this template for all aseer doc").

## Template Structure

### Required Elements (in order)

1. **`doc-strip`** — Thin header bar with: document reference · project name · page info · revision · date
   - Example: `Aseer Museum · Drawing Status File Tree · ASR-SAM-DWG-TREE-001 · Register A2742_5.05_DIS_021 · Rev 00 · 2026-05-29`

2. **`logo-strip`** — 4-column grid with partner logos:
   - MoC (Ministry of Culture) — Employer
   - ACE Moharram Bakhoum — PMC
   - CG (Consultancy Group) — Consultant
   - Samaya Investment — Main Contractor
   - Each cell: img (height:10mm) + `.rt` role label + `.nm` org name
   - **Logo paths** from the package root (`Completed Tender Package From NRS/`):
     `../Docs/09_Registers/Key_Personnel_Register/CVs/_assets/logos/`
   - Always use relative paths starting with `../` from the document location

3. **Title block** — Centered, bordered below:
   - Subtitle (9pt, uppercase, letter-spaced, gray `#595959`)
   - Main title `<h1>` (26-28pt, bold, uppercase)
   - Project reference (14pt, bold)

4. **`meta-grid`** — 3-column grid with info cells:
   - Project / Contract
   - Reference / Register
   - Prepared by / Submitted to
   - Document No.
   - Status
   - Each cell has `.k` (key, 7.5pt, uppercase) and `.v` (value, 9pt)

5. **Content sections** — `<h2>` black underline headers, free-form body

6. **`dc-block`** (Document Control block) at the bottom:
   - Black header bar with white text "Document Control"
   - 5-column `dc-grid`: Document No. · Revision · Issue Date · Status · Distribution
   - Uses `0.8pt solid #000` border

### CSS Foundation

- **Font:** Calibri / Carlito (Google Fonts), 9.75pt base. `'Calibri','Carlito','Arial','Helvetica',sans-serif`
- **Color:** Pure black and white (`--ink: #000000`, `--rule: #000000`, `--paper: #FFFFFF`). No colors except status indicators.
- **Borders:** All `0.6pt solid var(--rule)` — thin black lines throughout
- **Page:** A4 portrait, `210mm`, margins 14mm-18mm
- **Sheet class:** `.sheet` with `width:210mm; min-height:297mm; padding:14mm 18mm; page-break-after:always`
- **Table column widths:** Add `table-layout:fixed` to the global `table` CSS rule + `word-wrap:break-word; overflow-wrap:break-word` to `td` and `th`. Without `table-layout:fixed`, browsers ignore `th style="width:X%"` and auto-size by content, causing overflow on A4. Also convert any pixel-width columns (e.g. `width:60px`) to percentages for consistent A4 rendering. This one-line fix handles all tables globally.

### Print CSS (Critical — Multi-Page Support)

For documents that span multiple A4 pages (like the drawing status tree with 243 entries), **do NOT use `overflow: hidden`** in print mode. Use this pattern instead:

```css
@media print {
  html, body { background: #FFFFFF; margin: 0 !important; padding: 0 !important; }
  .sheet {
    margin: 0 !important; box-shadow: none !important;
    width: 210mm !important; min-height: 297mm !important;
    padding: 14mm 18mm !important;
    overflow: visible !important;  /* ← NOT hidden — allows page breaks */
    page-break-after: always; break-after: page;
    box-sizing: border-box !important;
  }
  .sheet.cover { padding: 12mm 16mm !important; }
  .sheet:last-child { page-break-after: auto; break-after: auto; }

  /* Protect header blocks from page breaks */
  h1, h2, .doc-strip, .logo-strip, .dc-block .head { page-break-after: avoid; break-after: avoid; }
  .logo-strip, .meta-grid, .dc-block, .counter-row, .disc-grid, .legend-box {
    page-break-inside: avoid; break-inside: avoid;
  }
}
@page { size: A4 portrait; margin: 0; }
```

**Why `overflow: visible`:** The old `overflow: hidden !important` clips content that overflows a single A4 page. For tree documents with ~200+ lines, content must be able to flow naturally across multiple pages. The browser auto-inserts page breaks at the `.sheet` boundary.

**⚠️ Pitfall: Do NOT use `@page { margin: 15mm 18mm }` with `.sheet { padding: 14mm 18mm }`** — this double-applies margins, pushing content into an ~154mm wide column (210 - 30 - 28 = 152mm usable). Always use `@page { margin: 0 }` and let `.sheet` padding handle all spacing. The `.sheet` is already sized at `width: 210mm` (exact A4 width) with `padding: 14mm 18mm` giving a 174mm-wide content area.

### Auto-Pagination for Long Content

When content exceeds a single A4 page (common for drawing trees, status reports), **do NOT set `height: 297mm; max-height: 297mm`** on `.sheet`. Instead:

1. Use `min-height: 297mm` (not `height`) so content can grow
2. Use `overflow: visible` in print mode (not `overflow: hidden`)
3. The browser auto-splits content across multiple physical pages
4. Set `page-break-inside: avoid` on header blocks to keep them intact

#### Cover Page Pattern (Critical — User Approved Pattern)

For documents with a statistics summary + long tree/list content, **split the first sheet into a STATISTICS-ONLY cover page**. The tree starts on page 2. This was explicitly requested by Mohamed Essa when the first page overflowed.

**Page 1 (Cover):** Statistics only — NO tree/list content:
- doc-strip + logo-strip + title block + meta-grid
- Counter tiles (4-column: Stamped/Pending/Missing/Rev-Gap)
- Discipline summary grid (20 items, 5 columns)
- Legend box
- That's all — no tree content on this page

**Pages 2..N (Tree):** Tree/list content only:
- First tree page: doc-strip (full reference) + `<h2>` File Tree heading + tree chunk
- Subsequent tree pages: mini doc-strip with `Sheet N of M` label + "continued" paragraph + tree chunk
- Last page: tree chunk + dc-block at the bottom

#### Programmatic Multi-Sheet Splitting at Group Boundaries

For **programmatic multi-sheet splitting** (e.g., splitting a tree into separate `.sheet` divs at discipline group boundaries):

```python
import re

# 1. Read the complete tree as lines
tree_lines = tree_text.split('\n')

# 2. Find group boundary markers
grp_indices = [i for i, l in enumerate(tree_lines) if 'grp' in l and 'span' in l and '<' in l]

# 3. Calculate chunk sizes — target ~60-80 lines per tree page
# Each tree page has a small header (~3 lines), leaving ~77 lines for content
# Usable A4 height: 297 - 28(padding) = 269mm
# Tree font 6.5pt × 1.2 line-height = ~2.8mm per line
# ~269/2.8 = ~96 lines per page max. With 3-line header = ~93 lines of tree.
# But for safety target 60-80 lines to account for DC-block on last page.

# 4. For the Aseer Museum tree (20 groups, 264 lines):
#   Page 2: groups 0-5  (00 to 1350)  = 40 lines
#   Page 3: groups 6-8  (1510 to 1600) = 46 lines
#   Page 4: groups 9-10 (1700 to 1720) = 92 lines
#   Page 5: groups 11-17 (1800 to 1950) = 83 lines
splits = [
    (0, grp_indices[6]),       # root + groups 0-5
    (grp_indices[6], grp_indices[9]),  # groups 6-8
    (grp_indices[9], grp_indices[11]), # groups 9-10
    (grp_indices[11], len(tree_lines)) # groups 11-17
]

# 5. Build sheets
out = []
for ci, (s, e) in enumerate(splits):
    chunk = tree_lines[s:e]
    
    if ci == 0:
        doc = doc_strip  # full reference
        h2 = '<h2>File Tree — Drawing Status vs Register (DIS_021)</h2>'
        out.append(f'<div class="sheet">{doc}{h2}<pre class="tree-box">{"".join(chunk)}</pre></div>')
    elif ci == len(splits) - 1:
        doc2 = doc_strip.replace('2026-05-29', f'Sheet {ci+2} of {total} · 2026-05-29')
        out.append(f'<div class="sheet">{doc2}<p style="font-size:8pt;font-weight:700;margin:0 0 1.5mm;text-transform:uppercase;letter-spacing:.06em;">File Tree — continued (Sheet {ci+2} of {total})</p><pre class="tree-box">{"".join(chunk)}</pre>{dc_block}</div>')
    else:
        doc2 = doc_strip.replace('2026-05-29', f'Sheet {ci+2} of {total} · 2026-05-29')
        out.append(f'<div class="sheet">{doc2}<p style="font-size:8pt;font-weight:700;margin:0 0 1.5mm;text-transform:uppercase;letter-spacing:.06em;">File Tree — continued (Sheet {ci+2} of {total})</p><pre class="tree-box">{"".join(chunk)}</pre></div>')
```

**Key constraints for the cover page pattern:**

1. The cover page has NO `<pre class="tree-box">` — it's just stats
2. The first tree page (page 2) has a full doc-strip with h2 heading
3. Subsequent tree pages have a modifed doc-strip: replace date with `Sheet N of M` label
4. Add a "continued" paragraph below the doc-strip on non-first tree pages
5. The dc-block (Document Control) goes ONLY on the last tree page
6. Ensure the closing `<pre>` tag is not doubled — check that `</pre></pre>` doesn't appear in the output

**Total pages for a typical 264-line tree (20 groups):** 1 cover + 4 tree pages = 5 sheets.

The non-first sheets should include a "Sheet N of M" label in the doc-strip so the user knows which page they're reading.

### Required Media Queries

```css
@media screen { .sheet { overflow: hidden; } }    /* On-screen: clip overflow */
@media print { .sheet { overflow: visible; } }     /* Print: allow multi-page flow */
```

### Naming Convention

- Doc code prefix: `ASR-SAM-<CATEGORY>-<TYPE>-NNN`
- Examples: `ASR-SAM-DWG-TREE-001`, `ASR-SAM-KP-CV-PACK-SUST-001`
- Revision and date appended: `Rev 00 · 2026-05-29`

## ⚠️ QA Checklist — Verification Before Delivery

Every HTML document must pass these checks before showing to the user. Mohamed Essa corrects immediately on any of these — fix before submitting:

### Structural Verification

- [ ] **Balanced `<div>` tags** — `grep -c '<div' file.html` should equal `grep -c '</div' file.html`. An unbalanced div breaks the entire layout (logos vanish, grid collapses). Run `grep -o '<div' file.html | wc -l` and compare with `grep -o '</div' file.html | wc -l`.
- [ ] **No double-closing `<pre>`** — `grep -c '</pre></pre>' file.html` should be 0. When building multi-page documents, a trailing `</pre>` from a previous iteration can leak into the next page's content, creating unbalanced HTML. Check: `grep -o '<pre' file.html | wc -l` == `grep -o '</pre' file.html | wc -l`.
- [ ] **Cover page is STATISTICS ONLY** — first `.sheet` div must have NO `<pre class="tree-box">` or `<table>` content longer than ~10 lines. The cover page only shows: doc-strip, logo-strip, title, meta-grid, counter tiles, discipline grid, legend. Tree/list content starts on page 2.
- [ ] **Logo paths resolve** — open the HTML file in a browser. If the 4 logos (MoC, ACE, CG, Samaya) show as broken images, the relative path is wrong. From `Completed Tender Package From NRS/` root, use: `../Docs/09_Registers/Key_Personnel_Register/CVs/_assets/logos/` (the `../` goes up to the Aseer-Museum root).
- [ ] **Page title is set** — `<title>` tag must be present and descriptive (e.g., "Aseer Museum · Drawing Status File Tree").
- [ ] **A4 sizing is correct** — the page must render at `210mm × 297mm`. If it looks stretched/compressed, check that `@page { size: A4 portrait; margin: 0; }` is present, `.sheet` has `width: 210mm; min-height: 297mm;`, and there's no `@page { margin: 15mm 18mm }` double-applying margins.

### Printing & Multi-Page Verification

- [ ] **Print preview doesn't clip** — open in browser → File → Print → check that content from page N doesn't overflow into the header of page N. If it clips, ensure `.sheet` in `@media print` has `overflow: visible !important` (NOT `overflow: hidden`).
- [ ] **Each `.sheet` gets its own page** — in print preview, each sheet starts on a fresh A4 page. Ensure `page-break-after: always;` on `.sheet` (except the last).
- [ ] **Doc-control block appears only on last page** — if the document has multiple pages, the `dc-block` goes only on the final `.sheet`, not on every page.
- [ ] **"Sheet N of M" labels** — on pages 3+, the doc-strip should show "Sheet N of M" and a "continued" label below the heading so the user knows they're reading a continuation page.

### Counter & Status Accuracy

- [ ] **Counter tiles match the data** — if the document shows "162 Stamped / 69 Pending / 12 Missing", these numbers must be hand-verified against the source data. Do NOT leave placeholder numbers.
- [ ] **Discipline grid counts match** — each discipline's OK/Pending/Missing counts in the grid should sum to the tile totals.

### Font & Styling

- [ ] **All caps on titles** — `h1`, subtitle, and key section headings must be `text-transform: uppercase`. Mohamed Essa expects uppercase titles.
- [ ] **Pure black and white** — no colors except the status indicator fills (green/blue/red/amber on counter tiles). Borders, text, and rules are `#000000`.
- [ ] **Font stack is Calibri/Carlito** — not Arial, not system-ui, not any other font. `font-family: 'Calibri','Carlito','Arial','Helvetica',sans-serif`.

> **Note**: The Calibri/Carlito stack above applies to the **CV Pack / Drawing Tree** document class. For **Formal Plans** (SMP, DMP, Resource Mgmt, etc.), follow `Samaya-Formal-Plan-A4-Style-Guide.md` which mandates **Inter** (body), **Montserrat** (headings), **Menlo** (metadata) — never Calibri. Check the document's own `:root` tokens and `font-family` declaration to determine which class it belongs to.

## Template Variant: Drawing Status Tree

The `Aseer_Drawing_Status_Tree.html` adds these components on top of the base template:

### Counter Tiles (4-column grid)

```html
<div class="counter-row">
  <div class="counter-tile ok">
    <div class="num">162</div>
    <div class="label">Stamped [OK]</div>
  </div>
  <div class="counter-tile pn">
    <div class="num">69</div>
    <div class="label">Pending [&gt;&gt;]</div>
  </div>
  ...
</div>
```

```css
.counter-row { display: grid; grid-template-columns: repeat(4, 1fr); gap: 3mm; margin: 3mm 0; }
.counter-tile { border: 0.6pt solid #000; padding: 1.5mm 2mm; text-align: center; }
.counter-tile .num { font-size: 18pt; font-weight: 800; line-height: 1.1; }
.counter-tile .label { font-size: 7pt; font-weight: 700; text-transform: uppercase; letter-spacing: 0.08em; color: #444; }
.counter-tile.ok { background: #F0FDF4; } .counter-tile.ok .num { color: #15803D; }
.counter-tile.pn { background: #EFF6FF; } .counter-tile.pn .num { color: #1D4ED8; }
.counter-tile.xx { background: #FEF2F2; } .counter-tile.xx .num { color: #B91C1C; }
.counter-tile.na { background: #FFFBEB; } .counter-tile.na .num { color: #92400E; }
```

### Discipline Summary Grid (20 items, 5 columns)

```html
<div class="disc-grid">
  <div class="disc-item">
    <div class="code">00 — Existing</div>
    <span class="s xx">[XX]10</span> <span class="s pn">[&gt;&gt;]5</span>
  </div>
  ...
</div>
```

```css
.disc-grid { display: grid; grid-template-columns: repeat(5, 1fr); gap: 1.5mm; margin: 3mm 0; }
.disc-item { border: 0.4pt solid #000; padding: 1mm 1.5mm; font-size: 7.5pt; }
.disc-item .code { font-weight: 700; }
.disc-item .s.ok { color: #15803D; font-weight: 700; }
.disc-item .s.pn { color: #1D4ED8; font-weight: 700; }
.disc-item .s.xx { color: #B91C1C; font-weight: 700; }
```

### Legend Box

```html
<div class="legend-box">
  <b>Legend:</b>
  <b class="ok">[OK]</b> = stamped
  <b class="pn">[&gt;&gt;]</b> = pending
  <b class="xx">[XX]</b> = missing
</div>
```

```css
.legend-box { border: 0.6pt solid #000; padding: 1.5mm 2mm; margin: 3mm 0; font-size: 7.5pt; }
```

### File Tree Block

```css
.tree-box {
  border: 0.6pt solid #000; background: #FAFAFA;
  padding: 2mm 2.5mm;
  font-family: 'Courier New','Courier','monospace';
  font-size: 6.8pt; line-height: 1.25;
  white-space: pre; overflow: hidden; margin: 0;
}
.tree-box .root { font-weight: 700; font-size: 7.2pt; }
.tree-box .grp { font-weight: 700; }
.tree-box .ok { color: #15803D; font-weight: 700; }
.tree-box .pn { color: #1D4ED8; font-weight: 700; }
.tree-box .xx { color: #B91C1C; font-weight: 700; }
```

### Status Tags (Inline)

```css
.status-tag {
  display: inline-block; font-size: 6pt; font-weight: 700;
  text-transform: uppercase; letter-spacing: 0.06em;
  padding: 0.3mm 1.5mm; border: 0.4pt solid #000; margin-left: 1mm;
}
.status-tag.ok { background: #F0FDF4; color: #15803D; }
.status-tag.pn { background: #EFF6FF; color: #1D4ED8; }
.status-tag.xx { background: #FEF2F2; color: #B91C1C; }
```

## No QC Block on Status Trees

The drawing status tree variant omits the `qc-block` (which IS present on CV Pack template for Prepared/Review/Approved signatures). Only the `dc-block` is included at the bottom.

## Risk Register — Standard PM Table Format (User-Approved)

Use a **standard project management risk register table** — NOT a card-grid layout. The user explicitly requested "redesign as standard risk register always used in project management" after seeing the card-grid version.

### Columns

| # | Risk Description | Category | Prob. | Impact | Rating | Mitigation / Response Strategy | Owner | Status |
|---|-----------------|----------|-------|--------|--------|-------------------------------|-------|--------|

- **Prob.** scale: 1=Rare · 2=Unlikely · 3=Likely · 4=Almost Certain
- **Impact** scale: 1=Negligible · 2=Minor · 3=Moderate · 4=Major · 5=Severe
- **Rating** = P × I, shown as colored badge: 1-4 Low (green `#16A34A`) · 5-9 Medium (amber `#F59E0B`) · 10-20 High (red `#B91C1C`)
- **Status**: Open (red `#B91C1C` text) / Tracking (brown `#92400E` text) / Planned (green `#16A34A` text) / Closed

### Legend (below the table)

```html
<div style="margin-top:5px;display:flex;gap:12px;font-size:0.38rem;color:var(--text-muted);">
  <span><b>Prob. scale:</b> 1=Rare · 2=Unlikely · 3=Likely · 4=Almost Certain</span>
  <span><b>Impact scale:</b> 1=Negligible · 2=Minor · 3=Moderate · 4=Major · 5=Severe</span>
</div>
<div style="margin-top:2px;display:flex;gap:12px;font-size:0.38rem;color:var(--text-muted);">
  <span><b>Rating:</b> P × I → 1-4 Low (green) · 5-9 Medium (amber) · 10-20 High (red)</span>
  <span><b>Status:</b> Open · Tracking · Planned · Closed</span>
</div>
```

### Rating Badge HTML

```html
<span style="background:#B91C1C;color:white;font-size:0.35rem;font-weight:800;padding:1px 4px;border-radius:2px;">12 · HIGH</span>
<!-- Medium: background:#F59E0B, text: "9 · MED" -->
<!-- Low: background:#16A34A, text: "4 · LOW" -->
```

## Workflow Charts — Inline SVG for Process Sections

Add compact inline SVG workflow charts to process sections to make plans easier to read. The user explicitly requested: "add workflow charts wherever its needed and will make the plan easy to read."

### When to Add

- **Induction/onboarding steps** — linear flowchart
- **Replacement/succession protocol** — decision flowchart with yes/no branches
- **Procurement lifecycle** — linear flow with 5 stages
- **Monitoring cycle** — circular flow (Plan vs Actual → Variance → Corrective Actions → Reporting → loop)
- **Change control** — decision flowchart (Key Personnel? → CG approval vs internal approval)

### SVG Style (aligned to Samaya Formal Plan A4 Style Guide)

**Canonical reference**: `~/OneDrive.../Technical Office/_Style-Guides/Samaya-Formal-Plan-A4-Style-Guide.md`

- `viewBox` around `0 0 560 72-100` depending on chart complexity
- Box style: `rx=2, fill=#FFFFFF, stroke=#0F172A, stroke-width=1` (white boxes, NOT #F8FAFC)
- Background rect: `fill="#F8FAFC" rx="4"` on the SVG root
- Header labels: `font-family="Inter,sans-serif", font-size="7", font-weight="800", fill="#0F172A", letter-spacing="0.5"` (e.g., STEP 1, STAGE 1, TRIGGER)
- Body text: `font-family="Inter,sans-serif", font-size="8", font-weight="700", fill="#0F172A"`
- Sub-labels: `font-size="7", fill="#64748B"`
- Arrows: `→` character at `font-size="14", fill="#0F172A", font-weight="700"` (NOT SVG line markers — matches existing phase strip style)
- Branch arrows: `↗` / `↘` characters for yes/no splits
- End/approve boxes: `fill="#0F172A"` with white text (navy dark box, like phase strip P5)
- Highlighted boxes: HSSE/critical = red border (`#B91C1C`, fill `#FEE2E2`), ERP/system = blue border (`#0284C7`, fill `#EFF6FF`), trigger = amber (`#F59E0B`, fill `#FEF3C7`), approved/done = green (`#16A34A`, fill `#BBF7D0`)
- Wrapper: `<div style="margin:6px 0;border:1px solid var(--border);border-radius:2px;padding:6px;background:var(--bg-light);">` (2px radius max per style guide)
- Width: `style="width:100%;max-width:560px;display:block;margin:0 auto;"`

**NEVER use Calibri in SVGs** — the existing phase strip may have Calibri from an older version, but the style guide mandates Inter for body text. Replace any Calibri with Inter when touching SVGs.

**Color tokens (from style guide)**:
- `--primary: #0F172A` (navy)
- `--secondary: #0284C7` (sky blue)
- `--accent: #F59E0B` (amber — triggers, start boxes)
- `--pass: #16A34A` (green — approved, done, low risk)
- `--fail: #B91C1C` (red — critical, rejected, high risk)
- Brown: `#92400E` (medium severity, tracking status)
