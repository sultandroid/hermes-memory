# DOCX Table Structure Repair — Mismatched Column Counts

**When to use:** Tables where header row has different number of columns than data rows (merged cells, empty trailing columns, gridSpan mismatches). User says "table columns not equal" or "2nd row columns don't match header".

## Detection

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

## Root causes

| Symptom | Cause | Fix |
|---------|-------|-----|
| Header has 9 cols, data has 5 | Header has empty trailing cells (Word artifact) | Rebuild with 5 cols |
| Header has 3 cols, data has 2 | Data rows use gridSpan=2 (merged cells) | Rebuild with 3 cols, split pipe-delimited content |
| Header has 12 cols, data has 4 | Header has 8 empty trailing cells | Rebuild with 4 cols |
| Header has 6 cols, data has 5 | Header has 1 empty trailing cell | Rebuild with 5 cols |

## Rebuild pattern

Extract data from original table via XML tc elements, then rebuild from scratch:

```python
def get_tc_text(tc):
    return ''.join(t.text or '' for t in tc.findall('.//' + qn('w:t'))).strip()

def make_cell(text, is_header=False, row_idx=0):
    """Create a w:tc element with proper styling"""
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
    # ... margins, paragraph, run, font, text ...
    return tc

def rebuild_table(table, data_rows, num_cols):
    """Rebuild a table from data_rows (list of lists of strings)"""
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

## Common data extraction patterns

### T3 — Current Risk Snapshot (header 9→5 cols)
```python
data = []
for ri, row in enumerate(table.rows):
    tc_elements = list(row._tr.findall(qn('w:tc')))
    if ri == 0:
        row_data = [get_tc_text(tc) for tc in tc_elements[:5]]  # skip empty trailing
    else:
        row_data = [get_tc_text(tc) for tc in tc_elements]
    data.append(row_data)
rebuild_table(table, data, 5)
```

### T7 — Current Risk Distribution (3-col header, 2-col data with pipe-delimited content)
```python
data = []
for ri, row in enumerate(table.rows):
    tc_elements = list(row._tr.findall(qn('w:tc')))
    if ri == 0:
        row_data = [get_tc_text(tc) for tc in tc_elements]
    else:
        cat = get_tc_text(tc_elements[0])
        rest = get_tc_text(tc_elements[1])
        parts = [p.strip() for p in rest.split('|')]
        code = parts[0] if len(parts) >= 1 else ''
        count = parts[1] if len(parts) >= 2 else ''
        critical = parts[2] if len(parts) >= 3 else ''
        high = parts[3] if len(parts) >= 4 else ''
        row_data = [cat, code, f"{count} | {critical} | {high}"]
    data.append(row_data)
rebuild_table(table, data, 3)
```

### T28 — Register Status Summary (header 12→4 cols)
```python
data = []
for ri, row in enumerate(table.rows):
    tc_elements = list(row._tr.findall(qn('w:tc')))
    if ri == 0:
        row_data = [get_tc_text(tc) for tc in tc_elements[:4]]
    else:
        row_data = [get_tc_text(tc) for tc in tc_elements]
    data.append(row_data)
rebuild_table(table, data, 4)
```

## Pitfalls

- **Always work from a backup copy.** Multiple failed rebuild attempts corrupt the file. Keep `/tmp/risk_plan_original.docx` and restore before each attempt.
- **Rebuilding loses all original formatting** — the new cells use the `make_cell()` styling. Run the uniform table styling pass after rebuilding.
- **gridSpan detection:** `tcPr.find(qn('w:gridSpan'))` tells you if a cell spans multiple grid columns. The `getattr(tc, 'gridSpan', 1)` approach doesn't work — use XML directly.
- **vMerge detection:** `tcPr.find(qn('w:vMerge'))` with `val="restart"` or no val (continue) indicates vertical merged cells. These are rare in project plan tables.
- **After rebuild, verify:** `len(table.columns)` should equal `num_cols`, and every row should have the same number of tc elements.
