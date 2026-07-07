# Steady-State Verification Pattern (Parallel Sub-Agent Decomposition)

## When to Use

The pipeline has **no new files to copy** — all attachments in `mails/attachments/` are already filed in BIM OneDrive. You still need to:

1. Verify nothing was missed (cross-reference against all BIM targets)
2. Check for new `.md` email archive files with project updates
3. Update PROJECT_MEMORY.md with new CG codes or findings
4. Produce a report (cron instructions demand it, or running interactively)

The "backlog pattern" (`batch-inventory-comparison.md`) assumes a Phase 2 copy step. The steady-state pattern skips that entirely because the comparison itself is done within each sub-agent's independent scope.

## Decomposition (3 parallel sub-agents, no sequential phase)

This pattern works **only** when all attachments are expected to be already filed. Each sub-agent independently verifies one aspect of the pipeline and returns a structured summary. The leader synthesizes.

### Sub-Agent Tasks (run concurrently via `delegate_task(tasks=[...])`)

| Task | Scope | Goal | Output |
|------|-------|------|--------|
| **Task 1** | Aseer-Museum OneDrive (`Aseer-Museum/`) | Inventory 6 target BIM subfolders against attachment filenames. Confirm all already filed or flag gaps. | File count per subfolder, cross-reference result, any unfiled files |
| **Task 2** | Zamzam Museum OneDrive (`Zamzam Museum/Docs/03_Inspection_Requests/`) | Inventory inspection requests. Cross-reference against Zamzam attachments. | File count, cross-reference result, any unfiled files |
| **Task 3** | Email archive (`mails/23.md` or latest) | Extract structured project findings: CG codes, meeting outcomes, new submittals, key contacts | Markdown summary formatted for PROJECT_MEMORY.md insertion |

### Leader Integration

```python
result = {
    "aseer_new_files": task1.summary["unfiled_count"],
    "zamzam_new_files": task2.summary["unfiled_count"],
    "email_findings": task3.summary,  # CG codes, meetings, contacts
}
if all(count == 0 for count in [result["aseer_new_files"], result["zamzam_new_files"]]):
    # Steady state confirmed — proceed to PROJECT_MEMORY.md update
    if result["email_findings"] has new data:
        patch PROJECT_MEMORY.md
    produce_final_report(result)
```

### Key Differences from Backlog Pattern

| Aspect | Backlog Pattern (`batch-inventory-comparison.md`) | Steady-State Pattern (this file) |
|--------|--------------------------------------------------|-----------------------------------|
| **Phase count** | 2 (3 parallel + 1 sequential) | 1 (3 parallel, all independent) |
| **Copy step** | Required — `cat` workaround to OneDrive | None — all files already present |
| **Sub-agent focus** | Inventory only (filenames + sizes + mtimes) | Inventory + content extraction |
| **PROJECT_MEMORY.md update** | Phase 2 sub-agent or leader | Leader after collecting all results |
| **When to use** | New emails likely downloaded | Pipeline confirms no new activity |

## Confirmed Run (Jun 7, 2026)

**Outcome:** All 22 attachment files across 7 subdirectories already present in BIM OneDrive. PROJECT_MEMORY.md updated with 5 new CG code entries + 7 project updates from 23.md.

**Sub-agent timing:**

| Task | Duration | Files Scanned | New Files Found |
|------|----------|---------------|-----------------|
| Aseer inventory (6 subfolders) | 36s | ~13,631 (across 6 dirs) | 0 |
| Zamzam inventory (Inspection_Requests) | 37s | 435 inspection request files | 0 |
| Email extraction (23.md, 5K lines) | 95s | 178KB, 5025 lines | 11 CG codes + meeting data + structural data |

## Confirmed Run (Jun 8, 2026 — Post-Catchup Steady State)

**Context:** Two earlier Jun 8 runs had filed 63+ new attachments from a backlog of 208. This third run found **everything already processed** — a true post-catchup double steady state (0 emails + 0 new attachments).

