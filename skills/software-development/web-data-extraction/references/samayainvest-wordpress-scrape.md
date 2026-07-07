# Samaya Invest WordPress Scrape — Working Recipe

## Site
`samayainvest.com` — Betheme/WordPress with Visual Composer. Arabic primary, English under `/en/`.

## Discovery
Sitemap: `https://samayainvest.com/wp-sitemap-posts-portfolio-1.xml`
→ 16 portfolio entries (URLs in `/w/`)

## Extraction Pattern
- Page body is JS-rendered (Visual Composer) → body is empty in raw HTML
- Rely on `<meta property="og:*">` tags:
  - `og:title` → clean Arabic title
  - `og:description` → actual project description
  - `og:image` → featured image URL

## Image Extraction
All content images under `wp-content/uploads/`. Regex:
```
https://samayainvest\.com/wp-content/uploads/[^"'\\\s?]+\.(?:jpg|jpeg|png|gif|webp)
```
Filter out `favicon` and `touch-icon`.

## Bilingual
Each Arabic page has `<link hreflang="en" href="https://samayainvest.com/en/w/...">`
- 15/16 projects have English pages
- Al-Safiyyah Museum (متحف وبستان الصافية) has no English hreflang — no English page

## Known English URL Patterns
| Arabic Slug | English URL |
|---|---|
| معرض-الوحي | /en/w/revelation-exhibition/ |
| فعاليات-مكة-تعايدنا | /en/w/makkah-greets-us/ |
| حفل-افتتاح-مستشفى-الملك-فيصل-التخصصي | /en/w/%d8%ad%d9%81%d9%84-... (same Arabic slug) |
| لبيك | /en/w/labbayk/ |
| متحف-الجوف | /en/w/al-jouf-museum/ |
| معرض-أصحابي | /en/w/%d9%85%d8%b9%d8%b1%d8%b6-%d8%a3%d8%b5%d8%ad%d8%a7%d8%a8%d9%8a/ |
| معرض-الخلق-العظيم | /en/w/the-superior-moral-character-of-prophet-muhammad/ |
| معرض-جماليات-الخط-العربي | /en/w/the-exquisite-art-of-arabic-calligraphy-exhibition/ |
| معرض-شلايل | /en/w/shalayil-exhibition/ |
| ساحة-اللغة-والثقافة | /en/w/language-and-culture-arena/ |
| معرض-عمارة-المسجد-النبوي | /en/w/prophets-mosque-expansion-exhibition/ |
| معرض-أسماء-الله-الحسنى | /en/w/the-beautiful-names-of-allah-exhibition/ |
| واحات-الملك-سلمان-للعلوم-بالأحياء | /en/w/king-salman-science-oasis/ |
| معرض-متحف-تبوك | /en/w/tabouk-museum/ |
| quran-museum | /en/w/quran-museum/ |
| متحف-وبستان-الصافية | (no English page) |
