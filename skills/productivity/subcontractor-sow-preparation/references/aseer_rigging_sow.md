# Rigging Contractor SOW — package specifics (Aseer Museum)

Package ref: `MOC-ASEER-SIC-1K0-SC-0008`. Governing source: Project SOW `6380_KMS_RPT_PM_AS_00006` Rev 00 (03/03/2025).

## Canonical locations
- **Formal issued DOCX (Rev C01)** — byte-identical copies (MD5 `1bd5abd6…`) across three spots on the Micro volume:
  - `24_Subcontractors/06_Rigging/01_Scope_of_Work/48993_Rigging_Contractor_SOW_RACI_C01.docx` (newest mtime)
  - `24_Subcontractors/10_Rigging/01_Scope_of_Work/Rigging_Contractor_SOW_RACI_C01.docx`
  - `24_Subcontractors/10_Rigging/01_Prequalification/Rigging_Contractor_SOW_RACI_C01.docx`
- **Current working draft (newest content, 2026-08-24)** — repo MD, incorporates CG comments:
  `aseer-museum-pm/03_Plans/15_Subcontractor_Deliverables/Draft_SOW_RACI/06_Rigging_Contractor_SOW_Discussion_Draft.md`
  (bilingual AR/EN; sections 1–11 + PMBOK Compliance as §12). This is the basis for the next Rev.
- Older RACI-only draft: `…/06_Rigging_Contractor_SOW_RACI_Draft.md` (last_updated 2026-07-14, 89 lines).
- Email archive: `Desktop/Work_Projects/Aseer-emails-md-only-2026-05-22/Subcontractors/14_Rigging_Contractor/` (empty subfolders + `SCOPE_REQUEST.md`).

## Build scripts (stale — do not run as-is)
`_Style-Guides/Doc Style Guide/build_rigging_sow_final.py` and `build_rigging_sow_cg.py` both save to a hardcoded
`C:\Users\user\aseer-museum-pm\...\06_Rigging_Contractor_SOW_RACI_Rev01.docx` Windows path. They were never run on this Mac.
To produce the next Rev DOCX, fix the `out` path to the canonical `00_Scope_of_Work/` location first.

## Key scope facts (from the Discussion Draft)
- Rigging is **sequenced, not parallel**: gates = (1) MoC final Object List (weights + Hung/Floor) → (2) approved structural BOD → (3) Rigging Schedule Rev.0 + Suspension-Point Register → (4) pull-out tests/install after structural SCIR → (5) final load tests + certs at TOC − 30 days.
- Heavy loads: G11 Scriptst stone ~180kg+; Qasr Abu Melha / OB227-1 (G12) 2.5–3.0 t (~3200×1500mm) = heaviest; hundreds of suspension points across 14 galleries + LB1–LB3; ceiling-hung models; projectors (G3/CL.1/G4); lighting gantries.
- **Deliverables**: Suspension-Point Register (tied to structural approval, per DDR-STR-003), BIM LOD 300 design / LOD 500 as-built, Method Statement + Lifting Plan + Risk Assessment, pull-out tests + load certificates, as-built + O&M + handover training.
- **Inspection standard**: Static + proof-load per piece (SBC/project QA); NO dynamic testing unless specifically ordered (rejects CG's rejected "dynamic test per artwork" comment).
- **Exclusions/interfaces**: mounts fabrication = MoC (ApxA 2.14); art handling/install = MoC; structural verification = structural consultant (5.6); AV equipment = AV/IT contractor; catwalks = basebuild (access point only); showcases = Glasbau Hahn.
- **Certification schedule**: load calcs/details by rigger pre-fabrication; pull-out tests by rigger + independent witness; static+proof-load by rigger at install; final structural cert by structural consultant (5.6); as-built+O&M by rigger at handover.
- **HSE**: work-at-height (HSE-03), Lifting Operation Plan (PL-0046), critical lift plan + load chart + sling-angle protection.
- **Prequalification status**: PQ-0130 Code D, PQ-0131/0132 Code C — root cause "SOW not defined in detail". Plan: submit detailed scope (separate from pricing) → complete company file (Rigging Specialist CV + SCE/GOSI, 5-yr KSA exhibit-rigging experience, org chart) → single specialist → re-submit targeting Code B.
- **Open decisions**: SRC-003 (certification ordering) and SRC-004 (mounts interface) — proposed in draft, need PM decision; heritage structural engineer unappointed (offer only from Abdelmohaymen Farag); BOD blocked (Code C).
