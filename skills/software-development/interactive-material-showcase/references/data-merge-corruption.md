# Data Merge Corruption — Subagent Pitfall

## Symptom
After delegating a merge task (adding AV schedule, lighting schedule, etc.) to a subagent, ALL existing materials lose their `schedule_key`. Everything shows as "Other" schedule. Known codes like `04.04_SW_01` and `FI_FL_01` become "NOT FOUND" in materials.json. The tooltip card shows generic fields instead of schedule-specific groups.

## Root Cause
The subagent's merge script doesn't preserve existing `schedule_key` assignments. It groups items by `source` string instead of the existing `schedule_key`, or uses a different normalization that discards the keys (e.g., grouping all non-matching items under "other").

## Prevention Workflow

### Before Delegating
```python
import shutil
shutil.copy2('src/data/materials.json', '/tmp/materials-backup.json')
```

### After Subagent Completes — Verify
```python
import json
from collections import Counter
with open('src/data/materials.json') as f:
    mats = json.load(f)
sched_counts = Counter(m.get('schedule_key','?') for m in mats)
print('Schedule counts:', dict(sched_counts))
# Check known codes
for code in ['04.04_SW_01', 'FI_FL_01', 'FI_WA_03']:
    found = any(m.get('code') == code for m in mats)
    print(f'{code}: {"OK" if found else "MISSING"}')
```

Expected output for a healthy merge:
```
Schedule counts: { 'setwork_schedule': 225, 'finishes_schedule': 84, 'graphic_schedule': 245, ... }
04.04_SW_01: OK
FI_FL_01: OK
FI_WA_03: OK
```

If all items show `other: NNN`, the merge is corrupted.

### Recovery — Re-merge Manually
```python
# 1. Restore backup materials.json
with open('/tmp/materials-backup.json') as f:
    backup_mats = json.load(f)

# 2. Read new schedule files
with open('src/data/schedules/av_equipment_schedule.json') as f:
    av_items = json.load(f)

# 3. Add schedule_key + source to new items
for item in av_items:
    item['schedule_key'] = 'av_equipment_schedule'
    item['source'] = 'AV Equipment Schedule'

# 4. Append (don't merge/overwrite)
existing_codes = {m.get('code') for m in backup_mats if m.get('code')}
for item in av_items:
    if item.get('code') and item['code'] not in existing_codes:
        backup_mats.append(item)
        existing_codes.add(item['code'])

# 5. Write
with open('src/data/materials.json', 'w') as f:
    json.dump(backup_mats, f, indent=2)
```

## Why This Happens
Subagents receive the merge task with instructions like "merge all schedule JSONs into materials.json." They write a Python script that reads each file, extracts items, and combines them. But the script:
- May check `source` or `_source` fields instead of existing `schedule_key`
- May use a hardcoded `SCHEDULE_KEYS` mapping that doesn't match the data
- May reset all `schedule_key` values based on file name only
- May deduplicate by code but lose the assigned schedule_key from the original

**Always** append new items to the existing materials.json rather than rebuilding from scratch.
