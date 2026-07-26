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
- `_scope_ddr()` maps `impact → severity`, passes through `actions`

### HSE — CRITICAL FIELD MAPPING
- `hse_risks.json` — has DIFFERENT field names
- `_scope_hse()` maps:
  - `activity → title`
  - `hazards → cause` (hazards ARE the cause)
  - `controls → response_action` (controls are the response measures)
  - `c_init → severity` (consequence initial rating = severity)
  - `l_init → probability` (likelihood initial = probability)
  - `response_action` → pass through (inject strategy prefix)
- **Pitfall:** The HSE JSON also has `response_action` field which contains `[Strategy: X]` prefix. Always prefer `r.get("response_action", r.get("controls", ""))` to get the strategy-rich text.

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

- Cover block: QR (A1), title (C1), logo (G1) — no merged cells
- KPI strip: B5:G6 (Total, Critical, High, Medium, Low, Open)
- Risk matrix: COUNTIFS formulas referencing Risk Register P and S columns
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

## Matrix COUNTIFS Formulas

The risk matrix uses cross-sheet COUNTIFS formulas instead of hardcoded counts:

```excel
=COUNTIFS('Risk Register'!$C$12:$C$82,4,'Risk Register'!$D$12:$D$82,1)
```

- `$C` = P (probability) column in Risk Register
- `$D` = S (severity) column in Risk Register
- Range starts at row 12 (after header) and ends with generous buffer

### CRITICAL: Formula range must cover all data rows

The formula range is calculated as `11 + len(risks) + 10` (header row + risk count + 10 buffer rows). If the range is too short, COUNTIFS misses the last risks and the matrix shows wrong counts.

**Always add 10+ buffer rows to the formula range.** The `last_data_row` calculation must be generous.

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

## Column Index Tracking

After adding/removing columns in `REG_COLS`, update ALL of these references:

1. **`REG_COLS` list** — the authoritative column layout
2. **`vals` array** in loop — order must match `REG_COLS`
3. **`bold=(i in (...))`** — which columns get bold font
4. **`color=NAVY if i in (...)`** — which columns get navy color
5. **`rcell = ws.cell(row=row, column=...)`** — rating fill on correct column
6. **Auto-filter range** — must cover all columns
7. **Action Plan `cols` list** — separate from REG_COLS

### Known mistakes from adding P and S columns

When P and S were added (columns 3 and 4):
- `rcell` was still pointing at column 3 (now P) instead of column 5 (now Rating) — caused rating fill to appear on P column
- `bold=(i in (1, 4))` pointed to wrong columns — column 4 was Score but became S
- `color=NAVY if i in (1, 4, 7, 8)` also wrong for the same reason

## HSE-specific Scoring Labels

HSE uses Consequence × Likelihood (C×L) scoring instead of Probability × Severity (P×S):

| Register | Matrix scale | Risk Register columns | Dashboard header |
|----------|-------------|----------------------|------------------|
| PRR | P×S 1-4 | P=x, S=x | `P ↓ / S →` |
| DDR | P×I 1-5 | P=x, S=x | `P ↓ / S →` |
| HSE | C×L 1-5 | P=c_init, S=l_init | `C ↓ / L →` |
| AVR | P×S 1-5 | P=x, S=x | `P ↓ / S →` |

The HSE data stores consequence in `c_init` and likelihood in `l_init`. These are mapped to `probability` (l_init) and `severity` (c_init) in `_scope_hse()`. Despite the standard field names, the HSE matrix headers show "C" and "L".

## No Merged Cells Rule

The user explicitly rejected merged cells. All cover block sections (title, meta, QR caption) use individual cells. Section headers write to a single cell without merge.

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

## Verification Checklist

```python
for path in [PRR, DDR, HSE, AVR]:
    wb = openpyxl.load_workbook(path)
    ws = wb['Risk Register']
    wsd = wb['Dashboard']
    
    # 1. No merged cells
    assert len(list(wsd.merged_cells.ranges)) == 0
    
    # 2. Matrix has COUNTIFS formulas
    f = wsd.cell(13, 3).value
    assert str(f).startswith('=COUNTIFS')
    
    # 3. Formula range covers all data
    last_risk = max(r for r in range(12, ws.max_row+1) if ws.cell(r,1).value)
    formula_range = int(re.search(r'\$C\$12:\$C\$(\d+)', str(f)).group(1))
    assert formula_range >= last_risk
    
    # 4. Strategy column present
    headers = [ws.cell(11, c).value for c in range(1, ws.max_column+1)]
    assert 'STRATEGY' in [str(h).upper() for h in headers]
    
    # 5. P and S values populated
    for r in range(12, ws.max_row+1):
        if ws.cell(r,1).value and str(ws.cell(r,1).value)[:3] in prefixes:
            assert ws.cell(r,3).value is not None  # P
            assert ws.cell(r,4).value is not None  # S
    
    # 6. Rating fill on correct column
    rcell = ws.cell(12, 5)
    # rcell should have colored fill
```
