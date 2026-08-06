---
name: factory-violations
description: Register, search, and manage factory employee violations (مخالفات) in the samaya-workspace repo. Search Outlook SQLite for historical violations, cross-reference with Odoo employee data, and create formal Arabic memo files.
---

# Factory Violations System

Register disciplinary violations for Samaya Factory (Manufacturing dept) employees.

## Structure

```
VIOLATIONS/
├── INDEX.md              # Master register (table of all violations)
├── VIOL-YYYY-NNN-<desc>.md  # Individual violation memo (formal Arabic)
├── assets/               # Logos, stamps
├── exports/              # DOCX/PDF exports
└── scripts/              # add_violation.py, md_to_docx.py, etc.
```

## Workflow

### 1. Search for historical violations

Source: **Outlook SQLite** on Mac (`~/Library/Group Containers/.../Outlook.sqlite`)

```python
import sqlite3
db = '~/Library/Group Containers/UBF8T346G9.Office/Outlook/Outlook 15 Profiles/Main Profile/Data/Outlook.sqlite'
conn = sqlite3.connect(db)
cur = conn.cursor()

# Search by Arabic keywords + sender
cur.execute('''
SELECT Record_RecordID, Message_NormalizedSubject, Message_Preview, Message_SenderList, Message_TimeReceived
FROM Mail
WHERE (Message_Preview LIKE '%مخالف%' OR Message_Preview LIKE '%خصم%' OR Message_Preview LIKE '%إنذار%')
  AND (Message_SenderList LIKE '%raoof%' OR Message_SenderList LIKE '%sultan%')
  AND Message_Hidden = 0
ORDER BY Message_TimeReceived DESC
''')
```

**DO NOT use Gmail IMAP** — the user's factory email is on Outlook/Exchange.

### 2. Cross-reference with Odoo

Login via password-based session (API key may be expired):

```python
session = requests.Session()
session.post(f'{url}/web/session/authenticate', json={
    'jsonrpc': '2.0',
    'params': {'db': db, 'login': user, 'password': password}
})
```

Search employees by name to get biotime codes, job titles, departments:

```python
session.post(f'{url}/web/dataset/call_kw', json={
    'params': {
        'model': 'hr.employee', 'method': 'search_read',
        'args': [],
        'kwargs': {
            'domain': [['name', 'ilike', name]],
            'fields': ['id', 'name', 'job_title', 'biotime_code', 'department_id']
        }
    }
})
```

Filter to **Manufacturing department only** (`department_id.name ilike 'Manufacturing'`).

### 3. Create violation memo

Each violation gets:
- A unique code: `VIOL-YYYY-NNN` (auto-increment)
- A formal Arabic memo file in `VIOLATIONS/`
- An entry in `VIOLATIONS/INDEX.md`

Use the script: `python3 VIOLATIONS/scripts/add_violation.py --biotime <code> --date YYYY-MM-DD --violation "..." --severity low|medium|high|critical --manager "..." --action "..."`

Or create manually following the template in `VIOLATIONS/exports/Violation_Template_v1_Blank.docx`.

### 4. Update INDEX.md

Add row to the table and update the footer counters.

### 5. Commit and push

```bash
git add VIOLATIONS/
git commit -m "docs(violations): register VIOL-YYYY-NNN - <summary>"
git push origin master
```

## Severity Levels

| Code | Arabic | Description |
|------|--------|-------------|
| low | منخفضة | Verbal warning |
| medium | متوسطة | Written warning |
| high | عالية | Final warning / deduction |
| critical | حرجة | Suspension / termination |

## Violation Types (canonical)

| Code | Type | Default Severity |
|------|------|-----------------|
| ATTENDANCE_LATE | تأخر عن الحضور | low→medium |
| ATTENDANCE_ABSENT | غياب بدون إذن | medium→high |
| SAFETY_VIOLATION | مخالفة سلامة | high→critical |
| QUALITY_ISSUE | مشكلة جودة | medium→high |
| ATTITUDE | سوء سلوك | medium→high |
| INSUBORDINATION | عدم طاعة | high→critical |
| OVERTIME_REFUSAL | رفض العمل الإضافي | medium→high |
| THEFT | سرقة | critical |

## Data Sources

### 1. Outlook SQLite (historical emails)
Primary source for historical violations. Search by Arabic keywords:

```sql
-- Violation keywords
WHERE Message_Preview LIKE '%مخالف%' OR Message_Preview LIKE '%خصم%' OR Message_Preview LIKE '%إنذار%'

-- Employment decision keywords (tickets)
WHERE Message_NormalizedSubject LIKE '%تذكرة%' OR Message_Preview LIKE '%تذكرة%'
```

### 2. ERP-Samaya Helpdesk Tickets (تذاكر)
The ERP-Samaya system generates helpdesk tickets for HR actions. These appear in Outlook as emails from `Erp-Samaya` sender. They cover:
- **Hiring requests** (طلب توظيف) — new employee requisitions
- **Termination decisions** (الاستغناء عن الخدمات) — management decides to let someone go
- **Leave requests** (إجازة)
- **Flight tickets** (تذاكر سفر)

**Critical distinction**: A helpdesk ticket closure saying "سيتم اغلاق التذكرة" (ticket will be closed) is an **administrative action**, not a violation. Do NOT register ticket closures as violations.

### 3. Odoo Live Data
Login via password-based session (API key may be expired):

```python
session = requests.Session()
session.post(f'{url}/web/session/authenticate', json={
    'jsonrpc': '2.0',
    'params': {'db': db, 'login': user, 'password': password}
})
```

Search employees by name to get biotime codes, job titles, departments. Filter to **Manufacturing department only**.

## Distinguishing Violations from Employment Decisions

| Signal | It's a Violation | It's a Management Decision |
|--------|-----------------|---------------------------|
| Keywords | مخالفة, خصم, إنذار, مشاجرة, تكاسل, سوء سلوك | تذكرة, طلب توظيف, استغناء, إغلاق |
| Sender | Raoof (رؤوف) directly | Erp-Samaya (system) |
| Action | Penalty against employee | HR process (hire/fire/leave) |
| User says | "سجل مخالفة" | "مديره قرر الاستغناء" |

**Rule**: When the user says "مديره قرر الاستغناء عن خدماته" (manager decided to terminate), do NOT create a violation memo. This is an HR/employment decision, not a disciplinary action.

## Org Chart (Samaya Factory)

| Role | Person |
|------|--------|
| **مدير المصنع (Factory Manager)** | محمد سلطان عباس عيسى |
| **مدير الإنتاج (Production Manager)** | رؤوف محمد رضا الديب |

**⚠️ Warith Sultan has NO relation to the factory** — he is Aseer Museum project director only.

## Arabic Communication Style

When the user writes in Arabic:
- **Keep responses simple and direct** — avoid complex technical explanations
- If the user says "بسط اللغه مش فاهم" (simplify, I don't understand), strip all technical detail and give the plain answer
- Use short bullet points or a single sentence, not paragraphs
- Match the user's language: Arabic question → Arabic answer, English → English

## Pitfalls

- **API key may be expired** — use password-based session auth instead
- **Gmail IMAP does NOT work** for factory email search — use Outlook SQLite
- **Only factory employees** (Manufacturing dept) — skip other departments
- **Arabic keywords** in search must be encoded properly for SQLite
- **Rebase before push** — remote may have diverged (force-push history cleanup)
- **Conflict resolution** on INDEX.md is common — resolve manually
- **Don't confuse tickets with violations** — a helpdesk ticket closure is not a disciplinary record
- **Don't register management decisions** (termination, hiring) as violations — they belong in HR records, not the violations register
