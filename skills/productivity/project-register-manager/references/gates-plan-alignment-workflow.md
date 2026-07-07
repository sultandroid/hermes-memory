# Gates Submission Plan → Register Alignment

## When to use

When a consultant provides a Stage 04 Submission Plan (Gates plan) and the existing register needs ref-numbering, item additions, or reorganization to match.

## Workflow

### 1. Parse both sources

Gates plan typically has two sheets (Arch + Mech) with columns:
- Gate / Stage (Detailed Design, Material Approval, Coordinated IFC)
- Drawing Package / Item (ref numbers for Mech, descriptive names for Arch)
- Submission Description
- Planned Submission Date

Register has per-stage sheets (50%, 90%, 100%, IFC/AFC) with columns:
- Ref #
- Submittal / Deliverable
- Discipline
- Stage dates (50%, 90%, 100%, IFC/AFC)
- Sub-Package

### 2. Extract all Gates refs (set A) and Register refs (set B)

```python
# Gates plan — refs in column 5 (Drawing Package / Item)
gates_refs = set()
for row in ws_gates.iter_rows(min_row=4, values_only=True):
    ref = row[4]
    if ref and str(ref).strip().startswith('MOC-ASE'):
        gates_refs.add(str(ref).strip())

# Register — refs in column A of every stage sheet
reg_refs = set()
for sname in ['50% Design', '90% Design', '100% Design', 'IFC  AFC  Construction']:
    ws = wb_register[sname]
    for r in range(3, ws.max_row + 1):
        ref = ws.cell(row=r, column=1).value
        if ref and str(ref).startswith('MOC-ASE'):
            reg_refs.add(str(ref).strip())
```

### 3. Identify gaps

- `gates_refs - reg_refs` = items missing from register
- `reg_refs - gates_refs` = register-only items (BIM, QA, register-internal)
- Type A: **Numbering mismatch** — same deliverable, different ref (e.g., per-floor items where Gates uses unique sequences -30001/-30002 and register uses same number for all floors)
- Type B: **Stage mismatch** — item exists but at wrong stage (e.g., in 100% only but Gates wants at 50%)
- Type C: **Genuinely missing** — item not in register at any stage

### 4. Numbering alignment patterns

**Pattern 1 — Unique per-floor sequences (Mech Gates):**
```
Gates: MOC-ASE-ME-MHV-AC-LGF-DDD-30002-00
Register had:   MOC-ASE-ME-MHV-AC-LGF-DDD-30001-00  (same -30001 for all floors)
Fix: rename per floor
```

Each discipline package uses a sequential range:
| Package | Range | Example |
|---------|-------|---------|
| AC (Air Conditioning) | 30001–30006 | BF=30001, LGF=30002, ..., RF=30006 |
| VE (Ventilation) | 30007–30012 | BF=30007, LGF=30008, ..., RF=30012 |
| CH (Chilled Water) | 30013–30018 | BF=30013, ..., RF=30018 |
| CD (Condensate Drain) | 30019–30024 | BF=30019, ..., RF=30024 |
| FF (Fire Fighting) | 30001–30006 | BF=30001, ..., RF=30006 |
| WS (Water Supply) | 30001–30006 | BF=30001, ..., RF=30006 |
| DRN (Drainage) | 30001–30006 | BF=30001, ..., RF=30006 |

**Pattern 2 — Single number all floors (simplified, what register had before):**
```
Register: MOC-ASE-ME-MHV-AC-LGF-DDD-30001-00  (all floors = 30001)
```
Fix: replace with Pattern 1 sequences.

### 5. Missing items common patterns

| Category | Items typically missing from 50% | Source |
|----------|--------------------------------|--------|
| Duct installation details | GEN 20002-20006 (1/3–3/3 Duct, Piping, Equipment Connection) | Only in 100% per original register |
| Fire Fighting details | GEN 20002-20006 (Typical install parts 1-2, Pumps Room, Pumps Schedule, Riser Diagram) | Only in 90%/100% |
| Water Supply details | GEN 20002 (Typical installation details) | Only in 100% |
| Drainage details | GEN 20002 (Typical installation details) | Only in 100% |
| Irrigation details | IRR-GEN-20001 (Typical installation details) | Completely missing |
| Missing floor | CD-RF-30024 (Condensate Drain, Upper-Roof Floor) | Completely missing |
| Material Submittals | QA-50000, QA-50001 | Only in IFC sheet |

### 6. Reorganization by floor zone (if needed)

When switching from discipline-based to floor-based grouping:

```
BEFORE (discipline):           AFTER (floor zone):
A - HVAC GENERAL               A — Basement Floor (BF)
B - HVAC PER-FLOOR LAYOUTS     B — Lower Ground Floor (LGF)
C - FIRE FIGHTING              C — Ground Floor (GF)
D - WATER SUPPLY               D — First Floor (1F)
E - DRAINAGE                   E — Second Floor (2F)
F - IRRIGATION                 F — Upper-Roof Floor (RF)
G - BIM                        G — General
H - MATERIAL SUBMITTALS
```

Each floor section groups ALL disciplines (HVAC, FF, WS, DRN) under that floor. General holds non-floor items (DBR, CALC, GEN, IRR, BIM, Materials).

### 7. Date corrections

- Always store as `datetime.date()` objects, not strings
- Apply `cell.number_format = 'DD/MM/YYYY'` 
- Avoid Excel serial number storage (46202 = 29/06/2026) — convert to date objects
- For bulk date shifts: use timedelta arithmetic, not string manipulation

### 8. Gate-specific items

Gate 2 (Material Approval) items typically go into the 50% sheet as one row per discipline.
Gate 3 (Coordinated IFC) items go into the IFC sheet (both the register's IFC/AFC sheet and the 100% sheet).

## Pitfalls

- **insert_rows + merged cells** — corrupts adjacent cell data. Unmerge first or rebuild in memory.
- **MergedCell write errors** — always unmerge before writing, re-merge after.
- **Stage column confusion** — 90% sheet dates go in column 5, 100% sheet dates in column 6. CD-RF added in wrong column is a common mistake.
- **Duplicate CD-RF** — if both the CD-section insertion AND the per-floor insertion trigger, you get two CD-RF rows. Deduplicate.
- **Count row** — after inserts, always recount and update the "N submittal(s)" row. Multiple stale count rows may accumulate.