**Outcome:** Zero new items across all checks. PROJECT_MEMORY.md already up-to-date with WEEK24_EMAIL_UPDATE.md companion file in place. No updates applied.

**Key pattern difference from Jun 7:** Three BIM correspondence locations needed cross-referencing, not one:

| Location | Purpose |
|----------|---------|
| `Aseer-Museum/09_Correspondence/` | Current active correspondence |
| `Aseer-Museum/Correspondence/` | Legacy root-level correspondence |
| `Aseer-Museum/Completed Tender Package From NRS/05_Correspondence_Archive/` | Archive from NRS tender package |

Files may exist in any one of these but be absent from the others. A `find` across only one misses true duplicates. The triple cross-reference is required for confident dedup.

**Additional checks that proved negative:**

| Check | Result | Method |
|-------|--------|--------|
| Aseer correspondence (25 files) | All pre-filed | `find -name` across 3 correspondence locations |
| Aseer reports/drawings/other (17 files) | All pre-filed | `find -name` across Design Files, 07_Daily_Reports, 09_Correspondence, 02_Submittals |
| Zamzam correspondence (14 files) | All pre-filed | `find -name` across Zamzam Correspondence + Docs/03_Inspection_Requests |
| `attachments_summary.md` | **Empty** (0 lines, 738-byte stub) | read_file showed no content — indicates prior cleanup completed |
| `23.md` latest archive | Already mined for CG codes | WEEK24_EMAIL_UPDATE.md + PROJECT_MEMORY.md both current |
| `download_mails.py` | 0 new emails (AppleScript -1728 fail) | Ran from `scripts/download_mails.py` — correct path, expected failure |

**Pitfall reconfirmed — filename prefix variants cause false positives:** Using `find -name "MOC-ASEER-1C0-SNA-002.pdf"` missed the actual file `MOC-MUS-ASE-1C0-SNA-002.pdf` which was already present in 4 BIM locations. When the extracted attachment filename has a different prefix than the actual file (e.g. `MOC-ASEER-` vs `MOC-MUS-ASE-`), `find -name` returns no results and produces a false positive. Always use substring matching (`find -name "*1C0*SNA*"`) for dedup when prefix variants are known to exist.

## Pitfalls

- **Don't assume steady state.** Always run full inventory scans — the finding "0 new files" must come from actual comparison, not from skipping the scan. The 06-07 session found files in `attachments/` subdirectories that appeared new — only cross-referencing against BIM OneDrive proved they were already filed.
- **Aseer-Museum scale:** 106,224 files total across the project. The 6 target subfolders contain ~13,600 files. Budget ~35s per sub-agent.
- **`download_mails.py` may timeout.** Its timeout doesn't mean no new emails — it means AppleScript is broken. The weekly `.md` archives from previous successful runs are the authoritative source for project updates. Don't block on the download script.
- **Archive freshness:** Check `ls -lt ~/Documents/04_Outlook_Connection/mails/*.md | head -3` to find the most recent archive. The watchdog state at `scripts/.outlook_watch_state.json` provides the `last_id` watermark.
- **Write success ≠ read success:** PROJECT_MEMORY.md writes can succeed even when reads fail (OneDrive write/read asymmetry). Always attempt the `patch`. Fall back to staged updates only on actual error.
- **7-folder scan is insufficient for confident dedup (confirmed Jun 9, 2026):** Scanning only the 7 specified target folders misses ~17.5% of pre-filed files that live in other BIM directories (HR/, _References/, Jabal Omar/, El-Haramain/, Al Galal/, etc.). A full-tree fallback scan (`find -name "*<basename>*"` across the entire BIM Unit tree) catches these. After the 7-folder pass, always run a broad `find` across the full BIM unit root for any basename still unaccounted. This adds ~60-90s but eliminates false positive "new" declarations.
