# DOCX Merged Cell Extraction & Table Rebuild

**When to use:** An existing DOCX has tables with merged cells (gridSpan) that need to be restructured — removing duplicate columns, fixing column count, or rebuilding with clean data.

## The problem

python-docx's `cell.text` returns merged text from gridSpan cells, but you can't distinguish which part came from which logical column. The XML `w:tc` elements reveal the real structure.

## Extract text from merged cells via XML

```python
from docx.oxml.ns import qn

def get_tc_text(tc_elem):
    """Get all text from a w:tc element, handling merged cells."""
    texts = []
    for t_elem in tc_elem.findall('.//' + qn('w:t')):
        if t_elem.text:
            texts.append(t_elem.text)
    return ' '.join(texts).strip()

for ri, row in enumerate(table.rows):
    tr = row._tr
    tc_elements = list(tr.findall(qn('w:tc')))
    for tci, tc in enumerate(tc_elements):
        text = get_tc_text(tc)
        # Check for gridSpan
        tcPr = tc.find(qn('w:tcPr'))
        if tcPr is not None:
            gs = tcPr.find(qn('w:gridSpan'))
            if gs is not None:
                span = int(gs.get(qn('w:val')))
                print(f"  tc[{tci}] gridSpan={span} text='{text[:40]}'")
```

## Rebuild a table from scratch (when column structure is broken)

When merged cells make column removal impossible, rebuild the table entirely:

```python
from docx.oxml import OxmlElement

tbl = table._tbl

# 1. Remove all existing rows
for row in list(tbl.findall(qn('w:tr'))):
    tbl.remove(row)

# 2. Fix grid to correct column count
tblGrid = tbl.find(qn('w:tblGrid'))
if tblGrid is not None:
    for gc in list(tblGrid.findall(qn('w:gridCol'))):
        tblGrid.remove(gc)
    for w in ['1400', '3000', '2000', '1000']:  # widths in dxa
        gc = OxmlElement('w:gridCol')
        gc.set(qn('w:w'), w)
        tblGrid.append(gc)

# 3. Helper to create a cell
def make_cell(text, is_header=False, row_idx=0):
    tc = OxmlElement('w:tc')
    tcPr = OxmlElement('w:tcPr')
    tc.append(tcPr)
    
    tcW = OxmlElement('w:tcW')
    tcW.set(qn('w:w'), '1875')
    tcW.set(qn('w:type'), 'dxa')
    tcPr.append(tcW)
    
    # Shading
    shd = OxmlElement('w:shd')
    shd.set(qn('w:val'), 'clear')
    shd.set(qn('w:color'), 'auto')
    shd.set(qn('w:fill'), '1E293B' if is_header else ('FFFFFF' if row_idx % 2 == 1 else 'F1F5F9'))
    tcPr.append(shd)
    
    # Cell margins
    tcMar = OxmlElement('w:tcMar')
    for edge in ['top', 'bottom']:
        el = OxmlElement(f'w:{edge}')
        el.set(qn('w:w'), '28'); el.set(qn('w:type'), 'dxa')
        tcMar.append(el)
    for edge in ['left', 'right']:
        el = OxmlElement(f'w:{edge}')
        el.set(qn('w:w'), '56'); el.set(qn('w:type'), 'dxa')
        tcMar.append(el)
    tcPr.append(tcMar)
    
    # Paragraph with text
    p = OxmlElement('w:p')
    pPr = OxmlElement('w:pPr')
    p.append(pPr)
    spacing = OxmlElement('w:spacing')
    spacing.set(qn('w:before'), '20'); spacing.set(qn('w:after'), '20')
    spacing.set(qn('w:line'), '240'); spacing.set(qn('w:lineRule'), 'auto')
    pPr.append(spacing)
    
    r = OxmlElement('w:r')
    rPr = OxmlElement('w:rPr')
    r.append(rPr)
    rFonts = OxmlElement('w:rFonts')
    rFonts.set(qn('w:ascii'), 'Calibri'); rFonts.set(qn('w:hAnsi'), 'Calibri')
    rPr.append(rFonts)
    sz = OxmlElement('w:sz'); sz.set(qn('w:val'), '18'); rPr.append(sz)
    color = OxmlElement('w:color')
    color.set(qn('w:val'), 'FFFFFF' if is_header else '1F293B')
    rPr.append(color)
    if is_header:
        b = OxmlElement('w:b'); rPr.append(b)
    
    t = OxmlElement('w:t')
    t.set(qn('xml:space'), 'preserve')
    t.text = text
    r.append(t); p.append(r); tc.append(p)
    return tc

# 4. Rebuild rows
for ri, hd in enumerate(header_data):
    tr = OxmlElement('w:tr')
    trPr = OxmlElement('w:trPr')
    tr.append(trPr)
    cs = OxmlElement('w:cantSplit'); trPr.append(cs)
    tr.append(make_cell(hd['doc'], is_header=True, row_idx=ri))
    tr.append(make_cell(hd['ref'], is_header=True, row_idx=ri))
    tbl.append(tr)
```

## Pitfalls

- **gridSpan removal:** After removing gridCols from tblGrid, also remove gridSpan from each tc's tcPr. Otherwise the cell still claims to span 2 columns and the table renders wrong.
- **Row index for alternating colors:** When rebuilding, track `row_idx` separately from `ri` if you skip rows. The alternating fill depends on visual position, not data index.
- **Always extract data from the ORIGINAL file first** (before any edits), then rebuild. If you edit the table in-place (removing tc elements), the gridSpan values change and extraction becomes unreliable.
- **cantSplit on every row** means a tall table pushes entirely to the next page. This is correct per user request — they don't want tables split across pages.
