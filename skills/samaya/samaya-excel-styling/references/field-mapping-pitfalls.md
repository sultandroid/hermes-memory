# Field Mapping Pitfalls (Risk Register Build Pipeline)

When data comes from different source JSONs with different key names, the scoper/field-mapping layer must properly translate. Common failures:

## HSE Field Mapping

The HSE data may have fields from different source formats:

| Intended Field | Old Source Key | New Source Key | Fallback |
|---|---|---|---|
| title | activity | title | title → activity |
| cause | hazards | cause | cause → hazards |
| consequence | controls | consequence | consequence → controls |
| probability | l_init | probability | probability → l_init |
| severity | c_init | severity | severity → c_init |
| response_action | controls | response_action | response_action → controls |
| target_close | (none) | target_close | empty string |
| actions | (none) | actions | empty array |
| evidence | (none) | evidence | empty array |
| history | (none) | history | empty array |

**Pattern:** Use `r.get("new_key", r.get("old_key", default))` so the scoper works with both old and new data formats.

```python
"title": r.get("title", r.get("activity", "")),
"cause": r.get("cause", r.get("hazards", "")),
"probability": r.get("probability", r.get("l_init", 0)),
"severity": r.get("severity", r.get("c_init", 0)),
```

**Never** hardcode empty strings or arrays — always pass through from source data with fallback:
```python
"actions": r.get("actions", []),  # CORRECT — passes through real data
"actions": [],                     # WRONG — always empty
```

## DDR Field Mapping

The DDR data uses `probability` and `severity` (not `impact`). The scoper must NOT use old field names:

```python
"severity": r.get("severity", 0),  # CORRECT
"severity": r.get("impact", 0),    # WRONG — impact doesn't exist in new data
```

## Strategy Column Extraction

The `response_action` field often contains a strategy prefix: `[Strategy: Transfer] Action text...`

Extract with regex in the build_xlsx.py data loop:

```python
import re
raw_action = r.get("response_action", "") or ""
strategy = ""
sm = re.match(r'^\[Strategy:\s*([^\]]+)\]\s*', raw_action)
if sm:
    strategy = sm.group(1).strip()
    clean_action = raw_action[sm.end():].strip()
```

The Strategy value goes in the Strategy column; the clean action text uses the actions array as bullet points (`• item1\n• item2`).

## P and S Column Data Types

All registers must have P and S values as integers. If the source data stores them as strings, convert:
```python
try: p = int(r.get("probability", 0))
except: p = 0
```
Matrix COUNTIFS formulas compare against integers, so string values (e.g. "4") will not match and produce 0 counts.
