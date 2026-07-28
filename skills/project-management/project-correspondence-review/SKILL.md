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
- **Cross-register consistency** — when you update one register, update every related register in the same pass. The user spots inconsistencies.
- **User action items are not register entries** — present them as a separate list after the register updates. The user needs to know what they personally must do, not just what was logged.
- **Sender on leave** — if the sender is on annual leave, note their return date and who to contact in their absence. The user's action items may need to go to a colleague instead.
- **Risk register is already comprehensive** — most project issues are already tracked as PRR risks. Check carefully before adding a new risk. The existing risk may cover the issue under a broader description.
- **Distinguish "reference to X" from "X itself"** — when a risk register or action item says "NRS comments on 57 pre-contract drawings", the risk is a *reference* to the comments, not the comments themselves. The user wants the actual source document, not the risk description quoting it back at them. Find the source (email attachment, drawing PDF, remarks table) — don't echo the risk entry.
- **OneDrive placeholders cannot be read** — files returning "Resource deadlock avoided" or null bytes have not synced locally. Do not brute-force read them. Instead find cached copies in Outlook attachments, Adel snapshots, or the repo.
- **NRS comment PDFs are image-only** — NRS stamped/redlined drawing PDFs are scanned AutoCAD plots. pdftotext and OCR return empty output. Open in PDF viewer.
- **Pipeline confirmed ≠ pipeline completed** — confirming a pipeline cron job ran successfully is not enough. You must read the extracted documents, understand their content, and take action (update registers, notify user of findings). Running the pipeline and reporting "ok" without reading the output will be corrected by the user. After extraction, always: read → understand → route → update → report with actual findings.

## OneDrive Placeholder Workaround

Many project files in the local OneDrive tree are cloud-only placeholders that return "Resource deadlock avoided" on any read attempt. Valid alternatives:

1. **Outlook SQLite** — email previews (`Message_Preview`) contain sender, subject, and CG response codes. Attachment names found in the `Files` virtual table.
2. **Adel Darwish snapshots** — `99_Archive/adel_snapshots/file_list.txt` lists all files in Adel's OneDrive with sizes and dates. Presence of an `Approval/` subfolder confirms CG has responded.
3. **Repo registers** — `01_Registers/prequalification_register.md`, `01_Registers/submittal_register.md`, `Technical_Office/Specialist_Management/specialist_register.md` have structured data.
4. **Aconex notification emails** — `noreply@aconex.com` notifies when transmittals are processed.
5. **Outlook cached attachments** — under `~/Library/Group Containers/UBF8T346G9.Office/Outlook/.../Files/S0/2/Attachments/0/`. These are the actual PDFs if they were cached. Not all attachments are cached.
6. **Document Control folder** — `~/Documents/Asher_Regional_Museum_Document_Control/` has `.md` summary files and some cached content. Files with `status: active` in the frontmatter are placeholders; larger files (non-zero `file_size`) may have extractable text.

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

### Step 3: Read key documents — extract CG comments and CRS data

**Do not file by filename alone.** Read the document content first. The CG rejection reason, status code, and action items are in the document body, not the filename.

- **DOCX agreements**: `textutil -convert txt -stdout <file>.docx`
- **PDF submittals/DS forms**: `pdftotext <file>.pdf -` — extract the **CG Comments** field (near bottom, labelled "CG Comments:" or "ملاحظات المهندس المشرف"). This is the authoritative rejection reason — quote verbatim, never paraphrase.
- **PDF CG response attachments**: Same method. The DS form's status code (A/B/C/D) and CG reviewer's signature block are at the bottom of page 1. Read them.
- **Excel CRS files** (CG Comment Resolution Sheets): Use Python openpyxl with `data_only=True`. Count Open vs Closed comments per column. Extract each comment: section reference, CG requirement, status. The CRS is where CG documents exactly what must change — do not skip it.
- **Image-based PDFs** (renders, scanned dwgs): `pdftotext` returns empty. Note as image-based and move on.
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

## Finding a Specialist by Scope / Doc Code Cross-Reference

When the user asks "who does the [scope] assessment?" and you need to identify which company performs a specific scope of work (e.g. electrical testing, BMS assessment, mechanical survey):

### 1. Start with the PQ register — NOT email guessing

**First step: check the prequalification register in the repo.** This is the authoritative vendor-by-discipline list.

```
01_Registers/prequalification_register.md
```

Search for the discipline (e.g. "1M0") or the scope keyword. The register maps: PQ ref → Scope description → Company name → CG code.

Do NOT start by guessing from email subject lines or file names. The user will correct you if you guess wrong.

### 2. Identify the PQ / doc code pattern

Most specialist subcontractors are registered via a Prequalification (PQ) document code. The discipline code in the PQ ref tells you the scope:

| Discipline Code | Scope |
|----------------|-------|
| 1E0 | Electrical |
| 1M0 | Mechanical |
| 1C0 | Civil |
| 1KH | HSE |
| 1A0 | Architecture |

For example, `PQ-0084` with code `1M0` = Mechanical testing & assessment.

### 3. Search Outlook SQLite for the company's reports

Once the company name is confirmed from the PQ register, search their doc codes in Outlook to find their actual work products:

```sql
-- Find all assessment reports by this specialist's discipline
SELECT DISTINCT m.Message_NormalizedSubject as subject
FROM Mail m
WHERE m.Message_NormalizedSubject LIKE '%1M0-ZD-%'  -- change discipline code
ORDER BY m.Message_NormalizedSubject;
```

The discipline code + doc type pattern is critical:
- `ZD` = Design/Assessment report
- `RP` = Report  
- `MS` = Method Statement
- `IR` = Inspection Request

