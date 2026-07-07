# Samaya Odoo — Procurement Workflow (Replica Project SC-01 Pattern)

## Full Procurement Pipeline

```
Supplier Research → Create Supplier (res.partner) → Create Product (product.product) → Create RFQ (purchase.order draft) → Receive Quote → Update Prices → Confirm PO
```

## 1. Create Supplier (res.partner)

**⚠ VAT required:** KSA localization requires `vat` (Tax ID) for company-type partners.

**VAT rules:**
- **KSA vendors** (`country_id: 192`): VAT must be 15 digits, first and last digit = "3" (e.g. `311873177200003`). Set `company_type: 'company'`, `is_company: True`.
- **International vendors** (UAE, Egypt, etc.): If the vendor does NOT have a KSA VAT number, do NOT set `company_type: 'company'` — KSA localization will reject any VAT format that doesn't match the 15-digit KSA pattern. Instead, keep `company_type: 'person'` (which bypasses the KSA VAT requirement entirely). The PO can still be created against a person-type vendor.
- **Wrong VAT format** (e.g. `'EG-PLACEHOLDER'` or `'AE123456789'` on a company-type vendor) **will be rejected** with: `The VAT Number does not seem to be valid. Note: the expected format is 310175397400003 [Fifteen digits, first and last digits should be "3"]`.
- **Fixing an existing vendor**: If the vendor already exists with `company_type='person'` and no VAT, you can create POs against it without changing to `company_type='company'`.

```python
partner_id = models.execute_kw(db, uid, pwd, 'res.partner', 'create', [{
    'name': 'ESTS - Electronics Scientific Trading',          # Full trading name
    'company_type': 'person',                                  # Use 'person' for non-KSA vendors without KSA VAT
    'supplier_rank': 1,                                        # Mark as supplier
    'customer_rank': 0,                                        # Not a customer
    'country_id': 229,                                         # UAE = 229, KSA = 192
    'email': 'info@supplier.com',
    'website': 'https://supplier.com',
    'comment': 'Notes about what they supply',
}]
```

**Always search by partial name AND email domain before creating a vendor** — the user's Odoo may have the vendor under a slightly different name:
```python
partners = models.execute_kw(db, uid, pwd, 'res.partner', 'search_read',
    [[['name','ilike','radinance']]], {'fields':['id','name','email','supplier_rank'],'limit':5})
# If found with same email domain but different name, UPDATE the name instead of creating duplicate:
models.execute_kw(db, uid, pwd, 'res.partner', 'write',
    [[partner_id], {'name': 'Radinance Group'}])
```

**Country IDs:** KSA = 192, UAE = 229, Egypt = 65

## 2. Create Product (product.product)

For services/equipment procurement (not stock items):

```python
product_id = models.execute_kw(db, uid, pwd, 'product.product', 'create', [{
    'name': 'X-Rite Ci64UV Spectrophotometer',                 # Product name
    'type': 'service',                                         # 'service' for non-stock, 'consu' for consumables
    'categ_id': 640,                                            # 640 = Subcontracts category
    'lst_price': 40000.0,                                      # List price (estimated)
    'standard_price': 40000.0,                                 # Cost price
    'uom_id': 1,                                               # Units
    'uom_po_id': 1,
    'default_code': 'CI64-XR-UV',                              # Optional: internal SKU
    'description': 'Detailed description for RFQ/PO line',
}])
```

Product categories commonly used:
- 640 = Subcontracts (services, consulting, equipment procurement)
- 639 = Contracts
- 679 = Software and System Support (for software licenses, subscriptions — e.g. Autodesk AEC Collection uses this category)

## 3. Create RFQ (purchase.order in draft)

### RFQ Pattern (Currency: USD — for international suppliers)

```python
from datetime import datetime

rfq_id = models.execute_kw(db, uid, pwd, 'purchase.order', 'create', [{
    'partner_id': 8156,                          # Supplier ID
    'project_id': 219,                            # Aseer Museum project
    'date_order': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
    'currency_id': 1,                             # USD for international
    'payment_term_id': 4,                         # 30 Days
    'origin': 'RFQ for Replica Project (SC-01) - Equipment Name',
    'notes': 'Request for Quotation text...',
    'order_line': [(0, 0, {
        'product_id': 27626,
        'name': 'Full product description for RFQ line',
        'product_qty': 1.0,
        'product_uom': 1,
        'price_unit': 40000.0,                   # Estimated price
        'taxes_id': [(6, 0, [])],                # No tax on international RFQs
    })],
}])
```

