---
name: interactive-material-showcase
description: Build and maintain React-based material specification viewers with image hotspot annotations, schedule-based info cards, grouped sidebar legends, and mobile-responsive gallery modals. Used for museum/interior fit-out material presentations.
version: 1.0.0
author: Hermes Agent
platforms: [macos, linux]
metadata:
  hermes:
    tags: [react, gallery, materials, museum, showcase, hotspot, info-card, schedule, mobile]
---

# Interactive Material Showcase

Build and maintain React/TypeScript material specification viewers. Covers gallery modals with hotspot annotations, schedule-type info cards, grouped sidebar legends, and mobile-responsive layouts.

## Pipeline — Complete Workflow (absorbed from `interactive-material-hotspots`)

### 1. Extract Callout Positions from PPTX

```python
from pptx import Presentation
import re
prs = Presentation("file.pptx")
for slide in prs.slides:
    for shape in slide.shapes:
        if shape.has_text_frame:
            text = shape.text_frame.text.strip()
            if re.match(r'^[A-Z0-9_]+\\.[0-9A-Z_]+$', text):
                img_shape = find_overlapping_image(shape, slide)
                rel_x = (shape.left - img_shape.left) / img_shape.width
                rel_y = (shape.top - img_shape.top) / img_shape.height
```

### 2. Generate Hotspot Data JSON

```typescript
interface Hotspot { code: string; x: number; y: number; }
interface View { viewName: string; filename: string; desc: string; hotspots: Hotspot[]; }
interface GalleryData { id: string; title: string; views: View[]; }
```

### 3. Build the React Gallery Component

Key patterns:
- Percentage-based pin positioning (`left: hs.x+'%', top: hs.y+'%'`)
- Three-layer pin state: `pinnedRef` + `clickedRef` + `pinnedCode`
- Cross-component nav uses `CustomEvent` for `schedule-change`
### Placeholder entries: use `hotspots:[]` for views that need admin-pin setup later (shows photo + gallery card but no clickable pins until user adds them via admin panel)
- **Adding new galleries**: append entries to `galleryData` array in `Gallery.tsx`. Each new gallery needs `{id, title, views: [{viewName, filename, desc, hotspots}]}`. Update the static gallery description text (e.g., "16 annotated 3D views across 8 galleries") to match the new count.

### Submission Reference (subRef) for Document Names

When images carry a submission document name (e.g., `MOC-ASE-AR-ARC-BF-DDD-VIS001`), store it as a `subRef` field on each view and display as a gold badge in the sidebar:

```typescript
// Interface
interface View { viewName: string; filename: string; desc: string; subRef?: string; hotspots: Hotspot[] }

// Data entry
{viewName:'G4_View_1', filename:'/aseer/images/g4_G4_View_1.jpg', subRef:'MOC-ASE-AR-ARC-BF-DDD-VIS001', desc:'Main gallery hall overview', hotspots:[...]}

// Display in sidebar (GalleryViewer JSX, after view description)
{view.subRef && (
  <div style={{
    fontFamily:"'IBM Plex Mono',monospace", fontSize:'0.55rem',
    color:'#C8A45C', background:'rgba(200,164,92,.1)',
    padding:'3px 8px', borderRadius:'4px', marginBottom:'8px',
    display:'inline-block', letterSpacing:'0.02em',
  }}>{view.subRef}</div>
)}
```

### Photo Replacement Preserving Hotspot Positions

When replacing a view's image with a new photo (e.g., updated architectural render), **do NOT change the `filename` path** in Gallery.tsx. Instead:

1. Upload the new image to the **same path** on the server — overwrite the old file
2. The `hotspots:[{code, x, y}]` array stays untouched — percentage positions remain valid
3. Add cache-busting so browsers load the new image (see Cache-Busting below)

```bash
cat /path/to/new_VIS004.jpg | ssh -p <port> user@host "cat > /remote/images/g6_G6_View_3B.jpg"
```

### Cache-Busting for Replaced Images

Add a version constant at the top of the gallery file and append it to image URLs:

