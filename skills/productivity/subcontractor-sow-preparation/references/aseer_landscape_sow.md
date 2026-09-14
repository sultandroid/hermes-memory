# Aseer Landscape Specialist (TLC) — SOW case notes (updated 2026-08-28)

Worked example for the **Landscaping Specialist** package: candidate negotiation, the canonical SOW location, the final negotiated scope split, the build technique, and the submission-reference-register companion.

## Candidate / procurement status (source: `Technical_Office/Specialist_Management/specialist_register.md`)
- **TLC (The Landscape Company)** — leading candidate, **PQ-0127 Code B** (CG approved w/ comments 23-Jul). `thelandscape.sa`, CR 4030490797, Jeddah/Riyadh.
- Evergreen (PQ-0122) and PINE (PQ-0126) — **Code C** (CG rejected).
- Contract: **not executed** — the SOW signature was the last blocker to appointing the designer.

## Canonical files
- **Repo SOW/RACI draft:** `03_Plans/15_Subcontractor_Deliverables/Draft_SOW_RACI/21_Landscaping_Specialist_SOW_RACI_Draft.md` (Samaya internal tracking).
- **Canonical SOW .docx (FINAL LOCATION — user-corrected 2026-08-28):** `24_Subcontractors/21_Landscaping_Specialist/08 Scope of work/Landscape_Designer_SOW_REV00_MOC-MUS-ASE-1L0-ZD-0116.docx` (OneDrive). **NOT** `03_Scope/TLC_Landscaping/` (repo mirror) and **NOT** the vendor-prequalification subfolder `00_Prequalification/`.
- **Placement rules (user was explicit):** the specialist/designer SOW lives in the **`08 Scope of work` subfolder** of the specialist's `24_Subcontractors/<NN>_<Specialist>/` folder — that subfolder is the "nطاق عمل" home and already holds `Landscape_Designer_SOW.docx` + `Landscape_Supplier_SOW.docx` (designer vs supplier are two separate SOWs). `00_Prequalification/` is vendor evaluation only — never place a SOW there. `03_Scope/TLC_Landscaping/` is a repo mirror, not the source of truth. When placing: back up any legacy file first (`..._LEGACY_pre_REV00.docx`), keep the old file, add the new one beside it with `_REV00_<ref>` in the name — do not overwrite the old SOW.
- **TLC offer mirror:** `03_Scope/Evergreen_Landscaping/TLC_Design_Offer_2026-08-04.md` (SAR 175,000 design-only, offer E 26263-26-3204-001; Rev.2 = 26263-26-3304-001 dated 11-Aug).
- **Submission plan:** `02_Schedule/landscaping_submission_plan.md` (50% concept Critical/overdue; 90% D-85, IFC later).

## Negotiation history (from PM Waris email 27-Aug, Outlook 51841)
| Stage | SAR | Note |
|---|---|---|
| TLC initial | 170,000 | incl. Revit + 3D renders + full CG-approved scope |
| After PM negotiation | 135,000 | |
| PM offer | 120,000 | TLC prepared to accept |
| Ali reduced scope (dropped Revit + 3D) | 120,000 | TLC accepted reduced scope |
| After further negotiation | **130,000** | **10 × 3D renders in PDF, WITHOUT Revit**; PM + Project Director (Adil) agree to finalise at 130,000 excl. VAT |
| Existing TLC offer (04-Aug) | 175,000 | design-only, includes Revit native, excludes 3D renders |

**Blocker:** PM requires the **CG-approved SOW signed by Samaya Technical Office + TLC** before he finalises the contract. (Same gate as ZNA, Trans Orient, AD Eng, SPS.)

