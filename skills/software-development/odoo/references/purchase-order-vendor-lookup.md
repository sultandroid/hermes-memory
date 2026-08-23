# Finding a Vendor's Purchase Orders & Invoices (Samaya Odoo 18)

Worked 2026-08-23: user asked to open the PO page of an individual specialist (Dr. Waleed Salah, BIM) and draft the next invoice.

## Pattern

1. **Locate the person's partner record.** Search `res.partner` by name. An individual specialist is often a *child* of a company: `parent_id` points to the billing company.

   ```python
   models.execute_kw(db, uid, pw, 'res.partner', 'search_read',
       [[['name','ilike','waleed']]], {'fields':['id','name','email','parent_id','supplier_rank'],'limit':20})
   ```

2. **Search POs by the company id**, not the person's id — invoices/POs are on the parent vendor. Example: `Waleed Salah` (id 6367) has `parent_id` = `Radiance Group` (id 6366); POs are on 6366, not 6367. Querying `partner_id = 6367` returns `[]`.

   ```python
   pos = models.execute_kw(cfg['db'], uid, cfg['pw'], 'purchase.order', 'search_read',
       [[['partner_id','in',[6366,6367]]]],
       {'fields':['id','name','partner_id','amount_total','state','invoice_status','project_id','date_order','origin'],'order':'create_date desc'})
   ```

3. **Which PO is the one to invoice?** Filter on `invoice_status == 'to invoice'`. Open lines' `qty_invoiced` vs `qty_received`/`product_qty` gives the unpaid balance. The main services contract PO is usually the one with a large remaining balance (e.g. P00555 BIM Services, SAR 20,000, 46% invoiced).

## Useful fields
- `purchase.order`: `name` (PO no), `partner_id`, `amount_total`, `amount_untaxed`, `amount_tax`, `state` (purchase/draft/cancel), `invoice_status` (`to invoice`/`invoiced`/`no`), `project_id`, `date_order`, `payment_term_id`, `origin`.
- `purchase.order.line`: `name` (description, may contain the contract no), `product_id`, `product_qty`, `price_unit`, `price_subtotal`, `qty_invoiced`, `qty_received`.

## Pitfall — invalid field
`amount_to_invoice` is NOT valid on `purchase.order` — raises `ValueError: Invalid field 'amount_to_invoice'`. Use `invoice_status` on the header + `qty_invoiced` on the line instead.

## Opening the PO page for the user
PO pages live at `https://samayainv.odoo.com/odoo/purchase/<id>` (e.g. `/odoo/purchase/555`).

## Confirm before drafting an invoice
Ask which PO (default = the contract PO with the remaining balance) and the amount/percentage before creating the vendor bill. Respect the standard PO-approval guardrails (quotation attached, line/total match, ±20% of standard_price) per the PO-approval skill.
