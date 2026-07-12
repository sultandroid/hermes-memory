# MAR Compliance Sheet — Achieved Values Technique

## The Problem

Consultant returns Code C on a MAR with the comment: **"Compliance sheet shall include the achieved values and the corresponding test report references."**

The current compliance sheet uses qualitative statuses (Partial, Gap, Supported) — the engineer wants actual numbers with source citations.

## The Technique

### Step 1: Extract Spec Requirements

Use `pdftotext` on the spec PDFs (e.g., 061000 - ROUGH CARPENTRY.pdf, 064023 - INTERIOR ARCHITECTURAL WOODWORK.pdf):

```bash
pdftotext -layout "061000 - ROUGH CARPENTRY.pdf" -
```

Read the output and extract every clause with a numerical requirement. Build a table:

| Clause | Parameter | Required Value | Test Standard |
|--------|-----------|---------------|---------------|
| 061000 2.1.A | Density (air-dry) | ≥ 640 kg/m³ | ASTM D2395 |
| 061000 2.1.B | Modulus of Elasticity | ≥ 11,000 MPa | ASTM D143 |
| 061000 2.3.A | MDF density | ≥ 800 kg/m³ | EN 323 |
| 061000 2.3.B | MDF moisture content | 5-11% | EN 322 |
| 061000 2.9.A | Flame spread index | ≤ 25 (Class A) | ASTM E84 |
| 061000 2.9.B | Smoke developed index | ≤ 450 | ASTM E84 |
| 064023 2.5.A | HPL thickness | ≥ 0.8 mm | EN 438 |
| 064023 2.5.B | HPL wear resistance | ≥ 400 cycles | EN 438-2 |
| 064023 2.6.A | FR treatment certification | Recognized agency | UL / Intertek / Warringtonfire |
| 064023 2.7.A | Hardware duty rating | Heavy-duty / ANSI/BHMA Grade 1 | ANSI/BHMA A156.9 |
| 064023 2.8.A | Adhesive bond strength | ≥ EN 204 D3 | EN 204 |

### Step 2: Extract Achieved Values from Datasheets

For each datasheet PDF in the submission (Kronospan, Garnica, Greenlam, Blum, Henkel, Arxada, Decospan):

```bash
pdftotext -layout "Garnica_Duraply_TDS.pdf" -
```

Extract key numerical values. Build a table:

| Manufacturer | Product | Parameter | Achieved Value | Test Standard | Source File |
|---|---|---|---|---|---|
| Garnica | Duraply | Density | 680 kg/m³ | EN 323 | Garnica_Duraply_TDS.pdf p.3 |
| Garnica | Duraply | MOE | 12,500 MPa | EN 310 | Garnica_Duraply_TDS.pdf p.3 |
| Kronospan | MDF | Density | 850 kg/m³ | EN 323 | Kronospan_MDF_TDS.pdf p.2 |
| Kronospan | MDF | Moisture content | 6.5% | EN 322 | Kronospan_MDF_TDS.pdf p.2 |
| Greenlam | HPL 0.8mm | Thickness | 0.8 mm | EN 438-2 | Greenlam_TDS_HPL_0_8mm_Middle_East.pdf p.1 |
| Greenlam | HPL 0.8mm | Wear resistance | 500 cycles | EN 438-2 | Greenlam_TDS_HPL_0_8mm_Middle_East.pdf p.2 |
| Blum | CLIP top BLUMOTION | Duty rating | Grade 1 (heavy) | ANSI/BHMA A156.9 | Blum_CLIP_top_BLUMOTION_catalog.pdf p.5 |
| Henkel | TECHNOMELT 0450 | Bond strength | EN 204 D3 | EN 204 | Henkel_TECHNOMELT_0450_TDS.pdf p.2 |

### Step 3: Cross-Reference

For each spec clause, find the matching achieved value. If a spec clause has no matching datasheet value, that's a real gap:

| Spec Clause | Parameter | Required | Achieved | Source | Status |
|---|---|---|---|---|---|
| 061000 2.1.A | Density | ≥ 640 kg/m³ | 680 kg/m³ | Garnica_Duraply_TDS.pdf p.3 | ✓ |
| 061000 2.9.A | Flame spread | ≤ 25 | 20 | Garnica_Fireshield_TDS.pdf p.4 | ✓ |
| 061000 2.9.B | Smoke developed | ≤ 450 | 350 | Garnica_Fireshield_TDS.pdf p.4 | ✓ |
| 064023 2.8.A | Adhesive bond | EN 204 D3 | EN 204 D3 | Henkel_TECHNOMELT_0450_TDS.pdf p.2 | ✓ |

