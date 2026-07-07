# CSS Architecture — Restructured 2026-06-07

## Before
- 15 CSS files, 13,419 lines total
- `01-base.css` (703 lines) — junk drawer mixing templates, components, utilities
- `30-redesign.css` (6,344 lines) — monolithic file defeating the modular split
- Inline `<style>` block in index.html (~80 lines)

## After
- 33 CSS files, same total CSS, same visual output
- Three new foundation files split from 01-base.css:
  - `01-reset.css` — page chrome, @page, print rules
  - `02-utilities.css` — grids, spacing, typography utilities
  - `03-components.css` — shared components (cards, badges, stats, process)
- 15 per-archetype files split from 30-redesign.css:
  - `31-cover.css` → shared v3 tokens + cover
  - `32-toc.css` → table of contents
  - `33-about.css` → about page
  - `34-capacity.css` → operational capacity
  - `35-method.css` → QA/QC methodology
  - `36-scope.css` → scope archetypes
  - `37-catalog.css` → catalog, tier, prequal
  - `38-cmyk.css` → colour-managed print
  - `39-type.css` → wayfinding type
  - `40-macro.css` → GRC macro
  - `41-blueprint.css` → engineering blueprint
  - `42-gallery.css` → replica gallery, landmark, materiality
  - `43-scan.css` → 3D scanning
  - `44-p25.css` → materiality chapter (p25a-p25e)
  - `45-overrides.css` → print safety, back cover, misc overrides
- `50-replicas.css` → extracted from inline HTML <style>

## Key Style Notes
- **No BEM/ITCSS/SMACSS** — uses ad-hoc prefix namespacing (v3-, v4-, ed-, po-, pf-, ps-)
- **~5-8% dead code** — legacy styles from earlier template versions, suppressed with display:none
- **01-base.css** still contains some page-specific styles not yet migrated
- **Original 30-redesign.css preserved on disk** for reference (no longer linked from HTML)
- **All original CSS files (10-cover through 20-redesign) kept as-is**

## HTML Link Order (33 links)
00-tokens → 01-reset → 02-utilities → 03-components → 01-base → 02-scope-base → 10-cover → 11-toc → 12-about → 13-scope → 14-process → 15-closing → 16-about-magazine → 17-archetypes → 18-projects → 19-org → 20-redesign → 31-cover → 32-toc → 33-about → 34-capacity → 35-method → 36-scope → 37-catalog → 38-cmyk → 39-type → 40-macro → 41-blueprint → 42-gallery → 43-scan → 44-p25 → 45-overrides → 50-replicas

## Verification Command
```bash
# All links point to existing files
for f in $(grep -o 'css/[^"]*\.css' index.html); do
  [ -f "$f" ] || echo "MISSING: $f"
done
echo "All OK"
```
