# Per-Risk GitHub Issue Tracker (one issue per risk)

Pattern for tracking risks via GitHub issues where **one issue = one risk**, synced
from the register JSON source-of-truth files. Built for `aseer-museum-pm`
(PRR/DDR/HSE/AVR registers), 2026-08-15.

## Architecture

```
06_Risk_System/
  prr_risks.json   -> PRR-*  (label PRR)
  ddr_risks.json   -> DDR-*  (label DDR)
  hse_risks.json   -> HSE-*  (label HSE)
  av_risks.json    -> AVR-*  (label AV)
  .risk_issue_state.json   <- per-risk fingerprint cache (NOT category map)

scripts/
  risk_issue_tracker.py   # create missing issues (idempotent)
  risk_issue_daily.py     # daily status comment + close on Closed/Mitigated
```

Two scripts, not one:
- **`risk_issue_tracker.py`** — creates one issue per risk. Idempotent: matches
  existing issues by title `Risk — <ID>`, only creates missing ones. Run once or
  when new risks are added. Labels: `risk-tracker,risk-daily,<REGISTER>`.
- **`risk_issue_daily.py`** — daily sync. Posts a dated status comment on an issue
  ONLY when the risk's state changed (status, rating, score, owner, target_close,
  actions, evidence count). **Closes the issue when the risk is Closed/Mitigated.**

## State file — the critical pitfall

`risk_issue_daily.py` fingerprints each risk and stores `{risk_id: fingerprint}`
in `.risk_issue_state.json`. **The state file MUST be per-risk fingerprints.**

Symptom of a stale/wrong-format state file: the daily run reports
`Baseline=0 Unchanged=188` (or `Unchanged=N` for every risk) instead of
`Baseline=195`. This happens when the state file still holds the OLD category
format (`{"APP": ["PRR-APP-01", ...]}`) from a previous per-category system.

**Fix:** delete the state file and re-run once to establish the per-risk baseline:
```bash
rm -f 06_Risk_System/.risk_issue_state.json
python3 scripts/risk_issue_daily.py   # -> Baseline=195, Errors=0
```
Verify after: `python3 -c "import json; d=json.load(open('06_Risk_System/.risk_issue_state.json')); print(all(k.startswith(('PRR','DDR','HSE','AVR')) for k in d))"` → `True`.

## Auth — use `gh` CLI, not a raw token

Scripts that read `~/.git-credentials` for a PAT **fail** when the machine is
authenticated via `gh` keyring (no `~/.git-credentials` file exists). Error:
`RuntimeError: No GitHub token found`.

**Fix:** make the API wrapper detect `gh` and shell out to `gh api` instead of
raw `urllib` with a token:
```python
def get_token():
    import shutil
    if shutil.which("gh"):
        return "gh-cli"          # gh is keyring-authenticated
    # fall back to ~/.git-credentials or GITHUB_TOKEN ...

def api(method, path, token, body=None):
    if token == "gh-cli":
        import subprocess
        args = ["gh", "api", "--method", method, path]
        if body is not None:
            args += ["--input", "-"]
        r = subprocess.run(args, input=json.dumps(body) if body is not None else None,
                           capture_output=True, text=True)
        if r.returncode != 0:
            return {"_error": "gh", "_body": r.stderr}
        return json.loads(r.stdout) if r.stdout.strip() else {}
    # ... raw urllib path with token
```

## Rating case format — match existing issues exactly

Existing issue bodies use **`CRITICAL` uppercase** but **`Medium`/`High`/`Low`
title-case**. If your body builder uppercases everything (or title-cases
everything), the body-hash diff flags every issue as changed on every run →
perpetual re-update churn.

```python
rating = risk.get('rating','') or ''
rating_disp = rating.upper() if rating.lower() == 'critical' else rating
```

## Idempotency verification

Before the first real run, dry-run and confirm a re-run is stable:
```bash
python3 scripts/risk_issue_daily.py --dry-run   # first: Baseline=195
python3 scripts/risk_issue_daily.py             # second: Unchanged=195, Errors=0
```
A second run showing `Unchanged=195` proves the body builder matches the live
issues (no format churn). If it shows `Updated=N`, diff one issue's generated
body against the live body to find the format mismatch (rating case, emoji,
`—` vs `-`, etc.).

## Close-on-mitigated

The daily script must close the issue when the risk status is `Closed`/`Mitigated`
(and reopen is not needed — the tracker is a view of the register). Check the
issue's current state first (`GET /issues/{num}`), only PATCH `state: closed`
if it's still open. Use `state_reason: "completed"`.

## Pitfall — sibling-commit duplication

Before building a new tracker script, **check `git log` for an existing one**.
A parallel agent may have already committed `risk_issue_tracker.py` +
`risk_issue_daily.py` (and created the 195 issues). Building a second
`sync_risk_issues.py` duplicates the system and two scripts fight over the same
issues. If a sibling system exists, consolidate onto it (enhance the missing
behaviour — e.g. add close-on-mitigated + gh auth) and delete your duplicate,
rather than maintaining two.

## Cron

Daily cron runs `risk_issue_daily.py` (status comments + close), then
`risk_issue_tracker.py` (create issues for any newly added risks), then rebuilds
the webapp if a register JSON changed. Report `[SILENT]` when nothing changed.
