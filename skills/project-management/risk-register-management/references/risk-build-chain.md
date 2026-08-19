# Risk Register Sync Chain (risks.json → MD → Webapp → Excel snapshot)

The Aseer Museum risk register has a **strict one-way build chain**. Edit the correct source
or the changes get overwritten on the next build.

## Source of truth = risks.json (NOT risk_register.md)

`06_Risk_System/risks.json` is the master. `risk_register.md` is **generated** from it.

- **WRONG:** editing `01_Registers/risk_register.md` directly — `risk_sync.py` will overwrite it.
- **RIGHT:** edit `risks.json`, then regenerate everything below.

## Full rebuild chain (run in this order)

```bash
cd ~/aseer-museum-pm/06_Risk_System

# 1. Regenerate the markdown register from JSON (JSON → MD)
python3 risk_sync.py
#   -> 01_Registers/risk_register.md

# 2. Rebuild the webapp PRR page (reads risks.json, auto-discovers latest snapshot)
cd webapp && python3 build_risk.py
#   -> webapp/src/index.html (self-contained, N risks, rev CX)

# 3. Bump + regenerate Excel snapshots (per register)
python3 build_snapshots.py --bump
#   -> src/EXP-RISK-PRR-YYYY-NNN_RevC<rev>_ACTIVE.xlsx
#   -> src/DDR/EXP-RISK-DDR-... , src/HSE/EXP-RISK-HSE-...
```

## Risk JSON schema (key fields)

`id, category, title, cause, event, consequence, probability, severity, score,
rating, status, owner, target_close, created, last_reviewed, treatment_file,
evidence[], response_action, actions[{id,text,owner,due,status,evidence}],
history[{date,action,by,note}], diagram{fishbone}, action_due`

When editing an existing risk: update `cause`/`response_action`/`status`, set
`last_reviewed` to today, and **append a `history` entry** documenting the change
so the audit trail is preserved.

## Excel snapshot conventions

- `build_snapshots.py` increments a `snapshot_counter.json` per register
  (`PRR`/`DDR`/`HSE`).
- Snapshot file naming: `EXP-RISK-<REG>-<YEAR>-<NNN>_Rev<C# >_ACTIVE.xlsx`.
- `build_risk.py` **auto-discovers** the latest `EXP-RISK-PRR-2026-*_ACTIVE.xlsx`
  via `glob`, so it picks up the new snapshot automatically on rebuild.
- **Excel snapshots are gitignored** (binaries stay in OneDrive per AGENTS.md).
  Commit only the JSON, the regenerated MD, `webapp/src/index.html`, and
  `snapshot_counter.json`.

## Pitfall — editing MD directly

If you patch `risk_register.md` by hand and then run `risk_sync.py`, your manual
edits are silently lost. Always make the change in `risks.json` first. The only
exception is purely cosmetic/formatting tweaks that don't come from the JSON.
