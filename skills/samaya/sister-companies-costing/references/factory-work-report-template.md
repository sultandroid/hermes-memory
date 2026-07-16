# Factory Work Report Template

Each project gets a `Factory_Work/` subfolder containing one Excel report.

## Path
```
{Project_Folder}/Factory_Work/{Project}_Factory_Work_Report.xlsx
```
Example: `10_Rateeb_Store_07/Factory_Work/Rateeb_Factory_Work_Report.xlsx`

## Sheet Structure (3 sheets)

### Sheet 1: POs_Summary
- Header row: project name, source, JN, code
- PO table: PO#, Date, Status, Created By, Approved By, Est. Cost, Items, Justification
- PO Items detail table below: PO#, Item, Qty, Unit Cost, Total, Ship To
- Total row in navy with white font

### Sheet 2: Labor_Costs
- Section A: Job-type aggregate (from FCA) — Job Type, Records, Hours, Cost, Rate/hr
- Section B: Task-level BOQ labor (from SysLeaders tasks) — BOQ, Description, Qty, Unit, Labor Cost, Unit Labor, Status
- Note explaining the two views of labor (aggregate vs. task-level)
- Total rows in navy

### Sheet 3: Factory_Summary
- Section 1: Raw Materials (POs) — each PO as a line, subtotal
- Section 2: Factory Labor — each job type as a line, subtotal with total hours
- Section 3: Fleet/Transport — transport + crane/equipment, subtotal
- TOTAL FACTORY COST row

## Style Conventions
- Navy fill: `#1E293B` with white bold Calibri 11pt
- Section headers: Calibri 12pt bold, `#1E293B`
- Data cells: Calibri 10pt, thin border `#D1D5DB`
- Notes: Calibri 9pt italic, `#999999`
- All amounts: `#,##0.00` number format
- RTL sheet view: `ws.sheet_view.rightToLeft = True`

## Data Sources
| Component | Primary Source | Fallback |
|-----------|---------------|----------|
| POs | SysLeaders live (browser) | Archived `Pruchasing-Orders_{Project}.xlsx` |
| PO Items | SysLeaders PO detail pages | Same archive |
| Job-type labor | FCA Analysis file (`{Project}_Factory_Cost_Analysis.xlsx`) | — |
| BOQ task labor | SysLeaders tasks or `tasks_{Project}.xlsx` | — |
| Fleet costs | Raw cost data (`تكاليف متجر {name}.xlsx` or `3004_{Project}_Cost_Data.xlsx`) | — |

## Python Dependencies
```python
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter
```

## Example: Rateeb Store totals
| Component | SAR |
|-----------|-----|
| PO00350 (manufacturing supplies) | 36,124.50 |
| PO00354 (paint) | 2,053.00 |
| PO00393 (glass) | 1,792.00 |
| **Subtotal POs** | **39,969.50** |
| Carpenter (78.5 hrs) | 962.00 |
| Fiber Technician (63.5 hrs) | 870.00 |
| Welder (54.5 hrs) | 649.00 |
| **Subtotal Labor** | **2,481.00** |
| Transport + Crane | 1,300.00 |
| **TOTAL FACTORY** | **43,750.50** |

## Verification
After building, read back with `read_file(path)` to confirm all 3 sheets populated correctly and totals match source data.
