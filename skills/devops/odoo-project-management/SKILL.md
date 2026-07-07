---
name: odoo-project-management
description: Manage Odoo 18 across two instances — Moqtana (project management) and Samaya (procurement/purchasing). Create POs, projects, tasks, milestones, and regenerate MD mapping files.
---

# Odoo Project Management — Two Instances

Mohamed Essa operates **two distinct Odoo 18 instances**. Know which one the task targets.

## ⚠️ Session Rules (User Preference — DO NOT MIX)

- **Sessions are project-stream-specific.** When the user says "this session is for X" (e.g., Moqtana/Tqanny, Aseer/Samaya), that stream is **exclusive** for the entire session.
- **Never cross-reference or mix contexts** between Moqtana and Aseer work in the same conversation. If the user corrects you with "dont mix work ok", stop immediately and refocus.
- **Project directories are separate**: Moqtana projects live under `~/OneDrive/Work/PWork/01_PROJECTS/Tqanny_Projects/`; Aseer Museum lives under the Aseer project path. Never assume a document or context from one applies to the other.
- If the user gives a project folder path, work exclusively with that project's documents, contracts, and Odoo records. Do not bring in references from other streams.

## Instance Quick Reference

| Instance | URL | DB | User | Purpose |
|----------|-----|----|------|---------|
| **Moqtana** | `http://167.99.224.43:8069` | `moqtana` | `mohamedsultanabbas@gmail.com` | Project management, tasks, milestones |
| **Samaya** | `https://samayainv.odoo.com` | `peerless-tech-samaya-18-0-18447146` | `sultan@samayainvest.com` | Procurement, POs, accounting |

- Moqtana details continue below.
- Samaya Odoo Purchase Orders → see `references/samaya-odoo-purchase-orders.md`

---

# Moqtana Odoo 18 (Project Management)

## Access
- **URL**: `http://167.99.224.43:8069`
- **DB**: `moqtana`
- **Admin**: `mohamedsultanabbas@gmail.com` / `1batagoniaA`
- **API**: XML-RPC at `/xmlrpc/2/common` (auth) and `/xmlrpc/2/object` (models)
- **Odoo 18 Community** — no custom modules, all config via scripts/API

## Custom Fields (created via ir.model.fields)
- `project.project.x_project_code` (char) — project code like `DAR-VIC`
- `project.task.x_planned_start` (date) — planned start date for tasks

## Naming Convention for Project Codes
| Pattern | Example | Usage |
|---------|---------|-------|
| `XXX-VC` | DAR-VIC, SHO-VIC, ALB-VC, ALF-VC, ANT-VC, TAB-VC | Visitor Centers |
| `XXX-ARC` | ARA-ARC | Archaeological Centers |
| `XXX-SQ` | SAH-SQ | Square projects |
| `URP-VC` | URP-VC | Urwa Palace VC |

## Project Serial Numbering
Every project must have:
1. **Name prefix**: `NN — Project Name` (e.g., `01 — Darin Visitor Center`)
2. **Odoo `sequence` field**: set in 10-step increments (`seq=10` → `seq=90`)
3. **Local folder**: `NN_Folder_Name` matching the serial (e.g., `01_Darin_Visitor_Center`)
4. **Project code**: set in `x_project_code` field

Serial order matches the folder numbering:
```
seq=10 | 01 — Darin      | 01_Darin_Visitor_Center
seq=20 | 02 — Shobra     | 02_Shobra
...
seq=90 | 09 — Urwa Palace| 09_Urwa_Palace_VC
```

## Compressed Timeline — Max 5 Weeks for Design Development

**Key constraint**: Design Development stage must not exceed 4-5 weeks total from project start. All dates are compressed accordingly:

| Stage | Start Day | Duration | Week |
|-------|-----------|----------|------|
| Brief & Discovery (9) | Day 0 | 5 days | Week 1 |
| Concept Design (10) | Day 5 | 5 days | Week 2 |
| Design Development (11) | Day 10 | 7 days | Week 3 |
| Procurement & Tender (12) | Day 17 | 12 days | Week 4-5 |
| Off-site Manufacturing (17) | Day 29 | 10 days | Week 5+ |
| Installation & Fitout (14) | Day 39 | 14 days | — |
| Snagging & Commissioning (15) | Day 53 | 7 days | — |
| Handover & Closeout (16) | Day 60 | 5 days | — |

