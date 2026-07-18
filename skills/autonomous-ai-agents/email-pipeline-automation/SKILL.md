---
name: email-pipeline-automation
description: "Scan Outlook every 3h for project emails, extract attachments, route to project folders, update repo registers. Full email triage pipeline."
tags:
  - outlook
  - email
  - automation
  - pipeline
  - cron
---

# Email Pipeline Automation — Aseer Museum

Run every 3 hours via cron. Scans last 48h of Outlook, identifies project-critical emails, extracts attachments, routes to correct project folders, updates repo registers.

Project root: `/Volumes/MIcro/Work/Aseer-Museum/`
Repo root: `~/aseer-museum-pm/`

## WORKFLOW RULE (MANDATORY)

**Check project emails BEFORE modifying any repo files.** Email may contain PM instructions, CG comments, or context that changes what needs to be done. When you enter a session intending to edit project-controlled files, run a manual email scan first. This applies to: risk register, RMP, NCR register, subcontractor SOWs, submission plans, design status, any project-controlled document.

## DB Location
`~/Library/Group Containers/UBF8T346G9.Office/Outlook/Outlook 15 Profiles/Main Profile/Data/Outlook.sqlite`

## Step 0 — Verify epoch

```sql
SELECT Message_TimeReceived,
       datetime(Message_TimeReceived, 'unixepoch', 'localtime') as as_unix,
       datetime(Message_TimeReceived + 978307200, 'unixepoch', 'localtime') as as_mac
FROM Mail ORDER BY Message_TimeReceived DESC LIMIT 1;
```
If `as_unix` shows today's date, use `'unixepoch'`. If `as_mac` shows today's date, add `+ 978307200` to every timestamp.

## Step 1 — Scan emails (last 48h)

```sql
SELECT m.Record_RecordID as id,
       datetime(m.Message_TimeReceived, 'unixepoch', 'localtime') as received,
       f.Folder_Name as folder,
       m.Message_SenderList as sender,
       m.Message_NormalizedSubject as subject,
       m.Message_HasAttachment as att
FROM Mail m
JOIN folders f ON m.Record_FolderID = f.Record_RecordID
WHERE m.Message_TimeReceived >= strftime('%s', 'now', '-48 hours', 'localtime')
ORDER BY m.Message_TimeReceived DESC;
```

## Step 2 — Extract attachments

Use AppleScript batch extract (save to `/tmp/email_attachments/`). Skip `image/*` content types.

### Cron-mode pattern: per-email `.applescript` files (PREFERRED)

The ~700-byte AppleScript body limit blocks monolithic batch scripts. Write one short `.applescript` file per email ID, then run each with `osascript`:

```bash
# Write individual scripts via write_file tool, then:
for f in /tmp/extract_*.applescript; do osascript "$f" 2>&1; done
```

Each script handles one email ID — stays well under the byte limit:

```applescript
set outFolder to "/tmp/email_attachments/"
tell application "Microsoft Outlook"
	set eidVal to 48572
	set theMsg to message id eidVal
	set atts to (every attachment of theMsg)
	repeat with att in atts
		if content type of att does not start with "image/" then
			set attName to name of att
			set savePath to outFolder & "48572_" & attName
			do shell script "touch " & quoted form of savePath
			save att in (POSIX file savePath as alias)
		end if
	end repeat
end tell
```

