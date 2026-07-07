# Subcontractor Prequal Document Creation — Methodology & Programme

Trigger: User provides subcontractor company profile + certs and asks to create methodology/programme docs for prequal submission.

## Key Principles

1. **Subcontractor-branded, not Samaya-branded.** Documents use the sub's own logo/style, not SamayaDoc template. The doc is submitted *from* the sub *to* Samaya.
2. **iAcoustics/existing reports as internal reference only.** Never cite them as authoritative sources in the sub's own docs. Use data from them but present as the sub's own analysis.
3. **Programme by days (D0-D250), not calendar dates.** D0 = appointment date. All phases expressed as day ranges.
4. **DMP gates for phase mapping.** Use G-1 Design Dev, G-2 Material Approval, G-3 IFC, G-4 Construction, G-5 Handover.
5. **RACI matrix required.** Show who does what: SDE=R, NRS=A (design), Samaya=A (IFC/commissioning), CG=A (final).

## Standalone DOCX Pattern (No SamayaDoc)

```python
from docx import Document
from docx.shared import Cm, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml.ns import qn, nsdecls
from docx.oxml import parse_xml

# Define brand colors
PRIMARY = RGBColor(0x0D, 0x57, 0xA5)  # Pan Acoustics blue
DARK = RGBColor(0x07, 0x3B, 0x6E)
ACCENT = RGBColor(0x0A, 0x7D, 0xE6)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)
BLACK = RGBColor(0x00, 0x00, 0x00)
```

## SVG Charts via cairosvg

Render inline SVG as PNG and embed in DOCX:

```python
import cairosvg
def add_svg_flowchart(doc, svg_content, caption="", width_cm=16.5):
    png_path = "/tmp/chart_temp.png"
    cairosvg.svg2png(bytestring=svg_content.encode('utf-8'), write_to=png_path,
                     output_width=1600, output_height=500)
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run()
    run.add_picture(png_path, width=Cm(width_cm))
    os.unlink(png_path)

# Run with: DYLD_FALLBACK_LIBRARY_PATH=/opt/homebrew/lib python3 script.py
```

## Programme Timeline Gantt (Days-Based SVG)

Axis markers at D0, D30, D50, D65, D80, D95, D110, D150, D220, D250. Each bar is a `<rect>` with its x-position proportional to day. No calendar dates on axis — just D-prefixed day numbers.

## Styled Table Helper

```python
def set_cell_shading(cell, color_hex):
    tc = cell._tc
    tcPr = tc.get_or_add_tcPr()
    shading = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{color_hex}"/>')
    tcPr.append(shading)

def add_styled_table(doc, headers, rows, col_widths_cm=None):
    table = doc.add_table(rows=1 + len(rows), cols=len(headers))
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    for i, h in enumerate(headers):
        cell = table.rows[0].cells[i]; cell.text = h
        for p in cell.paragraphs:
            for run in p.runs:
                run.font.size = Pt(9); run.font.bold = True
                run.font.color.rgb = WHITE; run.font.name = 'Calibri'
        set_cell_shading(cell, '0D57A5')
    for ri, row_data in enumerate(rows):
        for ci, val in enumerate(row_data):
            cell = table.rows[ri + 1].cells[ci]; cell.text = str(val)
            for p in cell.paragraphs:
                for run in p.runs:
                    run.font.size = Pt(9); run.font.color.rgb = BLACK
                    run.font.name = 'Calibri'
            if ri % 2 == 1:
                set_cell_shading(cell, 'E8F0FA')
    # Set column widths
    if col_widths_cm:
        for row in table.rows:
            for ci, w in enumerate(col_widths_cm):
                row.cells[ci].width = Cm(w)
    return table
```

## Common Pitfalls

- **Baseline Noise Survey:** Don't include if building shell exists but fit-out isn't built — no useful data to collect. Remove and renumber sections.
- **iAcoustics references:** User explicitly said not to cite the report. Use CadnaR (not EASE) if that's what the reference uses, but present as the sub's own tool choice.
- **BIM coordination:** Never assign BIM coordination to the sub — that's Samaya's role. Sub provides layout drawings and input specs only.
- **Oddy test:** Only applies to materials in showcases/display areas near exhibits, not general acoustic treatments.
- **Word shapes (VML):** Unreliable via python-docx XML manipulation. Prefer SVG rendered to PNG via cairosvg, or simple text-based flow descriptions.
- **DOCX vs regenerate:** When the user has made manual edits, edit the existing DOCX directly (not regenerate from script). Close Word first, edit, then reopen.
- **AI fingerprints:** After generation, scan for: smart quotes, em-dashes, arrow symbols (→), section symbols (§), bullet characters (• → use -), and AI-sounding phrases like "this document outlines" or "SDE applies a three-phase protocol". Replace with human equivalents.
- **Section numbering:** When removing a section, renumber ALL subsequent sections and their sub-sections. The RACI matrix typically goes as §3.0, pushing commissioning to §4.0, quality to §5.0, team to §6.0.
- **Subsection renumbering:** When you remove a subsection (e.g. §1.1 Baseline Noise Survey), renumber ALL following subsections in that parent (1.2→1.1, 1.3→1.2, 1.4→1.3). Check SVG chart references and any inline cross-references that mention the old numbers. SVG charts often contain hardcoded labels like "AC-001, AC-002, AC-003" that reference removed deliverables — update those too.
- **Cross-doc deliverable consistency:** If you remove a deliverable (e.g. AC-002 existing survey) from the Methodology doc sections, also remove it from the Programme doc's deliverable schedule table and the Gantt chart. Every deliverable mentioned in one doc must appear in the other, and vice versa. Renumber remaining deliverables so refs are sequential with no gaps.
