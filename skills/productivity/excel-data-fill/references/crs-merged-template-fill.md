# Filling a Samaya Merged CRS Template Without Breaking It

Working recipe for the Samaya Comments Resolution Sheet (and similar merged Excel templates).
Verified against the AV Package Part II Rev.001 CRS (Aug 2026) and openpyxl 3.1.2.

## Goal
Fill N comment rows into a merged CRS template (header rows 1-10, data rows start at 11)
while preserving the footer/legend/signature block byte-for-byte and not breaking any merges.

## Key facts
- `openpyxl.insert_rows()` does NOT move merged cells. Values move, merges don't → broken file. Never use it.
- `ws.cell(r,c).value = x` raises `AttributeError: 'MergedCell' object ... read-only` inside a merge except at the anchor.
- Unmerging a data region irreversibly breaks the layout.
- The footer (legend + signature block) carries specific styling (bold headers, FFCC9900 fills, medium borders) that a fresh rebuild cannot reproduce.

## Strategy: shift the footer via XML row insertion, then fill data via merge anchors

### Part A — Shift footer down in the sheet XML
Work on a copy of the pristine file. Rewrite the sheet XML inside the .xlsx zip:

```python
import zipfile, re, shutil

PRISTINE = "/path/pristine.xlsx"
SHIFT = 14  # rows >= this shift down by SHIFT

with zipfile.ZipFile(PRISTINE) as z:
    sheet_path = next(n for n in z.namelist() if re.match(r'xl/worksheets/sheet\d+\.xml', n))
    content = z.read(sheet_path).decode('utf-8')

row_pat = re.compile(r'(<row\b.*?</row>)', re.S)
parts = row_pat.split(content)

new_parts = []
for p in parts:
    m = re.match(r'<row\s+r="(\d+)"', p)
    if m:
        idx = int(m.group(1))
        if idx >= 20:   # shift everything from the data end + footer down
            p = re.sub(r'<row\s+r="(\d+)"', f'<row r="{idx+SHIFT}"', p, count=1)
            # shift each cell's r="A{n}"
            p = re.sub(
                r'(<c\s+[^>]*?)\br="([A-Z]+)(\d+)"',
                lambda mm: f'{mm.group(1)}r="{mm.group(2)}{int(mm.group(3))+SHIFT}"',
                p)
    new_parts.append(p)
new_content = ''.join(new_parts)

def shift_ref(ref, d):
    return re.sub(r'([A-Z]+)(\d+)', lambda mm: f'{mm.group(1)}{int(mm.group(2))+d}', ref)

new_content = re.sub(r'<mergeCell ref="([^"]+)"/>', lambda m:
    (f'<mergeCell ref="{shift_ref(m.group(1), SHIFT)}"/>' if int(re.findall(r'\d+', m.group(1).split(':')[0])[0]) >= 20 else m.group(0)),
    new_content)

# write back into a copy of the zip
shutil.copy(PRISTINE, out_path)
zin = zipfile.ZipFile(out_path, 'r')
zout = zipfile.ZipFile(tmp_out, 'w', zipfile.ZIP_DEFLATED)
for item in zin.infolist():
    data = zin.read(item.filename)
    if item.filename == sheet_path:
        data = new_content.encode('utf-8')
    zout.writestr(item, data)
zin.close(); zout.close()
```

### Part B — Fill data rows via merge anchors
```python
import openpyxl
wb = openpyxl.load_workbook(out_path)
ws = wb['CRS']

def setv(r, c, v):
    for mc in ws.merged_cells.ranges:
        if mc.min_row <= r <= mc.max_row and mc.min_col <= c <= mc.max_col:
            if mc.min_row == r and mc.min_col == c:
                ws.cell(r, c).value = v   # top-left anchor only
            return
    ws.cell(r, c).value = v

# header meta via anchors
setv(5,4,'DOC_REF'); setv(6,4,'DOC_REF'); setv(7,4,'Doc Title')

# ensure extra data rows carry the template merge pattern (C:D, E:I, J:O, Q:R)
for r in range(20, 34):
    if not any(mc.min_row <= r <= mc.max_row and mc.min_col <= 3 for mc in ws.merged_cells.ranges):
        ws.merge_cells(start_row=r, start_column=3, end_row=r, end_column=4)
        ws.merge_cells(start_row=r, start_column=5, end_row=r, end_column=9)
        ws.merge_cells(start_row=r, start_column=10, end_row=r, end_column=15)
        ws.merge_cells(start_row=r, start_column=17, end_row=r, end_column=18)

# fill (write to anchors; merges carry the value)
for idx, c in enumerate(comments):
    r = 11 + idx
    setv(r,1, idx+1); setv(r,2,'CG'); setv(r,3,c['sheet'])
    setv(r,5,c['comment']); setv(r,10,c['reply']); setv(r,16,'Rawasin')
```

## Verification
After saving, re-open and print: (a) all data rows landed (No./Sheet/Comment/Reply), (b) footer rows still show the legend + signature block, (c) `len(ws.merged_cells.ranges)` is sane (template merges + added data rows). Open in Excel/LibreOffice to visually confirm the footer format is intact.

## Comment-source pitfall
The CG comments for BOTH submittal rounds live on the DS submittal cover pages (18 for the 1st Code-B submission, 5 for the 2nd Code-D submission). The `Audit Response.xlsx` sheets are NOT the full comment set — a given sheet may only carry a subset. Read the actual CG response PDF cover pages (from Outlook attachments, e.g. `47953_...1G-0001.pdf`, `49829_...1G-0002.pdf`) for the authoritative comment list, and pair each with its reply from the Audit Response.
