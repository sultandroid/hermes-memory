---
name: bulk-file-organization
description: Systematic methodology for organizing large filesystem collections (1K-100K+ files) — rename misspellings, restructure directories, classify loose files, deduplicate, and generate a searchable serialized index.
tags: [filesystem, cleanup, organization, file-management, rename, classification]
related_skills: [project-email-archive, bim-project-register, samaya-technical-office]
---

# Bulk File Organization

Methodology for large-scale filesystem reorganization. Use when a directory has hundreds+ of loose files, inconsistent naming, spelling errors, or nested redundancy.

## Pre-pass: Survey → Plan → Approval → Execute

Before large reorganization jobs, present the user with a structured plan:

1. **Survey**: measure scope — file count at root, dir tree, disk usage (`du -sh`, `find -maxdepth`)
2. **Categorize**: classify files by type prefix, project code, and function using a script (e.g. Python with `os.listdir`)
3. **Propose**: write a clear table with issue count, action phases, expected destinations, and notes
4. **Confirm**: get user approval before executing any move/delete
5. **Execute**: batch operations in phases (delete junk first, then route files, then organize subdirectories). Write moves as a single bash script with `set -e` for atomic execution — prevents partial failure and gives one clean verification step.
6. **Verify**: confirm root is clean, count remaining files, spot-check destinations

This avoids surprises and lets the user catch errors before data moves. Format:

```
| Issue | Count | Notes |
|---|---|---|
| Loose files in root | 251 | PDFs, DWGs, XLSX |
| UUID temp files | 92 | OneDrive cloud stubs |
| image*.png/jpg junk | 40 | Email extracts |
| .dwl/.dwl2 lock files | 1,597 | AutoCAD — safe to delete |
```

Then present phases:

```
**Phase 1** — Delete junk (safe)
**Phase 2** — Route root files → project folders
**Phase 3** — Organize auxiliary folders (Reports/, Scans/, etc.)
```

### Delegation for large moves

For root-level file routing (100+ files to multiple destinations), delegate to parallel subagents using `delegate_task(tasks=[...])`. Each subagent handles a file category (Aseer docs, company docs, remaining orphans). This keeps your context window clean and lets moves run in parallel.

Pass the complete file-to-destination mapping in the `context` field. Each subagent should:
- Use `mv` (not copy) for files on the same filesystem
- Create destination dirs with `mkdir -p`
- Verify counts match expected
- Report back what was moved and any issues

## Multi-pass strategy

Always work in isolated passes. Never mix concerns.

### Pass 1: Inventory

Understand scope before changing anything.

```
find "$BASE" -type f | grep -v '.DS_Store' | wc -l
find "$BASE" -type d | sort
find "$BASE" -maxdepth 1 -type f | sort | head
```

Use `find -maxdepth` to check root-level files separately from nested ones.

### Pass 2: Detect issues

Scan for:
- **Spelling**: directory names and file names with common typos
  - `Visulizations` → `Visualizations`, `Regester` → `Register`, `Basment` → `Basement`
  - `Digram` → `Diagram`, `Schamatic` → `Schematic`, `Requierments` → `Requirements`
  - `Arrangment` → `Arrangement`, `Appencices` → `Appendices`, `Musuem` → `Museum`
  - `Deliveable` → `Deliverable`, `Sitwork` → `Setwork`
  - `BIm Team` → `BIM Team`, `Regester` → `Register` (case/typo in folder and filenames)
  - `Asher` → `Aseer`, `ASEER` → `Aseer` (project code consistency — non-official names only)
- **Cloud sync marker files**: `.dc_purpose`, `.dropbox`, `desktop.ini` — identify and preserve, never move or delete
- **Empty/corrupt stubs**: files exactly 4 bytes in size are failed uploads or incomplete syncs. Flag for user decision rather than deleting automatically
- **Zero-byte files**: files exactly 0 bytes are genuinely empty/corrupted (distinct from 4-byte stubs and OneDrive cloud-only placeholders which show 0 bytes in `ls -la` but have content). Safe to move to an `00_Empty_Files/` archive subfolder rather than leaving loose at root
- **Organization**: empty overlapping dirs, loose files at root, redundant nesting
- **Duplicates**: `(1)` suffix files, 4-byte stubs, same-size files
- **Formatting**: double spaces, trailing spaces, `Asser` vs `Aseer` (project code inconsistencies)
- **Nesting**: single-child dir chains like `Life_Safety_Drawings/Life_Safety_Drawings/`

