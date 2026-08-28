# Risk-Tracker GitHub Issue Sync — Auto-Generated, Do NOT Manually Close

## What these issues are

The `sultandroid/aseer-museum-pm` repo has a cron (`risk_issue_daily.py`, job "Daily Risk-Tracker Issue Sync" `204dc4f6de92`) that maintains **one GitHub issue per risk** titled `Risk — <ID>` (e.g. `Risk — PRR-APP-02`, `Risk — DDR-SHC-005`, `Risk — HSE-01`, `Risk — AVR-OPS-01`). These are labelled `risk-tracker,risk-daily,<REGISTER>`.

**They are a mirror of the live risk registers, not independent work items.** The source of truth is `06_Risk_System/{prr,ddr,hse,av}_risks.json`. The cron:
- posts a dated status comment on an issue ONLY when the risk's state changed (status/rating/score/owner/target_close/actions/evidence count)
- **closes the issue automatically** when the risk's `status` becomes `closed`/`mitigated` in the JSON
- records a fingerprint per risk in `06_Risk_System/.risk_issue_state.json`

## The critical rule

**Do NOT manually close a `risk-tracker` GitHub issue.** The 188+ open risk-tracker issues are NOT stale or abandoned — they are genuinely open risks in the registers. Manually closing them would (a) desync them from the JSON source of truth, and (b) be re-opened or contradicted on the next cron run. The ONLY correct way to close a risk-tracker issue is to close the underlying risk in `*_risks.json` (via the SoT pipeline in `risk-id-conventions.md`), and let the cron close the issue.

## Verify sync before concluding anything

Before reporting "N risk-tracker issues are open" or "these can be closed", run the dry-run to confirm the issues are in sync with the JSON:

```bash
cd ~/aseer-museum-pm
python3 scripts/risk_issue_daily.py --dry-run
# Output: "Done. Commented=0 Closed=0 Baseline=0 Unchanged=188 MissingIssue=0 Errors=0"
```

- `Unchanged=188` → all open risk issues match their JSON fingerprint (nothing stale, nothing to close).
- `Closed=0` → no risk in the JSON has flipped to closed/mitigated, so no issue should be closed.
- If `Closed>0` in dry-run, those are risks whose JSON status is closed but whose issue is still open — the real (non-dry) run will close them.

## Distinguish risk-tracker issues from real work items

When the user asks "close all open issues" or "find evidence to close them", FIRST separate the two populations:

```bash
# Non-risk-tracker issues (real work items — these are the ones you can act on)
gh issue list -R sultandroid/aseer-museum-pm --state open --limit 300 \
  --json number,title,labels -q '.[] | select(([.labels[].name] | join(",")) | test("risk-tracker") | not) | "\(.number)\t\([.labels[].name]|join(","))\t\(.title)"'
```

The risk-tracker population (typically 180-190 of ~200) is auto-managed — leave it alone. The non-risk population (Open Questions, known-issues, commercial, bug) is where manual close-with-evidence work happens.

## Evidence-based closing of NON-risk issues

For the real work items, close only with evidence (per AGENTS.md Rule 10: Code B = practical final approval → risk closed; and the user's standing rule "ردودك تكون بادله" — every claim cites a repo path / register row / doc ref / Outlook ID). Patterns that worked (2026-08-28):
- **Open Question answered** → close with the answer + evidence source (email ID, register row, issue #).
- **known-issue fixed** → verify the fix in the current file/script, then close citing the commit hash.
- **Commercial resolved** → reconstruct the agreed position from the email thread (Sent Items + vendor acceptance), reconcile the repo file, close citing the email IDs. See `outlook-email/references/commercial-counter-schedule-drafting.md` Rule 5 & 7.
- **Deploy/bug fixed** → verify the latest CI run succeeded (`gh run list` + `gh run view <id>`), confirm the runner is online, close citing the fix commit.

## Pitfall — "close all" does not mean close the risk-tracker population

When the user says "عالج الكل" / "close everything", they usually mean the actionable non-risk issues. Do not interpret it as license to mass-close the 188 risk-tracker issues — those require the underlying risk to actually be mitigated in the register, which is a real project action, not an issue-hygiene task. Report the split clearly: "X non-risk issues closed; N risk-tracker issues remain open because they are live risks in the register."
