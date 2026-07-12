# DOCX Formatting Fixes — Page Breaks, Table Splitting, Column Widths

**When to use:** User asks to "fix tables", "don't split tables", "add page breaks before sections", "fix column widths", or "make Rev00 from RevC03" on an existing DOCX.

## Common request patterns

| User says | What they want |
|---|---|
| "dont split the tables in two tables" | Set `cantSplit` on every table row |
| "always break pages in the new sections" | Add `pageBreakBefore` to all H2 section headings |
| "fix tables column width" | Set proportional percentage widths on all table cells |
| "make version Rev00" | Copy RevC03 → Rev00, apply formatting fixes, update revision metadata |

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

Add `pageBreakBefore` to every H2 (numbered section heading like "1. Document Control", "2. Purpose...") and section divider paragraphs:

```python
body = doc.element.body
h2_count = 0

# Match numbered H2 headings: "1. ", "2. ", ..., "12. "
# Also match section divider text like "ADMINISTRATIVE GOVERNANCE"
section_divider_texts = [
    "ADMINISTRATIVE GOVERNANCE", "STRATEGIC GOVERNANCE", "TEAM ORGANIZATION",
    "RESOURCE BREAKDOWN", "DEPLOYMENT TIMELINE", "RESOURCE LOADING",
    "PHYSICAL DEPLOYMENT", "INDUCTION", "DEMOBILIZATION", "RESOURCE CONTROL",
    "PLAN GOVERNANCE"
]

for p in doc.paragraphs:
    txt = p.text.strip()
    
    is_h2 = any(txt.startswith(f"{n}. ") and len(txt) < 100 for n in range(1, 13))
    is_divider = any(dt in txt.upper() for dt in section_divider_texts) and len(txt) < 100
    
    if is_h2 or is_divider:
        pPr = p._p.find(qn('w:pPr'))
        if pPr is None:
            pPr = OxmlElement('w:pPr')
            p._p.insert(0, pPr)
        
        existing = pPr.find(qn('w:pageBreakBefore'))
        if existing is None:
            pb = OxmlElement('w:pageBreakBefore')
            pPr.append(pb)
            h2_count += 1
```

**Pitfall:** Only add page breaks to section-level headings (H2), not sub-headings (H3 like "1.1", "2.1"). Sub-headings should flow naturally after their parent section content. The divider paragraphs (all-caps section labels like "ADMINISTRATIVE GOVERNANCE") also need breaks.

## 2. Prevent table splitting across pages

Set `cantSplit` on every table row. Also set table-level width to 100%:

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

## 4. RevC03 → Rev00 reset pattern

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

## 6. Charts check

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
