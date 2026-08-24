# Finding POs / invoices for a person vs a vendor company (Odoo XML-RPC)

A person is often a **child contact** of a vendor company in `res.partner`
(`parent_id` set). POs are booked against the **parent** vendor, not the child
person. Searching POs by the person's name returns empty; you must climb to the
parent.

## Pattern (Samaya instance, project 219 = Aseer)

```python
from odoo_connect import connect
uid, models, cfg = connect("samaya")

# 1. Find the person; read parent_id
p = models.execute_kw(cfg['db'], uid, cfg['pw'], 'res.partner', 'search_read',
    [[['name','ilike','Waleed']]], {'fields':['id','name','email','parent_id','supplier_rank']})
# -> e.g. {"id":6367,"name":"Waleed Salah","parent_id":[6366,"Radiance Group"]}

# 2. Query POs against the PARENT id (and the child) — child alone returns []
pos = models.execute_kw(cfg['db'], uid, cfg['pw'], 'purchase.order', 'search_read',
    [[['partner_id','in',[6366,6367]]]],
    {'fields':['id','name','amount_total','state','invoice_status','project_id','date_order'],'order':'create_date desc','limit':15})
```

**Key fields on `purchase.order`:**
- `invoice_status` — one of `no` / `to invoice` / `invoiced` / `to receive & bill` (use this to identify which PO is ready for the next invoice). **There is NO `amount_to_invoice` field on `purchase.order`** — requesting it raises `ValueError: Invalid field 'amount_to_invoice'`.
- `amount_untaxed`, `amount_tax`, `amount_total`, `project_id` (header), `payment_term_id`, `origin`.
- Per-line billing state lives on `purchase.order.line`: `qty_invoiced`, `qty_received`, `qty_to_invoice`.

## Reading a PO's invoice-readiness
For each candidate PO, read its `invoice_status` + the line `qty_invoiced` to tell
`invoiced` (fully billed) vs `to invoice` (has balance) vs `cancel`.

## Context
- Aseer Museum = project **219** on Samaya Odoo (`samayainv.odoo.com`, user `sultan@samayainvest.com`).
- Sample finding: Dr. Waleed Salah (BIM) is a child contact of **Radiance Group** (id 6366);
  Radiance holds PO **P00555** (BIM services, SAR 20,000, ~46% invoiced → `to invoice`)
  and **P02003** (Autodesk AEC, SAR 1,500, `to invoice`).
- Script location: `/Users/mohamedessa/.hermes/shared_exchange/skills/claude/software-development/odoo/scripts/odoo_connect.py` (also mirrored under `.agents/`, `.claude/`, `.kimi/`, `.codex/`, `hermes-memory/skills/`).
