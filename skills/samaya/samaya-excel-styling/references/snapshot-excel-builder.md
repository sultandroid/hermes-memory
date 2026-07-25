# Snapshot Excel Builder — Per-Register Pipeline

**Source code:** `~/projects/aseer-museum-pm/06_Risk_System/webapp/build_xlsx.py`
**Counter:** `~/projects/aseer-museum-pm/06_Risk_System/webapp/snapshot_counter.json`
**Builder script:** `~/projects/aseer-museum-pm/06_Risk_System/webapp/build_snapshots.py`
**Deployment:** `~/projects/aseer-museum-pm/06_Risk_System/webapp/deploy.sh`

## Architecture

```
build_snapshots.py [--bump]
  ├─ reads PRR: 06_Risk_System/risks.json
  ├─ reads DDR: 06_Risk_System/generated/drr_risks.json
  ├─ reads HSE: 06_Risk_System/generated/hse_risks.json
  ├─ calls build_xlsx.build() for each register with explicit snapshot_no
  ├─ names output src/EXP-RISK-<REG>-2026-NNN_RevC11_ACTIVE.xlsx
  └─ updates snapshot_counter.json

build_risk.py / build_ddr.py / build_hse.py
  ├─ discover latest EXP-RISK-*_ACTIVE.xlsx via glob (src/ or src/DDR/ or src/HSE/)
  └─ embed xlsx_name in HTML's Excel button

deploy.sh (order matters)
  1. python3 build_snapshots.py --bump
  2. python3 build_risk.py
  3. python3 build_ddr.py
  4. python3 build_hse.py
  5. rsync -avz --delete ./src/ u517606786@samaya-factory.com:.../Risk/
```

## Per-Register Separation (RMP-Compliant)

RMP Section 9.1 defines four linked risk registers with different scoring
scales. Never merge into one view:

| Register | Code | Scale | Count | URL |
|----------|------|-------|-------|-----|
| Master Risk Register | PRR | P x S 1-4 | 52 | /aseer/registers/Risk/ |
| Design Discipline Register | DDR | P x I 1-5 | 79 | /aseer/registers/Risk/DDR/ |
| HSE Risk Register | HSE | C x L 1-5 | 41 | /aseer/registers/Risk/HSE/ |
| AV (if available) | AV | P x S 1-4 | ~30 | (no data yet) |

Each register gets its own build script and xlsx snapshot. The webapp pages
share a single template.html with register-flag-based navigation.

## Webapp Multi-Register Navigation

Each page embeds a flag (e.g. `is_ddr`, `is_hse`) in its data JSON.
The `renderFooter()` in template.html renders sibling links dynamically:

```javascript
const regName = RISK.is_ddr ? 'Design (DDR)' : RISK.is_hse ? 'HSE' : 'Master (PRR)';
const siblings = [];
if (!RISK.is_ddr) siblings.push({url: 'DDR/', label: 'Design (DDR)'});
if (!RISK.is_hse) siblings.push({url: 'HSE/', label: 'HSE'});
if (RISK.is_ddr || RISK.is_hse) siblings.push({url: '../', label: 'Master (PRR)'});
```

- Each build script sets its own flag: `"is_ddr": true`, `"is_hse": true`
- Adding a new register: create the build script, add its flag to data dict,
  add sibling entry in `renderFooter()`, add mkdir to deploy.sh

## Snapshot Counter Management (prevents drift bug)

- `build_xlsx.build()` accepts `snapshot_no` param. When provided, skip auto-bump.
- `build_snapshots.py` manages the counter via `--bump` flag.
- **Idempotent by default** — no counter advance on repeated test runs.
- Only `--bump` advances the number on a real deploy.
- Snapshot number is resolved BEFORE `build()` — xlsx content always matches filename.
- Counter keys: only "PRR", "DDR", "HSE". Never human-readable register names.

```json
{"_comment": "...", "PRR": {"last_snapshot": 1}, "DDR": {"last_snapshot": 1}, "HSE": {"last_snapshot": 0}}
```

## Key lessons from the counter drift bug (fixed Jul 24)

- **Never auto-increment inside the build function.** The build function should
  accept `snapshot_no` as a parameter and let the caller manage the counter.
  When build() both reads and writes the counter, the number printed in the
  xlsx content diverges from the filename.
- **Counter keys must be stable short codes** ("PRR", "DDR"), not human-readable
  names ("Master Risk Register (PRR)"). The rename script and the build script
  must use the SAME key.
- **Idempotent is the default.** `--bump` is the explicit opt-in for advancing
  the counter. This lets you test-build repeatedly without polluting the
  snapshot number sequence.
- **Verify content matches filename after deploy.** Test with:
  ```python
  grep "Snapshot No. NNN" /tmp/live.xlsx && echo "MATCH"
  ```

## Hostinger LiteSpeed 404 Cache (case-sensitive directories)

- New lowercase subdirectories get stuck in a 404 cache with
  `last-modified: Tue, 22 Apr 2025` (Hostinger default).
- **Fix: use UPPERCASE** for the directory name (e.g. `DDR/` not `ddr/`).
- Add `.htaccess` with `CacheDisable public /` and
  `Header set Cache-Control "no-cache, no-store, must-revalidate"`.

## Adding a New Register (checklist)

1. Extract risk data from source Excel -> `06_Risk_System/generated/<reg>_risks.json`
2. Create `build_<reg>.py` in `webapp/` (copy from `build_hse.py` template)
3. Add `COUNTER_KEYS` entry in `build_snapshots.py`
4. Add loop entry in `build_snapshots.py` main()
5. Add sibling link in `template.html` `renderFooter()`
6. Update `deploy.sh` to build and `mkdir -p` the new register
7. Seed snapshot counter to 0 in `snapshot_counter.json`
8. Run `python3 build_snapshots.py --bump && python3 build_<reg>.py`
9. Deploy via `deploy.sh`
10. Verify all 4 URLs (page + xlsx) return HTTP 200

## Cover sheet layout (every xlsx, all 3 sheets)

- Row 1: "ASEER REGIONAL MUSEUM — <Register>" (18pt bold, Navy #1E293B)
- Row 2: "Doc No. <...> · Contract: <...> · Rev <C11> · ACTIVE"
- Row 3: "Snapshot No. <NNN> · Date: <YYYY-MM-DD> · Time: <HH:MM (Asia/Riyadh)> · Source: <URL>"
- Rows 5-6: 6-card KPI strip (B..G), one column per card (NO merged cells)
- Row 8: QR code (A8) + Samaya logo (G8)
- Row 9: "Scan to open live register → <URL>" (italic 8pt gray)

## File naming

`EXP-RISK-<REG>-YYYY-NNN_Rev<rev>_<STATUS>.xlsx`

Example: `EXP-RISK-PRR-2026-001_RevC11_ACTIVE.xlsx`

Old non-versioned names are superseded. The versioned snapshot is the
authoritative download.
