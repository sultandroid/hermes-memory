---
name: register-webapp-operations
title: Register Web App Operations — Deployment, Snapshots, Multi-Register Pipeline
description: Operations for the Aseer Museum multi-register webapp system — building, deploying, fixing cards, generating Excel snapshots, managing cron-based auto-deploy, and LiteSpeed cache busting.
---

## When to use

When deploying or troubleshooting the risk register webapps (PRR, DDR, HSE, AVR) on samaya-factory.com. Also when adding/removing columns from Excel snapshots, fixing the current register card label, or dealing with auto-deploy cron overriding manual changes.

## Build pipeline per register

```
risks.json (PRR-only)  →  build_risk.py  →  src/index.html          (PRR)
drr_risks.json         →  build_ddr.py   →  src/DDR/index.html       (DDR)
hse_risks.json         →  build_hse.py   →  src/HSE/index.html       (HSE)
risks_av.json          →  build_av.py    →  av/src/index.html         (AVR)
```

All four build scripts use `template.html` which has `__RISK_DATA__` and `__XLSX_FILE__` tokens.

## Fixing register cards (current label)

`template.html` has static register cards always showing PRR as current. Each sub-register page must show its own card as current. Use `fix_cards_static.py` post-processor:

```python
# In each build script's __main__:
if __name__ == "__main__":
    ret = main()
    import subprocess, sys as _sys, pathlib
    script = pathlib.Path(__file__).resolve().parent / "fix_cards_static.py"
    if script.exists():
        subprocess.run([_sys.executable, str(script), str(OUT)], check=False)
    raise SystemExit(ret)
```

The script detects the current register via RISK.is_ddr/is_hse/is_av flags.

**WARNING: Nesting-aware HTML replacement.** When replacing the registers `<div>`, count nested `<div>`/`</div>` to find the matching close tag. Never use `.*?</div>` regex which stops at the first inner `</div>` and eats the rest of the page.

## Risks.json contamination

`risks.json` must only contain PRR-prefixed risks. During git merges, non-PRR risks (DDR/AVR/HSE) frequently get merged in, inflating the PRR page count (e.g., 184 instead of 61).

**Also check that generated/ files haven't been moved.** The user moved data files from `generated/` subdirectory to root:

| Old path | New path |
|----------|---------|
| `06_Risk_System/generated/drr_risks.json` | `06_Risk_System/ddr_risks.json` |
| `06_Risk_System/generated/hse_risks.json` | `06_Risk_System/hse_risks.json` |
| `06_Risk_System/generated/risks_av.json` | `06_Risk_System/av_risks.json` |

Update build scripts when paths change (`build_ddr.py`, `build_hse.py`, `build_snapshots.py`).

## Fixing register cards (current label)

The template has static register cards always showing PRR as current. Each sub-register page must show its own card as current. **Two layers of defense:**

### Layer 1: Build-time fix (fix_cards_static.py)

Runs after each build. Detects current register via RISK.is_ddr/is_hse/is_av flags.

**CRITICAL — use nesting-aware HTML replacement.** When replacing the registers div, count nested `<div>`/`</div>` to find the matching close tag. Never use `.*?</div>` regex — it stops at the first inner `</div>`, eats the rest of the page, and produces an empty webapp.

### Layer 2: Runtime JS fix (fixCards in template.html init)

Auto-corrects card paths and marks the current register on every page load. Added inline in `init()` before other init code. Detects current register, adds/removes `reg-current` class, injects the `current` badge into the current register's `<a>` tag (does NOT replace it with a `<div>` — that would destroy the link), and fixes hrefs to use `../` prefix for sub-pages.

**Do NOT remove fixCards from init().** If editing register card HTML, test all 4 pages and verify fixCards still works.

**CRITICAL: fixCards must keep `<a>` tags, not swap them for `<div>`.** The original implementation replaced the current card's `<a>` with a `<div>` (`el.parentNode.replaceChild(d, el)`), making it impossible to click back to the current page. The fix is to keep the `<a>` tag and only add the badge:

