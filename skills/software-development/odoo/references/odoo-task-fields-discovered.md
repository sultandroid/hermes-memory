# Odoo Task Fields — Discovered During Active Use

## Connectivity (Samaya Odoo)

Samaya Odoo (samayainv.odoo.com) uses a Let's Encrypt certificate chain that macOS Python's built-in SSL context may reject:

```python
import xmlrpc.client, ssl

ctx = ssl._create_unverified_context()
transport = xmlrpc.client.SafeTransport(context=ctx)
common = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/common', transport=transport)
uid = common.authenticate(db, login, pw, {})
```

This is only needed for CLI access via `xmlrpc.client`. The web UI works fine in a browser.

## `project.task` State Field

Full selection options discovered via `fields_get`:

| Value | Label | Use |
|-------|-------|-----|
| `01_in_progress` | In Progress | Active work item |
| `02_changes_requested` | Changes Requested | CG returned with C status / needs revision |
| `03_approved` | Approved | CG returned with A or B code |
| `1_done` | Done | Filed, completed, no further action |
| `1_canceled` | Cancelled | Abandoned |
| `04_waiting_normal` | Waiting | Blocked / awaiting input |

## `project.task` Progress Field

- **Field name:** `progress`
- **Type:** `float`
- **Scale:** **0.0 to 1.0** (NOT 0–100)
- Setting 100.0 causes "10K%" display because Odoo renders `progress` on a 0–100% scale internally, but the stored value is 0.0–1.0. So 100.0 renders as 10,000%.

**Correct usage:**
- 100% done → `progress: 1.0`
- 50% done → `progress: 0.5`
- 25% done → `progress: 0.25`

## `display_mark_as_done_primary`

- **Type:** `boolean`
- When `True`, shows a visual checkmark/badge on the task card in Kanban view
- Set to `True` for any task with state `1_done` or `03_approved`

## `date_assign`

- **Type:** `date` (YYYY-MM-DD string)
- Represents the assignment/start date
- Used alongside `date_deadline` for planning
- Always set both when creating tasks

## Package Progress = Average of Subtask Progress

For package tasks (parent tasks with subtasks), the recommended progress is the arithmetic mean of all subtask progress values:

```python
subtasks = models.execute_kw(db, uid, pw, 'project.task', 'search_read',
    [[['parent_id', '=', package_id]]],
    {'fields': ['progress']})
total = sum(k.get('progress') or 0 for k in subtasks)
avg = total / len(subtasks) if subtasks else 0
models.execute_kw(db, uid, pw, 'project.task', 'write',
    [[package_id], {'progress': avg}])
```

## Hiding Subtasks from Kanban View

By default, Odoo 18 shows subtasks as separate cards in the Kanban/List view alongside parent tasks. To show only parent tasks:

```python
models.execute_kw(db, uid, pw, 'ir.actions.act_window', 'write', [[416], {
    'domain': "[('project_id', '=', active_id), ('display_in_project', '=', True), ('parent_id', '=', False)]"
}])
```

Action IDs vary by instance but commonly: 416 (Tasks menu), 427 (Project's tasks), 420 (All Tasks). The added clause `('parent_id', '=', False)` filters out all subtask cards. Subtasks remain accessible inside each parent task's form view under the "Sub-tasks" tab.

## Task Creation Checklist

When creating a new task in Odoo (especially for project 219 — Aseer Museum):

```python
models.execute_kw(db, uid, pw, 'project.task', 'create', [{
    'name': 'Task Name',
    'project_id': 219,                         # Always
    'stage_id': 36,                            # Correct stage
    'parent_id': 2946,                         # Correct package parent
    'user_ids': [(4, uid)],                    # Assignee
    'state': '01_in_progress',                 # State
    'progress': 0.0,                           # 0.0-1.0 scale
    'date_assign': '2026-06-12',               # Always set
    'date_deadline': '2026-06-19',             # Always set
    'display_mark_as_done_primary': False,      # True for done tasks
    'description': '<p>Details</p>',            # HTML
}])
```

All 6 fields: `project_id`, `stage_id`, `parent_id`, `state`, `date_assign`, `date_deadline` should always be set. Missing dates break planning visibility.

## Tag IDs (tags)

- **Field:** `tag_ids` (many2many to `project.tags`)
- Create tag: `models.execute_kw(db, uid, pw, 'project.tags', 'create', [{'name': 'Prequalification', 'color': 8}])`
- Assign to task: `models.execute_kw(db, uid, pw, 'project.task', 'write', [[task_id], {'tag_ids': [(4, tag_id)]}])`
- Check existing: `models.execute_kw(db, uid, pw, 'project.tags', 'search_read', [[]], {'fields': ['id', 'name', 'color']})`

### Known Tags (Aseer Museum, project 219)

| ID | Name | Color | Use |
|----|------|-------|-----|
| 130 | A1-Architecture | Green | Architecture tasks |
| 132 | S1-Structure | Purple | Structural tasks |
| 133 | M1-MEP-Engineering | Blue | MEP tasks |
| 134 | L1-LifeSafety-CivilDefense | Red | Life Safety tasks |
| 136 | P1-Technical-Proposals | Orange | Proposals |
| 140 | Prequalification | Orange | Prequal package tasks |
| 141 | Plans & Procedures | Blue | Projects Plans subtasks |

## User Assignment Priority (Aseer Project)

**HARD RULE: All prequalification/procurement tasks for specialists → project management team ONLY.**
- **Mohamed Samir** (ID 564) — procurement specialist, handles ALL vendor/sourcing/prequal tasks
- **Sultan** (ID 151) — PM, handles strategic/oversight items (ITCA, T&C Manager, MOI Security, BEP, NRS)
- **Hesham** (ID 163) — site/document control, handles Tier 1 CV follow-ups only

Technical office team handles design deliverables (architecture, structural, MEP drawings/IFCs), NOT prequal:
- **Ali** (ID 160), **Ahmed Salah** (ID 162) — technical coordination, design documents, specialist design scope (Acoustic, FLS)
- **Raoof** (ID 153) — NOT part of Aseer project team. Never assign Aseer tasks to Raoof.

⚠ **User lookup pattern:** Find users by email/name substring:
```python
users = models.execute_kw(db, uid, pw, 'res.users', 'search_read',
    [[['login', '=ilike', '%hesham%']]],                               {'fields': ['id', 'name', 'login']})
```
Use `=ilike` for case-insensitive substring matching on `name` or `login` fields.

## Stage IDs (Samaya Odoo — Project 219 Aseer Museum)

| ID | Name | Sequence |
|----|------|----------|
| 35 | 01 Initiation | 10 |
| 36 | 02 Design Development (DD) Stage | 20 |
| 37 | 03 Procurement | 30 |
| 41 | 04 Off-site Manufacturing | 35 |
| 42 | 05 On-site Work / Execution | 40 |
| 43 | 06 Handover (As-Built & Snagging) | 50 |
| 44 | 07 Cancelled | 60 |

Always verify stage IDs before creating tasks — they vary per instance.
