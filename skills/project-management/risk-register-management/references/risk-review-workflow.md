# Risk Review Workflow — PM Session Pattern

## When to Use

- User (PM) says "show me risk after risk to discuss and update"
- Weekly/bi-weekly risk review meeting
- Going through the register one-by-one with the PM to update status, owner, response, or close risks

## Workflow

### 1. Present One Risk at a Time

Show the risk in a compact format:

```
**Risk N — PRR-XXX-XX** (Severity)
Risk event: one-line summary
- P=X, S=X, Score=X
- Owner: Name
- Target: date
- Status: Open/Mitigated/Closed
- Action needed: [clear question about what update the PM needs to provide]
```

### 2. State the Action Needed Upfront

Bad: "Any update?"
Good: "Has the Namaa PQ progressed? Any MoC response on the licence?"

The user explicitly asked: *"always tell me the action or the response so i know what is the update you need"*

### 3. Apply Updates Immediately

When the PM gives an update:
- **Owner change** → update both `risk_register.md` and `risks.json`
- **Status change** (Open→Mitigated→Closed) → update both files
- **Response action change** → update the response field
- **Score change** → update P, S, score, and rating
- **Target close change** → update date

### 4. Close vs Mitigate

- **Closed** = the specific threat no longer exists (root cause eliminated). Example: CG approved drywall → blockwork risk is Closed.
- **Mitigated** = the risk still exists but controls have reduced it to acceptable level.
- When closing, the consequence field should say "Risk no longer applicable — resolved via [specific resolution]"

### 5. Owner Names

Use real person names (e.g. "Hani Alghamdi"), not role titles (e.g. "Commercial Manager"). The user corrected this explicitly.

### 6. Response Actions Should Be Specific

Bad: "Freeze AV content scope and define 'by others' boundary"
Good: "Raise RFI to CG/PMC to define 'by others' boundary for AV content scope"

The user corrected PRR-AV-01's response from a generic statement to a specific action ("raise RFI").

### 7. End-of-Session Summary

After going through all risks, provide:
- Summary of changes made (N risks updated, M closed, O owners changed)
- Overdue targets that need attention
- Recommendations for the next review
