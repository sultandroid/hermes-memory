# Action Plan Audit — RMP Compliance & Project Stage Logic

## When to Use

- User says "fix all action plans" or "update all risks to follow approved response periods"
- Before a weekly risk review — ensure all action plans are realistic for the remaining project duration
- After a major schedule change (milestone slip, EOT, acceleration) — action plans may need recalibration
- When the project enters a new stage (e.g. design → procurement → construction → commissioning) — response actions that made sense in design may be stage-mismatched

## Audit Criteria

Every risk's action plan must satisfy three checks:

| Check | Question | Source |
|-------|----------|--------|
| **Target Close exists** | Does every risk have a non-blank Target Close date? | RMP §8.2 — all severities need accountability timelines |
| **Target Close is realistic** | Is the date achievable given remaining project duration and the risk's nature? | Project stage (e.g. ~10 weeks to handover, ~39% complete at day 189/303) |
| **Response matches stage** | Does the response action reflect the current project stage, not an earlier one? | Current stage (design DD / procurement / construction / commissioning) |

## Common Non-Compliance Patterns

| Pattern | Example | Fix |
|---------|---------|-----|
| **Missing Target Close** | `Close=—` on 15 risks in C11 | Assign a date based on risk severity and project stage. Critical/High: 2-4 weeks. Medium: 4-6 weeks. Low: 6-8 weeks. |
| **Unrealistic Close** | PRR-COM-01 close=24-Jul for an EOT dispute that needs weeks of negotiation | Extend to a realistic date (e.g. 15-Aug). Add history note explaining why. |
| **Stage-mismatched response** | PRR-DES-06: "Secure novation" at 62% elapsed — novation is a pre-contract action, not a mid-project one | Reframe: "Document design-responsibility gap; price assumed work as variation; proceed under reservation" |
| **Vague response for severity** | PRR-APP-03 (High 9): "Authority-approval matrix" without per-body actions or dates | Tighten: list each authority body, assign owner per body, add milestone dates |
| **Wrong response strategy** | Employer/authority dependency risks marked "Mitigate" instead of "SOW-Protect" | Change to SOW-Protect — these are not Samaya's scope to mitigate |

## Audit Workflow

1. **Read the RMP** — extract approved response time periods (§8.2 Response Planning Matrix):
   - Critical (12-16): Detailed plan, specific actions, owner, budget, timeline — weekly review, 48h response latency
   - High (8-11): Formal plan with actions, owner, timeline — bi-weekly review, 48h latency
   - Medium (4-7): Response actions identified, owner assigned — monthly review
   - Low (1-3): Monitor, response actions optional — quarterly review

2. **Read the project status** — extract current stage, % complete, days elapsed vs total, remaining duration. Use `project_status.md`, `master_programme.md`, `look_ahead.md`.

3. **Read all risks** from the Excel or markdown register. For each risk, check:
   - Does Target Close exist? If not → assign one
   - Is Target Close realistic for the remaining project duration? If not → extend
   - Does the Response Action match the current project stage? If not → reframe
   - Is the Response Strategy correct for the risk type? (SOW-Protect for Employer/authority dependencies)
   - Is the Response Action specific enough for the severity level?

4. **Apply fixes** — update both the Excel (openpyxl) and the repo markdown (Python string replacement or patch). The markdown register has NO separate Response Strategy column — strategy is embedded in the Response Action text (e.g. "SOW-PROTECT: ...").

5. **Update Last Review** to current date for all changed risks.

6. **Commit** with a summary of what changed and why.

## Markdown vs Excel Column Mapping

The markdown register (`01_Registers/risk_register.md`) has a different column layout than the Excel:

| Content | Excel Column | Markdown Column Index |
|---------|-------------|----------------------|
| Response Strategy | L (col 12) | **Not present** — embedded in Response Action text |
| Response Action | M (col 13) | Index 11 (7th pipe-delimited field after #) |
| Target Close | Q (col 17) | Index 14 (10th pipe-delimited field after #) |
| Last Review | P (col 16) | Not in markdown table |

**Pitfall:** When fixing the markdown, do NOT try to add a separate Response Strategy column — the markdown table has 15 columns and no strategy column. Strategy is prepended to the Response Action text (e.g. "SOW-PROTECT: ..."). If you overwrite the Response Action with just the strategy name, you'll lose the action text.

## Row Mapping Pitfall

The markdown risk rows are numbered 1-54 sequentially. The Excel rows start at row 4 (header at row 3). When applying fixes, map by **Risk ID** (PRR-XXX-NN), not by row number. The markdown and Excel may have different row ordering for the same risk ID.

## Example: 22-Risk Audit (C11, 2026-07-20)

From the C11 audit:
- 15 risks missing Target Close → assigned dates (31-Jul to 31-Aug)
- 8 risks with unrealistic close dates → extended (e.g. PRR-COM-01 24-Jul→15-Aug, PRR-SCH-01 24-Jul→30-Sep)
- 4 risks with wrong strategy → changed to SOW-Protect (APP-01, APP-04, MEP-01, SIT-02)
- 6 response actions updated for stage-mismatch or vagueness
- Total: 22 of 54 risks (41%) non-compliant
