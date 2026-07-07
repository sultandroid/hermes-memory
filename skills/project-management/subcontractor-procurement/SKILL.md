---
name: subcontractor-procurement
description: Generate RFPs from technical proposals, audit against project requirements, and check cross-subcontractor scope conflicts. Covers RFP generation, conflict audit, SPEC.md update, and deliverable deployment.
version: 1.1.0
author: Hermes Agent
license: MIT
platforms: [macos]
metadata:
  hermes:
    tags: [rfp, procurement, subcontractor, conflict-audit, scope]
    related_skills: [project-register-manager, samaya-technical-office, design-change-control]
---

# Subcontractor Procurement Workflow

## Overview
Generate RFPs from received technical proposals, audit against project SOW/ER requirements, and check cross-subcontractor scope conflicts before award.

## Workflow

### Step 0: Find Governing Design Documents FIRST
Before generating any subcontractor scope document (SOW, SPEC, or RFP):
1. **Search the project's design files** — look in `03_Design_Files/` and subcontractor `02_Reference_Drawings/` for the governing design report (e.g. iAcoustics Acoustic Design Strategy, NRS Materials Spec, ER extracts, Pre-Appointment design packs)
2. **Read the design intent** — extract treatment types, performance targets (NRC, RT60, NR), product classes (Class A/B/C), and product names specified by the designer
3. **Cross-reference with BOQ** — map design intent to BOQ finish codes
4. **Only then read vendor proposals** — vendor products (TOS, BoSpray, BoCoustic, etc.) are for RFP comparison/compliance checking, NOT for SOW scope definition

**Critical rule:** The SOW must reference only contract documents (ER, SOW, governing design reports, iAcoustics strategy). Vendor proposal products NEVER appear in a SOW document. They belong in:
- RFP Compliance Matrix (as proposed alternatives)
- Submittal Register (once approved)
- Conflict audit (as proposed vs design intent comparison)

### Step 1: Extract Source Data
1. **Read technical proposals** — use `pdftotext -layout` for PDFs (handles binary/encoded PDFs better than `pdfgrep`)
2. **Read ceiling finishes/quotation PDFs** — same method
3. **Extract key data**:
   - BOQ items (ref, description, quantity, unit rate)
   - Product specifications (NRC, fire rating, thickness)
   - Acoustic targets (RT60, NR per space)
   - Programme duration
   - Commercial terms

### Step 2: Generate RFP Excel
Create a 7-sheet workbook:

| Sheet | Content |
|---|---|
| **Cover** | Project info, RFP ref, submission deadline, site visit date |
| **RFP Overview** | Background, scope, design responsibility, key requirements, submission requirements, evaluation criteria, commercial terms |
| **Technical Specs** | BOQ items with NRC targets, fire ratings, proposed products |
| **BOQ** | Quantities, unit rates TBD for bidder pricing |
| **Compliance Matrix** | Proposed products vs spec requirements — colour-code: green=exceeds, blue=equivalent, red=fails |
| **Submission Requirements** | Deliverables checklist (D1–D10) with format requirements |
| **Evaluation Criteria** | Sub-criteria across categories (Tech 40%, Commercial 30%, Programme 15%, Local Content 10%, HSE 5%) |

**Formatting rules:**
- Dark blue headers (`#1F4E79`), alternating row colours
- Auto-filter on all data sheets
- Frozen panes on header row
- Compliance status colour-coded
- Bidder pricing columns left as TBD

### Step 3: Cross-Subcontractor Conflict Audit
Before finalizing any RFP, audit against ALL other subcontractors for scope conflicts:

**Subcontractors to check:**
1. MEP Contractor — duct silencers, sprinkler integration, MEP noise criteria
2. MEP Designer — noise control specs, ceiling void coordination
3. Lighting Designer — fixture integration in ceilings
4. AV/IT Contractor — ceiling speakers, cut-out coordination
5. FLS Specialist — PAVA speakers, fire detectors in acoustic ceilings
6. Structural Contractor — suspension loading, slab anchors
7. CITC/BMS-ICT — WAP mounting in acoustic ceilings
8. Showcases Contractor — floor-to-ceiling case interfaces
9. Rigging Contractor — suspension point overlap
10. Exhibition Fit-Out — wall-ceiling junction coordination

