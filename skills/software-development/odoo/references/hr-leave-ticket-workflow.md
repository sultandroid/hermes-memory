# Odoo HR Leave → project.task Ticket Workflow

Creating a "مباشرة العمل بعد الإجازة" (return-to-work) or any HR-leave ticket on Samaya Odoo.

## CRITICAL: "my leave" vs "someone else's leave"
When the user says "مباشرة العمل بعد الاجازه" (return to work after leave) with no name,
they almost always mean **their OWN leave** — NOT the Shamshad/other-employee email that
happens to be in the inbox. Do not assume the ticket is about a name you saw in a recent
email. Confirm the subject employee before drafting. (User corrected this: "لا بتاعتي انا".)

## Find the employee record
Arabic names do NOT match `ilike` with Latin queries, and `ilike 'شامشاد'` may return
nothing. Look up by **work_email** or **user_id** instead:

```python
# by email (reliable)
emps = models.execute_kw(db, uid, pw, 'hr.employee', 'search_read',
    [[['work_email','=','sultan@samayainvest.com']]],
    {'fields':['id','name','job_id','department_id','work_email']})
# by user_id (the Odoo login uid)
emps = models.execute_kw(db, uid, pw, 'hr.employee', 'search_read',
    [[['user_id','=',151]]], {'fields':['id','name']})
```

Known: **محمد سلطان عباس عيسى** = employee id **975**, user id **151**, Factory Manager,
dept Samaya/Manufacturing, work_email sultan@samayainvest.com.

## Query the leave (hr.leave)
Useful fields: `id, name, holiday_status_id, date_from, date_to, state,
number_of_days, request_date_from, request_date_to, employee_id`.

```python
leaves = models.execute_kw(db, uid, pw, 'hr.leave', 'search_read',
    [[['employee_id','=',975]]],
    {'fields':['id','name','holiday_status_id','date_from','date_to','state',
               'number_of_days','request_date_from','request_date_to'],'limit':20})
```

- `state='validate'` = approved.
- `name` often carries the leave-coordination note (who covered the work) — include it
  in the ticket description.
- Leave types: 1=Annual, 11=Sick, 12=Unpaid, 13=Excuse, 7=Marriage, 8=Bereavement,
  18=Hajj, 19=Exam, 20=Paternity, 21=Maternity.

## PITFALL: `private_name` access denied
`hr.leave.private_name` requires group "Time Off / Officer: Manage all requests".
A normal user (uid 151) gets `Fault 4: You do not have enough rights to access the
fields "private_name"`. Drop it from the field list — `name` is sufficient.

## Where the ticket goes
- **Internal project = 237**, stage **1 = Internal**. This is where HR/time-off/attendance
  tickets live (has child tasks Training=1007, Meeting=1008, Time Off=1009).
- Factory project 161 (مصنع سمايا) is for manufacturing work orders, not HR tickets.
- Create with `project.task` `create`:
  ```python
  models.execute_kw(db, uid, pw, 'project.task', 'create', [{
      'name': 'مباشرة العمل بعد الإجازة — <employee>',
      'project_id': 237,
      'stage_id': 1,
      'user_ids': [(4, 151)],   # assignee
      'description': '<leave details + coordination note>',
  }])
  ```

## Draft ticket description template
```
مباشرة العمل بعد انتهاء الإجازة السنوية.

بيانات الإجازة:
- الموظف: <name> (<job>)
- نوع الإجازة: <holiday_status>
- المدة: <number_of_days> يوم
- من: <request_date_from>  إلى: <request_date_to>
- الحالة: <state>

ملاحظة الإجازة: <name / coordination note>

تاريخ مباشرة العمل: <end date>
```
Confirm the return date (leave end vs today) with the user before creating.
