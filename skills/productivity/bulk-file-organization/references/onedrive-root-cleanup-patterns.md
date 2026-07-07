# OneDrive Root Cleanup Patterns

## Source
Samaya Investment OneDrive root cleanup, Jun 2026. ~250 loose files, 26G total.

## File routing by prefix — Samaya project codes

| Prefix | Project | Target dir |
|---|---|---|
| `MOC-*`, `MOC-MUS-ASE-*`, `MOC-ASSER-*`, `MOC-CG-ASE-*` | Aseer Museum | `Aseer-Museum/09_Correspondence/` |
| `M2742-*`, `A2742-*` | Aseer Museum (drawing series) | `Aseer-Museum/` |
| `SI-CG-ASEER-*` | Aseer Museum (site instructions) | `Aseer-Museum/09_Correspondence/` |
| `RE *`, `Reply to *`, `Re NCR *` | Aseer Museum (replies) | `Aseer-Museum/09_Correspondence/` |
| `BMS *`, `HSE NCR *` | Aseer Museum (reports) | `Aseer-Museum/09_Correspondence/` |
| `ZAM-NWC-*` | Zamzam Visitor Center | `Zamzam-Visitor Center/` |
| `P083_*` | Zamzam Museum | `Zamzam-Visitor Center/` |
| `MVii*` | Madinah/Haramain project | `_Misfiled_From_Aseer_00Admin/MVii/` |
| `Daily Report *` | Aseer Museum | `Aseer-Museum/07_Daily_Reports/` |
| `Aseer Regional Museum - Weekly Report *` | Aseer Museum | `Aseer-Museum/08_Weekly_Reports/` |
| `Asir_Regional_Museum_WEEKLY STATUSDASHBORD *` | Aseer Museum | `Aseer-Museum/08_Weekly_Reports/` |
| `Weekly Project Coordination Report*` | Aseer Museum | `Aseer-Museum/08_Weekly_Reports/` |
| `* update.pdf` (23 may, 30 may, etc.) | Aseer Museum progress updates | `Aseer-Museum/07_Daily_Reports/` |
| `Aseer 2026 *`, `Zna Scope *`, `Asir *NDA*` | Aseer proposals | `Aseer-Museum/11_Proposals/` |
| `01-Leica*`, `*RTC360*`, `*BLK360*`, `*Spider*`, `*EinScan*`, `*Cyclone*` | Hardware specs | `Samaya/Docs/Hardware_Specs/` |
| `Package * CV Submittal*` | Company CV packs | `Samaya/Docs/` |
| `* CV_2026*`, `Eng. *` | Employee files | `Samaya/Employe details/` |
| `OVER TIME MAY*`, `overtime_report*` | Overtime records | `Samaya/OVER TIME/2026/` |
| `accountDetailStatement*`, `VD.pdf`, `RAK*`, `G16131*` | Financial docs | `Samaya/Docs/Financial/` |
| `Sent Items - Kareem*` | Old email exports | `Archives/` |
| `01-AL JALAL*`, `AL JALAL*` | Al Galal & Al Gamal project | `Al Galal & Al Gamal Meuseum/` |
| `Car Booking Request*` | Admin/orders | `Samaya/Orders/` |
| Arabic-named DOCX/PDF referencing specific projects | Route to matching project folder | Check project name in filename |
| `*Makkah*`, `*الغمامة*` | Route by location reference | Match to Bim Unit project subfolder |
| `1000113724.jpg`, `IMG_*.jpeg`, `WhatsApp Image*` | Site/temp photos | `_Unsorted/` for review |
| Timestamp PNGs (`240831*`, `260430*`) | Likely screenshots | `_Unsorted/` |

## Reports/ subfolder consolidation

When two folders share the same purpose:
- `Budget/` + `Budgets/` → consolidate into `Budgets/`
- `Projects List/` + `ProjectsList/` → consolidate into `ProjectsList/`

## Reporting structure for user

Present results as a comparison table:

| Metric | Before | After |
|---|---|---|
| Root-level files | ~251 | ~26 (all cloud stubs) |
| .dwl/.dwl2 lock files | 1,597 | 920 (remaining are cloud-only) |
| Reports/ loose files | ~38 | 0 (sorted into 33 subdirs) |
| Scans/ organization | 58 loose folders | grouped into 4 categories |

## Key lessons
- Always check if files are 4B OneDrive stubs before deleting — these are cloud-only placeholders, not actual files
- Use `find -exec rm` as fallback when `find -delete` hangs due to OneDrive sync
- Parallel delegation with 3 subagents works well for 100+ file moves
- Keep system folders (PDFs/, Revit/, SoftWare/) — OneDrive recreates them
