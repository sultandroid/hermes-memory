# Design Document → Odoo Task Audit Workflow

Used on 2026-06-21 for Jalal & Jamal (ID 166) and Maalem Al-Haramain (ID 176).

## When to Use

User provides an exhibition/museum design PDF (hall layouts, sculpture lists, AV specs) and wants to check what's covered in Odoo vs missing.

## Workflow

### Phase 1 — Extract Items from PDF

```bash
pdftotext -layout "$pdf_path" /tmp/extracted.txt
# Read and organize items by hall/zone/type
```

Organize items as structured data — by hall, by zone, or by category depending on the document layout. Use the document's own structure (hall numbers, zones, item types) as the grouping principle.

### Phase 2 — Query Odoo Tasks

Get ALL tasks for the project(s):

```python
tasks = models.execute_kw(db, uid, pw, 'project.task', 'search_read',
    [[['project_id', '=', PID]]],
    {'fields': ['id', 'name', 'parent_id', 'stage_id', 'state'], 'limit': 500})
```

Also query stages used in that project — they vary per project:

```python
stage_ids = models.execute_kw(db, uid, pw, 'project.task', 'search_read',
    [[['project_id', '=', PID]]], {'fields': ['stage_id'], 'limit': 200})
used_stages = set(t['stage_id'][0] for t in stage_ids if t['stage_id'])
```

### Phase 3 — Manual Cross-Reference

Keyword-based matching is unreliable for Arabic/English mixed names. Instead:

1. **Read all Odoo task names** in full
2. **For each design item**, look for a matching Odoo task by scanning names manually
3. Mark as:
   - **✅ Covered** — exact match exists (sculpture model, specific item)
   - **⚠️ Partial** — generic package exists but no task for this specific item
   - **❌ Missing** — no matching Odoo task at all

Key matching signals: Arabic names (مجسم, شاشة), document codes (SLD-1-1, WH/MO/...), English keywords (screen, film, projection, fiberglass).

### Phase 4 — Classify Gaps

| Category | Action |
|----------|--------|
| Missing sculpture/model | Create under relevant package (Makkah/Madinah/Fit-out) |
| Missing AV item (projector, screen, film) | Likely contractor scope (Rawasen) — create under AV package |
| Missing graphic/fabric panel | Create under Engineering & Design or Graphics |
| Unstructured (all flat tasks) | Restructure first (see restructure workflow) |

### Phase 5 — Create & Reorganize Missing Items

```python
for name, desc in missing_items:
    tid = models.execute_kw(db, uid, pw, 'project.task', 'create', [{
        'name': name,
        'project_id': PID,
        'stage_id': STAGE,        # Must match the project's stage IDs
        'parent_id': PARENT_ID,   # Under the correct package
        'user_ids': [(4, uid)],
        'state': '01_in_progress',
        'progress': 0.0,
        'date_assign': today,
        'description': f'<p>{desc}</p><p><b>Source:</b> Design document dated ...</p>',
    }])
```

### Phase 6 — Re-sequence Subtasks by State

After creating/reassigning subtasks, order them so active items appear first:

```python
for pkg_id in package_ids:
    kids = models.execute_kw(db, uid, pw, 'project.task', 'search_read',
        [[['parent_id', '=', pkg_id]]],
        {'fields': ['id', 'state', 'sequence'], 'order': 'sequence ASC, id ASC'})
    
    # State priority: in_progress (0) → done (1) → cancelled/other (2)
    kids.sort(key=lambda k: (
        0 if k['state'] == '01_in_progress' else 1 if k['state'] == '1_done' else 2,
        k['id']))
    
    for i, k in enumerate(kids):
        new_seq = (i + 1) * 10
        if k['sequence'] != new_seq:
            models.execute_kw(db, uid, pw, 'project.task', 'write',
                [[k['id']], {'sequence': new_seq}])
```

## Pitfalls

