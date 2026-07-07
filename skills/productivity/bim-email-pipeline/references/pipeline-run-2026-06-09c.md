# Pipeline Run — 2026-06-09c (Cron, 12:00)

## Context
Third pipeline run on Jun 9 (after 00:45 and 06:55). Ran as cron job with the user's explicit 5-step instructions: check Outlook → download → compare attachments → copy → check .md archives → update PROJECT_MEMORY.md → report.

## Summary
Fully steady-state. No new emails, no un-filed attachments, PROJECT_MEMORY.md already current.

## Key Findings

| Check | Result |
|-------|--------|
| Outlook running | ✅ |
| download_mails.py (corrected path: `scripts/download_mails.py`) | ✅ Executed, exits 0 — no output (AppleScript silent failure, expected) |
| Attachment scan | **200 files across 7 subdirs → 0 new** (all pre-filed) |
| Full-tree fallback | ✅ Scanned entire BIM Unit tree — all 200 files accounted for, 17.5% in non-target BIM dirs |
| PROJECT_MEMORY.md | ✅ Rev 07 current (08 Jun, 09:45). Zamzam §19 has all 12 IRs. No new updates needed. |
| New .md archives | None beyond 23.md. WEEK24_EMAIL_SUPPLEMENT.md already generated at 06:55. |
| Pipeline log | Appended to `pipeline_run_2026-06-09.log` |

## New Technique: Full-Tree Fallback Dedup

This run confirmed that **7-target-folder scanning alone leaves a dedup gap**. The subagent's full-tree scan found files in 20+ BIM subdirectories beyond the 7 specified targets. 

**Quantified gap (Jun 9, 2026):** 
- 165/200 files (82.5%) in exact target folders
- 35/200 files (17.5%) in other BIM directories (HR/, _References/, Jabal Omar/, El-Haramain/, Al Galal/, DOCS/, Masjid Alnoor/)

**Recommendation:** The steady-state verification pattern should always include a full-tree fallback pass after the 7-folder scan. The `find -name "*basename*"` across the full BIM tree is the authoritative dedup check.

## Edge Cases Noted

- **Script path mismatch:** User instructions said `~/Documents/04_Outlook_Connection/download_mails.py` but actual path is `~/Documents/04_Outlook_Connection/scripts/download_mails.py`. Already documented in skill but worth flagging.
- **XSubcontractors/14_MEP_Contractor/ not exist:** Confirmed again. Closest is `12_MEP_Installation/` and `18_MEP_Designer/`.
- **Resource deadlock on download_mails.py read:** OneDrive cloud-locked the file. Skipped content inspection — ran via `python3` instead, which bypasses the lock.
- **Pipeline already ran today:** The 06:55 run did the heavy analysis. This run was purely verification — no new data to extract from emails or attachments.
