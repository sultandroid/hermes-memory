# Excel Schedule Extraction — Full Column Preservation

Extract all rows from Excel schedule files while preserving every original column, without mapping to a reduced schema.

## When to Use

Multiple Excel files each with different column structures (e.g. museum exhibit schedules), and you need all columns available in the app's data layer.

## Pattern

### 1. Auto-detect header row

Schedules have title rows (1-4), then a header row, then data. Detect the header by scanning rows for known column names:

```python
import openpyxl

HEADER_KEYWORDS = {'Code', 'ID', 'Name', 'Description', 'Type', 'Qty', 'Finish'}

wb = openpyxl.load_workbook(filepath, read_only=True, data_only=True)
ws = wb.active

header_row = None
for row_idx, row in enumerate(ws.iter_rows(values_only=True), 1):
    non_null = [c for c in row if c is not None]
    # A header row has 3+ populated cells and at least one known keyword
    if len(non_null) >= 3 and any(
        any(kw.lower() in str(c).lower() for kw in HEADER_KEYWORDS)
        for c in non_null
    ):
        header_row = row
        header_row_num = row_idx
        break

if header_row is None:
    raise ValueError(f'Could not detect header in {filepath}')
```

### 2. Read column names

```python
columns = [str(c).strip() if c else f'Col_{i}' for i, c in enumerate(header_row)]
```

### 3. Extract data rows

```python
rows = []
for row in ws.iter_rows(min_row=header_row_num + 1, values_only=True):
    non_null = [c for c in row if c is not None and str(c).strip() != '']
    # Skip empty rows and section-header-only rows (<2 data cols)
    if len(non_null) < 2:
        continue
    item = {}
    for i, val in enumerate(row):
        if i < len(columns):
            if isinstance(val, str):
                val = val.strip()
            item[columns[i]] = str(val) if val is not None else ''
    rows.append(item)
```

### 4. Handle multi-sheet files

```python
all_rows = []
for sheet_name in wb.sheetnames:
    ws = wb[sheet_name]
    # same detection + extraction as above
    for item in sheet_rows:
        item['_source_sheet'] = sheet_name
    all_rows.extend(sheet_rows)
```

### 5. Merge into unified JSON

When combining multiple schedule types into one `materials.json`, preserve ALL fields per item but add `schedule_key` and `source` for filtering:

```python
# Each item has ALL its original columns
{
  "code": "AX_CA.01_GR_01",
  "Graphic Type": "Special: Cafe Backlit Imagery",
  "Description": "Section E: Back-lit Image",
  "Substrate": "Acrylic Lightbox",
  "Print Method": "DTM Duratran translucent film",
  "Height (mm)": "1812",
  "Width (mm)": "5060",
  "Qty": "1",
  "schedule_key": "graphic_schedule",
  "source": "Graphic Schedule"
}
```

### 6. Normalize field names for app code

If the app expects standard fields (`code`, `description`, `finish` instead of `Code`, `Description`, `Finish`), normalize after merge:

```python
FIELD_MAP = {
    'Code': 'code', 'Description': 'description', 'Category': 'category',
    'Element': 'element', 'Finish': 'finish', 'Colour': 'colour',
    'Supplier': 'supplier', 'QTY': 'qty', 'Qty': 'qty',
}

for mat in all_materials:
    for old_key, new_key in FIELD_MAP.items():
        if old_key in mat:
            mat[new_key] = mat.pop(old_key)
```

### 7. Handle deduplication

Same code may appear in multiple schedule files (e.g. a code with `_SW_` prefix in the Graphic file). Assign schedule from code prefix, keep the first occurrence:

```python
PREFIX_SCHEDULE = [
    (r'[0-9.]+_SW_', 'setwork_schedule', 'Setwork Schedule'),
    (r'[0-9.]+_GR_', 'graphic_schedule', 'Graphic Schedule'),
    # ...
]

for item in extracted_rows:
    code = item['code']
    if code not in seen_codes:
        seen_codes[code] = item
        # Assign schedule from code prefix
        for pattern, sched_key, source in PREFIX_SCHEDULE:
            if re.search(pattern, code):
                item['schedule_key'] = sched_key
                item['source'] = source
                break
```

## Pitfalls

- **Section-header rows interspersed with data**: Some schedules group items under category headers (e.g. "Floor Finishes", "Wall Finishes"). These rows look like data (one populated cell) but aren't. Filter by requiring ≥2 non-null columns.
- **`#VALUE!` cells**: Excel formula errors appear as `#VALUE!` in `data_only=True` mode. Preserve them as-is or strip.
- **Multi-sheet files**: One file may have 9 gallery sheets. Process all sheets and merge.
- **Duplicate codes across files**: Same code in different files means different data. Keep the one matching the code's schedule prefix.
- **Spelling errors in headers**: "Susbtrate" should map to "substrate". Handle with FIELD_MAP or case-insensitive matching.
- **Zero data rows**: Some schedule files are templates with headers but no data (e.g. Asset Schedule). Handle gracefully.
- **IDs have different field names per schedule type**: Art Commission ID, Showcase ID, Setwork ID, Graphic ID, etc. Build a list of known ID fields to detect the `code` field.
