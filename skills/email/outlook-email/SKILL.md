---
name: outlook-email
description: Search Microsoft Outlook emails via SQLite database on macOS and extract attachments using AppleScript.
tags:
  - outlook
  - email
  - sqlite
  - applescript
  - attachments
  - macos
---

# Outlook Email Management on macOS

Search, filter, and extract attachments from Microsoft Outlook on macOS using its local SQLite database and AppleScript automation.

## Trigger

User asks to:
- Triage their inbox / review what's waiting / find action items
- Find emails from a specific sender or project
- Search for project-related emails
- Extract attachments from Outlook

## Database Location

**Note:** The user may be using OneDrive for Outlook storage. If the database is not found in the standard location, check:
- `~/OneDrive/Work/Samaya/Tenders/` or similar OneDrive paths for Outlook-related files.
- Manually inspect `/Applications/Microsoft Outlook.app` to verify Outlook installation and profile setup.

If the user has a custom Outlook profile path, the database may be stored elsewhere. **Always verify the correct profile path before querying.**

Only one account (sultan@samayainvest.com) — no account filtering needed.

### Database Location Reference

For troubleshooting, see `references/outlook-one-drive-paths.md` for possible database locations and troubleshooting steps.

Only one account (sultan@samayainvest.com) — no account filtering needed.

## Key Tables & Columns

### Folders table

| Column | Type | Description |
|--------|------|-------------|
| `Record_RecordID` | INTEGER | Folder ID (referenced by Mail.Record_FolderID) |
| `Folder_Name` | TEXT | Folder display name (Inbox, Sent Items, Asher Regional Museum, etc.) |
| `Folder_ParentID` | INTEGER | Parent folder ID for nested folders |
| `Folder_FolderType` | INTEGER | 1=Inbox, 3=Contacts, 4=Calendar, 5=Notes, 6=Tasks, 8=Sent, 9=Deleted, 10=Drafts, 12=Junk, 15=Archive, 99=root container |
| `Folder_SpecialFolderType` | INTEGER | Non-zero for special folders (e.g. 111=Birthdays/Calendar) |

**Pitfall: Mail table spans ALL folders.** Querying `Mail` without joining `folders` on `Record_FolderID` returns emails from Inbox, Sent Items, Archive, project sub-folders, etc. — everything mixed together. **Always JOIN with folders** so the user knows where each message lives.

### Mail table

| Column | Type | Description |
|--------|------|-------------|
| `Record_RecordID` | INTEGER | Unique email ID (use with AppleScript `message id`) |
| `Message_SenderList` | TEXT | Display name of sender |
| `Message_SenderAddressList` | TEXT | Email address of sender |
| `Message_NormalizedSubject` | TEXT | Email subject line |
| `Message_TimeReceived` | INTEGER | **Epoch varies by DB.** Some Outlook DBs use Mac absolute time (seconds since 2001-01-01), others use standard Unix epoch. **Always verify first:** `SELECT Message_TimeReceived, datetime(Message_TimeReceived, 'unixepoch', 'localtime') as as_unix, datetime(Message_TimeReceived + 978307200, 'unixepoch', 'localtime') as as_mac FROM Mail ORDER BY Message_TimeReceived DESC LIMIT 1;` — the one showing today's date is correct. If `as_unix` is correct, use `datetime(col, 'unixepoch')`. If `as_mac` is correct, use `datetime(col + 978307200, 'unixepoch')`. |
| `Message_HasAttachment` | BOOLEAN | 1 = has attachments, 0 = no attachments |
| `PathToDataFile` | TEXT | Relative path to `.olk15Message` file (proprietary — use AppleScript instead) |

### Quick Read Email (canonical first query)

When you need to read an email, start with this — gets preview, folder context, and attachment status in one shot:

```sql
SELECT m.Record_RecordID as id,
       datetime(m.Message_TimeReceived, 'unixepoch', 'localtime') as received,
       f.Folder_Name as folder,
       m.Message_SenderList as sender,
       m.Message_SenderAddressList as email,
       m.Message_NormalizedSubject as subject,
       substr(m.Message_Preview, 1, 500) as preview,
       m.Message_HasAttachment as att
FROM Mail m
JOIN folders f ON m.Record_FolderID = f.Record_RecordID
WHERE m.Record_RecordID = <ID>;
```

The `Message_Preview` column holds the first ~500 chars of the email body — enough to understand the purpose. For longer bodies, try AppleScript (`properties of theMsg` — requires Accessibility permissions).

