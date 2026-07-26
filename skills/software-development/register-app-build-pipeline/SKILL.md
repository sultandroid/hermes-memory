---
name: register-app-build-pipeline
title: Register App Build Pipeline — Source Data, Build, Deploy, Auto-Sync
description: |
  How the Aseer Museum risk registers (PRR, DDR, HSE, AVR, LN) are built
  from source JSON, deployed to LiteSpeed hosting, and kept in sync via
  cron jobs and git hooks. Covers the regex truncation bug, the auto-deploy
  cron that overwrites SCP, register cards current-state management, and
  risk ID conventions.
---

## When to use

You need to rebuild, deploy, or debug any of the register web apps.
You're fixing risk IDs and need the rename to stick across builds.
You SCP'd a fix but it keeps getting reverted.

## Architecture — build pipeline

Each register has a separate data file and build script:

| Register | Source JSON | Build script | Output HTML |
|----------|------------|--------------|-------------|
| PRR | `risks.json` | `build_risk.py` | `src/index.html` |
| DDR | `generated/drr_risks.json` | `build_ddr.py` | `src/DDR/index.html` |
| HSE | `generated/hse_risks.json` | `build_hse.py` | `src/HSE/index.html` |
| AVR | `risks_av.json` | `build_av.py` | `av/src/index.html` |

All share `template.html` — the build script injects data via `__RISK_DATA__` token replacement.

### Build scripts generate their own risk IDs

`build_ddr.py` creates meaningful sub-category codes (`DDR-SHC-001`, `DDR-MEP-001`, `DDR-GRA-001`, etc.). Never rename IDs in output HTML — always edit source JSON, then rebuild.

## Auto-deploy mechanisms (overwrite SCP)

The server has three mechanisms that redeploy from repo:

| Mechanism | Schedule | How it works |
|-----------|----------|-------------|
| `deploy-registers-on-commit` cron | Every 15 min | Checks repo for changes, rebuilds + SCPs |
| `register-auto-update` cron | Daily 13:00 | Runs `update-all-registers.sh` |
| Post-commit git hook | On every commit | Runs `update-all-registers.sh` |

**SCP-only changes get overwritten within 15 min.** Always commit+push to git and let auto-deploy pick them up. To deploy immediately, temporarily disable the cron:

```bash
cronjob action=pause job_id=<id>
cronjob action=resume job_id=<id>
```

Verify if a change survived auto-deploy:
```bash
ssh -p 65002 u517606786@samaya-factory.com \
  "grep -c 'YOUR_MARKER' /path/to/remote/index.html"
```

## Register cards — fixing 'current' label

All registers share `template.html` which has PRR as the default "current" card. Build output always shows PRR as current and DDR/HSE/AVR as links.

**Use post-process fix, NEVER JS-based fix in template.html.**

### ✅ Working approach: post-build fix_cards_static.py

`fix_cards_static.py` (in `06_Risk_System/webapp/`) reads the output HTML, detects register type from `RISK.is_ddr/hse/av` flags, and rewrites the `#registers` section with the correct "current" card.

To add this to a build script:
```python
if __name__ == "__main__":
    ret = main()
    import subprocess, sys as _sys
    spath = HERE / "fix_cards_static.py"
    if spath.exists():
        subprocess.run([_sys.executable, str(spath), str(OUT)], check=False)
    raise SystemExit(ret)
```

### ⛔ NEVER use JS-based DOM manipulation in template.html

Adding functions like `fixCards()` or `renderCards()` to `template.html` that manipulate the register cards at `init()` time **causes the entire page to fail** — JS parse error in the template's script block prevents ALL JavaScript from executing, resulting in a blank page with zero errors visible in browser console.

The JS injector in the build pipeline doesn't validate the template's JS correctness. A syntax error in template.html (unclosed template literal, wrong ES6 syntax, unmatched braces) silently breaks every register page built from it.

