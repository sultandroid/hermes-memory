# Aseer Interactive SOW — Worked Example (2026-08-23)

## Source inputs
- `MOC-MUS-ASE-1KH-SOW-INT-001_Interactive_Design_Scope.docx` (original — G9 only, RFP-style).
- NRS `A2742-6.04-018` RFI (01-Jun-2026): 12 open technical questions, all on G9 scent interactive.
- NRS Tactile & Manual Interactives Schedule V2 + Exhibit Schedule V3.

## Scope decision (6 → 4)
Original SOW covered only ET_09.03 (G9). The schedules define SIX interactives:
- 04.05_MI_01 Architecture (G4) — Manual
- 05.02_MI_01 Making Space (G5) — Manual
- 08.04_MI_01 Al Qatt (G8) — Manual
- 09.03_HI_01 Sensory Smell (G9) — Hybrid/Electromechanical ← ONLY truly electronic one
- 12.05_MI_01 Archaeology Touch (G12) — Tactile
- 12.05_MI_02 Archaeology Rubbing (G12) — Manual

**Decision: G12 (touch + rubbing) EXCLUDED — replica-based, delivered by Replica Subcontractor.** Only 4 interactives in scope (G4/G5/G8/G9). User: *"نعم نترك g12 للرابليكا"*.

## NRS 12-RFI classification (G9) — confirmed 9+3=12
- **9 = Samaya/Rawasin design intent (addressed)**: idle state, image breakdown 3/pot, attract+answer sequence, multi-user mapping, lid-left-open timeout, pot↔wall sync, interpretive text duration, colour temp per lid, colour coding, trigger delay (covered by programming).
- **3 = CLIENT INPUT**: image/content per pot (curatorial), interpretive text/translation (content), scent mechanism (dispenser vs passive sniffing — visitor experience).
- **Count consistency**: the matrix has 9 addressed + 3 client = 12 rows. Any prose summary (Sections 3.4 / 6.0) MUST say **nine (9) addressed + three (3) = 12** — never 8, which undercounts the table and is an easy CG rejection point. (The original Rev03 prose wrongly said "eight (8)".)

## Material handling (no guessing)
User rejected assuming materials. Rule: PROPOSE (local-building-inspired: stone/earth/wood tones; authentic Al Qatt colours red/black/white+accents) with **"sample for approval before fabrication"** gate. Never assert a material.

## Submission party
File submitted BY Rawasin → phrasing "Rawasin submits…", "Rawasin shall…", obligations 10.1 = RAWASIN, 10.2 = SAMAYA (CLIENT/EMPLOYER). Header logo MUST be Rawasin's, not Samaya's. (No Rawasin logo found in repo/style-guide — needs user to provide; fallback = text "Rawasin" in header.)

## Internal items stripped for CG submission
- Section 4 Prequalification (whole).
- "NRS confirmed… outside their scope" + "sister company, contract EXECUTED".
- "Forward deliverables to CG/NRS (72h DIR cycle)".
- Authority basis: "T2-09 interactives under Rawasin umbrella" → "T2-09 interactives allocation".

## python-docx mutation recipe (preserve format/logo)
- Load source .docx, edit in place. Do NOT `docx.Document()` from scratch.
- `find_para(prefix)` loops paragraphs, matches `text.strip().startswith(prefix)`.
- `set_para(p, text)`: clear runs, add one run.
- `set_cell(cell, text)`: clear cell paragraphs' runs, add run.
- Remove section: collect paragraphs between two marker paras, `p._p.getparent().remove(p._p)`.
- Header image survives automatically (media/image1.png in header part).
- **Swap header logo** (when submitter changes): locate the header image relationship and overwrite its blob:
  ```python
  for sec in d.sections:
      hdr = sec.header
      for rel in hdr.part.rels.values():
          if 'image' in rel.reltype:
              with open(NEW_LOGO_PATH,'rb') as f: blob = f.read()
              rel.target_part._blob = blob   # in-place overwrite, keeps relationship
              break
  ```
  This keeps the `media/image1.png` relationship intact — only the bytes change. Verify after save by comparing blob size to the source logo.

## Logo storage convention (repo)
- New logos go to `_Style-Guides/logos archives/<name>.<ext>` and a row is added to that folder's `README.md` table (`| Logo | File | Public URL |`) with the public URL `https://samaya-factory.com/assets/logos/<name>`.
- Rawasin logo added as `rawasin-logo.jpg` this session (1043×396, from a user-supplied image).
- Source of truth for logos = that folder; upload to samaya-factory.com only after committing to repo.

## Document Control — correct parties (Aseer, 2026-08-24)
- **Prepared By** = Rawasin (Samaya sister company — AV/IT Subcontractor 03).
- **Reviewed By** = Sultan Issa — Samaya Investment (Technical Office Manager).
- **Approved By** = **Eng. Waris Sultan — Samaya Investment (Project Manager)**. NOT Adel Darwish, NOT "Projects Director". Verify approver against SOW/deliverables before writing; never invent a name/title.

