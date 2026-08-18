# Rawasin AV Package CRS — Extraction & File Location Workflow

Applies when building a CRS for the **AV Package Part II** (Rawasin, doc ref `MOC-MUS-ASE-1E0-1G-0002`), a DD 50% Gate submittal returned Code C/D by CG reviewer **Venugopal Poyakkara Veetil** (Interactive AV Specialist, rejects generic documents).

## Doc refs & locations
- **Doc ref:** `MOC-MUS-ASE-1E0-1G-0002` (AV Package Part II). Discipline 1E0 (Electrical/AV).
- **Source of truth (Adel bank):** `OneDrive - SAMAYA INVESTMENT/Adel  Darwish's files - 01- Execution Documents/20- DDD/ELE/02-  MOC-MUS-ASE-1E0-1G-0002/`
  - Contains only `MOC-MUS-ASE-1E0-1G-0002.pdf`, `... Att.zip`, `... .xlsx` (submittal register). **These are OneDrive stubs** — reading them raises `EDEADLK` / `BadZipFile` (openpyxl "File is not a zip file"). Not directly readable; source them elsewhere.
- **Working package (readable):** `/Volumes/MIcro/Download/AV Package Part II Rev. 001/` with subfolders:
  - `00- Submital Register/`
  - `01- Requirements/` → `Key Control and Programming Requirements.docx/.pdf`, `UPS Requirements for AV Rack Aseer Museum.pdf`, `Ups Requirements Av Rack {Basement|Ground|Lower Ground} Rack Aseer Museum.docx`
  - `02- Documents/` → `AV Control Hierarchy.docx/.pdf`, `AV Network Architecture for Dante and Dedicated AV Network.docx/.pdf`
  - `03- Projection Study/` → `Projection Mapping Study.pdf`
  - `04- Response/` → `Audit Response.xlsx`
  - `05- AV Content Managment System (CMS)/` → `AV Control Managment System (CMS).pdf`

## CG 2nd-submittal doc refs (verbatim file names CG cites)
| CG comment | Actual file in package |
|---|---|
| `AV Control Hierarchy.pdf` | `02- Documents/AV Control Hierarchy.pdf` |
| `AV Network Architecture...pdf` | `02- Documents/AV Network Architecture for Dante and Dedicated AV Network.pdf` |
| `Control System User Interface & Fault Monitoring.pdf` | NOT a standalone file in `02- Documents/` — verify it exists (may be inside `Att.zip` or another folder) before claiming it's submitted. |
| `Key Control and Programming Requirements.doc` | `01- Requirements/Key Control and Programming Requirements.docx` |
| `UPS Requirements for AV Rack.pdf` | `01- Requirements/UPS Requirements for AV Rack Aseer Museum.pdf` |

## Audit Response.xlsx structure (2 sheets) — comment/reply in ALTERNATING ROWS
The subcontractor's response workbook is NOT the standard one-row-per-comment CRS. Structure:
- **Sheet `1st Submital responce`** — A=No, B=CG comment (row N), B=Rawasin reply (row N+1), repeating. 18 comments.
- **Sheet `2nd Submital responce. `** (note trailing space in sheet name) — same alternating pattern. 5 comments.
- When reading: iterate rows; a row with a No. in col A begins a comment, the next row's col B is the reply. Do not expect reply in a separate column.

## CRS template mapping (from `CRS_TEMPLATE_BLANK.xlsx`)
- Data rows start **row 11**. Header block rows 1-7 (PROJECT NAME, CRS NUMBER, DOCUMENT No., Rev, DATE, DISCIPLINE, DOCUMENT TITLE, DOCUMENT TYPE).
- Columns: A=No., B=Initial, C+D=Sheet/Ref, E-I=Reviewer Comment (merged), J-O=Originator Reply (merged), P=Reply By, Q=Status.
- Code C cells: red fill `#B01E2F`, white bold. Status: Closed=green `#C6EFCE`; Open=red `#FFC7CE`.
- Write values BEFORE merged-cell handling; set col widths + row heights for readability.

## Pitfalls
- **CDE "ExportDocs" export only includes first 100 of N results.** When the user sends an Aconex/CDE `ExportDocs-*.xlsx`, the AV/Rawasin files may not be in the visible 100 (often all weekly/daily reports, meeting minutes, demolition drawings). Do NOT conclude files are missing — search **Adel's bank** (`20- DDD/` DDD folder) for the doc ref instead.
- **OneDrive stubs + EDEADLK:** reading files under `Adel Darwish's files - 01- Execution Documents/` fails (`Resource deadlock avoided` on cp, `File is not a zip file` on openpyxl). Use the `/Volumes/MIcro/Download/...` copy for actual parsing.
- The AV Package Part II CRS carries status **Open for the blockers** (Lighting/PAVA scope gap, commissioning, labelling, iPad/BOQ deviation, DALI/DMX accountability) — it is a **pre-submission** document, not to be sent to CG until Rawasin resolves them.
