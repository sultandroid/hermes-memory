# Aseer Register Update Cascade (from email bodies)

When reading Aseer project emails (bodies + attachments) and updating registers, apply
updates in this order — submittal register first (source of truth), then derived registers,
then action items. This prevents stale references.

## Registers to update per email type

| Email content | Register(s) in `~/aseer-museum-pm/` |
|---|---|
| CG response (A/B/C/D) on a submittal | `01_Registers/submittal_register.md` (code + date per doc ref ZD/1G/PQ) |
| PQ (prequalification) response | `01_Registers/prequalification_register.md` (PQ codes) |
| Letter (LT-*) | `01_Registers/letters_register.md` |
| Invoice (INV-*) | `01_Registers/invoice_register.md` |
| Site Instruction (SI-*) | `01_Registers/si_register.md` |
| Safety Observation (SOR-*) | `01_Registers/sor_register.md` |
| Specialist package status | `01_Registers/subcontractor_package_register.md` |
| Any new action / follow-up | `00_Status/action_items.md` (owner + due + source) |

## Key pitfalls when editing registers

- **Check the register already has the row before adding.** Many refs (PQ-0145/146,
  ZD-0108/109, ZD-0078, ZD-0086, SI-001, SOR-003) were already logged by prior scans.
  `grep -n "<REF>" 01_Registers/<register>.md` first; only append/update if absent or changed.
- **`patch` on duplicate rows fails.** Some registers (e.g. `assessment_evaluation_register.md`)
  contain the same block twice (`||`- and `|||`-prefixed). Use a unique anchor with enough
  surrounding context, or a Python script inserting after the FIRST occurrence only.
- **`patch replace_all=true` creates duplicate rows.** Never use it on table rows.
- **SOR closeouts can be PARTIAL.** A single SOR may have multiple observation items, only
  some resolved. Read the closeout PDF and check each numbered item before writing "Closed".
  (SOR-013: item 3 closed, items 1-2 still In Progress.)
- **Zamzam emails (Mohamed Habib, ZAM-NWC prefix) are a SEPARATE project.** Do NOT log them
  in Aseer registers — entity isolation. Skip them.
- **Aconex transmittal notifications** (sender `Aconex Notification`) are CDE syncs, not new
  items — reference-only, no register row unless the underlying doc is genuinely new.

## Commit cadence

Commit each batch of ~10 emails:
```bash
cd ~/aseer-museum-pm
git add -A 01_Registers/ 00_Status/
git commit -m "Email batch N (MMM-DD): <summary of key changes> - YYYY-MM-DD"
```
The repo has a post-commit hook that regenerates `06_Risk_System/webapp/src/index.html` —
leave that auto-generated file dirty; don't commit it. Only commit your register/action changes.
