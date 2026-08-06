# Odoo API Key Management — Odoo 18 (Samaya)

## Problem

API keys expire. The old key in `.odoo_config` returns `Fault 3: Access Denied` / `UID: False`.

## Cannot create API keys via the API itself

Odoo 18 blocks `res.users.apikeys.create` with:
```
AccessError: You are not allowed to create 'Users API Keys' records.
```

Keys can only be generated through the **web UI**.

## How to generate a new API key

1. Login at `https://samayainv.odoo.com/web/login` with password
2. Click user avatar → **My Profile** → tab **Account Security**
3. Scroll to **API KEYS** section → **New API Key**
4. Enter description (e.g. "Hermes"), pick duration (1 Year recommended)
5. Confirm password when prompted (Odoo shows a "Security Control" dialog)
6. Copy the generated key into `.odoo_config`

## Session-based fallback (read-only, when key is expired)

Use password login + `requests.Session()` to get a live session, then query via the JSON web API:

```python
import requests

url = 'https://samayainv.odoo.com'
db = 'peerless-tech-samaya-18-0-18447146'

session = requests.Session()
login = session.post(f'{url}/web/session/authenticate', json={
    'jsonrpc': '2.0',
    'params': {'db': db, 'login': 'sultan@samayainvest.com', 'password': '1batagoniaA'}
}).json()
uid = login['result']['uid']  # 151 for Sultan Issa

# Query via /web/dataset/call_kw
resp = session.post(f'{url}/web/dataset/call_kw', json={
    'jsonrpc': '2.0', 'method': 'call',
    'params': {
        'model': 'hr.employee',
        'method': 'search_read',
        'args': [],
        'kwargs': {'domain': [['department_id.name', 'ilike', 'Manufacturing']],
                   'fields': ['id', 'name', 'job_title', 'work_phone', 'work_email', 'active'],
                   'limit': 100}
    }
}).json()
employees = resp['result']
```

This works for **read-only queries**. For writes, generate a proper API key via the web UI.

## Existing API keys (Sultan Issa, UID 151)

| Name | Created | Expires |
|------|---------|---------|
| Clawdbot2 | 2026-02-25 | 2027-02-25 |
| Claw3 | 2026-04-27 | 2027-04-27 |
| Hermies 2 | 2026-05-18 | 2026-11-14 |
| Claude | 2026-05-20 | 2026-11-16 |
| kimi | 2026-05-20 | 2026-11-16 |

The old key in `.odoo_config` (`bfc7d8a6cffece1e31d8f295b230f9fa9c6eb713`) is not in this list — it was revoked/replaced.
