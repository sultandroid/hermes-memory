# Plan Approval Email → Repo Update Workflow (Aseer Museum)

When CG/PMC returns a **Code B approval** for a plan via Outlook email, process it end-to-end in one pass. Worked example: PEP `MOC-MUS-ASE-1K0-ZD-0086 Rev.02` approved 06-Aug-2026 (Aconex CGP-WTRAN-000236).

## 1. Confirm the approval code from the email + PDF

- Query Outlook SQLite: `SELECT Message_Preview FROM Mail WHERE Message_NormalizedSubject = '<doc ref> / <PLAN NAME>' ORDER BY Message_TimeReceived DESC LIMIT 1;`
- The approval email body states the code directly, e.g. `CG Code : Approved with Comment - B`. Use the **email text** over any summary/transcript — the user's hard rule is "read source, verify CG codes from actual email preview, not cron summary."
- Cross-check the submittal PDF cover sheet if needed: `pdftotext -layout <pdf> -` shows the approval block (A/B/C/D). The email is usually sufficient.

## 2. Locate the plan folder's PDF attachment

Outlook stores attachments under:
`~/Library/Group Containers/UBF8T346G9.Office/Outlook/Outlook 15 Profiles/Main Profile/Files/S0/2/Attachments/0/`
Filenames are `MOC-...-ZD-XXXX_Rev.NN[NNNNNNN].pdf`. `find ... -iname "*<DOCREF>*"` to list all revisions + CRS xlsx.

## 3. Update the plan folder's OWN files (the most-missed step)

| File | Change |
|------|--------|
| `<plan>.md` frontmatter | `revision: Rev.NN`, `cg_status: Code B ... (DD-MMM-YYYY)`, `date_issued`, `source:` now points to the approval transmittal |
| `<plan>.md` Revision History table | Append each submission row (Rev.00 C, Rev.01 C, Rev.02 B), last row = approved |
| `approval_log.md` | Append the approved rev row with Aconex no.; set footer `> Approval Status: ✅ Code B ...` |
| `plan_summary.md` | `status: draft` → `approved`; add Approval Status table showing the full rev cycle; tick the "approval obtained" checkbox |

## 4. Update the index + registers (must recount)

- `08_Document_Index/plan_<ref>.md` — CG status → Code B
- `08_Document_Index/00_plan_tracker.md` — move row to Approved section; **recount Quick Summary** (Code B +1, Submitted -1)
- `08_Document_Index/obligation_matrix.md` — move to Approved section; **recount its own Quick Summary** (it can drift to a different total than the tracker)
- `08_Document_Index/approved_plans.md` — update the plan row status
- `01_Registers/submittal_register.md` — add `Rev.NN ... B` row with approval date + Aconex; update any "days silent / risk" table row
- `CHANGELOG.md` — add entry under `## [Unreleased] / ### Added`

## 5. Commit + push (multi-agent repo conflict handling)

- `git add -A && git commit -m "Update YYYY-MM-DD: <PLAN> Rev.NN Code B approved (Aconex ...)"`
- `git pull --rebase && git push`. If a parallel sub-agent pushed meanwhile:
  - `rm -f .git/index.lock`
  - if stuck in rebase: `git rebase --abort`, `git checkout main`, `git pull --rebase origin main`
  - resolve file conflicts with `git checkout --theirs <file> && git add <file>`, then `GIT_EDITOR=true git rebase --continue`
  - Do NOT `git reset --hard` blindly — it can orphan a sibling sub-agent's commits.
  - Verify `git log --oneline origin/main -1` matches local `-1` and that your edits are actually in the pushed tree.

## 6. Report

Give the user: approval code + date + transmittal, the rev history (C → C → B), and which files changed. Note any still-pending plans.

## 7. After approval — extract obligations AND derive linked risks

Once a plan is approved (Code B), the user's standing expectation is that it produces two downstream artifacts:

1. **Compliance obligations** — append rows to `08_Document_Index/00_compliance_system.md` §1 Master Obligations Register. Each row: `Plan Ref | Category | Obligation | Source Plan | Frequency`. For a PEP, pull the time-bound and recurring obligations: T&C Plan submission (8 weeks pre-PC), Method Statements 14 days pre-package, ITPs 14 days pre-works, emergency drill 30 days post-mobilisation, test results to Aconex in 3 working days, clash reports bi-weekly, monthly EAC/P6/cash-flow/progress claims/VO register, WBS to Level 4.

2. **Linked risks** — for each obligation that could fail, add a risk. Derive the ID from the correct RBS category (a T&C/methodology gap = `CON`, a reporting/financial gap = `COM`, an upload/QC gap = `QLT`). Score via probability×severity (≥12 Critical, ≥8 High, ≥4 Medium). Owner = the role accountable for the obligation (Tech Office Mgr for T&C plan, Project Mgr for MS/ITP and monthly reports, HSE Mgr for drill, QA/QC for test upload).

The two-step order matters: obligations first (source of truth for what's required), then risks (each obligation becomes a risk whose failure mode is "obligation not met").

### Sync a new risk across ALL register files (single source of truth is `06_Risk_System/risks.json`)

After editing `risks.json`, run the FULL sync chain — the webapp and dashboards read derived files, not `risks.json` directly:

```bash
# 1. Canonical PRR file (webapp dashboard reads this, not risks.json)
python3 scripts/sync_pep_risks_prr.py        # copies new PRR-* risks from risks.json → prr_risks.json

# 2. Markdown register (auto-generated from risks.json — do NOT hand-edit)
python3 06_Risk_System/risk_sync.py          # → 01_Registers/risk_register.md

# 3. Dashboard snapshot (Critical+High only)
python3 scripts/sync_pep_risks_dashboard.py  # copies only Critical/High PRR risks → dashboards/risks.json

# 4. Webapp build (deployed page)
python3 06_Risk_System/webapp/build_risk.py  # → webapp/src/index.html

# 5. Arabic titles (bilingual webapp/snapshots)
#    append to "titles_ar" in 06_Risk_System/risk_titles_ar.json
```

Then verify JSON validity on all four files (`risks.json`, `prr_risks.json`, `dashboards/risks.json`, `risk_titles_ar.json`) before committing. The `01_Registers/risk_register.md` is regenerated by `risk_sync.py`, so a manual edit there gets overwritten on the next sync — always edit `risks.json` (SoT) and re-run the generator.

**Keep a reusable script pattern**: save each sync step as a small script in `scripts/` (`add_pep_risks.py` creates the risks in `risks.json`, `sync_pep_risks_prr.py` / `sync_pep_risks_dashboard.py` copy derived files) rather than re-typing the JSON merge inline each session. The risk object schema (from `risks.json`): `id, category, title, cause, event, consequence, probability, severity, score, rating, status, owner, target_close, created, last_reviewed, treatment_file, evidence, response_action, actions[], history[], diagram.fishbone, action_due`.

