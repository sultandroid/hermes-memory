---
name: odoo-timesheet-logger
description: Log Hermes session work to Odoo timesheets (account.analytic.line) via XML-RPC. Reads task map from ~/.hermes/odoo_task_map.md, appends to worklog at ~/.hermes/worklog.md, and creates timesheet entries.
version: 1.0
author: Hermes Agent
---

# Odoo Timesheet Logger

## When to Use
At end of every Hermes session where work was done for Samaya/Aseer Museum projects. Also when user asks to log hours.

## Prerequisites
- `~/.config/samaya/odoo.env` with ODOO_URL, ODOO_DB, ODOO_USER, ODOO_API_KEY
- `~/.hermes/odoo_task_map.md` — project/task ID reference
- `~/.hermes/worklog.md` — session log file

## Steps

### 1. Read the task map
```
cat ~/.hermes/odoo_task_map.md
```
Identify the correct task IDs for the work done.

### 2. Log to worklog
Append to `~/.hermes/worklog.md`:
```
YYYY-MM-DD | HH:MM | Duration | Task(s) | Description | Odoo Task IDs
```

### 3. Create Odoo timesheet entries
Use XML-RPC to `account.analytic.line`:
```python
models.execute_kw(db, uid, pw, 'account.analytic.line', 'create', [{
    'task_id': TASK_ID,
    'project_id': PROJECT_ID,
    'unit_amount': 120,       # MINUTES, not hours (120 = 2h)
    'name': 'Description of work',
    'date': 'YYYY-MM-DD',
}])
```

### 4. Verify
Read back the created entries to confirm.

## CRITICAL RULES (never forget)

### unit_amount = minutes, not hours
`unit_amount` is in **minutes** (integer), not hours. 2 hours = 120, not 2.0.
Example: `{'unit_amount': 120}` for 2 hours of work.

### Task descriptions — human writing, not AI bullets
Descriptions must read like a person wrote them. One or two natural paragraphs.
NO bullet lists, NO section headers, NO meta-commentary ("this document covers...").
Write as: "Prepared the XYZ document for the Zamzam Museum. Covered the full approach for..."
Not: "- Section 1: ...\n- Section 2: ..."

### Task updates — natural language
When updating task descriptions via Odoo, write a short paragraph explaining what was done, not a structured breakdown.

## Pitfalls
- `unit_amount` is in **minutes** (integer), not hours
- `task_id` must be an integer, not False
- `project_id` is required for timesheet entries
- Employee is auto-linked from the authenticated user
- Don't log more than 8-10 hours per day per task
- Always verify by reading back after write
- **Private tasks reject timesheets** — Odoo returns `Fault 2: 'Timesheets cannot be created on a private task.'` if the task has `privacy_visibility` set to 'private' (e.g. task #203). Before logging, verify the task accepts timesheets by checking its `privacy_visibility` field. If private, use a different task (e.g. #3008 Daily Reports) or ask the user which task to use.
- **Corporate Odoo SSL cert issues** — Some corporate Odoo instances use self-signed or internal CA certs. The default `xmlrpc.client.ServerProxy` will fail with `SSL: CERTIFICATE_VERIFY_FAILED`. Use a custom transport with `ssl._create_unverified_context()`:
  ```python
  import ssl, http.client, xmlrpc.client
  ctx = ssl._create_unverified_context()
  class SafeTransport(xmlrpc.client.Transport):
      def make_connection(self, host):
          return http.client.HTTPSConnection(host, context=ctx)
  common = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/common', transport=SafeTransport())
  models = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/object', transport=SafeTransport())
  ```
  Also check `allow_timesheets` field on the task (not `privacy_visibility` — that field doesn't exist on `project.task` model in Odoo 18).

## Task Map Reference
Key Aseer tasks: 2891 (Life Safety), 3215 (MEP Scope), 2883 (Admin Block), 3211 (Stakeholder Plan), 2893 (Wall Types), 3008 (Daily Reports), 1721 (RFI #16), 1718 (RFI #18), 1716 (RFI #19), 3208 (BIM Review), 3296 (LiDAR MOS), 1660 (Cooling Load), 2880/2887/2888 (Replica Fab), 3134 (50% Design), 3090 (Lighting), 3298 (4D BIM), 3075-3096 (DD deliverables), 3147/3148 (Materials), 3198-3164 (Procurement).

Key RCRC tasks: 3364-3378 (tender phase).
