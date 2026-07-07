# Odoo Task Hierarchy — Two-Level Pattern

**Updated 2026-06-15:** Restructured from 3-level (Package → Stage Package → Deliverable) to 2-level (MAIN → SUB). All intermediate "50% Design Package", "90% Design Package", "100% Design Package", "IFC/AFC Package" tasks were archived.

**Updated 2026-06-15 (session 2):** Added manufacturing-project pattern (product-type grouping), serial numbering, Kanban sequence ordering, and BOQ-to-Odoo mapping workflow.

## Two-Level Hierarchy

```
MAIN (parent_id=False, visible in Kanban)
  └── SUB (parent_id=Main ID, hidden inside Sub-tasks tab)
```

### Level 1 — MAIN (Package)
Shows in Kanban. Named with serial: `00 — General`, `01 — Architecture`, `07 — Lighting (SC-02)`.

Fields: `parent_id=False`

### Level 2 — SUB (Deliverable)
Hidden inside the parent's Sub-tasks tab. Contains the actual deliverable document code.

Fields: `parent_id=Main Package ID`

## Patterns (all packages must match)

**Pattern A — Specialist Package (06-17):**
```
MAIN: 07 — Lighting (SC-02)
  ├── LG-001 — Lighting design concept — ZD-0056 submitted Code B
  ├── LG-002 — Lighting plans and elevations
```

**Pattern B — Discipline Package (01-04, 00):**
```
MAIN: 01 — Architecture
  ├── 01.01 General arrangement drawing
  ├── 01.02 Architectural Package (NRS)
  ├── Arch Viz 3D Shots — ZD-0060
  └── (30+ subtasks)
```

**Pattern C — Plans Package (05):**
```
MAIN: 05 — Projects Plans
  ├── PL-0029 — Design Management Plan (DMP) Rev C04
  ├── PL-0018 — Project Communication Plan Rev.02
  ├── BEP — BIM Execution Plan / MIDP / TIDP
  └── (40+ subtasks)
```

## Manufacturing Project Pattern (Product-Type Grouping)

For manufacturing/fit-out projects (e.g., Project 166 — Jalal & Jamal - Jabal Omer), tasks are standalone production orders that need to be grouped by product type.

### Categorization by Product Type

When restructing a flat manufacturing project (70+ standalone tasks with no hierarchy):

1. **Read all tasks** and analyze them by product type based on names
2. **Create categories** matching the natural groupings:
   - Furniture (benches, reception counters, sofas)
   - Walls, Cladding & Ceiling (wall panels, fabric, mirror, cladding, ceiling elements)
   - Display Cases & Acrylic (acrylic boxes, cylindrical showcases, display units)
   - Screens, Signage & LED (LED screens, signage boards, screen stands)
   - Planters (artificial planter boxes, planting basins)
   - Fiber Glass & Decorative Stone (fiber glass panels, stone, tree branches)
   - Decorative & 3D Printed Models (round frames, platforms, 3D printed models)
   - Doors & Glass (sliding doors, glass work)
   - Hardware & Samples (electrical covers, fire extinguisher stands, paint samples)
   - Steel & Metal (steel skirting, structural steel stiffeners)
   - Flooring & Base Finishes (Topcrete flooring)

### Serial Numbering

All main packages get serial numbers:
```
01 — Engineering & Design
02 — Procurement & Admin
03 — Materials & Mockup Approval
04 — Walls, Cladding & Ceiling
...
14 — Flooring & Base Finishes
```

Order by stage first (Design → Procurement → Manufacturing), then alphabetically within stage.

### Kanban Sequence

Use the `sequence` field to control Kanban display order. Set values matching serial numbers:

```python
serial_seq = {
    3250: 1,   # 01 — Engineering & Design
    3249: 2,   # 02 — Procurement & Admin
    # ... up to 14
}
for tid, seq in serial_seq.items():
    models.execute_kw(db, uid, pw, 'project.task', 'write', [[tid], {'sequence': seq}])
```

### Stage Assignment for Manufacturing Items

- Manufacturing items (production orders, fabrication) → **Stage 659 (Off-site Manufacturing)**
- Procurement items (BOQ, PO, shop drawings, material samples) → **Stage 39 (Procurement)**
- Design/engineering items (architectural, MEP, graphics, civil defense) → **Stage 36 (DD)**

**⚠ Material samples go to Procurement (39), NOT DD (36).** A "submit material sample" task is a procurement/approval action, not a design deliverable.

## BOQ-to-Odoo Mapping Workflow

When asked to map a project's BOQ against Odoo tasks:

1. **Find the latest BOQ** — check `B.O.Q/` folder (Option-01, Option-02) and `As-Built Docs/` for dates. Use the most recent MasterFormat BOQ (Boq.xlsx type), NOT older detailed Arabic BOQs.

2. **Categorize BOQ items** by MasterFormat division:
   - DIV 5 (Steel) → Steel & Metal package (or create if missing)
   - DIV 6 (Wood) → Walls, Cladding & Ceiling (columns, stiffeners)
   - DIV 8 (Doors) → Doors & Glass package
   - DIV 9 (Finishes) → Walls, Cladding & Ceiling (ceilings, wall finishes) or Flooring package (flooring)
   - DIV 12 (Furnishings) → Furniture package (shelves, display units)

3. **Map each item** to existing Odoo packages. Create new packages for uncovered divisions.

4. **Check for gaps** — BOQ items with no corresponding Odoo task need new subtasks created.

5. **Present as a table:** BOQ Category → Odoo Package → Coverage (✅/⚠/❌)

## Creating the Two-Level Hierarchy

```python
# 1. Create Package (MAIN)
pkg_id = models.execute_kw(db, uid, pw, 'project.task', 'create', [{
    'name': '07 — Lighting (SC-02)',
    'project_id': 219,
    'stage_id': 36,
    'parent_id': False,
    'user_ids': [(4, 151)],
    'state': '01_in_progress',
    'date_assign': '2026-06-15',
    'date_deadline': '2026-06-18',
    'description': '<p>Lighting design specialist. Studio ZNA appointed.</p>',
}])

# 2. Create Deliverable (SUB) — directly under MAIN, no stage package
models.execute_kw(db, uid, pw, 'project.task', 'create', [{
    'name': 'LG-001 — Lighting design concept — ZD-0056 submitted Code B',
    'project_id': 219,
    'stage_id': 36,
    'parent_id': pkg_id,  # Directly under the package
    'user_ids': [(4, 151)],
    'state': '03_approved',
    'progress': 1.0,
    'date_assign': '2026-06-11',
    'date_deadline': '2026-06-17',
    'display_mark_as_done_primary': True,
}])
```

## Restructuring Existing 3-Level to 2-Level

When finding existing tasks with the old 3-level pattern (Package → Stage Package → Deliverable):

1. Move all Level-3 (deliverable) items up one level (set parent_id to the main package ID)
2. Verify each Level-2 (stage package) has no children left
3. Archive empty stage packages (set `state: '1_canceled'`)

```python
# Move deliverables up
for dlv_id in [3090, 3091]:  # deliverable IDs
    models.execute_kw(db, uid, pw, 'project.task', 'write', [[dlv_id], {
        'parent_id': 3089  # main package ID
    }])

# Archive empty stage packages
for sp_id in [3102, 3103, 3104, 3105]:  # stage package IDs
    children = models.execute_kw(db, uid, pw, 'project.task', 'search_count',
        [[['parent_id', '=', sp_id]]])
    if children == 0:
        models.execute_kw(db, uid, pw, 'project.task', 'write', [[sp_id], {
            'state': '1_canceled'
        }])
```
