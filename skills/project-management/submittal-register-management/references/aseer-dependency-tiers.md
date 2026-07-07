# Aseer Museum — Internal Dependency Tiers per Register

Analysis of which register items can start immediately vs need prerequisite work.
Produced 2026-06-29 during register audit session.

## Structural

| Ref | Item | Tier | Date | Depends On |
|-----|------|------|------|------------|
| ST-001 | Dilapidation survey | 1 — Immediate | 29 Jun | — |
| ST-002 | Cloud survey | 1 — Immediate | 29 Jun | — |
| ST-003 | As-built drawing review | 1 — Immediate | 29 Jun | — |
| ST-004 | Slab/weight loading assessment | 2 — After surveys | 29 Jul | ST-001/002/003 |
| ST-005 | Structural design criteria | 2 — After assessment | 29 Jul | ST-004 |
| ST-006 | Site assessment report | 2 — After surveys | 29 Jul | ST-002/003 |
| ST-007 | Ceiling support design | 3 — After Arch GA | 28 Aug | ST-006 + Arch GA |
| ST-008 | Sunshade design | 3 — After Arch GA | 28 Aug | ST-004 + Arch GA |
| ST-009 | Balustrade design | 3 — After Arch GA | 28 Aug | ST-004 + Arch GA |
| ST-010 | Reinforcement details | 4 — IFC | IFC | ST-007/008/009 |
| ST-011 | Anchoring details (hung) | 4 — IFC | IFC | ST-007 |
| ST-012 | Anchoring details (floor) | 4 — IFC | IFC | ST-007 |
| ST-013 | ITP | 4 — IFC | IFC | All design |
| ST-014 | AFC | 4 — IFC | IFC | All design |
| ST-015 | Record Drawings | 4 — IFC | IFC | Construction |

## MEP (46 items — grouped by tier)

| Tier | Count | 50% Date | Example Items |
|------|-------|----------|--------------|
| 1 — Immediate | 7 | **29 Jun** | Power design criteria, cooling load estimate, HVAC criteria, FF criteria, plumbing criteria, overall design criteria doc, BIM model |
| 2 — Needs Arch GA + Structural survey | 24 | **29 Jul** | Power layout/small power per floor, UPS, distribution panels, earthing, lighting layout, BMS layout, all low current, ductwork layout, chilled water, ventilation, sprinkler layout, hydrant layout, all plumbing layouts |
| 3 — Needs all disciplines | 9 | **28 Aug** | Lux calculation, BMS riser, cable routing, CCTV, duct/piping/equipment details, pump room details, coordination drawings |
| 4 — IFC only | 6 | **IFC** | Submittals, ITP, AFC, Record Drawings, O&M, commissioning |

## FLS (36 items — already has staggered categories)

| Category | 50% Date | Dependency |
|----------|----------|------------|
| A — Strategy | 29 Jun | Immediate (code-based, no Arch dependency) |
| B — Active FP | 06 Jul | Needs Arch GA + structural slab loads |
| C — Passive FP | 13 Jul | Needs Arch compartmentation + sections |
| D — Coordination (all 6 trades) | 20 Jul | Needs AV, Lighting, MEP, Showcase, Setworks layouts |
| E — Commissioning | 27 Jul→IFC | All design approved |
| F — QA | IFC | — |
| G — Handover | IFC | — |

## Lighting (35 items)

| Sub-Package | 50% Date | Blocked By |
|-------------|----------|------------|
| Design Philosophy (criteria, zones, daylight) | **10 Jul** | Immediate (ZNA appointed) |
| Preliminary Design (layouts) | 10 Jul | Arch 50% GA |
| Detailed Design (sections, calcs, fixture schedule) | 09 Aug | Preliminary approved |
| Coordination (AV, Showcase, MEP, Setworks) | 09 Aug | Other discipline layouts |
| Conservation report | **BLOCKED** | Client object list |
| BOQ & VE | 09 Aug | Detailed design approved |
| Mock-Up & Sample | 08 Sep | Fixture selection |
| IFC / Handover | 28 Aug | All above |

## AV

| Sub-Package | Current 50% | Should Be | Blocked By |
|-------------|-------------|-----------|------------|
| Design philosophy, systems schedule | 29 Jun | **29 Jun** (immediate) | — |
| Display, Audio, Projection, Control system design | 29 Jun | **29 Jul** | Arch GA + equipment selection |
| Coordination, cable schedule, power reqs | 29 Jun | **28 Aug** | MEP preliminary + all disciplines |
| Rack elevations, mounting details | 29 Jun | **IFC** | Design approved |

## Showcase (70 items — GBH)

| Step | 50% Date | Status |
|------|----------|--------|
| Design spec per type | 29 Jun (stagger) | Immediate per type |
| Shop drawings | 29 Jun (stagger) | **ALREADY SUBMITTED** (Sub-01 to Sub-11 from Apr-Jun) |
| Prototype | +30d | Shop dwg approved |
| Production | +60d | Prototype approved |
| Delivery/Install | IFC | Production complete |
| QA/O&M/Spares | IFC | All above |

## Interactives (54 items)

| Step | 50% Date | Dependency |
|------|----------|------------|
| Concept/Philosophy | **15 Jul** | Immediate |
| Material Approval | 15 Jul | Concept approved |
| Prototype | 14 Aug | Material + design approved |
| Production | 13 Sep | Prototype approved |
| Delivery/Install | IFC | Production complete |

## FFE — Loose Furniture (85 items)

| Step | Earliest 50% | Blocked By |
|------|-------------|------------|
| Catalog/Brochure | **Immediate** | — |
| TDS/Cut Sheet | +30d | Vendor responses |
| Sample | +60d | Shortlisted vendors |
| Compliance/Warranty | IFC | Purchase order |

## No Dates Registers

| Register | Reason |
|----------|--------|
| Graphics | Client content research pending — RFI sent Jun 2026 |
| Model Maker | Client object list/data pending — RFI sent Jun 2026 |

## Cross-Register Dependency Summary

```
[Arch 50%] ────→ [MEP/FLS/AV/Lighting 50%] ← Needs base geometry
     │
     ├──→ [Arch 90%] ────→ [Landscaping 50%] ← Terrace/roof finalized
     │                     [Interactives 50%] ← Needs Arch geometry
     │
     ├──→ [Surveys] ────→ [Structural design] ← Needs slab loads
     │
     └──→ [Client data] ────→ [Graphics] ← Content research
                              [Model Maker] ← Object list
```

**Note:** Tier 2 items should shift +N days if the upstream Tier 1 items are delayed. Track this visually by checking if the Remarks column dates are approaching or past their planned 50% date.
