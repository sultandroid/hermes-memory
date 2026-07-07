---
name: bim-submittal-register
category: project-management
description: Build BIM submittal registers and submission plans from project data (MIDP, TIDP, SOW, existing registers) using a standardized 13-column template.
triggers:
  - "build submittal plan for [discipline]"
  - "create submission register for [discipline]"
  - "review submittal register format"
  - "fix approval authority in submittal plan"
  - "extract deliverables from MIDP/TIDP"
---

# BIM Submittal Register & Submission Plan

## Workflow

### 1. Understand the Template (AV format)
The standard template has **13 columns**:
| Col | Header | Notes |
|---|---|---|
| A | Gate | e.g. "Detailed Design", "Coordinated IFC" |
| B | Level / Zone | Floor or system zone |
| C | Discipline | e.g. FLS, Electrical, Mechanical |
| D | Submission Category | Detailed Design, BIM, Material & Samples, Coordinated IFC |
| E | Drawing Package / Item | Unique reference code |
| F | Submission Description | Full description of deliverable |
| G | Responsibility | Who prepares it |
| H | Planned Submission Date | DD/MM/YYYY format |
| I | Review Duration (Days) | 3 days (design), 14 days (IFC) |
| J | Approval Authority | **Always CG** |
| K | Linked Activity ID | Program activity reference |
| L | Status | Planned / In Progress / Pending |
| M | Remarks | Notes, dependencies, clarifications |

### 2. Gather Source Data
- **MIDP** (Master Information Delivery Plan) — high-level deliverables per phase
- **TIDP** (Task Information Delivery Plan) — detailed task breakdown per discipline
- **SOW** (Scope of Work) — contractual deliverables
- **Existing registers** — subcontractor drawing lists, equipment schedules
- **CG review comments** — PDFs with approval conditions

### 3. Build the Plan
- Copy the AV template as base (formatting, merged cells, column widths)
- Set **Approval Authority = CG** as the **default in the generation script** — not as a post-fix
- Use 3 gates:
  - **Gate 1 — Detailed Design**: Strategy, design reports, calculations, drawings, BIM models
  - **Gate 2 — Material Approval**: Material submittals register, equipment submittals (leave empty if none)
  - **Gate 3 — Coordinated IFC**: Per-floor IFC packages, specs, BIM LOD 500, ITP, O&M, training, spares
- Review duration: 3 days for design items, 14 days for IFC packages

### 4. Verify After Generation
- **Re-read the saved file** to confirm changes persisted
- Check all Approval Authority cells = CG
- Check all IFC rows have Responsibility, Dates, Review Duration filled
- Check sheet name ≤ 31 characters (Excel limit)
- Check date format is consistent (DD/MM/YYYY)
- Check no duplicate drawing references per floor
- Check multi-discipline files are split into separate files

## User Preferences (Aseer Museum Project)
- **Approval Authority**: Always CG for all items
- **Responsibility**: Replace "Consultant" with "MEP Designer Office" per CG comment #8
- **Discipline discussion**: One at a time, not batch-build all
- **Status**: Use "Planned" as default for new items
- **Language**: English only
- **SOW Alignment**: When building plans from a Program/SOW, cross-reference against the latest CG Responses to ensure all mandated engineering scopes (e.g., Lighting Control, Conservation studies) are explicitly included, even if not listed as separate activities in the Gantt chart.
- **Program Synchronization**: Always compare "Planned Submission Dates" against the Master Programme. A variance of >14 days is a critical non-compliance and must be reported immediately.
- **CG Response PDF Check**: Before auditing a register against CG comments, check the register's folder for existing CG response PDFs (e.g., `MOC-MUS-ASE-MEP-ZD-0068.pdf`). These may contain CG comments that need to be addressed in the register — do not start from scratch.
- **Linked Activity ID**: This column must be populated with program activity references. An empty column is a compliance gap that CG will flag.

## CG-Requested Items to Add
When CG comments reference a PDF review, check for these additional deliverables:
- Site Assessment & Survey Report
- MEP Design Risk Management Report
- MEP Value Engineering Study
- Concept Design Review & Gap Analysis Report
- Existing As-Built Drawing Survey (per CG comment #5)
- RACI Matrix for interface parties (per CG comment #4)

## Pitfalls
- **Default values in generation scripts**: Always set CG as the default in the script, not as a post-fix. A post-fix can be overwritten by the script's own defaults.
- **Sheet name truncation**: Excel limits sheet names to 31 characters. Verify after creation.
- **Duplicate IFC refs**: Each floor needs a unique package reference (e.g., `ME-300001-BF-IFC` not `ME-300001-IFC` for all floors).
- **Mixed date formats**: Standardize to DD/MM/YYYY string format. Avoid datetime objects that render differently across locales.
- **Empty IFC rows**: When copying template, ensure all IFC rows are fully populated (Responsibility, Date, Review Duration, Approval Authority).
- **Multi-discipline files**: Each discipline gets its own file. Do not put Arch + Mech in the same workbook.
- **Merged cells — safe insertion pattern**: When inserting rows into an Excel sheet with merged cells, do NOT use `ws.insert_rows()` directly — merged cells break. Instead:
  1. Unmerge ALL merged ranges first (store their definitions)
  2. Read all data into a list-of-dicts structure
  3. Insert new rows into the data structure
  4. Clear the sheet completely
  5. Write all data back row by row
  6. Re-apply merged ranges (shifted for rows after the insertion point)
  7. Apply new merges for any new section headers
  See `references/excel-merge-safe-insertion.md` for a reusable Python script.
- **PDF extraction**: Use pdfplumber (not pdfminer) for PDF text extraction. Handle extraction failures gracefully.

## Gate Structure
The standard 3-gate structure (DD → Material → IFC) may need a **Gate 1.5 (90% Detailed Development)** for disciplines where accessibility/compliance plans are required. This applies to:
- **Architecture**: Accessibility & Universal Design Plans (SBC 201) — spatial layout must be finalized at DD first, then accessibility overlay at 90%
- Insert Gate 1.5 between Gate 1 and Gate 2, with the same per-floor breakdown as Gate 1
- Use submission category "Detailed Development (90%)" to distinguish from DD items

## Related Skills
- `design-submission-packaging` — packaging design drawings for submission
- `sample-submittal-system` — physical material sample submittal pages
