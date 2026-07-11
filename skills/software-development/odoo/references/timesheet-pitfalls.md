# Timesheet (account.analytic.line) — Common Pitfalls

## employee_id ≠ res.users ID (CRITICAL)

When creating `account.analytic.line` records, `employee_id` is the **`hr.employee` ID**, NOT the `res.users` ID.

- User `res.users` ID 151 (Sultan Issa) → `hr.employee` ID **975** (`محمد سلطان عباس عيسى`)
- Always verify: `models.execute_kw(db, uid, api_key, 'res.users', 'read', [[user_id]], {'fields': ['employee_id']})`
- Using the wrong ID gives: `Fault: 'Timesheets must be created with an active employee in the selected companies.'`

```python
# CORRECT — find employee_id from user record
user_rec = models.execute_kw(db, uid, api_key, 'res.users', 'read',
    [[151]], {'fields': ['id', 'name', 'employee_id']})
employee_id = user_rec[0]['employee_id'][0]  # 975

# Then use employee_id in timesheet creation
timesheet_id = models.execute_kw(db, uid, api_key, 'account.analytic.line', 'create', [{
    'task_id': 2947,
    'project_id': 219,
    'employee_id': employee_id,
    'unit_amount': 30.0,  # minutes
    'name': 'Description of work',
    'date': today,
}])
```

## unit_amount is in minutes

Per user preference: `unit_amount` is stored in **minutes**, not hours. 30.0 = 30 minutes.

## Required fields for account.analytic.line

| Field | Type | Notes |
|-------|------|-------|
| `task_id` | many2one | `project.task` ID |
| `project_id` | many2one | `project.project` ID (219 = Aseer Museum) |
| `employee_id` | many2one | `hr.employee` ID (NOT res.users ID) |
| `unit_amount` | float | Duration in minutes |
| `name` | char | Description of work done |
| `date` | date | YYYY-MM-DD |
