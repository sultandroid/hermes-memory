# Contract Document → Structured Markdown — DMP Rev C04 Conversion (2026-07-28)

## Source

- Source file: `/tmp/dmp_full.txt` (11,660 lines, 205KB) — pdftotext extraction of DMP Rev C04 PDF
- Original: `MOC-MUS-ASE-1K0-PL-0029` — Design Management Plan, Rev.02/C04, 52 pages
- Target: `~/aseer-museum-pm/00_Contracts/01_DMP/`

## Chunk-Reading Strategy

The text file was read in 200-500 line chunks across 15+ calls. The pattern:

1. First 3 calls at 200-300 lines each to understand overall structure (TOC, page layout, section boundaries)
2. Then larger chunks (300-500 lines) to cover the bulk of sections 3-10
3. Final chunks (500-600 lines) for the remaining sections 11-16
4. One final 360-line chunk to read the tail (appendices, last pages, colophon)

**Key:** Do not read sequentially through all 11,660 lines before starting to write. Read enough to build a mental map of the document structure (first ~20% of lines), then read targeted chunks when you reach each section.

## Structure Discovery

The document had these natural split points discovered during reading:

| Part | Sections | Pages | Content |
|---|---|---|---|
| Part 1 | 1-4 | 3-12 | Document Control, Purpose, Project Overview, RIBA, Standards |
| Part 2 | 5 | 13-17 | Org Chart, Design Team, RACI, Stakeholders |
| Part 3 | 6 | 18-32 | Design Process, Stage Gates, Submittals, VE, NCR, Discipline Strategies |
| Part 4 | 7-9 | 33-37 | BIM, QA/QC, Interface Management |
| Part 5 | 10-16 | 38-52 | Programme, Deliverables, Risk, KPIs, Appendices |

Page boundaries discovered via `\f` characters in the text (form feed = new page). Each page had a header pattern: `DOC PAGE X OF 52` + `Aseer Museum | DMP Rev C04 | Samaya Investment`.

## Table Reconstruction Examples

### RACI Matrix (5 columns × 31 rows)

Extracted text showed: `# \n ACTIVITY \n SAMAYA \n NRS \n CG \n PMC \n MOC`
Each activity was a separate block. Reconstructed as:
```markdown
| # | ACTIVITY | SAMAYA | NRS | CG | PMC | MOC |
|---|---|---|---|---|---|---|
| 01 | Pre-S4: Cloud Survey | R | C | A | I | I |
```

### Revision History

Extracted as vertical key-value pairs (REV \n DATE \n DESCRIPTION \n PREPARED \n CHECKED \n STATUS). Reconstructed as a proper table with columns: REV, DATE, DESCRIPTION, PREPARED, CHECKED, STATUS.

### LOD Coverage Check

Extracted as a 3-column pattern: `DISCIPLINE \n LOD RCVD \n LOD REQD`. Reconstructed as a markdown pipe table.

### RACI Qualifiers

Extracted as single-letter codes with multi-line definitions. Used a simple 2-column key-value table:
```markdown
| R | Responsible — performs the work |
| A | Accountable — single sign-off owner |
```

## Frontmatter Template Used

```yaml
---
doc_ref: MOC-MUS-ASE-1K0-PL-0029
revision: Rev.02/C04
title: Design Management Plan — Part N: Description
status: formal_read_only
last_updated: 2026-05-17
approved_date: 2026-05-21
approved_by: CG (Consultant Group)
approval_code: B (Approved with Comments)
source_file: 04_Docs/02_Plans_and_Procedures/02.1_DMP/01_Source_Files/02_PDFs/2026-05-18_DMP_Rev_C04_REV02_NRS_signed.pdf
agent_edit: prohibited
---
```

## File Breakdown

| File | Size | Lines | Sections |
|---|---|---|---|
| `00_INDEX.md` | 6.4 KB | 165 | Cover, metadata, revision history, TOC |
| `01_Part1_Understanding_the_Project.md` | 40.7 KB | 572 | Sec 1-4 (Document Control, Purpose, Project Overview, Standards) |
| `02_Part2_Governance_and_Team.md` | 18.9 KB | 248 | Sec 5 (Org, RACI, Stakeholders) |
| `03_Part3_Managing_the_Design.md` | 35.0 KB | 639 | Sec 6 (Process, Gates, Submittals, VE, NCR, Discipline Strategies) |
| `04_Part4_Information_Quality_Interfaces.md` | 20.2 KB | 328 | Sec 7-9 (BIM, QA/QC, Interface Mgmt) |
| `05_Part5_Delivery_Risk_Performance.md` | 34.5 KB | 629 | Sec 10-16 (Programme, Deliverables, Risk, KPIs, Appendices) |

