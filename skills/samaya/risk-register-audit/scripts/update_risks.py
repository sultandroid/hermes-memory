#!/usr/bin/env python3
"""Reusable helper to update risks.json after an email-scan risk review.

Pattern: append to `evidence` (keep audit trail), add a `history` entry with
date + what changed, bump `last_reviewed`. Never replace evidence, never close
a risk unless the parent's root cause is fully resolved.

Usage: copy this into a temp script, fill the UPDATES dict, run:
    python3 update_risks.py
Then rebuild + deploy:
    cd 06_Risk_System && python3 webapp/build_risk.py && python3 risk_sync.py
    cd webapp && python3 build_snapshots.py --bump && bash deploy.sh
Commit with a dated message listing which risks changed and explicitly noting
"no risks closed" when that's the case.
"""
import json

PATH = '/Users/mohamedessa/aseer-museum-pm/06_Risk_System/risks.json'
REVIEW_DATE = '2026-08-15'  # set to today
REVIEW_NOTE = 'Updated from email scans 11-15 Aug'  # window description

# risk_id -> list of evidence strings to append
UPDATES = {
    # 'PRR-HSE-01': ["SI-022 OPEN (13-Aug) — ..."],
}

# risk_id -> history note (one per risk)
HISTORY = {
    # 'PRR-HSE-01': "New OPEN SI-022 (13-Aug) on C&D waste non-compliance added.",
}


def main():
    d = json.load(open(PATH))
    risks = {r['id']: r for r in d['risks']}

    for rid, items in UPDATES.items():
        r = risks[rid]
        ev = r.get('evidence', [])
        if isinstance(ev, str):
            ev = [ev]
        for it in items:
            if it not in ev:
                ev.append(it)
        r['evidence'] = ev

    for rid, note in HISTORY.items():
        r = risks[rid]
        h = r.get('history', [])
        if isinstance(h, str):
            h = []
        h.append({"date": REVIEW_DATE, "action": "Updated from email scans",
                  "by": "Hermes", "note": note})
        r['history'] = h
        r['last_reviewed'] = REVIEW_DATE

    json.dump(d, open(PATH, 'w'), indent=2, ensure_ascii=False)
    print("Updated:", sorted(set(UPDATES) | set(HISTORY)))
    print("No risks closed.")


if __name__ == '__main__':
    main()
