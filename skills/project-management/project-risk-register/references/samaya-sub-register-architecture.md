# Samaya Sub-Register Architecture (PRR · DDR · HSE · AVR)

> Use when a single project holds multiple live risk registers (master + per-discipline sub-registers) on the same web page family. Covers the cross-nav banner, naming convention, SEQ auto-increment, and rsync pattern that lets the master and N sub-registers coexist on the same server without `--delete` wiping each other.

## When You Need This

The user runs a project with more than one live risk register on the same web app family. On Aseer Museum the family is `samaya-factory.com/aseer/registers/Risk/` with:

| Folder | Code | Scope | Risks (C11) | RBS |
|---|---|---|---|---|
| `/` | PRR (master) | Cross-discipline project risks | 51 | 18 categories (PRC, COM, DES, CON, …) |
| `/DDR/` | DDR | Design discipline risks | 79 | 6 categories (TEC, SCH, EXT, PRO, QA, COM) |
| `/HSE/` | HSE | HSE / fit-out risks | 41 | 1 category (HSE), status `Ongoing` |
| `/AVR/` (or `/AV/`) | AVR | AV & multimedia risks | 12 | 7 categories (AV, IFC, HW, MEP, STR, LGT, OPS) |

Each sub-register has its own scoring scale, its own categories, and its own xlsx exports. The user wants one click between any two.

## Naming Convention for xlsx Exports

`EXP-RISK-{PLAN}-{YEAR}-{SEQ}_RevC{REV}_{STATE}.xlsx`

| Token | Meaning | Aseer examples |
|---|---|---|
| `EXP-RISK-` | Literal prefix | — |
| `{PLAN}` | 3-letter register code | `PRR`, `DDR`, `HSE`, `AVR` |
| `{YEAR}` | Snapshot year | `2026` |
| `{SEQ}` | 3-digit sequence, never overwritten | `001`, `002`, `003` |
| `RevC{REV}` | Revision token without "Rev" prefix | `RevC11` |
| `{STATE}` | Always `ACTIVE` for live snapshots | `ACTIVE` |

### SEQ auto-increment

Every new build must never overwrite a prior export. Scan `src/` (or the live server) for `EXP-RISK-{PLAN}-{YEAR}-(\d{3})_*.xlsx` and use `max(seen)+1` for the new build. This keeps a full history on disk; each `DEPLOY-*.md` note can cite the SEQ it shipped.

```python
def _next_seq(out_dir, plan, year):
    pat = re.compile(rf"^EXP-RISK-{plan}-{year}-(\d{{3}})_.*\.xlsx$")
    return max((int(m.group(1)) for p in out_dir.iterdir()
                for m in [pat.match(p.name)] if m), default=0) + 1
```

## Cross-Register Nav Banner

Every page in the family must show a banner of N cards (one per register in the family), with the current register marked `current` and the rest as clickable links. Two parts:

### A. The banner block (static HTML, lives in the master template)

```html
<div class="registers" id="registers">
  <div class="reg-card reg-current">
    <div class="reg-head"><span class="reg-badge">current</span><span class="reg-code">PRR</span></div>
    <div class="reg-title">Master Risk Register</div>
    <div class="reg-sub">PRR — <span class="reg-doc">ASR-SAM-RMP-001</span> · Rev C11</div>
    <div class="reg-stats" id="regStats"></div>
    <div class="reg-foot">51 risks · 18 categories · you are here</div>
  </div>
  <a class="reg-card" href="DDR/">
    <div class="reg-head"><span class="reg-code">DDR</span></div>
    <div class="reg-title">Design Discipline Register</div>
    <div class="reg-sub">DDR — <span class="reg-doc">ASR-SAM-DDR-001</span> · Rev C11</div>
    <div class="reg-stats">79 risks · 1 Critical · 22 High · 28 Medium · 28 Low · all Open</div>
    <div class="reg-foot">Open sub-register →</div>
  </a>
  <a class="reg-card" href="HSE/">…</a>
  <a class="reg-card" href="AV/">…</a>
</div>
```

- `reg-current` = the current page's card; non-clickable, navy outline
- sibling cards are `<a href="…">` so the browser gives them hand-cursor
- static `reg-stats` is a deliberate snapshot — for the *current* card the JS fills it live; for siblings, hard-code the count so the banner survives even if a sibling JSON payload is broken

