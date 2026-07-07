---
name: subcontractor-submittal-registers
description: >-
  Create and maintain submittal registers for each subcontractor package, driven
  from contract documents (SOW/ER) via SPEC.md specs. Registers are organized by
  design stage (50/90/100/IFC), stored in their own subfolder per subcontractor,
  with management specs in _MANAGER_DASHBOARD/.
version: 1.0.0
author: Hermes Agent
metadata:
  hermes:
    tags:
      - submittals
      - registers
      - subcontractors
      - specs
      - project-management
    related_skills:
      - project-register-manager
      - sub-labor-orchestrator
---

# Subcontractor Submittal Register Workflow

## When to Use

The user asks to create, update, or review submittal registers for subcontractor
packages — typically on a D&B museum/cultural project with staged design delivery
(50% / 90% / 100% DD → IFC/AFC).

**Trigger phrases:** "list design submittals", "make register for", "submittal
tracker", "next discipline", "next".

## Process

### 1. Identify the Subcontractor Package

- **Authoritative source:** Use `APPendix B.pdf` (`Subcontractors/_assets/`)
  for the canonical subcontractor list — NOT the README or folder listing.
- Check which packages already have registers in their subfolder.
- Verify the folder exists under `Subcontractors/NN_Discipline_Contractor/`.

### 2. Extract Scope from Contract Documents

Read the relevant SOW sections (document:
`Contracts/01_Main_Contract/Contractors Scope of Works Document - Technical_250313/6380_KMS_RPT_PM_AS_00006_Aseer_Contractors_Scope of Work.pdf`)
and ER sections (document:
`Contracts/01_Main_Contract/Contractors Employers Requirements - Engineering_250313/250313_ER Document - Aseer Museum of Arts_R02.pdf`).

Key SOW sections by discipline:

| Package | SOW Sections |
|---------|-------------|
| AV/IT | 6.22.2, 6.22.4(xiii), 8.9 |
| Exhibition Fit-Out | 6.22, 6.22.4(i–xviii), 8.2–8.7 |
| Graphics | 6.22.1, 6.22.4(viii–xi), 8.14 |
| Structural | 7.2, 7.3, 8.2, 8.3 |
| MEP | 7.1, 7.3, ER 3.2–3.5, 5.0 |
| FLS | 6.22, ER 3.5, SBC801 |
| Lighting | 6.22.3, 6.22.4(xiv), 8.8 |
| Showcases | 6.22, 6.22.4(v–vi), 8.15 |
| Model Maker | 6.22, 6.22.4(iii–iv, vii), 8.12 |
| Rigging | 8.2, 8.3 |

### 3. Write SPEC.md First (Spec-Driven)

Create `SPEC.md` in `Subcontractors/NN_Discipline_Contractor/_MANAGER_DASHBOARD/SPEC.md`.

Structure:

```markdown
# SPEC — [Discipline Name]

**Package:** NN — [Name]
**Folder:** ...
**Appendix B ref:** ...
**SOW sections:** ...
**Lead time:** [from README or _MANAGER_DASHBOARD/SCOPE_REQUEST.md or known project facts]

## 1. Scope
[exact scope from SOW — bullet list]

## 2. Exclusions
[items explicitly excluded per SOW or contract]

## 3. Deliverables by Stage
[table per stage — 50%, 90%, 100%, IFC/AFC]

### 50% Design
| Ref | Deliverable |
|-----|-------------|

### 90% Design
...

### 100% Design
...

### IFC / AFC / Construction
...

## 4. Standards & Codes

## 5. Coordination Interfaces

## 6. Long-Lead Items
[CRITICAL — check project README / SCOPE_REQUEST for lead times]

## 7. Quality Gates
```

### 4. Set Stage Masks Appropriately

Use `[50%, 90%, 100%, IFC]` flags per item.

**Rules of thumb:**
- **50%** items: surveys, existing conditions, design concept/philosophy,
  preliminary schedules, basis of design. Target **5–10 items** minimum — not 1–2.
  For long-lead packages, front-load more decisions to 50%.
- **90%** items: refined design, coordinated drawings, detailed schedules,
  specifications, initial samples.
- **100%** items: final coordinated design, ready for IFC documentation.
  Should complete all design items.
- **IFC/AFC** items: shop drawings, fabrication, material submittals with cut
  sheets, prototypes, mock-ups, commissioning, training, spares.

**⚡ CRITICAL: Check lead times before assigning stages.**
- If a package has a known lead time (from README, SCOPE_REQUEST, or project
  context), ALWAYS adjust 50% and 90% packages to include procurement / design
  freeze items early. DO NOT wait for the user to tell you.
- Example: Showcases (14-week lead) need lighting spec, lock system, structural
  design, and power/data integration ALL at 50% — not just the schedule.

### 5. Generate the Excel Register

Write a Python generator script that:
- Reads item data (inline — no external parser for now)
- Creates 4 package sheets (50%, 90%, 100%, IFC/AFC) + Legend sheet
- Uses colour-coded headers matching each stage
- Freezes header row, enables auto-filter
- Saves to 3 locations:

| Location | Path |
|----------|------|
| Submittals | `02_Submittals/<Register_Name>/` |
| Registers | `Docs/09_Registers/<Register_Name>/` |
| Subcontractor | `Subcontractors/NN_Discipline/<Register_Name>/` |

**Register folder naming:** `<Discipline>_Submittal_Register/` containing the
Excel file with the same name.

### 6. Reference Rules

