# Formal SOW .docx Generation using SamayaDoc Template

## Setup

```python
import sys
# Add the template path
sys.path.insert(0, "/Users/mohamedessa/Library/CloudStorage/OneDrive-SAMAYAINVESTMENT/Samaya/Technical Office/_Style-Guides/Doc Style Guide")
from samaya_doc_template import SamayaDoc, SamayaColors
from docx.shared import Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH
```

## Basic usage

```python
doc = SamayaDoc()

# Header with doc info
doc.create_header(
    project_name="Aseer Regional Museum — [Topic]",
    doc_ref="MOC-ASEER-SIC-1K0-SC-XXXX",  # follow project numbering
    doc_type="SCOPE_REQUEST",               # or RPT, SPEC, etc.
    revision="A",
    date="Jun 2026"
)

# Footer with doc number
doc.create_footer("MOC-ASEER-SIC-1K0-SC-XXXX")

# Document title (H1 — 18pt Bold Navy uppercase)
doc.add_h1("SCOPE OF WORK REQUEST — ODDY TESTING LAB SERVICES")

# Section heading (H2 — 14pt Bold Navy uppercase)
doc.add_h2_u("1. PURPOSE OF THIS REQUEST")       # unnumbered
# or numbered:
doc.add_h2("1.0", "PURPOSE OF THIS REQUEST")

# Sub-section (H3 — 12pt Bold Dark Gray uppercase)
doc.add_h3("3.1", "MATERIAL CATEGORIES")

# Body text (11pt Calibri justified)
doc.add_body("Standard body paragraph text.")

# Mixed-format paragraph (bold segments within text)
doc.add_rich_body([
    {"text": "Critical path: ", "bold": True},
    {"text": "any sample submitted after ~01-Jul-2026 risks missing TOC."},
])

# Tables with navy header row + alternating shading
doc.add_table(
    ["#", "Category", "Source Sub", "Qty"],
    [
        ["1", "Showcase materials", "Sub 02", "~30–40"],
        ["2", "Joinery materials", "Sub 06", "~15–20"],
    ],
    col_widths_cm=[1.0, 5.0, 3.0, 2.0]  # total should fit A4 - margins = ~16cm
)

# Italic text (blockquote style)
doc.add_body("This is a privity note or blockquote.", italic=True, size=10)

# Small spacer
doc.line()

# Save
doc.save("output.docx")
```

## Document naming convention

Save alongside SCOPE_REQUEST.md:

```
Subcontractors/NN_Discipline_Contractor/MOC-MUS-ASE-XKH-SOW-XXX-00N_Scope.docx
```

Example: `Subcontractors/10_Oddy_Testing_Lab/MOC-ASEER-SIC-1K0-SC-0010_SCOPE_REQUEST.docx`

## Template style reference

| Element | Font | Size | Color | Notes |
|---------|------|------|-------|-------|
| H1 | Calibri Bold | 18pt | Navy `#1E293B` | Uppercase, bottom border 12pt |
| H2 | Calibri Bold | 14pt | Navy `#1E293B` | Uppercase, bottom border 6pt |
| H3 | Calibri Bold | 12pt | Dark Gray `#334155` | Uppercase, bottom border 4pt |
| Body | Calibri | 11pt | Black | Justified, 13pt line spacing |
| Table header | Calibri Bold | 9.5pt | White | Navy `#1E293B` background |
| Table cell | Calibri | 9.5pt | Black | Alternating row shading |
| Page margins | — | — | — | Top/Left 2.5cm, Bottom/Right 2.0cm |

## Converting from SCOPE_REQUEST.md

The typical pipeline:

1. Author `SCOPE_REQUEST.md` first (following Samaya 10-section template)
2. Write a Python generator that reads the .md, parses headings/tables/paragraphs, and calls `SamayaDoc` methods
3. Save to `.docx` in the same folder

Key parsing rules:
- `# Title` → `doc.add_h1()`
- `## Section` → `doc.add_h2_u()` or `doc.add_h2(number, text)`
- `### Subsection` → `doc.add_h3(number, text)`
- `| table |` → `doc.add_table(headers, rows)`
- `> quote` → `doc.add_body(text, italic=True, size=10)`
- `---` → `doc.line()`
- `**bold**` → split into segments for `doc.add_rich_body()`
- Regular text → `doc.add_body()`
