---
name: subcontractor-sow-preparation
description: Author/draft a Scope of Work (SOW) or specialist scope document for a subcontractor/specialist (Rawasin AV/IT, Replicas, Setworks, etc.) to submit to the Consultant (CG) for approval on Aseer Museum / Samaya projects. Covers scope-boundary discussion, consultant-submission hygiene, and submitting-party phrasing. Inverse of subcontractor-sow-audit (which reviews, not authors).
---

# Subcontractor SOW Preparation

## Trigger
Use when the user asks to create, draft, revise, or package a **Scope of Work / specialist scope document** for a subcontractor or specialist to submit to the Consultant (CG) for approval — e.g. Rawasin (AV/IT, sister company), Replicas, Setworks, Interactive Design. Also when the chat is about "what should this SOW say", scope boundaries between specialists, or "make it ready to send to the consultant".

## When NOT to use
- Reviewing/auditing an existing SOW for gaps → `subcontractor-sow-audit`.
- Pure Samaya-branded formal letters/reports → `samaya-docx-template`.

## Workflow (ORDER MATTERS)
1. **Discuss scope FIRST, edit the .docx LAST.** Never write/edit the deliverable document until every scope point is settled in chat. The user explicitly corrected this: *"لا تعدل المستند الا لما نخلص كل النقاش"*. Build the file only after the full Q&A closes (all items get "تمام").
2. **Update the repo scope README BEFORE generating the file.** When `03_Scope/<name>/README.md` exists, refresh it first (doc ref, Rev, submission party, structure under discussion, scope table) and commit it, then continue discussing. User: *"حدث النطاق على الريبو قبل توليد الملف"*. Also flip stale states — e.g. the Interactive README said "CLOSED / folded into Rawasin, no separate SOW" and needed to become ACTIVE with the new INT-001 doc ref. Commit message carries the date (YYYY-MM-DD) per repo rule.
2. **Mutate the ORIGINAL template, never rebuild from scratch.** python-docx recreating a Document() from zero **destroys the header logo, fonts, and table styling**. Instead load the source .docx and edit in place:
   - `find_para(startswith)` → locate by leading text, then `set_para(p, text)` (clear runs, add one run).
   - `set_cell(cell, text)` for table cells.
   - Remove a whole section by collecting paragraphs between two marker paragraphs and `remove_para` each.
   - Preserve the header image (`media/image1.png`) — do NOT swap/delete unless the submitting party changes.
3. **Strip internal rationale for consultant submission.** Remove: prequalification sections, "sister company / contract EXECUTED" status, "NRS confirmed X is outside their scope" explanations, "Forward deliverables to CG/NRS (72h DIR cycle)" internal procedures. The consultant only needs scope + design intent + open questions.
4. **Submitting party = phrasing owner + logo.**
   - If the **subcontractor submits** (e.g. Rawasin): "Rawasin submits this Scope of Work…", "Rawasin shall design/engineer…", obligations = "RAWASIN (Interactive Design Specialist)" as obligor and "SAMAYA (CLIENT/EMPLOYER)" as the other party. **Swap the header logo to the submitting party's logo** — do NOT leave Samaya's logo on a Rawasin-submitted doc.
   - If **Samaya submits as owner**: "Samaya defines the scope…".
5. **Propose, don't leave blank.** For open design questions, state Samaya/Rawasin **design intent (proposal)** and mark items needing Client input as **"CLIENT INPUT"**. Never present a bare "?". Show understanding: e.g. material proposals framed as "PROPOSED: … sample for approval before fabrication".
6. **State scope boundaries explicitly.** Physical replicas, models, glass, joinery, setworks are OTHER subcontractors' scope. The specialist **integrates/mounts only**. Call out exclusions clearly (e.g. tactile/rubbing interactives = Replica Subcontractor, outside interactive scope).

## Two SOW use-cases — establish the goal BEFORE judging structure (2026-08-24)
A specialist SOW can serve either (or both) of two purposes, and the correct structure depends on which:
- **(a) Technical scope approval** — submitted to CG to prove the specialist *understands* the scope (e.g. "اعتماد نطاق فني"). Emphasis: exhibit identification, per-exhibit design intent, PROPOSED + sample-for-approval gates.
- **(b) Basis of a subcontractor contract** — the approved scope that prevents *undiscovered extra works* later ("حتى لا يظهر أي أعمال إضافية غير مكتشفة"). Emphasis: contract-protective sections.

