# PPTX → HTML Gallery Conversion

Convert a PowerPoint presentation (with 3D renders, schedule tables, bilingual content, and reference photos) into a single self-contained HTML page with image galleries.

## When to Use

- User has a `.pptx` deck with embedded images (3D renders, product photos) and tabular data
- The deck needs to be shared as a web page (not as a downloadable file)
- The content includes schedules, comparison tables, and gallery-style image sections
- Target audience prefers browser viewing over PowerPoint

## Workflow

### Phase 1: Extract Content

```bash
# Extract text structure
python3 -c "
from pptx import Presentation
prs = Presentation('deck.pptx')
print(f'Slides: {len(prs.slides)}')
for i, slide in enumerate(prs.slides):
    print(f'--- Slide {i+1} ---')
    for s in slide.shapes:
        if s.has_text_frame and s.text.strip():
            print(f'  {s.text[:200]}')
        if s.has_table:
            t = s.table
            for r_idx in range(len(t.rows)):
                cells = [t.cell(r_idx, c).text.strip() for c in range(len(t.columns))]
                print(f'  TABLE ROW: {cells}')
"

# Extract all embedded images
python3 -c "
from pptx import Presentation
from pptx.enum.shapes import MSO_SHAPE_TYPE
import os
prs = Presentation('deck.pptx')
os.makedirs('images', exist_ok=True)
for i, slide in enumerate(prs.slides):
    for j, shape in enumerate(slide.shapes):
        if shape.shape_type == MSO_SHAPE_TYPE.PICTURE:
            img = shape.image
            ext = img.content_type.split('/')[-1]
            if ext == 'jpeg': ext = 'jpg'
            fname = f'slide{i+1:02d}_img{j+1:02d}.{ext}'
            with open(f'images/{fname}', 'wb') as f:
                f.write(img.blob)
"
```

### Phase 2: Map Gallery Sections to Images

Use python-pptx to identify which slide belongs to which gallery section by scanning text labels:

```python
for idx, slide in enumerate(prs.slides):
    for s in slide.shapes:
        if s.has_text_frame:
            for p in s.text_frame.paragraphs:
                t = p.text.strip()
                # Gallery codes: G4, G6, G8, G9, G11, G12, G5, LB3 etc.
                if t in ['G4','G5','G6','G8','G9','G11','G12','G13','G14','LB2','LB3']:
                    gallery_code = t
```

Render images (large JPEGs, 3-5MB each) are on "view" slides. Reference images (smaller PNGs, <500KB) are on schedule/table slides.

### Phase 3: Optimize Images for Web

PPTX embeds full-resolution images. 3D renders are typically 4-5MB each — must be resized:

```python
from PIL import Image

img = Image.open(src_path)
if img.mode in ('RGBA', 'P') and ext == '.jpg':
    img = img.convert('RGB')

w, h = img.size
if w > 1400:  # max width for web
    ratio = 1400 / w
    new_h = int(h * ratio)
    img = img.resize((1400, new_h), Image.LANCZOS)

if ext == '.jpg':
    img.save(dst_path, 'JPEG', quality=82, optimize=True)
else:
    img.save(dst_path, 'PNG', optimize=True)
```

**Results:** 4-5MB renders → 70-150KB (97-98% reduction). Reference PNGs → minor reduction.

### Phase 4: Build HTML Page

Delegate HTML generation to a subagent (delegate_task with toolsets=["terminal","file"]) with complete data specification. The prompt must include:

1. **Every table row** with exact values (codes, descriptions, references, evaluations)
2. **Every pricing cell** with exact SAR amounts
3. **Arabic text** to preserve verbatim
4. **Design spec** (color palette, typography, layout)

**Design spec for museum/cultural projects:**

```
Color Palette:
- Primary bg: #0F1923 (very dark navy)
- Surface/cards: #FFFFFF, section alt: #F7F3EE (warm light)
- Accent: #B85042 (terracotta)
- Gold accent: #C9953C
- Text: #1A1A2E body, #FFFFFF on dark
- "Comply" badge: #2D8A4E green

Typography: Inter (body) + Playfair Display (headings) via Google Fonts

Layout:
- Sticky vertical sidebar TOC with Intersection Observer active highlighting
- Expandable/collapsible gallery schedule sections
- Horizontal scroll for comparison tables
- Recommendation box: accent left border, subtle shadow
- Print-ready (@page A4, 15mm margins)
- Dark hero for title + end sections, light warm for content
```

### Phase 5: Inject Images into HTML

After the subagent generates the HTML, inject image galleries:

```python
gallery_html = """
<div class="section-gallery" id="g4-gallery">
  <div class="gallery-row">
    <div class="gallery-item">
      <a href="images/slide03_img06.jpg" target="_blank">
        <img src="images/slide03_img06.jpg" alt="View 1 – G4 Saudi Art" loading="lazy">
      </a>
      <div class="gallery-caption">View 1 – G4 Saudi Art</div>
    </div>
    ...
  </div>
</div>
"""

# Inject after section-header, before section-card
header_end = html.find('<div class="section-card', section_start)
html = html[:header_end] + "\n" + gallery_html + html[header_end:]
```

Also inject gallery CSS (responsive grid, hover effect, print-hidden):

```css
.gallery-row{display:grid;grid-template-columns:repeat(auto-fill,minmax(320px,1fr));gap:16px}
.gallery-item{border-radius:8px;overflow:hidden;background:#fff;box-shadow:0 1px 4px rgba(0,0,0,.08)}
.gallery-item img{width:100%;height:200px;object-fit:cover;display:block}
.gallery-caption{padding:8px 12px;font-size:12px;color:#555;font-weight:500}
@media(max-width:768px){.gallery-row{grid-template-columns:1fr}}
@media print{.section-gallery{display:none!important}}
```

### Phase 6: Verify

Check for every data point:
```python
for keyword in ["Arabic title", "English title", "price values", "vendor emails", "gallery codes"]:
    assert keyword in html
```

Verify image count matches render count.

## Pitfalls

- **Slide numbers in HTML index may not match PPTX slide indexes.** The user's PPTX can have schedules interleaved with views. Always check actual gallery codes via python-pptx text scanning, not assumed slide ranges.
- **Image modes:** PPTX images can be RGBA PNG. Convert to RGB before saving as JPEG or the thumbnail is black.
- **Arabic text:** Preserve `dir="auto"` on all Arabic spans. Do NOT retype — extract and inject verbatim.
- **Image paths:** Use relative paths (`images/...`) so the HTML works when served from any directory.
- **Callout labels in PPTX must be composited into images — do NOT skip them.** The user's annotations (FI_FL_01, 05.02_SW_03, etc.) are information-carrying FF&E codes. Extract and bake them into renders using `python-pptx` + `Pillow` compositing. See the dedicated guide: `references/pptx-image-annotation-compositing.md`.
- **Schedule reference photos:** PPTX has small PNGs in schedule slides. These are hard to map to specific table rows without XML analysis. Skip them unless the user specifically asks — the 3D renders (with annotations) are the primary value.
