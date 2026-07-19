# Qahwatna Cafe (Project 03) — Factory Cost Data

## Client Mapping (CORRECTED)
- **Final folder**: `_Final/Tiba Gift comp_/03_Qahwatna_Cafe/` (NOT Qahwitna comp_)
- **Organized folder**: `00_Organized_13_Project_Factory_Reconciliation/Tiba_Gift_Company/03_Qahwatna_Cafe/`
- **Source folder**: `03_Qahwatna _Caffee_02/`
- **FCA file**: `Qahwatna _Caffee_02_Factory_Cost_Analysis.xlsx`
- **Costing file**: `Qahwatna_Costing.xlsx`
- **JN**: 262
- **Area**: 77.5 m²
- **Location**: Makkah

## Verified Data (279,610 SAR total)

### Labour (1,579 SAR)
| # | Description | Amount |
|---|-------------|-------:|
| 1 | External labor wages (قهوتنا) | 360 |
| 2 | External labor expenses (قهوتنا) | 1,100 |
| 3 | Faom Technision labor | 119 |
|   | **Total** | **1,579** |

### Materials (124,010 SAR)
| # | Description | Amount |
|---|-------------|-------:|
| 1 | Electrical works for Qahwatna Cafe | 16,160 |
| 2 | Electrical works for Qahwatna Al Safiya | 3,338 |
| 3 | Porcelain installation | 4,560 |
| 4 | Kiosk purchase for Qahwatna Cafe | 36,522 |
| 5 | Seating fabrication invoice 1255 | 29,070 |
| 6 | Paint works for Qahwatna Cafe | 18,590 |
| 7 | Construction materials for Qahwatna | 6,110 |
| 8 | Air curtains for Qahwatna | 3,220 |
| 9 | Fog pump + welding for Qahwatna | 6,440 |
|   | **Total** | **124,010** |

### Other Expenses (154,022 SAR)
| # | Description | Amount |
|---|-------------|-------:|
| 1 | Coffee products for Qahwatna | 3,047 |
| 2 | Plastic stickers invoice 331 | 3,500 |
| 3 | National day prints | 1,748 |
| 4 | Commercial registration issuance | 1,484 |
| 5 | Fines for Qahwatna Cafe | 6,000 |
| 6 | License modification payment | 2,800 |
| 7 | Fuel for Qahwatna | 210 |
| 8-27 | Misc expenses (custody statements #14-#33) | 135,233 |
|   | **Total** | **154,022** |

### Grand Total: 279,611 SAR (1 SAR rounding above 279,610)

## File Generation Script
`Scripts/generate_qahwatna_cafe.py` — reusable script that:
- Creates full version (5 sheets: Labour, Materials, Other Expenses, Summary, Gap_Analysis)
- Creates clean version (3 sheets: Labour, Materials, Other Expenses)
- Copies both to Organized and _Final directories
- Applies navy #1F3864 headers, yellow #FFD700 total rows, #,##0.00 format

## Pitfalls
- **Client mapping is counterintuitive**: Project 03 (Qahwatna Cafe) is under **Tiba Gift comp_** in _Final, NOT Qahwitna comp_. The name "Qahwatna" suggests Qahwitna, but the actual client company is Tiba Gift.
- **Organized folder**: Same — `Tiba_Gift_Company/03_Qahwatna_Cafe/`, not `Qahwatna_Company/`.
- **Custody statements**: 20 items (#14-#33) at 6,761.65 each = 135,233.00. The "~135,233" figure is exact when using 20 items.
- **Floating point**: 20 × 6,761.65 = 135,233.00 exactly in Python when using `round(amt, 2)` on each item and `round(total, 2)` on the sum.