```javascript
// CORRECT — keep the <a>, just add badge:
if (isCur && el.tagName === 'A') {
    var h = el.querySelector('.reg-head');
    if (h && !el.querySelector('.reg-badge')) {
        var b = document.createElement('span');
        b.className = 'reg-badge'; b.textContent = 'current';
        h.insertBefore(b, h.firstChild);
    }
}
```

Also ensure the CSS does not override the link cursor: remove `cursor: default` from `.reg-card.reg-current`.

### WARNING comments in build scripts

Both `build_ddr.py` and `build_hse.py` have prominent comments after the docstring warning agents about register card path issues.

## HSE field mapping

HSE risks in `hse_risks.json` use different field names than PRR/DDR. The `_scope_hse()` function in `build_snapshots.py` (and the mapping in `build_hse.py`) must map with fallbacks for old and new field names:

| Standard field | HSE field (preferred) | HSE field (fallback) |
|---------------|----------------------|----------------------|
| `title` | `title` | `activity` |
| `cause` | `cause` | `hazards` |
| `consequence` | `consequence` | `controls` (~ but note: controls maps to response_action) |
| `probability` | `probability` | `l_init` (likelihood) |
| `severity` | `severity` | `c_init` (consequence) |
| `score` | `score` | `score_init` |
| `response_action` | `response_action` | `controls` |
| `target_close` | `target_close` | `""` |
| `actions` | `actions` | `[]` |

**CRITICAL — c_init/l_init meaning:** `c_init` = consequence/severity rating, NOT probability. `l_init` = likelihood/probability rating, NOT severity. The original code had these backwards in the matrix formulas.

**CRITICAL — cause and consequence may be missing in the new data format.** The user restructured hse_risks.json and lost the `hazards` and `controls` fields that populated CAUSE and CONSEQUENCE. Restore them from git history:

```python
import json, subprocess

# Extract old data
result = subprocess.run(
    ["git", "show", "d59a41b:06_Risk_System/generated/hse_risks.json"],
    capture_output=True, text=True,
    cwd="/Users/mohamedessa/aseer-museum-pm"
)
old = json.loads(result.stdout)
old_map = {r["id"]: r for r in old["risks"]}

# Merge into current
for r in new_data["risks"]:
    if r["id"] in old_map:
        o = old_map[r["id"]]
        if not r.get("cause") and o.get("hazards"):
            r["cause"] = o["hazards"]
        if not r.get("consequence") and o.get("controls"):
            r["consequence"] = o["controls"]
```

Always use `r.get("new_field", r.get("old_field", default))` pattern in scoper functions to support both old and new data formats.

## Strategy column — extract from response_action prefix

The Strategy column is populated by extracting the `[Strategy: X]` prefix from the `response_action` field:

```python
import re
raw_action = r.get("response_action", "") or ""
strategy = ""
clean_action = raw_action
sm = re.match(r'^\[Strategy:\s*([^\]]+)\]\s*', raw_action)
if sm:
    strategy = sm.group(1).strip()
    clean_action = raw_action[sm.end():].strip()
```

The extracted strategy is written to the Strategy column; the remaining text goes to Response/Action.

If no strategy prefix is found, Strategy is left empty and the raw text goes to Response/Action.

## Response/Action as bullet list

Instead of displaying the raw `response_action` text (which is a long paragraph), format the `actions` array as bullet points:

```python
acts = r.get("actions", []) or []
if acts:
    bullets = "\n".join(f"• {a.get('text','')}" for a in acts if a.get('text'))
    clean_action = bullets if bullets else clean_action
```

This shows each action as a separate bullet item, making it much more readable in the Excel cell.

## Build script data path updates

When data file paths change, update:
- `build_ddr.py` — `DDR_JSON = HERE.parent / "ddr_risks.json"`
- `build_hse.py` — `HSE_JSON = HERE.parent / "hse_risks.json"`
- `build_snapshots.py` — both DDR and HSE paths

`HERE = webapp/`, so `HERE.parent = 06_Risk_System/`.

## PRR page shows 184+ risks — diagnosis

If PRR shows 184+ risks, `risks.json` has been contaminated. Check:
```python
from collections import Counter
prefixes = Counter(r['id'].split('-')[0] for r in data['risks'])
# Should show {'PRR': 61}. If more, filter.
data['risks'] = [r for r in data['risks'] if r['id'].startswith('PRR')]
```

