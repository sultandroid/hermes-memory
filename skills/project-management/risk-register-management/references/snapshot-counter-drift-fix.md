# Snapshot Counter Drift Fix

## When this applies

You have a build pipeline that produces versioned Excel snapshots with auto-incrementing snapshot numbers (e.g. `EXP-RISK-PRR-2026-001_RevC11_ACTIVE.xlsx`), and you deployed a file whose *content* says one snapshot number but whose *filename* says another.

## Root cause

**Counter key mismatch.** The build function used the human-readable register name (e.g. `"Master Risk Register (PRR)"`) as the key in `snapshot_counter.json`, while the file-rename step used the short code (`"PRR"`). This creates two key families with different counters. The xlsx content reads from the long-name key (e.g. count 6) but the filename reads from the short-code key (e.g. count 1).

## The fix

1. **Use ONLY short codes** as counter keys (`"PRR"`, `"DDR"`, `"HSE"`).
2. **Pass `snapshot_no` explicitly** to the build function. Don't let it auto-increment internally.
3. **Resolve the snapshot number BEFORE the build call**, then use the same value for:
   - The xlsx content (`"Snapshot No. 001"` in cell A3)
   - The output filename (`EXP-RISK-PRR-2026-001_RevC11_ACTIVE.xlsx`)
4. **Make the builder idempotent by default**: default mode = build without incrementing; `--bump` flag = explicit publish.

## Architecture

```
build_snapshots.py --bump
  ├── reads counter (e.g. PRR=0)
  ├── snapshot_no = counter + 1 (e.g. 1)
  ├── calls build_xlsx.build(snapshot_no=1)  ->  all sheets say "Snapshot No. 001"
  ├── renames output to EXP-RISK-PRR-2026-001_RevC11_ACTIVE.xlsx
  ├── saves counter (PRR=1)
  └── (next --bump produces 002, not 001)
```

```
build_snapshots.py                (no --bump)
  └── rebuilds same file with same number - no counter change
```

## Verification

```bash
python3 -c "
from openpyxl import load_workbook
wb = load_workbook('path/snapshot.xlsx', data_only=True)
d = wb['Dashboard']
snapshot_no = d['A3'].value.split('Snapshot No. ')[1].split()[0]
filename = 'EXP-RISK-PRR-2026-001_RevC11_ACTIVE.xlsx'
file_no = filename.split('-')[-3]
assert snapshot_no == file_no, f'DRIFT: content says {snapshot_no}, filename says {file_no}'
print('OK: content matches filename')
"
```
