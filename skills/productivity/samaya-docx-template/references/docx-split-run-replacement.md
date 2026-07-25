# DOCX Split-Run Text Replacement

**When to use:** User asks to fix a document reference, revision number, company name, or other text in an existing DOCX where the text is split across multiple XML runs.

## The problem

In DOCX files, text like "R01" or "AMA/SMP-01" can be split across multiple `<w:r>` elements:

| Visible text | Actual runs | Why this matters |
|---|---|---|
| `R01` | `['R0', '1']` | `run.text.replace('R01', 'Rev 01')` finds nothing — neither run contains the full string |
| `Doc Ref: AMA/SMP-01` | `['Doc Ref: AM', 'A', '/SMP-01 ']` | Split across 3 runs — any single-run replacement misses it |
| `Rev 01` | `['Re', 'v']` (after partial fix) | Previous partial fix left it broken across runs |

This happens because:
- The original author typed the text and Word split it at format boundaries (bold/italic changes, spellcheck corrections, paste operations)
- A previous python-docx edit replaced part of the text but didn't merge the runs

## Detection

```python
# Find paragraphs where paragraph.text differs from what any single run contains
for i, p in enumerate(doc.paragraphs):
    full = p.text
    # Check if any run contains the full string
    combined = ''.join(r.text for r in p.runs)
    # If combined == full but no single run has the target, split-run problem
    # Example: looking for 'R01' but runs are ['R0', '1']
    if full == combined and 'R01' in full:
        has_full = any('R01' in (r.text or '') for r in p.runs)
        if not has_full:
            print(f"Para {i}: split-run issue - text='{full[:50]}'")
```

## Fix: merge all runs into one

The simplest fix is to merge all runs in a paragraph into a single run:

```python
def merge_paragraph_runs(para):
    """Merge all runs in a paragraph into a single run."""
    if len(para.runs) <= 1:
        return
    
    W = '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}'
    full_text = ''.join(r.text for r in para.runs)
    
    # Collect all t elements
    t_elems = para._p.findall(f'.//{W}t')
    
    if not t_elems:
        return
    
    # Put all text in the first t element
    t_elems[0].text = full_text
    
    # Clear and remove the rest
    for t in t_elems[1:]:
        t.text = ''
        parent = t.getparent()
        if parent is not None:
            parent.remove(t)
```

**Use case:** `merge_paragraph_runs(p)` then `p.runs[0].text = p.runs[0].text.replace('R01', 'Rev 01')`

## Fix: replace text across runs without merging

When you need to preserve run formatting (different font sizes, bold/italic within the same paragraph), merge and restore:

```python
def replace_across_runs(para, old_text, new_text):
    """Replace old_text with new_text across multiple runs, preserving first run's formatting."""
    full = para.text or ''
    if old_text not in full:
        return False
    
    # Store formatting of each run
    formats = []
    for run in para.runs:
        fmt = {
            'bold': run.font.bold,
            'italic': run.font.italic,
            'size': run.font.size,
            'color': run.font.color.rgb if run.font.color and run.font.color.rgb else None,
            'name': run.font.name,
        }
        formats.append(fmt)
    
    new_full = full.replace(old_text, new_text, 1)
    
    # Merge then redistribute
    W = '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}'
    t_elems = para._p.findall(f'.//{W}t')
    
    if not t_elems:
        return False
    
    # Put all text in first, clear others
    t_elems[0].text = new_full
    for t in t_elems[1:]:
        t.text = ''
        parent = t.getparent()
        if parent is not None:
            parent.remove(t)
    
    return True
```

## Full workflow: Samaya-brand an existing DOCX

