# CG Submission Plan — From Email Attachments to Excel

After extracting project email attachments, the next step is often producing a **structured submission plan** for the Consultant/PMC. This reference documents the workflow used for Aseer Museum (Jun 2026).

## When to Use

- You've received multiple deliverable files via email (drawings, specs, samples, submittals)
- Some need to be submitted to CG/PMC for formal review
- You need a structured Excel plan mapping each file to schedule items

## Workflow

### Phase 1 — Identify CG-worthy emails

Filter for emails containing actual deliverables (not ops/logistics/invoices unless they're submittal-related):

```sql
SELECT m.Record_RecordID, datetime(m.Message_TimeReceived, 'unixepoch', 'localtime'),
       f.Folder_Name, m.Message_SenderList, m.Message_NormalizedSubject,
       m.Message_HasAttachment, substr(m.Message_Preview, 1, 300)
FROM Mail m JOIN folders f ON m.Record_FolderID = f.Record_RecordID
WHERE f.Folder_Name = '<ProjectFolder>'
  AND date(m.Message_TimeReceived, 'unixepoch') >= date('now', '-X days', 'localtime')
ORDER BY m.Message_TimeReceived DESC;
```

### Phase 2 — Extract attachment metadata (AppleScript)

Before downloading everything, catalog what each email has:

```applescript
tell application "Microsoft Outlook"
    set theMsg to message id <ID>
    set atts to (every attachment of theMsg)
    repeat with att in atts
        set attName to name of att
        set attType to content type of att
        log attName & " (" & attType & ")"
    end repeat
end tell
```

This tells you which emails have actual submittal PDFs vs. signature images vs. WeTransfer links.

### Phase 3 — Classify items into submission categories

Group extracted files into batches:

| Batch | Description |
|-------|-------------|
| **Batch 1 — For CG Submission** | New deliverables from subconsultants that need formal CG approval. Includes: drawings, specs, samples, method statements |
| **Batch 2 — Information/Record** | Meeting minutes, reports, admin docs — file only, no CG action |
| **Batch 3 — CG Responses** | Incoming CG reviews (Code A/B/C) — address comments, file in CG_Responses/ |
| **Batch 4 — Pending/Follow-up** | Overdue items, missing deliverables, pending responses — escalate |

### Phase 4 — Cross-reference against existing schedule

Map each item to an existing schedule row (if one exists):

| Email File | Schedule Ref | Matching Criteria |
|------------|-------------|-------------------|
| NRS DD drawings (DIS sheet) | DD-02 through DD-19 | Drawing number range, producer = NRS |
| GH Showcase back panel | DD-15 | Showcase drawings |
| Brass sample datasheets | MS-04 | Material submittal — showcases |
| MEP design scope docs | DD-24A→E | MEP design deliverables |

Check the existing Deliverables Submission Schedule (usually `*Deliverables_Submission_Schedule*.xlsx`) for matching items. New items (not in the schedule) should be flagged as new.

### Phase 5 — Build the Excel submission plan

Use openpyxl with a structured 2-sheet format:

**Sheet 1: Submission Plan**
Columns: #, Schedule Ref, Deliverable Description, Received From, Date Received, Files Attached, Status/Action Needed, Route to CG

Color coding:
- Header: dark blue (#2F5496) white font
- Section headers: light blue (#D6E4F0) — one per batch
- Received/Action: green fill (#E2EFDA)
- Overdue/Missing: red fill (#FCE4EC)
- Pending/Waiting: yellow fill (#FFF3CD)

**Sheet 2: File Manifest**
Columns: #, Filename, Size, Source Email, Linked Schedule Item

Add a note row at the bottom flagging:
- Files stored at staging path
- WeTransfer links that need manual download
- Expiry dates

### Phase 6 — Stage files to project folder

Copy extracted attachments to project location:

```
02_Submittals/<Date>_Batch/
```

Use a prefix pattern for filename sorting: `01_LG_Floor_`, `02_Basement_`, `03_Submittal13_`, etc.

## Pitfalls

- **WeTransfer links** — The browser/sandbox environment often can't access WeTransfer (timeout, CSP blocks). Extract the links and tell the user to download manually. The DIS/cover-sheet PDF attachments are often just transmittals; the actual files are behind the links.
- **Schedule references change** — The existing schedule v1/v2/v3 may have different item numbers. Always read the latest version and note which schedule version you're referencing.
- **Not all attachments are submittals** — Filter out: signature images (image001.png), invoices (unless they're submittal-related), Sharepoint notification emails, automated reminders.
- **CG responses are inbound, not outbound** — Code A/B/C emails from CG are responses to previous submissions, not new submissions. File in `02_CG_Responses/`, flag for user action, but don't route to CG again.

## Required Tools

- AppleScript (Outlook Automation for attachment extraction)
- Python + openpyxl (for Excel generation)
- pdftotext (poppler — for reading PDF contents to identify drawing numbers, codes)
