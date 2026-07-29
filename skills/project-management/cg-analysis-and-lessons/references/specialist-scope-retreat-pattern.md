# Specialist Scope Retreat — Response Playbook

When a design or consultancy specialist signs for multi-stage scope (DD → 90% → IFC) and later reneges to early-stage only.

## Worked Example: AD Engineering (Aseer Museum, Jul 2026)

AD Engineering signed agreement 15-Jul-2026 for MEP design at LOD 300 (DD), LOD 350 (Coordination), LOD 400 (IFC) per ZD-0068 Rev.01. Later claimed they would only produce DD-stage deliverables and would not support 90% or 100%/IFC drawings. Signed SOW explicitly states all three stages.

## Immediate Response (first 24h)

1. **VERIFY the signed scope document** — do not rely on memory or what was said in meetings. Read the signed SOW/agreement. If the scope is clearly stated as multi-stage, the retreat is a contractual breach, not a misunderstanding.

2. **DOCUMENT the delta** — create a table of what was agreed vs what is now offered:

   | Deliverable | Agreed (SOW) | Now Offered | Gap |
   |-------------|-------------|-------------|-----|
   | DD (LOD 300) | ✅ | ✅ | — |
   | Coordination (LOD 350) | ✅ | ❌ | Full gap |
   | IFC (LOD 400) | ✅ | ❌ | Full gap |

3. **ESCALATE linked risk scores** — scope retreat nearly always escalates risk. Review every PRR risk that references this specialist and increase P or S if the downstream cascade worsens. For AD Engineering, PRR-MEP-01 (Critical 12) and PRR-PRC-10 (Critical 16) were directly affected.

4. **MAP the downstream cascade** — list every dependent discipline/package that needs the withdrawn deliverables:

   | Dependent | Needs | Without It |
   |-----------|-------|-----------|
   | Ceiling coordination | Coordinated MEP (LOD 350) | Triple clash unresolved at IFC |
   | AV design | MEP power/cooling/containment | AV design frozen at assumptions |
   | FLS IFC packages | MEP fire pump/smoke basis | FLS packages blocked |
   | MEP installation contractor | IFC MEP drawings | No construction documents |
   | Lighting (ZNA) | MEP ceiling interface | Lighting positions uncoordinated |

5. **UPDATE submittal register status** — set the specialist's status to "Disputed", not "Under Review" or "Flagged". This is a contractual dispute, not a pending submission.

## Mid-Term Response (1-2 weeks)

### Option A — Contractual Enforcement
- Issue formal letter referencing the signed SOW clause that covers full scope
- Demand compliance within a defined period (e.g. 14 days)
- Reserve rights for damages/cost of replacement procurement
- **Use when:** specialist is capable but stalling; project can't absorb delay of re-procurement

### Option B — Scope Re-Procurement
- Identify alternative specialists who can deliver the missing stages
- Issue SCOPE_REQUEST for the gap scope (90% + IFC only, using DD as input)
- **Use when:** specialist is unable or unwilling; contract has termination provisions

### Option C — In-House Completion
- Assign remaining design stages to another existing consultant (e.g. MEP installer who can design-build)
- **Use when:** speed is critical; gap scope is well-defined; no time for full re-procurement

## Registers to Update

| Register | What to Change |
|----------|---------------|
| Risk register (PRR) | Escalate scores for any risk linked to this specialist; add new risk if gap creates new exposure |
| Design discipline risk register (DDR) | Update all DDR entries that assume full-stage delivery from this specialist |
| Lessons learned register | Add a lesson: specialist scope retreat, root cause, actions taken |
| Submittal register | Mark specialist status as "Disputed"; track all missed submission dates |
| Submission tracker | Flag specialist as 🔴 with note "Scope dispute — IFC deliverables withdrawn" |
| Letters register | Log any formal correspondence about the dispute |

## Lessons Learned — What to Capture

Every specialist scope retreat should generate a lesson with:

- **Root cause:** Was the scope ambiguous? Was the specialist overstating capacity? Was the contract unclear on stage gates?
- **Preventive action:** What will prevent this next time — clearer stage-gate definitions in SOW? Phased payment tied to stage completion? Performance bond?
- **Trigger condition:** The first sign is usually when the specialist resists submitting to a submission plan that covers later stages.