- **Stage IDs are NOT the same across projects.** Project 166 uses stages 35/36/39/659/479/480. Project 176 uses stages 36/479/610/611/659/770. Always query the project's actual used stages first.
- **Hierarchy status differs.** Project 166 already had packages with subtasks. Project 176 had all 90 tasks flat (no parents). Check `parent_id` before assuming structure.
- **Arabic vs English names in Odoo.** Tasks may be in Arabic (مجسم), English (Model:), or mixed. Search both.
- **Manufacturing orders (WH/MO/...) are often separate tasks** from the design/sculpture they belong to. Cross-reference by content, not by name alone.
- **Orphan subtasks** exist when a subtask's parent was deleted or never created. Catch these via `parent_id not in {set of package IDs}`. Reassign to the correct existing package.
- **Non-package main tasks** are main tasks (`parent_id=False`) whose name doesn't match the `NN — Package` pattern. After restructuring, audit these and either rename them to packages or nest them under the appropriate package.
- **Follow-up tasks nested under individual items** (e.g., "Folow UP" under "Solar system sculpture") should be flattened to the package level. Rename for clarity while moving.
- **Document design vs Odoo project:** A single design PDF may map to multiple Odoo projects (e.g., Jalal & Jamal main project ID 166 + combined project ID 309). Check all relevant project IDs.

## Example: Maalem Al-Haramain Audit (2026-06-21)

Design PDF showed ~40 items (sculptures, models, AV). Odoo had 90 flat tasks.

| Outcome | Count |
|---------|-------|
| ✅ Covered (had matching Odoo task) | 34 |
| ❌ Missing (no Odoo task) | 6 |
| 🔧 Restructured (flat → 6 packages) | 90 tasks moved |

Missing items added: New Makkah model, New Madinah model, Current pulpit, Green Dome, Wall projection, 162" screen.

## Verification After Adding Missing Items

After creating missing items and restructuring, run a final check:

```python
# 1. Count packages vs standalone tasks
mains = models.execute_kw(db, uid, pw, 'project.task', 'search_count',
    [[['project_id', '=', PID], ['parent_id', '=', False]]])
subs = models.execute_kw(db, uid, pw, 'project.task', 'search_count',
    [[['project_id', '=', PID], ['parent_id', '!=', False]]])

# 2. Check for orphans
pkg_ids = set()
all_t = models.execute_kw(db, uid, pw, 'project.task', 'search_read',
    [[['project_id', '=', PID]]],
    {'fields': ['id', 'name', 'parent_id'], 'limit': 500})
for t in all_t:
    if not t['parent_id']:
        pkg_ids.add(t['id'])
orphans = [t for t in all_t if t['parent_id'] and t['parent_id'][0] not in pkg_ids]

# 3. Check for non-package main tasks
package_patterns = ['01 —', '02 —', '03 —', '04 —', '05 —', '06 —',
                    '07 —', '08 —', '09 —', '10 —', '11 —', '12 —',
                    '13 —', '14 —', '15 —', '16 —']
non_pkg_mains = [t for t in all_t if not t['parent_id']
                 and not any(t['name'].startswith(p) for p in package_patterns)]

print(f"Packages: {mains}, Subs: {subs}, Orphans: {len(orphans)}, Non-pkg mains: {len(non_pkg_mains)}")
```

## Example: Jalal & Jamal Audit (2026-06-21)

Design PDF showed ~50 items across 6 hall + lobby. Odoo had 14 packages.

| Category | Covered | Missing | Action |
|----------|---------|---------|--------|
| Sculptures (heart, solar system, eye) | ✅ | 0 | Already in Decorative & 3D Prints pkg |
| Screens & touch screens | ⚠️ | Stands, 23" screens, backlights | Added under existing packages |
| Fabric graphics (8 panels) | ❌ | 8 | Added under Engineering & Design |
| Films (4K, cinema, solar system) | ❌ | 5 | Added under new AV pkg |
| Projectors & projection | ❌ | 4 | Added under new AV pkg |
| Flying theater + eye projection | ❌ | 2 | Added under new AV pkg |
