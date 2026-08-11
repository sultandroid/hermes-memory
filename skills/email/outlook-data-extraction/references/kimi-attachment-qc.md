# Kimi QC of Extracted Email Attachments (v0.23.3)

Workflow for "read all attachments" + QC via kimi, proven 2026-08-11 on an 11-email Aseer/Zamzam batch.

## 1. Extract attachments to /tmp

Use the Python AppleScript generator (one `.applescript` per email ID, under the ~700-byte limit), then run each via `osascript`. Output lands in `/tmp/email_attachments/`.

## 2. Pre-read the key files yourself (fast, cheap)

Before delegating, extract text/OCR the critical docs so you can verify kimi's report and report even if kimi times out:
- `pdftotext -layout` for text PDFs
- `pdftoppm` + `tesseract -l ara+eng` for scanned Arabic forms
- `openpyxl` for Excel schedules/metadata templates

## 3. Delegate the QC pass to kimi

**Kimi v0.23.3 flags (verify with `kimi --help`):**
- `-p, --prompt <task>` IS the prompt flag — pass the task as a string argument.
- `--output-format text` for clean output.
- `--yolo` CANNOT combine with `--prompt` (`error: Cannot combine --prompt with --yolo`).
- The old `--print` / `--quiet` / `-y` / `--max-steps-per-turn` / `--afk` / `-f` flags NO LONGER EXIST in v0.23.3.

**Pitfall — large multi-file QC prompts time out (>300s).** A single `kimi -p` prompt asking it to read+OCR+QC 10+ attachments exceeds the foreground timeout. Run in background with output redirected, then read the file:

```bash
kimi -p "$(cat /tmp/qc_task.txt)" --output-format text > /tmp/kimi_out.txt 2>&1
# terminal(background=true, notify_on_complete=true), then read /tmp/kimi_out.txt
```

Kimi is agentic in prompt mode: it reads files, runs OCR, and writes a report (e.g. `QC_Report.md`) into the workdir. Point it at the `/tmp` staging dir so its output lands where you can read it back.

## 4. QC report shape

Give kimi a per-doc verdict list (OK / ACTION NEEDED / FLAG) + key findings + inconsistencies. For a construction email batch, the report should cover: submittal refs, CG codes, HSE observations with risk ratings, Aconex metadata completeness, vendor offer terms (fee/duration/validity/exclusions), MEP clearance forms, and schedule-approval codes.

## Pitfalls

- **Image-based PDFs return empty `pdftotext`** — OCR with `pdftoppm` + `tesseract -l ara+eng`. Run tesseract from `/tmp` (it fails to open files in some subdirs).
- **CG/consultant review code is a checked box, not text** — OCR the "Review Result" region to confirm A/B/C/D.
- **Nested/unsaveable attachments save as 0-byte files** (e.g. a `.zip` CAD) — flag for manual open in Outlook, don't retry.
- **Excel "982 rows" is often a formatting remnant** — only a few rows hold data; check `max_row` vs actual populated cells.
