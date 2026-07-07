---
name: project-resource-loading
description: Build defensible headcount/resource loading estimates for construction and fit-out projects — derive from DMP/PEP programme day references, map role FTEs to phases, aggregate into headcount curves with documented Basis of Estimate.
version: 1.1.0
author: Samaya BIM Unit
tags: [resource-loading, headcount-estimate, basis-of-estimate, resource-management-plan, construction-staffing]
---

# Project Resource Loading

For building the resource loading / headcount section of a Project Resource Management Plan (or similar deliverable). The core principle: **headcount numbers must be derivable from programme durations**, not carried forward from previous revisions without justification.

## When to Use

- Building or auditing a Resource Management Plan's headcount curve (§5 equivalent)
- Responding to CG review comments on staffing assumptions
- Documenting the Basis of Estimate for resource loading
- Deriving peak manpower from programme day references

## Core Method: Programme Days → Headcount

The chain of derivation:

```
DMP/PEP programme days
    ↓
Phase durations (working days per phase calendar)
    ↓
Role schedule (FTE commitment per role per phase)
    ↓
Aggregate active FTEs per phase → headcount curve
    ↓
Document Basis of Estimate table
```

### Step 0 — Align Org Structure with DMP Before Building Content

Before extracting phase durations or building the role schedule, verify that **§3 Organization Structure & Hierarchy** matches the DMP's organization chart:

3. **Read the latest DMP HTML** (usually Rev C04 or latest) — find the organization chart section (typically §5.0 Project Organization Chart in DMP). For Aseer Museum, see `references/aseer-dmp-tier-mapping.md` for the complete tier-to-role mapping.
2. **Compare Tier 1 roles**: DMP's 6 management specialists must match exactly. Common mismatches:
   - DMP says "Site Manager" — resource plan says "Construction Manager" → align naming
   - DMP does NOT list "Tech Office Manager" as separate Tier 1 → remove from Tier 1 card grid or add annotation
   - DMP may include "Project Manager" or "Design Manager" as separate Tier 1 → add if present
3. **Compare Tier 2 design specialists**: DMP typically lists 14 design specialists in a 2-column table. The resource plan must include ALL of them, not substitute internal BIM coordination roles. Missing roles commonly include:
   - Audio-Visual Hardware Specialist
   - Mech. & Electromech. Interactives
   - Models & Props Specialist
   - Graphic Artwork & Illustration
   - Café Terrace Shade Specialist
   - Landscaping Specialist
4. **Report discrepancies to user** before making changes — some differences are intentional (e.g. resource plan shows internal team structure, DMP shows consultant structure)

5. **Reorganize tiers if user confirms**: Once user approves alignment, restructure §3 as:
   - **Tier 1 — Management** (6 cards): Exactly matching DMP's 6 management specialists. Drop extra cards (Tech Office Manager, Construction Manager) or rename to match DMP naming (Site Manager not Construction Manager).
   - **Tier 2 — Design Specialists** (table): Only external design consultant firms. Move internal Samaya BIM/support roles out of this tier.
   - **Tier 3 — Samaya Technical Office & Support** (table): BIM Coords, BIM Leads, BIM Modelers, Electrical Eng., IT/Data, Tech Office Mgr, Document Controllers, Submittals Coord, Planner, ITCA. Add note referencing Authority Specialists per DMP Tier 3.
   
   **Key rules when reorganizing:**
   - The user will correct firm assignments (e.g. "AV Hardware is Rawasin, not NRS") — expect and fix these
   - Keep the Construction Org Chart (§3.2) as-is below the tiers
   - Do not remove existing approved names — only move them to correct tiers
   - Add a footnote referencing DMP for Authority Specialists rather than duplicating the full list

Day references come from the DMP (Design Management Plan) or PEP (Project Execution Plan). Standard phases for a museum/fit-out project:

| Phase | Day Range | Calendar Duration | Working Days |
|-------|-----------|------------------|-------------|
| P1 — Pre-LOA / Setup | D-14 → D0 | 14 | ~12 (Sat-Thu) |
| P2 — Kick-off / Mobilization | D0 → D14 | 14 | ~12 |
| P3 — Design Development | D14 → D88 | 74 | ~63 |
| P4 — Construction / Fit-out | D88 → D270 | 182 | ~156 |
| P5 — Demobilization | D270 → D300 | 30 | ~26 |

**Always source the actual day ranges from the approved DMP/PEP document.** The example above is for a typical museum fit-out (Aseer Museum pattern). Adjust for your project's specific programme.

### Step 2 — Build the Role Schedule (FTE per Phase)

For each role, assign a commitment level per phase:

| Commitment | FTE Factor | Meaning |
|------------|-----------|---------|
| FT (Full-Time) | 1.0 | 100% committed |
| 50% (Half-Time) | 0.5 | Alternating days or shared role |
| part (Part-Time) | 0.3 | On-call / advisory / shared across projects |
| stage (Stage-Specific) | count-specific | Active only during a defined sub-phase |
| ramp (Ramping Up/ Down) | 0.3–0.7 | Transition period, typically 2 weeks |

Example role schedule pattern:

| Role | P1 | P2 | P3 | P4 | P5 |
|------|:--:|:--:|:--:|:--:|:--:|
| Project Director | 50% | FT | FT | FT | FT |
| Construction Manager | — | FT | FT | FT | 50% |
| BIM Manager | 50% | FT | FT | 50% | — |
| Tech Office Manager | FT | FT | FT | 50% | — |
| QA/QC Manager | — | FT | FT | FT | 50% |
| Site Team | — | — | ramp | FT | part |

### Step 3 — Aggregate Headcount Curve

Sum all active FTE values per phase. The curve typically looks like:

| Day | Headcount | Notes |
|-----|:---------:|-------|
| D-14 | ~2 | Core management only |
| D0 | ~10 | After LOA, key leads active |
| D35 (G2) | ~30 | Design team fully mobilized |
| D65 (G3) | **~38 peak** | Design surge + early site overlap |
| D88 (AFC) | ~37 | Design roll-off begins, site team scales |
| D180 | ~17 | Construction steady-state |
| D270 | ~7 | Demobilization phase |
| D300 | ~2 | Close-out only |

**Peak timing**: The peak occurs when the design team is at maximum (around G3/90% gate) and overlaps with the beginning of construction site mobilization. This dual-surge creates the highest point on the curve.

### Step 4 — Document the Basis of Estimate

Create a 5-parameter Basis of Estimate table to make the headcount defensible:

| Parameter | What to State |
|-----------|--------------|
| **Phase durations** | Source document (DMP Rev XX or PEP), phase day ranges, working calendar (e.g. Sat–Thu, Friday excluded) |
| **Staffing assumptions per role** | Each role's FTE commitment per phase, assigned against WBS activity groups, dimensioned via a resource quantification tool (e.g. QS_Template.xlsx) |
| **Aggregation method** | Headcount = sum of active-role FTEs per phase. Account for staggered roll-off (design → site transition at AFC) |
| **Contingency factor** | +10% allowance for unplanned surge (scope creep, late substitution, snagging peaks). State whether this is included in the reported peak or separate |
| **Validation** | Cross-check against comparable projects (similar type, scale, geography). State margin of error (e.g. ±15% pending schedule approval) |

Also add a note about planned updates: "Rev XXa update will re-baseline once the Master Programme is formally approved and a confirmed start date (D0) is established."

## Handling Unapproved Schedules

When the Master Programme / baseline schedule is not yet formally approved:

1. **Flag it as a risk** in the Resource Risk Register: "R# — Headcount curve based on draft programme; ±15% margin pending baseline approval."
2. **Use provisional day references** from the DMP/PEP (which are contract-committed targets even if the CPM model isn't approved yet)
3. **Promise a formal update** at programme approval: "Rev XXa will re-baseline with confirmed D0 and approved activity durations."
4. **Do not guess** calendar dates (e.g. "2025-12-01") if D0 is provisional — use D-NN references throughout and note in the margin

## Headcount Curve SVG — Key Values

When plotting the headcount curve as an SVG:

- Y-axis: 0–40+ (3px per headcount at standard scale)
- X-axis: D-14 through D300 mapped proportionally
- Peak marker: gold circle at the G3/D65 point with "Peak ~38" label
- Gate markers: vertical dashed lines at G2, G3, G5-AFC
- Phase labels below x-axis: P1–P5

The SVG path can use these control points (for a 600×220 viewBox):

| Day | X | Headcount | Y |
|-----|:---:|:----------:|:---:|
| D-14 | 40 | ~0 | 170 |
| D-7 | 80 | ~4 | 158 |
| D0 | 120 | ~10 | 140 |
| D14 | 160 | ~20 | 110 |
| D35 | 200 | ~30 | 80 |
| D65 | 280 | ~38 | 50 |
| D88 | 350 | ~37 | 60 |
| D130 | 420 | ~27 | 90 |
| D180 | 500 | ~17 | 120 |
| D270 | 560 | ~7 | 150 |
| D300 | 580 | ~2 | 165 |

## Appendix: Full Resource Management Plan (§5) Structure

For the resource loading section of a formal Resource Management Plan:

```
§5.1  Headcount Loading Curve
        SVG chart 600×220 with curve + peak marker + gate annotations
        Caption: peak timing, risk alerts, basis cross-reference

§5.2  Role Allocation by Phase
        Table: role × commitment per phase (FT/50%/part/stage/ramp)
        Footnote: legend for commitment codes

§5.3  Basis of Estimate — Headcount Derivation
        5-parameter table (phase durations, staffing assumptions,
        aggregation method, contingency factor, validation)
        Note on planned re-baseline after programme approval
```

## Stacked Manpower Histogram (Improved §5.1)

When the PD or CG requests a "detailed manpower histogram" (improvement of the single-curve SVG), build a stacked area chart with 5 discipline bands:

### Discipline Categories and Colors (DMP-aligned 4-band)

When the PD or CG requests a detailed manpower histogram (stacked by DMP tier), use this 4-band structure instead of the older 5-band approach:

| Band | SVG Fill | Peak Persons | Active Phase |
|----------|---------|:------------:|:------------:|
| T1 Management | `#0F172A` (navy) | ~6 | P1→P5 |
| T2 Design Specialists | `#0284C7` (sky) | ~16 | P2→P4 |
| Site / Construction | `#16A34A` (green) | ~12 | P3→P5 |
| T3 Support | `#94A3B8` (slate) | ~8 | P1→P5 |

**Peak total at D65/G3: ~35 persons** (not 38 — the 4-band reclassification corrected overstated headcount). Construction scales post-AFC to ~30 during P4 fit-out.

### SVG Construction Approach (4-band stacked)

Maintain the same 600×220 viewBox as the single curve. Build each band as a <path> element with fill-opacity="0.7" for stacking visibility. Order from bottom to top (T3 Support → Site/Construction → T2 Design Specialists → T1 Management).

```svg
<!-- Bottom band (Support) — cumulatively lowest -->
<path d="M 40 185.75 L 120 181.5 ... Z" fill="#94A3B8" fill-opacity="0.7"/>
<!-- Each subsequent band stacks on top by using cumulative Y values -->
<path d="..." fill="#16A34A" fill-opacity="0.7"/>
<path d="..." fill="#F59E0B" fill-opacity="0.7"/>
<path d="..." fill="#0284C7" fill-opacity="0.7"/>
<!-- Top band (Management) — cumulatively highest -->
<path d="..." fill="#0F172A" fill-opacity="0.7"/>
```

### SVG Coordinate Data Points (600×220 viewBox)

Use these values for a 4-band DMP-aligned stacked histogram (T1 Management, T2 Design Specialists, T3 Support, Site/Construction):

| Day | X | T1 Mgmt | T2 Design Spec. | Site/Const. | T3 Support | Bottom |
|-----|----|---------|----------------|------------|-----------|--------|
| D-14 | 40 | 156.00 | 164.50 | 177.25 | 177.25 | 190 |
| D0 | 120 | 113.50 | 139.00 | 173.00 | 173.00 | 190 |
| D14 | 160 | 83.75 | 109.25 | 160.25 | 164.50 | 190 |
| D35 | 190 | 49.75 | 75.25 | 143.25 | 156.00 | 190 |
| D65 | 280 | 41.25 | 66.75 | 134.75 | 156.00 | 190 |
| D88 | 350 | 45.50 | 71.00 | 113.50 | 156.00 | 190 |
| D180 | 450 | 62.50 | 88.00 | 113.50 | 164.50 | 190 |
| D270 | 540 | 117.75 | 130.50 | 143.25 | 177.25 | 190 |
| D300 | 580 | 160.25 | 168.75 | 173.00 | 185.75 | 190 |

**Peak total at D65/G3: 35 persons.** Construction scales post-AFC to ~30 during P4 fit-out. |

### Key Design Rules

1. **Bottom → Top order**: The SVG draws from bottom layer to top. Support is drawn first, followed by Site Team, Discipline Engineers, BIM+Design, Management last.
2. **Cumulative coordinates**: Each band's Y values are CUMULATIVE (includes all lower bands). This creates the stacking effect.
3. **Legend**: Add a color-coded legend below the chart using small `<rect>` elements + labels.
4. **Gate markers**: Maintain G2, G3, G5-AFC vertical dashed lines (+ phase labels P1-P5) from the single-curve version.
5. **Axis labels**: Keep Y-axis (0-40 headcount) and X-axis (D-14 to D300) identical to single-curve version.
6. **Peak label**: Optional — add "Peak ~38" annotation at the topmost point of the Mgmt band around D65.

## KPR Cross-Referencing — Mandatory Before Any Plan Submission

Before finalizing any Resource Management Plan (or any document naming personnel), cross-reference ALL names against the live Key Personnel Register (KPR). The KPR is the single source of truth for who is approved, pending, or vacant.

### KPR Location

`Docs/09_Registers/13_Key_Personnel_Register/Aseer_Museum_Key_Personnel_Register.xlsx`

### Reading the KPR

**Use `terminal` with system python3 — NOT `execute_code`.** The OneDrive cloud path times out with openpyxl's fcopyfile when called from execute_code's sandbox. From terminal:

```bash
python3 -c "
import openpyxl
wb = openpyxl.load_workbook('/path/to/KPR.xlsx', data_only=True)
ws = wb['Key Personnel']
for row in ws.iter_rows(min_row=1, max_row=40, values_only=True):
    if any(v is not None for v in row):
        print(list(row))
"
```

If `terminal` also times out on copy, run python3 directly against the OneDrive path — `openpyxl.load_workbook()` can read in streaming mode even when `cp`/`shutil.copy2` times out.

### KPR Approval Statuses (authoritative terminology)

| Status | Meaning | Can name appear in plan? |
|--------|---------|--------------------------|
| Approved | MoC-approved | Yes — name allowed |
| Approved with Comments (Code B) | Approved with minor comments | Yes — firm name, not individual |
| Pending submission | CV not yet submitted to MoC | **YES — person IS on board and working. Keep the name.** Do NOT blank it. Do NOT write "pending MoC submission" — just show the name with "On board" or no status label. |
| C - Revise and Resubmit (Code C) | Rejected, needs revision | **YES — keep the name.** Show "submission in progress". Do NOT write "Code C (revise & resubmit)" — that's KPR-level detail, not for plan documents. |
| Vacant | Role unfilled | "Vacant" |
| Not yet appointed | TBC | "TBC" |
| Pending - not yet approved by CG | Under review | Keep firm name only, no individual names |
| Nominated - pending approval | NDA/prequal stage | Keep firm name only, no individual names |

### Brand Names in Materials Section

**Do NOT include brand names or supplier names in the Materials section of the RBS unless materials are formally approved with supplier confirmed.** The user explicitly rejects brand names during draft/pre-submission stages. Use generic descriptions:

| Wrong (with brands) | Right (generic) |
|---------------------|-----------------|
| Porcelain tiles (Ceramiche Piemme), micro concrete tiles (Concept Tiles), carpet (Tarkett) | Porcelain & mosaic tiles, micro concrete effect tiles, carpet |
| Sonacoustic plasterboard (Asona), metal baffle (Knauf), acoustic panels (Kvadrat) | Acoustic plasterboard, metal baffle ceiling, acoustic panels |
| iGuzzini spotlights, Yamaha audio, Dante network | Spotlights & track, audio systems, network equipment |

**Exception:** Glasbau Hahn (showcases) is an approved specialist FIRM — its name can appear in the Sub-Contractor table (§7.3) and Tier 2 list, but not as a brand name in the Materials RBS list.

### TBC Status Display — No Commentary for Unassigned Roles

When a role has **no assigned firm** (status is genuinely TBC/vacant), show just the bare status without qualifying commentary:

| Wrong | Right | Reasoning |
|-------|-------|-----------|
| `TBC — pending submission` | `TBC` | Pending submission is internal process detail |
| `TBC — Code C (revise & resubmit)` | `TBC` | Code C is KPR-level detail, not for plan docs |
| `TBC — prequal in progress` | `TBC` | Prequal status is internal |
| `TBC — ⚠ CRITICAL PATH` | `TBC` | Risk commentary belongs in risk register, not org chart |

**Exception — roles with an assigned firm name**: When a firm IS named (e.g. Rawasen), the CG status IS relevant in the Exhibition Team Matrix (§7.3):

| Row | Status Format | Example |
|-----|--------------|---------|
| Tier 2 role table | Firm name only (no status appended) | `Rawasen` |
| Exhibition Matrix | Firm name + CG status | `Rawasen — pending approval` or `Approved` |
| Location Matrix | Location only (no status appended) | `Site-based` |

### Direct KPR Excel Updates — Only When User Provides File

The default rule is: **do NOT modify the KPR Excel directly** — it's a controlled register maintained by PD/HR. The plan flags what needs to change; it does not change it.

**Exception**: If the user explicitly attaches the KPR Excel file AND asks you to sync/update it, you may edit it directly via openpyxl. Use `terminal` (not `execute_code`) for OneDrive paths. Rules when editing:

- Update notes columns (`MoC Approval Status`, `Lock-in Notes / Comments`) — never change names, tiers, or statuses without user confirmation
- Use `ws.cell(row=N, column=M).value = '...'` — do NOT use `ws.insert_rows()` which silently loses data on OneDrive-synced files
- Save in place with `wb.save(path)` — the original filename is preserved
- Report exactly what changed

### Core Philosophy: Plan Documents Record Structure, Not People

The KPR is the people register. The plan document records roles, organization, and processes. **We do not duplicate the KPR inside the plan.** When submitting, reference the KPR snapshot as a companion document:

> **"Plans for plan content, not for names. Known KPR names appear; all others referenced via KPR snapshot submitted alongside."**

Implementation rules:
- **KPR-approved individuals** with status "Approved" → name appears in plan
- **KPR-approved firms** with no approved individual → firm name only in plan
- **Firms in prequal/NDA stage** → REMOVE entirely from all plan sections (see "Unapproved Subcontractors" rule)
- **Vacant/TBC roles** → show "Vacant" / "TBC" — never invent a name
- **Known KPR names are NEVER removed during restructuring** — when reorganizing tiers (e.g. T2 → T3), preserve all existing named individuals. Move them to the correct tier, don't drop them. The user will catch missing names immediately ("Hesham why you lost him?").
- **Do NOT add a role to the plan just because PD mentioned it** without verifying against DMP T2 list (14 roles) and SMP 55-role register. If absent from both, flag as potentially redundant — existing roles may already cover the scope. Confirm with user before adding.
- **Do NOT guess which firm covers a design discipline** — check the DMP §5.1.1 and SMP Rev 03 §4.4 first. Common mistakes: AV Hardware is Rawasin (not NRS), Mech. Interactives is Rawasin (not Lumotion — also unapproved), Sustainability specialist is TBC (Dr. Ehab Foda not approved).
- **Do NOT use `execute_code` to read OneDrive xlsx files.**
### Rules for Plan Documents

1. **Keep on-board personnel names.** "Pending submission" in KPR means the person IS on board and working — their CV just hasn't been formally submitted to MoC. Show the name. Do NOT write "pending MoC submission" as a label — just show "On board" or nothing.
2. **Firm names are allowed** only for approved firms (AD Engineering, ZNA Studio, Nama Consulting, Glasbau Hahn, NRS). Firms in prequal / NDA stage or without formal CG approval must NOT appear in any plan section — remove references from subcontractor tables, risk registers, induction steps, mobilization notes, companion documents, and RBS lists entirely.
3. **Individual names within approved firms** (e.g. Julie Riley at ZNA, M. Moustafa at AD Engineering) should NOT appear — use firm name only. **BUT** if the INDIVIDUAL is separately approved in the KPR as a named role (e.g. Eng. Jim Richards at NRS — DSN NRS Design Lead, Approved 2026-02-11), the name CAN and should appear. Check KPR status per role, not per firm: if KPR shows a named individual with status "Approved", use the individual name. If KPR shows only the firm with no approved individual, use firm name only.
4. **Tech Office Manager is NOT a KPR Tier 1 role.** The 6 KPR Tier 1 roles are: Project Director, BIM Manager, T&C Manager, QA/QC Manager, HSSE Manager, Site Manager/Construction Manager. Do not invent Tier 1 roles outside the KPR.
5. **Tier 3 roles** (ITCA, Licensed Fire-Proofing Contractor) must appear in the plan — they are KPR roles even when TBC.
6. **Document control sign-off fields** (Prepared by, Issued by) are operational roles, not KPR claims — those names may remain.
7. **Do NOT mention "Overseas"** or non-project-site cities (Dubai, London, Egypt). Only Riyadh and Abha are location references. The location matrix columns (HO Riyadh / Site Abha / Remote) are sufficient.
8. **Do NOT use "on-site"** for personnel not physically at site. Use "appointed" instead.
9. **Include all team members in location-group lists.** If listing BIM Modelers at Riyadh HO, include everyone assigned there (e.g. Ali A. Mostafa, Mohamed Mostafa, Toka Hesham, Mohamed Matrawy, Alaa Hissi) — don't omit people who appear elsewhere in the document.
10. **Materials lists must be detailed from project schedule data**, not generic. Pull actual material descriptions, suppliers, and specifications from the finishes schedule, showcase schedule, AV equipment schedule, and lighting schedule JSONs.

### Entity Name Corrections (KPR-authoritative)

| Wrong name | Correct name (per KPR) |
|------------|----------------------|
| Nama Al Amal | Nama Consulting |
| Glassbühne | Glasbau Hahn |
| AD Engineering Co. — M. Moustafa | AD Engineering (firm name only — individual not approved) |
| ZNA Studio — Julie Riley | ZNA Studio (firm name only — individual not approved) |
| AV Hardware — NRS | Rawasin (AV/Interactive specialist is Rawasin, not NRS. The DMP §5.1.1 lists Audio-Visual Hardware Specialist at #4 and Electronmech. Interactives at #8 — both under Rawasin.) |
| Eng. Jim Richards (if KPR shows "NRS Design Lead") | Eng. Jim — NRS (individual IS approved for DSN role, show name with firm) |

### Cross-Reference Checklist

Before submitting any plan with personnel names:

- [ ] Read KPR xlsx (terminal python3, not execute_code)
- [ ] For each name in the plan, find the matching KPR row
- [ ] If status ≠ Approved/Code B → replace name with "—" or "TBC", add status note
- [ ] Verify Tier 1 card grid matches KPR's 6 Tier 1 roles exactly AND the DMP's Tier 1 classification (cross-reference DMP Rev C04 org chart for role naming: Site Manager vs Construction Manager, inclusion/exclusion of Tech Office Manager, Project Manager, etc.)
- [ ] Verify Tier 3 includes ITCA + Fire-Proofing (even if TBC)
- [ ] Verify firm entity names match KPR spelling
- [ ] Search the full HTML for any remaining unapproved individual names
- [ ] Location matrix, phase loading matrix, and subcontractor tables all checked

## Source Document Authority — PD Comments Are Triggers, Not References

When the PD (or any reviewer) sends comments on a draft plan, their suggestions are **triggers to investigate** — not authoritative source references. Every role, chart, or table added in response must trace back to a contract document (ER, SOW, DMP) before being included in the plan.

### Classification Rule

| Source | Authority Level | Use in Plan |
|--------|----------------|-------------|
| **ER** (Employer Requirements) | Contractual | Primary — must comply |
| **SOW** (Scope of Work) | Contractual | Primary — §5.5 minimum staffing is mandatory |
| **DMP** (Design Management Plan) | Approved plan | Co-equal — org chart tiers are authoritative |
| **CG review comments** | Client directive | Must address — map to contract clauses |
| **PD comments** | Internal review | Investigate — verify each ask exists in a contract source before building |
| **SMP** (Stakeholder Management Plan) | Approved plan | Cross-reference for entity names, tier classification, CRS codes |
| **KPR** (Key Personnel Register) | Live register | Authoritative for names/statuses — plan references it, doesn't duplicate it |

### Practical Example

PD says: *"Add Humidity/Environmental Specialist"*

**Don't:** Add the role to the plan and run with it.
**Do:** Check DMP T2 list (14 roles — not there), check SMP 55-role register (not there), check SOW §5.5 minimum staffing (not there). The conservation environment is already covered by Glasbau Hahn (showcase micro-climate) and AD Engineering (MEP HVAC). Report this to the user and let them decide whether to merge with Acoustic Consultant or drop it entirely.

### Reference Label Rule

Every chart, table, or section in the plan should have an inline source reference in the subtitle or caption:
- ✅ `SoW §5.5 Staffing & Deployments · §10 On Site Fit-Out`
- ❌ `Per PD recommendation — site team structure`
- ❌ `Per PD recommendation — specialist roles`

PD recommendations may have **triggered** the addition, but the **justification** in the published document must be a contract source.

## CG Submission Cleanup — Stripping Internal Content

Before any document is submitted to CG (Consultant), scan for and remove:

| Item | Example | Action |
|------|---------|--------|
| **Internal KPR action notes** | Amber callout box with "Key Personnel Register Update Required" | **Remove entirely** — it's PD/HR housekeeping, not for client review |
| **"PD recommendations" language** | Cover description or revision history saying "Updated per PD recommendations" | Rewrite as "Updated: [what changed]" — CG doesn't need to know the trigger was an internal review |
| **"DRAFT" status badges** | `[DRAFT — FOR CG REVIEW]` | Change to `[ISSUED FOR CG REVIEW]` — never submit a document labeled Draft |
| **"Hiring in progress" notes** | QA/QC Manager card saying "Hiring in progress" | Keep "Vacant" status but remove informal notes — show facts, not process |
| **Unapproved subcontractor references** | Any firm with prequal/NDA/pending status | Remove from ALL sections: subcontractor tables, risk registers, induction steps, mobilization notes, companion documents, RBS lists |
| **Internal role names** | "Construction Manager" when DMP says "Site Manager" | Align to DMP naming before submission |
| **Invented tier labels** | "Construction Tier" pill in §3.2 chart | Remove — only use T1/T2/T3 per DMP classification |

### General Principle

> **The CG reviews roles, structure, and compliance — not internal staffing process.**

Any content that answers "how we decided this" or "who still needs to do what" belongs in an internal memo, not the submission document. Strip it before generating the final HTML.

<hr>

## KPR Action Note — Internal Housekeeping (for INTERNAL drafts only)

When the plan adds new roles, renames existing ones, or adds named individuals that need KPR entries, do NOT edit the KPR Excel directly. Instead, for internal drafts, add:

1. Add an **amber callout box** at the end of §3 listing all KPR updates needed
2. Label it with `pill pill-amber` and heading "Key Personnel Register Update Required"
3. Split into columns: Role | Update Needed | Action By (PD/HR)
4. Add a footnote: *"Roles marked TBC pending appointment. Plan references KPR as live source of truth."*

The KPR is a controlled register (`MOC-ASEER-SIC-1K0-KP-0001`) — only PD/HR has authority to modify it. The plan flags what needs to change; it does not change it.

### KPR Action Note HTML Template

```html
<div style="margin-top:8px;border:1px solid var(--accent);border-left:4px solid var(--accent);background:#FFFBEB;border-radius:4px;padding:6px 10px;">
  <div style="display:flex;align-items:center;gap:6px;margin-bottom:3px;">
    <span class="pill pill-amber">KPR Action</span>
    <b style="font-size:0.55rem;color:var(--primary);">Key Personnel Register Update Required</b>
    <span style="font-size:0.42rem;color:var(--text-muted);font-style:italic;margin-left:auto;">PD/HR action — KPR MOC-ASEER-SIC-1K0-KP-0001</span>
  </div>
  <table style="font-size:0.42rem;">
    <thead><tr><th style="width:20%;">Role</th><th>Update Needed</th><th style="width:18%;">Action By</th></tr></thead>
    <tbody>
      <tr><td>[Role]</td><td>[Description of change needed]</td><td>PD/HR</td></tr>
    </tbody>
  </table>
  <p style="font-size:0.4rem;color:var(--text-muted);margin:2px 0 0 0;font-style:italic;">Roles marked TBC pending appointment. Plan references KPR as live source of truth.</p>
</div>
```

### CRITICAL: Strip Before CG Submission

The entire KPR Action Note block is **INTERNAL USE ONLY**. Before generating the final CG submission HTML:

1. Delete the entire `<div>` block (the amber callout box) from the HTML
2. Do NOT leave any trace — no placeholder comments, no hidden divs
3. The KPR Action Note exists only in internal drafts; the CG submission document must be clean of all PD/HR housekeeping

## Pitfalls

- **Do NOT submit internal housekeeping blocks to CG.** The KPR Action Note (amber callout box listing PD/HR tasks) must be STRIPPED before generating the CG submission HTML. CG reviews roles and compliance, not internal staffing process. Same rule applies to any "PD recommendations" language in revision history or cover descriptions — rewrite as neutral "Updated: [what changed]" before submission.
- **Do NOT add a role to the plan just because PD mentioned it without first verifying against DMP T2 list (14 roles) and SOW §5.5 minimum staffing.** If absent from both, the role is likely redundant — existing roles may already cover the scope. Example: PD asked for "Humidity/Environmental Specialist" but it's not in DMP T2, not in SOW §5.5, and the scope (RH control, conservation environment) is already covered by Glasbau Hahn (showcase micro-climate) and AD Engineering (MEP HVAC). Flag this to the user and let them decide on merge vs drop.
- **Do NOT carry forward headcount numbers from a previous plan revision without documented basis.** The user (or CG) will ask "how was the peak calculated?" and you need a traceable answer.
- **Do NOT use calendar dates (DD-MM-YYYY) for milestones when D0 is provisional.** Use D-NN references throughout. Add a note that D0 = provisional.
- **Do NOT report peak headcount without contingency context.** State whether the peak includes or excludes the +10% allowance so reviewers understand the buffer.
- **Do NOT place the peak at D88 (AFC).** The peak should occur BEFORE AFC (around G3/D65) when the design team is at maximum and site mobilization has begun — the overlap creates the surge. Post-AFC, design roles roll off.
- **Do NOT assume a 5-day work week.** KSA construction uses Sat–Thu. A 7-day week assumption overstates available working days by 40%.
- **Do NOT include roles in P1 that can only be mobilized after LOA (D0).** Pre-LOA = core management only (PD 50%, BIM Manager 50%, Doc Control part).
- **Do NOT skip the Validation row in the Basis of Estimate.** Benchmarking against comparable projects is what makes the estimate defensible to CG reviewers.
- **Do NOT forget to cross-reference the Resource Risk Register.** If the headcount depends on an unapproved schedule, flag it as a risk.
- **Do NOT blank on-board personnel names.** "Pending submission" in KPR means the person IS on board — keep their name. Do NOT write "pending MoC submission" as a label. For Code C, keep the name and write "submission in progress" — never write "Code C (revise & resubmit)" in plan documents. Cross-reference against KPR to verify status before every submission — see KPR Cross-Referencing section above.
- **Do NOT invent Tier 1 roles outside the KPR.** Tech Office Manager, for example, is an internal Samaya role but NOT a KPR Tier 1 role. Only the 6 KPR Tier 1 roles should appear in the Tier 1 org chart.
- **Do NOT use `execute_code` to read OneDrive xlsx files.** The sandbox's fcopyfile times out on cloud-synced paths. Use `terminal` with system `python3` instead.
- **Do NOT mention "Overseas" or non-project-site cities** (Dubai, London, Egypt) in plan documents. Only Riyadh and Abha are location references.
- **Do NOT use "on-site" for personnel not physically at site.** Use "appointed" instead.
- **Do NOT use `ws.insert_rows()` in OneDrive-synced KPR Excel files.** It silently loses data on save — the row appears inserted in memory but values vanish after save+reopen. Write directly to the first empty row before the STATUTORY header instead.
- **Risk Register in HTML plans — use card grid, not plain table.** See "HTML Risk Register Card-Grid Design" section below.
- **Do NOT list brand names in the Materials RBS section.** Use generic material descriptions. Brand/supplier names are only acceptable once formally approved — not during draft/pre-submission stages. See "Brand Names in Materials Section" above.
- **Do NOT submit C03 as first CG issue.** First formal submission is ALWAYS Rev C00. Strip internal draft history from the revision log. Renumber the file, cover, footers, section tags, and revision history table.
- **Do NOT include "Vacant" names or invent appointees.** If PD asks you to fill a vacancy, politely flag it as their hiring action. Do not fabricate a name to make the plan look complete.
- **Do NOT let the resource plan's §3 org chart diverge from the DMP's organization chart.** The DMP (Design Management Plan) defines the project's authoritative Tier 1/2/3 hierarchy. The Resource Management Plan must mirror it. Key checks: (a) Tier 1 role names must match DMP (DMP uses "Site Manager" not "Construction Manager" — align naming); (b) Tier 2 design specialists (14 per DMP Rev C04) must be listed, not replaced by internal Samaya BIM coordination roles; (c) roles present in the resource plan but absent from DMP (e.g. Tech Office Manager as separate Tier 1 card) should be flagged. Read the latest DMP HTML and compare §3 side-by-side before submitting.
- **Do NOT confuse internal Samaya BIM coordination roles with Tier 2 design discipline roles.** The DMP's 14 Tier 2 roles are DESIGN SPECIALISTS (Structural, MEP, FLS, AV, Lighting, Showcase, Setworks, Interactives, Models, Graphics, Café Shade, Landscape, Architecture, Interior). The resource plan's Tier 2 table currently shows BIM coordination roles (Arch-Str BIM Coord, MEP BIM Coord, Arch BIM Lead, Mech BIM Lead) which are internal execution roles, not the DMP's design specialist classification. Both tiers can coexist — but the DMP's 14 must be explicitly present.
- **After bulk-renaming a role (e.g. "Construction Manager" → "Site Manager"), always audit for duplicates in the §3.2 Construction chart.** The rename tool operates globally, so if the 3.2 chart originally had both a "Site Manager (TBC)" card AND a "Construction Manager (Eng. Mohamed Samir)" card, after rename both become "SITE MANAGER" — creating an obvious duplicate. Post-rename, grep for the old and new names to verify no double-ups exist. Remove the duplicate card from 3.2 and keep only one instance (Eng. Mohamed Samir already appears in Tier 1).
- **Do NOT assign a single named individual per role when the user wants co-leads.** When the user says "add Mohamed Mostaga with Ahmed Ghoneim to be full time", it means BOTH people share the role. Format as `Eng. Ahmed M. Ghoneim · Eng. Mohamed Mostaga` with a `·` (middle dot ·, U+00B7) separator, not as separate rows. Bump the type pill to FT (navy) if the user says "full time".
- **Do NOT mention unapproved subcontractors/firms anywhere in the plan.** A firm with status "prequal ongoing", "NDA signed", "scope under negotiation", or any status short of formal appointment/CG approval must be removed from ALL plan sections — not just hidden from the names column. Remove them from: RBS sub-contractor lists, induction step descriptions, mobilization notes, Exhibition Team Matrix rows, risk register descriptions, companion documents list, and any document codes referencing their SOW. Restore only once formal CG approval is recorded in the KPR.
- **BUT: Do NOT remove the role itself if it's contractually mandated.** SOW §5.5 defines a minimum staffing list. If a role appears there (e.g. Mechanical & Electromech Interactives Specialist), the role stays in the plan as "TBC" even if its assigned firm is unapproved. Remove only the firm name, not the role.
- **Do NOT reply to PD comments with just a plan for action.** Classify each item into 🔴 PD action / 🟡 we build / 🟢 we improve. PD expects a clear split of responsibility, not vague promises.
- **Do NOT omit PD's own template doc from analysis.** PD may attach a reference structure document along with their email. Read it, compare against existing plan, and explain what your plan already covers that theirs doesn't — prevents unnecessary redesign.

## Handling PD (Project Director) Review Comments

When the PD sends review comments on a Resource Management Plan (typically as bullet points or a reference template), classify each item into one of three categories:

| Category | Icon | Action | Examples |
|----------|------|--------|---------|
| **Appointment / Hiring** | 🔴 | Flag as **PD/HR action** — cannot fill from the plan. Update KPR vacancy status; plan shows "Vacant" or "TBC" until appointed. | "Fill QA/QC Manager", "Nominate T&C Manager" |
| **Plan Content — Add** | 🟡 | Build into the plan — new section, table, matrix, or chart. These are the team's scope. | RACI Matrix, Succession Matrix, stacked histogram, new specialist roles (Accessibility, Acoustic, Environmental) |
| **Plan Content — Improve** | 🟢 | Expand existing section that partially addresses the request. | Convert headcount curve to stacked-by-discipline histogram, expand sub-contractor table into Exhibition Team Matrix |

### Common PD Requests and Where They Go

| PD Says | Category | What to Do |
|---------|----------|------------|
| "Fill QA/QC Manager" | 🔴 PD action | Flag as appointment. Plan shows "Vacant". PD must assign. |
| "Nominate T&C Manager" | 🔴 PD action | Same — PD/HR appoints. |
| "Add [X] Consultant" | 🟡 Add to plan | Add to Tier 2 or §7.3 Sub-Contractor table. Verify against SMP Rev03 and KPR for correct entity names. |
| "Add Construction Resource Org Chart" | 🟡 Add new chart | Add dedicated P4-phase site hierarchy chart (Site Manager → Trade Supervisors → Foremen → Crews). |
| "Add Specialist Exhibition Team Matrix" | 🟢 Expand | Expand §7.3 Sub-Contractor table into a proper matrix with: Specialist, Package Code, Discipline, Phase, Deliverables, CG Status, Dependency, Integration Mechanism. |
| "Add RACI Matrix" | 🟡 New section | Add RACI covering: resource mobilization, demobilization, change requests, risk responses, quality inspections, sub-contractor approvals, KPR updates. |
| "Add Detailed Manpower Histogram" | 🟢 Improve §5 | Replace or supplement single-series headcount curve with stacked histogram showing headcount by discipline/role category across P1–P5. |
| "Add Succession Matrix" | 🟢 Add table | Add table: Role × Primary × Deputy/Backup × Handover Period. Cover all Tier 1 and critical Tier 2 roles. The succession protocol may exist (§7.2) but the matrix is separate. |

### Response Template to PD

```
Re: Resource Management Plan Review

Noted. Below is how we'll address each item:

Items we will add to Rev C01 (our build scope):
- [list items 3-10 with brief description]

Items requiring PD appointment action:
- [list items 1-2: QA/QC Manager, T&C Manager]

The existing Rev C00 structure already covers [document governance /
tier framework / location matrix / phase loading / risk register /
CG compliance clauses] that form the foundation. We will layer your
additional items on top without losing existing features.
```

## Revision Numbering Convention for Plan Documents

**First CG submission is ALWAYS Rev C00**, regardless of internal draft numbering:

| Revision Type | Numbering | Status Badge |
|---------------|-----------|--------------|
| Internal drafts | C01, C02, C03... | DRAFT · INTERNAL REVIEW |
| First formal submission | **C00** (not C03) | ISSUED FOR CG REVIEW |
| After CG Code C | C01 (incorporates CG comments) | ISSUED FOR CG REVIEW |
| After CG Code B | C01/C02 (incorporates conditions) | APPROVED / ISSUED FOR IMPLEMENTATION |

**Rule:** If internal drafts reached C03 but it's the first time going to CG, renumber to C00. Do not submit C03 as a first issue — the revision history must show a clean C00 → C01 → C02 trajectory for CG/PMC audit.

**Revision history in the document:** Strip all internal draft entries. Show only formal revisions (C00 = first CG issue, C01 = after first CG review, etc.).

## Plan Content Boundary — What We Put in the Plan vs What PD/HR Must Do

The resource management plan documents **roles and organizational structure** but does NOT appoint individuals. Boundary:

| Aspect | Our Scope (in plan) | PD/HR Scope |
|--------|-------------------|-------------|
| Role definitions | ✅ Org chart, RACI, responsibility matrix | ❌ Hiring/firing individuals |
| Vacant roles | ✅ Show as "Vacant" or "TBC" | ✅ Must fill via KPR process |
| Named persons | ✅ List approved KPR names | ✅ Submit CVs, obtain MoC approval |
| Skill requirements | ✅ Competency matrix, training plan | ✅ Recruit/assign qualified people |
| Headcount estimates | ✅ Histogram, FTE loading, Basis of Estimate | ✅ Approve budget for headcount |

**Never invent a name** for a vacant position just to make the plan look complete.
**Never remove** a placeholder (TBC/Vacant) because it looks weak — it's honest and expected.

## Mandatory PMBOK Additions — Commonly Requested by PD and CG

When upgrading a basic Resource Organization Plan to a full PMBOK-compliant Resource Management Plan, the following are commonly requested:

| PMBOK Area | What to Add | Where in Plan |
|------------|-------------|---------------|
| Resource Breakdown Structure (RBS) | Hierarchical decomposition: Human Resources, Equipment & Plant, Materials, Facilities, Services | §3.1 (after org chart) |
| Physical Resource Management | Equipment acquisition/inspection/maintenance, material procurement/storage/inventory | §6.4 |
| Training & Competency | Training matrix (induction, BIM, safety, quality, specialist). Competency verification process. | §7.4 |
| Team Charter & Conflict Resolution | Team values, Tuckman model, conflict escalation, health/welfare. | §7.5 |
| Resource Control | Plan vs actual comparison, variance analysis, corrective actions, monitoring tools, change control. | §9 |
| Plan Governance | Living document clause, phase transition, compliance declaration, escalation matrix. | §10 |

## Construction Resource Organisation Chart (§3.2)

When PD requests a "Construction Resource Organization Chart", add a dedicated P4-phase site team hierarchy after the main Tier 1/2/3 org chart:

### Chart Structure

```
Project Director
    └── Construction Manager
        ├── Site Manager (TBC — target CP-1)
        │   ├── Trade Supervisors (3-4): MEP, Finishes, Setworks/Joinery, AV/Lighting
        │   │   └── Foremen / Chargehands
        │   │       ├── Skilled Labour (carpenters, MEP fitters, metal workers, painters, AV installers)
        │   │       └── General Labour
        │   └── Site Engineer (Planning)
        ├── QA/QC Inspector
        ├── HSSE Manager
        └── Storekeeper
```

### HTML Card Format

```html
<div style="border:1.5px solid var(--primary);border-radius:4px;padding:6px 10px;margin-bottom:4px;background:var(--bg-light);">
  <div style="display:flex;align-items:center;gap:6px;margin-bottom:3px;">
    <b style="font-size:0.6rem;color:var(--primary);">P4 Site Execution Team</b>
    <span style="font-size:0.45rem;color:var(--text-muted);font-style:italic;margin-left:auto;">SoW §5.5 Staffing &amp; Deployments · §10 On Site Fit-Out</span>
  </div>
  <div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:3px;">
    <!-- Three-card top row for Site Manager, Construction Manager, HSSE Manager -->
  </div>
  <table style="font-size:0.45rem;margin-top:4px;">
    <thead><tr><th>Role</th><th>Responsibility</th><th style="text-align:center;">Commitment</th></tr></thead>
    <tbody>
      <tr><td><b>Site Manager</b></td><td>Overall site delivery, coordination, safety compliance, daily reporting</td><td style="text-align:center;">FT</td></tr>
      <tr><td><b>Trade Supervisors (3-4)</b></td><td>MEP, Finishes, Setworks/Joinery, AV/Lighting oversight per discipline</td><td style="text-align:center;">FT</td></tr>
      <tr><td><b>Foremen / Chargehands</b></td><td>Direct labour supervision, quality checks, material management</td><td style="text-align:center;">FT</td></tr>
      <tr><td><b>Skilled Labour</b></td><td>Carpenters, MEP fitters, metal workers, painters, AV installers</td><td style="text-align:center;">FT</td></tr>
      <tr><td><b>General Labour</b></td><td>Assistance, material movement, cleaning, waste removal</td><td style="text-align:center;">FT</td></tr>
      <tr><td><b>Site Engineer (Planning)</b></td><td>Short-term look-ahead, resource tracking, daily diaries</td><td style="text-align:center;">FT</td></tr>
      <tr><td><b>QA/QC Inspector</b></td><td>In-process inspections, ITP sign-off, NCR tracking</td><td style="text-align:center;">FT</td></tr>
      <tr><td><b>Storekeeper</b></td><td>Material receiving, inventory, tool issuance</td><td style="text-align:center;">FT</td></tr>
    </tbody>
  </table>
  <p style="font-size:0.4rem;color:var(--text-muted);margin:2px 0 0 0;font-style:italic;">Construction team sizes confirmed once Master Programme approved and MEP/FF&E packages awarded.</p>
</div>
```

## Succession Matrix (§7.2a)

When PD requests a "Succession Matrix" (complementing the existing Replacement Protocol), add a table showing primary and deputy/backup for each critical role:

### Succession Matrix Template

| Role | Primary | Deputy / Backup | Handover Period |
|------|---------|----------------|-----------------|
| Project Director | [Name] | [Name/Group] | 4 weeks (SoW §5.5) |
| Construction Manager | [Name] | Project Director (interim) | 2 weeks |
| BIM Manager | [Name] | Arch BIM Lead / BIM Lead | 2 weeks |
| HSSE Manager | [Name] | Construction Manager | 2 weeks |
| QA/QC Manager | [Vacant — PD action] | — | — |
| T&C Manager | [TBC — PD action] | — | — |
| Tech Office Manager | [Name] | BIM Manager | 1 week |
| MEP Coordinator | [Name] | — | 2 weeks |
| NRS Design Lead | [Name] | NRS Alternate | 2 weeks |
| Submittals Coordinator | [Name] | Doc Controller | 1 week |

### Rules

- QA/QC and T&C Manager roles show "Vacant" / "TBC" with annotation "PD action pending" — do not invent names
- Deputy assignments are provisional — formal deputisation requires MoC notification per SoW §5.5
- Role schedule §5.2 FTE commitment determines handover feasibility (can a deputy cover both roles?)
- Add footnote: "All deputy assignments provisional — formal deputisation requires MoC notification per SoW §5.5"

## Specialist Exhibition Team Matrix (§7.3)

When expanding the sub-contractor table into a full Exhibition Team Matrix, add these columns beyond the basic Sub-contractor + Discipline + Phase + Integration:

| Specialist | Package Code | Discipline | Active Phase | Key Deliverables | CG Approval Status | Dependency / Integration |
|------------|-------------|-----------|-------------|-----------------|-------------------|------------------------|
| [Firm Name] | [Doc Ref] | [Discipline] | [Phases] | [Specific deliverables] | [Code A/B/C + date] | [Prerequisite/interface] |

### Data Sources for Each Column

| Column | Data Source | Rule |
|--------|------------|------|
| **Specialist** | KPR + SMP Rev03 | Use correct entity names per KPR (e.g. "Nama Consulting" not "Nama Al Amal") |
| **Package Code** | CG site instructions, SOW references, DMP appendices | Include actual document codes (ZD-0026, MA-0006, PQ-013, etc.) |
| **CG Approval Status** | CG_STATUS.md, KPR status column | Map to pill colors: green=Approved, amber=Code B, red=Code C, slate=TBC |
| **Key Deliverables** | SOW §6.22, SMP scope descriptions | Be specific: "Showcase drawings + schedules + micro-climate design + FAT/SAT" |
| **Dependency** | Master Programme logic | What must complete before this specialist can start (e.g. "Requires AFC package") |

### Status Pill Mapping

| CG Status | Pill Style | HTML Class |
|-----------|-----------|------------|
| Approved | Green | `pill-green` |
| Code B — Approved w/ Comments | Amber | `pill-amber` |
| Code C — Revise & Resubmit | Red (inline) | `background:#B91C1C;color:white` |
| Prequal ongoing / TBC | Slate | `pill-slate` |

## RACI Matrix for Resource Management (§7.6)

When PD requests a "RACI Matrix" as a new standalone section, use this template:

### Columns (Roles)

Use abbreviations to fit on A4: PD (Project Director), SM (Site Manager — NOT "CM" since DMP uses Site Manager), BIM (BIM Manager), TOM (Tech Office Manager), QA (QA/QC Manager), HSSE (HSSE Manager), DC (Document Controller), NRS (NRS Design Lead interface)

**Abbreviation rule:** Match the role name used in Tier 1. If the DMP says "Site Manager", use `SM` not `CM`. Update both the RACI header AND the RBS abbreviation list (e.g. `PD, SM, BIM Mgr, Tech Office Mgr, QA/QC Mgr`).

### Rows (Activities)

Cover these resource management activities at minimum:

| Activity | PD | SM | BIM | TOM | QA | HSSE | DC | NRS |
|----------|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|
| Resource Mobilization | A | R | C | C | I | I | C | I |
| Induction & Onboarding | A | I | C | C | C | R | C | I |
| Equipment Procurement | A | R | I | I | C | C | C | I |
| Material Requisition | I | A | I | C | C | I | R | I |
| Sub-contractor Onboarding | A | R | C | R | C | C | I | C |
| KPR Update | A | I | C | R | I | I | R | I |
| Demobilization | A | R | C | C | I | I | R | I |
| Training Needs Assessment | A | C | R | C | C | R | I | I |
| Succession Planning | A | C | C | C | I | I | I | I |
| Risk Response | A | R | C | R | C | C | I | I |

### Legend

- **R** = Responsible (does the work)
- **A** = Accountable (approves — one per activity)
- **C** = Consulted (input before decision)
- **I** = Informed (notified after decision)

### Design Rules

- Use 8 role columns max — more than 8 won't fit on A4 landscape
- If more roles needed, split into two matrices (strategic + operational)
- Add footnote: "Full RACI Matrix maintained in project EDMS"
- Place after Team Charter (§7.5) and before Demobilization (§8)

## KPR Snapshot — Handling Unapproved Names

When individuals have not been approved (status "Pending submission", "Code C", "Nominated"), use the following approach instead of naming them in the plan:

### Principle

> **Plans document structure, not people. The KPR is the people register. We reference it, we don't duplicate it with unapproved names.**

### How to Reference

In the Companion Documents section (§10.5), add:

```html
<li><b>Key Personnel Register (KPR)</b> · <code>MOC-ASEER-SIC-1K0-KP-0001</code> Rev C05 (live)
    — submitted alongside this plan as a companion snapshot. All named personnel, CV statuses,
    and MoC approval decisions are maintained in the KPR as the single source of truth.</li>
```

### What Goes Where

| Situation | In Plan | In KPR Snapshot |
|-----------|---------|----------------|
| Approved individual | Show name in plan | In KPR with status "Approved" |
| Firm approved, individual not | Show FIRM NAME only | Individual status in KPR |
| Subcontractor in prequal / NDA stage | **REMOVE all references from plan** | Not in plan until formally appointed |
| Vacant role | Show "Vacant" | Listed with status |
| TBC (not yet appointed) | Show "TBC" | Listed as vacant |
| Pending submission | Show FIRM or role title, not individual name | Individual in KPR with "Pending submission" |
| Code C (resubmit) | Show FIRM or role title, not individual name | Individual in KPR with "Code C" |

This protects the plan from needing revision when CVs are approved — the KPR snapshot is updated independently.

## Page Overflow — Splitting Long Pages

When content on any single A4 page exceeds approximately **95 lines of HTML** or **10,000 characters** (including markup), it will overflow the 297mm printable height (~1030px at 96dpi vs typical content of 1200-1500px for dense tables). This affects all sections, not just the org chart.

### Detection

Check page sizes after every major content edit. Thresholds that signal overflow:
- **>95 lines** of raw HTML between page markers → very likely to overflow
- **>10,000 chars** of content → high risk, check visually
- **>25 table rows** on one page → must split
- **Tables + SVG + bullet lists** combined on same page → always too tall

### Split Strategy

Split at natural content boundaries. General approach:
1. Identify the last complete logical block that fits (close table, close section div)
2. Insert `</section>` + page footer
3. Create new `<section class="page">` with header, title, and continued content
4. Use header-info text reflecting the split (e.g. "05.02 CONSTRUCTION TEAM SCHEDULE" for a continued table)

**Example — Role Allocation table (45 rows + SVG chart):**
The page has an SVG chart (full viewBox) plus a 36-row role table. Too tall for one page.

PAGE 07: [SVG chart + caption + footer] /section
PAGE 08: [Role table header + T1+T2 rows + footer] /section
PAGE 09: [Role table header + T3 rows + Construction rows + footer] /section

Key points when splitting tables mid-content:
- Each continuation page MUST have its own <thead> with full column headers — the browser doesn't repeat thead across section breaks
- Close the table (/tbody /table) before the footer, not after
- Add the legend line after every table close (users shouldn't have to flip back)
- The split point between T2 and T3 should be at the section header row (after the last T2 row, before the T3 section header)

**Example — Location Matrix (16 rows + Office Setup grid):**
The Location Matrix fits one page; the Office Setup 2-column grid + Deadline table need a second page.

PAGE 08: [Location Matrix table + legend + footer] /section
PAGE 09: [Office Setup grid + Deadline table + footer] /section

**Example — Org structure (T1+T2+T3+Construction chart):**
Split after Tier 2 legend line, before Tier 3 section header. Page 4 = T1+T2, Page 4b = T3+Construction.

### After Splitting

- Update `.page-number::after { content:"DOC PAGE " counter(page-counter) " OF N"; }` with new total
- Verify: `grep -c '<section class="page"'` matches N
- Continued tables need their own `<thead>` if split mid-table
- **Page balancing**: After splitting, check if adjacent pages have roughly equal row counts. If one page has 25 rows and the next has 11, move the split point to balance. Target: within 20% of each other.
- **Within-table balancing**: When a section (e.g. T2 Design Specialists, 19 rows) is the bulk of content, split INSIDE it rather than cutting at a section boundary. Count total rows across both pages and divide evenly. Example — T1(6) + T2(19) + T3(11) = 36 total rows. Split at row 18 (after Landscaping, the 12th T2 row) so page 8 = T1+first 12 T2 (18 rows) and page 9 = last 7 T2+T3 (18 rows). Use a `(cont.)` header on the continuation page for the split section.
- **When splitting mid-T2**: add a `<tr><td colspan="6" style="background:...">Tier 2 — Design Specialists (cont.)</td></tr>` header row on the second page so the reader knows the table continues. Also update the page header-info to "(CONTINUED)".
- **After splitting**: re-read the merged boundary area to check for orphaned `</tbody>`, misplaced section headers, or row ordering errors. A common bug is the T3 section header row landing AFTER the first T3 data row instead of before it.
- **Checking programmatically**: Measure lines between `<section class="page">` markers with python: `grep -n '<section class="page"' file.html | wc -l`. Then for each page, check `wc -c` of the content between markers. Pages over ~95 lines likely overflow A4.

### Merging Pages (removing page breaks)

When merging a split page back:

1. Remove the page footer + `</section>` of the first page
2. Remove the HTML comment + `<section>` + header block of the second page
3. Connect content directly — if a table was split, continue the `<tbody>` into the next section
4. Decrement the OF count by 1
5. Remove stale HTML comments referencing the merged page

**Pitfalls when merging table pages:**

- **Do NOT leave orphaned `</tbody></table>` before the merge point** — removing the page break but keeping the close tags severs the table connection. Delete the premature close tags so row content flows into the existing open `<tbody>`.
- **Do NOT forget the section header row** — after removing the page break + header block, the second page's section header row (e.g. `Tier 3 — Support`) may be lost. Re-insert it between the last row from page 1 and the first row of page 2's content.
- **Check row order** — after inserting the section header, verify rows are in correct sequence (last row of section A → new section header → first row of page B). The merge may insert the header AFTER the first data row if the script order was wrong.
- Verify: `grep -c '<section class="page"'` matches the new page count
- Continued tables need their own `<thead>` if split mid-table

### Anti-patterns

- **Do NOT reduce font sizes** to squeeze everything onto one page
- **Do NOT combine** unrelated sections on same page to save pages

## HTML Page Structure & Print Layout

When building HTML plan documents for A4 print:

- Use `@page { size:A4; margin:0; }` in CSS
- Each page: `<section class="page">` with `width:210mm; min-height:297mm; padding:12mm 16mm;`
- Cover page: `<section class="page page-cover">` with dark navy background
- Footer uses `margin-top:auto` to stick to bottom via flexbox
- Page counter: `.page { counter-increment:page-counter; }` + `.page-number::after { content:"DOC PAGE " counter(page-counter) " OF N"; }`
- Verify total pages match the N in the CSS counter after every structural edit

## HTML Risk Register Card-Grid Design

For the Resource Risk Register section (§8.3 or equivalent) in an HTML plan document, use a 2-column card grid with color-coded severity instead of a plain table. This is more readable on A4 print and visually communicates risk priority.

### Layout

```html
<div style="display:grid;grid-template-columns:1fr 1fr;gap:5px;">
  <!-- One card per risk -->
</div>
```

### Card Template (per risk)

```html
<div style="border:1px solid var(--border);border-left:3px solid {COLOR};border-radius:4px;padding:6px 8px;background:{BG};">
  <div style="display:flex;align-items:center;gap:4px;margin-bottom:3px;">
    <span style="background:{COLOR};color:white;font-size:0.4rem;font-weight:800;padding:1px 5px;border-radius:2px;">R{N}</span>
    <span style="font-size:0.4rem;color:{DARK};font-weight:700;text-transform:uppercase;letter-spacing:0.04em;">{SEVERITY}</span>
  </div>
  <div style="font-size:0.5rem;font-weight:700;color:var(--primary);margin-bottom:2px;">{RISK TITLE}</div>
  <div style="font-size:0.42rem;color:var(--text-muted);margin-bottom:3px;">{IMPACT}</div>
  <div style="font-size:0.42rem;color:var(--text-main);border-top:1px dashed {DASH};padding-top:2px;"><b>Mitigation:</b> {MITIGATION}</div>
  <div style="font-size:0.38rem;color:var(--text-muted);margin-top:2px;"><b>Owner:</b> {OWNER}</div>
</div>
```

### Color Scheme

| Severity | Border + Badge | Background | Dark Text | Dashed Separator |
|----------|---------------|------------|-----------|-----------------|
| High | `#EF4444` | `#FEF2F2` | `#991B1B` | `#FECACA` |
| Medium | `#F59E0B` | `#FFFBEB` | `#92400E` | `#FDE68A` |
| Low | `#22C55E` | `#F0FDF4` | `#166534` | `#BBF7D0` |

### Legend (below the grid)

```html
<p style="font-size:0.38rem;color:var(--text-muted);margin:5px 0 0 0;font-style:italic;">
  <span style="background:#EF4444;color:white;font-size:0.35rem;font-weight:800;padding:1px 4px;border-radius:2px;">High</span> immediate action ·
  <span style="background:#F59E0B;color:white;font-size:0.35rem;font-weight:800;padding:1px 4px;border-radius:2px;">Medium</span> monitor &amp; track ·
  <span style="background:#22C55E;color:white;font-size:0.35rem;font-weight:800;padding:1px 4px;border-radius:2px;">Low</span> plan ahead
</p>
```

### Design Rules

- Each card shows: Risk ID badge, severity label, risk title, impact, mitigation (with dashed separator), owner
- 2 columns on A4 — fits ~8 risks on one page
- Remove internal annotations like "Expanded for C00" from the section header
- Content should be sourced from real project risks (Master Programme status, personnel gaps, sub-consultant delays, ITCA critical path)
- Risk R5 should reference the actual Master Programme status from the Register Log (e.g. "Under Review by CG since 09-May-2026")

## Reference Files

- `references/aseer-dmp-tier-mapping.md` — DMP Rev C04 tier-to-role mapping for Aseer Museum
- `references/kpr-plan-two-way-sync.md` — Two-way KPR ↔ Plan sync workflow, entity name alignment, and direct KPR editing when user provides the file