Use Python for bulk pattern detection with `os.listdir` and regex; use `find` for shell-level detection.

### Pass 3: Fix spelling

Rename directories **first** — directory renames affect all child paths and avoid stale path references in subsequent operations.

```
os.rename(old_dir, new_dir)    # Python (atomic on same filesystem)
mv -n old_dir new_dir          # Shell (no-clobber)
```

- Use `mv -n` (no clobber) to prevent accidental overwrites
- Always check `os.path.exists(dst)` before rename
- For directories with files inside, rename works atomically on macOS
- **Do NOT rename** external document IDs (e.g., `MOC-Asser-SIC-*`, `SI-CG-*`). These are the sender's reference numbers and must be preserved even if misspelled. Flag them in the register with a note.

### Pass 4: Flatten nesting

Remove unnecessary single-child directory chains:

```
# Pattern: flatten /Parent/SingleChild/ -> move files up
for f in Parent/SingleChild/*; do mv f Parent/; done
rmdir Parent/SingleChild
```

Check for: `folder/subfolder/subsubfolder` where all three have the same name/category.

### Pass 5: Classify loose files

For root-level files (or any flat directory with mixed content):

1. Define category rules as ordered list of lambda/regex functions
2. First match wins — order by priority (most specific first)
3. Track unclassified files for manual assignment

```python
categories = [
    ("01_Plans_and_Reports", [
        lambda f: name_contains(f, "weekly report", "design management"),
        lambda f: name_matches(f, r'moc[-_]'),
    ]),
]
```

Helper functions pattern:

```python
def ext_in(f, *exts):
    return os.path.splitext(f)[1].lower() in exts

def name_contains(f, *patterns):
    fn = os.path.basename(f).lower()
    return any(p.lower() in fn for p in patterns)

def name_matches(f, *patterns):
    fn = os.path.basename(f).lower()
    return any(re.search(p, fn) for p in patterns)  # use string patterns
```

4. Batch-move using `shutil.move(src, dst)` in Python
5. Verify root directory has zero files afterward
6. Handle destination conflicts by appending `_moved` suffix

### Pass 5a: Map to existing folder hierarchy (if present)

Before defining new category targets, check if the project already has a **numbered document-control structure** (e.g. `00_Admin`, `01_Contracts`, `02_Plans`, `03_Submittals`... up to `99_Reference`). If so, classify loose files into those existing subfolders by content type rather than creating a parallel structure:

| Content type | Likely target in numbered hierarchy |
|---|---|
| Scope of Work, proposals, fee docs | `01_Contracts_and_ER/` or `01.3_Contractors_SOW/` |
| Schedules, programmes, plans | `02_Plans_and_Procedures/` (e.g. `02.8_Master_Programme/`) |
| Analyses, markdown reports | `07_Reports/` or equivalent |
| Financial/overhead docs | `04_Financial/` |
| Emails, sent items, correspondence | `11_Correspondence/` (e.g. `11.1_To_From_CG/`) |
| Spec sheets, vendor literature | `99_Reference/` |
| Inspections, test records | `10_Test_and_Inspection/` or `03_Inspection_Requests/` |

Check the sub-structure inside each numbered folder before routing — many have numbered sub-subfolders (e.g. `02.8_Master_Programme/` under `02_Plans_and_Procedures/`). Route to the most specific match.

After classifying loose files, handle `_ARCHIVE/` or similarly named archive folders that mirror the live structure:

1. **Inventory archive subdirs** — compare against live counterpart
2. **Remove exact duplicates** within archive using content hash (MD5):
   ```python
   for h, paths in hash_map.items():
       if len(paths) > 1:
           # Keep in more structured location, delete rest
   ```
