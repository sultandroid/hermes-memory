# Samaya Odoo — Key Reference IDs

**Instance:** `https://samayainv.odoo.com`
**Database:** `peerless-tech-samaya-18-0-18447146`
**Auth:** `sultan@samayainvest.com` (password in `~/.config/samaya/odoo.env`)

## Reference IDs

| Item | ID | Notes |
|------|----|-------|
| Currency: SAR | 150 | Default is USD (ID 1) — set explicitly |
| Currency: USD | 1 | Odoo default, must override to SAR |
| 15% Purchase Tax | 5 | For PO lines (supplier VAT) |
| Subcontracts category | 640 | Service/consulting procurement |
| UOM: Units | 1 | Standard unit of measure |
| Project: متحف عسير الإقليمى | 219 | Aseer Museum project |
| Vendor: شركة نبيل قطب للاستشارات الهندسية | 2640 | Nabil Qutb Engineering Consulting |
| Vendor: ARSSAD ALKHALIJ | 8193 | Faro 3D laser scanner distributor, Riyadh |

## PO Creation — Verified Working Pattern

### Currency Pitfall
The PO may be created with USD (ID 1) even if `currency_id: 150` is passed in `create`. Always verify and update after creation:

```python
# After create
models.execute_kw(db, uid, pwd, 'purchase.order', 'write', [[po_id], {'currency_id': 150}])
```

### Tax on PO Line
Use `taxes_id: [(6, 0, [5])]` for 15% Purchase Tax (supplier VAT).

### Notes Field
- HTML format with `direction: rtl` for Arabic
- User prefers **pure Arabic text** (no English/Latin characters mixed in Arabic sentences — causes RTL rendering issues)
- Write numbers as Arabic words when in formal documents
- **NEVER use emoji/icons** in task descriptions or notes — plain text only. User explicitly rejected icons. Use plain hyphens (`-`) for bullet lists, not emoji markers.

### Product for Service PO
- `type: 'service'`
- `categ_id: 640` (Subcontracts)
- `uom_id: 1` (Units)
- `uom_po_id: 1`

## Common Product IDs

| Product | ID | Est. Price (SAR) |
|---------|----|------------------|
| Faro Focus Premium 200m | 27782 | 195,000 |
| Faro Blink | 27783 | 140,000 |

## Aseer Museum Task Stages (Samaya Odoo, project 219)

| ID | Name | Sequence |
|----|------|----------|
| 35 | 01 Initiation | 10 |
| 36 | 02 Design Development (DD) Stage | 20 |
| 39 | 03 Procurement | 30 |
| 659 | 04 Off-site Manufacturing | 40 |
| 40 | 05 On-site Work / Execution | 50 |
| 479 | 06 Handover (As-Built & Snagging) | 60 |
| 480 | 07 Cancelled | 70 |

These are **Samaya-specific** — different from the Moqtana stage IDs (9-16) documented in the main SKILL.md.

### Key Parent Tasks (Aseer Museum, project 219)

| Task ID | Name | Stage |
|---------|------|-------|
| 2946 | Projects Plans | DD Stage |
| 2938 | 01 Architecture | DD Stage |
| 2939 | 02 Structural Engineering | DD Stage |
| 2940 | 03 MEP & IT Engineering | DD Stage |
| 2941 | 04 Life Safety | DD Stage |
| 2945 | 00 General | DD Stage |
| 1700 | 01.02 Architectural Package (NRS) | DD Stage |
| 1073 | 03.01 MEP & IT Detailed Design | DD Stage |
| 1072 | 02.01 Structural Scope - Stairs | DD Stage |
| 1308 | BEP | Initiation |

When creating subtasks, use `parent_id` to attach to one of these parent tasks and `stage_id` matching the parent's stage.

### Task Creation — Verified Working Pattern (Samaya)

```python
# Create a subtask under "Projects Plans" (2946) in DD Stage (36)
from datetime import date
today = date.today().strftime('%Y-%m-%d')

task_id = models.execute_kw(db, uid, pw, 'project.task', 'create', [{
    'name': 'Task title — with context',
    'project_id': 219,
    'stage_id': 36,           # DD Stage
    'parent_id': 2946,        # Projects Plans
    'user_ids': [(4, uid)],   # Assign to current user
    'description': f'''<h3>Task created {today}</h3>
<p><b>Context:</b> Description here</p>
<ul><li>Bullet details</li></ul>''',
    'date_deadline': '2026-06-18',
}])
```

