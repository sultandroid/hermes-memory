# Register Log Verification (xlsb)

## When to Use

When you need to verify the actual CG approval status of a document for updating disposition tables, related documents lists, or status reports. The project's `Register Log.xlsb` is the authoritative source — CG_STATUS.md sidecars can be stale or incorrect.

## How to Read

Use `pyxlsb` (available in the environment):

```python
from pyxlsb import open_workbook
from datetime import datetime, timedelta

def excel_to_date(serial):
    if not serial or serial == 0:
        return ""
    base = datetime(1899, 12, 30)
    return (base + timedelta(days=float(serial))).strftime("%d-%b-%Y")

path = "/path/to/Register Log.xlsb"
wb = open_workbook(path)
print("Sheets:", wb.sheets)
```

## Key Sheets

| Sheet | Content |
|-------|---------|
| `Document Submittals` | Management plans (PL-XXXX) with full submission history per round |
| `19. Document Anaysis` | Summary report — counts of A/B/C/D per document type |
| Each type sheet | Detailed logs for specific deliverable types |

## Document Submittals Sheet Structure

Headers: `Sl.No. | Document Number | Discipline | Description | TYPE | ...`

For each document, the register tracks multiple submission rounds (R0, R1, R2, R3) with:
- **Date Received** (Excel serial — convert with function above)
- **Date Reply** (Excel serial — when CG responded)
- **Status** (A=Approved, B=Approved as Noted, C=Revise & Resubmit, D=Under Review, E=Rejected)
- **Days** (turnaround time)

The **last non-empty status** in the row is the Current Status. R0 status is in columns 8-10, R1 in 11-14, R2 in 16-18, etc.

## Verification Workflow

1. Open `Register Log.xlsb` with pyxlsb
2. Navigate to `Document Submittals` sheet
3. Search for the document number (e.g., PL-0029, PL-0010)
4. Find the **latest non-empty status** — that's the current CG approval status
5. Compare against what the CRP or CG_STATUS.md says — if different, the register wins

## Document Code Prefixes

| Prefix | Meaning |
|--------|---------|
| MOC-MUS-ASE-1K0-PL- | Multi-discipline project plans |
| MOC-ASEER-SIC-1K0-PL- | Samaya internal plans |
| MOC-ASEER-SIC-1KH-PL- | HSE plans |
| MOC-ASEER-SIC-1A0-ZD- | Architecture-led design docs/methodology |
| MOC-ASEER-SIC-0Q0-PL- | Quality plans |
| MOC-MUS-ASE-1M0-PL- | MEP plans |
