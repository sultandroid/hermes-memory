# CRS-to-DOCX Update Patterns (Samaya RMP)

## Overview

When CG returns Code C with a CRS (Comments Resolution Sheet) for a plan document, the workflow is:

1. Read the CRS Excel via openpyxl — extract all comment-response pairs
2. Map each comment to the correct DOCX section using the "Section / Ref." column
3. Update the DOCX one change at a time
4. Add REVxx row to the revision history table
5. Save to a RevXX subfolder alongside the styled CRS Excel

## Body Heading Search — Critical

The DOCX has BOTH a Table of Contents (toc-style paragraphs) AND body headings (Heading 1/2/3 style). Searching by text alone finds the TOC entry first. **Always filter by style:**

```python
def body_heading_idx(doc, text_start):
    for i, p in enumerate(doc.paragraphs):
        t = p.text.strip()
        s = p.style.name
        if t.startswith(text_start) and s.startswith('Heading'):
            return i
    return None
```

Never use a plain `para_idx()` text match on a document with a TOC — content lands in the wrong block.

## Insertion: `insert_paragraph_after()` Does Not Exist

Only `insert_paragraph_before()` exists on `Paragraph`. To insert after index N:

```python
# Correct — insert before the NEXT paragraph
new_p = doc.paragraphs[N+1].insert_paragraph_before('')
```

## Style Inheritance on Insert

`insert_paragraph_before()` copies the style from the target. If the target is inside the TOC block, the new paragraph inherits `toc 1` style. Fix:

```python
new_p = doc.paragraphs[idx].insert_paragraph_before('')
new_p.style = doc.styles['Normal']
for run in new_p.runs:
    run.font.size = Pt(10)
```

Better: find the body heading directly so the target is a Normal/Heading paragraph, not a toc paragraph.

## Table Row Append

Use `table.add_row()` to append rows to existing tables:

```python
for table in doc.tables:
    first = table.rows[0].cells[0].text.strip()
    if first == 'Risk Factor':
        row = table.add_row()
        row.cells[0].text = 'New Risk Factor Name'
        row.cells[1].text = 'Description text'
        row.cells[2].text = 'Critical'
        break
```

## Common Pitfalls

| Error | Cause | Fix |
|-------|-------|-----|
| New content inside TOC | `para_idx()` matches TOC entry, not body heading | Use `body_heading_idx()` with style filter |
| `AttributeError: 'Paragraph' object has no attribute 'insert_paragraph_after'` | Method doesn't exist | Use `insert_paragraph_before()` on next index |
| TOC-style text in wrong section | Style inheritance from target paragraph | Set `p.style = doc.styles['Normal']` after insert |
| Inserted row not appearing | `table.add_row()` not called, or cell count mismatch | Verify column count matches |

## CRS Excel Samaya Styling

After extracting data, restyle the CRS sheet:

| Element | Style |
|---------|-------|
| Title row | Navy fill, white 16pt, merged A1:H1 |
| Info rows | Light grey label cells, blue labels |
| Column headers | Navy fill, white 10pt bold |
| Code C cells | Red fill (#FF4444), white bold |
| Status Closed cells | Green fill (#166534), white bold |
| Sign-off headers | Gold fill (#C9A84C), dark text |
| Alternating data rows | Light grey (#F2F4F7) stripes |
| Data cells | Thin grey borders, wrap text |
| Freeze panes | After header row (row 9) |
