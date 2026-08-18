---
name: register-webapp-maintenance
title: Register Web App Maintenance — Data Updates, Multi-Page Consistency, Repair
description: Operational notes for maintaining the Aseer Museum risk register web apps (PRR/DDR/HSE/AVR) — safe JSON data replacement, template consistency across sibling pages, toolbar preferences, and recovery from accidental overwrite.
category: software-development
---

## When to Use

- Updating risk data in any of the register web apps (PRR, DDR, HSE, AVR) at `samaya-factory.com/aseer/registers/Risk/`
- Adding or removing toolbar buttons, register navigation links, or register cards across ALL sibling pages
- Recovering from accidental overwrite where the HTML structure was replaced with only JSON data
- Building any new register page that should follow the same template pattern as the risk registers

## Safe JSON Data Replacement (Critical Pitfall)

The deployed register files have the RISK JSON minified on a single line. **Do NOT** use this pattern:

```python
# DESTRUCTIVE — LOSES ALL HTML/JS OUTSIDE THE JSON LINE
m = re.search(r'(const RISK = )({.*?})(;\s*$)', content, re.MULTILINE | re.DOTALL)
new_content = prefix + new_json_str + suffix  # WRONG
```

The `(;\s*$)` with MULTILINE only captures up to `;\n` at end of the JSON line. Everything above (DOCTYPE, CSS) and below (JS rendering) is LOST.

**Correct approach** — replace only the JSON portion between the match group boundaries:

```python
m = re.search(r'(const RISK = )({.*?})(;?\n)', content, re.MULTILINE | re.DOTALL)
prefix = m.group(1)
suffix = m.group(3)
# Parse, modify, re-serialize
data = json.loads(m.group(2))
# ... modify data ...
new_json_str = json.dumps(data, ensure_ascii=False, separators=(',', ':'))
new_content = content[:m.start(2)] + new_json_str + content[m.end(2):]
```

**Always verify after any rewrite:**
```python
assert new_content.startswith('<!DOCTYPE html>'), "Lost HTML head!"
assert '</html>' in new_content, "Lost HTML tail!"
assert 'function init()' in new_content, "Lost JS rendering code!"
```

## Template Consistency — All Sibling Registers

The risk register has 4 sibling pages sharing the same template:

| Page | Path on server | URL suffix |
|------|----------------|------------|
| PRR (Master) | `.../build/aseer/registers/Risk/index.html` | `./` |
| DDR | `.../build/aseer/registers/Risk/DDR/index.html` | `DDR/` |
| HSE | `.../build/aseer/registers/Risk/HSE/index.html` | `HSE/` |
| AVR | `.../build/aseer/registers/Risk/AV/index.html` | `AV/` |

**CRITICAL: Multiple deployment paths exist.** The server has TWO locations serving each register due to `.htaccess` rewrite rules:

- `/build/aseer/registers/{NAME}/index.html` — main path (mapped by `RewriteRule ^(.*)$ /build/$1`)
- `/build/technical-office/aseer/registers/{NAME}/index.html` — secondary path

Both must be updated. After SCP to the main path, also SCP to the technical-office path.

**CRITICAL: Server file can be silently overwritten.** The git post-commit hook may regenerate the server file after your SCP. Always verify MD5:

```bash
MD5_LOCAL=$(md5 -q local/index.html)
MD5_REMOTE=$(ssh -p 65002 u517606786@samaya-factory.com "md5sum /remote/path" | awk '{print $1}')
echo $MD5_LOCAL $MD5_REMOTE
```

**CRITICAL: Disable post-commit hook before git pull/merge.** The hook fires on merge commits and creates uncommitted changes, causing conflicts:
```bash
chmod -x .git/hooks/post-commit
git pull origin main
chmod +x .git/hooks/post-commit
```

### When modifying one register's template, replicate ALL structural changes to the other 3. Structural changes include: toolbar buttons, register nav HTML/CSS/JS, register cards, footer, any CSS class additions.

## Risk ID Convention — Standardize Across Registers

PRR uses `PRR-{RBS}-{NN}` (e.g. `PRR-COM-08`). DDR uses a different scheme with sub-category codes (`PR-Q-001`, `CO-X-001`, `DB-M-001`). AVR is mixed (`PRR-AV-01`, `R-AV-08`). HSE uses `HSE-{NN}`.

### Target format per register

| Register | Format | Example |
|----------|--------|---------|
| PRR | `PRR-{RBS}-{NN}` | `PRR-COM-08` |
| DDR | `DDR-{RBS}-{NN}` | `DDR-TEC-01` |
| AVR | `AVR-{RBS}-{NN}` | `AVR-HW-01` |
| HSE | `HSE-{NN}` | `HSE-01` |

