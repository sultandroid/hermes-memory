---
name: material-submittal-resubmission
description: "Respond to CG Code C material submittal rejections — build CRS sheets, track compliance, and prepare resubmissions (Aseer Museum MA-0007 pattern)"
version: 1.0.0
author: Samaya Tech Office
---

# Material Submittal Resubmission (Code C → Rev.01)

Workflow for responding to a CG **Code C (Revise and Resubmit)** material submittal rejection and preparing the resubmission. Built from the Aseer Museum MA-0007 (Patinated Brass) case.

## When to use
- A material submittal (MA-XXXX) comes back **Code C** from CG
- You need to build a **CRS sheet** (Comments Resolution Sheet) responding to each CG comment
- You need to track which requirements are complied vs pending, and prepare the Rev.01 resubmission

## Core concepts

### The CRS sheet (MOC_HQ template)
Use the official MOC_HQ CRS Excel template — NOT a custom one. The user explicitly corrected this: *"use deffrent template i will send the last template for CRS sheet"*.

**Template location:** `https://samaya-factory.com/assets/templates/CRS_Template_MOC_HQ.xlsx` (deployed shared asset; referenced in `aseer-museum-pm/AGENTS.md` style-guide table).

**Template structure (columns A–Q):**
- Header block: Project name, CRS number, Doc No., Doc Title, Rev., Date, Discipline
- Comment rows (rows 11+): `A=No.`, `B=Initial`, `C=Sheet`, `D:H=Reviewer Comment`, `I:N=Originator Reply`, `O=Reply By`, `P:Q=Reply Status by Reviewer`
- Legend rows 42–50: status codes (A=Approved, B=Approved w/ comments, C=Revise & Resubmit, D=Rejected, F=For Information) + sign-off block (SC / PMCM / MOC / Originator)

**Fill with openpyxl** — load the template, write header + comment rows, save to the sample's Rev01 OneDrive folder. The "Reply Status by Reviewer" column (P) is filled by CG, not by us — mark our intended status (Closed/Open) as provisional.

### Compliance tracking — classify each CG requirement
For each CG comment, classify as **COMPLIED / PENDING / PARTIAL**:

| Status | Meaning | Example |
|--------|---------|---------|
| COMPLIED | Evidence in hand | Oddy test PASS, chemical composition datasheet, manufacturer details |
| PENDING | Supplier lead-time, follow as Rev.02 | VOC, off-gassing, fire-rated, MSDS |
| PARTIAL | One option ready, other in dev | 2 alternative samples (A ready, B in development) |

**Key insight — challenge over-demanding requirements.** Not every CG requirement is technically justified. For a metal (brass):
- **Oddy test** — legitimately required (museum conservation), and the decisive one. A PASS here is the strongest lever to flip Code C → B/A.
- **Chemical composition** — covered by the alloy datasheet (e.g. KME CuZn37/C27200).
- **MSDS** — standard, easy, legit.
- **VOC / off-gassing** — only matters for sealed showcase interiors, not open walls/doors. Metals don't emit VOC; the lacquer does.
- **Fire-rated** — over-demanding for a non-combustible metal.
- **2 alternative manufacturers** — over-demanding when the material is single-source globally (documented via supplier letter).

**Strategy:** submit what you have + commit to the rest with a deadline (Rev.02 addendum) + raise documented technical objections on the over-demanding items. This shifts programme-delay pressure onto CG, not Samaya.

## Workflow steps

1. **Pull the current status** from the submission DB (single source of truth):
   ```sql
   SELECT s.doc_no, st.code, st.label, s.revision, s.is_latest
   FROM submission s JOIN status st ON s.status_id=st.id
   WHERE s.doc_no LIKE '%MA-XXXX%' ORDER BY s.revision;
   ```
   (DB at `aseer-museum-pm/08_Document_Index/submission.db`; latest-revision-wins. Do NOT read codes from stale markdown registers.)

