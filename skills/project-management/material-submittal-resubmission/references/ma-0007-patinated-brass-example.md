# MA-0007 Patinated Brass — Worked Example (2026-09)

Concrete reference for the material-submittal-resubmission workflow, from the Aseer Museum MA-0007 (Patinated Brass by Glasbau Hahn) case.

## Submission identity
- **Doc No.:** MOC-MUS-ASE-1A0-MA-0007
- **Title:** Patinated Brass
- **Rev.00 status:** Code C — Revise and Resubmit (CG Mansour Alrezeni, 02-Jul-2026)
- **Supplier:** Glasbau Hahn GmbH (PQ-0063 Code B, single global source)
- **Sample code (internal, deprecated):** SAM-FIN-PB-001 → renamed to MA-0007

## CG's Code C requirements → compliance status

| # | CG requirement | Status | Evidence |
|---|----------------|--------|----------|
| 1 | Attach NRS comments + review docs | COMPLIED | ZD-0033 (Code B), ZD-0060 extracts |
| 2 | Address ALL applications, not just showcases | COMPLIED | Finishes Schedule 6930 Rev A (4 items) |
| 3 | Manufacturer details | COMPLIED | Glasbau Hahn profile, PQ-0063 |
| 4 | Oddy test | COMPLIED (PASS) | NonaChem T2607222, 21-Aug-26, P/Permanent on Ag/Cu/Pb |
| 5 | Chemical composition | COMPLIED | KME CuZn37 (C27200) datasheet |
| 6 | MSDS | PENDING (Rev.02) | GBH to issue |
| 7 | VOC test | PENDING (Rev.02) | GBH / accredited lab |
| 8 | Off-gassing test | PENDING (Rev.02) | GBH; note Oddy already confirms no corrosive emissions |
| 9 | Fire-rated report | PENDING (Rev.02) | brass is non-combustible — challenge |
| 10 | 2 alternative samples | PARTIAL | A: IGP 591T PARKOUR powder coat (ready); B: PVD (in dev ~30 days) |

## Approved applications (from Finishes Schedule 6930 Rev A PDF)
FI_ME_01: Walls, Main Gallery Doors, Door Reveals, Setworks (Display Units, Display Frames, AV Units), Reception Desk
FI_ME_03: Floorbox Trim
FI_ST_03: Reception Feature Wall (limestone w/ brass detailing)
FI_GR_11: Wayfinding Signage (2mm patinated brass, CNC cut) — **present in PDF but MISSING from materials.json** — always cross-check the PDF.

## CRS fill pattern (openpyxl)
Load the MOC_HQ template, write header + comment rows, save to `MA-007 Rev01/` OneDrive folder:
```python
import openpyxl
wb = openpyxl.load_workbook(SRC)  # CRS_Template_MOC_HQ.xlsx
ws = wb["CRS"]
# header block
ws["D4"]="Regional Museum (Aseer)"; ws["I4"]="MOC-MUS-ASE-1A0-MA-0007"
ws["D5"]="CRS-MA-0007-Rev01"; ws["K5"]="08-Sep-2026"
ws["D6"]="MOC-MUS-ASE-1A0-MA-0007"; ws["K6"]="Architectural"
ws["D7"]="Patinated Brass — Material Submittal (by Glasbau Hahn)"; ws["K7"]="Material Submittal"
# comment rows 11+ : A=No, B=Initial, C=Sheet, D=Comment, I=Reply, O=ReplyBy, P=Status
wb.save(OUT)
```

## Oddy test report (NonaChem T2607222) — key facts
- Test report T2607222, NonaChem GmbH (Ladenburg, Germany), on behalf of Glasbau Hahn
- Sample: Patinated Brass, double determination (1-1, 1-2), 18 coupons tested
- Method: Oddy per DIN EN 60068-2-2:2008-05, 60°C / 28 days / ~100% RH
- Result: **P (Permanent)** on Silver (sulphur), Copper (chlorides/oxides), Lead (organic acids) — blank value clean
- Tested 22-Jul → 21-Aug-2026, report dated 21/08/2026
- This PASS is the decisive lever to flip MA-0007 from Code C to B/A.

## Risk register linkage
- PRR-PRC-05 (Critical, score 12): "Patinated brass Oddy failure + finish matching risk"
- A passed Oddy test lowers probability → update score, actions A1–A4, target close (was 2026-09-14).
- Risk closure rule: Code B = practical final approval (PM decision 2026-08-18); only Code C/D keep a risk open.
