---
name: rfp-generation
description: Generate RFPs (Request for Proposal) from received technical proposals and quotations. Extract specs, BOQ, compliance data from source PDFs, build multi-sheet RFP Excel, deploy to subcontractor folder.
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [macos]
metadata:
  hermes:
    tags: [bim, procurement, rfp, excel, subcontractor, document-control]
    related_skills: [project-register-manager, samaya-technical-office]
---

# RFP Generation

## When to Use
- User provides a **technical proposal** (TOS) and/or **quotation** from a vendor
- User asks to generate an **RFP** to solicit competitive bids for a subcontractor package
- User says "generate RFP from these docs" or "form this docs i want to generate RFP"

## Workflow

### Step 0: Find Governing Design Documents FIRST

Before extracting vendor data or generating an RFP:
1. Search the project's design files (`03_Design_Files/`) and subcontractor `02_Reference_Drawings/` for the governing design report
2. Read the design intent - treatment types, performance targets (NRC, RT60, NR), product classes (Class A/B/C)
3. Cross-reference with BOQ to map design intent to finish codes
4. Only then read vendor proposals - vendor products are for comparison, not scope definition

**CRITICAL:** The RFP Technical Specs sheet must reference **design intent treatments** (e.g. "Class B acoustic spray (Sonaspray 15mm)") - NOT vendor product names. Vendor proposed products appear in the Compliance Matrix sheet only, as alternatives being evaluated against the design intent.

### Step 1: Extract Source Data
Use `pdftotext` to extract text from source PDFs:

```bash
pdftotext -layout "/path/to/TOS.pdf" /tmp/tos_full.txt
pdftotext -layout "/path/to/Quotation.pdf" /tmp/quotation_full.txt
```

Read extracted text with `read_file` to understand:
- **TOS**: scope, BOQ items, product specs (NRC, fire rating), quantities, programme, deliverables
- **Quotation**: unit rates, total price, payment terms, warranty, programme

### Step 2: Check Existing Subcontractor Folder
Before creating anything, inspect the subcontractor folder at `24_Subcontractors/NN_xxx_Contractor/`:

- `_MANAGER_DASHBOARD/SPEC.md` — existing scope spec
- `_MANAGER_DASHBOARD/SITUATION_REPORT.md` — current status
- `_MANAGER_DASHBOARD/SCOPE_REQUEST.md` — original scope request
- `01_Schedule_and_BOQ/` — existing schedules
- `03_Specifications_and_Standards/` — vendor datasheets, material specs
- `05_Returned_Submittals/` — previously returned submittals

### Step 3: Generate RFP Excel
Create a multi-sheet RFP workbook with these sheets:

| Sheet | Content |
|---|---|
| **Cover** | Project info, RFP ref, submission deadline, site visit date, prepared by |
| **RFP Overview** | Background, scope of work, design responsibility, key requirements, submission requirements, evaluation criteria, commercial terms |
| **Technical Specs** | BOQ items with design intent treatments (e.g. Sonaspray 15mm, Sonacoustic), NRC targets, fire ratings, absorption class. Vendor proposed products go in the Compliance Matrix sheet only. |
| **BOQ** | Quantities with unit rates column (TBD for bidder pricing) |
| **Compliance Matrix** | TOS proposed products vs iAcoustics spec — NRC, fire rating, thickness, status |
| **Submission Requirements** | Deliverables checklist (D1–D10) with descriptions and formats |
| **Evaluation Criteria** | Weighted criteria (Tech 40%, Commercial 30%, Programme 15%, Local Content 10%, HSE 5%) |

**Formatting rules** (per Aseer standard):
- Dark blue headers (`1F4E79`), white bold font
- Alternating row colors (`DDEBF7` / `FFFFFF`)
- Green fill (`E2EFDA`) for "Exceeds" compliance status
- Auto-filter on all data sheets
- Frozen panes on header row
- Column widths auto-adjusted

### Step 4: Deploy to Subcontractor Folder
Copy files to the subcontractor folder:

```
24_Subcontractors/NN_xxx_Contractor/
├── _MANAGER_DASHBOARD/
│   └── RFP_xxx_Package.xlsx
└── 08_RFP_and_Proposals/          (create if not exists)
    ├── TOS-xxx.pdf                (source proposal)
    ├── Quotation-xxx.pdf          (source quotation)
    └── Backup_Report_xxx.xlsx     (if applicable)
```

Use `cp` for deployment (OneDrive syncs automatically).

### Step 5: Report Summary
Report to user:
- Files deployed and their destinations
- Key RFP parameters (deadline, scope, total quantity)
- Current subcontractor status (appointed/pending, design basis status)
- Next actions (issue RFP, appoint specialist, update SPEC.md)

## RFP Excel Template Structure

```python
# Key constants
HDR = PatternFill(start_color="1F4E79", end_color="1F4E79", fill_type="solid")
SUB = PatternFill(start_color="DDEBF7", end_color="DDEBF7", fill_type="solid")
ALT = PatternFill(start_color="F2F2F2", end_color="F2F2F2", fill_type="solid")
GRN = PatternFill(start_color="E2EFDA", end_color="E2EFDA", fill_type="solid")

# Cover sheet: project info, RFP ref, submission deadline, site visit
# RFP Overview: 7 sections (background, scope, design resp, requirements, submission, evaluation, commercial)
# Technical Specs: BOQ Ref, Description, Floor(s), Class, NRC Target, Fire Rating, Proposed Product, Remarks
# BOQ: Item No, BOQ Ref, Description, Supplier, Unit, Qty, Unit Rate (TBD)
# Compliance Matrix: Product, Spec NRC, Proposed NRC, Status, Fire Rating, Thickness, Remarks
# Submission Requirements: #, Deliverable, Description, Format
# Evaluation Criteria: Criteria, Weight, Sub-Criteria, Scoring Guide, Max Score
```

## Pitfalls

- **OneDrive cloud stubs**: If deploying to OneDrive path, verify the file is a real ZIP (not a 6KB stub) before reporting success. Use `cp` not `wb.save()` to OneDrive path.
- **Missing SPEC.md**: If the subcontractor folder has no SPEC.md, create one first (see `project-register-manager` skill).
- **TOS vs BOQ mismatch**: The TOS may propose value-engineered alternatives (e.g., 25mm spray instead of 15mm). Document the substitution clearly in the Compliance Matrix with NRC comparison.
- **Fire rating conflicts**: Some products (e.g., Kvadrat Hallingdal 65) may fail KSA fire rating requirements. Flag in the Compliance Matrix and recommend alternatives.
- **Local content**: Track KSA-sourced vs imported materials. USG ME (baffles) is local; Bowiq (spray/plaster) and Kvadrat are imported.
- **Programme alignment**: The RFP programme should match the project's DMP milestones. TOS proposes 22 weeks — verify against the project's master schedule.
- **Bidder pricing columns**: Leave unit rate columns as "TBD" — bidders fill these in. Do NOT populate with the source quotation's rates (that's the received proposal, not the RFP).
