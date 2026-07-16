# Compliance Sheet Filling (Material Submittals)

## When the Engineer provides their own format

- **Use their format.** Do not create a new compliance sheet. The Engineer's Excel file already has the spec clauses written in. Fill the empty columns (Manufacturer/Supplier Statement, Compliance, Remarks).
- **Do not modify the spec text.** The Engineer's sheet has the full spec clauses — leave them as-is.

## Status values — plain text, no symbols

| Wrong | Right |
|-------|-------|
| ✓ / △ / — | Compliant / Partial / Pending |
| "Exceeds minimum by 20%" | "Exceeds minimum" |
| "Well within limit" | "Within limit" |
| "Standard industry practice" | Just state the fact |

## Manufacturer/Supplier Statement column

Write actual achieved values with test standard and source file. Pattern:

> [Product]: [value] per [test standard]. [Source file reference].

Example:
> Verdo FR MDF: 800.80 kg/m3 per ASTM D1037-12(2020). Verdo FR MDF TDS.

## Compliance column

Three values only:
- **Compliant** — achieved value meets or exceeds spec
- **Partial** — value available but standard differs, or manufacturer declaration still needed
- **Pending** — to be confirmed at shop drawing / material selection stage

## Remarks column

Short factual note. No hedging, no filler. State the gap or the source.

Examples:
- "Within spec range of 700-850 kg/m3."
- "Exceeds minimum of 0.55 N/mm2."
- "Verdo FR MDF is Class B (FSI 35). Spec requires Class A (FSI 25 or less). Ritver coating system provides BS 476 Class 0 alternative per clause 2.6.C.1."
- "Blum catalog does not state BHMA Grade 1 explicitly. Manufacturer declaration to be provided."

## Before filling — verify data availability

1. List all new evidence files (datasheets, test reports, approvals)
2. For each, extract the key numerical values
3. Check if the values actually meet the spec requirement — do not assume
4. Flag gaps honestly: if a product is Class B and spec requires Class A, say so
5. Exclude irrelevant datasheets (e.g. lighting LED strip for a woodwork submission)

## No AI fingerprints

- No "comprehensive", "robust", "streamlined", "leveraged"
- No "per your", "kindly", "please note"
- No em-dashes, smart quotes, section symbols
- No symbols for status — use words
- Direct statements only. "Verdo FR MDF: 800.80 kg/m3." Not "The Verdo FR MDF product has a density of 800.80 kg/m3 which is within the specified range."
