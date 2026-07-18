# Unified Register Template

When building a multi-sheet risk register workbook, ALL register sheets must use the **exact same 14-column template** with identical headers, widths, and formatting.

## Standard 14-Column Template

| # | Column | Width | Type |
|---|--------|-------|------|
| 1 | ID | 14 | Text |
| 2 | Category / Discipline | 22 | Text |
| 3 | Risk Event | 35 | Text |
| 4 | Cause / Hazard | 30 | Text |
| 5 | Impact / Consequence | 30 | Text |
| 6 | Probability | 10 | Number |
| 7 | Severity | 10 | Number |
| 8 | Score | 10 | **Formula** (P × S) |
| 9 | Rating | 10 | **Formula** (IF) |
| 10 | Response Strategy | 18 | **Dropdown** (6 options) |
| 11 | Mitigation / Controls | 40 | Text |
| 12 | Risk Owner | 20 | Text |
| 13 | Target Close | 14 | Text |
| 14 | Status | 14 | Text |

## Rules

- Every sheet gets the same 14 columns in the same order
- Every sheet gets the same column widths
- Every sheet gets the same header style (navy fill, white bold 10pt Calibri)
- Every sheet gets the same body style (9pt Calibri, alternating rows)
- Every sheet gets the same dropdown on Response Strategy (column J)
- Every sheet gets auto-filter + frozen header row
- Score and Rating are always FORMULAS, never hardcoded values
- Dashboard COUNTIF/COUNTIFS formulas reference the PRR sheet's Rating column (I) and Category column (B)

## Scoring Formulas by Register Type

| Register | Score Formula | Rating Formula |
|----------|--------------|----------------|
| PRR | `=F{r}*G{r}` | `=IF(H{r}>=12,"Critical",IF(H{r}>=8,"High",IF(H{r}>=4,"Medium","Low")))` |
| DDR | `=F{r}*G{r}` | `=IF(H{r}>=16,"Critical",IF(H{r}>=10,"High",IF(H{r}>=5,"Medium","Low")))` |
| HSE | `=F{r}*G{r}` | `=IF(H{r}>=16,"Critical",IF(H{r}>=10,"High",IF(H{r}>=5,"Medium","Low")))` |
| AV | `=IF(F{r}="","",F{r}*G{r})` | `=IF(H{r}="","",IF(H{r}>=12,"Critical",IF(H{r}>=8,"High",IF(H{r}>=4,"Medium","Low"))))` |

## Dropdown for Response Strategy

```python
dv = DataValidation(
    type="list",
    formula1='"Avoid,Transfer,Mitigate,Accept (Active),Accept (Passive),SOW-Protect"',
    allow_blank=True,
    showDropDown=False
)
ws.add_data_validation(dv)
dv.add(f'J2:J{last_row}')
```

## Cleanup Stale Dropdowns

After rebuilding sheets, clear all existing data validations and add a single one:

```python
ws.data_validations.dataValidation = []
# then add single dropdown as above
```

## Dashboard Formulas After Template Change

```python
ws.cell(row=5, column=3).value = f'=COUNTIF({prr_sheet}!I2:I100,"Critical")'
ws.cell(row=5, column=4).value = f'=COUNTIF({prr_sheet}!I2:I100,"High")'
ws.cell(row=5, column=5).value = f'=COUNTIF({prr_sheet}!I2:I100,"Medium")'
ws.cell(row=5, column=6).value = f'=COUNTIF({prr_sheet}!I2:I100,"Low")'
```

## Risk Close vs Mitigate

When a risk's root cause is eliminated (the specific threat no longer exists), set status to **Closed**, not Mitigated. "Mitigated" means the risk still exists but controls have reduced it. "Closed" means the risk event cannot happen anymore.

Example: PRR-CON-03 (blockwork mandate) — CG approved drywall, so the blockwork threat is gone → **Closed**. The residual coordination work is normal design development, not a risk.
