# XER/P6 Schedule Analysis — Programmatic Critical Path & Root Cause

Method for extracting schedule data from Primavera P6 XER/XML exports using Python, identifying the critical path, and quantifying why a phase overruns its duration target (e.g. "why does design exceed 3 months?").

## When to Use

- User sends an `.xer` or `.xml` P6 export and asks "why is this phase too long?" or "what's on the critical path?"
- Need to quantify approval-cycle overhead, calendar effects, or cross-discipline sequential delays
- Schedule is too large to read visually and relationships/computation matter

## XER File Parsing

The XER format is tab-separated with section headers. Each section has:

```
%T  TABLE_NAME
%F  field1\tfield2\t...
%R  value1\tvalue2\t...
```

### Parser (Python)

```python
with open("schedule.xer", 'r', encoding='utf-8', errors='replace') as f:
    content = f.read()

lines = content.replace('\r\n', '\n').replace('\r', '\n').split('\n')

tables = {}
current_table = None
for line in lines:
    if not line.strip(): continue
    if line.startswith('%T'):
        current_table = line[3:].strip()
        tables[current_table] = {'fields': [], 'rows': []}
    elif line.startswith('%F') and current_table:
        tables[current_table]['fields'] = line[3:].strip().split('\t')
    elif line.startswith('%R') and current_table:
        tables[current_table]['rows'].append(line[3:].strip().split('\t'))
```

After parsing, map fields to rows:

```python
tasks = {}
if 'TASK' in tables:
    tf = tables['TASK']['fields']
    for row in tables['TASK']['rows']:
        t = dict(zip(tf, row))
        tasks[t['task_id']] = t
```

### Key Table Names

| Section | Content | Field | Purpose |
|---------|---------|-------|---------|
| TASK | Activities | task_id, task_code, task_name, target_drtn_hr_cnt, target_start_date, target_end_date, total_float_hr_cnt, status_code, phys_complete_pct, wbs_id, clndr_id, task_type | Main activity data |
| TASKPRED | Relationships | task_id, pred_task_id, pred_type (FS/SS/FF/SF), lag_hr_cnt | Predecessor network |
| PROJWBS | WBS | wbs_id, parent_wbs_id, wbs_short_name, wbs_name, seq_num | WBS hierarchy |
| CALENDAR | Calendars | clndr_id, clndr_name, day_hr_cnt, week_hr_cnt, month_hr_cnt, year_hr_cnt | Which calendar each activity uses |
| PROJECT | Project | proj_id, plan_start_date, plan_end_date, clndr_id | Project-level metadata |

## Building the WBS Path

To understand the organizational context of each activity:

```python
wbs_map = {}
if 'PROJWBS' in tables:
    wf = tables['PROJWBS']['fields']
    for row in tables['PROJWBS']['rows']:
        w = dict(zip(wf, row))
        wbs_map[w['wbs_id']] = w

def get_wbs_path(wid):
    parts = []
    cur = wbs_map.get(wid)
    while cur:
        parts.insert(0, cur.get('wbs_name', '?'))
        pid = cur.get('parent_wbs_id')
        if pid and pid in wbs_map:
            cur = wbs_map[pid]
        else:
            break
    return ' / '.join(parts)
```

