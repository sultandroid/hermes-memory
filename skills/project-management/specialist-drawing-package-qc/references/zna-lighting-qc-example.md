# Worked example — ZNA 50% Lighting package QC (2026-08-26)

Session detail: QC of `260821 %50 Lighting Issue (Lighting Plans)` from Studio ZNA.

## Package contents (what was actually received)
- 8 PDFs: 4 floors (Basement, LGF, GF, 1F) × 2 drawing types (LL + HL)
- 8 DWG transmittal zips (AutoCAD `- Standard.zip`) = CAD source for the PDFs

**User correction applied here:** the zips are only the CAD files for the PDFs — NOT separate deliverables. QC the PDFs only.

## Title-block findings (real, per-sheet)
| Sheet | Rev | Date | Checker |
|-------|-----|------|---------|
| B_LL_01 / B_HL_01 | V1 | 21/08/2026 | DK |
| GF_LL_01 | V0 | **21/01/2025 (stale, 19 months)** | DK |
| GF_HL_01 | V0 | 21/08/2026 | DK |
| LGF_LL_01 | V0 | 21/01/2025 | DK |
| LGF_HL_01 | **V2** | 21/08/2026 | BN |
| 1F_LL_01 | V0 | 21/01/2025 | DK |
| 1F_HL_01 | V0 | 21/08/2026 | DK |

Mixed revisions (V0/V1/V2) + stale 2025 dates across one package = CG format rejection.

## Drawing-set gap
- Register requires 50% Lighting **Elevations** (L-D-E-001) — NOT delivered. Plans only.
- No cover/transmittal, no QA/QC gate, no NRS review attached.

## CAD XREF baselines (evidence of coordination base)
- Basement: `MOC-ASE-AR-ARC-BF-DDD-1200-01.dwg` (note `-01`, others `-00`)
- LGF: `MOC-ASE-AR-ARC-LGF-DDD-1201-00.dwg`
- GF: `MOC-ASE-AR-ARC-GF-DDD-1202-00.dwg`
- 1F: `MOC-ASE-AR-ARC-1F-DDD-1203-00.dwg`

## Verdict
NOT ready. Fix: project-numbered filenames + cover; align rev/date across all sheets; add elevations; QA/QC sign-off; confirm stamp renders on plots.
