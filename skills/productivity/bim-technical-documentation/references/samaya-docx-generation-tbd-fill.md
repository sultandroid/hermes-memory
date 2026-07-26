# Samaya-Branded DOCX Generation — Styling & TBD Filling

## Mandatory: Load the samaya-docx-template skill first

Before generating any Samaya-branded DOCX, load `samaya-docx-template` with `skill_view(name='samaya-docx-template')`. It defines the SamayaDoc class, import path, style rules, and table-width workaround.

## OneDrive template deadlock — detection and fallback

The SamayaDoc template lives on OneDrive and may be a **stale stub** (null bytes / `Resource deadlock avoided`) when OneDrive hasn't fully synced. **Priority order:**

1. **GitHub repo clone (preferred)** — no sync issues, always accessible:
   ```python
   import sys
   sys.path.insert(0, '/Volumes/MIcro/Temp/aseer-museum-pm/_Style-Guides/Doc Style Guide')
   from samaya_doc_template import SamayaDoc, SamayaColors
   ```
   Clone if not present: `git clone https://github.com/sultandroid/aseer-museum-pm.git /Volumes/MIcro/Temp/aseer-museum-pm/`

2. **OneDrive CloudStorage** — may return null bytes when sync is pending:
   `~/Library/CloudStorage/OneDrive-SAMAYAINVESTMENT/Samaya/Technical Office/_Style-Guides/Doc Style Guide/samaya_doc_template.py`

3. **Group Containers fallback** — same OneDrive content:
   `~/Library/Group Containers/UBF8T346G9.OneDriveStandaloneSuite/OneDrive - SAMAYA INVESTMENT.noindex/OneDrive - SAMAYA INVESTMENT/Samaya/Technical Office/_Style-Guides/Doc Style Guide/samaya_doc_template.py`

Always verify before importing: `f.read(100)` — if all null bytes, use the repo path instead.

## Manual Samaya styling fallback

When the SamayaDoc class is inaccessible, replicate the styling directly with python-docx. Samaya brand spec:

| Element | Style |
|---------|-------|
| **H1** | 18pt Bold Calibri, Navy #003366, UPPERCASE, bottom border (single, 8px, #003366) |
| **H2** | 14pt Bold Calibri, Navy #003366, two-arg format: `add_h2(number, text)` |
| **H3** | 12pt Bold Calibri, Dark Gray #333333, two-arg format |
| **Body** | 11pt Calibri, justified, colour #1A1A1A, 1.15 line spacing, 6pt space after |
| **Table header** | 9pt Bold Calibri, White, Navy #003366 background fill |
| **Table data** | 9pt Calibri, #1A1A1A, alternating row shading (#F2F6FA every other row) |
| **Table width** | `w:w="5000" w:type="pct"` (100% table width) |
| **Header** | 3-column table: left = "SAMAYA INVESTMENT / Technical Office", centre = title, right = doc ref + rev |
| **Header bottom border** | Single line, 4px, Navy #003366 |
| **Footer** | Centred: "Samaya Investment Company | HZL-SUP-XX | Rev X | Page X of Y" with top border |
| **Page margins** | Top/Bottom: 2.0cm, Left: 2.5cm, Right: 2.5cm |
| **Cover info table** | 2-column key-value with Navy header cells, White text |

### Key python-docx patterns for Samaya styling

```python
from docx import Document
from docx.shared import Pt, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn, nsdecls
from docx.oxml import parse_xml

NAVY = RGBColor(0x00, 0x33, 0x66)
DARK_GRAY = RGBColor(0x33, 0x33, 0x33)
BODY_COLOR = RGBColor(0x1A, 0x1A, 0x1A)

def add_h1(doc, text):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    p.paragraph_format.space_before = Pt(18)
    p.paragraph_format.space_after = Pt(8)
    p.paragraph_format.keep_with_next = True
    run = p.add_run(text.upper())
    run.bold = True
    run.font.size = Pt(18)
    run.font.color.rgb = NAVY
    pBdr = parse_xml(
        f'<w:pBdr {nsdecls("w")}>'
        '  <w:bottom w:val="single" w:sz="8" w:space="4" w:color="003366"/>'
        '</w:pBdr>'
    )
    p._p.get_or_add_pPr().append(pBdr)

def set_cell_shading(cell, hex_color):
    shading = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{hex_color}" w:val="clear"/>')
    cell._tc.get_or_add_tcPr().append(shading)
```

