# HSE Strategy Classification per RMP 8.1

## Rule

Per RMP §8.1 strict interpretation: **Mitigate only if actions reduce probability** (not just impact).

| Strategy | When | Examples |
|----------|------|----------|
| **Mitigate** | Physical/engineering controls that reduce likelihood of the hazard occurring | Lift plan + banksman, LOTO, guard rails, harness, fire watch, hot work permit, confined space entry procedure + rescue plan, method statement + isolation, authorised start-up |
| **Accept (Active)** | Administrative/monitoring-only controls that reduce impact or increase detection but don't reduce probability | RAMS (risk identification only), PTW (admin process), TBT/toolbox talk (awareness), PPE (reduces impact not P), supervision, HSE monitoring |

## Current Classification (9 Mitigate, 32 Accept)

| ID | Title | Strategy | Rationale |
|----|-------|----------|-----------|
| HSE-07 | Lifting operations | Mitigate | Lift plan + banksman (reduces P) |
| HSE-09 | Confined space | Mitigate | Entry procedure + rescue plan (reduces P) |
| HSE-11 | Electrical isolation / LOTO | Mitigate | LOTO (reduces P) |
| HSE-12 | Testing & commissioning (M&E) | Mitigate | LOTO + authorised start-up (reduces P) |
| HSE-36 | Demolition / enabling works | Mitigate | Method statement + isolation (reduces P) |
| HSE-37 | MEWP / Manlift operation | Mitigate | Guard rails, harness (reduces P) |
| HSE-38 | Mobile / tower scaffold | Mitigate | Guard rails, harness (reduces P) |
| HSE-40 | Work at height | Mitigate | Fall protection / harness (reduces P) |
| HSE-41 | Hot work | Mitigate | Fire watch + hot work permit (reduces P) |
| All other HSE-01–06, 08, 10, 13–35 | Various | Accept (Active) | RAMS/PTW/TBT/PPE — admin only, no P reduction |

## Data Field Convention

Strategy is embedded in the `response_action` field as a `[Strategy: X]` prefix:

```json
"response_action": "[Strategy: Mitigate] Lift plan + banksman reduces lifting risk probability"
```

The Excel snapshot builder extracts the strategy via:
```python
re.match(r'^\[Strategy:\s*([^\]]+)\]\s*', response_action)
```

## Workflow for Updating Strategies

1. Edit `hse_risks.json` — update `response_action` values (rewrite the action text to match the new framing)
2. Bump revision in JSON header (C12 → C13)
3. Regenerate snapshots: `python3 build_snapshots.py --bump`
4. Commit & push (exclude 00_Contracts/ from staging — pre-commit hook rejects them)
5. Trigger OneDrive sync: `cronjob(action='run', job_id='ef2495d20159')`
6. Verify strategy column in the OneDrive Excel after sync
