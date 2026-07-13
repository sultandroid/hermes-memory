---
name: submission-plan-validator
title: Submission Plan Validation System
description: Automated validation of submission plans against SOW/scope, programme schedule, submittal registers, and cross-discipline dependencies. Detects conflicts, missing items, schedule misalignment, and duplicate entries.
trigger: user asks to validate a submission plan, check for conflicts, or ensure completeness before submission
tags: [submission-plan, validation, sow, programme, schedule, cross-check, aseer]
---

# Submission Plan Validation System (SPVS)

## Overview

Validates any submission plan (Excel or markdown) against 10 checks:

| # | Check | What it catches |
|---|-------|-----------------|
| 1 | **SOW Coverage** | Deliverables in SOW missing from submission plan |
| 2 | **Scope Boundary** | Items in plan not traceable to any SOW/scope document |
| 3 | **Schedule Alignment** | Dates mismatch between plan and programme milestones |
| 4 | **Dependency Chain** | Predecessor items scheduled after their dependents |
| 5 | **Review Buffer** | Insufficient CG review time between submissions |
| 6 | **No Duplicates** | Same item appearing in multiple discipline plans |
| 7 | **Cross-Register Sync** | Plan items missing from submittal register or vice versa |
| 8 | **Gate Compliance** | Items for a gate (50%/90%/IFC) scheduled after gate deadline |
| 9 | **Responsibility** | Items with no assigned party |
| 10 | **Linked Activity ID** | Programme codes missing where they exist in the schedule |

## Input Sources

| Source | Format | Path Convention |
|--------|--------|-----------------|
| Submission Plan | Excel (.xlsx) or Markdown (.md) | `02_Schedule/{discipline}_submission_plan.md` or OneDrive `04_Registers/{discipline}_Submittal_Register/` |
| Master Programme | Markdown (.md) | `02_Schedule/master_programme.md` |
| Submittal Register | Markdown (.md) | `01_Registers/submittal_register.md` |
| Scope Summary | Markdown (.md) | `03_Scope/scope_summary.md` |
| SOW Documents | DOCX/PDF | OneDrive `01_Contracts/{specialist}/` |
| Master Submission Plan | Markdown (.md) | `02_Schedule/submission_plan_risk_assessment.md` |

## Validation Script

The script `scripts/validate_submission_plan.py` performs all 10 checks. Run:

```bash
python3 scripts/validate_submission_plan.py \
  --plan "02_Schedule/landscaping_submission_plan.md" \
  --programme "02_Schedule/master_programme.md" \
  --register "01_Registers/submittal_register.md" \
  --scope "03_Scope/scope_summary.md" \
  --master-plan "02_Schedule/submission_plan_risk_assessment.md" \
  --output "02_Schedule/validation_report.md"
```

### Output

A markdown validation report with:

1. **Summary** — PASS/FAIL per check, total issues count
2. **Issues Table** — each issue with severity (CRITICAL/HIGH/MEDIUM/LOW), description, and recommendation
3. **Schedule Timeline** — visual Gantt showing plan dates vs programme dates
4. **Dependency Graph** — ASCII dependency tree with conflicts highlighted
5. **Action Items** — prioritised fixes

## Validation Rules (Detailed)

### 1. SOW Coverage Check

For each deliverable in the specialist's SOW/scope document, verify it appears in the submission plan.

**Sources:**
- `scope_summary.md` — "In Scope" section lists all contractor obligations
- Specialist SOW documents in `01_Contracts/{specialist}/`
- `SCOPE_REQUEST.md` in `_MANAGER_DASHBOARD/` for internal scope definitions

**Logic:**
```python
scope_items = extract_scope_items(scope_file)
plan_items = extract_plan_items(plan_file)
missing = [s for s in scope_items if not any(matches(s, p) for p in plan_items)]
```

**Severity:** CRITICAL if a contractual deliverable is missing from the plan.

### 2. Scope Boundary Check

Every item in the submission plan must trace to a SOW clause, scope document, or CG-approved scope addition.

**Logic:**
```python
plan_items = extract_plan_items(plan_file)
scope_items = extract_all_scope_items(scope_file, sow_docs)
unscoped = [p for p in plan_items if not any(matches(p, s) for s in scope_items)]
```

**Severity:** MEDIUM — may indicate scope creep or undocumented additions.

### 3. Schedule Alignment Check

Compare planned submission dates against programme milestone dates.

**Sources:**
- `master_programme.md` — key milestones
- `submission_plan_risk_assessment.md` — master schedule with dates
- Activity ID mapping (if available)

**Logic:**
```python
plan_dates = extract_dates(plan_file)
programme_dates = extract_programme_dates(programme_file)
for item in plan_dates:
    prog_date = programme_dates.get(item.activity_id)
    if prog_date and abs(item.date - prog_date) > 5:  # 5-day tolerance
        flag_mismatch(item, prog_date)
```

**Severity:** HIGH if >5 days off programme; MEDIUM if 2-5 days off.

### 4. Dependency Chain Check

For each item with a dependency listed, verify the predecessor has an earlier or same planned date.

**Logic:**
```python
deps = extract_dependencies(plan_file)
for item, predecessor in deps:
    if item.date < predecessor.date:
        flag_inversion(item, predecessor)
```

