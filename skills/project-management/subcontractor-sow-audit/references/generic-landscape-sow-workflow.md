# Generic Supplier-Agnostic Specialist SOW — Worked Workflow (Aug 2026)

Case: drafting a Landscape Specialist SOW for the Aseer Regional Museum. Initial draft was
written "for TLC" and copied TLC's quoted exclusions; the user corrected both behaviours and
then reframed the goal as **client protection**, not neutrality.

## User's corrections (verbatim intent, in order)

1. "Dont make the sow for TLC exactly make it generally for any supplier" — supplier-agnostic.
2. "we use the cg comments as requirements for any supplier" — CG reqs as mandatory, not a firm's exclusions.
3. "the goal is to reach a complete document with nothing missing that won't cause future problems or disputes" — complete & dispute-proof.
4. "Dont mention or refer to any internal references like any md file" — no repo paths in client-facing SOW.
5. "أنا عايز أحمي نفسي مش المقاول" ("I want to protect MYSELF, not the contractor") — the SOW must favour Samaya as the client; this OVERRIDES the earlier neutral "IN/OUT choice" framing.

## FINAL client-protective SOW structure (17 sections)

This is the architecture after ALL corrections. It is supplier-agnostic, dispute-proof, AND
client-protective (differs from the earlier draft in bold).

1. **Purpose and Status** — applies to "the Landscape Specialist selected through the
   procurement process"; binding only on signature by both parties; supersedes earlier drafts;
   nothing implied.
2. **Appointment Reference** — prequalification = "Prior CG approval (Code B - approved with
   comments) required before appointment"; firm = "[name to insert]".
3. **Physical Scope and Boundaries** — **defined BY the issued architectural drawings and
   scoping plan referenced in Annex 1, which take precedence over any description**; Specialist
   must confirm in writing that it priced the full Annex scope before signing. Interior planters
   excluded. (User correction: do NOT list assumed areas like "Stramp/Al-Bahar/terrace" from
   memory — use the annexed drawing register to prevent boundary disputes.)
4. **Consultant (CG) Requirements — Mandatory for ANY Supplier** — CG-01..CG-08 (layout,
   planting plans/schedule, irrigation+hydraulic calcs, hardscape coordination, drainage/
   waterproofing, tech specs & material submittals, multi-discipline coordination, specialist's
   own SOW/Understanding/Contact Data). CG comments on PQ/submissions are deemed project
   requirements.
5. **Services Included in Scope** — S-01..S-09 (review, concept, 50% detailed, 90% IFC = Shop
   Drawing Package, coordination, material selection, CG comment responses, CG-08 deliverables,
   presentation visuals).
6. **Included Deliverables (Locked Into the Fixed Fee)** — **table marked INCLUDED, NOT an
   IN/OUT choice**: Revit/BIM native updates; 3D renders; BOQ/cost estimation; O&M manuals.
   "The Specialist has no unilateral right to exclude these; if it contends an item is not
   covered it must state so in writing BEFORE signing; failure to do so gives no additional
   payment." (This is the client-protective override of the earlier IN/OUT rows.)
7. **Data, Access, and Client Responsibilities** — who supplies survey/cloud/geotech/base
   model. **Best-available-data obligation on the Specialist: proceed with available data and
   record assumptions; not suspend work; delay claim valid only after written notice naming the
   datum + reasonable remedy time.** (Kills "no data" stall tactics.)
8. **Interfaces and Coordination** — lighting/structural/irrigation/MEP + hard-soft/external
   interface **per the Annex 1 drawings**. Who owns each.
9. **Submission Plan** — 5 batches (Concept D-55 → Detailed D-85 → Final D-115 → IFC →
   Handover), refs L-D-L-001/002/003, L-IFC-001..004, CG-requirement mapping per batch. Note:
   tracking is generic ("recorded with actual date and CG response code A/B/C/D") — no repo path.
10. **Exclusions** — generic (structural strengthening, lighting/electrical, civil infra,
    authority approvals, construction supervision beyond 90% IFC, interior planters, material
    procurement/testing/mock-ups, anything not expressly included). **Do NOT list ">2 review
    cycles" or "O&M unless IN" as exclusions — those are now IN (Section 6) / unlimited (Section 11).**
