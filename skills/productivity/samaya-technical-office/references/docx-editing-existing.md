# Editing Existing DOCX Files with python-docx

Covers inserting annotated paragraphs, updating tables/cells, modifying headers/footers, and formatting runs in existing .docx files.

## Open and Save

```python
from docx import Document

doc = Document("input.docx")
# ... edits ...
doc.save("input.docx")          # overwrite in-place
doc.save("output.docx")         # save as new file
```

## Insert a Paragraph After a Specific Heading

Use `addnext()` on the heading's XML element to position the new paragraph immediately after it:

```python
from docx.shared import Pt, RGBColor

HALFTONE = RGBColor(0x99, 0x99, 0x99)  # medium gray

for para in doc.paragraphs:
    if para.text.strip().startswith("6.1  DESIGN GOVERNANCE"):
        new_p = doc.add_paragraph()
        run = new_p.add_run("Ref: PL-0015 Rev 04 sec 5.1 · Contract 0010003521 (SoW)")
        run.font.size = Pt(7.5)
        run.font.color.rgb = HALFTONE
        run.font.italic = True

        # Move new paragraph right after the heading in XML order
        heading_elem = para._element
        new_elem = new_p._element
        heading_elem.addnext(new_elem)
        break
```

## Update Table Cell Content

Iterate tables, find by header text, then modify cell paragraphs:

```python
for table in doc.tables:
    if table.cell(0, 0).text.strip() == "GATE" and table.cell(0, 1).text.strip() == "RIBA STAGE":
        cell = table.cell(1, 1)
        if cell.paragraphs[0].runs:
            cell.paragraphs[0].runs[0].text = "Pre-contract (RIBA 2)"
            for r in cell.paragraphs[0].runs[1:]:
                r.text = ""
        break
```

## Modify Header Text

```python
for section in doc.sections:
    header = section.header
    for para in header.paragraphs:
        for run in para.runs:
            if "Rev:" in run.text and "A" in run.text:
                run.text = run.text.replace("Rev: A", "Rev: 01")
```

## Text Replacement Across All Content

Apply a replacement map to paragraphs, tables, headers, and footers:

```python
replacements = [
    ("PEP Rev 04", "PL-0015 Rev 04"),
    ("DMP Rev C03", "PL-0013 Rev C03"),
    ("BEP Rev 01", "PL-0021 Rev 01"),
    ("Contract 0010", "Contract 0010003521"),  # fix truncated refs
]

for para in doc.paragraphs:
    old = para.text; new = old
    for a, b in replacements: new = new.replace(a, b)
    if new != old and para.runs:
        para.runs[0].text = new
        for r in para.runs[1:]: r.text = ""

for table in doc.tables:
    for row in table.rows:
        for cell in row.cells:
            for p in cell.paragraphs:
                old = p.text; new = old
                for a, b in replacements: new = new.replace(a, b)
                if new != old and p.runs:
                    p.runs[0].text = new
                    for r in p.runs[1:]: r.text = ""

for section in doc.sections:
    for container in [section.header, section.footer]:
        for para in container.paragraphs:
            if para.runs:
                old = para.text; new = old
                for a, b in replacements: new = new.replace(a, b)
                if new != old:
                    para.runs[0].text = new
                    for r in para.runs[1:]: r.text = ""
```

## Pitfalls

- **`addnext()` only works on XML elements**, not on the Paragraph object directly. Always use `para._element.addnext(new_p._element)`.
- **`doc.add_paragraph()` appends to the end** — you MUST move it with `addnext()` for correct positioning.
- **Merged cells**: Writing to a merged cell raises `AttributeError: 'MergedCell'`. Write to the top-left cell of the merged range only.
- **Table cells** created by merging/splitting may have inconsistent paragraph counts. Check `cell.paragraphs[0]` exists before accessing `.runs`.
- **Headers with tables**: Some Word headers use tables not paragraphs. Iterate `header.tables` as well as `header.paragraphs`.
- **Don't use `replace_all=True`** on text that appears as substring of longer text (e.g., "Contract 0010" inside "Contract 0010003521"). Do specific replacements in order.
