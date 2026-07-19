# Consolidated Register Audit Workflow

## When to Use

- PM sends an old consolidated Excel with multiple sheets (master, DRR, HSE, AV)
- You need to check if the live register covers all risks from the old file
- User says "audit first and if applicable add"

## Workflow

### Step 1: Read ALL Sheets in the Old File

Don't assume the old file only has master risks. Read every sheet:

```python
import openpyxl
wb = openpyxl.load_workbook('old_file.xlsx')
print(wb.sheetnames)
```

Common sheets in consolidated registers:
- Master Risk Register (33-49 risks, PxS 1-4)
- Designer Risk Register / DRR (79 risks, PxI 1-5)
- HSE Risk Register (41 task-level controls, CxL 1-5)
- DRR Status Audit (evidence review)
- DRR Duplicate Check (overlap analysis)
- HSE Out-of-Scope Log (excluded items)

### Step 2: Audit Master Risks First

Read ALL master risk IDs + event descriptions from the old file. Read ALL from the live register. Create a side-by-side mapping:

| Old ID | Old Risk Event | Live ID | Status |
|--------|---------------|---------|--------|
| PRR-COM-01 | Scope changes post-award | PRR-COM-01 | ✅ Covered |
| PRR-SCH-02 | AV procurement delays | PRR-AV-02 | ❌ Missing → add |

**Key rules:**
- Same ID does NOT mean same risk — read the event descriptions side by side
- A risk may have been renumbered (e.g. PRR-SCH-01 → PRR-PRC-02) or recategorised
- A risk may have been split into multiple risks (e.g. one fire risk → FLS-01 + FLS-02)
- Report gaps as a table with proposed new ID and severity

### Step 3: Add Missing Master Risks

For each confirmed gap:
1. Score per RMP scale (PxS 1-4 for PRR)
2. Assign next available ID in the category (e.g. PRR-AV-02 if PRR-AV-01 exists)
3. Add to xlsx Risk Register sheet (append at end)
4. Update Cover (totals), Dashboard (counts), RBS (category counts), Register Control (revision history)
5. Add to repo markdown (`01_Registers/risk_register.md`)
6. Create treatment file if Critical (≥12)

### Step 4: Decide on DRR/HSE/AV Sheets

**Do NOT merge DRR or HSE risks into the master register.** They use different scoring scales:

| Register | Scale | Range | Severity Bands |
|----------|:-----:|:-----:|----------------|
| Master (PRR) | PxS 1-4 | 1-16 | Critical ≥12, High 8-11, Medium 4-7, Low ≤3 |
| Design (DRR) | PxI 1-5 | 1-25 | Critical ≥20, High 12-19, Medium 8-11, Low 4-7, Very Low 1-3 |
| HSE | CxL 1-5 | 1-25 | Critical 16-25, High 10-15, Medium 5-9, Low 1-4 |

Mixing them in one sheet with a Type column would break severity band interpretation.

**Options:**
- **Separate sheets in the same xlsx** (recommended) — each sheet keeps its own scoring header and column layout
- **Separate files** — DRR lives in repo, HSE in HSE plan

### Step 5: Copy DRR/HSE Sheets into the Live xlsx — Exclude Internal Working Sheets

When copying sheets from the old consolidated register, **remove internal working sheets** (Status Audit, Duplicate Check, Overlap Analysis). These are one-time analysis tools, not part of the formal register. Keep only the main data sheets.

```python
from copy import copy

src = openpyxl.load_workbook('old_file.xlsx')
dst = openpyxl.load_workbook('live_file.xlsx')

# Only copy the main data sheets — NOT internal working sheets
sheets_to_copy = [
    'Designer Risk Register (DRR)',
    'HSE Risk Register (Fit-Out)',
]

for sheet_name in sheets_to_copy:
    ws_src = src[sheet_name]
    ws_dst = dst.create_sheet(title=sheet_name)
    
    # Copy all cells with formatting
    for row in ws_src.iter_rows(min_row=1, max_row=ws_src.max_row, max_col=ws_src.max_column):
        for cell in row:
            new_cell = ws_dst.cell(row=cell.row, column=cell.column, value=cell.value)
            if cell.has_style:
                new_cell.font = copy(cell.font)
                new_cell.border = copy(cell.border)
                new_cell.fill = copy(cell.fill)
                new_cell.number_format = copy(cell.number_format)
                new_cell.protection = copy(cell.protection)
                new_cell.alignment = copy(cell.alignment)
    
    # Copy merged cells
    for merged_range in ws_src.merged_cells.ranges:
        ws_dst.merge_cells(str(merged_range))
    
    # Copy column widths
    for col_idx, col_dim in enumerate(ws_src.column_dimensions.values(), 1):
        if col_dim.width:
            ws_dst.column_dimensions[openpyxl.utils.get_column_letter(col_idx)].width = col_dim.width
    
    # Copy row heights
    for row_idx, row_dim in enumerate(ws_src.row_dimensions.values(), 1):
        if row_dim.height:
            ws_dst.row_dimensions[row_idx].height = row_dim.height

# Remove any duplicate sheets that may have been created
for sheet in list(dst.sheetnames):
    if sheet.endswith('1') and sheet[:-1] in dst.sheetnames:
        del dst[sheet]

# Reorder sheets — DRR and HSE after the PRR sheets
desired_order = ['Cover', 'Dashboard', 'Risk Register', 'RBS', 'Scoring Matrix', 'Register Control',
                 'Designer Risk Register (DRR)', 'HSE Risk Register (Fit-Out)']

for i, name in enumerate(desired_order):
    if name in dst.sheetnames:
        idx = dst.sheetnames.index(name)
        if idx != i:
            dst.move_sheet(name, offset=i - idx)

dst.save('live_file.xlsx')
```

### Step 6: Update All Counts

After adding master risks AND copying DRR/HSE sheets:

| Location | What to Update |
|----------|---------------|
| Cover sheet | Total risks, Open count, Medium count |
| Dashboard | Medium count, category counts (AV, PRC, etc.) |
| RBS sheet | Category counts |
| Register Control | Add revision entry |
| Repo markdown | Snapshot table, RBS table, new risk rows |

### Pitfalls

- **ID collision is the most common bug** — read risk event/cause side by side, not just IDs
- **Copying sheets with merged cells** — openpyxl's `copy()` doesn't copy merged cell ranges. You must explicitly iterate `ws_src.merged_cells.ranges` and re-merge in the destination
- **Column widths don't auto-copy** — iterate `column_dimensions` explicitly
- **Row heights don't auto-copy** — iterate `row_dimensions` explicitly
- **Sheet reorder uses `move_sheet(name, offset=N)`** — offset is relative to current position, not absolute. Calculate `i - idx` where `i` is desired index and `idx` is current index
- **The old file may have duplicate or mislabeled sheets** — e.g. "AV Risk Register" sheet that is actually a duplicate of the HSE sheet. Verify content before copying
