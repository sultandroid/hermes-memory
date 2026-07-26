---
name: single-file-webapp-maintenance
title: Single-File Web App Data Maintenance
description: Safe editing of embedded JSON data within single-file HTML/JS web apps while preserving HTML/CSS/JS structure and server-side customizations.
---

## When to use

You need to modify the data embedded in a single-file web app (e.g. risk register, lessons learned, any register built from `register-webapp-template`):
- Rename risk IDs (e.g. PRR-SMP-001 → PRR-COM-08)
- Add/remove risk records
- Update fields across many records
- Fix a data inconsistency

## Core rule: never restore from git

The server version of a single-file web app often has customizations NOT in the git repo — register navigation links, DOWNLOAD SNAPSHOT button, CSS tweaks, different header content, footer links. Doing `git checkout -- index.html` to "restore" the file **wipes all those customizations**.

Instead:
1. **Fetch the current server version** (it has the latest data AND all customizations)
2. **Modify only the JSON data portion** within the file
3. **Re-inject the modified JSON** preserving everything else
4. **Re-add any missing customizations** if you already restored from git

## Safe JSON editing workflow

### Step 1: Fetch the server version

```bash
curl -s "https://samaya-factory.com/aseer/registers/Risk/" > /tmp/index.html
```

### Step 2: Extract, modify, re-inject the JSON

```python
import json, re

# Read full HTML file
with open('/tmp/index.html') as f:
    html = f.read()

# Locate the JSON within the full HTML
# The JSON is on one line: const RISK = {...}; followed by rest of file
m = re.search(r'(const RISK = )({.*?})(;\s*$)', html, re.MULTILINE | re.DOTALL)
if not m:
    raise ValueError('RISK JSON pattern not found')

prefix = m.group(1)   # "const RISK = "
json_str = m.group(2)  # the JSON object
suffix = m.group(3)    # ";\n"

# Parse and modify
data = json.loads(json_str)
for r in data['risks']:
    if r['id'] == 'PRR-SMP-001':
        r['id'] = 'PRR-COM-08'
        # Also fix action IDs that reference old naming
        for a in r.get('actions', []):
            a['id'] = re.sub(r'^SMP-\d+-', '', a['id'])

# Re-serialize MINIFIED (same format as original)
new_json_str = json.dumps(data, ensure_ascii=False, separators=(',', ':'))

# Inject back: replace ONLY the JSON portion
new_html = html[:m.start(2)] + new_json_str + html[m.end(2):]

with open('/tmp/index.html', 'w') as f:
    f.write(new_html)
```

### Step 3: Deploy

```bash
# Deploy to BOTH server paths (main + technical-office mirror)
scp -P 65002 /tmp/index.html u517606786@samaya-factory.com:/home/u517606786/domains/samaya-factory.com/public_html/build/aseer/registers/Risk/index.html
scp -P 65002 /tmp/index.html u517606786@samaya-factory.com:/home/u517606786/domains/samaya-factory.com/public_html/build/technical-office/aseer/registers/Risk/index.html
```

### Step 4: Verify

```bash
# Check MD5 matches the deployed file (catches silent SCP failure or server-side overwrite)
MD5_LOCAL=$(md5 -q /tmp/index.html)
MD5_REMOTE=$(ssh -p 65002 u517606786@samaya-factory.com "md5sum /home/u517606786/domains/samaya-factory.com/public_html/build/aseer/registers/Risk/index.html" | awk '{print $1}')
if [ "$MD5_LOCAL" = "$MD5_REMOTE" ]; then echo "MATCH"; else echo "MISMATCH — file was overwritten after deploy"; fi

# Check file structure intact
curl -s URL | head -n 1   # MUST start with <!DOCTYPE html> or <html>
curl -s URL | tail -n 5   # MUST end with </html>

# Check rendering code intact
curl -s URL | grep -c 'init()'    # must be >= 1
curl -s URL | grep -c 'renderKPIs' # must be >= 1

# Check specific fix applied
curl -s URL | grep -c 'PRR-SMP-001'  # must be 0
curl -s URL | grep -c 'PRR-COM-08'   # must be >= 1
```

**MD5 mismatch means the file was overwritten after your SCP** — likely by the git post-commit hook. Re-deploy after disabling the hook:

```bash
chmod -x /path/to/repo/.git/hooks/post-commit
# Re-deploy
chmod +x /path/to/repo/.git/hooks/post-commit
```

### LiteSpeed cache quirk

Hostinger LiteSpeed often serves stale content even after successful SCP deploy. Signs:
- `curl -s URL | grep 'my_feature'` shows 0 but `ssh ... grep 'my_feature' server_file` shows 1
- User reports old version but server file is correct

**Fix:** Use a cache-busting query param: `curl -s "https://...?cb=$(date +%s)"`. For the user's browser, ask them to hard refresh with Cmd+Shift+R or append `?cb=1`.