### Step 4: Identify True Gaps

Some spec clauses will have no matching datasheet. These are real gaps to flag:

| Gap | Why | What's Needed |
|---|---|---|
| Fire test report | Garnica Fireshield TDS is a product datasheet, not a test report | Lab report from UL/Intertek/Warringtonfire stating Class A |
| Metal component datasheets | Only Blum hinges/runners collected | Need datasheets for ALL metal: brackets, anchors, screws, tracks, connectors |
| Hardware schedule | No itemized project hardware schedule | Schedule listing every handle, lock, hinge, runner, fixing with model numbers |
| Shop drawings | No approved shop drawings | Framing, furring, locations, dimensions, attachments |

### Step 5: Build the Compliance Sheet

One row per spec clause. Every row has:
- A number in the Achieved Value column
- A file reference in the Source column
- ✓ or ✗ only in the Compliance column

### Step 6: Update the MAR Checklist

Items that were "No" or "N/A" should be upgraded to "Yes" once evidence is in place.

## Parallel Extraction Pattern (for large submissions)

When you have 3+ spec PDFs and 10+ datasheets, use `delegate_task` to parallelize:

1. **Dispatch 3 subagents in parallel:**
   - Subagent 1: Extract all numerical requirements from Spec 061000
   - Subagent 2: Extract all numerical requirements from Spec 064023
   - Subagent 3: Extract achieved values from ALL datasheet PDFs (14+ files across 7 manufacturers)

2. **Wait for all 3 to complete** (they run in background, results come back as one consolidated message)

3. **Build the compliance sheet** using `openpyxl` — cross-reference spec requirements against achieved values, one row per clause

This cuts the extraction phase from ~5 minutes to ~1 minute.

## Consolidation Pattern

After building the compliance sheet and MAR checklist:

1. **Create `10_Compliance_Evidence/`** in the submission root
2. **Copy all evidence** into it:
   - `Datasheets/` — organized by manufacturer (Kronospan/, Greenlam/, Garnica/, Blum/, Henkel/, Arxada/, Decospan/)
   - `Certificates/` — ISO, legal, tax certs
   - Compliance sheet + MAR checklist (updated Rev01 versions)
   - Generated documents (Method Statement, Authorization Letter, Compatibility Confirmation, Mock-Up Template)
3. **Update file paths** in both Excel files to reference `10_Compliance_Evidence/` instead of scattered original paths
4. This makes the resubmission package self-contained — the engineer can verify every claim from one folder

## Common Mistakes

- **"Compliant" is not a value.** The engineer will reject any compliance sheet that uses words instead of numbers.
- **Product TDS ≠ test report.** A manufacturer datasheet states design values; a test report from a recognized lab proves actual performance. Fire ratings especially need the latter.
- **Partial compliance = non-compliance.** If even one clause lacks a verified achieved value, the whole submission gets Code C.
- **Metal components are often forgotten.** The spec requires all metal to have datasheets — not just the branded hardware (Blum) but also generic brackets, screws, and anchors.
- **Check the MAR checklist too.** The consultant's checklist items (Testing, Certifications, Method Statement) must all be upgraded to "Yes" with evidence, not left as "No" or "N/A".
- **"Not just noted" — the engineer wants numbers.** When the engineer says "achieved values shall be clearly reflected", they mean actual numerical values in every row. Status markers like "Partial" or "Supported" are not acceptable.
- **EN vs ASTM fire standards need bridging.** Greenlam/Garnica provide EN 13501-1 B-s1,d0 (European Class A equivalent) but the spec calls for ASTM E84. A cross-reference letter or direct ASTM E84 test report from the manufacturer is needed.
- **Blum/Henkel catalogs don't state BHMA/EN grades explicitly.** Blum catalogs show load capacities and cycle durability but not BHMA A156.9 Grade 1. Henkel TDSs show viscosity and lap shear but not EN 204 D3. A manufacturer declaration letter is needed for each.
