# NRS Email Triage Workflow

When NRS (Jim Richards / Nissen Richards Studio) replies to a coordination email, triage into three categories:

## 1. Action Items (adopted / will do)
NRS confirms adoption of a requirement. Record and move on.
- **Example**: Drawing numbering system — Jim confirms adoption despite file-stacking concerns
- **Action**: Note in project memory, no further escalation unless issues arise

## 2. Clarifications / No Discrepancy
NRS explains there's no actual issue. Accept and close.
- **Example**: Room sheet colours — 3 primary colours (red, grey, white), white = no colour assigned, all references being updated
- **Action**: No register entry needed. Close.

## 3. Risks / Escalations ⚠️
NRS flags a technical coordination gap, design flaw, or process frustration that could cause rework, delay, or quality issues.
- **Example**: Light box / acoustic baffle coordination gap — NRS Stage 2 drawings show light boxes at baffle underside, Museum Studio Stage 3 visuals extend them into baffle depth, ZNA drawings don't cover this detail
- **Action**: Record in **Design Risk Register** (06_Design_Risk_Register), escalate for design coordination meeting

## Decision Tree
```
Does Jim say "we will" / "agreed to"?
  → Action item (track in memory, no register)
Does Jim say "no discrepancy" / "already in progress"?
  → Clarification (close, no action)
Does Jim say "risk" / "frustrating" / "cannot resolve" / "if not corrected"?
  → Risk ⚠️ (Design Risk Register + escalation)
```

## Risk Register Format for Design Coordination Risks
When adding to the Design Risk Register (`06_Design_Risk_Register/Aseer_Museum_Design_Risk_Register.xlsx`):
- **Risk ID**: Next sequential CO-X-XXX (Coordination category)
- **Category**: Coordination
- **Risk Description**: State what, who (NRS/ZNA/Museum Studio), and which stage/drawing
- **Consequences**: Specific impact (shadows, void lit, rework before IFC)
- **P/I**: Typically 3/3 = 9 (Medium) for unresolved coordination gaps
- **Mitigation**: Design coordination meeting; agree detail before IFC
- **Evidence Source**: "Jim Richards email [date]"
