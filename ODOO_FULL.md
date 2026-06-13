# Samaya Odoo — Hermes Agent Setup Guide

> لتعليم وكيل Hermes على جهاز آخر للتعامل مع أودو سمايا (مشروع متحف عسير)
> Version: 1.0 — Last updated: 2026-06-13

---

## 1. Overview: Two Odoo Instances

| | **Samaya** (الأساسي) | **Moqtana** (المصنع) |
|---|---|---|
| **URL** | `https://samayainv.odoo.com` | `http://167.99.224.43:8069` / `https://odoo.moqtana.sa` |
| **Database** | `peerless-tech-samaya-18-0-18447146` | `moqtana` |
| **User** | `sultan@samayainvest.com` (uid 151) | `mohamedsultanabbas@gmail.com` |
| **Version** | Odoo 18.0+e | Odoo 18.0+e |
| **Credentials file** | `~/.config/samaya/odoo.env` | User-supplied |
| **Use for** | POs, procurement, invoices, **Aseer Museum** (proj 219) | Manufacturing, HR, inventory, projects |
| **Alias** | "اودو سمايا" (DEFAULT) | "اودو المصنع" (only when user says so) |

**🔴 HARD RULE:** Aseer Museum (project 219) is on **Samaya** Odoo, NOT Moqtana. Default to Samaya for ALL task creation.

---

## 2. XML-RPC Connection Boilerplate

### Samaya (SSL cert bypass needed on macOS)

```python
import xmlrpc.client, ssl, os

# Option A: SSL bypass (if certifi not available)
ctx = ssl._create_unverified_context()
transport = xmlrpc.client.SafeTransport(context=ctx)

# Option B: SSL with certifi (preferred)
# import certifi
# ctx = ssl.create_default_context(cafile=certifi.where())
# transport = xmlrpc.client.SafeTransport(context=ctx)

URL = 'https://samayainv.odoo.com'
DB = 'peerless-tech-samaya-18-0-18447146'
LOGIN = 'sultan@samayainvest.com'

# Read password from env file
with open(os.path.expanduser('~/.config/samaya/odoo.env')) as f:
    for line in f:
        if 'ODOO_API_KEY' in line and '=' in line:
            PWD = line.split('=', 1)[1].strip()

common = xmlrpc.client.ServerProxy(URL + '/xmlrpc/2/common', transport=transport)
uid = common.authenticate(DB, LOGIN, PWD, {})

models = xmlrpc.client.ServerProxy(URL + '/xmlrpc/2/object', transport=transport)

# Helper
def exec_kw(method, args, kwargs=None):
    if kwargs:
        return models.execute_kw(DB, uid, PWD, 'project.task', method, args, kwargs)
    return models.execute_kw(DB, uid, PWD, 'project.task', method, args)
```

---

## 3. Project 219 — Aseer Museum Task Structure

### Stage IDs (Samaya-specific)

| ID | Name | Use For |
|----|------|---------|
| 35 | 01 Initiation | Prequal, studies, pricing, S00101 contract |
| 36 | 02 Design Development (DD) Stage | All design/technical work, plans, specialist pkgs |
| 39 | 03 Procurement | SC-01 Replica, procurement submittals, material approvals |
| 659 | 04 Off-site Manufacturing | Replica work packages, manufacturing orders |
| 40 | 05 On-site Work / Execution | Construction phases, site fabrication |
| 479 | 06 Handover (As-Built & Snagging) | Commissioning, handover, as-built |

### Key Package IDs (parent tasks)

| Package ID | Name | Stage |
|-----------|------|-------|
| 3011 | 00 — Pre-Qualification & Procurement | 35 |
| 3014 | 02 — Pricing & RFQs | 35 |
| 2945 | 00 General | 36 |
| 2938 | 01 Architecture | 36 |
| 2939 | 02 Structural Engineering | 36 |
| 2940 | 03 MEP & IT Engineering | 36 |
| 2941 | 04 Life Safety | 36 |
| 2946 | 05 Projects Plans | 36 |
| 1700 | 01.02 Architectural Package (NRS) | 36 |
| 1073 | 03.01 MEP & IT Detailed Design | 36 |
| 1072 | 02.01 Structural Scope - Stairs | 36 |
| 1308 | BEP | 35 |
| 3013 | S00101 Contract Scope | 39 |
| 3018 | 00 — Site Fabrication & Installation | 40 |

