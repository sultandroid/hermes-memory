# Subcontractor Folder Population Workflow

Use when populating/updating any subcontractor folder under `Subcontractors/NN_Subcontractor_Name/`.

## Standard Folder Structure
```
01_Schedule_and_BOQ/     → BOQs, pricing, power reqs, quantity surveys
02_Reference_Drawings/   → DWG/PDF drawings, system plans, spec sheets
03_Specifications_and_Standards/ → specs, codes, ER docs, discipline files
04_Reference_Imagery/    → concept imagery, photos
05_Returned_Submittals/  → IFC packages, returned submittals, vendor docs
06_RFIs/                 → RFI register + individual RFIs
07_Approvals/            → stamped drawings, approvals, CG responses
SCOPE_REQUEST.md         → scope definition
REGISTER.md              → status register (create this)
```

## Workflow Steps

### 1. ASSESS SCOPE
- Read existing `SCOPE_REQUEST.md` — defines what deliverables the sub owes
- Read `PROJECT_MEMORY.md` — current status, critical issues
- Check `RFI_REGISTER.md` — open RFIs for this discipline

### 2. SEARCH THREE DOMAINS IN PARALLEL (delegate_task × 3)
Use 3 parallel sub-agents:
- **A. Project folder**: search ALL subdirectories (Submittals/, Docs/, Design Files/, Design Files (Stage 04)/, Completed Tender Package From NRS/, As-Built Docs/, Revit Files/, Specs & Datasheet/, Contracts/, Correspondence/, Invoices/, odoo/) — use `find` with keyword patterns
- **B. Email archives**: search `Email_Archive/` .md files, `Scripts/output/email_bodies/`, `Scripts/notes/`, `PROJECT_EMAILS.md` — find emails with discipline-specific ref numbers
- **C. Registers**: scan `PROJECT_MEMORY.md`, `RFI_REGISTER.md`, `PROJECT_EMAILS.md` for status info

### 3. COPY FILES TO TARGET
- Deduplicate across source locations — keep newest/latest version
- Organise into correct subfolder per the structure above
- Create subdirectories as needed (e.g., `IFC-XXXX/` under `05_Returned_Submittals/`)
- Include email extracts, CG response PDFs, stamped drawings

### 4. CREATE STATUS REGISTER (REGISTER.md)
Template sections:
- Scope summary (table of deliverables vs status)
- File inventory (by subfolder with counts)
- Critical open issues (RAG-rated)
- Deliverables progress (per RIBA or stage)
- Key emails archive table
- Contractor engagement status table
- Hardware/material census (if applicable)
- Knowledge gaps & next steps (priority-ordered)

### 5. UPDATE MAIN REGISTERS
- `PROJECT_MEMORY.md` — update IFC package status, add note with file count
- `RFI_REGISTER.md` — update FLS-related RFI status
- `PROJECT_EMAILS.md` — update date
- Persistent memory — save folder status to memory

## Entity Isolation Check
**CRITICAL before any copy/move**: Verify you're working in the correct entity's project folder.
- Samaya = `OneDrive-SAMAYAINVESTMENT/Samaya/`
- Tqanny = `OneDrive-Personal/Work/PWork/Tqanny/`
- Never cross-copy between these.