## Rev03 state + structure verdict (2026-08-24)
- Rev03 doc (this is the version the user reviewed) = 4 interactives (G4/G5/G8/G9), sections 1.0 Purpose → 6.0 NRS RFI, plus 2 tables (ET_09 exhibit list; 12-item NRS RFI matrix).
- **Section numbering gap**: jumps 3.4 → 6.0 (missing 4.0 Deliverables, 5.0 Exclusions).
- **RFI count mismatch**: prose in 3.4/6.0 said "eight (8) addressed + three (3)" = 11, but the 12-row matrix shows **9 addressed + 3 client** = 12. Must fix prose to nine (9).
- **Revision**: Doc Control said "00" but file is Rev03 → match.
- **Structure verdict**: this is a **Technical Design Brief**, not a contract SOW. User's stated purpose = "اعتماد نطاق فني ليكون أساس عقد مقاول" (approve technical scope as the basis of the contractor contract). To block undiscovered extra works it still needs: Exclusions, Changes & Variations, Interfaces & Coordination, Deliverables, Signature. (Full 17-section client-protective inventory: `subcontractor-sow-audit` → `references/generic-landscape-sow-workflow.md`.)
- **Keep the NRS RFI matrix** in this submission — for a "prove understanding to CG" goal it is evidence of competence, not a gap. Only the 3 CLIENT INPUT items (content per pot, text/translation, scent mechanism) are genuinely open and could be surfaced as TBC/exclusions.

