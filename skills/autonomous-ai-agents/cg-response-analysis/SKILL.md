---
name: cg-response-analysis
description: Extract CG (Consultant) response PDFs, write structured MD analysis files to repo, then present each document to the user one-by-one with Arabic explanations for review before committing.
tags:
  - cg
  - consultant
  - response
  - analysis
  - md
  - review
  - arabic
---

# CG Response Analysis — Aseer Museum

Workflow for processing CG (Consulting Group) response documents from email attachments into structured MD analysis files, with user review.

## Trigger

- User says "read all files convert to md push to repo"
- User says "اقرأ كل المرفقات وحولها إلى MD"
- After email scan extracts CG response PDFs from Outlook
- After routing PDFs to OneDrive

## Step 1 — Identify documents to convert

Priority order:
1. **CG responses** (ZD-* with CG codes A/B/C/D) — most critical
2. **PQ documents** — supplier prequalification knowledge files
3. **Key correspondence** — SI closeouts, GBH letters, SOWs, MOMs
4. **Reports & trackers** — daily reports, design trackers, compliance sheets

## Step 2 — Extract text

For each PDF:
```bash
pdftotext /tmp/email_attachments/<filename> /tmp/<basename>.txt 2>&1
```

Fallbacks if pdftotext fails:
- PyMuPDF (`fitz`) for corrupted xref tables
- pdfminer for stubborn PDFs
- pdfplumber as last resort

If all fail, note "Image-based PDF" or "Corrupted PDF — needs re-sent copy".

## Step 3 — Write MD analysis files

### MD summary format

```markdown
---
last_updated: YYYY-MM-DD
owner_agent: Hermes
status: active
source: <doc ref>
---

# <Doc Ref> — <Title>

**From:** <sender> | **Date:** <date> | **Status:** <CG code if known>

## Summary
Brief description.

## Key Points
- Point 1

## CG Comments (if applicable)
- Comment 1

## Actions Required
- [ ] Action 1
```

### Where to save

| Document type | Repo path |
|---------------|-----------|
| ZD submittals (CG responses) | `03_Plans/02_Stakeholder/CG_Responses/<doc-ref>_analysis.md` |
| DD Gateway (1G-*) | `02_Submittals/01_DD_Gate/{discipline}/<doc-ref>_analysis.md` |
| PQ prequalification | `Technical_Office/Specialist_Management/pq_knowledge/<category>.md` |
| SI (Site Instructions) | `04_Docs/05_SIs/05.1_Issued_by_CG/<doc-ref>_analysis.md` |
| NRS reports | `03_Design_Files/Architecture/NRS_Reports/<doc-ref>_analysis.md` |
| GBH letters | `24_Subcontractors/05_Showcases_Contractor/06_Correspondence/<doc-ref>_analysis.md` |
| SOW documents | `24_Subcontractors/{NN}_{Specialist}/01_Scope_of_Work/<doc-ref>_analysis.md` |
| MOM (Minutes) | `04_Docs/08_Meeting_Minutes/08.1_Weekly_Coordination/<doc-ref>_analysis.md` |
| Daily reports | `00_Status/Daily_Reports/<doc-ref>_analysis.md` |
| Compliance reports | `03_Design_Files/Electrical/Compliance_Reports/<doc-ref>_analysis.md` |
| Design trackers | `04_Docs/09_Registers/01_Design_Deliverables_Tracker/<doc-ref>_analysis.md` |
| Method Statements | `04_Docs/02_Plans_and_Procedures/02.15_Method_Statements/<doc-ref>_analysis.md` |
| Material compliance | `03_Design_Files/FF&E_Material_Boards/<doc-ref>_analysis.md` |

## Step 4 — Present to user ONE BY ONE (CRITICAL)

**Do NOT batch-push all summaries without user review.** The user wants to review each document's content before proceeding.

For each document:
1. Show the document ref + title
2. Give a **brief Arabic explanation** of what the document contains (لازم تشرح المحتوي)
3. State the CG code (A/B/C/D) and what it means
4. List the key CG comments in simple Arabic
5. List the actions required
6. Ask "ما رأيك؟ موافق أستمر للباقي؟" (What do you think? Shall I continue to the next?)

### Arabic explanation template

