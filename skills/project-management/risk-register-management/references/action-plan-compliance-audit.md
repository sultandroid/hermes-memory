# Action Plan Compliance Audit — RMP Response Time Periods & Project Stage Logic

## When to Use

- User says "audit all risk action plans" or "check target close dates against RMP"
- Before weekly risk review — verify every risk's Response Action and Target Close date comply with RMP §8.2
- After a register revision (new risks added, scores changed) — ensure new entries have compliant action plans
- When project stage shifts significantly (e.g. entering final 10 weeks to handover) — revalidate all target dates

## The Core Principle

Every risk's action plan must satisfy **two constraints simultaneously**:

1. **RMP §8.2 Response Time Standards** — the plan must be proportionate to severity
2. **Project Stage Reality** — the target close date must be achievable given remaining programme float and current progress

## RMP §8.2 Response Time Standards (from RMP C03)

| Severity | Score | Required Response | Plan Response Latency | Review Frequency |
|----------|-------|-------------------|----------------------|------------------|
| Critical | 12-16 | Detailed plan, specific actions, owner, budget, timeline | 48h | Weekly |
| High | 8-11 | Formal plan with actions, owner, timeline | 48h | Bi-weekly |
| Medium | 4-7 | Response actions identified, owner assigned | — | Monthly |
| Low | 1-3 | Monitor, response actions optional | — | Quarterly |

## Audit Checklist — Four Non-Compliance Categories

| # | Category | What to Check | Example |
|---|----------|---------------|---------|
| 1 | **Missing Target Close** | Risk has no target_close date — no accountability timeline | 15 of 54 risks in C11 had no target close |
| 2 | **Unrealistic Target Close** | Date is too soon given project stage (remaining float, dependencies, complexity) | PRR-FLS-01 target 22-Jul when IFC-0004 Code C needs Nama endorsement + Rev.02 — 2 days impossible |
| 3 | **Stage-Mismatched Response** | Response action describes a multi-week process but project has <10 weeks left; or action is appropriate for early-stage but not late-stage | PRR-CON-03: "Technical workshop with CG... 3D coordination study... submit engineered drywall as VE" — needs a hard deadline, not open-ended process |
| 4 | **Vague Response for Severity** | Critical/High risk has generic response without specific actions, dates, or owners | PRR-APP-03 (High 9): "Authority-approval matrix... pre-clear SABER/SASO... appoint local approvals consultant" — no specific actions per authority body |

## Audit Workflow

### Step 1: Establish Project Stage Baseline

Before auditing, determine the project's current stage parameters:

| Parameter | Source | Example (Aseer Museum, 19-Jul-2026) |
|-----------|--------|--------------------------------------|
| Contract handover date | Contract | 30-Sep-2026 |
| Days elapsed | NTP date | 189 of 303 (~62%) |
| Progress % | project_status.md | ~39% complete |
| Remaining weeks | Handover - today | ~10 weeks |
| Critical path blockers | look_ahead.md | IFC-0004, Fire Pump, MEP mobilisation, interactive specialist |

### Step 2: Read All Risks from Register

Read the full risk register (MD or JSON). For each risk, extract:
- Risk ID, severity, score
- Response Action text
- Target Close date
- Status

### Step 3: Check Each Risk Against Four Categories

For each risk, ask:

1. **Missing Target Close?** — If `target_close` is empty or `—`, flag it. Every risk needs a target close date per RMP governance.

2. **Unrealistic Target Close?** — Is the date achievable given:
   - Remaining programme float (from look_ahead / master programme)
   - Dependencies that must resolve first (e.g. CG approval, specialist appointment, test results)
   - Complexity of the response action (multi-week process vs 2-day deadline)
   - Historical velocity (has this risk been open for months with no progress?)

3. **Stage-Mismatched Response?** — Does the response action:
   - Describe a multi-week process that should have started weeks ago?
   - Propose a workshop/study when a decision deadline is what's needed?
   - Assume early-stage flexibility when the project is in late-stage execution?
   - Use "if X persists, serve Notice of Dispute" language when the dispute should already be escalated?

4. **Vague for Severity?** — For Critical/High risks:
   - Are specific actions listed (not just categories like "authority-approval matrix")?
   - Does each action have an owner?
   - Does each action have a due date?
   - Is there a measurable success criterion?

### Step 4: Classify Findings

| Finding | Count (C11 example) | Action Required |
|---------|---------------------|-----------------|
| Missing Target Close | 15 of 54 | Add realistic target close date based on project stage |
| Unrealistic Target Close | 8 of 54 | Extend to achievable date; add history note explaining why |
| Stage-Mismatched Response | 4 of 54 | Reframe response to match current project stage; add hard deadlines |
| Vague Response for Severity | 3 of 54 | Tighten response with specific actions, owners, dates |

### Step 5: Report Findings

Produce a structured report with:

1. **Summary table** — total risks audited, non-compliant count, breakdown by category
2. **Per-risk detail** — risk ID, severity, current target close, issue category, suggested fix
3. **Project stage context** — remaining weeks, critical path blockers, why certain dates are unrealistic
4. **Recommended actions** — numbered, prioritised, with rationale

## Common Patterns by Project Stage

### Late-Stage Project (10-15 weeks to handover)

| Pattern | Old Response | Stage-Appropriate Fix |
|---------|-------------|----------------------|
| Open-ended process | "Technical workshop with CG... 3D coordination study... submit engineered drywall as VE" | "CG must decide by 31-Jul or Samaya proceeds with drywall under dispute reservation" |
| Novation pursuit | "Secure novation or collateral warranty; delineate design-responsibility split" | "Document design-responsibility gap, price assumed design work as variation, proceed under reservation" |
| No EV baseline | "Establish resource-loaded logic-linked baseline and EV reporting" | Same action but with hard deadline: "EV baseline established by 31-Jul — every week without = no objective progress measurement" |
| Commissioning plan | "Appoint commissioning manager and integrated plan" | "Commissioning manager appointed by 15-Aug — 6 weeks before handover" |

### Early-Stage Project (6+ months to handover)

- Target close dates can be more generous (2-4 weeks for response actions)
- Workshops, studies, and coordination meetings are appropriate responses
- Novation/collateral warranty pursuit is still viable

## Pitfalls

- **Don't set target close dates that are just "end of project"** — every risk needs a specific review/closure gate, not just "30-Sep-2026"
- **Don't accept "—" as a target close** — it means no accountability. Every risk needs a date, even if it's far out
- **Don't confuse "response action is correct" with "response action is stage-appropriate"** — a correct action can be wrong for the current stage
- **Don't set Critical risk target close dates in 2-3 days** unless the action is literally a single decision or submission. Most Critical risks involve multi-step processes
- **Don't leave vague responses for Critical/High risks** — CG will flag them as inadequate. Every Critical risk needs specific actions with owners and dates
- **Check the register's severity distribution first** — if severity bands are all showing 0 (as in C11), the formulas may be broken. Fix scoring before auditing action plans
