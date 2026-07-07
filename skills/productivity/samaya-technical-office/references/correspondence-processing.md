# Incoming Correspondence Processing (Aseer Museum)

## When to use

A PDF document lands for the Aseer Museum project and needs to be analyzed, filed, tracked, and routed to the correct party. This is the standard pipeline for processing submittals, RFIs, NRS correspondence, and CG comments.

## Pipeline

### Step 0: Understand the document from its code

Parse the document code to determine filing location. Aseer Museum uses the format:
`MOC-MUS-ASE-<ORIGINATOR>-<TYPE>-<SEQUENCE>`

| Code part | Meaning | Examples |
|-----------|---------|----------|
| MOC | Ministry of Culture (client) | always prefix |
| MUS | Museum project | always MUS |
| ASE | Aseer region | always ASE |
| Originator: 1KH | Samaya (contractor) HSE/planning docs | PL, SC, ZD |
| Originator: 1K0 | Samaya wider team | PL, ZD, RP |
| Originator: 1A0 | NRS (design consultant) | ZD, MA, TQ |
| Originator: 1C0 | Civil works | IR |
| Originator: 1E0 | Electrical | PQ, ZD, MS |
| Originator: 1M0 | Mechanical | PL, ZD |
| Originator: 1V0 | ? | IR |
| Type: PL | Plan / Procedure | HSE plans, management plans |
| Type: ZD | Drawing / Design deliverable | shop drawings, IFC |
| Type: SC | Submittal / Compliance doc | HSE submittals |
| Type: IR | Inspection Request | temporary works, site inspections |
| Type: TQ | Technical Query / RFI | questions to CG |
| Type: RP | Report | assessment, status reports |
| Type: MA | Material / Material Approval | sample boards |
| Type: PQ | Prequalification | vendor pre-qual |
| Type: MS | Method Statement | installation methods |
| Type: SH | Schedule | programme |

HSE-related PL/SC documents (originator 1KH) go to the HSE plan folder **in addition to** Correspondence. Other submittals go only to Correspondence.

### Step 1.5: Batch detection — check for related documents

Before processing a single document, check if it's part of a batch. Signals:
- Sequential document numbers from the same originator-type (e.g., `PL-0055`, `ZD-0052`, `ZD-0053` all submitted same date)
- Same preparer (Muhammad Ahmed), same reviewer (Anwar Sadat), same submission date
- Same discipline (HSE) — PL, ZD, SC docs with 1KH prefix

When batch is detected:
- Process all documents from the batch together before filing any single one
- Create a consolidated note about the batch in the analysis of the first/key document
- Reference the batch relationship in each document's analysis ("Companion to PL-0055")

### Step 2: Check if file already exists (pre-stamp vs stamped)

Before copying, check if a file with the same document code exists in the target:

```bash
ls -la "Correspondence/MOC-MUS-ASE-1KH-PL-0055.pdf"
md5sum "/path/to/download.pdf" "/path/to/existing.pdf"
```

**Different sizes = different versions.** The new file may be the **CG-stamped version** (with sign-off, approval code, reviewer signature appended) and the existing file the pre-stamp submission. In that case:
- **Replace** the existing with the stamped version (authoritative record)
- **Update** the analysis to include the CG decision (approval code, reviewer, date, comments)
- Correct existing analysis if it recorded status as "Pending"

**Same size ≈ same file** — skip copy, just verify analysis is current.

### Step 3: Extract & read

| Document type | Filing pattern | Analysis pattern |
|---|---|---|
| HSE/PL submittal (1KH-PL-XXXX) | **Primary**: `Docs/02_Plans_and_Procedures/02.5_HSE_Plan/01_Source_Files/<doc>.pdf` **Secondary**: `Correspondence/<doc>.pdf` | Status + CG comments table + actions. Also update `_Project_Memory/PROJECT_MEMORY.md` with a status row in the Latest Updates section. |
| NRS RFI (A2742-XX) | `Completed Tender Package From NRS/05_Correspondence_Archive/03_NCRs_and_SIs/` | Open questions table + responsible party |
| NRS correspondence | `Correspondence/` or `Completed Tender Package From NRS/05_Correspondence_Archive/` | Scope clarification + action routing |
| CG response to submittal | `Correspondence/` alongside original submittal | Code meaning + items to address |

### Step 3: Determine correct filing location

**Submittals (MOC-MUS-ASE-XXX):** Go to `Correspondence/` alongside other submittals.
**NRS documents (A2742):** Go to `Completed Tender Package From NRS/05_Correspondence_Archive/` by subfolder type (NCRs_and_SIs, etc.)
**Contracts:** Go to `Contracts/NN_Party/`
**Subcontractor documents:** Go to `Subcontractors/NN_Trade/05_Returned_Submittals/`

### Step 4: Copy the file

```bash
cp "/path/to/download.pdf" "/path/to/Aseer-Museum/Correspondence/MOC-MUS-ASE-1KH-PL-0055.pdf"
```

### Step 5: Create analysis file

Follow the existing naming convention: `<doc-number>_Analysis.md`

For **CG-reviewed submittals**, the analysis should cover:
- Identity & status table (doc number, rev, type, approval code)
- CG comments table (finding → action required)
- Internal approvals (prepared by, reviewed by, approved by)
- Action required summary

For **NRS RFIs/correspondence**, the analysis should cover:
- Document identity
- Key statement (what NRS is saying)
- Open questions table (if any)
- Responsible party analysis (who should respond — check T2 allocation)
- Action required summary

