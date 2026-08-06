# Subcontractor SOW + RACI Matrix DOCX Generation

When the user asks for a "complete SOW" for a subcontractor (setwork, FF&E, fit-out, acoustic, etc.) with a RACI matrix, generate a full Samaya-branded DOCX, not a stub. This is a recurring class of work for the Aseer Museum specialist packages.

## Source of truth

The draft baseline lives in the repo as markdown:
`03_Plans/15_Subcontractor_Deliverables/Draft_SOW_RACI/<NN>_<Package>_SOW_RACI_Draft.md`

Read it first — it already has Included Scope, Exclusions/Interfaces, Deliverables, Quality/HSE/BIM/Sustainability controls, and an Open-Items table. Build the DOCX from this, filling gaps.

## Standard 9-section SOW structure

1. **Document Control** — package, doc ref, rev, date, prepared by, status, governing source (e.g. `6380_KMS_RPT_PM_AS_00006`), contract no.
2. **Scope Basis** — 2 short paragraphs: what the contractor is responsible for + governing docs + any PM direction that clarified package split.
3. **Included Scope** — table: Ref (SOW-01..) / Scope Item / Source. 4-6 rows.
4. **Exclusions and Interfaces** — table: Excluded Item / Responsible Party / Coordination Requirement. List every specialist interface (showcases, AV/IT, lighting, graphics, MEP, structural, FF&E, base-build).
5. **Deliverables Schedule** — table: Deliverable / Stage Gate / Acceptance Criteria.
6. **RACI Matrix** — see below.
7. **Quality, HSE, BIM and Sustainability Controls** — table: Control / Requirement / Evidence.
8. **Submittal Requirements** — short prose: Aconex CDE, 14-calendar-day CG review, CRS for Code C resubmission within 10 WD.
9. **Commercial Terms** — short prose: price deemed inclusive; out-of-scope raised as TQ; variations via VO, no work without signed VO.

## RACI Matrix — FILL EVERY CELL (user rejects TBC)

The draft markdown often leaves the RACI rows as `TBC`. Fill them with real R/A/C/I values before generating. Standard roles column:
`Activity | Setwork Contr. | Samaya Tech Office | Samaya Proc. | NRS (Design) | BIM Manager | CG | PMC (ACE) | MoC`

Typical activities and a reasonable default pattern (verify against project RACI in the approved Stakeholder Plan Sec 9 if it exists):
- Shop drawings / fabrication drawings: R / A / - / C / C / A / I / I
- Material selection & sample submission: R / C / C / A / - / A / I / I
- Material testing (Oddy, VOC, fire): R / A / - / I / - / A / I / I
- Mock-up fabrication & approval: R / C / - / A / I / A / I / I
- Off-site fabrication & QC: R / A / C / I / - / I / I / -
- Interface coordination: R / A / - / C / C / I / I / -
- Installation & on-site integration: R / A / - / C / C / I / I / -
- Snagging & defect rectification: R / A / - / - / - / I / I / -
- As-built docs & O&M: R / A / - / I / C / I / A / I
- Handover & training: R / A / - / I / - / I / A / A

## Humanised prose (user correction — "dont talk too much")

The user rejected the first SOW draft for being verbose and AI-sounding. Rules when writing body paragraphs:
- Short active sentences. One idea per paragraph. No padding.
- Replace every `§` with "Section N" (never the section symbol).
- No em-dashes, arrows, or emoji status symbols — plain ASCII punctuation.
- No AI clichés (comprehensive, robust, seamless, "it is worth noting").
- Keep tables dense and factual; keep prose minimal — the tables carry the substance.

## Generate + open

Write the Python script to /tmp, run it, then `open` the output. Output path convention:
`03_Plans/15_Subcontractor_Deliverables/Draft_SOW_RACI/<Package>_Contractor_SOW_Rev00.docx`

After the user confirms the draft, offer to commit it to the repo.