### Renaming approach

**Do NOT auto-number sequentially** — review each risk's content and assign IDs carefully. Group by RBS category, then number within each category.

### HSE note

HSE uses flat sequential `HSE-{NN}` format (e.g. `HSE-01` through `HSE-41`). The original sub-group numbering (1.1–1.6 for Civil, 2.1–2.3 for Mechanical, etc.) was replaced for consistency with other registers. Trade grouping info is preserved in the risk title and category filter, not the ID.

## Risk ID Migration: Step by Step

1. Fetch the current HTML: `curl -s URL > local_file.html`
2. Load and parse the RISK JSON via regex+json
3. Build a rename dict from old ID → new ID: group risks by category, sort by old ID, assign sequential NN
4. Update `r['id']` for each risk
5. Update evidence text and history notes that reference old IDs
6. Re-serialize with `json.dumps(data, ensure_ascii=False, separators=(',', ':'))`
7. Replace only the JSON portion in the HTML (preserve surrounding HTML/JS)
8. Deploy to BOTH server paths
9. Verify with curl and browser

### Per-register differences to preserve

- **Axis labels**: PRR/AVR = P×S, DDR = P×I, HSE = C×L. Controlled by `is_ddr`/`is_hse`/`is_av` flags in RISK object.
- **Register nav sibling links**: `renderFooter()` computes relative URLs. From PRR: `DDR/`, `HSE/`, `AV/`. From sub-registers: `../DDR/`, `../HSE/`, `../AV/`, `../` (master).
- **Register cards**: Current register gets class `reg-current`. Stats are populated by `renderRegisterStats()`. Call it from `init()`.

### Required elements on every page

1. **Toolbar**: RESET + DOWNLOAD SNAPSHOT only. No CSV, no PRINT.
2. **Register nav (compact)**: `<div class="reg-nav" id="registerNav">` in the topbar, between LIVE SNAPSHOT tag and logo. Populated by `renderFooter()`.
3. **Register cards (big nav)**: 4 cards below KPIs, linking to sibling registers. Static HTML with `#regStats` on the current card.
4. **CSS classes**: `.reg-nav`, `.registers`, `.reg-card`, `.reg-head`, `.reg-badge`, `.reg-code`, `.reg-title`, `.reg-sub`, `.reg-doc`, `.reg-stats`, `.reg-foot`.
5. **JS function**: `renderRegisterStats()` to populate `#regStats`.
6. **All 4 buttons removed from JS bindings in `init()`**: no CSV, no PRINT, no EXCEL.

### Register cards HTML pattern

Place between KPIs div and analytics div:

```html
<div class="registers" id="registers">
  <a class="reg-card reg-current" href=".">
    <div class="reg-head"><span class="reg-badge">current</span><span class="reg-code">PRR</span></div>
    <div class="reg-title">Master Risk Register</div>
    <div class="reg-sub">...doc info...</div>
    <div class="reg-stats" id="regStats"></div>
    <div class="reg-foot">61 risks - 18 categories - you are here</div>
  </a>
  <a class="reg-card" href="DDR/">
    <div class="reg-head"><span class="reg-code">DDR</span></div>
    <div class="reg-title">Design Discipline Register</div>
    ...
    <div class="reg-foot">Open sub-register →</div>
  </a>
  <!-- repeat for HSE, AVR -->
</div>
```

### Register nav CSS

```css
.reg-nav { font-family: var(--mono); font-size: 11px; color: var(--text-muted); white-space: nowrap; }
.reg-nav a { color: var(--secondary); text-decoration: none; font-weight: 600; }
.reg-nav a:hover { text-decoration: underline; }
```

### Register cards CSS

```css
.registers { display: grid; grid-template-columns: repeat(4, minmax(0, 1fr)); gap: 12px; margin-bottom: 18px; }
.reg-card { background: #fff; border: 1px solid var(--border); border-radius: 12px; padding: 14px 16px; text-decoration: none; ... }
.reg-card.reg-current { box-shadow: inset 0 0 0 1px var(--navy); }
.reg-head { display: flex; align-items: center; gap: 8px; margin-bottom: 6px; }
.reg-badge { background: var(--navy); color: #fff; font-size: 9.5px; ... padding: 2px 7px; border-radius: 999px; }
.reg-code { font-family: 'IBM Plex Mono', monospace; font-weight: 700; font-size: 12px; ... }
.reg-title { font-size: 15px; font-weight: 700; color: var(--navy); margin-bottom: 2px; }
.reg-sub { font-size: 11.5px; color: var(--muted); margin-bottom: 8px; }
.reg-doc { font-family: 'IBM Plex Mono', monospace; }
.reg-stats { font-size: 12.5px; ... }
.reg-foot { font-size: 11px; font-weight: 600; ... }
```

