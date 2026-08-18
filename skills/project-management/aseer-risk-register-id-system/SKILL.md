---
name: aseer-risk-register-id-system
title: Aseer Museum Risk Register ID Conventions & Features
description: Standardised risk ID formats, register navigation, and deployment conventions for all Aseer Museum register web apps (PRR, DDR, HSE, AVR, LN).
---

## When to use

When creating, modifying, or standardising risk IDs on any Aseer Museum register web app. Also when adding register navigation features (register nav links, register cards) or troubleshooting deployment.

## Risk ID conventions

| Register | Format | Example | Notes |
|----------|--------|---------|-------|
| PRR (Master) | `PRR-{RBS}-{NN}` | `PRR-PRC-10` | RBS = 3-letter category code, NN = 2-digit per category |
| DDR (Design) | `DDR-{CAT}-{NN}` | `DDR-TEC-17` | CAT = 3-letter category code |
| AVR (AV) | `AVR-{CAT}-{NN}` | `AVR-HW-01` | CAT = 2-3 letter code |
| HSE (Safety) | `HSE-{NN}` | `HSE-23` | Single category, flat sequential |
| LN (Lessons) | `LL-{NNN}` | `LL-023` | 3-digit sequential |

Rules:
- Zero-pad: 2 digits for PRR/DDR/AVR/HSE, 3 digits for LN
- Category code in ID matches risk object's `category` field
- Sequential per category, not global
- Gaps are OK — do not renumber

## Register Nav Links

Every register page has a nav bar in the header showing sibling registers. The nav is populated by `renderFooter()` — and must include ALL 4 sibling registers (PRR, DDR, HSE, AVR). The AV link was missing in earlier versions; ensure the AV case is handled:

```javascript
if (!RISK.is_av)  siblings.push({url: prefix+'AV/',  label: 'AV'});
```

And the ternary resolves AVR as well:
```javascript
const regName = RISK.is_ddr ? 'Design Discipline Register (DDR)' : RISK.is_hse ? 'HSE Risk Register (Fit-Out)' : RISK.is_av ? 'AV & Multimedia Register (AVR)' : 'Master Risk Register (PRR)';
```

Full register nav implementation — this goes at the top of `renderFooter()`:

```javascript
function renderFooter(){
  $('#brandSub').innerHTML = `Contract <b>${esc(RISK.contract||'')}</b> · Doc <b>${esc(RISK.doc_ref||'')}</b> · Rev <b>${esc(RISK.revision||'')}</b> · Updated <b>${esc(RISK.last_updated||'')}</b>`;
  const regName = RISK.is_ddr ? 'Design Discipline Register (DDR)' : RISK.is_hse ? 'HSE Risk Register (Fit-Out)' : RISK.is_av ? 'AV & Multimedia Register (AVR)' : 'Master Risk Register (PRR)';
  const prefix = (RISK.is_ddr || RISK.is_hse || RISK.is_av) ? '../' : '';
  const siblings = [];
  if (!RISK.is_ddr) siblings.push({url: prefix+'DDR/', label: 'Design (DDR)'});
  if (!RISK.is_hse) siblings.push({url: prefix+'HSE/', label: 'HSE'});
  if (!RISK.is_av)  siblings.push({url: prefix+'AV/',  label: 'AV'});
  if (RISK.is_ddr || RISK.is_hse || RISK.is_av) siblings.push({url: '../', label: 'Master (PRR)'});
  const links = siblings.map(s => `<a href="${esc(s.url)}">${esc(s.label)}</a>`).join('  -  ');
  $('#registerNav').innerHTML = `Viewing: <b>${esc(regName)}</b>  -  ${links}`;
  // ... rest of footer
}

## Register Cards

Between KPIs and analytics, add clickable register cards:

```html
<div class="registers" id="registers">
  <div class="reg-card reg-current">
    <div class="reg-head"><span class="reg-badge">current</span><span class="reg-code">PRR</span></div>
    <div class="reg-title">Master Risk Register</div>
    <div class="reg-stats" id="regStats"></div>
    <div class="reg-foot">61 risks - 18 categories - you are here</div>
  </div>
  <a class="reg-card" href="DDR/">...DDR...</a>
  <a class="reg-card" href="HSE/">...HSE...</a>
  <a class="reg-card" href="AV/">...AVR...</a>
