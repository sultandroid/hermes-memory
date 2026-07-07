# Odoo Personal Tasks (To-Do Module) — XML-RPC Pattern

Personal tasks live in the **To-Do** app (no project required). In Odoo 18, these are `project.task` records with `project_id = False`.

## Authentication Fix (Odoo 18)

Odoo 18 SaaS requires a `user_agent_env` dict on `authenticate()`:

```python
import xmlrpc.client, ssl, certifi, os
ctx = ssl.create_default_context(cafile=certifi.where())
common = xmlrpc.client.ServerProxy(URL + '/xmlrpc/2/common', context=ctx)
uid = common.authenticate(DB, USER, PWD, {'interactive': True})  # ← required
M = xmlrpc.client.ServerProxy(URL + '/xmlrpc/2/object', context=ctx)
```

Without `{'interactive': True}`, Odoo 18 raises:
```
TypeError: exp_authenticate() missing 1 required positional argument: 'user_agent_env'
```

## Credentials

```python
URL  = "https://samayainv.odoo.com"
DB   = "peerless-tech-samaya-18-0-18447146"
USER = "sultan@samayainvest.com"      # uid=151
PWD  = os.getenv('ODOO_API_KEY')      # from ~/.config/samaya/odoo.env
```

Load from env file:
```python
env_file = os.path.expanduser("~/.config/samaya/odoo.env")
env = {}
with open(env_file) as f:
    for line in f:
        if '=' in line and not line.startswith('#'):
            k, v = line.strip().split('=', 1)
            env[k] = v
PWD = env.get('ODOO_API_KEY', '')
```

## Key Field Values

| Field | Odoo value | Notes |
|-------|-------------|-------|
| `priority` | `'1'` = High, `'0'` = Low | String, not int |
| `stage_id` | `95` = Inbox (To-Do app) | New tasks land here |
| `date_deadline` | `'YYYY-MM-DD'` | String ISO format |
| `state` | `'1_done'` = completed | Do NOT change stage_id to mark done |
| `user_ids` | `[(4, uid)]` = assign to user | Many2many — use `(4, uid)` to add |

## Creating Personal Tasks (No Project)

```python
task_id = M.execute_kw(DB, uid, PWD, 'project.task', 'create', [{
    'name':          '[Aseer] Artec Space Spider RFQ — Decision Needed',
    'priority':      '1',           # High
    'stage_id':      95,             # Inbox (To-Do)
    'date_deadline': '2026-05-29',
    'description':   'Action: Approve or reject quotation\nFrom: omar.bittar@3d-me.com',
}])
# Assign to user
M.execute_kw(DB, uid, PWD, 'project.task', 'write', [[task_id], {
    'user_ids': [(4, uid)]
}])
```

## Marking Tasks Done

```python
# CORRECT — stays in current stage
M.execute_kw(DB, uid, PWD, 'project.task', 'write', [[task_id], {'state': '1_done'}])

# WRONG — never change stage_id to mark done
M.execute_kw(DB, uid, PWD, 'project.task', 'write', [[task_id], {'stage_id': some_done_stage}])
```

## Querying Personal Tasks

```python
# My tasks (no project) — personal To-Do items
my_todos = M.execute_kw(DB, uid, PWD, 'project.task', 'search_read',
    [[['project_id', '=', False], ['user_ids', 'in', [uid]]]],
    {'fields': ['id', 'name', 'priority', 'stage_id', 'date_deadline', 'state']})

# My all tasks (any project)
my_tasks = M.execute_kw(DB, uid, PWD, 'project.task', 'search_read',
    [[['user_ids', 'in', [uid]]]],
    {'fields': ['id', 'name', 'project_id', 'priority', 'state'], 'limit': 20})
```

## Available Stages (Personal To-Do)

| stage_id | Name | Use for |
|----------|------|---------|
| 95 | Inbox | New unread tasks |
| 96 | Today | Do today |
| 97 | This Week | Do this week |
| 98 | This Month | Do this month |
| 99 | Later | Backlog |
| 100 / 43 / 211 | Done | Completed |
| 101 | Cancelled | Discarded |

## Delivery Options for Daily Todo Cron

1. **Telegram only** (current default) — free-form markdown to chat
2. **Odoo To-Do** (preferred for tracked work) — creates `project.task` records with priority flag, deadline, description, and assignment to `sultan@samayainvest.com`

## Important: `type` Field on `project.project`

The `project.project.type` field is deprecated/invalid in Odoo 18. To find the To-Do project, search by `project_id = False` (no project) rather than by project type. All personal tasks have `project_id = False / null`.
