# Odoo Task Mapping — Pattern Reference

## When to Create

When the user says "create a mapping of Odoo tasks and subtasks in this repo" or "link Odoo task structure to update status."

## Query Pattern

```python
import ssl, xmlrpc.client, os

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

env = {}
with open(os.path.expanduser('~/.config/samaya/odoo.env')) as f:
    for line in f:
        line = line.strip()
        if '=' in line and not line.startswith('#'):
            k, v = line.split('=', 1)
            env[k] = v

transport = xmlrpc.client.SafeTransport(context=ctx)
common = xmlrpc.client.ServerProxy(f'{env["ODOO_URL"]}/xmlrpc/2/common', transport=transport)
uid = common.authenticate(env['ODOO_DB'], env['ODOO_USER'], env['ODOO_API_KEY'], {})
models = xmlrpc.client.ServerProxy(f'{env["ODOO_URL"]}/xmlrpc/2/object', transport=transport)

# Get stages
stages = models.execute_kw(env['ODOO_DB'], uid, env['ODOO_API_KEY'],
    'project.task.type', 'search_read',
    [[['project_ids', '=', PROJECT_ID]], ['id', 'name']])

# Get all tasks with parent info
tasks = models.execute_kw(env['ODOO_DB'], uid, env['ODOO_API_KEY'],
    'project.task', 'search_read',
    [[['project_id', '=', PROJECT_ID]],
     ['id', 'name', 'parent_id', 'stage_id', 'progress', 'date_deadline', 'user_ids']],
    {'order': 'parent_id asc, id asc', 'limit': 500})
```

## Tree Construction

```python
parents = [t for t in tasks if not t['parent_id']]
children = [t for t in tasks if t['parent_id']]

for p in sorted(parents, key=lambda x: x['id']):
    pid = p['id']
    kids = [c for c in children if c['parent_id'][0] == pid]
    print(f"\n{pid}|{p['name'][:100]}|{pstage}|{pprog}")
    for c in sorted(kids, key=lambda x: x['id']):
        print(f"  └─ {c['id']}|{c['name'][:90]}|{cstage}|{cprog}")
```

## Mapping File Structure

Create `01_Odoo_Mapping/task_mapping.md` in the repo with:

1. **Header** — project ID, Odoo instance, last synced date
2. **Stage reference table** — ID → name mapping
3. **Per-discipline sections** — each parent task as a heading, subtasks in a table

### Table format per section

```markdown
## 01 — Architecture (2938)
| ID | Name | Stage | Progress | Notes |
|----|------|-------|----------|-------|
| 352 | دراسة المشروع و تقديم خطة عمل | DD | 0% | |
| 2983 | 3D Render Sample — ZD-0033 Rev.01 | DD | 100% | Approved Code B |
```

### Standalone tasks section

Tasks with no parent go in a standalone section at the end.

## Key Fields

| Field | Odoo Key | Notes |
|-------|----------|-------|
| Task ID | `id` | Primary key |
| Name | `name` | |
| Parent | `parent_id` | `[id, name]` or `False` |
| Stage | `stage_id` | `[id, name]` |
| Progress | `progress` | 0.0–1.0 float |
| Deadline | `date_deadline` | ISO date string or `False` |
| Assignees | `user_ids` | Array of user IDs |

## Aseer-Specific (Project 219)

- **Odoo instance**: `samayainv.odoo.com`
- **Project ID**: 219
- **Total tasks**: ~347
- **Parent tasks**: 18 discipline packages + procurement/manufacturing/site work groups
- **Stages**: 35 Initiation, 36 DD, 39 Procurement, 659 Off-site Mfg, 40 On-site, 479 Handover, 480 Cancelled
