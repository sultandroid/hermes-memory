---
name: samaya-proposals
category: productivity
description: Create bilingual (AR/EN) A4 print-ready HTML tender proposals for Samaya Investment. Covers material specs (Cement Board, Jotun Epoxy, PVC Flex, LED), BOQ Excel, Surge.sh deployment, multi-store tender programs with supplier data conversion, and iterative refinement via Claude Code.
triggers:
  - User asks to create/propose a tender or quotation
  - User hands you a tender brief / RFP / proposal request
  - User says "make a proposal for ..."
  - Building a print-ready HTML proposal from scratch
  - User says "study proposals against project knowledge" or "study pricing against style guide"
  - Supplier has sent raw pricing data (Excel) for multiple stores/projects — needs conversion to Samaya proposals
  - Multi-store/multi-client tender program with partial pricing data
  - Creating framework proposals with TBD pricing for upcoming supplier quotations
  - User asks to "prepare costing" or "price this tender" for a supply/manufacturing item (non-construction)
  - Extracting specs from an Etimad government tender PDF
---

# Samaya Proposals — HTML Tender Proposal Workflow

## ⚠️ Mandatory First Step: Read the Style Guide

**Before building ANY HTML proposal or document for Samaya, you MUST read the current authoritative style guide:**

```
OneDrive/Samaya/Technical Office/_Style-Guides/Samaya-Formal-Plan-A4-Style-Guide.md
```

This style guide from the Technical Office is the SINGLE SOURCE OF TRUTH for:
- Color palette (navy/sky/green/red — NOT bronze/gold)
- Font stack (Montserrat/Inter/Menlo/IBM Plex — NOT Playfair/Tajawal)
- Page model (exact 210×297mm .page sheets — NOT loose sections)
- Component classes (.h2-row, .pg-footer, .page-header, .disposition-chip, .strip, .snapshot-card, .banner, .cat-row)
- Badge system (.badge-pass, .badge-critical, .badge-high, .badge-warn, .badge-low)
- Cover page (full-bleed navy with green keyline)
- SVG chart patterns (6 standard charts)
- Print CSS (@page { size: A4 portrait; margin: 0; })

The style guide also includes an `_A4-print-template.html` reference file — review it for structural patterns.

**Do NOT rely on the design system documented in this skill's reference files alone** — those references may lag behind the authoritative style guide. Always verify against the actual style guide first.

## Design System

### For Type A (Fence/Perimeter) — Factory Brand
- **Theme:** Red accent (`#B01E2F`), dark ink (`#1F2430`), white pages
- **Fonts:** IBM Plex Sans Arabic (AR), Inter (EN), JetBrains Mono (code/data)
- **Layout:** A4 portrait (794×1123px), bilingual Arabic/English RTL
- **Print:** `@page{size:A4 portrait;margin:10mm 0}` with page-break-after
- **Footer:** Brand + samaya-factory.com (with QR) + page number

### For Type B (Exhibition/Museum) — Samaya Formal Plan (AUTHORITATIVE)
Use the Samaya Formal Plan A4 Style Guide palette and components (navy/sky/green). See `references/exhibition-design-system.md` for the full token reference.

- **Primary:** Navy `#0F172A` — headers, table th, cover background
- **Secondary:** Sky Blue `#0284C7` — H2 bars, icons, RACI-A
- **Success / Pass:** Green `#16A34A` — cover keyline, pass badges
- **Fail:** Red `#B91C1C` — reject, critical badges
- **Warn:** Amber `#92400E` — partial/advisory badges
- **Body text:** `#1E293B`
- **Muted:** `#64748B` — captions, footnotes
- **Border:** `#E2E8F0`
- **Bg light:** `#F8FAFC` — zebra stripes, muted fills
- **EN Headings:** Montserrat 800 UPPERCASE
- **EN Body:** Inter 400/500/600/700/800
- **AR:** Cairo (preferred, user approved) — weights 400/500/600/700/800/900. **Do NOT use IBM Plex Sans Arabic** unless a specific project requires it — user switched to Cairo in Jun 2026 for the RCRC Exhibition proposal and prefers the cleaner geometric look. IBM Plex references in existing documents should be migrated to Cairo when editing. Google Fonts import: `family=Cairo:wght@400;500;600;700;800;900`
- **Metadata/Mono:** Menlo/Monaco
- **Border-radius:** Max 2px (no rounded cards)
- **Box-shadow:** Screen-only, never on content elements
- **Page model:** `.page { width:210mm; height:297mm; overflow:hidden; }` — exact A4
- **Cover:** Full-bleed navy `#0F172A`, white text, green `#16A34A` keyline strip on title
- **Section header:** `.h2-row` with 10px sky-blue `.h2-bar`
- **Footer:** `.pg-footer` with `doc# · context · PAGE N/Total`
- **Header:** `.page-header` with breadcrumb left, SAMAYA logo right
- **Metric cards:** `.snapshot-card` — metric with colored top border
- **Spec strip:** `.strip` — bordered block with `.strip-grid` key-value pairs
- **Section banner:** `.banner` — sub-section header with border-bottom
- **Badges:** `.badge-pass`, `.badge-critical`, `.badge-high`, `.badge-warn`, `.badge-low`
- **Disposition chip:** `.disposition-chip` — mono uppercase label with border
- **Category row:** `.cat-row` — navy full-width row in tables
- **RACI badges:** `.raci-r`, `.raci-a`, `.raci-c`, `.raci-i` — colored square badges
- **SVG diagrams:** 6 required (Integration Workflow, Issue Escalation, Quality Flow, Org Chart, Gantt, Risk Heatmap)
- **⚠️ Monochrome charts only** — do NOT use multiple colors in SVG charts or icons. This is a formal tender document, not a marketing brochure. Use only navy `#0F172A`, slate `#475569`, white `#FFFFFF`, and light gray `#E2E8F0` fills. No green (`#16A34A`), sky blue (`#0284C7`), red (`#B91C1C`), amber (`#92400E`), purple (`#7C3AED`), or any accent color in charts, legends, or icons. The one exception is the navy cover page where white-on-navy is expected.
- **TOC icons:** Use monochrome symbols (▶, ●, ◆) on light gray `#E2E8F0` backgrounds with `#475569` text. No emoji icons. Part badges all use navy `#0F172A` background regardless of part number — no part-specific colors.

## Standard Proposal Structure (17 pages)
1. **Cover** — client name, location, project stats, 4 scope cards
2. **Table of Contents** — 4 categorized groups with emoji icons + anchor links
3. **Executive Summary** — company profile, key stats row, operating model
4. **Scope of Work** — detailed items table with specs (incl. gates)
5. **Capabilities** — manufacturing capabilities grid
6. **Technical Specifications** — overview table (all materials, dimensions, standards)
7. **Banner & UV Printing TDS** — PVC Flex material data sheet
8. **Cement Board 12mm TDS** — fiber cement data sheet
9. **Jotun Epoxy Mastic TDS** — coating data sheet
10. **LED Flood Light TDS** — lighting data sheet
11. **BOQ Part 1** — Steel Structure + Civil Works + Cladding
12. **BOQ Part 2** — Banner/Printing + Lighting/Electrical + Gates + Additional
13. **Implementation Methodology** — 5-phase execution plan
14. **Project Timeline** — Gantt chart with phases
15. **Company Documents & Certifications**
16. **Payment Schedule + Terms**
17. **Signature Page**

### TOC Category Structure
```
Project Introduction · مقدمة المشروع    📋 Cover, 📊 Executive Summary
Technical Scope · النطاق الفني           🔧 Scope, 📐 Specs, 💡 Lighting, 📦 BOQ
Execution Plan · خطة التنفيذ            📅 Timeline
Company & Commercial · الشركة            🏢 Team, 💰 Payment, ⚖️ Terms, ✍️ Signature
```

**⚠️ Monochrome TOC only:** Replace the above emoji icons with monochrome symbols (▶, ●, ◆) when placing in the actual HTML. Part badges all use navy `#0F172A` background regardless of part number. Icon backgrounds are light gray `#e2e8f0` with `#475569` text/icon color. No green, sky, red, purple, or any part-specific colors in the TOC table.

### TOC Design Pattern (Formal Proposal)
For the Table of Contents section, use this structure:
1. **Snapshot bar** — 5 metric cards (sections, parts, duration, work packages, team size)
2. **Table** with 3 columns: `#` (30px), `القسم (Section)`, `الصفحة` (65px)
3. **Part divider rows** — navy `#0F172A` full-width cat-row with part number badge + title + English subtitle in muted white
4. **Each section row** — monochrome icon (▶, ◆, ●, ◼) on gray `#e2e8f0` background + section name + page number
5. **Self-highlight** — the current section (TOC itself) gets a sky-blue icon `#0284C7` with white text

### Anchor Links Pattern
- Every `<section class="page">` gets `id="page-N"` (sequential 1-17)
- Cover uses `<section class="page cover" id="page-1">` — note the `cover` class + id together
- TOC items wrap content in `<a href="#page-N" style="text-decoration:none;color:inherit">` — preserves visual style
- Verify no double-quote bugs: `id="page-1""` is WRONG, should be `id="page-1"`
- **After ANY structural change (add/remove/reorder pages), run this verification checklist:**
  - [ ] Page IDs are sequential (1 to total_pages) with no gaps
  - [ ] Footer page numbers match their section's ID number
  - [ ] Footer total "/N" matches the actual total page count
  - [ ] Every TOC `href="#page-N"` points to an existing section
  - [ ] TOC page numbers match actual footer page numbers
  - [ ] Cover's `PAGE 01 / N` matches total page count

