# CG Response Management — Workflow for Consultant Review Responses

Process for finding, classifying, filing, and tracking Client/Government (CG) consultant review responses across plan/procedure folders.

## When to Use

- The user asks "check for CG responses" or "check consultant review comments"
- New plan submissions were sent to CG and you need to check for incoming responses
- Bulk audit of all plan review statuses is needed
- Any task involving "CG", "review", "response", "comments" from consultants

## The Workflow (9-Step)

### Phase 1: Source Discovery

**Step 1 — Inventory known attachment files.**

Check these directories first (they may contain already-downloaded CG response PDFs):
```
Email_Archive/_attachments/
Email_Archive/Attachments/
```

Look for files containing: `CG`, `cg-`, `CodeC`, `Code-B`, `SI-`, `NCR`, `response`, `review`, `comment`, `remark`, `approval`, `reject`, `letter`, `LET-`.

**Step 2 — Search Outlook SQLite for CG consultant emails (ALL folders).**

This is **much faster** than AppleScript scanning (instant vs 120s+). Query the Outlook for Mac SQLite database.

**⚠️ CRITICAL: Query ALL folders, not just Inbox.** The user corrected this — many CG responses are only in Sent Items, Archive, or project-specific folders. Querying only Inbox misses ~2/3 of emails. Always join Mail with Folders on Record_FolderID.

Database path:
```
~/Library/Group Containers/UBF8T346G9.Office/Outlook/Outlook 15 Profiles/Main Profile/Data/Outlook.sqlite
```

Table schemas:
- **Folders**: Record_RecordID, Folder_Name, Folder_SpecialFolderType (1=Inbox)
- **Mail**: Record_RecordID, Record_FolderID, Message_NormalizedSubject, Message_TimeReceived (unix epoch), Message_SenderAddressList, Message_ReadFlag (0=unread), Message_HasAttachment, Message_ReadFlag

**Step 2a — List all folders:**
```sql
SELECT Record_RecordID, Folder_Name, Folder_SpecialFolderType 
FROM Folders ORDER BY Folder_Name;
```

**Step 2b — Query ALL folders for @cg.com.sa emails (last 90 days):**
```sql
SELECT datetime(m.Message_TimeReceived, 'unixepoch') as dt,
       m.Message_NormalizedSubject as subj,
       m.Message_SenderAddressList as sender,
       f.Folder_Name as folder,
       CASE WHEN m.Message_ReadFlag = 0 THEN 'UNREAD' ELSE 'read' END as status,
       CASE WHEN m.Message_HasAttachment = 1 THEN 'ATTACH' ELSE '' END as attach
FROM Mail m JOIN Folders f ON m.Record_FolderID = f.Record_RecordID
WHERE m.Message_TimeReceived > strftime('%s', 'now', '-90 days')
  AND m.Message_SenderAddressList LIKE '%@cg.com.sa'
ORDER BY m.Message_TimeReceived DESC;
```

