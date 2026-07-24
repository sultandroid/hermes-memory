---
name: register-webapp-template
title: Register Web App Template — Samaya Engineering-Deck Style
description: Build any project register (risk, lessons learned, submittals, NCRs, etc.) as an interactive single-page web app matching the Samaya Engineering-Deck style guide. Deploy to samaya-factory.com with auto-update on every commit.
---

## When to use

Any time you build a **web-based register** for the Aseer Museum project — risk register, lessons learned, submittal register, NCR register, SI register, etc.

## Reference URLs

| Register | URL | Notes |
|----------|-----|-------|
| Risk Register (reference template) | https://samaya-factory.com/aseer/registers/Risk/ | Full-featured: matrix, bars, drawer, print |
| Lessons Learned (built from template) | https://samaya-factory.com/aseer/registers/LN/ | Simplified: no matrix, adapted columns |

## Template structure

### 1. Design tokens (CSS :root)

```css
:root {
  --primary:   #0F172A;   /* navy — headers, borders */
  --secondary: #0284C7;   /* sky — accents */
  --bg-app:    #EEF1F5;    /* screen gutter */
  --bg-light:  #F8FAFC;    /* alt rows */
  --text-main: #1E293B;
  --text-muted:#64748B;
  --border:    #E2E8F0;
  --border-2:  #CBD5E1;
  --fail:      #B91C1C;   /* critical / fail */
  --pass:      #15803D;   /* accept / low-risk */
  --warn:      #92400E;   /* amber */
  --accent:    #C9A84C;   /* gold — for lessons learned; change per register */
  --mono: 'IBM Plex Mono','Menlo','Monaco',ui-monospace,monospace;
}
```

### 2. Accent bar color by register type

| Register | Accent Color | Hex |
|----------|-------------|-----|
| Risk | Red (critical) | `#B91C1C` |
| Lessons Learned | Gold | `#C9A84C` |
| Submittals | Blue | `#0284C7` |
| NCRs | Red | `#B91C1C` |
| SIs | Orange | `#C2410C` |

### 3. Required sections (in order)

1. **Topbar** — sticky header with accent bar, title, doc ref, logo, action buttons (Reset, Snapshot, Print)
2. **KPI cards** — 6 cards in a grid (total, key breakdowns)
3. **Analytics** — 2-column grid: left card (category bars), right card (status + owner bars)
4. **Toolbar** — search, status chips, category/owner dropdowns, showing count
5. **Table** — sortable columns, severity stripe on left border, clickable rows
6. **Footer** — document control strip with source, revision, last updated
7. **Drawer** — slide-in detail panel with PDF print button
8. **Print sheet** — hidden `#printsheet` div for A4 Samaya formal doc output

### 4. Data format

Embed data as a JSON array in a `<script>` tag:

```javascript
const LESSONS = [
  {
    id: "LL-001",
    date: "2026-07-20",
    source: "MA-0001 rejected Code D — single supplier",
    category: "Procurement",
    rootCause: "Only 1 supplier submitted",
    impact: "Floor finishes blocked 5+ months",
    correctiveAction: "Source 3+ suppliers",
    preventiveAction: "Add minimum 3 suppliers to checklist",
    owner: "Procurement Lead",
    status: "Open",
    governingPlan: "Procurement Plan Section 6.1",
    linkedRisk: "PRR-PRC-08"
  }
];
```

### 5. Key CSS classes (from template)

| Class | Purpose |
|-------|---------|
| `.topbar` | Sticky header |
| `.kpi` | KPI card (`.c-total`, `.c-open`, `.c-critical` etc for coloring) |
| `.bar-row` | Clickable bar chart row |
| `.chip` | Filter chip (`.on` = active, `.r-critical` etc for color) |
| `.tcard` | Table card wrapper |
| `.rid` | ID cell (mono font) |
| `.cat-tag` | Category tag |
| `.rate-pill`, `.st-pill` | Status/rating pill |
| `.score-badge` | Score badge (`.b-critical`, `.b-high`, `.b-medium`, `.b-low`) |
| `.drawer` | Slide-in detail panel |
| `.scrim` | Drawer backdrop |
| `#printsheet` | Hidden A4 print layout |
| `.ps-*` | Print sheet classes (`.ps-header`, `.ps-footer`, `.ps-tbl`, `.ps-h1`, `.ps-h2`, `.ps-kv`, `.ps-note`) |

