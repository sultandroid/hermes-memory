# Samaya Odoo — Purchase Orders

## Instance Details
- **URL**: `https://samayainv.odoo.com`
- **DB**: `peerless-tech-samaya-18-0-18447146`
- **User**: `sultan@samayainvest.com`
- **Password Source**: `~/.config/samaya/odoo.env` (key: `ODOO_API_KEY`)
- **Type**: Odoo 18 Enterprise (cloud-hosted)

## Authentication
```python
import xmlrpc.client, ssl, certifi
ctx = ssl.create_default_context(cafile=certifi.where())
common = xmlrpc.client.ServerProxy(f'{URL}/xmlrpc/2/common', context=ctx)
uid = common.authenticate(DB, USER, PWD, {})
models = xmlrpc.client.ServerProxy(f'{URL}/xmlrpc/2/object', context=ctx)
```

## Purchase Order Creation Workflow

### Step 1: Find or Create Vendor (res.partner)
```python
# Search vendor
vendors = models.execute_kw(db, uid, pwd, 'res.partner', 'search_read',
    [['name', 'ilike', 'اسم المورد']],
    {'fields': ['id', 'name', 'display_name']})
```

### Step 2: Create Service Product (product.product)
```python
product_id = models.execute_kw(db, uid, pwd, 'product.product', 'create', [{
    'name': 'اسم الخدمة أو المنتج',
    'type': 'service',                    # 'service' for services, 'consu' for materials
    'categ_id': 640,                      # 640 = Subcontracts, 639 = Contracts
    'lst_price': 15000.0,                 # Sales price
    'standard_price': 15000.0,            # Cost price
    'uom_id': 1,                          # 1 = Units
    'uom_po_id': 1,
    'description': 'وصف الخدمة',
}])
```

**Known Product Categories:**
| ID | Name |
|----|------|
| 1 | All |
| 639 | Contracts |
| 640 | Subcontracts |

### Step 3: Create Purchase Order (purchase.order)
```python
from datetime import datetime

po_id = models.execute_kw(db, uid, pwd, 'purchase.order', 'create', [{
    'partner_id': 2640,                    # Vendor ID
    'project_id': 219,                     # Project ID (optional)
    'date_order': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
    'currency_id': 150,                    # 150 = SAR, 1 = USD
    'fiscal_position_id': False,
    'payment_term_id': 4,                  # Payment term (see below)
    'origin': 'مرجع العرض',
    'notes': '<p>شروط وأحكام بالغة العربية</p>',
    'order_line': [(0, 0, {
        'product_id': product_id,
        'name': 'وصف البند في أمر الشراء',
        'product_qty': 1.0,
        'product_uom': 1,                  # 1 = Units
        'price_unit': 15000.0,
        'taxes_id': [(6, 0, [5])],         # 5 = 15% Purchase Tax
    })]
}])
```

### Currencies
| ID | Code |
|----|------|
| 1 | USD |
| 150 | SAR |

### Taxes (Purchase)
| ID | Name | Amount | Use |
|----|------|--------|-----|
| 5 | 15% Purchase Tax | 15% | Standard |
| 153 | 15% | 15% | Purchase |
| 155 | 15% EX | 15% | Purchase exempt? |
| 157 | 0% | 0% | Zero-rated |
| 158 | 0% EXEMPT | 0% | Exempt |

### Payment Terms
| ID | Name |
|----|------|
| 1 | Immediate Payment |
| 2 | 15 Days |
| 4 | 30 Days |
| 8 | 30% Now, Balance 60 Days |

For custom two-installment payments (e.g., 60% advance + 40% on completion), set the `notes` field with terms in HTML rather than using a payment term ID.

### Project to Link POs To
| ID | Name |
|----|------|
| 219 | متحف عسير الإقليمى |

