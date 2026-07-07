#!/usr/bin/env python3
"""
Build Samaya Factory Cashout Report from Odoo 18.
Usage: SSL_CERT_FILE=$(python3 -c "import certifi; print(certifi.where())") python3 build_cashout_report.py

Output: Samaya_Factory_Cashout_Report_Updated.xlsx in the reports folder.
"""
import xmlrpc.client, os, sys
from datetime import datetime
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side

# ── Config ──
ENV_PATH = os.path.expanduser('~/.config/samaya/odoo.env')
OUTPUT = '/Users/mohamedessa/Library/CloudStorage/OneDrive-SAMAYAINVESTMENT/Samaya/Orders/2026/0000 اداريات/00 تقارير الاعمال/Samaya_Factory_Cashout_Report_Updated.xlsx'
FACTORY_PROJECT_ID = 244
CREDIT_PARTNERS = {2427, 5603}  # Mada Aljezera, Saba Najad
ODOO_BASE = 'https://samayainv.odoo.com'

# هام file POs to include (from user's WhatsApp file)
HAM_POS = [
    'P01094','P01252','P01818','P01819','P01909','P01924','P01939',
    'P01970','P02030','P02033','P02038','P02061','P02066','P02084',
    'P02088','P02093','P02096','P02098','P02099'
]

# Descriptions from هام file
DESCRIPTIONS = {
    'P01094': 'المصنع - طابعات اوراق',
    'P01252': 'عجلة ضبط شفرة منشار الطاولة',
    'P01818': 'وايرليس و تابليت - ا عبد الله محفوظ',
    'P01819': 'دهان ذهبي وفضي اونلاين - ا عبد الله محفوظ',
    'P01909': 'ماكينة وسم وحفر ليزر فايبر',
    'P01924': 'تنجيد كنب الغمامة - تم ارسال جزء من المبلغ',
    'P01939': 'مواسير المتاجر - 40 حبة',
    'P01970': 'اعاشة عارف الحداد',
    'P02030': 'متاجر -الغمامة - متجر الهدايا - معالم الحرمين',
    'P02033': 'متاجر الغمامة - متاجر الغمامه 2 السقف',
    'P02038': 'Jalal & Jamal - كونكترات لليد',
    'P02061': 'القشرة الجديدة مكة 750 متر',
    'P02066': 'غراء ابيض و اسود للكوريان',
    'P02084': 'Maalim Al-Haramein - اعمال تشطيب في الموقع',
    'P02088': 'Maalim Al-Haramein - اعمال خارجية دهانات',
    'P02093': 'Jalal & Jamal - عاكس زجاج لاستندات الشاشات',
    'P02096': 'متاجر الغمامة - متجر الهدايا - اخشاب متنوعه',
    'P02098': 'كشف مصروفات شراء مسلتزمات للمصنع + العهدة',
    'P02099': 'Maalim Al-Haramein - عمالة خارجية قسم الفايبر',
}

# ── Odoo connection ──
env = {}
with open(ENV_PATH) as f:
    for line in f:
        line = line.strip()
        if not line or line.startswith('#') or '=' not in line: continue
        k, v = line.split('=', 1)
        env[k.strip()] = v.strip()

common = xmlrpc.client.ServerProxy(f'{env["ODOO_URL"]}/xmlrpc/2/common')
uid = common.authenticate(env['ODOO_DB'], env['ODOO_USER'], env['ODOO_API_KEY'], {})
models = xmlrpc.client.ServerProxy(f'{env["ODOO_URL"]}/xmlrpc/2/object')
def call(model, method, args=None, kwargs=None):
    return models.execute_kw(env['ODOO_DB'], uid, env['ODOO_API_KEY'], model, method, args or [], kwargs or {})

# ── Fetch data (fetch ALL — Odoo 18 crashes on project_id domain) ──
fields = ['name','partner_id','amount_total','date_order','state','project_id','invoice_status','partner_ref']
all_pos = call('purchase.order', 'search_read', [[]], {'fields': fields, 'limit': 2000})

# Filter to هام POs
ham_set = set(HAM_POS)
ham_pos = [p for p in all_pos if p['name'] in ham_set]

# Separate included vs excluded
included = []
excluded = []
for po in sorted(ham_pos, key=lambda x: x['name']):
    pid = po.get('project_id')
    is_factory = pid and pid[0] == FACTORY_PROJECT_ID
    amt = po['amount_total']
    is_credit = po.get('partner_id') and po['partner_id'][0] in CREDIT_PARTNERS

    if not is_factory:
        excluded.append((po, 'Other project'))
    elif amt <= 0:
        excluded.append((po, 'Zero amount'))
    elif is_credit:
        excluded.append((po, 'Credit supplier'))
    else:
        included.append(po)

total = sum(p['amount_total'] for p in included)

# Credit supplier balances (all unpaid Factory POs for these partners)
mada_all = [p for p in all_pos if p.get('project_id') and p['project_id'][0] == FACTORY_PROJECT_ID
    and p.get('partner_id') and p['partner_id'][0] == 2427
    and p['state'] == 'purchase' and p.get('invoice_status') in ('to invoice','no') and p['amount_total'] > 0]
saba_all = [p for p in all_pos if p.get('project_id') and p['project_id'][0] == FACTORY_PROJECT_ID
    and p.get('partner_id') and p['partner_id'][0] == 5603
    and p['state'] == 'purchase' and p.get('invoice_status') in ('to invoice','no') and p['amount_total'] > 0]

mada_total = sum(p['amount_total'] for p in mada_all)
saba_total = sum(p['amount_total'] for p in saba_all)
grand_total = total + mada_total + saba_total

# ── Build Excel (openpyxl) ──
# ... (standard styling: navy headers, yellow totals, alternating rows, landscape A4)
# See samaya-factory-pos skill for full styling constants

print(f'Included: {len(included)} POs = {total:,.2f} SAR')
print(f'Credit Mada: {mada_total:,.2f} | Saba: {saba_total:,.2f}')
print(f'Grand Total: {grand_total:,.2f} SAR')