### renderRegisterStats() function

```javascript
function renderRegisterStats(){
  const el = $('#regStats');
  if (!el) return;
  const by = r => risks.filter(x=>x.rating===r).length;
  const open = risks.filter(r=>r.status==='Open').length;
  const totalCats = (RISK.rbs_categories||[]).length || (new Set(risks.map(r=>r.category).filter(Boolean))).size;
  el.textContent = `${by('Critical')} Critical - ${by('High')} High - ${by('Medium')} Medium - ${by('Low')} Low - ${open} Open - ${totalCats} categories`;
}
```

Add call in `init()`: `renderKPIs(); renderRegisterStats(); renderFooter(); ...`

## Three-Layer Protection Against Auto-Deploy Overwrites

The `deploy-registers-on-commit` cron (every 15 min) and `register-auto-update` (daily at 13:00) can overwrite SCP'd fixes. Use three layers of protection:

| Layer | What | Where | How | 
|---|---|---|---|
| 1. Build-time | Post-processor rewrites HTML after build | `fix_cards_static.py` called from `build_risk.py`, `build_ddr.py`, `build_hse.py`, `build_av.py` | Detects register type from `RISK.is_ddr/hse/av` flags, rewrites card section with correct `reg-current` and relative paths |
| 2. Runtime | JS auto-corrects on every page load | `init()` in `template.html` (IIFE) | Reads current register from `RISK.is_ddr/hse/av`, swaps CSS classes and hrefs on all `.reg-card` elements |
| 3. Agent notes | Prominent warnings in build scripts | Top of `build_ddr.py`, `build_hse.py` | "CRITICAL — REGISTER CARD PATHS !!! fixCards() in template.html init() auto-corrects at runtime" |

**Layer 2 (JS) must be a simple IIFE, not a named function.** Complex JS functions injected into `template.html` caused JS parse errors (RISK undefined, 0 KPIs, 0 table rows). Keep the fix minimal and directly in `init()`.

**Layer 2 refix logic (UPDATED Jul 2026):**
- If a card is the current register: keep the `<a>` wrapper, add `reg-current` class and `current` badge, set `href="."` for page reload
- If a card is NOT the current register: if it was a `<div>`, wrap in `<a>` with correct relative href
- Fix broken hrefs: if `href` starts with `DDR/`, `HSE/`, `AV/` (relative from wrong parent), replace with `../DDR/`, `../HSE/`, `../AV/`

**CRITICAL — DO NOT replace `<a>` with `<div>` for the current card.** The old JS code did this (lines 946-956 in the original fixCards function). This broke the Master Risk Register card link on the PRR page. The correct JS keeps the `<a>` tag and only adds the badge:

```javascript
if (isCur && el.tagName === 'A') {
  var h = el.querySelector('.reg-head');
  if (h && !el.querySelector('.reg-badge')) {
    var b = document.createElement('span');
    b.className = 'reg-badge'; b.textContent = 'current';
    h.insertBefore(b, h.firstChild);
  }
}
```

The runtime JS is a safety net. The build-time post-processor should be the primary fix.

### CSS `cursor: default` — Second Trap (Equally Important)

Even after the JS is fixed, the CSS rule `.reg-card.reg-current { cursor: default; }` overrides the natural pointer cursor of the `<a>` tag. The card works as a link (clicking navigates), but there is NO visual affordance — no hand cursor, no indication it is clickable. The user perceives it as "not active" or "dead."

**Fix:** Remove `cursor: default` from the CSS rule in ALL 4 built HTML files, both templates (`template.html`, `av/template_av.html`), AND `fix_cards_static.py` (which generates the CSS).

Without this CSS fix, users see a static-looking card even though the HTML has a proper `<a href=".">`. Always pair the JS fix with the CSS fix — they are two independent causes of the same symptom.

### Debugging: curl Raw HTML vs Browser Accessibility Tree

When the browser accessibility tree shows a card as "StaticText" but `curl` confirms `<a>` in the raw HTML, the JS is manipulating the DOM after page load. This is a reliable diagnostic pattern:

```bash
# Step 1 — Check raw HTML (what the server sent)
curl -s URL | grep 'reg-card reg-current'
# → <a class="reg-card reg-current" href=".">   (correct HTML on server)

# Step 2 — Check browser DOM (what JS did after load)
# Browser console:
document.querySelector('.reg-card.reg-current').tagName
# → "DIV"  (means JS replaced the <a> — fixCards() is the culprit)
# → "A"    (means JS kept the link intact — check CSS cursor)
```

