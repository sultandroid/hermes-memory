# Samaya Factory Profile Website

Conventions and workflows for the Samaya Factory profile website deployed at
`samaya-factory-profile.surge.sh`.

## Project Structure

- **Root:** `…/Technical Office/samaya-profile/v6/`
- **Assets:** `…/assets/img/projects/` (outside v6)
- **HTML:** `v6/index.html` (single-page A4 print profile)
- **CSS:** `v6/css/30-redesign.css`, `v6/css/18-projects.css`, `v6/css/17-archetypes.css`
- **Source photos:** `…/Samaya/Orders/2025/00000 صور واتساب سنة 2025 الورشة/`

## Core Rules

### Replace photos in-place — never add new blocks
Edit existing `.pmat-cell`, `.v4-tier-tile`, `.v4-type-fam-img` etc. **Never**
inject new containers, gallery rows, or sections unless the user explicitly
says "add".

### Delegate design/layout/text to Claude Code CLI
Any HTML/CSS redesign, text rewrite, or layout restructure must go through
`delegate_task`. Do not write new CSS blocks or rewrite long text passages
yourself.

### Overflow → multi-page OK
Remove `overflow: hidden` and fixed `height` on `.content` so content flows
naturally to the next page. Do not shrink content to fit.

### Materiality grid
- Images: `height: 48mm`, `background-size: cover`
- Grid: `grid-auto-rows: auto` (not `1fr`)
- Equipment photos: `background-size: contain`

### Wayfinding
Use **finished installed signage** photos, not workshop fabrication photos.

### Surge deploy
Full rebuild from v6/. Asset path rewrite `../assets/` → `assets/`. Always
verify with `curl | grep` after deploy. Use `?t=$(date +%s)` cache-bust.

### Gallery curation
Pick the **best 6–9** most important photos. Remove weaker duplicates.
