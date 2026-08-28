# CG Comment Dependency-Chain Tracing (Aseer Museum)

When a CG comment says "must be confirmed after X is approved" (e.g. ZD-0114 structural: *"confirm after approval of cloud survey"*, *"confirm fc' after concrete core test results"*), the comment names **prerequisite activities** whose status determines whether the submittal can actually be closed. To answer "what's really blocking / what do we need to do", trace the full dependency chain — do NOT answer from the comment alone.

## Steps

1. **Extract the named prerequisites** from the CG comment. ZD-0114 (Code C, structural) named: cloud survey, concrete core testing, geotechnical borehole, foundations model, unsafe-element calcs.

2. **Trace each prerequisite's status in Outlook** — search by keyword, not just the doc ref:
   ```sql
   SELECT m.Record_RecordID, datetime(m.Message_TimeReceived,'unixepoch','localtime'),
          f.Folder_Name, m.Message_SenderList, substr(m.Message_NormalizedSubject,1,60),
          m.Message_HasAttachment
   FROM Mail m JOIN folders f ON m.Record_FolderID=f.Record_RecordID
   WHERE (m.Message_NormalizedSubject LIKE '%cloud survey%'
      OR m.Message_NormalizedSubject LIKE '%demolition%'
      OR m.Message_NormalizedSubject LIKE '%dismantl%'
      OR m.Message_NormalizedSubject LIKE '%core%'
      OR m.Message_NormalizedSubject LIKE '%geotech%')
     AND m.Message_Hidden=0
   ORDER BY m.Message_TimeReceived DESC;
   ```
   Keywords that surface the chain: `cloud survey`, `demolition`, `dismantl`, `3D scanner`, `core`, `geotech`, `borehole`, `SNA` (Start New Activity).

3. **Cross-reference repo registers** — `01_Registers/submittal_register.md` (per-doc CG code + status) and the `09_Agent_Workspace/backfill_analysis_*.md` files (they log SNA statuses, NCR closeouts, and per-doc CG codes). Grep for the prerequisite refs (ZD-0106, ZD-0032, NC-1G0-0018, SNA refs).

4. **Distinguish architectural vs structural survey.** The architectural cloud survey (as-built Revit + point cloud) can start without demolition. The **structural** survey needs the columns exposed — i.e. **cladding removal (marble/gypsum)** to reach the concrete and measure actual member sizes. This is the crux: the user's instinct ("structural needs us to break/remove the cladding") is correct and is exactly what the CG comment is gating on.

5. **Check the enabling-work approval status.** The demolition/dismantling plan is the enabler. In this case ZD-0106 (Dismantling for Cloud Survey) was **Code B** (approved w/ comments, 25-Aug) but ZD-0032 Rev.01 (Demolition routing plans) was still **Code C** — so the enabling work is only partially approved. That partial approval is the real blocker, not the survey itself.

6. **Conclude with the actual blocker + the decision the user must make**, not a restatement of the CG comment.

## Worked example (2026-08-27)

- CG ZD-0114 Code C, 5 comments, all gated on structural verification.
- Ahmed Gad (CG, 06-Aug) follow-up asked for: as-built column dimensions, material-testing quotations (concrete core + geotech), Big Stone technical report.
- Architectural cloud survey: started (Waris 26-Aug, RVT + RCP link).
- Structural: needs cladding removal to measure columns.
- Demolition plan: ZD-0106 Code B (approved), ZD-0032 Code C (still needs rework).
- NCR NC-1G0-0018 (cloud survey delay): CLOSED 09-Aug.
- **Blocker:** structural column measurement requires cladding removal, whose demolition plan is only partially approved (ZD-0032 Code C). Concrete core + geotech quotations still pending.

## Pitfalls

- **Don't assume the survey is one activity.** Architectural and structural cloud surveys are separate; only the architectural one can proceed without demolition.
- **A Code B on the demolition plan ≠ full approval.** Check the *other* demolition-related ref (ZD-0032) — it may still be Code C.
- **A closed NCR about the survey does NOT mean the survey is done** — it means the delay was resolved, not that the structural survey completed.
- **The user's domain instinct is often the answer.** When the user says "structural needs us to break the cladding", verify it against the CG comment + demolition plan status rather than dismissing it — it's usually the correct reading of the dependency.
