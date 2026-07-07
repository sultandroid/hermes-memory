# MasterFormat BOQ Extraction — NRS XLSX Parsing

## OneDrive Read Issue

When the MasterFormat BOQ `.xlsx` lives on OneDrive (`~/Library/CloudStorage/OneDrive-SAMAYAINVESTMENT/…`):
- `openpyxl` with local copy → **times out** if OneDrive hasn't synced the file locally
- `zipfile.ZipFile(xlsx_path)` → works after OneDrive sync completes
- Tell the user: *"OneDrive sync required — force download"* → retry after confirmation

## Extraction Pattern

XLSX files are ZIP archives. The actual text content lives in `xl/sharedStrings.xml`.

```python
import zipfile, re, os

path = os.path.expanduser("~/path/to/MasterFormat_BOQ.xlsx")
z = zipfile.ZipFile(path)

# 1. Extract all shared strings
ss_content = z.read('xl/sharedStrings.xml').decode('utf-8', errors='ignore')
strings = re.findall(r'<t[^>]*>([^<]+)</t>', ss_content)

# 2. Read each sheet's XML
for name in z.namelist():
    if not name.startswith('xl/worksheets/sheet') or not name.endswith('.xml'):
        continue
    content = z.read(name).decode('utf-8', errors='ignore')
    rows = re.findall(r'<row[^>]*r="(\d+)"[^>]*>(.*?)</row>', content, re.DOTALL)
    
    for row_num, row_xml in rows:
        cells = re.findall(r'<c[^>]*r="([^"]+)"[^>]*>(.*?)</c>', row_xml, re.DOTALL)
        vals = {}
        for cell_ref, cell_xml in cells:
            col = re.match(r'([A-Z]+)', cell_ref).group(1)
            v_match = re.search(r'<v>([^<]+)</v>', cell_xml)
            val = v_match.group(1) if v_match else ''
            t_match = re.search(r'<c[^>]*t="s"[^>]*>', cell_xml)
            if t_match and val:
                idx = int(val)
                val = strings[idx] if idx < len(strings) else f"[{idx}]"
            vals[col] = val
        
        # Now search/process vals dict
z.close()
```

## Column Mapping (NRS MasterFormat BOQ)

From actual data (May 2026 — sheet13, Division 08 Openings):

| Column | Content | Example |
|--------|---------|---------|
| `A` | **Description** (shared string) | "Supply and installation of internal single door 900×2100 mm including frame…" |
| `B` | Reference/price code (integer) | 226 |
| `C` | Unit of measure code (151 = EA) | 151 |
| `D` | **QUANTITY** (integer) | 1, 3, 4, 6 |
| `E` | Subtotal or flag (0 or empty) | 0 |
| `G` | Section reference | 227 |

**Key pattern:** Descriptions are on odd-numbered rows (6, 8, 10, 13, 16, 19). The **quantity is on the NEXT row** (7, 9, 12, 15, 18) in column D.

Example parsed data:
```
Row 6:  A="Supply and install flush wood door as per drawings…"
Row 7:  D=6  (flush wood door QTY)
Row 8:  A="Supply and installation of internal double door 2400×4200 mm…"
Row 9:  D=3  (double door 2400×4200 QTY)
Row 12: D=1  (double door 2400×3700 QTY)
Row 15: D=4  (double door 2000×2700 QTY)
Row 18: D=1  (single door 900×2100 QTY)
```

## Scope Gap Detection

When the BOQ doesn't contain scope items your RFP assumes (e.g., fire-rated metal doors, emergency exits), check:

1. Is the item in a different MASTERFORMAT section? (e.g., 08 11 00 Metal Doors vs 08 14 00 Wood Doors)
2. Is it in the BASE BUILDING contract, not the fit-out scope?
3. Need PMO/Consultant confirmation before including in RFP

## File: `جدول الكميات للبنود التفصيلية المعدل - المتحف الاقليمي.xlsx`

The Arabic detailed BOQ has the same door items but with Arabic descriptions and different column layout. Quantities are embedded in description text rather than clean integer columns — harder to parse programmatically. Use the English MasterFormat BOQ as primary source.
