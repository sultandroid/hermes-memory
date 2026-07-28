# Excel Snapshot Generation System

## Overview

The risk register system generates Samaya-branded Excel snapshots (`.xlsx`) for all 4 registers via `build_xlsx.py`. Each snapshot has 3 sheets: Dashboard, Risk Register, Action Plan.

## Build Pipeline

```
build_snapshots.py --bump   # generates PRR + DDR + HSE
build_av.py                 # generates AVR (separate counter)
```

Each calls `build_xlsx.build()` with register-specific parameters.

## Data Files & Field Mapping

Each register has its own data source with potentially different field names. The build pipeline maps them to standard fields:

### Standard fields (what build_xlsx.py expects)

```python
["id", "category", "title", "cause", "event", "consequence", 
 "probability", "severity", "score", "rating", "status", 
 "owner", "target_close", "response_action", "actions", "evidence"]
```

### PRR
- `risks.json` — already uses standard field names
- `_scope_prr()` passes through as-is

### DDR
- `ddr_risks.json` — uses standard field names
- `_scope_ddr()` maps `severity` (NOT `impact`), passes through `actions`

### HSE — CRITICAL FIELD MAPPING
- `hse_risks.json` — can have DIFFERENT field names (old format) or standard names (new format)
- `_scope_hse()` maps with fallback to old names:
  - `title` (fallback `activity`) → title
  - `cause` (fallback `hazards`) → cause
  - `consequence` (fallback `controls`) → consequence
  - `probability` (fallback `l_init`) → probability
  - `severity` (fallback `c_init`) → severity
  - `response_action` (fallback `controls`) → response_action
  - `actions` → pass-through
  - `target_close` → target_close (NOT hardcoded empty)
- **Pitfall:** If the HSE data was restructured, `cause` and `consequence` may be empty. Restore from git history: `git show <commit>:06_Risk_System/generated/hse_risks.json` and merge `hazards`→`cause`, `controls`→`consequence`.

### AVR
- `av_risks.json` — uses standard field names
- No scoper needed (handled by `build_av.py`)

## Column Layout

### Risk Register (14 columns)

| # | Header | Key | Width | Notes |
|---|--------|-----|-------|-------|
| 1 | ID | `id` | 12 | bold, navy |
| 2 | CAT | `category` | 8 | |
| 3 | P | `probability` | 5 | center |
| 4 | S | `severity` | 5 | center |
| 5 | RATING | `rating` | 10 | colored fill (Critical=red, etc.) |
| 6 | SCORE | `score` | 7 | bold |
| 7 | STATUS | `status` | 11 | |
| 8 | STRATEGY | extracted | 14 | parsed from `[Strategy: X]` prefix |
| 9 | OWNER | `owner` | 18 | |
| 10 | TARGET | `target_close` | 12 | |
| 11 | RISK EVENT / TITLE | `title` | 36 | wrap |
| 12 | CAUSE | `cause` | 32 | wrap |
| 13 | CONSEQUENCE | `consequence` | 32 | wrap |
| 14 | RESPONSE / ACTION | bullet list | 36 | wrap, bullet from actions |

### Action Plan (8 columns)

| # | Header | Width |
|---|--------|-------|
| 1 | RISK ID | 12 |
| 2 | CAT | 8 |
| 3 | RATING | 10 |
| 4 | STRATEGY | 14 |
| 5 | ACTION | 55 |
| 6 | OWNER | 20 |
| 7 | DUE | 12 |
| 8 | STATUS | 14 |

### Dashboard

- Cover block: QR (A1), title (C1), logo (G1) — **no merged cells**
- KPI strip: B5:G6 (Total, Critical, High, Medium, Low, Open)
- Risk matrix: **pre-calculated values** (computed in Python, not COUNTIFS formulas)
- By Rating table: counts per band
- By Status table: counts per status
- Exposure by Category: table + bar chart
- Top Owners: top 8 by count
- Charts: Doughnut (Risks by Rating) + Bar (Risks by Category)

## Strategy Extraction

The `response_action` field may contain a strategy prefix like `[Strategy: Transfer]` followed by the action text.

