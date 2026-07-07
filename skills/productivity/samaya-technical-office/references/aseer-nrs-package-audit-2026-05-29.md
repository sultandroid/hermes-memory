# Aseer Museum — NRS Tender Package Receipt Audit (29 May 2026)

**Package location:** `OneDrive-SAMAYAINVESTMENT/Samaya/Technical Office/Bim Unit/Aseer-Museum/Completed Tender Package From NRS/`

**Drawing Register:** `Drawing Regester - NRS 27-4-26.xlsx` (in 01_Registers_and_Logs)
**Register version also on file:** `A2742_5.05_DIS_021.pdf` (issued 24 May 2026)

**Pre-existing audit tree:** `Aseer_Drawing_Status_Tree.txt` — Register DIS-021 baseline, generated 2026-05-26

---

## Baseline Status (from existing tree)

| Status | Count |
|--------|-------|
| [OK] Stamped | 162 |
| [>>] Pending (unstamped) | 69 |
| [XX] Missing | 12 |
| **Total** | **243** |

## 12 Missing Drawings

All in 1100-series (Existing/Demolition) and 1350/1500 (Sections) — likely never received from NRS:

- A2742-1100 through 1104 — Existing floor plans GA
- A2742-1150 through 1154 — Existing floor plans Demolition
- A2742-1350 — Existing Longitudinal Section GA
- A2742-1500 — Proposed Longitudinal Section GA

## Duplicate CAD Source Files Detected

Every .dwg exists in **3+ copies** across:
1. `02_Approved_Stamped_Packages/*/02_CAD_Source/`
2. `06_Drawing_Source_Folders/`
3. `05_Correspondence_Archive/Deliverables to NRS/`
4. `03_Incoming_For_Review/Previous_and_Raw_Packages/`

Worst offenders (8 copies each): A2742-1250A through -1253A.dwg (ceiling finishes)

## Structural Issues Found

| Issue | Details |
|-------|---------|
| Underscore folder | `03_Incoming_For_Review/_/` has ALL content; sibling folders empty |
| Wrong discipline | A2742-1230..1233 (floor finishes) in `1250_Ceiling_Details/` |
| Overlap | `08_Stairs_Details_Stamped` duplicates `01/1550_Stairs_Details` |
| .bak files | Mixed into stamped PDF folders under `From_Design_Files/` |
| Typo folder | `1700_Setworks_and_Partitions` vs `1700_Setworks_Partitions` |
| Empty folder | `02_Approved_Stamped_Packages/00_Tracking_Logs` |
| Root-level reports | Audit HTML/TXT/MD reports at root, should be in 01_Registers_and_Logs/ |

## Folder Structure (Final — 29 May 2026, Post-Reorganization)

```
Completed Tender Package From NRS/
├── 01_Registers_and_Logs/         ← Drawing registers + 5 audit reports
├── 02_Approved_Stamped_Packages/  ← Stamped PDFs ONLY (zero CAD files)
│   ├── 01_Architectural_Stamped/  (1200_GA, 1550_Stairs, 1600_Washrooms, 1700_Setworks)
│   ├── 02_Finish_and_Flooring_Stamped/
│   ├── 03_Showcases_Stamped/
│   ├── 04_Life_Safety_Stamped/
│   └── 05_Systems_and_MEP_Stamped/
├── 04_Specifications_and_BOQ/
│   ├── 01_Approved_Specs_NRS/
│   ├── 02_Appendix_PDFs/         ← K/M series, DIS_003/005/006 moved here
│   ├── 03_Previous_Spec_Versions/
│   ├── Appendices/
│   └── Mep Requirements/
├── 05_Correspondence_Archive/     ← ALL unsorted, raw, archival content
│   ├── 03_RFIs_and_Submittals/
│   ├── 05_Previous_and_Raw_Packages/
│   │   ├── 01_NRS_Stage04_Package/
│   │   ├── 03_NRS_Ceiling_CAD_14Apr2026/
│   │   └── 05_Arch_Extraction_Old_Revisions/
│   ├── Deliverables to NRS/
│   ├── Incoming_Drawings_Archive/        ← from former 03/_/01_Raw_Incoming_Drawings
│   ├── Incoming_Registers/               ← Drawing Register versions
│   ├── Incoming_Specs_and_Reports/       ← AV Package, Life Safety, specs versions
│   ├── REBA_Remarks/                     ← REBA comments
│   └── Unstamped_and_Old_Revisions/
│       └── 1700_Setworks_and_Partitions_archive/
├── 06_Drawing_Source_Folders/     ← SINGLE source for ALL unique drawings (609 DWGs + PDFs)
│   ├── 00_Stamped_CAD_Source/     ← CAD from approved stamped package (10 discipline subdirs)
│   ├── 1100_Existing_and_Demolition/  (5 drawing folders)
│   ├── 1200_General_Arrangement/     (8 drawing folders)
│   ├── 1230_Floor_Finishes/          (8 drawing folders — includes A-suffix)
│   ├── 1250_Ceiling_Details/         (13 drawing folders — includes versions)
│   ├── 1510_Internal_Elevations/     (empty, ready)
│   ├── 1570_External_Details/        (empty, ready)
│   ├── 1600_Washrooms_VIP/           (4 drawing folders)
│   ├── 1700_Setworks_Partitions/     (95 drawing folders — largest)
│   ├── 1800_Showcases/               (18 drawing folders)
│   ├── 1850_Graphics_Housing/        (empty, ready)
│   ├── 1860_Graphics_Housing/        (15 drawing folders)
│   ├── 1890_Painted_Finishes/        (empty, ready)
│   ├── 1900_Finishing_and_Flooring/  (34 drawing folders)
│   ├── 1920_Wall_Type_Details/       (4 drawing folders)
│   ├── 1930_Doors_Lifts/             (empty, ready)
│   └── 1950_Door_Types/              (empty, ready)
└── FOLDER_AUDIT_AND_REORG_REPORT.md
```

