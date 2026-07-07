---
name: product-research
description: Use when sourcing specialized industrial/scientific/museum-grade products — find exact model numbers, extract specs, estimate USD + local prices, identify regional (ME) suppliers, and compile comparison reports.
tags:
  - research
  - sourcing
  - equipment
  - specifications
  - procurement
  - suppliers
  - middle-east
---

# Product Research & Equipment Sourcing

Class-level skill for researching specialized technical products with exact model numbers, specifications, pricing, and regional supplier identification.

## Trigger Conditions

Load this skill when the user asks you to:
- "Find the exact model number for [product type] used in [industry/application]"
- "Research [device/instrument/model] specs and pricing"
- "Find suppliers in [region/country] for [product]"
- "What's the standard [tool/instrument] for [use case]?"
- "Compare models of [product category] for [specific application]"
- Any request involving equipment research, supplier identification, or technical product comparison

## Workflow

### Phase 1: Identify the Exact Model

1. **Start with the use case, not the product name.** User may know the category (e.g., "spectrophotometer for museum color matching") but not the exact model. Search by application domain first.
   - "What model do conservation labs use for X?"
   - "Industry standard for measuring Y in Z industry"

2. **Go direct to manufacturer sites** — avoid search engines (captcha-prone, slow, imprecise for technical queries):
   - Manufacturer product category pages (e.g., `xrite.com/categories/portable-spectrophotometers`)
   - Top products / best-sellers lists on manufacturer sites
   - "Industries" or "Applications" sections that map products to use cases

### Phase 2: Extract Specifications

#### 2A. Standard Manufacturer / Distributor Pages

For JS-heavy manufacturer pages:

1. **Use `browser_console`** to extract product details:
   - `document.title` — confirms you're on the right page
   - `document.body.innerText.substring(start, end)` — full page text without JS rendering noise
   - `document.querySelector('h1')?.innerText` — product name
   - `document.querySelector('[class*="spec"]')?.innerText` — specs table

2. **Extract JSON-LD structured data** via terminal:
   ```bash
   curl -sL -H "User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36" URL | python3 -c "
   import sys, re, json
   content = sys.stdin.read()
   scripts = re.findall(r'<script type=\"application/ld\\\\+json\">(.*?)</script>', content, re.DOTALL)
   for s in scripts:
       try:
           data = json.loads(s)
           print(json.dumps(data, indent=2))
       except:
           pass
   "
   ```
   JSON-LD often contains SKU, brand, description, and dimensions.

3. **Extract spec tables** from HTML:
   ```bash
   curl -sL URL | python3 -c "
   import sys, re, html
   content = sys.stdin.read()
   content = re.sub(r'<script[^>]*>.*?</script>', '', content, flags=re.DOTALL)
   content = re.sub(r'<style[^>]*>.*?</style>', '', content, flags=re.DOTALL)
   text = re.sub(r'<[^>]+>', '\n', content)
   text = html.unescape(text)
   lines = [l.strip() for l in text.split('\n') if l.strip() and len(l.strip()) > 5]
   for l in lines:
       if any(k in l.lower() for k in ['aperture', 'spectral', 'wavelength', 'resolution', 'repeatability', 'measurement ', 'battery', 'interface', 'weight', 'dimension', 'model #']):
           print(l)
   "```

#### 2B. Alibaba / Chinese B2B Platforms (captcha-blocked)

Alibaba product pages (`/product-detail/<slug>_<id>.html`) serve a captcha on direct access. Use this fallback chain:

**Step 1 — Try the PLA (Product Listing Ad) URL.** This lighter page often bypasses captcha and reveals product name, price, MOQ, supplier name, and JSON-LD structured data — but NOT detailed spec tables.

Construct the PLA URL: `https://www.alibaba.com/pla/<slug>_<id>.html?biz=pla&product_id=<id>&pcy=<COUNTRY>&material=<IMAGE_FILE>`

- Find the `slug` and `material` values by searching DuckDuckGo `html.duckduckgo.com/lite/?q=...` for the product — results contain PLA URLs in redirect links
- `material` is a product image filename from alicdn.com

**Step 2 — Visit the supplier's own website.** Extract the supplier name from the PLA page, then visit their independent company website. Many Chinese suppliers have WordPress-like sites with no bot detection. Check their product category pages.

**Step 3 — Third-party listings:** Made-in-China.com, TradeIndia, GlobalSources may carry the same products with weaker bot detection.