If `curl` shows `<a>` but the browser shows `DIV`, the `fixCards()` IIFE inside `init()` is swapping the tag. The destructive line is `el.parentNode.replaceChild(d, el)` — search for it and replace with the badge-only approach above.

**Also:** The accessibility tree sometimes renders `<a>` wrappers around block content as "generic" containers even when the link works. Do not trust the browser snapshot alone — always verify with `curl` against raw HTML.

## LiteSpeed Cache Can Mask Deployments

Hostinger uses LiteSpeed server which has its own cache layer. Even with `cache-control: no-cache, no-store`, LiteSpeed may serve stale pages for several minutes after SCP.

**Evidence:** SSH grep on server files shows `fixCards=1` but curl returns `fixCards=0` — because curl hits the cached version, not the file on disk.

**Workarounds:**
- Append cache buster: `?cb=timestamp` or `?v=RANDOM`
- Wait a few minutes for cache to expire
- Use SSH to verify server files directly: `ssh ... grep 'fixCards' /path/to/file`

### Register cards on sub-pages — current-register bug

**When building register cards for DDR and HSE pages**, the PRR card was incorrectly marked as `reg-current` instead of the actual current page. This also broke relative link paths.

**Correct configuration per page:**

| Page | PRR card | DDR card | HSE card | AVR card |
|------|----------|----------|----------|----------|
| PRR | `reg-current` (static) | link `DDR/` | link `HSE/` | link `AV/` |
| DDR | link `../` | `reg-current` | link `../HSE/` | link `../AV/` |
| HSE | link `../` | link `../DDR/` | `reg-current` | link `../AV/` |
| AVR | link `../` | link `../DDR/` | link `../HSE/` | `reg-current` |

**Relative paths from sub-registers** (e.g. `.../Risk/DDR/`):
- `../` = master PRR
- `../DDR/`, `../HSE/`, `../AV/` = sibling registers
- Absolute links like `HSE/` (without `../`) from a sub-register path resolve to WRONG location

### fixCards() JS: Root vs Sub-Page Path Logic (Critical)

The `fixCards()` JS in `init()` sets correct hrefs on register cards. **From the PRR root page (`/Risk/`), hrefs must be `DDR/`, `HSE/`, `AV/`** (no `../` prefix). From sub-pages (`/Risk/DDR/`), hrefs must be `../`, `../DDR/`, `../HSE/`, `../AV/`.

Without the `isRoot` check, ALL hrefs get `../` prefix, breaking navigation from the PRR page:

```javascript
var isRoot = reg === 'PRR';  // PRR is at /Risk/, sub-pages at /Risk/DDR/ etc.
// On root: href = c+'/'  (e.g. "DDR/")
// On sub-page: href = map[c]  (e.g. "../DDR/")
```

**Always verify links from ALL 4 pages after any template change:**
- PRR: `DDR/`, `HSE/`, `AV/` (direct child paths)
- DDR: `../`, `../HSE/`, `../AV/` (parent + sibling)
- HSE: `../`, `../DDR/`, `../AV/`
- AVR: `../`, `../DDR/`, `../HSE/`

### fix_cards_static.py — Post-Build Register Card Corrector

To avoid the current-register card bug permanently, use a **post-build processor** instead of JS-based fixCards() (which caused JS parse errors):

**Script location:** `06_Risk_System/webapp/fix_cards_static.py`
**Purpose:** After `build_ddr.py` or `build_hse.py` writes the output file, fix_cards_static.py re-reads it, detects the register type from `RISK.is_ddr`/`is_hse`/`is_av` flags, and rewrites the register cards section with the correct current register.

**How it works:**
1. Parse the built HTML, extract `RISK` JSON to determine current register
2. Find the registers div via nesting-aware parsing (counts `<div>` / `</div>` — NOT regex)
3. Replace all 4 register cards with correct `reg-current` assignment and relative paths
4. For each card: current = `<a class="reg-card reg-current" href=".">`, others = `<a class="reg-card" href="...">`

**Integration into build scripts:**
```python
if __name__ == "__main__":
    ret = main()
    import subprocess, sys as _sys
    script = HERE / "fix_cards_static.py"
    if script.exists():
        subprocess.run([_sys.executable, str(script), str(OUT)], check=False)
    raise SystemExit(ret)
```

**CRITICAL: Use nesting-aware div matching, NOT regex.** The old approach used `r'<div class="registers"...>.*?</div>'` which matched to the FIRST `</div>` inside the cards, eating the rest of the page content. Correct approach:
```python
start_idx = html.find(start_marker)
depth = 0; end_idx = start_idx
while end_idx < len(html):
    if html[end_idx:end_idx+4] == '<div': depth += 1; end_idx += 4
    elif html[end_idx:end_idx+6] == '</div>': depth -= 1; end_idx += 6
    else: end_idx += 1
    if depth == 0: break
```

