# Stakeholder Register Update from Email

Workflow for keeping the Key Personnel Register (KPR) and Stakeholder Register up to date by searching Outlook emails for appointments, departures, CV submissions, and prequalifications.

## Trigger

User asks to "check all updates for stakeholders from emails" or "update registers from email sweep."

## Workflow Steps

### 1. Query Outlook SQLite for Stakeholder-Related Emails

The Outlook DB at `~/Library/Group Containers/UBF8T346G9.Office/Outlook/Outlook 15 Profiles/Main Profile/Data/Outlook.sqlite`

Run these search categories:

```sql
-- DEPARTURES: people leaving, resigning, being replaced
SELECT datetime(m.Message_TimeReceived, 'unixepoch', 'localtime'), 
       m.Message_NormalizedSubject, m.Message_Preview
FROM Mail m
WHERE (m.Message_NormalizedSubject LIKE '%resign%'
   OR m.Message_NormalizedSubject LIKE '%left%'
   OR m.Message_NormalizedSubject LIKE '%no longer%'
   OR m.Message_NormalizedSubject LIKE '%leaving%'
   OR m.Message_NormalizedSubject LIKE '%replaced%'
   OR m.Message_NormalizedSubject LIKE '%depart%')
  AND m.Message_TimeReceived > 1767225600  -- 2026-01-01
ORDER BY m.Message_TimeReceived DESC;

-- NEW APPOINTMENTS: appointed, nominated, assigned
SELECT datetime(m.Message_TimeReceived, 'unixepoch', 'localtime'), 
       m.Message_NormalizedSubject, substr(m.Message_Preview,1,500)
FROM Mail m
WHERE (m.Message_NormalizedSubject LIKE '%appoint%'
   OR m.Message_NormalizedSubject LIKE '%nominat%'
   OR m.Message_NormalizedSubject LIKE '%assign%')
  AND m.Message_TimeReceived > 1767225600
ORDER BY m.Message_TimeReceived DESC;

-- CV SUBMISSIONS / KEY PERSONNEL
SELECT datetime(m.Message_TimeReceived, 'unixepoch', 'localtime'), 
       m.Message_NormalizedSubject, substr(m.Message_Preview,1,500)
FROM Mail m
WHERE (m.Message_NormalizedSubject LIKE '%CV%'
   OR m.Message_NormalizedSubject LIKE '%Key Personnel%'
   OR m.Message_NormalizedSubject LIKE '%KP Register%')
  AND m.Message_TimeReceived > 1767225600
ORDER BY m.Message_TimeReceived DESC;

-- PREQUALIFICATION STATUS
SELECT datetime(m.Message_TimeReceived, 'unixepoch', 'localtime'), 
       m.Message_NormalizedSubject, substr(m.Message_Preview,1,500)
FROM Mail m
WHERE m.Message_NormalizedSubject LIKE '%prequal%'
   OR m.Message_NormalizedSubject LIKE '%PQ-%'
ORDER BY m.Message_TimeReceived DESC;

-- DOCUMENT CODES (e.g. PL-0020, ZD-0056, PQ-0097)
SELECT datetime(m.Message_TimeReceived, 'unixepoch', 'localtime'), 
       m.Message_NormalizedSubject, m.Message_SenderList
FROM Mail m
WHERE m.Message_NormalizedSubject LIKE '%PL-0020%'
   OR m.Message_NormalizedSubject LIKE '%ZD-0056%'
-- Add specific doc codes to check
ORDER BY m.Message_TimeReceived DESC;

-- SPECIFIC ROLE NAMES (companies, specialists)
SELECT datetime(m.Message_TimeReceived, 'unixepoch', 'localtime'), 
       m.Message_NormalizedSubject, substr(m.Message_Preview,1,500)
FROM Mail m
WHERE (m.Message_NormalizedSubject LIKE '%ZNA%'
   OR m.Message_NormalizedSubject LIKE '%Glasbau%'
   OR m.Message_NormalizedSubject LIKE '%Rawasen%'
   OR m.Message_NormalizedSubject LIKE '%Lumotion%'
   OR m.Message_NormalizedSubject LIKE '%NRS%'
   OR m.Message_NormalizedSubject LIKE '%AD Engineering%')
  AND m.Message_TimeReceived > 1767225600
ORDER BY m.Message_TimeReceived DESC;
```

### 2. Read the Current Registers

```python
import openpyxl

# KPR Excel
kpr_path = "/path/to/Key_Personnel_Register.xlsx"
wb = openpyxl.load_workbook(kpr_path)
ws = wb['Key Personnel']

# Print all rows to see current state
for row in range(1, ws.max_row + 1):
    vals = [str(ws.cell(row=row, column=c).value or '') for c in range(1, ws.max_column + 1)]
    print(f"R{row}: {vals[0]:12s} | {vals[1]:40s} | {vals[2]:30s}")

# Also check columns 7-10 for CV Ref, MoC Status, Approval Date, Notes
```

