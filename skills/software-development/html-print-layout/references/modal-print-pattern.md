# Modal Print Pattern

When building a single-file HTML app that needs to print individual records (lessons, risks, submittals) as A4 documents, use this pattern:

## Approach

1. The main page (table, filters, KPIs) is hidden during print via `@media print { display: none }`
2. A `.print-mode` class is toggled on the modal overlay before calling `window.print()`
3. The print CSS shows only the modal content as a full A4 page

## CSS

```css
/* Hide everything except the modal during print */
@media print {
  .app-header, .kpi-bar, .filter-bar, .table-wrap, .app-footer { display: none; }

  /* Show modal as full page when print-mode is active */
  .modal-overlay.print-mode {
    display: block !important;
    position: static !important;
    background: none !important;
    padding: 0 !important;
  }
  .modal-overlay.print-mode .modal-content {
    max-width: 100% !important;
    max-height: none !important;
    box-shadow: none !important;
    border-radius: 0 !important;
    animation: none !important;
  }
  .modal-overlay.print-mode .modal-header {
    background: #1E293B !important;
    color: #fff !important;
    -webkit-print-color-adjust: exact !important;
    print-color-adjust: exact !important;
    border-radius: 0 !important;
  }
  .modal-overlay.print-mode .btn-print { display: none !important; }

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

## JavaScript

```javascript
function printLesson() {
  const overlay = document.getElementById('modalOverlay');
  overlay.classList.add('print-mode');
  window.print();
  // Remove class after print dialog closes
  overlay.classList.remove('print-mode');
}
```

## Key Details

- The `.print-mode` class is added **before** `window.print()` and removed **after** — the print dialog is synchronous in most browsers
- `-webkit-print-color-adjust: exact` ensures colored backgrounds (navy header, status badges) print correctly
- The fixed `.print-footer` appears on every printed page via `position: fixed; bottom: 0`
- The `@page` rule sets A4 portrait with 15mm/18mm margins
- The print button itself is hidden via `.modal-overlay.print-mode .btn-print { display: none }`
