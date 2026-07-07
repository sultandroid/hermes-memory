---
name: aseer-document-control
description: File Aseer Museum submittals, create analysis sidecars, build subcontractor folders with SCOPE_REQUEST.md, and draft project correspondence with clear responsibility separation.
---

# Aseer Museum — Document Control & Correspondence Workflow

Trigger: user sends a PDF file for the Aseer Museum project or asks to create a subcontractor folder.

## Key reference: Drawing & Discipline Codes

The file `references/aseer-drawing-discipline-codes.md` documents all project-wide conventions: document numbering (MOC-MUS-ASE-1A0-IFC-0005), drawing numbering (MOC-ASEER-SIC-SDW-AR-GA-BF-0001), submittal register codes (AV/NNN, LG/NNN, LS/NNN), specialist codes for BEP forms, the **full BEP Table 30 discipline code set** (AR, ST, ID, HV, EL, etc.), the **BEP Table 24 sheet naming format**, and a **workflow for verifying proposed naming conventions against BEP/ISO 19650 compliance**. Consult this when coding deliverables, filling TIDP/MIDP tables, or checking a numbering system for BEP/ISO 19650 compliance.

The file `references/sow-622-deliverables-packages.md` documents the **SOW §6.22/§2.4 Technical Design Deliverables package structure** — the authoritative mapping of drawing-type packages (GA 1200, Walls 1220, Floor Finishes 1230, Ceilings 1250, Sections 1350/1500, Elevations 1510, Stairs 1550, External 1570, Showcases 1800, Graphics 1850/1860, etc.) to SOW §6.22 items. **DD submission is organized by drawing package type per SOW §6.22, NOT by floor level.** CG requests for "basement priority" or "staggered by floor" contradict this SOW structure. Consult this when building submission schedules, responding to CG schedule requests, or verifying DD package completeness.

The file `references/prequalified-suppliers.md` documents all prequalified suppliers for the Aseer Museum as of 2026-07-04 — a consolidated reference table by discipline with CG status, scope, and notes. Consult this when checking whether a supplier has been prequalified, or when building procurement schedules.

The file `references/review-approval-periods.md` documents all **contractual review and approval periods** with exact source clauses. Use this when building submission schedules, reviewing CG turnaround claims, or calculating submission buffers. Key rules: (1) always cite the exact clause source for each review period, (2) distinguish calendar days vs working days per source, (3) Comm Plan §9.3 Conflict Rule — most stringent provision governs.

The file `references/structural-submission-plan-cg-comments.md` documents the **CG comments on the Structural and Architectural Submission Plans** with full contract-doc cross-reference against the ASG SD Report, Contractor's SOW, and Employer's Requirements. Use this when responding to CG structural/arch comments, updating submission registers, or verifying whether a CG demand is in scope.

---

## 1c. Building Deliverables Submission Schedules

**Trigger:** CG or PMC requests a submission schedule; user asks to build/revise DD or IFC delivery timelines.

### Core Principles

1. **Never simplify deliverable lists.** Every SOW §6.22 line item gets its own row with the full clause reference, complete description, and drawing-type code. Do not collapse multiple SOW items into one row or summarize package types into generic groups. The user corrects this immediately — full contractual detail is required.
2. **Rows = drawing packages by TYPE per SOW §6.22**, not by floor. See `references/sow-622-deliverables-packages.md` for the authoritative mapping.
3. **Review periods must be sourced from approved documents** — never use a blanket "14 days" or assumed period. Each review period column must cite its source (e.g., "14 CD per ER §2.4.A", "14 WD per PL-0027 §7.1"). See `references/review-approval-periods.md` for the full reference table.
4. **Distinguish Calendar Days vs Working Days.** PMC conformance = 14 CD (ER §2.4.A). CG technical review = 14 WD (PL-0027 §7.1). WD = Saturday–Thursday per Comm Plan §2.4. Comm Plan §9.3 Conflict Rule: most stringent provision applies.
5. **DD dates are TBD until NRS confirms** — do not add production dates for others' work.
6. **IFC drawings produced by Samaya Tech Office** (not NRS). Coordination drawings are part of IFC, not a separate package.
7. **Material Submittals are a separate phase** (Project Team scope, not DD).

### SOW §6.22 Reference in Each Row

Every schedule row must include:
- **SOW §6.22 Ref** (e.g., "(i)", "(v)", "(xiv)", or "(ii)" for specifications)
- **Deliverable Description** — full SOW language, not abbreviated
- **Drawing Type Code** (e.g., 1200_GA, 1930/1950_Doors)
- **Review Period** with clause citation per `references/review-approval-periods.md`
- **DMP Milestone** (if applicable — e.g., G-1 Design Development, G-2 IFC Issue)

### openpyxl / File Writing Workaround

**OneDrive Desktop sync causes `cp` and `open` commands to time out.** When writing Excel/schedule files via openpyxl or any script:
1. Write the file to `/tmp/` first
2. Copy from `/tmp/` to `~/Documents/` (NOT `~/Desktop/` — OneDrive sync blocks file operations)
3. `open` from `~/Documents/` location

### Pitfalls

- **Oversimplifying the schedule** — The user explicitly corrected this: "why you simplify?" Every SOW line item must appear as a separate row. A 32-deliverable schedule is appropriate; do not compress it to 10–15 rows.
- **Blanket review periods** — Writing "14 days" without specifying CD/WD and without citing the clause source is wrong. PMC and CG have different review types with different day-count bases.
- **Adding dates for others' work** — DD dates come from NRS. IFC dates come from Samaya Tech Office. Leave DD dates as TBD until NRS confirms.
- **"By floor" framing** — CG may request submission organized by floor level. The SOW §6.22 organizes by drawing TYPE, not floor. This is a documented CG mistake (tracked in memory).
- **Using unapproved documents as authority** — Time Baseline Rev.03 (Code C, not approved) cannot be cited for review periods. Use DMP Rev C04 (Code B), Comm Plan Rev C02 (Code B), and ER §2.4.

---

## 0. Creating New Submittal Folders for Unmatched Doc Types

**Trigger:** A document's type prefix (e.g., `MS-` for Method Statement) has no matching folder under `02_Submittals/`.

### Workflow

1. **Check existing folders** under `02_Submittals/` — they follow the pattern `NN_Name` (e.g., `01_Shop Drawings`, `02_Material Samples`, `03_DD Documents`)
2. **Determine next number** — find the highest `NN` prefix among numbered folders (ignore unnumbered ones like `3.1_ DD Doucments AV`)
3. **Create folder** as `{next_NN:02d}_{Plural_Name}/` (e.g., `08_Method_Statements/`)
4. **File the document** in the new folder
5. **Mirror to Document Control** working copy at `04_Submittals/{Discipline}/` — create the discipline subfolder if it doesn't exist

### Discipline-to-Folder Mapping for Mirror Copy

| Doc Code | Discipline | Mirror Folder |
|----------|-----------|--------------|
| `1C0` | Civil/Structural | `04_Submittals/Structure/` |
| `1A0` | Architecture | `04_Submittals/Architecture/` |
| `1E0` | Electrical | `04_Submittals/Electrical/` |
| `1M0` | Mechanical | `04_Submittals/Mechanical/` |
| `1K0` | General | `04_Submittals/General/` |

### CG Response Mirroring

When a submittal document contains CG comments (Code B/C/D stamped on the cover), file a **separate copy** to `02_CG_Responses/{Discipline}/` in the Doc Control working copy:

1. **Create discipline subfolder** under `02_CG_Responses/` if it doesn't exist (e.g., `Structure/`, `Architecture/`, `General/`)
2. **Copy the PDF** — same file, no modification
3. **Discipline mapping** follows the same table as the mirror copy above

| Doc Code | Discipline | CG Responses Folder |
|----------|-----------|---------------------|
| `1C0` | Civil/Structural | `02_CG_Responses/Structure/` |
| `1A0` | Architecture | `02_CG_Responses/Architecture/` |
| `1E0` | Electrical | `02_CG_Responses/Electrical/` |
| `1M0` | Mechanical | `02_CG_Responses/Mechanical/` |
| `1K0` | General | `02_CG_Responses/General/` |

This is separate from the submittal copy — the CG Responses folder is a quick-reference archive of all CG review outcomes by discipline.

### Pitfalls

- **Don't file MS- documents under Plans & Procedures** — Method Statements are submittals, not plans. They go under `02_Submittals/`, not `02_Plans_and_Procedures/`.
- **Don't assume a folder exists** — check with `ls` or `search_files` before filing. Create if missing.
- **OneDrive BIM path is primary** — always file to OneDrive first, then mirror to Document Control working copy.

## 1. Filing a submitted/returned submittal PDF (Direct file upload)

**Trigger:** User shares a PDF directly (WhatsApp, chat, drag-drop) — not via email.

**Pattern:** `06_PDFs/Submittals/{YYYY-MM-DD}_{DocNo}___{Description}.pdf` + mirror copy to `04_Submittals/`

### Steps
1. **Extract text** from the PDF using `python3 -c "import fitz; doc=fitz.open('{path}'); [print(page.get_text()) for page in doc]"` or `pdftotext`
2. **Identify metadata**: doc number, revision, title, submittal date, approval status (Code A/B/C/D), CG reviewer, CG comments, reference to previous submittals
3. **Copy PDF to canonical location**:
   - Primary: `{project_root}/06_PDFs/Submittals/{YYYY-MM-DD}_{DocNo}___{Description}.pdf`
   - The `04_Submittals/` folder may be unused (empty) — file to `06_PDFs/Submittals/` only, unless existing files confirm `04_Submittals/` is active
   - Use the naming convention established by existing files: `YYYY-MM-DD_{DocNo}___{Description}.pdf` (date prefix + doc code + triple underscore + description)