If the page loads empty (no KPIs, no table, just HTML structure), check:
```bash
node -e "
const fs = require('fs');
const html = fs.readFileSync('template.html', 'utf8');
const m = html.match(/<script>([\\s\\S]*?)<\\/script>/);
try { new Function(m[1]); console.log('JS OK'); }
catch(e) { console.log('JS ERROR:', e.message); }
"
```

### Pitfall: `Path` vs `pathlib.Path` in build scripts

When adding post-processing code to build scripts, use the correct class reference:

```python
# CORRECT — build scripts import 'import pathlib'
spath = pathlib.Path(__file__).resolve().parent / "fix_cards_static.py"

# WRONG — NameError: name 'Path' is not defined
spath = Path(__file__).resolve().parent / "fix_cards_static.py"
```

The imported module is `pathlib`, not `Path`. All build scripts use `HERE = pathlib.Path(__file__).resolve().parent` to define the working directory — reuse `HERE` when possible.

## Regex truncation bug — CRITICAL

When editing minified JSON embedded in HTML (the `const RISK = {...};` on a single line), this regex **silently TRUNCATES the file**:

```python
# WRONG — DO NOT USE
re.search(r'(const RISK = )({.*?})(;\s*$)', content, re.MULTILINE | re.DOTALL)
```

In MULTILINE mode, `$` matches end-of-line, not end-of-string. The suffix `(;\s*$)` only captures `;\n` — everything after that line (the rest of the JS, `</script>`, `</body>`, `</html>`) is LOST.

**Correct approach** — capture only the `{...}` JSON, reconstruct the full file:

```python
import json, re

# Find the JSON object between { and }
m = re.search(r'const RISK = ({.*?});', content, re.DOTALL)
head = content[:m.start(0)]           # everything before "const RISK = "
json_str = m.group(1)                 # just the JSON object
tail = content[m.end(1)+1:]           # everything after "}" (skip the ";")

# Modify the data
data = json.loads(json_str)
# ... edit data ...
new_json = json.dumps(data, ensure_ascii=False, separators=(',', ':'))

# Reconstruct the full file
content = head + f"const RISK = {new_json};" + tail
```

The key insight: `m.end(1)` is the position of the closing `}` of the JSON. Adding +1 skips the semicolon that follows. The tail then captures everything after that — the rest of the JS code, `</script>`, `</body>`, `</html>`, everything.

## Risk ID conventions

| Register | Format | Example |
|----------|--------|---------|
| PRR | `PRR-{RBS}-{NN}` | `PRR-COM-08` |
| DDR | `DDR-{CAT}-{NN}` (or `DDR-{SUB}-{NN}` via build_ddr.py) | `DDR-TEC-22`, `DDR-SHC-001` |
| AVR | `AVR-{CAT}-{NN}` | `AVR-HW-01` |
| HSE | `HSE-{NN}` (sequential) | `HSE-01` |
| LN | `LL-{NN}` | `LL-001` |

Do NOT use non-standard RBS codes like `SMP` — they don't match any standard category. Always use the project's RBS codes.

## Risk ID renaming — update every layer

When renaming IDs, propagate through ALL layers or the next build reverts it:

1. Edit source JSON
2. Rebuild (run the build script)
3. Verify output HTML has new IDs
4. Deploy (SCP or commit+push)
5. If using auto-deploy: commit+push to git

Missing any layer means the next build/cron overwrites your changes.

## Verification checklist after any deploy

```bash
# 1. Check server file has the fix
ssh -p 65002 u517606786@samaya-factory.com \
  "grep -c 'YOUR_MARKER' /path/to/remote/index.html"

# 2. Check HTTP response has the fix (use cache-buster)
curl -s "https://samaya-factory.com/aseer/registers/Risk/?v=$(date +%s)" | \
  grep -c 'YOUR_MARKER'

# 3. Check browser console for JS errors and data availability
# typeof RISK !== 'undefined' ? RISK.risks.length : 'missing'
# document.querySelectorAll('#tbody tr').length
# document.querySelector('#showing')?.textContent
```

### Browser cache vs server cache

Two separate caching layers can show stale content:

