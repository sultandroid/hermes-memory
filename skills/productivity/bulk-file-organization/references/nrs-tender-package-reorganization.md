# NRS Completed Tender Package Reorganization

**Project**: Aseer Museum (A2742) — Samaya BIM Unit  
**Date**: 2026-06-07  
**Scope**: `Completed Tender Package From NRS/` directory (19,168 files) + `05_Correspondence_Archive/` (13,544 files)

## Scope

The root directory had 8 numbered folders + 3 empty overlapping dirs. The `05_Correspondence_Archive/` had 157 loose files at root level mixed with 8 unnumbered subdirectories.

## What was done

### Spelling fixes (directory names)

| Before | After |
|--------|-------|
| `07_Visulizations Packages` | `07_Visualizations` |
| `Signal follow Digram` | `Signal_Follow_Diagram` |
| `AV Block Digram` | `AV_Block_Diagram` |
| `AV Schamatic & Rack Elevation` | `AV_Schematic_and_Rack_Elevation` |
| `Power Requierments` | `Power_Requirements` |
| `Stage 03 Appencices` | `Stage 03 Appendices` |
| `General Arrangment Drawing` | `General Arrangement Drawing` (2 occurrences) |
| `Deliveable no 02` | `Deliverable no 02` |
| `Free Standing Wall Types & Sitwork` | `Free Standing Wall Types & Setwork` |
| `Apendices` | `Appendices` |

### Spelling fixes (file names)

| Before | After |
|--------|-------|
| `Drawing Regester - NRS 27-4-26.xlsx` | `Drawing Register - NRS 27-4-26.xlsx` |
| `Drawing Regester - NRS.xlsx` | `Drawing Register - NRS.xlsx` |
| `Basment Floor.pdf` | `Basement Floor.pdf` |
| `*requierments*` (3 files) | `*requirements*` |
| `Aseer Regional Musuem*` | `Aseer Regional Museum*` |
| 22 files with double spaces | Normalized to single spaces |
| `New folder/` (90 Revit families) | `Setworks_RFA_Families/` |

### Organizational cleanup

- **Removed** 3 empty overlapping dirs: `Approval and Stamping`, `Latest Version (Drawing & Specs)`, `Submittals`
- **Deleted** 2 stub files (4-byte empty `(1)` duplicates)
- **Renumbered** all 20 subdirs in `05_Correspondence_Archive/` with 01-20 prefixes
- **Flattened** `13_RFIs_and_Submittals/RFI and Submittal/` → files up one level
- **Flattened** `19_REBA_Remarks/Latest/` → files up one level
- **Flattened** `Life_Safety_Drawings/Life_Safety_Drawings/` → removed double nesting

### 157 loose files → 12 categorized folders

New folders created at `05_Correspondence_Archive/`:

| Folder | Files | Content |
|--------|-------|---------|
| `01_Plans_and_Reports` | 15 | Weekly reports, design management, mobilization, stakeholder plans, IFC offers |
| `02_Correspondence_MOC` | 78 | All MOC-MUS-ASE / MOC-ASEER / MOC-Asser document transmittals, replies |
| `03_NCRs_and_SIs` | 4 | Non-conformance reports, site instructions |
| `04_Technical_Submittals` | 5 | CV packs, product compliance statements, evaluation criteria |
| `05_AV_and_BMS` | 6 | AV BTU calcs, BMS reports |
| `06_Drawings_and_DWG` | 21 | Floor plans, DWGs, layout PDFs |
| `07_Product_Datasheets` | 4 | TDS, Öko-Tex certificates, P083 drawings |
| `08_Model_and_Exhibition` | 8 | MVii model documents, bank details, licenses |
| `09_Spreadsheets_and_Logs` | 5 | Design & Drawing, MEP LOD, Clarification Sheet |
| `10_Contractual_and_Legal` | 2 | Arabic contracts (Al-Noor mosque, Samaya letter) |
| `11_Samaya_Internal` | 2 | Integrity/MEC MOM, technology notes |
| `12_Comments_and_Marks` | 6 | NRS comments on cases, ZNA scope, WhatsApp scans |

### Categorization rules used

Rules were prioritized Python lambdas matching on filename patterns:

```
name_contains(f, "weekly report", "mobilization", ...) → 01_Plans
name_matches(f, r'moc[-_]mus[-_]ase[-_]') → 02_Correspondence
name_contains(f, "ncr", "si-cg") → 03_NCRs
ext_in(f, '.dwg') → 06_Drawings
name_contains(f, "mvii", "model") → 08_Model
ext_in(f, '.xlsx') → 09_Spreadsheets
ext_in(f, '.eml') → 10_Contractual
```

See `SKILL.md` in this skill for the full helper function pattern.

### File register

Created `01_Registers_and_Logs/File_Register_Index.csv`:
- 19,166 entries (19168 - 2 stub deletions)
- Fields: Serial, Category, Subcategory, FilePath, FileName, Extension, Size_KB, Modified, Issues
- Remaining issues flagged: 9 files with `Asser` (external doc IDs), 5 `(1)` duplicates (genuine content differences)

## Cross-project file relocation (Pass 8)

After initial classification, 24 files from `05_Correspondence_Archive/` were identified as belonging to **other Samaya projects**. The first pass moved them to a `_Unrelated_Projects/` catch-all, but the user corrected this — files should go **directly to the target project's folder**.

### Files routed to other projects

