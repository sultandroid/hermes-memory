# Odoo 18 Domain Syntax Pitfall — `project_id` + `in` operator

## The Bug
Combining `project_id` in a domain with `['invoice_status','in',['to invoice','no']]` crashes Odoo 18 with:
```
TypeError: 'int' object is not subscriptable
  File "/home/odoo/src/odoo/odoo/osv/expression.py", line 261
    elif token[1] == 'in' and not (isinstance(token[2], Query) or token[2]):
```

## Root Cause
Odoo's `expression.py` mis-parses the domain when `project_id` (a many2one field returning `[id, name]` tuple) is combined with an `in` operator on another field. The `project_id` value `[244, 'Samaya Factory']` gets confused with a domain token.

## Workarounds

### Workaround 1: search() + read() in two steps
```python
ids = call('purchase.order', 'search', [['project_id','=',244]], {'limit': 500})
all_pos = call('purchase.order', 'read', [ids], {'fields': fields})
unpaid = [p for p in all_pos if p['state']=='purchase' and p.get('invoice_status') in ('to invoice','no')]
```

### Workaround 2: Fetch all, filter in Python
```python
all_pos = call('purchase.order', 'search_read', [[]], {'fields': fields, 'limit': 500})
factory_pos = [p for p in all_pos if p.get('project_id') and p['project_id'][0] == 244]
```

## Affected Models
- `purchase.order` with `project_id` in domain
- Likely affects any many2one field combined with `in` operator in the same domain on Odoo 18

## Verified On
- Odoo 18.0+e (peerless-tech-samaya-18-0-18447146)
- Python 3.13 XML-RPC client
