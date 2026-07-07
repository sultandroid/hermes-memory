# Moqtana Odoo Connection Pattern (2026-06)

**Endpoint:** `https://odoo.moqtana.sa` (root, not `/odoo`)
**Database:** `moqtana`
**Username:** `mohamed.essa@samayainvest.com`
**SSL handling:** Must disable certificate verification (`ssl.CERT_NONE` + `check_hostname=False`)

**Working connection snippet:**
```python
import xmlrpc.client
import ssl

url = "https://odoo.moqtana.sa"
db = "moqtana"
username = "mohamed.essa@samayainvest.com"
password = "<user-provided>"

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

common = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/common', context=ctx)
uid = common.authenticate(db, username, password, {})
models = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/object', context=ctx)
```

**Common failure modes & fixes:**
- Using `https://odoo.moqtana.sa/odoo` → 400 Bad Request (wrong path)
- SSL verification enabled → certificate error on this host
- Wrong database name → authentication fails even with correct password

Add this pattern to any future Moqtana Odoo automation.