**Within each package:**
- Subtasks spaced 2 days apart
- Each subtask: 3 day duration
- Base date: `2026-06-01` (project start)

### Setting Dates in Code
```python
from datetime import date, timedelta
base = date(2026, 6, 1)
stage_offsets = {
    9:  (0, 5),    # Brief: day 0, 5 days
    10: (5, 5),    # Concept: day 5, 5 days
    11: (10, 7),   # Design Dev: day 10, 7 days
    12: (17, 12),  # Procurement: day 17, 12 days
    17: (29, 10),  # Off-site: day 29
    14: (39, 14),  # Install: day 39
    15: (53, 7),   # Snagging: day 53
    16: (60, 5),   # Handover: day 60
}
for pkg in packages:
    stage_id = pkg['stage_id']
    start_off, dur = stage_offsets.get(stage_id, (0, 10))
    pkg_start = base + timedelta(days=start_off + pkg_idx * 2)
    pkg_end = pkg_start + timedelta(days=dur)
```

## Task Structure: Packages with Subtasks

Every project uses a **package → subtask hierarchy**:

1. **Parent tasks (packages)** = named `[Package Name]` with:
   - `sequence` in 10-step increments (10, 20, 30...) for ordering
   - `milestone_id` linked to appropriate milestone
   - `x_planned_start` + `date_deadline` set per compressed timeline

2. **Child tasks (subtasks)** = linked via `parent_id`, sequenced as `seq_package + n` (11, 12, 13...)

3. **MD files** in `Odoo Tasks/` show packages as `### N. 📦 Package Name 🔷 MS-XX Name`

### Setting Sequences
```python
# Set package sequence (10-step increments)
models.execute_kw(db, uid, password, 'project.task', 'write', [[parent_id], {'sequence': 10}])

# Set subtask sequence (within package)
models.execute_kw(db, uid, password, 'project.task', 'write', [[child_id], {'sequence': 11}])
```

## Portfolio Stages (project.project.stage)
| ID | Stage | Use |
|----|-------|-----|
| 1 | Lead / Enquiry | Initial inquiry, very early |
| 5 | Tender / Bid | RFP issued, proposal submitted |
| 6 | Awarded | Contract awarded |
| 2 | In Progress | Active execution |
| 7 | On Hold | Paused |
| 3 | Completed | Done (folded) |
| 4 | Lost / Cancelled | Folded |

## Task Stages (project.task.type)
| ID | Stage | Sequence |
|----|-------|----------|
| 9 | Brief & Discovery | 10 |
| 10 | Concept Design | 20 |
| 11 | Design Development | 30 |
| 12 | Procurement & Tender | 40 |
| 17 | Off-site Manufacturing | 45 |
| 14 | Installation & Fitout | 60 |
| 15 | Snagging & Commissioning | 70 |
| 16 | Handover & Closeout | 80 |

## Milestones
Each project has **21 milestones** (01-21) auto-created from the template via the `08_new_project_template_automation.py` script on project creation.

### Linking Packages to Milestones
Every package task must set `milestone_id` to the appropriate milestone:

| Task Stage ID | Milestone Name |
|---------------|----------------|
| 9 (Brief) | 01 - Brief & Requirements Sign-off |
| 10 (Concept) | 02 - Concept Design Approved |
| 11 (Design Dev) | 03 - Design Development Approved |
| 12 (Procurement) | 04 - IFC Drawings Issued |
| 17 (Off-site) | 09 - Off-site Manufacturing Complete |
| 14 (Install) | 10 - Civil & Builders Work Complete |
| 15 (Snagging) | 19 - Testing & Commissioning Complete |
| 16 (Handover) | 21 - Client Handover & Closeout |

