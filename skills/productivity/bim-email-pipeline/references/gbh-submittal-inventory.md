# GBH (Glasbau Hahn) Submittal Inventory — Aseer Museum

Complete inventory of all showcase submittals from GBH, cross-referenced from email archives, BIM folder structure, and submittal register logs.

## Canonical Location

All GBH submittals consolidated under:
```
Subcontractors/02_Showcases_Contractor/05_Returned_Submittals/
```

## Complete Table

| # | Date | Types | BIM Location | Status |
|---|------|-------|-------------|--------|
| 01 | 1-Apr | Type 4 (Freestanding), Type 6a | `2026-04-01_Submittal_01/` — 18 files | ✅ In BIM |
| 02 | 7-Apr | Type 4 (revised) | `2026-04-07_Submittal_02/` — 1 .7z (11 files) | ✅ Recovered from attachments |
| 03 | 8-Apr | Type 1 (Wall Case), Type 5a | `2026-04-08_Submittal_03/` — 1 .7z (13 files) | ✅ In BIM |
| 04 | 14-Apr | Type 3, 5a, 6a, Type 1 | `2026-04-14_Submittal_04/` — 9 files | ✅ In BIM |
| 05 | — | — | **Never existed** — skipped by GBH | ❌ |
| 06 | — | — | **Never existed** — skipped by GBH | ❌ |
| 07 | 21-Apr | Type 2 | `2026-04-21_Submittal_07/` — 1 .7z (11 files) | ✅ In BIM |
| 08 | 22-Apr | Type 6b | `2026-04-22_Submittal_08/` — 2 files | ✅ In BIM |
| 09 | 2-May | Type 6b | `2026-05-02_Submittal_09/` — 2 files | ✅ In BIM |
| 10 | 20-May | Type 1, 2, 5a, 6b | `2026-05-20_Submittal_10_NRS_Comments/` — 11 files NRS-stamped | ✅ In BIM |
| 11 | 25-May | Type 1, 2 | `2026-05-27_Submittal_11_NRS_Comments/` — 6 files NRS-stamped + .7z + DWG | ✅ In BIM |

## Cross-Reference Method

When reconstructing a vendor submittal sequence, cross-reference THREE sources:
1. **Email archives** — grep "Submittal N" in all weekly .md files
2. **BIM folder** — search `*submittal*N*` across multiple locations
3. **Submittal register logs** — xlsx in `Docs/09_Registers/Submittal_Tracker_IFC_Log/`

If no trace after exhaustive search, record as "never existed" not "missing".

## Consolidation Pattern

GBH .7z files were scattered across 3 locations before consolidation:
- `Docs/03_Submittals/03.7_Submittal_Packages/` (03, 04, 07, 08)
- `Completed Tender Package From NRS/Submittals/` (04)
- `Subcontractors/02_Showcases_Contractor/05_Returned_Submittals/` (08, 09, 10, 11)

Submittal 02 recovered from `attachments/correspondence/Submittal 02 04-07-2026.7z` (was in email pipeline but never filed to BIM).

Submittals 01, 04 had loose NRS-commented PDFs in the root of `05_Returned_Submittals/` that were moved into their respective numbered folders.

Duplicate .7z files existed for Submittal 04 (3 copies across different folders, identical MD5 hash) — deduplicated to one copy.

Final canonical location: all 11 submittals under `Subcontractors/02_Showcases_Contractor/05_Returned_Submittals/` with date-prefixed subfolder names.

## GBH Kickoff

First GBH meeting: **March 10, 2026** (per week 11 email archive).