### B. The CSS — responsive grid

```css
.registers { display: grid; grid-template-columns: repeat(4, 1fr); gap: 12px; margin-bottom: 18px; }
.reg-card { background: #fff; border: 1px solid var(--border); border-radius: 12px; padding: 14px 16px; text-decoration: none; color: var(--ink); display: block; }
.reg-card.reg-current { background: linear-gradient(180deg, #f8fafc 0%, #fff 100%); border-color: var(--navy); box-shadow: inset 0 0 0 1px var(--navy); cursor: default; }
a.reg-card:hover { transform: translateY(-1px); box-shadow: 0 6px 18px rgba(15,23,42,.08); border-color: var(--navy); }
.reg-head { display: flex; align-items: center; gap: 8px; margin-bottom: 6px; }
.reg-badge { display: inline-block; background: var(--navy); color: #fff; font-size: 9.5px; font-weight: 700; letter-spacing: .08em; text-transform: uppercase; padding: 2px 7px; border-radius: 999px; }
.reg-code { font-family: 'IBM Plex Mono', monospace; font-weight: 700; font-size: 12px; color: var(--muted); }
.reg-title { font-size: 15px; font-weight: 700; color: var(--navy); margin-bottom: 2px; }
.reg-doc { font-family: 'IBM Plex Mono', monospace; }
.reg-foot { font-size: 11px; color: var(--accent); font-weight: 600; }
a.reg-card .reg-foot { color: var(--navy); }

@media (max-width: 1180px) { .registers { grid-template-columns: repeat(2, 1fr); } }
@media (max-width: 1080px) { .registers { grid-template-columns: 1fr; } }
```

### C. The JS — sibling nav line in the header (small text)

```js
const regName = RISK.is_ddr ? 'Design Discipline Register (DDR)'
              : RISK.is_hse ? 'HSE Risk Register (Fit-Out)'
              : RISK.is_av  ? 'AV & Multimedia Register (AVR)'
                            : 'Master Risk Register (PRR)';
const siblings = [];
if (!RISK.is_ddr) siblings.push({url: 'DDR/', label: 'Design (DDR)'});
if (!RISK.is_hse) siblings.push({url: 'HSE/', label: 'HSE'});
if (!RISK.is_av)  siblings.push({url: 'AV/',  label: 'AV'});
if (RISK.is_ddr || RISK.is_hse || RISK.is_av) siblings.push({url: '../', label: 'Master (PRR)'});
const links = siblings.map(s => `<a href="${esc(s.url)}">${esc(s.label)}</a>`).join(' · ');
$('#registerNav').innerHTML = `Viewing: <b>${esc(regName)}</b> · ${links}`;
```

The pattern is: every page reads its own `RISK.is_ddr/is_hse/is_av` flags, suppresses itself from the sibling list, and adds a "back to master" link only if it *is* a sub-register. Add the flag at the top of the corresponding `risks_*.json`:

```json
"is_ddr": false,
"is_hse": false,
"is_av":  false
```

## deploy.sh — rsync --delete with sibling protection

The master deploy pushes `./src/` to `${TARGET_DIR}/`. If a sibling subfolder (`DDR/`, `HSE/`, `AV/`) lives in `${TARGET_DIR}/` on the server but NOT in `./src/`, the default `--delete` will **wipe the sibling**. Two patterns that fix it:

```bash
# Option 1: exclude the sub-folders explicitly on the master rsync
rsync -avz --delete \
  --exclude='DDR/' --exclude='HSE/' --exclude='AV/' \
  -e "ssh -p ${PORT}" \
  ./src/ "${USER}@${HOST}:${TARGET_DIR}/"

# Then push the AV/ sub-register from its own src/ tree in a second rsync
rsync -avz --delete \
  -e "ssh -p ${PORT}" \
  ./av/src/ "${USER}@${HOST}:${TARGET_DIR}/AV/"
```

```bash
# Option 2: protect with rsync filter rules (one rule per sibling)
rsync -avz --delete \
  --filter='P /DDR/' --filter='P /HSE/' --filter='P /AV/' \
  -e "ssh -p ${PORT}" \
  ./src/ "${USER}@${HOST}:${TARGET_DIR}/"
```

