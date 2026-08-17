# Odoo HR — Employee & Contract Field Access (Samaya)

Sultan's account (uid 151) has LIMITED HR rights. Know what you can/can't read before querying.

## Access matrix (uid 151)

| Model / field | Access | Notes |
|---|---|---|
| `hr.employee` basic fields (name, job_title, department_id, work_email, work_phone, active, company_id) | ✅ | |
| `hr.employee` sensitive fields (identification_id, gender, birthday, marital, country_id, notes, contract_id) | ❌ | Needs group `Employees / Officer: Manage all employees` |
| `hr.contract` (any read) | ❌ | Needs `Contracts/Administrator` or `Contracts/Employee Manager` |
| `hr.contract.line`, `batch.contract.line`, `hr.employee.contract` | ❌ | Same contract groups |
| `batch.contract` | ✅ | But ONLY fields: name, employee_count, create_date. **No dates, no wage, no employee list.** It's a pure grouping header. |

## Field-name gotchas on hr.employee

- `date_of_hire` — **does not exist** (ValueError: Invalid field).
- `hire_date` — exists but is a **char** (string), not a date; often `False`.
- `create_date` — record-creation datetime, NOT the actual contract start date. Do not present it as the hire date.
- `work_location` — does not exist on hr.employee.
- `badge_ids` / `direct_badge_ids` — fingerprint/badge records; **empty for factory laborers**. Fingerprint numbers (e.g. 656, 664, 1171) live in the EXTERNAL attendance system, not Odoo. Don't expect to find them here.

## Departments (Samaya)

- 18 = Samaya / Manufacturing (الورشة/المصنع)
- 98 = Samaya / المستودع (warehouse) — complete_name "Samaya / المستودع", name field is "warehouse"
- 52 = Samaya (general)
- 95 = Finance, 97 = IT, 17 = Project Management

## Practical recipe — list a department's workers

```python
ids = models.execute_kw(db, uid, pw, 'hr.employee', 'search', [[['department_id','=',18]]])
recs = models.execute_kw(db, uid, pw, 'hr.employee', 'read', [ids],
    {'fields':['name','job_title','active']})
```

## Moving an employee to another department

```python
models.execute_kw(db, uid, pw, 'hr.employee', 'write', [[emp_id], {'department_id': 98}])
# verify:
models.execute_kw(db, uid, pw, 'hr.employee', 'read', [[emp_id]], {'fields':['name','department_id']})
```

## Pitfall — employee ID vs name

User may give a wrong numeric ID (e.g. "سهيل رقمه 898"). Always `read` the ID first and confirm the name matches before writing. سهيل = **موحد سهيل عارف, id 1629** (898 is a different, inactive employee). Verify before any department move.

## Contract end dates

Real contract start/end dates are in `hr.contract` (blocked). If you cannot get access, source end dates from the user or from chat/email evidence (e.g. Raouf stated محمود النجار + حسن البرمبالي contracts end 18/10/2026). Never fabricate dates from `create_date`.