Description field accepts HTML. Use `<h3>`, `<p>`, `<ul>/<li>`, `<b>` for structuring task details.

## Task Timesheets — unit_amount is in MINUTES

When creating timesheet entries via `account.analytic.line`, `unit_amount` is in **minutes**, not hours:

```python
# Log 4 hours of work
models.execute_kw(db, uid, pw, 'account.analytic.line', 'create', [{
    'task_id': task_id,
    'name': 'Description of work performed',
    'unit_amount': 240,       # MINUTES! 240 = 4 hours
    'date': '2026-06-27',
    'project_id': project_id,
}])
```

| Hours | unit_amount |
|-------|-------------|
| 30 min | 30 |
| 1 hr | 60 |
| 2 hrs | 120 |
| 4 hrs | 240 |
| 6 hrs | 360 |
| 8 hrs | 480 |

## Partner Creation — Saudi CR/VAT Documents

### Saudi VAT Prefix (CRITICAL PITFALL)
When creating a Saudi company partner, the VAT number from the official certificate **must** be prefixed with `SA`:
- Valid: `SA313137332100003`
- Invalid (triggers Fault 2): `313137332100003`
- Odoo error if wrong: `"The VAT number [X] does not seem to be valid. Note: the expected format is SI12345679"`
- The `l10n_sa` module validates the format; always prepend `SA` to the raw 15-digit VAT number from the certificate.

### Country ID
- Saudi Arabia: `country_id = 192` (not 199 — that's a different country)

### Data mapping from Saudi CR/National Address documents
| Document field | Odoo field | Example |
|----------------|------------|---------|
| الرقم الوطني الموحد (Unified National No.) | `company_registry` | `7050810840` |
| رقم التسجيل الضريبي (VAT Registration No.) | `vat` | `SA313137332100003` (prepend SA) |
| الهاتف (Phone) | `phone` | `0112919494` |
| البريد الإلكتروني (Email) | `email` | `rayan@ole.sa` |
| العنوان الوطني (National Address) — الشارع | `street` | `مكة المكرمة الفرعي` |
| العنوان الوطني — رقم المبنى | `street2` | `مبنى 5917` |
| المدينة | `city` | `الرياض` |
| الرمز البريدي | `zip` | `12813` |

### Contact person pattern
Create a separate `res.partner` record for the contact person:
- `parent_id`: company partner ID
- `type`: `'contact'`
- `name`: person's name
- `phone`: direct contact number
- `function`: job title (e.g., `'Projects Coordinator'`)
- Do NOT set `vat` on the contact — it inherits from the parent company.
- Do NOT set `is_company` on the contact.

### Company partner creation pattern
```python
partner_id = models.execute_kw(db, uid, pw, 'res.partner', 'create', [{
    'name': 'شركة مقتنى للمتاحف والاستشارات',
    'vat': 'SA313137332100003',
    'company_registry': '7050810840',
    'phone': '0112919494',
    'email': 'rayan@ole.sa',
    'street': 'مكة المكرمة الفرعي',
    'street2': 'مبنى 5917',
    'city': 'الرياض',
    'zip': '12813',
    'country_id': 192,
    'is_company': True,
    'customer_rank': 1,
    # or customer_rank: 0 for vendors
}])

contact_id = models.execute_kw(db, uid, pw, 'res.partner', 'create', [{
    'name': 'Abdullah Alshojaa',
    'phone': '0501537162',
    'parent_id': partner_id,
    'type': 'contact',
    'function': 'Projects Coordinator',
}])
```

### Verification
```python
models.execute_kw(db, uid, pw, 'res.partner', 'search_read',
    [[['id', 'in', [partner_id, contact_id]]]],
    {'fields': ['id', 'name', 'vat', 'phone', 'email', 'parent_id', 'type']})
```

### Known partner IDs (created via this pattern)
| Partner | ID | Contact | Contact ID |
|---------|----|---------|------------|
| شركة مقتنى للمتاحف والاستشارات | 8304 | Abdullah Alshojaa | 8305 |

## SSL Certificate Issue (macOS)

XML-RPC to `https://samayainv.odoo.com` may fail with `SSL: CERTIFICATE_VERIFY_FAILED` because macOS Python can't find system root certs. Fix:

```python
import ssl, xmlrpc.client
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE
common = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/common', context=ctx)
models = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/object', context=ctx)
```
