---
name: samaya-company-profile
title: Samaya Factory Company Profile
description: Build, design, and deploy the Samaya Factory bilingual company profile to Surge.sh. Covers asset management, image optimization, SVG chart design, QR generation, and HTML/CSS patching.
triggers:
  - User says "samaya profile", "company profile", "v6", "deploy to surge"
  - User mentions "samaya-factory-profile.surge.sh"
  - File path contains "samaya-profile/"
os: macOS
---

# Samaya Factory Company Profile

## Source structure
- `v6/index.html` — main profile (single HTML, bilingual AR/EN, RTL)
- `v6/css/` — split CSS files (00-tokens.css through 30-redesign.css)
- `assets/` — all images, at parent level of v6/ (DOES NOT live under v6/)
  - `assets/img/projects/` — serves double duty: **project gallery thumbnails** AND **section hero background images**. Not just gallery photos.
- `v6/مشاريع سمايا/` — high-quality original project photos (Arabic-named folders)
- **OneDrive Orders source**: `.../Samaya/Orders/2025/00000 صور واتساب سنة 2025 الورشة/classified/website-ready/01-Finished-Products/` — user-sent WhatsApp project photos in date-stamped filenames (`Finished-Project-YYYYMMDD-NNN.jpg`)

## Deploy protocol — approval required

**DO NOT deploy to Surge unless the user explicitly says "deploy" or "publish".** If they say "fix this page", "redesign", "show me" — stop at local file changes only. Wait for a clear deploy command. This was a user correction.

## CHANGELOG — always update

Every change to the profile must be logged in `profile-info-and-control/CHANGELOG.md` with:
- Date, page(s) affected, change description, author (Hermes/Claude)
- Backup snapshot name (if one was taken)
Append a new row to the version table. This enables undo.

## Code-only backups — not full image backups

Before any set of changes, back up only code files (HTML + CSS), not the 1.4GB+ assets folder:
```bash
BACKUP_DIR="/path/to/v6-backups"
TS="v6-code-$(date +%Y%m%d_%H%M%S)"
mkdir -p "$BACKUP_DIR/$TS/css"
cp v6/index.html "$BACKUP_DIR/$TS/"
cp v6/css/*.css "$BACKUP_DIR/$TS/css/"
```

## Image organization — section-based folders

Images must live in section-based folders, not scattered:
```
assets/img/
  01-cover/   02-about/   03-capacity/    04-engineering/
  05-qa-lab/  06-machinery/  07-projects/  08-scope/
  09-wayfinding/  10-material-samples/  11-process/
  brand/  badges/  vendors/
```
When the user sends a new image, place it in the appropriate section folder with a descriptive English filename (hyphenated, lowercase).

## Content writing — client-focused, not hero narrative

- Focus on organizational capability, not individual roles
- Don't single out any person as a hero (e.g. "the Factory Manager")
- Use collective language: "The factory operates through four directorates"
- Keep factual and concise — 1 sentence per idea
- Bilingual: Arabic first, English second, balanced weight
- Headlines: noun phrase with interpunct — `"هيكل متكامل · مسؤولية واضحة"` / `"Integrated Structure. Clear Accountability."`

## Deployment workflow

### 1. Prepare deploy directory (always from /tmp/)
```
rm -rf /tmp/samaya-profile-deploy
mkdir -p /tmp/samaya-profile-deploy/css
```

### 2. Copy index.html with path fix
The HTML uses `../assets/` paths (relative from v6/ subdirectory). For flat root deployment, fix:
```python
html_fixed = html.replace("../assets/", "assets/")
```

### 3. Copy CSS
```
cp /path/to/v6/css/*.css /tmp/samaya-profile-deploy/css/
```

### 4. Copy only referenced assets (not entire 800MB+ directory)
Extract asset paths from HTML + CSS with regex `\.\./assets/[^"\')\s]+`, strip `../`, copy only those files keeping directory structure. This avoids copying the full 780MB+ assets folder.

### 5. Image optimization
Use macOS `sips` before deploy:
```
# Resize to max 1920px wide, JPEG Q85
sips --resampleWidth 1920 --setProperty format jpeg --setProperty formatOptions 85 file.jpg --out file.jpg
```
Optimize: projects dir (was 1.48GB → 58MB), CNC dir (780MB → 89MB).

### 6. Deploy
```
cd /tmp/samaya-profile-deploy
surge --project ./ --domain samaya-factory-profile.surge.sh
```

## Project photo replacement

When the user says "update project photos from مشاريع سمايا":

1. The `v6/مشاريع سمايا/` folder has high-quality originals in Arabic-named project folders
2. The site uses `assets/img/projects/` with English filenames
3. Map Arabic folder → English site paths (see references/project-photo-mapping.md)
4. For each mapping, pick the largest/best photo from the HQ folder
5. Replace the site image: `shutil.copy2(hq_photo, site_path)`
6. **Each site image should get a unique photo** — don't copy the same photo to multiple paths
7. Always optimize after replacing

## Section hero image replacement

Different from gallery photo updates. Users may send photos from any source (OneDrive Orders/Finished-Products, WhatsApp, etc.) to use as full-width hero backgrounds on profile sections.

