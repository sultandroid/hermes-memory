# Standard BOQ Structure — Samaya Fence Projects

## 4-Sheet Excel Model (`BOQ_Pricing_Model.xlsx`)

### Sheet 1: Option C — BOQ
Base unit rates (direct cost before OH&P). Full detailed item descriptions matching Excel source.

8 sections, 12 line items:

| # | Section | Item | Unit | Qty | Base Rate |
|---|---------|------|------|-----|-----------|
| 01 | Steel Structure | Complete steel hoarding structure per m² face — MS Tube columns 60×60×3mm, primary beams 50×50×4mm & rails 50×50×3mm, bracing, shop primer | m² | 11,350.4 | 85 |
| 02 | Civil Works | Precast RC isolated footing 2.75×1.50×0.60m Fcu 300 complete with anchor bolts, reinforcement cage, lifting inserts — delivered & levelled | pc | 477 | 1,900 |
| 03 | Cladding | Cement Board 12mm exterior grade, fixed to steel frame with self-drilling screws @ ≤400mm centres | m² | 11,350.4 | 55 |
| 04 | Cladding | Joint sealant + aluminum/PVC cover strip | m | 9,304 | 6 |
| 05 | Banner | Printed PVC Frontlit Flex Banner 550gsm (Obekan) with UV digital print ≥1440 dpi, fixed onto cement board | m² | 11,350.4 | 28 |
| 06 | Lighting | LED Flood Light 300W c/w mounting bracket/arm, complete with wiring, tested & commissioned | pc | 711 | 280 |
| 07 | Electrical | Floodlight wiring in galvanized steel conduit from MDP to each light | m | 7,106.8 | 32 |
| 08 | Electrical | Distribution panel MCB/MCCB breakers + timer — one every ~150m | pc | 10 | 3,500 |
| 09 | Gates | Truck/vehicle access gate (heavy-duty) steel frame, hinges, lockable latch — 6m opening | pc | 1 | 6,500 |
| 10 | Gates | Pedestrian access gate steel frame, hinges, lockable handle — 1.2m opening | pc | 1 | 1,800 |
| 11 | Safety | Warning & directional safety signage reflective 600×900mm with posts | pc | 29 | 120 |
| 12 | Safety | Mobilization — equipment transport, site setup, safety provisions, cleanup | lot | 1 | 25,000 |

**Input parameters tab** at bottom:
- Fence length: 1,426m, Height: 8m
- Truck gate: 6m × 1, Pedestrian gate: 1.2m × 1
- Footing spacing: 3m, Light spacing: 2m
- Panel spacing: 150m

### Sheet 2: Option C — BOQ (Loaded)
Same items as Sheet 1 but with OH&P built into unit rates.
Loaded Rate = Base Rate × **1.30** (loading factor)
### OH&P Loading (for "Loaded" Sheet)
When using `Option C - BOQ (Loaded)` sheet:
- Supervision / Preliminaries: 8%
- Overhead (G&A): 10%
- Profit Margin: 12%
- **Loading Factor: 1.30×** (multiply base rate by this to get loaded rate)
- The loaded sheet has fractional rates (e.g., 110.50 → 111.44 after Section 08 distribution)
- Round to 2 decimal places when displaying in HTML

### Section 08 Distribution
The user may distribute Section 08 (Mobilization + Safety = 37,024 SAR) pro-rata into all other items:
- Distribution factor = Section 08 total / Sum of all other items = 28,480 / 3,338,788.80 ≈ 0.00853
- Each item's rate increases by ~0.853%
- Section 08 is REMOVED from the BOQ entirely
- Grand Summary becomes 7 rows
- The loaded sheet already has this distribution applied when it says "DISTRIBUTED ITEMS"

HTML proposal uses LOADED prices. Add a note below the Grand Summary table showing the loading factor breakdown.

### Sheet 3: Pricing Summary
Section-by-section cost breakdown with subtotals and % of total.

### Sheet 4: Notes
- Assumptions, input parameters, loading factor details
- Arabic + English notes
- 15% VAT, 60-day validity, 12-month warranty
