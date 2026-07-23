---
name: markdown-register-viewer
description: "Build interactive single-file HTML apps that parse markdown table data and render sortable, filterable, searchable dashboards with KPI cards, detail modals, and A4 print support. For project registers (lessons learned, risk, submittal, NCR, materials) stored as markdown tables."
triggers:
  - "build an HTML app / dashboard from a markdown table / register"
  - "lessons learned register / risk register / submittal register / NCR register viewer"
  - "interactive table with sorting, filtering, search from markdown data"
  - "KPI dashboard from tabular data"
  - "clickable table rows that open detail modals"
  - "print individual record as A4 PDF from a web app"
  - "self-contained single-file HTML data viewer"
  - "markdown table with emoji status indicators needs parsing"
  - "offline-capable data viewer with embedded fallback data"
tags:
  - "html"
  - "javascript"
  - "markdown"
  - "data-visualization"
  - "spa"
  - "print-layout"
  - "samaya"
related_skills:
  - "html-print-layout"
  - "samaya-doc-engine"
  - "web-data-extraction"
---

# Markdown Register Viewer

Build a complete single-file HTML app that reads a markdown table (like a project register), parses it, and renders an interactive dashboard with sorting, filtering, search, KPI cards, detail modals, and A4 print support.

This pattern is used for Aseer Museum project registers: Lessons Learned, Risk Register, Submittal Register, NCR Register, Materials Register — all stored as markdown tables in the repo.

## Architecture

```
Single HTML file
├── Embedded CSS (Samaya branding: #1E293B navy, #C9A84C gold, Calibri)
├── Embedded JS
│   ├── Data loading (fetch URL → fallback to embedded data)
│   ├── Markdown table parser (pipe-delimited, emoji status handling)
│   ├── Render engine (table rows, KPI cards, filter dropdowns)
│   ├── Sort handler (click column header → asc/desc toggle)
│   ├── Filter engine (category, status, plan, free-text search)
│   ├── Modal system (click row → detail view with all fields)
│   └── Print system (window.print() with @media print CSS)
└── Embedded fallback data (for offline / 404 scenarios)
```

## Step-by-Step Workflow

### 1. Understand the Source Table

Before writing any code, read the actual markdown file. Count the columns, note the header names, and identify:

- **Column order** (0-indexed after pipe-split)
- **Status column format** — emoji prefixes (🔴 Open, 🟡 In Progress, 🟢 Closed) or plain text
- **Multi-line cells** — some cells contain line breaks or long text
- **Empty/missing cells** — marked as `—` or empty

### 2. Build the Parser

```javascript
function parseLessons(markdown) {
  const lines = markdown.split('\n');
  const lessons = [];
  let inTable = false;

  for (const line of lines) {
    const trimmed = line.trim();

    // Detect table start by matching the header row
    if (trimmed.includes('LL ID') && trimmed.startsWith('|')) {
      inTable = true;
      continue;
    }

    // Skip separator rows (|---|)
    if (/^\|[\s\-:]+\|/.test(trimmed)) continue;
    if (!inTable) continue;
    if (!trimmed.startsWith('|')) continue;

    const cols = trimmed.split('|').map(c => c.trim()).filter(c => c !== '');
    if (cols.length < 10) continue;

    const num = parseInt(cols[0], 10);
    if (isNaN(num)) continue;

    // Map columns by position — verify against actual header
    lessons.push({
      num, id: cols[1], dateCaptured: cols[2], sourceEvent: cols[3],
      category: cols[4], rootCause: cols[5], impact: cols[6],
      correctiveAction: cols[7], preventiveAction: cols[8],
      owner: cols[9], status: parseStatus(cols[10]),
      governingPlan: cols[11], linkedRisk: cols[12]
    });
  }
  return lessons;
}
```

### 3. Handle Emoji Status Parsing

The status column may contain emoji prefixes. Map them to clean text values:

```javascript
const STATUS_MAP = { '🔴': 'Open', '🟡': 'In Progress', '🟢': 'Closed' };

function parseStatus(raw) {
  for (const [emoji, label] of Object.entries(STATUS_MAP)) {
    if (raw.includes(emoji)) return label;
  }
  return raw; // fallback to raw text
}
```

### 4. Data Loading with Fallback

Always try the live URL first, then fall back to embedded data:

```javascript
async function loadData() {
  let markdown = null;

  // Try GitHub raw URL
  try {
    const resp = await fetch(DATA_URL);
    if (resp.ok) markdown = await resp.text();
  } catch (e) { /* fall through */ }

  // Try local file:// path (may fail in some browsers)
  if (!markdown) {
    try {
      const resp = await fetch('file://' + LOCAL_PATH);
      if (resp.ok) markdown = await resp.text();
    } catch (e) { /* fall through */ }
  }

  // Last resort: embedded data
  if (!markdown) markdown = getEmbeddedData();

  if (!markdown) { showError(); return; }

  allLessons = parseLessons(markdown);
  if (allLessons.length === 0) { showError('No lessons parsed'); return; }

  populateFilterOptions();
  applyFilters();
}
```

### 5. Interactive Features

| Feature | Implementation |
|---------|---------------|
| **Sort** | Click column header → toggle asc/desc. Store `currentSort = { col, dir }`. Re-sort filtered data before render. |
| **Filter** | `<select>` per dimension (category, status, plan). `Array.filter()` on allLessons. |
| **Search** | `<input>` with `oninput`. Concatenate all fields into a haystack, check `includes(query)`. |
| **KPI Cards** | Count filtered lessons by status. Update on every filter change. |
| **Detail Modal** | Click row → find lesson by num → populate all fields in modal DOM. |
| **Print** | `window.print()` with `@media print` CSS. Add `.print-mode` class to modal for full-page print. |

### 6. A4 Print Support

Add `@media print` CSS that:

- Hides the header, KPI bar, filter bar, table, and footer
- Shows only the modal content as a full A4 page
- Uses `@page { size: A4 portrait; margin: 15mm 18mm; }`
- Sets `-webkit-print-color-adjust: exact` on colored elements
- Adds a fixed confidentiality footer at page bottom

```css
@media print {
  .app-header, .kpi-bar, .filter-bar, .table-wrap, .app-footer { display: none; }

  .modal-overlay.print-mode {
    display: block !important;
    position: static !important;
    background: none !important;
  }

  @page { size: A4 portrait; margin: 15mm 18mm; }

  .print-footer {
    position: fixed;
    bottom: 0;
    text-align: center;
    font-size: 8pt;
    color: #94a3b8;
    border-top: 1px solid #cbd5e1;
    padding-top: 6px;
  }
}
```

### 7. Samaya Branding

- **Header**: Navy `#1E293B` background, Gold `#C9A84C` accent, SVG logo
- **Font**: Calibri (body 0.88rem, headings 1.4rem, tables 0.8rem)
- **Table**: Navy header row, white rows, light gray `#f1f5f9` hover
- **Status badges**: Red (Open), Yellow (In Progress), Green (Closed) — rounded pills
- **Category badges**: Gray `#e2e8f0` background, dark text
- **Plan badges**: Blue `#dbeafe` background

## Pitfalls

### Column Count Mismatch
The markdown table may have trailing empty cells that get dropped by `.filter(c => c !== '')`. Always check the actual column count against your parser. If a row has fewer columns than expected, the last columns will be missing — add default values.

### Emoji in Status
The status column may contain emoji (🔴🟡🟢) that need stripping before comparison. Always parse emoji → text before filtering or displaying.

### Multi-line Cells
Some cells contain line breaks or long text. The pipe-delimited parser handles this if the markdown is well-formed (no pipes inside cells). If cells contain pipes, the parser breaks — use a more robust approach (count pipes, or pre-process the markdown).

### 404 on Data URL
The GitHub raw URL may return 404 if the repo is private. Always include embedded fallback data. The fallback should be a complete copy of the markdown table, not a stub.

### file:// Fetch Limitations
Some browsers block `fetch('file://...')` for security reasons. The fallback to embedded data handles this, but the local file path should still be tried first.

### Sort Stability
JavaScript's `Array.sort()` is stable in modern engines but the comparison function must return 0 for equal values to preserve original order. Always handle the equality case.

### Missing `$` Helper (document.querySelector shorthand)
If the JS code uses `$('#kpis')`, `$('#tbody')`, etc. but never defines `const $ = s => document.querySelector(s)`, every rendering function silently fails. The page loads with empty KPI cards, no table rows, and no console errors (the exception is caught generically). **Always verify the `$` helper is defined before `init()` is called.** Add it right before `function init()`:

```javascript
const $ = s => document.querySelector(s);
```