### 3. Categorize Findings

Group email findings into categories:

| Category | What to Look For |
|----------|------------------|
| **Departed** | Resignation emails, "no longer with company", removal from distribution |
| **Newly Appointed** | Appointment emails, nomination letters, NDA confirmations |
| **Status Changed** | CG codes (A/B/C/D) on prequal/design documents |
| **CV Submitted** | KP CV packs submitted for approval |
| **Still Vacant** | Emails asking to find/engage specific roles (ITCA, MOI Security, etc.) |
| **New Contacts** | Names + emails discovered in CC lines or signatures |

### 4. Cross-Reference Against Registers

For each finding:
- Check if the role already exists in KPR → update the row
- Check if the role exists in the Stakeholder Register → update or add
- If a person departed, check if a replacement is already listed
- If a CG code changed (e.g. Pending → Code B), update MoC Status column

### 5. Update KPR Excel Cells

Key columns in the KPR (`Key Personnel` sheet):
- **Col 2**: Role name
- **Col 3**: Person name
- **Col 7**: CV reference
- **Col 8**: MoC Approval Status (Pending submission / Approved / Code B / Code C / etc.)
- **Col 9**: MoC Approval Date
- **Col 10**: Lock-in Notes / Comments

Update pattern:
```python
# Update a single row's MoC Status and Notes
ws.cell(row=12, column=8).value = 'Approved with Comments (Code B)'
ws.cell(row=12, column=10).value = existing_notes + '. ZNA Studio APPOINTED — Julie Riley. ZD-0056 Code B, 11 Jun 2026.'

# Append to notes (preserve existing info)
existing = ws.cell(row=row, column=10).value or ''
ws.cell(row=row, column=10).value = existing.rstrip('.') + '. New info here.'
```

### 6. Update Stakeholder Register

Read the stakeholder Excel, find matching rows by role name or STK reference, update:
- Contact names/emails
- Status (Appointed / Prequal in Progress / TBC / Rejected)
- Notes with latest developments

Add new rows for roles not yet in the register (e.g. ITCA, MOI Security Consultant).

### 7. Update Project Memory

Update PROJECT_MEMORY.md sections:
- **§0 (Latest Updates)**: Add lines for each major change
- **§2 (Org Chart / Personnel)**: Update departed/replaced personnel
- **§11 (Submittals & Specialist Status)**: Update approval status tables

### 8. Update Odoo Task Description

If the relevant Odoo task (e.g. PL-0020 Stakeholder Management Plan) tracks stakeholder status, append a structured HTML update section with:
- Departed/replaced personnel
- New appointments with CG codes
- Critical path vacancies
- New contacts discovered

## SQL Query Tips

- Use `datetime(m.Message_TimeReceived, 'unixepoch', 'localtime')` for readable dates
- Use `substr(m.Message_Preview, 1, 500)` for body preview (column name is `Message_Preview`)
- Filter by `m.Message_TimeReceived > <unix_timestamp>` to recent results (1767225600 = 2026-01-01)
- Join with `folders` table for folder context: `JOIN folders f ON m.Record_FolderID = f.Record_RecordID`
- The `Message_SenderList` column contains sender name/email

## Files to Update

| File | Location (Aseer Museum base) | Action |
|------|------------------------------|--------|
| KPR Excel | `Docs/09_Registers/13_Key_Personnel_Register/Aseer_Museum_Key_Personnel_Register.xlsx` | Update cells |
| Stakeholder Register | `Docs/02_Plans_and_Procedures/02.13_Stakeholder_Plan/04_Registers/AMA-STK-REG-001_Stakeholder_Register_Internally initial draft 01.xlsx` | Update rows |
| PROJECT_MEMORY.md | `PROJECT_MEMORY.md` | Patch sections |
| CG Compliance File | `Desktop/CG_Comments_Compliance_Rev03.md` | Update comments |
| Odoo Task | `project.task` ID 3211 (PL-0020) | Update description |

## Pitfalls

- **Don't overwrite existing notes** — append to Col10 using `.rstrip('.')) + '. new info.'` pattern 
- **CG Code C ≠ Done** — Code C means Revise & Resubmit; the task stays open. Only Code A or B closes the cycle.
- **Names may be stale** — A person named in the register may have left; cross-check with departure emails before assuming current
- **Thread subjects may be misleading** — An email about "ZNA Studio - Contract Preparation" may not mention "Lighting" in the subject; search by company name too
- **Check Email_Archive folder** — Some processed email summaries exist as .md files in the project's `Email_Archive/` folder and can supplement raw SQLite queries
