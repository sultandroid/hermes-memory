---
name: discipline-submission-plan
title: Create a Discipline-Specific Submission Plan (Markdown + Excel)
description: Full workflow for creating a per-discipline submission plan — markdown source in repo, Excel workbook in OneDrive registers folder. Follows the Arch Submission Plan Rev02 format and Graphics plan template.
---

## When to use

The user asks you to create a submission plan for a specific discipline (Landscape, Lighting, Structural, MEP, AV, Graphics, etc.).

## Prerequisites

1. Load this skill: `skill_view(name='discipline-submission-plan')`
2. Read the repo instructions in `AGENTS.md` under "Discipline-Specific Submission Plans" and "Design Submission Plan & Risk Assessment"
3. Read the existing reference plans:
   - `02_Schedule/graphics_submission_plan.md` — markdown template (8 sections)
   - `02_Schedule/submission_plan_risk_assessment.md` — master schedule with dates per discipline
   - `02_Schedule/landscaping_submission_plan.md` — example of a completed plan
4. Read the Arch Excel template at `OneDrive: .../02_Submittals/04_Registers/Arch_Submittal_Register/Aseer_Arch_Submission_Plan_Rev02.xlsx` — this is the style reference

## Step 1 — Research the discipline

Before writing anything, gather:

| Source | What to extract |
|--------|----------------|
| **SoW / ER** | Scope items, clause numbers, deliverables |
| **Master submission plan** (`submission_plan_risk_assessment.md`) | Dates, parallel group, dependencies for this discipline |
| **Specialist's own submittal register** (if exists in OneDrive) | Their own deliverable list, ref codes, stages |
| **CG approval** (if specialist is appointed) | Any scope extensions or conditions |
| **PROJECT_MEMORY.md** | Procurement status, blockers, key personnel |
| **DMP Scope Summary** (`04_Scope_of_Works_Summary.md`) | SoW clause mapping |

**Critical scope boundary check:** read the specialist's SoW AND their submittal register. The SoW may list one scope, but the CG-approved scope or submittal register may extend it. Example: ZNA's SoW lists interior areas, but CG comment #1 requires "all project different lighting systems, spaces" and ZNA's own submittal register includes LG-024 "Exterior lighting design" under SoW §8.8. Always check the full picture before assigning deliverables.

## Step 2 — Create the markdown file

Save to `02_Schedule/{discipline}_submission_plan.md` with 8 sections:

### Section 1 — Deliverable Register

Table with columns: Ref, Deliverable, Due Stage, Acceptance Criteria, Status

| Ref | Deliverable | Due Stage | Acceptance Criteria | Status |
|-----|------------|-----------|-------------------|--------|
| L-D-L-001 | 50% Landscape Concept & Schedule | D-55 (29/07) | Design intent approval by NRS | **Not started** |

Ref format: `{DISCIPLINE_PREFIX}-{STAGE}-{NNN}` where:
- L = Landscape, LG = Lighting, G = Graphics, M = MEP, S = Structural, AV = AV/IT, etc.
- D-L = Design Level, IFC = IFC, HO = Handover

### Section 2 — Approval Workflow

4-stage table: Stage → Action → Responsible → Duration → Gate

### Section 3 — Schedule & Milestones

Table: Milestone → Target → Dependency → Risk

### Section 4 — Submission Batches

Grouped by stage: Concept → Detailed Design → Final Design → IFC → Handover

Each batch lists the deliverables included and the trigger condition.

### Section 5 — Dependencies & Risks

Table: Dependency → Owner → Status → Impact

### Section 6 — Coordination Interfaces

Table: Trade → Key Coordination Item

### Section 7 — Procurement Status

Table: Item → Status (specialist, prequal, contract, blockers, overall risk level)

### Section 8 — Scope Summary

Table: Item → SoW Reference → Description

Add a note at the bottom clarifying any scope boundaries with other specialists.

## Step 3 — Create the Excel workbook

Save to `/Volumes/MIcro/.pi-tmp/work/` first, then copy to OneDrive.

### Style (match Arch Submission Plan Rev02 exactly)

| Element | Style |
|---------|-------|
| **Row 1 headers** | Navy `#1F3864` fill, white bold 11pt Calibri, center aligned, wrap text, thin borders |
| **Gate section headers** | Light blue `#D6E4F0` fill, navy `#1F3864` bold 11pt, left aligned, merged across all 15 columns |
| **Level section headers** | Gray `#E8E8E8` fill, navy `#1F3864` bold 10pt, left aligned, merged across all 15 columns |
| **Data rows** | Light green `#F0F8F0` fill, 10pt Calibri, wrap text, thin borders |
| **Column widths** | A=18, B=18, C=16, D=20, E=30, F=55, G=12, H=16, I=12, J=10, K=20, L=14, M=12, N=14, O=22 |

