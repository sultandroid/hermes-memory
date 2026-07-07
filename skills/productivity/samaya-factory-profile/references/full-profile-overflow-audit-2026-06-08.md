# Samaya Factory Profile — Full Overflow Audit (2026-06-08)

## Methodology

Scanned 34 CSS files and full index.html (3963 lines). Classified every page by content-area constraint.

- **Base `.content`**: `top:22mm` + `bottom:18mm` → **170mm** usable
- **Archetypes with override**: `height: calc(210mm - 22mm - 14mm)` → **174mm** usable

## Results

### Pages with height constraints (must fit in 174mm)

| Page | Archetype | Constraint | Est. Content | Verdict |
|------|-----------|------------|-------------|---------|
| #p2 | v3-toc | 174mm | ~105mm | ✅ FITS |
| #p6 | v3-method | 174mm | ~163mm | ✅ FITS tight |
| #p12 | v4-catalog | 174mm | ~179mm | ❌ OVERFLOW ~5mm (FIXED v6.6) |
| #p13b | v4-replica-gallery | 174mm | ~133mm | ✅ FITS |
| #p24a | proj-sectorial | 174mm | ~162mm | ⚠️ TIGHT |
| #p26 | proj-org | 174mm | ~120mm | ✅ FITS |

### Pages without fixed height (multi-page OK)

| Page | Archetype | Notes |
|------|-----------|-------|
| #p4 | v4-capacity | ✅ FITS |
| #p5 | v4-scope | ✅ FITS |
| #p7 | v4-atelier | ✅ FITS |
| #p8 | v4-mosaic | ✅ FITS |
| #p14 | v4-cmyk | Converted to 2-page spread (v6.8) |
| #p14b | v4-cmyk | New page for process+QA |
| #p15 | v4-type | Converted to 2-page spread (v6.9) |
| #p15b | v4-type | New page for sign types+specs |
| #p25a-p25e | p25* | Multi-page by design |

### ed-spread pages (HSE, Approvals, After-Sales, Certifications, Financial)

All use `ed-spread` layout with 2-column (navy visual + cream editorial). Fit-fixes applied in 20-redesign.css:
- #p4-hse: padding 7mm/9mm/6mm, font 8.6pt
- #p22: Same compressed pattern
- #p20, #p25, #p4-financial: FITS

### p12 Overflow Fix Applied (v6.6)

Photo strip: 40mm→32mm, column images: 43mm→38mm, post-grid spacing reduced. Total ~16mm saved.

### Photoshop Size Reference

| Context | Recommended Size |
|---------|-----------------|
| Machine cards (p14) | 42mm min |
| Evidence bar | 32mm |
| QA photo | 50mm |
| Hero photo | 48-85mm |
| Gallery thumbnails | 26mm |
| Production strip | 28mm |
