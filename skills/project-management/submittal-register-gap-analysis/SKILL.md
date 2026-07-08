---
name: submittal-register-gap-analysis
description: Systematic process for auditing project submittal registers against consultant comments to identify missing deliverables and required updates.
---

# Submittal Register Gap Analysis

## Trigger
Use this skill when a user provides a submittal register (Excel/Plan) and requests a "study", "gap analysis", or "fix" to identify missing items. Two common patterns:

1. **Consultant Comment Review**: User provides a consultant's comment document (PDF/Text) + existing register.
2. **Subcontractor Register Review**: User provides a subcontractor's submitted register and asks to check completeness against contractual scope.

## Workflow

### Phase 1: Understand the Source Documents
1. **Read the register** — understand structure, columns, numbering scheme, dates, statuses.
2. **Identify the reference scope** — what are we comparing against?
   - For **consultant comments**: extract all requirements from the comment document.
   - For **subcontractor registers**: identify the contractual scope docs (SOW, SCOPE_REQUEST.md, DMP, ER, Div specs, concept design packages).

### Phase 2: Cross-Reference Against Scope
Cross-reference each register item (or missing item) against the **contractual scope documents** (ER, SOW, pre-contract design reports, DMP, SCOPE_REQUEST.md). This identifies:

- **Scope Gap**: The source demands X, but the ER/SOW/design report explicitly excludes X from contractor scope. The register is correct — the gap is in the contractual scope, not the register.
- **Contractor Omission**: The source demands X, and the ER/SOW requires it, but the register doesn't list it. This is a genuine gap.
- **Stage Mismatch**: The source demands X, but X belongs to a later stage (e.g., CG asks for IFC-level detail during DD submission).
- **Pre-Contract Exclusion Confirmed**: The pre-contract design report explicitly states "X to be done by D&B contractor" — the source is now demanding X, confirming it IS in scope. The register needs to add it.

### Phase 3: Gap Identification
Classify each item as:

- **Present**: Item exists and meets the requirement.
- **Partial**: Item exists but lacks specific detail (e.g., "missing per-floor breakdown").
- **Missing — In Scope**: No corresponding item exists, but the scope docs require it. Must be added.
- **Missing — Out of Scope**: No corresponding item exists, and the scope docs don't require it. Flag for commercial/contractual resolution.
- **Explicitly Excluded**: The pre-contract design report explicitly excluded this item. The source demanding it is a scope addition, not a register gap.

### Phase 4: Produce the Corrected Register
When the user says "fix" or "can you fix", the deliverable is a **working corrected Excel file**, not just a gap table.

1. **Preserve original formatting** — keep the subcontractor's column structure, colors, merged cells, fonts. Build on their file.
2. **Add missing items** — insert rows for every "Missing — In Scope" item with proper codes, descriptions, and realistic dates.
3. **Fix structural issues**:
   - Add proper drawing/package codes (e.g., ASE-AV-xxx) where missing.
   - Stagger per-floor IFC packages instead of lumping all on one date.
   - Add BIM submittals (LOD300/350/500) if missing.
   - Add post-install deliverables (FAT, SAT, cable tests, cybersecurity, O&M, training, spares).
   - Add coordination submittals (Interface Register, setwork housings, showcase AV interface, DALI/BMS).
4. **Fix dates** — move past-due items to realistic forward dates. Account for CG review durations (typically 7-14 days).
5. **Add status tracking** — mark items as Planned / In Progress / Submitted / Overdue.
6. **Save to the project location** — copy to the OneDrive BIM path under the appropriate submittal register folder.

## Output Format

### For analysis-only requests:
| Source Ref | Requirement | Current Status | Action Required | Priority |
| :--- | :--- | :--- | :--- | :--- |
| [Ref] | [Concise description] | Present / Partial / Missing | [Specific change] | High/Med/Low |

### For fix requests:
The corrected Excel file saved to the project path, plus a summary table showing:
- What was added (count + list)
- What was fixed (dates, codes, structure)
- What was preserved from the original

