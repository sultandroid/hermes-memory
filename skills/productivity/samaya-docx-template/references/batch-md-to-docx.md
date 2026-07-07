# Batch MD → DOCX Conversion Pattern

When multiple tender-phase markdown deliverables need Samaya-branded DOCX conversion, use this pattern.

## Script Skeleton

```python
import sys, os, re
sys.path.insert(0, "/Users/mohamedessa/Library/CloudStorage/OneDrive-SAMAYAINVESTMENT/Samaya/Technical Office/_Style-Guides/Doc Style Guide")
from samaya_doc_template import SamayaDoc
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

def set_table_widths(table, col_widths_cm):
    """Fix table column widths via XML (avoids python-docx EMU/dxa bug)."""
    # ... (see docx-generation-example.md for full function)

def get_col_widths(headers, total=16.0):
    """Auto-calc widths based on header keywords."""
    kw = {'#': 1.2, 'ref': 1.5, 'description': 6.0, 'scope': 6.0,
          'status': 2.5, 'priority': 2.5, 'qty': 2.0, 'unit': 2.0, ...}
    n = len(headers)
    widths = [total/n] * n
    for i, h in enumerate(headers):
        hl = h.lower().strip().rstrip('.')
        if hl in kw: widths[i] = kw[hl]
    s = sum(widths)
    return [w * total / s for w in widths]

def md_to_docx(md_path, docx_path, doc_ref, doc_type, title,
               project="RCRC Exhibition — Riyadh: From Memory to Vision"):
    """Convert a Markdown file to Samaya-branded DOCX."""
    with open(md_path) as f:
        md = f.read()
    
    doc = SamayaDoc()
    doc.create_header(project_name=project, doc_ref=doc_ref,
                      doc_type=doc_type, revision="00", date="June 2026")
    doc.create_footer(doc_ref)
    
    # Parse markdown sections: h1→add_h1, h2→add_h2, h3→add_h3
    # Parse tables: collect |...| rows, skip separator lines
    # Fix table widths after creation via set_table_widths()
    
    doc.save(docx_path)
```

## Key Points

- Tables are collected as rows of cell strings, then passed to `doc.add_table(headers, data)` WITHOUT `col_widths_cm`.
- After ALL tables are created, iterate and call `set_table_widths(t, widths)`.
- Section numbering auto-extracted from heading text (e.g. "1. Purpose" → h2("1", "Purpose")).
- Doc ref pattern for tender deliverables: `CODE-RCRC-001` (MOS, SOW, ER, PS, BOQ, AVT, LIT, MFS).
- Always update Odoo tasks after generating DOCX files (append file info to task description + log timesheet).
