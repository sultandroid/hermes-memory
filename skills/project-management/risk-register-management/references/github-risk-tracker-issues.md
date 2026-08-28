# GitHub Risk-Tracker Issue System — Aseer Museum PM

The repo `sultandroid/aseer-museum-pm` maintains a **GitHub issue per risk** (title `Risk — <ID>`), auto-generated and kept in sync by `scripts/risk_issue_daily.py`. This is a coordination layer over the risk registers, NOT a separate source of truth.

## How it works

- **Source of truth = `06_Risk_System/{prr,ddr,hse,av}_risks.json`** (NOT the GitHub issues).
- `risk_issue_daily.py` reads every risk, computes a `fingerprint()` (status, rating, score, owner, target_close, action statuses, evidence count), and:
  - **First run** (no cached state): records baseline, does NOT comment.
  - **Risk status Closed/Mitigated**: closes the matching open issue (`state_reason: completed`).
  - **Fingerprint changed**: posts a dated status comment on the issue.
  - **Unchanged**: silent.
- State cache: `06_Risk_System/.risk_issue_state.json` (maps risk ID → last-synced fingerprint).
- Cron: `Daily Risk-Tracker Issue Sync` (job `204dc4f6de92`, 07:00 daily).

## CRITICAL — do not manually close risk-tracker issues

The 188+ `risk-tracker`-labelled issues (PRR/DDR/HSE/AVR) are **legitimately open** because the underlying risks are still open in the JSON. Closing them by hand is FALSE — the daily cron will not re-open them, and you lose the audit trail.

**Before touching ANY risk-tracker issue, run the sync in dry-run to see what the source of truth says:**
```bash
cd ~/aseer-museum-pm && python3 scripts/risk_issue_daily.py --dry-run
```
Output `Commented=0 Closed=0 ... Unchanged=188` means all issues are in sync with the JSON — leave them alone. Only if the dry-run reports `Closed=N` (risks whose JSON status is Closed/Mitigated but whose issue is still open) should you let the real sync close them.

## Triage rules for NON-risk issues

When asked to "handle all open issues", separate the risk-tracker noise from the actionable ones:

| Issue type | Label | Action |
|---|---|---|
| Risk-tracker | `risk-tracker,risk-daily,{PRR/DDR/HSE/AV}` | Do NOT close manually. Verify via dry-run. |
| Known-issue (bug) | `known-issue` | Check if already fixed in repo/commit. If fixed → close with evidence (commit SHA + what changed). Sibling agents often fix these first — verify current state before re-fixing. |
| Open Question (answered) | `question` | If the question is answered with evidence in comments and no action remains → close with the evidence summary. |
| Open Question (pending external) | `question` | If it needs an external party (Waris, Nader, Finance, HR, sign-off) → LEAVE OPEN. Do not close falsely. |
| Commercial / Discussion | `commercial`, `discussion` | Leave open unless the deliverable (e.g. formal reply doc) is actually produced and signed off. |

## Pitfalls

- **Sibling-agent race**: multiple agents (Hermes, Kimi, Codex) work the same repo. A fix you apply may already exist on the remote. Before editing a register, `git pull --rebase`; if a rebase conflicts on your file, check whether the remote version already contains the fix — if so, take `--theirs` and drop your redundant change rather than force your version.
- **`git pull --rebase` stalls on unstaged changes**: stash unrelated workstream changes first (`git stash push -m "wip"`), rebase+push, then `git stash pop`. Do NOT commit other agents' in-flight work.
- **Rebase conflict resolution**: `git checkout --theirs <file>` + `git add` + `GIT_EDITOR=true git rebase --continue` (EDITOR unset in dumb terminal).
- **Issue count truncation**: `gh issue list --limit 100` truncates. Use `--limit 300` and filter out `risk-tracker` labels to see the real actionable set.
- **Close with evidence**: always attach a comment citing the source (commit SHA, register line, CG sheet ref, Aconex no.) before closing. Never close with a bare "done".
