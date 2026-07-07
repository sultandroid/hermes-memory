# PPTX Callout Positions → Interactive HTML Hotspots

Extract annotation positions from PPTX callout shapes and create hoverable HTML pin overlays on rendered images, linked to enriched material data from Excel schedules.

## When to Use

- You rendered PPTX slides to images WITH callout annotations baked in
- User wants to hover over materials/objects in the rendered photo and see full material details
- You have source Excel schedule files with enriched descriptions, finishes, colours, suppliers
- Target: a single self-contained interactive HTML page

## Key Design Decision: Percentage-Based Positioning

**CRITICAL: Always use PERCENTAGE coordinates (`left:XX%`, `top:YY%`) for hotspot positions, not absolute pixels.**

Absolute pixel positions (`left:320px;top:180px`) break on responsive layouts where the image is displayed at different sizes (mobile, tablet, zoom). Percentage coordinates are relative to the parent `.gallery-item` container and automatically scale.

```python
# ✅ CORRECT — percentage-based
pct_x = (callout_center_x_emu - image_left_emu) / image_width_emu * 100
pct_y = (callout_center_y_emu - image_top_emu) / image_height_emu * 100
# HTML: style="left:42.5%;top:31.8%"

# ❌ WRONG — pixel-based (breaks on responsive)
pixel_x = pct_x / 100 * 1600  # fixed to 1600px image width
# HTML: style="left:680px;top:286px"
```

## Workflow

### Phase 1: Extract Callout Positions (Percentage-Based)

```python
import re, json
from pptx import Presentation
from pptx.enum.shapes import MSO_SHAPE_TYPE

prs = Presentation("source.pptx")

for slide_idx in range(len(prs.slides)):
    slide = prs.slides[slide_idx]

    # Find the main image shape (largest PICTURE)
    main_img = None
    for s in slide.shapes:
        if s.shape_type == MSO_SHAPE_TYPE.PICTURE:
            if main_img is None or (s.width * s.height > main_img.width * main_img.height):
                main_img = s
    if not main_img:
        continue

    spots = []
    for s in slide.shapes:
        if s == main_img or not s.has_text_frame:
            continue
        t = s.text_frame.paragraphs[0].text.strip() if s.text_frame.paragraphs else ""
        if not t or len(t) < 3 or len(t) > 60:
            continue
        if not re.match(r'^[A-Za-z0-9_\.\s\-–\(\)/]{3,60}$', t):
            continue  # skip non-code text

        # Percentage of image dimensions
        pct_x = (s.left + s.width/2 - main_img.left) / main_img.width * 100
        pct_y = (s.top + s.height/2 - main_img.top) / main_img.height * 100

        if pct_x < -5 or pct_x > 105 or pct_y < -5 or pct_y > 105:
            continue  # outside image

        spots.append({
            "code": t.split('\n')[0].strip(),
            "x": round(pct_x, 1),
            "y": round(pct_y, 1),
        })
```

### Phase 2: Extract Material Data from Schedule Excel Files

Use openpyxl to read source schedule files. The Finishes Schedule typically has a header row around row 6-7:

```python
import openpyxl

data = {}

# Finishes Schedule — codes start with FI_
wb = openpyxl.load_workbook("6930_Finishes_Schedule_rev A.xlsx", data_only=True)
for row in wb.active.iter_rows(min_row=7, values_only=True):
    code = str(row[0] or "").strip()
    if not code.startswith("FI_"):
        continue
    data[code] = {
        "Component": str(row[1] or "").strip(),
        "Material": str(row[2] or "").strip(),
        "Finish": str(row[3] or "").strip(),
        "Colour": str(row[4] or "").strip(),
        "Supplier": str(row[5] or "").strip(),
    }

# Setwork Schedule — codes contain _SW_ or _WF_
# Scan for header row containing "Setwork ID"
wb = openpyxl.load_workbook("6930_Aseer_Setwork Schedule_rev A.xlsx", data_only=True)
header_row = None
for r_idx, row in enumerate(wb.active.iter_rows(max_row=20, values_only=True), 1):
    if any("Setwork ID" in str(v or "") for v in row):
        header_row = r_idx
        break
```

### Phase 3: Pin-Style HTML Overlay (GUI Indicator)

