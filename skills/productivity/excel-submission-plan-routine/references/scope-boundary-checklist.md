# Scope Boundary Checklist — Submission Plans

Before assigning a deliverable to a discipline, read the specialist's SoW. Do not assume.

## Common Traps (verified from actual SoW documents)

| Deliverable | Assumed Owner | Actual Owner | Source |
|-------------|---------------|--------------|--------|
| Landscape Lighting Layout | Studio ZNA (Lighting Designer) | **Landscape specialist** | ZNA SoW covers interior only (exhibition, galleries, showcases, public areas). No external/terrace/landscape lighting. |
| Graphics panel production | Architect (NRS) | **Graphics specialist (Graphit)** | Graphit Sub-08 scope |
| Showcase electrical integration | MEP Contractor | **Showcase manufacturer (Glasbau Hahn)** | Showcase scope includes own electrical |
| AV hardware mounting details | Structural Engineer | **AV specialist (Rawasin)** | AV scope includes mounting design |
| Emergency lighting layout | Lighting Designer (ZNA) | **MEP (AD Engineering)** | Per ZNA contract review G1 — gap between AD and ZNA |
| BMS/DALI integration | Lighting Designer (ZNA) | **ICT/BMS Specialist** | ZNA provides design intent only; detailed control engineering excluded |

## Verification Protocol

1. Find the specialist's SoW PDF in `24_Subcontractors/{Specialist}/00_Scope_of_Work_from_04/`
2. Extract text with PyMuPDF (`fitz`)
3. Search for keywords: external, landscape, terrace, outdoor, exterior, facade
4. If no match, the deliverable stays with the discipline that owns the physical element
5. If unsure, list as a coordination interface — never assign to the wrong discipline
