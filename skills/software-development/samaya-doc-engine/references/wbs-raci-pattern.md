# WBS & RACI Matrix Pattern

Built for RCRC Exhibition Technical Proposal (Appendix G = WBS, Appendix B = RACI).

## WBS Structure

9 work packages, 46 elements across 4 pages.

| Package | ID | Elements |
|---------|----|----------|
| Project Management | 1.0 | 5 |
| Design & Development | 2.0 | 6 |
| Procurement & Supply | 3.0 | 7 |
| Factory Manufacturing | 4.0 | 6 |
| Site Mobilization | 5.0 | 4 |
| Gallery Fit-Out (G1–G7 + Reception) | 6.0 | 8 |
| AV/LED Installation | 7.0 | 7 |
| Integration & Programming | 8.0 | 4 |
| Testing & Commissioning | 9.0 | 6 |

## WBS Table Format

```html
<div class="banner"><b>N. Package Name</b><span>WBS: N.0</span></div>
<table class="eng-table compact" style="margin-top:1px;font-size:0.4rem;table-layout:fixed">
  <thead>
    <tr><th style="width:8%">ID</th><th style="width:25%">Task</th><th style="width:10%">Package</th><th style="width:45%">Description</th><th style="width:12%">Owner</th></tr>
  </thead>
  <tbody>
    <tr><td class="mono">N.1</td><td>Task Name</td><td>Package</td><td>Bilingual description</td><td>Owner</td></tr>
  </tbody>
</table>
```

## RACI Matrix Codes

| Code | Color | Meaning |
|------|-------|---------|
| R | `#1E40AF` blue | Responsible (does the work) |
| A | `#991B1B` red | Accountable (approves, signs off) |
| C | `#92400E` amber | Consulted (provides input) |
| I | `#065F46` teal | Informed (receives updates) |

CSS badges:
```css
.raci-r{background:#1E40AF;color:#fff;padding:1px 6px;border-radius:2px;font-weight:700;font-size:0.4rem}
.raci-a{background:#991B1B;color:#fff;padding:1px 6px;border-radius:2px;font-weight:700;font-size:0.4rem}
.raci-c{background:#92400E;color:#fff;padding:1px 6px;border-radius:2px;font-weight:700;font-size:0.4rem}
.raci-i{background:#065F46;color:#fff;padding:1px 6px;border-radius:2px;font-weight:700;font-size:0.4rem}
```

## Summary KPIs

```html
<div style="display:flex;gap:2px;margin-top:3px">
  <div style="flex:1;background:#0F172A;color:#fff;padding:3px;border-radius:2px;text-align:center">
    <b>N Work Packages</b><br>حزم عمل
  </div>
  <div style="flex:1;background:#1E40AF;color:#fff;padding:3px;border-radius:2px;text-align:center">
    <b>N WBS Elements</b><br>عنصر
  </div>
</div>
```
