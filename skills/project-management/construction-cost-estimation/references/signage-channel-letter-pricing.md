# Signage / Channel-Letter BOQ Pricing

Class of work: pricing a large-format illuminated signage proposal (e.g. EXPO 2030 land-art logo, airport-road signage) from a design PDF + vector file. Two common design variants:

1. **Channel Letters** (individual 3D letters) — priced per letter from face area + perimeter.
2. **Light Boxes** (ACP boxes along a frame perimeter) — priced per box.

## Channel-Letter Per-Letter Cost Build-Up

For each letter, given width (m), height (m), perimeter (m) from the Letter Dimensions sheet:

| Component | Formula | Unit |
|-----------|---------|------|
| Face area | `width × height` | m² |
| Steel body area | `perimeter × depth(0.3m) × 2 sides` | m² |
| Steel weight | `steel_area × kg/m²` (3mm galvanized ≈ 23.55 kg/m²) | kg |
| LED modules | `face_area / 0.15` (1 module per 0.15 m² of face) | nos |
| Wiring | `perimeter` | m |

**Cost =** `steel_kg × R_steel + face × R_poly + led × R_led + led × R_bracket + wire × R_wire`

### Typical BOQ rates (SAR)
| Rate | Value | Basis |
|------|-------|-------|
| Steel fabrication (labor) | 12 /kg | FR-05 |
| Polycarbonate sheet (face) | 80 /m² | LT-02 |
| LED module IP67 3000K | 100 /nos | LT-03 |
| Mounting bracket + fixation | 5 /nos | LT-04 (1 per LED) |
| Internal wiring + drivers | 50 /m | LT-05 (along perimeter) |

### Worked example (letter "E", 29.5×26m, perimeter 111m)
- Face = 767 m², steel area = 67 m², steel = 1,569 kg
- LED = 5,113 nos, wire = 111 m
- Cost ≈ 622,632 SAR

## Light-Box Variant (ACP boxes along frame perimeter)

Per box (e.g. 50×100cm, 15cm deep, ACP 4mm body + polycarbonate face):
- ACP body = 0.95 m²/box, poly face = 0.50 m²/box
- LED = 5 modules/box (5W each, IP67 3000K)
- Driver + wiring per box, fabrication/assembly per box

## Steel Frame (perimeter rail system)

For a frame of known perimeter (e.g. 1,540m) with SHS posts @ 3m c/c:
- Posts = `perimeter / spacing` (513 nos for 1540m @ 3m)
- Perimeter rails = full perimeter length
- Cross bracing ≈ 10% of rail length
- Steel weight = Σ(length × kg/m); price at ~10,000 SAR/ton fabricated

## The Frame BOQ is the METHOD template

When the user says "بعتلك الملف اللي عملناه لتسعير الفريم الخارجي للوجو علشان تفهم" (I'm sending you the frame-pricing file so you understand the method), the frame BOQ (`*_Final.xlsx`) is the **reference template** for how to structure the letters BOQ. Mirror its exact structure:

- **3 sheets:** `BOQ <variant>` (items), `Summary`, `Specifications`
- **BOQ sheet:** sections → items (Qty × Unit Rate = Total via `=D*F`) → `Subtotal - <Section>:` (`=SUM(...)`) → `GRAND TOTAL` → `VAT (15%)` (`=G*0.15`) → `TOTAL INCLUDING VAT` → `PER LINEAR METER` (grand/perimeter)
- **Summary sheet:** per-section amounts pulled from the BOQ sheet + `% of Total` + GRAND/VAT/TOTAL/PER-UNIT rows
- **Specifications sheet:** design basis (frame dims, post spacing, section, steel weight, LED count, power load, target rate, exclusions)

Reuse the SAME unit rates from the frame BOQ (steel 10 SAR/kg, polycarbonate 80/m², LED 100/nos) so both files are consistent.

## Pitfalls

- **Cross-sheet reference with a space in the sheet name → `#NAME?`.** If the BOQ sheet is named `BOQ Channel Letters` (space), a Summary formula `=BOQ Channel Letters!G8` fails. You MUST quote the sheet name: `='BOQ Channel Letters'!G8`. This bit me when building the Summary sheet.
- **openpyxl `data_only=True` returns `None` for uncalculated formulas.** A freshly-written workbook has no cached values, so reading it back with `data_only=True` shows blanks/None for every formula cell. To VERIFY formulas actually compute, force recalculation with LibreOffice headless:
  ```bash
  soffice --headless --convert-to xlsx --outdir /tmp/boqcalc EXPO2030_Channel_Letters_BOQ.xlsx
  python3 -c "import openpyxl; wb=openpyxl.load_workbook('/tmp/boqcalc/EXPO2030_Channel_Letters_BOQ.xlsx', data_only=True); ..."
  ```
  The converted copy has cached values; read THAT to confirm grand totals/VAT/percentages are correct before delivering.
- **Two different BOQ files may exist** for the same proposal (channel-letters version vs light-box version). Confirm WHICH design the client approved before pricing — the user may be iterating between them.
- **"كمل باقي الاحرف بنفس الطريقه"** = continue pricing the remaining letters using the same per-letter build-up — don't re-derive the method, just extend the table.
- **Totals often left blank** in the BOQ template (Subtotal/Grand Total/VAT rows empty) — fill them with `=SUM(...)` over item rows only (see construction-cost-estimation §4 formula rule).
- **Exclusions matter:** foundations, ground levelling, geotextile, gravel are often "by client" — keep them out of the signage BOQ and note them.
- **Vector file** (`*.svg`) is the source of truth for letter geometry; the PDF proposal gives dimensions. Cross-check letter widths/heights against the vector before pricing.
