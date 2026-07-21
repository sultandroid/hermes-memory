#!/usr/bin/env python3
"""Find new POs created in last 3 days for Factory/Workshop."""
import os, sys, xmlrpc.client, ssl
from datetime import date, timedelta

ENV_PATH = os.path.expanduser('~/.config/samaya/odoo.env')
env = {}
with open(ENV_PATH) as f:
    for line in f:
        line = line.strip()
        if not line or line.startswith('#') or '=' not in line: continue
        k, v = line.split('=', 1)
        env[k.strip()] = v.strip()

ctx = ssl._create_unverified_context()
common = xmlrpc.client.ServerProxy(f'{env["ODOO_URL"]}/xmlrpc/2/common', context=ctx)
uid = common.authenticate(env['ODOO_DB'], env['ODOO_USER'], env['ODOO_API_KEY'], {})
print(f'uid={uid}', file=sys.stderr)
models = xmlrpc.client.ServerProxy(f'{env["ODOO_URL"]}/xmlrpc/2/object', context=ctx)

three_days_ago = (date.today() - timedelta(days=3)).isoformat()
domain = [['date_order', '>=', three_days_ago]]
fields = ['name','partner_id','amount_total','date_order','state','receipt_status','invoice_status','project_id']
rows = models.execute_kw(env['ODOO_DB'], uid, env['ODOO_API_KEY'],
    'purchase.order', 'search_read', [domain], {'fields': fields, 'limit': 50})

workshop_vendors = ['ورشة','مفاهيم خشبية','نجارة','دهان','فايبر','حدادة','تنجيد',
    'اخشاب','قشرة','المنشار','النجارة','مصنع','Sigma Machines','AMAZON ONLINE',
    'Outsorce Labor','Expenses Statement','Bodour Abdul Rehman','ندرة','امداد التوريد',
    'الشعبية الاولى','انظمة الرنين','التوتنجي','جي 4 تيك','اثمان العاصمه',
    'صروح الخالدية','الاخشاب الفاخرة','خليجنا','جفن الالوان','الواح الخليج',
    'آرت آند ستيشنري','اعمال الابتكار','عبدالعزيز رشيد']

def is_workshop(po):
    p = po.get('partner_id', ['', '']); pn = p[1] if isinstance(p, list) and len(p) > 1 else ''
    return any(kw.lower() in pn.lower() for kw in workshop_vendors)

relevant = []
for po in rows:
    pid = po.get('project_id')
    is_f = pid and isinstance(pid, list) and len(pid) >= 1 and pid[0] == 244
    is_w = is_workshop(po)
    if is_f or is_w:
        pname = po.get('partner_id', ['',''])[1] if po.get('partner_id') else ''
        relevant.append({'po': po['name'], 'vendor': pname, 'amount': po.get('amount_total',0), 'date': str(po.get('date_order',''))[:10], 'state': po.get('state',''), 'src': 'F' if is_f else 'W'})

relevant.sort(key=lambda r: r['date'])
print(f'\n=== NEW POs (last 3 days) ===')
print(f'{"PO #":<12} {"Vendor":<35} {"Amount":>10} {"Date":<12} {"State":<12} {"Src":<4}')
print('-' * 90)
for r in relevant:
    print(f'{r["po"]:<12} {r["vendor"][:34]:<35} {r["amount"]:>10,.2f} {r["date"]:<12} {r["state"]:<12} {r["src"]:<4}')
total = sum(r['amount'] for r in relevant)
print(f'\nTotal: {len(relevant)} POs = {total:,.2f} SAR')
