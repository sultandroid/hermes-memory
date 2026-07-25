# Scoring System Validation & Cross-Document Alignment

> Verifying that the PxS/PxI scoring in every register matches the RMP-documented bands, and that terminology (PxS vs PxI) is consistent between the register column headers and the RMP document body.

## Per-Register Scoring Bands

| Register | Scale | Max Score | Critical | High | Medium | Low | RMP Reference |
|----------|-------|-----------|----------|------|--------|-----|---------------|
| PRR | PxS 4x4 (P 1-4, S 1-4) | 16 | 12-16 | 8-11 | 4-7 | 1-3 | RMP Table 14 |
| DDR | P 1-4 x I 1-5 | 20 | 12-20 | 8-11 | 4-7 | 1-3 | RMP §6.5 (5-point impact scale) |
| HSE | CxL 5x5 (C 1-5, L 1-5) | 25 | 16-25 | 10-15 | 5-9 | 1-4 | RMP Table 15 |
| AVR | PxS 4x4 (P 1-4, S 1-4) | 16 | 12-16 | 8-11 | 4-7 | 1-3 | RMP Table 14 |

**Common pitfall**: DDR scores can reach 20 (P=4, S=5). If you apply the PRR 4x4 Critical band (12-16) to DDR, entries with score >16 raise false warnings. DDR uses the same bands but with a higher max due to the 5-point severity scale.

**HSE pitfall**: HSE uses 5x5 bands (Table 15), NOT the 4x4 bands from Table 14. Score=16 is Critical per HSE bands (16-25) but would be labelled High if the 4x4 bands are mistakenly applied. This happened in the 2026-07-25 session where 11 HSE entries score 15-16 were mis-rated.

## Verification Script

```python
from collections import Counter

bands = {
    'PRR': {'Critical': (12,16), 'High': (8,11), 'Medium': (4,7), 'Low': (1,3)},
    'DDR': {'Critical': (12,20), 'High': (8,11), 'Medium': (4,7), 'Low': (1,3)},
    'HSE': {'Critical': (16,25), 'High': (10,15), 'Medium': (5,9), 'Low': (1,4)},
    'AVR': {'Critical': (12,16), 'High': (8,11), 'Medium': (4,7), 'Low': (1,3)},
}

def check_ratings(risks, bands):
    errors = []
    for r in risks:
        s = r.get('score', 0)
        ra = r.get('rating', '')
        lo, hi = bands.get(ra, (0,0))
        if not (lo <= s <= hi):
            errors.append((r['id'], s, ra, f'expected {lo}-{hi}'))
    return errors
```

## Fixing HSE Ratings (Remote Data)

HSE risk data is embedded as inline JSON in the server's `index.html` — there is NO local `risks_hse.json` file. To fix HSE ratings:

1. **Download** the live HSE HTML page
2. **Extract** the JSON from `const RISK = {...};`
3. **Modify** ratings in the parsed data
4. **Re-inject** the JSON back into the HTML (avoid `ensure_ascii=True` because `\\u` escapes break Python `re.sub`)
5. **Upload** the fixed HTML back to the server
6. **Rebuild** the HSE Excel snapshot using the build script (which fetches HSE data from the same live URL)

```python
import re, json, urllib.request, ssl
ctx = ssl._create_unverified_context()
h = urllib.request.urlopen(
    'https://samaya-factory.com/aseer/registers/Risk/HSE/',
    context=ctx).read().decode('utf8','replace')
data = json.loads(re.search(r'const RISK\s*=\s*(\{.*?\});', h, re.S).group(1))

# Fix ratings
for r in data['risks']:
    if r.get('score') == 16 and r.get('rating') == 'High':
        r['rating'] = 'Critical'  # Per 5x5 bands: 16-25 = Critical

# Re-inject JSON into HTML
new_json = json.dumps(data, indent=2, ensure_ascii=False).replace('/', '\\/')
html2 = re.sub(
    r'const RISK\s*=\s*\{.*?\};',
    lambda m: f'const RISK = {new_json};',
    html, count=1, flags=re.S)
```

**Important**: The server has no Python binary. All JSON modification must be done locally, then the fixed HTML rsync'd up.

## DDR Web Page Stale Data

The DDR web page (`.../Risk/DDR/index.html`) is a static HTML file deployed separately from the PRR/AVR pipeline (which has `build_risk.py` / `deploy.sh`). When `risks_ddr.json` is updated, the DDR HTML needs a manual rebuild:

1. Download the current DDR `index.html` from the server
2. Extract the inline `const RISK` JSON
3. Replace with the corrected local `risks_ddr.json` data
4. Upload the updated HTML

```python
# Inject corrected JSON into DDR HTML
ddr = json.loads(Path('risks_ddr.json').read_text())
new_json = json.dumps(ddr, indent=2, ensure_ascii=True)
html2 = re.sub(
    r'const RISK\s*=\s*\{.*?\};',
    lambda m: f'const RISK = {new_json};',
    html, count=1, flags=re.S)
```

## PxS vs PxI Terminology Alignment

The RMP document body uses "Impact" (Table 12: "Severity (Impact) Scale", criteria columns labelled "Cost Impact" / "Schedule Impact"). Register column headers must match:

| Location | Old Label | Correct Label |
|----------|-----------|---------------|
| Risk Register Col H | S (Severity) | I (Impact) |
| Dashboard Risk Matrix | Already correct: "Probability (rows) × Impact (cols)" | No change |

The Dashboard formula references use column letters (J=RATING, K=STATUS, L=OWNER, B=CAT) — changing the header label text does not break formulas.

## File Permissions After Deployment

rsync with `-az` (archive mode) preserves source file permissions. If the source files in `/tmp/` have `-rwx------` (700), the deployed files inherit those same restrictive permissions, blocking the web server from reading them.

**Fix**: After any rsync deployment, verify and fix permissions:

```bash
ssh server "chmod 644 /path/to/registers/*/EXP-RISK-*.xlsx"
```

Or add `--chmod=644` to the rsync command:

```bash
rsync -az --chmod=644 -e 'ssh ...' src/ user@host:target/
```

**Check command**: `ssh server "ls -la /path/*.xlsx"` — should show `-rw-r--r--` (644).

## Three Targets for Every Scoring Fix

Every scoring correction must be applied to three places:

1. **JSON data source** — the master JSON (e.g. `risks.json`, `risks_ddr.json`)
2. **Web page** — the live HTML page with inline JSON (separate deploy for DDR/HSE)
3. **Excel snapshot** — the downloadable .xlsx file (rebuild via `build_all_template_registers.py`)
4. **Submittal folder** — the OneDrive copy at `05_Submittle/REV{N}/` (copy the rebuilt snapshot)

The web page HTML and Excel snapshot can diverge if only one is rebuilt. Always verify both after a fix.
