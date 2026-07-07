# Excel Merge-Safe Row Insertion Pattern

When inserting rows into an Excel sheet that has merged cells, `ws.insert_rows()` corrupts the merge structure and produces `AttributeError: 'MergedCell' object attribute 'value' is read-only` on subsequent writes.

## The Pattern

```python
import openpyxl
from openpyxl.styles import Font, Alignment, PatternFill, Border
from openpyxl.utils import get_column_letter, range_boundaries
from copy import copy

wb = openpyxl.load_workbook('file.xlsx')
ws = wb['SheetName']

# Step 1: Unmerge ALL cells first
original_merges = []
for mc in list(ws.merged_cells.ranges):
    min_col, min_row, max_col, max_row = range_boundaries(str(mc))
    original_merges.append((min_row, max_row, min_col, max_col))
    ws.unmerge_cells(str(mc))

# Step 2: Read all data into memory (values + styles)
all_data = []
for row in ws.iter_rows(min_row=1, max_row=ws.max_row):
    row_data = []
    for cell in row:
        row_data.append({
            'value': cell.value,
            'font': copy(cell.font),
            'fill': copy(cell.fill),
            'alignment': copy(cell.alignment),
            'border': copy(cell.border),
            'number_format': cell.number_format,
        })
    all_data.append(row_data)

# Step 3: Build new rows as list of dicts
new_rows = []
# ... populate new_rows with the same dict structure ...

# Step 4: Insert into all_data at the right position
insert_idx = 73  # 0-based: after row 73, before row 74
all_data = all_data[:insert_idx] + new_rows + all_data[insert_idx:]

# Step 5: Clear the sheet completely
for row in ws.iter_rows(min_row=1, max_row=ws.max_row):
    for cell in row:
        cell.value = None
        cell.font = Font()
        cell.fill = PatternFill()
        cell.alignment = Alignment()
        cell.border = Border()

# Step 6: Write all data back
for i, row_data in enumerate(all_data, start=1):
    for j, cell_data in enumerate(row_data, start=1):
        cell = ws.cell(row=i, column=j)
        cell.value = cell_data.get('value')
        if cell_data.get('font'): cell.font = cell_data['font']
        if cell_data.get('fill'): cell.fill = cell_data['fill']
        if cell_data.get('alignment'): cell.alignment = cell_data['alignment']
        if cell_data.get('border'): cell.border = cell_data['border']
        if cell_data.get('number_format'): cell.number_format = cell_data['number_format']

# Step 7: Re-apply original merged ranges (shifted for rows >= insert point)
for (min_row, max_row, min_col, max_col) in original_merges:
    if min_row >= (insert_idx + 1):
        min_row += len(new_rows)
        max_row += len(new_rows)
    start_cell = f"{get_column_letter(min_col)}{min_row}"
    end_cell = f"{get_column_letter(max_col)}{max_row}"
    ws.merge_cells(f"{start_cell}:{end_cell}")

# Step 8: Apply new merges for any new section headers
# ws.merge_cells(start_row=74, start_column=1, end_row=74, end_column=13)

wb.save('file.xlsx')
```

## Key Points

- **Always unmerge first** — merged cells block writes to all cells except the top-left
- **Store merge definitions** before unmerging so you can re-apply them
- **Shift row numbers** for merges that were below the insertion point
- **Clear the sheet** before writing back to avoid stale data in rows beyond the new total
- **Write styles explicitly** — `copy()` from openpyxl's `copy` module, not Python's built-in
