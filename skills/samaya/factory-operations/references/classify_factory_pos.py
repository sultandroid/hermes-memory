#!/usr/bin/env python3
"""
تصنيف POs المصنع حسب الاستلام والدفع + ربط إيميلات إبراهيم شعبان
Usage: python3 classify_factory_pos.py
Requires: factory_pos_full.json (from Odoo dump), Outlook SQLite access
"""
import json, sqlite3, os, re
from datetime import datetime
from collections import defaultdict

# === 1. Load POs ===
with open('/Users/mohamedessa/.hermes/tmp/factory_pos_full.json') as f:
    data = json.load(f)
fp = data['factory_project_pos']
pos = fp['pos']

# === 2. Load Ibrahim Shaaban emails from Outlook ===
outlook_path = os.path.expanduser(
    '~/Library/Group Containers/UBF8T346G9.Office/Outlook/'
    'Outlook 15 Profiles/Main Profile/Data/Outlook.sqlite'
)
conn = sqlite3.connect(outlook_path)
cur = conn.cursor()

cur.execute("""
    SELECT datetime(m.Message_TimeReceived, 'unixepoch'),
           m.Message_NormalizedSubject,
           m.Message_Preview
    FROM Mail m
    WHERE m.Message_SenderList LIKE '%Ibrahim%Shaaban%'
       OR m.Message_SenderList LIKE '%إبراهيم%شعبان%'
    ORDER BY m.Message_TimeReceived DESC
""")
ibrahim_emails = cur.fetchall()
conn.close()

# Extract PO numbers mentioned in Ibrahim's emails
payment_notes = {}
for dt, subj, body in ibrahim_emails:
    if not body: body = ''
    pos_found = re.findall(r'P0\d{4,5}', body)
    for po in pos_found:
        if po not in payment_notes:
            payment_notes[po] = []
        payment_notes[po].append((dt, subj, body[:200]))

# === 3. Classify POs ===
classification = {
    'مستلم كامل + مفوتر': [],
    'مستلم كامل + غير مفوتر': [],
    'مستلم جزئي': [],
    'لم يستلم + مفوتر': [],
    'لم يستلم + غير مفوتر': [],
    'ملغي': [],
    'مسودة': [],
}

for p in pos:
    state = p['state']
    if state == 'cancel':
        classification['ملغي'].append(p); continue
    if state == 'draft':
        classification['مسودة'].append(p); continue

    rec = p.get('receipt_status', False)
    inv = p.get('invoice_status', 'no')

    if rec == 'full' and inv == 'invoiced':
        classification['مستلم كامل + مفوتر'].append(p)
    elif rec == 'full' and inv != 'invoiced':
        classification['مستلم كامل + غير مفوتر'].append(p)
    elif rec == 'pending':
        classification['مستلم جزئي'].append(p)
    elif rec in (False, 'False', None, '') and inv == 'invoiced':
        classification['لم يستلم + مفوتر'].append(p)
    else:
        classification['لم يستلم + غير مفوتر'].append(p)

# === 4. Print Report ===
print('=' * 100)
print('تقرير تصنيف أوامر الشراء — مصنع سمايا')
print(f'التاريخ: {datetime.now().strftime("%Y-%m-%d %H:%M")}')
print(f'إجمالي POs: {len(pos)}')
print('=' * 100)

grand_total = 0
for cat, items in classification.items():
    total = sum(p['amount_sar'] for p in items)
    grand_total += total
    print(f'\n{"─" * 80}')
    print(f'📁 {cat} — {len(items)} أمر | {total:,.2f} SAR')
    print(f'{"─" * 80}')

    items_sorted = sorted(items, key=lambda x: x['amount_sar'], reverse=True)
    for p in items_sorted:
        po = p['po_number']
        amt = p['amount_sar']
        ven = p['vendor'][:45]
        date = p.get('order_date', '')[:10]
        ref = p.get('partner_ref', '')[:50]

        ib_note = payment_notes.get(po, [])
        ib_str = ''
        if ib_note:
            latest = ib_note[-1]
            ib_str = f' [💰 إبراهيم: {latest[1][:60]}]'

        print(f'  {po:8s} | {amt:>8,.2f} SAR | {date} | {ven:45s} | {ref:50s}{ib_str}')

print(f'\n{"=" * 100}')
print(f'الإجمالي الكلي: {grand_total:,.2f} SAR')
print(f'{"=" * 100}')

# === 5. Monthly payment summary from Ibrahim ===
print(f'\n{"=" * 100}')
print('📅 ملخص السداد الشهري — من إيميلات إبراهيم شعبان')
print(f'{"=" * 100}')

monthly = defaultdict(lambda: {'count': 0, 'subjects': []})
pay_keywords = ['سداد', 'دفع', 'صرف', 'تحويل', 'عهدة', 'مستخلص', 'كشف حساب', 'بنكي']
for dt, subj, body in ibrahim_emails:
    if any(k in subj for k in pay_keywords):
        month = dt[:7]
        monthly[month]['count'] += 1
        monthly[month]['subjects'].append(f'  {dt[:10]} | {subj[:80]}')

for month in sorted(monthly.keys()):
    m = monthly[month]
    print(f'\n📆 {month} — {m["count"]} إيميل')
    for s in m['subjects'][:10]:
        print(s)
    if len(m['subjects']) > 10:
        print(f'  ... و {len(m["subjects"]) - 10} أخرى')

print(f'\n{"=" * 100}')
print('✅ تم')
