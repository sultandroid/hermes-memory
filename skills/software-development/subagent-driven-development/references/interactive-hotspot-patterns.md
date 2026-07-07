# Interactive Image Hotspot Patterns

Architecture/interior design material visualization on 3D render images.

## Core UX Pattern: Study Pin + Detail Panel

1. **Pins at rest** — visible gold dots with subtle glow, numbered badges for orientation
2. **Proximity reveal** — nearby pins glow brighter as cursor approaches (12% radius)
3. **Hover tooltip** — rich dark glassmorphism card with: code, name, category, finish, colour, supplier, element
4. **Click/pin** — opens sidecar panel with full material specification
5. **Sidebar** — scrollable material list for the current view, searchable, filterable

## Pin Styling

| State | Style | Size |
|-------|-------|------|
| Default | `opacity: 1`, `box-shadow: 0 0 0 4px rgba(255,255,255,.2), 0 0 0 7px rgba(196,117,74,.2), 0 0 20px rgba(196,117,74,.3)` | 14px |
| Active (proximity) | Stronger glow, wider rings | 20px |
| Selected (clicked) | Multi-ring glow (white + gold + wide) | 20px |

**NEVER use `pointer-events: none` on pin elements** — this is the #1 cause of "click doesn't work" bugs in hotspot systems. The browser silently drops all mouse events, making React onClick handlers dead code.

| Pin property | Effect | |
|-------------|--------|--|
| `pointer-events: none` | Click handler NEVER fires | ❌ Avoid |
| `cursor: pointer` | Click handler fires, visual feedback | ✅ Correct |

The pins need to be clickable. Use `pointer-events: auto` (default) on the pin itself, and only use `pointer-events: none` on decorative children (label badges, inner rings) that should let events pass through to the pin.

## Tooltip Positioning (Viewport Clamping, No Flip)

Never flip the card to the opposite side — this makes the card "fly away" from the hotspot point. Instead, clamp to viewport edges:

```js
const cardW = 340, cardH = 420;
let x = pinPosition + 16; // from hotspot center
let y = pinPosition + 16;
// Simple clamp — card stays near the pin, doesn't flip to opposite side
x = Math.max(10, Math.min(x, window.innerWidth - cardW - 10));
y = Math.max(10, Math.min(y, window.innerHeight - cardH - 10));
```

**Before (wrong — aggressive flip):**
```js
if (tx + cardW > window.innerWidth - 10) tx = e.clientX - cardW - 16; // flies to left side
```
This sends the card far from the pin when near the right edge.

**After (correct — viewport clamp):**
```js
tx = Math.max(10, Math.min(tx, window.innerWidth - cardW - 10));
```
Keeps the card within viewport but as close to the pin as possible.

## Click-to-Pin Tooltip (Stays on Click)

The tooltip should appear on hover but **stay pinned when the user clicks the hotspot**. This prevents the card from disappearing when the mouse moves away.

### Implementation Pattern (clickedRef Boolean — Simplest, Most Reliable)

Use a single `clickedRef` that **completely blocks all mousemove-based tooltip changes** after a click:

```tsx
const [pinnedCode, setPinnedCode] = useState<string | null>(null);  // for UI (active pin styling)
const clickedRef = useRef(false);  // blocks ALL mousemove tooltip changes after click

const handleMouseMove = useCallback((e) => {
  // Throttle with rAF
  // ... proximity detection in rAF callback ...
  requestAnimationFrame(() => {
    // If a pin was clicked, never update/clear tooltip via mousemove
    if (clickedRef.current) return;
    // ... proximity logic ...
  });
}, [displayHotspots]);

const handlePinClick = useCallback((hs) => {
  if (clickedRef.current && pinnedRef.current === hs.code) {
    // UNPIN same pin
    clickedRef.current = false;
    setPinnedCode(null);
    setTooltip(null);
  } else {
    // PIN
    clickedRef.current = true;
    setPinnedCode(hs.code);
    setTooltip({ x, y, code: hs.code, mat: matMap.get(hs.code) || {} });
  }
}, [pinnedCode]);
```

**Key insight:** Once `clickedRef.current` is `true`, the rAF callback in `handleMouseMove` returns BEFORE touching the tooltip. The tooltip can only be cleared by:
- Clicking the same pin again (toggle)
- Clicking the backdrop (clears clickedRef + removes tooltip)
- Clicking close button
- Navigating to a different view (through `handleViewChange` which clears all state)

### Why NOT ref + state combo (deprecated approach)

Previous attempts used THREE layers (`pinnedRef` + `isPinned` state + `pinnedCode` state) with `isPinned` in the useCallback dependency array. This was over-engineered and unreliable due to:
- Stale closures in useCallback when deps didn't include the pinning state
- Race conditions between rAF callbacks scheduled before vs after the click
- Event handler timing: the old handler (pre-pin) was still attached during the re-render window

