# Retrofitting Samaya Branding onto Existing DOCX

**When to use:** You have an existing `.docx` file that was NOT created with `SamayaDoc` (e.g., a draft from another source, an earlier revision with raw python-docx styles, or a consultant deliverable) and need to apply Samaya-branded formatting — header, footer, margins, heading styles, table styles, symbol cleanup — without regenerating the document from scratch.

**Key difference from `docx-editing-techniques.md`:** That reference covers *text edits* (find-and-replace, revision bump, row removal). This reference covers *formatting retrofit* — applying SamayaDoc visual styles to an existing document's elements.

## Prerequisites

```python
import sys, os
_template_dir = "/Users/mohamedessa/Library/CloudStorage/OneDrive-SAMAYAINVESTMENT/Samaya/Technical Office/_Style-Guides/Doc Style Guide"
if not os.path.exists(_template_dir):
    _template_dir = "/Users/mohamedessa/Library/Group Containers/UBF8T346G9.OneDriveStandaloneSuite/OneDrive - SAMAYA INVESTMENT.noindex/OneDrive - SAMAYA INVESTMENT/Samaya/Technical Office/_Style-Guides/Doc Style Guide"
sys.path.insert(0, _template_dir)

from samaya_doc_template import SamayaColors, _set_font, format_header_cell, format_data_cell, set_cell_shading, _add_bottom_border, _add_top_border, _add_field, _set_tab_stops
from docx import Document
from docx.shared import Pt, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_LINE_SPACING
from docx.enum.table import WD_TABLE_ALIGNMENT
```

## Step 1: Close Word first

```bash
osascript -e 'tell application "Microsoft Word" to close every document saving yes'
```

## Step 2: Set page margins

```python
section = doc.sections[0]
section.page_width = Cm(21.0)
section.page_height = Cm(29.7)
section.top_margin = Cm(2.5)
section.bottom_margin = Cm(2.0)
section.left_margin = Cm(2.5)
section.right_margin = Cm(2.0)
section.header_distance = Cm(1.5)
section.footer_distance = Cm(1.2)
```

## Step 3: Create Samaya header

Clear existing header, add logo (left), project name + doc ref (center), revision + date (right), with tab stops and bottom border:

```python
header = section.header
header.is_linked_to_previous = False
for p in header.paragraphs:
    p.clear()

p = header.paragraphs[0]
p.paragraph_format.space_before = Pt(0)
p.paragraph_format.space_after = Pt(2)

# Logo
logo_path = "/path/to/samaya-logo-trans.png"
if os.path.exists(logo_path):
    run = p.add_run()
    run.add_picture(logo_path, width=Cm(2.5))
    run2 = p.add_run('\t')
    _set_font(run2, size=7.5)
else:
    run = p.add_run('[SAMAYA]  \t')
    _set_font(run, size=7.5, bold=True, color=SamayaColors.NAVY)

# Center
run = p.add_run('Project Name\n')
_set_font(run, size=7.5, color=SamayaColors.DARK_GRAY)
run = p.add_run('Doc Ref: REF-001  |  TYPE')
_set_font(run, size=7.5, color=SamayaColors.MEDIUM_GRAY)

# Right
run = p.add_run('\t')
_set_font(run, size=7.5)
run = p.add_run('Rev: C03\n')
_set_font(run, size=7.5, bold=True, color=SamayaColors.NAVY)
run = p.add_run('2026-06-16')
_set_font(run, size=7.5, color=SamayaColors.MEDIUM_GRAY)

_set_tab_stops(p)
_add_bottom_border(p, color='CBD5E1', size=4)
```

## Step 4: Create Samaya footer

