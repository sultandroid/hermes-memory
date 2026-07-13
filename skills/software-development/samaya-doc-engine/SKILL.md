---
name: samaya-doc-engine
description: "Samaya Document & Engineering-Chart Framework v1.0 — build formal print-ready A4 engineering technical proposals as self-contained HTML with auto-numbering, SVG charts, RACI matrices, WBS, and bilingual (AR/EN) content."
version: 1.2.0
author: Samaya Technical Office
---

# Samaya Document & Engineering-Chart Framework v1.3

## Overview

This skill covers THREE output formats for Samaya-branded engineering technical proposals:

1. **HTML/SVG** — self-contained A4 print-ready pages with auto-numbering, SVG charts, bilingual content (the original focus)
2. **DOCX** — Microsoft Word documents using the `samaya_doc_template.py` Python class (python-docx wrapper)
3. **Review** — evaluating incoming technical proposals (from subcontractors, competitors, or Samaya's own drafts) using `references/technical-proposal-review-methodology.md`

Choose the format based on the deliverable: HTML for self-contained digital viewing/printing, DOCX for formal submission packages where the client expects editable Word documents.

## Quick Reference — DOCX Generation

DOCX generation uses the `samaya_doc_template.py` Python class (python-docx wrapper) at:
```
/Users/mohamedessa/Library/CloudStorage/OneDrive-SAMAYAINVESTMENT/Samaya/Technical Office/_Style-Guides/Doc Style Guide/samaya_doc_template.py
```

### SamayaDoc Class API

| Method | Purpose |
|--------|---------|
| `create_header(project_name, doc_ref, doc_type, revision, date)` | Standard Samaya header with logo + doc info strip |
| `create_footer(doc_number, confidential=True)` | Footer with page numbers, confidentiality notice |
| `add_h1(text)` | Document title — 18pt Bold Navy, bottom border |
| `add_h2(number, text)` | Section heading — 14pt Bold Navy, numbered, bottom border |
| `add_h2_u(text)` | Unnumbered H2 (front matter) |
| `add_h3(number, text)` | Subsection heading — 12pt Bold Dark Gray, bottom border |
| `add_body(text, bold=False, italic=False, size=11, color=None, align=None)` | Standard body paragraph |
| `add_rich_body(segments)` | Mixed-format body paragraph |
| `add_table(headers, rows, col_widths_cm=None)` | Styled table with navy header + alternating rows |
| `line()` | Small spacer paragraph |
| `save(path)` | Save to file |
| `save_temp(prefix='samaya_doc_')` | Save to /tmp with timestamp |

### Table Column Widths (A4, 16.5cm usable)

See `references/docx-proposal-structure.md` for the full width catalog. Common patterns:
- 2-col key-value: [4.0, 12.5]
- 3-col: [1.0, 12.0, 3.5] (TOC), [3.0, 8.0, 5.5] (descriptions)
- 4-col: [1.0, 5.0, 5.0, 5.5] (numbered lists)
- 9-col stakeholder register: [1.2, 3.5, 1.5, 3.5, 0.6, 0.6, 2.5, 1.5, 1.6]

### SVG → DOCX Image Rendering (CRITICAL)

cairosvg outputs RGBA PNGs, but Word on macOS does NOT render RGBA properly. Always convert to RGB:

```python
from PIL import Image
import io

def render_svg_to_rgb_png(svg_content, width=1600):
    import cairosvg
    png_data = cairosvg.svg2png(bytestring=svg_content.encode('utf-8'), output_width=width)
    img = Image.open(io.BytesIO(png_data))
    if img.mode == 'RGBA':
        bg = Image.new('RGB', img.size, (255, 255, 255))
        bg.paste(img, mask=img.split()[3])
        buf = io.BytesIO()
        bg.save(buf, format='PNG', optimize=True)
        return buf.getvalue()
    return png_data
```

**SVG XML pitfall**: Unescaped `&` in SVG text content (e.g. `T&C`, `O&M`, `D&B`) causes cairosvg XML parse errors. Always use `&amp;` in SVG text nodes.

**cairo library path**: On macOS with Homebrew, cairosvg needs `DYLD_LIBRARY_PATH=/opt/homebrew/lib` in the environment. Set it before running the script or wrap in a shell alias.

### Post-Processing Formatting Fixes

After generating content, apply these fixes for professional output:

```python
def apply_formatting_fixes(doc):
    # 1. pageBreakBefore on all H2 headings (14pt bold navy paragraphs)
    for p in doc.doc.paragraphs:
        runs = p.runs
        if runs and runs[0].font.size and runs[0].font.size == Pt(14) and runs[0].font.bold:
            pPr = p._p.get_or_add_pPr()
            pPr.append(OxmlElement('w:pageBreakBefore'))

    # 2. cantSplit on all table rows + compact cell margins
    for table in doc.doc.tables:
        for row in table.rows:
            trPr = row._tr.get_or_add_trPr()
            trPr.append(OxmlElement('w:cantSplit'))
            for cell in row.cells:
                tcPr = cell._tc.get_or_add_tcPr()
                tcMar = parse_xml(
                    f'<w:tcMar {nsdecls("w")}>'
                    f'  <w:top w:w="14" w:type="dxa"/>'
                    f'  <w:bottom w:w="14" w:type="dxa"/>'
                    f'  <w:start w:w="28" w:type="dxa"/>'
                    f'  <w:end w:w="28" w:type="dxa"/>'
                    f'</w:tcMar>'
                )
                tcPr.append(tcMar)

    # 3. 9pt halftone on descriptive/remark paragraphs
    remark_keywords = ["4 spheres of influence", "2x2 graphical classification",
                       "Project organisational structure", "5-tier escalation path"]
    for p in doc.doc.paragraphs:
        text = p.text.strip()
        if any(kw.lower() in text.lower() for kw in remark_keywords):
            for run in p.runs:
                run.font.size = Pt(9)
                run.font.color.rgb = SamayaColors.MEDIUM_GRAY
```

### Symbol Cleanup

Always run `clean_symbols(doc)` before saving to remove decorative Unicode characters and AI fingerprints:

```python
replacements = {
    '\u2014': ' - ', '\u2013': ' - ', '\u00b7': ' - ', '\u2022': ' - ',
    '\u00a7': 'Sec. ', '\u2192': ' > ', '\u25cf': '[P]', '\u25cb': '[V]',
    '\u201c': '"', '\u201d': '"', '\u2018': "'", '\u2019': "'",
    '\u00e9': 'e', '\u00e8': 'e', '\u00ea': 'e', '\u00eb': 'e',
    '\u00e0': 'a', '\u00e2': 'a', '\u00e4': 'a',
    '\u00f9': 'u', '\u00fb': 'u', '\u00fc': 'u',
    '\u00f4': 'o', '\u00f6': 'o', '\u00ee': 'i', '\u00ef': 'i',
    '\u00e7': 'c', '\u00b0': ' deg',
}
```

### Template Import Pattern

```python
_template_dir = "/Users/mohamedessa/Library/CloudStorage/OneDrive-SAMAYAINVESTMENT/Samaya/Technical Office/_Style-Guides/Doc Style Guide"
if not os.path.exists(_template_dir):
    _template_dir = "/Users/mohamedessa/Library/Group Containers/UBF8T346G9.OneDriveStandaloneSuite/OneDrive - SAMAYA INVESTMENT.noindex/OneDrive - SAMAYA INVESTMENT/Samaya/Technical Office/_Style-Guides/Doc Style Guide"
sys.path.insert(0, _template_dir)
from samaya_doc_template import SamayaDoc, SamayaColors
```

### DOCX Generation Script Structure

1. Import template + SVG constants
2. Define SVG rendering helper (with RGBA→RGB fix)
3. Define symbol cleanup function
4. Define post-processing formatting function
5. `main()`: create SamayaDoc → header/footer → add_h1 → add_h2/add_h3 → add_body/add_table → add_svg_to_doc → clean_symbols → apply_formatting_fixes → save

See `references/docx-proposal-structure.md` for the full section inventory and table width catalog.

#### Page Template

### Page Template
```html
<section class="page">
  <header class="page-header">
    <div class="header-info">
      <span class="doc-no">SMP-PROJ-TP-001</span>
      <span class="doc-rev">Rev 01</span>
      <span class="doc-status">IFR</span>
      <span class="doc-section">Project · Section Label</span>
    </div>
  </header>
  <div class="h2-row"><div class="h2-bar"></div><h2>N. AR_TITLE <span style="font-family:var(--font-body);font-weight:400;font-size:0.6rem;text-transform:none">- EN_TITLE</span></h2><span class="disposition-chip">CHIP</span></div>
  [CONTENT]
  <footer class="pg-footer">
    <span>Technical Office · المكتب الفني</span>
    <span>RESTRICTED · محدود</span>
    <span class="pgnum">Page <span data-page-current></span> of <span data-page-total></span></span>
  </footer>
</section>
```

### CRITICAL RULES

1. **NO PRICES in technical proposals.** Never mention monetary values ($/SAR/ريال/دولار) anywhere — in gaps, provisional sums, allowances, assumptions, risk registers, OR appendices. Replace with "(بتكلفة إضافية)" / "(additional cost)" or remove entirely. This includes:
   - Provisional sums (e.g. $549K for ELV, $80K for HVAC)
   - Any dollar/riyal amounts in risk registers, assumption tables, or gap analyses
   - KPI tiles showing project value
   - Gallery budget references in project understanding sections
   - Project values in experience/relevant-project tables
7. When stripping prices from the HTML, ALSO update the source `.md` files in `_PRICING_DOCS/` — they carry the same wrong values.
2. **NO icons, emoji, or AI symbols ANYWHERE.** Never use ✅❌⚠️⭐§™®🐱🚀🔥💡 or Bootstrap icons (`<i class="bi-...">`). Engineering proposals are text-only. Use plain labels (e.g. mark CV status with "مرفق" / "TBD", not ✅).
3. **Content flows directly after title.** No display:flex on .page. Use plain block layout.
4. **One page = one section.** Overflowing pages split into NEW page files, never condensed.
5. **NO hardcoded page numbers.** Use data-page-current / data-page-total auto-numbering.
6. **Tables are NEVER dismissed without replacement.** If a table is removed, its content must be merged into another table or replaced with equivalent structure.
7. **NO placeholder text like "المهندس / …………………."** Use actual names or titles (e.g. "مدير المبيعات / Sales Manager").
8. **Overflow = split, never delete.** Move content to new page.
9. **Verify every page file** has exactly 1 `<section>`, 1 `</section>`, 1 `<header>`, 1 `<footer>` — any imbalance corrupts the assembled document by swallowing subsequent pages into the unclosed section.
10. **Cover page Arabic text** must have explicit `color:#fff` — the parent div's color doesn't always cascade to the Arabic `<span>`.

#### Chart Design Standards

| Element | Rule |
|---------|------|
| Colors (formal ONLY) | #0F172A navy - #1E40AF deep blue - #92400E dark amber - #065F46 dark teal - #4338CA indigo - #991B1B dark red - #475569 slate |
| Colors (NEVER use) | #0284C7 sky blue (shiny) - #F59E0B bright amber (shiny) - #10B981 bright green (shiny) - #6366F1 bright indigo (shiny) - #16A34A green - #EA580C orange - #d91e2e bright red - #0369A1 light navy - #7C3AED purple - #1D8649 bright green |
| ViewBox width | 680px for most charts, 780px for wide flows (joinery manufacturing), 680×120-155 for curves |
| Arrow marker | markerWidth=8 markerHeight=5 refX=8 refY=2.5, polygon 0,0-8,2.5-0,5 fill=#0F172A |
| Feedback arrow | Same but fill=#991B1B, use marker-end=url(#arr_red) |
| Forward flow | Solid line, #0F172A, stroke-width:1 |
| Feedback/rework | DASHED line, #991B1B, stroke-width:1, stroke-dasharray:4,3 |
| Box roundness | rx=3 for all flow boxes |
| Font | font-family=Inter,Cairo,sans-serif |
| SVG wrapper | chart-card with cc-head, not bare svg-wrap |
| SVG responsive | Always: width:100%;height:auto;max-width:100%;display:block |
| Chart-card padding | 4px 6px for dense SVGs (default 12px 14px) |
| SVG overflow prevention | Check y+height ≤ viewBox height AND x+width ≤ viewBox width. Bottom info bars commonly overflow. |
| Gradient fills | Use linearGradient def, never hardcoded opacity fills in rects |

### Layout Rules
- .page uses position:relative;width:210mm;height:297mm;padding:12mm 16mm -- NO overflow:hidden (causes bottom-of-page clipping). Use plain block layout, no display:flex.
- Tables use table-layout:fixed to prevent column overflow
- SVGs in chart-card must have max-width:100%
- Footer CSS: position:absolute;bottom:10mm;left:16mm;right:16mm;display:grid;grid-template-columns:1fr auto auto;gap:8px;overflow:hidden
- NEVER add width:100% on footer with left+right positioning

### Auto-Numbering Engine
```javascript
function buildDocument(){
  const pages = [...document.querySelectorAll('.page')];
  pages.forEach((p, i) => {
    p.querySelectorAll('[data-page-current]').forEach(e => e.textContent = i + 1);
    p.querySelectorAll('[data-page-total]').forEach(e => e.textContent = pages.length);
  });
}
document.addEventListener('DOMContentLoaded', buildDocument);
window.addEventListener('beforeprint', buildDocument);
```

##### Appendix Creation
- Appendices use number-letter filenames for sort order: 48b=Appendix B, 48c=Appendix C, 48d=Appendix D, 48g=Appendix G (gaps allow future insertions between letter-codes)
- 48b between 48 and 49 sorts correctly alphabetically
- Appendix index page (appendix table of contents) must list ALL appendices with page numbers
- After adding/removing an appendix, update the appendices index page AND the TOC

###### NO Icons, Emoji, or AI Symbols
- **NO icons, emoji, or AI symbols ANYWHERE in the document.** This includes:
  - ✅ ❌ ⚠️ ⭐ — use plain text like "مرفق" / "TBD" / "ملاحظة"
  - Bootstrap icon tags `<i class="bi-...">` — replace with plain `<span>`
  - § ™ ® — remove entirely
  - Any Unicode decorative characters
- Engineering proposals are text-only formal documents. Visual distinction comes from tables, headings, and color-coded badges, NOT from emoji or icons.
* Cover page: Samaya logo SVG is OK (it's the official logo). Everything else must be text.
* Cover page Arabic company name (`شركة سمايا الاستثمارية`) must have explicit `color:#fff` in the `<span>` style — parent div color does not always cascade to RTL spans.
- Cover page Arabic company name (`شركة سمايا الاستثمارية`) must have explicit `color:#fff` in the `<span>` style — parent div color does not always cascade to RTL spans.

8. **Revision history**: NEVER list specific changes (area corrections, team updates, chart redesigns). Write generically: "النسخة المحدثة — تمت المراجعة والاعتماد وجاهزة للتقديم" (Updated version — reviewed, approved, ready for submission).

9. **Rev number**: Increment with every content change. Update BOTH the Document Control header AND the page headers (`<span class="doc-rev">Rev XX</span>`). Keep in sync.

10. **Page count**: After adding/removing pages, update the count in Document Control (`عدد الصفحات` field). If the count changes by more than 1, double-check file count.

11. **Arabic terminology — projector**: NEVER use "أجهزة إسقاط" (literal translation "projection devices"). Always use "بروجيكتور" (arabicized loanword) when referring to projectors (e.g. "بروجيكتور Epson").
1. Copy PDF CVs from source project (Aseer) to `pages/cv-*.pdf`
2. Strip all source-project logos, stamps, project references from the CV PDFs
3. Create appendix C page with table: #/Name/Role/Tier/Experience/Qualifications/CV status
4. Mark status: ✅=PDF attached, TBD=not yet available, —=reference only
5. CV PDFs sit in `pages/` alongside HTML (assemble.py ignores .pdf files)
6. Update appendices index page to show Appendix C as "مرفق"

###### RACI Appendix (B)
- Leadership strip: 10 roles with actual names from PEP
- RACI matrix: 11 roles × 10 activities
- Activities: Design, Shop Drawings, BIM, Procurement, Construction, AV, Testing, Quality, HSE, Documentation

###### Risk Register Appendix (D)
- Summary KPIs: count Critical/High/Medium/Low risks
- RBS codes: TEC, DES, MAN, HSE, SIT, LOG
- 14 risks max per page, 6 columns (ID/RBS/Description/Prob/Impact/Mitigation/Owner)

###### WBS Appendix (G)
- 9 work packages, max 46 elements
- Fit in 2 pages (or 1 at user's request)
- Font: 0.36rem for compact table
- Summary badges at bottom (9 packages, 46 elements, 52 weeks, PMI compliant)

##### Tag Balance Check (CRITICAL — HIGHEST PRIORITY)
After EVERY edit session, run this check on ALL page files. An unbalanced tag corrupts the entire assembled document by swallowing subsequent pages into the unclosed section:
```python
import glob
for f in glob.glob('pages/*.html'):
    c = open(f).read()
    opens = c.count('<section')
    closes = c.count('</section>')
    footers = c.count('<footer')
    if opens != closes or opens != 1 or footers != 1:
        print(f"CORRUPT: {f} sections={opens}/{closes} footers={footers}")
```
Fix a corrupted file by appending the missing closing tags at the end before any closing `</section>`.

##### Font Size Rules for Balanced Pages
| Context | Font Size | Notes |
|---------|-----------|-------|
| Standard eng-table | 0.4rem | Most data tables |
| Compact eng-table | 0.36-0.38rem | Dense content (TOC, WBS) |
| KPR Tier 1 table | 0.44rem | Key personnel register |
| Part headers | 0.4-0.42rem | Section category labels |
| CV Page 1 tables | 0.4rem | Summary + skills |
| CV Page 2 tables | 0.38rem | Experience timeline |
| Workforce summary | 0.36rem | 4-category deployment |
| TOC table | 0.36rem | 1-page goal |

##### File Renumbering (CRITICAL)
Never loop forward (12→13, 13→14…) — this renames files multiple times. Instead:
```python
# Get all files, sort descending, rename one at a time
for old_num in range(49, 11, -1):  # REVERSE
    # ... safe rename
```
OR: build a complete mapping first, then rename.

##### Sales Manager Signature
Letter signature line uses "مدير المبيعات / Sales Manager" — NOT "المهندس / …………………."

##### Post-Subagent File Re-read
After ANY delegate_task sub-agent modifies a page file, the parent session MUST re-read the file before writing. The sandbox cache is stale — writing without re-reading overwrites the sub-agent's changes.

##### Page Count & Rev Sync
After page count changes, update BOTH:
- Document Control: `عدد الصفحات</span><span class="value">N</span>`
- Rev number in Document Control header AND every `<span class="doc-rev">Rev XX</span>` in page headers
- Add revision history entry

##### Arabic Projector Terminology
NEVER use "أجهزة إسقاط" (literal translation). Always use "بروجيكتور" (arabicized loanword). Example: "بروجيكتور Epson" not "أجهزة إسقاط Epson"

##### Cover Arabic Text Color
`شركة سمايا الاستثمارية` on the cover page needs explicit `color:#fff` in the `<span>` style. Parent div color does NOT always cascade to RTL-direction spans.

##### Revision History Convention
Never list specific changes or corrections in the revision history. Use the generic format:
"النسخة المحدثة — تمت المراجعة والاعتماد وجاهزة للتقديم"
(Updated version — reviewed, approved, ready for submission)

###### Workforce Summary Table (Section 9.4)
When a detailed workforce table is needed alongside the curve chart, use a compact 4-category table:
- PM Team (14 peak, M3-4) — PM, Site Mgr, QS, Planning, QC, HSE, BIM, Doc Control, Procurement, Admin
- Civil & Demolition (27 peak, M4) — General labourers, demolition operatives, foreman
- Fit-Out (51 peak, M7-8) — Carpenters, scenic theming, painters, MDF/Corian, glass/metal
- AV Installation (29 peak, M8-9) — Technicians, cable pullers, rack builders, programmers, commissioning
Font: 0.36rem, compact class, 4 columns (Category/Peak/Month/Key Roles)

###### Curriculum Vitae (CV) Page Balance
CV pages often have white space at the bottom because the content is sparse. Fix:
1. Add `<div style="min-height:40px"></div>` after the last `</table>` before the footer to push content up
2. Or make the last table naturally fill the page by adding more detail rows
3. Ensure each person gets EXACTLY 2 pages (Part 1: Summary + Competencies + Skills; Part 2: Experience + Education + Certifications)

###### Gallery Names — Arabic Primary
Gallery names in matrices/tables should be ARABIC primary with English subtitle:
```html
<td><b>عاصمة المملكة</b><br><span style="font-size:0.32rem">Capital of the Kingdom</span></td>
```
The 7 galleries: G1=عاصمة المملكة, G2=مدينة الجمال, G3=الواحة المعاصرة, G4=المدينة الذكية, G5=المدينة الإنسانية, G6=استراتيجية الرياض, G7=المدينة في الزمن

##### CV Page Balance (CRITICAL)
CV pages often have white space at the bottom. Fix:
1. Add `<div style="min-height:40px"></div>` after the last `</table>` before the footer
2. Each person = exactly 2 pages: Part 1 (Summary+Competencies+Skills) and Part 2 (Experience+Education+Certifications)
3. Font size 0.4rem for tables
4. Use .strip for personal info block

##### Sales Manager Signature
Letter signature line uses "مدير المبيعات / Sales Manager" — NOT "المهندس / ……………………"

##### Structural (CRITICAL)
- display:flex on .page pushes content away from title -- use block only
- Hardcoded page numbers break when pages change -- always use JS engine
- File renumbering: loop renames already-renamed files. Fix: iterate REVERSE (highest to lowest) or list-based rename, NOT forward loop over full range
- Backup restore overwrites session work -- selectively restore missing files only, never bulk-restore over current work
- ALWAYS verify tag balance after edits: every page file must have `page.count('<section') == page.count('</section>') == 1` and `footer.count == 1`. A missing `</section>` tag swallows ALL subsequent pages into the unclosed section, corrupting the assembled document.
- After renumbering files: verify sort order in filesystem. Files with same prefix (e.g. 11- and 11b-) sort alphabetically — ensure correct order.
- Section numbering in content may diverge from file numbering after insertions/deletions — keep section numbers consistent within h2 tags.
- ALWAYS re-read a page file before editing if it was modified by a sub-agent — cached content causes overwrites.

##### SVG & Charts
- max-width:680px overflows 672px content area -- use max-width:100%
- SVG overflow: elements at x+width > viewBox width get clipped. Fix: increase viewBox width.
- SVG bottom overflow: elements at y+height > viewBox height get clipped. Always check all rect y+h values against viewBox height.
- Chart-card default padding (12px 14px) reduces inner width to ~644px. For wide SVGs, reduce padding to 4px 6px.
- Chart-card padding adds to border width: total inner padding = padding-left + padding-right + 2px (border).
- When reusing colors across process steps, ensure each step has a UNIQUE color. Never duplicate.

##### Footer
- Remove width:100% from footer when left+right are set (conflicts with absolute positioning)
- Footer needs `overflow:hidden` to prevent RTL Arabic text overflow
- Each footer span needs explicit `text-align` (left/center/right) per column
- Direction:ltr on footer with Arabic text causes overflow — use RTL-aware grid

##### TOC
- Arabic-only columns (no English), 3 columns (# / Arabic title / Page)
- Fit in 1 page (use compact font 0.36rem, tight margins)
- Needs Bootstrap Icons CDN in base.html `<head>`
- Page numbers: compute from assembled output, fill manually. Update when page count changes.
- Use `eng-table compact` not CSS grid for formal appearance

##### Data Integrity
- Area figures from PEP may be wrong — always verify against actual design drawing PDFs. (PEP said 3,500+ sqm, actual was 870 sqm from design DWGs)
- When document data changes (area, team names, spec numbers), also update source `.md` files in `_PRICING_DOCS/`
- After page count change: update Document Control page count and add revision history entry
- Rev number must increment with each content change. Document Control header and page footer must match.
- Letter signature: use "مدير المبيعات / Sales Manager" not generic placeholder "المهندس / …………………."
- Prices never appear in technical proposals. Strip all $/SAR values from pages and source MDs.

##### Proposal QA — Exclusions vs BOQ
- Before final submission, run the consistency check in `references/proposal-consistency-audit.md`. Items listed as "client responsibility" or "out of scope" in Section 34 must NOT have priced BOQ line items. Content Production (exclusion X2) is the most common contradiction.

##### Clarifications Wording — Equipment Brands (C1 Pattern)
When the proposal lists specific brands/models (LOPU LED, Epson, QSC, Nexmosphere, Chief etc.) in clarifications/assumptions section (Section 35.3), DO NOT phrase them as "confirmed/مؤكدة" brands. Instead, phrase as **equivalent alternatives meeting same spec**:

- CORRECT: "العلامات التجارية المقدمة (X، Y، Z) هي بدائل معادلة لنفس المواصفات الفنية المطلوبة"
- WRONG: "جميع المواصفات الفنية ... هي مواصفات مؤكدة" (implies exact brand match, creates liability if substituted)
- The quantities remain confirmed/مؤكدة — only brands get the "equivalent alternative" framing
- This protects Samaya from claims if an equivalent brand is substituted during procurement

##### Page Layout
- Content flows directly after h2-row — no display:flex on .page
- Overflowing pages SPLIT into new page files, never compressed.
- After page split: delete old file, renumber ALL subsequent files, verify assembled order.
- Part dividers (dark navy banners) count as pages. When removing them, renumber accordingly.
- TOC page numbers computed from assembled output, filled manually.