### Excel snapshot generation

```bash
python3 build_snapshots.py          # regenerate all PRR/DDR/HSE snapshots
python3 build_snapshots.py --bump   # increment counter
cd av && python3 build_av.py        # AVR snapshot (separate build)
```

Snapshots: `src/EXP-RISK-{REG}-{SEQ}_Rev{REV}_ACTIVE.xlsx`

**Dashboard layout (cover block) — no merged cells:**
- Row 1: QR code (col A, 55px), Title (col C), Logo (col G)
- Row 2: Doc No · Contract · Rev · Status
- Row 3: Snapshot No · Date · Time · Source URL
- Row 5-6: KPI strip (TOTAL/CRITICAL/HIGH/MEDIUM/LOW/OPEN)
- Row 9: QR caption

QR and logo were previously on row 8, wasting 120px. **They must be in row 1.**

### Risk matrix — pre-calculate in Python (no formulas)

**Do NOT use COUNTIFS formulas.** LibreOffice recalculation is unreliable (fails on shared hosting, requires local install, can corrupt files). Compute matrix values in Python and write as hardcoded integers:

```python
ps_counts = defaultdict(int)
for rsk in risks:
    key = (rsk.get("probability"), rsk.get("severity"))
    if key[0] and key[1]:
        ps_counts[key] += 1

for ridx, p in enumerate(range(scale, 0, -1)):
    for s in range(1, scale + 1):
        n = ps_counts.get((p, s), 0)
        cell = ws.cell(row=rr, column=2 + s, value=n if n > 0 else None)
        # Color fill per risk band
        band = "Critical" if p*s >= 16 else "High" if p*s >= scale*2 else "Medium" if p*s >= scale else "Low"
        cell.fill = PatternFill("solid", fgColor=RATING_FILL[band] if n > 0 else GRAY_ALT)
```

The values display immediately on open — no recalc needed. Empty cells get gray fill; populated cells get color-coded fill per risk band.

### HSE matrix uses C/L labels

For HSE (Consequence × Likelihood scoring), matrix labels use `C ↓ / L →` instead of `P ↓ / S →`:

```python
p_label = "C" if data.get("is_hse") else "P"
s_label = "L" if data.get("is_hse") else "S"
```

Row labels: `C5, C4, C3, C2, C1`. Column headers: `L1, L2, L3, L4, L5`.

This is set in `_dashboard_sheet()` in `build_xlsx.py` — check `data.get("is_hse")` flag (must be True for HSE data, set in `_scope_hse()`).
**P and S columns must be added to REG_COLS:** The Risk Register sheet needs separate P (Probability) and S (Severity) columns for the COUNTIFS formulas to work. Add them after Cat and before Rating:

```python
REG_COLS = [
    ("ID",          12, "left"),
    ("Cat",          8, "center"),
    ("P",            5, "center"),   # added
    ("S",            5, "center"),   # added
    ("Rating",      10, "center"),
    ...
]
```

And in `vals` array add:
```python
r.get("probability", ""),
r.get("severity", ""),
```

**Avoid merged cells:** The user explicitly rejects merged cells. Write section headers and labels to single cells (e.g., `ws["A2"]`) instead of merging ranges. This affects: title row, doc info, meta row, section headers (BY RATING, BY STATUS, EXPOSURE BY CATEGORY, TOP OWNERS), QR caption, and footer. The only exception is images which overlay on cells without merging.

**Column customization:** Edit `REG_COLS` in `build_xlsx.py` and the `vals` array in `_register_sheet()` to add/remove columns. The EVIDENCE column was removed by user request — delete both the `("Evidence", 30, "left")` entry in REG_COLS and the `"; ".join(r.get("evidence", []) or [])` line in the vals array.

**Strategy column** — extracted from `[Strategy: X]` prefix in `response_action` field. REG_COLS entry: `("Strategy", 14, "left")` after Status.

**Response/Action as bullet list** — uses `actions` array items with `\u2022` bullets instead of raw `response_action` text.