Run all extraction scripts in parallel (they're independent) to speed up the batch.

### Interactive-mode alternative: bash heredoc loop

For non-cron sessions where `execute_code` is available, a bash heredoc loop works for smaller batches:

```bash
for id in 35001 35002 35003; do
  osascript <<EOF
tell application "Microsoft Outlook"
    set theMsg to message id $id
    set atts to (every attachment of theMsg)
    set outFolder to "/tmp/email_attachments/"
    repeat with att in atts
        set attName to name of att
        set savePath to outFolder & "${id}_" & attName
        do shell script "touch " & quoted form of savePath
        set saveFile to POSIX file savePath as alias
        save att in saveFile
    end repeat
end tell
EOF
done
```

### Verify extraction

After extraction, list the staging directory to confirm files landed:

```bash
ls -la /tmp/email_attachments/
```

## Step 3 — Classify & Route

| Document Type | Routing Folder (Aseer Museum root) |
|---|---|
| NCR (MOC-MUS-CG-ASE-NC-*) | `04_Docs /10_Test_and_Inspection/10.3_NCRs/{NCR-ID}/` |
| Subcontractor Prequal (PQ-*) | `24_Subcontractors/{NN}_{Specialist}/01_Prequalification/` |
| Contracts/Agreements (main contract) | `00_Contracts/` |
| Subcontractor Contracts | `24_Subcontractors/{NN}_{Specialist}/02_Contract/` |
| Scope of Work | `24_Subcontractors/{NN}_{Specialist}/01_Scope_of_Work/` |
| Proposals | `24_Subcontractors/{NN}_{Specialist}/08_RFP_and_Proposals/` |
| Design Submittals — DD Gate (1G-*) | `02_Submittals/01_DD_Gate/{Discipline}/` |
| Design Studies (DS01, DDD-*) | `03_Design_Files/` |
| DWG drawings | `03_Design_Files/` |
| Material Lists | `04_Docs /09_Registers/22_Procurement_Schedule/MEP_Materials/` |
| Plans (PL-*) | `04_Docs /02_Plans_and_Procedures/{folder}/` |
| General Documents (ZD-*) | `04_Docs /02_Plans_and_Procedures/{folder}/` |
| Weekly / Daily Reports | `00_Status/` |
| Meeting Minutes (MOM) | `00_Status/` |
| Material Board Review Comments | `03_Design_Files/FF&E_Material_Boards/` |
| Management Plans Status | `04_Docs /09_Registers/` |
| Design Management / Tracking | `03_Design_Files/` |
| Safety / HSE Documents | `04_Docs /02_Plans_and_Procedures/02.5_HSE_Plan/` |
| HERC/SASO compliance guidelines | `04_Docs /02_Plans_and_Procedures/02.5_HSE_Plan/` |
| Daily Reports | `00_Status/` |
| RFQ / Procurement Schedules | `04_Docs /09_Registers/22_Procurement_Schedule/` |
| Schedule files (.xer) | `02_Schedule/` |
| Risk Register | `04_Docs /09_Registers/23_Project_Risk_Register/` |
| Aconex notifications (no att) | Skip — CDE-based, reference only |
| Ops/HR/ERP | Skip — not project-critical |

## Step 4 — Update Repo Registers

- **NCRs**: Append new NCR rows to `~/aseer-museum-pm/01_Registers/ncr_register.md`
- **Risk Register**: Add new risks or update status in `~/aseer-museum-pm/01_Registers/risk_register.md`
- **Subcontractors**: Note prequal/submission status in subcontractor `_status.md` files
- **Procurement**: Note proposals received in procurement tracking
- **Weekly Review**: Log findings to `~/aseer-museum-pm/03_Plans/08_Risk/reviews/`

## Step 5 — Key Senders to Watch

| Sender | Role | Priority |
|---|---|---|
| Hossam Mabrouk | CG (PMC) — NCRs, design reviews, submittal responses | High |
| Muhammad Waris Sultan Khan | Project Director — directives, deadlines, contracts | High |
| Mohamed Samir | Construction Manager — coordination, procurement, prequal | High |
| Hesham Abdelhameed | Design submittals, daily reports, material boards | High |
| Soliman Obiya / Shihab Mohamed | Rawasin (AV/IT subcontractor) — proposals, prequal | Medium |
| Aconex Notification | CDE transmittals — document submissions | Medium |
| Amro Mohammed | MEP — material lists, technical | Medium |
| Ali Abdelrahman | RFQ, procurement, ceiling systems | Medium |
| Mohammed Ahmed | Safety — lookahead reports | Medium |
| Mohammed Elshaikh | Plans (PEP, recovery plans) | Medium |

## Pitfalls

- **Check emails before repo edits** — PM instructions, CG comments, or deadlines in email may change what files need updating. Always scan first.
- **Epoch verification is mandatory** — run the Step 0 query every session. The DB may have been rebuilt with a different epoch.
- `Message_NormalizedSubject` comparison is case-sensitive — use `LIKE '%keyword%'`
- `Message_TimeReceived` epoch varies — verify with `datetime(col + 978307200, 'unixepoch')` (Mac absolute) vs `datetime(col, 'unixepoch')` (Unix)
- AppleScript `.applescript` files have ~700-byte body limit — use short scripts or bash loop with `osascript -e` one-liners
- OneDrive paths cause EDEADLK on reads — use `/tmp/` for staging, then `shutil.copy2()`
- **Use Python `shutil.copy2()` for file routing**, not terminal `cp` — OneDrive paths with parentheses, spaces, and special chars break bash quoting
- **`execute_code` is blocked in cron mode** — write the script to `/tmp/` with `write_file` first, then run `python3 /tmp/script.py` via terminal. The `-c "..."` one-liner pattern breaks on multi-line scripts with imports, quotes, and error handling. The write-then-run pattern is the canonical cron-mode approach.
- `write_file` tool bypasses OneDrive lock for writes — prefer it over direct file ops
- **Duplicate attachments** (same file from different senders) — route both to same destination; don't deduplicate unless exact byte match confirmed
- **Aconex notification emails** have no attachments and no email address — filter by `Message_SenderList LIKE '%Aconex%'`
- **Non-project emails to filter out**: Saudi Wood Expo, Instagram, Cognito Forms, Bluebeam Events, Power Automate reminders, FJDynamics webinars, visitor registration, car/vehicle requests, ERP notifications (salary, tickets, leave, POs), SharePoint link notifications
- **Review log format**: Save to `~/aseer-museum-pm/03_Plans/08_Risk/reviews/email_scan_YYYY-MM-DD.md` with YAML frontmatter, summary, key findings table, Aconex transmittals list, filtered-out items count, and registers-updated section
