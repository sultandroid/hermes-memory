# Risk Closure → Cascade (GitHub issues + Odoo tasks + webapp + snapshots)

Worked end-to-end 2026-08-28. When you close a PRR risk because the underlying gap
is resolved (specialist appointed, work folded in-house, submission approved Code B),
the change propagates through SIX layers. Missing any one leaves an inconsistency.

## The cascade (order matters)

1. **Find the resolvable risks.** Sources of truth for "is this gap actually closed":
   - `Technical_Office/Specialist_Management/specialist_register.md` — appointment status
     (🟢 appointed / 🟡 in progress / 🔴 not started / ⚪ vacant). A risk like
     "X specialist not appointed" is CLOSED when the register shows the specialist
     Integrated/Appointed, even if a DIFFERENT entity does the work (e.g. interactive
     folded into Rawasin; structural in-house at Samaya).
   - GitHub issues that were closed with PM answers (e.g. #262 "structural done
     internally from Samaya") are independent corroborating evidence — but the
     register row is primary.
   - Rule 10 in AGENTS.md: a submission returned **Code B = approved** → the
     associated risk is closed (client rarely issues clean Code A).

2. **Edit `prr_risks.json`** — set `status:"Closed"`, `target_close:today`, append a
   `history` entry (`{date, action:"Closed", by:"Hermes", note:"<evidence>"}`) and add
   the factual evidence strings to `evidence[]`. Keep the note CLEAN (no internal
   rationale/decision commentary) per AGENTS.md Rule 10.

3. **Mirror the SAME change into `risks.json`** — separate file, separate SoT for the
   master webapp page. (See SKILL.md "PRR has TWO source JSON files".)

4. **Rating downgrade (not closure):** to move High→Medium, lower probability/severity
   and recompute `score = p × s`; pick the rating from `{3:Low,4:Medium,6:Medium,9:High,12:Critical}`.
   Flipping the label alone leaves it High.

5. **Rebuild webapps + snapshots + copy to OneDrive:**
   ```bash
   cd 06_Risk_System/webapp
   python3 build_risk.py && python3 build_dashboard.py
   python3 build_ddr.py && python3 build_hse.py     # if those changed
   python3 build_snapshots.py --bump                 # PRR/DDR/HSE new seq
   # copy the new EXP-RISK-*_ACTIVE.xlsx to OneDrive 05_Submittle/REV{NN} subfolders
   ```

6. **Deploy** — `bash deploy.sh` (SSH to Hostinger port 65002). Verify with curl
   that the page shows "Closed" / new revision, and all 4 register URLs return 200.

7. **Sync GitHub issues** — `python3 scripts/risk_issue_daily.py` (repo root). It
   auto-closes the `Risk — <ID>` issue for each newly-closed/mitigated risk and posts
   a comment on downgraded ones. Confirms "Closed #NNN" in output.

8. **Commit + push** both JSON files + rebuilt HTML + snapshot_counter.json. Use the
   stash/rebase dance (`git stash push`, `git pull --rebase`, `git push`, `git stash pop`)
   because the repo post-commit hook dirties `webapp/src/index.html` on every commit.

## Odoo task reconciliation (project 219)

After the risk/register cascade, check whether the corresponding Odoo tasks mis-state
project reality. Tasks that were 100% but shouldn't be (or 0% but work is active):

| Evidence (repo) | Odoo task fix |
|-----------------|---------------|
| Specialist has no signed contract / deliverable still blocked | Lower progress (e.g. 100%→20%), NOT close |
| Task folded into another entity's scope (Rawasin interactive) | Set `stage_id:480` (Cancelled) rather than delete (append-only rule) |
| Contract signed + work proceeding | Set `progress:0.20` (started, not done) |
| Deliverable approved Code B | Set `progress:1.0` |

**Pitfall — `xmlrpc read` with a list of ids is unhashable.** Use
`execute_kw(..., 'read', [tid, [...fields]])` with a single int id, or
`search_read` — do NOT pass `[[1,2,3], fields]` to `read`. (Hit this 2026-08-28:
`TypeError: unhashable type: 'list'`.)

## Worked example — 2026-08-28 closures

- **PRR-PRC-03** (Interactive specialist not appointed, Critical) → **Closed**.
  Interactive folded into Rawasin scope (decision 08-Aug), SOW INT-001 Rev03 in
  Rawasin's name; DDR-INT-001 already Closed. `risks.json` + `prr_risks.json` both
  updated; `risk_issue_daily.py` auto-closed GitHub issue #93.
- **PRR-PRC-12** (Heritage structural engineer not appointed) → **Closed**. Structural
  is in-house at Samaya (Eng. Ahmed Gad); corroborated by GitHub #262. Auto-closed #111.
- **PRR-PRC-01** (ZNA contract conditions, High) → **Medium**. ZNA appointed, ZD-0056
  Code B, fee approved, A1 done. Lowered probability 3→2, score 9→6. Issue #91 got a
  status comment (stayed open).