The full implementation (168 paragraphs, 32 tables, header/footer with page numbers) was generated for Heritage_Zone_Logistics_Supplement_HZL-SUP-01.docx on 26 Jul 2026. See that file in `MOBILIZATION/` for the complete working example.

## TBD filling rule — CRITICAL

**The user will reject documents with TBD fields left as placeholders.** Before generating any formal Samaya document:

1. **Check the project status** — search project files, email archive, existing plans, and registers for actual data
2. **Fill with best available estimates** where survey data is pending — use "estimated at X" or "to be confirmed by survey" rather than bare "TBD"
3. **Known defaults for heritage palace logistics** (when site survey hasn't been completed):
   - Gate widths: 4.5m main, 3.8m perimeter, 3.2m pedestrian zone
   - Height clearances: 4.2m main, 3.5m perimeter
   - Surface load ratings: 40t compacted gravel, 25t reinforced concrete
   - Crane reach: ~25m for 50t mobile crane, ~15m for 15t light crane
   - Showcase dimensions: ~3.0×1.5×2.5m (large), ~2.0×1.0×2.0m (medium)
   - Showcase weight: 800–1,200 kg (large), 400–700 kg (medium)
   - AV rack: ~0.8×0.6×2.0m, 150–250 kg
4. **Flag genuinely unknown items** as "to be confirmed by [survey/report]" — not bare "TBD"
5. **Add a note** about items needing verification in the body text or revision history

### What NOT to do
- ❌ Leave bare "TBD" in tables — the user reads this as incomplete work
- ❌ Use "TBD" with no explanation of what's needed to resolve it
- ❌ Use generic values without noting they're estimates pending survey

## Table handling in python-docx

```python
def add_samaya_table(doc, headers, rows, col_widths_cm=None):
    """Create a styled Samaya table with navy headers and alternating rows."""
    table = doc.add_table(rows=1 + len(rows), cols=len(headers))
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.style = 'Table Grid'
    
    # Header row — Navy bg, white bold text
    for i, h in enumerate(headers):
        cell = table.rows[0].cells[i]
        cell.text = ""
        p = cell.paragraphs[0]
        run = p.add_run(h)
        run.bold = True
        run.font.size = Pt(9)
        run.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
        set_cell_shading(cell, "003366")
    
    # Data rows — alternating shading
    for r_idx, row in enumerate(rows):
        for c_idx, val in enumerate(row):
            cell = table.rows[r_idx + 1].cells[c_idx]
            cell.text = ""
            p = cell.paragraphs[0]
            run = p.add_run(str(val))
            run.font.size = Pt(9)
            if r_idx % 2 == 1:
                set_cell_shading(cell, "F2F6FA")
    
    # Set table width to 100%
    tbl = table._tbl
    tblPr = tbl.tblPr
    tblW = parse_xml(f'<w:tblW {nsdecls("w")} w:w="5000" w:type="pct"/>')
    tblPr.append(tblW)
    
    if col_widths_cm:
        for row in table.rows:
            for i, w in enumerate(col_widths_cm):
                if i < len(row.cells):
                    tc = row.cells[i]._tc
                    tcPr = tc.get_or_add_tcPr()
                    tcW = parse_xml(f'<w:tcW {nsdecls("w")} w:w="{int(w*567)}" w:type="dxa"/>')
                    tcPr.append(tcW)
```
