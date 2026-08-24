---
name: samaya-sow-submission
title: Samaya Scope-of-Work / SOW Submission Protocol
description: How to prepare and submit Scope-of-Work / interactive-design / specialist SOW documents for consultant (CG) approval — avoiding the SOW-vs-RFP mix-up, in-place docx editing, and invented sign-offs. Use when the user asks to build, revise, or clean up a Samaya/Sister-Company SOW, scope document, or specialist submission package.
---

# Samaya SOW Submission Protocol

Applies to any Scope-of-Work, interactive-design scope, or specialist SOW destined for **consultant (CG) approval** on Samaya / Aseer / sister-company projects. Distilled from a real Aseer Interactive Design SOW rework (2026-08) where the draft was wrongly built as a tender package.

## 1. SOW is NOT a tender/RFP

When the document is submitted **for approval**, include ONLY the scope. Remove from any source template:
- Prequalification requirements (mandatory experience, PQ submission, ISO/turnover)
- Pricing / BoQ line-items / payment milestones
- Programme milestones (Day-N Gantt, IFC-by-Day-N)
- Quality minutiae (GREENGUARD, Oddy schedule, burn-in) unless specifically requested
- Required Manpower / organogram
- Restrictions (no-privity, maintenance access)
- Obligations (warranty/escrow) — keep only if the submission explicitly needs them
- Critical Interfaces / BOQ & Contractual References / Authority Basis

Those belong in a bid. An approval SOW = scope + exhibit list + per-item scope + open technical questions (if any).

## 2. Edit the original template IN-PLACE (never rebuild)

Building `docx.Document()` from empty strips the brand template (header logo, fonts, table styles, page layout).
- Always open the source: `d = docx.Document(SRC_TEMPLATE)` then modify.
- Use helpers that clear runs and add one run:
  ```python
  def set_para(p, text):
      for r in list(p.runs): r._r.getparent().remove(r._r)
      p.add_run(text)
  def set_cell(cell, text):
      for p in cell.paragraphs:
          for r in list(p.runs): r._r.getparent().remove(r._r)
      cell.paragraphs[0].add_run(text)
  ```
- To insert after a paragraph: build `<w:p>`, `ref._p.addnext(new)`, wrap with `Paragraph(new, ref._parent)`.
- To delete a block: collect body children between two markers and `e.getparent().remove(e)`; for tables use `t._tbl.getparent().remove(t._tbl)`.
- **Logo swap:** header image lives in `section.header.part.rels` with `reltype` containing 'image'. Overwrite `rel.target_part._blob = open(new_logo,'rb').read()` — keeps everything else intact.

## 3. Never invent names / titles / sign-offs

Do NOT auto-fill Approved By / Project Manager from memory. Pull from the project SOW or registers.
- Aseer Regional Museum: PM = **Eng. Waris Sultan**; Samaya TO / Technical Office = **Sultan Issa**; Rawasin engineer = **Eng. Shihab Mohamed**.
- If unknown, leave blank or ask. Inventing (e.g. "Adel Darwish — Projects Director") gets rejected.

## 4. Do not edit the document until the discussion is closed

User rule: *"لا تعدل المستند إلا لما نخلص كل النقاش"* — iterate scope/decisions in chat first; only write to docx after the user confirms the scope is settled.

**This applies to every SOW iteration.** The Aseer Interactive SOW went through ~7 discussion rounds (G9 scope split, manual interactives treatment, G12 exclusion, logo/header, voice, approvals) before the final docx was produced. Writing prematurely wastes rework.

## 5. "Submitted by contractor" vs "prepared by owner" — different voice

- **Contractor/sister submits its own SOW:** Prepared By = engineer name (e.g. Eng. Shihab Mohamed — Rawasin); Reviewed/Approved By = Samaya (Sultan Issa / Waris Sultan); header logo = contractor logo. Voice: "Rawasin submits this Scope of Work…".
- **Samaya submits:** voice is "Samaya defines…"; keep Samaya logo.
- Do not mix — a contractor submission must not read like an owner scope-giver.

## 5a. Aseer Interactive Design SOW — concrete parameters (2026-08 session)

From the Aseer Regional Museum Interactive Design SOW (MOC-MUS-ASE-1KH-SOW-INT-001):

| Parameter | Value |
|-----------|-------|
| **Submitted by** | Rawasin (AV/IT Subcontractor 03, T2-09) |
| **Prepared By** | Eng. Shihab Mohamed — Rawasin |
| **Reviewed By** | Sultan Issa — Samaya Investment (Technical Office Manager) |
| **Approved By** | Eng. Waris Sultan — Samaya Investment (Project Manager) |
| **Header Logo** | Rawasin logo (stored in `_Style-Guides/logos archives/rawasin-logo.jpg`) |
| **Scope covers** | 4 interactives: G4 (04.05_MI_01 Architecture), G5 (05.02_MI_01 Making Space), G8 (08.04_MI_01 Al Qatt), G9 (09.03_HI_01 Sensory Smell) |
| **Excluded** | G12: 12.05_MI_01 Touch + 12.05_MI_02 Rubbing → Replica Subcontractor |
| **NRS RFI (12 items)** | 8 "Rawasin design intent" + 3 "Client input" + 1 "Rawasin design intent" on colour coding |
| **Sections removed** | 4 Prequal, 5 Programme, 7 Quality/Greenguard, 8 Manpower, 9 Restrictions, 10 Obligations, 11 Interfaces, 12 BOQ, 13 Authority |
| **Voice** | "Rawasin submits this Scope of Work…" (contractor voice) |

These are **session-verified facts** — do not reuse blindly; check current project registers before applying.

## 6. Strip internal rationale before consultant submission

Remove: NRS "interactive outside our scope" remarks, "sister company / contract EXECUTED", "Rawasin umbrella" internal notes, "Forward deliverables to CG/NRS (72h DIR cycle)". Keep T2-09 allocation as a neutral line. Present scope only.

## 7. Scope boundary = list every item, mark exclusions minimally

For multi-exhibit scope: list each interactive (ID + gallery + type). Mark replica-based ones as "delivered by Replica Subcontractor, outside this interactive scope" (Aseer example: G12 touch/rubbing excluded from interactive scope). Present proposed materials/activities as **"PROPOSED" + "sample for approval before full fabrication"** rather than open questions — shows competence, leaves an approval gate.

## 8. Logos archive system (Aseer repo)

Logos live in `_Style-Guides/logos archives/` with a `README.md` table (Logo | File | Public URL). When given a new logo (e.g. Rawasin), save it there and add a README row. Source of truth = that folder; upload to `samaya-factory.com/assets/logos/` separately.

## 10. Ready-to-run helper script

`references/docx_inplace_edit.py` — copy into a session for in-place docx editing (set_para / set_cell / add_para_after / delete_between / swap_header_logo). Avoids rebuilding from empty `Document()`.

## 9. Evidence-before-claim (cross-cutting)

User rule: *"ردودك تكون بادله"* — verify against actual sources (Outlook, repo files, Odoo, NRS schedules) before asserting scope facts. The Aseer Interactive SOW was corrected because claims about "all interactives" / "manual interactives excluded" were checked against the NRS Tactile & Manual Interactives Schedule (V2) and Exhibit Schedule (V3) first.
