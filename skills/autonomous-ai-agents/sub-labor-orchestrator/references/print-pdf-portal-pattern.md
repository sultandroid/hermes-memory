# Print-to-PDF via React Portal + CSS

## Pattern
Render a print-optimized React component via `createPortal(..., document.body)` and call `window.print()` after images load. The portal renders directly to `<body>`, bypassing the app's stacking context.

## Key CSS Lessons

### 1. `position: fixed` on print wrapper = no page breaks
```css
.print-wrapper { display: block !important; }  /* ✅ correct */
.print-wrapper { display: block !important; position: fixed; inset: 0; }  /* ❌ breaks pagination */
```
Browsers treat `position: fixed` elements as a single overlay — they cannot split them across pages. Without `position: fixed`, the wrapper participates in normal print pagination.

### 2. Page breaks need block elements, not flex containers
```css
/* ✅ works */
.print-page { page-break-after: always; }

/* ❌ breaks — flex with minHeight prevents pagination */
.print-page { display: flex; flex-direction: column; min-height: 26.7cm; }
```
`page-break-after: always` on a flex container with `minHeight` is unreliable. Use plain block elements.

### 3. Image sizing for A4 landscape
A4 landscape = 297mm × 210mm. Printable area after header + title/label + footer ≈ **95mm tall**.
```
max-height: 95mm; object-fit: contain;
```
`height: auto` alone causes overflow — images taller than available space push content to next page.

### 4. `@page` with zero margins
```css
@page { size: A4 landscape; margin: 0; }
```
Allows full-bleed header that extends to page edge. Content padding handled by `.print-view { padding: 8mm }`.

### 5. Hide everything except print content during print
```css
@media print {
  body > :not(.print-wrapper):not(style) { display: none !important; }
}
```
The `style` tag is excluded from hiding so `@page` and `@media print` rules still apply.

## Page Structure
```
Page 1: Header + Clean Photo (full width)
Page 2: Header + Annotated Photo (with numbered pins)
Page 3: Header + Material Legend Table
```
Header repeated on each page by including it inside each `.print-page` div.

## QR Code
Use `api.qrserver.com` with size≥200×200 for print:
```
https://api.qrserver.com/v1/create-qr-code/?size=200x200&data=URL
```
Render at ≥80px (≈21mm) for scannability at 300dpi.

## When Build Hangs (Vite + Node.js v22)
If Vite 7.3.x fails on Node.js v22 with `does not provide an export named 'g'`:
1. Fix source files
2. Patch the compiled JS directly: `sed -i '' 's/oldValue/newValue/g' dist/assets/index-*.js`
3. Restart the static server — no rebuild needed for CSS/value-only changes

## Sub-Labor Assignment
- **Codex**: Diagnose print CSS issues (page breaks, layout, portal)
- **Claude**: QC the fix — check page-break logic, image sizing within printable area, header repetition, QR size, TS correctness
