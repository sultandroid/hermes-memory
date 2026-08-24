---
name: audio-acoustic-design-review
description: Audit loudspeaker coverage, speech intelligibility (STI), and acoustic design-review documents as an Audio/AV Engineer. Triggered by "audit this [speaker/AV/acoustic/loudspeaker] report", "review the AV design", "check speaker coverage".
tags:
  - audio
  - acoustics
  - AV
  - loudspeaker
  - STI
  - engineering-review
  - aseer-museum
---

# Audio / Acoustic Design Review (as Audio Engineer)

Audit engineering review reports covering loudspeaker coverage, speech intelligibility (STI), reverberation, and AV sound-system design — chiefly for Aseer Museum / Samaya museum projects.

## Trigger
- "audit the file as Audio Engineer" / "review as [acoustic/AV] engineer"
- Loudspeaker coverage, speech intelligibility, or acoustic report review
- AV package review (AV-12xx drawings, PA/VA, sound systems)

## First: locate the file
The user often references a document without giving a path. Search in this order:
1. **Outlook SQLite** by subject/preview keywords (`Speaker`, `Coverage`, `Acoustic`, `QUO-8715`).
2. **OneDrive submittal path** — the Aseer AV/acoustic files live at
   `OneDrive-SAMAYAINVESTMENT/Samaya/Technical Office/Bim Unit/Aseer-Museum/02_Submittals/3.1_DD Doucments AV/` (note the typo "Doucments" and per-item subfolders like `Speackers Coverage/Speaker Coverage.pdf`).
3. Repo register/tracker mentions (e.g. `Technical_Office/Submission_Tracker/AV_IT/AV_Stage04_Plan_*.md` lists owner + status of each AV deliverable).
Exact-subject misses in Outlook are normal — the review file is often a OneDrive submittal copy with a different title.

## Audit methodology (Audio Engineer lens)
1. **Establish the document's status & authority first.** Read the cover: is it "for review" (R01), a "personal commission", single-engineer, un-checked? A self-declared *non-submittable* doc is decision-support, NOT compliance — say so up front. Don't over-credential it.
2. **Verify target criteria are APPROVED.** Pass/fail verdicts are only as good as the target spec. If the STI target (e.g. MEM-001 open under project RFI-013/010) is "NOT YET APPROVED", the verdicts are against a *proposal*, not an agreed spec — flag this or CG will dismiss the findings.
3. **Independence check.** "not independently checked", "single-engineer", "validated against limiting cases to ±0.015 STI", directivity "modelled from graph-only polar data", ceiling heights "assumed". List the largest assumption (usually ceiling height) and its effect.
4. **Numerical consistency — recompute derived columns.** The highest-value check: *headroom = max dB(A) − programme level* for every space row. E.g. gallery 107 = 75+32, workshop 110 = 78+32, retail 110 = 78+32. Every row must reconcile. Zero arithmetic error = the report's numbers are internally consistent.
5. **Cross-check the results table against the figures** (STI chart vs table; headroom bars vs table) so no figure/table drift.
6. **Sanity-flag physically-impossible values.** A "Zone served" or coverage metric >100% is a *ratio* (array-footprint ÷ room area), not a fraction — it reads as impossible and invites rejection. Call the mislabel out and propose a relabel.

## Standard findings this user's reviews surface (Aseer Museum)
- **Ceiling treatment is usually the critical path, not the loudspeakers.** Re-run without scheduled acoustic treatment collapses STI 0.59–0.75 → 0.34–0.42 ("Poor") and RT to 3.0–5.3 s; no loudspeaker layout bridges it. If any absorption is value-engineered out, the intelligibility case goes with it.
- **G10 untracked room** — if the BOQ leaves one gallery untreated ("already compliant" with no evidence), it fails on two independent criteria (RT + STI) in the same room. Demand evidence or bring it into scope.
- **Un-served spaces** — compare labelled spaces vs loudspeaker-bearing spaces; a public-space gap may or may not be covered by a separate PA/voice-alarm package (ask, don't assume).
- **Level/power over-spec** — 24–38 dB headroom on the 30 W tap can push 110 dB(A) in a small room (exposure, not margin). A lower tap (e.g. 15 W) halves connected load (1710→855 W) and removes ~1070 W amplifier plant; take remaining margin in DSP gain.
- **EN 54-24 / SBC 801**: standard PA products (e.g. Yamaha VXC6/VXC8) may not be EN 54-24 certified; if occupant load ≥1 000 (Group A) the -VA variant is required, which changes sensitivity (≈−1 dB) and depth (≈+36 mm) — procurement-critical.
- **Double-spec / document conflict**: same unit specified as two different products across drawings vs concept BOQ (e.g. flush-ceiling VXC8 vs surface-mount VXS8), and weather-rating of semi-external units. Must resolve before procurement.

## Deliverable shape (match user preference)
- Lead with a **Verdict** (sound / not submittable-as-is / needs X).
- **Correct & important** findings table.
- **Consistency check — PASSED** with the recomputed evidence.
- **Engineering flaws / corrections** numbered.
- **Priority actions** for the discipline lead.
- **Bottom line**: engineering right vs what blocks submittal (presentation mislabels, unapproved targets, independence).

## Pitfalls
- `pdftotext -layout` on the PDF; figures are raster — render `pdftoppm -f N -l N -r 80 -png` and use vision to verify chart content if the model lacks native vision.
- PDF may be `python-docx`-generated (author metadata "python-docx") — a Word round-trip, so check `pdfinfo` metadata and page count before trusting pagination.
- Arabic content → translate silently (project hard rule, English only in output).
