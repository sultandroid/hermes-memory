#!/usr/bin/env python3
"""
Samaya Factory — Daily Manager Report generator (data sections).
Fetches MRP state counts + factory POs from Odoo, and Raoof emails from Outlook.
Outputs the data sections (1-3) of the daily report to stdout as markdown.
The cron agent appends section 4 (decisions) and saves the full report.

Usage: python3 factory_daily_report.py
"""
import os, ssl, xmlrpc.client, sqlite3, json
from datetime import datetime, timedelta
from collections import Counter, defaultdict

ENV_PATH = os.path.expanduser('~/.config/samaya/odoo.env')
env = {}
with open(ENV_PATH) as f:
    for line in f:
        line = line.strip()
        if not line or line.startswith('#') or '=' not in line:
            continue
        k, v = line.split('=', 1)
        env[k.strip()] = v.strip()

OUTLOOK = os.path.expanduser(
    '~/Library/Group Containers/UBF8T346G9.Office/Outlook/'
    'Outlook 15 Profiles/Main Profile/Data/Outlook.sqlite')

# Factory project IDs (from fetch_factory_pos_v2.py)
FACTORY_PROJECT_IDS = {161, 244, 302, 307, 315}
FACTORY_SUPPLIER_IDS = {2427, 5603, 5606, 5608, 5677, 5744, 5749, 5750,
                        6948, 6949, 6952, 6964, 6994, 7106, 7161, 7163,
                        7167, 7169, 7207, 7252, 7260, 7268, 7290, 7291,
                        7306, 7323, 7328, 7330, 7333, 7334, 7335, 7390,
                        7429, 7502, 7514, 7531, 7547, 7553, 7568, 7597,
                        7598, 7639, 7653, 7663, 7709, 7804, 7806, 7817,
                        7856, 7859, 7870, 7871, 7893, 7894, 7953, 7961,
                        7968, 8037, 8039, 8120, 8121, 8122, 8152, 8168,
                        8170, 8192, 8200, 8212, 8234, 8237, 8288, 8291,
                        8294, 8311, 8317, 8319, 8354, 8442, 8444, 8452}

STATE_AR = {'draft': 'مسودة', 'sent': 'مرسل', 'to approve': 'بانتظار الموافقة',
            'purchase': 'مؤكد (مفتوح)', 'done': 'مستلم', 'cancel': 'ملغي'}
MRP_STATE_AR = {'done': 'مكتمل (Done)', 'progress': 'قيد التنفيذ (Progress)',
                'draft': 'مسودة (Draft)', 'to_close': 'بانتظار الإغلاق (To Close)',
                'cancel': 'ملغي (Cancel)', 'confirmed': 'مؤكد (Confirmed)'}

today = datetime.now()
today_str = today.strftime('%Y-%m-%d')
today_ar = today.strftime('%d %B %Y')


def connect():
    ctx = ssl._create_unverified_context()
    common = xmlrpc.client.ServerProxy(f'{env["ODOO_URL"]}/xmlrpc/2/common', context=ctx)
    uid = common.authenticate(env['ODOO_DB'], env['ODOO_USER'], env['ODOO_API_KEY'], {})
    models = xmlrpc.client.ServerProxy(f'{env["ODOO_URL"]}/xmlrpc/2/object', context=ctx)
    return uid, models


def fetch_mrp(models, uid):
    mos = models.execute_kw(env['ODOO_DB'], uid, env['ODOO_API_KEY'],
                            'mrp.production', 'search_read', [[]],
                            {'fields': ['state'], 'limit': 2000})
    return dict(Counter(m['state'] for m in mos))


def fetch_pos(models, uid):
    po_fields = ['name', 'partner_id', 'amount_total', 'date_order', 'state',
                 'project_id', 'invoice_status', 'receipt_status', 'partner_ref',
                 'date_planned', 'create_date']
    all_pos = models.execute_kw(env['ODOO_DB'], uid, env['ODOO_API_KEY'],
                                'purchase.order', 'search_read', [[]],
                                {'fields': po_fields, 'limit': 5000,
                                 'order': 'date_order desc'})
    factory_pos, supplier_pos = [], []
    for po in all_pos:
        pid = po.get('project_id')
        proj_id = pid[0] if pid and isinstance(pid, list) and len(pid) >= 1 else None
        partner = po.get('partner_id')
        partner_id = partner[0] if partner and isinstance(partner, list) and len(partner) >= 1 else None
        if proj_id in FACTORY_PROJECT_IDS:
            factory_pos.append(po)
        elif partner_id in FACTORY_SUPPLIER_IDS:
            supplier_pos.append(po)
    return factory_pos, supplier_pos