**Simple `clickedRef` boolean wins** — one synchronous ref, checked in one place (inside the rAF callback), one guard, no stale closure problems, no dependency juggling.

### Viewport Clamping (No Flip)

When positioning the tooltip card, **don't flip to the opposite side** — it makes the card fly far from its hotspot. Instead, use simple viewport clamping:

```ts
const cardW = 340, cardH = 420;
let x = rect.left + (hs.x / 100) * rect.width + 16;
let y = rect.top + (hs.y / 100) * rect.height + 16;
// Clamp to viewport — card stays near the pin
x = Math.max(10, Math.min(x, window.innerWidth - cardW - 10));
y = Math.max(10, Math.min(y, window.innerHeight - cardH - 10));
```

## Dynamic Field Groups Per Schedule Type

When different material schedules (Showcase, Object, Setwork, Graphic, FF&E, etc.) have vastly different field sets, use a **schedule-keyed field group map** to render a compact, relevant tooltip card for each type.

### Pattern

```tsx
interface FieldDef { key: string; label: string; mono?: boolean; full?: boolean }

const SCHEDULE_FIELD_GROUPS: Record<string, { label: string; fields: FieldDef[] }[]> = {
  'showcase_schedule': [
    { label: 'Showcase', fields: [
      { key: 'Showcase Type', label: 'Type' },
      { key: 'Showcase ID', label: 'ID', mono: true },
    ]},
    { label: 'Glass & Display', fields: [
      { key: 'Glass Thcikness', label: 'Glass' },
      { key: 'Integrated Plinth', label: 'Plinth' },
    ]},
  ],
  'setwork_schedule': [
    { label: 'Setwork', fields: [
      { key: 'Type', label: 'Type' },
      { key: 'Exhibit Name', label: 'Exhibit' },
    ]},
  ],
  // ... per schedule type
};
```

Then render dynamically based on the material's `schedule_key`:

```tsx
{renderFieldGroups(m, m.schedule_key || '')}
```

### Presentation-Stage Curation Rules

For a presentation info card (client/team review), follow these rules:

| Principle | Action |
|-----------|--------|
| **Identifying info** | Keep code, name, type, exhibit |
| **Decision-relevant specs** | Keep finish, colour, supplier, material, glass, lighting |
| **Cross-references** | Remove Exhibit IDs, Setwork IDs, Object IDs (internal linking) |
| **Verbose text blocks** | Remove paragraph-length messages, outcomes, research requirements |
| **Administrative fields** | Remove copyright, collection codes, internal notes |
| **Always-null fields** | Check data first — don't waste card space on always-empty fields |
| **Max per schedule** | 1–2 groups, 3–6 fields total — keeps card compact with no scroll |

Key field names from Excel often differ from app field names. Maintain a normalization map:

```python
FIELD_MAP = {
    'Material ID': 'code',
    'Treatment/Finish': 'finish',
    'Susbtrate': 'substrate',  # Excel typo preserved
    'Description': 'description',
}
```

### Card Size Constraints

- No scrollbar: remove `max-height` and `overflow-y: auto` from `.hotspot-tooltip-card`
- Cap at `max-height: 60vh` so card never exceeds the photo area
- Use compact padding (`10px 14px`) and small fonts (labels 7px, values 9px)
- Reduce group spacing (`margin-bottom: 4px`, gap `8px`) for dense layout
- When pinned: add `pointer-events: auto; user-select: text` via `.pinned` class so text can be selected/copied

### View Change Clears Pin State

When navigating between views (prev/next arrows, view selector buttons), always clear pin/tooltip state before switching:

```tsx
const handleViewChange = useCallback((i: number) => {
  setPinnedCode(null);
  pinnedRef.current = null;
  clickedRef.current = false;
  setTooltip(null);
  setActivePin(-1);
  onViewChange(i);
}, [onViewChange]);
```

Apply this to ALL view change handlers: view number buttons, prev/next arrows, and sidebar clicks.

## Performance: Mouse Move Throttling

Raw `onMouseMove` fires ~60fps. For hotspot calculations:

1. **Min-distance skip** — skip processing if mouse moved <3px (prevents sub-pixel jitter)
2. **requestAnimationFrame** — cancel previous frame, only process one per ~16ms
3. **for loop instead of forEach** — avoids closure allocation overhead for 50+ hotspots

