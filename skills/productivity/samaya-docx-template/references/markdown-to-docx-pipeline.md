# Markdown-to-DOCX Pipeline — Full-Feature Pattern

When the source document is a **markdown file** (project plan, register, report) and the deliverable is a **professional DOCX** with cover page, styled tables, colour-coded matrices, header/footer, and page numbers — use this pattern.

## When to use

- Source is a `.md` file with tables, headings, code blocks, blockquotes, lists, and separators
- The document needs a **cover page** with document metadata (ref, revision, date, status, contract info)
- Tables need **navy headers** (#1E293B), alternating row shading (#F1F5F9), and keep-with-next
- A **Probability × Severity matrix** (or similar colour-coded grid) is needed
- Header/footer with **Page X of Y** fields are required
- The document is **not** using the SamayaDoc class (e.g., for standalone deliverables, subcontractor documents, or when the template path is unavailable)

## Architecture

The pipeline has three layers:

1. **Markdown parser** — walks lines, classifies each as heading/table/list/code/blockquote/separator/paragraph
2. **DOCX builder** — renders each classified element using raw python-docx with professional styling
3. **Post-processor** — applies header/footer, page breaks, and colour-coded matrix

## Key functions

### `parse_markdown_table_lines(lines, start_idx)`
Parses a markdown table starting at `start_idx`. Returns `(headers, rows, end_idx)`. Handles separator lines and empty lines between tables.

### `make_table(doc, headers, rows, col_widths=None)`
Creates a styled table with navy header, white bold text, alternating row shading, and keep-with-next on all rows.

### `make_pi_matrix(doc)`
Creates a 4×4 Probability × Severity matrix with colour-coded cells:
- Score ≥ 12: red (#B91C1C) — Critical
- Score 8–11: orange (#F97316) — High
- Score 4–7: yellow (#EAB308) — Medium
- Score ≤ 3: green (#22C55E) — Low
- Row labels: navy (#1E293B) with white text

### `add_header_footer(doc)`
Adds header with document reference and footer with Page X of Y fields (using Word field codes PAGE and NUMPAGES).

### `add_cover_page(doc)`
Creates a cover page with:
- 6 blank lines for top spacing
- Title (28pt bold navy)
- Subtitle (16pt medium gray)
- Separator line
- Document details table (label: value pairs, centered)

## Markdown constructs handled

| Construct | Rendering |
|-----------|-----------|
| `## Heading` (h1) | 14pt bold navy, page break before, Calibri |
| `### Heading` (h2) | 12pt bold dark gray, page break before, Calibri |
| `#### Heading` (h3) | 11pt bold medium gray, Calibri |
| `---` separator | Thin gray horizontal rule |
| Tables (`\|...\|`) | Styled table with navy header, alternating rows |
| Blockquotes (`> text`) | Left-indented, 10pt italic, medium gray |
| Code blocks (```` ``` ````) | 9pt Consolas, left-indented |
| Bullet lists (`- item`) | List Bullet style |
| Numbered lists (`1. item`) | List Number style |
| Regular paragraphs | 11pt Calibri, inline bold preserved |
| P-I Matrix (special table) | Colour-coded 4×4 grid |

## Cover page metadata pattern

```python
details = [
    ("Document Reference:", "MOC-MUS-ASE-1KH-PL-02.17"),
    ("Revision:", "C01"),
    ("Date:", "2026-07-12"),
    ("Status:", "For Submission"),
    ("Contract:", "0010003521 — Design & Build (SAR 65,153,751.16)"),
    ("Employer:", "Ministry of Culture (MoC) — Museums Commission"),
    ("PMC:", "ACE Moharram-Bakhoum"),
    ("Design Lead:", "NRS (Nissen Richards Studio, Job A2742)"),
    ("Handover Date:", "30 September 2026"),
    ("Originator:", "Samaya Technical Office"),
]
```

## Page setup

```python
section = doc.sections[0]
section.page_width = Cm(21.0)
section.page_height = Cm(29.7)
section.top_margin = Cm(2.0)
section.bottom_margin = Cm(2.0)
section.left_margin = Cm(2.0)
section.right_margin = Cm(2.0)
```

## Pitfalls

- **P-I Matrix detection**: The matrix table is identified by checking if the header line contains both `"P×S"` and `"Sev"`. If the markdown uses different column headers, adjust the detection logic.
- **HSE 5×5 scoring table**: Detected by checking if `"Score Range"` and `"Severity"` appear in the header AND `"≥ 16"` appears in the next few rows. This prevents the HSE table from being rendered as a regular table.
- **Page X of Y fields**: Must use Word XML field codes (`PAGE` and `NUMPAGES`), not plain text. The `fldChar` begin/separate/end sequence is required for each field.
- **Table column widths**: Set via `set_cell_width(cell, width_cm)` which uses `w:tcW` with `w:type="dxa"`. Sum of widths should be ~16.5cm for A4 with 2cm margins.
- **Keep-with-next on table rows**: Prevents rows from splitting across pages. Applied via `set_row_keep_with_next(row)` which adds `<w:cantSplit/>` to the row properties.
- **Cover page page break**: Use `doc.add_page_break()` after the cover page, not a manual page break paragraph. The first content section starts on page 2.
- **Inline bold in paragraphs**: Use regex `re.split(r'(\*\*.+?\*\*)', text)` to split on bold markers, then render each segment with appropriate bold flag.
- **Markdown link removal**: Strip `[text](url)` patterns from heading text with `re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', text)`.
- **Empty lines between tables**: The parser skips empty lines before table detection. If a table is preceded by a heading, the heading is rendered first, then the table.
- **Code block indentation**: Use `p.paragraph_format.left_indent = Cm(0.5)` for code blocks to visually distinguish them from body text.
- **Blockquote styling**: Use italic + medium gray color + left indent to visually distinguish quotes from body text.
- **Separator rendering**: Use a thin gray horizontal rule (repeated `─` characters at 8pt) rather than a full-width line, which python-docx cannot render natively.

## Full script structure

```python
#!/usr/bin/env python3
from docx import Document
from docx.shared import Pt, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml.ns import qn, nsdecls
from docx.oxml import parse_xml

# Constants
NAVY = RGBColor(0x1E, 0x29, 0x3B)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)
DARK_TEXT = RGBColor(0x1A, 0x1A, 0x1A)

# Helper functions (set_cell_shading, set_cell_width, set_row_keep_with_next,
# add_formatted_paragraph, add_rich_paragraph, style_table_header,
# style_table_body, make_table, make_pi_matrix, add_header_footer,
# add_cover_page, parse_markdown_table_lines)

def build_docx():
    doc = Document()
    # Page setup
    # Cover page
    # Read markdown
    # Parse and render line by line
    # Add header/footer
    doc.save(OUT_PATH)

if __name__ == "__main__":
    build_docx()
```

## Verification checklist

- [ ] Cover page renders correctly (title, subtitle, metadata)
- [ ] Page 2 starts with first content section
- [ ] All tables have navy headers with white bold text
- [ ] Alternating row shading visible on body rows
- [ ] P-I Matrix has correct colour coding (red/orange/yellow/green)
- [ ] Header shows document reference on every page
- [ ] Footer shows "Page X of Y" correctly
- [ ] Code blocks render in monospace font
- [ ] Blockquotes are italic and indented
- [ ] Bullet and numbered lists are properly formatted
- [ ] Page breaks occur before each major section
- [ ] No orphaned table rows across page breaks
- [ ] File opens in Word without errors
