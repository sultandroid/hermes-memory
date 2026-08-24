# ZNA 50% Lighting Package QC — Worked Case (2026-08-23)

Session detail backing the `cg-response-protocol` "QC of a specialist's first-issue package" pitfall table.

## The package
- Folder: `02_Submittals/3.5_DD Documents Lighting /260821 %50 Lighting Issue (Lighting Plans)`
- 8 PDFs + 8 DWG transmittal zips: LL + HL x Basement/LGF/GF/1F
- ZNA covering email (Record_RecordID 51275, 2026-08-21): "Below you can find our %50 Stage 4 Draft Lighting plans for all floors" + WeTransfer link → internal hand-off to Eng. Abdullah Omer, NOT a CG submission.

## Errors I made in the QC and corrected
1. Counted the 8 CAD zips as deliverables. They are AutoCAD transmittal packages (`.dwg` + `MOC-ASE-AR-ARC-{FL}-DDD-1200/01/02/03` xrefs + Fonts + LOGO + Stamp.png + PlotCfg). The submittal CG reviews = the PDFs only.
2. Flagged "no lighting elevations" as a 50% blocker. Wrong — the CG-issued `Design Phase Deliverables Tracker 20-08-2026` sheet `Exhibition Lighting Deliverable` defines the 50% package as ONLY the 8 floor plans + a Design Base Report (already Code B). Elevations/LUX calc/legend/control/emergency are later-gate items (forecast 08-30 / 09-01). The user's correction: "this the trukers" (the tracker governs).
3. Flagged "no stamp" from `pdftotext` output. The user corrected: "it have ZNA stamp already". Raster stamps don't appear in text-layer extraction — confirm visually first.
4. The real blockers the user pointed to: **title block** (rev/date not uniform) and **naming convention**.

## The real findings
- **Title block**: LGF-HL = V2, others V0/V1; GF-LL dated 21/01/2025 (stale) vs rest 21/08/2026.
- **Naming**: ZNA used internal `ZNA3297_LG002_{FL}_LL/HL_01`; project expects `MOC-ASE-EL-ELT-*`.
- **Split formal vs technical**: user explicitly said "دي فقط المراجعه الشكلية المراجعه الفنيه الداخليه هاتكون عن طريق المهندس عبد الله عمر" — the formal/document-control review only; technical review handled separately by Eng. Abdullah Omer. State this in the reply.

## Drawing numbering to quote to specialists
Project reference: `MOC-ASE-{Disc}-{System}-{Type}-{Floor}-DDD-{Seq}-{Rev}`
- Disc codes: 1A0 Arch, 1C0 Struct, 1E0 Elec, 1M0 Mech, 1G0 Graphics, 1K0 PM, 1KH HSE, SIC Samaya.
- Lighting (Electrical) from tracker:
  - `MOC-ASE-EL-ELT-DBR-DDD-30001-00` Design Base Report
  - `MOC-ASE-EL-ELT-CALC-DDD-30001-00` LUX calc
  - `MOC-ASE-EL-ELT-GEN-DDD-20001-00` Legend/Notes/Luminaire schedule
  - `MOC-ASE-EL-ELT-GEN-DDD-20002-00` Lighting Control Schematic & LCP schedule
  - `MOC-ASE-EL-ELT-EM-BF-DDD-30007-00` Emergency lighting, Basement
  - Floor plans: `MOC-ASE-EL-ELT-LL-{BF/LGF/GF/1F}-DDD-3000X-00` / `...-HL-...`

## How to read the tracker for a gate check
`Design Phase Deliverables Tracker 20-08-2026 (2).xlsx`, sheet `Exhibition Lighting Deliverable`:
- Column "Gate" (Detailed Design) + "Submission Category" + "Drawing Package / Item" + "Revision" + "Status (Code-A/B/C/D)" + "Preparation/Submitted/Approved %".
- The 50% lighting drawing block = rows for each floor LL/HL; calcs/legend/control/emergency rows carry their own forecast dates (30-Aug / 01-Sep) — they are separate tracked deliverables, NOT part of this plan-issue.
- The overall discipline row in sheet `Design Deliverables Tracker` ("Exhibition Lighting Design, Eng. Abdullah Omer / Eng. Ahmed Ghonim") shows 17 planned / 1 actual at 50%, 35% overall.

## Notes
- ZNA baselines for the lighting plans are the ARCH DDD-1200/01/02/03 GA plans (already Code B in the Arch deliverables sheet). So the arch base is frozen; the naming mismatch is purely the specialist's output numbering.
- Fix path for ZNA: re-title sheets to project references, align Rev + date across the whole issue, keep the (present) stamp, and add a package cover. Then it can go to CG via Aconex, not WeTransfer.
