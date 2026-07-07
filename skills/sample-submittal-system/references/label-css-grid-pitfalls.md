# CSS Grid Interaction Pitfalls in Fixed-Height Labels

## Problem: `auto` Rows Collapse to Zero

When a fixed-height CSS Grid has `1fr` followed by `auto`, the `1fr` row absorbs ALL remaining space, leaving **zero height** for the `auto` row.

```css
/* WRONG — QR band (.auto) gets 0px */
.front-cover {
  display:grid;
  grid-template-rows:18mm 30mm 1fr auto 10mm;  /* auto = 0 */
}
```

**Fix:** Give every row an explicit height:

```css
/* RIGHT — all rows have defined height */
.front-cover {
  display:grid;
  grid-template-rows:18mm 30mm 1fr 14mm 10mm;  /* QR row explicit */
}
```

## Problem: Photo Not Rendering in Grid + Flex Container

When a `<div>` is both a CSS Grid cell (`1fr`) AND a flex container (`display:flex; align-items:center;`), the `<img>` inside needs **both** `height:100%` and `width:auto` to render at the correct size.

```css
/* WRONG — photo renders at intrinsic size, overflows */
.photo-frame {
  min-height:0;
  background:var(--warm-bg);
  padding:2mm;
  display:flex; align-items:center; justify-content:center;
  overflow:hidden;
}
.photo-frame img {
  max-width:100%; max-height:100%;
  object-fit:contain; display:block;
  /* missing height:100% — the img uses intrinsic dimensions */
}
```

**Fix:**

```css
.photo-frame img {
  height:100%;        /* fills the flex container */
  width:auto;          /* maintains aspect ratio */
  max-width:100%;      /* never wider than container */
  object-fit:contain;  /* scales within bounds */
  display:block;
}
```

**Why it matters:** Without `height:100%`, the `<img>` defaults to its intrinsic pixel dimensions (e.g., 1200×1600), which is far larger than the grid cell and overflows silently.

## Problem: CSS `filter` Fails in Print Renderers

`filter: brightness(0) invert(1)` works in browsers but fails in most print engines (Adobe Acrobat, Preview PDF), causing logos to render black-on-navy (invisible).

**Fix — add `@media print` override:**

```css
.party-logo img {
  filter:brightness(0) invert(1);
  opacity:.92;
}
@media print {
  .party-logo img {
    filter:none;
    -webkit-filter:none;
  }
}
```

For SVG text logos, add `fill="#ffffff"` explicitly.

## Problem: CSS Gradients Fail in Print

Complex gradients (`repeating-radial-gradient`, `linear-gradient` with transparency) may not render in print engines.

**Fix — solid fallback:**

```css
.back-cover::before {
  background:repeating-radial-gradient(...);
  -webkit-print-color-adjust:exact;
  print-color-adjust:exact;
}
@media print {
  .back-cover::before {
    background:var(--navy);  /* solid fallback */
  }
}
```

## Debugging Checklist

When a label section is invisible or wrong size:

1. **Is the element there?** — Right-click → Inspect in browser. Check computed styles.
2. **Is `auto` row collapsing?** — Temporarily change `auto` to a fixed value like `20mm`. If it appears, that's the problem.
3. **Is `height:100%` set on img?** — Without it, the img uses intrinsic pixel size.
4. **Is overflow hidden?** — Check `overflow:hidden` on parent elements.
5. **Are all units in mm/pt?** — Stray `px` values cause rendering inconsistencies.