### A4 Height Constraint Enforcement
- `.page` has `min-height:1123px` on desktop + `overflow:hidden` — this clips anything exceeding A4
- **Flex blowout prevention:** ALL children with `flex:1` MUST also have `min-height:0` — otherwise flex items can grow past the container
- **Images inside flex containers:** use `height:100%` + `object-fit:contain` (NOT `height:auto`) — this makes the image scale to the container, not its natural dimensions
- When splitting space between elements, use `flex-shrink:0` on header/footer bars so they don't compress, and `flex:1;min-height:0` on content that should fill remaining space

### TOC Update Rule (MANDATORY)
- **Every time ANY page is added, removed, or reordered:** update TOC immediately
- Update: item descriptions, page numbers, href targets, category groupings
- Verify: every TOC page number matches actual footer page number
- Verify: every `href="#page-N"` points to an existing `id="page-N"` on a `<section>`

### Loaded Pricing (OH&P Markup)
The Excel BOQ should have two sheets:
1. **"Option C - BOQ"** — base unit rates (direct cost)
2. **"Option C - BOQ (Loaded)"** — rates with OH&P built in:
   - Supervision / Preliminaries: 8%
   - Overhead (G&A): 10%
   - Profit Margin: 12%
   - **Total Loading Factor: 1.30×**
- The HTML BOQ should use LOADED prices, not base rates
- Add a note below the Grand Summary table showing the loading breakdown

### BOQ Consolidation Pattern
- All BOQ content should fit on pages 12-13 (2 pages max)
- **Must match the Excel exactly** — 8 sections, not 6:
  1. **SECTION 01 — STEEL STRUCTURE · الهيكل المعدني** (Item 01)
  2. **SECTION 02 — CIVIL WORKS · الأعمال المدنية** (Item 02)
  3. **SECTION 03 — CLADDING & FINISH · الكسوة والتشطيب** (Items 03-04)
  4. **SECTION 04 — BANNER & PRINTING · البانر والطباعة** (Item 05)
  5. **SECTION 05 — LIGHTING · الإضاءة** (Item 06)
  6. **SECTION 06 — ELECTRICAL WORKS · أعمال الكهرباء والتمديدات** (Items 07-08)
  7. **SECTION 07 — DOORS & GATES · الأبواب والبوابات** (Items 09-10)
  8. **SECTION 08 — ADDITIONAL & SAFETY · أعمال إضافية وسلامة** (Items 11-12)
- **Item numbering: sequential 01-12 across ALL sections** (not per-section restart)
- **Grand Summary table: 8 rows** matching the sections above, with correct subtotals
- Page 17 = Payment Terms + Terms & Conditions + Signature (NO BOQ on page 17)
- The Excel may have Section 08 items (Mobilization + Safety signage) distributed pro-rata into all other items. When this happens, Section 08 is removed and each item's rate is adjusted upward by a small factor (~0.85%). The unit rates become fractional (e.g., 111.44 instead of 110.50). Update ALL rates from the loaded sheet when this occurs.

### BOQ Data Sync from Excel (openpyxl)
When the user updates the Excel file and says "update from Excel":
1. Read `BOQ_Pricing_Model.xlsx` with `openpyxl` + `data_only=True` from the `Option C - BOQ (Loaded)` sheet
2. Extract every row: item #, description, unit, qty, rate, total
3. Compare each value against the current HTML BOQ tables on pages 12-13
4. Patch every discrepancy individually using `patch()` with the exact `class="price">OLD_RATE</td>` pattern
5. Update the Grand Summary table rows (section subtotals, excl. and incl. VAT per section)
6. Update the grand total, VAT, and total incl. VAT footer rows
7. Check for stale values on earlier pages (cover page scope card shows rate/m², executive summary shows total project value)
8. The user may also restructure sections — if Section 08 items (Mobilization + Safety signage) get distributed pro-rata into all other items, remove Section 08 entirely and adjust each item's rate upward by ~0.85% (distribution factor = 28,480 / 3,338,788.80 ~ 0.00853). Verify the grand total stays the same.
8. The user may also restructure sections — if Section 08 items (Mobilization + Safety signage) get distributed pro-rata into all other items, remove Section 08 entirely and adjust each item's rate upward by ~0.85% (distribution factor = 28,480 / 3,338,788.80 ~ 0.00853). Verify the grand total stays the same.

### Default Quantities (Fence Projects)
- **Fence length:** 1,426 m (perimeter)
- **Height:** 8 m
- **Banner/cladding area:** 11,408 m²
- **Column spacing:** 3 m (NOT 4m — user corrected this)
- **Columns/footings:** floor((length − gate_width) / spacing) + 1 (e.g., (1426−7.2)/3 = 474)
- **Footing spec:** Precast RC isolated footing 2.75×1.50×0.60m, Fcu 300, complete with anchor bolts, reinforcement cage, lifting inserts — delivered & levelled on prepared bed
- **LED lights:** depends on spacing — at 12m: ~118 units; at 2m (Excel): ~711 pcs. **Always check the Excel QUANTITY INPUTS section for Light spacing value.**
- **Gate deductions:** Vehicle gate 6m + Pedestrian gate 1.2m = 7.2m total. Deduct from effective fence length before calculating columns AND lights
- **Distribution panels:** 1 per ~150m = ~10 panels
- **Effective fence length (after gates):** 1,426 − 7.2 = 1,418.8m

### Quantity Recalculation Pattern
When spacing changes (e.g., 4m → 3m), update ALL dependent items:
1. Columns count → footings, base plates, anchor bolts, numbering paint
2. Bolts count → columns × 8 bolts per column
3. LED lights → recalculate from effective length / 12m
4. Update HTML stat boxes, spec tables, BOQ items, methodology/timeline references
5. Update BOQ_Pricing_Model.xlsx formulas automatically
- **Cladding:** Cement Board 12mm (fiber cement, A1 fire rated) as rigid substrate
- **Banner:** PVC Frontlit Flex 440-510 gsm with UV digital printing 1440 dpi
- **Coating:** Jotun Epoxy Mastic (≥200µm DFT) — NO galvanizing unless client demands it
- **Steel:** HSS sections per structural calculation (do NOT specify exact profile in proposal)
- **Lighting:** LED Flood Light 300W IP66 5000K, spaced ~12m, adjust for gates
- **Gates:** Vehicle gate 6m×8m + Pedestrian gate 1.2m×2.1m (deduct from light count)
- **Foundation:** RC footings 1.2×1.2×0.9m K-300, above-ground

## Proposal Types

This skill covers **two proposal classes**, each with different scope and deliverables:

### Type A: Fence / Perimeter Projects (Default)
Carbon fence, cement board cladding, banner printing, LED flood lighting, gates. 17-page standard structure. See `references/BOQ-structure.md` for the itemised BOQ template.

### Type B: Exhibition / Museum Fit-Out (CLIENT-FACING — strip PMBOK jargon)\nHigh-end interior exhibition with AV (Epson, QSC, Crestron), LED walls (LOPU, Muxwave), lighting (DGA, FLOS, Prolights), imported European furniture (B&B Italia, Poltrona Frau, Calligaris), custom display cases, scenic theming, and MEP integration. 12-chapter proposal structure covering all disciplines.\n\n**NOTE:** This skill covers Type B exhibition proposal CONTENT (org charts, experience cards, gallery sections). For the STRUCTURAL FRAMEWORK (build pipeline, CSS tokens, auto-numbering engine, page anatomy), load the `samaya-doc-engine` skill alongside this one.\n- Every `"— PMBOK X"` suffix in section headings, every `"PMBOK-aligned"` phrase, every `"per PMBOK"` reference must be deleted before delivery.\n- The client does not need to see project-management framework labels — use plain-English discipline names: `Scope of Work`, `Schedule Management`, `Quality Management`, etc. never `Scope of Work — PMBOK Scope Management`.\n- **Do NOT reference documents Samaya authored** (SOW, ER, technical specifications) as if they're external client-given documents. Samaya wrote them, so referencing `"Per ER §2.1"` or `"per SOW"` in the proposal is self-referential and unprofessional. Replace with topic descriptions or remove.

| Aspect | Type A — Fence | Type B — Exhibition |
|--------|---------------|-------------------|
| Typical value | $0.5–5M | $5–20M+ |
| Disciplines | Steel, civil, printing, basic electrical | AV, lighting, furniture, scenography, MEP, joinery, graphics, content |
| PMBOK coverage | Not required | Stripped from client docs (see Type B note) |
| Bilingual | AR/EN | AR/EN |
| Charts | Simple Gantt + timeline | 6+ SVGs: org chart, workflow, Gantt, escalation, QC, risk heatmap (all redesigned with navy/sky/green palette) |
| Compliance matrix | Not typically | 38–50 items covering all categories |
| RACI matrix | Not typically | 14 roles × 37 activities |

When the user says "proposal" or "technical proposal" for an exhibition/museum/interactive experience, use Type B instead of Type A.

## Multi-Store Tender Program — Supplier Data to Proposals

### Overview
When a supplier sends raw pricing (Excel) for multiple stores/outlets under a single brand program (e.g., Saudi Coffee — 10 stores, 4 client companies), the workflow is:

1. **Extract & classify** — Read the supplier Excel with openpyxl. Classify each line item as Construction / Equipment / Operations using Arabic keyword rules (same classification as Samaya costing).
2. **Identify pricing coverage** — Determine which stores have actual pricing data vs which are gaps.
3. **Create Study Report** — `PROPOSAL_STUDY_REPORT.md` covering: store inventory & data status, pricing analysis, style-guide compliance gaps, store-specific profiles, update plan with priority order.
4. **Build framework proposals** — For stores with data: fully priced 12-page HTML proposal. For stores without: full framework with all sections present, BOQ rows as "TBD — awaiting supplier quotation" with an amber badge, and a note in the executive summary.
5. **Reuse template** — All stores share the same HTML template; only the store name, scope description, and pricing section differ. Build the template once, parameterise the 4-5 variable fields.

