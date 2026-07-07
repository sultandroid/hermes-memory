# Tender Package Organization

When the user asks to create a tender (مناقصة) package subfolder for a project, the correct approach is to **copy existing project files** — never generate new documents (BOQ, SOW, conditions, etc.) from scratch.

## Golden Rule: Copy, Don't Generate

The user's project already has all the documents it needs. A tender package is a **curated subset** of existing files, organized for external distribution. Generating new documents creates confusion and duplicates.

## Pre-work: Survey the Full Project

Before organizing, read the root project folder structure:

```bash
find "$PROJECT_ROOT" -maxdepth 1 -not -name ".*" | sort
```

Then check each subfolder's contents at depth 2-3. This reveals:
- What documents exist (BOQ, specs, drawings, submittals)
- What's empty (Contracts, Invoices, Reports — flag these as gaps)
- What the project scope actually is (from BOQ items, email subjects, drawing titles)

## Tender Package Folder Structure

```
Tinder Doc/                    # (named as user specified)
├── 01_BOQ/
│   └── Items Status.xlsx      # Copy from B.O.Q/ — keep only one, remove "Talha-PC" duplicates
├── 02_Drawings/
│   ├── 01_Shop_Drawings_PDF/  # All PDFs from Revit Files/Detail Drawings/ + Revit Files/Pdf/
│   ├── 02_CAD_Source/         # All DWGs from Revit Files/Cad/ + Detail Drawings/
│   ├── 03_Revit_Model/        # RVT from Revit Files/Rvt/ (latest version)
│   ├── 04_3D_Renders/         # Scene renders from Design Files/NEW/
│   ├── 05_Reference_Images/   # PNGs, JPGs from Detail Drawings (reference only)
│   └── 06_Plot_Config/        # PCP plot config files
├── 03_Specifications/
│   ├── Division 00-46.pdf     # PDFs only — delete DOCX duplicates
│   └── Division 27 COMMUNICATIONS/
└── 04_Submittals/
    ├── 01_Architectural/      # Full copy from Submittal's/Arch/
    ├── 02_Structural/         # (may be empty)
    └── 03_MEP/               # (may be empty)
```

## What NOT to Include

| Item | Reason |
|------|--------|
| Cost estimate PDFs | Separate from tender — user explicitly removes these |
| DOCX specs | Duplicate of PDFs — keep only PDF |
| "Talha-PC" suffixed files | Duplicate of main file — keep the cleaner one |
| Revit backup versions (.0001-.0006) | Only the latest .rvt |
| Email archives | Internal correspondence, not for tender |
| Design Files/OLD/ | Old reference photos, not for tender |
| Clash reports, NWC/NWD | Construction-phase docs, not tender |

## Pitfalls

- **Always copy, never move** — the original project structure must remain intact. Use `cp -R` for folders, `cp` for files.
- **Verify submittals copy is complete** — `cp -R` can silently fail on OneDrive. After copy, count files in destination and compare to source.
- **Flatten double-nested folders** — `cp -R Submittal's/ Tinder Doc/04_Submittals/` creates `04_Submittals/Submittal's/Arch/...`. Fix with `mv` + `rmdir`.
- **User may call it "Tinder" not "Tender"** — confirm before acting, but use their spelling for the folder name.
- **Empty folders are fine** — `Mep/` and `Struc/` may be empty in source; keep them in the structure for completeness.
- **Numbered subfolder names** — use `01_`, `02_` prefixes for ordering. Within drawings, use `01_Shop_Drawings_PDF`, `02_CAD_Source`, etc.
