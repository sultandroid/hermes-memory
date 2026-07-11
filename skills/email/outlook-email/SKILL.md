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
| `Message_TimeReceived` | INTEGER | Mac absolute time (seconds since 2001-01-01). Use `datetime(col + 978307200, 'unixepoch')` to convert — NOT `datetime(col, 'unixepoch')` which gives wrong dates (2057). |
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
... AND Message_NormalizedSubject LIKE '%متجر%' OR Message_NormalizedSubject LIKE '%project%'

-- Combined: project doc codes + attachments
SELECT Record_RecordID, datetime(Message_TimeReceived, 'unixepoch'),
       Message_SenderList, Message_NormalizedSubject
FROM Mail
WHERE Message_NormalizedSubject LIKE '%MOC-MUS-ASE%'
  AND Message_HasAttachment = 1
ORDER BY Message_TimeReceived DESC;

-- Build team contact index for a project
-- Find all unique senders from a specific project folder or by doc code prefix
SELECT DISTINCT m.Message_SenderList as sender,
       m.Message_SenderAddressList as email
FROM Mail m
JOIN folders f ON m.Record_FolderID = f.Record_RecordID
WHERE f.Folder_Name = 'Asher Regional Museum'  -- or: Message_NormalizedSubject LIKE '%MOC-MUS-ASE%'
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
1. First search Outlook by subject keyword (`Risk Management`, `خطة إدارة المخاطر`, doc code, etc.)
2. Then search by sender (e.g. CG consultants: `hmabrouk@cg.com.sa`, `Hesham.a@samayainvest.com`)
3. Only then conclude "no matching attachments exist" — the user created the folder because they received relevant documents on email.

### Email Recipient Analysis (To vs CC)

When you need to verify who an email was addressed TO vs CC'd (e.g., checking communication plan compliance):

```sql
SELECT m.Message_ToRecipientAddressList as to_list,
       m.Message_CCRecipientAddressList as cc_list
FROM Mail m
WHERE m.Record_RecordID = <ID>;
```

This returns semicolon-separated email addresses for each field. Useful for checking if key personnel were included before responding, or understanding routing compliance with Communication Plan matrices.

### Cross-Referencing Email Requests Against Approved Plans

When a CG/consultant email requests deliverables or action that touches communication routing:

1. Check the email's To/CC lists from SQLite (`Message_ToRecipientAddressList`, `Message_CCRecipientAddressList`)
2. Look up the project's approved Communication Plan (search `PL-0018` or `Project Communication Plan`)
3. The plan defines: item type → From party → To party → Review/Approval → Reply time
4. If the email's routing doesn't match the plan, flag it — but first verify facts from the DB, not from preview text
5. A sample workflow: CG requests deliverables → search approved plan matrix → identify correct submitter per matrix → route response accordingly

See `references/cg-correspondence-analysis.md` for cross-referencing CG requests against the approved Communication Plan — section references, routing validation, CG behavior patterns, and response approach.
See `references/forwarded-document-analysis.md` for the thread-first workflow when the user forwards a document and asks "what do they want from me" — trace Outlook thread before analyzing the PDF.
See `references/cg-schedule-extraction.md` for extracting CG consultant schedule requirements from email chains and building phased delivery schedules.

### Pitfalls

**macOS TCC blocks direct SQLite access.** Since macOS SIP + Transparency Consent & Control, `sqlite3` on `~/Library/Group Containers/UBF8T346G9.Office/Outlook/Outlook 15 Profiles/Main Profile/Data/Outlook.sqlite` returns "authorization denied" even via AppleScript's `do shell script`. This is NOT fixable with permissions grants — the sandbox is hard. **Always use AppleScript's Outlook object model** as the primary access method. Only SQLite fallback when AppleScript fails for a specific query.

**`every folder` AppleScript command fails.** `every folder` at the top level returns error -1728 ("Can't get every folder"). Use `(every message of inbox)` for Inbox scanning, or target specific project folders by name: `folder "Asher Regional Museum" of inbox` (the `of inbox` suffix is required). Do NOT attempt `(every folder)` iteration or `folder "Name"` standalone — both fail.

**`folder "Name" of inbox` may fail with error -10006.** When `folder "Name" of inbox` returns `Can't set subfolders to every mail folder of mail folder id N. (-10006)`, the `set` assignment is the problem — not the access itself. **Workaround:** iterate directly without assignment: `repeat with f in (every mail folder of inboxN)`. To get folder IDs reliably: iterate and capture `(name of f) & "|" & (id of f)`, then use `mail folder id <N>` for subsequent queries. This bypasses the `set` assignment error entirely.

**Multiple Inbox folders exist (one per account).** `mail folder "Inbox"` or `mail folder id 1` may return the wrong Inbox (empty or stale). Use `get id of every mail folder whose name is "Inbox"` to discover all Inbox IDs, then check `unread count of mail folder id <N>` to find the active one. The primary account's Inbox is often NOT id 1 — it can be id 114 or higher. Always verify before querying.

