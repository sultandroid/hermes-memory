# AV Cable Schedule — Fast RFI Answer Pattern

## Problem

Need to locate AV headend/control room but MEP DWG files require AutoCAD. PDF design documents don't label rooms.

## Solution

The AV cable schedule XLSX (`RCRC_CABLE_*.xlsx` under `AV EXCEL FILES/`) contains a `From` column revealing the headend location.

## Proven Discovery (RCRC Exhibition, 2026-06-26)

```python
import openpyxl
wb = openpyxl.load_workbook("RCRC_CABLE_19.12.25 rev0.xlsx", data_only=True)
ws = wb.active

from_locations = set()
for row in ws.iter_rows(min_row=6, values_only=True):
    if row[6]:  # Column G = "From"
        from_locations.add(str(row[6]).strip())

print(from_locations)  # → {'Rackroom'}
```

Result: All 7 galleries connect to "Rackroom" — this IS the AV headend.

## Cross-Reference Sources

| Source | Reveals |
|--------|---------|
| `RCRC_CABLE_*.xlsx` | From/To locations, cable lengths, cable types |
| `RCRC H&P_*.xlsx` | Heat & Power — electrical load per gallery |
| `RCRC SPECS_*.xlsx` | Equipment model numbers, quantities |
| `RCRC BOQ_*.xlsx` | Cost/quantity (exclude from technical proposals) |

## Workflow

1. Read cable schedule first — fastest path to headend location
2. Cross-reference H&P for electrical capacity
3. If MEP DWG exists, locate "Rackroom" label on floor plans
4. Update RFI-03 with confirmed headend name and cable topology