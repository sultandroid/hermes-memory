# PPTX Image Extraction with Callout Annotation Compositing

Extract slide images from a `.pptx` and **bake callout annotations (code labels, bent-line connectors) into the image pixels**. The callouts are separate PPTX shapes — extracting only the image blob loses them.

## When to Use

- User wants extracted renders/photos WITH their PPTX label overlays (FI_FL_01, 05.02_SW_03, G6_SW_01, etc.)
- Converting a deck to HTML and the annotations are information-carrying (FF&E codes, material references)
- You cannot use LibreOffice (`soffice`) to render slides to images

## The Problem

PPTX stores images as raw blobs and callout labels as separate shapes (AUTO_SHAPE with text). Extracting `shape.image.blob` gives the bare render with no annotations. The user expects the annotated view they see in PowerPoint.

## The Solution

Use **python-pptx + Pillow** to composite: extract the image, read callout shape positions (in EMU), map to pixel coordinates, overlay text labels as semi-transparent badges.

## Full Compositing Script

```python
import io, os, re
from pptx import Presentation
from pptx.util import Emu
from pptx.enum.shapes import MSO_SHAPE_TYPE
from PIL import Image, ImageDraw, ImageFont

prs = Presentation("source.pptx")

def extract_image_from_shape(shape):
    """Extract PIL Image from picture shape."""
    img = shape.image
    return Image.open(io.BytesIO(img.blob))

def is_callout_text(shape):
    """True if shape has a short annotation code (e.g. FI_FL_01)."""
    if not shape.has_text_frame:
        return False
    t = shape.text_frame.paragraphs[0].text.strip() if shape.text_frame.paragraphs else ""
    if not t or len(t) < 3 or len(t) > 60:
        return False
    if re.match(r'^[A-Za-z0-9_\.\s\-–\(\)/]{3,60}$', t):
        return True
    return False

for slide_idx in range(len(prs.slides)):
    slide = prs.slides[slide_idx]

    # Find the main image (largest picture shape)
    main_img_shape = None
    for s in slide.shapes:
        if s.shape_type == MSO_SHAPE_TYPE.PICTURE:
            if main_img_shape is None or (s.width * s.height > main_img_shape.width * main_img_shape.height):
                main_img_shape = s

    if main_img_shape is None:
        continue  # no image on this slide

    bg = extract_image_from_shape(main_img_shape)
    bg_w, bg_h = bg.size

    # Scale to target width (e.g. 1600px)
    OUTPUT_W = 1600
    scale = OUTPUT_W / bg_w
    out_h = int(bg_h * scale)
    bg_resized = bg.resize((OUTPUT_W, out_h), Image.LANCZOS)
    draw = ImageDraw.Draw(bg_resized, 'RGBA')

    # Image position on slide (in EMU)
    img_left = main_img_shape.left
    img_top = main_img_shape.top
    img_w_emu = main_img_shape.width
    img_h_emu = main_img_shape.height

    def emu_to_img(emu_x, emu_y):
        """Convert slide EMU to image pixel coordinates."""
        rel_x = (emu_x - img_left) / img_w_emu
        rel_y = (emu_y - img_top) / img_h_emu
        return (int(rel_x * bg_w * scale), int(rel_y * bg_h * scale))

    # Collect callout labels
    callouts = []
    for s in slide.shapes:
        if s == main_img_shape:
            continue
        if is_callout_text(s):
            text = s.text_frame.paragraphs[0].text.strip()
            cx, cy = emu_to_img(s.left + s.width//2, s.top + s.height//2)
            callouts.append((cx, cy, text))

    # Load font
    font = ImageFont.load_default()
    for fp in ["/System/Library/Fonts/Helvetica.ttc",
               "/System/Library/Fonts/HelveticaNeue.ttc"]:
        if os.path.exists(fp):
            try:
                font = ImageFont.truetype(fp, 13)
                break
            except:
                pass

    # Draw each callout
    for cx, cy, text in callouts:
        # Red dot at anchor
        r = 4
        draw.ellipse([cx - r, cy - r, cx + r, cy + r],
                     fill=(200, 80, 60, 220))

        label = text.split('\n')[0][:35]
        bbox = draw.textbbox((0, 0), label, font=font)
        tw = bbox[2] - bbox[0]
        th = bbox[3] - bbox[1]
        pad = 4

        # Position label next to anchor (right, then fallback left/up/down)
        lx = cx + 8
        ly = cy - th//2 - pad
        if lx + tw + pad*2 > OUTPUT_W:
            lx = cx - tw - pad*2 - 8
        if ly < 0:
            ly = cy + 8
        if ly + th + pad*2 > out_h:
            ly = cy - th - pad*2 - 8

        # Semi-transparent white background + border
        draw.rectangle([lx, ly, lx + tw + pad*2, ly + th + pad*2],
                       fill=(255, 255, 255, 220))
        draw.rectangle([lx, ly, lx + tw + pad*2, ly + th + pad*2],
                       outline=(200, 80, 60, 180), width=1)
        draw.text((lx + pad, ly + pad), label,
                  fill=(40, 40, 40, 255), font=font)

    # Save
    bg_resized.save(f"slide{slide_idx+1:02d}_annotated.jpg",
                    "JPEG", quality=88)
```

## Key Concepts

### Coordinate Mapping

PPTX positions everything in **EMU (English Metric Units)**:
- 1 inch = 914,400 EMU
- 1 pt = 12,700 EMU
- Widescreen slide: 12,192,000 x 6,858,000 EMU

The image on the slide occupies a rectangle `(left, top, width, height)` in EMU. A callout shape at `(cx_emu, cy_emu)` maps to image pixels:

```python
rel_x = (cx_emu - img_left_emu) / img_width_emu   # 0.0 to 1.0
pixel_x = rel_x * image_pixel_width
```

### Callout Detection

The heuristic `re.match(r'^[A-Za-z0-9_\.\s\-–\(\)/]{3,60}$')` catches FF&E codes like:
- `FI_FL_01`, `FI_CL_01`, `FI_WA_01`, `FI_ME_01` (finish codes)
- `05.02_SW_03`, `G6_SW_01`, `G8_SW_02` (setwork codes)
- `G9.01_SC_01`, `G12.01_SC_04` (showcase codes)
- `LB3_SW_04A-E (LB3_WF_04A-E)` (multi-code labels)

It excludes long sentences, URLs, and shape labels like "Lightbox" that aren't reference codes.

### Label Positioning

The label badge appears near the anchor point with a small connector dot:
1. Red dot at the text box center
2. White semi-transparent label offset to the right
3. Falls back to left/above/below if out of bounds
4. Terracotta border to match the design palette

## Results

| Metric | Before | After |
|--------|--------|-------|
| 3D render size | 4-5 MB | 150-250 KB (88% JPEG) |
| Annotations | Lost (bare image) | Baked in at correct positions |
| Labels per slide | — | 6-11 annotation codes |

## When NOT to Use

- The user only needs raw images (for further processing, not presentation)
- Callout labels are decorative/design elements, not information-carrying codes
- LibreOffice is available — `soffice --headless --convert-to pdf` + `pdftoppm` renders the slide with all shapes intact (much simpler)
