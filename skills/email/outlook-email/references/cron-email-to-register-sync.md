# Cron: Email → Register Sync (4× Daily)

## When to Use

- User asks to "update all registers daily" from email
- Setting up an autonomous pipeline: Outlook scan → classify → update repo registers → commit → push → notify

## Architecture

```
Cron (09:00, 13:00, 17:00, 21:00 AST)
  │
  ├── SQLite query (last 6h) → classify emails
  │     └── Fallback: AppleScript if TCC blocks SQLite
  │
  ├── Update registers:
  │     ├── deliverables_register.md (submittals, DD gates)
  │     ├── plan_tracker.md (plan submissions)
  │     ├── subcontractor_sow_raci_register.md (prequals)
  │     ├── ncr_register.md (NCRs)
  │     ├── decisions_log.md (CG responses, approvals)
  │     ├── action_items.md (meeting follow-ups)
  │     ├── risks.json → risk_sync.py (risk-related)
  │     └── project_status.md (milestones)
  │
  ├── Write email scan log to reviews/email_scan_<date>.md
  ├── Update AGENTS.md Latest Updates section
  ├── git add + commit
  └── Deliver summary to user (Telegram + all channels)
```

## Classification Table

| Type | Pattern | Register |
|------|---------|----------|
| Submittal / DD Gate | `1G-`, `ZD-`, `IFC-`, `PL-`, `MA-` | `deliverables_register.md` |
| Plan submission | `PL-`, `ZD-` (plan-related) | `plan_tracker.md` |
| Prequalification | `PQ-` | `subcontractor_sow_raci_register.md` |
| NCR | `NC-`, `NCR` | `ncr_register.md` |
| Decision / CG response | Code B/C/D, approval/rejection | `decisions_log.md` |
| Action item | Meeting follow-up, request | `action_items.md` |
| Risk-related | Assessment, delay, issue | `risks.json` → `risk_sync.py` |
| Milestone | Submission, approval | `project_status.md` |
| Aconex transmittal | `WTRAN` | Info only — log in scan file |

## Filtering Rules

**Filter out** (non-project):
- ERP POs (P01939, P02044, etc.)
- SPMS project status notifications
- Power Automate failure reminders
- SharePoint anonymous access link notifications
- Marketing / promotional emails
- Ops/logistics: car requests, shipments, painter notifications, rest house/rental

**Keep** (project-critical):
- Document submittals, contract actions, consultant deliverables
- Vendor approvals, CG correspondence, inspection requests
- CVs, schedules, safety reports, PO requests, task assignments

## SQLite Query (6h window)

```sql
SELECT m.Record_RecordID, datetime(m.Message_TimeReceived, 'unixepoch', 'localtime') as received,
       f.Folder_Name, m.Message_SenderList, m.Message_NormalizedSubject, m.Message_HasAttachment
FROM Mail m JOIN folders f ON m.Record_FolderID = f.Record_RecordID
WHERE datetime(m.Message_TimeReceived, 'unixepoch', 'localtime') >= datetime('now', '-6 hours', 'localtime')
  AND (f.Folder_Name IN ('Asher Regional Museum', 'Inbox') OR m.Message_NormalizedSubject LIKE '%MOC-MUS-ASE%')
ORDER BY m.Message_TimeReceived;
```

## Pitfalls

- **SQLite TCC blocks intermittently** — always have AppleScript fallback ready
- **Arabic subjects** — translate to English on display
- **No project-critical emails** — still write a brief scan log saying so, commit only the scan file
- **Append only** — never delete rows from registers
- **Deliver to `all`** so the user gets Telegram notification each run
- **Scan window = 6h** (not 24h) since runs 4× daily
