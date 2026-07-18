---
name: samaya-excel-styling
description: Apply Samaya brand styling to Excel workbooks using openpyxl — headers, severity fills, heat maps, row striping, auto-fit, freeze panes, and formula-cell handling.
domain: productivity/samaya
triggers:
  - "Apply Samaya branding to an Excel file"
  - "Style/fix/format an Excel workbook or risk register"
  - "Excel formatting with openpyxl"
  - "Brand-colored Excel headers and fills"
---

# Samaya Excel Styling with openpyxl

Apply consistent Samaya-brand formatting to Excel workbooks (.xlsx) using openpyxl. Covers headers, fills, borders, severity coloring, heat maps, auto-fit, freeze panes, and the critical pattern for handling formula cells with no cached values.

## Brand Colors

| Token | Hex | Usage |
|-------|-----|-------|
| Navy | `#1F3864` | Primary headers, titles, section accents |
| Gold | `#C9A84C` | Secondary headers (Treatment Plan, Cover metrics) |
| Light Grey | `#F2F4F7` | Alternating row stripes |
| Border Grey | `#D0D0D0` | Thin cell borders |
| Critical Red | `#FF4444` | Critical severity, heat-map top band |
| High Orange | `#FF8C00` | High severity, heat-map middle band |
| Medium Yellow | `#FFD700` | Medium severity, heat-map low band |
| Low Green | `#90EE90` | Low severity |

## Font

- **Default data**: Calibri 9pt
- **Headers**: Calibri 10pt bold, white font on navy/gold fill
- **Titles**: Calibri 14pt bold, navy
- **Severity**: Calibri 9pt bold, white on red/orange, black on yellow/green

## Core Reusable Patterns

### Severity Fill Map
```python
SEVERITY_MAP = {
    "critical": (PatternFill(start_color="FF4444", end_color="FF4444", fill_type="solid"),
                 Font(name="Calibri", size=9, bold=True, color="FFFFFF")),
    "high":     (PatternFill(start_color="FF8C00", end_color="FF8C00", fill_type="solid"),
                 Font(name="Calibri", size=9, bold=True, color="FFFFFF")),
    "medium":   (PatternFill(start_color="FFD700", end_color="FFD700", fill_type="solid"),
                 Font(name="Calibri", size=9, bold=True, color="000000")),
    "low":      (PatternFill(start_color="90EE90", end_color="90EE90", fill_type="solid"),
                 Font(name="Calibri", size=9, bold=True, color="000000")),
}
```

### Auto-Fit Columns (CJK-aware)
```python
def auto_fit_columns(ws):
    for col_cells in ws.columns:
        max_len = 0; col_letter = None
        for cell in col_cells:
            if col_letter is None:
                col_letter = get_column_letter(cell.column)
            val = str(cell.value) if cell.value is not None else ""
            for line in val.split("\n"):
                length = sum(2 if ord(c) > 127 else 1 for c in line)
                if length > max_len: max_len = length
        if col_letter and max_len > 0:
            adjusted = min(max_len + 3, 55)
            ws.column_dimensions[col_letter].width = max(adjusted, 5)
```

### Navy Header Row
```python
def apply_navy_headers(ws, row, min_col, max_col):
    for col_idx in range(min_col, max_col + 1):
        cell = ws.cell(row=row, column=col_idx)
        cell.font = Font(name="Calibri", size=10, bold=True, color="FFFFFF")
        cell.fill = PatternFill(start_color="1F3864", end_color="1F3864", fill_type="solid")
        cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
```

### Alternating Row Stripes
```python
def apply_striping(ws, min_row, max_row, min_col, max_col):
    for row_idx in range(min_row, max_row + 1):
        fill = PatternFill(start_color="F2F4F7", end_color="F2F4F7", fill_type="solid") \
               if (row_idx % 2 == 0) else PatternFill(start_color="FFFFFF", end_color="FFFFFF", fill_type="solid")
        for col_idx in range(min_col, max_col + 1):
            ws.cell(row=row_idx, column=col_idx).fill = fill
```

