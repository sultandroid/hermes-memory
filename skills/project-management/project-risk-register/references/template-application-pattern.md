# Template Application Pattern — Apply One Register's Styling to Another

## When to Use

- User says "use the same template of [existing_register] to [target_register]"
- User wants one register's column layout, styling, sheets, and chart structure replicated onto another existing register
- Target register has different column count / different structure than source
- Both are existing `.xlsx` files with data worth preserving

## Workflow

### Phase 1: Audit Both Files

Read both workbooks to understand structure, then plan the mapping.

```python
import openpyxl

# Source (the template)
wb_src = openpyxl.load_workbook(src_path)
for s in wb_src.sheetnames:
    ws = wb_src[s]
    print(f'Sheet: {s}, Rows: {ws.max_row}, Cols: {ws.max_column}')
    print(f'  Merged: {list(ws.merged_cells.ranges)}')
    if ws._charts:
        print(f'  Charts: {len(ws._charts)}')

# Target (the data to migrate)
wb_tgt = openpyxl.load_workbook(tgt_path)
for s in wb_tgt.sheetnames:
    ws = wb_tgt[s]
    print(f'Sheet: {s}, Rows: {ws.max_row}, Cols: {ws.max_column}')
    for row in ws.iter_rows(min_row=1, max_row=5, values_only=True):
        vals = [str(v)[:40] for v in row if v is not None]
        if vals: print(f'  {vals}')
```

Collect exactly:
- Source sheet names, merged cells, column widths, freeze panes, auto-filter, charts
- Source header row styling (font name, size, bold, color, fill, alignment, border) — row by row, cell by cell
- Target data rows (all of them) — preserve every field
- Any sheets in target that should be preserved (e.g. `Cover` with project metadata)

### Phase 2: Map Data Columns

Map target's old columns into source's new column layout. Typical risk register mappings:

| Old Column (Target) | New Column (Source Template) | Notes |
|---------------------|-----------------------------|-------|
| Risk ID | Risk ID (col B) | Keep as-is |
| Risk Category | RBS Category (col C) | Map category name to RBS code (TEC/SCH/PRO/etc.) |
| Risk Description | Risk Event (col D) + Cause (col E) | Split on ` — ` delimiter if present |
| Consequences | Impact (col F) | Direct mapping |
| P | Prob (col G) | May need 1-4 to 1-5 rescaling |
| I | Impact (col H) | Keep as-is |
| (computed) | PxI (col I) | = prob x impact |
| (computed) | Severity (col J) | Based on PxI per source's thresholds |
| Response Strategy | Response Strategy (col K) | Derive from mitigation approach |
| Mitigation Action | Response Action (col L) | Direct mapping |
| Owner / Escalation | Risk Owner (col M) | Map codes to readable names |
| Status | Status (col N) | Uppercase: Open/Mitigated/Watch/Closed |
| Target Close | Target Close (col O) | Preserve if exists; else None |
| ID'd | ID'd (col P) | Preserve if exists; else None |
| Last Review | Last Review (col Q) | Today's date as fallback |
| Residual P/R/S | Resid. Prob/Impact/PxI (R/S/T) | Preserve if exists; else None |
| Contingency Plan | Contingency Plan (col U) | Preserve if exists; else None |
| Trigger | Trigger / Early Warning (col V) | Preserve if exists; else None |
| Linked Risks | Linked Risks (col W) | Preserve if exists; else None |
| Source / Notes | Evidence Source (col X) | Document name or "Design Risk Register" |

### Phase 3: Preserve Project-Specific Sheets

If the target has a `Cover` sheet with project metadata (doc number, revision, date, parties), **preserve it but restyle** to match source's navy theme:

```python
ws_cover = wb.create_sheet('Cover', 0)  # first sheet
# Set column widths to match source proportions
# Apply navy fill (#0F172A) to section titles
# Apply Inter font, consistent alignment
# Keep owner codes and status definitions
```

### Phase 4: Build Main Register Sheet

Apply the full source template styling:

```python
NAVY = 'FF0F172A'
NAVY_FILL = PatternFill('solid', fgColor=NAVY)
HEADER_FONT = Font(name='Inter', size=8, bold=True, color='FFFFFFFF')
BODY_FONT = Font(name='Inter', size=8)
TITLE_FONT = Font(name='Inter', size=12, bold=True, color=NAVY)
SUBTITLE_FONT = Font(name='Inter', size=7, color='FF64748B')
THIN_BORDER = Border(left=Side('thin', 'FFCBD5E1'), right=Side('thin', 'FFCBD5E1'),
                     top=Side('thin', 'FFCBD5E1'), bottom=Side('thin', 'FFCBD5E1'))
LIGHT_GRAY = PatternFill('solid', fgColor='FFF8FAFC')
```

