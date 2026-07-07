# _Unsorted_Emails Cleanup Pattern

## Location

`Bim Unit/_Unsorted_Emails/` at the BIM OneDrive root. This is a catch-all folder where files land before being sorted into project subfolders.

## Stale File Detection

Files in `_Unsorted_Emails/` that remain after a pipeline filing pass are either:
1. **Duplicates** — already present in a project BIM subfolder (should be deleted)
2. **Deferred** — OneDrive-locked files that couldn't be copied (keep, retry next run)
3. **Unfiled** — genuinely new files not yet sorted (should be moved)

### Identification Procedure

```bash
# Step 1: List all files in _Unsorted_Emails
ls -lt "$BIM_ROOT/_Unsorted_Emails/"

# Step 2: For each file, search entire BIM tree for same basename
# (ignoring _Unsorted_Emails itself and _Archive/)
for f in "$BIM_ROOT/_Unsorted_Emails/"*; do
    basename=$(basename "$f")
    matches=$(find "$BIM_ROOT" -path "$BIM_ROOT/_Unsorted_Emails" -prune -o \
              -path "$BIM_ROOT/_Archive" -prune -o \
              -name "$basename" -print 2>/dev/null | head -5)
    echo "$basename | $([ -n "$matches" ] && echo 'DUPLICATE' || echo 'NEW') | $([ -f "$f" ] && stat -f%z "$f" || echo '?') bytes"
done
```

### Evidence: Jun 8, 2026 Run

| File | Status | Copies in BIM | Action |
|------|--------|:-------------:|--------|
| `2026_0527_MVii_MADINAH PHYSICAL MODEL FINAL BOUNDARY.pdf` | DUPLICATE | 3 (El-Haramain Museum) | Deleted |
| `2026_0527_MVii_MADINAH MODEL (SCALE 1-200) QUESTIONS v2.pdf` | DUPLICATE | 3 (El-Haramain Museum) | Deleted |
| `2026_0519_MVii_MADINAH MODEL (SCALE 1-200) QUESTIONS.pdf` | DUPLICATE | 3 (El-Haramain Museum) | Deleted |
| `متجر الايس كوفي 2023.xls` | DEFERRED | 0 (OneDrive lock prevented copy to `El-Ghamama -(Qahwtna)/Email_Archive/`) | Remains in _Unsorted_Emails |

### Project Mapping for Unfiled Files

| Filename Pattern | Target Project | Target Folder |
|-----------------|----------------|---------------|
| `MVii_MADINAH*` | El-Haramain Museum | `Design Files/MVii_Models/` |
| `متجر الايس*` (Ice Coffee Shop) | El-Ghamama -(Qahwtna) | `Email_Archive/` |
| Other uncategorized | Manual review needed | — |

## OneDrive Lock Handling

Files that fail `cp` with `fcopyfile failed: Resource deadlock avoided` during copy from `_Unsorted_Emails` to a BIM project folder:

1. **Do NOT force delete** — the file stays in `_Unsorted_Emails` for the next pipeline run
2. **Log it** — note in pipeline report as `DEFERRED` with the target path
3. **Retry pattern** — each subsequent pipeline run will re-attempt the copy
4. **Detection** — `cp` succeeds silently (OneDrive handles the sync) when the lock has cleared

The `rm` of confirmed duplicates from `_Unsorted_Emails` works even when `cp` to BIM destination fails — OneDrive locks are specific to file pairs, not directory-wide.

## Cadence

Run this cleanup after every pipeline filing pass (cron every 2h). Most runs will find 0 stale files — the `_Unsorted_Emails` folder is a transient holding area, not a permanent archive.
