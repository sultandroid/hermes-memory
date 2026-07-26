---
name: register-webapp-pipeline
title: Multi-Register Webapp Build Pipeline — Risk ID Standardization & Snapshot Management
description: Manage the 4-register risk webapp system (PRR/DDR/HSE/AVR) — build pipeline, risk ID conventions, register card fixing, Excel snapshot generation, and auto-deploy cron behavior.
---

## Architecture

### Register Files on GitHub

| Register | Source Data | Build Script | Output HTML |
|----------|-------------|--------------|-------------|
| PRR | `06_Risk_System/risks.json` | `webapp/build_risk.py` | `webapp/src/index.html` |
| DDR | `06_Risk_System/ddr_risks.json` | `webapp/build_ddr.py` | `webapp/src/DDR/index.html` |
| HSE | `06_Risk_System/hse_risks.json` | `webapp/build_hse.py` | `webapp/src/HSE/index.html` |
| AVR | `06_Risk_System/av_risks.json` | `webapp/av/build_av.py` | `webapp/av/src/index.html` |

All build scripts read from the `template.html` in `webapp/` and inject data via the `__RISK_DATA__` token.

**IMPORTANT**: `risks.json` must contain ONLY PRR risks. Other processes frequently add DDR/HSE/AVR risks to it, causing the PRR page to show 184+ risks (should be 61). Check and clean periodically.

The old `generated/` subdirectory has been removed. All source files at `06_Risk_System/` root.

### Server Paths
The `.htaccess` rewrite rule maps `https://samaya-factory.com/aseer/*` → `/build/aseer/*`:
```
RewriteRule ^(.*)$ /build/$1 [L]
```

Actual server paths:
- `/build/aseer/registers/Risk/index.html` — PRR
- `/build/aseer/registers/Risk/DDR/index.html` — DDR
- `/build/aseer/registers/Risk/HSE/index.html` — HSE
- `/build/aseer/registers/Risk/AV/index.html` — AVR

### Risk ID Convention

All registers must follow `{REG}-{RBS}-{NN}` format:

| Register | Format | Example |
|----------|--------|---------|
| PRR | `PRR-{RBS}-{NN}` | `PRR-COM-08` |
| DDR | `DDR-{CAT}-{NN}` | `DDR-TEC-21` |
| HSE | `HSE-{NN}` (single category) | `HSE-01` |
| AVR | `AVR-{CAT}-{NN}` | `AVR-HW-01` |

**Key rule**: Always fix BOTH the source JSON data AND the built HTML. Build scripts regenerate output from source — fixing only the HTML is temporary.

## HSE & DDR Field Mapping (UPDATED 2026-07-26)

**Both HSE and DDR now use standard field names.** Do NOT map old/different field names.

### HSE
HSE data in `hse_risks.json` uses: `title`, `probability`, `severity`, `score`, `response_action`, `cause`, `status`, `owner`, `actions`, `evidence`, `history`.

Historical bug (fixed 2026-07-26): Both `_scope_hse()` in `build_snapshots.py` and `build_hse.py` incorrectly mapped:
- `l_init` → `probability` (should be pass-through)
- `c_init` → `severity` (should be pass-through)
- `activity` → `title` (should be pass-through)
- `hazards` → `cause`/`consequence` (should be pass-through)
- `controls` → `response_action` (should be pass-through)
- `score_init` → `score` (should be pass-through)

**Current correct mapping:**
```python
"probability": r.get("probability", r.get("l_init", 0)),   # fallback for old data
"severity": r.get("severity", r.get("c_init", 0)),         # fallback for old data
"response_action": r.get("response_action", r.get("controls", "")),
"actions": r.get("actions", []),
```

### DDR
DDR data in `ddr_risks.json` uses standard fields: `probability`, `severity`, `score`, `rating`, `title`, `cause`, `consequence`, `response_action`, `actions`.

Historical bug (fixed 2026-07-26): `_scope_ddr()` mapped `r.get("impact", 0)` to severity. DDR data uses `severity`, not `impact`. Fix: `r.get("severity", 0)`.