### RFQ Pattern (Currency: SAR — for local KSA suppliers)

```python
rfq_id = models.execute_kw(db, uid, pwd, 'purchase.order', 'create', [{
    'partner_id': supplier_id,
    'project_id': 219,
    'date_order': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
    'currency_id': 150,                          # SAR
    'payment_term_id': 4,
    'origin': 'طلب عرض سعر - مشروع متحف عسير',
    'notes': '<div style="direction: rtl;"><p>نص الطلب...</p></div>',
    'order_line': [(0, 0, {
        'product_id': product_id,
        'name': 'وصف تفصيلي',
        'product_qty': 1.0,
        'product_uom': 1,
        'price_unit': 15000.0,
        'taxes_id': [(6, 0, [5])],               # 15% Purchase Tax for KSA suppliers
    })],
}])
```

### ⚠ Key differences: RFQ vs PO

| Aspect | RFQ (Request for Quote) | Confirmed PO |
|--------|------------------------|--------------|
| State | `draft` | `purchase` (after confirm) |
| Price | Estimated | Actual from supplier quote |
| Purpose | Send to supplier for pricing | Commit to purchase |
| In Odoo | Same `purchase.order` model | Same model, different state |

Both are the same model in Odoo. An RFQ starts as draft, and after the user reviews and confirms, it becomes a confirmed PO.

## 4. Common Partner IDs (Samaya Odoo)

| Vendor | ID | Supplies |
|--------|----|----------|
| شركة نبيل قطب للاستشارات الهندسية | 2640 | Structural engineering |
| ESTS - Electronics Scientific Trading | 8156 | X-Rite spectrophotometer |
| Tajco Scientific | 8157 | BYK gloss meter |
| 3D Middle East (check/create) | — | Artec Spider II scanner |
| **مؤسسة أرساد الخليج للتجارة (ARSSAD ALKHALIJ)** | **8193** | **Faro Focus Premium 200m / Faro Blink** |
| **Radinance Group** | **6366** | **Autodesk AEC Collection / BIM Collaborate licensing** |

## 5. Common Product IDs (Samaya Odoo)

| Product | ID | Est. Price (SAR) |
|---------|----|------------------|
| X-Rite Ci64UV Spectrophotometer | 27626 | 40,000 |
| BYK micro-TRI-gloss | 27627 | 8,000 |
| أعمال الدراسات والتصميم الإنشائي | 27618 | 15,000 |
| Artec Spider II (TBD — from 3DME) | — | 131,250 |
| **Faro Focus Premium 200m** | **27782** | **195,000** |
| **Faro Blink** | **27783** | **140,000** |
| **Architecture Engineering & Construction Collection Commercial** | **23589** | **$50/user/month** |
| **BIM Collaborate Pro** | **23590** | **$50/user/month (est.)** |

## 6. Real-World Example: Faro Focus Premium 200m RFQ

Created June 2026 for Aseer Museum project 219.

### Supplier
- **Name:** مؤسسة أرساد الخليج للتجارة — ID: 8193
- **VAT:** 311873177200003 | **Email:** sales-manager@arssadalkhalij.com | **Phone:** +966 55 229 8744
- **Country:** KSA (ID 192)

### Product Creation
```python
product_id = models.execute_kw(db, uid, api_key, 'product.product', 'create', [{
    'name': 'Faro Focus Premium 200m - ماسح ضوئي ليزري ثلاثي الأبعاد',
    'type': 'service', 'categ_id': 640,
    'lst_price': 195000.0, 'standard_price': 195000.0,
    'uom_id': 1, 'uom_po_id': 1,
    'default_code': 'FARO-FOCUS-P200',
    'description': 'Faro Focus Premium 200m 3D Laser Scanner - includes scanner, tripod, batteries, charger, case, backpack, training, 1yr warranty',
}])
```

### RFQ
```python
rfq_id = models.execute_kw(db, uid, api_key, 'purchase.order', 'create', [{
    'partner_id': 8193,        # ARSSAD ALKHALIJ
    'project_id': 219,          # Aseer Museum
    'date_order': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
    'currency_id': 150,         # SAR
    'origin': 'طلب عرض سعر - ماسح ضوئي ليزري Faro Focus Premium 200m - مشروع متحف عسير',
    'notes': '<div style="direction: rtl;"><h4>طلب عرض سعر</h4><p>الماسح الضوئي Faro Focus Premium 200m شامل الملحقات والتدريب والضمان</p><p>شروط الدفع: 50% / 25% / 25%</p></div>',
    'order_line': [(0, 0, {
        'product_id': 27782,
        'name': 'Faro Focus Premium 200m - شامل الملحقات والتدريب والضمان',
        'product_qty': 1.0, 'product_uom': 1,
        'price_unit': 195000.0,
        'taxes_id': [(6, 0, [5])],   # 15% Purchase Tax
    })],
}])
# Result: RFQ 1911, total SAR 224,250 (incl. VAT)
```

