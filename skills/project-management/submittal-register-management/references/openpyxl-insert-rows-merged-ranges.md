# openpyxl insert_rows + merged ranges pitfall

## Problem
`ws.insert_rows(n, k)` shifts cell *values* but does NOT shift merged cell ranges.
In a register with merged section-header rows (e.g. `A9:O9`, `A19:O19`), inserting rows
leaves the merges at their original positions, so they overlap the new data rows and the
section headers land on the wrong rows.

## Fix pattern (every time you insert into a merged register)
1. `ws.insert_rows(n, k)` — insert the rows.
2. Unmerge ALL: `for m in list(ws.merged_cells.ranges): ws.unmerge_cells(str(m))`.
3. Re-merge at corrected positions: every merge whose `min_row >= n` shifts down by `k`.
   Rebuild with `ws.merge_cells('A{row}:O{row}')`.
4. Re-fill any data row clobbered by an overlapping merge (the merge may blank it) —
   copy style from a sibling data row via `copy(cell.font/border/fill/alignment)`.

## Verification
After the merge repair, dump the FULL column set of every inserted row (not just col A)
and confirm the section headers sit on the correct rows. A data row inserted directly
under a section header is the one most likely to be silently emptied.

## Related: `&` in inline heredoc
A `python3 << 'EOF'` heredoc whose content contains `&` (e.g. "Parts 01 & 02") is rejected
by the terminal tool as a backgrounding command. Write the script to a file with
`write_file` and run `python3 /tmp/script.py` instead of inlining it.
