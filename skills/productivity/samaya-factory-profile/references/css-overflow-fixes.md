# CSS Overflow & Page Balance Fixes for Samaya Profile

## Global Page Rule (00-tokens.css:63-68)

**Multi-page mode** (most pages):
```css
.page {
  height: auto;
  min-height: 210mm;
  overflow: visible;
}
```

**Single-page mode** (back cover only):
```css
.ed-back-cover {
  height: 210mm;
  overflow: hidden;
}
```

## .content div strategies

### Single-page content (fill A4 exactly)
Add to the section-specific `.content` rule in the appropriate CSS file:
```css
height: calc(210mm - 22mm - 14mm);
```
And use `grid-template-rows: ... 1fr ...` so the last row expands.

### Multi-page content (flow onto next page)
Remove all height constraints on `.content`:
```css
height: auto;  /* or remove the line entirely */
overflow: visible;  /* NOT hidden */
```

## Common Pitfalls

1. **1fr collapsing**: After removing `height: calc(...)` from `.content`, any `1fr` in `grid-template-rows` collapses to `auto`. Replace with `auto` or add a new height constraint.

2. **Inline overflow:hidden**: Some pages have inline `style="overflow:hidden"` on the `.content` div. Must be removed with patch().

3. **CSS variable name changes**: The profile uses both old (--v3-line, --v3-gold) and new (--hairline, --gold) variable names. New code should use the new names.

4. **Restoring from v5**: The per-archetype CSS files (31-cover.css through 45-overrides.css) were split from the original `30-redesign.css` monolith. If accidentally overwritten, restore from the v6-backups directory. The split completed on 2026-06-07 — `30-redesign.css` is no longer linked from index.html (retained on disk as reference only).

5. **Page class collision**: `.ed-spread` pages (HSE, After-Sales, Scanning) use inline styles on `.content` div with `height:calc(210mm - 22mm - 14mm)` — these should keep it for single-page balance but remove `overflow:hidden`.

## Page Class Collisions Found

### `.ed-spread` vs custom section classes
**Problem**: `.ed-spread .content` (specificity 0,2,0 in 20-redesign.css) overrides custom class rules like `.v4-scan-meth` (specificity 0,1,0).

If a page has both `ed-spread` on the section and a custom class on `.content`, the `ed-spread` layout (grid, padding:0) wins over the intended flex layout.

**Fix**: Don't use `ed-spread` on sections with custom layout classes. Only use `ed-spread` for pre-built archetypes (HSE, Approvals, After-Sales).

### Quick reference: height calc logic
- 210mm = A4 landscape height
- 22mm = page header (brand + section-tag)
- 14mm = page footer
- Result: 174mm content area

## v4-catalog (Display/Vitrines) Overflow

#p12 (class v4-catalog) overflows by ~8-10mm due to: title block (18mm) + photo strip (40mm) + 4-column grid (51mm) + post-grid cards+process+disclaimer (50mm) + padding/gaps (~12mm) = ~179mm > 174mm.

**Fix (applies ~16mm savings):**

1. Photo strip `height: 40mm` → `32mm` (inline style)
2. `.v4-catalog-col-img { block-size: 43mm; }` → `38mm` (37-catalog.css)
3. Post-grid margin-top: 5mm → 3mm, padding-top: 3.8mm → 2.4mm
4. Process pill margin-top: 3.5mm → 2.5mm, padding: 2mm → 1.5mm
5. Disclaimer margin-top: 3mm → 2mm, padding: 2.6mm → 2mm

## TOC Broken Link Detection

After structural changes (pages added/removed/renumbered), dead TOC links are common:
```bash
# Extract all TOC href="#p..." targets
toc_refs=$(grep -oP 'href="#p[^"]*"' v6/index.html | sed 's/href="#//;s/"//')
# Extract all section IDs
section_ids=$(grep -oP 'id="p[^"]*"' v6/index.html | sed 's/id="//;s/"//')
# Check each TOC ref exists as a section
for ref in $toc_refs; do
  if ! echo "$section_ids" | grep -q "$ref"; then
    echo "BROKEN TOC LINK: #$ref → no matching section"
  fi
done
```
Common victims: `p13a`, `p13a-1` (removed but TOC entries lingered).
- 60+ cells in 4-column grid = ~15+ rows. Each cell 22mm image + 3mm caption ≈ 25mm per row
- Total: 15 × 25mm = ~375mm ≈ 2-3 pages
- If adding more cells and overflow returns, reduce cell height further (18mm min)
- The `.content` div has NO fixed height constraint — flows naturally to multiple pages