### Thin Borders
```python
THIN_BORDER = Border(
    left=Side(style="thin", color="D0D0D0"),
    right=Side(style="thin", color="D0D0D0"),
    top=Side(style="thin", color="D0D0D0"),
    bottom=Side(style="thin", color="D0D0D0"),
)
```

## Unified Register Template (14-Column Standard)

All risk registers (PRR, DDR, HSE, AV) must use the **identical 14-column template** with same headers, widths, and column types:

| # | Column | Type | Notes |
|---|--------|------|-------|
| 1 | ID | Text | Risk identifier |
| 2 | Category / Discipline | Text | RBS category or discipline name |
| 3 | Risk Event | Text | What could happen |
| 4 | Cause / Hazard | Text | Root cause or hazard |
| 5 | Impact / Consequence | Text | Effect if risk materialises |
| 6 | Probability | Number | P score (1-4 or 1-5 per scale) |
| 7 | Severity | Number | S/I/C score (1-4 or 1-5 per scale) |
| 8 | Score | **Formula** | `=F{row}*G{row}` — P × S |
| 9 | Rating | **Formula** | `=IF(H{row}>=12,"Critical",IF(H{row}>=8,"High",...))` |
| 10 | Response Strategy | **Dropdown** | Avoid, Transfer, Mitigate, Accept (Active), Accept (Passive), SOW-Protect |
| 11 | Mitigation / Controls | Text | Response actions or control measures |
| 12 | Risk Owner | Text | Named person |
| 13 | Target Close | Text | Target date |
| 14 | Status | Text | Open / LIVE / Mitigated / Closed |

```python
UNIFIED_HEADERS = [
    "ID", "Category / Discipline", "Risk Event", "Cause / Hazard",
    "Impact / Consequence", "Probability", "Severity", "Score",
    "Rating", "Response Strategy", "Mitigation / Controls",
    "Risk Owner", "Target Close", "Status"
]
UNIFIED_WIDTHS = [14, 22, 35, 30, 30, 10, 10, 10, 10, 18, 40, 20, 14, 14]
```

### Building a Unified Register Sheet

```python
def build_unified_sheet(ws, data_rows, score_formula, rating_formula):
    clear_sheet(ws)
    for ci, (h, w) in enumerate(zip(UNIFIED_HEADERS, UNIFIED_WIDTHS), 1):
        ws.cell(row=1, column=ci, value=h)
        ws.column_dimensions[get_column_letter(ci)].width = w
    style_header(ws, 1, len(UNIFIED_HEADERS))
    
    for ri, row_data in enumerate(data_rows, 2):
        alt = (ri - 2) % 2 == 1
        for ci, val in enumerate(row_data, 1):
            style_cell(ws, ri, ci, alt).value = val
        ws.cell(row=ri, column=8).value = score_formula(ri)
        ws.cell(row=ri, column=9).value = rating_formula(ri)
    
    # Dropdown for Response Strategy (col 10)
    dv = DataValidation(type="list",
        formula1='"Avoid,Transfer,Mitigate,Accept (Active),Accept (Passive),SOW-Protect"',
        allow_blank=True, showDropDown=False)
    ws.add_data_validation(dv)
    dv.add(f'J2:J{len(data_rows)+1}')
    
    ws.auto_filter.ref = f"A1:N{len(data_rows)+1}"
    ws.freeze_panes = "A2"
```

### Dashboard Cross-Sheet Formulas

Dashboard metrics must use COUNTIF/COUNTIFS referencing the PRR sheet, not hardcoded numbers:

```python
prr_sheet = "'Master Risk Register'"
ws.cell(row=5, column=3).value = f'=COUNTIF({prr_sheet}!I2:I100,"Critical")'
ws.cell(row=5, column=4).value = f'=COUNTIF({prr_sheet}!I2:I100,"High")'
ws.cell(row=5, column=5).value = f'=COUNTIF({prr_sheet}!I2:I100,"Medium")'
ws.cell(row=5, column=6).value = f'=COUNTIF({prr_sheet}!I2:I100,"Low")'
```