4. **Update the Submittals Log** (Excel register at `01_Logs_Registers/Asher_Regional_Museum_Logs.xlsx`):
   - Find the next S.No from existing rows (col A)
   - Append a new row with: S.No, Submittal No., Date Submitted, Description, Submittal Type, Specification Section, Submitted By, Reviewed By, Date Returned, Status, Resubmissions, Remarks (summarise CG comments verbatim), Attachment Ref (filename)
   - Use `openpyxl` via system Python 3.13 (not execute_code sandbox)
5. **Create Odoo task** under the Aseer Museum project (ID 219):
   - Determine the right package (usually Procurement 39 / pkg 3146 for submittals, or DD 36 for design-review items)
   - Set stage, assign to relevant user (Sultan Issa ID 151), tag appropriately
   - Copy the CG comments verbatim into the HTML description
   - Log ~0.5 hr session time via `account.analytic.line`
   - Use the `odoo-task-injection` skill for exact API calls
6. **Log to backlog**: Append a row to `Email_Archive/_aseer_tasks_backlog.md` with date, reference, description, action taken, status
7. **Update memory** with doc status + key action items

### Doc Code Naming Conventions
- `1KH-PL` = HSE Plans
- `1KH-ZD` = HSE Design/Methodology
- `1A0-ZD` = Architecture-led Design docs
- `1K0-PL` = Multi-discipline Plans

## 1a. CG Comment Disposition tables — cumulative across rounds

CRP (Communication & Reporting Plan) CG Comment Disposition tables must track ALL review rounds, not just the current one. Add a **Round** column to distinguish Rev.00 comments from Rev.01/Code C, etc. Future rounds append to the same table — never replace it with only the current round's comments.

### Table structure for cumulative disposition (HTML)

Use `cat-row` section dividers to group rounds. Each round divider gets a `colspan` across all columns (5 columns for summary page, 4 for detailed). Add round badges per row using existing CSS classes:
- `badge badge-high` = Rev.00 (amber)
- `badge badge-critical` = Code C (red)
- `badge badge-info` = Code B / Approved as Noted (blue)
- `badge badge-pass` = Code A / Approved (green)

### Handling CG review rounds

CG comments may arrive in different formats — identify the format before extracting:

| Format | Where to Find | Extraction Method |
|--------|--------------|-------------------|
| **Formal DS Reply** (Standard CG review form with Code A/B/C/D stamp) | `02_CG_Responses/` as `{DocNo}_CG_Reply_Code*.pdf` or `{DocNo} REPLY.pdf` | `pdftotext "{path}" - 2>/dev/null` — CG comments appear after "CG Comments:" or "ملاحظات المهندس المشرف" |
| **Email with attached directive** (CG sends a document/workbook as the review outcome, e.g. Roadmap for Rev.00) | May be in `02_CG_Responses/` as a separately downloaded file, or referenced in email archives | Extract via `pdftotext`. The email body often contains the context/framing; the attachment is the actual requirement. **The attachment IS the comment** — it's not just a reference document. |
| **Embedded in sidecar analysis** | `*_Reply_Analysis.md` or `*_STATUS.md` files | Useful for quick reference but **not authoritative** — always verify against the actual CG reply PDF. Sidecars can be premature or incorrect. |

### Flow for processing a new CG review round

1. Find the CG reply document in `02_CG_Responses/` — the user typically downloads it there
2. Extract full text with `pdftotext` — don't rely on sidecar files alone
3. Identify the round's review code (Code A/B/C/D) and the CG reviewer
4. List each comment verbatim — note comments that reference previous round comments (e.g., "address all comments from REV00")
5. For the first round (Rev.00), the CG response may not be a formal DS form — it could be an emailed directive. The comment is the requirement itself.
6. Build/update the cumulative disposition table:
   - Add a new `cat-row` divider for the new round
   - Add the round's comments with appropriate number and badge
   - Link each resolution to the relevant CRP section
7. **Verify each comment's resolution actually changed the document** — diff old vs new version. A disclaimer note appended to an unchanged table block is not "addressing" the comment. Check that:
   - Structural changes (removing a table, reordering sections) were actually applied — not just covered by a note
   - The old version still matches the new version in the areas CG complained about
   - Use `diff` or compare key line ranges between revisions
8. Update `CG_STATUS.md` to reflect current status accurately — check physical PDF packages exist before claiming submission

### Pitfalls

- **"Addressed" ≠ "Changed"** — When you claim a CG comment is resolved, verify the actual document content changed between revisions. A new disclaimer note on an otherwise identical table/section does not constitute addressing the comment. Always diff old vs new HTML/PDF to confirm.
- **CG comments can contradict each other across rounds** — Round 1 may mandate one sequence (e.g., Shop Drawings before Material Submittals), Round 2 (Code C) may mandate the opposite. The CRP should follow the **latest** CG direction and cite the Roadmap's override clause as authority.
- **Not all CG comments are correct as written** — Some comments are administratively impractical (e.g., "remove SAMAYA from workload table" — the table is a management tool, not a contractual document). The response should address the underlying concern (prevent misinterpretation) rather than blindly delete useful data. Relabel the table, add explicit disclaimers, keep the management data.
- **Status docs are not ground truth** — `CG_STATUS.md`, `*_STATUS.md`, and CRP status banners can be written prematurely. Always verify submission status by checking actual deliverable files (PDFs in `01_Source_Files/02_PDFs/`, email timestamps, Aconex records).
- **Sidecar analysis files can be wrong** — Reply analysis `.md` files may reference comments or statuses that don't match the actual CG reply PDF. Always extract from the PDF directly.
- **Cross-verify statuses against register logs (.xlsb/.xlsx)** — The project register log (`Register Log.xlsb`) is the authoritative source for document approval statuses. It tracks every submission round (R0, R1, R2...), dates, and status codes. CG_STATUS.md can be out of sync with the register. Always read the register with `pyxlsb` to verify a document's current status before updating disposition tables or related documents lists. See `references/register-log-verification.md` for the full workflow.
- **Use formal labels in document notes** — When writing explanatory notes in tables or boxes, use direct formal labels like `Purpose:`, `Contractual Position:`, `Communication Volume:` — never conversational phrases like `What this table shows`, `What stays the same`, `Why SAMAYA PD shows 78%`. The user corrects this immediately.

## 1ab. Forwarded Document Triage — Determining Expected Action

**Trigger:** A project document (TQ, proposal, letter, submittal) is forwarded to the user (Technical Office Manager) without an explicit instruction. The user asks "what they want from me now?"

### Workflow

1. **Locate the original document** in the project files — check `09_Correspondence/`, `02_Submittals/`, or `Email_Archive/` for the matching doc ref/PDF

2. **Extract document content** — use PyPDF2 or pdftotext to read the full PDF. Understand what the document proposes/requests

3. **Check distribution list** — who was on the original distribution? Who is NOT on it? If the user wasn't on original distro, someone intentionally forwarded it to them

4. **Check email archive** for related correspondence (even 0-byte .eml stubs reveal thread existence — SENT_FW_ = forwarded, Re: = replies). Note dates:
   - Original issue date vs forward date (time gap tells urgency)
   - Recent forward (hours/days) = active action item
   - Old forward (months) = may be informational/for awareness

5. **Determine the user's role in the chain** — Technical Office Manager's expected actions on forwarded documents typically fall into one of:

   | Document Type | Expected Action | Evidence |
   |---|---|---|
   | **TQ/RFI** (consultant proposing alternative) | Provide technical assessment: is the alternative feasible? Cost/schedule/quality impact? Recommendation for Samaya's formal response | User wasn't on original distribution but forwarded for technical input |
   | **Vendor proposal** (product/system offer) | Review against project spec, BOQ, and design intent. Flag gaps, compliance issues, or opportunities | Forwarded from procurement/PM for Tech Office review |
   | **CG response** (review comments) | Read comments, classify per CG Comment Classification framework. Determine which need Samaya action vs consultant action | Forwarded so Tech Office can triage to relevant subs |
   | **Subcontractor submission** (method statement, shop drawing) | Verify against approved design, SOW, spec. Approve or reject with comments | Forwarded for technical clearance |
   | **Meeting minutes / MOM** | Extract action items assigned to Samaya. Check if any belong to Tech Office specifically | Forwarded for awareness + action tracking |

6. **Assess timing and priority:**
   - Recent forward + pending CG response → input needed before formal reply
   - Old document + no follow-up → may be catch-up review. Check if action already taken
   - Multiple SENT_FW stubs = circulated multiple times — likely an unresolved item

7. **Formulate answer:** Present the document's request, your analysis of what the sender needs, and offer to draft the response or recommendation

### Example (this session — TQ-0021 Gallery Partitions)

```
Document: MOC-ASEER-SIC-1A0-TQ-0021 (4-Mar-2026)
Forwarded: 29-Jun-2026 (3 months after issue)
Original distro: Albahrawi, Darwish, Sultan Issa, A. Salah, Bouyiri
User: NOT on original distro — forwarded for input

What they want: Technical Office assessment on NRS's proposed switch from blockwork to drywall for gallery partitions — before Samaya formally responds to CG.
```

### Pitfalls

- **0-byte .eml stubs reveal nothing about the email body** — don't waste time trying to read them. Use filenames (SENT_FW_, Re:) and timestamps to reconstruct the thread structure
- **Time gap between issue and forward matters** — a 3-month-old TQ forwarded today is likely a different ask than the original (someone is circling back to close it)
- **Not being on original distribution is the key signal** — if the user was on the original distro, the document was sent to them at the time. If forwarded later, someone specifically wants their input on it now
- **Don't assume a single ask** — the forward may have multiple purposes (review + coordinate + respond). Separate them

## 1b. CG Comment Reasonableness Assessment & Response Strategy

**Trigger:** A CG review response arrives with comments. Before filing or updating the disposition table, assess each comment against the project stage, contractual scope, and existing deliverables.

### Comment Classification Framework

Classify every CG comment before deciding how to respond:

| Classification | Description | Example |
|---------------|-------------|---------|
| **Scope Mismatch** | Requests deliverables outside the agreed submission scope or stage | "Show all MEP systems in 3D renders" — viz renders show design intent, not MEP coordination |
| **Out-of-Stage** | Asks for items due in a later stage as if missing from current | "Missing material board and FF&E" — arch viz Pkg 01 is intent renderings, material selection is separate |
| **Administrative Change** | Requests process/format change mid-stream without formal amendment | "Submit gallery-by-gallery not floor-based" — requires register revision first |
| **Valid Technical Correction** | Genuine error or omission to fix. If comment is vague ("missing annotations", "incorrect tile pattern"), ask CG for specifics before actioning | Wrong tile pattern, missing annotations |
| **Subjective/Aesthetic** | Opinion-based preference | "View 6 to be improved" |
| **Spec Reference Dispute** | CG claims deviation from approved spec — verify first for internal position, but DO NOT task designers with spec-checking | "Patinated brass rejected" — tell NRS "CG requires patinated brass, update renders"; spec check is internal only |
| **Missing Scope Confirmation** | CG says items missing — check if they were in the agreed package | "G7, G10, G13 renders missing" — were these in Package 01 scope? |
| **Boilerplate / Standard Clause** | Generic contractual reminder, not specific to this submission | "Design changes must be formally submitted" |

### Response Strategy per Classification

| Classification | Recommended Response |
|---------------|-------------------|
| **Scope Mismatch** | Push back — cite deliverable definition in submittal register or SOW. Offer alternative that addresses the underlying concern |
| **Out-of-Stage** | Clarify the deliverable track and stage. Reference digital material board if it already exists as a separate deliverable |
| **Administrative Change** | Accept conditionally — requires formal revision to Submission Plan first |
| **Valid Technical Correction** | Accept — fix in next revision |
| **Subjective/Aesthetic** | Accept reasonable ones, use judgment on vague ones |
| **Spec Reference Dispute** | Request CG cite the approved spec reference. If spec backs them, accept. If not (finish not in approved schedule), ask CG for the specific reference. The spec check is internal — NRS only needs to hear "CG requires [finish], please update" |
| **Missing Scope Confirmation** | Confirm scope. If not in agreed package, they go in a later package |
| **Boilerplate / Standard Clause** | Acknowledge — no action needed beyond noting in response |

### Verifying Spec References from Schedule Data

When CG claims a material doesn't match the approved spec, verify against the actual schedule data before responding:

1. **Find the finish code** referenced in the CG comment (e.g., FI_ME_01, FI_ST_03)
2. **Check the JSON schedule files** at the project's data directory (e.g., `~/Desktop/aseer-backups/src-*/data/schedules/finishes_schedule.json` or per-schedule `.json` files)
3. **Search all schedules** — the disputed finish may live in Finishes, Setwork, Showcase, Graphic, or another schedule
4. **Record what the spec actually says:** supplier (TBC or named), product code/RAL (or missing), colour reference, treatment/finish description
5. **Use this data to inform your response:**
   - If spec has no supplier/RAL/sample → ask CG for the approved product reference
   - If spec has a named product → verify the renders match it
   - If spec says "refer to visuals" → no approved sample exists, request one from CG

This analysis is for **Samaya's internal position** — do not pass spec-checking tasks to NRS. NRS only hears "CG requires [finish X], please update."

### Decision Tree

```
CG comment received
│
├─ Boilerplate/contractual reminder?
│   └─ Acknowledge, move on
│
├─ About something NOT in agreed scope/stage?
│   ├─ Claimed missing → Confirm scope
│   ├─ Scope mismatch → Push back with scope reference
│   └─ Out-of-stage → Clarify separate track
│
├─ Administrative process change?
│   └─ Accept conditionally (requires register amendment)
│
├─ Spec/dispute?
│   └─ Request CG cite approved spec reference
│
└─ Valid technical issue?
    └─ Accept and schedule fix
```

### Digital Material Board Reference

