---
name: odoo-task-restructure
description: Use when reorganizing flat Odoo task lists into hierarchical MAIN→SUB packages with standardized naming. Studies all tasks, classifies them, creates packages, assigns subtasks, and standardizes names per Odoo project conventions.
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [odoo, tasks, restructure, hierarchy, cleanup]
    related_skills: [odoo, writing-plans]
---

# Odoo Task Restructure — Reorganize & Standardize Tasks

## Overview

Reorganizes a project's flat Odoo task list into a proper two-level hierarchy (MAIN package → SUB deliverable) with standardized naming conventions. The workflow: audit all tasks → classify by type → create packages → nest subtasks → rename → verify.

Works on both Samaya Odoo and Moqtana Odoo via XML-RPC. Confirm the instance first (see `odoo` skill for instance distinction).

## When to Use

- Project has 20+ flat tasks with no `parent_id` (all main-level, no hierarchy)
- Tasks have inconsistent names (mix of Arabic/English, no doc codes, cryptic descriptions)
- User says "reorganize this project" or "arrange the tasks into packages"
- After a BOQ-to-Odoo mapping reveals missing packages

**Do NOT use for:**
- Creating a brand-new project with no existing tasks (use standard task creation patterns)
- Adding 1-2 tasks to an already-structured project
- Cross-project bulk operations without explicit scope

## Workflow

### Phase 0: Pre-Flight

```python
# 1. Confirm connection
from odoo_connect import connect
uid, models, cfg = connect("samaya")  # or "moqtana"

PROJECT_ID = 166  # ← SET THIS

# 2. Verify stage IDs first — query what the project actually uses
stage_ids = models.execute_kw(cfg['db'], uid, cfg['pw'], 'project.task', 'search_read',
    [[['project_id', '=', PROJECT_ID]]],
    {'fields': ['stage_id'], 'limit': 200})
used_stages = {}
for t in stage_ids:
    if t['stage_id']:
        used_stages[t['stage_id'][0]] = t['stage_id'][1]
print("Stages in use:", json.dumps(used_stages, indent=2))
# ⚠ Map your expected stages against this output. If stage 36/39/659 don't exist, update the IDs.

# 3. Count and read all non-cancelled tasks (with pagination for large projects)
import json

all_tasks = []
offset = 0
batch_size = 200
while True:
    batch = models.execute_kw(cfg['db'], uid, cfg['pw'], 'project.task', 'search_read',
        [[['project_id', '=', PROJECT_ID], ['state', '!=', '1_canceled']]],
        {'fields': ['id', 'name', 'stage_id', 'state', 'progress', 'parent_id', 'user_ids', 'date_deadline', 'date_assign', 'description'],
         'order': 'id ASC', 'limit': batch_size, 'offset': offset})
    if not batch:
        break
    all_tasks.extend(batch)
    offset += batch_size

print(f"Total active tasks: {len(all_tasks)}")
flat = [t for t in all_tasks if not t['parent_id']]
print(f"Main-level (parent_id=False): {len(flat)}")
print(f"Already sub-tasks: {len(all_tasks) - len(flat)}")
```

### Phase 1: Study & Classify

Read every task name, description, and current stage. Classify into logical groups:

| Group | Description | Stage | Examples |
|-------|-------------|-------|----------|
| Engineering & Design | Design/engineering deliverables | DD (36) | Architecture, MEP, structural drawings |
| Procurement & Admin | Purchasing, BOQ, PO, shop drawings | Procurement (39) | PO, material requests, shop drawings |
| Materials & Mockup | Material submissions, samples, mockups | Procurement (39) | Submit material, mockup review |
| Manufacturing — [Product] | Production orders by product type | Off-site Mfg (659) | Wooden items, signage, displays, furniture |
| On-site / Installation | Site work, installation, fit-out | On-site (40) | Install, site measurements |
| AV & Multimedia | Audio-visual, projection, interactives | Procurement (39) or DD (36) | Projectors, films, touch screens |

