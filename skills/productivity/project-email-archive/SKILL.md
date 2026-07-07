---
name: project-email-archive
description: Use when setting up or maintaining a project's email archive folder. Defines the canonical 2-tier folder structure (Email_Archive + Docs/Email Archive) with 14 document-category folders, naming conventions, and file organization rules.
version: 1.1.0
author: Hermes Agent / Samaya Technical Office
license: MIT
metadata:
  hermes:
    tags: [project-management, document-control, email-archive, samaya]
    related_skills: [bim-project-register, project-register-manager, samaya-technical-office, bim-email-pipeline]
---

# Project Email Archive — Standard Template

## Overview

Every Samaya Investment project gets a standardized email archive with **two root locations** that must be kept in sync:

> **Automation:** The `bim-email-pipeline` skill handles automated classification, attachment extraction, and archiving — it files emails into this exact structure every 2 hours.

```
<Project Folder>/
├── Email_Archive/            ← raw email exports (.eml + attachments)
│   ├── _attachments/         ← extracted PDF/DWG file attachments from emails
│   └── Attachments/          ← manually saved key attachments
│
└── Docs/
    └── Email Archive/
        └── <Project Arabic Name>/    ← one per sub-project or stream
            ├── DOC - تقديم مستندات/
            ├── IR - طلبات استلام الأعمال/
            ├── MAR - اعتماد مواد وعينات/
            ├── MIR - فحص مواد بالموقع/
            ├── RFP - مقترحات فنية/
            ├── RFI - استفسارات/
            ├── SI - ملاحظات الموقع/
            ├── SCH - الجداول الزمنية/
            ├── SDR - المخططات التنفيذية/
            ├── WIR - طلبات بدء الأعمال/
            ├── REP - التقارير والخطط/
            ├── SI-REF/ (reference copies)
            ├── Dashboard_<project>.html
            └── Project_Log_<project>.csv
```

> **Why two trees?** `Email_Archive/` holds the raw inbox/sent `.eml` exports. `Docs/Email Archive/` holds structured, categorized `.md` records — one file per submission/letter — that are the working register for the Technical Office.

## Document Category Codes (14 codes)

| Code | Arabic | English | Trigger |
|------|--------|---------|---------|
| **DOC** | تقديم مستندات | Document Submission | Any formal submittal: drawings, reports, calculations, shop drawings, graphic files |
| **IR** | طلبات استلام الأعمال | Inspection/Work Receipt | On-site inspection requests, handover certificates, snagging lists |
| **MIR** | فحص مواد بالموقع | Material Inspection @ Site | On-site material verification before installation |
| **MAR** | اعتماد مواد وعينات | Material Approval Request | Material/sub-product sample submissions for approval |
| **RFP** | مقترحات فنية | Technical Proposal | Design proposals, RFP responses, concept submissions |
| **RFI** | استفسارات | Request for Information | Technical queries to consultant/owner |
| **SI** | ملاحظات الموقع | Site Instruction | Site observations, instructions issued to contractor |
| **SCH** | الجداول الزمنية | Schedules | Programme updates, milestones, delay notices |
| **SDR** | المخططات التنفيذية | Shop Drawing Register | Drawing submissions and revision tracking |
| **WIR** | طلبات بدء الأعمال | Work Initiation Request | Approvals to commence a specific work package |
| **REP** | التقارير والخطط | Reports & Plans | Weekly reports, method statements, risk assessments |
| **GEN** | رسائل عامة | General Correspondence | Anything not fitting the above categories |
| **MUM** | – | Museum-specific submittal | Submittal log code for museum fit-out (NWC contracts) |
| **CTR** | – | Contract document | Contractual letters, agreements, NOCs |

## File Naming Convention

### Format (MD files in Docs/Email Archive)
```
YYYY-MM-DD - [RE ]نموذج <Category> <description>_Rev.NN.ext
```

**Examples:**
```
2025-11-30 - نموذج تقديم استلام أعمال (IR) الفريم استيل للدور الأرضي_Rev.00.md
2025-10-13 - RE نموذج تقديم مواد (MAR) كابلات البيانات بمشروع إعادة تأهيل_Rev.01.md
2026-03-08 - نموذج تقديم مواد (MAR) مواد حجر إغلاق واجهة الرصيف_Rev.02.md
```

### Document Code Prefix (for tracked documents)
```
<PRJ>-<CTR|MUM>-<CATEGORY>-<DISC>-<NNN>_Rev.<XX>
```
**Examples:**
```
ZAM-NWC-CTR-DOC-STR-041_Rev.01.pdf
ZAM-NWC-MUM-IR-AR-152_Rev.00.pdf
ZAM-NWC-MUM-MIR-AR-064_Rec.00.pdf
```