## Changes Executed (29 May 2026 — Full Reorganization)

1. Moved 5 root-level audit reports to 01_Registers_and_Logs/
2. Deleted 12 .bak files from 02_Approved_Stamped_Packages/*/From_Design_Files/
3. Removed duplicate 08_Stairs_Details_Stamped (already in 01/1550)
4. Archived typo folder 1700_Setworks_and_Partitions → Unstamped_and_Old_Revisions/
5. Fixed discipline placements:
   - Created 1100_Existing_and_Demolition, moved 1160-1164 from 1200_GA
   - Created 1230_Floor_Finishes, moved 1230-1233 from 1250_Ceiling_Details
6. Renamed _/ to 01_Raw_Incoming_Drawings (before elimination)
7. Removed 00_Tracking_Logs loose file from stamped packages
8. Deleted .DS_Store across all folders
9. **Consolidated ALL CAD from 02_Stamped into 06_Source** — 149 DWG files moved from 5 stamped disciplines to 06_Source/00_Stamped_CAD_Source/
10. **Eliminated 03_Incoming_For_Review** — distributed all content:
    - Raw drawings → 06_Source/ proper discipline folders
    - AV Package → 05_Archive/Incoming_Specs_and_Reports/
    - Life Safety → 05_Archive/Incoming_Specs_and_Reports/
    - Appendix PDFs (84 files) → 04_Specs/02_Appendix_PDFs/
    - REBA remarks → 05_Archive/REBA_Remarks/
    - Previous packages → 05_Archive/05_Previous_and_Raw_Packages/
    - Incoming registers → 05_Archive/Incoming_Registers/
    - RFIs/Submittals → 05_Archive/03_RFIs_and_Submittals/
11. **Cleaned up 04_Stage04_Design_Files** (messy dumping ground):
    - Compared 549 DWG/PDF files against 06_Source (241 baselines)
    - Found 155 unique files not in 06_Source
    - Moved Appendix PDFs to 04_Specifications_and_BOQ/02_Appendix_PDFs/
    - Moved AV & Life Safety to 05_Archive/Incoming_Specs_and_Reports/
    - Moved REBA Notes to 05_Archive/REBA_Remarks/
    - Deleted all NRS auto-download folders (~6,500 duplicate CAD files)
12. **Fixed stray folders** at 06_Source root → into proper discipline folders
13. **Pre-created empty discipline folders** in 06_Source: 1510, 1570, 1600, 1850, 1890, 1930, 1950

### Remaining (User Action Needed)
- **12 missing drawings** — need NRS resubmission (all 1100/1150/1350/1500 series)
- **69 pending drawings** — received, awaiting stamp
- **AV Package** — Samaya consultant docs in 05_Archive, not yet integrated
- **Life Safety drawings** — in 05_Archive, not yet in 06_Source

## Recovery Audit — 06_Source vs DIS_021 (Final)

After reorganizing and recovering drawings from archives, an additional ~66 drawings were brought into 06_Source through systematic search across all archive folders.

### Drawings Recovered from Archives

| Source | Count | Drawings |
|--------|-------|----------|
| Incoming_Drawings_Archive/1500_General_Details/ | 26 | All Internal Elevations (1510-1537) |
| Unstamped_and_Old_Revisions/ | 14 | 1220-1223 (Wall Finishes), 1728-1729 (Display Panels), 1769, 1794, 1799, 1920, 1922-1923, 1940-1945 |
| Incoming_Drawings_Archive/1200_GA/ | 1 | A2742-1204 (Second Floor GA) |
| Incoming_Drawings_Archive/1700/ + Setwork/ | 4 | 1721-1722 (Floral Crown), 1769, 1799 |
| 00_Stamped_CAD_Source/ (extracted) | 13 | Stairs CAD (1550-1559), Showcase Schedule (1820), Painted Finishes (1890) |
| **Total recovered** | **~66** | |

### Still Truly Missing (18 drawings — need NRS to provide)

**12 [XX] Missing — never received:**
- A2742-1100 to 1104 (Existing Basement through Second Floor Plans — GA)
- A2742-1150 to 1154 (Existing Basement through Second Floor Plans — Demolition)
- A2742-1350 (Existing Longitudinal Section — GA)
- A2742-1500 (Proposed Longitudinal Section — GA)

**5 [>>] Pending — never received final versions:**
- A2742-1570 to 1574 (External Details — Fixed Benches)

**1 [>>] Pending — only stamped PDF exists, no CAD:**
- A2742-1711 (Counter for Manual Interactive, G4 Saudi Art Gallery)

### Final Coverage
- **Present in 06_Source:** 225 of 243 drawings (92.6%)
- **Truly missing from NRS:** 18 (7.4%)
- 06_Source contains 609 DWG files + hundreds of PDFs across 12 active discipline folders
- The 00_Stamped_CAD_Source/ folder holds 149 DWG files from the approved stamped package as insurance against any version discrepancies