### Useful query patterns

```sql
-- LIST RECENT EMAILS ACROSS ALL FOLDERS (canonical — always join folders)
SELECT m.Record_RecordID as id,
       datetime(m.Message_TimeReceived, 'unixepoch') as received,
       f.Folder_Name as folder,
       m.Message_SenderList as sender,
       m.Message_NormalizedSubject as subject,
       m.Message_HasAttachment as att
FROM Mail m
JOIN folders f ON m.Record_FolderID = f.Record_RecordID
ORDER BY m.Message_TimeReceived DESC
LIMIT 15;

-- Filter by specific folder
...WHERE f.Folder_Name = 'Inbox'

-- Count per folder
SELECT f.Folder_Name, COUNT(*) as count
FROM Mail m JOIN folders f ON m.Record_FolderID = f.Record_RecordID
GROUP BY f.Folder_Name ORDER BY count DESC;

-- Find by sender
SELECT Record_RecordID, datetime(Message_TimeReceived, 'unixepoch') as received,
       Message_NormalizedSubject, Message_HasAttachment
FROM Mail
WHERE Message_SenderAddressList LIKE '%email@domain.com%'
ORDER BY Message_TimeReceived DESC;

-- Today's emails (local timezone)
SELECT Record_RecordID, datetime(Message_TimeReceived, 'unixepoch') as received,
       Message_NormalizedSubject, Message_HasAttachment
FROM Mail
WHERE date(Message_TimeReceived, 'unixepoch') = date('now', 'localtime')
ORDER BY Message_TimeReceived ASC;

-- Filter by attachment only
... AND Message_HasAttachment = 1

-- Filter by subject keywords (Arabic or English)
... AND Message_NormalizedSubject LIKE '%project%'

-- Combined: project doc codes + attachments
SELECT Record_RecordID, datetime(Message_TimeReceived, 'unixepoch'),
       Message_SenderList, Message_NormalizedSubject
FROM Mail
WHERE Message_NormalizedSubject LIKE '%MOC-MUS-ASE%'
  AND Message_HasAttachment = 1
ORDER BY Message_TimeReceived DESC;

-- Build team contact index for a project
SELECT DISTINCT m.Message_SenderList as sender,
       m.Message_SenderAddressList as email
FROM Mail m
JOIN folders f ON m.Record_FolderID = f.Record_RecordID
WHERE f.Folder_Name = 'Asher Regional Museum'
ORDER BY m.Message_SenderList;

-- Get email activity summary by person (last 90 days)
SELECT m.Message_SenderList as sender,
       m.Message_SenderAddressList as email,
       COUNT(*) as emails,
       MAX(datetime(m.Message_TimeReceived, 'unixepoch')) as last_email
FROM Mail m
JOIN folders f ON m.Record_FolderID = f.Record_RecordID
WHERE f.Folder_Name = 'Asher Regional Museum'
  AND m.Message_TimeReceived >= strftime('%s', 'now', '-90 days')
GROUP BY m.Message_SenderAddressList
ORDER BY COUNT(*) DESC;

-- Get columns
PRAGMA table_info(Mail);
```

### Workflow: search before concluding

When investigating **why a project folder exists** (e.g. a Plans & Procedures sub-folder like `02.17_Risk_Management_Plan`):
1. First search Outlook by subject keyword (`Risk Management`, doc code, etc.)
2. Then search by sender (e.g. CG consultants: `hmabrouk@cg.com.sa`, `Hesham.a@samayainvest.com`)
3. Only then conclude "no matching attachments exist" — the user created the folder because they received relevant documents on email.

### Email Recipient Analysis (To vs CC)

```sql
SELECT m.Message_ToRecipientAddressList as to_list,
       m.Message_CCRecipientAddressList as cc_list
FROM Mail m
WHERE m.Record_RecordID = <ID>;
```

### Cross-Referencing Email Requests Against Approved Plans

1. Check the email's To/CC lists from SQLite
2. Look up the project's approved Communication Plan (search `PL-0018`)
3. The plan defines: item type → From party → To party → Review/Approval → Reply time
4. If the email's routing doesn't match the plan, flag it — but first verify facts from the DB, not from preview text

See `references/cg-correspondence-analysis.md` for cross-referencing CG requests against the approved Communication Plan.
See `references/forwarded-document-analysis.md` for the thread-first workflow when the user forwards a document.
See `references/cg-schedule-extraction.md` for extracting CG consultant schedule requirements from email chains.

### Pitfalls