When the user asks "is this structure complete?", ASK or establish the goal first. A pure technical brief (like the Interactive SOW: Purpose/Context/Scope/RFI) is structurally a **"Technical Design Brief," NOT a contract SOW** — it's missing the sections that actually block scope-creep: **Exclusions, Changes & Variations, Interfaces & Coordination, Deliverables, Signature/Acceptance**. When the user says the SOW will be "الأساس لعقد مقاول" (basis of a contractor contract), it must carry those sections even if CG only sees the technical part. Reference the full 17-section client-protective inventory in `subcontractor-sow-audit` → `references/generic-landscape-sow-workflow.md`.

## Keep the RFI matrix in the SOW when the goal is proving understanding
Do NOT strip the NRS/consultant open-question table from a SOW whose goal is CG approval of the technical scope. The RFI-response matrix (each question answered as "design intent" + the Client-input ones separated) is the **concrete evidence of understanding** — it demonstrates competence better than any prose. It is a strength, not a gap, when the submission exists to win CG confidence. (Contrast: in an RFP/tender the same matrix would be noise — context matters.)

## Interfaces & Coordination — build DIMENSIONALLY, not as a flat list (2026-08-24)
When drafting the Interfaces section, do NOT dump a flat list of parties. The user rejected yes-man agreement with: *"لا انا مش هاعقود اقولك وانت تقولي صح ادرس الموضوع بعمق شويه"* — study the interfaces deeply and ask the hard boundary questions. Build the section by DIMENSION, and for each interface state **who delivers what + who takes over from where** (the boundary is where scope-creep claims start):

| Dimension | Parties to consider | Hard boundary question |
|---|---|---|
| Design & approval | NRS (Design Lead), CG/PMC | Who owns design intent? Who approves each stage? |
| Physical fabrication & mounting | Setworks/Joinery, Main/Fit-Out (surface prep), Structural, MEP/AD, Replica sub | **Who fabricates the physical furniture (plinth/table/wall-board)?** This is the single biggest extra-works door |
| Content & graphics | MoC (text), Graphics contractor (production) | Who writes text vs who produces graphics? (ApxA 2.12: exhibition/interactives TEXT = MoC; graphics production = Graphics contractor) |
| Internal (within the submitting umbrella) | AV/IT, show-control, install | Is there a within-company hand-off to show? |
| Handover & operation | Client/Operator | Who receives handover, who is trained on operation? |

Key boundary insights (Interactive case):
- **Within-umbrella coordination ≠ exclusion.** If the specialist is inside a company that also does AV (Rawasin), the AV/show-control/install hand-off is an INTERNAL interface, NOT an exclusion. Present it as "internal coordination (within Rawasin)", not as "AV hardware excluded".
- **Don't forget AD/MEP** — electrical supply to a defined connection point per interactive location + **HVAC coordination for the G9 scent dispersion**. Boundary: MEP supplies to the connection point; specialist makes all downstream connections.
- **MEP boundary must be written** (MEP → point, specialist → downstream) or it becomes a "who runs the last cable" dispute.
- **Surface/substrate prep** — who finishes the wall/floor at interactive locations (Main/Fit-Out).
- **Ask the user, don't guess**, on: who fabricates the physical furniture, who produces the manual interactives' instruction graphics, whether scent needs HVAC, and who takes handover. These four are the ones that bite after approval.

