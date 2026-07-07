# PO Report Update Workflow

When user says "update the POs reports" and attaches the Samaya Factory Cashout Report Excel.

## Workflow

### 1. Read the Existing Report

Use openpyxl with `data_only=True` to read the current report structure. Note:
- **Summary sheet**: Cashout requirements, PO table, credit suppliers, excluded items
- **POs Detail sheet**: All POs with vendor, date, amount, receipt status, due, bills
- **Mada Aljezera / Saba Najad sheets**: Credit supplier transaction logs (keep untouched)

Key data points from Summary:
- Outstanding PO count + total
- Credit supplier balances (Mada, Saba)
- Grand total required

### 2. Check Odoo for Current Data

Connect to Samaya Odoo via XML-RPC:
```python
import xmlrpc.client, ssl
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE
common = xmlrpc.client.ServerProxy("https://samayainv.odoo.com/xmlrpc/2/common", context=ctx)
uid = common.authenticate(db, user, api_key, {})
models = xmlrpc.client.ServerProxy("https://samayainv.odoo.com/xmlrpc/2/object", context=ctx)
```

### 3. Query Criteria for Cashout POs

```python
# Confirmed, unbilled, SAR, >=1000, exclude credit suppliers
pos = models.execute_kw(db, uid, api_key, 'purchase.order', 'search_read',
    [[
        ('state', '=', 'purchase'),
        ('invoice_status', '=', 'to invoice'),
        ('amount_total', '>=', 1000),
    ]],
    {'fields': ['name','partner_id','date_order','amount_total','currency_id'],
     'order': 'name', 'limit': False})
```

**Filters to apply in code (not in domain):**
- **Currency**: Skip non-SAR (`currency_id[1] != 'SAR'`)
- **Credit suppliers**: Known vendor IDs — Mada Aljezera (2427), Saba Najad (5603)
- **Below 1000 SAR**: Original report excludes these

### 4. Check Existing PO Statuses

For each PO in the original report, verify its current state in Odoo:
```python
po_info = models.execute_kw(db, uid, api_key, 'purchase.order', 'search_read',
    [[('name', '=', 'P01818')]],
    {'fields': ['state','invoice_status','invoice_count','amount_total']})
```

**Status change interpretations:**
- `invoice_status = 'invoiced'` and `invoice_count > 0` → PO has been billed, remove from cashout (set due=0)
- `invoice_status = 'to invoice'` and `invoice_count = 0` → Still unbilled, keep
- `invoice_status = 'to invoice'` and `invoice_count > 0` → Partial billing, keep with remaining amount
- `state = 'draft'` → Not yet confirmed, exclude (unless user confirmed it's real — check Notes column)

### 5. Get Credit Supplier Balances

```python
for pid in [2427, 5603]:  # Mada, Saba
    posted = models.execute_kw(db, uid, api_key, 'account.move', 'search_read',
        [[('partner_id','=',pid), ('state','=','posted')]],
        {'fields': ['name','amount_total','payment_state'], 'limit': 200})
    open_balance = sum(b['amount_total'] for b in posted if b['payment_state'] != 'paid')
```

**Important:** User confirmed "keep original credit supplier balances" pattern — only update if explicitly told to.

### 6. Update the Excel

**Key challenges with merged cells:**

```python
# ALWAYS unmerge before writing to merged ranges
for mc in list(ws.merged_cells.ranges):
    ws.unmerge_cells(str(mc))

# When inserting rows before stats footer, unmerge first
ws.unmerge_cells('A15:G15')
ws.insert_rows(13, count)
```

**POs Detail sheet update:**
1. Mark invoiced POs with `due=0` and status `"Paid — Invoiced"`
2. Insert rows for new POs before the statistics section
3. Write all rows sequentially (old valid + old invoiced + new + screen stand)
4. Update statistics footer

**Summary sheet update (unmerge all, rebuild):**
1. Unmerge everything
2. Clear all cells
3. Rewrite: Cashout requirements → PO table → Credit suppliers → Grand total → Notes
4. Do not re-merge — the data is readable without merged cells
5. Add an `▎UPDATES` notes section at the bottom

### 7. PO Table Structure

Each row: (PO#, Vendor, Date, Amount, Due, Status, Notes)

**Status values:**
- `"Pending"` — confirmed, unbilled
- `"Paid — Invoiced"` — bill received, due=0
- `"Draft — Unpaid"` — not confirmed in Odoo but user confirmed real
- `"Partial — X remaining"` — partial billing

### 8. Screen Stand Entry

When adding a costed-but-not-yet-PO item:
```
PO# = "NEW"
Vendor = "Screen Stand + Counter (MDF, painted)"
Notes = "Costing approved — PO pending"
```

### 9. Openpyxl Techniques for This File

```python
# Copy cell style from reference row
from copy import copy
ref_row = 5
for c in range(1, 8):
    src = ws.cell(row=ref_row, column=c)
    dst = ws.cell(row=new_row, column=c)
    if src.has_style:
        dst.font = copy(src.font)
        dst.border = copy(src.border)
        dst.fill = copy(src.fill)
        dst.number_format = copy(src.number_format)
        dst.alignment = copy(src.alignment)

# After insert_rows, all references shift — recalc totals
```

### 10. Verification

After saving:
- Verify the file opens in Excel without corruption
- Check: PO count, total amount, total due, grand total
- Confirm credit supplier balances are unchanged (unless told)

## Pitfalls

- **MergedCell write errors**: `'MergedCell' object attribute 'value' is read-only` — Always unmerge the affected range first
- **Prepared date**: Update to current date in Summary row 2
- **Odoo API doman syntax**: Use flat list format `[('field','op','value')]` — avoid nested `|` operators which cause syntax errors
- **Credit supplier IDs**: Check Odoo for current vendor IDs (they may change). Use `res.partner` search with name lookup
- **Vendor ID verification**: Credit suppliers have moved IDs in the past. Always verify by searching `('name', 'ilike', 'مؤسسة مدى الجزيرة')` before filtering
- **P02025 discrepancy**: The Excel may show a different vendor/amount than Odoo — trust the user's notes column over Odoo for manually-entered data
