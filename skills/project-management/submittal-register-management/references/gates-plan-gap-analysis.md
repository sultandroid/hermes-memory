# Gates Plan Gap Analysis — Aseer Mech Register

Session 29 Jun 2026 — cross-referenced `Mechanical_Submittal_Register.xlsx` against `Aseer_Mech_Gates_Submission_Plan.xlsx`.

## Source Files

| File | Path |
|------|------|
| Gates Plan | WhatsApp download: `Aseer_Mech_Gates_Submission_Plan.xlsx` |
| Register | `OneDrive/.../04_Registers/Mechanical_Submittal_Register/Mechanical_Submittal_Register.xlsx` |

## Gates Plan Structure (Mech Stage 04 Submission Pl sheet)

- 71 items across 7 systems: HVAC General, AC Duct Layout, Ventilation Layout, AC Piping Layout, Condensate Drain, Smoke Management, Fire Fighting, Water Supply, Drainage, Irrigation
- Gates: Detailed Design (Gate 1), Material Approval (Gate 2), Coordinated IFC (Gate 3)
- Detailed Design items at 50% stage

## Numbering Convention

Gates plan uses **unique sequential numbers per floor** within each sub-system:

| Sub-System | Start | End | Floors |
|-----------|-------|-----|--------|
| AC (Air Conditioning) | 30001 | 30006 | BF, LGF, GF, 1F, 2F, RF |
| VE (Ventilation) | 30007 | 30012 | BF, LGF, GF, 1F, 2F, RF |
| CH (Chilled Water) | 30013 | 30018 | BF, LGF, GF, 1F, 2F, RF |
| CD (Condensate Drain) | 30019 | 30024 | BF, LGF, GF, 1F, 2F, RF |
| SM (Smoke Mgmt) | 30025 | — | 2F only |
| FF (Fire Fighting) | 30001 | 30006 | BF, LGF, GF, 1F, 2F, RF |
| WS (Water Supply) | 30001 | 30006 | BF, LGF, GF, 1F, 2F, RF |
| DRN (Drainage) | 30001 | 30006 | BF, LGF, GF, 1F, 2F, RF |

Register used single -30001-00 for all floors in each sub-system — common simplification that diverges from consultant's numbering.

## Items Missing from Register 50% Sheet (but present at later stages)

### HVAC — Duct/Piping/Equipment Details (in 100% sheet instead of 50%)
- MOC-ASE-ME-MHV-GEN-DDD-20002-00 Duct Installation Detail (1 of 3)
- MOC-ASE-ME-MHV-GEN-DDD-20003-00 Duct Installation Detail (2 of 3)
- MOC-ASE-ME-MHV-GEN-DDD-20004-00 Duct Installation Detail (3 of 3)
- MOC-ASE-ME-MHV-GEN-DDD-20005-00 Piping Installation Detail
- MOC-ASE-ME-MHV-GEN-DDD-20006-00 Equipment Connection Detail

### Fire Fighting — Schedule/Riser/Details (in 90%+100% instead of 50%)
- MOC-ASE-ME-MFF-GEN-DDD-20002-00 Typical installation details - part 1
- MOC-ASE-ME-MFF-GEN-DDD-20003-00 Typical installation details - part 2
- MOC-ASE-ME-MFF-GEN-DDD-20004-00 Pumps Room Details
- MOC-ASE-ME-MFF-GEN-DDD-20005-00 Fire Fighting Pumps Schedule
- MOC-ASE-ME-MFF-GEN-DDD-20006-00 Fire Fighting systems Riser Diagram

### Water Supply + Drainage — Details (in 100% instead of 50%)
- MOC-ASE-ME-MPL-WS-GEN-20002-00 Typical installation details - WS
- MOC-ASE-ME-MPL-DRN-GEN-20002-00 Typical installation details - Drainage

## Genuinely Missing Item
- MOC-ASE-ME-MPL-IRR-GEN-20001-00 Typical installation details - Irrigation System (not in any register sheet)

## Final Outcome (29 Jun 2026 session)

User chose to **align numbering with Gates plan** (unique per-floor sequences). Complete update applied:

### Changes Made

1. **Renumbered 34 per-floor items** across all 4 register sheets (50%/90%/100%/IFC):
   - AC: BF=30001, LGF=30002, GF=30003, 1F=30004, 2F=30005, RF=30006
   - VE: BF=30007, LGF=30008, GF=30009, 1F=30010, 2F=30011, RF=30012
   - CH: 30013→30018, CD: 30019→30024, FF/WS/DRN: 30001→30006 per floor

2. **Added 14 new items** to 50% Design sheet:
   - 5 HVAC Duct/Piping/Equipment Details (GEN 20002-20006) — were only in 100%
   - 5 Fire Fighting details (GEN 20002-20006) — were only in 90%/100%
   - 1 Water Supply detail (WS GEN 20002) — was only in 100%
   - 1 Drainage detail (DRN GEN 20002) — was only in 100%
   - 1 Irrigation detail (IRR GEN 20001) — was completely missing
   - 1 Condensate Drain RF (CD-RF 30024) — was completely missing

3. **Updated Legend** with numbering convention note.

3. **Kept 9 register-only items** (BIM 40001/40002, QA 50000-50006) — legitimate, not in Gates plan.

### Format Unification (post-alignment)

Applied Arch_Submittal_Register format template to all 4 sheets:
- **Row 1**: Dark blue (#1F4E79) header, Calibri 11 bold white, thin borders, center alignment
- **Row 2**: Medium blue (#2E75B6) title row, Calibri 12 bold white, left alignment
- **Section headers**: Light green (#E2EFDA) fill, Calibri 10 bold green (#375623), thin borders
- **Data rows**: Calibri 10 regular, top wrap alignment, thin borders all around
- **Column widths**: A=32, B=55, C=14, D–G=10, H=22, I=28
- **Date columns**: Converted all string dates to proper `datetime.date` objects with `DD/MM/YYYY` format

### Technical Approach

Used the in-memory rebuild pattern (see SKILL.md Critical Pitfall) to avoid `insert_rows` corruption from merged cells:
- Unmerged all cells in 50% Design sheet
- Read all rows into Python list
- Applied renumbering and insertions on the list
- Cleared sheet and rewrote from scratch
- Applied simple renames + single-row CD-RF insertion to 90%/100% sheets (these lacked merged cells)

## Script Used for Analysis

```python
# Load Gates plan
wb_gates = openpyxl.load_workbook(gates_path, data_only=True)
ws = wb_gates['Mech Stage 04 Submission Pl']
gates_items = []
for row in ws.iter_rows(min_row=4, values_only=True):
    if row[4] and str(row[4]).strip().startswith('MOC-ASE'):
        ref = str(row[4]).strip()
        desc = str(row[5]).strip() if row[5] else ''
        gates_items.append((ref, desc))

# Load register
wb_reg = openpyxl.load_workbook(reg_path, data_only=True)
register_items = set()
for sname in wb_reg.sheetnames:
    if sname == 'Legend': continue
    for row in wb_reg[sname].iter_rows(min_row=3, values_only=True):
        ref = row[0]
        if ref and str(ref).strip().startswith('MOC-ASE'):
            register_items.add(str(ref).strip())

gates_refs = set(item[0] for item in gates_items)
missing = gates_refs - register_items
extra = register_items - gates_refs
```