When applying Samaya branding to an existing DOCX (e.g., Fida's SMP), follow this sequence:

```python
from docx import Document
from docx.shared import Pt, Cm, RGBColor
from docx.oxml.ns import qn, nsdecls
from docx.oxml import parse_xml
import shutil, re

# 1. Copy the file
src = "original.docx"
dst = "output.docx"
shutil.copy2(src, dst)
doc = Document(dst)

# 2. Fix split-run text references first
for p in doc.paragraphs:
    for old, new in [('R01', 'Rev 01'), ('AMA/SMP-01', 'MOC-MUS-ASE-1KH-PL-0055')]:
        if old in (p.text or '') and not any(old in (r.text or '') for r in p.runs):
            merge_paragraph_runs(p)
            for run in p.runs:
                run.text = run.text.replace(old, new)

# 3. Fix "the Contractor" -> "Samaya" (case-insensitive)
for p in doc.paragraphs:
    for run in p.runs:
        run.text = re.sub(r'(?i)\bthe\s+[Cc]ontractor\b', 'Samaya', run.text)

# 4. Fix "as per" -> "per"
for p in doc.paragraphs:
    for run in p.runs:
        run.text = re.sub(r'(?i)\bas per\b', 'per', run.text)

# 5. Set page margins
for section in doc.sections:
    section.top_margin = Cm(2.5)
    section.left_margin = Cm(2.5)
    section.bottom_margin = Cm(2.0)
    section.right_margin = Cm(2.0)

# 6. Set Calibri font on all runs
for p in doc.paragraphs:
    for run in p.runs:
        run.font.name = 'Calibri'
        rPr = run._r.find(qn('w:rPr'))
        if rPr is None:
            rPr = parse_xml(f'<w:rPr {nsdecls("w")}></w:rPr>')
            run._r.insert(0, rPr)
        rFonts = rPr.find(qn('w:rFonts'))
        if rFonts is None:
            rFonts = parse_xml(f'<w:rFonts {nsdecls("w")} w:ascii="Calibri" w:hAnsi="Calibri" w:cs="Calibri"/>')
            rPr.insert(0, rFonts)
        else:
            rFonts.set(qn('w:ascii'), 'Calibri')
            rFonts.set(qn('w:hAnsi'), 'Calibri')
            rFonts.set(qn('w:cs'), 'Calibri')

# 7. Style all table headers (navy #1E293B, white bold text)
for table in doc.tables:
    for ci, cell in enumerate(table.rows[0].cells):
        tcPr = cell._tc.find(qn('w:tcPr'))
        if tcPr is None:
            tcPr = parse_xml(f'<w:tcPr {nsdecls("w")}></w:tcPr>')
            cell._tc.insert(0, tcPr)
        # Remove existing shading
        existing = tcPr.find(qn('w:shd'))
        if existing is not None:
            tcPr.remove(existing)
        # Add navy shading
        shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="1E293B" w:val="clear"/>')
        tcPr.append(shd)
        # White bold text
        for p in cell.paragraphs:
            for run in p.runs:
                run.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
                run.font.bold = True
                run.font.size = Pt(9.5)

# 8. Apply Calibri to table body cells too
for table in doc.tables:
    for row in table.rows:
        for cell in row.cells:
            for p in cell.paragraphs:
                for run in p.runs:
                    run.font.name = 'Calibri'

# 9. Fix company name on cover
for p in doc.paragraphs:
    for run in p.runs:
        if 'Samaya Investment Company' in (run.text or ''):
            run.text = run.text.replace('Samaya Investment Company', 'Samaya Investment')

# 10. Save
doc.save(dst)
print(f"Saved: {dst}")
```

## Verification

```python
# Check remaining issues
doc2 = Document(dst)
full = '\n'.join([p.text for p in doc2.paragraphs])
print(f'Doc ref in doc: {"MOC-MUS-ASE" in full}')
print(f'AMA ref gone: {"AMA/SMP-01" not in full}')
print(f'R01 standalone: {any(p.text.strip()=="R01" for p in doc2.paragraphs)}')
print(f'Contractor: {"the Contractor" in full}')
print(f'as per: {"as per" in full.lower()}')

# Check fonts on a sample
for p in doc2.paragraphs[:5]:
    for run in p.runs:
        print(f'Font: {run.font.name}')
        break
    break

# Check table headers
W = '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}'
navy_count = 0
for table in doc2.tables:
    cell = table.rows[0].cells[0]
    tcPr = cell._tc.find(f'{W}tcPr')
    if tcPr is not None:
        shd = tcPr.find(f'{W}shd')
        if shd is not None and shd.get(f'{W}fill') == '1E293B':
            navy_count += 1
print(f'Navy headers: {navy_count}/{len(doc2.tables)}')
```

## Pitfalls

1. **Split runs are invisible to `run.text` replacement** — always check `p.text` vs `''.join(r.text for r in p.runs)` to detect split-run issues
2. **Merging runs loses per-run formatting** — if the paragraph has mixed bold/italic, merging discards it. Acceptable for cover page text (revision, doc ref) but not for body content
3. **OneDrive file operations are slow** — copying large DOCX files on OneDrive can timeout. Use longer timeouts (60-120s) or copy from temp
4. **Always work on a copy** — never edit the original; the user wants to keep the source as-is for reference
5. **Table cells with no runs** — `len(p.runs) == 0` means you must add a run via `p.add_run()` before setting text
