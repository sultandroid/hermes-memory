# Sub-Register UI Pattern — HTML / CSS / JS

Drop-in pattern for adding a **master + DMP-chapter sub-register** split to any register webapp built from the Samaya template. Two layers of cross-navigation: a header line (always visible, all pages) and a 4-card strip below the KPIs (visible, scannable). The shipped reference is https://samaya-factory.com/aseer/registers/Risk/ (master PRR + DDR + HSE + AV).

## Data flags

Add to the JSON data file at the top level:

```json
{
  "project": "Aseer Regional Museum",
  "is_ddr": false,
  "is_hse": false,
  "is_av": false
}
```

| Register | `is_ddr` | `is_hse` | `is_av` | label shown |
|----------|----------|----------|---------|-------------|
| Master PRR | `false` | `false` | `false` | "Master Risk Register (PRR)" |
| DDR | `true` | `false` | `false` | "Design Discipline Register (DDR)" |
| HSE | `false` | `true` | `false` | "HSE Risk Register (Fit-Out)" |
| AV | `false` | `false` | `true` | "AV & Multimedia Register (AVR)" |

## Layer 1 — Header line

### HTML placeholder (add under `brandSub`)

```html
<div class="dcline" id="brandSub"></div>
<div class="dcline"><span id="registerNav"></span></div>
```

### JS (replaces the existing `renderFooter` brandSub line)

```javascript
function renderFooter(){
  $('#brandSub').innerHTML = `Contract <b>${esc(RISK.contract||'')}</b> · Doc <b>${esc(RISK.doc_ref||'')}</b> · Rev <b>${esc(RISK.revision||'')}</b> · Updated <b>${esc(RISK.last_updated||'')}</b>`;

  // Register-switch nav. Show on every page so users can hop between registers.
  const regName = RISK.is_ddr ? 'Design Discipline Register (DDR)'
                  : RISK.is_hse ? 'HSE Risk Register (Fit-Out)'
                  : RISK.is_av ? 'AV & Multimedia Register (AVR)'
                  : 'Master Risk Register (PRR)';
  const siblings = [];
  if (!RISK.is_ddr) siblings.push({url: 'DDR/', label: 'Design (DDR)'});
  if (!RISK.is_hse) siblings.push({url: 'HSE/', label: 'HSE'});
  if (!RISK.is_av)  siblings.push({url: 'AV/',  label: 'AV'});
  if (RISK.is_ddr || RISK.is_hse || RISK.is_av) siblings.push({url: '../', label: 'Master (PRR)'});
  const links = siblings.map(s => `<a href="${esc(s.url)}">${esc(s.label)}</a>`).join(' · ');
  $('#registerNav').innerHTML = `Viewing: <b>${esc(regName)}</b> · ${links}`;

  $('#foot').innerHTML = `
    <div class="dc">${esc(RISK.doc_ref||'')} · Rev ${esc(RISK.revision||'')} · ${esc(RISK.contract||'')} · ${esc(RISK.last_updated||'')}</div>
    <div><b>${esc(RISK.project||'')}</b> — Risk Register. Scoring: Probability (1–4) × Impact (1–4); bands Critical ≥ ${BANDS.critical}, High ${BANDS.high}–${BANDS.critical-1}, Medium ${BANDS.medium}–${BANDS.high-1}, Low &lt; ${BANDS.medium}. ${risks.length} risks.</div>
    <div class="mn">Samaya Investment · Technical Office — project risk control document.</div>`;
}
```

## Layer 2 — 4-card strip below the KPIs

### HTML (insert after `<div class="kpis" id="kpis"></div>`)

```html
<div class="registers" id="registers">
  <div class="reg-card reg-current">
    <div class="reg-head"><span class="reg-badge">current</span><span class="reg-code">PRR</span></div>
    <div class="reg-title">Master Risk Register</div>
    <div class="reg-sub">Project Risk Register (PRR) — <span class="reg-doc">ASR-SAM-RMP-001</span> · Rev C11</div>
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
  <a class="reg-card" href="HSE/">
    <div class="reg-head"><span class="reg-code">HSE</span></div>
    <div class="reg-title">HSE Risk Register (Fit-Out)</div>
    <div class="reg-sub">HSE — <span class="reg-doc">ASR-SAM-HSE-001</span> · Rev C11</div>
    <div class="reg-stats">41 risks · 30 Critical · 11 High · all Ongoing</div>
    <div class="reg-foot">Open sub-register →</div>
  </a>
  <a class="reg-card" href="AV/">
    <div class="reg-head"><span class="reg-code">AVR</span></div>
    <div class="reg-title">AV &amp; Multimedia Register</div>
    <div class="reg-sub">AVR — <span class="reg-doc">ASR-SAM-AVR-001</span> · Rev C11</div>
    <div class="reg-stats">12 risks · 5 High · 5 Medium · 2 Low · all Open</div>
    <div class="reg-foot">Open sub-register →</div>
  </a>
</div>
```

### JS (live counts for the current-register card)

```javascript
function renderRegisterStats(){
  const el = $('#regStats');
  if (!el) return;
  const by = r => risks.filter(x=>x.rating===r).length;
  const open = risks.filter(r=>r.status==='Open').length;
  const totalCats = (RISK.rbs_categories||[]).length
    || (new Set(risks.map(r=>r.category).filter(Boolean))).size;
  el.textContent = `${by('Critical')} Critical · ${by('High')} High · ${by('Medium')} Medium · ${by('Low')} Low · ${open} Open · ${totalCats} categories`;
}
```

