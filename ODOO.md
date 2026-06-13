# ODOO — Connection & Patterns

## Instance: Samaya (DEFAULT)

| Field | Value |
|-------|-------|
| URL | https://samayainv.odoo.com |
| Database | peerless-tech-samaya-18-0-18447146 |
| User | sultan@samayainvest.com |
| API Key | `~/.config/samaya/odoo.env` → `ODOO_API_KEY=***` |
| Odoo Version | 18.0+e |

## XML-RPC Connection

```python
import xmlrpc.client, ssl, os

ctx = ssl._create_unverified_context()
transport = xmlrpc.client.SafeTransport(context=ctx)

URL = 'https://samayainv.odoo.com'
DB = 'peerless-tech-samaya-18-0-18447146'
LOGIN = 'sultan@samayainvest.com'

with open(os.path.expanduser('~/.config/samaya/odoo.env')) as f:
    for line in f:
        if 'ODOO_API_KEY' in line and '=' in line:
            PWD = line.split('=', 1)[1].strip()

common = xmlrpc.client.ServerProxy(URL + '/xmlrpc/2/common', transport=transport)
uid = common.authenticate(DB, LOGIN, PWD, {})
models = xmlrpc.client.ServerProxy(URL + '/xmlrpc/2/object', transport=transport)
```

## Task Creation Template

```python
task_id = models.execute_kw(DB, uid, PWD, 'project.task', 'create', [{
    'name': 'DOC-CODE — Title',
    'project_id': 219,
    'stage_id': 36,
    'parent_id': PACKAGE_ID or False,
    'user_ids': [(4, USER_ID)],
    'tag_ids': [(4, TAG_ID)],
    'date_assign': str(date.today()),
    'date_deadline': str(date.today()),
    'state': '01_in_progress',
    'progress': 0.5,                # 0.0-1.0
    'display_mark_as_done_primary': False,
    'description': '<h3>Title</h3><p><b>Context:</b>...</p>',
}])
```

## PO Creation

### Key IDs
| Item | ID |
|------|----|
| SAR Currency | 150 |
| USD Currency | 1 |
| 15% Purchase Tax | 5 |
| Subcontracts Category | 640 |
| UOM Units | 1 |
| Vendor: نبيل قطب (Nabil Qutb) | 2640 |
| Vendor: ARSSAD ALKHALIJ | 8193 |

```python
# Create product
product_id = models.execute_kw(DB, uid, PWD, 'product.product', 'create', [{
    'name': 'اسم المنتج', 'type': 'service',
    'categ_id': 640, 'uom_id': 1, 'uom_po_id': 1,
}])

# Create PO
po_id = models.execute_kw(DB, uid, PWD, 'purchase.order', 'create', [{
    'partner_id': VENDOR_ID, 'project_id': 219,
    'currency_id': 150,
    'payment_term_id': 4,
    'order_line': [(0, 0, {
        'product_id': product_id, 'product_qty': 1.0,
        'price_unit': 15000.0, 'taxes_id': [(6, 0, [5])],
    })]
}])

# Fix currency (defaults to USD!)
models.execute_kw(DB, uid, PWD, 'purchase.order', 'write',
    [[po_id], {'currency_id': 150}])
```

## Search Patterns

```python
# Find tasks
tasks = models.execute_kw(DB, uid, PWD, 'project.task', 'search',
    [[['project_id', '=', 219], ['name', '=ilike', '%PL-0057%']]])

# All packages
pkgs = models.execute_kw(DB, uid, PWD, 'project.task', 'search_read',
    [[['project_id', '=', 219], ['parent_id', '=', False]]],
    {'fields': ['id', 'name', 'stage_id', 'state', 'progress']})

# Find users
users = models.execute_kw(DB, uid, PWD, 'res.users', 'search_read',
    [[['login', '=ilike', '%hesham%']]],
    {'fields': ['id', 'name', 'login']})
```

## ⚠️ Critical Pitfalls

1. **Aseer (219) is on Samaya Odoo, NOT Moqtana** — never fallback
2. **Dates REQUIRED on every task** — `date_assign` + `date_deadline`
3. **Assignee = `user_ids`** (many2many) with `[(4, uid)]`, NOT `user_id`
4. **Progress = 0.0–1.0**, NOT 0–100
5. **Always search with `=ilike` first** — prevent duplicates
6. **SOW descriptions = exact wording** — no paraphrasing in registers
7. **Never reference /tmp paths** — copy to project folder first
8. **Sultan = DD only**, Samir = site/proc, Hani = purchasing — assign correctly
9. **PO defaults to USD** — always verify and set to SAR (150)
10. **SSL bypass needed on macOS** — `ssl._create_unverified_context()`
