# Specialist Drawing-Package QC — Formal vs Technical Review Split

Applies when a design specialist (ZNA lighting, Rawasin AV, etc.) issues a drawing package at a stage gate and the user asks you to QC it.

## The split — never merge the two streams

| Stream | Owner | Goes to specialist? | Content |
|--------|-------|--------------------|---------|
| Formal / document-control | Samaya (Technical Office) | Yes | Title block, drawing numbering/naming convention, rev/date consistency, stamp rendering, cover/transmittal |
| Internal technical review | Discipline lead (e.g. Eng. Abdullah Omer for MEP/electrical) | No — internal only | Design content, calculations, coordination |

State the split explicitly in the reply email: "This covers formal / document-control only. The internal technical review of the design will be carried out separately by [discipline lead]."

## 4 standard formal findings on specialist packages
1. Wrong title block — specialist uses its own; project requires the approved Aseer Museum specialist title block (template `18_Invoices/Docs/Title Block Data/Title block.dwg`, supplied by the user).
2. Wrong naming convention — specialist uses internal numbers (e.g. `ZNA2607_LG002_*`); must use the project convention (see below).
3. Revision/date inconsistency — one sheet V2, rest V0/V1, a stale prior-year date. All sheets in one issue must match.
4. Stamp rendering — confirm the stamp renders on plotted PDFs (CADs carry `Stamp.png` but it may not print). Verify visually / with the user; do NOT assume it is missing from pdftotext extraction alone.

## Check the Design Phase Deliverables Tracker BEFORE flagging "missing" deliverables
The tracker (`Design Phase Deliverables Tracker YYYY-MM-DD.xlsx`, per-discipline sheet) defines what a gate requires. Do not flag a package as missing a deliverable until checked against it — a deliverable you think is missing may simply not be required at that gate.

Worked correction (Aseer lighting 50%): "no lighting elevations" was flagged as a gap. Wrong. The tracker showed the 50% lighting package = 8 floor plans only (LL + HL x Basement/LGF/GF/1F); elevations are a 90%/100% deliverable. The report was a separate approved item; calcs/legend/control/emergency are separate tracked items still in progress.

## ZIPs beside PDFs = CAD source, not a separate package
A `.zip` named the same as a `.pdf` is the DWG source for that plot, not an extra deliverable. The submittal CG sees is the PDFs. Do not treat CAD zips as separate package items.

## Aseer project document naming convention
`MOC-ASE-{Discipline}-{System}-{Type}-{Floor}-DDD-{Sequence}-{Rev}`
- Discipline: 1A0 Arch / 1C0 Struct / 1E0 Electrical / 1M0 Mech / 1K0 PM / SIC Samaya
- System codes (electrical): ELT=Lighting, EPW=Power, EER=Earthing, EFA=Fire Alarm, ELV=BMS/ELV
- Type: DBR=Design Base Report, CALC=Calculation, GEN=Legend/Notes/Schedule, LL=Lighting Layout, HL=Highlight, EM=Emergency
- Floor: BF/LGF/GF/1F/2F/RF
- Example: `MOC-ASE-EL-ELT-LL-BF-DDD-30001-00` = Basement Lighting Layout

Architect floor baselines use `MOC-ASE-AR-ARC-{Floor}-DDD-1200/01/02/03` (GF/LGF/1F proposed GA series). Full standard in repo `_Style-Guides/naming-conventions.md`.