def fetch_raoof_emails(days=30):
    conn = sqlite3.connect(OUTLOOK)
    cur = conn.cursor()
    since = int((datetime.now() - timedelta(days=days)).timestamp())
    cur.execute("""
        SELECT datetime(Message_TimeReceived,'unixepoch','localtime'),
               Message_NormalizedSubject, substr(Message_Preview,1,120)
        FROM Mail
        WHERE Message_SenderList LIKE '%Raoof%'
          AND Message_TimeReceived > ?
        ORDER BY Message_TimeReceived DESC
    """, (since,))
    rows = cur.fetchall()
    conn.close()
    return rows


def main():
    uid, models = connect()
    mrp = fetch_mrp(models, uid)
    factory_pos, supplier_pos = fetch_pos(models, uid)

    # --- Section 1: MRP ---
    print(f'# تقرير مدير المصنع — {today_ar}')
    print()
    print('> **مدير المصنع:** محمد سلطان')
    print('> **مدير الإنتاج:** رؤوف الديب')
    print(f'> **المصدر:** Odoo MRP + Odoo POs + Outlook SQLite')
    print()
    print('---')
    print()
    total_mrp = sum(mrp.values())
    print(f'## 1️⃣ أوامر التصنيع (MRP) — {total_mrp} أمر')
    print()
    print('| الحالة | العدد |')
    print('|--------|:-----:|')
    for s in ['done', 'progress', 'draft', 'to_close', 'cancel', 'confirmed']:
        if s in mrp:
            print(f'| {MRP_STATE_AR.get(s, s)} | {mrp[s]} |')
    print()

    # --- Section 2: POs ---
    print('## 2️⃣ أوامر الشراء (POs) — المصنع')
    print()
    fp_total = sum(p['amount_total'] for p in factory_pos)
    sp_total = sum(p['amount_total'] for p in supplier_pos)
    open_count = sum(1 for p in factory_pos if p['state'] == 'purchase')
    draft_count = sum(1 for p in factory_pos if p['state'] == 'draft')
    print('| البند | العدد | الإجمالي (SAR) |')
    print('|------|:-----:|:--------------:|')
    print(f'| POs مشاريع المصنع | {len(factory_pos)} | {fp_total:,.2f} |')
    print(f'| POs موردي المصنع لمشاريع أخرى | {len(supplier_pos)} | {sp_total:,.2f} |')
    print(f'| **المفتوح (purchase)** | {open_count} | — |')
    print(f'| **مسودة** | {draft_count} | — |')
    print()

    # Top vendors by outstanding (open POs)
    open_vendors = defaultdict(float)
    for p in factory_pos:
        if p['state'] == 'purchase':
            v = p['partner_id'][1] if p['partner_id'] else '?'
            open_vendors[v] += p['amount_total']
    if open_vendors:
        print('**أعلى موردين بالمستحقات المفتوحة:**')
        for v, t in sorted(open_vendors.items(), key=lambda x: -x[1])[:5]:
            print(f'- {v}: {t:,.2f} SAR')
        print()

    # --- Section 2b: Confirmed POs not yet received ---
    RECEIPT_AR = {'pending': 'لم يُستلم', 'partial': 'استلام جزئي',
                  'full': 'مستلم كامل', False: 'غير محدد'}
    not_received = [p for p in factory_pos
                    if p['state'] == 'purchase' and p.get('receipt_status') != 'full']
    if not_received:
        nr_total = sum(p['amount_total'] for p in not_received)
        print(f'## 2️⃣ب أوامر الشراء المؤكدة غير المستلمة — {len(not_received)} أمر / {nr_total:,.2f} SAR')
        print()
        print('| الأمر | المورد | القيمة (SAR) | حالة الاستلام |')
        print('|------|--------|:------------:|:--------------:|')
        for p in sorted(not_received, key=lambda x: -x['amount_total']):
            name = p['name']
            vendor = p['partner_id'][1] if p['partner_id'] else '?'
            rs = RECEIPT_AR.get(p.get('receipt_status'), p.get('receipt_status') or 'غير محدد')
            print(f'| {name} | {vendor} | {p["amount_total"]:,.2f} | {rs} |')
        print()

    # --- Section 3: Emails ---
    emails = fetch_raoof_emails(30)
    print('## 3️⃣ الإيميلات — آخر 30 يوم')
    print()
    print('### من رؤوف (مدير الإنتاج):')
    if emails:
        for dt, subj, prev in emails:
            print(f'- **{dt[:10]}** {subj}')
    else:
        print('- لا توجد إيميلات جديدة من رؤوف')
    print()

    # --- Data footer for the agent ---
    print('---')
    print()
    print('## 4️⃣ القرارات')
    print()
    print('*(اكتب القرارات هنا — حلل الأقسام أعلاه واقترح إجراءات واضحة: ماذا/من/متى/الأولوية)*')
    print()
    print(f'<!-- DATA_TS:{today_str} -->')


if __name__ == '__main__':
    main()
