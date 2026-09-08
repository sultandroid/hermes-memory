# Material Submittal (MA) Comment-Response Strategy

How to respond to a CG **Code C (Revise & Resubmit)** on a material submittal (e.g. MA-0007 Patinated Brass). The goal is to flip Code C → Code B/A by submitting what you have, committing to the rest with a date, and technically challenging over-demanding certs — putting the delay risk on CG, not Samaya.

## Core principle
Do NOT fight every CG requirement — that stalls the project. Instead classify each requirement and respond accordingly. The strongest position is: submit the decisive evidence now + a dated commitment for the rest + a documented technical objection to the unreasonable items. This shifts the "who is delaying the project" burden onto CG.

## Classification of CG requirements

| Class | What it is | How to respond |
|-------|------------|----------------|
| **Complied** | Evidence already in hand | Mark Closed, attach the doc |
| **Pending** | Supplier lead-time item | Mark Open, commit to a dated Rev.02 addendum |
| **Partial** | Partly done | Mark Open, show what's ready + what's in development |
| **Over-demanding** | Technically unjustified | Raise a documented technical objection |

## The decisive-evidence pattern
For a material submittal, the **Oddy test** is usually the highest-risk item that drove the Code C. If it passes, that is the decisive fix. Frame the resubmission around it: "Oddy test PASSED (Permanent) — the decisive test for a museum environment. Approve Rev.01 now; remaining certs follow as Rev.02."

## Technically challenging over-demanding certs (with reasoning)
These are the ones CG often over-demands on a metal material. Object with documented logic, don't just refuse:

- **Fire-rated report on a metal** — metal is non-combustible. Fire-rating matters for combustible materials (fabric, wood, plastic). Requesting a fire cert for brass = applying a generic checklist without thinking. Object: "Brass is a non-combustible metal; fire-rating report to be issued for the record."
- **Off-gassing test when Oddy already passed** — the Oddy test already confirms no corrosive emissions. Off-gassing is redundant with Oddy + VOC. Object: "The passed Oddy test (report no.) already confirms no corrosive emissions."
- **2 alternative certified manufacturers for a single-source material** — if the manufacturer confirms only ONE global supplier exists (e.g. Glasbau Hahn Letter 002), requesting 2 additional certified manufacturers is impossible. Object: "Manufacturer confirms single global source; provide supplementary finish options (powder coat, PVD) instead."
- **VOC on a bare metal** — metals don't emit VOC; the lacquer/coating does. VOC matters only for sealed showcase interiors, not open walls/doors. Respond partially: commit VOC for sealed spaces only.

## What a metal datasheet does and does NOT cover
A manufacturer alloy datasheet (e.g. KME CuZn37/C27200) covers **chemical composition** only. It does NOT cover VOC, off-gassing, fire-rating, or MSDS. When a user asks "is this datasheet enough for VOC?" — the answer is no; VOC comes from the coating/lacquer, not the alloy. Use the datasheet to close the **chemical composition** requirement, not the others.

## CRS sheet structure for a material submittal
Use the MOC_HQ template (see main SKILL.md). Fill the comment rows (No / Initial / Sheet / Reviewer Comment / Originator Reply / Reply By / Reply Status). The "Reply Status by Reviewer" column is filled by CG, not by Samaya — mark your own status (Closed/Open) as a provisional indicator only.

## Example: MA-0007 Patinated Brass (worked example)
CG Code C (02-Jul) required: NRS comments, all applications, manufacturer details, Oddy, VOC, off-gassing, chemical composition, fire-rated, MSDS, 2 alternatives.

| Requirement | Class | Evidence |
|-------------|-------|----------|
| NRS comments | Complied | ZD-0033/ZD-0060 extracts |
| All applications | Complied | Finishes Schedule 6930 extract |
| Manufacturer details | Complied | Glasbau Hahn (PQ-0063 Code B) |
| Oddy test | Complied | NonaChem T2607222 — PASS (Permanent) |
| Chemical composition | Complied | KME CuZn37 datasheet |
| MSDS | Pending | GBH → Rev.02 |
| VOC | Pending (partial) | GBH → Rev.02; sealed spaces only |
| Off-gassing | Over-demanding | Redundant with passed Oddy |
| Fire-rated | Over-demanding | Metal non-combustible |
| 2 alternatives | Partial | IGP 591T ready + PVD in development |

## Source of truth for applications list
When listing a material's applications in the submittal, source from the **approved Finishes Schedule PDF** (`6930_Finishes_Schedule_rev A.pdf`), NOT from `aseer-museum-viz/src/data/materials.json`. The JSON can carry items not in the approved schedule (e.g. Wayfinding Signage FI_GR_11 appeared in JSON but was absent from the approved PDF). Read the PDF directly with PyMuPDF (`fitz`) and list only the `FI_*` entries whose Material Description/Colour actually say patinated brass. Drop generic/placeholder applications (cladding, handrails, screens, joinery, lift lobby) that were never in the schedule.
