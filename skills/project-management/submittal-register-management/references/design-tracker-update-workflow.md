# Design Tracker Update Workflow

## When to Use

After any submittal (CG review response received, drawing submitted, status change) or commit that affects design deliverable status.

## Tracker Files

| File | Location | Purpose |
|------|----------|---------|
| Excel (source of truth) | `01_Registers/Design_Phase_Deliverables_Tracker.xlsx` | Master tracker with formulas, 4 sheets |
| Excel (OneDrive copy) | `OneDrive - SAMAYA INVESTMENT/Documents/Aseer_Museum/Design_Phase_Deliverables_Tracker_23.07.2026.xlsx` | Synced copy for team access |
| MD version | `01_Registers/design_phase_deliverables_tracker.md` | Repo-readable version, updated on each submittal/commit |

## Steps

1. **Open Excel** — update the relevant discipline sheet (Arch/Mech/Str):
   - Add new drawing row if new submittal
   - Update `Date Submitted` (col H)
   - Update `Status` (col J) with CG code (A/B/C/D/DA)
   - Update `Preparation & Submitted` (col K) — 1 if submitted
   - Update `Approved %` (col L) — 1 if approved, 0.9 if Code C
   - Update `Date Approved` (col M) if approved
   - Update forecast date (col I) for pending items

2. **Update dashboard** (Sheet 1 "Design Deliverables Tracker"):
   - Verify discipline summary rows pull correct data from detail sheets
   - Update remarks (col AJ) with current status summary
   - Update `Last Updated` (col AK) to today

3. **Regenerate MD** — run extraction script:
   ```bash
   python3 /Users/mohamedessa/aseer-museum-pm/scripts/regenerate_design_tracker_md.py
   ```
   Or manually extract from Excel and write to `01_Registers/design_phase_deliverables_tracker.md`

4. **Copy Excel to OneDrive**:
   ```bash
   cp 01_Registers/Design_Phase_Deliverables_Tracker.xlsx \
      "/Users/mohamedessa/OneDrive - SAMAYA INVESTMENT/Documents/Aseer_Museum/Design_Phase_Deliverables_Tracker_23.07.2026.xlsx"
   ```

5. **Commit**:
   ```bash
   git add 01_Registers/Design_Phase_Deliverables_Tracker.xlsx \
           01_Registers/design_phase_deliverables_tracker.md
   git commit -m "tracker: update design deliverables [discipline] - [description]"
   ```

## CG Status Codes

| Code | Meaning | Action |
|------|---------|--------|
| A | Approved | Update col L = 1, col M = today |
| B | Approved with Comments | Update col L = 1, col M = today |
| C | Revise & Resubmit | Update col L = 0.9, add forecast resubmission date |
| D | Disapproved | Update col L = 0, flag for resubmission |
| DA | Deemed Approved (>14 days) | Update col L = 1, col M = submission + 14 days |
| U | Under Review | Keep col K = 1, col L empty |

## Drawing Number Convention

`MOC-ASE-{Discipline}-{Type}-{Phase}-{####}`

- Discipline: AR (Architectural), ST (Structural), ME (Mechanical), EL (Electrical)
- Type: ARC (Architecture), MHV (HVAC), MFF (Fire Fighting), MPL (Plumbing)
- Phase: DDD (DD Design), IFC (Issued for Construction)
- Example: `MOC-ASE-AR-ARC-BF-DDD-1200` = Architecture, Basement, Proposed GA Plan

## Pitfalls

- **OneDrive sync**: Write to `/tmp` first, then copy to OneDrive destination to avoid sync corruption
- **Formula cells**: The Excel has cross-sheet formulas (Arch!K305, Mech!K28). Do not overwrite formula cells with static values
- **Merged cells**: The dashboard sheet has merged header ranges. Use `safe_set_cell()` pattern when writing
- **Date format**: Convert all datetime objects to `DD/MM/YYYY` strings before writing to Excel
- **Structural sheet**: Currently has example/placeholder rows. Delete before entering real data
