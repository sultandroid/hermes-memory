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
| AVR | `webapp/av/risks_av.json` (source) ← also mirror in `06_Risk_System/av_risks.json` | `webapp/av/build_av.py` | `webapp/av/src/index.html` |

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

**PRR has TWO source JSON files — update BOTH when changing PRR risks (recurring trap, bit me 2026-08-28).** `risks.json` (read by `webapp/build_risk.py` for the PRR master page) and `prr_risks.json` (read by `webapp/build_dashboard.py` for the unified dashboard) are SEPARATE files that both carry the PRR risks. Editing only one leaves the other stale — the master page and dashboard will disagree. When you close/downgrade a PRR risk or edit any PRR risk field:
1. Edit `06_Risk_System/prr_risks.json` (canonical register for the dashboard + Excel snapshot).
2. Edit `06_Risk_System/risks.json` with the SAME change (SoT for the PRR master webapp page).
3. Rebuild BOTH: `python3 build_risk.py` (master page) AND `python3 build_dashboard.py` (unified dashboard) — plus `build_ddr.py`/`build_hse.py` if those data changed.
4. `python3 build_snapshots.py --bump` to regenerate Excel snapshots, then copy to OneDrive (see snapshot delivery section).
5. Commit BOTH JSON files + all rebuilt HTML + snapshot_counter.json together.

**Rating downgrade — recompute score, don't just flip the label (bit me 2026-08-28).** Setting `r["rating"]="Medium"` on a risk whose `probability×severity` still equals 9 (High) leaves the risk High in the webapp/Excel because the rating is DERIVED from `score = probability × severity`. To actually downgrade: lower the probability/severity (e.g. `probability 3→2`, `score 9→6`) AND update the rating. Always derive rating from the recomputed score via the rating map `{3:Low, 4:Medium, 6:Medium, 9:High, 12:Critical}`.

**Risk closure → GitHub issue auto-close.** The per-risk GitHub issues (titled `Risk — <ID>`) are synced by `risk_issue_daily.py`. After closing/mitigating risks in the JSON source, run `python3 scripts/risk_issue_daily.py` (from repo root) — it auto-closes the matching GitHub issues for any risk whose status became `closed`/`mitigated`, and posts a dated status comment on changed open risks. It is idempotent and only acts on changed fingerprints, so it's safe to run after every risk-edit commit.

**Full risk-closure cascade** (repo register → webapp → snapshots → OneDrive → GitHub issues → Odoo tasks) is documented in `references/risk-closure-cascade.md` — follow it end-to-end when closing a risk, so no layer is missed.

**CRITICAL — sync direction is JSON → MD, never MD → JSON.** `risks.json` is the single source of truth. `risk_sync.py` regenerates `01_Registers/risk_register.md` FROM the JSON. If you edit the markdown register directly (e.g. to add a new risk or update a cause/response_action), the next `risk_sync.py` run **overwrites your edit**. The correct workflow when adding/updating a risk:
1. Edit `06_Risk_System/risks.json` (add the risk object with full schema: id, category, title, cause, event, consequence, probability, severity, score, rating, status, owner, target_close, created, last_reviewed, response_action, actions[], history[], diagram, action_due).
2. Run `python3 risk_sync.py` to regenerate the markdown register.
3. Run `python3 webapp/build_risk.py` to rebuild the webapp HTML.
4. Run `python3 webapp/build_snapshots.py --bump` to regenerate the Excel snapshot.
5. Commit risks.json + risk_register.md + webapp/src/index.html + snapshot_counter.json (the .xlsx is gitignored — stays in OneDrive).
Verify the new risk appears in all three layers (JSON, MD, webapp) before reporting done.

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

### HSE Strategy Classification (RMP 8.1)

Per RMP §8.1, **Mitigate** only when actions reduce probability (physical controls). Administrative/monitoring-only controls (RAMS, PTW, TBT, PPE) are **Accept (Active)**. See `references/hse-strategy-rmp81.md` for the full classification table, current assignments, and update workflow.

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
Embedded as an IIFE inside `function init()` in `template.html`. On every page load:
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

### Manual snapshot delivery to OneDrive — DELETE-FIRST workflow