**Audit methodology:**
1. Read scope documents (SCOPE_REQUEST.md, SOW files, SPEC.md) for each subcontractor
2. Search for references to the RFP's scope items (e.g., acoustic ceilings, baffles, spray, plaster)
3. Identify conflicts by category:
   - **Scope overlap** — two subcontractors claiming the same work
   - **Scope gap** — work not assigned to anyone
   - **Interface conflict** — two scopes that must coordinate but haven't
   - **Timing risk** — dependency on unappointed consultant
4. Rate severity: High (blocks award), Medium (needs resolution before IFC), Low (manageable with standard detailing)

**Output format:**
```markdown
### C-NN | Subcontractor Name — Issue Title
| Field | Detail |
|-------|--------|
| **Subcontractor** | NN_Subcontractor_Name |
| **Issue** | Description of the conflict |
| **Severity** | 🔴 High / 🟡 Medium / 🟢 Low |
| **Recommended Resolution** | Specific action to resolve |
```

### Step 4: Update SPEC.md
After RFP generation and conflict audit:
1. Update SPEC.md header with RFP ref, submission deadline, current status
2. Replace generic scope with specific BOQ items and design intent treatments
3. Add exclusions based on conflict audit findings
4. Add key performance targets table (NRC, fire rating, absorption class) — use design intent targets, not vendor product specs

### Step 5: Deploy Deliverables
1. Copy RFP Excel to `_MANAGER_DASHBOARD/`
2. Copy source proposals to `08_RFP_and_Proposals/`
3. Save conflict audit to `_MANAGER_DASHBOARD/ACOUSTIC_CEILING_CONFLICT_AUDIT.md`
4. Create `08_RFP_and_Proposals/` folder if it doesn't exist

### Step 6: Proposal Compliance Audit (Vendor Proposals vs SOW)

After receiving vendor proposals and before award, audit each proposal against the SOW / governing design report.

**Audit categories:**
1. **Scope compliance** - Does the proposal cover all assessment, design, commissioning items from the SOW?
2. **Product compliance** - Do proposed products meet or exceed design intent treatment classes (NRC targets, fire ratings)?
3. **Treatment coverage by space** - Does each gallery/space have the correct treatment type per the governing design report (iAcoustics, NRS)?
4. **Programme compliance** - Does the proposal timeline match the SOW programme milestones?
5. **Deliverables compliance** - Does the proposal cover all AC-001 to AC-021 deliverables?
6. **Prequalification compliance** - Are certifications, experience, capabilities verified?

**Critical rules:**
- SOW defines the baseline (contract scope). Vendor proposals are alternatives evaluated against it.
- Design intent product names (Sonaspray, Sonacoustic, Knauf) are the reference. Vendor products are proposed equivalents.
- Where vendor product differs from design intent (e.g. 25mm spray vs 15mm spray), flag as "needs approved-equal" - not non-compliant.
- Programme gaps: if vendor proposes shorter timeline than SOW, flag as high severity.
- Deliverable gaps: if proposal covers 7 of 21 SOW deliverables, scope-related gap - ask vendor to expand.

**Save audit to:** `_MANAGER_DASHBOARD/PROPOSAL_COMPLIANCE_AUDIT.md`

## Document Style Rules (Mandatory for ALL generated documents)

1. **No Section symbol** — use "Section" or "Clause" (e.g. "ER Section 3.5" not "ER Section 3.5")
2. **No AI marketing phrases** — NEVER use: delve, leverage, robust, seamless, cutting-edge, state-of-the-art, pinnacle, testament to, elevate your environment, seamless integration, seamless finish
3. **Plain construction English** — write like a project PM, not a brochure. Direct, factual, specific.
4. **No rewrites of others' quotes** — never rewrite NRS/CG/iAcoustics quotes as your own words. If quoting, use quotes.
5. **DOCX table widths** — always set explicit column widths. Never auto-fit.
6. **No special Unicode chars** — replace: en-dash (-) with hyphen (-), middot () with hyphen/comma, em-dash (--) with double hyphen (--), right arrow (->) with "->", greater-or-equal (>=) with ">=", superscript (²) with "2"
7. **No AI footprint phrases** — avoid: "as per", "in accordance with", "please find attached", "kindly", "I trust this meets your expectations", "we are pleased to submit", "valued feedback", "sincerely appreciate", "look forward to", "remains fully available"
8. **Numbers and codes stay original** — drawing codes, standards references, product names keep their original formatting

## SOW Content Rules (Added 2026-07-03)

