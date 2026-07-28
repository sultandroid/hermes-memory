---
name: document-intake-pipeline
title: Master Document Intake & Register Update Pipeline
description: Process any incoming document (PDF, DOCX, XLSX, MD, email) — extract text, classify type, update all relevant registers (submittal, NCR, RFI, risk JSON, lessons learned, etc.), and push to GitHub. Supports full retroactive backfill and daily incremental scans.
---

## When to use

Any time a document arrives (email attachment, uploaded file, Aconex transmittal, new file in repo) and needs to be:
- Classified by type (IR, NCR, ZD, PQ, Contract, Plan, Invoice, RFI, SI, Letter, MoM, etc.)
- Extracted for key fields (dates, references, status codes, parties, amounts)
- Linked to affected risk register entries
- Logged in the appropriate markdown registers

## Script location

`scripts/document_intake.py` in the repo root (`~/aseer-museum-pm/`).

## Commands

```bash
# First run — full retroactive scan of ALL repo directories
python3 scripts/document_intake.py --backfill

# Daily — incremental scan (new/changed files only, tracked by hash)
python3 scripts/document_intake.py --incremental

# Single file
python3 scripts/document_intake.py --file path/to/document.pdf

# Scan a specific directory
python3 scripts/document_intake.py --scan-dir 05_Comms
```

## Pipeline steps

1. **Extract text** — supports PDF (PyPDF2), DOCX (python-docx), XLSX (openpyxl), TXT/MD/CSV/JSON/YAML, HTML
2. **Classify** — 20+ document types matched by regex patterns on filename + content
3. **Extract fields** — dates, MOC-MUS-ASE refs, status codes (A/B/C/D), SAR amounts, party names
4. **Determine risk impacts** — keyword-to-risk-ID mapping (e.g. "brass" → PRR-PRC-05, "oddy" → DDR-MAT-001)
5. **Update registers** — appends rows to markdown tables in `01_Registers/`, `05_Comms/`, `Technical_Office/`
6. **Update risk JSONs** — adds evidence + history entries to `risks.json`, `ddr_risks.json`, `hse_risks.json`
7. **Mark processed** — records file hash in `.sync_state.json` for dedup

## Supported document types (20+)

| Type | Registers Updated |
|------|-------------------|
| IR (Inspection Request) | risk_register, submittal_register, ncr_register |
| NCR (Non-Conformance) | ncr_register, risk_register, lessons_learned_register |
| ZD (Submittal) | submittal_register, deliverables_register, risk_register |
| PQ (Prequalification) | prequalification_register, subcontractor_package_register, specialist_register |
| Contract / SOW | subcontractor_sow_raci_register, procurement_package_register, risk_register, change_register |
| Plan | plan_tracker, approval_log, risk_register |
| Invoice | invoice_register, invoice_log, procurement_package_register |
| RFI | rfi_register, risk_register |
| SI (Site Instruction) | si_register, change_register, risk_register |
| Letter | correspondence_register, letters_register, risk_register |
| MoM (Minutes) | meeting_minutes_register, decisions_log, risk_register, lessons_learned_register |
| Email | outlook_mail_register, correspondence_register, risk_register |
| Progress Report | daily_report_register, project_status, risk_register |
| Method Statement | method_statement_register, risk_register |
| Drawing | drawing_register, arch_drawing_register, submittal_register |
| BOQ / Quantity | boq_quantity_register, change_register, procurement_package_register |
| Change Order / VO | change_register, cost_register, risk_register |
| Handover | handover_register, commissioning_register, risk_register |
| Specialist / Subcontractor | specialist_register, subcontractor_package_register, sow_raci_register, prequalification_register |
| BIM / Model | bim_coordination_log, clash_register, model_release_log |
| Quality / Testing | qa_testing_log, defects_register, risk_register, lessons_learned_register |

## State tracking

`.sync_state.json` in repo root tracks:
- `last_full_scan` — timestamp of last backfill
- `last_incremental_scan` — timestamp of last incremental run
- `processed_files` — dict of `{sha256_hash: {path, timestamp}}` for dedup
- `registers_updated` — list of register names touched
- `documents_processed` — cumulative count

Files are skipped if their hash matches a previously processed entry (incremental mode). If a file changes (new hash), it's re-processed.

## Risk impact mapping

The script has a keyword-to-risk-ID map covering ~40 risk IDs across PRR, DDR, HSE, and AVR registers. When a document mentions a keyword (e.g. "showcase", "glasbau", "mep", "oddy"), the corresponding risk gets an evidence entry appended.

## Pitfalls

- **risk_register mapping uses `{prefix}_risks.json`** — the `risk_register` entry in `REGISTER_FILES` has a `{prefix}` placeholder that isn't resolved. The script falls through to the direct `RISK_JSON_MAP` for risk updates, but the register update step logs a "file not found" warning. This is cosmetic — risk JSONs are still updated correctly.
- **Some risk IDs not found in JSON** — PRR-VO-001, PRR-SI-001, PRR-NCR-001 don't exist in the current `risks.json`. The script logs `✗ Risk not found` and continues. These may need to be added to the risk register if they represent real risks.
- **Classification is regex-based** — a README.md containing "Contract" gets classified as Contract. The script picks the highest-scoring type. For ambiguous files, the classification may be wrong — review the output.
- **Markdown table appending** — inserts a row after the `|---|` separator line. If the table has no separator, the append fails. All standard registers have this.
- **Pre-commit hook blocks 00_Contracts/** — if backfill processes contract files, `git add -A` will stage them and the commit will fail. Use `git reset HEAD 00_Contracts/` before committing.
- **Post-commit hook modifies risks.json** — after commit, the hook regenerates `risks.json`. Use `git stash` before `git pull --rebase`.
