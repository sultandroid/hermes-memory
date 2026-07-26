# Excel Snapshot Column Layout

## Risk Register Sheet — column definitions

Defined in `build_xlsx.py` as `REG_COLS` (line ~472) with data in `vals` (line ~527).

### Current columns (11 columns, EVIDENCE removed 2026-07-26)

| # | Header | Width | Alignment | Data source |
|---|---|---|---|---|
| 1 | ID | 12 | left | `r.get("id")` |
| 2 | Cat | 8 | center | `r.get("category")` |
| 3 | Rating | 10 | center | `r.get("rating")` |
| 4 | Score | 7 | center | `r.get("score")` |
| 5 | Status | 11 | center | `r.get("status")` |
| 6 | Owner | 18 | left | `r.get("owner")` |
| 7 | Target | 12 | center | `r.get("target_close")` |
| 8 | Risk Event / Title | 42 | left | `r.get("title")` |
| 9 | Cause | 38 | left | `r.get("cause")` |
| 10 | Consequence | 38 | left | `r.get("consequence")` |
| 11 | Response / Action | 42 | left | `r.get("response_action")` |

### Removing a column

Both `REG_COLS` (headers + widths + alignment) and `vals` (data rows) must be updated in sync:

```python
# In REG_COLS — remove the tuple
REG_COLS = [
    ("ID", 12, "left"),
    ...
    # ("Evidence", 30, "left"),  ← delete this line
]

# In vals — remove the corresponding data line
vals = [
    r.get("id", ""),
    ...
    # "; ".join(r.get("evidence", []) or []),  ← delete this line
]
```

### Adding a column

Add a tuple to `REG_COLS` and a corresponding `r.get(...)` to `vals` at the same index position.
