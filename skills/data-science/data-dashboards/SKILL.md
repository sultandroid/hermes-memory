---
name: data-dashboards
description: Build single-file interactive HTML dashboards with Chart.js — no build step, no server. Covers chart selection, print-ready A4 landscape styles, snapshot timestamps, Surge.sh deployment, and cron-based daily auto-update.
tags:
  - dashboard
  - chartjs
  - visualization
  - surge
  - cron
  - print
  - samaya
---

# Data Dashboards — Single-File Interactive HTML

Build self-contained interactive dashboards as a single HTML file. No build step, no server, no npm. Deploy to Surge.sh. Update daily via cron.

## When to Use

- User asks for a "live dashboard", "interactive report", or "online chart"
- You have tabular data (from registers, spreadsheets, databases) that needs visualisation
- The deliverable must be printable (A4) and carry a snapshot timestamp
- The data changes over time and needs daily auto-update

## Architecture

```
Single HTML file
├── <head>
│   ├── Chart.js CDN (v4)
│   ├── chartjs-plugin-datalabels (optional)
│   └── <style> — all CSS inline (screen + print)
├── <body>
│   ├── Sticky header (navy, gold accent)
│   ├── Snapshot timestamp (frozen at page load)
│   ├── KPI cards row
│   ├── Charts grid (2-col, full-width for single)
│   ├── Data tables
│   └── Footer
└── <script>
    ├── const DATA = { ... } — hardcoded data object
    └── Chart.js initialisation + table rendering
```

## Chart Selection Guide

| Data Shape | Chart Type | When |
|------------|-----------|------|
| Category totals | Bar | Comparing magnitudes across categories |
| Proportions | Doughnut | Showing code/status distribution |
| Stacked categories | Stacked bar | Category × sub-category (e.g. category × CG code) |
| Percentages | Horizontal bar | Approval rates, completion % |
| Time series | Horizontal bar | Days overdue, durations (indexAxis: 'y') |
| 2D matrix | Stacked bar | Heatmap alternative for small dimensions |

## Samaya Brand Tokens

```css
:root {
  --navy: #0F172A;
  --gold: #C9A84C;
  --red: #B91C1C;
  --red-bright: #EF4444;
  --orange: #F97316;
  --amber: #F59E0B;
  --green: #16A34A;
  --slate-50: #F8FAFC;
  --slate-100: #F1F5F9;
  --slate-200: #E2E8F0;
  --slate-400: #94A3B8;
  --slate-500: #64748B;
  --slate-700: #334155;
  --slate-800: #1E293B;
}
```

- **Font:** Inter (Google Fonts) — body text, headings
- **Header:** Navy `#0F172A` background, gold `#C9A84C` accent logo
- **Cards:** White, 1px slate-200 border, 12px border-radius, subtle shadow
- **Table headers:** Navy background, white uppercase text, 11px
- **Badges:** Rounded pills with semantic colours (blue=B, amber=C, red=D, purple=U)
- **No gradients, no drop shadows on content, no emoji**

## Print-Ready Styles (Mandatory)

Every dashboard MUST include a `@media print` block:

```css
@media print {
  @page {
    size: A4 landscape;
    margin: 12mm 10mm 10mm 10mm;
  }
  body {
    background: white;
    -webkit-print-color-adjust: exact;
    print-color-adjust: exact;
  }
  .header { position: static; box-shadow: none; }
  .kpi-card, .chart-card, .table-card {
    box-shadow: none;
    border: 1px solid #CBD5E1;
    border-radius: 4px;
  }
  .chart-wrap { page-break-inside: avoid; }
  thead th { background: #0F172A !important; color: white !important; }
  .badge { border: 1px solid transparent; }
  /* Reduce font sizes for print */
  .kpi-value { font-size: 24pt; }
  table { font-size: 8pt; }
  thead th { font-size: 7.5pt; padding: 6px 8px; }
}
```

## Snapshot Timestamp

The dashboard must display a frozen timestamp so printed copies are verifiable:

```html
<div class="snapshot-stamp">
  Snapshot taken: <strong id="snapStamp">—</strong>
</div>
```

```javascript
function fmtDateLong() {
  const d = new Date();
  return d.toLocaleDateString('en-GB', {
    weekday:'long', day:'numeric', month:'long', year:'numeric'
  }) + ' at ' + d.toLocaleTimeString('en-GB', {
    hour:'2-digit', minute:'2-digit', second:'2-digit'
  });
}
document.getElementById('snapStamp').textContent = fmtDateLong();
```

## Data Update Script + Cron

Create a Python script that:
1. Reads the source data (markdown register, Excel, JSON)
2. Replaces the `const DATA = { ... }` block in the HTML
3. Saves the updated HTML

```python
import re, json

def update_dashboard(register_path, dashboard_path):
    with open(register_path) as f:
        content = f.read()
    # Parse data from register
    data = { ... }
    # Serialise to JS
    data_js = json.dumps(data, indent=2)
    # Replace DATA block in HTML
    with open(dashboard_path) as f:
        html = f.read()
    html = re.sub(
        r'const DATA = \{[\s\S]*?\};',
        f'const DATA = {data_js};',
        html
    )
    with open(dashboard_path, 'w') as f:
        f.write(html)
```

Set up daily cron:

```bash
cronjob action=create \
  schedule="0 8 * * *" \
  name="dashboard-daily-update" \
  prompt="Run update script, copy to /tmp/, deploy to Surge.sh, report stats"
```

## Deployment

Deploy as a named HTML file to Surge.sh:

```bash
rm -rf /tmp/surge-deploy && mkdir -p /tmp/surge-deploy
cp dashboard.html /tmp/surge-deploy/dashboard.html
npx surge /tmp/surge-deploy/ my-domain.surge.sh
```

Access: `https://my-domain.surge.sh/dashboard.html`

## Pitfalls

- **Chart.js CDN required** — the HTML is not truly self-contained; it needs internet for Chart.js. For offline use, inline Chart.js from a local copy.
- **`print-color-adjust: exact` is mandatory** — without it, browsers strip background colours in print mode. Badges, severity indicators, and navy headers all go white-on-white.
- **Snapshot timestamp must be JS-generated at page load** — not a server-side date. The printed page is a permanent record; the timestamp proves when the data was current.
- **Data update script must use regex, not full HTML parser** — the DATA object is a JS const, not JSON. Use `re.sub()` with a pattern that matches `const DATA = {` through `};`.
- **Cron job must redeploy** — updating the HTML file locally is not enough. The cron prompt must include the Surge deploy step.
- **Surge CDN cold start** — first hit after deploy may return 504. Wait 10-30s and retry. Do not redeploy because of a 504.
- **KPI cards need semantic colours** — use inline `style="color:#..."` on the value element, not CSS classes. This survives print colour-adjust and makes the intent explicit.
