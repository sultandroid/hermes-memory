# Scope-Expansion Responses on a Specialist SOW (CG Code C)

Pattern for the class of CG comment where the consultant tells the Contractor to widen a **specialist scope** — most often by adding *execution*, or by handing the specialist a package the project has already allocated elsewhere. Worked case: a Landscaping Specialist SOW returned Code C demanding "complete design, coordination **and execution**", plus Landscape Lighting and Museum Signage.

## Step 1 — Establish which document the comment is about, and whose scope it is

Read the SOW that was actually submitted (Designer SOW vs Supplier/Execution SOW are usually two separate documents for the same specialist) and its Document Control block. Note the document number the CG actually responded to — a resubmission should move under **that** number, not the number the draft was originally built with.

## Step 2 — Search the project allocation registers before writing anything

| Register | What it gives you |
|---|---|
| `01_Registers/specification_list.md` (mirror of DMP Rev C04 Project Specification List) | per-spec **Responsible Party** code `DSN-X/S/E/M/T/F/A/V/L/G/B` + `CTR` + `ITCA`, with the SoW clause that mandates it. This is the single strongest citation: find every spec for the disputed package and read its owner column. |
| `00_Contracts/03_Stakeholder_Plan/MOC-MUS-ASE-1K0-PL-0020_Rev04_Stakeholder_Management_Plan.md` | the `T2-NN` tier-2 specialist allocation table (party name per specialist), plus the statement that **NRS is Design Lead / AoR on all design-stage deliverables** including the discipline in question. |
| `00_Contracts/01_DMP/*` and `00_Contracts/…Subcontract_Plan/*` | DMP **§6.13** and Project SoW **§1.4** — specialist sub-contractors operate under the Main Contract with **no privity** to MoC/PMC/CG/NRS. |
| `Technical_Office/Specialist_Management/specialist_register.md` | whether the specialist is appointed, and its PQ code. |

`DSN-L` = Lighting Designer; for Aseer that is Studio ZNA (T2-06, Code B) and its register entry explicitly covers **exhibition lighting and landscape lighting**. Exterior landscape lighting is therefore specced under `DSN-L`, not under the landscaping specialist.

## Step 3 — Split the comment; do not answer it as one block

A scope-expansion comment almost always contains a legitimate part and an illegitimate part. Answer them separately in the same reply:

- **Legitimate** ("reflect the contractual and project requirements", "align with the Kick-off Meeting scope") → **Complied**. Add or strengthen an **Authority Basis** section that names the governing Project SoW clauses, Appendix A Interface Responsibility Matrix, Appendix B package map, ER, DMP, PQP, HSE Plan. Keep it to formal project documents — no negotiation notes, no internal schedule codes.
- **Expansion** (execution, another discipline's package) → **Objection / not applicable at this stage**, evidenced by Steps 2.

## Step 4 — Reply template (plain prose, no headings inside the body)

> The scope is set against the governing contractual framework — Project SoW `<ref>` Section `<x>` and Section `<y>`, Appendix A Interface Responsibility Matrix, and Appendix B package allocation. These reference documents are being restated explicitly in the revised document so the basis is traceable on its face.
>
> On the design and execution point: the document submitted defines the **design** scope for the `<Discipline>` Specialist, and the appointment is still under prequalification. Execution scope will be defined in the corresponding execution document when that package is placed, in line with the programme.
>
> `<Disputed package>` sits with the appointed `<Discipline>` Designer (`<firm>`, `<T2-NN>`), consistent with the project specification register where `<Spec No.>` is assigned to `<DSN-code>`. The Specialist provides `<what it actually gives>` as co-ordination context only.
>
> Under the Main Contract, all specialist packages are engaged by Samaya with no privity to MoC/CG/NRS (DMP Section 6.13, SoW Section 1.4); the engagement structure of those packages remains the Contractor's. We will align the revised document with the governing requirements and resubmit.
>
> *Status: Partially complied — governing basis confirmed and being restated; execution scope and `<disputed package>` are outside the design-scope document. Open.*

Keep it short. State position, evidence, status. Do not restate the CG comment back at them.

## Step 5 — Do not amend the document until the user decides the position

The expansion question (accept design+execution, hold design-only, or a middle position such as design + supervision of execution) changes price, the specialist's qualification basis and the programme. Present the problem and let the other party instruct the change so the cost lands with them — never silently edit the SOW to include execution.

**Once the user's position is settled, assert it — do not write a promise to amend.** The reply says what the document *is*, not what it will be changed into. "The Specialist is engaged as designer, so the scope covers design and coordination only; execution is a separate appointment taken after the design is approved and does not belong in this document." Drafting it as "the execution scope will be defined in the corresponding execution document when that package is placed" reads as a commitment to edit a document that is already correct, and the user will reject it on those grounds.

**Execution wording does not survive into a design-only SOW.** When CG demands "design, coordination **and execution**" and the user holds design-only, the correct edit note is usually **"No change to the scope required"** — grep the document for the word anyway (Rev01 of the Landscaping SOW contained no `execution` term, so CG was pushing an expansion the document did not carry). Conversely, when the user *does* narrow a boundary, every place that states the boundary moves together: the Scope Basis prose, the Included Scope table row, the Deliverables Schedule acceptance criterion, the Exclusions table party, and the RACI rows. Editing one and leaving the others is the defect CG catches next round.

### Per-discipline split outcomes confirmed by the user (Landscape, 2026-08/09)

| Contested item | Confirmed position | Edit to the SOW |
|---|---|---|
| Irrigation — design detail and hydraulic calculations | **Schematic only from the Specialist; detailed design + hydraulic calcs by the MEP Designer** | SOW-03/SOW-04 say *schematic* irrigation; the "100% Final Design (hydraulic calcs, drainage details)" acceptance row moves to AD Eng; RACI splits into *irrigation schematic* (Specialist R / AD Eng C) and *detailed irrigation design + hydraulics + sub-soil drainage* (AD Eng R / Specialist C) |
| Landscape lighting | **Specialist proposes lighting positions and zones; the Lighting Designer (ZNA, T2-06 / `DSN-L`) designs fixtures, conduits, cabling, connections and controls** | Exclusions row rewritten with both halves explicit (positions = Specialist, lighting design = ZNA) — a bare "excluded, ZNA" row understates the Specialist's contribution |
| Interior planter boxes / planting inside the building envelope | separate decision, do not fold into the general scope answer | — |
| Museum / external signage | Graphics discipline (`DSN-G`, spec 32-00-004 / SoW 6.22.4.xv.g); Specialist coordinates signed positions only | new Exclusions row naming the Graphics Specialist |
| O&M manuals | executing contractor at handover, never the designer | Exclusions row + Scope Basis prose |

A boundary stated with both halves ("who does what up to where") is stronger than an exclusion, and it pre-empts the follow-up "but who proposes the locations?".

## Review checklist for the revised SOW

Run these against the actual file before it goes back out:

- **RACI numeric consistency** — every row exactly one `R` and one `A`; a row accidentally left with the other party as `R` silently transfers responsibility. Re-read the irrigation/hydraulics-type rows specifically: when a matrix row is split (e.g. "irrigation design" + "hydraulic calculations"), the split rows are where the `R` gets misplaced.
- **No duplicated scope rows** — copy-paste duplication in the Included Scope table is a CG rejection point.
- **Numbering** — no orphan sub-section heading (e.g. `6.1` appearing immediately after section 5 with section 6 later); renumber sequentially.
- **Document Control block** — doc ref matches the submittal CG responded to, revision, date, and all five CG-required roles (prepared / reviewed / quality / approved / document controller).
- **No internal-only identifiers** on the CG-facing face: internal doc refs in footers, sister-company status, negotiation notes.
- **Stale exclusion clauses** that a CG comment has already asked to remove are still the top rejection trigger — grep the exclusions table *and* the Scope Basis prose, because the same exclusion is usually written in both places.
- **Attachments** — if CG referenced a supporting drawing/plan, confirm it actually arrived; if it did not, request it rather than guessing the boundary.
