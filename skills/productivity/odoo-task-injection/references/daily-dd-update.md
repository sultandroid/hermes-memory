# Daily DD Update — Outlook-to-Odoo Status Sync

> Cron-based workflow: check Outlook for recent project email activity, then update DD package task descriptions with a scan timestamp.

## Script Location

`~/.hermes/scripts/daily_dd_update.sh`

Runs as a `no_agent=True` cron job (no LLM cost) every day at 11:00.

## What It Does

1. Connects to **Samaya Odoo** (project 219, stage 36)
2. Loads all 18 DD packages
3. Queries **Outlook SQLite** for email count (total + last 24h)
4. Writes scan timestamp + email count into package **2946 (05 — Projects Plans)** description
5. Reports results

## Key Patterns

### Outlook SQLite Query
```python
import sqlite3, os
db = os.path.expanduser('~/Library/Group Containers/UBF8T346G9.Office/Outlook/Outlook 15 Profiles/Main Profile/Data/Outlook.sqlite')
conn = sqlite3.connect(db)
cur = conn.cursor()
cutoff = int(datetime.now().timestamp()) - 86400
cur.execute('''
SELECT COUNT(*) FROM Mail
WHERE Message_TimeReceived > ?
  AND (Message_NormalizedSubject LIKE '%ASE%'
    OR Message_NormalizedSubject LIKE '%Aseer%'
    OR Message_NormalizedSubject LIKE '%MOC-MUS%')
''', (cutoff,))
recent = cur.fetchone()[0]
```

### Writing Scan Timestamp
```python
scan_time = datetime.now().strftime('%Y-%m-%d %H:%M')
models.execute_kw(db, uid, pw, 'project.task', 'write', [[2946], {
    'description': f'<h3>05 Projects Plans</h3><p><b>Last daily scan:</b> {scan_time}</p><p><b>New emails today:</b> {recent}</p>'
}])
```

### Cron Setup
```
cronjob(action='create', name='Daily DD Update', schedule='0 11 * * *',
        script='daily_dd_update.sh', no_agent=True, deliver='origin')
```

### ⚠ Heredoc F-String Pitfall
Python in a bash heredoc (`<< 'PYEOF'`) with f-strings containing `.strftime()` + backslash escapes:
```
# ❌ SyntaxError
f'... {datetime.now().strftime(\"%Y-%m-%d\")} ...'
# ✅ Fix: assign variable first
scan_time = datetime.now().strftime('%Y-%m-%d %H:%M')
f'... {scan_time} ...'
```

## Existing Cron Jobs

| Name | Schedule | Purpose |
|------|----------|---------|
| Daily DD Update | `0 11 * * *` | Check Outlook → update Odoo DD tasks |
| Memory GitHub Sync | `every 2h` | Sync memory files to GitHub |

## Related Skills

- `odoo-task-injection` — Odoo task CRUD (this workflow writes scan info to task descriptions)
- `hermes-memory` — GitHub sync of memory files (separate cron, separate purpose)