```typescript
const IMG_VERSION = '2'; // bump when replacing photos

// In image render:
<img ref={imgRef} src={`${view.filename}?v=${IMG_VERSION}`} alt={view.desc} ... />
```

When you bump `IMG_VERSION`, the `?v=N` param changes → browser treats it as a new URL → fetches from server instead of cache. This is simpler than renaming files on the server.

### Floor-Based Gallery Sorting

Add a `floor` field to each gallery entry and sort by floor in the render:

```typescript
interface GalleryData { id: string; title: string; floor?: string; views: View[] }

// In gallery data:
{id:'g4', title:'G4 - Saudi Art', floor:'BF', views:[...]}
{id:'g1', title:'G1 - Welcome Gallery', floor:'LGF', views:[...]}

// Sort in render - LGF first, BF second:
{[...galleryData].sort((a,b)=>{
  const order = {LGF:0, BF:1};
  return (order[a.floor||'']||2) - (order[b.floor||'']||2);
}).map(g=>{...})}
```

Floor badge on each gallery card (gold monospace label, below the title):
```typescript
{g.floor && <span style={{
  fontFamily:"'IBM Plex Mono',monospace", fontSize:'.6rem', fontWeight:600,
  color:'#C8A45C', background:'rgba(200,164,92,.1)',
  padding:'2px 8px', borderRadius:'3px', letterSpacing:'0.05em'
}}>{g.floor === 'LGF' ? 'LOWER GROUND' : 'BASEMENT'}</span>}
```

### Updating Gallery Count Text

After adding/removing galleries, manually update the static text in the gallery render section:

```
20 annotated 3D views across 12 galleries. Click to explore...
```

Count from `galleryData` array — no dynamic counter. Update whenever gallery count changes.

### OneDrive Path Restructure — Symlink Fixes

The project may be stored under OneDrive with deep paths. When OneDrive sync restructures the folder hierarchy (e.g., `Completed Tender Package From NRS` → `14_Completed_Tender_Package_From_NRS`):

1. **Find the new path** with `mdfind -name 'Gallery.tsx'` or `find` (may be slow on OneDrive)
2. **Check symlinks** in `public/`:
   ```bash
   ls -la public/aseer/images   # if symlink, check destination exists
   ```
3. **Fix broken symlinks** caused by path changes:
   ```bash
   rm public/aseer/images && ln -s ../images public/aseer/images
   ```
4. **Rebuild** — Vite follows symlinks and copies images from the target dir into dist/

Common symptom of broken symlink: `ENOENT: no such file or directory, stat 'public/aseer/images'` during build.

### Tooltip Card Styling (Redesigned — Light Gold Accent)

```css
.hotspot-tooltip-card {
  position: fixed; z-index: 210; pointer-events: none;
  width: 360px; max-height: 65vh;
  background: #FCFAF7;
  border: 1px solid rgba(200,164,92,.25);
  border-radius: 14px; padding: 14px 16px 12px;
  box-shadow: 0 12px 48px rgba(0,0,0,.15), 0 0 40px rgba(200,164,92,.08);
  overflow-y: auto;
}
/* Gold gradient accent bar at top */
.hotspot-tooltip-card::before {
  content: ''; position: absolute; top: 0; left: 16px; right: 16px;
  height: 3px; background: linear-gradient(90deg, #C8A45C, #D4B872, #C8A45C);
  border-radius: 0 0 2px 2px;
}
.hotspot-tooltip-card.pinned { pointer-events: auto; user-select: text; }
```

Key changes from previous glassmorphism version:
- Solid off-white bg (`#FCFAF7`) instead of translucent + backdrop-filter — more readable
- Gold gradient accent bar at top via `::before` pseudo-element
- Wider card: 360px instead of 340px
- Group backgrounds: `rgba(200,164,92,.04)` with `border-radius: 6px` and `padding: 4px 8px`
- Group titles: darker brown `#8A7A5A`, bold 700
- Category badges: darker text `#6B5D42`, no border
- Source badges: removed border, darker text `#6B5D42`

