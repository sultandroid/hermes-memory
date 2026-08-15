# GitHub Risk-Tracker Issue System — Aseer Museum

> How the risk register is exposed as GitHub issues on `sultandroid/aseer-museum-pm`, and the duplication pitfall.

## Two overlapping systems (as of 2026-08-15)

| System | Issues | Managed? | Sync |
|--------|--------|----------|------|
| **A. Per-category** | #45–#64 (20) | ✅ `scripts/sync_risk_issues.py` + cron `204dc4f6de92` (daily 07:00) | Regenerated daily from `06_Risk_System/risks.json` |
| **B. Per-risk** | #65–#259 (195) | ❌ **orphaned** — no script, no cron, no commit | **None** |

### System A — the intended one
- One issue per risk category (APP, AV, HSE, PRC, COM, CON, DES, FLS, LOG, MEP, OPS, QLT, SCH, SEC, SHC, SIT, STK, TCH, AVS, CNS).
- Category→issue map is hardcoded in `scripts/sync_risk_issues.py` (`CAT_ISSUE` dict).
- Body is a "living issue": agents update by **commenting**, never editing the top body. Source of truth is `risks.json`.
- Close an issue only when ALL risks in that category are Closed/Mitigated.
- Protocol doc: `06_Risk_System/RISK_ISSUES_PROTOCOL.md`.

### System B — the orphan
- Created 2026-08-15 11:08, one issue per individual risk (HSE-36, AVR-OPS-02, PRR-CNS-01, DDR-…).
- Breakdown: PRR 70 · DDR 72 · HSE 41 · AVR 12.
- All authored by `sultandroid`, labelled `risk-daily` + `risk-tracker`.
- **No manager** — it duplicates System A and will go stale. It also floods the issue list and the Repo Issue Auto-Responder treats them as "new".

## Pitfalls / checks
- **Before answering "check risk issues"**: run `gh issue list --repo sultandroid/aseer-museum-pm --label risk-tracker --state open` and also `--label risk-daily`. If you see both labels, you're looking at the duplication — don't assume both are live.
- **Don't create a third system.** If the user asks for risk issues, extend System A (add a category to `CAT_ISSUE` + `CAT_NAMES`), don't spawn per-risk issues.
- **Recommended cleanup** (if user approves): close the 195 orphaned per-risk issues (#65–#259) in one `gh` batch, keep the 20 managed category issues.
- **Repo Issue Auto-Responder** (cron `4a5142794838`, every 2h) scans 4 repos incl. `aseer-museum-pm` and posts replies autonomously. It will try to reply to any "new" issue — including orphaned risk issues — so dedupe/close orphans before it fires, or add a skip rule for issues authored by `sultandroid`.
