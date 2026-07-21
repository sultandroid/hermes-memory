# AD Engineering Email Extraction — Worked Example

## Context
User asked: "check all emails related to AD Engineering" then "read all attachments" then "update everything in repo"

## Phase 1 — Discovery
SQLite query used 3 LIKE patterns:
- `Message_SenderAddressList LIKE '%adeng%'`
- `Message_SenderAddressList LIKE '%@adeng%'`
- `Message_NormalizedSubject LIKE '%AD Engineering%'`

Also searched for `Adel Darwish` and `AD-ENG` in subject/sender.

**Key lesson:** Always search by email domain AND subject keywords. AD Engineering emails came from 5 different @adeng.com.sa addresses (maher, BD, supervision, mr, osama) plus internal forwards.

## Phase 2 — Results
29 emails found across Inbox, Asher Regional Museum, Sent Items, Zamzam Projects, Deleted Items. Presented as table with English-only subjects.

## Phase 3 — Extraction
Wrote 15 individual .applescript files (one per email ID with attachments). Ran in batches of 3 via osascript. Skipped image/* content types. 18 files extracted to /tmp/ad_engineering_attachments/.

**Key lesson:** Individual .applescript files per email ID is the most reliable pattern for batch extraction. The ~700-byte limit means each script must be minimal.

## Phase 4 — Classification
| Document Type | Count | Tools Used |
|--------------|-------|------------|
| Signed Agreement (.docx) | 1 | textutil |
| SOW / Drawing List (.pdf) | 2 | pdftotext |
| Electrical SOW Draft (.docx) | 1 | textutil |
| Submission Plan (.xlsx) | 2 | openpyxl |
| Technical & Financial Proposals (.pdf) | 7 | pdftotext |
| CVs (.pdf) | 2 | pdftotext |
| Certificates (.pdf) | 1 | pdftotext |
| Original RFP (.pdf) | 1 | pdftotext |

## Phase 5 — Repo Filing (3-Layer System)
Created:
- `03_Scope/AD_Engineering/README.md` — SOW summary with scope, CG conditions, exclusions, filed docs index
- `03_Scope/AD_Engineering/` — 10 source files (agreement, SOWs, CVs, cert)
- `02_Schedule/AD_Engineering/README.md` — full submission plan (3 gates, 30+ items)
- `02_Schedule/AD_Engineering/` — 2 xlsx files
- `Technical_Office/Submission_Tracker/AD_Engineering/README.md` — live submission log with 20+ DD items

Updated:
- `specialist_register.md` — added SOW/Plan columns to Tier 2 table with folder paths
- `PROJECT_MEMORY.md` — AD Engineering entry with file paths + first DD dates
- `01_Registers/subcontractor_sow_raci_register.md` — MEP Designer row: "package SOW exists — filed in repo"
- `01_Registers/subcontractor_package_register.md` — `13_MEP_Designer` row with repo paths

**Key lesson:** The repo already had a SOW control system (`01_Registers/subcontractor_sow_raci_register.md`, `03_Plans/15_Subcontractor_Deliverables/`). Always check existing infrastructure before creating new structures. Link into it, don't build parallel systems. The user will correct you if you miss existing infrastructure.

## Phase 6 — Master Tracker
Created `Technical_Office/Submission_Tracker/README.md` covering all 30 packages with SOW/Plan/Tracker status and priority actions.

## Key Contacts Identified
| Name | Email | Role |
|------|-------|------|
| Maher | maher@adeng.com.sa | Coordination, kick-off |
| Mohanna Abdulkhaliq | supervision@adeng.com.sa | MEP design SOW, pricing |
| Rashed Bati | mr@adeng.com.sa | Electrical design SOW |
| Osama Abdel Shafi | osama@adeng.com.sa | RFP stage |
| BD | BD@adeng.com.sa | Business Development |