### 5. Font Hierarchy

| Element | Font | Weight | Size |
|---------|------|--------|------|
| Hotspot code (tooltip header) | IBM Plex Mono | 700 | 10px uppercase |
| Material name (tooltip title) | Playfair Display | 600→700 | 14px |
| Category badge | Inter | — | 9px |
| Field labels | Inter | 500 | 7px uppercase |

See `interactive-material-hotspots` skill (now absorbed) for complete theme colors, RAL color swatch regex, clean name utilities, sidebar legend grouping, presentational schedule filtering, mobile modal layout, and dimension cleaning functions.

## Schedule Info Card Design

Each schedule type (Finishes, Setwork, Showcase, etc.) has a custom field group definition in `SCHEDULE_FIELD_GROUPS`. Follow these rules:

### Field Group Structure
```typescript
'schedule_type': [
  { label: 'Group Name', fields: [
    { key: 'Exact JSON Key', label: 'Display Label' },
    { key: 'description', label: 'Description', full: true },  // spans both columns
    { key: 'code', label: 'Code', mono: true },                 // monospace font
  ]},
]
```

### Design Rules
- **2-3 groups max** per type. Merge related fields into fewer groups for compactness (e.g., Showcase info card went from 5 groups / 27 fields to 2 groups / 17 fields — dimensions + specs merged into the main "Showcase" group, environment/climate kept separate).
- **2-6 fields per group** — the main group can have up to 12 fields if they're short label-value pairs (e.g., W, H, D, Glass Sides, Door, Lock, Rating, Objects)
- Mark long text fields as `full: true` (spans both columns)
- Mark code/ID fields as `mono: true` (monospace font)
- Most important fields first (what a site architect needs quick access to)
- Description/main text field always included when available
- Use `'description'` (lowercase) as key — the materials.json uses lowercase, not the schedule JSON casing

### Key Casing Pitfall
The `materials.json` has **different key casing** than the schedule JSON files. Always verify against `materials.json`:
- `description` (lowercase d) — NOT `Description`
- `finish`, `colour`, `supplier` (lowercase) — NOT the schedule JSON's capitalized versions
- `substrate` (lowercase s) — NOT `Susbtrate`
- Schedule-specific keys like `Exhibit Name`, `Gallery Name`, `Space Name` retain their original casing
- Use `.get('code')` to verify — the `code` field is the unified identifier

### hasValue Check
The `hasValue()` helper treats these as empty: `#VALUE!`, `#VALUE`, `n/a`, `N/A`, `None`, empty strings. Fields with only placeholder values are auto-hidden in the info card.

## Gallery Modal & Sidebar Legend

### Layout
- Desktop: image on left, sidebar on right (flex row)
- Mobile (≤768px): stacks vertically via `flexWrap:'wrap'`
- Sidebar width: 320px, scrollable, with backdrop blur

### Sidebar Legend Structure
```
Gallery Title (Playfair Display, 1.3rem, bold)
View Description · View X of Y (Inter, 0.8rem, medium weight)
[1] [2] ...           ← view selector buttons
[◎ Hotspots ON]       ← toggle in sidebar, not floating on image
MATERIALS (N)
  FINISHES            ← group header (gold-tinted bg, dark brown text)
    1  FI_FL_04
  SETWORK
    2  04.04_SW_01
```

### Grouping Materials
Group sidebar materials by `schedule_key`:
```typescript
const GROUP_LABELS: Record<string,string> = {
  'finishes_schedule':'Finishes',
  'setwork_schedule':'Setwork',
  // ... add as needed
};
```
Groups are sorted: known order first, then alphabetical. Known order: Finishes, Setwork, Showcase, Graphic, Wayfinding, FF&E, Object, Exhibit, Art Commission, Media, AV Equipment, Lighting.

### Group Header Styling
- Text: bold 700, uppercase, 0.55rem, dark brown `#5A4E2A`
- Background: gold tint `rgba(200,164,92,.12)`, rounded corners, tight padding

## Presentation Data Filtering

