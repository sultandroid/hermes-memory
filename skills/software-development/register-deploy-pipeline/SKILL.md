---
name: register-deploy-pipeline
title: Register Deploy Pipeline — XLSX Generation, Sub-Register Split, rsync Safety
description: Deploy a Samaya register web app + its Excel snapshot to samaya-factory.com. Covers the xlsx-from-JSON generation pattern (no OneDrive), the master + DMP-chapter sub-register split, rsync --delete safety for sibling subdirs, and the EXP-RISK-{PLAN}-{YEAR}-{SEQ}_Rev{REV}_{STATE}.xlsx versioning convention.
---

## When to use

Any time you deploy (or fix the deploy of) a Samaya register web app at `samaya-factory.com/aseer/registers/{NAME}/`. Specifically:

- The EXCEL/Snapshot download button is 404'ing (xlsx missing on the server).
- The register is being split into a master + DMP-chapter sub-registers (e.g. PRR + DDR + HSE).
- `rsync --delete` is being used in `deploy.sh` and there are sibling subdirs on the server that must not be wiped.
- The data is in a JSON file and the build script copies the xlsx from OneDrive (unreliable, breaks deploys).

## Reference URLs

- Master PRR: https://samaya-factory.com/aseer/registers/Risk/
- DDR sub-register: https://samaya-factory.com/aseer/registers/Risk/DDR/
- HSE sub-register: https://samaya-factory.com/aseer/registers/Risk/HSE/

## The four lessons (in priority order)

### 1. Generate the xlsx from JSON — never copy from OneDrive

The single most common cause of a broken EXCEL download is a deploy script that does:

```bash
MASTER="/Users/mohamedessa/Library/CloudStorage/OneDrive-SAMAYAINVESTMENT/...xlsx"
if [ -f "$MASTER" ]; then
  cp "$MASTER" "src/$(basename "$MASTER")"
fi
```

OneDrive sync is unreliable: the file can be 0 bytes, missing, or stale. When that happens, the deployed page 404's the EXCEL button.

**Fix:** generate the xlsx locally from the same JSON that drives the webapp. A `build_xlsx.py` module should expose:

```python
def build(data: dict, out_path: str, *,
          page_url: str, register: str, doc_no: str, doc_ref: str,
          revision: str, status: str, total: int,
          scale: int = 4, snapshot_no: int = None) -> str:
    """Build a Samaya-templated multi-sheet workbook (Dashboard, Register, Action Plan)."""
```

Wire it into the build script right after the HTML write:

```python
from build_xlsx import build as _build_xlsx
xlsx_path = OUT_DIR / xlsx_name
snapshot_date = str(data.get("last_updated", "") or "")
_build_xlsx(data, str(xlsx_path),
            page_url=cfg["page_url"],
            register=cfg["register"],
            doc_no=cfg["doc_no"],
            doc_ref=cfg["doc_ref"],
            revision=rev,
            status="ACTIVE",
            total=n,
            scale=cfg.get("scale", 4),
            snapshot_no=xlsx_seq)
os.chmod(xlsx_path, 0o644)  # web server needs world-read
```

**CRITICAL: `build()` uses keyword-only arguments** (the `*` in the signature). Do NOT pass extra positional args — `_build_xlsx(data, xlsx_path, snapshot_date, rev, n)` fails with `TypeError: takes 2 positional arguments but 5 were given`.

Now the xlsx is byte-for-byte reproducible from `risks.json`. No OneDrive in the loop. If a sub-register has a different shape (e.g. DDR uses different categories), give it its own `build_xlsx_ddr.py`.

### 2. `rsync --delete` wipes sibling subdirs — always exclude

`rsync -avz --delete ./src/ DEST/` deletes **everything** in DEST that isn't in `src/`. If you have sibling subdirs on the server (e.g. `DEST/DDR/`, `DEST/HSE/`) that are deployed by a different pipeline or have already been deployed manually, `--delete` will wipe them.

**Fix:** explicitly exclude them. The non-negotiable line in any `deploy.sh` that has siblings:

```bash
rsync -avz --delete \
  --exclude='DDR/' --exclude='HSE/' \
  -e "ssh -p ${PORT} -o StrictHostKeyChecking=no" \
  ./src/ "${USER}@${HOST}:${TARGET_DIR}/"
```

Alternative if siblings are managed elsewhere: don't use `--delete` at all. Manually delete only the files you intend to replace.

**Always** auto-create the subdir's `.htaccess` the first time the master deploy runs, so a new sub-register ships with the right MIME types and `CacheDisable`:

