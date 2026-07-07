# NRS Submittal Cycle — Aseer Museum (A2742)

## Overview

The Aseer Museum project uses NRS (Nissen Richards Studio) as design reviewer for subcontractor shop drawings before CG (Consultancy Group) review. Each submittal cycle follows a 3-stage pattern.

## Submittal Structure

```
05_Returned_Submittals/
├── YYYY-MM-DD_Submittal NN_MM-DD-YYYY.7z        ← Source (un-stamped, from subcontractor)
├── YYYY-MM-DD_Submittal_NN_Extracted/             ← Extracted source files
│   └── Submittal NN MM-DD-YYYY/
│       ├── *.dwg (CAD source)
│       ├── *.pdf (un-stamped shop drawings)
│       └── plot.log, logo files, title blocks
└── YYYY-MM-DD_Submittal_NN_NRS_Comments/          ← Stamped versions (AFTER NRS review)
    ├── README.md                                   ← Document batch contents, stamp date, notes
    ├── *NRS_Comments_YYMMDD_stamped.pdf            ← NRS-reviewed shop drawings
    └── *reference.png/pdf                          ← Reference drawings from NRS
```

## Location

`Bim Unit/Aseer-Museum/Subcontractors/02_Showcases_Contractor/05_Returned_Submittals/`

For GBH (Glasbau Hahn) showcases specifically.

## Naming Convention

| Artifact | Pattern | Example |
|----------|---------|---------|
| Source archive | `YYYY-MM-DD_Submittal NN_MM-DD-YYYY.7z` | `2026-05-25_Submittal 11 05-25-2026.7z` |
| Extracted folder | `YYYY-MM-DD_Submittal_NN_Extracted/` | `2026-05-25_Submittal_11_Extracted/` |
| NRS comments | `YYYY-MM-DD_Submittal_NN_NRS_Comments/` | `2026-05-27_Submittal_11_NRS_Comments/` |

Note: The stamp date (in filename `260527`) may differ from the submission date (folder `05-25-2026`). Use the NRS stamp date for the NRS Comments folder name.

## When Organizing Submittals

1. Check if source `.7z` already exists in the destination before re-archiving
2. Move NRS-stamped PDFs into `YYYY-MM-DD_Submittal_NN_NRS_Comments/`
3. Create `README.md` following Submittal 10/11 pattern
4. Update `PROJECT_MEMORY.md` with session update section
5. Clean up Downloads → Trash
6. Do NOT re-upload to Odoo — submittal register lives on Aconex CDE

## Example Files (Submittal 11)

- `Freestanding Case-Type 2- ID.Nr. 08.03_SC_01_NRS_Comments_260527_stamped.pdf`
- `Wall Case-Type 1- ID.Nr. 12.05_SC_01_NRS_Comments_260527_stamped.pdf`
- `Wall Case-Type 1- ID.Nr. 12.06_SC_01_NRS_Comments_260527_stamped.pdf`
- `Wall Case-Type 1- ID.Nr. 12.06_SC_02_NRS_Comments_260527_stamped.pdf`
- `A2742_Type_6b_1500mm_BackPanels.png` (reference from NRS)

## Project Context

- **Project**: Aseer Regional Museum (متاحف عسير)
- **Job**: A2742 (NRS reference)
- **Client**: Ministry of Culture (MOC) — Regional Museum Program
- **Main Contractor**: Samaya Investment
- **Designer**: Nissen Richards Studio (NRS), London
- **Showcase Subcontractor**: Glasbau Hahn (GBH)
- **Contract**: Design-Build (EPC), No. 0010003521
- **Current Stage**: RIBA 4 / LOD 400
- **PROJECT_MEMORY.md**: At `Bim Unit/Aseer-Museum/PROJECT_MEMORY.md` — always update after handling submittals
