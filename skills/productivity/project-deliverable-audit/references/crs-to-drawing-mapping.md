# CRS-to-Drawing Mapping — CG Review Code Extraction

Extract CG review codes (B/C/U.R) from Excel CRS (Comments Resolution Sheet) files and map them to individual drawings in a register.

## Trigger
- CG returns a CRS Excel file with per-drawing review codes
- You need to update a drawing register with actual CG status per sheet

## Workflow

### Step 1 — Extract CRS Data

```python
import openpyxl
wb = openpyxl.load_workbook('CRS_FILE.xlsx', data_only=True)
ws = wb['CRS']  # Sheet name is typically 'CRS'

# CRS header structure (varies by project):
# Row 1-6: Project info, CRS number, document reference
# Row 7: Column headers (No. | Initial | Sheet | Reviewer Comment | Code | ...)
# Row 8+: Drawing entries

# Key columns to extract:
# Column C (index 2) = Sheet/Drawing reference
# Column D (index 3) = Reviewer Comment
# Column E (index 4) = Code (B/C/U.R/-)
# Column B (index 1) = Reviewer name/initials
```

### Step 2 — Build Code Dictionary

```python
crs_codes = {}
for row in ws.iter_rows(min_row=8, max_row=ws.max_row, values_only=True):
    drg_no = str(row[2]).strip() if row[2] else ''
    code = str(row[4]).strip() if row[4] else ''
    reviewer = str(row[1]).strip() if row[1] else ''
    crs_date = '2026-07-02'  # from CRS header
    
    if drg_no and drg_no != 'None' and drg_no != 'Gen':
        crs_codes[drg_no] = (code, reviewer, crs_date)
```

### Step 3 — Handle General Comments

CRS files often have "Gen" (General) comments that apply to all drawings in the package. These are not mapped to individual sheets but should be noted in the register header.

### Step 4 — Handle Range Entries

Some CRS entries cover a range of drawings (e.g., "MOC-ASE-AR-ARC-GEN-DDD-2550→2559"). Expand these:

```python
import re
range_match = re.match(r'(.+DDD-)(\d+)→(\d+)', drg_no)
if range_match:
    prefix = range_match.group(1)
    start, end = int(range_match.group(2)), int(range_match.group(3))
    for n in range(start, end + 1):
        crs_codes[f'{prefix}{n}'] = (code, reviewer, crs_date)
```

### Step 5 — Map to Drawing Register

When creating a markdown register from an NRS Excel source:

```python
for row in ws_nrs.iter_rows(min_row=8, max_row=ws_nrs.max_row, values_only=True):
    drg_no = str(row[1]).strip()
    code, reviewer, crs_date = crs_codes.get(drg_no, ('—', '—', '—'))
    # Write row with CG status columns
```

### Step 6 — Generate Summary Table

```markdown
| Floor | DD Gate | CRS Rev | CRS Date | B | C | U.R | — | Total | Status |
|-------|---------|:-------:|:--------:|:-:|:-:|:---:|:--:|:-----:|--------|
| Basement | 1G-0001 | 00 | 2026-06-30 | 10 | 5 | 36 | 0 | 51 | **Mixed** |
```

## Pitfalls

- **CRS "Gen" rows have no drawing number** — they're general comments, not per-sheet codes. Don't map them to individual drawings.
- **Setwork/Showcase details may be U.R (Under Review)** — excluded from the review cycle. These are not Code C, they're deferred.
- **CRS may have mixed codes per package** — some sheets B, some C, some U.R. Don't label the whole package as one code.
- **CRS date ≠ CG signature date** — the CRS may be dated earlier than the reviewer's signature. Use the CRS date for the register, note signature date separately.
- **Reviewer names may be initials or full names** — normalize to full name where possible.
- **Some CRS entries have no reviewer** (e.g., U.R items) — leave reviewer as "—".
- **The same drawing number may appear in multiple CRS files** (different floors, different DD gates) — the latest CRS overrides.