- `PRJ`: Project code (ZAM = Zamzam, ASE = Aseer, etc.)
- `CTR` / `MUM`: Contract type — CTR = main contractor, MUM = museum fit-out
- `CATEGORY`: 3-letter category code (DOC, IR, MAR, MIR, etc.)
- `DISC`: Discipline (AR=architectural, STR=structural, MEP=mechanical, EL=electrical)
- `NNN`: Sequential 3-digit number
- `Rev.NN` / `Rec.NN`: Revision or Record number

### Prefix Key
| Prefix | Meaning |
|--------|---------|
| `RE ` | Reply / response to a previous submission |
| `FW ` | Forward |
| `نموذج` | Official submission form |

## When to Use

- **New project onboarding** — create the full folder structure before any emails are filed
- **Filing an email** — determine its category code, rename per convention, place in correct folder
- **Updating registers** — scan folder counts and sync with Project_Log CSV
- **Cross-auditing submittals** — compare folder counts across categories to spot gaps
- **Generating dashboard** — parse folder structures to produce Dashboard HTML
- **Processing weekly email archives** — `references/weekly-archive-processing.md` covers the repeatable procedure for scanning weekly `.md` files, comparing against BIM destinations, filing new attachments, and updating PROJECT_MEMORY.md

## Workflow: Filing a New Email

1. **Determine category** using the 14-code table above
2. **Determine discipline**: `AR` (architectural), `STR` (structural), `MEP`, `EL` (electrical), `PL` (plumbing), `FS` (fire safety), `CONT` (contractual)
3. **Check document code**: Look at the last number used in that category/discipline and increment
4. **Format filename**: `YYYY-MM-DD - نموذج <Category> <description>_Rev.00.md`
5. **Extract attachments**: Save PDFs/DWGs to `Email_Archive/Attachments/`, cross-reference in the MD
6. **Log in Project_Log CSV**: append row with date, category, description, doc code, revision, status

## Workflow: Initializing a New Project Archive

1. Create the top-level folder structure
2. Create `Email_Archive/_attachments/` and `Email_Archive/Attachments/`
3. Create all 14 category folders under `Docs/Email Archive/<Project Name>/`
4. Create empty `Project_Log_<project>.csv` with headers
5. Set up dashboard HTML (can be generated from CSV)
6. Update the main BIM Project Register

## Common Pitfalls

1. **Over-classifying GEN** — GEN is the catch-all and will always be the largest folder for active projects with heavy coordination traffic (car requests, personnel, access-link notifications, internal replies). Do NOT force GEN items into formal submittal codes. A GEN folder of 100+ files on an active project is normal and expected. The value is that everything is searchable and dated.
2. **Naming inconsistencies** — `RE` prefix: always `RE ` (with trailing space), never `RE:` or `RE-`
3. **Mixing CTR and MUM** — MUM only for museum fit-out submittals under NWC contract; CTR for main construction
4. **Revision numbers** — always start at `Rev.00`, increment on every resubmission
5. **Attachments not linked** — save PDFs/DWGs to `Email_Archive/Attachments/` with matching doc code, cross-reference in the MD
6. **Using rm** — never delete from archive; move to `_archive/` subfolder if needed
7. **Empty folders** — 0-file folders (RFI, SDR, WIR) are normal initially; don't delete them
8. **OneDrive sync conflicts & APFS compressed/dataless** — `Resource deadlock avoided` (EDEADLK, errno 11) when reading a file can mean:
   - The file is a **OneDrive placeholder** (0 bytes, not yet downloaded from cloud).
   - The file is **actively syncing** (has content but NSFileProvider holds an exclusive coordination lock).
   - The file has been **APFS-compressed to `compressed,dataless`** (macOS storage optimization — non-zero file size but content offloaded). Detect with `ls -lO`.

   Do NOT assume a 0-byte file is broken — first check with `ls -lO` for the `compressed,dataless` flag. If present, `os.open()` also fails; use `rsync src /tmp/` to materialize. For pure OneDrive placeholders, `os.open(path, os.O_RDONLY)` may work but `rsync` is the most reliable fix across both scenarios.
