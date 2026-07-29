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

## 5. Password-Protected SPAs (React/Vue/Angular)

When the target is a **logged-in SPA** (single-page app) where all content is behind authentication and rendered client-side:

### 5.1 Login

Use `browser_navigate` + `browser_type` + `browser_click` to log in. The accessibility tree snapshot shows form fields after navigation.

### 5.2 Navigate Sections

SPA routing (React Router, Vue Router) may not update the accessibility tree snapshot after `browser_click`. **Workaround:** use `browser_console` with JS to click buttons programmatically:

```javascript
// Click nav button by text content
document.querySelectorAll('button').forEach(b => {
  if (b.textContent.trim() === 'اسم القسم') b.click();
});
```

Then extract all visible text via:

```javascript
document.body.innerText
```

### 5.3 Extract All Sections

Pattern for a multi-section SPA:

1. Log in via browser tool (type credentials, click login)
2. Get snapshot to confirm login success
3. For each navigation section, programmatically click via `browser_console` expression
4. Extract `document.body.innerText` (captures all rendered text including tables, nested components)
5. Save raw text files to disk
6. If data is large, use `browser_console` with `document.body.innerText.substring(0, 15000)` in chunks
7. Delegate analysis/MD creation to a sub-agent (avoids flooding context with raw data)

### 5.4 When browser_snapshot is stale

The accessibility tree snapshot may show the same content after navigation because SPAs reuse the same DOM shell. **Trust `document.body.innerText` via console** — it captures what's actually rendered, even when the snapshot doesn't reflect the route change.

### 5.5 Form Filling with JS Fallback

When a form has custom combobox/select elements, radio buttons, or other complex UI components that `browser_type` and `browser_click` cannot handle reliably:

**Step 1 — Identify the DOM structure** via `browser_console`:

```javascript
// Check if it's a real <select> or a custom ARIA widget
document.querySelector('select[name="GovernorateID"]') // real select
document.querySelector('[role="combobox"]') // custom ARIA combobox
```

**Step 2a — For real `<select>` elements**, use `browser_console` to set the value:

```javascript
(function() {
  const sel = document.getElementById('governorate');
  sel.selectedIndex = 8; // or sel.value = '2';
  sel.dispatchEvent(new Event('change', {bubbles: true}));
  return sel.options[sel.selectedIndex].text;
})()
```

**Step 2b — For radio buttons**, enumerate them and set by index:

```javascript
(function() {
  const radios = document.querySelectorAll('input[type="radio"]');
  // Log them first to find the right index
  let r = '';
  radios.forEach((rb, i) => r += i + ': name=' + rb.name + ' value=' + rb.value + ' checked=' + rb.checked + '\\n');
  return r;
})()
```

Then check the desired radio:

```javascript
(function() {
  const radios = document.querySelectorAll('input[type="radio"]');
  radios[1].checked = true; // set علمى رياضة
  radios[1].dispatchEvent(new Event('change', {bubbles: true}));
})()
```

**Step 2c — Verify all form values before submit:**

```javascript
(function() {
  const g = document.getElementById('governorate');
  const radios = document.querySelectorAll('input[type="radio"]');
  return 'Gov: ' + g.options[g.selectedIndex].text + ' | Dept: ' + radios[0].checked + ',' + radios[1].checked + ',' + radios[2].checked;
})()
```

**Pitfalls:**
- Typing into a combobox may contaminate the NEXT text field on the page (keyboard events leak). Use JS to set values instead.
- `browser_click` on a `<select>` option may fail with `CDP error (DOM.getBoxModel): Could not compute box model` — use JS `selectedIndex` instead.
- The accessibility tree snapshot may not reflect JS-set values until the page is re-navigated. Verify with `browser_console` expressions instead.
- Some form validation is client-side. After setting values via JS, also dispatch `change` events so the framework (Angular/React/Vue) picks up the changes.
- **Click the submit button, don't call `form.submit()` from console.** The button triggers the JS validation/submission handler registered via `addEventListener('submit', ...)`. Calling `form.submit()` bypasses the handler and does a raw HTTP POST that the server may reject (HTTP 405). Always use `browser_click` on the submit button ref.
- **No visible feedback after submission.** Some forms show a hidden success popup rather than navigating away. Check via `browser_console` for `data-show-success="true"` on the form element, or if a hidden popup gained the `is-open` class. The `browser_snapshot` may miss hidden elements.

### 5.6 Extract → Save → Delegate Pattern

Do NOT hold all extracted data in your context. Instead:

1. Extract each section's data via `browser_console`
2. Write raw `.txt` files to disk with `write_file`
3. Delegate analysis and MD file creation to a sub-agent via `delegate_task` — pass file paths and analysis goals
4. The sub-agent reads the files, analyzes, and produces structured output

This avoids context overflow and keeps the session responsive.

See `references/spa-session-extraction.md` for a complete worked example.

### 5.6 Download Attached Files from Cloud Storage

Many SPAs store uploaded documents (contracts, receipts, reports) in cloud storage like **Supabase Storage**, AWS S3, or Cloudinary. The download/view URLs are embedded in the DOM as `<a href="...">` or `<button onclick="...">` elements.

**Pattern:**

1. After navigating to the documents/files section, extract all download URLs from the DOM:

```javascript
// Find all download/view links
const links = document.querySelectorAll('a[href*="supabase.co"], a[href*="s3.amazonaws.com"], a[href*="cloudinary.com"]');
const urls = Array.from(links).map(a => ({ text: a.textContent.trim(), href: a.href }));
```

Or filter by text content:

```javascript
document.querySelectorAll('a, button').forEach(el => {
  if (el.textContent.includes('تحميل') || el.textContent.includes('Download')) {
    console.log(el.href || el.getAttribute('onclick'));
  }
});
```