### Framework vs Complete Proposal

| Feature | Complete (has data) | Framework (TBD pricing) |
|---------|-------------------|------------------------|
| Cover page | Store name, client, location | Store name, client, location |
| Company profile | Full Samaya credentials | Full Samaya credentials |
| Scope of Work | Store-specific trades | Generic Saudi Coffee scope |
| Technical approach | Standard (SASO/SBC/NFPA) | Standard (SASO/SBC/NFPA) |
| Schedule | 12-week timeline | 12-week timeline |
| Quality & HSE | Standard | Standard |
| Risk register | 5 risks | 5 risks |
| Team structure | Samaya org chart | Samaya org chart |
| **BOQ / Pricing** | ✅ **Itemised, loaded rates** | ⚠️ **TBD placeholder — all values empty** |
| Appendices | Certificates + portfolio | Certificates + portfolio |

### Pricing Gap Handling
- Stores without supplier data: every BOQ cell shows `—` or `TBD` text, never 0 or blank (0 implies free).
- Add a yellow/amber note banner at the top of the BOQ page: "🔶 Pricing pending supplier confirmation — estimated values will be inserted upon quotation receipt."
- In the study report, flag the gap with priority (HIGH/MEDIUM/LOW) and the contact who needs to follow up (e.g., "Ibrahim — supplier").

### Study Report Structure
The `PROPOSAL_STUDY_REPORT.md` must contain these sections:
1. Executive Summary
2. Store Inventory & Data Status (table per company)
3. Pricing Data Analysis (available data with category breakdown)
4. Style Guide Compliance Gap Analysis
5. Best Practice Tender Bracket Compliance
6. Store-Specific Profiles
7. Update Plan (immediate actions vs next steps requiring external input)
8. HTML Template Architecture
9. Appendices

### File Organization
Proposals live under `~/_Final Folder/{COMPANY}/{STORE}/index.html`:
- Company directories: `Qahwitna comp.`, `Rateeb Trading Com.`, `Tezkarat Trading Com.`, `Tiba Gift comp.`
- Store directories: numbered prefix + English store name
- Source pricing data: `~/projects/{project-name}/`
- Study report: `~/projects/{project-name}/PROPOSAL_STUDY_REPORT.md`
- The `clients/` mirror under `~/projects/{project-name}/clients/` mirrors the _Final Folder structure

### Template Architecture
Each proposal is a self-contained HTML file (no external dependencies except Google Fonts):
- 12 pages (sections): Cover · TOC · Company Profile · Project Understanding · Scope of Work · Technical Approach · Schedule · Quality & HSE · Risk Management · Team Structure · BOQ/Pricing · Appendices
- Samaya base64-embedded logo
- Bilingual AR/EN with RTL support (IBM Plex Sans Arabic + Inter)
- A4 print-ready (@page A4 portrait, @media print with color-adjust:exact)
- Page numbers on every page
- CSS tokens: --primary #0F172A, --secondary #0284C7, --accent #B01E2F
- Div-balanced HTML (verify: open divs == close divs)

## Workflow

### Phase 1 — Research & Reference
1. Read `Obekan.pdf` for banner material TDS if present
2. Read `PROJECT.md`, `BOQ.md`, `Technical_Specification.md` for existing specs
3. Identify client name and location from user input or documents
4. **Logo collection** — Download client logo, designer logo, and Samaya logo concurrently:
   - Client: search their official website or Google Images, curl/download SVG or high-res PNG
   - Designer: same approach — identify the design firm (e.g., Boris Micka Associates) and find their logo
   - Samaya: use `Docs/Branding/Samaya-Logo.png` from OneDrive (191x71, RGBA PNG)
   - Convert all to base64 data URIs for HTML embedding: `python3 -c "import base64; b=base64.b64encode(open('logo.png','rb').read()).decode(); print(f'data:image/png;base64,{b}')"`
   - If SVG, inline the raw SVG directly in the HTML (no base64 needed, easier to style with CSS filter for light/dark backgrounds)
5. **Project document study** — When project PDFs exist (BoQ, detailed design, material schedules, furniture schedules):
   - Extract text using PyMuPDF (fitz): `python3 -c "import fitz; doc=fitz.open('file.pdf'); [print(p.get_text()) for p in doc]"`
   - For large PDFs (100+ pages/100K+ chars), extract all text to a markdown file for reference
   - Pipe key content to Kimi CLI for summarization: `pdftotext -layout file.pdf - | kimi -p "Summarize this PDF content with all specs, quantities, and technical data" --print -y`
   - Key things to extract: experience requirements (e.g., "project manager 35 yrs"), equipment specs, material/finish schedules, BoQ cost breakdown, designer/scenographer names
   - Reflect these findings in the proposal: mention specific years of experience, reference actual equipment models (QSC Core 510 DSP, LOPU LED, Crestron CP4), use actual material and finish names from the design drawings

> **If you are fixing an existing proposal based on an audit report**, skip to `Phase 2.5 — Fix from Audit Report` below.

### Phase 2.5 — Fix Proposal from Audit Report

When the user provides an audit report (from Kimi or another agent) and asks you to fix the proposal:

**Step 1 — Locate files**
- Find the proposal HTML (often in /tmp/ or the project folder — NOT always on OneDrive)
- Find the audit report (.md file)
- Read both fully

**Step 2 — Pre-flight check: verify which audit findings are still applicable**
Audit reports are often run against intermediate snapshots. Many findings may already be fixed.
Check each finding's current state with search_files before patching:
- `~1,500 m²` (area) — often already corrected
- `36 weeks` (schedule) — often already 52 weeks
- `available on request` (CVs) — may be reworded to "attached in Package B"
- `ER (Employer's Requirements)` (references) — may be cleaned

Only patch things that are actually wrong.

**Step 3 — Delegate the fixes via sub-agent (preferred), NOT raw kimi CLI**
```python
delegate_task(
    goal="Fix all issues from the audit report...",
    context="Proposal path, audit path, checklist of 22 fixes...",
    toolsets=["terminal", "file"]
)
```
The sub-agent has patch(), read_file, search_files, terminal — all needed for multi-fix HTML surgery with its own timeout. Do NOT use `kimi -p "..."` with PTY mode for this — it times out on files >150KB with 20+ fixes.

**Step 4 — Verify key fixes in the parent turn**
After the sub-agent returns, check: old area gone, old schedule gone, CVs note fixed, new appendix present, risks expanded, page count corrected.

**Step 5 — Report what was actually fixed vs already-fine**
Present a table showing: applied fixes, already-correct findings, and any blockers.

See `references/audit-driven-fix.md` for the full workflow with examples and pitfalls.

### Phase 3 — Build HTML Proposal

There are two approaches depending on proposal size:

#### Option A: Monolithic HTML (single file, <500KB, <30 pages)
4. Delegate visual design to Claude Code (the user expects this)
5. Use patch() operations — never rewrite entire file
6. Follow the standard proposal structure (Type A or Type B)

#### Option B: Build Pipeline (manifest + partials + build script, >500KB or >40 pages)

**⚠️ PREFER the simple concat approach (Option A) over a complex build pipeline.** The build pipeline with manifest.json, placeholders, and post-processing introduces fragility:
- Placeholder replacement failures (unreplaced `{{page_number}}` in output)
- Regex bugs in section-tag post-processing (the `>>` double-gt bug from not consuming `>` in the regex)
- Puppeteer timeouts on slow filesystems (OneDrive: ~44s to read 49 small files)
- Section numbering drift between manifest, page files, and assembled output

The simple concat approach (`base.html` + `scripts/assemble.py` + `pages/NN-title.html`) has none of these issues and produces correct output on first try. Only add post-processing engines AFTER the base document is accepted and stable.

**If you MUST use a build pipeline:**
For large proposals where the monolithic approach becomes unwieldy, use a build pipeline:

1. **Create `manifest.json`** — list every section with `id`, `type` (`cover`/`content`/`divider`), `title_ar`, `title_en`, `short_title_ar`, `continued` flag for multi-page sections, and `children` array for subsections.

2. **Create `template.html`** — HTML5 skeleton with `<html lang="ar" dir="rtl">`, Google Fonts, CSS link, `<main>{{body}}</main>`.

3. **Split into section partials** (`sections/{id}.html`) — each file contains ONE `<section class="page">...content...</section>` with placeholders:
   - `{{section_number}}`, `{{title_ar}}`, `{{title_en}}`, `{{short_title_ar}}` — from manifest
   - `{{page_number}}`, `{{total_pages}}` — auto-assigned by build
   - `{{doc_code}}`, `{{rev}}`, `{{date}}`, `{{chip_text}}`
   - `{{toc_placeholder}}` — for Table of Contents

4. **Create `scripts/build.js`** — reads manifest, renders partials via placeholders, then post-processes:
   - Count `<section class="page...">` elements for total page count
   - Assign `{{page_number}}` by scanning line-by-line (each section open increments counter, each `{{page_number}}` gets current value)
   - Replace `{{total_pages}}` with actual count
   - Section numbering: cover = page 1, first content = section 2 (offset +1)

5. **Create `scripts/validate.js`** — 30+ automated checks: tag balance, page numbers sequential, semantic HTML, CSS rules, no broken SVG attributes, no unfilled placeholders.

6. **Create `package.json`** with build/validate scripts.

**⚠️ Critical regex pitfall:** The section-tag regex MUST consume the entire tag including `>`:
```js
// CORRECT — consumes >, replacement adds one >
const pageRegex = /<section[^>]*class="[^"]*page[^"]*"[^>]*>/g;
// WRONG — leaves > unconsumed, produces >> at end of every section tag
// const pageRegex = /<section[^>]*class="[^"]*page[^"]*"/g;
```

