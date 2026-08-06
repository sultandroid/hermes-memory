# Contract Key Terms Extraction — Worked Example

> **Session:** 2026-08-02 — Aseer Museum 5-contract analysis
> **Source:** OneDrive contract folders + aseer-museum-pm fallback copies
> **Key challenge:** OneDrive file-lock on all signed PDFs and DOCX files

## Extraction Pattern

### 1. Start with the most accessible document

The Main Contract (10003521) had a pre-extracted markdown file (`Contract_0010003521_Full_EN.md`, 3518 lines). Read this first to establish the contractual framework that all subcontracts flow down from.

### 2. For each subcontract, search for alternative copies

When OneDrive files are locked (`Resource deadlock avoided`), search outside OneDrive:

```bash
find /Users/mohamedessa -maxdepth 5 -name "*keyword*" 2>/dev/null | grep -v "CloudStorage" | grep -v "Library"
```

**Fallback locations found:**
- `/Users/mohamedessa/aseer-museum-pm/03_Scope/Studio_ZNA_Lighting/` — ZNA consultancy agreement PDF (extractable)
- `/Users/mohamedessa/aseer-museum-pm/03_Scope/AD_Engineering/` — MEP designer SOW PDF (extractable)
- `/Users/mohamedessa/aseer-museum-pm/00_Contracts/04_NRS_Methodology/` — NRS contract index and scope references
- `/Users/mohamedessa/aseer-museum-pm/02_Schedule/Glasbau_Hahn_Showcases/README.md` — GBH status summary
- `/Users/mohamedessa/aseer-museum-pm/03_Scope/Glasbau_Hahn_Showcases/README.md` — GBH scope summary
- `/Users/mohamedessa/aseer-museum-pm/03_Scope/MEP_Contractor/README.md` — MEP installation status
- `/Users/mohamedessa/aseer-museum-pm/99_Archive/09_Procurement_Management/Contracts/` — ZNA review memos
- `/Users/mohamedessa/Desktop/Work_Projects/Asher_Regional_Museum_Emails/Attachments/` — email attachments (some readable)

### 3. For each contract, extract these fields

| Field | Notes |
|-------|-------|
| **Parties** | Full legal names, registration numbers, representatives |
| **Date / Effective Date** | Signature date, effective date, expiry |
| **Project** | Full project name |
| **Contract Type** | Lump-sum, cost-plus, FIDIC-based, supply agreement |
| **Total Value** | Amount + currency + tax treatment |
| **Term** | Duration + start/end dates |
| **Governing Law** | Jurisdiction, language precedence |
| **Payment Terms** | Milestones, invoicing, retention, advance payment |
| **Key Obligations** | Scope of work, deliverables, standards |
| **Termination** | Grounds, notice periods, cure periods |
| **Insurance** | Types, minimum amounts, duration |
| **Liability Caps** | Aggregate caps, per-occurrence caps, exclusions |
| **IP Rights** | Assignment, background IP, licenses, moral rights |
| **Dispute Resolution** | Courts, arbitration, escalation ladder |
| **Force Majeure** | Definition, notice periods, termination thresholds |

### 4. Cross-reference subcontracts against the Main Contract

Key flow-down patterns to check:
- **IP assignment:** Subcontractors assign IP to Samaya → Samaya assigns to MoC per Main Contract Art. 10
- **Liability caps:** Main Contract penalties capped at 20% of 74.9M SAR; subcontract caps should be proportional
- **Insurance:** Subcontractor PI insurance should meet or exceed Main Contract requirements
- **Scope alignment:** Subcontractor SOW should be a subset of Main Contract Annex 2 (Detailed Scope of Work)

### 5. Document the extraction limitations

When files are inaccessible, be explicit about what was NOT read:

> **Note:** Several signed PDFs on OneDrive are inaccessible due to OneDrive file-lock issues ("Resource deadlock avoided"). Where possible, alternative copies from the aseer-museum-pm repo were used.

### 6. Output structure

Save the structured summary to `00_Contracts/contracts_summary.md` in the project repo with:
- One section per contract with a consistent table format
- A cross-contract summary table at the end
- Key observations about gaps, risks, and flow-down issues
- File path to the saved summary

## OneDrive Lock Diagnostic

When ALL tools fail on a OneDrive file, the diagnostic is:

```
head: Error reading /path/to/file (Resource deadlock avoided)
file: ERROR: cannot read (Resource deadlock avoided)
pdftotext: Syntax Warning: May not be a PDF file (continuing anyway)
           Syntax Error: Couldn't find trailer dictionary
```

This means the file is a OneDrive "files on demand" placeholder that hasn't hydrated. The lock is at the macOS VFS layer — no tool can bypass it for PDFs. The only workaround is finding an alternative copy outside OneDrive.

## Tools that failed on locked OneDrive files (this session)

| Tool | Error |
|------|-------|
| `pdftotext` | 0 bytes output, `Couldn't find trailer dictionary` |
| `pdfminer.high_level.extract_text` | `OSError: [Errno 11] Resource deadlock avoided` |
| `pdfplumber` | `[Errno 11] Resource deadlock avoided` |
| `PyMuPDF (fitz)` | `Failed to open file` |
| `python-docx` | `OSError: [Errno 11] Resource deadlock avoided` |
| `textutil` (macOS) | `The file couldn't be opened` |
| `shutil.copy2`, `cp`, `cat`, `head`, `file` | All `Resource deadlock avoided` |
| `zipfile.ZipFile` | Also failed for PDFs (bypasses lock for DOCX only) |
