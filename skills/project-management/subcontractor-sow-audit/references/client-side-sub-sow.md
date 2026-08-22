# Client-Side (Samaya-Protective) Subcontractor SOW Generation

Worked lessons from the Aug 2026 Landscape SOW task. When Samaya (the CLIENT) asks you to
draft a subcontractor/specialist SOW, the document is a **contract that protects Samaya** —
NOT a neutral/fair agreement, and NOT a mirror of the subcontractor's own offer.

## The core correction (user-verbatim)
> "ياعم وأنا ليه أحكم على نفسي، أنا عايز أحمي نفسي مش المقاول"
> (Why am I judging myself neutrally? I want to protect MYSELF, not the contractor.)

> "الهدف ليس المطابقة، الهدف الوصول لوثيقة متكاملة لا ينقصها شيء ولا تسبب مشاكل أو نزاعات مستقبلاً"
> — Goal is NOT matching the subcontractor's offer; it's a COMPLETE, dispute-proof doc.

An assistant writing a "fair" SOW (balanced deliverables, contractor-choice clauses, IP
license not assignment, "contractor not liable for late data") is producing a document that
works AGAINST the client. Every such clause must be flipped to favour Samay.

## Drafting rules (encode these into every client SOW)

1. **Delivery lock-in, not choice.** Ambiguous deliverables (Revit/BIM model, 3D renders,
   BOQ/cost estimation, O&M manuals) are written "INCLUDED in the fixed fee", not "IN SCOPE /
   OUT OF SCOPE — contractor selects". The contractor has no unilateral right to exclude them;
   if it contends one is unpriced it must say so IN WRITING before signing, else no extra pay.

2. **Payment on APPROVAL + unlimited review cycles.** The client's consultant rejects often
   (Code C/D), so "up to two review cycles then extra fee" bleeds the client dry. Write:
   payment triggered by approval of each milestone, and an UNLIMITED number of review rounds
   / resubmissions included until CG/Samaya approval. No variation fee for getting approved.
   (Trade-off: "unlimited + approval-gated" is strong legally but un-bankable commercially —
   a smart bidder refuses or inflates. Balance it: cap rounds at ~3 then written variation.)

3. **Full IP ASSIGNMENT, not license.** Irrevocable transfer of full ownership (drawings,
   models, specs, copyright) to Samaya on each deliverable delivered+paid. Contractor shall
   not reuse/resell/license to third parties. Add indemnity against infringement + fit-for-purpose
   warranty + deliver editable native files at close.

4. **Include risk-closing commercial clauses** a client SOW must carry:
   - Termination (for convenience + for material breach; pay only accepted work; IP transfers on termination)
   - Liquidated damages for unexcused delay (rate fixed BEFORE signing, not "to be stated later")
   - Governing law = KSA + good-faith negotiation then Saudi courts
   - Confidentiality clause (separate from IP)
   - Retention / security vs late-detected design defects

5. **Boundaries by the actual drawings, not an invented list.** Never write area/zone lists
   (Stramp, Al Bahar, terrace) from memory — the contractor will dispute wrong boundaries.
   Reference "BY THE ISSUED ARCHITECTURAL DRAWINGS AND SCOPING PLAN REFERENCED IN ANNEX 1",
   list the actual drawing numbers in Annex 1, and add: the contractor confirms in writing it
   priced the full scope within N working days, else deemed to have accepted it.

6. **Realistic current dates from the project tracker**, never a hypothetical baseline plan.
   The user: "review the project tracker to know the timing, we are already late". Pull
   TODAY'S status (00_Status/project_status.md, master_programme.md) before fixing milestone
   dates. Stale/past dates make the LD clause unenforceable and the contract unexecutable.

7. **Contract-facing language — no internal references.** A contract facing a third party must
   NOT contain repo paths, `.md` files, tracker paths, or the git repo name. Keep only
   contract/doc numbers. Requirement list headings read "Design and Submission Requirements",
   not "Consultant (CG) Requirements" — the contractor is bound to the project requirements;
   CG is merely the reviewer. (Acceptance codes like "CG Code A/B" are external/real, keep them.)

## Commercial reality check (the case study)
The TLC Landscape case: the subcontractor's own offer EXCLUDED Revit. Samaya's contract then
INCLUDED it. Waris (PM) demanded "clear SOW signed by both" while TLC refused over the Revit
split. Writing a fully client-protective SOW (Revit INCLUDED in a fixed 175k fee) is
contractually sound but may break the deal with a bidder whose price assumed exclusion. When
that conflict appears, surface it to the user rather than silently choosing:
- Option 1: Revit OUT of fee (matches the bidder's offer, they'll sign)
- Option 2: Revit as an option at a pre-agreed rate (protects client, keeps deal alive)
- Option 3: Revit INCLUDED (client-strongest, but bidder likely refuses)
The user decides which trade-off; the agent should not unilaterally break a live contract on
either side.

## Tooling notes
- DOCX output: use the `samaya_doc_template` SamayaDoc class (navy/gold Samaya brand). If the
  OneDrive path deadlocks (`Resource deadlock avoided`), import the template from the repo copy:
  `~/aseer-museum-pm/_Style-Guides/Doc Style Guide/samaya_doc_template.py`.
- `add_table` takes `col_widths_cm=`, not `widths_cm`.
- `add_body(..., align=...)` takes a `WD_ALIGN_PARAGRAPH` enum, not the string "center".
- OneDrive deadlock: quit OneDrive, wait 30-60s, retry; or read via `textutil -convert txt`/
  `python-docx` after the lock clears. Accessibles files occasionally appear once OneDrive re-syncs.
