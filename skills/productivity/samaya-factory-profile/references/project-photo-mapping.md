# Project Photo Mapping — مشاريع سمايا → assets/img/projects/

Each Arabic-named folder in `v6/مشاريع سمايا/` maps to one or more English-named files in `assets/img/projects/`. When the user says "update project photos from مشاريع سمايا", use this mapping.

| Arabic Folder | Site Image Path(s) |
|---|---|
| متحف الجوف | aljouf-museum.jpg, from-website/aljouf-museum-cover.jpg |
| متحف تبوك | tabuk-museum.jpg, from-website/tabuk-museum-cover.jpg |
| متحف خير الخلق | from-graphite/khair-alkhalq-creation-stencil.jpg, from-graphite/khair-alkhalq-stencil-creation.jpg, from-work/khair-alkhalq-facade-night.jpg, from-work/khair-alkhalq-hira-cave-replica.jpg |
| متحف قصة الخلق | from-graphite/creation-story-interior.jpg, from-graphite/creation-story-obelisk.jpg |
| متحف عالم التمور | from-graphite/world-of-dates-camel-hall.jpg, from-graphite/world-of-dates-rock-art.jpg |
| متحف القرآن الكريم | from-graphite/quran-museum-curved-wall.jpg, from-graphite/quran-museum-stand.jpg, from-website/quran-museum-cover.jpg, from-work/quran-museum-holographic-display.jpg |
| متحف وبستان الصافية | safiya-museum-garden.jpg, from-website/safiya-museum-cover.jpg, from-work/safia-museum-engineering-cad.jpg |
| حي حراء الثقافي | from-website/hira-cultural-district-cover.jpg, from-work/hira-cultural-district-main-hall.jpg, hira-cultural-district/hira-night-signage.jpg |
| معرض مطايا | from-graphite/mataya-camel-exhibit.jpg, from-graphite/mataya-entrance.jpg |
| جـــادة الإبـــــل - حائــل | from-graphite/camel-festival-stage.jpg |
| معرض شلايل | shalayel-exhibit.jpg, from-website/shalayel-falcons-cover.jpg, from-graphite/shalayil-falcon-mural.jpg, from-graphite/shalayil-led-canopy.jpg |
| معرض عمارة المسجد النبوي | from-website/mosque-architecture-cover.jpg, prophet-mosque-architecture-exhibition/interior-travertine-hall.jpg, prophet-mosque-architecture-exhibition/laser-cut-islamic-facade.jpg, prophet-mosque/expansion-exhibition.jpg, from-work/prophet-mosque-frame-assembly.jpg |
| معرض كنوز الصين | from-graphite/china-dynasty-costumes.jpg |
| معـــرض التاريخ والثقافة الكورية | from-work/korea-exhibition-vitrine-fabrication.jpg |
| معرض الوحي | revelation-exhibit.jpg, from-website/revelation-cave-cover.jpg, from-website/story-of-revelation-immersive-cover.jpg |
| معرض تأسيس الدولة السعودية | from-graphite/companions-arched-corridor.jpg |
| معرض جماليات الخط العربي | arabic-calligraphy.jpg, from-website/calligraphy-manuscripts-cover.jpg, from-graphite/calligraphy-vitrines-row.jpg, from-work/calligraphy-cnc-panel-finishing.jpg, from-graphite/king-salman-book-presentation.jpg |
| مركز حكايا علم م- الغذاء والدواء | hakaia-elm/world-map-curved-wall.jpg |
| مراكز الزوار - شركة علم | from-graphite/heritage-visitor-centers-map.jpg, from-graphite/visitor-center-aseer-corridor.jpg, from-graphite/visitor-center-jazan-history.jpg, from-graphite/visitor-center-qassim-blue.jpg, from-work/visitor-center-vitrine-installation.jpg |
| ملتقى المدينة المنورة للخط العربي | from-graphite/calligraphy-vitrines-row.jpg |
| واحة الملك سلمان | from-website/king-salman-oases-cover.jpg |
| مبادرة التاريخ الإسلامي | from-graphite/heritage-visitor-centers-map.jpg |
| فعالية درب مكة | from-graphite/road-to-makkah-corridor.jpg |
| مهرجان المللك عبدالعزيز للإبل | from-graphite/camel-festival-stage.jpg |
| احتفالات عيد الفطر المبارك | makkah-eid-events.jpg |

## Replacement rules
1. Pick the **largest/best photo** from each Arabic folder (sort by file size descending)
2. **Each site image gets a unique photo** — never copy the same photo to multiple paths
3. Always run `sips` optimization after replacement
4. Skip folders with no matching site images (e.g. معرض الأميرة حصة)
