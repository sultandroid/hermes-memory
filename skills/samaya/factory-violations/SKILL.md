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

### 2. Cross-reference with the repo's local employee database (PREFERRED — do NOT re-query Odoo every time)

User correction (2026-08-24): "مش كل مرة نرجع من جديد" — the employee master data already lives in the repo. **Source of truth for names + biotime codes = `samaya-workspace/OT_SYSTEM/data/odoo_employees_biotime.csv`** (columns: `odoo_id,name,biotime_code,job_title,department,email,manager`). Cross-check `OT_SYSTEM/EMPLOYEES.md` (canonical Arabic names by EID) and `OT_SYSTEM/employees/<EID>.md` per-employee records. `OT_SYSTEM/data/workshop_employees_final.csv` holds workshop/local name variants — the CSV `name` column is canonical. Only hit Odoo live (`hr.employee` via `~/.config/samaya/odoo.env`) when an employee isn't in the repo database.

**Official names ≠ workshop/street names.** Always use the exact Arabic name from the repo database in formal documents (complaints, memos). Known staff: محمد عبد الجليل عبد النبي عطية = Factory Supervisor (مشرف المصنع), biotime 683; ادريس عثمان احمد محمد (Welder, 253); عثمان سيد (Carpenter, 186); مد موسى شيخ (Labor, 749); سامساد على جولاه (Labor, 434). All under `Samaya / Manufacturing`, direct manager رؤوف محمد رضا الديب.

(Odoo session-based lookup below retained as the fallback when the repo DB lacks a record.)

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

### Find last violation by biotime code (Odoo helpdesk.ticket) — learned 2026-08-18

When the user asks "what's the last complaint against biotime 586" (ما اخر شكوي منه), the authoritative source is **`helpdesk.ticket`** in Odoo (the ERP-Samaya emails are the notifications; the ticket holds the detail + chatter). Workflow:

1. **Resolve biotime → employee name** via `hr.employee` (`biotime_code`), e.g. biotime 586 = محمد تميج الإسلام (Odoo ID 968, Carpentry).
2. **Find the ticket** — Raoof's violation email subject `#2761 مخالفة <name>` maps directly to `helpdesk.ticket.id = 2761`. Search by `name` (`[('name','ilike','2761')]`) or by description containing the employee name.
3. **Field-schema pitfalls** (`helpdesk.ticket` differs from project.task — these will throw `Invalid field` if guessed):
   - There is **NO `subject`** field — use `name` (the ticket number/title).
   - There is **NO `state`** — use `stage_id` (e.g. `[2, 'In Progress']`).
   - `description` holds the violation text; read it to extract the cause (e.g. "اعتراض علي تنفيذ اوامر مشرف الورشة" = insubordination) + repeat flag ("مش اول مرة").
4. **Pull the chatter** (`mail.message` where `model='helpdesk.ticket'`, `res_id=<id>`) for the escalation trail: Raoof's original complaint, the follow-up (`@Sultan Issa`), and who resolved/handed it to HR (e.g. Ahmed Alrabaei "وجه الموظف الى قسم الموارد البشرية"). If stage still `In Progress`, the ticket is not closed.
5. **Check the local `VIOLATIONS/` register** for a formal memo. A ticket may exist in Odoo with NO memo filed in `VIOLATIONS/` (the register only covers VIOL-001..012, so a biotime 586 violation may be missing a formal memo) — flag the gap and offer to file one.

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

## Attendance-Complaint Emails → Technician Identity Resolution (load 2026-08-24)

The user receives attendance/attendance-complaint emails (شكوى بعدم الالتزام بالدوام) listing **technicians by first-name + trade** (e.g. فني حداد/إدريس, فني نجار/عثمان, مساعد/سامساد). To produce the real names + biotime codes, resolve through the **repo employee DB first** (`OT_SYSTEM/data/odoo_employees_biotime.csv` — grep by name + job_title), falling back to Odoo `hr.employee` only if not found:

