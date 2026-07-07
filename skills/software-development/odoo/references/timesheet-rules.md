# Odoo Timesheet Rules (Samaya)

**Critical Rules**

- `unit_amount` is in **MINUTES**, not hours.
  - 60 = 1 hour
  - 120 = 2 hours
  - 30 = 30 minutes

- Task descriptions must be **plain text only** — no emoji, no icons, no special characters.

**Example**
```python
models.execute_kw(db, uid, pw, 'account.analytic.line', 'create', [{
    'task_id': 3370,
    'name': 'Technical proposal - sections 14-20, 33, 34, 36 redesign',
    'unit_amount': 240,  # 4 hours
    'date': '2026-06-27',
    'project_id': 324,
}])
```