**Rating color fill** — When P/S columns are added, `rcell` shifts from col 3 to col 5 (`rcell = ws.cell(row=row, column=5)`).

**Bold/navy column refs** — After adding Strategy: `bold=(i in (1, 6))` (ID, Score), `NAVY if i in (1, 7, 8, 10, 11)` (ID, Status, Strategy, Target, Title).

**Action Plan columns** — Keep in sync. Add Strategy after Rating, shift Action wrap_text index: `i == 5` instead of `i == 4`.

**P and S columns** must be added for COUNTIFS formulas to work (see Risk Matrix section above). The EVIDENCE column was removed as a user request.

**Snapshot file cleanup:** After regeneration, old files accumulate. The build picks the alphabetically LAST file — old files with higher sequence numbers take priority over newer ones. Always delete old snapshot files after regeneration (both local and server):

```bash
# Remove specific old files
rm src/EXP-RISK-PRR-2026-0{04,05,06}_RevC*_ACTIVE.xlsx
# Clean all but the latest (local)
ls -t src/EXP-RISK-PRR-*.xlsx | tail -n +2 | xargs rm
```

**Server-side cleanup (required — old files accumulate there too):** The deploy rsyncs `src/` but does NOT delete stale xlsx on the server. Clean all-but-latest per register over SSH after deploying:

```bash
ssh -p 65002 u517606786@samaya-factory.com \
  "cd /home/u517606786/domains/samaya-factory.com/public_html/aseer/registers/Risk; \
   ls -t EXP-RISK-PRR-*.xlsx | tail -n +2 | xargs rm -f; \
   ls -t DDR/EXP-RISK-DDR-*.xlsx | tail -n +2 | xargs rm -f; \
   ls -t HSE/EXP-RISK-HSE-*.xlsx | tail -n +2 | xargs rm -f; \
   ls -t AV/EXP-RISK-AV-*.xlsx | tail -n +2 | xargs rm -f"
```

**Git rename-detection gotcha when cleaning snapshots:** Old snapshots were force-added to git (`git add -f`), so deleting them + adding the new one makes git report them as **renames** (`R old → new`), not add+delete. To stage the deletions correctly use `git add -u` on the snapshot dirs (not just `git add -f` on the new file):

```bash
git add -f 06_Risk_System/webapp/src/EXP-RISK-PRR-*.xlsx   # new file
git add -u 06_Risk_System/webapp/src/ 06_Risk_System/webapp/av/src/  # stage deletions/renames
git add 06_Risk_System/webapp/snapshot_counter.json
```

**Full "update all register snapshots" workflow** (when the user asks to refresh the webapp + snapshots across all 4 registers):
1. `python3 build_snapshots.py --bump` → PRR/DDR/HSE fresh snapshots
2. `cd av && python3 build_av.py` → AVR snapshot (separate build, own sequence)
3. Clean old snapshots locally (all-but-latest per register)
4. `bash deploy.sh` → rsyncs all 4 pages + snapshots
5. Clean old snapshots on the server (SSH, above)
6. Verify all 4 live pages HTTP 200 + snapshot counter updated
7. `git add -f` new xlsx + `git add -u` deletions + counter, commit, push

### Risks.json and source data contamination

`risks.json` must only contain PRR-prefixed risks. `generated/drr_risks.json` must only contain DDR risks. `generated/hse_risks.json` must only contain HSE risks. `risks_av.json` must only contain AVR risks.

During git merges, these files frequently get cross-contaminated (e.g., DDR risks appear in `risks.json`, inflating the PRR page count from 61 to 90+).

**After every merge, verify ALL source files:**

```python
from collections import Counter
import json

for path, expected_prefix in [
    ('risks.json', 'PRR'),
    ('generated/drr_risks.json', 'DDR'),
    ('generated/hse_risks.json', 'HSE'),
    ('av/risks_av.json', 'AVR'),
]:
    with open(path) as f:
        data = json.load(f)
    prefixes = Counter(r['id'].split('-')[0] for r in data['risks'])
    # Check only the expected prefix exists
    for p in prefixes:
        if p != expected_prefix:
            print(f"CONTAMINATION: {path} has {p} risks")
```

