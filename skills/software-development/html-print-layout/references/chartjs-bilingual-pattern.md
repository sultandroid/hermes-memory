# Bilingual Chart.js Dashboard Pattern

## When to use
Building estimate-vs-actual cost comparison dashboards with Chart.js that need Arabic/English labels for personal or Samaya projects.

## Data structure pattern
```js
const catData = [
  { n:'Int. Plastering\nمحارة داخلية', c:'#3B82F6', e:330930, a:171525, m:93400, l:78125, ar:'محارة' },
  // e = BOQ estimate, a = actual, m = materials, l = labor
];
```

## Chart label convention
- Chart title: `<h4>ENGLISH / العربية</h4>`
- Dataset labels: `'BOQ / المقايسة'`, `'Actual / الفعلي'`
- Axis labels: every label has `English\nالعربية` via `\n` in the string
- Table headers: `<th>ENGLISH<span class="ar">العربية</span></th>`

## Curved chart styling (user preference)
- Bar charts: `borderRadius: 8, barPercentage: 0.5, categoryPercentage: 0.6`
- Line charts: `tension: 0.5` for smooth curves, `pointRadius: 6, pointBorderWidth: 2, pointBorderColor: '#fff'`
- Doughnut: `borderRadius: 4` on dataset for rounded segment ends
- Animation: `animation: { duration: 1000, easing: 'easeOutQuart' }`

## Pitfalls
- **Do NOT auto-apply Samaya branding** (logo header, "SAMAYA CONFIDENTIAL" footer) unless user explicitly confirms it's a Samaya corporate document. Personal projects get generic "CONFIDENTIAL" only. When in doubt, omit branding.
- **Verify no CJK/foreign characters leak** into Arabic text. Grep `[\u4e00-\u9fff]` on all generated Arabic strings before delivery. A single mixed-script character like 绝大部分 in Arabic text will be rejected.
- Arabic labels in Chart.js use `\n` not `<br>` inside string literals.
- Bar charts need `maintainAspectRatio: false` with explicit height container for responsive layouts.
- When deploying to Surge, use a directory with `index.html`, not a single file — Surge expects a directory.
