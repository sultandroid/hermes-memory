# AV/IT Subcontractor Dossier Pattern

AV/IT subcontractors (like NMK/Q-Sys for Aseer Museum) have a distinct file structure from other trades. Their deliverables include product datasheets, company profiles, and scope-of-work spreadsheets alongside standard prequalification docs.

## Standard AV Subcontractor Folder Structure

```
AV/
├── Prequalifications/
│   ├── NMK Company Profile - Brands.pdf
│   ├── NMK Company Profile -KSA Version.pdf
│   └── COO and Warranty.pdf
├── Product_Datasheets/
│   ├── CORE 510i.pdf              (master processor/DSP)
│   ├── SERVER CORE X10.pdf        (server processor)
│   ├── TSC-50-G3.pdf              (5" touch screen)
│   └── TSC-70-G3.pdf              (7" touch screen)
└── Scope_of_Work/
    └── Q-Sys scope of work.xlsx
```

## Key Differences from Other Trades

| Aspect | AV/IT | Other Trades |
|--------|-------|-------------|
| **Company profile** | Often includes brand portfolio (NMK distributes multiple brands) | Single-entity profile |
| **Product datasheets** | Multiple per product line (Core processors, touch screens) | Usually 1-2 per material |
| **Scope format** | Excel BOQ with location mapping | Word/PDF narrative |
| **Subfolders** | UUID-named duplicates common (from download managers) | Rare |

## UUID-Named Duplicate Detection

AV product downloads from distributor portals often create UUID-named PDFs (e.g. `3eae2483-f4c5-42b9-829d-5e3674949222.pdf`). These are identical to the named datasheets. Detection:

```bash
# Compare file sizes to find duplicates
ls -la *.pdf | sort -k5 -n
# Check MD5 of UUID files vs named files
md5 -q 3eae2483-*.pdf
md5 -q CORE\ 510i.pdf
```

If sizes match, the UUID files are duplicates — skip them.

## NMK / Q-Sys Specifics (Aseer Museum)

- **Supplier:** NMK (Q-Sys distributor in KSA)
- **Products:** Q-Sys Core 510i (master processor/DSP/Dante), Core X10 (server), TSC-50-G3 (5" touch), TSC-70-G3 (7" touch)
- **Scope:** 4x TSC-50-G3 (Café, VIP, Shop, Children's, Makers Room) + 1x Core 510i + 1x TSC-70-G3
- **AV Designer:** Rawasin (Samaya sister company) — contract executed per scope_summary.md
- **Doc code prefix:** MOC-ASE-AV-TAV-{floor}-DDD-xxxx

## When to Use

- User drops AV/IT files from Downloads and asks to organize
- User shares a Q-Sys or similar AV control system scope
- Need to distinguish between AV equipment supplier (NMK) and AV designer (Rawasin)