**Working directory rule:** ALWAYS work in the user's project folder (`~/Documents/` or `~/Desktop/`). Never stage work in `/tmp` — the user explicitly requires project files remain in their workspace.
4. Delegate visual design to Claude Code (the user expects this)
7. **Embed logos on cover** — left side gets client logo (e.g., RCRC), right side gets Samaya branding + ref info. If a designer/consultant is involved, add their logo smaller between or below. Use SVG inline for vector logos, base64 data URI for PNG logos.
   - **Client logo:** Search the client's official website (curl their homepage, look for `.svg` or logo in HTML). Download SVG for clean embedding — SVGs render at any size, take CSS `filter:brightness(0) invert(1)` for dark navy covers, and don't bloat the file. Fallback: high-res PNG → base64.
   - **Designer logo:** Same approach — find their official site, curl their logo URL (e.g., `borismicka.com/images/logo-white.svg`).
   - **Samaya logo:** Use the official file at `_Style-Guides/samaya-rfi-style-guide/assets/samaya.png` (1885x621, RGBA transparent) for cover. For page headers (tiny 14px space), create a simplified SVG wordmark with the signature red "A" — but save to the project folder, NOT to the logos archives. The logos archives (`_Style-Guides/logos archives/`) should only contain official brand files. **Do NOT save custom/fake Samaya SVGs to the archives** — user will flag and ask to delete.
   - Cover party icons: 3-party row (Client · Designer · Contractor) with `filter:brightness(0) invert(1)` so they render white on the navy background. All SVGs should be full/real brand logos, not placeholder text or geometric approximations — user will catch fakes.
   - **⚠️ Cover party icons: no background —** `.cover-party-icon` must NOT have `background:rgba(255,255,255,0.15)` or any other background color. Logos sit directly on the navy cover. Add `.cover-party-icon img{filter:brightness(0) invert(1)}` to make all three logos white.
8. **Redesign all SVG charts** with Samaya brand colors (navy `#0F172A`, sky `#0284C7`, green `#16A34A`, red `#B91C1C`) — NOT generic greys or mismatch colors. Each chart should use brand-consistent gradients for depth.

### Phase 3 — Material Rules
- **Cement Board 12mm** is the default cladding (NOT ACP or bare banner)
- PVC Flex banner is MOUNTED ON the cement board surface
- Jotun Epoxy Mastic is default coating — never mention galvanizing
- Steel profile is "حسب التصميم الإنشائي / per structural calculation" — never specify HSS 200×200×8
- LED count: start at 120, subtract 1 fixture per ~12m of gate openings
- Gates break the fence — no banner/cladding on gates

### Phase 4 — BOQ Excel
1. Create `BOQ_Pricing_Model.xlsx` using Python (openpyxl)
2. 3 sheets: BOQ (with formulas), Pricing Summary, Notes
3. Sections: Steel Structure, Civil Works, Cement Board, Banner & Printing, Lighting & Electrical, Gates, Additional
4. Leave unit rates empty for user to fill
5. Auto-calculating totals with formulas
6. See `references/BOQ-structure.md` for full item list and formula pattern

> **For supply/manufacturing tenders (توريد عام, non-construction):** Use an alternative costing structure — Materials + Hardware + Labor + Logistics + OH&P. See `references/supply-tender-pricing.md` for the 4-cost-category model, Etimad PDF extraction tips, and 3-sheet Excel template.

### Phase 5 — Deploy
1. Copy `index.html` + `proposal_assets/` + `assets/` + `Obekan.pdf` to `/tmp/surge-full/`
2. **Large asset folders (>100MB from OneDrive):** directly copying folders like `assets/` (can be 781MB) times out via OneDrive. Instead:
   a. Extract all referenced asset paths from HTML (`src="..."` and `url('...')`) and CSS (`url('...')`)
   b. Copy only those files to `/tmp/surge-full/`, preserving directory structure
   c. If `index.html` was in a subdirectory using `../assets/` paths, `sed 's|\.\./assets/|assets/|g'` to flatten for Surge root serving
   d. Log any referenced-but-missing files — they won't break layout but show broken backgrounds
   e. See `references/surge-deploy-large-assets.md` for the full Python extraction script
3. **Image optimization before deploy:** If source images are camera-originals from a project photos folder (1-50MB each), batch-optimize to prevent Surge free-plan size rejection (~1GB cap). Use macOS `sips`:
   ```bash
   # Resize jpg/jpeg to max 1920px longest side, Q85
   find /tmp/surge-full/assets/ -type f \( -iname "*.jpg" -o -iname "*.jpeg" \) \
     -exec sips --resampleWidth 1920 --setProperty format jpeg \
       --setProperty formatOptions 85 {} --out {} \;
   ```
   This drops 1.4GB → ~55MB with no visible loss for screen/print. PNGs need separate handling — sips has limited PNG support. If PNGs are oversized, convert to jpg or use `pngquant`.
4. Deploy: `surge /tmp/surge-full/ <domain>.surge.sh`
5. Domain convention: `<project-name>.surge.sh` (e.g., `al-zaidi-parking.surge.sh`)
6. Always deploy from /tmp, NOT from OneDrive path (OneDrive causes Surge to fail for large copies)
7. After deploy, wait **10-30 seconds** for CDN propagation, then verify with `curl -s -o /dev/null -w "%{http_code}" https://<domain>.surge.sh` — expect 200
8. If HTTP 404 or 504 is returned on first check, it's CDN propagation — wait 10s and retry. If it persists, redeploy.
9. Verify assets: `curl -s -o /dev/null -w "%{http_code}" https://<domain>.surge.sh/proposal_assets/logo.png` for each asset type

### Phase 6 — SVG Project Timeline
When creating/redesigning the timeline Gantt chart, use inline SVG:
- **viewBox:** 820×250 (provides enough room for Arabic labels + 12 week columns + legend)
- **Label column:** left panel at x=0 to x=210 with light gray `#F9FAFB` background + separator line
- **Arabic labels:** use `text-anchor="end"` anchored at x=204 with `direction="rtl"` and `unicode-bidi="embed"` — this prevents overflow/hidden text
- **⚠️ Text clipping fix:** WITHOUT `direction="rtl"` + `unicode-bidi="embed"`, Arabic SVG text renders in document-order (left-to-right) and overflows the viewBox boundary on the left side. Adding these two attributes makes Arabic render right-to-left from the anchor point, keeping it fully visible. This was discovered after 3 redesign iterations — do not skip it.
- **Week spacing:** 50px per week (W0 at x=210, W12 at x=810)
- **Bar height:** 20px with `rx="4"` rounded corners + drop shadow filter
- **Gradients:** define `<linearGradient>` for each color category (prep=gray, steel=red, civil=amber, electrical=teal)
- **Legend:** at y=240, compact 4 items with 8px color swatches
- **Height constraint:** 250px total — leaves room for note paragraph + spec boxes below on the same page
- **Bar colors:** prep=`#374151`/gray, exec=`#B01E2F`/red, civ=`#D97706`/amber, elec=`#0D9488`/teal

### Page Overflow & Balancing
When pages overflow A4 or are visually unbalanced:
1. **Measure content lines** per page — find `<!-- PAGE N -->` and `<!-- PAGE N+1 -->` comments, count non-empty, non-comment lines between them
2. **Compact CSS first** — reduce padding, font-size, line-height on the overflowing page's table/card classes before moving content:
   - `.ds-table th/td` → `padding:2px`, `font-size:10px`
   - `.doc-card` → `padding:8px`, `min-height:68px`
   - `.pay` → `padding:5px`, `font-size:10px`
   - `.terms li` → `padding:7px 0`, `font-size:9px`
3. **Move content between pages** as a second resort — shift doc cards, summary bars, or signature blocks to balance line counts (target ~120-150 content lines per page)
4. **Remove Section 08 from BOQ** if items were distributed pro-rata — update Grand Summary to 7 rows
5. **Always update TOC + page numbering** after moving content between pages

### Page Overflow Split + Renumber Pattern
When a single page overflows A4 and needs to be split into two:
1. **Trim source page** — cut content at a natural boundary (end of table, section break). Target ~10-12KB max per page for dense content.
2. **Create new page file** — insert numerically between existing files (e.g., create `11b-title.html` between `11-*` and `12-*`). Use the same framework template.
3. **Renumber all subsequent files** — shift every file whose number >= insertion point up by 1. Handle gaps caused by previously removed divider pages.
4. **Rebuild and verify** — check the split page no longer overflows, and verify no other pages shifted content from the renumbering ripple.
5. **Update TOC** — add the new page entry with correct page number.
- Page 6 table too loose? Target these CSS selectors:
  - `.spec-table td` → `padding:2px 8px` (was 5px 12px)
  - `.ds-table td` → `padding:4px 10px` (was 9px 12px — biggest gain)
  - `.gantt-row` → `padding:6px 14px`, `.gantt-track` → `height:20px`
  - `.pay` → `padding:12px 14px`, `.pay .nm` → `margin-top:6px`
  - `.tds-stat` → `padding:6px 10px`
  - `.phase` → `padding:10px 12px`
  - `.terms li` → `padding:10px 0`
  - `.sign-card` → `padding:16px 18px 20px`
  - `.gantt-legend` → `padding:8px 14px`
  - Reduce `.ds-table .grp td` padding too (3px 10px)