1. **Search by the trade too, not just the name.** Multiple employees share first names across departments. Match BOTH name fragment AND job_title. Known trade→job_title mapping: فني هناد→`Welder`, فني نجار→`Carpenter`, مساعد/فني→`Labor`. Verify the resolved person is in **`Samaya / Manufacturing`** department (the factory). Example: "إدريس" matched 4 employees (id 3720 منظم at Quran Museum, id 874 Welder at Manufacturing, id 2758 Labor at Eventech, id 3483 مرشد at Revelation gallery) — only the Manufacturing Welder (biotime 253) is the complainant.
2. **Senders may be registered under a different transliteration.** Searching Arabic display names for "عبد الجليل" can miss the sender. The complaint sender was **Mohammed Abdelgil / Muhammad Abdeljalil Abdelnabi Attia / `m.abdelglil@samayainvest.com`** — match by email address/domain OR by subject keywords (الالتزام، حضور، دوام) instead of relying on Arabic display-name match.
3. **Expected attachment layout**: complaint emails carry the movement/attendance evidence as the LARGEST image attachment (e.g. bus-ticket screenshot Riyadh→Makkah) plus 2 small Samaya-logo images (signature). Read the big image with vision; ignore the logos. The 255-char `Message_Preview` usually shows the technician list — enough to record names without full-body extraction.

**Field pitfall — `hr.employee` does NOT have `work_location` on Samaya Odoo.** Querying it raises `Invalid field 'work_location' on model 'hr.employee'`. Use fields: `name`, `job_title`, `biotime_code`, `department_id` only. The `biotime_code` IS the attendance/fingerprint ID the user asks for ("أرقام بصمة").

## Distinguishing Violations from Enforcement Decisions

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

- **`helpdesk.ticket` schema differs from `project.task`** — there is NO `subject` (use `name` = ticket number) and NO `state` (use `stage_id`). Guessing the wrong field raises `Invalid field ... on model 'helpdesk.ticket'`. A Raoof violation email subject `#2761 مخالفة <name>` maps directly to ticket id 2761.
- **Raoof's violation emails are the index, not the record** — the `Erp-Samaya` notification emails show only a one-line preview ("وجه الموظف الى قسم الموارد البشرية"). The full cause + chatter trail lives in the Odoo `helpdesk.ticket` (search by name, read `description` + `mail.message` chatter).
- **API key may be expired** — use password-based session auth instead
- **Gmail IMAP does NOT work** for factory email search — use Outlook SQLite
- **Only factory employees** (Manufacturing dept) — skip other departments
- **Arabic keywords** in search must be encoded properly for SQLite
- **Rebase before push** — remote may have diverged (force-push history cleanup)
- **Conflict resolution** on INDEX.md is common — resolve manually
- **Don't confuse tickets with violations** — a helpdesk ticket closure is not a disciplinary record
- **Don't register management decisions** (termination, hiring) as violations — they belong in HR records, not the violations register

## Running `add_violation.py` — script + credential + INDEX bugs (learned 2026-08-24)

Three separate traps fired when actually filing the 4 attendance memos:

1. **`add_violation.py` may be left with UNRESOLVED git merge-conflict markers** (`<<<<<<< HEAD` ... `>>>>>>> <commit>`) — the file is broken and exits on `import`. Fix BEFORE first run: resolve to the `from odoo_auth import ...` shim (NOT the inline-hardcoded `API_KEY = 'bfc7...'` block), then `grep -n "HEAD\|====\|<<<<\|>>>>" VIOLATIONS/scripts/add_violation.py` to confirm clean. (Resolving to the shim also removes a hardcoded API key — good hygiene.)
2. **The canonical credential may NOT be `.odoo_config` at workspace root** — it was absent this session. The working Samaya creds are at `~/.config/samaya/odoo.env` (`ODOO_URL`, `ODOO_DB`, `ODOO_USER`, `ODOO_API_KEY`). Before running any Odoo script: `set -a; source ~/.config/samaya/odoo.env; set +a`. If the script exits "ODOO_API_KEY not set", this is the cause.
3. **`add_violation.py`'s `update_index()` appends the new row to the END of INDEX.md** — under the `## System Memos` table at the bottom — NOT into the main `## جميع المخالفات` table. After each run, manually: (a) insert the row into the main table following the `| 000012 | VIOL-2026-012 | ...` pattern (format `| 0000NN | VIOL-2026-NNN | date | name (biotime) | violation | عالية | manager | action | مفتوحة |`), (b) delete the duplicate row the script left at the bottom, (c) bump the `*آخر تحديث:*` date and `*إجمالي المخالفات:*` count in the footer. Then commit + push (rebase first — remote may have diverged).\n\n4. **Concurrent-agent number collision — check the register BEFORE assigning codes, renumber with `git mv`.** Sibling agents (email-scan, other Hermes sessions) also append VIOL rows to the SAME `INDEX.md`. This session a sibling added VIOL-013-019 (other employees' OVERTIME_REFUSAL/insubordination) while my 4 attendance memos were staged as 013-016 → collision on 016. When a rebase/pull surfaces a conflict or you see codes you allocated now owned by others: **resolve to the remote (HEAD) version**, then renumber YOUR memos to free numbers above the remote max (mine 013-016 → 020-023). Rename the memo files with `git mv VIOL-2026-OLD-<desc>.md VIOL-2026-NEW-<desc>.md`, rewrite the internal code + `رقم المذكرة` occurrences in each file (Python str-replace `VIOL-2026-OLD`→`NEW`, `**000OLD**`→`**000NEW**`), then edit the single merged INDEX.md: append your rows after the remote's last row (formatted consistently) and recompute the footer count. Always `grep -nE \"VIOL-2026-0[1-9][0-9]\" INDEX.md` after merging to confirm no leftover collision markers or duplicated/truncated rows (a truncated row loses its trailing columns — rewrite the whole row).\n\n5. **Before filing, verify there are no PRIOR violations for the named employees.** When the user asks \"شوف المخالفات السابقة لهم\", `grep` INDEX.md + OT_SYSTEM employee files + ARCHIVE/legacy/hr/employees/<name>.md + TICKETS/ + DECISIONS/ for each biotime/name. If all clean (typical for long-serving workers), state it explicitly in the ticket/memo — it is the first violation and drives severity.\n\n## Complaint Email → Violation Memos + Linked Ticket (workflow 2026-08-24)\n\nAn attendance complaint (شكوى بعدم الالتزام بالدوام) typically lands as email → user asks to (a) draft the formal complaint, (b) check each employee's prior violations, (c) register the memos, and (d) create a TICKET for Odoo upload.\n\n1. **Resolve real names + biotime** from the repo DB first (see the identity-resolution section above).\n2. **Draft the formal complaint** with the OFFICIAL repo names (never the street/trade names from the email) and biotime codes; correct the sender's title (e.g. محمد عبد الجليل = مشرف المصنع / Factory Supervisor, not \"مشرف مشاريع\").\n3. **Check prior violations** (per pitfall above) — report clean records explicitly.\n4. **File the memos** via `add_violation.py`, fix the INDEX placement + footer, commit + push.\n5. **Create a TICKET to mirror the Odoo helpdesk upload**: `TICKETS/TKT-YYYY-NNN-<desc>.md` modeled on the newest existing `TICKETS/TKT-*.md` (fields: Ticket Code, النوع, التاريخ, الحالة, المُرسِل, الموظفون table, plus a `## سجل المخالفات المرتبط` table linking the VIOL codes/files). Add a row to `TICKETS/INDEX.md` (format `| TKT-YYYY-NNN | <OutlookID> | date | subject | النوع | الحالة |`). The ticket is what gets raised to Odoo `helpdesk.ticket`; the VIOL memos are the local disciplinary record. Next higher TKT number = `ls TICKETS/TKT-YYYY-*.md | sed -E 's/TKT-[0-9]+-([0-9]+).*/\\1/' | sort -n | tail -1` + 1.\n6. **Commit message dates + summary**: the user requires `YYYY-MM-DD` in repo commit messages and status reports.

**Ticket body MUST follow the Odoo helpdesk formal-memo style** (user rejected a narrative "وصف الموضوع" heading on 2026-08-24). Use a `## Description` section (matches the Odoo field) with the exact template from old tickets TKT-2026-013/035/056: open `السادة / إدارة الموارد البشرية المحترمين، تحية طيبة وبعد،،،`, state the fact + the employee table, then `برجاء التكرم باتخاذ اللازم بخصوص ... وفق اللوائح المعتمدة في المنشأة`, close `شاكرين تعاونكم، مع خالص التحية.`. Keep the employee table + prior-violations note as separate trailing sections below Description.

**Reference any PRIOR HR email on the same issue** (user: "شير لنفس الاميل فالتذكره"). Before finalizing, search Outlook **SENT ITEMS** (`f.Folder_Name IN ('Sent Items','Sent')`) for an earlier complaint about the same root cause — keywords بصمة/دوام/حضور/انصراف/استهتار/مشاريع مكة. Read the full body via AppleScript `plain text content of m`, and add a `## إيميل سابق للموارد البشرية (لم يُتخذ بشأنه إجراء)` section to the ticket with subject, date, recipients, Outlook ID, and the exact quoted text. This proves the problem is **systemic/recurring, not one-off**, and shows HR was already notified. Concrete example: Sultan's 2025-01-19 "إشعار بخصوص الحضور والانصراف بمشاريع مكة" (Outlook 19476, to alrabaei@ + osama@) explicitly asked for an electronic attendance (بصمة) system or a dedicated attendance officer for Makkah projects — never actioned — and the same absence problem recurred 2026-08-24. This recurrence evidence strengthens the case for escalation.",
