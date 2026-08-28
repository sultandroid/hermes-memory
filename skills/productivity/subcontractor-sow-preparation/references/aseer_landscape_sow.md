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

## Submission status (2026-08-28)
SOW built Rev.00 ref `MOC-MUS-ASE-1L0-ZD-0116`, status **For Review** (added to submission reference register). Not yet submitted to CG. Earlier: only a "Landscape & Irrigation Design Package" was submitted 08-Aug (design package, not the SOW); CG sent "Second Reminder – Outstanding Landscape Specialist Submissions" (20-Aug).

## Companion: submission reference register (2026-08-28)
`08_Document_Index/submission_reference_register.md` tracks every submission (ZD/PQ/SNA/MA/NCR/MS/SOW) + CG status, auto-built from an Aconex export via `scripts/build_submission_register.py` (`python3 scripts/build_submission_register.py <export.xlsx>`). Source of truth for "was X submitted?" A daily 17:00 cron reminds to refresh. When a new SOW/submission is issued, add its ref row. **Doc-number conventions:** ZD=Submittal, PQ=Prequalification, SNA=Start New Activity, MA=Material Approval, MS=Method Statement, NC/NCR=Non-Conformance, IR=Inspection Request, SI=Site Instruction, PL=Plan, SOW=Scope of Work. Format `MOC-MUS-ASE-<disp>-<TYPE>-<seq>` (1L0=Landscape). New ZD = highest existing ZD + 1.
