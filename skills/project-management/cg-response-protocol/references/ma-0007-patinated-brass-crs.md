# MA-0007 Patinated Brass — CRS Resubmission Reference

Session-specific detail for the MA-0007 (Patinated Brass by Glasbau Hahn) Code C resubmission. Use with the CRS Creation Workflow in SKILL.md.

## Context
- Submittal: `MOC-MUS-ASE-1A0-MA-0007` — Patinated Brass by Glasbau Hahn
- Status: **Code C** (Revise & Resubmit, CG Mansour Alrezeni, 02-Jul-2026). Confirmed via submission DB (`08_Document_Index/submission.db`), NOT the manual register (superseded 2026-09-05).
- Risk: **PRR-PRC-05** (Critical, score 12) — Oddy failure + finish matching. target_close 2026-09-14.
- CG latest email: 03-Sep-2026 "Kindly update us regarding the Patinated Brass sample" — needs a reply.

## CG's 10 Code C requirements → compliance status
| # | Requirement | Status | Evidence |
|---|-------------|--------|----------|
| 1 | Attach NRS comments + review docs | ✅ Closed | ZD-0033 (Code B), ZD-0060 extracts |
| 2 | Address ALL applications, not only showcases | ✅ Closed | Finishes Schedule 6930 Rev A — 4 items |
| 3 | Manufacturer details | ✅ Closed | Glasbau Hahn (PQ-0063 Code B, single source) |
| 4 | **Oddy test** | ✅ **Closed — PASS** | NonaChem T2607222 (21-Aug-2026), P (Permanent) on Ag/Cu/Pb |
| 5 | Chemical composition | ✅ Closed | KME CuZn37 (C27200) datasheet |
| 6 | MSDS | ⏳ Open → Rev.02 | GBH to issue |
| 7 | VOC test | ⏳ Open → Rev.02 | GBH in progress |
| 8 | Off-gassing | ⏳ Open → Rev.02 | GBH in progress (note: Oddy PASS already covers corrosive emissions) |
| 9 | Fire-rated report | ⏳ Open → Rev.02 | Brass is non-combustible; cert for record only |
| 10 | 2 alternative samples | 🔵 Partial | Option A IGP 591T PARKOUR (submitted); Option B PVD (in dev ~30 days) |

## Approved patinated brass applications (Finishes Schedule 6930 Rev A)
- FI_ME_01: Walls, Main Gallery Doors, Door Reveals, Setworks (Display Units, Display Frames, AV units), Reception Desk
- FI_ME_03: Floorbox Trim
- FI_ST_03: Reception Feature Wall (limestone w/ patinated brass detailing)
- NOTE: FI_GR_11 (Wayfinding Signage) is in `materials.json` but NOT in the approved PDF — do not include.

## CRS template structure (MOC_HQ)
- Sheet "CRS", header rows 2-9, comment rows 11-41 (10 rows available)
- Columns: A=No, B=Initial, C=Sheet, D:H=Reviewer Comment, I:N=Originator Reply, O=Reply By, P:Q=Reply Status by Reviewer
- Column P (Reply Status) is filled by the REVIEWER (CG), not us — we put a provisional Closed/Open.
- Merged cells: D:H and I:N per comment row; header A2:G2, A3:G3, etc.
- Save to OneDrive: `.../Brass_Patinated_Sample_GH/MA-007 Rev01/YYYYMMDD_MA-0007_Rev01_CRS.xlsx`

## Strategy
- The Oddy PASS is the decisive fix — request Rev.01 approval (Code B/A) on its strength; remaining 5 certs follow as Rev.02 addendum.
- Frame the 2 alternatives as supplementary choices (per NRS recommendation + KSA development), NOT substitutions of the specified patinated brass.
- Split-tracks framing: Track A (showcase materials MA-0006 + shop drawings) independent; Track B (brass finish) strengthened by Oddy PASS.
