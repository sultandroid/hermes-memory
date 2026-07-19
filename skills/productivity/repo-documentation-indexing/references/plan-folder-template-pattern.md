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

## Source

Worked example: Aseer Museum PM repo — 16 plan subdirectories, 64 files generated and committed in a single pass.