## Build Pipeline

### Building All Registers
```bash
cd /Users/mohamedessa/aseer-museum-pm/06_Risk_System/webapp
python3 build_risk.py && python3 build_ddr.py && python3 build_hse.py
cd av && python3 build_av.py
```

### Deploying to Server
```bash
cd /Users/mohamedessa/aseer-museum-pm/06_Risk_System/webapp
scp -P 65002 src/index.html u517606786@samaya-factory.com:/home/u517606786/domains/samaya-factory.com/public_html/build/aseer/registers/Risk/index.html
scp -P 65002 src/DDR/index.html .../Risk/DDR/index.html
scp -P 65002 src/HSE/index.html .../Risk/HSE/index.html
scp -P 65002 av/src/index.html .../Risk/AV/index.html
```

## Register Cards Fix

The template has 4 register cards (PRR/DDR/HSE/AVR). **The template hardcodes PRR as current with wrong relative paths** (e.g. `DDR/` instead of `../DDR/` for sub-pages). Two layers of protection (BOTH required):

### Layer 1: Post-build fix_cards_static.py (build-time)
A post-processor `webapp/fix_cards_static.py` runs after each build, replacing register card HTML with correct paths and current-state. All 4 build scripts must call this.

### Layer 2: fixCards() in template.html (JS runtime)
Embedded in `function init()` in `template.html`. On every page load:
1. Reads `RISK.is_ddr` / `is_hse` / `is_av` to determine current register
2. Loops through `#registers .reg-card` elements
3. Fixes href paths using map: `{PRR:'../', DDR:'../DDR/', HSE:'../HSE/', AVR:'../AV/'}`
4. Swaps `<a>` ↔ `<div>` for current vs non-current cards

**Do NOT remove fixCards() from template.html.** The JS function survives auto-deploy reverts.

### Critical notes
- Both layers needed. Post-build gets reverted by auto-deploy cron; JS survives any deployment.
- When testing: verify ALL 4 register pages have correct card links.
- Agent warning comments placed at top of `build_ddr.py` and `build_hse.py`.

## Excel Snapshots

### Generation
```bash
cd /Users/mohamedessa/aseer-museum-pm/06_Risk_System/webapp
python3 build_snapshots.py --bump   # increment counter, generate PRR+DDR+HSE
```
AVR generates its own: `cd av && python3 build_av.py`

### Output files
- `src/EXP-RISK-PRR-2026-{NNN}_Rev{rev}_ACTIVE.xlsx`
- `src/DDR/EXP-RISK-DDR-2026-{NNN}_Rev{rev}_ACTIVE.xlsx`
- `src/HSE/EXP-RISK-HSE-2026-{NNN}_Rev{rev}_ACTIVE.xlsx`
- `av/src/EXP-RISK-AV-2026-{NNN}_Rev{rev}_ACTIVE.xlsx`

### Excel Template Layout

**CRITICAL: Risk matrix values are PRE-CALCULATED in Python (hardcoded integers), NOT COUNTIFS formulas.**
Updated 2026-07-26: LibreOffice recalculation was unreliable and time-consuming. `build_xlsx.py` now computes P×S counts from the risk data using `defaultdict(int)` and writes integer values directly. Cells with 0 risk get `None` (gray fill). Empty cells use `GRAY_ALT` fill.

**Key layout rules:**
- **No merged cells** — every cell is individual. Title, subtitle, meta rows, section headers, and footer must NOT use merged cells.
- **Logo in row 1, column G** (top-right). **QR code in row 1, column A** (top-left), 55px. Title text between them in row 1.
- **Strategy column** extracted from `[Strategy: X]` prefix in `response_action` text. Regex: `r'^\[Strategy:\s*([^\]]+)\]\s*'`
- **Response/Action** formatted as bullet list from `actions` array: each action's `text` field prefixed with `•`
- **Rating fill on column 5** (Rating column), NOT column 3 (P). After adding P/S columns, column indices shifted.
- **P and S columns** are columns C (3) and D (4) in Risk Register. Needed for matrix computation.
- **No EVIDENCE column** in Risk Register sheet — user explicitly rejected.
- **HSE matrix labels**: "C ↓ / L →" with "L1..L5" columns and "C5..C1" rows (controlled by `data.get("is_hse")` flag).

