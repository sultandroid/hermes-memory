---
name: subcontractor-folder-setup
title: Subcontractor Folder Setup & Audit
description: Full workflow for creating, auditing, and populating subcontractor folders with standard structure, SOW, and reference files.
---

## When to use

- Creating a new subcontractor folder (e.g., for a newly identified specialist)
- Auditing existing subs for missing structure, SOW, or misplaced files
- Remediating gaps found during audit (missing dirs, no SCOPE_REQUEST, root-level clutter)

## Standard folder structure

Subcontractors live under `Subcontractors/NN_Name/` where NN = sequential number.

**Two co-existing Aseer patterns — pick by location:**

| Location | Pattern | Filename | Naming |
|----------|---------|----------|--------|
| **Repo** (`~/aseer-museum-pm/Subcontractors/...`) | Sub-per-vendor tree | `NN_<Vendor>/00_Prequalification/...` | NN = sequential sub number; vendor name as folder |
| **OneDrive — CG/CDE submittal copy** (`Adel Darwish's files - 01- Execution Documents/07- Pre-Qualification Submittal/`) | Flat by PQ ref | `NN- MOC-...PQ-XXXX/...` with `Approval/` subfolder | NN = PQ number; flat — no sub-per-vendor wrapping |

The OneDrive copy is what goes to CG via Aconex. The repo copy is the coordination
mirror. They must agree. When a new vendor PQ lands, mirror it in both: create
`00_Prequalification/<Vendor>/` in the repo AND `NN- MOC-...PQ-XXXX/` in OneDrive.

```\\nNN_Subcontractor_Name/\\n├── SCOPE_REQUEST.docx                 (generated from SamayaDoc template)\\n├── 09_Prequalification/             Prequalification dossiers, company profiles, qualifications docs, support docs for supplier to stamp — each company gets its own subfolder (e.g., `Acoustige/`, `AME/`)\\n├── 01_Schedule_and_BOQ/               BOQs, schedules, cost data\\n├── 02_Reference_Drawings/             IFC drawings, reference CAD/PDF\\n├── 03_Specifications_and_Standards/   ER, SoW, Division specs, codes, TDS/SDS\\n├── 04_Reference_Imagery/             Photos, reference images\\n├── 05_Returned_Submittals/           Submittals returned from review\\n├── 06_RFIs/                          RFI register and correspondence\\n├── 07_Approvals/                     Approved documents, certificates\\n├── 09_Offers/                        Commercial proposals, quotations per company — each company gets its own subfolder (e.g., `AD_Engineering/`, `SG_Group/`)\\n├── Email_Data_Extraction/            Extracted email threads\\n└── _MANAGER_DASHBOARD/               All .md management files live here (NO Excel files, NO draft email .md files, NO .docx)\\n    ├── SCOPE_REQUEST.md               Source markdown (editing copy)\\n    ├── SITUATION_REPORT.md            Status tracking\\n    └── SPEC.md                        Package specification (scope, deliverables by stage, long-lead items)\\n\\n**Note:** Draft email .md files (`_Email_to_*.md`, `DRAFT_EMAIL_*.md`) are deleted — do not keep them. Send the email directly instead.\\n```

## File placement rules (hard conventions)

| File type | Goes in | Never in |
|-----------|---------|----------|
| SCOPE_REQUEST.md | `_MANAGER_DASHBOARD/` | Sub root |
| SCOPE_REQUEST.docx | Sub root | `_MANAGER_DASHBOARD/` |
| SITUATION_REPORT.md | `_MANAGER_DASHBOARD/` | Sub root |
| Email drafts, research notes | `_MANAGER_DASHBOARD/` | Sub root |
| PDFs, xlsx, dwg, docx | `01_*` through `07_*` | Sub root |

## Full setup workflow

### 1. Create folder structure
```bash
mkdir -p Subcontractors/NN_Name/{00_Prequalification,01_Schedule_and_BOQ,02_Reference_Drawings,03_Specifications_and_Standards,04_Reference_Imagery,05_Returned_Submittals,06_RFIs,07_Approvals,09_Offers,Email_Data_Extraction,_MANAGER_DASHBOARD}
```

### 2. Write SCOPE_REQUEST.md
Write to `_MANAGER_DASHBOARD/SCOPE_REQUEST.md`. Section structure varies by sub type:

