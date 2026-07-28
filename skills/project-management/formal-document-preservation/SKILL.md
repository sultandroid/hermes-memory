---
name: formal-document-preservation
title: Formal Document Preservation
description: "Convert approved formal project documents from PDF to well-structured markdown, split into logical sections, indexed, and saved with formal_read_only status and agent_edit: prohibited frontmatter."
tags:
  - pdf
  - markdown
  - conversion
  - formal-document
  - contract
  - read-only
---

# Formal Document Preservation — PDF to Read-Only Markdown

## When to Use

- User says "convert this plan to md and save in repo as read-only"
- User says "we should have all full approved plan like this read only for all agents"
- Adding a CG-approved management plan (Code B) as permanent agent reference
- Converting any formal project document (letter, instruction, report) for agent reference

## Workflow

### Step 1: Locate the Source PDF

Approved plans are typically in OneDrive under:
`04_Docs/02_Plans_and_Procedures/{NN}.{Plan_Name}/01_Source_Files/`

Or in the repo archive at `99_Archive/01_Integration_Management/...`

Search with:
```bash
find ".../OneDrive.../Aseer-Museum/04_Docs/02_Plans_and_Procedures" -name "*.pdf" | grep -i "keyword"
```

Check `08_Document_Index/key_documents.md` for known paths.

### Step 2: Extract Text

```bash
pdftotext "path/to/document.pdf" /tmp/doc_output.txt
wc -l /tmp/doc_output.txt
```

Read first 200 lines to understand structure (TOC, sections).

### Step 3: Identify Document Structure

From the TOC, identify:
- Parts / Chapters / Sections
- Number of logical divisions
- Any appendices or annexes

Create a split plan before writing:
- `00_INDEX.md` — cover, metadata, revision history, TOC with links
- `01_Part1_...`, `02_Part2_...`, etc. — one per major section

### Step 4: Read in Chunks and Write

Read `/tmp/doc_output.txt` in 200-line chunks via `read_file` with `offset`/`limit`. For each chunk:

1. Identify section boundaries
2. Write to the appropriate part file
3. Heading hierarchy:
   - `#` — title (INDEX only)
   - `##` — Part headings
   - `###` — Section numbers (e.g. `### 3.4 RIBA Plan of Work`)
   - `####` — Subsections
4. Preserve tables as markdown `|` tables
5. Preserve lists (numbered and bulleted)
6. Use `>` for quotations or notes
7. Preserve ALL original content — no summarising, paraphrasing, or interpreting

### Step 5: Create the Index File

00_INDEX.md structure:
- YAML frontmatter with full metadata
- Document title and revision info
- Document metadata table
- Revision history table
- Table of Contents linking to all part files

### Step 6: Frontmatter Template (EVERY file)

```yaml
---
doc_ref: {DOC-REF}
revision: {REV}
title: "{DOC TITLE} — {Part Name}"
status: formal_read_only
last_updated: {DATE}
approved_date: {CG_APPROVAL_DATE}
approved_by: CG (Consultant Group)
approval_code: B (Approved with Comments)
source_file: {PATH_TO_SOURCE_PDF}
agent_edit: prohibited
---
```

- `agent_edit: prohibited` — mandatory on every file
- `status: formal_read_only` — mandatory
- `title` should include part name for section files

### Step 7: Repo Location

Save under `00_Contracts/{NN}_{Plan_Name}/`:

| Folder | Content |
|--------|---------|
| `00_Contracts/01_DMP/` | Design Management Plan PL-0029 |
| `00_Contracts/02_Communication_Plan/` | Communication Plan PL-0018 |
| `00_Contracts/03_Stakeholder_Plan/` | Stakeholder Plan PL-0020 |
| `00_Contracts/04_NRS_Methodology/` | NRS Methodology ZD-0026 |
| `00_Contracts/05_Correspondence/` | Letters, NCRs, formal notices |

Correspondence uses descriptive filenames like `LT-003_Warning_Letter_Material_Approval.md`.

### Step 8: User Review Before Commit

Create files for review first. The user says "commit" when ready:

```bash
cd ~/aseer-museum-pm
git add 00_Contracts/{NN}_{Plan_Name}/
git commit -m "Add {Plan Name} {Rev} as formal read-only reference (Code B). {N} files." --no-verify
git push origin main
```

Note: `00_Contracts/` is protected by AGENTS.md Rule 9. Use `--no-verify` when user explicitly instructs the write.

## Delegation Pattern

For large documents (100+ pages), delegate to a sub-agent:

```python
delegate_task(
    goal="Convert {Plan Name} PDF to formal read-only markdown in 00_Contracts/{NN}_{Plan_Name}/",
    context="""PDF PATH: {path}
DOC METADATA:
- doc_ref: {ref}
- revision: {rev}
- title: {title}
- status: formal_read_only
- approved_date: {date}
- approved_by: CG
- approval_code: B
- agent_edit: prohibited

INSTRUCTIONS:
1. pdftotext the PDF to /tmp/doc.txt
2. Read chunks, preserve ALL content
3. Split into 00_INDEX.md + Part files
4. Every file gets frontmatter with agent_edit: prohibited
5. Do NOT commit — create for review
"""
)
```

## Pitfalls

- **Do NOT commit to 00_Contracts/ without user instruction.** AGENTS.md Rule 9 marks it read-only.
- **Do NOT copy existing analysis files** — the repo already has summaries under 03_Plans/ or 08_Document_Index/. The preservation goes in 00_Contracts/.
- **Check if the PDF is the full document** — some are 1-page DS cover sheets only. Flag gaps.
- **Large PDFs** — delegate to sub-agent. A single part file should not exceed 50 KB.
- **Arabic text** — pdftotext may garble Arabic. Note in index, preserve original PDF path.
- **`\f` (form feed)** — replace with `---` or section breaks.
- **`title` field value with colons** — quote the whole value in YAML frontmatter to avoid parse errors.
