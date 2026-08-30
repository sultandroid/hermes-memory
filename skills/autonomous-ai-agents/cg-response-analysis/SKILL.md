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
- **Programmatic fill**: the template's exact cell map (header fields, data-row columns A/B/C/E/J/P/Q, merged ranges E:I / J:O / Q:R, row 11 start) and a ready openpyxl fill script are in `references/crs-template-fill.md`. Use it instead of hand-typing rows. **Formatting is mandatory** — widen columns, auto-calc row heights (never fixed 60px), font 11, color-code status (green=Closed/red=Open), then render-verify via soffice→pdftoppm→vision before delivering. The user bounces the file with "format not good" if you skip this.
- **Spec-stage Code C (evidence timing)**: when CG returns a *specifications* submittal Code C demanding test reports / certificates / warranties / mock-ups, reply that these are MAR / pre-installation stage deliverables, not spec-stage. Embed the criteria into each spec section, commit to evidence at the correct later stage, and request CG agreement to staged delivery. See `references/crs-template-fill.md` for the full argument.

## Step 7 — AUDIT each comment before assigning a reply (do NOT default to "Complied")

**The user's #1 correction on CRS work: never mark every comment "COMPLIED/Closed" by reflex.** Before writing any reply, audit each CG comment against the governing docs and classify it into one of five positions:

| Position | When to use | Evidence to cite |
|---|---|---|
| **Complied** | Comment is a legitimate requirement already in the spec, or a real internal-QA obligation | SoW / ER clause |
| **Not applicable at this stage** (push back) | CG demands a deliverable that belongs to a later stage (test reports, certs, warranties, mock-ups) | SoW §6.11 (product data = IFC-package submittal, "shall not be submitted independently"); SoW §13.12 + ER §2.4.F (mock-ups per Mockups Schedule, construction phase) |
| **Noted** (not a comment) | CG states a principle, not a technical requirement (e.g. "approval does not relieve contractor responsibility", "no variation to price/schedule") | ER §2.4 (design liability stays with Contractor; PMC review = conformance only) |
| **Deferred** | Comment requires a specialist who is NOT yet appointed | specialist_register.md — verify actual appointment status |
| **Open / clarify** | Comment is vague or downstream of an unresolved design (e.g. "display cases suspended until compliant") | link to the unresolved parent submittal (e.g. 1G-0009 Code C) |

**Governing rules to cite (Aseer Museum):**
- ER §2.4 — PMC review is **conformance only, not technical review**; technical review is the Contractor's Designer's job. Design liability stays with Contractor even after "approval".
- ER §E — spec framework = AIA/CSI MasterSpec (so MasterFormat numbering is correct, not a defect).
- SoW §6.9–6.19 — the submittal taxonomy (product data, certs, test reports, design data) and their stage.
- SoW §13.12 — mock-ups/samples/prototypes per the Mockups Schedule.

**Design-authority direction — the lead designer owns the spec, specialists ACHIEVE it (do NOT "defer" specialist-review comments by default).** When CG demands "review by the acoustics/sustainability specialist" on an *architectural specification* submittal, the correct position is usually **"not applicable / wrong direction"**, not merely "deferred until appointed". The governing principle (Aseer, from the approved NRS Methodology `MOC-ASEER-SIC-1A0-ZD-0026` Code B, 05-Apr-2026, single page):
- **Comment 2a** — "Designer Nissen Richards is responsible for architectural and graphic design, while Samaya's Technical Office acts as the central coordinator to integrate work (electrical, mechanical, **acoustics**, and others)." → NRS writes the architectural spec; the specialist provides input to Samaya, not a review of NRS's spec.
- **Comment 3b** — review sequence is "suppliers/technical office → **Samaya review** → **designer (NRS) review** → CG/MoC". There is **no specialist in the spec-review chain**.
- So the correct reply to "specialist must review the architectural spec" is: the lead designer (NRS) sets the performance requirements per room/material; specialists *deliver against* those requirements in their own design packages, not review/approve the architectural spec. The only legitimate specialist feedback is a *feasibility* check (e.g. "NRC 0.90 is unachievable with this ceiling type"), which happens when the specialist is appointed and starts work — not at spec stage.
- This is a stronger position than "Deferred": it says the request is **structurally wrong**, not just premature. Cite ZD-0026 Comment 2a + 3b (page 1) as the approved-methodology evidence. Note ZD-0026 is a single-page PDF; the whole comment set is on page 1.

**CRITICAL — verify specialist appointment status before claiming "appointed".** When a comment says "review by the acoustics/sustainability specialist", do NOT write "reviewed by X (Code B, appointed)" from memory. Read `Technical_Office/Specialist_Management/specialist_register.md` and confirm the actual PQ code + stage. In this session the agent fabricated "TransOrient PQ-0128 Code B, appointed" when the register showed **Code U (conditional), still awaiting CG review** — a factual error in a CG-facing document. The register can also be internally inconsistent (Tier 2 row vs Tier 3 row disagreeing); when it is, flag the conflict and take the conservative reading (not appointed).

