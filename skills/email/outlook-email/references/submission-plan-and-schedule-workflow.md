# Submission Plan & Schedule Workflow (from Email to CG)

## When to Use

CG/PMC asks for a deliverables schedule, or you need to: update a submission plan with actual receipts, build a design phase timeline with review buffers, cross-reference a register log against the plan, or clean up discipline overlaps in a project plan.

## Workflow

### Phase 1: Gather Sources

Collect ALL relevant data before making any changes:
1. **Existing submission plan** — find the canonical plan (usually `04_Docs/02_Plans_and_Procedures/02.2_BEP_MIDP_TIDP/04_Registers/Aseer_Submission_Plan.xlsx`)
2. **Emails from CG/PMC** — search Outlook for the CG's deadline email (e.g., Mohammad Elbaz's 3-month mandate)
3. **Register logs** — the project's CG response tracking log (e.g., `Register Log.xlsx` with Material Submittal, SNA, IR, etc. sheets)
4. **Project memory** — `PROJECT_MEMORY.md` for approved items, appointment statuses, known blockages
5. **Deliverables schedule** — the detailed v3+ schedule from desktop (e.g., `Aseer_Deliverables_Submission_Schedule_v3.xlsx`)
6. **Received files** — what was actually delivered (check `02_Submittals/`, email attachments)

### Phase 2: Identify the CG's Rules

From the CG email, extract:
- **Deadline date** — e.g., 3 months from DMP approval (21 May → 21 Aug 2026)
- **Deliverable categories** — e.g., DD Drawings, Material Submittals, IFC Drawings, Coordination Drawings
- **Submission rules** — basement first, staggered (no clustering), include review buffers
- **Approval requirement** — "fully delivered AND approved" vs just submitted

### Phase 3: Map the Current State

For EACH discipline, determine:
- Has the consultant been appointed? (pre-qual status from log/emails)
- Have any design submissions been received? What's their CG status (A/B/C/D)?
- Are there missing/overdue items?
- What's the dependency chain? (IFC depends on DD approval, etc.)

Build a status matrix:
| Discipline | Appointed? | DD Submitted? | CG Status | IFC Status | Risk |
|------------|-----------|--------------|-----------|-----------|------|

### Phase 4: Build the Schedule with Review Buffers

Apply these buffer rules per complexity:
- **Simple** (1-sheet submittal): 2 WD Samaya review, 7 WD CG review
- **Medium** (multi-sheet package): 3 WD Samaya, 14 WD CG
- **Complex** (full discipline package): 5-7 WD Samaya, 14-21 WD CG
- **Resubmission** (Code B/C): 3 WD Samaya, 7-10 WD CG

Stagger same-discipline submissions by min 5 WD. Working week: Sun-Thu (KSA).

Calculate:
```
Prep → Samaya Review → CG Submit → CG Review (N WD) → CG Response
→ If Code A: Approved → IFC can start
→ If Code B/C: Revise (3-10 WD) → Resubmit → CG Re-review (7-10 WD)
→ If Code D: Rejected — complete redesign needed
```

### Phase 5: Cross-Reference Register Log

The Register Log (`.xlsx` with multiple sheets) contains the actual CG response history:

| Log Sheet | Tracks | Key Fields |
|-----------|--------|------------|
| Material Submittal | MA-xxxx document numbers | Date Received, Date Reply, Status (A/B/C/D) |
| Starting New Activity | SNA-xxxx | Assessment approvals |
| Inspection Request | IR-xxxx | Site inspection outcomes |
| Document Submittals | PL-/ZD-xxxx | Plan/document submissions |
| Pre-Qualification | PQ-xxxx | Vendor approvals |
| Shop Drawings | SD-xxxx | Construction drawings |
| Method Statement | MS-xxxx | Installation methods |

**Matching:** Map document numbers from log (e.g., `MOC-MUS-ASE-1A0-MA-0006`) to submission plan items (e.g., MS-04 Showcase Materials). The log's `Status` column uses codes: A=Approved, B=Approved w/Comments, C=Revise & Resubmit, D=Rejected.

Dates in the log are Excel serial numbers — convert with:
```python
from datetime import datetime, timedelta
base = datetime(1899, 12, 30)
actual = base + timedelta(days=serial_date)
```

### Phase 6: Clean Up Duplicates

When multiple data sources describe the same scope:
- **"Architectural" vs "NRS"** — base-build architectural construction (blockwork, flooring, joinery) is DIFFERENT from NRS exhibition design. Keep separate.
- **"Exhibition Works" vs NRS** — Exhibition Works = installer subcontractor. NRS = designer. DIFFERENT.
- **"Design Consultant" vs NRS** — Design Consultant pre-qual IS NRS. Update status to COMPLETED, don't duplicate.
- **"Display Cases" vs "Display Cases (GH)"** — same category. Merge GH submittals under the existing "Display Cases" discipline.

**Legit overlaps to keep:**
- "Architectural/Design" = NRS exhibition DD drawings (design-phase)
- "Architectural/SD" = base-build shop drawings (construction-phase)
- "Exhibition Works" = installation contractor's scope

### Phase 7: Report Verdict

For each of CG's categories, give a clear YES/NO:
```
1. DD Drawings: ✅ POSSIBLE — 10/10 packages by 18-Aug
2. Material Submittals: ✅ POSSIBLE — 8/8 by 22-Jul
3. IFC Drawings: ❌ NOT POSSIBLE — only 2/10 fit
4. Coordination: ❌ NOT POSSIBLE — needs until Oct
```

Root cause: IFC depends on DD APPROVAL (not just submission). Complex MEP DD takes until 4-18 Aug, leaving no time for IFC prep + review.

## Pitfalls

- **Don't trust "Planned" status** — the original plan may have serial dates from Dec 2025 that are all past due. Every row needs a realistic status.
- **Register Log vs Submission Plan** — the log tracks construction-phase materials (flooring tiles, concrete blocks). The submission plan tracks design-phase deliverables. They overlap only at specific items (MS-04 Showcases, some MEP equipment).
- **Column shifts** — inserting columns in an existing formatted Excel shifts ALL data. Always verify column mapping after insert_cols().
- **Excel serial date leakage** — after column shifts, old serial dates (e.g., 46062) can end up in wrong columns. Clean up with a sweep: if col contains int > 45000, clear it.
- **IFC dependency** — the most common schedule error is assuming IFC can start immediately after DD SUBMISSION. It depends on DD APPROVAL, which adds 14-21 WD + possible resubmission cycle.