```python
import re
raw_action = r.get("response_action", "") or ""
strategy = ""
clean_action = raw_action
sm = re.match(r'^\[Strategy:\s*([^\]]+)\]\s*', raw_action)
if sm:
    strategy = sm.group(1).strip()
    clean_action = raw_action[sm.end():].strip()
```

Strategy goes to column 8 (STRATEGY). Cleaned action text goes to column 14 (RESPONSE / ACTION).

If actions array is present, format as bullet list:
```python
acts = r.get("actions", []) or []
if acts:
    clean_action = "\n".join(f"• {a.get('text','')}" for a in acts if a.get('text'))
```

## Risk Matrix — Pre-Calculated Values (No Formulas)

**The matrix uses pre-calculated values computed in Python, NOT COUNTIFS formulas.** This was changed from formulas to avoid LibreOffice recalculation dependency.

```python
ps_counts = defaultdict(int)
for rsk in risks:
    key = (rsk.get("probability"), rsk.get("severity"))
    if key[0] and key[1]:
        ps_counts[key] += 1
# Then write directly as integers
n = ps_counts.get((p, s), 0)
cell = ws.cell(row=rr, column=2 + s, value=n if n > 0 else None)
```

**CRITICAL: `defaultdict` must be imported** (`from collections import defaultdict`). Matrix values are written as integers (n) or `None` (empty cells with gray fill). Cells with values get band-colored fill.

### CRITICAL: Formula range must cover all data rows (historical — only applies if switching back to formulas)

The formula range was `11 + len(risks) + 10`. This is no longer relevant since we use pre-calculated values.

### HSE-specific: Axis labels change

| Register | Header | Col labels | Row labels |
|----------|--------|------------|------------|
| PRR | `P ↓ / S →` | `S1 S2 S3 S4` | `P4 P3 P2 P1` |
| DDR | `P ↓ / S →` | `S1 S2 S3 S4 S5` | `P5 P4 P3 P2 P1` |
| HSE | `C ↓ / L →` | `L1 L2 L3 L4 L5` | `C5 C4 C3 C2 C1` |
| AVR | `P ↓ / S →` | `S1 S2 S3 S4 S5` | `P5 P4 P3 P2 P1` |

Controlled by `data.get("is_hse")` flag:
```python
p_label = "C" if data.get("is_hse") else "P"
s_label = "L" if data.get("is_hse") else "S"
```

The HSE column headers and row labels both use these variables. Do NOT hardcode `"P"` or `"S"`.

## Column Index Tracking (Critical)

After adding/removing columns in `REG_COLS`, update ALL of these references:

1. **`REG_COLS` list** — the authoritative column layout
2. **`vals` array** in loop — order must match `REG_COLS`
3. **`bold=(i in (...))`** — which columns get bold font (currently `i in (1, 6)` = ID and Score)
4. **`color=NAVY if i in (...)`** — which columns get navy color (currently `i in (1, 7, 8, 10, 11)`)
5. **`rcell = ws.cell(row=row, column=...)`** — rating fill on correct column (currently column 5)
6. **Auto-filter range** — must cover all columns
7. **Action Plan `cols` list** — separate from REG_COLS

### Known mistakes from adding P and S columns

When P and S were added (columns 3 and 4):
- `rcell` was still pointing at column 3 (now P) instead of column 5 (now Rating) — caused **rating fill to appear on P column**
- `bold=(i in (1, 4))` pointed to wrong columns — column 4 was Score but became S
- `color=NAVY if i in (1, 4, 7, 8)` also wrong for the same reason

## No Merged Cells Rule

The user explicitly rejected merged cells. All cover block sections (title, meta, QR caption) use individual cells. Section headers write to a single cell without merge. **Zero merged cells across all sheets.**

## OneDrive Daily Sync

A cron job (`Daily Risk Snapshot Sync`, job_id `ef2495d20159`) runs daily at 9:00 AM to download the latest snapshots to OneDrive:

```bash
BASE=".../05_Submittle/REV01/"
01_Master_Risk_Register/  → PRR snapshot
02_Design_Risk_Register/ → DDR snapshot
03_HSE_Risk_Register/    → HSE snapshot
04_AV_Risk_Register/     → AVR snapshot
```