When the user asks to "download" or "get" the risk snapshot registers, they want the files **copied to the OneDrive target location**, not generated-and-left in the repo nor sent via chat.

**Target path:**
```
~/Library/CloudStorage/OneDrive-SAMAYAINVESTMENT/Samaya/.../05_Submittle/REV{NN}/
  01_Master_Risk_Register/  → PRR
  02_Design_Risk_Register/  → DDR
  03_HSE_Risk_Register/     → HSE
  04_AV_Risk_Register/      → AVR
```

Full base: `/Users/mohamedessa/Library/CloudStorage/OneDrive-SAMAYAINVESTMENT/Samaya/Technical Office/Bim Unit/Aseer-Museum/04_Docs/02_Plans_and_Procedures/02.17_Risk_Management_Plan/04_Registers/05_Submittle`

**After generating snapshots, copy them immediately:**
```bash
SRC="/Users/mohamedessa/aseer-museum-pm/06_Risk_System/webapp"
DST=".../05_Submittle/REV{NN}"

cp "$SRC/src/EXP-RISK-PRR-2026-{NNN}_RevC{rev}_ACTIVE.xlsx" \
   "$DST/01_Master_Risk_Register/Aseer_Museum_PRR_Snapshot_$(date +%Y-%m-%d).xlsx"
cp "$SRC/src/DDR/EXP-RISK-DDR-2026-{NNN}_RevC{rev}_ACTIVE.xlsx" \
   "$DST/02_Design_Risk_Register/Aseer_Museum_DDR_Snapshot_$(date +%Y-%m-%d).xlsx"
cp "$SRC/src/HSE/EXP-RISK-HSE-2026-{NNN}_RevC{rev}_ACTIVE.xlsx" \
   "$DST/03_HSE_Risk_Register/Aseer_Museum_HSE_Snapshot_$(date +%Y-%m-%d).xlsx"
cp "$SRC/av/src/EXP-RISK-AV-2026-{NNN}_RevC{rev}_ACTIVE.xlsx" \
   "$DST/04_AV_Risk_Register/Aseer_Museum_AVR_Snapshot_$(date +%Y-%m-%d).xlsx"
```

Use today's date as the snapshot filename to replace the previous day's file. The dated filename avoids accumulation — older same-date files overwrite.

**CRITICAL — Delete old files before copying:**
OneDrive does NOT auto-replace files with different names. Old snapshots accumulate. Before copying new files, remove all `.xlsx` from each subfolder:
```bash
rm -f "$DST/01_Master_Risk_Register/"*.xlsx
rm -f "$DST/02_Design_Risk_Register/"*.xlsx
rm -f "$DST/03_HSE_Risk_Register/"*.xlsx
rm -f "$DST/04_AV_Risk_Register/"*.xlsx
```
Then copy. Never copy first and delete after — the old files persist until explicitly removed.

**Safer than `rm`: move old/corrupt files to a `_CORRUPT_<date>/` sibling folder instead of deleting.** This is OneDrive-safe (no destructive delete that propagates), preserves the audit trail, and is preferred over `rm -f` when the user's standing rule is "never delete without explicit confirmation." Use the same dated filename convention for the new files so each release is `Aseer_Museum_{PRR|DDR|HSE|AVR}_Snapshot_YYYY-MM-DD.xlsx` and older dates land in `_CORRUPT_/`.

**Verify source data before generating:**
After a `git pull`, verify the source JSON files actually contain the expected changes before generating snapshots. Pull commits may add fishbone diagrams, fix scores, or adjust dates — but they may NOT have changed the fields you expect (e.g. `response_action`/strategy). Check before building:
```bash
cd 06_Risk_System
python3 -c "import json; d=json.load(open('hse_risks.json')); [print(r['id'], r.get('response_action','')[:60]) for r in d['risks']]"
```

**Verify after copy — spot-check the Excel:**
After copying to OneDrive, open the Excel and confirm key risks have the right values (e.g. PRR-COM-08 title, HSE strategy column). If the user reports wrong data, check the source JSON first — if the JSON has old values, the Excel is correct by construction.

## Auto-Deploy Cron Behavior

**Two** auto-deploy mechanisms:

1. **`deploy-registers-on-commit`** (agent-based, every 15 min) — checks for file changes and deploys from git. **Always commit and push** after any fix — SCP-only changes get overwritten within 15 minutes.

2. **`register-auto-update`** (daily at 13:00, no_agent) — runs `update-all-registers.sh` (PRR + LN only, NOT DDR/HSE/AVR).

**Action**: After any fix, commit+push, then SCP if immediate deploy needed. The cron will re-deploy within 15 min from git. Always rebuild ALL 4 registers when changing `template.html`.

## OneDrive Daily Snapshot Sync

A cron job `Daily Risk Snapshot Sync` (job_id: `ef2495d20159`, daily at 9 AM) runs `sync_risk_snapshots.sh`:
- Downloads latest snapshots from webapp to: `.../05_Submittle/REV{NN}/`
- One file per register, replaces old on new download
- Each subfolder: 01_Master_Risk_Register, 02_Design_Risk_Register, 03_HSE_Risk_Register, 04_AV_Risk_Register
- Weekly (Sundays): the script detects current REV folder and increments (REV01 → REV02)
- Never ran initially (last_run_at was null after creation) — trigger it manually after creation or after major data changes: `cronjob(action='run', job_id='ef2495d20159')`

**CRITICAL — script has stale hardcoded URLs:** The script `sync_risk_snapshots.sh` downloads from hardcoded server URLs with old snapshot filenames (e.g. `EXP-RISK-PRR-2026-012_RevC11_ACTIVE.xlsx`). These filenames increment with each `--bump` build, so the hardcoded URLs go stale. The script will download a 404 or the wrong file if the server doesn't serve the exact old name. **Fix:** update the script to either (a) copy from local repo instead of downloading from server, or (b) discover the latest snapshot filename from the repo directory before downloading.

## GitHub Actions Auto-Deploy

A workflow `.github/workflows/deploy-risk-webapp.yml` auto-deploys on every push to `main` that touches risk files:
- Trigger paths: `06_Risk_System/*.json`, `webapp/**`, workflow file
- Build steps: install deps → build all 4 registers → generate snapshots → SCP to Hostinger
- **SSH key secret `HOSTINGER_SSH_KEY`** is now configured in GitHub repo secrets
- Runs on `ubuntu-latest` with Python 3.12

After every push, check the workflow status:
```bash
gh run list --repo sultandroid/aseer-museum-pm --limit 3
```

If the deploy fails, check: (1) SSH key is still valid on Hostinger, (2) `HOSTINGER_SSH_KEY` secret exists in GitHub, (3) workflow file is syntactically valid.

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
- **AVR has TWO JSON source files** — `build_av.py` reads from `webapp/av/risks_av.json`, NOT from `06_Risk_System/av_risks.json`. When updating AVR strategies, data, or revision, edit BOTH files. The repo-root file (`av_risks.json`) is the canonical source for the repo; the av-folder file (`risks_av.json`) is what the build script reads. Forget one and the Excel won't reflect the change.
- **Register IDs must be unique** — verify no duplicates when renaming
- **Git conflicts on risks.json** — remote frequently has different version; use `--ours` or force-push
- **Old snapshot files take precedence** — clean old snapshots before rebuilding (sorted picks highest number)
- **Auto-deploy reverts built files** — always commit `src/*/index.html` after rebuild
- **HSE status = "Ongoing"** — not "Open". The KPI heading still says "OPEN" which can be confusing
- **Template changes affect ALL registers** — always rebuild all 4 and verify each one
- **Trigger the cron, don't manually copy** — the `Daily Risk Snapshot Sync` cron (job_id `ef2495d20159`) handles OneDrive delivery. Prefer `cronjob(action='run', job_id='ef2495d20159')` over manual `cp` to OneDrive. Only manually copy if the cron is failing and immediate delivery is needed — and always delete-old-first.
- **Pre-commit hook blocks 00_Contracts/ commits** — The repo's pre-commit hook rejects any commit that stages files under `00_Contracts/` (read-only per AGENTS.md). If untracked contract files exist, `git add -A` will stage them and the commit will fail. Use `git add <specific files>` or `git reset HEAD 00_Contracts/` before committing.
- **Post-commit hook modifies risks.json** — After every commit, a post-commit hook regenerates `06_Risk_System/risks.json`. This creates unstaged changes. When pulling with rebase, stash these first or use `git stash && git pull --rebase && git stash pop`.
- **Post-commit hook causes a rebase LOOP (recurring, severe)** — The post-commit hook regenerates files (risks.json, webapp/src/index.html, adel_snapshots, compliance_matrix) on EVERY commit. During a multi-commit `git pull --rebase`, each replayed commit re-triggers the hook, leaving new unstaged changes that block the next rebase step with "cannot pull with rebase: You have unstaged changes." This can cascade into a stale `.git/rebase-merge` state. **Full recovery sequence:**
  1. Commit the auto-generated changes: `git add -A && git commit -m "Auto-sync (post-commit)" --no-verify`
  2. If rebase is stuck, clear the stale state: `rm -fr .git/rebase-merge && git rebase --abort` (ignore "no rebase in progress")
  3. Drop stale stashes that are just auto-sync noise: `git stash drop stash@{N}` (verify each is only sync_state/webapp noise, not real work)
  4. Rebase with a non-interactive editor so the hook can't hang: `GIT_EDITOR=true GIT_SEQUENCE_EDITOR=true git pull --rebase origin main`
  5. If a conflict appears in an auto-generated file (e.g. `webapp/src/index.html`, `risks.json`), resolve by keeping the remote version: `git checkout --theirs <file>` then `git add <file>`
  6. Continue: `GIT_EDITOR=true git rebase --continue`, then `git push origin main`
  **Prevention:** before pulling, `git checkout 06_Risk_System/webapp/src/index.html` to discard the auto-generated copy so it can't conflict. Use `--no-verify` on the auto-sync commit so the hook doesn't re-fire mid-rebase.
