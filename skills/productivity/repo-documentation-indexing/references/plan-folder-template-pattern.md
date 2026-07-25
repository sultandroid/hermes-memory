# Plan Folder Template Pattern

When populating project management plan subdirectories with standardized governance files, use this 4-file template pattern.

## When to Use

- User asks to "create/update template files in all plan subdirectories"
- User asks to "populate plan folders with README, summary, checklist, approval log"
- Setting up a new set of management plans (DMP, PEP, BEP, SMP, HSE, Risk, etc.)
- Standardizing existing plan folders to a common template format

## The 4-File Pattern

Every plan subdirectory gets these 4 files:

| File | Purpose | Key Sections |
|------|---------|-------------|
| `README.md` | Folder overview and metadata | YAML frontmatter, Metadata table, Purpose, Key Dates, Linked Documents, Contents Index |
| `plan_summary.md` | Executive overview | YAML frontmatter, Executive Overview (placeholder), RACI table, Critical Success Factors, Known Constraints, Approval Chain |
| `checklist.md` | Compliance checklist | YAML frontmatter, CONSTITUTION Compliance, PMBOK Alignment, Document Quality Standards, Approval Gates |
| `approval_log.md` | Approval history | YAML frontmatter, Approval History table, Decision Log, Change Requests |

## Template Structure Details

### README.md

```yaml
---
title: {folder_name} — {plan_title}
owner_agent: {owner_name}
last_updated: YYYY-MM-DD
status: draft
access: read-write
compliance_ref: CONSTITUTION.md §3
---
```

Sections: Metadata table (Plan Name, Owner Agent, Status, Last Updated, Approval Status, Contract Reference), Purpose paragraph, Key Dates table (TBD/⏳), Linked Documents (CONSTITUTION.md, plan tracker, operating model, contract summary), Contents Index table, footer status line.

### plan_summary.md

```yaml
---
title: {plan_title} — Plan Summary
owner_agent: {owner_name}
last_updated: YYYY-MM-DD
status: draft
---
```

Sections: Executive Overview (placeholder text), RACI table (5 rows: Plan Development, Review, Approval, Implementation, Updates × 5 columns: Owner, PMC, CG, MoC, NRS), Critical Success Factors (3 checkboxes), Known Constraints (placeholder), Approval Chain (3-step: PMC → CG → MoC).

### checklist.md

```yaml
---
title: {plan_title} — Compliance Checklist
owner_agent: {owner_name}
last_updated: YYYY-MM-DD
status: active
---
```

Sections: CONSTITUTION Compliance (7 checkboxes: frontmatter, source traceability, no AI cliches, British English, active voice, no emoji, cross-references), PMBOK Alignment (9 checkboxes: Integration through Procurement), Document Quality Standards (6 checkboxes: prefix convention, Calibri/A4/navy, table styling, readability, no binaries, OneDrive source of truth), Approval Gates (3 checkboxes: internal, PMC, CG+MoC).

### approval_log.md

```yaml
---
title: {plan_title} — Approval Log
owner_agent: {owner_name}
last_updated: YYYY-MM-DD
status: active
---
```

Sections: Approval History table (Rev, Date, Author, Status, Notes — 3 placeholder rows: A01 Draft, A02 Under Review, A03 Approved), Decision Log (2 placeholder entries), Change Requests (2 placeholder CRs), footer status line.

## Plan-Specific Data Per Folder

