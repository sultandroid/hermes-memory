# HSE Data Restoration from Git History

## Problem

After restructuring the HSE risk data file (`hse_risks.json`), the `cause` and `consequence` fields became empty because the new format dropped `hazards` and `controls` fields.

## Solution: Merge from Git History

The old HSE data (with `hazards` and `controls` fields) still exists in git history. Extract and merge:

### Step 1: Find the right commit

```bash
cd /path/to/repo
git log --all --oneline -- "06_Risk_System/generated/hse_risks.json"
```

Look for the last commit BEFORE the data was restructured. In our case, commits `0890f8b` and `d59a41b` still had `hazards` and `controls`.

### Step 2: Extract old data and merge

```python
import json, subprocess

OLD_COMMIT = "d59a41b"  # last commit with hazards/controls

# Get old HSE data
result = subprocess.run(
    ["git", "show", f"{OLD_COMMIT}:06_Risk_System/generated/hse_risks.json"],
    capture_output=True, text=True, cwd="/path/to/repo"
)
old = json.loads(result.stdout)
old_map = {r["id"]: r for r in old["risks"]}  # index by risk ID

# Load current data
with open("06_Risk_System/hse_risks.json") as f:
    new = json.load(f)

# Merge fields
for r in new["risks"]:
    rid = r["id"]
    if rid in old_map:
        o = old_map[rid]
        if not r.get("cause") and o.get("hazards"):
            r["cause"] = o["hazards"]
        if not r.get("consequence") and o.get("controls"):
            r["consequence"] = o["controls"]

# Save
with open("06_Risk_System/hse_risks.json", "w") as f:
    json.dump(new, f, ensure_ascii=False, indent=2)
```

### Field Mapping (Old → New)

| Old field | New field | Notes |
|-----------|-----------|-------|
| `hazards` | `cause` | The hazard description IS the cause |
| `controls` | `consequence` or `response_action` | Controls are the response measures |
| `l_init` | `probability` | Likelihood initial = probability |
| `c_init` | `severity` | Consequence initial = severity |
| `response_strategy` | N/A | Not used in new format |

### Scoper Update

After merging, ensure `_scope_hse()` in both `build_snapshots.py` and `build_hse.py` reads the correct field names with fallback to old names:

```python
"title": r.get("title", r.get("activity", "")),
"cause": r.get("cause", r.get("hazards", "")),
"consequence": r.get("consequence", r.get("controls", "")),
"probability": r.get("probability", r.get("l_init", 0)),
"severity": r.get("severity", r.get("c_init", 0)),
"response_action": r.get("response_action", r.get("controls", "")),
"target_close": r.get("target_close", ""),  # NOT hardcoded empty
"actions": r.get("actions", []),  # pass-through
```
