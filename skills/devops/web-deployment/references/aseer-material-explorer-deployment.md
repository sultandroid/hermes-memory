# Aseer Material Explorer — Deployment Details

## Project Location

**Source:** OneDrive (may reorganize — paths below are current)

```bash
# Path as of June 2026 (post-reorg):
~/Library/CloudStorage/OneDrive-SAMAYAINVESTMENT/Samaya/Technical Office/Bim Unit/Aseer-Museum/14_Completed_Tender_Package_From_NRS/07_Visualizations/Kimi_Agent_Interactive 3D Material Showcase/app/

# Prior path (may reappear after OneDrive re-sync):
~/Library/CloudStorage/OneDrive-SAMAYAINVESTMENT/Samaya/Technical Office/Bim Unit/Aseer-Museum/Completed Tender Package From NRS/07_Visualizations/Kimi_Agent_Interactive 3D Material Showcase/app/
```

⚠️ **OneDrive path re-org:** The parent folder changed from `Completed Tender Package From NRS` to `14_Completed_Tender_Package_From_NRS`. If `ls` fails on the expected path, search with `mdfind`:
```bash
mdfind "kMDItemFSName == 'Gallery.tsx'" | grep -v node_modules | head -3
```

### Symlink Fix (public/aseer/images)

When OneDrive reorganizes, the symlink at `public/aseer/images` breaks (points to old absolute path). Fix:

```bash
APP="<project/app path>"
rm "$APP/public/aseer/images"
ln -s "../images" "$APP/public/aseer/images"
# Verify: ls -la "$APP/public/aseer/" shows a working relative symlink
```

The symlink should be **relative** (`../images` → `public/images/`), not absolute, so it survives OneDrive path changes.

## Server Access

| Field | Value |
|-------|-------|
| Host | `samaya-factory.com` (not raw IP — IP blocks SSH) |
| Port | `65002` |
| User | `u517606786` |
| Web root | `/home/u517606786/domains/samaya-factory.com/public_html/build/aseer/` |
| Image dir | `/home/u517606786/domains/samaya-factory.com/public_html/build/aseer/images/` |
| Hotspot data | `/home/u517606786/domains/samaya-factory.com/public_html/hotspot-data/` (outside deploy dir) |
| Auth | SSH key (passphrase-less, `BatchMode=yes` works) |

## SSH Commands

```bash
# Upload file
cat /local/file.jpg | ssh -p 65002 -o BatchMode=yes u517606786@samaya-factory.com "cat > /remote/path/file.jpg"

# Run remote command
ssh -p 65002 -o BatchMode=yes u517606786@samaya-factory.com "ls /remote/path/"

# Deploy tar
cat /tmp/deploy.tar.gz | ssh -p 65002 -o BatchMode=yes u517606786@samaya-factory.com "cat > /home/u517606786/deploy.tar.gz"
ssh -p 65002 -o BatchMode=yes u517606786@samaya-factory.com "cd /web/root && tar xzf /home/u517606786/deploy.tar.gz && rm -f /home/u517606786/deploy.tar.gz"
```

**Note:** SCP often hangs on this host — always use SSH pipe instead.

## Build

```bash
cd "$APP" && node node_modules/vite/bin/vite.js build
# Then copy sync.php:
cp sync.php dist/sync.php
```

## Technical Proposals Subfolder

A new folder was created for housing technical proposals at:
`/home/u517606786/domains/samaya-factory.com/public_html/build/technical-office/Technical-Proposals/`

Each proposal gets its own subfolder with an `index.html`:

```bash
# Create project folder
ssh -p 65002 -o BatchMode=yes u517606786@samaya-factory.com \
  "mkdir -p /home/u517606786/domains/samaya-factory.com/public_html/build/technical-office/Technical-Proposals/PROJECT-NAME/"

# Upload
cat /local/index.html | ssh -p 65002 -o BatchMode=yes u517606786@samaya-factory.com \
  "cat > /home/u517606786/domains/samaya-factory.com/public_html/build/technical-office/Technical-Proposals/PROJECT-NAME/index.html"
```

