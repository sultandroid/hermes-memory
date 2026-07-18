# Comprehensive Risk Register Excel — Generation Pattern

**When to use:** User asks to create a comprehensive project risk register with dashboard, or to populate an existing template with live data from the C09 consolidated register.

## Workbook structure

| Sheet | Content | Source |
|-------|---------|--------|
| Dashboard | Metric boxes, distribution chart, top 5 risks, register status, review cadence | Computed from PRR data |
| Master Risk Register | 20-column full register with all 49 risks | C09 Excel |
| Design Risk Register | Template for 77 DDR risks | Empty template |
| HSE Risk Register | Template for 41 HSE risks | Empty template |
| AV Risk Register | Template for ~30 AV risks | Empty template |
| Reference | Scoring scales, response strategies, status definitions | Plan methodology |

## Dashboard layout

### Metric boxes (row 5-6)
```
B5: Total Risks (49)  C5: Critical (16)  D5: High (12)  E5: Medium (20)  F5: Low (1)
B6: label              C6: label          D6: label       E6: label         F6: label
```
Use 20pt bold navy font, `#F8FAFC` background, thin borders. Merge cells vertically (row+1 for label).

### Risk distribution table (row 11+)
Headers: Category | Code | Total | Critical | High
Data: sorted by total descending, with total row at bottom.
Color-code: Critical ≥2 = red bold, High ≥2 = amber bold.

### Bar chart
Column chart from distribution data. Place at `B{total_row + 2}`. Remove old chart before adding new one when updating.

### Top 5 Critical risks
Headers: Risk ID | Category | Risk Event | P | S | Score | Owner | Status
Data: sorted by score descending, filtered to Critical only. LIVE status = red fill.

### Register status summary
Headers: Register | Code | Count | Scoring | Status
Active = green fill, In Progress = amber fill.

### Review cadence
Headers: Review | Frequency | Lead | Participants
From plan §10.

## Master Risk Register columns (20)

| # | Column | Width | Notes |
|---|--------|-------|-------|
| 1 | Risk ID | 14 | PRR-XXX-XX |
| 2 | Category | 22 | Full category name |
| 3 | RBS Code | 10 | SCH, DES, COM, etc. |
| 4 | Risk Event | 35 | What could happen |
| 5 | Consequence / Impact | 35 | What happens if it materialises |
| 6 | Cause / Source | 25 | Root cause |
| 7 | P (1-4) | 8 | Probability |
| 8 | S (1-4) | 8 | Severity |
| 9 | Score (PxS) | 10 | 1-16 |
| 10 | Rating | 10 | Critical/High/Medium/Low |
| 11 | Response Strategy | 16 | Avoid/Transfer/Mitigate/Accept/SOW-Protect |
| 12 | Mitigation / Action Plan | 40 | Specific actions |
| 13 | Residual P | 8 | After mitigation |
| 14 | Residual S | 8 | After mitigation |
| 15 | Residual Score | 10 | After mitigation |
| 16 | Risk Owner | 18 | Named person |
| 17 | Target Close | 14 | Date |
| 18 | Status | 14 | Open/LIVE/Watch/Mitigated/Closed |
| 19 | Review Date | 14 | Last review |
| 20 | Notes / Evidence | 25 | Source references |

## Data extraction from C09

The C09 consolidated register has the Master Risk Register sheet with data starting at row 5, columns B-K:

| C09 Col | Field |
|---------|-------|
| B | Risk ID |
| C | Category |
| D | Rating |
| E | Score |
| F | Status |
| G | Owner |
| H | Risk Event |
| I | Consequence |
| J | Response / Mitigation |
| K | Target Close |

## Styling

- Navy `#1E293B` header row, white bold 10pt Calibri
- Alternating body rows `#FFFFFF` / `#F1F5F9`, 9pt Calibri
- Critical rating = red fill `#FEE2E2` + red bold font
- High rating = amber fill `#FEF3C7` + amber bold font
- LIVE status = amber fill
- Active status = green fill `#DCFCE7`
- Thin borders `#E2E8F0`
- Auto-filter on all data columns
- Frozen header row

## Updating existing register

When the C09 data changes, re-run the extraction and rebuild the Master Risk Register sheet. The Dashboard metrics and chart auto-update from the data. The DDR, HSE, and AV sheets remain as templates (not auto-populated from C09).
