# Samaya DOCX Template Usage

**All .docx outputs MUST use SamayaDoc** from `templates/samaya_doc_template.py`.

## Quick Reference

```python
from samaya_doc_template import SamayaDoc, SamayaColors

doc = SamayaDoc()
doc.create_header('Aseer Museum', 'ASR-SAM-XXX-001', 'RPT', 'A', 'Jun 2026')
doc.create_footer('ASR-SAM-XXX-001')
doc.add_h1('DOCUMENT TITLE')
doc.add_h2('1.0', 'SECTION HEADING')
doc.add_h3('1.1', 'SUBSECTION')
doc.add_body('Body text here.')
doc.add_rich_body([
    {'text': 'Bold label: ', 'bold': True},
    {'text': 'normal text'},
])
doc.add_table(
    ['Header1', 'Header2'],
    [['row1col1', 'row1col2']],
    col_widths_cm=[2.0, 5.0]
)
doc.line()
doc.save('output.docx')
```

## Template Location

Canonical: `_Style-Guides/Doc Style Guide/samaya_doc_template.py` (OneDrive)
Copy: `templates/samaya_doc_template.py` (Hermes skill)

## What It Enforces
- A4 portrait, Samaya margins (T2.5/B2.0/L2.5/R2.0)
- Calibri throughout (18pt H1, 14pt H2, 12pt H3, 11pt body, 9.5pt table)
- Navy #1E293B headings with bottom borders
- Accent red #B01E2F for emphasis
- Header: Samaya logo + doc info strip
- Footer: doc ref + Page X of Y + "Samaya Investment Company"
- Tables: navy header row, alternating gray/white rows, border gray #CBD5E1

## Document Control (DC) Block

The user requires a **Document Control block** immediately after the title in all formal documents. This establishes Prepared By / Reviewed By / Approved By chain.

```python
doc.add_h2_u('DOCUMENT CONTROL')
doc.add_table(
    headers=['Field', 'Detail'],
    rows=[
        ['Document Ref', 'MOC-MUS-ASE-1KH-SOW-INT-001'],
        ['Revision', '00'],
        ['Issue Date', '07 June 2026'],
        ['Prepared By', 'Samaya Investment — Technical Office / BIM Unit'],
        ['Reviewed By', 'Sultan Issa — Technical Office Manager'],
        ['Approved By', 'Adel Darwish — Projects Director'],
        ['Document Type', 'Scope of Work & Prequalification Requirements'],
        ['Project', 'Aseer Regional Museum (Project 3092 — Contract 0010003521)'],
        ['Discipline', 'Specialist Interactive Design / Gallery Interactives'],
        ['T2 Allocation', 'T2-09 (Interactives → Rawasin umbrella)'],
        ['Distribution', 'CG · PMC · MoC · Rawasin · Samaya TO'],
        ['Classification', 'Confidential — Samaya Investment'],
    ],
    col_widths_cm=[5.0, 11.5],
)
doc.line()
```

The key method `add_h2_u(text)` adds an un-numbered h2 heading — use it for structural blocks like Document Control.

## `create_header` / `create_footer` — Actual Signatures

```python
create_header(self, project_name, doc_ref, doc_type, revision, date=None)
create_footer(self, doc_number, confidential=True)
```

These are **positional**, not keyword, so call them as:
```python
doc.create_header('Project Name', 'DOC-REF-001', 'DOCUMENT TYPE', '00', '07 June 2026')
doc.create_footer('DOC-REF-001', confidential=True)
```

## Missing Methods — Manual Workarounds

`SamayaDoc` does **not** have `add_bullet()` or `add_note()` methods. Use manual paragraphs:

```python
def bullet(doc, text, level=0):
    p = doc.doc.add_paragraph()
    pf = p.paragraph_format
    pf.space_before = Pt(0)
    pf.space_after = Pt(2)
    pf.line_spacing = Pt(13)
    pf.line_spacing_rule = WD_LINE_SPACING.EXACTLY
    pf.left_indent = Cm(1.0 + level * 0.8)
    pf.first_line_indent = Cm(-0.5)
    run = p.add_run(f'• {text}')
    run.font.name = 'Calibri'
    run.font.size = Pt(11)
```

For a note/callout:

```python
p = doc.doc.add_paragraph()
run = p.add_run('NOTE LABEL:')
run.font.bold = True
run.font.size = Pt(10)
run.font.color.rgb = SamayaColors.MEDIUM_GRAY
p2 = doc.doc.add_paragraph()
run2 = p2.add_run('Note text here.')
run2.font.size = Pt(10)
run2.font.color.rgb = SamayaColors.DARK_GRAY
```

## `add_rich_body` Useful for Bold+Normal on Same Line

```python
doc.add_rich_body([
    {'text': 'Critical: ', 'bold': True, 'color': SamayaColors.ACCENT_RED},
    {'text': 'normal continuation text'},
])
```

## Pitfalls

- **Sourcing accuracy is critical.** Every claim in a formal document must trace back to a verifiable project document reference (contract clause, SoW section, DMP section, RFI, approved submittal, schedule). Never state "X is not required" or "Y does not apply" without a specific document reference that proves it — the user will call out unsourced assertions. When uncertain, omit the claim or flag it as TBC.
- `SamayaDoc.__init__()` takes no arguments — it's a bare constructor. All setup is via `create_header()` and `create_footer()`.
- The `SamayaDoc` module is at `_Style-Guides/Doc Style Guide/samaya_doc_template.py` — import with `sys.path.insert(0, ...)` before import.
- Column widths in `add_table()` must sum to ~16.5 cm (A4 width 21.0 cm minus L2.5 + R2.0 margins).
- Never use `set_row_height()` — breaks wrapped text in table cells.
