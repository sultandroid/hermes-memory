# Register Reconciliation — Received Document vs Existing Register Entry

When a received submittal's document number conflicts with what a register already says, the **received document is authoritative**. Correct the register and flag the mismatch — do not silently trust the register.

## Core Rule

> The physical/PDF document you hold is ground truth. A register is a derived index and can carry stale or wrong labels (vendor name, discipline, scope, status). When they disagree, the document wins.

## Worked Example (2026-08-10)

- Register (`prequalification_register.md`) listed **PQ-0134 = ICT Security System Integrator — NETGEAR**.
- Received PDF cover sheet: **PQ-0134 = Audio Solutions Supplier — Molitor** (with CG Code C response).
- Resolution: corrected the register to Molitor/Audio, added the CG Code C rejection reasons, and flagged the discrepancy in the row notes.

## Steps

1. **Extract the cover-sheet doc number + title first** — the cover sheet (not the body) defines the submittal identity.
2. **Grep the register for that doc number** before assuming the entry is correct.
3. **If the register entry conflicts with the received doc**, correct the register to match the document. Note the correction in the row (e.g. "corrected from NETGEAR").
4. **Update ALL registers that track the same submittal** — PQ register, submittal register, and any discipline-specific tracker. A single submittal can touch 3+ registers.
5. **Flag the mismatch in the row notes** so a future reader knows the register was corrected and why.

## CG Comment-Sheet Mismatch Pitfall

CG response PDFs sometimes carry a **comment sheet that references a DIFFERENT submittal** than the cover sheet. In this session, the CG comments page referenced **PQ-0133 (Network/Netgear)** while the cover sheet was **PQ-0134 (Audio/Molitor)**.

- Always compare the comment sheet's submittal reference against the cover sheet's.
- If they differ, **flag it** ("verify correct comment sheet applies") rather than assuming the comments belong to the received submittal.
- Do not apply the comments blindly — the wrong comment sheet could send you chasing the wrong vendor's fixes.

## Multi-Register Intake Pattern

One incoming document often updates several files. For a submittal + CG response, update:
- `01_Registers/prequalification_register.md` (vendor PQ status)
- `01_Registers/submittal_register.md` (submittal status)
- `01_Registers/change_register.md` (if it drives a variation)
- `00_Status/action_items.md` (follow-up actions)
- Discipline README (e.g. `03_Scope/AD_Engineering/README.md`) if it affects a consultant's coordination status
- `01_Registers/meeting_minutes_register.md` (if it's a meeting/workshop)

Update the `last_updated` frontmatter on every file touched. Commit with a dated message (YYYY-MM-DD) listing the doc numbers ingested.
