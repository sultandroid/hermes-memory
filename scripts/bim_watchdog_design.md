# BIM Downloads Watchdog — Full Processing Pipeline

## Overview
A cron-driven system that watches `~/Downloads`, moves new project files to correct BIM folder, then uses Claude Code to analyze, register, and document every file.

## Phase 1: Detection & Classification (watchdog script)
**Trigger:** Cron every 1hr → `bim_watchdog.py --once`

```
~/Downloads/new_file.pdf
  ├── Keyword match → Project + Subfolder
  ├── Checksum check → already exists? SKIP (no duplicate)
  ├── Filename check → same name at destination? SKIP
  └── Move file → BIM/Project/Subfolder/file.pdf
```

**Rules:**
- Non-project files: ❌ LEAVE IN DOWNLOADS (no move)
- Duplicate by checksum: ❌ SKIP 
- Duplicate by filename: ❌ SKIP
- ZIP: extract then move

## Phase 2: Content Analysis (Claude Code labor)
After file moved, trigger Claude Code to analyze it.

**Input:** File path, project name, subfolder
**Process:** Claude reads file (PDF/image/docx/xlsx/eml) and extracts:
- Document type (Submittal, RFI, MAR, Invoice, Drawing, Contract, etc.)
- Project reference codes (ASR-SAM-, ZAM-NWC-, etc.)
- Subject / title
- Date, revision, author
- Key data points (amounts, quantities, dates, parties)
- 2-3 sentence summary

**Output:** Structured JSON with all extracted metadata.

## Phase 3: Register Update (Claude Code labor)
Update the project's Excel tracking register.

**Supported registers (by subfolder):**
- `Submittal's/` → Submittal Log (.xlsx)
- `B.O.Q/` → BOQ Register (.xlsx)
- `Invoices/` → Invoice Register (.xlsx)
- `Contracts/` → Contract Register (.xlsx)
- `Docs/` → Document Register (.xlsx)
- `Specs & Datasheet/` → Material Register (.xlsx)

**Process:**
1. Find existing register file in project folder
2. Read existing rows, determine next row number
3. Append new entry with: Date, File Name, Type, Code, Description, Status
4. Save register

If no register exists, create a new one with header.

## Phase 4: Project Memory Update (Claude Code labor)
Update the project's MARKDOWN memory/constitution files.

**Files to update:**
- `PROJECT_MEMORY.md` — main project log
- `*CONSTITUTION.md` — if document affects scope

**Process:**
1. Read existing PROJECT_MEMORY.md
2. Add entry under "📦 Recent Documents" section:
   ```markdown
   | 2026-05-28 | [Type] | [File Name] | [Summary] | [Location] |
   ```
3. Save

## Phase 5: Notion Update (Claude Code labor)
Update the project's Notion database page.

**Prerequisite:** Notion API key configured. Pages shared with MacHermes bot.

**Process:**
1. Query Notion for the project database/page
2. Create/append a new database item with:
   - Title: File name
   - Date: today
   - Type: document type
   - Project: linked project
   - Status: Received
   - Summary: extracted summary
3. Save

## Pipeline Control
- If Phase 2 fails → log error, skip Phases 3-5
- If Phase 3 fails → log error, continue to 4-5
- If Phase 4 fails → log error, continue to 5
- All phases logged to `~/.hermes/data/bim_watchdog_processed.json`

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│  Cron (every 1hr)                                       │
│  └─ bim_watchdog.py --once                              │
│      ├── Check Downloads for new files                  │
│      ├── Classify → project + subfolder                 │
│      ├── Dedup check (checksum + filename)              │
│      ├── Move file                                      │
│      └── Save processed tracking                        │
│                                                         │
│  After all moves done, for EACH moved file:             │
│  └─ delegate_task to Claude Code:                       │
│       [1] Read & analyze file → structured summary      │
│       [2] Update project Excel register                 │
│       [3] Update project MD files                       │
│       [4] Update Notion project page                    │
└─────────────────────────────────────────────────────────┘
```
