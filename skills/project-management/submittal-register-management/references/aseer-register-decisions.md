# Aseer Museum — Register Scope Decisions

Final state as of 01 July 2026. Updated: FLS Submission Plan created (36 items, 13-column gate format, CG approval authority). AV template now the standard for all discipline submission plans.

## Registers in 04_Registers

| # | Register | Items | Data Source | Dates? | Ref Format |
|---|----------|-------|-------------|--------|------------|
| 1 | Arch_Submittal_Register | 67 | NRS Gates Submission Plan + BOQ | ✅ Staggered (BF 29/06 → 1F 20/07) | MOC-ASE-AR-ARC-{FL}-DDD-{CAT}-00 |
| 2 | Acoustic_Submittal_Register | — | SOW template | ✅ | AR-xxx |
| 3 | AV_Submittal_Register | 16 | SOW template | ✅ | AV-xxx |
| 4 | CITC_Telecom_Submittal_Register | 6 | SOW template | ✅ | CT-xxx |
| 5 | FFE_Submittal_Register | 266 | BOQ 004. Furniture (6 zones) | ✅ Per zone (LB1 29/06 → LR 03/08) | FF-xxx |
| 6 | FLS_Submittal_Register | 36 | 24_Subcontractors register (real) | ✅ Staggered (Strategy 29/06 → Coordination 20/07) | FL-xxx |
| 7 | Graphics_Submittal_Register | 120 | BOQ_QTY_EXTRACT (39 line items, 5 groups) | ❌ No dates — RFI pending client research/data | GR-xxx |
| 8 | Interactives_Submittal_Register | 54 | Tactile & Manual Schedule (6 objects) | ✅ 15/07 staggered +7d per object | IN-xxx |
| 9 | Landscaping_Submittal_Register | — | SOW template | ✅ | LS-xxx |
| 10 | Lighting_Submittal_Register | 35 | Studio ZNA scope doc (8 sections 1.1–1.8) | ✅ 10/07 staggered +7d per cat | LI-xxx |
| 11 | MEP_Submittal_Register | 11 | SOW template | ✅ | ME-xxx |
| 12 | Model_Maker_Submittal_Register | 33 | Model & Replica Schedule (5 objects) | ❌ No dates — RFI pending client research/data | MM-xxx |
| 13 | Oddy_Testing_Submittal_Register | 2 | SOW template | ✅ | OD-xxx |
| 14 | Rigging_Submittal_Register | 9 | SOW template | ✅ | RG-xxx |
| 15 | Showcase_Submittal_Register | — | SOW template | ✅ | SC-xxx |
| 16 | Structural_Submittal_Register | 39 | 4-tier dependency model (Surveys→Assessment→Design→IFC) + Rigging merged | ✅ | ST-xxx |
| 17 | QA_Commissioning_Handover_Register | 138 | 8 common items × 16 packages + specific items | ✅ All IFC 28/08 | QA-xxx |

## Registers Deleted

| Register | Reason |
|----------|--------|
| Exhibition_FitOut_Submittal_Register | Completely redundant with Architecture register (NRS scope). Design items in Arch; management items in QA/Handover register. |
| Rigging_Submittal_Register | Merged into Structural as Category E. Items preserved with ST-xxx refs. |

## Architecture Register Coverage

NRS (Architecture register) covers:
- GA plans, sections, elevations (all levels)
- Specifications
- BIM Model
- Material presentations
- Graphic signage/wayfinding (not content)
- Showcase schedules (coordination)
- Object mount schedules (coordination)
- Models & Replicas schedules (coordination)

NOT covered by Architecture (separate subcontractors):
- Graphic content/design
- Showcase fabrication
- Model/Replica production
- Interactives fabrication
- AV/IT systems
- Lighting design/controls
- MEP
- FLS
- Acoustic
- Rigging/structural
- Landscaping

## MOC Drawing Numbering System

Only applies to **Architecture** register. Other discipline registers (MEP, Structural, Lighting, AV) track system-based deliverables, not individual drawing sets organized by floor and category.

Format: `MOC-ASE-{Disc}-{SubDisc}-{Floor}-DDD-{Cat}-{Rev}`
Stage code: DDD = Detailed Design (50%)

