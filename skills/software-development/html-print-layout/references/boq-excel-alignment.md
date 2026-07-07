# BOQ — Excel Alignment Pattern

## Principle
The HTML BOQ must be **structurally identical** to the Excel BOQ sheet. Client reviewers cross-check against the Excel — any mismatch in sections, items, quantities, or totals is a credibility failure.

## Verification Flow
1. Read Excel with `openpyxl(data_only=True)` — this gives computed values, not formulas
2. Extract: sheet names, section headers, item descriptions, units, quantities, unit rates, totals
3. Compare to HTML: exact match per row, per section, per subtotal
4. Check OH&P loading: the Excel has a loading factor (e.g. 1.30× = 8% supervision + 10% overhead + 12% profit). The HTML must either show loaded rates (Excel "Loaded" sheet) or show the loading breakdown separately
5. Verify bottom-line totals: Bid Price excl VAT, VAT amount, Grand Total incl VAT

## Common Mismatches
| Issue | Symptom | Fix |
|-------|---------|-----|
| Section order differs | Reviewer sees different grouping | Reorder HTML to match Excel exactly |
| Item counts differ | Excel has 8 sections × 12 items, HTML has 5 sections × 30 items | The HTML grouped items differently — match Excel's granularity |
| Quantities differ | Excel has 477 footings, HTML has 474 | Use Excel values — they're the source of truth |
| Pricing format differs | Excel has loaded rates, HTML has base rates | Use the "Loaded" sheet rates or add loading factor note |
| Missing sections | No Cladding section in HTML | Add missing sections per Excel |

## 8-Section BOQ Template (Al Zaidi Advertising Fence)
```
S01 — Steel Structure       1 item   (m² steel frame)
S02 — Civil Works            1 item   (precast footings)
S03 — Cladding & Finish      2 items  (cement board + joint sealant)
S04 — Banner & Printing      1 item   (PVC Flex Banner)
S05 — Lighting               1 item   (LED floodlights)
S06 — Electrical Works       2 items  (wiring + distribution panels)
S07 — Doors & Gates          2 items  (truck gate + pedestrian gate)
S08 — Additional & Safety    2 items  (signage + mobilization)
```

## OH&P Loading Display
Show the loading breakdown in the Grand Summary area:
```
Direct Cost Subtotal        SAR 3,367,269
Supervision 8%               SAR 269,381
Overhead 10%                 SAR 336,727
Profit 12%                   SAR 404,072
  Loading = 1.30× (30%)
Bid Price (excl VAT)        SAR 4,377,449
VAT 15%                      SAR 656,617
Grand Total (incl VAT)      SAR 5,034,067
```

## Key Quantities from Excel (Al Zaidi)
- Banner area: 11,350.4 m² (not 11,408)
- Footings: 477 at 3m spacing
- LEDs: 711 at 2m spacing
- Net length: 1,418.8m (after gate deductions)
- Joint sealant: 9,304m
- Wiring: 7,106.8m
- Distribution panels: 10

## Always
- Keep `.price.fill` cells empty — they're fill-in fields for the client
- Use the Excel "Loaded" sheet rates for final display (these include OH&P)
- Verify math: direct cost × 1.30 = bid price; bid price × 1.15 = grand total
