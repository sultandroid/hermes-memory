---
name: samaya-factory-profile
description: Maintain and update the Samaya Factory profile website — photo management, layout fixes, page overflow/balance, Surge.sh deployment.
tags: [samaya, profile, website, surge, a4-layout]
---

# Samaya Factory Profile Website

⚠️ AMBIGUOUS NAME — This skill name `samaya-factory-profile` collides with a reference file under `samaya-technical-office/references/`. Use the **categorized path** to load it: `skill_view(name='productivity/samaya-factory-profile')` or `skill_view(name='productivity/samaya-factory-profile/SKILL.md')`. The bare name `samaya-factory-profile` will fail with an ambiguity error.

## Project Location
`/Users/mohamedessa/Library/CloudStorage/OneDrive-SAMAYAINVESTMENT/Samaya/Technical Office/samaya-profile/v6/`

## CSS Architecture (33 files, restructured 2026-06-07)

```
v6/css/
├── 00-tokens.css           Design tokens + CSS variables
├── 01-reset.css            Page chrome (header, footer, .content), @page, print
├── 02-utilities.css         Grid helpers, spacing, typography utilities
├── 03-components.css        Shared: cards, badges, stats, process, quote, evidence
├── 01-base.css              Reduced: page-specific legacy styles
├── 02-scope-base.css        Scope-detail styles
├── 10-cover.css             Cover (editorial v1)
├── 11-toc.css               Table of Contents (editorial v2)
├── 12-about.css             About page (v2, v3)
├── 13-scope.css             Scope utilities, catalog, products
├── 14-process.css           Process page primitives
├── 15-closing.css           Closing pages
├── 16-about-magazine.css    About v5 magazine spread
├── 17-archetypes.css        Archetype layout shells
├── 18-projects.css          Project history, timeline, flagship, map
├── 19-org.css               Org chart SVG styles
├── 20-redesign.css          .ed- page overrides
├── 31-cover.css → 45-overrides.css   Per-archetype CSS (split from 30-redesign.css)
└── 50-replicas.css          Extracted from HTML <style>
```

Style notes:
- **No BEM/ITCSS** — uses ad-hoc prefix namespacing per file (v3-, v4-, ed-, po-, pf-, ps-)
- **30-redesign.css was a monolith** (6,344 lines) now split into 31–45 per-archetype files
- **Dead code exists** (~5-8%) — legacy styles suppressed with display:none
- **01-base.css was a junk drawer** — split into 01-reset, 02-utilities, 03-components
- All CSS variable references use `--v3-` prefix in 31-cover.css shared tokens

### Known Dead CSS (recurring maintenance)
- **`:where(.page)` in 31-cover.css** — The rule `:where(.page) { background: var(--v3-paper); }` appears to set all pages to cream but has **zero CSS specificity** (0,0,0), so the base `.page { background: var(--paper) }` (specificity 0,1,0) always beats it. The v3/v4 pages only get cream because their explicit class selectors override. Remove this `:where()` rule on sight — it's dead code that misleads new agents into thinking cream is universal when it isn't.

## Deployment
Surge.sh at `samaya-factory-profile.surge.sh`. Auth stored via `surge login` (email: mohamedsultanabbas@gmail.com).

## Surge Auth Handling

Credentials: mohamedsultanabbas@gmail.com. **Never run `surge logout`** — it deletes the .netrc token and requires the user's password to re-authenticate. To re-login if broken: use `terminal(background=true, pty=true)` then `process(action="submit", data="email")` then `process(action="submit", data="password")`.

Deploy sequence:
```bash
rm -rf /tmp/samaya-profile-deploy && mkdir -p /tmp/samaya-profile-deploy/css
v6="/Users/mohamedessa/Library/CloudStorage/OneDrive-SAMAYAINVESTMENT/Samaya/Technical Office/samaya-profile/v6"
cp "$v6/index.html" /tmp/samaya-profile-deploy/index.html
cp "$v6/css/"*.css /tmp/samaya-profile-deploy/css/
# Fix relative asset paths (../assets/ → assets/)
sed -i '' 's|../assets/|assets/|g' /tmp/samaya-profile-deploy/index.html
# Copy all referenced assets (use Python script, see Pre-Deploy Image Verification)
cd /tmp/samaya-profile-deploy && surge --project ./ --domain samaya-factory-profile.surge.sh
```

### Pre-Deploy Image Verification (MANDATORY)

Before running `surge`, verify ALL image references in the deploy HTML resolve to actual files:

```python
import re, os
with open("/tmp/samaya-profile-deploy/index.html") as f:
    html = f.read()
paths = set()
for m in re.findall(r"url\('([^']+)'\)", html):
    paths.add(m)
missing = []
for p in sorted(paths):
    full_path = os.path.join("/tmp/samaya-profile-deploy", p)
    if not os.path.exists(full_path):
        missing.append(p)
print(f"Total: {len(paths)}, Missing: {len(missing)}")
for m in missing: print(f"  MISS: {m}")
```

**Expected**: `Missing: 0`. If any files are missing:
- Check if they exist in the old `samaya-web/assets/` directory and need migration
- Check if they use non-standard path patterns (see Stale Path Check)
- Copy them from source before proceeding

### Stale Path Check (pre-deploy)

Scan for old path patterns that survived previous migrations:

```bash
# Old samaya-web structure (pre-v6.3 reorganization)
grep -c 'samaya-web' /tmp/samaya-profile-deploy/index.html
# Expected: 0. If >0, fix with:
sed -i '' 's|../samaya-web/assets/|assets/|g' /tmp/samaya-profile-deploy/index.html

# Stale samaya-wassets (from corrupted deploy builds)
grep -c 'samaya-wassets' /tmp/samaya-profile-deploy/index.html
# Expected: 0. If >0, fix with:
sed -i '' 's|../samaya-wassets/|assets/|g' /tmp/samaya-profile-deploy/index.html
```

### Non-Standard Image Path Handling

**China Treasures Exhibition** photos in #p12 (Display/Vitrines) use inline `url('مشاريع سمايا/معرض كنوز الصين/...')` paths — these are NOT caught by `sed ../assets/ → assets/` because they don't contain `../assets/`.

**Fix**: Copy the China Treasures photos to the deploy dir from the source:
```bash
V6="/Users/mohamedessa/Library/CloudStorage/OneDrive-SAMAYAINVESTMENT/Samaya/Technical Office/samaya-profile/v6"
mkdir -p "/tmp/samaya-profile-deploy/مشاريع سمايا/معرض كنوز الصين"
cp "$V6/مشاريع سمايا/معرض كنوز الصين/"* "/tmp/samaya-profile-deploy/مشاريع سمايا/معرض كنوز الصين/" 2>/dev/null
```

**Long-term fix**: Migrate these to `assets/img/07-projects/china-treasures-*.jpg` in the source HTML so they follow the standard `../assets/img/...` pattern.

### OneDrive Copy Fidelity

The source files live on OneDrive, which uses "Files On-Demand" — `cp` may receive a stale placeholder instead of the current file content.

**After copying, verify**:
```bash
md5 "/Users/mohamedessa/Library/CloudStorage/OneDrive-SAMAYAINVESTMENT/Samaya/Technical Office/samaya-profile/v6/index.html"
md5 /tmp/samaya-profile-deploy/index.html
```
If hashes differ and you didn't run sed yet, it's a OneDrive staleness issue. Re-copy with `cat` to force sync:
```bash
cat "$v6/index.html" > /tmp/samaya-profile-deploy/index.html
```

### Efficient Asset Copy (avoids OneDrive slowness)

OneDrive is slow for bulk rsync. Instead, use Python to copy only referenced files:

1. Extract all unique `url('...')` paths from deploy HTML
2. Map to source path under the BASE directory
3. Copy only what's referenced — avoids copying the full 300MB+ assets directory

```python
import re, os, shutil
with open("/tmp/samaya-profile-deploy/index.html") as f:
    html = f.read()
paths = set()
for m in re.findall(r"url\('([^']+)'\)", html):
    paths.add(m)
BASE = "/Users/mohamedessa/Library/CloudStorage/OneDrive-SAMAYAINVESTMENT/Samaya/Technical Office/samaya-profile"
for p in paths:
    src = os.path.join(BASE, p)
    dst = os.path.join("/tmp/samaya-profile-deploy", p)
    if os.path.exists(src):
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        if not os.path.exists(dst):
            shutil.copy2(src, dst)
```

This copies only the ~152 referenced images (~55MB) instead of scanning the full assets tree (~2GB).

## Photo Management

### REPLACE, never add new blocks
The user strongly enforces this: **replace existing photos in-place, never add new gallery blocks, sections, or layout elements.** If a section already has a defined structure (e.g., a 4-tile grid, a pipeline, a 3-column gallery), replace the photo URL in the existing element — do not add extra divs, extra cells, or extra grid items.

Exception: the user explicitly says "add another page" or "you can make more than one page". Then a new page/section can be created.

#---

## Domain: Editorial Redesign Workflow (absorbed from `samaya-profile-editorial`)

### Page-by-Page Redesign Pattern

When doing a full editorial rewrite/redesign:

1. Read the page HTML + CSS rules
2. Understand what it communicates — rewrite text, resize/reposition photos, vary layout density
3. Check overflow — remove `height: calc(210mm - 22mm - 14mm)` if content overflows
4. Update TOC if page count changed
5. Patch index.html + relevant CSS
6. Move to next page

### Design System Constants

- **Colors**: Navy `#111827` (var(--v3-ink)), Gold `#C9A24B` (var(--v3-gold)), Cream `#F7F2E8` (var(--v3-paper))
- **Fonts**: Cairo (Arabic, 400-900), Inter (English), Cormorant Garamond (serif/italic)
- **Format**: RTL, A4 landscape (297mm × 210mm)
- **Google Fonts URL**: use `wght@` (with `@`) not `wght;` — `family=Cairo:wght@400;500;600;700;800;900`

