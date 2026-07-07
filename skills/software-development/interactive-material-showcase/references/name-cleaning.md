# Name Cleaning & Dimension Stripping

Material descriptions often start with or contain raw dimensions that clutter the info card display.

## The cleanName() function

```typescript
export function cleanName(desc: string): string {
  if (!desc || desc === '#VALUE!' || desc === 'n/a' || desc === 'N/A') return desc || '';
  let s = desc.trim();
  // 1. Leading dimension: "2500 x 450mm ", "3500(w) x 4000(h) x 400(d)mm "
  s = s.replace(/^[\d.]+(?:\([wWhHdD]\))?\s*[xX×]\s*[\d.]+(?:\([wWhHdD]\))?(?:\s*[xX×]\s*[\d.]+(?:\([wWhHdD]\))?)?\s*mm?\s*/i, '');
  // 2. Leading "Nx " pattern: "8x ", "3x "
  s = s.replace(/^\d+\s*[xX]\s+/i, '');
  // 3. Leading thickness: "3mm thick ", "10mm thick "
  s = s.replace(/^[\d.]+mm\s+thick\s+/i, '');
  // 4. Inline dim fragments: " - 450 x 2000mm", " - 172mm x 304mm"
  s = s.replace(/\s*[-–—]\s*[\d.]+(?:\([wWhHdD]\))?\s*[xX×]\s*[\d.]+(?:\([wWhHdD]\))?(?:\s*[xX×]\s*[\d.]+(?:\([wWhHdD]\))?)?\s*mm?\s*/g, '');
  // 5. Remaining embedded dims like " / 286 x 205mm"
  s = s.replace(/\s*[/,]\s*[\d.]+(?:\([wWhHdD]\))?\s*[xX×]\s*[\d.]+(?:\([wWhHdD]\))?\s*mm?.*/gi, '');
  // 6. Trailing standalone " 1000mm" or " (mm)"
  s = s.replace(/\s+\d+mm\s*$/, '');
  s = s.replace(/\s*\(\s*mm\s*\)\s*/g, '');
  // Cleanup
  s = s.replace(/\s{2,}/g, ' ').replace(/\s+\./g, '.').replace(/\s+,/g, ',').trim();
  s = s.charAt(0).toUpperCase() + s.slice(1);
  return s || desc.trim();
}
```

## Where to apply

| Location | What to use |
|---|---|
| `.htc-name` (tooltip title) | `cleanName(m.description \|\| tooltip.code)` |
| Sidebar material list description | `cleanName(mat.description \|\| '')` |
| Description field values in tooltip | `summarizeDescription(val)` if >80 chars |
| Schedule table (Schedule.tsx) | Full raw description — leave untouched |

## summarizeDescription()

For long field values (>80 chars), trim to first sentence or 100-char boundary with ellipsis:

```typescript
export function summarizeDescription(desc: string, maxLen = 100): string {
  const cleaned = cleanName(desc);
  if (cleaned.length <= maxLen) return cleaned;
  const truncated = cleaned.substring(0, maxLen);
  const lastSentence = truncated.lastIndexOf('.');
  const lastSpace = truncated.lastIndexOf(' ');
  const breakAt = lastSentence > maxLen * 0.6 ? lastSentence + 1 : (lastSpace > 10 ? lastSpace : maxLen);
  return cleaned.substring(0, breakAt).trim() + '…';
}
```

Both functions live in `src/lib/utils.ts`.
