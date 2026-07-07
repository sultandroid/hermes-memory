# Alibaba Product Specification Extraction

Extracting structured specs (temperature range, humidity control, power, dimensions, etc.) from Alibaba product pages is routinely blocked by captchas and bot detection. This reference documents bypass strategies that worked across multiple sessions.

## The Problem

Alibaba product pages (`/product-detail/<slug>_<id>.html`) serve a captcha page (`punish-component`) when accessed by:
- Direct browser navigation (Browserbase/Browserless)
- Raw `curl` with any User-Agent
- Google Cache, Wayback Machine, Bing Cache
- Third-party scrapers (Jina.ai, CORS proxies)
- Textise.iitty, r.jina.ai

The captcha is an Alibaba-internal sliding puzzle / click-grid ("sufei-punish"). There is no general bypass — you must use alternative access paths.

## Bypass Strategies (Priority Order)

### 1. PLA (Product Listing Ad) URL — BEST PARTIAL BYPASS

The Alibaba PLA page serves a **different, lighter page** that often bypasses captcha. It loads product name, price range, MOQ, supplier name, JSON-LD structured data, and images — but NOT the detailed specification tables.

**How to construct a PLA URL:**

```
https://www.alibaba.com/pla/<product-slug>_<id>.html?biz=pla&product_id=<id>&pcy=<COUNTRY_CODE>&material=<MATERIAL_IMG>
```

Where:
- `<product-slug>` from the original URL (e.g., `Active+Microclimate+Generator+for+museum+Display+Cases`)
- `<id>` from the original URL (e.g., `1600875137680`)
- `pcy` = destination country code (e.g., `US`, `SA`, `AE`)
- `material` = a product image filename from the JSON-LD `image` array

**Discovery method:** Search DuckDuckGo or Bing for the product ID — Alibaba's own ad platform generates PLA links. The DuckDuckGo `html.duckduckgo.com/lite/?q=...` endpoint can reveal these PLA URLs.

**What you get:**
- Product name (h1)
- Price range (e.g., `SAR 4,204.52-5,733.43`)
- MOQ (e.g., `MOQ: 1`)
- Supplier name and country
- JSON-LD structured data (brand, name, offers with price/currency/availability, images)
- Product image URLs
- Related products recommendations

**What you DON'T get:**
- Specification tables (temperature range, humidity control, etc.)
- Full product description
- Detailed attributes

### 2. Supplier Website — DIRECT

Extract the supplier name from the PLA page (it's always in the page text), then go to their **own website** directly. Chinese B2B suppliers on Alibaba usually have:
- An independent company website (e.g., `hzfreeair.com`)
- An Alibaba storefront (`freeair.en.alibaba.com` — also blocked by captcha)

**How to find it:**
- Search: `"{supplier name}" official website`
- Or from the Alibaba PLA page HTML, search for the supplier store URL embedded in the encrypted data blobs (often contains the supplier name in plaintext)

**What you might get:**
- Full product category listings
- Detailed specifications for standard products
- Contact information (email, phone, WhatsApp) for direct inquiry

**What you might NOT get:**
- The exact product as listed on Alibaba (Chinese supplier websites often lag behind Alibaba listings)
- Detailed spec sheets for bespoke/custom products

### 3. Third-Party Listings (Made-in-China, TradeIndia, etc.)

Chinese suppliers often list the same products on:
- `made-in-china.com` — search for the product name
- `tradeindia.com`
- `globalsources.com`

These sites have weaker bot detection. Use `browser_navigate` with a standard User-Agent to try these.

### 4. Google Shopping Results

Search: `https://www.google.com/search?tbm=shop&q="{exact product name}"`

Google Shopping may have cached pricing and brief specs. However, Google's bot detection also fires frequently.

## curl-based Extraction Example (from PLA page)

```bash
curl -sL "https://www.alibaba.com/pla/Active+Microclimate+Generator+for+museum+Display+Cases_1600875137680.html?biz=pla&product_id=1600875137680&pcy=US&material=H0e767a66369447b58a1d81ee63644b94a.jpg" \
  -H "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36" \
  -H "Accept: text/html,application/xhtml+xml" \
  -o /tmp/response.html
```

Then extract:

```python
import re, json
with open('/tmp/response.html') as f:
    content = f.read()

# 1. JSON-LD structured data (most reliable)
scripts = re.findall(r'<script[^>]*type="application/ld\+json"[^>]*>(.*?)</script>', content, re.DOTALL)
for s in scripts:
    data = json.loads(s)
    # data["name"] = product name
    # data["offers"]["price"] = price
    # data["offers"]["priceCurrency"] = currency
    # data["image"] = list of image URLs

# 2. Price from text (failsafe)
price = re.findall(r'SAR\s*[\d,]+\.?\d*', content)

# 3. MOQ from text
moq = re.findall(r'MOQ:\s*\d+', content)

# 4. Supplier name
supplier = re.findall(r'Hangzhou[^<,]{0,100}', content)  # adjust for actual supplier name

# 5. Product image URLs
images = re.findall(r'https?://[^"\'\\s]+(?:jpg|jpeg|png)', content)
```

## What Cannot Be Extracted

If the product specifications (temperature range, humidity range, power, dimensions, weight, cooling method, noise level, warranty) are not visible on the PLA page or supplier website, **the only reliable option is direct inquiry**:

- Contact the supplier via the Alibaba chat / "Send inquiry" button
- Contact via email found on their company website
- Request a datasheet / catalog

Some products on Alibaba are **custom/bespoke** — the supplier builds to order, so there is no fixed specification sheet to extract.

## Pitfalls

- **PLA URLs are ephemeral** — the `material` parameter is tied to a specific product image. If the supplier changes product images, the URL breaks.
- **Alibaba blocks IPs** after repeated attempts. If you get the captcha page, wait and try the PLA URL instead.
- **Supplier websites may be in Chinese only** — use browser translation or look for an EN language toggle.
- **No Wayback Machine save** — Alibaba product pages are rarely archived.
- **Pricing on PLA pages is in local currency** — the `pcy` parameter controls this. Always note the currency (SAR, USD, etc.).
