# Aseer Interactives — Evidence & Museum-Wide SOW Editing

Supplementary to `aseer-interactives-scope-classification.md`. Covers the RFI evidence chain
and the concrete technique for turning the G9-only SOW into a comprehensive 6-interactive
scope document for CG submission.

## Evidence chain for the scope basis

| Doc | Covers | Role in scope |
|-----|--------|---------------|
| **`A2742-6.04-018`** NRS RFI (01-Jun-2026) | G9 Flowersmen Sensory Interactive ONLY | Origin evidence that interactive design is OUT of NRS scope → basis for moving it to Rawasin. Carries the **12 open technical questions** (image breakdown, idle state, multi-user, trigger delay, colour temp, scent dispenser-vs-sniff). Section 6.0 of INT-001 mirrors these. |
| `6930_Aseer_Tactile & Manual Interactives Schedule` V2 | All 6 interactives | The authoritative scope basis for the museum-wide list. |
| `6930_Aseer_Exhibit Schedule` V3 | Per-exhibit component columns | Proves interactives are NOT screens: an exhibit with no `Media ID` has no screen; its `Tactile/Manual ID` is physical/hybrid. |

**Key point:** the NRS RFI supports ONLY G9. When presenting a *museum-wide* scope to CG,
the Tactile/Exhibit schedules are the primary reference and the RFI is a supporting G9 detail
— not the basis for the whole.

## SOW must be COMPREHENSIVE (user directive)

User confirmed (2026-08-23): *"لا احنا عايزين يكون شامل كله طبعا"* — the interactive SOW
presented to CG must cover **all 6 interactives**, not Exhibit ET_09.03 alone. Do NOT leave it
as the G9-only draft. Also confirmed: the interactive people do NOT fabricate models, glass,
joinery, or metalwork — *"الناس بتاعت الانتراكتيف مش هاتعمل موديلات ولا تصنيع زجاج ولا اعمال
خشبيه او اخري فقط الانتراكتيف"* — the rest is by others. Encode this as an explicit
SCOPE BOUNDARY in the doc.

## Technique — python-docx: single-exhibit SOW → museum-wide SOW

Converting `INT-001` from G9-only to a 6-interactive document (no LibreOffice/Word needed):

```python
from docx import Document
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

d = Document(SRC)

def set_para_text(p, text):          # replace a paragraph's runs with one bold-ish run
    for r in list(p.runs): r._r.getparent().remove(r._r)
    p.add_run(text)

def set_cell(cell, text):            # clear + rewrite a table cell
    for p in cell.paragraphs:
        for r in list(p.runs): r._r.getparent().remove(r._r)
    cell.paragraphs[0].add_run(text)

def insert_para_after(p, text, bold=True):
    """Insert a paragraph AFTER existing <p> using raw lxml; set xml:space preserve."""
    np = OxmlElement('w:p'); pPr = OxmlElement('w:pPr'); rPr = OxmlElement('w:rPr')
    if bold: rPr.append(OxmlElement('w:b'))
    pPr.append(rPr); np.append(pPr)
    run = OxmlElement('w:r'); t = OxmlElement('w:t')
    t.text = text; t.set(qn('xml:space'), 'preserve')   # keep leading spaces/lists
    run.append(t); np.append(run)
    p._p.addnext(np)   # NOT p.insert — addnext puts it right after the anchor
```

Key moves for the museum-wide rewrite:
1. **Title + Purpose (para 1, para 6)** — `set_para_text` to "Museum-Wide Manual, Tactile &
   Sensory Interactives" and "defines the scope for the six (6) interactive exhibits".
2. **1.2 Exhibit Identification** — delete the old 4 bullets (`for idx in [13,12,11,10]:
   d.paragraphs[idx]._p.getparent().remove(...)`) then `insert_para_after` the 6-item list
   (insert in REVERSED order so they land in order, since addnext stacks).
3. **Replace the G9-exhibit context table** — rewrite header via `set_cell`, then `add_row()`
   until `len(table.rows) == 1+len(data)` and fill each row.
4. **Append scope rows to Table 3** (manual/tactile hardware, replica coordination,
   accessibility) via `table.add_row()` + `set_cell`.
5. **Rewrite SCOPE BOUNDARY paragraph** (find by content startswith `'SCOPE BOUNDARY'`) to
   list all 6 IDs + state integration-only (no fabrication of replicas/glass/joinery).
6. **Doc-control table**: bump Revision + Issue Date + Document Type to the new umbrella title.
7. Save to a NEW `.docx` (the user opens/approves; don't overwrite the source).

Pitfalls hit while doing this:
- `t.text = text` on an `OxmlElement('w:t')` needs `t.set(qn('xml:space'),'preserve')` for
  leading-space/bullet strings, else Word strips indentation.
- `addnext` inserts immediately AFTER the anchor; to place several items in order, iterate the
  list in `reversed()` or keep inserting relative to the last-inserted element.
- Don't redefine helper functions after first use in the same script (NameError).
- Verify with a re-open loop printing `[p.text for p in d.paragraphs]` and the modified table
  rows before declaring success.