### Photo sources (all subfolders)
- **Primary**: `...Samaya/Orders/2025/00000.../01-Finished-Products/` — date-stamped finished-project photos (e.g. `Finished-Project-YYYYMMDD-NNN.jpg`)
- **Workshop environment**: `.../02-Workshop-Environment/` — workshop fabrication/setup photos
- **Material samples**: `.../04-Material-Samples/` — material finish, hardware, and process close-ups
- **Opening Ceremony**: `.../05-Opening-Ceremony/` — event/opening ceremony photos showing replica installations in situ; these often feed the Replicas gallery
- **Best High-Res**: `.../06-Best-High-Res/` — high-quality/high-resolution shots (3-7MB each), often for packing, woodwork, and furniture detail
- **Folder 011**: `.../011/` (no thematic prefix) — mixed content: site installation sub-frames, workshop fabrication, benches. Photos have `Finished-Project-`, `Workshop-`, or `Material-Sample-` prefixes despite being in this folder
- **Secondary**: `مشاريع سمايا/` Arabic-named project folders (same as gallery source)
- **Desktop drop**: When user drags a photo from WhatsApp/iMessage to Desktop, copy from `~/Desktop/<filename>` — no deep OneDrive path needed
- **Downloads/Production/**: User may stock production photos at `~/Downloads/Production/WhatsApp Image <date> at <time> AM/PM (N).jpeg` — these are pre-organized production photos outside the OneDrive structure. Filenames follow the `WhatsApp Image` pattern; use `ls ~/Downloads/Production/` to list available photos.
- **WhatsApp temp**: When user attaches a photo from WhatsApp Desktop, the file lands at `/Users/mohamedessa/Library/Containers/net.whatsapp.WhatsApp/Data/tmp/documents/<UUID>/PHOTO-<date>-<time>-NN.jpg` — check this path when the file isn't in OneDrive or Desktop. The UUID directory changes per attachment — use `ls` to find the actual path.
- **Cross-source**: Photos from **any** source subfolder can go to **any** section. E.g. a Material-Sample photo (showcase label) can go to Wayfinding gallery if it shows signage, or a Workshop-Environment photo can go to Materiality grid. See `references/photo-source-folders.md` for the full directory map.

### Workflow
1. Copy the photo to `assets/img/projects/<meaningful-name>.jpg`
2. Find the hero div in `index.html` — look for `class="v4-scope-hero"` (or similar `v4-*-hero`) with an inline `style="background-image:url(...)"`
3. Update the URL path — always `'../assets/img/projects/<filename>.jpg'` (relative from v6/)
4. No `<img>` tag needed — these are CSS `background-image` on hero divs
5. Verify the file isn't oversized (>3MB); use `sips --resampleWidth 1920 --setProperty format jpeg --setProperty formatOptions 85` if needed

### Hero photo "zoom out" adjustment

When the user says "zoom out" on a hero background image:

1. The CSS is in `v6/css/30-redesign.css`, class `.v4-scope-hero`
2. The property is `background: center/cover no-repeat ...` — `cover` zooms in to fill the container (crops edges)
3. Change `cover` → `contain` to show the entire image without cropping: `background: center/contain no-repeat ...`
4. `contain` may leave background-color bars on sides if the image aspect ratio doesn't match the container
5. If `contain` looks bad (white bars), try a custom `background-size` percentage like `100% auto` or `auto 100%` instead
6. Verify with a hard refresh (Cmd+Shift+R) — Surge CDN may serve stale CSS from edge nodes

### Caption quality rules (USER STRONG PREFERENCE)

This is the #1 user-corrected issue. **Every caption must be descriptive**, not generic.

Rules:
1. **Use what the user tells you**: If they say "packing", write "Packaging & crating · التغليف والتعبئة — تجهيز الشحن". Never write just "Packing".
2. **Embed context**: Include material (acrylic, wood, metal), technique (laser engraving, patina, CNC), and purpose (screen integration, signage, cladding).
3. **Bilingual symmetry**: English label and Arabic description should convey the same information, not just a translation of the keyword.
4. **If unsure → ask**: Do NOT write a generic caption when you can't see the photo. Say "Describe what this shows and I'll write the caption."
5. **Format for `pmat-cell`**: `<strong>Specific EN detail</strong>Arabic description with details`
6. **Format for wayfinding gallery**: `EN LABEL · وصف عربي` — both parts descriptive

**Do NOT use**: "Photo frames" — write "Photo frame fabrication · تصنيع براويز الصور — أعمال التأطير"
**Do NOT use**: "Packing" — write "Packaging & crating · التغليف والتعبئة — حماية المنتجات للشحن"
**Do NOT use**: Long marketing sentences — keep captions to 3-8 words total (EN + AR combined)

If the user says "you have to rewrite description alwayes", STOP and rewrite all pending captions with their specific descriptions added, not just the current one. Ask them to describe each photo briefly and use those exact details.

### Bulk photo addition — Materiality & Craft grid (pmat-grid)

The Materiality & Craft page (p24c) has a `pmat-grid` of photo cells. Users frequently send batches of material sample photos to add.

**Workflow:**
1. Copy photo from any source folder (04-Material-Samples/, Desktop, etc.) to `assets/img/projects/material-samples/<descriptive-name>.jpg`
2. Open `index.html`, find the last `pmat-cell` in the grid (search for `royal-frame-carved-detail` or the last cell you added)
3. Insert new cell(s) between the last cell and the grid's closing `</div>`:
   ```html
   <div class="pmat-cell">
     <div class="pmat-cell-img" style="background-image:url('../assets/img/projects/material-samples/photo-name.jpg');"></div>
     <span class="pmat-cell-cap"><strong>Short EN</strong>وصف عربي</span>
   </div>
   ```
4. Update the footer counter: `MATERIALITY & CRAFT · N PROCESS DETAILS` — increment N
5. **Before deploy**: verify the counter matches the actual cell count (count `pmat-cell` occurrences in the grid section)

**Caption format:** `<strong>English keyword</strong>Arabic description` — keep EN 1-3 words, AR 2-6 words. Be descriptive (include material/technique).

### Adding photos to Wayfinding gallery (v4-type-workshop)

The Wayfinding section (p15) has a gallery `.v4-type-workshop` with `grid-template-columns`. When adding photos:

1. Copy photo to `assets/img/projects/wayfinding/<name>.jpg` (or `assets/img/projects/material-samples/` if it's a material sample repurposed for wayfinding)
2. Add a new `.v4-type-workshop-img` div in the grid
3. Update CSS `grid-template-columns` in `30-redesign.css` to increment the column count (e.g. `1fr 1fr 1fr` → `1fr 1fr 1fr 1fr`) — or switch to `repeat(4, 1fr)` when the count exceeds 4 for a cleaner multi-row layout
4. Use caption format: `EN LABEL · وصف عربي` (capital EN, middle-dot separator)

**Cross-source acceptance**: Photos for the wayfinding gallery can come from any source folder — `02-Workshop-Environment/` (signage fabrication), `04-Material-Samples/` (showcase labels, outdoor signage structures), or `01-Finished-Products/` (installed signage). The user will say "whyfinding section" regardless of the original folder. Check the photo description, not the source folder, to decide placement.

**Grid column scaling**: Each new photo increments the column count. When it reaches 5+ columns, photos become very narrow. Consider capping at 4 columns (`repeat(4, 1fr)`) for a compact 2-row layout when the user sends multiple photos in sequence.

The user may ask to replace a photo in one project section with a photo from another project entirely (e.g., "replace Madinah Royal Reception Banquet Hall with Quran Kareem photo"). 

When this happens:
1. Copy the new photo to the **destination section's asset directory**, not the source section's
2. Use a descriptive filename (`quran-kareem-engraving.jpg`) not the original OneDrive timestamp name
3. Update `background-image:url(...)` in the HTML — the paths are always `'../assets/img/projects/<section>/<filename>.jpg'`
4. Optionally update the `aria-label` to match the new content
5. The old photo file remains in assets (no need to delete) — just the HTML reference changes

### Convenience scripts

Two scripts saved under the skill directory:

| Script | Purpose |
|---|---|
| `scripts/deploy.sh` | Full deploy pipeline: clean, copy, fix paths, copy assets, surge, verify |
| `scripts/copy-deploy-assets.py` | Extract all asset paths from index.html, copy only referenced files |

Run from anywhere: `bash ~/.hermes/skills/productivity/samaya-company-profile/scripts/deploy.sh`

### Flagship page — bottom alignment of small photos with hero

Each flagship project section (§14.x) has a two-column layout: `pf-panel` (narrative + facts + small photos) on one side, `pf-hero` (large background photo) on the other. The user wants `pf-details` (small photos) bottom-aligned with the hero photo.

**Working CSS approach (18-projects.css):**

```css
.proj-flagship .pf-panel {
  padding: 10mm 8mm 4mm 10mm;  /* 4mm bottom = matches hero overlay */
  display: flex; flex-direction: column; gap: 4mm;
}
.proj-flagship .pf-facts {
  flex: 1; min-height: 0;  /* grows to fill space, pushes pf-details to bottom */
}
.proj-flagship .pf-details {
  display: grid; grid-template-columns: 1fr 1fr; gap: 2mm;
  /* NO margin-top: auto — flex:1 on pf-facts does the pushing */
  /* NO padding-bottom — pf-panel bottom padding provides the gap */
}
```

**Why this works:**
- `pf-facts` has `flex: 1` so it expands to fill available height in the flex column
- `pf-details` sits directly after `pf-facts`, naturally pushed to the bottom
- `pf-panel` has `padding-bottom: 4mm` matching `pf-hero-overlay`'s `padding: 4mm 6mm 4mm`
- Both bottom edges align at 4mm from the container bottom
- Grid row height is shared (`grid-template-columns: 1.2fr 0.8fr`) so both columns are the same height

**Visual check**: small photo bottom edge should align with hero overlay text bottom edge. Hard-refresh (Cmd+Shift+R) to verify — Surge CDN may serve stale CSS from edge nodes.

### Comprehensive Scope hero — side-by-side 2-column layout

The COMPREHENSIVE SCOPE section (p5) hero block was redesigned from a single full-width background image to a 2-column side-by-side layout.

**HTML pattern (index.html, lines 1213-1225):**
```html
<div class="v4-scope-hero">
  <div class="v4-scope-hero-col v4-scope-hero-col-a"
       style="background-image:url('../assets/img/projects/quran-museum-hero.jpg');"></div>
  <div class="v4-scope-hero-col v4-scope-hero-col-b"
       style="background-image:url('../assets/img/projects/from-graphite/quran-museum-curved-wall.jpg');"></div>
  <div class="v4-scope-hero-cap">
    <span class="v4-scope-hero-eyebrow">COMPREHENSIVE SCOPE <span>نطاق الأعمال</span></span>
    <h1 class="v4-scope-hero-title">ستة نطاقات متكاملة حول مركز واحد.</h1>
    <p class="v4-scope-hero-tag">Six integrated scopes — orbiting a single delivery core.</p>
  </div>
