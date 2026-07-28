# HSE Plan Batch Conversion — Pre-Converted MD with DS Headers

Batch conversion of 12 HSE plan markdown files from OneDrive Plans_MD directory to formal read-only documents in `00_Contracts/05_HSE_Plans/`.

## Source Location

```
OneDrive: .../02.5_HSE_Plan/00_Master_Index/Plans_MD/
Files: 01_PL-0036 through 12_PL-0055
```

## Selection Criteria

Only Code B (approved) plans should be added to `00_Contracts/`. Check `approved_plans.md` for status:

| Code | Action |
|------|--------|
| **B** (Approved) | Convert and add to repo |
| **C** (Revise & Resubmit) | Skip — not yet approved |
| **D** (Rejected) | Skip |

## DS Header Stripping

Each file starts with a bilingual Document Submittal form (~184 lines) that must be removed:

1. Read the file content
2. Find all occurrences of the doc ref (e.g., `MOC-MUS-ASE-1KH-PL-0041`)
3. The **last** occurrence marks the end of the DS form
4. Strip everything from start through the last doc ref line
5. The remaining content is the actual plan body

**Pitfall — two doc ref occurrences:** The first is in the DS header table (~line 27), the second at the bottom of the DS form (~line 184-186). Stripping at the first leaves residual DS content. Always strip at the **last** occurrence.

**Pitfall — Arabic text artifacts:** DS headers contain RTL Arabic/English mixed text that produces garbled UTF-8. These lines should be removed entirely.

**Pitfall — CG comment sheets (PL-0054/0055):** Some files have additional CG comment/review sheets between the DS header and the actual plan content. These should also be stripped — they are not part of the plan document.

## YAML Frontmatter

```yaml
---
doc_ref: MOC-MUS-ASE-1KH-PL-00XX
revision: Rev.00 (or Rev.01)
title: [Plan Name as shown in document]
status: formal_read_only
last_updated: YYYY-MM-DD (from CG approval date)
approved_date: YYYY-MM-DD
approved_by: CG (Consultant Group)
approval_code: B (Approved with Comments)
source_file: [full OneDrive source path]
agent_edit: prohibited
---
```

## Target Directory

```
00_Contracts/05_HSE_Plans/
```

## Parallel Processing

For 9+ plans, dispatch 3 sub-agents (3 plans each) with `delegate_task`. Each sub-agent handles: read → strip → add frontmatter → save.

## Verification

After all files are created:
- Confirm frontmatter present on each file
- Confirm agent_edit: prohibited
- Confirm no residual DS header lines
