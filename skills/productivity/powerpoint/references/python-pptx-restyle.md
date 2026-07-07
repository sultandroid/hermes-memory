# python-pptx Programmatic Restyle Pattern

Full script pattern for restyling an existing deck without touching images, callouts, or table content. Tested on a 36-slide deck (ASM_3D_Views_Schedules).

## Complete Script Structure

```python
#!/usr/bin/env python3
"""
Restyle a .pptx deck: backgrounds, shapes, tables, fonts.
Preserves all images, callouts, table content, Arabic text.
"""
import copy
from pptx import Presentation
from pptx.util import Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pathlib import Path

# ── Palette ──
DARK_BG   = RGBColor(0x2C, 0x3E, 0x50)  # dark charcoal
WARM_BG   = RGBColor(0xF5, 0xF0, 0xE8)  # warm off-white
ACCENT    = RGBColor(0xB8, 0x50, 0x42)  # terracotta
GOLD      = RGBColor(0xC9, 0x95, 0x3C)  # gold accent
WHITE     = RGBColor(0xFF, 0xFF, 0xFF)
DARK_TEXT  = RGBColor(0x2C, 0x3E, 0x50)
LIGHT_TEXT = RGBColor(0xF5, 0xF0, 0xE8)
LIGHT_ROW = RGBColor(0xEE, 0xE8, 0xDC)  # alternating table row

# ── Helpers ──

def recolor_shape_text(shape, color):
    if not shape.has_text_frame:
        return
    for para in shape.text_frame.paragraphs:
        for run in para.runs:
            run.font.color.rgb = color

def style_shape_bg(shape, color):
    shape.fill.solid()
    shape.fill.fore_color.rgb = color

def style_table(table, accent=ACCENT, alt_row=LIGHT_ROW):
    """Style table: accent header, alternating rows, thin borders."""
    # Header row
    for cell in table.rows[0].cells:
        cell.fill.solid()
        cell.fill.fore_color.rgb = accent
        for para in cell.text_frame.paragraphs:
            para.alignment = PP_ALIGN.LEFT
            for run in para.runs:
                run.font.color.rgb = WHITE
                run.font.bold = True
                run.font.size = Pt(11)
                run.font.name = "Calibri"

    # Data rows
    for r_idx, row in enumerate(table.rows):
        if r_idx == 0:
            continue
        bg = alt_row if r_idx % 2 == 1 else WARM_BG
        for cell in row.cells:
            cell.fill.solid()
            cell.fill.fore_color.rgb = bg
            for para in cell.text_frame.paragraphs:
                for run in para.runs:
                    run.font.color.rgb = DARK_TEXT
                    run.font.size = Pt(10)
                    run.font.name = "Calibri"

    # Thin borders via XML (on every cell)
    from pptx.oxml.ns import qn
    for row in table.rows:
        for cell_obj in row.cells:
            tcPr = cell_obj._tc.get_or_add_tcPr()
            # Remove existing borders
            for tag in ['a:lnL', 'a:lnR', 'a:lnT', 'a:lnB']:
                for el in tcPr.findall(qn(tag)):
                    tcPr.remove(el)
            # Add thin light-gray line on each side
            ln = tcPr.makeelement(qn('a:lnL'), {
                'w': '6350', 'cap': 'flat', 'cmpd': 'sng'
            })
            solid = ln.makeelement(qn('a:solidFill'), {})
            clr = ln.makeelement(qn('a:srgbClr'), {'val': 'D5CCC0'})
            solid.append(clr)
            ln.append(solid)
            tcPr.append(ln)
            # Copy to other 3 sides
            for side in ['a:lnR', 'a:lnT', 'a:lnB']:
                el = copy.deepcopy(ln)
                el.tag = qn(side)
                tcPr.append(el)

# ── Slide type detection ──

def is_title_or_end(slide):
    """Detect hero title/end slides by text content."""
    texts = []
    for s in slide.shapes:
        if s.has_text_frame:
            for p in s.text_frame.paragraphs:
                t = p.text.strip()
                if t:
                    texts.append(t)
    full = " ".join(texts)
    if any(x in full for x in ["END OF VISUALIZATION", "Interior 3D Views",
                                "Exhibition Design"]):
        return True
    if len(texts) >= 2 and "متحف" in texts[0] \
       and ("MUSEUM" in texts[1] or "Museum" in texts[1]):
        return True
    return False

def is_view_slide(slide):
    """Slide with a large image (3D render) and no table."""
    has_large_img = False
    has_table = False
    for s in slide.shapes:
        if s.shape_type == 13 and s.width > Emu(6000000):
            has_large_img = True
        if s.has_table:
            has_table = True
    return has_large_img and not has_table

# ── Main ──

SRC = Path("input.pptx")
DST = Path("output_redesigned.pptx")
import shutil
shutil.copy2(SRC, SRC.with_suffix('.pptx.bak'))

prs = Presentation(str(SRC))

for idx, slide in enumerate(prs.slides):

    # Background
    bg = slide.background.fill
    if is_title_or_end(slide):
        bg.solid()
        bg.fore_color.rgb = DARK_BG
    else:
        bg.solid()
        bg.fore_color.rgb = WARM_BG

    for shape in slide.shapes:

        # ── Skip images and pictures ──
        if shape.shape_type == 13:
            continue  # leave pictures untouched

        # ── Shape (rectangle, text box) ──
        if shape.shape_type == 1:
            # Header bar: top of slide, full width
            if shape.top < Emu(200000) and shape.width > Emu(10000000):
                style_shape_bg(shape, ACCENT)
                recolor_shape_text(shape, WHITE)
                for para in shape.text_frame.paragraphs:
                    for run in para.runs:
                        run.font.bold = True
                        run.font.size = Pt(11)
                        run.font.name = "Calibri"

            # Footer bar: bottom of slide
            elif shape.top > Emu(5800000) and shape.width > Emu(10000000):
                style_shape_bg(shape, DARK_BG)
                recolor_shape_text(shape, LIGHT_TEXT)
                for para in shape.text_frame.paragraphs:
                    for run in para.runs:
                        run.font.size = Pt(11)
                        run.font.name = "Calibri"

            # Title/end slide text
            elif is_title_or_end(slide):
                recolor_shape_text(shape, WHITE)

        # ── Tables ──
        if shape.has_table:
            style_table(shape.table)

prs.save(str(DST))
print(f"Saved: {DST}")
```