| Category | Files | Destination | Reasoning |
|----------|-------|-------------|-----------|
| **MVii Madinah model** | 4 files (questions v1/v2, physical model boundary, 3mx3m boundary) | `El-Haramain Museum/Design Files/MVii_Models/` | Madinah model relates to Prophet's Mosque — El-Haramain = The Two Holy Mosques |
| **MVii company docs** | 6 files (bank details, business reg, license, REACH cert, drawing materials list) | `El-Haramain Museum/Docs/MVii_Models/` | Company docs support both mosque models, logically placed at El-Haramain |
| **MVii Makkah model** | 1 file (Makkah model boundary) | `Zamzam Museum/Design Files/` | Makkah model relates to Grand Mosque — Zamzam already has matching boundary file |
| **P083 drawings** | 2 files (Landscape Design, Architectural Final Design) | `Zamzam Museum/Design Files/` | P083 is Zamzam project code; duplicates already exist in Zamzam's Email_Archive |
| **TF2438 drawing** | 1 file | `Zamzam Museum/Docs/` | TF2438 already exists in Zamzam Museum |
| **Al-Noor Mosque contract** | 1 file (عقد مشروع مسجد النور) | `Masjid Alnoor/Contracts/` | Clear legal document for a different project |
| **Haram barriers report** | 1 file (TP-09-2512 حواجز و سواتر) | `El-Haramain Museum/Docs/` | About Grand Mosque + Prophet's Mosque barriers |

### Files that seemed off-project but actually belong to Aseer

| File | Clue they belong to Aseer |
|------|--------------------------|
| `M2742-1.00-004.pdf` | Same document series found in `Aseer-Museum/Contracts/02_NRS_Contract/01_Signed_Agreements/` as `M2742-1.00-003.pdf` |
| `A-02 - AS BUILT KING KHALED ROAD.pdf` | Aseer Museum is on King Khaled Road; same file exists in `Aseer-Museum/Design Files/Package_Part 1/02_Aseer Existing Building Information/MoC As Built Drawings/` |
| `MOC-Asser-SIC-*` (6 files) | An analysis note `MOC-ASSER-0PS-SH-006_Analysis.md` already exists in `Aseer-Museum/Docs/` — these are NRS documents with a consistent typo |

### How to discover cross-project files

For each candidate file found in `_Unrelated_Projects/` (or during classification):

```bash
# 1. Search for the same code in OTHER project folders
find "Samaya/Technical Office/Bim Unit" -type f -iname "*P083*" 2>/dev/null

# 2. Search the entire Samaya workspace for context
find "Samaya/" -type f -iname "*M2742*" 2>/dev/null

# 3. Check for matching As-Built / Design Files in the current project
# (King Khaled Road is an as-built for the Aseer Museum building location)
```

### Key discovery: project code ↔ project name mappings

| Code/Pattern | Project |
|-------------|---------|
| `A2742`, `MOC-MUS-ASE`, `MOC-ASEER` | Aseer Museum |
| `P083` | Zamzam Museum / Zamzam Visitor Center |
| `M2742-*` | Aseer Museum (NRS contract document series, not a different project) |
| `TF2438*` | Zamzam Museum |
| `MVii` Madinah references | El-Haramain Museum |
| `MVii` Makkah references | Zamzam Museum |
| King Khaled Road | Aseer Museum (museum address) |
| `مسجد النور` / Al-Noor | Masjid Alnoor project |
| Haram / Haramain references | El-Haramain Museum |

## Archive deduplication (`_ARCHIVE/04_Specifications_and_BOQ/`)

### Before
```
_ARCHIVE/04_Specifications_and_BOQ/
├── 02_Appendix_PDFs/              76 files
├── 03_Previous_Spec_Versions/     25 files
├── DIS_Registers/                  3 files
├── Old_Spec_Revisions/             6 files
├── SpaceNamed_Dupes/               2 files
```

### Merged structure

1. **Identified exact duplicates** within archive using MD5 hash
2. **Merged unique files** into `Version 00 - Earliest/`
3. **Moved DIS Registers** to live `01_Registers_and_Logs/` — sequential gap fill
4. **Renamed** `02_Appendix_PDFs` → `02_Old_Individual_Appendix_PDFs`

### After
```
_ARCHIVE/04_Specifications_and_BOQ/
├── 02_Old_Individual_Appendix_PDFs/  78 files
└── 03_Previous_Spec_Versions/        25 files (V00-V05)
```

## `04_Specifications_and_BOQ` cleanup

8 loose root files redistributed:
- 4 AV/BMS files → `05_Correspondence_Archive/05_AV_and_BMS/`
- 2 MOC documents → `05_Correspondence_Archive/02_Correspondence_MOC/`
- 2 P083 drawings → `Zamzam Museum/Design Files/`

Folder `03_Sketch_Sheets` → `03_Stage3_Clash_Review_Stairs_Ramps` (user corrected: files were clash reviews, not sketches)

## Items intentionally NOT changed

- 9 files with `Asser` in filename (MOC-Asser-SIC-*) — these are official NRS document IDs and must be preserved
- 5 files with `(1)` suffix — confirmed to have different content than originals
- `Deliverables to NRS/0-References/` — the `0-` prefix is from the sender and kept as-is
- Vendor AV package subdirectory spaces — `Audio Visual System _Shop Drawings set/`, `RCP PLAN/`, `FLOOR PLAN/` — vendor content
- `Version 01/02/03` version dirs — semantic labels, spaces preserved
