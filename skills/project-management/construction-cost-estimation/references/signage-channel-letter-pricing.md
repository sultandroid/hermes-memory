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

## CRITICAL — Confirm the DESIGN before pricing (1m-high wall + perimeter strip)

The user corrected the design assumption **multiple times** in one session. The EXPO 2030 letters are NOT deep boxes with the whole face illuminated — they are **1m-high extruded walls** (like a maze/labyrinth, per the renderings) with a **0.5m-wide LED strip running along the top edge of the perimeter**. This is the single biggest cost driver and getting it wrong swings the total by ~15M SAR.

**Ask/confirm BEFORE building the LED and ACP quantities:**
1. **Letter height** — the user said "ارتفاع الحرف فقط ١ متر" (letter height is only 1m). The wall is 1m tall, NOT the full letter width/height dimension.
2. **Illumination area** — "مساحه الحرف مش كلها مضيئه فقط الحرف نصف متر فالحرف فقط" (the letter face is not all illuminated, only a 0.5m strip). Illuminated area = `perimeter × 0.5m`, NOT `width × height`.
3. **ACP coverage** — the wall has a **top face** (the letter shape, `width × height`) + **vertical sides** (`perimeter × 1m height`). NOT face + deep-box sides.

**Correct quantities (EXPO 2030 / RIYADH / SAUDI ARABIA, 25 letters, 1m-high walls):**
| Item | Formula | Qty |
|------|---------|-----|
| ACP top face | `Σ(width × height)` | 23,400 m² |
| ACP vertical sides | `Σ(perimeter × 1m)` | 2,987 m² |
| LED modules | `Σ(perimeter × 0.5m) × 55/m²` | 82,142 nos |
| Wiring | `Σ(perimeter)` | 2,987 m |
| Steel structure | 19.37 kg/m² × 2,987 m² | 57.9 tons |

**LED density — use the STANDARD 45–70 modules/m², NOT the datasheet string math.** The reference module is the **DOTLUX ACplus 1.5W 160° IP67 3000K** (100-light string, 20m chain, direct 230V, self-adhesive). The datasheet gives 100 modules/20m string = 5 modules/linear meter, which the user REJECTED as too low when I derived 10 modules/m² from it. The correct basis is the **standard LED module density: 45–70 modules/m²** (120×120mm to 150×150mm spacing). Use **55 modules/m²** as the mid value. Do NOT use the old "1 module per 0.15 m² of face" rule either — that was also wrong.

```python
perim = 2987
strip_w = 0.5
illum_area = perim * strip_w            # 1,493.5 m²
modules_per_m2 = 55                     # standard 45-70/m², mid value
total_modules = illum_area * modules_per_m2   # 82,142
```

**LED module price is ~1.25 SAR each** (user: "سعر الموديول الواحد تكلفه ١ ريال وربع") — NOT 100 SAR. This is a ~80× price correction that collapses the LED line from ~1M to ~103K SAR. Always confirm the actual module unit price from the supplier/datasheet before pricing; the 100 SAR figure in the old frame BOQ was a placeholder.

**Driver sizing is by WATTAGE, not by length.** Total LED power = modules × 1.5W (82,142 × 1.5 = 123.2 kW). Divide by driver capacity with 80% derating (drivers must not run at 100%): e.g. 200W driver usable 160W → 770 drivers; 300W driver usable 240W → 513 drivers. Ask the user which driver size and its unit price before finalizing the driver line — do NOT price drivers as a flat "perimeter × rate" line.