```bash
ssh -p "${PORT}" "${USER}@${HOST}" \
  "for d in DDR HSE; do \
     mkdir -p ${TARGET_DIR}/\$d; \
     printf 'AddType application/vnd.openxmlformats-officedocument.spreadsheetml.sheet .xlsx\\nAddType text/csv .csv\\n<IfModule mod_headers.c>\\n  Header set Cache-Control no-cache, no-store, must-revalidate\\n  Header set Pragma no-cache\\n  Header set Expires 0\\n</IfModule>\\n<IfModule LiteSpeed>\\n  CacheDisable public /\\n</IfModule>\\n' > ${TARGET_DIR}/\$d/.htaccess; \
   done"
```

### 3. SEQ auto-increment for `EXP-RISK-{PLAN}-{YEAR}-{SEQ}_Rev{REV}_{STATE}.xlsx`

The deployed file convention. SEQ is the export sequence number — always **increment**, never overwrite. The build script should scan `src/` for existing `EXP-RISK-{PLAN}-{YEAR}-NNN_*.xlsx` files and return `max+1`:

```python
def _next_prr_seq(out_dir: pathlib.Path, year: int) -> int:
    pat = re.compile(rf"^EXP-RISK-PRR-{year}-(\d{{3}})_.*\.xlsx$")
    max_seq = 0
    if out_dir.is_dir():
        for p in out_dir.iterdir():
            m = pat.match(p.name)
            if m:
                max_seq = max(max_seq, int(m.group(1)))
    return max_seq + 1
```

Use `{xlsx_seq:03d}` to format the SEQ. Keeps a full audit trail of every published snapshot on disk.

**Filename structure:**
- `PLAN` = register code (`PRR` master, `DDR`, `HSE`, ...)
- `YEAR` = snapshot year
- `SEQ` = 3-digit export sequence (`001`, `002`, ...)
- `REV` = register revision token (`C11`)
- `STATE` = `ACTIVE` for the live snapshot, or any other state for archive copies

### 4. Sub-register split (master + DMP chapters)

When one logical register (e.g. project risk) actually spans multiple DMP/management-plan chapters, split it into a master page + chapter sub-registers. They share the same HTML template, render the same JSON-driven webapp, and provide cross-navigation. The shipped pattern: PRR (master, 51 project risks, 18 categories) + DDR (design discipline, 79 risks) + HSE (HSE fit-out, 41 risks).

**Data file additions:** add two top-level boolean flags to each JSON so the page knows which register it is:

```json
{
  "project": "Aseer Regional Museum",
  "is_ddr": false,
  "is_hse": false,
  ...
}
```

| Register | `is_ddr` | `is_hse` | label shown |
|----------|----------|----------|-------------|
| Master PRR | `false` | `false` | "Master Risk Register (PRR)" |
| DDR | `true` | `false` | "Design Discipline Register (DDR)" |
| HSE | `false` | `true` | "HSE Risk Register (Fit-Out)" |

**Cross-navigation:** the JS that fills the header `registerNav` placeholder (see `references/sub-register-ui.md`) renders "Viewing: <register name> · <link to siblings> · <link to master>". The visible 3-card strip below the KPIs shows the split at a glance — the current register's card is `reg-current` (no link, navy border), the others are clickable.

For the full HTML / CSS / JS pattern (cards, header nav, mobile breakpoint), see `references/sub-register-ui.md`.

## Per-register scoring labels (dynamic P·S / P·I / C·L)

Each register type uses different column labels per RMP Section 6.5:

| Register | RMP Scale | Col Headers | Axis Y | Axis X |
|----------|-----------|-------------|--------|--------|
| PRR | 4x4 PxS | **P** · **S** | Probability | Impact / Severity |
| DDR | 5-pt impact | **P** · **I** | Probability | Impact |
| HSE | 5x5 CxL | **C** · **L** | Consequence | Likelihood |
| AVR | 4x4 PxS | **P** · **S** | Probability | Impact / Severity |

### Implementation in the shared template

The risk register template (`template.html`) is shared across all four registers. Add a `REG_LABELS` block before `const COLS` that reads `RISK.is_ddr` / `RISK.is_hse` flags from the JSON data:

```javascript
const REG_LABELS = (()=>{
  if (RISK.is_hse) return {p:'C', s:'L', pFull:'Consequence', sFull:'Likelihood', axisX:'Likelihood  to '};
  if (RISK.is_ddr) return {p:'P', s:'I', pFull:'Probability', sFull:'Impact', axisX:'Impact  to '};
  return {p:'P', s:'S', pFull:'Probability', sFull:'Severity', axisX:'Impact / Severity  to '};
})();
```