11. **Design Review Cycles** — **UNLIMITED within the fixed fee** until CG and Samaya approval;
    no additional payment. (Client-protective: CG rejects often, so capping at 2 lets the
    contractor bill every resubmission.)
12. **Changes and Variations** — any change agreed in writing before work, else no extra
    payment (kills scope-creep).
13. **Compliance, Standards, Sustainability** — ER, codes, climate-suitable planting, evidence.
14. **Fee & Payment** — 10/30/30/30 triggered by **APPROVAL** of PO/Concept/50%/90%-IFC (Shop
    Package); VAT note. (Client-protective: approval-gated, not submission-gated.)
15. **Duration** — 20 working days.
16. **Intellectual Property, Liability, Handover** — **FULL ASSIGNMENT of all deliverables
    (incl. copyright) to Samaya on final payment** + warranty of originality + **indemnity**
    against infringement + delivery in editable native formats. (NOT a "non-exclusive licence" —
    that lets the contractor resell the design.)
17. **Annex 1 — Scoping Drawings** — drawing register (e.g. MOC-ASE-AR-ARC-1F-DDD-1203-00
    Scoping Areas; 2570 series external details; A-62 Site Development Plan; A-01 plans). Note:
    register to be confirmed before execution; post-signature drawing changes = variation under
    Section 12.
18. **Signature & Acceptance** — both parties.

## CRITICAL: summary vs source (Aug 2026 correction)

The repo README (`03_Scope/TLC_Landscaping/README.md`) claimed the TLC offer was **4 weeks /
40-30-30 / 3 stages**. The ACTUAL `Revised_TLC_Landscape_Proposal.docx` (Samaya-authored,
08-Aug-2026, Rev.01) states:
- **Duration: 20 working days** (Concept 5d, 50% 8d, Approvals concurrent, 90% IFC 7d).
- **Payment 10/30/30/30 upon APPROVAL** of PO/Concept/50%/90%-IFC — not 40/30/30 on submission.
- **4 stages, 90% = IFC = Shop Drawing Package.**
- **Revit/BIM explicitly removed** from TLC scope by Samaya in this very offer — so the later
  Revit "dispute" partly traces to Samaya's own drafted offer, not just TLC.
- **Exclusions beyond the README list:** O&M manuals; material procurement/testing/mock-ups;
  shop-drawing prep beyond 90% IFC; blanket "services not expressly included."
- **O&M conflict:** CG's Handover batch requires O&M manuals, but the bid excludes them — a
  signature-blocking contradiction, must be an express INCLIS decision (now locked INTO fee),
  not a silent exclusion.

**Lesson:** ALWAYS read the source .docx/.pdf with python-docx/pdftotext before building the
SOW. A package README is a condensed, sometimes stale summary.

## Physical boundary lesson (Aug 2026)

User: "لو قريت المخططات هتلاقينازعاملينركلاود علي المطاقات" — the drawings define the scope,
so the SOW must say "according to the attached drawings" via an Annex, not an invented list.
The folder actually held `New Scoping Architectural Drawing/1F/MOC-ASE-AR-ARC-1F-DDD-1203-00
Scoping Areas.pdf`, `2570 - External Details/*.pdf`, `A-62 Site Development Plan.pdf`, `A-01
Plan LGF/GF/1F.pdf` — these become the Annex 1 drawing register.

## Generator

`scripts/gen_landscape_sow.py` in `aseer-museum-pm`. Uses `SamayaDoc` imported from the **repo
copy** of the template (`/Users/mohamedessa/aseer-museum-pm/_Style-Guides/Doc Style Guide/`),
NOT the OneDrive path (OneDrive can raise `Resource deadlock avoided` EDEADLK on read).

## Places to file the output

- Repo tracked folder: `03_Scope/TLC_Landscaping/Landscape_Specialist_SOW_DRAFT.docx` (a .docx
  is NOT committed — `.gitignore` no-binaries rule; commit only the generator script).
- OneDrive canonical: `24_Subcontractors/03_Landscaping/` (mirror of the `supported documents 02`
  folder holding the TLC proposal + BOQ).