**Add the icon/logo as a separate perimeter.** The EXPO 2030 logo is ~1,500m perimeter, 130m tall, and must be added to the letters' 2,987m (total ~4,487m) for ACP sides, LED strip, and steel. Confirm the logo's top-face area separately (it is NOT the same as the letters' 23,400 m²).

**Cost impact (the whole point of confirming):**
| Variant | LED modules | LED cost | Grand total |
|---------|------------|----------|-------------|
| Face-based (WRONG) | 156,000 | 15,600,000 | 20,767,975 |
| **1m-wall + 0.5m strip (CORRECT)** | **9,957** | **995,700** | **5,684,485** |

The correct design drops the project from ~20.8M to **5.68M SAR** (pre-VAT) — a ~15M swing. Always confirm the design variant before committing to LED/ACP quantities.

## ACP Pre-Painted Variant (all-ACP build)

The user may decide the ENTIRE proposal is pre-painted ACP panels instead of steel + polycarbonate. Trigger phrase: **"احنا اتفقنا هانشتغل كله ACP الواح مدهونه جاهزه"** (we agreed to do it all in pre-painted ACP panels). When this fires, REBUILD the whole BOQ — do not keep the steel/poly build-up.

**Material swap (per component):**
| Old (steel + poly) | New (ACP pre-painted) |
|--------------------|----------------------|
| Steel body (10 SAR/kg) | ACP panel (120 SAR/m²) |
| Polycarbonate face (80/m²) | ACP panel (120 SAR/m²) |
| LED modules | unchanged (still internal LED) |

**ACP quantity build-up for channel letters:**
- Face area = `width × height` (m²)
- Sides area = `perimeter × depth(0.3m)` (m²)
- Total ACP = face + sides
- LED modules = `face / 0.15` (unchanged)

**Worked example (EXPO 2030 / RIYADH / SAUDI ARABIA, 25 letters):**
- Face 23,400 m² + sides 896 m² = **24,296 m² ACP**
- LED 155,999 nos, wiring 2,987 m

**Combined all-ACP BOQ sections** (frame + light boxes + letters + electrical):
| Section | Amount (SAR) |
|---------|-------------|
| Frame ACP cladding (1,540m perimeter) | 260,260 |
| Light boxes (ACP + LED, 770 boxes) | 592,190 |
| Channel letters (ACP + internal LED) | 19,446,015 |
| Electrical & wiring | 90,170 |
| **GRAND TOTAL** | **20,388,635** |
| VAT 15% | 3,058,295 |
| **TOTAL + VAT** | **23,446,930** |

**Pitfall — unit check:** letter dimensions are in METERS (frame is 610m × 160m), not cm. A first pass treating them as cm gave an absurd 11.3 m² total; correct is 24,296 m². Always sanity-check total ACP area against the frame scale before building.

**Cost impact vs steel+poly:** ACP at 120/m² is pricier than steel(10/kg)+poly(80/m²), so the all-ACP total runs ~+1M SAR higher (20.39M vs 19.34M pre-VAT). State this delta when delivering so the user sees the trade-off.

## Steel structure is ALWAYS a separate line item (user-corrected)

The user explicitly corrected twice: **"لازم يكون في اشاره للحديد في سطر لوحده الخاص بالهيكل بالوزن بتاعه"** (steel must be its own line with its weight) and **"اعمل الهيكل الحديد لوحده ومساحه ال ACP لوحده"** (make the steel structure separate and the ACP area separate). Do NOT fold steel into the ACP cladding line.

**Frame steel (FR-01):** separate line, qty in tons, weight stated in description AND notes. E.g. `Steel structure - posts, rails, bracing (SHS 30x30x2mm) - 4.47 tons` @ 10,000 SAR/ton, notes: `Total steel weight: 4.47 tons (posts 513 + rails 1,540m + bracing 10%)`.

**Letter steel (LT-01):** same treatment. The user gave the ACTUAL module build-up — do not use the perimeter-rail + internal-ribs estimate (46.4t) as the default. The real per-module (1m × 3m = 3 m²) steel is:

| Component | Build-up | Weight |
|-----------|----------|--------|
| SHS 30×30×2mm external frame (1m high) | 10m (perim 8m + 2 cross × 1m) × 1.76 | 17.6 kg |
| IPE 100 legs (70cm) | 4 × 0.7m × 8.1 | 22.7 kg |
| Shelf (30cm, 3m long) | 3m × 1.76 | 5.3 kg |
| Base plates 20×20×1cm | 4 × (0.2×0.2×0.01×7850) | 12.6 kg |
| **Total per module** | | **58.1 kg** |

**Per m² = 58.1 / 3 = 19.37 kg/m².** For the 25 letters (2,987 m² wall area): `2,987 × 19.37 = 57,858 kg = 57.9 tons` @ 10,000 = 579,000 SAR. The legs are 70cm + shelf 30cm = 1m total height, all clad with ACP. Always ask the user for the actual steel module build-up (leg section, leg height, shelf, base plate) rather than estimating from perimeter ribs.

**Split ACP into face and sides as separate line items** (LT-02 face, LT-03 sides) — do not combine into one "body" line. Face = `width × height`, sides = `perimeter × depth`.

## Frame ACP band = perimeter × depth (0.5m), NOT perimeter × 0.1m caps

The user caught a wrong assumption: I priced "top/bottom caps" as `2 × 1,540m × 0.1m = 308 m²`. Correct: the illuminated frame band is **perimeter × depth (0.5m)** = `1,540 × 0.5 = 770 m²`, which already includes the top/bottom caps (they're part of the band, not an add-on). Never add caps as a separate quantity on top of the band.

## Ground works (by client) + foundations (provisional) sections

Add two explicit sections so exclusions are visible:
- **Ground works (BY CLIENT):** levelling & compaction, geotextile & gravel — each `1 lot @ 0 SAR`, notes `BY CLIENT - excluded from this BOQ`.
- **Concrete foundations (PROVISIONAL):** `1 lot @ 0 SAR` provisional sum — leave 0 until the user sets a % of total.

## Final combined all-ACP BOQ (1m-high walls, corrected design + datasheet LED + real steel)

| Section | Amount (SAR) |
|---------|-------------|
| Frame (steel 4.47t + ACP 770m² band) | 175,600 |
| Light boxes (ACP + LED, 770 boxes) | 212,003 |
| Channel letters (steel 57.9t + ACP top 23,400m² + sides 2,987m² + LED 82,142 @1.25) | 4,101,395 |
| Electrical & wiring | 90,170 |
| **GRAND TOTAL** (excl. ground works & foundations) | **4,579,168** |
| VAT 15% | 686,875 |
| **TOTAL + VAT** | **5,266,043** |
| Per linear meter (1,540m) | 2,973 |

**Channel letters section (LT-01..LT-07), final corrected design (55 modules/m²):**
| # | Item | Qty | Total (SAR) |
|---|------|-----|-------------|
| LT-01 | Steel structure (SHS 30x30x2mm + IPE 100 legs) — 57.9 tons | 57.9 ton | 579,000 |
| LT-02 | ACP top face (letter shape) | 23,400 m² | 2,808,000 |
| LT-03 | ACP vertical sides (perimeter × 1m) | 2,987 m² | 358,440 |
| LT-04 | LED modules (55/m² × 1,493.5 m² strip) @ 1.25 | 82,142 nos | 102,678 |
| LT-05 | Mounting brackets @ 1.25 | 82,142 nos | 102,678 |
| LT-06 | Internal wiring + drivers | 2,987 m | 149,350 |
| LT-07 | Fabrication & assembly | 25 nos | 1,250 |

**Cost driver note:** the LED line collapsed from ~1M SAR (at 100/module) to ~103K SAR (at 1.25/module) once the real module price was applied — the LED is NO LONGER the dominant cost. The ACP top face (2.8M) is now the largest single line. Always confirm the module unit price AND the modules/m² density before finalizing; a placeholder rate or wrong density can mislead the whole estimate.

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
