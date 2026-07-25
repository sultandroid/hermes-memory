# DOCX Retrofit — Applying Samaya Branding to Existing Documents

**When to use:** A subcontractor, consultant, or third party submitted a .docx that needs Samaya branding before CG submission or internal use. The document was not generated with SamayaDoc — it uses wrong fonts, no headers, wrong margins, unformatted tables, wrong doc reference, or "the Contractor" instead of "Samaya".

## Workflow

1. Copy the original (never edit in place)
2. Inspect structure — paragraphs, tables, runs
3. Apply fixes in this order (font → margins → headers → text → tables → cover)

## 1. Copy before editing

```python
import shutil
shutil.copy(original_path, output_path)
```

## 2. Inspect the document first

Always check how text is structured before editing — text is often split across runs:

```python
from docx import Document

doc = Document(path)

# Check how paragraphs store text
for i, p in enumerate(doc.paragraphs[:5]):
    print(f"Para {i}: text={repr(p.text[:80])}")
    print(f"  runs={[r.text for r in p.runs]}")
```

### ⚠️ Split-run pitfall

DOCX often splits text across runs at unexpected boundaries (e.g. "R0" in run[0], "1" in run[1], or "Do" in run[0], "c" in run[1], " Ref:" in run[2]). Standard `run.text.replace()` will miss these because neither run contains the full target string.

**Fix — XML-level text replacement for fragmented runs:**

```python
from lxml import etree

W = '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}'

def replace_paragraph_text_xml(para, old_text, new_text):
    """Replace text across fragmented runs by operating at XML level."""
    t_elems = para._p.findall(f'.//{W}t')
    
    # Collect all text
    all_text = ''
    for t in t_elems:
        all_text += (t.text or '')
    
    if old_text not in all_text:
        return False
    
    # Build new full text
    start = all_text.index(old_text)
    end = start + len(old_text)
    new_all = all_text[:start] + new_text + all_text[end:]
    
    # Redistribute — set first run to full new text, clear the rest
    first = True
    for t in t_elems:
        if first:
            t.text = new_all
            first = False
        else:
            t.text = ''
            parent = t.getparent()
            if parent is not None:
                parent.remove(t)
    return True
```

## 3. Apply fixes in order

### 3a. Set page margins (A4 portrait)

```python
from docx.shared import Cm

for section in doc.sections:
    section.top_margin = Cm(2.5)
    section.left_margin = Cm(2.5)
    section.bottom_margin = Cm(2.0)
    section.right_margin = Cm(2.0)
    section.page_width = Cm(21.0)
    section.page_height = Cm(29.7)
```

### 3b. Set font to Calibri throughout

```python
from docx.oxml.ns import qn, nsdecls
from docx.oxml import parse_xml

def set_font_calibri(doc):
    """Set Calibri on all paragraph runs and table cell runs."""
    body_font = 'Calibri'
    for p in doc.paragraphs:
        for run in p.runs:
            _set_run_font(run, body_font)
    for table in doc.tables:
        for row in table.rows:
            for cell in row.cells:
                for p in cell.paragraphs:
                    for run in p.runs:
                        _set_run_font(run, body_font)

def _set_run_font(run, font_name):
    rPr = run._r.find(qn('w:rPr'))
    if rPr is None:
        rPr = parse_xml(f'<w:rPr {nsdecls("w")}></w:rPr>')
        run._r.insert(0, rPr)
    rFonts = rPr.find(qn('w:rFonts'))
    if rFonts is None:
        rFonts = parse_xml(f'<w:rFonts {nsdecls("w")} w:ascii="{font_name}" w:hAnsi="{font_name}" w:cs="{font_name}"/>')
        rPr.insert(0, rFonts)
    else:
        rFonts.set(qn('w:ascii'), font_name)
        rFonts.set(qn('w:hAnsi'), font_name)
        rFonts.set(qn('w:cs'), font_name)
    # Ensure default size 11pt if not set
    sz = rPr.find(qn('w:sz'))
    if sz is None:
        sz = parse_xml(f'<w:sz {nsdecls("w")} w:val="22"/>')
        rPr.append(sz)
```

### 3c. Fix text replacements (style + terminology)

Common Samaya fixes:

| Find | Replace |
|------|---------|
| `the Contractor` | `Samaya` |
| `the Contractor's` | `Samaya's` |
| `as per` | `per` |
| `innovative` | `effective` |
| `world-class` | `high-quality` |
| `R01` (cover) | `Rev 01` |
| `Samaya Investment Company` | `Samaya Investment` |

Apply with care — paragraphs where text is fragment across runs need the XML-level function above:

```python
for i, p in enumerate(doc.paragraphs):
    t = p.text or ''
    if 'the Contractor' in t:
        # Check if text is fragmented
        full_run_text = ''.join(r.text for r in p.runs)
        if 'the Contractor' in full_run_text and 'the Contractor' not in ''.join(r.text or '' for r in p.runs if r is p.runs[0]):
            # Fragmented — use XML approach
            replace_paragraph_text_xml(p, 'the Contractor', 'Samaya')
        else:
            # Simple — iterate runs
            for run in p.runs:
                if 'the Contractor' in (run.text or ''):
                    run.text = run.text.replace('the Contractor', 'Samaya')
```

### 3d. Fix document reference

Replace wrong document codes with correct MOC-MUS-ASE- prefix:

```python
# Example: replace "AMA/SMP-01" → "MOC-MUS-ASE-1KH-PL-0055"
for i, p in enumerate(doc.paragraphs):
    if 'AMA/SMP-01' in (p.text or ''):
        replace_paragraph_text_xml(p, 'AMA/SMP-01', 'MOC-MUS-ASE-1KH-PL-0055')
```

### 3e. Style table headers (navy background)

```python
from docx.oxml.ns import qn, nsdecls
from docx.oxml import parse_xml
from docx.shared import RGBColor, Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH

W = '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}'
NAVY = '1E293B'
WHITE = RGBColor(0xFF, 0xFF, 0xFF)

for table in doc.tables:
    for ci, cell in enumerate(table.rows[0].cells):
        tcPr = cell._tc.find(f'{W}tcPr')
        if tcPr is None:
            tcPr = parse_xml(f'<w:tcPr {nsdecls("w")}></w:tcPr>')
            cell._tc.insert(0, tcPr)
        # Remove existing shading
        existing = tcPr.find(f'{W}shd')
        if existing is not None:
            tcPr.remove(existing)
        # Add navy shading
        shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{NAVY}" w:val="clear"/>')
        tcPr.append(shd)
        # White bold centered text
        for p in cell.paragraphs:
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            for run in p.runs:
                run.font.color.rgb = WHITE
                run.font.bold = True
                run.font.size = Pt(9.5)
```

### 3f. Clean up document history table

Many subcontractor DOCXs have duplicate rows (one with names, one with roles, one empty). Keep one per revision:

```python
for table in doc.tables:
    row0_text = ' '.join([c.text.strip()[:20] for c in table.rows[0].cells]).lower()
    if 'rev' in row0_text and 'developed' in row0_text:
        # Group by revision number
        groups = {}
        for ri in range(1, len(table.rows)):
            cell0 = table.rows[ri].cells[0].text.strip()
            rev_num = cell0.split('\n')[0].strip()
            groups.setdefault(rev_num, []).append(ri)
        
        rows_to_remove = []
        for rev, indices in groups.items():
            if len(indices) > 1:
                # Keep first (usually most complete), remove rest
                rows_to_remove.extend(indices[1:])
        
        tr_elems = table._tbl.findall(f'{W}tr')
        for ri in sorted(rows_to_remove, reverse=True):
            table._tbl.remove(tr_elems[ri])
```

## 4. Verify after all fixes

```python
doc2 = Document(output_path)
full = '\n'.join([p.text for p in doc2.paragraphs])

# Check all issues resolved
checks = {
    'Wrong doc ref': 'AMA/SMP-01' in full,
    'New doc ref': 'MOC-MUS-ASE-1KH-PL-0055' in full,
    'The Contractor': 'the contractor' in full.lower(),
    'as per': 'as per' in full.lower(),
    'Clichés': any(c in full.lower() for c in ['innovative', 'world-class']),
    'Cover R01': any(p.text.strip() == 'R01' for p in doc2.paragraphs),
    'Wrong company': 'samaya investment company' in full.lower(),
}

# Check margins
s = doc2.sections[0]
assert s.top_margin == Cm(2.5)
assert s.left_margin == Cm(2.5)

# Check table headers
navy_count = sum(
    1 for t in doc2.tables
    if t.rows[0].cells[0]._tc.find(f'{W}tcPr') is not None
    and t.rows[0].cells[0]._tc.find(f'{W}tcPr').find(f'{W}shd') is not None
    and t.rows[0].cells[0]._tc.find(f'{W}tcPr').find(f'{W}shd').get(f'{W}fill') == NAVY
)
print(f"Navy headers: {navy_count}/{len(doc2.tables)}")
```

## Common pitfalls

- **Split runs:** Always check `p.runs` before assuming `run.text.replace()` will work. If text is fragmented across runs, use the XML-level function.
- **Empty t elements after fix:** After removing fragmented runs, verify no stray empty runs remain (can cause spaces in rendered text).
- **OneDrive copy timing:** Writing to OneDrive paths can slow the script. Copy first to `/tmp/`, edit there, then `cp` to final destination.
- **Font not applying:** If a run has explicit font set in its XML, changing the document default isn't enough — iterate all runs and set font directly.