**Severity:** CRITICAL if a dependent item is scheduled before its predecessor.

### 5. Review Buffer Check

Ensure adequate CG review time between submissions of the same discipline.

**Standards:**
| Complexity | Samaya Internal | CG Review | Total Buffer |
|-----------|----------------|-----------|-------------|
| Simple | 2 WD | 7 WD | 9 WD |
| Medium | 3 WD | 14 WD | 17 WD |
| Complex | 5 WD | 14-21 WD | 19-26 WD |

**Logic:**
```python
discipline_items = group_by_discipline(plan_items)
for discipline, items in discipline_items:
    for i in range(1, len(items)):
        gap = items[i].date - items[i-1].date
        if gap < min_buffer(discipline, items[i]):
            flag_insufficient_buffer(items[i-1], items[i], gap)
```

**Severity:** HIGH if buffer < 7 WD; MEDIUM if < 14 WD.

### 6. Duplicate Detection

Check if the same deliverable appears in multiple discipline plans with different dates or statuses.

**Logic:**
```python
all_plans = load_all_discipline_plans()
descriptions = [normalize(p.description) for p in all_plans]
duplicates = find_duplicates(descriptions)
```

**Severity:** HIGH — conflicting dates cause coordination issues.

### 7. Cross-Register Sync

Items in the submission plan should have corresponding entries in the submittal register, and vice versa.

**Logic:**
```python
plan_items = extract_plan_items(plan_file)
register_items = extract_register_items(register_file)
missing_from_register = [p for p in plan_items if not in_register(p, register_items)]
missing_from_plan = [r for r in register_items if not in_plan(r, plan_items)]
```

**Severity:** MEDIUM — register and plan should be in sync.

### 8. Gate Compliance

All items assigned to a gate (50%/90%/100%/IFC) must be scheduled before the gate deadline.

**Gate deadlines** (from DMP or master programme):
| Gate | Deadline |
|------|----------|
| G2 — 50% Design | D35 (~end Jul 2026) |
| G3 — 90% Design | D65 (~late Aug 2026) |
| G4 — IFC | D82 (~mid Sep 2026) |
| G5 — AFC | D88 (~late Sep 2026) |

**Logic:**
```python
for item in plan_items:
    gate_deadline = gate_deadlines.get(item.gate)
    if gate_deadline and item.date > gate_deadline:
        flag_gate_miss(item, gate_deadline)
```

**Severity:** CRITICAL if item misses its gate deadline.

### 9. Responsibility Check

Every item must have a named responsible party.

**Logic:**
```python
unassigned = [p for p in plan_items if not p.responsibility or p.responsibility in ['TBC', 'TBD', '']]
```

**Severity:** MEDIUM.

### 10. Linked Activity ID Check

If the programme schedule has activity IDs, verify they're referenced in the plan.

**Logic:**
```python
programme_activities = extract_activities(programme_file)
plan_activities = extract_activity_ids(plan_file)
missing_ids = [a for a in programme_activities if a.id not in plan_activities]
```

**Severity:** LOW — activity IDs are optional per the skill rules.

## Workflow

### Step 1: Load Sources
```bash
python3 scripts/validate_submission_plan.py --plan <plan> --all-sources
```

### Step 2: Review Validation Report
Open `02_Schedule/validation_report.md` — issues are sorted by severity.

### Step 3: Fix Issues
- **CRITICAL** — fix before submitting to CG
- **HIGH** — fix before next internal review
- **MEDIUM** — fix before next gate
- **LOW** — track for next revision

### Step 4: Re-validate
```bash
python3 scripts/validate_submission_plan.py --plan <plan> --recheck
```

### Step 5: Update AGENTS.md
After validation, update the project status with validation results.

## Integration with Existing Skills

| Skill | Integration Point |
|-------|------------------|
| `excel-submission-plan-routine` | Uses the same 15-column format; validator parses this format |
| `submittal-register-management` | Cross-references plan items against register |
| `submittal-register-gap-analysis` | Feeds gap analysis findings into validation |
| `project-deliverable-audit` | File-system audit feeds into SOW coverage check |

## Pitfalls

- **Activity IDs are optional.** The Linked Activity ID check (check 10) should warn, not fail, when IDs are missing. The skill `excel-submission-plan-routine` explicitly says "leave EMPTY until programme activity codes are confirmed."
- **Scope documents may be in OneDrive, not the repo.** The validator should accept a path to the SOW document or skip the SOW coverage check if not provided.
- **Dates in Excel are serial numbers.** The validator must convert serial dates (e.g. 46210) to readable dates before comparison.
- **Not all SOW items are submission plan items.** Some SOW items are services (meetings, reports, site visits) that don't appear in the submission plan. The validator should filter these out.
- **Cross-discipline plans may not all exist.** The validator should gracefully handle missing discipline plans.
- **The master programme may be out of date.** The validator should note the programme's last_updated date and warn if >14 days old.
- **CG review buffers are working days, not calendar days.** The validator should use a working-day calendar (Sun-Thu, KSA weekend Fri-Sat).

## Verification

After running validation:
1. Confirm the report file was created at the output path
2. Spot-check 2-3 issues from the report against the actual source documents
3. If the plan was modified, re-run validation to confirm fixes
4. Update the project status in `00_Status/project_status.md`
