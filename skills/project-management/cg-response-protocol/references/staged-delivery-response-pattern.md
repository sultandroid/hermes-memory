# Staged-Delivery Response Pattern (CG demands evidence at the wrong stage)

## The recurring trap

CG frequently returns Code C on a **specification / DD 50% gateway** submittal with comments that demand
**evidence deliverables** — test reports, compliance certificates, manufacturer warranties, mock-ups, third-party
test results — as if they belong in the specification document itself.

This is a **stage confusion**. The correct contractor position:

| Stage | What is due | Who produces it |
|---|---|---|
| Specification (DD 50%) | The *criteria*: standard + performance number (e.g. "NRC ≥ 0.90 per ASTM C423") | Design team / Technical Office |
| Material Approval (MAR) | The *evidence*: test reports, certs, warranties, data sheets | Supplier / manufacturer |
| Pre-installation | Mock-ups, control samples, prototypes | Contractor + supplier on site |

Evidence is **not** the design team's responsibility and is **not** submitted with the specification.

## The response pattern (use in CRS)

For each evidence-demanding comment, respond **"COMPLIED (staged)"** and split the answer:

1. **Embed the criterion** — confirm the specification now *states* the required standard and performance number
   (so it is contractually binding).
2. **Commit the evidence to the correct later stage** — state that test reports / certs / warranties / mock-ups
   will be submitted by the approved suppliers at the Material Approval (MAR) stage per the approved Submission
   Plan and Inspection & Test Plan.

Add a **Stage Alignment Note** section at the end of the CRS that:
- Cites the DMP Stage-Gate Review Schedule (Part 1 Sec 3.4.1) and RIBA Stage Gates (Part 1 Sec 3.4.2).
- States the LOD/gate mapping (50% DD = Stage 4-A, LOD 300–350).
- Explicitly requests CG agreement to staged delivery, so front-loading MAR evidence into DD is rejected as
  premature and inconsistent with the approved DMP.

## Distinguish comment types before drafting

CG comments on a spec submittal fall into three buckets — respond differently to each:

1. **Procedural / routine** (specialist review, discipline coordination, mock-up, warranties) — "Complied",
   route to the named specialist (acoustics → TransOrient, sustainability → Muhammad Fida, etc.).
2. **Technical / substantive** (specific performance numbers, fire ratings, dimensional limits) — "Complied",
   state the exact revision made to the section.
3. **Legal-protection boilerplate** ("approval does not relieve the contractor…", "no variation to price or
   schedule") — "Noted", no revision required. Do NOT treat these as technical comments.

## The one comment that is NOT routine

When CG says a sub-package's review is **"suspended until resubmitted compliant"** (e.g. display cases), that is
a *design disagreement signal*, not a missing-evidence signal. Do NOT mark it "Complied" blindly. Instead:
- Extract that sub-package for a **separate, dedicated resubmission**.
- **Ask CG to confirm the specific design requirements** it must satisfy — "suspended until compliant" is vague
  and you need the exact requirement to resubmit correctly.

## Worked example

`MOC-MUS-ASE-1A0-1G-0012` (Arch DDD Specifications, 50% gateway) — CG Code C, 27-Aug-2026, 10 general + 21
section comments. Full CRS at `02_CG_Responses/1G-0012_Arch_Specs_CRS_Rev01.md`. The 10 general comments were
mostly evidence-demanding (warranties, certs, mock-ups) → answered "Complied (staged)"; the display-case
suspension (G10) was answered "Complied (separate resubmission)" + a request for CG to confirm the specific
design requirements.
