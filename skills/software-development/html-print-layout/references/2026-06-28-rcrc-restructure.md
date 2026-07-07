# RCRC Exhibition Restructure — Key Lessons (2026-06-28)

## Simple Python concat beats two-pass build

For a 49-page A4 document, the simple concat approach (base.html + numbered page partials + assemble.py) was far more reliable than a two-pass build with Puppeteer measurement and placeholder replacement.

**Why:** Two-pass builds introduced brittle failure modes:
- Puppeteer timeout on `file://` URLs
- Regex post-processing stripped `>` from section tags (producing `ection class="page">>` — the `>>` bug)
- Page-count miscounts from regex not matching `page-cover` / `page-divider` classes
- Section number drift between manifest and rendered output

**Verdict:** For A4 documents with fixed page positions (each page is exactly `<section class="page">` with `page-break-after:always`), editing a page never shifts other pages. Pre-numbered static files stay valid. No build-time computation needed.

## Flexbox content stretching for sparse A4 pages

Some pages had very little content (2500-3000 bytes) leaving most of the A4 vertical space empty.

**Fix:** Added `display:flex;flex-direction:column` on `.page` and `flex:1 1 auto` on `.ar` (Arabic text divs). Content now stretches to fill available vertical space, pushing the footer to the bottom. All other page elements (header, h2-row, strip, table, footer) are `flex-shrink:0`.

```css
.page{display:flex;flex-direction:column}
.page>.ar{flex:1 1 auto}
```

## Divider-to-banner merging

4 divider pages (Part 2-5) were ~600 bytes each — intentionally minimal (centered part title on dark navy). The user found these "white pages" (empty). 

**Fix:** Removed divider pages entirely. Merged the part title into the first content page of each part as a dark navy banner at the top of the page, between the h2-row and the content.

## The `>>` regex bug

When using regex to modify section tags, the pattern:
```js
const pageRegex = /<section[^>]*class="[^"]*page[^"]*"/g;
```
Matches `<section class="page page-cover">` only up to the final `"` of the class attribute — NOT including the closing `>`. The replacement then adds its own `>`, but the original `>` remains, producing `>>` at the end of every section tag.

**Fix:** Consume the entire opening tag:
```js
const pageRegex = /<section[^>]*class="[^"]*page[^"]*"[^>]*>/g;
```

## Pre-existing malformed h2-row across page boundary

The original HTML had `<div class="h2-row"><div class="h2-bar"></div>` opening on page 20 but the `<h2>` and `</div>` on page 21 outside any `<section>` tag. Mechanical splitting by `<section>` boundaries produced:
- Page 20: empty page with orphaned div start
- Page 21: bare `</div>` with no section wrapper

**Fix:** Manually reconstruct both pages. Page 20 gets its own complete h2-row with a proper h2 title. Page 21 gets its own `<section class="page">` wrapper with header + h2-row.

## Python vs Node.js for file I/O on macOS

Node.js `fs.readFileSync` on 49 HTML files (total ~640KB) took 44+ seconds — consistently timing out the terminal tool at 30s. Python's `open()` completed in <1 second.

**Verdict:** Always use Python for assemble/deploy scripts on this system. Update `package.json` to run `python3 scripts/assemble.py`.
