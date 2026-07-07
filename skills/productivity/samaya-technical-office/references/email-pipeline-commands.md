# Email Pipeline — Zamzam Museum (ID 121)

## Overview
Extracts 828 emails from Outlook `sultan@samayainvest.com` → `Zamzam Projects` folder, classifies attachments, organizes into category MD files. Pipeline lives under `Docs/_Tools/` in the project folder.

## Pipeline Scripts

### 01_extract.py — Outlook Extraction
```bash
# Runs Outlook pass → extracts attachments + manifest.json
cd "Docs/_Tools/"
python3 01_extract.py
# Output: attached/ + manifest.json in project root
```

### 02_generate_md.py — Category File Generation
```bash
# Re-runnable — computes move-status by scanning the file tree
python3 02_generate_md.py
# Output: Docs/Zamzam_Emails_Organized/{CATEGORY}.md files + INDEX.md
```

### classify_driver.py — AI Attachment Classification
```bash
# Parallel classify 972 attachments via Kimi + Gemini
# Adds discipline + description + suggested destination
python3 classify_driver.py
# Results merge into the category MD files
```

## Category Files

| Category | Emails | Range | Description |
|---|---|---|---|
| DOC | 206 | 2025-07→2026-05 | Document Submittals (تقديم مستندات) |
| MAR | 112 | 2025-10→2026-05 | Material Approvals (اعتمادات وعينات المواد) |
| IR | 141 | 2025-08→2026-05 | Inspection Requests (طلبات استلام الأعمال) |
| MIR | 67 | 2025-10→2026-05 | Site Material Inspection (فحص مواد بالموقع) |
| SDR | 88 | 2024-08→2026-05 | Shop Drawings (المخططات التنفيذية) |
| RFP | 35 | 2025-08→2026-05 | Technical Proposals (مقترحات فنية) |
| RFI | 9 | 2025-08→2026-05 | Requests for Information (استفسارات) |
| SCH | 15 | 2025-08→2026-01 | Schedules (الجداول الزمنية) |
| REP | 5 | 2025-11→2026-01 | Reports (التقارير والخطط) |
| SI | 7 | 2025-11→2025-12 | Site Instructions (ملاحظات الموقع) |
| GEN | 132 | 2023-09→2026-05 | General Correspondence (رسائل عامة) |

## Update Workflow
1. Move staged files from `attached/` to proper destination folders
2. Re-run `02_generate_md.py` to flip status 📥 → ✅
3. Do NOT edit category MD files manually for status changes — let the script handle it
4. For new emails: re-run `01_extract.py` then `02_generate_md.py`

## Auto-Sort Routing
Based on discipline code in filename:
- `-STR-` → `Submittal's/Struc`
- `-EL-` or `-ME-` → `Submittal's/Mep`
- `-AR-` → `Submittal's/Arch`
- Others → manual review

## Key Paths
- Outlook source: `sultan@samayainvest.com` → `Zamzam Projects`
- Attachments cache: `Zamzam -Visitor Center/attached/` (972 files)
- Category MD files: `Zamzam -Visitor Center/Docs/Zamzam_Emails_Organized/`
- Pipeline scripts: `Zamzam -Visitor Center/Docs/_Tools/`
- SharePoint links: `samayainvestksa-my.sharepoint.com`
