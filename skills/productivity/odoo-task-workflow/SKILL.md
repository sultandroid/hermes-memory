---
name: odoo-task-workflow
title: Odoo Task Management — Complete Workflow
description: How to manage Odoo tasks end-to-end — create, update, stage, progress, timesheet, descriptions. Works for any project on any Odoo instance.
version: 1.1
---

# Odoo Task Management — Complete Workflow

## MANDATORY: Load this skill for EVERY Odoo operation

Read this entire skill before touching any Odoo task. Every instruction here is hard-won from user corrections.

## Connection

```python
import ssl, xmlrpc.client

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
```

## Task Descriptions — HUMAN WRITING ONLY

**NEVER write descriptions as bullet points or AI-style structured summaries.**

WRONG (AI style - REJECTED):
```
- Section 1: Introduction
- Section 2: Methodology
- Section 3: Specs
```

CORRECT (human style):
```
Prepared the Showcase Microclimate Control Methodology document for the Zamzam Museum.
Seven sections covering the whole approach — how the units work, installation steps,
Freeair FL-Z81 specs, layout plans with MCU and sensor locations marked, and a legend
to match the drawings. Ready for Mustafa to review before sending to the client.
```

Rules:
- Write as **one or two natural paragraphs**, not bullet lists
- No section headers, no numbered items, no meta-commentary
- No colons starting lists
- Describe what was done in plain language, like telling a colleague
- Use HTML `<p>` tags for multi-paragraph formatting in Odoo (the HTML field renders them)
  - `<p>First paragraph...</p><p>Second paragraph...</p>`

## Timesheets — MINUTES, NOT HOURS

`unit_amount` is in **minutes** (integer).

| Duration | Correct value |
|----------|---------------|
| 30 min | 30 |
| 1 hour | 60 |
| 2 hours | 120 |
| 3.5 hours | 210 |
| 8 hours | 480 |

```python
# CORRECT
models.execute_kw(db, uid, pw, 'account.analytic.line', 'create', [{
    'task_id': TASK_ID,
    'project_id': PROJECT_ID,
    'unit_amount': 120,           # 120 = 2 hours
    'name': 'Description of work done',
    'date': '2026-07-07',
}])

# WRONG
{'unit_amount': 2.0}   # This is wrong - must be minutes
```

## ALWAYS check and set these fields when updating a task:

### 1. Progress — always set
- **100%** when work is complete and awaiting review/approval
- **0%** for new or not-started
- Set via: `{'progress': 1.0}` (1.0 = 100% in Odoo)

### 2. Stage — check before setting
Always read the project's available stages first:
```python
p = models.execute_kw(db, uid, pw, 'project.project', 'read',
    [PROJECT_ID, ['type_ids', 'name']])
stages = models.execute_kw(db, uid, pw, 'project.task.type', 'read',
    [p[0]['type_ids'], ['id', 'name']])
```

Common stages for Samaya projects:
| Stage ID | Name | When to use |
|----------|------|-------------|
| 35 | 01 Initiation | New tasks, before work starts |
| 36 | 02 Design Development (DD) | Active work in progress |
| 39 | 03 Procurement | Procurement-related tasks |
| 659 | 04 Off-site Manufacturing | Manufacturing |
| 40 | 05 On-site Work / Execution | Installation, site work |
| 479 | 06 Handover | Completed, handed over |
| 480 | 07 Cancelled | Cancelled tasks |

### 3. Description — in human format (see above)

### 4. Date deadline — set reasonable deadlines
```python
{'date_deadline': '2026-07-08'}
```

## CRITICAL: Reflect subtask progress to parent task

Whenever you update a **subtask**, you MUST also update the **parent task** to reflect the overall progress.

### How to check parent-child relationships
```python
task = models.execute_kw(db, uid, pw, 'project.task', 'read',
    [[TASK_ID], ['id', 'name', 'parent_id', 'child_ids']])
```

### Rules for parent task updates:
- **Parent description** — append a sentence noting which subtask was completed
- **Parent progress** — update to reflect overall completion of all subtasks
- **Parent stage** — keep in same stage unless all children are done

### Example pattern:
```python
# After updating subtask 3397 (Methodology Approval), update parent 3396:
parent = models.execute_kw(db, uid, pw, 'project.task', 'read',
    [[3396], ['child_ids', 'name', 'progress']])
# Check all children progress, calculate overall, update parent
```

### NEVER forget:
- Subtask done ≠ parent done. But parent needs reflecting.
- At minimum: add to parent description that this subtask was completed.
- If all subtasks are at 100%, move parent to next stage.

## Full update pattern (always do ALL steps):

```python
# 1. Read current state
task = models.execute_kw(db, uid, pw, 'project.task', 'read',
    [[TASK_ID], ['stage_id', 'progress', 'name']])
print(f"Task: {task[0]['name']}, stage={task[0]['stage_id']}, progress={task[0]['progress']}")

# 2. Update all relevant fields
models.execute_kw(db, uid, pw, 'project.task', 'write',
    [[TASK_ID], {
        'progress': 1.0,          # 100% complete
        'description': '<p>Paragraph one.</p><p>Paragraph two.</p>',
        'date_deadline': '2026-07-08',
    }])

# 3. Create timesheet
models.execute_kw(db, uid, pw, 'account.analytic.line', 'create',
    [{
        'task_id': TASK_ID,
        'project_id': PROJECT_ID,
        'unit_amount': 120,           # MINUTES, not hours
        'name': 'What was done',
        'date': '2026-07-07',
    }])

# 4. Verify
ts = models.execute_kw(db, uid, pw, 'account.analytic.line', 'read',
    [[NEW_ID], ['id', 'unit_amount', 'name']])
print(f"Timesheet verified: {ts}")
```

## Task creation pattern

```python
new_id = models.execute_kw(db, uid, pw, 'project.task', 'create', [{
    'project_id': PROJECT_ID,
    'name': 'Task Name',
    'description': '<p>Human-written description...</p>',
    'stage_id': 36,                     # DD stage
    'user_ids': [(4, 151)],             # Assign to user
    'date_deadline': '2026-07-10',
}])
```

## Verification — always read back after write

After any write/update, ALWAYS verify by reading the data back:
```python
result = models.execute_kw(db, uid, pw, 'project.task', 'read',
    [[TASK_ID], ['progress', 'stage_id', 'description', 'name']])
print(result)
```

## Common mistakes to never repeat

1. ✅ unit_amount = **minutes** (120), NOT hours (2.0)
2. ✅ Descriptions = **human paragraphs**, NOT bullet lists
3. ✅ Always check **current stage** before deciding if it needs changing
4. ✅ Always set **progress** when completing work (1.0 = 100%)
5. ✅ Always **verify** after write (read back and confirm)
6. ✅ Use **HTML `<p>` tags** for multi-paragraph Odoo descriptions
7. ❌ Never touch Moqtana Odoo unless explicitly told