2. **Read the CG rejection requirements** — from the register reconciliation notes or the CG response doc. List every requirement.

3. **Gather evidence** for each requirement:
   - Oddy test report (NonaChem T2607222 pattern — PASS = P/Permanent on Ag/Cu/Pb)
   - Alloy datasheet (KME CuZn37) for chemical composition
   - Manufacturer profile (see below — identify the MATERIAL's manufacturer, not the fabricator)
   - NRS review docs

### Manufacturer vs fabricator — identify the MATERIAL's maker
When CG asks for **manufacturer details**, they mean the maker of the **material itself**, NOT the specialist who assembles it into the final product. In the MA-0007 case: **Eden-Design GmbH** (Iserlohn, Germany) manufactures the patinated brass (EDEN BRONZE™ — solid brass CuZn, chemically bronzed & patinated), while **Glasbau Hahn** (PQ-0063, Code B) is only the approved showcase *fabricator* who assembles the material into showcases. Do not answer a "manufacturer" comment with the fabricator's profile. If the material has two elements (substrate + surface finish), name both: substrate alloy maker (e.g. KME) + surface-finish/patination house (e.g. Eden-Design).

### Building a company profile when the manufacturer has none
If the manufacturer has no official company-profile PDF, build one ourselves from their website + certificates (same pattern as the fabricator profile). User requirements:
- **General company profile** — the company overall and ALL its product lines, NOT a profile focused on our specific product.
- **Preferred format is a text-only site summary** (the user rejected the image-grid version): list product lines as a table, plus sections for processes/capabilities, applications & project types, and environment & sustainability. Treat the file as a summary of their whole website.
- **Include**: company name/legal entity, address, established year, core business, contact, product lines, processes, applications, and (if the user supplies it) an environment & sustainability block.
- **Do NOT include a Certifications section by default** — the user supplies their own cert copy and said to remove it. Keep ISO badges in the header only.
- **Footer label = "Company details"** (NOT "Company Profile · Confidential") — because the profile is self-made from their public info, not an official manufacturer document.
- **Never mention our project name** (e.g. "Aseer Regional Museum") in a manufacturer's profile — it's internal, and the profile is a generic company document.
- If the site has no dedicated references/projects page (Eden-Design's `/references-2/`, `/referenzen/`, `/historie/` all 404), source "projects" from the homepage's Applications block instead.
- Render as a single A4 page via weasyprint (HTML → PDF); compress spacing/fonts to fit one page.
- Be transparent: the profile is self-made from their public info, not an official manufacturer brochure. If CG demands an official brochure, request one from the manufacturer.

4. **Build the CRS sheet** from the MOC_HQ template (see above).

5. **Prepare the resubmission package** — CRS + evidence PDFs + schedule extract, saved to the sample's `MA-XXXX Rev01/` OneDrive folder.

6. **Update the risk register** — a passed Oddy test lowers the risk score (e.g. PRR-PRC-05 from Critical). Update actions A1–A4 and target close.

7. **Draft the CG reply email** — lead with the decisive evidence (Oddy PASS), commit to Rev.02 for pending certs, request Rev.01 approval.

## Pitfalls
- **ALWAYS humanize CRS replies** — natural engineer voice, no AI/template phrasing, no inflated counts. The user repeatedly corrected this. Write replies as a working engineer would, not as a form letter. E.g. don't say "four (4) applications" when one line item covers six elements — say "all patinated brass applications" and enumerate them.
- **Propose the material as the CONTROL SAMPLE** — if the project has not yet submitted a control sample for that raw material, state the material is proposed as the control sample. This is a strong, legitimate argument that anchors the submission and pre-empts "no reference sample" pushback.
- **Build a SAMPLE BANK / multi-source story** — when the same material arrives from multiple suppliers (e.g. anodised aluminium from the German maker via the fabricator, plus a Chinese supplier and a local KSA supplier to the same spec, plus the same finish on a different substrate like SS304), list them all as "available for reference". Multiple sources for the same material = supply security + price competition + local support, and it strengthens the reply. Don't name a supplier you're not committing to — "a Chinese supplier" / "a local (KSA) supplier" is safer than naming one before it's approved.
- **Oddy vs VOC are complementary, not substitutes** — Oddy protects the ARTIFACTS (corrosion on Ag/Cu/Pb); VOC protects the PEOPLE (air quality in sealed spaces). CG wants both. A passed Oddy is the strongest lever but does not clear the VOC requirement.
- **Off-gassing is a DUPLICATE of Oddy** — a passed Oddy already confirms no corrosive emissions, which covers off-gassing. State this explicitly ("is therefore a duplicate of the Oddy result") and commit to closing the point formally via Rev.02, rather than re-running a redundant test. This is a documented technical objection, not a refusal.
- **Fire-rated for a non-combustible metal is over-demanding** — state "brass is a non-combustible metal, so no fire-rating is technically required", but keep the item OPEN and commit to a "for the record" report as Rev.02 (don't close it — closing on a technical objection risks antagonising CG; Open + "for the record" is the smart middle).
- **MSDS sourcing reality** — the KME site times out on direct download; a same-alloy SDS from another maker (e.g. Robert Laminage CuZn37/C27200) is findable but the user judged it NOT useful for the submission (it only confirms "solid metal, not hazardous"). Close the MSDS item simply: the SDS for the patination chemicals comes from the material manufacturer (Eden-Design) as a Rev.02 addendum. Don't attach a generic same-alloy SDS that adds nothing.
- **The user often fills the CRS sheet themselves** — when they say "انا بعمله بنفسي" (I'll do it myself), STOP editing the file. Provide the humanized replies as reference text only; don't touch the workbook.
- **When a material spans multiple applications, name each application's fabricator** — don't stop at the showcase specialist. Every application (setworks, doors, reception, wayfinding, floorbox trim) is fabricated by its own approved specialist; the material itself comes from one manufacturer. Enumerate all applications from the approved schedule.
- **Single-source argument strengthens the reply** — if the material must match in colour/finish across applications, state it is supplied from one source (the manufacturer) to guarantee consistency. This is a technical justification, not filler.
- **Don't invent applications/locations** not in the approved schedule. Pull formal names verbatim from the approved Finishes Schedule PDF, not from `materials.json` (which can miss entries present in the PDF).
- **Thickness is application-dependent** — the sample is for finish/look-and-feel, not a fixed gauge. State "thickness varies by application" with the range, don't hard-code one.
- **Unify on the Aconex number** — use `MOC-MUS-ASE-1A0-MA-XXXX` (or short `MA-XXXX`), not the internal sample code (`SAM-FIN-PB-001`). The user wants a single source of truth. Rename folder/photo/QR + regenerate QR to the new clean URL.
- **OneDrive deadlock** — reading/writing OneDrive files can hit "Resource deadlock avoided". Quit OneDrive, wait ~30s, retry; or stage to `/tmp` first.
- **The Oddy test is the decisive lever** — a PASS directly clears the highest-risk item that drove the Code C. Lead the resubmission with it.

## Related
- `sample-submittal-system` (protected) — sample page design, A4 layout, deploy
- `samaya-factory-deploy` (protected) — server deploy mechanics
- `aseer-museum-pm/AGENTS.md` — repo rules, submission DB protocol, risk closure rule (Code B = practical final approval)

## Reference
- `references/ma-0007-patinated-brass-example.md` — worked example: MA-0007 compliance table, approved applications, CRS openpyxl fill pattern, Oddy report facts, risk linkage.
- `references/ma-0007-crs-humanized-replies.md` — the FINAL humanized reply wording for every CG comment (items 1–10), plus the sample-bank table. Copy these verbatim into the CRS sheet.
- `references/eden-design-manufacturer-profile.md` — Eden-Design GmbH facts (the patinated-brass material maker), ISO cert numbers, product-line image URLs, and the single-A4 company-profile build recipe.
