# Label Printing Pitfalls

## Print Readiness — CSS Standards

For professional printing (not just browser → PDF):

| Requirement | CSS | Why |
|------------|-----|-----|
| Bleed | `@page { size: 486mm 236mm; bleed: 3mm; marks: crop cross; }` | Prevents white edges after cutting |
| Crop marks | `marks: crop cross` in `@page` | Trim guides for the printer |
| No px units | Use **mm** for borders/padding, **pt** for fonts | Print engines render px inconsistently |
| No sub-pixel | Replace `0.5px`, `1.5px` with `0.15mm`, `0.4mm` | Fractional px may render as 0 in Adobe/Preview |
| Print color | `-webkit-print-color-adjust: exact; print-color-adjust: exact;` globally | Keeps backgrounds, gradients, colors |
| Filter fallback | `@media print { .logos { filter:none; } }` | CSS filters ignored by most print engines |
| Gradient fallback | `@media print { .gradient { background: solid-color; } }` | Complex gradients fail in PDF renderers |

**Bleed layout pattern:** Content lives in the safe 480×230mm center. Edge-to-edge elements (nav bar, footer, back cover background) extend 1.5mm with negative margins:

```css
.top-bar { margin:0 -1.5mm; }
.footer  { margin:0 -1.5mm -1.5mm; }
.back-cover { margin:-1.5mm; }
```

The `@page` size is 486×236mm (3mm added to each dimension). The printer trims to 480×230mm.

## Browsers & file:// Protocol

| Browser | Local image loading | Print fidelity |
|---------|-------------------|----------------|
| Safari | Blocks same-directory images via file:// | Good — respects @page size |
| Chrome | Blocks ALL local images via file:// | Good — print preview matches CSS |
| Firefox | Allows local images | Good — best for testing locally |

**Solution:** Embed images as base64 data URIs (see SKILL.md Critical Pitfall section).

## Print Settings (All Browsers)

1. **Paper size**: Select "240 × 330mm" or "Custom" → set 240mm × 330mm
   - If the size isn't in the dropdown, create custom paper size
2. **Margins**: Set to "None" or "Minimum"
3. **Scale**: 100% (no scaling)
4. **Background graphics**: Check ON (for dark green header/strip)
5. **Orientation**: Portrait

## OneDrive Sync Issues

- OneDrive macOS files can be "online-only" — browser can't read them even though `file` shows the file exists
- After copy/move: `Operation not permitted` errors are common
- **Fix:** Embed images as base64 (self-contained HTML)

## Creating Custom Paper Size (macOS)

1. Cmd+P → Paper Size dropdown → "Manage Custom Sizes"
2. Click "+":
   - Name: "Samaya Sample Folder 24x33"
   - Width: 240mm, Height: 330mm, Margins: None
3. Save → select from dropdown

## Folder Assembly

- Print label → trim to 240×330mm
- Mount on front cover of physical folder (clear sleeve or glue)
- Sample, datasheet, test report inside
- QR code should be scannable without opening folder
