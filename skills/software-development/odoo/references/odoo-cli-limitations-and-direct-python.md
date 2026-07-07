# Odoo CLI Limitations & Direct Python Script Pattern

## `odoo_connect.py` CLI Limitations

The CLI wrapper at `scripts/odoo_connect.py` supports `search_read`, `search`, `read` methods — but NOT `create`, `write`, or `unlink`.

### Method Behavior

| Method | CLI Support | Args | Example |
|--------|-------------|------|---------|
| `search_read` | ✅ Yes | `--domain`, `--fields`, `--limit` | Best for listing records with field selection |
| `search` | ✅ Yes | `--domain`, `--limit` | Returns only IDs |
| `read` | ⚠️ Partial | `--domain` (misleading) | `read()` expects **integer IDs** as first arg, not a domain. Using `--domain` with `read` will fail with `IndexError: tuple index out of range`. Use `search_read` instead for domain-based queries. |
| `create` | ❌ No | N/A | Must use direct Python script |
| `write` | ❌ No | N/A | Must use direct Python script |
| `unlink` | ❌ No | N/A | Must use direct Python script |

### Complex Domain Pitfall

Domains with nested lists like `[['project_ids', 'in', [309]]]` must be passed as **properly escaped JSON**. The CLI wrapper does `json.loads(a.domain)`, so the string must be valid JSON:

```bash
# Correct: use single quotes for the outer shell string
python3 odoo_connect.py --instance samaya --model project.task.type \\
  --method search_read --domain '[["project_ids","in",[309]]]' \\
  --fields '["id","name"]' --limit 10

# Wrong: double quotes outside will break shell parsing
```

### Finding Project-Specific Task Stages

Samaya projects may only have a subset of stages configured. Query by project ID:

```bash
python3 odoo_connect.py --instance samaya --model project.task.type \\
  --method search_read --domain '[["project_ids","in",[309]]]' \\
  --fields '["id","name","sequence"]'
```

If you get an empty result, query ALL stages and check the `project_ids` field manually — the domain filter may fail silently on some Odoo versions.

---

## Direct Python Script Pattern (for Create/Write)

When you need to create records (tasks, projects, POs), write a standalone script using the same connection pattern:

```python
#!/usr/bin/env python3
import xmlrpc.client, os

url = 'https://samayainv.odoo.com'
db = 'peerless-tech-samaya-18-0-18447146'
login = 'sultan@samayainvest.com'

# Read API key from env file
env_path = os.path.expanduser('~/.config/samaya/odoo.env')
password = None
with open(env_path) as f:
    for line in f:
        line = line.strip()
        if 'ODOO_API_KEY' in line:
            password = line.split('=')[1].strip().strip("'\"")
            break

if not password:
    print("ERROR: Could not read API key")
    exit(1)

common = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/common')
uid = common.authenticate(db, login, password, {})
models = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/object')

# Create a main task with sub-tasks
parent_id = models.execute_kw(db, uid, password, 'project.task', 'create', [{
    'name': 'Main Task Name',
    'project_id': 309,     # Project ID
    'stage_id': 36,        # Stage ID (check per project)
    'planned_date_start': '2026-06-08',
    'description': '<h3>Header</h3><p>Description</p>',
}])

# Create sub-task linked to parent
sub_id = models.execute_kw(db, uid, password, 'project.task', 'create', [{
    'name': 'Sub-task Name',
    'project_id': 309,
    'stage_id': 36,
    'parent_id': parent_id,   # Links as child
    'description': '<ul><li>Item</li></ul>',
}])

print(f'Created main task: {parent_id}')
print(f'Created sub-task: {sub_id}')
```

### Key field quirks for `project.task`:

| Field | Type | Notes |
|-------|------|-------|
| `project_id` | many2one | Integer project ID |
| `stage_id` | many2one | Task stage ID — varies per project |
| `parent_id` | many2one | Set to create sub-task (link to parent task ID) |
| `user_ids` | many2many | **NOT `user_id`** — use `[(4, user_id)]` |
| `planned_date_start` | date | String 'YYYY-MM-DD' |
| `date_deadline` | date | String 'YYYY-MM-DD' |
| `description` | html | HTML string — use `<ul>`, `<li>`, `<h3>` for formatting |

### Samaya Odoo Auth Details

| Field | Value |
|-------|-------|
| URL | `https://samayainv.odoo.com` |
| DB | `peerless-tech-samaya-18-0-18447146` |
| Login | `sultan@samayainvest.com` |
| Password file | `~/.config/samaya/odoo.env` |
| Env key | `ODOO_API_KEY=...` |

### Moqtana Odoo Auth Details

| Field | Value |
|-------|-------|
| URL | `http://167.99.224.43:8069` |
| DB | `moqtana` |
| Login | `mohamedsultanabbas@gmail.com` |
| Password source | User supplies at runtime |
