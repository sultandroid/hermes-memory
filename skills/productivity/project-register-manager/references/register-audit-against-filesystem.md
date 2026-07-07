# Register Audit: Cross-Reference Excel Register Against Live Filesystem

## When to use

A user asks why something is missing from a register, or asks you to verify a register's completeness. The register in question (e.g. Key Personnel Register, Subcontractor Register, Procurement Schedule) may be stale relative to the live project structure.

## The multi-source audit pattern

Cross-reference **at least three sources** to find gaps:

| Source | What it tells you | Example |
|--------|-------------------|---------|
| **Excel Register** (the file) | What's officially recorded | `Key_Personnel_Register.xlsx` lists 38 Tier 1-3 roles |
| **Live filesystem** (Subcontractors/, Specialist/, etc.) | What actually exists on disk | 21 subcontractor directories numbered 01-19 |
| **Contract documents** (SoW, ER, Prequalification Register) | What *should* exist per obligations | SoW Appendix B: 20 specialist categories; Subcontractor Prequalification Register: 47 subcontractor/specialist types |
| **Scope/request documents** | Recently identified gaps | `SCOPE_REQUEST.md`, RFI responses, NRS queries |

## Steps

### 1. Inventory the live filesystem

Scan the `Subcontractors/` directory (or equivalent) for all numbered subdirectories:

```python
import os
subs = sorted([d for d in os.listdir('Subcontractors/')
               if os.path.isdir(os.path.join('Subcontractors/', d))
               and not d.startswith('_')])
```

Output: `['01_Replica_Model_Contractor', '02_Showcases_Contractor', ...]`

### 2. Extract the Excel register's data

Read the Key Personnel Register/Subcontractor Register with `openpyxl`:

```python
wb = openpyxl.load_workbook('Key_Personnel_Register.xlsx', data_only=True)
ws = wb['Key Personnel']  # or whatever the data sheet is called
for r in range(2, ws.max_row+1):
    role = ws.cell(r, role_col).value
    assigned_to = ws.cell(r, assign_col).value
```

Extract: role name, assigned entity (company/person), tier/level, approval status.

### 3. Read contract obligation documents

Read the Subcontractor Prequalification Register markdown (or equivalent) for the master list of required specialists:

```python
# Categories from SoW Appendix B reproduced in the register markdown
# Category B — Exhibition Design Specialists:
#   B-01 AV Hardware Specialist → Rawasen
#   B-02 Mech/Electromech Interactives Specialist → Rawasen
#   B-07 Showcase / Conservation Showcase Specialist → Glasbau Hahn
```

### 4. Cross-reference and identify gaps

For each **physical subcontractor folder** on disk, check if the corresponding role exists in the Excel register:

| Subcontractor Folder | Expected Register Role | Found in Register? |
|---------------------|----------------------|--------------------|
| `03_AV_IT_Contractor` | AV Hardware Specialist | ✅ R11: Rawasen |
| `19_Interactive_Design_Contractor` | Interactive Design Specialist | ❌ MISSING |
| `16_Acoustic_Specialist` | Acoustic Specialist | ✅ R32: TBC |

### 5. Determine root cause

Gaps fall into three categories:

| Gap Type | Cause | Action |
|----------|-------|--------|
| **Newly identified** | Role was created *after* register was last revised (e.g., in response to an RFI) | Add new row to register, mark status as "Pending submission" |
| **Not in contract scope** | Role was never in SoW Appendix B (e.g., Interactive Design was scoped under B-02 Mech/Electromech, but a design/fabrication sub was needed separately) | Add new row, note source (RFI #, date), flag as new category beyond original SoW |
| **Overlaps with existing role** | Two subcontractors share the umbrella of one register role (e.g., Rawasin handles B-02 *and* a dedicated Interactive Designer handles design/UX) | Clarify in register: add note to the existing row, or split into two rows with distinct scopes |

### 6. Report findings

Structure the report as:
1. **All subcontractors listed** — from filesystem
2. **Gap found** — what's missing from register, why
3. **Recommended fix** — exact new row content (role, tier, assigned entity, status, source reference)

## Example output format

```
## Audit: Key Personnel Register vs Subcontractors/

### All Subcontractors (21 active)
01 Replica_Model_Contractor | 02 Showcases_Contractor | 03 AV_IT_Contractor ...

### Gaps Found
1. Interactive Design Specialist (Sub 19, 2026-06-07)
   - Exists on disk as 19_Interactive_Design_Contractor/
   - NOT listed in Key Personnel Register (Rev C02, 2026-05-06)
   - Root cause: Created post-register in response to NRS RFI A2742-6.04-018
   - SoW Appendix B has no dedicated "Interactive Design" category — was scoped under B-02
   - Recommended: Add new Tier 2 row with source reference to RFI

### Register Status
- Total roles in register: 38
- Subcontractor folders not in register: 1 (Interactive Design)
- Register is stale by 32 days (last rev: 2026-05-06)
```

## Pitfalls

- **Don't conflate scopes**: A "Mech/Electromech Interactives Specialist" (hardware build) and an "Interactive Design Specialist" (UX/design/programming) are different roles even though both relate to "interactives"
- **Check register revision date**: if the register is older than the subcontractor folder, the gap is likely a timing issue, not an omission
- **One subcontractor can serve multiple register roles**: Rawasin = AV Hardware (R11) + Mech Interactives (R15). Don't flag as "missing subcontractor" if they already appear under a different role