```js
const lastPos = useRef({x:0, y:0});
const rafRef = useRef(0);

const handleMouseMove = useCallback((e) => {
  const dx = e.clientX - lastPos.current.x;
  const dy = e.clientY - lastPos.current.y;
  if (Math.abs(dx) < 3 && Math.abs(dy) < 3) return;
  lastPos.current = {x: e.clientX, y: e.clientY};

  if (rafRef.current) cancelAnimationFrame(rafRef.current);
  rafRef.current = requestAnimationFrame(() => {
    // ... compute distances with for loop ...
  });
}, [deps]);
```

## Hotspot Coordinate System

- Store positions as **percentage values** (0–100), not pixels
- Convert at runtime: `mx = ((e.clientX - rect.left) / rect.width) * 100`
- This works at any image zoom level and screen size
- Filter out positions < 0 or > 100 (outside image bounds)

## Gallery Expand/Collapse: Hotspot Visibility

When gallery sections are expandable/collapsible (common for museum presentations with schedule tables):

- Hotspot pins AND their parent image section should collapse WITH the gallery details
- Move `.section-gallery` INSIDE the `.gallery-details` toggle container
- Toggle JS: `sectionGallery.style.display = details.classList.contains('open') ? 'block' : 'none'`
- Hotspots only activate/interact when their gallery section is expanded and photos are visible
- Rule: **no invisible overlay processing on hidden sections** — avoids wasted computation

## Editor Mode Architecture

When adding a control panel for users to manage hotspots:

| Component | Responsibility |
|-----------|---------------|
| EditorOverlay | Wraps image view, manages EDIT/VIEW toggle, click-to-add, drag-to-reposition, delete |
| MaterialPicker | Searchable/filterable popup list of materials to assign to a hotspot |
| hotspotStore.ts | localStorage persistence layer: save, load, export, import, reset |

### Admin-Only Access (Critical UX)

Edit features MUST be hidden from regular users. Implement:

```js
// Check on component mount
const [isAdmin] = useState(() =>
  window.location.search.includes('admin=1') ||
  sessionStorage.getItem('aseer_admin') === '1'
);
```

- The "Edit Hotspots" button only renders when `isAdmin === true`
- Regular users see viewer-only mode with no indication edit is possible
- To enable: add `?admin=1` to URL or set `sessionStorage.aseer_admin='1'`
- Never show editor controls to non-admin users