This happens because LiteSpeed has its own page cache that ignores `Cache-Control: no-cache, no-store` headers. The file on disk is correct — the cache serves an old copy for up to several minutes.

## What NOT to do

### ❌ Reconstructing file from just the JSON line

```python
# This captures ONLY the JSON line, discarding everything else:
m = re.search(r'(const RISK = )({.*?})(;\s*$)', html, re.MULTILINE | re.DOTALL)
new_content = m.group(1) + new_json + m.group(3)
# Now the file contains ONLY: const RISK = {...};
# All HTML/CSS/JS before and after the JSON line is GONE
```

The regex uses `$` in MULTILINE mode which matches end-of-line, not end-of-string. So `group(3)` is just `;\n` — nothing after line break. When you reconstruct, you lose the entire HTML document.

**Signs you made this mistake:**
- `curl URL | head -1` shows `const RISK =` instead of `<!DOCTYPE html>`
- Blank/white page in browser
- User says "site broken"

### ❌ `git checkout` to restore a broken file

```bash
# If you broke the file, DON'T just:  (wipes server customizations)
git checkout -- index.html
```

Instead:
1. Restore from git to get HTML/CSS/JS structure back
2. Fetch the JSON data from the broken server file (it's still valid JSON)
3. Inject the JSON into the restored file using the safe pattern above
4. Re-add missing customizations (see below)

## Features to re-add after a git restore

If you restored from git and lost server-side customizations, here's what to check and re-add:

### Register navigation links (DDR, HSE, AVR)

Add to topbar header:

```html
<div class="reg-nav" id="registerNav"></div>
```

CSS:
```css
.reg-nav { font-family: var(--mono); font-size: 11px; color: var(--text-muted); white-space: nowrap; }
.reg-nav a { color: var(--secondary); text-decoration: none; font-weight: 600; }
.reg-nav a:hover { text-decoration: underline; }
```

JS in `renderFooter()`:
```javascript
// Register-switch nav
const regName = RISK.is_ddr ? 'Design Discipline Register (DDR)' : RISK.is_hse ? 'HSE Risk Register (Fit-Out)' : RISK.is_av ? 'AV & Multimedia Register (AVR)' : 'Master Risk Register (PRR)';
const prefix = (RISK.is_ddr || RISK.is_hse || RISK.is_av) ? '../' : '';
const siblings = [];
if (!RISK.is_ddr) siblings.push({url: prefix+'DDR/', label: 'Design (DDR)'});
if (!RISK.is_hse) siblings.push({url: prefix+'HSE/', label: 'HSE'});
if (!RISK.is_av)  siblings.push({url: prefix+'AV/',  label: 'AV'});
if (RISK.is_ddr || RISK.is_hse || RISK.is_av) siblings.push({url: '../', label: 'Master (PRR)'});
const links = siblings.map(s => `<a href="${esc(s.url)}">${esc(s.label)}</a>`).join('  -  ');
$('#registerNav').innerHTML = `Viewing: <b>${esc(regName)}</b>  -  ${links}`;
```

### DOWNLOAD SNAPSHOT button

Replace any static Excel link with:

```html
<a class="btn" id="btnSnapshot" href="javascript:void(0)" title="Download the full register snapshot">
  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><path d="M7 10l5 5 5-5"/><path d="M12 15V3"/></svg>DOWNLOAD SNAPSHOT
</a>
```

## If the file is already broken on the server

1. Restore HTML structure from git: `git checkout -- path/to/index.html`
2. The git version has full HTML/CSS/JS but outdated data
3. Fetch the current JSON from the broken server file: `curl -s URL | python3 ...`
4. Inject the good JSON into the restored HTML using the safe pattern
5. Re-add server customizations (register nav, snapshot button)
6. Deploy

## Risk ID naming conventions

### PRR (Master Risk Register)
```
PRR-{RBS_CATEGORY}-{NN}
```
- `PRR` = Project Risk Register prefix
- `{RBS_CATEGORY}` = 3-letter category code (APP, COM, DES, FLS, MEP, PRC, SCH, etc.)
- `{NN}` = 2-digit sequential number (01, 02, 03...)
All 2-digit. Do NOT use 3-digit padding (001, 002). Category in ID must match risk's actual category field.

### DDR (Design Discipline Register)
```
DDR-{RBS_CATEGORY}-{NN}
```
RBS categories: COM (Commercial), EXT (External/Authority), PRO (Procurement), QA (Quality), SCH (Schedule), TEC (Technical).
Migrated from sub-category codes like `PR-Q-001`, `CO-X-001`, `DB-M-001`, `ST-E-001`.

### AVR (AV & Multimedia Register)
```
AVR-{RBS_CATEGORY}-{NN}
```
RBS categories: HW (Hardware), IFC (IFC/Design maturity), LGT (Lighting), MEP, OPS (Operations), STR (Structure).
Migrated from mixed `PRR-AV-01`, `R-AV-08` format.

### HSE (HSE Risk Register)
```
HSE-{NN}
```
Flat sequential (single category, no RBS code in ID). Migrated from sub-group `HSE-1.1`, `HSE-2.1` format.

## Register cards HTML pattern (between KPIs and Analytics)

```html
<div class="registers" id="registers">
  <div class="reg-card reg-current">
    <div class="reg-head"><span class="reg-badge">current</span><span class="reg-code">PRR</span></div>
    <div class="reg-title">Master Risk Register</div>
    <div class="reg-sub">Project Risk Register (PRR)  -  <span class="reg-doc">ASR-SAM-RMP-001</span>  -  Rev C12</div>
    <div class="reg-stats" id="regStats"></div>
    <div class="reg-foot">61 risks  -  18 categories  -  you are here</div>
  </div>
  <a class="reg-card" href="DDR/">...DDR card...</a>
  <a class="reg-card" href="HSE/">...HSE card...</a>
  <a class="reg-card" href="AV/">...AVR card...</a>
</div>
```

## renderRegisterStats() function

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

Call from `init()`: `renderKPIs(); renderRegisterStats(); renderFooter();`

## Cross-page template updates (not just JSON)

When you change the template for one register page, replicate ALL structural changes to the other 3 sibling pages. This includes:
- Toolbar buttons (DOWNLOAD SNAPSHOT, no CSV/PRINT)
- Register nav HTML/CSS/JS
- Register cards HTML/CSS
- Any CSS class additions
- The `renderRegisterStats()` function

### AVR page was already correctly configured

The AVR page (`.../Risk/AV/`) already had proper relative paths (`href="../DDR/"`, `href="../HSE/"`) and correct `reg-current` assignment from the start. Only DDR and HSE pages had the register cards bug.

### Register nav separator inconsistency

The renderFooter() register nav code may use different separators between template versions. The more important issue is the register nav relative URL logic:

**Correct** (includes AV link and `../` prefix for sub-registers):
```javascript
const prefix = (RISK.is_ddr || RISK.is_hse || RISK.is_av) ? '../' : '';
if (!RISK.is_ddr) siblings.push({url: prefix+'DDR/', label: 'Design (DDR)'});
if (!RISK.is_hse) siblings.push({url: prefix+'HSE/', label: 'HSE'});
if (!RISK.is_av)  siblings.push({url: prefix+'AV/',  label: 'AV'});
if (RISK.is_ddr || RISK.is_hse || RISK.is_av) siblings.push({url: '../', label: 'Master (PRR)'});
```

**Wrong** (missing AV, no prefix from sub-register):
```javascript
if (!RISK.is_ddr) siblings.push({url: 'DDR/', label: 'Design (DDR)'});  // wrong path from sub-register
if (!RISK.is_hse) siblings.push({url: 'HSE/', label: 'HSE'});
if (RISK.is_ddr || RISK.is_hse) siblings.push({url: '../', label: 'Master (PRR)'});
// AV link missing entirely
```

### Register cards current-register bug on sub-pages

After restoring from git and re-adding register cards, check the correct card is marked `reg-current`:

| Page | Current card | Other cards' href | 
|------|-------------|-------------------|
| PRR | PRR (static `<div>`) | `DDR/`, `HSE/`, `AV/` |
| DDR | DDR | `../`, `../HSE/`, `../AV/` |
| HSE | HSE | `../`, `../DDR/`, `../AV/` |
| AVR | AVR | `../`, `../DDR/`, `../HSE/` |

DDR and HSE pages had the PRR card incorrectly as `reg-current` instead of their own card.

### Post-commit hook interferes with git operations

The post-commit hook runs on EVERY commit including rebase. Disable before complex git operations:
```bash
chmod -x .git/hooks/post-commit
git pull --rebase origin main
chmod +x .git/hooks/post-commit
```

### After git merge/rebase, re-verify risks.json

Every merge can revert `risks.json` to a version with DDR risks mixed in or SMP IDs restored:
```bash
python3 -c "
import json
with open('06_Risk_System/risks.json') as f: d = json.load(f)
r = d['risks']
print(f'Total: {len(r)}, SMP: {sum(1 for x in r if \"SMP\" in x[\"id\"])}, Non-PRR: {sum(1 for x in r if not x[\"id\"].startswith(\"PRR\"))}')
"
```
Fix immediately if non-PRR or SMP appear.

`template.html` at `06_Risk_System/webapp/template.html` is the source for `build_risk.py`. To make a structural change stick across all future builds:

1. Edit `template.html` (not just `src/index.html`)
2. Rebuild: `cd 06_Risk_System/webapp && python3 build_risk.py`
3. Deploy `src/index.html` to server
4. Commit `template.html` + `risks.json` + `src/index.html` to git

This prevents the post-commit hook from overwriting your customizations with the unmodified template.
