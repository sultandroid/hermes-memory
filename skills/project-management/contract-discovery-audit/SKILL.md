---
name: contract-discovery-audit
category: project-management
description: "Multi-source contract, agreement, and submission plan discovery for construction projects. Searches OneDrive, Outlook, team member folders, and repo registers in parallel to produce a consolidated status table of all specialist contracts."
version: 1.0.0
author: Hermes Agent
platforms: [macos]
tags:
  - contracts
  - agreements
  - submission-plans
  - discovery
  - audit
  - outlook
  - onedrive
  - project-management
---

# Contract Discovery & Audit

When asked to find contracts, agreements, or submission plans for a project, search **all four sources** in parallel and produce a consolidated status table.

## The Four Sources

| Source | What to search | Key patterns |
|--------|---------------|--------------|
| **OneDrive project folder** | `01_Contracts/` subdirectories | Each numbered subfolder = one contract (e.g. `02_NRS_Contract`, `03_GBH_Showcase_Contract`) |
| **OneDrive subcontractor folders** | `24_Subcontractors/{NN}_{Specialist}/` | Look for `02_Contract/` subfolder, or `_CONTRACT_STATUS.md` in root |
| **Outlook SQLite** | Emails with contract/agreement keywords | Search last 12 months for: contract, عقد, agreement, SOW, scope of work, plus each specialist name |
| **Adel Darwish's folder** | `Adel  Darwish's files - 01- Execution Documents/` | Contract correspondence, advance payment letters, appendices |
| **Repo (aseer-museum-pm)** | `00_Contracts/README.md`, `02_Schedule/submission_plan_risk_assessment.md` | Contract references, submission plan with 32+ items |

## Canonical SQL Query (Outlook)

```sql
SELECT m.Record_RecordID as id,
       datetime(m.Message_TimeReceived, 'unixepoch', 'localtime') as received,
       f.Folder_Name as folder,
       m.Message_SenderList as sender,
       m.Message_NormalizedSubject as subject,
       m.Message_HasAttachment as att
FROM Mail m
JOIN folders f ON m.Record_FolderID = f.Record_RecordID
WHERE (m.Message_NormalizedSubject LIKE '%contract%'
   OR m.Message_NormalizedSubject LIKE '%agreement%'
   OR m.Message_NormalizedSubject LIKE '%submission plan%'
   OR m.Message_NormalizedSubject LIKE '%submittal plan%'
   OR m.Message_NormalizedSubject LIKE '%SOW%'
   OR m.Message_NormalizedSubject LIKE '%عقد%')
  AND m.Message_TimeReceived >= strftime('%s', 'now', '-365 days', 'localtime')
ORDER BY m.Message_TimeReceived DESC;
```

## Status Table Template

| # | Specialist | Contract File | Status | Notes |
|---|-----------|--------------|--------|-------|
| 1 | NRS (Design) | `01_Contracts/02_NRS_Contract/` | ✅ Signed | 2026-02-19 signed agreement |
| 2 | Glasbau Hahn (Showcase) | `01_Contracts/03_GBH_Showcase_Contract/` | ✅ Signed | Supply Agreement #328 |
| 3 | Studio ZNA (Lighting) | `01_Contracts/09_ZNA_Lighting_Contract/` | ✅ Signed | Consultancy Agreement |
| 4 | AD Engineering (MEP Designer) | — | ❌ Not found | Agreement emails exist but no signed contract on OneDrive |
| 5 | Rawasin (AV/IT) | — | ❌ Not found | PQ docs exist, no contract |
| 6 | Nama Consulting (FLS) | — | ❌ Not found | PQ docs only |
| 7 | Evergreen (Landscaping) | — | ❌ Not found | PQ docs only |
| 8 | Structural (Qotob) | `01_Contracts/07_Qotob_Stractural Designer Contract/` | ⚠️ Proposal only | Technical & financial offer, not a signed contract |
| 9 | Scenography | — | ❌ Not found | No contract, no PQ |

## Submission Plan Discovery

| Source | What exists |
|--------|------------|
| OneDrive `02_Submittals/04_Registers/` | Master_Submission_Plan.xlsx, Arch (Rev00-02), Mechanical, Landscape, AV |
| Repo `02_Schedule/submission_plan_risk_assessment.md` | 32-item consolidated plan with risk assessment |
| Outlook | Mechanical Submittal Plan, Arch Submission Plan CG comments, Deliverables Submission Schedule |

## Key Findings Pattern

When reporting, always state:
1. **Contracts found** — with folder path and status (Signed / Draft / Proposal only)
2. **Contracts NOT found** — explicitly list each missing contract
3. **Submission plans found** — per discipline
4. **Submission plans missing** — which specialists have no plan
5. **Next actions** — what needs to be extracted from email attachments, what needs to be created

## Workflow

### Phase 1: Scan OneDrive Contracts folder

```bash
ls -la "/path/to/01_Contracts/"
```

Each numbered subfolder is one contract. Check inside for signed PDFs, DOCX agreements, and supporting docs.

### Phase 2: Scan OneDrive Subcontractor folders

```bash
ls -la "/path/to/24_Subcontractors/"
```

For each specialist folder, check for:
- `02_Contract/` subfolder with signed agreements
- `_CONTRACT_STATUS.md` in root (one-page contract snapshot)
- `01_Prequalification/` for PQ docs (indicates pre-contract stage)

### Phase 3: Search Outlook

Run the canonical SQL query above. For each specialist, also search by name:
```sql
AND (m.Message_NormalizedSubject LIKE '%Glasbau%'
   OR m.Message_NormalizedSubject LIKE '%AD Engineering%'
   OR ...)
