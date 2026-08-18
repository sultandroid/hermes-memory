# Risk Entry Approval Gate (User Rule 2026-08-18)

**Never create, update, close, merge, reschedule, or otherwise modify ANY risk entry
(risks.json / risk_register / PRR / DDR / HSE / AVR) without first reviewing the change
and getting explicit user approval.**

## What is gated
Any change to a risk *entry or its fields* — target_close, status, rating/score, actions,
reschedules, merges. These always require per-item user sign-off.

## What is NOT gated
Routine register-file maintenance: `submittal_register.md`,
`assessment_evaluation_register.md`, NCR register, etc. Those are normal record-keeping and
can proceed.

## Workflow that satisfies the rule
1. Collect the change set (risk ID, current state, proposed state, reason).
2. Present each proposed change ONE AT A TIME and await yes/no.
3. Apply only the approved ones.
4. If you already pushed without approval: disclose the commit, re-present the diff
   item-by-item, and revert any rejected items with a fresh dated commit.

## Why it exists
On 2026-08-18 the agent pushed 4 risk modifications (PRR-MEP-02 target/action, PRR-MEP-03
TABCOM action, PRR-NCR-001 + PRR-STK-02 history) to origin/main and deployed them before
showing the user. User correction: "لا تسجل مخاطر إلا بعد المراجعة والعرض عليّ أولاً"
(do not register risks except after review and showing me first). The assessment register
update itself was fine; the risk-entry edits were not.

## Cross-reference
Also in user memory: "Risk review: evidence from Outlook first. NEVER register/modify any
risk without prior user approval."