**Oddy test scope — NOT universal.** The Oddy test (British Museum conservation test) applies ONLY to materials **inside or adjacent to display voids / in proximity to artifacts** — not to the whole building. Do not treat "Oddy test" as a blanket requirement for all materials. Governing evidence (Aseer):
- ER §6.11 — "All materials proposed for use **within exhibition spaces** must be confirmed as **non-deleterious to museum-grade objects**" (the governing principle: it's about object safety, not building-wide).
- SoW §13.29 — "Oddy testing of **any non pre-approved material** recommended by the Contractor" (narrow: only non-pre-approved materials).
- SoW §8.1 — "Ensure **all proposed materials** have been Oddy tested" (overly broad — read in context with ER §6.11 and SoW §13.29).
- CG's own comment on 1G-0012 S21 was correctly scoped: "Oddy test results ... **for materials used inside display voids**". When CG scopes it correctly, agree; when a comment or your own reply implies Oddy applies to everything, correct it.

## Pitfalls

- **"See attached CRS Sheet" but no CRS attached.** A CG response PDF's DS cover page may say "See attached CRS Sheet" while the email carries only the PDF (no `.xlsx`). Before concluding the comments are missing, list the email's actual attachments via AppleScript (`name of a` + `content type of a`). The comments are then written as plain text section-by-section inside the PDF itself — you have all the comments, just not in CRS-table form. This works in your favour: use your own CRS template to respond. Do not assume a missing CRS sheet means missing comments, and do not burn cycles hunting for a `.xlsx` that was never sent.
- **CG often requests things ALREADY in the NRS spec — read the actual spec section before replying "Complied, we'll add it".** Before writing any "Complied" reply, open the corresponding NRS spec `.docx` (OneDrive `.../DD Specification MasterFormat/<NN - Division>/<NN NN NN - Title>_<NRS-ref>.docx`) and check whether the requested requirement is already there. Example (1G-0012, 01 73 29 Cutting & Patching): CG's 4 comments (no holes >10mm, no rebar cutting, no chasing hollow block, 0.125 joist notch) were ALL already in NRS spec §3.02/3.05/3.07 verbatim — only the 360° photo documentation was genuinely new. Correct reply: "already specified at §3.02.B.2 / §3.05.C / §3.07.E.1 — no revision required", not "we'll add it". This is a recurring CG pattern (requesting what's already written), and it's a strong, defensible CRS position. See `references/cg-comment-audit-classification.md` for the full audit taxonomy and governing-clause table.
- **Always double-check any rated/status register before citing it.** Registers (specialist register, PQ codes, submittal codes) can be internally inconsistent — the same firm listed as "Appointed 🟢" in one tier and "Prequalify 🟡" in another. Never trust a single register row; cross-check the code/status against the actual source doc. This is a standing user directive, not a one-off.
- **Image-based PDFs**: CG comment sheets are often scanned images. `pdftotext` returns empty. Try PyMuPDF fallback, then flag for manual review.
- **Corrupted PDFs**: Some PDFs fail all extraction tools. Flag as "Corrupted — needs re-sent copy".
- **User wants Arabic explanations**: The MD file is in English, but the presentation to the user MUST be in Arabic with clear explanation of each CG comment.
- **One-by-one, not batch**: The user explicitly wants to review each document sequentially. Do not push all at once.
- **CG code meaning**: A=Approved, B=Approved w/comments, C=Revise & Resubmit, D=Rejected. Explain this in Arabic when presenting.
- **Post-commit hook**: The repo auto-regenerates `index.html` after commit. Discard it before push to avoid conflicts.
- **NEVER use `replace_all=true` on a markdown table row that appears multiple times.** When appending new action-item rows to a register (e.g. `00_Status/action_items.md`), a row like `Review Stage 4 Showcase Lighting Package` may appear 2+ times (duplicate entries from prior scans). `replace_all=true` then duplicates the ENTIRE new block at every occurrence, corrupting the file (frontmatter, headers, section titles all get injected rows). Fix: restore from git (`git checkout -- <file>`), then append via a unique anchor — either `cat >> file <<EOF` (write the block to a temp file first to avoid the `&` tool guard) or anchor on a longer unique multi-line context that appears only once. Verify with `tail` after appending.
- **OneDrive EDEADLK on cloud-placeholder files — hydration requires Finder/Preview, not `brctl`.** `brctl download` fails on OneDrive paths ("Path is outside of any CloudDocs app library") — it only works for iCloud. `open` in Finder/Preview triggers hydration but may not finish within a short wait; the file stays locked (Errno 11 Resource deadlock avoided) until OneDrive downloads it. Reliable path: `open` the file/folder in Finder, ask the user to double-click it so OneDrive hydrates (cloud icon → checkmark), then retry. Do NOT keep retrying `cp`/`file`/`pdftotext` on a locked file.
