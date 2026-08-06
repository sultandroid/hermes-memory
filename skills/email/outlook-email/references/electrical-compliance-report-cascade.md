# Electrical Compliance & Understanding Report → Register Cascade

Recurring deliverable type on Aseer Museum: the **Compliance & Understanding Report** (produced by Engr. BMR / AEC, the electrical design consultant) submitted under a ZD ref (e.g. `MOC-MUS-ASE-1E0-ZD-0103 Rev.01`). Each Rev is a resubmittal to CG via Aconex (both the email and the Aconex transmittal arrive — the Aconex one has `HasAttachment=0`, treat as notification only).

## What the report contains (and what to extract)

The PDF is a Document Submittal (DS) cover page followed by a per-system compliance summary. It is the authoritative signal for electrical redesign readiness. Key things to read from it:

1. **"ASSESSMENT REPORTS NOT YET RECEIVED" section** — a numbered list of electrical assessment reports the MEP designer still needs (e.g. Substation TR, Standby generator & ATS, LV cables, Motor Control Centers, MDB/SMDB, UPS, Wiring devices, Panelboards).
2. **"PENDING ASSESSMENT REPORTS WITH CODE (C)" section** — systems still in Revise & Resubmit.
3. Per-system status notes that carry hidden risks:
   - **FAS non-compliant with interface requirements** (not interfaced with AHU / elevator / escalator / fire suppression) → fire-safety risk.
   - **10-year-old systems without final engineering recommendation** (e.g. Master Clock) → fit-for-purpose unconfirmed.
   - **Separation mandates** (CCTV separate from IT per SAIS-MOI; telecom separate from CCTV) → security/network design constraint.
   - **Code C systems** (PAVA, CCTV, Telecom, Lighting, DB) block that subsystem's redesign.

## Register cascade (in order)

1. `01_Registers/assessment_evaluation_register.md` — add the new ZD ref + Rev as `Submitted` (awaiting CG), with the Aconex ref from the subject.
2. `01_Registers/risk_register.md` + `06_Risk_System/risks.json` (the SoT) — add ONE consolidated risk for "N assessment reports not received + M systems Code C block electrical redesign" (PRR-MEP category). Keep the MD title block in sync: bump revision (e.g. C13→C14), Total Risks count, and re-derive the Summary rating/status counts from the actual table rows (don't guess — the counts drift).
3. `00_Status/action_items.md` — add chase actions: (a) chase the missing reports with a dated tracker, (b) prioritise the Code C resubmissions, (c) verify FAS interface compliance, (d) coordinate redesign against pending CG codes.
4. `03_Plans/08_Risk/reviews/email_scan_YYYY-MM-DD.md` — archive the scan with the findings.
5. Git commit + push.

## Pitfalls

- **Aconex transmittal email for the same document has `HasAttachment=0`** — skip extraction, log via the subject's Aconex ref. Only extract the email that actually carries the inline PDF.
- **Report may have 2 identical attachments** (same md5 — DS cover + report) — dedupe by md5 before routing.
- **Always re-derive risk_register Summary counts from the table** — after adding a row, recalc Rating and Status counts with a script rather than manually bumping, because the pre-existing counts are often stale.
- **The `deliverables_register.md` under `Technical_Office/` is a noisy auto-generated mirror** — do NOT append assessment rows there; the assessment-specific register is `01_Registers/assessment_evaluation_register.md`.
