#!/bin/bash
# Daily DD Packages Update — checks Outlook for recent status and updates Odoo
set -euo pipefail

TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')
echo "=== Daily DD Update — $TIMESTAMP ==="

python3 << 'PYEOF'
import xmlrpc.client, ssl, os, sqlite3
from datetime import date, datetime
TIMESTAMP = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

# --- Odoo ---
ctx = ssl._create_unverified_context()
transport = xmlrpc.client.SafeTransport(context=ctx)
URL, DB, LOGIN = 'https://samayainv.odoo.com', 'peerless-tech-samaya-18-0-18447146', 'sultan@samayainvest.com'
with open(os.path.expanduser('~/.config/samaya/odoo.env')) as f:
    for line in f:
        if 'ODOO_API_KEY' in line and '=' in line:
            PWD = line.split('=', 1)[1].strip()
common = xmlrpc.client.ServerProxy(URL + '/xmlrpc/2/common', transport=transport)
uid = common.authenticate(DB, LOGIN, PWD, {})
models = xmlrpc.client.ServerProxy(URL + '/xmlrpc/2/object', transport=transport)

# Get current DD packages
pkgs = models.execute_kw(DB, uid, PWD, 'project.task', 'search_read',
    [[['project_id', '=', 219], ['stage_id', '=', 36], ['parent_id', '=', False]]],
    {'fields': ['id', 'name', 'state', 'progress', 'date_assign']})
print(f'Loaded {len(pkgs)} DD packages')

# --- Outlook ---
outlook_db = os.path.expanduser('~/Library/Group Containers/UBF8T346G9.Office/Outlook/Outlook 15 Profiles/Main Profile/Data/Outlook.sqlite')
if not os.path.exists(outlook_db):
    print('Outlook DB not found — skipping')
    exit(0)

conn = sqlite3.connect(outlook_db)
cur = conn.cursor()

# Count new emails in last 24h about Aseer
cutoff = int(datetime.now().timestamp()) - 86400
cur.execute('''
SELECT COUNT(*) FROM Mail
WHERE Message_NormalizedSubject LIKE '%ASE%' OR Message_NormalizedSubject LIKE '%Aseer%'
   OR Message_NormalizedSubject LIKE '%MOC-MUS%'
''')
count = cur.fetchone()[0]

# Count today's
cur.execute('''
SELECT COUNT(*) FROM Mail
WHERE (Message_NormalizedSubject LIKE '%ASE%' OR Message_NormalizedSubject LIKE '%MOC-MUS%')
  AND Message_TimeReceived > ?
''', (cutoff,))
recent = cur.fetchone()[0]
print(f'Outlook: {recent} new Aseer emails today (total {count})')

connected = False
scan_time = datetime.now().strftime('%Y-%m-%d %H:%M')
models.execute_kw(DB, uid, PWD, 'project.task', 'write', [[2946], {
    'description': f'<h3>05 Projects Plans</h3><p><b>Last daily scan:</b> {scan_time}</p><p><b>New emails today:</b> {recent}</p>'
}])
print(f'Updated 2946 with scan timestamp')

conn.close()
print(f'=== Done {TIMESTAMP} ===')
PYEOF
