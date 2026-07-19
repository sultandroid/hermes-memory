# DOCX Formatting Fixes — Page Breaks, Table Splitting, Column Widths

**When to use:** User asks to "fix tables", "don't split tables", "add page breaks before sections", "fix column widths", or "make Rev00 from RevC03" on an existing DOCX.

## Common request patterns

| User says | What they want |
|---|---|
| "dont split the tables in two tables" | Set `cantSplit` on every table row |
| "always break pages in the new sections" | Add `pageBreakBefore` to all H2 section headings |
| "fix tables column width" | Set proportional percentage widths on all table cells |
| "make version Rev00" | Copy RevC03 to Rev00, apply formatting fixes, update revision metadata |

## Runtime: terminal heredoc

python-docx is installed system-wide but NOT in execute_code sandbox. Always use:

```python
python3 << 'PYEOF'
from docx import Document
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
import shutil

src = "input.docx"
dst = "output.docx"
shutil.copy2(src, dst)
doc = Document(dst)
# ... edits ...
doc.save(dst)
PYEOF
```

## 1. Page breaks before section headings

Add `pageBreakBefore` to every major section heading. Use regex patterns for robust matching across different document styles:

```python
import re

pb_count = 0
for p in doc.paragraphs:
    text = p.text.strip()
    if not text:
        continue
    
    clean = text.lstrip("'\"` ")
    is_section = False
    
    # "N  TEXT" or "N TEXT" where N is 1-15 (section headings)
    if re.match(r'^\d{1,2}\s+[A-Z]', clean):
        is_section = True
    
    # "A  TEXT", "B TEXT", "C ABBREVIATIONS" (appendices)
    if re.match(r'^[A-C]\s+[A-Z]', clean):
        is_section = True
    
    # "DOCUMENT CONTROL", "TABLE OF CONTENTS"
    if clean in ["DOCUMENT CONTROL", "TABLE OF CONTENTS"]:
        is_section = True
    
    # All-caps section dividers like "ADMINISTRATIVE GOVERNANCE"
    if re.match(r'^[A-Z][A-Z\s&/]{3,60}$', clean):
        is_section = True
    
    if is_section:
        pPr = p._p.find(qn('w:pPr'))
        if pPr is None:
            pPr = OxmlElement('w:pPr')
            p._p.insert(0, pPr)
        
        existing = pPr.find(qn('w:pageBreakBefore'))
        if existing is None:
            pb = OxmlElement('w:pageBreakBefore')
            pPr.append(pb)
            pb_count += 1
```

**Pitfall:** Only add page breaks to section-level headings (H1/H2), not sub-headings (H3 like "1.1", "2.1"). Sub-headings should flow naturally after their parent section content. The regex `^\d{1,2}\s+[A-Z]` catches both "1  PURPOSE" (double space) and "12 RISK" (single space) patterns that different documents use. Some documents have leading quote characters (`'12 RISK'`) — strip those with `lstrip("'\"` ")` before matching.

## 2. Prevent table splitting across pages + compact cells

Set `cantSplit` on every table row. Also compact cell margins and reduce font size to fit more content per page:

```python
for table in doc.tables:
    for row in table.rows:
        tr = row._tr
        trPr = tr.find(qn('w:trPr'))
        if trPr is None:
            trPr = OxmlElement('w:trPr')
            tr.insert(0, trPr)
        cantSplit = trPr.find(qn('w:cantSplit'))
        if cantSplit is None:
            trPr.append(OxmlElement('w:cantSplit'))
        
        # Compact each cell: reduce margins, font size, line spacing
        for cell in row.cells:
            tc = cell._tc
            tcPr = tc.find(qn('w:tcPr'))
            if tcPr is None:
                tcPr = OxmlElement('w:tcPr')
                tc.insert(0, tcPr)
            tcMar = tcPr.find(qn('w:tcMar'))
            if tcMar is None:
                tcMar = OxmlElement('w:tcMar')
                tcPr.append(tcMar)
            # Set top/bottom=0, left/right=28dxa (~0.5mm)
            for edge, val in [('top', '0'), ('bottom', '0'), ('left', '28'), ('right', '28')]:
                el = tcMar.find(qn(f'w:{edge}'))
                if el is None:
                    el = OxmlElement(f'w:{edge}')
                    tcMar.append(el)
                el.set(qn('w:w'), val)
                el.set(qn('w:type'), 'dxa')
            
            for p in cell.paragraphs:
                for run in p.runs:
                    if run.font.size is None or run.font.size > Pt(8):
                        run.font.size = Pt(8)
                p.paragraph_format.space_before = Pt(0)
                p.paragraph_format.space_after = Pt(0)
                p.paragraph_format.line_spacing = Pt(10)
```

```python
for ti, t in enumerate(doc.tables):
    tbl = t._tbl
    tblPr = tbl.find(qn('w:tblPr'))
    if tblPr is None:
        tblPr = OxmlElement('w:tblPr')
        tbl.insert(0, tblPr)
    
    # Set table width to 100%
    tblW = tblPr.find(qn('w:tblW'))
    if tblW is None:
        tblW = OxmlElement('w:tblW')
        tblPr.append(tblW)
    tblW.set(qn('w:w'), '5000')
    tblW.set(qn('w:type'), 'pct')
    
    # Set cantSplit on each row
    for ri, row in enumerate(t.rows):
        tr = row._tr
        trPr = tr.find(qn('w:trPr'))
        if trPr is None:
            trPr = OxmlElement('w:trPr')
            tr.insert(0, trPr)
        
        cs = trPr.find(qn('w:cantSplit'))
        if cs is None:
            cs = OxmlElement('w:cantSplit')
            trPr.append(cs)
        
        # keepNext on header row
        if ri == 0:
            kn = trPr.find(qn('w:keepNext'))
            if kn is None:
                kn = OxmlElement('w:keepNext')
                trPr.append(kn)
```

**Pitfall:** `cantSplit` on every row means a table that's too tall for one page will push entirely to the next page, leaving a large gap. This is the correct behaviour — the user explicitly asked for no table splitting. If they later complain about gaps, offer to remove cantSplit from mid-table rows.

## 3. Set proportional column widths

Use percentage-based widths so they scale to any page width. Define width profiles by column count:

```python
# Width profiles: percentages per column count
WIDTH_PROFILES = {
    2: [35, 65],
    3: [20, 45, 35],
    4: [10, 25, 35, 30],
    5: [15, 20, 25, 20, 20],
    6: [20, 20, 20, 15, 15, 10],
}