Instead of invisible hotspots (users don't know where to hover), use **small gold pulsing pin dots** that indicate interactability:

```html
<div class="gallery-item" onclick="openLightbox(...)">
  <img src="asm_views/render.jpg" alt="View" loading="lazy">
  <div class="pin-layer">
    <div class="pin" style="left:42.5%;top:31.8%" data-code="FI_FL_01">
      <div class="pin-ring"></div>
      <div class="pin-dot"></div>
    </div>
  </div>
  <div class="gallery-caption">View 1</div>
</div>
```

**CSS for pins:**
```css
.gallery-item{position:relative}
.pin-layer{position:absolute;top:0;left:0;width:100%;height:100%;z-index:3;pointer-events:none}
.pin{position:absolute;pointer-events:all;cursor:pointer;z-index:3}
.pin .pin-dot{width:10px;height:10px;border-radius:50%;background:#C9953C;border:2px solid rgba(255,255,255,.9);
  box-shadow:0 0 6px rgba(201,149,60,.5);transition:all .25s cubic-bezier(.22,1,.36,1);
  position:absolute;top:50%;left:50%;transform:translate(-50%,-50%)}
.pin:hover .pin-dot{width:14px;height:14px;box-shadow:0 0 12px rgba(201,149,60,.7);background:#fff;border-color:#C9953C}
.pin .pin-ring{position:absolute;top:50%;left:50%;width:24px;height:24px;border-radius:50%;
  border:1.5px solid rgba(201,149,60,.2);transform:translate(-50%,-50%);transition:all .3s;
  animation:pinPulse 3s ease-in-out infinite}
.pin:hover .pin-ring{width:36px;height:36px;border-color:rgba(201,149,60,.4)}
@keyframes pinPulse{0%,100%{opacity:1;transform:translate(-50%,-50%) scale(1)}50%{opacity:.5;transform:translate(-50%,-50%) scale(1.3)}}
@media print{.pin-layer{display:none!important}}
```

## ⚠️ Critical UX Rule: Hotspot Pins Only When Section Is Expanded

When gallery sections use an expand/collapse toggle (clickable header), the hotspot pins must only activate when the section is **expanded** and photos are visible. If pins respond to hover while the section is collapsed, users see invisible click targets floating over nothing.

**Implementation approaches (in priority order):**

### Approach A: Move images inside the collapsible container (preferred)

Put the `.section-gallery` div inside `.gallery-details` so it collapses/expands with the schedule table. This is the cleanest solution — when collapsed, pins simply don't exist in the DOM flow.

```html
<div class="gallery-header" onclick="toggleGallery(this)">
  <h3>G4 – Saudi Art</h3>
  <span class="expand-icon">▼</span>
</div>
<div class="gallery-details">
  <div class="gallery-details-inner">
    <div class="section-gallery">
      <!-- images + hotspot pins here -->
    </div>
    <table class="schedule-table">...</table>
  </div>
</div>
```

### Approach B: JS toggle (fallback)

Modify the `toggleGallery` function to also show/hide the `.section-gallery`:

```javascript
function toggleGallery(headerEl) {
  const details = headerEl.nextElementSibling;
  const isOpen = details.classList.contains('open');
  details.classList.toggle('open');
  headerEl.querySelector('.expand-icon').textContent = isOpen ? '▶' : '▼';
  // Hide/show gallery images when collapsing/expanding
  const section = headerEl.closest('.section');
  if (section) {
    const gallery = section.querySelector('.section-gallery');
    if (gallery) gallery.style.display = isOpen ? 'none' : '';
  }
}
```

**Pitfall:** `read_file(limit=500)` truncation + line-number contamination corrupted this file during a previous session. See the critical pitfall section below for recovery.

## Advanced Pattern: Proximity-Based Pin Reveal + Sidecar Panel

For high-end presentations (museum/architecture client reviews), use the **"Study Pin + Sidecar Detail Panel"** pattern:

### UX Design

| State | What happens |
|-------|-------------|
| **At rest** | Pristine 3D render — no visual clutter on the image |
| **Move cursor over image** | Gold pins fade in within 60px proximity of each hotspot |
| **Hover near a pin (≤30px)** | Floating tooltip card appears with material code, name, description |
| **Click a pin** | Sidecar panel slides in from right with full specification |
| **Sidecar content** | Code, Material, Component, Finish, Colour, Supplier, Description, Source Reference |
| **Close sidecar** | X button, click outside, or Escape key |
| **Clustering** | Pins within 80px of each other collapse into a single cluster dot showing count |

### CSS Pin States

```css
.hotspot-pin{position:absolute;pointer-events:all;width:6px;height:6px;border-radius:50%;
  background:#C9953C;opacity:0;transition:opacity .25s ease,transform .2s ease,box-shadow .2s ease;
  transform:translate(-50%,-50%);cursor:pointer;z-index:6;box-shadow:0 0 0 2px rgba(201,149,60,.2)}
.hotspot-pin.active{opacity:.85;width:10px;height:10px;
  box-shadow:0 0 0 4px rgba(201,149,60,.15),0 0 12px rgba(201,149,60,.2)}
.hotspot-pin.selected{opacity:1;width:14px;height:14px;
  box-shadow:0 0 0 8px rgba(201,149,60,.3),0 0 0 12px rgba(201,149,60,.1),0 0 30px rgba(201,149,60,.2)}
.hotspot-pin:hover{opacity:1!important;width:14px;height:14px;
  box-shadow:0 0 0 6px rgba(201,149,60,.25),0 0 20px rgba(201,149,60,.3)}
```

### Tooltip Card Design

Dark glassmorphism card with rich material details:

```css
.hotspot-tooltip-inner{background:rgba(10,15,26,.92);backdrop-filter:blur(20px);
  border:1px solid rgba(201,149,60,.2);border-radius:12px;padding:16px 18px;
  box-shadow:0 8px 40px rgba(0,0,0,.6),0 0 30px rgba(201,149,60,.05)}
.ht-code{color:#C9953C;font-weight:700;font-size:12px;letter-spacing:1.5px;text-transform:uppercase}
.ht-name{color:#fff;font-weight:600;font-size:15px;font-family:'Playfair Display',Georgia,serif}
.ht-category{display:inline-block;font-size:10px;color:rgba(255,255,255,.5);
  background:rgba(255,255,255,.06);padding:2px 8px;border-radius:10px}
.ht-meta{display:grid;grid-template-columns:1fr 1fr;gap:2px 12px;border-top:1px solid rgba(255,255,255,.06)}
```

### JavaScript Proximity Detection

```javascript
function handleImageMove(e, overlay) {
  var rect = overlay.getBoundingClientRect();
  var mx = e.clientX, my = e.clientY;
  var allPins = overlay.querySelectorAll('.hotspot-pin');
  var closestPin = null, closestDist = Infinity;

  allPins.forEach(function(pin) {
    // Pin position in viewport coordinates
    var pctX = parseFloat(pin.style.left);
    var pctY = parseFloat(pin.style.top);
    var pinLeft = rect.left + (pctX / 100) * rect.width;
    var pinTop = rect.top + (pctY / 100) * rect.height;
    var dx = mx - pinLeft, dy = my - pinTop;
    var dist = Math.sqrt(dx * dx + dy * dy);

    // Proximity: 60px radius → fade in, 30px → show tooltip
    if (dist <= 60) pin.classList.add('active');
    else pin.classList.remove('active');

    if (dist < closestDist) { closestDist = dist; closestPin = pin; }
  });

  if (closestPin && closestDist <= 30) showTooltip(closestPin, e);
  else hideTooltip();
}
```

### Clustering Algorithm

Cluster pins that are within 80px of each other (in viewport-pixel space). Use percentage coordinates for the cluster centroid so it scales properly:

```javascript
function buildClusters(pins) {
  // Group pins within 80px of each other using pairwise distance
  // Only cluster groups of 3+ pins -> show count dot at centroid
  // Cluster dot: terracotta bg (#B85042), shows count number
  // Clicking a cluster dot expands to show individual pins in that area
}
```

### ⚠️ Critical Pitfall: const in &lt;script&gt; Tags

When defining material data in a `<script>` tag and accessing it from another script:

```html
<script>const MATERIAL_DATA = {...};</script>  <!-- ❌ NOT on window -->
<script>
  // ❌ window.MATERIAL_DATA is undefined!
  // ❌ var MATERIAL_DATA = null shadows the global
  // ✅ Use window.MATERIAL_DATA = {...}
  // ✅ Access as window.MATERIAL_DATA from other scripts
</script>
```

**Rule:** `const` and `let` at the top level of a `<script>` tag do NOT create properties on `window`. Use `window.MATERIAL_DATA = {...}` explicitly for cross-script access.

## ⚠️ TypeScript Strict-Null Narrowing Trap (React + useCallback)

When implementing proximity detection in React/TypeScript with strict mode enabled:

```typescript
// ❌ WRONG — TypeScript narrows `closest` to `never` in strict mode
const handleMouseMove = useCallback((e) => {
  let closest: { idx: number; dist: number } | null = null;
  hotspots.forEach((hs, i) => {
    const dist = Math.sqrt(...);
    if (dist < (closest?.dist ?? Infinity)) closest = { idx: i, dist };
  });
  // ❌ TS error: Property 'dist' does not exist on type 'never'
  if (closest && closest.dist <= 6) { ... }
}, [hotspots]);
```

**Root cause:** TypeScript's control flow analysis cannot track mutations to a `let` variable that happen inside a callback/closure (`forEach` lambda). It infers the type as `never`.

**Fix — use primitives instead of nullable objects:**

```typescript
// ✅ CORRECT — use minDist + closestIdx primitives
let minDist = Infinity;
let closestIdx = -1;
hotspots.forEach((hs, i) => {
  const dist = Math.sqrt(...);
  if (dist < minDist) { minDist = dist; closestIdx = i; }
});
if (closestIdx >= 0 && minDist <= 6) {
  const hs = hotspots[closestIdx];  // ✅ no type issue
}
```

This avoids `| null` narrowing entirely — sentinel value `-1` + `Infinity` works in any strict TS config.

---

## Phase 4: Hover-on-Photo Best Practices (UX Pattern)

When the user wants descriptions on photos, follow this hierarchy of interactions:

1. **Invisible pins at rest** — 6px gold dots with 0 opacity. Image is pristine with no visual clutter.
2. **Proximity reveal** — dots fade in when cursor enters ~60px radius of the hotspot position.
3. **Tooltip on close hover** — when cursor is within ~30px of the hotspot, show a rich tooltip card with: code (gold, uppercase), name (serif, white), category badge, and a meta grid of finish/colour/supplier.
4. **Click to pin** — clicking a hotspot opens a sidecar panel with the full material spec.
5. **Positioning** — tooltip should be above and to the side of the cursor (16px offset), flipping to prevent overflow off-screen.

**User preference**: always make hotspot pins invisible at rest unless the user explicitly asks to see labels. The first version commonly shows always-visible labels — this is NOT what the user wants. They want pristine images with info that reveals on interaction.

### Tooltip Edge-Flip Positioning (Smart)

The tooltip must always stay on-screen regardless of cursor position. Use edge detection that tries bottom-right first, then flips:

```javascript
let tx = e.clientX + 16, ty = e.clientY + 16;
const cardW = 300, cardH = 280;
// Try bottom-right — but flip if too close to edge
if (tx + cardW > window.innerWidth - 20) tx = e.clientX - cardW - 16;
if (ty + cardH > window.innerHeight - 20) ty = e.clientY - cardH - 16;
// Clamp to minimum margin
if (tx < 10) tx = 10;
if (ty < 10) ty = 10;
```

### Mouse Move Performance (rAF Throttling)

Raw `mousemove` handlers fire at display refresh rate (60fps+) and cause React re-render storms. **Always throttle with requestAnimationFrame and a minimum-distance skip:**

```javascript
// React pattern
const rafRef = useRef(0);
const lastPos = useRef({x:0, y:0});

const handleMouseMove = useCallback((e) => {
  // Skip if mouse barely moved (<3px) — avoids jitter on still cursor
  const dx = e.clientX - lastPos.current.x;
  const dy = e.clientY - lastPos.current.y;
  if (Math.abs(dx) < 3 && Math.abs(dy) < 3) return;
  lastPos.current = {x: e.clientX, y: e.clientY};

  // Cancel any pending frame — only process latest
  if (rafRef.current) cancelAnimationFrame(rafRef.current);
  rafRef.current = requestAnimationFrame(() => {
    // Expensive proximity calculations here
    // Use for-loop instead of .forEach for less closure overhead
    for (let i = 0; i < hotspots.length; i++) {
      // distance calculation...
    }
  });
}, [hotspots]);
```

### React/TypeScript Integration

When embedding hotspot functionality in a Vite+React+TypeScript app:

**Data flow:**
1. Extract images from PPTX → copy to `public/images/`
2. Extract schedule swatches → copy to `public/images/swatches/`
3. Use `materials.json` as the data source (created by Kimi or from Excel)
4. Build hotspot data as static TypeScript arrays in the component

**Component structure:**
- `Gallery.tsx` — card grid (entry point)
- `GalleryModalContent` — image viewer with hotspots, sidebar, view navigation
- Use `useCallback` + `useRef` for performant mousemove handlers
- Use `useState` for tooltip position/content and active pin index

**Key patterns:**
```typescript
// Hotspot type
interface Hotspot { code: string; x: number; y: number; }

// Tooltip state
const [tooltip, setTooltip] = useState<{x:number; y:number; code:string; data:Record<string,string>}|null>(null);

// Lookup material data from JSON
const matMap = new Map(mats.map((m:any) => [m.code, m]));
// Usage: const mat = matMap.get(hs.code) || {};
```

## Extracting Swatch Images from Schedule Tables

When a PPTX has schedule tables with reference images next to each material row, extract them by matching table rows to images by position:

```python
from pptx import Presentation
from pptx.enum.shapes import MSO_SHAPE_TYPE
from PIL import Image
import io, os, re

prs = Presentation("presentation.pptx")
slide = prs.slides[slide_idx]

# Get all images on this slide
images = []
for shape in slide.shapes:
    if shape.shape_type == MSO_SHAPE_TYPE.PICTURE:
        images.append({'blob': shape.image.blob, 'left': shape.left, 'top': shape.top})

# Match table rows to images by position order
for shape in slide.shapes:
    if shape.has_table:
        table = shape.table
        for row_idx in range(1, len(table.rows)):  # Skip header
            cells = [cell.text.strip() for cell in table.rows[row_idx].cells]
            code = cells[1]  # Second column is material code
            # Match by row order (images in the table column are ordered top-to-bottom)
            img_idx = row_idx - 1
            if img_idx < len(images):
                img_data = images[img_idx]['blob']
                pil = Image.open(io.BytesIO(img_data))
                if pil.mode == 'RGBA': pil = pil.convert('RGB')
                safe_name = code.replace('/', '_').replace('\\', '_')
                pil.save(f'swatches/{safe_name}.jpg', 'JPEG', quality=80)
```

**In the Gallery.tsx component**, include the swatch in the tooltip data:
```typescript
swatch: `/images/swatches/${hs.code}.jpg`,
```

And render it in the tooltip card with an `onError` fallback:
```tsx
{tooltip.data.swatch && (
  <div className="htc-swatch">
    <img src={tooltip.data.swatch} alt={tooltip.code}
      onError={(e) => (e.currentTarget.style.display = 'none')}
      style={{width:'100%', height:'100%', objectFit:'cover', borderRadius:'6px'}}/>
  </div>
)}
```

## ⚠️ Critical Pitfall: read_file() Truncation

When working with large HTML files (>500 lines) generated by subagents:

**`read_file()` defaults to 500 lines.** Any content beyond line 500 is silently truncated. If you then pass the result to `write_file()`, the file is permanently corrupted.

**Always pass `limit=N`** where N exceeds the expected file size (e.g. `limit=10000` for a 1400-line file), or use `cat` via terminal() to get the raw content.

**Line-number contamination:** `read_file()` returns content with `N|` prefixes (e.g. `1|<!DOCTYPE html>`). Writing this output back via `write_file()` bakes line numbers into the file, breaking CSS, HTML structure, and all functionality. To fix contaminated files, strip with:

```python
import re
with open('file.html') as f: raw = f.read()
clean = re.sub(r'^\s*\d+\|', '', raw, flags=re.MULTILINE)
with open('file.html', 'w') as f: f.write(clean)
```
