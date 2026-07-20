---
name: odoo-bulk-audit
title: Odoo Bulk Audit & Update — Sync Tasks from Repo Registers
description: Compare Odoo project tasks against repo data sources (submittal registers, backlog files, Excel trackers) and apply batch corrections — stage moves, progress fixes, deadline extensions, CG response updates.
version: 1.0
author: Hermes Agent
---

# Odoo Bulk Audit & Update

## When to use

User says "update Odoo from repo", "sync tasks from registers", or "fix Odoo tasks" — any task comparing Odoo task data against Excel registers, backlog files, or submittal trackers and applying batch corrections.

## Pipeline

1. **Query Odoo** — dump all tasks for the project with key fields
2. **Read repo data** — submittal registers, backlog files, Excel trackers
3. **Compare** — identify gaps: wrong stage, wrong progress, past deadlines, missing CG response codes
4. **Batch-write** — group updates by type and apply in bulk
5. **Verify** — re-query and count remaining issues

## Common data quality issues

| Issue | Fix |
|-------|-----|
| Task in `1_done` state but `progress=0.0` | Set `progress: 1.0` |
| Task in `02_changes_requested` but CG response was Code B (Approved) | Set `state: 03_approved`, `progress: 1.0` |
| S00101 contract scope tasks in Initiation stage | Move to Procurement stage (39) |
| Past-deadline tasks with no progress | Extend deadline to contract end date or near-future date |
| Procurement submittal tasks (PR series) with stale deadlines | Extend in bulk |

## Deadline cleanup strategy

Group past-deadline tasks by type and apply consistent extensions:

| Task type | Extension target | Rationale |
|-----------|-----------------|----------|
| S00101 contract scope | Contract end date | Long-term contract items |
| PR procurement submittals | Near-term date (e.g. Jul 31) | Procurement push |
| Prequal specialist tasks | Jul 31 or Aug 15 | Depends on urgency |
| DD design tasks | Jul 31 | Active workstream |
| On-site work | Jul 31 | Site execution |
| Old abandoned items | Contract end date | Keep visible but not urgent |

## Stage migration rules

| Task pattern | Current stage | Correct stage |
|-------------|---------------|---------------|
| S00101 - [8880-8888-0164..0178] | Initiation (35) | Procurement (39) |
| Material submittal tasks (PR*) | Initiation (35) | Procurement (39) |
| Shop drawing / contractor submittals | DD (36) | Procurement (39) |

## Connection (SSL-safe for macOS)

```python
import xmlrpc.client, os, ssl
from datetime import date, datetime

ctx = ssl._create_unverified_context()
url = 'https://samayainv.odoo.com'
db = 'peerless-tech-samaya-18-0-18447146'
login = 'sultan@samayainvest.com'
with open(os.path.expanduser('~/.config/samaya/odoo.env')) as f:
    for line in f:
        if 'ODOO_API_KEY' in line and '=' in line: pw = line.split('=', 1)[1].strip()
transport = xmlrpc.client.SafeTransport(context=ctx)
common = xmlrpc.client.ServerProxy(url + '/xmlrpc/2/common', transport=transport)
uid = common.authenticate(db, login, pw, {})
models = xmlrpc.client.ServerProxy(url + '/xmlrpc/2/object', transport=transport)
```

## Full bulk update script pattern

```python
def read_task(tid):
    r = models.execute_kw(db, uid, pw, 'project.task', 'read',
        [[tid], ['name', 'stage_id', 'progress', 'state', 'date_deadline']])
    return r[0] if r else None

def write_task(tid, vals):
    models.execute_kw(db, uid, pw, 'project.task', 'write', [[tid], vals])
    r = read_task(tid)
    print(f"  -> Task {tid}: {r['name'][:60]} | progress={r['progress']} | state={r['state']} | stage={r['stage_id']}")
    return r

# Always verify after writes
all_tasks = models.execute_kw(db, uid, pw, 'project.task', 'search_read',
    [[('project_id', '=', PROJECT_ID)], ['id', 'name', 'progress', 'state', 'date_deadline']])
past = 0
for t in all_tasks:
    if t['date_deadline']:
        dl_str = t['date_deadline'][:10]
        dl = datetime.strptime(dl_str, '%Y-%m-%d').date()
        if dl < date.today() and t['state'] not in ('1_done', '03_approved', '1_canceled'):
            past += 1
print(f"Tasks still past deadline: {past}")
```

## Real example: Aseer Museum (project 219) — 2026-07-20

**Before:** 347 tasks, 138 past deadline, 233 at 0% progress, 51 Procurement tasks all at 0%.

**Updates applied:**
- 8 tasks: fixed progress=1.0 for done tasks stuck at 0%
- 1 task: LG-001 Lighting (ZD-0056 Code B) → marked Approved
- 15 tasks: S00101 contract scope moved from Initiation → Procurement
- 35 tasks: PR procurement deadlines extended (Jun 12 → Jul 31)
- 24 tasks: prequal specialist deadlines extended
- 15 tasks: DD design deadlines extended
- 3 tasks: on-site work deadlines extended
- 4 tasks: finishes procurement deadlines extended
- 26 tasks: remaining old-deadline tasks → Sep 7 (contract end) or Aug 15

**After:** 0 tasks past deadline.

## Pitfalls

- `date_deadline` may include time component — always slice `[:10]` before parsing
- `stage_id` is `[id, name]` tuple — compare with `t['stage_id'][0]`
- `progress` is 0.0–1.0 float, not percentage
- Always read current state before writing — don't assume
- Always verify after each batch — some writes may not persist
- Use `ssl._create_unverified_context()` for Samaya Odoo (self-signed cert)
- Set `SSL_CERT_FILE` env var when running from terminal: `SSL_CERT_FILE=$(python3 -c "import certifi; print(certifi.where())") python3 script.py`
