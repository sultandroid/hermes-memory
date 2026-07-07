# Standalone SOW DOCX — Python-docx Pattern (No SamayaDoc Template)

When generating a Scope of Services / SOW DOCX for an **in-house team member** (not a subcontractor or external consultant), the SamayaDoc template may not be appropriate. Use raw python-docx with the CV-pack color scheme instead.

## When to use this pattern

- Creating a SOW for an approved Key Personnel member (e.g., Sustainability Manager)
- The document follows the CV submittal pack visual style (dark green #0F766E headers) rather than the formal SamayaDoc navy style
- The SamayaDoc template path is inaccessible due to OneDrive TCC blocking
- Delivering to internal stakeholders who expect the CV-pack branding

## Color Scheme

| Element | Color | Hex |
|---------|-------|-----|
| Headers | Dark Green (CV-pack) | `#0F766E` |
| Body text | Dark Gray | `#333333` |
| Muted text | Medium Gray | `#666666` |
| Table header bg | Dark Green | `#0F766E` |
| Table header text | White | `#FFFFFF` |
| Horizontal rule | Dark Green | `#0F766E` |

Note: The SamayaDoc formal template uses Navy `#1E293B` for headers. Use CV-pack green for documents related to Key Personnel submittals, and SamayaDoc navy for formal contract/procurement documents.

## Structure Pattern

```
Cover → Project Info Table → [Page Break]
1. Role Summary
2. Scope of Responsibilities (2.1..2.8 subsections)
3. Deliverables Schedule (table: # / Deliverable / Phase / Frequency)
4. Coordination Matrix (table: Deliverable / Coordinates With / Frequency)
5. Reporting Line & Governance
6. Scope Exclusions
7. Acceptance (signature block table)
```

## python-docx Setup

```python
from docx import Document
from docx.shared import Pt, Inches, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml.ns import qn, nsdecls
from docx.oxml import parse_xml

doc = Document()

# Page setup
for section in doc.sections:
    section.page_width = Cm(21.0)
    section.page_height = Cm(29.7)
    section.top_margin = Cm(2.0)
    section.bottom_margin = Cm(1.5)
    section.left_margin = Cm(2.0)
    section.right_margin = Cm(2.0)

style = doc.styles['Normal']
font = style.font
font.name = 'Calibri'
font.size = Pt(11)
font.color.rgb = RGBColor(0x33, 0x33, 0x33)
```

## Helper Functions

```python
def add_green_header(text, size=16):
    p = doc.add_paragraph()
    run = p.add_run(text)
    run.font.size = Pt(size)
    run.font.bold = True
    run.font.color.rgb = RGBColor(0x0F, 0x76, 0x6E)
    run.font.name = 'Calibri'
    return p

def add_body(text, bold=False):
    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(4)
    run = p.add_run(text)
    run.font.size = Pt(11)
    run.font.bold = bold
    run.font.name = 'Calibri'
    run.font.color.rgb = RGBColor(0x33, 0x33, 0x33)
    return p

def add_bullet(text, bold_prefix=''):
    p = doc.add_paragraph(style='List Bullet')
    p.paragraph_format.space_after = Pt(2)
    if bold_prefix:
        run = p.add_run(bold_prefix)
        run.font.bold = True
        run = p.add_run(text)
    else:
        run = p.add_run(text)
    run.font.size = Pt(11)
    run.font.name = 'Calibri'
    return p

def set_cell_shading(cell, color):
    shading = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{color}"/>')
    cell._tc.get_or_add_tcPr().append(shading)

def add_table_row(table, cells_data, header=False):
    row = table.add_row()
    for i, text in enumerate(cells_data):
        cell = row.cells[i]
        cell.text = ''
        p = cell.paragraphs[0]
        run = p.add_run(str(text))
        run.font.size = Pt(10)
        run.font.name = 'Calibri'
        if header:
            run.font.bold = True
            run.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
            set_cell_shading(cell, '0F766E')
        else:
            run.font.color.rgb = RGBColor(0x33, 0x33, 0x33)
```

## Dark Green Line Separator

```python
def add_dark_green_line():
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(2)
    p.paragraph_format.space_after = Pt(6)
    run = p.add_run('_' * 80)
    run.font.color.rgb = RGBColor(0x0F, 0x76, 0x6E)
    run.font.size = Pt(8)
```

## Tables Without col_widths_cm

Same rule as SamayaDoc: NEVER pass `col_widths_cm` to `add_table()` — python-docx stores EMU as 'dxa', producing 4000-inch columns. Create the table without widths, set column widths via `row.cells[i].width = Cm(N)` after creation.

Example:
```python
table = doc.add_table(rows=0, cols=4)
table.style = 'Table Grid'
# Header
hdr = table.add_row()
for i, text in enumerate(['#', 'Deliverable', 'Phase', 'Frequency']):
    # ... format cell
# Set widths
for row in table.rows:
    row.cells[0].width = Cm(0.8)
    row.cells[1].width = Cm(6.5)
    row.cells[2].width = Cm(2.5)
    row.cells[3].width = Cm(3.0)
```

## Full Example

See the Muhammad Fida Noor SOW created in the June 2026 session at:
`04_Consultants/05_Muhammad_Fida_Noor/Muhammad_Fida_Noor_Scope_of_Services.docx`

The gen script pattern: write to `/tmp/<filename>.docx`, then use AppleScript `duplicate` to copy into OneDrive.
