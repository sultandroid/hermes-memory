# Samaya Factory — Manufacturing Orders (Odoo MRP)

## Overview

Samaya Factory (project 244) has **502 manufacturing orders** as of Aug 2026:
- 375 done, 38 in progress, 32 draft, 9 confirmed, 26 cancelled
- 926 work orders

## Query pattern

```python
# Count by state
for state in ['draft', 'confirmed', 'progress', 'done', 'cancel']:
    cnt = models.execute_kw(db, uid, password, 'mrp.production',
        'search_count', [[('state', '=', state)]])

# Recent MOs (use keyword order, not positional)
mo_ids = models.execute_kw(db, uid, password, 'mrp.production', 'search',
    [[('id', '!=', 0)]], {'limit': 20, 'order': 'id desc'})
mos = models.execute_kw(db, uid, password, 'mrp.production', 'read',
    [mo_ids], {'fields': ['id', 'name', 'product_id', 'product_qty',
                          'state', 'date_start', 'date_finished', 'origin']})
```

## MO naming convention

| Prefix | Meaning |
|---|---|
| `WH/MO/` | Workshop Manufacturing Order (main factory) |
| `FA/WH/SWH/` | Factory Workshop Sub-Warehouse |
| `FA/WH/MO/` | Factory Workshop MO |

## Key states to monitor

| State | Count | Action |
|---|---|---|
| `progress` | 38 | Active production — check for delays |
| `draft` | 32 | Not yet started — may need confirmation |
| `confirmed` | 9 | Ready to start — assign to workers |
| `to_close` | ~2 | Awaiting closure — check if done |

## Work orders

```python
wo_count = models.execute_kw(db, uid, password, 'mrp.workorder',
    'search_count', [[]])
wo_ids = models.execute_kw(db, uid, password, 'mrp.workorder', 'search',
    [[('id', '!=', 0)]], {'limit': 10, 'order': 'id desc'})
wos = models.execute_kw(db, uid, password, 'mrp.workorder', 'read',
    [wo_ids], {'fields': ['id', 'name', 'production_id', 'operation_id',
                          'state', 'date_start', 'qty_produced', 'qty_producing']})
```

## Common products in production

| Product | MOs | Notes |
|---|---|---|
| Wooden frames / فريمات خشبية | Multiple | Interior display frames |
| Acrylic display units | Multiple | Gift shop displays |
| Metal stands / ستاند حديد | Multiple | Definition stands, light boxes |
| 3D printed items | Multiple | Pearl finish, resin |
| Fabric printing | Multiple | Decotex, sticker printing |
| Showcase units | FA/WH/MO/ | Glass + wood display cases |
| Arch walls | FA/WH/SWH/ | Madina & Macca arch replicas |
