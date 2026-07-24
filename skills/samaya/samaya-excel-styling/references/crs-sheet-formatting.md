# CRS (Comment Resolution Sheet) Excel Formatting

A CRS is a standard document submitted alongside revised plans to show how each CG comment was addressed. It has a fixed structure.

## Standard CRS Layout

| Section | Rows | Content |
|---------|------|---------|
| Title | 1 | "COMMENTS RESOLUTION SHEET (CRS)" — navy bar |
| Project Info | 2-6 | Project name, CRS number, Document No., Document Title, Revision |
| Legend | 7 | Review status codes (A/B/C/D) |
| Column Headers | 8 | No., Initial, Section/Ref., Code, Reviewer Comment, Originator Reply, Reply By, Status |
| Comment Rows | 9-13+ | One row per CG comment |
| Legend | 14 | Review status codes repeated |
| Sign-off | 15-19 | Supervision Consultant, PMCM, MOC, Originator — with Name/Position/Signature/Date rows |

## Samaya Branding for CRS

```python
NAVY = "1F3864"       # Title bar + column headers
GOLD = "C9A84C"       # Sign-off section headers
RED = "FF4444"        # Code C cells
GREEN = "166534"      # Closed status cells
LIGHT_GREY = "F2F4F7" # Alternating row stripes + info labels
```

## Key Styling Rules

1. **Code C column** — red fill + white bold font, center-aligned
2. **Status column** — green fill + white bold font for "Closed", center-aligned
3. **Comment rows** — 80px row height for readability, alternating stripes
4. **Project info labels** — right-aligned, bold navy on light grey
5. **Project info values** — left-aligned, merged across C-H columns
6. **Freeze panes** at row 9 (below column headers)
7. **Landscape orientation**, fit to width

## Pitfall: MergedCell Read-Only Error

When rebuilding a sheet that has merged cells, you MUST unmerge ALL merged cells BEFORE clearing values:

```python
# Step 1: Unmerge all
for mr in list(ws.merged_cells.ranges):
    ws.unmerge_cells(str(mr))

# Step 2: Clear all content
for row in ws.iter_rows(min_row=1, max_row=ws.max_row, max_col=8):
    for cell in row:
        cell.value = None
        cell.font = Font(name="Calibri", size=9)
        cell.fill = PatternFill(fill_type=None)
        cell.border = Border()
        cell.alignment = Alignment()

# Step 3: Now merge and set values
ws.merge_cells('A1:H1')
ws['A1'].value = 'COMMENTS RESOLUTION SHEET (CRS)'
```

If you skip step 1, `MergedCell` attribute errors occur when writing to cells that were part of old merged ranges.

## Data Source

The CRS data comes from the CG response PDF or the `send_crs.xlsx` file. The 5 standard columns are:
- No. (sequential)
- Initial (reviewer initials, e.g. "Noman")
- Section / Ref. (e.g. "Section 9.1")
- Code (always "C" for Code C comments)
- Reviewer Comment (full text)
- Originator Reply (full text)
- Reply By (e.g. "Technical Office")
- Status (e.g. "Closed")