Row structure:
- Row 1: merged title row — project name + register type + doc control ref
- Row 2: merged subtitle — classification + description
- Row 3: column headers — Inter 8pt bold white, fill #0F172A, center/center/wrap, thin borders
- Row 4+: data — alternating rows (no fill / #F8FAFC), RBS cat in light green (#D1FAE5), severity color-coded, status color-coded

### Phase 5: Add Supplementary Sheets

**RBS & Scoring Guide** — customize RBS categories for the target domain, then add:
- Probability scale (1-5) with % ranges
- Impact scale (1-5) with cost/schedule descriptions
- PxI heat map (5x5 matrix) with color bands
- Severity bands with required actions

**Dashboard** — compute from migrated data:
- KPI cards (Total, Open, Mitigated, Watch, High, Critical)
- RAG Health (RED/AMBER/GREEN based on High+Critical count)
- Donut chart for status distribution
- Bar chart for severity distribution
- Risk Category Breakdown table
- Top 8 Risks by PxI
- Risk Owner Workload analysis
- Risk Register Health Check checklist

### Phase 6: Data Validation

```python
dv_severity = DataValidation(type='list', formula1='"Critical,High,Medium,Low,Very Low"', allow_blank=True)
dv_prob = DataValidation(type='list', formula1='"1,2,3,4,5"', allow_blank=True)
dv_status = DataValidation(type='list', formula1='"Open,Mitigated,Watch,Closed"', allow_blank=True)
dv_response = DataValidation(type='list', formula1='"Avoid,Mitigate,Transfer,Accept,Escalate"', allow_blank=True)
```

### Phase 7: Final Touches

```python
ws.freeze_panes = 'A4'
ws.auto_filter.ref = f'A3:X{3 + len(risks)}'
ws.sheet_view.showGridLines = False
ws.page_setup.orientation = 'landscape'
ws.page_setup.fitToWidth = 1
```

### Phase 8: Verify

After saving:
1. Re-open and check sheet names, counts, chart presence, freeze panes, filter
2. Spot-check data migration on a few rows
3. Verify severity/status colors
4. Check Cover preserved and restyled
5. Confirm all supplementary sheets exist

## Category-to-RBS Mapping Example (Design Register)

| Target Category | RBS Code | RBS Name |
|----------------|----------|----------|
| Design Baseline | TEC | Technical / Design |
| Coordination | TEC | Technical / Design |
| Exhibition | TEC | Technical / Design |
| Technical | TEC | Technical / Design |
| BIM/Digital | TEC | Technical / Design |
| Quality Assurance | QA | Quality & Compliance |
| Commercial | COM | Commercial / Contract |
| Programme | SCH | Schedule / Programme |
| Resource | PRO | Procurement / Supply Chain |
| Statutory | EXT | External / Regulatory |

## Severity Bands (PxI 1-5 scale)

| Range | Severity | Fill | Action |
|-------|----------|------|--------|
| 20-25 | Critical | #FEE2E2 | CG/MoC escalation, weekly review |
| 12-19 | High | #FEF3C7 | PM escalation, monthly review |
| 8-11 | Medium | #FEF9C3 | Mitigate, 4-week response |
| 4-7 | Low | #DBEAFE | Accept, monthly review |
| 1-3 | Very Low | #F0FDF4 | Accept, document & monitor |

## Status Colors

| Status | Fill |
|--------|------|
| Open | #FFFEF2F2 |
| Mitigated | #FFFEF9C3 |
| Watch | #FFFFF7ED |
| Closed | #FFF0FDF4 |

## Pitfalls

- **Preserve Cover sheet** — don't delete it. It carries doc control info, revision history, owner codes, and status definitions. Restyle it instead.
- **Scoring scale mismatch** — source may use P 1-5, target P 1-4. Either rescale or use source thresholds. Document on Cover.
- **Description splitting** — the 24-column template splits into Risk Event + Cause. If descriptions are single-field, keep full text in Risk Event and create a generic cause reference.
- **DataPoint import** — `from openpyxl.chart import DataPoint` raises ImportError. Use `from openpyxl.chart.series import DataPoint`.
- **Chart data in worksheet** — donut/bar charts need data rows in the sheet. Place status/severity counts in rows 11-16 (below KPI row 9) for chart references to work.