### Task Hierarchy Rules

| Level | `parent_id` | Appears In |
|-------|-------------|------------|
| **MAIN (Package)** | `False` | Kanban as card |
| **SUBTASK (Deliverable)** | Package ID | Package's Sub-tasks tab |
| **SUB-SUBTASK** | Stage-sub ID | Stage subtask's children |

### Tag IDs

| Tag | ID |
|-----|----|
| Prequalification | 140 |
| Plans & Procedures | 141 |
| A1-Architecture | 130 |
| S1-Structure | 132 |
| M1-MEP-Engineering | 133 |
| L1-LifeSafety-CivilDefense | 134 |

### Team Members (Samaya Odoo User IDs)

| Name | ID | Role |
|------|----|------|
| Sultan Issa | 151 | **Technical Office Manager** — DD stage technical packages ONLY |
| Mohamed Samir | 564 | Site execution + procurement — construction, site fabrication, manufacturing |
| Hani Alghamdi | 478 | Purchasing lead — pricing, RFQs, S00101 contract, PR material submittals |
| Hesham Abdelhameed | 163 | Document Control — submittals, daily reports, documentation flow |
| Ahmed Salah | 162 | Project Coordination — manufacturing orders |
| Ali Abdelrahman | 160 | Technical Office — DD stage technical work ONLY |
| Adel Darwish | 7 | Project Management |
| Mohammed Elshaikh | 157 | Project Planner — schedule review, planning |

### Task State Values

| State | Meaning | Progress |
|-------|---------|----------|
| `01_in_progress` | In Progress (default) | 0.25–0.75 |
| `02_changes_requested` | Changes Requested | 0.5 |
| `03_approved` | Approved | 1.0 |
| `1_done` | Done | 1.0 |
| `1_canceled` | Cancelled | 0.0 |
| `04_waiting_normal` | Waiting | 0.0 |

---

## 4. Task Creation — Verified Working Pattern

### Mandatory fields (ALL required)

```python
from datetime import date

task_id = models.execute_kw(DB, uid, PWD, 'project.task', 'create', [{
    'name': 'DOC-CODE — Standardized Title',
    'project_id': 219,
    'stage_id': 36,                    # Correct stage per task type
    'parent_id': PARENT_ID or False,   # MAIN=False, SUB=Package ID
    'user_ids': [(4, USER_ID)],        # Always assign to correct team member
    'tag_ids': [(4, TAG_ID)],          # Plans=141, Prequal=140, Architecture=130, etc.
    'date_assign': str(date.today()),
    'date_deadline': str(date.today()),
    'state': '01_in_progress',
    'progress': 0.5,                   # 0.0-1.0 scale (NOT 0-100!)
    'display_mark_as_done_primary': False,  # True for done/approved (shows checkmark)
    'description': (
        '<h3>Title</h3>'
        '<p><b>Context:</b> Why this task exists</p>'
        '<p><b>Status:</b> Current progress note</p>'
        '<p><b>Ref:</b> Related documents</p>'
    ),
}])
```

### ⚠ Critical field quirks

- **Assignee:** `user_ids` (many2many) with `[(4, id)]` syntax, NOT `user_id`
- **Tags:** `tag_ids` with `[(4, id)]` to append or `[(6, 0, [id1,id2])]` to replace
- **Progress:** 0.0–1.0 scale (0.5 = 50%), not 0–100
- **`read()` returns list:** `task[0]['name']` NOT `task['name']`
- **Always verify `date_assign <= date_deadline`** after date changes
- **Never leave dates empty —** "التخطيط بدون تواريخ ليس تخطيط"

---

## 5. PO Creation (Samaya)

### Key Reference IDs

