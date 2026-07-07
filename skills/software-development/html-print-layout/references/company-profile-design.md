# Company Profile HTML Design — Samaya Factory Pattern

Bilingual (Arabic-led) A4 landscape company profile with premium print layout.

## Page Structure

| Page | Section | Content |
|------|---------|---------|
| 1 | Cover | Factory hero photo, brand, edition, compliance badges |
| 2 | TOC | Table of contents with page anchors |
| 3 | About | Workshop team portrait, identity prose (Who/Vision/Mission) |
| 4 | Operational Capacity | Clean 4-stat counters (8,000m² / 53,000m² / 217 eq / 25y), pipeline, photo tiles, tech stack |
| 5+ | Scope, Process, Projects | Various archetypes per DESIGN.md |
| ~27 | Back Cover | Thank you, contact grid, QR code |

## User Preferences (Durable)

- **No charts on Operational Capacity page** — clean stat counters only.
- **Replace existing photos, don't add new blocks** — swap the existing image, not insert a new tile.
- **No duplicate photos** — every image exactly once. Run Counter() scan after bulk replacements.
- **Keep content process-focused** — avoid naming specific client projects in methodology sections.
- **Slogan is SACRED** — DO NOT change "صناعة الإرث. هندسة الفنّ." / "Crafting Legacy. Engineering Art." on the cover. Claude redesigns often alter this — restore before deploying.

## Design Tokens

```css
:root {
  --navy: #1E293B;
  --gold: #C9A24B;
  --gold-deep: #A47A1F;
  --gold-pale: oklch(0.92 0.05 80);
  --paper: #F6F0E4;
  --ink: #1E293B;
  --ink-soft: oklch(0.40 0.05 260);
  --ink-mute: oklch(0.62 0.025 250);
}
/* Fonts: Tajawal (Arabic), Inter (English), Cormorant Garamond (serif/italics) */
```

## Cover Photo

- CSS background-image on `.v3-photo-img` via `var(--v3-img, url(...))` variable
- **⚠ CSS variable URL resolution issue:** `--v3-img` defined as inline HTML style on `<section>`, but the `url()` resolves relative to the CSS file when consumed via `var()` — not the HTML file. Browsers differ in behavior. **Fix:** set `background-image` directly via inline `style` on the `.v3-photo-img` element and use the CSS variable only as a fallback.
- Optimize: `sips --resampleWidth 1920 --setProperty format jpeg --setProperty formatOptions 85`
- **Surge CDN cold start:** after deploy, hero may return 504 for 10-30s. Normal — wait and retry.

## Slogan on Cover (DO NOT CHANGE)

The cover slogan is the company's primary brand statement. It appears in:
- Arabic: `<span>صناعة الإرث.</span><span>هندسة الفنّ.</span>`
- English: `<span>Crafting Legacy.</span><span>Engineering Art.</span>`

**This is a hard blocker.** Any redesign that changes this text must be reverted before deploy. Check after every Claude Code design pass.

## Stat Counters (Page 4 — Operational Capacity)

NO charts, NO gauges, NO SVG visualizations. Clean stat numbers only.

## Overflow Prevention Strategy

Two patterns, depending on content volume:

### Pattern A: Single-page content (most pages)
Keep the content constrained to one A4 page:
```css
.page-type .content {
  height: calc(210mm - 22mm - 14mm);  /* A4 landscape - header - footer */
}
.page-type {
  height: 210mm;
  overflow: hidden;
}
```

### Pattern B: Multi-page content (50+ grid cells, Materiality)
Remove the height clamp so content flows to subsequent pages:
```css
.page-type .content {
  /* NO height clamp */
  overflow: visible;
}
.page-type {
  height: auto;
  min-height: 210mm;
}
.page-type .grid {
  grid-auto-rows: auto;  /* rows size to content, not forced equal */
}
```
The user explicitly approved: "you can make more than one page no problem".

### Back cover fix
The back cover (`.ed-back-cover`) stretches when global `.page` has `height: auto`. Fix:
```css
.ed-back-cover { height: 210mm; overflow: hidden; }
```

## Materiality Grid Photo Sizing

- **`background-size: contain` NOT `cover`** — user rejected cropping. Photos must show fully.
- Cell height: 22mm (reduced from 48mm after overflow fix for 70+ cells)
- `background-repeat: no-repeat` to prevent tiling
- Footer counts: update from `N PROCESS DETAILS` to `N+1 PROCESS DETAILS` when adding cells

## QR Code on Back Cover

Position the QR **inline beside the text** (not below it):
- Text left, QR right — `display:flex; flex-direction:row`
- Size: 16mm (not 20mm)
- Gold border `0.5px solid var(--gold)` with 1mm border-radius
- **Never stack QR below text on its own row**

## Editorial Text Style

- **Punchy, active verbs in Arabic** — e.g., "نصنع المتاحف" not "صناعة المتاحف"
- **English uses em-dashes** for rhythmic breaks: "Every Decision Documented. Every Change Approved."
- **Vary layout density** — alternate between dense technical pages and airy editorial pages
- **No two adjacent pages should feel the same**
- Museum-catalog tone: italic Cormorant tags, concise bilingual pairings

