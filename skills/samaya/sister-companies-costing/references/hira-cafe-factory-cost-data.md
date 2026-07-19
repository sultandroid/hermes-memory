# Hira Cafe (Project 04) — Factory Cost Data

## Source
- Accounting file: `04_Hira_Cafee_02/Hira_Cafee_02_Restructured_Costing.xlsx`
- FCA file: `04_Hira_Cafee_02/Hira_Cafee_02_Factory_Cost_Analysis.xlsx`
- Client: Qahwitna comp_ (company folder) — **but files placed under Tiba Gift comp_ in this session per user direction**
- Organized company: Qahwatna_Company — **but files placed under Tiba_Gift_Company in this session per user direction**
- **Pitfall:** The project map says Qahwitna comp_ / Qahwatna_Company, but the user directed files to Tiba Gift comp_ / Tiba_Gift_Company. Always verify the company mapping with the user before hardcoding paths in the generator script. The project map in the skill is authoritative unless the user explicitly overrides it.

## Factory Cost Breakdown (verified items)

### Labour — 23,897 SAR (8 trades)

| Trade | Records | Hours | Cost (SAR) |
|-------|---------|-------|-----------|
| Welder | 68 | 601.5 | 9,248 |
| Painter | 72 | 592 | 8,434 |
| Carpenter | 31 | 268.4 | 2,237 |
| Labor | 27 | 222.4 | 1,815 |
| CNC Operator | 12 | 106.5 | 1,041 |
| Veneer Technician | 7 | 66.5 | 791 |
| Supervisor | 3 | 14.5 | 194 |
| 3D Printers Operator | 2 | 18.5 | 137 |

### Materials — 61,265 SAR (7 POs)

| PO# | Description | Amount (SAR) |
|-----|-------------|-------------|
| PO#416 | Paint | 25,000 |
| PO#609,623,891,894 | Upholstery | 17,335 |
| PO#418,465 | Electrical | 8,900 |
| PO#472 | Marble | 4,700 |
| PO#476 | Other | 3,000 |
| PO#454 | Metal/Steel | 930 |
| — | Fleet / Transport | 1,400 |

### Reallocation
- Billboard costs moved to Ice Coffee (12): -29,549 SAR

### Net Factory Cost: 55,613 SAR

## Files Created
- `00_Organized_13_Project_Factory_Reconciliation/Qahwatna_Company/04_Hira_Cafe/04_Hira_Cafe_Factory_Cost_Details.xlsx` (full)
- `00_Organized_13_Project_Factory_Reconciliation/Qahwatna_Company/04_Hira_Cafe/04_Hira_Cafe_Factory_Cost_Details_Clean.xlsx` (clean)
- `_Final/Qahwitna comp_/04_Hira_Cafe/` (copies of both)