### Variable Name Mismatch (case-sensitive)
If the data array is declared as `const LESSONS = [...]` (uppercase) but all functions reference `lessons` (lowercase), every filter, render, and KPI function operates on `undefined`. The page appears structurally complete but shows zero data. **Always verify the variable name used in functions matches the declaration.** Use a single grep to check: `grep -n 'lessons\\.\\|lessons\\.length\\|lessons\\.filter\\|lessons\\.find\\|lessons\\.forEach\\|lessons\\.some'` — if the declaration is `LESSONS`, every reference must be `LESSONS` too. The safest approach: declare as `const DATA = [...]` and reference `DATA` everywhere, avoiding case confusion entirely.

### Modal Scroll Position
When opening a modal on a long page, the body scroll position is preserved. Set `document.body.style.overflow = 'hidden'` when modal is open, restore on close.

### Print Mode State
The `.print-mode` class must be added before `window.print()` and removed after. The print dialog is synchronous in most browsers, but the class removal should happen in a `setTimeout` or after print completes (use `window.onafterprint` event).

## Hardcoded-Data Dashboards (No Markdown Parsing)

Not all dashboards need markdown parsing. When the data is static (known at build time), embed it directly as a JS object. This is simpler and avoids parser bugs.

### Pattern

```javascript
const DATA = {
  total: 217,
  categories: {
    "Pre-Qual":    { total:101, B:67, C:22, D:11, U:1,  F:0 },
    "Documents":   { total:76,  B:49, C:15, D:3,  U:6,  F:3 },
    // ...
  },
  deemedApproved: [
    { ref:"IFC-0003", subject:"Flooring", days:92, risk:"HIGH" },
    // ...
  ],
  ifc: [
    { pkg:"IFC-0003", subject:"Flooring", submitted:"22-Apr", code:"DA", days:92, status:"Deemed Approved" },
    // ...
  ],
  hse: [
    { ref:"PL-0041", plan:"Emergency Response / Preparedness", code:"B", status:"Approved" },
    // ...
  ],
  overdue: [
    { ref:"—", subject:"HVAC Complete Submittal Package", submitted:"02-Jul", days:21, risk:"HIGH", status:"DA" },
    // ...
  ]
};
```

### When to use hardcoded vs parsed

| Situation | Approach |
|-----------|----------|
| Data changes daily, source is markdown in repo | Parse from markdown |
| Data is stable, or source is a PDF/email/Excel | Hardcode in JS |
| Dashboard needs auto-update via cron | Parse from markdown + rebuild script |
| One-off report / snapshot | Hardcode in JS |

### Chart.js Integration

For interactive charts, load Chart.js from CDN and create charts in `window.onload` or at the bottom of the `<script>` block:

```html
<script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.7/dist/chart.umd.min.js"></script>
```

**Chart types commonly used in project dashboards:**

| Chart Type | Use Case | Example |
|------------|----------|---------|
| `bar` | Category totals, approval rates | Submittals per category |
| `doughnut` | Code/status distribution | B vs C vs D vs U |
| `bar` (stacked) | Multi-dimension breakdown | Category × Code heatmap |
| `bar` (horizontal, `indexAxis: 'y'`) | Timelines, ranked data | Deemed approval days, approval rates |
| `line` | Trends over time | Submission rate per week |

**Key Chart.js options for dashboards:**

```javascript
options: {
  responsive: true,
  maintainAspectRatio: false,  // let CSS control height
  plugins: {
    legend: { position: 'bottom', labels: { usePointStyle: true, font: { size: 11 } } },
    tooltip: { backgroundColor: '#0F172A' }
  },
  scales: {
    y: { beginAtZero: true, grid: { color: '#E2E8F0' } },
    x: { grid: { display: false } }
  }
}
```

**Doughnut with percentage in tooltip:**
```javascript
tooltip: {
  callbacks: {
    label: ctx => ctx.label + ': ' + ctx.parsed + ' (' + (ctx.parsed / DATA.total * 100).toFixed(1) + '%)'
  }
}
```

**Horizontal bar for timelines:**
```javascript
options: {
  indexAxis: 'y',  // horizontal bars
  scales: {
    x: { beginAtZero: true },
    y: { grid: { display: false } }
  }
}
```

### Snapshot Timestamp (Frozen at Page Load)

Every dashboard should display a snapshot timestamp that freezes at page load, so printed copies are traceable:

```html
<div class="snapshot-stamp">
  Snapshot taken: <strong id="snapStamp">—</strong>
</div>
```