**Cross-folder search for supplier replies.** Do NOT limit the search to the project's main folder. Supplier replies may be filed under a DIFFERENT project folder. Always use a cross-folder SQL query.

**macOS TCC blocks SQLite access intermittently.** Always try SQLite first. If it fails, fall back to AppleScript.

**`every folder` AppleScript command fails.** Use `(every message of inbox)` for Inbox scanning, or target specific project folders by name.

**`folder "Name" of inbox` may fail with error -10006.** Workaround: iterate directly without assignment: `repeat with f in (every mail folder of inboxN)`.

**`mail folder id <N>` is more reliable than `folder "Name" of inbox`.** Discover the numeric ID first, then use `every message of mail folder id <N>`.

**Multiple Inbox folders exist (one per account).** Use `get id of every mail folder whose name is "Inbox"` to discover all Inbox IDs.

**`sender` returns a Mail Recipient record, not a string.** Always wrap in a try block with `as text` coercion.

**`sender` returns blank via `osascript -e` one-liners.** Use a short `.applescript` file on disk for sender extraction.

**`plain text content` works reliably for Inbox messages, may fail for sub-folders.**

**`PathToDataFile` returns %20-encoded paths.** Use `$'...'` bash quoting or Python `urllib.parse.unquote`.

**AppleScript `.applescript` files have a ~700-byte script body limit.** Keep scripts short. Break into multiple small files.

**Most reliable pattern: bash `for` loop with individual `osascript -e` one-liners per property.**

**`has attachment` returns empty string via `osascript -e` one-liners.** Use a `.applescript` file for reliable attachment detection.

**`read status` filtering is unreliable.** Scan all inbox messages and present the most recent N.

**`time received` returns a formatted date string.** Parse with `date -j -f "%A, %d %B %Y at %I:%M:%S %p"` on macOS.

**Inbox message ordering is oldest-first (CRITICAL).** Message index 1 is the **newest** message. This applies to ALL folders.

### CG Deadline Assessment — "Possible or Not" Verdict Style

1. **Lead with the verdict.** First sentence: "POSSIBLE" or "NOT POSSIBLE — only X of Y items."
2. **Show the numbers.** How many items meet vs miss the deadline. Use a table with dates.
3. **Explain the blocker.** One-sentence root cause.
4. **Propose mitigation.** 3-5 bullet actions.
5. **Update the Excel.**

Do NOT give a hedging answer ("it depends", "maybe", "let me analyze further").

### Register Log Cross-Referencing

1. Load the log with `openpyxl`, extract MOC document numbers, status codes (A/B/C/D), and dates
2. Map each log entry to the submission plan by matching discipline + description keywords
3. Translate CG codes: A=Approved, B=Approved w/Comments, C=Revise & Resubmit, D=Rejected
4. Update status, actual date, and remarks on the matched submission plan row
5. Scan for stale serial date values leaking into the Actual Date column

See `references/register-log-reconciliation.md` for the complete workflow.

### Aconex / Oracle C&E Browser Access

**Aconex notification emails** are system-generated (sender `Aconex Notification`) with no email address — query `Message_SenderList LIKE '%Aconex%'`.

**Login:** Navigate to `https://constructionandengineering.oraclecloud.com/ui/v1/login`

**OneDrive file management (macOS):**
- `mv` (rename within same OneDrive directory) works — it's a metadata-only operation
- Direct `cp`/write to OneDrive paths can cause EDEADLK
- Stage large archives to /tmp first with `unzip`, then `mv` to OneDrive target

**WeTransfer / cloud-link attachments are NOT downloadable from this environment.** Flag to the user for manual download.

**Verify recipient claims from the DB, not from preview or inference.** Always query `Message_ToRecipientAddressList` and `Message_CCRecipientAddressList`.

**`Message_Preview` is truncated; full body extraction is fragile.** Use AppleScript via `plain text content of msg`.

**Timezone: always use 'localtime' for filtering.**

### Reading DOCX contract attachments

```bash
textutil -convert txt -stdout /path/to/contract.docx
```

For structured extraction, parse `word/document.xml` directly with Python (zipfile + ElementTree).

**Worked pattern for contract review:**
1. Extract attachments by email ID (AppleScript, skip `image/*`)
2. Identify the `.docx`/`.pdf` contract file
3. Convert/read with `textutil` or Python XML parse
4. Extract key articles by searching for `ARTICLE N` paragraphs
5. Build a findings table: scope, fees, payment terms, programme, liability/insurance caps, IP, termination, governing law
6. Flag blank placeholders and mismatches
7. Note any scope expansions

