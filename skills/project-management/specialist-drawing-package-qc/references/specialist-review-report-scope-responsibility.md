# Specialist Review Report — Determine Design Ownership Before Submitting to CG

When a specialist (acoustic, AV, lighting, etc.) sends a **review/assessment report** and the user
asks "should I submit this to the consultant (CG)?" — the FIRST question is not "is the report
good?" but **"who owns the design being reviewed?"**

## The core rule

- If the specialist is the **design owner** (their SOW says they produce the design), then their
  "review" is **internal QC of their own work**. A report that finds gaps is EVIDENCE THE DESIGN IS
  DEFICIENT. Submitting it to CG proves the deficiency → risks a Code C/D on the package it reviews.
  → Route it back to the specialist to FIX the design first, then it becomes evidence the design
    was corrected, not that it was wrong.
- If the specialist is an **independent reviewer** (no design responsibility), the report is a
  submittable deliverable and can go to CG as-is (after formalisation).

## How to determine design ownership (evidence-first)

1. **Read the specialist's SOW / scope file.** Look for "design & delivery", "Full X design→IFC→install→T&C",
   "design development (50%→90%→100%)". That language = design owner.
2. **Check the drawing code prefix** on the reviewed drawings. e.g. `MOC-ASE-AV-TAV-...-DDD-1230/1251/1254`
   — the `TAV` (Theatre AV) series belongs to the AV designer. Match it to the specialist register.
3. **Check the specialist register** (`Technical_Office/Specialist_Management/specialist_register.md`)
   for who is appointed as the AV/design lead and their scope.
4. **Check who submitted the package** the report reviews (e.g. `1E0-1G-0001` submitted by Eng. Shihab/Rawasin).

## Worked example (Aseer Museum, 2026-08-24)

- Acoustic engineer sent `AC-RPT-001 Rev R01` "Loudspeaker Coverage and Speech Intelligibility —
  Review of the Stage 4 AV layout" (12pp), reviewing AV-1230/1231/1232/1233/1250/1251/1254 Rev00.
- Findings: 10/11 spaces meet STI target; **G10 fails** (untreated ceiling, RT 3.39s vs 0.9–1.5 target,
  STI 0.38); **39 of 50 labelled spaces carry no loudspeaker**; G9/G13 partial coverage; 24–38 dB
  level headroom (over-specified); VXC6/VXC8 not EN 54-24 certified; terrace double-spec VXC8 vs VXS8.
- **Design owner = Rawasin** (Samaya sister co) via DHD Services Ltd (UK). SOW-01: "Full AV
  design→IFC→install→T&C". Rawasin submitted the reviewed package (1E0-1G-0001, 06-Jul).
- **Conclusion:** the report is internal QC of Rawasin's own design. The 39 un-served spaces + G10
  are Rawasin design gaps. Do NOT submit to CG (would prove the AV DD Part I is deficient — same
  reason Part II 1E0-1G-0002 was already Code D "generic AV guidance, not coordinated project design").
  → Send to Rawasin (Eng. Shihab) to fix the design first.

## Report formalisation checklist (if it IS to be submitted)

A single-engineer "personal commission" report is NOT a formal deliverable. Before CG submission:
- **Criteria must be approved.** If the report's pass/fail targets (STI, RT) are "NOT YET APPROVED —
  open under RFI-xxx", CG can dismiss the whole report. Either get the criteria approved or remove
  the "not approved" caveat from the submitted version.
- **Independent check.** Single-engineer, un-checked output is not a compliance submission. Add a
  real reviewer who actually reads the calcs (not just a name block).
- **Fix presentation flaws.** e.g. "Zone served" values >100% (G10 146%) read as impossible — relabel
  as array/room-area ratio or explain the metric.
- **Verify arithmetic.** Spot-check headroom = max dB(A) − programme level across all rows.

## Pitfall — T2 allocation code inconsistency

The repo may disagree on a specialist's T2 code (e.g. Rawasin listed as T2-05 "AV Hardware" in the
specialist register but T2-09 "AV/IT/interactives" in the risk register). Doesn't change the
design-ownership decision, but confirm the correct T2 code from the allocation table before writing
a formal letter to the specialist.
