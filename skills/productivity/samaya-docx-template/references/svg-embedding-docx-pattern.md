# SVG → DOCX Embedding Pattern

## Problem
`python-docx` does not support SVG natively — `run.add_picture(svg_path)` raises `UnrecognizedImageError`.

## Solution
Convert SVG to PNG via cairosvg, then embed as a picture.

## Prerequisites
```bash
brew install cairo
pip install cairosvg
```

Always run with:
```bash
DYLD_FALLBACK_LIBRARY_PATH=/opt/homebrew/lib python3 gen_script.py
```

## Working `add_svg_to_doc` function — two variants

### Variant A: SVG from file path

```python
from docx.shared import Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH

def add_svg_to_doc(doc_obj, svg_path, width_cm):
    """Convert SVG file to PNG via cairosvg, then add as centered picture."""
    import cairosvg
    png_path = svg_path.replace('.svg', '.png')
    with open(svg_path, 'rb') as f:
        svg_data = f.read()
    png_data = cairosvg.svg2png(svg_data, output_width=1740, output_height=None)
    with open(png_path, 'wb') as f:
        f.write(png_data)
    p = doc_obj.doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run()
    run.add_picture(png_path, width=Cm(width_cm))
    os.unlink(png_path)
```

### Variant B: SVG from inline string (preferred for generated scripts)

More practical when SVG is defined as a Python string constant in the gen script — no temp SVG file needed:

```python
import tempfile, os, cairosvg
from docx.shared import Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH

def add_svg_to_doc(doc, svg_content, width_cm=16.5):
    """Render SVG string to PNG and insert into SamayaDoc document."""
    png_data = cairosvg.svg2png(bytestring=svg_content.encode('utf-8'), output_width=1740)
    with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as f:
        f.write(png_data)
        temp_path = f.name
    p = doc.doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run()
    run.add_picture(temp_path, width=Cm(width_cm))
    os.unlink(temp_path)
    return p
```

**IMPORTANT:** `SamayaDoc` has NO `.add_paragraph()` method. To insert raw paragraphs (e.g. for images), access the underlying python-docx `Document` via `doc.doc.add_paragraph()`. Calling `doc.add_paragraph()` will raise `AttributeError`.

**DO NOT confuse**: `doc.add_body()` exists (SamayaDoc wrapper), `doc.doc.add_paragraph()` exists (python-docx raw access), but `doc.add_paragraph()` does NOT exist.

## Critical: viewBox must match content bounds

The SVG `viewBox` must be cropped to the actual content, not the full canvas width.

**WRONG** — content only spans x=30 to x=1040 but viewBox is 1740 wide:
```svg
<svg viewBox="0 0 1740 520">
```
Result: image appears off-center because the right 700px is empty space.

**RIGHT** — viewBox matches content:
```svg
<svg viewBox="0 0 1100 520">
```

Rule: set viewBox width to the rightmost content element's x + width, not the design canvas width.

## Flowchart arrow routing rules

When creating multi-row flowcharts (Row 1 → Row 2):

1. **Down arrow from Row 1 to Row 2**: must route to the START of Row 2 (Step 5), not drop straight down from Step 4
2. Use an L-shaped path: `M{x4},{y1_bottom} L{x4},{mid_y} L{x5},{mid_y} L{x5},{y2_top}`
3. The arrow endpoint (`y2`) must exactly equal the target box's `y` value — even a 10px gap means the arrowhead doesn't touch the box
4. Arrow stroke-width should match the visual weight of the boxes (3px for 100px-tall boxes)

Example:
```python
# From Step 4 (x=940, bottom=180) to Step 5 (x=30, top=250)
path = "M940,180 L940,210 L130,210 L130,250"
```

## SVG sizing for A4 DOCX

- Width: 16.5cm (full text width) → viewBox width ~1650-1740 units at 10 units/mm
- Font sizes: 16px for box titles, 13px for sub-text, 12px for labels
- Box sizes: 200x100px for main steps, with 8px border-radius
- Arrow markers: 14x10px with stroke-width 3
