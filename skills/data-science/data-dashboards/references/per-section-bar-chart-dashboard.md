# Per-Section Bar Chart Dashboard Pattern

Build a visual status dashboard where each section (specialist, discipline, category) gets its own card with horizontal bar charts showing status breakdown. Useful for project submission trackers, risk registers, or any multi-category status view.

## When to Use

- You have a markdown tracker with N sections, each containing items with status codes
- User wants a "visual status" overview — not just numbers, but bars per section
- The data is static enough to hardcode as JS (updated via script, not live API)

## Architecture

```
Single HTML file
├── KPI row (6 cards: Total, Approved, Revise, Rejected, Under Review, Pending)
├── Legend (coloured dots for each status)
├── Section cards grid (auto-fill, min 420px)
│   └── Each card:
│       ├── Section title + item count badge
│       └── 6 horizontal bar rows (one per status)
│           ├── Label (80px fixed)
│           ├── Track (flex:1) with coloured fill
│           └── Number (30px right-aligned)
└── Overall donut chart (Chart.js)
```

## Data Format

```javascript
const SECTIONS = [
  {name:"1. Architecture", total:11, approved:6, revise:3, rejected:0, review:2, submitted:0, pending:0},
  // ... one per section
];
```

## CSS Bar Chart (No Chart.js dependency for section cards)

```css
.bar-row {
  display: flex; align-items: center; gap: 8px;
  margin-bottom: 6px;
}
.bar-label {
  font-size: 11px; font-weight: 500; color: var(--slate-500);
  width: 80px; flex-shrink: 0;
}
.bar-track {
  flex: 1; height: 20px; background: var(--slate-100);
  border-radius: 10px; overflow: hidden;
}
.bar-fill {
  height: 100%; border-radius: 10px;
  display: flex; align-items: center; justify-content: flex-end;
  padding-right: 6px;
  font-size: 10px; font-weight: 600; color: white;
  min-width: 24px;
}
.bar-fill.approved { background: #16A34A; }
.bar-fill.revise   { background: #D97706; }
.bar-fill.rejected { background: #DC2626; }
.bar-fill.review   { background: #2563EB; }
.bar-fill.pending  { background: #6B7280; }
.bar-fill.submitted { background: #7C3AED; }
.bar-num {
  font-size: 12px; font-weight: 600; color: var(--slate-600);
  width: 30px; text-align: right;
}
```

## HTML Template Per Card

```javascript
SECTIONS.forEach(s => {
  const max = s.total || 1;
  card.innerHTML = `
    <div class="section-title">${s.name} <span class="count">${s.total} items</span></div>
    <div class="bar-row">
      <span class="bar-label">Approved</span>
      <div class="bar-track"><div class="bar-fill approved" style="width:${s.approved/max*100}%">${s.approved||''}</div></div>
      <span class="bar-num">${s.approved}</span>
    </div>
    <!-- repeat for revise, rejected, review, submitted, pending -->
  `;
});
```

## Data Source: Markdown Tracker

Parse a markdown file with sections like `## N. Section Name` and table rows with status codes in the 5th column:

```python
import re
content = open('tracker.md').read()
sections = {}
current_section = None
current_items = []

for line in content.split('\n'):
    m = re.match(r'^## (\d+)\.\s+(.+)$', line)
    if m:
        if current_section and current_items:
            sections[current_section] = current_items
        current_section = f'{m.group(1)}. {m.group(2).strip()}'
        current_items = []
    m2 = re.match(r'^\|(.+?)\|\s*\*{0,2}([A-Za-z]+)\*{0,2}\s*\|', line)
    if m2 and current_section and not line.startswith('| Ref'):
        code = m2.group(2).strip()
        if code in ('B','C','D','DA','U','S','P','UR','Final','TBV'):
            current_items.append(code)
```

## Deployment

```bash
surge --domain my-status.surge.sh ./deploy-dir/
```

## Pitfalls

- **CSS bar width = count/total × 100%** — if total is 0, default to 1 to avoid division by zero
- **Bar min-width: 24px** — ensures small values still show a visible sliver
- **Section grid uses `auto-fill, minmax(420px, 1fr)`** — on mobile this collapses to single column naturally
- **Donut chart needs Chart.js CDN** — the section cards do not; they're pure CSS
- **Data must be hardcoded as JS const** — no server-side rendering. Update via Python script that regex-replaces the `const SECTIONS = [...]` block
