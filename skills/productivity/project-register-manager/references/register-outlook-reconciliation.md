# Register × Outlook Reconciliation

Cross-reference any project register (RFI, submittal, material, etc.) against Outlook emails to detect status discrepancies and find updates the register hasn't captured.

## The Problem

Project registers go stale between manual updates. Emails reveal the actual current state (NRS responded, drawings were shared, a meeting happened) but nobody updated the register. The user asks "list the RFIs" expecting the register, but also "update from the Outlook" meaning check what's changed.

## Workflow

### Phase 1 — Read the Register

```
Register path pattern: Subcontractors/NN_<Discipline>_Contractor/06_RFIs/RFI_Register.xlsx
Master path:            Docs/09_Registers/Subcontractor_RFI_Register/Aseer_Museum_Subcontractor_RFI_Register.xlsx
```

**First: check `os.path.getmtime()` (file modification time).** If the register was modified recently (within 3-5 days) and no project-critical emails are expected, skip the deep scan — saves 2+ minutes of SQLite/attachment work. Report the mtime so the user knows the register is already current.

Read the register's data sheet using the preview/MD sidecar if available (faster than openpyxl). Identify:
- Each item's ID, subject, current status, date received
- The date the register was last meaningfully updated (compare row dates vs file mtime)

### Phase 2 — Query Outlook for Related Emails

Database: `~/Library/Group Containers/UBF8T346G9.Office/Outlook/Outlook 15 Profiles/Main Profile/Data/Outlook.sqlite`

```sql
-- Find emails by vendor code, subject keywords, or RFI ID
SELECT m.Record_RecordID, datetime(m.Message_TimeReceived, 'unixepoch', 'localtime') as received,
       f.Folder_Name, m.Message_SenderList, m.Message_NormalizedSubject,
       substr(m.Message_Preview, 1, 800) as preview
FROM Mail m
JOIN folders f ON m.Record_FolderID = f.Record_RecordID
WHERE f.Folder_Name = 'Asher Regional Museum'
  AND (m.Message_NormalizedSubject LIKE '%GBH%'
     OR m.Message_NormalizedSubject LIKE '%Glasbau%'
     OR m.Message_NormalizedSubject LIKE '%Showcase%'
     OR m.Message_NormalizedSubject LIKE '%RFI%')
ORDER BY m.Message_TimeReceived DESC;
```

Key search targets by vendor code:

| Vendor Code | Vendor | Keywords |
|---|---|---|
| GBH | Glasbau Hahn (Showcases) | GBH, Glausbau, Showcase, RFI |
| Rawasin | Rawasin (AV/IT) | Rawasin, Gallery, AV, IT |
| Setworks | Setworks (Joinery) | Setworks, Joinery, FF&E |

### Phase 3 — Extract & Read Submittal Attachments

When the register says "Escalated" or "Pending Response" but an email exists from the consultant/client referencing the same submittal/ZD/RFI code with an attachment, **extract the PDF and read the formal response code** rather than relying on email subject/preview alone.

The email subject may say "RE: Submittal ZD-0030" but the actual **decision code (A/B/C/D)** is only in the attached PDF.

**Workflow:**
1. Find the email by submittal code in subject (`'%MOC-MUS-ASE%ZD-0030%'`)
2. Check `Message_HasAttachment = 1`
3. Extract using AppleScript (see outlook-email skill for script template)
4. Run `pdftotext <file.pdf> - 2>/dev/null` — the response code block is usually in the last 50 lines

**Response codes to look for:**
| Code | Meaning | Text Signal in PDF |
|------|---------|--------------------|
| A | Approved | "this submittal is hereby Approved" |
| B | Approved with Comments | "Approved with comments / معتمد مع ملاحظات" |
| C | Revise and Resubmit | "Revise and Resubmit" |
| D | Disapproved | "Disapproved / مرفوض" |

**Example (ZD-0030 Rev.01, May 2026):**
The email thread had "RE: MOC-MUS-ASE-1K0-ZD-0030 Rev.01 / Glasbau Hahn Presentation" (subject looked like a routine submission). But the extracted PDF contained the CG review stamp showing **Code A (Approved)** with conditions:
- Submit separate shop drawings for fixation mechanisms
- Submit updated time schedule coordinated with site progress
- Signed by Maged Zamzam (CG) on 31-May-2026

This changed the action: instead of "chase approval", the correct next step was "inform GBH of approval conditions".

### Phase 4 — Compare & Identify Discrepancies

For each RFI/item in the register, check:
1. **Status vs email evidence** — does the register say "Escalated" but NRS already responded?
2. **Date received vs email date** — was the RFI actually submitted earlier/later via email?
3. **New info not in register** — updated time schedule, new drawings shared, meeting outcomes

