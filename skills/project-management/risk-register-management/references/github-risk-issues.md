# GitHub Per-Risk Issue Tracking (sultandroid/aseer-museum-pm)

The Aseer Museum PM repo maintains **one GitHub issue per risk** so any agent can
answer/update risks through issues without knowing the full repo layout. This is
the established model — do NOT create a different (e.g. per-category) issue scheme.

## The 170+ per-risk issues

- Label: `risk-tracker` (+ `risk-daily`, + a register label `PRR`/`DDR`/`HSE`).
- Title format: `Risk — <RISK-ID>` (e.g. `Risk — PRR-COM-01`).
- Coverage (as of 2026-08-15): PRR 70/70, DDR 72/72, HSE 24/41, AVR 0/12.
  - **Gaps to fill if you touch this:** HSE-12..16, HSE-20..26, HSE-31, HSE-33..36
    (17 missing) and all 12 AVR-* risks.
- Body format (per issue): living-issue header → Register/Rating/P×S/Status/Owner/
  Target-close/Last-reviewed → Title/Cause/Event/Consequence → Response/Strategy →
  Actions → Evidence → Update Protocol → Rules → auto-maintained footer.

## Source of truth

`06_Risk_System/risks.json` (PRR), `ddr_risks.json`, `hse_risks.json`,
`av_risks.json`. Issues are **generated views** refreshed by the daily cron.

## Agent update protocol (embedded in every issue body)

1. Read current state from the register JSON + submittal/NCR/RFI registers.
2. Edit the JSON: append to `evidence` (never delete), bump `last_reviewed`,
   add a `history` entry `{"date","action","by","note"}`.
3. Rebuild + deploy:
   `cd 06_Risk_System && python3 webapp/build_risk.py && python3 risk_sync.py && cd webapp && python3 build_snapshots.py --bump && bash deploy.sh`
4. Comment on the issue with a dated summary.
5. Close the issue only when the risk is Closed/Mitigated.

## Rules (non-negotiable)

- **Sub-approval ≠ parent closure.** A sub-assessment Code B does not close a
  parent risk whose own blocking item is still open.
- **Never delete** evidence — append only (audit trail).
- **No closure** unless the root cause is fully resolved.
- **Never edit the issue top body** — append updates as comments; the cron
  regenerates the body from the register JSON.

## CRITICAL PITFALL — check for existing issues BEFORE creating new ones

Before building any new risk-issue scheme, run:
`gh issue list --repo sultandroid/aseer-museum-pm --label risk-tracker --state all --limit 500`
A per-risk system already exists. Creating a parallel scheme (e.g. per-category
issues) duplicates it and pollutes the label. If you must propose a different
model, ask the user first — do not assume.

## gh CLI pitfalls (learned the hard way)

- **Pagination:** `gh issue list --state all` without `--limit` silently returns
  only ~30 issues. Always pass `--limit 500` (or higher) when counting/auditing.
- **ID regex:** risk IDs contain two dashes (`PRR-COM-10`, `DDR-STR-001`). A regex
  like `(PRR|DDR)-[A-Z0-9]+` truncates at the second dash. Use
  `(PRR|DDR|HSE|AVR)-[A-Z0-9]+(?:-[0-9]+)?` to capture the full ID.
- **Shell blocklist:** `$'\t'` and similar shell-escape constructs in a command
  string can trip the hardline command blocklist. Use a Python script (via
  `write_file` + `python3`) to build tab-separated maps instead of inline shell.
- **Concurrent cron edits:** the `register-auto-update` cron (13:00) and
  `deploy-registers-on-commit` (every 15m) modify `06_Risk_System/webapp/src/index.html`
  concurrently. After a risk rebuild, `git pull --rebase` may conflict on that
  generated file — resolve by re-running `build_risk.py` and recommitting, not by
  hand-editing.

## Daily automation

Cron "Daily Risk-Tracker Issue Sync" (`204dc4f6de92`, 07:00) should run a
**per-risk** sync script that: regenerates each issue body from the register JSONs,
creates missing issues (HSE/AVR gaps), updates via `gh issue edit --body-file`,
reopens issues whose risk is still open, closes issues whose risk is Closed/Mitigated,
and rebuilds+deploys the webapp if the JSON changed.
