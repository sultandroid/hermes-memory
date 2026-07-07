# Folder Standardization Pattern — Template-Based Reorganization

Standardize a project's document folder tree by applying a reference template structure across all subfolders.

## When to Use

- A project has 10+ subfolders (e.g., plan types, disciplines, work packages) with inconsistent organization
- Some folders are fully structured, others are flat or use different naming conventions
- You need a single, auditable, standardized structure that a future agent or human can navigate predictably

## The Pattern (11-Step)

### Phase 1: Study & Inventory

**Step 1 — Identify the reference folder.**
Pick the most thoroughly structured subfolder as the template model. Its existing subdirectory layout becomes the target. Document its structure:
```
00_Master_Index/
01_Source_Files/
  01_HTML/
  02_PDFs/
  03_Word/
  04_Assets/
02_CG_Responses/
03_Supplementary/
04_Registers/
05_Compliance_Audit/
06_Legacy_Files/
07_Guidelines/
README.md
```

**Step 2 — Take a BEFORE inventory.**
Use `find` to list all files + directories at maxdepth 2 across every subfolder. Save this to a file. It becomes the baseline for the audit.

### Phase 2: Structuring

**Step 3 — Rename inconsistent folder names.**
Fix spacing, punctuation, or naming discrepancies (e.g., `02.13 Stakeholder Plan` → `02.13_Stakeholder_Plan`). Do this first so all subsequent paths are consistent.

**Step 4 — Create the template structure in every subfolder.**
For each subfolder, create the full directory tree from the template:
```
for d in 00_Master_Index 01_Source_Files/01_HTML 01_Source_Files/02_PDFs \
         01_Source_Files/03_Word 01_Source_Files/04_Assets 02_CG_Responses \
         03_Supplementary 04_Registers 05_Compliance_Audit 06_Legacy_Files \
         07_Guidelines; do
    mkdir -p "$SUBFOLDER/$d"
done
```

**Step 5 — Classify and move root-level files.**
Rules for classifying files by name/extension:
| Pattern | Target |
|---------|--------|
| `.html` | `01_Source_Files/01_HTML/` |
| `.pdf` | `01_Source_Files/02_PDFs/` |
| `.docx` / `.doc` | `01_Source_Files/03_Word/` |
| `.png` / `.jpg` / `.gif` / `.svg` / `.ico` | `01_Source_Files/04_Assets/` |
| Filename contains `cg_response`, `code-b`, `code-c`, `comments response`, `review response` | `02_CG_Responses/` |
| `.xlsx` / `.xls` / `.csv` | `04_Registers/` |
| Filename contains `audit`, `compliance`, `gap` | `05_Compliance_Audit/` |
| Filename contains `backup`, `.bak`, `legacy`, `superseded`, `old_`, `obsolete` | `06_Legacy_Files/` |
| `.md` documents — name/flag-based (recovery→`00_Master_Index`, register→`04_Registers`) | Various |
| `.py` / `.txt` / `.css` / `.xer` / `.xml` | `03_Supplementary/` |
| `.dc_purpose` (Dropbox metadata) | `00_Master_Index/` |

### Phase 3: Consolidation

**Step 6 — Preserve existing organized content.**
Before moving anything, check each subfolder for pre-existing directory structures. If they contain useful content:
- Map old names to new template names (e.g., `PDFs/` → `02_PDFs/`, `HTML/` → `01_HTML/`, `Word/` → `03_Word/`, `assets/` → `04_Assets/`)
- Merge content by moving files FROM old structure INTO template structure
- Remove old empty directories after merging

**Step 7 — Consolidate old subdirectory names.**
Common old → new mappings:
| Old directory | New directory |
|---------------|---------------|
| `01_Source_Files/PDFs/` | `01_Source_Files/02_PDFs/` |
| `01_Source_Files/HTML/` | `01_Source_Files/01_HTML/` |
| `01_Source_Files/Word/` | `01_Source_Files/03_Word/` |
| `assets/` (at root) | `01_Source_Files/04_Assets/` |
| `_archive/HTML/` | `06_Legacy_Files/` or `03_Supplementary/` |
| `_archive/Scripts/` | `03_Supplementary/` |
| `_archive/Research/` | `03_Supplementary/` |

**Step 8 — Handle name conflicts without losing data.**
If a destination file already exists, append a suffix (`_1`, `_2`, `_legacy`, source-folder name) before the extension. Never overwrite.

### Phase 4: README & Audit

**Step 9 — Create/update README.md per subfolder.**
Each subfolder gets a standardized README.md documenting:
- The folder's purpose (e.g., `02.2 — BEP / MIDP / TIDP`)
- The template structure with explanation of each directory's purpose
- File classification rules table
- Checkboxes for whether each template directory exists

```markdown
# Folder Name

> Standardized structure following the **02_Plans_and_Procedures** template model (based on 02.1_DMP).

## Structure

  00_Master_Index/            ✓  Overview, index, recovery plans
  01_Source_Files/            ✓  Original source documents
    01_HTML/                  ✓  HTML source files
    02_PDFs/                  ✓  PDF submissions
    03_Word/                  ✓  Word documents
    04_Assets/                ✓  Images and logos
  02_CG_Responses/            ✓  Client/Consultant/Govt responses
  03_Supplementary/           ✓  Supporting references
  04_Registers/               ✓  Schedules, matrices, logs
  05_Compliance_Audit/        ✓  Audits, gap analysis
  06_Legacy_Files/            ✓  Superseded versions
  07_Guidelines/              ✓  Templates and conventions
```

**Step 10 — Audit the result (Codex QC).**
Run a full audit checking all acceptance criteria:
- [ ] All subfolders have 0 loose root-level files (only README.md)
- [ ] All subfolders have the complete template directory tree (00–07)
- [ ] Inconsistent folder names were renamed
- [ ] Existing organized content preserved (check a few key subdirs by name)
- [ ] Reference folder's internal structure preserved unchanged
- [ ] No files deleted or overwritten
- [ ] README.md present in every subfolder

**Step 11 — Fix and deliver.**
Apply all audit findings:
- Move hidden dotfiles (`.DS_Store`, `.dc_purpose`, `.dmp_authoritative_ref`) into `00_Master_Index/` or appropriate template directory
- Move any parent-level loose files into appropriate subfolders
- Re-audit after fixes
- Update memory with the final structure

## Pitfalls

- **Don't touch the reference folder's internal structure.** If the reference (DMP) has its own convention (e.g., `02_DMP_Chapters`, `04_Discipline_Files`, `05_Compliance_Audit_and_Mapping`), preserve both the old AND new template directories. The old dirs contain working content.
- **Don't delete legacy/archive folders.** Move their contents into the appropriate template directories and remove only the now-empty container.
- **Assets that contain internal assets/ subdirs.** DMP had `01_Source_Files/Assets/assets/`. Merge at the right level — don't create double nesting.
- **Sustainability-type folders with complex sub-subfolders** (consultants, codes, submittals). These are NOT loose files — they're organized content that should be preserved alongside the template dirs.
- **Parent-level loose files.** After organizing subfolders, check if the parent directory itself still has loose files. Move them into the correct subfolder's source directory.
- **"Scan Downloads" = ALL files, not just one category.** When the user says "check/scan download folder", classify EVERY file for usefulness to ANY project purpose. Don't filter by document code prefix (PL, ZD, etc.). Include proposals, vendor docs, meeting minutes, RFIs, drawings, shop drawings, structural calcs, CVs, and any other document. File each to its most appropriate location (plan 03_Supplementary/, 99_Archive/, or relevant plan 01_Source_Files/). The user corrected this explicitly: "useful for anything not only for plans".
