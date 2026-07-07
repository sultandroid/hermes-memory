# Session Reference: Aseer Regional Museum — Equipment Research

**Source session:** June 1, 2026 — KSA museum replica fabrication project.

## Research Targets

| Item | Recommended Model |
|------|------------------|
| Spectrophotometer | X-Rite Ci64UV (SKU: CI64-XR with UV) |
| Gloss Meter | BYK micro-TRI-gloss (20°/60°/85°) |

## Key Findings

### X-Rite Ci64 Spectrophotometer
- **Geometry:** d/8° sphere, simultaneous SPIN/SPEX
- **Spectral Range:** 400–700 nm, 10 nm resolution
- **Apertures:** Switchable 4mm, 8mm, or 14mm
- **II Agreement:** 0.13 ΔE*
- **Repeatability:** 0.04 ΔE* (white ceramic)
- **UV:** Ci64UV model available — important for museum work (optical brighteners, UV-fluorescent materials)
- **Price:** ~$8,000–$12,000 USD (30,000–45,000 SAR)

### BYK micro-TRI-gloss
- **Angles:** 20°/60°/85° (covers full gloss range)
- **Range:** 0–2,000 GU (20°), 0–1,000 GU (60°), 0–160 GU (85°)
- **Repeatability:** ±0.1 GU (60°)
- **Conforms to:** ISO 2813, ASTM D523
- **Price:** ~$1,800–$2,500 USD (6,750–9,375 SAR)
- **Alternative:** Elcometer 480 (~$1,200–$1,800 USD)

### KSA/UAE Suppliers

| Supplier | Region | Products |
|----------|--------|----------|
| ESTS (Electro Scientific & Technical Supplies) | Dubai, UAE | X-Rite authorized distributor |
| Tajco Scientific | Dubai / Riyadh | BYK, Elcometer, general lab |
| Al Sweilem Scientific Bureau | Riyadh, KSA | General scientific instruments |
| SMEH (Scientific & Medical Equipment House) | Riyadh / Jeddah, KSA | Lab equipment procurement |
| Al Rashedi & Al Omran | Dammam / Riyadh, KSA | BYK-Gardner instruments |

## Techniques Used

1. **Search engine workaround:** Google/Bing/DuckDuckGo all blocked automated browser traffic. Went direct to manufacturer product category pages.
2. **JS-heavy page extraction:** X-Rite's Ci64 page loaded specs via JavaScript. Used `browser_console` with `document.body.innerText` and CSS selectors to extract spec values.
3. **JSON-LD mining:** Extracted product schema from `<script type="application/ld+json">` tags on the Ci64 page, yielding SKU (CI64-XR), brand (X-Rite), and product description.
4. **curl fallback:** When browser was slow, used `curl + Python regex` to strip HTML tags and filter for spec lines.
5. **Broken site awareness:** BYK Instruments and Elcometer sites returned 404 for all product pages (Salesforce Commerce Cloud deployment issue). Relled on third-party specs and training data.
6. **Report compilation:** Saved comprehensive `.md` report to `~/aseer-museum-equipment-research.md` with tables, pricing, supplier contacts, and procurement strategy.

## Full Report

The complete research output with all specs, pricing tables, and supplier contact details is at:
`/Users/mohamedessa/aseer-museum-equipment-research.md`
