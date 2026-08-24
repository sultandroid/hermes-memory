---
name: specialist-drawing-package-qc
description: "QC specialist design-drawing submittal packages (lighting, AV, arch plans/elevations/sections) before CG submission. Register reconciliation, per-sheet title-block audit, CAD source vs plotted PDF handling, and drawing-type gap detection."
tags:
  - qc
  - submittal
  - drawing
  - design
  - lighting
  - specialist
  - title-block
---

# Specialist Drawing Package QC

Use when a design specialist (ZNA lighting, NRS arch, Rawasin AV, etc.) delivers a drawing package (plans, elevations, layouts) and the user asks to "QC it" / "check this package" / "is it ready to submit" before it goes to CG. Also use when a specialist sends a **review/assessment report** (acoustic, AV coverage, etc.) and the user asks whether to submit it to CG — see `references/specialist-review-report-scope-responsibility.md` for the design-ownership check that decides whether the report is a submittable deliverable or internal QC evidence of a design gap.

Pairs with `cg-submittal-review-checklist` (the full pre-submission gate). This skill covers the drawing-specific dimension that checklist's design section (B3) references but does not detail.

## Package anatomy — PDFs vs CAD zips

A specialist often ships both:

| File | Role | QC treatment |
|------|------|--------------|
| **PDFs** | The actual plotted submittal CG reviews | QC these — the deliverable |
| **DWG transmittal zips** (AutoCAD `- Standard.zip`) | CAD source files backing the PDFs | NOT separate deliverables. Use them only as evidence of the coordination baseline |

**Pitfall (user-corrected):** Do not list CAD zips as extra deliverables or count them in the package inventory. When a zip's role is ambiguous, confirm with the user — they will correct you if you treat source as a deliverable.

## Step 1 — Reconcile against the register (drawing-set gap check)

Map the submitted drawings to the register's expected deliverable set per gate. The gap is by drawing **TYPE**, not just floor spread.

Example — lighting register (50% gate):
- `L-D-P-001` 50% Lighting Plan
- `L-D-E-001` 50% Lighting Elevations
- later gates: 90% complete plan/elevations + fixture cut sheets; 100% final; IFC; AFC; as-built

A package that ships **plans only** (no elevations/sections) is missing `L-D-E-001` — a gap even with complete floor coverage.

## Step 2 — Per-sheet title-block audit (whole package in one pass)

Scan EVERY sheet's title block, not one representative sheet. Real failure found in a ZNA lighting package:
- One sheet `LGF_HL_01` = **V2**, all others **V0/V1** → mixed revisions in a single "issue".
- One sheet `GF_LL` V0 dated **21/01/2025** (19 months stale) vs the rest current.
- Checker initials (DK, BN) present but **no Samaya QA/QC gate**.
- `Logo` + `Stamp.png` in the CAD zip — verify the stamp actually renders on the plotted PDF (often it does not).

Mixed revisions + a stale date in one package = automatic CG format rejection. Flag every inconsistency across the whole package, not per sheet.

## Step 3 — Internal codes vs project numbering

Specialist output filenames are internal (e.g. `ZNA3297_LG002_{FL}_LL/HL_01`). Verify they reconcile to the project submittal numbering (`MOC-MUS-ASE-*`), even when the DWG XREFs are already project-coded.

Base-drawing XREF convention observed (project-coded): `MOC-ASE-AR-ARC-{BF|LGF|GF|1F}-DDD-1200/01/02/03.dwg` — floor code + drawing-series code in the XREF name.

If CG expects project numbers on the submittal, re-number the output filenames to the register format and add a cover/transmittal.

## Step 4 — Standard design-drawing flags

| Flag | Source |
|------|--------|
| Missing drawing TYPE (plans yes, elevations/sections no) | register reconciliation |
| Mixed revisions / stale dates across sheets in one package | title-block audit |
| Specialist internal filename codes not project-conformant | numbering |
| No package cover/transmittal (doc ref, rev, supersedes, references) | CG comment 6 |
| No QA/QC sign-off (checker initials ≠ Samaya QA gate) | CG comment 6; LL-017/18 |
| No design-lead (NRS) review attached for specialist deliverables | LL-007 |
| Cross-discipline coordination notes absent (lighting ↔ MEP/AV/arch) | scope + A4 |
| Copyright wording ("property of [specialist]") on a project deliverable | flag for acceptability |

## Output

Present as a table: `# | Issue | Detail` split into 🔴 Critical (blocks submission) and 🟡 Advisory, then a bottom line: READY / NOT READY with the specific fixes required.

Not ready until: project-numbered filenames + cover/transmittal; revisions and dates aligned across all sheets; missing drawing types added; QA/QC sign-off; stamp confirmed on the plots.

## Related
- `cg-submittal-review-checklist` — universal pre-submission checklist (A0 doc control, B type-specific, C reviewer, D closure gate). This skill is the drawing-package specialization of its Section B3.
- `references/zna-lighting-qc-example.md` — worked example: the ZNA 50% Lighting package review (per-sheet title-block findings, register reconciliation, CAD XREF baselines).
