# Full vs Clean Workbook Pattern

When creating factory cost detail workbooks for sister companies, the user often needs **two variants** of the same file:

## Variants

| Variant | Suffix | Sheets | Purpose |
|---------|--------|--------|---------|
| **Full** | `_Factory_Cost_Details.xlsx` | Labour, Raw Materials, Other/Logistics, **Summary**, **Gap_Analysis** | Internal review, reconciliation, management reporting |
| **Clean** | `_Factory_Cost_Details_Clean.xlsx` | Labour, Raw Materials, Other/Logistics | Client-facing, supplier-facing, or simplified distribution |

## Sheet Structure

### Full version (5 sheets)
1. **Labour** — Cost breakdown by trade (Carpenter, Painter, Welder, etc.) with subtotals and percentages
2. **Raw Materials** — Cost breakdown by PO reference with subtotals
3. **Other - Logistics** — Fleet/transport, reallocated costs, etc.
4. **Summary** — Line-by-line comparison: Real vs Forecast vs Target vs Gap per component
5. **Gap_Analysis** — Target vs Real Data vs Forecast with gap calculation and notes

### Clean version (3 sheets)
Same Labour, Raw Materials, Other - Logistics sheets — no Summary or Gap_Analysis.

## Styling Rules

- Navy `#1F3864` headers with white bold Calibri 11pt
- Yellow `#FFD700` total rows with bold font
- Number format `#,##0.00` on all cost columns
- Alternating row shading (light gray `#F2F2F2`)
- Thin borders on all data cells
- Title row: Calibri 14pt bold navy, merged across columns
- Subtitle row: Calibri 11pt bold navy

## Python Build Pattern

```python
def create_full_workbook():
    wb = Workbook()
    wb.remove(wb.active)
    build_labour_sheet(wb.create_sheet("Labour", 0))
    build_materials_sheet(wb.create_sheet("Raw Materials", 1))
    build_other_sheet(wb.create_sheet("Other - Logistics", 2))
    build_summary_sheet(wb.create_sheet("Summary", 3))
    build_gap_analysis_sheet(wb.create_sheet("Gap_Analysis", 4))
    return wb

def create_clean_workbook():
    wb = Workbook()
    wb.remove(wb.active)
    build_labour_sheet(wb.create_sheet("Labour", 0))
    build_materials_sheet(wb.create_sheet("Raw Materials", 1))
    build_other_sheet(wb.create_sheet("Other - Logistics", 2))
    return wb
```

## Pitfalls

1. **Sheet title `/` character** — Excel sheet titles cannot contain `/`. Use `-` instead (e.g. "Other - Logistics"). The cell text content can still show `/` — only the sheet tab name is restricted.
2. **Both `create_sheet()` and `ws.title` validate** — if you set the title in a builder function AND pass it to `create_sheet()`, both must use the safe name.
3. **Copy to _Final** — always copy both variants to the `_Final` directory after creation.
4. **Data consistency** — the clean version must use the same data and builder functions as the full version, just omitting the summary/gap sheets. Never duplicate data definitions.
