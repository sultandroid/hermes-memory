---
name: email-intel-batch-processing
description: "Process project emails in batches — read bodies, update registers, commit. Covers the Email Intel system (hermes-memory/email_intel/) and the batch email→register workflow for Aseer/Samaya projects."
tags:
  - email
  - outlook
  - registers
  - batch
  - aseer
  - email-intel
---

# Email Intel & Batch Email→Register Processing

Two related workflows for handling project email at scale on this machine.

## 1. The Email Intel System (hermes-memory/email_intel/)

A **cross-project email intelligence layer** in the hub repo `sultandroid/hermes-memory/email_intel/` — NOT inside any single project repo. Classifies senders, routes emails to project repos, analyzes behavior/replies, raises issues. File-only: MD + JSON, no binaries.

### Directory layout
```
hermes-memory/email_intel/
├── README.md                  # full spec + Mac Pro agent contract
├── contacts.json              # sender/contact classification (role, project, trust)
├── projects.json              # project routing map (email → repo)
├── inbox/                     # one .md per ingested email (YYYY-MM-DD-<sender>-<subject>.md)
├── behavior/sender_profiles.json
├── threads/THREAD-*.md
├── issues/ISSUE-NNN.md
└── archive/                   # processed/closed (append-only)
```

### Scripts (in hermes-memory/scripts/)
- `email_intel_agent.py` — full pipeline: `--run`, `--plan` (dry-run), `--ingest FILE`, `--behavior`, `--issues`.
- `email_intel_backfill.py` — reads legacy `email_scan_*.md` reports, extracts (sender, subject) pairs, writes normalized inbox files.
- `email_intel_outlook_backfill.py` — pulls project-relevant emails DIRECTLY from Outlook SQLite for a date window (scan reports only go back ~Jul 15; Outlook has data back to April+).

### ⚠️ CRITICAL: backfill files are HEADER-ONLY
The backfill importer writes only `From / Subject / Date / Project / Source` — **no email body, no attachments**. Median file ~350 bytes. The Email Intel system is a **metadata index**, not a content reader. Its "issues" are **keyword flags on subject lines only**, not real understanding.

To actually READ content, pull from Outlook SQLite:
- `Message_Preview` — first ~255 chars of body (enough for CG codes, submittal intent).
- Full body → AppleScript `plain text content of msg` (see `outlook-email` skill).
- Attachments → AppleScript extraction (see `outlook-email` skill).

### Pitfalls (both fixed 2026-08-15)
1. **Backfill date bug**: `email_intel_backfill.py` originally stamped `datetime.now()` on every file instead of the scan file's date (`email_scan_YYYY-MM-DD.md`), creating hundreds of misdated duplicates. Fix: parse the date from the source filename. When re-running a corrected backfill, dedup by removing files whose `Date:` header doesn't match their `Source:` scan date.
2. **Broken `email_ref` in issues**: `email_intel_agent.py` wrote `email_ref: inbox/{slugified-subject}.md` but actual files are `{date}-{sender}-{subject}.md`. Fix: match the subject slug against actual inbox filenames before writing the ref.
3. **Scripts get deleted by auto-sync**: the `memory_skills_exchange.sh` cron has deleted `email_intel_agent.py`/`email_intel_backfill.py` more than once. If missing, restore from git history (`git show <commit>:scripts/email_intel_agent.py`).

## 2. Batch Email→Register Processing Workflow (the "read 10, update, commit" loop)

When the user asks to "read and understand all emails for updating registers/projects", do NOT try to process everything at once. Loop in batches of 10:

1. **Query Outlook SQLite** for project-critical emails in a date window (JOIN folders, filter by MOC/Aseer/Museum subject + key sender names, `Message_Hidden=0`). Order DESC by time.
2. **Read the bodies** of the 10 most recent (via `Message_Preview`; full body via AppleScript if needed).
3. **Check register state** for each doc ref (PQ/ZD/1G/LT/SI/SOR/INV) before editing — many are already logged; only add/update what's new.
4. **Update registers**: prequalification, submittal, letters, invoice, si, sor, subcontractor_package, action_items.
5. **Commit each batch** with a dated message (`Email batch N (DD-MM): <summary> - YYYY-MM-DD`).
6. **Skip non-project emails** (Zamzam = separate project per entity isolation; marketing/ERP/notifications).

### Pitfalls (batch loop)
- **Issue detector over-raises — do NOT treat issue count as a status metric.** After a big backfill, `email_intel_agent.py --issues` explodes to 300+ "reply-required" flags because it keyword-matches ANY email containing urgent/please/action/confirm. These are raw flags, not verified action items — many are already handled in the registers. Triage before reporting them as actionable; the system is a historical index until triaged.
- **`git add -A` in `aseer-museum-pm` will sweep sibling-agent + hook-generated dirt** (`.sync_state.json`, `06_Risk_System/webapp/src/index.html`, `compliance_matrix.md`, `adel_snapshots/file_list.txt`). Only `git add` the specific register files you edited (`01_Registers/ 00_Status/` etc.), not the whole tree, to avoid committing another agent's in-flight work.
- **Register row prefix consistency**: table rows in some registers use single `|` (SOR) while others use `||`/`|||` (nested sections). When patching, match the EXACT existing prefix of the target row — introducing a mismatched prefix (e.g. `||` into a `|` table) breaks the markdown table. Re-read the row before writing.
- **Verify CG codes from the actual email preview, not the register's stale row.** When an old register row says `U`/`DA`/`Submitted` but a CG response email arrived, the code in the body (A/B/C/D) is authoritative — update the row with the real code + date from the preview.
- **Attachments are the unread layer.** Bodies are read via `Message_Preview`, but actual PDF/Excel attachments (CG comment sheets, contracts, drawings) are NOT extracted in this loop. For Code C/D CG responses the reviewer comments live in the attachment — flag for a separate extraction pass.

### Key sender→role map (Aseer)
- Hossam Mabrouk / Mohammad Elbaz / Mansour Alrezeni / Maged Zamzam — CG (PMC)
- Jim Richards / Francesco Bitelli — NRS (design lead)
- Hesham Abdelhameed — document control / submittals
- Waris Sultan Khan — project manager / contracts
- Adel Darwish — projects director / EOT / invoices
- Ali Abdelrahman — architectural engineer / material inquiries
- Shihab Mohamed / Soliman Obiya — AV/IT / acoustic subcontractors
- Mohamed Mustafa / Talha Yousaf — MEP / HVAC
- Mohamed Habib — Zamzam (separate project — do NOT log in Aseer registers)

## Related
- `outlook-email` skill — SQLite queries, AppleScript body/attachment extraction, CG code reading from previews.
- `email-pipeline-automation` / `aseer-email-routing` — the older per-project pipeline + routing tables.
