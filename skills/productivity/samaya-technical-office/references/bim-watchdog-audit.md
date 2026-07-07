# BIM Watchdog Audit — 13 Recommendations (from Claude Code review)

## Verdict: CONDITIONALLY APPROVED

## Critical Fixes Applied
1. ✅ **Unsorted quarantine** — low-confidence files go to _UNSORTED/ (not Downloads)
2. ✅ **Extension allowlist** — only PDF, DOCX, XLSX, DWG, RVT, etc.
3. ✅ **Size cap** — 500MB max file size
4. ✅ **Lock file** — prevents overlapping cron runs
5. ✅ **Dry-run mode** (--plan)
6. ✅ **Duplicate detection** — checksum (+ filename fallback)
7. ✅ **Extension allowlist** in place

## Phase 2 — Implemented
5. ✅ **Daily summary notification** — implemented as a separate daily BIM todo cron job (see `references/daily-todo-workflow.md`). Delivers prioritized action items from email registers + watchdog file activity to Telegram at 05:00 Riyadh daily.

## Still To-Do (Phase 2)
1. □ **Claude Code delegation for analysis** — after move, trigger Claude for content extraction
2. □ **Excel register auto-update** — openpyxl atomic append (warn if file open)
3. □ **MD cache auto-creation** — after analysis, write .pdf.md sidecar
4. □ **Notion auto-update** — dedup by file hash before insert
6. □ **Excel format preservation rule** — append-only, don't rewrite existing formatting
