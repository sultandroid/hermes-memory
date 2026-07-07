# Aseer Museum — AV Submittal Register Creation (June 2026)

## Source Documents

| Doc | Path |
|-----|------|
| SOW | `Contracts/01_Main_Contract/Contractors Scope of Works Document - Technical_250313/6380_KMS_RPT_PM_AS_00006_Aseer_Contractors_Scope of Work.pdf` (72 pages) |
| ER | `Contracts/01_Main_Contract/Contractors Employers Requirements - Engineering_250313/250313_ER Document - Aseer Museum of Arts_R02.pdf` (170 pages) |

## Key SOW Sections for AV

- **SOW 6.22.2** — Audio-visual hardware systems design (21 deliverable types)
- **SOW 6.22.4** — Technical Design Deliverables Summary (50%/90%/100% sub-stages; item xiii = AV, xiv = Lighting)
- **SOW 6.9** — Design Phase Submittals (design reports, IFC docs, specs, material/equipment submittals, ITPs)
- **SOW 6.10-6.18** — Product data, certificates, test reports, design data
- **SOW 8.9** — Audiovisual Hardware (full design-fab-install-commission scope)
- **SOW 8.10** — AV Software (EXCLUDED from Contractor scope — coordination only)
- **SOW 13** — Training programme (AV systems O&M training for MoC)

## Key ER Sections for AV

- **ER 3.2** — Power supply & distribution (SMDB-AV, surge protection, power wiring)
- **ER 3.3** — Network/Telecoms (fibre to AV rooms, data points, WAPs)
- **ER 3.4** — Network/Security (CCTV independent per MOI, access control, AI cameras)
- **ER 3.5** — Fire Alarm & PAVA (COOPER FACP integration, SPL calcs, Civil Defense approval)
- **ER 5.0** — Room Data Sheets (AV heat dissipation loads per gallery, AV Room FCU specs)

## Package Distribution (60 items total)

| Package | Count | Key content |
|---------|-------|-------------|
| 50% Design | 9 | Block schematics, load estimates, design intent |
| 90% Design | 37 | Refined drawings, coordinated layouts, detailed schedules |
| 100% Design | 37 | Final coordinated, ready for IFC |
| IFC/AFC/Construction | 20 | Equipment data, fabrication dwgs, commissioning, handover |

## Register Columns

Ref #, Submittal/Deliverable, SOW §, ER §, Discipline, 50% Status, 90% Status, 100% Status, Final IFC/AFC, Works Package, Remarks

## Deployment Locations

All 3 copies are identical — update the original, then recopy:
1. `02_Submittals/AV_Submittal_Register.xlsx` (original + generator script)
2. `Docs/09_Registers/AV_Submittal_Register.xlsx`
3. `Subcontractors/03_AV_IT_Contractor/01_Schedule_and_BOQ/AV_Submittal_Register.xlsx`

## Generator Script

`02_Submittals/AV_Submittal_Register.py` — rerun to regenerate all 3 copies.

## AV Systems (from SOW 8.9)

- Ceiling/wall mounted projectors (incl. setworks-integrated)
- Directional + ambience speakers (ceiling/wall/setwork/plinth)
- Screens, monitors, interactive screens, pads
- Universal Access Points
- VR Headsets (as applicable)
- AV racks + Show Control System (separate from basebuild IT)
- Mockup/prototype AV kit for software-hardware integration testing

## Coordination Interfaces

| System | Coordinates With |
|--------|-----------------|
| AV Display | Setworks, Showcases, Lighting, Structural |
| Audio | Acoustic consultant, Setworks, FLS |
| Show Control | Lighting Control DALI/DMX, BMS, FLS |
| PAVA | Fire Alarm FACP (COOPER), BMS, Civil Defense |
| CCTV | MOI Security Network |
| AV Power | MEP, SMDB-AV, Scenographer equipment |
| Control Room | Security, FLS, BMS, HVAC (clean agent FP) |
