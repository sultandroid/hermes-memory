# Dimension Stripping for Info Card Descriptions

When displaying material descriptions in info card tooltips or sidebars, raw descriptions often contain dimensions that clutter the presentation. This reference documents the regex approach to strip them while preserving the meaningful text.

## Common Dimension Patterns in Museum/Construction Descriptions

| Pattern | Example | Stripped |
|---------|---------|----------|
| Leading dim | `2500 x 450mm freestanding bespoke bench in dark wood` | `Freestanding bespoke bench in dark wood` |
| Leading 3D dim | `3500(w) x 4000(h) x 400(d)mm freestanding wall` | `Freestanding wall` |
| Leading Nx prefix | `8x Group Object Label Housing` | `Group Object Label Housing` |
| Leading thickness | `3mm thick powder coated metal shelves` | `Powder coated metal shelves` |
| Mid-sentence dim | `Theme Panel Housing - 420mm x 1420mm graphic housing` | `Theme Panel Housing` |
| Trailing specs | `Speaker / 286 x 205mm / 75w` | `Speaker` |

## JavaScript Implementation

```typescript
export function cleanName(desc: string): string {
  if (!desc || desc === '#VALUE!' || desc === 'n/a' || desc === 'N/A') return desc || '';
  let s = desc.trim();
  
  // 1. Leading dimension: "2500 x 450mm ", "1960x450mm ", "3500(w) x 4000(h) x 400(d)mm "
  s = s.replace(/^[\d.]+(?:\([wWhHdD]\))?\s*[xX×]\s*[\d.]+(?:\([wWhHdD]\))?(?:\s*[xX×]\s*[\d.]+(?:\([wWhHdD]\))?)?\s*mm?\s*/i, '');
  
  // 2. Leading "Nx " pattern: "8x ", "3x "
  s = s.replace(/^\d+\s*[xX]\s+/i, '');
  
  // 3. Leading thickness: "3mm thick ", "10mm thick "
  s = s.replace(/^[\d.]+mm\s+thick\s+/i, '');
  
  // 4. Trailing/middle dimension fragments: " - 450 x 2000mm", " - 172mm x 304mm"
  s = s.replace(/\s*[-–—]\s*[\d.]+(?:\([wWhHdD]\))?\s*[xX×]\s*[\d.]+(?:\([wWhHdD]\))?(?:\s*[xX×]\s*[\d.]+(?:\([wWhHdD]\))?)?\s*mm?\s*/g, '');
  
  // 5. Remaining embedded dims like " / 286 x 205mm"
  s = s.replace(/\s*[/,]\s*[\d.]+(?:\([wWhHdD]\))?\s*[xX×]\s*[\d.]+(?:\([wWhHdD]\))?\s*mm?.*/gi, '');
  
  // 6. Strip trailing "mm" specs: " 1000mm", " (mm)"
  s = s.replace(/\s+\d+mm\s*$/, '');
  s = s.replace(/\s*\(\s*mm\s*\)\s*/g, '');
  
  // Clean up and capitalize first letter
  s = s.replace(/\s{2,}/g, ' ').replace(/\s+\./g, '.').replace(/\s+,/g, ',').trim();
  s = s.charAt(0).toUpperCase() + s.slice(1);
  
  return s || desc.trim();
}
```

## Pitfalls

- **Regex ordering matters** — apply leading patterns first (full dimension prefix) before inline patterns (mid-sentence dashes) to avoid partial matches corrupting the string
- **Capitalized first letter** after stripping helps presentation but check that the original starts with lowercase for proper names
- **Some descriptions have no dimension prefix** — "Theme Panel Housing - 420mm x 1420mm..." starts with the name, then has a dash + dims. Pattern #4 handles this case
- **Always test against real data** before deploying — the exact format varies between data sources (e.g., `mm` vs `mm ` vs `mm.`)
