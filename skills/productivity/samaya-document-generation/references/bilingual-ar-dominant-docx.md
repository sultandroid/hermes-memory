# Bilingual AR-Dominant DOCX (RTL + Arabic fonts) — SamayaDoc post-processing

SamayaDoc outputs everything in **Calibri, left-to-right**. It has no RTL/Arabic support. For a
bilingual report where **Arabic is the leading language** (e.g. an Arabic-English variation claim,
formal letter to MoC, or any document the user wants "عربي سائد"), you must **post-process the
generated .docx** after calling `doc.save()`.

## Pattern (proven 2026-08-30 — FF pump VO claim report)

1. Build with SamayaDoc normally (header/footer/tables via its API, Arabic/English interleaved so
   each section is "Arabic text, then English text").
2. After `doc.save()` (or before), walk the underlying python-docx object (`doc.doc`) and fix fonts
   + direction on any element containing Arabic.

```python
import re
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn

AR_FONT = "IBM Plex Sans Arabic"   # Samaya bilingual font (per style guide)
EN_FONT = "Calibri"

def has_arabic(s):
    return bool(re.search(r'[\u0600-\u06FF]', s))

def set_rtl(paragraph):
    pPr = paragraph._p.get_or_add_pPr()
    bidi = pPr.find(qn('w:bidi'))
    if bidi is None:
        bidi = pPr.makeelement(qn('w:bidi'), {})
        pPr.append(bidi)

def fix_paragraph_fonts(paragraph):
    txt = paragraph.text
    if not has_arabic(txt):
        return
    set_rtl(paragraph)
    paragraph.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    for run in paragraph.runs:
        rPr = run._r.get_or_add_rPr()
        rFonts = rPr.find(qn('w:rFonts'))
        if rFonts is None:
            rFonts = rPr.makeelement(qn('w:rFonts'), {})
            rPr.append(rFonts)
        rFonts.set(qn('w:ascii'), EN_FONT)
        rFonts.set(qn('w:hAnsi'), EN_FONT)
        rFonts.set(qn('w:cs'), AR_FONT)      # complex-script font = Arabic
        rPr.set(qn('w:rtl'), '1')

# tables need per-cell treatment too
def fix_table_rtl(table):
    for row in table.rows:
        for cell in row.cells:
            for p in cell.paragraphs:
                if has_arabic(p.text):
                    set_rtl(p)
                    p.alignment = WD_ALIGN_PARAGRAPH.RIGHT
                    for run in p.runs:
                        rPr = run._r.get_or_add_rPr()
                        rFonts = rPr.find(qn('w:rFonts'))
                        if rFonts is None:
                            rFonts = rPr.makeelement(qn('w:rFonts'), {})
                            rPr.append(rFonts)
                        rFonts.set(qn('w:cs'), AR_FONT)
                        rPr.set(qn('w:rtl'), '1')

# after generation:
for p in doc.doc.paragraphs:
    fix_paragraph_fonts(p)
for t in doc.doc.tables:
    fix_table_rtl(t)
doc.save(output_path)
```

## Verify, don't guess

Check the **XML**, not `paragraph.text`, for styling — scanning body text for the font name always
returns MISSING (it's not in the text).

```python
from docx.oxml.ns import qn
for p in d.paragraphs:
    if 'العنوان' in p.text:
        pPr = p._p.find(qn('w:pPr'))
        assert pPr.find(qn('w:bidi')) is not None          # RTL applied
        for run in p.runs[:1]:
            rf = run._r.find(qn('w:rPr')).find(qn('w:rFonts'))
            assert rf.get(qn('w:cs')) == 'IBM Plex Sans Arabic'
        break
```

## Layout rule
- Arabic leading, English after — e.g. every section heading and body: `"الملخص التنفيذي | EXECUTIVE SUMMARY"`.
- Headings/table headers can carry both: `"الملخص التنفيذي | Executive Summary"`; body paragraphs state the
  argument in Arabic first, then an English mirror.
- Keep the header/footer (SamayaDoc `create_header`) bilingual where the doc_ref/date justify it.

## Pitfalls
- **`add_body` line spacing is EXACTLY 13pt** — mixing Arabic into a fixed line-height run can clip
  Arabic glyphs. If Arabic looks cut off, widen line spacing on the affected paragraphs after the fact.
- **Do not overwrite the whole doc with write_file** — generate via `doc.save()` from the script. The
  `.docx` is binary; patch/write_file is for source .md, not the output.
- **NULL-byte placeholder template** — import SamayaDoc from the repo clone
  `~/aseer-museum-pm/_Style-Guides/Doc Style Guide/`, not OneDrive (see main SKILL.md pitfall).
