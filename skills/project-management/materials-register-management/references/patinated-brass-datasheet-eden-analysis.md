# EDEN-DESIGN Patinated Brass — Datasheet Risk Analysis

## Source Document

`/Users/mohamedessa/Downloads/datasheet-patination.pdf` (provided 2026-07-14 by user)
Author: Ahmed Metwally (Glasbau Hahn), created 2026-04-10

## Verbatim Datasheet Content

```
EDEN -DESIGN-PANELS Metal Matting/Coloring
as cut pieces from brass MS63
CuZn37, stress-free, custom-planed, ARCHITECTURAL QUALITY

Surface EDEN -CD/CC "RANDOM-CLOUDY" BURNISHED, CLEAR COAT SEALED

SAMPLE - CUSTOMER SAMPLE
4 x DIN A4 (200x300) t= 2.0mm

CUT EDGES BURNISHED AND LACQUERED!!!!

This is a randomly generated surface finish. The final result will differ from this sample. Therefore,
the final appearance is not a basis for subsequent complaints.

With chemically darkened non-ferrous metals, slight color variations may occur within a single piece
and from batch to batch. These color variations are due to the material's inherent properties and do
not constitute grounds for a complaint.

Please refer to our care instructions and pass them on to your customers.
```

## Key Disclaimers Extracted

| # | Verbatim Quote | Risk Type | Severity |
|---|---------------|-----------|----------|
| 1 | "Randomly generated surface finish" | Finish consistency | 🔴 Critical |
| 2 | "Final result will differ from this sample" | Sample-to-production mismatch | 🔴 Critical |
| 3 | "Final appearance is not a basis for subsequent complaints" | Legal limitation of liability | 🔴 Critical |
| 4 | "Slight color variations may occur within a single piece and from batch to batch" | Batch variation | 🟠 High |
| 5 | "Color variations...do not constitute grounds for a complaint" | Legal limitation of liability | 🔴 Critical |
| 6 | "Chemically darkened non-ferrous metals" | Process type (batch chemical, not production line) | 🟠 High |

## Risk Register Mappings

### 1. Oddy Testing Risk — Batch Chemical Process

**Issue:** The surface is "chemically darkened" — a wet chemical patination process. Unlike production-line coating (PVD, powder coat), each batch is a unique chemical reaction. An Oddy pass on one batch does not guarantee the next batch passes.

**Impact:** If Oddy testing takes 3-4 months per cycle, and the first batch passes but production batches fail, the re-test delay is 3-4 months. This directly threatens the programme.

**Register target:** New risk in DDR under Showcases (DDR-SHC) or a new Metal/Material category.

### 2. Finish Matching Risk — Cross-Application Variation

**Issue:** The same EDEN CD/CC patination process may be specified for:
- Showcases (via Glasbau Hahn)
- Doors / door hardware
- Cladding / railings / architectural metalwork

The datasheet explicitly states each piece and each batch will differ. If different fabricators (Glasbau Hahn for showcases + another for doors) use the same EDEN process, the finish WILL NOT MATCH.

**Impact:** CG/MoC rejects installations where patinated brass components don't match. Remediation cost is high (remove, re-fabricate, re-install).

**Register target:** Existing PRR-PRC-02 (showcase procurement) scope expansion, or new PRR under Procurement.

### 3. Supplier Liability Limitation Risk

**Issue:** EDEN-DESIGN's datasheet explicitly states:
- "Final appearance is not a basis for subsequent complaints"
- "Color variations...do not constitute grounds for a complaint"

This means if CG rejects the delivered material due to appearance variation (which is guaranteed to occur), Samaya has no contractual recourse against EDEN-DESIGN.

**Impact:** Samaya bears the full cost of replacement if CG rejects. No claim-back possible.

**Register target:** New PRR under Commercial (PRR-COM) or Procurement.

## Recommended Mattigation

### Immediate (before procurement)

- Disclose the EDEN disclaimer language to CG explicitly — do not hide it
- Request CG to approve a RANGE of acceptable appearance, not a single sample
- Lock the colour/finish range in the specification as "EDEN CD/CC medium range" rather than matching a specific sample
- Require a first-article inspection before bulk production release

### Parallel (risk mitigation)

- Develop PVD-coated patinated brass effect from local KSA suppliers as backup
- If PVD passes Oddy and CG approval, it eliminates the batch-variation risk (PVD is production-line controlled)
- Use the datasheet's own disclaimers as justification: "the supplier themselves acknowledge this finish cannot be replicated consistently"

### Contractual

- Include a letter from EDEN-DESIGN accepting a defined colour range and minimum standards
- Ensure the procurement contract with the fabricator (Glasbau Hahn for showcases, others for doors/cladding) requires them to manage the supplier and accept returns if finish is outside the agreed range
- Do not accept EDEN's disclaimer as-is — negotiate a minimum acceptance criteria clause

## Cross-References

- Material Submittal Register: MA-0007 (Patinated Brass — Code C, resubmission pending)
- Action Items: M14-3.2 (Patinated brass sample NOT approved — attach certifications)
- Supplier: EDEN-DESIGN-PANELS (via Glasbau Hahn procurement)
- Application: Showcase metalwork, doors, cladding, architectural metal
