# Contact & Quotation Creation (Samaya Odoo)

## Creating a Company Contact (`res.partner`)

**Pitfall:** `is_company=True` requires a VAT field. Without it, Odoo raises:
`Tax ID (VAT) is required for company "Lujain".`

**Fix:** Always include `"vat": "TBC"` (or the real VAT) when creating company-type partners.

```python
partner_id = models.execute_kw(DB, uid, PWD, "res.partner", "create", [{
    "name": "Lujain",
    "email": "M.Arafat@nord.sa",
    "phone": "+966 54 398 7228",
    "website": "https://lujain.com.sa",
    "company_type": "company",
    "is_company": True,
    "vat": "TBC",  # REQUIRED for company contacts
}])
```

Individual contacts (`is_company=False`, the default) don't need VAT.

## Creating a Draft Quotation (`sale.order`)

Customer quotations use the `sale.order` model, NOT `purchase.order`.

```python
so_id = models.execute_kw(DB, uid, PWD, "sale.order", "create", [{
    "partner_id": partner_id,
    "partner_invoice_id": partner_id,
    "partner_shipping_id": partner_id,
    "state": "draft",  # default, but explicit is fine
    "order_line": [(0, 0, {
        "product_id": product_id,
        "name": product_name,
        "product_uom_qty": 1.0,
        "price_unit": price,
    })],
}])
```

**Quotation URL pattern:**
```
{ODOO_BASE}/web#id={so_id}&model=sale.order&view_type=form
```

## Checking for Existing Contacts

Always search by email first to avoid duplicates:

```python
existing = models.execute_kw(DB, uid, PWD, "res.partner", "search_read",
    [[["email", "=", email]]],
    {"fields": ["id", "name", "email", "phone", "website"]})
```

## Listing Saleable Products

```python
products = models.execute_kw(DB, uid, PWD, "product.product", "search_read",
    [[["sale_ok", "=", True]]],
    {"fields": ["id", "name", "list_price", "default_code"], "limit": 20})
```