for ti, t in enumerate(doc.tables):
    num_cols = len(t.columns)
    if num_cols == 0:
        continue
    
    widths_pct = WIDTH_PROFILES.get(num_cols, [100 // num_cols] * num_cols)
    
    for row in t.rows:
        for ci, cell in enumerate(row.cells):
            tc = cell._tc
            tcPr = tc.find(qn('w:tcPr'))
            if tcPr is None:
                tcPr = OxmlElement('w:tcPr')
                tc.insert(0, tcPr)
            
            existing_w = tcPr.find(qn('w:tcW'))
            if existing_w is not None:
                tcPr.remove(existing_w)
            
            tcW = OxmlElement('w:tcW')
            tcW.set(qn('w:w'), str(widths_pct[ci] if ci < len(widths_pct) else 10))
            tcW.set(qn('w:type'), 'pct')
            tcPr.append(tcW)
```

**Pitfall:** Percentage widths (`type='pct'`) are relative to the table's total width. If the table itself has `type='dxa'` (fixed), the percentages won't scale. Always set table-level width to `type='pct'` first (see step 2).

## 4. RevC03 to Rev00 reset pattern

When the user asks to "make Rev00" from a RevC03 (or any Cxx revision), this is a revision reset — not an increment. The file is copied as-is with formatting fixes applied, and the revision label in the filename changes to Rev00. Do NOT update revision metadata inside the document (the content stays at C03 level; only the filename changes to Rev00 for the formatting-fix baseline).

```python
import shutil
src = "Project_Resource_Management_Plan_RevC03.docx"
dst = src.replace("RevC03", "Rev00")
shutil.copy2(src, dst)
# Apply formatting fixes to dst
doc = Document(dst)
# ... page breaks, cantSplit, column widths ...
doc.save(dst)
```

## 5. Verification after fixes

Always verify the output before presenting:

```python
doc2 = Document(dst)
print(f"Paragraphs: {len(doc2.paragraphs)}")
print(f"Tables: {len(doc2.tables)}")

# Count page breaks
pb_count = sum(1 for p in doc2.paragraphs 
               if p._p.find(qn('w:pPr')) is not None 
               and p._p.find(qn('w:pPr')).find(qn('w:pageBreakBefore')) is not None)
print(f"Page breaks: {pb_count}")

# Count cantSplit rows
cs_count = sum(1 for t in doc2.tables for row in t.rows
               if row._tr.find(qn('w:trPr')) is not None
               and row._tr.find(qn('w:trPr')).find(qn('w:cantSplit')) is not None)
print(f"Rows with cantSplit: {cs_count}")

# Check table widths
for ti, t in enumerate(doc2.tables):
    if t.rows:
        widths = []
        for ci, cell in enumerate(t.rows[0].cells):
            tc = cell._tc
            tcPr = tc.find(qn('w:tcPr'))
            if tcPr is not None:
                tcW = tcPr.find(qn('w:tcW'))
                if tcW is not None:
                    widths.append(f"{tcW.get(qn('w:w'))}({tcW.get(qn('w:type'))})")
        print(f"  T{ti} widths: {widths}")
```

## 6. Halftone remark paragraphs using `add_remark()`

Every SamayaDoc document should use `add_remark()` for descriptive/commentary sentences between headings and tables instead of `add_body()`. This renders them in **halftone gray `#64748B` at 9pt** — visually de-emphasised from substantive body text.

```python
# Instead of:
doc.add_body("4 spheres of influence showing the contractual hierarchy.")

# Use:
doc.add_remark("4 spheres of influence showing the contractual hierarchy.")
# → 9pt halftone #64748B, compact spacing (2pt before/after, 11pt line)
```

**When to use `add_remark()` vs `add_body()`:**

| Use `add_body()` for | Use `add_remark()` for |
|---|---|
| Project metadata (name, ref, revision) | Short descriptions of tables/charts |
| Policy statements, scope descriptions | Explanatory notes between sections |
| Formal content paragraphs | Commentary / clarification sentences |
| Paragraphs that carry contractual weight | "This snapshot baselined..." timestamps |
| Paragraphs > ~180 chars of content | RACI legend definitions |

**Post-processing fallback** (when editing existing docs, not generating from scratch):

```python
HALFTONE = RGBColor(0x64, 0x74, 0x8B)
for p in doc.paragraphs:
    text = p.text.strip()
    if not text or len(text) < 15:
        continue
    if p.runs and p.runs[0].font.bold:
        continue  # skip headings
    if len(text) < 180:
        for run in p.runs:
            run.font.size = Pt(9)
            run.font.color.rgb = HALFTONE
        p.paragraph_format.space_before = Pt(2)
        p.paragraph_format.space_after = Pt(2)
```

## 7. Image rendering fix (empty cNvPr names)

After python-docx edits, embedded PNG images may not render in Word. The root cause is **empty `pic:cNvPr name=""` attributes**. Fix via zip manipulation:

```python
import zipfile
from lxml import etree

with zipfile.ZipFile(docx_path, 'r') as zin:
    doc_xml = zin.read('word/document.xml')
    root = etree.fromstring(doc_xml)
    
    NS = {
        'pic': 'http://schemas.openxmlformats.org/drawingml/2006/picture',
        'wp': 'http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing',
        'a': 'http://schemas.openxmlformats.org/drawingml/2006/main',
    }
    
    # Fix empty cNvPr names
    for cnvpr in root.findall('.//pic:cNvPr', NS):
        name = cnvpr.get('name', '')
        if not name or name.strip() == '':
            cnvpr_id = cnvpr.get('id', '')
            docprs = root.findall(f'.//wp:docPr[@id="{cnvpr_id}"]', NS)
            if docprs and docprs[0].get('name', ''):
                cnvpr.set('name', docprs[0].get('name'))
            else:
                cnvpr.set('name', f'Image_{cnvpr_id}')
    
    # Add noChangeAspect to graphicFrameLocks
    for lock in root.findall('.//a:graphicFrameLocks', NS):
        if lock.get('noChangeAspect') is None:
            lock.set('noChangeAspect', '1')
    
    fixed_xml = etree.tostring(root, xml_declaration=True, encoding='UTF-8', standalone=True)
    
    with zipfile.ZipFile(docx_path + '.tmp', 'w', zipfile.ZIP_DEFLATED) as zout:
        for item in zin.infolist():
            if item.filename == 'word/document.xml':
                zout.writestr(item, fixed_xml)
            else:
                zout.writestr(item, zin.read(item.filename))

os.replace(docx_path + '.tmp', docx_path)
```

Also remove orphaned media files (images in `word/media/` not referenced in `word/_rels/document.xml.rels`):

```python
with zipfile.ZipFile(docx_path, 'r') as zin:
    rels = zin.read('word/_rels/document.xml.rels').decode('utf-8')
    refs = re.findall(r'Target="([^"]*media[^"]*)"', rels)
    
    with zipfile.ZipFile(docx_path + '.tmp', 'w', zipfile.ZIP_DEFLATED) as zout:
        for item in zin.infolist():
            if item.filename.startswith('word/media/'):
                short = item.filename.split('/')[-1]
                if not any(short in r for r in refs):
                    continue  # skip orphan
            zout.writestr(item, zin.read(item.filename))
    os.replace(docx_path + '.tmp', docx_path)
```

## 8. Section page breaks for sub-sections

Add `pageBreakBefore` to sub-section headings (4.2, 4.3, 8.4 etc.) when they start a major new content block:

```python
for p in doc.paragraphs:
    t = p.text.strip()
    if t in ['4.2  TIER 2 - DESIGN SPECIALISTS', '4.3  TIER 3 - AUTHORITIES + CONDITIONAL SPECIALISTS', '8.4  BIM FEDERATION CADENCE']:
        pPr = p._p.get_or_add_pPr()
        existing = pPr.find(qn('w:pageBreakBefore'))
        if existing is None:
            pPr.append(parse_xml(f'<w:pageBreakBefore {nsdecls("w")} w:val="1"/>'))
```

## 9. Apply Word heading styles after SamayaDoc generation

SamayaDoc's `add_h1()`/`add_h2()`/`add_h3()` apply direct formatting (font size, bold, color) but do NOT set the Word paragraph style. The user will reject documents where all paragraphs show as "Normal" style. Apply after all content is generated:

```python
for p in doc.paragraphs:
    t = p.text.strip()
    if not t:
        continue
    if t == 'STAKEHOLDER MANAGEMENT PLAN':  # or whatever the doc title is
        p.style = doc.styles['Heading 1']
    elif len(t) > 3 and t[0].isdigit() and '.0' in t[:4]:
        p.style = doc.styles['Heading 2']
    elif len(t) > 3 and t[0].isdigit() and '.' in t[:5] and '.0' not in t[:4]:
        p.style = doc.styles['Heading 3']
```

## 10. Fix mismatched table column counts (merged cells / empty columns)

When a DOCX has tables where header rows and data rows have different numbers of XML `w:tc` elements, the table renders with broken column alignment. This happens when:
- The original was created with merged cells (gridSpan) that python-docx doesn't expand
- Extra empty columns were added to the header row
- Data rows have fewer tc elements than the grid defines

### Detection

```python
from docx.oxml.ns import qn

for ti, table in enumerate(doc.tables):
    if len(table.rows) < 2:
        continue
    first_row_tcs = len(list(table.rows[0]._tr.findall(qn('w:tc'))))
    for ri, row in enumerate(table.rows):
        tcs = len(list(row._tr.findall(qn('w:tc'))))
        if tcs != first_row_tcs:
            print(f"T{ti}: R0={first_row_tcs}tc, R{ri}={tcs}tc")
```

### Fix: rebuild the table from scratch

Extract data from the original XML tc elements (handling gridSpan), then rebuild with consistent column count:

```python
def get_tc_text(tc):
    return ''.join(t.text or '' for t in tc.findall('.//' + qn('w:t'))).strip()

def make_cell(text, is_header=False, row_idx=0):
    tc = OxmlElement('w:tc')
    tcPr = OxmlElement('w:tcPr')
    tc.append(tcPr)
    tcW = OxmlElement('w:tcW')
    tcW.set(qn('w:w'), '1875')
    tcW.set(qn('w:type'), 'dxa')
    tcPr.append(tcW)
    shd = OxmlElement('w:shd')
    shd.set(qn('w:val'), 'clear')
    shd.set(qn('w:color'), 'auto')
    shd.set(qn('w:fill'), '1E293B' if is_header else ('FFFFFF' if row_idx % 2 == 1 else 'F1F5F9'))
    tcPr.append(shd)
    # ... margins, paragraph, run with Calibri 9pt ...
    return tc

def rebuild_table(table, data_rows, num_cols):
    tbl = table._tbl
    for row in list(tbl.findall(qn('w:tr'))):
        tbl.remove(row)
    tblGrid = tbl.find(qn('w:tblGrid'))
    if tblGrid is not None:
        for gc in list(tblGrid.findall(qn('w:gridCol'))):
            tblGrid.remove(gc)
        for _ in range(num_cols):
            gc = OxmlElement('w:gridCol')
            gc.set(qn('w:w'), '1875')
            tblGrid.append(gc)
    for ri, row_data in enumerate(data_rows):
        tr = OxmlElement('w:tr')
        trPr = OxmlElement('w:trPr')
        tr.append(trPr)
        cs = OxmlElement('w:cantSplit')
        trPr.append(cs)
        is_header = (ri == 0)
        for ci, cell_text in enumerate(row_data):
            tr.append(make_cell(cell_text, is_header=is_header, row_idx=ri))
        tbl.append(tr)
```

### Common patterns by column count

| Original issue | Detection | Fix |
|---|---|---|
| Header 9 cols (5 text + 4 empty), data 5 | `R0=9tc, R1=5tc` | Rebuild 5 cols, take first 5 header texts |
| Header 3 cols, data 2 (merged) | `R0=3tc, R1=2tc` | Extract pipe-delimited content, split into proper cols |
| Header 6 cols (last empty), data 5 | `R0=6tc, R1=5tc` | Rebuild 5 cols, drop empty last header col |
| Header 12 cols (4 text + 8 empty), data 4 | `R0=12tc, R1=4tc` | Rebuild 4 cols, take first 4 header texts |
| Header 2 cols, data 4 | `R0=2tc, R1=4tc` | Rebuild 4 cols, pad header rows with empty cells |

**Pitfall:** When extracting data from merged cells (gridSpan), python-docx's `row.cells[ci].text` may return empty strings for cells that are part of a merge. Always use XML-level `tc.findall('.//' + qn('w:t'))` to get actual text. Check `gridSpan` and `vMerge` attributes on `tcPr` to understand merge structure.

## 11. Writing to empty table cells (no runs)

When a table cell has no runs (`len(p.runs) == 0`), you cannot set `run.text`. Fix:

```python
p = cell.paragraphs[0]
if len(p.runs) == 0:
    run = p.add_run("your text here")
    run.font.size = Pt(9)
    run.font.name = 'Calibri'
    run.font.color.rgb = RGBColor(0x1F, 0x29, 0x3B)
else:
    p.runs[0].text = "your text here"
```

## 12. Removing sections (heading + table) from an existing DOCX

When the user asks to remove a section (e.g. "remove Appendix A, B, and 15"), you need to remove BOTH the section heading paragraph AND its associated table. The body element tree is flat — paragraphs and tables are siblings, not nested.

### Detection

```python
# Find target paragraphs by exact text match
target_texts = ["15 APPENDICES", "A  RISK REGISTER LOCATION", "B KEY RISK-RELATED DOCUMENTS AND DATA GAPS"]
target_paras = []
for i, p in enumerate(doc.paragraphs):
    t = p.text.strip()
    if t in target_texts:
        target_paras.append(p._p)

# Find target tables by header cell content
tables_to_remove = []
for ti, table in enumerate(doc.tables):
    if table.rows:
        first_cell = table.rows[0].cells[0].text.strip()
        if first_cell == 'Version' and table.rows[0].cells[1].text.strip() == 'Location':
            tables_to_remove.append(table._tbl)  # Appendix A
        elif first_cell == 'DOCUMENT' and table.rows[0].cells[1].text.strip() == 'REFERENCE':
            tables_to_remove.append(table._tbl)  # Appendix B
```

### Removal

Remove from the body element in reverse order to preserve indices:

```python
body = doc.element.body
elements_to_remove = target_paras + [t for t, _ in tables_to_remove]

for elem in reversed(elements_to_remove):
    body.remove(elem)
```

**Pitfall:** The body element tree is flat — paragraphs and tables are siblings. You cannot rely on python-docx's `doc.paragraphs` index to find the table position. Always use XML-level matching on `table.rows[0].cells[0].text` to identify which table to remove. Remove in reverse order so earlier indices don't shift.

## 13. Adding a DC block (Prepared/Reviewed/Approved) after revision history

When the user asks to add a document control block with Prepared by / Reviewed by / Approved by, create a 4-column table and insert it after the revision history table.

### Table structure

| (empty) | Prepared by | Reviewed by | Approved by |
|---------|-------------|-------------|-------------|
| Name:   |             |             |             |
| Name:   |             |             |             |
| Name:   |             |             |             |

### Implementation

Build the table from scratch using OxmlElement (not python-docx's `add_table()`) so you can insert it at a specific position in the body:

```python
def make_dc_table():
    tbl = OxmlElement('w:tbl')
    tblPr = OxmlElement('w:tblPr')
    tbl.append(tblPr)
    tblW = OxmlElement('w:tblW')
    tblW.set(qn('w:w'), '5000')
    tblW.set(qn('w:type'), 'pct')
    tblPr.append(tblW)
    
    # Grid: 4 columns
    tblGrid = OxmlElement('w:tblGrid')
    tbl.append(tblGrid)
    for w in ['1000', '1500', '2500', '2500']:
        gc = OxmlElement('w:gridCol')
        gc.set(qn('w:w'), w)
        tblGrid.append(gc)
    
    # Header row: navy background, white bold text
    tr = OxmlElement('w:tr')
    trPr = OxmlElement('w:trPr')
    tr.append(trPr)
    cs = OxmlElement('w:cantSplit')
    trPr.append(cs)
    
    for text in ['', 'Prepared by', 'Reviewed by', 'Approved by']:
        tc = OxmlElement('w:tc')
        tcPr = OxmlElement('w:tcPr')
        tc.append(tcPr)
        tcW = OxmlElement('w:tcW')
        tcW.set(qn('w:w'), '1875')
        tcW.set(qn('w:type'), 'dxa')
        tcPr.append(tcW)
        shd = OxmlElement('w:shd')
        shd.set(qn('w:val'), 'clear')
        shd.set(qn('w:color'), 'auto')
        shd.set(qn('w:fill'), '1E293B')
        tcPr.append(shd)
        # ... paragraph with white bold 9pt Calibri text ...
        tr.append(tc)
    tbl.append(tr)
    
    # Data rows: alternating shading, "Name:" in first column
    for row_idx in range(3):
        tr = OxmlElement('w:tr')
        # ... same pattern, alternating FFFFFF/F1F5F9 ...
        for ci, label in enumerate(['Name:', '', '', '']):
            # ... cell with 9pt Calibri text ...
            tr.append(tc)
        tbl.append(tr)
    
    return tbl

# Insert after revision history table
body = doc.element.body
rev_table = doc.tables[-1]._tbl  # last table is revision history
insert_idx = list(body).index(rev_table) + 1
body.insert(insert_idx, make_dc_table())
```

**Pitfall:** The DC block must be inserted AFTER the revision history table, not before. Find the revision table by position (last table) and insert at `index + 1`. The table must use the same styling as all other tables (navy header, alternating rows, cantSplit) for consistency.

## 14. Paragraph classification for DOCX reformatting

When reformatting an existing DOCX (not generating from scratch), classify paragraphs into these tiers:

| Class | Font | Color | Bold | Spacing | Matches |
|---|---|---|---|---|---|
| H1 | 11pt Calibri | Navy `#1E293B` | Yes | 12pt before, 4pt after | `r'^\d{1,2}\s+[A-Z]'` or all-caps divider |
| H2 | 10.5pt Calibri | Navy `#1E293B` | Yes | 8pt before, 3pt after | `r'^\d{1,2}\.\d{1,2}\s+[A-Z]'` |
| TOC | 10pt Calibri | Navy `#1E293B` | No | - | `r'^\d{1,2}\.\s{2,}[A-Z]'` |
| Body | 10pt Calibri | `#1F293B` | No | 3pt before/after | Long text, bullet items |
| Halftone | 9pt Calibri | Gray `#64748B` | No | 2pt before/after | Short text <120 chars, references (RIBA, Contract, ER, SoW, etc.) |

**Pitfall:** The initial pass often makes ALL body text halftone (9pt gray) because the heuristic "short text = remark" is too aggressive. Section headings like "10. Risk Review Cadence" are short but are NOT remarks. Use regex patterns to detect actual headings first, then classify remaining text by length and content keywords.

### Classification order (mandatory)

Apply classifications in this exact order to avoid false positives:

1. **H1** — `r'^\d{1,2}\s{2,}[A-Z]'` (e.g. "1  PURPOSE & SCOPE") or all-caps divider `r'^[A-Z][A-Z\s&/]{3,60}$'`
2. **H2** — `r'^\d{1,2}\.\d{1,2}\s{2,}[A-Z]'` (e.g. "1.1  PURPOSE")
3. **TOC** — `r'^\d{1,2}\.\s{2,}[A-Z]'` (e.g. "1.  Purpose & Scope")
4. **Cover metadata** — specific strings like "RISK MANAGEMENT PLAN", "Aseer Regional Museum"
5. **Bullet items** — starts with `•` or `- `
6. **Halftone** — short text <120 chars OR contains reference keywords (RIBA, Contract, Article, ER, SoW, SBC, FIDIC, ASHRAE, "As a result of", "Residual Risk", "Secondary Risk", "Triggered by", "Team Member > PM", "Contingency adequacy", "This document is maintained", "Identify > Assess")
7. **Body** — everything else

**Pitfall:** Strip leading quote/backtick characters with `text.lstrip("'\"` ")` before regex matching. Some documents have `'12 RISK BUDGET & CONTINGENCY'` with leading quotes that break the pattern.

## 15. Moving tables to first page (cover → DC → Rev)

When the user asks to put the DC block and revision history on the first page (after cover metadata), move them by removing from their current position and re-inserting after the cover table:

```python
body = doc.element.body

cover_table = doc.tables[0]._tbl
rev_table = doc.tables[29]._tbl    # find by position or content
dc_table = doc.tables[30]._tbl

# Remove from current positions (reverse order)
body.remove(dc_table)
body.remove(rev_table)

# Re-insert after cover table
new_children = list(body)
new_cover_idx = new_children.index(cover_table)
body.insert(new_cover_idx + 1, dc_table)
body.insert(new_cover_idx + 2, rev_table)
```

**Pitfall:** Table indices shift after removal. Always remove in reverse order (last table first), then re-insert. The cover table is always T0 (first table in the document). After moving, verify the order: T0=cover, T1=DC, T2=rev history.

## 16. Adding spacing between first-page tables

After moving DC and rev tables to the first page, add empty paragraphs between them for visual separation:

```python
def insert_spacing_para(after_elem, count=1):
    for _ in range(count):
        p = OxmlElement('w:p')
        pPr = OxmlElement('w:pPr')
        p.append(pPr)
        spacing = OxmlElement('w:spacing')
        spacing.set(qn('w:before'), '0')
        spacing.set(qn('w:after'), '120')  # ~6pt
        spacing.set(qn('w:line'), '240')
        spacing.set(qn('w:lineRule'), 'auto')
        pPr.append(spacing)
        children = list(body)
        idx = children.index(after_elem)
        body.insert(idx + 1, p)

insert_spacing_para(cover_table, 1)
insert_spacing_para(dc_table, 1)
```

## 17. Clearing and replacing page header content

When the user asks to remove doc ref / revision from page headers:

```python
for section in doc.sections:
    header = section.header
    if header:
        for p in header.paragraphs:
            for run in p.runs:
                run.text = ""
            run = p.add_run("New header text")
            run.font.size = Pt(8)
            run.font.color.rgb = RGBColor(0x64, 0x74, 0x8B)
            run.font.name = 'Calibri'
        # Clear any header tables
        for table in header.tables:
            table._tbl.getparent().remove(table._tbl)
```

## 18. Adding a REV00 row to the revision history table

When issuing a new version (REV00 for CG review), add a row to the revision history table. **The revision entry must be client-appropriate** — describe what changed in a way that matters to the reviewer, not internal formatting details.

| Wrong (internal) | Right (client-facing) |
|---|---|
| "Format revision — unified table styles, halftone remarks, page breaks, removed internal references. REV00 issue for CG review." | "REV00 - First issue for CG review" |
| "Fixed table column widths, added cantSplit, removed markdown paths" | "Updated risk distribution data from departmental reviews" |

**Rule:** The revision entry should answer "what changed that affects the content?" not "what did we fix in the formatting?" Formatting fixes are invisible to the client and don't belong in the revision log.

## 19. Inserting a Word TOC field with heading styles

When the user asks for a TOC with page numbers and hyperlinks, replace static text entries with a Word TOC field. This requires applying Word heading styles (Heading 1, Heading 2) to the document paragraphs first.

### Step 1: Apply Word heading styles

```python
import re

h1_pattern = re.compile(r'^(\d{1,2})\s{2,}[A-Z]')
h2_pattern = re.compile(r'^(\d{1,2}\.\d{1,2})\s{2,}[A-Z]')
divider_pattern = re.compile(r'^[A-Z][A-Z\s&/]{3,60}$')
appendix_pattern = re.compile(r'^[A-C]\s{2,}[A-Z]')

for p in doc.paragraphs:
    text = p.text.strip()
    if not text:
        continue
    
    if h1_pattern.match(text):
        p.style = doc.styles['Heading 1']
    elif h2_pattern.match(text):
        p.style = doc.styles['Heading 2']
    elif divider_pattern.match(text) and len(text) < 60:
        p.style = doc.styles['Heading 1']
    elif appendix_pattern.match(text) and len(text) < 60:
        p.style = doc.styles['Heading 1']
    elif text in ["DOCUMENT CONTROL", "TABLE OF CONTENTS"]:
        p.style = doc.styles['Heading 1']
```

### Step 2: Remove old TOC entries

```python
body = doc.element.body
to_remove = []
found_toc = False
for p in doc.paragraphs:
    text = p.text.strip()
    if text == "TABLE OF CONTENTS":
        found_toc = True
        continue
    if found_toc:
        if text.startswith("1  PURPOSE & SCOPE") or text == "1  PURPOSE & SCOPE":
            break
        if text:
            to_remove.append(p._p)

for elem in to_remove:
    try:
        body.remove(elem)
    except:
        pass
```

### Step 3: Insert TOC field

```python
toc_p = OxmlElement('w:p')
toc_pPr = OxmlElement('w:pPr')
toc_p.append(toc_pPr)

# Begin field
r = OxmlElement('w:r')
fldChar_begin = OxmlElement('w:fldChar')
fldChar_begin.set(qn('w:fldCharType'), 'begin')
r.append(fldChar_begin)
toc_p.append(r)

# Instruction
r2 = OxmlElement('w:r')
instrText = OxmlElement('w:instrText')
instrText.set(qn('xml:space'), 'preserve')
instrText.text = 'TOC \\o "1-2" \\h \\z \\u'
r2.append(instrText)
toc_p.append(r2)

# Separate
r3 = OxmlElement('w:r')
fldChar_separate = OxmlElement('w:fldChar')
fldChar_separate.set(qn('w:fldCharType'), 'separate')
r3.append(fldChar_separate)
toc_p.append(r3)

# Placeholder text
r4 = OxmlElement('w:r')
rPr4 = OxmlElement('w:rPr')
r4.append(rPr4)
rFonts = OxmlElement('w:rFonts')
rFonts.set(qn('w:ascii'), 'Calibri')
rFonts.set(qn('w:hAnsi'), 'Calibri')
rPr4.append(rFonts)
sz = OxmlElement('w:sz')
sz.set(qn('w:val'), '20')
rPr4.append(sz)
color = OxmlElement('w:color')
color.set(qn('w:val'), '1E293B')
rPr4.append(color)
t = OxmlElement('w:t')
t.set(qn('xml:space'), 'preserve')
t.text = 'Right-click > Update Field'
r4.append(t)
toc_p.append(r4)

# End field
r5 = OxmlElement('w:r')
fldChar_end = OxmlElement('w:fldChar')
fldChar_end.set(qn('w:fldCharType'), 'end')
r5.append(fldChar_end)
toc_p.append(r5)

# Insert after TOC heading
body.insert(toc_heading_idx + 1, toc_p)
```

**Pitfall:** The TOC field uses `\\o "1-2"` to include Heading 1 and Heading 2 levels. If the document uses custom heading styles, adjust the level range. The `\\h` flag adds hyperlinks, `\\z` hides tab leader dots, `\\u` uses paragraph outline level. After inserting, the user must right-click > Update Field > "Update entire table" in Word to generate page numbers.

## 20. Adding Samaya logo to page header

```python
logo_path = "/Users/mohamedessa/Library/CloudStorage/OneDrive-SAMAYAINVESTMENT/Samaya/Technical Office/_Style-Guides/logos archives/samaya-logo-trans.png"

for section in doc.sections:
    header = section.header
    for p in header.paragraphs:
        p.clear()
    
    p = header.paragraphs[0]
    run = p.add_run()
    run.add_picture(logo_path, width=Inches(1.0))
    
    run2 = p.add_run("    Document Title")
    run2.font.size = Pt(8)
    run2.font.color.rgb = RGBColor(0x64, 0x74, 0x8B)
    run2.font.name = 'Calibri'
    
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
```

**Pitfall:** `run.add_picture()` embeds the image into the DOCX. The logo path must be accessible at generation time. If the path is on OneDrive and TCC-blocked, use the Group Containers fallback path. The image is stored in `word/media/` inside the zip.

## 21. Footer with Page X of Y (Word fields)

```python
for section in doc.sections:
    footer = section.footer
    for p in footer.paragraphs:
        p.clear()
    
    p = footer.paragraphs[0]
    
    # Tab
    run = p.add_run("\tPage ")
    run.font.size = Pt(8)
    run.font.color.rgb = RGBColor(0x64, 0x74, 0x8B)
    
    # PAGE field
    run = p.add_run()
    fldChar_begin = OxmlElement('w:fldChar')
    fldChar_begin.set(qn('w:fldCharType'), 'begin')
    run._r.append(fldChar_begin)
    
    run2 = p.add_run()
    instrText = OxmlElement('w:instrText')
    instrText.set(qn('xml:space'), 'preserve')
    instrText.text = 'PAGE'
    run2._r.append(instrText)
    
    run3 = p.add_run()
    fldChar_separate = OxmlElement('w:fldChar')
    fldChar_separate.set(qn('w:fldCharType'), 'separate')
    run3._r.append(fldChar_separate)
    
    run4 = p.add_run("1")
    run4.font.size = Pt(8)
    run4.font.color.rgb = RGBColor(0x64, 0x74, 0x8B)
    
    run5 = p.add_run()
    fldChar_end = OxmlElement('w:fldChar')
    fldChar_end.set(qn('w:fldCharType'), 'end')
    run5._r.append(fldChar_end)
    
    # " of "
    run = p.add_run(" of ")
    run.font.size = Pt(8)
    run.font.color.rgb = RGBColor(0x64, 0x74, 0x8B)
    
    # NUMPAGES field (same pattern as PAGE)
    run = p.add_run()
    fldChar_begin = OxmlElement('w:fldChar')
    fldChar_begin.set(qn('w:fldCharType'), 'begin')
    run._r.append(fldChar_begin)
    
    run2 = p.add_run()
    instrText = OxmlElement('w:instrText')
    instrText.set(qn('xml:space'), 'preserve')
    instrText.text = 'NUMPAGES'
    run2._r.append(instrText)
    
    run3 = p.add_run()
    fldChar_separate = OxmlElement('w:fldChar')
    fldChar_separate.set(qn('w:fldCharType'), 'separate')
    run3._r.append(fldChar_separate)
    
    run4 = p.add_run("1")
    run4.font.size = Pt(8)
    run4.font.color.rgb = RGBColor(0x64, 0x74, 0x8B)
    
    run5 = p.add_run()
    fldChar_end = OxmlElement('w:fldChar')
    fldChar_end.set(qn('w:fldCharType'), 'end')
    run5._r.append(fldChar_end)
    
    # Company name
    run = p.add_run("\tSamaya Investment Company")
    run.font.size = Pt(8)
    run.font.color.rgb = RGBColor(0x64, 0x74, 0x8B)
```

**Pitfall:** Word field codes (PAGE, NUMPAGES) must be constructed as three separate runs: fldChar begin → instrText → fldChar separate → placeholder text → fldChar end. The placeholder text ("1") is what Word displays before updating. After opening in Word, the fields auto-update to show the correct page numbers.

## 22. Adding a halftone note under a specific section table

When the user asks to add a note like "This snapshot is based on the live Project Risk Register and is updated weekly" under a specific table:

```python
HALFTONE = RGBColor(0x64, 0x74, 0x8B)
body = doc.element.body

# Find the target table
target_table = None
for table in doc.tables:
    if table.rows and table.rows[0].cells[0].text.strip() == 'Category':
        target_table = table._tbl
        break

# Create halftone paragraph
p = OxmlElement('w:p')
pPr = OxmlElement('w:pPr')
p.append(pPr)
spacing = OxmlElement('w:spacing')
spacing.set(qn('w:before'), '40')
spacing.set(qn('w:after'), '40')
spacing.set(qn('w:line'), '240')
spacing.set(qn('w:lineRule'), 'auto')
pPr.append(spacing)

r = OxmlElement('w:r')
rPr = OxmlElement('w:rPr')
r.append(rPr)
rFonts = OxmlElement('w:rFonts')
rFonts.set(qn('w:ascii'), 'Calibri')
rFonts.set(qn('w:hAnsi'), 'Calibri')
rPr.append(rFonts)
sz = OxmlElement('w:sz')
sz.set(qn('w:val'), '18')  # 9pt
rPr.append(sz)
color = OxmlElement('w:color')
color.set(qn('w:val'), '64748B')
rPr.append(color)

t = OxmlElement('w:t')
t.set(qn('xml:space'), 'preserve')
t.text = "Your note text here."
r.append(t)
p.append(r)

# Insert after the table
children = list(body)
idx = children.index(target_table)
body.insert(idx + 1, p)
```

**Pitfall:** When inserting after a table, check if a note already exists after it (e.g., an RBS note). If so, insert after the existing note, not between the table and the note. Use `idx + 1` and verify the next element's content before inserting.

## 23. Revision entries must be client-appropriate

**Hard rule:** Revision entries describe what changed that affects the content, NOT internal formatting details. The user explicitly corrected this.

| Wrong (internal) | Right (client-facing) |
|---|---|
| "Format revision — unified table styles, halftone remarks, page breaks, removed internal references. REV00 issue for CG review." | "REV00 - First issue for CG review" |
| "Fixed table column widths, added cantSplit, removed markdown paths" | "Updated risk distribution data from departmental reviews" |
| "Removed internal file paths and repo references" | "REV00 - First issue for CG review" |

**User correction signal:** "dont tell such information like this its not usful for the client" — if you wrote formatting/internal details in a revision entry, the user will call it out. The revision log is for the client/CG reviewer, not for the internal team.

## 24. Scanned PDF OCR Workflow

When a supplier letter arrives as a scanned PDF (images only, no text layer):

1. Extract images from PDF using PyMuPDF: `page.get_pixmap(matrix=fitz.Matrix(3, 3))`
2. Save as PNG, convert to JPEG for tesseract
3. Run tesseract with `--psm 6` for single uniform block of text
4. For 1-bit images (black/white), invert before OCR: `ImageOps.invert(img)`
5. Cross-reference multiple OCR runs on different image variants to resolve noise
6. If tesseract fails due to encoding issues, run it directly in shell (not via subprocess in Python)

## 25. SOW-Protect Out-of-Scope Items in Plans

When a plan section mixes in-scope and out-of-scope items, split them. Keep Samaya's scope in the document, flag Employer/third-party scope as SOW-Protect or remove entirely.

Example: PRR-CNS-01 originally had "artifact damage liability, ICOM accreditation, loan conditions" — those are Employer responsibilities, not Samaya's. The in-scope part (dust control, temp/humidity during construction) stayed as a Medium risk.

## 26. Plan documents describe methodology, not live data

**Critical distinction for risk plans, resource plans, and similar methodology documents:**

| Belongs in the plan | Belongs in the live register |
|---|---|
| How risks are identified, assessed, and managed | The actual risk list with scores and EMV |
| The RBS categories and scoring scales | Which categories have active risks |
| The review cadence and RACI | The current risk count and distribution |
| The contingency methodology | The contingency amount |
| The register architecture (how many registers) | The status of each register |

**CG review expectation:** A plan that says "To be recalculated from PRR" or "To be confirmed" for methodology-describes-live-data items is acceptable — the plan describes the process, the register holds the numbers. However, if the plan claims completeness (e.g., "4-register architecture") but one register is "in progress," that's a contradiction. Either complete the register or note it as "under development."

**User preference:** Revision entries should be client-appropriate. "REV00 - First issue for CG review" is correct. "Format revision — unified table styles, halftone remarks, page breaks, removed internal references" is wrong — those are internal formatting details invisible to the client.

## 24. CG response forecasting for plan documents

When the user asks to forecast CG response on a plan document, evaluate against these criteria:

| Code | Meaning | Typical triggers |
|---|---|---|
| A | Accepted | Standard methodology (PMBOK-aligned), no factual errors |
| B | Minor comments | Missing notes on empty categories, role titles instead of names, vague contingency figures |
| C | Revise & Resubmit | Unfilled data placeholders ("To be confirmed"), incomplete register architecture, contradictions between sections |
| D | Rejected | Wrong methodology, missing required sections, factual errors |

**Key insight for methodology plans:** CG evaluates whether the plan describes a workable process, not whether the live data is complete. "To be recalculated from PRR" is acceptable for EMV values because EMV lives in the register. But "AV Register in progress" while claiming "4-register architecture" is a contradiction that triggers Code B/C.

**Common CG comments on risk plans:**
- "RBS has 17 categories but only 12 have active risks" → Add monitoring note
- "No contingency amount stated" → Methodology is sufficient; amount is commercial
- "Role titles instead of names in DC block" → Replace with actual names
- "EMV values marked TBC" → Acceptable if methodology is clear; values live in register

When issuing a new version (REV00 for CG review), add a row to the revision history table:

```python
table = doc.tables[2]  # revision history is T2 after moving
row = table.add_row()

# Set text via XML (cells may have no runs)
texts = ["REV00", "18 July 2026", "Samaya Technical Office", "Description of changes"]
for ci, cell in enumerate(row.cells):
    tc = cell._tc
    # Clear existing text
    for t_elem in tc.findall('.//' + qn('w:t')):
        t_elem.text = ""
    # Find or create a run
    runs = tc.findall('.//' + qn('w:r'))
    if runs:
        t_elem = runs[0].find(qn('w:t'))
        if t_elem is None:
            t_elem = OxmlElement('w:t')
            t_elem.set(qn('xml:space'), 'preserve')
            runs[0].append(t_elem)
        t_elem.text = texts[ci]
    else:
        # Create run from scratch
        p = tc.find(qn('w:p'))
        if p is None:
            p = OxmlElement('w:p')
            tc.append(p)
        r = OxmlElement('w:r')
        rPr = OxmlElement('w:rPr')
        r.append(rPr)
        rFonts = OxmlElement('w:rFonts')
        rFonts.set(qn('w:ascii'), 'Calibri')
        rFonts.set(qn('w:hAnsi'), 'Calibri')
        rPr.append(rFonts)
        sz = OxmlElement('w:sz')
        sz.set(qn('w:val'), '18')
        rPr.append(sz)
        color = OxmlElement('w:color')
        color.set(qn('w:val'), '1F293B')
        rPr.append(color)
        t = OxmlElement('w:t')
        t.set(qn('xml:space'), 'preserve')
        t.text = texts[ci]
        r.append(t)
        p.append(r)
    
    # Style cell (alternating shading)
    tcPr = tc.find(qn('w:tcPr'))
    if tcPr is None:
        tcPr = OxmlElement('w:tcPr')
        tc.insert(0, tcPr)
    fill = 'FFFFFF' if len(table.rows) % 2 == 0 else 'F1F5F9'
    shd = tcPr.find(qn('w:shd'))
    if shd is None:
        shd = OxmlElement('w:shd')
        tcPr.append(shd)
    shd.set(qn('w:val'), 'clear')
    shd.set(qn('w:color'), 'auto')
    shd.set(qn('w:fill'), fill)

# cantSplit
tr = row._tr
trPr = tr.find(qn('w:trPr'))
if trPr is None:
    trPr = OxmlElement('w:trPr')
    tr.insert(0, trPr)
cs = trPr.find(qn('w:cantSplit'))
if cs is None:
    cs = OxmlElement('w:cantSplit')
    trPr.append(cs)
```

**Pitfall:** Newly added table rows via `add_row()` have cells with 1 paragraph and 0 runs. You cannot set `run.text` directly — you must either use `p.add_run()` or write via XML `w:t` elements. Always check `len(p.runs)` before accessing `p.runs[0]`.

When SVG→PNG images don't render in Word (common on macOS with RGBA PNGs), replace the chart with a styled table. Use navy header, alternating rows, compact 8pt font:

```python
table = doc.add_table(rows=N, cols=M)
table.style = 'Table Grid'
# Header row
for ci, h in enumerate(headers):
    cell = table.rows[0].cells[ci]
    cell.text = h
    for p in cell.paragraphs:
        for run in p.runs:
            run.font.bold = True
            run.font.size = Pt(8)
            run.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
    shading = parse_xml(f'<w:shd {nsdecls("w")} w:fill="1E293B" w:val="clear"/>')
    cell._tc.get_or_add_tcPr().append(shading)
# Data rows with alternating shading
for ri, row_data in enumerate(data):
    for ci, val in enumerate(row_data):
        cell = table.rows[ri+1].cells[ci]
        cell.text = val
        for p in cell.paragraphs:
            for run in p.runs:
                run.font.size = Pt(8)
        if ri % 2 == 0:
            shading = parse_xml(f'<w:shd {nsdecls("w")} w:fill="F1F5F9" w:val="clear"/>')
            cell._tc.get_or_add_tcPr().append(shading)
# Set column widths
for row in table.rows:
    for ci, cell in enumerate(row.cells):
        tc = cell._tc
        tcPr = tc.find(qn('w:tcPr'))
        if tcPr is None:
            tcPr = OxmlElement('w:tcPr')
            tc.insert(0, tcPr)
        tcW = tcPr.find(qn('w:tcW'))
        if tcW is None:
            tcW = OxmlElement('w:tcW')
            tcPr.append(tcW)
        tcW.set(qn('w:w'), str(int(widths_cm[ci] * 567)))  # cm to twips
        tcW.set(qn('w:type'), 'dxa')
```

Also remove orphaned media files (images in `word/media/` not referenced in any rels file) to keep the DOCX clean.

Before claiming "charts fixed", verify what's actually in the DOCX:

```python
import zipfile
with zipfile.ZipFile(path) as z:
    chart_files = [f for f in z.namelist() if 'chart' in f.lower()]
    image_files = [f for f in z.namelist() if f.startswith('word/media/')]
    print(f"Charts: {chart_files}")
    print(f"Images: {image_files}")
```

Most DOCX files from this project have PNG images (org charts, phase strips, headcount curves), not OLE chart objects. If there are no chart files, report that to the user rather than pretending to fix them.

### Chart/image disappearance after python-docx edits

**Known issue:** After editing a DOCX with python-docx (adding page breaks, cantSplit, column widths), embedded PNG images may appear to "disappear" in Word. Investigation shows:

- The PNG files are still in the zip (same bytes, same dimensions)
- The drawing XML is intact (inline, correct extents, valid blip embed IDs)
- The relationships are intact (rId -> media/image.png)
- The Content_Types are correct

**Root cause (two factors):**

1. **Empty `pic:cNvPr name=""` attribute** — The `wp:docPr` elements have proper names (e.g., `"Picture 4"`), but the inner `pic:cNvPr` elements (which Word also reads for display) have **empty name attributes**. This mismatch can cause Word to fail rendering the image, especially after bulk edits that trigger re-layout. This is the primary cause.

2. **Missing `noChangeAspect` on `a:graphicFrameLocks`** — If one image has `noChangeAspect="1"` and another doesn't, Word may mis-scale the second image during re-layout, making it appear as a zero-height element.

**Fix script (reusable):**

```python
import zipfile
import xml.etree.ElementTree as ET

NS = {
    'wp': 'http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing',
    'a': 'http://schemas.openxmlformats.org/drawingml/2006/main',
    'pic': 'http://schemas.openxmlformats.org/drawingml/2006/picture',
}

def fix_docx_images(src_path, dst_path):
    """Fix empty cNvPr names and missing noChangeAspect in a DOCX."""
    # Register all namespaces
    for prefix, uri in NS.items():
        ET.register_namespace(prefix, uri)
    ET.register_namespace('r', 'http://schemas.openxmlformats.org/officeDocument/2006/relationships')
    ET.register_namespace('w', 'http://schemas.openxmlformats.org/wordprocessingml/2006/main')
    ET.register_namespace('w14', 'http://schemas.microsoft.com/office/word/2010/wordml')
    ET.register_namespace('wpg', 'http://schemas.microsoft.com/office/word/2010/wordprocessingDrawing')
    ET.register_namespace('mc', 'http://schemas.openxmlformats.org/markup-compatibility/2006')
    ET.register_namespace('wps', 'http://schemas.microsoft.com/office/word/2010/wordprocessingShape')
    
    with zipfile.ZipFile(src_path, 'r') as zin:
        doc_xml = zin.read('word/document.xml').decode('utf-8')
        root = ET.fromstring(doc_xml)
        
        # Fix 1: Set empty pic:cNvPr names from matching wp:docPr names
        for cnvpr in root.findall('.//pic:cNvPr', NS):
            name = cnvpr.get('name', '')
            if not name or name.strip() == '':
                cnvpr_id = cnvpr.get('id', '')
                docprs = root.findall(f'.//wp:docPr[@id="{cnvpr_id}"]', NS)
                if docprs and docprs[0].get('name', ''):
                    cnvpr.set('name', docprs[0].get('name'))
                else:
                    cnvpr.set('name', f'Image_{cnvpr_id}')
        
        # Fix 2: Add noChangeAspect to any graphicFrameLocks missing it
        for lock in root.findall('.//a:graphicFrameLocks', NS):
            if lock.get('noChangeAspect') is None:
                lock.set('noChangeAspect', '1')
        
        # Write fixed DOCX
        fixed_xml = '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\r\n' + \
                    ET.tostring(root, encoding='unicode', xml_declaration=False)
        
        with zipfile.ZipFile(dst_path, 'w', zipfile.ZIP_DEFLATED) as zout:
            for item in zin.infolist():
                if item.filename == 'word/document.xml':
                    zout.writestr(item, fixed_xml.encode('utf-8'))
                else:
                    zout.writestr(item, zin.read(item.filename))
```

**Verification after fix:**

```python
with zipfile.ZipFile(dst_path, 'r') as z:
    verify_root = ET.fromstring(z.read('word/document.xml'))
    for c in verify_root.findall('.//pic:cNvPr', NS):
        name = c.get('name', '')
        assert name and name.strip(), f"cNvPr id={c.get('id')} still empty"
    for l in verify_root.findall('.//a:graphicFrameLocks', NS):
        assert l.get('noChangeAspect') == '1', "Missing noChangeAspect"
```

**Investigation checklist (before fixing):**

1. Verify images are still in the zip: `z.namelist()` → check `word/media/` files exist with non-zero sizes
2. Verify relationships: read `word/_rels/document.xml.rels` → confirm `rIdX` → `media/imageN.png` entries exist
3. Verify drawing XML: find `w:drawing` elements → check `a:blip` has valid `r:embed` attribute
4. Check `pic:cNvPr name=""` — this is the smoking gun
5. Check `a:graphicFrameLocks` for missing `noChangeAspect`
6. Check Content_Types: `[Content_Types].xml` must have `<Default Extension="png" ContentType="image/png"/>`

**Pitfall:** Do NOT tell the user "the charts are gone" without first verifying the zip contents. The images are almost certainly still there — the rendering issue is caused by the empty cNvPr name attribute, not data loss. Always check the zip before reporting. The fix is structural (XML attribute repair), not a re-embed.
