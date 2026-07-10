# Merged from bim-project-register skill

## The 14 Registers

Every project has these in `Docs/09_Registers/`:
1. Drawing_Register.xlsx — all drawing files (CAD, PDF)
2. Submittal_Register.xlsx — all submittal packages
3. RFI_Register.xlsx — Request for Information
4. SI_Register.xlsx — Site Instruction
5. NCR_Register.xlsx — Non-Conformance Report
6. Change_Order_Register.xlsx — change orders
7. Material_Register.xlsx — material approvals
8. Invoice_Register.xlsx — invoices
9. Meeting_Minutes_Register.xlsx — meeting minutes
10. Transmittal_Register.xlsx — transmittals
11. Contract_Register.xlsx — contracts
12. Risk_Register.xlsx — risks
13. Subcontractor_Register.xlsx — subcontractors
14. HSE_Register.xlsx — health, safety, environment

## Standard Column Headers Per Register

| Register | Data Sheet | Columns |
|---|---|---|
| RFI | RFI | Date, RFI #, Subject, From, To, Status, Priority, Response, File Path, Remarks |
| SI | SI | Date, SI #, Subject, From, To, Status, File Path, Remarks |
| NCR | NCR | Date, NCR #, Description, Discipline, From, To, Status, File Path, Remarks |
| Change Order | ChangeOrder | Date, CO #, Description, From, To, Status, File Path, Remarks |
| Material | Material | Date, Material #, Description, Type, Status, File Path, Remarks |
| Invoice | Invoice | Date, Invoice #, Description, Contractor, Amount, Status, File Path, Remarks |
| Meeting Minutes | MeetingMinutes | Date, MM #, Subject, Location, Time, Status, File Path, Remarks |
| Transmittal | Transmittal | Date, Transmittal #, Subject, From, To, Status, File Path, Remarks |
| Contract | Contract | Date, Contract #, Description, Contractor, Status, File Path, Remarks |
| Risk | Risk | Date, Risk #, Description, Impact, Probability, Mitigation, Status, File Path, Remarks |
| Subcontractor | Subcontractor | Date, SC #, Name, Scope, Status, File Path, Remarks |
| HSE | HSE | Date, HSE #, Description, Type, Status, File Path, Remarks |

## Watchdog (Automatic Register Updates)

Script: `~/.hermes/scripts/bim_watchdog.py`
- `--scan` : One-shot scan (used by cron every 2 minutes)
- `--daemon` : Continuous FSEvents mode (macOS native)

Cron: Job `048f24e5d9dd` — runs `bim_watchdog.py --scan` every 2 minutes

State file: `~/.hermes/scripts/.watchdog_state.json`
Log: `~/.hermes/scripts/bim_watchdog.log`
Notify script: `~/.hermes/scripts/hermes_notify.sh`

Projects watched (17): Aseer-Museum, El-Ghamama (4 projects), Zamzam Museum, Zamzam Visitor Center, El-Haramain, Hera' Ghar, Masjid Alnoor, Khair El-Khalq, Jabal Al-Noor Dispatch, Prime Business Resort, Jabal Omar retail shops (3)

## Pitfalls (merged)

- `execute_code` sandbox does NOT have openpyxl — use `terminal(python3 -c "...")`
- `ws.append()` fails on empty/headerless sheets — use explicit row assignment
- Cover sheet "Last Updated" uses merged cells — catch AttributeError on merged cells
- Data sheet names differ per register — look up by name, not index
- Always verify after saving: re-open and check headers + data rows