### Editor Flow
1. Click "Edit Hotspots" (admin-only) → EditorOverlay opens in EDIT mode (not VIEW)
2. **Open in EDIT mode by default**: `setMode('edit')` on mount, not `setMode('view')`
3. Click image in EDIT mode → record x/y% → open MaterialPicker
4. Select material → assign to new hotspot → pins turn green (#4ADE80)
5. Drag to reposition → mousedown → mousemove → mouseup commits
- Delete → × button on hover → removes hotspot
- Save → localStorage under key `aseer_hotspots_{galleryId}_{viewName}`
- Discard → restore original hotspots from backup

### Search Crash: Null-Check `.toLowerCase()`

**Bug:** Typing in the material search field makes "everything disappear."

**Root cause:** The filter function calls `.toLowerCase()` on material fields (`category`, `description`, `finish`, `colour`) that are `undefined` for many items. This throws a TypeError during React render phase, crashing the component tree.

**Fix — always null-check before calling string methods in filters:**

```tsx
// WRONG — crashes when field is undefined:
m.category.toLowerCase().includes(q)

// CORRECT — safe:
m.category && m.category.toLowerCase().includes(q)
```

**Pattern:** Every `.toLowerCase()`, `.trim()`, `.includes()` on a user-data field must be guarded with `m.field &&` or `(m.field || '').toLowerCase()`. This applies to ALL filter functions, not just editor search.

### Persistent Save Button (Always Visible)

User feedback: the save button must be prominent and always clickable. **Never disable it** — always show the "Save Hotspots" button in edit mode. Add a floating bottom bar with:

- **Save Hotspots** (big green button, always enabled)
- **Export JSON** (downloads a `.json` file with all hotspot positions)
- **Import JSON** (file upload to restore saved positions)
- Text note: "Saved in browser (localStorage) — export to keep backups"

### Data Integrity — Never Invent Data for Hotspots

User corrected this (strong signal): **Do NOT add swatch images, thumbnails, or visual representations of materials that don't exist in the source data files.**

- If the source materials JSON/Excel has no `image` or `swatch` field, do NOT:
  - Extract images from PPTX schedule slides and attach them to materials
  - Generate colored circles from colour names
  - Create placeholder swatches "for now"
- The tooltip card should only show fields that ACTUALLY EXIST in the source data
- If enrichment is needed, ask the user what data source to use
- Violation example: creating a 56-image swatch directory from PPTX schedule tables → user rejects with "dont make form you side"

## Material Admin CRUD Panel

When building a full admin panel for the material database:

### Data Layer (`materialStore.ts`)

- **localStorage-backed**: stores custom materials (`aseer_custom_materials`) and hidden defaults (`aseer_hidden_materials`)
- **Merge logic**: defaults from JSON → remove hidden codes → overlay custom entries → sort by code
- **CRUD**: `getMaterials()`, `addMaterial()`, `updateMaterial()`, `deleteMaterial()`
- **Export/Import**: `exportMaterials()` → JSON string, `importMaterials(json)` → parse and merge
- **Reset**: `resetToDefaults()` → clear localStorage custom data

### UI Pattern (Admin Panel Component)

- **Table**: 7 columns (Code, Category, Description, Colour, Supplier, Thumbnail, Actions)
- **Search**: filters by code or description (case-insensitive)
- **Pagination**: 20 items per page
- **Add/Edit Modal**: form with all fields, code validation, duplicate check
- **Delete**: confirmation dialog with material code
- **Thumbnail column**: 40×40 image if URL exists, "No img" fallback on error
- **Design**: matches app dark theme (#0A0806, gold accents, glassmorphism panels)

### Thumbnail Rule

Only add a `thumbnail` field to the Material interface if the user explicitly asks for it and provides image URLs. Do NOT auto-generate thumbnails from existing data.

## Editor Save Persistence — Critical Bug Pattern

**Bug:** EditorOverlay initializes from view.hotspots (default data), ignoring saved/custom hotspots from localStorage.

**Fix:** Always pass the resolved hotspots (saved overrides) to the editor:

```tsx
const displayHotspots = customHotspots ?? view.hotspots;
<EditorOverlay view={{...view, hotspots: displayHotspots}} .../>
```

**Rule:** The editor component should receive the CURRENT state (with overrides), not the original data source.

## Material Picker: Popup-Only (No Persistent Bar)

The material picker should NEVER be a persistent bottom bar. Popup only:

1. **Add hotspot:** Click empty image area → popup picker appears → select material → closed
2. **Edit existing:** Click a pin → popup picker appears with current material → select new → updated

Bottom bar in edit mode ONLY has: Save (always enabled) + Cancel (discard). No schedule tabs, no code chips, no export/import.

## Pin Click to Edit Material

In edit mode, clicking an existing pin opens the material picker to change assignment (not just show info). On selection, update that pin's code in-place via editingPinIdx state.

## Hotspot Server Sync — Data Loss on Deploy (Critical)

**Bug:** Hotspot data stored inside the deploy directory (`sync.php` with `$dataDir = __DIR__ . '/hotspot-data'`) gets **wiped on every deploy** when the build directory is deleted and recreated (`rm -rf app && mkdir app`).

**Fix — store data OUTSIDE the deploy directory:**

```php
$dataDir = __DIR__ . '/../../hotspot-data';
if (!is_dir($dataDir)) mkdir($dataDir, 0755, true);
```

**Rule:** Any PHP sync endpoint that persists user data must store it OUTSIDE the deploy directory. The deploy script does `rm -rf` on the deploy folder — anything inside it is temporary.

## RAL Color Swatch Rendering

When material fields contain RAL color codes (e.g., `RAL 7015`), render a small inline color swatch next to the value:

```tsx
const RAL_COLORS: Record<string, string> = {
  '7015':'#434B4D','7016':'#293133','7035':'#C5C7C4','9003':'#F4F4F4',
  '9005':'#0A0A0A','9010':'#F7F9F8','5005':'#00538A','3000':'#AF2B1E',
  // ... add RAL codes from project schedules as needed
};

function renderColorSwatch(val: string): React.ReactNode {
  const m = val.match(/\bRAL\s*(\d{4})\b/i);
  if (!m) return null;
  const hex = RAL_COLORS[m[1]];
  if (!hex) return null;
  return <span style={{display:'inline-block',width:14,height:14,
    borderRadius:3,background:hex,marginLeft:6,verticalAlign:'middle',
    border:'1px solid rgba(255,255,255,.15)',flexShrink:0}} />;
}
```

Attach to every field value in the tooltip card:
```tsx
<span className={`fval${f.mono ? ' mono' : ''}`}>
  {String(mat[f.key])}{renderColorSwatch(String(mat[f.key]))}
</span>
```

The regex `/\bRAL\s*(\d{4})\b/i` matches `RAL7015`, `RAL 7015`, or `RAL  7015`. Returns `null` (renders nothing) when the value doesn't contain a RAL code.

## Schedule Table Pagination

For large material schedule tables (1000+ rows), paginate at 25 rows per page with Prev/Next and page number buttons. Reset to page 0 when schedule tab or search query changes.