```python
# Get milestones for a project
milestones = models.execute_kw(db, uid, password, 'project.milestone', 'search_read',
    [[['project_id', '=', pid]]], {'fields': ['id', 'name']})
ms_by_name = {m['name']: m['id'] for m in milestones}

# Link package to milestone
models.execute_kw(db, uid, password, 'project.task', 'write', [[task_id], {
    'milestone_id': ms_by_name['01 - Brief & Requirements Sign-off']
}])
```

## Project-Task CRUD via XML-RPC

### Authenticate
```python
import xmlrpc.client
common = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/common')
uid = common.authenticate(db, login, password, {})
models = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/object')
```

### Create Project (with serial prefix)
```python
models.execute_kw(db, uid, password, 'project.project', 'create', [{
    'name': 'NN — Project Name (العربية)',
    'stage_id': 5,       # Tender/Bid
    'user_id': 2,        # Mohamed Essa
    'partner_id': 14,    # Heritage Commission
    'x_project_code': 'XXX-VC',
    'sequence': 10,      # 10-step increments
}])
```

### Create Package (Parent Task)
```python
parent_id = models.execute_kw(db, uid, password, 'project.task', 'create', [{
    'name': '[Package Name]',
    'project_id': project_id,
    'stage_id': stage_id,
    'user_ids': [(4, 2)],
    'x_planned_start': '2026-06-01',
    'date_deadline': '2026-06-15',
    'sequence': 10,
    'milestone_id': milestone_id,  # link to milestone
}])
```

### Create Subtask Under Package
```python
models.execute_kw(db, uid, password, 'project.task', 'create', [{
    'name': 'Task name',
    'project_id': project_id,
    'stage_id': stage_id,
    'parent_id': parent_id,
    'user_ids': [(4, 2)],
    'x_planned_start': '2026-06-01',
    'date_deadline': '2026-06-05',
    'sequence': 11,  # package_seq + n
}])
```

### Move Existing Task Under Package
```python
models.execute_kw(db, uid, password, 'project.task', 'write', [[task_id], {
    'parent_id': parent_id,
}])
```

### Update Multiple Tasks (batch dates, sequences)
```python
# Read all tasks for a project
tasks = models.execute_kw(db, uid, password, 'project.task', 'search_read',
    [[['project_id', '=', pid]]],
    {'fields': ['id', 'name', 'parent_id', 'stage_id', 'sequence']})

# Write in batch per task
models.execute_kw(db, uid, password, 'project.task', 'write', [[task_id], vals])
```

## Full Workflow: Folder Analysis → Odoo Setup

When a new project folder is added to `Tqanny_Projects/`:

1. **Analyze folder** — read Admin/, Client Inputs/, Submittals/, Design/ for SOW, ER, RFP, BOQ docs
2. **Create client partner** if new (e.g., Heritage Commission, Elm Company)
3. **Create project** in Odoo with serial name, code, stage, manager, client
4. **Analyze scope** and create packages with appropriate stage mapping
5. **Create subtasks** under each package
6. **Set sequences** (10-step for packages, sequential for subtasks)
7. **Link milestones** via `milestone_id`
8. **Set compressed dates** per timeline table above
9. **Create `Odoo Tasks/` subfolder** + `Odoo_Tasks_Map.md` in the project folder
10. **Create/update** `PROJECT_MEMORY.md` if needed

## MD Mapping File — Regeneration

After any task changes (dates, sequences, milestones, new tasks), regenerate the MD file:

```python
# Fetch all data: project info, milestones, packages with children
# Build markdown with:
# - Project header (code, ID, stage, timeline)
# - Packages listed as ### N. 📦 Name 🔷 Milestone
# - Package metadata: *stage · start → deadline*
# - Table of subtasks with #, Task, Start, Deadline
# Write to {folder}/Odoo Tasks/Odoo_Tasks_Map.md
```

MD file sections:
```
# NN — Project Name
| **Project Code** | `XXX-VC` |
| **Odoo ID** | `N` |
| **Timeline** | YYYY-MM-DD → YYYY-MM-DD |
| **Total Tasks** | N |

### 1. 📦 Package Name 🔷 01 - Milestone Name
*Stage · start → deadline*
| # | Task | Start | Deadline |
|---|------|-------|----------|
```

