# Risk Register Data Sources — Field Map & Structure

## PRR (Project Risk Register)

| Property | Value |
|----------|-------|
| Source file | `aseer-museum-pm/06_Risk_System/risks.json` |
| Format | Single JSON object with `risks` array |
| Action plan field | `response_action` |
| Required per-risk fields | `id`, `category`, `title`, `cause`, `consequence`, `probability`, `severity`, `score`, `rating`, `response_action`, `owner`, `status` |
| Risk count | ~109 |
| ID format | `PRR-{RBS}-NN` (e.g., `PRR-COM-02`) |

## DDR/DRR (Design Discipline Risk Register)

| Property | Value |
|----------|-------|
| Source file (JSON) | `aseer-museum-pm/06_Risk_System/generated/drr_risks.json` |
| Source file (MD) | `aseer-museum-pm/01_Registers/design_discipline_risk_register.md` |
| Format (JSON) | Single JSON object with `risks` array |
| Format (MD) | Pipe table with 11 columns: ID, Discipline, Stage, Risk Event, Cause/Trigger, Impact, Priority, Existing PRR/DRR Link, **Immediate Control Action**, Owner, Evidence Source |
| Action plan field (JSON) | `response_action` |
| Action plan field (MD) | `Immediate Control Action` (column index 9, 0-indexed) |
| Risk count | ~79 (JSON) / ~122 (MD — includes NRS overlay) |
| ID format | `DDR-{DISC}-NNN` (e.g., `DDR-STR-001`), also `PR-Q-NNN`, `DB-A-NNN`, etc. |

## HSE (Health & Safety Risk Register)

| Property | Value |
|----------|-------|
| Source file | `aseer-museum-pm/06_Risk_System/generated/hse_risks.json` |
| Format | Single JSON object with `risks` array |
| Action plan field | `controls` (NOT `response_action`) |
| Scoring scale | Consequence 1-5 × Likelihood 1-5 (different from PRR's 1-4) |
| Risk count | ~41 |
| ID format | `HSE-{section}.{seq}` (e.g., `HSE-1.1`) |
| Other fields | `activity`, `hazards`, `controls`, `c_init`, `l_init`, `score_init`, `rating`, `response_strategy`, `owner`, `status` |

## AVR (AV & Multimedia Risk Register)

| Property | Value |
|----------|-------|
| Source file | `aseer-museum-pm/06_Risk_System/webapp/av/src/index.html` |
| Format | Embedded JSON in `const RISK = {...};` at line ~470 |
| Action plan field | `response_action` (string) + `response_list` (array of steps) |
| Risk count | ~12 |
| ID format | `AVR-{RBS}-NN` (e.g., `AVR-OPS-01`) |
| Required per-risk fields | `id`, `category`, `title`, `cause`, `event`, `consequence`, `probability`, `severity`, `score`, `rating`, `status`, `owner`, `target_close`, `response_action` |

## Construction Risk Register

| Property | Value |
|----------|-------|
| Source file | `aseer-museum-pm/01_Registers/construction_risk_register.md` |
| Format | Two pipe tables: generic (C-001 to C-040) and project-specific (C-041 to C-060) |
| Generic table columns | ID, Risk Description, Probability, Risk Level, Owner — **no action column** |
| Project-specific columns | ID, Risk Description, Cause, Impact, Probability, Risk Level, **Mitigation**, Owner, Source, Linked PRR |
| Action plan field (specific) | `Mitigation` (column index 6) |
| Risk count | 40 generic + 20 project-specific |

## Common Audit Columns (JSON)

```python
# All PRR/DDR/AVR JSON risks use these field names uniformly:
FIELDS = {
    'action_plan': 'response_action',  # PRR, DDR, AVR
    'action_plan_hse': 'controls',      # HSE (different field)
    'id': 'id',
    'category': 'category',
    'probability': 'probability',
    'severity': 'severity',            # PRR, AVR: severity; DDR: impact
    'score': 'score',
    'rating': 'rating',
    'owner': 'owner',
    'status': 'status',
    'target_close': 'target_close',
}
```

## Parsing AVR from HTML

The JSON is a single `const RISK = {...};` assignment inside a `<script>` tag in `index.html`. Extract with:

```python
import re, json
with open('webapp/av/src/index.html') as f:
    content = f.read()
m = re.search(r'const RISK = (\{.+?\});', content, re.DOTALL)
if m:
    data = json.loads(m.group(1))
```
