# Comprehensive Risk Register Pattern

## Structure

6 sheets in a single workbook:

| Sheet | Content |
|-------|---------|
| **Dashboard** | Metric boxes (formula-linked to PRR), distribution table + bar chart, top 5 critical risks, register status summary, review cadence |
| **Master Risk Register (PRR)** | All 49 project-level risks, 14 columns, formula-based scoring |
| **Design Risk Register (DDR)** | Design-originated risks, same 14-column template |
| **HSE Risk Register** | Task-level HSE risks, same 14-column template |
| **AV Risk Register** | AV/multimedia risks, same 14-column template |
| **Reference** | Scoring scales, response strategies, status definitions |

## Unified 14-Column Template (ALL register sheets)

| # | Column | Type | Notes |
|---|--------|------|-------|
| 1 | ID | Text | Risk ID (PRR-XXX-XX, DDR-XXX, etc.) |
| 2 | Category / Discipline | Text | RBS category or discipline name |
| 3 | Risk Event | Text | What could happen |
| 4 | Cause / Hazard | Text | Root cause or trigger |
| 5 | Impact / Consequence | Text | Effect on project objectives |
| 6 | Probability | Number | 1-4 (PRR/AV) or 1-5 (DDR/HSE) |
| 7 | Severity | Number | 1-4 (PRR/AV) or 1-5 (DDR/HSE) |
| 8 | Score | **Formula** | `=F{r}*G{r}` (P × S) |
| 9 | Rating | **Formula** | `=IF(H{r}>=12,"Critical",IF(H{r}>=8,"High",...))` |
| 10 | Response Strategy | **Dropdown** | Avoid, Transfer, Mitigate, Accept (Active), Accept (Passive), SOW-Protect |
| 11 | Mitigation / Controls | Text | Response actions |
| 12 | Risk Owner | Text | Named person |
| 13 | Target Close | Date | Target resolution date |
| 14 | Status | Text | Open / Watch / Mitigated / Closed / LIVE |

## Column Widths

A=14, B=22, C=35, D=30, E=30, F=10, G=10, H=10, I=10, J=18, K=40, L=20, M=14, N=14

## Dashboard Formulas

- Total risks: `=COUNTA('Master Risk Register'!A2:A100)`
- Critical count: `=COUNTIF('Master Risk Register'!I2:I100,"Critical")`
- High count: `=COUNTIF('Master Risk Register'!I2:I100,"High")`
- Distribution by category: `=COUNTIF('Master Risk Register'!B:B,"*CategoryName*")`
- Distribution critical: `=COUNTIFS('Master Risk Register'!B:B,"*CategoryName*",'Master Risk Register'!I:I,"Critical")`

## Rating Thresholds by Register

| Register | Critical | High | Medium | Low |
|----------|----------|------|--------|-----|
| PRR (P×S 1-4) | ≥12 | ≥8 | ≥4 | <4 |
| DDR (P×I 1-5) | ≥16 | ≥10 | ≥5 | <5 |
| HSE (C×L 1-5) | ≥16 | ≥10 | ≥5 | <5 |
| AV (P×S 1-4) | ≥12 | ≥8 | ≥4 | <4 |

## Response Strategy Dropdown

`"Avoid,Transfer,Mitigate,Accept (Active),Accept (Passive),SOW-Protect"`

Per RMP §8.1. Applied to column J on all register sheets.

## Styling

- Header: Calibri 10pt bold white on navy `#1E293B` fill
- Body: Calibri 9pt `#1F293B` on alternating `#F1F5F9` / white rows
- Critical rating: red fill `#FEE2E2`, bold red font `#DC2626`
- High rating: amber fill `#FEF3C7`, bold amber font `#D97706`
- Open/LIVE status: amber fill
- Thin borders `#E2E8F0` on all cells
- Auto-filter on all columns
- Frozen header row (A2)

## Data Source

PRR data comes from the repo `01_Registers/risk_register.md` or `06_Risk_System/risks.json`.
DDR/HSE/AV data comes from the C09 consolidated Excel workbook at `09_Registers/23_Project_Risk_Register/`.

## SOW-Protect Pattern

For risks that are Employer responsibilities (not in Samaya's scope):
- Add "SOW-PROTECT:" prefix to the response action
- Note in evidence column: "SOW-PROTECT: [description of Employer responsibility]"
- Example: "SOW-PROTECT: artifact damage liability, ICOM accreditation, and loan conditions are Employer responsibilities — not in Samaya scope"

## Risk Review Workflow (per PM preference)

1. Show full risk data: ID, category, event, cause, consequence, P, S, score, rating, owner, status, target
2. State the action needed clearly: "Action needed: ..."
3. Ask for update
4. If user says "no" or provides update, update the risk in both `risk_register.md` and `risks.json`
5. Move to next risk
