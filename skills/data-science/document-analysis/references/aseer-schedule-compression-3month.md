# Aseer Museum — 3-Month Design Schedule Compression Worked Example

**Source**: Original Moharram Bakhoum schedule (216-day design phase)
**Target**: 90 calendar days per SOW/ER
**Project**: MOC-MUS-ASE, 3rd Regional Museum (Asir)

## What changed

| Aspect | Original | Compressed (3mo) |
|--------|----------|------------------|
| Total design duration | 216 days | 90 days |
| Phase count | 4 phases | 8 phases |
| Activities | ~120 design activities | ~260 design+material+prequal activities |
| Material submittals | Embedded in 216d, after design | Standalone phase between 50% and 90% |
| Prequalification | After assessment, ad-hoc | Dedicated phase before 50% design |
| Discipline sequencing | Sequential (implicit) | All parallel |
| Approval duration | 5d per item | 3d per item |

## Restructured phase sequence

```
Original (216 days):
Prelim(30d) -> Assessment(51d) -> 50%(70d) -> 90%(88d) -> IFC(27d) -> Fab(11d)

Compressed (90 days):
Prelim+Assess+Prequal(14d) -> 50%Design(19d) -> MaterialSub(27d) -> 90%+BIM(26d) -> IFC+Fab(28d)
                                                              ^ material approvals feed 90%
                                          ^ prequalified vendors feed design
```

## Dependency rules enforced

| Rule | Why |
|------|-----|
| Prequalification -> 50% Design | Design teams need approved vendor list |
| 50% Approval -> Material Submittals | Can't submit materials without concept approval |
| Prequalification -> Material Submittals | Only prequalified vendors submit |
| Material Approvals -> 90% Design | 90% specs use approved materials |
| 90% Approval -> BIM Federation | BIM uses final discipline models |
| BIM -> Clash Detection | Sequential |
| 90% Clearance -> IFC 100% | Stage gate |
| IFC Approval -> Fabrication Drawings | Can't fabricate without approved IFC |

## Realistic durations per package

| Package | Days | Reasonable? |
|---------|------|-------------|
| Architectural 50% | 12d | Plans + elevations + material selection for museum |
| Structural 50% | 10d | Existing structure assessment, minimal new build |
| MEP 50% | 8-10d | Renovation — existing systems mapped, modifications sized |
| Specialized 50% | 7-10d | Unique per discipline (AV, graphics, lighting, showcase) |
| Architectural 90% | 12d | Detailed specs, joinery schedules, material call-outs |
| BIM Federation | 10d | All disciplines coordinated in single model |
| IFC Package | 12d | Final coordinated set |

## Key enabling assumptions

1. **All disciplines fully staffed Day 1** — No ramp-up. No waiting for key hires.
2. **Point cloud data available Week 1** — Cloud survey completed before NTP or within 5 days.
3. **Copyright/exhibition text/AV software provided at project start** — Not mid-design. This is a client dependency.
4. **3-day consultant review turnaround committed in writing** — Without this, the schedule slips immediately.
5. **5 concurrent review streams** — One reviewer per discipline (ARC, STR, MECH, ELEC, AV). Single reviewer = bottleneck.
6. **Prequalification completed before 50% design starts** — Vendor packages sent Day 1, results by Day 12.
7. **BIM is continuous, not gated** — Model federation happens weekly, not at stage boundaries.
8. **No mid-design scope changes** — Any change request goes through formal change order process (stops the clock).

## Milestone timeline

| Day | Milestone |
|-----|-----------|
| 0 | NTP |
| 12 | Prequalification complete |
| 15 | Permits + assessments complete |
| 33 | 50% design complete |
| 49 | Material approvals complete |
| 61 | 90% design + BIM complete |
| 77 | IFC submitted |
| 90 | Design phase complete |

## Excel generation notes

- 258 activities total
- 4 sheets: Full Schedule, Timeline Summary, Compression Analysis, Dependency Map
- WBS format: 2.3.5-style (Phase.Discipline.Activity)
- Predecessors reference Activity IDs (A1480, PR2610, etc.)
- Color coding: navy headers (#1F3864), yellow phase rows (#FFD966), distinct per-phase fills
- Freeze panes at row 2 on Schedule sheet
- Week column: f"Week {(start - project_start).days // 7 + 1}"

## Lessons learned (pitfalls encountered)

1. **Material approvals were initially placed after design** — User corrected: "materials approvals should be in before we complete the 90%". Fixed by inserting MATERIAL SUBMITTALS phase between 50% and 90%.

2. **Prequalification was absent** — User asked "what about the prequalification". Fixed by adding PREQUALIFICATION phase after assessment, with 11 prequal activities and its own approval milestone.

3. **Durations were too short** — User said "duration for design packages not logic very tit". Initial 5-day design packages were unrealistic. Bumped to 8-12 days per package based on real museum renovation scope.

4. **Parallel not sequential is counterintuitive** — The compressed schedule works only because all disciplines run simultaneously. Most schedulers default to sequential. Must be explicit in assumptions.
