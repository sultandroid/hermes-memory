# Standalone Subcontractor DOCX Pattern

Use when generating DOCX documents **for a subcontractor to submit TO Samaya** (methodology, programme, prequal docs). These must NOT use SamayaDoc or Samaya branding — they are the subcontractor's own documents.

## Flowcharts in DOCX: use SVG (preferred) or tables (for editability)

**First generation:** Use SVG charts via cairosvg — they render cleanly with proper boxes, arrows, and spacing at full width. Run with `DYLD_FALLBACK_LIBRARY_PATH=/opt/homebrew/lib`.

**If the user asks to edit charts:** Build as styled tables with arrow characters (`>` `v`) as connectors. Tables survive manual edits in Word.

**Do NOT use Word VML shapes** — python-docx cannot build them reliably; they produce microscopic boxes or corrupt the document.

### SVG Gantt chart axis convention

For programme Gantt charts: x-axis ticks = days from appointment (D0, D30, D50, D65, D80, D95, D110, D150, D220, D250). Each 10 days = approximately 5.28px on a 1600px-wide SVG (1320px for 250 days). Bars start at `200 + (start_day * 5.28)` px offset.

**Do NOT use calendar months** on the x-axis — use days-from-appointment. Calendar dates change if the appointment shifts; day-based charts stay correct regardless.

### Programme deliverables table: add DMP Gate, Day, and RACI columns

Use 6 columns: `Ref | Deliverable | DMP Gate | Day | Resp. | Review / Approve`

| Column | Content |
|--------|---------|
| DMP Gate | Pre-Design, G-1 Design Dev, G-2 Material Approval, G-3 IFC, G-4 Construction, G-5 Handover |
| Day | Day range from appointment (e.g. D30–D50) |
| Resp. | Who does the work (SDE, Subcontractor name) |
| Review/Approve | Who reviews/approves per RACI: NRS for design + materials, Samaya for IFC/commissioning/handover, CG final authority |

### RACI for acoustic specialist docs

| Role | Responsibility |
|------|--------------|
| **SDE / Subcontractor** | Design, supply materials, installation — RESPONSIBLE for all deliverables |
| **NRS** | Review and approve all design-related deliverables (criteria, specs, drawings, material submittals) — ACCOUNTABLE for design correctness |
| **Samaya** | Coordinates BIM, MEP interfaces, structural coordination — reviews IFC, commissioning, handover docs |
| **CG** | Final approval authority on all gates |

### Programme table: remove site survey phase when building shell exists

If the building already exists (fit-out project, not new build), do NOT include a "Site Survey" or "Baseline Noise Survey" phase. Design starts at D0 immediately upon appointment. The assumption line should state: "Design starts immediately upon appointment — no site survey phase needed (building exists)."

### Methodology doc: remove baseline noise survey section

When the building shell exists but fit-out hasn't started, there's nothing to measure — empty shell noise doesn't predict finished museum conditions. Remove the "Baseline Noise Survey" subsection entirely and renumber subsequent sections.

### Third-party reports: use as guide only, never cite as authority

When the project already has a pre-existing design report (e.g. iAcoustics Acoustic Design Strategy, NRS Material Spec), the subcontractor's methodology document must NOT reference that report as if it's their source. Frame everything as the subcontractor's own analysis:

| Don't | Do |
|-------|-----|
| "per iAcoustics Strategy V2" | "per project design criteria" |
| "NR30 per iAcoustics report" | "Target NR30 for galleries" |
| "Model using CadnaR per iAcoustics (ref. J3574)" | "Model using CadnaR particle model" |
| "Derogations accepted per iAcoustics" | "Accepted derogations: G1, G3/G14, G5" |

The subcontractor must present the methodology as their own deliverable, produced from first principles using the project's design criteria. The existing report informed their approach but is NOT their authority. The user explicitly corrected: "we use it as guide only we have to make our own report."

### Treatment products: describe as recommendations, not specifications

List preferred product families (Sonacoustic, Sonaspray, Filva-T, acoustic curtains) as "equivalent alternatives accepted" — these are the subcontractor's recommendations, not a specification they must follow.

