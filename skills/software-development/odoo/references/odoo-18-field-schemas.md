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

### 'not in' operator crashes

`[['state','not in',['draft','cancel']]]` causes `TypeError: BaseModel.search_read() got multiple values for argument 'fields'`. Use positive list: `[['state','in',['purchase','done']]]`.

### search_read domain format

Must wrap domain in an extra list: `[domain]` not `domain`. Correct:
```python
models.execute_kw(db, uid, apikey, model, 'search_read', [domain], {'fields': fields})
```

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
| `receipt_status` | selection | no, pending, full, not_received |
| `project_id` | many2one | `[id, 'Project Name']` — **buggy in domains** |
| `invoice_ids` | one2many | `[id, ...]` — linked vendor bill IDs |
| `message_ids` | one2many | `[id, ...]` — chatter message IDs |
| `id` | int | Internal ID — use for Odoo hyperlinks |

**Odoo hyperlink pattern:**
```
{ODOO_BASE}/web#id={id}&model=purchase.order
```

## account.move (Vendor Bills / Invoices)

| Field | Type | Notes |
|-------|------|-------|
| `name` | char | Bill number (e.g. BILL/2026/07/0013) |
| `amount_total` | float | Total bill amount |
| `amount_residual` | float | Remaining unpaid amount |
| `payment_state` | selection | not_paid, in_payment, paid, partial, reversed |
| `state` | selection | draft, posted, cancel |
| `invoice_date` | date | Bill date |
| `move_type` | selection | in_invoice (vendor bill), in_refund, out_invoice, etc. |

**Reading bills linked to a PO:**
```python
# Get invoice_ids from PO
inv_ids = po.get('invoice_ids', [])
for inv_id in inv_ids:
    b = models.execute_kw(db, uid, apikey,
        'account.move', 'read', [inv_id],
        {'fields': ['name','amount_total','amount_residual','payment_state','state']})
```

**Payment detection logic:**
```python
if b.get('state') == 'posted' and abs(b.get('amount_residual', 0)) < 0.01:
    paid = True  # Fully paid
elif b.get('state') == 'posted' and b.get('amount_residual', 0) < b.get('amount_total', 0):
    partial = True  # Partially paid
elif b.get('state') == 'draft':
    draft_bill = True  # Bill created but not posted
```

## mail.message (Chatter)

| Field | Type | Notes |
|-------|------|-------|
| `body` | html | Message body (HTML, strip tags to read) |
| `date` | datetime | When posted |
| `author_id` | many2one | `[id, 'Author Name']` |
| `model` | char | Model name (e.g. 'purchase.order') |
| `res_id` | int | Record ID this message belongs to |
| `message_type` | selection | comment, email, notification, etc. |
| `subtype_id` | many2one | `[id, 'Subtype Name']` — e.g. note, discussion |

**Reading chatter for a PO:**
```python
# Method 1: search_read (works for simple queries)
msgs = models.execute_kw(db, uid, apikey,
    'mail.message', 'search_read',
    [['model','=','purchase.order'], ['res_id','=',po_id]],
    {'fields': ['body', 'date'], 'limit': 20})

# Method 2: via message_ids (more reliable)
po_full = models.execute_kw(db, uid, apikey,
    'purchase.order', 'read', [po_id],
    {'fields': ['name', 'message_ids']})
msg_ids = po_full[0].get('message_ids', [])
for mid in msg_ids[:15]:
    msg = models.execute_kw(db, uid, apikey,
        'mail.message', 'read', [mid],
        {'fields': ['body', 'date']})
```

**Stripping HTML from body:**
```python
import re
clean = re.sub(r'<[^>]+>', '', body).strip()
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

## project.task

| Field | Type | Notes |
|-------|------|-------|
| `id` | int | Task ID |
| `name` | char | Task name |
| `parent_id` | many2one | `[id, 'Parent Name']` or `False` for top-level tasks |
| `stage_id` | many2one | `[id, 'Stage Name']` — use `project.task.type` model to get stage list |
| `progress` | float | 0.0–1.0 (0.0 = not started, 1.0 = completed) |
| `date_deadline` | datetime | **Includes time component** — always strip to `[:10]` before parsing |
| `date_assign` | datetime | Assignment date |
| `state` | selection | `01_in_progress`, `1_done`, `1_canceled`, `03_approved`, `02_changes_requested`, `04_waiting_normal` |
| `user_ids` | many2many | Array of user IDs assigned |
| `description` | html | Task description (HTML, strip tags) |
| `create_date` | datetime | Creation timestamp |
| `write_date` | datetime | Last modification timestamp |
| `project_id` | many2one | `[id, 'Project Name']` |

**Querying all tasks for a project:**
```python
tasks = models.execute_kw(db, uid, apikey, 'project.task', 'search_read',
    [[('project_id', '=', PROJECT_ID)],
     ['id', 'name', 'stage_id', 'progress', 'date_deadline', 'state', 'parent_id']])
```

**Getting stages for a project:**
```python
stages = models.execute_kw(db, uid, apikey, 'project.task.type', 'search_read',
    [[('project_ids', '=', PROJECT_ID)], ['id', 'name']])
stage_map = {s['id']: s['name'] for s in stages}
```

**Deadline parsing (time component stripping):**
```python
from datetime import datetime, date
if t['date_deadline']:
    dl_str = t['date_deadline'][:10]  # strip time
    dl = datetime.strptime(dl_str, '%Y-%m-%d').date()
    if dl < date.today():
        # overdue
```

**Progress classification:**
```python
completed = sum(1 for t in tasks if t['progress'] >= 1.0)
in_progress = sum(1 for t in tasks if 0 < t['progress'] < 1.0)
not_started = sum(1 for t in tasks if t['progress'] == 0.0)
```

**Getting latest modification timestamp:**
```python
latest = models.execute_kw(db, uid, apikey, 'project.task', 'search_read',
    [[('project_id', '=', PROJECT_ID)], ['write_date']],
    {'order': 'write_date desc', 'limit': 1})
```

**Tasks modified after a cutoff:**
```python
modified = models.execute_kw(db, uid, apikey, 'project.task', 'search_read',
    [[('project_id', '=', PROJECT_ID), ('write_date', '>', cutoff_date)],
     ['id', 'name', 'write_date', 'progress', 'stage_id']],
    {'order': 'write_date desc'})
```

## project.task.type (Stages)

| Field | Type | Notes |
|-------|------|-------|
| `id` | int | Stage ID |
| `name` | char | Stage name (e.g. "01 Initiation", "02 Design Development (DD) Stage") |
| `project_ids` | many2many | Projects this stage is used in |

## project.project

| Field | Type | Notes |
|-------|------|-------|
| `id` | int | Project ID |
| `name` | char | Project name |
| `partner_id` | many2one | Customer |
| `task_count` | int | Number of tasks |

**Samaya Factory = project 244**
**Aseer Museum = project 219**