| Layer | How to verify | How to fix |
|-------|-------------|-----------|
| **Server (LiteSpeed)** | `curl -s URL \| grep 'marker'` — if missing, server hasn't updated | Wait for auto-deploy cron or SCP directly |
| **Browser** | Server has the fix (curl shows it) but browser shows old version | Hard refresh (Cmd+Shift+R) or incognito window |

Use `?v=N` cache-buster when testing, but note LiteSpeed ignores query params for cache — only browser cache is bypassed.

## Deployment paths

The `.htaccess` rewrite rule maps `/aseer/` → `/build/aseer/`:

```
RewriteEngine on
RewriteCond %{REQUEST_URI} !^/build/
RewriteRule ^(.*)$ /build/$1 [L]
```

When deploying manually, update BOTH paths:

- `/build/aseer/registers/Risk/index.html` (primary)
- `/build/technical-office/aseer/registers/Risk/index.html` (secondary)

### Reliable deploy method

Due to the auto-deploy cron overwriting SCP'd files, the only reliable method is to **commit to git and push** — let the auto-deploy pick up the changes. If you must deploy manually and need it to stick immediately: pause the cron, SCP, resume.

## Risks.json contamination — fix after every merge

`risks.json` at `06_Risk_System/risks.json` **keeps getting contaminated** with non-PRR risks (DDR, AVR, HSE) during git merges and auto-sync processes.

**Symptom:** PRR page shows >61 risks (83, 90, 109, 184). DDR-prefixed IDs appear in the PRR table.

**Check after any git operation:**
```bash
python3 -c "
import json
from collections import Counter
d = json.load(open('06_Risk_System/risks.json'))
r = d['risks']
p = Counter(x['id'].split('-')[0] for x in r)
print(f'Total: {len(r)}, SMP: {sum(1 for x in r if chr(83)+chr(77)+chr(80) in x[\"id\"])}')
for k in sorted(p): print(f'  {k}: {p[k]}')
"
```

**Fix:** strip non-PRR risks:
```python
d['risks'] = [r for r in d['risks'] if r['id'].startswith('PRR')]
for r in d['risks']:
    if r['id'] == 'PRR-SMP-001': r['id'] = 'PRR-COM-08'
    if r['id'] == 'PRR-SMP-002': r['id'] = 'PRR-PRC-13'
d['total'] = len(d['risks'])
```
Then rebuild and commit immediately.

## Excel snapshot generation

Generated by `build_snapshots.py --bump` which produces 3-sheet Samaya-templated workbooks (Dashboard / Risk Register / Action Plan). Build scripts autodetect the latest Excel via `sorted(glob("*_ACTIVE.xlsx"))[-1]`.

### Counter reset pitfall

`--bump` resets the counter. Old higher-numbered snapshots ("047") outrank new ones ("004") in `sorted()`. **Delete old files after --bump:**

```bash
cd src && rm -f EXP-RISK-PRR-2026-{001..047}_RevC*.xlsx
```

Also clean old files on the server.

### Snapshot audit checklist

| Check | Verify |
|-------|--------|
| Risk IDs match current format | DDR uses `DDR-{CAT}-{NN}`, not old `PR-Q-001` |
| Dashboard categories match register | DDR shows TEC/SCH/EXT/PRO/QA/COM, not PRR categories |
| Risk count correct | PRR=61, DDR=79, HSE=41 |
| Date is current | Not stale |
| Rev matches data | PRR=C12, DDR=C11, HSE=C11 |
| Has 3 sheets | Dashboard, Risk Register, Action Plan |

### Deploy snapshots

```bash
for f in src/EXP-RISK-PRR-*_ACTIVE.xlsx src/DDR/*_ACTIVE.xlsx src/HSE/*_ACTIVE.xlsx; do
  reg=$(echo $f | grep -oP '(PRR|DDR|HSE)')
  scp -P 65002 "$f" u517606786@samaya-factory.com:/remote/Risk/$reg/
done
```

Rebuild webapp pages after deploying so DOWNLOAD SNAPSHOT links point to new files.
