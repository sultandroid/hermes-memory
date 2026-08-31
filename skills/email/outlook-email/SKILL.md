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

## Saving an attachment via AppleScript (POSIX file wrapper required)

To save an email attachment to disk:

```bash
osascript -e 'tell application "Microsoft Outlook"' \
  -e 'set m to message id <Record_RecordID>' \
  -e 'set att to first attachment of m' \
  -e 'set p to POSIX file "/tmp/out.pdf"' \
  -e 'save att in p' -e 'end tell'
```

**The `POSIX file` wrapper is REQUIRED.** `save att in "/tmp/out.pdf"` (plain string path) fails with error `-2700`. Get the attachment name first via `get name of every attachment of m`, then `pdftotext -layout /tmp/out.pdf -` to read it.

## Trigger

User asks to:
- Triage their inbox / review what's waiting / find action items
- Find emails from a specific sender or project
- Search for project-related emails
- Extract attachments from Outlook
- "check mail" / "check mails" / "check emails"
- "update repo" / "update registers" / "follow repo instructions"

## Mandatory First Step: Check Repo Pipeline

**When the user says "update repo" or "follow repo instructions", do NOT start with ad-hoc register edits.** The `aseer-museum-pm` repo has a document intake pipeline at `scripts/document_intake.py`. Run it first:

**User rule — "Always check GitHub issues and answer" (2026-08-15):** Before answering a project question or claiming a state, check the repo's open GitHub issues (`gh issue list --repo sultandroid/aseer-museum-pm --state open`). Open issues may already document a known gap, a pending request, or a decision the user expects you to act on. When the user says "check issues on GitHub", they want you to (a) list open issues, (b) find answers from Outlook/OneDrive/repo registers, and (c) reply on the issue. The `Repo Issue Auto-Responder` cron (every 2h) does this autonomously across `aseer-museum-pm`, `aseer-museum-viz`, `samaya-workspace`, `samaya-profile` — searching Outlook SQLite + Adel Darwish's OneDrive folder + repo registers for evidence before replying. Do not self-reply to issues authored by `sultandroid` unless asked.

**Pitfall — "عالج الكل" (handle all open issues) does NOT mean close the risk-tracker issues.** The `aseer-museum-pm` repo auto-generates one GitHub issue per risk from `06_Risk_System/*_risks.json` via `scripts/risk_issue_daily.py` (labels `risk-tracker,risk-daily,<REGISTER>`). These are **live state mirrors, not actionable bugs** — they are legitimately open and must NOT be closed manually. Before bulk-closing: (1) identify the risk-tracker set by label, (2) run `python3 scripts/risk_issue_daily.py --dry-run` — output `Unchanged=N, Closed=0` means all are in sync and none should be closed, (3) only close the **non-risk** issues (known-issues, open questions, commercial) and only those with verified resolution evidence. The cron closes risk issues automatically when the JSON status flips to `closed`/`mitigated`. Verified 2026-08-28: 188/198 open were risk-tracker and in sync; only the 10 non-risk issues were actionable. Also: many "known-issue" and "open question" issues are already CLOSED or already fixed in a prior commit — check `gh issue view <n> --json state,comments` and `git log` before re-fixing; a sibling agent may have already applied the fix on the remote (resolve rebase conflicts to `--theirs` when the remote version is more detailed).
```bash
cd /Users/mohamedessa/aseer-museum-pm
python3 scripts/document_intake.py --scan-dir 05_Comms
python3 scripts/document_intake.py --scan-dir 01_Registers
```

The pipeline classifies documents, extracts key fields, and updates registers automatically. After it runs, check `git diff --stat` to see what changed, then commit the pipeline's output. Only do manual register edits for items the pipeline missed (e.g. new PQ codes from email previews, invoice entries, specialist register updates).

**Exception:** The pipeline does NOT handle:
- PQ code updates from email previews (CG codes in Message_Preview)
- Invoice register entries (no invoice pipeline yet)
- Specialist register updates (derived from PQ data)
- Knowledge document generation (Phase 9)

These still need manual register edits after the pipeline runs.

### SQLite Lock Detection (MANDATORY before querying)

Outlook holds the SQLite database open with a WAL journal. **WAL mode permits concurrent reads even when Outlook holds the file open.** A locked DB does NOT mean queries will fail — only writes (backup, checkpoint, PRAGMA write) are blocked.

```bash
# Check if Outlook holds the lock
lsof ~/Library/Group\\ Containers/UBF8T346G9.Office/Outlook/Outlook\\ 15\\ Profiles/Main\\ Profile/Data/Outlook.sqlite 2>&1 | head -5

# Check WAL file size (2MB+ = active transaction log, but reads still work)
ls -la ~/Library/Group\\ Containers/UBF8T346G9.Office/Outlook/Outlook\\ 15\\ Profiles/Main\\ Profile/Data/Outlook.sqlite-wal 2>&1
```

**Decision tree:**
1. **Try SQLite first** — even with Outlook PID holding the file and a 3MB+ WAL, `SELECT` queries usually succeed. WAL mode permits concurrent readers.
2. **If query times out** (rare — only when Outlook is in the middle of a write transaction), retry once. If it times out again, fall back to AppleScript.
3. **Do NOT retry more than once.** The AppleScript fallback is slower but always works.

**Signals that SQLite is genuinely blocked (not just locked):**
- `lsof` shows Microsoft Outlook PID holding the file AND a `SELECT` query times out
- WAL file is 2MB+ AND the query times out
- `PRAGMA wal_checkpoint(TRUNCATE)` times out (this is a write — expected to fail when locked)
- `.backup` and `cp` both fail (these are writes — expected to fail when locked)

**Key insight:** A 3MB WAL + Outlook PID holding the file is the NORMAL state during business hours. Do NOT skip SQLite just because these conditions are true. Try the query first. Only fall back to AppleScript if the query actually times out.

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
| `Message_TimeReceived` | INTEGER | **Epoch varies by DB.** The active database at `Data/Outlook.sqlite` (with `Mail`/`folders` tables) uses **Unix epoch** — `datetime(col, 'unixepoch', 'localtime')` works directly. The old root-level `Outlook.sqlite` (0 bytes) is a stub. **Always verify first:** `SELECT Message_TimeReceived, datetime(Message_TimeReceived, 'unixepoch', 'localtime') as as_unix, datetime(Message_TimeReceived + 978307200, 'unixepoch', 'localtime') as as_mac FROM Mail ORDER BY Message_TimeReceived DESC LIMIT 1;` — the one showing today's date is correct. If `as_unix` is correct, use `datetime(col, 'unixepoch')`. If `as_mac` is correct, use `datetime(col + 978307200, 'unixepoch')`. |
| `Message_HasAttachment` | BOOLEAN | 1 = has attachments, 0 = no attachments |
| `PathToDataFile` | TEXT | Relative path to `.olk15Message` file (proprietary — use AppleScript instead) |

### Finding CG Response PDFs by Document Code

When CG returns Code C on a submittal, the response PDF is stored in Outlook's proprietary attachment store. Search by document code (ZD ref):

```bash
find "/Users/mohamedessa/Library/Group Containers/UBF8T346G9.Office/Outlook/Outlook 15 Profiles/Main Profile/Files" -name "*ZD-0086*" 2>/dev/null
```

Two files typically exist for a CG response:
- Smaller file (2-3MB) — the clean submitted document
- Larger file (5-7MB) — the CG-marked version with markup layers (handwritten annotations, stamps, highlights)

Copy both to the project's `02_CG_Responses/` folder for reference. The larger file is the one with CG markup.

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

