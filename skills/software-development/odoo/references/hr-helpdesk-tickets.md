# Odoo HR / Helpdesk Ticket Creation (Samaya)

How to create HR helpdesk tickets and look up employee/leave data on the Samaya Odoo instance.

## Helpdesk tickets (HR) — NOT project.task

HR/administrative requests (return-to-work, salary disputes, leave, visas, hiring) go in the
**`helpdesk.ticket`** model, NOT `project.task`. The user corrected this: "لا اعتقد بتكون في Ticket support model, hr".

- **Team:** `helpdesk.team` id **10** = "Human Resources And Administration"
- **Stages** (`helpdesk.stage`, team 10): 1 New · 6 Waiting · 2 In Progress · 4 Solved · 5 Cancelled
- **Fields:** `name`, `team_id`, `stage_id`, `partner_id` (the requester's contact), `user_id` (assigned HR officer), `description` (HTML), `priority` ("0"=normal)
- Other teams: 12 Customer Care · 1 IT Help Desk · 11 Legal affair · 15 Odoo Helpdesk

### Create pattern
```python
from odoo_connect import connect
uid, models, cfg = connect('samaya')
tid = models.execute_kw(cfg['db'], uid, cfg['pw'], 'helpdesk.ticket', 'create', [{
    'name': '...',
    'team_id': 10,
    'stage_id': 1,          # New
    'partner_id': 5503,     # requester contact
    'description': '<p>...</p>',
}])
```

## User's own employee / partner identity (Samaya)

- **Employee:** محمد سلطان عباس عيسى — `hr.employee` id **975**, job 569 "Factory Manager", dept 18 "Samaya / Manufacturing", work_email sultan@samayainvest.com
- **Partner (work_contact_id):** id **5503** "Sultan Issa" — use this as `partner_id` on the user's own tickets
- Find by email: `hr.employee` search `[['work_email','=','sultan@samayainvest.com']]` or `[['user_id','=',151]]`

## Leave (hr.leave) lookup

- Model `hr.leave`; filter `[['employee_id','=',975]]`
- User's annual leave 2026: id **1487**, Annual leave (type 1), 26 days, 19-07-2026 → 13-08-2026, state `validate`
- Leave types: 1 Annual · 11 Sick · 13 Excuse · 7 Marriage · 12 Unpaid · 18 Hajj · 8 Bereavement · 19 Exam · 16/21 maternity · 20 paternity

## Access / field pitfalls

- **`hr.payslip` is NOT readable by user 151** — requires Payroll/Officer group. Do not attempt; report the access block instead.
- **`hr.employee.address_home_id` does NOT exist** — invalid field error. Use `work_contact_id` for the partner.
- `hr.leave.private_name` requires "Time Off / Officer: Manage all requests" — omit it.

## Context: user's assignment allowance

The user (Factory Manager) was assigned to also manage the Technical Office since ~Jul 2025 for a
**5000 SAR/month** assignment allowance. Company policy deducts this allowance during annual leave.
The user disputes the deduction because the Technical Office role is administrative and was still
followed (remotely) during leave. This is the recurring subject of his HR tickets.
