---
name: design-submission-packaging
category: project-management
description: How to analyze design drawings and package them into staggered submissions for CG/consultant review with appropriate review buffers
tags: [cg-submission, drawing-packaging, review-buffer, submission-plan, consultant-review, bod-audit, scope-verification, submission-register]
trigger: user asks how to package or submit design drawings for CG/consultant review, or asks to create/update a discipline submission register
version: "1.2"
---

# Design Submission Packaging for CG/Consultant Review

How to analyze a batch of design drawings and package them into staggered submissions for CG (Consultant Group) review, with appropriate review buffers. Also covers creating discipline submission registers from scratch.

## Trigger Conditions

Use this skill when:
- A batch of design drawings (DD, IFC, SD) has been received from a design consultant (NRS, ADENG, GH, etc.)
- User asks "how to submit" or "how to package" drawings for CG approval
- User asks about floor-by-floor vs type-by-type submission
- User needs a submission calendar aligned with a project deadline
- User asks to create or update a discipline submission register
- User asks to audit a submission plan against a BOD/SOW document

## Workflow

### Step 1: Inventory the Drawing Set

Extract the drawing register from the Document Issue Sheet (DIS) or cover document:

```sql
# If DIS is a PDF:
pdftotext -raw "DIS-xx.pdf" - 2>/dev/null | grep "^MOC-" > /tmp/drawing_list.txt
```

Key fields to capture per drawing:
- Drawing number (e.g. MOC-ASE-AR-ARC-XXXX-DDD-NNNN)
- Title
- Floor (BF, LGF, GF, 1F, 2F)
- Sheet size
- Scale

### Step 2: Determine Packaging Strategy

**Test floor-by-floor viability first:**

For each floor, list which drawings apply exclusively to that floor vs cross-floor:

| Drawing Type | Test | Verdict if cross-floor |
|-------------|------|----------------------|
| GA Plans | One sheet per floor ✅ | Can split by floor |
| Sections | Single sheet cuts through ALL floors ❌ | Cannot split — duplicate across packages |
| Elevations | Each elevation is one room, but rooms span floors ❌ | Mixed-floor sheets |
| Details | Gallery G1=BF, G8=LGF, G3=GF on same sheet series ❌ | Gallery locations are per-gallery, not per-floor |
| Schedules | All doors/rooms in one schedule ❌ | Cannot split |
| Visuals | Overall views showing multiple floors ❌ | Cannot split |

**Floor-by-floor fails when ≥30% of drawings are cross-floor.**  
In that case, use **Type-Based Packaging**.

### Step 3: Design Packages by Drawing Type

Group drawings by **functional type** (not floor):

| Package | Contents | Typical Size | Complexity |
|---------|----------|:------------:|:----------:|
| **A: Basement Priority** | Existing plans, demolition plans, basement-specific plans/sections | 35-50 dwgs | Medium |
| **B: Core Plans** | Proposed GA plans, wall/floor/ceiling scoping (all floors), sections | 30-40 dwgs | Low-Medium |
| **C: Elevations + Stairs** | Room elevations, stair details, external details | 40-50 dwgs | Medium |
| **D: Setworks + Furniture** | Gallery setwork details, showcase coordination, furniture | 55-70 dwgs | High |
| **E: Details + Schedules + Visuals** | Finishing details, schedules, door types, 3D visuals | 45-60 dwgs | Low |

**Basement-first rule** per Elbaz/CG: Package A should contain all basement-specific drawings.

### Step 4: Calculate Review Buffers

Apply buffer per package complexity:

| Complexity | Samaya Review | CG Review | Resubmission Cycle |
|:----------:|:------------:|:---------:|:------------------:|
| Low | 2 WD | 10 WD | N/A |
| Medium | 3 WD | 14 WD | 7 WD |
| High | 5-7 WD | 14-21 WD | 10 WD |

**Stagger packages** 3-5 working days apart so CG reviewers aren't overwhelmed.

### Step 5: Validate Against Deadline

For each package, calculate:
```
Samaya Review Start → Samaya Submit to CG → CG Review Complete → (If B/C: Resubmit → Re-review)
```

