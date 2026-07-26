# Snapshot Excel Audit Checklist

Use this checklist after generating any risk register Excel snapshot.

## Core Checks

- [ ] No merged cells
- [ ] Matrix uses COUNTIFS formulas, not hardcoded
- [ ] All P and S values populated
- [ ] All Scores populated
- [ ] Strategy column extracted from [Strategy: X] prefix
- [ ] Response/Action uses bullet points from actions array

## Matrix Labels

| Register | Header | Columns | Rows |
|----------|--------|---------|------|
| PRR | P ↓ S → | S1-S4 | P4-P1 |
| DDR | P ↓ S → | S1-S5 | P5-P1 |
| HSE | C ↓ L → | L1-L5 | C5-C1 |
| AVR | P ↓ S → | S1-S5 | P5-P1 |

## Data Sources

- risks.json = PRR only (61)
- ddr_risks.json = DDR only
- hse_risks.json = HSE only
- av_risks.json = AVR only
- No SMP IDs anywhere