## Stage-Aware Analysis

**CRITICAL:** Match submittal requirements to the **project stage**, not a generic checklist.

| Stage | What's Expected | What's NOT Expected |
|-------|----------------|---------------------|
| Stage 2-3 (Concept/Developed) | Design philosophy, UX strategy, system architecture narrative | Technical drawings, detailed schedules |
| Stage 4 (Technical Design) | Drawings, schedules, calculations, diagrams, rack elevations | Design Basis Report, concept philosophy docs |
| Stage 5 (IFC/Construction) | Per-floor IFC packages, specs, ITP, commissioning plans | Detailed design studies |

**Common mistake:** Recommending a Design Basis Report for Stage 4. CG reviews technical content at this stage — drawings, schedules, and calculations are the deliverable, not design narrative. The concept designer (e.g., DHD Services) already produced the philosophy at Stage 2-3.

## Drawing Code Floor Prefix — Do NOT Assume

**Pitfall:** Drawing codes like `MOC-ASE-AV-TAV-BF-DDD-1230-00` may use `BF` as a **project prefix** (e.g., "Building Fit-out" or project code), NOT "Basement Floor". The actual floor is in the title block text.

**Always verify by reading the title block** — extract text from the PDF/DWG title block area to find the actual floor name. In the Aseer Museum AV case, all 8 drawings had `-BF-` in the code but actually covered 4 different floors (Basement, Lower Ground, Ground, First). The `BF` was a project code, not a floor indicator.

## CG-Facing Register — No Internal Responsibility Split

When submitting a register to CG, do NOT show internal responsibility splits (subcontractor vs main contractor). CG sees everything as "Samaya". Use only 3 status values: `Submitted` (green), `Pending` (yellow), `Future Gate` (grey). Set all Responsibility column values to `'Samaya'`.

## Responsibility Split Pattern