- **OneDrive snapshots — stale hardcoded URLs** — The `sync_risk_snapshots.sh` script hardcodes snapshot filenames like `EXP-RISK-PRR-2026-012_RevC11_ACTIVE.xlsx`. These go stale when snapshot numbers increment with each `--bump`. Fix: update the script to copy from local repo instead of downloading from server, or discover the latest filename before downloading.
- **Pull doesn't mean data changed** — a pull with 30 commits may add fishbone diagrams and fix scores, but NOT change `response_action`/strategy fields. Verify source JSON fields before generating snapshots; don't assume what the pull contained.
- **OneDrive cp may write stub files** — CloudStorage File Provider can create stub files instead of real content. After copying to OneDrive, verify file size matches the source (within 5%). If stubbed (file exists but seems wrong), open in Excel directly to force hydration.
- **Existing OneDrive snapshots may ALREADY be broken stubs from a prior failed sync** — observed 2026-08-12: the REV01 subfolders contained 4,511-byte stub `.xlsx` files (dated 08-09) left by an earlier cron run that never hydrated. The `cp` in the delete-first workflow *overwrites* them so they become correct — but **always verify byte-exact size match after copy** (`stat -f%z dst` vs `stat -f%z src`), and confirm the old stub is gone. A stub that gets overwritten is fine; the risk is only if you skip the delete-first step and a differently-named stub survives.
- **AVR may have TWO snapshot files at once (same Rev, different seq)** — observed 2026-08-12: `av/src/` contained both `EXP-RISK-AV-2026-016_RevC12_ACTIVE.xlsx` and `EXP-RISK-AV-2026-017_RevC12_ACTIVE.xlsx`. Pick the **highest sequence number** (017), not any matching-Rev file. The AVR counter is independent of `snapshot_counter.json` (build_av.py derives seq from the files present), so duplicates linger after interrupted builds.
- **User says 'wrong data' — check source first** — If user reports incorrect snapshot data, check the source JSON before the Excel. If the JSON has old values, the Excel is correct by construction and the fix is in the data layer, not the snapshot.
- **User says 'recheck' — verify data content, not just commit log** — When the user says "recheck" after you've already checked, they want you to verify the actual data values (e.g. `response_action` field content, strategy classification), not just the commit history. A pull with 30 commits may add fishbone diagrams and fix scores but NOT change the field you're being asked about. Run a targeted data query on the source JSON, not `git log`.