**Current proposals:**
- `RCRC-Exhibition/` — RCRC Exhibition Technical Proposal (bilingual AR/EN)
  - URL: `https://samaya-factory.com/build/technical-office/Technical-Proposals/RCRC-Exhibition/index.html`

## OneDrive + Git Operations

When working with files on OneDrive, git operations (init, add, commit) can time out due to OneDrive's sync overhead. **Workaround**: copy files to `/tmp/`, run git there, push from `/tmp/`:

```bash
cp /path/to/file /tmp/work-dir/
cd /tmp/work-dir
git init && git add -A && git commit -m "message"
git branch -m main
gh repo create org/repo-name --private --source=. --remote=origin --push
```

The `/tmp/` version becomes the authoritative git source. If needed later, clone from GitHub back to OneDrive.

## Gallery Structure

Gallery views are defined in `src/sections/Gallery.tsx` in the `galleryData` array. Each entry has:
- `id` — short code (g4, g6, g8, g9, g11, g12, lb3, g5, g1, g3, lb2, tg)
- `title` — display name
- `views` — array of `{viewName, filename, desc, hotspots}`

Image naming: short readable names like `g4_G4_View_1.jpg`, `lgf_vis017.jpg` (not full MoC codes).

### Current Galleries (June 2026)

| ID | Title | Views | Floor |
|----|-------|-------|-------|
| g4 | G4 – Saudi Art | 2 | Basement |
| g6 | G6 – Saudi Art | 3 | Basement |
| g8 | G8 – Al Qatt | 2 | Basement |
| g9 | G9 – Flowersmen | 1 | Basement |
| g11 | G11 – Scripts | 2 | Basement |
| g12 | G12 – Archaeology | 3 | Basement |
| lb3 | LB3 – Link Bridge | 2 | Basement |
| g5 | G5 – Children's Room | 1 | Basement |
| g1 | G1 – Welcome Gallery | 1 | LGF |
| g3 | G3 – Al Muftaha | 1 | LGF |
| lb2 | LB2 – Lobby | 1 | LGF |
| tg | TG – Temporary Gallery | 1 | LGF |

## Adding New Photos

### 1. Upload images to server
Use short readable server filenames — the full MoC codes are unwieldy in the source.

```bash
cat /path/to/photo.jpg | ssh -p 65002 -o BatchMode=yes u517606786@samaya-factory.com \
  "cat > /home/u517606786/domains/samaya-factory.com/public_html/build/aseer/images/lgf_vis017.jpg"
```

### 2. Add gallery entries in Gallery.tsx
```typescript
// New gallery entirely:
{id:'lgf', title:'LGF – Lower Ground Floor', views:[
  {viewName:'LGF_View_1', filename:'/aseer/images/lgf_vis017.jpg',
   desc:'View 1 – Name',
   hotspots:[{code:'MAT_CODE',x:50.0,y:50.0}]},
]},

// New view in existing gallery:
{viewName:'G4_View_3', filename:'/aseer/images/g4_new_view.jpg',
 desc:'View 3 – Updated view',
 hotspots:[{code:'FI_FL_04',x:50.0,y:88.0}]},
```

### 3. When hotspot data isn't ready
Create entries with empty hotspots `[]` — user adds pins later via admin panel (`?admin=1`, password: `aseer2026`). The hotspot editor allows drag-and-drop positioning.

### 4. Hotspot preservation when replacing photos

**Best approach — same filename, same path:**
Upload the new image to the **exact same server path** as the old one. The `filename` in `Gallery.tsx` doesn't change — only the file content on disk changes. Hotspot positions (percentage-based x,y) remain valid because the image aspect ratio/viewpoint stays the same.

```bash
# Replace existing photo — same filename on server, no code change needed
cat /path/to/VIS001.jpg | ssh -p 65002 -o BatchMode=yes u517606786@samaya-factory.com \
  "cat > /home/u517606786/domains/samaya-factory.com/public_html/build/aseer/images/g4_G4_View_1.jpg"
```

