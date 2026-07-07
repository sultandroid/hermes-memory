# Downloads Organization Pattern

## Class: File System Organization

A recurring class of task where the user asks to "check," "clean," "organize," or "sort" the Downloads folder (or similar accumulation points). This is NEVER a simple `ls` / delete operation — it has a defined full workflow.

## Trigger Phrases
- "check download folder" / "check my Downloads"
- "clean up Downloads"
- "organize my downloads"
- "sort the download folder"
- "what's in Downloads"

## Full Workflow (7 Phases)

### Phase 1: Discovery & Inventory
Scan every file and folder. For each item capture: path, size, mod date, SHA256 hash, extension, parent folder. Group exact duplicates by hash. Identify version variant groups by normalized filename. Output: inventory CSV + dedup report + version variants report.

**Tools:** `find`, `sha256sum`, `du -sh`

### Phase 2: Classification & Project Mapping
Categorize each file into bucket: project-specific, general admin, software, personal, unknown. For spreadsheets: inspect sheet names and sample rows to determine project. Build proposed move plan with confidence levels (high/medium/low/unknown).

**Known projects for Mohamed Essa:**
- Aseer Museum (3092) — Abha, D&B exhibition fit-out
- Zamzam (121) — museum project
- Tahakom — BOQs, experience center
- RCRC — BOQs
- Esnad — feasibility studies
- Samaya Factory/Workshop — production costing, machine lists
- Haramain Museums (Makkah & Madinah) — museum production
- General Samaya — employee lists, Odoo exports, HR

### Phase 3: Destination Folder Structure
Create project-based hierarchy. Use this standard structure when project folders don't have existing conventions:

```
_organized/Downloads_Import_YYYY-MM-DD/
  00_Admin/            — Templates, Registers
  01_ProjectName_ID/   — Project-specific (Commercial, Design, Production subfolders)
  02_Zamzam_121/
  03-99_Other_Projects/
  11_Images/           — Workflow_Diagrams, AI_Generated, Photos, WhatsApp, Reference
  12_Media/            — Audio, Video
  13_Web/              — HTML files
  14_Personal_NonWork/
  99_Archive/          — Old_Versions, operation_log, final_report
  __SECURE/            — SSH keys, sensitive files (flag for proper placement)
```

**Note:** If `~/Samaya/` doesn't exist locally (project files are on OneDrive), stage in `~/Downloads/_organized/Downloads_Import_YYYY-MM-DD/` and flag for sync.

### Phase 4: Dedup & Versioning
- **Exact duplicates** (same hash): keep one canonical (newest mod time, clearest filename), delete rest
- **Version variants** (similar name, different hash): keep latest/most-complete version in project folder, move older versions to `99_Archive/Old_Versions/`

Common version groups seen in this environment:
- `employee_list_*.xlsx` (10+ versions — keep FINAL_ALL_MATCHED or largest)
- `overtime_january_2026*.xlsx` (6 versions — keep formatted latest)
- `دراسة_الجدوى_الشمسية_v2*.xlsx` (8 versions — keep highest number)
- `Production_Costing_Planner*.xlsx` (keep SAR_FIXED_CORRECTED)
- `Technical Office Log*.csv/xlsx` (keep .xlsx as canonical)
- `Register Log_*.csv` (match to project registers, keep in Admin/Registers/)

### Phase 5: Move Execution
Execute the approved move plan. Create destination folders as needed. Preserve original filenames. Resolve collisions with `_imported_YYYYMMDD` suffix. Generate operation log CSV with: SourcePath, DestinationPath, Action (move/delete/keep), Size, Reason.

### Phase 6: Register & Memory Update
Update ALL knowledge stores:
1. Hermes agent memory (via `memory` tool)
2. PROJECT_MEMORY.md for Aseer Museum (OneDrive path) — append session update
3. Notion Aseer-Museum page (page ID: `2e36d275-a6c9-4857-87c7-094084138b6a`) via `ntn api` markdown PATCH
4. Project registers (if applicable)

### Phase 7: Final Report
Produce a report with:
- Summary statistics (files processed, moved, deleted, archived)
- Space reclaimed
- Files moved by project (each project section with count and key contents)
- Older versions archived (table of variant groups)
- Outstanding items (SSH keys, sync needed, leftover directories)

## Known Environment Facts (Mohamed Essa's Mac)
- **Downloads location:** ~/Downloads/
- **Project files:** OneDrive - SAMAYAINVESTMENT/Samaya/Technical Office/Bim Unit/
- **Local project code:** ~/Projects/estmat/ (Odoo)
- **PROJECT_MEMORY.md:** OneDrive-SAMAYAINVESTMENT/Samaya/Technical Office/Bim Unit/Aseer-Museum/PROJECT_MEMORY.md
- **Notion Aseer page ID:** 2e36d275-a6c9-4857-87c7-094084138b6a

## Pitfalls
- **read_file() contamination:** NEVER pipe `read_file()` output to `write_file()` — the tool returns line-number-prefixed content. Use `cat` via terminal to get raw content.
- **Arabic filenames:** Preserve as-is — do not transliterate.
- **Business documents:** Never delete older versions without user approval — archive them.
- **SSH keys:** If found in Downloads, move to `__SECURE/` folder and recommend `chmod 600` in `~/.ssh/`.
- **"Scan Downloads" scope = ALL files, not just your current workstream.** When the user says "check download folder", classify EVERY file — not just ones matching document codes (PL, ZD, SH, etc.). Include: proposals, vendor quotes, RFIs, meeting minutes, shop drawings, structural calcs, CVs, design drawings, correspondence, images, and any other document. The user corrected this explicitly: "useful for anything not only for plans".
