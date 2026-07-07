---
name: odoo-task-injection
description: Create standardized Odoo tasks — project setup, task injection, batch updates, and tender-phase management — for Samaya Odoo instances.
---

⚠ **General execution rule: always rewrite user prompts through Codex CLI (`codex exec --skip-git-repo-check "rewrite: ..."`) before executing.** This refines vague requests into specific actionable steps. Saved as a standing preference — do not skip.

Create standardized Odoo tasks in **Samaya Odoo (project 219 — Aseer Museum)** with proper hierarchy, metadata, and logging.

See `references/design-study-workflow.md` for the full pattern of extracting PDF design docs → creating organized MD summaries → updating proposals + Odoo tasks.

## Connection

```python
import xmlrpc.client, os, ssl
from datetime import date
ctx = ssl._create_unverified_context()
url = 'https://samayainv.odoo.com'
db = 'peerless-tech-samaya-18-0-18447146'
login = 'sultan@samayainvest.com'
with open(os.path.expanduser('~/.config/samaya/odoo.env')) as f:
    for line in f:
        if 'ODOO_API_KEY' in line and '=' in line: pw = line.split('=', 1)[1].strip()
transport = xmlrpc.client.SafeTransport(context=ctx)
common = xmlrpc.client.ServerProxy(url + '/xmlrpc/2/common', transport=transport)
uid = common.authenticate(db, login, pw, {})
models = xmlrpc.client.ServerProxy(url + '/xmlrpc/2/object', transport=transport)
```

## Hierarchy Rules

| Level | `parent_id` | Appears In |
|-------|-------------|------------|
| **MAIN TASK** | `False` | Kanban as card |
| **SUBTASK** | Package ID | Package's Sub-tasks tab |
| **SUB-SUBTASK** | Stage-sub ID | Stage subtask's children |

## Stage IDs & Package IDs

| Stage | ID | Key Packages | ID |
|-------|----|-------------|-----|
| Initiation | 35 | 00 — Pre-Qual | 3011 |
| DD Stage | 36 | 00 General / 01 Architecture / 02 Structural / 03 MEP / 04 Life Safety / 05 Projects Plans | 2945/2938/2939/2940/2941/2946 |
| Procurement | 39 | S00101 Contract Scope | 3013 |
| Manufacturing | 659 | — | — |
| On-site Work | 40 | — | — |
| Handover | 479 | — | — |

### Task Placement Guide

Use these rules to decide which stage/package to use for a new task:

| Document/Activity Type | Stage | Package ID | Rationale |
|------------------------|-------|-----------|-----------|
| **Prequal submission received** | 35 — Initiation | 3011 (00 — Pre-Qual) | Prequal review happens before procurement |
| **CG Response (Code B/C) on a submittal** | 39 — Procurement | 3146 ([REF] S00101 — Procurement & Material Submittals) | Submittal review + response tracking |
| **Design deliverable creation (DD stage)** | 36 — DD Stage | Per discipline pkg (2938 Architecture, 2939 Structural, etc.) or 2945 (00 — General) | Design deliverables under development |
| **Material sample/procurement submittal** | 39 — Procurement | 3146 or per-material package | Procurement & material approval |
| **RFI / Technical Query** | 36 — DD Stage | Per discipline pkg | Design clarification |
| **Site instruction received** | 40 — On-site Work | — | Site-level action |
| **Shop drawing submittal** | 39 — Procurement | 3146 | Contractor submittal review |

## Creating a New Project

When the task requires creating a new project (not just tasks under an existing one):

```python
# Discover the company ID first
companies = models.execute_kw(db, uid, pw, "res.company", "search_read", [[]],
    {"fields": ["id", "name"]})
# Samaya Investment = ID 1

pid = models.execute_kw(db, uid, pw, "project.project", "create", [{
    "name": "Project Name — Tender Stage",
    "stage_id": PORTFOLIO_STAGE_ID,   # See portfolio stages below
    "user_id": USER_ID,
    "company_id": COMPANY_ID,         # REQUIRED — project must have a company
    "allow_timesheets": True,
    "description": "<h3>Title</h3><p>Description...</p>",
}])
```

⚠ `company_id` is REQUIRED when creating a new `project.project` — without it Odoo raises `Fault 2: "This project is not associated with any company"`. Always query `res.company` first.

### Portfolio Stages (`project.project.stage`)

| ID | Name | Use |
|----|------|-----|
| 12 | Tendering | Pre-award tender/bid phase |
| 13 | Award / Initiation | After award, before start |
| 14 | Inquiry & Brief | Early client enquiry |
| 15 | Estimation & Quotation | Pricing stage |
| 5 | In Progress | Active execution |
| 3 | Done | Completed |