## Handling Cover-Sheet-Only PDFs

When the source PDF is a **single-page DS submittal transmittal cover** (not the actual document), the real content is in one of these fallback locations — check them before concluding the document is missing:

### Discovery Order

1. **`99_Archive/`** — search for `*ZD-0026*OLD_VARIANT*` or `*_OLD_*` patterns. Archived PDFs often contain the actual CG comment sheet that was attached to the cover but not merged into the main PDF.
2. **`02_CG_Responses/`** — CG response PDFs and summaries may contain distilled version of the comments even if the main source is absent.
3. **`03_Plans/<category>/`** — pre-existing markdown analysis files; the repo may already have plan summaries, checklists, or approval logs.
4. **`reference/`** — PMBOK reference docs (e.g., `ref_NRS_Methodology.md`) document known scope and PMBOK mapping even when the source plan is not on disk.
5. **Cross-references in DMP, BEP, Stakeholder Plan** — search the repo for the document ref (e.g., `ZD-0026`) to find every mention. These citations reveal the document's scope, approval status, and role in the project governance.

### CG Comment Sheet Extraction (from OLD_VARIANT PDFs)

`_OLD_VARIANT.pdf` PDFs in `99_Archive/` often contain the CG comment sheet. Extract with pdftotext:

```bash
pdftotext -layout /path/to/OLD_VARIANT.pdf /tmp/comments.txt
```

These are typically **Arabic-only**. Present them bilinqually in the formal markdown:

```markdown
### Comment N: Domain in Arabic (نطاق العمل بالعربية)

**Status:** ⚠ Condition

> Arabic original text here

**English translation (equivalent):**
> Translation of the Arabic comment

**Implication:** Concrete action required to close this condition.
```

**CG signatories** are often listed at the bottom of the OLD_VARIANT PDF — extract their full names and titles.

Common comment domains (translated from Arabic):

| Arabic Domain | English Equivalent |
|---|---|
| نطاق العمل والتصميم | Scope of Work and Design |
| الهيكل التنظيمي والأدوار | Organisational Structure and Roles |
| آلية العمل والمراجعة | Work and Review Mechanism |
| الجداول الزمنية والمخرجات المطلوبة | Schedules and Required Deliverables |

### Documenting Missing Source Content

When the actual plan document is not on disk, the markdown must be **transparent** about this:

1. Add a yellow-bordered metadata table at the top of the INDEX file clearly showing what is/isn't on disk
2. List the exact action items needed (e.g., "Request full methodology source from NRS — file to: `01_Source_Files/PDFs/MOC-...`")
3. Reconstruct **known scope** from cross-references found in other documents — cite every source
4. Add an **"Anticipated Contents"** section listing the expected section structure (from PMBOK reference docs or standard templates) so future agents know what to populate when the source arrives
5. Cross-reference the document in all affected registers/plans even in its partial state — Code B approval makes it citable

## Verification Checklist

- [ ] All frontmatter fields present and correct on every file
- [ ] `status: formal_read_only` and `agent_edit: prohibited` on all contract docs
- [ ] Index file navigation links (TOC) point to the correct part files
- [ ] All tables that existed in the original are present in markdown
- [ ] No content was added, summarized, or interpreted — verbatim transcription
- [ ] Page markers (`DOC PAGE X OF Y`) retained in section headers
- [ ] Workflow diagrams rendered as ASCII flow charts with arrows
- [ ] RACI matrices rebuilt correctly from vertical-key-value to pipe tables
- [ ] Risk registers and KPI tables fully represented
- [ ] Appendices A-BB indexed with status codes and locations
- [ ] **Cover-sheet-only check**: if source PDF was <2 pages, discovered fallback content (archive, CG responses, repo analysis, cross-references)
- [ ] **Missing-source transparency**: if source document still not found, clearly flagged with actionable next steps
- [ ] **CG comments bilingual**: Arabic original preserved alongside English translation
- [ ] **Cross-references updated**: repo-wide search for the doc ref performed to identify every citation