**`sender` returns a Mail Recipient record, not a string.** This applies to ALL senders, not just Aconex. Using `sender of m` directly in a string comparison crashes with error -1700. Always wrap in a try block with `as text` coercion or `name of senderRecord`:
```applescript
set senderName to ""
try
    set senderRecord to sender of m
    set senderName to (name of senderRecord) as text
end try
```

**`sender` returns blank via `osascript -e` one-liners.** When using the bash loop pattern (`osascript -e "tell application \"Microsoft Outlook\" to set sr to sender of message $i of ...; return name of sr"`), the sender name consistently returns empty string even though the message exists. This is a serialization quirk — the `sender` property's Mail Recipient record doesn't serialize to text in one-liner mode. **Workaround:** Use a short `.applescript` file on disk for sender extraction instead of inline `-e` one-liners. The file-based `osascript` call serializes the record correctly. See `references/sender-blank-one-liner.md` for the two-phase pattern (fast bash loop for subjects/times, file-based script for senders).

**`plain text content` works reliably for Inbox messages, may fail for sub-folders.** `plain text content of message N of inbox` returns the full email body for inbox messages. For messages in project sub-folders, archived messages, or very old emails, it may return `""` (empty string). When body is empty, fall back to subject + attachment analysis — don't try `properties of theMsg` which returns an unparseable record. The subject line and attachment names usually carry enough signal for triage purposes.

**Always show folder context.** Every email listing MUST JOIN with `folders` table and display the folder name. Without it, the user cannot tell which messages are in Inbox vs project-specific sub-folders.

**Arabic subject lines — translate on display, every time.** The user prefers English-only output. When Arabic subjects appear, present them with a concise English description (e.g. `طلب تصديق من الخارجية` → "Attestation request from Ministry of Foreign Affairs"). Do not show raw Arabic text. This applies to sender names and any other Arabic content in email output. Even if the subject was shown raw once, the user expects you to fix it immediately when called out — do not let it appear again in the same session.

**Filter out ops/logistics from digests.** When compiling an email summary/digest, silently skip operational and logistics emails: car/vehicle requests, material shipments, rest house/rental arrangements, technician transport, promotional/conference invitations. Only flag project-critical items (document submittals, contract actions, consultant deliverables, vendor approvals, CG correspondence, inspection requests, CVs, schedules, safety reports, PO requests, task assignments). This keeps the digest focused on what the user actually acts on.

**Mail table spans ALL folders implicitly.** Querying `Mail` without a `JOIN folders` on `Record_FolderID` returns everything (Inbox, Sent, Archive, project sub-folders) mixed together. The canonical query always uses `FROM Mail m JOIN folders f ON m.Record_FolderID = f.Record_RecordID` and includes `f.Folder_Name` in the SELECT. Without this, the user sees a jumbled list and can't tell which emails are actionable.

**`PathToDataFile` returns %20-encoded paths.** The `Message%20Attachments/` paths from the DB use URL-encoded spaces. On the filesystem, the actual directory is `Message Attachments/` (literal spaces). Use `$'...'` bash quoting or Python `urllib.parse.unquote` when resolving attachment paths.

**AppleScript `.applescript` files have a ~700-byte script body limit.** Scripts longer than ~700 bytes of AppleScript code (not comments) cause `Expected variable name or property but found class name (-2741)` at runtime. The parser chokes on large token streams. Workarounds:
  - **Keep scripts short.** Break into multiple small files (one per folder/query) and call `osascript` separately for each.
  - **Use `osascript -e` for one-liners** (no file at all) when the logic fits in a single line.
  - **Use `tell application "Microsoft Outlook" to get ...`** as a single-line `-e` expression for simple property reads (unread count, folder count, last message time).
  - **For complex multi-folder scans**, write a bash loop that calls a short `.applescript` per folder rather than one monolithic script.
  - **Variable name shortening** (single-letter vars, no `set ... to ...` where possible) helps fit more logic under the limit.
  - **`linefeed` vs `return`** — both work, but `linefeed` is one fewer character. Every byte counts.

**Most reliable pattern: bash `for` loop with individual `osascript -e` one-liners per property.** When the script body limit blocks multi-property scripts, use a bash loop that calls one `osascript -e` per property per message. Each call is a single-line expression that stays well under the limit:

```bash
for i in 1 2 3 4 5; do
  subj=$(osascript -e "tell application \"Microsoft Outlook\" to get subject of message $i of inbox" 2>/dev/null)
  att=$(osascript -e "tell application \"Microsoft Outlook\" to get has attachment of message $i of inbox" 2>/dev/null)
  echo "$i|$subj|$att"
done
```

This is slow (N calls × M messages) but **always works** when file-based scripts fail. The `2>/dev/null` suppresses errors from messages that don't exist. For 20 messages × 3 properties = 60 calls, expect ~30-60s runtime.

**`has attachment` returns empty string via `osascript -e` one-liners.** When called as `get has attachment of message N of inbox`, the property returns blank (not `true`/`false`/`1`/`0`). This is a macOS Outlook AppleScript quirk — the property exists but serializes as empty in one-liner mode. For reliable attachment detection, use a `.applescript` file (if under the byte limit) or extract all attachments unconditionally and filter by content type.

