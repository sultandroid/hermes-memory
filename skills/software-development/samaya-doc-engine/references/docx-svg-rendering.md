# DOCX SVG Rendering & Post-Processing

> Session: 2026-07-13 — SMP Rev 03 DOCX generation
> Captures SVG→RGB PNG rendering fix, cairo library path, and post-processing formatting.

## SVG → RGB PNG Rendering

cairosvg outputs RGBA PNGs by default. Word on macOS does NOT render RGBA — images appear as blank/transparent boxes. Always convert to RGB:

```python
from PIL import Image
import io

def render_svg_to_rgb_png(svg_content, width=1600):
    import cairosvg
    png_data = cairosvg.svg2png(bytestring=svg_content.encode('utf-8'), output_width=width)
    img = Image.open(io.BytesIO(png_data))
    if img.mode == 'RGBA':
        bg = Image.new('RGB', img.size, (255, 255, 255))
        bg.paste(img, mask=img.split()[3])
        buf = io.BytesIO()
        bg.save(buf, format='PNG', optimize=True)
        return buf.getvalue()
    return png_data
```

## cairo Library Path (macOS + Homebrew)

cairosvg needs the system cairo library. On macOS with Homebrew:

```bash
# Install
brew install cairo

# Run with correct library path
DYLD_LIBRARY_PATH=/opt/homebrew/lib python3 gen_smp_docx.py
```

Without `DYLD_LIBRARY_PATH`, Python's ctypes can't find `libcairo.2.dylib` and raises:
```
OSError: no library called "cairo-2" was found
```

## SVG XML Pitfall: Unescaped &

SVG text content containing `&` (e.g. `T&C`, `O&M`, `D&B`, `FF&E`) causes cairosvg XML parse errors:

```
xml.etree.ElementTree.ParseError: not well-formed (invalid token)
```

**Fix**: Use `&amp;` in SVG text nodes:
```xml
<!-- WRONG -->
<text>T&C Mgr - TBC</text>
<!-- RIGHT -->
<text>T&amp;C Mgr - TBC</text>
```

## Post-Processing Formatting Fixes

Apply after all content is generated, before `doc.save()`:

### 1. pageBreakBefore on H2 Headings

```python
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

for p in doc.doc.paragraphs:
    runs = p.runs
    if runs and runs[0].font.size and runs[0].font.size == Pt(14) and runs[0].font.bold:
        pPr = p._p.get_or_add_pPr()
        pPr.append(OxmlElement('w:pageBreakBefore'))
```

### 2. cantSplit on Table Rows + Compact Margins

```python
for table in doc.doc.tables:
    for row in table.rows:
        trPr = row._tr.get_or_add_trPr()
        trPr.append(OxmlElement('w:cantSplit'))
        for cell in row.cells:
            tcPr = cell._tc.get_or_add_tcPr()
            tcMar = parse_xml(
                f'<w:tcMar {nsdecls("w")}>'
                f'  <w:top w:w="14" w:type="dxa"/>'
                f'  <w:bottom w:w="14" w:type="dxa"/>'
                f'  <w:start w:w="28" w:type="dxa"/>'
                f'  <w:end w:w="28" w:type="dxa"/>'
                f'</w:tcMar>'
            )
            tcPr.append(tcMar)
```

### 3. 9pt Halftone on Descriptive Paragraphs

Short descriptive paragraphs between headings and tables (e.g. "4 spheres of influence showing...") should be 9pt `#64748B` (MEDIUM_GRAY):

```python
remark_keywords = [
    "4 spheres of influence", "2x2 graphical classification",
    "Project organisational structure", "5-tier escalation path",
    "R = Responsible", "9 attributes per stakeholder",
]
for p in doc.doc.paragraphs:
    text = p.text.strip()
    if any(kw.lower() in text.lower() for kw in remark_keywords):
        for run in p.runs:
            run.font.size = Pt(9)
            run.font.color.rgb = SamayaColors.MEDIUM_GRAY
```

## Verification

After generation, verify the DOCX:

```python
from docx import Document
import zipfile

doc = Document(path)
print(f"Tables: {len(doc.tables)}")
print(f"Paragraphs: {len(doc.paragraphs)}")

# Check images are RGB
with zipfile.ZipFile(path) as z:
    for f in z.namelist():
        if f.startswith('word/media/'):
            from PIL import Image
            import io
            img = Image.open(io.BytesIO(z.read(f)))
            print(f"{f}: mode={img.mode}, size={img.size}")
            # All SVG-rendered images should be RGB, not RGBA
```

## Full Script Template

```python
#!/usr/bin/env python3
import os, sys, tempfile, io
from PIL import Image

# Import template
sys.path.insert(0, _template_dir)
from samaya_doc_template import SamayaDoc, SamayaColors
from docx.shared import Pt, Cm
from docx.oxml.ns import qn, nsdecls
from docx.oxml import parse_xml, OxmlElement

# SVG rendering
def render_svg_to_rgb_png(svg_content, width=1600):
    import cairosvg
    png_data = cairosvg.svg2png(bytestring=svg_content.encode('utf-8'), output_width=width)
    img = Image.open(io.BytesIO(png_data))
    if img.mode == 'RGBA':
        bg = Image.new('RGB', img.size, (255, 255, 255))
        bg.paste(img, mask=img.split()[3])
        buf = io.BytesIO()
        bg.save(buf, format='PNG', optimize=True)
        return buf.getvalue()
    return png_data

def add_svg_to_doc(doc, svg_content, width_cm=16.5):
    png_data = render_svg_to_rgb_png(svg_content)
    with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as f:
        f.write(png_data)
        tmp_path = f.name
    p = doc.doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run()
    run.add_picture(tmp_path, width=Cm(width_cm))
    os.unlink(tmp_path)
    return p

# Symbol cleanup
def clean_symbols(doc):
    replacements = { ... }  # see SKILL.md
    for p in doc.doc.paragraphs:
        for run in p.runs:
            for old, new in replacements.items():
                if old in run.text:
                    run.text = run.text.replace(old, new)
    for t in doc.doc.tables:
        for row in t.rows:
            for cell in row.cells:
                for p in cell.paragraphs:
                    for run in p.runs:
                        for old, new in replacements.items():
                            if old in run.text:
                                run.text = run.text.replace(old, new)

# Post-processing
def apply_formatting_fixes(doc):
    ...  # see above

def main():
    doc = SamayaDoc()
    doc.create_header(...)
    doc.create_footer(...)
    doc.add_h1("TITLE")
    doc.add_h2("1.0", "SECTION")
    doc.add_h3("1.1", "SUBSECTION")
    doc.add_body("Body text.")
    doc.add_table(headers, rows, col_widths_cm=[...])
    add_svg_to_doc(doc, SVG_CONSTANT, width_cm=16.5)
    clean_symbols(doc)
    apply_formatting_fixes(doc)
    doc.save(output_path)

if __name__ == '__main__':
    main()
```