3. **Merge fragmented archives** — if old revisions are split across `Previous_Spec_Versions/` and `Old_Spec_Revisions/`:
   - Merge into a single versioned hierarchy (e.g. `Version 00 - Earliest` through `Version 05`)
   - Remove empty source folders
4. **Propagate sequential archives** to live location — if archive contains sequentially-numbered documents (e.g. DIS_003, DIS_005, DIS_006) that extend the live set (DIS_014+), move them to the live folder. They are not duplicates — they fill a gap in the sequence.
5. **Consolidate single-file subdirs** — folders containing individual page PDFs that were later compiled into combined documents should be kept in the archive but renamed clearly (e.g. `02_Old_Individual_Appendix_PDFs` instead of `02_Appendix_PDFs`).
6. **Handle orphan doubles** — files with ` 2` or `(1)` suffixes but different content than the original: verify uniqueness via hash, then merge into the main archive collection.

### Pass 5c: Re-label misnamed folders

If during classification or user feedback, a folder name is found to be inaccurate (e.g. `03_Sketch_Sheets` actually contains clash review documents), rename immediately:

```python
os.rename(old, new)   # Python atomic rename on same filesystem
```

- The new name must describe actual content, not the original label
- Check the document metadata/title when possible to confirm content
- User correction of folder naming is a high-priority signal — do not defer

### Pass 6: Build target structure

Before moving, plan the new directory tree. Number prefix for ordering:

```
01_Plans_and_Reports
02_Correspondence
03_NCRs_and_SIs
...
```

Guidelines:
- Use zero-padded 2-digit prefixes (01-99)
- Use underscores not spaces
- Keep names descriptive but concise
- Avoid redundancy (not `07_Visualizations_Packages` — `07_Visualizations` is enough)

### Pass 7: Generate serialized register

After all moves, build a CSV index:

```
Serial, Category, Subcategory, Path, Filename, Extension, Size_KB, Modified, Issues
```

The register:
- Serves as the deliverable artifact
- Tracks remaining issues (unfixable items like external IDs)
- Enables future search without filesystem scans
- Column `Issues` flags: `SPELL:`, `DUP:`, `NOTE:`, `FORMAT:`

### Pass 8 (NEW): Cross-project file relocation

After classifying all files within the target directory, identify files that belong to **other projects** — not just misplaced within the same project, but actual cross-contamination from other project folders.

**Signals of cross-project files:**

| Signal | Example | Action |
|--------|---------|--------|
| Different project code prefix | `P083_*` in Aseer folder → Zamzam project | Move to target project with descriptive subfolder |
| Third-party company docs for another site | `MVii Makkah Model` files → Makkah-related project | Route by location/scope |
| Contract/legal for another entity | `عقد مشروع مسجد النور` → Masjid Alnoor project | Move to target's Contracts/ |
| Subcontractor docs for different building | Haram barriers report → El-Haramain Museum | Move to target's Docs/ |
| Drawing number matches known project | `TF2438MSC` → Zamzam Museum | Confirm via search before moving |

**Process:**

1. **Search broadly** before concluding a file is off-project:
   ```python
   # Check if the code exists elsewhere in the project tree
   find "$WORKSPACE" -type f -iname "*<code>*" 2>/dev/null
   ```
   A code like `M2742` may actually belong to the current project (found in Contracts/ and Docs/ elsewhere under Aseer-Museum). A code like `P083` belongs to a different project (Zamzam).

2. **Consolidate scattered discipline items under numbered parents**: When an existing numbered hierarchy has good bones but discipline-specific items (registers, scripts, packages) are scattered at root:
   - Identify the anchor folders (existing numbered dirs)
   - Classify each root item by which anchor it belongs to (by discipline, not name alone)
   - Create new numbered folders for items that don't fit existing anchors but deserve their own number (e.g. `04_Registers/` for all registers, `07_Drawing_Source_Folders/` for extracted packages)
   - **One-shot script execution**: Write ALL `mv` commands into a single bash script with `set -e`. This prevents partial failure and gives you one verification step. Run then verify with `ls -1 | wc -l` on root + spot-check destinations.
   - **Keep project-wide tools at root**: Cross-cutting scripts (scheduling, dashboards, master registers) that apply to the whole folder stay at root to signal their project-wide role.

