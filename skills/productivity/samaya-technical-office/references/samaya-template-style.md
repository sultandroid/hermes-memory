# Samaya Report Template Style — SVG Chart Conventions

## Overview

All chart SVGs embedded in Samaya Technical Office reports must follow this style guide. This applies to EVM S-curves, payment bar charts, waterfall charts, and any other data visualization added to HTML reports.

## Template Fundamentals

- **Background:** White (`#FFF`) — never dark
- **Page:** A4 portrait (210mm × 297mm). SVG width ~174mm (650px), height variable
- **Font:** Calibri / Carlito / Arial, sans-serif
- **Text colors:** Titles `#1E293B`, body `#000`, secondary `#444`, metadata `#64748B`

## Samaya Tag Colors (from template CSS)

| Tag | Background | Border | Text | Use Case |
|-----|-----------|--------|------|----------|
| Green (g) | `#F0FDF4` | `#BBF7D0` | `#15803D` | Earned, Positive, Complete |
| Blue (b) | `#EFF6FF` | `#BFDBFE` | `#1D4ED8` | Paid, Active, In Progress |
| Amber (a) | `#FEF3C7` | `#FDE68A` | `#92400E` | Owed, Warning, Pending |
| Red (r) | `#FEF2F2` | `#FCA5A5` | `#B91C1C` | Behind, Negative, Billed-not-earned |
| Gray (n) | `#F1F5F9` | `#CBD5E1` | `#64748B` | Future, Not-started, Reference |

## Chart Structure

### Metric Cards Row
- 4-6 cards in a row at top of SVG
- Card: `rx="2"`, fill = tag background, stroke = tag border, `stroke-width="0.5"`
- Label: `font-size="5.5-6"`, `font-weight="700"`, text = tag text color, centered
- Value: `font-size="9-10"`, `font-weight="700"`, same tag text color, centered

### Chart Area
- Background: `#FAFAFA` (matches template's `tr:nth-child(even) td`)
- Border: `stroke="#CBD5E1"` `stroke-width="0.5"`
- Gridlines: `#E5E7EB`, 0.5px
- Y-axis labels: `#64748B`, `font-size="6"`
- X-axis labels: `#64748B`, `font-size="6.5"`
- Current month highlight: `#92400E`, font-weight="700"

### TODAY / Current-Period Marker
- Vertical dashed line: `stroke="#92400E"`, `stroke-dasharray="3,2"`, `stroke-width="1"`
- Label: `#92400E`, font-weight="700", placed above chart area

### Legend Box
- Background: `#FAFAFA`, stroke `#CBD5E1`
- Title: `#1E293B`, `font-weight="700"`
- Body text: `#000`
- Colored lines: use EVM curve colors (green, blue, amber)

### Assessment Box
- Yellow warning style matching `.note.warn`:
  - `fill="#FEF3C7"`, `stroke="#FDE68A"`, `rx="2"`
  - Title: `#92400E`, `font-weight="700"`
  - Body: `#000`, `font-size="7"`
- Bullet points start with `•`

### Table Header (within SVG)
- `fill="#1E293B"` rect with white text — matches template's `th{background:#1E293B;color:#FFF}`

### Footer
- Thin line: `stroke="#000"`, `stroke-width="0.5"`
- Text: `#64748B`, centered, `font-size="6.5"`

## Prohibited Elements
- ❌ Dark backgrounds (`#0F172A`, `#1E293B` as fill)
- ❌ Dark card bars (`#1E293B` as metric card fill)
- ❌ Light text on dark backgrounds
- ❌ Shadow/filter drop-shadow effects
- ❌ Glow effects or gradients spanning dark colors
- ❌ Landscape orientation
- ❌ Solid fills that don't match template palette

## Curve Colors (EVM-specific)
- PV (Planned): `#22C55E` green, stroke-width 2
- EV (Earned): `#3B82F6` blue, stroke-width 2, dasharray "4,2"
- EV forecast: `#3B82F6`, stroke-width 1, dasharray "2,2", opacity 0.5
- AC (Actual): `#F59E0B` amber, stroke-width 2
- Dots at current month: `circle r="3"` in curve color

## Coordinate Math
Y-axis formula: `y = 357 - (K_value * 0.3)`
- 0K → 357, 200K → 297, 400K → 237, 600K → 177, 800K → 117
