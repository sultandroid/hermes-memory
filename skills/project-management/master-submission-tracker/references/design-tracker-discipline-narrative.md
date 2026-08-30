# Design Phase Deliverables Tracker — Per-Discipline Progress Narrative

When the user says "شوف التقديمات" / "what's the submission situation" / "work me up talking points" and hands the CG **`Design Phase Deliverables Tracker_<date>.xlsx`**, the fastest, most meeting-ready output is a **per-discipline progress narrative** extracted from the tracker itself — not a re-count of `submittal_register.md` rows. The tracker is the authoritative granular source (verified sheets, real `MOC-ASE-...-DDD-XXXX` drawing numbers).

## Two extraction targets

1. **Summary sheet** (`Design Deliverables Tracker`) — rows ~9–24 hold one row per discipline with an **`Overall % Complete`** column (col 37) and an `Overall Status` (col 38). Reading JUST this sheet gives the headline numbers in one shot:
   - Architecture 60%, Mechanical 51%, AV 35%, Showcase 49%, Electrical ~11.6%, ICT/Security ~2.5%, Exhibition Lighting ~3.5%, Structural ~9%, BIM ~7%, Clash 0%, Landscape 0%, FLS 0%, Scenography 100%.
   - Column layout note: col 5 = 50% planned date, col 6 = 50% actual, col 7 = planned qty, col 8 = actual qty, col 9 = 50% progress, col 11 = status. Forecast dates live at col 13/21/29 (90%/coord/IFC) — **all three are typically empty / "Not Started"**, which is itself the story: nothing has reached 90%/IFC yet.

2. **Per-discipline detail sheets** (`Electrical Deliverables`, `AV Deliverables`, `Low Current & ICT Deliverables `, `STR Deliverables `, `SHOWCASES Deliverables  `, etc.) — each has a **Status/Code** column (col 11/12). Extract the Code C / Code D / Not-started rows and the resubmitted/red-forecast dates (col 10–11). Note trailing-space + trailing-period variations in sheet names and status text.

## How to read the cells (openpyxl)

```python
import openpyxl
wb = openpyxl.load_workbook(path, data_only=True)
ws = wb['Design Deliverables Tracker']          # summary sheet
for r in range(9, ws.max_row+1):                # discipline rows
    qty_planned = ws.cell(r,7).value; qty_actual = ws.cell(r,8).value
    pct = ws.cell(r,9).value                    # 50% progress
    overall = ws.cell(r,37).value               # Overall % Complete (0-1 float)
    status = ws.cell(r,38).value
```

- Use `data_only=True` so formulas resolve to computed floats (progress % comes back as 0–1 float, e.g. `0.6` = 60%). Without it you get `None`.
- A discipline row with only `[37]` filled means it has NOT started (col 37 overall present, col 38 status absent) — read both.

## Narrative shape the user wants

The user (Aseer Tech Office Mgr) wants this synthesized by discipline, plain Egyptian Arabic ("بالبلدي"), terse, and **pre-split by root cause** (administrative blocker vs. genuine technical delay — see the ROOT-CAUSE TRIAGE pitfall in the umbrella SKILL.md). Structure:

- **Strong / OK** (high % + mostly Code B): e.g. Mechanical 51% (HVAC/Firefighting/Water all Code B approved), Architecture 60% (existing + demolition + GA all Code B), Scenography 100%.
- **Weak / stalled** (low % + Code C/D): Electrical (~12%, Earthing+LPS all Code C), ICT (~2.5%, BMS/ICT Base Report Code C, ELV still 80% prep), Exhibition Lighting (ZNA all 80% prep, not submitted), Structural (23 planned / 2 submitted = 9%), FLS 0%.
- **Never got to later gates**: every discipline shows 90%/coordination/IFC "Not Started".
- **Per-critical-item callouts** worth escalating at the meeting: FLS at 0% (life-safety), Electrical + ICT everything Code C ("the ones we DO submit get bounced — quality problem, not speed problem"), Showcases half Code C bouncing since June (delays the museum's own content).

## Pitfall

- Confirm with the user WHICH source they mean before answering: the **per-discipline plan sheets of this tracker** vs **`submission_tracker.md` section** vs **`submittal_register.md`**. They disagree on statuses and granularity (see Step 6 scoping correction). The tracker detail sheets carry real drawing numbers and per-deliverable codes; `submittal_register.md` is the Aconex/outlook-driven log. When the user supplies the tracker xlsx fresh, prefer IT for the progress/narrative answer.
