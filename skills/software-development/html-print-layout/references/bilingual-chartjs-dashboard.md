# Bilingual Chart.js Dashboard — Project Cost Reporting

## When to Use

Building an interactive bilingual (English/Arabic) HTML dashboard with Chart.js for construction project cost comparison (estimate vs actual). Best for personal or corporate project reporting where static tables aren't enough.

## Chart Types Used (8-chart layout)

| Chart | Type | Purpose |
|---|---|---|
| BOQ vs Actual | Grouped bar | Each category — estimate bar vs actual bar |
| Variance % | Horizontal bar | Over/under % — red over, green under |
| Plastering Per Floor | Grouped bar | Per-zone BOQ vs actual comparison |
| BOQ Allocation | Doughnut | Contract allocation across categories |
| Material vs Labor | Stacked bar | Cost type split per category |
| Bond Type | Doughnut | MST (labor) vs TWD (materials) vs SRF (cash) |
| Cumulative | Line x2 | Cumulative paid vs cumulative spend over time |
| Monthly Spend | Bar | Monthly spending with peaks highlighted |

## Bilingual Pattern — HTML

Every label has English + Arabic. Pattern:

```html
<h4>BOQ vs Actual / المقايسة مقابل الفعلي</h4>
<th>Category / البند</th>
```

## Bilingual Pattern — Chart.js

Chart labels use `\n` for line break:

```js
labels: ['Int. Plastering\nمحارة داخلية', 'Electrical\nكهرباء', ...]
```

## Curved Bar Styling

Key parameters for rounded/curved bars:

```js
{
  borderRadius: 8,
  barPercentage: 0.5,        // thinner bars = curves more visible
  categoryPercentage: 0.6,   // spacing between groups
  borderWidth: 1.5
}
```

For line charts (cumulative):

```js
{
  tension: 0.5,              // softer curves
  borderWidth: 3,
  borderJoinStyle: 'round',
  pointRadius: 6,
  pointBorderWidth: 2,
  pointBorderColor: '#fff'
}
```

## Animation

```js
animation: { duration: 1000, easing: 'easeOutQuart' }
```

## Color Palette for Cost Reports

```js
const C = {
  navy: '#1E293B',    // BOQ bars, headers
  gold: '#C8A84E',    // Actual bars, accents
  green: '#10B981',   // Under budget
  red: '#EF4444',     // Over budget
  blue: '#3B82F6',    // Plastering
  orange: '#F59E0B',  // Electrical
  purple: '#8B5CF6',  // Arch Mods
  pink: '#EC4899',    // Plumbing
  gray: '#94A3B8'     // Other
};
```

## Cumulative Chart Data Pattern

When showing cumulative paid vs cumulative spend over payment milestones:

```js
// Payment dates as x-axis labels
const pDt = ['22 Jul 25', '10 Apr 26', '21 May 26', '11 Jul 26'];
// Cumulative paid at each milestone
const cumP = [300000, 400000, 450000, 550000];
// Cumulative spend at same milestones
const cumS = [35000, 65000, 140000, 414585];
```

## Key Pitfalls

- **Chart.js datalabels plugin**: Must register with `Chart.register(ChartDataLabels)`. If labels overlap, set `display:false` per-dataset or use `datalabels: { display: false }` in plugins.
- **RTL in Chart.js**: Not natively supported for axis labels. Use `\n` line breaks for bilingual labels instead.
- **A4 print**: Set `@page { size: A4; margin: 18mm 16mm; }` and `-webkit-print-color-adjust: exact` on colored elements.
- **Mobile responsive**: Use `@media (max-width:900px)` to stack chart grid to single column.
- **Surge deploy**: Must deploy a directory with `index.html`, not a single file. `mkdir dir && cp report.html dir/index.html && surge dir/ domain.surge.sh`.
