# Joinery / Furniture Costing — Reference Rates & Examples

## Standard Material Rates (KSA Workshop, SAR)

| Material | Unit | Rate SAR | Notes |
|----------|------|----------|-------|
| MDF 18mm 2440×1220mm | sheet | 120 | Standard grade |
| MDF 25mm 2440×1220mm | sheet | 180 | For countertop build-up |
| MDF 12mm 2440×1220mm | sheet | 90 | For decorative/CNC panels |
| Hardwood (walnut/mahogany) | bdft | 35 | Rough-sawn, select grade |
| Hardwood (oak) | bdft | 50 | European/imported |
| Teak solid | bdft | 65 | Burmese/Indonesian |
| Marine ply 18mm | sheet | 200 | For wet areas |
| Veneer (matching wood) | roll | 250 | For visible panel faces |
| Water-based primer (MDF sealer) | gal | 100 | |
| Water-based paint (satin) | liter | 110 | Dark colors typical |
| Stain (dark walnut) | liter | 120 | |
| Lacquer (satin, clear) | liter | 180 | Spray grade |
| Adhesives (PVA + contact) | lot | 120 | Per unit |
| Concealed push-latch | set | 200 | 4x per unit |
| Edge banding / filler | lot | 80 | For MDF edges |
| Abrasives 120-400 grit | lot | 60 | MDF, less needed |
| Abrasives | lot | 80 | Hardwood, more needed |

## Standard Labor Rates (KSA Woodwork Shop)

| Role | Daily Rate SAR | Notes |
|------|---------------|-------|
| Joiner/cabinet maker | 350 | Frame & panel construction |
| CNC operator/programmer | 500 | Include CAM programming time |
| Painter/finisher | 300 | Spray application |
| General assembly | 300 | Fitting, hardware install |
| Installer (site) | 400 | Leveling, anchoring |
| Sanding/prep helper | 250 | |

## Finishing Cost Comparison

| Finish | Materials SAR | Labor SAR | Total SAR | Notes |
|--------|-------------|-----------|-----------|-------|
| Water-based paint (dark, satin, 2 coats) | 220 + 100 primer | 300 | 620 | Fastest, simplest |
| Stain + satin lacquer (3 coats) | 120 + 360 | 525 | 1,005 | Higher quality, more durable |
| High-gloss paint system | 280 + 100 primer | 450 | 830 | More coats, more sanding |

## Quantity Indicators (from CAD pixel analysis)

Given a 458×521px CAD elevation image on white background:
- Object coverage ~5.4% → piece is slender/medium size
- H/V edge ratio ~1.85 → more horizontal features (counter, shelves, base)
- Strong horizontal bands = countertop (~y=280-310), base (~y=420-430)
- Strong vertical columns at x=80-90, x=320-330 = side supports or panel dividers
- Scale using assumption: counter height = 1100mm

## Typical Piece: Arabic Reception Kiosk (~1250W × 1100H × 600D)

### All Hardwood + Lacquer
| Category | SAR |
|----------|-----|
| Materials | 2,425 |
| Labor | 2,725 |
| Finishing | 1,005 |
| Overhead 10% | 616 |
| Transport | 200 |
| Installation | 500 |
| **Total** | **7,471** |

### All MDF + Water-Based Paint
| Category | SAR |
|----------|-----|
| Materials | 1,410 |
| Labor | 1,975 |
| Overhead 10% | 338 |
| Transport | 200 |
| Installation | 400 |
| **Total** | **4,324** |

Savings: SAR 3,147 (42%)

## Recalculation Pattern

When user corrects spec (e.g., "no solid wood all mdf and waterbase paint"):

```
Hardwood variant → MDF variant:
- Hardwood framing materials: -1,225 SAR
- Add MDF sheets: +360 +180 +90 = +630 SAR
- Remove stain+lacquer: -120 -360 = -480 SAR
- Add primer+paint: +100 +220 = +320 SAR
- Frame labor: -450 (3d → 2d @350)
- Sanding labor: -175 (1d → 0.5d @350)
- Finishing labor: -225 (1.5d → 1d @300)
- Less overhead: -278
- Net: ~-3,147 SAR (42%)
```
