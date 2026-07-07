# Samaya Factory Profile — Website Management

## Overview
The Samaya Factory Profile is a bilingual (AR/EN) A4 landscape print-style website deployed at **samaya-factory-profile.surge.sh**. Source lives in OneDrive under `Samaya/Technical Office/samaya-profile/v6/`.

## Key Pages

| ID | Section | Content |
|----|---------|---------|
| p4 | OPERATIONAL CAPACITY | Stats + pipeline + tech stack |
| p5 | COMPREHENSIVE SCOPE | Hero with side-by-side photos |
| p13 | SCOPE 04 · REPLICAS & MODELS | 3-tier fidelity grid + 3D scanning methodology |
| p13b | REPLICA WORKS GALLERY | 6 best replica photos (3×2 grid) |
| p14 | GRAPHICS · WAYFINDING · AV (p15 is continuation) | CMYK print scope |
| p15 | WAYFINDING SYSTEM | Hero spec + 3 sign families |
| p18 | ENGINEERING & TECHNICAL METHODOLOGY | 4-stage pipeline (BIM → SD → CNC → Assembly) |
| p20 | APPROVALS · TESTING · HANDOVER | 5-step approval flow |
| p22 | AFTER-SALES SUPPORT | Maintenance cycle + dispatch photos |
| p27 | Back cover | QR code + contact info |

## Workflow Rules

### Photo Sourcing
- Source folders: `Downloads/`, `Downloads/Production/`, WhatsApp temp under `Containers/net.whatsapp.WhatsApp/Data/tmp/documents/`
- Workshop folder: `OneDrive/Orders/2025/00000 صور واتساب سنة 2025 الورشة/classified/website-ready/`
- Copy to: `assets/img/projects/<section-name>/<descriptive-name>.jpg`

### Design/Content Changes
- **Always delegate to Claude** — do NOT edit HTML/CSS or write text directly unless it's a trivial one-line path change
- Say "use Claude for design" or "play with text using Claude" triggers the delegation
- Replace existing photos in-place; do NOT add new blocks/sections unless the user explicitly asks
- For page overflow: remove `overflow: hidden`, use `grid-auto-rows: auto`, set fixed `height` on images

### Caption Format
- English in bold + Arabic after: `**CAPTION EN** · وصف بالعربية`
- Example: `**KAABA DOOR · SITE INSTALLATION** · باب الكعبة — التركيب في الموقع`

### Deploy
```bash
rm -rf /tmp/samaya-profile-deploy && mkdir -p /tmp/samaya-profile-deploy
cp index.html /tmp/samaya-profile-deploy/
cp -R css/ /tmp/samaya-profile-deploy/css/
python3 -c "p='/tmp/samaya-profile-deploy/index.html';c=open(p).read();c=c.replace('../assets/','assets/');open(p,'w').write(c)"
python3 copy_assets2.py
cd /tmp/samaya-profile-deploy && surge --project ./ --domain samaya-factory-profile.surge.sh
```

### Surge Auth
- Email: mohamedsultanabbas@gmail.com
- Login via PTY mode: `surge login` with PTY enabled, send email then password interactively
- If `surge logout` was run, re-login is needed before any deploy

### Verification
- After deploy, verify with: `curl -sL "https://samaya-factory-profile.surge.sh/" | grep 'changed-string'`
- Add `?t=$(date +%s)` cache-buster if CDN is stale
- Check the live preview URL too

### Materiality Grid
- 48mm image height in 4-column grid with `grid-auto-rows: auto`
- Multi-page overflow OK (removed `overflow: hidden`)
- Footer count should match actual cell count

### Replicas Gallery (p13b)
- Curated to 6 best photos in a 3-column grid (2 rows)
- Photos must show actual replica/installation work, not fabrication process

## Common Pitfalls
- **Don't add new blocks** unless user explicitly says "add" — default is replace
- **Don't design/edit text directly** — use Claude via delegate_task
- **Don't forget the path fix**: `../assets/` → `assets/` in deploy HTML copy
- **Don't use cover on grid images** where contain is better (or vice versa — ask user preference)
- **Surge CDN serves stale for seconds** — verify with cache-bust parameter
