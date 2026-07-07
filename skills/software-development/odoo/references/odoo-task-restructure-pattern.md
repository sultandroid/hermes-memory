# Odoo Task Restructuring Pattern

Applied to projects 219 (Aseer), 166 (Jalal & Jamal), and 176 (Maalem Al-Haramain).

## Pattern

1. Read all tasks in the project: `search_read` with `fields=['id', 'name', 'parent_id', 'stage_id', 'state']`
2. **Analyze and categorize**: Group tasks by type/function. Manufacturing projects → by product type (Furniture, Walls, Display Cases, etc.). Museum projects → by theme (Makkah models, Madinah models, Fit-out, etc.)
3. **Create MAIN package tasks** for each category with serial numbering: `01 — Category Name`, `02 — Category Name`
4. **Move existing tasks** under their corresponding MAIN package by setting `parent_id` to the package ID
5. **Check for orphans**: verify no tasks remain as main tasks that should be subtasks
6. **Flatten depth-3 nesting**: Move sub-sub-tasks directly under the package
7. **Re-sequence by state priority**: In-progress → waiting → done → cancelled, increments of 10
8. **Set Kanban order** for packages via `sequence` field
9. **Verify**: re-read the full tree to confirm all tasks are correctly nested

## Orphan Detection & Fix

Tasks with `parent_id` pointing to a package that was deleted or renamed:

```python
pkg_ids = {p['id'] for p in packages}
orphans = [t for t in all_tasks if t['parent_id'] and t['parent_id'][0] not in pkg_ids]

for o in orphans:
    models.execute_kw(db, uid, pw, 'project.task', 'write',
        [[o['id']], {'parent_id': target_package_id}])
```

Also check for **non-package main tasks** — `parent_id=False` but name doesn't match `NN — Package` pattern. These should either be renamed to packages or nested under one.

## Flatten Depth-3 Nesting

Tasks nested 3 levels deep (Package → Subtask → Deep-subtask):

```python
pkg_ids = {p['id'] for p in packages}
subtask_ids = {t['id'] for t in all_tasks if t['parent_id'] and t['parent_id'][0] in pkg_ids}
depth3 = [t for t in all_tasks if t['parent_id'] and t['parent_id'][0] in subtask_ids]

for d3 in depth3:
    parent = next(t for t in all_tasks if t['id'] == d3['parent_id'][0])
    pkg_id = parent['parent_id'][0] if parent['parent_id'] else None
    if pkg_id:
        models.execute_kw(db, uid, pw, 'project.task', 'write',
            [[d3['id']], {'parent_id': pkg_id}])
```

Exception: Sub-items under MEP Coordinations or Architectural Works that are legit sub-deliverables (specific drawings, reviews) can stay at depth 3.

## Re-sequence Subtasks by State Priority

Active items first, done items last:

```python
state_priority = {
    '01_in_progress': 0, '02_changes_requested': 0,
    '04_waiting_normal': 1,
    '1_done': 2, '03_approved': 2,
    '1_canceled': 3,
}
for pkg_id in package_ids:
    kids = models.execute_kw(db, uid, pw, 'project.task', 'search_read',
        [[['parent_id', '=', pkg_id]]],
        {'fields': ['id', 'state', 'sequence'], 'order': 'sequence ASC, id ASC'})
    kids.sort(key=lambda k: (state_priority.get(k['state'], 99), k['id']))
    for i, k in enumerate(kids):
        new_seq = (i + 1) * 10
        if k['sequence'] != new_seq:
            models.execute_kw(db, uid, pw, 'project.task', 'write',
                [[k['id']], {'sequence': new_seq}])
```

## Correcting Misplaced Tasks Between Packages

Common corrections noticed in audits:
- **"shop drawing"** → belongs in Engineering & Design (DD stage), not Procurement
- **"Follow up" tasks** → belong at the package level, not nested under individual items
- **Manufacturing orders (WH/MO/...)** → belong in Off-site Manufacturing stage, not Initiation

```python
models.execute_kw(db, uid, pw, 'project.task', 'write',
    [[task_id], {'parent_id': correct_package_id}])
```

## Verification

After restructuring, verify:
```python
orphans = models.execute_kw(db, uid, pw, 'project.task', 'search_count',
    [[['project_id', '=', PID], ['parent_id', '!=', False],
      ['parent_id', 'not in', list(package_ids.values())]]])

mains = models.execute_kw(db, uid, pw, 'project.task', 'search_count',
    [[['project_id', '=', PID], ['parent_id', '=', False]]])
subs = models.execute_kw(db, uid, pw, 'project.task', 'search_count',
    [[['project_id', '=', PID], ['parent_id', '!=', False]]])

print(f"{mains} packages, {subs} sub-tasks, orphans: {orphans}")
```

