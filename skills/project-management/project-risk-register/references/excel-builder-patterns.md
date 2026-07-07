# Risk Register Excel Builder — Patterns & Code Reference

## 3-Sheet Workbook Structure

| Sheet | Purpose | Key Content |
|-------|---------|-------------|
| `Risk Register` | 31 risks × 24 columns | Full data, severity/staus colors, auto-filter, freeze panes |
| `RBS & Scoring Guide` | Reference sheet | 8 RBS categories, P×I matrix heat map, probability/impact scales |
| `Dashboard` | Executive summary | KPI cards, donut+bar charts, top-8 table, category breakdown, owner workload, health check |

## Risk Data Tuple Format (31 entries)

Each risk is a tuple of 20 fields in this order:

```python
(rid, rbs_cat, event, cause, impact, prob, imp, strategy, resp_action,
 owner, status, target_close, date_id, last_review, res_prob, res_imp,
 contingency, trigger, linked, notes)
```

**Application in Aseer Museum project:**
- 24 OPEN risks, 2 MITIGATED, 5 WATCH, 0 CLOSED
- 2 CRITICAL (P×I=20), 9 HIGH, 5 MEDIUM, 13 LOW, 2 VERY LOW
- 8 RBS categories covered (min 2 risks per category, max 6)
- RAG = RED (11 High+Critical risks)

## openpyxl Styling Constants

```python
# Colors
NAVY         = "0F172A"
DARK_BLUE    = "1E3A5F"
MID_BLUE     = "2563EB"
LIGHT_BLUE   = "DBEAFE"
WHITE        = "FFFFFF"
LIGHT_GRAY   = "F8FAFC"
MED_GRAY     = "E2E8F0"
DARK_GRAY    = "64748B"

# Fills
NAVY_FILL  = PatternFill(start_color=NAVY, end_color=NAVY, fill_type="solid")
RED_FILL   = PatternFill(start_color="FEE2E2", end_color="FEE2E2", fill_type="solid")
GREEN_FILL = PatternFill(start_color="DCFCE7", end_color="DCFCE7", fill_type="solid")

# Borders
THIN_BORDER = Border(
    left=Side(style="thin", color="CBD5E1"),
    right=Side(style="thin", color="CBD5E1"),
    top=Side(style="thin", color="CBD5E1"),
    bottom=Side(style="thin", color="CBD5E1"),
)

# Fonts
TITLE_FONT    = Font(name="Calibri", bold=True, color=WHITE, size=14)
HEADER_FONT   = Font(name="Calibri", bold=True, color=WHITE, size=9)
BODY_FONT     = Font(name="Calibri", size=9)
BODY_FONT_SM  = Font(name="Calibri", size=8)
DASH_FONT     = Font(name="Calibri", bold=True, color=NAVY, size=11)

# Alignments
ALIGN_CENTER      = Alignment(horizontal="center", vertical="center", wrap_text=True)
ALIGN_LEFT        = Alignment(horizontal="left", vertical="top", wrap_text=True)
ALIGN_LEFT_CENTER = Alignment(horizontal="left", vertical="center", wrap_text=True)
```

## Key openpyxl Patterns

### Pattern 1: Cell Writing with ALL Properties
```python
for col_idx, val in enumerate(data, 1):
    cell = ws.cell(row=row, column=col_idx)
    cell.value = val                           # ← ALWAYS set value first
    cell.font = BODY_FONT
    cell.border = THIN_BORDER
    cell.alignment = ALIGN_CENTER if col_idx <= 2 else ALIGN_LEFT
    # conditional styling per column follows...
```

### Pattern 2: Merged Cells for Titles
```python
ws.merge_cells("A1:X1")  # title row across all 24 columns
ws["A1"].value = "PROJECT TITLE"
ws["A1"].font = TITLE_FONT
ws["A1"].fill = NAVY_FILL
ws["A1"].alignment = ALIGN_CENTER
# Do NOT write to A1:X1 individually — only A1 is writable
```