Floors: BF, LGF, GF, 1F, GEN
Categories: 1100 (Existing GA), 1150 (Demolition GA), 1200 (Proposed GA), 1210 (Viz Plans), 1220 (Wall Scoping), 1230 (Floor Scoping), 1250 (Ceiling Scoping), 2700 (Setwork Details), 4000 (Existing Sections), 4020 (Demolition Sections), 4050 (Proposed Sections), 5510 (Room Elevations), 2550-2950 (Details & Schedules), Specs (Specifications), Viz (3D Viz), 3DViz (Digital Material Board), BIM (BIM Model), BOQ (MasterFormat BOQ)

## FLS Register

Full replacement from subcontractor register. 36 items, 7 categories:
- A: FLS Strategy (FL-001–006)
- B: Active Fire Protection (FL-007–012)
- C: Passive Fire Protection (FL-013–018)
- D: FLS Coordination (FL-019–024)
- E: Commissioning (FL-025–029)
- F: QA/Commissioning (FL-030–032)
- G: Handover (FL-033–036)

## Structural Register (Updated 30 Jun 2026)

39 items, 5 categories, 4-tier dependency model. Rigging merged as Category E.

**Categories:**
- A — Surveys (Tier 1, 29 Jun start): Dilapidation, laser scan, as-built review, investigation report, design criteria
- B — Assessment (Tier 2, 29 Jul start): Loading assessment, load schedules, site report, core tests, capacity assessment
- C — Design (Tier 3, 11 Sep start): Strengthening design, stairs (2-flight/3-flight), ceiling supports, sunshade, balustrade, ETABS model, opening schedules, GA drawings
- C1 — BIM Models (15 Jul start per BEP): Existing Conditions (LOD 300, 50%+90% only), Scope/Design Model (LOD 300→350→500)
- D — IFC/Handover (Tier 4, 28 Aug): ITP, AFC, material submittals, record drawings, as-built BIM, O&M, training, spares
- E — Rigging (merged from Rigging register): Philosophy, load schedule, suspension points, design details, pull-out test, ITP, O&M

**BIM existing model only goes to 90% (LOD 300 handoff) — no 100% or IFC dates.**
**BIM Scope/Design model goes 50%→90%→100% — no IFC.**

## Lighting Register (Studio ZNA)

35 items, 8 categories mapping to ZNA scope sections 1.1–1.8:
- A: Design Philosophy (1) — 4 items
- B: Preliminary Design (1.1) — 4 items
- C: Detailed Design (1.1–1.5) — 5 items
- D: Coordination (1.0) — 4 items
- E: Conservation & Compliance (1.6) — 4 items
- F: BOQ & Value Engineering (1.7) — 3 items
- G: Mock-Up & Sample Review (1.8) — 2 items
- H: IFC/Commissioning/Handover (Samaya internal) — 9 items

50% start: 10/07/2026, staggered +7d per category.

## FF&E Register

Scope: **Loose furniture only** per BOQ 004. Furniture. Pick list includes:
- Lobby (LB1): Dining chairs, sofas, coffee tables, rugs, baggage scanner
- VIP Space (VI): Curtains, coffee tables
- Children's Education (EC): Curtains
- Café & Terrace (CA): Armchairs, dining chairs, sofas, tables, curtains, outdoor lounge chairs
- Circulation (CL1.1F): Dining chairs, sofas, coffee tables
- Library (LR): Coffee tables, dining chairs, armchairs

Each product tracks: Catalog → TDS → Cut Sheet → Sample → Compliance → Warranty → O&M

## Interactives Register

6 tactile/manual/hybrid interactive objects from 6930_Aseer_Tactile & Manual Interactives Schedule:
- 04.05_MI_01 — Architecture Interactive (G4 Saudi Art)
- 05.02_MI_01 — Making Space Interactive (G5)
- 08.04_MI_01 — Al Qatt Interactive (G8)
- 09.03_HI_01 — Sensory Smell Interactive (G9 Flowersmen) — HYBRID
- 12.05_MI_01 — Archaeology Touch Interactive (G12) — TACTILE
- 12.05_MI_02 — Archaeology Rubbing Interactive (G12)

50% start: 15/07/2026, staggered +7d per object.
Steps: Concept Approval → Material Approval → Prototype → Production → QC → Installation → QA → O&M

## QA/Handover Register Structure

8 common items × 16 packages = 128 base items. Plus per-package specific items (Material Test Reports for Arch, BMS Integration for MEP, Civil Defense for FLS, Load Testing for Rigging, Compliance Statement for Oddy) = ~138 items total. All at IFC stage only (28/08/2026).