**Alternative — new filename:**
If the image has a different name, update the `filename` path in `Gallery.tsx` but **keep the `hotspots` array unchanged.** The hotspot coordinates are relative (x%, y%) and work with any image of the same viewpoint.

### Cache-Busting Image Version

After replacing photos on the same server path, old browser cache shows stale images. Use a version constant:

```typescript
const IMG_VERSION = '2'; // bump when replacing photos

// In JSX:
<img src={`${view.filename}?v=${IMG_VERSION}`} alt={view.desc} />
```

Increment the constant on each batch of photo replacements. All images get `?v=N` appended, bypassing cache.

### Submission Reference Badge (`subRef`)

Each view can carry a `subRef` field with the full MoC submission code. The server filename stays short while the UI shows the formal reference:

```typescript
{viewName:'G4_View_1', filename:'/aseer/images/g4_G4_View_1.jpg',
 subRef:'MOC-ASE-AR-ARC-BF-DDD-VIS001', desc:'Main gallery hall overview',
 hotspots:[...]}
```

Rendered as a gold badge in the sidebar. Omit `subRef` to show no badge.

### 5. Updating view description
After replacing a photo, update the `desc` field to show the new reference:
```typescript
// Before
desc:'View 1 – Main gallery hall overview',
// After
desc:'VIS001 – Main gallery hall overview',
```

## Visualization Location Plans

New DD photos come with MoC location plan PDFs showing which gallery/room each VIS number belongs to:
```
.../DD_Package_26Jun2026/1210 - Visualisation Location Plans/
  MOC-ASE-AR-ARC-BF-DDD-1210-00.pdf   ← Basement floor
  MOC-ASE-AR-ARC-LGF-DDD-1211-00.pdf  ← Lower Ground Floor
```

### Extracting VIS-to-Gallery mapping from floor plans

Floor plans are dense technical drawings. `pdftotext` captures partial labels — enough to build a mapping table:

```bash
# Convert PDF to text
pdftotext -layout "MOC-ASE-AR-ARC-BF-DDD-1210-00.pdf" /tmp/bf_vis.txt

# Find all VIS references
grep -o 'VIS[0-9][0-9][0-9]\|MOC-ASE-AR-ARC-BF-DDD-VIS[0-9][0-9][0-9]' /tmp/bf_vis.txt | sort -u

# Context around each VIS
grep -n -B 15 -A 5 "VIS013" /tmp/bf_vis.txt
# Look for gallery labels (G4, G8, G12, etc.) near the VIS number
```

**Limitations:**
- Only ~20-30% of VIS labels are captured by text extraction (labels overlaid on dense hatch patterns)
- Full labels like `MOC-ASE-AR-ARC-BF-DDD-VIS011` appear completely; truncated ones like `VIS0` are partial captures
- For full coverage, convert to image and examine visually: `pdftoppm -png -r 150 input.pdf /tmp/output.png`
- Results are best-effort — confirm mapping with the user before replacing files

## Tooltip Card — Schedule Field Groups & Redesign

The info card (hover/pin tooltip) uses `SCHEDULE_FIELD_GROUPS` in `Gallery.tsx` to define which fields appear per schedule type. Configuration is a `Record<string, { label: string; fields: FieldDef[] }[]>`.

To remove a field from the card (e.g. "Exhibit Name" from setwork/showcase), delete its entry from the `fields` array in the config. Rebuild and deploy.

### Card Redesign (CSS)

The tooltip card CSS lives in `src/index.css` under `.hotspot-tooltip-card` and related `.htc-*` classes. When redesigning:

- Card width: `360px` (was 340px)
- Uses `::before` pseudo-element for gold accent bar at top
- Group sections have subtle background (`rgba(200,164,92,.04)`)
- Fields use dark label text over the old `opacity` approach for better readability
- `overflow-y: auto` for tall content
- Remove `backdrop-filter` for better performance on older machines