**`read status` filtering is unreliable.** Both `where unread is true` and `whose read status is not read` fail with errors (`The variable unread is not defined` / `Can't make application into type file`). There is no reliable AppleScript filter for unread messages. Workaround: scan all inbox messages and present the most recent N, letting the user identify what's new. The `unread count of inbox` property works (returns a number) but cannot be used as a filter predicate.

**`time received` returns a formatted date string.** `get time received of message N of inbox` returns a string like `date Saturday, 11 July 2026 at 1:48:57 AM` — not a Unix timestamp. Parse with `date -j -f "%A, %d %B %Y at %I:%M:%S %p"` on macOS.

**Inbox message ordering is oldest-first (CRITICAL).** When you iterate `(every message in mail folder id N)`, message index 1 is the **newest** message and index N is the **oldest**. This is the opposite of what most agents assume. Scanning the "last 100" messages by index (e.g. `repeat with i from n-99 to n`) returns the **oldest** emails, not the most recent. To find recent emails, scan from index 1 forward (e.g. `repeat with i from 1 to 100`). This applies to ALL folders, not just Inbox. The Asher Regional Museum folder (1257 messages) also follows this pattern: index 1 = newest (Apr 2024), index 1257 = oldest (Aug 2022).

### CG Deadline Assessment — "Possible or Not" Verdict Style

The user expects a clear yes/no answer when asked if a deadline is achievable. When assessing CG-mandated timelines:

1. **Lead with the verdict.** First sentence: "✅ POSSIBLE" or "❌ NOT POSSIBLE — only X of Y items."
2. **Show the numbers.** How many items meet vs miss the deadline. Use a table with dates.
3. **Explain the blocker.** One-sentence root cause (e.g., "IFC depends on DD approval; complex MEP DD approves 4-18 Aug → IFC needs +19-27 WD").
4. **Propose mitigation.** 3-5 bullet actions the user can take or propose to CG.
5. **Update the Excel.** Put the verdict in a dedicated sheet with rows color-coded green/red.

Do NOT give a hedging answer ("it depends", "maybe", "let me analyze further"). Analyze first, then deliver the verdict in the first paragraph.

### Register Log Cross-Referencing

When the user provides a Register Log Excel (from Aconex export or project register) to update the submission plan:

1. Load the log with `openpyxl`, extract MOC document numbers, status codes (A/B/C/D), and dates
2. Map each log entry to the submission plan by matching discipline + description keywords
3. Translate CG codes: A=Approved, B=Approved w/Comments, C=Revise & Resubmit (flag overdue), D=Rejected
4. Update status, actual date, and remarks on the matched submission plan row
5. Scan for stale serial date values leaking into the Actual Date column from column shifts

See `references/register-log-reconciliation.md` for the complete workflow with code tables and pitfalls.

### Aconex / Oracle C&E Browser Access

The user's project uses Oracle Construction and Engineering (Oracle Aconex) as the Common Data Environment (CDE). Access is via browser tools.

**Aconex notification emails** are system-generated (sender `Aconex Notification` or `Aconex Notification (Aseer Museum)`) with no email address — query `Message_SenderList LIKE '%Aconex%'` not `Message_SenderAddressList`. These are notification-only with no attachments. See `references/aconex-email-patterns.md` for sender format, transmittal naming conventions, volume patterns, and the epoch offset fix for SQLite timestamps.

**Login:**
- Navigate to `https://constructionandengineering.oraclecloud.com/ui/v1/login`
- Enter username → Next → Password → Sign In (two-step login flow)
- After login, the project lobby shows active projects

**Navigating to a project:**
- In the project list, click the project row to open it (the SPA loads an iframe)
- Once loaded, the top bar shows tabs: Home, Models, Documents, Mail, Field, Packages, Workflows, Directory, Insights, Setup

**Document Register:**
- Click Documents tab or the "Document Register" shortcut on the Home page
- The register loads inside an iframe (cross-origin — JavaScript access limited)
- Use browser_snapshot to see grid data; results may be truncated for large datasets
- Standard searches: "Approved", "Issued for approval", "Drawings modified today"
- Reset pinned filters if search returns no results (click "Reset pinned filters" button)

**Limitations:**
- Oracle Aconex is a heavy SPA; page loads are slow and sessions time out (~10 min)
- Document register content is inside a cross-origin iframe — bulk extraction is impractical
- Exporting via Reports → Excel is the preferred bulk data extraction method
- If export isn't available, ask the user to provide the Aconex export manually

**OneDrive file management (macOS):**
- `mv` (rename within same OneDrive directory) works — it's a metadata-only operation
- Direct `cp`/write to OneDrive paths can cause EDEADLK (resource deadlock)
- Stage large archives to /tmp first with `unzip`, then `mv` to OneDrive target
- Background extraction with `terminal(background=true, notify_on_complete=true)` for large zip files (1000+ files)

**WeTransfer / cloud-link attachments are NOT downloadable from this environment.** Design consultants frequently send deliverables via WeTransfer links (often 3-day expiry) instead of direct email attachments. The sandboxed browser and CLI cannot download these — WeTransfer requires client-side JavaScript and Auth0 authentication. When the email body contains a WeTransfer URL, flag it to the user as needing manual download. Do not attempt API-based download (WeTransfer returns 400/401 without JS session). Pattern: `https://we.tl/t-XXXXX` or `https://wetransfer.com/downloads/...`.