```
## شرح [Doc Ref] — [Title]

**المرسل:** [sender] | **الحالة:** [CG code]

### عن إيه المستند؟
[2-3 sentences in Arabic explaining what this document is]

### أهم ملاحظات CG:
1. [Comment 1 in Arabic]
2. [Comment 2 in Arabic]

### المطلوب منك:
- [ ] [Action 1]
- [ ] [Action 2]

---

موافق أستمر للوثيقة التالية؟
```

## Step 5 — After user approval

1. `git add -A`
2. `git commit -m "CG response analysis YYYY-MM-DD: N documents processed"`
3. `git checkout -- 06_Risk_System/webapp/src/index.html` (discard auto-generated post-commit file)
4. `git fetch origin && git rebase origin/main` (if remote has new commits)
5. `git push origin main`

## Step 6 — Code C responses: build a CRS and place it BESIDE the CG file

**For any submittal returned Code C (Revise & Resubmit), the user expects a Comment Resolution Sheet (CRS) built from the approved template, placed in the SAME folder as the original CG response PDF** (the `02_CG_Responses/` folder of the relevant plan/discipline). Do NOT put the CRS in a separate `Submission_Plan_CRS/` or `01_Source_Files/` folder.

```
.../02_CG_Responses/MOC-MUS-ASE-1E0-ZD-0102.pdf          ← CG response (Code C)
.../02_CG_Responses/MOC-MUS-ASE-1E0-ZD-0102_CRS_Rev01.xlsx  ← our CRS reply
```

- **Blank CRS template** (approved, reusable): `Technical_Office/Compliance_System/templates/CRS_TEMPLATE_BLANK.xlsx` (repo) / `04_Docs/09_Registers/CRS_Templates/CRS_TEMPLATE_BLANK.xlsx` (OneDrive). See the `compliance-sheet-filling` skill for the full fill pattern and the leftover-comments pitfall.
- **CRS content**: one row per CG comment — `No. | Initial | Sheet | Reviewer Comment | Originator Reply | Reply By | Reply Status`. Reply wording is plain "Accepted"/"Closed" (draft — user reviews before sending to the consultant).
- **Code B** responses do NOT need a CRS — just log the approval.

## Pitfalls

- **Image-based PDFs**: CG comment sheets are often scanned images. `pdftotext` returns empty. Try PyMuPDF fallback, then flag for manual review.
- **Corrupted PDFs**: Some PDFs fail all extraction tools. Flag as "Corrupted — needs re-sent copy".
- **User wants Arabic explanations**: The MD file is in English, but the presentation to the user MUST be in Arabic with clear explanation of each CG comment.
- **One-by-one, not batch**: The user explicitly wants to review each document sequentially. Do not push all at once.
- **CG code meaning**: A=Approved, B=Approved w/comments, C=Revise & Resubmit, D=Rejected. Explain this in Arabic when presenting.
- **Post-commit hook**: The repo auto-regenerates `index.html` after commit. Discard it before push to avoid conflicts.
- **NEVER use `replace_all=true` on a markdown table row that appears multiple times.** When appending new action-item rows to a register (e.g. `00_Status/action_items.md`), a row like `Review Stage 4 Showcase Lighting Package` may appear 2+ times (duplicate entries from prior scans). `replace_all=true` then duplicates the ENTIRE new block at every occurrence, corrupting the file (frontmatter, headers, section titles all get injected rows). Fix: restore from git (`git checkout -- <file>`), then append via a unique anchor — either `cat >> file <<EOF` (write the block to a temp file first to avoid the `&` tool guard) or anchor on a longer unique multi-line context that appears only once. Verify with `tail` after appending.
- **OneDrive EDEADLK on cloud-placeholder files — hydration requires Finder/Preview, not `brctl`.** `brctl download` fails on OneDrive paths ("Path is outside of any CloudDocs app library") — it only works for iCloud. `open` in Finder/Preview triggers hydration but may not finish within a short wait; the file stays locked (Errno 11 Resource deadlock avoided) until OneDrive downloads it. Reliable path: `open` the file/folder in Finder, ask the user to double-click it so OneDrive hydrates (cloud icon → checkmark), then retry. Do NOT keep retrying `cp`/`file`/`pdftotext` on a locked file.
