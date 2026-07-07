# Flowchart SVG Patterns for DOCX Reports

Patterns for creating process flowcharts as inline SVGs, converting to PNG via cairosvg, and embedding in SamayaDoc DOCX documents.

## SVG Design Rules for DOCX Flowcharts

- `viewBox` must match actual content bounds — don't leave empty space or the image won't center properly
- Use `font-family="Calibri, Arial, sans-serif"` to match DOCX body font
- Samaya palette: `#1E293B` (navy boxes), `#334155` (alternate boxes), `#B01E2F` (diamonds/numbers), `#64748B` (labels/lines), `#F1F5F9` (backgrounds)
- Boxes: `rx="8" ry="8"` for rounded corners
- Arrows: `stroke-width="3"` for readability, `marker-end="url(#arrow)"` with custom arrowhead
- Title: 18px bold navy, centered at top

## Common Flowchart Patterns

### 1. Linear Process (left to right, single row)

```
viewBox="0 0 {N*boxWidth + (N-1)*gap + margins} 200"
Boxes: rect x="30" y="60" width="190" height="80"
Arrows: line x1="220" y1="100" x2="280" y2="100"
```

### 2. Two-Row Process with L-Shaped Return

Row 1: Steps 1-4 left to right
Row 2: Steps 5-8 left to right
Connection: L-shaped path from Step 4 bottom → Step 5 top

```svg
<!-- Down arrow row 1→2 -->
<path d="M940,180 L940,210 L130,210 L130,250" fill="none" stroke="#1E293B" stroke-width="3" marker-end="url(#arrow2)"/>
```

### 3. Control Cycle (closed loop)

Process steps in a circle/loop with feedback path back to sensor.

```svg
<!-- Feedback loop -->
<path d="M615,150 L615,380 L850,380 L850,180" fill="none" stroke="#64748B" stroke-width="2" stroke-dasharray="8,4" marker-end="url(#arrow)"/>
```

### 4. Decision Diamond

```svg
<polygon points="850,40 950,110 850,180 750,110" class="diamond"/>
<text x="850" y="105" class="diamond-text">Controller</text>
<text x="850" y="125" class="diamond-text">Compare</text>
<text x="850" y="145" class="diamond-text">to Setpoint</text>
```

## Arrow Definitions

```svg
<defs>
  <marker id="arrow" markerWidth="14" markerHeight="10" refX="14" refY="5" orient="auto">
    <polygon points="0 0, 14 5, 0 10" fill="#1E293B"/>
  </marker>
</defs>
```

## Insertion into DOCX

```python
from docx.enum.text import WD_ALIGN_PARAGRAPH

def add_svg_to_doc(doc_obj, svg_path, width_cm):
    """Convert SVG to PNG via cairosvg, then add as centered picture."""
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

Always run with: `DYLD_FALLBACK_LIBRARY_PATH=/opt/homebrew/lib python3 gen_script.py`

## Pitfalls

- **viewBox too wide**: If SVG viewBox is wider than content, the image appears off-center even with `p.alignment = CENTER`. Crop viewBox to actual content bounds.
- **Arrow not touching next box**: Arrow endpoint must reach the target box's edge (e.g. y2=250 for a box starting at y=250). 10px gap = visible disconnect.
- **L-shaped arrow routing**: Down arrow from Step 4 (x=940) must route to Step 5 (x=130), not drop straight down into empty space.
- **Font size**: 16px for box titles, 13px for subtitles, 12px for labels — smaller than that is unreadable when printed.
- **Temp file cleanup**: Always `os.unlink(png_path)` after insertion.
