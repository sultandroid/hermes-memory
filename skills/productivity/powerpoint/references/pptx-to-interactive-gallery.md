# PPTX → Interactive HTML Gallery Pipeline

## When to use

You have a PowerPoint deck with 3D rendered view slides containing callout annotations (labels with connector lines pointing to specific elements in the image). You want to convert these into an interactive HTML gallery where:
- Each render is a clickable/hoverable image
- Callout labels become interactive hotspots showing material details on hover
- Schedule tables from the deck are preserved as expandable content

## The Pipeline

### Step 1: Extract images from PPTX slides

Use python-pptx to extract picture shapes from each slide:

```python
from pptx import Presentation
from pptx.enum.shapes import MSO_SHAPE_TYPE
from PIL import Image
import io

prs = Presentation("deck.pptx")
for i, slide in enumerate(prs.slides):
    for j, shape in enumerate(slide.shapes):
        if shape.shape_type == MSO_SHAPE_TYPE.PICTURE:
            img = shape.image
            ext = img.content_type.split('/')[-1]
            with open(f"slide{i+1:02d}_img{j+1:02d}.{ext}", "wb") as f:
                f.write(img.blob)
```

### Step 2: Composite annotated renders (bake callouts into images)

Callout text and connector lines are separate AUTO_SHAPE objects in the PPTX. To produce a single image with labels baked in, overlay them using Pillow:

```python
from PIL import Image, ImageDraw

# Get main image bounds (EMU units)
img_left = main_img_shape.left
img_top = main_img_shape.top
img_w_emu = main_img_shape.width
img_h_emu = main_img_shape.height

# Extract callout text from AUTO_SHAPE objects
callouts = []
for s in slide.shapes:
    if s == main_img_shape: continue
    if not s.has_text_frame: continue
    t = s.text_frame.paragraphs[0].text.strip()
    # Filter to annotation-like text codes
    if re.match(r'^[A-Za-z0-9_\.\s\-–\(\)/]{3,60}$', t):
        # Map EMU to pixel coords
        rel_x = (s.left + s.width/2 - img_left) / img_w_emu
        rel_y = (s.top + s.height/2 - img_top) / img_h_emu
        px = int(rel_x * img_pixel_width)
        py = int(rel_y * img_pixel_height)
        callouts.append((px, py, t))
```

**Key coordinate mapping:**
- PPTX positions are in **EMU** (English Metric Units): 1 inch = 914,400 EMU
- To map: `pixel = (shape_center_emu - image_origin_emu) / image_dimension_emu * image_pixel_dimension`
- Always use relative position (ratio), not absolute pixels, for responsiveness

### Step 3: Schedule table data extraction

Read Excel schedule files to get enriched material data:

```python
import openpyxl
data = {}
for row in ws.iter_rows(min_row=header_row, values_only=True):
    code = str(row[0]).strip()
    data[code] = {
        "description": row[2],
        "finish": row[3],
        "colour": row[4],
        "supplier": row[5],
    }
```

### Step 4: Build interactive HTML with hotspots

Three approaches for making renders interactive, in order of preference:

**A. Percentage-based overlays (recommended, responsive)**
- Position hotspot divs using percentage values (not absolute px)
- The overlay container is `position:absolute; top:0; left:0; width:100%; height:100%`
- Each hotspot: `left: {rel_x * 100}%; top: {rel_y * 100}%`
- Works with any image display size

**B. Image maps (`<map>` + `<area>`)**
- Use `coords` with percentage-based or fixed coordinates
- Good for irregular polygon shapes
- Less flexible for hover effects

**C. CSS `background-position` on the image container**
- Set the render as `background-image` on a div
- Position hotspot elements using absolute positioning relative to the container
- Requires fixed aspect-ratio container

### Step 5: Tooltip with material data

```javascript
// Embed material data as JSON in a <script> tag
const MATERIAL_DATA = {"FI_FL_01": {"Material":"60x60cm Bits&Pieces","Finish":"Antislip","Colour":"Steel Grain Quad","Supplier":"Ceramiche Piemme"}};

// On hotspot hover
document.querySelectorAll('.hotspot').forEach(el => {
  el.addEventListener('mouseenter', e => {
    const code = el.dataset.code;
    const info = MATERIAL_DATA[code];
    // Show tooltip with formatted data
  });
});
```

## Known Pitfalls

### Absolute pixel coordinates break on responsive images
If you compute hotspot positions at a fixed resolution (e.g., 1600px wide), they'll be misaligned when the image renders at a different size on mobile/tablet. Always use percentage-based positioning.

### Filter: brightness(0) invert(1) destroys brand logos
Samaya style guide logos should keep their original colors. Never apply color inversion filters to client/PMC/contractor logos.

### PPTX image extraction may yield low-resolution thumbnails
Some PPTX files store compressed/preview versions of images. If resolution is insufficient, request the original high-res renders separately.

### Slide number mismatch between python-pptx and display
`python-pptx` uses 0-based indexing. The slide number shown in PowerPoint is 1-based. Always verify by checking slide text content rather than assuming slide_index + 1 = display number.

### Callout text detection is heuristic
Not every AUTO_SHAPE with text is a callout label. Filter by:
- Length: 3-60 chars
- Pattern: codes with underscores, dots, slashes, or hyphens
- Position: must overlap the image bounds
- Exclude title/header text (check position near top of slide)
