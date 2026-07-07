# Stacked SVG Area Chart — Headcount Loading Curve

## Use Case

Visualize headcount ramp-up/phase-down across project phases with stacked tiers. Used in Resource Management Plan Section 5.1.

## Pattern

SVG `viewBox="0 0 600 260"` with:
- Stacked area layers (3 tiers), each with semi-transparent fill
- Top outline stroke showing total
- Data callouts with circles + leader lines at key points
- Color legend in top-right corner
- Gate markers (G2, G3, G5 AFC) as vertical dashed lines
- Axis labels and grid lines

## Stacking Strategy

Draw bottom-to-top so each layer sits on top of the previous:

```
Bottom layer (Tier 3):  y-coords based on tier-3-only headcount
Middle layer (Tier 2):  y-coords based on tier-3 + tier-2 combined
Top layer (Tier 1):     y-coords based on total = tier-3 + tier-2 + tier-1
Top outline stroke:     follow the top layer path
```

Formula: `Y = 185 - (cumulative_headcount * 3)` where 185 = Y-axis origin and 3 = pixels per person.

## Color Scheme

- Tier 1 (Management): `#0F172A` at 0.3 opacity
- Tier 2 (Specialists): `#0284C7` at 0.4 opacity  
- Tier 3 (Support): `#64748B` at 0.5 opacity
- Peak marker: `#F59E0B` (gold dot)
- Outline stroke: `#0F172A` at 2px

## Data Points (Aseer Museum)

| Phase | Day | T1 | T2 | T3 | Total |
|---|---|---|---|---|---|
| P1 Pre-LOA | D-14 | 2 | 1 | 1 | ~4 |
| P2 Kick-off | D0 | 3 | 3 | 2 | ~8 |
| P2 Active | D14 | 4 | 5 | 3 | ~12 |
| P3 Mid | D35 | 5 | 10 | 7 | ~22 |
| P3 Peak | D65 | 6 | 19 | 13 | ~38 |
| P3→P4 | D88 | 5 | 12 | 8 | ~25 |
| P4 Mid | D180 | 5 | 14 | 9 | ~28 |
| P4 Late | D270 | 4 | 8 | 5 | ~17 |
| P5 Demob | D300 | 2 | 3 | 3 | ~8 |

## Callout Annotations

Each callout = `<circle>` at data point + `<text>` label offset above:

```svg
<circle cx="310" cy="65" r="4" fill="#F59E0B" stroke="#FFFFFF" stroke-width="1.5"/>
<text x="310" y="53" font-family="Inter,sans-serif" font-size="9" font-weight="700" text-anchor="middle" fill="#92400E">Peak ~38</text>
```

## Legend Box

Top-right corner, semi-transparent white background:

```svg
<rect x="410" y="10" width="175" height="65" rx="3" fill="#FFFFFF" fill-opacity="0.9" stroke="#E2E8F0" stroke-width="0.5"/>
<rect x="418" y="18" width="10" height="10" fill="#0F172A" fill-opacity="0.4"/>
<text x="433" y="27" font-family="Inter,sans-serif" font-size="7" fill="#64748B">Tier 1 Management</text>
<rect x="418" y="32" width="10" height="10" fill="#0284C7" fill-opacity="0.5"/>
<text x="433" y="41" font-family="Inter,sans-serif" font-size="7" fill="#64748B">Tier 2 Specialists</text>
<rect x="418" y="46" width="10" height="10" fill="#64748B" fill-opacity="0.5"/>
<text x="433" y="55" font-family="Inter,sans-serif" font-size="7" fill="#64748B">Tier 3 Support</text>
```

## Gate Markers

Vertical dashed lines at key milestones:

```svg
<line x1="220" y1="185" x2="220" y2="25" stroke="#64748B" stroke-width="0.5" stroke-dasharray="3 2"/>
<text x="220" y="18" font-family="Inter,sans-serif" font-size="7" text-anchor="middle" fill="#64748B" font-weight="700">G2</text>
```

## Axes

Y-axis: 0 to 40 with 10-unit grid lines. X-axis: D-14 to D300 with 8 tick marks. Always label "Headcount" on Y and "Day" on X.

## Delegation to Claude

When delegating SVG chart creation to Claude, pass:
- Exact data table (the 9-row table above)
- Color hex values
- ViewBox dimensions
- Callout text for each key point
- A reference to an existing SVG in the file as template