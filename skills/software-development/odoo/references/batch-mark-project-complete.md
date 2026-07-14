# Batch-Mark All Tasks 100% Complete (In-Place)

Use when a project is finished and all its tasks should show 100% progress **without moving stages**. The user's instruction is typically: "mark all tasks done in the same stage, don't move them."

## Pattern

```python
import xmlrpc.client, ssl, os

# Load credentials
env = {}
with open(os.path.expanduser('~/.config/samaya/odoo.env')) as f:
    for line in f:
        line = line.strip()
        if '=' in line and not line.startswith('#'):
            k, v = line.split('=', 1)
            env[k.strip()] = v.strip()

url = env.get('ODOO_URL', 'https://samayainv.odoo.com')
db = env.get('ODOO_DB')
user = env.get('ODOO_USER')
api_key = env.get('ODOO_API_KEY')

ctx = ssl._create_unverified_context()
t = xmlrpc.client.SafeTransport(context=ctx)
common = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/common', transport=t)
uid = common.authenticate(db, user, api_key, {})

models = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/object', transport=t)

PROJECT_ID = 290  # ← SET THIS

# 1. Verify project exists
proj = models.execute_kw(db, uid, api_key, 'project.project', 'search_read',
    [[['id', '=', PROJECT_ID]]], {'fields': ['id', 'name'], 'limit': 1})
print(f"Project: {proj}")

# 2. Get all tasks
tasks = models.execute_kw(db, uid, api_key, 'project.task', 'search_read',
    [[['project_id', '=', PROJECT_ID]]],
    {'fields': ['id', 'name', 'stage_id', 'state', 'progress', 'parent_id'], 'limit': 500})
print(f"Total tasks: {len(tasks)}")

# 3. Show current state
for t in tasks:
    pid = f" (parent={t['parent_id'][0]})" if t['parent_id'] else ""
    print(f"  ID={t['id']} | {t['name'][:80]}{pid} | stage={t['stage_id']} | state={t['state']} | progress={t.get('progress', 'N/A')}")

# 4. Mark ALL as 100% done in their current stage
print(f"\n--- Marking {len(tasks)} tasks as 100% complete (same stage) ---")
updated = 0
for t in tasks:
    models.execute_kw(db, uid, api_key, 'project.task', 'write',
        [[t['id']], {'progress': 1.0}])
    updated += 1

print(f"Done. {updated}/{len(tasks)} tasks updated to 100% in their current stage.")
```

## Key points

- **`progress: 1.0`** = 100% (Odoo uses 0.0–1.0 scale, NOT 0–100)
- **Do NOT change `stage_id`** — the user explicitly wants tasks to stay in their current stage
- **Do NOT change `state`** — leave as-is (e.g. `01_in_progress`, `1_done`)
- Always print the before-state so the user can verify what was changed
- Always print the count of updated tasks as confirmation

## Finding the right project

Search by Arabic name with `=ilike`:

```python
projs = models.execute_kw(db, uid, api_key, 'project.project', 'search_read',
    [[['name', '=ilike', '%مسجد%نبوي%']]], {'fields': ['id', 'name'], 'limit': 5})
```

Or search tasks for project name clues:

```python
tasks = models.execute_kw(db, uid, api_key, 'project.task', 'search_read',
    [[['name', '=ilike', '%Prophet%Mosque%']]],
    {'fields': ['id', 'name', 'project_id'], 'limit': 10})
```