| Item | ID | Notes |
|------|----|-------|
| Currency: SAR | 150 | Default is USD (1) — set explicitly |
| Currency: USD | 1 | Odoo default |
| 15% Purchase Tax | 5 | For PO lines (supplier VAT) |
| Subcontracts category | 640 | Service/consulting procurement |
| UOM: Units | 1 | Standard unit of measure |
| Vendor: نبيل قطب | 2640 | Nabil Qutb Engineering Consulting |
| Vendor: ARSSAD ALKHALIJ | 8193 | Faro 3D laser scanner |

### PO Creation Pattern

```python
# 1. Create service product
product_id = models.execute_kw(DB, uid, PWD, 'product.product', 'create', [{
    'name': 'أعمال الدراسات والتصميم الإنشائي لمتحف عسير الدولي',
    'type': 'service',
    'categ_id': 640,
    'lst_price': 15000.0,
    'standard_price': 15000.0,
    'uom_id': 1,
    'uom_po_id': 1,
}])

# 2. Create PO
po_id = models.execute_kw(DB, uid, PWD, 'purchase.order', 'create', [{
    'partner_id': 2640,
    'project_id': 219,
    'date_order': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
    'currency_id': 150,          # SAR
    'payment_term_id': 4,        # 30 Days
    'origin': 'عرض سعر رقم 26519',
    'order_line': [(0, 0, {
        'product_id': product_id,
        'name': 'وصف تفصيلي للخدمة',
        'product_qty': 1.0,
        'product_uom': 1,
        'price_unit': 15000.0,
        'taxes_id': [(6, 0, [5])],   # 15% Purchase Tax
    })]
}])

# 3. Verify currency (may default to USD — fix if needed)
models.execute_kw(DB, uid, PWD, 'purchase.order', 'write',
    [[po_id], {'currency_id': 150}])
```

### ⚠ PO Pitfalls
- **Currency may default to USD** even if `currency_id: 150` passed — verify after create
- **Notes are HTML:** Use `<div style="direction: rtl;">` for Arabic
- **Arabic-only text:** Pure Arabic in note fields (no mixing English with Arabic)
- **Write numbers as Arabic words** in formal document text

---

## 6. Procurement Workflow (Supplier → Product → RFQ → PO)

### Supplier Creation
```python
pid = models.execute_kw(DB, uid, PWD, 'res.partner', 'create', [{
    'name': 'اسم المورد',              # Arabic name
    'company_type': 'company',
    'country_id': 189,                  # Saudi Arabia
    'phone': '+966 XX XXX XXXX',
    'email': 'info@supplier.com',
    'vat': '3XXXXXXXXXXXXX',            # Required for KSA companies
}])
```

### RFQ = `purchase.order` in draft state
- USD (1) for international suppliers (no tax)
- SAR (150) for KSA suppliers (with 15% Purchase Tax ID 5)

---

## 7. Search Patterns

### Find existing tasks (prevent duplicates)
```python
# Case-insensitive substring match
tasks = models.execute_kw(DB, uid, PWD, 'project.task', 'search',
    [[['project_id', '=', 219], ['name', '=ilike', '%PL-0057%']]])

# All top-level packages in project 219
pkgs = models.execute_kw(DB, uid, PWD, 'project.task', 'search_read',
    [[['project_id', '=', 219], ['parent_id', '=', False]]],
    {'fields': ['id', 'name', 'stage_id', 'state', 'progress'],
     'order': 'id asc'})

# Subtasks under a package
subs = models.execute_kw(DB, uid, PWD, 'project.task', 'search_read',
    [[['parent_id', '=', package_id]]],
    {'fields': ['id', 'name', 'state', 'progress']})

# Find users
users = models.execute_kw(DB, uid, PWD, 'res.users', 'search_read',
    [[['login', '=ilike', '%hesham%']]],
    {'fields': ['id', 'name', 'login']})
```

### Update task state (without changing stage)
```python
models.execute_kw(DB, uid, PWD, 'project.task', 'write', [[task_id], {
    'state': '1_done',
    'progress': 1.0,
}])
```