Fix contamination by keeping only the expected prefix and renaming any SMP leftovers.

## Rebuild → commit → push workflow (after a risks.json change)

When a risk is added/updated in `risks.json` AND the user asks to "update the webapp too", run the full build, then commit + push:

```bash
# 1. Rebuild the HTML page from risks.json (reflects new risk, rev bump)
python3 webapp/build_risk.py          # → src/index.html (prints risk count + rev)

# 2. Regenerate Excel snapshots, bumping the counter for a fresh snapshot
python3 webapp/build_snapshots.py --bump   # → src/EXP-RISK-PRR-YYYY-NNN_Rev<rev>_ACTIVE.xlsx

# 3. Verify the new risk actually landed in the page
#    (use search_files on src/index.html for the new risk ID)

# 4. Stage: the new snapshot xlsx is GITIGNORED (*.xlsx at .gitignore)
#    but its predecessor was force-added, so track the new one explicitly:
git add -f 06_Risk_System/webapp/src/EXP-RISK-PRR-*.xlsx
git add 06_Risk_System/webapp/snapshot_counter.json 06_Risk_System/webapp/src/index.html
git commit -m "..."
```

**Push conflict (remote-ahead + post-commit hook dirty `index.html`):** The repo's post-commit hook regenerates register webapps and dirties `06_Risk_System/webapp/src/index.html` after every commit, so a non-fast-forward push is common. Sequence:

```bash
# Discard the local post-commit-dirited index.html BEFORE pulling (else rebase conflicts)
git checkout -- 06_Risk_System/webapp/src/index.html
git pull --rebase origin main
# The hook dirties index.html AGAIN after the rebase commit — discard once more
git checkout -- 06_Risk_System/webapp/src/index.html
git push origin main
```

Do NOT force-push — the discard-and-rebase flow preserves the remote's newer commits and is safe because `index.html` is auto-generated.

## Deploy SSH key — use id_rsa, NOT id_ed25519

`deploy.sh` must use `-i ~/.ssh/id_rsa`. The server **rejects** `~/.ssh/id_ed25519` (`Permission denied (publickey,password)`), even though the default-key SSH works. If a deploy fails with permission denied, check the `-i` key in `deploy.sh` and switch it to `id_rsa`. Verify which key works before assuming a network problem:

```bash
for k in id_rsa id_ed25519; do
  ssh -p 65002 -i ~/.ssh/$k -o BatchMode=yes u517606786@samaya-factory.com "echo OK_$k" 2>&1 | head -1
done
```

## Verify the DEPLOYED site, not just the local build

The local `webapp/src/index.html` and the deployed `samaya-factory.com/aseer/registers/Risk/index.html` can drift (auto-deploy cron, stale SCP, missed deploy). After any rebuild, confirm the LIVE revision and card count via SSH (not HTTP — LiteSpeed caches):

```bash
ssh -p 65002 u517606786@samaya-factory.com \
  "grep -o '\"revision\":\"[^\"]*\"' .../registers/Risk/index.html | head -1; \
   grep -o '\"id\":\"PRR-[A-Z]*-[0-9]*\"' .../registers/Risk/index.html | sort -u | wc -l"
```

**Card-count gotcha:** a superseded risk merged into another (e.g. `PRR-DES-08` merged into `PRR-AVS-02`) still appears in the `history` text as `"Merged with PRR-DES-08"`. So `grep -o 'PRR-[A-Z]*-[0-9]*'` (bare, no `"id":` prefix) over-counts by 1. Count only `"id":"PRR-..."` occurrences for the true card count.

**Sub-agent review findings are self-reports — cross-check them.** When a delegated reviewer (kimi/Codex) audits the registers, verify its claims against the actual files before acting. In one session kimi falsely reported the local webapp was stale (C12/72) and the markdown register was missing 2 rows — both were wrong on direct inspection (local was C20/73, all 73 rows present). The reliable checks are the JSON-vs-HTML ID diff and the MD table-row count:

```python
import json, re
src = {r['id'] for r in json.load(open('risks.json'))['risks']}
html = re.search(r'const RISK = (\{.+?\});', open('webapp/src/index.html').read(), re.DOTALL)
ids = {r['id'] for r in json.loads(html.group(1))['risks']}
print('missing in webapp:', sorted(src - ids), '| extra:', sorted(ids - src))
md = open('01_Registers/risk_register.md').read()
rows = set(re.findall(r'^\| \d+ \| (PRR-[A-Z]*-[0-9]*) ', md, re.M))
print('MD rows:', len(rows), '| missing:', sorted(src - rows))
```

## Auto-deploy cron overrides SCP

The `deploy-registers-on-commit` cron (every 15 min) deploys from git — it **overwrites** manually SCP'd files. Commit built HTML files to git after SCP to keep them in sync.

The `register-auto-update` cron (daily 13:00) runs `update-all-registers.sh` which rebuilds + deploys from the repo.

### LiteSpeed cache

Hostinger uses LiteSpeed which caches HTML aggressively. Even with `Cache-Control: no-cache`, the server may serve stale content for several minutes.

**Verification:** Check the server file directly via SSH, not via HTTP curl:
```bash
ssh server "grep -c 'btnXlsx' /path/to/index.html"
```

**Cache busting:** Add `?cb=$(date +%s)` to URL when testing with curl.

## Lessons Learned Webapp (LN)

The Lessons Learned register has its own webapp at `https://samaya-factory.com/build/aseer/registers/LN/`.

**Build pipeline:**
```
03_Plans/11_Quality/lessons_learned_register.md  →  update-all-registers.sh  →  /tmp/lessons-learned-app/index.html  →  SCP to server
```

The post-commit hook runs `update-all-registers.sh` which:
1. Reads the markdown register, parses all `LL-` rows
2. Injects them as a `const LESSONS = [...]` JSON array into the HTML template at `/tmp/lessons-learned-app/index.html`
3. SCPs to `samaya-factory.com/build/aseer/registers/LN/index.html`

**Template location:** `/tmp/lessons-learned-app/index.html` — this is a LOCAL file, NOT in the git repo. If it's deleted (e.g. `/tmp` cleanup), the post-commit hook fails with `FileNotFoundError: '/tmp/lessons-learned-app/index.html'`. Restore it from the server:

```bash
ssh -p 65002 u517606786@samaya-factory.com "cat /home/u517606786/domains/samaya-factory.com/public_html/build/aseer/registers/LN/index.html" > /tmp/lessons-learned-app/index.html
mkdir -p /tmp/lessons-learned-app
```

**Remote dir missing → scp fails.** The LN deploy (`update-all-registers.sh`) SCPs directly to `$REMOTE_BASE/LN/index.html`. If the remote `LN/` dir doesn't exist (e.g. after server rebuild), scp fails with `dest open ... No such file or directory`. Fix: create the dir first, and the script now does this automatically:
```bash
ssh -p 65002 u517606786@samaya-factory.com "mkdir -p /home/u517606786/domains/samaya-factory.com/public_html/build/aseer/registers/LN"
```

**Verification:** After any commit, check the hook output for `Rebuilt LN: N lessons` and `LN: HTTP 200`.

**Data source:** Only `03_Plans/11_Quality/lessons_learned_register.md` is parsed. The `01_Registers/lessons_learned_register.md` is NOT included in the webapp — it's a separate simplified register.

**ID format requirement:** The parser (inline Python in `update-all-registers.sh`) scans for `LL-` in the ID cell. Rows with numeric-only IDs (e.g. `14 | ...`) are **silently skipped**. Always prefix lesson IDs with `LL-` (e.g. `LL-018`).

**Summary-only lessons never reach the webapp.** The parser reads ONLY the table rows (lines starting with `|` that contain `LL-`). A lesson that appears only in the summary sections — "Lessons by Governing Plan" (§2), "Lessons by Status" (§3), or the PQP-KPI list — but has NO full table row is silently dropped from the webapp. Symptom: the register header says N lessons but the live page shows N−1. Fix: add the complete table row (all 13 columns) in the correct numeric position. Verify with `grep -oE 'LL-[0-9]+' /tmp/lessons-learned-app/index.html | sort -u` vs the register's `LL-` IDs.