Each folder needs its own:
- **Plan name** (e.g. `01_DMP`, `12_SMP`)
- **Full title** (e.g. "Design Management Plan", "Sustainability Management Plan (SMP)")
- **Owner** (person or role, e.g. "NRS (Nissen Richards Studio)", "Muhammad Fida")
- **Contract references** (e.g. "SoW §6.22; ER §2.4; Contract §4 Art. 2")
- **Purpose** (1-2 sentence description of the plan's scope)
- **Owner short name** (for RACI column header, e.g. "NRS", "BIM Manager")

## Generation Strategy

### Option A: Python Script (preferred for 5+ folders)

Write a single Python script that:
1. Defines a list of plan tuples with all plan-specific data
2. Has 4 writer functions (one per template file)
3. Iterates over all plans, calling each writer
4. Uses string concatenation (not f-strings) to avoid `#` parsing issues in YAML frontmatter

**Pitfall:** Python f-strings with `#` inside the string body cause `SyntaxError: f-string expression part cannot include '#'`. Use string concatenation or `.format()` instead:

```python
# BAD — SyntaxError
content = f"""---
title: {p['title']} — Plan Summary
# {p['title']} — Plan Summary
"""

# GOOD — string concatenation
content = """---
title: """ + p['title'] + """ — Plan Summary
owner_agent: """ + p['owner'] + """
...
"""
```

### Option B: Manual per-folder (for 1-3 folders)

Copy an existing folder's 4 files and use `patch()` to replace plan-specific data.

## Verification

After generation, verify:
- [ ] All folders have exactly 4 files (README.md, plan_summary.md, checklist.md, approval_log.md)
- [ ] Each file has valid YAML frontmatter
- [ ] Plan-specific data (name, owner, contract refs, purpose) is correct per folder
- [ ] No Python generator script left behind in the repo
- [ ] Git commit with descriptive message

---

## Plan Reference Files (`ref_*.md`)

In addition to the 4-file template inside each plan subdirectory, maintain **reference sheets** in `04_Docs/02_Plans_and_Procedures/reference/` (or equivalent central reference directory). These are quick-lookup cards for each approved/submitted plan, storing document metadata, revision history, submittal status, and cross-references.

### File Naming

```
ref_{PlanShortName}.md
```

Examples: `ref_Procurement_Plan.md`, `ref_PQP_Project_Quality_Plan.md`, `ref_HSE_Plan.md`.

### YAML Frontmatter Fields

```yaml
---
last_updated: YYYY-MM-DD
owner_agent: <agent-name>
status: active | superseded
source: <OneDrive or CDE path to the PDF>
doc_code: <document-code>
revision: '<NN>'
date: 'YYYY-MM-DD'
title: <plan-title>
project: <project-name>
contract: <contract-number>
prepared_by: <person/role>
approved_by: <person/role or organization>
owner: <responsible person — plan owner>
cg_status: Code <A/B/C/D> — <Status description>
---
```

### Body Sections

| Section | Purpose | Key Content |
|---------|---------|-------------|
| **Document Identification** | Metadata table | Doc Code, Rev, Date, Title, Project, Contract, Prepared/Approved By, Format |
| **Document Location** | Source path | OneDrive directory path in code block |
| **Revision History** | Change log | Rev table: Rev, Date, Description, Author |
| **Submittal Status** | CG review status | Submittal Type, Date, CG Review Status, Next Action |
| **Description** | Plan summary | 2-3 sentence overview of what the plan covers |
| **Content Summary** | TOC outline | Bullet list of sections covered |
| **Cross-References** | Linked plans | Table: Ref, Plan, Note — bidirectional links to other plans |

### Guidelines

- Keep frontmatter and body in sync (revision, date, CG status must match)
- Update `last_updated` on every modification
- Source path should point to the actual PDF in OneDrive/CDE, not a local copy
- Cross-references should be bidirectional — if Plan A references Plan B, Plan B's ref file should also mention Plan A
- When a plan moves from draft → submitted → approved, update the submittal status and next action accordingly

---

## Obligation Matrix

An **obligation matrix** maps every project plan to its document code, plan owner, CG approval status, and next required action. It serves as a single-page accountability overview.

### Location

Place it in the document index directory (e.g., `08_Document_Index/obligation_matrix.md`).

### YAML Frontmatter

```yaml
---
last_updated: YYYY-MM-DD
owner_agent: <agent-name>
status: active
source: 08_Document_Index/00_plan_tracker.md, approved_plans.md, 03_Plans/*/plan_summary.md, AGENTS.md
---
```

### Structure

The matrix is organized by CG status category, each as a separate table section:

1. **Colour Key** — CG code definitions (Code B = Approved, Code C = Revise & Resubmit, etc.)
2. **Plans Submitted to CG — Approved (Code B)** — plans that have passed CG review
3. **Plans with CG Comments (Code C/D)** — plans needing revision or resubmission
4. **Draft / Submitted Plans (Awaiting CG Response)** — plans in progress
5. **Missing Plans (Not Yet Created)** — plans required but not yet drafted
6. **Quick Summary** — count per status category
7. **Key Contacts** — role-to-person mapping for plan owners

### Table Columns per Section

**Submitted / Approved / Needs Revision tables:**

| # | Plan | Doc Code | Rev | CG Status | Owner | Next Obligation |

**Draft / Submitted (Awaiting) tables:** (same columns)

**Missing Plans table:**

| # | Missing Plan | Why Needed | Referenced In | Owner | Priority |

### Guidelines

- **Cover all plans.** Every plan in the project should appear in exactly one section — don't leave gaps.
- **Keep statuses consistent** with the plan tracker (`00_plan_tracker.md`) and approved plans index (`approved_plans.md`).
- **Update when any plan's CG status changes.** A plan moving from Draft → Submitted, or Code C → Code B, should be moved to the correct section.
- **Include the Key Contacts table** at the bottom so the matrix doubles as an ownership directory.
- **No emoji or symbols in formal versions** (follow Samaya style guide). In internal registers, status indicators like ✅ 🔴 🟡 🟢 are acceptable.
- **Priority column** (for missing plans): 🟡 High / 🟢 Medium / 🔵 Low.

---

## Source

Worked example: Aseer Museum PM repo — 16 plan subdirectories, 64 files generated and committed in a single pass. Reference files updated and obligation matrix created at `08_Document_Index/obligation_matrix.md` (32 plans tracked, 25 existing + 7 missing, 15 Code B approved).