## FINAL negotiated scope split (user's decisions, 2026-08-28) — the SOW is built to this
| Item | Owner | Note / verbatim |
|---|---|---|
| **Revit / BIM model updates** | **Samaya = R** (TLC = C) | Samaya maintains its own BIM asset; excluded from TLC fee |
| **3D renders (design-intent)** | **TLC = R**, Samaya = A | 10 × PDF renders owed by TLC |
| **BOQ / cost estimation** | **TLC = R** | "لازم هو اللي يعمل الـ BOQ طبعا اومال مين اللي هايعملها" — the designer prices the quantities |
| **O&M manuals** | **OUT of scope** → executing contractor/supplier | "اللي بينفذ هو اللي بيقدم المانولز" — NOT the designer |
| Structural coordination | **Eng. Ahmed Gad (Samaya)** — internal, not a separate external discipline | "جاد تحت سمايا" |

## Structure decision — the canonical Setwork standard (NOT the old 17-section)
The user flagged the 17-section Landscape SOW is **not the Samaya standard**. The **canonical structure = Setwork Contractor SOW Rev00** (`03_Plans/15_Subcontractor_Deliverables/Draft_SOW_RACI/Setwork_Contractor_SOW_Rev00.docx`): Document Control → Scope Basis → Included Scope → Exclusions & Interfaces → Deliverables Schedule → RACI → Quality/HSE/BIM/Sustain → Submittal Requirements → Commercial Terms. When the SOW is to be (a) CG-approved AND (b) the specialist's contract basis, use this structure + RACI with interfacing-specialty columns.

**Doc-Control block (mandatory — CG requires it on EVERY submitted file):** the FIELD/VALUE table carries Package / Document Ref / Revision / Date / Prepared by / Status / Governing Source / Contract, **plus** Reviewed By / Quality Checked By / Approved By / Document Controller / Distribution (added as extra rows). Names used (2026-08-28): Prepared=Samaya Tech Office, Reviewed=Mohamed Samir (Construction Mgr), Quality=Aftab Adeel (QA/QC Mgr), Approved=Eng. Waris Sultan (PM), DC=Hesham Abdelhamid. Never invent a name — verify from registers/emails first.

**RACI columns = the interfacing SPECIALISTS, named individually.** User: "احنا عندنا mep designer and mep contractor, the designer AD Engineering, and lighting designer ZNA" — do NOT collapse MEP into one column. Columns: **TLC | NRS | AD Engineering (MEP Designer) | MEP Contractor | ZNA (Lighting) | CG/PMC | MoC | Samaya** (Structural folds into Samaya as Ahmed Gad). Samaya = A on most rows; each row exactly one R + one A.

## Build technique (python-docx, template mutation) — learned 2026-08-28
- **Copy the Setwork template to the target path, then `docx.Document()` that copy and edit in place** — never `Document()` from scratch (kills the header logo).
- `fill_table(table, data)`: `while len(table.rows) < len(data): table.add_row()` then set cells. Add Doc-Control block rows the same way with `table.add_row()`.
- Replace body paragraphs by matching `startswith` on the ORIGINAL Setwork lead-in text (e.g. `"This document defines the Scope of Work for the Setwork Contractor"`), clear all runs, write one run. The section HEADINGS (digit-start) stay untouched — do not try to replace them.
- **Pitfall — `set_para` on a heading can silently corrupt it** (replaced headings with body text / duplicated body). Match body lead-ins, never the numbered headings, and re-verify headings afterward.
- **Verify after build:** (a) all 9 numbered headings present, (b) zero leftover "Setwork" in any paragraph or table cell, (c) header logo (`/word/media/image1.png`) still present.
- The .docx is **NOT committed to git** (no-binaries rule; Word lives in OneDrive). Commit only the .md sidecar/registers.

## Reconciliation gotcha — RESOLVED
The old 17-section SOW listed Revit + 3D renders + BOQ + O&M all "INCLUDED in the fixed fee". The rebuilt SOW aligns with the 130,000 split: Revit excluded (Samaya), renders = 10 PDF (TLC), BOQ included (TLC), O&M out of scope (executor). No longer contradicts the offer.

