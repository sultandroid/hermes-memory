# Worked Example: SMP Rev.02 -> 00_Contracts/03_Stakeholder_Plan/

## Source

- **Document**: Stakeholder Management Plan Rev.02 (MOC-MUS-ASE-1K0-PL-0020)
- **Status**: Code B (Approved with Comments), approved 2026-06-22
- **Original**: PDF, 23 pages, 15 sections, 56 stakeholder roles
- **Source path**: `04_Docs/02_Plans_and_Procedures/02.13_Stakeholder_Plan/01_Source_Files/02_PDFs/`

## Target

- **Folder**: `00_Contracts/03_Stakeholder_Plan/`
- **6 files**: 1 index + 5 part files (1279 lines total)
- **All with frontmatter**: `agent_edit: prohibited`, `status: formal_read_only`

## File Structure

| File | Lines | Content |
|------|-------|---------|
| `00_INDEX.md` | 111 | Cover page, metadata, revision history, TOC, plan snapshot |
| `01_Part1_Foundation_and_Governance.md` | 197 | Sections 1-2: Document Control, CG Disposition (25 comments), Purpose, Scope, Definitions |
| `02_Part2_Identification_and_Register.md` | 269 | Sections 3-4: Identification methodology, full 56-role register across all tiers |
| `03_Part3_Analysis_and_Strategy.md` | 178 | Sections 5-7: P/I Matrix, Salience, Influence/Impact, Engagement Gap, Quadrant Strategy, Cultural |
| `04_Part4_Execution_Framework.md` | 258 | Sections 8-11: Communication Plan (5 channels, 7 reports, 11 meetings), RACI 10x7, 14 Interfaces, Escalation 5-tier/8-trigger |
| `05_Part5_Performance_and_Closeout.md` | 266 | Sections 12-15: 10 KPIs, PDCA, POE, Change Management, Visual Tools, Compliance, Sign-off |

## Frontmatter Template

```yaml
---
doc_ref: MOC-MUS-ASE-1K0-PL-0020
revision: Rev.02
title: Stakeholder Management Plan
status: formal_read_only
last_updated: 2026-06-16
approved_date: 2026-06-22
approved_by: CG (Consultant Group)
approval_code: B (Approved with Comments)
source_file: 04_Docs/02_Plans_and_Procedures/02.13_Stakeholder_Plan/01_Source_Files/02_PDFs/Aseer Museum · Stakeholder Management Plan · Rev 02.pdf
agent_edit: prohibited
---
```

Part files add:
```yaml
part: 4
sections: 8-11
original_pages: 14-18
```

## Conversion Steps

1. **Extract PDF text**: `pdftotext "/path/to.pdf" /tmp/smp.txt` -> 6129 lines, 78KB
2. **Read in chunks**: 200-line reads + 1000-line reads to capture all content
3. **Check existing pattern**: Found `00_Contracts/01_DMP/` files for frontmatter, naming, part structure
4. **Map document structure**: 5 parts, 15 sections, TOC-driven split
5. **Write files**: One per part, preserving all tables, scores, registers, and metadata
6. **Verify**: All 6 files checked for correct `agent_edit: prohibited` and `status: formal_read_only`

## Key Decisions

- Used `00_Contracts/03_Stakeholder_Plan/` not `03_Plans/02_Stakeholder/` because this is the formal approved archive
- Folder named `03_Stakeholder_Plan` (not `02_Stakeholder`) to match parent numbering: 01_DMP, 03_Stakeholder_Plan (02 likely reserved for future PEP)
- Part boundaries follow the document's own Part structure (5 parts, matching the TOC)
- CG disposition matrix: all 25 comments (R1+R2) captured, not compressed
- Tables: every register entry, scoring convention, KPI, and interface row preserved from the PDF

## AGENTS.md Rule 9

The project `AGENTS.md` explicitly prohibits agents from creating/modifying files in `00_Contracts/`. This conversion proceeded because the user explicitly directed it. Future agents must not assume blanket permission.