## Responsibility (RACI) matrix in a consultant-facing SOW (2026-08-24)
The user expects a **RACI responsibility matrix** in the specialist SOW — when asked "هل حطيت RACI matrix?" the answer should be yes. But use a **simplified responsibility matrix**, NOT the internal Samaya RACI with full Samaya/Sub/PMC/MoC columns (those internal RACI drafts live under `03_Plans/15_Subcontractor_Deliverables/Draft_SOW_RACI/` and are for Samaya's own tracking, not CG submission). Build a compact per-activity table: activity × [specialist = R] × [Samaya = A] × [CG/PMC = C/I] × [NRS = C/I] × [others = R with the firm named]. Rows cover: design development, physical samples, fabrication/integration, then the delivered-by-others rows (electrical supply → AD Eng, plinths/tables → Setworks, graphics → Graphit, replicas → Replica Specialist, content → MoC) as `I / A / I / I / <firm> (R)`. End with the key legend "R = Responsible · A = Accountable · C = Consulted · I = Informed". This reinforces the Exclusions and Interfaces and shows CG who owns what — extra protection against later "not my scope" claims.

## Materials/standards — don't over-commit the specialist (2026-08-24)
- **Oddy testing does NOT apply museum-wide.** In the Project SOW it is tied to **"any non pre-approved material recommended by the Contractor"** in the context of third-party inspections near **artifacts/archaeological pieces** (SOW Section 8.11 / third-party inspection list) — NOT every material in every gallery. If the specialist's interactives sit in public/display zones with no original artifacts nearby (interactive materials are for hands-on use; even the electromechanical one uses REPLICAS, not originals), do NOT impose an Oddy obligation on the specialist's SOW — that adds a liability the Project SOW does not actually require. The user corrected this explicitly: *\"الاودي قالك فالاماكن الي فيها قطع اثريه مش كل المتحف صح؟\"* (Oddy applies where artifacts are, not the whole museum).
- **Substitute best museum practice instead of Oddy** where the real requirement is durability/use, not artifact conservation: materials selected for **child safety, durability under heavy public use, cleanability/ease of maintenance, and moisture resistance**. This is the practical, correct compliance framing for interactive exhibits. When the user says "best museum practice", propose these concrete criteria rather than reaching for artifact-conservation standards.
- **Standards compliance section should defer to the Project SOW, not re-invent codes.** Frame as "shall comply with the standards and codes set out in the Project Scope of Work", then list the specific obligations (safety per SOW Section 8.11, ITCA-certified prototype testing per ER Section 2.6, accessibility, electrical standards for the electromechanical one). Don't enumerate codes the user hasn't confirmed apply — reference the governing document instead.

## Internal-consistency checks before submitting (concrete, from the Interactive SOW)
- **RFI count mismatch**: prose said "eight (8) addressed + three (3) = 11" but the matrix had 9 addressed + 3 = 12. Make the prose count match the table count — a count inconsistency is an easy CG rejection point.
- **Section numbering gap**: section jumped 3.4 → 6.0 (missing 4.0/5.0). Either renumber sequentially or insert the missing sections (e.g. Deliverables, Exclusions).
- **Revision field**: Doc Control "Revision 00" must match the file's Rev number (e.g. Rev03).

## Pitfalls (from real corrections)
- **Editing mid-discussion** → user rejection + rework. Wait for "تمام" on all items.
- **Agreeing instead of studying** → the user rejects shallow yes-man responses: *"لا انا مش هاعقود اقولك وانت تقولي صح ادرس الموضوع بعمق شويه"*. When the user pushes back, go DEEPER on the actual subject (dimensions, boundaries, who-supplies-what), don't just re-affirm or reword. Ask the hard boundary questions rather than listing parties.
- **Rebuilding the docx from zero** → lost logo/format. Always mutate the source file.
- **Leaving "sister company / contract EXECUTED" in a CG submission** → leaks internal procurement status. Strip it.
- **Guessing materials** → propose instead. User: *"انت ماتقدرش تتوقع… ممكن تكون المواد ايه"* — propose (local-building-inspired, sample-approval gate), never assert.
- **Over-scoping electronics**: only the sensory/scent interactive is truly electromechanical; manual/tactile ones are hands-on physical. Don't assign sensors/programming where none exist.
- **Mismatched logo**: file submitted by Rawasin but header still shows Samaya logo → wrong. Match logo to submitter.
- **Fabricating approver names**: NEVER invent a person/role for Document Control. User rejected "Adel Darwish — Projects Director" because the actual PM is **Eng. Waris Sultan** (per the project SOW/deliverables). Verify the approver from repo sources before writing it; if unknown, ask the user. *"مدير المشروع ليس عادل — دا وارث انت بتنسي ليه"*.
- **Title precision**: use the real job title — "Project Manager" (مدير المشروع), NOT "Projects Director" (مدير المشاريع). The user corrects this distinction explicitly.
- **Doc-Control split**: when a subcontractor submits, use **Prepared By = subcontractor**, **Reviewed By = Samaya TO Manager (Sultan Issa)**, **Approved By = Samaya Project Manager (Eng. Waris Sultan)**. Samaya reviews/approves; it does not "prepare".
- **Named vs generic specialist references**: appointed specialists → name them (AD Engineering, Studio ZNA, NRS, and a confirmed graphics firm like Graphit); unappointed → generic "X Specialist" with no name. Verify appointment status in `03_Scope/<name>/README.md` BEFORE writing a name. The user expects known appointed firms to be named and unappointed ones left generic — don't leave an appointed firm off, and don't name one that isn't confirmed.
- **Safety certification comes from a THIRD PARTY (ITCA), not the specialist** — ER Section 2.6.B: the Independent Testing & Commissioning Agent must NOT be the contractor/subsidiary. So a specialist SOW must phrase it as **"prototype safety testing and submission of test records to the ITCA for certification"** (per ER Section 2.6, SOW Section 8.11), NEVER "safety certification" as if the specialist issues the certificate.
- **Use "Section", not the § symbol** — Samaya documents avoid the § symbol; write "Section 2.6" not "§2.6".
- **Only the electromechanical interactive has programming** — G9 (Sensory Smell) is the only electromechanical/hybrid interactive (sensors, DALI/DMX, scent, show-control); the manual ones (building blocks, making space, Al Qatt) are physical with NO show-control/source-code. Scope show-control programming deliverables to the electromechanical one only.
- **Logo storage**: store any new logo in the repo's `_Style-Guides/logos archives/` folder AND add a row to its `README.md` table (File + Public URL `samaya-factory.com/assets/logos/<name>`), then reference that path when swapping the header. Don't drop a logo file ad hoc.

## Authority Basis / references section — verify EVERY ref against the source (2026-08-24)
When the user supplies (or asks you to add) an \"Authority Basis\" / governing-references section, treat it as a **source-traceability check, not a paste**. The user flagged a proposed reference block and every wrong ref is a CG rejection point. Rules learned:
- **Verify each section number against the ACTUAL source doc** before writing it. The user's proposed block had fatal errors that a repo check exposed: ER §3.10 = Structural Modifications (NOT AV/IT), SoW §6.4 = Monthly Reporting and Tracking (NOT AV), SoW §6.6 = Review and Approvals (NOT finishes). The interactives genuinely live in **SoW §8.11 (Mechanical and Electromechanical Interactives)** and ER §2.4/2.6. Run `rg -in \"8\\.11|3\\.10|6\\.4\"` on the charter docs before asserting any section number.
- **Don't cite a claim you can't source.** \"NRS Appendix A — interactive design outside NRS scope\" and \"NRS A2742-1721/1722\" had no repo trace. The user corrected the former: NRS being the Design Lead with a specialist per discipline is **normal and already covered by the DMP** — it needs NO explicit scope-exclusion citation. If a reference has no source in the repo/email/CDE, either find it or drop it; never assert an unverifiable authority.
- **Scope the references to what's actually governing the specialist package**: Main Contract/ER clauses that bind it, the Project SOW section for that discipline, DMP sections (Vendor & Procurement, Interface Management), the design-lead schedules, the RFI, the T2/stakeholder allocation, and the approved design drawings. Keep it tight.

## Drawing references: cite the numbers in the specialist's `02_Reference_Drawings` folder, NOT your guessed migration (2026-08-24)
The user's correction here is CRITICAL and reversed an earlier assumption. When citing the design drawings in a specialist SOW, DO NOT try to migrate the legacy NRS numbers to new DDD numbers on your own. The **authoritative drawing numbers for the specialist package are the files in its own `02_Reference_Drawings` folder** under `90_Legacy_Source_Bank/06_Procurement/General/<NN>_<Specialist>/02_Reference_Drawings/`. For the Interactive Design contractor that folder holds:
- `A2742-1721A_Floral_Crown_Smell_Table_Sheet1.pdf`
- `A2742-1722A_Floral_Crown_Smell_Table_Sheet2.pdf`
- `A2742-6.04-018_NRS_RFI_Interactive.pdf`

So the SOW's reference list must cite **`A2742-1721A / A2742-1722A`** (the original NRS numbers with the "A" revision suffix) — NOT the `MOC-ASE-AR-ARC-GEN-DDD-2721-00/2722-00` numbers I earlier proposed by cross-referencing the NRS register against the DD Gate submittal PDFs. Both sets describe the same drawings (Floral Crown 'Smell' Table, G9, `09.03_HI_01`, 3 smell jars + vitrines + 9 lightboxes, depth 650→800mm), but the numbers in `02_Reference_Drawings` are what the contractor actually works to. When the user says "all the reference numbers are in 02_Reference_Drawings", go THERE first — it is the source of truth for citation, not a drawing register you re-derive. Distinguish: the DD-Gate DDD numbers are the NRS *production* drawing numbers; the A2xxxA numbers are the *reference-package* numbers given to the subcontractor. Cite the one the package actually received.

**The RFI number likewise comes from the specialist's own folders.** When the user says "RFIs are here 06_RFIs", the authoritative RFI is in `24_Subcontractors/<NN>_<Specialist>/06_RFIs/` (and mirrored in `02_Reference_Drawings`). For the Interactive package that is **`A2742-6.04-018`** — the 4-page NRS RFI "Floral Crown and Smell Pots Interactive · G9" containing the 12 open items. Do not hunt for an alternate RFI number across the repo/register when the package folder already holds the exact file; the `06_RFIs` subfolder (even if the Legacy-bank copies are empty) plus `02_Reference_Drawings` are the canonical citation sources. Also note the RFI matrix in the SOW's own table is separate from the cited RFI number — the matrix rows restate its 12 items, the Authority Basis cites the number.

## Final SOW section order (Interactive case, 2026-08-24)
A specialist SOW submitted by Rawasin for CG approval settles on this 10-section sequence — use as the canonical ordering and renumber sequentially (no gaps):
1.0 Purpose (Background, Exhibit ID) → 2.0 Exhibit Context → 3.0 Scope of Work (3.1–3.4 per exhibit) → 4.0 Exclusions → 5.0 Interfaces & Coordination → 6.0 Responsibility Matrix (RACI) → 7.0 Deliverables → 8.0 Standards & Compliance → 9.0 NRS RFI — Open Technical Questions → **10.0 Authority Basis** (final, after the RFI). The Authority Basis is the closing section that anchors traceability; the internal cross-reference "Section 9" (the RFI) must stay correct after renumbering. When the user sees a number in a proposed ref block and asks "why 13.0?" — if it has no basis in the current document structure, default to the actual section count of the doc (here 10) rather than inventing a higher number.

## Self-review as the Consultant (CG) before submit (2026-08-24)
Before delivering a specialist SOW, review it as the CG would — \"راجعه كانك الـ cg\". The user explicitly asked for this and it surfaced real pre-submission defects. Concrete checklist that catches them:
- **\"sister company\" / internal procurement status in a consultant-facing SOW** → strip it (it weakens the independent-certification position). Doc Control \"Prepared By\" should be \"<firm> (Interactive Design Specialist)\", not \"(Samaya sister company…)\".
- **\"PROPOSED\" reads as non-binding** to a CG approving a contractual scope → rephrase to **\"Design intent (subject to sample approval)\"** — commits the intent while keeping the approval gate.
- **Within-umbrella AV/show-control needs an explicit boundary line in Exclusions**, not just the Interfaces section: \"Show-control and AV hardware — provided by Rawasin (AV) under T2-09; Interactive Design coordinates the interface and hand-off only, and does not supply or install AV equipment.\"
- **Open client-input items need a closing line**: \"Items 10–12 remain OPEN pending Client decision; their impact on scope, programme, and cost will be captured through the agreed change mechanism.\" — so an approved SOW doesn't silently imply resolved items.
- **Submission/sample PROGRAMME table by DAYS, not calendar dates** — the user wants programme stages keyed to the Master Submittal Register gate days (e.g. G2 50% DD=D35, G3 90% DD=D65, G4 IFC=D82, G5 AFC=D88, handover=D300), never hardcoded calendar dates that go stale. Build a table: Submittal × Stage × Day × Content × Approval Authority. Pull the day numbers from `_MANAGER_DASHBOARD/Master_Submittal_Register.xlsx`, not invented.

## File placement & edit-in-place (2026-08-24)
- **Edit the existing file in place; do NOT create a fresh Desktop copy on every revision.** The user's explicit rule: \"المستند حطه في مكانه ومش كل مره تعمل نسخه جديده صلح الموجوده او امسحها\" — place the deliverable at its canonical location and fix that copy (or delete stale ones); do not litter new copies.
- **Consolidate to ONE canonical version across ALL of OneDrive.** When the user says \"احذف كله خلي آخر نسخة بس\" (delete everything, keep only the latest version), they want a SINGLE surviving copy. `find "$BASE" -iname "*SOW-INT-001*" -not -path "*00_Scope_of_Work*"` and delete every stale copy (correspondence archives, Design Files, 04_Docs images, legacy procurement folders), keeping only the one in the canonical `00_Scope_of_Work/`. The user confirmed this explicitly before deletion — it overrides the usual OneDrive caution. **Critical gotcha:** paths contain spaces (\"Technical Office\", \"Bim Unit\") — `for f in $DEL; do rm ...` WILL break (splits on spaces, tries to delete phantom \"Technical\"/\"Bim\" entries). Use `while IFS= read -r f; do rm -f \"$f\"; done` to preserve quoting.
- Canonical location for Aseer specialist SOWs: `OneDrive-SAMAYAINVESTMENT/Samaya/Technical Office/Bim Unit/Aseer-Museum/24_Subcontractors/<NN>_<Specialist>/00_Scope_of_Work/` — the user asked for a dedicated **`00_Scope_of_Work`** folder per package so the scope is obvious to everyone (mirrors the existing Lighting `00_Scope_of_Work_from_04` pattern). After a final build, copy there, verify it opens (python-docx paragraph/table count), and delete temp Desktop/cache copies. The repo does not track the .docx (no-binaries) — OneDrive is source of truth.
- **Doc-Control face hygiene** — the user stripped from the client-facing header table: **Project number (3092), Contract number (0010003521), T2 allocation (T2-09), Classification (\"Confidential\"), and the Prepared-By firm suffix** (kept just \"Eng. Shihab Mohamed\"). Keep the contract number ONLY inside the Authority Basis section as a governing reference, not in the face. This is consistent with the earlier sister-company strip — remove internal identifiers that leak procurement/commercial status from anything CG will see.

## DC handoff message after SOW is finalised (2026-08-24)
Once the SOW is final and placed at its canonical `00_Scope_of_Work/` path, the user may ask for a **draft message to the Document Controller (DC, e.g. Hesham Abdelhamid) to submit the doc to CG**. This is a distinct small deliverable — draft it as a submission-cover message, not more document editing. Structure:
- **Subject**: "Submission for Approval — <doc ref> <title> (Rev X)"
- **To**: DC by name (verified from repo/team list, not invented).
- **Body**: document ref + title + Rev; submission party (e.g. "From: Rawasin (Interactive Design Specialist)"); distribution; the transmittal body's key scope summary (what it covers + exclusions); requested action ("review and approve, or advise required revisions — Code B/C/D").
- **Close**: ask DC to confirm once submitted on Aconex with the transmittal reference number.
- Before finalising, confirm with the user: (1) is it a Teams/email draft vs a formal cover letter for the Aconex submission, (2) distribution list (CG only vs also MoC), (3) the correct CG approver/PM name (verify from repo — do not guess), (4) bilingual EN+AR or EN-only. Flag these four as open confirmations rather than assuming.

## References
- `references/aseer_interactive_sow.md` — worked example: 6→4 interactive scope, G12 exclusion, NRS 12-RFI classification (9 design intent + 3 client input), Rawasin submission phrasing.