</div>
```

**CSS approach (30-redesign.css):**
- Parent `.v4-scope-hero` becomes a flex container: `display: flex; flex-flow: row nowrap`
- Each `.v4-scope-hero-col` gets `flex: 1 1 50%; min-block-size: 200px; background: center/cover no-repeat`
- A gold hairline divider between columns: `.v4-scope-hero-col + .v4-scope-hero-col { border-inline-start: 0.5pt solid rgba(162, 141, 98, 0.35); }`
- Caption overlay (`.v4-scope-hero-cap`) remains a sibling in the flex container, overlaying both columns via the parent's `::after` gradient
- The `::after` pseudo-element bottom shading stays on the parent and spans both photos

**Do NOT** keep `background-image` on the parent div when splitting into columns — move it to the individual column divs instead.

### Replacing pipeline photos in-place — do NOT add new blocks

The ENGINEERING & BIM section (p18) has a 4-stage pipeline with photos at each stage. When the user wants to "add photos":

1. **Interpret as REPLACE, not append** — The user wants the pipeline photos updated, not a new gallery block added below
2. The 4 stages are:
   - Stage 01 (MODEL · BIM) — uses `.v4-blueprint-stage-photo` with aria-label "محطّة BIM ثلاثيّة الأبعاد"
   - Stage 02 (SHOP DRAWING) — uses `.v4-blueprint-stage-photo` with aria-label "رسم ورشة تفصيليّ بالتعليقات"
   - Stage 03 (CNC · CAM) — uses `.v4-blueprint-stage-photo` with aria-label "ماكينة CNC تنفّذ شكلًا منحنيًا"
   - Stage 04 (ASSEMBLY · ON-SITE) — uses `.v4-blueprint-stage-photo` with aria-label "فريق التركيب في الموقع — مسجد قباء"
3. Copy new photo to `assets/img/projects/bim/<name>.jpg`
4. Find the exact line with `style="background-image:url(...)"` for the target stage
5. Replace the URL with the new photo path (always `'../assets/img/projects/bim/<name>.jpg'`)
6. Update the `aria-label` to match the new photo content
7. Remove any `background-position` override if present — the default `center` is usually fine

**CRITICAL**: Do NOT add a separate BIM gallery block below the pipeline. The user will say "I mean replace the existing photos dont add new blocks." If you already added one, strip the entire block (HTML + orphan CSS selectors).

### User preference: "use Claude Code for design work"

When the user says "use claude for design work" or "consult claude for design":
1. Read the relevant HTML section + CSS rules first to provide full context
2. Delegate to Claude Code with:
   - Exact file paths
   - Current HTML snippet (5-10 lines around the target)
   - Current CSS rules for the section
   - Brand colors, fonts, layout dimensions
   - The specific change requested
   - Instructions to return patch-format output (old_string/new_string)
3. Verify the patches applied correctly before deploying
4. Applies to: section redesigns, new layout patterns, SVG org chart changes, and any non-trivial visual restructuring

### Which section layout patterns exist
| Section | Hero/gallery class | Photo slot type |
|---|---|---|
| Comprehensive Scope (p5) | `.v4-scope-hero` | Full-width background-image hero |
| FF&E (p7) | `.v4-atelier-hero` | Full-width background-image hero with cap overlay |
| Display & Experience (p12) | `.v4-catalog-col-img` | 4-column grid, each has background-image |
| Replicas & Models (p13) | `.v4-tier-tile-img` / `.v4-tier-featured` | 3-tier grid tiles + 3D scanning section below |
| 3D Scanning (p13a) | `.v4-scan-photo` / `.v4-scan-body` | Standalone methodology section with hero, 4-step text, stats, comparison gallery |
| Wayfinding (p15) | `.v4-type-workshop-img` | Gallery at bottom of page — N-column grid |
| Wayfinding (p15) | `.v4-type-workshop-img` | Gallery at bottom of page — N-column grid, update `grid-template-columns` in CSS when adding photos |
| Materiality & Craft (p24c) | `.pmat-cell-img` | `pmat-grid` — grid of cell images with bilingual captions |
| Flagship sections (p4-flag*) | `.pf-detail` / `.pf-hero` | Two-column layout: detail grid + hero background |

### Adding a featured gallery to Replicas section — create a separate page

**CRITICAL**: The user explicitly requires work photos to go on a **separate page**, NOT appended to the SCOPE 04 page (p13). If you add the gallery inside p13, the user will say "why you cancel the SCOPE 04 page its very important you can add another page for work photos but dont replace".

The correct approach is to create a **new standalone page** between p13 and p14:

1. Copy photos to `assets/img/projects/replicas/<name>.jpg`
2. Insert a new `<section>` between p13's closing `</section>` and p14's opening `<section>`:
   ```html
   <section class="page v4-replica-gallery" id="p13b" dir="rtl">
     <header class="page-header">
       <div class="brand"><span class="dot"></span> SAMAYA FACTORY</div>
       <div class="section-tag">11b · REPLICA WORKS GALLERY</div>
     </header>
     <div class="content">
       <div class="v4-replica-gallery-head">
         <span class="v4-replica-gallery-eyebrow">REPLICA PROJECTS GALLERY <span>معرض أعمال المستنسخات</span></span>
         <h2 class="v4-replica-gallery-title">نماذج <em>متحفيّة</em> — من التصنيع إلى الافتتاح.</h2>
         <p class="v4-replica-gallery-tag">Museum-grade replicas, models, and exhibition works — from fabrication to opening ceremony.</p>
       </div>
       <div class="v4-replica-gallery-grid">
         <div class="v4-replica-gallery-item" style="background-image:url('...');">
           <div class="v4-replica-gallery-cap">
             <span class="v4-replica-gallery-en">EN LABEL · وصف عربي</span>
             <span class="v4-replica-gallery-ar">وصف عربي بالتفصيل</span>
           </div>
         </div>
         <!-- more items... -->
       </div>
     </div>
     <footer class="page-footer">
       <div>REPLICA WORKS GALLERY · N PROJECTS</div>
       <div class="num">13b</div>
     </footer>
   </section>
   ```
3. Add CSS in `30-redesign.css`:
   ```css
   .v4-replica-gallery { background: var(--v3-paper); }
   .v4-replica-gallery .content {
     padding: 5mm 6mm 6mm;
     display: flex; flex-direction: column; gap: 3mm;
   }
   .v4-replica-gallery-head { display: flex; flex-direction: column; gap: 1mm; }
   .v4-replica-gallery-eyebrow {
     font-family: 'Inter', sans-serif; font-size: 10pt; font-weight: 700;
     letter-spacing: 0.24em; color: var(--v3-gold-dark); text-transform: uppercase;
   }
   .v4-replica-gallery-title {
     font-family: 'Tajawal', sans-serif; font-weight: 800; font-size: 20pt;
     color: var(--v3-ink); line-height: 1.15;
   }
   .v4-replica-gallery-title em { color: var(--v3-gold-dark); font-style: normal; }
   .v4-replica-gallery-tag {
     font-family: 'Cormorant Garamond', serif;
     font-style: italic; font-size: 10pt; color: var(--v3-ink-soft);
   }
   .v4-replica-gallery-grid {
     display: grid; grid-template-columns: repeat(3, 1fr);
     gap: 2mm; flex: 1;
   }
   .v4-replica-gallery-item {
     position: relative; background: center/cover no-repeat var(--v3-line-soft);
     height: 52mm; border: 0.4pt solid var(--v3-line); overflow: hidden;
   }
   .v4-replica-gallery-cap {
     position: absolute; inset-inline: 0; bottom: 0;
     background: linear-gradient(to top, rgba(11,31,63,0.85), transparent);
     padding: 3mm 4mm 2mm; display: flex; flex-direction: column; gap: 0.3mm;
   }
   .v4-replica-gallery-en {
     font-family: 'Inter', sans-serif; font-size: 7pt; font-weight: 600;
     letter-spacing: 0.06em; color: var(--paper); display: block;
   }
   .v4-replica-gallery-ar {
     font-family: 'Tajawal', sans-serif; font-size: 6.5pt;
     color: var(--gold-light); display: block;
   }
   ```
4. Grid uses 3 columns for balanced item sizes (52mm height per item). For 9 items: 3 rows of 3. For other counts, adjust `grid-template-columns` to maintain visual balance.
5. Use `id="p13b"` and page number `13b` in the footer to denote it's a sub-page of the Replicas section.
6. The section-tag reads `11b · REPLICA WORKS GALLERY` to match the SCOPE 04 numbering.

**Cross-folder sourcing**: Photos for the replica gallery come from `05-Opening-Ceremony/` (opening ceremony event photos), `01-Finished-Products/`, or the user's Desktop — not just from a dedicated replicas folder.

**Caption format**: EN label with middle-dot + AR description in the same line for the header row within the overlay:
```html
<span class="v4-replica-gallery-en">EN LABEL · وصف عربي</span>
<span class="v4-replica-gallery-ar">وصف عربي بالتفصيل</span>
```

**OLD/INCORRECT approach (do NOT use)**: Previously, the gallery was added inside p13 as a `.v4-tier-gallery` grid appended after the `.v4-tier-grid`. This caused the SCOPE 04 first page to be pushed down/crowded, which the user explicitly rejected. Always create p13b instead.

### Extracting an inline section into its own page

When the user says "this content needs to be in a separate page" (e.g. 3D Scanning Methodology was embedded inside page 13):

1. Read the full section HTML block you need to extract
2. Create a new `<section>` with proper page shell:
   - `<header>` with brand div and section-tag
   - `<div class="content">` with `height:calc(210mm - 22mm - 14mm); overflow:hidden` (inline style if the page doesn't have its own CSS class)
   - The section content wrapped in its original div structure (`.v4-scan-section` etc.)
   - `<footer class="page-footer">` with section name and page number
3. Insert the new section **between** the old page's `</section>` and the next page's `<section>`
4. **Remove** the original section HTML from the old page using Python string-position surgery — NOT patch matching on the duplicated text (which will match the new copy too):

```python
# Find p13, locate where scan section starts (after tier grid div ends),
# find the </div> before <footer>, remove everything between
content_close = html.find('\\n  </div>', scan_section_start)
footer_start = html.find('<footer class="page-footer">', content_close)
new_html = html[:content_close] + '\\n  </div>\\n\\n' + html[footer_start:]
```

5. Remove any CSS that was specific to it being a **sub-section** (e.g. `.v4-scan-section` had `margin-block-start: 5mm` — remove it now that it's a standalone page)
6. Choose an ID between existing pages (e.g. `p13a` between p13 and p13b)

### Replicas & Models section

The Replicas section (p13) has:
- 3-tier grid: Museum Grade (6 col), Scenography Grade (4 col), Arch. Model (2 col)
- Optional `.v4-tier-featured` hero banner below the grid for important showcase pieces
- The banner uses the same visual language as the flagship hero overlays

### Text example → photo match rule

When a tile's description text cites a **specific artifact as an example** (e.g., "مثال: باب الكعبة بالنقش والتذهيب الكامل" in the Museum Grade tile), the tile's photo should show **that exact artifact**. Do NOT use a generic hero photo or a model overview — the user expects the photo to visually match the textual example.

For the Kaaba door (Tile 01 · MUSEUM GRADE):

## Image deduplication (no repeated photos)

The user requires **every image to be used exactly once** across the entire profile. After any batch photo replacement (HQ project photos, new hero images, etc.), run a dedup check.

### CRITICAL: User will correct you if you add blocks they didn't ask for

When the user says "add photos" or "replace photo" — do EXACTLY that specific action. 

- **"add photos" → replace existing photos** in the pipeline/gallery blocks, do NOT create new sections or new gallery rows
- **"replace photo X" → only change that one photo URL**, do NOT restructure the surrounding layout
- If you already added a new block by mistake, **remove it immediately** when they correct you (remove both HTML block and orphaned CSS)

The user prefers you REMOVE the wrongly-added block rather than leave it. This applies to:
- Engineering pipeline stages (p18) — "add photos to BIM" means replace the stage photos, not add a gallery below
- Wayfinding gallery — "add photos" means append to existing `.v4-type-workshop` grid, not create a new section
- Replicas gallery — "add photos" means add to the standalone p13b page, not inside the SCOPE 04 page
- Materiality grid — "add photos" means append new `.pmat-cell` to existing grid, not create new section

When in doubt, read the existing section structure first to see if there's already a gallery/photos block that accepts more items. If there is, use it. If there isn't, it probably means the user wants you to replace existing photos, not add a new block.

### Deploy script: handle URL-encoded filenames

Some files on disk have spaces in their names (e.g. `Oddy Test_Lab.jpg`) but are referenced in the HTML as URL-encoded (`Oddy%20Test_Lab.jpg`). The deploy's `unquote()` must be applied to BOTH the source path AND the destination path:

```python
from urllib.parse import unquote