## Structural Reorganization Audit (ADD/REMOVE/MOVE pages)
When you add, remove, or reorder a page, you MUST update ALL of these or navigation breaks:
1. `id="page-N"` attributes on `<section>` tags
2. Footer `Page <b>N</b> / Total` spans  
3. Footer `/Total` denominator (e.g., `/16` → `/17`)
4. TOC `href="#page-N"` targets (every anchor link)
5. TOC page number labels (`toc-page">N</span>`)
6. Section `<!-- PAGE N — TITLE -->` comments
7. Cover `PAGE 01 / N` text
8. `data-screen-label` attributes if page content changed
9. **The easiest mistake is updating 6 out of 9** — always run a verification script:
   ```python
   # Check for gaps/mismatches
   ids = set(re.findall(r'id="page-(\d+)"', content))
   footers = set(re.findall(r'Page <b>(\d+)</b> / (\d+)', content))  
   print(f"IDs: {sorted(ids, key=int)}")
   print(f"Footers: {sorted(footers)}")
   print(f"Total pages: {len(ids)}")
   ```

## CDN Propagation Delay
After `surge` deployment, the CDN edge nodes take **10-30 seconds** to refresh. During this window:
- HTTP 404 = old domain cache cleared, new deploy not propagated yet → wait 10s, retry
- HTTP 504 = CDN timeout → wait 10s, retry  
- After 30s, always 200 if deploy succeeded
- To verify quickly: `curl -s -o /dev/null -w "%{http_code}" https://domain.surge.sh`
- Do NOT redeploy unless 404 persists beyond 60s

### Samaya Logo: ALWAYS Use Real PNG (Never Fake SVGs)
- **Official logo:** `_Style-Guides/logos archives/samaya-logo-trans.png` (bilingual Arabic/English: lowercase "samaya" with red "a" + "investment")
- **Page headers (14px):** Embed the PNG as base64 data URI in CSS as a single background-image class (`.samaya-header-logo{width:90px;height:14px;background:url(data:image/png;base64,...) no-repeat center/contain}`) — do NOT create fake SVG text wordmarks
- **Cover bottom party icon:** Use the real PNG with `filter:brightness(0) invert(1)` for the navy background
- **Never save fake Samaya SVG logos to the archives** — user will flag and demand deletion
- **Never create uppercase "SAMAYA" with diamond accents** — the real logo uses lowercase "samaya" with red "a" and "investment" in black

### Cover Text Readability on Navy Background (#0F172A)
- **Minimum contrast:** All text on the navy cover must use high-contrast colors
- **Labels (Client:, Date:, etc.):** Use `rgba(255,255,255,0.78)` at minimum — NOT 0.5 (too dim)
- **Values:** Use `#fff` with `font-weight:600` for crisp readability
- **Party labels (RCRC·Client, BMA·Designer, SAMAYA·Contractor):** Use `rgba(255,255,255,0.85)` at `0.44rem` — do NOT use `var(--accent)` (green #16A34A) which is unreadable at small sizes on navy
- **Eyebrow ("عرض فني"):** Use `#7DD3FC` (bright sky blue) — NOT `#0284C7` which blends into navy
- **Contractor line:** Use `#CBD5E1` (light slate) — NOT `#94A3B8` (too dark on navy)

### Team Section: Use Real Samaya KPR Names
- **Do NOT use fabricated names** (e.g., "أحمد السعيد", "خالد العتيبي") — these will be flagged
- Use real Samaya team names from the Aseer Museum Key Personnel Register:
  - Eng. Waris Sultan (Project Director)
  - Dr. Waleed Abdelmabood Salah (BIM Manager)
  - Eng. Mohamed Samir (Site Manager)
  - Eng. Mohamed Sultan (Tech Office Manager)
  - Plus specialist firms: AD Engineering, ZNA Studio, Rawasen, Glasbau Hahn, Lumotion, Nama Consulting, Samaya Factory, Samaya Graphit
- Add qualifying footnote for specialists not yet approved for the project: "تم مخاطبتها وأبدت استعدادها — على أن يتم التعاقد الرسمي بعد الترسية"

### Project Experience: Use Real Photos from samayainvest.com
- **Do NOT use AI-generated text-only cards** for projects that have real photos on the website
- Source real project photos from `https://samayainvest.com/our-work/`
- Each card: `border:1px solid #e2e8f0; overflow:hidden` with 80px photo thumbnail + title + description
- Add footer note: "جميع الصور من مشاريع سمايا المنشورة على الموقع الرسمي samayainvest.com"
- For current projects without photos (e.g., Aseer Museum), use a gradient placeholder

### CDE Platform: ACC Not Aconex
- The project uses **Autodesk Construction Cloud (ACC)** as the CDE platform, not Aconex
- Replace all "Aconex" references with "ACC" in proposal text, tables, and workflow charts
- ACC workflow: Revit → ACC Docs (CDE) → Navisworks (clash) → ACC Review/Transmittal → Approval → ACC Publish

### Revision History: Draft Proposals
- For draft proposals where work started recently, only show **one entry** (Rev 00, current month)
- Do NOT fabricate past revision entries (e.g., Rev 01 submitted, future revisions placeholder)
- Description: "مسودة أولية — قيد الإعداد والتطوير"

### Arabic Font Enforcement
- Add `'Cairo'` as a fallback to ALL font-family CSS variables: `--font-heading`, `--font-body`, `--font-mono`
- This ensures any element with Arabic text falls back to Cairo instead of system default Arabic font
- Google Fonts import: `family=Cairo:wght@400;500;600;700;800;900`
### Section 33 (Site Visit) Content Rules
When writing the Site Visit & Field Observations section:
- **No personal names** — remove any engineer/manager names (e.g., "سلطان عيسى"). Use role titles only: "مدير فني (Technical Manager) + فريق فني مساعد"
- **No photo quantities** — remove "12 صورة", "6 صور", "3 صور", "صورتان", "صورة واحدة" and similar photo counts
- **No photographic register** — remove Section "33.1 سجل الصور الفوتوغرافية" entirely. Field observations table is sufficient.
- **Generic description**: "أسفرت الزيارة عن توثيق الملاحظات الميدانية الرئيسية التي شملت المداخل والواجهات الزجاجية والأعمدة ومنطقة المعرض والكشك العلوي." instead of specific photo counts and locations
- Renumber: after removing 33.1, renumber 33.2→33.1, 33.3→33.2, 33.4→33.3

### GitHub Version Control for Proposals
When the user wants version control:
1. The OneDrive path causes git operations to timeout (slow cloud sync)
2. **Always work from /tmp** for git operations:
   ```bash
   cp "/path/to/OneDrive/proposal.html" /tmp/proposal-repo/
   cd /tmp/proposal-repo
   echo "*.bak" > .gitignore
   git init && git add -A && git commit -m "message"
   git branch -m main
   gh repo create <owner>/<repo-name> --private --source=. --remote=origin --push
   ```
3. For subsequent commits, copy updated file to /tmp repo, commit, and push
4. Don't forget to copy updated file back to OneDrive after git operations
5. Check `gh auth status` first to verify GitHub CLI is logged in

When the user says "ask expert to redesign section X" or "make section X more advanced":
1. Read the current section content
2. Delegate to Claude with context about the project data (gallery names, specialists, specs)
3. Request specific deliverables: SVG workflow chart, enhanced data tables, gallery references, quality gates, testing standards
4. Keep bilingual Arabic/English format and page structure consistent
5. After sub-agent returns, verify div balance and check for overflow

### Design Stage Terminology Rules
- **ALWAYS check what BMA actually delivered** before describing the design stage. Don't assume — read the document filenames and content. As of Dec 2025, BMA delivered **RIBA Stage 4 (Detailed Design)** for most systems: Scenographic Design, Detailed Design CAD, AV BOQ/Specs/H&P, Lighting schedules, Material/Furniture schedules. The only gap is MEP/ELV (22 systems) which was not in BMA's scope.
- Correct terminology: "التصميم التفصيلي (RIBA Stage 4 — Detailed Design) مُسلَّم ديسمبر 2025"
- MEP/ELV note: "مع فجوة تصميمية في أنظمة MEP/ELV (22 نظاماً) يقع تصميمها على عاتق المقاول"
- This applies to any design firm — check actual document dates and stages before describing. Never guess.
- **Do NOT reference documents Samaya hasn't received.** The ER (Employer's Requirements) was NOT received. Replace ALL external clause references (`ER-X.X`) with:
  - **Internal section codes** (`ق.10`, `ق.14`, `ق.18`) for proposal-internal navigation
  - **Standards references** (SBC, ISO, NFPA, ASTM, SASO, ICOM) for compliance/normative claims
- **Do NOT reference documents Samaya authored** (SOW, ER, technical specs) as if they're external client-given documents. Samaya wrote them — citing them in the proposal is self-referential. Rephrase as topic descriptions.
- The compliance matrix column header is `المعيار` (not `المرجع (ER/SOW)` and not `المرجع (SOW/ق.)`). Show standards (SBC, ISO, NFPA, ASTM, SASO, ICOM) or section refs, not internal document codes.
- Replace "كراسة الشروط (ER)" and "نطاق العمل (SOW)" with "المتطلبات والمعايير" throughout.

### Page Overflow Prevention
- Use `min-height:297mm` NOT `height:297mm` so pages expand if content exceeds A4
- Add CSS rule `section svg{max-width:100%;height:auto}` — prevents SVG overflow
- For dense tables: reduce `eng-table td` padding from `4px 7px` to `3px 5px`, font from `0.5rem` to `0.48rem`
- Keep text content per section under ~5,000 chars for comfortable A4 fit
- Wide SVGs (>800 viewBox width): split title into Arabic + English lines to prevent overflow
- **Section 8 (Experience cards):** 12-13 cards over 3 pages, each page with 3-5 cards. Image height 80px (not 46px). 2-column grid. All images from samayainvest.com with unique URLs (no duplicates).

