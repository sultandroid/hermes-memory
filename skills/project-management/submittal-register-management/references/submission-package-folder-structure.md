# Submission Package Folder Structure — Aseer DD (Model A)

User decision (2026-08-23): organize submittals **submission-centered**, NOT
document-centered. Each outgoing submission is a discrete, traceable event
(one transmittal, one revision set, one date, one CG review) and must stay whole
so it can be re-issued/resubmitted as a unit.

## Convention
Under the DD submittals root (e.g. `3.2_DD Doucments Structure/`):

```
<root>/
├── 0_Registers/          # master register
├── 1- DD Drawing/        # document-type reference archive (legacy category folders)
├── 2- BOD/
├── 03_CG Response/
└── Submissions/          # ← ALL submission packages live here
    ├── 4- ETABS Model Submission 2026-08-17/
    │   ├── 00_Transmittal/      Transmittal_...xlsx  (From/To/Cc, doc table, sign-off)
    │   ├── 01_ETABS_Model/      delivered files (.EDB/.e2k)
    │   ├── 02_AsBuilt_Drawings/  delivered files
    │   ├── 03_QC_Checklist/      filled QC/QA checklist
    │   ├── 04_Registers/         package-specific submission register snapshot
    │   └── README.md             package index + purpose + QC gate note
```

## Rules
- One dated folder per submission: `Submissions/<NN>-<Name> <YYYY-MM-DD>/`.
- Every package carries: transmittal, the files, a filled QC checklist, a
  submission-register snapshot, README.
- Document-type folders (`1- DD Drawing/`, `2- BOD/`) remain the **reference
  archive** — a file may legitimately exist in BOTH a reference folder and a
  submission package (dual-location pattern). Don't delete from reference folder
  when packaging.
- Log the outgoing transmittal in the project master transmittal register
  (`04_Docs/09_Registers/30_Transmittal_Register/`) using TRX-OUT-#### numbering,
  and note the 14-day deemed-approval action per ER §2.4.A.
- Register refs map to the master register rows; Status=Submitted; leave
  Response Code column to fill on CG reply.

## QC checklist conventions
- Simple single-sheet: full header (title/date), one section per submittal type,
  `☐`/`☑` checkbox + PASS/FAIL/NA. **Any FAIL = do not submit.**
- openpyxl has NO native checkbox API — use `☐` (U+2610) / `☑` (U+2611) text glyphs.
- Do the actual QC review against the real files (open PDFs, read ETABS headers,
  verify drawing numbers via vision on title blocks) and fill the Done/Pass columns.
  Don't leave the checklist blank. Distinguish PASS / NA (not applicable) / NO (real gap).
- The F. Internal QA Gate section (Preparer → Checker → Tech Office Reviewer) is
  the user's sign-off — leave those blank for them; flag NO items as blockers to
  issue.