When a subcontractor's scope doesn't cover all submittals (e.g., AV Designer doesn't do BIM or coordination drawings), split the register by party:

1. **AV Designer scope** — their contractual deliverables (drawings, schedules, calculations, diagrams, rack elevations, control requirements, testing, handover)
2. **Samaya scope** — items Samaya handles (BIM models, structural calcs, IT/ELV, acoustic, coordination, Interface Register, cybersecurity)

Use color coding (green tint = AV Designer, blue tint = Samaya) and section headers to make the split visually clear. This lets you send the AV Designer only their section while keeping the full picture internally.

## CG Comment Response Workflow — Submission Plan Review

When CG issues comments on a submission plan (e.g., "add scenography drawings", "add furniture layouts"), follow this sequence:

### Response Voice Rules

- **Samaya is the contractor.** All responses are from Samaya's perspective. Do NOT say "NRS scope" or "AV Designer scope" — CG sees everything as Samaya.
- **No internal sub-consultant splits.** If a designer (NRS, ZNA, etc.) provides input, report it as information received, not as a scope boundary.
- **Items to be included later** → "will be coordinated and included in subsequent stages from 50% to 90% to IFC. [Specialist] to be appointed."
- **Items already covered by Stage 3** → "was defined and approved at Stage 3. To be confirmed with CG whether existing submission is sufficient."
- **Items by other discipline** → "will be provided as part of the overall submission under the relevant scope, coordinated with the [specialist]."

### Full CR Sheet + Response Package Workflow

See `references/cr-sheet-response-package.md` for the complete workflow: building the CR Sheet, updating submission plans, splitting specialized scope registers, packaging the response folder, and filing to OneDrive.

### Step 1: Check the Designer's SOW/Contract FIRST

**Do NOT ask the designer "is this in your scope?"** — the user will correct you. Check the signed SOW, responsibility matrix, and contract documents before writing to the designer.

**Where to check (Aseer Museum NRS example):**
- `01_Contracts/02_NRS_Contract/01_Signed_Agreements/Nissen SOW_OPTION_01_updated.xlsx` — responsibility matrix
- `01_Contracts/02_NRS_Contract/01_Signed_Agreements/Nissen SOW responsibilty matrix.pdf` — detailed scope breakdown

**NRS SOW Responsibility Matrix (reference):**

| Item | NRS Role |
|------|----------|
| Scenography | Design & SD ✓ |
| FF&E (Furniture & Furnishings) | Design & SD ✓ |
| Display Cases & open displays | Design & SD ✓ |
| Setworks & Fit-Out | Design & SD ✓ |
| Life & Safety / Civil Defense | Samaya Design & SD — NRS coordinates on base plans |
| Universal Access / Accessibility | Not listed — potential gap |
| Signage & Graphics | NRS scope (locations on GA plans) |
| Maintenance Access | Defined by Stage 3 — NRS can copy annotations |

### Step 2: Prepare the Modified Submission Plan Yourself

Do NOT ask the designer to prepare the revised plan. The user (Samaya) updates the submission plan with new items added, then sends to the designer for date suggestions only.

**New items to add (from CG comments):**
- Scenography Drawing
- Furniture Layout (FF&E)
- Signage & Graphics Plan
- Universal Access Drawings
- Maintenance Access Plan

Set responsibility to `NRS` and dates to `'as Nrs Date'` or similar placeholder.

### Step 3: Send Concise Email to Designer

Format: point-by-point, no scope questions, just request dates.

```
Subject: [Project] — CG Comments on Submission Plan / Revised Plan for Review

Dear [Designer],

CG has reviewed the [Discipline] Submission Plan and issued the following comments:

1. [Comment 1]
2. [Comment 2]
...

We have updated the submission plan and added the following new items:
- [Item 1]
- [Item 2]
...

Please review the attached revised submission plan and suggest the proposed dates for these new items so we can finalise and submit to CG.

Regards,
[Name]
```

### Step 4: Forward Designer's Response to CG

When the designer responds with their position (e.g., "scenography already in Stage 4 pack", "furniture by others"), forward their email to CG with a summary. Do NOT try to resolve scope disputes yourself — let CG and the designer negotiate.

### Common NRS Positions on CG Comments (from actual response)

| CG Comment | NRS Position |
|------------|--------------|
| Scenography drawings | Already in Stage 4 pack — not a Stage 4 requirement per RIBA |
| Furniture layouts | NRS only does bespoke setwork furniture. Other FF&E by Samaya |
| Universal Access Drawings | Defined by Stage 3 — no changes proposed |
| Access & Evacuation Plans | Life safety is outside NRS scope — prepared by others |
| Signage & Graphics | Locations on GA plans. Graphics content outside NRS scope |
| Maintenance Access Plan | Defined by Stage 3 — can copy annotations from Stage 3 doc |

## Pitfalls
- **Vague Mapping**: Avoid saying "it's there." Specify which drawing number or item # corresponds to the requirement.
- **Missing Context**: For "Partial" status, explicitly state what is missing from the existing deliverable.
- **Formatting**: Use formal construction project management English. No emojis or conversational filler.
- **Don't just analyze — fix**: When the user says "fix", produce the corrected file. A gap table alone is not the deliverable.
- **Don't overwrite blindly**: Preserve the subcontractor's original formatting and structure. Build on their work, don't replace it.
- **Check for already-submitted items**: The register may start from scratch and omit items already submitted (e.g., IFC-0008). Add them with "Submitted" status.
- **BIM is often forgotten**: Subcontractors frequently omit BIM submittals (LOD300/350/500). Add them explicitly.
- **Per-floor IFC**: Subcontractors often lump all floors into one IFC package. Split into per-floor packages with staggered dates.
- **Post-install deliverables**: FAT, SAT, cable test certs, network config, cybersecurity — these are often missing from subcontractor registers.

## Verification
- Cross-reference the final register against the original scope docs to ensure 100% coverage.
- Verify all items have proper codes, realistic dates, and assigned responsibility.
- Confirm the file opens correctly and preserves the original's formatting.