The `Message_Preview` column holds a **capped** slice of the email body — **measured at exactly 255 chars** on the active `Data/Outlook.sqlite` (2026-08-15: `SELECT length(Message_Preview)` = 255 for every email checked). For bodies that fit, it's enough to understand the purpose; for anything needing the full body (longer threads, forwarded CG codes, full WeTransfer/SharePoint URLs), the preview is USELESS — do not assume ~500 chars. Verify cap with `SELECT length(Message_Preview) FROM Mail WHERE Record_RecordID=<ID>;`, then fall back to AppleScript `plain text content of m` or the `.olk15Message` body extraction (see TNEF section). The 255-char cap means: (a) a CG code in a forwarded body will NOT be in the preview, (b) a full sharepoint.com link will be cut off mid-URL, (c) Arabic/BOM preamble eats most of the budget leaving almost no real content.

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
See `references/cg-comment-dependency-chain-tracing.md` for when a CG comment says "confirm after X is approved" (e.g. ZD-0114 structural gated on cloud survey / concrete core / geotech) — trace the status of every named prerequisite across Outlook + repo registers to find the real blocker; distinguish architectural vs structural survey (structural needs cladding removal to measure columns); check the enabling demolition-plan approval (ZD-0106 Code B vs ZD-0032 Code C).
See `references/rfi-register-prior-correspondence-check.md` for the "does this RFI already exist / have prior correspondence?" dedup workflow — search the register FIRST (entries often already present, e.g. `RFI.xlsx` rows 566-569 under `Coordination - ...` blocks, frequently with empty No./sender/response columns), then Outlook subject → preview/body → related active packages (Rigging series, AV Package); place pure interface/coordination queries in a `Coordination - <topic>` block, NOT the `Showcase` block; the RFI Tracker (`A2742-10.05-004 RFI Traker.docx`) is often OneDrive EDEADLK-locked — note "unreadable" not "absent".
See `references/vendor-reply-drafting.md` for the "what's the reply to X / draft the reply to [vendor]" workflow — check Sent Items for an existing reply first, read the full thread body, then draft in the user's preferred format (manual-copy text, numbered list, flag open decisions).
See `references/commercial-counter-schedule-drafting.md` for drafting a reply to a vendor COMMERCIAL email (payment schedule, fee proposal, resolution request) — check the repo for the already-agreed position (GitHub issue comments, `03_Plans/05_Cost/REVISED_*_<VENDOR>_<date>.md` formal letters, correspondence register) BEFORE drafting; verify the schedule sums to the outstanding balance; check the submittal register before conceding "stalled / no input" claims; propagate mid-draft scope changes everywhere. A revised payment schedule is a RESCHEDULING, not a contract amendment — never write "issue the contract amendment" unless the parties actually amended scope/terms/value.
See `references/github-issue-triage.md` for the full "عالج الكل / شوف المشكله N" workflow — classify risk-tracker (auto-generated, don't close) vs actionable, verify current state before closing, close with evidence, git push discipline (post-commit hook + sibling-agent register conflicts).
See `references/evidence-based-correspondence-triage.md` for triaging contractor/vendor info-request lists — CHECK the repo registers + live Outlook before branding items "obstruction/delay tactic". Pitfalls: a design element the vendor questions may already be approved (PVC conduits Code B in MS-0005/PQ-0086/87); re-verify specialist appointment status from the signed-contract email, not a stale repo summary (SPS returned signed ICT contract 18-Aug, making "ICT not appointed" obsolete); the real open gap may be BMS (Jadco). User rule 2026-08-23: "اهم حاجه ردودك تكون بادله" — every claim must cite a repo path / register row / doc ref / Outlook ID.
See `references/forwarded-document-analysis.md` for the thread-first workflow when the user forwards a document.
See `references/cg-schedule-extraction.md` for extracting CG consultant schedule requirements from email chains.
See `references/sender-discovery-patterns.md` for the iterative workflow to find the correct sender name format when you don't know it.

### Pitfalls

**OneDrive .xlsx/.docx stub files** (recurring trap when reading Office files in OneDrive folders). Symptom: `cp file.xlsx /tmp/` succeeds, the destination file shows 15-100 KB on disk, but `unzip -l file.xlsx` fails with `End-of-central-directory signature not found`, and `openpyxl.load_workbook()` raises `BadZipFile: File is not a zip file`. Root cause: OneDrive files-on-demand cloud placeholder — the OS shows a non-zero stub but the real bytes never hydrated. Detection: file size looks plausible (10s-100s of KB) but the file fails any zip validity check. Fix: open the file in Finder, right-click → "Always keep on this device" to force the real bytes to download, then retry. Affects all zip-based Office formats (.xlsx, .docx, .pptx). Programmatic check: `python -c "import zipfile; zipfile.ZipFile(path).testzip()"` before parsing — if it raises `BadZipFile`, the file is a stub. Same trap appears for `.olk15Message` (Outlook internal format) and `.pdf` files; always test readability before assuming content. Recovery is per-file; no global "force download" command exists.

**CloudStorage EDEADLK (new OneDrive path, 2026+):** Files under `~/Library/CloudStorage/OneDrive-*/` use a different File Provider mechanism than the old `~/OneDrive/` path. Symptoms: `cp` fails with `fcopyfile failed: Resource deadlock avoided`, `ditto` fails, `openpyxl` raises `BadZipFile`, `textutil` says "couldn't be opened", `file` command says "cannot read (Resource deadlock avoided)", `brctl download` says "Path is outside of any CloudDocs app library", and even `open -a "Microsoft Excel"` followed by a 45s wait does NOT hydrate the file. The File Provider holds an exclusive lock that blocks ALL read access from terminal/Python/AppleScript. **No programmatic workaround exists** — the user must open the file manually in Finder, let OneDrive hydrate it (the file icon changes from cloud to checkmark), then retry. AppleScript via Excel also fails because Excel cannot open the stub either. Detection: `python3 -c "import zipfile; zipfile.ZipFile(path)"` raises `BadZipFile` AND `cp path /tmp/` fails with EDEADLK. This is distinct from the old OneDrive path where `cp` succeeded but the file was a stub.

**Cross-folder search for supplier replies.** Do NOT limit the search to the project's main folder. Supplier replies may be filed under a DIFFERENT project folder. Always use a cross-folder SQL query.

**macOS TCC blocks SQLite access intermittently.** Always try SQLite first. If it fails, fall back to AppleScript.

**`every folder` AppleScript command fails.** Use `(every message of inbox)` for Inbox scanning, or target specific project folders by name.

**`folder "Name" of inbox` may fail with error -10006.** Workaround: iterate directly without assignment: `repeat with f in (every mail folder of inboxN)`.

**`mail folder id <N>` is more reliable than `folder "Name" of inbox`.** Discover the numeric ID first, then use `every message of mail folder id <N>`.

**Multiple Inbox folders exist (one per account).** Use `get id of every mail folder whose name is "Inbox"` to discover all Inbox IDs.

**`sender` returns a Mail Recipient record, not a string.** Always wrap in a try block with `name of sender` (NOT `(sender of m) as text`). **`as text` coercion on sender produces garbled Unicode/raw bytes** when Outlook returns a non-decomposable recipient object — the output looks like Chinese/box-drawing characters instead of the actual name. Use `name of sender` inside a `try`/`on error` block for reliable results.

**`sender` returns blank via `osascript -e` one-liners.** Use a short `.applescript` file on disk for sender extraction.

**`plain text content` works reliably for Inbox messages, may fail for sub-folders.**

**`PathToDataFile` returns %20-encoded paths.** Use `$'...'` bash quoting or Python `urllib.parse.unquote`.

**AppleScript `.applescript` files have a ~700-byte script body limit.** Keep scripts short. Break into multiple small files. Scripts exceeding this limit fail with misleading `Expected "," but found class name` (-2741) errors. **Workaround:** use per-index `osascript -e` one-liners for simple property reads (each is a separate process, no body limit). Reserve `.applescript` files for complex operations like attachment extraction.

**However, a single `.applescript` file with a `repeat` loop under ~500 bytes DOES work reliably** for batch inbox reads (subject, time, attachment count, sender name). Verified working example loops through indexes 1-10 returning pipe-delimited output. The 700-byte limit is a *compiled* limit — loops with short bodies (no nested `tell` blocks, minimal string concatenation) compile compactly and pass. Use `name of sender` inside try/on-error for clean sender names.

**`considering case` block causes syntax errors inside `tell application` blocks.** The `considering case` construct is not supported inside Outlook's AppleScript dictionary. Use uppercase-only string matching instead (e.g., `if subj contains "ASEER"`). If case-insensitive matching is needed, write a `toLower` handler outside the `tell` block.

**Most reliable pattern: bash `for` loop with individual `osascript -e` one-liners per property.**

**`has attachment` returns empty string via `osascript -e` one-liners.** Use a `.applescript` file for reliable attachment detection. Even in `.applescript` files, `has attachment of theMsg` can fail with `Expected end of line, etc. but found class name` (-2741) errors. **Reliable workaround:** use `count of (every attachment of theMsg)` instead — this always works and returns the integer count. Example:

```applescript
tell application "Microsoft Outlook"
    set theMsg to message id 49039
    set attCount to count of (every attachment of theMsg)
    return attCount
end tell
```

This is the most reliable pattern for attachment detection across both `.applescript` files and `osascript -e` one-liners.

**Body lists filenames but `Message_HasAttachment=0` → Aconex/SharePoint-uploaded, NOT extractable.** Some submittal emails (esp. from Hesham Abdelhameed, and all Aconex transmittal notifications) name the document files in the body ("MOC-MUS-ASE-1E0-ZD-0103 Rev.01.pdf") but carry NO actual inline attachment — `count of (every attachment of m)` returns 0 and the `Mail_OwnedBlocks`/`Blocks` join returns no rows. The file was uploaded to Aconex/CDE and the email is just a notification. **Do not burn AppleScript/base64 cycles retrying** — check `Message_HasAttachment` in the SQLite query FIRST and only attempt extraction when it's 1. Log these as `Submitted` using the Aconex ref from the subject (e.g. `SIC.-WTRAN-000148`) and route to the register without an attachment copy. Note: an email that shows 0 attachments but looks like a document submittal is almost always a CDE sync, not a genuine inline-attachment failure.

**`subject of m` / `time received of m` / `has attachment of m` fail with `Can't make |subject| of incoming message id X into type specifier` (-1700) on Outlook 16.90+.** This is a persistent AppleScript regression where direct property access on `message id N` objects fails. The error is NOT a syntax issue — the same syntax works on older Outlook versions. **Reliable workaround:** use `item N of (every message of mail folder id <FOLDER_ID>)` instead of `message id N`. This bypasses the broken property-access path:

```applescript
-- BROKEN (Outlook 16.90+):
set m to message id 49107
set msub to subject of m  -- ERROR: Can't make |subject| of incoming message id 49107 into type specifier

-- WORKS:
set msgs to (every message of mail folder id 114)
set m to item 1 of msgs
set msub to subject of m  -- OK
```

**Combined workaround for scanning recent inbox messages:** use `item N of (every message of mail folder id <ID>)` in a loop, or generate individual `.applescript` files via Python (one per message index, not per message id). The `item N` approach works reliably for all property reads (subject, time received, has attachment, sender).

**`message/rfc822` attachments (forwarded .eml) cannot be saved via AppleScript.** When an email's attachment has content type `message/rfc822`, the `save att in saveFile` command fails with error -2700. The actual file is embedded inside the forwarded message. Workaround: open the email manually in Outlook and save the attachment from the forwarded message's own attachment list. If the forwarded message itself contains an Excel/PDF, you may need to extract the inner message's attachments separately.

**`time received` returns a formatted date string.** Parse with `date -j -f "%A, %d %B %Y at %I:%M:%S %p"` on macOS.

**Inbox message ordering is oldest-first (CRITICAL).** Message index 1 is the **newest** message. This applies to ALL folders.

**Pitfall — closeout reports can be PARTIALLY closed, not fully.** When a Safety Observation Report (SOR) or NCR closeout email arrives with an attached closeout report, do NOT mark the register item "Closed" from the email body alone. Read the attached PDF: a single SOR may have multiple observation items, and only some may be resolved. Example (2026-08): SOR-013 had 3 items — item 3 (housekeeping) closed 06-Aug but items 1-2 (glass panel storage) were still "In Progress". Marking it fully "Closed" in the NCR register was wrong and had to be corrected to "Partially Closed (items 1-2 open)". Always open the closeout PDF and check each numbered item's status before writing "Closed"/"Open" to the register.

**Pitfall — `.eml` (message/rfc822) attachments save as 0-byte files.** The `save att in saveFile` command "succeeds" (exit 0) but writes a 0-byte file when the attachment is a forwarded `.eml`. The actual content is nested inside the forwarded message and is not directly extractable via AppleScript. Detect: after extraction, check `ls -la` — a 0-byte `.eml` means the content is embedded. Flag for manual open in Outlook rather than burning retries.

### Reading CG Response Codes from Preview Text (No Attachment Extraction)

CG responses from Hossam Mabrouk follow a consistent pattern: `Message_Preview` starts with a classification line, then contains the CG code. You can read A/B/C/D codes **without extracting attachments** — saves ~30s per email.

**Pattern in preview text:**
```
Classification-ASE-External-DS-ELC-0089
...
B - Approved with Comments       ← or "C - Revise and Resubmit"
REF. MOC-MUS-ASE-1E0-ZD-0089
```

**Batch CG code checking query:**
```sql
SELECT m.Record_RecordID, m.Message_NormalizedSubject,
  CASE
    WHEN m.Message_Preview LIKE '%B - Approved with Comments%' THEN 'B'
    WHEN m.Message_Preview LIKE '%A - Approved%' THEN 'A'
    WHEN m.Message_Preview LIKE '%C - Revise%' THEN 'C'
    WHEN m.Message_Preview LIKE '%D%Rejected%' THEN 'D'
    WHEN m.Message_Preview LIKE '%Approved%' THEN 'B'
    ELSE 'UNKNOWN'
  END as cg_code
FROM Mail m
WHERE m.Record_RecordID IN (49279, 49271, 49259)
  AND m.Message_SenderList = 'Hossam Mabrouk';
```
Exact-phrase branches come FIRST with the explicit letter prefix (e.g. `'B - Approved with Comments'`), so a bare-`A` branch can never swallow the B-line. The loose `'%Approved%'` fallback is LAST. This ordering is critical — see the CASE-order pitfall below.

**Pitfall — CASE branch ORDER mislabels "B - Approved with Comments" as Code A.** A first branch `WHEN ... LIKE '%A%Approved%' THEN 'A'` matches the phrase "**B** - Approved with Comments" because the literal "Approved" contains an "A" and the `%` wildcards span the "B -". The loose pattern swallows the B-line, returning 'A'. Consequence (2026-08-14): PQ-0145 and PQ-0146 interlock suppliers were auto-classified Code A but were genuinely Code B — caught only by re-reading the previews. **Rule: order the CASE branches by the explicit code letter first, never a bare `%A%` wildcard branch.** Match the distinct full phrases — `'B - Approved with Comments'`, `'A - Approved'`, `'C - Revise'`, `'D – Rejected'` — with the letter prefix included, and put the loose fallbacks (`'%Approved%'` → B) LAST. Verify a sample of `UNKNOWN` rows against the actual preview text before writing codes to registers, per the "verify from the actual email" rule below.

**Pitfall — CG code uses en-dash, not hyphen.** The preview text uses `D – Rejected` (en-dash, U+2013), not `D - Rejected`. The CASE pattern `LIKE '%D - Rejected%'` (hyphen) does NOT match `D – Rejected` (en-dash). Use `LIKE '%D%Rejected%'` or `LIKE '%D – Rejected%'` with the actual en-dash character. Similarly, `Approved with Comment - B` uses a hyphen, so `LIKE '%Approved with%'` catches it. Always test the actual preview text before hardcoding CASE patterns.

**Workflow (see the MANDATORY rule below — preview-code fast-path is for Triage only, not final register writes):**
1. Query recent emails from CG senders with doc refs
2. Extract CG codes from preview using CASE pattern (fast triage)
3. For the actual register update, ALWAYS extract the PDF and read the full document — Code B/C/D responses carry substantive reviewer remarks on later pages of the same PDF (see "See attached comments sheet" pattern below). The code alone is insufficient.
4. Code C/D → capture each numbered CG comment verbatim in the register + action item
5. Code B → capture the approved-with-comments remarks + reviewer(s) too; do NOT skip extraction

This preview-CASE shortcut is a *triage* accelerator (prioritising which emails to dig into), not a substitute for attachment reading.

**Pitfall:** `Message_Preview` truncated to **255 chars** (not ~500). If long preamble before the code line, fall back to AppleScript `plain text content`.

**Pitfall — CG code may be in forwarded body, not top-level preview.** When Hossam Mabrouk forwards a CG response (e.g. ZD-0103 Rev.01), the top-level `Message_Preview` may only show "@Hesham Abdelhameed The Contractor Must to submit..." with no A/B/C/D code. The actual CG code (e.g. "D – Rejected") is in the *forwarded* message body below. Use AppleScript `plain text content of m` to read the full thread. If the preview shows a reply/forward instruction but no code, always extract the full body — the code is in the quoted original message.

**Pitfall — "Resubmit as new submission number" is a distinct rejection mode.** CG may reject a Rev.01 not with Code C/D but with an instruction to "submit with a new submission and provide the justification/reason for the change accordingly." This is a procedural rejection — the document must be resubmitted under a new doc ref, not revised under the same ref. Log this as **Rejected — Resubmit as New** in the register, not as Code C or D. It implies the revision was procedurally invalid (wrong ref, wrong routing), not substantively deficient.

### MANDATORY: Read All Attachments, Not Just Previews/Codes (user rule)

The user requires that every email scan **extract and READ the actual attachments**, not stop at the email preview or the CG status code. "Read all attachments and understand and remarks if any" is an explicit, recurring instruction. A scan that only logs codes/registers without reading the attached documents is incomplete. **This overrides the workflow below that says "Code B → no attachment needed"** — even Code B responses carry substantive reviewer remarks that drive the next submission.

**Extraction-first workflow:**
1. For every project email with `Message_HasAttachment=1`, extract the PDFs via AppleScript (batch generator — see above).
2. `pdftotext -layout` **the full document** (all pages), not just the first page.
3. Register the status code **AND** the actual reviewer remarks/comments, not just the A/B/C/D letter.
4. The code alone is NOT the deliverable. The remarks drive the resubmission work — capture them verbatim in the register.

**CG response "See attached comments sheet" pattern:** A CG response email may return a single PDF whose first page is the Document Submittal (DS) form showing only "See attached comments sheet" or "See attached." The actual reviewer comments are on **later pages of the same PDF** (often page 2: a `CG comments:` block with numbered items, plus reviewer name/signature lines like "Senior Architecture Engineer" / "CG Project Director"). Do NOT conclude the comments are missing or a separate attachment — run `pdftotext -layout` on the whole file and read past the DS form. Example (2026-08-17, ZD-0109): email preview + DS page 1 said only "B - Approved with Comments"; the 4 substantive comments (structural coordination, accessible routes, G5 Making Space, Main Entrance GA updates) and reviewers (Maged Zamzam / Mansour Alrezeni) were on page 2.

**Pitfall — CG Code C comments may be a CRS sheet in `.xlsx`, not a PDF.** The DS form page may say "Follow the attached CRS sheet" and the actual numbered reviewer comments live in an attached **Excel Comments Resolution Sheet (CRS)**, not in the PDF. Extract the `.xlsx` alongside the PDF and read it with `openpyxl` (iterate `ws.iter_rows(values_only=True)`, print non-empty cells). The CRS sheet has a `Reviewer Comment` column, a `Code` column (A/B/C/D/F per row), and a reviewer name/position/date block at the bottom. Example (2026-08-18, 1E0-1G-0004): DS page 1 said only "Follow the attached CRS sheet"; the 15 comments (BMR Designer role, CG logo, reference drawings, DMP adherence, LSZH cables, separate AV DBs, etc.) were all in the attached `..._1G-0004.xlsx` CRS sheet by Mohamed Elbaz. Always extract BOTH the PDF and any `.xlsx` attachment from a Code C email — the code alone and the DS page are insufficient.

**CG remark capture format for registers:** When logging a Code C/B, include a `**CG comments (N):**` block in the register row enumerating each numbered remark verbatim (or closely paraphrased), and note the reviewer(s). This is what makes the register actionable for the resubmission.

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

**OneDrive file management (macOS):**\n- `mv` (rename within same OneDrive directory) works — it's a metadata-only operation\n- Direct `cp`/write to OneDrive paths can cause EDEADLK (read) or `Operation not permitted` (write from non-Finder processes)\n- The write restriction is a macOS File Provider TCC limitation: ALL write methods fail (`cp`, `mv`, `ditto`, `cat >`, Python `open()`, AppleScript Finder `duplicate`, `mkdir`). Does not depend on cloud-only state — even fully local files in CloudStorage are unwritable from terminal/Python.\n- **User-preferred staging area = the Micro volume (`/Volumes/MIcro/`), NOT `/tmp`.** The user explicitly corrected this (2026-08): \"you have to copy one by one to micro volume not build it will work fine with you.\" Copy the organized files to `/Volumes/MIcro/Temp/<job>_filed/` (a real writable filesystem — `cp -R` works fine there), then `open` that folder in Finder and tell the user to drag the folders into OneDrive manually. `/tmp` also works for staging but the user prefers Micro; use Micro so the user can find and drag the files easily. Keep a `_FILE_MAPPING.csv`/`.md` in the staged folder mapping each file to its OneDrive destination folder.\n- Stage large archives to /tmp first with `unzip`, then `mv` to OneDrive target (though `mv` to CloudStorage destination also fails — use Finder or copy to a non-CloudStorage target).

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
See `references/email-subject-not-found-onedrive-search.md` for when an email subject isn't found in Outlook — search the OneDrive submittal tree + repo by keyword before concluding it's missing (the document is often filed under a descriptive folder name, not the email subject; OneDrive EDEADLK on the found file is a cloud stub, not corruption).
See `references/html-body-strip-pattern.md` for the HTML-body-strip-to-text pattern that preserves tables (block tags → newline, `</td>` → `|`), plus `pdftotext -layout` for PDFs and python-docx for DOCX attachment content.
See `references/email-chain-tracing.md` for tracing forwarded email chains (FW:).
See `references/chaser-reminder-email-pattern.md` for the chaser/reminder email class (Samaya chasing a specialist for documents/CG-comment responses) — 255-char preview truncation, recall-message noise, corrupt CG-comments attachment handling.
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

## Factory Employee Violation Search (Outlook → VIOLATIONS System)

When the user asks to find historical violations/penalties for factory employees:

**Source:** Outlook SQLite (NOT Gmail IMAP). The user's Gmail is personal; work emails are in Outlook.

**Arabic search keywords that work:**
- `مخالفة` / `مخالفات` — violation(s)
- `خصم` — deduction
- `إنذار` — warning
- `جزاء` / `جزاءات` — penalty/penalties
- `تأديب` — disciplinary
- `غرامة` — fine
- `تأخير` — delay/lateness
- `رفض` — refusal
- `عقوبة` — punishment
- `لفت نظر` — notice

**Canonical query pattern:**
```sql
SELECT m.Record_RecordID, m.Message_NormalizedSubject,
       substr(m.Message_Preview, 1, 1500) as preview,
       m.Message_SenderList, m.Message_TimeReceived
FROM Mail m
WHERE (m.Message_Preview LIKE '%مخالفة%' OR m.Message_Preview LIKE '%خصم%'
       OR m.Message_Preview LIKE '%إنذار%' OR m.Message_Preview LIKE '%جزاء%'
       OR m.Message_Preview LIKE '%تأديب%' OR m.Message_Preview LIKE '%رفض%')
  AND m.Message_SenderList LIKE '%raoof%'
  AND m.Message_Hidden = 0
ORDER BY m.Message_TimeReceived DESC;
```

**Cross-reference with Odoo:** After finding a violation email, look up the employee in Odoo by name to get their Odoo ID, biotime code, job title, and department. Use the session-based Odoo API (password auth, not API key — the key is expired).

**Registration workflow:**
1. Extract violation details from email preview (date, employee, type, reporter, action taken)
2. Look up employee in Odoo for biotime code and Odoo ID
3. Create violation memo in `VIOLATIONS/VIOL-YYYY-NNN-<short-desc>.md` following the existing memo format
4. Update `VIOLATIONS/INDEX.md` with the new row
5. Update the stats footer (total count, last updated)

**Pitfall — email preview truncation:** `Message_Preview` is **255 chars** (measured 2026-08-15). For full body, use AppleScript `plain text content of msg`. If the preview contains enough info (date, employee name, violation type, action), skip AppleScript.

**Pitfall — employees not in Odoo:** Some workers (e.g. هريدهاي, عبد المجاهد) may not have Odoo records or biotime codes. Note this in the memo and use available info.

**Pitfall — attachment-only details:** Some violation emails reference an attached PDF/image for full details. These attachments cannot be extracted from the preview. Flag as "تفاصيل ناقصة" in the memo.

See `references/factory-violation-search.md` for a complete worked example.

## Hard Rules (apply to every response)

**ZERO Arabic in any output.** All subject lines, sender names, folder names, file names, and email body excerpts must be presented as concise English descriptions only. No raw Arabic text, no Arabic in parentheses, no mixed-language lines. This is a hard rule — applies to every email listing, summary, and document analysis. Even when the DB returns Arabic sender names or subjects, translate them silently before display.

**User preference — "بالبلدي" plain-language summaries (2026-08-27).** When the user asks "what's required / what do I need to do" after an email scan, do NOT dump the full technical breakdown. Give a **plain, simple Arabic summary** (بالبلدي) of the action items: what came back from the consultant, what needs revision, what needs a decision, what's just informational. Lead with the required actions, keep it short, no jargon. The user explicitly asked for this over the detailed English table.

**User preference — always include the full submission title/ref (2026-08-27).** When listing submittals, CG responses, or action items, ALWAYS state the full document reference AND title (e.g. `MOC-MUS-ASE-1C0-ZD-0114 — Design Deliverables Tracker – Structural Analysis & Design`), not just a short label like "the structural sheet". The user needs the exact title to know which document you mean. This applies in both English and بالبلدي summaries.

**User preference — direct yes/no verdict on approval status (2026-08-27).** When the user asks "did it get approved or not?" (e.g. "يعني اتوافق عليها ولا لا !"), LEAD with a clear ✅/❌ verdict on the specific document, THEN the detail. Do NOT open with a hedged breakdown of codes and conditions. State plainly: "ZD-0106 = ✅ approved (Code B, approved with comments — you can start). ZD-0032 = ❌ not approved (Code C, needs revision)." Only after the verdict explain the conditions/comments. This mirrors the existing "Possible or Not" verdict style for deadlines — apply it to approval-status questions too.

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

### PREFERRED: Python generator script (cron-safe, no `&` issues, under byte limit)

Write a Python script to `/tmp/` that generates individual `.applescript` files, then run it. This avoids the `&` tool guard issue AND the ~700-byte AppleScript body limit in one step. The Python script can include filename sanitization (replacing `/` with `-`) via AppleScript's `text item delimiters` — this fits under the byte limit at ~538 bytes per script:

```python
#!/usr/bin/env python3
"""Generate AppleScript files for each email ID with sanitized filenames."""
import os

ids = [49039, 49034, 49036]  # your email IDs here
outdir = "/tmp/email_attachments"
os.makedirs(outdir, exist_ok=True)

for eid in ids:
    script = f'''set o to "/tmp/email_attachments/"
tell application "Microsoft Outlook"
\tset m to message id {eid}
\trepeat with a in (every attachment of m)
\t\tif content type of a does not start with "image/" then
\t\t\tset n to name of a
\t\t\tset my text item delimiters to "/"
\t\t\tset nParts to text items of n
\t\t\tset my text item delimiters to "-"
\t\t\tset n to nParts as string
\t\t\tset my text item delimiters to ""
\t\t\tset p to o & "{eid}_" & n
\t\t\tdo shell script "touch " & quoted form of p
\t\t\tsave a in (POSIX file p as alias)
\t\tend if
\tend repeat
end tell
'''
    path = f"/tmp/ext_{eid}.applescript"
    with open(path, "w") as f:
        f.write(script)
    print(f"{eid}: {os.path.getsize(path)} bytes")
```

Then run sequentially (batch 5-6 per terminal call):

```bash
python3 /tmp/gen_as_scripts.py
osascript /tmp/ext_49039.applescript 2>&1
osascript /tmp/ext_49034.applescript 2>&1
# ... one per email, 5-6 per terminal() call
```

**Why this is preferred over bash heredoc:** The Python generator avoids the `&` tool guard entirely (no `&` in the terminal command), handles sanitization cleanly, and each generated script stays under the 700-byte limit.

### Fallback: inline `osascript -e` when `.applescript` file fails

When the Python-generated `.applescript` file approach fails silently (no output, no files saved), try inline `osascript -e` with the same `message id N` syntax. This works for simple single-attachment extraction even when the file-based approach doesn't:

```bash
osascript -e '
tell application "Microsoft Outlook"
    set m to message id 49773
    set atts to (every attachment of m)
    set outFolder to "/tmp/email_attachments/"
    repeat with a in atts
        set attName to name of a
        set savePath to outFolder & "49773_" & attName
        do shell script "touch " & quoted form of savePath
        save a in (POSIX file savePath as alias)
    end repeat
end tell
' 2>&1
```

For batch extraction of multiple emails, use a bash `for` loop with inline `osascript -e`:

```bash
for id in 49810 49823 49824; do
  osascript -e "
tell application \"Microsoft Outlook\"
    set m to message id $id
    set atts to (every attachment of m)
    set outFolder to \"/tmp/email_attachments/\"
    repeat with a in atts
        set attName to name of a
        set savePath to outFolder & \"${id}_\" & attName
        do shell script \"touch \" & quoted form of savePath
        save a in (POSIX file savePath as alias)
    end repeat
end tell
" 2>&1
done
```

**Pitfall:** The inline approach may fail for emails with many attachments or special characters in filenames. The Python generator approach is preferred for reliability; use inline as a fallback when the generator produces no output.

### Fallback: inline `osascript -e` when `.applescript` file fails

When the Python-generated `.applescript` file approach fails silently (no output, no files saved), try inline `osascript -e` with the same `message id N` syntax. This works for simple single-attachment extraction even when the file-based approach doesn't:

```bash
osascript -e '
tell application "Microsoft Outlook"
    set m to message id 49773
    set atts to (every attachment of m)
    set outFolder to "/tmp/email_attachments/"
    repeat with a in atts
        set attName to name of a
        set savePath to outFolder & "49773_" & attName
        do shell script "touch " & quoted form of savePath
        save a in (POSIX file savePath as alias)
    end repeat
end tell
' 2>&1
```

For batch extraction of multiple emails, use a bash `for` loop with inline `osascript -e`:

```bash
for id in 49810 49823 49824; do
  osascript -e "
tell application \"Microsoft Outlook\"
    set m to message id $id
    set atts to (every attachment of m)
    set outFolder to \"/tmp/email_attachments/\"
    repeat with a in atts
        set attName to name of a
        set savePath to outFolder & \"${id}_\" & attName
        do shell script \"touch \" & quoted form of savePath
        save a in (POSIX file savePath as alias)
    end repeat
end tell
" 2>&1
done
```

**Pitfall:** The inline approach may fail for emails with many attachments or special characters in filenames. The Python generator approach is preferred for reliability; use inline as a fallback when the generator produces no output.

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

### Pitfall: adding recipients to an outgoing message FAILS on Outlook 16.90+ (verified 2026-08-22)

`make new recipient at end of recipients of <msg> with properties {...}` fails for **every** key tried, all with `-1700 Can't make X into type properties of recipient`:

```applescript
-- ALL FAIL with -1700 on 16.90+:
make new recipient at end of recipients of m with properties {address:"x@y.com"}
make new recipient at end of recipients of m with properties {name:"X"}
make new recipient at end of recipients of m with properties {email address:"x@y.com"}
make new recipient at end of to recipients of m with properties {address:"x@y.com", name:"X"}
make new recipient at end of recipients of m with properties {email address:{address:"x@y.com", name:"X"}}
make new recipient with properties {address:"x@y.com"}
```

Also fails: `set email address of r to "x@y.com"` (`Can't make "x@y.com" into type email address`), `make new email address with properties {...}` (-2710), and creating a bare recipient then assigning fields (bare `make new recipient` errors with `-2710 Cannot create a recipient without a name or e-mail address`). Even `properties of m` on the new draft fails.

**Subject+body in a single `make new outgoing message with properties {subject:..., body:...}` also fails** with `-1700 ... into type properties of outgoing message` when body is a long multi-line string. Creating with just `{subject:...}` works reliably and opens the compose window — but you still cannot attach recipients.

**Gotcha — the draft is still created even when body/recipient steps fail.** Partial drafts (subject set, no recipients) land in the `Placeholder_Drafts_Placeholder` folder, NOT the `Drafts` folder. They show `Message_TimeReceived = 2001-01-01 03:00` in SQLite (never saved-to-send). Each failed attempt silently leaves an orphan draft — delete them to avoid accumulating clutter:

```applescript
tell application "Microsoft Outlook"
	repeat with mid in {51261,51262,51263}   -- draft ids to purge
		try
			delete message id mid
		end try
	end repeat
	return "done"
end tell
```

**Reliable path:** Do NOT burn cycles iterating AppleScript recipient syntax (it is genuinely blocked on 16.90+). Create the draft with the subject only to open the compose window, then hand the user the full body text + To/CC addresses to paste — which already matches the user preference above (manual copy over automated drafts). Look up the confirmed recipient addresses from SQLite (`Message_SenderAddressList` for a known person, or `Message_ToRecipientAddressList`/`Message_CCRecipientAddressList` on a related email) so the user can paste them. This is the pragmatic resolution of an AppleScript-dictionary regression, not a workaround to keep hunting for.

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

**Distinguish cloud-link types — they are NOT all the same:**
- **WeTransfer / external transfer links** — NOT downloadable from this environment. Flag to the user for manual download with ⚠️ expiry warning.
- **Samaya internal SharePoint links** (`samayainvestksa-my.sharepoint.com/...`) — internal submittal deliveries (e.g. Scenography Report from Ali Abdelrahman). These are accessible to the user (no expiry risk like WeTransfer) and are NOT a download blocker — just report the link and note the deliverable. The full URL is in the email body, NOT the preview (preview truncates at **255 chars**). Use AppleScript `plain text content of m` to recover the complete link. Example (2026-08-13): Scenography Report email preview showed only "Attached link which contain..." — the actual `https://samayainvestksa-my.sharepoint.com/:f:/g/personal/sultan_samayainvest_com/...` was only in the full body.

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
See `references/multi-project-routing-script.py` — reusable Python router for multi-project scans (Aseer, Zamzam, Jabal Omar). Document-code-based patterns, OneDrive paths, dedup handling.

## Batch Email Pipeline (End-to-End Workflow)

### Phase 1 — Discovery
Query Outlook SQLite. Always JOIN folders table. Always use 'localtime'.

### Phase 2 — Extract Attachments (AppleScript batch)
Write a bash heredoc script that loops through email IDs.

### Phase 3 — Read & Route
Use `pdftotext` to extract text from PDFs, then route by document code pattern.

### Phase 3.5 — Produce CG Submission Plan
See `references/email-to-submission-plan.md`.

### Phase 4 — Create MD Summary Files
For each CG response PDF extracted, create a structured MD summary alongside it in `02_CG_Responses/`:
- YAML frontmatter (last_updated, owner_agent, status, source)
- Submittal metadata table (ref, date, CG code, reviewer)
- CG comments table with status per item
- Filed documents list
- **Actions Required** section — numbered list of what the user needs to do next

### Phase 5 — Cross-reference & Update

**CRITICAL: The review log alone is NOT sufficient.** The user requires that every email scan updates the actual registers, not just writes `email_scan_*.md`. A cron run that only writes the review log is a failed run. For every CG code (A/B/C/D) extracted, update the relevant register files in `~/aseer-museum-pm/`:
- `01_Registers/submittal_register.md` — status column per doc ref (ZD/1G/PQ) to the new CG code + date; append row if absent
- `01_Registers/prequalification_register.md` — PQ codes
- `01_Registers/assessment_evaluation_register.md` — electrical/mechanical assessment reports
- `01_Registers/si_register.md` — **CG Site Instructions (SI-0NN)**. New SI → append a row (ref `MOC-MUS-CG-ASE-1KN-SE-NNN` / `Classification-...-SI-HSE-NNNN-OPEN`, date, subject, Status OPEN) + bump `last_updated` frontmatter. Check the register's current max SI number first — a new SI (e.g. SI-022 when the register ends at SI-020) is genuinely new; an Aconex transmittal (e.g. `CGP-TRANSMIT-NNNNNN`) is just the same SI's CDE sync, not a separate item.
- `01_Registers/risk_register.md` + `06_Risk_System/risks.json` — new risks from Code D/C; update revision + total in BOTH (risks.json is SoT; recompute Summary counts from actual rows, don't hand-edit)

**SI → risk decision rule:** A new CG Site Instruction is usually *evidence for an existing risk*, NOT a new risk row. Before creating a new PRR row, check whether the SI's discipline already has a mapped risk (e.g. an HSE/Compliance SI links to `PRR-HSE-01`). If so, append the SI ref to that risk's Evidence column and leave the score/stats unchanged. Only create a NEW risk when the SI introduces a genuinely new, uncaptured exposure with its own score. Example (2026-08-13): CG SI-022 (C&D waste management non-compliance) was OPEN and new to `si_register.md`, but linked as evidence under `PRR-HSE-01` — no new risk, no stats change.
- `00_Status/action_items.md` — action item per Code C/D with owner + due
- `03_Plans/08_Risk/reviews/email_scan_YYYY-MM-DD.md` — review log (append-only)

**Verify CG codes from the actual email, not the cron summary.** The cron's CG-code extraction can MISLABEL a document's title. Example (2026-08-06): the cron called ZD-0103 "Compliance & Understanding Report" but the actual email subject was "Earthing LPS Compliance Understanding Report" (Code D). Always re-query the email preview (`Message_Preview`) for the exact doc title and code before writing it to a register. The CG email from Hossam Mabrouk is authoritative — trust it over the cron's summary.

**Pitfall — sibling subagents may be editing the same register concurrently.** The email pipeline runs as a cron alongside other agents (Adel bank sync, document_intake, dashboard regen, other Hermes sessions). When `patch` returns a `_warning` like "modified by sibling subagent ... but this agent never read it", a concurrent agent has written the file since your last read. Re-read the file (or the specific rows) BEFORE writing, and re-verify your edit landed after the patch — otherwise you can clobber the sibling's changes or create duplicate rows. This is common on `submittal_register.md` during morning scans. Also note: the same register row may appear in BOTH a `||`-prefixed and a `|||`-prefixed section, so a `patch` anchor that isn't unique fails with "Found 2 matches" — for appends use a Python insert-after-FIRST-occurrence (matching `l.strip()==anchor.strip()`) instead of `patch`.

**Pitfall — `patch` tool fails on duplicate register rows.** Some registers (e.g. `assessment_evaluation_register.md`) contain the SAME block of rows twice (a `||`-prefixed section and a `|||`-prefixed section with identical doc refs). `patch` with a non-unique anchor fails with "Found N matches" and loops. Do NOT keep retrying with slightly different context — switch to a Python script that inserts after the FIRST occurrence only:

**Pitfall — `patch replace_all=true` can create duplicate rows.** When `replace_all=true` matches the same old_string in multiple locations (e.g. a row that appears in both a `||`-prefixed and `|||`-prefixed section), it replaces ALL occurrences, creating duplicate rows. After a `replace_all` operation, always verify the file for duplicates and deduplicate if needed. Use a Python one-liner via terminal to remove exact duplicate lines:

**Pitfall — `patch` can CORRUPT the pipe-nesting prefix on the anchor row when inserting a new row.** When you use `patch` to insert a new register row by replacing an existing anchor row with `anchor + newline + new_row`, the tool sometimes rewrites the anchor's leading `|`-prefix (e.g. `|||` → `|||||` or `|` → `||`), silently changing the row's nesting level in the markdown table. This happened 4× in one session (2026-08-22) on `submittal_register.md` and `sor_register.md` — each insert shifted the anchor row's pipe count, requiring a follow-up `patch` to restore it. **Rule: after every row-insert `patch`, re-read the anchor line and verify its leading pipe count is unchanged; if it drifted, fix it back immediately.** The pipe count encodes the row's section nesting — a wrong count breaks the register's table structure even though the diff looks clean. Prefer the Python insert-after-FIRST-occurrence approach (below) for appends to avoid this entirely.

```bash
python3 -c "
with open('path/to/register.md', 'r') as f:
    lines = f.readlines()
seen = set()
new_lines = []
for line in lines:
    stripped = line.strip()
    if stripped in seen and 'DOC-REF' in line:
        continue  # skip duplicate
    seen.add(stripped)
    new_lines.append(line)
with open('path/to/register.md', 'w') as f:
    f.writelines(new_lines)
print('Dedup done')
"
```
```python
with open(path) as f: lines = f.readlines()
if any("ZD-XXXX Rev.01" in l for l in lines):
    print("already present")
else:
    for i, l in enumerate(lines):
        if "ZD-XXXX | <exact anchor text>" in l:
            lines.insert(i+1, new_row); break
    with open(path, "w") as f: f.writelines(lines)
```
Also verify the exact anchor line with `repr(lines[idx])` first — trailing whitespace/pipe-count differences break exact-match anchors.

**Rebuild risk webapp if risks.json changed:** `python3 webapp/build_risk.py` (→ src/index.html) then `python3 webapp/build_snapshots.py --bump` (→ new snapshot xlsx). Force-add the xlsx (`git add -f`) since `*.xlsx` is gitignored but the latest snapshot is force-tracked. Handle the post-commit hook that dirties `index.html`: `git checkout -- 06_Risk_System/webapp/src/index.html` before and after `git pull --rebase origin main`, then push.

Update ALL relevant registers: Master Submittal Register, Plan Tracker, discipline-specific CG_STATUS.md, submission plans, Lessons Learned Register, Odoo tasks, Memory.

**Cascade pattern (CG responses touch multiple files):**

When CG responses arrive, one email scan usually updates:
- `01_Registers/submittal_register.md` — CG code + date for each submittal
- `01_Registers/prequalification_register.md` — for PQ responses: code, resubmission dates
- `Technical_Office/Specialist_Management/prequalification_log.md` — specialist appointment lifecycle (especially for PQ responses)
- `Technical_Office/Specialist_Management/specialist_register.md` — specialist status, candidate names, stage (especially acoustic, landscaping, lab specialists)
- `01_Registers/subcontractor_package_register.md` — package-level status updates for acoustic, landscaping, setwork, lab packages
- `01_Registers/arch_drawing_register.md` and/or `01_Registers/drawing_register.md` — status per drawing package
- `00_Status/action_items.md` — new actions for Code C (revise) or Code B (proceed with hiring/next stage)
- `03_Plans/02_Stakeholder/CG_STATUS.md` — if stakeholder-specific
- `00_Command_Center/master_dashboard.md` — if key milestones change

Apply updates in order: submittal register first (source of truth), then specialist/log registers (derived), then action items (new work generated). This prevents stale references.

### Phase 6 — Archive
Log the batch to `03_Plans/08_Risk/reviews/email_scan_YYYY-MM-DD.md` with YAML frontmatter (last_updated, owner_agent: Hermes, status: active, source). This log serves as the dedup reference for the next scan.

**Pitfall — a decision/analysis doc is NOT done until it is LINKED into the registers.** Creating a standalone `.md` (decision log, risk analysis, discussion outcome) in `09_Agent_Workspace/` and committing it is only half the job. The user expects it wired into the repo's index/registers so it is discoverable from the source-of-truth rows. For a decision that changes a submittal's status, you must ALSO: (a) update the relevant `01_Registers/submittal_register.md` row (status + a `**Decision log:** <path>` pointer), (b) update the affected `00_Status/action_items.md` row, and (c) append an entry to `09_Agent_Workspace/handoff_log.md`. Commit all together. A file committed but not linked is "طايف" (floating) — the user will flag it. Verified 2026-08-27: the structural cloud survey decision log was committed alone; user asked "ازاي ربط هذه المناقشه بالمشروع هل هملت index معين؟" — the fix was linking it into the ZD-0106 submittal row, the M14-6.2 action item, and the handoff log.

**Dedup step (do this BEFORE classifying NEW vs already-reported):** Read the most recent `email_scan_*.md` in `03_Plans/08_Risk/reviews/` (e.g. `ls -t ... | head -1`) and compare its refs/subjects against the current query results. Anything already in the last log is NOT new — skip it. Only items absent from the last log get 🆕/⚠️ status. This is what makes the "only report NEW since last check" requirement reliable; without reading the prior log you risk re-reporting the same Aconex transmittals every run.

**Pitfall — a doc can already be a register row from a DIFFERENT source (email vs Adel bank sync vs document_intake).** Before inserting a submittal row, `grep -n "<doc-ref>" 01_Registers/submittal_register.md` FIRST — a document you got from an email may have been added as a register row by a sibling agent from the Adel bank folder scan (or vice-versa). If the ref is already present, UPDATE that existing row (append the CG code / Aconex ref / date) instead of inserting a second row. Verified 2026-08-23: `1E0-1G-0007` (AV Package Part II) ended up as TWO rows — one from the email scan (SIC.-WTRAN-000190) and one from an earlier Adel bank sync — because the insert didn't grep the register for the ref first. The email/bank/dashboard pipelines each run in their own session, so a ref can legitimately pre-exist from a source you didn't query. Grep the register (and action_items.md) for the exact doc ref before ANY append.

**Pitfall — a doc ref can be MISLABELED with the wrong title in the register (Adel-bank-sync collision).** A register row may carry the correct doc ref but the WRONG document title, because the Adel bank folder sync (or a sibling agent) filed a different document under that ref. Example (2026-08-29): `submittal_register.md` listed `MOC-MUS-ASE-1C0-ZD-0114` as "Plan for Concrete Core Test Location" (from an Adel bank sync), but the CG response PDF authoritatively titled it "Design Deliverables Tracker – Structural Analysis & Design" (Code C). The "Plan for Concrete Core Test Location" is actually **ZD-0110** (already Code B). **Rule: when a CG response arrives, the CG email subject + response PDF title are authoritative over the register's title.** Before writing a CG code to a row, verify the doc ref maps to the correct title — grep the register for the ref AND read the CG PDF's DS-form "DESCRIPTION" field. If the register title disagrees with the CG PDF, the register row is mislabeled and must be corrected (title + status), not just code-updated.

**Pitfall — a doc can already be a register row under a DIFFERENT ref number (sibling ExportDocs collision).** It's not only identical refs that collide. A sibling agent (e.g. `ExportDocs` Aconex sync) may register the SAME document under a ref whose trailing digits differ from the one you derived from the email preview — e.g. the same waste-disposal NCR logged as `NC-1KH-0021` by the sibling vs the `NC-1KH-021` I inferred. **Rule: before committing, `git fetch` + check for a sibling's row that matches the document SUBJECT (not just the ref) — the same subject under a close-but-different number is the same doc.** When a sibling's ref already exists for that subject, DROP your row and keep the sibling's number (treat the sibling ExportDocs ref as authoritative — it came from the actual source doc, your email-preview inference may have dropped a digit). Flag the dedup in the commit message and scan log. Verified 2026-08-29: NC 1KH-021 vs 1KH-0021 — kept sibling's `NC-1KH-0021`, removed mine, noted it in `email_scan_2026-08-29-pm.md`.

**Pitfall — Python row-insert can GLUE the new row onto the previous line (missing newline).** When inserting a register row via the `readlines` + `lines.insert(i+1, new_row)` pattern, if the anchor line you matched does NOT end in `\n` (or your insert points mid-row), the new row concatenates directly onto the previous row's line instead of starting a fresh line. Symptom: a rendered table row appears as `...previous cell... || 159 | ... |` on ONE line. **After ANY row insert (Python or `patch`), re-read the inserted area and verify the new row begins its own line and the previous row still terminates cleanly.** Fix by inserting `\n` before the new row's content if the anchor lacked a trailing newline. Verified 2026-08-29: PQ-0153 row glued onto the PQ-0152 line in `prequalification_register.md`; had to split the line back into two.

**Pitfall — grep the register BEFORE adding an action item (backfill dedup).** During long backward-chronological backfill (process date-by-date from recent to old), many email threads were already captured on an earlier forward pass — the doc code (ZD/PQ/1G/SI ref) is already a row in `submittal_register.md`, and the corresponding action is already in `action_items.md` (from the forward run or the reply thread). Before adding a NEW action or register row for a batch, `grep -in "<doc-ref>|<keyword>" 00_Status/action_items.md 01_Registers/submittal_register.md` first. If the ref is already tracked, skip it — only add rows for genuinely NEW items (e.g. a CG code change on an existing row, or a distinct new request like "provide 2 alternative manufacturers" not previously logged). This prevents the register from accumulating duplicate rows for the same document. Concretely in the Jul 2026 backfill, most 12–15 Jul emails (ZNA/AD agreements, 1G-0001, ZD-0020/0082/0076/0081/0093, PQ-0105, ZD-0064, TQ-0021, NCR-1KH-009) were already registered — only a handful (ZD-0006 Rev.05 Code B, MA-0007 manufacturer request, CG Recovery Plan, AD Eng 15% advance) were genuinely new.

### Phase 7 — Build / Update Submission Register
See `references/email-deliverables-to-submission-plan.md`.

### Phase 8.5 — Extract & Analyze Document Content (for PQ / specialist / vendor documents)

After filing attachments to OneDrive and updating registers, the next step is extracting document intelligence — reading the actual content to understand each specialist's capabilities, CG comments, and clearance path.

**Tools:** `pdftotext` (brew-installed poppler) for PDFs, `openpyxl` for XLSX, `zipfile` for ZIP contents.

**Workflow:**
1. Run a batch extraction script that walks the filed document tree and converts each PDF/XLSX/ZIP to text under a common `_Text_Extracts/` directory
2. Some PDFs are image-based (scanned CE DoCs, authorization letters) — pdftotext returns empty; flag them as image-based
3. Delegate document analysis to sub-agents in parallel (one per specialist group): each reads text extracts and produces structured MD knowledge

### Phase 9 — Knowledge Document Generation (New)

After register updates are committed, generate specialist knowledge MDs from the document extracts. This creates a searchable knowledge base that future sessions can reference instead of re-extracting attachments.

**Sub-agent delegation pattern (parallel document analysis):**
```
Delegate parallel sub-agents, one per specialist group:
  - Group A: Acoustic specialists (3-4 candidates)
  - Group B: Landscaping + lab specialists
  - Group C: AV vendors + materials
```

Each sub-agent receives:
- Paths to text extracts in `_Text_Extracts/`
- The `pq_knowledge/` output directory
- The knowledge MD format specification

**Standard knowledge MD format per specialist:**

```markdown
## PQ-012X [SPECIALIST NAME]
**CG Code:** X (Code description) | **Submitted:** date | **Key Offering:** one-liner

### Company Profile
- Founded, HQ, leadership, team size, classification/certifications
- Local content (Nitaqat, Saudization, Saudi HQ)

### Scope Offered / Products
- Specific products / services proposed for the project
- Quantities, locations, BOQ references where available

### Certifications / Docs on File
| Certification | Standard | Expiry |
|---|---|---|

### CG Comments Summary
> **Status:** Code X
> **Reviewer:** Name
> **Comments:** numbered list from CG response

### Path to Clearance
1. Action item 1
2. Action item 2

### Relevant Docs on File
| File | Description |
|---|---|
```

**Save location:** `Technical_Office/Specialist_Management/pq_knowledge/<specialist_group>.md`
**Commit with registers** — knowledge files are part of the repo, updated alongside register changes.

**Pitfall — CG codes may be blank on forms:** The CG code shown on the submitted PQ review sheet may not match the code delivered by email. The CG email from Hossam Mabrouk is authoritative. Cross-check: if the form says nothing but the email says `B - Approved` or `C - Revise`, trust the email. Annotate the knowledge MD with `— per CG email from <sender> (<date>)`.

### Phase 10 — Git Commit & Push (REQUIRED for repo-based registers)

After updating all registers in the git repo (`aseer-museum-pm`), the user expects a **git commit + push to GitHub**, not just OneDrive file saves.

```bash
cd /Users/mohamedessa/aseer-museum-pm
git add -A
git commit -m "Email scan YYYY-MM-DD: <summary of key changes>"
git push origin main
```

**Pitfall — post-commit hook regenerates `index.html`:** The repo has a post-commit hook that auto-rebuilds the risk register and lessons learned web apps. This modifies `06_Risk_System/webapp/src/index.html` after every commit. If the remote has a newer version of this auto-generated file, `git pull --rebase` will fail with "Your local changes would be overwritten". **Workaround:** use `git push origin main --force` (the index.html is auto-generated, so force-push is safe). Alternatively, `git checkout 06_Risk_System/webapp/src/index.html` before pulling to discard the local auto-generated copy.

**Pitfall — "dd you deploy?" means git push:** When the user asks "did you deploy?" or "dd you deploy?" after register updates, they are asking whether the changes were committed and pushed to the GitHub repo, not whether OneDrive files were saved. Always include the git commit+push step in the workflow and report the commit hash.

**Pitfall — "Final transmittal" ≠ Approved for PQs:** Aconex transmittal notes sometimes label a CG response as "Final transmittal" even when the CG code is C (Revise & Resubmit) or B (Approved w/ Comments). Never mark a PQ "Final" in the register based on transmittal subject line alone — always read the actual CG code from email preview or the attached response PDF. The code A/B/C/D in the CG email body governs, not the transmittal classification. Example from 2026-07-23: PQ-0126 PINE was labelled "Final transmittal" in Aconex but the CG response was Code C.

**Pitfall — Git push conflicts with post-commit hooks:** The `aseer-museum-pm` repo has a post-commit hook that auto-regenerates `06_Risk_System/webapp/src/index.html` after every commit. After `git commit`, `index.html` has unstaged changes. Two approaches:

**Simple approach (no remote divergence):** Discard the auto-generated copy and push:
```bash
git checkout -- 06_Risk_System/webapp/src/index.html
git push origin main
```

**Stash approach (when remote has new commits):** The post-commit hook leaves `index.html` dirty. When you then `git fetch && git rebase origin/main`, the dirty file causes a merge conflict. Clean sequence:
```bash
git add <your register files>
git commit -m "..."
git stash                              # save the post-commit dirty state
git fetch origin && git rebase origin/main
git stash pop                          # may conflict in index.html — accept theirs
git checkout --theirs 06_Risk_System/webapp/src/index.html  # if conflicted
git add 06_Risk_System/webapp/src/index.html
git commit -m "merge: accept remote index.html"
git push origin main
```

This avoids force push in most cases. The simple `git checkout --` approach works when you haven't fetched/rebased — the post-commit hook's auto-generated file is identical to what's on remote, so discarding it is safe.

**Pitfall — PQ updates cascade to TWO registers, not one:** Unlike ZD or MS submissions which update a single submittal register row, a prequalification (PQ) email batch typically updates two repo files:
1. `01_Registers/prequalification_register.md` — the full PQ list with refs, codes, dates
2. `Technical_Office/Specialist_Management/prequalification_log.md` — a curated specialist tracking log with CG code → MoC approval state machine

Always update both. The register is the full list; the log tracks the appointment lifecycle (OPEN → SUBMITTED → CG-CODE → MoC-APPROVED). Updates to the log must also update the roll-up section with new counts.

## Direct Attachment Extraction (fallback — AppleScript is preferred)

See `references/olk15-attachment-parsing.md` for the file format specification.

**When AppleScript `save` fails (-2700, 0-byte files) AND the `Mail_OwnedBlocks`/`Blocks` join returns no rows, the attachment bytes are still on disk** in `Message Attachments/<NN>/` — where `<NN>` matches the subdir of the email's `PathToDataFile` (`Messages/<NN>/...`). The `.olk15Message` is a binary pointer (no PDF base64 inside); the real `.olk15MsgAttachment` MIME files live in the `Message Attachments` dir. See `references/attachment-location-message-attachments-dir.md` for the scan recipe and the shared-dir false-positive pitfall.

## Direct Body Extraction from .olk15Message (No AppleScript)

When AppleScript `message id N` fails on Outlook 16.90+ (error -1700) or is unavailable, the full email body can be extracted directly from the `.olk15Message` file on disk. The file has a 20-byte binary header followed by raw MIME content including HTML body.

**Works for:** Standard MIME emails with HTML content.
**Does NOT work for:** TNEF-encoded emails (`Content-Type: application/ms-tnef`) — the body is encoded inside the TNEF stream and requires a TNEF decoder.

See `references/olk15message-body-extraction.md` for the complete extraction pattern with Python code.

## TNEF (winmail.dat) Decoding

Some Outlook emails (especially from Exchange/Outlook senders) use Microsoft TNEF format (`Content-Type: application/ms-tnef; name="winmail.dat"`). The body is NOT directly extractable from the `.olk15Message` file.

**Tool available:** `tnef` (installed via `brew install tnef`). Usage:
```bash
tnef /tmp/email_winmail.dat -C /tmp/tnef_output/
```

**Limitation:** The TNEF data is stored inside the `.olk15Message` file in a proprietary binary structure, not as a separate MIME part. Extracting the raw TNEF stream from the binary requires finding the TNEF magic bytes (`0x78 0x9f 0x3e 0x22`) within the file, which may not be present in all cases. When the TNEF data is embedded in the binary header area (before the MIME headers), it cannot be extracted by simple byte search.

**Workaround:** For TNEF emails, the `Message_Preview` column in SQLite provides the first **255 chars** (measured 2026-08-15, NOT ~500). For full body, AppleScript is the only reliable method.

### Base64 PDF extraction from .olk15MsgAttachment (no AppleScript)

When AppleScript fails or is unavailable, Outlook `.olk15MsgAttachment` files can contain MIME-encoded attachments with base64-encoded bodies. Works for `.pdf`, `.docx`, `.xlsx`.

**⚠️ CRITICAL: The marker format is `Content-transfer-encoding: base64\r\r` (two CRs, not \r\n).** The base64 data starts at offset +35 from the marker. Searching for `base64` alone or using `idx+7` will produce corrupted output. See `references/olk15-base64-extraction-corrected.md` for the corrected extraction pattern.

**Finding the path — Mail_OwnedBlocks join to Blocks:**
```sql
SELECT mb.Record_RecordID, mb.BlockTag, b.PathToDataFile
FROM Mail_OwnedBlocks mb
JOIN Blocks b ON mb.BlockID = b.BlockID
WHERE mb.Record_RecordID = <EMAIL_ID>;
```
Path is relative to `Data/` — construct full path:
`~/Library/Group Containers/UBF8T346G9.Office/Outlook/Outlook 15 Profiles/Main Profile/Data/<PathToDataFile>`

**Pitfall — multiple attachments per email:** Each attachment gets its own row in `Mail_OwnedBlocks` with a distinct `BlockID`. Check for multiple rows.

**Pitfall — image-based PDFs:** CAD/stamped drawings and scanned contracts return empty `pdftotext`. For a **single-page** image PDF, `sips -s format jpeg file.pdf --out out.jpg` + `tesseract` works. For a **multi-page** scanned PDF (contracts, stamped agreements), `sips` only converts **page 1** — use `pdftoppm` per page instead:
```bash
pdfinfo file.pdf | grep -i pages          # get page count first
pdftoppm -f N -l N -r 150 -jpeg file.pdf /tmp/pg   # one page at a time
tesseract /tmp/pg-N.jpg - 2>/dev/null | grep -iE "SAR|fee|payment|%|total|milestone"
```
`pdftoppm` names output `prefix-NN.jpg` (zero-padded, e.g. `pg2-02.jpg` for page 2) — glob the actual filename, don't assume `-01`. Loop pages 2..N to read fees/payment/milestone clauses. 150 DPI is enough for OCR.

## Reference files

- `references/python-applescript-generator.md` — Python generator pattern for batch AppleScript extraction (cron-safe, under byte limit, with sanitization)
- `references/batch-email-routing.md`
- `references/register-log-reconciliation.md`
- `references/exportmailin-analysis.md`
- `references/submission-plan-and-schedule-workflow.md`
- `references/email-thread-analysis.md`
- `references/cron-24h-email-scan.md` — cron scan pattern, dedup, multi-project reporting, iCloud EDEADLK workarounds
- `references/olk15-attachment-parsing.md`
- `references/olk15-attachment-locate-by-content.md` — find a specific `.olk15MsgAttachment` by content (random GUID filename) via `grep -E` on a unique doc-ref substring + `-newermt` bound, then base64-decode from the `JVBERi0` (`%PDF-`) marker; for when AppleScript `save` fails
- `references/attachment-location-message-attachments-dir.md` — when AppleScript `save` fails AND the `Mail_OwnedBlocks`/`Blocks` join is empty, the attachment bytes live in `Message Attachments/<NN>/` (same numeric subdir as the email's `Messages/<NN>/`); scan recipe + shared-dir false-positive pitfall
- `references/aconex-email-patterns.md`
- `references/aconex-register-update-workflow.md` — Aconex transmittal → submittal register dedup workflow (cron-safe, pipe-alignment pitfalls)
- `references/email-to-submission-plan.md`
- `references/cg-schedule-extraction.md`
- `references/forwarded-document-analysis.md`
- `references/email-chain-tracing.md`
- `references/cg-email-triage.md`
- `references/evidence-based-correspondence-triage.md` — triage contractor/vendor info-request lists evidence-first (check registers + live Outlook before calling anything "obstruction"); PVC already approved, ICT appointed 18-Aug, real gap = BMS. User rule 2026-08-23: answers must be مدعمة بالدليل
- `references/cg-correspondence-analysis.md`
- `references/specialist-delay-assessment.md` — identifying which design specialists are genuinely late: cross-ref vendor-domain emails + Design Phase Deliverables Tracker xlsx + repo registers; distinguish technical vs procurement vs client-blocked delay; pitfalls (Landscape "not appointed" vs "identified-not-appointed", Acoustic "PQs under review" vs "contract already signed"); ALSO the drafting-email-to-PM variant — verify live contracting status from Outlook before listing design risks (MEP execution contractor = the true gap vs advanced MEP design; correct specialist name is TLC not "TSC"; acoustic/ICT already signed)
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
- `references/pq-email-processing.md` — PQ-specific workflow: sender mapping, two-phase processing (draft vs formal), CG code extraction from preview, dual-register cascade, pitfalls (Final transmittal ≠ Approved)
- `references/multi-project-routing-script.py` — Reusable Python router for multi-project email attachment routing (Aseer, Zamzam, Jabal Omar). Document-code-based patterns, OneDrive paths, dedup handling.\n- `references/electrical-compliance-report-cascade.md` — Electrical Compliance & Understanding Report → assessment + risk register cascade (missing-reports & Code-C systems risk, Aconex attachment=0 handling)
- `references/test-result-compliance-report.md` — lab test-result submittals (e.g. SMITS concrete-core compressive report): no A/B/C/D code, caught only via sender/folder filter; parse the pass/fail verdict from the PDF (`pdftotext -layout`), cite as EVIDENCE against the structural-verification risk (`PRR-SIT-02`/`PRR-DES-07`, ZD-0110/0114), not a new risk. Don't edit registers without approval — report out first.
- `references/screen-ocr-fallback.md` — read on-screen text (live meeting captions, dialogs, terminal output) via `screencapture` + Swift Vision OCR, for sessions without `computer_use` or when the model lacks vision
- `references/onedrive-fileprovider-write-block.md` — macOS File Provider (OneDrive.appex) blocks ALL programmatic writes into OneDrive trees (`cp`/`ditto`/`mv`/`os.sendfile`/`shutil.copy2`/Finder `duplicate` = `Operation not permitted` / -8004), even with OneDrive killed (extension re-launches). Stage on `/Volumes/MIcro/Temp/`, `open` both folders, user drags manually. Only drag works. Ship a `_FILE_MAPPING.csv` beside staged files.
- `references/git-post-commit-hook-conflict-loop.md` — full break-the-loop recipe for the `aseer-museum-pm` post-commit webapp-regen hook: commit `--no-verify` to stabilise, `checkout --theirs` for auto-gen conflicts, `GIT_EDITOR=true git rebase --continue`, drop stale stashes, merge remote register rows