### Active Schedules
At presentation stage, only load schedules relevant to the project phase. Define in `ACTIVE_SCHEDULES`:
```typescript
const ACTIVE_SCHEDULES = ['finishes_schedule','setwork_schedule','showcase_schedule', ...];
const matMap = new Map(mats.filter((m:any)=>ACTIVE_SCHEDULES.includes(m.schedule_key)).map((m:any)=>[m.code, m]));
```

**Do NOT auto-detect by hotspot usage** — the user decides what's relevant. Keep non-essential types (Object, Exhibit, Media, Asset, Model, etc.) out until the user adds them.

### Schedule Table Column Filtering
In Schedule.tsx `hasData()`:
```typescript
const hasData = (field: string) => currentMats.some(m => {
  const v = m[field as keyof typeof m];
  return v && !['#VALUE!','#VALUE','n/a','N/A','TBC','TBD','None'].includes(String(v).trim()) && String(v).trim();
});
```
This auto-hides columns where all values are placeholders (image columns with `#VALUE!`, `TBC` fields, etc.).

## Version Control Before CSS Changes

**Always run `git init && git add -A && git commit -m "init"` before making CSS/layout changes.** This allows reverting broken changes. Push to GitHub:

```bash
gh repo create <name> --private --source=. --remote=origin --push
```

Commit after every working change. The user explicitly requested version control.

## Build on OneDrive — Workarounds

The project lives under OneDrive. The large schedule JSON files (`src/data/schedules/*.json`, each 1-5MB, 21 files) cause `tsc -b` and `vite build` to hang for minutes or time out entirely.

### Workaround 1: API Build (skip tsc)

Create a `build.mjs` in the project root:
```js
import { build } from 'vite';
const result = await build({ logLevel: 'info' });
console.log('Build completed');
```
Then: `node build.mjs`

This bypasses `tsc -b` (which is `noEmit: true` anyway — only type-checks) and runs Vite's Rollup build directly. Completes in ~60-90s instead of hanging indefinitely.

### Workaround 2: Incremental Deploy (skip tarball)

Rather than `tar czf dist/` (47MB+ with images), upload only changed files:
```bash
scp -P <port> dist/assets/index-<hash>.js  user@host:/remote/assets/
scp -P <port> dist/index.html              user@host:/remote/
```

Images rarely change between builds.

### Pre-Deploy Build Verification

See `web-deployment` skill's **Vite Build Warnings → Silent Runtime Crash (Three.js)** and **Script crossorigin + No CORS Headers** sections. These checks catch the most common "build succeeded but site is blank" scenarios.

### Deploy via SSH Pipe (when SCP hangs)

Some hosting providers block SCP or throttle large transfers. If `scp` hangs despite SSH working (`ssh -o BatchMode=yes` succeeds), use a pipe instead:

```bash
# Upload single file
cat local-file.jpg | ssh -p <port> -o BatchMode=yes user@host \
  "cat > /remote/path/target.jpg"

# Upload tarball (multiple files)
tar czf /tmp/deploy.tar.gz index.html assets/ sync.php
ssh -p <port> -o BatchMode=yes user@host \
  "cat > /tmp/deploy.tar.gz" < /tmp/deploy.tar.gz
ssh -p <port> -o BatchMode=yes user@host \
  "cd /remote/path && tar xzf /tmp/deploy.tar.gz && rm /tmp/deploy.tar.gz"
```

The pipe avoids SCP's authentication negotiation — it runs over the existing SSH session. Always verify files landed correctly with a follow-up `ls -lh` or `file` command.

For the samaya-factory.com server: port 65002, user u517606786, base path `/home/u517606786/domains/samaya-factory.com/public_html/build/aseer/`.

## Print PDF Feature

The project includes an optional `PrintView` component that renders an A4-portrait printable view via `window.print()`. It is triggered by a button in the gallery modal sidebar.

### Location