### 15 columns

| Col | Header | Alignment |
|-----|--------|-----------|
| A | Gate | Center |
| B | Level / Zone | Left |
| C | Discipline | Center |
| D | Submission Category | Center |
| E | Drawing Package / Item | Left |
| F | Submission Description | Left |
| G | Responsibility | Left |
| H | Planned Submission Date | Center |
| I | Review Duration (Days) | Center |
| J | Approval Authority | Center |
| K | Linked Activity ID (Program) | Center — **leave empty**, not confirmed yet |
| L | Status | Center |
| M | Response Code | Center |
| N | Resubmit Date | Center |
| O | Remarks | Left |

### Section hierarchy

```
Row 1: Headers (navy)
Row 2: Gate 1 - Detailed Design (light blue, merged A-O)
Row 3: DD - Zone Name (gray, merged A-O)
Row 4+: Data rows (light green)
...
Row N: Gate 2 - Material Approval (light blue, merged A-O)
...
Row N: Gate 3 - IFC (light blue, merged A-O)
...
Row N: General - All Levels (gray, merged A-O)
```

### Python generation pattern

```python
from openpyxl import Workbook
from openpyxl.styles import PatternFill, Font, Alignment, Border, Side

# Styles
navy_fill = PatternFill(start_color='FF1F3864', end_color='FF1F3864', fill_type='solid')
light_blue_fill = PatternFill(start_color='FFD6E4F0', end_color='FFD6E4F0', fill_type='solid')
gray_fill = PatternFill(start_color='FFE8E8E8', end_color='FFE8E8E8', fill_type='solid')
light_green_fill = PatternFill(start_color='FFF0F8F0', end_color='FFF0F8F0', fill_type='solid')

header_font = Font(name='Calibri', bold=True, size=11, color='FFFFFFFF')
gate_font = Font(name='Calibri', bold=True, size=11, color='FF1F3864')
level_font = Font(name='Calibri', bold=True, size=10, color='FF1F3864')
data_font = Font(name='Calibri', size=10)

center_align = Alignment(horizontal='center', vertical='center', wrap_text=True)
left_center = Alignment(horizontal='left', vertical='center')
top_wrap = Alignment(vertical='top', wrap_text=True)
center_top = Alignment(horizontal='center', vertical='top', wrap_text=True)
thin_border = Border(top=Side(style='thin'), bottom=Side(style='thin'))

# Helper functions
def write_section(ws, row, text, fill=light_blue_fill, font=gate_font):
    ws.merge_cells(start_row=row, start_column=1, end_row=row, end_column=15)
    c = ws.cell(row=row, column=1, value=text)
    c.fill = fill; c.font = font; c.alignment = left_center; c.border = thin_border
    return row + 1

def write_data_row(ws, row, vals):
    for ci, v in enumerate(vals, 1):
        c = ws.cell(row=row, column=ci, value=v)
        c.fill = light_green_fill; c.font = data_font; c.alignment = top_wrap; c.border = thin_border
    for ci in [1, 3, 4, 8, 9, 10, 11, 12, 13, 14]:
        ws.cell(row=row, column=ci).alignment = center_top
    return row + 1
```

## Step 4 — Save and copy

1. Save Excel to `/Volumes/MIcro/.pi-tmp/work/{filename}.xlsx`
2. Copy to `OneDrive: .../02_Submittals/04_Registers/{filename}.xlsx`
3. Markdown stays in `02_Schedule/{discipline}_submission_plan.md` as repo truth

## Pitfalls

- **Linked Activity ID (col K):** leave empty. Do not invent programme codes.
- **Scope boundary check:** before assigning a deliverable to a discipline, read the specialist's SoW AND their submittal register. The SoW may say one thing but the CG-approved scope or submittal register may extend it. Example: ZNA's SoW lists interior areas, but CG comment #1 requires "all project different lighting systems, spaces" and ZNA's own submittal register includes LG-024 "Exterior lighting design" under SoW §8.8.
- **Dates:** pull from `submission_plan_risk_assessment.md` master schedule. Do not invent dates.
- **Section headers:** always merge across all 15 columns. Never leave a section header unmerged.
- **Column K:** always empty until programme activity codes are confirmed by the planning engineer.
- **File naming:** `Aseer_{Discipline}_Submission_Plan_Rev00.xlsx` for Excel, `{discipline}_submission_plan.md` for markdown.
- **OneDrive copy:** use `cp` from `/Volumes/MIcro/.pi-tmp/work/` to the OneDrive path. Do not write directly to OneDrive.
