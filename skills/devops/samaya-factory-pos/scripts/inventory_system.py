#!/usr/bin/env python3
"""
نظام متابعة مخزون المواد الأساسية — مصنع سمايا
يجري يومياً: يسحب POs المستلمة + MOs المنصرفة + الرصيد الحالي
ويحسب الرصيد لكل مادة خام

المستهلكات: توزع شهرياً على MOs المفتوحة/المنجزة

Usage:
  SSL_CERT_FILE=$(python3 -c "import certifi; print(certifi.where())") python3 inventory_system.py
"""
import os, xmlrpc.client, ssl, json, datetime
from collections import defaultdict

ENV_PATH = os.path.expanduser('~/.config/samaya/odoo.env')
env = {}
with open(ENV_PATH) as f:
    for line in f:
        line = line.strip()
        if not line or line.startswith('#') or '=' not in line: continue
        k, v = line.split('=', 1)
        env[k.strip()] = v.strip()

url = env['ODOO_URL']
db = env['ODOO_DB']
user = env['ODOO_USER']
key = env['ODOO_API_KEY']
ctx = ssl.create_default_context()
common = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/common', context=ctx)
uid = common.authenticate(db, user, key, {})
models = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/object', context=ctx)

# === 1. Raw Materials Categories ===
raw_cat_ids = models.execute_kw(db, uid, key, 'product.category', 'search', [
    [('name', 'in', ['Raw materials', 'Raw Materials'])]
])
all_cats = models.execute_kw(db, uid, key, 'product.category', 'search_read', [[]], 
    {'fields': ['id', 'name', 'parent_id']})

def get_all_child_ids(cat_id):
    ids = [cat_id]
    for c in all_cats:
        if c['parent_id'] and c['parent_id'][0] == cat_id:
            ids.extend(get_all_child_ids(c['id']))
    return ids

raw_cat_tree = []
for rc in raw_cat_ids:
    raw_cat_tree.extend(get_all_child_ids(rc))
raw_cat_tree = list(set(raw_cat_tree))

# === 2. Products ===
products = models.execute_kw(db, uid, key, 'product.product', 'search_read', [
    [('categ_id', 'in', raw_cat_tree)]
], {'fields': ['id', 'display_name', 'default_code', 'categ_id', 'qty_available', 'uom_id']})
prod_map = {p['id']: p for p in products}

# === 3. Stock Quants ===
factory_locs = [45, 46, 47, 51, 77, 78]
quants = models.execute_kw(db, uid, key, 'stock.quant', 'search_read', [
    [('product_id', 'in', [p['id'] for p in products]), ('location_id', 'in', factory_locs)]
], {'fields': ['product_id', 'location_id', 'quantity', 'reserved_quantity']})

quant_by_prod = defaultdict(float)
reserved_by_prod = defaultdict(float)
for q in quants:
    pid = q['product_id'][0]
    quant_by_prod[pid] += q['quantity'] or 0
    reserved_by_prod[pid] += q['reserved_quantity'] or 0

# === 4. Stock Moves (12 months) ===
date_from = (datetime.datetime.now() - datetime.timedelta(days=365)).strftime('%Y-%m-%d')
moves = models.execute_kw(db, uid, key, 'stock.move', 'search_read', [
    [('product_id', 'in', [p['id'] for p in products]), ('date', '>=', date_from),
     ('state', '=', 'done')]
], {'fields': ['product_id', 'product_qty', 'location_id', 'location_dest_id', 
               'raw_material_production_id', 'date', 'reference'],
    'limit': 10000, 'order': 'date DESC'})

incoming_by_prod = defaultdict(float)
outgoing_by_prod = defaultdict(float)
outgoing_by_mo = defaultdict(lambda: defaultdict(float))

for m in moves:
    pid = m['product_id'][0]
    qty = m['product_qty']
    loc_from = m['location_id'][0] if m['location_id'] else 0
    loc_to = m['location_dest_id'][0] if m['location_dest_id'] else 0
    mo_id = m['raw_material_production_id'][0] if m['raw_material_production_id'] else 0
    
    if loc_to in factory_locs:
        incoming_by_prod[pid] += qty
    elif loc_from in factory_locs and loc_to in [15, 98]:
        outgoing_by_prod[pid] += qty
        if mo_id:
            outgoing_by_mo[mo_id][pid] += qty