```python
footer = section.footer
footer.is_linked_to_previous = False
for p in footer.paragraphs:
    p.clear()

p = footer.paragraphs[0]
p.paragraph_format.space_before = Pt(2)
p.paragraph_format.space_after = Pt(0)
_add_top_border(p, color='1E293B', size=8)

run = p.add_run('DOC-REF')
_set_font(run, size=8, color=SamayaColors.MEDIUM_GRAY)
run = p.add_run('\t')
_set_font(run, size=8, color=SamayaColors.MEDIUM_GRAY)
run = p.add_run('Page ')
_set_font(run, size=8, color=SamayaColors.MEDIUM_GRAY)
_add_field(p, 'PAGE')
run = p.add_run(' of ')
_set_font(run, size=8, color=SamayaColors.MEDIUM_GRAY)
_add_field(p, 'NUMPAGES')
run = p.add_run('\t')
_set_font(run, size=8)
run = p.add_run('Samaya Investment Company')
_set_font(run, size=8, color=SamayaColors.MEDIUM_GRAY)
_set_tab_stops(p)

# Confidentiality notice
p2 = footer.add_paragraph()
p2.paragraph_format.space_before = Pt(0)
p2.paragraph_format.space_after = Pt(0)
run = p2.add_run(
    'This document is the property of Samaya Investment Company. '
    'Unauthorised reproduction or distribution is prohibited.'
)
_set_font(run, size=7, italic=True, color=SamayaColors.MEDIUM_GRAY)
p2.alignment = WD_ALIGN_PARAGRAPH.CENTER
```

## Step 5: Classify and format paragraphs

Use text pattern matching to detect heading levels, then apply SamayaDoc styles:

```python
import re

for para in doc.paragraphs:
    text = para.text.strip()
    if not text:
        continue

    # H1: Document title (all caps, short, at start)
    if len(text) < 50 and text.isupper() and len(text.split()) <= 6:
        for run in para.runs:
            _set_font(run, size=18, bold=True, color=SamayaColors.NAVY)
        para.alignment = WD_ALIGN_PARAGRAPH.LEFT
        pf = para.paragraph_format
        pf.space_before = Pt(18)
        pf.space_after = Pt(12)
        pf.line_spacing = Pt(24)
        pf.line_spacing_rule = WD_LINE_SPACING.EXACTLY
        pf.keep_with_next = True
        _add_bottom_border(para, color='1E293B', size=12)
        continue

    # Section banners: "ADMINISTRATIVE GOVERNANCE | 01. DOCUMENT CONTROL & AUTHORITY"
    if '|' in text and any(kw in text.upper() for kw in ['GOVERNANCE', 'ORGANIZATION', 'DEPLOYMENT', 'CLOSE-OUT', 'PROCESS', 'RESOURCE BREAKDOWN', 'RESOURCE LOADING', 'PHYSICAL', 'TEAM', 'STRATEGIC']):
        for run in para.runs:
            _set_font(run, size=14, bold=True, color=SamayaColors.NAVY)
        para.alignment = WD_ALIGN_PARAGRAPH.LEFT
        pf = para.paragraph_format
        pf.space_before = Pt(18)
        pf.space_after = Pt(6)
        pf.line_spacing = Pt(18)
        pf.line_spacing_rule = WD_LINE_SPACING.EXACTLY
        pf.keep_with_next = True
        _add_bottom_border(para, color='CBD5E1', size=6)
        continue

    # H2: "1. Document Control & Authority"
    h2_match = re.match(r'^(\d+\.?\d*)\s+([A-Z].+)', text)
    if h2_match and len(text) < 100:
        for run in para.runs:
            _set_font(run, size=14, bold=True, color=SamayaColors.NAVY)
        para.alignment = WD_ALIGN_PARAGRAPH.LEFT
        pf = para.paragraph_format
        pf.space_before = Pt(18)
        pf.space_after = Pt(6)
        pf.line_spacing = Pt(18)
        pf.line_spacing_rule = WD_LINE_SPACING.EXACTLY
        pf.keep_with_next = True
        _add_bottom_border(para, color='CBD5E1', size=6)
        continue

    # H3: "1.1 Revision History Log"
    h3_match = re.match(r'^(\d+\.\d+)\s+([A-Z].+)', text)
    if h3_match and len(text) < 100:
        for run in para.runs:
            _set_font(run, size=12, bold=True, color=SamayaColors.DARK_GRAY)
        para.alignment = WD_ALIGN_PARAGRAPH.LEFT
        pf = para.paragraph_format
        pf.space_before = Pt(12)
        pf.space_after = Pt(4)
        pf.line_spacing = Pt(16)
        pf.line_spacing_rule = WD_LINE_SPACING.EXACTLY
        pf.keep_with_next = True
        _add_bottom_border(para, color='CBD5E1', size=4)
        continue

    # Body text — default
    for run in para.runs:
        if not run.font.size or run.font.size.pt > 12:
            _set_font(run, size=11, color=SamayaColors.BLACK)
    para.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    pf = para.paragraph_format
    pf.space_before = Pt(0)
    pf.space_after = Pt(6)
    pf.line_spacing = Pt(13)
    pf.line_spacing_rule = WD_LINE_SPACING.EXACTLY
```

