# mrp.production — Odoo 18 Query Quirks

Verified against `samayainv.odoo.com` (Odoo 18.0+e).

## Field name differences

| Wrong (doesn't exist) | Correct |
|---|---|
| `date_planned_start` | `date_start` |
| `date_planned_finished` | `date_finished` |

## `product_id` returns `False` (boolean)

When a product is deleted or the field is empty, `product_id` returns `False` instead of a many2one tuple. Always guard:

```python
prod = mo.get('product_id')
if isinstance(prod, bool):
    prod_name = 'N/A'
elif isinstance(prod, (list, tuple)):
    prod_name = prod[1]
else:
    prod_name = str(prod)
```

Same pattern for `user_id`, `origin`, `location_src_id`, and any many2one.

## `search` with `order` — keyword argument required

```python
# Correct
mo_ids = models.execute_kw(db, uid, password, 'mrp.production', 'search',
    [[('id', '!=', 0)]], {'limit': 20, 'order': 'id desc'})

# Wrong — crashes with DatatypeMismatch
mo_ids = models.execute_kw(db, uid, password, 'mrp.production', 'search',
    [[], ['id', 'desc']], {'limit': 20})
```

The second form passes order as a positional argument → Odoo 18 interprets it as part of OFFSET → `psycopg2.errors.DatatypeMismatch: argument of OFFSET must be type bigint, not type text[]`.

## `mrp.workorder.operation_id` — empty string

`operation_id` may return `''` (empty string) instead of `[id, name]` when the work order was created without a specific operation. Guard with `isinstance` check.

## State values

| State | Meaning |
|---|---|
| `draft` | Not yet confirmed |
| `confirmed` | Confirmed, ready to start |
| `progress` | In production |
| `done` | Completed |
| `cancel` | Cancelled |
| `to_close` | Awaiting closure (rare) |
