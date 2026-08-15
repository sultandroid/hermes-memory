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

## Pitfalls

- **Sub-approval ≠ parent closure.** Fire alarm ZD-0067 approved B did not close PRR-FLS-01 (IFC-0004 still Code C). Always check the parent's own blocking item.
- **Counts drift between scan and register.** A scan may say "13B/8C" while the register shows a different split (e.g. 9B/4C/7UR from a different date). Use the register's most recent authoritative count; note the date.
- **New rejections worsen a risk** — e.g. setwork PQs (BTT, Saudi Emaar) Code D feed PRR-PRC-04; don't downgrade it just because another specialist got approved.
- **RMP/plan approvals often have no dedicated risk** — check before assuming a risk tracks it. If none exists, the approval is informational only.

## Update pattern (when a risk needs updating)

Append to `evidence` (don't replace — keep the audit trail), bump `last_reviewed`, add a `history` entry with the date + what changed. A runnable helper is at `scripts/update_risks.py` — copy it, fill the `UPDATES`/`HISTORY` dicts, run it. Then rebuild + deploy:

```bash
cd 06_Risk_System && python3 webapp/build_risk.py && python3 risk_sync.py
cd webapp && python3 build_snapshots.py --bump && bash deploy.sh
```

Commit with a message listing which risks changed and explicitly noting "no risks closed" when that's the case.