Then use `REG_LABELS` in all display locations:

1. **COLS array** — `{k:'probability', t:REG_LABELS.p}, {k:'severity', t:REG_LABELS.s}`
2. **Matrix tooltips** — `${REG_LABELS.p}${p} × ${REG_LABELS.s}${s}`
3. **Detail panel score** — `${REG_LABELS.p}${r.probability} × ${REG_LABELS.s}${r.severity}`
4. **Risk row detail** — `${REG_LABELS.p}${r.probability} × ${REG_LABELS.s}${r.severity}`

### Axis labels (static HTML → JS update)

Axis labels are in static HTML, not JS template strings. Add `id` attributes and set via `textContent` in `renderAll()`:

```html
<div class="axis-y" id="axisY">Probability  to </div>
<div class="axis-x" id="axisX">Impact / Severity  to </div>
```

```javascript
function renderAll(){
  const yEl = document.getElementById('axisY');
  const xEl = document.getElementById('axisX');
  if (yEl) yEl.textContent = REG_LABELS.pFull + '  to ';
  if (xEl) xEl.textContent = REG_LABELS.axisX;
  renderMatrix(); renderCatBars(); renderStatusBars(); renderOwnerBars();
  renderChips(); renderTable(); updateShowing(); syncActive();
}
```

### Injecting flags into JSON data

When building each register page, add the appropriate flag to the JSON before injecting into the template:

```python
# DDR
ddr_data['is_ddr'] = True
html = template.replace('__RISK_DATA__', json.dumps(ddr_data, indent=2, ensure_ascii=True))

# HSE
hse_data['is_hse'] = True
html = template.replace('__RISK_DATA__', json.dumps(hse_data, indent=2, ensure_ascii=True))

# PRR and AVR — no flag needed, defaults to P·S
```

### Excel snapshot column header

The Excel template's column H header must match the register type. Update `risk_snapshot_template.xlsx` before rebuilding:

```python
from openpyxl import load_workbook
w = load_workbook(template_path)
w['Risk Register'].cell(5, 8).value = 'I'  # DDR: I, HSE: L, PRR/AVR: S
w.save(template_path)
```

### Rebuilding static pages (DDR, HSE)

DDR and HSE are static HTML files (not rebuilt by `deploy.sh`). After updating the template, rebuild them from the updated template:

```python
import json, re
from pathlib import Path

template = Path('webapp/template.html').read_text()

# DDR
ddr = json.loads(Path('webapp/ddr/risks_ddr.json').read_text())
ddr['is_ddr'] = True
html = template.replace('__RISK_DATA__', json.dumps(ddr, indent=2, ensure_ascii=True))
Path('/tmp/ddr_rebuilt.html').write_text(html)

# HSE — fetch from live
import urllib.request, ssl
ctx = ssl._create_unverified_context()
h = urllib.request.urlopen('https://samaya-factory.com/aseer/registers/Risk/HSE/', context=ctx).read().decode('utf8','replace')
hse = json.loads(re.search(r'const RISK\s*=\s*(\{.*?\});', h, re.S).group(1))
hse['is_hse'] = True
html2 = template.replace('__RISK_DATA__', json.dumps(hse, indent=2, ensure_ascii=True))
Path('/tmp/hse_rebuilt.html').write_text(html2)
```

Then deploy both via rsync.

## Risk Register sheet column layout

The template is a user-formatted `.xlsx` at `webapp/templates/risk_snapshot_template.xlsx`. When the user reformats it (colors, column order, chart layout), **replace the template file** and update the build script column mapping to match. Do NOT try to programmatically reproduce the user's formatting.

The current layout (updated 2026-07-25 after user reformat):

**Risk Register sheet:**

| Col | Header | Content |
|-----|--------|---------|
| A | ID | Risk ID (merged A1:O1, A2:O2, A3:O3 for header) |
| B | CATEGORY | Category code |
| C | RISK | Risk title/event |
| D | CAUSE | Risk cause |
| E | EVENT | Event / trigger description |
| F | CONSEQUENCE | Risk consequence |
| G | P | Probability (user-entered) |
| H | I | Impact (user-entered) |
| I | SCORE | Formula: =G*H (calculated) |
| J | RATING | Rating value from JSON (string, not formula) |
| K | STATUS | Risk status |
| L | OWNER | Risk owner |
| M | TARGET CLOSE | Target close date |
| N | RESPONSE / MITIGATION | Mitigation/response text |
| O | EVIDENCE | Supporting evidence |