Post-download, the actual files are extracted via unzip/7z and filed to the project structure — see `references/email-deliverables-to-submission-plan.md`.

**Verify recipient claims from the DB, not from preview or inference.** The `Message_Preview` column truncates the email body and does not reliably show To/CC headers. Always query `Message_ToRecipientAddressList` and `Message_CCRecipientAddressList` before making claims about who an email was addressed to. Incorrect routing statements erode trust quickly.

**`Message_Preview` is truncated; full body extraction is fragile.** The SQLite `Message_Preview` column holds roughly the first ~500 chars of the email body (Outlook truncates it). The raw `.olk15Message` files use TNEF (winmail.dat) format internally — `strings` or direct text extraction rarely finds contiguous body text. AppleScript via `plain text content of msg` is the preferred way to get the full body. Use a `.applescript` file on disk rather than inline `osascript -e` to avoid quoting issues:

```bash
# Write to a temp file first (via write_file tool), then:
osascript /tmp/read_email.applescript
```

Script template (`read_email.applescript`):
```applescript
tell application "Microsoft Outlook"
    set msg to message id <ID>
    set msgContent to plain text content of msg
    return msgContent
end tell
```

This works even without explicit Accessibility permissions in many setups (the `do shell script` AppleScript context bridges permissions). The fallback, `properties of theMsg`, returns a structured record (not plain text) and is harder to parse. If even AppleScript fails (error **-1741**: "An error of type -1741 has occurred" = Outlook/Accessibility not granted), present what's available from `Message_Preview` and flag it as truncated. To grant: System Settings > Privacy & Security > Automation > allow Terminal/Agent to control Outlook.

**Timezone: always use 'localtime' for filtering.** The `datetime(col, 'unixepoch')` returns UTC. For today/this-week filters, always use `date('now', 'localtime')` to match the user's local timezone. Without `'localtime'`, date boundaries are misaligned (UTC vs AST/GMT+3).

### Email body via `strings` on `.olk15Message` files is unreliable.** The TNEF/winmail.dat format embeds body text as opaque blobs. `strings` with `-n 5` or higher misses most body content. Don't waste time trying to carve out email text from message files — use `Message_Preview` (truncated) or AppleScript (requires permissions) instead.

### Reading DOCX contract attachments

When the user asks to "check the contract" and the contract is a `.docx` attachment, extract it with AppleScript, then read it with macOS `textutil`:

```bash
textutil -convert txt -stdout /path/to/contract.docx
```

For structured extraction of specific articles/clauses, parse `word/document.xml` directly with Python (zipfile + ElementTree) — this preserves paragraph boundaries better than plain-text conversion for long legal documents with tables of contents.

**Worked pattern for contract review:**
1. Extract attachments by email ID (AppleScript, skip `image/*`)
2. Identify the `.docx`/`.pdf` contract file
3. Convert/read with `textutil` or Python XML parse
4. Extract key articles by searching for `ARTICLE N` paragraphs
5. Build a findings table: scope, fees, payment terms, programme, liability/insurance caps, IP, termination, governing law
6. Flag blank placeholders (`[ • ]`) and mismatches between numerals and words in fee clauses
7. Note any scope expansions that override the consultant's original limitations (e.g., "complete lighting control engineering" overriding "design intent only")

### Email thread analysis (PREFERRED — Conversation_ConversationID)

Outlook's `Conversation_ConversationID` column groups every message in a thread (replies, forwards, all senders). This is more reliable than subject matching — it's indexed, handles sub-thread variants, and catches cross-sender replies automatically.

**Two-step pattern:**

```sql
-- Step 1: Find one email in the thread
SELECT Record_RecordID FROM Mail
WHERE Message_NormalizedSubject LIKE '%Visualization Package%' LIMIT 1;

-- Step 2: Get the full conversation (use the ID from step 1)
SELECT m.Record_RecordID, datetime(m.Message_TimeSent, 'unixepoch', 'localtime') as sent,
       m.Message_SenderList as sender, m.Message_HasAttachment as att,
       substr(m.Message_Preview, 1, 300) as preview
FROM Mail m
WHERE m.Conversation_ConversationID = (
    SELECT Conversation_ConversationID FROM Mail WHERE Record_RecordID = <ID>
)
ORDER BY m.Message_TimeSent;
```

Use subject-based matching (`LIKE '%keyword%'`) only for **discovery** (finding candidate threads), then switch to `Conversation_ConversationID` to expand each thread.

See `references/email-thread-analysis.md` for a complete worked example comparing both techniques.
See `references/email-chain-tracing.md` for tracing forwarded email chains (FW:) where Conversation_ConversationID doesn't apply — subject-keyword discovery, reconstructing forward hops, understanding request intent at each level, and cross-referencing against project files.
See `references/cg-email-triage.md` for CG consultant response scanning.
See `references/email-triage-pattern.md` for the complete inbox review / action-items workflow — the phased query pattern and presentation format for "check my email, what's waiting for me."
See `references/submission-plan-and-schedule-workflow.md` for building/updating CG submission plans from email data — register log cross-referencing, design phase scheduling with review buffers, duplicate cleanup, and feasibility verdicts for CG's 4-category deliverables (DD, Material Submittals, IFC, Coordination).
See `references/register-log-reconciliation.md` for matching MOC document codes from Register Log Excel exports against the submission plan — status code translation, date handling, and pitfalls.

