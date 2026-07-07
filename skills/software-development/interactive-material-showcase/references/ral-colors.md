# RAL Color Swatches in Tooltip Cards

Used in `renderColorSwatch()` in Gallery.tsx to show a small colored dot next to field values containing RAL codes like "RAL 7015".

## Implementation

```typescript
const RAL_COLORS: Record<string, string> = {
  '7015':'#434B4D','7016':'#293133','7021':'#2F3538','7035':'#C5C7C4','7038':'#B0B5B1',
  '7030':'#939388','7042':'#8D9292','7040':'#9DA1A2','9003':'#F4F4F4','9005':'#0A0A0A',
  '9010':'#F7F9F8','5005':'#00538A','2002':'#BF392C','1003':'#F9A800','3000':'#AF2B1E',
  '6002':'#2D6B2A','6005':'#104410','8004':'#8D4E2A','8017':'#45322E','8014':'#4A3A2B',
  '3020':'#CC3A2B','5018':'#048E8C','5021':'#00777B','1015':'#E6D2B5','1013':'#E3D9C6',
  '1014':'#E1CC9C','6018':'#5D9B3A','1000':'#C9B87C','7001':'#8F9698','7004':'#9DA1A3',
};

function renderColorSwatch(val: string): React.ReactNode {
  const m = val.match(/\bRAL\s*(\d{4})\b/i);
  if (!m) return null;
  const hex = RAL_COLORS[m[1]];
  if (!hex) return null;
  return <span style={{display:'inline-block',width:14,height:14,borderRadius:3,
    background:hex,marginLeft:6,verticalAlign:'middle',
    border:'1px solid rgba(255,255,255,.15)',flexShrink:0}} 
    title={`RAL ${m[1]} (${hex})`} />;
}
```

The regex `/\bRAL\s*(\d{4})\b/i` matches:
- `\b` word boundary
- `RAL` literal (case-insensitive due to `/i`)
- `\s*` optional whitespace
- `(\d{4})` capture group: exactly 4 digits  
- `\b` word boundary

The swatch is a 14×14px colored square with rounded corners (3px radius), placed inline after the value text in the `fval` span:

```tsx
<span className={`fval${f.mono ? ' mono' : ''}`}>
  {String(mat[f.key])}{renderColorSwatch(String(mat[f.key]))}
</span>
```

## Add Missing RAL Colors

When a RAL number appears in the data but has no swatch, add it to the `RAL_COLORS` object. Find the HEX value from:
- https://www.ralcolor.com/
- Project lighting/luminaire specification documents
- The `Treatment/Finish` or `Colour` fields in finishes_schedule data
