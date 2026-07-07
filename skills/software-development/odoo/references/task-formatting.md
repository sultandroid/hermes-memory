# Odoo Task & Timesheet Formatting

## Task description format

Odoo task descriptions accept HTML. Use this format — no icons, no emoji, no AI language:

```python
description = """<p>Brief summary of the task.</p>

<p><b>Scope</b></p>
<ul>
<li>Bullet point one</li>
<li>Bullet point two</li>
</ul>

<p><b>Deliverables</b></p>
<ul>
<li>Deliverable one</li>
</ul>

<p><b>Next Steps</b></p>
<ul>
<li>Step one</li>
</ul>"""
```

Rules:
- No emoji, no icons, no decorative characters
- No AI fingerprints ('delve', 'leverage', 'seamlessly', 'cutting-edge')
- Write as a human engineer would — short factual bullets
- Use `<b>` for section headers, not `<h1>`/`<h2>`

## Timesheet entries

`unit_amount` is in **hours** (e.g. 3.5 = 3 hours 30 minutes). Not minutes.

```python
timesheet_data = {
    'task_id': task_id,
    'project_id': project_id,
    'employee_id': employee_id,  # Use hr.employee id, not res.users id
    'name': 'Description of work done',
    'unit_amount': 3.5,  # hours
    'date': '2026-07-06',
}
```

## Subtask creation

Create subtasks under a parent by setting `parent_id`:

```python
subtask = {
    'project_id': parent_project_id,
    'name': 'Subtask Name',
    'parent_id': parent_task_id,
    'stage_id': stage_id,
    'description': '<p>HTML description</p>',
    'user_ids': [(4, user_id)],
    'date_assign': 'YYYY-MM-DD',
    'date_deadline': 'YYYY-MM-DD',
}
```

## Common pitfalls

- Employee ID is NOT the same as user ID. Look up via `hr.employee` model, not `res.users`.
- SSL cert verification fails on macOS Python 3.13 — use `ssl._create_unverified_context()`.
- Odoo project names may be in Arabic — search with `ilike` and partial terms.
- Stage IDs are project-specific. Always fetch stages for the target project first.
