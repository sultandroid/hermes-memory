---
name: "design-interface-risk-analysis"
title: "Design Interface Risk Analysis"
description: "Systematic cross-interface risk analysis across multiple design disciplines (Structural, FLS, Acoustics, Accessibility, MEP). Identify contradictions, gaps, and uncoordinated assumptions at discipline boundaries from scheme-stage design reports."
category: "project-management"
triggers:
  - "cross-interface risk analysis"
  - "multi-discipline design review"
  - "interface coordination"
  - "design gap analysis across reports"
  - "review structural, FLS, acoustics, accessibility coordination"
  - "design discipline contradiction check"
priority: "standard"
version: "1.0"
---

# Design Interface Risk Analysis

A systematic method for reviewing multiple design discipline reports and identifying cross-interface risks — contradictions, gaps, uncoordinated assumptions, and unresolved dependencies between disciplines.

## When to use

- A design package includes reports from ≥3 disciplines (Structural, FLS, Acoustics, Accessibility, MEP, Lighting, etc.)
- You need to answer: "What happens if we build this design as-is, without coordinating these disciplines?"
- Pre-appointment design review, RIBA Stage 3 gateway, IFC readiness check
- Any Samaya/Aseer Museum project where discipline reports are submitted separately

## Required inputs

- All discipline reports for the same design stage (scheme, developed, etc.)
  - Structural Report (loadings, slab types, beam locations, interventions)
  - FLS / Risk Assessments (fire strategy, evacuation, material ratings)
  - Acoustics Report (RT targets, NR criteria, vibration limits, treatment products)
  - Accessibility Report (door widths, gradients, turning circles, viewing heights)
  - Interface Statement (base-build ↔ exhibition scope split, deferred scopes)
- Drawing register (to confirm referenced GA sheets exist)
- Any supplementary reports (Visitor Flow, Programming, Lighting, etc.)

## Methodology

### Phase 1 — Independent report digestion

For each report, extract:

| Field | What to extract |
|-------|----------------|
| **Load-bearing requirements** | Every numeric criterion, target, constraint (kN/m², RT60, NR, dB, mm, kg) |
| **Interventions** | Every physical change (new openings, suspended loads, ramp/stair mods, slab infill, new walls) |
| **Gaps** | Explicitly flagged unknowns (missing drawings, deferred checks, assumed weights) |
| **Cross-references** | Every GA number, drawing ref, or other discipline mentioned |
| **Deferred scope** | Items explicitly kicked to "next stage" / "D&B contractor" |

### Phase 2 — Systematic boundary crossing

For each **ordered pair** of disciplines, check:

**STRUCTURAL × FLS:**
- Do structurally modified walls/beams have fire-resistance ratings?
- Are suspended art/AV elements above escape routes?
- Do new stair infills (escalator replacements) have fire-rated construction?
- Are external ramp/egress routes structurally verified and in-scope?

**STRUCTURAL × ACOUSTICS:**
- Do ceiling-mounted acoustic treatments conflict with structural suspension points?
- Is the floor slab's vibration response known (ribbed slabs vs. 0.05 m/s² target)?
- Do structural spreader beams (library) obstruct acoustic ceiling depth?

**STRUCTURAL × ACCESSIBILITY:**
- Are ramp gradients structurally achievable (1:20 on base structures of unknown capacity)?
- Do new window openings avoid hidden columns while meeting viewing-height ranges?
- Is the goods lift capacity verified for MEWP maintenance access?

**FLS × ACOUSTICS:**
- Do lowered sprinklers (for FLS response) intrude into acoustic baffle zones?
- Do smoke-control fans meet gallery noise targets (NR 30)?
- Are fire damper locations compatible with acoustic partition integrity?

**FLS × ACCESSIBILITY:**
- Are accessible refuges identified on every floor where evac distances exceed code max?
- Do relocated fire hose cabinets / lowered sprinklers reduce accessible clear width or headroom?

**ACOUSTICS × ACCESSIBILITY:**
- Do hearing-augmentation induction loops conflict with acoustic wall panel placement?
- Do reconfigurable gallery walls (movable partitions) make fixed acoustic wall panels impossible?

**STRUCTURAL × COLUMN GRID × ARCHITECTURE:**
- Is there a coordinated structural grid GA across all disciplines?
- Are hidden / undocumented columns identified via intrusive survey before architectural GAs are finalized?

### Phase 3 — Severity classification

| Level | Criteria |
|-------|----------|
| **HIGH** | Blocks safety compliance (fire egress, accessible refuge), structural capacity exceeded, or creates design rework if not caught before D&B stage |
| **MED** | Requires coordination resolution at Detailed Design; resolvable with cross-discipline GAs |
| **LOW** | Minor conflict that standard detailing can resolve |

### Phase 4 — Systemic risk identification

Beyond pairwise checks, look for:

1. **Deferred scope inheritance** — Reports that defer work to "D&B contractor" while making commitments that constrain that same contractor (e.g., Fire Strategy deferred but acoustic ceiling treatments + sprinkler lowering already committed)
2. **Missing information on critical path** — Gaps that block multiple disciplines (e.g., missing drawing ST-06 blocking structural stair design, fire-rating, MEP routing)
3. **Unverified assumptions** — Assumed weights, dimensions, or capacities not yet confirmed by the responsible party (art commissioners, FF&E supplier, AV contractor)

### Phase 5 — Deliverable

Write a structured report as a `.md` file with:

- **Risk ID** (discipline-prefixed: S1, A1, FA1, FS1, AD1, G1, P1)
- **Risk title**
- **Evidence** — direct citations from reports with document references
- **Impact** — what happens if not resolved (safety, cost, programme, quality)
- **Mitigation needed** — specific next-step action
- **Severity** (HIGH / MED / LOW)
- Summary table with count per severity
- Document review register (files reviewed)
- Any searched-for items not found (e.g., IFC-0004, specific drawing refs)

## Pitfalls

- **Do not stop at one discipline pair.** A risk may only surface at the 3-way intersection (Acoustics × FLS × Structural via ceiling zone), not any pair alone.
- **Watch for 'In Abeyance' items.** Deferred areas (like EX2 external ramp) often have FLS implications that weren't analysed when they were put on hold.
- **Do not trust assumed weights.** Art commission, AV rack, and FF&E weights labelled "anticipated" or "not expected to exceed" are not verified — flag them.
- **Missing drawings are risks, not footnotes.** If a structural drawing referenced by the report (e.g., ST-06) is missing, it blocks multiple downstream disciplines — flag it centrally.
- **Ribbed slabs are not conventional flat slabs.** Check punch-through risk for point loads, spreaders, and posts over rib junctions.
- **Reconfigurable spaces (movable walls) × fixed acoustic treatment × suspension cables** is a recurring triangle of conflict. Flag it every time.

## Related skills

- `submittal-register-gap-analysis` — audit submittal registers against SOW
- `document-gap-analysis` — compare two related documents
- `project-deliverable-audit` — audit deliverables against requirements
- `compliance-system` — Aseer Museum compliance tracking
- `museum-project-management` — broader PM framework
