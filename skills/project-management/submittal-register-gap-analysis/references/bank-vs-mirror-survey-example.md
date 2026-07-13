# Bank-vs-Mirror Survey — Worked Example

> Canonical reference for future agents. This is the 2026-07-13 survey of
> `~/OneDrive/.../Adel Darwish's files - 01- Execution Documents/` against the
> `~/aseer-museum-pm` repo registers. Five commits were produced from this
> single survey.

## When to use

Reach for this reference when the user hands over an external OneDrive bank
folder and asks "is there new info to push to the repo?" — the answer is
usually yes, but the workflow has specific mechanics (Python over bash,
temp scratch on /Volumes/MIcro, no binaries in the repo) that bite if you skip
them. This file shows the full cycle.

## The bank structure (Aseer Museum Adel Darwish example)

```
~/OneDrive/.../Adel Darwish's files - 01- Execution Documents/
├── 01- Letters/                IN/OUT split — partial mirror in correspondence_register.md
├── 02. DOC - Document Submittal/  not indexed
├── 03. SD  SHOP DRAWING/       not indexed
├── 04- Daily Report/           not indexed
├── 05- Request For Information-RFI/  19 folders — match rfi_register.md
├── 06- Weekly Meeting MOM/     12 PDFs (02-14) — only 14 in repo — BACK-FILL
├── 07- Pre-Qualification Submittal/  110+ folders — match prequalification_register.md
├── 08- Material Submittal MA/  7 AR + 1 EL — match material_submittal_register.md
├── 09- Method Statement MWS/   16 folders — match method_statement_register.md
├── 10- CG Site Instruction SI/ 19+ folders — match si_register.md (some mis-filed)
├── 11- IFC Drawing/            drawing_register only
├── 12- NCR/                    13 folders — not mirrored (ncr_register.md sparse)
├── 13- Weekly Report/          18 PDFs (mostly Arabic) — dashboard aggregates
├── 14- Inspection Request/     4 folders — NOT mirrored
├── 15- Start Nwe Activity (SNA)/  5 folders — NOT mirrored
├── 16- Safety Notices/         HSE plan covers
├── 17- SOR/                    11 folders — NOT mirrored
├── 18- MIR/                    not mirrored
├── 19- Weekly HSE Reports/     5 folders — HSE plan covers
├── 20- DDD/                    3 subfolders (AR / ci / ELE) — not indexed
└── ASM_Material_Procurement_Schedule_ARCH.xlsx   169 rows — NEW MASTER DATA
```

## The assessment file structure (output)

`09_Agent_Workspace/adel_execution_bank_assessment.md` followed this layout:

1. **YAML frontmatter** — last_updated, owner_agent, status, source path
2. **Bank inventory table** — 24 rows (sub-folders + root Excel) with
   Count column + Mirror Status column ("Already mirrored" / "Partial mirror"
   / "Not mirrored" / "NEW DATA")
3. **What is genuinely new** (ranked by value):
   - **HIGH**: Master ASM Material Procurement Excel (169 rows), 11 historical
     MoMs, CG Site Instruction register enrichment
   - **MED**: MA folder cross-check artefacts (388 supplier PDFs in MA-0001
     subfolder, sample board data sheets in MA-0006)
   - **LOW / SKIP**: Weekly Reports, Letters, NCR (already aggregated)
4. **What's already mirrored** — explicit list so user verifies completeness
5. **Actionable updates table** — file path + one-line change per commit. The
   user picks what to do from this table.

## The five commits produced (in order)

| # | Commit | File updated | New info added |
|---|--------|--------------|----------------|
| 1 | Back-fill MoM 02-13 | `00_Status/meeting_minutes.md` | 11 weekly progress meetings with key points per section + cross-Meeting trend table |
| 2 | Enrich SI register | `01_Registers/si_register.md` | 17-row cross-check table from bank, expanded descriptions for 6 critical SIs |
| 3 | Back-fill MA cross-check | `01_Registers/material_submittal_register.md` | Per-MA folder breakdown of artefacts (388 supplier PDFs, sample boards, data sheets), 7 procurement gap callouts |
| 4 | ARCH working-file note | `01_Registers/material_procurement_list.md` | Header warning about ASM_*_ARCH.xlsx (169 rows, 2027 delivery dates post-handover) |
| 5 | Confirm RFI + MS completeness | `01_Registers/rfi_register.md` + `method_statement_register.md` | Single-line cross-check confirming 21 RFIs + 16 MS items match the bank |

## Key findings to watch for in any bank audit

These are recurring patterns in Aseer Museum surveys — flag each one when seen:

1. **Delivery target dates past contract handover.** Schedules with delivery columns
   must be checked: 17 rows = 2027-01-01, 14 rows = 2027-12-03 are all AFTER the
   30-Sep-2026 contract handover. The Excel tracks installation milestones,
   not contract milestones — confirm with Procurement Dept that no procurement
   date falls before Practical Completion.

2. **Submittal ref concentration in single MA.** A package with 13 of 14
   rejections on a single submittal ref (MA-0006 Showcases) means a known
   CG-side problem cascading. Hunt the master register for the root cause.

3. **Submittal-refgaps.** Working files often show items with NO submittal ref
   column filled. If >50% lack a submittal ref, the pipeline isn't flowing —
   procurement warning, not data quality issue.

4. **Status columns uniformly empty.** All rows None on the rightmost
   "actual status" column = the Excel is **planning/structural only**. Declare
   it as a working file. Do NOT overwrite the repo register on first inspection.

5. **Folder name mismatches vs convention.** Bank uses `01-`, `02-`-prefixed
   folder names; some SIs mis-file unrelated documents (NRS Portfolio in
   `02- CLOSED/`, MEP assessment plan in `03- CLOSED/`). Verify each primary
   doc matches the doc ref before extracting.

6. **Bilingual doc dates in Arabic numerals.** CG SI PDFs are bilingual;
   Arabic text doesn't extract cleanly but the English block contains the
   real metadata. Search for the doc ref or status keywords after the Arabic
   header block.

## Mechanics checklist

Before running a bank audit, confirm:

- [ ] `/Volumes/MIcro/.aseer-tmp/text_extracts/<topic>/` exists and is writable
- [ ] pdftotext is on PATH (`which pdftotext`)
- [ ] openpyxl installed (`python3 -c 'import openpyxl'`)
- [ ] Bank root path is captured with raw apostrophes/space handling
- [ ] Repo is clean (commits up to date, no leftover temp files in 09_Agent_Workspace)

After running, always:

- [ ] Delete scratch directory if it contains >50 MB
- [ ] Update each register's `last_updated` frontmatter
- [ ] Confirm 0 PDF binaries in the new commits (`git log --stat | grep '.pdf$'`)
