# Aseer Museum 09_Registers Reorganization (2026-06-07)

## Context

The `09_Registers` folder under `Aseer-Museum/Docs/` had ~206 files with ~30 loose files at root, naming inconsistencies, corrupt stubs, and two `_archive` hierarchies. The folder tracks project registers (drawing, AV, procurement, risk, subcontractors, etc.) across ~20 subdirectories.

## Issues found

| Category | Count | Examples |
|----------|-------|----------|
| Loose files at root | 29 | AV spreadsheets, CV packs, drawing PDFs mixed at same level |
| Naming typos | 7 | `Regester` → `Register`, `BIm` → `BIM`, `Asher` → `Aseer`, `ASEER` → `Aseer` |
| Corrupt stubs (4 bytes) | 2 | Shop Drawings Log PDF, MEP LOD xlsx |
| Directory case | 1 | `BIm Team` → `BIM Team` |
| Cloud sync markers | 16 | `.dc_purpose` files in 16 subdirectories — preserved |
| .DS_Store | 3 | Removed |

## Operation sequence

1. **Inventory** — `find`, `du -sh`, cross-reference against subfolder structure
2. **Propose plan** — markdown table with 8 action items, sent for user approval
3. **Move AV files** (6) → `AV_Interface_Register/`
4. **Move drawing files** (9) → `Drawing_Register/`
5. **Move CV submission packs** (4) → `Key_Personnel_Register/CVs/{team}/`
6. **Move master logs** (4) → `Master_Register_Index/`
7. **Relocate email** (1) → `Key_Personnel_Register/`
8. **Rename** for consistency — 7 file/directory renames
9. **Remove .DS_Store** — 3 files, deleted
10. **Verify** — root has 0 loose files (only `.dc_purpose`)

## What to preserve

- `.dc_purpose` files are Dropbox/OneDrive sync markers — leave in place
- External document IDs (`MOC-ASEER-SIC-*`, `MOC-MUS-ASE-*`) retain their original document numbers even when inconsistent — only rename after confirming with user
- Empty subdirectories (`SG Group/`, `Specialist/` subdirs with 0B in `du`) noted but left in place

## Key user preference

User accepted all proposed moves and renames in a single approval. No corrections. The "propose plan as table → confirm → execute" pattern was effective for this class of work.