## CG Code C outcome — scope expansion demanded (ZD-0120, Rev 00)
The submitted Landscaping SOW was returned **Code C — Revise & Resubmit** by CG (Landscape Specialist **Ahmed Yehia**, with Mohammed Magdy and Mansour Alrezeni as acting CG PM). CG's nine comment groups ask to:
- widen the scope from **design** to "design, coordination **and execution**" (softscape, hardscape, irrigation, landscape lighting);
- **remove the exclusions the 130,000 fee was built on** — "interior planters and planting inside the building envelope" and the design of irrigation plus associated drainage;
- add **landscape lighting** (fixtures, conduits, cabling, controls) — which sits with **ZNA (lighting designer)**;
- add **museum signage** associated with the site development;
- restate that all landscape works sit under TLC as the specialised subcontractor, with interfaces defined to avoid gaps/overlaps.

Standing position (per the user): CG is **expanding a designer's scope without justification**. The submitted document is a designer SOW — execution belongs to a separate SOW/contract with the executing contractor (the folder holds `Landscape_Designer_SOW` and `Landscape_Supplier_SOW` as two documents for exactly this reason). Present the problem and the cost consequence; do not offer a repriced design-and-build scope.

Internal defects to fix before resubmitting: `SOW-05` and `SOW-06` are duplicated verbatim in the Included Scope table, and the document footer carried the sibling ref `ZD-0119` while the cover read `ZD-0120`.

**File-name vs submitted ref.** The SOW folder holds `..._REV00_MOC-MUS-ASE-1L0-ZD-0116.docx/.pdf` and `..._REV01_MOC-MUS-ASE-1L0-ZD-0116...` copies while the submittal CG actually reviewed is **ZD-0120**. Read the ref from `08_Document_Index/submission.db`, never from the file name.

## STANDING SCOPE DECISIONS (user, 2026-09-14) — apply to every landscape reply

1. **TLC = DESIGNER ONLY; the executing contractor is appointed later, separately.** User: *"النطاق دا للمصمم فقط، المقاول بعدين"*. Never write execution into the designer SOW and never accept wording that puts "design, coordination **and execution**" in it. Execution appears in the Exclusions table as "by others under a separate appointment".
2. **Irrigation = SCHEMATIC ONLY by the Specialist.** User: *"المتخصص بيدينا schematic only and detail design by MEP designer"*. Detailed irrigation design + hydraulic calculations + sub-soil drainage → **AD Engineering (MEP Designer)**, working from the Specialist's schematic. Fixes the Rev01 RACI defect where AD Eng was made R on "hydraulic calcs".
3. **Landscape lighting = Studio ZNA (Lighting Designer).** The Specialist **proposes lighting positions and zones** within the landscape layout (tree/feature uplighting, path and boundary treatment) and coordinates them; ZNA selects the fixtures and designs the conduits, cabling, connections and controls. Evidence: the project spec register assigns "Exterior Electrical and Lighting for Landscape" to **DSN-L** (`13-00-008`, `32-00-003`, from SoW Section 6.22.4.xv.f).
4. **Museum/external signage = Graphics discipline** (`32-00-004`, SoW Section 6.22.4.xv.g) — the Specialist coordinates positions only.
5. **No privity to CG.** Every specialist is engaged by Samaya under Main Contract 0010003521 with no privity to MoC/PMC/CG/NRS (DMP Section 6.13, SoW Section 1.4). The engagement structure of the specialist packages is the Contractor's, not the Consultant's.
6. **T2-13 = Landscape** in the approved Stakeholder Plan Rev04; NRS = Design Lead/AoR on all design-stage deliverables including landscape.

### External pavement / site development = OPTIONAL Item 01 (check before conceding anything)
External planting, paving, signage and lighting around the building sit under **Item 01 — Ground Floor Entrance Enhancement Works** (SAR 5,630,621.37), which is **outside the base contracted scope**: BOQ Sheet 016 marks it "Enhancement works (Not included in Main Package)"; clause **18.00** makes it non-binding ("the Client reserves the absolute right to accept, reject, or proceed… does not constitute a commitment… no claims if not awarded"); revised BOQ sheet 015 heads it "EXTERNAL WORKS & WATERPROOFING OPTION". Base scope = Exhibition Fit Out only (Items 2–14, SAR 56,389,518). Source: `00_Contracts/10_Main_Contract_BOQ/SCOPE_REFERENCE.md`. Rebuttal to anticipate: clauses 1.06 + 3.13 (deemed inclusion) — answer with clause 18.00 being the later, item-specific provision carrying its own separate subtotal.

