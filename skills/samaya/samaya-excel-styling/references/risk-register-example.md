# Risk Register Styling Session — Aseer Museum Consolidated Risk Register

File: `Aseer_Museum_Consolidated_Risk_Register_v2.0.xlsx`
Sheets: 13 (Cover, Risk Register, Dashboard, Risk Matrix, Treatment Plan, DRR, DRR Status Audit, DRR Duplicate Check, HSE, AV Risk Register, HSE Exclusions, Methodology, Change Log)

## Key Approach

The workbook had formula-driven severity columns (e.g. `=IF(K>=12,"Critical",IF(K>=8,"High",...))`) with **no cached values** because openpyxl created the workbook and it was never opened in Excel. `data_only=True` returned `None` for all formula cells.

**Solution:** Two-pass pattern:
1. Open with `data_only=True` to read static source columns (I=Probability, J=Impact = both static integers)
2. Compute score = I×J, map to severity bands (Critical≥12, High≥8, Medium≥4, Low)
3. Open with `data_only=False` (default) for actual styling

## Sheet-by-Sheet Structure

| Sheet | Data Range | Header Row | Key Columns |
|-------|-----------|------------|-------------|
| Cover | B2:F18 | — | Metrics B8:C13, Index E8:F18 |
| Risk Register | B6:U54 | Row 5 | I=Prob, J=Impact, K=I*J, L=Inherent Rating, O=Resid Score, P=Resid Rating |
| Dashboard | B5:S42 | Row 5 KPI | Row 6=KPI values, Row 10=Status, Row 15=Rating, Row 20=RBS, Row 26=Watchlist |
| Risk Matrix | B5:G9 + B12:G21 | Row 5 | P×I heat map (P=4,3,2,1 × I=1,2,3,4) |
| Treatment Plan | B6:I33 | Row 5 (GOLD) | Risk ID, Strategy, Actions, Owner, Target Close, Treatment File |
| DRR | A4:X82 | Row 3 | A=#, B=RiskID, G=Prob, H=Impact, I=P×I, J=Severity, R=ResProb, S=ResImpact |
| DRR Status Audit | A6:H101 | Row 5 | A=RiskID, C=Severity, F=Audit Status |
| DRR Duplicate Check | A2:G80 | Row 1 | A=Seq, B=RiskID, E=Severity; Review section rows 83-97 |
| HSE | B7:M47 | Row 6 | B=Ref, C=Activity, F=C, G=L, H=Init Score; I=C, J=L, K=Res Score |
| AV Risk Register | B7:M50 | Row 6 | Same structure as HSE |
| HSE Exclusions | B6:D25 | Row 5 | B=HSE Sec, C=Excluded Activity, D=Reason |
| Methodology | B4:F47 | Varies | Section headers at rows 4,11,18,24,30,37 |
| Change Log | B5:E15 | Row 4 | B=Version, C=Date, D=Author, E=Change |

## Severity Score Bands (1-4 scale)

| Score | Rating | Color |
|-------|--------|-------|
| ≥12 | Critical | Red #FF4444 |
| 8-11 | High | Orange #FF8C00 |
| 4-7 | Medium | Yellow #FFD700 |
| 1-3 | Low | Green #90EE90 |

## Special Notes

- **Dashboard row 6**: KPI data row uses COUNTIF formulas referencing Risk Register sheet
- **Risk Matrix**: P×I cells colored by score; P=4 row has all I=1(4→Yellow), I=2(8→Orange), I=3(12→Red), I=4(16→Red)
- **Treatment Plan**: Uses gold (#C9A84C) headers instead of navy to differentiate from main register
- **DRR Duplicate Check**: Has two sections — data rows (2-80) and overlap review summary (83-97)
- **Methodology**: Section headers at rows 4, 11, 18, 24, 30, 37 should use navy background
- **Residual columns (M,N,O,P)** in Risk Register: formulas reference Response and Owner (text) × Status (text) — these will always be empty/error in openpyxl-generated workbooks
