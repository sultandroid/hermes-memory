---
name: contracts-register-system
title: Samaya Contracts Register System
description: Master contracts register across all Samaya projects — CONTRACTS_REGISTER.md at repo root, per-project detail folders, obligations matrix, SOW documents, and cross-references from project repos.
tags:
  - contracts
  - subcontractors
  - register
  - samaya
  - aseer
---

## When to Use

This skill governs the **contracts register system** for all Samaya projects. Use it when:

- The user asks to inventory, audit, or report on subcontract/specialist contracts
- You need to find a contract file, its status, or key terms
- You are generating a contract register document (DOCX or MD)
- You need to add a new project to the system
- You need to generate a Scope of Work (SOW) for a specialist

## System Architecture

```
samaya-workspace/
├── CONTRACTS_REGISTER.md          ← Master index (all projects)
├── AGENTS.md                      ← System docs + agent instructions
└── PROJECTS/<project>/contracts/  ← Per-project detail
    ├── README.md                  ← Full contract inventory with key terms
    ├── obligations_matrix.md      ← Obligations per specialist (scope, commercial, insurance, IP, compliance, termination)
    ├── <Specialist>_SOW.docx      ← Scope of Work documents (SamayaDoc format)
    └── <extracted agreements>     ← PDFs/DOCXs extracted from email
```

Each project repo (e.g. `aseer-museum-pm`) has a `CONTRACTS_REF.md` in its `00_Contracts/` folder pointing to the master register.

## Rules

1. **Read-only.** Never modify contract files. Analysis goes in `03_Plans/` or `Technical_Office/`.
2. **Cite by reference.** Use `Contract Section 5 Art. 14` — do not copy contract text into other files.
3. **Update the master register** when a new contract is signed or status changes.
4. **Per-project detail** goes in `PROJECTS/<project>/contracts/README.md`.

## Workflow: Building a Contract Register

### Step 1 — Search Sources

Search in this order:
1. **OneDrive** `01_Contracts/` folder — existing signed contracts
2. **OneDrive** `24_Subcontractors/{NN}_{Specialist}/` — subcontractor folders
3. **Outlook SQLite** — email attachments with contract drafts/agreements
4. **Adel Darwish's OneDrive folder** — `Adel Darwish's files - 01- Execution Documents/`
5. **Project repo** (`aseer-museum-pm`) — existing registers and scope docs

### Step 2 — Extract Attachments (if needed)

Use the Python generator + AppleScript pattern from the `outlook-email` skill:
- Write a Python script to `/tmp/gen_extract.py` that generates individual `.applescript` files
- Run each with `osascript` (sequential, 5-6 per terminal call)
- Save to `/tmp/contract_attachments/`
- Read DOCX with `zipfile` + `word/document.xml` XML stripping
- Read PDF with `pdftotext` (or `python3 -c` with zipfile for DOCX)

### Step 3 — Build the Register

Per-contract fields to capture:

| Field | Description |
|-------|-------------|
| Parties | Client × Contractor |
| Contract No. | Reference number |
| Type | Consultancy, Supply, Construction, etc. |
| Value | Fee/price with currency |
| Signed Date | Date of execution |
| Term | Duration |
| Governing Law | Jurisdiction |
| Dispute Resolution | Courts or arbitration |
| Scope | Summary of services/works |
| Payment Terms | Milestones, percentages, conditions |
| Liability Cap | Aggregate limit |
| Insurance | PI, PL, other |
| IP | Ownership and license terms |
| Warranty | Period and scope |
| Termination | Notice periods, FM clauses |
| Key Conditions | CG approval gates, set-off rights, etc. |

### Step 4 — Generate Obligations Matrix

Create `obligations_matrix.md` with tables covering:

| Category | Rows |
|----------|------|
| Scope Delivery | Design deliverables, shop drawings, IFC, samples, O&M, as-built |
| Commercial | Fixed lump-sum, milestone payment, performance bond, bank guarantee, variation mechanism |
| Insurance & Liability | PI insurance, liability cap, warranty, defect correction, IP indemnity |
| IP & Confidentiality | IP ownership, native files delivery, confidentiality, non-infringement |
| Compliance | Saudi Building Code, SCE registration, local content, authority NOCs, CG approval |
| Termination | For cause, for convenience, force majeure, suspension, post-termination handover |

### Step 5 — Generate SOW Documents (SamayaDoc)

For each specialist that needs a SOW:
1. Load the `samaya-document-generation` skill
2. Use `SamayaDoc` from the style guide (`samaya_doc_template.py`)
3. Generate **separate** documents for Designer vs Supplier/Contractor
4. NEVER use emojis in formal documents — use text: Signed, Draft, Pending, Approved, Rejected
5. Use navy (`#1E293B`) header rows, alternating light gray (`#F1F5F9`) data rows
6. Save to `PROJECTS/<project>/contracts/`

### Step 6 — Commit

```bash
cd /Users/mohamedessa/samaya-workspace
git add CONTRACTS_REGISTER.md PROJECTS/<project>/contracts/
git commit -m "Update contracts register: <summary>"
git pull --rebase origin master
git push origin master
```

## Pitfalls

- **OneDrive files are often stubs** (cloud-only). Files show plausible sizes but fail `zipfile`/`pdftotext`. Copy to `/tmp/` first and verify with `file` command.
- **Signed PDFs are often scanned images** — `pdftotext` returns empty. Use OCR or read the DOCX draft version instead.
- **AD Engineering agreement was found in 3 identical copies** (email IDs 48453, 48456, 48422). Deduplicate by content hash.
- **NRS contract RAR archive** (6.1MB) needs `unar` to extract — `unrar` is not installed.
- **GBH DOCX files may be corrupted** (not valid ZIP archives). The signed PDF is the authoritative version.
- **Never use emojis in formal DOCX documents.** Text alternatives only.
- **Landscape scope splits into Designer + Supplier.** Two separate SOW documents, two separate doc references.