The Aseer hotspot platform (https://samaya-factory.com/aseer/) serves as the project's **digital material board**. It covers 12 schedule types: Finishes, Setwork, Showcase, Graphic, Wayfinding, FF&E, Object, Exhibit, Art Commission, Asset, Media & AV, Mockups. When CG claims "missing material board", respond by providing access — this platform IS the material board, interactive and organized by gallery.

### Cross-Reference Against Approved Scope Submittals

Before responding to any CG comment that claims items are "missing" or requests organizational changes (e.g., "submit gallery-by-gallery"), **check for an earlier approved submittal that defines the scope/format**:

1. Search Outlook SQLite for related submittals with codes like `ZD-`, `PL-`, or the same discipline prefix + sequential numbering
2. Look for an approved (Code A/B) submittal that defines: what was agreed, how items are organized, which elements are included/excluded
3. In this session's example: **MOC-MUS-ASE-1A0-ZD-0031 Rev.01** (General Layout Plan for Proposed 3D Viewpoints) was **approved B by CG on 19-May-2026**. It defines the exact camera shots, organization, and gallery scope. CG then contradicted it in ZD-0060 by requesting gallery-by-gallery and claiming G7/G10/G13 were "missing"
4. Use this evidence to push back: "This was approved in submittal [X] on [date]. A change requires a formal amendment."

**Decision Tree addition** — after the existing decision tree, add:

```
├─ Is CG contradicting their own earlier approval (Code A/B)?
│   └─ Reference the approved submittal as binding scope
│   └─ Accept conditionally: requires formal amendment
```

### CG Comment Analysis Workflow

1. Extract all CG comments from PDF (use `pdftotext` — never rely on sidecar files alone)
2. **Cross-reference the email thread** — Check Outlook SQLite for the CG's email (it may have a different review code than the PDF). Also check for NRS replies in the same conversation thread — Jim/Robin may have already responded with scope confirmations or questions that affect your response.
3. Classify each comment using the framework above
4. Cross-reference against: actual submittal package scope, project stage (DD/Procurement/On-site), approved specifications, existing registers and deliverable tracking
5. For ambiguous/vague comments ("improve", "missing" without specifics), prepare a clarification request to CG rather than assuming or passing vague instructions to NRS
6. Formulate response per classification:
   - **Accept** — valid corrections, schedule fix
   - **Push back** — scope/stage mismatches, cite contractual basis
   - **Clarify** — CG may be unaware of existing deliverables (e.g., hotspot platform) OR the comment needs more detail to action
   - **Conditionally accept** — require formal amendment first
7. Draft response memo and file with the CG response PDF

### Material Change Response — "Sample First, Render Once"

When CG rejects a finish/material in renders and demands reversion to the approved spec:

1. **Accept** the comment — do not argue the spec at the design team level
2. **Check the approved finishes schedule data** (JSON files in `~/Desktop/aseer-backups/src-*/data/schedules/`) to see what the spec actually says for that finish code
3. **If the spec has no supplier/RAL/product code** (e.g., supplier "TBC Locally Sourced", colour "refer to visuals") → respond to CG requesting the approved product reference/sample. The spec is not sufficiently defined to render from.
4. **If the spec has a named product with RAL/supplier** → it's defined, render to match.
5. **Source a physical sample** matching the spec description and submit it to CG for approval through the material submittal process.
6. **Only after CG approves the sample, instruct NRS to update the renders.** This avoids re-rendering twice if CG rejects the interim reference.
7. **NRS communication:** NRS only needs to hear "CG requires [finish X], please update renders." Do NOT pass spec-checking details or supplier TBC issues to NRS — that's Samaya's internal coordination.

### Drafting CG Responses with Opening Context Paragraph

When CG returns a C-status response on a deliverable that is meant to close gaps from an earlier stage (e.g., 3D visualization to close Stage 3 tender gaps), and several comments appear to be scope mismatches or process changes rather than genuine quality issues, add an **opening paragraph** that sets context:

> "We note that several comments reference matters that were already agreed and approved under previous submissions. The [deliverable type] is intended to [its purpose — e.g., close gaps from the Stage 3 tender documentation and provide a clear visual reference for all stakeholders ahead of fabrication]. We trust you will agree that the project will benefit from resolving these points efficiently so that work can proceed without unnecessary delays."

This frames the conversation around project progress, not just compliance with each individual comment.

### Pitfalls

- **"Addressed" ≠ "Changed"** — When you claim a CG comment is resolved, verify the actual document content changed between revisions. A new disclaimer note on an otherwise identical table/section does not constitute addressing the comment. Always diff old vs new HTML/PDF to confirm.
- **CG comments can contradict each other across rounds** — Round 1 may mandate one sequence (e.g., Shop Drawings before Material Submittals), Round 2 (Code C) may mandate the opposite. The CRP should follow the **latest** CG direction and cite the Roadmap's override clause as authority.
- **CG may contradict their own earlier approval** — Always check for an approved scope submittal (Code A/B) before accepting claims that items are "missing" or organization is wrong. If CG approved the shot layout (ZD-0031 Rev.01) that defined floor-by-floor with specific galleries, they cannot later claim gallery-by-gallery or list excluded galleries as "missing." Reference the approved submittal and require a formal amendment.
- **Not all CG comments are correct as written** — Some comments are administratively impractical (e.g., "remove SAMAYA from workload table" — the table is a management tool, not a contractual document). The response should address the underlying concern (prevent misinterpretation) rather than blindly delete useful data. Relabel the table, add explicit disclaimers, keep the management data.
- **Status docs are not ground truth** — `CG_STATUS.md`, `*_STATUS.md`, and CRP status banners can be written prematurely. Always verify submission status by checking actual deliverable files (PDFs in `01_Source_Files/02_PDFs/`, email timestamps, Aconex records).
- **Sidecar analysis files can be wrong** — Reply analysis `.md` files may reference comments or statuses that don't match the actual CG reply PDF. Always extract from the PDF directly.
- **Cross-verify statuses against register logs (.xlsb/.xlsx)** — The project register log (`Register Log.xlsb`) is the authoritative source for document approval statuses. It tracks every submission round (R0, R1, R2...), dates, and status codes. CG_STATUS.md can be out of sync with the register. Always read the register with `pyxlsb` to verify a document's current status before updating disposition tables or related documents lists. See `references/register-log-verification.md` for the full workflow.
- **Use formal labels in document notes** — When writing explanatory notes in tables or boxes, use direct formal labels like `Purpose:`, `Contractual Position:`, `Communication Volume:` — never conversational phrases like `What this table shows`, `What stays the same`, `Why SAMAYA PD shows 78%`. The user corrects this immediately.
- **CG comments are not automatically correct** — Some are written generically without awareness of project stage, existing deliverables, or scope definitions. Always cross-reference.
- **"Missing" doesn't mean not done** — May be submitted under a different deliverable track. Check all registers and the hotspot platform before accepting.
- **Don't task designers with finish spec-checking** — When CG rejects a finish (e.g., "patinated brass not accepted"), the email to NRS says "CG requires [finish X], please update renders." NOT "check the spec and update." Spec checking is internal decision-making for Samaya; designers just reflect CG direction in their renders.
- **Spec disputes need evidence** — Don't take CG's word on what the spec says. Check the approved material schedule PDF. But this check is for Samaya's internal position, not something to pass to NRS.
- **Administrative process changes mid-stream** — Accepting without amending the plan creates tracking gaps.
- **CG review code comes from the email, not the attached PDF** — The CG's email explicitly states the status (Code A/B/C/D). The PDF attachment may use softer language ("generally accepted") while the email declares "C - Revise and Resubmit." The email is the formal notification. Always check both and use the email's code.
- **Ambiguous CG comments need clarification before actioning** — When a comment is vague ("View 6 to be improved", "annotations missing" without specifics, "tile pattern incorrect" without direction), DO NOT pass the vague instruction to NRS. First ask CG to clarify/specify what needs changing. Common patterns:
  - "Improve" / "to be improved" → ask what aspect (composition, lighting, texture, angle?)
  - "Missing" without list → ask what specifically is missing
  - "Incorrect" without correction → ask what the correct value/layout should be
  - No feedback detail on a response sheet → the CG marked it but wrote nothing — ask for specifics
- **Cross-reference the full email thread before finalizing response** — Jim/NRS may have already replied with critical details (scope confirmations, movement joint issues, product reference requests) that change how you respond to CG. Always check Outlook SQLite for the latest NRS reply in the conversation thread before drafting the formal CG response. In this session, Jim's reply (ID=45582) confirmed G7/G10/G13 were excluded per scope AND revealed the movement joints issue AND asked for a brass sample reference — all of which changed the CG response strategy.
- **NRS scope confirmation overrides CG assumptions about missing items** — When CG says "G7/G10/G13 renders missing" but NRS confirms "agreed not to visualise these spaces," the CG comment is invalid — respond citing the agreed scope, not accepting the "missing" framing."
- **WhatsApp images may use alpha-channel-only content** — Some screenshots from messaging apps store text in the alpha channel (RGB channels are black, alpha has the content). Attempt OCR on the alpha channel or use delegate_task with a vision-capable sub-agent before concluding the image is unreadable.
- **One CG reply + forward to NRS, not separate threads** — Draft a single reply to CG covering all points, then forward that same email to NRS with a brief cover note ("FYI, sent to CG on your input"). This avoids maintaining two separate response narratives.

## 5b. Authoring Technical Documents (MOS, Plans, Reports) — Doc Number Convention

**Trigger:** Creating or editing a Method of Statement, Plan, Report, or any formal technical document where the document number has not yet been assigned by the Document Controller.

### Document Number Rules

- **Leave the Document No. field blank** — use `—` (em dash) everywhere the document number would appear. The DC assigns the number at submission time.
- **Document Ref on cover:** show `— · Rev XX · YYYY-MM-DD` (e.g., `— · Rev 00 · 2026-06-16`)
- **Page footers:** show `— · Rev XX` instead of the full doc ref
- **Document Control block "Document No." field:** show `—`
- **Title tag / doc-strip header:** omit the doc number entirely
- **End-of-document "Document:" line:** use `Document: — · Revision XX`
- **Appendix page strips:** use `—` in place of the doc ref

### Internal Consistency When Updating Building Data

When a user supplies corrected floor-by-floor area data, update ALL of these consistently:

1. **Cover — Building field** — area + levels list
2. **Section 1 description** — narrative text with area total and levels
3. **Section 2 scope intro** — list of levels covered
4. **Scan Round coverage descriptions** — levels listed per round
5. **Level area table** — rows, descriptions, areas, scan estimates

Proportional scan estimate guideline: maintain the original scan density ratio (~1 scan per 40–55 sqm) when adjusting estimates for new areas. Flag adjusted estimates to the user for confirmation.

### Pitfalls

- If the user previously said the document number should be included (old version), switching to "—" requires checking ALL occurrences — not just the DC block but also page footers, appendix strips, doc-strip headers, end-of-document text, and the HTML title tag. 27+ occurrences is typical for a 22-page MOS.
- The page footer span pattern is `<span class="dc">— · Rev XX</span>` — the em dash preserves readability.
- Area data and level counts must be consistent across all sections. A mismatch between the cover summary and the detailed table causes rejection at review.

## 5c. Extracting one-page section summaries from HTML MOS/plan documents

**Trigger:** User asks for one or more sections from a large HTML Method of Statement, Plan, or Report on a single printable page (e.g., "Sections 3.2 and 4 in one page").

**Reference:** `references/html-section-extraction.md` — full workflow including how to locate section boundaries in large HTML exports, build a print-ready A4 one-pager, name the file, and open it for review/PDF output.

### Quick summary
1. Use `search_files` to find the target headings in the source HTML.
2. Use `read_file --offset --limit` to capture headings, paragraphs, and tables.
3. Create a new HTML file with A4 `@page` CSS, Samaya header, rev chip, and footer.
4. Name it `{OriginalDocNo}_Sections_{X}_and_{Y}.html` and save it next to the source.
5. Open in browser for the user to view/print.

### Pitfalls
- Large HTML files may fail full-file reads; use heading search + offset reads.
- Sections may span multiple `<div class="sheet">` pages in the source — read far enough.
- Preserve exact technical values (resolutions, distances, quantities) without rephrasing.
- Do not invent a document number if the source uses an em dash placeholder.

### Section §-linking in formal HTML docs

When building or editing formal project HTML documents, all internal section references (`§1.2`, `§7.0`, `§9`, etc.) must be clickable anchor links that match the document's section IDs. Use:

```html
<a href="#s7" style="text-decoration:none;color:inherit">§7.0</a>
```

The `text-decoration:none;color:inherit` keeps the link invisible — no visual change from plain text, but clickable in digital format. Apply this to ALL CRP section references (not ROADMAP §, ER §, SoW §, or Contract § — those point to other documents).

## 5d. Verifying RFI/TQ Submission Status Against Registers

**Trigger:** User asks "have we sent this RFI?" or "check RFI against project info" — verifying whether drafted RFIs were formally submitted as TQs (Technical Queries).

### The Core Problem

RFI registers (.xlsx) frequently go **stale** — showing RFIs as "Open" or "Draft (HOLD)" long after they've been formally issued as TQ documents with Rev A status through Aconex. Never trust the register alone.

### Workflow

1. **Read the markdown drafts** — `FORMAL_RFI_NNN_*.md` files in the subcontractor's `06_RFIs/` folder. Note the questions, references, and "ready to submit" markers.

2. **Scan for issued PDFs** — Look for PDFs in the same `06_RFIs/` folder matching the RFI topic. Issued TQ PDFs follow the pattern: `طلب XXX - وصف · MOC-MUS-ASE-1A0-TQ-NNNN Rev A.pdf`

3. **Extract PDF metadata** — Use pdftotext to check the document header block:
   ```bash
   pdftotext "path/to/TQ-NNNN Rev A.pdf" - 2>/dev/null | head -30
   ```
   Look for: doc ref (`MOC-MUS-ASE-1A0-TQ-NNNN Rev A`), issue date, status line (`Issued to CG` / `Issued to Employer`), document control block with `Rev A`.

4. **Compare draft vs submitted content** — Extract the PDF body and compare against the markdown draft:
   ```bash
   pdftotext "path/TQ-NNNN Rev A.pdf" - 2>/dev/null | tail -100
   ```
   Match question headings, numbered items, and reference citations (SOW, ER, Briefing Pack references). Bilingual PDFs embed English alongside Arabic — search for unique English phrases.

5. **Cross-reference against RFI Register** — Read the register data sheet:
   Check status column, linked TQ column, and dates against actual submission.

6. **Report discrepancies** — Compact table with: Draft RFI, TQ Issued, Register Status, Accurate? (Y/N).

### Key Detection Patterns

| Register Status | PDF Evidence | Conclusion |
|----------------|-------------|------------|
| "Open" / "Draft" | TQ-NNNN Rev A, "Issued to" | Register stale — update to Issued/Awaiting Response |
| "Open" / "Draft" | No matching TQ PDF | Not yet sent — draft is still internal |
| Blank TQ column | TQ-NNNN Rev A exists | Register missing linked TQ ref |

### Pitfalls
- Register mtime is not reliable — recent changes may be formatting, not status
- TQ PDFs may be in `05_Returned_Submittals/` or master archive, not `06_RFIs/`
- TQ numbers may skip — don't assume gaps
- Bilingual PDFs confuse text extraction — search for unique English identifiers
- Internal RFIs never get TQ numbers
- Master register copy vs per-subcontractor copy may have different column structures

### June 2026 Example (Graphics Contractor)
- RFI-003 Scope Boundary → TQ-0027 Rev A PDF existed in folder, register showed "Open" — **NOT actually issued via Aconex.** PDF was a prepared draft awaiting PM approval.
- RFI-004 MoC Content → TQ-0028 Rev A PDF existed, register showed "Draft (HOLD)" — **NOT actually issued.** Drafted but never submitted.
- Folder `03_Graphics_Contractor` but docs all reference "Sub-08"
- **Lesson: Rev A on a PDF does not mean formally issued.** Verify through Aconex trail or PM confirmation before marking as Issued.

## 5e. Pre-Issue QA Review of Formal RFIs/TQs

**Trigger:** User asks to review draft RFI/TQ before issue — or corrects a mistake in one (invented citation, wrong route, missing doc ref).

Before any formal RFI/TQ is submitted via Aconex, run a 3-domain quality review using the template at `references/rfi-tq-qa-review-template.md`:

### Domain 1 — Format & Document Control
Check: fonts (Noto Naskh Arabic / Carlito / JetBrains Mono), RTL, bilingual labels, logo strip (all 4 parties), doc-control block, RFI ref number, revision history, QC sign-off, footer pagination, status consistency.

### Domain 2 — Content vs Project Information
**Critical: Verify every contractual quotation against the source document.** This session found Evidence D (ER §1.3) contained entirely invented text. Check:
- SOW §2.2, §8.1, §8.14, p.17 against the actual SOW PDF
- ER citations — especially §1.3 (scope overview, NOT scenographer coordination)
- Briefing Pack M2 — AR primary, native typographer, curator-reviewer sign-off
- Programme dates against current baseline
- Gallery codes against official list (G6=Saudi Art, G8=Al Qatt)

### Domain 3 — Communication & Stakeholder Plan
Routing, distribution, POCs, response deadline, register logging, WITHOUT PREJUDICE clause.

### Output
Findings table (Pass/Fail/Flag per check) + verdict (Issue / Issue-with-corrections / Do-not-issue).

### Pitfalls
- **ER §1.3 does NOT contain scenographer coordination language** — confirmed in June 2026 review, invented text
- **RFI ref numbers often missing** — HTML covers lack formal TQ-XXXX ref
- **"High priority" ≠ response deadline** — required-by date must be stated
- **Distribution often omits the Curator** — content RFIs need Curator on distribution per ER §2.2
- **No WITHOUT PREJUDICE clause** — scope-boundary RFIs need rights-reservation language per Comm Plan
- **Response deadlines may not carry from markdown to HTML** — check the HTML before calling review done

## 6. Verifying Plan Document References Against the Register Log

**Trigger:** Before publishing or submitting any plan/procedure revision, verify all document references (doc numbers, revisions, statuses) against the Register Log.

### Workflow

1. **Open the Register Log** — located at the project's `_MANAGER_DASHBOARD/` area or shared drive. The log has multiple sheets (tabs).
2. **Navigate to the `Document Submittals` tab** — this is the authoritative list of all submitted documents with their official document numbers, titles, and types.
3. **Extract the log's doc reference data** using Python/openpyxl (or delegate to a subagent). Get all rows with their doc numbers, descriptions, and types.
4. **Cross-reference every doc ref in the plan** against the log:
   - Match plan's cited doc ref → log entry by number
   - Verify the title/description matches (confirm it's the same document, not just same prefix)
   - If the plan says `MOC-ASEER-GN-DS-006` and log says the same → correct
   - If the plan says `PL-0010` and log says `PL-0010` → correct
5. **Check HSE/plan refs carefully** — The main HSE Plan (PL-0010) is different from individual HSE Plans (e.g., `1KH-PL-0040` = Site Security Management Plan, not the HSE Plan). Verify the description matches.
6. **Fix discrepancies** — If a doc ref in the plan doesn't match the log, update the plan to use the log's number.

### Key Patterns from the Aseer Register Log

| Pattern | Meaning | Examples |
|---------|---------|---------|
| `MOC-MUS-ASE-1K0-PL-NNNN` | Current convention (multi-discipline Plans) | PL-0029 = DMP |
| `MOC-ASEER-SIC-1K0-PL-NNNN` | Older convention (still valid, used for earlier docs) | PL-0010 = HSE Plan, PL-0015 = BEP |
| `MOC-MUS-ASE-1KH-PL-NNNN` | HSE-specific Plans | PL-0040 = Site Security Plan |
| `MOC-ASEER-GN-DS-006` | Master Programme (Time Schedule) — NOT PL- series | |

### Old vs Current Naming Convention

Documents numbered before ~PL-0028 use `MOC-ASEER-SIC-1K0-...` (older convention).  
Documents numbered after ~PL-0028 use `MOC-MUS-ASE-1K0-...` (current convention).  
Both are valid — use what the Register Log says for each document.

### Pitfalls

- The Register Log does NOT contain plan/procedure document numbers until they've been submitted. Unsubmitted plans use `—` (em dash) as their reference.
- The Document Submittals tab only covers documents that have been formally submitted to the CDE. Internal documents won't appear.
- Some document numbers from the Register Log may not match filenames on the filesystem — the log is authoritative for the plan's reference section.
- The HSE Plan (`PL-0010`) and individual HSE specialist plans (`1KH-PL-0040` onwards) are different documents. Don't conflate them.

## 5d. Verifying RFI/TQ Submission Status Against Registers

**Trigger:** User asks "have we sent this RFI?" or "check RFI against project info" — verifying whether drafted RFIs were formally submitted as TQs (Technical Queries).

### The Core Problem

RFI registers (.xlsx) frequently go **stale** — showing RFIs as "Open" or "Draft (HOLD)" long after they've been formally issued as TQ documents with Rev A status through Aconex. Never trust the register alone.

### Workflow

1. **Read the markdown drafts** — `FORMAL_RFI_NNN_*.md` files in the subcontractor's `06_RFIs/` folder. Note the questions, references, and "ready to submit" markers.

2. **Scan for issued PDFs** — Look for PDFs in the same `06_RFIs/` folder matching the RFI topic. Issued TQ PDFs follow the pattern: `طلب XXX - وصف · MOC-MUS-ASE-1A0-TQ-NNNN Rev A.pdf`

3. **Extract PDF metadata** — Use pdftotext to check the document header block:
   ```bash
   pdftotext "path/to/TQ-NNNN Rev A.pdf" - 2>/dev/null | head -30
   ```
   Look for: doc ref (`MOC-MUS-ASE-1A0-TQ-NNNN Rev A`), issue date, status line (`Issued to CG` / `Issued to Employer`), document control block with `Rev A`.

4. **Compare draft vs submitted content** — Extract the PDF body and compare against the markdown draft:
   ```bash
   pdftotext "path/TQ-NNNN Rev A.pdf" - 2>/dev/null | tail -100
   ```
   Match question headings, numbered items, and reference citations (SOW, ER, Briefing Pack references). Bilingual PDFs embed English alongside Arabic — search for unique English phrases.

5. **Cross-reference against RFI Register** — Read the register data sheet:
   Check status column, linked TQ column, and dates against actual submission.

6. **Report discrepancies** — Compact table with: Draft RFI, TQ Issued, Register Status, Accurate? (Y/N).

### Key Detection Patterns

| Register Status | PDF Evidence | Conclusion |
|----------------|-------------|------------|
| "Open" / "Draft" | TQ-NNNN Rev A, "Issued to" | Register stale — update to Issued/Awaiting Response |
| "Open" / "Draft" | No matching TQ PDF | Not yet sent — draft is still internal |
| Blank TQ column | TQ-NNNN Rev A exists | Register missing linked TQ ref |

### Pitfalls
- Register mtime is not reliable — recent changes may be formatting, not status
- TQ PDFs may be in `05_Returned_Submittals/` or master archive, not `06_RFIs/`
- TQ numbers may skip — don't assume gaps
- Bilingual PDFs confuse text extraction — search for unique English identifiers
- Internal RFIs never get TQ numbers
- Master register copy vs per-subcontractor copy may have different column structures

### June 2026 Example (Graphics Contractor)
- RFI-003 Scope Boundary → TQ-0027 Rev A PDF existed in folder, register showed "Open" — **NOT actually issued via Aconex.** PDF was a prepared draft awaiting PM approval.
- RFI-004 MoC Content → TQ-0028 Rev A PDF existed, register showed "Draft (HOLD)" — **NOT actually issued.** Drafted but never submitted.
- Folder `03_Graphics_Contractor` but docs all reference "Sub-08"
- **Lesson: Rev A on a PDF does not mean formally issued.** Verify through Aconex trail or PM confirmation before marking as Issued.

## 5e. Pre-Issue QA Review of Formal RFIs/TQs

**Trigger:** User asks to review draft RFI/TQ before issue — or corrects a mistake in one (invented citation, wrong route, missing doc ref).

Before any formal RFI/TQ is submitted via Aconex, run a 3-domain quality review using the template at `references/rfi-tq-qa-review-template.md`:

### Domain 1 — Format & Document Control
Check: fonts (Noto Naskh Arabic / Carlito / JetBrains Mono), RTL, bilingual labels, logo strip (all 4 parties), doc-control block, RFI ref number, revision history, QC sign-off, footer pagination, status consistency.

### Domain 2 — Content vs Project Information
**Critical: Verify every contractual quotation against the source document.** This session found Evidence D (ER §1.3) contained entirely invented text. Check:
- SOW §2.2, §8.1, §8.14, p.17 against the actual SOW PDF
- ER citations — especially §1.3 (scope overview, NOT scenographer coordination)
- Briefing Pack M2 — AR primary, native typographer, curator-reviewer sign-off
- Programme dates against current baseline
- Gallery codes against official list (G6=Saudi Art, G8=Al Qatt)

### Domain 3 — Communication & Stakeholder Plan
Routing, distribution, POCs, response deadline, register logging, WITHOUT PREJUDICE clause.

### Output
Findings table (Pass/Fail/Flag per check) + verdict (Issue / Issue-with-corrections / Do-not-issue).

### Pitfalls
- **ER §1.3 does NOT contain scenographer coordination language** — confirmed in June 2026 review, invented text
- **RFI ref numbers often missing** — HTML covers lack formal TQ-XXXX ref
- **"High priority" ≠ response deadline** — required-by date must be stated
- **Distribution often omits the Curator** — content RFIs need Curator on distribution per ER §2.2
- **No WITHOUT PREJUDICE clause** — scope-boundary RFIs need rights-reservation language per Comm Plan
- **Response deadlines may not carry from markdown to HTML** — check the HTML before calling review done

## 6. Verifying Plan Document References Against the Register Log

**Trigger:** Before publishing or submitting any plan/procedure revision, verify all document references (doc numbers, revisions, statuses) against the Register Log.

### Workflow

1. **Open the Register Log** — located at the project's `_MANAGER_DASHBOARD/` area or shared drive. The log has multiple sheets (tabs).
2. **Navigate to the `Document Submittals` tab** — this is the authoritative list of all submitted documents with their official document numbers, titles, and types.
3. **Extract the log's doc reference data** using Python/openpyxl (or delegate to a subagent). Get all rows with their doc numbers, descriptions, and types.
4. **Cross-reference every doc ref in the plan** against the log:
   - Match plan's cited doc ref → log entry by number
   - Verify the title/description matches (confirm it's the same document, not just same prefix)
   - If the plan says `MOC-ASEER-GN-DS-006` and log says the same → correct
   - If the plan says `PL-0010` and log says `PL-0010` → correct
5. **Check HSE/plan refs carefully** — The main HSE Plan (PL-0010) is different from individual HSE Plans (e.g., `1KH-PL-0040` = Site Security Management Plan, not the HSE Plan). Verify the description matches.
6. **Fix discrepancies** — If a doc ref in the plan doesn't match the log, update the plan to use the log's number.

### Key Patterns from the Aseer Register Log

| Pattern | Meaning | Examples |
|---------|---------|---------|
| `MOC-MUS-ASE-1K0-PL-NNNN` | Current convention (multi-discipline Plans) | PL-0029 = DMP |
| `MOC-ASEER-SIC-1K0-PL-NNNN` | Older convention (still valid, used for earlier docs) | PL-0010 = HSE Plan, PL-0015 = BEP |
| `MOC-MUS-ASE-1KH-PL-NNNN` | HSE-specific Plans | PL-0040 = Site Security Plan |
| `MOC-ASEER-GN-DS-006` | Master Programme (Time Schedule) — NOT PL- series | |

### Old vs Current Naming Convention

Documents numbered before ~PL-0028 use `MOC-ASEER-SIC-1K0-...` (older convention).  
Documents numbered after ~PL-0028 use `MOC-MUS-ASE-1K0-...` (current convention).  
Both are valid — use what the Register Log says for each document.

### Pitfalls

- The Register Log does NOT contain plan/procedure document numbers until they've been submitted. Unsubmitted plans use `—` (em dash) as their reference.
- The Document Submittals tab only covers documents that have been formally submitted to the CDE. Internal documents won't appear.
- Some document numbers from the Register Log may not match filenames on the filesystem — the log is authoritative for the plan's reference section.
- The HSE Plan (`PL-0010`) and individual HSE specialist plans (`1KH-PL-0040` onwards) are different documents. Don't conflate them.

## 7. Document Content Rules & Style Guardrails

When authoring or editing project documents (plans, reports, method statements), always follow `references/document-content-rules.md`. Key rules to keep in mind:

### Cover Page & Front Matter

- **Document Number**: Leave as `—` (em dash) until the Document Controller assigns it. Never use placeholder "XX" or "TBD" as a doc ref on the cover.
- **REF line**: Omit entirely if no number has been assigned. Do not write `REF: MOC-...-XX`.
- **Revision/CG Review text**: Keep on the cover's content card (e.g., "Issued for CG Review" + "REVISION C02"), not as a standalone footer block.
- **Logos**: Center them full-width at the bottom of the cover, using `justify-content:space-between` on a `width:100%` flex container. Labels should be short ("Consultant" not "Consultant (CG)").

### Self-Incriminating Language  

Never write anything that could be used to claim Samaya is failing an obligation:
- ❌ `TBC — ⚠ CRITICAL PATH`
- ✅ `TBC`
- Avoid: "CRITICAL PATH", "delayed", "behind schedule", "at risk", "failure", "deficiency", "problem" re Samaya's own performance.
- Use neutral terms: "pending", "in progress", "to be confirmed", "awaiting".

### Named Persons & Firms

- Unless a name/firm appears in an approved KPR or approved submittal, use `—` or a generic description.
- Never name unapproved consultants: ❌ "Dr. Ehab Foda — LEED / Mostadam", ❌ "Lumotion".
- ✅ Generic: "Sustainability Strategy — per ER", "Interactive Applications — prequalification in progress".
- If the user corrects you once on a name, persist that correction — don't reintroduce the name later in the same session.

### Materials Section

Use only generic material descriptions — no brand names:
- ❌ `Porcelain & mosaic tiles (Ceramiche Piemme), carpet (Tarkett), acoustic panels (Kvadrat)`
- ✅ `Porcelain & mosaic tiles, carpet, acoustic panels`

Exception: Specialist subcontractor firm names in Tier 2/Appendix B tables are fine for scope identification.

### Role Accuracy

- Mohamed Mostafa = **Technical Office Mechanical Engineer**, not BIM modeler
- Electrical Engineer = on site (not HO) — drop "(HO)" suffix
- Junior engineer names should not appear in the plan
**Use the canonical workflow in `samaya-technical-office/references/subcontractor-creation-workflow.md`** — it is the single source of truth and is more detailed than what's below. The summary here is a quick reference; defer to the canonical workflow for the full process.

### Quick reference
1. Find next available number (check `Subcontractors/` folder listing)
2. Create 9 standard subdirs: `01_Schedule_and_BOQ/`, `02_Reference_Drawings/`, `03_Specifications_and_Standards/`, `04_Reference_Imagery/`, `05_Returned_Submittals/`, `06_RFIs/`, `07_Approvals/`, `Email_Data_Extraction/`, `_MANAGER_DASHBOARD/`
3. Write `_MANAGER_DASHBOARD/SCOPE_REQUEST.md` using the **Samaya standard 10-section template** (see canonical workflow for exact structure)
4. Generate `SCOPE_REQUEST.docx` at sub root using `samaya-docx-template` (SamayaDoc class)
5. Create `_MANAGER_DASHBOARD/SITUATION_REPORT.md` + `_MANAGER_DASHBOARD/_Email_Draft_to_find_lab.md`
6. Search entire project for related docs and **copy** them into the appropriate subdirs
7. Verify every file path referenced in the SOW actually exists in the subfolder
8. Update `README.md` register with new row

### Key rules (from canonical workflow)
- **All `.md` files go in `_MANAGER_DASHBOARD/`** — never at sub root. Only root file is `SCOPE_REQUEST.docx`.
- **Status docs require physical file verification** — A claim of "submitted" in a status doc (CG_STATUS.md, any _STATUS.md) is NOT ground truth. Always check for the actual PDF submission package in `01_Source_Files/02_PDFs/`. Sidecar status files can be prematurely written or incorrect.
- **SCOPE_REQUEST.md must be original** — structure is reusable, content is trade-specific.
- **Reference files must exist** — SOW can only list files actually in the subfolder.
- **Duplicate numbering**: keep first sub at `NN_Name`, suffix the newer one (`NNa_` trade, `NNb_` vendor).
- **Formal DOCX uses SamayaDoc template** — import from `samaya_doc_template.py`.
- **SOW cites only approved source docs** — never infer scope. Omit or flag TBC.
- **Supplier cert ≠ independent test** — flag this distinction.

## 2b. Standardizing a plan document folder structure

**Pattern:** `02_Plans_and_Procedures/02.{NN}_{Name}/`

Use when setting up or expanding a plan/procedure document folder (e.g., 02.17_Risk_Management_Plan). Follow the canonical structure in `references/plan-document-folder-structure.md`.

### Quick steps
1. Identify the next `02.{NN}` number from sibling folders
2. Create the 11-standard-entry hierarchy (see reference)
3. Write `README.md` with folder-purpose table and key-documents list
4. If source files already exist (`01_Source_Files/`), leave them in place — just add the missing subfolders

### Template README format

```markdown
# 02.{NN} {Name} — Aseer Museum

## Folder Structure

| Folder | Description |
|--------|-------------|
| `00_Master_Index/` | Index & version control |
| `01_Source_Files/01_HTML/` | HTML master document |
| `01_Source_Files/02_PDFs/` | Signed/stamped PDF copies |
| ... | ...

## Key Documents
- **Master Source:** `01_Source_Files/aseer_{name}.md`
- **HTML Render:** `01_Source_Files/01_HTML/aseer_{name}.html`
```

## 3. Drafting project correspondence

### Email rules
- **NRS emails**: only items NRS must act on. Remove any mention of Samaya-internal actions.
- **PM emails**: separate NRS-action list from Samaya-team-action list clearly.
- Save drafts as `.md` in `Correspondence/draft_email_{recipient}_{topic}.md` for review before sending.
- Never ask NRS to decide something the contract/spec already defines — NRS suggestions are flags, not decision requests.

### Subcontractor quotation review workflow

When reviewing a quotation/proposal against contract documents (ER, SOW, DMP), see `subcontractor-folder-setup/references/subcontractor-quotation-review.md` for the full 7-phase workflow: extract quote from email → cross-reference → baseline selection → gap classification → payment alignment → document pack → correspondence.

## 4a. Batch-Processing Prequalification Submittals (PQ Files)

**Trigger:** User sends multiple PQ PDFs at once (via chat, drag-drop, or email) — typically 5–20 files in a batch.

### Workflow

1. **Extract all PDFs to text** in parallel:
   ```bash
   for f in *.pdf; do pdftotext -layout "$f" "/tmp/${f%.pdf}.txt" 2>&1 | tail -1; done
   ```

2. **Read the cover page** (first 30 lines) of each text file to identify:
   - Subcontractor/supplier name
   - Discipline code (1A0=Arch, 1C0=Civil, 1E0=Elec, 1M0=Mech, 1K0=General)
   - CG status code (A/B/C/D) — look for the status stamp near the top
   - Submittal date
   - Description/scope
   - **Contract number** — verify it matches the project (Aseer = 0010003521). Flag mismatches.

3. **Detect CG status unreadability**: If pdftotext produces garbled/encoded text (Arabic glyphs rendered as Latin characters, or the status line is unreadable), the CG code may be embedded in a non-extractable font. Flag to user: *"CG status unreadable via text extraction — open PDF visually to confirm A/B/C/D."*

4. **Detect duplicates and near-duplicates**:
   - Same scope from different suppliers (e.g., Rajhi Steel + ALSSAD Steel both for "Reinforcement steel") — both are valid, file both
   - Same submittal number with different content — flag as potential duplicate
   - Same date + same description — likely duplicate upload

5. **Detect incomplete downloads**: Files ending in `.crdownload` or with suspicious sizes (e.g., 113MB for a PQ) — check with `file` command. If it's a PDF but pdftotext fails, it's incomplete. Advise user to re-download.

6. **Determine filing location** per discipline code:

   | Code | Discipline | OneDrive Target | Doc Control Mirror |
   |------|-----------|-----------------|-------------------|
   | `1A0` | Architecture | `02_Submittals/09_Prequalifications/` | `04_Submittals/Architecture/` |
   | `1C0` | Civil/Structural | `02_Submittals/09_Prequalifications/` | `04_Submittals/Structure/` |
   | `1E0` | Electrical | `02_Submittals/09_Prequalifications/` | `04_Submittals/Electrical/` |
   | `1M0` | Mechanical | `02_Submittals/09_Prequalifications/` | `04_Submittals/Mechanical/` |
   | `1K0` | General | `02_Submittals/09_Prequalifications/` | `04_Submittals/General/` |

   **Note**: All PQ files go to the same OneDrive folder (`09_Prequalifications/`). The discipline subfolder in Doc Control is for quick-reference mirroring only.

7. **Cross-reference against existing registers** before filing:
   - Check if the supplier already has a PQ entry in the relevant register
   - Check if the same PQ number already exists in the target folder
   - If a PQ file already exists in the target folder with the same number, compare sizes and dates — the newer one may be a resubmission

8. **File the PDFs** — copy to OneDrive target first, then mirror to Doc Control working copy

9. **Update registers** — append rows to the relevant submittal register (Arch, Elec, Mech, Structural, or General) with: PQ number, supplier, scope, date, CG status (or "TBC" if unreadable)

10. **Update memory** with a compact summary table of all processed PQs

### Prequal Compliance Assessment & Gap-Filling

**Trigger:** User sends prequal documents for a supplier and asks "are they compliant?" or "can they pass?" — evaluating a supplier against a specific SOW's prequalification requirements (§5).

#### Workflow

1. **Read the SOW prequal requirements** (§5 of the relevant SOW) — extract mandatory certifications, experience minimums, technical capabilities, and submittal package items.

2. **Map supplier's submitted docs** against each requirement in a compliance table:
   - ✅ Pass — requirement met
   - ❌ Missing — not provided
   - ⚠️ Partial — partially met or TBC

3. **Classify gaps into three tiers:**
   | Tier | Description | Verdict |
   |------|-------------|---------|
   | **Waivable** | ISO certs, BIM capability, fire/GREENGUARD knowledge — common for KSA establishments, CG may accept track record instead | Likely pass with conditions |
   | **Negotiable** | Museum project count (2 of 3 if cultural venues), team CVs if strong lead | Partial — needs framing |
   | **Blocker** | Missing methodology, programme, team CVs per SOW §5.4 | Must provide |

4. **Give a practical verdict** — not just pass/fail, but "can they pass with conditions" and what's needed.

5. **Offer to generate missing docs** — if the supplier lacks methodology and/or programme, generate them using the SOW as reference:
   - **Methodology doc**: Map each SOW scope section to a technical approach section. Use the supplier's actual equipment, tools, and team where known from their profile. Cover: assessment methodology, design methodology, commissioning, quality management, team capabilities.
   - **Programme doc**: Extract deliverables from SOW §3 (Deliverables by Stage), map to phases with dates from the project's Design Phase Master Programme. Include: programme summary table, deliverable schedule, coordination dependencies, assumptions.
   - **Format**: Generate as DOCX (user preference — editable) using SamayaDoc template. PDF also acceptable as secondary format.

6. **File both docs** in the supplier's prequal folder and update the register's "Docs Filed" column.

#### Pitfalls
- **Don't overstate compliance** — If the supplier has 0 museum projects, say so. Don't soften the gap.
- **Methodology must use the supplier's actual tools** — Don't invent equipment they don't have. Extract from their profile.
- **Programme dates must align with project baseline** — Use the Design Phase Master Programme (MOC-ASEER-0PS-SH-006), not invented T+X durations.
- **DOCX is preferred over PDF** for editable documents the supplier may need to modify. Generate both if time allows.
- **The generated docs are for the supplier to submit** — they are not Samaya deliverables. Mark them as draft/pending supplier review.
- **CRITICAL: Subcontractor-facing DOCX must NOT use Samaya branding.** When generating methodology/programme docs FOR a subcontractor to submit TO Samaya, do NOT use the SamayaDoc template. Use standalone DOCX generation (raw python-docx) with the subcontractor's own logo and color scheme. The cover should say "Submitted to: Samaya Investment" and "Prepared by: [Subcontractor Name]". The user will correct you if you put Samaya branding on a subcontractor's submission document — it's their document, not Samaya's.

### Pitfalls

- **CG status is often unreadable** — Many PQ PDFs use embedded fonts that pdftotext cannot decode. The status line (A/B/C/D) may appear as garbled text. Always flag this to the user rather than guessing.
- **Contract number mismatch** — PQ-0006 in this session had contract 4800000960 instead of 0010003521 (Aseer). This may belong to a different Samaya project. Flag for verification.
- **Same-scope PQs from different suppliers are both valid** — Don't deduplicate by scope alone. Multiple suppliers may be prequalified for the same material category (e.g., Rajhi Steel + ALSSAD Steel for reinforcement).
- **Same submittal number + same date = duplicate** — Keep only one copy. The `(1)` suffix in filenames is a browser download artifact.
- **Incomplete downloads** — `.crdownload` files that are PDFs but fail text extraction are incomplete. Delete and re-download.
- **OneDrive sync blocks file operations** — Write to `/tmp/` first, then copy to OneDrive path. See section 1c for the workaround.
- **Registers may not have a dedicated PQ column** — Some registers track PQs under "Submittal No." or "Type" columns. Check the register structure before appending.

## 4b. Processing Incoming Email Submissions (Batch Workflow)

Trigger: user asks to process project emails — read, extract attachments, route to folders, update registers.

### Full workflow per email

For each email with attachments:

1. **Read body** via `SELECT Message_Preview FROM Mail WHERE Record_RecordID = <ID>`
2. **Extract attachments** via AppleScript (reliable — always use this, skip .olk15MsgAttachment binary parsing):
   ```bash
   osascript -e "
   tell application \"Microsoft Outlook\"
       set theMsg to message id $ID
       set atts to (every attachment of theMsg)
       set outFolder to \"/tmp/outlook_extracts/\"
       repeat with att in atts
           set attName to name of att
           set savePath to outFolder & \"${ID}_\" & attName
           do shell script \"touch \" & quoted form of savePath
           set saveFile to POSIX file savePath as alias
           save att in saveFile
       end repeat
   end tell"
   ```
3. **Read attachment content** with `pdftotext` (poppler) — identify doc code, revision, approval status (Code A/B/C/D), CG reviewer
4. **Determine routing** from doc code prefix + discipline code (see routing table below)
5. **Save** to destination folder
6. **Update SITREP** in `_MANAGER_DASHBOARD/SITUATION_REPORT.md` if applicable
7. **Log** to `Email_Archive/_email_processing_log.md`

### Batch processing pattern

For 10+ emails, use parallel sub-agents in batches of 3:

```python
# Pattern: get IDs, extract all at once via shell loop, then route in Python
# Step 1: Extract all in one batch
for id in ID_LIST; do osascript ... done
# Step 2: Read each PDF, determine routing
# Step 3: Copy to destination folders
```

### Aseer Document Code Routing Table

Parse the doc code `MOC-MUS-ASE-{disc}{num}-{type}-{seq}`:

| Discipline Code | Discipline | Default Routing |
|----------------|------------|-----------------|
| `1A0` | Architecture | `02_Submittals/Architecture/` or `Design Files/` |
| `1C0` | Civil | Per doc-type prefix (default: `Docs/03_Inspection_Requests/`) |
| `1E0` | Electrical | `Design Files/Electrical/` or `09_Correspondence/` |
| `1KH` | HSE | `Docs/02_Plans_and_Procedures/02.5_HSE_Plan/` |
| `1K0` | General/Multi | Per doc type (see below) |
| `1M0` | Mechanical | `Docs/02_Plans_and_Procedures/02.16_Mobilization_Plan/` or per type |
| `1KN` | Security/ICT | `Docs/05_SIs/05.1_Issued_by_CG/` |

| Doc Type Prefix | Document Type | Routing Pattern |
|----------------|--------------|-----------------|
| `PL-` | Plan | `02_Plans_and_Procedures/02.{NN}_{Name}/` |
| `ZD-` | General/Methodology | Per discipline folder or `09_Correspondence/` |
| `MS-` | Method Statement | `02_Submittals/08_Method_Statements/` (create if missing) |
| `IR-` | Inspection Request | `Docs/03_Inspection_Requests/` |
| `NC-` | Non-Conformance Report | `Docs/10_Test_and_Inspection/10.3_NCRs/` |
| `SI-` | Site Instruction | `Docs/05_SIs/05.1_Issued_by_CG/` |
| `JSI-` | Joint Site Instruction | `Docs/05_SIs/05.1_Issued_by_CG/` |
| `PQ-` | Prequalification | `Docs/09_Registers/27_Subcontractor_Prequalification_Register/` |
| `MI-` | Mobilization Items | `02_Plans_and_Procedures/02.16_Mobilization_Plan/` |
| `TQ-` | Technical Query | `Design Files/` per discipline |
| `RP-` | Report | `02_Submittals/10_Reports/` (create if missing) |
| `SC-` | HSE Compliance | `02.5_HSE_Plan/01_Source_Files/` |

**CG Responses** (Code B or C status): copy to `02_CG_Responses/` subfolder within the parent document folder. The original submission goes to `01_Source_Files/`.

**Daily Reports**: always to `07_Daily_Reports/` with filename `Daily Report {DD-MM-YYYY}.pdf`.
**Weekly Reports**: to `07_Daily_Reports/Weekly_Reports/`.
**Invoices**: to `Docs/04_Financial/Invoices/`.

### Updating SITREP on email processing

When a key submission arrives (prequal, CG response, new appointment), update the relevant `_MANAGER_DASHBOARD/SITUATION_REPORT.md`:

- Bump date stamp
- Update `Status:` line
- Update `Prequal Register Status:` if applicable
- Check/uncheck action items
- Update `Subcontractor:` line if new firm

### Prequal register — handling all intake methods

**Location:** `Docs/09_Registers/27_Subcontractor_Prequalification_Register/`

Prequal submissions arrive via three paths — email attachments, direct chat file uploads (WhatsApp/Telegram), or SharePoint links. Each path converges on the same workflow below.

#### Common prequal intake workflow

1. **Identify the supplier** — If filenames are generic ("prequalification.pdf", "Company Profile -A.pdf"), extract PDF text with `python3 -c "import fitz; doc=fitz.open('path'); print(doc[0].get_text()[:2000])"` or `pdftotext` to find company name, address, and scope.

2. **Determine the PQ number** — Check the last row in `_status.md`:
   - If the last entry is `PQ-NNNN`, the next PQ number is `PQ-NNNN + 1`
   - If the last entry is a non-PQ entry (e.g., `C-05`), the next PQ number is the last PQ-NNNN + 1
   - Format: `PQ-` followed by 4 digits, zero-padded

3. **Create supplier folder** — `{Prequal_Register}/{Supplier_Name}/` (PascalCase, no spaces beyond underscore). No subfolder hierarchy — all files flat in the supplier folder.

4. **File documents** — Rename each PDF with a descriptive prefix:
   - Prequal ISO certs: `{Supplier}_Prequalification_ISO_Certs.pdf`
   - Company profile: `{Supplier}_Company_Profile.pdf`
   - TDS documents: `{Supplier}_{ProductCode}_{ProductName}_TDS.pdf`
   - Test reports: `{Supplier}_{ReportType}_Test.pdf`
   - Keep original product codes (e.g., WT73X0, WB711) in filenames for traceability

5. **Update `_status.md`** — Append a new table row:

   ```
   | PQ-XXXX | {Supplier Name} | {Package Description} | Received {DD-Mmm} | {YYYY-MM-DD} | {comma-separated key filenames} |
   ```

   Also append an update note below the table: `*Updated {YYYY-MM-DD} — Added {Supplier Name} ({Package}) prequal*`

6. **Create Odoo subtask** under package 3011 (00 — Pre-Qualification & Procurement) as a Tier 2 task (see `odoo-task-injection` skill for exact API). Assign to Sultan Issa (ID 151), tag 140 (Prequalification), stage 35 (Initiation), progress 20%. Include description listing all filed docs and their folder path.

7. **Log session time** to `account.analytic.line` with task ID, project 219, and estimated hours.

#### Handling mixed document packages

A single prequal submission often includes multiple document types: ISO certificates, company profile, product TDS (technical data sheets), test reports (VOC, LEED, etc.), and material safety data sheets.

File ALL documents in the supplier folder — not just the certs. The TDS and test reports are supporting evidence the reviewer will need. Name each file descriptively so the register's "Docs Filed" column gives a genuine inventory.

#### Direct chat uploads (WhatsApp/Telegram/Files)

When the user sends files directly (not via email):
1. Files are passed as paths in the conversation — copy from the provided temp location
2. No email body to extract context from — rely entirely on PDF text extraction to identify content
3. No SITREP or email log update needed (no email was processed)
4. Otherwise follow the common intake workflow above

#### Email-attachment prequal submissions

Follow section 4b (Processing Incoming Email Submissions) for extraction, then apply the common intake workflow for filing and register updates.

### SharePoint link handling (no direct attachment)

Some emails reference a file shared via OneDrive/SharePoint link rather than including it as a direct attachment. Signs:
- Email body contains a `https://...sharepoint.com/...` or `https://...my.sharepoint.com/...` URL
- `Mail_OwnedBlocks` only has image attachments (signatures), no PDF/document blocks
- The sender used Outlook's "Share" or "Attach → Share link" feature

These links require corporate authentication and cannot be downloaded programmatically. Do not waste iterations trying to curl/wget them (HTTP 401). Instead:

1. Confirm it's a SharePoint link by checking the email body
2. Create a **routing memo** `.md` file in the target folder documenting the link, document code, and sender
3. Log to `Email_Archive/` with a note that manual download is needed
4. Flag it to the user: the file path + that it's behind auth

Example memo content:
```markdown
# MOC-MUS-ASE-1K0-MI-0001 — SharePoint Link

**From:** Hossam Mabrouk (hmabrouk@cg.com.sa)
**Date:** 2026-06-11
**Link:** https://cgksa-my.sharepoint.com/... (requires CG KSA auth)

**Routing destination:** `Docs/02_Plans_and_Procedures/02.16_Mobilization_Plan/01_Source_Files/`
**Action:** Open link while authenticated to CG KSA tenant, download PDF, save to destination.
```

## 5. Maintaining PROJECT_MEMORY.md from Email Archives

Trigger: user asks to extract findings from an email archive (N.md) and update PROJECT_MEMORY.md.

### Workflow

1. **Read both files fully**
   - Read the email archive (`N.md`) — use `read_file` with offset pagination for large files. The archives are typically 5,000–17,000 lines.
   - Read the existing `PROJECT_MEMORY.md` — identify the latest section 0 entries and the most recent Session Update date.

2. **Cross-reference and identify delta**
   - Scan emails for:
     - Document references (`PL-XXXX`, `ZD-XXXX`, `IFC-XXXX`, `TQ-XXXX`, `PQ-XXXX`, `SI-XXXX`, `IR-XXXX`, `NCR-XXX`, `RP-XXXX`)
     - CG response codes (Code A/B/C/D from CG reviewers: `melbaz@cg.com.sa`, `hmabrouk@cg.com.sa`, `salfeer@cg.com.sa`, `asadat@cg.com.sa`)
     - PMC communications from `mohamed.elmahlawy@ace-mb.com` (meetings, MOMs)
     - NRS activities from Jim Richards, Francesco Bitelli, etc.
     - Subcontractor progress (Studio ZNA, ITC, Bluehaus, Leica/SITML, Artec/3DME, Heritage Sites)
     - Meeting references (Progress Meeting No., MOM No.)
     - Structural/technical developments (core tests, as-built drawings, quotations)
   - Check which items are ALREADY in section 0 — don't duplicate.
   - Identify items that are NEW or need updated detail.

3. **Apply updates to section 0 (LATEST STATUS UPDATES)**
   - Section 0 is a table with two columns: `Change` and `Detail`.
   - New entries go before the closing `|---` separator.
   - Use `patch` with multi-line context to ensure uniqueness (section 0 table rows have repeating `|| Change | Detail |` patterns).
   - Each entry follows the format:
     ```
     || **{Short Title (Date)}** | {Full detail including doc ref, outcome, filing location}. |
     ```
   - For CG code progressions, show both the initial and final status: e.g., "Originally Code C on 25-May, resubmitted 31-May, approved Code B 2-Jun."
   - Enhanced entries (adding detail to existing rows) can be done via targeted patch on the row's Detail column.

4. **Append Session Update section at end**
   - Location: after section 12 (or last numbered section, before any previous Session Updates).
   - Format:
     ```
     |## Session Update — {Date} ({Short label})
     |
     || Item | Detail |
     ||------|--------|
     || **Action** | {What was processed} |
     || **Source** | {Path to archive file} |
     || **Key Update** | {Brief summary of changes made} |
     |
     |### {Subsection} (e.g., CG Consultant Responses)
     |{Tables or bullet lists with structured findings}
     ```
   - Group findings into subsections: CG Consultant Responses, Progress Meetings, Lighting Design, 3D Scanning Evaluation, Structural Design, ICT Security, Core Test Data, etc.

5. **Update the date header** at the top of the file: `> آخر تحديث: **{date}**`

### Information Sources in Email Archives (N.md)

| Source | What to Look For |
|--------|------------------|
| **CG (melbaz@cg.com.sa)** | Response codes, review comments, SI issuances |
| **CG (hmabrouk@cg.com.sa)** | HSE plan responses, NCR closeout |
| **PMC (mohamed.elmahlawy@ace-mb.com)** | Meeting minutes (MOM No.), schedule updates, PMC directives |
| **NRS (Jim Richards, Francesco Bitelli)** | Design direction, RFIs, drawing comments |
| **Samaya (Hesham Abdelhameed)** | Submittals sent to CG, daily reports |
| **Samaya (Mohammed Hakami)** | Lighting, AV, ICT Security coordination |
| **Samaya (Abdelmohaymen Farag)** | Structural/technical coordination, quotation forwarding |
| **Samaya (Fahad Hassan)** | 3D scanning procurement evaluation |
| **Subcontractors** | Fee proposals, scope documents, CVs (Studio ZNA, Heritage Sites, SITML) |

### Pitfalls
- The `|---` separator after section 0 is not unique — always include surrounding table rows for context when patching.
- CG codes can change between email rounds (Code C → Code B for PL-0043, PL-0046). Track the initial AND final status.
- Some entries already exist in section 0 under different wording. Check for doc ref numbers, not just titles.
- The project memory already has a "Week 23 Email & Document Activity" section (section 12) that is separate from the Session Update. Session Updates go below it.
- NRS "outside our scope" = outside NRS scope, not outside Samaya scope. Check T2 allocation table first.
- Patinated brass finish concerns from NRS are advisory — the spec stands unless CG changes it.
- When a document has both CG comments and an NRS comment sheet, treat them as separate review layers.
