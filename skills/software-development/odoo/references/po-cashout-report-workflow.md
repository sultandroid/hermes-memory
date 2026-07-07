# PO Cashout Report Workflow (Samaya Factory)

## When to Use
- User asks for a PO cashout / payment report for Samaya Factory (project 244)
- User provides a هام (WhatsApp) file with PO numbers to reconcile
- Need to build a formatted Excel report with Odoo data

## Workflow

### 1. Fetch POs from Odoo

```python
fields = ['name','partner_id','amount_total','date_order','state','project_id','invoice_status','partner_ref']
# Fetch ALL POs — Odoo 18 has a bug with project_id in search_read domain
all_pos = call('purchase.order', 'search_read', [[]], {'fields': fields, 'limit': 2000})
```

**⚠️ Odoo 18 domain bug:** `search_read` with `project_id` in the domain causes `TypeError: 'int' object is not subscriptable` on Odoo 18.0+e. Workaround: fetch all POs and filter in Python:
```python
factory_pos = [p for p in all_pos if p.get('project_id') and p['project_id'][0] == 244]
```

### 2. Filter Logic

| Condition | Include? |
|-----------|----------|
| Project != 244 (Samaya Factory) | Exclude |
| `amount_total <= 0` | Exclude |
| Credit supplier (Mada=2427, Saba=5603) | Exclude from main list, show as balance only |
| `state == 'cancel'` | Exclude |
| `state == 'draft'` | Include (user wants these visible) |
| `state == 'purchase'` + `invoice_status in ('to invoice','no')` | Include |
| `state == 'purchase'` + `invoice_status == 'invoiced'` | Include (user wants all هام POs) |

### 3. Credit Supplier Handling

**User preference:** Credit suppliers (Mada Aljezera, Saba Najad) are NOT listed as individual POs in the cashout report. They are handled via **periodic statements** (bank/supplier statement PDFs).

Show their total balance as a single line in the Summary, with a note: "Credit supplier POs not listed individually — handled via periodic statements."

For Saba Najad, when a statement PDF is available, show the breakdown:
- Opening balance
- Payment received
- New invoices
- Closing balance

### 4. هام File Reconciliation

When the user provides a هام file (WhatsApp screenshot/Excel with PO numbers):

1. Extract PO numbers from the file
2. Fetch those POs from Odoo
3. Apply filter logic above
4. Report which POs are included and which are excluded (with reason)
5. The هام file is the SOURCE OF TRUTH for which POs to include — not the Odoo project filter alone

### 5. Excel Formatting (openpyxl)

**Colors:** Navy `#1F3864` headers, yellow `#FFD700` totals, alternating `#F2F2F2` rows.

**Columns:** PO # (clickable Odoo link), Vendor, Vendor Reference, Description, Date, Amount (SAR), State, Invoice, Notes.

**PO # as hyperlink:**
```python
po_link = f'{ODOO_BASE}/web#id={po["id"]}&model=purchase.order'
cell = ws.cell(row=r, column=1, value=po['name'])
cell.hyperlink = po_link
cell.font = Font(color='0284C7', size=10, name='Calibri', underline='single')
```

**Page setup:** Landscape A4, `fitToWidth=1`.

**Sheets:** Summary, POs Detail, (optional) Mada Aljezera, Saba Najad.

### 6. Descriptions from هام File

Maintain a Python dict mapping PO numbers to Arabic descriptions from the هام file:
```python
descriptions = {
    'P01094': 'المصنع - طابعات اوراق',
    'P01818': 'وايرليس و تابليت - ا عبد الله محفوظ',
    ...
}
```

### 7. Credit Supplier Balances

Calculate from ALL unpaid Factory POs for that partner (not just the هام list):
```python
mada_all = [p for p in all_pos 
    if p.get('project_id') and p['project_id'][0] == 244
    and p.get('partner_id') and p['partner_id'][0] == 2427
    and p['state'] == 'purchase'
    and p.get('invoice_status') in ('to invoice','no')
    and p['amount_total'] > 0]
mada_total = sum(p['amount_total'] for p in mada_all)
```

### 8. Script Pattern

Write the build script to `/tmp/build_cashout_report.py` and execute it. Never inline Python heredocs for multi-sheet Excel generation — write to a file first.

## Pitfalls

- **Odoo 18 domain bug:** `project_id` in `search_read` domain crashes. Always fetch all and filter in Python.
- **Odoo 500-row limit:** `search_read` defaults to 500. Total POs may be 1895+. Set `limit=2000`.
- **هام file may have POs outside first 500:** Old POs (P01094, P01252) won't appear in a 500-row fetch. Always use `limit=2000`.
- **Credit supplier POs in هام file:** The user explicitly excludes these from the main list. Don't ask — just move them to the credit supplier section.
- **Zero-amount POs:** Always exclude (P01543, P01876, P02053, P02092 patterns).
- **Cancelled POs:** Exclude (P01252, P02066 patterns).
- **Other-project POs in هام file:** The هام file may contain POs from other projects (P01224 = project 227). Exclude with reason.