- **All references must be only SOW § and ER §.** No external specs, no
  interface matrix citations.
- Item descriptions must use **exact SOW wording** — not paraphrased.
- When the user says "list same as SOW Listed", descriptions must match the
  SOW document verbatim.

### 7. Run QA Before Delivery

Per user preference: **Kimi = QC** for register generation tasks.
Delegate QC review to Kimi (or delegate_task if Kimi times out) to validate:
- [ ] Stage masks appropriate for each item
- [ ] 50% package has enough items (not 1–2)
- [ ] Long-lead items identified and front-loaded
- [ ] Descriptions match SOW wording
- [ ] No external references (only SOW/ER)
- [ ] All SOW scope items represented
- [ ] Category header ranges don't overlap

## Known Pitfalls

1. **50% packages that are too thin** — requires active checking. Minimum 5–8
   items for a meaningful gate review. For long-lead packages (Showcases 14wks,
   MEP 12-16wks), push to 8+ items at 50%.
2. **Ignoring lead times** — README, SCOPE_REQUEST, and project memory contain
   lead times. Check ALL of them before assigning stages. Long-lead packages
   need structural design, material selection, and lighting/AV integration
   concepts at 50% — not just a schedule. DO NOT wait for the user to flag this.
3. **Using wrong subcontractor list** — always use APPendix B.pdf as the
   authority, not the README or folder listing.
4. **References to non-SOW/ER sources** — strictly prohibited. All refs must
   be SOW § or ER § numbers.
5. **Paraphrasing instead of exact SOW wording** — use verbatim descriptions
   from the contract documents.
6. **Draft email files left in project** — remove any `draft_email_*` or
   `_Email_to_*.md` files. They are not needed.
7. **Category header range overlap** — when using ref-number-based ranges in
   generator scripts, ensure upper bound doesn't overreach into the next
   category. Use next category key as exclusive bound.
8. **Register files in wrong location** — Excel registers go in their own
   subfolder (`<Register_Name>/<Register_Name>.xlsx`). SPEC.md goes in
   `_MANAGER_DASHBOARD/`. Never mix them.
9. **Stale generator paths after renumbering** — when subcontractor folders are
   renumbered to Appendix B order, ALL generator scripts' `Subcontractors/<old>/`
   paths must be updated. Run: `grep -r "Subcontractors/" 02_Submittals/*.py`
   and verify each path resolves to the current folder name. Regenerate all
   registers after fixing paths.
10. **Master register not updated** — after creating/changing any individual
    register, regenerate `Master_Submittal_Register` and recopy to all
    `Subcontractors/*/_MANAGER_DASHBOARD/`.


## Document Numbering — Discovery Protocol

Before adding ANY document reference to a submission, verify the standard:

1. **Check the DMP** (Design Management Plan) — Sec 7.2 naming convention for project-specific discipline codes
2. **Check the BEP Document Numbering Procedure** at `Invoices/Docs/design managment plan/BEP/DOCUMENT NUMBERING PROCEDURE.xlsx` — the authoritative standard with all discipline codes and document type codes
3. **Cross-check actual project documents** — verify the format is actually used in real submittals (e.g. `MOC-MUS-ASE-1E0-ZD-0038`)
4. **Check project memory** (`_Project_Memory/PROJECT_MEMORY.md`) — look for CG directives on numbering format
5. **Never guess** — if the standard isn't clear, ask the user

### Known Aseer Museum Convention

- Format: `MOC-MUS-ASE-<DISCIPLINE>-<TYPE>-<SEQ>`
- Discipline codes: 1A0=Arch, 1E0=Electrical+AV, 1K0=Multi, 1KH=HSE
- CG directive (Jun 2026): prefers simple format `AV-XXXX` for submittal items
- For Submittal Register documents: type code `RG` (Register)
- Document type codes from BEP: MP=Plan, ZD=Drawing, PQ=Prequal., SC=Spec/Submittal, RG=Register, IR=Inspection, SH=Schedule

## Submission Formatting for Consultant

**Excel file structure (full package):**
- Cover sheet with logo (Samaya), project info, doc ref, revision, date, distribution table
- ALL stages as separate sheets: 50%, 90%, 100%, IFC/AFC/Construction — never one stage alone
- Systems Matrix sheet
- Legend/Status Codes sheet

**Excel formatting rules:**
- All prices/numbers must be actual numeric values with number formatting (`#,##0" SAR"`), NOT text strings
- Use formulas for calculated cells (totals, VAT = total*0.15)
- Never leave empty placeholder cells — truly blank where N/A
- Status column with color coding: P(red), S(yellow), UR, A(green), RR, R
- Freeze header panes, landscape orientation, A3 for wide tables

**Cover sheet:**
- Add Samaya logo (from `_Style-Guides/logos archives/samaya-logo.png`)
- Project identity block, doc reference, revision, date
- Distribution table (Role | Company | Contact)
- List of included packages with item counts

**Writing style:** Brief, factual descriptions per deliverable. No verbose intros or AI-sounding text.

## Cross-Package Submittal Merging

Some submittal items span multiple packages (e.g. rigging is its own package
AND part of Structural's scope). When this happens:
- Keep the standalone subcon folder (e.g. 06_Rigging) with its own register
- ALSO add the rigging items to the parent package's register (e.g. 12_Structural)
  as a new category (e.g. Category G — RIGGING)
- Update the parent package's SPEC.md scope section
- This gives the TO one register covering both scopes while the subcon register
  tracks the specialist's deliverables