for rp in paths:
    c = rp.replace("../", "", 1)
    dc = unquote(c)  # DECODE destination too — Surge decodes URLs before file lookup
    sp = os.path.join(src, c)
    dp = os.path.join(dst, dc)  # ← NOT os.path.join(dst, c)
    if os.path.isfile(sp):
        shutil.copy2(sp, dp)
    else:
        d = unquote(sp)
        if os.path.isfile(d):
            shutil.copy2(d, dp)
```

Without this fix, Surge stores the file with `%20` in the filename, then decodes the URL request to look for a space — 404 every time.

### Dedup workflow

```python
import re
from collections import Counter

with open("v6/index.html") as f:
    html = f.read()

refs = Counter()
for m in re.finditer(r'\.\./assets/img/[^"\')\s]+', html):
    refs[m.group()] += 1

dupes = {k: v for k, v in refs.items() if v > 1}
```

The goal is **zero duplicates** — every image path appears exactly once.

### Fixing duplicates

For each duplicate (x2, x3, etc.), replace the 2nd+ occurrence with a different image:

1. **Find unused images**: scan `assets/img/projects/` subdirectories for files NOT in `refs` keys
2. **Prefer context-appropriate replacements**: same project category, same subdirectory
3. **Use a running set**: track already-used images to avoid creating new duplicates

```python
all_refs = Counter()
for m in re.finditer(r'\.\./assets/img/[^"\')\s]+', html):
    all_refs[m.group()] += 1

# Images used exactly once = safe pool
safe = {k for k, v in all_refs.items() if v == 1}

# All available images in asset dirs
all_available = set()
for dir_path in ["projects/from-work", "projects/from-graphite", "projects/from-website", ...]:
    for f in os.listdir(base + "/assets/img/" + dir_path):
        all_available.add(f"../assets/img/{dir_path}/{f}")

# Unused = available but not referenced at all
unused = all_available - set(all_refs.keys())

# Replace 2nd+ occurrence of each duplicate with an unused image
for dup_path in sorted(dupes):
    count = 0
    pos = 0
    while True:
        idx = html.find(dup_path, pos)
        if idx == -1: break
        count += 1
        if count >= 2:
            replacement = unused.pop()
            html = html[:idx] + replacement + html[idx+len(dup_path):]
            break
        pos = idx + 1
