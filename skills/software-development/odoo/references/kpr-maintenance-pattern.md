# KPR Maintenance — Status Labels, Dates & Action Tracking

## Field Reference (Key Personnel Register Excel)

| Column | Field | Purpose |
|--------|-------|---------|
| 1 | Tier | 1=Management, 2=Design Specialists, 3=Testing/Authority, Authority=Statutory |
| 2 | Role | Full role name per contract/Appendix B |
| 3 | Name | Entity or person (company name or individual) |
| 4 | Years Exp | Optional experience note |
| 5 | Discipline/Specialty | Brief scope description |
| 6 | Authority Registration | Cert/license numbers |
| 7 | CV Ref | Path to CV file on Aconex |
| 8 | MoC Approval Status | See status labels below |
| 9 | MoC Approval Date | Date of approval or milestone |
| 10 | Notes | Scope notes + **ACTION:** prefix for pending items |

## Status Labels (Col 8)

Use exact labels for consistency:

| Status | Meaning | When to Use |
|--------|---------|-------------|
| `Approved` | Fully approved by CG/MoC | Glasbau Hahn, NRS roles, Nama (FLS) |
| `Approved with Comments (Code B)` | Approved but has minor CG notes | ZNA (11 Jun), AD Engineering (15 Jun) |
| `Nominated - pending approval` | Selected but not yet CG-approved | Lumotion (7 Jun, NDA signed) |
| `Pending - not yet approved by CG` | Submitted but awaiting CG review | Rawasen AV, Samaya Graphit, Samaya Factory |
| `Pending - to be submitted during project` | Will be submitted later per programme | M&E Contractor |
| `Prequalification in progress` | Pre-qual active, not yet submitted | Landscaping |
| `Not yet appointed` | Vacant, no vendor/entity identified | Fire-Proofing, Acoustic, Rigging |
| `Not yet appointed - CRITICAL PATH` | Vacant AND on critical path | ITCA (needed before commissioning) |
| `C - Revise and Resubmit` | CG returned with Code C | Sustainability (11 Jun) |
| `Statutory` | Authority role — not Samaya's hire | SEC, Municipality, CITC, MOI rows |
| `Approved (pending formal notification)` | Approved per user knowledge, no email yet | Waris (PD) |

## Approval Dates (Col 9)

- Always use format: `DD-Mon-YYYY` (e.g. `15-Jun-2026`)
- For pending dates, use the event date: `07-Jun-2026 (NDA signed)`
- For user-reported dates not yet in email: prefix with `~` (e.g. `~13-Jun-2026`)

## Action Notes (Col 10)

Every pending row MUST have a clear action prefix:

```
ACTION: [what needs to happen, by whom, referencing which contract/CG requirement]
```

Examples from Aseer project:
- `ACTION: Source and appoint M&E Contractor for MEP+FLS+Lighting installation package.`
- `ACTION: Submit PQD + 2 alternative vendors per CG CRS comment 11.`
- `ACTION: Revise CV Packages A and B and resubmit to CG.`
- `ACTION: Appoint before any system commissioning begins per ER sec 2.6.B. Independent of Samaya.`
- `ACTION: Complete prequal of 2-3 contractors and submit to CG.`

## Personnel Change Tracking

When a team member departs or a new appointment happens:

1. If from email: check subject and attachment for confirmation
2. If from user knowledge (no email yet): mark status as `Approved (pending formal notification)` and date as `~DD-Mon-YYYY`
3. Update the Name field to the new person
4. Update Notes to record the replacement chain: `Replaced [old person]. [New person] status: [detail].`
5. Sync to PROJECT_MEMORY.md and Odoo task description
6. Only remove the old person from register when you have a confirmed replacement

## Excel Write Safety

- **CRITICAL: Never rebuild a formatted Excel from scratch.** The user has approved a unified register template with logos, merged cells, and company styling. A subagent that rebuilds the file with plain openpyxl without preserving the template will destroy all formatting. Always:
  1. **Copy from the .bak file** or the original formatted template first (`openpyxl.load_workbook(original)`)
  2. **Read source data** from the modified file, **copy values only** to the formatted backup
  3. **Never use `skill_view(...)` subagents to modify Excel** — their default openpyxl saves strip styling
  4. If formatting is accidentally lost, restore from the `.bak` file and re-apply data changes with value-only writes
  
- **Always close the .xlsx file in Excel before writing with openpyxl.**
  If the file is open, `wb.save()` may fail silently or corrupt data.
  The user's instruction: "always when need to write in file already opened close it first and then write or update and reopen."

- **After writes, verify by re-reading** — call `openpyxl.load_workbook()` again and print the rows to confirm values persisted. openpyxl may not save correctly if the file was locked or path was wrong.