### Rev01 file + defects still to fix (as of 2026-09-14)
Rev01 (user's own file, MD5 `1f22aa044905c512e6657914944df59a`) sits at `08 Scope of work/MOC-MUS-ASE-1L0-ZD-0116 REV01.docx`. Rev01 already fixed the duplicate SOW-05/SOW-06 row and dropped the stale `ZD-0119` footer ref. Still to fix before resubmission: (a) RACI R05 "hydraulic calcs" wrongly gives AD Eng = R (see decision 2); (b) header still carries Doc Ref `ZD-0116` / date `2026-08-28` — as a CG response it must move to **`MOC-MUS-ASE-1L0-ZD-0120` Rev.01**, the ref CG rejected; (c) the interior-planter exclusion sentence is still in Scope Basis and as an Exclusions row (CG comment G5); (d) no Authority Basis section; (e) numbering runs `5 → 6.1 → 6` and needs sequential renumbering; (f) the firm's name must not appear anywhere while the appointment is unconcluded — write "the Landscaping Specialist" (check coordination/attendee lists and meeting-cadence bullets, where a name hides most easily).

### Planter-box waterproofing + landscape drainage = DESIGNER'S SCOPE (user, 2026-09-14)
User correction: *"عزل البلانتر بوكسس مش الخرسنات يعني دا معماري تبع اللاند سكيب ونفس الموضوع للصرف"*. Distinguish TWO different waterproofing families — do not confuse them:
- **Planter-box waterproofing/lining = architectural, LANDSCAPE scope.** Waterproof membrane + protective lining + drainage layer + geotextile + root barrier INSIDE the planter boxes (terrace `CA.02_SW_01/02`, Stramp, Al Bahar). Belongs to the Landscaping Specialist. Backed by the spec register: `13-00-006` Landscape and Horticulture Special Construction (Landscape/DSN-L) and `32-00-001` Hard Landscaping Specification (Landscape/DSN-L).
- **Structural weatherproofing = NOT landscape.** `07-00-001` Terrace Sunshade Weatherproofing, `07-00-002` Exterior "Stramp" Weatherproofing, `07-00-003` Roof Waterproofing are DSN-S (Structural) from SoW Section 8.2 / 6.22.4.xvi–xvii. Never cite these when the user says "عزل البلانتر بوكسس".
- **Landscape drainage likewise = LANDSCAPE scope**, per spec `13-00-009` "Drainage and Watering for Landscape" (Landscape/DSN-L, SoW Section 6.22.4.xv.e) and deliverable `E-EX-05` Drainage and Watering Schedule. ZD-0120 wrongly moves this to AD Engineering — the spec register contradicts the SOW.
- **Delivery split (user, 2026-09-14):** *"خلي التصميم علي مصمم اللاند سكيب والتنفيذ علي المنفذ"* — DESIGN on the landscape designer (TLC / "the Landscaping Specialist"); EXECUTION on the executing contractor (the separate later appointment). Both planter waterproofing and landscape drainage therefore: **designed by the Specialist, executed by the Landscape Contractor**, written in the Exclusions table as "execution by others under a separate appointment", never as an exclusion of the design itself.
- The ZD-0120 gap this exposes: no planter waterproofing/lining line at all in Included Scope, and the drainage exclusion hands the Specialist's own design deliverable to AD Eng. Both are Resubmission fixes.

### CRS for ZD-0120
Lives beside the submittal at `24_Subcontractors/21_Landscaping_Specialist/08 Scope of work/MOC-MUS-ASE-1L0-ZD-0120ـCRS.xlsx` — note the **Arabic tatweel `ـ`** before `CRS`. Verdicts agreed with the user: **G1** (design+execution, landscape lighting) and **G8** (signage) = Not applicable; **G2/G3** (softscape/hardscape) = Partially Complied; **G4** (irrigation) = Partially Complied; **G6** (lighting) = Partially Complied; **G7** (responsibility) = Partially Complied; **G9** (kick-off / Site Development Plan) = Noted, with CG asked to issue the plan. **G5** (planter boxes / interior planters) RESOLVED 2026-09-14 — verdict **Partially Complied**: the interior-planter exclusion is deleted and the boundary follows the drawing extents; planter-box waterproofing + protective lining + drainage layer + geotextile + root barrier + growing medium + planting + landscape/planter-box drainage are the Specialist's DESIGN; execution is by others under a separate appointment. The prior CRS wording that gave box waterproofing to "MEP and structural designers" was WRONG and has been replaced.

### Rev.01 build + CRS delivered (2026-09-14)
Built by mutating the user's own `MOC-MUS-ASE-1L0-ZD-0116_REV01` docx (from the Outlook attachment store, `Files/S0/2/Attachments/0/`), not the repo draft. Changes: Doc Control Status -> "Resubmission — Issued for Review"; Scope Basis prose carries planter waterproofing/lining + landscape drainage; Included Scope **SOW-10** (planter waterproofing/lining/drainage layer/geotextile/root barrier, source SoW 6.22.4.xv + spec **13-00-006**) and **SOW-11** (landscape drainage & watering, source 6.22.4.xv.e + spec **13-00-009**); Exclusions AD Eng row reworded (incoming supply + building drainage only) + new execution row; RACI rows added for planter waterproofing and landscape drainage (Specialist R / Samaya A), `CG/PMC` double-A rows fixed to I, old "sub-soil drainage" text struck from the AD Eng hydraulic-calcs row; review cycle corrected 7->**14 calendar days** and resubmit 3->**10 working days** (ER 2.4.A).
Pitfall: `clone_row` copies the LAST row, so cloning with an empty ACTIVITY cell inherits "—" — always write the activity label explicitly (use an `add_raci(activity, overrides)` helper). `verify.py`/`inspect.py` as script names are unsafe (stdlib `inspect` name-collision with `lxml.etree` import) — use `check_doc.py`.
CRS: patched **G4, G5, G9** reply cells (column I) in place on the CG-returned workbook, header date `K5` -> 14-Sep-2026. Deliverables placed at OneDrive `.../24_Subcontractors/02_Landscaping/08 Scope of work/MOC-MUS-ASE-1L0-ZD-0120_REV01.docx`. 
**OneDrive pitfall (2026-09-14):** Adel Darwish's synced folder (`Adel  Darwish's files - 01- Execution Documents/...`) returns `fts_read: Resource deadlock avoided` and is **unwritable** — the same path that worked before. The Samaya-side CloudStorage tree, by contrast, accepts writes. Put deliverables under `Samaya/Technical Office/Bim Unit/Aseer-Museum/04_Docs/...`; if the Adel-side path must be populated, the user has to do it.

## Submission status (2026-08-28)
SOW built Rev.00 ref `MOC-MUS-ASE-1L0-ZD-0116`, status **For Review** (added to submission reference register). Not yet submitted to CG. Earlier: only a "Landscape & Irrigation Design Package" was submitted 08-Aug (design package, not the SOW); CG sent "Second Reminder – Outstanding Landscape Specialist Submissions" (20-Aug).

## Companion: submission reference register (2026-08-28)
`08_Document_Index/submission_reference_register.md` tracks every submission (ZD/PQ/SNA/MA/NCR/MS/SOW) + CG status, auto-built from an Aconex export via `scripts/build_submission_register.py` (`python3 scripts/build_submission_register.py <export.xlsx>`). Source of truth for "was X submitted?" A daily 17:00 cron reminds to refresh. When a new SOW/submission is issued, add its ref row. **Doc-number conventions:** ZD=Submittal, PQ=Prequalification, SNA=Start New Activity, MA=Material Approval, MS=Method Statement, NC/NCR=Non-Conformance, IR=Inspection Request, SI=Site Instruction, PL=Plan, SOW=Scope of Work. Format `MOC-MUS-ASE-<disp>-<TYPE>-<seq>` (1L0=Landscape). New ZD = highest existing ZD + 1.