</div>
```

Populate dynamically with `renderRegisterStats()` — call in `init()`:

```javascript
function renderRegisterStats(){
  const el = $('#regStats');
  if (!el) return;
  const by = r => risks.filter(x=>x.rating===r).length;
  const open = risks.filter(r=>r.status==='Open').length;
  const totalCats = (RISK.rbs_categories||[]).length || (new Set(risks.map(r=>r.category).filter(Boolean))).size;
  el.textContent = `${by('Critical')} Critical  -  ${by('High')} High  -  ${by('Medium')} Medium  -  ${by('Low')} Low  -  ${open} Open  -  ${totalCats} categories`;
}
```

## Toolbar buttons

| Button | ID | Status |
|--------|-----|--------|
| RESET | `#btnReset` | ✅ Always |
| DOWNLOAD SNAPSHOT | `#btnXlsx` (not `#btnSnapshot`) | ✅ Always — links to latest Excel snapshot file |
| CSV | `#btnCsv` | ❌ Removed per user request |
| PRINT | `#btnPrint` | ❌ Removed per user request |

The DOWNLOAD SNAPSHOT button uses the `__XLSX_FILE__` token in `template.html`, which each build script resolves to the latest `.xlsx` file in the build directory. The token replacement happens at build time, not runtime.

## Post-build processing: fix_cards_static.py

After each build script generates the HTML, `fix_cards_static.py` runs as a post-processor to inject the correct register cards markup. This is necessary because `template.html` has static cards (always showing PRR as current) but each register page should show itself as current.

The script:
1. Parses the RISK JSON from the built HTML
2. Detects `is_ddr`, `is_hse`, `is_av` flags
3. Generates register cards where:
   - The current register gets `reg-current` class with a "current" badge
   - Other registers become `<a>` links with **correct relative paths**: `../DDR/`, `../HSE/`, `../AV/` for sub-pages, `DDR/`, `HSE/`, `AV/` for the PRR page
4. Replaces the `<div class="registers" id="registers">` section entirely

**Pitfall: relative link paths on sub-pages** — from `.../Risk/DDR/`, the HSE link must be `../HSE/`, not `HSE/` (which would resolve to `.../Risk/DDR/HSE/`). The `fix_cards_static.py` handles the prefix correctly by checking the current register.

**Every build script must include this post-processing.** The pattern (added at the end of each `build_*.py`):

```python
if __name__ == "__main__":
    ret = main()
    import subprocess, sys as _sys, pathlib
    spath = pathlib.Path(__file__).resolve().parent / "fix_cards_static.py"
    if spath.exists():
        subprocess.run([_sys.executable, str(spath), str(OUT)], check=False)
    raise SystemExit(ret)
```

This must be in ALL 4 build scripts:
- `webapp/build_risk.py` — PRR ✅
- `webapp/build_ddr.py` — DDR ✅
- `webapp/build_hse.py` — HSE ✅
- `webapp/av/build_av.py` — AVR ✅ (note: fix_cards_static.py is in parent dir: `parent.parent / "fix_cards_static.py"`)

**IMPORTANT:** the `build_av.py` call to `_build_xlsx` uses keyword arguments only (the function signature has `*` separator). The old positional call `_build_xlsx(data, str(xlsx_path), ...)` fails. Use `_build_xlsx(data, out_path=str(xlsx_path), ...)`.

## Multi-register build pipeline

4 independent build scripts, all in `webapp/`:

| Register | Source data | Build script | Output |
|----------|------------|-------------|--------|
| PRR | `risks.json` | `build_risk.py` | `src/index.html` |
| DDR | `generated/drr_risks.json` | `build_ddr.py` | `src/DDR/index.html` |
| HSE | `generated/hse_risks.json` | `build_hse.py` | `src/HSE/index.html` |
| AVR | `av/risks_av.json` | `av/build_av.py` | `av/src/index.html` |

All 4 use the same `template.html` with `__RISK_DATA__` and `__XLSX_FILE__` tokens.

## HSE field mapping (critical)

HSE data in `generated/hse_risks.json` uses **different field names** than PRR/DDR/AVR. Both `build_hse.py` and `build_snapshots.py` must map these via a `_scope_hse()` function before passing to `build_xlsx.py`:

| HSE JSON field | Standard field | Notes |
|---|---|---|
| `activity` | `title` | Description of the work activity |
| `hazards` | `cause` + `consequence` | The hazard description maps to both cause and consequence |
| `controls` | `response_action` | Safety control measures |
| `l_init` | `probability` | Likelihood rating (NOT consequence) |
| `c_init` | `severity` | Consequence rating (NOT likelihood) |
| `score_init` | `score` | Initial risk score |
| `response_strategy` | *(not used in xlsx)* | Maps to HTML only |
| `owner` | `owner` | Same |
| `status` | `status` | HSE uses "Ongoing" not "Open" |

**Common mistake:** `c_init` and `l_init` were originally mapped to the wrong fields. `c_init` = consequence/severity, `l_init` = likelihood/probability. They were swapped in early builds.

