# Aseer Museum — Schedule Data Key Casing Reference

The app uses `src/data/materials.json` at runtime. Key casing in this file differs from the raw schedule JSON files in `src/data/schedules/`.

## Mapping: Raw Schedule File → materials.json

| Raw Schedule Key | materials.json Key | Notes |
|---|---|---|
| `Description` | `description` | Lowercase in runtime |
| `Supplier` | `supplier` | Lowercase |
| `Susbtrate` | `substrate` | Lowercase + typo fixed |
| `finish` | `finish` | Already lowercase |
| `colour` | `colour` | Already lowercase |
| `Treatment/Finish` | `finish` | Mapped to the 'finish' key |
| `Material ID` | `code` | Uses the unified `code` field |
| `Qty` | `Qty` | Same |
| `QTY` | `QTY` | FF&E uses uppercase |
| `Unit` | `Unit` | Same |
| `Exhibition Element Component` | `Exhibition Element Component` | Same |
| `Material Description` | `Material Description` | Same |
| `Exhibit Name` | `Exhibit Name` | Same |
| `Finishes` | `Finishes` | Same |
| `Drawing Code Reference` | `Drawing Code Reference` | Same |
| `Art Commission Title` | `Art Commission Title` | Same |

## Schedule-specific keys that work as-is

All schedule-specific keys (not `description`, `supplier`, `substrate`) retain their original casing from the schedule files. The normalization only affects the fields that overlap with the unified `materials.json` schema (`code`, `description`, `source`, `schedule_key`, etc.).

## Verification command

```bash
python3 -c "import json; d=json.load(open('src/data/materials.json')); \
  for m in d[:3]: print(m.get('schedule_key'), '→', list(m.keys())[:10])"
```