9. **Outlook Exchange Cached Mode on macOS** — Samaya's Outlook (samayainvest.com) stores all mail in Microsoft's cloud, not locally. The Outlook SQLite database on macOS (`~/Library/Containers/com.microsoft.Outlook/Data/`) contains only font cache and HTTP storage — **no message content**. `.eml` files in `_attachments/` are OneDrive cloud placeholders (0 bytes until downloaded). The 18,099-message inbox (actually "On My Computer" local store) can only be queried efficiently by **index** — not by filtered search:

> ⚠️ **CRITICAL UPDATE (May 31, 2026):** The Exchange account Inbox shows **0 messages** while the "On My Computer" Inbox has 18,099 messages from July 2022. The Exchange account appears disconnected. Project subfolders (Asher Regional Museum, Zamzam Project) are under the Exchange account and show stale data (latest Oct 2025). The most recent project emails (May 19, 2026) are in Deleted Items. See `bim-email-pipeline` skill's `references/outlook-folder-hierarchy.md` for the full folder tree.

   - ✅ `item N of allMsgs` — fast, ~6 s per message (random access)
   - ✅ `item N of allMsgs` — fast, ~6 s per message (random access)
   - ✅ Get count: `count of messages of inbox` — ~22 s
   - ❌ `messages of inbox whose subject contains "X"` — **times out** (~300 s+) on 18k+ mailboxes in cached mode
   - ✅ **Bulk search with short timeout:** Use `osascript` directly and set a 300 s timeout — each search term (e.g., "ASEER", "regional museum", "MOC-MUS-ASE") returns in ~15–35 s. For large inboxes (18k+ messages), this is the practical approach.
   - ✅ **Date format for AppleScript:** use DMY format `"01/01/2024"` — YMD `"2024-01-01"` is interpreted as MDY (causing wrong year), Arabic month names fail in en_SA locale. Preferred: `"Monday, 25 May 2026 11:25 AM"` or `"January 1, 2024"` (full format).
   - ✅ **Getting full email data (subject, sender, plain text body):** Use AppleScript `plain text content` property. Stream all messages in a single `repeat` loop — do NOT use filtered queries on large inboxes. Output as `===MSG===` delimited blocks. Parse date from the body's `Sent:` header line (never from `date received` AppleScript property which is broken on Exchange accounts). A 300 s osascript timeout handles 40+ messages per batch.
   - ✅ **Keywords that find Aseer emails:** `"ASEER"` (95 msgs), `"regional museum"` (41 msgs), `"MOC-MUS-ASE"` (66 msgs), `"Asir"` (23 msgs), `"museum"` (327 msgs — very broad). Combined multi-keyword fetch yields ~185 unique messages. Always dedupe by `(date + subject)` before outputting.
   - ✅ **Getting To: field:** The `recipient to recipients` property returns a list. Use `address of every recipient of msg` instead of `get address of to recipients of msg`. The `To:` line must be extracted from `plain text content` body, not from the `to recipients` AppleScript property which fails silently.
   - ✅ **Getting From: field:** Use AppleScript sender properties (authoritative) — `name of sender` + `address of sender`. The body's `From:` line may be contaminated with URLs/HTML.
   - ✅ **Token access:** Microsoft Graph API tokens are NOT in the macOS Keychain for Outlook. For full email metadata (sender, recipient, body), use bulk AppleScript fetch or export `.msg` files to a local folder.
   - ⚠️ **OneDrive placeholders are 0 bytes:** `find ... -size +0` filters out cloud-only files. Only `.eml`/`.msg` files with actual content can be parsed.
   - ⚠️ **`date received` property is broken:** On Exchange-cached Outlook on macOS, reading `date received` for any message hangs indefinitely. Always parse date from the email body's `Sent:` header line instead.
10. **Register output format — document-controller grade** — The user expects a professional register table with ALL of these columns. Never produce fewer. Leave cells blank if data is unavailable (e.g., sender/receiver from cloud-only emails), but the column schema is fixed:
    | No. | Date | From | To | Action | Doc Code | Revision | Category | Status | Remarks |
    |-----|------|------|-----|--------|----------|----------|----------|--------|---------|
    | 1 | 2026-05-10 | [sender name & email] | [recipient(s)] | [subject / action taken] | MOC-MUS-ASE-1K0-PL-0018 | Rev.01 | DOC | Filed | — |
    | | | | | | | | | | |
    Do **not** output a flat `.md` list with only Date/Category/Description/Doc_Code/Revision/Status. The full 10-column table is the standard.
    **If sender/receiver data is unavailable:** still include From/To columns, leave blank. The structure is non-negotiable.
