# Adel Darwish Folder Scan → Register Update Workflow

> Cron-driven pattern: scan a OneDrive project folder for new/changed files, map subfolders to repo registers, and update.

## Trigger

Cron job runs `bash /Users/mohamedessa/aseer-museum-pm/scripts/check_adel_files.sh` which compares current file inventory against a stored snapshot.

## Folder → Register Mapping

| Adel Subfolder | Repo Register | Notes |
|----------------|---------------|-------|
| `05- Request For Information-RFI/` | `01_Registers/rfi_register.md` | Look for new TQ/RFI refs in Approval/ subdirs |
| `12- NCR/` | `01_Registers/ncr_register.md` | New NCR PDFs |
| `08- Material Submittal MA/` | `01_Registers/material_submittal_register.md` | New MA refs |
| `07- Pre-Qualification Submittal/` | `01_Registers/prequalification_register.md` | New PQ refs |
| `20- DDD/` | `01_Registers/submittal_register.md` | DD Gateway packages with Approval subfolders |
| `10- CG Site Instruction SI/` | `01_Registers/si_register.md` | New SI PDFs |
| `06- Weekly Meeting MOM/` | `01_Registers/meeting_minutes_register.md` | New MOM PDFs |
| `09- Method Statement MWS/` | `01_Registers/method_statement_register.md` | New MS refs |
| `13- Weekly Report/` | `01_Registers/weekly_report_board.md` | New weekly reports |
| `17- SOR/` | `01_Registers/sor_register.md` | HSE observation reports |
| `01- Letters/` | `05_Comms/correspondence_register.md` | New LT refs (OUT/CG/ and IN/CG/) |
| `15- Start Nwe Activity (SNA)/` | No register yet | Flag for creation if recurring |

## Scan Types

### First-Time Scan (no snapshot exists)
- Script dumps ALL files as "new" — can be 4,000+ files
- Focus on **recent files** (Jul 2026+) for register updates
- Historical files (Dec 2025–Jun 2026) are baseline — snapshot them, don't add to registers unless they fill gaps
- Use `grep "Jul"` to filter recent files from the snapshot

### Incremental Scan (snapshot exists)
- Script reports only truly new/changed files
- Process each changed subfolder against its register
- OneDrive sync can cause false positives if files are still hydrating

## OneDrive Quirks

- `ls -la` shows folders exist, but `find`/`ls` on the path returns "No such file or directory" — this is a OneDrive sync state where the folder metadata is present but content hasn't hydrated
- Workaround: `cd` into the parent directory first, then use relative paths
- If `find` returns nothing but `ls` shows files, the files are cloud-only stubs not yet downloaded
- The `check_adel_files.sh` script uses `find` with `-exec stat` which triggers hydration

## Register Update Rules

1. **Append only** — never delete rows; mark superseded
2. **Frontmatter** — update `last_updated` and append source line
3. **Date filter** — only add files dated after the register's `last_updated`
4. **Approval subfolders** — CG response PDFs in `Approval/` subdirs indicate CG has reviewed; update status to CLOSED or add CG response date
5. **CRS xlsx files** in DDD Approval subfolders = CG Comment Response Sheets — evidence of CG review

## Verification

After updates, run:
```bash
python 09_Agent_Workspace/update_statistics.py --activity "Adel folder scan: updated registers"
```

Check that:
- Each register's `last_updated` reflects the scan date
- New entries have correct ref codes matching the document prefix
- No duplicate entries were added
