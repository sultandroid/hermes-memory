# Design Tracker Excel — Populating from Repo + Odoo

## When to Use

User provides a Design Tracker Excel (Drawing Register + Validation Summary sheets) and asks to fill it with real data from the repo and Odoo.

## Source Priority Chain

| Priority | Source | What It Provides |
|----------|--------|-----------------|
| 1 | **Odoo** (project.task) | Actual package completion dates, progress %, state. Query via XML-RPC. |
| 2 | **Repo submittal register** (`01_Registers/submittal_register.md`) | Actual submission/approval dates, CG codes (B/C/D/DA/U) |
| 3 | **Repo submission plan** (`02_Schedule/submission_plan_risk_assessment.md`) | Forecast dates for phases not yet submitted |
| 4 | **Phase defaults** | Fallback: S→Mar, D-50→Jul, D-90→Aug, D-100→Sep, IFC→Aug, AFC→Sep, C→Sep |

## Odoo Integration

Key Odoo packages relevant to drawing phases (Project 219 — Aseer Museum):

| Odoo Package ID | Name | Drawing Phase | Notes |
|-----------------|------|---------------|-------|
| 3012 | 01 — Initial Studies & Survey | Survey (S) | Completed ~2 weeks from NTP (01-Dec-2025 → 15-Dec-2025) |
| 2938 | 01 — Architecture | DD 50%/90%/100%, IFC, AFC | |
| 2939 | 02 — Structural Engineering | Structural DD/IFC/AFC | |
| 2940 | 03 — MEP & IT Engineering | MEP DD/IFC/AFC | |
| 2941 | 04 — Life Safety | FLS DD/IFC/AFC | |

**"Project 5" in conversation = Odoo package ID 3012** (Initial Studies & Survey), not a drawing phase code. Always check Odoo first for actual completion dates.

## Phase-to-Drawing Mapping

Drawing number format: `{DISCIPLINE}-{PHASE}-{TYPE}-{SEQ}`

| Phase Code | Meaning | Submittal Ref |
|------------|---------|---------------|
| S | Survey | Odoo "01 — Initial Studies & Survey" (ID 3012) |
| D (50%) | DD 50% Gate | 1G-0001/0002 (Arch), 1C0-1G-0001 (Structural), 1E0-1G-0001 (Electrical), 1M0-1G-0001 (MEP) |
| D (90%) | DD 90% Gate | Not yet submitted for most disciplines |
| D (100%/Final) | DD 100% Gate | Not yet submitted |
| I | IFC | IFC-0003 through IFC-0008 |
| A (not Authority) | AFC | Not yet issued |
| A (Authority/Municipality/SEC/MOI/CITC/Fire) | Authority Submission | Various |
| C | As-Built | Not yet issued |

## Phase-to-Date Mapping (from submittal register)

| Phase | Date Source | Example |
|-------|-------------|---------|
| S (Survey) | Odoo package 3012 | Submitted 2025-12-01, Approved 2025-12-15 |
| D-50 (DD 50%) | DD Gate submittals (1G-0001 etc.) | Architecture: 2026-07-02→2026-07-15 (U) |
| D-50 Structural | 1C0-1G-0001 Rev.01 | 2026-07-18→2026-07-18 (C) |
| D-50 Electrical | 1E0-1G-0001 | 2026-07-06→2026-07-15 (U) |
| D-50 AV | AV DD Package | 2026-07-06 (DA) |
| D-50 Lighting | ZNA SOW | 2026-06-11→2026-06-11 (B) |
| IFC | IFC-0003–0008 | 2026-04-22→2026-04-29 (C) |
| BEP/Kick-Off | BEP submittal | Approved 2026-03-17 (B) |

## Excel Columns to Fill

| Col | Field | Source |
|-----|-------|--------|
| 1 | P6 Activity ID | Auto-generated (EN1000+) |
| 2 | Discipline | From drawing register |
| 4 | Drawing No. | From drawing register |
| 5 | Drawing Title | From drawing register |
| 7 | Date Submitted | From Odoo or submittal register (phase mapping) |
| 8 | Forecast Submission Date | Same as submitted date if real, else from submission plan |
| 9 | Status | From submittal register (Code-B/C/D/DA/U) |
| 10 | Date Approved | Real from submittal register, or calculated (submission + 7 working days) |
| 11 | Remarks | **Arabic status note** (not English source clause) |

## Remarks Column — Arabic Only

Use meaningful Arabic status notes, NOT contract clause references (SoW §7.1, ER §3.1.A.1.a):

