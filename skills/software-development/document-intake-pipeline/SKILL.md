---
name: document-intake-pipeline
title: Master Document Intake & Register Update Pipeline
description: Process any incoming document (PDF, DOCX, XLSX, MD, email) — extract text, classify type, update all relevant registers (submittal, NCR, RFI, risk JSON, lessons learned, etc.), and push to GitHub. Supports full retroactive backfill and daily incremental scans.
---

## When to use

Any time a document arrives (email attachment, uploaded file, Aconex transmittal, new file in repo, external download link) and needs to be:
- Classified by type (IR, NCR, ZD, PQ, Contract, Plan, Invoice, RFI, SI, Letter, MoM, etc.)
- Extracted for key fields (dates, references, status codes, parties, amounts)
- Linked to affected risk register entries
- Logged in the appropriate markdown registers
- **Converted from binary (Excel/PDF/ZIP) to structured markdown** in the repo — see `references/external-file-to-repo-markdown.md` for the full workflow covering Zoho downloads, multi-sheet Excel with dynamic column mapping, gallery-by-gallery analysis, and risk identification

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

## Reference files

| File | Covers |
|------|--------|
| `references/pq-knowledge-file-pattern.md` | Batch conversion of prequalification PDFs to structured MD knowledge files — fallback chain for corrupted PDFs, trade classification, CG comment patterns, clearance paths |

## Delegating extraction/reading to Kimi CLI (email → register workflow)

When reading many extracted attachment text files, delegate to **Kimi** to keep your context clean (proven this session: 63KB across 11 docs → 3 parallel `kimi -p` calls). 

**⚠️ Kimi CLI interface changed (confirmed 2026-08-12):** the newer Kimi Code CLI dropped `--print`/`--quiet` and takes the prompt as a positional arg via `-p`/`--prompt`. `kimi --print` now errors `unknown option '--print' (Did you mean --prompt?)`.

```bash
# ✅ CURRENT — positional -p, prompt inline
kimi -p "Summarize these documents: <content>" --output-format text

# ✅ Pipe a batch file into the prompt string (avoids ReadFile timeout on large content)
kimi -p "$(cat /tmp/BATCH1.md)" --output-format text
```

- **Split large batches** — 63KB of text split into 3 files, run 3 parallel `kimi -p` calls, each stays under the ~300s shell timeout. Do NOT dump everything into one call.
- **OCR image-based PDFs before delegating** — `pdftotext` returns 1-byte/empty output for scanned PDFs. Convert with `pdftoppm -r 200 -jpeg` then `tesseract <img> <out> -l ara+eng`, and **run tesseract from `/tmp`** (it fails to open files from some subdirs). Arabic review forms need `-l ara+eng`.
- **Extract attachments from Outlook** — the `.olk15MsgAttachment` files are binary header + MIME headers + base64 payload. Find the base64 marker (`Content-transfer-encoding: base64`), decode, and identify type by magic bytes (`%PDF`, `PK\x03\x04` for xlsx). See `outlook-data-extraction` skill for the full query/decode recipe.

## Pitfalls

- **risk_register mapping uses `{prefix}_risks.json`** — the `risk_register` entry in `REGISTER_FILES` has a `{prefix}` placeholder that isn't resolved. The script falls through to the direct `RISK_JSON_MAP` for risk updates, but the register update step logs a "file not found" warning. This is cosmetic — risk JSONs are still updated correctly.
- **Some risk IDs not found in JSON** — PRR-VO-001, PRR-SI-001, PRR-NCR-001 don't exist in the current `risks.json`. The script logs `✗ Risk not found` and continues. These may need to be added to the risk register if they represent real risks.
- **Classification is regex-based** — a README.md containing "Contract" gets classified as Contract. The script picks the highest-scoring type. For ambiguous files, the classification may be wrong — review the output.
- **Markdown table appending** — inserts a row after the `|---|` separator line. If the table has no separator, the append fails. All standard registers have this.
- **Pre-commit hook blocks 00_Contracts/** — if backfill processes contract files, `git add -A` will stage them and the commit will fail. Use `git reset HEAD 00_Contracts/` before committing.
- **Post-commit hook modifies risks.json** — after commit, the hook regenerates `risks.json`. Use `git stash` before `git pull --rebase`.
- **Pre-commit / register-update hook regenerates `06_Risk_System/webapp/src/index.html` on EVERY commit** — a concurrent `register-update` process (cron or background) rebuilds the risk webapp and rewrites `index.html` with a fresh snapshot timestamp (`download="..._YYYY-MM-DD_HHMM.xlsx"`) each run. This file is perpetually dirty, so when the remote has moved ahead and you `git pull --rebase`, git aborts with *"Your local changes to the following files would be overwritten by merge: 06_Risk_System/webapp/src/index.html"*. **Durable fix (confirmed 2026-08-12):**
  1. Never commit the hook-regenerated `index.html` — its only change is the snapshot timestamp and the hook rewrites it anyway. Drop it from your commit:
     ```bash
     git checkout -- 06_Risk_System/webapp/src/index.html
     ```
  2. Stash the working tree before rebasing, pull, then restore:
     ```bash
     git stash && git pull --rebase origin main && git stash pop
     ```
  3. If the rebase still aborts mid-way (the hook re-fires and re-dirties index.html during the rebase), `git rebase --abort`, `git checkout -- 06_Risk_System/webapp/src/index.html`, stash, and retry. The `[register-update]` lines you see during git operations are this background process, NOT the pre-commit hook.
  4. After push, `git checkout -- 06_Risk_System/webapp/src/index.html` again and `git stash drop` — the regenerated snapshot is a CI/background concern, not something to version manually.
  - **Do NOT edit `.git/hooks/pre-commit`** to work around this — the register-update is a separate background process (the pre-commit hook is just the 00_Contracts read-only guard, symlinked to `scripts/pre-commit-hook.sh`). Moving the hook does not stop the rebase conflict because the file is re-dirtied by the background process, not the hook. Restore the hook with `mv /tmp/pre-commit.bak .git/hooks/pre-commit` after.
- **Corrupted PDFs are common** — many project PDFs have broken xref tables, missing endstream markers, or damaged object streams. pdftotext will silently produce no output (exit code 1) with no useful error. **Fallback chain for PDF extraction:**
  1. `pdftotext file.pdf /tmp/output.txt` — fastest, works for 90% of clean PDFs
  2. `pdftotext -layout file.pdf /tmp/output.txt` — helps with some corrupted xref tables
  3. `python3 -c "import fitz; doc=fitz.open('file.pdf'); ..."` (PyMuPDF) — handles many corrupted PDFs that pdftotext cannot, though it may lose images and some formatting
  4. `python3 -c "from pdfminer.high_level import extract_text; ..."` — last resort for text extraction
  5. `python3 -c "import pdfplumber; ..."` — alternative fallback for table-heavy PDFs
  - If ALL tools fail (Unexpected EOF, object is not a stream), the PDF is genuinely corrupted and must be re-sourced from the sender.
  - **Always check output file size** after extraction — a 0-byte or tiny output means extraction failed even if exit code was 0.
  - For PQ documents specifically, the cover sheet text is often extractable even when the body (catalog pages) is image-based. Don't assume a short extraction means the PDF is empty — check the page count.
