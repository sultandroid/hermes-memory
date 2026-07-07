# Logo Embedding in HTML Proposals

Sourced from RCRC Exhibition proposal work (June 2026).

## Overview

Embedding three-party logos (Client · Designer · Contractor) into a Samaya-branded HTML proposal cover page. Logos must render crisply at small sizes (header: ~32px, party icons: ~14px) and work on dark backgrounds (navy `#0F172A`).

## Logo Sources

| Party | Where to find | Format |
|-------|--------------|--------|
| **Client** | Client's official website, `/wp-content/uploads/YYYY/` or inspect their press kit | SVG preferred (vectors scale cleanly) |
| **Designer / Consultant** | Their official website (`borismicka.com/images/logo-white.svg` for BMA) | SVG |
| **Samaya** | `Docs/Branding/Samaya-Logo.png` in project folder | PNG (convert to base64) |

## Workflow

### Step 1: Find logo URL
Search the party's official website. Common paths:
- `https://<domain>/images/logo-<color>.svg`
- `https://<domain>/wp-content/themes/.../logo.svg`
- Check page source for `<img>` tags with logo class names
- Browser tools: curl + grep for `.svg`, `.png`, `logo` in URL

### Step 2: Download
```bash
curl -sL "<url>" -o /tmp/<party>_logo.svg
```

### Step 3: Embed in HTML

**Client logo (cover top-left):**
```html
<svg width="..." viewBox="0 0 ..." fill="none" xmlns="..." style="filter:brightness(0) invert(1);width:auto;height:40px">
  <!-- paste SVG path data -->
</svg>
```

**Samaya logo (cover top-right):**
Convert PNG to base64 data URI:
```python
import base64
with open('Samaya-Logo.png', 'rb') as f:
    b64 = base64.b64encode(f.read()).decode()
print(f'data:image/png;base64,{b64}')
```
Embed:
```html
<img src="data:image/png;base64,<data>" alt="Samaya Investment Company" style="height:32px;width:auto;display:inline-block">
```

**Designer logo (cover parties row):**
Use SVG directly, sized as inline-block in the `.cover-party-icon` div:
```html
<div class="cover-party-icon">
  <svg width="120" height="14" viewBox="0 0 375 30" style="width:auto;height:14px">
    <!-- paste SVG path data -->
  </svg>
</div>
```

### Step 4: Cover parties layout

```html
<div class="cover-bottom">
  <div class="cover-parties">
    <div class="cover-party">
      <div class="cover-party-icon">RCRC</div>       <!-- or SVG -->
      <div class="cover-party-label">Client</div>
    </div>
    <div class="cover-party">
      <div class="cover-party-icon"><!-- BMA SVG--></div>
      <div class="cover-party-label">Designer</div>
    </div>
    <div class="cover-party">
      <div class="cover-party-icon">SA</div>           <!-- or Samaya logo -->
      <div class="cover-party-label">Contractor</div>
    </div>
  </div>
</div>
```

## CSS Requirements

- Client SVG needs `filter: brightness(0) invert(1)` on dark backgrounds (navy cover)
- Party icons: text or SVG, centered, with label below
- No AI-generated branding — use only official logos from source

## Pitfalls

- **White SVG on white background:** If the logo is white-only (borismicka.com logo-white.svg), it's designed for dark backgrounds — OK on navy cover, invisible on white. If the proposal has light sections, get a dark variant.
- **SVG viewBox:** Always preserve original viewBox. Scale via `width:auto; height:Npx` not via viewBox manipulation.
- **base64 PNG size:** Samaya-Logo.png is 191x71px, ~10K base64 chars — OK for HTML but adds ~30% to file size. Acceptable.
- **Page headers:** Small `SAMAYA` text in running headers (`.header-logo`) is fine at 12-14px — no need to replace with image.
- **Codex alternative:** The user mentioned `codex` for logo embedding. If codex CLI is installed, you can delegate: `codex exec "embed the 3 logos into the proposal cover"` — but direct patch is faster for known-content HTML.