### Duplicate Part 01/Part 02 Structure Fix

When a proposal HTML file has TWO concatenated copies (Part 01 + Part 02 with separate cover pages):

**Detect:** Count `<section class="page page-cover">` — if > 1, the file has duplicate parts.

**Fix:**
1. Find the SECOND cover page: `second_cover = h.find('<section class="page page-cover">', first_cover + 50)`
2. Find where the UNIQUE Part 02 content begins (usually Section 9 after the duplicate sections 2-8): `s9 = h.find('<h2>9.', second_cover)`
3. Keep: Cover + Part 01 sections + Part 02 content from Section 9 onwards
4. Remove: Second cover (Part 02) + duplicate sections 2-8
5. Then renumber ALL pages sequentially

**Page renumbering (single-pass regex, avoid cascading bugs):**
```python
import re
pattern = r'<span class="pg-num">صفحة \d+ / \d+</span>'
matches = list(re.finditer(pattern, h))
total = len(matches) + 1  # +1 for cover (no page number)
for i, m in enumerate(reversed(matches)):
    pg_num = total - i  # backwards: last gets highest number
    h = h[:m.start()] + f'<span class="pg-num">صفحة {pg_num} / {total}</span>' + h[m.end():]
```
- Go BACKWARDS to avoid offset shifts
- Use `<span class="pg-num">` as the anchor, not raw "صفحة X / Y" text (prevents matching TOC entries or content text)
When a file accidentally has TWO copies of `</style></head><body>` (e.g., from concatenated Part 01 + Part 02), the browser treats ALL CSS between the first `</style>` and the second `</style>` as raw text content — causing the page to show CSS code instead of rendered HTML.

**Fix:** Find the SECOND `</style></head><body>` block (unique context: preceded by `.cover-party-icon` CSS rule) and delete it. Then restore any accidentally-removed first block. Verify:
- `<style>` opens == `</style>` closes
- `<head>` == `</head>` == 1
- `<body>` == `</body>` == 1

### Table Column Width Pattern
For 4-column engineering tables in A4 proposals, use these explicit percentage widths that sum to 100%:

| Columns | Width pattern | Example use |
|---------|--------------|-------------|
| 4 columns | `8%` `30%` `44%` `18%` | Stage/Phase tables (stage, description, deliverables, responsible) |
| 5 columns | `8%` `22%` auto `14%` `12%` | Equipment schedules |
| 3 columns | `8%` auto `65px` | TOC (`#`, section name, page) |

**Always** add `table-layout:fixed` to the global `table` CSS rule so the browser respects width percentages instead of auto-sizing by content.

### SVG Timeline Chart Construction Rules
When building or fixing the Programme Timeline Gantt chart:

1. **ViewBox:** `0 0 840 230` minimum — title at y=14, phase bars from y=60 to y=170, legend at y=178
2. **Title:** Split into TWO lines — Arabic line (font-size 9), English line (font-size 7, `#64748B`). Never one combined line with "·" separator
3. **Phase bands:** Use `<rect>` with `rx="2"` (rounded rectangles), NOT `<polygon>` trapezoids which waste text space. 5-7 phases at 20-22px vertical step. Bar height = 16px.
4. **Legends:** Place INSIDE the SVG at bottom (y=178), with a `#F8FAFC` fill background box. Never outside the SVG.
5. **Labels:** Keep phase labels short — "المخططات" not "المخططات التنفيذية" — at font-size 8 bold white. Left-side labels at font-size 5, `fill-opacity:0.3`, `text-anchor:end` at x=22.
6. **Milestones:** Use dashed vertical lines at full SVG height with `stroke-dasharray="2,3" opacity="0.12"`.
7. **Grid:** Light gray `#CBD5E1` vertical lines at `opacity:0.3`, horizontal grid lines at `stroke-opacity:0.4`.
8. **Colors (monochrome only):** Navy `#0F172A`, `#475569` (slate), `#1E293B` (dark navy) alternating. No green, sky blue, red, or accent colors in the chart.

### Cover Page in Print
- **Do NOT hide** `.cover-wrap::before` in `@media print` — keep a solid gradient so the cover has full-page background
- Add these in the print block:
  ```css
  .cover-wrap::before{background:linear-gradient(180deg,#F6F8FC,#EDEEF2)!important;display:block!important;content:""!important}
  .page.cover{padding:0!important}
  .cover-wrap{min-height:1123px!important}
  ```
- Regular page decorative gradients SHOULD be hidden: `.page::before{display:none!important}`

## Sign-Off Blocks Layout
- Both signature blocks (Client + Contractor) should display **side-by-side** on the last page
- Wrap both in a flex container: `<div style="display:flex;gap:16px">` — the `.sign` CSS already has `grid-template-columns:1fr 1fr` but the inner content uses `sign-card`, so the outer structure is `flex` with gap
- Remove `margin-top:16px` from `.sign` CSS when using a flex wrapper — the wrapper handles spacing
- Order: Client signature on the left, Contractor signature on the right

## Sign-Off Integrity Audit (pages 16-18)
When splitting content between the last 3 pages, orphaned `<div>` tags cause broken rendering:

### Page 16 orphan pattern
After moving signature blocks off page 16, a fragmented `sign-line` + `sign-fields` block may remain between the doc-sum closing `</div>` and the footer. This causes 2 extra `</div>` closes (opens=116, closes=118). Fix:
```python
# Find the doc-sum end
sr = page16.find('جميع الوثائق الرسمية سارية المفعول')
sr_close = page16.find('</div>', sr)
doc_sum_close = page16.find('</div>', sr_close + 6)
footer = page16.find('footer class="pf"')
new = page16[:doc_sum_close+6] + page16[footer:]
```
Then add the missing deck container close before `</body>`:
```python
body_end = content.rfind('</body>')
content = content[:body_end] + '</div>' + content[body_end:]
```

### Per-page div verification
```python
for pg in range(1, 20):
    m = f'PAGE {pg} —'
    nm = f'PAGE {pg+1} —' if pg < 18 else 'TWEAKS PANEL'
    s = content.find(m)
    if s < 0: continue
    e = content.find(nm, s) if pg < 18 else len(content)
    sec = content[s:e]
    o = len(re.findall(r'<div\\b', sec))
    c = len(re.findall(r'</div>', sec))
    if o != c: print(f'Page {pg}: {o}/{c} diff={o-c}')
```
A single stray `<div class="deck">` at the file start needs `</div>` added before `</body>`. The overall file has `<div class="deck">` before page 1 but the closing is often missing. Always check deck balance.

## openpyxl Excel Reading (data_only=True)
When reading the BOQ_Pricing_Model.xlsx, ALWAYS use `data_only=True` in `load_workbook()` — otherwise cells with formulas return `None` instead of computed values:
```python
wb = load_workbook(path, data_only=True)
ws = wb['Option C - BOQ (Loaded)']
```
Without this flag, `.value` on formula cells returns `None` and all BOQ sync attempts silently produce empty values.

## Content Balancing Between Pages 16-17
When doc cards overflow page 16 or payment/terms overflow page 17:
1. First compact CSS (reduce padding, font-size on `.doc-card`, `.pay`, `.terms`)
2. Move doc cards from page 16 to page 17 (or vice versa) — keep doc-sum + available-on-request card with the doc cards (same topical group)
3. The closing block (وتفضلوا بقبول فائق التحية والاحترام) belongs on the LAST page BEFORE signatures
4. After ANY move, run the div balance verification above

### Critical Rules for Type B (Exhibition) Proposals

1. **No prices in technical proposals.** Technical proposals describe methodology, approach, and qualifications only. All monetary values (USD, SAR, $ amounts) must be removed. Replace budget references with "Budget Classification" or scope descriptions. The commercial proposal is a separate document.

2. **Formal engineering palette only.** The old bright palette (`#0284C7` sky blue, `#F59E0B` amber, `#10B981` green) was explicitly rejected as unprofessional. All charts must use the formal palette from `samaya-doc-engine`: `#1E40AF` deep navy, `#92400E` dark amber, `#065F46` dark teal, `#4338CA` deep indigo, `#991B1B` dark burgundy. Load `samaya-doc-engine` and use its CSS tokens.

3. **Block layout only on `.page` — no flex.** Never use `display:flex; flex-direction:column` on `.page`. Flex distribution pushes content DOWN from the title, creating white space the user explicitly rejected. Use `position:relative` block layout. The `h2-row` has `margin-bottom:6px` — enough spacing.

4. **Content flows directly after title.** If a page is sparse, add content (KPIs, data tables, detail paragraphs) rather than using flex to stretch. Adding content is preferred over CSS hacks.

3. **SVG viewBox must fit all content.** Check the maximum y + height of every SVG element. If any element exceeds the viewBox height, increase the viewBox. Clipped SVGs look broken.

4. **Team names go through iterative corrections.** Expect multiple rounds of updates as the user refines the team roster. Use the actual names from PEP or KPR documents — never fabricate names. Common corrections:
   - Project Director: Waris Sultan → Adel Darwish
   - Design Manager → Technical Office Manager: Eng. Mohamed Sultan
   - Commercial Mgr: TBC → Abdallah Mahfouz