**Added to 3 build scripts:**
- `build_risk.py`, `build_ddr.py`, `build_hse.py` all call fix_cards_static.py after building

### AVR was already correct

The AVR page (`.../Risk/AV/`) already had proper relative paths (`href="../DDR/"`, `href="../HSE/"`) and correct `reg-current` assignment from the start. It did not need the register cards fix — only DDR and HSE needed it.

### Build token replacement

Build scripts only replace `__RISK_DATA__` in template.html with JSON data. Other tokens like `__REVISION__`, `__TOTAL__`, `__CATS__` used in register cards HTML are **NOT handled** — they render as literal text. Hardcode these directly in template.html.

## Post-commit hook interferes with git operations

The post-commit hook at `.git/hooks/post-commit` runs `update-all-registers.sh` on EVERY commit, including rebase commits from `git pull --rebase`. This can:

1. **Create uncommitted changes during rebase**: The hook runs `build_risk.py` which rebuilds `src/index.html`. If the rebase modifies risks.json or template.html, the rebuilt `src/index.html` won't match what git expects, causing the rebase to fail with "unstaged changes".

2. **Overwrite manual SCP fixes**: After you SCP a fixed `src/index.html` to the server, if you then `git commit`, the hook runs and rebuilds `src/index.html` from template+risks.json, potentially overwriting template customizations that were only in `src/index.html`.

**Fix options:**
- Disable hook during complex git ops: `chmod -x .git/hooks/post-commit && git pull && chmod +x .git/hooks/post-commit`
- Or ensure all changes flow through `template.html` + `risks.json` → `build_risk.py`, never edit `src/index.html` directly for structural changes

## Rebase merge-conflict resolution (recurring, 2026-08)

The post-commit hook fires on rebase commits and rebuilds `src/index.html`, causing conflicts across multiple auto-generated files. The working sequence that resolves the full flow:

```bash
# 1. Push rejected → pull --rebase
git stash
git pull --rebase origin main

# 2. Hook may fail rebase by rebuilding index.html mid-rebase → discard it
git checkout 06_Risk_System/webapp/src/index.html
git stash pop
git push origin main

# 3. If rebase is mid-flight (multi-commit) and conflicts appear:
#    a. List conflicts
git diff --name-only --diff-filter=U
#    b. For AUTO-GENERATED files (index.html, .sync_state.json, compliance_matrix.md,
#       specialist_register.md, adel_snapshots/file_list.txt) keep the INCOMING (theirs) —
#       a daily email sync from another session often carries newer data:
git checkout --theirs .sync_state.json
git checkout --theirs 06_Risk_System/webapp/src/index.html
git checkout --theirs Technical_Office/Compliance_System/compliance_matrix.md
git add .
git rebase --continue   # may hang on post-commit scp deploy; use timeout 90 + GIT_EDITOR=true

# 4. `git rebase --continue` hangs → run with non-interactive editor + longer timeout
GIT_EDITOR=true GIT_SEQUENCE_EDITOR=true git rebase --continue
git push origin main
```

**When a conflict is in a HAND-EDITED register (e.g. `specialist_register.md`)**: do NOT blindly take theirs. Inspect the `<<<<<<< / ======= / >>>>>>>` blocks per file. The incoming "Daily email sync" version usually has richer newer rows (AD Eng, ZNA, Glasbau Hahn 1G-0009 Code C, all setwork PQs) — prefer it, but merge carefully and clean up any stray `|`/`||` table-cell artifacts from the conflict resolution. Then `git add` + `git rebase --continue`.

**Post-rebase**: verify no DDR risks leaked into `risks.json` (see the verification section below). The rebase can silently revert risk IDs.

## Server has stale files at alternate paths

The server has multiple paths serving the same register files:

```
/build/aseer/registers/Risk/          # main path (mapped by .htaccess)
/build/technical-office/aseer/registers/Risk/  # secondary — often stale
```

The `/build/technical-office/` path can retain old files with wrong risk IDs (e.g. PRR-SMP-001) long after the main path is fixed. The `.htaccess` rewrites `https://samaya-factory.com/aseer/...` → `/build/aseer/...`, so the main path is what users see, but the technical-office path is a fallback that can serve stale content.

**Always check both paths with `find` on the server:**
```bash
ssh -p 65002 u517606786@samaya-factory.com \
  "find /home/.../public_html -name 'index.html' -path '*registers/Risk*'"
```

## After git merge/rebase, re-verify risks.json

