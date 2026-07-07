# Schedule Excel Extraction Pattern

When material schedule data comes from Excel files, the naive extraction (just reading all columns) misses schedule-specific fields like Graphic Type, Substrate, Print Method.

## Extraction Process

### 1. Identify Source File

Find the correct schedule Excel file:
```bash
find "/path/to/project" -iname "*graphic*" -name "*.xls*" 2>/dev/null
```

### 2. Read Column Headers

Use openpyxl to find the header row (not always row 1):
```python
import openpyxl
wb = openpyxl.load_workbook(filepath)
ws = wb.active
for row in range(1, 10):
    vals = [ws.cell(r, c).value for c in range(1, ws.max_column + 1)]
    if any(v and 'Code' in str(v) or 'Graphic ID' in str(v) for v in vals):
        print(f"Header at row {row}: {vals}")
        break
```

### 3. Extract All Fields as JSON

```python
header_row = 5  # As discovered above
data_start = header_row + 1

records = []
for r in range(data_start, ws.max_row + 1):
    row_vals = {}
    for c in range(1, ws.max_column + 1):
        header = ws.cell(header_row, c).value
        val = ws.cell(r, c).value
        if header and val is not None:
            key = header.strip().replace(' ', '_').lower()
            row_vals[key] = val
    if row_vals.get('graphic_id') or row_vals.get('code'):
        # Normalize the code field name
        records.append(row_vals)

import json
with open('extracted.json', 'w') as f:
    json.dump(records, f, indent=2)
```

### 4. Merge into Existing Schedule JSON

Match extracted records to existing schedule items by code. Add new fields to the item dict:

```python
with open('schedule_json_file') as f:
    schedule = json.load(f)

with open('extracted.json') as f:
    extracted = json.load(f)

extracted_map = {}
for item in extracted:
    code = item.get('graphic_id', '').strip() or item.get('code', '').strip()
    if code:
        extracted_map[code] = item

field_map = {
    'graphic_type': 'Graphic Type',  # key in schedule_item ← header in Excel
    'substrate': 'Substrate',
    'substrate_details': 'Substrate Details',
    'print_method': 'Print Method',
}

for item in schedule:
    code = item['code']
    if code in extracted_map:
        for sched_field, excel_key in field_map.items():
            item[sched_field] = extracted[code].get(excel_key, '') or ''
    else:
        for sched_field in field_map:
            item.setdefault(sched_field, '')

# Also update materials.json for items with matching schedule_key
with open('materials_json') as f:
    all_mats = json.load(f)

for mat in all_mats:
    if mat.get('schedule_key') == correct_key:
        code = mat.get('code', '')
        if code in extracted_map:
            for sched_field in field_map:
                mat[sched_field] = extracted[code].get(sched_field, '') or ''
        else:
            for sched_field in field_map:
                mat.setdefault(sched_field, '')
```

### 5. Known Fields by Schedule

| Schedule | Extra Fields | Excel Column (Row 5 header) | Sample |
|----------|-------------|---------------------------|--------|
| Graphic | `graphic_type` | Graphic Type | "Single Object Label", "Infographic F7" |
| Graphic | `substrate` | Substrate (Excel typo: "Susbtrate") | "Acrylic Lightbox", "Setworks" |
| Graphic | `substrate_details` | Substrate Details | "Brass" (only value) |
| Graphic | `print_method` | Print Method | "Direct to media", "UV Direct to media" |

### 6. TypeScript Type Update

After adding new fields, update three places:
- `materialStore.ts` → `Material` interface
- `Gallery.tsx` → tooltip data type in `useState<{...}>`
- `Schedule.tsx` → `columns` array

The tooltip data type should match the Material interface fields. If they diverge, tooltip cards won't show the new data.
