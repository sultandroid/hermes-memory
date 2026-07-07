# RACI-Driven Scope Realignment Workflow

When CG Comment #4 or a project-wide RACI matrix triggers scope realignment across multiple subcontractors, use this workflow to update all scopes consistently.

## Trigger

- CG returns a submittal with Code C (Revise & Resubmit) and Comment #4: "RACI matrix between specialists required"
- A RACI matrix is approved by CG/Samaya defining R/A/C/I for each interface item
- Multiple subcontractor scopes need simultaneous realignment to match the RACI

## Workflow

### 1. Read the RACI matrix

Extract all rows from the approved RACI Excel. For each row, identify:
- **Interface activity** (e.g., "BMS integration with lighting control")
- **RACI assignments** per party (Samaya, AD, ZNA, RAWASIN, BMS/ICT, Namaa, etc.)

### 2. For each subcontractor, extract their R/A rows

Filter the RACI to show only items where the sub is:
- **R (Responsible)** — they do the work
- **A (Accountable)** — they answer for it (usually Samaya)
- **C (Consulted)** — they provide input
- **I (Informed)** — they're notified

### 3. Compare against current scope document

For each sub's current SCOPE_REQUEST.md, check:

| Check | What to look for |
|-------|-----------------|
| **Items to REMOVE** | Scope items where the sub is I or not listed — these belong to another sub |
| **Items to NARROW** | Scope items where the sub is C but the current scope says R — downgrade the language |
| **Items to ADD** | RACI items where the sub is R but the current scope doesn't mention them |
| **Items to CLARIFY** | Items where the sub is R but shared with another sub (both R) — add coordination language |

### 4. Common scope adjustments by party

#### AD Engineering (MEP Designer)

| Action | Items |
|--------|-------|
| **Remove** | ELV/Low-Current (ACS, CCTV, intercom, MATV, BMS network) → BMS/ICT specialist leads |
| **Remove** | PAVA system → BMS/ICT specialist leads |
| **Remove** | Existing Services Survey → Namaa leads (AD=I only) |
| **Remove** | Construction Support (submittal review, RFIs, site inspections, FAT, commissioning) → Samaya=R, AD=I |
| **Remove** | Telecom/IT subconsultant management → BMS/ICT specialist leads, AD=C only |
| **Narrow** | Lighting → AD provides power supply, containment, emergency lighting only. ZNA=R for all lighting design |
| **Narrow** | BIM → AD provides coordinated 2D CAD for Samaya BIM Unit to model (DC-06, DC-07) |
| **Narrow** | Telecom/IT → AD provides server room/MDF layout (IC-02), ICT cable routing (IC-04), telecom room environmental monitoring (IC-05) |
| **Add** | MEP Spatial Coordination (DC-01 to DC-05) — risers/shafts, ceiling voids, structural openings, plant rooms |
| **Add** | Fire & Life Safety Interfaces (FL-02 to FL-04) — smoke management, fire dampers, emergency lighting with FA zones |
| **Add** | AV heat load calculation for HVAC sizing (AV-03) |

#### ZNA (Lighting Designer)

| Action | Items |
|--------|-------|
| **Keep (R)** | Lighting design — general, gallery, accent, ambient (LS-01) |
| **Keep (R)** | LUX calculations & lighting performance verification (LS-05) |
| **Clarify (C)** | Lighting control system (DALI) — ZNA provides design intent/control philosophy, AD does the engineering (LS-02) |
| **Clarify (C)** | Emergency lighting & exit signs — ZNA provides fixture requirements, AD does the engineering (LS-03) |
| **Note (I)** | Lighting power supply & containment — ZNA is informed only (LS-04) |

#### BMS/ICT Specialist