## Step 6: Format all tables

```python
for table in doc.tables:
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit = False

    # Even column widths
    if len(table.columns) > 0:
        col_w = 16.5 / len(table.columns)
        for row in table.rows:
            for i, cell in enumerate(row.cells):
                cell.width = Cm(col_w)

    # Header row
    for i, cell in enumerate(table.rows[0].cells):
        format_header_cell(cell, cell.text.strip())

    # Data rows
    for r_idx, row in enumerate(table.rows):
        if r_idx == 0:
            continue
        bg = 'F1F5F9' if r_idx % 2 == 0 else 'FFFFFF'
        for c_idx, cell in enumerate(row.cells):
            align = WD_ALIGN_PARAGRAPH.CENTER if c_idx == 0 else WD_ALIGN_PARAGRAPH.LEFT
            format_data_cell(cell, cell.text.strip(), align=align)
            set_cell_shading(cell, bg)
```

## Step 7: Symbol cleanup

Remove decorative symbols and accented characters that the Samaya style guide forbids:

```python
SYMBOL_MAP = {
    '\u00a7': 'Sec ',       # section sign
    '\u2014': '-',          # em dash
    '\u2013': '-',          # en dash
    '\u2018': "'",          # left single quote
    '\u2019': "'",          # right single quote
    '\u201c': '"',          # left double quote
    '\u201d': '"',          # right double quote
    '\u2022': '-',          # bullet
    '\u00b7': '-',          # middle dot
    '\u2192': '->',         # right arrow
    '\u00d7': 'x',          # multiplication sign
    '\u00b0': ' deg ',      # degree
    '\u2026': '...',        # ellipsis
    '\u00e9': 'e',          # e-acute
    '\u00e8': 'e',          # e-grave
    '\u00ea': 'e',          # e-circumflex
    '\u00eb': 'e',          # e-diaeresis
    '\u00e0': 'a',          # a-grave
    '\u00e2': 'a',          # a-circumflex
    '\u00e4': 'a',          # a-diaeresis
    '\u00f9': 'u',          # u-grave
    '\u00fb': 'u',          # u-circumflex
    '\u00f6': 'o',          # o-diaeresis
    '\u00f4': 'o',          # o-circumflex
    '\u00ee': 'i',          # i-circumflex
    '\u00ef': 'i',          # i-diaeresis
    '\u00e7': 'c',          # c-cedilla
}

def clean_text(text):
    for old, new in SYMBOL_MAP.items():
        text = text.replace(old, new)
    return text

for para in doc.paragraphs:
    for run in para.runs:
        if run.text:
            run.text = clean_text(run.text)
```

## Step 8: Save and reopen

```python
doc.save(path)
# Then reopen in Word
import subprocess
subprocess.run(['open', path])
```

## Pitfalls

- **Close Word first** — python-docx will corrupt the file if Word holds a lock. Always run the osascript close command before editing.
- **Heading detection is heuristic** — the regex patterns (`^\d+\.?\d*\s+[A-Z]`) work for numbered headings. For unnumbered headings, add explicit text matching.
- **Table column widths** — even distribution (16.5 / N) works for most tables. For tables with specific width requirements, use `col_widths_cm` logic instead.
- **Symbol cleanup runs on ALL text** — including code blocks, URLs, and technical references. Verify no unintended replacements (e.g., `->` replacing `→` in arrow notation).
- **Run-level formatting preserved** — `_set_font()` on each run keeps existing bold/italic. The heading classification only changes font size/color/alignment, not the run's bold state.
- **Section banners with `|`** — the pipe-delimited section headers (e.g., "ADMINISTRATIVE GOVERNANCE | 01. ...") are specific to this document's structure. For other documents, adjust the keyword list or pattern.