---

## 8. Skills Required on the New Hermes Agent

Install these Hermes skills (from `.hermes/skills/` on the source machine):

### Core
1. **`odoo`** — Full Odoo skill: connection, query, create, update, PO creation, team info
2. **`odoo-task-injection`** — Compact task creation template for project 219

### Supporting (Samaya Technical Office)
3. **`samaya-technical-office`** — All BIM Unit workflows (sub creation, RFIs, doc control, submittal registers, daily task→Odoo mapping)
4. **`project-email-archive`** — Email archiving per project
5. **`bim-email-pipeline`** — Classify emails by project
6. **`bim-daily-todo`** — Daily task builder
7. **`bulk-file-organization`** — File organization across project folders
8. **`subcontractor-folder-setup`** — Subcontractor folder creation

### References to Copy (from the `odoo` skill's linked files)
| File | Purpose |
|------|---------|
| `references/samaya-odoo-reference.md` | Quick reference IDs |
| `references/samaya-odoo-procurement-workflow.md` | Full procurement pipeline |
| `references/samaya-odoo-users.md` | Known users + query patterns |
| `references/odoo-task-hierarchy.md` | Task hierarchy + Kanban config |
| `references/odoo-task-fields-discovered.md` | All task fields reference |
| `references/email-to-odoo-task-workflow.md` | Email → Odoo pipeline |
| `references/verbal-task-odoo-mapping.md` | Verbal task → Odoo mapping workflow |
| `references/odoo-connections.md` | Connection details for both instances |
| `scripts/odoo_connect.py` | Connection helper script |

### References from `samaya-technical-office`
| File | Purpose |
|------|---------|
| `references/sub-creation.md` | Subcontractor creation |
| `references/submittal-register-from-contracts.md` | Submittal registers from SOW/ER |
| `references/scope-analysis-rfi-workflow.md` | RFI register creation |
| `references/correspondence-processing.md` | Document control workflow |
| `references/style-guide.md` | Document style guide |
| `references/subcontractor-package-creation.md` | Subcon package workflow |
| `references/daily-todo-workflow.md` | Daily task workflow |
| `references/aseer-nrs-package-audit-*.md` | NRS package audit examples |

---

## 9. Key Workflows Summary

### A — Daily Verbal Task → Odoo Mapping
1. Query existing packages and subtasks in project 219
2. Check against verbal task list — categorize as: already exists in progress / already done (flag for Rev.02) / new task
3. Assign correct package + tag + user
4. Present mapping to user BEFORE executing
5. Create/update with all mandatory fields (dates, state, progress, assignee)
6. Log to `Email_Archive/_aseer_tasks_backlog.md`

### B — Post-Creation Enrichment from Outlook
1. Search Outlook SQLite for relevant emails
2. Extract attachments (AppleScript → /tmp)
3. Parse PDFs/XLSX with Python
4. **Copy file to project folder** (NEVER reference /tmp paths)
5. Update Odoo task `description` (HTML) with extracted context + project folder path

### C — Submittal Register Creation (from SOW/ER)
1. Read SOW and ER PDFs for the discipline
2. Extract exact SOW wording (no paraphrasing)
3. Organize by 50%/90%/100%/IFC design-stage packages
4. Generate Excel via openpyhl with proper formatting
5. Save to: `02_Submittals/`, `Docs/09_Registers/`, `Subcontractors/NN_/`
6. ALWAYS create SPEC.md first (source of truth), then generate Excel from it