### 4. Cross-reference against multiple sources (triangulation)

**Do NOT rely on any single source.** Always check at least three:

| Source | What it reveals | Limitation |
|--------|----------------|------------|
| **Outlook SQLite** (`Message_Preview`) | CG response codes (B/C), submission dates, sender/recipient | Preview truncated ~200 chars; CG codes only visible in CG-sent emails |
| **Adel Darwish folder snapshot** (`99_Archive/adel_snapshots/file_list.txt`) | Approval folder presence, file dates, Rev.01/Rev.02 cycles | Only covers files copied to Adel's folder; may be stale |
| **Repo registers** (PQ, submittal, specialist) | Company names, scope descriptions, status codes | May lag behind live Aconex status |

**Key insight:** A CG response may exist as a PDF in the Adel snapshot's `Approval/` folder even when no CG email appears in Outlook. The "Approval" subfolder next to a submission doc (e.g. `.../ZD-0065/Approval/MOC-MUS-ASE-1M0-ZD-0065.pdf`) confirms CG has reviewed it.

### 5. Query assessment report CG status

For each report found, check CG status:

```sql
SELECT datetime(m.Message_TimeReceived, 'unixepoch') as dt,
       m.Message_NormalizedSubject as subject,
       m.Message_SenderAddressList as sender,
       CASE WHEN m.Message_Preview LIKE '%B -%' THEN 'Code B'
            WHEN m.Message_Preview LIKE '%C -%' THEN 'Code C'
            WHEN m.Message_Preview LIKE '%A -%' THEN 'Code A'
            ELSE substr(m.Message_Preview, 1, 60)
       END as code
FROM Mail m
WHERE m.Message_NormalizedSubject IN (
    'MOC-MUS-ASE-1M0-ZD-0065 / HVAC Testing & Assessment Report'
    -- list each report subject
)
  AND m.Message_SenderAddressList LIKE '%@cg.com.sa%'
ORDER BY m.Message_TimeReceived DESC;
```

Note: Some reports get recalled and reissued (e.g. "would like to recall the message" → reissued with different code same day). Check for both C and B on the same doc.

### 6. Check the Aconex notification trail

Some submittals go via Aconex and CG responds there, not by direct email. Search for Aconex notifications:

```sql
WHERE m.Message_SenderAddressList = 'noreply@aconex.com'
  AND m.Message_NormalizedSubject LIKE '%ZD-00%'
```

Aconex emails contain workflow transmittal numbers but rarely the CG code itself — use the Adel snapshot `Approval/` folder as backup.

### 7. Build a tracker

Create a structured tracker in `03_Scope/<Company>/README.md` with:
- Company info + PQ ref + CG code
- Table of all submitted reports with doc ref, title, submission date, CG code, status
- For reports submitted in the same batch (e.g. 8 reports on 23-Jul), note which have CG responses and which are still pending
- Summary row with counts: Approved (B), Rejected (C), Pending, Closed

### 8. Update all registers consistently

When adding a new specialist or updating report status, update ALL of these:

| Register | What to update |
|----------|---------------|
| `01_Registers/prequalification_register.md` | PQ row notes with report refs and status |
| `01_Registers/submittal_register.md` | Assessment Reports Dashboard section |
| `Technical_Office/Specialist_Management/specialist_register.md` | Tier 3 entry with report counts |
| `01_Registers/risk_register.md` | PRR-MEP risk with current pending count |
| `03_Scope/<Company>/README.md` | Full report tracker |

Do not update one register in isolation — the user will spot the inconsistency.

### 9. Report clearly

When presenting findings, use a table format with:
- Company name + PQ ref + CG approval code
- Report-by-report status with doc refs and dates
- Clear summary: what's done, what's pending, what needs resubmission
- Distinguish "no CG response yet" from "no response found in this source"

## Extended Workflow: NCR / Formal Letter Procedural Audit

When CG issues an NCR or formal warning letter (LT), audit its procedural validity against the Communication Plan, DMP, and scope documents before responding. This determines whether to contest (procedural defects found) or comply (procedurally clean).

### What to Check

| Check | What to Verify | Document Reference |
|-------|---------------|-------------------|
| **Channel** | Was instruction sent via Aconex C1 or direct email C2? | Communication Plan §6.1 |
| **Recipient** | Correct escalation tier (L1-L5)? | Communication Plan §7.1 |
| **Scope** | Is the demanded action in scope / in DMP? | DMP, SOW, Risk Register |
| **Timeline** | Is the deadline appropriate for the tier SLA? | Communication Plan §7.1 |
| **NCR validity** | Proper escalation chain (SI → NCR → LT)? Proper use of NCR mechanism? | DMP §8.5, Communication Plan §8.5 |

### Reference File

See `references/ncr-procedural-audit.md` for the full 5-point audit checklist with clause references, verdict format, and worked examples (NC-1G0-0019 vs LT-003).

## Pitfall: OneDrive placeholders for submittal docs

PQ documents and assessment reports are often stored in OneDrive submittal folders that return null bytes or "Resource deadlock avoided" when read. **Do not rely on the OneDrive project folder for document content.** Use:
1. **Outlook SQLite** (`Message_Preview`) for email content and CG codes
2. **The repo** (`/Volumes/MIcro/Temp/aseer-museum-pm/`) for prequalification registers, SOW summaries, and specialist trackers
3. **Aconex notification emails** (sender `noreply@aconex.com`) for submittal transmittal tracking
4. **Adel Darwish folder snapshot** (`99_Archive/adel_snapshots/`) for file listing and approval docs
