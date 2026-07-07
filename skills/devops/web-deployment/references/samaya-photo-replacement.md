# Samaya Profile — HQ Photo Replacement Workflow

Used when replacing low-res site images with high-quality originals from `مشاريع سمايا`.

## Source inventory

- **HQ photos**: `v6/مشاريع سمايا/<project-name>/` — 114 files, ~1.4GB total
- **Site images**: `assets/img/projects/` — 183 files, varies
- **All other site assets**: `assets/img/` (brand/, scope-*, 05-machinery-cnc/, etc.)

## Mapping logic

Each Arabic folder in `مشاريع سمايا` maps to one or more site image paths:

| Arabic folder | Site path patterns |
|---|---|
| متحف الجوف | aljouf-museum.jpg, from-website/aljouf-museum-cover.jpg |
| متحف تبوك | tabuk-museum.jpg, from-website/tabuk-museum-cover.jpg |
| متحف خير الخلق | from-graphite/khair-alkhalq-*, from-work/khair-alkhalq-* |
| متحف قصة الخلق | from-graphite/creation-story-* |
| متحف عالم التمور | from-graphite/world-of-dates-* |
| متحف القرآن الكريم | from-graphite/quran-museum-*, from-website/quran-museum-cover.jpg |
| متحف وبستان الصافية | safiya-museum-garden.jpg, from-website/safiya-museum-cover.jpg |
| حي حراء الثقافي | from-website/hira-cultural-district-cover.jpg, from-work/hira-cultural-district-main-hall.jpg |
| معرض مطايا | from-graphite/mataya-* |
| معرض شلايل | shalayel-exhibit.jpg, from-website/shalayel-falcons-cover.jpg |
| معرض عمارة المسجد النبوي | prophet-mosque-architecture-exhibition/*, prophet-mosque/* |
| معرض كنوز الصين | from-graphite/china-dynasty-costumes.jpg |
| معرض الوحي | revelation-exhibit.jpg, from-website/revelation-cave-cover.jpg |
| معرض جماليات الخط العربي | arabic-calligraphy.jpg, from-website/calligraphy-manuscripts-cover.jpg |
| مركز حكايا علم | hakaia-elm/* |
| مراكز الزوار - شركة علم | from-graphite/visitor-center-*, from-work/visitor-center-* |
| واحة الملك سلمان | from-website/king-salman-oases-cover.jpg |
| فعالية درب مكة | from-graphite/road-to-makkah-corridor.jpg |
| مهرجان الملك عبدالعزيز للإبل | from-graphite/camel-festival-stage.jpg |
| احتفالات عيد الفطر | makkah-eid-events.jpg |

## Selection rule

Pick the **largest file** from each Arabic folder as the replacement — it has the most detail. Use `os.path.getsize()` to sort.

## Duplicate avoidance

Each site image path should get a **different** HQ photo from the same source folder when possible. Copying the same 50MB photo to 4 different site paths wastes bandwidth and blows past Surge size limits.

When a folder has 3-5 photos, cycle through them: assign the largest to the hero/primary path, then sequentially smaller ones to covers/thumbnails. Use `os.listdir()` sorted by size descending, then `zip()` with site paths.

## Optimization after replacement

**Always** run sips optimization after replacement. HQ photos are typically 10-50MB each — unoptimized they'll exceed Surge's free plan limit:

```bash
# Batch resize all JPEGs in projects to max 1920px, Q85
find assets/img/projects/ -type f \( -iname "*.jpg" -o -iname "*.jpeg" \) \
  -exec sips --resampleWidth 1920 --setProperty format jpeg \
    --setProperty formatOptions 85 {} --out {} \;
```

For PNG files over 500KB, convert to JPEG via sips or use pngquant. sips can't resize PNGs if they don't have dimension metadata — convert to JPEG first.

## Wayfinding photos — finished signage only (CRITICAL)

The wayfinding section (p15) was rejected as "total wrong" because it used workshop fabrication photos. **Rule**: every photo on this page must show a **finished installed sign**, not a fabrication-in-progress shot. Workshop/fabrication photos belong in the Materiality grid (p24c).

**Sign family card photo selection (by type):**
- PRIMARY DIRECTIONAL · TOTEM → installed directional totem (e.g., `bespoke-kufic-totem-column.jpg`)
- IDENTIFICATION · WALL PLAQUE → installed wall sign (e.g., `hira-night-signage.jpg`)
- INTERPRETIVE · LECTERN → installed interpretive panel (e.g., `almuzaini-signage-billboard.jpg`)

**Workshop gallery below sign families**: If the user wants to add photos below the 3 sign families, use a separate `.v4-type-workshop` gallery with fabrication process shots — but keep these as a distinct second block, clearly separate from the hero and sign-family cards above.

## Materiality grid multi-page fix (30+ cells)

When the user has added 30+ photos to the Materiality & Craft section and reports them as "verysmall croped cant see it":

**3 CSS changes needed:**
1. `grid-auto-rows: 1fr` → `grid-auto-rows: auto` — rows size to content
2. Image `flex: 1; background-size: cover` → `height: 34mm; background-size: cover`
3. Remove `overflow: hidden` from `.content` — allows multi-page flow

See the main surge-deploy SKILL.md for the full CSS pattern.

## Colour-Managed Print gallery (p14, SCOPE 05)

When adding printing machine photos to the COLOUR-MANAGED PRINT section:

1. Replace the main printer hero photo (`real-printers.jpg` → HQ photo like `durst-printer.jpg`)
2. Add a 3-column gallery below the 4-output strip using class `v4-cmyk-gallery` with `v4-cmyk-gallery-img` items
3. Each item: 32mm height, cover background, gradient caption overlay (same pattern as `.v4-type-workshop-img`)
4. Style: `grid-template-columns: repeat(3, 1fr); gap: 2mm;`

## Operational Capacity overflow fix (p4)

When the OPERATIONAL CAPACITY section overflows:
1. Remove `height: calc(210mm - 22mm - 14mm)` from `.v4-capacity .content`
2. Change `overflow: hidden` → `overflow: visible` on the parent
3. Change `grid-template-rows: auto auto auto 1fr auto` → `auto auto auto auto auto`
4. Add `height: auto; min-height: 210mm` to the page class

The cover uses `assets/img/01-cover/exterior.jpg` (fallback) or `hero-cover.jpg`. When replacing from an external source (e.g. samaya-factory.com):
- Browse the site with `browser_get_images()` to find hero image URLs
- Download with curl, save to `assets/img/01-cover/`
- Update the CSS background reference in `v6/css/30-redesign.css` line 108
- Always optimize after download (resize 1920px, Q85)