### NR and LAeq targets: state as design criteria, not as quotes

Noise criteria (NR30 galleries, NR35 VIP, NR40 cafe, etc.) and ambient noise limits (LAeq,T 40 max for exhibition spaces) should be stated as SDE's own design targets derived from project requirements — not attributed to any third-party report. Same for vibration limits (0.05 m/s² per ISO 2631-2) and external noise boundaries (50 dB site boundary / 45 dB public). Reference only the governing ISO/BS standard, not the pre-existing study.

### Oddy test scope boundary

Oddy test only applies to materials **inside showcases or directly adjacent to exhibits**. Never list Oddy as a general acoustic treatment requirement — ceiling panels, baffles, wall absorbers, floor underlay do not need it. The user explicitly corrected: "Oddy test only required for items related to exhibition or object near."

### BIM coordination is Samaya scope, not subcontractor

Never show "BIM Coordination" or "RCP federation" as a subcontractor deliverable in methodology flowcharts or text. Samaya's BIM Manager handles coordination at LOD 300. The subcontractor provides treatment layout drawings per gallery and MEP input specs only.

## Table-based flowchart pattern (when SVG not suitable)

```python
BLUE = RGBColor(0x0D, 0x57, 0xA5)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)
BLACK = RGBColor(0x00, 0x00, 0x00)

def shade(cell, color_hex):
    tc = cell._tc
    tcPr = tc.get_or_add_tcPr()
    shading = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{color_hex}"/>')
    tcPr.append(shading)

def write_cell(cell, text, bold=False, color=BLACK, size=9, bg=None):
    cell.text = ''
    p = cell.paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run(text)
    run.font.size = Pt(size)
    run.font.bold = bold
    run.font.color.rgb = color
    run.font.name = 'Calibri'
    if bg:
        shade(cell, bg)

# Horizontal pipeline (2 rows x 5 cols)
table = doc.add_table(rows=2, cols=5)
table.alignment = WD_TABLE_ALIGNMENT.CENTER
write_cell(table.rows[0].cells[0], "STEP 1\nDescription", True, WHITE, 8, '0D57A5')
write_cell(table.rows[0].cells[1], ">", False, BLUE, 12)
write_cell(table.rows[0].cells[2], "STEP 2\nDescription", True, WHITE, 8, '0D57A5')
write_cell(table.rows[0].cells[3], ">", False, BLUE, 12)
write_cell(table.rows[0].cells[4], "STEP 3\nDescription", True, WHITE, 8, '0D57A5')
```

## Helper functions (copy into gen script)