**Step 2c — Query ALL folders for project doc codes (Hesham's submissions):**
```sql
SELECT datetime(m.Message_TimeReceived, 'unixepoch') as dt,
       m.Message_NormalizedSubject, m.Message_SenderAddressList,
       f.Folder_Name,
       CASE WHEN m.Message_ReadFlag = 0 THEN 'UNREAD' ELSE 'read' END as status
FROM Mail m JOIN Folders f ON m.Record_FolderID = f.Record_RecordID
WHERE m.Message_TimeReceived > strftime('%s', 'now', '-90 days')
  AND (m.Message_NormalizedSubject LIKE '%MOC-MUS-ASE%'
    OR m.Message_NormalizedSubject LIKE '%MOC-ASEER%'
    OR m.Message_NormalizedSubject LIKE '%SI-CG%'
    OR m.Message_NormalizedSubject LIKE '%NCR%')
ORDER BY m.Message_TimeReceived DESC;
```

**Step 2d — Find distinct CG senders:**
```sql
SELECT DISTINCT m.Message_SenderAddressList, COUNT(*) as cnt,
       MAX(datetime(m.Message_TimeReceived, 'unixepoch')) as latest
FROM Mail m JOIN Folders f ON m.Record_FolderID = f.Record_RecordID
WHERE m.Message_SenderAddressList LIKE '%@cg.com.sa'
GROUP BY m.Message_SenderAddressList ORDER BY cnt DESC;
```

**Pitfall (proven 2026-05-29):** Querying only Inbox found 14 CG emails. Querying ALL folders found 43 — nearly 3x more. Always search all folders.

**Pitfall:** SQLite column names vary between Outlook versions. Always run `.schema Mail` and `.schema Folders` first to verify.

**Step 3 — Search existing Email_Archive markdown records.**

Check:
```
Email_Archive/hesham_archive_*.md        — batch-processed email logs
Docs/Email Archive/<project-name>/*.md   — categorized archive files
```

Look in `SI - ملاحظات الموقع.md` for site instructions, `DOC - تقديم مستندات.md` for document submissions with CG threads.

**Step 4 — Check existing plan CG_Responses folders.**

Each plan folder under `02_Plans_and_Procedures/` has `02_CG_Responses/` where previous CG responses were filed. Check these for existing `CG_STATUS.md` files.

### Phase 2: Classification

**Step 5 — Map each CG document to its plan.**

Use the document code embedded in the filename to identify which plan it relates to:

| Document Code Prefix | Plan Folder |
|---------------------|-------------|
| PL-0029 | 02.1_DMP |
| PL-0018 | 02.7_Communication_Plan |
| PL-0020 | 02.13_Stakeholder_Plan |
| PL-0035, PL-0036, PL-0037, PL-0040, PL-0041, PL-0043 | 02.5_HSE_Plan |
| SH-006 | 02.8_Master_Programme |
| ZD-0026 | 02.6_NRS_Methodology |
| CG-LET-008, CG-LET-009 | 02.2_BEP_MIDP_TIDP |
| RP-0039 | 02.3_PEP |
| IFC-0004 | 02.1_DMP |
| SC-0035 | 02.5_HSE_Plan |
| MS-0010 | 02.3_PEP |

For documents without a clear code mapping:
- `SI-CG-ASEER-007` (Site Instructions) → 02.3_PEP
- `ARM-SIC-CG-LET-*` (CG Letters) → 02.2_BEP_MIDP_TIDP
- `NCR *` (Non-Conformance Reports) → project-level, note in master register
- Samples comments → primary plan + 02.10_Subcontractor_Deliverables if subcontractor-related

### Full Document Code Reference (55+ codes discovered from 90-day Outlook scan)

| Code | Document Type | Likely Plan |
|------|--------------|-------------|
| PL-0013 | Submission Plan | 02.2_BEP_MIDP_TIDP |
| PL-0015 | BIM Execution Plan (BEP) | 02.2_BEP_MIDP_TIDP |
| PL-0018 | Project Communication Plan | 02.7_Communication_Plan |
| PL-0020 | Stakeholder Management Plan | 02.13_Stakeholder_Plan |
| PL-0029 | Design Management Plan (DMP) | 02.1_DMP |
| PL-0035 / SC-0035 | HSE Deliverables | 02.5_HSE_Plan |
| PL-0036 / SC-0036 | Fire Prevention Plan | 02.5_HSE_Plan |
| PL-0037 | Workers Welfare Management Plan | 02.5_HSE_Plan |
| PL-0040 | Site Security Management Plan | 02.5_HSE_Plan |
| PL-0041 | Emergency Preparedness Response Plan | 02.5_HSE_Plan |
| PL-0043 | Temporary Electrical Management Plan | 02.5_HSE_Plan |
| SH-006 | Time Schedule / Master Programme | 02.8_Master_Programme |
| ZD-0017 | Workflow: CG/Design Office/Specialist | 02.2_BEP_MIDP_TIDP |
| ZD-0023 | LOD 300 Existing BIM Models | 02.2_BEP_MIDP_TIDP |
| ZD-0025 | Title Block | 02.2_BEP_MIDP_TIDP |
| ZD-0026 | NRS Design Methodology | 02.6_NRS_Methodology |
| ZD-0030 | Glasbau Hahn Presentation | 02.10_Subcontractor_Deliverables |
| ZD-0031 | 3D Viewpoints Layout | 02.1_DMP |
| ZD-0032 | Demolition Routing Plans | 02.3_PEP |
| ZD-0033 | Sample for 3D Render | 02.1_DMP |
| ZD-0034 | Audit and Understanding Report | 02.1_DMP |
| ZD-0038 | Proposed Exterior CCTV Locations | 02.3_PEP |
| ZD-0042 | Temporary Power Distribution | 02.3_PEP |
| ZD-0044 | HSE Notice Board Report | 02.5_HSE_Plan |
| RP-0039 | BMS Site Assessment & Evaluation Report | 02.3_PEP |
| IFC-0001 | Showcases IFC Drawing (Arch) | 02.1_DMP |
| IFC-0003 | Flooring Package IFC Drawing | 02.1_DMP |
| IFC-0004 | Life Safety IFC Drawings | 02.1_DMP |
| IFC-0005 | Freestanding Walls IFC Package | 02.1_DMP |
| IFC-0006 | Internal Stairs IFC Package | 02.1_DMP |
| IFC-0007 | VIP WC IFC Package | 02.1_DMP |
| IFC-0008 | AV Drawings IFC Package | 02.1_DMP |
| MS-0010 | Method Statement — Electrical Systems Assessment | 02.3_PEP |
| MA-0006 | Showcases Materials (samples approval) | 02.10_Subcontractor_Deliverables |
| IR-0001 | Site Survey & As-Built Verification | 02.3_PEP |
| PQ-0056 | Projector Vendor — Panasonic (procurement) | 02.11_Procurement_Plan |
| TQ-0012/13/15/16/17/21 | Technical Inquiries (various) | 02.3_PEP |
| QT-0021/22 | Quantity Take-off | 02.11_Procurement_Plan |
| RFI-010 | Request for Information | 02.3_PEP |
| SI-CG-ASEER-007 | Site Instruction (multiple revisions) | 02.3_PEP |
| NCR-003 | Non-Conformance Report — Electrical | (Project-level) |
| CG-LET-008/009 | CG Letters (Stage transition, BEP/CDE) | 02.2_BEP_MIDP_TIDP |

Classify CG response status using the standard codes:
- **Code A** — Approved (no comments)
- **Code B** — Approved with Comments (address conditions)
- **Code C** — Revise & Resubmit (🔴 needs immediate action)
- **Code D** — Disapproved (🔴 critical)

### CG Reply PDF Pattern (proven 2026-05-29)

Many CG response PDFs are named with a "Reply" suffix in `Email_Archive/Attachments/`. These contain embedded CG review comment sheets behind a transmittal cover. Examples:
- `MOC-MUS-ASE-1K0-PL-0018-REV01 REPLY.pdf` — 8 CG comments, signed by Mohammad Elbaz as Acting PM
- `MOC-MUS-ASE-1KH-PL-0037 - Welfare Management Plan - Reply.pdf` — 8 CG HSE comments, Code B
- `MOC-MUS-ASE-1KH-SC-0035 - Reply.pdf` — Mixed HSE review codes (A/B/C)
- `MOC-MUS-ASE-1KH-SC-0036 - Reply.pdf` — Fire Prevention, Code C, 12 comments

Search pattern for Reply PDFs:
```bash
find "Email_Archive/Attachments" -name "*Reply*" -o -name "*REPLY*" | sort
```

These should be the FIRST place to look for actual CG review content — they contain the reviewer's name, comment count, and review code.

**Step 6 — File documents to plan 02_CG_Responses/.**

For each classified document:
```bash
cp <source> <PLANS_DIR>/<plan>/02_CG_Responses/
```

Handle name conflicts: append `_from_archive` suffix if file already exists.

For cross-plan documents (relevant to multiple plans), copy to each applicable folder.

### Phase 3: Status Tracking

**Step 7 — Create/update CG_STATUS.md for every plan.**

Each plan's `02_CG_Responses/CG_STATUS.md` should contain:

```markdown
# CG Response Status — 02.X_PlanName

| Document | CG Status | Date | Detail | Action |
|----------|-----------|------|--------|--------|
| [Doc Name] | Code C — Revise & Resubmit | 2026-05-25 | CG reviewer: name@cg.com.sa. N comments. | ACTION REQUIRED |

## Filed Documents
- [file1.pdf] (size bytes)

## Email Sources
- CG consultant emails from `@cg.com.sa` in Outlook Inbox
- Email Archive: <path>
```

Include alert banners for critical items:
```
> **🔴 Code C — Revise & Resubmit. Immediate action needed.**
> **⚠️ N unread CG responses in Outlook. Download required.**
```

For plans with NO CG responses found, create a single-entry status:
```
| Plan Name | No CG Response Found | — | No CG review records in emails/archives | Monitor |
```

**Step 8 — Create/update the Master CG Response Register.**

At the parent level (`CG_Response_Register.md`), create a summary with:
- Counts by status (Code C / Code B / Submitted / Unread / No Response)
- Critical actions table (what needs immediate work)
- Full register table with: Plan, Document, Status, Date, Reviewer, Action
- CG consultant contact list (name, email, role)

Track unread emails separately from read-but-pending responses. The count should reflect actual unread Outlook items.

### Phase 4: Audit & Deliver

**Step 9 — QC audit the CG response filing.**

Run Codex to audit against these criteria:
- [ ] All 14 plans have `02_CG_Responses/CG_STATUS.md` with ≥1 entry
- [ ] Filed documents exist for plans where CG responses were found
- [ ] Master `CG_Response_Register.md` exists at parent level
- [ ] Plans with unread CG emails are flagged in their status
- [ ] Code C items are clearly marked with 🔴
- [ ] Cross-plan documents are filed in all relevant folders
- [ ] No duplicate filings or overwritten files
- [ ] Unread count in master register matches detail rows

## Known CG Consultant Contacts (Aseer Museum)

| Name | Email | Role | Emails Found |
|------|-------|------|-------------|
| Mohammad Elbaz | melbaz@cg.com.sa | Primary CG reviewer (Acting PM) — plans, drawings, reports | 28 |
| Mahmoud Afifi | mafifi@cg.com.sa | Project Management — BIM/Submission Plan approvals | 7 |
| Mohamed Elroby | melroby@cg.com.sa | MEP discipline reviewer — electrical, temp power | 3 |
| Sundus Alfeer | salfeer@cg.com.sa | NCR / QHSE reviewer — site survey, non-conformance | 2 |
| Yasser Zaki | yzaki@cg.com.sa | Aconex system administrator — user accounts, training | 3 |
| Anwar Sadat | — | CG HSE Manager — co-signs HSE plan reviews with Elbaz | (appears in Reply PDFs) |

**NOTE:** melbaz@cg.com.sa (Mohammad Elbaz) is the dominant reviewer — 28 of 38 CG emails. Most CG responses go through him.

## Pitfalls

- **Outlook SQLite schema differs by version** — always check with `.schema Mail` before querying. Column names vary between Outlook for Mac versions.
- **EML stub files are 0 bytes** — these are Outlook reference pointers with no content. Don't attempt to extract info from them.
- **Corrupt PDFs** — some CG response PDFs may fail text extraction. Classify by filename and email context, not content.
- **Unread count accuracy** — count actual unread flags from Outlook SQLite (`Message_ReadFlag = 0`), not inferred from status files. Keep the register count in sync.
- **AppleScript vs SQLite** — SQLite query is instant but shows metadata only. AppleScript can download attachments but is slow. Use SQLite for discovery, AppleScript for targeted attachment download.
- **Status vs filed documents** — A plan can have a CG STATUS (e.g., "Submitted — Awaiting Response") without any filed CG document. The CG_STATUS.md should still exist with the status entry.