```

Key email IDs with contract attachments should be noted for potential extraction.

### Phase 4: Check Adel Darwish folder

```bash
ls -la "/path/to/Adel  Darwish's files - 01- Execution Documents/"
```

Adel's folder typically has contract correspondence (advance payment letters, appendices) but not the contracts themselves.

### Phase 5: Check repo

```bash
ls ~/aseer-museum-pm/00_Contracts/
cat ~/aseer-museum-pm/02_Schedule/submission_plan_risk_assessment.md | head -80
```

### Phase 6: Consolidate

Build the status table. For each contract:
- **✅ Signed** — signed PDF/DOCX exists on OneDrive
- **⚠️ Proposal only** — only technical/financial offer, no signed contract
- **❌ Not found** — no contract file in any source
- **📧 Email only** — agreement discussed in email but no signed file on OneDrive

## Pitfalls

- `01_Contracts/` may have numbered subfolders that don't match the 11 specialists (e.g. `07_Qotob_Stractural Designer Contract` for structural)
- Some contracts are in `24_Subcontractors/{NN}_{Specialist}/02_Contract/` not in `01_Contracts/`
- Email attachments with signed agreements may not have been saved to OneDrive — check Outlook IDs with `Message_HasAttachment = 1`
- Adel Darwish's folder has contract correspondence (advance payments, appendices) but not the contracts themselves
- The repo's `00_Contracts/` is READ-ONLY for agents — cite by reference, don't modify
- Submission plans may exist as Excel in OneDrive but not as MD in the repo
- OneDrive cloud-only files (0 blocks) cannot be read — use Outlook or repo as fallback
- Epoch verification is mandatory for Outlook queries — run the Step 0 query first
- When user asks in Arabic "هل تبحث علي الاميلات" (are you searching emails?), confirm which sources you've searched — they want to know you checked emails, not just files

## DOCX Extraction from OneDrive Stubs

`textutil` returns empty for OneDrive cloud-only .docx files (stubs). Use Python zipfile to extract `word/document.xml` directly:

```bash
python3 -c "
import zipfile, re, shutil
src = '/path/to/contract.docx'
tmp = '/tmp/clean_name.docx'
shutil.copy2(src, tmp)
with zipfile.ZipFile(tmp) as z:
    with z.open('word/document.xml') as f:
        content = f.read().decode('utf-8', errors='replace')
text = re.sub(r'<[^>]+>', ' ', content)
text = re.sub(r'\s+', ' ', text).strip()
print(text)
"
```

This works even when `textutil` and `pdftotext` return empty because the file is a OneDrive placeholder.

## Key Terms Extraction Pattern

After extracting contract text, search for these keywords to find critical clauses:

```python
for kw in ['Fee', 'Payment', 'Liability', 'Termination', 'Insurance', 
           'Intellectual Property', 'Governing Law', 'Warranty', 'Variation']:
    idx = text.find(kw)
    if idx >= 0:
        print(f'=== {kw} ===')
        print(text[idx:idx+2000])
