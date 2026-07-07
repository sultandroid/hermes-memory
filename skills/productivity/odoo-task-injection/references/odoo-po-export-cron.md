# Odoo Purchase Order Export Cron (no_agent=True Pattern)

Used for the SAMAYA WORKSHOP purchasing tracker — a daily 2PM cron that exports all POs for buyer (`user_id=155`) to an Excel tracker.

## Script Template

Save as `~/.hermes/scripts/<name>.py`. Must be self-contained — cron runs no_agent=True, so no context, no skills, just pure Python.

```python
#!/usr/bin/env python3
import xmlrpc.client, ssl, os
from datetime import datetime
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

ODOO_URL = 'https://samayainv.odoo.com'
ODOO_DB = 'peerless-tech-samaya-18-0-18447146'
ODOO_USER = 'sultan@samayainvest.com'
OENV = os.path.expanduser('~/.config/samaya/odoo.env')
TARGET = "/path/to/output.xlsx"

def get_pw():
    with open(OENV) as f:
        for line in f:
            if 'ODOO_API_KEY' in line and '=' in line:
                return line.split('=', 1)[1].strip()
    return None

def connect():
    ctx = ssl._create_unverified_context()
    transport = xmlrpc.client.SafeTransport(context=ctx)
    common = xmlrpc.client.ServerProxy(ODOO_URL + '/xmlrpc/2/common', transport=transport)
    pw = get_pw()
    uid = common.authenticate(ODOO_DB, ODOO_USER, pw, {})
    models = xmlrpc.client.ServerProxy(ODOO_URL + '/xmlrpc/2/object', transport=transport)
    return uid, models, pw
```

### Pulling data

```python
pos = models.execute_kw(ODOO_DB, uid, pw, 'purchase.order', 'search_read',
    [[('user_id', '=', 155)]],  # SAMAYA WORKSHOP
    {'fields': ['name', 'partner_id', 'partner_ref', 'amount_total', 'state',
                'receipt_status', 'invoice_status', 'date_order'],
     'order': 'date_order desc',
     'limit': 500})
```

### State label mapping

```python
state_labels = {
    'draft': 'RFQ', 'sent': 'RFQ Sent', 'to approve': 'To Approve',
    'purchase': 'Purchase Order', 'done': 'Locked', 'cancel': 'Cancelled',
}
receipt_labels = {
    False: '', 'no': 'Not Received', 'partial': 'Partially Received', 'full': 'Received',
}
invoice_labels = {
    'no': 'Not Billed', 'to invoice': 'Waiting Bills', 'invoiced': 'Billed',
}
```

### Cron job setup

```bash
# via the cronjob tool:
cronjob(action='create',
    name='Description',
    schedule='0 14 * * *',       # daily 2PM
    script='<name>.py',
    workdir='/Users/mohamedessa/.hermes',
    no_agent=True)
```

### Important notes

- **no_agent=True** means the script IS the job — no LLM runs, just the script's stdout is delivered
- The script must handle Odoo authentication independently (reads ~/.config/samaya/odoo.env)
- **Close Excel before the cron runs** — openpyxl writes need exclusive file access
- Leave a `Notes/تحويل` column for manual entry of transfer receipt info — the script only overwrites the data columns
- Include `ws.freeze_panes` and `ws.auto_filter` for usability
- Title row with update timestamp helps the user know data is current