Common discrepancy patterns:
- Register: `Escalated to NRS` → Email: NRS responded with comments → **Status should be "Answered"**
- Register: `Open` → Email: response sent but not captured → **Status should be "Under Review" or "Answered"**
- Register: no entry → Email: new RFI submitted → **New row needed in register**

### Phase 5 — Report Findings

Present as a compact table showing:
- RFI ID, current register status, email evidence, recommended update

Example output format:
```
RFI-010 | Escalated to NRS | Robin/NRS responded May 8   | → Answered
RFI-011 | Escalated to NRS | Robin/NRS responded May 8   | → Answered
007-009 | Escalated to NRS | No new emails found          | No change
```

Also flag peripheral updates (new drawings, schedule changes) that don't directly affect a single RFI row.

## Worked Example: Showcase RFIs (June 2026)

**Register** (last modified 2026-06-03 — checked via `os.path.getmtime`, already current):
- ASR-SAM-GBH-RFI-007 → Escalated to NRS
- ASR-SAM-GBH-RFI-008 → Escalated to NRS
- ASR-SAM-GBH-RFI-009 → Escalated to NRS
- ASR-SAM-GBH-RFI-010 → Escalated to NRS
- ASR-SAM-GBH-RFI-011 → Escalated to NRS
- ASR-SAM-GBH-RFI-012 → Open (patinated brass, awaiting MoC)

**Outlook evidence**:
- 2026-05-06: Yara (GBH) sent RFI-010 & 011 to Ahmed
- 2026-05-08: Robin Kiang (NRS) replied to both RFI-010 & 011 with comments
- 2026-05-11: Yara chased open RFIs (patinated brass decision)
- 2026-05-18: Yara sent updated time schedule v2
- 2026-06-09: Elmer Gregorio shared DT_4001-4008 (Showcase Type 1-6B drawings)

**ZD-0030 verification** (new pattern):
- Email: "RE: MOC-MUS-ASE-1K0-ZD-0030 Rev.01 / Glasbau Hahn Presentation"
- Extracted PDF → pdftotext → Found **Code A (Approved)** by Maged Zamzam on 31-May-2026
- Conditions: submit fixation shop drawings + updated schedule
- Impact: register didn't need updating (not an RFI), but informed next action for GBH

**Discrepancies**:
| RFI | Register | Email Evidence | Action |
|-----|----------|----------------|--------|
| 010 | Escalated to NRS | NRS responded May 8 | Update → Answered |
| 011 | Escalated to NRS | NRS responded May 8 | Update → Answered |
| 007-009 | Escalated to NRS | No response found | Keep — still pending |
| 012 | Open | Patinated brass decision pending MoC meeting (week of May 11) | Chase — still open |

## SQL Query Templates

### By document code prefix (vendor/package)
```sql
SELECT ... FROM Mail m JOIN folders f ON m.Record_FolderID = f.Record_RecordID
WHERE m.Message_NormalizedSubject LIKE '%MOC-MUS-ASE%'
  AND m.Message_TimeReceived >= strftime('%s', 'now', '-90 days')
ORDER BY m.Message_TimeReceived;
```

### By specific email thread (RFI IDs in subject)
```sql
SELECT ... FROM Mail m
WHERE m.Message_NormalizedSubject LIKE '%RFI%10%'
   OR m.Message_NormalizedSubject LIKE '%RFI%11%'
ORDER BY m.Message_TimeReceived;
```

### Unread or recent emails from specific senders
```sql
SELECT ... FROM Mail m
WHERE m.Message_SenderAddressList LIKE '%@glasbau-hahn.de'
  AND m.Message_TimeReceived >= strftime('%s', 'now', '-30 days')
ORDER BY m.Message_TimeReceived;
```

### All emails in a project folder since a date
```sql
SELECT ... FROM Mail m JOIN folders f ON m.Record_FolderID = f.Record_RecordID
WHERE f.Folder_Name = 'Asher Regional Museum'
  AND m.Message_TimeReceived >= strftime('%s', 'now', '-60 days')
ORDER BY m.Message_TimeReceived;
```

## Pitfalls

- **Preview truncation** — `Message_Preview` is ~200-500 chars. For full body, use AppleScript or fall back to the preview's key signal (who said what to whom).
- **Duplicate folder paths** — emails may appear in both `Asher Regional Museum` and `Zamzam Projects` folders. De-duplicate by subject line.
- **SharePoint notifications** — `SharePoint Online` sends alerts like "created an anonymous access link to 'file.pdf'". These indicate new drawings/versions exist. Note them as peripheral updates.
- **Status word choice varies** — the register may use "Escalated to NRS" while emails say "NRS responded". The update direction is clear: if NRS responded, it's no longer escalated.
- **Check reply chains** — a single email thread may span RFI submission → NRS response → Samaya internal discussion. Read all messages in thread.