**Classification script pattern:**
```python
classification = {
    '01 — Engineering & Design': [],
    '02 — Procurement & Admin': [],
    '03 — Materials & Mockup Approval': [],
    '04 — Manufacturing: Wood & Furniture': [],
    '05 — Manufacturing: Signage & Displays': [],
    '06 — Manufacturing: Metal & Steel': [],
    '07 — Doors, Glass & Hardware': [],
    '08 — Flooring & Finishes': [],
    '09 — AV, Multimedia & Interactives': [],
    '10 — 3D Printing & Models': [],
    '11 — AV & Multimedia (Rawasen)': [],
}

def classify_task(task):
    """Return package name (key) based on task fields"""
    name_lower = (task['name'] or '').lower()
    desc_lower = (task.get('description') or '').lower()
    stage_id = task['stage_id'][0] if task['stage_id'] else 0

    # Manufacturing orders (WH/MO/FA/MO prefix)
    if any(p in name_lower for p in ['wh/mo/', 'fa/wh/mo/', 'manufacturing:']):
        if any(k in name_lower for k in ['signage', 'stand', 'logo', 'acrylic', 'display']):
            return '05 — Manufacturing: Signage & Displays'
        if any(k in name_lower for k in ['wood', 'veneer', 'arch', 'cladding', 'counter', 'shelf', 'furniture']):
            return '04 — Manufacturing: Wood & Furniture'
        if any(k in name_lower for k in ['steel', 'metal', 'stiffener', 'skirting']):
            return '06 — Manufacturing: Metal & Steel'
        if any(k in name_lower for k in ['door', 'glass']):
            return '07 — Doors, Glass & Hardware'
        if any(k in name_lower for k in ['floor', 'microcement', 'painting', 'paint']):
            return '08 — Flooring & Finishes'
        if any(k in name_lower for k in ['3d', 'print', 'model']):
            return '10 — 3D Printing & Models'
        return '04 — Manufacturing: Wood & Furniture'  # default mfg

    # Procurement items
    if stage_id == 39 or any(k in name_lower for k in ['po', 'purchase', 'procurement', 'boq', 'rfq']):
        if any(k in name_lower for k in ['material', 'sample', 'mockup', 'submittal', 'mock']):
            return '03 — Materials & Mockup Approval'
        return '02 — Procurement & Admin'

    # AV items
    if any(k in name_lower for k in ['av', 'projector', 'screen', 'multimedia', 'film', 'audio', 'rawasen', 'touch']):
        return '11 — AV & Multimedia (Rawasen)'

    # Design/engineering
    if stage_id == 36 or any(k in name_lower for k in ['design', 'engineering', 'mep', 'architect', 'coord']):
        return '01 — Engineering & Design'

    # On-site
    if stage_id == 40:
        return '08 — Flooring & Finishes'

    return '01 — Engineering & Design'  # fallback

# Apply classification
for t in all_tasks:
    if not t['parent_id']:  # only classify main-level tasks
        pkg = classify_task(t)
        classification[pkg].append(t['id'])

# Show results
for pkg_name, task_ids in sorted(classification.items()):
    if task_ids:
        print(f"{pkg_name}: {len(task_ids)} tasks")
    else:
        print(f"{pkg_name}: (empty — will skip)")

# ════════════════════════════════════════════════════════════════
# ⚠ STOP — REVIEW BEFORE PROCEEDING ⚠
# ════════════════════════════════════════════════════════════════
# Show the user the classification above and get explicit confirmation
# before Phase 2. The user should verify:
#   1. Every task is classified correctly
#   2. Empty packages that should be created anyway
#   3. Edge-case tasks that could fit multiple categories
#   4. The correct stage IDs for each package
#
# Run this check:
print(f"\n⚠ Phase 1 complete. {len([v for v in classification.values() if v])} non-empty groups.")
print("▶ Run Phase 2 only after user confirms the classification.")
# ════════════════════════════════════════════════════════════════
```

### Phase 2: Create Package Tasks

Create MAIN package tasks for each group that has items:

```python
import xmlrpc.client

package_ids = {}  # name → id

stages = {
    'dd': 36,
    'procurement': 39,
    'offsite_mfg': 659,
    'onsite': 40,
    'handover': 479,
}

# ⚠ REPLACE 151 with the actual user ID from your project
# Find users: models.execute_kw(db, uid, pw, 'res.users', 'search_read',
#     [[['login', '=ilike', '%sultan%']]], {'fields': ['id', 'name', 'login']})
# DO NOT hardcode user IDs across instances — they vary.
USER_ID = 151  # ← CONFIRM THIS IS YOU
TARGET_USERS = [USER_ID]

# Define packages — only create those with classified tasks
packages_template = [
    ('01 — Engineering & Design', stages['dd']),
    ('02 — Procurement & Admin', stages['procurement']),
    ('03 — Materials & Mockup Approval', stages['procurement']),
    ('04 — Manufacturing: Wood & Furniture', stages['offsite_mfg']),
    ('05 — Manufacturing: Signage & Displays', stages['offsite_mfg']),
    ('06 — Manufacturing: Metal & Steel', stages['offsite_mfg']),
    ('07 — Doors, Glass & Hardware', stages['offsite_mfg']),
    ('08 — Flooring & Finishes', stages['offsite_mfg']),
    ('09 — AV, Multimedia & Interactives', stages['procurement']),
    ('10 — 3D Printing & Models', stages['offsite_mfg']),
    ('11 — AV & Multimedia (Rawasen)', stages['procurement']),
]

# Filter to only packages with classified tasks (plus optionally user-requested empties)
packages_to_create = [(n, s) for n, s in packages_template if n in classification and classification[n]]

print(f"Creating {len(packages_to_create)} packages with tasks:")
for name, stage_id in packages_to_create:
    print(f"  • {name} (stage {stage_id}) — {len(classification.get(name, []))} tasks")

try:
    for name, stage_id in packages_to_create:
        pid = models.execute_kw(cfg['db'], uid, cfg['pw'], 'project.task', 'create', [{
            'name': name,
            'project_id': PROJECT_ID,
            'stage_id': stage_id,
            'parent_id': False,
            'user_ids': [(4, u) for u in TARGET_USERS],
            'state': '01_in_progress',
            'description': f'<p>Package: {name}</p>',
        }])
        package_ids[name] = pid
        print(f"  ✅ Created: {name} (ID {pid})")

except (xmlrpc.client.Fault, xmlrpc.client.ProtocolError, ConnectionError) as e:
    print(f"❌ ERROR during Phase 2: {e}")
    print("⚠ Packages may be partially created. Run Phase 6 to verify.")
    # Rollback hint: if you captured created IDs, delete them:
    # for n, pid in package_ids.items():
    #     models.execute_kw(cfg['db'], uid, cfg['pw'], 'project.task', 'unlink', [[pid]])
    raise  # Stop here — don't proceed to Phase 3 with partial data

# CRITICAL: Read back the package IDs to use in Phase 3
# Run this block after creation to capture the actual IDs
print(f"\n✅ Phase 2 complete. {len(package_ids)} packages created.")
print("Package IDs:", package_ids)
```

### Phase 3: Assign Subtasks to Packages

Set `parent_id` on each task to its classified package:

```python
# Map task_id → package_name from Phase 1 classification
task_pkg_map = {}  # task_id → package_name (e.g., '04 — Manufacturing: Wood & Furniture')
for pkg_name, task_ids in classification.items():
    for tid in task_ids:
        task_pkg_map[tid] = pkg_name

# Move tasks under their packages
for tid, pkg_name in task_pkg_map.items():
    if pkg_name in package_ids:
        models.execute_kw(cfg['db'], uid, cfg['pw'], 'project.task', 'write',
            [[tid], {'parent_id': package_ids[pkg_name]}])
        print(f"Moved task {tid} → {pkg_name}")
```

### Phase 4: Standardize Task Names

Apply naming convention to each subtask:

```python
# Pattern: [DOC-CODE] — Standardized Title (w/ context)
# Examples:
#   "WH/MO/00041 — Wooden Arch (w1.3 x d0.3 x h3.1)"
#   "PO-001 — VIP Furniture Purchase Order"
#   "PL-0057 — Time Schedule Cost Proposal"
#   "LG-001 — Lighting design concept — ZD-0056"

import re

def standardize_name(task):
    """Return standardized name for the task"""
    original = task['name'] or ''
    name_lower = original.lower().strip()

    # Already has prefix pattern like WH/MO/ or FA/WH/MO/
    mo_match = re.match(r'^(FA/WH/MO|WH/MO|FA/MO)/(\d+)\s*[-–—]\s*(.+)$', original)
    if mo_match:
        code = f"{mo_match.group(1)}/{mo_match.group(2)}"
        title = mo_match.group(3).strip()
        # Capitalize properly
        title = title[0].upper() + title[1:] if title else ''
        return f"{code} — {title}"

    # Has manufacturing order prefix
    if name_lower.startswith('manufacturing:'):
        parts = original.split('-', 1)
        if len(parts) > 1:
            code = parts[0].strip()
            title = parts[1].strip()
            return f"{code} — {title[0].upper() + title[1:] if title else ''}"
        return original

    # Generic: capitalize first letter, remove extra spaces
    title = original.strip()
    title = re.sub(r'\s+', ' ', title)
    if title and title[0].islower():
        title = title[0].upper() + title[1:]
    return title

# ⚠ Read the existing name first, ask user for confirmation on major changes
for t in all_tasks:
    new_name = standardize_name(t)
    if new_name != t['name']:
        print(f"  TASK {t['id']}: \n    Old: {t['name']}\n    New: {new_name}\n")
        # Uncomment to apply:
        # models.execute_kw(cfg['db'], uid, cfg['pw'], 'project.task', 'write',
        #     [[t['id']], {'name': new_name}])
```

### Phase 5: Kanban Sequence

Set `sequence` field so packages appear in correct order:

```python
seq = [('01 — Engineering & Design',           1),
       ('02 — Procurement & Admin',             2),
       ('03 — Materials & Mockup Approval',     3),
       ('04 — Manufacturing: Wood & Furniture', 4),
       ('05 — Manufacturing: Signage & Displays', 5),
       ('06 — Manufacturing: Metal & Steel',    6),
       ('07 — Doors, Glass & Hardware',         7),
       ('08 — Flooring & Finishes',             8),
       ('09 — AV, Multimedia & Interactives',   9),
       ('10 — 3D Printing & Models',           10),
       ('11 — AV & Multimedia (Rawasen)',      11)]

for name, seq_no in seq:
    if name in package_ids:
        models.execute_kw(cfg['db'], uid, cfg['pw'], 'project.task', 'write',
            [[package_ids[name]], {'sequence': seq_no}])
```

### Phase 6: Verify

```python
# 1. Count main tasks vs subtasks
active = models.execute_kw(cfg['db'], uid, cfg['pw'], 'project.task', 'search',
    [[['project_id', '=', PROJECT_ID], ['state', '!=', '1_canceled']]])

mains = models.execute_kw(cfg['db'], uid, cfg['pw'], 'project.task', 'search_count',
    [[['project_id', '=', PROJECT_ID], ['parent_id', '=', False], ['state', '!=', '1_canceled']]])

subs = models.execute_kw(cfg['db'], uid, cfg['pw'], 'project.task', 'search_count',
    [[['project_id', '=', PROJECT_ID], ['parent_id', '!=', False], ['state', '!=', '1_canceled']]])

print(f"Total: {len(active)}, Main: {mains}, Sub: {subs}")

# 2. Check for orphans (subtask with parent not in any package)
parent_ids = list(package_ids.values())
orphans = models.execute_kw(cfg['db'], uid, cfg['pw'], 'project.task', 'search',
    [[['project_id', '=', PROJECT_ID], ['parent_id', '!=', False],
      ['parent_id', 'not in', parent_ids], ['state', '!=', '1_canceled']]])
if orphans:
    print(f"⚠ {len(orphans)} orphan tasks (parent not in packages): {orphans}")
else:
    print("✅ No orphans")

# 3. Verify all packages have subtasks
for name, pid in package_ids.items():
    kids = models.execute_kw(cfg['db'], uid, cfg['pw'], 'project.task', 'search_count',
        [[['parent_id', '=', pid]]])
    status = "✅" if kids > 0 else "⚠ EMPTY"
    print(f"  {status} {name}: {kids} subtasks")
```

## Stage ID Reference (Samaya Odoo — Project 166/176)

| Stage ID | Name | Use |
|----------|------|-----|
| 35 | Initiation | New tasks, not yet started |
| 36 | DD Stage | Design & engineering |
| 39 | Procurement | PO, RFQ, shop drawings, materials |
| 40 | On-site Work / Execution | Site installation, fit-out |
| 479 | Handover | Completion & handover |
| 480 | Cancelled | Dead/archived tasks |
| 659 | Off-site Manufacturing | Production orders (fabrication) |