Distribution by category uses COUNTIFS:
```python
ws.cell(row=ri, column=4).value = f'=COUNTIF({prr_sheet}!B:B,"*{category}*")'
ws.cell(row=ri, column=5).value = f'=COUNTIFS({prr_sheet}!B:B,"*{category}*",{prr_sheet}!I:I,"Critical")'
```

### Rating Formula by Scoring Scale

| Register | Scale | Score Formula | Rating Formula |
|----------|-------|---------------|----------------|
| PRR (Master) | P×S 1-4 | `=F{r}*G{r}` | `=IF(H{r}>=12,"Critical",IF(H{r}>=8,"High",IF(H{r}>=4,"Medium","Low")))` |
| DDR (Design) | P×I 1-5 | `=F{r}*G{r}` | `=IF(H{r}>=16,"Critical",IF(H{r}>=10,"High",IF(H{r}>=5,"Medium","Low")))` |
| HSE | C×L 1-5 | `=F{r}*G{r}` | `=IF(H{r}>=16,"Critical",IF(H{r}>=10,"High",IF(H{r}>=5,"Medium","Low")))` |
| AV | P×S 1-4 | `=IF(F{r}="","",F{r}*G{r})` | `=IF(H{r}="","",IF(H{r}>=12,"Critical",...))` |

### Clearing Sheets with Merged Cells

When rebuilding a sheet that may have merged cells, unmerge first:
```python
def clear_sheet(ws):
    for mr in list(ws.merged_cells.ranges):
        ws.unmerge_cells(str(mr))
    for ri in range(1, ws.max_row + 1):
        for ci in range(1, ws.max_column + 1):
            ws.cell(row=ri, column=ci).value = None
```

### Dropdown (Data Validation) for Controlled Fields

Response Strategy and similar controlled fields must use dropdown lists, not free-text entry:

```python
from openpyxl.worksheet.datavalidation import DataValidation

strategies = '"Avoid,Transfer,Mitigate,Accept (Active),Accept (Passive),SOW-Protect"'
dv = DataValidation(
    type="list",
    formula1=strategies,
    allow_blank=True,
    showDropDown=False  # False = show dropdown arrow; True = inline only
)
dv.error = "Please select a valid response strategy"
dv.errorTitle = "Invalid Strategy"
dv.prompt = "Select response strategy"
dv.promptTitle = "Response Strategy"
ws.add_data_validation(dv)
dv.add(f'J2:J{last_row}')  # Column J = Response Strategy
```

**Pitfall:** When rebuilding a sheet that already has data validations, old validations accumulate. Always clear them first:
```python
ws.data_validations.dataValidation = []  # Clear all existing
# Then add the single new one
```

### AV Register Blank-Handling Formulas

AV risks often have empty Probability/Severity (not yet scored). Use IF-blank formulas to avoid showing "FALSE" or 0:

```python
# Score formula — blank until P and S filled
ws.cell(row=ri, column=8).value = f'=IF(F{ri}="","",F{ri}*G{ri})'

# Rating formula — blank until score computed
ws.cell(row=ri, column=9).value = f'=IF(H{ri}="","",IF(H{ri}>=12,"Critical",IF(H{ri}>=8,"High",IF(H{ri}>=4,"Medium","Low"))))'
```

### Clearing Sheets with Merged Cells

When rebuilding a sheet that may have merged cells, unmerge first or `MergedCell` attribute errors occur:

```python
def clear_sheet(ws):
    for mr in list(ws.merged_cells.ranges):
        ws.unmerge_cells(str(mr))
    for ri in range(1, ws.max_row + 1):
        for ci in range(1, ws.max_column + 1):
            ws.cell(row=ri, column=ci).value = None
```