## Extracting Attachments — AppleScript (PREFERRED)

Outlook stores attachments inside proprietary `.olk15Message` files. **Always try AppleScript first** — the binary parsing of `.olk15MsgAttachment` files (see "Direct Attachment Extraction" below) is fragile: the `Mail_OwnedBlocks` table provides attachment UUIDs, but pairing them with the correct `.olk15MsgAttachment` file is unreliable. AppleScript via `osascript` is the only method that consistently works for all attachment types.

### Key technique: `touch` before `save`

AppleScript's `POSIX file path as alias` requires the destination file to **already exist**. Create it first with `touch`:

```applescript
set savePath to "/path/to/destination/filename.xlsx"
do shell script "touch " & quoted form of savePath
set saveFile to POSIX file savePath as alias
save att in saveFile
```

### Working with message IDs

The `Record_RecordID` from SQLite maps directly to AppleScript's `message id`:

```applescript
tell application "Microsoft Outlook"
    set theMsg to message id 34500
    set msgSubject to subject of theMsg
    set atts to (every attachment of theMsg)

    repeat with att in atts
        set attName to name of att
        -- save logic here
    end repeat
end tell
```

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

For mass extraction (50+ emails), the sub-agent approach serializes work. A faster pattern: write a bash script with heredoc osascript blocks, then run it. Each osascript invocation is a separate process, so a simple `for id in ...; do osascript <<EOF ... EOF; done` works reliably:

```bash
#!/bin/bash
# Save as /tmp/batch_extract.sh, then: bash /tmp/batch_extract.sh
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

This avoids the sub-agent overhead (context window, tool trace, iteration limits) for pure attachment extraction. After extraction, use Python/`execute_code` for the routing logic (pdftotext → identify → copy).

### Safer alternative — write .scpt file first

When the AppleScript contains special characters (`&`, quotes, Unicode) that break heredoc parsing (bash treats `&` as background operator, causing `Foreground command uses '&' backgrounding` errors), use this pattern instead:

1. **Write the .scpt file** using `write_file` tool (or `skill_manage action=write_file`):
   ```
   /tmp/extract_attachments.scpt
   ```

2. **Run with osascript**:
   ```bash
   osascript /tmp/extract_attachments.scpt
   ```

This bypasses heredoc quoting issues entirely. The .scpt is a proper AppleScript UTF-8 file with no shell interpolation.

### Filtering images vs documents

Most emails include signature images. To extract only non-image attachments:

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

For emails without attachments:

```applescript
tell application "Microsoft Outlook"
    set theMsg to message id 12345
    set msgProps to properties of theMsg
    return msgProps  -- gives headers, html, plain text content
end tell
```

**Pitfall: `content` and `plain text content` don't return plain text.** The `content` property returns a record (not a string), and `plain text content` may also fail if Accessibility permissions are not granted. The error looks like: `Can't make {name:"x", ...} into type Unicode text`. When this happens, rely on `Message_Preview` from SQLite (truncated) or use `properties of theMsg` to get the full object dump.

## Creating Draft Emails in Outlook

