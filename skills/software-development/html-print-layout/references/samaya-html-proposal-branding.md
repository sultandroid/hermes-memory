# Samaya HTML Proposal — Branding Conventions

## Critical — USE THE REAL LOGO FILES, NOT TEXT APPROXIMATIONS

The user will CORRECT you if you create fake SVG text-based logo approximations. Always use the actual logo files.

### Samaya Logo

**Path:** `_Style-Guides/logos archives/samaya-logo-trans.png`
**Format:** PNG (transparent background), bilingual Arabic/English
**Usage:**
- Light backgrounds: `<img src="...samaya-logo-trans.png" alt="Samaya" style="height:14px;vertical-align:middle">`
- Dark backgrounds: `<img src="...samaya-logo-trans.png" alt="Samaya" style="...filter:brightness(0) invert(1)">`
- The filter turns the PNG into a white silhouette on navy/colored backgrounds
- NEVER create inline SVG with text elements (S-A-M-A-Y-A with red A, diamond shapes, etc.)

### RCRC Logo

**Source:** `https://www.rcrc.gov.sa/wp-content/uploads/2026/06/RCRC-logo-2.svg`
**ViewBox:** 189×41
**Description:** Official tree/plant emblem in dark green `#1D8649`
**Saved at:** `_Style-Guides/logos archives/rcrc-logo.svg`
**Usage on dark bg:** Embed the SVG directly with `fill="#fff"` for all paths. Do NOT use `filter:brightness(0) invert(1)` on inline SVGs that already have white fills.

### BMA (Boris Micka Associates) Logo

**Source:** `https://www.borismicka.com/images/logo-white.svg`
**ViewBox:** 375×30
**Description:** Full Boris Micka wordmark, white path data
**Saved at:** `_Style-Guides/logos archives/bma-logo.svg`
**Usage on dark bg:** Embed the SVG directly. Paths already use `fill="#fff"`. Do NOT add `filter:brightness(0) invert(1)` — it would invert white to black.

## Arabic Font — Cairo (NOT IBM Plex Sans Arabic)

When creating Arabic HTML documents:
- Primary Arabic font: **Cairo** (with weights 400-900)
- Google Fonts URL: `family=Cairo:wght@400;500;600;700;800;900`
- CSS variable: `--font-arabic: 'Cairo', sans-serif;`
- Chart/fallback font list: `font-family:'Inter','Cairo',sans-serif`
- DO NOT use IBM Plex Sans Arabic — user corrected this explicitly

## Brand Colors for Proposal HTML

| Use | Hex | CSS Variable |
|-----|-----|-------------|
| Primary (navy) | `#0F172A` | `--primary` |
| Secondary (sky) | `#0284C7` | `--secondary` |
| Green (pass) | `#16A34A` | `--accent` |
| Red (fail/critical) | `#B91C1C` | `--fail` |
| Amber (warning) | `#92400E` | `--warn` |

## Programme Timeline Chart — Samaya Brand

Use stacked horizontal bar design with Samaya colors, viewBox 840×160:
- Phases as colored segments in a single unified bar
- All 12 months labeled inline on one axis with tick marks
- Short Arabic labels: تصميم, مخططات, مشتريات, تصنيع, تركيب, تشغيل, تسليم
- Legend strip at bottom showing all 5 brand colors
- W1 / W26 / W52 milestone markers
- No overlapping arrows — clean stacked bar only

## Agent Routing for HTML Tasks

| Work Type | Delegate To | 
|-----------|-------------|
| SVG charts, timeline graphics | Claude |
| Logo sourcing, cover graphics | Codex (but verify logos are REAL, not fake SVGs) |
| QC review, structural audit | Kimi |
| Major page redesign, cover from scratch | Pi (if available) |

## Cover Bottom Party Icons — Masking Pattern

All three party icons (RCRC, BMA, SAMAYA) at cover bottom must render white on navy:

1. **RCRC**: Embed real SVG, replace all fills with `#fff`, NO filter
2. **BMA**: Embed real white-path SVG directly, NO filter (paths are already white)
3. **SAMAYA**: PNG with `filter:brightness(0) invert(1)` to create white silhouette

Verify each icon renders as pure white on the navy background. Remove any `brightness(0) invert(1)` filter from SVGs that already have `fill="#fff"` paths.
