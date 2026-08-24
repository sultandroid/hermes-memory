# Internal Review of a Specialist Design-Review Report (before CG)

When a specialist/consultant (e.g. an acoustic engineer) sends a **design-review report** (e.g. "Loudspeaker Coverage and Speech Intelligibility Review", AC-RPT-001) for the Technical Office to pass to CG, do NOT just forward it. Run this triage first. The report may be technically correct yet **not submittable** — and worse, it may expose a scope gap in the responsible designer that, if it reaches CG, triggers another Code C/D.

## The three-part triage

### 1. Technical soundness (is the engineering right?)
- Re-verify the arithmetic independently. For an acoustic/level report: check every row's **headroom = max dB(A) − programme level** (e.g. 110 = 78+32). Zero arithmetic errors = consistent.
- Check the results table against the figures (coverage uniformity, STI, headroom charts) — they must match.
- Flag presentation defects that undermine credibility even when the numbers are right:
  - A "zone served" / "coverage" column showing **>100%** (e.g. 146%) reads as impossible. It is really *array-footprint ÷ room area*, not a served fraction — must be relabelled or it invites rejection.
  - A space showing both "146% zone served" AND "12% within ±3 dB uniformity" looks contradictory; it is reconcilable (broadband throw vs 4 kHz uniformity are different metrics) but needs one clarifying line.

### 2. Formal submittability (is the report a submittable document?)
A technically-correct report can still be rejected/ignored by CG if it is not a formal deliverable. Check for:
- **Single-engineer, no independent check** — report says "not independently checked / personal commission / not part of any consultancy appointment." CG will not accept this as a compliance submission.
- **Criteria not yet approved** — the pass/fail targets (STI, RT) may be "open under RFI-0xx / NOT YET APPROVED." If the report judges against a *proposal*, CG can dismiss the whole thing ("what did you measure against?"). Either get the criteria approved first, or remove the "not approved" caveat from the CG-facing version.
- **Signature block** — designer + reviewer + checker. CRITICAL: only add a reviewer's name if someone actually read the calculations. Adding a name without a real review is professional misconduct.
- **Assumptions stated** (ceiling heights, absorption coefficients, directivity) — good reports state these in a "what is provisional" section. Flag the largest assumption (often ceiling height, which may be on no issued drawing).

### 3. Scope responsibility (who must fix it — the decisive step)
Before deciding what to do with the report, check the **responsible designer's SOW** to determine whether they must **produce** the design or merely **evaluate** it. This reframes the report entirely.

- Look up the specialist's SOW / scope README in the repo (e.g. `03_Scope/Rawasin_AV_IT/README.md`, `03_Plans/15_Subcontractor_Deliverables/Draft_SOW_RACI/`).
- If the SOW says "Full X design → IFC → install → T&C" (design-produce), then a review finding "39 of 50 spaces carry no loudspeaker" is a **scope gap in the designer's own design**, NOT an open question.
- Consequence: **do NOT submit the report to CG as-is.** Submitting it proves the designer's package is incomplete → same Code D rejection pattern as the prior package ("generic / not coordinated with the project"). Instead route it **internally to the responsible designer** to fix the design first, then the report becomes evidence the design was corrected, not evidence it was deficient.

## Workflow
1. Locate the report (search Outlook by subject; if not found, search OneDrive submittal paths — e.g. `02_Submittals/3.1_DD Doucments AV/Speackers Coverage/`).
2. Extract text (`pdftotext -layout`) and read the full document, not just the summary.
3. Run the three-part triage above.
4. Check the actual submission status in the register (`01_Registers/submittal_register.md`) — is the package the report reviews already under review (U) or already rejected (Code D)? This determines the risk of submitting.
5. Decide: **route internally to the responsible designer to fix** (if it exposes a scope gap) vs **return to the author for formalisation** (if technically right but not submittable) vs **submit** (only if formal AND no scope gap).

## Pitfalls
- **"The report is weak" ≠ "the findings are wrong."** The findings (e.g. G10 fails, 39 spaces unserved) can be correct and important while the document is not submittable. Separate content from form.
- **A review report can be used AGAINST you.** If the package it reviews is already under CG review, submitting a report that documents missing coverage gives CG the evidence to reject it. Route internally first.
- **Don't add a reviewer name without a real review.** A signature block with a name who never read the calcs is fraud.
- **Check the register, not the PDF cover.** A report dated "for review" does not mean the package was submitted. The register status column is ground truth.
- **Rawasin (T2-09) is design-produce, not design-evaluate.** Its SOW is "Full AV design → IFC → install → T&C" (31 zones / 4 floors). A coverage review finding gaps in the AV layout is a Rawasin scope gap, not an open question — route to Rawasin (Eng. Shehab) to fix, don't submit to CG.
