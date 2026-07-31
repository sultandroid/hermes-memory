# BIM Coordination — Top Lessons

> **Curated wisdom** extracted from the 8 cases built on 31 July 2026. Read first; jump to `cases/INDEX.md` for the per-case detail.

## From Cases 001 + 003 (ISO 19650 + Saudi National BIM Strategy) — The Standard

1. **ISO 19650 is the global BIM standard, and the Saudi National BIM Strategy (2024) explicitly mandates it for Vision 2030 mega-projects.**
   **Operational rule:** your BEP must reference ISO 19650 explicitly; your CDE workflow must follow ISO 19650-2; your information requirements must follow ISO 19650-4 (EIR) and ISO 19650-5 (AIR).

2. **The Saudi BIM market is $1.3T over the Vision 2030 horizon (BIM Design LLC 2026).**
   Compliance with the National BIM Strategy is a *commercial gate* on Vision 2030 projects. Non-compliance is increasingly a *contractual* defect, not just a technical one.

## From Case 002 (Mehrbod et al. ITcon 2019) — Coordination Issue Taxonomy

3. **BIM coordination issues fall into four categories: design, workflow, technology, and management.**
   The "clash detection" view of BIM coordination is only the *design* category. The bigger drivers of BIM failure are *workflow* (no BEP), *technology* (CDE not set up), and *management* (no BIM coordinator with authority).

4. **Soft clashes (clearance, accessibility, maintenance) are more costly to fix in construction than hard clashes (geometry).**
   BIM clash detection focused only on hard geometry misses the more expensive coordination failures. **Operational rule:** your BIM coordination review must explicitly check for soft clashes.

## From Case 004 (Abdelalim et al. MDPI 2024) — BEP Framework

5. **A standard BEP framework has 12 sections: project info, goals, BIM uses, roles, process, CDE, technology, QA, milestones, delivery strategy, risk, and capability assessment.**
   **Operational rule:** if your BEP is missing more than 2 of these sections, it will be rejected by the Employer's BIM team.

## From Case 005 (BIM Forum LOD Specification 2024) — LOD

6. **LOD 100-500 is a progression, not a binary state.**
   LOD 200 is *generic* geometry with approximate quantities. LOD 350 is *specific* geometry with connections, supports, and clearances. LOD 500 is *as-built* verified geometry. The "LOD" you can demand at each stage is a contract decision, not a BIM decision.

7. **The single most-disputed LOD boundary is LOD 300 vs LOD 350.**
   LOD 300 = accurate geometry, no connections. LOD 350 = accurate geometry + connections. The connection information is what enables fabrication and coordination. **Drafting consequence:** always specify LOD 350 as the construction-stage target, not LOD 300.

## From Case 006 (12d Synergy CDE Guide) — ISO 19650-2 Workflow

8. **The ISO 19650-2 CDE workflow has 6 states: Work In Progress (WIP), Shared, Published, Archived, and the 3 review states (Review, Information Model Authorisation, Information Model Acceptance).**
   **Operational rule:** every BIM deliverable must transition through all 6 states. Skipping states (e.g. publishing without Authorisation) is a *contractual* defect.

## From Case 007 (BIM Design LLC — Digital Twin) — Handover

9. **Most digital twins die at commissioning because the AIM (Asset Information Model) is never built.**
   The AIM is the transition from PIM (Project Information Model) to operational reality. Without a structured AIM handover (data drops, asset registers, O&M manuals in digital form), the digital twin is a model, not a system.

10. **AIM handover requires: (a) structured data drops at the right stages, (b) the AIM information requirements (AIR) in the contract from day one, (c) the COBie or equivalent data standard, (d) client capability to receive.**
    Missing any of these four → digital twin dies at handover.

## From Case 008 (Iqbal PLOS 2025) — Adoption Drivers in KSA

11. **The top 3 BIM adoption drivers in KSA: (a) client mandate (Vision 2030), (b) contractor capability gap (still huge), (c) regulatory uncertainty (no single mandated standard yet).**
    **Operational rule:** if you are a contractor, your BIM capability is a *commercial differentiator* on Vision 2030 mega-projects. If you are a client, your BIM mandate must be specific (which standard, which LOD, which CDE) or your contractors will deliver inconsistent results.

## Cross-cutting

12. **BIM is a *project management* discipline, not a *technology* discipline.**
    The BIM coordinator needs authority (project-level, not CAD-team level), a budget, a mandate, and a seat at the design coordination meeting. Without these, BIM becomes a parallel documentation effort, not a coordination tool.

## How to use this file

- Read before any BIM decision
- Search here first when facing a BEP review, clash dispute, LOD argument, or handover question
- If a lesson contradicts what you're about to do, STOP and re-read the source case

## Cross-references

- `../vocabulary.md` (cross-topic)
- `../READING_GUIDE.md`
- All cases: `cases/INDEX.md`
- Related topics: `../design-management/`, `../construction-management/`, `../codes-standards/`