## Verification After Restyle

```python
from pptx import Presentation
prs = Presentation("output_redesigned.pptx")

checks = {'pass': 0, 'fail': 0}
for i, slide in enumerate(prs.slides):
    bg = str(slide.background.fill.fore_color.rgb)

    # Check table headers
    for s in slide.shapes:
        if s.has_table:
            hdr = str(s.table.rows[0].cells[0].fill.fore_color.rgb)
            ok = hdr == 'B85042'
            checks['pass' if ok else 'fail'] += 1
            break

print(f"{checks['pass']} passed, {checks['fail']} failed")
```

## When to Use This Pattern vs Template Editing

| Situation | Approach |
|---|---|
| Restyle existing 20-50 slide deck | python-pptx restyle (this pattern) |
| Create new deck from brand template | `editing.md` + template approach |
| Create new deck from scratch | `pptxgenjs.md` |
| Add/remove slides or reorder | Manual or python-pptx slide ops |

## Known Pitfalls

- **`cell.fill.fore_color.rgb` raises error if no fill exists** — always call `cell.fill.solid()` first
- **`tbl.iter_tcells()` doesn't exist in python-pptx 1.0.2** — use `row.cells` iteration instead
- **Paragraphs have no `font_size` attribute** — check `run.font.size` on individual runs
- **Shape detection by position** — EMU values are specific to 16:9 widescreen (12192000 x 6858000). For 4:3 (9144000 x 6858000), adjust pixel thresholds.
- **soffice not available** — LibreOffice may not be installed. Verify with `python-pptx` read-back instead.
