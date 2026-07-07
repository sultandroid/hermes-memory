# BIM Unit — Standard Folder Template

Reference: `Bim Unit/Template Folder/`

## Top-Level Folders (14)

```
Project Name/
├── As-Built Docs/          # Completed/as-built drawings and documents
├── B.O.Q/                  # Bills of Quantities (pricing, item schedules)
├── Contracts/              # Agreements, POs, SOWs, subcontracts
├── Design Files/           # Design drawings, PDFs, CAD files, renders
├── Docs/
│   ├── 09_Registers/       # Excel tracking registers (Submittal Log, Drawing Register, RFI Log, etc.)
│   └── ... (project documents, plans, memory files)
├── Email_Archive/          # Email threads and attachments
├── Invoices/               # Financial invoices and payment records
├── Reports & Meeting/      # Meeting minutes, weekly/monthly reports
├── Revit Files/
│   ├── Cad/                # Exported CAD from Revit
│   ├── Clash Reports/      # Navisworks clash detection reports
│   ├── Excel Sch/          # Revit schedules exported to Excel
│   ├── Nwc/                # Navisworks NWC cache files
│   ├── Pdf/                # Revit sheet PDF exports
│   ├── Rfa/                # Revit family files (.rfa)
│   └── Rvt/                # Revit project files (.rvt)
├── Scripts/                # Automation scripts, tools, generators
├── Specs & Datasheet/      # Technical specifications, product datasheets
├── Submittal's/
│   ├── Arch/               # Architectural submittals
│   ├── Mep/                # MEP submittals
│   └── Struc/              # Structural submittals
├── Time Scheduales/        # Project schedules, timelines, Gantt charts
└── odoo/                   # Odoo ERP exports
    ├── 01_Initiation/      # Phase 1: Initiation
    ├── 02_DD_Stage/        # Phase 2: Design Development
    ├── 03_Procurement/     # Phase 3: Procurement
    ├── 04_Manufacturing/   # Phase 4: Manufacturing
    ├── 05_Execution/       # Phase 5: Execution / On-site
    └── 06_Handover/        # Phase 6: Handover / Close-out
```

## Projects Currently Following This Template

| Project | Status |
|---|---|
| Aseer-Museum | ✅ Template source |
| Hera' Ghar | ✅ Verified |
| Masjid Alnoor | ✅ Reorganized to match |
| Zamzam -Visitor Center | ✅ Close match |
| Zamzam Museum | ✅ Close match |

## Non-Standard Projects (refer to their custom structure)

| Project | Structure |
|---|---|
| Jabal Omar - Samaya Scope | Datasheets, Docs, Exterior Screens, General, Jabal Omar - Deliverables |
| Ryadh Museum | Docs, Ryadh Meuseum Fin |
| Hadaya_Teiba_01_GND | odoo/ only |
| Jabal Omar - Samaya Scope | Custom subdirs only |

## Keywords for Auto-Classification

When the watchdog or a labor needs to classify a file to a subfolder:

| File Name Contains | Route To |
|---|---|
| submittal | Submittal's/ |
| design or DWG or PDF (design context) | Design Files/ |
| revit or RVT or RFA | Revit Files/ |
| boq or pricing or quantity | B.O.Q/ |
| contract or agreement or PO | Contracts/ |
| invoice or payment | Invoices/ |
| report or meeting | Reports & Meeting/ |
| schedule or timeline | Time Scheduales/ |
| spec or datasheet | Specs & Datasheet/ |
| as built | As-Built Docs/ |
| archive or email | Email_Archive/ |
| script or tool | Scripts/ |
| register or log | Docs/09_Registers/ |
