# Interactive Material Hotspot Presentations

## When to use
Building a web-based material/object review system on 3D rendered interior/exhibition photos. Each render has hotspot markers overlaid at material positions — hover/click shows full spec from schedule Excel files. Team can collaborate on hotspot placement via server-sync.

## Tech Stack (proven for Aseer Museum)
- **React 19 / Vite** — static build, deployed to any web host
- **TypeScript** — strict mode
- **Inline styles** with light/formal theme (no Tailwind dependency)
- **GSAP / ScrollTrigger** — scroll animations
- **localStorage + server sync** — hotspot position persistence shared across team
- **PHP** — single-file sync endpoint (`sync.php`) for team collaboration
- **openpyxl** (Python) — Excel schedule extraction

## Data Model
```ts
interface Hotspot { code: string; x: number; y: number }  // x,y = percentage
interface View { viewName: string; filename: string; desc: string; hotspots: Hotspot[] }
interface Material {
  code: string; category: string; element: string; description: string;
  finish: string; colour: string; supplier: string; source?: string; schedule_key?: string;
  [key: string]: any;  // index signature for schedule-specific fields
}
```

## Architecture

### Hotspot System
- **Percentage coordinates** only — never pixels. `left: XX%` + `top: YY%` on absolutely positioned overlay div.
- **Gold numbered pins** (14px, `#C8A45C`) with ring + glow. Always visible (not opacity:0).
- **Pins must have `pointer-events: auto`** — otherwise the onClick handler never fires (common CSS bug).
- **Rich tooltip**: glassmorphism card with schedule-aware field groups. Labels: 7px uppercase muted, Values: 9px light text.
- **Tooltip pinning via `clickedRef` (useRef)**: clicking a pin sets `clickedRef.current = true` and `pinnedRef.current = hs.code`. The `handleMouseMove` reads `clickedRef.current` to skip ALL tooltip updates when pinned. This avoids stale closure issues with useCallback.
- **Tooltip card redesign**: wider (360px), solid `#FCFAF7` background (no blur), gold gradient top accent bar (`::before` pseudo-element with `linear-gradient(90deg, #C8A45C, #D4B872, #C8A45C)`), `overflow-y: auto` for long content, subtle group backgrounds `rgba(200,164,92,.04)` with rounded corners. Section labels use darker gold `#8A7A5A` with 700 weight.
- **Submission reference badge**: Add `subRef?: string` to View interface. Display as gold mono badge in sidebar. See `references/image-replacement-workflow.md`.
- **Tooltip position clamping**: `Math.max(10, Math.min(tx, window.innerWidth - cardW - 10))` — simple viewport clamp, no complex flip logic.
- **Tooltip dismissal**: click backdrop/× clears all refs and state. Click image (when pinned) also dismisses.
- **Tooltip selectable when pinned**: `.pinned` class on card adds `pointer-events: auto; user-select: text`.
- **RAL color swatches**: rectangular (40×18px) color chip shown next to values matching `RAL` + 4 digits. Regex uses `(?!\d)` lookahead to avoid matching RAL Design codes (e.g., "RAL 040 40 30" won't produce a false swatch).
- **Schedule-specific field groups**: each schedule type has curated field groups (e.g., Graphic: Type/Substrate/Print Method/Gallery). Non-empty fields only. See `SCHEDULE_FIELD_GROUPS` in Gallery.tsx.
- **Exhibit Name field — REMOVED from showcase/setwork groups**: The NRS schedule has `Exhibit Name` values like "Landscape" (gallery theme names, not exhibit names). These confuse users who see "Exhibit: Landscape" in a setwork info card. Remove `{ key: 'Exhibit Name', label: 'Exhibit' }` from `showcase_schedule` and `setwork_schedule` field groups in `SCHEDULE_FIELD_GROUPS`. Keep `Exhibition ID` — it's a technical reference that doesn't mislead.
- **Generic fallback**: items without a recognized schedule_key show all non-base fields in a 2-column grid.
- **Source schedule line**: bottom of tooltip shows `📋 {source}` (e.g., "Finishes Schedule").
- **Throttle mousemove**: `requestAnimationFrame` + skip if mouse moved <3px. When `clickedRef.current` is true, the rAF callback returns early.
- **Gallery title overlay**: gradient-faded title + description at top of modal.

### Team Sync (Server)
- **Single PHP file** (`sync.php`) acts as the sync endpoint — no database, no Node.js.
- **GET** `/sync.php?gallery=X&view=Y` — returns hotspot JSON array for that view.
- **POST** `/sync.php` — body `{ gallery, view, hotspots }` — saves to `hotspot-data/` directory.
- **Client `hotspotStore.ts`**: tries server first, falls back to localStorage.
- **SYNC_URL** constant set to the deployment URL (e.g. `https://samaya-factory.com/aseer`).

### Admin-Gated Edit Mode
- **Two-layer auth**: `?admin=1` URL param triggers a **password prompt modal**.
- Password check: `sessionStorage.getItem('aseer_admin_auth') === 'true'` — persists for session.
- Admin password is a constant `ADMIN_PW` in the code (changeable).
- After correct password, both "Edit Hotspots" button and Materials Admin panel become visible.
- **Admin check** for child components: `sessionStorage.getItem('aseer_admin_auth')==='true'`.

**Editor workflow (clean bottom bar):**
- Bottom bar only shows **💾 Save** and **✕ Cancel** — no persistent material list.
- **Add hotspot**: click empty area on image → material picker popup appears → select material → pin placed.
- **Edit hotspot material**: click existing pin → material picker opens with current material → pick new material.
- **Move hotspot**: drag pin to new position.
- **Delete hotspot**: hover pin → red × button.
- **Export/Import**: 📤/📥 buttons (separated by divider) for sharing data when sync server is offline.
- Data persists via server sync + localStorage fallback.

**Material picker popup:**
- Schedule filter pills at top (Finishes · Setwork · Showcase · Graphic · Wayfinding · etc.)
- Filtered material chips below — click to select → closes picker → pin placed/updated.
- Search field to filter by code.

### Materials Admin Panel (CRUD)
- Only visible when `?admin=1` AND password-authenticated.
- Full table with add/edit/delete materials.
- Modal forms for each operation.
- **Reset to Defaults**: hidden by default (user must explicitly request it).

### Materials by Schedule (Separate Files)
- Materials are organized into separate schedule files in `src/data/schedules/`:
  - `finishes_schedule.json`, `setwork_schedule.json`, `showcase_schedule.json`, etc.
- `materialStore.ts` loads from all schedule files and merges.
- Admin panel and editor both use `getMaterials()` which returns the merged array.

### Finish Categories → Schedule Navigation
- "02 / Materials" section shows finish category cards (Flooring, Walls, Ceilings, etc.).
- Clicking a card → scrolls to Schedule section → auto-selects that schedule tab via `sessionStorage`.
- **3D hover effect**: `translateY(-4px) scale(1.02) rotateX(2deg)` with gold border glow and box shadow.
- **Back button** in Schedule page navigates back to Materials section.

### Schedule Page
- **Schedule dropdown** selector at top organizing all material schedules.
- **Search**: filters by code, description, supplier, colour, category. Uses safe `.some(f => f && f.toLowerCase().includes(q))` — fields may be undefined.
- **Dynamic columns**: base columns (code, description, category, element, finish, colour, supplier) + schedule-specific extra fields auto-detected from data.
- **Pagination**: 25 rows per page with page number buttons + Prev/Next.
- **Responsive table**: `overflowX: auto`, description wraps at 2 lines, clean row hover.

### Persistence
- **Hotspot edits**: localStorage + server sync (`hotspot-data/` on PHP server).
- **Custom materials**: localStorage `aseer_custom_materials`.
- **Hidden defaults**: localStorage `aseer_hidden_materials`.
- **Export/Import**: JSON download/upload for backup.

### Excel Schedule Extraction (Python / openpyxl)
When extracting material data from 15–20 Excel schedule files:

1. **Auto-detect header row**: scan first 20 rows for column headers matching known keywords.
2. **Skip title rows**: most files have 4–5 title rows before the actual table.
3. **Column matching**: partial match against known header names.
4. **Merge by code**: collect from all files, deduplicate by code. APPEND new items, never wholesale replace.
5. **Handle merged cells**: unmerge before writing.
6. **Source field mapping**: code prefix → schedule name (see pattern below).

**Code prefix → Schedule mapping:**
- `FI_*`, `_CL_*`, `_WA_*`, `_FL_*` → "Finishes Schedule"
- `_SW_*` → "Setwork Schedule"
- `_SC_*` → "Showcase Schedule"
- `GR_*` → "Graphic Schedule"
- `WF_*` → "Wayfinding Schedule"
- `OB_*` → "Object Schedule"
- `FF_*` → "FF&E Schedule"
- `EX_*` → "Exhibit Schedule"
- `MD_*` → "Media Schedule"
- Plus Art Commission, Model, Mockup, Tactile, Space schedules.

### Hero / Welcome Page
- **Title**: "3D Visualization Presentation" (large Playfair Display)
- **Subtitle**: "Aseer Regional Museum of Art" (gold Inter uppercase)
- **Logo row**: MoC · PMC · CG · Samaya · NRS (32-38px logos, ~70% opacity)
- **Attribution**: "Technical Office · BIM Unit" on its own line below logos
- **No floating hotspots**: clean hero with loading fade transition.
- **Loading gate**: light background (#F5F1EB) with gold progress bar.

### Navigation
- Links: Gallery, Materials, Schedule (no Contact).
- Scroll-aware transparent-to-light header.
- Light background when scrolled: `rgba(245,241,235,0.95)`.

## Deploying to Production

### Surge.sh (quick preview)
```
cd dist && npx surge --project ./ --domain my-project.surge.sh
```

### Hostinger / PHP Web Host (production)
After building with `npm run build`:

1. **Copy sync.php** to dist: `cp /path/to/sync.php dist/sync.php`
2. **SCP to server** (ssh alias configured):
   ```bash
   tar czf /tmp/project.tar.gz -C dist .
   sshpass -p 'PASSWORD' scp -P 65002 /tmp/project.tar.gz USER@HOST:/home/USER/
   sshpass -p 'PASSWORD' ssh -p 65002 USER@HOST "\
     cd /home/USER/domains/example.com/public_html/build && \
     rm -rf appname && mkdir appname && cd appname && \
     tar xzf /home/USER/project.tar.gz && rm /home/USER/project.tar.gz && \
     chmod 755 sync.php"
   ```

3. **Image path fix when deploying to subdirectory**: If deployed at `/appname/` (not root), change all image paths from `/images/...` to `/appname/images/...`. Search for `'/images/'` in all `.tsx` files and update. Gallery data in `Gallery.tsx` and logo paths in `Hero.tsx` both need updating.

4. **Set SYNC_URL** in `hotspotStore.ts` to the deployment URL.

### SSH Config (Hostinger example)
```
Host samaya-factory
  HostName 92.113.28.250
  User u517606786
  Port 65002
  IdentityFile ~/.ssh/id_rsa
```

## Pitfalls

### 🔴 Hotspot pins must have `pointer-events: auto`
The most common bug: `.hotspot-pin-modal { pointer-events: none }` in CSS. This makes the onClick handler unreachable. The user will say "no pin to click on." Fix: `pointer-events: auto; cursor: pointer`.

### 🔴 Tooltip pinning via useRef, not useCallback state
When clicking a pin to freeze the tooltip, use a `useRef` (e.g., `clickedRef`) instead of relying on `useCallback` dependencies. The ref's `.current` value is always up-to-date in any closure, avoiding stale closure issues where the old event handler fires before React re-renders with new state.

Check pattern in Gallery.tsx:
```tsx
const clickedRef = useRef(false);
const handleMouseMove = useCallback((e) => {
  if (clickedRef.current) return;  // always reads latest value
  // ... rAF logic ...
}, [displayHotspots]);  // clickedRef is a ref — no dependency needed
```

### 🔴 Hotspot data wiped on every deploy
If `sync.php` stores data in `__DIR__ . '/hotspot-data/'`, and the deploy command does `rm -rf appname && mkdir appname`, the `hotspot-data/` directory is **deleted with all saved hotspots**. Fix: store outside the deploy directory:
```php
$dataDir = __DIR__ . '/../../hotspot-data';  // 2 levels up from /build/appname/
```

### 🔴 `.toLowerCase()` crashes on undefined fields
Many material items have `undefined` values for fields like `description`, `supplier`, `colour`, `category`. Calling `.toLowerCase()` on `undefined` throws a **TypeError that crashes React's render phase** — everything disappears silently.

**Safe filter pattern:**
```tsx
const safeFields = [m.code, m.description, m.supplier, m.colour, m.category];
const match = safeFields.some(f => f && f.toLowerCase().includes(q));
```
Apply this in EVERY filter function (schedule search, editor picker, admin panel).

### 🔴 RAL color regex must not match RAL Design codes
Standard RAL codes are 4 digits (e.g., RAL 7015). RAL Design codes use 7-digit format (e.g., RAL 040 40 30). A simple `\bRAL\s*(\d{4})\b` regex will match "RAL 0404" from "RAL 040 40 30" — producing an incorrect swatch for a non-existent RAL code.

**Safe regex:** `/\bRAL\s*(\d{4})(?!\d)/i` — the `(?!\d)` lookahead prevents matching the first 4 digits of a longer code.

### 🔴 Verify known codes after any data merge
When a subagent rebuilds `materials.json` (e.g., adding new schedule types like AV or Lighting), the merge script can corrupt `schedule_key` and `source` for ALL existing items, grouping them under "other." Before deploying, run:
```bash
python3 -c "
import json
with open('materials.json') as f: mats = json.load(f)
from collections import Counter
sched = Counter(m.get('schedule_key','?') for m in mats)
for k, v in sorted(sched.items()):
    print(f'{k}: {v}')
# Check known codes
for code in ['04.04_SW_01', 'FI_FL_01']:
    match = [m for m in mats if m.get('code') == code]
    print(f'{code}: {\"FOUND\" if match else \"MISSING\"} ({match[0].get(\"schedule_key\",\"\") if match else \"-\"})')
"
```
If known codes are missing or schedule_keys are "other," restore from backup and re-merge with APPEND-only logic.

### 🔴 Never fabricate data
If a source Excel file has no thumbnail/image column: **do not add one**. Do not generate placeholder images or extract images from PPTX schedule tables if they aren't in the original Excel data. If the user asks for thumbnails and none exist, tell them clearly rather than inventing a source.

### 🔴 Image paths when deploying to subdirectory
If the site is served from `https://domain.com/subdir/`, ALL image paths in the code must be `/subdir/images/...` not `/images/...`. This affects:
- Gallery view images (`Gallery.tsx`)
- Logo images on hero (`Hero.tsx`)
- Any other `src="/images/..."` references
Failing to update these will result in broken images (404s).

### 🔴 PHP sync.php permissions
After uploading `sync.php`, run `chmod 755 sync.php` on the server. The directory `hotspot-data/` will be created automatically by the script (PHP needs write permission to the parent directory).

### 🔴 Tar from macOS to Linux
`tar` on macOS adds Apple extended attributes (`._*` files). These are harmless on Linux but visible in `ls -la`. Use `COPYFILE_DISABLE=1 tar ...` or just ignore the `._*` files.

### 🔴 Smart tooltip must handle edge cases
Always implement edge-flip detection. Hardcoded offsets will clip at screen edges. Simple approach: `Math.max(10, Math.min(tx, window.innerWidth - cardW - 10))`.

### 🔴 Mousemove performance
Do NOT run distance calculation on every pixel event. Use:
```ts
if (Math.abs(dx) < 3 && Math.abs(dy) < 3) return;
rafRef.current = requestAnimationFrame(() => { ... });
```
When tooltip is pinned, the rAF callback returns immediately.

### 🔴 Editor z-index stacking
Editor overlay (`position: fixed; z-index: 300`) must be higher than modal backdrop. Add `onClick={e => e.stopPropagation()}` to the editor container to prevent click events reaching elements behind it during drag operations.

### 🔴 Save button always enabled
Editor save button must NOT be disabled. User should always be able to click save — persist current state regardless of whether it differs from original.

### 🔴 Schedule page pagination reset
When switching schedule tabs or searching, reset page to 0 with a `useEffect` on `[activeSchedule, searchQuery]`.

### 🔴 HotspotStore async
When `loadHotspots` and `saveHotspots` become async (due to server fetch), all callers must be updated:
- `useEffect` → wrap in `(async () => { ... })()`
- `useCallback` → make the callback `async`

### 🔴 Only show danger buttons on explicit request
Reset/Danger buttons (like "Reset to Defaults") must be hidden by default — only show when the user explicitly asks for them.

### 🔴 Never modify original schedule data
The Excel-extracted schedule JSON files are canonical. The app must never alter field names or values from the original. Only add metadata fields (`_source`, `schedule_key`) during merge. If data appears incorrect, verify against the source Excel — it's likely correct there.

## Color Scheme (Light/Formal Museum Theme)
- Background: `#F5F1EB` (warm off-white)
- Surface: `#EDE8E0` (light cream)
- Text: `#1A1D23` (dark charcoal)
- Muted: `#7E828A` (cool gray)
- Gold accent: `#C8A45C` (museum gold)
- Gold light: `#D4AF5A`
- Edit mode: `#4ADE80` (green)
- Danger: `#EF4444` (red)
- Borders: `rgba(26,29,35,0.1)`

## Admin UI Pattern (Editor)
```
┌──────────────────────────────────────┐
│ [VIEW | EDIT]  [× Close]            │
├──────────────────────────────────────┤
│                                      │
│   [image with numbered green pins]   │
│   Click to add · Click pin to edit   │
│   Drag to move · Hover × to delete  │
│                                      │
├──────────────────────────────────────┤
│      [💾 Save] [✕ Cancel] [📤] [📥]   │
└──────────────────────────────────────┘
```

## Admin UI Pattern (Password Prompt)
```
┌──────────────────────┐
│        🔐            │
│    Admin Access      │
│                      │
│  [password input]    │
│                      │
│      [Unlock]        │
│    [Back to site]    │
└──────────────────────┘
```