Header row is **row 5** (labels), data starts at **row 6**. Last data row = 5 + risk_count.
A, B, C, D, E, F (header info) merged across A1:O1, A2:O2, A3:O3. Footer merged at A(last):O(last).

**Dashboard formula references:**

| Section | Formula pattern | Column refs |
|---------|----------------|-------------|
| KPI cards (row 6) | COUNTA(A6:A{last}), COUNTIF(J6:J{last},"Critical"/"High"/"Medium"/"Low") | ID=A, RATING=J |
| KPI: Open count | COUNTIF(K6:K{last},"Open") | STATUS=K |
| Risk Matrix (row 12-15) | COUNTIFS(G6:G{last},P,H6:H{last},S) | P=G, S=H |
| By Rating (row 11-14 col I) | COUNTIF(J6:J{last},rating) | RATING=J |
| By Status (row 17-18 col I) | COUNTIF(K6:K{last},status) | STATUS=K |
| Top Owners (row 11-18 col L) | COUNTIF(L6:L{last},owner) | OWNER=L |
| Categories (row 20-36 col D) | COUNTIF(B6:B{last},code) | CAT=B |
| Bar chart data | Dashboard!$D$20:$D${last_cat} | Category counts |
| Bar chart categories | Dashboard!$B$20:$B${last_cat} | Category names |

When building, update ALL Dashboard formulas containing `'Risk Register'!$col$6:$col$` with the correct last row number using regex: `re.sub(r'(\$[A-Z]+\$6:\$[A-Z]+)\$\d+', lambda m: m.group(1)+'$'+str(last), v)`.

