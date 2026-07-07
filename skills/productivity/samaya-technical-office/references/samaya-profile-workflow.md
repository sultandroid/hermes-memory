# Samaya Factory Profile — Workflow & Conventions

## Project Location
`/Users/mohamedessa/Library/CloudStorage/OneDrive-SAMAYAINVESTMENT/Samaya/Technical Office/samaya-profile/v6/`

## Deployment
- Domain: `samaya-factory-profile.surge.sh`
- Deploy from `/tmp/samaya-profile-deploy/` after copying HTML + CSS + resolving `../assets/` → `assets/`
- Auth: `mohamedsultanabbas@gmail.com`
- Verify deploy with `curl -sL https://samaya-factory-profile.surge.sh/` and check for changed strings
- CDN may serve stale — append `?t=$(date +%s)` cache-buster

## Design Rules (CRITICAL)
1. **Cover slogan is SACRED** — "صناعة الإرث. هندسة الفنّ." / "Crafting Legacy. Engineering Art." Never change.
2. **Delegate design/HTML/CSS to Claude** — use `delegate_task` to Claude Code for any layout, text, or visual redesign. Do not do it directly.
3. **Replace photos in-place** — never add new HTML blocks or sections unless explicitly told to. Swap `background-image` URLs only.
4. **Materiality & Craft grid**: `background-size: contain` (NOT `cover`), `background-repeat: no-repeat`, multi-page overflow OK.
5. **Page overflow**: remove `height: calc(210mm - 22mm - 14mm)` + `overflow: hidden` on `.content` divs. Use `flex: 1` with fixed parent height instead.
6. **QR code**: must be inline beside text (flex row), not stacked below.
7. **TOC update**: always check and update TOC page (`id="p2"`) when sections are added, removed, or renumbered.
8. **`write_file` DESTROYS entire files** — never use it on existing multi-file projects. Always use `patch()` for targeted edits.

## Photo Workflow
- Source photos: `OneDrive/.../Orders/2025/00000 صور واتساب سنة 2025 الورشة/` or `Downloads/Production/`
- Copy to: `assets/img/projects/<section>/`
- Compress large RAW photos (15MB+) to max 2000px wide using `sips -Z 2000`
- Captions: bold EN name + AR description

## Key Sections & Their Pages
| Section | Page ID | Notes |
|---------|---------|-------|
| Cover | p1 | Slogan never change |
| TOC | p2 | Update when pages change |
| Operational Capacity | p4 | Factory hero + stats + pipeline |
| Comprehensive Scope | p5 | 6-scope index with dual hero photos |
| FF&E | p7-8 | Furniture specimens |
| Finishings & Scenography | p9-11 | Mosaic tile grid |
| Museum Vitrines | p12 | 4-column spec comparison |
| Replicas & Models | p13 | 3-tier grades + 3D scanning |
| Replica Works Gallery | p13b | Curated to 6-9 best photos — no multi-page for gallery |

### Photo curation rule

When the Replica Works Gallery (p13b) overflows A4 with 10+ photos, curate to fit ONE page. Pick the best 6 (2 rows of 3) most representative/impressive photos. Remove weaker duplicates. Delegate curation to Claude.

### China Treasures / Exhibition Photo Mapping

When the user provides a folder of exhibition photos for the DISPLAY & EXPERIENCE SYSTEMS page (p12):
1. Copy to `assets/img/projects/<exhibition-name>/`
2. Compress: `sips -Z 2000` (reduce 15MB RAW → ~500KB)
3. Analyze photos using vision (or Pillow image metrics as fallback) to identify vitrine type
4. Map to correct column in the 4-col vitrine grid
5. Update `background-image` URL + `aria-label` in each column
6. Leave spec tables unchanged
| Graphics/Wayfinding | p14-15 | Print + wayfinding systems |
| Engineering & BIM | p18 | 4-stage pipeline |
| Flagship Projects | p23-24 | 5 alternating hero layouts |
| Materiality & Craft | p25-28 | 4-column grid, multi-page |
| HSE / Approvals / After-Sales | p29-31 | Editorial spreads |
| Back Cover | p27 | QR inline with contact text |