3. **Route to canonical location**, not a catch-all. The user prefers files moved directly to the correct project's subfolder (e.g. `Zamzam Museum/Design Files/`), not into an intermediate `_Unrelated_Projects/` holding pen.

4. **For ambiguous codes**, check broader workspace:
   - `Samaya/Technical Office/Bim Unit/<Project Name>/` — all BIM project folders
   - Search across `Samaya/` recursively for the code
   - Check the project's `Design Files/`, `Docs/`, `Completed Tender Package From NRS/` for matching files

4. **Common Samaya project code mappings** (discover via search, update as new codes appear):
   - `A2742`, `MOC-MUS-ASE`, `MOC-ASEER` → Aseer Museum
   - `P083` → Zamzam Museum / Zamzam Visitor Center
   - `MVii` Madinah-related → El-Haramain Museum
   - `MVii` Makkah-related → Zamzam Museum (or whichever project has MVii docs)
   - `TF2438` → Zamzam Museum
   - `M2742` → Aseer Museum (different document series, same project)
   - King Khaled Road references → Aseer Museum (museum is located on King Khaled Road)
   - `مسجد النور` / `Al-Noor` → Masjid Alnoor project

5. **Move files using shutil** with proper directory creation:
   ```python
   os.makedirs(os.path.dirname(dst), exist_ok=True)
   shutil.move(src, dst)
   ```
   
6. **Verify destination** after move and clean up empty source directories.

**Pitfall**: The `_Unrelated_Projects` catch-all folder is NOT the desired pattern. The user wants files routed directly to their correct project directory. A catch-all should only be a temporary staging spot during analysis, never the final destination.

### Pass 9: Verify

```
find "$BASE" -maxdepth 1 -type f | wc -l    # should be 0
find "$BASE" -type f | wc -l                 # compare with initial count
```

Rebuild and re-scan the register. Verify no new issues were introduced.

## Pitfalls

- **OneDrive sync**: Bulk operations on OneDrive can trigger sync contention. Keep individual rename/move batches under 200 operations at a time. Python `os.rename` and `shutil.move` are safe on local OneDrive sync folders.
- **`(1)` duplicates**: Check file size before deciding. 4-byte files are empty stubs (safe to delete). Files with similar size but different content are genuine — keep both.
- **External doc IDs**: `MOC-Asser-SIC-*`, `MOC-MUS-ASE-*`, `SI-CG-*` are official document control numbers from the sender. Do NOT rename even if the project code is wrong (`Asser` vs `Aseer`). Document in register instead.
- **Version dirs**: `Version 01`, `Version 02` are semantic version labels. Keep the space. Do not convert to `Version_01`.
- **Empty dirs**: Check for overlapping top-level dirs (`Approval and Stamping` may duplicate `02_Approved_Stamped_Packages`). Remove only if confirmed empty and redundant.
- **Don't over-normalize vendor content**: Vendor delivery folder names with natural English (`Free Standing Wall`, `Stage 03 Appendices`) are fine. Only fix clear spelling errors.
- **Ambiguous date folder names**: Date-named folders like `8-6-26`, `26-06-26`, `06-26-26` are ambiguous (DD-MM vs MM-DD). Rename to ISO 8601 format `2026-08-06` when restructuring. The rename + parent move can be done in one `mv` command: `mv "8-6-26" "05_Batch_Deliveries/2026-08-06"`.
- **OneDrive cloud stubs**: Files with UUID-format names (8-4-4-4-12 hex, e.g. `080a42ed-7339-41d7-a030-600b9d422664`) that are exactly 4 bytes are OneDrive cloud-only placeholder stubs. They have no local content — the actual file exists only in the cloud. Do NOT delete them; OneDrive uses them for sync tracking. Includes both extensionless files and ones with `.jpg`/`.jfif`/`.jpeg` extensions.
- **OneDrive junk file patterns**: These are safe to bulk-delete from OneDrive roots:
  - `image*.png`, `image*.jpg`, `image*.jpeg`, `image*.gif` — email/Outlook extracted images
  - `Outlook-*.png`, `Outlook-*.jpg` — email signature artifacts
  - `ATT00001.gif` — legacy email attachment header
  - `Icon` (0 bytes, filename may contain carriage return) — macOS resource fork artifact
  - `*.dwl`, `*.dwl2` — AutoCAD lock files, always safe to delete (may need `find -exec rm` if `-delete` hangs due to OneDrive sync)