```

4. Rerun the counter check until zero duplicates
5. Rebuild deploy and deploy

### Prevent duplicates during photo replacement

When replacing site images with HQ photos from `مشاريع سمايا`:
- **Never copy the same HQ photo to multiple site paths**
- Each site image should get a different photo from the same project folder
- If a project folder has fewer photos than its site slots, use photos from related projects or from-work/from-graphite alternatives

## Org chart SVG (Page 26 — Organizational Chart)

### Mermaid-to-SVG translation pattern

When the user provides a Mermaid flowchart as a reference for the org chart structure:

1. **Read the mermaid structure** — note parent-child relationships, box styling classes (dark/gold/white), and dotted line annotations
2. **Translate to flat SVG** with explicit x/y coordinates:
   - Parent entity centered at top
   - Divisions below in a horizontal row
   - Production as an intermediate layer
   - Workshops in 2×3 or similar grid
3. **Line routing rules** (critical for this user):
   - Solid lines connect the main hierarchy: Parent → divisions → production → workshops
   - Dotted gold lines represent functional/matrix reporting — route these OUTSIDE the box areas, not through them
   - All horizontal busbars must be at a y-level that doesn't intersect any box
   - Matrix line labels should be HORIZONTAL, not rotated — rotated labels in tight gaps (50px or less) will overflow visually
   - Each line must end with a segment pointing INTO the target box (arrow direction matches the last segment direction)
4. **Box sizing**: 
   - Verify all text fits within box width. Test the longest English label at given font-size + letter-spacing
   - "FACTORY MANAGEMENT" at 10px + 0.28em ≈ 174px — widen the box or reduce font/letter-spacing
   - Arabic at 15px 800 weight in 170px × 48px box: verify bottom margin (text baseline at y=193, box bottom at y=200 → last pixel of descender at ~y=198 → only 2px margin)
5. **External SVG file**: save to `assets/brand/org-chart.svg`, reference from HTML via `<object>` tag
6. **XML validity**: check bare `&` in aria-labels and text content — use `&amp;` in both attributes and text nodes
7. **No deploy without approval** — user must explicitly say "deploy" after seeing the result

When the user asks to redesign the org chart for readability, apply this pattern:

**Color scheme**: Navy-filled boxes with white text for governance/management nodes, gold-filled box for the Factory Manager hub, paper-colored boxes with navy borders for workshops.

```
Tier 1 (Governance):     Navy fill, dashed border, white Arabic + English
Tier 2 (Hub):            Gold fill (#C9A24B), navy text, navy accent bar at bottom
Tier 3 (Direct Reports): Navy fill, white text (Arabic bold, English 85% opacity, tag 50% opacity)
Tier 4 (Workshops):      Paper fill, navy border, navy Arabic + grey English
```

**viewBox**: start at `900 520` — wider than default to prevent text overflow. If overflow persists, increase width further.

**Key sizing**:
- Governance nodes: 200×40, rx=2
- Hub: 260×58, rx=3  
- Direct function nodes: 140×56, rx=2
- Workshop nodes: 160×40, rx=2 (if Arabic text overflows, increase to 190×40)

**Matrix lines**: Dashed gold (`po-edge--matrix`), stroke-width 0.9, routed cleanly past the hub on both sides with vertical labels at y=180.

**Font sizes inside SVG**:
- Governance Arabic: 12px bold, English: 8px 75% opacity
- Hub Arabic: 17px bold, English: 10px letter-spacing 0.28em
- Direct functions Arabic: 12.5px bold, English: 8px 85% opacity, tag: 6.5px 50% opacity
- Workshop Arabic: 10-11px, English: 7px

**Connection lines**:
- Regular edges: `po-edge` class, stroke-width 0.7
- Governance edges: `po-edge--ext`, stroke-width 0.6, dashed
- Matrix edges: `po-edge--matrix`, stroke-width 0.9, gold dashed, with arrowhead marker

**Bottom band (outside SVG)**:
- 4 stat tiles in CSS (`.po-stats` + `.po-stat`)
- Authority callout (`.po-authority`) with gold left border
- Stat labels at 5.5pt to prevent overflow in narrow columns

### Avoiding overflow

After any SVG resize or text change, check:
1. **Long Arabic labels** like `النجارة وأعمال الخشب` (15 chars at 10-11px ≈ 150-165px) — widen the box to 190px or reduce font to 10px
2. **Stat key labels** like `SPECIALISED ATELIERS` in narrow columns — set `font-size: 5.5pt` with `letter-spacing: 0.12em` and `text-overflow: ellipsis`
3. **SVG viewBox height** — ensure footnotes at y=470-502 fit within viewBox height (520 minimum)
4. **`text-anchor="end"` for RTL Arabic** — right-align text for the RTL reading direction

## SVG chart design (Page 4 — Operational Capacity)

**NOTE**: The user explicitly does NOT want charts on this page. Keep stat counters clean — just numbers with labels, no gauge bars, no SVG data visualizations.

- Use **inline SVG** (`<svg class="v4-cap-chart" viewBox="0 0 180 N"...`) — NOT CSS divs/bars
- viewBox width 180 units minimum to prevent text overflow
- Brand colors via CSS variables: `var(--v3-ink)` navy, `var(--v3-gold-deep)` gold, `var(--v3-gold-pale)` light gold
- Add **abstract geometric icons** per stat (building mark, compass rings, gear/cog, diamond)
- Icons should be minimal line art matching the profile's industrial-refined aesthetic
- Stat key labels at 5.8pt with `text-overflow: ellipsis` to prevent clipping
- Use `text-anchor="end"` for RTL Arabic labels
- Chart types per stat:
  - 8,000m²: dual comparison bars (current vs target) + 6.6× growth badge
  - 53,000m²: bold full gold bar with dashed reference line at current
  - 217 equipment: stacked proportional bar + 2-row color-coded legend
  - 25y: timeline spine with 4 milestone circles

## Standing procedure — overflow + TOC check after any edit

After ANY edit (photo add, text change, layout restructure), run this mandatory pipeline:

1. **Claude audits** — Go through affected pages and find overflow issues (content height > 174mm, `height: calc()` constraints, `overflow: hidden` clipping)
2. **Kimi fixes** — For flagged pages: reduce image sizes, remove `height: calc()` constraints, change `overflow: hidden` → `visible`
3. **Codex verifies** — Check TOC entries match actual page order, numbering, and titles

**Overflow check specifics:**
- Read the section's `.content` CSS rule
- If it has `height: calc(210mm - 22mm - 14mm); overflow: hidden;` and content is dense, remove the constraint
- The user explicitly allows multi-page flow

**TOC update:**
- Open section id="p2" (Table of Contents)
- Verify every entry matches actual page order, numbering, and title
- If pages were added/removed/reordered, update TOC entries and page numbers
- TOC entry format: `<span class="v3-toc-t">SECTION NAME</span><span class="v3-toc-p">NN</span>`

## Slogan is a brand asset — never change

The cover slogan **"صناعة الإرث. هندسة الفنّ." / "Crafting Legacy. Engineering Art."** is the company's brand tagline. Never rewrite, rephrase, or translate it differently. If Claude Code or any subagent changes it during a redesign pass, restore it immediately with `patch()` targeting the exact `<span>` elements in the cover page (id="p1"). Both the Arabic `<h1 class="v3-title-ar">` and English `<p class="v3-title-en">` versions must be restored.

## Aseer Museum exclusion — NEVER appear in profile

The Aseer Regional Museum (متحف عسير الإقليمي) project is still in progress and must NEVER appear anywhere in the profile — not in project listings, key projects cards, landmark deliveries, or any other section. This applies to both Arabic and English references. If found, remove immediately.

## 3D Scanning Prequalification page — no brand names

When designing a 3D scanning prequalification/technical capability page:
- Do NOT mention any device name, brand name, supplier name, or model name (no Artec, Spider, EinScan, Shining 3D)
- Use technical specifications only
- Describe as a technical process, not a product page
- Page structure: Document header → Hero → Capability Cards → Process Flow → Measurement Example → Technical Specs Table → Application Areas → Notes

## Preference: ultra-concise text (do NOT write marketing prose)

The user has repeatedly said "dont talk too much" about profile text and assistant responses. For ALL profile sections:

**Profile text:**
- Keep both AR and EN text under 3-4 lines maximum per section
- Use bullet-point style over paragraphs where possible
- Remove filler words ("comprehensive", "integrated", "full", "complete", "professional")
- One sentence per idea. If you can say it in 3 words instead of 10, do it.
- For process descriptions (e.g., 3D Scanning), use numbered steps with bullet format:
  ```
  ① Setup — artefact on grid · scanner · photogrammetry.
  ② Scan — 30 μm capture · real-time preview.
  ```
- The tag/subtitle line should be 6-12 words maximum

**Do NOT write:**
- "Every museum-grade replica begins with a digital twin — not a guess. Using industrial-grade structured-light scanners..."
- Instead write: "① Setup — artefact on grid · Artec Spider II · photogrammetry. ② Scan — 30 μm capture."

**Assistant responses:**
- Short directive replies. No preamble, no restating the question.
- When the user sends a photo with a label ("sanding machine"): say "Done" or "Added" + brief info. Don't explain what you're about to do.

## Slogan is a brand asset — never change

The cover slogan "صناعة الإرث. هندسة الفنّ." / "Crafting Legacy. Engineering Art." is the company's brand tagline. Never rewrite, rephrase, or translate it differently. If Claude Code changes it during a redesign pass, restore it immediately with patch().

## Flagship hero photo flip (alternating layout)

The flagship project pages (p4-flag4 through p4-flag8) use a two-column grid (`grid-template-columns: 1.2fr 0.8fr`) in RTL. DOM order determines visual order: first child = right column (wider), second child = left column (narrower).

To alternate the hero photo side between flagships:
- **Default** (even flagships): `pf-panel` first → text on right, photo on left
- **Flipped** (odd flagships): `pf-hero` first → photo on right, text on left

Implementation: swap the DOM order of the `<div class="pf-panel">...</div>` and `<div class="pf-hero">...</div>` blocks. No CSS changes needed — the grid + RTL handles the rest.

## Back cover — QR code + phone

### Back cover — fixed page height (prevent stretching)

The back cover page (`.ed-back-cover`, id="p27") uses `height: 100%` internally for its flex layout. When the global `.page` rule was changed from `height: 210mm` to `height: auto; min-height: 210mm`, the back cover stretched because `100%` had no fixed parent to reference. The fix is a specific override:

```css
.ed-back-cover { height: 210mm; overflow: hidden; }
```

This keeps the back cover fixed at exactly one A4 landscape page regardless of other page overflow settings.

### QR inline with text (not below)

The Online column on the last page must show the QR code **inline beside the website text**, not centered below it:
```html
<div style="display:flex; flex-direction:row; align-items:center; gap:3mm;">
  <div style="display:flex; flex-direction:column; flex:1;">
    <span>samaya-factory.com</span>
    <span>info@samaya-factory.com</span>
  </div>
  <div style="border:0.5px solid rgba(201,162,75,.5); border-radius:1mm; padding:1mm; display:inline-flex; flex-shrink:0;">
    <img src="../assets/img/brand/qr-profile.png" alt="QR: samaya-factory.com" style="width:16mm; height:16mm;">
  </div>
</div>
```
- QR at 16mm (not 20mm) — smaller fits better beside text when inline
- Container uses `flex-shrink:0` so QR doesn't collapse on narrow viewports
- Gold border: `0.5px solid rgba(201,162,75,.5)`, `1mm` padding, `1mm` border-radius

- Generate QR: `curl -sL "https://api.qrserver.com/v1/create-qr-code/?size=300x300&data=https://samaya-factory.com&margin=10"`
- Save to `assets/img/brand/qr-profile.png`
- Embed in "Online" column of contact grid, **inline beside the website text** (not centered below it):
```html
<div style="display:flex; flex-direction:row; align-items:center; gap:3mm;">
  <div style="display:flex; flex-direction:column; flex:1;">
    <span>samaya-factory.com</span>
    <span>info@samaya-factory.com</span>
  </div>
  <div style="border:0.5px solid rgba(201,162,75,.5); border-radius:1mm; padding:1mm; display:inline-flex; flex-shrink:0;">
    <img src="../assets/img/brand/qr-profile.png" alt="QR: samaya-factory.com" style="width:16mm; height:16mm;">
  </div>
</div>
```
- The QR container uses `flex-shrink:0` so it doesn't collapse on narrow viewports
- QR at 16mm (not 20mm) when inline — smaller fits better beside text
- Gold border frame: `0.5px solid rgba(201,162,75,.5)`, `1mm` padding, `1mm` border-radius

### Subagent side-effect corruption of unrelated sections

When delegating broad HTML redesigns to Claude Code via `delegate_task`, the subagent's patch may accidentally modify OTHER sections of the HTML. This happened when a Wayfinding (p15) redesign corrupted the Hakaia Elm flagship section (p23d) — the pf-hero photo was changed and pf-details were replaced with a text block.

**Prevention protocol:**
1. **Scope-limit context**: Only pass the exact section ID range (e.g., `id="p15"` to its `</section>`) — do not include adjacent sections in the context
2. **Pre-deploy verification**: After Claude patches, run these checks before deploying:
   - `grep -c '<section.*id="'` vs `grep -c '</section>'` — should match
   - Check 2 sections above and below the target for unexpected changes
   - Verify flagship pf-detail/pf-hero counts: `grep -c 'pf-detail'` should match previous count
3. **Known-vulnerable sections** (check these first after any Claude delegation):
   - All `p4-flag*` flagship sections — pf-details and pf-hero are commonly overwritten
   - The `p24*` materiality/landmark pages — pmat-cell content
   - Adjacent sections that share CSS class naming patterns with the target section

### "Play with text" editorial redesign pattern

When the user says "play with text using claude" for editorial/text-heavy pages (HSE, Approvals, After-Sales, etc.):

1. Read the full section HTML to provide complete context
2. Delegate to Claude Code with:
   - The exact section HTML
   - Brand/palette guidelines (navy/gold, fonts, RTL)
   - Request: rewrite the text to be more confident, substantive, and compelling
   - Keep bilingual (AR primary, EN secondary)
   - Preserve all factual claims (numbers, stats, certifications)
   - Request patch-format output
3. After Claude applies changes, verify:
   - Stats/numbers are preserved exactly
   - Arabic reads naturally (check for broken grammar)
   - No HTML structure breakage (open/close tag balance)
4. Pages that got this treatment: HSE (p4-hse), Approvals & Handover (p20), After-Sales (p22)

This is distinct from photo/layout redesigns — it's purely editorial improvement of existing text blocks.

### Design consultation delegation

When the user says "consult Claude Code" for design:
- Read the relevant HTML section + CSS rules first
- Pass to Claude Code with: section context, brand colors, fonts, layout dimensions
- Ask for patch-format output (old_string/new_string)
- Always verify the patches applied correctly before deploying

### Wayfinding page redesign by Claude Code

The Wayfinding page (p15, .v4-type) was redesigned by Claude Code. Key pattern:

**Hero area**: full-bleed photo (workshop-signage-01.jpg) with navy gradient overlay, white Arabic text (قاعة المعروضات at 48-82pt clamp), gold English text (Exhibition Hall). The overlay uses OKLCH colors: `oklch(0.20 0.06 260 / 0.88)` to `0.72` to `0.85`.

**Sign family cards**: 3-column grid, each card has a 16mm photo thumbnail of the actual sign type + Arabic/English description + spec text.

**Workshop gallery**: 5 image tiles at 26mm height, gold-tinted borders, navy gradient overlay captions using OKLCH.

When delegating to Claude Code, read the full section HTML (lines ~1780-1863) and CSS rules (~lines 3476-3690 in 30-redesign.css) and ask for patch-format output.

### 3D Scanning Methodology section

When the user asks to add or redesign the 3D scanning methodology section (within p13 or as p13a):

**Layout structure:**
- Head: eyebrow ("3D SCANNING METHODOLOGY") + title + tag (standard head pattern)
- Body: 2-column split — hero photo (left, 5fr) + text + stats (right, 6fr) (deprecated in favour of the 4-photo layout below)
- Gallery: 3-column comparison grid (actual scan → digital twin per column) (deprecated)
- Reference bar: scanner equipment thumbnail + model name + specs

**Preferred 4-photo narrative layout (user explicitly requested this):**
- **Hero**: Full-width `artec-scanner.jpg` (Artec Spider II scanner device — most credible) with gradient overlay showing step 01 label
- **3-column grid below hero**: 
  - Column 1: `scan-actual-stone-1.jpg` (step 02 — scan in progress)
  - Column 2: `scan-accuracy.jpg` (step 03 — verification screenshot)
  - Column 3: `animal-sculpture-replica.jpg` or `kaaba-door-site.jpg` (step 04 — finished replica)
- Stats row retained (accuracy, point spacing, modalities)
- Reference bar retained with 2 thumbnails (equipment + accuracy)
- **Process text (keep at most 4 lines, user will say "dont talk too much"):**
  ```
  EN: ① Setup — artefact on grid · Artec Spider II · photogrammetry.
       ② Scan — 30 μm geometry capture · real-time preview.
       ③ Process — clean · align · merge · watertight for CNC.
       ④ Verify — ±0.05 mm accuracy · reference grid check · ready.
  AR: ① الإعداد — قطعة على شبكة · ماسح ضوئي · مسح تصويري.
       ② المسح — 30 ميكرون · معاينة فورية.
       ③ المعالجة — تنظيف · محاذاة · دمج · شبكة للتصنيع.
       ④ التحقق — ±0.05 مم · مطابقة · جاهز للإنتاج.
  ```
- **CSS classes**: Use prefix `v4-scan-` — `.v4-scan-hero`, `.v4-scan-hero-img`, `.v4-scan-hero-overlay`, `.v4-scan-step-num`, `.v4-scan-step-en`, `.v4-scan-step-ar`, `.v4-scan-grid`, `.v4-scan-grid-item`, `.v4-scan-grid-img`, `.v4-scan-grid-cap`
- **Photo count**: EXACTLY 4 photos total — no more, no less

**Photo arrangement (hero first, gallery below):**
- Hero should show the **scanner device** (e.g., Artec Spider II) not the stone/artifact — more credible
- Gallery columns show scan-actual-stone before/after with model comparison below each
- All photos use `background-size: cover` consistently (no mixing with contain)
- Scanner reference bar includes a thumbnail of the equipment setup

**Process text (keep ultra-concise — user will say "dont talk too much"):**
```
EN: ① Setup — artefact on grid · Artec Spider II · photogrammetry.
     ② Scan — 30 μm geometry capture · real-time preview.
     ③ Process — clean · align · merge · watertight for CNC.
     ④ Verify — ±0.05 mm accuracy · reference grid check · ready.
AR: ① الإعداد — قطعة على شبكة · ماسح ضوئي · مسح تصويري.
     ② المسح — 30 ميكرون · معاينة فورية.
     ③ المعالجة — تنظيف · محاذاة · دمج · شبكة للتصنيع.
     ④ التحقق — ±0.05 مم · مطابقة · جاهز للإنتاج.
```

**Accuracy stats:** ±0.05 mm accuracy · 30 μm point spacing · 3 scan modalities

**Accuracy screenshot:** When the user shares a screenshot showing accuracy readings, add it to the reference bar as a second thumbnail (gold border to highlight it), next to the equipment setup photo.

**CSS classes:** Use prefix `v4-scan-` for all section styles. See the CSS under Section 21 in 30-redesign.css.

## A4 page overflow prevention

**CRITICAL UPDATE (session 2026-06-06):** The old approach of `height: calc(210mm - 22mm - 14mm); overflow: hidden` on every `.content` causes content clipping when sections have too many elements (materiality 48+ cells, operational capacity with pipeline+evidence+tech stack, replica galleries, HSE/approvals panels). 

### New approach — allow multi-page overflow

Pages that the user adds dense content to MUST have their overflow constraints removed:

```css
.page {
  height: auto;
  min-height: 210mm;  /* start at one A4 landscape page */
  overflow: visible;  /* allow flow to next page */
}
.page .content {
  /* REMOVE: height: calc(210mm - 22mm - 14mm);  — this clips content */
  /* REMOVE: overflow: hidden; */
}
```

**When to fix overflow** (user says "overflow in the page" or photos look clipped):
1. Change global `.page` in `00-tokens.css`: `height: 210mm` → `height: auto; min-height: 210mm`, `overflow: hidden` → `overflow: visible`
2. In each section's CSS file (17-archetypes, 18-projects, 30-redesign, 19-org, 20-redesign): remove `height: calc(210mm - 22mm - 14mm)` and `overflow: hidden` from `.content` rules
3. For grid-based layouts (v4-capacity), also change `grid-template-rows: auto auto auto 1fr auto` → `auto auto auto auto auto` so the 1fr row doesn't squeeze
4. The user explicitly said "you can make more than one page no problem" — multi-page is acceptable

**Sections that need this fix:**
- `proj-materiality .content` (>30 cells)
- `v4-capacity .content` (pipeline + evidence + tech stack)
- `v4-replica-gallery .content` (gallery grids)
- `v4-cmyk .content` (if adding machine gallery)
- Editorial `.ed-spread .content` panels (HSE, approvals, after-sales)

### Materiality grid photo cropping fix

When the user says "photos croped cant see any of it" for the Materiality & Craft grid:

1. Change `background-size: cover` → `background-size: contain` with `background-repeat: no-repeat` on `.proj-materiality .pmat-cell-img`
2. `contain` shows the full image without cropping; the cell background color fills any whitespace gaps
3. If images are still too small, increase `height` (e.g., 34mm → 48mm)
4. `cover` crops to fill the container — never use cover when the user complains about cropping
5. The user will NOT complain about whitespace from contain — they prefer uncropped photos with minor whitespace over cropped photos that fill the frame

**Do NOT** try to fix cropping by increasing cell height alone — `cover` will still crop regardless of container size.
**Do NOT** use `object-fit: contain` — these are CSS background-images, not img tags.

**Replica gallery specific sizing** (9 items in 3×3 grid):
- Item tiles: `height: 46mm` not 52mm (3 × 46mm + 2 × 2mm gaps + header ≈ fits A4)
- Content needs both `height` and `overflow: hidden`

**Verification after overflow fix**: deploy and curl-check the changed CSS:
```bash
curl -s https://domain.surge.sh/css/<file>.css | grep -c 'height: calc'
```
- **Surge free plan limit**: ~1GB max. Optimize images before deploy. The projects directory was 1.48GB after raw HQ photo replacement → must run sips optimization.
- **CSS variables in SVG**: `fill: var(--v3-ink)` works in inline SVGs within HTML. Use `style` attribute not `fill` attribute for CSS variable references.
- **Overflow text**: SVG viewBox must be wide enough for text labels. 180 units works. Add `text-overflow: ellipsis` on stat key labels.
- **Surge cache**: User may see old version after deploy. Tell them Cmd+Shift+R hard refresh. For persistent staleness, add `?v=N` cache-buster to CSS `<link>` in HTML and re-deploy.
- **DO NOT run `surge logout`**: Removes `.netrc` credentials with no recovery path. If accidentally run, recover in this order:
  1. **Plan A (fastest)**: Write `.netrc` directly if you have the password:
     ```
     echo -e "machine surge.sh\n  login mohamedsultanabbas@gmail.com\n  password <password>" > ~/.netrc
     chmod 600 ~/.netrc
     ```
     Verify: `surge whoami` should return the email. If it says "Not Authenticated", try with `machine api.surge.sh` as the hostname instead — surge checks both.
  2. **Plan B (interactive PTY)**: Use terminal(pty=true, background=true) with process(submit) for email/password:
     - `terminal(command='surge login', pty=true, background=true, notify_on_complete=true)`
     - `process(action='log', session_id=...)` — wait for `email:` prompt
     - `process(action='submit', data='mohamedsultanabbas@gmail.com', session_id=...)`
     - `process(action='poll', session_id=...)` — wait for `password:` prompt
     - `process(action='submit', data='<password>', session_id=...)`
     - `process(action='wait', session_id=..., timeout=10)` — check for "Success - Logged in"
     - Verify: `surge whoami`
  3. **Plan C (user's own terminal)**: If PTY pipes fail with special characters (@, #, $), ask the user to run `surge login` directly in their terminal — they can enter credentials interactively.
  2. `process(action='log', session_id=...)` — wait for `email:` prompt
  3. `process(action='submit', data='mohamedsultanabbas@gmail.com', session_id=...)` — send email
  4. `process(action='poll', session_id=...)` — wait for `password:` prompt (check log output)
  5. `process(action='submit', data='<password>', session_id=...)` — send password
  6. `process(action='wait', session_id=..., timeout=10)` — wait for "Success - Logged in" or re-prompt
  7. Verify: `terminal(command='surge whoami')` should return the email
  8. **If password rejected via PTY pipe**: Ask the user to run `surge login` directly in their own terminal. Piped PTY input occasionally fails with special characters (@, #, $). The user can enter credentials themselves through an interactive PTY session — start with `terminal(command='surge login', pty=true)` (foreground, no background) so the session blocks and the user can see the prompts.
  9. If the user provides the password but PTY rejections persist, try writing the `.netrc` file directly:
     ```
     echo -e "machine surge.sh\n  login mohamedsultanabbas@gmail.com\n  password <password>" > ~/.netrc
     chmod 600 ~/.netrc
     ```
     Then verify with `surge whoami`. If still rejected, the password is definitely wrong — use the interactive approach instead.
  10. After successful login, proceed with deploy immediately — the session token is valid for that terminal session.
- **Surge cache gotcha**: `curl` right after deploy may hit a stale edge node. Wait 5-10s and retry. Verify specific content (grep for the changed string), not just HTTP 200. If cache persists after multiple redeploys, increment `?v=N` each time (`?v=2`, `?v=3`, etc.) until the browser and edge nodes pick up the new file.
- **Surge auth persistence**: If `surge whoami` says "Not Authenticated" after a successful login, the `.netrc` file was removed. Do NOT run `surge logout` — this deletes the netrc credentials. If accidentally logged out, recover via `printf "email\\npassword\\n" | surge login` or PTY-based interaction (see "Surge auth recovery" pitfall above).
- **write_file WILL OVERWRITE entire CSS files**: `write_file()` on an existing CSS file replaces ALL content, not just appends. If you intend to add a single rule to a CSS file, use `patch()` or `terminal(cat >>)` instead. When `write_file` on 30-redesign.css was called with just 2 lines of CSS, the entire 4276-line file was destroyed. 
  
  **Recovery protocol:**
  1. Check if the v5/ directory has the file — copy from the nearest version:
     ```
     cp "/path/to/v5/css/30-redesign.css" "/path/to/v6/css/30-redesign.css"
     ```
  2. Use `skills_list` and check `samaya-web/`, `v4/`, `v3/` subdirectories for working copies
  3. If no local backup exists, download from Surge CDN (may also be corrupted if the bad file was already deployed):
     ```
     curl -sL "https://domain.surge.sh/css/30-redesign.css" -o /tmp/recovery.css
     ```
  4. After restore from v5 backup, re-apply all CSS changes made during the current session (check git log or session memory for what changed):
     - Materiality contain + height fix (18-projects.css)
     - Page overflow fixes (00-tokens.css)
     - All new section CSS added this session (scan-section, replica-gallery, cmyk-gallery, etc.)
     - ed-back-cover rule
  5. Verify: `wc -l` should match session memory — if v5 was 3858 lines and the session added ~400+, expect ~4276 lines
  6. Deploy immediately to push the corrected CSS to production
- **aria-label drift**: When replacing a photo in a section (e.g. banquet hall → quran engraving), update the `aria-label` on the image div to match the new content. Stale aria-labels confuse screen readers.
- **Deploy counter drift**

- **Photo caption quality (USER STRONG PREFERENCE)**: Captions must be descriptive - now documented in the dedicated "Caption quality rules" subsection above.
- **Flex + gap + margin-top:auto**: In a flex column with `gap: N`, `margin-top: auto` on the last child may not push it to the very bottom in all browser engines. Instead, give a middle sibling `flex: 1` to absorb remaining space and push the target element down naturally. Used in the flagship page bottom-alignment fix.
- **Deploy counter drift**: When adding cells to pmat-grid (Materiality grid) or photos to v4-type-workshop (Wayfinding gallery), verify footer counters and CSS grid-template-columns match the actual count. After adding cells to pmat-grid, update the footer from "X PROCESS DETAILS" to "X+N PROCESS DETAILS". After adding photos to v4-type-workshop, update `grid-template-columns: 1fr ... 1fr` to match the new column count.
- **Materiality grid overflow / "photos too small" fix (>30 cells)**: When the pmat-grid exceeds 30 cells, `grid-auto-rows: 1fr` makes each row share the page height equally, resulting in 10-14mm rows where images are illegible. The user will say "verysmall croped cant see it". Fix in `18-projects.css`:
  1. Change `.proj-materiality .pmat-grid` `grid-auto-rows: 1fr` → `grid-auto-rows: auto` — rows size to their content, not squeezed into 1/Nth of page height
  2. Replace `.proj-materiality .pmat-cell-img` `flex: 1; background-size: cover; min-height: 0;` with `background-size: cover; height: 34mm;` — fixed image height gives each cell a consistent visible size
  3. Remove `overflow: hidden` from `.proj-materiality .content` — this allows the grid to continue onto multiple pages naturally in print/PDF output
  4. Result: each photo is 34mm tall x ~70mm wide (in 4-col grid), fully visible (cover fills the space without distorting), spanning ~3 pages for 43 cells
  5. The footer counter "N PROCESS DETAILS" becomes the main indicator of how many cells exist across pages

  **Do NOT** try `background-size: contain` to fix cropping — it leaves whitespace bars on the sides and the user will still complain about visibility. `cover` at 34mm height produces acceptable thumbnails across all aspect ratios.

  The user explicitly said "you can make more than one page no problem" — so multi-page overflow is acceptable.
- **CSS column count for gallery grid**: The Wayfinding gallery (`.v4-type-workshop`) uses `grid-template-columns: 1fr ... 1fr`. Each new photo requires incrementing the column count. If grid-columns CSS doesn't match the HTML photo count, the last photo wraps to a new row and looks broken.
- **Bulk photo deploy cycle**: When the user sends many photos one-by-one (common with material samples), each photo requires: copy, HTML patch, counter update, CSS check, deploy. Deploying after every single photo creates long waits. Consider batching: collect 3-5 photos from the user before deploying. However, the user may not wait — deploy each one promptly when sent unless they signal they're done.
