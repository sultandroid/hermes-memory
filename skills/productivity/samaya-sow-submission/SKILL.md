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

## 1a. Approve the SCOPE — everything governance lands in a separate submittal

When CG returns a SOW **Code C** with governance/contractual comments (appoint qualified Specialist Exhibition Staff, org structure, CVs, qualifications, demonstrated experience, specialist prequalification), do NOT answer them inside the SOW:

- The SOW is submitted **for scope approval only**; the CRS reply states plainly that the appointment / personnel / prequalification package **will be submitted separately, following approval of this Scope of Work**.
- Add **no** CV, org-chart, qualification or prequalification content to the document. No "see Section 10.0" teaser, no "separate submittal" sentence, no numbering-note cross-reference to the Contractor's SOW — the reply carries the deferral, the document stays scope-only. (User direction; adding the cross-reference was rejected.)
- Same principle for anything the document cannot itself prove: interface/support arrangements are stated as scope (what the party does, response-time commitments), while named individuals, warranty contacts and prequalification certificates are deferred.
- Never name an **uncontracted or candidate** specialist in a CG-facing SOW — write the role title only ("Specialist", "Replica Specialist", "Setworks / Joinery"). Naming a candidate whose prequalification is still Code C invites an immediate second Code C and hands CG a lever.
- Keep a "roles, not names" matrix: list every activity CG asked about as its own row so the matrix itself demonstrates coverage, and let the *discipline* names (AD Engineering, ZNA, Graphit, ITCA) appear where they are already approved/contracted.

## 1b. Responsibility matrix design (when CG asks for one)

CG's standard ask is a matrix "correctly identifying the contractual parties" across design, sensors/controllers, triggering, show-control interfaces, programming, prototyping, fabrication integration, installation, testing and commissioning.

- **One party = one column.** Columns are the contractual parties, and each supporting discipline gets its own column even when it is not a party to our contract (Rawasin AV under T2-09, and any other party CG names by name). Activity text carries the activity only.
- **Do not add a "Specialist / Supplier (named)" column.** A SOW holds roles, not sub-contract awards — the user will reject it, and a named-supplier column contradicts Section 1a. If a supporting party has no column and is not named by CG, fold it into the activity text, not into a new column.
- **Contractor holds A, not R, on every execution row.** The point of the matrix is CG's clause "the Contractor shall retain overall responsibility": Samaya = Contractor with **A** on all execution lines; the design specialist holds R. The Consultant holds A only on the approvals row; the Employer only where the Employer is the doer (content/text).
- **Never write two letters in one cell** (e.g. `R/A`). One role per cell, split the activity into two rows if genuinely both.
- **Row set = CG's list, one row each.** Walk CG's own enumeration (design, sensors/controllers, triggering, show-control interfaces, programming, prototyping, fabrication integration, installation, testing, commissioning) and give each its own row — the matrix demonstrates coverage by its row list.
- **RFI-response rows do not belong in the matrix.** Responses to an NRS RFI are CG / Client / design-lead output, not ours — the design intent sits in the design-development row. Do not create a row that claims we author the RFI responses. Same rule for the SOW's RFI table itself: see Section 11.
- The old matrix is usually left untouched in the "revised" docx (only the Revision number gets bumped). Rebuild the whole table; do not append rows to the existing one.

## 1c. Never present an unverified assertion as a document fact

An exclusion bullet or scope line that asserts a state of the world ("these elements are static, contain no sensors, power or lighting, delivered by joinery") is only as good as its verification. When the instruction includes a confirm-before-issuing caveat, surface the question to the user rather than issuing on assumption: if the assertion is wrong, it becomes a scope gap CG can open later. Same rule for who delivers an item — confirm the delivering party before writing it into an exclusion.

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
- Same rule for third parties: a candidate specialist is never named in the SOW or in the reply until its prequalification is approved — refer to the role (see Section 1a).

## 4. Do not edit the document until the discussion is closed

User rule: *"لا تعدل المستند إلا لما تخلص كل النقاش"* — iterate scope/decisions in chat first; only write to docx after the user confirms the scope is settled.

**This applies to every SOW iteration.** The Aseer Interactive SOW went through ~7 discussion rounds (G9 scope split, manual interactives treatment, G12 exclusion, logo/header, voice, approvals) before the final docx was produced. Writing prematurely wastes rework.

**Corollary — the CRS reply is written comment-by-comment, in chat, and humanized.** Send the drafted reply to the user for approval **before** it goes into the CRS sheet or to CG: natural engineer voice, no template/boilerplate phrasing, no "we confirm compliance". One comment at a time; the user drives the order. Do NOT edit the docx or the CRS while the wording is still under discussion.

**Format the user wants ("give me the humanize replay to copy direct"):** the reply itself as one flowing paragraph of prose — no headings, no bullets, no numbered lists inside it — followed by a clearly separated short note on document status (what the SOW already covers, what still needs adding). When asked to "summarize and humanize", tighten that same paragraph rather than re-structuring it. The reply is only written into the CRS sheet on the user's instruction.

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

## 11. Reviewing a returned revision before it goes back out

When the user hands you the latest Rev (or you are checking whether it is issue-ready), read the docx text and verify against the edit guide / CRS replies point by point — do not assume an applied edit is correct. `references/rev-review-checklist.md` holds the full checklist; the recurring defect classes are:

- **Edit-point coverage** — list every planned edit and mark applied / missing. Partial application is the norm, not the exception: the Revision number and revision-history row usually get applied while the substantive sections do not.
- **Question-to-answer misalignment in response tables** — an RFI/comment table can be shifted by one row so every question carries its neighbour's answer. Read the table as question→answer pairs; a wrong pairing is the single most damaging defect because CG spots it instantly.
- **Cross-version numbers** ("nine (9) items" vs twelve) and stale **issue dates** carried over from the previous revision.
- **Header/control fields** — a Document Ref field holding a revision value, or a revision history restating the superseded date.
- **Numbering collisions** — when CG cites "Section 5.5 of the Contractor's Scope of Works" and our document also has a 5.5, resolve it in the CRS reply, not by bolting a note onto the SOW.
- **Response-table ownership** — check that every row of an RFI/comment table names a responder we are entitled to answer for. Curatorial, visitor-experience and content decisions belong to CG / Client; a table showing us answering them contradicts a scope-only SOW. Flag the rows for reassignment instead of reproducing the old wording.
- **Stale cross-version counts in body text**, not just tables — an intro sentence ("the nine (9) NRS RFI items below") can contradict the table it introduces after rows are added or split. Count the actual rows.

Report the gap list to the user as **missing / errors / fix order** and ask before editing the document.

## 12. Reading the docx without python-docx

`python-docx` may be unavailable in the sandbox interpreter, and a heredoc script can be blocked by the gateway's command filter. Reliable path: write a small reader script to a file with `write_file`, then run it with `terminal`. Parse `word/document.xml` from the zip, converting `</w:p>` → newline, `</w:tc>` → ` | `, `</w:tr>` → newline, then strip tags and unescape — this preserves table cells on one line and gives line numbers you can grep. Keep it as a reusable script rather than retyping the regexes each session.

`scripts/read_docx_text.py` is that script — run it as `python3 scripts/read_docx_text.py <docx> > /tmp/doc.txt`, then grep the output for the section headings you are reviewing.
