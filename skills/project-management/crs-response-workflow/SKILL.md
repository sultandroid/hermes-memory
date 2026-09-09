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

## Reply writing — ALWAYS humanize
The user's standing rule for CRS replies: **humanize every reply** — natural engineer voice, no AI/template phrasing, no inflated counts. Concretely:
- **Don't inflate counts.** Saying "all four (4) applications" is misleading when one schedule item (e.g. FI_ME_01) alone covers 6 elements (walls, doors, reveals, setworks, AV units, reception desk). Say "all patinated brass applications" and enumerate them fully — this shows CG full coverage, not a small number.
- **State facts plainly.** "The submittal now covers all patinated brass applications in the approved Finishes Schedule 6930 (Rev A), not just the showcases:" then a bulleted list with each schedule ref.
- **Tie claims to a source.** "per their letter of confirmation" / "per the approved schedule" instead of bare assertions.
- **Distinguish material from fabrication.** When CG asks for "manufacturer details", they mean the **material** manufacturer, not the showcase fabricator. For patinated brass: the material (EDEN BRONZE™, solid CuZn chemically bronzed & patinated) is made by **Eden-Design GmbH** (Iserlohn, Germany); **Glasbau Hahn** (PQ-0063, Code B) is the approved showcase *fabricator* who assembles showcases from that material. Name both roles explicitly — don't answer a material question with the fabricator.
- **Enumerate EVERY application, each with its own approved fabricator.** When CG asks about fabrication, don't stop at showcases. List all applications from the approved schedule and state each is fabricated by its respective approved specialist: Showcases (Glasbau Hahn), Setworks (display units/frames/AV), Main gallery doors & door reveals, Reception desk, Reception feature wall (FI_ST_03), Wayfinding signage (FI_GR_11), Floorbox trim (FI_ME_03). The material comes from one source; each application is assembled by its own specialist.
- **Single-source argument for finish matching.** State that the patinated brass is supplied from a **single source** (Eden-Design) specifically to guarantee colour/finish consistency across all applications. This is a strong technical justification that also pre-empts the "2 alternatives" objection.
- **MSDS: substrate online, chemicals from manufacturer.** For a metal material, the SDS splits in two: (a) the **substrate alloy** SDS (e.g. CuZn37/C27200) is freely available online from any manufacturer of the same alloy (e.g. Robert Laminage SA) — grab it immediately; (b) the **surface-treatment chemicals** (patination) SDS is proprietary to the material manufacturer (Eden-Design) and must be requested from them, submitted as a Rev.02 addendum. Reply: "The SDS for the CuZn37 brass substrate is attached. The SDS for the patination chemicals will be issued by the material manufacturer, Eden-Design GmbH, and submitted as a Rev.02 addendum." Status Open (partially met).
- **A generic substrate SDS is often NOT useful for the CG requirement.** A CuZn37 SDS from a third-party alloy maker only confirms "solid metal, not hazardous / no special measures required" — it does NOT address the CG concern (the patination chemicals). The user's call: don't attach a low-value generic SDS; just commit to the manufacturer's chemicals SDS as a Rev.02 addendum. Keep the generic SDS as an internal reference only, not part of the submission.

## When to push back (technical objections)
Not every CG comment is legitimate. Push back with documented technical reasoning on:
- **Fire-rated report for a metal** — metal is non-combustible; a fire-rating certificate is overreach.
- **Off-gassing test when Oddy already passed** — the Oddy test already confirms no corrosive emissions; off-gassing is redundant.
- **2 alternative manufacturers for a single-source material** — if the supplier confirms only one global source exists (e.g. Glasbau Hahn Letter 002), document that and offer alternatives as *supplementary options*, not substitutions.
- **Control-sample framing for the "2 alternatives" objection.** When CG asks for alternative samples, the strongest framing is: the submitted material is proposed as the project's **control sample** for that raw material, because **no control sample has yet been submitted for it on the project**. State this up front, then present the alternatives as *supplementary reference choices only, not a substitution* of the control sample. This anchors the approved material as the baseline and pre-empts CG treating an alternative as a replacement. (If the user mentions other control samples received — e.g. an aluminium sample — note them as building a control-sample bank, which strengthens the position.)
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

## Material manufacturer reference
See `references/eden-design-manufacturer.md` for Eden-Design GmbH (the patinated brass material manufacturer) — contact, ISO certs, product line, and the material-vs-fabricator split vs Glasbau Hahn.

## Building a manufacturer profile PDF (no official brochure)
When the material manufacturer has no downloadable company-profile PDF (only web pages + ISO certs), build a one-page A4 profile from their site facts + ISO certs for speed. See `references/foreign-manufacturer-profile-pdf.md` for the full pattern — weasyprint one-page HTML, brand-matching color scheme, image-only ISO cert handling, and the hard rules: NEVER put the project name in a manufacturer's profile, and make it a GENERAL company profile (all products + applications, NOT our specific material) unless the user asks otherwise.