**Contractor/installer subs** (standard structure):
1. Purpose
2. Programme (table: Milestone | Target Date)
3. Scope of Work (with subsections and discipline tables where applicable)
4. Submission Requirements
5. Reference Documents (table: Location | Contents)
6. Workflow & Communication
7. Sign-offs Required (table: # | Sign-off | Owner | Trigger)
8. Action

**Designer/consultant subs** (lighter structure — no install/submission/sign-off sections):
1. Purpose
2. Scope (discipline subsections)
3. Deliverables (table: Deliverable | Due)
4. Reference Documents
5. Compliance / Standards
6. Programme (table: Milestone | Date)

Designer scopes focus on design deliverables and compliance standards rather than site installation, submittal routing, or sign-off workflows. Omit submission requirements and sign-off tables for design-only subs.

Metadata block at top: Project, Issuer, Issued to, Issue date, Reply by, Discipline, KPR ID, Subcontractor Register ID.

**Pitfall — "Issued to" for pre-award subs:** When the sub hasn't been appointed yet, do NOT write a placeholder or leave blank. Write the current negotiation status explicitly, e.g.:
- `"being negotiated — ITC contract on hold; candidates include AD Engineering, Bluehaus, SG Group"`
- `"pre-qualified pending appointment"`
- `"under evaluation — offers received from [Company A], [Company B]"`
This ensures the reader can immediately see the procurement status from the document header without cross-referencing other files.

### 3. Generate SCOPE_REQUEST.docx
Use `samaya-docx-template` skill — read .md from `_MANAGER_DASHBOARD/`, save .docx to sub root.
Doc ref pattern: `MOC-ASEER-SIC-1K0-SC-NNN`

**CRITICAL:** Never pass `col_widths_cm` to `doc.add_table()` — python-docx stores EMU as 'dxa' units, producing 4000-inch-wide columns. Instead, call `add_table()` without widths, then apply `set_table_widths(t, widths)` after creation. See `samaya-docx-template/references/docx-generation-example.md` for the full gen script with `cm_to_twips()` and `set_table_widths()` helpers.

### 4. Create SITUATION_REPORT.md
Write to `_MANAGER_DASHBOARD/` with: project info, status, key requirements, action checklist.

### 5. Create email draft
Write to `_MANAGER_DASHBOARD/_Email_to_Project_Team.md` — assign actions with timeline.

### 6. Copy reference files
Copy from existing subs (typically 10_Oddy_Testing_Lab as source):
- ER Document (Employer's Requirements)
- SoW PDF
- Division 00 + 01 (General Requirements)
- Applicable Codes

## Audit workflow

When asked to "clean up" or "organize" subcontractors:

### 1. Structure audit
Check each sub against the standard 9-dir structure. Flag missing dirs.

### 2. SOW audit
Check each sub has SCOPE_REQUEST.md in `_MANAGER_DASHBOARD/`. Flag missing.

### 3. Root file audit
Check for files at sub root — should only be `SCOPE_REQUEST.docx`.
- `.md` files → move to `_MANAGER_DASHBOARD/`
- Technical files (PDFs, xlsx) → move to `01_*` through `07_*` subdirs
- Delete duplicate `.docx` if `.md` exists with same content

### 4. Duplicate check
Check for identical files (same MD5 hash) within a sub. Keep project-registered naming, remove original-named duplicates.

### 5. Numbering conflict check
Check for duplicate numbers (e.g., `10_Oddy` and `10_Purchasing`). Use `a`/`b` suffix to disambiguate.

### 6. Duplicate discipline check
If the same discipline appears under multiple numbered folders (e.g., `12_MEP_Installation`, `14a_MEP_Contractor`, `18_MEP_Designer`), **verify they represent genuinely distinct contractual scopes** before assuming they're all needed. Common MEP split on museum fit-out:
- **Designer** (#18 typically) — produces IFC drawings, load calculations, BIM models (consultant/engineer role)
- **Contractor** (#12 typically) — manages procurement, supply, and installation as a single entity

If Installation and Contractor are the same entity, consolidate into one folder (keep #12 as it's earlier in the sequence; delete the `a`-suffixed duplicate). Update the README register table accordingly.

See reference: `references/mep-scope-split-consolidation.md` for a worked example of this exact pattern on the Aseer Museum project.
### 7. Offers folder audit

`09_Offers/` must contain **commercial proposals/quotations only** — NOT prequalification or qualifications docs. Prequalification material goes in `09_Prequalification/` at the same level.

Offers folder conventions:
- **Each company** gets its own subfolder inside `09_Offers/` (e.g., `09_Offers/AD_Engineering/`, `09_Offers/SG_Group/`)
- Prequalification docs stay in `09_Prequalification/` — even if from the same company
- When a company submits both prequalification and an offer, file prequal in `09_Prequalification/<Company>/` and the offer in `09_Offers/<Company>/`
- If the company name is unknown, use a descriptive folder name (e.g., `MEP_Design_Offer/`) and ask the user

### 8. Offer gap analysis (SOW §8)

After one or more offers are received in `09_Offers/`, document the gap analysis directly in the SCOPE_REQUEST.md:

**Before starting the gap analysis, trace the full email thread first.** The quotation you're reviewing may already have a history — CG submissions, Code B/C responses, CRS requirements, internal cross-references done weeks ago. Check:

1. **Outlook** — search the sub's name/email domain in the SQLite database (see `outlook-email` skill). Read the full thread in order: initial proposal → internal review → CG submission → CG response → revised quotation
2. **CG status** — was the sub's SOW submitted to CG as a formal document (ZD-xxxx)? What was the response? Code B means comments need a CRS before the quotation can be finalized
3. **Existing cross-references** — search session history for previous reviews of this sub's proposal (using `session_search`). Sultan may have already completed a cross-reference against ER/SOW/DMP that you should build on, not redo
4. **Scope split decisions** — check if the team has already decided to move scope items between subs (e.g., BIM/Revit moved from Lighting Designer to MEP Designer; shop drawings moved from specialist to MEP Contractor). The quotation may need to be adjusted to reflect the revised split

**Pitfall — reviewing a quotation without thread context:** A quotation that looks incomplete may actually already have a CG-approved SOW with Code B comments. The gaps you identify may overlap with an existing CRS in progress. Always read backwards from the most recent email to the oldest.

**Pitfall — scope review baseline:** Always use the **submitted and CG-approved SOW** as the baseline for gap analysis, not internal revisions that were never submitted. A SOW returned Code B by CG is still the approved scope — CG accepted it with minor comments, not full rejection. If the user's own internal cross-reference said "substantially compliant — no missing core deliverables," that is the correct framing. Avoid grading against internal Rev XX documents that were never sent to CG.

**Pitfall — don't over-state gaps:** When the user says "we will base only the submitted scope of work," take that as the final word. Don't counter with a different baseline or argue about coverage percentages. The user knows their documents. Simple frame: "here's what's covered, here's what we need from them to close CG comments, here's what other subs own."

**Pitfall — not all gaps are gaps:** When something looks missing from a quotation, first check which other subcontractor owns that deliverable in the full scope split. Common patterns on museum fit-out:
- BIM/Revit authoring → often assigned to a dedicated BIM specialist (e.g., Radiance Group), not each designer
- Shop/workshop drawing production → often assigned to the MEP Contractor, not the designer
- Supply, installation, commissioning execution → assigned to contractor, not designer
- Civil Defence submissions → assigned to MEP Designer or MEP Contractor
- O&M manuals → produced by the installing contractor, not the designer
- As-built documentation → site contractor, not design consultant

Before flagging a gap, trace who actually does the work across all subs. See `references/zna-quotation-review-pattern.md` for a worked example.

1. Read each offer PDF/email in `09_Offers/<Company>/`
2. Open `_MANAGER_DASHBOARD/SCOPE_REQUEST.md`
3. Add a **§8 Offer Appraisal** section comparing each offer against the SOW requirements
4. Create a 4-column gap table: SOW Section | Required Scope | Their Offer | Gap Severity
5. Use plain text severity labels ("Critical" / "Moderate") — no emoji icons, no bold in body cells
6. Add a fee benchmark sub-table under §8.2
7. Wrap up with a recommendation verdict paragraph
8. Regenerate SCOPE_REQUEST.docx to include the new section

The gap analysis documents procurement traceability — who offered what, what's missing, and why the recommendation stands. Reference the company's offer file path in the analysis paragraph.

**Pitfall — scope split mismatch:** The offer may include scope items that have already been reassigned to another subcontractor (e.g., Lighting Designer quotes shop drawing production but the team decided MEP Contractor does shop drawings; designer quotes Revit/BIM authoring but MEP Designer covers that). Before gap analysis, adjust which quotation items are in-scope for THIS sub by removing items reassigned elsewhere. Document what was removed and why. This prevents asking the sub to requote for items they shouldn't be doing.

See `samaya-docx-template/references/mep-offer-appraisal.md` for a worked example (AD Engineering vs MEP Designer SOW).

Cross-discipline check: `09_Offers/` may contain proposal documents from a **different discipline** than the folder they're filed under (e.g., MEP design consultancy proposals filed inside the MEP Contractor's folder). Before assuming they belong:
- Read the proposal file names — do they match the folder discipline?
- Check title pages or metadata for the actual scope described
- Move mis-filed proposals to the correct sub's `09_Offers/`
- If no `09_Offers/` exists at the target, create it before moving

### 9. Filename convention audit (Arabic→English)

Arabic-named files from KSA subcontractors must be renamed to descriptive English names. Check every subfolder for Arabic characters in filenames.

Procedure:
1. **List all files** under the sub's directories
2. **Identify Arabic filenames** — look for Arabic script characters
3. **Translate** the filename to English reflecting document content
4. **Rename** using the rules:
   - Keep numbering prefix for sort order
   - Underscores between words, not spaces
   - Company name as suffix
5. **Leave existing English-only files unchanged**

See `references/mep-scope-split-consolidation.md` for the full Arabic→English translation table covering the 23 most common document types.

## Domain: Supplier Profile Receipt & Assessment Workflow

When a supplier sends a company profile / prequalification PDF (via email, download, or file share):

### 1. Check if already filed

Compare MD5 hash of the incoming file against the file already in the subcontractor folder. If identical, no move needed — confirm to user.

### 2. Assess compliance against project specs

Open the sub's `_MANAGER_DASHBOARD/SCOPE_REQUEST.md` and `SPEC.md`. Compare the supplier profile against each requirement:

| Check | What to verify |
|-------|---------------|
| Portfolio | ≥3 similar projects (museum/cultural/high-profile) |
| Climate/region | Experience in project-specific conditions (e.g. high altitude, coastal) |
| Team depth | Landscape Architect, Engineers, specialists per SPEC |
| Certifications | CR, VAT, SCA, ISO, Classification |
| Scale | Has the supplier done projects of comparable complexity? |

Produce a structured verdict: recommended for sole appointment, keep as execution-only sub, or not recommended. List specific gaps.

### 3. Create prequalification support document

Generate a DOCX for the supplier to complete and stamp. This is Samaya's document sent TO the supplier — NOT the supplier's own methodology doc. See "Prequalification Support Document" below.

### 4. Generate compliance Excel sheet

Create a companion compliance matrix as an Excel file alongside the prequalification documents. This is the structured audit record of the supplier against project requirements. Save as `00_Prequalification/<Supplier>_Compliance_Sheet.xlsx`.

**Required sheets (5):**

| Sheet | Content |
|-------|---------|
| Overview | Sub info, assessment date, overall verdict, score summary table (5 domains) |
| Compliance Matrix | Line-by-line against SCOPE_REQUEST submission requirements (Yes/Partial/Missing with severity) |
| Technical | Technical requirements mapped to source docs (ER, SOW, SPEC) with status |
| Risk Assessment | 7+ risks with likelihood, impact, severity, mitigation, owner |
| Actions | Prioritized next actions with owner and target date |

**Excel formatting rules:**
- Navy header row (#1E293B), white bold text, 10pt Calibri
- Body cells: 10pt Calibri, wrap text on description columns
- Status cells: color-coded fill (green=met, amber=partial, red=missing)
- Risk severity: red fill for CRITICAL/HIGH, amber for MEDIUM
- Borders: thin gray (#D0D0D0) on all cells
- Column widths: proportional to content (description columns widest)

**Data sources to check per row:**
- `_MANAGER_DASHBOARD/SCOPE_REQUEST.md` — submission requirements (Section 5), technical requirements, programme
- `_MANAGER_DASHBOARD/SPEC.md` — deliverables by stage, standards, long-lead items
- Supplier profile PDF — company credentials, portfolio, team
- Signed PQ letter — RACI matrix, risk register, compliance statements
- ER / SoW documents — specific code references, sustainability requirements

**Pitfall — do not mark items as "Missing" that are Samaya dependencies.** If the supplier cannot provide a priced BOQ because Samaya has not provided the design yet, mark severity as "Low (Samaya dep.)" not "Critical".

### 5. Organize folder

- Create `09_Prequalification/` at sub root if not exists
- Move supplier profile PDF into `09_Prequalification/`
- Move the compliance Excel sheet into `09_Prequalification/`
- Move the support document into `09_Prequalification/`
- Clean up any Word temp files (`~$*.tmp`)
- Remove duplicate SCOPE_REQUEST.docx from `_MANAGER_DASHBOARD/` (keep only .md there)

## Domain: Prequalification Support Document (Samaya → Supplier)

When Samaya needs to send a supplier a document to complete, stamp, and return as part of prequalification. This is distinct from SCOPE_REQUEST (Samaya's scope brief) and from the supplier's own methodology doc.

### Document structure (10 sections)

| Section | Content |
|---------|---------|
| Cover | Project name, contract ref, trade, "Submitted to: Samaya Investment" |
| 1.0 | Introduction & Purpose |
| 2.0 | Project overview table (location, altitude, contract type, team) |
| 3.0 | Scope of Work (hard/soft landscape, existing services) |
| 4.0 | Design deliverables by stage (50%/90%/100%/IFC) |
| 5.0 | Supporting documents provided (table: #, Document, Contents) |
| 6.0 | **Submission forms to fill** — blank tables for CR info, portfolio (5 rows), personnel CVs, method statement, plant schedule, priced BoQ, O&M sample |
| 7.0 | Coordination interfaces |
| 8.0 | Programme & milestones |
| 9.0 | Commercial terms |
| 10.0 | **Declaration & signature block** — "Authorised Signatory", "Signature", "Date", "Company Stamp" |

### Branding rule

This is Samaya's document sent TO the supplier. Use Samaya branding (navy/red, SamayaDoc template or standalone navy style). Cover says "Submitted to: Samaya Investment" and "Prepared by: [Supplier Name]". The supplier stamps Section 10.0.

### Key sections that must be fill-in forms

Section 6.0 must contain blank tables the supplier fills out:

- **Company Information** — CR No., VAT, SCA, ISO, employees, turnover
- **Portfolio** — 5-row table: Project Name, Location, Client, Value, Year, Scope
- **High-Altitude / Region Experience** — blank lines for narrative
- **Key Personnel** — Role, Min. Experience, Name (blank)
- **Method Statement** — blank lines
- **Plant Schedule** — blank
- **Priced BoQ** — blank
- **O&M Manual Sample** — request

### Generation approach

Use standalone python-docx (not SamayaDoc) with navy color scheme. The document is a formal Samaya document but doesn't need the full SamayaDoc header/footer template — it's a working document for the supplier to fill.

### When to generate

- A supplier profile is received and assessed (see Supplier Profile Receipt workflow)
- The user asks "make a doc for the supplier to stamp"
- A prequalification process is initiated for a new sub
- CG rejects a prequalification because SOW and RACI were not attached — generate a combined SOW+RACI support doc (see `references/acoustic-prequalification-pattern.md`)

### Generation script

A reusable generation script is at `templates/gen_acoustic_prequal.py`. It produces a 10-section Samaya-branded DOCX with full SOW, 21 deliverables, RACI matrix (11 activities × 6 roles), prequalification requirements, submission forms, coordination interfaces, standards, and declaration. Adapt the COMPANIES list and BASE path for other specialist types.

## Domain: Subcontractor Prequalification Doc Generation (absorbed from session learnings)

When creating prequalification documents for a subcontractor (methodology, programme, company profile docs):

### Branding rule — subcontractor's logo, not Samaya's

The documents are prepared FOR Samaya BY the subcontractor. Use the subcontractor's own logo and color palette. The cover should say "Submitted to: Samaya Investment — Technical Office" and "Prepared by: [Subcontractor Name]". Do NOT use SamayaDoc or Samaya colors.

See `samaya-docx-template/references/standalone-subcontractor-docx-pattern.md` for the full pattern: SVG chart embedding, programmatic DOCX generation with cairosvg, DMP Gate + Day + RACI column templates, Oddy scope boundary, BIM coordination ownership split, and third-party report handling.

### Two prequalification doc patterns

**Pattern A — Samaya prepares ON BEHALF of the supplier (preferred when supplier needs guidance):**
Samaya writes the complete prequalification letter as if from the supplier, confirming project understanding, design awareness, execution sequence, and compliance. The doc is then sent to the supplier to stamp and return. This is the preferred pattern when the supplier needs guidance on what to submit.

Standard package includes:
- Prequalification letter (project understanding, design awareness, execution sequence, compliance statement, company capability)
- RACI matrix (12+ activities × all project parties — Landscape Evergreen, NRS, Samaya BIM Unit, Samaya PM, CG)
- Risk register (8+ project-specific risks with likelihood/impact/severity/mitigation/owner)
- Declaration & signature block

**Pattern B — Samaya sends a support doc for the supplier to fill (existing pattern):**
Samaya creates a document with blank fill-in forms (CR info, portfolio, personnel, method statement, plant schedule, priced BoQ) for the supplier to complete and stamp. See "Prequalification Support Document" section above.

### Procurement handoff after prequalification

After the prequalification doc is prepared on behalf of the supplier:
- Save to `09_Prequalification/` under the subcontractor's folder
2. Email procurement team with the doc attached
3. Procurement's role: contact the supplier directly, ask them to review, apply company stamp, sign, and return
4. A separate Scope of Work (SOW) document follows as a standalone deliverable

Email template for procurement handoff:
```
Subject: [Supplier Name] — Prequalification Package — Please Contact Supplier to Stamp & Resend

Team,

Please find attached the prequalification package for [Supplier Name].

Action required:
Please contact [Supplier Name] directly, ask them to review the document, apply their company stamp, sign it, and resend it back to us. This is their prequalification submission — it needs their stamp and signature to be valid.

Note:
We have prepared this document on their behalf to ensure they understand the scope of work and all project requirements. A separate Scope of Work (SOW) document will follow to define the full scope, deliverables, and programme.

Please proceed and confirm once done.
```

### Programme: day-based, not calendar dates

Use days from appointment (D0, D30, D50...) on the x-axis, not calendar dates. Calendar dates change if the appointment date shifts; day-based timelines stay correct. Follow DMP gate conventions: G-1 Design Dev, G-2 Material Approval, G-3 IFC, G-4 Construction, G-5 Handover.

### RACI for design specialist subs

| Role | Responsibility |
|------|--------------|
| **Subcontractor** | Design, supply, install — RESPONSIBLE for all deliverables |
| **NRS** | Review/approve all design & material deliverables |
| **Samaya** | Coordinates BIM, MEP, structural. Reviews IFC/commissioning/handover |
| **CG** | Final approval authority |

### Site survey phase — skip if building exists

For fit-out projects where the building shell already stands, do NOT include a separate Site Survey or Baseline Noise Survey phase. Design starts immediately at D0. Add an assumption: "No site survey phase needed — existing building."

## Reference files to copy to every new sub

From `10_Oddy_Testing_Lab/03_Specifications_and_Standards/`:
- `250313_ER Document - Aseer Museum of Arts_R02.pdf`
- `6380_KMS_RPT_PM_AS_00006_Aseer_Contractors_Scope of Work.pdf`
- `Division 00 GENERAL PROJECT REQUIREMENTS.pdf`
- `Division 01 GENERAL REQUIREMENTS.pdf`
- `1.5 APPLICABLE CODES.pdf`

## Pitfall — OneDrive cache blocks `mkdir` from this terminal

The OneDrive tree at
`/Users/mohamedessa/OneDrive - SAMAYA INVESTMENT/Adel  Darwish's files - 01- Execution Documents/`
(and likely the whole `Adel Darwish's files` subtree) shows
`drwx------ 114 mohamedessa staff` in `ls` and the shell reports `uid=501`, but
`mkdir` returns "Operation not permitted" anyway. Cause: OneDrive placeholder
ownership mismatch between the cached copy and the source-of-truth on the
sharepoint server. This is environmental, not a permissions bug you can fix.

**Workaround pattern (Aseer-proven):**
1. Write a `_FILE_PLAN.md` next to the source files (in `~/Downloads` or
   wherever the submittal arrived) naming: (a) the target OneDrive subfolders
   (mirror the `NN- MOC-MUS-ASE-1E0-PQ-XXXX/` pattern with an `Approval/`
   subfolder), (b) which source file goes in which folder, (c) exact `cp`
   commands.
2. The user creates the new subfolders via onedrive.live.com web UI and waits
   for sync to reach this Mac (~5–15 min).
3. The user (or a follow-up session) runs the `cp` commands.
4. The compliance / register update is finalised only after the files have
   been verified on disk — leave PQ Ref cells as `—` until then.

Do not waste a tool call trying to `mkdir` directly — the failure is
deterministic.

## Sample generation script (DOCX)

The full gen script lives under `samaya-docx-template/references/docx-generation-example.md`. Key points:

- Import `SamayaDoc`, `SamayaColors` from the template
- Add `from docx.oxml.ns import qn` and `from docx.oxml import OxmlElement`
- Use `set_table_widths(t, col_widths_cm)` after `add_table()` — never use `col_widths_cm` parameter
- `cm_to_twips()` converts cm to twips (1 cm = 567 twips) for proper Word rendering
- Save .docx to sub root (NOT inside `_MANAGER_DASHBOARD/`)

## Quick status assessment

When asked "what's the status of subcontractor X?" or "what's needed from client for sub X?", run this rapid assessment before digging into the full audit.

### Documents to check (in order)

| Document | What it reveals |
|----------|----------------|
| `_MANAGER_DASHBOARD/SITUATION_REPORT.md` | Current health, critical issues, timeline snapshot, engagement status |
| `06_RFIs/RFI_Register.xlsx` | Pending/open RFIs specific to this sub — check Status column (Open/Under Review/Answered/Closed) |
| `SCOPE_REQUEST.docx` (or `_MANAGER_DASHBOARD/SCOPE_REQUEST.md`) | Full scope split, programme milestones, what the sub must do vs what others/MoC must do |
| `Email_Data_Extraction/*.md` | Recent correspondence, pending actions, design-stage vs production-stage items |
| `01_Schedule_and_BOQ/Registers/*` | Procurement schedule — award status, lead times |
| `_CONTRACT_STATUS.md` (if exists) | One-line contract snapshot: executed/not-yet/on-hold |

### Key questions to answer

1. **Award status** — Is the sub pre-qualified? Awarded? Contract signed? (Check SITUATION_REPORT, Contract/ folder, _CONTRACT_STATUS.md)
2. **RFI posture** — Are there open RFIs waiting on MoC/CG response? Any that need to be chased? (Check RFI_Register.xlsx)
3. **Client dependencies** — What does MoC/PMC/CG need to provide before the sub can proceed (content, approvals, site access)?
4. **Programme compression** — Compare current date against TOC. Is the sub's production/install window still feasible?
5. **Scope boundary clarity** — Where does this sub's responsibility end and another's begin? Look for production-only vs design-author vs content-author splits.

### Common scope split patterns (museum fit-out)

| Sub type | Sub does | Someone else does |
|----------|----------|-------------------|
| Graphics/wayfinding production | Typeset, proof, print, fabricate, mount, install | **MoC** authors exhibition text content |
| AV/IT (Rawasin) | Supply, install, configure hardware, software | **Designer (NRS)** authors media content |
| Showcases (GBH) | Fabricate, deliver, install showcases | **Graphics sub** produces in-case labels, **Oddy lab** tests materials |
| Setworks/joinery | Build brass housings, counters, wall panelling | **Graphics sub** produces inserts for housings |
| **Lighting Designer** (e.g. ZNA) | Design only — layouts, specs, calculations, control strategy, conservation analysis, BIM authoring, site focusing direction | **MEP Contractor** produces shop/workshop drawings, supplies, installs, commissions, executes focusing under designer's direction |
| **MEP Contractor** (lighting install portion) | Shop/workshop drawings, supply, installation, DALI field commissioning, focusing execution | **Lighting Designer** authors design, reviews shop dwgs, directs focusing; **MEP Designer (Bluehaus)** provides power feeds, containment, SLD to luminaire position |

If the sub is **pre-award** (Gap G-XXX open), the binding constraint is typically **procurement** — raise the parallel dependency (client content, designer intent freeze) via RFI in parallel so both tracks converge.

### Output format

Return a compact table:
```
| Aspect | Status | Action Needed |
|--------|--------|---------------|
| Award status | Pre-award (Gap G-009) | Close pre-qualification |
| MoC content | Not received | RFI to CG for freeze date |
| RFI register | Empty | Raise content freeze RFI |
| Programme | TOC 30-Sep, install TOC-21d | Compressing — act now |
```

## Related skills

- `samaya-docx-template` — DOCX generation with SamayaDoc template

## Document pack for contract drafting (`08_Contract_Drafting/`)

When preparing to send a subcontractor their SOW, DMP, and CG comments for confirmation and contract draft review, create an `08_Contract_Drafting/` folder under the subcontractor's directory. Populate with:

| File | Purpose |
|------|---------|
| Sub SOW (Rev XX) | The scope basis for their contract — use the **CG-submitted and approved** version, not an internal revision that was never sent for review |
| DMP (approved/stamped) | Always extract the **NRS-signed or CG-approved** PDF from email, not an internal Word draft |
| CG response (if applicable) | The Code B/C response on their submitted SOW, so they see the comments |
| Submittal Register | Payment milestone alignment |
| Their own quotation (copy) | Reference for cross-checking |

**Key rule — DMP is the most important reference.** The user explicitly flags when the wrong version is used. Always trace Outlook for the actual NRS-signed or CG-stamped PDF.

**Key rule — scope baseline.** Use the submitted-and-CG-approved SOW as the baseline for gap analysis. Internal Rev XX documents that were never submitted to CG are not the contractual reference. If the user's own cross-reference said "substantially compliant," that is the correct finding.

## SPEC.md → Register workflow (spec-first)

Do NOT create the Excel register first and then document it. Follow this order:

1. **Write SPEC.md** — defines scope, exclusions, deliverables by stage (50%/90%/100%/IFC), standards, coordination interfaces, long-lead items
2. **Generate register** — the Excel submittal register is a **derived output** generated FROM the SPEC.md data
3. **Save to 3 locations**: `02_Submittals/<Name>_Submittal_Register/`, `Docs/09_Registers/<NN>_<Name>_Submittal_Register/`, `Subcontractors/<NN>_<Name>/<Name>_Submittal_Register/`
4. **Copy Master** — update and redistribute `_Master_Submittal_Register/Master_Submittal_Register.xlsx` to all subcontractor `_MANAGER_DASHBOARD/` folders

## Submittal Register file conventions

- **One subfolder per register** — each register lives in its own subfolder (e.g., `AV_Submittal_Register/AV_Submittal_Register.xlsx`), NOT as a loose file
- **Same file in 3 locations**: `02_Submittals/`, `Docs/09_Registers/NN_<Name>/`, `Subcontractors/NN_Name/<Name>/`
- **Packages by stage**: 4 sheets (50%/90%/100%/IFC) + Legend
- **Do NOT put register Excel files inside `_MANAGER_DASHBOARD/`**

## Master Submittal Register

Consolidated single-file tracker for ALL subcontractor packages. One sheet per package + Dashboard summary.

- Location: `Docs/09_Registers/_Master_Submittal_Register/Master_Submittal_Register.xlsx`
- **Copied to every subcontractor's `_MANAGER_DASHBOARD/`** after each update
- Dashboard: item counts per stage, status (green/amber/red), lead times, contractor names

## Design Schedule Programme

Gantt-based timeline generated from Master Submittal Register data.

- Programme sheet: packages, item counts, placeholder submission windows (M1–M18)
- Gantt sheet: visual bars per stage (blue/green/amber/brown)
- Critical Path sheet: CRITICAL (MEP), LONG-LEAD (showcases 14wks), COORDINATION (AV), EXTERNAL (interactives)
- Dependencies sheet: predecessor/successor matrix

Saved alongside Master Submittal Register. Distributed to all subcontractor `_MANAGER_DASHBOARD/`.

## 09_Registers folder conventions

- **Index and Master files** get `_` prefix (sort before numbers): `_Master_Register_Index/`, `_Master_Submittal_Register/`
- **Real registers** get `01_` to `NN_` serial numbers: `01_Acoustic_Submittal_Register/`, `02_AV_Interface_Register/`
- No loose `.xlsx` files at the root — every register is a subfolder with the file inside
- No duplicate folders or files

## Long-lead item awareness

Check the project context (README, SCOPE_REQUESTs) for lead times BEFORE the user points them out:

| Package | Lead Time |
|---------|-----------|
| Showcases | 14 wks |
| MEP | 12-16 wks |
| Exhibition Fit-Out | 8-12 wks |
| FF&E | 8-12 wks |
| Interactives | 8-12 wks |
| Lighting | 5 wks (delivery) |

**Flag at 50% stage** — long-lead packages need more items approved earlier to trigger procurement.

## QC gate before delivery

Before presenting any register, SPEC.md, or programme to the user:

1. **Self-review**: Verify items against SOW/ER, check 50% package adequacy for long-lead items
2. **Sub-agent review**: Delegate to Kimi (QC), Claude (execution), or Codex (planning) via `delegate_task` with context showing the generator script
3. **Check**: Stage assignments correct? Long-lead items flagged? Descriptions exact SOW wording? Paths correct after renumbering?

See `sub-labor-orchestrator` for the full QA pipeline protocol.

### Reference file

`references/aseer-master-submittal-register-workflow.md` in `project-register-manager` skill — complete registry of packages, lead times, status, and key lessons from the June 2026 build-out of all 16 subcontractor registers.

---

## Domain: Submittal Register Creation (absorbed from `subcontractor-submittal-registers`)

The spec-first register workflow for creating 50%/90%/100%/IFC submittal registers for each subcontractor package.

### When to Use

The user asks to create, update, or review submittal registers for subcontractor packages on a D&B museum/cultural project with staged design delivery.

### SPEC.md → Register Workflow (Spec-First)

**Do NOT create the Excel register first.** Follow this order:

1. **Write SPEC.md** in `_MANAGER_DASHBOARD/SPEC.md` — defines scope, exclusions, deliverables by stage, standards, coordination interfaces, long-lead items
2. **Generate register** — the Excel submittal register is a **derived output** generated FROM the SPEC.md data
3. **Save to 3 locations**: `02_Submittals/<Name>_Submittal_Register/`, `Docs/09_Registers/<NN>_<Name>_Submittal_Register/`, `Subcontractors/<NN>_<Name>/<Name>_Submittal_Register/`

### SPEC.md Structure

```markdown
# SPEC — [Discipline Name]

**Package:** NN — [Name]  **SOW sections:** §...
**Lead time:** [from project context]

## 1. Scope
[exact scope from SOW — bullet list]

## 2. Exclusions
[items explicitly excluded per SOW]

## 3. Deliverables by Stage
### 50% Design — [5-10 items min; long-lead packages need more]
### 90% Design
### 100% Design
### IFC / AFC / Construction

## 4. Standards & Codes
## 5. Coordination Interfaces
## 6. Long-Lead Items
## 7. Quality Gates
```

### Stage Mask Rules

| Stage | Purpose | Min Items |
|-------|---------|-----------|
| **50%** | Surveys, concept, preliminary schedules, basis of design, design philosophy | 5-10 items. Long-lead packages: front-load structural design, material selection, lighting/AV integration |
| **90%** | Refined design, coordinated drawings, detailed schedules, specs, samples | — |
| **100%** | Final coordinated design, ready for IFC documentation | Complete all design items |
| **IFC/AFC** | Shop drawings, fabrication, prototypes, mock-ups, commissioning | — |

### SOW Section Mapping by Discipline

| Package | SOW Sections |
|---------|-------------|
| AV/IT | 6.22.2, 6.22.4(xiii), 8.9 |
| Exhibition Fit-Out | 6.22, 6.22.4(i–xviii), 8.2–8.7 |
| Graphics | 6.22.1, 6.22.4(viii–xi), 8.14 |
| Structural | 7.2, 7.3, 8.2, 8.3 |
| MEP | 7.1, 7.3, ER 3.2–3.5, 5.0 |
| Showcases | 6.22, 6.22.4(v–vi), 8.15 |

### Aseer Museum Document Numbering

Format: `MOC-MUS-ASE-<DISCIPLINE>-<TYPE>-<SEQ>`
- Discipline codes: 1A0=Arch, 1E0=Electrical+AV, 1K0=Multi, 1KH=HSE
- Document type codes (from BEP): MP=Plan, ZD=Drawing, PQ=Prequal., SC=Spec/Submittal, RG=Register, IR=Inspection, SH=Schedule

### Cross-Package Submittal Merging

When a deliverable spans multiple packages (e.g. rigging is its own package AND part of Structural's scope):
- Keep the standalone subcon folder (e.g. 06_Rigging) with its own register
- ALSO add rigging items to the parent package's register (e.g. 12_Structural) as a new category
- Update the parent SPEC.md scope section

### Master Submittal Register

Consolidated single-file tracker for ALL subcontractor packages. One sheet per package + Dashboard summary.
- Location: `Docs/09_Registers/_Master_Submittal_Register/Master_Submittal_Register.xlsx`
- Copied to every subcontractor's `_MANAGER_DASHBOARD/` after each update

### QC Gate

**Kimi = QC** for register tasks. Validate:
- Stage masks appropriate
- 50% package has enough items (not 1–2)
- Long-lead items identified and front-loaded
- Descriptions match SOW wording (verbatim, not paraphrase)
- References use only SOW § and ER § (no external sources)

---

## Domain: Procurement Info Packs (absorbed from `procurement-info-pack`)

Create purchasing information packs when the Technical Office needs to brief the Procurement Department on materials to source.

### Trigger

- A new subcontractor is engaged and material purchasing is needed
- IFC drawings depend on specific product data from suppliers
- A design direction requires new materials not yet sourced
- User says "prepare a folder for Purchasing Department"

### Standard Structure

```
Subcontractors/{NN}_{Trade}_Contractor/10_Purchasing/
├── Door_Hardware_Purchasing_Info.docx   # Main purchasing doc
├── 01_NRS_Specs/                         # Spec PDFs (if available)
├── 02_Datasheets/                        # Manufacturer datasheets
└── 03_Drawings/                          # Referenced drawings
```

### DOCX Template Sections

| Section | Content |
|---------|---------|
| Title | ITEM — PURCHASING INFORMATION |
| Subtitle | Prepared for Purchasing Dept · Source: spec refs · Rev X |
| 1. Summary | Quick table: brand specified?, finish, standards, source, fire rating, qty |
| 2. Specification Reference | Table of governing docs (NRS spec, ER, SOW, DMP, Div) |
| 3. Materials | Material-by-material with spec, qty, application |
| 4. Quantities | Summary table of estimated quantities |
| 5. Actions | Checklist of what Purchasing needs to do |

### Style Rules

- **Font:** Calibri throughout
- **Title:** 16pt Bold, Navy #1E293B, bottom border
- **Tables:** Navy header with white text, alternating rows, 8pt font
- **Note box:** Left red border, muted background
- **Footer:** Doc ref, Page X of Y, Samaya Investment Company

### Bilingual Mode (EN lead)

- English paragraph first, Arabic below (RTL, right-aligned)
- Table headers: `'ITEM / البند'`, `'QTY / الكمية'`
- Use `bilingual(doc, en_text, ar_text)` for paired content

### Vendor Quotation Comparison

Before purchasing, compare vendor quotations in an Excel workbook:

1. Collect all vendor quotation PDFs from Outlook attachments
2. Organize by product model (each product gets its own folder)
3. Extract pricing: hardware price, discount, VAT, total with VAT, delivery terms
4. Build Excel comparison with columns: Vendor, Contact, Model, Specs, Price (excl VAT), VAT, Total, Terms
5. Spec verification: cross-reference quotation specs against manufacturer brochures

## Post-quotation-review: submittal register update

After the quotation gap analysis confirms which scope items belong to this sub vs others, the submittal register must be updated to reflect the final scope split.

### When to do this

- The user confirms a scope split change (e.g., designer role changed from design+S&I to design-only)
- CG comments clarify deliverable ownership
- A quotation review reveals items quoted that belong to another sub

### Steps

1. **Identify items to remove** — walk each register line item against the confirmed split. Execution items (ITP, programming, spares, training, as-built production) typically go to the installer/contractor. BIM goes to the BIM specialist.

2. **Identify items to adjust** — items where the sub's role changed (e.g., "produces fabrication drawings" → "reviews fabrication drawings"; "performs focusing" → "directs focusing"). Update the description, not just the stage column.

3. **Update descriptions** — be precise: "ZNA reviews fabrication drawings — MEP Contractor produces" rather than just removing.

4. **Remove rows** — clear all columns (not just the reference number) so the row count is accurate.

5. **Update submittal counts** — the summary row at the bottom of each sheet must reflect the new item count.

6. **Update dashboard** — if a Master Submittal Register exists in `_MANAGER_DASHBOARD/`, update the counts (50%/90%/100%/IFC columns + total) for this sub's row.

7. **Update the Legend/Notes** — if the Legend sheet describes the scope split, update it to match (e.g., "Design only. BIM by [X]. Shop dwgs, install, commissioning execution by [Y].")

### Common scope split adjustments on museum fit-out

| Register Item | Designer → Stays? | → Moves to | New Description Pattern |
|---|---|---|---|
| Fabrication/shop drawings | ❌ Move | Contractor | "Review — Contractor produces" |
| ITPs | ❌ Move | Contractor | Remove from designer register |
| Control programming records | ❌ Move | Controls vendor | Remove from designer register |
| Spares/attic stock | ❌ Move | Contractor | Remove from designer register |
| Training | ❌ Move | Contractor | Remove from designer register |
| BIM model authoring | ❌ Move | BIM specialist | Remove from designer register |
| Light balancing/focusing report | ⚠️ Adjust | Designer directs | "Direction report — Contractor executes" |
| AFC documentation | ⚠️ Adjust | Designer certifies | "Design certification — Contractor compiles" |
| As-built | ⚠️ Adjust | Designer verifies | "Design verification — Contractor produces" |

## Reference files
- `references/aseer-purchasing-packs.md` — Aseer Museum purchasing pack examples (absorbed from `procurement-info-pack`)
- `references/docx-build-engine.md` — Samaya doc engine function reference (absorbed from `procurement-info-pack`)
- `references/appendix-b-packages.md` — Canonical subcontractor list (absorbed from `subcontractor-submittal-registers`)
- `references/zna-quotation-review-pattern.md` — Worked example: ZNA Studio lighting designer quotation review against ER/SOW/DMP, including email thread tracing, CG Code B handling, scope split clarification, and gap analysis
- `references/contract-drafting-pack.md` — Worked example: assembling the document pack for ZNA Studio contract drafting, including DMP sourcing from email, scope baseline rule, and who-owns-what cross-check
- `references/acoustic-prequalification-pattern.md` — Acoustic specialist prequalification with SOW + RACI matrix (worked example from CG rejection fix)
- `templates/gen_acoustic_prequal.py` — Reusable generation script for prequalification support documents with SOW, RACI, deliverables, and submission forms
---