**Template replacement workflow:**
1. User opens the generated xlsx, reformats it (columns, colors, layout, removes/includes charts).
2. Save the user's version as the new template: `cp user_file.xlsx webapp/templates/risk_snapshot_template.xlsx`
3. Update the build script's `setv()` calls to write data to the NEW column positions.
4. Verify Dashboard formulas still resolve (the template's own formulas reference the columns as designed by the user — only the last-row number needs updating).
5. Rebuild all four registers.

Column widths are set by the template, not the build script — the template's column_dimensions are preserved when openpyxl `load_workbook`+`save` round-trips.

## Do NOT embed scoring in text fields

The RESPONSE / ACTION, EVIDENCE, and CAUSE fields must never contain text like `Risk Score: 8 (MEDIUM)` or `Risk Score: 12 (HIGH)`. All scoring appears only in the dedicated P, S, SCORE, and RATING columns. This is a common and easily introduced error — any script that writes `response_action` values must strip trailing scoring annotations.

## Dashboard formula update technique

When the template's Risk Register column layout changes, the Dashboard formulas (which reference Risk Register columns by letter) must be updated too. The template Dashboard already has formula-based sections — do not write static values over them. Only update the column references.

The key replacement technique:

```python
import re

# Replace old column reference in range: update the last row number
v=re.sub(r'(\$[A-Z]+\$6:\$[A-Z]+)\$\d+', lambda m: m.group(1)+'$'+str(last), v)
```

Dashboard column mapping for the current template (2026-07-25 user format):
- ID: A, CAT: B, RISK: C, CAUSE: D, EVENT: E, CONSEQ: F
- P: G, S: H, SCORE: I, RATING: J, STATUS: K, OWNER: L, TARGET: M, RESPONSE: N, EVIDENCE: O

## Never overwrite Dashboard cells with static values

The template Dashboard contains a hand-formatted layout with formulas, merged cells, borders, and colour coding. Do NOT write static count/owner/category data to the Dashboard sheet — that destroys the template layout. Only update the formula column references in existing cells. The build script should:

1. Copy the template (preserves all Dashboard formatting).
2. Update Dashboard formulas' last-row references to match the data count (regex on `\$6:\$[A-Z]+\$\d+` → new last row).
3. Write risk data to the Risk Register sheet starting at row 6 (row 5 has headers).
4. Save.

**Data sheet start row:** The current template has data starting at row 6. For N risks, the last data row = 5 + N. The template's footer/header merged cells (row 1-3, row ~last+2) must not be overwritten.

## Variable shadowing pitfall with openpyxl

When iterating over column widths, do NOT use `w` as the loop variable — it shadows the workbook object:

```python
# WRONG: w is overwritten by integer width values
widths={'A':12,'B':8,'C':45}
for col_letter,w in widths.items():  # w is now an int!
    rr.column_dimensions[col_letter].width=w
# w.save(OUT/filename)  # ERROR: 'int' object has no attribute 'save'

# RIGHT: use a different variable name
for col_letter,wd in widths.items():
    rr.column_dimensions[col_letter].width=wd
```

## Formula-driven Excel dashboards and live-register QR

The Dashboard must not contain fixed numeric snapshot values only. Build KPI, matrix, rating, status, owner, and category cells as formulas referencing the `Risk Register` sheet. Use absolute ranges covering the generated register rows, for example:

```python
id_rng = "'Risk Register'!$A$6:$A$52"
rating_rng = "'Risk Register'!$J$6:$J$52"
status_rng = "'Risk Register'!$K$6:$K$52"
p_rng = "'Risk Register'!$G$6:$G$52"
s_rng = "'Risk Register'!$H$6:$H$52"
ws["B6"] = f'=COUNTA({id_rng})'
ws["D6"] = f'=COUNTIF({rating_rng},"Critical")'
ws["C12"] = f'=COUNTIFS({p_rng},4,{s_rng},1)'
```

However, the preferred approach is to let the **template** contain pre-made formulas and only update the last-row numbers via regex. This preserves all formatting and merged cells from the user's template.

Add the canonical live-register URL to the Dashboard as a clickable Excel hyperlink and embed a QR image pointing to the same URL. Generate the QR during the build with the `qrcode` Python package and `openpyxl.drawing.image.Image`; include both the logo and QR in the workbook. Verify after generation by loading the workbook with `data_only=False`, checking KPI cells begin with `=`, checking the hyperlink target, and checking the dashboard image count.

Use the URL by register type:

- PRR: `https://samaya-factory.com/aseer/registers/Risk/`
- DDR: `https://samaya-factory.com/aseer/registers/Risk/DDR/`
- HSE: `https://samaya-factory.com/aseer/registers/Risk/HSE/`
- AV: `https://samaya-factory.com/aseer/registers/Risk/AV/`

## Created-date and project-status audit

Before publishing a revised register, audit every risk against the project timeline and current status. For each risk check:

1. `created` exists and falls between NTP and the current review date.
2. The date reflects when the exposure first emerged, not when the row was later entered into the register. Use dated MoM, CG comments, Code C/D responses, procurement events, and design gates as evidence.
3. `target_close` is present for every Open or Watch risk.
4. `target_close` is not before `created`.
5. Past target dates are either extended to a justified current action date or the risk status is updated with evidence. Do not silently leave Open risks overdue.
6. Status is consistent with the latest project activity: Closed and Mitigated require evidence or a history entry.
7. Owner and category match the risk's actual control path.

Do not claim that DDR or HSE creation dates have been audited if their source records do not contain `created` and `target_close` fields. Report those fields as unavailable and request a source-data update.

## Download-link verification and stale filenames

After every build and deployment, extract the actual `.xlsx` href from each live page and request that exact URL. Do not assume the filename from the page title or from a previous build. If a DDR/HSE page points to a missing PRR filename, list the server directory to identify the actual register-specific workbook, then patch the page to use the actual file:

- DDR filename must use `EXP-RISK-DDR-...xlsx`.
- HSE filename must use `EXP-RISK-HSE-...xlsx`.
- PRR filename must use `EXP-RISK-PRR-...xlsx`.
- AV filename must use `EXP-RISK-AV-...xlsx`.

Verify all four URLs return HTTP 200 with the OpenXML spreadsheet MIME type. Protect sibling subdirectories from master `rsync --delete`.

## Deploy verification (always run these five checks)

```bash
# 0. Verify HTML file structure before deploying (prevents site-breaking uploads)
head -c 20 "$LOCAL_FILE"  # must show: <!DOCTYPE html>
tail -c 20 "$LOCAL_FILE"  # must show: </html>

# 0a. Verify JSON modification did not strip HTML
python3 -c "
with open('$LOCAL_FILE') as f:
    c = f.read()
assert c.startswith('<!DOCTYPE html>'), 'Missing DOCTYPE — JSON replacement destroyed the HTML!'
assert c.endswith('</html>'), 'Missing closing HTML — file was truncated!'
print('File OK:', len(c), 'bytes')
"

# 1. Main page returns 200 and references the new xlsx
curl -s https://samaya-factory.com/aseer/registers/Risk/ \
  | grep -oE 'EXP-RISK-PRR-[0-9-]+_[A-Za-z0-9_]+\\.xlsx' | head -1

# 2. The new xlsx returns 200
curl -sI "https://samaya-factory.com/aseer/registers/Risk/EXP-RISK-PRR-2026-004_RevC11_ACTIVE.xlsx" \
  | head -1

# 3. Every sub-register still alive (must NOT have been wiped by --delete)
for sub in DDR HSE; do
  curl -s -o /dev/null -w "$sub %{http_code}\n" "https://samaya-factory.com/aseer/registers/Risk/$sub/"
done

# 4. The cross-nav line is present in the rendered page
curl -s https://samaya-factory.com/aseer/registers/Risk/ | grep -c 'registerNav\\|reg-card'
```

A passing run prints the latest EXP-RISK filename, `200` for the xlsx, `200` for each sub-register, and a non-zero count for the nav markers.

## Hostinger multi-path deploy verification (CRITICAL — do not skip)

The `.htaccess` on Hostinger rewrites ALL requests to `/build/`:

```
RewriteEngine on
RewriteCond %{HTTP_HOST} ^samaya-factory.com$ [NC,OR]
RewriteCond %{HTTP_HOST} ^://samaya-factory.com$ [NC]
RewriteCond %{REQUEST_URI} !^/build/
RewriteRule ^(.*)$ /build/$1 [L]
```

This means two server paths serve the risk register:
- `/build/aseer/registers/Risk/index.html` (primary)
- `/build/technical-office/aseer/registers/Risk/index.html` (mirror — updated by git post-commit hook)

**After every deploy, verify MD5 across ALL paths.** The git hook may overwrite your SCP:

```bash
MD5_LOCAL=$(md5 -q "$LOCAL_FILE")
for REMOTE_PATH in \
  "/home/u517606786/domains/samaya-factory.com/public_html/build/aseer/registers/Risk/index.html" \
  "/home/u517606786/domains/samaya-factory.com/public_html/build/technical-office/aseer/registers/Risk/index.html"; do
  MD5_REMOTE=$(ssh -p 65002 u517606786@samaya-factory.com "md5sum '$REMOTE_PATH'" 2>&1 | awk '{print $1}')
  echo "$([ \"$MD5_LOCAL\" = \"$MD5_REMOTE\" ] && echo MATCH || echo MISMATCH): $REMOTE_PATH"
done
```

**If mismatch persists:** the git post-commit hook is overwriting the file. Disable temporarily:
```bash
ssh -p 65002 u517606786@samaya-factory.com \
  "chmod -x /home/u517606786/domains/samaya-factory.com/public_html/build/.git/hooks/post-commit 2>/dev/null"
```
Re-deploy, then re-enable after confirming stable.

**LiteSpeed cache persists despite no-cache headers.** Even with `cache-control: no-cache, no-store, must-revalidate`, LiteSpeed may serve stale HTML. Force fresh serve:
1. Add query param: `curl -s 'https://.../Risk/?v=$(date +%s)'`
2. Purge: `rm -rf /tmp/lshttpd/* && /usr/local/lsws/bin/lshttpd -s restart`
3. Verify content has your fix with unique param

For the full toolbar standard (all four registers must match), see `references/toolbar-standardization.md`.

## Pitfalls

- **Local file may be stale** — the HTML source at `~/aseer-museum-pm/06_Risk_System/webapp/src/` is NOT the authoritative data source. The server often has newer risks added or edited directly. Before editing the local copy, always compare risk counts. If the server has more risks, download from server first and edit that.
- **Git restore overwrites server customizations** — the live server may have toolbar buttons, register nav links, CSS tweaks, or button handlers that the git repo doesn't have. These were added directly to the server file. Before restoring from git: download the server version, compare features, and re-add any missing customizations after restore. The safe JSON fix procedure: extract RISK JSON from server HTML, modify via json.loads/dumps, slice-replace only the JSON portion (using m.start(2)/m.end(2)), verify `<!DOCTYPE html>` + `</html>` still bookend the file.
- **Sub-registers missing CSV/Print buttons** — older DDR/HSE/AVR pages built from an earlier template may lack `exportCSV()` function and `btnPrint` bindings. Fix: copy `exportCSV()` from PRR (register-agnostic, reads from RISK global), add `btnCsv.onclick = exportCSV; btnPrint.onclick = ()=>window.print();` to init(). After adding, verify all four toolbar buttons (Reset, Snapshot, CSV, Print) work on every register.
- **Fixes must replicate to ALL sibling pages** — after fixing one register page (e.g. PRR), always check the other three (DDR, HSE, AVR) for the same issue. User catches discrepancies across registers. Common gaps: missing CSV/Print buttons, registerNav in wrong location (htitle vs hright), duplicate registerNav elements, missing register cards section.
- **PRR risk ID convention** — PRR uses `PRR-{RBS_CATEGORY}-{NN}` with 2-digit sequential (01-99). Non-standard codes like `SMP` (not an RBS category) or 3-digit padding (`001`) must be renumbered. Check `rbs_categories` dict for valid codes. Action IDs inside risks should match the project-wide format (`A1`, `A2`) not risk-specific (`SMP-001-A1`).
- **OneDrive-stale xlsx → 404**: if deploy.sh does `cp "$ONE_DRIVE_PATH" src/` and OneDrive is sync-disabled, the xlsx will be 0 bytes or missing. Symptom: EXCEL button 404, page itself loads fine. Fix: generate the xlsx from JSON (lesson 1).
- **`rsync --delete` wipes siblings**: the most destructive silent failure. Symptom: sub-register pages start 404'ing right after a master deploy. Fix: `--exclude='DDR/' --exclude='HSE/'` (lesson 2).
- **Hardcoded xlsx filename in template**: the template used to have `Aseer_Museum_Risk_Register_C11_2026-07-19.xlsx` baked in. Any filename change requires a template rebuild. The current approach uses `__XLSX_FILE__` in the template (reused for both href and download), then overrides the `download` attribute with a regex post-processing step.

  **Download filename split:** The `href` points to the server filename (`EXP-RISK-PRR-2026-040_RevC12_ACTIVE.xlsx`). The `download` attribute should be user-friendly: `Aseer_Regional_Museum_PRR_2026-07-26_1324.xlsx`.

  **Standard naming convention (all 4 registers):**

  | Register | Download name pattern | Example |
  |----------|----------------------|---------|
  | PRR | `Aseer_Regional_Museum_PRR_{date}_{time}.xlsx` | `Aseer_Regional_Museum_PRR_2026-07-26_1324.xlsx` |
  | DDR | `Aseer_Regional_Museum_DDR_{date}_{time}.xlsx` | `Aseer_Regional_Museum_DDR_2026-07-24_1324.xlsx` |
  | HSE | `Aseer_Regional_Museum_HSE_{date}_{time}.xlsx` | `Aseer_Regional_Museum_HSE_2026-07-19_1324.xlsx` |
  | AVR | `Aseer_Regional_Museum_AVR_{date}_{time}.xlsx` | `Aseer_Regional_Museum_AVR_2026-07-25_1325.xlsx` |

  **Implementation (add to each build script after the main template replacements):**
  ```python
  from datetime import datetime
  snap_date = str(data.get("last_updated", "") or "")
  snap_time = datetime.now().strftime("%H%M")
  download_name = f"Aseer_Regional_Museum_{REG_CODE}_{snap_date}_{snap_time}.xlsx"
  import re as _re
  html = _re.sub(r'download="[^"]+\.xlsx"', f'download="{download_name}"', html)
  ```

  The date comes from `data["last_updated"]` (data currency date), not `datetime.now()`, because the register may have been last updated days ago. The time comes from `datetime.now()` (generation time). This gives `YYYY-MM-DD_HHMM` format.

  For sub-registers that derive from the master page (like AVR from PRR), replace both `href` and `download` attributes using regex on the already-built master HTML:
  ```python
  # Find the existing href/download values from the master page
  m = re.search(r'href="([^"]*\.xlsx)"', html)
  m2 = re.search(r'download="([^"]*\.xlsx)"', html)
  if m and m2:
      html = html.replace(m.group(1), xlsx_name)      # swap server filename
      html = html.replace(m2.group(1), download_name)  # swap download name
  ```
- **Legacy xlsx not cleaned up**: the old `Aseer_Museum_Risk_Register_*.xlsx` files in `src/` will keep getting shipped if not deleted on rebuild. Add `for old in OUT_DIR.glob("Aseer_Museum_Risk_Register_*.xlsx"): old.unlink()` in the build script so the legacy name is dropped.
- **Permissions 640/700 on web server → 404**: The server's web user must have world-read on Excel files. Two common causes: (1) OneDrive-copied files arrive with `0640` perms — LiteSpeed returns 403/404. (2) openpyxl `save()` on macOS creates files with `-rwx------` (700) — rsync `-az` preserves these. PRR/AV were always fine because deploy.sh's build scripts call `os.chmod(xlsx_path, 0o644)`. **Always** `os.chmod(path, 0o644)` after writing any xlsx, whether from the build script or after an `rsync` deploy on the server.
- **LiteSpeed cache hides the fix**: see `register-webapp-template` section 8b for the standard `.htaccess` + meta-tag cache-busting. Always add `?v=$(date +%s)` to the URL you curl in the verification step.
- **`rbs_categories` must be a dict, not a list**: `build_xlsx._dashboard()` expects `data["rbs_categories"]` to be a `{code: name}` dict (e.g. `{"AV": "AV & Multimedia", "HW": "Hardware & long-lead"}`). If you pass a list of `{code, name}` objects, the xlsx build crashes with `AttributeError: 'list' object has no attribute 'get'`. Always check the format in the master `risks.json` before writing a sub-register's JSON.
- NEVER regex-patch a deployed page to add/remove cards: regex-based banner replacement is fragile and can eat adjacent sections. Always rebuild from the master template.
- **Regex-based JSON data replacement destroys the file**: A regex like `(const DATA = )({.*?})(;\s*$)` captures only up to `;` at end of line. On a minified single-line JSON (all register SPAs), writing back `prefix + new_json + suffix` **loses all HTML/CSS/JS** before and after that line — the page becomes bare JSON. Always use JSON-level manipulation: parse with `json.loads()`, modify the dict, re-stringify with `json.dumps(ensure_ascii=False, separators=(',',':'))`, then slice-replace ONLY the JSON portion in the original HTML string using `m.start(2)` / `m.end(2)` boundaries. Verify the result starts with `<!DOCTYPE html>` and ends with `</html>` before deploying.
- Use string slicing, not regex, for banner replacement in build scripts

## Companion skills

- `register-webapp-template` — the HTML/JS template, the KPI/matrix/table rendering, the print sheet, the A4 PDF button. The visual layer that this skill deploys.
- `submittal-register-management` — the analogous flow for submittal registers (markdown source → JSON → Excel + webapp).
- `project-risk-register` — building the actual risks (RBS taxonomy, heat map, evidence-based register content). This skill only handles the deploy/webapp side.

## Cross-register duplication detection

When a master register (PRR) is split into DMP-chapter sub-registers (DDR, HSE, AV), risks can end up in both. This happens when:
- A risk is carried from PRR into a sub-register during creation (e.g. PRR-AV-01/02 copied into AV but never removed from PRR).
- The same event is logged independently in two registers (e.g. PRR-DES-05 and DDR-DES-005 — same MoC object-list redesign risk).

### Detection method

```python
# Load all registers
prr_ids = {r['id'] for r in prr['risks']}
ddr_ids = {r['id'] for r in ddr['risks']}
hse_ids = {r['id'] for r in hse['risks']}
av_ids  = {r['id'] for r in av['risks']}

# 1. Exact ID match — same risk ID in two registers
for name1, ids1 in [('PRR',prr_ids), ('DDR',ddr_ids), ('HSE',hse_ids), ('AV',av_ids)]:
    for name2, ids2 in [('PRR',prr_ids), ('DDR',ddr_ids), ('HSE',hse_ids), ('AV',av_ids)]:
        if name1 < name2:
            overlap = ids1 & ids2
            if overlap:
                print(f"DUPLICATE ID: {overlap} in {name1} AND {name2}")

# 2. Title similarity — same event, different ID
def words(s):
    return set(w.lower() for w in re.findall(r'\b[a-z]{4,}\b', s.lower()))

for (reg1, id1, t1), (reg2, id2, t2) in combinations(all_risks, 2):
    w1, w2 = words(t1), words(t2)
    common = w1 & w2
    if len(common) >= 4 and len(common)/max(len(w1),len(w2)) > 0.4:
        print(f"SIMILAR: {reg1}/{id1} <-> {reg2}/{id2} — {t1[:80]}")
```

### Resolution

- **Exact ID match**: the sub-register is the canonical home. Remove from PRR. The sub-register has better action plans and domain-specific context.
- **Title similarity**: check if they describe the same event/cause/consequence. If yes, keep the one in the register that owns that domain (e.g. DDR for design risks, HSE for HSE risks). Add a cross-reference note to the PRR version's history before removing.
- **Never keep the same risk in two registers** — it creates confusion about which is the source of truth, and updates to one won't propagate to the other.

### Prevention

When creating a new sub-register, explicitly decide which risks move out of PRR and which stay. The PRR should hold only risks that don't belong to any DMP chapter — cross-cutting project risks (schedule, commercial, stakeholder). Chapter-specific risks (design, HSE, AV) live in their sub-register only.
