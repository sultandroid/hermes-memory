# Samaya Factory Cashout Report — Build Guide

## Source

Odoo `purchase.order` records for **project 244 (Samaya Factory)** on `samayainv.odoo.com`.

## Connection

```python
# SSL fix for macOS Python 3.13+
SSL_CERT_FILE=$(python3 -c "import certifi; print(certifi.where())") python3 script.py
```

## Data Fetching

```python
fields = ['name','partner_id','amount_total','date_order','state','project_id','invoice_status','partner_ref']
all_pos = call('purchase.order', 'search_read', [[]], {'fields': fields, 'limit': 2000})
```

**⚠️ Domain bug:** `project_id` in `search_read` domain crashes Odoo 18.0+e. Always fetch all and filter in Python:
```python
factory_pos = [p for p in all_pos if p.get('project_id') and p['project_id'][0] == 244]
```

## Filtering Rules

| Include | Exclude |
|---------|---------|
| `state == 'purchase'` | `state == 'cancel'` |
| `invoice_status in ('to invoice', 'no')` | `invoice_status == 'invoiced'` |
| `amount_total > 0` | `amount_total <= 0` |
| Not a credit supplier | Credit suppliers (Mada=2427, Saba=5603) |

## Credit Suppliers

- **Mada Aljezera** (partner 2427) — show as statement balance total
- **Saba Najad** (partner 5603) — show as statement balance total with breakdown (opening, payment, new invoices, closing)
- Do NOT list individual credit supplier POs in the main table
- Add a note: "Credit suppliers handled via periodic statements"

## Excel Format

| Element | Value |
|---------|-------|
| Header fill | Navy `#1F3864` |
| Header font | White, bold, Calibri 11 |
| Total row fill | Yellow `#FFD700` |
| Alternating rows | Light gray `#F2F2F2` |
| Orientation | Landscape |
| Fit to page | `fitToWidth=1` |
| Body font | Calibri 10, color `#1E293B` |
| Number format | `#,##0.00` |

## Columns (POs Detail sheet)

1. **PO #** — clickable hyperlink to Odoo: `{ODOO_BASE}/web#id={id}&model=purchase.order`
2. **Vendor** — `partner_id[1]`
3. **Vendor Reference** — `partner_ref` field
4. **Description** — from هام file or `partner_ref`
5. **Date** — `date_order[:10]`
6. **Amount (SAR)** — `amount_total`
7. **Due (SAR)** — same as amount (all unpaid)
8. **State** — `state`
9. **Invoice** — `invoice_status`
10. **Notes** — "No Bill" + optional `[supplier IN: ref#]`

## Sheets

1. **Summary** — cashout requirements, credit supplier balances with breakdown
2. **POs Detail** — individual PO rows + credit supplier section + excluded list
3. (Optional) **Mada Aljezera** / **Saba Najad** — statement detail

## Supplier Invoice Mapping

Match Saba Najad statement invoice numbers to POs by amount:
```python
supplier_invoices = {
    'P01865': '20229',   # 4,174.50
    'P02026': '20580',   # 1,322.50
    'P02041': '20653',   # 621.00
    'P02078': '20661',   # 2,461.00
}
```

## Odoo Hyperlink

```python
po_link = f'{ODOO_BASE}/web#id={po["id"]}&model=purchase.order'
cell.hyperlink = po_link
cell.font = Font(color='0284C7', underline='single')
```
