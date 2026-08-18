# Risk Webapp UI: Recent Updates block & per-page header source-of-truth

Applies to the Aseer risk register webapp: `06_Risk_System/webapp/` — PRR (`src/index.html`),
DDR (`src/DDR/`), HSE (`src/HSE/`), AV (`src/AV/`).

## All pages share one template — but each has its OWN source JSON

All four pages build from the same `template.html`, so any UI change (Recent Updates
block, layout, CSS) propagates to all four **on rebuild**. BUT each page reads a
**different source-of-truth JSON** for its data and header:

| Page | Build script | Source JSON | Header `last_updated` comes from |
|------|-------------|-------------|----------------------------------|
| PRR  | `build_risk.py` | `risks.json` | `risks.json` |
| DDR  | `build_ddr.py` | `ddr_risks.json` | `ddr_risks.json` |
| HSE  | `build_hse.py` | `hse_risks.json` | `hse_risks.json` |
| AV   | `build_av.py` (in `av/`) | `av/risks_av.json` | `av/risks_av.json` |

**Pitfall — stale-looking header:** if you update `risks.json` (PRR) only, the PRR
header shows today but DDR/HSE/AV still show their own older `last_updated`. That is
CORRECT — their data did not change. Do not fake-touch their source JSON just to make
the header current; a header date newer than the data is misleading. If the user wants
all headers refreshed, the right move is to actually review/update each sub-register,
not bump a date.

**Pitfall — rebuilding only PRR:** `deploy.sh` step 6 does `cp -r av/src/* src/AV/`.
If you changed `template.html` and only ran `build_risk.py`, the live DDR/HSE/AV pages
keep the old UI until you rebuild those too. After any `template.html` edit, rebuild
ALL four (`build_risk.py`, `build_ddr.py`, `build_hse.py`, `build_av.py` then copy
`av/src/*` to `src/AV/`) and commit — the post-commit hook re-deploys.

## Recent Updates block

Sits at the bottom of the page. Purpose: show the reader what changed in each snapshot
release — the user wants it ABOVE the register table (below the toolbar) so they see
activity first, and they want the *change text*, not just a flat date+ID.

### How it works (JS `renderRecentUpdates()` in `template.html`)
- Old behaviour: sorted risks by `last_reviewed`/`last_updated`, showed 5 rows of
  `date + id + title + status`. Problem: every risk touched in one pass shares the
  same `last_reviewed`, so the block looked frozen and showed nothing about *what* changed.
- New behaviour (2026-08-18): flattens EVERY risk's `history[]` into one event list,
  sorts by `history[].date` newest-first, shows 8 rows of
  `date + id + title(+ change note) + status`. The change note is `history[].action + note`.
- **Filter internal-noise history rows** so the block only surfaces meaningful changes:
  - skip if note matches `/no score change/i`
  - skip merge bookkeeping: action matches `/duplicate scope absorbed/i`
  - skip creation noise: action is exactly `Created` (matches `/^Created$/i`)
- Rows are clickable → open the risk drawer.
- Column header is `What changed` (not `Title`); the change note renders in muted
  small text under the bold risk title (CSS `.ru-note`).

### HTML placement (in `template.html`)
The block div must sit BETWEEN the `.toolbar` and the `.tcard` (the register table) so
it appears above the table. CSS lives under the `/* ---------- recent updates ---------- */`
comment (add `.ru-note`/`.ru-t` rules there). After editing: rebuild all 4 pages, commit.

## Build + deploy
```bash
cd 06_Risk_System/webapp
python3 build_risk.py   # PRR
python3 build_ddr.py    # DDR
python3 build_hse.py    # HSE
cd av && python3 build_av.py && cd ..
# copy av/src/* into src/AV/ (deploy.sh does this; do it manually if running builds separately)
bash deploy.sh          # rsyncs src/ to Hostinger /build/aseer/registers/Risk/
```
Then `git add -A && git commit`.

**CRITICAL deploy pitfall — the post-commit hook only deploys PRR.** The hook
(`~/.hermes/scripts/update-all-registers.sh`) rebuilds and scp's ONLY
`src/index.html` (PRR) to `/build/aseer/registers/Risk/index.html`. It does NOT
deploy DDR/HSE/AV. So after a `template.html` or DDR/HSE/AV data change:
1. `bash deploy.sh` uploads to the **non-build** path (`.../public_html/aseer/...`),
   but the site is served from `/build/` (root `.htaccess` rewrites `!^/build/` → `/build/$1`).
   So `deploy.sh` alone does NOT make DDR/HSE/AV live.
2. The post-commit hook only refreshes PRR on `/build/`.
3. **You must scp DDR/HSE/AV to `/build/` manually** after building:
   ```bash
   scp -P 65002 -i ~/.ssh/id_rsa -o StrictHostKeyChecking=no \
     src/DDR/index.html u517606786@samaya-factory.com:/home/u517606786/domains/samaya-factory.com/public_html/build/aseer/registers/Risk/DDR/index.html
   # repeat for HSE/ and AV/
   ```
Verify each live page with `curl .../build/aseer/registers/Risk/{DDR,HSE,AV}/index.html?cb=N`
and grep for the expected change (e.g. `What changed`, or a closed risk id).

LiteSpeed may serve stale HTML for a few minutes; bypass with `?cb=N` query param.

## Ownership & Tracking drawer — "Rescheduled" field

The risk drawer's **Ownership & Tracking** section shows Owner / Target close / Created /
Last reviewed. When a risk's `target_close` is moved (e.g. by an EOT extension), record
it so the reader sees the reschedule and its reason:

1. In the source JSON, add a `rescheduled` object to the risk:
   ```json
   "rescheduled": {
     "date": "2026-08-18",
     "from": "2026-08-21",
     "to": "2027-05-11",
     "note": "EOT LT-0007 (223-day) to 11-May-2027 — completion rescheduled"
   }
   ```
   Also update `target_close` to the new date and append a `history` entry
   `{date, action:"Rescheduled", note:"... (from <old>)"}` so the Recent Updates block
   surfaces it.
2. In `template.html`, inside the Ownership & Tracking `.kv` block, add a conditional
   row that renders only when `r.rescheduled` exists:
   ```js
   ${r.rescheduled?`<div class="k">Rescheduled</div><div class="v mono">${esc(r.rescheduled.date||'')} · ${esc(r.rescheduled.from||'')} → ${esc(r.rescheduled.to||'')}</div><div class="k">Reason</div><div class="v">${esc(r.rescheduled.note||'')}</div>`:''}
   ```
3. Rebuild all four pages, deploy, commit.

**Caveat — reschedule vs approval:** only reschedule `target_close` when the new date is
grounded in a real instrument (e.g. an EOT request). If the EOT is still *pending* MoC
approval, the date is provisional — flag it (e.g. "pending EOT approval") rather than
presenting it as final, and be ready to revert if rejected.