Every git merge or rebase can revert `risks.json` to a version with:
- **DDR risks mixed in** (causes PRR page to show 83 instead of 61 risks)
- **PRR-SMP-001/002 IDs** restored (SMP remnants that were renamed to COM-08/PRC-13)

**After any git operation, run:**
```bash
python3 -c "
import json
from collections import Counter
with open('06_Risk_System/risks.json') as f:
    d = json.load(f)
risks = d['risks']
p = Counter(r['id'].split('-')[0] for r in risks)
smp = sum(1 for r in risks if 'SMP' in r['id'])
print(f'Total: {len(risks)}, SMP: {smp}')
for k in sorted(p): print(f'  {k}: {p[k]}')
"
```

If DDR risks or SMP IDs appear, fix immediately:
```python
d['risks'] = [r for r in d['risks'] if r['id'].startswith('PRR') and 'SMP' not in r['id']]
```

## Verify all 4 pages respond with correct data after deploy

```bash
for url in Risk DDR HSE AV; do
    echo "=== $url ==="
    curl -s "https://samaya-factory.com/aseer/registers/$url/" | python3 -c "
import sys, json, re
h = sys.stdin.read()
m = re.search(r'const RISK = ({.*?});', h, re.DOTALL)
if m:
    d = json.loads(m.group(1))
    r = d['risks']
    print(f'  Risks: {len(r)}')
    print(f'  SMP: {sum(1 for x in r if \"SMP\" in x[\"id\"])}')
    print(f'  DOCTYPE: {h.startswith(\"<!DOCTYPE\")}')
    print(f'  /html: {\"</html>\" in h[-20:]}')
    print(f'  init(): {\"function init()\" in h}')
"
done
```

```bash
# Deploy all 4
for reg in index.html DDR/index.html HSE/index.html AV/index.html; do
  scp -P 65002 local_src/$reg u517606786@samaya-factory.com:/remote_base/aseer/registers/Risk/$reg
done

# Verify all 4 return 200
for url in "https://samaya-factory.com/aseer/registers/Risk/" \
           "https://samaya-factory.com/aseer/registers/Risk/DDR/" \
           "https://samaya-factory.com/aseer/registers/Risk/HSE/" \
           "https://samaya-factory.com/aseer/registers/Risk/AV/"; do
  curl -s -o /dev/null -w "%{http_code} $url\n" "$url"
done

# Verify no CSV/PRINT buttons exist
for url in "https://samaya-factory.com/aseer/registers/Risk/" \
           "https://samaya-factory.com/aseer/registers/Risk/DDR/" \
           "https://samaya-factory.com/aseer/registers/Risk/HSE/" \
           "https://samaya-factory.com/aseer/registers/Risk/AV/"; do
  csv=$(curl -s "$url" | grep -c "btnCsv")
  prt=$(curl -s "$url" | grep -c "btnPrint")
  echo "$url CSV:$csv PRINT:$prt"
done
```

## Recovery After Accidental Overwrite

If the HTML file is replaced with only the JSON:

1. **Restore from git**: `git checkout -- path/to/index.html`
2. This gives full HTML/JS structure but may have outdated data or be a base template
3. Fetch the current JSON from the server's broken page (the JSON itself survives even when structure is lost)
4. Use the safe JSON replacement method (preserving `[:m.start(2)]` + new JSON + `[m.end(2):]`)
5. Re-add any template customizations that existed only on the server version (register nav, register cards, toolbar preferences)
6. Deploy and verify all 4 pages

## Reference

- Full register-webapp-template: load with `skill_view(name='register-webapp-template')`
- Risk ID conventions: load with `skill_view(name='risk-register-management', file_path='references/risk-id-conventions.md')`
- fix_cards_static.py walkthrough: `skill_view(name='register-webapp-maintenance', file_path='references/fix-cards-static-pattern.md')`
- Excel snapshot audit checklist: `skill_view(name='register-webapp-maintenance', file_path='references/snapshot-audit-checklist.md')`
- Excel snapshot generation system (pipeline, columns, formulas, field mapping): `skill_view(name='register-webapp-maintenance', file_path='references/excel-snapshot-system.md')`
- HSE data restoration from git history: `skill_view(name='register-webapp-maintenance', file_path='references/hse-data-restoration.md')`

## Auto-Deploy Cron Overwrites SCP (Every 15 Minutes)

There is a cron job `deploy-registers-on-commit` that runs **every 15 minutes**. Its agent checks the repo for file changes and if any register files were modified, it rebuilds and deploys them to the server.

**SCP'd files are temporary.** If you SCP a fixed `index.html` to the server, the cron overwrites it within 15 minutes with whatever is committed to git.