- **Consolidating duplicate subdirs**: When two folders have the same purpose but different names (e.g. `Budget/` and `Budgets/`, `Projects List/` and `ProjectsList/`), merge content into the better-named one, then delete the other. Always check content of both first.
- **Root files with project code prefixes**: Categorize root-level files by examining their filename prefix:
  - `MOC-*`, `SI-*`, `A2742-*`, `M2742-*` → Aseer Museum project
  - `ZAM-*`, `P083-*` → Zamzam Museum / Visitor Center
  - `MVii-*` → Madinah/Haramain project
  - `CV*`, `CV Submittal*` → HR / company docs
  - `Leica*`, `RTC360*`, `Spider*`, `BLK360*`, `EinScan*`, `Cyclone*` → hardware spec sheets

### Scan folder organization (Pass 5e)

When reorganizing folders of dated scan images (common in construction/administration), group by calendar period:

**Date formats encountered on macOS OneDrive:**
| Pattern | Example | Group |
|---|---|---|
| `Scan DD Mon YY HH·MM·SS` | `Scan 21 Feb 23 16·40·24` | Year folder (`2023/`) |
| `Scan DD Mon. YY · HH·MM·SS` (Gregorian) | `Scan 01 Mar 23 12·42·50` | Year folder (`2023/`) |
| `Scan DD Mon. YY · HH·MM·SS` (Hijri with colons as ·) | `Scan 24 Rmdn. 44 · 22·47·01` | Hijri year folder (`1444_AH/`) |
| Payment/account folders (Arabic names) | `حساب يوسف وعطا مايو ٢` | Department group (`حسابات_عمالة/`) |
| Vacation/HR folders | `Raji vacation` | HR group (`إجازات/`) |

**Hijri month abbreviations:** `Rmdn.`=Ramadan, `Shwl.`=Shawwal, `Dhuʻl-H.`=Dhul-Hijjah, `Dhuʻl-Q.`=Dhul-Qi'dah

**Process:**
1. Parse date from folder name (both Gregorian and Hijri patterns)
2. Group into year folders: `2023/` for Gregorian, `1444_AH/` for Hijri
3. Group non-date folders by functional category (labor accounts, vacations, invoices)
4. Move the entire dated folder (preserving its name and contents) under the group folder
5. Leave loose PDFs at the root of Scans/ for manual review

This preserves the original folder structure while adding navigable hierarchy.

## Examples

- `references/nrs-tender-package-reorganization.md` — 19,168 files across Aseer Museum NRS Completed Tender Package
- `references/aseer-museum-09-registers-cleanup.md` — 206 files in project registers folder (~30 loose, typos, corrupt stubs)
- `references/onedrive-root-cleanup-patterns.md` — 250+ loose files at OneDrive root, routing by project code prefix, Reports/ consolidation, Scans/ date grouping
- `references/sister-companies-project-folders.md` — Renaming Arabic subsidiary files to English, creating per-project folders from a numbered list (متجر/كافيه format), searching Downloads for related files
- `references/aseer-museum-02-submittals-reorg.md` — Consolidating scattered discipline registers under numbered hierarchy, one-shot batch script execution, ISO date rename, project-tools-kept-at-root decision

---

## Domain: macOS-Specific Housekeeping (absorbed from `macos-housekeeping`)

For cleaning up personal macOS folders (Downloads, Desktop, Documents) and handling cloud-storage quirks unique to macOS.

### When to Use

