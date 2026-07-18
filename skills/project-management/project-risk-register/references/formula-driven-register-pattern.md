# Formula-Driven Risk Register — Excel Pattern (v2.0)

## Overview

The v2.0 Excel pattern uses **live Excel formulas** instead of static computed values. 
When the user changes Probability or Severity, Score and Rating auto-calculate.

## Workbook Structure

| Sheet | Purpose | Formula Type |
|-------|---------|-------------|
| Cover | Project overview + key metrics | `=COUNTA`, `=COUNTIF` linked to Risk Register |
| Risk Register | Full register with formula-driven rating | `=I6*J6`, nested `IF` rating |
| Dashboard | Live KPIs, distribution, watchlist | `=COUNTIF('Risk Register'!L6:L54,"Critical")` |
| Risk Matrix | 4×4 heat map (P×I) | `=COUNTIFS('Risk Register'!I6:I54,4,'Risk Register'!J6:J54,4)` |
| Treatment Plan | Critical & High risk actions | Static (filtered from data) |
| Ancillary | DRR, HSE, AV, Methodology, Change Log | Imported from source |

## Column Layout (Risk Register, row 5 header, data rows 6+)

| Col | Field | Type |
|-----|-------|------|
| B | # | Static sequential |
| C | Risk ID | Static |
| D | RBS Code | Static |
| E | Category | Static |
| F | Risk Event | Static (wrapped) |
| G | Cause | Static (wrapped) |
| H | Consequence/Impact | Static (wrapped) |
| I | Inherent P (1-4) | User-entered number |
| J | Inherent I (1-4) | User-entered number |
| K | **Inherent Score** | `=I{row}*J{row}` |
| L | **Inherent Rating** | `=IF(K{row}="","",IF(K{row}>=12,"Critical",IF(K{row}>=8,"High",IF(K{row}>=4,"Medium","Low"))))` |
| M | Residual P (1-4) | User-entered (optional) |
| N | Residual I (1-4) | User-entered (optional) |
| O | **Residual Score** | `=IF(OR(M{row}="",N{row}=""),"",M{row}*N{row})` |
| P | **Residual Rating** | `=IF(O{row}="","",IF(O{row}>=12,"Critical",IF(O{row}>=8,"High",IF(O{row}>=4,"Medium","Low"))))` |
| Q | Response/Mitigation | Static |
| R | Owner | Static |
| S | Status | Static |
| T | Target Close | Static |
| U | Actions | Static |

## Formula Definitions (Python)

```python
def inherent_score(row):
    return f"=I{row}*J{row}"

def inherent_rating(row):
    return f'=IF(K{row}="","",IF(K{row}>=12,"Critical",IF(K{row}>=8,"High",IF(K{row}>=4,"Medium","Low"))))'

def residual_score(row):
    return f'=IF(OR(M{row}="",N{row}=""),"",M{row}*N{row})'

def residual_rating(row):
    return f'=IF(O{row}="","",IF(O{row}>=12,"Critical",IF(O{row}>=8,"High",IF(O{row}>=4,"Medium","Low"))))'
```

## Dashboard COUNTIF Pattern

```python
last_data_row = 5 + len(risks)

# KPI counts
ws["C5"].value = f"=COUNTA('Risk Register'!C6:C{last_data_row})"
ws["D6"].value = f"=COUNTIF('Risk Register'!L6:L{last_data_row},\"Critical\")"
ws["E6"].value = f"=COUNTIF('Risk Register'!L6:L{last_data_row},\"High\")"

# Category distribution
for ci, code in enumerate(["SCH","DES","FLS","MEP","APP","COM","PRC"], 2):
    ws.cell(row=21, column=ci).value = f"=COUNTIF('Risk Register'!D6:D{last_data_row},\"{code}\")"

# Status breakdown
for ci, s in enumerate(["Open","Watch","Mitigated","Closed"], 2):
    ws.cell(row=11, column=ci).value = f"=COUNTIF('Risk Register'!S6:S{last_data_row},\"{s}\")"
```

## Risk Matrix COUNTIFS Pattern (4×4)

```python
for prob in range(4, 0, -1):
    rn = 6 + (4 - prob)
    for imp in range(1, 5):
        cn = 2 + imp
        ws.cell(row=rn, column=cn).value = \
            f"=COUNTIFS('Risk Register'!I6:I{last_data_row},{prob},'Risk Register'!J6:J{last_data_row},{imp})"
```

## Heat Map Colors (Score-Based)

| Score | Range | Fill | Font |
|-------|-------|------|------|
| 16 | Critical | `#FF4444` | White bold |
| 12 | Critical | `#FF4444` | White bold |
| 9 | High | `#FF8C00` | White bold |
| 8 | High | `#FF8C00` | White bold |
| 6 | Medium | `#FFD700` | `#333333` |
| 4 | Medium | `#FFD700` | `#333333` |
| 3 | Low | `#90EE90` | `#333333` |
| 2 | Low | `#90EE90` | `#333333` |
| 1 | Low | `#90EE90` | `#333333` |

## Cover Sheet Live Metrics

```python
metrics = [
    ("Total Risks", f"=COUNTA('Risk Register'!C6:C{last_data_row})"),
    ("Critical",    f"=COUNTIF('Risk Register'!L6:L{last_data_row},\"Critical\")"),
    ("High",        f"=COUNTIF('Risk Register'!L6:L{last_data_row},\"High\")"),
    ("Medium",      f"=COUNTIF('Risk Register'!L6:L{last_data_row},\"Medium\")"),
    ("Low",         f"=COUNTIF('Risk Register'!L6:L{last_data_row},\"Low\")"),
    ("Open",        f"=COUNTIF('Risk Register'!S6:S{last_data_row},\"Open\")"),
]
```

## Pitfalls

- **`last_data_row` off-by-one** — data starts at row 6, so `last_data_row = 5 + len(risks)`. 
  An error here breaks ALL COUNTIF ranges silently.
- **Residual columns start blank** — formulas use `IF(OR(...=""),"",...)` to return empty 
  until user fills values. Never pre-fill with inherent values.
- **Severity fills on formula cells** — apply fill based on *static* data (known score), 
  not formula result. The fill is visual aid, not computation.
- **Freeze panes** at `F6` so ID/RBS stay visible while scrolling risk events.
- **AutoFilter** must extend to all data columns: `ws.auto_filter.ref = f"B5:T{last_data_row}"`.
- **Cross-sheet references break if sheet renamed** — Dashboard formulas reference 
  `'Risk Register'!...`. Keep the sheet name stable.
- **String parameter ordering** — `add_risk(rid, cat, title, event, cause, consequence, 
  response, prob, sev, owner)`. Five strings BEFORE two integers. A missing string shifts 
  all params and causes cryptic `missing required positional argument` errors.
