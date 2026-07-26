# Risk Register Webapp Build Pipeline

## Architecture

```
06_Risk_System/
├── risks.json              → build_risk.py    → webapp/src/index.html (PRR)
├── ddr_risks.json          → build_ddr.py     → webapp/src/DDR/index.html
├── hse_risks.json          → build_hse.py     → webapp/src/HSE/index.html
└── av_risks.json           → build_av.py      → webapp/av/src/index.html

webapp/
├── build_risk.py           — PRR HTML + xlsx link
├── build_ddr.py            — DDR HTML
├── build_hse.py            — HSE HTML
├── build_snapshots.py      — Generates ALL Excel snapshots (PRR/DDR/HSE)
├── build_xlsx.py           — Samaya-styled Excel workbook builder
├── fix_cards_static.py     — Post-processor: fixes register card current/links
├── template.html           — Shared HTML template for all registers
├── av/
│   └── build_av.py         — AVR HTML + xlsx
└── src/                    — Built HTML outputs
    ├── index.html (PRR)
    ├── DDR/
    ├── HSE/
    └── (AV is under av/src/)
```

## Risk ID Format

All registers follow: `{REG}-{RBS}-{NN}` where REG is PRR/DDR/HSE/AVR.

- Rename IDs in the **source JSON** (`risks.json`, `ddr_risks.json`, etc.)
- **Always rebuild** the affected pages after ID changes — build scripts overwrite output-only edits
- Show the mapping per-risk and get user approval before applying
- Check evidence fields and history notes for old ID references

## Build & Deploy

### Rebuild all webapp pages:
```bash
cd 06_Risk_System/webapp
python3 build_risk.py
python3 build_ddr.py
python3 build_hse.py
python3 av/build_av.py
```

### Regenerate Excel snapshots:
```bash
cd 06_Risk_System/webapp
python3 build_snapshots.py --bump   # increment counter + build
```

### Deploy to server (Hostinger):
```bash
scp -P 65002 src/index.html u517606786@samaya-factory.com:/home/u517606786/.../build/aseer/registers/Risk/index.html
# Repeat for DDR, HSE, AV — same pattern
```

**CRITICAL**: There is an auto-deploy cron job (`deploy-registers-on-commit`) that runs every **15 minutes**. It deploys from the committed git files, overwriting any SCP-only changes. Always commit+push to GitHub to make changes permanent.

## Register Card Navigation

Each page has 4 register cards (PRR, DDR, HSE, AVR) in the `#registers` div.

- **Current register** card → `<div class="reg-card reg-current">` with `current` badge
- **Other registers** → `<a class="reg-card" href="...">` links

**Relative paths must use `../` prefix on sub-pages** (DDR, HSE, AVR):
- From PRR: `DDR/`, `HSE/`, `AV/`
- From DDR: `../`, `../HSE/`, `../AV/`
- From HSE: `../`, `../DDR/`, `../AV/`
- From AVR: `../`, `../DDR/`, `../HSE/`

The `fix_cards_static.py` post-processor automatically corrects these after each build. It's called from build_risk.py, build_ddr.py, build_hse.py, and build_av.py. If cards are wrong, check that the post-processor ran.

## Excel Snapshot Rules (build_xlsx.py)

- **No merged cells** — write to individual cells only
- **Risk matrix** uses **COUNTIFS formulas** referencing the Risk Register sheet's P (col C) and S (col D) columns
- **P and S columns** are written as separate columns in the Risk Register sheet
- **No EVIDENCE column** in the Risk Register — removed from REG_COLS
- **Action Plan** sheet reads from `r.get("actions", [])` — pass through from source data
- Header labels use C/L for HSE (Consequence × Likelihood) instead of P/S

## HSE Field Mapping

HSE data uses different field names. Both build_hse.py and build_snapshots.py's `_scope_hse()` map them:

| Source Field | Mapped To |
|---|---|
| `activity` | `title` |
| `hazards` | `cause`, `consequence` |
| `controls` | `response_action` |
| `l_init` | `probability` |
| `c_init` | `severity` |
| `score_init` | `score` |

Also add: `category: "HSE"`, `is_hse: True`, `rbs_categories: {"HSE": "Health, Safety & Environment"}`.

## Toolbar

Only two buttons: **RESET** + **DOWNLOAD SNAPSHOT**. No CSV, PRINT, or EXCEL buttons. The DOWNLOAD SNAPSHOT links to a pre-generated static `.xlsx` file (not on-demand generation).

## LiteSpeed Cache

Hostinger uses LiteSpeed cache. Even with `no-cache` headers, cached versions may be served for several minutes. Use `?cb=N` query parameter for cache-busting during verification. Hard refresh (Cmd+Shift+R) on the browser.