### 6. Print system

The print system uses `body.printing` class to hide all interactive chrome and show only `#printsheet`:

```css
body.printing > *:not(#printsheet) { display: none !important; }
body.printing #printsheet { display: flex !important; flex-direction: column; min-height: 267mm; }
@page { size: A4 portrait; margin: 15mm; }
```

The PDF button in the drawer:
1. Populates `#printsheet` with the selected item's data
2. Adds `class="printing"` to body
3. Calls `window.print()`
4. Removes `class="printing"` on print close (use `window.onafterprint` event)

### 7. JavaScript helpers (copy from risk template)

```javascript
const $ = (s, r=document) => r.querySelector(s);
const esc = s => String(s==null?'':s).replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
```

### 8. Deployment

**CRITICAL: Use SSH pipe deploy on LiteSpeed hosts.** SCP directly to the target path can silently return exit code 0 while the server file remains unchanged. Always verify after deploy.

```bash
# PREFERRED METHOD (most reliable — SSH pipe):
ssh -p 65002 u517606786@samaya-factory.com \
    "cat > /home/u517606786/domains/samaya-factory.com/public_html/build/aseer/registers/{NAME}/index.html" \
    < /tmp/register-app/index.html

# FALLBACK METHOD (two-step via /tmp):
scp -P 65002 -o ConnectTimeout=10 /tmp/register-app/index.html \
    u517606786@samaya-factory.com:/tmp/register_index.html
ssh -p 65002 u517606786@samaya-factory.com \
    "cp /tmp/register_index.html /home/u517606786/domains/samaya-factory.com/public_html/build/aseer/registers/{NAME}/index.html && echo OK"

# VERIFY server has the correct file (grep on server, NOT curl):
ssh -p 65002 u517606786@samaya-factory.com \
    "grep -c 'const lessons =' /home/u517606786/domains/samaya-factory.com/public_html/build/aseer/registers/{NAME}/index.html"

# VERIFY via HTTP (may show cached version — use ?v=N to bypass):
curl -s -o /dev/null -w "%{http_code}" \
    "https://samaya-factory.com/build/aseer/registers/{NAME}/?v=$(date +%s)"
```

### 8b. LiteSpeed cache busting

Hostinger uses LiteSpeed which aggressively caches HTML. After deploying a fix:

1. Add `.htaccess` in the register directory:
```
<IfModule mod_headers.c>
    Header set Cache-Control "no-cache, no-store, must-revalidate"
    Header set Pragma "no-cache"
    Header set Expires "0"
</IfModule>
<IfModule LiteSpeed>
    CacheDisable public /
</IfModule>
```

2. Add meta tags in HTML `<head>`:
```html
<meta http-equiv="Cache-Control" content="no-cache, no-store, must-revalidate">
<meta http-equiv="Pragma" content="no-cache">
<meta http-equiv="Expires" content="0">
```

3. Verify cache headers in response:
```bash
curl -s -D - -o /dev/null https://samaya-factory.com/build/aseer/registers/{NAME}/
# Look for: cache-control: no-cache, no-store, must-revalidate
```

### 9. Reference files

- Risk template: download fresh from https://samaya-factory.com/aseer/registers/Risk/
- Lessons Learned built app: `/tmp/lessons-learned-app/index.html`
- Master update script: `~/.hermes/scripts/update-all-registers.sh`

### 10. Style rules (mandatory — user will reject violations)

- **No `§` symbol** anywhere — use "Section" instead (e.g. "DMP Section 3" not "DMP Section 3")
- **No AI fingerprints** — plain English, engineer language. Never use: seamlessly, robust, cutting-edge, bespoke, leveraging, delve, navigate, holistic, streamline, game-changer, state-of-the-art, world-class, innovative, dynamic
- **No AI phrasing** — never use: "It is worth noting that", "It is important to mention", "Please be advised", "In the realm of", "When it comes to", "It should be noted"
- **Active voice** — "Samaya will install..." not "Installation will be carried out by..."
- **British English** — natural, direct, Level 6 (B2-C1) readability
- **Samaya** (not "the Contractor") when referring to ourselves
- **No emoji in print mode** — strip emoji from status labels when rendering the print sheet
- **No `**` bold markers** in data values — strip markdown bold syntax from parsed table cells
- **Write like a human engineer** — short sentences, direct statements, no fluff