### Known Vendors
| ID | Name | Notes |
|----|------|-------|
| 2640 | شركة نبيل قطب للاستشارات الهندسية | Structural engineering consulting |
| 8156 | ESTS - Electronics Scientific Trading | X-Rite spectrophotometer distributor (Dubai) |
| 8157 | Tajco Scientific | BYK gloss meter distributor (Dubai/Riyadh) |

### Creating RFQs (Draft POs sent to suppliers for quotation)

RFQs are Purchase Orders created in `draft` state — they become confirmed POs when the vendor responds and the PO is approved. Same `purchase.order` model, same creation pattern.

```python
rfq_id = models.execute_kw(db, uid, pwd, 'purchase.order', 'create', [{
    'partner_id': vendor_id,
    'project_id': 219,
    'date_order': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
    'currency_id': 1,          # 1 = USD for imported equipment
    'payment_term_id': 4,      # 30 Days
    'origin': 'RFQ: Replica Project (SC-01)',
    'notes': 'Request for Quotation text...',
    'order_line': [(0, 0, {
        'product_id': product_id,
        'name': 'Item description',
        'product_qty': 1.0,
        'product_uom': 1,      # Units
        'price_unit': 40000.0, # Estimated price
        'taxes_id': [(6, 0, [])],
    })],
}])
```

### Known Products (Service Type)
| ID | Name | Code | Category |
|----|------|------|----------|
| 27618 | أعمال الدراسات والتصميم الإنشائي لمتحف عسير الدولي | — | Subcontracts (640) |
| 27626 | X-Rite Ci64UV Spectrophotometer | CI64-XR-UV | Subcontracts (640) |
| 27627 | BYK micro-TRI-gloss Gloss Meter | BYK-4430 | Subcontracts (640) |


## Update PO After Creation
```python
models.execute_kw(db, uid, pwd, 'purchase.order', 'write', [[po_id], {
    'currency_id': 150,
    'notes': '<p>محتوى محدث</p>',
}])
```

## Read PO Details
```python
po = models.execute_kw(db, uid, pwd, 'purchase.order', 'read', [po_id],
    {'fields': ['id', 'name', 'partner_id', 'amount_total', 'amount_untaxed', 'state', 'currency_id', 'project_id', 'origin']})
```

## Read PO Lines
```python
line_ids = models.execute_kw(db, uid, pwd, 'purchase.order.line', 'search',
    [[['order_id', '=', po_id]]])
lines = models.execute_kw(db, uid, pwd, 'purchase.order.line', 'read', [line_ids],
    {'fields': ['id', 'product_id', 'name', 'product_qty', 'price_unit', 'price_subtotal', 'taxes_id']})
```

## Credential Source
Credentials are NOT hardcoded. Read them programmatically from:
```python
env_file = os.path.expanduser("~/.config/samaya/odoo.env")
env = {}
with open(env_file) as f:
    for line in f:
        if '=' in line and not line.startswith('#'):
            k, v = line.strip().split('=', 1)
            env[k] = v
PWD = env.get('ODOO_API_KEY', '')
```

## Pitfalls
- **XML-RPC domain filters on many2one fields** can cause `TypeError: 'int' object is not subscriptable` in Odoo 18 — pass the id directly as an integer, not in a tuple
- **`product.product` search domain** with certain operators (like `['type', '=', 'service']`) can break in Odoo 18 with `IndexError: string index out of range` — use empty domain `[]` with `limit=N` instead
- **Currency defaults to USD (ID 1)** — always explicitly set `currency_id: 150` for SAR
- **UOM ID 1** = Units (correct for services)
- **`notes` field** accepts HTML — use it for full Arabic payment terms and scope description
- **Creating a vendor (`res.partner`) with `company_type='company'` requires VAT** — the KSA localization enforces `vat` field as mandatory for companies. Provide a placeholder like `'AE123456789'` for UAE suppliers or `'300000000000003'` for KSA suppliers. Use `is_company=True` instead if VAT is unknown, but `company_type='company'` will trigger the constraint.