⚠ **Stage IDs vary per project.** Always query the actual stages in use:

```python
used_stages = {}
for t in all_tasks:
    if t['stage_id']:
        used_stages[t['stage_id'][0]] = t['stage_id'][1]
for sid, sname in sorted(used_stages.items()):
    print(f"  Stage {sid}: {sname}")
```

## Task Naming Convention

```
[MAIN]       NN — Package Title                     e.g. "04 — Manufacturing: Wood & Furniture"
[SUB]        [DOC-CODE] — Standardized Title         e.g. "WH/MO/00041 — Wooden Arch (w1.3 x d0.3 x h3.1)"
```

**Rules:**
- Main tasks: `NN — Title` (serial number + em-dash)
- Subtasks: Preserve doc codes (MO orders, PO numbers); capitalize first letter
- No Arabic/English mixing in single name if avoidable
- No trailing spaces, no double spaces
- No ALLCAPS titles (use Title Case or Sentence case)
- Avoid generic names like "Wood Works" → "WH/MO/00467 — فريمات خشب ذهبي Golden Wooden Frame"

## Rollback (Undo)

If the restructure goes wrong, reset all modified `parent_id` values back to `False`:

```python
# Rollback script — run if you need to undo Phase 3
affected_ids = list(task_pkg_map.keys())  # from Phase 3
for tid in affected_ids:
    models.execute_kw(cfg['db'], uid, cfg['pw'], 'project.task', 'write',
        [[tid], {'parent_id': False}])
print(f"Reset {len(affected_ids)} tasks back to main level.")

# Delete packages created in Phase 2 (optional)
for name, pid in package_ids.items():
    models.execute_kw(cfg['db'], uid, cfg['pw'], 'project.task', 'unlink', [[pid]])
    print(f"Deleted package: {name} (ID {pid})")
```

## Common Pitfalls

1. **Stage IDs vary per project instance.** Never hardcode stage IDs across projects. Always query stages from existing tasks first.

2. **Orphan tasks after restructuring.** If a package is deleted or renamed without reassigning its children, subtasks become orphaned (their `parent_id` points to a non-existent task). Verify with the orphan check in Phase 6.

3. **Depth-3 nesting.** Odoo allows unlimited task nesting, but projects follow a strict 2-level convention. If a subtask already has subtasks (depth 3), flatten by setting the child's `parent_id` directly to the package.

4. **Sequence field for Kanban order.** The `sequence` field controls Kanban card order (lower = first). After creating packages, assign sequence values matching the serial numbers.

5. **Always APPEND to task descriptions — never replace.** When updating a task's description, read the existing value first and prepend/append new content.

6. **User assignment via `user_ids` (many2many), NOT `user_id`.** Use `[(4, user_id)]` syntax.

7. **Progress is 0.0-1.0 scale, NOT 0-100.** Setting `progress: 50` will fail silently.

8. **`display_mark_as_done_primary` is UI-only — cannot be set via API.** The real done indicator is `state='1_done'`.

9. **Backup package IDs after creation.** The XML-RPC create returns the new ID — store it in a dict immediately. If you lose the IDs, search by name pattern to recover.

10. **Classification is imperfect.** Always show the user the proposed classification before executing writes. Some tasks may fit multiple categories — defer to user judgment on edge cases.

11. **Shared tasks spanning multiple zones.** A single task like "VIP & Cafeteria Doors" belongs to two packages. The classification algorithm can only assign one parent_id. Flag these for the user to decide which package gets it, or create a shared/general package for cross-zone items.

## Verification Checklist

- [ ] All tasks have `parent_id` set correctly (either False for main, or a valid package ID for sub)
- [ ] No tasks left at the main level that should be subtasks (except package tasks)
- [ ] No orphan subtasks (parent doesn't exist)
- [ ] All package names follow `NN — Package Title` format
- [ ] All subtask names follow the naming convention (doc codes preserved, no ALLCAPS, no double spaces)
- [ ] Kanban sequence values assigned (1, 2, 3...) matching serial numbers
- [ ] Stage IDs correct per package type (design → DD, procurement → Procurement, manufacturing → Off-site Mfg)
- [ ] User notified of classification for approval before any write operations
- [ ] Summary reported: total tasks → main packages → subtasks