The cron script at `~/.hermes/scripts/sync_risk_snapshots.sh` handles:
- Daily download (replaces old file with latest)
- Weekly rev folder increment (new `REV{NN}` each Sunday)
- File naming: `Aseer_Museum_{REG}_Snapshot_{YYYY-MM-DD}.xlsx`

## Snapshot File Naming Convention

```
EXP-RISK-{REG}-{YYYY}-{NNN}_Rev{rev}_{STATUS}.xlsx
```

Example: `EXP-RISK-PRR-2026-016_RevC11_ACTIVE.xlsx`

- `{REG}` = PRR, DDR, HSE, AV (AVR uses "AV" in filename)
- `{YYYY}` = year
- `{NNN}` = sequential snapshot number per register (counter managed by `snapshot_counter.json`)
- `{rev}` = document revision (C11, C12, etc.)
- `{STATUS}` = ACTIVE

## Action Plan Population

The Action Plan sheet iterates every risk's `actions` array. Each action becomes a row:

```python
for a in (r.get("actions") or []):
    vals = [r.get("id", ""), r.get("category", ""), r.get("rating", ""),
            strategy,  # parsed from response_action prefix
            a.get("text", ""), a.get("owner", ""), 
            a.get("due", ""), a.get("status", "")]
```

If a risk has no `actions` array, no action row is generated. The sheet shows "No discrete actions recorded" if all risks have empty actions.

PRR: 565 actions (from risks.json)
DDR: 193 actions (from ddr_risks.json)
HSE: 164 actions (from hse_risks.json)
AVR: 26 actions (from av_risks.json)

## Build Script Data File Paths

The data files were moved from `generated/` subdirectory to root level:

| Old path | New path | Used by |
|----------|----------|---------|
| `generated/drr_risks.json` | `ddr_risks.json` | `build_ddr.py`, `build_snapshots.py` |
| `generated/hse_risks.json` | `hse_risks.json` | `build_hse.py`, `build_snapshots.py` |

Path resolution from `webapp/`:
```python
# webapp/build_ddr.py
DDR_JSON = HERE.parent / "ddr_risks.json"  # 06_Risk_System/ddr_risks.json
```

## GitHub Actions Auto-Deploy

The workflow at `.github/workflows/deploy-risk-webapp.yml` auto-deploys on push to `main` that touches risk files. It requires the `HOSTINGER_SSH_KEY` secret:

```bash
gh secret set HOSTINGER_SSH_KEY --repo sultandroid/aseer-museum-pm < ~/.ssh/id_rsa
```

This secret is the SSH private key used to authenticate to the Hostinger server. Without it, every push fails at the SSH step.

## Verification Checklist

```python
for path in [PRR, DDR, HSE, AVR]:
    wb = openpyxl.load_workbook(path)
    ws = wb['Risk Register']
    wsd = wb['Dashboard']
    
    # 1. No merged cells
    assert len(list(wsd.merged_cells.ranges)) == 0
    
    # 2. Matrix has pre-calculated values (integers, not formulas)
    total = sum(wsd.cell(r,c).value or 0 for r in range(13,19) for c in range(3,9) 
                 if isinstance(wsd.cell(r,c).value, (int,float)))
    assert total == len([r for r in data['risks'] if r.get('probability') and r.get('severity')])
    
    # 3. Strategy column present
    headers = [ws.cell(11, c).value for c in range(1, ws.max_column+1)]
    assert 'STRATEGY' in [str(h).upper() for h in headers]
    
    # 4. P and S values populated
    for r in range(12, ws.max_row+1):
        if ws.cell(r,1).value and str(ws.cell(r,1).value)[:3] in prefixes:
            assert ws.cell(r,3).value is not None  # P
            assert ws.cell(r,4).value is not None  # S
    
    # 5. Rating fill on correct column (5, not 3)
    rcell = ws.cell(12, 5)
    # rcell should have colored fill
    
    # 6. Action plan has Strategy column
    ws2 = wb['Action Plan']
    act_headers = [ws2.cell(11, c).value for c in range(1, ws2.max_column+1)]
    assert 'STRATEGY' in [str(h).upper() for h in act_headers]
```
