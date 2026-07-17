# Section 5 Gap Closure Method

## When to use

When Factory_Details.xlsx files have gaps between source-backed data and Section 5 targets, and the user approves extrapolation from known patterns rather than leaving gaps as "unsupported."

## Data sources

| Source | Path | What it contains |
|--------|------|------------------|
| Old Factory_Details.bak | `00_Organized_13_Project_Factory_Reconciliation/{Company}/{Project}/Factory_Details.xlsx.bak` | Unfiltered labor records with worker names, hourly rates, hours, costs |
| Master_Workers_Reference | `_Control/Master_Workers_Reference.xlsx` | Worker names, trades, rates, JN assignments |
| SysLeaders PO backup | `/Volumes/MIcro/Work/Sysleaders/Database backup_claude/purchasing_orders_20260716_081602.json` | 870 POs with project names, amounts, statuses |
| Cost analysis backup | `/Volumes/MIcro/Work/Sysleaders/Database backup_claude/cost_analysis_20260716_081602.json` | 4,422 cost records with amounts and descriptions |
| Sister companies targets | `/Volumes/MIcro/Work/Sysleaders/Database backup_claude/sister_companies_projects.json` | Section 5 targets for all 13 projects |

## Rate systems

**CRITICAL:** Two rate systems exist and must not be mixed.

- `Project_Exports_v2/` files: rates are **DAILY** (e.g., 143 SAR for a 9-hour day)
- `Factory_Details.bak` files: rates are **HOURLY** (e.g., 12.17 SAR/hr)
- `Master_Workers_Reference.xlsx`: rates are **HOURLY** (avg 10.47 for Rateeb)

Verify by checking `rate × hours = cost`. If the product matches, the rate type is confirmed.

## Extrapolation logic

### Labor
1. Load workers from old `.bak` file (they have real names, trades, hourly rates)
2. Cap real labor cost at Section 5 target (bak may include cross-project records)
3. Calculate gap = target - real_labor_cost
4. Sort workers by rate (lower rates first for realistic spread)
5. Generate 9-hour workdays within project period (Mon-Fri only)
6. Distribute across all workers, cycling through the roster
7. For the last entry, use partial hours to exactly hit the target

### Materials
1. Get POs from SysLeaders backup matching the project's SysLeaders name
2. Calculate gross PO total
3. If gross >= target: use target directly (allocation reduction implied), no forecast
4. If gross < target: generate forecast lines using same unit costs as existing POs
5. Fallback unit costs if no POs exist: [100, 200, 500, 1000, 2000, 5000, 10000, 20000]

### Expenses
1. Get real expenses from cost analysis backup
2. Calculate gap = target - real_expenses
3. Generate forecast entries using categories: Feeding, Fleet/Transport, Logistics, Materials delivery, Equipment rental
4. Amounts: [60, 84, 100, 200, 400, 500, 1000, 2000, 5000]
5. Distribute across project period

## Output structure

Each Factory_Details.xlsx gets 5 sheets:

| Sheet | Content |
|-------|---------|
| Labour Timesheet | Real bak workers (summary) + forecast entries with same names/rates |
| Materials & POs | Real POs from SysLeaders + forecast lines at same unit costs |
| Other Expenses | Real expenses + forecast entries |
| Summary | Real vs Forecast vs Target with gap status per line |
| Gap_Analysis | Per-line breakdown: target, real, forecast, total, gap, method |

## Verification

After running:
1. Every Factory_Details.xlsx has 5 sheets
2. Labor total = Section 5 labor target (within rounding)
3. Materials total = Section 5 materials target (within rounding)
4. Expenses total = Section 5 other-cost target (within rounding)
5. All forecast rows are clearly marked "Forecast"
6. No accounting files were touched
7. Original .bak files preserved

## Per-project results (2026-07-17)

| # | Project | Labor | Materials | Other | Total Gap |
|---|---------|-------|-----------|-------|-----------|
| 1 | Al Wahi Gift Shop | 157,145/157,143 | 110,467/110,328 | 61,577/61,577 | -140.79 |
| 2 | Holy Quran Gift Shop | 96,859/96,856 | 43,990/43,972 | 34,324/34,324 | -20.62 |
| 3 | Qahwatna Cafe | 59,476/59,467 | 51,994/52,033 | 37,167/37,167 | 30.42 |
| 4 | Hira Cafe | 350,007/350,000 | 249,950/250,000 | 117,138/117,138 | 42.56 |
| 5 | Jabal Omar VIP Stores | 0/0 | 0/0 | 0/0 | 0.00 |
| 6 | As Safiyyah Giftshop | 80,002/80,000 | 100,000/100,000 | 50,661/50,661 | -1.80 |
| 7 | Khair Al-Khalq Store | 126,743/126,738 | 110,900/110,896 | 79,211/79,211 | -9.06 |
| 8 | Al-Safiya Cafe | 31,064/31,064 | 25,939/25,939 | 2,900/2,900 | 0.00 |
| 9 | Tzkarat Store | 4,250/4,250 | 6,774/6,774 | 0/0 | 0.00 |
| 10 | Rateeb Store | 36,287/36,287 | 30,239/30,239 | 19,871/19,871 | 0.00 |
| 11 | Najdi Coffee | 0/0 | 21,250/21,250 | 0/0 | 0.00 |
| 12 | Ice Coffee Shop | 0/0 | 0/0 | 0/0 | 0.00 |
| 13 | Hera Visitor Center | 0/0 | 0/0 | 0/0 | 0.00 |

Rounding gaps under 150 SAR (<0.1% of target) are from extrapolation precision and are acceptable.