**HSE matrix labels:** `build_xlsx.py` now checks `data.get("is_hse")` to display "C ↓ / L →" instead of "P ↓ / S →" for HSE registers.

The `_scope_hse()` function must also set:
- `is_hse = True` (triggers correct matrix labels)
- `rbs_categories = {"HSE": "Health, Safety & Environment"}` (prevents category table showing "—")

**Actions/evidence/history:** These fields are now passed through from source data instead of hardcoded as empty:
```python
"actions": r.get("actions", []),
"evidence": r.get("evidence", []),
"history": r.get("history", []),
```

This means if the user adds actions to `hse_risks.json`, the Action Plan sheet will populate automatically.

## Action Plan sheet audit

The Action Plan sheet reads from each risk's `actions` array. Current status:

| Register | Total Actions | Status |
|---|---|---|
| PRR | 182 | ✅ Fully populated from `risks.json` |
| DDR | 0 | ❌ `drr_risks.json` has no `actions` arrays |
| HSE | 0 | ❌ `hse_risks.json` has no `actions` arrays (waiting for user commit) |
| AVR | 26 | ✅ Populated from `risks_av.json` |

To populate DDR/HSE Action Plans, add `actions` arrays to the respective JSON files:
```json
{
  "id": "DDR-SCH-01",
  "actions": [
    {"text": "Prepare pre-approved templates", "owner": "Planner", "due": "2026-08-01", "status": "Open"},
    {"text": "Mobilise team on standby", "owner": "Planner", "due": "2026-08-05", "status": "Open"}
  ]
}
```

## Excel snapshot generation

Run from `webapp/`:
```bash
python3 build_snapshots.py --bump   # Generates PRR, DDR, HSE snapshots
cd av && python3 build_av.py        # Generates AVR snapshot (includes xlsx)
```

The xlsx is created by `build_xlsx.py` which creates a Samaya-branded 3-sheet workbook (Dashboard / Risk Register / Action Plan). Key layout (no merged cells — every cell is individual):
- Row 1: QR (A1) + Title (C1) + Logo (G1)
- Row 2: Doc info in A2
- Row 3: Snapshot metadata in A3
- Rows 5-6: KPI strip (B5:G6)
- Row 11+: Risk matrix (COUNTIFS formulas), By Rating table, By Status table, Donut chart, Category table + bar chart, Top Owners
- Footer: Samaya confidentiality notice in last row

**Key layout rules (user enforced):**
1. **No merged cells** — write each header/info cell individually; avoid `merge_cells()` entirely
2. **Risk matrix must use COUNTIFS formulas** — not hardcoded counts. Reference the Risk Register sheet's P (col C) and S (col D) columns:
   ```
   =COUNTIFS('Risk Register'!$C$12:$C$[last], p, 'Risk Register'!$D$12:$D$[last], s)
   ```
3. **P and S columns are required** in the Risk Register — add them to `REG_COLS` and the `vals` data array. They must come BEFORE the Rating column (positions 3 and 4).
4. **EVIDENCE column is excluded** from the Risk Register sheet — remove from both `REG_COLS` and `vals`
5. **Logo** is loaded from `_Style-Guides/logos archives/samaya-logo.png`  
6. **QR** generated via `segno` library, placed in A1

**Logo path:** `_Style-Guides/logos archives/samaya-logo.png`
**QR:** generated via `segno` library

## Snapshot deployment

The Excel files sit alongside the HTML in the same directory on the server:
- `{REMOTE}/Risk/EXP-RISK-PRR-2026-NNN_RevC12_ACTIVE.xlsx`
- `{REMOTE}/Risk/DDR/EXP-RISK-DDR-2026-NNN_RevC11_ACTIVE.xlsx`
- `{REMOTE}/Risk/HSE/EXP-RISK-HSE-2026-NNN_RevC11_ACTIVE.xlsx`
- `{REMOTE}/Risk/AV/EXP-RISK-AV-2026-NNN_RevC11_ACTIVE.xlsx`

After deploying a new snapshot, rebuild the HTML so `__XLSX_FILE__` resolves to the new filename. Clean old snapshot files from both local and server directories — the build script picks the highest-numbered file by sorted name.

## Deployment paths

Server `.htaccess` rewrites all requests to `/build/`. Two paths must be updated:

1. `/build/aseer/registers/{REGISTER}/index.html` — primary
2. `/build/technical-office/aseer/registers/{REGISTER}/index.html` — Tech Office alias