**Adding a lesson = update 5 places, not just the table.** When capturing a new lesson, keep the register internally consistent or the webapp count and the summary counts diverge:
1. Insert the full table row (13 columns) in numeric order.
2. Bump the header count line (`> **Current quarter:** ... — **N captured**`).
3. Add the lesson to the correct "Lessons by Governing Plan" subsection and bump its count.
4. Update the "Lessons by Status" table (Open / In Progress / Closed counts + ID lists).
5. Bump `last_updated` in the frontmatter.

Then rebuild via `update-all-registers.sh` and confirm `Rebuilt LN: N lessons` + `LN: HTTP 200`.

**Reference:** `references/register-source-mapping.md` — full source file mapping across all registers.

## Daily Snapshot Sync to OneDrive

A cron job syncs the latest risk register snapshots to OneDrive daily at 9 AM:

- **Script:** `~/.hermes/scripts/sync_risk_snapshots.sh`
- **Schedule:** `0 9 * * *` (daily)
- **Destination:** `.../05_Submittle/REV{N}/01_Master_Risk_Register/` etc.
- **File naming:** `Aseer_Museum_{REG}_Snapshot_{YYYY-MM-DD}.xlsx`
- **Rotation:** Old `.xlsx` files are removed before new ones are downloaded — one file per register per rev folder.
- **Weekly rotation:** On Sundays, the script creates a new `REV{N+1}` folder and populates it fresh.

The script runs as a `no_agent` cron job — no LLM tokens consumed, just the bash script executing.

## Common build errors

### AVR snapshot has merged cells / stale xlsx files

The AVR build (`build_av.py`) uses `_next_av_seq()` which scans `av/src/` for existing `EXP-RISK-AV-*.xlsx` files and increments the highest number. Old files ACCUMULATE — the sequence counter never resets.

**Problem:** If old AVR snapshots (e.g., `...-018_RevC11_ACTIVE.xlsx`) exist in `av/src/`, the build script finds them, increments, and generates a new file like `...-019_RevC11_ACTIVE.xlsx`. But these old files were generated by an earlier version of `build_xlsx.py` that used merged cells and hardcoded matrix values. The HTML page picks the NEWEST (highest-numbered) file, but that file might have been generated before the `build_xlsx.py` fixes. The downloaded file then has 10 merged cells and 0 matrix formulas instead of the expected 0 merged cells and 25 formulas.

**Fix:** Delete ALL old AVR xlsx files before rebuilding:
```bash
rm /Users/mohamedessa/aseer-museum-pm/06_Risk_System/webapp/av/src/EXP-RISK-AV-*.xlsx
cd /Users/mohamedessa/aseer-museum-pm/06_Risk_System/webapp/av && python3 build_av.py
```

This forces the sequence counter back to 001 and generates a fresh snapshot with the current `build_xlsx.py`. After cleanup, verify:
```python
import openpyxl
wb = openpyxl.load_workbook('av/src/EXP-RISK-AV-2026-001_RevC11_ACTIVE.xlsx')
ws = wb['Dashboard']
print('Merged:', len(list(ws.merged_cells.ranges)))   # must be 0
formulas = sum(1 for r in range(12,20) for c in range(3,9) if isinstance(ws.cell(r,c).value, str) and str(ws.cell(r,c).value).startswith('='))
print('Formulas:', formulas)   # must be 25 for 5x5
```

### `build()` takes 2 positional arguments but X were given

### `build()` takes 2 positional arguments but X were given

When calling `_build_xlsx()` from a register build script, the second positional arg must use `out_path=` keyword:

```python
# WRONG:
_build_xlsx(data, str(xlsx_path), page_url=...)

# CORRECT:
_build_xlsx(data, out_path=str(xlsx_path), page_url=...)
```

### `import sys` duped after adding post-processing code

When adding `import sys` to a build script that already has it (e.g., `build_risk.py`), check for duplicates. The fix_cards_static post-processing uses `_sys` (aliased) so it doesn't conflict.

### JS template-literals in template cause parse error in older Node

The `template.html` uses ES6 backtick template literals and arrow functions. Node < 8 doesn't support these. The browser does — ignore Node validation errors about `Unexpected token '?'` on default parameters.
