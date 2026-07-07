# SVG Chart Embedding into DOCX

Full working pattern for rendering SVG charts as PNG via cairosvg and inserting into SamayaDoc DOCX documents.

## Prerequisites

```bash
pip3 install cairosvg
# macOS Homebrew cairo (required by cairosvg)
brew install cairo
```

**Always run scripts with:**
```bash
DYLD_FALLBACK_LIBRARY_PATH=/opt/homebrew/lib python3 gen_script.py
```

## Render helper functions

```python
import tempfile, os

def render_svg_to_png(svg_content, w=1200, h=440):
    """Convert SVG string to a PNG file and return path."""
    import cairosvg
    fd, path = tempfile.mkstemp(suffix='.png')
    os.close(fd)
    cairosvg.svg2png(
        bytestring=svg_content.encode('utf-8'),
        write_to=path,
        output_width=w,
        output_height=h
    )
    return path

def render_svg_to_png_width(svg_content, w, h):
    """Convert SVG string to PNG with custom dimensions."""
    import cairosvg
    fd, path = tempfile.mkstemp(suffix='.png')
    os.close(fd)
    cairosvg.svg2png(
        bytestring=svg_content.encode('utf-8'),
        write_to=path,
        output_width=w,
        output_height=h
    )
    return path
```

## Insertion pattern

```python
from samaya_doc_template import SamayaDoc
from docx.shared import Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH

doc = SamayaDoc()
# ... header, footer, sections ...

# Render SVG to temp PNG
chart_path = render_svg_to_png(MY_SVG_CONSTANT)

# Insert centered in DOCX
p = doc.doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
run = p.add_run()
run.add_picture(chart_path, width=Cm(14.5))  # 14.5cm = fits A4 with margins

# Clean up temp file immediately
os.unlink(chart_path)
```

**Key points:**
- Use `p.alignment = WD_ALIGN_PARAGRAPH.CENTER` on the paragraph, not XML manipulation
- `width=Cm(14.5)` for A4 page (16cm text area minus margins)
- 2x resolution (1200px) renders crisp at 14.5cm on screen
- Always `os.unlink()` after insertion — temp files accumulate
- Insert AFTER text, BEFORE the next section heading

## SVG design rules

- Use `font-family="Calibri,sans-serif"` to match the DOCX body font
- Set explicit `viewBox` for aspect ratio (e.g. `viewBox="0 0 600 200"`)
- Charts should be self-contained (no external CSS dependencies)
- Use Samaya palette: `#0F172A` (primary navy), `#F59E0B` (accent amber), `#64748B` (muted gray), `#E2E8F0` (light border)
- Wrap in a `<rect>` background matching `#F8FAFC` (bg-light) for clean look

## Dual HTML + DOCX generation skeleton

```python
# Gen script structure for dual output:

# 1. SVG chart constants
HEADCOUNT_SVG = '''<svg ...>...</svg>'''
PHASESTRIP_SVG = '''<svg ...>...</svg>'''

# 2. Write HTML
html = f'''<!DOCTYPE html>
...content with inline SVG...
'''
with open("output.html", 'w') as f:
    f.write(html)

# 3. Write DOCX
doc = SamayaDoc()
# ... build content, render SVGs to PNG, insert ...
doc.save("output.docx")
```

## Known pitfalls

| Issue | Fix |
|-------|-----|
| `OSError: no library called "cairo-2"` | Set `DYLD_FALLBACK_LIBRARY_PATH=/opt/homebrew/lib` |
| PNG too large for page | Scale to `Cm(14.5)` max width |
| SVG fonts don't match DOCX | Use `Calibri,sans-serif` in SVG text elements |
| Temp files left behind | Always `os.unlink(chart_path)` after `run.add_picture()` |
| execute_code can't find cairosvg | Run via `terminal()` with env var instead of `execute_code` |
| Image not centered | Use `p.alignment = WD_ALIGN_PARAGRAPH.CENTER` on the paragraph, not XML manipulation |
| Arrow routing between rows | When connecting Row 1 end to Row 2 start, use an L-shaped path (`Mx1,y1 Lx1,midY Lx2,midY Lx2,y2`) — never drop straight down if the target box is at a different x position |
| Text too small in printed DOCX | Use minimum 15px font size for box labels, 12px for sub-labels, 18px for titles. 13px renders unreadable when scaled to A4 width |
| viewBox wider than content | Crop viewBox to actual content bounds (e.g. `viewBox="0 0 1100 520"` instead of `1740` if content only spans x=30 to x=1040) — otherwise the image has empty space and centering looks off |
