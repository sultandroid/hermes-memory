# Risk Closure Candidate Review — evidence-based workflow

Applies when the user asks "شوف دلائل لقفلها" / "find evidence to close the open issues" — i.e. they want the ~188 auto-synced risk-tracker issues (or the risks behind them) triaged for closure, using real evidence from the repo registers + specialist register + email thread.

## The setup (verified 2026-08-28)

`aseer-museum-pm` has ~188 open risk-tracker issues, one per open risk in `06_Risk_System/{prr,ddr,hse,av}_risks.json`. The daily cron `risk_issue_daily.py` auto-closes an issue when its risk's JSON status becomes `closed`/`mitigated`. So the ONLY way to close these issues is to change the underlying risk's status in the JSON — which is a **hard user-approval gate** (never modify a risk without prior approval).

## Workflow

1. **Confirm the issues are auto-synced, not manual:** `python3 scripts/risk_issue_daily.py --dry-run` → if `Closed=0`, every risk issue is legitimately open per SoT. Nothing to close by hand.
2. **List the non-risk issues** (the real triage targets) and their states:
   ```
   gh issue list -R sultandroid/aseer-museum-pm --state open --limit 300 \
     --json number,title,labels -q '.[] | select(([.labels[].name] | join(",")) | test("risk-tracker") | not) | "\(.number)\t\([.labels[].name]|join(","))\t\(.title)"'
   ```
   Then `gh issue view <n> --json state` for each — many are already CLOSED from prior sessions; don't re-chase.
3. **For each risk you suspect is closable, gather the falsifying evidence** from:
   - `Technical_Office/Specialist_Management/specialist_register.md` — appointment status (🟢 Appointed / Integrated). A risk premised on "specialist not appointed" is void once the specialist is appointed, folded into an internal scope, or done in-house.
   - The submittal/prequalification registers — Code B = practical final approval (PM decision 2026-08-18), so a risk premised on "plan stays rejected (Code C/D)" is CLOSED once that plan reaches Code B (actions stay in the action plan).
   - GitHub issue comments / closed sibling issues — e.g. #262 confirmed structural is done in-house by Samaya (Eng. Ahmed Gad); #261 confirmed AD Engineering contract effective.
   - `03_Scope/<specialist>/README.md` decisions (e.g. Rawasin README: interactive design+execution folded into Rawasin — an internal specialist, so "no interactive specialist appointed" is false).
   - Cross-referenced DDR risk that already closed (e.g. `DDR-INT-001` Closed mirrors the PRR-PRC-03 premise).

## Strong closure candidates observed (2026-08-28) — verify against CURRENT data, do not copy blindly

| Risk | Premise | Falsifying evidence | Action |
|------|---------|--------------------|-------|
| PRR-PRC-03 (Critical) | Interactive design specialist not appointed | Rawasin decision 08-Aug: interactive folded into Rawasin (sister co, internal specialist); specialist_register line 62 = Integrated 🟢; DDR-INT-001 = Closed; INT-001 SOW Rev03 prepared in Rawasin name (24-Aug) | Propose status→closed; needs user approval |
| PRR-PRC-12 (Medium) | Heritage structural engineer not appointed | Structural done in-house by Samaya (Eng. Ahmed Gad); specialist_register line 45; issue #262 | Propose status→closed; needs user approval |
| PRR-PRC-01 (High) | ZNA contract conditions not closed | ZNA appointed, ZD-0056 Code B, fee £40,527 approved; A1 (close ZD-0056 conditions)=Done, but A2 (mobilisation notice)=Not Started | Partially resolved → maybe downgrade High→Medium, not close |
| PRR-PRC-02 (Critical) | Showcase long-lead exceeds float | Glasbau Hahn appointed, ZD-0030 Code B; A1 In Progress but A2/A3 Not Started (PO + shop-drawing schedule pending) | Still open — no closure evidence |

## Not-yet-closable (no falsifying evidence) as of 2026-08-28

PRR-PRC-04 (missing Tier-2 — landscaping/T&C still gaps), PRR-PRC-08 (porcelain tiles MA-0001 still Code D), PRR-PRC-09 (paint submittal not submitted), PRR-PRC-10 (MEP installer not awarded), PRR-PRC-11 (no Oddy lab), PRR-PRC-13 (SASO/Energy Star), PRR-PRC-05/06/07 — all have actions Not Started and no evidence their premise is false.

## Critical rule

**Present the closure candidates to the user with evidence and get approval BEFORE touching `*_risks.json`.** The user's standing rule (from memory/risk audit) is: never register or modify any risk without prior approval. After approval: edit JSON → `risk_sync.py` → `webapp/build_risk.py` → `build_snapshots.py --bump` → rebuild → commit/push → next cron sync closes the GitHub issue automatically.
