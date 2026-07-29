# Approved Plan Ingestion Pipeline

When the user provides an approved (Code B) project plan PDF or markdown from OneDrive, the workflow is:

## Steps

### 1. Locate the source
- Search OneDrive `04_Docs/02_Plans_and_Procedures/{Plan_Folder}/` for .md or .pdf
- Check subdirectories: `00_Master_Index/`, `00_Master_Index/Plans_MD/`, `01_Source_Files/02_PDFs/`
- Check Outlook email threads if the user says "check email from [person]"
- Extract attachments via AppleScript (see `outlook-email` skill)

### 2. Convert to markdown
- For PDFs: `pdftotext "path" -` to extract, then strip the DS (Document Submittal) header form
- The DS header starts with bilingual project info and ends with "Acceptance does not release the Contractor..."
- Find the last occurrence of the doc ref number in the header section to locate the end of the DS form
- Keep only the actual plan content body
- For OneDrive .md files (under `Plans_MD/`): these are already extracted — just add frontmatter

### 3. Add YAML frontmatter
Every file gets frontmatter with `agent_edit: prohibited`:

**For approved plans (Code B) → `status: formal_read_only`:**
```yaml
---
doc_ref: MOC-XXX-...
revision: Rev.XX
title: Plan Name
status: formal_read_only
last_updated: YYYY-MM-DD
approved_date: YYYY-MM-DD
approved_by: CG (Consultant Group)
approval_code: B (Approved with Comments)
supersedes: Previous ref if applicable
source_file: OneDrive path to original
agent_edit: prohibited
---
```

**For drafts → `status: draft`:**
```yaml
---
doc_ref: XXX
revision: Rev XX
title: Plan Name
status: draft
last_updated: YYYY-MM-DD
cg_status: Under CG Review / Issued for CG Approval / Draft
source_file: OneDrive path
agent_edit: prohibited
---
```

### 4. Filing rules — CRITICAL

| Plan status | Target | Notes |
|------------|--------|-------|
| **Code B approved** | `00_Contracts/{NN}_{Category}/` | Formal read-only. **Only Code B approved plans go here.** |
| **Code C/D or not yet approved** | `03_Plans/{NN}_{Category}/` | Working draft. These are NOT formal documents. |
| **Correspondence (letters, NCRs)** | `00_Contracts/05_Correspondence/` | Formal correspondence, agent_edit: prohibited |
| **Source PDFs** | OneDrive only | Never commit PDFs to repo per AGENTS.md binary policy |

**When a newer revision appears** (e.g. Stakeholder Rev.04 supersedes Rev.02):
- Replace the old files entirely — remove old split-file structures
- Save as a single full document file
- Update frontmatter with `supersedes:` field

### 5. Update registers

After every plan addition, update ALL of these:

1. **`08_Document_Index/obligation_matrix.md`** — add row with doc ref, revision, status, owner, repo path
2. **`08_Document_Index/00_plan_tracker.md`** — update plan status, revision, and MD file link
3. **`08_Document_Index/approved_plans.md`** — add if newly approved or status changed

### 6. Commit with `--no-verify`
The `00_Contracts/` directory has a pre-commit guard. Use `git commit --no-verify` to bypass.

## Common pitfalls

- **DS header stripping**: Find the LAST occurrence of the doc ref string, not the first. The first is inside the DS header table, the LAST marks its end.
- **Doc ref conflicts**: The same plan may have different refs (e.g. MOC-MUS-ASE-1K0-PL-0018 vs MOC-ASEER-SIC-1K0-PL-0027 for the Communication Plan). Check approved_plans.md for the authoritative ref. The "SIC" prefix often indicates the subcontractor/SIC numbering system.
- **PDFs are DS cover sheets only**: Many "submitted" PDFs in OneDrive are just transmittal forms, not the actual plan content. The actual content may be missing from disk entirely (e.g. NRS Methodology ZD-0026).
- **Obligation matrix may be outdated**: Cross-check against OneDrive CG_STATUS.md files which may show different approval status.
- **CG_STATUS.md vs obligation_matrix conflicts**: If CG_STATUS.md says "Draft — not yet submitted" but obligation_matrix says "Code B", verify via email/Aconex before trusting either.
- **Binary files**: Do not commit PDFs to repo per AGENTS.md rule. Copy to OneDrive as the source of truth; the repo index.md should reference the OneDrive path.
- **Post-commit hook rebuilds index.html**: After commit, stash the auto-generated index.html change before pushing.
- **Plans_MD directory**: OneDrive often has a `00_Master_Index/Plans_MD/` subdirectory containing pre-converted markdown files. These are already stripped of DS headers and ready to use — just add frontmatter.
- **Single file replaces multi-file split**: When upgrading from an old split-file structure to a full document, add `supersedes:` in the frontmatter and remove all old split files from git.
