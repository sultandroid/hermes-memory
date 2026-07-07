# SVG Chart Components Reference

## Process Flow (6 steps, 680×120)
```svg
<svg viewBox="0 0 680 120" xmlns="http://www.w3.org/2000/svg" style="width:100%;height:auto;max-width:100%;display:block;font-family:'Inter','Cairo',sans-serif">
  <defs>
    <marker id="arr" markerWidth="8" markerHeight="5" refX="8" refY="2.5" orient="auto"><polygon points="0 0, 8 2.5, 0 5" fill="#0F172A"/></marker>
    <marker id="arr_r" markerWidth="8" markerHeight="5" refX="8" refY="2.5" orient="auto"><polygon points="0 0, 8 2.5, 0 5" fill="#991B1B"/></marker>
  </defs>
  <!-- Steps 1-6 with forward arrows -->
  <rect x="5" y="10" width="95" height="28" rx="3" fill="#0F172A"/>
  <text x="52" y="23" text-anchor="middle" font-size="5.5" font-weight="700" fill="#fff">Step 1</text>
  <text x="52" y="33" text-anchor="middle" font-size="4.2" fill="#94A3B8">ترجمة</text>
  <line x1="102" y1="24" x2="114" y2="24" stroke="#0F172A" stroke-width="1" marker-end="url(#arr)"/>
  <!-- ... repeat with 95px boxes at x=5,117,229,341,453,565 -->
  <!-- Last box uses #065F46 fill -->
  <!-- Dashed feedback from last back to first -->
</svg>
```

## Workforce Curve (680×130)
- 12 month positions: 65, 115, 165, 215, 265, 315, 365, 415, 465, 515, 565, 615
- Y = 130 - (value/127 * 116) for peak 127 scale
- Gradient fill under curve, quadratic bezier path, peak circle r=4-5

## Org Chart (680×250)
- Client (#0F172A) → PD → PM/DM/CM (#1E40AF) → subs (#64748B) → Tier3 (#92400E)
- Legend box right side with color swatches

## Interface Matrix (680×145)
- 7 cols × 6 rows, 78px per column, 16px per row
- Mechanisms: W=blue, M=green, R/A=red, D=slate, C=light

## Gantt Chart (680×240)
- 9px/week, 52 weeks, 7 phase bars, milestone diamonds, dependency arrows

## TOC Grid
```css
display:grid;grid-template-columns:35px 1fr 45px;gap:0;font-size:0.32rem;direction:rtl
```