### 11. Snapshot / export rules

- **Snapshot button must download CSV (Excel-compatible)**, not PDF
- CSV must include: metadata header (doc ref, revision, snapshot date/time, unique reference), KPI summary, full data table
- Filename format: `{DOC_REF}-SNAPSHOT-{YYYY-MM-DD}.csv`
- Use `text/csv` Blob download, not `window.print()`
- The individual item PDF print (via drawer button) stays as A4 print — only the full-register snapshot is CSV
- CSV rows with commas or quotes must be properly escaped (wrap in `"` and double internal `"`)

### 12. Auto-update from repo (post-commit hook + daily cron)

Wire **two** update paths so the web app stays in sync with the repo markdown.

#### Post-commit hook (instant — fires on every git commit)

Create `.git/hooks/post-commit` in the repo:

```bash
#!/bin/bash
REPO_DIR=$(cd "$(dirname "$0")/../.." && pwd)
SCRIPT="$HOME/.hermes/scripts/update-all-registers.sh"
echo "[post-commit] Updating register web apps..."
if [ -f "$SCRIPT" ]; then
    bash "$SCRIPT" 2>&1 | while IFS= read -r line; do echo "[register-update] $line"; done
fi
```

Make it executable: `chmod +x .git/hooks/post-commit`

#### Daily cron (safety net — catches anything the hook missed)

```bash
cronjob action=create name="register-auto-update" schedule="0 13 * * *" script="update-all-registers.sh" no_agent=true
```

#### Master update script (`~/.hermes/scripts/update-all-registers.sh`)

The script rebuilds ALL register apps from their source data. Each register gets its own section:

```bash
#!/bin/bash
set -e
REPO_DIR="/Users/mohamedessa/aseer-museum-pm"
SERVER="u517606786@samaya-factory.com"
REMOTE_BASE="/home/u517606786/domains/samaya-factory.com/public_html/build/aseer/registers"
SSH_OPTS="-o StrictHostKeyChecking=no"
SSH_PORT="65002"

# --- Lessons Learned (LN) ---
python3 << 'PYEOF'
# ... parse markdown, rebuild HTML, deploy ...
PYEOF
scp $SSH_OPTS -P $SSH_PORT "$INDEX_LN" "$SERVER:$REMOTE_BASE/LN/index.html"

# --- Risk Register ---
python3 build_risk.py
scp $SSH_OPTS -P $SSH_PORT "src/index.html" "$SERVER:$REMOTE_BASE/Risk/index.html"

# --- Verification ---
for reg in LN Risk; do
    curl -s -o /dev/null -w "%{http_code}" "https://samaya-factory.com/build/aseer/registers/$reg/"
done
```

#### Markdown parsing logic (critical — handles real-world table quirks)

```python
# Find the ID cell by scanning parts, not by hardcoded index
ll_id = ''
ll_idx = -1
for i, p in enumerate(parts):
    if p.startswith('LL-'):
        ll_id = p; ll_idx = i; break

# Map columns relative to LL-ID position
lesson = {
    "id": ll_id,
    "date": parts[ll_idx + 1],
    "source": clean(parts[ll_idx + 2]),
    "category": clean(parts[ll_idx + 3]),
    # ... etc
}

# Clean function: strip **, replace Section symbol
def clean(s):
    s = s.replace('**', '').replace('*', '')
    s = s.replace('\u00a7', 'Section ')
    return s.strip()

# Emoji status mapping
status_raw = parts[ll_idx + 9]
if '\U0001f534' in status_raw or 'Open' in status_raw: status = 'Open'
elif '\U0001f7e1' in status_raw or 'In Progress' in status_raw: status = 'In Progress'
elif '\U0001f7e2' in status_raw or 'Closed' in status_raw: status = 'Closed'

# JSON array replacement — marker-based, not regex
start_marker = 'const LESSONS = '
end_marker = '];'
start_idx = html.find(start_marker)
end_idx = html.find(end_marker, start_idx)
array_start = html.index('[', start_idx)
array_end = end_idx + len(end_marker)
new_html = html[:array_start] + compact + html[array_end:]
```