**Gotcha: `bash deploy.sh` alone does NOT make the site live.** `deploy.sh` rsyncs to `public_html/aseer/registers/Risk/` (the non-`/build/` path), but `.htaccess` rewrites every request to `/build/`. So the served page stays stale. The real live deploy happens ONLY via the git post-commit hook (`~/.hermes/scripts/update-all-registers.sh`), which rebuilds from source and deploys to `/build/`. **To make webapp changes appear, you MUST `git commit`** (the hook then builds + deploys + verifies HTTP 200). This bit us repeatedly: a build looked "not updated" on the live site until committed.

Verify the served build path (not the bare URL), and bypass LiteSpeed cache with a `?cb=` param:
```python
import re, json, urllib.request
c = urllib.request.urlopen(urllib.request.Request(
    'https://samaya-factory.com/build/aseer/registers/Risk/index.html?cb=check',
    headers={'Cache-Control':'no-cache'})).read().decode()
d = json.loads(re.search(r'const RISK = (\{.*?\});', c, re.DOTALL).group(1))
print(len(d['risks']), d.get('last_updated'))
```

## Recent Updates block (renderRecentUpdates in template.html)

The block shows the latest risk activity. **Original design pitfall:** it sorted risks by `last_reviewed` and showed the top 5 — so when a bulk pass sets many risks to the same `last_reviewed` date (e.g. 20+ risks all 2026-08-18), the block showed near-identical rows and looked frozen even though data changed. User: *"Recent Updates block not updates in each update why?!"* — they expect it to surface what actually changed.

Fix (applied 2026-08-18):
- Flatten **every `history` entry** across all risks into events `{date, id, title, status, text: action + ' ' + note}`, sort by date desc, show top 8.
- Add a `.ru-note` line under each title (CSS `.ru-table .ru-title .ru-note { color: var(--text-muted); font-size: 11.5px; ... }`) so the reader sees **what changed**, not just date+id+status.
- **Filter noise rows:** skip history entries matching `/no score change/i`, `/duplicate scope absorbed/i` (merge bookkeeping — action field, not note), and `/^Created$/i` (created/import rows).
- **Placement:** user wants the block ABOVE the register table (after the toolbar, before `.tcard`) so a reader sees changes first, not at the page bottom.
- Column header "What changed" (not "Title"); keep the status pill.

## `risks.json` purity

The build script `build_risk.py` generates `src/index.html` from `risks.json`. This file must contain ONLY PRR risks. DDR/AVR/HSE risks in `risks.json` will inflate the PRR page's risk count.

**Git merge conflicts** — the remote repo frequently receives commits that add DDR/AVR/HSE risks to `risks.json`. After every `git pull` or `git rebase`, verify `risks.json` contains only PRR-prefixed IDs. Fix with:
```python
prr = [r for r in risks if r['id'].startswith('PRR')]
data['risks'] = prr
```

Keep the PRR-only version committed to avoid re-contamination.

## Pitfall: editing RISK JSON in HTML safely

Do not use `re.search(r'const RISK = ({.*?});\s*$', ...)` with MULTILINE — `$` matches end of line in MULTILINE mode, truncating all content after the JSON line.

Safe approach — find by position:
```python
m = re.search(r'const RISK = ({.*?});', content, re.DOTALL)
head = content[:m.start(0)]
json_str = content[m.start(1):m.end(1)]
tail = content[m.end(0)-1+1:]  # after semicolon
# modify json_str via json.loads/dumps
new_content = head + f"const RISK = {new_json};" + tail
```

## Auto-sync mechanism

Git post-commit hook runs `~/.hermes/scripts/update-all-registers.sh` which:
1. Builds Lessons Learned from markdown → deploys to `{REMOTE}/LN/`
2. Builds Risk register from `risks.json` + `template.html` → deploys to `{REMOTE}/Risk/`
3. Currently does NOT auto-deploy DDR, AVR, or HSE — those are manually SCP'd

The auto-sync overwrites SCP changes. To make permanent changes, update the source data (`risks.json`, `template.html`) and rebuild, rather than editing the output file directly.

**Always commit built output files to git.** The `deploy-registers-on-commit` cron (every 15 min) deploys `src/index.html` and `src/DDR/index.html` directly from the committed repo versions. If you only SCP the file, the cron will overwrite it within 15 minutes. To make changes stick:
1. Rebuild the register pages with `python3 build_*.py`
2. Run `fix_cards_static.py` if needed (build scripts now do this automatically)
3. Commit the output HTML files to git
4. Push to GitHub
5. The auto-deploy cron picks them up

**Pitfall: LiteSpeed cache.** Despite `cache-control: no-cache` headers, Hostinger's LiteSpeed server may serve stale HTML for several minutes. Use `?cb=N` query parameter to bypass. Git-pushed changes will propagate eventually as the cache expires.
