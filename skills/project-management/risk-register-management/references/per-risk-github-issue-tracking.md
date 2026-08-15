# Per-Risk GitHub Issue Tracking — Aseer Museum

One GitHub issue per individual risk (the "risk-daily" model), so any agent can
answer/update a risk via a GitHub issue without knowing the repo layout. This
replaced the earlier per-category model (20 issues, one per RBS category).

## Architecture

| Register | Source file | ID prefix | Issue label |
|----------|------------|-----------|-------------|
| PRR | `06_Risk_System/prr_risks.json` | `PRR-*` | `PRR` |
| DDR | `06_Risk_System/ddr_risks.json` | `DDR-*` | `DDR` |
| HSE | `06_Risk_System/hse_risks.json` | `HSE-*` | `HSE` |
| AVR | `06_Risk_System/av_risks.json` | `AVR-*` | `AV` |

Issue title = `Risk — <ID>` (e.g. `Risk — PRR-APP-02`). Labels: `risk-tracker`,
`risk-daily`, plus the register label. All on `sultandroid/aseer-museum-pm`.

## Two scripts (do NOT duplicate)

- **`scripts/risk_issue_tracker.py`** — creates one issue per risk. Idempotent:
  only creates missing ones (matches existing by title `Risk — <ID>`). Run once,
  or when new risks are added.
- **`scripts/risk_issue_daily.py`** — daily sync. Posts a dated status comment
  on an issue ONLY when the risk's state changed (status, rating, score, owner,
  target_close, actions, evidence count). **Closes the issue when the risk is
  Closed/Mitigated.** State: `06_Risk_System/.risk_issue_state.json`.

Cron `204dc4f6de92` (daily 07:00) runs both.

## PITFALL: duplicate scripts from concurrent sub-agents

A sibling sub-agent commit (`b65e690`) had ALREADY built `risk_issue_tracker.py`
+ `risk_issue_daily.py` and created the 195 issues. A parallel agent (this
session) independently wrote a third script `sync_risk_issues.py` doing the same
job. Result: two scripts fighting over the same issues.

**Lesson:** before writing a new sync/automation script for a repo, check
`git log --oneline` for a recent sibling commit that may already have created
the mechanism. If one exists, extend it rather than writing a parallel one.
Consolidate: delete the duplicate, keep the committed one, add the missing
behaviour (e.g. close-on-mitigated) to the existing script.

## PITFALL: `gh` CLI keyring auth vs raw token

`risk_issue_daily.py` originally read a raw PAT from `~/.git-credentials` or
`GITHUB_TOKEN`. On this Mac neither exists — auth is via `gh` keyring
(`gh auth status` shows `sultandroid`). The script failed with
`RuntimeError: No GitHub token found`.

**Fix:** make the API wrapper prefer the `gh` CLI when available. Return a
sentinel `"gh-cli"` from `get_token()` when `shutil.which("gh")`, and in `api()`
shell out to `gh api --method <M> <path> [--input -]` instead of raw urllib.
This works with keyring auth and needs no stored token.

## PITFALL: state file format mismatch

The daily script's state file `.risk_issue_state.json` must hold per-risk
fingerprints (key = risk ID). If it still holds the OLD per-category format
(key = RBS category, value = list of risk IDs), the daily run reports
`Baseline=0 Unchanged=N` and never comments/closes. Reset the state file so the
next run records a clean per-risk baseline.

## Rating display format (match existing issues to avoid churn)

Existing issue bodies uppercase ONLY `CRITICAL`; `High`/`Medium`/`Low` stay
title-case. If a regenerator uppercases all ratings, every issue shows as
"changed" every run. Match the existing convention:
`rating.upper() if rating.lower() == 'critical' else rating`.

## Update protocol (for agents)

1. Read current state from the relevant register JSON + submittal/NCR/RFI registers for evidence.
2. Edit the register JSON: append to `evidence` (never delete), bump `last_reviewed`, add a `history` entry.
3. Rebuild + deploy: `cd 06_Risk_System && python3 webapp/build_risk.py && python3 risk_sync.py && cd webapp && python3 build_snapshots.py --bump && bash deploy.sh`
4. Comment on the risk's issue with a dated summary.
5. Close the issue only when the risk is Closed/Mitigated (daily sync also does this).

## Rules

- Sub-approval ≠ parent closure. A sub-assessment Code B does not close a parent risk whose own blocking item is still open.
- Never delete evidence — append only (audit trail).
- No closure unless the root cause is fully resolved.