### Email thread analysis (PREFERRED — Conversation_ConversationID)

Outlook's `Conversation_ConversationID` column groups every message in a thread. Two-step pattern:

```sql
-- Step 1: Find one email in the thread
SELECT Record_RecordID FROM Mail
WHERE Message_NormalizedSubject LIKE '%Visualization Package%' LIMIT 1;

-- Step 2: Get the full conversation
SELECT m.Record_RecordID, datetime(m.Message_TimeSent, 'unixepoch', 'localtime') as sent,
       m.Message_SenderList as sender, m.Message_HasAttachment as att,
       substr(m.Message_Preview, 1, 300) as preview
FROM Mail m
WHERE m.Conversation_ConversationID = (
    SELECT Conversation_ConversationID FROM Mail WHERE Record_RecordID = <ID>
)
ORDER BY m.Message_TimeSent;
```

See `references/email-thread-analysis.md` for a complete worked example.
See `references/email-chain-tracing.md` for tracing forwarded email chains (FW:).
See `references/cg-email-triage.md` for CG consultant response scanning.
See `references/email-triage-pattern.md` for the complete inbox review workflow.
See `references/submission-plan-and-schedule-workflow.md` for building CG submission plans from email data.

## Vendor Email Extraction → Repo Filing Workflow

When the user asks to "check all emails related to [vendor]" and then "read all attachments":

1. **Phase 1 — Discovery**: Query SQLite with multiple LIKE patterns covering the vendor's name, email domains, and subject keywords. Always JOIN folders. Always use 'localtime'.

2. **Phase 2 — Present results**: Table with id, date, folder, sender, subject (English only), attachment flag. Identify key contacts from the vendor's email domain.