### Pattern 3: KPI Cards (Merged 2-column blocks)
```python
kpi_data = [
    ("TOTAL RISKS", 31, "31", NAVY, NAVY_FILL, WHITE),
    ("OPEN", 24, "24", "DC2626", RED_FILL, WHITE),
    # ...
]
kpi_cols = [1, 3, 5, 7, 9, 11]
for idx, (label, val, val_str, bg, fill, fg) in enumerate(kpi_data):
    start_c = kpi_cols[idx]
    end_c = start_c + 1  # 2 columns per card
    # Label row
    ws.merge_cells(start_row=4, start_column=start_c, end_row=4, end_column=end_c)
    lbl = ws.cell(row=4, column=start_c, value=label)
    lbl.font = Font(name="Calibri", bold=True, color=DARK_GRAY, size=9)
    lbl.fill = PatternFill(start_color=LIGHT_GRAY, end_color=LIGHT_GRAY, fill_type="solid")
    lbl.alignment = ALIGN_CENTER
    # Value row (merged 2 rows for large number)
    ws.merge_cells(start_row=5, start_column=start_c, end_row=6, end_column=end_c)
    val_cell = ws.cell(row=5, column=start_c, value=val_str)
    val_cell.font = Font(name="Calibri", bold=True, color=WHITE, size=28)
    val_cell.fill = fill
    val_cell.alignment = ALIGN_CENTER
```

### Pattern 4: Severity/Status Conditional Formatting
Use dictionary-based fill mapping for clean code:
```python
SEVERITY_COLORS = {
    "CRITICAL": PatternFill(start_color="FEE2E2", end_color="FEE2E2", fill_type="solid"),
    "HIGH":     PatternFill(start_color="FEF3C7", end_color="FEF3C7", fill_type="solid"),
    "MEDIUM":   PatternFill(start_color="FEF9C3", end_color="FEF9C3", fill_type="solid"),
    "LOW":      PatternFill(start_color="E0F2FE", end_color="E0F2FE", fill_type="solid"),
    "VERY LOW": PatternFill(start_color="F0FDF4", end_color="F0FDF4", fill_type="solid"),
}
# Usage:
cell.fill = SEVERITY_COLORS.get(sev, row_fill)
```

## Print Setup
```python
ws.page_setup.orientation = "landscape"
ws.page_setup.paperSize = ws.PAPERSIZE_A4
ws.page_setup.fitToWidth = 1
ws.page_setup.fitToHeight = 0
ws.print_title_rows = "1:3"  # repeat header rows on each page
ws.sheet_view.showGridLines = False
```

## Dashboard Section Layout (row numbers)
| Row | Content |
|-----|---------|
| 1 | Title (merged A1:L1) |
| 2 | RAG Health banner (merged A2:L2) |
| 4-6 | KPI cards (6 cards × 2 cols each = 12 cols) |
| 8 | Status donut chart (A8) |
| 8 | Severity bar chart (H8) |
| 23 | Top 8 Risks table |
| 23+11 | RBS Category Breakdown |
| +2+8 | Risk Owner Workload |
| +2+5 | Health Check (7 checks) |
| +2+7 | Color Legend |

## Chart Data References
Place data in hidden rows (50+) to avoid cluttering the visible dashboard:
```python
chart_data_start = 50
ws.cell(row=chart_data_start, column=1, value="Status")
ws.cell(row=chart_data_start, column=2, value="Count")
# ... data rows ...
donut = PieChart()
data_ref = Reference(ws, min_col=2, min_row=chart_data_start, max_row=chart_data_start + 4)
labels_ref = Reference(ws, min_col=1, min_row=chart_data_start + 1, max_row=chart_data_start + 4)
donut.add_data(data_ref, titles_from_data=True)
donut.set_categories(labels_ref)
```

## Column Widths (Risk Register)
```python
col_widths_rr = [4, 9, 22, 35, 30, 30, 9, 8, 7, 10, 11, 40, 16, 9, 12, 11, 12, 10, 9, 8, 35, 28, 12, 30]
```
