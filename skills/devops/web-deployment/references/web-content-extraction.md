# Web Content Extraction for Blocked Pages

When sites require JavaScript (Medium, Cloudflare-protected pages, SPA-rendered content), standard `curl` returns "Just a moment..." or blank content.

## Jina AI Reader (r.jina.ai)

**Best option for Medium/Cloudflare pages.** No API key required for basic use.

```bash
curl -sL "https://r.jina.ai/https://medium.com/@user/article-slug-123abc"
```

Returns clean markdown with:
- Title, URL Source, Published Time headers
- Full body as markdown (images as markdown `![Image N](url)`)
- All links preserved

**Limits:** ~2-5MB response cap. For very long articles, pipe through `head -200`.

## When curl Strikes Out

| Symptom | Likely Cause | Try |
|---------|-------------|-----|
| "Just a moment..." | Cloudflare/WAF | `r.jina.ai` endpoint |
| Blank page | JS-rendered SPA | `r.jina.ai` or browser tools |
| "Enable JavaScript" | Bot detection | `r.jina.ai` |
| 403 Forbidden | IP blocked | Try browser_navigate instead |