5. **Work in the user's project folder.** Always use `~/Documents/<project>/`. Never stage work in `/tmp` — the user explicitly rejects this.
- **ALWAYS work in the user's project folder** (`~/Documents/` or `~/Desktop/`). Never stage work in `/tmp` — the user explicitly requires project files remain in their workspace. The user will call this out as a critical error.
- Exception: Surge deployments and git operations on OneDrive files may temporarily stage in `/tmp`, but the build source files (page partials, manifest, CSS) must be in the user's project directory.
- **Exhibition/Museum Fit-Out (Type B):** Load `samaya-doc-engine` alongside this skill for the structural build pipeline (CSS tokens, auto-numbering engine, chart library, page anatomy). This skill covers proposal CONTENT; `samaya-doc-engine` covers the STRUCTURAL FRAMEWORK.
- **A4 print CSS:** Use `@page{size:A4;margin:0}` — NOT `size:A4 portrait` (Safari-incompatible). Page class: `width:210mm;height:297mm;padding:12mm 16mm;box-sizing:border-box`. Add `overflow:visible;height:auto;min-height:297mm` in `@media print` to prevent content clipping.

## Related Skills

- **`samaya-doc-engine`** — For the structural framework (CSS tokens, auto-numbering engine, chart library, page anatomy, build pipeline). Load this alongside `samaya-proposals` for Type B (exhibition/museum) proposals. This skill covers proposal CONTENT; `samaya-doc-engine` covers the STRUCTURAL FRAMEWORK.
- **`samaya-factory-deploy`** — For deploying to samaya-factory.com shared hosting via SSH
- **`web-deployment`** — For deploying to Surge.sh or other hosting

## Pitfalls
- **CSS @import ordering** — `@import url(...)` MUST be the very first line after `<style>`, before any other rule (`@page`, body, @media, etc.). If any CSS rule precedes `@import`, browsers silently ignore it and fonts never load. No console error to hint at this.
- **Style guide validation** — Before building ANY HTML proposal, check `OneDrive/Samaya/Technical Office/_Style-Guides/` for the authoritative style guide. The exhibition/PMBOK design system uses Navy/Sky/Green palette and Montserrat/Inter/IBM Plex fonts — NOT the old bronze/gold/Playfair/Tajawal system that some reference files may still document.
- **Do NOT rewrite entire HTML files** — use patch() for targeted edits
- **Do NOT use branch for Surge credentials** — login via `surge login` interactively or use saved token
- **Prefer delegate_task over raw kimi CLI for large proposal fixes** — `kimi -p "fix all" --print -y` with PTY mode regularly times out at 600s on files >150KB with 20+ fixes. Use `delegate_task(goal="...", toolsets=["terminal","file"])` instead -- the sub-agent has its own timeout and full access to patch(), read_file, search_files, and terminal for multi-fix HTML surgery.
- **Samaya logo: ALWAYS use the real PNG — never create fake SVGs** — The official Samaya logo is at `_Style-Guides/logos archives/samaya-logo-trans.png` (50871 bytes, RGBA transparent PNG). It shows lowercase "samaya" with red "a" + "investment" in Arabic (الاستثمارية) and English.  
  - **Page headers:** Embed the PNG as a CSS background-image class (single instance reused across all headers). Do NOT create fake uppercase "SAMAYA" SVGs with diamond accents — the user will flag them as "wrong logo".  
  - **Cover bottom party icon:** Same PNG with `filter:brightness(0) invert(1)` for the navy cover.  
  - **Archives rule:** Do NOT save ANY custom/fake Samaya SVGs to `_Style-Guides/logos archives/` — only official brand files live there.  
  - If you need a small inline logo for page headers, use the CSS background-image approach (60-90px × 14px) which scales the real PNG cleanly.  
- **Pi agent Python 3.14 compatibility** — Pi uses the Python 3 `imp` module which was removed in Python 3.14. If `pi -p` fails with `AttributeError: 'FileFinder' object has no attribute 'find_module'`, fall back to executing the task directly or using another sub-agent (Claude, Codex, Kimi).

## References

- `references/html-template.md` — Base HTML template for A4 proposals.
- `references/tender-proposal-checklist.md` (from `samaya-doc-engine` skill) — Build pipeline checklist for tender proposals
- `references/pdf-study-and-logos.md` — Studying project PDFs and downloading/embedding client logos for tender proposals.
- `references/pdf-extraction-pipeline.md` — Extracting text from project PDFs via PyMuPDF for scope analysis and technical content gathering.
- `references/supplier-data-classification.md` — Converting raw supplier pricing Excel data into Samaya-branded HTML proposals: Excel structure, Arabic keyword classification rules, store inventory patterns, framework vs complete proposal logic, and the PROPOSAL_STUDY_REPORT.md format for multi-store tender programs.
- `references/supply-tender-pricing.md` — Costing model for supply/manufacturing tenders (non-construction): 4 direct-cost categories (materials, hardware, labor, logistics) + OH&P loading, Etimad PDF extraction tips, and 3-sheet Excel template.
- **Do NOT reference Samaya-authored documents** — If Samaya wrote the SOW, ER, or technical specs, do not cite them in the proposal as if they're external requirements (`"Per ER §2.1"`, `"per SOW"`). Remove the reference or rephrase as `"Excluded — client scope"`.
- **⚠️ ER document not received — use internal section refs only:** The Employer's Requirements (ER) document was NOT received. Replace ALL `ER-X.X` clause references with internal proposal section codes (`ق.10`, `ق.14`, `ق.18`, etc.). Replace "كراسة الشروط (ER)" with "نطاق العمل (SOW)". The compliance matrix column header becomes `المرجع (SOW/ق.)` instead of `المرجع (ER/SOW)`. Only reference documents Samaya actually has in hand.
- **Do NOT mention galvanizing** — use Jotun Epoxy Mastic
- **PMBOK stripping is mandatory for client delivery** — Every Type B (exhibition/museum) proposal must have ALL PMBOK jargon removed from headings, strips, chips, and body. `grep -c 'PMBOK'` must return 0. The exception is internal management docs only.
- **Codex CLI for HTML fixes** — When the user says "fix by codex" (logo placement, layout, styling), delegate to Codex CLI: `cd <dir> && codex -p "Embed these 3 logos..." --print -y`. Codex handles precise HTML embedding well.
- **Arabic RTL in SVG** — Any SVG containing Arabic text must use `direction="rtl"` + `unicode-bidi="embed"` on the text elements. Without both, Arabic renders left-to-right and overflows the viewBox boundary.
- **Do NOT hardcode "3 مشاريع متزامنة"** — use flexible phrasing like "قدرة تنفيذ مشاريع متزامنة — إدارة مرنة للجداول"
- **Do NOT split Technical Specs from Material Datasheets** in the TOC — they are one section
- **Do NOT put Lighting in Execution Plan TOC category** — it's a technical spec sheet under Technical Scope
- **Do NOT deploy directly from OneDrive path** — copy to `/tmp/surge-full/` first. OneDrive cloud-sync causes timeouts copying large folders (>100MB). Use selective-asset extraction (Phase 5 step 2) for large sites.
- **Always fix double-quote bugs** in id attributes: `id="page-1""` → `id="page-1"` (automated scripts often introduce these)
- Cover page uses `<section class="page cover">` — not same pattern as regular pages. When adding id, ensure `class="page cover"` is preserved, not split into `class="page" cover"`
- **Cover background in print:** do NOT hide `.cover-wrap::before` in `@media print` — give it a solid gradient instead (`background:linear-gradient(180deg,#F6F8FC,#EDEEF2)`). Also add `.page.cover{padding:0}` and `.cover-wrap{min-height:1123px}` in the print block so the cover fills the full printed page.
- **After adding/removing/reordering a page, audit ALL of these or navigation breaks:** `id="page-N"` attributes, footer page numbers, footer `/total` denominator, TOC `href="#page-N"` targets, TOC page number labels, section `<!-- PAGE N -->` comments, and the cover `PAGE 01 / N` text. The easiest mistake is updating 5 out of 6 and leaving one stale link.
- **LED count varies hugely by spacing:** 12m spacing = ~118 units, 2m spacing = ~711 units. Always check the Excel QUANTITY INPUTS section for the exact spacing value before assuming. When in doubt, ask the user.
- **Section 08 distribution creates fractional rates:** When Mobilization + Signage (28,480 SAR) is distributed pro-rata, rates become fractional (e.g., 111.44 instead of 110.50). The Grand Summary must be updated to 7 rows (remove Section 08). The grand total stays the same.
- **When moving content between pages 16-17, verify tag integrity:** Orphaned `<div class="sign">` without matching `</div>` causes floating/flush content. After any page remixing, verify: every `<div class="sign">` has a matching `</div>`, every signature card is properly wrapped, and the closing block has its correct ending. Use `grep -n '</div>' | grep 'sign'` to spot-check.
- **`doc-sum` and `Available on Request` cards belong with doc cards:** If doc cards move to page 16, move these too. They are topically related (documentation appendix) and keeping them together avoids contextually orphaned content.

### Sign-Off Verification (Last Page Integrity)

After any split or move involving pages 16-18, run these checks:

```python
# 1. Unique closing block
assert content.count("وتفضلوا بقبول") == 1

# 2. Client + Contractor signatures each exactly once
assert content.count("الطرف الأول") == 1
assert content.count("الطرف الثاني") == 1

# 3. Overall div balance
import re
opens = len(re.findall(r'<div\b', content))
closes = len(re.findall(r'</div>', content))
print(f"{'OK' if opens==closes else 'BROKEN'} - {opens}/{closes}")

# 4. Page-level div balance
for pg in range(1, 20):
    marker = f'PAGE {pg} --'
    start = content.find(marker)
    if start < 0: continue
    next_marker = f'PAGE {pg+1} --'
    end = content.find(next_marker, start)
    if end < 0: end = len(content)
    sec = content[start:end]
    o = len(re.findall(r'<div\b', sec))
    c = len(re.findall(r'</div>', sec))
    if o != c:
        print(f"  Page {pg}: {o}/{c} diff={o-c}")
```

The classic -2 imbalance on page 16 means stray sign-line/sign-fields fragments survived the content move. Fix by finding and removing the orphaned block between the doc-sum closing div and the footer.

