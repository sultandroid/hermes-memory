# Architecture Register Creation (June 2026)

## Source Data
- **Gates Submission Plan**: `04_Docs/02_Plans_and_Procedures/02.2_BEP_MIDP_TIDP/04_Registers/Aseer_Arch_Gates_Submission_Plan.xlsx`
- **BOQ sheets**: 001-003 (Design, Enabling, Finishes)
- **Designer**: NRS (Nissen Richards Studio)

## Structure
- 4 levels × 16 drawing packages = 64 items for DD stages (50/90/100%)
- Plus BIM, Material Approval, Coordinated IFC
- Organization: by LEVEL (A=Basement, B=Lower Ground, C=Ground, D=First Floor) — matching the Gates Submission Plan structure, NOT by drawing type

## Category Boundaries with `next_cat`

When categories have non-uniform sizes (16, 16, 16, 16, 1, 2, 1, 19), use the `next_cat` dict pattern instead of hardcoded range arithmetic:

```python
cn = {0:'PRELIMINARY — DIGITAL MATERIAL BOARD', 1:'A — BASEMENT FLOOR', 
      17:'B — LOWER GROUND FLOOR', 33:'C — GROUND FLOOR',
      49:'D — FIRST FLOOR (STRUCTURE)', 65:'E — BIM & STANDALONE',
      67:'F — MATERIAL APPROVAL', 68:'G — COORDINATED IFC'}
cn_keys = sorted(cn.keys())
next_cat = {k: cn_keys[i+1] if i+1 < len(cn_keys) else 999 
            for i, k in enumerate(cn_keys)}
```

## Digital Material Board as Separate Row

When the user asks for a cross-platform deliverable (digital material board, VR tour, etc.), add it as a separate row with its own category at the top, NOT appended to an existing description:

```python
# At top, before any floor items
its.append((f'AR-{ref:03d}', 'Digital Material Board — Basement Floor',
            'Architectural', ['29/06/2026', '—', '—', '—'], '3D Viz', ''))
ref += 1

# Category header
cn = {0:'PRELIMINARY — DIGITAL MATERIAL BOARD', ...}
```

Rules:
- 50% only unless user specifies otherwise
- Same date as the floor it belongs to
- Sub-Package matches related discipline
- Its own category header before category A

## Staggered Floor Dates (7-day review buffer)

| Floor | 50% | 90% (+30d) | 100% (+30d) |
|-------|-----|------------|-------------|
| Basement | 29/06 | 29/07 | 28/08 |
| Lower Ground | 06/07 | 05/08 | 04/09 |
| Ground | 13/07 | 12/08 | 11/09 |
| First Floor | 20/07 | 19/08 | 18/09 |
