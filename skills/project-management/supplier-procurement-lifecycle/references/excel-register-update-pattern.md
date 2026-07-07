# Excel Register Update Pattern

When updating a structured project register xlsx (Key Personnel Register, Subcontractor Register, etc.) with new rows:

## OpenPyXL Workflow

```python
import openpyxl
from copy import copy

wb = openpyxl.load_workbook('path/to/register.xlsx')
ws = wb['SheetName']

# 1. Check for merged cells first
print(list(ws.merged_cells.ranges))

# 2. Insert rows at specific position
ws.insert_rows(row_num)  # shifts existing rows down

# 3. Populate cells
for c, v in enumerate(values, 1):
    cell = ws.cell(row=row_num, column=c, value=v)
    # Copy style from adjacent row
    src = ws.cell(row=row_num-1, column=c)
    if src.has_style:
        cell.font = copy(src.font)
        cell.fill = copy(src.fill)
        cell.border = copy(src.border)
        cell.alignment = copy(src.alignment)

# 4. Update summary/cover sheets
ws_cover.cell(row_num, col_num, 'Rev C03')
ws_summary.cell(row_num, col_num, new_count)

# 5. Save
wb.save('path/to/register.xlsx')
```

## Best Practices

- Back up the file first: `cp file.xlsx file.xlsx.bak`
- Check for merged cells before inserting — they break `insert_rows`
- Copy styles from adjacent rows — preserves formatting
- Update ALL dependent values: revision, date, total counts, tier counts, status counts
- Verify after save by re-reading the new rows