1. **SOW references only contract documents**: ER, SOW, governing design reports (iAcoustics Acoustic Design Strategy, NRS Materials Spec, etc.). Never vendor proposals.
2. **Design intent language**: Use treatment types and absorption classes from the design report (e.g. "Class B acoustic spray (Sonaspray 15mm)", "Class A acoustic ceiling (Sonacoustic)"). Not vendor product names.
3. **Treatment options table**: Include a per-space table showing target RT, NR, and treatment options per the governing design report. This is the contract scope baseline.
4. **Performance targets by class**: NRC >= 0.80 for Class B, >= 0.90 for Class A. Not specific vendor NRC values.
5. **Vendor proposals go in the RFP only**: The RFP Compliance Matrix is where proposed products (BoSpray, BoCoustic, etc.) are compared against design intent. Not in the SOW.
6. **Always read the governing design report first**: The iAcoustics Strategy V2, NRS Materials Spec, and Pre-Appointment Exhibition Documentation are the authority. Vendor proposals are secondary.

## Pitfalls

### PDF text extraction
- `pdfgrep` fails on binary/encoded PDFs — use `pdftotext -layout` instead
- Large PDFs (>10 MB) may need chunked reading via `offset`/`limit`
- Some PDFs have embedded fonts that cause `Syntax Warning: Invalid Font Weight` — ignore these, text still extracts

### RFP generation
- Always leave unit rates as TBD for bidder pricing — never populate with received quotation rates
- Submission deadline should be 14 days from issue date (standard)
- Evaluation criteria weights must total 100%
- Include a site visit date (7 days from issue)

### Conflict audit
- Check ALL subcontractors, not just the obvious ones
- FLS/PAVA is often missed — PAVA speakers and fire detectors cannot mount in fabric or seamless acoustic ceilings
- MEP ceiling void coordination is critical for spray-on and seamless finishes (no void for services)
- Structural suspension responsibility is frequently ambiguous between acoustic and rigging contractors
- Always check if the specialist consultant is appointed — if not, flag as high-severity timing risk

### SPEC.md updates
- Keep the original scope sections (50%/90%/100%/IFC deliverables) — only update the header and scope description
- Exclusions must be explicit and reference the responsible subcontractor
- Add RFP ref and deadline to the header for traceability

### SOW generation (added 2026-07-03)
- **CRITICAL**: Never use vendor product names in a SOW document. The SOW defines the contract scope, not the contractor's proposed solution.
- The governing design report (iAcoustics, NRS) is the source of truth for treatment types and classes, not the TOS or any other vendor proposal.
- Treatment options table must include RT targets, NR criteria, and specific treatment types per space — this is the baseline against which equivalent products are evaluated.
- If the user corrects you on SOW content, it means you used vendor data instead of governing design data. Fix by reading the design report and rewriting.

## Tender Package Creation (from Project Scope)

### When to Use
- User asks to create a complete tender package for a project from scratch (not from a vendor proposal)
- You have an items status sheet, BOQ, or scope list and need to build structured tender documents
- The project is a fit-out / exhibition / museum with multiple zones and trade packages

### Workflow

#### Step 1: Survey Existing Project Files
Before creating anything, inventory what exists:
- **Items Status sheet** — the primary source for scope items (location, item, supplier, status)
- **Drawings** — list all available PDF/DWG/RVT files in `Revit Files/Detail Drawings/`
- **Specifications** — check `Specs & Datasheet/GENERAL SPECIFICATIONS/` for MasterFormat divisions
- **Revit models** — for quantity take-off reference
- **Email archive** — for procurement history, supplier contacts

#### Step 2: Extract Items from Status Sheet
Read the existing Items Status Excel to extract:
- Item number, location/zone, description, supplier, action status
- Group items by zone (Reception, Hall 1, Madinah, Media, etc.)
- Note which items are already contracted vs pending

#### Step 3: Create Tender Package (7 files)

| # | File | Description |
|---|---|---|
| 1 | `BOQ.xlsx` | Bill of Quantities with items by zone, unit rates column (TBD), grand total |
| 2 | `Pricing_Schedule.xlsx` | Fillable pricing template with VAT summary section |
| 3 | `Scope_of_Work.md` | Detailed SOW by zone + exclusions + contractor responsibilities |
| 4 | `Tender_Drawings_List.md` | All available drawings indexed with format, sheet ref, status |
| 5 | `Technical_Specifications_Index.md` | Applicable MasterFormat divisions mapped to existing spec docs |
| 6 | `Tender_Conditions.md` | Instructions to tenderers: submission, pricing, evaluation, bonds |
| 7 | `Tender_Form.md` | Letter of Tender template with declarations |

