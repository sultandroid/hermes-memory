# openpyxl insert_rows() does NOT shift merged cell ranges

## The bug
When you call `ws.insert_rows(n, k)` on a register that has merged header/section
rows (e.g. `A2:O2`, `A9:O9`, `A19:O19`), openpyxl shifts the **data cells** down
but leaves the **merged ranges in place**. The merges then point at the wrong rows
and can overlap the newly inserted rows, silently blanking them.

Observed 2026-08-23 on `Structural_Submittal_Register_Rev01.xlsx`:
- Inserted 3 rows at position 19 (before the "Gallery-Specific Structural Items"
  header which was merged `A19:O19`).
- The merge stayed at `A19:O19` and swallowed the first new data row (MDL-006),
  leaving it empty. Lower headers (BIM, Gate 2, Gate 3, IFC) also sat on the wrong
  rows because their merges didn't shift.

## The fix — repair merges manually after insert
After `insert_rows`, unmerge everything and re-merge at the corrected positions.
Merges at rows >= the insert point must shift down by `k`; merges above are unchanged.

```python
# after ws.insert_rows(19, 3)
for m in list(ws.merged_cells.ranges):
    ws.unmerge_cells(str(m))
# re-merge at corrected rows (cols A:O = 1:15)
for m in ['A2:O2','A3:O3','A4:O4','A9:O9','A22:O22','A35:O35','A39:O39',
          'A42:O42','A43:O43','A60:O60']:
    ws.merge_cells(m)
```

## Pitfalls
- **Verify after insert**: dump the merged ranges AND the affected rows before
  saving. A merge overlapping a data row silently blanks it — the row "disappears"
  from the register even though the file opens fine.
- **Copy styles from a data row, not a header**: use an existing populated data row
  as the format source (`copy(sc.font/border/fill/alignment)`), so new rows match
  the body, not the section headers.
- **Re-check the row you inserted at**: if a merge overlapped it, the values were
  written but are hidden/blanked — re-fill that specific row after fixing merges.
- **Never `mv`/`rm` OneDrive files**; write the register in place via openpyxl and
  save over the same path (OneDrive-safe).
