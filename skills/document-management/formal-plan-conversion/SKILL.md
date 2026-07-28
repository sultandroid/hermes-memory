---
name: formal-plan-conversion
description: Convert approved PDF plans (Code B) to formal read-only markdown in the repo. Covers extraction, structuring, frontmatter, and filing under 00_Contracts/.
tags:
  - document-control
  - pdf-conversion
  - formal-docs
  - read-only
---

# Formal Plan Conversion — PDF to Read-Only Markdown

## Trigger

User says: convert this approved plan to markdown / save as formal reference / add to 00_Contracts/

Or: an NCR/LT audit requires checking the approved DMP, Communication Plan, or other plan — and the plan isn't yet converted in the repo.

## Prerequisites

- `pdftotext` available (macOS: `brew install poppler`)
- Source PDF accessible in OneDrive or local path
- Approval status confirmed from `08_Document_Index/approved_plans.md`

## Step 1 — Locate the Approved PDF

Check `08_Document_Index/key_documents.md` for the OneDrive/archive path. Approved (Code B) plans are listed in `08_Document_Index/approved_plans.md`.

Common locations:
- `OneDrive/.../04_Docs/02_Plans_and_Procedures/{NN}_{Plan_Name}/01_Source_Files/`
- `OneDrive/.../99_Archive/{NN}_{Category}/{Plan_Name}/`

## Step 2 — Extract Text

```bash
pdftotext "SOURCE_PATH" /tmp/{plan_shortname}.txt
```

Check structure with:
```bash
head -80 /tmp/{plan_shortname}.txt
wc -l /tmp/{plan_shortname}.txt
```

For large documents (>2000 lines), delegate to a sub-agent with read instructions.

## Step 3 — Determine Structure

Read the Table of Contents. Identify logical parts/sections. Common patterns:
- Single document with sections → single .md file
- Multi-part document (Parts 1-5) → split into part files + 00_INDEX.md
- DS (Document Submittal) header form → strip before plan body

### For multi-part splits

Create files under `00_Contracts/{NN}_{Plan_Name}/`:
- `00_INDEX.md` — metadata, revision history, TOC
- `01_Part1_{name}.md`
- `02_Part2_{name}.md`
- ... etc.

### For single-file plans

One .md file under `00_Contracts/{NN}_{Plan_Name}/` with the plan name as filename.

## Step 4 — Add YAML Frontmatter

Every file MUST have identical frontmatter:

```yaml
---
doc_ref: MOC-MUS-ASE-XXXX-XX-XXXX
revision: Rev.XX
title: [Plan Title]
status: formal_read_only
last_updated: YYYY-MM-DD
approved_date: YYYY-MM-DD
approved_by: CG (Consultant Group)
approval_code: B (Approved with Comments)
source_file: [relative or full path to original PDF]
agent_edit: prohibited
---
```

For plans with unclear status (e.g., PL-0055 not in approved_plans.md), use `approval_code: TBC` and flag in the INDEX.

## Step 5 — Format the Content

- `#` for document title (use the Plan name)
- `##` for Part headings or major sections
- `###` for numbered sections (matching the original)
- `####` for subsections
- Preserve ALL tables as markdown `|` tables
- Preserve lists, numbered items, and notes verbatim
- For HSE plans with DS header forms: strip from the LAST occurrence of the doc_ref string (not the first), keeping only the plan body
- Preserve form-feed (`\f`) characters as `---` page-break markers only if they separate actual pages, otherwise strip

## Step 6 — Cleanup

- Strip the DS (Document Submittal) header form entirely from extracted text
- Remove Arabic text artifacts from the submittal form (they're not plan content)
- Preserve Arabic content that is PART OF the plan body (tables, notes, bilingual headers)
- For HSE plans: the header form ends at the second/last occurrence of the doc_ref string

## Step 7 — Do NOT Commit

Create files for user review first. Only commit when user says "commit" or "push".

## Numbering Convention

| Contract Folder | Plan Code | Example |
|----------------|-----------|---------|
| `00_Contracts/01_DMP/` | PL-0029 | Design Management Plan |
| `00_Contracts/02_Communication_Plan/` | PL-0018 | Communication Plan |
| `00_Contracts/03_Stakeholder_Plan/` | PL-0020 | Stakeholder Management Plan |
| `00_Contracts/04_NRS_Methodology/` | ZD-0026 | NRS Methodology |
| `00_Contracts/05_HSE_Plans/` | PL-00XX | HSE Plans (numbered by priority) |
| `00_Contracts/06_Correspondence/` | LT-XXX | Warning Letters / Formal Correspondence |

Use sequential numbering for new contract folders. Place the folder number immediately after `00_Contracts/`.

## Pitfalls

- **DS header appears twice**: The doc_ref appears once in the header table (line ~27) and once at the bottom of the header (line ~184-186). Cut at the LAST occurrence, not the first.
- **Form-feed characters**: `\f` from pdftotext are page-break markers. Strip them unless they separate distinct document sections.
- **Arabic text in DS form**: The header form is bilingual Arabic/English. Only the English plan body after the header is needed.
- **OneDrive stub files**: If the PDF is a OneDrive cloud placeholder (shows size but fails zip/read), the file needs to be force-downloaded first. Open in Finder → right-click → "Always keep on this device".
- **Large files**: Documents over 2000 lines need sub-agent delegation. The sub-agent reads in chunks and creates the files.
- **Multiple revisions**: Check `08_Document_Index/approved_plans.md` for which revision is Code B approved. Only convert the approved revision.
- **HSE plans**: 12 plan files exist in OneDrive `Plans_MD/` — only 9 are Code B approved. Skip PL-0036 (C), PL-0037 (C), PL-0040 (D).

## Verification

After creating files, verify:
1. Frontmatter has `agent_edit: prohibited` on every file
2. Frontmatter has `status: formal_read_only`
3. All section files are linked from the INDEX
4. The actual plan content is preserved (compare line count + key sections)
