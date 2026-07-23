---
name: external-folder-register-sync
title: External Folder → Repo Register Sync
description: Scan external team member OneDrive folders (Adel Darwish, etc.) for new/changed files, filter historical backfill from genuinely new items, and update repo markdown registers (RFI, NCR, submittal, SI, prequalification, material submittal). Covers the detection script, subfolder-to-register mapping, date-based filtering, and register update patterns.
trigger: user asks to check a team member's OneDrive folder for new files, or a cron job fires for folder scanning
tags: [onedrive, register-sync, adel, folder-scan, cron, project-management]
---

## Workflow

### 1. Run the detection script

```bash
bash /Users/mohamedessa/aseer-museum-pm/scripts/check_adel_files.sh
```

The script outputs all files that differ from its last snapshot. **First run after a long gap will flag hundreds of historical files** — this is expected.

### 2. Filter for genuinely new items

The script output is massive (600K+ chars). Do NOT try to register everything. Instead:

- **Focus on files dated within the last 7 days** (or since the last cron run)
- Historical backfill (Dec 2025–Jun 2026) should be noted but NOT re-registered
- Use `ls -lt` on each subfolder to see actual modification dates
- Cross-reference against existing registers to avoid duplicates

### 2a. 7-Day Recency Filter (Script-Level)

The detection script (`check_adel_files.sh`) now includes a **7-day recency filter** that silently suppresses files older than 7 days. This prevents false positives when the snapshot file is reset or re-deployed. The filter uses `date -v -7d` on macOS to compare file mtime against the cutoff.

**Do NOT remove this filter.** Without it, a snapshot reset causes ALL files (including Feb–Apr 2026 historicals) to appear as "new" in the next cron run.

### 3. Subfolder-to-Register Mapping

| Adel Subfolder | Repo Register | Notes |
|---------------|---------------|-------|
| `05- Request For Information-RFI/` | `01_Registers/rfi_register.md` | TQ/RFI refs, status changes, CG replies |
| `12-NCR/` | `01_Registers/ncr_register.md` | NCR documents (may not exist as folder — NCRs may be in Letters attachments) |
| `07-Pre-Qualification Submittal/` | `01_Registers/prequalification_register.md` | May not exist in Adel's structure |
| `08-Material Submittal MA/` | `01_Registers/material_submittal_register.md` | May not exist |
| `09-Method Statement MWS/` | `01_Registers/submittal_register.md` | May not exist |
| `10- CG Site Instruction SI/` | `01_Registers/si_register.md` | SI documents |
| `11-IFC Drawing/` | `01_Registers/submittal_register.md` | IFC packages |
| `13-Weekly Report/` | — | Often empty — note and skip |
| `14-Inspection Request IR/` | — | Often empty — note and skip |
| `15-Start New Activity SNA/` | — | Often empty — note and skip |
| `17-SOR/` | — | Often empty — note and skip |
| `20- DDD/` | `01_Registers/submittal_register.md` | Design Development Drawings (1G-xxxx packages) |
| `01- Letters/` | Cross-ref to NCR/SI registers | Letters attachments may contain NCRs, CG replies, TQ responses |
| `06-Weekly Meeting MOM/` | `01_Registers/meeting_minutes_register.md` | Often empty in Adel's folder |

### 4. Check subfolder existence before scanning

Many expected subfolders may not exist in the team member's OneDrive. Use `ls` and check exit code before trying to scan contents:

```bash
ls -lt "/path/to/subfolder/" 2>/dev/null || echo "FOLDER NOT FOUND"
```

### 5. Update registers

For each genuinely new item:

- **RFI register**: Add new TQ rows, update status from "Open" to "CG response received" when Approval subfolder appears
- **Submittal register**: Add new DD packages (1G-xxxx), update status codes
- **NCR register**: Add new NCR rows, update source line
- **SI register**: Add new SI entries if new folders appear

### 6. Update the last_updated timestamp

Always bump the `last_updated` field in the YAML frontmatter of every register you modify.

## Pitfalls

- **First-run noise**: The script's first scan after a long gap flags ALL files as "new". Filter by modification date. Only items from the last 7 days are genuinely new.
- **Old files re-appearing after snapshot reset**: If the snapshot file is deleted or the script is re-deployed, ALL files appear as "new" again — including files from Feb–Apr 2026. The detection script now includes a **7-day recency filter** (`date -v -7d`) that silently suppresses files older than 7 days. This prevents false positives from snapshot resets. The filter is in `check_adel_files.sh` — if you modify the script, preserve this filter.
- **Empty subfolders**: Several subfolders (13-Weekly Report, 14-IR, 15-SNA, 17-SOR) are consistently empty in Adel's OneDrive. Don't flag them as missing — they're expected to be empty.
- **NCRs in Letters**: NCR documents may appear as attachments in the Letters folder (e.g., `01- Letters/IN/CG/01-/مرفقات الخطاب/NCR-CG-001.pdf`) rather than in a dedicated 12-NCR folder.
- **CG Reply in Approval subfolders**: Many TQ folders have an `Approval/` subfolder containing CG response PDFs. When this appears, update the TQ status from "Open" to "CG response received".
- **DDD packages span multiple subfolders**: A single 1G-xxxx package may have a main folder (PDF+XLSX) and an `Approval/` subfolder (CG-reviewed PDFs + CRS xlsx + BS rar). Both are part of the same submittal — don't double-count.
- **Script output truncation**: The script output can exceed 600K chars. Use `ls -ltR` on specific subfolders to get focused views rather than relying on the full script output.
