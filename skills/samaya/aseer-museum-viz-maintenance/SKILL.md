---
name: aseer-museum-viz-maintenance
description: Maintain the Aseer Museum visualization app (samaya-factory.com/aseer/) — add gallery sections, deploy only changed files, fix image issues.
category: samaya
triggers:
  - "aseer museum viz"
  - "add gallery section"
  - "deploy aseer"
  - "aseer images"
  - "samaya-factory.com/aseer"
---

# Aseer Museum Viz App Maintenance

## Repo
- GitHub: `sultandroid/aseer-museum-viz` (private)
- Local clone: `/tmp/aseer-museum-viz`
- Live: `samaya-factory.com/aseer/`

## Adding New Gallery Sections

### DO NOT redesign
- Only append new entries to the `galleryData` array in `src/sections/Gallery.tsx`
- Never change the component structure, CSS, or layout
- Never add floor section headers or grouping to the UI — the original design is a flat grid

### Gallery entry format
```typescript
{id:'g7', floor:'basement', title:'G7 – Contemporary Art Commission: Reem Alnasser', views:[
  {viewName:'G7_View_1', filename:'/aseer/images/bf_VIS13.jpg', desc:'View – Art commission installation', hotspots:[]},
]},
```

### Floor classification (from NRS folder names)
| floor value | NRS folder | VIS range |
|-------------|------------|-----------|
| `'basement'` | `0_BASEMENT` | VIS001–VIS016 |
| `'lower-ground'` | `1_LOWER GROUND FLOOR` | VIS017–VIS020 |
| `'ground'` | `2_Ground Floor` | VIS021–VIS025 |

### Image naming convention
- Upload NRS JPGs renamed to: `{floor_prefix}_VIS{number}.jpg`
- Floor prefixes: `bf_` (basement), `lgf_` (lower ground), `gf_` (ground)
- Image path in code: `/aseer/images/{filename}`

## Deploying (only changed files)

### 1. Build
```bash
cd /tmp/aseer-museum-viz
npm run build
```

### 2. Upload new images to server
```bash
# Upload only new images (not the whole app)
scp -P 65002 /path/to/new/image.jpg u517606786@samaya-factory.com:/home/u517606786/domains/samaya-factory.com/public_html/build/aseer/images/
```

### 3. Fix permissions (images get 700 from scp — must be 644)
```bash
ssh -p 65002 u517606786@samaya-factory.com "chmod 644 /home/u517606786/domains/samaya-factory.com/public_html/build/aseer/images/*.jpg"
```

### 4. Deploy only built assets (JS/CSS + index.html)
```bash
cd /tmp/aseer-museum-viz/dist
tar czf /tmp/aseer-assets.tar.gz index.html assets/
scp -P 65002 /tmp/aseer-assets.tar.gz u517606786@samaya-factory.com:/home/u517606786/
ssh -p 65002 u517606786@samaya-factory.com "cd /home/u517606786/domains/samaya-factory.com/public_html/build/aseer && tar xzf /home/u517606786/aseer-assets.tar.gz && rm /home/u517606786/aseer-assets.tar.gz"
```

### 5. Verify
```bash
curl -sI https://samaya-factory.com/aseer/ | head -3
curl -sI https://samaya-factory.com/aseer/images/bf_VIS13.jpg | head -3
```

## Pitfalls
- **Images get 700 permissions** from scp → 403 Forbidden. Always chmod 644 after upload.
- **Do not redeploy the whole app** — only `index.html` + `assets/` + new images. The old images stay on the server.
- **Do not change the component design** — only add data entries. The user will correct you if you restructure the UI.
- **Floor classification** must match the NRS folder names exactly (0_BASEMENT, 1_LOWER GROUND FLOOR, 2_Ground Floor), not your own labels.
- **VIS number mapping** comes from the location plan PDFs in `1210 - Visualisation Location Plans/` — check those before guessing which VIS belongs to which gallery.
- **Gallery titles** should match the NRS plan labels (e.g. "G5 – Making Space", not "G5 – Children's Room").
- **Build errors** from pre-existing issues (type imports, postcss config) need fixing before deploy — check `npx tsc --noEmit` first.