Wire into `init()`:

```javascript
renderKPIs(); renderRegisterStats(); renderFooter(); renderSelects(); renderHead(); renderAll();
```

**Sibling cards keep STATIC counts** (a snapshot of the last deploy). They are not driven from the live data because the master page doesn't load sub-register JSONs. Update those numbers manually when a sub-register is rebuilt — or generate them at build time from each sub-register's last-known counts.

## CSS (add next to the existing `.kpis` rule)

```css
.registers { display: grid; grid-template-columns: repeat(4, minmax(0, 1fr)); gap: 12px; margin-bottom: 18px; }
.reg-card { background: #fff; border: 1px solid var(--border); border-radius: 12px;
            padding: 14px 16px; text-decoration: none; color: var(--ink);
            transition: transform .12s ease, box-shadow .12s ease, border-color .12s ease;
            display: block; min-width: 0; }
a.reg-card:hover { transform: translateY(-1px); box-shadow: 0 6px 18px rgba(15,23,42,.08); border-color: var(--navy); }
.reg-card.reg-current { background: linear-gradient(180deg, #f8fafc 0%, #ffffff 100%);
                        border-color: var(--navy); box-shadow: inset 0 0 0 1px var(--navy); cursor: default; }
.reg-head { display: flex; align-items: center; gap: 8px; margin-bottom: 6px; }
.reg-badge { display: inline-block; background: var(--navy); color: #fff;
             font-size: 9.5px; font-weight: 700; letter-spacing: .08em; text-transform: uppercase;
             padding: 2px 7px; border-radius: 999px; }
.reg-code { font-family: 'IBM Plex Mono', monospace; font-weight: 700; font-size: 12px;
            color: var(--muted); letter-spacing: .04em; }
.reg-title { font-size: 15px; font-weight: 700; color: var(--navy); margin-bottom: 2px; }
.reg-sub { font-size: 11.5px; color: var(--muted); margin-bottom: 8px; }
.reg-doc { font-family: 'IBM Plex Mono', monospace; color: var(--ink); }
.reg-stats { font-size: 12.5px; color: var(--ink); margin-bottom: 6px; }
.reg-foot { font-size: 11px; color: var(--accent); font-weight: 600; letter-spacing: .02em; }
a.reg-card .reg-foot { color: var(--navy); }

@media (max-width: 1180px) { .registers { grid-template-columns: repeat(2, 1fr); } }
@media (max-width: 700px) { .registers { grid-template-columns: 1fr; } }
@media (max-width: 1080px) { .registers { grid-template-columns: 1fr; } }
```

## Design tokens assumed by the CSS

The pattern above uses the standard Samaya register tokens already in the template:
- `--border` (light gray border)
- `--navy` (primary navy — for current register highlight + badge)
- `--ink` (body text)
- `--muted` (muted text)
- `--accent` (subtle red accent for the "you are here" footer text)

If your register template uses different tokens, rename the references in the CSS. The geometry (border-radius 12px, padding 14×16, gap 12px) is portable.

## When to update the sibling card counts

After every sub-register deploy, update the static `<div class="reg-stats">` lines in the master page. Quick recipe:

```bash
# After deploying DDR/, fetch the new counts and patch the master template
curl -s https://samaya-factory.com/aseer/registers/Risk/DDR/ \
  | python3 -c "
import sys, re, json
h = sys.stdin.read()
m = re.search(r'const RISK\\\\s*=\\\\s*(\\\\{.*?\\\\});', h, re.DOTALL)
d = json.loads(m.group(1))
risks = d.get('risks', [])
from collections import Counter
rc = Counter(r['rating'] for r in risks)
print(f\\\"{len(risks)} risks · {rc.get('Critical',0)} Critical · {rc.get('High',0)} High · {rc.get('Medium',0)} Medium · {rc.get('Low',0)} Low\\\")
"
```

Drop the output into the DDR card's `reg-stats` div, rebuild, redeploy. The current-register card stays live (driven by `renderRegisterStats()`), the siblings stay as last-known snapshot.

## CRITICAL: Never regex-patch deployed pages

Regex-based banner replacement (`<div class="registers" id="registers">.*?</div>\s*</div>`) is fragile — the `.*?` with multiple `</div>` closes can eat adjacent sections (analytics, matrix, toolbar). Always rebuild from the master template by swapping the JSON payload and the current-card marker, then upload the full file.

**Correct approach for adding a new sub-register:**

1. Add the new card to the master template's banner (static HTML + CSS + JS siblings).
2. Build the sub-register's JSON with the correct `is_*` flag.
3. Write a build script that:
   - Reads the master `src/index.html`
   - Swaps the JSON payload (regex: `const RISK = \{.*?\};`)
   - Swaps the current-card marker using **string slicing** (not regex):
     ```python
     i = html.find('<div class="registers" id="registers">')
     j = html.find('<div class="analytics">', i)
     if j < 0:
         j = html.find('<div class="toolbar">', i)
     html = html[:i] + new_banner + '\n\n  ' + html[j:]
     ```
   - Fixes hrefs to use `../` prefix
   - Writes to `av/src/index.html`
4. Upload the rebuilt HTML directly.

The `build_av.py` script at `~/aseer-museum-pm/06_Risk_System/webapp/av/build_av.py` is the reference implementation.