### Last Page Structure (after split)

When the last page overflows, split into Payment+Warranty (page 17) and General Conditions+Sign-Off (page 18):

Page 18 order:
1. General Conditions list
2. `<div class="rule">` separator
3. Closing block ("وتفضلوا بقبول فائق التحية والاحترام")
4. `<div class="rule">` separator
5. Client signature card (الطرف الأول)
6. Contractor signature card (الطرف الثاني)

Rules:
- Closing block goes BEFORE signatures (on same page)
- Client signature before Contractor signature
- Each signature is its own `<div class="sign">` - do not nest
- Page 16 must NOT contain any signature or closing content
- Verify: `content.count("الطرف الأول") == 1` and `content.count("وتفضلوا بقبول") == 1`

## CSS Compaction (Targeted Overrides Block)

When the user says "compact all tables and charts" or "fix spacing across all pages":

**DO NOT** modify individual CSS declarations one-by-one — this takes 15+ patch calls and risks missing elements.

**DO** add a single dense CSS overrides block at the end of the `<style>` block, wrapped in `@media screen` with `!important`:

```css
@media screen{
  /* BOQ tables */
  .boq td,.boq th{padding:4px!important;font-size:10px!important}
  .boq tfoot td{padding:5px!important}
  .boq-group{margin-bottom:8px!important}
  /* Spec tables */
  .spec-table td,.spec-table th{padding:1px 8px!important;font-size:11px!important}
  /* Data sheets */
  .ds-table td{padding:2px!important;font-size:10px!important}
  /* Gantt/timeline */
  .gantt-track{height:14px!important}
  .gantt-row{padding:6px!important}
  /* Payment cards */
  .pay{padding:6px!important}
  .pay .pct{font-size:28px!important}
  /* Doc cards */
  .doc-card{padding:6px!important;min-height:70px!important}
  .docs-grid{gap:6px!important}
  /* Stats */
  .stat{padding:8px!important}
  .spec-box{padding:6px!important}
  /* Page gutters */
  .page{padding:40px 48px 56px!important}
  /* Section spacing */
  .sec-kicker{margin-bottom:4px!important}
  .sec-sub{margin-top:10px!important}
  /* Timeline milestones (p15-* classes) */
  .p15-card{padding:6px!important}
  .p15-item{padding-bottom:8px!important;min-height:50px!important}
}
```

**Benefits:** One operation, preserves `@media print` styles entirely, easy to revert, and catches all instances of each class across the entire file.

## Large HTML File Redesign Strategy

Files >150KB or >2500 lines timed out Claude Code delegation (600s limit). Strategy:

### Option A — CSS-only redesign (preferred, ~50% success)
Replace the `<style>` block in the `<head>` with new CSS while keeping all HTML content identical. This is much faster (~150K tokens vs ~400K for full rebuild) and the subagent is more likely to complete.

### Option B — Split into shell + content
1. Create structural shell first: `write_file` with 18 page sections, headers, footers, CSS, and placeholder content
2. Fill content per page group: delegate content-fill in batches of 4-5 pages
3. If content-fill file corruption occurs (0 bytes), revert to the working source file and try Option A instead

### Option C — Phase by page group
Delegate one group of related pages at a time:
- Group 1: Cover + TOC + Executive Summary (pages 1-3)
- Group 2: Scope + Capabilities + Specs (pages 4-6)
- Group 3: Datasheets + Drawings (pages 7-10)
- Group 4: BOQ (pages 11-12)  
- Group 5: Methodology + Timeline (pages 13-14)
- Group 6: Docs + Payment + Terms + Sign-off (pages 15-18)

## Post-Delegation Verification Checklist

After any subagent modifies a multi-page HTML file (even one page), verify ALL of these before reporting done:

```python
# 1. Page count
assert len(re.findall(r'<section class=\"page', content)) == 18  # or expected count
# 2. Section balance
assert content.count('<section') == 18
assert content.count('</section>') == 18
# 3. Style block balance
assert content.count('<style>') == content.count('</style>')
# 4. Footer page numbers (check sample)
# 5. Page heights via browser_console (should not exceed 1123px)
# 6. CSS selector scoping — new styles should not leak into other pages
```

## BOQ Loaded Sheet EXACT Match Rule

When the user says "match Option C - BOQ (Loaded) exact no more no less":

The BOQ must reproduce the Loaded sheet **exactly as-is**, including:
- **Section headers**: SECTION 01 — STEEL STRUCTURE · الهيكل المعدني (which is bold uppercase in Excel)
- **Item descriptions**: Full bilingual text verbatim from Excel (not shortened)
- **Loaded rates**: Use the exact loaded rate values (e.g., 111.44, not 85 base rate)
- **No OH&P lines in grand summary**: The loaded sheet shows only 3 summary rows — Grand Total excl VAT, VAT 15%, Total incl VAT. No separate Supervision/Overhead/Profit rows.
- **OH&P as info note only**: Add a compact note below the grand summary: "OH&P Loading: Supervision 8% + Overhead 10% + Profit 12% = Factor 1.30" — but do NOT include in the pricing table
- **Quantity Inputs**: Add as a compact info table at bottom of BOQ page 13 — 8 rows showing all dimension inputs
- **All 10 items (01-10)**: The loaded sheet has exactly 10 items numbered 01-10 across 7 sections. No additional items.
- **No Section 08**: If the loaded sheet distributes mobilization/signage pro-rata, remove Section 08 entirely and verify grand total unchanged

**Verification commands:**
```bash
python3 -c "
import openpyxl
wb = openpyxl.load_workbook('BOQ_Pricing_Model.xlsx', data_only=True)
ws = wb['Option C - BOQ (Loaded)']
# Check grand total
print(f'Grand Total: {ws[\"F35\"].value}')
print(f'VAT: {ws[\"F37\"].value}')
print(f'Total: {ws[\"F38\"].value}')
"
```

Then compare every item's qty, rate, and total from Excel against the HTML. All must match.

## Exhibition Proposal Patterns (Session 2026-06-27)

### Org Chart: 3-Tier Card Format (instead of SVG)

For Section 9 (Organization & Team) in Type B proposals, use a **3-tier layout** fitting one A4 page:

1. **Group-level** — Blue gradient banner (`linear-gradient(135deg,#F0F9FF,#E0F2FE)`) with "Samaya Group — Technical Directorate"
2. **Tier 1** — 2×2 grid of cards (`border:1px solid var(--primary)`, `background:white`) on `var(--bg-light)` background:
   - 4 cards: Project Director, Project Manager, BIM Manager, Tech Office Manager
   - Each: role label (muted uppercase), name/title, status (italic smaller)
3. **Tier 2** — Compact table with Role / Responsibilities / RACI columns:
   - 7-10 specialist rows (AV Lead, Lighting, Architect, BIM/CAD, MEP, HSE, QC, Procurement)
   - Font 0.45rem, RACI badges, legend below
4. **Tier 3** — Paragraph with left border accent (`border-right:3px solid var(--text-muted)`):
   - Technical staff counts by discipline
   - Factory resources
   - Total headcount (~34 persons)

This fits one A4 page, is easier to edit than SVG org charts, and matches the format established for Aseer Museum.

### Project Experience: Card-Based Layout (instead of table)

For Section 8 (Relevant Experience), use a **card grid** grouped by type:
- **Museums** (sky #0284C7) — group header + 2-column card grid
- **Exhibitions** (navy #0F172A)
- **Events** (red #d91e2e)
- Each card: `border-left:3px solid [color]`, `padding:6px 8px 6px 10px`, `background:#f8fafc`, `border-radius:4px`
- Card content: project name + year badge + scope description + client
- Summary footer: count per category

### Adding Photos to Experience Cards

Each project card can include a photo thumbnail. When adding photos:

**Preferred: Real photos from samayainvest.com** (not AI-generated)
- Source project images from `https://samayainvest.com/our-work/` 
- Use the `exp-card` format with inline styles (not abstract CSS classes):
  ```html
  <div style="border:1px solid #e2e8f0;border-radius:2px;overflow:hidden;background:#fff;">
    <div style="height:80px;overflow:hidden;background:#f1f5f9;">
      <img src="https://samayainvest.com/wp-content/uploads/YEAR/MONTH/FILENAME" 
           alt="NAME" style="width:100%;height:100%;object-fit:cover;">
    </div>
    <div style="padding:3px 8px 4px 8px;">
      <span style="font-family:'Cairo',sans-serif;font-size:11px;font-weight:700;color:#0F172A;">NAME</span>
      ...
    </div>
  </div>
  ```
- Image height: **80px** (was 46px — found to be too small for visual impact)
- Layout: 2-column grid (`display:grid;grid-template-columns:1fr 1fr;gap:6px`)
- 12 images across 3 pages, each from a UNIQUE URL (no duplicate images for different projects)
- Add footer note: "جميع الصور من مشاريع سمايا المنشورة على الموقع الرسمي samayainvest.com"

**Fallback: AI generation** (`image_generate`), existing renders, or base64 embedding for projects without public photos on the website. For current projects without photos (e.g., Aseer Museum), use a gradient placeholder.

**Distribution**: 4-5 cards per page across 3 pages, balanced by content length

### Page Numbering Fix: Regex Counter

When page numbers have duplicates/gaps (e.g., 20-27 repeats then jumps to 45), use single-pass regex instead of sequential replace():

```python
import re
current_page = 2
def renumber(m):
    global current_page; pg = current_page; current_page += 1
    return f'{m.group(1)}صفحة {pg} / 45'
html = re.sub(r'(<span class="pg-num">)صفحة \\d+ / \\d+', renumber, html)
```

Single-pass avoids the cascade bug where 10→9, then 11→10 collapses all pages to 9.