#### Step 4: BOQ.xlsx Formatting (openpyxl)
```python
from openpyxl.styles import Font, Alignment, Border, Side, PatternFill

hdr_font = Font(name='Calibri', bold=True, size=11, color='FFFFFF')
hdr_fill = PatternFill(start_color='1F3864', end_color='1F3864', fill_type='solid')
cell_font = Font(name='Calibri', size=10)
thin_border = Border(
    left=Side(style='thin'), right=Side(style='thin'),
    top=Side(style='thin'), bottom=Side(style='thin')
)
total_fill = PatternFill(start_color='FFD700', end_color='FFD700', fill_type='solid')

# Headers: Item #, Location, Description, Unit, Qty, Unit Rate (SAR), Total (SAR)
# Grand total row: merge C:E, "GRAND TOTAL" with gold fill
# Notes sheet: BOQ notes (currency, VAT, quantities verification)
```

**Column widths:** A=8, B=20, C=50, D=14, E=10, F=16, G=16

#### Step 5: Scope_of_Work.md Structure
- **Project Overview** — one paragraph
- **Scope Breakdown by Zone** — each zone as a subsection with bullet items
- **Exclusions** — what's NOT in scope
- **Contractor Responsibilities** — site verification, shop drawings, samples, coordination, as-built, defects liability

#### Step 6: Tender_Drawings_List.md Structure
Table with columns: #, Drawing Title, Format, Sheet Ref, Status
Include Revit model files and as-built CAD as reference documents

#### Step 7: Technical_Specifications_Index.md
List all available MasterFormat divisions from the project's `Specs & Datasheet/GENERAL SPECIFICATIONS/` folder.
Highlight key applicable sections for the tender (e.g., Division 06 Wood/Plastic, Division 08 Openings, Division 09 Finishes, Division 12 Furnishings, Division 26 Electrical, Division 27 Communications).

#### Step 8: Tender_Conditions.md
Sections: Tender Submission, Tender Documents, Pricing Instructions, Qualification Requirements, Evaluation Criteria, General Conditions

#### Step 9: Tender_Form.md
Letter of Tender template with: total price fields (excl. VAT, VAT, incl. VAT), declarations, tenderer info table (name, CR, ZATCA, contact, signature, stamp, date)

### Pitfalls
- **"Tinder" vs "Tender"**: The user may type "Tinder Doc" as a folder name — clarify before populating
- **Items Status sheet is the source**: Read the existing status sheet first — it contains the actual project scope items, not a formal BOQ
- **BOQ rates are TBD**: Leave unit rate columns blank for the tenderer to fill — do NOT populate with estimated rates
- **Zone grouping**: Group items by physical zone (Reception, Hall 1, Madinah, etc.) not by trade — this matches how contractors price fit-out work
- **Specs index**: Only list divisions that actually exist in the project's specs folder — don't fabricate spec references
- **Drawings list**: Include the Revit model as a reference even if it's not a formal tender drawing — contractors need it for quantity take-off
- **OneDrive path**: Save files directly to the OneDrive-synced Tinder Doc/ folder — do NOT use /tmp/ and copy (OneDrive syncs automatically)
- **NEVER generate new files**: The tender package must consist ONLY of copies of existing project documents (Items Status, drawings, specs, submittals, cost estimates). Do NOT create BOQ.xlsx, SOW.md, Tender_Conditions.md, or any other new document from scratch. The user will correct you if you do.
- **Organize with numbered folders**: After copying files, organize them into `01_BOQ/`, `02_Drawings/`, `03_Specifications/`, `04_Submittals/`, `05_Cost_Estimate/` (or similar numbered categories). Flat file dumps in the root of Tinder Doc/ will be rejected as unorganized.
- **Fix double-nesting**: When moving folders like `Specifications/` or `Submittals/` into numbered folders, check for `03_Specifications/Specifications/` double-nesting and flatten it.

## Related Skills
- `project-register-manager` — for register creation and management
- `samaya-technical-office` — project context, folder structure, document conventions
- `design-change-control` — for backup report generation (DCR format)
- `subcontractor-folder-setup` — for initial folder scaffolding
- `rfp-generation` — for RFP Excel generation from proposals