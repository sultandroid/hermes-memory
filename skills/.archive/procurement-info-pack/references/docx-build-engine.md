# Samaya DOCX Build Engine — Helper Functions

Compact function reference for building purchasing info packs. These are the functions used in the Aseer Museum purchasing packs.

```python
import os
from docx import Document
from docx.shared import Pt, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_LINE_SPACING
from docx.enum.table import WD_TABLE_ALIGNATION
from docx.oxml.ns import qn, nsdecls
from docx.oxml import parse_xml, OxmlElement
```

## Colors

```python
class C:
    NAVY = RGBColor(0x1E, 0x29, 0x3B)
    RED = RGBColor(0xB0, 0x1E, 0x2F)
    WHITE = RGBColor(0xFF, 0xFF, 0xFF)
    GUN = RGBColor(0x33, 0x41, 0x55)      # dark gray
    GRAY = RGBColor(0x64, 0x74, 0x8B)     # medium gray
    LGRAY = RGBColor(0xF1, 0xF5, 0xF9)    # light gray
    BGRAY = RGBColor(0xCB, 0xD5, 0xE1)    # border gray
    MUTED = RGBColor(0xF8, 0xFA, 0xFC)    # muted bg
    BLACK = RGBColor(0x00, 0x00, 0x00)
```

## Low-level Helpers

```python
def shd(cell, hx):    # cell shading with hex color
def mar(cell, t=28, b=28, l=56, r=56):  # cell margins in dxa
def bdr(cell, c='CBD5E1', s=4):  # cell borders
def pbot(p, c='1E293B', s=8):    # bottom border on paragraph
def ptop(p, c='1E293B', s=8):    # top border on paragraph
def field(p, code):               # Word field code (PAGE, NUMPAGES)
def rtl(p):                       # set RTL on paragraph
def rtl_cell(cell):               # set RTL on all cell paragraphs
```

XML construction pattern:
```python
cell._tc.get_or_add_tcPr().append(
    parse_xml(f'<w:shd {nsdecls("w")} w:fill="{hx}" w:val="clear"/>'))
```

## Page Setup

```python
def setup(doc):
    s = doc.sections[0]
    s.page_width = Cm(21); s.page_height = Cm(29.7)   # A4
    s.top_margin = Cm(2.5); s.bottom_margin = Cm(2)
    s.left_margin = Cm(2.5); s.right_margin = Cm(2)
    s.header_distance = Cm(1.5); s.footer_distance = Cm(1.2)
```

## Header & Footer

```python
def header(doc, proj, ref, dt):
    # One-line: "Project Name  |  Doc Ref  |  Date"
    # 7.5pt Calibri, bottom border
def footer(doc, ref):
    # "DocRef    Page X of Y    Samaya Investment Company"
    # 8pt Calibri, top border, PAGE/NUMPAGES fields
```

## Content Elements

```python
def title(doc, t):         # 16pt Bold Navy, bottom border
def subtitle(doc, t):      # 10pt Gray
def h2(doc, t):            # 12pt Bold Navy uppercase, bottom border
def h3(doc, t):            # 10pt Bold Dark Gray
def body(doc, t, sz=10):   # Left-aligned, 12pt line spacing exact
def body_ar(doc, t, sz=10): # Right-aligned RTL
def bilingual(doc, en, ar): # body() + body_ar() pair
```

## Tables

```python
def tbl(doc, hdrs, data, widths=None):
    # widths = list of column widths in cm
    # Auto-calculates equal widths if None
```

## Special Elements

```python
def note(doc, t, lbl='NOTE'):   # Red left border, muted bg
def bullet(doc, t):              # Dash prefix, 9pt
def actions(doc, items):         # Checklist with empty checkboxes
```

## Complete Minimal Example

```python
doc = Document()
setup(doc)
header(doc, 'Aseer Regional Museum', 'PUR-XXX-001', '06 June 2026')
footer(doc, 'PUR-XXX-001')

title(doc, 'Materials — Purchasing Information')
subtitle(doc, 'For Purchasing Department  |  Rev A')

h2(doc, '1. Summary')
tbl(doc, ['Item', 'Detail'], [['Brand specified?', 'No — performance spec']], [3, 13.5])

note(doc, 'Verify quantities against latest schedule before ordering.', 'NOTE')

h2(doc, '2. Actions')
actions(doc, ['Source material from local suppliers', 'Submit samples for NRS approval'])

doc.save('output.docx')
```