11. **MEP/AV service requests** → classify as **IR** (design service inspection/requests), not GEN
12. **Showcases materials** (`MA-xxxx`) → **MAR**, not DOC
13. **Site survey / As-Built verification** (`1V0-IR-xxxx`) → **IR**, not GEN
14. **Weekly meeting reports** with 🗓 prefix → **REP**, not GEN or IR
15. **GBH / contractor time schedules** → **SCH**, not GEN
16. **Gen contractor invoices / payment certificates** → **DOC**, not GEN
17. **MOC design-plan codes** (`PL-0029` DMP, `PL-0018` Communication Plan, `SC-0035` HSE, `PL-0036/37/0040` welfare/security) → **DOC**, not GEN
18. **Vendor submissions** (Artec RFQ, Bluehaus, JOCAVI, P01112 price requests, Panasonic vendor) → **RFP**, not GEN
19. **Open RFIs tracker** → **RFI**, not GEN
20. **IFC drawing submissions** (`IFC-xxxx`) → **SDR**, not DOC
21. **Method statements** (`MS-xxxx`) → **DOC**, not GEN

## Dashboard HTML Structure

The dashboard (`Dashboard_<project>.html`) tracks:
- File count per category with colored bars
- Date range (oldest / newest submission)
- Last-30 rows table with category badges

The `Project_Log_<project>.csv` is the source of truth, updated every time a document is filed. Generate the dashboard from CSV using the Python script in `references/categorization_rules.md`.

## Aseer Museum — Live Example (May 2026)

- Project: Aseer Regional Museum (Project 3092)
- Root: `…/Aseer-Museum/Docs/Email Archive/مشروع متحف عسير الإقليمي/`
- 308 files migrated from flat `Email_Archive/` to 12 categorized subfolders
- GEN folder: 134 files (expected — active coordination project)
- Dashboard: `Dashboard_مشروع متحف عسير الإقليمي.html`
- Log: `Project_Log_مشروع متحف عسير الإقليمي.csv`

## Example Project Codes

| Project | Code | Owner | Contract Type | Doc Code Prefix |
|---------|------|-------|---------------|-----------------|
| Zamzam Museum — Makkah | ZAM | NWC (National Water Co.) | CTR + MUM | ZAM-NWC-{CTR\|MUM} |
| Aseer Regional Museum | ASE | Ministry of Culture (MoC) | CTR | MOC-MUS-ASE |
| Dawam Plaza | DAW | Dawam | CTR | — |

### Aseer-specific codes
Aseer uses `MOC-MUS-ASE` as its document code prefix, not the `ASE` shorthand:
```
MOC-MUS-ASE-<zone>-<discipline>-<number>  Rev.NN
```
| Zone | Meaning |
|------|---------|
| `1A0` | Architectural package |
| `1E0` | Electrical / AV |
| `1K0` | Master / coordination |
| `1V0` | Site / survey / IR |
| `0PS` | Scheduling |
| `1KH` | HSE |

## Register Output Format

The `Project_Log_<project>.csv` and any exported register MUST contain these columns:

| Column | Description |
|--------|-------------|
| **No.** | Sequential row number |
| **Date** | `YYYY-MM-DD` format |
| **From** | Sender name and email (from Outlook) |
| **To** | Recipient(s) name and email |
| **Action** | Brief description of what was sent/submitted/actioned |
| **Doc Code** | Document code (e.g. `MOC-MUS-ASE-1K0-PL-0029`) or `—` if not applicable |
| **Revision** | Rev.NN or `—` |
| **Category** | 3-letter code (DOC, IR, MAR, MIR, RFP, RFI, SI, SCH, SDR, WIR, REP, GEN) |
| **Status** | `Pending` / `Approved` / `Approved w/ Comments` / `Rejected` / `Received` / `Filed` |
| **Remarks** | Any outstanding actions, reviewer comments, or cross-references |

> **Note:** If sender/receiver data is unavailable (OneDrive placeholder files, no Graph API access), still include the columns — leave the cells blank. The register structure must always match this schema.

## Verification Checklist

- [ ] All 14 category folders exist (including 0-file folders)
- [ ] `Email_Archive/_attachments/` and `Attachments/` both exist
- [ ] Naming convention applied: `YYYY-MM-DD - نموذج ..._Rev.NN.md`
- [ ] Document codes are sequential per category/discipline
- [ ] `Project_Log.csv` updated with each new submission
- [ ] Dashboard HTML reflects latest folder counts
- [ ] No file deletions from archive (use `_archive/` if needed)
- [ ] OneDrive sync confirmed after each batch update