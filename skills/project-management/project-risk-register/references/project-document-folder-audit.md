# Project Document Folder Audit — Systematic Register Creation

## When to Use

- User provides access to a project's document folders (OneDrive, network share, local) and asks you to "check what's there" or "read all and update the repo"
- You need to find evidence for risk register entries by scanning project correspondence, SIs, NCRs, RFIs, MOMs
- Building a complete picture of project documentation from a contractor's or PM's file archive
- Any task where you need to systematically process 10-20+ folders of project documents

## Core Principle: One File at a Time

**Never batch-read or batch-process files on OneDrive.** OneDrive sync is fragile — batch operations (ls on 100+ files, reading multiple files in parallel, moving/renaming) can trigger "Resource deadlock avoided" errors or corrupt the sync state.

**Correct pattern:**
1. List folder contents first (one `ls` per folder)
2. Read one PDF at a time using `pdftotext`
3. Write findings incrementally
4. Never `mv` or `rm -rf` on OneDrive paths

## Workflow

### Step 1: Inventory All Folders

```bash
ls -1 "/path/to/OneDrive/Project Folder/"
```

This gives you the top-level folder list. Note the naming pattern — some folders have status suffixes (CLOSED, U, Open) that indicate document status.

### Step 2: Classify Each Folder

| Classification | Criteria | Action |
|---------------|----------|--------|
| **High value** | Formal correspondence, SIs, NCRs, RFIs, MOMs, letters | Read and create register |
| **Medium value** | Weekly reports, daily reports, inspection requests | Index or skip |
| **Already tracked** | Submittal registers, pre-qualifications, IFC drawings | Skip — repo already has them |
| **Operational** | SNA, IR, SOR, MIR, safety notices | Skip — site operational records, not project-level |

### Step 3: Read High-Value Folders

For each high-value folder, read the primary PDFs:

```bash
# List PDFs in the folder
ls "/path/folder/"*.pdf 2>/dev/null

# Extract text from the main SI/NCR/letter PDF
pdftotext -layout "/path/folder/main_document.pdf" - 2>/dev/null | head -40

# Get the instruction/subject section
pdftotext -raw "/path/folder/main_document.pdf" - 2>/dev/null | grep -i -A5 "instruction\|subject\|description\|observation" | head -20
```

**Two-pass extraction:**
- **Pass 1 (`-layout`):** Get the header/metadata (date, ref number, parties)
- **Pass 2 (`-raw`):** Get the body text (instructions, observations, required actions)

### Step 4: Extract Key Fields

For each document, extract:

| Field | How to Find | Example |
|-------|-------------|---------|
| **Document ref** | Header area, often in Arabic/English | `MOC-MUS-CG-ASE-1KN-1E0-012` |
| **Date** | Header or footer | `17-5-2026` or `2026-05-17` |
| **Subject** | "Subject:" or "RFI Subject:" line | `Re-mobilization of BMS Engineer` |
| **Key instruction** | "Instructions" or "Description" section | `Re-mobilise qualified BMS Engineer to site` |
| **Status** | Folder name suffix or document body | `CLOSED`, `U` (Under Review), `Open` |
| **Related docs** | Attachments or referenced documents | `NCR NC-1E0-003` |

### Step 5: Cross-Reference Against Existing Registers

Before creating a new register entry, check if the document is already tracked:

```bash
# Search the repo for the document ref
rg "MOC-MUS-CG-ASE-1KN" 01_Registers/
```

If found, update the existing entry with new evidence. If not found, add a new row.

### Step 6: Create/Update the Register

Each register follows the same pattern:

```markdown
---
last_updated: YYYY-MM-DD
owner_agent: Technical Office
status: active
source: OneDrive/path/to/folder/
---

# [Document Type] Register — [Project Name]

> Source: [OneDrive path]

| Ref | Date | Subject | Key Content | Status | Linked Risks |
|:---:|:----:|---------|-------------|:------:|:------------:|
| DOC-001 | YYYY-MM-DD | Subject line | Brief description of content | Open/Closed | PRR-XXX |
```

**Columns by document type:**