## Known Partners
| ID | Name |
|----|------|
| 14 | هيئة التراث — Heritage Commission |
| 15 | شركة علم — Elm Company |

## Current Projects (IDs 13-22)
| Seq | ID | Code | Project | Folder |
|-----|-----|------|---------|--------|
| 10 | 14 | DAR-VIC | 01 — Darin Visitor Center | `01_Darin_Visitor_Center` |
| 20 | 15 | SHO-VIC | 02 — Shobra Palace VC | `02_Shobra` |
| 30 | 16 | ALB-VC | 03 — Al Bay'ah Mosque VC | `03_Albiaa` |
| 40 | 17 | ALF-VC | 04 — Al Faw VC | `04_Al_Faw` |
| 50 | 18 | ARA-ARC | 05 — Al-Raka Archaeological Center | `05_Alrakaa_Center` |
| 60 | 19 | ANT-VC | 06 — Antara Rock VC | `06_Antara_Rock` |
| 70 | 20 | SAH-SQ | 07 — Said Alshohadaa Hoarding | `07_Said_Alshohadaa` |
| 80 | 21 | TAB-VC | 08 — Tabuk Castle VC | `08_Tabuk_Castle` |
| 90 | 13 | URP-VC | 09 — Urwa Palace VC | `09_Urwa_Palace_VC` |
| 43 | 22 | QAS-VC | 10 — Al Qassab Visitor Center | `10_Al_Qassab_Visitor_Center` |

## Reference Files
- `references/samaya-odoo-purchase-orders.md` — Samaya Odoo instance: PO creation, products, currencies, taxes, payment terms, vendors, pitfall fixes

## Pitfalls
- **XML-RPC can time out** on large batches (>50 task updates). Split into smaller groups or use shorter timeouts with retry.
- **Custom fields need model ID**, not model name, when creating via `ir.model.fields`. Always `search` for the model first.
- **Task `user_id` doesn't exist** — use `user_ids` (many2many) with `[(4, user_id)]` format.
- **Milestones are auto-created** by the template automation on project creation. Don't create them manually.
- **`sequence` field** on `project.milestone` does NOT exist — milestones have no built-in sequence field.
- **Folder rename** after creating Odoo Tasks MD — the MD file stays in the correct folder regardless of rename.
- **XML-RPC `search_read`** field validation is strict — only valid fields. Check with `fields_get()` first for unknown models.

## Mandatory Confirmation Step (User Preference)
Before ANY write operation (create/update/delete tasks or projects):
1. Always fetch and display the target project (by ID or name) with current stage and sequence.
2. Explicitly confirm the project name/code with the user if the action spans multiple records.
3. After updates, immediately re-query and show the affected task(s) for verification.
4. Provide a one-command revert pattern when possible (store original values before write).

This prevents cross-project mistakes (e.g., updating Al Bay'ah when intending another project).

## Ingesting Client Comments (Email / Image / PDF) → Odoo Tasks
Recurring workflow for visitor-center projects:
1. Extract bullet points from the client comment document.
2. Map each item to an existing parent package (Design Review, Tender Follow-up, Commercial, etc.) when possible.
3. Create new subtasks under the parent with:
   - Sequential numbering (next available seq under that parent)
   - Appropriate stage_id
   - x_planned_start / date_deadline aligned to the package timeline
   - Clear, plain-text names (no emoji)
4. If a comment cannot map cleanly, propose a new parent task only as last resort.
5. After creation, run a full project task list query and present the updated hierarchy.

Example XML-RPC pattern for subtask creation under parent:
```python
tid = models.execute_kw(db, uid, password, 'project.task', 'create', [{
    'name': 'X.Y New subtask description',
    'project_id': pid,
    'parent_id': parent_id,
    'stage_id': stage_id,
    'user_ids': [(4, 2)],
    'x_planned_start': '2026-06-14',
    'date_deadline': '2026-06-16',
    'sequence': next_seq
}])
```
