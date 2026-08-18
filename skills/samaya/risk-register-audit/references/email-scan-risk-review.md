# Email-Scan → Risk Review Workflow

Recurring task: "check all email scan rounds from the last weeks — any risks need update or close?"

## Where the scans live

`03_Plans/08_Risk/reviews/email_scan_*.md` — one file per scan round, named by date (e.g. `email_scan_2026-08-11.md`, `email_scan_2026-08-06-5.md` for multiple rounds same day). List them newest-first:

```bash
ls -t 03_Plans/08_Risk/reviews/email_scan_*.md
```

## What to extract from each scan

| Scan section | Risk-relevant signal |
|--------------|---------------------|
| CG Responses (Code B/C/D) | Code B = sub-risk reduced; Code C/D = sub-risk worsened |
| New Submissions | May resolve a risk's action item |
| Contract / EOT | EOT/agreement events feed PRR-COM-01, PRR-MEP-01 |
| NCR / SOR closeouts | Feed PRR-HSE-01, PRR-SIT-01 |
| Key Correspondence | Specialist appointments, disputes |

## Cross-reference pattern (the core skill)

1. **Read all scans** in the window (don't skip "no project-critical emails" rounds — they confirm nothing changed).
2. **Map each event to a risk ID** by grepping `risks.json` for the doc ref / keyword:
   ```python
   import json
   d = json.load(open('06_Risk_System/risks.json'))
   for r in d['risks']:
       blob = json.dumps(r).lower()
       if 'zd-0093' in blob or 'fire alarm' in blob:
           print(r['id'], r.get('status'), r.get('title','')[:60])
   ```
3. **Verify against the submittal register** (`01_Registers/submittal_register.md`) — it holds the authoritative CG codes and dates. Don't trust the scan's summary alone; the register's `source:` line and per-row codes are ground truth.
4. **Decide update vs close**:
   - **Update** when a sub-assessment/approval changes the risk's evidence or reduces (but doesn't eliminate) it.
   - **Close ONLY** when the parent risk's root cause is fully resolved. A sub-approval (e.g. fire alarm assessment Code B) does NOT close a parent risk (e.g. IFC-0004 still Code C). Verify the parent's blocking condition is actually gone before closing.
   - **Code B closes a "rejected deliverable" risk (user rule, 2026-08-18):** if the risk's CORE is that a plan **OR drawing / render / DD package / submission** "stays rejected / Code C / Code D / not approved" (PEP, BOD, arch 3D renders, structural DD, execution plan, etc.), then the moment that deliverable reaches **Code B**, the risk is CLOSED — the root cause (rejection) is gone. Keep the still-open `actions[]` in the action plan (they continue to be managed after close); closing the risk does NOT delete its actions. Do NOT leave such a risk "Mitigated/Open" on the theory that "Code B = approved with comments, still work to do" — the user treats **Code B as effective approval** (CG never issues Code A), and states it plainly as **"code B = not a real risk = close"**. This extends to drawings/renders/DD packages, not just formal "plans" — PRR-DES-02 (arch 3D renders Code B) closed under this rule.
   - **Sub-approval ≠ parent closure, but deliverable-approval = risk closure.** The distinction: a sub-approval of a *different* deliverable (e.g. fire alarm assessment under a life-safety risk) does not close the parent; but approval of the *very plan/drawing/render/package the risk is about* does close it.
   - **Apply the Code B rule across ALL registers, not just PRR (2026-08-18).** The user said "apply everything at all risk registers not only PRR". Each sub-register has its own source JSON (`ddr_risks.json`, `hse_risks.json`, `av_risks.json`) and its own submittal cross-refs. When sweeping:
     - **DDR** (`ddr_risks.json`): close risks whose core is a rejected/pending *design submission* now Code B — e.g. DDR-ARC-001 (arch 50% gates all Code B/DA), DDR-STR-001 (structural 1C0-1G-0001 Rev.02 Code B). Do NOT close genuine technical risks (clash, capacity, lead-time, humidity, load) even if some submittal got Code B.
     - **HSE** (`hse_risks.json`): all 41 are site-safety hazards (work at height, hot work, confined space, lifting) — these are NOT approval risks, NEVER close them regardless of submittals.
     - **AV** (`av_risks.json`): check AV submittals (e.g. AV DD 1E0-1G-0002 was Code D 02-Aug) — if still Code C/D, keep open. Only close if an AV design/IFC submission actually reached Code B (a supplier *prequalification* Code B like PQ-0056 Panasonic does NOT count — it's not the design deliverable).
   - **Deploy sub-register closures to `/build/` manually** — the post-commit hook only deploys PRR. After closing DDR/HSE/AV risks, rebuild each page and scp to `/build/aseer/registers/Risk/{DDR,HSE,AV}/index.html` (see `references/risk-webapp-ui.md`).

## Pitfalls

- **Sub-approval ≠ parent closure.** Fire alarm ZD-0067 approved B did not close PRR-FLS-01 (IFC-0004 still Code C). Always check the parent's own blocking item.
- **Counts drift between scan and register.** A scan may say "13B/8C" while the register shows a different split (e.g. 9B/4C/7UR from a different date). Use the register's most recent authoritative count; note the date.
- **New rejections worsen a risk** — e.g. setwork PQs (BTT, Saudi Emaar) Code D feed PRR-PRC-04; don't downgrade it just because another specialist got approved.
- **Never embed internal reasoning in `response_action`/`title` (user rule, 2026-08-18).** The register is a deliverable for the user/CG. Do not write justifications like "per internal decision", "Code B treated as final approval because CG never issues Code A", or any note explaining *why you* chose a status — that is internal process, not risk content. Keep `response_action` factual (the strategy + the actual state). Put process reasoning only in `history` if it must be recorded, or leave it out entirely. The user will correct you with "ولا تذكر هذه الملاحظه الداخليه / انا عايز ال risk الحقيقي فقط يسجل" if you add it.
- **When the user says "طبق عموماً" (apply generally), scope it by the rule's TRUE condition.** E.g. "close any plan that reached Code B" means close ONLY risks whose *core* is that plan's rejection — not every risk touching an approved doc. Confirm which candidates actually meet the condition before bulk-applying; a rejected-plan risk (PEP, BOD) closes, but a risk merely *linked* to an approved submittal does not.
- **RMP/plan approvals often have no dedicated risk** — check before assuming a risk tracks it. If none exists, the approval is informational only.

## Action-Plan Progress Pass (per snapshot release)

The user's standing requirement: **every new snapshot must show progress**. This
means updating the `actions[]` array on each risk — status AND due dates — not
just appending evidence. A snapshot whose action plan still says
"Not Started" with a stale past due date reads as no progress, even if evidence
was logged. So before building each snapshot:

1. **Read every email scan in the window + all registers** (NCR, SI, submittal,
   prequalification, procurement, material submittal, specialist register,
   letters, RFI, meeting minutes, daily report). Evidence lives scattered across
   all of them — a CG Code B in submittal_register, an NCR closure in
   ncr_register, a contract execution in specialist_register, etc.
2. **For each risk's actions, set `status` + `due` from evidence:**
   - CG approval / contract signed / NCR closed / submission approved → `Done` or `Closed`
   - Ongoing work with a passed date → `In Progress` + roll the `due` forward
   - `Done`/`Completed` counts and `In Progress` counts are the visible progress KPI
   - Match actions by a unique substring of `action['text']` — never by index.
3. **Roll forward In-Progress actions whose `due` is in the past** to a realistic
   forward date (never a Friday — KSA weekend). Otherwise the snapshot shows a
   wall of stale "Overdue" that hides the fact work is ongoing.
4. **Sync every mirror** after editing SoT `risks.json`: `prr_risks.json` (full
   mirror — replace each risk object with the fresh one by id, preserve wrapper
   fields like `scoring`/`rbs_categories`/`owners`) and `dashboards/risks.json`
   (curated subset — update only the ids present). Then `risk_sync.py` → rebuild
   snapshots → deploy.
5. **Report the before/after KPI delta** to the user (Done, In Progress, Not
   Started counts) so the progress is explicit. `risk_register.md` does NOT show
   the action plan (only core columns), so the snapshot Excel is what carries it.

## Update pattern (when a risk needs updating)

Append to `evidence` (don't replace — keep the audit trail), bump `last_reviewed`, add a `history` entry with the date + what changed. A runnable helper is at `scripts/update_risks.py` — copy it, fill the `UPDATES`/`HISTORY` dicts, run it. Then rebuild + deploy:

```bash
cd 06_Risk_System && python3 webapp/build_risk.py && python3 risk_sync.py
cd webapp && python3 build_snapshots.py --bump && bash deploy.sh
```

Commit with a message listing which risks changed and explicitly noting "no risks closed" when that's the case.
