# PPTX Hotspot Extraction → Interactive 3D Render Viewer

Extract callout annotations from PowerPoint slides and build an interactive material-review web app with proximity-based hotspot pins and hover tooltips.

## When to Use

A client/consultant has a PowerPoint presentation with 3D rendered views and manual callout labels (material codes) on each image. You need to turn this into an interactive web app where:
- Each render shows tiny numbered gold pins at every material location
- Hovering near a pin reveals a rich tooltip card with full material specs
- Positions exactly match the PPTX callouts (not hand-placed)

## Extraction Pipeline

### 1. Scan the PPTX

```python
from pptx import Presentation
from pptx.enum.shapes import MSO_SHAPE_TYPE

prs = Presentation("path/to/deck.pptx")
for i, slide in enumerate(prs.slides):
    texts = [s.text_frame.text.strip() for s in slide.shapes if s.has_text_frame and s.text_frame.text.strip()]
    has_img = any(s.shape_type == MSO_SHAPE_TYPE.PICTURE for s in slide.shapes)
    print(f"Slide {i+1}: {texts[0] if texts else '(no text)'} [IMG={has_img}]")
```

### 2. Filter for View Slides Only

Identify slides that contain a large 3D render image. Skip title slides, schedule tables, and end slides. Group by gallery code (e.g., G4, G6, G8).

### 3. Extract Callout Positions

Material codes in PPTX callouts follow patterns like `FI_FL_01`, `06.03_SW_04`, `LB3.01_SW_01`. Section titles (ARCHAEOLOGY, FLOWERSMEN) should be filtered out.

```python
import re
slide_w = prs.slide_width  # EMU
slide_h = prs.slide_height

hotspots = []
for shape in slide.shapes:
    if shape.has_text_frame:
        text = shape.text_frame.text.strip()
        # Material code pattern: alphanumeric with underscores/dots, 3-20 chars
        if re.match(r'^[A-Z0-9._]{3,20}$', text) and not re.match(r'^(G4|G6|G8|G9|G11|G12|G5|LB3)$', text):
            x_pct = round((shape.left / slide_w) * 100, 1)
            y_pct = round((shape.top / slide_h) * 100, 1)
            if 0 <= x_pct <= 100 and 0 <= y_pct <= 100:  # clamp to image bounds
                hotspots.append({'code': text, 'x': x_pct, 'y': y_pct})
```

### 4. Extract & Optimize Images

Pull the largest image from each view slide and resize for web:

```python
from PIL import Image
import io

for shape in slide.shapes:
    if shape.shape_type == MSO_SHAPE_TYPE.PICTURE:
        img = Image.open(io.BytesIO(shape.image.blob))
        if img.mode == 'RGBA': img = img.convert('RGB')
        if img.width > 1600:
            ratio = 1600 / img.width
            img = img.resize((1600, int(img.height * ratio)), Image.LANCZOS)
        img.save(f'/public/images/{filename}.jpg', 'JPEG', quality=85)
```

### 5. Build Hotspot Positions as Percentage Coords

Store as `{code, x (0-100), y (0-100)}` — percentage coordinates mean pins work at any zoom/responsive size.

## UI Pattern — Proximity Hotspot Pins

### Pin Design (CSS)

```css
.hotspot-pin-modal {
  position: absolute; width: 14px; height: 14px; border-radius: 50%;
  background: #C4754A;  /* gold */
  opacity: 1;  /* always visible */
  box-shadow: 0 0 0 4px rgba(255,255,255,.2), 0 0 0 7px rgba(196,117,74,.2), 0 0 20px rgba(196,117,74,.3);
  z-index: 10;
}
.hotspot-pin-modal.active {
  width: 20px; height: 20px;
  box-shadow: 0 0 0 4px rgba(255,255,255,.4), 0 0 0 8px rgba(196,117,74,.3), 0 0 0 14px rgba(196,117,74,.1);
}
```

Pin features:
- **14px gold dot** with white inner ring for contrast on any image background
- **Multi-ring glow** — visible even on bright image areas
- **Numbered badge** (1–N) above each pin in dark glassmorphism label
- Active state (cursor proximity <10%) grows to **20px with expanded glow**

### Proximity Detection (React/TS)