| Register | Columns |
|----------|---------|
| **Letters** | Ref, Date, Subject, Key Content, Status, Linked Risks |
| **RFI/TQ** | Ref, Date, Subject, Key Query, Status, Linked Risks |
| **MOM** | Ref, Date, Meeting Type, Chair, Location, Key Topics, Minutes File, Status |
| **NCR** | NCR #, Date, Source, Subject, Status, Owner, Due Date, Linked Risks |
| **SI** | SI #, Doc Ref, Date, Subject, Key Instruction, Status, Samaya Response, Linked Risks |
| **Weekly Reports** | Report #, Date, File |

### Step 7: Link to Risk Register

For each document, determine which PRR/DRR risks it relates to:

| Document Type | Typical Linked Risks |
|---------------|---------------------|
| CG Warning Letters | PRR-COM-05 (EOT), PRR-MEP-01 (MEP upgrade) |
| SIs about sequence | PRR-STK-01 (SI dispute), PRR-DES-02 (design incomplete) |
| SIs about materials | PRR-PRC-05 (material approval), PRR-QLT-01 (quality) |
| SIs about HSE | PRR-HSE-01 (HSE exposure) |
| NCRs | PRR-STK-02 (open NCR leverage) |
| RFIs about structure | PRR-SIT-02 (structural verification), PRR-DES-07 (structural DD) |
| RFIs about procurement | PRR-PRC-05 (patinated brass), PRR-PRC-02 (showcases) |
| MOMs | Multiple — depends on topics discussed |

### Step 8: Update Risk Register Evidence

After creating the document register, update the risk register's evidence column with new references:

```python
# Find the risk by ID and append to evidence
cell = ws.cell(row=risk_row, column=evidence_col)
old = str(cell.value or '')
cell.value = old + '; New Doc Ref (Date) — brief description'
```

Only do this for **important** evidence that changes the risk picture — not every document needs to be referenced.

## Folder Classification Reference

| Folder Name | Typical Content | Value | Register to Create/Update |
|-------------|-----------------|:-----:|---------------------------|
| 01- Letters | Formal correspondence (IN/OUT) | High | letters_register.md |
| 02- DOC Submittal | Document submittals (ZD series) | Low | Already tracked |
| 03- Shop Drawing | Shop drawing packages | Low | Already tracked |
| 04- Daily Report | Daily site reports | Medium | Index only |
| 05- RFI/TQ | Technical queries | High | rfi_register.md |
| 06- MOM | Meeting minutes | High | meeting_minutes_register.md |
| 07- Pre-Qualification | Subcontractor PQs | Low | Already tracked |
| 08- Material Submittal | Material approvals | Low | Already tracked |
| 09- Method Statement | MS documents | Low | Skip |
| 10- CG Site Instruction | CG instructions/SIs | High | si_register.md |
| 11- IFC Drawing | IFC packages | Low | Already tracked |
| 12- NCR | Non-conformance reports | High | ncr_register.md |
| 13- Weekly Report | Progress reports | Medium | weekly_report_index.md |
| 14- IR | Inspection requests | Low | Skip |
| 15- SNA | Start new activity | Low | Skip |
| 16- Safety Notices | HSE safety notices | Low | Skip |
| 17- SOR | Safety observation reports | Low | Skip |
| 18- MIR | Material inspection requests | Low | Skip |
| 19- Weekly HSE | HSE reports | Low | Skip |
| 20- DDD | Design gate submittals | Low | Already tracked |

## Pitfalls

- **OneDrive "Resource deadlock avoided"** — quit OneDrive, wait 30s, retry. Write to `/tmp/` first, then copy to OneDrive.
- **PDFs with no text layer** — some scanned PDFs have images only. Use `pymupdf` to extract images, then OCR with tesseract.
- **Arabic PDFs** — `pdftotext` may produce garbled output for Arabic text. The English portions (dates, ref numbers, subjects) are usually readable even when Arabic is corrupted.
- **Folder naming inconsistencies** — some folders have status suffixes (CLOSED, U), some don't. Read the document body to determine actual status.
- **Misplaced files** — folders may contain wrong documents (e.g. NRS Portfolio in an SI folder). Cross-check the document ref against the folder name.
- **Empty folders** — some numbered folders exist but contain no PDFs. Note as "Missing" in the register.
- **Template dates vs actual dates** — PDFs may show a template build date (e.g. 2026-02-06) that differs from the actual issue date (e.g. 2026-06-02). Cross-check against the register log.