**Step 4 — Direct inquiry.** Contact via the Alibaba chat button, or use email/WhatsApp from the supplier's company website.

See [`references/alibaba-product-extraction.md`](references/alibaba-product-extraction.md) for curl examples, PLA URL construction, and known pitfalls.

### Phase 3: Research Pricing

Pricing is rarely listed on manufacturer sites. Sources, best first:

| Source | Notes |
|--------|-------|
| Third-party lab distributors | Fisher Scientific, Cole-Parmer — often list street price |
| Regional distributor sites | Check UAE/KSA-specific stockists |
| Industry forums | Useful for ballpark ranges and street vs. list |
| Manufacturer "Request Quote" | Slowest, but gives an authoritative ballpark |

**Always provide both USD and local currency** (e.g., SAR for KSA) and flag estimates as estimates.

### Phase 4: Find Regional Suppliers (Middle East Focus)

For KSA/UAE suppliers, check these channels:
- **ESTS (UAE)** — wide scientific instrument distribution, authorized for X-Rite
- **Tajco Scientific** — Dubai/Riyadh, stocks BYK, Elcometer, and general lab instruments
- **Al Sweilem Scientific Bureau (Riyadh)** — established KSA supplier
- **Al Rashedi & Al Omran (Dammam/Riyadh)** — industrial testing equipment
- **SMEH (Riyadh/Jeddah)** — major Saudi scientific/medical supplier
- Manufacturer "Partner Locator" or "Find a Distributor" pages (may 404 — fall back to contacting manufacturer ME sales directly)
- Amazon.sa / Amazon.ae for in-stock items from 3rd-party sellers

### Phase 5: Compile Structured Report

Save a comprehensive markdown report with:

```markdown
# Equipment Research: [Project Name]
## [Product Type] Sourcing for [Region]

## 1. [Product Name]

### Recommended Model: [Exact Model # / SKU]

| Spec | Value |
|------|-------|
| Exact Model | ... |
| Key Spec 1 | ... |
| Key Spec 2 | ... |
| Standards | ... |

**Why this model for [use case]:** ...

### Pricing

| Region | USD | Local |
|--------|-----|-------|
| Standard | $X – $Y | Z – W SAR |

### KSA/UAE Suppliers

1. **Supplier Name** — Location, contact, notes

### Combined Budget / Procurement Strategy
- Total estimate
- Ordering priority
- Calibration/service notes
- Delivery timelines
```

## Pitfalls

- **Search engine captchas** — Google, Bing, and DuckDuckGo all block automated browser traffic. Go direct to manufacturer sites instead of searching.
- **Alibaba captcha** — The `punish-component` captcha is served on every direct access (browser or curl) to Alibaba product detail pages. The PLA (Product Listing Ad) URL is the only known bypass, and it only yields metadata (name, price, supplier) — not spec tables. Google Cache, Wayback Machine, and Bing Cache rarely have Alibaba product pages saved.
- **Broken manufacturer sites** — BYK Instruments and Elcometer sites currently (2026) have Salesforce Commerce Cloud deployment issues returning 404 for product pages. Fall back to third-party distributor pages or cached descriptions.
- **No public pricing** — X-Rite, BYK, and most industrial equipment makers hide prices behind "Request Quote." Provide market estimates based on distributor knowledge and flag as estimates.
- **Specs behind JS rendering** — Spec tables are often loaded dynamically via JavaScript. Use `browser_console` with `document.body.innerText` or JSON-LD extraction rather than raw HTML.
- **"X" in product names causes search confusion** — Searching "X-Rite" on some engines can trigger Twitter/X results. Use quotes or hyphenated terms. Bing is particularly bad for this.
- **Regional supplier info may be outdated** — Contact details change frequently. Always give multiple supplier options and note which is the authorized distributor.

## Worked Example

See [`references/aseer-museum-equipment.md`](references/aseer-museum-equipment.md) for a complete worked session — X-Rite Ci64UV spectrophotometer and BYK micro-TRI-gloss meter researched for a KSA museum replica project, including verified specs, price ranges (USD + SAR), and ME suppliers.

## Verification

Before delivering, confirm:
- [ ] Exact model number/SKU verified from manufacturer page or JSON-LD
- [ ] Key specs extracted (not just marketing copy)
- [ ] Pricing in both USD and local currency
- [ ] At least 2–3 supplier options per region
- [ ] Report saved as a `.md` file locally
- [ ] Standards compliance noted (ISO/ASTM/etc.)