| Status | Arabic Remark |
|--------|---------------|
| Survey completed | مكتمل - الدراسات الأولية والمسح الموقعي |
| DD 50% submitted, under review | قيد المراجعة - 50% Design |
| DD 50% approved | معتمد - 50% Design |
| DD 50% Code C | إعادة تقديم - 50% Design |
| DD 50% deemed approved | معتمد تلقائياً - 50% Design |
| Not yet submitted | لم يقدم بعد - 50% Design |
| IFC rejected | مرفوض - IFC |
| IFC deemed approved | معتمد تلقائياً - IFC |
| AFC not issued | لم يصدر بعد - AFC |
| As-Built not issued | لم يصدر بعد - As-Built |
| Authority submission | تقديم للجهات الرسمية |
| BEP approved | معتمد - BEP |
| BIM in progress | قيد التطوير - BIM |

## CG Review Period

- **Contractual SLA (ER §2.4.A)**: 14 calendar days
- **User preference**: 7 working days (Sun-Thu, KSA weekend Fri-Sat)
- When no real approval date exists, calculate: `submission_date + 7 working days`

## Working Days Calculator (KSA)

```python
from datetime import timedelta

def add_working_days(start_date, days):
    """Add working days (Sun-Thu). Fri/Sat are weekends."""
    current = start_date
    added = 0
    while added < days:
        current += timedelta(days=1)
        if current.weekday() in (4, 5):  # Fri=4, Sat=5
            continue
        added += 1
    return current
```

## Validation Summary Sheet

Fill P6 activity rows with actual drawing counts per discipline. Add formulas for:
- `Calculated Performance %` = `=IF(E>0,E/D,0)`
- `Variance` = `Calc - P6`
- `Validation Status` = `=IF(ABS(Variance)<=Tolerance,"Match","MISMATCH - Review")`

## Key Rules

- **No example/placeholder rows** — user insists on real data only
- **Unmerge merged cells** before writing (the template may have merged ranges)
- **Phase mapping is discipline-specific** — Architecture D-50 dates differ from Structural D-50 dates
- **DA (Deemed Approved)** is a valid status code — use it for submittals with no CG response >14 days
- **Source must be from repo registers or Odoo only** — do not invent dates. Every date must trace to `01_Registers/submittal_register.md`, `01_Registers/drawing_register.md`, `02_Schedule/submission_plan_risk_assessment.md`, or Odoo XML-RPC.
- **Clear separation: real dates vs forecast** — drawings with matching submittal refs get real dates. Drawings without matching refs get forecast dates. Never mix sources in the same cell.
- **Remarks = Arabic status, not source reference** — user explicitly rejected English source clause remarks.

## Pitfalls

- **"Project 5" in conversation = Odoo package ID 3012** (Initial Studies & Survey), not a drawing phase code
- **Survey dates**: NTP 01-Dec-2025, completed ~2 weeks = 15-Dec-2025. Do NOT use IR-0001 date (2026-05-14) — that's a different submittal
- **Remarks column**: User wants meaningful status notes in Arabic, not contract clause references
- **Merged cells**: Always unmerge before writing data rows, or openpyxl raises `MergedCell` errors
- **OneDrive**: Write to `/tmp` first, then copy to destination to avoid sync corruption
- **Odoo has no project ID 5** — the project list starts at ID 110+. "Project 5" refers to the 5th package in the Aseer project listing, which is package ID 3012.

## Python Pattern

```python
import openpyxl, re
from collections import Counter

# 1. Read drawing register markdown
with open("01_Registers/drawing_register.md") as f:
    content = f.read()

# 2. Parse drawing rows from markdown tables
drawings = []
for line in content.split('\n'):
    if '|' in line and line.strip().startswith('|'):
        cells = [c.strip() for c in line.split('|') if c.strip()]
        if len(cells) >= 7 and re.match(r'^[A-Z]-[A-Z]-[A-Z]-\d', cells[0]):
            drawings.append({
                'no': cells[0], 'title': cells[1],
                'discipline': cells[2], 'phase': cells[3],
            })

# 3. Open workbook, unmerge cells, clear data rows
wb = openpyxl.load_workbook("Design_Tracker.xlsx")
ws = wb['Drawing Register (Master Log)']
for mr in list(ws.merged_cells.ranges):
    ws.unmerge_cells(str(mr))
for r in range(2, 252):
    for c in range(1, 12):
        ws.cell(r, c).value = None

# 4. Phase-to-date mapping dict
phase_dates = {
    'S': ('2025-12-01', '2025-12-15', 'B'),
    'D-50': ('2026-07-02', '2026-07-15', 'U'),
    # ... add discipline-specific overrides
}

# 5. Fill rows
for i, d in enumerate(drawings, 2):
    ws.cell(i, 1, f"EN{1000 + i - 2}")
    ws.cell(i, 2, d['discipline'])
    ws.cell(i, 4, d['no'])
    ws.cell(i, 5, d['title'])
    # ... map phase to dates

# 6. Save
wb.save("Design_Tracker_filled.xlsx")
```
