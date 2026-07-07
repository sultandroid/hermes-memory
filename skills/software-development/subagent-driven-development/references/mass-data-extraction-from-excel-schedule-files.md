# Mass Data Extraction from Excel Schedule Files

Extracting material/object/asset data from 17+ Excel schedule files for museum/exhibition projects.

## The Challenge

Museum projects produce dozens of Excel schedule files (Finishes, Setwork, Showcase, Graphic, Object, Asset, FF&E, Exhibit, Media, Model, Wayfinding, Art Commission, etc.) each with:
- Different column structures (headers vary by file type)
- Title rows before actual headers (rows 1–4 are project info)
- Gallery/section header rows interspersed with data
- Inconsistent code formats (dots vs underscores)

## Extraction Strategy

### 1. Auto-detect Header Row

Scan the first ~20 rows for header-like keywords rather than assuming row 1:

```python
KEYWORDS = ['id', 'code', 'ref', 'item', 'description', 'name', 'title', 
            'type', 'category', 'finish', 'colour', 'supplier', 'element']

def find_header_row(ws, max_scan=20):
    for ri, row in enumerate(ws.iter_rows(min_row=1, max_row=max_scan, values_only=True), start=1):
        vals = [str(v or '').strip().lower() for v in row]
        matches = sum(1 for v in vals if any(kw in v for kw in KEYWORDS))
        if matches >= 3:
            return ri, row
    return None, []
```

### 2. Column Matching (Fuzzy)

Map columns by header substring, not exact match:

```python
def find_col(names):
    for i, h in enumerate(headers):
        hl = h.lower()
        for n in names:
            if n in hl:
                return i
    return None

code_col = find_col(['id', 'code', 'ref', 'setwork id', 'object no'])
desc_col = find_col(['description', 'title', 'name', 'exhibit name'])
cat_col = find_col(['type', 'category', 'group'])
```

### 3. Skip Non-Data Rows

Filter out section headers, empty rows, and metadata:

```python
if not code or re.match(r'^(NA|N/A|none|total|Object Schedule|Setworks Schedule)$', code, re.I):
    continue
if len(code) < 3 or code.isdigit():
    continue
if re.match(r'^[A-Z]\d+\s*[-–]\s*', code) and code.count(' ') >= 2:
    continue  # gallery section headers like "G1 - Welcome Gallery"
```

### 4. Merge Strategy

When combining data from Excel with existing materials.json:

1. Start with existing materials (preserves hand-curated descriptions)
2. Override empty fields with Excel data (fill missing descriptions, finishes, suppliers)
3. Add entirely new codes from Excel
4. Deduplicate by code, keeping richer entries

```python
for code in all_new:
    if code not in existing_codes:
        merged.append({...from excel...})
```

## Full Pipeline (17 Files ~ 1200 Records)

```bash
for f in *.xlsx; do
    python3 extract.py "$f"
done
```

After extraction: merge, sort by category, write to materials.json, rebuild.

## Pitfalls

- **Read-only mode**: Use `data_only=True, read_only=True` for large workbooks (prevents OOM)
- **Header row not at row 1**: Always skip the first 4–5 title rows
- **Gallery headers**: Files like Object Schedule intersperse gallery names as bold rows — detect and skip them
- **Code format variation**: `01_SW_01` vs `04.03_SW_04` vs `G1_OB_001` — all valid, just pass through
- **Merged cells**: OpenPyXL returns the first non-empty value; text duplication is common across merged regions — deduplicate by code
- **Never fabricate**: If the Excel has no `finish` column, leave the field empty — don't derive from other columns or guess

## 🔴 Critical: Verify Data Integrity After Subagent Merge

When a subagent is tasked with **rebuilding or appending** to `materials.json` (e.g., adding AV equipment or lighting schedule data), the subagent's merge script can **corrupt existing data** by overwriting `schedule_key`, `code`, or `source` values for all previously-extracted materials.

**Signal:** User reports "info card changed" or "known materials missing" after a subagent task completes.

**Rule — ALWAYS verify after subagent merge:**

1. **Backup `materials.json` BEFORE delegating** — copy to `/tmp/materials_backup.json`
2. **After subagent completes, verify known codes exist:**
   ```bash
   python3 -c "
   import json
   with open('src/data/materials.json') as f:
       mats = json.load(f)
   from collections import Counter
   sched = Counter(m.get('schedule_key','?') for m in mats)
   for k, v in sorted(sched.items()):
       print(f'{k}: {v}')
   # Check at least ONE known code from each expected schedule
   for code in ['04.04_SW_01', 'FI_FL_01', 'FI_WA_03']:
       matches = [m for m in mats if m.get('code') == code]
       print(f'{code}: {matches[0].get(\"schedule_key\",\"NOT FOUND\") if matches else \"NOT FOUND\"}')"
   ```
