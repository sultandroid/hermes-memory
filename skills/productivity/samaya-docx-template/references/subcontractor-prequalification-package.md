# Subcontractor Prequalification Package

## When to use

When a subcontractor has been identified but lacks direct museum/cultural project experience, or when procurement needs a formal prequalification record. You prepare the document **on their behalf** (as Samaya Technical Office) to ensure they understand the project, then route it through procurement for the supplier to stamp and sign.

## Package contents

| Component | Purpose |
|-----------|---------|
| **Prequalification letter** | Confirms project understanding, design awareness, execution sequence, full compliance |
| **RACI matrix** | Defines responsibilities across subcontractor, NRS, Samaya BIM Unit, Samaya PM, CG |
| **Risk register** | 8-10 project-specific risks with likelihood/impact/severity/mitigation/owner |

## Document structure (9 sections)

1. Introduction — company interest, project name, contract ref
2. Project Understanding — scope, design intent, programme, quality standards, contractual framework
3. Design Understanding — design intent, integration with other trades, material submittal process, shop drawings
4. Execution Sequence Understanding — phased delivery, coordination, inspection hold points, handover
5. Compliance Statement — specs, QMS, HSE, programme, BEP, CG approval, SBC
6. Company Capability — experience, team, equipment, supply chain
7. RACI Matrix — 12+ activities × 6 parties (sub, NRS, Samaya BIM, Samaya PM, CG)
8. Risk Register — 8+ risks with likelihood/impact/severity/mitigation/owner
9. Declaration — signed commitment

## RACI matrix columns

| Column | Party |
|--------|-------|
| Activity | Description of work item |
| [Subcontractor Name] | R — does the work |
| NRS | A — approves design/material decisions |
| Samaya BIM Unit | R/A for BIM coordination |
| Samaya PM | A — accountable for programme/quality |
| CG | A — final approval authority |

## Risk register columns

| Column | Content |
|--------|---------|
| # | R1, R2, etc. |
| Risk Description | Specific project risk |
| Likelihood | Low / Medium / High |
| Impact | Low / Medium / High |
| Severity | Low / Medium / High (product of L×I) |
| Mitigation Measure | Concrete action to reduce risk |
| Owner | Who manages it (Procurement, Site Manager, Design Lead, PM, BIM Coord.) |

## Procurement routing workflow

1. **Prepare** the prequalification package (letter + RACI + risk register) as a DOCX
2. **Save** to `24_Subcontractors/NN_TradeName/00_Prequalification/`
3. **Email procurement** explaining:
   - The subcontractor lacks museum experience
   - You prepared a support document on their behalf
   - Procurement should send the doc to the supplier
   - Supplier must: review, apply company stamp, sign, return
4. **Procurement does NOT stamp it** — the supplier stamps their own document
5. **Separate SOW** follows later to define full scope, deliverables, programme

## Reference drawings to include

Only drawings directly related to the subcontractor's scope. For landscaping:

| Drawing type | Source location |
|-------------|-----------------|
| NRS External Details | `14_Completed_Tender_Package_From_NRS/06_Drawing_Source_Folders/1570_External_Details/` (A2742-1570 to 1578) |
| Site Development Plan | `03_Design_Files/.../Reprinted Drawings/ARCHITECTURE/11-LAYOUT/A - 62 - SITE DEVELOPMENT PLAN.pdf` |
| Irrigation Plans | `03_Design_Files/.../Reprinted Drawings/MECHANICAL/IRRIGATION/` (ME-01 to ME-05) |
| Landscape Design Comments | `03_Design_Files/00_Scope_and_Proposals/P083_Landscape Design Development COMMENTS 00.pdf` |

**Do NOT include interior architecture drawings** (GA plans, sections, wall details, room elevations, schedules) — those are not landscape-related.

## Email template (reply to procurement)

```
Subject: RE: [Supplier Name] Profile — Prequalification Support Document

Team,

Thanks for sharing the [Supplier Name] profile.

As you can see, they don't have direct museum project experience. To support
their prequalification, we prepared a document on their behalf that confirms
they understand the project, the design, the execution sequence, and that they
comply with all requirements — including a RACI matrix and risk register.

Please send this document to [Supplier Name] and ask them to:
1. Review the content.
2. Apply their company stamp.
3. Sign and return it to us.

This gives us a formal record that they acknowledge the project requirements
despite their lack of museum background. A separate SOW will follow to define
the full scope and deliverables.

Regards,
Mohamed Sultan
Technical Office Manager
```

## Pitfalls

- **Do NOT include interior drawings** for a landscape subcontractor — only site/external/irrigation drawings are relevant
- **Verify drawing relevance against the SOW scope before copying.** Do not grab drawings from the Arch DD Package just because they exist in the project folder. Read the SCOPE_REQUEST.md first, identify what the subcontractor actually does (hardscape, softscape, irrigation, site development), then search for files matching those keywords (landscape, stramp, terrace, external, site, planting, irrigation, hardscape, grading). Interior GA plans, sections, wall details, room elevations, and finishes schedules are NOT landscape drawings.
- **Search strategy for reference drawings:** Use `find` with `-iname` patterns matching the subcontractor's scope keywords. Check `14_Completed_Tender_Package_From_NRS/06_Drawing_Source_Folders/` for NRS discipline-specific folders (e.g. `1570_External_Details` for landscape). Check `03_Design_Files/` for as-built drawings in the MoC reprint folders. Do NOT default to the Arch DD Package — that is interior architecture.
- **Procurement routes to supplier** — procurement does NOT stamp the doc; the supplier stamps it
- **Supplier has no museum experience** — the prequal letter is a support document to formally record their acknowledgment, not a claim of expertise
- **Separate SOW** — the prequal letter is not the SOW; a standalone SOW doc follows later
- **RACI and risk register are expected** — a plain letter alone is insufficient; procurement and PM expect these matrices
- **Doc ref prefix** — use `MOC-ASEER-SIC-1K0-PQ-00XX` for prequalification documents
