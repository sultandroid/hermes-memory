# Aseer Materials JSON — Key Casing Pitfall

The app uses `src/data/materials.json` as its **runtime data source** (loaded via `matMap`).
The individual schedule JSON files under `src/data/schedules/` are the **source-of-record workbooks**.

## The mismatch

materials.json has **different key casing** than the schedule JSON files:

| Key | In schedule JSON file | In materials.json |
|-----|----------------------|-------------------|
| Description | `Description` (Title Case) | `description` (lowercase) |
| Finish | `finish` (lowercase) | `finish` (lowercase) |
| Treatment/Finish | `Treatment/Finish` | ❌ field doesn't exist; use `finish` |
| Colour | `Colour` (Title Case) | `colour` (lowercase) |
| Supplier | `Supplier` (Title Case) | `supplier` (lowercase) |
| Substrate | `Susbtrate` (typo!) | `substrate` (lowercase, corrected) |
| Qty | `Qty` or `QTY` | `Qty` or `QTY` (inconsistent) |
| Unit | `Unit` | ✅ matches |

## How to verify

```python
import json
data = json.load(open('materials.json'))
for m in data:
    if m.get('schedule_key') == 'setwork_schedule':
        print(sorted(m.keys()))
        break
```

## Why it matters

When designing `SCHEDULE_FIELD_GROUPS` in `Gallery.tsx`, the `key` property must match the **materials.json key**, not the schedule file key. Using the schedule-file casing produces empty fields in the tooltip info card.

## Affected field groups (fixed 2026-06-18)

- `finishes_schedule`: use `finish`, `colour`, `supplier` (lowercase)
- `graphic_schedule`: use `substrate` (lowercase), `description` (lowercase)
- `wayfinding_schedule`: use `substrate` (lowercase), `description` (lowercase)
- `ff_e_schedule`: use `supplier` (lowercase)
- `setwork_schedule`: use `description` (lowercase)
- `asset_schedule`: use `description` (lowercase)
- `mockups_prototypes_schedule`: use `description` (lowercase)
- `mockups_prototypes_graphic_schedule`: use `description` (lowercase)