## 13. Pitfalls

### JavaScript structure (most common failure modes)

- **Variable name must match exactly**: The data array variable name in the `<script>` tag (e.g. `const LESSONS = [...]`) must match the variable name used in every function (e.g. `lessons.filter(...)`). A single uppercase/lowercase mismatch causes all rendering to silently produce empty output — no console error, just blank KPIs and table. Always declare as `const lessons = [...]` (lowercase) to match the function references, or add `const lessons = LESSONS;` as an alias immediately after the data block.
- **`const lessons = LESSONS.slice()` must be at TOP LEVEL, not inside a function**: If you place the slice inside `function filtered() { ... }`, the `lessons` variable is scoped to that function and all other functions (`renderKPIs`, `renderTable`, `openDrawer`, etc.) will throw `ReferenceError: lessons is not defined`. The browser console shows no error for this — the page just renders blank. Always place `const lessons = LESSONS.slice();` immediately after the data array, before any function declarations. Verify by checking `typeof lessons` in browser console after page load — it should return `'object'`, not `'undefined'`.
- **`function filtered()` must have proper opening/closing braces**: If the `const lessons` line is accidentally placed where the `filtered()` function opening brace should be, the entire JS block breaks. After `const lessons = LESSONS.slice();`, the next line must be `function filtered(){` with a proper opening brace. Check browser console for syntax errors.
- **`$` helper must be defined before `init()`**: The `const $ = s => document.querySelector(s);` line must appear before `function init()` or every `$('#kpis')` call throws. Add it as the first line inside the `<script>` block, right before `function init()`. Verify by checking `typeof $` in browser console after page load.
- **`init()` must be called**: The last line of the `<script>` block must be `init();`. If missing, the page loads but nothing renders. Verify by checking `typeof init` in browser console — if `'function'`, call it manually. If `'undefined'`, the script has a syntax error.
- **JSON syntax error in data array**: A trailing comma in the JSON array or a missing quote causes the entire script block to fail silently. Validate with `JSON.parse(JSON.stringify(LESSONS))` in browser console.
- **Sort stability**: `Array.sort()` must return 0 for equal values to preserve original order. Without this, the table order can shuffle on every sort click.
- **Modal scroll**: Set `document.body.style.overflow = 'hidden'` when modal is open, restore on close.

### Deployment (LiteSpeed hosting quirks)

- **SCP can silently fail on LiteSpeed hosts**: `scp` may return exit code 0 but the server file remains unchanged. Always verify after deploy with `ssh server "grep -c 'marker' path"`. Use SSH pipe as the primary deploy method: `ssh server "cat > path" < local_file`.
- **LiteSpeed cache persists after file update**: Hostinger uses LiteSpeed which aggressively caches HTML. Add `.htaccess` with `CacheDisable public /` and `Header set Cache-Control "no-cache, no-store, must-revalidate"`. Also add `<meta http-equiv>` cache-busting tags in the HTML `<head>`.
- **Browser cache after deploy**: After deploying a fixed HTML to the server, the browser may serve a cached version. Verify server has the fix with `curl -s URL | grep -c 'const $ ='`. If server has it but browser doesn't, hard refresh (Cmd+Shift+R) or add `?v=N` cache-buster.
- **Deploy verification sequence**: After any deploy, run this sequence: (1) `ssh server "grep -c 'marker' path"` to confirm server file is correct, (2) `curl -s URL | grep -c 'marker'` to confirm HTTP response has the fix, (3) open browser with `?v=$(date +%s)` cache-buster. If (1) and (2) pass but browser still shows old version, the issue is browser cache — hard refresh.

### Git / CI

