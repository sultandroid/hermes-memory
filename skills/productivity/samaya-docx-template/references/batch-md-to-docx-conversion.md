# Batch MD-to-DOCX Conversion Pattern

When converting multiple Markdown deliverables to Samaya-branded DOCX in one pass.

## Key Pattern

```python
import sys, os, re
sys.path.insert(0, STYLE_GUIDE_PATH)
from samaya_doc_template import SamayaDoc
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

def md_to_docx(md_path, docx_path, doc_ref, doc_type, title, project="Project Name"):
    with open(md_path) as f:
        md = f.read()
    
    doc = SamayaDoc()
    doc.create_header(project_name=project, doc_ref=doc_ref, doc_type=doc_type,
                      revision="00", date="June 2026")
    doc.create_footer(doc_ref)
    
    # Parse markdown: h1, h2, h3, tables, body text
    lines = md.split("\n")
    in_table = False
    table_rows = []
    tables = []
    
    def flush_table():
        nonlocal in_table, table_rows, tables
        if not table_rows:
            return
        headers = table_rows[0]
        data = table_rows[1:]
        widths = get_col_widths(headers)
        t = doc.add_table(headers, data)  # NO col_widths_cm
        tables.append((t, widths))
        in_table = False
        table_rows = []
    
    for line in lines:
        # handle ##, ###, |table|, body text
        # ... see references/docx-generation-example.md for full parse logic
    
    flush_table()
    
    # Fix table widths AFTER creation
    for t, widths in tables:
        set_table_widths(t, widths)
    
    doc.save(docx_path)

# Run for each document
for doc in documents:
    md_to_docx(**doc)
```

## Column Width Auto-Detection

```python
def get_col_widths(headers, total=16.0):
    n = len(headers)
    widths = [total / n] * n
    kw = {
        '#': 1.2, 'id': 1.0, 'ref': 1.5, 'code': 1.2,
        'status': 2.5, 'qty': 2.0, 'priority': 2.5,
        'description': 6.0, 'scope': 6.0, 'deliverable': 5.0,
        'reference': 5.0, 'notes': 5.0, 'comments': 6.0,
    }
    for i, h in enumerate(headers):
        hl = h.lower().strip().rstrip('.')
        if hl in kw:
            widths[i] = kw[hl]
    s = sum(widths)
    return [w * total / s for w in widths]
```

## Pitfalls

- **NEVER pass `col_widths_cm` to `add_table()`** — python-docx stores EMU as dxa, producing giant columns (16cm becomes 4000 inches)
- Always call `set_table_widths()` after `add_table()` via XML manipulation
- The `SamayaDoc` header `create_header()` and footer `create_footer()` must be called in order
- Save path: sub root (not inside `_MANAGER_DASHBOARD/`)
- Multiple DOCX files can be generated in one script, each with their own doc ref
