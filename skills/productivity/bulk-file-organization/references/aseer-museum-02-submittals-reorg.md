# Aseer Museum 02_Submittals Reorganization

**Date**: 2026-06-28  
**Scope**: 6.4M, 25 root items → 10, all register files consolidated

## Before

Root had 25 items: 11 folders + 14 files scattered.

```
02_Submittals/
├── 01_Shop Drawings/           ✓ numbered
├── 02_Material Samples/        ✓ numbered
├── 03_DD Documents/            ✓ numbered
├── 13 Submittal Register folders/   ✗ scattered at root
├── 19 .py scripts + 4 .xlsx     ✗ loose at root (register code + data)
├── Architecture/                ✗ orphan — belongs in 03_DD/
├── AV Packages/                 ✗ orphan — belongs in 01_Shop/
├── IFC_Packages/               ✗ unnumbered — sibling to numbered dirs
├── 26Jun2026_Batch/            ✓ batch delivery (good naming)
├── 8-6-26/                     ✗ ambiguous date format
├── A2742_5.05_DIS_024.pdf      ✗ loose PDF
├── nissenrichardsstudio_.../   ✗ 6,766 auto-extracted files at root
├── Design_Schedule_Programme.py/.xlsx  ✓ project-level tools — keep
└── 2Week_Look_Ahead.py         ✓ project-level tool — keep
```

## Phase 1 — Restructure (25 → 10 root items)

**Approved plan, single bash script with `set -e`.**

All register folders + their .py/.xlsx files → `04_Registers/`
Architecture/ → `03_DD Documents/Architecture/`
AV Packages/ → `01_Shop Drawings/AV Packages/`
IFC_Packages/ → `06_IFC_Packages/` (numbered sequence)
8-6-26/ → `05_Batch_Deliveries/2026-08-06/`
26Jun2026_Batch/ → `05_Batch_Deliveries/26Jun2026_Batch/`
nissenrichardsstudio_.../ + loose PDF → `07_Drawing_Source_Folders/`
Design_Schedule_Programme.*, 2Week_Look_Ahead.py → kept at root (project-wide tools, not per-discipline scripts)

## Phase 2 — Scripts → Subfolder (31 → 18 + scripts/)

Within `04_Registers/`, the 19 .py scripts were cluttering the folder alongside the 12 register folders and standalone .xlsx files. Moved ALL `.py` files into `04_Registers/scripts/`:

```
04_Registers/
├── scripts/                              ← 16 .py generator scripts
│   ├── Acoustic_Submittal_Register.py
│   ├── AV_Submittal_Register.py
│   ├── ...
│   └── Structural_Submittal_Register.py
├── Acoustic_Submittal_Register/          (folder with .xlsx)
├── AV_Submittal_Register.xlsx            (standalone xlsx)
├── CITC_Telecom_Submittal_Register/
├── ...
└── Structural_Submittal_Register/
```

## Outcome

```
02_Submittals/                   25→10 items
├── 01_Shop Drawings/            +AV Packages/
├── 02_Material Samples/         (unchanged)
├── 03_DD Documents/             +Architecture/
├── 04_Registers/                18 items (folders+xlsx) + scripts/ subfolder
├── 05_Batch_Deliveries/         2 batch folders (2026-08-06, 26Jun2026)
├── 06_IFC_Packages/             (renamed)
├── 07_Drawing_Source_Folders/   extracted packages + loose PDF
├── Design_Schedule_Programme.py/.xlsx
└── 2Week_Look_Ahead.py
```

## Key Decisions

- **Project tools kept at root**: `Design_Schedule_Programme.*` and `2Week_Look_Ahead.py` are not per-discipline registers — they're cross-cutting scheduling scripts. They stay at root to signal their project-wide role.
- **nissenrichardsstudio_ folder → 07_Drawing_Source_Folders**: 6,676 extracted drawing files. Belongs in its own numbered folder, not inside Batch_Deliveries (it's a drawing source package, not a batch delivery).
- **8-6-26 → 2026-08-06**: Ambiguous DD-MM-YY renamed to ISO 8601 for sortability. Parent changed to 05_Batch_Deliveries. Done in one `mv` command: `mv "8-6-26" "05_Batch_Deliveries/2026-08-06"`.
- **No dedup performed**: The loose `A2742_5.05_DIS_024.pdf` may duplicate content in both the batch folder and the extracted drawing folder. Left for manual review — content dedup requires hash comparison and was out of scope.
- **Scripts in subfolder**: .py files separated from .xlsx data files to reduce visual clutter and keep the register folder navigable. Only the human-readable register files (folders + xlsx) stay at top level; generator scripts go into `scripts/`.
