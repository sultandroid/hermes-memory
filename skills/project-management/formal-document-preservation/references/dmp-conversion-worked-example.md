# DMP Conversion Worked Example

Source: DMP Rev.02/C04 PDF (11,660 lines, 205 KB after pdftotext)
Output: 6 files, 156 KB total, 2,581 lines

## Structure

The DMP had 5 parts covering 16 sections:

| File | Size | Content |
|------|------|---------|
| 00_INDEX.md | 6.4 KB | Cover, metadata, revision history, TOC |
| 01_Part1_Understanding_the_Project.md | 41 KB | Sections 1-4 (Document Control, Purpose, Scope, RIBA, Standards) |
| 02_Part2_Governance_and_Team.md | 19 KB | Section 5 (Org chart, Design Team, RACI, Stakeholders) |
| 03_Part3_Managing_the_Design.md | 35 KB | Section 6 (Process, Gates, VE, NCR, submittals, disciplines) |
| 04_Part4_Information_Quality_Interfaces.md | 20 KB | Sections 7-9 (BIM, QA/QC, Interface Management) |
| 05_Part5_Delivery_Risk_Performance.md | 34 KB | Sections 10-16 (Programme, deliverables, risk, KPI, appendices) |

## Delegation Prompt Used

The conversion was delegated to a sub-agent with this prompt structure:

```
TASK: Convert this approved PDF plan to markdown and save to the repo as a formal read-only document.

PDF PATH: {full_path}

REPO: /Users/mohamedessa/aseer-museum-pm

DOC METADATA:
- doc_ref: {ref}
- revision: {rev}
- title: {title}
- status: formal_read_only
- approved_date: {date}
- approved_by: CG
- approval_code: B
- source_file: {path}
- agent_edit: prohibited

OUTPUT: Create files under 00_Contracts/{NN}_{Name}/
- 00_INDEX.md with metadata, revision history, TOC
- Section files splitting into logical parts

INSTRUCTIONS:
1. pdftotext the PDF
2. Read full text in chunks
3. Create markdown preserving ALL original content
4. Every file gets YAML frontmatter with agent_edit: prohibited
5. Do NOT commit — just create files for review
```

## Key Decisions

- Used `pdftotext` (not `pdfminer` or `pypdf`) — best text extraction for structured documents
- Split by Parts (major divisions), not individual sections — keeps file count manageable
- Each part file got its own YAML frontmatter with distinct title
- Index file included revision history and page numbers from original PDF
- TOC in index linked directly to part files with relative paths

## Files Created

All under `/Users/mohamedessa/aseer-museum-pm/00_Contracts/01_DMP/`