## Tender / Bid Stage Mapping

When creating tasks for a **tender-phase project**, map tender phases to these Odoo task stages:

| Tender Phase | Odoo Stage | ID | Rationale |
|-------------|------------|----|-----------|
| Mobilisation & Kick-Off | 01 Initiation | 35 | Early setup, no design content |
| Site Visit | 01 Initiation | 35 | Pre-scope fact-finding |
| Scope Review / RFI | 02 Design Development (DD) Stage | 36 | Technical scope analysis |
| Pricing & Estimation | 03 Procurement | 39 | Supplier enquiries, take-offs |
| Technical Proposal | 02 Design Development (DD) Stage | 36 | Technical document creation |
| Commercial Proposal | 03 Procurement | 39 | Pricing, rates, bid docs |
| Programme & Methods | 02 Design Development (DD) Stage | 36 | Schedule + method statements |
| Review & Submission | Tender/DD Support | 37 | QA, sign-off, delivery |
| Post-Submission | Tender/DD Support | 37 | Clarifications, archive |

## Batch Date Updates (Hard-Deadline Compression)

When a tender deadline moves up and all tasks must finish by a single date, update all dates in parallel:

```python
deadlines = {
    # key phrase in task name -> (date_assign, date_deadline)
    "01 — Tender Document": ("2026-06-25", "2026-06-28"),
    "02 — Tender Strategy": ("2026-06-25", "2026-06-26"),
    # ... all tasks
}
for task in all_tasks:
    for key, (assign, deadline) in deadlines.items():
        if task["name"].startswith(key):
            models.execute_kw(db, uid, pw, "project.task", "write", [[task["id"]], {
                "date_assign": assign,
                "date_deadline": deadline,
                "state": "01_in_progress",
            }])
```

**Principle:** With a hard deadline, tasks run in parallel across all phases, not sequentially. Earlier task deadlines become the start of dependent phases rather than the finish of the phase.

## Batch Progress / State Updates

After completing a batch of work (e.g., end of day), update state + progress + log timesheets in one pass:

```python
updates = {
    TASK_ID: {"state": "1_done", "progress": 1.0},     # completed
    TASK_ID: {"state": "01_in_progress", "progress": 0.5},  # in progress
    TASK_ID: {"state": "01_in_progress", "progress": 0.0},  # not started
}
for tid, vals in updates.items():
    models.execute_kw(db, uid, pw, "project.task", "write", [[tid], vals])

# Log timesheets for done tasks
for tid in done_tasks:
    task = [t for t in all_tasks if t["id"] == tid][0]
    models.execute_kw(db, uid, pw, "account.analytic.line", "create", [{
        "task_id": tid,
        "project_id": PROJECT_ID,
        "unit_amount": 2.0,
        "name": f"Tender work: {task['name']}",
        "date": str(date.today()),
    }])
```

Always **read back after writes** to verify the values persisted.

## Team

| Name | ID | Role |
|------|----|------|
| Sultan Issa | 151 | Tech Office Manager |
| Mohamed Samir | 564 | Procurement/Site |
| Hani Alghamdi | 478 | Purchasing |
| Hesham | 163 | Document Control |
| Ahmed Salah | 162 | Coordination |
| Ali Abdelrahman | 160 | Tech Office (design) |
| Mohamed Elshaikh | 157 | Planner |
| SAMAYA WORKSHOP | 155 | Workshop buyer (login: workshop@samayainvest.com) |
| Ibrahim Shaaban | 169 | Finance — posts transfer receipts on POs when paid |

## Purchase Order Export (SAMAYA WORKSHOP)

See `references/odoo-po-export-cron.md` for the full pattern — creating a no_agent=True daily cron that pulls purchase orders from Odoo to an Excel tracker.

Key facts:
- SAMAYA WORKSHOP user_id = 155 (used in `[('user_id', '=', 155)]` domain)
- Purchase Order model: `purchase.order`
- States: `draft` (RFQ), `sent` (RFQ Sent), `to approve`, `purchase` (Purchase Order), `done` (Locked), `cancel`
- Receipt status: `no` (Not Received), `partial` (Partially Received), `full` (Received)
- Invoice/Billing status: `no` (Not Billed), `to invoice` (Waiting Bills), `invoiced` (Billed)
- Payment confirmation: NOT available as a field — only indicated by Ibrahim Shaaban posting transfer receipt image as a message on the PO
- Tracker file: `Orders/2026/0000 اداريات/شراء/ورشة المشتريات.xlsx` (daily cron `fa074c0eb9dd` at 14:00)

## Create Template

