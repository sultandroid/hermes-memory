# DOCX Image Rendering Fix — Images Disappear After Bulk Edits

## Symptom
After bulk edits to a DOCX (page breaks, table cantSplit, column widths, symbol cleanup), embedded PNG images stop rendering in Word. The images are still in `word/media/`, relationships are intact, and drawing XML is well-formed — but Word shows a blank or broken image.

## Root Cause (3 factors)

1. **RGBA color mode** — cairosvg outputs RGBA PNGs. Word on macOS does NOT render RGBA PNGs reliably. Must convert to RGB with white background.
2. **Empty cNvPr names** — `pic:cNvPr name=""` or `name="tmpXXXX.png"` (temp filenames from cairosvg). Word reads cNvPr name for display; empty/temp names break rendering.
3. **Missing noChangeAspect** — `a:graphicFrameLocks` without `noChangeAspect="1"` can cause Word to mis-scale images during re-layout.

## Detection

```python
from docx import Document
from lxml import etree
import zipfile

doc = Document(path)
nsmap = {
    'a': 'http://schemas.openxmlformats.org/drawingml/2006/main',
    'pic': 'http://schemas.openxmlformats.org/drawingml/2006/picture',
    'wp': 'http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing',
}

# Check cNvPr names and noChangeAspect
for i, p in enumerate(doc.paragraphs):
    drawings = p._p.findall('.//' + qn('w:drawing'))
    for d in drawings:
        cNvPr = d.find('.//pic:cNvPr', nsmap)
        if cNvPr is not None:
            name = cNvPr.get('name')
            if not name or name.strip() == '' or 'tmp' in name:
                print(f"P{i}: BROKEN cNvPr name='{name}'")
        locks = d.findall('.//a:graphicFrameLocks', nsmap)
        for lock in locks:
            nca = lock.get('{http://schemas.openxmlformats.org/drawingml/2006/main}noChangeAspect')
            if nca != '1':
                print(f"P{i}: MISSING noChangeAspect=1")

# Check image color modes
with zipfile.ZipFile(path) as z:
    for f in z.namelist():
        if f.startswith('word/media/') and f.endswith('.png'):
            data = z.read(f)
            from PIL import Image
            import io
            img = Image.open(io.BytesIO(data))
            if img.mode == 'RGBA':
                print(f"{f}: RGBA mode (will not render in Word)")
```

## Complete Fix Script

Run this after EVERY python-docx edit pass that touches the document body:

```python
import zipfile, os, io, re
from lxml import etree
from PIL import Image

def fix_docx_images(docx_path):
    """Fix all 3 image rendering issues in a DOCX file."""
    
    with zipfile.ZipFile(docx_path, 'r') as zin:
        # --- Fix 1: RGBA -> RGB conversion ---
        media_fixes = {}
        for fname in zin.namelist():
            if fname.startswith('word/media/') and fname.endswith('.png'):
                data = zin.read(fname)
                img = Image.open(io.BytesIO(data))
                if img.mode == 'RGBA':
                    bg = Image.new('RGB', img.size, (255, 255, 255))
                    bg.paste(img, mask=img.split()[3])
                    buf = io.BytesIO()
                    bg.save(buf, format='PNG')
                    media_fixes[fname] = buf.getvalue()
                elif img.mode == 'P':
                    img = img.convert('RGB')
                    buf = io.BytesIO()
                    img.save(buf, format='PNG')
                    media_fixes[fname] = buf.getvalue()
        
        # --- Fix 2 & 3: cNvPr names + noChangeAspect ---
        doc_xml = zin.read('word/document.xml')
        root = etree.fromstring(doc_xml)
        
        NS = {
            'pic': 'http://schemas.openxmlformats.org/drawingml/2006/picture',
            'wp': 'http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing',
            'a': 'http://schemas.openxmlformats.org/drawingml/2006/main',
        }
        
        # Fix cNvPr names by position-matching to wp:docPr
        docprs = root.findall('.//wp:docPr', NS)
        cnvprs = root.findall('.//pic:cNvPr', NS)
        for i, cnvpr in enumerate(cnvprs):
            if i < len(docprs):
                cnvpr.set('name', docprs[i].get('name', f'Picture {i+1}'))
            else:
                cnvpr.set('name', f'Picture {i+1}')
        
        # Fix missing noChangeAspect
        for lock in root.findall('.//a:graphicFrameLocks', NS):
            if lock.get('noChangeAspect') is None:
                lock.set('noChangeAspect', '1')
        
        fixed_xml = etree.tostring(root, xml_declaration=True, encoding='UTF-8', standalone=True)
        
        # --- Remove orphaned media ---
        rels = zin.read('word/_rels/document.xml.rels').decode('utf-8')
        refs = re.findall(r'Target="([^"]*media[^"]*)"', rels)
        
        # --- Write fixed DOCX ---
        tmp_path = docx_path + '.fixed'
        with zipfile.ZipFile(tmp_path, 'w', zipfile.ZIP_DEFLATED) as zout:
            for item in zin.infolist():
                if item.filename == 'word/document.xml':
                    zout.writestr(item, fixed_xml)
                elif item.filename in media_fixes:
                    zout.writestr(item, media_fixes[item.filename])
                elif item.filename.startswith('word/media/'):
                    short = item.filename.split('/')[-1]
                    if not any(short in r for r in refs):
                        continue  # skip orphan
                    zout.writestr(item, zin.read(item.filename))
                else:
                    zout.writestr(item, zin.read(item.filename))
    
    os.replace(tmp_path, docx_path)
```

## Verification

```python
with zipfile.ZipFile(docx_path) as z:
    for f in z.namelist():
        if f.startswith('word/media/'):
            data = z.read(f)
            assert data[:8] == b'\x89PNG\r\n\x1a\n', f"{f} not a valid PNG"
    
    root = etree.fromstring(z.read('word/document.xml'))
    NS = {'pic': 'http://schemas.openxmlformats.org/drawingml/2006/picture'}
    for c in root.findall('.//pic:cNvPr', NS):
        assert c.get('name', '').strip(), f"cNvPr id={c.get('id')} still empty"
    
    NS2 = {'a': 'http://schemas.openxmlformats.org/drawingml/2006/main'}
    for l in root.findall('.//a:graphicFrameLocks', NS2):
        assert l.get('noChangeAspect') == '1', "Missing noChangeAspect"
```

## When to Run

After ANY python-docx edit that touches the document body — page breaks, cantSplit, column widths, symbol cleanup, paragraph spacing, font changes. The act of saving via python-docx triggers the cNvPr name corruption.

## Prevention in SVG->DOCX generation scripts

When generating a DOCX from SVGs via cairosvg, apply the RGBA->RGB conversion immediately after rendering:

```python
import cairosvg
from PIL import Image
import io

def render_svg_to_rgb_png(svg_string, output_width=1740):
    """Render SVG to RGB PNG (not RGBA) for Word compatibility."""
    png_data = cairosvg.svg2png(bytestring=svg_string.encode('utf-8'), output_width=output_width)
    img = Image.open(io.BytesIO(png_data))
    if img.mode == 'RGBA':
        bg = Image.new('RGB', img.size, (255, 255, 255))
        bg.paste(img, mask=img.split()[3])
        buf = io.BytesIO()
        bg.save(buf, format='PNG')
        return buf.getvalue()
    return png_data
```
