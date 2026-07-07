# Samaya Odoo — Factory Company Setup & ERP Tasks

Created from 2026-06-14 session where Samaya Factory (company ID 7) was set up as a separate Odoo entity with 16 implementation tasks.

## Company / Partner Setup

Samaya Factory (formerly "مصنع سمايا") was renamed to "Samaya Factory — كيان مستقل" and set as a separate company entity:

```python
# Update res.company
models.execute_kw(db, uid, pw, 'res.company', 'write', [[7], {
    'name': 'Samaya Factory — كيان مستقل',
    'parent_id': False,   # Separate from Samaya Investment
}])

# Also update res.partner (companies are also partners in Odoo)
models.execute_kw(db, uid, pw, 'res.partner', 'write', [[7], {
    'name': 'Samaya Factory — كيان مستقل',
    'company_type': 'company',
}])
```

## Factory Setup Project

- **Project ID:** 302 (Odoo Factory Requests)
- **Project name:** Odoo Factory Requests (سمايا)
- **Location:** Samaya Odoo (samayainv.odoo.com), NOT Moqtana
- **Purpose:** Track ERP implementation tasks for the new factory company

### Task Creation Pattern for Setup Tasks

Tasks are created under a flat parent (no nested hierarchy) across ERP modules:

```python
tid = models.execute_kw(db, uid, pw, 'project.task', 'create', [{
    'name': 'DOC-CODE — Standardized Title',
    'project_id': 302,
    'stage_id': stage_id,          # Initiation or In-Progress
    'user_ids': [(4, user_id)],    # Assignee
    'date_assign': today,
    'date_deadline': today,
    'state': '01_in_progress',     # or 03_approved / 1_done
    'progress': 0.0,
}])
```

### Task Assignment Rules

| Assignee | Task Types |
|----------|------------|
| Sultan (151) | Quality Control, Factory IT infra, documentation |
| Kiwan (196) | Accounting, CRM, Invoices, Work Centers, Manufacturing Ops, Inventory, Purchase, Reports, HR |

### Stage Mapping (Project 302)

| Stage ID | Name | Use |
|----------|------|-----|
| 692 | 01 In-Progress / Follow-Up | Active implementation tasks |
| 479 | 06 Handover (As-Built & Snagging) | Completed setup tasks |

### X2M Quirk — Replacing user_ids

When re-assigning tasks to a different user, use `(6, 0, [user_id])` to **replace** all users, not `(4, user_id)` which appends:

```python
# CORRECT — replaces all assignees with just Kiwan:
models.execute_kw(db, uid, pw, 'project.task', 'write', [[task_id], {
    'user_ids': [(6, 0, [196])],
}])

# INCORRECT for re-assignment — appends Kiwan but Sultan remains:
models.execute_kw(db, uid, pw, 'project.task', 'write', [[task_id], {
    'user_ids': [(4, 196)],  # Sultan (151) is still assigned
}])
```

Use `(4, id)` when assigning multiple users to the same task (e.g. both Sultan and Kiwan).
Use `(6, 0, [id])` when you want ONLY one user on the task.
