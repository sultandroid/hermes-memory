# SVG Timeline Gantt Chart Pattern

Used for the Project Timeline page in Samaya HTML proposals. Renders a horizontal Gantt chart with 6 phases, 12-week axis, and 4-color legend.

## SVG Structure

```
viewBox="0 0 790 258"
├── Outer background rect (white, rx=10, drop-shadow)
├── Header gradient bar (dark #1F2430→#2D3548, title + total weeks)
├── Row striping (3 alternating #F8F9FB rows)
├── Left label panel (#FAFBFC, x=0 to ~196)
├── Phase bars (6 rects, rx=11, gradient fills, drop-shadow)
├── Week highlight column (red gradient at current week)
├── Week axis (W0–W12 labels)
└── Legend (4 color swatches at bottom)
```

## Phase Data (6 phases)

| # | Arabic | English | Duration | Color |
|---|--------|---------|----------|-------|
| 1 | التصميم واعتماد الرسومات | Design & Approvals | W1–W2 (2wk) | Gray `#6B7280` |
| 2 | التصنيع في المصنع | Steel Fabrication | W2–W6 (5wk) | Red `#B01E2F` |
| 3 | القواعد الخرسانية | Precast Footings | W3–W5 (3wk) | Amber `#D97706` |
| 4 | التركيب والكسوة والبانر | Steel Erection + Banner | W5–W9 (5wk) | Red `#B01E2F` |
| 5 | الإضاءة والكهرباء | LED + Electrical | W7–W10 (4wk) | Teal `#0D9488` |
| 6 | الفحص والتسليم النهائي | Inspection + Handover | W11 (1wk) | Gray `#6B7280` |

## Design Pattern

### Colors by Category
- **Preparation** (Design, Handover): Gray `#6B7280` with `#8B95A5` gradient
- **Steel Works** (Fabrication, Erection): Red `#B01E2F` with `#D12E40` gradient
- **Civil Works** (Footings): Amber `#D97706` with `#E8972E` gradient
- **Electrical** (LED + wiring): Teal `#0D9488` with `#14B8A6` gradient

### Week Axis Calculation
```
W0 = 196 (bar_start_x)
W0=196  W1=244  W2=292  W3=340  W4=388  W5=436
W6=484  W7=532  W8=580  W9=628  W10=676 W11=724
```
- Spacing per week: **48px**
- Grid lines: vertical lines at each week boundary
- Current week highlight: red gradient column (8% opacity) at W6

### Bar Properties
- Height: **22px**
- Border radius: **11px** (fully pill-shaped)
- Display duration label inside bar (e.g., "W1–W2 · 2wk")
- Use `<filter id="gs">` (feDropShadow) for subtle depth

### Gradient Definitions
Four `<linearGradient>` defs with pattern: luminance stop at 0% (lighter), base color at 100% (darker):
- `pg` (prep gray): #8B95A5 → #6B7280
- `eg` (exec red): #D12E40 → #B01E2F
- `cg` (civil amber): #E8972E → #D97706
- `lg` (light teal): #14B8A6 → #0D9488
- `hh` (week highlight): transparent → #B01E2F at 8% opacity

## Key UX Rules
- Arabic labels use `text-anchor="end"` with `direction="rtl"` and `unicode-bidi="embed"` — renders RTL from anchor point, preventing overflow
- **⚠️ CRITICAL:** Without these attributes, Arabic SVG text renders LTR and overflows past the viewBox left boundary
- English sub-labels below Arabic, same alignment
- Legend at y=244 with 7px squares and 7.5px labels, compact 4-item row
- Total SVG height: **258px** (fits within A4 with surrounding content)
