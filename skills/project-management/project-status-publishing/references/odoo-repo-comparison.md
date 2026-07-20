# Odoo-to-Repo Status Comparison — Manual Audit Workflow

## When to Use

- User asks "query Odoo project X and compare against the repo status"
- User wants to verify the repo's status file is accurate against live Odoo data
- User wants to know what's changed in Odoo since the last sync
- User wants a discrepancy report between Odoo and the repo

## Workflow

### 1. Query Odoo for All Project Tasks

```python
import ssl, xmlrpc.client
from datetime import datetime, date
from collections import Counter

ctx = ssl._create_unverified_context()
common = xmlrpc.client.ServerProxy(f'{ODOO_URL}/xmlrpc/2/common', context=ctx)
uid = common.authenticate(ODOO_DB, ODOO_USER, ODOO_API_KEY, {})
models = xmlrpc.client.ServerProxy(f'{ODOO_URL}/xmlrpc/2/object', context=ctx)

# Get stages
stages = models.execute_kw(ODOO_DB, uid, ODOO_API_KEY,
    'project.task.type', 'search_read',
    [[('project_ids', '=', PROJECT_ID)], ['id', 'name']])
stage_map = {s['id']: s['name'] for s in stages}

# Get all tasks
tasks = models.execute_kw(ODOO_DB, uid, ODOO_API_KEY,
    'project.task', 'search_read',
    [[('project_id', '=', PROJECT_ID)],
     ['id', 'name', 'stage_id', 'progress', 'date_deadline', 'date_assign',
      'state', 'parent_id', 'user_ids', 'description', 'create_date', 'write_date']])
```

### 2. Compute Key Metrics

```python
completed = sum(1 for t in tasks if t['progress'] >= 1.0)
in_progress = sum(1 for t in tasks if 0 < t['progress'] < 1.0)
not_started = sum(1 for t in tasks if t['progress'] == 0.0)

# Tasks per stage
stage_counts = Counter()
for t in tasks:
    sid = t['stage_id'] and t['stage_id'][0] if t['stage_id'] else None
    stage_counts[sid] += 1

# Past deadline
past_deadline = []
for t in tasks:
    if t['date_deadline']:
        dl_str = t['date_deadline'][:10]
        dl = datetime.strptime(dl_str, '%Y-%m-%d').date()
        if dl < date.today():
            past_deadline.append((t, dl))

# Tasks by state
state_counts = Counter(t['state'] for t in tasks)
```

### 3. Check Repo Status File

```python
# Read the repo's status file
status_file = REPO_DIR / '00_Status' / 'project_status.md'
content = status_file.read_text() if status_file.exists() else ''

# Extract frontmatter
import re
source_match = re.search(r'source: (.+)', content)
last_updated_match = re.search(r'last_updated: (.+)', content)

# Check sync state
sync_state = json.loads((REPO_DIR / '.sync_state.json').read_text()) if (REPO_DIR / '.sync_state.json').exists() else {}
```

### 4. Check PROJECT_MEMORY.md Hash

```python
import hashlib
pm_path = Path.home() / 'Library/CloudStorage/OneDrive-SAMAYAINVESTMENT/Samaya/Technical Office/Bim Unit/Aseer-Museum/_Project_Memory/PROJECT_MEMORY.md'
current_hash = hashlib.md5(pm_path.read_bytes()).hexdigest()
stored_hash = (REPO_DIR / '.last_project_memory_hash').read_text().strip() if (REPO_DIR / '.last_project_memory_hash').exists() else ''
hash_match = current_hash == stored_hash
```

### 5. Check Recent Odoo Modifications

```python
# Tasks modified after a cutoff date
modified = models.execute_kw(ODOO_DB, uid, ODOO_API_KEY,
    'project.task', 'search_read',
    [[('project_id', '=', PROJECT_ID), ('write_date', '>', cutoff_date)],
     ['id', 'name', 'write_date', 'progress', 'stage_id']],
    {'order': 'write_date desc'})

# Tasks created after cutoff
created = models.execute_kw(ODOO_DB, uid, ODOO_API_KEY,
    'project.task', 'search_read',
    [[('project_id', '=', PROJECT_ID), ('create_date', '>', cutoff_date)],
     ['id', 'name', 'create_date', 'stage_id']],
    {'order': 'create_date desc'})
```

### 6. Build Discrepancy Report

Compare these dimensions:

| Dimension | Odoo Source | Repo Source | What to Check |
|-----------|-------------|-------------|---------------|
| Total task count | `len(tasks)` | `Total Tasks` in snapshot | Match? |
| Completed count | `sum(progress >= 1.0)` | `Completed` in snapshot | Match? |
| In Progress count | `sum(0 < progress < 1.0)` | `In Progress` in snapshot | Match? |
| Not Started count | `sum(progress == 0.0)` | `Not Started` in snapshot | Match? |
| Source date | Current date | `source:` frontmatter | Stale? |
| Last sync timestamp | Latest `write_date` | `.sync_state.json` | Stale? |
| Individual deadlines | Odoo `date_deadline` | Deadline table in status | Mismatches? |
| Discipline progress | Computed from children | Discipline Health table | Stale? |
| Recent milestones | N/A (from PROJECT_MEMORY.md) | Recent Milestones section | Check hash match |
| Modified tasks | `write_date > last_sync` | N/A | New changes to sync |

### 7. Common Discrepancies Found

- **Deadline mismatches**: Odoo deadline differs from what the status file shows (e.g. Odoo says 2025-12-15, status says 2026-01-08)
- **Stale source date**: Status file frontmatter says `live sync YYYY-MM-DD` but the date is days old
- **Modified tasks with no progress change**: `write_date` bumped but progress unchanged — likely metadata edits (stage change, assignee change, etc.)
- **PROJECT_MEMORY.md hash mismatch**: New milestones in the memory file that haven't been pushed to Odoo
- **Discipline parent tasks at 0%**: Odoo stores progress on child tasks only; parent progress is computed. The status file's discipline health percentages are computed from child averages, not from Odoo's own progress field.

## Pitfalls

- **Odoo `date_deadline` includes time component** — always strip to `[:10]` before parsing: `dl_str = t['date_deadline'][:10]`
- **Odoo `progress` is 0.0–1.0 float** — multiply by 100 for percentage display. Tasks at exactly 0.0 are "not started", 1.0 is "completed"
- **Discipline parent tasks show 0% in Odoo** — their progress is computed from children. The `aseer-pm-status.py` script has a `parent_progress()` function that averages child progress
- **PROJECT_MEMORY.md may be locked by OneDrive** — use the `_Project_Memory/` subfolder path as fallback
- **No new tasks created after cutoff** is a valid finding — means no scope additions since last sync
- **`.sync_state.json` may be stale** — check `pm_mtime`, `repo_mtime`, and `odoo_write_time` separately
- **Status file deadlines may be truncated** — the status file shows only a subset of overdue tasks (e.g. 15 of 138). Note the total count in the report
