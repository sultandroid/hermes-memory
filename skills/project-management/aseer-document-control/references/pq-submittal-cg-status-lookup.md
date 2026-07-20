# PQ Submittal CG Status Lookup — Aseer Museum

## The Problem

The user asks to "extract all CG rejection PDFs for PQ submittals with C or D codes." The PQ submittals they name (PQ-0026 EXA, PQ-0122 Evergreen, PQ-0100 Waves/SDE, PQ-0105 MizarLabs, PQ-0107–0110 HVAC/Water Supply) may not exist as CG rejection PDFs in the correspondence folder. This reference documents the systematic search pattern.

## Search Strategy

### 1. Check the Correspondence folder first

```
09_Correspondence/  (root level)
├── 2025/
├── 2025-Archive/
├── 2026-02/ through 2026-06/
├── NRS/
├── Correspondence_Archive/02_Correspondence_MOC/
└── 14_Completed_Tender_Package_From_NRS/05_Correspondence_Archive/02_Correspondence_MOC/
```

Search for `*PQ*` files across all of these.

### 2. Check the Prequalification Register status file

```
04_Docs/09_Registers/27_Subcontractor_Prequalification_Register/_status.md
```

This markdown file tracks all PQ submissions with their status, date received, and filed docs. It is the **single source of truth** for what PQs have been submitted and their current status.

### 3. Check the PROJECT_MEMORY

```
_Project_Memory/PROJECT_MEMORY.md
```

Contains a "Submittals Dashboard" section with PQ refs, dates, and CG codes. Also has a "Latest Updates" section with recent CG responses.

### 4. Check the actual PQ submittal PDFs

```
02_Submittals/09_Prequalifications/
```

These are the raw vendor prequalification packages (often 10-50MB each). They contain the vendor's submission, not the CG response. The CG response is a separate PDF in the correspondence folder.

### 5. Check the Email Archive

```
16_Email_Archive/
```

Contains `.md` files with email summaries and `Attachments/` with PDFs. Search for `*PQ*` in both.

## CG Approval Codes

| Code | Meaning | Arabic |
|------|---------|--------|
| A | Approved | موافقة |
| B | Approved with Comments | موافقة مع شرط |
| C | Revise and Resubmit | تصحيح وإعادة تقييم |
| D | Disapproved | مرفوض |

## PQ Submittal Form Structure

Each PQ submittal PDF uses a standard bilingual form with these key fields:

- **Submittal No** (رقم التقديم) — e.g. MOC-MUS-ASE-1A0-PQ-0101
- **Submittal Date** (تاريخ التقديم)
- **Revision No** (رقم المراجعة)
- **Subcontractor** (اسم الشركة)
- **APPROVAL STATUS** (رمز الحالة) — checkboxes for A/B/C/D
- **CG Comments** (ملاحظات المهندس المشرف) — free-text field
- **CG Reviewer** — Name in "Revision By" or "Reliance By" field
- **Date** — Date in the CG signature block

## Known PQ Locations (worked example)

| PQ Ref | Vendor | Where Found | CG Code |
|--------|--------|-------------|---------|
| PQ-0101 | STUMIX (Acoustic) | `Correspondence_Archive/02_Correspondence_MOC/20260711_MOC-MUS-ASE-1A0-PQ-0101.pdf` | **C** |
| PQ-0096 | Namaa Office | `09_Correspondence/MOC-MUS-ASE-1K0-PQ-0096.pdf` | Blank (pending) |
| PQ-0085 | GITCO (BMS) | `14_Completed_Tender_Package_From_NRS/05_Correspondence_Archive/02_Correspondence_MOC/MOC-Asser-SIC-1E0-PQ-0085.pdf` | **B** |
| PQ-0056 Rev.00 | Panasonic | `14_Completed_Tender_Package_From_NRS/05_Correspondence_Archive/02_Correspondence_MOC/MOC-Asser-SIC-1E0-PQ-0056.pdf` | No code (CG: "Follow attached comment sheet") |
| PQ-0056 Rev.01 | Panasonic | `14_Completed_Tender_Package_From_NRS/05_Correspondence_Archive/02_Correspondence_MOC/MOC-MUS-ASE-1E0-PQ-0056 Rev.01.pdf` | **B** (per PROJECT_MEMORY) |
| PQ-013 | ICT Security | `09_Correspondence/MOC-MUS-CG-ASE-1KN-PQ-013_ICT_Security_System_Integrator.pdf` | Empty file |

## Why Specific PQs May Not Be Found

1. **Not yet formally submitted to CG** — The PQ may be in the prequal register as "Received" but not yet submitted via Aconex
2. **Only a company profile exists** — Some vendors (e.g. Evergreen Landscaping) submitted a profile but no formal PQ submittal form
3. **CG response not yet received** — The PQ was submitted but CG hasn't responded yet
4. **CG response is an email attachment, not a PDF** — Check the email archive for the CG response as an email body or attachment
5. **File is a OneDrive stub** — 4-byte `null` files that need hydration via `open` (Preview) first

## Extraction Pattern

```bash
# Extract CG comments from a PQ PDF
pdftotext "/path/to/PQ.pdf" - 2>/dev/null | grep -i "code\|status\|A\|B\|C\|D\|approv\|reject\|comment\|ملاحظات" | head -30

# Get the full CG comments section
pdftotext "/path/to/PQ.pdf" - 2>/dev/null | sed -n '/CG Comments/,/Contractor/p'
```
