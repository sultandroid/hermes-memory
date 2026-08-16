# Aseer Museum — Email Attachment Routing (OneDrive)

Verified 2026-08-16. Corrections + additions to the routing tables in the
`email-pipeline-automation` / `bim-email-pipeline` skills (those two are manually
authored and off-limits to autonomous curation, so the verified routes live here).

Project root:
`/Users/mohamedessa/Library/CloudStorage/OneDrive-SAMAYAINVESTMENT/Samaya/Technical Office/Bim Unit/Aseer-Museum/`

## Corrections to existing tables

- **Daily / Weekly Reports** → `07_Daily_Reports/` (NOT `00_Status/`). The
  `email-pipeline-automation` table says `00_Status/` — that is wrong. Daily
  Report PDFs land in `07_Daily_Reports/`.
- **Meeting Minutes (MOM)** → `00_Status/` (correct as-is).

## Verified document-code routes (add to routing script)

| Document code / pattern | Destination (relative to project root) |
|---|---|
| `1M0-1G-0005` (Fire Fighting 50% DD Gateway) | `02_Submittals/01_DD_Gate/MEP/` |
| `Fire_Fighting_System` / `TemplateMetadata` (FF submission xlsx) | `02_Submittals/01_DD_Gate/MEP/` |
| `1E0-1G-0004` (Small & AV Power Layout) | `02_Submittals/01_DD_Gate/Electrical/` |
| `1C0-IR-0003` (Core Test of Highlighted Columns) | `04_Docs/10_Test_and_Inspection/10.2_Inspection_Requests_IR/` |
| `1C0-ZD-0110` (Plan For Concrete Core Test Location) | `03_Design_Files/26_Structural/` |
| `1A0-PQ-0142/143/144` (Ready-mix Concrete Suppliers) | `24_Subcontractors/Civil_PQ/01_Prequalification/` |
| `SOR, 017` (Safety Observation Report) | `04_Docs/10_Test_and_Inspection/10.3_NCRs/SOR-017/` |
| `ICT ELV` / `Samaya and ICT Contract` | `00_Contracts/` |
| `Lighting Submissions Schedule` / `Lighting_Submittal_Register` (ZNA) | `24_Subcontractors/02_Lighting_Designer/01_Schedule_and_BOQ/` |
| `MEP-ZD-0107` (MEP design doc) | `03_Design_Files/MEP/` |

## Notes

- **Ready-mix concrete prequals** go to `24_Subcontractors/Civil_PQ/01_Prequalification/`
  — a flat folder, NOT a numbered `NN_` subcontractor folder. Verify with `ls`
  before routing; the numbered-folder assumption in the pipeline skill is wrong
  for these.
- **Core test IR** (1C0-IR-0003) routes to `10.2_Inspection_Requests_IR/`, not
  `10.3_NCRs/`. IR ≠ NCR — keep them separate.
- **SOR** (Safety Observation Report) gets its own numbered subfolder under
  `10.3_NCRs/SOR-NNN/`, mirroring the existing `SOR-015` pattern.
- **Daily Report** filenames use format `Daily Report DD-MM-YYYY.pdf` (space
  separators) — the `Daily_Report` underscore pattern in the pipeline skill
  misses these. Match both `Daily Report` and `Daily_Report`.
- **Stranded-file check**: after routing, `ls /tmp/email_attachments/` for
  non-image, non-eml leftovers. A prior-scan file (e.g. `MEP-ZD-0107` dated
  days earlier) may be stranded with no matching route — route it manually to
  its discipline folder.
