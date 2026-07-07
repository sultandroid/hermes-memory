# HTML Table → Excel Export

After fixing HTML page overflow, a common downstream task is exporting the data to Excel for tracking. This pattern was used on the Aseer Museum RIBA Deliverable Tree (279 rows, 15 categories, 3 stages).

## HTML table structure

```
<table class="tree-table">
  <thead><tr><th>Ref</th><th>Deliverable Tree</th><th>Description</th><th>RAG</th></tr></thead>
  <tbody>
    <tr class="stage-header"><td colspan="4">STAGE 4 ...</td></tr>
    <tr class="cat-header"><td colspan="4"><span class="cat-label">A. Manufacturing Info</span>...</td></tr>
    <tr><td class="ref">A01</td><td class="tree">├── A01 ...</td><td class="desc">description</td><td class="stat"><span class="rag g">OK</span></td></tr>
  </tbody>
</table>
```

## Parsing

1. Find all `<table class="tree-table">` elements
2. Extract all `<tr>` rows
3. Classify by `class` attribute: `stage-header`, `cat-header`, or data row
4. For data rows, extract 4 cells: ref, tree text, description, RAG status

## Utility functions

```python
def extract_text(el_html):
    text = re.sub(r'<br\s*/?>', ' ', el_html)
    text = re.sub(r'<[^>]+>', '', text)
    text = text.replace('&amp;', '&').replace('&ensp;', ' ').replace('&bull;', '•')
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def parse_rag(rag_html):
    rag = extract_text(rag_html).strip().upper()
    return rag if rag in ('OK','PARTIAL','PENDING','MISSING','FUTURE') else ''
```

## RAG color mapping (openpyxl)

```python
rag_fills = {
    'OK':      PatternFill(start_color='F0FDF4', end_color='F0FDF4', fill_type='solid'),
    'PARTIAL': PatternFill(start_color='FEF3C7', end_color='FEF3C7', fill_type='solid'),
    'PENDING': PatternFill(start_color='EFF6FF', end_color='EFF6FF', fill_type='solid'),
    'MISSING': PatternFill(start_color='FEF2F2', end_color='FEF2F2', fill_type='solid'),
    'FUTURE':  PatternFill(start_color='F8FAFC', end_color='F8FAFC', fill_type='solid'),
}
rag_fonts = {
    'OK':      Font(bold=True, color='15803D', size=9),
    'PARTIAL': Font(bold=True, color='92400E', size=9),
    'PENDING': Font(bold=True, color='1D4ED8', size=9),
    'MISSING': Font(bold=True, color='B91C1C', size=9),
    'FUTURE':  Font(bold=True, color='475569', size=9),
}
```

## Excel layout

**Sheet 1 — "Deliverable Tree":**
- Header row (black fill, white text)
- Stage headers (dark navy #1E293B, white text, merged A-D)
- Cat headers (light gray #F1F5F9, bold, merged A-D)
- Data rows with RAG-colored status column
- Alternating row shading (#FAFAFA on evens)
- Column widths: Ref=10, Tree=60, Description=55, RAG=16
- Freeze pane at A2, auto-filter on all columns

**Sheet 2 — "Summary Dashboard":**
- RAG status counts table (OK/Partial/Pending/Missing/Future with %)
- Category-by-category breakdown with per-category RAG counts
- Grand total reconciliation

## Determining categories for summary

Parse cat-header text with `([A-Z])\.` to get the category letter. Track `current_cat` as you iterate data rows:

```python
current_cat = ''
cat_data = {}
for entry in rows_data:
    if entry['type'] == 'cat':
        m = re.match(r'([A-Z])\.', entry['text'])
        if m: current_cat = m.group(1)
    elif entry['type'] == 'data' and entry['rag']:
        cat_data.setdefault(current_cat, {'OK':0,'PARTIAL':0,'PENDING':0,'MISSING':0,'FUTURE':0,'total':0})
        cat_data[current_cat][entry['rag']] += 1
        cat_data[current_cat]['total'] += 1
```

## Pitfalls

- Rogue `/private/tmp/struct.py` breaks numpy/openpyxl imports — delete it if found
- Stage headers span 4 cols, need `merge_cells` in Excel
- HTML entities (`&amp;`, `&ensp;`, `&bull;`) must be decoded before writing to cells
