# Session Specifics: Al Zaidi Parking Proposal (June 3, 2026)

## Project
- **Client:** شركة الغربية للتطوير والاستثمار المحدودة (Al Gharbia Development & Investment Co. Ltd.)
- **Location:** Al Zaidi Parking, Makkah
- **Scope:** Advertising fence 1,426m × 8m, 11,350 m² banner area
- **Site:** https://al-zaidi-parking.surge.sh

## Key Parameters (from Option C - BOQ (Loaded) sheet)
- Column spacing: 3m → **474 columns** (was 4m → 358)
- Light spacing: 2m → **711 LED** fixtures (was 12m → 120)
- Gates: Vehicle 6m + Pedestrian 1.2m (deducted from effective length)
- Effective fence length: **1,418.8m** (1,426 − 7.2)
- Footing type: Precast RC 2.75×1.50×0.60m, Fcu 300
- Cladding: **Cement Board 12mm** (not ACP, not plywood)
- Banner: PVC Frontlit Flex 550gsm (Obekan/Obeflex Premium)
- Steel coating: **Epoxy paint ≥200µm DFT** (no galvanizing)
- Loading factor: **1.30×** (8% supervision + 10% OH + 12% profit)
- Distribution panels: 10 (1 per ~150m)

## Loaded Prices (from Option C - BOQ (Loaded) sheet, final version with Section 08 distributed)
| # | Item | Qty | Rate | Total |
|---|------|-----|------|-------|
| 01 | Steel Structure (per m² face) | 11,350.4 | 111.44 | 1,264,917.74 |
| 02 | Precast RC Footings | 477 | 2,491.07 | 1,188,240.01 |
| 03 | Cement Board 12mm | 11,350.4 | 72.11 | 818,476.18 |
| 04 | Joint Sealant + Cover Strip | 9,304 | 7.87 | 73,190.24 |
| 05 | PVC Banner 550gsm | 11,350.4 | 36.71 | 416,678.78 |
| 06 | LED Flood Light 300W | 711 | 367.10 | 261,011.61 |
| 07 | Wiring in Galv. Conduit | 7,106.8 | 41.95 | 298,164.73 |
| 08 | Distribution Panel | 10 | 4,588.81 | 45,888.12 |
| 09 | Truck Gate | 1 | 8,522.08 | 8,522.08 |
| 10 | Pedestrian Gate | 1 | 2,359.96 | 2,359.96 |
| | **Grand Total excl. VAT** | | | **4,377,449.44** |
| | VAT 15% | | | **656,617.42** |
| | **Grand Total incl. VAT** | | | **5,034,066.86** |

Note: After Section 08 distribution (Mobilization 32,500 + Safety 4,524 distributed pro-rata), rates increased ~0.85% across all items.

## Final Page Structure (17 pages)
| # | Section | Content |
|---|---------|---------|
| 1 | Cover | Client name, location, 4 scope cards, PAGE 01/16 |
| 2 | TOC | 4 categories with emoji icons + anchor links |
| 3 | Executive Summary | Stats row (1,426m, 8m, 4.38M SAR, 477 footings) |
| 4 | Scope of Work | Detailed items + gates table |
| 5 | Capabilities | Manufacturing grid + org chart |
| 6 | Technical Specifications | Overview table (all materials) |
| 7 | Banner & UV Printing TDS | PVC Flex material data sheet |
| 8 | Cement Board 12mm TDS | Fiber cement data sheet |
| 9 | Jotun Epoxy Mastic TDS | Coating data sheet |
| 10 | LED Flood Light TDS | Lighting data sheet |
| 11 | Technical Drawings | Calculation sheet + Hoarding Option C |
| 12 | BOQ Part 1 | Sections 1-4 (Steel, Civil, Cladding, Banner) |
| 13 | BOQ Part 2 | Sections 5-7 (Lighting, Electrical, Doors/Gates) + Grand Summary |
| 14 | Methodology | 5-phase execution plan |
| 15 | Timeline | SVG Gantt chart (820×250 viewBox, 11-week programme) |
| 16 | Company Documents | 17 doc cards (incl. ISO) + doc-sum + closing + Client signature |
| 17 | Payment + Terms + Sign-Off | 4 payment stages + warranty + general conditions + Contractor signature |

## Key Iterations During Session
1. **Cover background in print:** Removed decorative gradient, kept solid fallback for full-page cover
2. **BOQ restructured** 6 sections → 8 sections (matching Excel)
3. **Section 08 distributed** pro-rata into all items (~0.85% loading)
4. **Pages 16-17 balanced** — moved doc cards + closing + 1 signature card to balance (173→205 vs 252→212 lines)
5. **SVG timeline redesigned** 3 times — final version: 820×250 viewBox, label panel at x=0-210, `text-anchor="end"` + `direction="rtl"` for Arabic
6. **TOC links fixed** — broken `id="page-1""` bug from automated renumbering
7. **Print CSS fixed** — `overflow:hidden` → `min-height:1123px` enforced, `cover-wrap::before` kept visible in print
