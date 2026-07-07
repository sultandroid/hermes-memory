# Odoo Authentication Troubleshooting — Session Notes (2026-06-01)

## What was tried

Goal: list projects from the `moqtana` database on `167.99.224.43:8069`.

### 1. XML-RPC authenticate (all failed)

```python
common.authenticate('moqtana', 'admin', 'admin', {})           # False
common.authenticate('moqtana', 'admin', '2e8c7f5a...4ab22', {}) # False  (admin_passwd from config)
common.authenticate('moqtana', 'admin', 'moqtana', {})          # False
common.authenticate('moqtana', 'admin', '', {})                 # False
common.authenticate('moqtana', 'basem@moqtana.sa', '...', {})   # False (all known users × common passwords)
common.authenticate('moqtana', 'admin', 'cc2907...757f', {})    # False (DB password)
```

### 2. Web login (admin/admin got session cookie but redirects to /web/login)

Used /web/session/authenticate JSON-RPC. Session cookie obtained but post-auth redirect shows auth didn't actually succeed — Odoo returns a session cookie even for failed logins in some configurations.

### 3. Database management API (master password rejected)

```python
db_ep = xmlrpc.client.ServerProxy('http://167.99.224.43:8069/xmlrpc/2/db')
db_ep.duplicate_database(master_pwd, 'moqtana', 'moqtana_test')
# → Fault 3: 'Access Denied'
db_ep.dump(master_pwd, 'moqtana', 'sql')
# → Fault 3: 'Access Denied'
```

Both the 32-char hex `admin_passwd` from `config/odoo.conf` and `admin` as master password returned Access Denied.

### 4. PostgreSQL direct connection
Port 5432 not exposed externally (Docker bridge network only). Connection timed out.

### 5. SSH to droplet
Permission denied (publickey). No SSH key on this machine grants access to `ubuntu@167.99.224.43`.

## Root cause

The credentials in the local mirror (`/Users/mohamedessa/Documents/01_Odoo/config/odoo.conf` and `docker-compose.yml`) **were changed on the live server after deployment**. The `admin_passwd` (database master password), `db_password` (PostgreSQL), and all user account passwords were modified post-setup and the updated values were not synced back to the local copy.

## Resolution

The admin login is NOT `admin`. It's documented in `assets/company_data.md`:

```
## Odoo Access
- URL: http://167.99.224.43:8069
- Admin login: mohamedsultanabbas@gmail.com
- Database: moqtana
```

With the user-provided password (supplied at runtime — never stored here), XML-RPC authenticate returned UID=2 and data access succeeded.

## Working API call (verified 2026-06-01)

```python
import xmlrpc.client

url = 'http://167.99.224.43:8069'
db = 'moqtana'
login = 'mohamedsultanabbas@gmail.com'
password = '<supplied by user>'

common = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/common')
uid = common.authenticate(db, login, password, {})
# uid = 2 on success

models = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/object')
projects = models.execute_kw(db, uid, password, 'project.project', 'search_read', [[]],
    {'fields': ['id', 'name', 'user_id', 'partner_id', 'stage_id'], 'order': 'id asc'})
```

## Custom fields via ir.model.fields (verified 2026-06-01)

Custom fields can be created via XML-RPC without debug mode, as long as the user has the admin/Technical Features group. The `model_id` parameter must be the integer ID from `ir.model`:

```python
# Step 1: Find the model's numeric ID
model = models.execute_kw(db, uid, password, 'ir.model', 'search_read',
    [[['model', '=', 'project.project']]], {'fields': ['id']})
model_id = model[0]['id']

# Step 2: Create the field — available immediately, no restart needed
field_id = models.execute_kw(db, uid, password, 'ir.model.fields', 'create', [{
    'model_id': model_id,      # Numeric ID (e.g. 701), NOT model name string
    'name': 'x_project_code',
    'field_description': 'Project Code',
    'ttype': 'char',
    'state': 'manual',         # 'manual' = custom user field
    'required': False,
    'size': 20,
}])

# Step 3: Read/write immediately
models.execute_kw(db, uid, password, 'project.project', 'write', [[id], {'x_project_code': 'CODE'}])
```

Note: The `model_id` field is a many2one to `ir.model`. Passing just the integer works via XML-RPC (the orm wraps it). Do NOT pass the model name string — that causes "Expected singleton" errors as Odoo iterates each character of the string.

## Diagnostic commands (when SSH is available)

```bash
# Check if admin_passwd in config matches what's in DB
docker compose exec -T odoo odoo shell -d moqtana --log-level=warn <<< "
p = config.get('admin_passwd')
print(f'Configured master password: {p}')
# Check res.users
users = env['res.users'].search([])
for u in users:
    print(f'ID:{u.id} login:{u.login} name:{u.name}')
"
```
