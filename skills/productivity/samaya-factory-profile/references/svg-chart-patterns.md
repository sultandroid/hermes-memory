# SVG Chart Patterns — Page 4 Operational Capacity

## Brand palette (CSS variables)
- Navy: `var(--v3-ink)` — primary data, current state
- Gold deep: `var(--v3-gold-deep)` — targets, growth, highlights
- Gold: `var(--v3-gold)` — secondary accent
- Gold pale: `var(--v3-gold-pale)` — subtle fills
- Ink soft: `var(--v3-ink-soft)` — secondary text, muted data
- Ink mute: `var(--v3-ink-mute)` — tertiary text, grid lines
- Paper: `var(--v3-paper)` (#F6F0E4) — track background

## SVG template
```svg
<svg class="v4-cap-chart" viewBox="0 0 180 N" fill="none">
  <!-- content -->
</svg>
```
- viewBox width: **180 minimum** (140 caused overflow)
- Use `style="fill: var(--v3-ink)"` not `fill="var(--v3-ink)"` — CSS variables need the style attribute in inline SVG
- `text-anchor="end"` for Arabic labels (RTL)

## Abstract icons per stat

### 1. Building/factory (8,000m² — Current Facility)
```
3 stacked rectangles + base line
Represents: factory building blocks
```

### 2. Compass/target (53,000m² — Expansion)
```
Concentric circles with crosshair lines at cardinal points
Represents: target, masterplan, future vision
```

### 3. Gear/cog (217 — Machines & Equipment)
```
Circle with 4 radial tooth paths + crosshair spokes
Represents: machinery, production, mechanical
```

### 4. Diamond (25y — Experience)
```
Two stacked opposing triangles (Najdi seal shape)
Represents: milestone, heritage, achievement
```

## Text sizing
- Data values (numbers): 9px Cormorant Garamond, bold
- Labels (حالي/مخطط): 5px Inter, uppercase, letter-spaced
- Badge (6.6×): 6.5px Cormorant Garamond
- Legend items: 5px Inter
- Timeline years: 6px Inter bold
- Timeline Arabic labels: 5px Inter

## Charts

### Comparison bar (Stat 1)
```
حالي [████░░░░░░░░░░░░░░░] 8,000
مخطط [████████████████████] 53,000
              [6.6×]
```

### Full bar (Stat 2)
```
          | ← اليوم 8,000 reference
[██████████████████████████████]
MASTERPLAN 53,000m²        6.6×
```

### Stacked bar (Stat 3)
```
[████████████████░░░░░░░░░░░░░░░░]
 CNC 42 | Panel 18 | Edge 12 | Finish 8 | Other 137
```

### Timeline (Stat 4)
```
 ●─────────●─────────●─────────●
1999     2005      2012      2024
تأسست    توسعة     عالمي     مخطط
```
