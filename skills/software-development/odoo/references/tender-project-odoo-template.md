# Tender Project Odoo Task Template — 18 Tasks Across 9 Phases

> Pattern established on RCRC Exhibition Tender (Project 324), 25–26 June 2026.

## Project Creation

```python
# 1. Create project under Tendering stage (portfolio stage ID 12 for Samaya)
pid = models.execute_kw(db, uid, pw, 'project.project', 'create', [{
    'name': 'RCRC Exhibition — Tender Stage',
    'stage_id': 12,          # Tendering
    'user_id': assignee_uid, # Project lead
    'description': '<p>Tender project for ...</p>',
}])
```

## Task Stages for Tender Projects

| Phase | Stage | Stage ID | Reason |
|-------|-------|----------|--------|
| Mobilisation & Site Visit | Initiation | 35 | Pre-award startup |
| Scope Review & Design | DD Stage | 36 | Technical evaluation |
| Pricing & Estimation | Procurement | 39 | Costing/quotes |
| Proposal Writing | DD Stage | 36 | Document preparation |
| Review & Submission | Tender/DD Support | 37 | Final QC |
| Post-Submission | Tender/DD Support | 37 | Clarifications |

## 18-Task Template (9 Phases)

```python
TASKS = [
    # Phase 1: Tender Mobilisation (→ Initiation 35)
    (None, "01 — Tender Document Inventory & Register",
     "Inventory all tender docs, create register in OneDrive, index SOW/ER/BoQ."),
    (None, "02 — Tender Strategy Kick-Off",
     "Define bid strategy, team assignments, key dates, evaluation focus areas."),

    # Phase 2: Site Visit (→ Initiation 35)
    (None, "03 — Site Visit & Existing Conditions Survey",
     "Attend mandatory site visit, document with photos, prepare site report."),

    # Phase 3: Scope & Technical Review (→ DD Stage 36)
    (None, "04 — Scope Gap Analysis / RFI Log",
     "Review all docs against BoQ, identify discrepancies, submit RFIs."),
    (None, "05 — Method Statement — Preliminary Draft",
     "Draft preliminary method statements for key work packages."),

    # Phase 4: Pricing & Estimation (→ Procurement 39)
    (None, "06 — Material Take-Off & Verification",
     "Re-measure quantities from drawings, verify against BoQ."),
    (None, "07 — Subcontractor & Supplier Enquiries",
     "Issue RFQs to vendors, collect and analyze quotations."),
    (None, "08 — Pricing Model Compilation",
     "Build the consolidated pricing model from quotations and take-offs."),
    (None, "09 — Risk & Contingency Assessment",
     "Identify project risks, price contingencies, prepare risk register."),

    # Phase 5: Technical Proposal (→ DD Stage 36)
    (None, "10 — Technical Proposal Finalisation",
     "Write, format, and brand the technical proposal document."),

    # Phase 6: Commercial Proposal (→ Procurement 39)
    (None, "11 — Commercial Proposal Preparation",
     "Prepare sealed commercial offer, verify against pricing model."),

    # Phase 7: Programme & Methods (→ DD Stage 36)
    (None, "12 — Tender Programme Development",
     "Build 36-week programme with milestones, critical path, long-lead items."),
    (None, "13 — Method Statements — Full Draft",
     "Complete method statements for all work packages, QA/QC, HSE, logistics."),

    # Phase 8: Review & Submission (→ Tender/DD Support 37)
    (None, "14 — Internal Compliance & Quality Check",
     "Pre-submission compliance audit against tender requirements."),
    (None, "15 — Management Review & Sign-Off",
     "Director-level review, final approval, sign-off letter."),
    (None, "16 — Submission Preparation & Delivery",
     "Package, format, bind, and deliver submission."),

    # Phase 9: Post-Submission (→ Tender/DD Support 37)
    (None, "17 — Post-Submission Clarifications",
     "Respond to client clarifications, attend post-submission meetings."),
    (None, "18 — Lessons Learned & Archive",
     "Archive all work, document pricing decisions, lessons learned."),
]
```

## Bulk Task Creation Pattern

```python
from datetime import date, timedelta

base_date = date.today()
task_ids = []

for parent, name, desc in TASKS:
    tid = models.execute_kw(db, uid, pw, 'project.task', 'create', [{
        'name': name,
        'project_id': pid,
        'stage_id': get_stage_for_phase(parent),  # per table above
        'parent_id': parent or False,
        'user_ids': [(4, assignee_uid)],
        'state': '01_in_progress',
        'progress': 0.0,
        'date_assign': str(base_date),
        'date_deadline': str(base_date + timedelta(days=deadline_days)),
        'description': f'<p>{desc}</p>',
    }])
    task_ids.append(tid)
```

## Session Progress Update Pattern

After each work session on the tender, update the relevant Odoo tasks by APPENDING to description:

```python
# ALWAYS read existing description first
current = models.execute_kw(db,uid,pw,'project.task','read',[[task_id]],{'fields':['description']})
old = current[0].get('description','') or ''

new_block = f'''<hr><h4>Session: {today}</h4>
<ul><li>Work completed</li></ul>'''

models.execute_kw(db,uid,pw,'project.task','write',[[task_id],{
    'description': old + new_block,  # APPEND, never replace
    'progress': progress_float,       # 0.0-1.0
    'state': '01_in_progress' if not done else '1_done',
}])
```

## Lessons Learned

- **Deadlines compress hard**: 6 weeks → 6 days when tender submission is "before July 1"
- **Parallelize phases**: All labors (Fugu, Kimi, Codex) work simultaneously on different sections
- **Site visit is a milestone gate**: RFIs flow from site observations, not just document review
- **AV specs from cable schedule**: The XLSX cable schedule ("Rackroom" references) is often faster than DWG files for finding AV headend location