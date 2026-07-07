# Two-Way KPR ↔ Plan Sync Workflow

## Context

The KPR (Key Personnel Register) is the authoritative source for personnel/firm names and approval statuses. The Resource Plan must reflect the KPR, and in some cases (when user provides the file), the KPR can be updated to reflect plan changes.

## Direction 1: KPR → Plan (Mandatory before every submission)

### Step 1 — Read the KPR
```bash
python3 -c "
import openpyxl
wb = openpyxl.load_workbook('path/to/KPR.xlsx', data_only=True)
ws = wb['Key Personnel']
for row in ws.iter_rows(min_row=2, max_row=ws.max_row, values_only=True):
    if any(v is not None for v in row):
        print(f'{row[0] or \"\":8s} | {str(row[1] or \"\")[:40]:40s} | {str(row[2] or \"\")[:30]:30s} | {str(row[7] or \"\")[:25]:25s}')
"
```

### Step 2 — Entity Name Alignment
The KPR's entity names are authoritative. The following corrections are routinely needed:

| Plan says | KPR says | Action |
|-----------|----------|--------|
| `Rawasin` | `Rawasen` | Use KPR spelling |
| `Nama Al Amal` | `Nama Consulting` | Use KPR spelling |
| `Glassbühne` | `Glasbau Hahn` | Use KPR spelling |
| `Eng. Jim Richards` | `Eng. Jim — NRS` | Use KPR format if individual is separately approved |
| `AV Hardware — NRS` | `Rawasen` | Rawasen is the AV/interactives specialist |

### Step 3 — Status Mapping
Map KPR status columns to plan display:

| KPR Status | Plan Display (Tier 2 table) | Plan Display (Exhibition Matrix §7.3) |
|------------|----------------------------|--------------------------------------|
| Approved | Firm name only | `Approved` |
| Approved with Comments (Code B) | Firm name only | `Code B approved [date]` |
| Pending - not yet approved by CG | Firm name only | `Firm — pending approval` |
| Pending submission | Name (person IS on board) | Name or `On board` |
| C - Revise and Resubmit (Code C) | TBC (firm-level status) | `TBC` (don't write "Code C" in plan) |
| Vacant | `Vacant` | `Vacant` |
| Not yet appointed | `TBC` | `TBC` |
| Nominated - pending approval | Do NOT mention in plan | Remove entirely |

### Step 4 — Plan Updates
For each discrepancy found, update the plan:
- Entity name correction (Tier 2 table, Exhibition Matrix, Location Matrix)
- Status column update
- Tier reclassification if KPR has different tier assignment
- Missing role addition if KPR shows a role not in the plan

## Direction 2: Plan → KPR (Only when user provides the file)

### When to do this
The default rule is **do NOT modify the KPR Excel** — it's a controlled register maintained by PD/HR. Only edit when the user explicitly attaches the file AND asks for sync.

### What to update
- Only the **notes columns** (`Lock-in Notes / Comments`, column 10)
- NEVER change: names, tiers, MoC Approval Status, dates, or role titles without explicit user instruction
- The Site Manager role rename (Construction Manager → Site Manager per DMP) can be done in the KPR notes

### What NOT to update
- Internal Samaya staff (Tech Office Manager, Planner, Document Controller, BIM Modelers, Electrical Eng.) are NOT KPR roles — they are operational staff, not "Key Personnel"
- Document metadata fields (Prepared By, Checked By) are operational facts, not KPR claims

### Technical notes
- Use `terminal` with system python3, NOT `execute_code` — OneDrive paths time out from the sandbox
- Use `ws.cell(row=N, column=M).value = '...'` — do NOT use `ws.insert_rows()` which silently loses data on OneDrive-synced files
- Save in place with `wb.save(path)` — preserve the original filename
- Report exactly what changed: count of rows modified, specific values

## Common Pitfalls

- **Do NOT blank on-board personnel names.** "Pending submission" in KPR means the person IS on board — keep the name. "Pending - not yet approved by CG" means firm is FIRM name only, no individuals.
- **Do NOT write "Code C (revise & resubmit)" in plan documents.** That's KPR-level detail. For the plan, show `TBC` (if no firm) or firm name with `submission in progress`.
- **Do NOT remove a contractually-mandated role** just because its assigned firm is unapproved. The role stays as TBC per SOW §5.5.
- **Do NOT use `execute_code` to read OneDrive xlsx files** — the sandbox's fcopyfile times out.
