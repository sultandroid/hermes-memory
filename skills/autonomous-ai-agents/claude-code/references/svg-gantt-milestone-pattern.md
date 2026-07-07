# SVG Gantt Chart — Milestone Symbol Pattern

For construction programme timelines with bilingual (Arabic/English) milestones.

## Coordinate System

Given a 52-week timeline spanning viewBox width `W`, with left margin `L` and right margin `R`:

- Chart width = `W - L - R` pixels
- Pixels-per-week = `(W - L - R) / 52`
- Pixel-per-day = `pixels-per-week / 7` (used for DMP day-based milestones)

Position a milestone at week `w`, day offset `d`:
```
x = L + (w - 1) * PX_PER_WEEK + d * PX_PER_DAY
```

Example (840×240 viewBox, L=25, R=25):
- PX_PER_WEEK = (840-25-25)/52 = 15.19
- PX_PER_DAY = 15.19/7 = 2.17
- G2 at week 5 (D35): x = 25 + 4*15.19 = 25 + 60.76 ≈ 86 (correct)
- But contract says D35 = day 35, which is exactly week 5 → 25 + 4*15.19 = 85.77

**Important**: DMP milestones are specified in "Days from LOA" (D0, D14, D35, D65, D82, D88). Convert days to weeks: `week = days / 7`, then use the formula above. When a milestone falls between week boundaries (e.g. D14 = week 2 exactly), use the precise fractional week.

## Symbol Differentiation

| Type | Symbol | Fill | Stroke | Use |
|------|--------|------|--------|-----|
| Gate review (G1–G5) | Diamond `<polygon>` | `#059669` (emerald) | `#047857` | Design/approval gates |
| Priority gap (P1–P3) | Circle `<circle>` | `#D97706` (amber) | `#92400E` | Critical-path gap closures |
| Generic milestone | Diamond `<polygon>` | `#FFFFFF` (white) | `#0F172A` | High-level phase markers |

### Diamond Geometry

4-point diamond, 8px × 8px centered on (cx, cy):
```
points="{cx-4},{cy-4} {cx},{cy} {cx+4},{cy+4} {cx-4},{cy+4}"
```
Wait — correct shape: 4 points forming a diamond. If center is at (cx, cy) with half-width=4 and half-height=4:
```
points="{cx},{cy-4} {cx+4},{cy} {cx},{cy+4} {cx-4},{cy}"
```
The order is top, right, bottom, left.

Apply `filter="url(#diamond-shadow)"` for subtle drop shadow.

### Circle Geometry

Radius 4px for P-milestones:
```
cx="{cx}" cy="{cy}" r="4"
```

## Bilingual Label Positioning

Labels appear in two rows below each symbol:
1. Arabic name (RTL, font-weight 600)
2. English name + "(Dnn)" (lighter, smaller font)

### Collision Avoidance

When two milestones share the same day position (e.g. G2 + P2 both at D35):
- One label offsets left (`text-anchor="end"`)
- Other offsets right (`text-anchor="start"`)
- Leave 10px minimum gap between label edges
- Use Arabic abbreviation for tight spaces: "غ.ف. أولوية N" instead of "إغلاق الفجوات أولوية N"

### Label Position Reference

```
G1 (D0, week 0-1):  centered — no neighbors
P1 (D14, week 2):   centered — no neighbors
G2 (D35, week 5):   left-anchored — P2 is 10px right
P2 (D35, week 5):   right-anchored
G3 (D65, week 9-10): left-anchored — P3 is 10px right
P3 (D65, week 9-10): right-anchored
G4 (D82, week 12):  centered
G5 (D88, week 13):  centered
```

## Leader Lines

Thin dashed lines connect from the generic milestone row to the DMP symbol row:
```svg
<line x1="{x}" y1="{generic_row_y}" x2="{x}" y2="{dmp_row_y}" 
      stroke="#0F172A" stroke-width="0.4" stroke-dasharray="1.5,1.5" stroke-opacity="0.15"/>
```

## Code Labels Above Symbols

Short identifiers (G1, P1, etc.) sit 2px above the symbol top:
```svg
<text x="{cx}" y="{cy-4}" text-anchor="middle" font-size="5" font-weight="700" fill="#059669">G1</text>
```
G-milestones use `#059669` (emerald), P-milestones use `#D97706` (amber).

## Legend Section

Add a second legend row below the phase-color legend for DMP milestones:

```svg
<rect x="25" y="{phase_legend_bottom + 3}" width="790" height="18" rx="2" 
      fill="#F1F5F9" stroke="#CBD5E1" stroke-width="0.4"/>
```

Lay out horizontally: G1 label, G2 label, G3 label, G4 label, G5 label on row 1; P1, P2, P3 on row 2. Use thin vertical dividers between groups.

Each entry has a mini symbol + "G# Arabic / English (Dnn)" text.

## ViewBox Adjustment

When adding a DMP milestone row between the generic milestones and phase bands, expand viewBox height by ~40px (symbols + leader space + bilingual labels). Shift all phase-band y-coordinates and grid lines down by ~20px.

Old pattern: generic milestones at y=30-40, phases start at y=41.
New pattern: generic at y=30-40, DMP symbols at y=44-60, phases start at y=61.

## Verification Checklist

After modification, verify:
1. All symbols are fully within the viewBox (no clipping)
2. Arabic and English labels do not overlap other elements
3. Phase band colors and labels preserved
4. Generic milestones (NTP, Design Freeze, etc.) still visible
5. Legend correctly references all added milestones
6. `count_diamonds + count_circles = expected milestone count`
7. Phase transition slants (overlapping polygons) remain intact
8. Grid lines extend to new phase-band Y positions