| Action | Items |
|--------|-------|
| **Add (R)** | BMS architecture & points schedule (BM-01) |
| **Add (R)** | BMS + DALI integration (BM-02) — coordinate with ZNA |
| **Add (R)** | BMS + fire alarm integration (BM-03) — coordinate with AD |
| **Add (R)** | BMS + PAVA integration (BM-04) — coordinate with RAWASIN |
| **Add (R)** | BMS + access control (BM-05) |
| **Add (R)** | BMS network & IP scheme (BM-06) |
| **Add (R)** | BMS graphics & HMI (BM-07) |
| **Add (R)** | Structured cabling — fibre backbone, copper, patch panels (IC-01) |
| **Add (R)** | WiFi AP locations & coverage (IC-03) |
| **Add (R)** | Fire alarm + BMS shutdown sequences (FL-01) |
| **Add (R)** | PAVA + fire alarm integration (FL-05) |
| **Add (R)** | BMS point-to-point commissioning (TC-02) |
| **Add (R)** | ICT network testing (TC-03) |
| **Add (R)** | Integrated systems testing (TC-05) |

#### Namaa (Existing Systems Survey)

| Action | Items |
|--------|-------|
| **Add (R)** | Existing HVAC systems survey & as-built verification (ES-01) |
| **Add (R)** | Existing electrical systems survey & as-built verification (ES-02) |
| **Add (R)** | Existing fire alarm / BMS systems survey (ES-03) |
| **Add (R)** | Existing structural constraints survey (ES-04) |
| **Add (R)** | Site assessment report compilation (ES-05) |
| **Add (R)** | Fire life safety interfaces (FL-01 to FL-05) — shared R with BMS/ICT and AD |
| **Add (R)** | Integrated systems testing (TC-05) — shared R with BMS/ICT |

### 5. Update the scope document

For each sub's SCOPE_REQUEST.md:

1. **Bump version** (R01 → R02, etc.)
2. **Update date** to current
3. **Update "Issued to"** — if the sub is now appointed, change from "being negotiated" to the actual company name
4. **Add RACI alignment preamble** — note that this revision aligns with the approved RACI matrix per CG Comment #4
5. **Remove** items that belong to other subs
6. **Narrow** items where the sub's role changed from R to C
7. **Add** new sections for items where the sub is R but wasn't previously scoped
8. **Update deliverables table** — remove deliverables that moved to other subs, add new ones
9. **Update commissioning section** — narrow to systems the sub is actually responsible for
10. **Update §8 Offer Appraisal** — if the old gap analysis was based on a different scope baseline, replace it with a note that scope has been realigned per RACI

### 6. Create new scope documents for subs that don't have one

For BMS/ICT, Namaa, or any other sub that needs a scope from scratch:

1. Use the standard SCOPE_REQUEST.md template structure
2. Populate scope sections from the RACI R items
3. Add deliverables table, programme, reference documents
4. Save to `_MANAGER_DASHBOARD/SCOPE_REQUEST_<NAME>.md`

### 7. Create ZNA scope review (not a full rewrite)

For subs that already have a signed contract/agreement, create a review document instead of rewriting:

1. Read the existing agreement
2. Map each RACI item to the agreement clauses
3. Flag: fully aligned ✅, moderate gap ⚠️, high gap ❌
4. Note any CG comments that override the sub's original position
5. Save to `_MANAGER_DASHBOARD/SCOPE_REVIEW_vs_RACI.md`

### 8. Verify against the RACI

After all updates, spot-check 5-10 RACI items against the updated scope documents to confirm alignment.

## Pitfalls

- **Don't remove items that are shared R** — If two subs are both R for the same item (e.g., AD and BMS/ICT both R for server room layout IC-02), keep it in both scopes with coordination language
- **Don't downgrade CG-rejected limitations** — If CG explicitly rejected a sub's attempt to limit scope (e.g., ZNA's "Design Intent only" on lighting controls), the scope must reflect the CG position, not the sub's original proposal
- **Don't forget the deliverables table** — When removing scope items, also remove the corresponding deliverables from the deliverables table
- **Don't forget commissioning** — When narrowing scope, update the commissioning section to match (e.g., "MEP systems only" not "all systems")
- **Don't forget the offer appraisal** — If the old gap analysis was based on a different scope baseline, it's now misleading. Replace or remove it
- **BMS/ICT may not have a folder** — Create the scope document in `_MANAGER_DASHBOARD/` at the subcontractors root level until a dedicated folder is created
