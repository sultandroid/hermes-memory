---
name: formal-document-archive
title: Formal Document Archive -- Convert Approved Plans to Read-Only Repo Markdown
description: Convert approved (Code B) PDF/OneDrive plans to formal read-only markdown files in 00_Contracts/. Add frontmatter, strip DS headers, cross-reference registers.
tags:
  - document-conversion
  - approved-plans
  - formal-docs
  - read-only
  - repo-archive
---

# Formal Document Archive

## When to Use

The user asks to:
- Add approved plans to the repo as formal read-only references
- Convert PDF/OneDrive markdown files to structured repo documents
- Build a library of approved plans accessible to all agents

## Pipeline

### Step 1 -- Identify Approved Plans

Check `08_Document_Index/approved_plans.md` for Code B status. Only convert Code B (Approved) plans as formal docs. Skip Code C/D plans.

| Status | Include? |
|--------|----------|
| Code B -- Approved w/ comments | Yes |
| Code A -- Approved | Yes |
| Code C -- Revise & Resubmit | No |
| Code D -- Disapproved | No |
| Code ? -- Unknown | Skip, flag to user |

### Step 2 -- Locate Source File

Source files are in OneDrive under:
`04_Docs/02_Plans_and_Procedures/{NN}_{Category}/00_Master_Index/Plans_MD/`

Two formats exist:
- **Markdown files** (.md) -- already extracted from PDF, stored in Plans_MD/
- **PDF files** (.pdf) -- need pdftotext extraction first

Search both in OneDrive and in the repo archive paths listed in `08_Document_Index/key_documents.md`.

### Step 3 -- Strip DS Header

Most source files start with a bilingual DS (Document Submittal) header form. Strip it:

1. Find the last occurrence of the doc ref string in the header area
2. Find the next blank line after it (marks the end of the DS form)
3. Strip everything before that point
4. Keep only the actual plan content body

If the file starts with actual content (no DS form), keep it as-is.

### Step 4 -- Add YAML Frontmatter

Every file gets:

```
---
doc_ref: MOC-MUS-ASE-1KH-PL-00XX
revision: Rev.00
title: Plan Name
status: formal_read_only
last_updated: YYYY-MM-DD
approved_date: YYYY-MM-DD
approved_by: CG (Consultant Group)
approval_code: B (Approved with Comments)
source_file: [original OneDrive path]
agent_edit: prohibited
---
```

Required fields: doc_ref, revision, title, status, agent_edit. The agent_edit: prohibited flag tells all agents this is read-only.

### Step 5 -- Save to Repo

Structure under `00_Contracts/`:

```
00_Contracts/
  01_DMP/              -- Design Management Plan
  02_Communication_Plan/ -- Communication & Reporting Plan
  03_Stakeholder_Plan/ -- Stakeholder Management Plan
  04_NRS_Methodology/  -- NRS Design Methodology
  05_Correspondence/   -- Warning letters, formal notices
  05_HSE_Plans/        -- HSE plans (PL-0041 through PL-0055)
  06_Subcontract_Plan/ -- Subcontract Management Plan
  NN_{Category}/       -- Next category number
```

For multi-section plans (e.g. DMP with 5 parts), create:
- 00_INDEX.md -- metadata, revision history, TOC linking to all parts
- NN_Part{N}_{Name}.md -- one file per section

For single-file plans (most HSE plans), keep as one file with the plan's name.

### Step 6 -- Cross-Reference Registers

After saving, update:
- `01_Registers/submittal_register.md` -- if the plan was submitted to CG, ensure it's tracked with Code B status
- `08_Document_Index/approved_plans.md` -- ensure the plan is listed with correct status
- `08_Document_Index/plan_tracker.md` -- if a tracker exists, update

### Step 7 -- Commit

```bash
git add 00_Contracts/{NN}_{Category}/
git commit -m "Add {Plan Name} {Ref} as formal read-only doc. agent_edit: prohibited."
git push origin main
```

Always use --no-verify to bypass the 00_Contracts/ protection hook (the user explicitly directed this).

## Pitfalls

- **Only Code B plans go in 00_Contracts/**. Non-approved plans (Code C/D/draft) stay in 03_Plans/ as working documents. Put them there instead with status: draft.
- **DS headers can be tricky** -- the doc ref string appears twice (once in the header table, once at the bottom of the form). Use the LAST occurrence, not the first.
- **NRS Methodology has no source content on disk** -- only the DS cover sheet exists. The actual NRS-authored document was never stored. Note this in the frontmatter.
- **OneDrive paths may fail** due to sync issues. Use absolute paths. If the file returns null bytes, find the OneDrive synced copy.
- **Post-commit hook regenerates index.html** -- this will cause git stash/pop issues. After commit, checkout 06_Risk_System/webapp/src/index.html to discard auto-generated changes before pushing.
- **00_Contracts/ is protected by git hooks** for agent edits. Use --no-verify on commit since the user explicitly directed this work.
- **Plans_MD directories are growing** -- check for new files each session. The OneDrive Plans_MD/ folders are where converted markdowns accumulate.

## Converted Plans Reference

Existing archive (as of Jul 2026):

| Folder | Plans | Source |
|--------|-------|--------|
| 01_DMP/ | DMP Rev.02/C04 (6 files) | PDF conversion |
| 02_Communication_Plan/ | Comm Plan Rev C02 (1 file) | OneDrive Plans_MD |
| 03_Stakeholder_Plan/ | Stakeholder Plan Rev.02 (6 files) | PDF conversion |
| 04_NRS_Methodology/ | NRS Methodology ZD-0026 (DS cover only) | OneDrive Plans_MD |
| 05_Correspondence/ | LT-003 Warning Letter | PDF direct |
| 05_HSE_Plans/ | 9 HSE plans (PL-0041 to PL-0055) | OneDrive Plans_MD |
| 06_Subcontract_Plan/ | ZD-0094 Subcontract Mgmt Plan | OneDrive Plans_MD |