- **Component**: `sections/PrintView.tsx` — renders clean photo, annotated photo with numbered pins, and material legend grouped by schedule type, spread across 3 pages.
- **Trigger**: `sections/Gallery.tsx` — `showPrint` state (useState false) + `<button>🖨️ Print PDF</button>` in the sidebar panel, between the Hotspots toggle and the materials list.
- **Print overlay**: Rendered in a `position:fixed; z-index:10000; background:#fff; overflow:auto` container via `createPortal` to `document.body`. Calls `window.print()` after image loads.

### Disabling Print PDF

To remove the print feature:

1. **Remove the button** in `Gallery.tsx` — the `<button>` block between the Hotspots toggle and the "Materials (N)" header (identified by `🖨️ Print PDF` text content).
2. **Optional**: Remove `import PrintView from './PrintView'` and the `showPrint` state + render block at the bottom of the component.
3. **Rebuild** (`npm run build`) and deploy only `index.html` + the new JS bundle.

### Finding the Print Feature in Minified JS

If the source is unavailable, search the deployed `assets/index-*.js` for:
- `window.print()` — the core print call
- `🖨️ Print PDF` — the button text (appears in JSX string)
- `k.jsx(ZB,{viewTitle:` — the PrintView component render (ZB is the minified name)

## Data Provenance Tracing

When the user questions why specific data appears in the schedule views, trace it back to the source JSON files in `src/data/schedules/`. The data comes directly from NRS (Nissen Richards Studio) design exports.

Common user questions and their sources:
- **"Why is 'Landscape' under setwork/exhibition?"** → The setwork schedule JSON has `"Exhibit Name": "Landscape"` and `"Architecture & Landscape"` — these are **gallery theme names** (sub-sections of G4: Saudi Art - Landscape & Architecture), not landscaping items. Exhibition IDs `ET_04.04` and `ET_04.05`.
- **"Remove the Exhibit field from the info card"** → When users see "Exhibit: Landscape" on a setwork/showcase info card, it's confusing because these are gallery theme names, not actual exhibit pieces. **Solution:** Remove `{ key: 'Exhibit Name', label: 'Exhibit' }` from `setwork_schedule` and `showcase_schedule` SCHEDULE_FIELD_GROUPS in Gallery.tsx. The `Exhibition ID` field can remain for reference. This fix applies to any schedule type where the exhibit name is a gallery theme rather than a specific exhibit piece.
- **"Where does this finish/colour come from?"** → The `materials.json` file (finishes schedule) or the specific schedule JSON (setwork, showcase, etc.)

Always check the source JSON first before assuming a display bug. The schedule viewer renders whatever keys/values exist in the source data — it doesn't transform or filter exhibit names.

## Performance Optimization

### WebGL Background Pause Pattern

If the app uses a Three.js animated background (`useInfiniteLights`), it can be the **#1 cause of desktop lag**. Key optimizations:

1. **Reduce pixel ratio** — `renderer.setPixelRatio(Math.min(window.devicePixelRatio, 1))` instead of 2. On Retina this halves the GPU workload (14.7M → 3.7M pixels/frame) with minimal visual difference for a background shader.

