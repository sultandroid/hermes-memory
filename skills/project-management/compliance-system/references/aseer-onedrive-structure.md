# Aseer Museum — OneDrive Folder Structure (verified 2026-07-13)

> Single source of truth for where to file Aseer Museum submittals in OneDrive.
> Last verified 2026-07-13 by `touch` write-test on the canonical folders.
> If a future session finds one of these paths has moved or is no longer
> writable, update this file and re-verify.

## Canonical project tree (writable from terminal, uid 501)

Root: `/Users/mohamedessa/OneDrive - SAMAYA INVESTMENT/Samaya/Technical Office/Bim Unit/Aseer-Museum/`

```
Aseer-Museum/
├── 00_Project_Charter/          # ER, SoW, contract
├── 02_Submittals/
│   ├── 03_Submittals/
│   │   ├── 03.3_Material_Submittals/<NN> -MA-####/  # approved MAs
│   │   └── ...
│   ├── 04_Registers/             # Submittal registers (Excel)
│   ├── 09_Prequalifications/    # ★ PQ canonical filing (flat folder)
│   └── ...
├── 03_Submittals/                # alias / older structure
├── 04_Docs/
│   ├── 03_Submittals/
│   ├── 09_Registers/             # ★ Includes 27_Subcontractor_Prequalification_Register
│   └── ...
├── 24_Subcontractors/
│   ├── 04_AV_IT_Contractor/      # Rawasin (AV/IT sub-contractor)
│   │   ├── 01_Schedule_and_BOQ/ # ★ Equipment BOQ XLSXs land here
│   │   ├── 05_Returned_Submittals/
│   │   ├── 07_Approvals/
│   │   └── ...
│   ├── 13_MEP_Designer/         # AD Engineering
│   ├── 14_MEP_Contractor/
│   ├── 05_Showcases_Contractor/ # Glasbau Hahn
│   ├── 21_Landscaping_Specialist/
│   ├── 12_Structural_Contractor/
│   └── ...                       # one folder per specialist
├── 99_Archive/                   # superseded / old revs (read-only archive)
└── ...
```

### Filing rules

- **PQ documents (formal cover letters, trade licenses, TRN, COO/Warranty, product datasheets submitted as part of a PQ):**
  → `02_Submittals/09_Prequalifications/` with filename
  `MOC-MUS-ASE-1<disc>-PQ-<####>_<Vendor>_<DocType>.pdf`

- **Equipment BOQ XLSXs / scope-of-work XLSXs / vendor commercial quotes:**
  → `24_Subcontractors/<NN>_<ContractorName>/01_Schedule_and_BOQ/`
  with filename `<Vendor>_<Scope>_<YYYY-MM-DD>.xlsx` + a sidecar
  `<_Vendor>_<Scope>_DepositRecord.md` per AGENTS.md `PDF + _Analysis.md sidecar` rule.

- **Approved material submittals (MA):**
  → `02_Submittals/03_Submittals/03.3_Material_Submittals/<NN> -MA-####/`
  with the standard MA-#### folder pattern.

- **Submittal registers (Excel):**
  → `04_Registers/` (per discipline), managed by the Submittal_Register scripts.

## Do NOT use (Adel's personal folder, unwritable from terminal)

```
~/OneDrive - SAMAYA INVESTMENT/Adel  Darwish's files - 01- Execution Documents/
```

Owner uid is 114, current user is uid 501 → `mkdir` returns
"Operation not permitted" even though shell `id` shows uid 501.
The folder is Adel's personal execution working area, not the project
canonical. Historical PQs are filed there; new ones go to the BIM tree.

## Writable check command

Before any new file operation, run:

```bash
TARGET="/Users/mohamedessa/OneDrive - SAMAYA INVESTMENT/Samaya/Technical Office/Bim Unit/Aseer-Museum/02_Submittals/09_Prequalifications"
touch "$TARGET/.test_write" && rm "$TARGET/.test_write" && echo "WRITABLE" || echo "NOT WRITABLE — DO NOT FILE HERE"
```

If the canonical tree ever reports NOT WRITABLE, fall back to writing a
`_FILE_PLAN.md` next to the source files in `/Volumes/MIcro/Download/` so
the user can run the `cp` commands manually. Never silently misfile.

## Related vendor facts (from this session)

- **ProLab Trading LLC** (TRN 100552354100003) is a **UAE/Dubai distributor**,
  not a KSA local agent. Trade licenses are Dubai/DET. When a submittal
  arrives via ProLab, the PQ is filed under ProLab's name with "UAE distributor"
  in the matrix and gap notes — NOT "KSA agent". See
  `references/local-agent-vs-distributor.md` for the verification recipe.
- **Audinate** is the manufacturer (AU); ProLab is the UAE distributor that
  fronts the BOQ. Both need separate PQs: one for the manufacturer (PQ-0113
  in this case, next free in the register) and one for the distributor
  (PQ-0114). The compliance gap must name both.