## ⚠️ CRITICAL: Stage IDs Vary Per Project

The stage IDs differ across projects. Always discover before writing:

```python
stage_ids = models.execute_kw(db, uid, pw, 'project.task', 'search_read',
    [[['project_id', '=', PID]]], {'fields': ['stage_id'], 'limit': 200})
used = set(t['stage_id'][0] for t in stage_ids if t['stage_id'])
```

| Project | Stages Used |
|---------|------------|
| Jalal & Jamal (166) | 35 (Init), 36 (DD), 39 (Proc), 479 (Handover), 480 (Cancelled), 659 (Off-site Mfg) |
| Maalem Al-Haramain (176) | 36 (DD), 479 (Handover), 610 (On-Site), 611 (Proc), 659 + 770 (Off-site Mfg) |

## Stage Assignment Rules (Samaya Odoo)

| Stage ID | Name | Use For |
|----------|------|---------|
| 36 | DD Stage | Design, engineering, coordination, plans |
| 39 / 611 | Procurement | BOQ, POs, shop drawings, material samples, mockups |
| 659 / 770 | Off-site Manufacturing | Production orders, fabrication, 3D printing |
| 610 | On-Site Work | Installation, fit-out, on-site activities |

## Jalal & Jamal — Jabal Omer (Project 166)

| # | Package | Stage | Items |
|---|---------|-------|-------|
| 01 | Engineering & Design | DD (36) | MEP, Architecture, Civil Defense, Graphics, Fabric panels |
| 02 | Procurement & Admin | Procurement (39) | PO civil, BOQ, PO requests |
| 03 | Materials & Mockup Approval | Procurement (39) | Materials submission, mockup reviews |
| 04 | Walls, Cladding & Ceiling | Off-site Mfg (659) | WF items, cladding, ceiling, MDF, BOQ items |
| 05 | Furniture | Off-site Mfg (659) | Benches, reception counter, sofa, shelving units |
| 06 | Display Cases & Acrylic | Off-site Mfg (659) | Acrylic boxes, showcases, display units, chandelier stands |
| 07 | Screens, Signage & LED | Off-site Mfg (659) | LED screens, signage, stands, backlights |
| 08 | Decorative & 3D Printed Models | Off-site Mfg (659) | Round frames, platforms, 3D printed models |
| 09 | Planters | Off-site Mfg (659) | Planter boxes type 01 & 02 |
| 10 | Fiberglass Works | Off-site Mfg (659) | Tree branches, fiberglass stone, eye, solar system |
| 11 | Doors & Glass | Off-site Mfg (659) | Sliding glass door, glass works, double leaf door |
| 12 | Hardware & Samples | Off-site Mfg (659) | Electrical cover, extinguisher stands, paint samples |
| 13 | Steel & Metal | Off-site Mfg (659) | Steel skirting, structural stiffeners |
| 14 | Flooring & Base Finishes | Off-site Mfg (659) | Microcement flooring |
| 15 | AV & Multimedia (Rawasen) | Procurement (39) | Films, projectors, projection, flying theater, lobby LED |

## Maalem Al-Haramain (Project 176) — Flat → Hierarchical

On 2026-06-21, all 90 tasks were flat. Restructured into 6 packages + 6 missing items added:

| # | Package | Stage | Items |
|---|---------|-------|-------|
| 01 | Makkah & Haram Sculptures | Off-site Mfg (659) | All Kaaba/Haram models, Makkah, Zamzam, Maqam (19 tasks) |
| 02 | Madinah & Prophet's Mosque Sculptures | Off-site Mfg (659) | Madinah models, Mihrab, Minaret, pulpit, Arches, Green Dome (18 tasks) |
| 03 | Fit-out, Furniture & Finishes | On-Site (610) | Counters, seating, display casework, doors, stairs (21 tasks) |
| 04 | Engineering & Design (Completed) | DD (36) | Workshop drawings, joinery, power/data, fire, HVAC, lighting (12 tasks) |
| 05 | 3D Printing & Manufacturing Orders | Off-site Mfg (659) | 3D prints, banners, small production items (23 tasks) |
| 06 | AV, Projection & Multimedia | Procurement (611) | Wall projection, 162" screen + missing items |

Missing items added: New Makkah, New Madinah, Current pulpit, Green Dome, Wall projection, 162" screen.
