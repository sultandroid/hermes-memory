# Compliance Sheet Fill Pattern — Outline Enterprise Rev02

## Context

Project 010 (Tqanny) — Outline Enterprise woodwork submission for KKIA Concourse A.
Engineer provided their own compliance Excel format (064023 + 061000). Rev02 brought new datasheets from the Ola team.

## Engineer's Format

Both `064023 - INTERIOR ARCHITECTURAL WOODWORK.xlsx` and `061000 - ROUGH CARPENTRY.xlsx` have:
- Spec text pre-filled in the Specifications column (257 lines for 064023, 183 for 061000)
- Empty Manufacturer/Supplier Statement, Compliance, and Remarks columns
- Header block with project name, manufacturer, supplier, date, discipline

## New Evidence from Rev02

| File | What it provides | Spec clauses addressed |
|------|-----------------|----------------------|
| Verdo FR MDF TDS | Density 800.8, MOR 29.5, MOE 2923, IB 1.05, TS 7.41%, Screw F 1010/E 845, NAUF | 064023 2.5.B.1, 061000 2.3.A |
| Verdo FR Class B (ASTM E84) | FSI 35, SDI 20 — **Class B** | 064023 1.4.E, 2.6.C, 061000 2.9.A.1 |
| Verdo TVOC Test | TVOC <0.01 mg/m³, Formaldehyde ND | 064023 2.5.B.1.b.2.b |
| UF Test Report | Nil urea formaldehyde (NAUF) | 064023 2.5.B.1.b.2.b, 061000 2.1.D |
| Ritver PB209IT (PU Sealer FR) | BS 476 Part 7 Class 1, Low VOC 94 g/l | 064023 1.4.E (alternative path) |
| Ritver PT29X0IT (PU Topcoat FR) | TS 19 Class 0 / BS Class 1 | 064023 1.4.E (alternative path) |
| Ritver Approvals PDF | Diriyah project submittal (not KKIA) | Shows product was approved elsewhere |
| SS 304 sheet 2.0mm | Image-based PDF — no extractable text | MAR Comment 2 (metal components) |
| Häfele Loox5 LED strip | Lighting product — **not relevant** | N/A |
| Shop Drawing | Submitted | MAR Item 6 |

## Critical Finding: Fire Class Gap

**Spec requires:** Class A (FSI ≤25, SDI ≤450) per ASTM E84 (064023 1.4.E, 2.6.C, 061000 2.9.A.1)

**Verdo FR MDF provides:** FSI 35, SDI 20 — **Class B**, not Class A.

**However**, the spec also says (064023 2.6.C.1): *"Wood products tested to BS 476 and satisfying Class 0 shall also be accepted."*

**Ritver coatings** are BS 476 Class 1 / TS 19 Class 0, so the coating system may satisfy the alternative path.

**Compliance marking:** △ (Partial) — not ✓. Note the alternative acceptance path in Remarks.

## Data Availability Summary

| Category | Status |
|----------|--------|
| MDF physical properties | ✓ All covered by Verdo TDS |
| Formaldehyde (NAUF) | ✓ Confirmed by test report |
| Fire test (ASTM E84 Class A) | ⚠️ Verdo is Class B (FSI 35). Ritver coatings provide BS 476 Class 0 alternative |
| Metal components (SS 304) | ⚠️ PDF is image-only, need visual check |
| Shop drawing | ✓ Submitted |
| Lighting (Häfele LED) | ❌ Not relevant to woodwork submission |

## Key Rules Applied

1. **Fill their format, don't create new** — Engineer's Excel is the authoritative compliance sheet
2. **Only fill 3 columns** — Statement, Compliance, Remarks. Never modify spec text.
3. **Check actual numbers against spec** — don't assume "datasheet exists = compliant"
4. **Fire class mismatch is the most common gap** — Class B ≠ Class A, even if both are "fire rated"
5. **Irrelevant datasheets happen** — exclude them, don't force-fit into compliance mapping
6. **Image-only PDFs** — note as unverifiable, don't invent values
