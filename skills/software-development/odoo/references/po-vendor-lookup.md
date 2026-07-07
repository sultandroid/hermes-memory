# PO Vendor Lookup by PO Name (Samaya Odoo)

When given a list of PO numbers (e.g. from a PDF or screenshot backlog list),
look up each PO in `purchase.order` by its `name` field to get vendor, price,
state, date, and database ID for building direct links.

## Query Pattern

```python
# Single PO lookup
records = models.execute_kw(db, uid, api_key, "purchase.order", "search_read",
    [[["name", "=", "P01927"]]],
    {"fields": ["id", "name", "partner_id", "amount_total", "state", "date_order"]})

if records:
    r = records[0]
    odoo_id = r["id"]                       # Integer DB ID for URL
    partner = r.get("partner_id", ["", ""]) # [id, display_name] tuple
    vendor_name = partner[1] if isinstance(partner, list) else str(partner)
    amount = r.get("amount_total", 0)
    state = r.get("state", "")
    date = r.get("date_order", "")
```

## Batch Lookup (list of PO names)

```python
po_names = ["P01927", "P01926", "P01924", ...]
for po_name in po_names:
    records = models.execute_kw(db, uid, api_key, "purchase.order", "search_read",
        [[["name", "=", po_name]]],
        {"fields": ["id", "name", "partner_id", "amount_total", "state", "date_order"]})
    if records:
        r = records[0]
        print(f"{po_name}|{r['id']}|{vendor_name}|{amount}|{state}|{date}")
    else:
        print(f"{po_name}|NOT_FOUND|||")
```

## State Mapping (display labels)

| Odoo State | Arabic Label |
|------------|-------------|
| `draft`    | مسودة |
| `purchase` | أمر شراء |
| `done`     | منتهي |
| `cancel`   | ملغي |

## Odoo PO URL Format (direct link)

```
https://samayainv.odoo.com/web#id={odoo_id}&model=purchase.order&view_type=form
```

Set as hyperlink in Excel:
```python
cell.hyperlink = url
cell.value = "فتح الأمر " + po_name
cell.font = Font(color='0563C1', underline='single')
```

## Zero-Value PO Handling

Always cross-reference Odoo `amount_total` — a PO may show a value in a PDF/screenshot
but be 0.00 in Odoo (draft RFQ, cancelled, or unfilled). Remove or flag those.
Check `state` — `cancel` means the PO was cancelled, worth keeping for reference.
