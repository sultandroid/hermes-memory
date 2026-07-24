# RMP Risk Statement Format Audit

Aseer RMP Section 5.3 mandates: "Each risk follows: As a result of [cause], [event] may occur, leading to [consequence / impact on project objectives]."

The `06_Risk_System/risks.json` register stores each risk with three separate fields — `cause`, `event`, `consequence` — and the webapp renders them as a "Cause → Event → Consequence" flow. Schema is fine. Content is what drifts. This reference is the audit workflow that catches the drift.

## When to run

- User asks: "do our risks follow the RMP format?"
- User asks: "audit the risk register against RMP Section 5.3"
- Before any CG submission of the register (CR sheet, formal report)
- After a batch risk ingest from `suggestions.json` (these are template-generated and most likely to fail)

## Three-field semantic test

Apply per risk:

1. **cause** = precondition / driver / existing fact. Must NOT contain "may / might / could / risk that / potential" — those are event words. A cause that reads as the risk itself is a fail.
2. **event** = the uncertain threat. Declarative phrasing is OK ("CG rejects IFC"). It must NOT be a restatement of the title and must NOT be a copy of the cause. If event ≈ title, it carries no information — fail.
3. **consequence** = impact on project objectives. Must reference at least one of: time, delay, handover, programme, schedule, cost, budget, overrun, penalty, claim, dispute, scope, quality, safety, regulatory, compliance, occupancy, certificate, customs, operations, rework, replacement, reputational, demurrage, opening, brand, legal. "Lost productivity" alone is too vague — fail.

The three fields must also be semantically distinct. Same fact in two fields = fail.

## Audit workflow (5 steps)

1. **Confirm the canonical file.** Aseer: `06_Risk_System/risks.json` is the master. `dashboards/risks.json` is a mirror. Edit master, then `risk_sync.py` to push.
2. **Independent heuristic pass** (fast, mechanical). Write a short Python script that scores each risk on three boolean checks: cause-no-uncertainty, event-distinct-from-title, consequence-has-impact-word. Cheap filter, catches the easy failures.
3. **Semantic review pass** (slow, judgement). Delegate to a subagent with the 5 criteria above. Subagent must return: compliant count, per-category breakdown, every non-compliant risk with which field failed and why, top 3–5 patterns, fix recommendation.
4. **Reconcile the two numbers.** Heuristic and auditor will disagree. Quote both, then give the user the honest middle-ground count. Never present a single false-precision number.
5. **Patch the source.** Edit `risks.json` directly. Re-run `risk_sync.py`. Spot-check `dashboards/risks.json` and the webapp render.

## Pitfalls

- **Schema is not content.** A risk can have all three fields populated and still fail the RMP rule because two fields say the same thing. The webapp rendering them in a flow doesn't make them compliant.
- **Template-generated risks fail most.** The `suggestions.json` scanner output produces risks where cause and event are nearly identical ("Project deadline approaching with low completion" / "Detected by scanning 00_Status/project_status.md"). These need manual rewrite, not auto-accept.
- **The auditor will be stricter than the heuristic.** Expect ~50% gap. Quote both numbers and explain the range.
- **Event re-stating the title is a silent fail.** It looks compliant because the field is populated, but the user learns nothing. Flag every instance.
- **Don't re-render the Excel as the source.** The Excel CR sheet is the CG-facing artifact, but the editable source is the JSON. Always edit the JSON.

## Verification

After the fix:
- Re-run the heuristic and the auditor. Compliant count should rise.
- Open the webapp (`dashboards/risk_dashboard.html`), pick 3 random risks, verify the Cause → Event → Consequence flow reads coherently.
- Spot-check the treatment markdown files — they should start with "As a result of …" (this is the RMP rule applied to prose).