### ⚠ SSL Certificate Workaround
Samaya Odoo at `samayainv.odoo.com` has SSL cert issues with Python's default SSL context. Use:
```python
import ssl, xmlrpc.client
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE
common = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/common', context=ctx)
models = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/object', context=ctx)
```

## 7. Real-World Example: Autodesk AEC Collection Subscription RFQ

Created June 2026 for CG Team software licensing from Radinance Group.

### Scenario
- **Supplier:** Radinance Group (Egypt-based, no KSA VAT) — ID: 6366
- **Product:** Autodesk AEC Collection (incl. BIM Collaborate Pro) — ID: 23589
- **Licenses:** 10 named-user subscriptions
- **Term:** 3 months
- **Rate:** $50/user/month
- **Total:** 10 × $150 ($50×3) = **$1,500.00 USD**
- **Project:** Internal (ID: 1)

### Pricing Pattern for Software Subscriptions
For multi-user × multi-month subscriptions, the PO line uses:
- `product_qty`: number of users (10)
- `price_unit`: monthly_rate × number_of_months ($50 × 3 = $150)
- Total = qty × price_unit = $1,500

This avoids creating separate lines per user or month.

### Vendor: Update Existing Instead of Creating Duplicate
If the vendor exists under a slightly different name, update it:

```python
# Rename existing vendor to match user's preferred name
models.execute_kw(db, uid, pwd, 'res.partner', 'write',
    [[6366], {'name': 'Radinance Group',
              'supplier_rank': 5}])
```

### RFQ Creation with HTML User Table in Notes

```python
from datetime import datetime

user_list_html = '''<div style="direction:ltr">
<h3>Request for Quotation — Autodesk AEC Collection</h3>
<p><strong>Product:</strong> Autodesk AEC Collection (incl. BIM Collaborate Pro)<br>
<strong>Licenses:</strong> 10 named-user subscriptions<br>
<strong>Term:</strong> 3 months<br>
<strong>Rate:</strong> $50.00/user/month<br>
<strong>Total:</strong> $1,500.00 USD</p>
<h4>User List</h4>
<table border="1" cellpadding="4" style="border-collapse:collapse;width:100%">
<tr style="background:#0F172A;color:white"><th>#</th><th>Name</th><th>Title</th><th>Email</th></tr>
<tr><td>1</td><td>Mohamed Elsayed Elbaz</td><td>Senior Electrical Engineer</td><td>melbaz@cg.com.sa</td></tr>
<tr><td>2</td><td>Mohammed Majdi Abdrabuh</td><td>Senior Mechanical Engineer</td><td>mabdelaal@cg.com.sa</td></tr>
<!-- ... all 10 users ... -->
<tr><td>10</td><td>Mohamed Elroby</td><td>Site Manager</td><td>melroby@cg.com.sa</td></tr>
</table>
</div>'''

rfq_id = models.execute_kw(db, uid, pwd, 'purchase.order', 'create', [{
    'partner_id': 6366,
    'project_id': 1,                             # Internal project
    'date_order': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
    'currency_id': 1,                             # USD
    'payment_term_id': 4,                         # 30 Days
    'origin': 'SAM-IT-2026-001 - Autodesk AEC Collection CG Team',
    'notes': user_list_html,
    'order_line': [(0, 0, {
        'product_id': 23589,                     # AEC Collection
        'name': 'Autodesk AEC Collection (incl. BIM Collaborate Pro) - 10 users x 3 months',
        'product_qty': 10.0,
        'product_uom': 1,
        'price_unit': 150.0,                     # $50 x 3 months
        'taxes_id': [(6, 0, [])],                # No tax - international supplier
    })],
}])
# Result: RFQ P02036, total $1,500.00
```

## 8. Currency Convention

- **International suppliers** (UAE, Dubai): Use **USD** (ID 1) for RFQ, add note about SAR equivalent
- **Local KSA suppliers**: Always use **SAR** (ID 150)
- After creating PO in draft, verify currency — default is USD (ID 1) even if SAR was specified in some configurations