Use `make new outgoing message` (NOT `make new draft message` — that class doesn't exist in Outlook for Mac).

When drafting appointment/contract emails to subcontractors: reference their own SOW, not other contractors' scope. See `references/subcontractor-email-protocol.md`.

### Plain Text Draft

```applescript
tell application "Microsoft Outlook"
    set newMsg to make new outgoing message with properties ¬
        {subject:"Your Subject Here"}
    make new recipient at newMsg with properties ¬
        {email address:{address:"person@domain.com"}}
    make new cc recipient at newMsg with properties ¬
        {email address:{address:"ccperson@domain.com"}}
    set content of newMsg to "Email body text here"
end tell
-- Auto-saves as draft; no explicit save needed
```

### HTML Draft with Tables (Formal Style — Preferred)

For business emails requiring tables, use HTML body. **User preference: clean, formal, no brand colors** — use black text on white, simple gray borders (#999999), no navy/red/colored headers.

**Best pattern — write HTML to a file first, then read it in AppleScript.** This avoids escaping issues with special characters (£, &, quotes, Unicode) inside AppleScript strings:

```bash
# 1. Write HTML to a temp file (use write_file tool)
# /tmp/email_body.html

# 2. Read and create draft via one-liner osascript
osascript -e '
set htmlContent to do shell script "cat /tmp/email_body.html"
tell application "Microsoft Outlook"
    set newMsg to make new outgoing message with properties ¬
        {subject:"Subject Line"}
    make new recipient at newMsg with properties ¬
        {email address:{address:"to@domain.com"}}
    make new cc recipient at newMsg with properties ¬
        {email address:{address:"cc@domain.com"}}
    set content of newMsg to htmlContent
end tell
'
```

**HTML template** (formal style — clean, no colors):

```html
<html><body style='font-family:Calibri,Arial,sans-serif;font-size:11pt;color:#000000;'>
<p>Dear ...,</p>
<p>Paragraph text here.</p>

<p><b>Section Heading</b></p>
<table style='border-collapse:collapse;width:100%;font-size:10pt;'>
<tr><td style='padding:4px 8px;border:1px solid #999999;'><b>Col1</b></td><td style='padding:4px 8px;border:1px solid #999999;'><b>Col2</b></td></tr>
<tr><td style='padding:4px 8px;border:1px solid #999999;'>Value</td><td style='padding:4px 8px;border:1px solid #999999;'>Value</td></tr>
</table>

<p>Regards,<br/>Name</p>
</body></html>
```

**Style rules:**
- `font-family: Calibri, Arial, sans-serif` — standard business font
- `font-size: 11pt` — readable but compact
- `color: #000000` — black text, no colors
- Table borders: `1px solid #999999` — subtle gray, no colored headers
- No background fills on table rows (white only)
- Use `<b>` not `<h3>` for headings when max formal

**User preference: provide text for manual copy, not Outlook drafts.** When the user asks you to prepare an email response, provide the text directly in your reply for them to review and copy. Do not create an Outlook draft unilaterally. The user edits the wording before sending.

**User preference: list format over tables in email drafts.** When listing package contents or items in an email body, use a simple numbered list (1. 2. 3.) — not an HTML table. The user explicitly corrected this. Reserve tables for Excel deliverables only.

## Batch Email Processing with Sub-Agents

For processing many project emails (10+), delegate individual emails to sub-agents in parallel batches of 3. Each sub-agent handles: read body → extract attachments → read content → determine routing → save to project folder.

**Pattern:**
```sql
-- First: get the list of emails to process
SELECT Record_RecordID, datetime(Message_TimeReceived, 'unixepoch', 'localtime'),
       Message_SenderList, Message_NormalizedSubject, Message_HasAttachment
FROM Mail WHERE ... ORDER BY Message_TimeReceived;
```

Then: queue up to 3 sub-agents at a time via `delegate_task`. Pass each sub-agent:
- The email ID and sender
- The project base path
- The Outlook DB path
- Known routing rules (doc code → folder mapping)

The sub-agent should extract attachments using AppleScript (`osascript message id <ID>`), then read PDF content with `pdftotext`, determine routing, and copy files.

**Routing by doc code convention** (Aseer Museum example):

First, parse the doc code: `MOC-MUS-ASE-{disc}{num}-{type}-{seq}`

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

CG responses (Code B/C) go into `02_CG_Responses/` subfolder within the document's parent folder. Original submissions go in `01_Source_Files/`.

**Doc code routing details are project-specific.** The routing table below shows the Aseer Museum conventions as a worked example. For other projects, inspect the target project's folder structure first and extrapolate from the discipline prefix.

### WeTransfer / cloud link handling

Some emails use cloud file-sharing links (WeTransfer) instead of direct attachments. These cannot be auto-downloaded from the sandbox environment (browser timeout / curl limitations).

**If browser-navigate fails:** Report the exact links to the user for manual download. The user will download to `~/Downloads/` and then ask the agent to move/extract.

**Detection pattern:**
- WeTransfer links start with `https://we.tl/t-` and redirect to `https://wetransfer.com/downloads/{id}/{hash}`
- Emails may mention "link is only X days valid" — flag expiry
- Attachment data is behind the link; the direct Outlook `.olk15MsgAttachment` is just the email notification, not the actual files

**After user downloads:**
1. Examine archive contents (`unzip -l` or `7z l` for .7z)
2. Extract to the appropriate project folder using `unzip -o` directly to OneDrive path (writes work; only reads trigger EDEADLK)
3. For large extractions (thousands of files), use `terminal(background=true, notify_on_complete=true)` with generous timeout
4. Copy DIS cover sheets to `02_Submittals/<Date>_Batch/` for reference

**7z files:** Use `7z x file.7z -o/target/dir -y` (macOS: `brew install p7zip` or The Unarchiver).

### Project folder serial-number convention

The user organizes project sub-folders with `NN_name` serial prefix for logical grouping:

```
00_Scope_and_Proposals
01_AS_Pre-Appointment...
...
07_Architecture
...
23_Schedules_and_Logs
99_NRS_Drops_2026-04-05
```

When creating new folders or organizing existing ones, use consistent `NN_` prefix with underscore (not dash). Skip hidden/system folders (`_PREFIX` stays as-is). Rename within OneDrive using `mv` (rename is metadata-only, works on OneDrive).

## Post-extraction: routing to project folders

After downloading attachments to a staging folder (`/tmp/outlook-attachments/<project>/`), route each file to its correct project path. Use Python (via `execute_code`) to handle Arabic names and special characters in paths — bash quoting of these paths is fragile.

### Route by project mapping

```python
import shutil, os

# Define a mapping: filename → relative-subfolder
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

When routing to BIM folders on OneDrive (`~/Library/CloudStorage/OneDrive-*/Bim Unit/`), you **cannot read file contents** to deduplicate (all reads trigger EDEADLK). Use filename-only matching:

1. `find -type f` to list all filenames in target BIM subfolders (never tries to read content)
2. Python with Arabic normalization (`unicodedata.normalize('NFC', ...)`, Alef/Yeh mapping, diacritic stripping) for fuzzy matching
3. `difflib.SequenceMatcher` with ratio > 0.9 for `_1`/`_2` suffix variants

See `references/onedrive-edeadlk.md` → "BIM scanning workaround" for full Python implementation.

### Pitfall: BIM is deep — search ALL subfolders

Don't just check the direct target folder (e.g. `05_Correspondence_Archive/`). The BIM archive is organized into numbered subfolders like `02_Correspondence_MOC/`, `01_Plans_and_Reports/`. Use recursive `find` across the whole tree — a file may already be filed in a deeper subfolder you didn't scan.

### Full dedup + routing reference

See `references/batch-email-routing.md` for complete AppleScript + Python workflow.

## Batch Email Pipeline (End-to-End Workflow)

This is the recommended workflow for processing large volumes of project emails (50+ in a session):

### Phase 1 — Discovery
Query Outlook SQLite to find relevant emails. Always JOIN folders table. Always use 'localtime' for date filtering.

```sql
SELECT m.Record_RecordID, datetime(m.Message_TimeReceived, 'unixepoch', 'localtime'),
       f.Folder_Name, m.Message_SenderList, m.Message_NormalizedSubject
FROM Mail m JOIN folders f ON m.Record_FolderID = f.Record_RecordID
WHERE f.Folder_Name = 'Asher Regional Museum' AND m.Message_HasAttachment = 1
ORDER BY m.Message_TimeReceived ASC;
```

Display results in a table with English-only subject translations for Arabic.

### Phase 2 — Extract Attachments (AppleScript batch)
Write a bash heredoc script that loops through email IDs. Run it via `terminal(timeout=120)`:

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

Extracts all attachments including inline images. Filter out .jpg/.png/.gif in routing phase. Limits: ~100 per batch.

### Phase 3 — Read & Route
Use `pdftotext` to extract text from PDFs, then route by document code pattern. Use Python/execute_code for mass filing with shutil.copy2, mapping email ID prefixes to destination folders.

### Phase 3.5 — Produce CG Submission Plan (intermediate step)

After extracting and reading the content, build a structured submission plan mapping received deliverables to the project's existing Deliverables Submission Schedule. This tells the user what to submit to the Consultant (CG) next.

**When to do this:** User asks "make a submission plan" or "what do we submit to CG from these files."

**Steps:**
1. Classify each received item (design deliverable / material submittal / CG response / admin)
2. Read the existing Deliverables Submission Schedule Excel to find matching refs
3. Read Document Issue Sheets (DIS) via `pdftotext` to understand drawing package contents and purpose codes (I=Information, A=Approval)
4. Produce a 2-sheet Excel workbook: Sheet 1 = Submission Plan with color-coded batches, Sheet 2 = File Manifest
5. Copy extracted files to the project's dated submittals folder
6. Flag WeTransfer/cloud links, CG Code C/E replies, and overdue items in the delivery summary

See `references/email-to-submission-plan.md` for the full workflow with classification tables, mapping heuristics, DIS reading patterns, and pitfalls.

### Phase 4 — Cross-reference & Update
After filing, update:
1. **Situation Reports** — document status in _MANAGER_DASHBOARD/
2. **Master Submittal Register** (Excel) — Dashboard status cells
3. **Subcontractor Prequal Register** — log prequal submissions
4. **Odoo tasks** — create/update under correct package parent
5. **Memory** — key actionable findings (C-status docs, new submissions)

### Phase 4b — Optional: Create a CG Submission Plan (Excel)

When received attachments contain new deliverables for Consultant/PMC review, produce a structured Excel plan:

1. Classify items into 4 batches: For CG Submission / Information Only / CG Responses / Pending
2. Cross-reference each item against the project's existing Deliverables Submission Schedule
3. Build a 2-sheet Excel workbook (openpyxl): submission plan + file manifest
4. Stage extracted files to `02_Submittals/<Date>_Batch/`
5. Flag WeTransfer links for manual download (not auto-downloadable from sandbox)

See `references/cg-submission-plan-from-email.md` for the full workflow with AppleScript and openpyxl patterns.

### Phase 5 — Archive
Log the batch to `Email_Archive/_email_processing_log.md` with a summary table.

### Phase 6 — Build / Update Submission Register
After extraction and routing, update the project's submission plan with actual receipt dates, document codes, and status. See `references/email-deliverables-to-submission-plan.md` for the complete workflow — extracting DIS cover sheets, parsing drawing registers, cross-referencing against the existing submission plan, and filing deliverables to the correct project folders.

## Direct Attachment Extraction (fallback — AppleScript is preferred)

**AppleScript is faster and more reliable** than binary parsing for most cases. The batch heredoc pattern (above) can extract 50+ attachments in ~2 minutes. Only fall back to this method when AppleScript fails.

Fallback: extract attachments directly from the Outlook attachment cache by querying the Blocks/Mail_OwnedBlocks relationship in the SQLite database.

### Finding attachment file paths

```sql
-- Find attachment file paths for a specific email
SELECT hex(b.BlockID), b.BlockTag, b.PathToDataFile
FROM Blocks b
JOIN Mail_OwnedBlocks m ON m.BlockID = b.BlockID
WHERE m.Record_RecordID = <RECORD_ID>
ORDER BY m.BlockTag;
```

This returns paths like `Message%20Attachments/35/<UUID>.olk15MsgAttachment` relative to the Data/ directory.

### Extracting PDF from .olk15MsgAttachment files

The `.olk15MsgAttachment` files have a proprietary binary header (~285 bytes) followed by base64-encoded PDF content starting with `JVBER`:

```python
import base64, re

with open('file.olk15MsgAttachment', 'rb') as f:
    data = f.read()

# Find base64 PDF start
idx = data.find(b'JVBER')
if idx >= 0:
    b64_text = data[idx:].decode('ascii', errors='ignore')
    b64_clean = re.sub(r'[^A-Za-z0-9+/=]', '', b64_text)
    pdf_data = base64.b64decode(b64_clean)

    with open('output.pdf', 'wb') as out:
        out.write(pdf_data)
```

### Getting attachment metadata (filenames, types)

The file header (first ~285 bytes) contains metadata in plain text:
- `Content-type: application/pdf; name="filename.pdf";`
- `x-mac-creator=`
- `Content-ID:`
- **iCloud + OneDrive EDEADLK on cloud-only files** — macOS cloud storage providers (OneDrive File Provider and iCloud Drive) permanently lock files whose content hasn't been fully downloaded locally. The error `Resource deadlock avoided (EDEADLK)` appears on any read attempt: cp, ditto, rsync, tar, Python open, head, cat, hexdump, file. This affects BOTH:
  - OneDrive at `~/Library/CloudStorage/OneDrive-*/`
  - iCloud Drive at `~/Documents/` (when iCloud sync is active for Documents)
  
  On iCloud, `file` and `stat` commands also fail (unlike OneDrive where `stat` still works). AppleScript returns I/O error -36.
  
  Detect cloud-stub status: `mdls -name com_apple_provenance_isDownloaded <file>` (OneDrive) or check extended attrs.

  **Priority-ordered workarounds:**
  1. `osascript -e 'do shell script "python3 <script.py> 2>&1"'` — even from a fully locked directory, AppleScript's `do shell script` can execute Python scripts when direct shell access fails. Proven to work on both iCloud and OneDrive.
  2. `python3 <script.py>` — can execute cloud-stored `.py` scripts successfully even when `cat`/`head`/`file` commands fail on the same file. `wc -c` reads full size.
  3. `brctl download <path>` — forces the file to sync locally. Wait 1–2s, verify with `stat -f "%Sf" <path>` (output `-` when fully local).
  4. Delete-and-copy — `os.remove(target_path)` then `cp -X /tmp/source target`; deleting the existing stub removes the sync engine lock. For iCloud `~/Documents/` files, `rm -f` + `cp /tmp/source target` also works after `brctl download` to force local sync first.
  5. `cat <src> > /tmp/x && mv /tmp/x <dest>` — bypasses `fcopyfile` deadlock in `cp`. ⚠️ Only works for OneDrive files, NOT iCloud Drive dataless files (those silently produce 0-byte output).
  6. **Content-request via time-based detection** — when you cannot read file contents, use `find -ctime -1` (change time), `find -newermt "<date>"` (modification time), or `find -newer <reference_file>` to detect if new/changed files exist. Compare filenames against target BIM folders with `find ... -name "${base}*"` to determine if already filed, without needing to read file bytes.

  Last resort: write companion sidecar files to the same directory (write-to-cloud works when reads fail — write/read asymmetry).
  See `references/olk15-attachment-parsing.md` for the file format specification (magic bytes, header offsets, base64 boundaries).
  See `references/aseer-email-processing-example.md` for a complete worked example (batch processing, AppleScript extraction, Aseer document routing rules, email thread analysis, team contact indexing).
See `references/cg-email-triage.md` for the CG email analysis pattern (cross-referencing requests against approved plans, identifying routing inconsistencies, proposing response channels).

See `references/meeting-agenda-workflow.md` for the weekly meeting agenda workflow — extract open points from emails, group by project, format as Excel for PD meetings.
See `references/cg-deliverables-schedule-response.md` for constructing the response schedule when CG requests a Deliverables Submission Schedule — ownership matrix, schedule rules, phases, and Excel format.
See `references/contract-review-from-email-attachment.md` for the contract-review workflow when the user asks to "check the contract" from an Outlook email attachment — DOCX/PDF extraction, structured summary template, and red-flag checklist.
See `references/onedrive-edeadlk.md` for full diagnostics.
See `references/cron-24h-email-scan.md` for the autonomous cron-job pattern — 24h scan using AppleScript (since TCC blocks SQLite), project-critical filtering, emoji status reporting, SILENT protocol, and Aconex transmittal register update workflow.
See `references/icloud-edeadlk-workaround.md` for the iCloud EDEADLK workaround — `cat > /tmp/` for reads, `python3 /tmp/script.py` for writes, `osascript` bridge as fallback.
