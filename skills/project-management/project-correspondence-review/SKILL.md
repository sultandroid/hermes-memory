---
name: project-correspondence-review
description: "Check emails from a specific project sender (NRS, CG, AD Engineering, ZNA, etc.), cross-reference against all repo registers, identify gaps, update registers, and extract user action items."
tags:
  - outlook
  - email
  - registers
  - gap-analysis
  - project-management
---

# Project Correspondence Review — Ad-Hoc Sender Check + Cross-Register Gap Analysis

Use when the user asks to "check" or "review" emails from a specific person or company (NRS, CG, AD Engineering, ZNA, Rawasin, etc.) — not a full pipeline scan, but a targeted look at one sender's recent activity.

## Workflow

### 1. Query the sender's recent emails

```sql
SELECT datetime(Message_TimeSent,'unixepoch') as sent,
       Message_NormalizedSubject as subject,
       substr(Message_Preview,1,200) as preview
FROM Mail
WHERE Message_SenderList LIKE '%Jim Richards%'
  AND Message_NormalizedSubject NOT LIKE '%Invoice%'
ORDER BY Message_TimeSent DESC
LIMIT 20;
```

Adjust the `LIKE` pattern for the target sender. Exclude noise patterns:
- `NOT LIKE '%Invoice%'`
- `NOT LIKE '%anonymous access%'`
- `NOT LIKE '%shared the folder%'`
- `NOT LIKE '%has changed%'`
- `NOT LIKE '%has created%'`

### 2. Read previews to understand context

The `Message_Preview` column contains the first ~200 chars of the email body. This is enough to identify:
- Whether the sender is on leave / unavailable (OOO auto-reply)
- Key deliverables sent or requested
- Issues flagged (scope disputes, process questions, technical concerns)
- Who to contact in their absence

### 3. Cross-reference against ALL repo registers

For each substantive email, check:

| Register | File | What to look for |
|----------|------|------------------|
| Submittal Register | `01_Registers/submittal_register.md` | Is the deliverable tracked? Status match? |
| Change Register | `01_Registers/change_register.md` | Did they flag something as out-of-scope? Log as pending VO. |
| Deliverables Register | `Technical_Office/deliverables_register.md` | Is the design study / report / drawing listed? |
| Risk Register | `01_Registers/risk_register.md` | Does the issue map to an existing risk? If not, new risk needed? |
| RFI Register | `01_Registers/rfi_register.md` | Any TQs referenced? |
| NCR Register | `01_Registers/ncr_register.md` | Any NCRs mentioned? |
| Letters Register | `01_Registers/letters_register.md` | Any formal correspondence? |

### 4. Identify gaps and update

For each gap found:

| Gap | Action |
|-----|--------|
| Missing variation | Add row to change_register.md, update summary counts (Total, Pending) |
| Missing deliverable | Add row to deliverables_register.md with phase, discipline, status |
| Missing risk | Add to risk_register.md (only if not already covered by existing risk) |
| Stale status | Update the register row to match current state from email |
| Cross-link | When adding a VO, also add the corresponding deliverable and link them (e.g. "Linked to VO-001") |

### 5. Extract user action items

After updating registers, identify what the user personally needs to do:

- **Forward information** to someone else (the sender's colleague, if sender is on leave)
- **Draft content** the sender requested (text, appendix, data)
- **Approve/review** a draft the sender sent
- **Respond** to a question the sender asked
- **Escalate** an issue the sender flagged

Present these as a short bullet list. If nothing is urgent, say so.

## Pitfalls

- **Epoch varies** — always verify with the Step 0 query from the email-pipeline-automation skill. Some Outlook DBs use Mac absolute epoch (+978307200), others use Unix epoch.
- **Preview truncation** — `Message_Preview` is ~200 chars. For full body, you'd need to extract the email via AppleScript or find the `.olk14Message` file. For gap analysis, the preview is usually sufficient.
- **Duplicate subjects** — the same email may appear multiple times (sent to multiple recipients). Deduplicate by subject + timestamp within a few seconds.
- **OOO auto-replies** — filter these out when counting substantive emails. They have the same subject as the original but the preview starts with "I am away".
- **Invoice emails** — always exclude from substantive analysis unless the user asks about payments.
- **SharePoint notifications** — "has created an anonymous access link" and "shared the folder" are not substantive emails. Skip them.
- **Cross-register consistency** — when you add a VO to the change register, also add the corresponding deliverable to the deliverables register, and link them. Don't update one without the other.
- **User action items are not register entries** — present them as a separate list after the register updates. The user needs to know what they personally must do, not just what was logged.
- **Sender on leave** — if the sender is on annual leave, note their return date and who to contact in their absence. The user's action items may need to go to a colleague instead.
- **Risk register is already comprehensive** — most project issues are already tracked as PRR risks. Check carefully before adding a new risk. The existing risk may cover the issue under a broader description.

## Email-to-SOW Pipeline

When the user asks to "check all emails from [supplier]" and the emails contain SOW documents, contracts, or submission plans, the workflow extends beyond correspondence review into SOW filing.

### Step 1: Query all emails from the supplier

```sql
SELECT m.Record_RecordID as id,
       datetime(m.Message_TimeReceived, 'unixepoch', 'localtime') as received,
       f.Folder_Name as folder,
       m.Message_SenderList as sender,
       m.Message_SenderAddressList as email,
       m.Message_NormalizedSubject as subject,
       m.Message_HasAttachment as att
FROM Mail m
JOIN folders f ON m.Record_FolderID = f.Record_RecordID
WHERE m.Message_SenderAddressList LIKE '%@supplierdomain%'
   OR m.Message_SenderAddressList LIKE '%@adeng%'
   OR m.Message_NormalizedSubject LIKE '%Supplier Name%'
ORDER BY m.Message_TimeReceived DESC;
```

### Step 2: Extract all attachments

Write individual `.applescript` files (one per email ID) to avoid the ~700-byte AppleScript body limit:

```applescript
set outFolder to "/tmp/supplier_attachments/"
tell application "Microsoft Outlook"
    set eidVal to <EMAIL_ID>
    set theMsg to message id eidVal
    set atts to (every attachment of theMsg)
    repeat with att in atts
        if content type of att does not start with "image/" then
            set attName to name of att
            set savePath to outFolder & "<EMAIL_ID>_" & attName
            do shell script "touch " & quoted form of savePath
            save att in (POSIX file savePath as alias)
        end if
    end repeat
end tell
```

Run sequentially: `osascript /tmp/extract_<id>.applescript`

### Step 3: Read key documents

- **DOCX agreements**: `textutil -convert txt -stdout <file>.docx`
- **PDF SOWs**: `pdftotext <file>.pdf -`
- **XLSX plans**: Python openpyxl to read sheets

### Step 4: File to repo

```bash
cp /tmp/supplier_attachments/<id>_<file> "03_Scope/<Package_Name>/<file>"
```

### Step 5: Create SOW README + update registers

See `subcontractor-sow-audit` skill for the full 3-layer system (SOW, submission plan, tracker).

### Step 6: Report action items

After filing, tell the user:
- What documents were found and filed
- What gaps were identified (missing SOW clauses, unconfirmed obligations)
- What needs their action (sign agreement, review draft, approve scope)