### Schedule Field Groups Reference

The following schedule keys have defined field groups:

| Schedule Key | Groups | Fields |
|---|---|---|
| `setwork_schedule` | Setwork, Details | ID, Type, Exhibition ID, Description, Finishes, Drawing Ref |
| `showcase_schedule` | Showcase, Display | Type, ID, Glass Sides, AR Coating, Lighting, Climate |
| `graphic_schedule` | Graphic, Specifications, Details | ID, Type, Gallery, Exhibit ID, Height/Width, Substrate, Print Method, Description, Qty |
| `wayfinding_schedule` | Wayfinding, Specifications, Materials | ID, Type, Floor, Gallery, Description, Height/Width, Substrate, Print Method, Qty |
| `ff_e_schedule` | FF&E Item, Details | ID, Space, Finish, Qty, Bespoke Qty, Supplier, Dimensions, Notes |
| `finishes_schedule` | Material, Specifications | ID, Component, Finish, Colour, Description, Supplier |
| `av_equipment_schedule` | Equipment Info, Specifications | ID, Ref, Description, Product, Category, Qty, Dimensions, Power, Voltage, Zone |
| `lighting_schedule` | Fixture Info, Lamp Specs, Installation | ID, Description, Manufacturer, Drawing Ref, Size, Type, Lamp, Wattage, Lumens, CCT, CRI, Beam Angle, Room, Floor, Mounting, Qty, IP Rating, Dimming, Finish, Notes |

**Note:** "Exhibit Name" was removed from setwork/showcase per user request — the NRS data has gallery theme names (e.g. "Landscape", "Architecture & Landscape") that confused stakeholders when shown as "Exhibit" in the tooltip.

## Deploy Diagram

```
Source (OneDrive) → Vite build → dist/
  ├── index.html
  ├── assets/index-<hash>.js
  ├── assets/index-<hash>.css
  ├── sync.php (copy manually)
  └── images/ (on server only, not in dist/)

Deploy to server: tar changed files → SSH pipe → extract → remove old bundles
```

## Incremental Deploy Template

```bash
APP="/path/to/app"
cd "$APP"
node node_modules/vite/bin/vite.js build
cp sync.php dist/sync.php

NEW_JS=$(ls dist/assets/index-*.js | xargs basename)
NEW_CSS=$(ls dist/assets/index-*.css | xargs basename)

cd dist
tar czf /tmp/deploy.tar.gz index.html "assets/$NEW_JS" "assets/$NEW_CSS" sync.php
cat /tmp/deploy.tar.gz | ssh -p 65002 -o BatchMode=yes u517606786@samaya-factory.com "cat > /tmp/deploy.tar.gz"

ssh -p 65002 -o BatchMode=yes u517606786@samaya-factory.com "
  cd /home/u517606786/domains/samaya-factory.com/public_html/build/aseer
  tar xzf /tmp/deploy.tar.gz
  rm -f /tmp/deploy.tar.gz
  rm -f assets/._*
  # Remove old bundles
  for f in assets/index-*.js; do
    grep -q \"\$f\" index.html || rm -f \"\$f\"
  done
  for f in assets/index-*.css; do
    grep -q \"\$f\" index.html || rm -f \"\$f\"
  done
"
```

## Admin Panel

Append `?admin=1` to the site URL. Password: `aseer2026`.
Allows hotspot editing, material management. Use when user can't provide hotspot coordinates — create placeholder views with `hotspots:[]` and let them fill in via the panel.

## Print PDF Feature

The site had a "🖨️ Print PDF" button in the gallery modal sidebar that triggered `window.print()` with a 3-page A4 layout (clean photo, annotated pins, material legend). Code in `PrintView.tsx` (still present in source but unreachable).

**Removed per client request** — button element and its `onClick` handler deleted from `Gallery.tsx`. The `PrintView` component and its import remain in source (harmless dead code).

If re-enabling is needed later: uncomment the button JSX block in the `modal-sidebar-panel` section of `Gallery.tsx`.