### Editorial Style Rules

- Arabic PRIMARY, English secondary. Every headline has a matching AR/EN pair.
- Active Arabic verbs: `"نصنع"` not `"يتم التصنيع"` — confident, declarative.
- Museum-catalog tone: professional, precise, not salesy.
- Titles: Punchy, action-oriented. Use em-dashes for rhythmic breaks.
- Captions: Bold EN + AR, e.g. `<strong>Photo name</strong>AR translation — description`.
- No text-shadows anywhere in CSS (user-enforced).
- Concise: User said "dont talk too much".
- Numbers: Use `&thinsp;` for thin spaces between number and unit.

### Hold Point Icons Pattern

Replace numbered spans with inline SVG icons (viewBox="0 0 20 20", stroke="#A47A1F", fill="none", stroke-width="1.5"):
01=document, 02=checkmark, 03=magnifier, 04=flask, 05=box. CSS: `.v3-method .v3-method-tl-icon { inline-size: 7mm; block-size: 7mm; flex-shrink: 0; }`

### Overflow Fix Root Cause

The profile's global `.page { height: 210mm; overflow: hidden; }` in `00-tokens.css` clips any content exceeding one A4 sheet. **To fix overflow:**
1. Change global `.page`: `height: auto; min-height: 210mm; overflow: visible;`
2. Remove `height: calc(210mm - 22mm - 14mm)` from `.content` rules
3. Remove `overflow: hidden` from `.content` rules
4. For grid-based layouts, also change `grid-template-rows: ... 1fr ...` so the 1fr row doesn't squeeze

**Exception — Back cover**: Keep `.ed-back-cover { height: 210mm; overflow: hidden; }` fixed.

### Gallery Curation

When too many photos overflow a page, curate to best 6-9 — don't add more pages unless user asks. Keep most impressive/credible; remove duplicates/weak.

---

## Domain: Legacy Deployment Scripts (absorbed from `samaya-company-profile`)

The `samaya-company-profile` skill contained supporting scripts and references that are now here:

### Convenience Scripts (moved to this skill's scripts/)

| Script | Purpose |
|--------|---------|
| `scripts/deploy.sh` | Full deploy pipeline: clean, copy, fix paths, copy assets, surge, verify |
| `scripts/copy-deploy-assets.py` | Extract all asset paths from index.html, copy only referenced files, handle URL-encoded filenames |

Run from anywhere: `bash ~/.hermes/skills/productivity/samaya-factory-profile/scripts/deploy.sh`

### Project Photo Mapping Reference (moved to references/)

`references/project-photo-mapping.md` — Maps Arabic-named project folders (مشاريع سمايا/) to English asset paths in `assets/img/projects/`. Used for batch HQ photo replacement from the على‌السعودية photo collection.

### SVG Chart Patterns (moved to references/)

`references/svg-chart-patterns.md` — Brand palette, SVG templates for the Operational Capacity page (p4): comparison bar, stacked bar, timeline spine, abstract icons per stat.

### Photo Source Folders (moved to references/)

`references/photo-source-folders.md` — Quick reference of dedicated asset subdirectories under `assets/img/`.

---

## Photo source paths
- WhatsApp temp: `/Users/mohamedessa/Library/Containers/net.whatsapp.WhatsApp/Data/tmp/documents/`
- Downloads: `/Users/mohamedessa/Downloads/`
- Production folder: `/Users/mohamedessa/Downloads/Production/`
- Best high-res: `.../classified/website-ready/06-Best-High-Res/`
- Opening Ceremony: `.../classified/website-ready/05-Opening-Ceremony/`
- Workshop folder 011: `.../00000 صور واتساب سنة 2025 الورشة/011/`
- Aseer project scanners: `.../Bim Unit/Aseer-Museum/Subcontractors/01_Replica_Model_Contractor/10_Purchasing/3D Scanner/Artec/`
- China Treasures Exhibition: `.../v6/مشاريع سمايا/معرض كنوز الصين/`
- Quran Museum project: `.../v6/مشاريع سمايا/متحف القرآن الكريم/`
- Needs-vision-check: `.../classified/review/needs-vision-check/`
- OneDrive-Personal Pictures: `/Users/mohamedessa/Library/CloudStorage/OneDrive-Personal(2)/Pictures/SamayaFactory/` — photos from personal backup (updated 2026-06-09)

### OneDrive-Personal(2) Path Pitfall
Paths containing `(2)` (from OneDrive-Personal sync) break shell commands that aren't quoted. Always use Python's `shutil.copy2()` or properly quoted shell strings when copying from `OneDrive-Personal(2)/`. Shell globs and unquoted `cp` commands will misinterpret the parentheses as subshell syntax.

### Photo compression
RAW photos (13-15MB) from exhibition folders must be compressed before copying to assets:
```bash
sips -Z 2000 "/path/to/source.jpg" --out "/tmp/compressed.jpg"
cp /tmp/compressed.jpg "/path/to/assets/photo-name.jpg"
```
This reduces ~15MB → ~500KB at 2000px wide, sufficient for A4 print at 300dpi.

### WebP file conversion
When user provides `.webp` files from Downloads, convert to JPEG:
```bash
sips -s format jpeg "/path/to/source.webp" --out "/tmp/converted.jpg"
cp /tmp/converted.jpg "/path/to/assets/destination.jpg"
```

### OneDrive Copy Fidelity

The source files live on OneDrive, which uses "Files On-Demand" — `cp` may receive a stale placeholder instead of the current file content.

**After copying, verify** with md5:
```bash
md5 "/path/to/onedrive/source/file"
md5 "/tmp/samaya-profile-deploy/file"
```
If hashes differ and you didn't run sed yet, it's a OneDrive staleness issue. Re-copy:
```bash
cat "/path/to/onedrive/source/file" > "/tmp/samaya-profile-deploy/file"
```

### Photo destination
- Materiality: `assets/img/projects/material-samples/`
- Replicas: `assets/img/projects/replicas/`
- Wayfinding: `assets/img/projects/wayfinding/`
- BIM/Engineering: `assets/img/projects/bim/`
- 3D Scanning: `assets/img/scope-replicas/process/`
- Hakaia Elm (SFDA): `assets/img/projects/hakaia-elm/`
- Madinah Royal: `assets/img/projects/madinah-royal-reception/`

### Photo type overrides
- `background-size: cover` — fills container, may crop edges (use for hero banners, gallery items with defined aspect ratios)
- `background-size: contain` — shows full image with whitespace gaps (use for Materiality grid cells to avoid cropping)

### Image height constraint pitfall
Photos inside flex/grid cards with `flex: 1` and NO explicit height will grow unbounded, creating giant vertical images that can overlap other pages. **Always set explicit heights** on image containers:
```css
.v4-prequal-img-card-photo {
  block-size: 130px;
  min-height: 130px;
  max-height: 130px;
}
```
For tier gallery tiles (v4-tier), **always add a height** to `.v4-tier-tile-img` — they have `background: cover` with no block-size, causing the tile to expand unpredictably.
All images must be used exactly once across the profile — after any batch photo replacement, run a `Counter()` check on all `../assets/img/` references in index.html to verify no duplicates.

## Layout & Overflow Rules

### Page height strategy
- Pages with **multi-page content** (Materiality, large galleries): global `.page { height: auto; min-height: 210mm; overflow: hidden; contain: paint; }` — **CRITICAL**: `overflow: visible` causes content to bleed into adjacent pages, breaking the entire profile layout
- Pages that should fill **exactly one A4 page** (flagships, capacity, scanning): add `height: calc(210mm - 22mm - 14mm)` to the `.content` div
- **Never mix both** on the same content div — it causes double-height issues

### Root Cause: Global .page overflow:hidden clips multi-page content

`00-tokens.css` declares:
```css
.page {
  overflow: hidden;    /* clips ANY content exceeding 210mm A4 */
  contain: paint;      /* creates clipping context */
}
@media print {
  .page {
    height: 210mm;
    overflow: hidden !important;
  }
}
```

When you split a single-page section into a 2-page spread (e.g., p14 → p14 + p14b), each `<section>` is still a `.page` with `overflow: hidden`. Content that overflows the first page is CLIPPED, not flowed to the second page.

**Fix pattern** — Override in the archetype's CSS file:
```css
.archetype-class {
  overflow: visible !important;
  contain: none !important;
}
@media print {
  .archetype-class {
    overflow: visible !important;
    contain: none !important;
    height: auto !important;
    min-height: 210mm;
  }
}
```

**When to apply**: Any archetype converted to multi-page. Current list:
- `v4-macro` (GRC pages, p19+p19b)
- `v4-cmyk` (Print pages, p14+p14b)
- `v4-type` (Wayfinding pages, p15+p15b)

**After adding the override, verify no other archetype broke**:
```bash
grep 'overflow: hidden' css/00-tokens.css
```

### Common overflow fixes
1. Remove `height: calc(210mm - 22mm - 14mm)` from `.content` to allow growth
2. Remove `overflow: hidden` from `.content` to prevent clipping
3. Remove `grid-template-rows: ... 1fr ...` if the parent has no fixed height (1fr collapses to auto)
4. For the back cover (`.ed-back-cover`): keep `{ height: 210mm; overflow: hidden; }` — it must be fixed
5. **If `.page` still clips after removing `.content` constraints**: the root cause is `00-tokens.css` `.page { overflow: hidden }`. Override with `overflow: visible !important` in the archetype CSS.

### Page balance
When content is too short for the page, increase element heights:
- Gallery items: 48mm → 52mm
- Hero images: 34mm → 42mm
- Grid images: 24mm → 32mm
- Use `flex: 1` on flex/grid containers that should expand to fill space
- **TOC update**: After ANY structural change (pages added/removed/renumbered), update section id="p2" page numbers