## TOC Maintenance

**Always update the TOC (p2) when:**
- Pages are added, removed, or renumbered
- Section tags change
- Page numbers in footers change

The TOC has ~21 entries across 2 columns with 4 act dividers. Each entry has: number, Arabic title, English subtitle, and page reference.

Check after every batch of page changes.

## Flagship Hero Photo Alternation

Flagship project pages (p4-flag4 through p4-flag8) use a two-column RTL grid:
- Column 1 (1.2fr): pf-panel (text) — appears on RIGHT in RTL
- Column 2 (0.8fr): pf-hero (photo) — appears on LEFT in RTL

**Alternate** which side the photo appears on by swapping DOM order:
- Even flagships (4,6,8): put pf-hero FIRST → photo on RIGHT
- Odd flagships (5,7): put pf-panel FIRST → photo on LEFT

This creates visual rhythm across 5 flagship spreads.

## 3D Scanning Methodology Page (p13a)

Use ONLY 4 photos telling a narrative:
1. Scanner device (hero)
2. Scan in progress
3. Accuracy verification
4. Digital twin / finished output

Text should be **concise, step-by-step** — not marketing. Use numbered steps (① ② ③ ④) with bullet-style descriptions. The user said "dont talk too much" — keep every line to 1-2 clauses separated by · (middle dot).

**AR captions** must be equally concise — matching the EN pattern.

**Keep it process-focused, not project-specific.** The user will reject mentions of specific client projects (e.g., "Aseer Museum") in methodology sections. Use the scanner model name (e.g., "Artec Spider II") and generic terms ("heritage artefacts and stonework") instead.

**Scan comparison gallery** — show actual-stone paired with 3D-model in a before/after layout. Three columns of paired images works well: actual photo above, scan model below, with a label per column.

## Overflow Audit Checklist

After any layout/content change, check:
1. Does the page have `height: calc()` that will clip content? If so, remove it or adjust content.
2. Does the page use `overflow: hidden` on .content? If multi-page, remove it.
3. Is the back cover `.ed-back-cover` fixed at 210mm?
4. Are grid items the right size (Materiality: 22mm, Replica Gallery: 52mm)?
5. Do flagship pages use the RTL two-column grid (modal row — no overflow possible)?
6. Is the TOC page count still accurate?

## CSS/HTML Class Mismatch After Section Copy

When copying sections between v5 and v6 (or between any two versions), the HTML classes may not match the CSS that exists in the target version. **Always verify** by searching the CSS files for each class used in the HTML section:

```python
# After copying a section, verify all CSS classes exist
import re
with open("index.html") as f:
    html = f.read()
with open("css/style.css") as f:
    css = f.read()

# Extract all classes from the section
section = re.search(r'<section[^>]*id="p14"[^>]*>.*?</section>', html, re.DOTALL)
classes = set(re.findall(r'class="([^"]+)"', section.group()))
# Flatten multi-class entries
all_classes = set()
for c in classes:
    for cls in c.split():
        all_classes.add(cls)

# Check each class exists in CSS
missing = [c for c in all_classes if f'.{c}' not in css and 'v4-' in c]
if missing:
    print(f"MISSING from CSS: {missing}")
```

**Pitfall:** v5 HTML uses old class names like `v4-cmyk-head`, `v4-cmyk-body`, `v4-cmyk-outputs` but v6 CSS has `v4-cmyk-hero`, `v4-cmyk-process`, `v4-cmyk-apps`. The page renders without any styling — just raw HTML stacking.

**Fix:** Rewrite the HTML to use the target version's CSS classes, preserving the content structure.

## Page Numbering Audit

After inserting/removing/renumbering pages, audit ALL of these synchronously:

1. **Footer page numbers** — `<div class="num">NN</div>` in each section's `<footer>`
2. **Section tags** — `<div class="section-tag">NN · NAME</div>` at the top
3. **TOC page references** — `<span class="v3-toc-p">NN</span>`
4. **TOC entry numbers** — `<span class="v3-toc-n">NN</span>` (these are section numbers, not page numbers — keep consistent)

### Audit pattern

```python
import re
with open("index.html") as f:
    html = f.read()

# Collect all footer page numbers
page_nums = []
for m in re.finditer(r'<div class="num">([^<]+)</div>', html):
    page_nums.append(m.group(1))

# Check sequential
prev = 0
for i, pn in enumerate(page_nums):
    if pn.isdigit():
        n = int(pn)
        if n != prev + 1 and n > 0:
            print(f"Gap: {prev} → {n} at page position {i+1}")
        prev = n
```

### Common numbering fixes needed

| Issue | Example | Fix |
|-------|---------|-----|
| Footer out of sync with page position | p6 footer says 06 but is 8th page | Update footer to 08 |
| Section tag prefix doesn't match | p19 tag says "13 · GRC" but footer says 17 | Update tag to "17 · GRC" |
| Sub-page numbering | p13b tag says "11b" but follows p13 | Update to "13b" |
| Missing page number | p12 footer has no `<div class="num">` | Add it |
| TOC reference stale | TOC says QA/QC is on page 06 but footer says 08 | Update TOC `<span class="v3-toc-p">` |

