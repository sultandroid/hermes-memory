# Samaya Report Template — SVG Chart Style Reference

## Core Template CSS (from Aseer_NRS_Contract_Study.html)

```css
*{margin:0;padding:0;box-sizing:border-box}
html,body{background:#E5E7EB}
body{font-family:Calibri,Carlito,Arial,Helvetica,sans-serif;color:#000;font-size:9.75pt;line-height:1.32}
.sheet{width:210mm;min-height:297mm;margin:12mm auto;background:#FFF;padding:14mm 18mm;box-shadow:0 1px 6px rgba(0,0,0,0.08)}
@page{size:A4 portrait;margin:0}
.doc-strip{font-size:8.5pt;border-bottom:.6pt solid #000}
h2{font-size:10pt;font-weight:700;text-transform:uppercase;border-bottom:.6pt solid #000}
h3{font-size:9pt;font-weight:700;color:#1E293B}
th{background:#1E293B;color:#FFF;padding:0.5mm 0.8mm;font-size:6.5pt;text-transform:uppercase}
td{padding:0.4mm 0.8mm;border:.3pt solid #000;font-size:7pt}
tr:nth-child(even) td{background:#FAFAFA}
```

## Tag Classes (inline usage for SVG metric cards)

| Tag | Fill | Stroke | Text | Meaning |
|-----|------|--------|------|---------|
| Green | `#F0FDF4` | `#BBF7D0` | `#15803D` | Complete, Earned, Positive |
| Blue | `#EFF6FF` | `#BFDBFE` | `#1D4ED8` | Paid, Active, Submitted |
| Amber | `#FEF3C7` | `#FDE68A` | `#92400E` | Warning, Pending, Owed |
| Red | `#FEF2F2` | `#FCA5A5` | `#B91C1C` | Risk, Behind, Overdue |
| Gray | `#F1F5F9` | `#CBD5E1` | `#64748B` | Future, Not-started, Reference |

## Note Boxes

| Style | Background | Border-left color | Use |
|-------|-----------|-------------------|-----|
| `.note` (blue) | `#EFF6FF` | `#1D4ED8` 2.5pt | Information |
| `.note.warn` (amber) | `#FEF3C7` | `#92400E` 2.5pt | Warning |
| `.note.r` (red) | `#FEF2F2` | `#B91C1C` 2.5pt | Critical |

## External Factor Banner (SI007 style)

When a site instruction or external change order blocks milestone delivery:

- **Position:** Immediate top of SVG, below title/subtitle, above metric cards
- **Style:** Red alert box — `fill="#FEF2F2"` bg, `stroke="#FCA5A5"` 0.5px, 2px rounded
- **Height:** ~24px (includes 2 lines of text)
- **Content:** First line: bold title + explanation. Second line: specific impact.
- **Impact:** Shifts the chart area down by ~22px. Recalculate all Y-coordinates (see Y-axis formula for SI007 variant).

## SVG Chart Technical Specs

### Sizing (embedded in A4 portrait)
```
SVG width: 174mm  (650px viewBox)
SVG height: variable (245mm / 920px with table, 255mm / 960px for detailed tables, 265mm / 1000px with SI007 banner + detailed tables)
Position: inside <div class="sheet"> (A4 portrait 210mm × 297mm)
```

### Y-axis Coordinate Formula

**IMPORTANT: The scale is 0.25 px/K, NOT 0.3!** (A 240px range covering 960K = 0.25 px/K. Using 0.3 will produce wrong coordinates off by ~30px.)

**Standard chart (no SI007 banner, chart area starts at y=95):**
```
y = 357 - (value_in_K × 0.25)

Examples:
0K    → y=357
200K  → y=307
400K  → y=257
600K  → y=207
614K  → y=204 (round to 204; 357 - 153.5 = 203.5)
800K  → y=157
```

**With SI007 banner (chart area shifts down to y=117, origin moves to y=379):**
```
y = 379 - (value_in_K × 0.25)

Examples:
0K      → y=379
200K    → y=329
400K    → y=279
460K    → y=264 (DD-only EV; 379 - 115 = 264)
614K    → y=225 (PV at Jun; 379 - 153.5 = 225.5)
800K    → y=179
```
The SI007 banner adds 22px to the top spacer (y=95→y=117), and the 0-value line moves 22px down (y=357→y=379).

**Verification:** Given any coordinate y, the value in SAR should be (379 - y) × 4 for SI007-banner charts, or (357 - y) × 4 for standard charts. If rounding, the result must be within ±2K of the expected value.

### X-axis Monthly Positions (6 months, ~72px spacing)
```
Feb (x=100) → Mar (x=190) → Apr (x=280) → May (x=370) → Jun (x=460) → Jul (x=550) → Aug (x=640)
```

### EVM Curve Rules
- **PV** = solid `#22C55E` stroke 2px, with circle dot at current period
- **EV** = dashed `#3B82F6` stroke 2px `stroke-dasharray="4,2"`, circle dot at current period
- **EV forecast** = dotted `#3B82F6` stroke 1px `stroke-dasharray="2,2"` opacity 0.5
- **AC** = solid `#F59E0B` stroke 2px, circle dot at current period

### Arrows
- **SV arrow** (EV→PV): `#B91C1C`, `<polygon>` arrowhead, label "SV = -xxxK"
- **CV arrow** (EV→AC): `#15803D`, `<polygon>` arrowhead, label "CV = +xxxK"
