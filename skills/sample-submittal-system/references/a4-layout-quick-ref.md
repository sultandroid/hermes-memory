# A4 Landing Page Layout Quick Reference

Dimensions: 210mm × 297mm (A4 portrait). 
Container: `.page { width:210mm; height:297mm; overflow:hidden; display:flex; flex-direction:column; }`

## Section breakdown (top to bottom)

| Section | Height | Notes |
|---------|--------|-------|
| Navy top bar | 12mm | 5 logos (MoC·PMC·CG·NRS·Samaya), white-filtered, label right |
| Title + meta | ~15mm | 24px h1 + code + category tags + meta line with ref/museum/client |
| Photo + info body | ~140mm photo + specs | 42/58 split, photo cropped (object-fit:cover, 135mm height) |
| Bottom strip | ~30mm | 3 cells side by side: QR (22mm) + datasheets + approval (82mm) |
| Footer | ~8mm | Thin navy top border |

## Key CSS patterns

**Page container:**
```css
.page { width:210mm; height:297mm; margin:8mm auto; background:#fff; display:flex; flex-direction:column; overflow:hidden; }
```

**Two-column body:**
```css
.body { flex:none; display:flex; padding:6mm 12mm 0; }
.col-photo { width:42%; flex:none; }
.col-photo img { width:100%; height:135mm; object-fit:cover; }
.col-info { width:58%; padding-left:8mm; margin-left:8mm; border-left:1px solid var(--border); }
```

**Bottom strip (3 cells):**
```css
.strip { margin-top:auto; padding:0 12mm; display:flex; }
.cell-qr { width:22mm; flex:none; }
.cell-ds { flex:1; }
.cell-ap { width:82mm; flex:none; }
```

**Approval signature lines (generous for stamps):**
```css
.cell-ap .sig { width:50%; }
.cell-ap .sig span { border-bottom:1.5px solid #999; height:14px; }
.cell-ap .dt { width:22px; }
.cell-ap td { font-size:7px; padding:3px 5px 2px 0; vertical-align:bottom; }
```

## Logo assets

Source logos from:
```
_Assets/MOS/.../02.15_Method_Statements/.../assets/
  moc-logo.png
  pmc-logo-trans.png  
  cg-logo-trans.png
  nrs-logo-trans.png
  samaya-logo-trans.png
```

Upload to server: `assets/` subdirectory alongside `index.html`.
Reference as: `src="assets/moc-logo.png"`.
Styling: `filter:brightness(0) invert(1)` on all logos except Samaya in the top bar.

## Print

```css
@page { size:A4 portrait; margin:0; }
@media print {
  .page { margin:0; box-shadow:none; }
  * { -webkit-print-color-adjust:exact; print-color-adjust:exact; }
}
```

## Pitfalls

- **Do NOT use `@media print` on a screen-first layout** — user will reject it ("same design"). Build the page for A4 from scratch.
- **Approval rows must be separate** — NRS, CG, PMC each get their own row with individual signature/date. Do NOT merge into one "Reviewed" row.
- **Logo filter** `brightness(0) invert(1)` renders PNG as white on dark — ok for MoC/PMC/CG/NRS. Samaya logo keeps original colors.
- **Photo must be cropped** — `height:135mm; object-fit:cover` on a 42% column. Without this, the photo overflows the page.
- **All measurements in mm** except font sizes (px). No sub-pixel values that don't round cleanly.
