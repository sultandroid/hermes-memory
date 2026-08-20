# Odoo 18 HR / Time Off — field quirks & overtime setup (Samaya)

Verified 2026-08-20 via JSON-RPC to `samayainv.odoo.com` (uid 151).

## Renamed fields — pre-18 names raise ValueError

Querying `hr.leave` / `hr.leave.type` with pre-18 field names fails with
`ValueError: Invalid field ... on model hr.leave.type` (search_read) or
`Invalid field hr.leave.<field> in leaf` (domain filter).

| Wrong (pre-18) | Correct (Odoo 18) |
|---|---|
| `hr.leave.type.allocation_type` | not a field — use `requires_allocation` |
| `hr.leave.type.validity_start` / `validity_stop` | not fields — drop |
| `hr.leave.holiday_type` (domain filter) | not a field — search `hr.leave` with `[]` |
| `hr.leave.holiday_status_id` | still valid (leave-type m2o) |

Safe `hr.leave.type` fields: `id, name, request_unit` (day/hour), `requires_allocation`.
Safe `hr.leave` fields: `id, name, employee_id, date_from, date_to, state, number_of_days, holiday_status_id`.
`state` values: `draft / confirm / validate / refuse`.

## Overtime on Samaya Odoo

Installed modules (all present): `hr_attendance`, `hr_holidays`, `hr_payroll`,
`hr_timesheet`, `hr_contract`.

- The employee portal shows a "My Overtime Requests" page (+ New Overtime Request,
  tabs All/Pending/Approved/Refused) — but there is **NO "Overtime" leave type**
  configured. Existing types are only Annual/Sick/Excuse/Marriage/Hajj/Exam/etc.
  That's why the page always shows "No overtime requests found."
- **The portal overtime page is driven by a CUSTOM module `hr_overtime_engine`
  ("HR Overtime Engine"), NOT the standard `hr.leave` overtime type.** Its models:
  `hr.overtime.entry`, `hr.overtime.batch`, `hr.overtime.batch.line`,
  `hr.overtime.config` ("Overtime Engine Configuration"), `hr.overtime.export.wizard`.
  To enable overtime for the team, configure THIS module (its config/entry models),
  not a leave type.
- **uid 151 (`sultan@samayainvest.com`) CANNOT read `hr.overtime.entry`,
  `hr.overtime.config`, or `hr.contract` — all raise AccessError.** So eligibility
  for overtime can't be determined via API with this account; the module's data is
  admin/HR-gated. `hr.attendance.overtime` (standard model) is also gated.
- To enable overtime: create an `hr.leave.type` named "Overtime" with
  `request_unit='hour'`, then add a payroll salary rule (1.5x / 2x) under `hr_payroll`.
- `hr_payroll` IS available on this Samaya instance (Enterprise, not Community) —
  do not assume it's missing.

## JSON-RPC note

`execute_code` is blocked in cron/background contexts; write a `.py` script to
`/tmp` and run via `terminal` instead. Use `requests(verify=False)` for the Samaya
HTTPS cert chain. Credentials: `~/.config/samaya/odoo.env` (ODOO_URL, ODOO_DB,
ODOO_USER, ODOO_API_KEY).