```python
tid = exec_kw('create', [{
    'name': '[DOC-CODE] — Title',
    'project_id': 219,
    'stage_id': 36,
    'parent_id': PACKAGE_ID,  # False for MAIN
    'user_ids': [(4, USER_ID)],
    'tag_ids': [(4, TAG_ID)],
    'date_assign': str(date.today()),
    'date_deadline': str(date.today()),
    'state': '01_in_progress',
    'progress': 0.5,
    'display_mark_as_done_primary': False,
    'description': '<h3>Title</h3><p><b>Context:</b>...</p>',
}])
```

## State → Progress

| State | Progress |
|-------|----------|
| `1_done` / `03_approved` | 1.0 |
| `02_changes_requested` | 0.5 |
| `01_in_progress` | 0.25-0.75 |

## Daily DD Update (Cron)

See `references/daily-dd-update.md` — a `no_agent=True` cron job that checks Outlook daily and records email activity in the DD packages' descriptions. Runs at 11:00 daily.

## Session Time Tracking (Mandatory)

After completing work on any Odoo task, **always log session time** to `account.analytic.line` via XML-RPC:

```python
m.execute_kw(db, uid, pw, 'account.analytic.line', 'create', [{
    'task_id': TASK_ID,       # project.task ID
    'project_id': PROJECT_ID, # use the actual project ID
    'unit_amount': 3.0,       # hours (estimate based on session effort)
    'name': 'Description of work done in this session',
    'date': str(date.today()),
}])
```

This is a standing requirement — Mohamed explicitly corrected: "always update the time sheet in the task with session time, always track my time in task by session time." Do NOT skip this step after any task work.

See `references/tender-project-setup.md` for the full RCRC Exhibition tender project pattern (creation, batch date updates, batch progress updates, timesheet logging).

## Log

Append to `Email_Archive/_aseer_tasks_backlog.md` with a table row.

## Deadline Principles

### User Expects Aggressive Timelines — Not Default 2-Week Windows

**When setting initial task dates, default to parallel execution with tight deadlines — not sequential with generous buffers.**

The user corrected: "submitt all before july 1" when the initial schedule had tasks spread across 8 weeks. Key rules:

- **All phases run in parallel under a hard deadline.** Pricing, proposals, programme, and scope review all start on day 1, not sequentially.
- **Initial deadline windows should be 3-5 days, not 14 days.** A task starting Monday finishes Thursday, not next month.
- **If a tender period is 6 days (not 8 weeks), every task starts immediately.** There is no "wait for Phase 1 to finish before Phase 2" — everything runs concurrently.
- **The deadline always comes from the baseline programme or the submission date.** Never set dates in isolation — derive them from the critical path to submission.

### Task Structure: Split Proposal Work into Separate Phases

Technical proposal, commercial proposal, and programme are **three independent workstreams** — not sub-tasks of a single "Proposal Preparation" phase. Each has its own deliverables, reviewers, and timeline. Never bundle them.

### Site Visit Is a Standalone Phase

The site visit is not a subtask of Scope Review — it's its own phase with before/during/after workflow. It's a critical milestone that feeds pricing, methodology, and RFI log. Make it a distinct phase.

## Pitfalls

- `read()` returns list: `task[0]['name']` not `task['name']`
- User/tag IDs: `[(4, id)]` to append or `[(6, 0, [id1,id2])]` to replace
- Always verify `date_assign <= date_deadline` after date changes
- **Before marking a task as "not started" or low-progress, check the project folder for existing files.** Previous sessions may have created deliverables stored in the project folder or `_PRICING_DOCS/` — search the filesystem for the deliverable filename mentioned in the task description or the TENDER_PLAN.md.
- **Always update Odoo when creating new deliverables.** User confirmed "yes always update" — after generating any document, append the file info to the relevant Odoo task's description and log a timesheet.
- **Use `company_id` when creating new projects.** Without it, Odoo raises `Fault 2: "This project is not associated with any company"`. Always discover via `res.company.search_read` first.
- **"Done" activity status = paid.** (No, this was wrong — kept for the pattern. "Done" activity status is NOT paid. Payment confirmed only by transfer receipt.)
- After state changes, run progress sync + parent recalc
- **`progress` field may not write in batch.** When updating many tasks with `{'state': ..., 'progress': N, 'description': ...}`, some records may retain their old progress. Always make a **second pass** to write only `progress`, then **read back to verify**.
- **Always read back after writes.** After any `write` call on multiple records, `search_read` or `read` the affected IDs back to confirm values took.
- **Maintain full email thread context in descriptions.** When updating a task with CG response details, include the full email timeline, each party's feedback, and the correct status from the email header.
- **The CG response email carries the official status, not the attached PDF narrative.** The email may say "C — Revise and Resubmit" while the PDF says "generally accepted." Always use the email's code as the task status.