**The only durable way to deploy changes:**
1. Fix the **source data** (`risks.json`, `generated/drr_risks.json`, etc.) 
2. Fix the **build scripts** (`build_risk.py`, `build_ddr.py`, `build_hse.py`)
3. Rebuild locally: run all build scripts in order
4. Commit **both source + built files** to git
5. Push to GitHub — the cron will either deploy your commit or you can SCP immediately and the next cron run won't overwrite since it matches the repo

**The daily register-auto-update cron** (run at 13:00 daily) runs `update-all-registers.sh` which only handles PRR (via `build_risk.py`) and LN. DDR, HSE, and AVR are NOT updated by this cron — only by the 15-min deploy-registers-on-commit.

### Why SCP keeps failing

Typical failure:
1. SCP corrected file → server has correct version
2. Commit/push to git → post-commit hook fires
3. Hook rebuilds `src/index.html` from `template.html` + `risks.json` (old versions)
4. Old version gets SCP'd over your fix
5. User sees old data

**Fix: always update template.html AND risks.json before committing any built output.**

## Recent Updates Block — Show Real "What Changed", Above the Table

The PRR page has a "Recent Updates" block (`#recentUpdates` + `renderRecentUpdates()` in `template.html`). User requirement (2026-08-18): it is a **reader-facing "what changed" feed**, and it must be positioned **ABOVE the register table** (immediately after the toolbar / before `.tcard`), so the reader sees recent changes first.

**Pitfall — the original block showed a flat `last_reviewed` date and looked frozen.** The first implementation sorted risks by `last_reviewed` and showed ID+title+status. Because an action-plan progress pass sets `last_reviewed` to the same date (e.g. 2026-08-18) on ~23 risks at once, the block looked static and told the reader nothing about *what* changed. The user flagged it: "Recent Updates block not updates in each update why?!"

**Fix — render from the `history[]` array, one row per real change:**
```javascript
function renderRecentUpdates(){
  const events = [];
  risks.forEach(function(r){
    (r.history || []).forEach(function(h){
      var d = h.date || ''; if (!d) return;
      var note = h.note || h.action || '';
      // SKIP internal noise:
      if (/no score change/i.test(note)) return;
      if (/duplicate scope absorbed/i.test(h.action||'')) return;   // merge bookkeeping
      if (/^Created$/i.test((h.action||'').trim())) return;          // creation rows
      var label = h.action || '';
      var full = (label + ' ' + note).trim();
      if (!full) return;
      events.push({date:d, id:r.id, title:r.title||'', status:r.status||'', text:full});
    });
  });
  events.sort((a,b)=> a.date<b.date?1 : a.date>b.date?-1:0);
  const top8 = events.slice(0,8);
  // render table: Date | ID | title + note (what changed) | Status
}
```
Columns: **Date · ID · What changed (title bold + grey note under it) · Status**. Rows clickable → `openDrawer(id)`. Show ~8 rows. Skip "No score change", merge-absorbed, and "Created" history rows — they are noise, not progress.

**CSS for the note line:**
```css
.ru-table .ru-title .ru-t { font-weight:600; color:var(--text-main); }
.ru-table .ru-title .ru-note { color:var(--text-muted); font-size:11.5px; line-height:1.4; margin-top:2px; }
```

**Deploy note:** the auto-deploy post-commit hook deploys the *built* `src/index.html` to `/build/...`. So after editing `template.html`, you must `python3 build_risk.py` (which injects data into the template) AND commit — the commit fires the hook that deploys. A bare SCP of `src/index.html` gets overwritten by the next 15-min cron if uncommitted. When verifying a change that touches the template, check the **built** `src/index.html` (not just curl the public URL) and append `?cb=` to bypass LiteSpeed cache.

## Separate Source Data Files per Register

Each register has its own source data file and build script:

| Register | Source data | Build script | Output |
|----------|------------|-------------|--------|
| PRR | `risks.json` | `build_risk.py` | `src/index.html` |
| DDR | `ddr_risks.json` | `build_ddr.py` | `src/DDR/index.html` |
| HSE | `hse_risks.json` | `build_hse.py` | `src/HSE/index.html` |
| AVR | `av_risks.json` | `build_av.py` | `av/src/index.html` |

**Do NOT mix DDR risks into `risks.json`.** During git merges, DDR-prefixed risks leak into `risks.json`, causing the PRR page to show >61 risks. Clean up immediately after any merge.

## CRITICAL: No Inline JS Functions in template.html

**Do NOT add complex JS functions directly to `template.html`.** This caused JS parse errors that broke the entire page (RISK undefined, 0 KPIs, 0 table rows).

