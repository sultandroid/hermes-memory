# CG Status Discovery Pattern

## Problem
User says "fix plans" or "review submissions" — but the work may already be done. Delegating to a labor without checking current state wastes tokens and may overwrite resolved items.

## Pattern (proven 2026-06-05)

Before any labor routing, check these status files:

### For Aseer Museum plans:
```bash
# Each plan folder has a CG_STATUS.md in 02_CG_Responses/
find "/OneDrive-SAMAYAINVESTMENT/Samaya/Technical Office/Bim Unit/Aseer-Museum/Docs/02_Plans_and_Procedures" -name "CG_STATUS.md" -maxdepth 4
```

Key statuses to extract:
- **Code C** = Revise & Resubmit (has open CG comments)
- **Code B** = Approved with Comments (minor, can proceed)
- **Code A** = Approved (done)
- **"Submitted — Awaiting Response"** = in CG's court, no action needed
- **"No CG Response Found"** = not yet reviewed

### For other projects:
Check the same pattern: `<project>/Docs/*/02_CG_Responses/CG_STATUS.md`

## Real example (2026-06-05)
User asked to "fix" the Communication Plan. The CG_STATUS.md showed it was ALREADY resolved (CRP Rev C02 resubmitted 03-Jun). The Stakeholder Plan was awaiting CG response. Both were in the CG's court — no action needed. Without the check, we would have wasted a Claude Code session regenerating already-submitted work.

## Rule
Always check CG_STATUS.md BEFORE routing plan-revision or submission tasks to labors. This is Phase 0 in the deploy-labors pipeline.
