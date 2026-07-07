# CG Deliverables Schedule Response Protocol

When CG (Mohammad Elbaz / Hossam Mabrouk) requests a Deliverables Submission Schedule via email, use this structured approach to build the response schedule.

## Prerequisites: Check These First

1. **Email recipients** — Query `Message_ToRecipientAddressList` + `Message_CCRecipientAddressList` to confirm routing before making claims
2. **Approved documents** — Cross-reference against:
   - Communication Plan (PL-0018 Rev.02) — who submits what
   - Design Management Plan (PL-0029 Rev.02) — D0 date + day milestones
   - Master Programme (0PS-SH-006) — phase durations (note approval status)
3. **3-month design window** — Comes from CG's comment on the Master Programme Rev.03: *"the first three months are allocated to site assessment, surveying, and technical design activities"*. D0 = DMP approval date (May 21). Window closes ~Aug 21.

## Deliverable Ownership Matrix

| Deliverable | Produced By | Submitted By | Depends On |
|---|---|---|---|
| DD Drawings | NRS (designer) | Samaya Tech Office | CG comments on DD patch → NRS to confirm own schedule |
| Material Submittals & Samples | Suppliers | Samaya Project Team | DD approval (finishes schedule) |
| IFC Drawings | Samaya Tech Office | Samaya Tech Office | DD approval |
| Coordination Drawings | **Not a separate phase** — coordination is built into IFC preparation | — | — |

## Schedule Construction Rules

1. **Don't put dates for other parties' work.** DD dates are TBD — NRS confirms their own production timeline. Do not guess.
2. **No CG review buffer column in initial schedule.** CG request includes reviewer buffer requirement. When building a compliance schedule, include a 14d buffer column to demonstrate feasibility but mark it 'to be confirmed by planner'.
3. **No Coordination Drawings row.** Coordination is part of IFC preparation, not a separate submittal. If CG lists it separately, it's likely a wording error — flag internally but don't challenge in the response.
4. **Basement-first priority.** CG explicitly requested basement floor as first milestone. All other packages stagger after.
5. **DD by SOW §2.4 packages, not by floors.** DD drawings are organized by drawing type/discipline packages (GA, Sections, Elevations, Finishes, Ceilings, Showcases, etc.), not by floors. NRS already submitted Patch 1 (Basement) as a group. List remaining packages accordingly.
6. **All submissions stamped and signed by Contractor's Project Director** per Communication Plan Rule 11.
7. **IFC schedule to follow** after DD approval — note as 'TBD, to be refined after DD closeout.'
8. **IFC produced by Samaya Tech Office**, not NRS. Material Submittals by Samaya Project Team.
9. **3-month window covers submission + approval.** CG's request says 'fully delivered and approved within this duration.' Ensure approval dates (submit + 14d buffer) also fit within May 21 → Aug 21.
10. **CG compliance validation.** After building the schedule, verify against CG's 4 requirements: (1) basement priority, (2) balanced/staggered, (3) review buffer included, (4) within 3-month window for submission + approval.

## Response Channel

Per the Communication Matrix:
- Item 19 (Time Baseline) / Item 20 (Others): From **Contractor** → To **CG**
- Rule 5: Engineering submittals addressed to Project Directors, key personnel in CC
- Rule 11: All submittals stamped and signed by Contractor's PM/PD
- The Project Director (PD) sends the response, not the Technical Office Manager directly

Let the PD respond with the stamped schedule — this teaches the correct channel by action, not words.

## Phases to Include

| Phase | Items | Status |
|---|---|---|
| 1 — DD Drawings | Basement → Roof (staggered per floor) | NRS to advise dates |
| 2 — Material Submittals | Basement → Remaining floors → Samples | After DD approval |
| 3 — IFC Drawings | Basement → Remaining floors | After DD approval |

## Common CG Email Management Mistakes (for analysis, not the response)

When reviewing a CG email for inconsistencies, watch for:

- **Party confusion**: Requesting items from a party that doesn't produce them (e.g., asking Samaya for DD drawings produced by NRS) — acceptable if Samaya is the umbrella contractor, but note the dependency
- **Mixed baskets**: Grouping DD, materials, IFC, and coordination into one flat request — each has different workflows
- **Undocumented deadlines**: "Previously agreed" timelines not found in approved docs — check Master Programme comments first
- **Wrong channel**: PD in CC instead of To for schedule submissions per Communication Matrix Item 19
- **Unrealistic turnaround**: 2 days for a comprehensive multi-party schedule

However, be careful: **CG oscillation is normal** — sometimes they treat NRS as separate, sometimes under Samaya's umbrella. Don't flag "party confusion" without checking recent pattern.

## Excel Delivery Format

When building the Excel schedule:
- Landscape orientation, clean headers (Phase / Ref / Deliverable / Producer / Submitter / Target Submission / Notes)
- No review buffer column (planner adds it)
- No dates for other parties' work (NRS = TBD)
- Notes section listing: D0 date, 3-month window, Communication Plan reference, stamp requirement
