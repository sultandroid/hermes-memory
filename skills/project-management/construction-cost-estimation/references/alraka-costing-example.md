# Al-Raka Archaeological Center — Costing Plan Workflow

This reference documents the costing plan built on 2026-06-14 for the Alrakaa Center (Moqtana/Tqanny).

## Project Parameters
- **Project**: Al-Raka Archaeological Center (مركز الراكة الأثري)
- **Contract**: AR-ER-2026-001, Design & Build Turnkey
- **Employer**: Moqtany (MQ)
- **Structure**: 6 × 40ft HC Corten-A containers, 2-storey (G+1)
- **Container module**: 12m × 5m = 60 m² each
- **Built-up area**: 3/floor × 60 m² × 2 floors = 360 m²
- **BOQ**: 43 items

## Steel Weight Calculation
| Component | kg each | Qty | Total kg |
|-----------|---------|-----|----------|
| Container structure (tare 40ft HC) | 3,900 | 6 | 23,400 |
| I-beam reinforcement (W8×31 @ 46.1 kg/m × 12.4m × 4 beams) | 2,286 | 1 | 2,286 |
| Steel sheet cladding (~3mm, ~120 m²) | 2,826 | 1 | 2,826 |
| External steel staircase (2-storey) | 2,500 | 1 | 2,500 |
| Connections, openings, bolts | 1,800 | 1 | 1,800 |
| **Total** | | | **32,810 kg (32.81 tons)** |

## Pricing
| Item | Rate | Unit | Source |
|------|------|------|--------|
| Structural steel | 10,000 | SAR/ton | Saudi market fabricated + marine coating |
| Concrete pad (RMC K350 + rebar + formwork) | 650 | SAR/m³ | Riyadh avg |
| SS316 handrail installed | 1,000 | SAR/lm | Riyadh avg |
| PWD ramp (concrete + finish + SS rails) | 2,000 | SAR/m² | Riyadh avg |

## Package Total: SAR 437,586
## Cost per m²: SAR 1,216

## Excel Sheet Structure
1. Cover Page (inserted as sheet 0)
2. Summary
3. Steel & Structural Works (4 items, 3 subgroups)
4. Facade Works (7 items, 3 subgroups)
5. MEP Works (10 items, 5 subgroups)
6. Interior Finishes & Fit-Out (22 items, 9 subgroups)

## Key openpyxl Patterns
- `PatternFill(start_color="1E293B")` — navy headers
- `PatternFill(start_color="FEF08A")` — yellow totals
- `PatternFill(start_color="F1F5F9")` — alternating rows
- `PatternFill(start_color="DBEAFE")` — subgroup headers
- `=IF(D{row}<>"",D{row}*F{row},"")` — item total formula
- `=SUMIF(G{start}:G{end},">0")` — subtotal/grand total
