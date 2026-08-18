# Determining When a Risk Actually Closed (Target Close ≠ closure date)

## The trap

The `risk_register.md` table has a column literally named **`Target Close`** (header:
`| ... | Owner | Status | Target Close | Evidence |`). The date in it is a
**target/plan date, NOT the actual closure date.**

Do NOT read a `Closed` row's date there and report it as "closed on <date>".
Example (2026-08-17): PRR-COM-06, PRR-CON-03, PRR-DES-06 all showed `2026-08-15`
in that column — which looks like last week — but `git log -S` on `risks.json`
proved all three were actually set to Closed on **27-Jul-2026** (commit `57e5a32`).
The `2026-08-15` value is a plan target, not a closure record.

## Authoritative source

`06_Risk_System/risks.json` is the source of truth; `risk_register.md` and the
webapp are generated mirrors of it. `target_close` in the JSON is likewise a plan
date. For status-transition timing, trust the **git history of `risks.json`**, not
the register's date column.

## Method 1 — Current Closed set + when each flipped

```bash
cd /Users/mohamedessa/aseer-museum-pm

# which risks are Closed right now (risks.json is SoT)
git show HEAD:06_Risk_System/risks.json | python3 -c "import json,sys; d=json.load(sys.stdin); r=d if isinstance(d,list) else d.get('risks',[]); print([x.get('id') for x in r if x.get('status')=='Closed'])"

# when did a given id first become Closed
git log --oneline -S'<RISK_ID>' -- 06_Risk_System/risks.json
git show -s --format='%h %ci %s' <COMMIT>   # gives the date of the flipping commit
```

## Method 2 — "Anything closed this week?"

Diff the `Closed` id-set across every commit in the window:

```bash
# For each commit in the last N days touching risks.json, list its Closed ids.
# If the set is identical across all of them, NOTHING closed — report that plainly.
for c in <commits>; do
  git show $c:06_Risk_System/risks.json 2>/dev/null | python3 -c "import json,sys; d=json.load(sys.stdin); r=d if isinstance(d,list) else d.get('risks',[]); print('$c','closed:',[x.get('id') for x in r if x.get('status')=='Closed'])"
done
```

Identical `closed:` lists across the week ⇒ no closure activity. Do not fabricate
a closure because a `Target Close` date fell inside the week.

## Report style for this user

Lead with a plain "نعم/لا" (or EN equivalent) answer to the asked question
(e.g. "did any risk close this week?" → "No, none closed this week."), then a
small table of the currently-Closed risks with their ACTUAL closure dates and the
note that the register's `Target Close` column is a plan date.