3. **Phase 3 — Extract attachments**: Write individual .applescript files per email ID (one per file, under the ~700-byte limit). Run in batches of 3-5 via osascript. Skip image/* content types. Save to /tmp/<vendor>_attachments/.

4. **Phase 4 — Read & classify**: Use textutil for .docx, pdftotext for .pdf, openpyxl for .xlsx. Identify: signed agreements, SOW documents, submission plans, CVs, certificates, pricing proposals.

5. **Phase 5 — File to repo (3-layer system)**: Create three parallel structures per vendor:
   - `03_Scope/<Vendor>/README.md` — SOW summary + all source documents (agreements, SOW PDFs, CVs, certs)
   - `02_Schedule/<Vendor>/README.md` — submission plan with dates, gates, deliverables table
   - `Technical_Office/Submission_Tracker/<Vendor>/README.md` — live submission log with planned vs actual dates
   Before creating, check existing registers (`01_Registers/subcontractor_sow_raci_register.md`, `01_Registers/subcontractor_package_register.md`, `03_Plans/15_Subcontractor_Deliverables/`) — link into them rather than building parallel systems. The repo already has a SOW control system; use it.

6. **Phase 6 — Update registers**: Update `specialist_register.md` with SOW/Plan column refs showing folder paths. Update `PROJECT_MEMORY.md` with file paths. Update `01_Registers/subcontractor_sow_raci_register.md` and `01_Registers/subcontractor_package_register.md` with repo file paths.

7. **Phase 7 — Master tracker**: Create/update `Technical_Office/Submission_Tracker/README.md` showing all specialists' SOW/Plan/Tracker status with priority actions. This is the single source of truth for all 27+ specialist packages.

## Hard Rules (apply to every response)

**ZERO Arabic in any output.** All subject lines, sender names, folder names, file names, and email body excerpts must be presented as concise English descriptions only. No raw Arabic text, no Arabic in parentheses, no mixed-language lines. This is a hard rule — applies to every email listing, summary, and document analysis. Even when the DB returns Arabic sender names or subjects, translate them silently before display.

**Always show folder context.** Every email listing MUST JOIN with `folders` table and display the folder name. Without it, the user cannot tell which messages are in Inbox vs project-specific sub-folders.

**Filter out ops/logistics from digests.** Silently skip: car/vehicle requests, material shipments, rest house/rental arrangements, technician transport, promotional/conference invitations. Only flag project-critical items (document submittals, contract actions, consultant deliverables, vendor approvals, CG correspondence, inspection requests, CVs, schedules, safety reports, PO requests, task assignments).

## Extracting Attachments — AppleScript (PREFERRED)

Outlook stores attachments inside proprietary `.olk15Message` files. **Always try AppleScript first.**

### Key technique: `touch` before `save`

```applescript
set savePath to "/path/to/destination/filename.xlsx"
do shell script "touch " & quoted form of savePath
set saveFile to POSIX file savePath as alias
save att in saveFile
```

### Working with message IDs

The `Record_RecordID` from SQLite maps directly to AppleScript's `message id`.

### Checking attachment types

```applescript
set attName to name of att
set attType to content type of att
set attSize to file size of att
```

### Full extraction script template

```applescript
set baseFolder to "/path/to/output/folder/"
do shell script "mkdir -p " & quoted form of baseFolder

tell application "Microsoft Outlook"
    set emailIds to {34500, 33140}
    set savedCount to 0

    repeat with eid in emailIds
        set eidVal to (eid as integer)
        try
            set theMsg to message id eidVal
            set atts to (every attachment of theMsg)

            repeat with att in atts
                set attName to name of att
                set savePath to baseFolder & eidVal & "_" & attName
                do shell script "touch " & quoted form of savePath
                set saveFile to POSIX file savePath as alias
                save att in saveFile
                set savedCount to savedCount + 1
            end repeat
        end try
    end repeat
    return "Saved: " & savedCount & " files"
end tell
```

### Batch extraction (bash + osascript heredoc)

```bash
#!/bin/bash
for id in 35001 35002 35003; do
  osascript <<EOF
tell application "Microsoft Outlook"
    set theMsg to message id $id
    set atts to (every attachment of theMsg)
    set outFolder to "/tmp/outlook_extracts/"
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
echo "DONE"
```

### Safer alternative — write .scpt file first

When the AppleScript contains special characters (`&`, quotes, Unicode) that break heredoc parsing, write the .scpt file first, then run with `osascript`.

### Alternative: .sh generator script (cron-safe, no `&` in terminal command)

Write a `.sh` script that uses `cat > file <<SCRIPTEND` to generate `.applescript` files. The `&` operators are inside the heredoc body, not in the terminal command itself.

### Filtering images vs documents

```applescript
set attType to content type of att
if attType does not start with "image/" then
    -- save document
end if
```

| Content type | Classification |
|---|---|
| `image/jpeg`, `image/png`, `image/gif` | Inline signature/email images — usually skip |
| `application/pdf` | Document — save |
| `application/vnd.ms-excel` | Excel (.xls) — save |
| `application/vnd.openxmlformats-officedocument.spreadsheetml.sheet` | Excel (.xlsx) — save |
| `application/vnd.openxmlformats-officedocument.wordprocessingml.document` | Word (.docx) — save |

### Email Reading (no attachments)

```applescript
tell application "Microsoft Outlook"
    set theMsg to message id 12345
    set msgProps to properties of theMsg
    return msgProps
end tell
```

## Creating Draft Emails in Outlook

Use `make new outgoing message` (NOT `make new draft message`).

**User preference: provide text for manual copy, not Outlook drafts.** Provide the text directly in your reply for them to review and copy. Do not create an Outlook draft unilaterally.

**User preference: list format over tables in email drafts.** Use a simple numbered list (1. 2. 3.) — not an HTML table. Reserve tables for Excel deliverables only.

**User preference: concise email drafts — no preamble.** Present only the email body text. No introductory explanation, no commentary.

## Batch Email Processing with Sub-Agents

For processing many project emails (10+), delegate individual emails to sub-agents in parallel batches of 3.

**Routing by doc code convention** (Aseer Museum example):

| Discipline Code | Discipline |
|----------------|------------|
| 1A0 | Architecture |
| 1C0 | Civil |
| 1E0 | Electrical |
| 1KH | HSE |
| 1K0 | General/Multi |
| 1M0 | Mechanical |
| 1KN | Security/ICT |

| Doc Type | Destination Folder |
|----------|-------------------|
| PL- (Plan) | `02_Plans_and_Procedures/02.{NN}_{Name}/` |
| ZD- (General) | Per discipline folder or `09_Correspondence/` |
| MS- (Method Statement) | `02_Plans_and_Procedures/02.15_Method_Statements/` |
| IR- (Inspection Request) | `Docs/03_Inspection_Requests/` |
| NC-/NCR (Non-Conformance) | `Docs/10_Test_and_Inspection/10.3_NCRs/` |
| SI-/JSI- (Site Instruction) | `Docs/05_SIs/05.1_Issued_by_CG/` |
| PQ- (Prequalification) | `Docs/09_Registers/27_Subcontractor_Prequalification_Register/` |
| MI- (Mobilization Items) | `02_Plans_and_Procedures/02.16_Mobilization_Plan/` |
| TQ- (Technical Query) | `Design Files/` per discipline |
| RP- (Report) | `Design Files/` per discipline |
| SC- (HSE Compliance) | `02.5_HSE_Plan/01_Source_Files/` |

### WeTransfer / cloud link handling

Cannot be auto-downloaded. Report exact links to the user for manual download.

### Project folder serial-number convention

Use consistent `NN_` prefix with underscore (not dash).

## Post-extraction: routing to project folders

Use Python (via `execute_code`) to handle Arabic names and special characters in paths.

### Route by project mapping

```python
import shutil, os

map = {
    "MOC-MUS-ASE-1KH-PL-0055.pdf": "Docs/02_Plans_and_Procedures",
    "ZAM-NWC-CTR-CLR-MEP-004_Rev.00.pdf": "Docs",
}

staging = "/tmp/outlook-attachments/aseer"
project_root = "/path/to/Aseer-Museum"

for fname, subdir in map.items():
    src = os.path.join(staging, fname)
    dst = os.path.join(project_root, subdir, fname)
    if os.path.exists(src):
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        shutil.copy2(src, dst)
```

### Categorize by doc code prefix

| Prefix | Project |
|--------|---------|
| `MOC-MUS-ASE` | Aseer Museum |
| `ZAM-NWC` or `ZAM-` | Zamzam Visitor Center |
| `AL JALAL`, `JALAL` | Al Galal & Al Gamal (Jabal Omar retail) |
| `MOC-ASEER-SIC` | Aseer Museum (alternate code) |

### BIM dedup with OneDrive EDEADLK

Use filename-only matching. See `references/onedrive-edeadlk.md`.

### Full dedup + routing reference

See `references/batch-email-routing.md`.

## Batch Email Pipeline (End-to-End Workflow)

### Phase 1 — Discovery
Query Outlook SQLite. Always JOIN folders table. Always use 'localtime'.

### Phase 2 — Extract Attachments (AppleScript batch)
Write a bash heredoc script that loops through email IDs.

### Phase 3 — Read & Route
Use `pdftotext` to extract text from PDFs, then route by document code pattern.

### Phase 3.5 — Produce CG Submission Plan
See `references/email-to-submission-plan.md`.

### Phase 4 — Cross-reference & Update
Update ALL relevant registers: Situation Reports, Master Submittal Register, Subcontractor Prequal Register, Lessons Learned Register, Odoo tasks, Memory.

### Phase 5 — Archive
Log the batch to `Email_Archive/_email_processing_log.md`.

### Phase 6 — Build / Update Submission Register
See `references/email-deliverables-to-submission-plan.md`.

## Direct Attachment Extraction (fallback — AppleScript is preferred)

See `references/olk15-attachment-parsing.md` for the file format specification.

## Reference files

- `references/batch-email-routing.md`
- `references/register-log-reconciliation.md`
- `references/exportmailin-analysis.md`
- `references/submission-plan-and-schedule-workflow.md`
- `references/email-thread-analysis.md`
- `references/cron-24h-email-scan.md`
- `references/olk15-attachment-parsing.md`
- `references/aconex-email-patterns.md`
- `references/email-to-submission-plan.md`
- `references/cg-schedule-extraction.md`
- `references/forwarded-document-analysis.md`
- `references/email-chain-tracing.md`
- `references/cg-email-triage.md`
- `references/cg-correspondence-analysis.md`
- `references/contract-review-from-email-attachment.md`
- `references/onedrive-edeadlk.md`
- `references/icloud-edeadlk-workaround.md`
- `references/email-deliverables-to-submission-plan.md`
- `references/email-triage-pattern.md`
- `references/cg-submission-plan-from-email.md`
- `references/cron-email-to-register-sync.md`
- `references/outlook-one-drive-paths.md`
- `references/tnef-utf16le-body-extraction.md`
- `references/sender-blank-one-liner.md`
- `references/subcontractor-email-protocol.md`
- `references/cg-crs-routing-to-specialists.md`
- `references/cg-deliverables-schedule-response.md`
- `references/meeting-agenda-workflow.md`
- `references/cg-data-package-forwarding.md`
- `references/aseer-email-processing-example.md`
- `references/batch-applescript-per-email.md`
- `references/ibrahim-shaaban-extraction-2026-06.md`