### Step 6: Identify the responsible party

**Critical check** — do not assume "procurement gap" when a party says something is outside their scope. Use this resolution order:

1. Who is the sender? (NRS = design consultant only, not executive)
2. Check T2 allocation table in `Scripts/notes/Knowledge Notes - Stakeholder Mgmt Plan Rev02.md`
3. Check the document's distribution list — CC'd parties already know about the issue
4. Only escalate to procurement gap if no T2 party exists AND no CC clue

### Step 7: Update registers

- **PROJECT_MEMORY.md** — always add a status row for new submittals (see Step 8)
- **Transmittal Register** (`Docs/09_Registers/Transmittal_Register/`) — currently a template (no data). Only add if actively maintained.
- **Submittal IFC Log** (`Docs/09_Registers/Submittal_Tracker_IFC_Log/`) — tracks design/IFC submittals only (Arch, Struc, MEP, AV, etc.). HSE/PL documents are NOT added here.
- **Asher_Regional_Museum_Log** — outdated (April 2026). Do NOT add new entries.
- **Memory** — if the document triggers a new subcontractor package or important action item, add a compact memory entry.

**Rule:** Not every document needs an Excel register entry. HSE/PL plan submittals are tracked by their folder placement (HSE plan archive) + PROJECT_MEMORY status update. Only add to Excel registers when the user explicitly asks or when the register is actively maintained for that document type.

### Step 7b: CG Response Register — Always Update for CG-Reviewed Docs

When a document has an embedded CG response (Code A/B/C/D on the cover page), also update `Docs/02_Plans_and_Procedures/02.5_HSE_Plan/04_Registers/CG_Response_Register.md`:

1. **Full Document Register** — add a new row with plan category, doc code, title, CG status, date, reviewer
2. **Key Statistics** — increment the appropriate count (Code C, Code D, etc.) if adding a new type
3. **Critical Actions section** — add Code C/D items to the top of the table (Code D is highest priority)
4. **CG Response Timeline** — add a line at the bottom with reviewer, doc, and code

**Critical:** Code D (Disapproved) items take priority over Code C — place them first in Critical Actions.

### Step 8: Update PROJECT_MEMORY.md

For new submittals (especially HSE/PL documents), add an entry to the **Latest Status Updates** table in `_Project_Memory/PROJECT_MEMORY.md`:

```markdown
| **New PL-XXXX Submitted (Date)** | `MOC-MUS-ASE-1KH-PL-XXXX Rev.00` — [Title]. Submitted to CG for review. Filed in HSE Plan source files + Correspondence. |
```

For CG-rejected documents, flag the status prominently:
```markdown
| **New ZD-XXXX Submitted — Code D (Date)** | `MOC-MUS-ASE-1KH-ZD-XXXX Rev.00` — [Title]. **CG DISAPPROVED (Code D)** same day by [Reviewer]. Comment: [summary]. Requires revision and resubmission. Filed in HSE Plan source files + Correspondence. |
```

This keeps the project memory current for all team members and the AI.

## Pitfalls

- **Live Outlook emails**: to check recent emails that haven't been archived yet, query the Outlook SQLite database directly. See `ref:outlook-sqlite-reading.md` for connection details and sample queries. AppleScript over Outlook is unreliable (returns 0 messages even when data exists).
- **Always check if the document already exists in the project** — use `find` to search for the document code before copying. A document already in Correspondence but not in the HSE folder means you should copy there too (not skip both).
- **Examine sibling document numbers to determine convention** — before filing a new PL document (e.g. PL-0054), check where PL-0049 and PL-0055 live. Their locations reveal the filing convention. Don't assume — verify.
- **NRS scope exclusion does not mean Samaya gap** — NRS is the design consultant (A2742). When they say "not our scope," the responsibility likely lies with a T2 subcontractor (Rawasin, ZNA, Glasbau Hahn, etc.). Check before flagging.
- **Distribution list is your best routing clue** — if Shihab Mohamed (Rawasin) is CC'd, the issue is already routed to AV/interactives. If Adel Darwish is CC'd, it's at director level.
- **Analysis files follow existing naming** — look for existing `*_Analysis.md` files in the target folder and match the naming convention exactly.
- **Code B ≠ approved without action** — CG Code B means "Approved with Comments" — the comments must be addressed in the next revision. Always extract and list them.
- **Read full document, not just first page** — CG comments and approval stamps may be on later pages. Use `tail` to check the end of the PDF too.
- **Cover page checkbox ≠ actual CG status** — The Document Submittal cover sheet may have "B" pre-checked by the submittor, but the CG's actual response on later pages may be Code D. Always read the full document, especially CG response sheets with reviewer signatures, before recording the status in registers.
- **Separate CG Reply PDFs** — Sometimes CG returns a response as a separate PDF (4-page document with cover sheet + CG comment pages, without the CV attachments). File these alongside the original submittal with naming: `<doc-code> - CG Reply.pdf`. Update both the Correspondence folder and the source folder (Design Submittals if applicable). These also need CG Response Register updates.
- **CG Response Register update** — When a CG response arrives (especially Code D), always: (a) add row to Full Document Register, (b) increment Key Statistics, (c) add to Critical Actions (Code D above Code C), (d) add to CG Response Timeline. If existing analysis file incorrectly recorded the status, correct it.
- **HSE plan submittals go to 02.5_HSE_Plan** even if they're ZD type — ZD docs that are HSE training/operational belong alongside PL docs in the HSE plan source files.