2. **Pause animation when hidden/covered** — the shader should not render when the gallery modal is open (it's hidden behind an opaque overlay) or when the browser tab is backgrounded:

```typescript
// In the useInfiniteLights effect:
let paused = false;
const onVis = () => { paused = document.hidden; };
const onModal = () => { paused = true; };
const onModalClose = () => { paused = false; };
document.addEventListener('visibilitychange', onVis);
window.addEventListener('gallery-modal-open', onModal);
window.addEventListener('close-gallery-modal', onModalClose);

const animate = () => {
  rafRef.current = requestAnimationFrame(animate);
  if (paused) return;  // skip render — GPU stays idle
  // ... render ...
};
```

Dispatch events from Gallery.tsx:
```typescript
const openGallery = useCallback((g) => {
  setActiveGallery(g);
  window.dispatchEvent(new Event('gallery-modal-open'));
}, []);
```

(The `close-gallery-modal` event is already dispatched by Navigation.tsx.)

3. **Remove `backdrop-filter: blur()`** — these re-composite the entire backdrop (including the animated canvas) on every frame. Replace with solid/near-opaque backgrounds (`rgba(245,241,235,.97)` instead of `.9` + `backdropFilter`).

4. **Lazy-load getMaterials()** — the 1.18MB materials dataset should only be loaded when the editor is open:
```typescript
materials={editMode ? getMaterials() : []}
```

### Canvas/Content Z-Index Stacking

The dynamic background canvas (WebGL) must stay behind ALL content. The correct stacking:

```html
<div id="root" style="position:relative;z-index:1;min-height:100vh;"></div>
<canvas id="webgl" style="position:fixed;top:0;left:0;width:100%;height:100%;z-index:-1;pointer-events:none;"></canvas>
```

Key rules:
- `z-index: -1` on canvas puts it behind even unpositioned elements (auto = 0)
- `z-index: 1` on root wraps all content above the canvas
- `pointer-events: none` on canvas ensures clicks/touches pass through
- `min-height: 100vh` on root ensures it covers the full viewport

Without this, the fixed canvas can appear above content sections that lack explicit `z-index`, especially after CSS changes to the gallery modal.

## Mobile Responsive Patterns

### ⚠ CSS Specificity Trap
Media query rules can be silently overridden by base class rules declared later in the CSS file — both have the same specificity, and the later rule wins. **Fix:** always use higher-specificity selectors inside media queries:

```css
/* BROKEN — base class `.modal-image-wrap` later in file overrides this */
@media (max-width: 768px) {
  .modal-image-wrap { overflow: visible; }       /* overridden! */
}

/* FIXED — parent selector adds specificity */
@media (max-width: 768px) {
  .gallery-modal .modal-image-wrap { overflow: visible; }  /* wins */
}
```

Apply this pattern to ALL mobile rules that override base styles: `.gallery-modal .modal-XXX` not just `.modal-XXX`.

### Mobile Layout: Page Scrolling, NOT Internal Image Panning

The user wants **normal page scrolling** on mobile — NOT touch-drag/pan inside the image container.

**Correct approach:**
- `.gallery-modal` has `overflow-y: auto` — modal is a scrollable page
- `.modal-image-wrap` has `overflow: visible` — image flows naturally, no internal scroll context
- `.modal-image-wrap img` has `width: 100%; height: auto; max-height: none` — image fills width, scrolls vertically
- The sidebar (`.modal-sidebar-panel`) has `max-height: none; overflow: visible` — flows below image

```css
@media (max-width: 768px) {
  .gallery-modal { padding: 16px; }
  .gallery-modal .modal-container { max-height: none; }
  .gallery-modal .modal-content-row { flex-direction: column !important; }
  .gallery-modal .modal-image-wrap { overflow: visible; width: 100%; }
  .gallery-modal .modal-image-wrap img { width: 100% !important; height: auto !important; max-width: 100% !important; max-height: none !important; }
  .gallery-modal .modal-sidebar-panel { width: 100% !important; max-height: none !important; overflow: visible !important; }
}
```

**WRONG approach** (creates internal touch-drag, which user rejected):
- ❌ `overflow: auto` with `max-height: 78vh` on image wrap — creates internal scroll context
- ❌ Touch-drag panning handlers on the image
- ❌ CSS transform translate on image

### Close Button Positioning (Mobile)

The × close button must be **always visible** on mobile, even when scrolling. The working formula:

```css
.gallery-modal .modal-close-btn {
  position: fixed !important;
  top: 12px !important;
  left: 12px !important;
  z-index: 99999 !important;
  background: rgba(245,241,235,.95);
  border: 1px solid rgba(26,29,35,.2);
  box-shadow: 0 2px 12px rgba(0,0,0,.14);
}
```

Key points:
- `position: fixed !important` with `!important` on ALL positioning props — the base class has `position: absolute; top: -12px; left: -12px` which must be fully overridden
- Use simple pixel values, NOT `env(safe-area-inset-*)` — the safe-area functions caused positioning bugs on some devices
- `z-index: 99999` ensures it's above the modal backdrop
- Opaque `rgba(245,241,235,.95)` background ensures it's visible over any image content
- If the close button stops being clickable, the backdrop is intercepting clicks — ensure `.modal-container` has `z-index` > `.modal-backdrop` (or leave backdrop without z-index and container with `position: relative; z-index: 2`)

### Image + Sidebar Stack
Use `flexWrap:'wrap'` on the image+sidebar row. On mobile the sidebar drops below the image.

### Hotspots Toggle Button
Place in the **sidebar legend** between view selector and materials list — NOT floating over the image. Use a compact full-width button with `showHotspots` toggle state (green when ON, gray border when OFF).

**Make it eye-catching:**
- Use emoji icons: `📍 Hotspots ON` / `🚫 Hotspots OFF`
- `fontSize: 0.65rem, fontWeight: 700`
- `padding: 7px 12px`
- When ON: `background: rgba(74,222,128,.15); boxShadow: 0 0 12px rgba(74,222,128,.15)` — green glow
- When OFF: `background: rgba(26,29,35,.03)` — subtle fill, not transparent

### Nav Closes Modal
Navigation items dispatch a `close-gallery-modal` CustomEvent. The Gallery component listens and calls `setActiveGallery(null)`.

### Mobile Close Button NOT Clickable
If the × button appears but doesn't close the modal, the `.modal-backdrop` (position: fixed; inset: 0) is intercepting the click. Fix the z-index stacking:
- `.modal-backdrop`: no z-index (stays at auto within gallery-modal)
- `.modal-container`: `position: relative; z-index: 2` (above backdrop)
- `.modal-close-btn`: highest z-index within container

## Hotspot Pin Positioning Stability

When hotspot pins shift after image resize (user complaint: "when image sizes changed hotspot location changed"):

### Root Cause
`object-fit: contain` + `maxHeight` on the image creates letterboxing — the image doesn't fill the container, but pins use percentage (`x%`/`y%`) positions relative to the **container**, not the **visible image area**. When the image is letterboxed (shrunk to fit), the pins' percentage positions map to wrong locations on the visible image.

### Fix
Use a **fixed-height container** with `overflow: hidden` and `object-fit: cover` on the image:
- The image fills the container completely (no letterboxing)
- Pins at `x%`/`y%` map to the container, which matches the visible image area
- Cropped portions of the image (if aspect ratio differs) are outside the visible area, so pins outside the cropped region simply aren't visible

```tsx
<div style={{ position: 'relative', height: '300px', overflow: 'hidden' }}>
  <img src={imageSrc} style={{ width: '100%', height: '100%', objectFit: 'cover', objectPosition: 'center top' }} />
  {hotspots.map(hs => (
    <div style={{ position: 'absolute', left: `${hs.x}%`, top: `${hs.y}%` }}>
      {hs.code}
    </div>
  ))}
</div>
```

For the **gallery modal (interactive)**, apply the same principle: make the image container's rendered dimensions match the image's displayed area. If using `object-fit: contain`, the container must have the same aspect ratio as the image.

For **print PDFs**, see the `html-print-layout` skill's React Print with createPortal section for the print-specific implementation (A4 landscape, page breaks, fixed image containers).

## Dimension Cleaning

For presentation, strip dimensions from material descriptions:
```typescript
export function cleanName(desc: string): string {
  // Strip leading: "2500 x 450mm ", "1960x450mm ", "3500(w) x 4000(h) x 400(d)mm "
  // Strip mid-text: " - 420mm x 1420mm", " / 286 x 205mm"
  // Capitalize first letter
}
```

## References
- `references/architectural-pdf-extraction.md` — extracting VIS numbers from NRS location plan PDFs
- `references/info-card-field-groups.md` — complete field group definitions for all schedule types
- `references/schedule-data-keys.md` — actual JSON keys from materials.json per schedule type
- `references/aseer-photo-replacement-jun2026.md` — batch photo replacement workflow with VIS mapping
- `references/section-numbering-pattern.md` — adding new sections: numbering, bilingual AR/EN labels, inline SVG icons, navigation registration, and layout conventions