User says "check my Downloads folder", "clean up Desktop", "this folder is a mess", or anything about file clutter on a personal macOS folder. For Project/BIM directory reorganization, use the main workflows above.

### macOS Clutter Categories

| Category | Indicators | Disposition |
|----------|------------|-------------|
| **App duplicates** | Same .app bundle in two locations (e.g. "App 2/") | Delete duplicate |
| **Excel temp files** | `~$*.xlsx`, `~$*.docx` | Delete — Excel crash/lock artifacts |
| **Empty folders** | Folders containing only `.DS_Store` | Delete |
| **Version noise** | `file (1).xlsx`, `file_FINAL.xlsx`, `file_FINAL_CORRECTED.xlsx` | Ask user — keep latest |
| **Iteration chains** | `report_v2.xlsx` → `report_v2_1.xlsx` → `report_v2_7.xlsx` | Ask user — keep latest |
| **Test artifacts** | `.test_*`, temp debug files | Delete |
| **Old installers** | `.dmg`, `.pkg` from past installs | Ask user |
| **Hidden macOS files** | `.DS_Store`, `.localized` | Ignore (or delete at end) |
| **BIM temp/cache** | `.pcp`, `.bak`, `.slog`, `.rws`, `.dat`, `.dwl`/`.dwl2` | Delete — all safe to remove |
| **Render/export temps** | `Bitmap*.png/jpg`, `cd*.jpg`, `881214*.jpg` | Delete — render farm / visualization cache |
| **Garbled filenames** | Corrupted Unicode names (`´`, `¦`, `¢`, etc.) | Delete — corrupted |
| **OneDrive 0-byte placeholders** | Files showing `0` bytes in `ls -la` but not actually empty | Treat with caution — cloud-only |
| **Other-project files mixed in** | Filename prefix doesn't match the containing folder's project | Archive out to correct project |

### macOS Diagnostics for Cloud Files

**OneDrive dataless detection:**
```bash
ls -laO file.md
# → compressed,dataless flag
fileproviderctl evaluate /path/to/file
# → isDownloaded, isDownloading, isUploading, isKeepDownloaded
```

**Stuck state** (orphaned placeholder - can never be materialized):
- `isUploading=1` + `isDownloaded=0` + `mostRecentVersionDownloaded=0`
- Recovery: re-create file from source, or check OneDrive web

**Recovery options for locked files:**
1. `open <file>` in native app (Preview for PDFs) — triggers OneDrive hydration
2. `cat src > /tmp/x && mv /tmp/x dst` — bypasses `fcopyfile` deadlock (OneDrive only)
3. `osascript -e 'do shell script "python3 <script.py> 2>&1"'` — works when direct shell access fails
4. `brctl download <path>` — forces sync; wait 1-2s

### iCloud File Coordination Locks

Files in iCloud-synced directories may get locked by the `bird` daemon. Symptoms:
- `cat file` → `Resource deadlock avoided`
- Python `open()` → `OSError: [Errno 11]`
- Has `com.apple.provenance` extended attribute

**Workaround:** `shutil.copy2()` in Python bypasses the `fcopyfile` syscall and works even when `cp`/`ditto`/`cat` all fail. For reading, use Swift's `NSFileCoordinator`.

### OneDrive Folder Rename Restrictions

**NEVER batch-rename OneDrive folders with `mv`** — this corrupts ALL siblings under the same parent, even untouched ones. Each sibling shows `isUploading=1, isUploaded=0` with error "The file doesn't exist."

**Safe rename methods (in order of reliability):**
1. OneDrive web UI (onedrive.live.com) — one folder at a time
2. `URLResourceValues.name` via Swift (`.setResourceValues`) — uses proper `FPItem` API
3. AppleScript `set name of folder` — goes through Finder

### BIM / Construction Project Cleanup

In addition to the main Pass methodology above, BIM folders have specific needs:

**Separating emails from project documents**: Email .md files typically have date prefixes (`2024-05-30 - Subject.md`) or email keywords (RE:, Fw:). Project .md files have structured codes (`ZAM-SAM-121-ADM-INIT-*`). Move email files to an `Email_Archive/` folder.

