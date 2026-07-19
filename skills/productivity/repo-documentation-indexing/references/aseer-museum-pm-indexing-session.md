# Aseer Museum PM — Repo Indexing Session (2026-07-19)

## Scope
- Repository: `sultandroid/aseer-museum-pm` (Aseer Regional Museum)
- Total files: **476** across 80+ directories
- Files created: FILE_MANIFEST.md, QUICK_LINKS.md, DEPRECATION_LOG.md
- Files patched: README.md (ASCII tree diagram inserted)

## Key Findings

### Duplicate Detection
- **DMP files (13):** `99_Archive/01_Integration_Management/DMP_Design_Management_Plan/` duplicates `03_Plans/01_DMP/`
- **Stakeholder Plan files (15):** `99_Archive/10_Stakeholder_Management/Stakeholder_Plan/` duplicates `03_Plans/02_Stakeholder/`
- **HSE Plan analyses (9):** `99_Archive/08_Risk_Management/HSE_Plans/` duplicates `03_Plans/04_HSE/`
- **CG_STATUS.md** appears in 4 locations (1 live + 3 archive)
- **README.md** appears in 16+ locations (expected — each subfolder has its own README)

### Empty Stubs (0 bytes)
- `99_Archive/02_Scope_Management/Exhibition/.dc_purpose`
- `99_Archive/02_Scope_Management/Exhibition/DRYWALL_EMAIL_DATABASE.md`
- `99_Archive/02_Scope_Management/Structural/FP_22.pat`
- `99_Archive/10_Stakeholder_Management/Stakeholder_Plan/09_Integration_with_Other_Plans.md`

### Artifacts
- `03_Plans/02_Stakeholder/MOC-ASEER-SIC-1K0-PL-0020_Rev03_Stakeholder_Management_Plan.html.bak` (293KB)
- `scripts/__pycache__/odoo_sync_aseer.cpython-314.pyc`
- `99_Archive/02_Scope_Management/Register Log.xlsb - Shortcut.lnk`
- `99_Archive/07_Communications_Management/Meeting_Minutes/Aseer BIM Weekly Meeting.loop`
- `99_Archive/06_Resource_Management/Mobilization/plot.log`

### Marker Files (.dc_purpose)
- `00_Project_Charter/.dc_purpose` (71 bytes)
- `99_Archive/05_Quality_Management/QA_QC_Plans/.dc_purpose` (50 bytes)
- `99_Archive/10_Stakeholder_Management/RACI_Matrix/.dc_purpose` (55 bytes)
- `99_Archive/07_Communications_Management/Meeting_Minutes/.dc_purpose` (51 bytes)
- `99_Archive/02_Scope_Management/Exhibition/.dc_purpose` (0 bytes)

## Frontmatter Coverage
- Most registers in `01_Registers/` have `owner_agent` and `last_updated` populated
- Plan subdirectories (`03_Plans/*/`) have template files (README, plan_summary, checklist, approval_log) with frontmatter
- Archive files (`99_Archive/`) generally lack frontmatter
- Root files (CONSTITUTION, AGENTS, CHANGELOG, VERSION) all have frontmatter

## ASCII Tree Design
- 3 levels deep (root → folder → subfolder)
- Annotations on every folder with purpose description
- Root files grouped under a `📄 Root files` section header
- 15 management plans listed individually under `03_Plans/`
- 11 manager lanes listed under `10_Manager_Lanes/`
- Archive sections listed with `— Legacy content (reference only)` annotation
- Tip at bottom pointing to QUICK_LINKS.md and FILE_MANIFEST.md

## Patch Pitfall
The initial patch introduced a double-pipe `||` in the table row. Fixed with a second targeted patch. Root cause: the old_string included the trailing `|` from the table row, and the new_string also started with `|`, creating `||`. Always verify table row patches.
