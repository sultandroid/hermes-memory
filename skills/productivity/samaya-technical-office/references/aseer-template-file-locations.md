# Aseer Project Template File Locations

Canonical source paths for template files that should be copied to new BIM projects.
The Aseer project uses spaces in folder names; new projects use underscores.

## Report Templates (markdown + xlsx pairs)

| Template | Aseer Source Path | Dest Path Pattern |
|----------|------------------|-------------------|
| Weekly Progress Report | `Aseer-Museum/Docs/07_Reports/07.1 Progress Reports/_TEMPLATE_Weekly_Progress_Report.md` | `[PROJECT]/Docs/07_Reports/07.1_Progress_Reports/` |
| Weekly Progress Report (xlsx) | `Aseer-Museum/Docs/07_Reports/07.1 Progress Reports/_TEMPLATE_Weekly_Progress_Report.xlsx` | same |
| QA/QC Log | `Aseer-Museum/Docs/07_Reports/07.2 QA-QC Reports/_TEMPLATE_QAQC_Log.md` | `[PROJECT]/Docs/07_Reports/07.2_QAQC_Reports/` |
| QA/QC Log (xlsx) | `Aseer-Museum/Docs/07_Reports/07.2 QA-QC Reports/_TEMPLATE_QAQC_Log.xlsx` | same |
| Clash Report | `Aseer-Museum/Docs/07_Reports/07.3 Clash Reports/_TEMPLATE_Clash_Report.md` | `[PROJECT]/Docs/07_Reports/07.3_Clash_Reports/` |
| Clash Report (xlsx) | `Aseer-Museum/Docs/07_Reports/07.3 Clash Reports/_TEMPLATE_Clash_Report.xlsx` | same |

## Register Templates

| Template | Aseer Source Path |
|----------|------------------|
| Penetration Register | `Aseer-Museum/Docs/09_Registers/Penetration_Register/Structural_Penetration_Register_Template.xlsx` |
| Source Tree | `Aseer-Museum/Completed Tender Package From NRS/01_Registers_and_Logs/06_Source_Tree_Template.md` |

## Adaptation Steps After Copying

1. **In .md files:** Replace all references to Aseer Museum with the new project:
   - `مشروع متحف عسير الإقليمي` → new project Arabic name
   - `Aseer Regional Museum` → new project English name
   - `MOC-ASEER-SIC-` or `MOC-MUS-ASE-` → new project document prefix
   - Project-specific reference codes (DMP, BEP, etc.)

2. **In .xlsx files:** Open in Excel and update:
   - Title bar references to Aseer
   - Sheet tab names if they reference the old project
   - Header/footer text

3. **Don't over-adapt:** The structure, RAG colors, column layout, and bilingual format should remain identical — only the project-specific text changes.

## Aseer vs New Project Folder Name Difference

Aseer's `Docs/07_Reports/` uses **spaces** inside subfolder names:
```
07.1 Progress Reports/
07.2 QA-QC Reports/
07.3 Clash Reports/
```

New projects created by `project-initializer` use **underscores**:
```
07.1_Progress_Reports/
07.2_QAQC_Reports/
07.3_Clash_Reports/
```

Always reference the Aseer source with spaces (its actual on-disk name) and the new project dest with underscores (the initialized convention).
