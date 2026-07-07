# Aseer Museum — Subcontractor RFI Register Layout

**File:** `Docs/09_Registers/28_Subcontractor_RFI_Register/Live Register Log.xlsb`
**Format:** XLSB (binary Excel) — use pyxlsb, NOT openpyxl
**Purpose:** Track all subcontractor RFIs across disciplines (Showcase, MEP, General, Architectural, Structural)

## Sheet Structure

| Sheet Name | Purpose |
|---|---|
| `Cover` | Dashboard — open/closed/rejected summary, status colour key |
| `Dashboard` | Potentially consolidated view |
| `RFI` | **Primary data sheet** — all 24+ RFI entries |
| `Material Submittal` | Separate material tracking |
| (other sheets) | Various tracking views |

## RFI Sheet Layout (0-indexed)

| Row Range | Content |
|---|---|
| 0 | Empty/logo |
| 1 | Title "Subcontractor's RFI Register" |
| 2–7 | Status code definitions (e.g., `A = Open`, `B = Closed`, `C = Rejected`) |
| 8–10 | Column headers split across 3 rows (merged cells) |
| **11+** | **Data rows start** — one RFI per row |

## Column Mapping (RFI sheet, row 11+)

Approximate column indices (always verify by reading headers at rows 8-10 first):

| Col | Content | Notes |
|---|---|---|
| 0 | RFI Ref # | e.g. `ARM-RFI-GN-007` |
| 1 | Date Raised | Excel serial date |
| 2 | RFI Description / Subject | Free text, may contain Arabic |
| 3 | Originator / Discipline | |
| 4 | Contractor | |
| 5 | Status | A=Open, B=Closed, C=Rejected |
| 6 | Response / Date Closed | Excel serial date when closed |
| 7 | Days Open | Integer (computed?) |
| 8–11 | Additional metadata | Remarks, attachments, etc. |

## Known Data Profile (as of June 2026)

- **24 total RFIs**: 20 Closed, 4 Open, 1 Rejected (some of 20 may include the 1 rejected)
- **4 open RFIs** — all aging 98–153 days
- **Showcase RFIs**: 9 total (7 Closed, 2 Open) — identified by subject containing keywords like "Showcase", "Object List", "Patinated Brass", "Finishes", "Cladding"

## Reading Pattern (Python)

```python
from pyxlsb import open_workbook
from datetime import datetime, timedelta

path = "Docs/09_Registers/28_Subcontractor_RFI_Register/Live Register Log.xlsb"
rows = []

with open_workbook(path) as wb:
    with wb.get_sheet('RFI') as sheet:
        for i, row in enumerate(sheet.rows()):
            if i < 11:  # skip header/legend rows
                continue
            vals = [cell.v for cell in row]
            if not vals or not vals[0]:  # skip empty rows
                continue
            rows.append({
                'ref': vals[0] or '-',
                'date_raised': (datetime(1899, 12, 30) + timedelta(days=vals[1])) if isinstance(vals[1], (int, float)) else None,
                'subject': vals[2] or '-',
                'status_code': vals[5] or '-',
                'days_open': vals[7] if isinstance(vals[7], (int, float)) else 0,
            })

# Status: A=Open, B=Closed, C=Rejected
opens = [r for r in rows if r['status_code'] == 'A']
```

## Filtering for Showcase Items

Showcase RFIs contain subject keywords specific to the showcase contractor's scope:
- `Showcase`
- `Object List` / `Object`
- `Patinated Brass` / `Brass`
- `Finishes` (e.g. `Bronze Finishes`, `Patinated`)
- `Cladding` / `Panel`
- `Louvre` / `Louvre Frame`

Not all open RFIs are showcase-related — always filter explicitly.
