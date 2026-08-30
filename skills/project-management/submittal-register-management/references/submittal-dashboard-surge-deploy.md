# Submittal Dashboard — Update + Surge Deploy Pipeline

Recurring cron operation for the Aseer Museum submittal dashboard. Runs clean end-to-end; no failures observed.

## Exact steps

```bash
cd /Users/mohamedessa/aseer-museum-pm
python3 scripts/update_dashboard.py          # prints: "Dashboard updated: {N} total, {C} categories, {D} DA items"
mkdir -p /tmp/submittal-dashboard
cp 00_Status/submittal_dashboard.html /tmp/submittal-dashboard/index.html
cd /tmp/submittal-dashboard && surge --domain aseer-submittals.surge.sh ./
```

Deploy output: `Success! - Published to aseer-submittals.surge.sh`. Live URL: `https://aseer-submittals.surge.sh/`.

## Verify live + extract stats

```bash
curl -s -o /dev/null -w "%{http_code}" https://aseer-submittals.surge.sh/   # expect 200
```

The dashboard is a single-file SPA with an embedded `const DATA = {...}` object. Parse it from the generated HTML to report stats:

```python
import re
html = open('/tmp/submittal-dashboard/index.html').read()
m = re.search(r'const DATA = (\{.*?\n\}),', html, re.S)   # or slice from 'const DATA' to the next top-level key
```

## DATA structure (for reporting)

```js
const DATA = {
  total: 217,
  categories: {
    "Material":    { total: 8,  A:0, B:4,  C:3,  D:1, F:0, U:0 },
    "Documents":   { total: 76, A:0, B:49, C:15, D:3, F:3, U:6 },
    "Shop Dwgs":   { total: 5,  A:0, B:4,  C:1,  D:0, F:0, U:0 },
    "IFC Dwgs":    { total: 11, A:0, B:0,  C:10, D:1, F:0, U:0 },
    "Method Stmt": { total: 16, A:0, B:16, C:0,  D:0, F:0, U:0 },
    "DD Drawings": { total: 3,  A:0, B:0,  C:0,  D:0, F:0, U:3 }
  },
  deemedApproved: [ { ref, subject, days, risk }, ... ]   // 35 DA items
}
```

- **Code distribution** is per-category `A/B/C/D/F/U` counts, NOT a flat `code:"X"` field. Grepping `code:"B"` in the HTML only finds the 16 JS render-branch literals (8 B, 5 C, 3 D) — misleading. Always read the `categories` object for true counts.
- **Code A is always 0** — consistent with the standing PM rule that Code B = practical final approval (no clean Code A in practice). Don't flag it as an anomaly.
- **DA items** = `deemedApproved` array length; each carries `ref`, `subject`, `days`, `risk` (HIGH/MEDIUM/LOW). Report the HIGH-risk ones (longest `days`).

## Reporting format

Report: total, per-category table (Total/A/B/C/D/F/U), DA count + top HIGH-risk items, and confirm HTTP 200. Note the Code A = 0 convention so it isn't misread as a bug.
