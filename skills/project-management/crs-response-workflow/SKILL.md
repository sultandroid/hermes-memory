---
name: crs-response-workflow
description: "Respond to CG Code C material submittal rejections with a Comments Resolution Sheet (CRS) + compliance tracking + resubmission package"
version: 1.0.0
author: Samaya Tech Office
---

# CRS Response Workflow (CG Material Submittal Resubmission)

When CG returns a material submittal **Code C (Revise & Resubmit)**, the response is a **Comments Resolution Sheet (CRS)** that maps each CG comment to a compliance status, backed by evidence. This skill covers the full workflow: gather the rejection requirements, build the CRS, track compliance, and assemble the resubmission.

## Trigger
- A material submittal (MA-XXXX) comes back Code C / Code D from CG.
- User asks to "prepare the resubmission", "make a CRS sheet", or "respond to the comments".

## Source-of-truth rules (Aseer Museum)
- **Submittal code** comes ONLY from the submission DB: `08_Document_Index/submission.db` (query `SELECT s.doc_no, st.code, st.label FROM submission s JOIN status st ON s.status_id=st.id WHERE s.is_latest=1 AND s.doc_no LIKE '%<ref>%'`). Never read codes from `PROJECT_MEMORY.md` or stale registers.
- **CG rejection requirements** live in the register reconciliation notes (`01_Registers/material_submittal_register.md`) and the CG response PDF.
- **Approved material applications** come from the approved Finishes Schedule PDF (e.g. `6930_Finishes_Schedule_rev A.pdf`), NOT from `materials.json` — the JSON can miss items that ARE in the approved PDF (e.g. FI_GR_11 Wayfinding Signage). When the user asks "is this all?", re-read the approved PDF directly.

## CRS template
Use the **MOC_HQ CRS template** (Excel) — the official format, not a custom one. Public URL:
`https://samaya-factory.com/assets/templates/CRS_Template_MOC_HQ.xlsx`
(Deployed 2026-09-08; see `samaya-factory-deploy` skill for how to deploy templates.)

Template structure:
- Header block: Project, CRS number, Doc No, Rev, Date, Title, Discipline.
- Comment rows (columns): No · Initial · Sheet · Reviewer Comment (D:H) · Originator Reply (I:N) · Reply By (O) · Reply Status by Reviewer (P:Q).
- The "Reply Status by Reviewer" column is filled by CG, not by us — mark our intended status (Closed/Open) as provisional.
- Fill with openpyxl, preserving the template's merged cells and column widths.

## Compliance status categories
| Status | Meaning |
|--------|---------|
| **COMPLIED** | Evidence attached, requirement met |
| **PENDING** | In progress with supplier, follows as Rev.02 addendum |
| **PARTIAL** | Partly met (e.g. one of two alternatives ready) |
| **OBJECTION** | Technical pushback — requirement is overreach (see below) |

## When to push back (technical objections)
Not every CG comment is legitimate. Push back with documented technical reasoning on:
- **Fire-rated report for a metal** — metal is non-combustible; a fire-rating certificate is overreach.
- **Off-gassing test when Oddy already passed** — the Oddy test already confirms no corrosive emissions; off-gassing is redundant.
- **2 alternative manufacturers for a single-source material** — if the supplier confirms only one global source exists (e.g. Glasbau Hahn Letter 002), document that and offer alternatives as *supplementary options*, not substitutions.
- **VOC for open applications** — VOC matters only in sealed/closed spaces (showcase interiors), not open walls/doors.

Frame objections as: "requirement X is overreach because [technical reason]; we offer [what we can provide] instead." This shifts programme-delay risk onto CG.

## Resubmission strategy
- **Lead with the decisive fix.** If the main blocker (e.g. Oddy test) now passes, that's the headline — request approval (Code B/A) on that strength.
- **Split tracks** when a finish test is pending: Track A (shop drawings + non-finish materials) proceeds independently; Track B (finish) follows. Patinated brass is a surface finish only and does not affect fabrication.
- **Remaining certs follow as Rev.02 addendum** with a committed timeline (e.g. 30 days from supplier), not held back indefinitely.
- **Sample is for finish/look-and-feel, not thickness** — thickness varies by application (doors ~1mm, showcases ~2mm). State this explicitly.

## Workflow steps
1. Pull the submittal's current code from the submission DB.
2. Read the CG rejection requirements (register notes + CG response PDF).
3. Read the approved Finishes Schedule PDF for the full application list.
4. Build the CRS from the MOC_HQ template, one row per CG comment.
5. Classify each row COMPLIED / PENDING / PARTIAL / OBJECTION.
6. Save to the submittal's Rev01 folder in OneDrive (e.g. `.../Brass_Patinated_Sample_GH/MA-007 Rev01/`).
7. Assemble the resubmission package: CRS + test reports (e.g. Oddy) + datasheets + schedule extract.
8. Update the risk register if a risk (e.g. PRR-PRC-05) is affected by the outcome.

## Pitfalls
- **Don't invent applications** not in the approved schedule. Use exact formal names (Wall Cladding, Main Gallery Doors, Door Reveals, Setworks — Display Units/Frames/AV Units, Reception Desk, Floorbox Trim, Reception Feature Wall, Wayfinding Signage).
- **Don't fabricate test results** — only mark COMPLIED when the evidence actually exists (e.g. Oddy report T2607222 in hand).
- **OneDrive deadlock** — reading/writing OneDrive files can hit "Resource deadlock avoided". Quit OneDrive, wait ~30s, retry, or stage to /tmp first.
- **The CRS "Reply Status" column is CG's to fill** — don't present our provisional status as final.

## Worked example
See `references/ma0007-patinated-brass-example.md` for the full MA-0007 patinated brass resubmission: the 10 CG requirements with compliance statuses, approved applications, evidence files, email thread, and resubmission framing.