Pick one and stick with it; mixing `--exclude` and `--filter` is confusing.

### Belt-and-braces: pre-create sibling .htaccess

If a sibling subfolder exists on the server but lacks `.htaccess` (e.g. it was created by a different pipeline), the master deploy won't fix it. Add a pre-flight ssh that creates each sibling folder + writes `.htaccess` if missing:

```bash
ssh -p "${PORT}" "${USER}@${HOST}" \
  "mkdir -p ${TARGET_DIR} && \
   for d in DDR HSE AV; do \
     [ -d ${TARGET_DIR}/\$d ] || mkdir -p ${TARGET_DIR}/\$d; \
     printf 'AddType application/vnd.openxmlformats-officedocument.spreadsheetml.sheet .xlsx\nAddType text/csv .csv\n<IfModule mod_headers.c>\n  Header set Cache-Control no-cache, no-store, must-revalidate\n  Header set Pragma no-cache\n  Header set Expires 0\n</IfModule>\n<IfModule LiteSpeed>\n  CacheDisable public /\n</IfModule>\n' > ${TARGET_DIR}/\$d/.htaccess; \
   done"
```

## When a Sub-Register Is Built Externally (in-place patch)

Often the DDR/HSE/AVR pages are deployed by a *different* pipeline (e.g. the user's external scripts) and live on the server as a black box. You need to add the cross-nav to those pages **without rebuilding them from source**. The pattern:

1. **Fetch** the deployed `index.html` via `scp get` into `/tmp/`
2. **Patch** by inserting:
   - a `<style>` block before `</style>` (CSS for `.registers` / `.reg-card`)
   - a `<div class="registers">` block after `<div class="kpis" id="kpis"></div>`
   - a `renderRegisterStats()` function before `renderKPIs()`
   - a call to it from `init()`
3. **Update the siblings JS** so the current register is suppressed and "back to master" is added
4. **Upload** via `scp put`
5. **Idempotency**: the patch script must check whether the banner is already there before patching, so re-runs are no-ops. Check by counting `class="registers"` AND `href="../AV/"` AND `AVR` — all three must be present for "already patched" to be true.

This is `references/...` not a script because the patch target changes per project — but the shape (4 inserts, 1 idempotency check, 1 upload) is fixed.

## Reusable Pitfalls (this architecture)

- **Sibling subfolders get wiped by `rsync --delete`** — see the deploy.sh pattern above. Always add the new sibling to BOTH the `--exclude` list AND the pre-flight `mkdir -p` loop.
- **JSON flags default to undefined for the master payload** — if `RISK.is_av` is `undefined` (falsy), the JS `if (!RISK.is_av)` evaluates to `true` and the AV link is shown. So a sub-register that doesn't have the flag still gets a working sibling link. But the master must explicitly set `"is_av": false` so future readers see the intent — never omit.
- **The first SEQ is 001, not 000** — `max(seen) + 1` from an empty `src/` returns 0+1 = 1. Always confirm with `ls src/ | grep -c 'EXP-RISK-...'` after the first build.
- **Hard-coded sibling stats must match reality** — when the banner says "41 risks · 30 Critical · 11 High · all Ongoing" and the actual HSE register has 41/30/11/Ongoing, fine. When the live register changes, the banner goes stale. Audit the static stats quarterly or pull them from a shared `index.json` if the number of registers grows beyond 4.
- **Banner card grid is 4-up on desktop, 2-up on tablet, 1-up on mobile** — the responsive breakpoints are mandatory; 4 cards at 1080px wraps badly without the 1180px 2-up breakpoint.
- **Use `repeat(4, minmax(0, 1fr))` not `repeat(4, 1fr)`** — without `minmax(0, 1fr)` plus `min-width: 0` on the cards, long content (a wide doc-ref like `ASR-SAM-AVR-001` plus a stats line) overflows the cell and pushes other cards off the row. Always set `.reg-card { min-width: 0; }` and `.registers { grid-template-columns: repeat(4, minmax(0, 1fr)); }` together.
- **Empty table + console `TypeError: Cannot set properties of null` on a sub-register = missing `<div class="matrix" id="matrix">`** — the analytics section (Risk Matrix + Category/Status/Owner bars) is JS-rendered into static placeholders. If the placeholders are missing, `renderMatrix()` throws on `$('#matrix').innerHTML = ...`, `renderAll()` aborts, and `renderTable()` never runs. The user sees the banner and KPIs but a blank table. Quick diagnostic: `curl -s https://.../ | grep -c 'id="matrix"'` — must be 1. Live test in browser console: `document.getElementById('tbody').innerHTML.length` after page load — 0 means matrix broke.
- **Banner-replacement regex MUST use a lookahead on the NEXT section, not a count of closing `</div>`** — the working pattern is `(<div class="registers" id="registers">.*?</div>\s*</div>)(?=\s*<div class="(?:analytics|toolbar)">)`. The naive `.*?</div>\s*</div>\s*</div>\s*</div>` matches 4 consecutive closing divs and is too greedy — it eats the matrix div and any sibling section that happens to have enough inner divs. The lookahead anchors the match on the next section's opening tag, which never lies. Always accept either `<div class="analytics">` OR `<div class="toolbar">` as the terminator (analytics can be missing from a previously-broken page).
- **Idempotency check needs ALL THREE markers** — checking only `class="registers"` returns "already patched" after the first run, but the page can still be broken (analytics eaten, no AV link). A correct idempotency test: `if 'class="registers"' in html and 'href="../AV/"' in html and 'AVR' in html:`. All three must be present.
- **The in-place patch should RESTORE the analytics section if missing** — when a previous patch ate the analytics, the next patch needs to insert it back. Embed a known-good copy of the analytics block (Risk Matrix card + Exposure by Category card + By status / Top owners grid, ~1.2 KB) and insert it between the banner's closing `</div>` and `<div class="toolbar">`. This is the recovery path when patches go wrong.
- **`build_xlsx.build()` requires `rbs_categories` to be a DICT (code → name), not a list of `{code, name}` objects.** The web renderer (`renderSelects`) works with either. If `build_xlsx._dashboard` errors with `'list' object has no attribute 'get'`, change `rbs_categories` to a flat dict.
- **`scrub_for_client()` is web-only** — it strips `treatment_file`, `history[].by`, `merge_note`. `build_xlsx.build()` expects the **un-scrubbed** data (it has its own internal handling). Order matters in the build script: call `scrub_for_client()` only when injecting the JSON payload, NOT when calling `build_xlsx.build()`.

## Pre-Build Sanity Checks (run before AND after every sub-register deploy)

If any check fails, **do not** consider the deploy done. Re-runs of `bash deploy.sh` are cheap; broken pages are not.

```bash
# 1. Local: structural completeness
for f in webapp/src/index.html webapp/av/src/index.html; do
  echo "=== $f ==="
  echo "  banner cards: $(grep -c 'class="reg-card' $f)  (expect 4)"
  echo "  matrix div:   $(grep -c 'id="matrix"' $f)     (CRITICAL: must be 1, else renderAll throws)"
  echo "  tbody div:    $(grep -c 'id="tbody"' $f)      (expect 1)"
  echo "  analytics:    $(grep -c 'class="analytics"' $f) (expect 1)"
  echo "  AV link:      $(grep -c 'href=\".\\.\\./AV/\"' $f) (expect 1)"
done

# 2. Live: HTTP 200 + payload intact
for path in /aseer/registers/Risk/ /aseer/registers/Risk/DDR/ /aseer/registers/Risk/HSE/ /aseer/registers/Risk/AV/; do
  printf "%-45s " "$path"
  curl -sI "https://samaya-factory.com$path" | head -1
done

# 3. xlsx link returns 200 for each register's most recent export
curl -sI "https://samaya-factory.com/aseer/registers/Risk/AV/$(curl -s https://samaya-factory.com/aseer/registers/Risk/AV/ | grep -oE 'EXP-RISK-AV-[0-9-]+_RevC[0-9]+_ACTIVE\.xlsx' | head -1)" | head -1
```

If `id="matrix"` is missing from the built HTML, the build script's banner-replacement regex is too greedy — fix the regex (see the lookahead pitfall above) and rebuild.