```javascript
function fmtDateLong() {
  const d = new Date();
  return d.toLocaleDateString('en-GB', { weekday:'long', day:'numeric', month:'long', year:'numeric' }) +
    ' at ' + d.toLocaleTimeString('en-GB', { hour:'2-digit', minute:'2-digit', second:'2-digit' });
}
document.getElementById('snapStamp').textContent = fmtDateLong();
```

### Print Button with SVG Icon

Add a print button in the header bar:

```html
<button class="print-btn" onclick="window.print()">
  <svg viewBox="0 0 24 24"><path d="M19 8h-1V3H6v5H5c-1.66 0-3 1.34-3 3v6h4v4h12v-4h4v-6c0-1.66-1.34-3-3-3zM8 5h8v3H8V5zm8 14H8v-4h8v4zm2-4v-2H6v2H4v-4c0-.55.45-1 1-1h14c.55 0 1 .45 1 1v4h-2z"/></svg>
  Print
</button>
```

```css
.print-btn {
  background: rgba(255,255,255,0.15);
  border: 1px solid rgba(255,255,255,0.3);
  color: white;
  padding: 6px 16px;
  border-radius: 20px;
  font-size: 12px;
  font-weight: 500;
  cursor: pointer;
  font-family: inherit;
  display: inline-flex;
  align-items: center;
  gap: 6px;
}
.print-btn:hover { background: rgba(255,255,255,0.25); }
.print-btn svg { width: 14px; height: 14px; fill: currentColor; }

@media print {
  .print-btn { display: none; }
}
```

### A4 Landscape Print Styles for Dashboards

Dashboards with wide tables and charts benefit from A4 landscape orientation:

```css
@media print {
  @page { size: A4 landscape; margin: 12mm 10mm; }
  body { background: white; font-size: 9pt; -webkit-print-color-adjust: exact; print-color-adjust: exact; }
  .header { position: static; box-shadow: none; }
  .kpi-card, .chart-card, .table-card { box-shadow: none; border: 1px solid #CBD5E1; }
  .chart-wrap { max-height: 260px; page-break-inside: avoid; }
  .table-card { page-break-inside: avoid; }
  thead th { background: #0F172A !important; color: white !important; }
  .badge { -webkit-print-color-adjust: exact; print-color-adjust: exact; }
  .kpi-value { font-size: 24pt; }
  table { font-size: 8pt; }
  thead th { font-size: 7.5pt; padding: 6px 8px; }
  tbody td { padding: 5px 8px; }
}
```

### Auto-Update via Cron + Rebuild Script

When the dashboard data changes over time, wire a daily cron that rebuilds the HTML and redeploys:

**Rebuild script** (`scripts/update_dashboard.py`):
```python
import re, json
# 1. Parse source data (markdown register, JSON, etc.)
# 2. Read the HTML template
# 3. Replace the DATA object in the HTML
# 4. Write updated HTML
```

**Cron job:**
```bash
cronjob action=create name="dashboard-daily-update" schedule="0 8 * * *" \
  prompt="Run update script, copy to /tmp/, deploy to Surge.sh"
```

**Deploy step in cron:**
```bash
cp dashboard.html /tmp/deploy-dir/index.html
cd /tmp/deploy-dir && surge --domain my-domain.surge.sh ./
```

### Cache Issues After Deploy

When a user reports the print button or other feature "not working" after deploy, the most likely cause is **browser cache** — Surge.sh CDN caches aggressively. Steps:

1. **Hard refresh** — Cmd+Shift+R (or Ctrl+F5)
2. **Incognito/private window** — bypasses all cache
3. **Verify deployed file** — check the live URL directly:
   ```bash
   curl -s https://domain.surge.sh | grep -c 'print-btn'
   ```
4. If the file is correct on server but user still sees old version, wait 30s for CDN propagation, then hard refresh again

## Verification

1. Open the HTML file in a browser — it should load and display data immediately
2. Check KPI counts match the register's status summary section
3. Click each column header — sort should toggle asc/desc with arrow indicator
4. Filter by each dimension — dropdowns should populate from actual data
5. Search for a term that appears in one lesson — only that row should show
6. Click a row — modal should open with all fields populated
7. Click "Print as PDF" — print dialog should show A4-formatted single page
8. Resize browser to mobile width — layout should adapt (stacked filters, bottom-sheet modal)
9. Disconnect network and reload — embedded fallback data should load
