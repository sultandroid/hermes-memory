# Samaya Odoo — HR Helpdesk Tickets (helpdesk.ticket)

HR requests (مباشرة عمل / return-to-work, salary disputes, HR admin requests) are **NOT** `project.task`.
They live in the **`helpdesk.ticket`** model, team **"Human Resources And Administration" (id 10)**.

## Model & key fields
- Model: `helpdesk.ticket`
- Team: `helpdesk.team` — HR = id **10** (also: 1 IT Help Desk, 11 Legal, 12 Customer Care, 15 Odoo Helpdesk)
- Stage: `helpdesk.stage` — HR stages: **1 New, 2 In Progress, 4 Solved, 5 Cancelled, 6 Waiting**
- `partner_id` = the requester's `res.partner` (use the employee's `work_contact_id`, NOT the employee record)
- `user_id` = assigned HR officer (e.g. Ahmed Alrabaei, id 177)
- `description` = HTML body (use `<p>` tags)
- `priority` = "0" (normal)

## Finding the requester's partner
The employee's `work_contact_id` is the partner to set on the ticket:
```python
e = models.execute_kw(db, uid, pw, 'hr.employee', 'read', [[emp_id]],
    {'fields':['id','name','work_contact_id','work_email']})
# partner_id = e[0]['work_contact_id'][0]
```

## Finding the employee & their leave
- Employee lookup: `hr.employee` search by `work_email` (e.g. `sultan@samayainvest.com`) or `user_id`.
- Leave: `hr.leave` search by `employee_id`; fields `holiday_status_id`, `date_from`, `date_to`, `state`, `number_of_days`, `request_date_from/to`.
- Leave types (`hr.leave.type`): 1 Annual, 11 Sick, 12 Unpaid, 13 Excuse, 7 Marriage, 8 Bereavement, 18 Hajj, 19 Exam, 20 Paternity, 21 Maternity.

## Access notes
- `hr.payslip` is **read-restricted** for non-payroll users (Fault 4). Don't try to read payslips as a normal user.
- `hr.employee` field `address_home_id` does NOT exist on this instance — use `work_contact_id`.

## Example: create an HR ticket
```python
models.execute_kw(db, uid, pw, 'helpdesk.ticket', 'create', [{
    'name': 'اعتراض على خصم 5000 ريال — تكليف المكتب الفني',
    'team_id': 10,
    'stage_id': 1,
    'partner_id': 5503,          # Sultan Issa work_contact_id
    'priority': '0',
    'description': '<p>السلام عليكم،</p><p>...</p>',
}])
```

## User context (Eng. Mohamed Sultan / Sultan Issa)
- Employee: محمد سلطان عباس عيسى, id **975**, Factory Manager, work_email sultan@samayainvest.com, work_contact_id = **Sultan Issa (5503)**.
- Annual leave 2026: id 1487, 26 days, 19-07-2026 → 13-08-2026, state validate.
- User prefers **formal, well-crafted Arabic** in HR tickets (not terse). He corrects wording to be more professional/legalistic.
