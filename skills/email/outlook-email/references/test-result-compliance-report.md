# Test-Result Submittals (lab reports) — compliance verdict parsing

Pattern (concrete-core example, 2026-08-28): emails from the PM (Muhammad Waris Sultan Khan)
or test labs submitting laboratory test results carry NO A/B/C/D code and often no
"Transmittal"/"Submittal" in the subject (e.g. "Aseer museum - Submission of Concrete Core
Test Results"). They surface in scans only because the sender/folder filter catches them.

## Why they're easy to miss
- Subject keyword filter (Transmittal/RFI/Submittal/Code X/IR-/NCR) does NOT match.
- You need broad senders (Waris/PM) OR folder filter (`Asher Regional Museum`) to catch them.
- `Message_HasAttachment=1` is the real signal — the compliance verdict is in the PDF.

## What to do
1. Extract the attachment (`save` via AppleScript, content-type not image/).
2. `pdftotext -layout` the WHOLE report — the pass/fail line is near the bottom.
3. Read the compliance verdict, not just the numbers.
4. Link to the relevant register risk as EVIDENCE (do not create a new risk or edit
   registers without prior approval — report out first).

## Concrete core report anatomy (SMITS / Saham Al Manar, Abha)
ASTM C42 compressive-strength test on drilled cores — fields at the top carry the
design/specified strength (e.g. 35 MPa) in the "Concrete Design Strength" row; per-core
results and the verdict appear at the bottom:

| Field | Meaning |
|---|---|
| Corrected Compressive Strength, MPa (per core) | individual core result |
| Average Compressive Strength, MPa | mean of cores |
| Average Achieved Strength % | avg ÷ specified ×100 |
| "Applicable Standard Specification" line | acceptance rule, e.g. ACI-318: avg ≥85% of spec AND no single core <75% |
| REMARKS / "(NOT COMPLY)" | explicit fail flag |

**Interpretation rule (ACI-318):** average must be ≥85% of specified strength AND no single
core <75% of specified. 3 cores of 35 MPa spec averaging 20.7 MPa = 59% → **NOT COMPLY**.
This is a structural-integrity signal, not record — flag for structural engineer/CG review
and cite as evidence against the structural-verification/strengthening risk.

## Cross-links seen in practice
- Concrete-core testing ↔ `PRR-SIT-02` / `PRR-DES-07` (structural verification of 1970s
  building; CG mandated executed core testing before BOD approval) and `ZD-0110`/`ZD-0114`
  (Plan for Concrete Core Test Location).
- Core-testing vendor = Smits Labs (Saham Al Manar); a supplier payment action (CR/VAT/bank
  details) often sits open in `00_Status/action_items.md` tied to the same testing.
- Inspection request `IR-0003` bundles material-lab prequalification (PQ-0121 Saham Al Manar,
  CG Code B 17-Jul).

## Rule
For test-result submittals, DO NOT register/modify risks or registers without user approval —
report the compliance verdict + proposed evidence link first. (Matches the standing
"NEVER register/modify any risk without prior user approval" rule.)