### Live Register Note Pattern

Any table showing live register data must carry a halftone note that the register is the authoritative source:

```python
note_text = "Data shown is a snapshot from the live Project Risk Register, which is the authoritative source and updated weekly."
# Insert as a paragraph element after the table in the body
p = OxmlElement('w:p')
# ... build paragraph with 9pt gray text ...
body.insert(table_idx + 1, p)
```

## Critical Pitfall: Formula Cells with No Cached Value

The most common issue when styling openpyxl workbooks: **formula cells created programmatically have no cached values**. Opening with `data_only=True` returns `None` for all formula cells — you cannot read the computed severity string.

**Never do this:**
```python
# Fails — data_only=True returns None for uncalculated formulas
wb = openpyxl.load_workbook(file, data_only=True)
val = ws.cell(row=r, column=12).value  # None if never opened in Excel
```

**Always do this — two-pass compute from source columns:**
```python
# Pass 1: Read the STATIC source columns that feed into the formulas
wb_cache = openpyxl.load_workbook(file, data_only=True)
severity_data = {}
for r in range(data_start, data_end + 1):
    i = wb_cache.cell(row=r, column=prob_col).value    # static int
    j = wb_cache.cell(row=r, column=impact_col).value   # static int
    if isinstance(i, (int, float)) and isinstance(j, (int, float)):
        score = int(i) * int(j)
        if score >= 12:      sev = "critical"
        elif score >= 8:     sev = "high"
        elif score >= 4:     sev = "medium"
        else:                sev = "low"
        severity_data[(r, rating_col)] = sev
wb_cache.close()

# Pass 2: Style with data_only=False (preserves all formulas)
wb = openpyxl.load_workbook(file)
for r in range(data_start, data_end + 1):
    cell = ws.cell(row=r, column=rating_col)
    sev_key = severity_data.get((r, rating_col), "")
    if sev_key:
        fill, font = SEVERITY_MAP[sev_key]
        cell.fill = fill; cell.font = font
wb.save(file)
```

**Rule of thumb:** For any formula-driven cell whose computed value you need for styling, trace the formula back to its leaf-level static-value inputs and compute manually. The formula `=IF(A*B>=12,"Critical",IF(A*B>=8,"High",...))` means you read columns A and B (static), compute `A*B`, map to bands.

## Heat Map Coloring

For a P×I matrix (probability rows × impact columns), color each cell by the score `P × I`:

```python
def heatmap_color(score):
    if score >= 12:  return "FF4444"  # Critical
    if score >= 8:   return "FF8C00"  # High
    if score >= 4:   return "FFD700"  # Medium
    return "90EE90"                   # Low

for row_idx, p in {6: 4, 7: 3, 8: 2, 9: 1}.items():
    for col_idx, i in {3: 1, 4: 2, 5: 3, 6: 4}.items():
        score = p * i
        cell = ws.cell(row=row_idx, column=col_idx)
        cell.fill = PatternFill(start_color=heatmap_color(score),
                                 end_color=heatmap_color(score), fill_type="solid")
        cell.font = Font(name="Calibri", size=12, bold=True,
                         color="FFFFFF" if score >= 12 else "000000")
```

## Typical Sheet Structure Walkthrough

The session that produced this skill styled a 13-sheet risk register. Each sheet type has a pattern:

1. **Cover** — Title row 2, metrics with gold fill, sheet index
2. **Main Register** — Title rows, header row + data with formula-driven severity, freeze panes
3. **Dashboard** — KPI headers, severity-colored distribution headers, red watchlist header
4. **Matrix/Heat Map** — Navy labels, color-coded P×I cells, score bands
5. **Sub-registers** (HSE, AV, DRR) — Same navy header pattern, severity fills on rating column
6. **Change Log** — Navy headers, alternating row stripes

## Reference

See `references/risk-register-example.md` for the full script structure and sheet-by-sheet breakouts from the Aseer Museum risk register session.