**Legacy projects/ subfolder merging**: When root-level numbered folders (`01_ProjectName`) coexist with a `projects/` subfolder containing the same projects' older content:
1. Check each pair for content location
2. Use `mv` for individual items (instant on OneDrive — metadata-only)
3. For "Directory not empty" conflicts, merge contents iteratively
4. Verify all numbered folders have content before removing `projects/`

### macOS-Specific Tool Reference

| Tool | Use for | Safety |
|------|---------|--------|
| `search_files(target='files')` | enumerate contents | read-only |
| `du -sh` | size checks | read-only |
| `find . -name '...' -type f -delete` | bulk temp-file removal | destructive — dry-run first |
| `fileproviderctl evaluate <path>` | OneDrive sync diagnosis | read-only |
| `sips` | image metadata extraction | read-only |
| `execute_code` + Python `os` module | operations with Arabic/special chars in filenames | safe |

### Reference Files (moved to this skill's references/)

## Domain: Client/Project Folder Hierarchy Setup (absorbed from client-project-folder-setup)

For basic client and project folder creation (not bulk reorganization — this is initial setup), use this simple Python pattern:

```python
import os

def create_client_project_folders(base_path, client_projects):
    os.makedirs(base_path, exist_ok=True)
    for client, folders in client_projects.items():
        client_path = os.path.join(base_path, client)
        os.makedirs(client_path, exist_ok=True)
        for folder in folders:
            project_path = os.path.join(client_path, folder)
            os.makedirs(project_path, exist_ok=True)

# Example:
create_client_project_folders("/path/to/projects", {
    "Client A": ["01_Project_Alpha", "02_Project_Beta"],
    "Client B": ["03_Project_Gamma"],
})
```

### Register / Spreadsheet Column Cleanup

When removing columns from Excel registers by matching header text, always exact-match, never substring-contain. `"SOW" in "Submittal / Deliverable (per SOW)"` is True and will delete the entire description column. Use:
```python
CLEAN = {'SOW', 'ER', 'SOW §', 'ER §'}
clean = header.strip().replace(' ','')
if clean in CLEAN:
    cols_to_delete.append(col)
```

Always verify one file before batch — print headers after cleanup on a single file. A missing description column means entire register's data is unreachable. Recovery requires regenerating from original generator scripts (which may also be corrupted).

**Recovery pattern when both .xlsx and .py are damaged:**
1. Find original .py data via `session_search` — original 8-field tuples
2. Strip SOW/ER fields → 6-field tuples preserving descriptions
3. Delegate regeneration to subagent with complete data + template
4. Copy .py with `cp`; copy .xlsx with AppleScript/Finder `duplicate` for OneDrive safety
5. Verify with openpyxl header check on ALL files after deploy

### Pitfalls
- Always use absolute paths to avoid unexpected directory creation
- The `exist_ok=True` parameter prevents errors if folders already exist
- Ensure write permissions to the base path

---

- `references/bim-project-cleanup.md` — BIM-specific folder cleanup, legacy projects/ subfolder merging, email vs project doc separation
- `references/downloads-cleanup-guide.md` — Downloads cleanup patterns, Excel version chains, register dumps, presentation format
- `references/incoming-document-triage.md` — Receiving new project documents from Downloads: study, file, update memory, advise user. Covers PQ/MA/ZD/MS doc types, discipline mapping, `mv`-not-`cp` pitfall, register update checklist
- `references/tender-package-organization.md` — Tender (مناقصة) package subfolder setup: copy existing project files only, never generate new documents. Numbered folder structure, what to include/exclude, OneDrive copy pitfalls
- `references/xlsx-column-cleanup-pitfalls.md` — openpyxl column removal: exact-match headers not substring, recovery pattern for deleted description columns
- `references/project-folder-standardization.md` — Template-driven 13-folder project organization, content mapping rules
- `references/onedrive-dataless-diagnostics.md` — Full OneDrive dataless file diagnostics, recovery options, cascade corruption prevention
- `references/icloud-file-coordination.md` — iCloud Drive coordination lock fixes, NSFileCoordinator code

---