### Excel Template Columns (Risk Register sheet)
Required columns (14 total):
ID, CAT, P, S, RATING, SCORE, STATUS, **STRATEGY**, OWNER, TARGET, RISK EVENT / TITLE, CAUSE, CONSEQUENCE, RESPONSE / ACTION

Bold/navy formatting: bold on cols 1 (ID) and 6 (Score); navy on cols 1, 7, 8, 10, 11 (ID, Status, Strategy, Target, Title).

### Action Plan Sheet
Columns: RISK ID, CAT, RATING, **STRATEGY**, ACTION, OWNER, DUE, STATUS
Each action item gets its own row from the `actions` array. Strategy is extracted same as Risk Register.

### Dashboard Categories
Each register has its own RBS categories. DDR uses: TEC, SCH, EXT, PRO, QA, COM — NOT PRR categories.
HSE uses single category: HSE (Health, Safety & Environment).

### Snapshot file management
- Clean old files before rebuilding: `rm src/EXP-RISK-*-0{01,02,...}_RevC*.xlsx`
- Old high-numbered files take precedence in `sorted(...)[-1]`
- AVR snapshot counter is independent (not in `snapshot_counter.json`)

## Auto-Deploy Cron Behavior

**Two** auto-deploy mechanisms:

1. **`deploy-registers-on-commit`** (agent-based, every 15 min) — checks for file changes and deploys from git. **Always commit and push** after any fix — SCP-only changes get overwritten within 15 minutes.

2. **`register-auto-update`** (daily at 13:00, no_agent) — runs `update-all-registers.sh` (PRR + LN only, NOT DDR/HSE/AVR).

**Action**: After any fix, commit+push, then SCP if immediate deploy needed. The cron will re-deploy within 15 min from git. Always rebuild ALL 4 registers when changing `template.html`.

## OneDrive Daily Snapshot Sync

A cron job `Daily Risk Snapshot Sync` (daily at 9 AM) runs `sync_risk_snapshots.sh`:
- Downloads latest snapshots from webapp to: `.../05_Submittle/REV{NN}/`
- One file per register, replaces old on new download
- Each subfolder: 01_Master_Risk_Register, 02_Design_Risk_Register, 03_HSE_Risk_Register, 04_AV_Risk_Register
- Weekly (Sundays): the script detects current REV folder and increments (REV01 → REV02)

## LiteSpeed Cache Issues

Hostinger's LiteSpeed cache **ignores `no-cache` headers**. Despite `Cache-Control: no-cache, no-store`, the cache can serve stale content for several minutes.

**Verification pattern:**
1. SSH onto server and `grep` the actual file: `grep -c 'search_term' /build/aseer/registers/Risk/DDR/index.html`
2. Use cache-busting URL parameter: `?cb=NNN`
3. Tell user to hard refresh (Cmd+Shift+R)

The file on disk is always correct — what curl or the browser returns may be cached.

## Pitfalls

- **SCP can silently fail** — verify with MD5 checksum after deploy
- **risks.json contamination** — after every git pull/merge, verify it's PRR-only
- **AVR build_av.py xlsx call** uses `out_path=str(xlsx_path)` keyword, not positional
- **Register IDs must be unique** — verify no duplicates when renaming
- **Git conflicts on risks.json** — remote frequently has different version; use `--ours` or force-push
- **Old snapshot files take precedence** — clean old snapshots before rebuilding (sorted picks highest number)
- **Auto-deploy reverts built files** — always commit `src/*/index.html` after rebuild
- **HSE status = "Ongoing"** — not "Open". The KPI heading still says "OPEN" which can be confusing
- **Template changes affect ALL registers** — always rebuild all 4 and verify each one