```typescript
const handleMouseMove = (e: React.MouseEvent) => {
  const rect = img.getBoundingClientRect();
  const mx = ((e.clientX - rect.left) / rect.width) * 100;
  const my = ((e.clientY - rect.top) / rect.height) * 100;

  let closestIdx = -1;
  let minDist = Infinity;
  hotspots.forEach((hs, i) => {
    const d = Math.sqrt((mx - hs.x)**2 + (my - hs.y)**2);
    if (d < minDist) { minDist = d; closestIdx = i; }
  });

  setActivePin(closestIdx >= 0 && minDist <= 10 ? closestIdx : -1);
  // Show tooltip only within 5% proximity
  if (closestIdx >= 0 && minDist <= 5) { setTooltip(...); }
};
```

Key thresholds:
- **Within 12%**: pin becomes active (grows, glows) — user notices something is there
- **Within 5%**: tooltip card appears with full material data
- **Within 6% click**: pin selects and opens sidecar/sidebar (for mobile tap)

### Tooltip Card Design

Dark glassmorphism card with backdrop blur:

```css
.hotspot-tooltip-card {
  position: fixed; z-index: 210; width: 300px; pointer-events: none;
  background: rgba(10,8,6,.92); backdrop-filter: blur(20px);
  border: 1px solid rgba(196,117,74,.2); border-radius: 12px;
  padding: 16px 18px;
  box-shadow: 0 8px 40px rgba(0,0,0,.6), 0 0 30px rgba(196,117,74,.05);
}
```

Content structure:
```
┌─────────────────────────────┐
│ FI_FL_01                    │  ← code (monospace, gold, uppercase)
│ 60x60cm Bits&Pieces...      │  ← name (serif, white, 15px)
│ [Flooring]                  │  ← category badge (pill, muted)
│                             │
│ Finish │ Antislip           │  ← meta grid (2 columns)
│ Colour │ Steel Grain Quad   │
│ Supplier│ Ceramiche Piemme  │
└─────────────────────────────┘
```

### Numbered Badge

```
.hotspot-label-badge {
  position: absolute; pointer-events: none;
  transform: translate(-50%, calc(-50% - 18px));
  font-family: 'IBM Plex Mono', monospace;
  font-size: 9px; color: #fff;
  background: rgba(10,8,6,.8); backdrop-filter: blur(4px);
  padding: 2px 6px; border-radius: 3px;
  border: 1px solid rgba(196,117,74,.3);
}
```

### Gallery Card Grid

Each gallery card shows the first view's thumbnail with metadata:
- Title + view count + total materials count
- Click → opens modal with full image, pins, view selector, and sidebar

### View Navigation

Within the modal:
- **Prev/Next arrows** (‹ ›) on left/right sides
- **Numbered view buttons** (1, 2, 3...) at top of sidebar
- **Collapsible sidebar** with material list for current view
- Hovering a sidebar item highlights the corresponding pin on the image

## Material Data Lookup

Join hotspot codes against a materials database (`materials.json` or similar):

```typescript
const matMap = new Map(materials.map(m => [m.code, m]));
// In tooltip:
const mat = matMap.get(hs.code) || {};
const name = mat.description || hs.code;
const category = mat.category || '';
// ... render fields
```

Material fields typically available:
- `code` — e.g., FI_FL_01, 06.03_SW_04
- `description` — what the material is
- `category` — Flooring, Walls, Ceilings, Setwork, Showcase
- `finish` — Antislip, Matt emulsion, Polished
- `colour` — RAL code + name
- `supplier` — Manufacturer/vendor
- `element` — Where it's used (Walls, Flooring, Reception)

## Known Pitfalls

1. **Section titles in PPTX callouts** — words like "ARCHAEOLOGY", "FLOWERSMEN", "SCRIPTS" appear as text shapes but are NOT material codes. Filter them out with a regex that requires at least one `_` or `.` and only alphanumeric chars.

2. **Callout positions outside image bounds** — Some callouts have negative `left`/`top` values (e.g., -5.0%) or >100% because they extend past the image edge. Clamp or skip with `if 0 <= x <= 100`.

3. **Images differ between PPTX and app** — If the Kimi/Claude app uses different placeholder images than the PPTX renders, you MUST extract the real images from the PPTX and replace them. Match images by slide number, not filename.

4. **Material code normalization** — Codes like `F1_WA_08` (letter O vs number 0) may differ between PPTX and materials database. Handle both variants.

5. **App uses different images** — The Kimi app may ship with placeholder JPGs. Extract real 1600px renders from the PPTX and overwrite the placeholder files.

6. **Build check after data update** — Always run `npm run build` (or equivalent) after replacing gallery data. TypeScript strict mode may flag unused variables in `.map()` callbacks or incorrect type narrowing.
