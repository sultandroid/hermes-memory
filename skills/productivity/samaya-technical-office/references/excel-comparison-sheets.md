# Excel Comparison Sheets — Template Pattern

Used for vendor/product comparison (3D scanners, LiDAR scanners, etc.).

## Rules

- **Formulas, not text**: TOTAL = SUM of line items. VAT = TOTAL * 0.15. GRAND TOTAL = TOTAL + VAT.
- **Number formatting**: `#,##0" SAR"` for currency, never concatenate "SAR" as a string.
- **Empty cells**: truly blank (`None`), never "N/A", "--", or "—" as string placeholders for numeric cells.
- **Symmetrical tabs**: if one vendor/product gets a software-options tab, every vendor/product does (or note why not).
- **Headers**: Dark navy `#1F3864` background, white bold text, 28px height.
- **Total rows**: Yellow `#FFF2CC` fill, medium navy border top+bottom.
- **Alternating rows**: `#E9EFF7` light blue for readability.
- **Freeze panes**: `B5` so headers + spec column stay visible.

## openpyxl Reference

```python
from openpyxl.styles import Font, Alignment, PatternFill, Border, Side

DARK_NAVY = "1F3864"
CUR_FMT = '#,##0" SAR"'

hdr_font = Font(bold=True, size=11, color="FFFFFF", name="Calibri")
hdr_fill = PatternFill(start_color="1F4E79", end_color="1F4E79", fill_type="solid")
total_fill = PatternFill(start_color="FFF2CC", end_color="FFF2CC", fill_type="solid")

# Currency cell
cell.value = 195000
cell.number_format = CUR_FMT

# Formula cell
cell.value = "=B18+B19+B20+B21"
cell.number_format = CUR_FMT
```

## Pitfalls

- OneDrive stubs (4-byte files with content "null") cannot be read — copy to `/tmp/` or use local copies.
- Always verify all prices against source PDFs after extracting — scanned PDFs may have OCR errors.
- When a vendor has multiple products, create separate product folders (e.g., `Faro_Focus_Premium_200m/`, `Faro_Blink/`).