```python
from docx import Document
from docx.shared import Cm, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml.ns import qn, nsdecls
from docx.oxml import parse_xml

NAVY = RGBColor(0x1E, 0x29, 0x3B)
DARK_GRAY = RGBColor(0x33, 0x41, 0x55)
MED_GRAY = RGBColor(0x64, 0x74, 0x8B)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)
BLACK = RGBColor(0x00, 0x00, 0x00)

def add_svg_logo(doc, svg_content, width_cm=6):
    import cairosvg
    png_path = "/tmp/logo_temp.png"
    cairosvg.svg2png(bytestring=svg_content.encode('utf-8'), write_to=png_path,
                     output_width=800, output_height=200)
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run()
    run.add_picture(png_path, width=Cm(width_cm))
    os.unlink(png_path)

def add_svg_flowchart(doc, svg_content, caption=""):
    import cairosvg
    png_path = "/tmp/flowchart_temp.png"
    cairosvg.svg2png(bytestring=svg_content.encode('utf-8'), write_to=png_path,
                     output_width=1600, output_height=550)
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run()
    run.add_picture(png_path, width=Cm(16.5))
    if caption:
        cap = doc.add_paragraph()
        cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run2 = cap.add_run(caption)
        run2.font.size = Pt(8)
        run2.font.color.rgb = MED_GRAY
    os.unlink(png_path)

def add_styled_table(doc, headers, rows, col_widths_cm=None):
    table = doc.add_table(rows=1 + len(rows), cols=len(headers))
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    for i, h in enumerate(headers):
        cell = table.rows[0].cells[i]
        cell.text = h
        for p in cell.paragraphs:
            p.alignment = WD_ALIGN_PARAGRAPH.LEFT
            for run in p.runs:
                run.font.size = Pt(9)
                run.font.bold = True
                run.font.color.rgb = WHITE
                run.font.name = 'Calibri'
        set_cell_shading(cell, '1E293B')
    for ri, row_data in enumerate(rows):
        for ci, val in enumerate(row_data):
            cell = table.rows[ri + 1].cells[ci]
            cell.text = str(val)
            for p in cell.paragraphs:
                p.alignment = WD_ALIGN_PARAGRAPH.LEFT
                for run in p.runs:
                    run.font.size = Pt(9)
                    run.font.color.rgb = BLACK
                    run.font.name = 'Calibri'
            if ri % 2 == 1:
                set_cell_shading(cell, 'F1F5F9')
    if col_widths_cm:
        for ri, row in enumerate(table.rows):
            for ci, w in enumerate(col_widths_cm):
                row.cells[ci].width = Cm(w)
    return table

def add_h1(doc, text):
    p = doc.add_paragraph()
    p.space_before = Pt(18); p.space_after = Pt(6)
    run = p.add_run(text.upper())
    run.font.size = Pt(16); run.font.bold = True; run.font.color.rgb = NAVY; run.font.name = 'Calibri'
    pPr = p._p.get_or_add_pPr()
    pBdr = parse_xml(f'<w:pBdr {nsdecls("w")}><w:bottom w:val="single" w:sz="8" w:space="4" w:color="1E293B"/></w:pBdr>')
    pPr.append(pBdr)

def add_h2(doc, number, text):
    p = doc.add_paragraph()
    p.space_before = Pt(14); p.space_after = Pt(4)
    run = p.add_run(f'{number}  {text.upper()}')
    run.font.size = Pt(13); run.font.bold = True; run.font.color.rgb = NAVY; run.font.name = 'Calibri'
    pPr = p._p.get_or_add_pPr()
    pBdr = parse_xml(f'<w:pBdr {nsdecls("w")}><w:bottom w:val="single" w:sz="4" w:space="2" w:color="334155"/></w:pBdr>')
    pPr.append(pBdr)

def add_body(doc, text):
    p = doc.add_paragraph()
    p.space_after = Pt(4)
    run = p.add_run(text)
    run.font.size = Pt(10); run.font.color.rgb = BLACK; run.font.name = 'Calibri'

def add_cover_info(doc, title, doc_ref, recipient, date_str):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER; p.space_before = Pt(60)
    run = p.add_run(title.upper()); run.font.size = Pt(20); run.font.bold = True; run.font.color.rgb = NAVY; run.font.name = 'Calibri'
    for label, val in [('Document Ref:', doc_ref), ('Submitted to:', recipient), ('Date:', date_str)]:
        p2 = doc.add_paragraph(); p2.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r2 = p2.add_run(f'{label}  {val}'); r2.font.size = Pt(10); r2.font.color.rgb = MED_GRAY; r2.font.name = 'Calibri'
    p5 = doc.add_paragraph(); p5.alignment = WD_ALIGN_PARAGRAPH.CENTER; p5.space_after = Pt(30)
    r5 = p5.add_run('Prepared by: [Subcontractor Name]'); r5.font.size = Pt(10); r5.font.color.rgb = DARK_GRAY; r5.font.name = 'Calibri'

## Page setup (A4)

```python
section = doc.sections[0]
section.page_width = Cm(21.0)
section.page_height = Cm(29.7)
section.top_margin = Cm(2.5)
section.bottom_margin = Cm(2.0)
section.left_margin = Cm(2.5)
section.right_margin = Cm(2.0)
```

## cairosvg on macOS

Always run with:
```bash
DYLD_FALLBACK_LIBRARY_PATH=/opt/homebrew/lib python3 gen_script.py
```