3. **Restore from backup if corrupted** — restore `/tmp/materials_backup.json`, then manually append new items by code (skip duplicates).
4. **Never let a subagent overwrite `materials.json` wholesale** — instruct them to only APPEND new items, never replace the file.

## Extracting From Non-Excel Sources (PDF, .md)

Some schedule data exists only as PDF or Markdown files (e.g., Lighting Fixture Schedule SC_01, Luminaire Specifications). Extraction strategy:

1. **Try `.md` first** — if both `.md` and `.pdf` exist, the `.md` is often a Markdown export with extractable tables
2. **Use `pdftotext`** for PDF extraction — preserves layout with `-layout` flag:
   ```bash
   pdftotext -layout "ZNA3297_ARM_SC_01 R3.pdf" /tmp/sc01.txt
   ```
3. **Parse structured text** — look for repeating field patterns (Fixture ID, Type, Description, Wattage, etc.) using regex
4. **Cross-reference multiple files** — the fixture schedule (SC_01) has items, the spec (SP_01) has technical details, the control zones (SC_02) has dimming info. Merge by fixture code.
5. **Manual cleanup** — PDF-extracted text often has line-break artifacts, merged columns, and alignment issues. Write a Python normalization script rather than hand-editing.

### Lighting Fixture Schedule Fields (Example)

| Extracted Field | Example Value |
|----------------|---------------|
| Fixture Code | SP1 |
| Type | Spotlight |
| Description | Track-mounted adjustable spotlight |
| Manufacturer | iGuzzini |
| Lamp Type | LED |
| Wattage | 35W |
| Voltage | 220-240V |
| CRI | >90 |
| CCT | 3000K |
| Lumens | 2800 lm |
| Dimming | DALI |
| Control Zone | Zone A1 |
| Room/Zone | G4 – Saudi Art Gallery |
| Floor | GF |
| Mounting | Track |
| Quantity | 12 |

### AV Equipment Schedule Fields (Example)

| Extracted Field | Example Value |
|----------------|---------------|
| Code | AV_001 |
| Ref | 09_1 |
| Description | AUDIO / Passive Speaker / Flush Mount Ceiling |
| Product | Yamaha VXC6 |
| Qty | 6 |
| Zone | 01.02_AV_01 - Welcome Gallery |
| Category | Audio |
| Dimensions | 286 x 186 mm |
| Power | 50W |
| Voltage | 100V |

## Field Name Normalization
## Field Name Normalization

Different schedule files use different column names for the same concept. Map them to canonical field names during merge:

### ID Field Names Per Schedule Type

| Schedule File | ID Column Name | 
|---------------|----------------|
| Finishes | `Material ID` |
| Setwork | `Setwork ID` |
| Showcase | `Showcase ID` |
| Object | `Object ID` |
| Graphic | `Graphic ID` |
| Wayfinding | `Wayfinding ID` |
| Media | `Media ID` |
| FF&E | `FF&E ID` |
| Tactile | `Tactile / Manual Interactive ID` or `Tactile/Manual ID` |
| Model | `Model/Replica ID` |
| Exhibit | `Exhibit ID` |
| Art Commission | `Art Commission ID` |
| Space | `Space ID` |
| Asset | `Asset ID` |
| Mockups | `Mockup code` or `#` |

### Common Cross-Schedule Mappings

```python
FIELD_MAP = {
    'Material ID': 'code',
    'Treatment/Finish': 'finish',
    'Susbtrate': 'substrate',          # Excel typo preserved from original .xlsx
    'Description': 'description',
    'Colour': 'colour',
    'Supplier': 'supplier',
    'QTY': 'qty',
    'Unit': 'unit',
}
```

### Merge Dedup Rule

When the same code appears in multiple schedule files (e.g., a `_SW_` code found in both setwork and graphic files), use the **code prefix to determine the correct schedule**:

```python
PREFIX_SCHEDULE = [
    (r'_SW_', 'setwork_schedule', 'Setwork Schedule'),
    (r'_SC_', 'showcase_schedule', 'Showcase Schedule'),
    (r'_GR_', 'graphic_schedule', 'Graphic Schedule'),
    # ... etc
]
```

If the detected schedule doesn't match the file the data came from, **clear description/category/element** — those fields from the wrong file are unreliable. Keep finish/colour/supplier as they're often cross-schedule.

## Presentation Card Field Group Design

After extraction and normalization, design the tooltip card field groups per schedule type. Follow the curation rules in `references/interactive-hotspot-patterns.md` under *Presentation-Stage Curation Rules*.