2. Download files to local disk via `terminal()` with `curl`:

```python
from hermes_tools import terminal

url = "https://supabase.co/storage/v1/object/public/..."
name = "contract.pdf"
r = terminal(f'curl -sL -o "{target_dir}/{name}" "{url}" -w "%{{http_code}}"')
```

3. **If files are scanned images/PDFs** (no extractable text), use `vision_analyze` on each file, or delegate to a sub-agent that can:
   - Convert PDF pages to images (`pdftoppm` or `sips` on macOS)
   - Use `vision_analyze` to read the content
   - Produce structured summaries as MD files

4. **Bond type codes** commonly found in construction tracking apps:
   - `MST` = مستخلص (progress payment certificate)
   - `TWD` = توريد (material supply)
   - `SRF` = صرفية (cash disbursement)

### 5.7 Post-Extraction: Delegate Document Analysis

After downloading files, do NOT try to read and summarize everything in your own context. Instead:

1. Save raw text data and downloaded files to a directory
2. Delegate a sub-agent with `delegate_task`:
   - Provide the directory path, file names, and context about the project
   - Ask it to use terminal + vision tools to read each document
   - Have it produce structured MD files

This keeps the main session responsive while the heavy processing happens in the background.

## Project Type Detection

When given a URL, determine if the target is:

| Type | Characteristics | Tool |
|------|----------------|------|
| Static site | HTML rendered server-side, visible in page source | `curl` + `web_extract` |
| WordPress | `/wp-content/`, `/wp-json/`, sitemap patterns | `curl` + OG meta extraction |
| SPA (React/Vue/Angular) | Login page, empty `<body>`, hash routing, Vercel/Netlify deploy | Browser tools + console |
| File storage backend | Supabase, S3, Cloudinary URLs in DOM | `curl` download + vision analysis |

## Pitfalls

- **Sandbox DNS isolation:** Codex CLI / Fugu sandboxes block outbound DNS. Use Hermes's own `terminal()` for curl calls, not delegated sandbox agents.
- **JS-rendered content:** Don't grep for `<div class="section-title">` — the page builder injects content via JS. OG meta tags are the reliable source.
- **SPA routing not reflected in snapshot:** The accessibility tree may not update after SPA navigation. Always verify via `browser_console` + `document.body.innerText` rather than relying on `browser_snapshot`.
- **Rate limiting:** 16 pages × 2 curls (AR+EN) = ~30 requests. Space them with `--max-time 30` per request.
- **URL encoding:** Arabic/hyphenated slugs in sitemap XML are URL-encoded (`%d9%85%d8%b9%d8%b1%d8%b6`). Feed them as-is to curl — the server decodes them. Use `urllib.parse.unquote()` for display.
- **Categories:** On JS-rendered portfolio pages, categories may not be extractable from HTML. The `/our-work/` listing page likely loads via AJAX. Skip if not available rather than fabricating.
- **Session loss on re-navigate:** Navigating away from a logged-in SPA and back (`browser_navigate` to same URL) may reset the session. Stay on the page and use programmatic navigation via console instead.
- **Alibaba / aggressive captcha sites:** Sites with Alibaba-style `punish-component` captcha block all tools (browser, curl, proxies). No URL-level bypass works — the captcha is IP-based and session-based. Known dead ends: Wayback Machine has no archive, Google Cache returns 404, Bing Cache has no entry, CORS proxies get blocked, Jina.ai returns 403. The only viable alternative is a **different URL path** (e.g., the Alibaba PLA ad URL which uses a different server-side rendering path). See `product-research` skill Phase 2B for the PLA URL construction technique.
- **DNS not resolving — Azure Application Gateway:** Some hostnames have no public DNS record but ARE configured in the Azure Application Gateway, which accepts forced-resolution connections. Use `curl --resolve <host>:<port>:<ip>` to test. Try **both HTTP and HTTPS** — the wildcard TLS cert may cover the subdomain even when HTTP fails. If the gateway returns **404 on all paths**, the hostname is configured but no backend service is deployed. This is common for inactive/off-season portals (e.g., exam result portals). Diagnose in steps: (1) `nslookup <host>` for baseline, (2) `curl --resolve` to the gateway IP (both ports 80 and 443), (3) delegate to sub-agent for alternative network path if both fail. When a user provides a URL that doesn't resolve, **try harder before giving up** — user-provided URLs are authoritative and worth the extra diagnostic steps.
- **User-provided URLs are authoritative:** When a user insists on a specific URL and keeps asking you to try it, trust their input. They likely know the correct URL from an external source (Ministry announcement, news article, SMS, etc.). Do not dismiss it after a few failed attempts — the URL may be correct but the service may not be deployed yet. Set up a recurring cron job to monitor the URL rather than concluding it's dead. The user's persistence is a signal that the URL is authoritative.

## References

- `references/print-doc-page-extraction.md` — extracting specific pages from assembled print-HTML documents where page numbers are JS-generated (`data-page-current`). Use when the target is one assembled HTML with `<section class="page">` per page and no static page numbers.
- `references/spa-session-extraction.md` — worked example: extracting all data from a password-protected React SPA (project management dashboard) by logging in, navigating sections via console JS clicks, extracting text, and delegating analysis to a sub-agent.
- `references/egyptian-gov-portal-patterns.md` — accessing Egyptian Ministry of Education (EMIS) portals for Thanaweya Amma result checking. Covers DNS resolution, transliterated Arabic service names ("sanwaya amaa" = ثانوية عامة), form field patterns (seat number + national ID), and common pitfalls with Next.js subdomain routing.

OG meta tags are the most reliable content source on WordPress sites using Betheme/Avada/Visual Composer themes. The meta tags are server-rendered while the body content is injected client-side.
