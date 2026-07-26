# 2026-07-26 — Risk Register Matrix & HSE Mapping Fixes

## Matrix: COUNTIFS formulas → pre-calculated values

**Problem:** COUNTIFS formulas in the Dashboard matrix required LibreOffice recalculation to display values. On shared hosting (Hostinger) where `soffice` isn't installed, the matrix shows empty cells. LibreOffice install via `brew` is slow (~2 min) and can timeout.

**Fix:** Compute matrix values in Python during `build_xlsx.py` and write as hardcoded integers:

```python
ps_counts = defaultdict(int)
for rsk in risks:
    key = (rsk.get("probability"), rsk.get("severity"))
    if key[0] and key[1]:
        ps_counts[key] += 1

# Then for each P×S cell:
n = ps_counts.get((p, s), 0)
cell.value = n if n > 0 else None
```

**Trade-off:** Values are frozen at snapshot time, not dynamic. This is acceptable because snapshots are regenerated on each build.

## HSE field mapping — cause and consequence lost

**Problem:** The user restructured `hse_risks.json` and lost `hazards` (cause) and `controls` (consequence) fields. The `_scope_hse()` function was reading `r.get("hazards", "")` which returned empty.

**Fix:** Restored from git commit `d59a41b` (the last commit that still had the old field names):

```python
result = subprocess.run(
    ["git", "show", "d59a41b:06_Risk_System/generated/hse_risks.json"],
    capture_output=True, text=True
)
old = json.loads(result.stdout)
old_map = {r["id"]: r for r in old["risks"]}

for r in current_data["risks"]:
    if r["id"] in old_map:
        o = old_map[r["id"]]
        if not r.get("cause") and o.get("hazards"):
            r["cause"] = o["hazards"]
        if not r.get("consequence") and o.get("controls"):
            r["consequence"] = o["controls"]
```

**Also:** Updated scoper to use fallback pattern:
```python
"cause": r.get("cause", r.get("hazards", "")),
```

## Strategy column extraction

Response_action format: `[Strategy: Transfer] Rapid impact assessment...`

Extract the strategy name from the `[...]` prefix using regex:
```python
sm = re.match(r'^\[Strategy:\s*([^\]]+)\]\s*', raw_action)
```

## OneDrive daily sync

Created ~/.hermes/scripts/sync_risk_snapshots.sh — a no_agent cron job that runs daily at 9 AM to download latest snapshots from webapp to OneDrive submittle folder. Replaces old files (one per register per REV folder). On Sundays, creates new REV{N+1} folder.