Check if the last package clears CG approval before the project deadline (e.g. Elbaz's 21 Aug).

### Step 6: Audit Against Scope Documents Before Editing

**CRITICAL WORKFLOW — do not skip:**

Before creating or editing a submission register, audit the scope against the project's governing documents:

1. **Identify the scope document** — BOD (Basis of Design), SOW (Scope of Work), or Design Philosophy report. Each discipline typically has one.
2. **Extract the scope items** — read the document's scope section (often Section 1.2 or similar). List every numbered scope item.
3. **Map scope items to submission packages** — create a side-by-side comparison: scope item # → proposed package # → description → match/mismatch.
4. **Present the audit verdict to the user first** — show the comparison, flag any mismatches (extra items not in scope, missing items from scope).
5. **Wait for user confirmation** before editing the file. Do not act on second-hand information (e.g., "the engineer said X") without auditing against the source document first.
6. **Only after user says "update"** — edit the register.

**Pitfall — acting on unverified information:** If someone (engineer, consultant, colleague) sends a short list or message about scope, do NOT edit the register based on that alone. Audit against the actual scope document first, present findings, and let the user decide. The user's instruction is: "audit his msg 1st before we edit the file."

### Step 7: Build the Submission Register

Use the project's standard template format. For Aseer Museum, the MEP template uses:

**13 columns:** Gate | Level/Zone | Discipline | Submission Category | Drawing Package/Item | Submission Description | Responsibility | Planned Submission Date | Review Duration (Days) | Approval Authority | Linked Activity ID (Program) | Status | Remarks

**3 gates:**
- Gate 1 — Detailed Design (all design deliverables)
- Gate 2 — Material Approval (material submittals)
- Gate 3 — Coordinated IFC (construction issue packages)

**Approval Authority:** Always "CG" for Aseer Museum (unless user explicitly overrides for a specific item). Do not default to "Consultant / PMC" — the user's standing instruction is CG for all disciplines.

**Responsibility label:** Per CG comment #8 on MOC-MUS-ASE-MEP-ZD-0068, replace "Consultant" with "MEP Designer Office" in the Responsibility column. Do not use "Consultant" as a responsibility label.

**CG-requested additional deliverables (from PDF review MOC-MUS-ASE-MEP-ZD-0068):**
When CG comments reference a review PDF, check for these additional items to add to the plan:
- Site Assessment & Survey Report (per CG comment #5, #14)
- MEP Design Risk Management Report (per CG comment #17)
- MEP Value Engineering Study (per CG comment #17)
- Concept Design Review & Gap Analysis Report (per CG comment #10)
- Existing As-Built Drawing Survey (per CG comment #5)
- RACI Matrix for interface parties (per CG comment #4)

**Do NOT include completed/submitted items** in a forward-looking submission plan unless they are active design submissions (like BOD/Loading Plans) that serve as prerequisites for subsequent items. Historical deliverables (as-built drawings, previous studies, existing reports) belong in a separate reference document, not the submission register.

### Step 8: Sequence Deliverables Logically

For structural design, the correct sequence (per BOD Section 1.2) is:

1. Review existing structural drawings and as-built conditions
2. Establish 3D ETABS model for existing building
3. Analyze existing building under gravity and lateral loads
4. Establish 3D ETABS model for modified building
5. Analyze modified building under gravity and lateral loads
6. Verify capacity of existing members + design strengthening
7. Prepare comprehensive engineering report

Each item depends on the previous. Do not reorder or skip.

### Step 9: Document the Plan

Create a submission plan Excel with:
- Package ID + name
- Drawing count + list
- Samaya review start/end dates
- CG submission date
- CG review period
- Expected CG response date
- Risk/status (✅ on track / ⚠️ tight / ❌ miss)

## Key Design Decisions & Patterns

### Approval Authority Default

For Aseer Museum, all disciplines: **CG** always. Never "Consultant / PMC". The user corrects this every time it's wrong.

### Responsibility Mapping (Aseer Museum)

| Work Type | Party | Notes |
|-----------|-------|-------|
| Detailed Design (MEP) | AD (MEP Designer Office) | Per CG #8, never "Consultant" |
| Coordinated IFC | Samaya | IFC packages issued by Main Contractor |
| LOD 300/350/400 Models | Samaya | Coordination models by Samaya |
| Existing Systems Survey | Namaa | Survey subcontractor |
| Lighting Design | ZNA (Lighting Designer) | Not AD |
| AV Design | RAWASIN | AV specialist |
| BMS / ICT | BMS/ICT Integrator | Combined scope, same entity |

### CG Comment Audit Workflow

When a CG review PDF arrives (e.g., MOC-MUS-ASE-MEP-ZD-0068):

1. Extract all numbered comments (use pdfplumber)
2. Categorize: 🔴 Critical / 🟡 Important / 🟢 Minor
3. Audit each comment against DMP / SOW / best practice
4. Present verdict table: ✅ justified / ❌ unjustified / ⚠️ needs clarification
5. Identify missing deliverables and add them to the plan
6. Do not skip this step — CG comments drive plan revisions

**Standard CG-requested deliverables to check for:**
- Existing Systems Survey & Site Assessment Report (#5, #14)
- Concept Design Review & Discrepancy Report (#10)
- MEP Design Risk Register (#17)
- MEP Value Engineering Study (#17)
- RACI Matrix for MEP/BMS/ICT/AV interfaces (#4)
- Design Conflict Resolution (e.g. Gallery G6 beams vs HVAC) (#15)
- LOD 350 Above-Ceiling Coordination note (#12)

### RACI Matrix Pattern

CG Comment #4 requirement. Internal coordination tool — no CG/Client column.

**Parties** (Aseer Museum): Samaya (Coordinator), AD (MEP Designer), ZNA (Lighting Designer), RAWASIN (AV/Specialist), BMS/ICT (combined), Namaa (Survey)

**Structure:** 10+ categories (Design Coordination, LOD Coordination, Power & Containment, Lighting Systems, AV Systems, BMS/ICT Integration, Fire & Life Safety, Existing Survey, Testing & Commissioning, Documentation & Handover), 50+ interface items. Color coding: R=green, A=red, C=blue, I=grey.

### Excel Technical Patterns

**Safe merged-cell writing:**
```python
def safe_set_cell(ws, row, col, value):
    cell = ws.cell(row=row, column=col)
    for merged_range in ws.merged_cells.ranges:
        if cell.coordinate in merged_range:
            ws.cell(row=merged_range.min_row, column=merged_range.min_col).value = value
            return
    cell.value = value
```

**Date standardization:** Convert `datetime.datetime`/`datetime.date` objects to `DD/MM/YYYY` strings before writing. Downstream tools fail on datetime objects.

**File separation:** One discipline per file. Never bundle Architecture + Mechanical in one Excel file.

**IFC reference uniqueness:** Each floor gets a unique IFC ref (e.g., `ME-300001-BF-IFC`, not shared `ME-300001-IFC`).

### Building a Submission Plan from Template

1. Copy AV template format (13 columns: Gate, Level/Zone, Discipline, Submission Category, Drawing Package/Item, Submission Description, Responsibility, Planned Submission Date, Review Duration (Days), Approval Authority, Linked Activity ID, Status, Remarks)
2. Replace all Approval Authority → CG
3. Map responsibilities per table above
4. Convert all dates to DD/MM/YYYY strings
5. Fill missing IFC data (14 days review, CG, Samaya)
6. Run verification: zero non-CG cells, no datetime objects
7. Open file for user review

## Pitfalls

- **Floor packaging trap**: Just because drawings cover a single floor doesn't mean the package works. Cross-discipline coordination sections and elevations will be duplicated or orphaned.
- **Review buffer underestimation**: CG teams of 5-7 reviewers cannot process 18 concurrent submissions. A stagger of minimum 3 WD between packages is essential.
- **Deadline trap**: The deadline (Elbaz 21 Aug) is for **approval**, not submission. Account for CG review time + possible Code B/C resubmission.
- **Document number confusion**: DIS cover sheets may list drawings by short code (e.g. "100 BF CEILING-DEMOLISH") rather than MOC-MUS-ASE codes. Match by title+floor, not by document number alone.
- **Overlapping row check**: Before adding new items to a submission plan, check existing rows for the same discipline. The plan may already have an umbrella row (e.g. "Architectural design drawings") that covers what you're adding. Add as sub-items or update the existing row rather than creating duplicate parallel entries.
- **Comprehensive discipline sweep**: When updating a multi-discipline document, verify EVERY discipline was reviewed and updated — not just the ones with obvious new data. The user will check: "did you update all?" and expects a complete sweep, not a partial update. Generate a per-discipline status summary to prove completeness.
- **Don't include completed items**: A submission plan shows pending deliverables. Historical/completed items confuse the reader and dilute the plan. Exception: active design submissions (BOD, Loading Plans) that are prerequisites for later items — these can appear with status=Submitted.
- **Don't act on unverified information**: Always audit against the source scope document before editing. Present verdict, wait for confirmation.
- **Don't reorder scope items**: The BOD/SOW defines the logical sequence. Follow it exactly.
- **Don't add items not in scope**: Serviceability checks, foundation assessments, stability evaluations — if not in the BOD scope, don't add them unless the user explicitly requests them.
- **Date assumption trap**: Never assume dates (e.g., "submitted on June 26"). Always confirm with the user or the source document. If the user says "we start tomorrow," use that as the baseline.
- **Missing BOD/SOW for a discipline**: If no BOD/SOW exists for a discipline (e.g., AV), use the existing register items as a starting point, but flag to the user that no scope document was found and ask them to verify with the discipline engineer.
- **Approval Authority default**: For Aseer Museum, the standing instruction is **CG** for all disciplines. Do NOT default to "Consultant / PMC" — the user will correct this every time. Apply CG to every data row in the Approval Authority column.
- **Responsibility mapping (Aseer Museum)**: Detailed Design → "AD (MEP Designer Office)" (per CG comment #8, never "Consultant"). Coordinated IFC → "Samaya". Existing systems survey → "Namaa". Verify these mappings before populating.
- **IFC reference uniqueness**: CG rejects generic IFC refs shared across floors (e.g., `ME-300001-IFC` used for all 6 floors). Each floor must have a unique reference (e.g., `ME-300001-BF-IFC`, `ME-300001-LGF-IFC`). Always generate per-floor unique codes.
- **Merged cell handling in Excel**: When writing to Excel files that may have merged cells, use a `safe_set_cell(ws, row, col, value)` function that checks if the target cell is part of a merged range and writes to the top-left cell instead. Direct assignment to a merged cell raises `AttributeError: 'MergedCell' object attribute 'value' is read-only`.
- **Date format standardization**: Excel `datetime` objects in cells cause issues with string-based downstream processing. Convert all dates to `DD/MM/YYYY` string format before writing. Check for `datetime.datetime` and `datetime.date` instances.
- **File separation per discipline**: Do not put multiple disciplines in one Excel file. Each discipline gets its own file (e.g., `Mechanical_Submittal_Plan.xlsx`, `Architecture_Submittal_Plan.xlsx`). The user will reject combined files.
- **CG comment audit workflow**: When a CG review PDF arrives (e.g., MOC-MUS-ASE-MEP-ZD-0068), extract all numbered comments, categorize by priority (Critical/Important/Minor), audit each against DMP/SOW/best practice, and present a verdict table. Then identify missing deliverables and add them to the plan. Do not skip this step — CG comments are the primary driver of plan revisions.
- **RACI Matrix as a deliverable**: CG Comment #4 requires a RACI matrix for MEP/BMS/ICT/AV interfaces. This is a standalone deliverable (not just a line item). Create it as a separate Excel file with 47+ interface items across 8 categories (Design Coordination, Power & Containment, BMS Integration, ICT & Telecom, AV Systems, Fire & Life Safety, Testing & Commissioning, Documentation & Handover). Map 9 parties: AD, Samaya, ZNA, RAWASIN, BMS Specialist, ICT Integrator, AV Specialist, Namaa, CG. Use color coding: R=green, A=red, C=blue, I=grey.

### Step 10: Communicate the Submission Plan

When sending the submission plan to CG/consultant via email, follow these rules:

**Discipline grouping rules (Aseer Museum):**
- **MEP** = Mechanical + Electrical + Plumbing bundled as one package. Never list Electrical as a separate discipline.
- **Excluded from standard design submission plan updates:** FFE, Model Maker, Oddy Testing — these follow separate procurement/specialty tracks. Do not include them unless the user explicitly asks.
- **Remaining disciplines to list separately:** Acoustic, AV, CITC/Telecom, Fire Life Safety (FLS), Graphics, Interactives, Landscaping, Lighting, QA/Commissioning/Handover, Showcase.

**Email structure:**
1. Acknowledge the request/reminder
2. State what's attached now (Arch + Struct + AV plans)
3. State what's coming next (MEP, Lighting — with ETA and "coordinating with specialist" caveat)
4. List remaining disciplines with the phrase: "under preparation and coordination with the project team and specialists, and will be submitted progressively"
5. Reference the Master Submission Plan and deadline alignment
6. Apologize for any delay and reaffirm commitment to the agreed timeframe

**Pitfall — discipline grouping:** Do not list Electrical as a standalone item if MEP covers it. The user will correct this. Similarly, do not include FFE/Model Maker/Oddy Testing in the "remaining disciplines" list unless the user explicitly adds them. When in doubt, ask the user to confirm the discipline list before sending.

**Pitfall — "(including Electrical)" after MEP:** Never add "(including Electrical)" in parentheses after MEP. The user considers MEP to inherently include Electrical. Writing it out implies it doesn't, and they will correct you.

**Pitfall — Graphics and Showcase:** Graphics may be "not yet approved" and Showcase may be handled separately. Confirm with the user before including either in the "remaining disciplines" list sent to CG.

**Pitfall — Accessibility plans go at 90% gate, not DD:** For museum/public building projects, accessibility & universal design compliance plans (SBC 201) belong at the 90% detailed development gate, not the 50% DD gate. The spatial layout must be finalized first, then the accessibility overlay is applied. Add a Gate 1.5 (90% Detailed Development) section between Gate 1 (DD) and Gate 2 (Material Approval) in the submission plan.

See `references/submission-plan-email-template.md` for a reusable template.

## Related

- `references/aconex-upload-workflow.md` — How to create Transmittals and set Review Workflows in Aconex for each package
- `references/cg-review-buffer-reference.md` — Standard CG review periods by document type on Aseer Museum
- `references/bod-scope-audit-pattern.md` — How to audit a submission plan against a BOD/SOW document
- `references/submission-plan-email-template.md` — Reusable email template for communicating submission plan status to CG/consultant

## References

See `references/` for:
- Drawing packaging analysis examples
- Review buffer calculations per discipline
- CG response code definitions (A/B/C/D)
- BOD scope audit examples
- Submission plan email template
