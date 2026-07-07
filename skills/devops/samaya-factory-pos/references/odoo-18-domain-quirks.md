# Odoo 18 Domain Quirks (discovered 2026-07-07)

## 1. `project_id` in search_read domains CRASHES

**Error:** `TypeError: 'int' object is not subscriptable` at `expression.py:261`

**Root cause:** Odoo 18 has a bug with many2one fields (`project_id`) in `search_read` domain filters.

**Workaround — fetch all + Python filter:**
```python
# BROKEN:
pos = call('purchase.order', 'search_read',
    [['project_id','=',244]], {'fields': fields, 'limit': 500})

# WORKS:
all_pos = call('purchase.order', 'search_read', [[]],
    {'fields': fields, 'limit': 2000})
factory_pos = [p for p in all_pos
    if p.get('project_id') and p['project_id'][0] == 244]
```

## 2. `['name','in',list]` domain CRASHES

**Error:** `ValueError: too many values to unpack (expected 3)` at `expression.py:378`

**Workaround — fetch all + Python filter:**
```python
ham_set = {'P01094', 'P01818', ...}
all_pos = call('purchase.order', 'search_read', [[]], {'fields': fields, 'limit': 2000})
filtered = [p for p in all_pos if p['name'] in ham_set]
```

## 3. Complex domains with `&`/`|` operators

Prefer the **two-step pattern**:
```python
ids = call('purchase.order', 'search', [domain], {'limit': 200})
pos = call('purchase.order', 'read', [ids], {'fields': fields})
```

## 4. `search_read` limit is 500 by default

Set to 2000 to catch all POs (1895 total in Samaya Odoo as of Jul 2026).