### TOC Overflow Fix Pattern
When the CONTENTS page (p2, class `v3-toc`) overflows:
1. Add `height: calc(210mm - 22mm - 14mm); overflow: hidden;` to `.v3-toc .content` (often missing)
2. Compact entry spacing: reduce `.v3-toc .v3-toc-entry` `padding-block` from 1mm→0.6mm
3. Reduce `.v3-toc .v3-toc-act` `padding-block` from 2.5mm/1mm→1.5mm/0.5mm
4. Reduce `.v3-toc-n` font-size: 12pt→9pt
5. Reduce `.v3-toc-ar` font-size: 9.5pt→8pt
6. Reduce `.v3-toc-en` font-size: 6.3pt→5.5pt, letter-spacing: 0.16em→0.1em
7. Reduce `.v3-toc-p` font-size: 9pt→8pt
These changes save ~30% vertical space across 23 entries + 6 section headers in 2 columns.

### v4-catalog (Display/Vitrines, #p12) Overflow Fix Pattern

When the Display & Experience Systems page (#p12, class `v4-catalog`) overflows its 174mm content area:

1. **Compress photo strip** — reduce the top hero strip from 40mm → 32mm. The photo strip is an inline-styled `<div>` with `height:40mm;min-height:40mm;`:
   ```html
   <div style="...height:32mm;min-height:32mm;">
   ```
2. **Reduce column image heights** — in `37-catalog.css`, change `.v4-catalog-col-img { block-size: 43mm; }` → `38mm`
3. **Tighten post-grid spacing** — the area below the 4-column grid has material cards + process pill + disclaimer. Reduce:
   - Post-grid `margin-top`: 5mm → 3mm
   - Process pill `margin-top`: 3.5mm → 2.5mm, `padding`: 2mm → 1.5mm
   - Disclaimer `margin-top`: 3mm → 2mm, `padding`: 2.6mm → 2mm
   - These save ~5-6mm total

**Typical savings**: ~16mm, bringing 182mm estimated content within 174mm bounds.

**If still overflowing**: remove `overflow: hidden` from `.v4-catalog .content` in `37-catalog.css` and set `height: auto` to allow multi-page flow.

### Multi-page vs single-page decision
The user is OK with multi-page overflow on dense content sections (Materiality & Craft with 48 cells).
The user prefers single-page with curated content for showcase pages (Replicas gallery → pick best 6 photos, 3×2 grid).

## Text Style — Concise, Punchy, Bilingual

### No Text Shadows — User-Enforced

The user explicitly requires: **remove ALL text-shadow from every element.** No exceptions for readability over photos.

When asked to remove shadows, use bulk sed across all CSS files:
```bash
CSS_DIR="/path/to/v6/css"
for f in "$CSS_DIR"/*.css; do
  sed -i '' 's/text-shadow: [^;]*;/text-shadow: none;/g' "$f"
done
```

If this was previously applied, verify no actual declarations (not comments) remain:
```python
for line in open('file.css'):
    if 'text-shadow:' in line and 'none' not in line:
        if not line.strip().startswith(('/*', '*', '//')):
            print(f"REMAINING: {line}")
```

Note: 30-redesign.css (unlinked legacy monolith) will still show text-shadow counts — ignore it. Only check active CSS files (31-*.css through 45-*.css).



The user repeatedly insists on brevity. Follow these rules:

1. Short sentences, bullet-point structure — avoid paragraphs longer than 3 lines
2. Active verbs in Arabic — prefer "نصنع المتاحف" over "صناعة المتاحف"
3. Bilingual pairs — every title has matching AR/EN. Arabic is primary, EN is secondary
4. No marketing fluff — no "we pride ourselves on", "our commitment to excellence"
5. Museum-catalog tone — confident, factual, direct
6. Em-dashes for rhythm — break long titles with em-dash
7. Numbers always prominent — use Cormorant Garamond italic for stat numbers at large size

## PROTECTED CONTENT — NEVER CHANGE
The following brand content must never be altered by editorial redesign passes:
- **Cover slogan**: AR: "هندسة الفنّ. لصناعة الإرث." / EN: "Engineering Art. For Crafting Legacy."
- If Claude or any subagent changes these, revert immediately.
- **IMPORTANT**: When delegating editorial redesign to Claude, explicitly instruct it to preserve the cover slogan. Claude will try to "improve" it if not told otherwise.

## Section Photo-Led Redesign (Consolidated Pattern)

This pattern applies when any section's photos are too small, or the user asks for a "photo-led" redesign (e.g., Print p14, Wayfinding p15, GRC p19, QA Lab p25c).

### Target Photo Sizes

| Role | Minimum | Good |
|------|---------|------|
| Hero / full-width | 70mm | 80-92mm |
| Gallery / card photos | 28mm | 32-42mm |
| Process step photos | 28mm | 32mm |
| Evidence / detail photos | 20mm | 26-32mm |

### Multi-Agent Consultant Team Workflow

When the user says "make consultant team from Claude, Kimi, Codex" for a section redesign:

**Steps:**

1. **Read current section HTML + CSS** — understand layout constraints (height:calc, overflow:hidden, position:absolute)

2. **Delegate to Claude** (with toolsets ["terminal","file"]):
   - Send the full section HTML range + CSS file paths
   - Specify target photo sizes (from table above)
   - Say: "Only use patch() — never write_file on CSS files. No SVG placeholder images."
   - Say: "Keep bilingual format (Arabic primary, English secondary)"
   - If splitting to 2 pages, specify: "Add second section id='pXNb' with proper footer number and TOC entry"

3. **Kimi reviews** after Claude completes:
   - Check ALL photo paths resolve to real files on disk (Claude invents phantom paths)
   - Check TOC has entries for all new sub-pages
   - Check footer numbers follow suffix pattern (p13→"13", p13b→"13b")
   - Check no third-party content leaked in (when adapting reference docs)
   - Check cover slogan intact

4. **Fix overflow** if Kimi reports it:
   - If `.content` uses `position: absolute; bottom: 18mm;` (p25a-p25e pages):
     - Content area is 170mm (210mm - 22mm header - 18mm bottom)
     - Add `overflow: hidden;` to the `.content` rule
     - Reduce element sizes until total fits within 170mm
   - If `.page` has `overflow: hidden; contain: paint;` (global 00-tokens.css):
     - Override in the archetype's CSS: `overflow: visible !important; contain: none !important;`
     - Also override in `@media print` (which has `overflow: hidden !important`)

### Known Section Transformations

| Section | ID | Before | After | Photo Gain |
|---------|----|--------|-------|------------|
| Print Machines | p14 | 17-20mm crushed | 42mm cards, 32mm evidence, 50mm QA | ~3× |
| Wayfinding | p15 | text-only + 20mm | 48mm hero, 26mm gallery | ~2× |
| GRC/GRP | p19 | text-heavy, ~30mm hero | 68mm hero, 32mm process | ~2× |
| QA Lab | p25c | ~20mm crushed in 2-col | 44mm hero, 28mm cards, 30mm flow bar | ~3× |

### Splitting to 2 Pages (Post-Split Checklist)

After splitting any single section into 2 pages (e.g., p14 → p14 + p14b):

1. **Both sections exist** in index.html with proper `class` and `dir="rtl"`
2. **TOC has entries for all new pages** — add `v3-toc-entry--sub` for letter-suffixed pages (p14b, p15b, p19b)
3. **No dead TOC links** — every `href="#p..."` has a matching `<section id="p...">`
4. **Footer numbers correct** — p14b → "14b", p15b → "15b", p19b → "19" (or next number in sequence)
5. **Adjacent page TOC preserved** — after adding p14b, verify p15's TOC entry wasn't accidentally overwritten
6. **Overflow handled** — either `overflow:hidden` with height:calc for single-page, or overflow:visible override for multi-page
7. **Image paths resolve** — run the phantom-path check before deploying

## Design Workflow
- **Delegate all design/layout/restructure work to Claude** via `delegate_task` with toolsets `["terminal","file"]`
- Never add new layout blocks, tiles, or sections unless explicitly asked
- Captions: bold EN + AR from user descriptions, bilingual
- Palette: #F7F2E8 paper, #111827 ink, #C9A24B gold, #A47A1F deep gold, #DED6C8 lines
- Fonts: Cairo (AR headings & body), Inter (EN labels & technical text), Cormorant Garamond (italics & serif)

## Prequalification Focus (mandatory for all sections)
Every section must frame content as **factory capability evidence**:
- Show **machines** and **equipment** photos (not just finished work)
- Describe the **process flow** and **operations** (not just features)
- Include **machinery specs** where relevant (CNC, laser, edge bander, HOMAG, etc.)
- Frame text as capability statements: "We can X using Y process with Z equipment"
- For QA/spec pages, include **measurement samples** and **calibration references** (VDI/VDE 2634, etc.)
- **No brand/device names** in scanning/specs sections — use generic technical terminology
- **Machine brand names ARE acceptable** for production equipment (HOMAG CNC, Blum/Hettich hardware, BIM 360) — the user confirmed these signal real capability in a prequal profile. Only scanner/print brands (Artec, Durst, Roland) should be generified.
- Load `samaya-profile-photo-assets` skill for photo classification before adding images

## Prequalification Audit Workflow (Multi-Agent)

See `references/prequalification-standards-checklist.md` for the full 7-point standards table and Aseer Museum relevance criteria. Load this file before delegating audits.

### Phase 1 — Establish Standards Checklist

Define 7 standards before delegating. Every section is checked against all:

| # | Standard | What to look for |
|---|----------|------------------|
| 1 | **Factory Language** | Never "ورشة/workshop/atelier" in visible text — always "مصنع/factory/production line/خط إنتاج" |
| 2 | **Capability Evidence** | Machines, process flow, equipment specs — not just finished-work photos |
| 3 | **No Brand Names** | 3D scanning generic only. Print section: prefer "UV Flatbed" over "Durst" |
| 4 | **Museum Relevance** | Conservation-grade materials, Oddy/PAT, climate control, display systems |
| 5 | **Bilingual Punch** | Arabic primary, English secondary. Short sentences, active verbs, no marketing fluff |
| 6 | **Photo Authenticity** | Real project/process photos only — no stock, no SVG placeholders, no GenAI images |
| 7 | **No Aseer Museum** | Profile must NOT mention Aseer Regional Museum (متحف عسير الإقليمي) |

### Phase 2 — Delegate Parallel Audits (3 Agents)

Split the 39 sections into 3 blocks, each audited by a separate subagent:

- **Agent A**: Sections p1–p13 (Cover through Replicas)
- **Agent B**: Sections p13b–p25e (Replica Gallery through Flagship Projects)
- **Agent C**: Sections p4-hse–p27 (HSE through Back Cover)

Each agent returns: section ID, specific quote with line number, priority (HIGH/MED/LOW), suggested fix text.

### Phase 3 — Fixes in Two Rounds

**Round 1 — Text fixes** (direct patch):
- Terminology violations (workshop→factory, ورش→خطوط إنتاج, atelier→production lines)
- Eyebrow numbering (see Ed-Eyebrow Check below)
- **Bilingual eyebrow flips** — Systematic issue: eyebrow labels like `SCOPE 05 · PRINT MACHINES <span>الطباعة</span>` have English first, Arabic inside span. Fix: flip so Arabic is the outer text: `الطباعة الرقمية وخط الإنتاج <span>SCOPE 05 · PRINT MACHINES</span>`. Check ALL section headers and eyebrow labels — English-first pattern is common across p7, p13b, p14, p14b, p15, p15b, p19.
- Brand names in print section (Durst→UV Flatbed, Roland→Roll-to-Roll)
- Minor text: marketing fluff removal, missing warranty, capability one-liners

**Round 2 — Content expansion** (delegate to a content subagent):
- Thin sections (GRC/GRP, gallery, wayfinding) need process strips, substrate lists, equipment references
- Replace GenAI/placeholder images with real project photos
- Add museum-relevance framing where missing

### Phase 4 — QA Verification (Single Agent)

Delegate a QA verification agent checking:
1. Terminology: 0 WORKSHOP/ورش/ATELIERS in visible text (filenames/comments OK)
2. Eyebrow numbers: all 5 ed-spread sections match (17→18→19→20→21)
3. Brand names: Durst/Roland = 0, GenAIImage = 0
4. Aseer Museum: 0 matches
5. Cover slogan intact ("هندسة الفنّ. لصناعة الإرث." / "Engineering Art. For Crafting Legacy.")
6. CSS height constraints undamaged — `grep -c '210mm' v6/css/*.css` count unchanged
7. Image dedup: counter on `../assets/` refs

### Ed-Eyebrow Numbering Cross-Check

The `ed-spread` archetype has TWO numbering locations that must match:

1. **Page header**: `<div class="section-tag">17 · HSE RECORD</div>`
2. **Ed-eyebrow**: `<span class="ed-eyebrow">17 · ... · HSE</span>`

| Section | ID | Tag # | Eyebrow # |
|---------|----|-------|-----------|
| HSE | p4-hse | 17 | **17** |
| Approvals | p20 | 18 | **18** |
| After-Sales | p22 | 19 | **19** |
| Certifications | p25 | 20 | **20** |
| Financial | p4-financial | 21 | **21** |

**Known failure**: When pages are restructured, eyebrow numbers are NOT auto-updated. After any structural edit, grep:
```bash
grep 'ed-eyebrow">[0-9]' v6/index.html
```
Expected sequence: `17`, `18`, `19`, `20`, `21` in page order.

## QA/QC Page (v3-method) — Photo Crop Fix Pattern

When QA page instrument photos appear cropped:
1. Change `background-size: cover` → `contain` on `.v3-method-ecard-img`
2. Add `background-color: #fff` or `var(--v3-paper)` so whitespace gaps blend with the page
3. Increase image height from 22mm → 28mm to give more room for contain
4. The QA instruments CSS may be in a separate file (`35-method.css`) created by Claude — check there first
5. Also check that photo paths point to the correct folder (the folder may be `05-qa-lab/` but HTML refs say `06-qa-lab/` — fix whichever is wrong)

## QA/QC Page (v3-method) — Evidence Card Hero Treatment

When the user says "hero photo" or "make this a hero" for a specific evidence card on the QA methodology page (#p6):

1. **Replace the image** in the existing evidence card — do NOT add new cards or change the 4-column grid layout
2. **Override background-size inline** on the specific card's `.v3-method-ecard-img`:
   ```html
   <div class="v3-method-ecard-img" style="background-image:url('../assets/img/05-qa-lab/tube_oddy.png'); background-size: cover;">
   ```
   This overrides the CSS default `contain` on just this card while the other 3 cards keep `contain`.
3. **Keep the badge** (e.g., `ENVIRO`) — it overlays the hero image and gives context
4. **28mm height still applies** — the CSS `block-size: 28mm` from 35-method.css constrains all cards equally
5. For tall/narrow photos (e.g., tube_oddy.png at 295×500px), `cover` crops sides aggressively but fills the card edge-to-edge — this is the desired hero look

**When NOT to use this pattern:**
- If the user wants a FULL-PAGE hero (background banner spanning the page), add a new hero layer above/below the evidence cards, not inside the 4-column grid
- If all 4 cards need hero treatment, update the CSS in `35-method.css` for `.v3-method-ecard-img` globally instead of inline per-card

**Also**: After replacing a photo on the QA page, verify no other page references the same photo path (see Photo Duplication check).

### Reference-Driven Section Redesign (Third-Party Guide → Samaya Capability)

When redesigning a section based on a third-party reference document (e.g., Vision wayfinding guide PDF):

1. **Extract & Summarize** — Have Kimi extract the PDF content and produce a 2-page bilingual summary covering services, specs, process, and standards
2. **Adapt, Don't Copy** — The summary is a REFERENCE, not source text. Every capability must be reframed as Samaya's own: "Vision offers X" → "Samaya delivers X using in-house Y equipment"
3. **Build the Prompt** — Codex role: write the Claude prompt incorporating the summary's key points + the current section HTML + the desired 2-page structure
4. **Claude Redesigns** — Delegate to Claude with: section HTML range, CSS file paths, summary reference, desired 2-page layout, and the explicit instruction to frame everything as Samaya's own capability
5. **Kimi Reviews** — Critical verification step:
   - Check NO third-party branding/text leaked into the profile (grep for Vision, the guide company name, URLs)
   - Check ALL photo paths resolve to existing files (Claude invents phantom paths)
   - Check bilingual format (Arabic primary, English secondary)
   - Check TOC has entries for new sub-pages (p15b etc.)
   - Check footer numbers follow the pattern (p15 → "15", p15b → "15b")

**Output files from this workflow**:
- Summary: `Guide/<GuideName>_Summary.md` — bilingual reference for future edits
- Profile changes: patched HTML + CSS as normal
- The summary file lives permanently as a project reference, not in the profile itself

**Example**: Wayfinding page redesign (v6.9) processed the `Vision_SignageWayfinding.pdf` (39 pages) into a 2-page reference, then built p15 as a 2-page Samaya capability spread.

See `references/reference-driven-section-redesign.md` for the full 4-agent workflow.

When doing a full profile redesign pass:

1. Start from page 1, go in order to the last page
2. For each page:
   a. Read the full section HTML + its CSS rules
   b. Understand the page's purpose and audience
   c. Redesign: rewrite text (punchy), resize/reposition photos, vary layout density
   d. Check overflow — if content doesn't fit, remove height calc or reduce element sizes
   e. Update TOC if page numbers changed
   f. Patch index.html + relevant CSS with exact diffs
3. Vary rhythm between adjacent pages: alternate dense/airy, text-heavy/image-heavy
4. After all pages, do a final overflow scan across the entire profile

### Page numbering and TOC sub-entries
Pages can have letter-suffixed numbers (p13a, p13a-1, p13b). Add sub-entries to the TOC:
```html
<a class="v3-toc-entry v3-toc-entry--sub" href="#p13a">
  <span class="v3-toc-n">11a</span>
  <span class="v3-toc-titles">
    <span class="v3-toc-ar">الاسم العربي</span>
    <span class="v3-toc-en">English Name</span>
  </span>
  <span class="v3-toc-p">13a</span>
</a>
```
CSS for sub-entries:
```css
.v3-toc .v3-toc-entry--sub {
  padding-inline-start: 8mm;
  border-block-end: none;
}
.v3-toc .v3-toc-entry--sub .v3-toc-n {
  font-size: 7pt;
}
```

### Post-Change Checklist
- TOC page numbers updated (section id="p2")
- TOC entries fit within A4 bounds (check overflow on #p2)
- No overflow on any .content block (check height calc patterns)
- All new CSS classes defined (not orphaned HTML)
- Surge deploy succeeded
- No duplicate images across the profile
- Brand slogan unchanged (cover page + about page)
- Aseer Museum (متحف عسير الإقليمي) NOT present anywhere
- CSS height constraints intact — run `grep -c '210mm' v6/css/*.css` after any subagent CSS edit
- **TOC entries all resolve** — grep for every `href=\"#p` in the TOC section (lines ~180-400) and verify each hash ID matches an existing `<section id=\"...\">` in the HTML. Dead links (e.g., `#p13a-1` where the section was removed) silently break navigation.

## Full Profile Overflow Audit Pattern
When asked to audit all pages for overflow:
1. Delegate to Claude with `delegate_task` — give it all CSS file paths and index.html
2. Claude reads each section, estimates content height vs the 174mm content area, flags issues
3. Then delegate fixes to a code agent — reduce image heights (e.g., Materiality 48mm→22mm), tighten gaps, remove height calcs, remove overflow:hidden
4. Fix **critical pages first** (Materiality with 60+ cells → largest overflow), then high risk (Capacity), then marginals
5. Deploy after fixes are applied

## Delegation Safety — CSS Height Constraint Fragility

**CRITICAL PITFALL**: Every subagent that patches CSS files may accidentally REMOVE height constraints from unrelated page rules. This has happened repeatedly:

1. Claude edits `proj-sectorial .content` → removes the `height: calc(...)` line from the rule
2. Claude edits `proj-org .content` → removes the `height` and `overflow` from the rule
3. Claude edits `v3-method .content` → removes height from this and adjacent rules

**Why it happens**: Claude's `patch` tool targets exact strings. When it replaces a large block of CSS, it copies the CURRENT state of the rule — if the rule was previously edited and the height was part of a different textual context, Claude's new version may omit it.

**Fix pattern**: After ANY subagent finishes a CSS edit, immediately verify:
```bash
grep '210mm\|height: calc' /path/to/v6/css/*.css
```

Expected output should include 10-14 pages with height constraints:
- `.v3-method .content`
- `.v4-catalog .content`
- `.v4-replica-gallery .content`
- `.proj-sectorial .content`
- `.proj-org .content`
- `.proj-landmark .content`
- `.proj-materiality .content`
- `.proj-flagship .content`
- `.proj-map .content`
- `.ed-spread .content`
- `.v4-discipline .content`
- `.v4-scope .content`
- `.p25a .content` through `.p25e .content`

**NOTE**: `.v4-cmyk .content`, `.v4-type .content` are NOT in this list — they were converted to multi-page layouts (no fixed height) during photo-driven redesigns. If they reappear in grep results, they were accidentally re-added.

If any are missing, the subagent's CSS patch silently broke them. Re-add immediately.

## v5 → v6 Section Copy Pattern

When copying sections from v5 into v6:

1. Parse v5's `<div class="content">...</div>` body (the inner content)
2. Keep v6's page shell: `<section>` opening with v6 CSS classes, `<header>` with v6 section tag, `<footer>` with v6 page number
3. Merge: v6 shell + v5 content body + v6 footer
4. Verify: after copy, check that the content's CSS classes still exist in v6's CSS files
5. The v5 content will inherit v6 styling automatically since the same CSS classes apply
6. If v5 uses different class names than v6, the content will NOT be styled — either add the v5 classes to the CSS or update the v5 HTML to use v6's class names
7. **Check `section-tag` consistency**: After copy, verify the `<div class="section-tag">` text matches the page's actual content (v5 may have different section numbering or names). Update if needed.

## Photo De-duplication — Mandatory Verification

After any batch photo replacement, verify uniqueness:
```python
import re
from collections import Counter
with open("v6/index.html") as f: html = f.read()
refs = [m.group() for m in re.finditer(r'\.\./assets/[^"\')\s]+', html)]
dupes = {k:v for k,v in Counter(refs).items() if v > 1}
print(f"Duplicate images: {len(dupes)}")
for img, count in sorted(dupes.items()): print(f"  {img} ({count}x)")
```

If duplicates exist and they're NOT intentional (same project photo in gallery + detail page), replace the 2nd+ occurrence with a different photo from the same directory.

### Use Real Photos, Not SVG Placeholders, GenAI Images, or Phantom Photo Paths (IMPORTANT)

**Claude has a strong tendency to:**
1. Create **SVG placeholder images** when real photos aren't available
2. Use **AI-generated images** (e.g., `GenAIImage_*.jpg` in #p12 vitrine)
3. **Invent photo paths that don't exist** — referencing directories that aren't in the project structure (e.g., `06-qa-lab/` instead of `05-qa-lab/`, `projects/material-samples/patina-work.jpg` which was never a Samaya photo)

**All three are unacceptable.** Prevention and detection for each:

#### SVG Placeholder Prevention
- In every delegation context, explicitly state: "Do NOT create SVG placeholder images"
- Detection: `grep -c '<svg ' v6/index.html` — if count increased, Claude created fake charts/icons
- Also check: `find assets/ -name '*.svg' | grep -i placeholder`

#### GenAI Image Prevention  
- Explicitly forbid in Claude prompts: "Do NOT use AI-generated images"
- Detection: `grep -ic 'GenAIImage\\|genai\\|ai.generated\\|ai-generated' v6/index.html`
- Expected: 0. If found, replace with a real project photo from `assets/img/07-projects/`

#### Phantom Photo Path Prevention (MOST COMMON)
Claude will invent photo paths that look plausible but don't exist. Common failure modes:
- Uses `06-qa-lab/` instead of `05-qa-lab/` (old folder name)
- Uses `projects/material-samples/*.jpg` which doesn't exist at that path
- Uses generic names like `real-quality-check.jpg` that no Samaya photo uses

**Prevention**: In every delegation context that adds/modifies photos, explicitly state:
- "Use ONLY photo paths from EXISTING files in assets/img/ — verify each path exists on disk before writing"
- "List the EXACT paths you plan to use before patching"

**Detection after delegation** (MANDATORY step after any Kimi/Claude redesign):
```python
import re, os
BASE = "/Users/mohamedessa/Library/CloudStorage/OneDrive-SAMAYAINVESTMENT/Samaya/Technical Office/samaya-profile"
with open(f"{BASE}/v6/index.html") as f: html = f.read()
paths = set()
for m in re.findall(r"url\\('([^']+)'\\)", html):
    paths.add(m)
missing = [p for p in paths if not os.path.exists(os.path.join(BASE, p)) and not p.startswith('data:')]
if missing:
    print(f"BROKEN PATHS ({len(missing)}):")
    for m in missing: print(f"  {m}")
```
Run this check BEFORE deploying. Fix any broken paths by finding the real file in `assets/img/` and updating the HTML.

#### Image Path Verification Flow
After ANY subagent adds new images to the profile:
1. Extract all url() paths from the HTML
2. Check each against the filesystem under the BASE directory
3. If paths use `06-qa-lab/` — this was renamed to `05-qa-lab/`; fix the path
4. If paths reference completely made-up files — search `assets/img/` for the actual file by name, or replace with a different real photo from the same context
5. Re-check until zero broken paths remain
6. Deploy with verification (Pre-Deploy Image Verification step)

## Version Tracking — CHANGELOG & Backups Mandatory

### CHANGELOG (every change)
Every change to the profile MUST be recorded in `profile-info-and-control/CHANGELOG.md`. Entry format:
```
## vX.Y — Brief Title (YYYY-MM-DD)
- **#pN** Section changed: what changed
- Backup: `v6-backups/v6-code-<timestamp>`
```

### Code-only backup (before any change)
Before modifying code, create a backup of ONLY HTML + CSS (no images):
```bash
BACKUP_DIR=".../samaya-profile/v6-backups"
TS="v6-code-$(date +%Y%m%d_%H%M%S)"
mkdir -p "$BACKUP_DIR/$TS/css"
cp path/to/v6/index.html "$BACKUP_DIR/$TS/"
cp path/to/v6/css/*.css "$BACKUP_DIR/$TS/css/"
```
This is fast (seconds, MB) vs a full backup with images (minutes, GB). User corrected that images don't need backup — they're static.

### Section-by-section workflow (user-enforced)
1. **Backup code** first → `v6-backups/v6-code-<timestamp>/`
2. **Work one section** at a time — don't touch multiple pages in one pass
3. **Log change** in CHANGELOG.md with backup reference
4. **Deploy** only when the section is done
5. **Repeat** for next section

### Restore from backup
```bash
cp "v6-backups/v6-code-<timestamp>/index.html" v6/index.html
cp "v6-backups/v6-code-<timestamp>/css/"*.css v6/css/
```

Three reference docs under `profile-info-and-control/`:
- `README.md` — project overview, deploy
- `STYLEGUIDE.md` — design system, 39-page structure, images per page, git undo
- `CHANGELOG.md` — version tracking (update every change)
- `font-gallery.html` — Arabic font comparison (open in browser)

## Profile Info Folder Convention

All documentation files belong under `profile-info-and-control/`:
```
samaya-profile/
├── v6/                    ← source code (HTML + CSS)
├── v5/                    ← reference version
├── assets/                ← images
├── profile-info-and-control/
│   ├── README.md         ← project overview
│   ├── STYLEGUIDE.md     ← design system, page structure
│   ├── CHANGELOG.md      ← version tracking (update every change)
│   └── font-gallery.html ← font comparison tool
```

## Font Change Procedure

**Current Arabic font: Cairo** (switched from Tajawal on 2026-06-07). Cairo pairs geometrically with Inter.

When switching the Arabic font:

1. **Replace in CSS** — find/replace all `'Tajawal', sans-serif` → `'NewFont', sans-serif` across all 15 CSS files in `v6/css/`
2. **Replace in HTML** — find/replace all inline `Tajawal` references in `v6/index.html` (style attributes, any variant: single-quoted, double-quoted, bare)
3. **Update Google Fonts link** — in index.html `<head>`, change the `family=` parameter:
   ```
   https://fonts.googleapis.com/css2?family=Cairo:wght@400;500;600;700;800;900&...
   ```
   **CRITICAL**: Use `wght@...` syntax (with `@`), NOT `wght;...` (with semicolon). The semicolon version silently fails — Google Fonts returns a CSS file that doesn't load correctly. This is a recurring bug.
4. **Update `00-tokens.css`** — the `--font-display` and `--font-body` CSS variables reference the old font
5. **Update this skill** — the font declarations section at the top
6. **Log in CHANGELOG.md**

## Font Gallery File

When the user wants to compare fonts, create `profile-info-and-control/font-gallery.html`:
- Load 4-6 Arabic fonts from Google Fonts
- Show the brand slogan + company name in each font
- Mark current and recommended options
- The user opens this file in the browser to compare
- After they choose, run the Font Change Procedure above

## Page Number Audit

After structural edits (pages added/removed/renumbered):

1. Audit all footer `.num` values:
   ```bash
   grep -o '<div class="num">[^<]*<' v6/index.html
   ```
2. Verify sequence: p1 (no num), p2=02, p3=03, ..., p27 (no num)
3. Check section tags match footer numbers where possible:
   ```python
   import re
   for m in re.finditer(r'<div class="section-tag">([^<]+).*?<div class="num">(\d+)', html, re.DOTALL):
       print(f"  Tag: {m.group(1)} → Num: {m.group(2)}")
   ```
4. Common mismatches to fix:
   - p6 footer shows "06" but it's the 8th page → fix to "08" + TOC ref
   - p12 missing footer number → add `<div class="num">12</div>`
   - p19 tag says "13·GRC" but footer should match position
5. After fixing, update TOC (`#p2`) page references to match

## No-Deploy Workflow

When the user says "Do not deploy" or "Work locally only":
1. Do NOT run surge or any deploy commands
2. Make changes to source files only
3. Verify images exist on disk (filesystem check, not curl)
4. Present change summary — wait for explicit deploy approval
5. Skip all deploy verification steps (curl, surge list)

## Deploy — CDN Cold Start Note

Surge.sh has a CDN cold-start issue: the first request after a deploy often returns **504 Gateway Timeout**. This is normal — the file was deployed successfully.

**Verification pattern**:
```bash
# Deploy
surge --project ./ --domain samaya-factory-profile.surge.sh

# First check: may 504 (cold start)
curl -s -o /dev/null -w "%{http_code}" "https://samaya-factory-profile.surge.sh/"
# → 504 (transient, not a failure)

# Wait 3-5 seconds, then retry
sleep 5 && curl -s -o /dev/null -w "%{http_code}" "https://samaya-factory-profile.surge.sh/"
# → 200 (confirming deploy worked)
```

Always wait 3-5 seconds after deploy before testing. The first 504 is not a failure.
Do NOT re-deploy because of a 504 — it will redeploy successfully but the user sees the same transient 504.

WARNING: The `surge --project` output message may be garbled by a Node.js error message printed to stdout by pwd/getcwd in certain terminal states. If `tail -1` shows "Node.js" or "pwd: error" instead of "Success!", the deploy **still succeeded**. Run `surge list | grep samaya-factory-profile` to confirm the timestamp updated.

## Cover Photo — Direct Inline Style Preferred

The cover photo on p1 uses a CSS variable approach (`--v3-img` inline on `<section>`) which can have URL resolution issues in some browsers.

**Preferred approach**: Set `background-image` directly as an inline `style` on the `.v3-photo-img` element:
```html
<div class="v3-photo-img" style="background-image:url('../assets/img/02-facility/workshop-wide.jpg');" aria-hidden="true"></div>
```

**Avoid**: CSS custom properties containing `url()` — they resolve relative to the CSS file, not the HTML file, causing path mismatches in some rendering contexts.

## CSS Class Mismatch Pattern (v5 → v6 Copy Pitfall)

When copying page content from v5 into v6, the CSS classes used in v5 HTML may NOT exist in v6's CSS files. This happened with p14 (Colour-Managed Print):

- v5 HTML used: `v4-cmyk-head`, `v4-cmyk-body`, `v4-cmyk-side`, `v4-cmyk-axis`, `v4-cmyk-outputs`
- v6 CSS defined: `v4-cmyk-hero`, `v4-cmyk-process`, `v4-cmyk-apps`, `v4-cmyk-evidence-bar`, `v4-cmyk-substrates`, `v4-cmyk-qa`

The v5 HTML rendered with zero styling because none of its classes matched.

**Fix pattern**: After any v5→v6 copy:
1. Read the v6 CSS file for the targeted page class (e.g., `.v4-cmyk` rules in `38-cmyk.css`)
2. Compare the CSS selectors against the HTML classes
3. If they don't match, **rewrite the HTML** to use v6's CSS classes, not the other way around
4. Verify that all new HTML class names appear as CSS selectors:
   ```bash
   grep -c '\\.v4-cmyk-' v6/css/38-cmyk.css
   ```
5. The v6 CSS already has the right design — the HTML just needs to call the right classes

**NOTE**: The `30-redesign.css` file was split into per-archetype files (`31-cover.css` through `45-overrides.css`) on 2026-06-07. Use the per-archetype file names for grep/verification, not the old monolith. Archetype-to-file mapping:
- v4-cmyk → `38-cmyk.css`
- v4-catalog, v4-tier, v4-prequal → `37-catalog.css`
- v3-method → `35-method.css`
- v4-type → `39-type.css`
- v4-macro → `40-macro.css`
- v4-blueprint → `41-blueprint.css`
- v4-replica-gallery, v4-landmark, v4-materiality → `42-gallery.css`
- v4-scan-meth → `43-scan.css`
- v4-about → `33-about.css`
- v4-scope, v4-atelier, v4-mosaic → `36-scope.css`

## Page Merge Pattern

When merging two pages (e.g., empty p13 + photo-led p13a-1):

1. **Replace** the first page's inner `<div class="content">...</div>` with the merged content
2. **Remove** the second page's `<section>...</section>` block entirely
3. **Do NOT renumber** subsequent pages unless the removed page was the only one with its number
4. Update any section-tag text that referenced the old page structure
5. Verify all image paths in the merged content — old content may have stale paths like `../samaya-web/assets/...` instead of `../assets/...`

**Python merge approach**:
```python
import re
pat = r'<section[^>]*id="p13"[^>]*>.*?</section>'
html = re.sub(pat, new_merged_section, html, count=1, flags=re.DOTALL)
pat2 = r'<section[^>]*id="p13a-1"[^>]*>.*?</section>\n'
html = re.sub(pat2, '', html, count=1, flags=re.DOTALL)
```

## No-Deploy Workflow

## No-Deploy Workflow

When the user says "Do not deploy" or "Work locally only":
1. **Do NOT run surge** or any deploy command
2. Make changes to `v6/index.html` and `v6/css/*.css` only
3. Verify images exist on disk (no `curl` to surge URLs)
4. Show the change summary to the user
5. Wait for explicit approval before deploying
6. The `surge` deploy script in the skill must NOT run during no-deploy sessions
7. Deploy verification checks (curl, surge list) must be skipped entirely

## User-Enforced: No Deploy Without Explicit Approval

The user explicitly said: "dont deploy to surge without i asked you to deploy." This overrides any workflow pattern that assumes auto-deploy. Every change cycle must end with asking, not deploying.
| 05 Handover | M4 4h12v12H4zM8 8h6M8 12h6 (box) |

CSS: `.v3-method .v3-method-tl-icon { inline-size: 7mm; block-size: 7mm; flex-shrink: 0; }`. Keep the small number (10pt italic) beside the icon.

## Page Merge Pattern

**Note**: The old SVG Text Shadow Removal Pattern is superseded. The user now requires ALL text-shadows removed globally — see "No Text Shadows" above.



When merging two pages (e.g., empty p13 + photo-led p13a-1):

1. **Replace** the first page's inner `<div class="content">...</div>` with the merged content
2. **Remove** the second page's `<section>...</section>` block entirely
3. **Do NOT renumber** subsequent pages unless the removed page was the only one with its number
4. Update any section-tag text that referenced the old page structure
5. Verify all image paths in the merged content — old content may have stale paths like `../samaya-web/assets/...` instead of `../assets/...`

**Python merge approach**:
```python
import re
pat = r'<section[^>]*id="p13"[^>]*>.*?</section>'
html = re.sub(pat, new_merged_section, html, count=1, flags=re.DOTALL)
pat2 = r'<section[^>]*id="p13a-1"[^>]*>.*?</section>\n'
html = re.sub(pat2, '', html, count=1, flags=re.DOTALL)
```

## Photo Uniqueness — Mandatory Across Entire Profile

The user explicitly enforces: **every photo must be used only once** across the entire profile. No exceptions for galleries, thumbnails, or repeated backgrounds.

After any batch photo replacement, verify uniqueness:
```python
import re
from collections import Counter
with open("v6/index.html") as f: html = f.read()
refs = [m.group() for m in re.finditer(r'\.\./assets/[^"\')\s]+', html)]
dupes = {k:v for k,v in Counter(refs).items() if v > 1}
print(f"Duplicate images: {len(dupes)}")
for img, count in sorted(dupes.items()): print(f"  {img} ({count}x)")
```

**Remediation**:
1. Identify which occurrences to replace (2nd+ occurrence)
2. Find a single-use image from the same directory or context
3. Use `patch()` to replace the second occurrence URL
4. Re-run the dedup check — repeat until zero duplicates

**Pitfall**: Replacing duplicates can create NEW duplicates if the replacement image was already used elsewhere. After each replacement, re-run the check.

## Page Number Audit

After structural edits (pages added/removed/renumbered), compare v5 and v6 page sections:
```python
import re
with open("v5/index.html") as f: v5 = f.read()
with open("v6/index.html") as f: v6 = f.read()
for v in [v5, v6]:
    ids = re.findall(r'<section[^>]*id="([^"]+)"', v)
    print(f"{len(ids)} sections: {ids}")
```

This catches pages that were accidentally duplicated or lost during merge operations.

## Post-Edit QC Pipeline (MANDATORY)
After ANY edit that changes page layout, photos, or content:
1. **Claude audits** — checks all pages for overflow (height:calc patterns, overflow:hidden, content height vs 174mm available)
2. **Kimi fixes** — applies CSS fixes (reduces sizes, removes height constraints, removes overflow:hidden)
3. **Codex verifies** — checks TOC accuracy and page count
4. Never skip any step in the pipeline

### CHANGELOG Patch Pitfall — Heading Mangling

When inserting a new entry at the TOP of CHANGELOG.md, the patch's `old_string` must include the `## v6.X` prefix WITH the `##`:

**WRONG** — `old_string: "v6.6 — Overflow Audit"` → heading text merges with backup line
**RIGHT** — `old_string: "## v6.6 — Overflow Audit"` → full heading preserved on its own line

**Failure mechanism**: If `old_string` omits `##`, the fuzzy matcher finds the text but replacement doesn't include `##`, producing: `Backup: \`path\` — v6.6 — Title` (merged).

**Always verify after a CHANGELOG patch**: Read first 20 lines. If previous heading got merged, fix:
```
old_string: "Backup: \`path\` — v6.X — Title"
new_string: "Backup: \`path\`\n\n## v6.X — Title"
```

**Best practice**: Use full `## v6.X — Title` as old_string. End new entry with `Backup: \`path\`\n\n## v6.X — Title`.

### Internet Photo Sourcing (Placeholder Workflow)

When a redesigned section needs photos that don't exist in project assets:

1. **Try Wikimedia Commons API first** (least blocking):
   ```bash
   curl -s "https://commons.wikimedia.org/w/api.php?action=query&list=search&srsearch=KEYWORD&format=json&srlimit=10"
   ```
   Then fetch image URLs via `imageinfo` API. Rate limit: ~5 requests before 429.

2. **Fallback: Wikipedia articles** — navigate via browser, use `browser_get_images` to find usable photos, download with curl.

3. **Name convention**: `section-photo-01.jpg` through `NN.jpg` in appropriate `assets/img/NN-SECTION/`.

4. **Update HTML**: Point existing `background-image:url(...)` refs to new placeholder paths.

5. **Alert the user**: "These temp photos can be replaced — drop your files into `assets/img/NN-SECTION/`."

**NOT compatible**: Unsplash, Pexels, Pixabay, Google Images — blocked by Cloudflare/anti-bot.

### Post-Split TOC Cross-Check

After splitting any page into 2+ pages (e.g., p14 → p14 + p14b):

1. **Verify both sections exist** in index.html.

2. **Verify TOC has entries for all new pages** — grep `href="#p14b"` in TOC region.

3. **Verify no dead TOC links** — every `href="#p..."` must match an `<section id="p...">`:
```python
import re
with open("v6/index.html") as f: html = f.read()
toc = {m.group(1) for m in re.finditer(r'href="#(p[^"]*)"', html)}
sids = {m.group(1) for m in re.finditer(r'<section[^>]*id="(p[^"]*)"', html)}
print(f"Dead: {toc - sids}")
```

4. **Footer sibling pattern**: Sub-page footer numbers must use LETTER SUFFIXES (p14b→`14b`, p15b→`15b`, p19b→`17b`), not sequential numbers. Do NOT use `18` for p19b. Verify:
```bash
grep 'class="num">14b\|class="num">15b\|class="num">17b' v6/index.html
```

5. **Adjacent page TOC preserved**: After adding p14b, check p15's TOC entry wasn't accidentally overwritten.

## Overlapping Skills

**Note**: `samaya-company-profile`, `samaya-factory-profile`, and `samaya-profile-editorial` overlap significantly.
- `samaya-factory-profile` is the most current/maintained (this skill)
- `samaya-profile-editorial` is shorter but covers editorial redesign
- `samaya-company-profile` is likely stale

Additionally, a **reference file** at `samaya-technical-office/references/samaya-factory-profile.md` causes a name collision — loading this skill by bare name (`skill_view(name='samaya-factory-profile')`) fails with an ambiguity error. Always use the categorized path: `skill_view(name='productivity/samaya-factory-profile')`.

- **Recommendation**: Consolidate into one skill when possible. `samaya-profile-editorial` already has `related_skills: [samaya-factory-profile]`. The reference file in `samaya-technical-office` should either be absorbed or removed.

## Reference Files
- `references/phantom-photo-path-detection.md` — post-delegation verification for hallucinated image paths
- `references/user-photo-replacement-workflow.md` — gallery label → photo path mapping for user photo swaps
- `references/css-overflow-fixes.md` — common overflow patterns across page types
- `references/session-2026-06-06-redesign.md` — full profile redesign notes (flagship flips, section creation, photo sources)

## CSS Safety
**Never use `write_file` on existing CSS files** — it overwrites the entire file. Always use `patch()` for targeted edits or `terminal()` to append content.

### HTML Inline Style Patch Pitfall
When patching a `<div class="..." style="...">` line to change an inline `background-image` or `background-size`:
- **Double-check quote matching** — the old_string must capture both the `class=` value AND the `style=` value with all quotes intact
- A broken patch (dropping a `"` between `class` and `style` attributes) produces mangled HTML that passes the patch tool's fuzzy matching but renders incorrectly
- After every HTML inline-style patch, read the surrounding 3-5 lines to verify the tag is well-formed:
  ```bash
  grep -n 'v3-method-ecard-img' v6/index.html | head -5
  ```
- **Common failure**: a patch result like `<div class="v3-method-ecard-img style="background-image:...">` — the `"` after `img` is missing, merging `class` and `style` into one broken attribute. Fix by re-patching with correct quotes.

### CSS Class Specificity Conflicts
**Pitfall**: `.ed-spread .content` (specificity 0,2,0) overrides custom section-specific classes (specificity 0,1,0) on pages using `ed-spread` for layout.

Example: p13a used `<section class="page ed-spread">` with `.v4-scan-meth` class on `.content`. The `.ed-spread .content` rule from `20-redesign.css` forced a 2-column grid layout and zero padding, breaking the intended flex layout.

**Fix**: Remove `ed-spread` from the `<section>` when using a custom CSS class that manages its own layout. Only use `ed-spread` for pre-built layout archetypes (HSE, Approvals, After-Sales).

## Flagship Page Layout
Flagship pages (p4-flag4 through p4-flag8, p23a, p23c, p23d) use a 2-column grid: `grid-template-columns: 1.2fr 0.8fr`.
In RTL layout, the first DOM child renders on the RIGHT side (wider column).
To flip hero photo side, swap the DOM order of `.pf-panel` and `.pf-hero` children.

### RTL Alternating Sequence (User Preference)
Flagship pages must **alternate photo side** between consecutive pages for visual rhythm:

| # | Page | Photo Side | DOM Order |
|---|------|-----------|-----------|
| 1 | p23a Khair Al-Khalq | **LEFT** | panel first, hero second |
| 2 | p23c Hira Cultural District | RIGHT | hero first, panel second |
| 3 | p23d Tales of Science | **LEFT** | panel first, hero second |
| 4 | p4-flag4 Quran Museum | RIGHT | hero first, panel second |
| 5 | p4-flag5 Prophet Mosque | **LEFT** | panel first, hero second |
| 6 | p4-flag6 Madinah Royal Reception | RIGHT | hero first, panel second |
| 7 | p4-flag7 Shalayil Pavilion | **LEFT** | panel first, hero second |
| 8 | p4-flag8 Pilgrim Heritage | RIGHT | hero first, panel second |

**Rule**: Odd-numbered flagship pages → panel-first (photo LEFT in RTL). Even-numbered → hero-first (photo RIGHT). This creates a natural back-and-forth reading rhythm.

## RTL 2-Column Layout Audit

After any structural change to 2-column pages, verify photo/hero renders on the RIGHT side in RTL:

**Rule**: In `dir="rtl"`, the first DOM child → inline-start → RIGHT side. Photo/hero must come FIRST in DOM order.

**Pages to check**:
- **Flagship** (p23a-p4-flag8): `.pf-hero` must be before `.pf-panel`
- **ed-spread** (p22, p4-hse, etc.): `.ed-visual` (photo/stat panel) before `.ed-panel` (text)
- **v4-about** (p3): `.v4-about-portrait` (photo) before `.v4-about-essay` (text)

**Fix**: Swap the two child divs in DOM order. Verify with:
```bash
grep -A1 'id="p22"' index.html
# Read first child inside .content
```

**Known correct pages** (photo-first, no fix needed): p3, p4-flag4, p4-flag6, p4-flag8.

**Known fixed pages** (2026-06-09): p22, p23a, p23c, p23d, p4-flag5, p4-flag7.

## Background System — Unifying Page Colors

The profile has a two-tone background system that should be unified to `var(--v3-paper)` warm cream for museum-book consistency.

**Current state**: ~18 pages on cream (`var(--v3-paper)`), ~12 pages on white (`var(--paper)`).

**Pages using white** (should be cream):
- `ed-spread` pages (HSE, Approvals, After-Sales, Certifications, Financial)
- `proj-flagship` pages
- `proj-sectorial` pages  
- `proj-org` page
- `ed-back-cover` (back cover)
- `v4-prequal` (p13) — may hardcode `#FFFFFF`

**Fix pattern** (change each CSS rule to `var(--v3-paper)`):
```css
/* In 18-projects.css */
.proj-flagship { background: var(--v3-paper); }
.proj-sectorial { background: var(--v3-paper); }

/* In 19-org.css */
.proj-org { background: var(--v3-paper); }

/* In 20-redesign.css — add */
.page.ed-spread { background: var(--v3-paper); }

/* In 37-catalog.css */
.page.v4-prequal { background: var(--v3-paper); }

/* In 45-overrides.css */
.ed-back-cover { background: var(--v3-paper); }
```

**Pitfall — `:where(.page)` selector**: The rule `:where(.page) { background: var(--v3-paper); }` in 31-cover.css appears to set all pages to cream but does NOT actually work. `:where()` has **zero CSS specificity** (0,0,0), so the base `.page { background: var(--paper) }` (specificity 0,1,0) always beats it. The v3/v4 pages only get cream because their explicit class selectors override. Remove the `:where()` rule if found — it's dead code that misleads.

## After-Sales & HSE Sections
These use the `ed-spread` layout with:
- Left (navy visual panel): stat counters, process steps
- Right (cream editorial panel): title, narrative, callouts
- Use existing `.ed-*` CSS classes in `17-archetypes.css`

## Prequalification Standards Reference
See `references/prequalification-standards-checklist.md` for the 7-point standards checklist and Aseer Museum relevance criteria. Load this reference when auditing the profile for prequal submission or when updating section content to meet museum-grade framing.

## Print Page (p14) Photo-Driven Redesign
See `references/print-page-photo-redesign.md` for the full pattern. When the user says "photos too small" on the Print Machines page (#p14, class v4-cmyk):
1. Remove the 45-overrides.css fit-fix block (#p14 lines with block-size/min-block-size)
2. Split into 2 pages (p14 + p14b) — hero+machines on page 1, process+QA on page 2
3. Add new CSS to 38-cmyk.css for enlarged photos (hero 85mm, machine cards 42mm, evidence 32mm, QA 50mm)
4. Update TOC with p14b sub-entry and verify p15 entry exists
5. Fix p14b footer to "14b"

## Photo Asset Classification
Load `samaya-profile-photo-assets` skill before any photo work — it documents all classified photos across machinery, QA lab, hardware, packaging, project work, and 3D scanning assets.

## No Brand Names Rule (3D Scanning Sections)
In ALL 3D scanning sections:
- **Never mention** scanner brand (Artec, EinScan, Shining 3D, FARO, etc.)
- **Never mention** scanner model (Spider, Spider II, etc.)
- **Never mention** supplier, manufacturer, or software brand
- Use only generic technical terminology: \"Structured blue light 3D scanning\", \"Blue LED\", \"No laser\"
- Describe the capability, not the product
- Reference standards generically: \"Calibration follows VDI/VDE 2634 Blatt 3:2008-12\" (ok to name the standard)
- For technical parameters, use exact values from the calibration certificate / proposal

## Step-by-Step Big Task Pattern (User-Enforced)
For large multi-page redesigns or layout fixes:
1. **Break into small controlled sub-tasks** — never rewrite the full profile in one pass
2. After each sub-task, check the result before moving to the next
3. Use `delegate_task` with single-focused goals (one goal per agent call)
4. Monitor progress between sub-tasks with CLI checks
5. Never try to patch 3+ files in a single agent call — it causes conflicts and missed edits
6. If a fix doesn't work on first try, stop and diagnose the root cause before fixing again

**Pitfall**: Patching the same section twice in rapid succession causes "file was modified by sibling subagent" warnings. Wait for the previous agent to complete fully before issuing the next patch on the same file.

## Terminology Rules — Critical for Factory Prequalification

### "Workshop" → Always "Factory"
The user explicitly enforces: **Never say "ورشة" (workshop) — always say "مصنع" (factory).**
This applies to ALL user-facing Arabic text. Key replacements:
- "ورشـتنـا" → "مصنعنـا" (our workshop → our factory)
- "ورشة واحدة" → "مصنع واحد" (one workshop → one factory)
- "ورشة النحت" → "قسم النحت" (sculpture workshop → sculpture department)
- "من ورشة سمايا" → "من مصنع سمايا" (from Samaya workshop → from Samaya factory)
- "رسم الورشة" → "رسم التصنيع" (workshop drawing → fabrication drawing)
- "ستّ ورشٍ" → "خطوط إنتاج" (six workshops → production lines)
- "ورش إنتاج" → "خطوط إنتاج" (production workshops → production lines)
- "الورشة" → "المصنع" (the workshop → the factory)
- English "atelier" → "factory" when referring to the production facility
- English "workshop" → "factory" or "production unit" in user-facing text

Internal code (HTML comments, CSS class names containing "workshop", photo filenames) can remain as-is since they're invisible to users.

### "Factory" terminology in English
Use "factory" consistently:
- "Riyadh factory" (not "atelier", not "workshop")
- "production lines" (not "workshops")
- "fabrication" or "production" (not "craft" for factory capability)
- "at the factory" (not "in our workshop")

**Pitfall: Subagent CSS height stripping**: After any subagent CSS edit, run:
```bash
grep -c '210mm' v6/css/*.css
```
If the count dropped from previous session, subagent silently removed height constraints. Recheck all `.content` blocks that had `height: calc(210mm - 22mm - 14mm)` — common victims: `proj-sectorial`, `proj-org`, `v3-toc`, `v4-replica-gallery`, `v3-method`.

## 3D Scanning Prequalification Spec Reference
See `references/scanning-prequalification-specs.md` for the exact technical specifications table.
Load this when designing 3D scanning capability pages for prequalification submissions.

## External SVG File Pattern

When the org chart or any diagram needs redesigning:

1. **Create a standalone SVG file** in `assets/brand/` (e.g., `org-chart.svg`)
2. Reference it from HTML via `<object>` tag:
   ```html
   <object type="image/svg+xml" data="../assets/brand/org-chart.svg" aria-label="...">
   </object>
   ```
3. Keep SVG self-contained — embed all `<style>` inside the SVG `<defs>` block
4. Use `viewBox` for responsive sizing
5. **Flat design only** — no shadows, gradients, or 3D effects. Clean corporate style.

### SVG XML Escaping — Critical

**SVG files are XML** — bare `&` characters in attribute values cause parse errors:
```
error on line 1 at column 251: xmlParseEntityRef: no name
```

**Fix**: Always use `&amp;` in SVG attribute values (aria-label, title, any text that contains &):
```xml
<!-- WRONG → parse error -->
<svg aria-label="Admin & Finance">

<!-- RIGHT → valid XML -->
<svg aria-label="Admin &amp; Finance">
```

Note: Inside `<text>` elements already use `&amp;` which is correct for XML text content too.

### Org Chart Content Rules

The user enforces: **Focus on structure, not individuals.** In org chart text:
- Don't single out "the Factory Manager" as a hero figure
- Use language like "The factory operates through four principal directorates supported by six specialized production workshops"
- Headlines should emphasize accountability and structure: "هيكل متكامل · مسؤولية واضحة" / "Integrated Structure. Clear Accountability."
- Remove any "single person controls everything" framing
- Authority callouts per-person should be removed

## Image Reorganization — Safe Procedure

When reorganizing images into new directory structure:

1. **BUILD a file map first** — scan all files in assets/img/ and index by filename:
   ```python
   file_map = {}
   for root, dirs, files in os.walk("assets/img"):
       for f in files:
           rel = os.path.relpath(os.path.join(root, f), "assets/img")
           file_map[f] = rel
   ```

2. **UPDATE all HTML/CSS references** to new paths BEFORE moving files:
   ```python
   import re
   def fix_path(m):
       ref = m.group(0)
       fname = ref.split('/')[-1]
       if fname in file_map:
           return f'../assets/img/{file_map[fname]}'
       return ref
   html = re.sub(r'\.\./assets/img/[^"\'\)]+', fix_path, html)
   ```

3. **COPY files** (don't MOVE) to the new directories — this preserves the originals as fallback

4. **CRITICAL: NEVER RENAME files during reorganization** — the subagent added prefixes like `veneer-process-` to filenames when moving, causing 170 broken references. Directory changes only.

5. **Verify** after: count all HTML image refs, ensure all resolve to existing files:
   ```python
   for m in re.finditer(r'\.\./assets/img/[^"\'\)]+', html):
       full = os.path.normpath(os.path.join("..", "assets", m.group(1)))
       assert os.path.isfile(full), f"Missing: {m.group()}"
   ```

### Stale Path Pitfall

After any image reorganization or content migration, some HTML image paths may still reference the **old directory structure**. Two known stale patterns:

1. **`../samaya-web/assets/`** — pre-v6.3 structure. The `samaya-web` directory still exists at the project root with orphaned images. Fix:
   ```bash
   sed -i '' 's|../samaya-web/assets/|../assets/|g' v6/index.html
   ```

2. **`../samaya-wassets/`** — corrupted deploy-build artifact. Fix:
   ```bash
   sed -i '' 's|../samaya-wassets/|../assets/|g' v6/index.html
   ```

3. **Inline `مشاريع سمايا/` paths** — China Treasures photos in #p12 use direct relative paths. These are NOT caught by `../assets/` pattern matching because they don't contain `../assets/`. Migrate them to `assets/img/07-projects/china-treasures-*.jpg` long-term.

After any migration, grep for these stale patterns:
```bash
grep -c 'samaya-web\|samaya-wassets\|مشاريع سمايا' v6/index.html
# Expected: 0 for web/wassets, handle مشاريع سمايا if still present
```

### Materiality Grid
- Class: `.v4-materiality-grid` with `.v4-materiality-cell` (4-column CSS grid)
- Each cell: `.v4-materiality-cell` with `.v4-materiality-cell-img` (background image) + `.v4-materiality-cell-cap`
- Image height: **22mm** with `background-size: contain` to avoid cropping (reduced from 48mm for overflow)
- **Overflow fix**: 64 cells ÷ 4 cols = ~16 rows × 22mm = ~352mm = ~2-3 pages. If still overflowing, reduce to 18mm.
- `grid-auto-rows: auto` (not `1fr`) so rows size to content
- Footer shows process count: update both cell count and footer text (e.g., "MATERIALITY & CRAFT · XX PROCESS DETAILS · 100% IN-HOUSE")
- Photo batch addition pattern: find last cell by `rfind('v4-materiality-cell')`, patch before grid close `</div>`, update count in footer
