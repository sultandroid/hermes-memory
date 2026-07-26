# PQ Batch Extraction — OneDrive Filing Pattern

> Reference for `outlook-email`. Covers the end-to-end workflow of extracting prequalification (PQ) emails from Outlook and filing them to the numbered PQ folder structure on OneDrive.

## When to use

The user asks to "check mails for prequalification" or "extract PQ attachments" — typically when a batch of supplier/contractor prequalification documents arrives via email and needs to be filed in the project's `07- Pre-Qualification Submittal/` folder hierarchy.

## Phase 1 — Discovery (SQLite)

Search for prequalification emails. The PQ ref pattern is `PQ-####` and subjects typically contain "prequalification", "Prequalification", or "PQ-":

```sql
SELECT m.Record_RecordID as id,
       datetime(m.Message_TimeReceived, 'unixepoch', 'localtime') as received,
       f.Folder_Name as folder,
       m.Message_SenderList as sender,
       m.Message_NormalizedSubject as subject,
       m.Message_HasAttachment as att
FROM Mail m
JOIN folders f ON m.Record_FolderID = f.Record_RecordID
WHERE (m.Message_NormalizedSubject LIKE '%prequalification%'
   OR m.Message_NormalizedSubject LIKE '%PQ-%'
   OR m.Message_NormalizedSubject LIKE '%prequ%')
  AND date(m.Message_TimeReceived, 'unixepoch') >= date('now', '-30 days', 'localtime')
ORDER BY m.Message_TimeReceived DESC;
```

## Phase 2 — Determine CG code from email preview

CG response emails contain the code (A/B/C/D) in the `Message_Preview` column. Query previews to determine the status without extracting:

```sql
SELECT substr(m.Message_Preview, 1, 400) as preview
FROM Mail m
WHERE m.Record_RecordID IN (<id1>, <id2>, ...);
```

Look for patterns like `"C - Revise and Resubmit"`, `"B - Approved with Comments"`, `"A - Approved"` in the preview text. The classification header often contains the PQ ref like `"Classification-ASE-External-PQ-LSA-0126"` where `0126` is the PQ number.

CG responses typically come from `Hossam Mabrouk` (hossam@cg.com.sa) or forwarded by `Hesham Abdelhameed`.

## Phase 3 — Extract attachments (AppleScript)

Use the Python generator pattern (see `outlook-email/SKILL.md` § "PREFERRED: Python generator script") to create .applescript files for each email ID. Filter out image attachments:

```applescript
if content type of a does not start with "image/" then
```

## Phase 4 — File to one of two destinations

| Destination | When | Action |
|---|---|---|
| **OneDrive `07- Pre-Qualification Submittal/`** | Has a numbered PQ folder (e.g. `122- MOC-MUS-ASE-1L0-PQ-0122/`) | Copy file to `/<PQ-folder>/Approval/` (CG responses) or root of folder (submission docs) |
| **Repo `01_Registers/prequalification_register.md`** | PQ ref exists or is being created | Update register rows with CG codes, new entries |
| **Repo `@ Draft/` folder** | No PQ ref assigned yet (new vendor PQ) | File to `@ Draft/` subfolder pending PQ ref assignment |

## Phase 5 — Critical: OneDrive write restriction

**macOS File Provider extension blocks ALL terminal/Python/Finder writes** to OneDrive volumes. This includes `cp`, `mv`, `mkdir`, `touch`, Python `open('wb')`, `shutil.copy2()`, and even `osascript -e 'tell application Finder to duplicate'`. All fail with:

```
Operation not permitted
```

This is distinct from the EDEADLK read-side issue (documented in `references/onedrive-edeadlk.md`). The write block applies even when the destination directory already exists and the user has rwx permissions.

**Workaround:** Stage organized files to `/tmp/` with the correct subfolder structure, plus a `_FILE_MAPPING.csv` document. The user then drags the folders from `/tmp/` into OneDrive via Finder.

```bash
# Example: stage to /tmp/ with organized structure
/tmp/filed_pq/PQ_Documents/
  PQ-0123_ACOUSTIEG/
    48822_PQ-0123_submission.pdf
    48037_ACOUSTIEG_Certificates.pdf
    Approval/
      48780_CG_Response_PQ-0123.pdf
  PQ-0127_TLC/
    Approval/
      49074_CG_Response_PQ-0127.pdf
  ...
  _FILE_MAPPING.csv      # tracks original email, PQ ref, destination
```

## Phase 6 — Update registers

Two registers need updating:

1. **`prequalification_register.md`** — Full PQ register (110+ entries). Add new rows for new PQs; update CG codes and notes for existing ones.
2. **`prequalification_log.md`** — Specialist-focused log tracking state (OPEN→SUBMITTED→CG-CODE→MoC-APPROVED). Update state, code, and notes per specialist.

Update roll-up metrics:
| Metric | How to compute |
|--------|---------------|
| PQs MoC-approved | Count rows with Code A/B + MoC Approved |
| PQs submitted, awaiting CG code | Count with Code U/— |
| PQs with CG code | Count with A/B/C/D |
| PQ approval rate | Code A+B count / total with codes |

## Phase 7 — Git commit

The repo root is `~/aseer-museum-pm/`. Branch `main`. Push may require `--force` if the post-commit hook (which auto-regenerates register web apps) causes a divergent index.html. The post-commit hook at `.git/hooks/post-commit` runs `update-all-registers.sh`.

```bash
cd ~/aseer-museum-pm
git add 01_Registers/prequalification_register.md \
        01_Registers/pq_attachment_mapping.md \
        Technical_Office/Specialist_Management/prequalification_log.md
git commit -m "PQ scan YYYY-MM-DD: N files extracted, CG codes updated"
git fetch origin
git rebase origin/main   # may need --autostash if post-commit modified risks.json
git push origin main     # use --force if rebase fails on auto-generated files
```

## Example mapping CSV format

```csv
EmailID_File,PQ_Ref,Destination_Folder,Notes
48780_CG_Response.pdf,PQ-0123,123- MOC-MUS-ASE-1A0-PQ-0123/Approval/,CG response - ACOUSTIEG Code C
49034_CG_Response.pdf,PQ-0126,126- MOC-MUS-ASE-1L0-PQ-0126/Approval/,CG response - PINE Code C
48861_TransOrient.pdf,PQ-0128,128- MOC-MUS-ASE-1A0-PQ-0128/,TransOrient submission
48531_Lab_Approval.pdf,PQ-0120,120- MOC-MUS-ASE-1C0-PQ-0120/Approval/,RAN Lab Code B
```

## See also

- `outlook-email/SKILL.md` — AppleScript extraction generator, SQLite queries
- `outlook-email/references/onedrive-edeadlk.md` — read-side EDEADLK on OneDrive
- `bulk-file-organization/references/onedrive-fileprovider-write-block.md` — write-side Operation not permitted
