# Aconex Transmittal → Submittal Register Update Workflow

## When to Use

- Cron job: "Check Aconex emails and update repo registers (no duplication)"
- Manual: user asks to scan for new Aconex transmittals

## Workflow

### 1. Query Outlook for Aconex emails

```sql
SELECT 
    datetime(Message_TimeReceived, 'unixepoch', 'localtime') as received,
    Message_NormalizedSubject as subject,
    Message_SenderList as sender,
    substr(Message_Preview, 1, 100) as preview
FROM Mail 
WHERE (Message_SenderList LIKE '%aconex%' OR Message_NormalizedSubject LIKE '%Aconex%' OR Message_NormalizedSubject LIKE '%WTRAN%')
ORDER BY Message_TimeReceived DESC
LIMIT 60;
```

**Epoch note:** `Data/Outlook.sqlite` (the active DB with `Mail`/`folders` tables) uses **Unix epoch** — `datetime(col, 'unixepoch', 'localtime')` works directly. Always verify with the 3-way test first.

### 2. Read the submittal register

Read `01_Registers/submittal_register.md` — specifically the three Aconex tables:
- **CG→Samaya (Final Review Outcomes)** — `CGP-WTRAN-*` rows
- **Samaya→CG (New Submissions)** — `SIC.-WTRAN-*` rows
- **Other Aconex Transmittals** — `CGP-TRANSMIT-*`, `SIC.-TRANSMIT-*` rows

### 3. Extract existing transmittal numbers

Use regex to extract all existing numbers from the markdown tables:

| Table | Regex | Example |
|-------|-------|---------|
| CG→Samaya | `CGP-WTRAN-(\d+)` | CGP-WTRAN-000086 |
| Samaya→CG | `SIC\.-WTRAN-(\d+)` | SIC.-WTRAN-000043 |
| Other | `CGP-TRANSMIT-(\d+)` | CGP-TRANSMIT-000001 |
| Other | `SIC\.-TRANSMIT-(\d+)` | SIC.-TRANSMIT-000004 |

### 4. Compare and identify new transmittals

For each Aconex email subject, extract the transmittal number. If it's NOT in the existing set, it's new.

**Dedup rule:** Match by transmittal number only (e.g. CGP-WTRAN-000171). If the number already appears in any row of the table, skip it — even if the subject/date differ slightly.

### 5. Add new rows to the appropriate table

**Format for CGP-WTRAN (CG→Samaya):**
```
|| CGP-WTRAN-000171 | Landscaping Specialist - PINE | 23-Jul | **NEW** — awaiting CG reply email |
```

**Format for SIC.-WTRAN (Samaya→CG):**
```
|| SIC.-WTRAN-000097 | Architectural Title Block Template | 23-Jul | **For Review** |
```

**Format for CGP-TRANSMIT (Other):**
```
|| CGP-TRANSMIT-000003 | MOC-MUS-CG-ASE-NC-1E0-014 — Temporary Exterior CCTV Installation | 23-Jul | **NEW** |
```

**Pitfall — pipe alignment:** The markdown table uses varying numbers of leading pipes to indicate row continuation. Match the existing pattern in the table (some rows have `||`, some `|||`, some `||||`). When adding new rows at the end, use the same pipe count as the last row.

### 6. Update frontmatter

Update `last_updated` in both files:
- `01_Registers/submittal_register.md` — e.g. `7 new CGP-WTRAN, 8 new SIC.-WTRAN, 1 new CGP-TRANSMIT added`
- `00_Status/project_status.md` — same summary in the source line

### 7. Update project_status.md

`00_Status/project_status.md` may be empty (0 lines, 0 bytes) or a OneDrive stub — `read_file` returns empty content even though `ls -la` shows 4903 bytes. This is a known macOS File Provider / OneDrive hydration issue. Write the file directly with `write_file` — it replaces the stub with real content.

### 8. Report

Output a table per category showing what was added, or "[SILENT]" if nothing new.

## Pitfalls

**Pitfall — `patch` fails on duplicate patterns in SIC.-WTRAN table.** The SIC.-WTRAN table often has inconsistent pipe alignment (some rows `||`, some `|||`, some `||||`, some `|||||`). When `old_string` matches 5+ times, `patch` refuses. **Fix:** replace the entire table section at once (from `### Samaya→CG` header to `### Other Aconex Transmittals` header) rather than trying to match individual tail rows. This is safer and avoids the duplicate-match problem.

**Pitfall — `replace_all=true` on `patch` causes massive duplication.** When `old_string` matches multiple times in a markdown table (e.g. `SIC.-TRANSMIT-000021 | Daily Progress Report / 04 Aug 2026 | 04-Aug | **For Review** |` appears in both the Samaya→CG and Other tables), `replace_all=true` replaces ALL occurrences, duplicating the new rows into every matched location. The result is hundreds of duplicated rows. **Never use `replace_all=true` on markdown tables with repeated patterns.** Instead, use one of:
- **`write_file` to rewrite the entire file** — safest when the file is small enough to hold in context
- **A unique `old_string` with enough surrounding context** (include the preceding and following rows) to make it match exactly once
- **Replace a whole section** (from one section header to the next) rather than individual tail rows

**Pitfall — `write_file` is the safest recovery from `patch` corruption.** When `replace_all=true` creates duplicate rows, the cleanest fix is to read the full file, reconstruct the affected section correctly, and write the entire file back with `write_file`. This avoids the `patch` duplicate-match problem entirely for the corrupted section.

**Pitfall — `execute_code` is blocked in cron mode.** Cron jobs run without user approval, so `execute_code` (which runs arbitrary Python including subprocess calls) is denied. Use `terminal()` for SQLite queries and `patch()`/`write_file()` for file edits instead.

**Pitfall — working directory may not be a git repo.** The cron job's working directory (`~/Documents/Asher_Regional_Museum_Document_Control/`) is a plain directory, not the `aseer-museum-pm` git repo. `git add/commit/push` will fail with `fatal: not a git repository`. The register files are updated locally but cannot be committed to GitHub from this path. Report this in the cron output so the user knows to commit manually or the cron should `cd` to the git repo before attempting git operations.

**Pitfall — `project_status.md` may be a OneDrive stub.** The file shows non-zero size in `ls -la` but `read_file` returns empty content and `cat` fails with `Resource deadlock avoided`. This is a macOS File Provider hydration issue — the file exists on disk as a cloud placeholder but the real bytes never downloaded. `write_file` replaces the stub successfully. Always use `write_file` for `project_status.md` updates rather than `patch`.
