# RCRC Exhibition Restructure — Lessons Learned (2026-06-28/29)

## Build Pipeline Decision
**Use simple Python concat, NOT two-pass with Puppeteer.** The two-pass approach introduced:
- Puppeteer timeout on `file://` URLs (page count returned 1 instead of 49)
- Regex `>` stripping bug (produced `ection class="page">>` — all section tags broken)
- Placeholder replacement failures
- Section number drift from post-processing

**Simple concat** (used in final version):
- `base.html` with `{{BODY}}` placeholder
- `pages/{NN}-title.html` — pre-numbered, one `<section class="page">` per file
- `scripts/assemble.py` — Python concat (NOT Node.js — `fs.readFileSync` times out on macOS)
- Zero post-processing, zero placeholder failures

## Always Use Python for File I/O
On this macOS system, Node.js `fs.readFileSync()` takes ~45s to read 49 small HTML files due to filesystem monitoring overhead. Python's `open()` does the same in <1s. All build scripts must use Python, not Node.js.

## Flex Layout Creates White Space (User Correction)
`display:flex; flex-direction: column` on `.page` with `flex:1 1 auto` on content divs PUSHES content down from the title, creating unwanted white space. The user explicitly rejected this approach.

**Fix:** Use block layout only. Content flows naturally:
```css
.page { position: relative; } /* no flex */
```
If a page is sparse, add content (KPIs, data tables, detail) rather than using flex to stretch. The user explicitly prefers content addition over flex gaps.

## No Prices in Technical Proposals
All monetary values (USD, SAR, $ amounts) must be removed from technical proposals. Replace budget references with "Budget Classification" or scope descriptions. Prices belong in the separate commercial proposal.

## SVG viewBox Must Fit All Content
Elements with y-values exceeding the viewBox height get clipped silently. Always check the maximum y + height of any SVG element and set viewBox to accommodate it.

**Pattern:** Run this check on every SVG:
```python
ys = re.findall(r'y="?(\\d+\\.?\\d*)"?', svg)
heights = re.findall(r'height="?(\\d+\\.?\\d*)"?', svg)
# viewBox height must be > max(y) + max(height) for elements
```

## Section Tag Regex Must Consume >
```js
// CORRECT — consumes >, replacement adds one >
const pageRegex = /<section[^>]*class="[^"]*page[^"]*"[^>]*>/g;
// WRONG — produces >> at end of every section tag
// const pageRegex = /<section[^>]*class="[^"]*page[^"]*"/g;
```

## Working Directory
Always work in `~/Documents/<project>/`. Never use `/tmp` — the user explicitly rejected this.

## Content After Title Rule
All content must start directly after the h2-row with no extra gap. The `.h2-row` has `margin-bottom:6px` — this is sufficient. No flex distribution of extra space.

## Team Name Corrections Are Iterative
Team member names go through multiple rounds of corrections. Expect changes like:
- Project Director: Waris Sultan → Adel Darwish
- Design Manager → Technical Office Manager: Eng. Mohamed Sultan  
- Commercial Mgr: TBC → Abdallah Mahfouz
- AV Lead: TBC → Rawasin
- Planning Engineer: TBC → Mohamed Elshikh

## Filesystem Performance
- Reading 49 page files: ~44s (extremely slow — blame macOS + Documents folder)
- Use `execute_code` (faster) instead of `terminal` for Python file ops
- Set timeouts generously: assemble.py needs 120s, deploy.py needs 30s

## Data Sources for Samaya Proposals
- Official Company Profile PDF (from Samaya): company history, vision, mission, 6 subsidiaries, services
- PEP docs: gallery data, team structure, execution methodology
- ER docs: compliance requirements
- QS Baseline: equipment quantities, RFQ references
- samayainvest.com: company overview, project portfolio
