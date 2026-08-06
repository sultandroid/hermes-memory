# MO Monitoring Patterns — Samaya Factory

## Context
Samaya Factory uses Odoo for manufacturing orders (MRP). Most products are non-standard (custom), so BoM usage is low (~12%). Material consumption is recorded manually on each MO. This reference covers monitoring compliance.

## Key Models & Fields

### mrp.production
| Field | Purpose |
|-------|---------|
| `move_raw_ids` | one2many — raw material stock moves. Empty = no materials recorded |
| `bom_id` | many2one — linked BoM. False = no BoM |
| `state` | draft → confirmed → progress → to_close → done |
| `project_id` | many2one — `[id, 'Project Name']` |

### stock.move (raw material consumption)
```python
# Get consumption moves for an MO
moves = models.execute_kw(db, uid, key, 'stock.move', 'search_read', [
    [('raw_material_production_id', '=', mo_id), ('state', '=', 'done')]
], {'fields': ['product_id', 'product_qty', 'date']})
```

## Detection: MOs Without Material Recording

```python
yesterday = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
mo_ids = models.execute_kw(db, uid, key, 'mrp.production', 'search', [
    [('state', 'in', ['progress', 'confirmed']),
     ('create_date', '<', yesterday)]
])
mos = models.execute_kw(db, uid, key, 'mrp.production', 'read', [mo_ids],
    {'fields': ['name', 'product_id', 'state', 'move_raw_ids']})
no_mat = [m for m in mos if not m.get('move_raw_ids')]
```

## Posting Chatter Notes (with dedup)

Delete old notes from same author first, then post new:

```python
# Delete old notes from this author
old_msgs = models.execute_kw(db, uid, key, 'mail.message', 'search', [
    [('model', '=', 'mrp.production'), ('res_id', '=', mo_id),
     ('author_id', '=', 151), ('message_type', '=', 'comment')]
])
for mid in old_msgs:
    models.execute_kw(db, uid, key, 'mail.message', 'unlink', [[mid]])

# Post new note
models.execute_kw(db, uid, key, 'mrp.production', 'message_post', [mo_id], {
    'body': '<p>⚠️ تذكير: لم يتم تسجيل المواد الخاصة بأمر التصنيع</p>',
    'message_type': 'comment',
    'subtype_xmlid': 'mail.mt_comment'
})
```

## Blocking MO Close

MOs in `to_close` state without `move_raw_ids` should be flagged:

```python
to_close = models.execute_kw(db, uid, key, 'mrp.production', 'search', [
    [('state', '=', 'to_close')]
])
mos = models.execute_kw(db, uid, key, 'mrp.production', 'read', [to_close],
    {'fields': ['name', 'move_raw_ids']})
blocked = [m for m in mos if not m.get('move_raw_ids')]
```

## BoM Creation Threshold

Products ordered/repeated **3+ times** → create a BoM. Check via:

```python
# Count MOs per product
mos = models.execute_kw(db, uid, key, 'mrp.production', 'search_read', [[]],
    {'fields': ['product_id'], 'limit': 2000})
from collections import Counter
prod_counts = Counter(m['product_id'][0] for m in mos if m.get('product_id'))
repeated = {pid: count for pid, count in prod_counts.items() if count >= 3}
```

## Stock Health Checks

### Negative stock detection
```python
quants = models.execute_kw(db, uid, key, 'stock.quant', 'search_read', [
    [('location_id', 'in', factory_locs)]
], {'fields': ['product_id', 'quantity']})
neg = [q for q in quants if q['quantity'] < 0]
```

### Near-empty stock (low qty + recent movement)
```python
moved_ids = set(m['product_id'][0] for m in recent_moves)
low = [p for p in products 
       if 0 < quant_by_prod.get(p['id'], 0) < 5 
       and p['id'] in moved_ids]
```

## Working Hours
- **Days:** Saturday → Thursday
- **Hours:** 08:00 → 17:00
- Cron schedule: `0 8 * * 6-4` (Sat=6, Thu=4 in cron)

## Weekly Report (Word)
Generate via python-docx. Sections:
1. New MOs this week (with material recording status)
2. Completed MOs this week
3. Violations (MOs without materials, without BoM)
4. Stock alerts (negative, near-empty)
5. New POs received
