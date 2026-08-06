# Risk Review Workflow — "Next Risk" Pattern

## When to Use

The user says "next risk" or names a risk ID (e.g. "PRR-DES-07") during a risk register review session. This workflow emerged from Aseer Museum PRR management.

## Workflow

### 1. Identify the next risk

```python
# Load PRR JSON
with open('06_Risk_System/risks.json') as f: prr = json.load(f)

# Sort open risks by descending score
open_risks = [r for r in prr['risks'] if r.get('status') in ('Open','Watch')]
open_risks.sort(key=lambda r: -r['score'])

# Show top 5
for r in open_risks[:5]:
    print(f"{r['id']} | {r['title'][:70]} | {r['score']} {r['rating']} | {r['status']}")
```

### 2. Read the full risk

```python
for r in prr['risks']:
    if r['id'] == 'PRR-XXX-XX':
        print(json.dumps(r, indent=2))
```

### 3. Search Outlook for updates

Query the Outlook SQLite database for emails related to the risk's subject:

```sql
SELECT m.Record_RecordID, datetime(m.Message_TimeReceived, 'unixepoch', 'localtime'),
       m.Message_NormalizedSubject, substr(m.Message_Preview, 1, 300)
FROM Mail m
WHERE m.Message_TimeReceived >= strftime('%s', '2026-07-20')
  AND (m.Message_NormalizedSubject LIKE '%keyword1%'
       OR m.Message_NormalizedSubject LIKE '%keyword2%')
ORDER BY m.Message_TimeReceived DESC
LIMIT 10;
```

### 4. Update the risk based on findings

| Finding | Action |
|---------|--------|
| No new emails | Extend overdue dates, add review history entry |
| CG response found (Code B/C/D) | Update score, status, evidence, actions |
| Progress on an action | Mark action In Progress/Completed with evidence |
| Risk event passed | Downgrade score, change status to Watch |

### 5. Report to user

Table format: Field | Before | After

### Key Patterns from Aseer Museum

- **PRR-DES-07** (Structural DD Code C): Rev.02 got Code B → downgraded from Critical 16 to High 9 (Watch)
- **PRR-FLS-01** (Life Safety Code C): No CG response found → extended dates. Later found Namaa docs sent → A1 completed
- **PRR-SCH-01** (Completion not achieved): Recovery Plan rejected Code D → risk worsened, evidence added
- **PRR-PRC-10** (MEP installer not awarded): No sourcing emails found. MEP design still in Code C cycle → pushed dates

### Pitfalls

- Always search Outlook before updating — the user expects proactive email scanning
- Don't assume a risk is unchanged just because no email mentions its exact ID. Search by subject keywords (e.g. "MEP installer", "recovery plan", "Life Safety")
- When extending dates, explain why (e.g. "blocked by IFC-Mech approval")
- A1 (first action) is often the most progressed — check it first
- The user says "next risk" to move sequentially through the sorted list. Don't skip or re-sort mid-session