```

## Phase 7: Build Obligations Matrix

After the discovery phase, build a structured obligations matrix covering all specialists across these categories:

| Category | Obligations |
|----------|-------------|
| **Scope Delivery** | Design deliverables, shop drawings, IFC/AFC docs, material samples, O&M manuals, as-built docs |
| **Commercial** | Fixed lump-sum, milestone payment, performance bond, bank guarantee, price fixed term, variation mechanism |
| **Insurance & Liability** | PI insurance amount, liability cap, warranty period, defect correction obligation, IP indemnity |
| **IP & Confidentiality** | IP ownership model (assigned/joint/license), native files delivery, confidentiality, non-infringement warranty |
| **Compliance** | Saudi Building Code, SCE-registered staff, local content, authority NOCs, CG approval required |
| **Termination** | For cause (breach), for convenience, force majeure period, suspension rights, post-termination handover |

Use a matrix table with specialists as columns and obligations as rows. Mark each cell: ✅ (present), ❌ (absent), — (N/A), or the specific value (e.g. "£2M", "200% fee").

## Phase 8: Build Master Contracts Register System

After discovery and matrix, set up a cross-project master register:

```
CONTRACTS_REGISTER.md          ← master index (all projects)
PROJECTS/<project>/contracts/  ← per-project detail + extracted agreements
  ├── README.md                ← full contract inventory with key terms
  ├── obligations_matrix.md   ← obligations matrix for this project
  ├── <specialist>_scope_of_work.md  ← per-specialist SOW docs
  └── <Project>_Contract_Register.docx  ← formatted Word report
```

### Per-project reference files
Each project repo gets a `CONTRACTS_REF.md` in its `00_Contracts/` folder pointing to the master register. This lets any agent working in a project repo find the master system.

### AGENTS.md update
Add a "Contracts Register System" section to the workspace `AGENTS.md` so every agent knows the system exists on first load.

## Phase 9: Generate DOCX Report

Use the `docx` skill (npm package) to generate a formatted Word document from the contract data:

```javascript
const docx = require('docx');
const { Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell,
  WidthType, AlignmentType, HeadingLevel, ShadingType, BorderStyle,
  Header, Footer, PageNumber } = docx;
```

Include:
- **Title page** with project name, document title, date, revision
- **Table of Contents** (auto-generated from heading levels)
- **Contract Summary table** — all specialists with status, value, signed date, key terms
- **Obligations Matrix tables** — one per category (Scope, Commercial, Insurance, IP)
- **Key Contract Terms** — detailed tables per contract (parties, value, liability cap, IP, etc.)
- **Per-specialist SOW** — scope summary, deliverables table, key interfaces, exclusions
- **Critical Gaps & Risks** — table with risk level, specialist, impact description
- **Submission Plans Status** — per discipline with status
- **Headers/Footers** with page numbers
- **Brand colors** — navy (#1F3864) headers, gold (#C5A55A) accents, alternating row shading

## Phase 10: Document Per-Specialist SOW

For each specialist without a signed contract, create a scope-of-work document:

```markdown
# <Specialist> — Scope of Work

> **Project:** Aseer Regional Museum
> **Status:** 🟡 Prequalifying / ⚠️ Draft / ❌ No contract
> **Candidates:** ...

## 1. Scope Summary
| Item | Description | SoW Reference |

## 2. Deliverables
| Ref | Deliverable | Due | Acceptance |

## 3. Key Interfaces
| Trade | Coordination Item |

## 4. Exclusions
```

## Contract Status Report Template

When building the final report, use this structure:

1. **Summary table** — all specialists with status (✅ Signed / ⚠️ Draft / ⚠️ Proposal only / ❌ Not found)
2. **Obligations matrix** — per-category tables covering scope, commercial, insurance, IP, compliance, termination
3. **Per-contract detail** — parties, date, value, key terms (fee, liability cap, IP, termination, governing law, insurance)
4. **Per-specialist SOW** — scope summary, deliverables, interfaces, exclusions
5. **Submission plans** — per discipline, with status
6. **Key gaps & risks** — which contracts are missing, which submission plans don't exist
7. **Extracted attachments** — files pulled from Outlook that should be saved to repo

## Multi-Project Email Pipeline

The user corrected that the email pipeline should scan ALL project emails, not just Aseer Museum. When setting up or updating the pipeline cron job, use a multi-project prompt that checks all project folders and classifies by document code prefix:

| Prefix | Project |
|--------|---------|
| `MOC-MUS-ASE`, `MOC-ASEER-SIC` | Aseer Museum |
| `ZAM-NWC`, `ZAM-` | Zamzam Visitor Center |
| `AL JALAL`, `JALAL` | Al Galal & Al Gamal (Jabal Omar retail) |

The cron job name should reflect this — "Project Email Pipeline" not "Aseer Email Pipeline".
