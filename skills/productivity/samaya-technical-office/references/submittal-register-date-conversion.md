# Submittal Register: Stage-Mask to Date-Based Conversion

## Problem
Registers originally used stage columns (50%, 90%, 100%, IFC) as **applicability indicators** (blank=due at this stage, `—`=N/A). Items filtered into stage-specific sheets. This wasted column real estate — the sheet already filters by stage.

## New Format
Stage columns hold **planned dates** instead of stage markers:
- `50%` column = planned submission date at 50% stage (only shown in 50% sheet, `—` elsewhere)
- `90%` column = planned submission date at 90% stage
- `100%` column = planned submission date at 100% stage
- `IFC/AFC` column = planned submission date at IFC stage
- `—` = N/A at this stage (item doesn't require this stage)

## Column Widths
```
cww = [7, 50, 14, 14, 14, 14, 14, 20, 28]
#      ref  desc   disc 50%  90%  100% IFC  spkg  remarks
```
Stage columns widen from 7 → 14 to fit `dd/mm/yyyy`.

## Item Tuple Format
```python
# Old (mask):
(ref, desc, disc, [1,1,0,0], spkg, rm)

# New (dates):
(ref, desc, disc, ['28/06/2026','28/07/2026','27/08/2026','—'], spkg, rm)
#                      50%          90%         100%       IFC
```

## Staggered Scheduling Pattern
Groups of items are staggered by 7 days per category/floor to give review buffering:

```python
STAGGER_MAP = {
    'Category A': '28/06/2026',
    'Category B': '05/07/2026',   # +7d
    'Category C': '12/07/2026',   # +14d
}
# 90% = +30d from 50%, 100% = +30d from 90%
# IFC = '27/08/2026' (fixed target, 60d from start)
```

## Generation Loop Changes

### Old filtering (mask-based):
```python
pkgs = [('50% Design', p50, lambda m: m[0]==1), ...]
for pn, pc, ff in pkgs:
    ...
    if not ff(mask): continue       # skip if not due at this stage
    vs = [ref, desc, disc,
          '' if mask[0] else '—',   # show blank if due, — if N/A
          '' if mask[1] else '—',
          '' if mask[2] else '—',
          '' if mask[3] else '—',
          spkg, rm]
```

### New filtering (date-based):
```python
stages = [('50% Design', p50, 0), ('90% Design', p90, 1),
          ('100% Design', p100, 2), ('IFC AFC Construction', pifc, 3)]
for pn, pc, si in stages:
    ...
    dt = dates[si]
    if dt == '—': continue          # skip if N/A at this stage
    # Only show THIS stage's date, mask others
    show = ['—','—','—','—']
    show[si] = dates[si]
    vs = [ref, desc, disc, show[0], show[1], show[2], show[3], spkg, rm]
```

## Category Header Filtering (cn dict)
When checking if a category header should appear, use:
```python
if rn in cn:
    grp = [it for it in its
           if int(it[0].split('-')[1]) >= rn
           and int(it[0].split('-')[1]) < (rn + N if rn < M else 100)
           and it[3][si] != '—']    # ← changed from ff(it[3])
```

### 6. No Icons or Emoji in Any Cell
Headers, status indicators, remarks, Legend sheets — all plain text only. Check for Unicode ranges 0x25A0-0x25FF (geometric shapes), 0x2700-0x27BF (dingbats), 0x2600-0x26FF (misc symbols), 0x1F000-0x1FFFF (emoji), 0x2500-0x257F (box drawing), 0x2580-0x259F (block elements). After icon cleanup, run `compile()` on all .py to verify no syntax breakage.

### 7. Data Sourcing Priority
1. Check `24_Subcontractors/{Package}/*` first — actual subcontractor register is authoritative
2. Check `01_Schedule_and_BOQ/` for BOQ-quantified items (FFE, Graphics, Models, Interactives)
3. Check `00_Scope_of_Work_from_04/` for consultant scope docs
4. Only if none exist — generate from generic SOW templates

### 8. Graphics/Model Maker = No Dates
These two registers use blank/em-dash stage markers only (no planned dates). Reason: RFI raised to client for content research/data, no reply received. Legend sheet notes "Dates TBC — RFI raised to client for research/data."

## Pitfalls

### 1. Column cleanup must NOT match "Submittal / Deliverable (per SOW)"
When automatically removing SOW/ER columns from xlsx, the column header "Submittal / Deliverable (per SOW)" contains "SOW" as a substring. Naive matching (`'SOW' in header`) deletes the **description column** instead of only the SOW/ER columns.

**Fix:** Match exact patterns only: `'SOW §'`, `'ER §'`, `'ER §b'`. Never match substring `'SOW'` or `'ER'` alone.

### 2. Regeneration from .py scripts is more reliable than patching .xlsx
Once .xlsx files have columns incorrectly deleted, it's faster to **regenerate from the .py generator scripts** than to try inserting columns and shifting data. The .py scripts are the source of truth.

### 3. Verification after bulk regeneration
After regenerating ALL registers:
```python
for folder, prefix in regs:
    fp = f'{BASE}/{folder}/{folder}.xlsx'
    wb = openpyxl.load_workbook(fp)
    ws = wb['50% Design']
    # Check col 2 = "Submittal / Deliverable"
    hdr2 = str(ws.cell(row=1, column=2).value or '')
    assert 'Submittal' in hdr2, f"Missing description column in {folder}"
    # Check col 4 contains a date
    for r in range(2, ws.max_row+1):
        ref = str(ws.cell(row=r, column=1).value or '')
        if ref.startswith(prefix):
            assert '20' in str(ws.cell(row=r, column=4).value or ''), f"Missing date in {folder}"
            break
    wb.close()
```

### 4. OneDrive-safe file copy for .xlsx
```bash
osascript -e "
tell application \"Finder\"
    set srcFile to POSIX file \"$SRC/file.xlsx\"
    set destFolder to POSIX file \"$BASE/folder/\"
    duplicate srcFile to destFolder with replacing
end tell
"
```
Direct `cp` to OneDrive may produce corrupt placeholders. Always use Finder `duplicate`.

### 5. Filename mismatch between subagent output and folder convention
Subagents may generate files with different naming (e.g., `FitOut_` instead of `Exhibition_FitOut_`, `OddyTesting_` instead of `Oddy_Testing_`). After regeneration, verify each file has the correct name matching its folder.

## Example: Architecture Staggered by Floor
```python
FLOOR_DATES = {
    'Basement Floor':      ['28/06/2026', '28/07/2026', '27/08/2026', '—'],
    'Lower Ground Floor':  ['05/07/2026', '04/08/2026', '03/09/2026', '—'],
    'Ground Floor':        ['12/07/2026', '11/08/2026', '10/09/2026', '—'],
    'First Floor (Structure)': ['19/07/2026', '18/08/2026', '17/09/2026', '—'],
}
```
Each floor has its 16 drawing packages submitted as a batch. 7d buffer between floors for review.