## "Do Not Deploy" Workflow

When the user explicitly instructs "Do not deploy. Do not publish. Do not push to production.", this is a binding constraint. The workflow becomes:

1. Make all changes locally
2. Verify all files on disk (not on a live server)
3. Verify all images exist with `os.path.isfile()`
4. Verify HTML nesting with div/section counter
5. Present the changes for review
6. WAIT for explicit deploy approval

### Verification commands for local-only work

```python
import os
# Verify all referenced images exist on disk
base = "/path/to/project"
for ref in image_refs:
    path = os.path.join(base, ref.replace("../", "", 1))
    if not os.path.isfile(path) and not os.path.isfile(unquote(path)):
        print(f"MISSING: {ref}")
```

## Delegating to Claude Code (Preferred Approach)

The user prefers to delegate ALL visual design/redesign work to Claude Code. Do NOT attempt to manually redesign pages with complex CSS/HTML unless it's a simple overflow fix or class correction.

### When to delegate
- Page redesign (layout, cards, colors)
- Adding new visual components
- Creating process flows, timelines, or diagrams
- Any task tagged "consult claude"

### When NOT to delegate (handle yourself)
- Simple image path fixes
- Overflow/height constraint fixes
- Page numbering updates
- TOC updates
- HTML class fixes
- Deploy/build tasks

### Delegation template

```
Context: [file paths, current HTML snippet, available images]
Goal: [specific before→after description]
IMPORTANT: Use ONLY real existing photos from the assets directory. 
Do NOT create placeholder or SVG images.
```

### Post-Claude verification checklist

After Claude Code returns, always verify:
1. ✅ Slogan unchanged (if cover was touched)
2. ✅ No duplicate images (run Counter() scan)
3. ✅ TOC still accurate
4. ✅ Overflow still acceptable
5. ✅ Arabic text renders correctly
6. ✅ No broken HTML nesting
7. ✅ No new blocks added (user wants replacement, not insertion)
8. ✅ No SVG placeholder images created
9. ✅ CSS classes match the CSS file (no orphan classes)

## Photo Usage Rules

### Replace photos, don't add blocks
The user does NOT want new tiles/cards/blocks added. Only replace the existing image in the current block. Check: "i didnt request to add new block i men you replace photo with current photo on 02 block".

### No duplicate images (ever)
After any bulk HQ photo replacement, verify with Counter() that every image appears exactly once. The user caught this and insisted.

### Verify project photos match their section
**Pitfall:** It's easy to grab a photo from the wrong project directory (e.g., safia-museum-hoarding-facade.jpg for Khair Al-Khalq). Always cross-reference:
- The HTML section's title/label tells you which project it's for
- The folder or filename prefix should match that project
- If in doubt, verify against the user's source photo folders

### Flagship alternation rule
Even-numbered flagship pages (4,6,8): photo on RIGHT. Odd-numbered (5,7): photo on LEFT. This creates visual rhythm across the spread.

### Image optimization (portrait vs landscape)
- Landscape images: `--resampleWidth 1920`
- Portrait images: `--resampleHeight 1200` (or the desired vertical dimension)
- Quality: `--setProperty formatOptions 85`

## Delegating to Claude Code

Pass:
- Exact file paths (+ line ranges)
- Current HTML snippet (5-10 lines context)
- Clear before→after description
- CSS variable names
- Font/color palette

### Post-Claude checks:
1. **Slogan unchanged** — revert if altered
2. **No new blocks added** — user wants photo replacement, not new tiles
3. **No duplicate images** — run Counter() scan
4. **TOC still accurate** — update if pages changed
5. **Overflow still OK** — check if Claude added content that exceeds A4
6. **Arabic text correct** — verify no broken glyphs or missing diacritics
7. **Project photo matches section** — verify photos aren't from wrong project folders
8. **No client/project names in methodology pages** — keep process-focused language
9. **No SVG placeholder images** — Claude subagents sometimes create SVG placeholder files when real images are missing. Always verify every image reference points to a real JPEG/PNG file. Add "Use ONLY real existing photos" explicitly to every delegation prompt.
10. **Sections between p13 and p13b** — p13a (3D Scanning) was inserted between these; verify p13 still closes properly without the scan section

## Image Optimization

```bash
# Batch resize to max 1920px wide, Q85
find "$dir" -type f \( -iname "*.jpg" -o -iname "*.jpeg" \) \
  -exec sips --resampleWidth 1920 --setProperty format jpeg \
  --setProperty formatOptions 85 {} --out {} \;
```

## Surge Deploy

```bash
surge /tmp/deploy-dir/ --domain project-name.surge.sh
```
Always stage in `/tmp/` — OneDrive causes timeouts/504s.

Verify: `surge ... 2>&1 | grep -E 'Success|Published|error'`