### D — Subcontractor Scope Analysis & RFIs
1. Read sub's existing scope docs
2. Cross-reference against SOW, ER, Communication Plan, DMP
3. Identify gaps → categorize (MoC content / scope boundary / design / interface / material)
4. Create RFI register
5. Draft actual RFI documents (formal HTML for CG, markdown for internal)
6. Phase RFIs by project stage (don't raise design RFIs before DD submission)

---

## 10. Critical Pitfalls Summary

| # | Pitfall | Correct Approach |
|---|---------|-----------------|
| 1 | Confusing Samaya vs Moqtana | Aseer (219) is **Samaya**. Never fallback to Moqtana. |
| 2 | Leaving dates empty | `date_assign` + `date_deadline` REQUIRED on every task |
| 3 | Using `user_id` instead of `user_ids` | Task assignee is `user_ids` (many2many) with `[(4, uid)]` |
| 4 | Setting progress as 0-100 | Progress is 0.0-1.0 scale (0.5 = 50%) |
| 5 | Creating duplicates | Always `search` with `'=ilike'` first |
| 6 | Paraphrasing SOW in registers | Use **exact wording** from SOW document |
| 7 | Referencing /tmp paths in Odoo | Copy to project folder first, then reference project path |
| 8 | Assigning wrong person | Sultan=DD technical only. Samir=site/procurement. Hani=purchasing. |
| 9 | Incorrect PO currency | PO defaults to USD — always verify and set to SAR (150) |
| 10 | No SSL context | Samaya HTTPS needs `ssl._create_unverified_context()` on macOS |

---

## 11. Admin/Superuser Credentials

| Instance | Login | Credential Location |
|----------|-------|-------------------|
| **Samaya** | `sultan@samayainvest.com` | `~/.config/samaya/odoo.env` (ODOO_API_KEY) |
| **Moqtana** | `mohamedsultanabbas@gmail.com` | User supplies at runtime |

---

## 12. File System — Key Project Paths

### Samaya OneDrive (Primary)
```
~/Library/CloudStorage/OneDrive-SAMAYAINVESTMENT/Samaya/Technical Office/Bim Unit/
└── Aseer-Museum/
    ├── 01_Contracts_and_ER/
    ├── 02_Submittals/
    ├── 03_Design_Files/
    ├── 04_Invoices/
    ├── 05_Correspondence/
    ├── 06_Meetings/
    ├── 07_Reports/
    │   └── 07.5_Audit_Report/
    ├── 08_Schedules/
    ├── 09_Registers/
    │   ├── Subcontractor_RFI_Register/
    │   └── ...other registers
    ├── 10_Plans/
    ├── Subcontractors/
    │   └── NN_Discipline_Contractor/
    │       ├── _MANAGER_DASHBOARD/     # SPEC.md, SCOPE_REQUEST.md, SITUATION_REPORT.md
    │       ├── 01_Schedule_and_BOQ/
    │       ├── 02_Reference_Drawings/
    │       ├── 03_Specifications_and_Standards/
    │       ├── 04_Reference_Imagery/
    │       ├── 05_Returned_Submittals/
    │       ├── 06_RFIs/
    │       ├── 07_Approvals/
    │       ├── Email_Data_Extraction/
    │       └── SCOPE_REQUEST.docx
    └── Email_Archive/
        └── _aseer_tasks_backlog.md
```

---

## 13. Setup Steps for New Device

1. **Install Hermes Agent** on new device
2. **Copy skills** from source machine:
   ```bash
   # From source machine:
   cd ~/.hermes
   tar czf samaya-skills.tar.gz skills/software-development/odoo/ skills/productivity/odoo-task-injection/ skills/productivity/samaya-technical-office/
   # Transfer to new machine and extract
   ```
3. **Create credentials file** at `~/.config/samaya/odoo.env`:
   ```
   ODOO_API_KEY=<password>
   ```
4. **Install certifi** (recommended): `pip3 install certifi` — or use SSL bypass pattern
5. **Test connection**:
   ```bash
   python3 -c "
   import xmlrpc.client, ssl
   ctx = ssl._create_unverified_context()
   t = xmlrpc.client.SafeTransport(context=ctx)
   c = xmlrpc.client.ServerProxy('https://samayainv.odoo.com/xmlrpc/2/common', transport=t)
   print(c.version())
   "
   ```
6. **Set up OneDrive** sync for project folders (same path structure)
7. **Install Microsoft Outlook** for email enrichment workflow (macOS only)
8. **Copy key reference files** from the skills' `references/` directories