## FINAL structure decision (2026-08-24) — standard SOW, NO commercial terms
- Submitted **BY Rawasin** for CG scope approval (satisfies CG double-gate: specialist's own SOW + understanding + contact data). Purpose = "اعتماد نطاق فني ليكون أساس عقد مقاول" (approve technical scope as contract basis) + prevent undiscovered additional works + same channel with owner/consultant.
- **Must match SOW siblings** (`03_Plans/15_Subcontractor_Deliverables/subcontractor_sow_raci_template.md` + the sibling package drafts), NOT be a bare technical brief. **Commercial terms (fee/duration/IP) stay in the Rawasin contract — do NOT put them in this CG-facing SOW.**
- **APPLIED (final 9-section structure, built into the Rev03 .docx 2026-08-24):**
  1. 1.0 Purpose (1.1 Background · 1.2 Exhibit ID)
  2. 2.0 Exhibit Context
  3. 3.0 Scope of Work (3.1–3.4)
  4. 4.0 **Exclusions**
  5. 5.0 **Interfaces & Coordination** (5.1 Design & Approval · 5.2 Physical Fabrication & Mounting · 5.3 Content & Graphics · 5.4 Internal Coordination within Rawasin · 5.5 Handover & Operation)
  6. 6.0 **Responsibility Matrix (RACI)** — user asked "هل حطيت RACI matrix?" → include one
  7. 7.0 **Deliverables** (7.1 Design docs · 7.2 Physical samples · 7.3 Fabrication/programming · 7.4 Install & commissioning · 7.5 Handover)
  8. 8.0 **Standards & Compliance**
  9. 9.0 NRS RFI — Open Technical Questions (renumbered from 6.0)
- Also fixed in the applied .docx: Revision 00→03, RFI count eight→nine, RACI table 11 rows (header + 10 activities).
- Repo `03_Scope/Interactive_Design/README.md` updated 2026-08-24 from "CLOSED/folded into Rawasin" → "ACTIVE — INT-001 Rev03 submitted by Rawasin" (commit b64f645).

## Oddy does NOT apply museum-wide (2026-08-24 correction)
- In the Project SOW, Oddy is tied to **"any non pre-approved material recommended by the Contractor"** (SOW Section 8.11) in the third-party inspection list — i.e. materials near **artifacts/archaeological pieces**, NOT every gallery.
- The interactives (G4/G5/G8/G9) are public hands-on exhibits; even G9 uses REPLICAS, not original artifacts. So do NOT impose an Oddy obligation on the interactive specialist's SOW — it would add liability the Project SOW does not actually require.
- Substitute **practical museum best practice** for durability instead: materials selected for **child safety, durability under heavy public use, cleanability/ease of maintenance, and moisture resistance**.
- Standards section phrasing: defer to the governing doc — "shall comply with the standards and codes set out in the Project Scope of Work" — then list the specific confirmed obligations (safety per SOW Section 8.11, ITCA-certified prototype testing per ER Section 2.6, accessibility, electrical standards for G9). Don't enumerate codes the user hasn't confirmed.

## RACI responsibility matrix in the CG-facing SOW (2026-08-24)
- The user expects the specialist SOW to carry a **RACI responsibility matrix** (asked "هل حطيت RACI matrix?" and approved it). Use the **simplified** per-activity matrix (specialist=R, Samaya=A, CG/PMC, NRS, and named firms in "Others"), NOT the internal full Samaya RACI drafts under `03_Plans/15_Subcontractor_Deliverables/Draft_SOW_RACI/`.
- Applied rows: design dev / physical samples / fabrication & integration / install & commissioning / O&M+TOC handover all = specialist **R**, Samaya **A**; and the delivered-by-others rows (electrical→AD Eng, plinths→Setworks, graphics→Graphit, replicas→Replica Specialist, content→MoC) = specialist **I**, Samaya **A**, firm **R**. Key legend: R=Responsible · A=Accountable · C=Consulted · I=Informed.

## python-docx insertion recipe used (2026-08-24)
- To insert new numbered sections + a table at a mid-document point: locate the existing section header paragraph (e.g. the "6.0 NRS RFI" one) as the insertion anchor, then `target.insert_paragraph_before(...)` for each new heading/bullet/body paragraph, in order 4.0→8.0; finally renumber the old "6.0" header to "9.0" by editing its run text.
- Headings = Normal style, Calibri bold 14pt; sub-headings (5.1/7.1) = bold, size None; body bullets = `List Bullet` style; body paragraphs = Normal + JUSTIFY.
- Add a table after a specific paragraph with `key_p._p.addnext(new_tbl._tbl)` (python-docx `add_table` appends at end-of-doc; move the `_tbl` element to the right anchor). Delete trailing empty rows by removing `_tr` for rows whose concatenated cell text is empty. Header-row shading via `w:shd` fill (e.g. D9D9D9) on each header cell's `tcPr`.


## AV is INTERNAL to Rawasin — NOT an exclusion (2026-08-24 correction)
- User: "كله مع رواسن لكن رواسن نفسها هايكون داخليها اكثر من متخصص" — everything (AV/IT, show-control, interactive) is ONE Rawasin package; internally Rawasin has multiple specialist departments.
- So do NOT list AV/show-control as an exclusion (would contradict "all within Rawasin"). Mention it as **internal coordination within Rawasin** (hand-off of sensors, lighting, scent, show-control programming) — one light line, not a full section.
- Only genuinely EXTERNAL parties are exclusions/interfaces: Replica Subcontractor (crowns/herbs), Client MoC (graphic content/text), ZNA (gallery lighting design), Structural (mounts/supports).

## AD (MEP) interface — electrical power (2026-08-24 addition)
- Interactives need electrical supply (esp. G9 electromechanical: sensors, LEDs, scent, microcontrollers; lit wall panels). Add **AD Engineering (MEP Designer)** to Interfaces.
- Define the power boundary explicitly to prevent later disputes: **MEP supplies power+containment TO A DEFINED CONNECTION POINT** at each interactive location; Interactive Design supplies point loads/connection requirements and makes ALL downstream connections to the interactive hardware. ("MEP → point, Rawasin → rest".)

## Dimensional interface map — CONFIRMED answers (2026-08-24)
The Interfaces section is built by dimension (see SKILL.md section), with the user confirming these boundary owners (do not re-guess these):
- **Physical furniture (plinths/tables/wall boards) = Setworks / Joinery** fabricates; Interactive Design supplies+integrates systems onto them + provides the G9 replica mounting platform. (This is the single biggest extra-works door — must be stated.)
- **Wayfinding/instruction/pattern-guide graphics = Graphics Contractor** produces (for the 3 manual interactives G4/G5/G8); **Client (MoC)** supplies the TEXT/translation (ApxA 2.12, 3.01–3.05). Split: text=MoC, production=Graphics.
- **G9 scent = yes, coordinate with HVAC (MEP)** — not self-contained; add HVAC coordination to the AD/MEP interface line.
- **Handover = Client / Operator** receives it; Interactive Design delivers O&M + training + TOC.
- **NRS = Design Lead** (design intent + governing schedules V2/V3 + reviews development + raised the 12 RFIs). It is an interface, NOT a deliverer — place under a "Design & Approval" sub-heading, not under "delivered by others".
- **Main Contractor / Fit-Out** prepares final surfaces/substrates (walls, floors) at interactive locations.
- **Structural** — supports/mounts where plinth or wall-board loads are imposed.
- Also present: **Internal coordination within Rawasin** (4.4) and **Handover & Operation to Client/Operator** (4.5).

## Study-deep, don't yes-man (2026-08-24)
User rejected shallow agreement: *"لا انا مش هاعقود اقولك وانت تقولي صح ادرس الموضوع بعمق شويه"*. When drafting boundaries, don't just re-affirm the user's suggestion — go deeper into dimensions (design/approval, fabrication, content, internal, handover) and ask the hard "who supplies what / who takes over where" questions. The four that matter after approval: who fabricates the physical furniture, who produces the manual interactives' graphics, whether scent needs HVAC, and who receives handover.
