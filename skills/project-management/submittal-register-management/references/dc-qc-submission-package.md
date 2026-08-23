# DC/QC Submission Package — Standard Structure

When a user sends new submittal files (models, drawings, reports) and asks to "add to the
submission folder with registers, QC/QA check, best practice as DC and QC engineer", build a
**self-contained submission package** rather than scattering files loose in the submittal root.

## Package layout

```
<NN>- <Submission Name> <YYYY-MM-DD>/
├── 00_Transmittal/   Transmittal_<name>_<date>.xlsx   (formal TRX, sign-off block)
├── 01_<Content>/     the actual deliverables (e.g. ETABS_Model/, AsBuilt_Drawings/)
├── 02_<Content>/     second content group if needed
├── 03_QC_Checklist/  Submission_QC_Checklist_<name>_<date>.xlsx
├── 04_Registers/     Submission_Register_<name>_<date>.xlsx  (package snapshot)
└── README.md         index + purpose + QC gate note
```

Number the content folders 01, 02, ... in the order they appear on the transmittal.

## Transmittal (00_Transmittal/)
- Title row (navy `#1F3864` fill, white bold) + project/contract line.
- Info block: Transmittal No. (TRX-OUT-####), Date, From (Samaya Investment — Technical Office),
  To (CG), Cc (PMC / NRS), Project, Subject, Submission Stage.
- Documents table: `# | Document Ref | Description | Format | Qty | Remarks`.
- Sign-off block: Prepared by (Designer) / Checked by (Discipline Lead) / Tech Office Reviewer (Release).

## Master transmittal register
Log the new TRX into the project's master register
(`04_Docs/09_Registers/30_Transmittal_Register/Aseer_Museum_Transmittal_Register.xlsx`,
sheet "Transmittal Register", columns TRX ID | Date | Direction | From | To | Cc | Subject |
Document Refs | Type | Aconex Ref | Action Required | Response Due | Status | Comments).
- Action Required: "Review (14-day deemed approval per ER 2.4.A)".
- Status: "Issued".
- Append at `ws.max_row + 1` (the register may be header-only / empty — don't assume rows exist).

## Submission register (04_Registers/)
Package-specific snapshot: `# | Register Ref | Document Ref | Description | Format | Qty |
Status | Response Code | Response Date | Remarks`. Status = Submitted; Response Code left blank
to fill on CG reply. Add a note row linking the package to the parent register items it supports
(e.g. ETABS model supports ASE-STR-REV-001 / ASE-STR-MDL-004).

## QC checklist (03_QC_Checklist/)
- Copy the project's `Submission_QC_Checklist.xlsx` template, rename for the package.
- Fill the **Cover** sheet only (Document, Applies to, Revision). Do NOT tick Done/Pass boxes or
  fill sign-off names — that is the user's internal QA gate ("NO sign-off = NO submission").
- The template's Done column ships as boolean `False` in General format, which renders as the
  word FALSE, not a checkbox. If the user wants checkboxes, convert to `☐`/`☑` text glyphs
  (openpyxl cannot create native form controls). Center-align the glyph cells.

## README.md
Index table (folder → contents → register ref), purpose, QC gate reminder, status line.

## Pitfalls
- **Don't scatter files loose in the submittal root** — the user explicitly asked for a
  self-contained package. If earlier steps left loose copies, offer to remove them.
- **Don't fabricate sign-offs or tick QC items** — leave the QA gate to the user.
- **Verify every generated xlsx opens** (`openpyxl.load_workbook`) before reporting done.
- **OneDrive-safe**: `cp` into the package, never `mv`/`rm -rf` (corrupts sync).
