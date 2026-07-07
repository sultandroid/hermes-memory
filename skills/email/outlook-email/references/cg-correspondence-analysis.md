# CG Correspondence Analysis & Communication Plan Routing

Used after extracting CG emails — validates routing against the approved Project Communication Plan before responding.

## Key Communication Plan Sections (Aseer Museum — PL-0018 Rev.02 / Rev C02)

**§12.5 Distribution & Record Matrix (Page 22/24)**
| Document | Originator | Reviewer | Approver | Distribution |
|---|---|---|---|---|
| Management Plans | Samaya PMO | Samaya PD | CG | CG → PMC → MoC |
| Design Submittals | NRS/Samaya | Samaya Tech Office | CG | Samaya → CG → PMC → MoC |
| Material Submittals | Samaya/Subcon | Samaya QA/QC | CG | Samaya → CG → PMC |
| Shop Drawings | Samaya | Samaya Tech Office | CG | Samaya → CG |

**§13 Phase-Gate Communication Matrix (Page 23/24)**
- G-1 (Design Development): Samaya issues → CG Code A/B/C/D
- G-2 (Submit/Procure): Samaya issues Stage 2 → CG review → IFC

**CG Comment 02 (on Rev.02 submittal):**
> "Per Table 7.2, the Contractor shall comply with the attached Communication Matrix"

## DD Package Structure (Per SOW §2.4)

DD drawings are submitted as **packages by drawing type**, not by building floors. The BIM folder structure follows:

| Package | Content |
|---|---|
| General Arrangement | Floor plans, GA drawings |
| Sections | Building sections, longitudinal sections |
| Internal Elevations | Room-by-room elevations |
| Floor Finishes | Finish plans, material layouts |
| Ceiling Details | RCPs, ceiling coordination |
| Showcases | Showcase drawings (Glasbau Hahn) |
| Graphics Housing | Graphic display housings |
| Setworks / FWalls | Setwork partitions, freestanding walls |
| Furniture, Retails | FF&E layout |
| Doors, Lifts | Door types, lift lining |

NRS submitted Patch 1 (Basement) as a group of all drawing types. Remaining packages follow per their schedule. When building a deliverables schedule, reference package names not floor names.

## Routing Validation Pattern

When CG sends a request, check:

1. **Who is it addressed to?**
   - Per §12.5, schedule/program submissions originate from Samaya PMO/PD
   - If sent directly to Tech Office Manager, the route is wrong

2. **What type of deliverable?**
   | CG Request | Correct Originator (per §12.5) |
   |---|---|
   | Schedule/Program dates | Samaya PMO → Samaya PD |
   | DD/IFC design drawings | NRS/Samaya → Tech Office review → CG |
   | Material submittals | Samaya/Subcon → Samaya QA/QC → CG |
   | Management Plans | Samaya PMO → Samaya PD → CG |

3. **Is the party in To or CC?**
   - Key persons (PD, CG RE, DC) must be in To per Communication Rules
   - PD in CC only = routing error

## Response Approach

**Do NOT lecture CG about their mistake.** Instead:
- Route through the correct channel (PD responds with stamped submission)
- Let the PD's proper response teach the process by example
- If CG mixed different deliverable types in one request, respond with what you can schedule now (DD), explain others depend on that

## CG Behavior Patterns (Mohammad Elbaz)
- Processes in batch waves — silent for days then dumps 10 decisions
- Aggressive/retaliatory demands within 2 days of pushback
- Mixes unlike deliverables (DD, Material, IFC, Coordination) into one flat request
- Bypasses his own approved Communication Matrix
- Uses "previously agreed-upon timeframe" without document references
- His own Rev.01 Comment 4 says "Samaya remains fully contractually responsible" — uses this against you but ignores routing rules

## When CG Is Actually Right

Despite the pattern, CG's requests often have legitimate basis. Before dismissing:

- **3-month design window**: CG's Master Programme comment says *"first three months allocated to site assessment, surveying, and technical design activities"* — this IS in their own approved (though C-status) document. The timeframe is real even if the "agreed-upon" language feels imposed.
- **Review buffer**: CG asking for review time in the schedule is standard practice, not overreach. Include a 14-day buffer column.
- **Basement-first priority**: Per CG's direction to expedite workflow, this aligns with normal construction sequencing.
- **Samaya as umbrella**: CG treating Samaya as single point of contact for all deliverables (including NRS-produced) IS consistent with Comment 4 from Rev.01 — Samaya is contractually responsible.

When building a response, comply with what's reasonable (basement priority, staggered, review buffer, 3-month window) and note genuine dependencies as notes, not objections.

## Quick Sanity Checks Before Responding

1. Verify actual recipients from `Message_ToRecipientAddressList` / `Message_CCRecipientAddressList` first — do not trust preview text
2. Check if the Master Programme has comments relevant to timing — even C-status documents carry CG's stated position
3. Confirm DD package structure from actual project folders (SOW §2.4), not by floors
4. If CG lists Coordination Drawings separately from IFC, it's likely a wording error — internally flag, don't challenge in response

## Common CG Email Management Mistakes
1. Party confusion — requesting from Samaya items that depend on NRS
2. Mixed baskets — grouping deliverables with different workflows into one flat deadline
3. Undocumented deadlines — "previously agreed" claims with no MOM/doc reference
4. Unrealistic turnaround — comprehensive schedule requested in 2 days
5. Bypassing Communication Matrix — emailing the wrong role directly
6. Coordination = IFC — these are the same, not separate deliverable tracks
