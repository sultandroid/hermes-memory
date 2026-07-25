# Four-Register Risk Architecture (the canonical pattern)

> Reference for `risk-register-management`. Captures the durable lesson from a real session: a project "risk register" is **four linked registers**, not one file, and the DDR lives inside the master workbook — not where you'd expect.

## The four linked registers

Aseer Museum RMP `MOC-MUS-ASE-1KH-PL-02.17` Section 9.1 is the canonical pattern for Samaya BIM projects:

| Register | Code | Scale | Scope | Typical count |
|----------|------|-------|-------|---------------|
| **Master Risk Register (PRR)** | `PRR-XXX-XX` (category-coded) | P×S 1-4 | All project-level risks — commercial, programme, design, construction, approvals, HSE | 50-60 |
| **Design Discipline Risk Register (DDR / DRR)** | `PR-Q-`, `DB-Q-`, `RE-Q-`, `ST-Q-`, etc. | P×I 1-5 | Active child design-phase risks for Technical Office control | 70-100 |
| **HSE Risk Register (HSE)** | varies | C×L 1-5 | Task-level HSE risks for fit-out scope | 40-50 | **Live** as of 2026-07-24 |
| **AV Risk Register (AV)** | varies | P×S 1-4 | AV/multimedia risks (design, procurement, integration, commissioning) | ~30 | **No source data found.** RMP says "in progress." The Consolidated workbook has an "AV Risk Register" sheet but its internal title reads "HSE Risk Register (Museum Fit-Out Scope)" and the data is HSE activity-based (C×L 1-5), NOT AV P×S risks. Treat as mislabeled HSE, not AV. |

## Where the DDR actually lives

**The DDR is a sheet INSIDE the master C-numbered workbook, not a standalone file.**

In OneDrive you may see a folder `02_Design_Risk_Register/` — it's almost always empty because the DDR lives in:

```
<Plan Folder>/04_Registers/01_Master_Risk_Register/
  └── Aseer_Museum_Risk_Register_C<rev>_<date>.xlsx
        ├── Sheet: Cover
        ├── Sheet: Dashboard
        ├── Sheet: Scoring Matrix
        ├── Sheet: RBS
        ├── Sheet: Risk Register                <-- PRR (51 rows, P×S 1-4)
        ├── Sheet: Designer Risk Register (DRR) <-- DDR (79 rows, P×I 1-5)
        ├── Sheet: Construction Stage
        └── Sheet: HSE Risk Register (Fit-Out)
```

If the dedicated folder is empty, that's not a bug — the data is in the master workbook's DRR sheet.

## DRR ID prefix conventions (very different from PRR)

The DDR uses **discipline-letter prefixes**, not category codes:

| Prefix | Likely meaning |
|--------|----------------|
| `PR-Q-` | Programme risk — quality/process (e.g. PR-Q-001 = "24 documents in 14 days") |
| `DB-Q-` | Design-Build quality (e.g. DB-Q-001 = "Pre-contract design liability") |
| `RE-Q-` | Regulatory/Requirements |
| `ST-Q-` | Standards/Strategy |
| `DB-A-` | Design-Build Architecture |
| `DB-S-` | Design-Build Structural |
| `DB-M-` | Design-Build Mechanical |
| `DB-E-` | Design-Build Electrical |
| `DB-F-` | Design-Build Fire |
| `DB-T-` | Design-Build Technology |
| `DB-X-` | Design-Build Cross-discipline |
| `CO-X-`, `CO-S-`, `CO-V-`, `CO-M-`, `CO-E-`, `CO-T-`, `CO-G-`, `CO-L-`, `CO-B-` | Commissioning variants by discipline |
| `TE-E-`, `TE-F-`, `TE-M-`, `TE-S-`, `TE-P-`, `TE-T-`, `TE-V-`, `TE-L-` | Test/commissioning variants |
| `BI-B-` | BIM coordination |
| `EX-X-`, `EX-L-`, `EX-V-`, `EX-G-`, `EX-S-` | Exhibition (Lighting, AV, Graphics, etc.) |
| `QA-Q-` | Quality Assurance |
| `ST-S-`, `ST-E-`, `ST-T-`, `ST-F-` | Structural discipline variants |
| `COM-CM-` | Commercial (CM = Commercial Management) |
| `DDR-DES-005`, `DDR-MAT-001` | occasional parent-style IDs linking to PRR or materials |

The DDR has its own RBS categories that **differ from the PRR**:

- `TEC` = Technical/design (49 risks — the bulk)
- `SCH` = Schedule
- `EXT` = External (stakeholder/authority)
- `PRO` = Procurement
- `QA` = Quality
- `COM` = Commercial

## RMP section cross-references

When updating an RMP, the following sections MUST stay aligned to the **live Excel C-number**, not the plan revision:

- **Section 2.1** — Current Risk Snapshot (Total / Critical / High / Medium / Low)
- **Section 4.2** — Current Risk Distribution (per RBS category)
- **Section 9.1** — Register Structure (the 4-register table)
- **Section 13** — Register Status Summary (C-number, count, status)
- **Section 7.3** — Quantitative Metrics (cites C-number)
- **Frontmatter** — `revision: REVxx` and `last_updated: YYYY-MM-DD`
- **Document Control table** — add new REV row describing what changed

## Drift pattern (and how to spot it)

The RMP plan and the live Excel drift in opposite directions:

- Plan revision: `REV00 → REV01 → REV02` (slow, human-driven, only on CG submission)
- Excel revision: `C01 → C02 → C03 ... → C11 → C12` (faster, weekly, more frequent)

A plan at REV01 citing "C05 / 29 risks" while the Excel is at C11 / 51 risks is the most common drift. Spot it by:

1. Reading the live Excel's first sheet cover/revision
2. Reading the RMP frontmatter
3. Comparing the two revision numbers — if Excel is ahead by ≥2 revisions, the plan is stale

## Quick verification (after any sync)

```bash
# Excel says:
python3 -c "from openpyxl import load_workbook; wb=load_workbook('<C11>'); ws=wb['Risk Register']; print(sum(1 for r in ws.iter_rows(values_only=True) if r[1] and str(r[1]).startswith('PRR-')))"

# JSON says:
python3 -c "import json; print(len(json.load(open('06_Risk_System/risks.json'))['risks']))"

# RMP says (in 9.1):
grep -E "^\| Master Risk Register" 03_Plans/08_Risk/risk_management_plan.md
```

All three must match. If not, the RMP is stale.
