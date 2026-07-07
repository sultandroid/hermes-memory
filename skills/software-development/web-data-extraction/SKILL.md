---
name: web-data-extraction
description: "Extract structured data from websites using terminal tools (curl, regex, jq, Python). Covers WordPress sitemap discovery, OG meta extraction for JS-rendered content, bilingual content via hreflang, and fallback when sandboxed agents can't reach external DNS."
version: 1.0.0
author: Hermes Agent
platforms: [macos, linux]
metadata:
  hermes:
    tags: [scraping, data-extraction, curl, wordpress, website, terminal]
    related_skills: [document-analysis, labor-clis]
---

# Web Data Extraction

Extract structured records from websites using terminal tools. Works when the site is JS-rendered (Visual Composer, page builders, React) or static HTML.

## When to Use

- User says "scrape/get all data from example.com"
- Need structured project/portfolio/article listings from a website
- Site uses Visual Composer, WPBakery, or similar JS-heavy page builders (content not in raw HTML body)
- Need bilingual content (AR/EN) and the site uses hreflang
- Codex/Fugu sandbox cannot resolve the target domain's DNS — do the work directly instead

## Workflow

### 1. Discovery — find all URLs

Start with the sitemap. WordPress sites expose:

```
/sitemap.xml  →  /wp-sitemap-posts-portfolio-1.xml
                  /wp-sitemap-posts-page-1.xml
                  /wp-sitemap-posts-post-1.xml
```

Extract URLs:

```bash
curl -sL 'https://example.com/wp-sitemap-posts-portfolio-1.xml' | grep -oP '<loc>\K[^<]+'
```

Or with Python:

```python
import re
r = terminal("curl -sL 'https://example.com/wp-sitemap-posts-portfolio-1.xml'")
urls = re.findall(r'<loc>(https://[^<]+)</loc>', r["output"])
```

**Pitfall:** The codex-fugu sandbox (Sakana provider sandbox) often cannot resolve external DNS (`curl: (6) Could not resolve host`). Do NOT rely on it for direct web scraping — do the work from Hermes's own terminal instead.

### 2. Extract Metadata — use OG tags, not HTML body

JS-rendered pages (Visual Composer, etc.) have empty `<body>` content in raw HTML. The actual data lives in `<meta property="og:*">` tags:

```python
def extract_meta(body):
    og_title = re.search(r'<meta[^>]*property="og:title"[^>]*content="([^"]+)"', body)
    og_desc  = re.search(r'<meta[^>]*property="og:description"[^>]*content="([^"]+)"', body)
    og_image = re.search(r'<meta[^>]*property="og:image"[^>]*content="([^"]+)"', body)
    return {
        "title": html.unescape(og_title.group(1)).strip() if og_title else "",
        "description": html.unescape(og_desc.group(1)).strip() if og_desc else "",
        "image": og_image.group(1) if og_image else "",
    }
```

Also extract all image URLs from the page:

```python
images = re.findall(r'(https://example\.com/wp-content/uploads/[^"\'\\\s?]+\.(?:jpg|jpeg|png|gif|webp))', body)
images = list(dict.fromkeys(images))  # dedupe, preserve order
# Filter out favicons/touch icons
images = [img for img in images if 'favicon' not in img and 'touch-icon' not in img]
```

### 3. Bilingual content via hreflang

Extract the English equivalent URL:

```python
hreflang_en = re.search(r'<link[^>]*hreflang="en"[^>]*href="([^"]+)"', body)
en_url = hreflang_en.group(1) if hreflang_en else ""
```

Then scrape the English URL with the same `extract_meta()` function.

**Pitfall:** Some projects may not have a real English translation — the English page may exist at an `/en/w/` URL but still show Arabic titles. Always check `og:title` to confirm.

### 4. Build structured output

Save as structured JSON and a readable Markdown report:

```python
output = {"projects": results, "total": len(results)}
with open("/path/to/output.json", "w", encoding="utf-8") as f:
    json.dump(output, f, ensure_ascii=False, indent=2)
```

For Markdown, generate a project table with: #, Arabic title, English title, Description, Image URL, AR URL, EN URL.

### 5. Validate

- All URLs start with the expected domain
- All records have at least an Arabic title and URL
- JSON parses clean with `json.load`
- Images are real content images (not favicons/touch icons)

## Pitfalls

- **Sandbox DNS isolation:** Codex CLI / Fugu sandboxes block outbound DNS. Use Hermes's own `terminal()` for curl calls, not delegated sandbox agents.
- **JS-rendered content:** Don't grep for `<div class="section-title">` — the page builder injects content via JS. OG meta tags are the reliable source.
- **Rate limiting:** 16 pages × 2 curls (AR+EN) = ~30 requests. Space them with `--max-time 30` per request.
- **URL encoding:** Arabic/hyphenated slugs in sitemap XML are URL-encoded (`%d9%85%d8%b9%d8%b1%d8%b6`). Feed them as-is to curl — the server decodes them. Use `urllib.parse.unquote()` for display.
- **Categories:** On JS-rendered portfolio pages, categories may not be extractable from HTML. The `/our-work/` listing page likely loads via AJAX. Skip if not available rather than fabricating.
- **Alibaba / aggressive captcha sites:** Sites with Alibaba-style `punish-component` captcha block all tools (browser, curl, proxies). No URL-level bypass works — the captcha is IP-based and session-based. Known dead ends: Wayback Machine has no archive, Google Cache returns 404, Bing Cache has no entry, CORS proxies get blocked, Jina.ai returns 403. The only viable alternative is a **different URL path** (e.g., the Alibaba PLA ad URL which uses a different server-side rendering path). See `product-research` skill Phase 2B for the PLA URL construction technique.

## References

- `references/print-doc-page-extraction.md` — extracting specific pages from assembled print-HTML documents where page numbers are JS-generated (`data-page-current`). Use when the target is one assembled HTML with `<section class="page">` per page and no static page numbers.

OG meta tags are the most reliable content source on WordPress sites using Betheme/Avada/Visual Composer themes. The meta tags are server-rendered while the body content is injected client-side.
