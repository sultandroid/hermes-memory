# Cost Comparison Excel — In-House vs External Supplier

Use this pattern when the user needs to evaluate an external supplier offer against in-house capability (factory, labor, materials).

## When to use

- External quotation received for manufacturing/design/construction
- User asks for comparison study to support a procurement decision
- Multiple options need to be evaluated (design-only, full mfg, split scope)

## Excel Structure

4 sheets in a single workbook:

### 1. Executive Summary

Side-by-side comparison table for each option:

| Column | Content |
|--------|---------|
| Metric | Cost, Duration, Scope, QC, Shipping, Coordination |
| Supplier Cost (SAR) | From the external quotation |
| Supplier Duration | Timeline from quotation |
| In-House Cost | Estimated: materials + labor + extra equipment |
| In-House Duration | Estimated: design + production + finishing |
| Advantage | "In-house", "Supplier", or "TBD" (color-coded green/yellow) |
| Notes | Clarifications, assumptions, caveats |

Show multiple options as separate sections:
- **Option 1 — Design + Manufacturing (Full Service)**
- **Option 2 — Manufacturing Only** (using external design)

End each section with a **Bottom Line** row.

### 2. Timeline

Visual Gantt (row per actor, column per week) showing:
- Supplier design phase
- In-house designer wait time
- In-house design phase
- Manufacturing prep
- Manufacturing phase
- Finishing + QC

Add a **Key Dates** section below the Gantt.

### 3. Cost Breakdown

Detailed line-item table for in-house costs:

| Item | Description | Est. Cost (SAR) | Notes |
|------|-------------|-----------------|-------|
| Extra equipment | 3D printers, tooling | 10,000 | One-time investment |
| Materials | Filament, MDF, paint, adhesives | 2,000 | Per project |
| Outsourced labor | Temp workers for assembly/finishing | 3,000 | ~15 days x 200/day |
| In-house overtime | Extra hours for production team | 1,500 | ~50 hrs x 30/hr |
| Design cost | Salaried (no added cost) | 0 | Already employed |
| **TOTAL** | | **~17,500** | |

Also show supplier's quoted costs in a separate section for comparison.

### 4. Recommendation

Decision matrix comparing all options:

| Opt | Option Name | Total Cost | Timeline | Risk | Assessment |
|-----|-------------|-----------|----------|------|------------|
| A | Full In-House | ~17,500 | ~35 days | Medium | Lowest cost, schedule risk (designer availability) |
| B | External Design + In-House Mfg | ~33,000+ | ~60 days | Med-High | Split scope adds overhead |
| C | Full External | 21,000+ + shipping | ? | High | Least control, shipping from abroad |

## Formatting Rules (User Preference)

- **No emoji, icons, or decorative symbols** in any cell
- Use PatternFill colors (green=C6EFCE, yellow=FFEB9C, red=FFC7CE) on status cells instead of icons
- Clean Calibri font, gray-blue header fill (2F5496), white text, thin borders
- "Advantage" column: green fill for the recommended side, yellow for TBD/uncertain
- Bottom Line rows: light gray background, bold text

## Python Implementation Pattern

```python
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side

wb = openpyxl.Workbook()
ws = wb.active
ws.title = 'Executive Summary'

# Define reusable style objects
hdr_font = Font(name='Calibri', bold=True, size=11, color='FFFFFF')
hdr_fill = PatternFill(start_color='2F5496', end_color='2F5496', fill_type='solid')
green_fill = PatternFill(start_color='C6EFCE', end_color='C6EFCE', fill_type='solid')
green_font = Font(bold=True, size=10, color='006100')
thin_border = Border(left=Side(style='thin'), right=Side(style='thin'),
                     top=Side(style='thin'), bottom=Side(style='thin'))

# Helper function
def set_cell(ws, row, col, value, font=None, fill=None, alignment=None):
    cell = ws.cell(row=row, column=col, value=value)
    if font: cell.font = font
    if fill: cell.fill = fill
    if alignment: cell.alignment = alignment
    cell.border = thin_border
    return cell
```

Source files from this session:
`/tmp/cost_comparison_v2.py` (full implementation)
`/Users/mohamedessa/Desktop/Old_Madinah_Model_Cost_Comparison.xlsx` (sample output)