# === 5. Build Report ===
report = []
for p in products:
    pid = p['id']
    on_hand = quant_by_prod.get(pid, 0)
    reserved = reserved_by_prod.get(pid, 0)
    incoming = incoming_by_prod.get(pid, 0)
    outgoing = outgoing_by_prod.get(pid, 0)
    available = on_hand - reserved
    
    report.append({
        'id': pid,
        'code': p.get('default_code') or '',
        'name': p['display_name'],
        'category': p['categ_id'][1] if p['categ_id'] else '',
        'uom': p['uom_id'][1] if p['uom_id'] else '',
        'on_hand': on_hand,
        'reserved': reserved,
        'available': available,
        'incoming_12m': incoming,
        'outgoing_12m': outgoing,
        'monthly_avg_out': round(outgoing / 12, 2),
        'coverage_days': round((on_hand / (outgoing / 365)) if outgoing > 0 else 999, 1)
    })

# === 6. Open MOs ===
mo_ids = models.execute_kw(db, uid, key, 'mrp.production', 'search', [
    [('state', 'in', ['progress', 'confirmed', 'draft'])]
])
mos = models.execute_kw(db, uid, key, 'mrp.production', 'read', [mo_ids], 
    {'fields': ['name', 'product_id', 'product_qty', 'state', 'date_start', 'date_finished']})

mo_summary = []
for mo in mos:
    mo_name = mo['name']
    mo_prod = mo['product_id'][1] if mo['product_id'] else ''
    mo_qty = mo.get('product_qty', 0)
    mo_state = mo.get('state', '')
    mo_date = (mo.get('date_start') or '')[:10]
    materials = outgoing_by_mo.get(mo['id'], {})
    mat_list = []
    for pid, qty in sorted(materials.items(), key=lambda x: -x[1]):
        prod = prod_map.get(pid, {})
        mat_list.append(f'{prod.get("display_name","?")[:40]} × {qty:.1f}')
    mo_summary.append({
        'name': mo_name, 'product': mo_prod, 'qty': mo_qty,
        'state': mo_state, 'date': mo_date, 'materials': mat_list
    })

# === 7. Consumables Distribution ===
consumable_cats = [220, 221, 222, 223, 224, 225, 226, 353, 354, 355, 396, 397, 398, 399, 400]
consumable_products = models.execute_kw(db, uid, key, 'product.product', 'search_read', [
    [('categ_id', 'in', consumable_cats)]
], {'fields': ['id', 'display_name']})
cons_prod_ids = [p['id'] for p in consumable_products]

cons_moves = models.execute_kw(db, uid, key, 'stock.move', 'search_read', [
    [('product_id', 'in', cons_prod_ids), ('date', '>=', date_from), ('state', '=', 'done'),
     ('location_dest_id', 'in', factory_locs)]
], {'fields': ['product_id', 'product_qty', 'date', 'reference'], 'limit': 5000})

cons_by_month = defaultdict(float)
for m in cons_moves:
    cons_by_month[m['date'][:7]] += m['product_qty']

mos_done = models.execute_kw(db, uid, key, 'mrp.production', 'search_read', [
    [('state', '=', 'done'), ('date_finished', '>=', date_from)]
], {'fields': ['name', 'date_finished']})
mos_by_month = defaultdict(int)
for m in mos_done:
    mos_by_month[m['date_finished'][:7]] += 1

# === 8. Save ===
output = {
    'generated': datetime.datetime.now().strftime('%Y-%m-%d %H:%M'),
    'summary': {
        'total_raw_materials': len(report),
        'total_on_hand': sum(r['on_hand'] for r in report),
        'total_available': sum(r['available'] for r in report),
        'total_incoming_12m': sum(r['incoming_12m'] for r in report),
        'total_outgoing_12m': sum(r['outgoing_12m'] for r in report),
        'open_mos': len(mo_summary),
    },
    'materials': [r for r in report if r['on_hand'] > 0 or r['incoming_12m'] > 0],
    'zero_stock': [r for r in report if r['on_hand'] == 0 and r['incoming_12m'] > 0],
    'negative_stock': [r for r in report if r['on_hand'] < 0],
    'open_mos': mo_summary,
    'consumables_by_month': dict(cons_by_month),
    'mos_by_month': dict(mos_by_month),
}

with open('/Users/mohamedessa/.hermes/tmp/inventory_report.json', 'w') as f:
    json.dump(output, f, indent=2, ensure_ascii=False)

# Print summary
s = output['summary']
print(f'مواد خام: {s["total_raw_materials"]}')
print(f'رصيد حالي: {s["total_on_hand"]:.0f}')
print(f'متاح للصرف: {s["total_available"]:.0f}')
print(f'أوامر تصنيع مفتوحة: {s["open_mos"]}')
print(f'مواد نافدة: {len(output["zero_stock"])}')
print(f'مواد برصيد سالب: {len(output["negative_stock"])}')
print(f'محفوظ في inventory_report.json')
