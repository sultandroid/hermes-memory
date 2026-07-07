# SCOPE_REQUEST.docx Generation — Example Script

Full working example for converting a SCOPE_REQUEST.md (in _MANAGER_DASHBOARD/) to a branded .docx (at sub root).

## Table width helper

Always fix table widths via XML after `add_table()` — never rely on `col_widths_cm` parameter (python-docx stores EMU as dxa, producing broken widths).

```python
"""Generate [Discipline] SOW docx using SamayaDoc template."""
import sys, os, re

sys.path.insert(0, "/Users/mohamedessa/Library/CloudStorage/OneDrive-SAMAYAINVESTMENT/Samaya/Technical Office/_Style-Guides/Doc Style Guide")
from samaya_doc_template import SamayaDoc
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

def cm_to_twips(cm):
    """Convert cm to twips (1 cm = 567 twips)."""
    return int(cm / 2.54 * 1440)

def set_table_widths(table, col_widths_cm):
    """Fix table column widths via direct XML manipulation (avoids python-docx EMU/dxa bug)."""
    total_cm = sum(col_widths_cm)
    tbl = table._tbl
    tblPr = tbl.find(qn('w:tblPr'))
    if tblPr is not None:
        tblW = tblPr.find(qn('w:tblW'))
        if tblW is not None:
            tblW.set(qn('w:w'), str(cm_to_twips(total_cm)))
            tblW.set(qn('w:type'), 'dxa')
    tblGrid = tbl.find(qn('w:tblGrid'))
    if tblGrid is not None:
        for child in list(tblGrid):
            tblGrid.remove(child)
        for w in col_widths_cm:
            gc = OxmlElement('w:gridCol')
            gc.set(qn('w:w'), str(cm_to_twips(w)))
            tblGrid.append(gc)
    for row in table.rows:
        for i, w in enumerate(col_widths_cm):
            if i < len(row.cells):
                cell = row.cells[i]
                tcPr = cell._tc.find(qn('w:tcPr'))
                if tcPr is not None:
                    tcW = tcPr.find(qn('w:tcW'))
                    if tcW is not None:
                        tcW.set(qn('w:w'), str(cm_to_twips(w)))
                        tcW.set(qn('w:type'), 'dxa')

def get_col_widths(headers, total=16.0):
    """Auto-calculate column widths based on header text keywords."""
    n = len(headers)
    widths = [total / n] * n
    keywords = {
        '#': 1.0, 'id': 1.0, 'no.': 1.0, 'item id': 1.0,
        'status': 2.5, 'qty': 2.5, 'count': 2.5, 'lead time': 3.0, 'tier': 2.5,
        'discipline': 3.0, 'category': 3.0, 'stage': 3.0, 'source sub': 3.0, 'source': 3.0,
        'scope': 6.0, 'scope of testing': 7.0, 'description': 6.0, 'detail': 9.0,
        'notes': 5.0, 'comments': 6.0, 'deliverable': 5.0, 'requirement': 5.0, 'parameter': 5.0,
        'specification': 8.0, 'contents': 9.0, 'location': 5.0, 'milestone': 6.0,
        'target date': 8.0, 'sign-off': 5.0, 'owner': 4.0, 'trigger': 5.0,
        'indicative qty': 2.5, 'lead': 3.0,
    }
    for i, h in enumerate(headers):
        hl = h.lower().strip().rstrip('.')
        if hl in keywords:
            widths[i] = keywords[hl]
    s = sum(widths)
    return [w * total / s for w in widths]
```

## Full generation script

```python
BASEDIR = sys.argv[1]   # e.g., "/path/to/Subcontractors/NN_Discipline"

doc = SamayaDoc()
doc.create_header(
    project_name="Aseer Regional Museum — [Discipline]",
    doc_ref="MOC-ASEER-SIC-1K0-SC-NNN",
    doc_type="SCOPE_REQUEST",
    revision="A",
    date="Jun 2026"
)
doc.create_footer("MOC-ASEER-SIC-1K0-SC-NNN")

# Read source .md from _MANAGER_DASHBOARD/
with open(os.path.join(BASEDIR, "_MANAGER_DASHBOARD", "SCOPE_REQUEST.md")) as f:
    md = f.read()

lines = md.split("\n")
in_table = False
table_rows = []
tables = []  # (table_object, col_widths) for post-processing

def flush_table():
    global in_table, table_rows, tables
    if not table_rows:
        return
    headers = table_rows[0]
    data = table_rows[1:]
    widths = get_col_widths(headers)
    t = doc.add_table(headers, data)  # NO col_widths_cm here!
    tables.append((t, widths))
    in_table = False
    table_rows = []

for line in lines:
    if line.startswith("# ") and not line.startswith("## "):
        flush_table(); doc.add_h1(line[2:]); continue
    if line.startswith("## ") and not line.startswith("### "):
        flush_table(); doc.add_h2_u(line[3:]); continue
    if line.startswith("### "):
        flush_table(); doc.add_h3("", line[4:]); continue
    if line.startswith("|") and line.endswith("|"):
        cells = [c.strip() for c in line.split("|")[1:-1]]
        if all(re.match(r"^[-:\s]+$", c) for c in cells if c):
            continue
        if not in_table: table_rows = [cells]; in_table = True
        else: table_rows.append(cells)
        continue
    flush_table()
    if line.startswith("---"):
        doc.line(); continue
    if line.startswith("> "):
        doc.add_body(line[2:], italic=True, size=10); continue
    if "**" in line:
        segs = []
        for p in re.split(r"(\*\*.*?\*\*)", line):
            if p.startswith("**") and p.endswith("**"): segs.append({"text": p[2:-2], "bold": True})
            elif p.strip(): segs.append({"text": p})
        if segs: doc.add_rich_body(segs); continue
    if line.strip(): doc.add_body(line)

flush_table()

# CRITICAL: Fix table widths after creation
for t, widths in tables:
    set_table_widths(t, widths)

# Save at sub root (NOT inside _MANAGER_DASHBOARD/)
out = os.path.join(BASEDIR, "SCOPE_REQUEST.docx")
doc.save(out)
print(f"✅ {out}")
```

## Key reminders

- Script reads from `_MANAGER_DASHBOARD/SCOPE_REQUEST.md` — NOT sub root
- Saves to `SCOPE_REQUEST.docx` at sub root — NOT inside `_MANAGER_DASHBOARD/`
- Doc ref pattern: `MOC-ASEER-SIC-1K0-SC-NNN` where NNN increments per sub
- **CRITICAL:** Call `set_table_widths(t, widths)` AFTER `add_table()` — never use `col_widths_cm` parameter (broken EMU/dxa conversion)
- Always clean up temp script: `rm /tmp/gen_*_docx.py`