Note: the original XER field name is `parent_wbs_id`, not `parent_wbs_id` (it's usually `parent_wbs_id` from the field headers but check the actual field list from your file).

## Building Predecessor/Successor Maps

```python
pred_map = {}  # task_id -> [pred_task_id, ...]
succ_map = {}  # task_id -> [succ_task_id, ...]
if 'TASKPRED' in tables:
    rf = tables['TASKPRED']['fields']
    for row in tables['TASKPRED']['rows']:
        r = dict(zip(rf, row))
        tid = r['task_id']
        pid = r['pred_task_id']
        if tid not in pred_map: pred_map[tid] = []
        pred_map[tid].append(pid)
        if pid not in succ_map: succ_map[pid] = []
        succ_map[pid].append(tid)
```

## Identifying the Critical Path

Primavera computes Total Float (TF). Activities with TF = 0 are on the critical path:

```python
for tid, t in sorted(tasks.items(), key=lambda x: int(x[0])):
    tf = int(t.get('total_float_hr_cnt', '999')) / 8 if t.get('total_float_hr_cnt') else 999
    if tf == 0:
        # This activity is on the critical path
        code = t.get('task_code', '')
        name = t.get('task_name', '')
        od = int(t.get('target_drtn_hr_cnt', '0')) / 8
        sd = t.get('target_start_date', '')[:10]
        fd = t.get('target_end_date', '')[:10]
```

### Tracing the Full Chain Backward

To trace the critical path from end to start:

```python
def trace_back(tid, depth=0, seen=None, max_depth=30):
    if seen is None: seen = set()
    if tid in seen or depth > max_depth: return []
    seen.add(tid)
    t = tasks.get(tid, {})
    preds = pred_map.get(tid, [])
    result = [(tid, t.get('task_code','?'), int(t.get('target_drtn_hr_cnt','0'))/8,
               t.get('target_start_date','')[:10], t.get('target_end_date','')[:10],
               int(t.get('total_float_hr_cnt','999'))/8 if t.get('total_float_hr_cnt') else 999)]
    if preds:
        for p in sorted(preds):
            pt = tasks.get(p, {})
            pf = int(pt.get('total_float_hr_cnt', '999'))/8 if pt.get('total_float_hr_cnt') else 999
            if pf == 0 or depth < 3:  # Follow TF=0 (critical) or shallow
                result.extend(trace_back(p, depth+1, seen))
                break  # follow first CP predecessor
    return result

chain = trace_back(final_milestone_id)
```

## Calendar Analysis

Identify which calendar each activity uses, because calendars have different day counts:

| Calendar Type | Days/Week | Hours/Day | Real Example |
|---|---|---|---|
| 6-day construction | 6 (Sat-Thu) | 8 | `6 days calendar SFDA-13` |
| 5-day client/approval | 5 (Sun-Thu) | 8 | `5 -Days for Client Approval` |

**Critical insight**: A 5-day approval on the 5-day calendar spans 7 calendar days minimum. A 5-day task on the 6-day calendar spans 5-6 calendar days. The calendar ratio causes "calendar stretch" on the critical path.

Always check:
- Which calendar is the project calendar? (from `PROJECT.clndr_id`)
- Which calendar does each CP activity use? (from `TASK.clndr_id`)
- Do approval tasks use a different calendar than design tasks?

## Root-Cause Analysis Framework

After extracting the critical path, analyze WHY the phase exceeds the duration target:

### 1. Stage-Gate Overhead Counting

Count how many sequential stage gates exist on the CP. Each 50%→90%→100% transition adds:
- Preparation duration (e.g., 10-18 days per discipline)
- Approval duration (typically 5 working days)
- Calendar stretch if on 5-day approval calendar

### 2. Cross-Discipline Dependencies

Trace the discipline chain on the CP:
```
3D Shot → Architecture 50% → Approval → Electrical 50% → Approval → Mechanical 50% → ...
```

Separate disciplines running in PARALLEL (which buy nothing) from those running SEQUENTIALLY on the CP (which consume time). The sequential chain length determines the minimum duration.

### 3. Approval Cycle Quantification

Count all approval-type activities on the CP and sum their durations:

```python
approval_days = 0
for tid, t in tasks.items():
    if 'Approval' in t.get('task_name', ''):
        tf = int(t.get('total_float_hr_cnt', '999'))/8 if t.get('total_float_hr_cnt') else 999
        if tf == 0:
            od = int(t.get('target_drtn_hr_cnt', '0'))/8
            approval_days += od
```

A typical museum design schedule has 30-40 approval activities on the CP consuming 40+ calendar days.

### 4. Procurement Intrusion Check

Sometimes procurement chains (supplier approval → material submit → material approval) run on the design CP — this is a structural problem because procurement and design should be concurrent, not sequential. If a procurement activity blocks design handoff, the schedule is poorly structured.

### 5. Dual-Deliverable Tail

Check if the final stage requires two sequential cycles (e.g., "Final Design Package → Approval → Final BIM → Final Approval"). Each cycle adds ~15 calendar days.

### 6. Calendar Effects

If the 5-day approval calendar is used for activities on the CP, convert working days to calendar days to get the real timeline. A 5-day activity on a 5-day calendar spanning a weekend = 7+ calendar days.

## Typical Output Template

```
## Root Causes: Why [Phase] Exceeds [Target]

**Timeline:** [Start] → [End] = ~[N] months, exceeding [target] by ~[X] days ([Y]%)

### 1. [Root Cause 1: e.g. Three Sequential Design Stages]
  - Stage A: [dates, duration]
  - Stage B: [dates, duration]
  - Stage C: [dates, duration]

### 2. [Root Cause 2: e.g. Cross-Discipline Sequential Handoffs]
  [description of the discipline chain on CP]

### 3. [Root Cause 3: e.g. N approval cycles on CP]
  [count, total days, breakdown]

### 4. [Root Cause 4: e.g. Calendar effects]
  [which calendars, the stretch factor]

### Summary
The [target] constraint cannot be met because:
1. [reason with number of days]
2. [reason with number of days]
3. [reason with number of days]

### To compress to [target]:
- [Recommendation 1]
- [Recommendation 2]
- [Recommendation 3]
```

## Common Root Causes in Museum Design Schedules

| Root Cause | Typical CP Days | Example from Aseer Schedule |
|---|---|---|
| 3-stage waterfall (50%→90%→100% IFC) | 45-60 | 3 stages × 17-20 days each |
| Cross-discipline sequential handoffs | 15-25 per stage | Arch→Elec→Mech sequential chain |
| Approval cycle overhead on CP | 35-45 | 30-40 approval acts × 5 days each |
| Procurement intruding on design CP | 35-45 | Ductwork chain: 40 days mid-stream |
| BIM/Clash bottleneck at 90% | 25-35 | BIM 90% + Clash + Consultant (32d) |
| Dual final deliverable chain | 25-35 | IFC pkg → Approval → Final BIM → Approval |
| Calendar stretch (5-day approval cal) | 15-25 | 5 approval cycles stretched by weekend gaps |

## Verification

- [ ] Activities with TF=0 are correctly identified as the critical path
- [ ] WBS path resolves correctly (parent-child chain terminates at project root)
- [ ] Calendar effects accounted for (5-day vs 6-day calendar distinction)
- [ ] Approval activities confirmed as approval-type, not preparation-type
- [ ] Procurement/design overlap confirmed as a structural issue, not a calculation error
- [ ] The analysis distinguishes between "design effort" and "calendar elapsed time"
