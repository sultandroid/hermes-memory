# Odoo 18 — Common Model Field Schemas (Samaya)

Verified against `samayainv.odoo.com` (Odoo 18.0+e, peerless-tech-samaya-18-0-18447146).

## ⚠️ Domain Bugs

### project_id in search_read / search

`search_read` with `project_id` in the domain causes `TypeError: 'int' object is not subscriptable` on Odoo 18.0+e. **Workaround:** fetch all records and filter in Python:

```python
all_pos = call('purchase.order', 'search_read', [[]], {'fields': fields, 'limit': 2000})
factory_pos = [p for p in all_pos if p.get('project_id') and p['project_id'][0] == 244]
```

The `search` method has the same bug. Use `search_read` with empty domain `[[]]` and a high limit, then filter in Python.

### 'in' operator with list values

`search_read` with `['name','in',['P01094','P01818']]` causes `ValueError: too many values to unpack (expected 3)`. **Workaround:** fetch all and filter in Python with a set.

## purchase.order

| Field | Type | Notes |
|-------|------|-------|
| `name` | char | PO number (e.g. P02104) |
| `partner_id` | many2one | `[id, 'Vendor Name']` |
| `partner_ref` | char | Vendor's reference/invoice number on the PO |
| `amount_total` | float | Total amount |
| `date_order` | datetime | PO date |
| `date_planned` | datetime | Expected receipt date |
| `state` | selection | draft, sent, to approve, purchase, done, cancel |
| `invoice_status` | selection | no, to invoice, invoiced |
| `project_id` | many2one | `[id, 'Project Name']` — **buggy in domains** |
| `id` | int | Internal ID — use for Odoo hyperlinks |

**Odoo hyperlink pattern:**
```
{ODOO_BASE}/web#id={id}&model=purchase.order
```

## mrp.production (Manufacturing Orders)

| Field | Type | Notes |
|-------|------|-------|
| `name` | char | MO number |
| `product_id` | many2one | `[id, 'Product Name']` |
| `product_qty` | float | Quantity |
| `date_start` | datetime | **NOT** `date_planned_start` |
| `date_finished` | datetime | **NOT** `date_planned_finished` |
| `state` | selection | draft, confirmed, progress, done, cancel |
| `origin` | char | Source document reference |

## hr.leave (Time Off / Leave Requests)

| Field | Type | Notes |
|-------|------|-------|
| `id` | int | Leave record ID |
| `name` | char | Leave reason / notes (often in Arabic) |
| `employee_id` | many2one | `[id, 'Employee Name']` |
| `holiday_status_id` | many2one | `[id, 'Leave Type']` — e.g. "Annual leave", "Sick leave" |
| `date_from` | datetime | Start datetime (in UTC) |
| `date_to` | datetime | End datetime (in UTC) |
| `number_of_days` | float | Duration in days |
| `duration_display` | char | Human-readable duration string |
| `state` | selection | `draft`, `confirm`, `validate` (approved), `refuse`, `cancel` |

**Domain filter by Odoo user:**
```python
[["employee_id.user_id", "=", 151]]  # 151 = Sultan Issa
```

**Employee lookup:**
```python
emp_ids = models.execute_kw(db, uid, pw, "hr.employee", "search",
    [[["user_id", "=", 151]]])
# Returns [975] for Sultan Issa
```

## res.partner

| Field | Type | Notes |
|-------|------|-------|
| `id` | int | Partner ID |
| `name` | char | Partner name |

**Known credit supplier IDs (Samaya Factory):**
- Mada Aljezera: 2427
- Saba Najad: 5603

**Odoo hyperlink pattern:**
```
{ODOO_BASE}/web#id={id}&model=purchase.order
```

## project.project

| Field | Type | Notes |
|-------|------|-------|
| `id` | int | Project ID |
| `name` | char | Project name |
| `partner_id` | many2one | Customer |
| `task_count` | int | Number of tasks |

**Samaya Factory = project 244**
