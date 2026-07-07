# File Handling Rules for Samaya Technical Office

## Golden Rule

**ALL file references in Odoo task descriptions, emails, and communications must point to project folders under OneDrive-SAMAYAINVESTMENT. NEVER reference /tmp or other temp directories.**

## Workflow

1. Extract attachment from Outlook to `/tmp/<context>/` for processing
2. Read/parse the file (pdftotext, openpyxl, etc.)
3. Determine the correct project subfolder
4. Copy the file to the project folder
5. Reference ONLY the project-relative path in any Odoo task or communication

## Project Root Paths

| Context | Root |
|---------|------|
| Aseer Museum BIM | `Samaya/Technical Office/Bim Unit/Aseer-Museum/` |
| General Correspondence | `.../09_Correspondence/` |
| NCRs / Formal Documents | `.../09_Correspondence/<doc-code>.pdf` |
| Submittals | `.../02_Submittals/` |
| Plans & Procedures | `.../10_Plans/` |
| Subcontractor docs | `.../Subcontractors/` |

## Why

- /tmp is ephemeral — files are lost on reboot
- Project folders are shared via OneDrive with the team
- The user navigates project folders, not /tmp
