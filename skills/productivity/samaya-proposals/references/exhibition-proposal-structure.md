# Exhibition / Museum Proposal Structure (Client-Facing)

## Structure Overview
16-page bilingual (AR/EN) HTML proposal. Strip all PMBOK jargon — this goes to the client.

## Page Layout
1. **Cover** — full-bleed navy, client logo (left), Samaya logo + ref (right), project title, 3 party icons (Client · Designer · Contractor)
2. **Table of Contents** — section links with page numbers
3. **Executive Summary** — project overview, Samaya profile, capabilities
4. **Integration & Governance** — project management approach, communication, document control
5. **Scope of Work** — detailed inclusions/exclusions table, WBS breakdown
6. **Project Management Plan** — controls, change management, reporting
7. **Schedule & Time Management** — 36-week master programme Gantt chart, milestones, long-lead items
8. **Quality Management** — QC gates, inspection points, FAT/SAT protocol, badges
9. **Resource & Organisation** — org chart with 4-tier hierarchy + headcount
10. **HSE Plan** — hazard matrix, controls, PPE requirements
11. **Risk Management** — 5×5 heatmap, risk register with 15+ items
12. **Procurement & Logistics** — supply chain, shipping, customs, warehousing
13. **Handover & Commissioning** — SAT, snagging, as-built, O&M manuals
14. **Compliance Matrix** — 38–50 items across all ER categories with badges
15. **RACI Matrix** — 14 roles × 37 activities
16. **Key Personnel** — team profiles with certifications
17. **Risk Register** — detailed table with probability × impact scores

## Visual Requirements
- **SVG charts:** 6 minimum — Integration Workflow, Issue Escalation (3-level), Gantt (36wk), Quality Flow (4-gate), Org Chart (4-tier), Risk Matrix (5×5 heatmap)
- **All charts use Samaya brand colors:** Navy #0F172A, Sky #0284C7, Green #16A34A, Red #B91C1C
- **Badges:** .badge-pass (green), .badge-critical (red), .badge-high (red/amber), .badge-warn (amber), .badge-low (grey)

## Document Study Integration
When project PDFs exist (BoQ, design drawings, material schedules):
- Extract specs using PyMuPDF (fitz)
- Note specific equipment models (QSC Core 510 DSP, LOPU P1.25 LED, Crestron CP4)
- Note material/finish names from design drawings
- Note experience requirements (e.g., "PM with 35 years museum experience")
- Reflect these specifics in proposal sections — generic language is the enemy

## Logo Placement
- Cover top-left: Client logo (RCRC) — downloaded from their website as SVG/PNG
- Cover top-right: Samaya logo (from Docs/Branding/Samaya-Logo.png, base64)
- Cover bottom: Party icons row — 3 only (Client · Designer · Contractor)
- No PMC or CG logos — those are different projects
