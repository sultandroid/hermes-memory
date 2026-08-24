# openpyxl insert_rows + Merged Cells — Pitfall (Aseer registers)

## The bug
`ws.insert_rows(pos, n)` shifts cell **values and styles** but does **NOT shift
merged-cell ranges that start at/below the insertion point**. After inserting rows
at position 19, header merges that lived on rows 19+ (e.g. `A19:O19` section headers,
`A57:O57` footer) stayed at their OLD row numbers, now overlapping your new data rows.
openpyxl then silently blanks the overlapping cells — the data you wrote is gone.

Symptoms: a new data row shows empty even though you wrote to it; section headers
sit on top of data rows.

## The Fix
Unmerge everything and re-merge at the corrected positions after inserting:

```python
ws.insert_rows(19, 3)          # insert
# old merges at row >= 19 must be shifted by +3
for m in list(ws.merged_cells.ranges):   # unmerge ALL (safe, then rebuild)
    ws.unmerge_cells(str(m))
# rebuild merges at their corrected rows (1:15 = A:O)
for m in ['A2:O2','A3:O3','A4:O4','A9:O9','A22:O22','A35:O35',
          'A39:O39','A42:O42','A43:O43','A60:O60']:
    ws.merge_cells(m)
```

## Order of operations that avoids the bug entirely
If you are **appending** rows (the common register case), `ws.max_row + 1` writes do
NOT disturb existing merges — prefer append over insert when you can. Only use
`insert_rows` when you truly must insert mid-table, then repair merges as above.

## Verify after every edit
- Reload the file, print the merged ranges, and print the new rows' cell values —
  confirm the data survived and the header rows land on the right rows.
