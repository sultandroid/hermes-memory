# Landscape Submission Plan — Worked Example

Created 2026-07-12 from the Arch Submission Plan Rev02 format. Updated 2026-07-12 with scope boundary lessons.

## Source Data Mapped

| Source | What it provided |
|--------|-----------------|
| SoW §6.2 | Hard/soft landscaping scope, Stramp, terrace |
| SoW §6.22.4.x | Horticulture/landscape design deliverable |
| SoW §6.22.4.xi | Terrace sunshade + balustrade |
| SoW §5.5 | Landscaping Specialist as Key Personnel |
| Master_Submission_Plan.xlsx | Dates: 29/07 (50%), 28/08 (90%), 27/09 (100%), 28/08 (IFC) |
| Design_Schedule_Programme.xlsx | Group 3 (needs Arch 90%), 7d review buffer |
| PROJECT_MEMORY.md | Evergreen Landscaping profile, candidates overdue, BOQ needed |
| DMP Scope Summary | §6.22.4.x horticulture, §6.22.4.xi sunshade/balustrade |

## Structure Decisions

| Decision | Rationale |
|----------|-----------|
| 3 gates (DD → Material → IFC) | Matches Arch plan gate structure |
| 4 zones (Stramp, Terrace, All External, General) | Landscape has no floors — zones are physical areas |
| 15 columns matching Arch plan | Consistency across all discipline plans |
| No Linked Activity IDs | Programme codes not confirmed — leave empty |
| Landscape Lighting removed | Belongs to Studio ZNA (Lighting Designer), not Landscape specialist |

## Date Logic

- 50% Concept: 29/07/2026 (from Master Plan row 20-21)
- 90% Design: 28/08/2026 (from Master Plan)
- 100% Final: 27/09/2026 (from Master Plan)
- IFC: 28/08/2026 (from Master Plan row 32 — same as other Group 3/5 items)
- Material samples: 01/10/2026 (after 100% design approval)
- IFC packages: 15/10/2026 (allowing 2 weeks after 100% approval)

## Save Pattern

1. Generate to `/Volumes/MIcro/.pi-tmp/work/` (temp volume, no OneDrive lock issues)
2. Open from there for user review
3. When approved, copy to OneDrive registers folder

## Scope Boundary Lesson (CRITICAL)

**Landscape Lighting Layout** was initially listed as a Landscape deliverable (L-IFC-004). User corrected: it belongs to Studio ZNA (Lighting Designer). The Landscape specialist provides layout context (plant locations, paving zones) as input, but fixture selection, light levels, and control design are ZNA's scope.

**How to handle in the plan:**
- Remove the deliverable from the Landscape plan
- Add a note in Batch 3/4: "Landscape lighting layout (by Studio ZNA — Lighting Designer)"
- Add a coordination interface row: "Lighting (Studio ZNA) — Landscape lighting layout, fixture selection, light levels"
- Keep MEP row for power supply coordination

**Rule for future plans:** Before assigning any deliverable, ask: "Which specialist actually produces this?" If the answer is not the discipline you're writing the plan for, move it to the correct plan or list it as a coordination interface only.

## Linked Activity ID Rule

Column K was populated with EN108/EN136/EN1000 codes. User said: "Remove the data of the linked activity ID because we are still not sure." 

**Rule:** Leave column K empty until programme activity codes are confirmed. Do not invent or copy codes from other discipline plans.

## Verification Checklist

- [ ] All 15 columns present with correct headers
- [ ] Section header hierarchy: Gate (light blue) → Level (gray) → Data (light green)
- [ ] Merged cells on section rows (all 15 cols)
- [ ] Column widths match Arch plan
- [ ] Column K (Linked Activity ID) — all empty
- [ ] No deliverables assigned to wrong specialist (scope boundary check done)
- [ ] Coordination interfaces include the correct specialist for each item
- [ ] Remarks column flags critical blockers
- [ ] Saved to /Volumes/MIcro/.pi-tmp/work/ first