- **Post-commit hook breaks git pull --rebase**: The hook fires on every commit, including rebase commits. During `git pull --rebase`, the hook rebuilds `index.html` which creates uncommitted changes that conflict with the rebase. Fix: temporarily disable the hook before rebasing: `chmod -x .git/hooks/post-commit && git pull --rebase && chmod +x .git/hooks/post-commit`.
- **Register validation CI fails if YAML frontmatter is removed**: The GitHub Actions workflow `validate-registers.yml` runs `scripts/validate-registers.py` which checks every file in `01_Registers/` for required YAML frontmatter fields (`last_updated`, `owner_agent`, `status`). If a register is rewritten in plain English format (e.g. `risk_register.md`), the frontmatter must be preserved or the CI will fail. Either (a) keep the `---` frontmatter block in every register file, or (b) update the validator to accept the new format.
- **Odoo sync workflow fails on PR if script missing**: The `odoo-sync.yml` workflow runs on `pull_request` trigger. If the PR branch doesn't have `scripts/odoo_sync_aseer.py`, the workflow fails. Fix: add a `check_script` step that checks if the script exists before running, and guard all subsequent steps with `if: steps.check_script.outputs.script_exists == 'true'`.
- **Approval logs are placeholder TBD by default**: Every plan folder in `03_Plans/` has an `approval_log.md` with placeholder rows (TBD dates, Draft/Under Review/Approved). These must be updated with real data when CG responses arrive. The submittal reference (ZD-XXXX) and CG code (A/B/C/D) should be recorded immediately upon receipt.

### Auto-update script

- **Auto-update script must generate valid JS**: The Python rebuild script replaces the LESSONS array content but must NOT remove the `const lessons = LESSONS.slice();` line or the `function filtered(){...}` declaration. After replacement, the script should validate that both exist. The template file is the source of truth — the script only replaces the array data, not the surrounding JS structure. If the template is manually fixed (e.g. adding `const lessons`), the script preserves it. If the template is regenerated from scratch, the script must include these lines.
- **Markdown parsing: never hardcode column indices**: The markdown table may have leading/trailing empty cells from pipe syntax. Always find the ID cell by scanning parts, then map other columns relative to it. Use `ll_idx = next(i for i, p in enumerate(parts) if p.startswith('LL-'))` pattern.
- **Multi-line cells**: Pipe-delimited markdown breaks if cells contain pipes. Pre-process to handle this.
- **CSV escaping**: Fields with commas or quotes must be wrapped in `"` and internal quotes doubled.

### Style (user will reject violations)

- **No `§` symbol** anywhere — use "Section" instead (e.g. "DMP Section 3" not "DMP §3")
- **No AI fingerprints** — plain English, engineer language. Never use: seamlessly, robust, cutting-edge, bespoke, leveraging, delve, navigate, holistic, streamline, game-changer, state-of-the-art, world-class, innovative, dynamic
- **No AI phrasing** — never use: "It is worth noting that", "It is important to mention", "Please be advised", "In the realm of", "When it comes to", "It should be noted"
- **Active voice** — "Samaya will install..." not "Installation will be carried out by..."
- **British English** — natural, direct, Level 6 (B2-C1) readability
- **Samaya** (not "the Contractor") when referring to ourselves
- **No emoji in print mode** — strip emoji from status labels when rendering the print sheet
- **No `**` bold markers** in data values — strip markdown bold syntax from parsed table cells
- **Write like a human engineer** — short sentences, direct statements, no fluff

### General

- **Font loading**: Always preconnect to Google Fonts for Inter + IBM Plex Mono
- **Print color**: Use `-webkit-print-color-adjust: exact` for colored table headers in print
- **Sticky headers**: Toolbar sticky at `top: 72px` (below topbar). On mobile, set to `position: static`
- **Drawer width**: Use `min(560px, 94vw)` for responsive drawer
- **No build tools**: Single HTML file, vanilla JS, CDN-loaded fonts only
- **Data embedding**: If the source repo is private, embed data directly; if public, fetch from raw.githubusercontent.com
- **Snapshot is CSV, not PDF**: the full-register download button must produce a CSV file, not a print-to-PDF
- **Print mode cleanup**: use `window.onafterprint` event to remove `.printing` class, not just setTimeout