The failure happened when I injected a `fixCards()` function using backtick template literals and arrow functions. While the syntax was valid ES6, the injection mechanism inserted it inside an existing function body, creating a nested scope issue.

**Instead, use the post-build processor approach** (`fix_cards_static.py`) which operates on the built HTML file after the build script writes it. This is safer because:
- It works at the HTML level, not JS level
- It doesn't risk JS syntax errors
- It can be independently tested by running the script directly
- It's called from the build script's `__main__` exit path

The post-processor integration pattern:
```python
if __name__ == "__main__":
    ret = main()
    import subprocess, sys as _sys
    script = HERE / "fix_cards_static.py"
    if script.exists():
        subprocess.run([_sys.executable, str(script), str(OUT)], check=False)
    raise SystemExit(ret)
```

Note: `HERE` is `pathlib.Path` — use `pathlib.Path(...)` in the post-processor code, not bare `Path(...)`, unless imported.

## CRITICAL: Nesting-Aware Regex for HTML Div Matching

When replacing a `<div>` section in HTML, **do NOT use `.*?</div>`** — this matches to the FIRST `</div>` inside the div's children, not the matching close tag. This ate the entire page content after the registers section.

Correct approach — count nested `<div>`/`</div>`:
```python
start_marker = '<div class="registers" id="registers">'
start_idx = html.find(start_marker)
depth = 0
end_idx = start_idx
while end_idx < len(html):
    if html[end_idx:end_idx+4] == '<div':
        depth += 1
        end_idx += 4
    elif html[end_idx:end_idx+6] == '</div>':
        depth -= 1
        end_idx += 6
        if depth == 0:
            break
    else:
        end_idx += 1
```

## risks.json Cleanup (Source of Build)

The `risks.json` at `06_Risk_System/risks.json` is the data source for `build_risk.py` which generates `src/index.html`. It must contain ONLY PRR risks. During git merges, DDR risks can leak into it, causing the PRR page to show 83 instead of 61 risks.

**Symptoms:** PRR page shows >61 risks; DDR-prefixed IDs appear in the PRR table.

**Fix:**
```python
import json
path = '06_Risk_System/risks.json'
with open(path) as f:
    data = json.load(f)
data['risks'] = [r for r in data['risks'] if r['id'].startswith('PRR')]
data['total'] = len(data['risks'])
with open(path, 'w') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
```
Then rebuild: `cd 06_Risk_System/webapp && python3 build_risk.py`

## template.html Update Workflow (Future-Proofing)

The `template.html` is the source template for ALL register pages. `build_risk.py` reads `template.html`, injects RISK data from `risks.json`, and writes `src/index.html`.

To make a structural change (register nav, toolbar buttons, CSS classes) permanent across all future builds:

1. **Edit `template.html`** (not just `src/index.html`)
2. **Rebuild**: `cd 06_Risk_System/webapp && python3 build_risk.py`
3. **Verify**: check the rebuilt `src/index.html` has the changes
4. **Deploy**: SCP `src/index.html` to server
5. **Commit**: git add `template.html` + `risks.json` + `src/index.html`
6. **Push**: git push origin main (auto-sync will catch the rest)

This prevents the post-commit hook from overwriting your customizations with an unmodified template.

## Full Verification After Multi-Page Deploy

```bash
# 1. HTTP status
for url in Risk DDR HSE AV; do
    echo "$url: $(curl -s -o /dev/null -w '%{http_code}' https://samaya-factory.com/aseer/registers/$url/)"
done

# 2. Risk counts and no SMP
for url in Risk DDR HSE AV; do
    curl -s "https://samaya-factory.com/aseer/registers/$url/" | python3 -c "
import sys, json, re
html = sys.stdin.read()
m = re.search(r'const RISK = ({.*?});', html, re.DOTALL)
if m:
    d = json.loads(m.group(1))
    r = d['risks']
    smp = sum(1 for x in r if 'SMP' in x['id'])
    print(f'$url: {len(r)} risks, SMP={smp}')
"
done

# 3. MD5 match between local and server (catches silent overwrite)
scp -P 65002 src/index.html u517606786@samaya-factory.com:/remote/path
MD5_LOCAL=$(md5 -q src/index.html)
MD5_REMOTE=$(ssh -p 65002 u517606786@samaya-factory.com "md5sum /remote/path" | awk '{print \$1}')
echo "Local: $MD5_LOCAL  Remote: $MD5_REMOTE  $([ \"$MD5_LOCAL\" = \"$MD5_REMOTE\" ] && echo MATCH || echo MISMATCH)"

# 4. JS rendering functions intact
for func in init renderKPIs renderFooter renderTable openDrawer; do
    curl -s URL | grep -c "function $func"
done
```
