# Factory Employee Violation Search — Worked Example

## Context

Session 2026-08-02: User asked to find historical violations for factory employees from emails and Odoo, to register them in the VIOLATIONS system.

## Source

Outlook SQLite at `~/Library/Group Containers/UBF8T346G9.Office/Outlook/Outlook 15 Profiles/Main Profile/Data/Outlook.sqlite`

## Discovery Query

```sql
SELECT m.Record_RecordID, m.Message_NormalizedSubject,
       substr(m.Message_Preview, 1, 1500) as preview,
       m.Message_SenderList, m.Message_TimeReceived
FROM Mail m
WHERE (m.Message_Preview LIKE '%مخالفة%' OR m.Message_Preview LIKE '%خصم%'
       OR m.Message_Preview LIKE '%إنذار%' OR m.Message_Preview LIKE '%جزاء%'
       OR m.Message_Preview LIKE '%تأديب%' OR m.Message_Preview LIKE '%رفض%')
  AND m.Message_SenderList LIKE '%raoof%'
  AND m.Message_Hidden = 0
ORDER BY m.Message_TimeReceived DESC;
```

## Violations Found (from Raoof Eldeeb emails)

| ID | Subject | Employee | Date | Type |
|----|---------|----------|------|------|
| 43056 | خصم اوفر تايم ولفت نظر | موسى, أكبر | 2025-04-10 | انصراف بدون إذن |
| 43320 | اسعار مخالفة نجار مجاهد رقم ١ و ٢ | عبد المجاهد محمد | 2025-07-07 | عدم طاعة الأوامر (مكرر) |
| 42205 | اشعار مخالفة | مد عارف | 2025 | مخالفة (تفاصيل ناقصة) |
| 43724 | اشعار مخالفة مساعد دهان هريدهاي | هريدهاي | 2025 | سوء سلوك — ألفاظ نابية |

## Odoo Employee Lookup

Used session-based Odoo API (password auth, expired API key fallback):

```python
session = requests.Session()
session.post(f'{url}/web/session/authenticate', json={
    'params': {'db': db, 'login': 'sultan@samayainvest.com', 'password': 'PASSWORD'}
})
# Then search hr.employee by name
```

Results:
- مد عارف → Odoo ID 1005, biotime 702, Labor, Samaya/Manufacturing
- عبد المجاهد محمد → Odoo ID 933, no biotime code, Carpenter
- هريدهاي → NOT FOUND in Odoo (no record)
- موسى → مد موسى شيخ (ID 1633, biotime 749)
- أكبر → اكبر حسين سايمون (ID 3301, biotime 483) — but this is Hoo dept, not Manufacturing

## Memo Files Created

- `VIOL-2026-004-انصراف-بدون-إذن-موسى-أكبر.md` — مد عارف (702), انصراف بدون إذن
- `VIOL-2026-005-عدم-طاعة-أوامر-عبد-المجاهد.md` — عبد المجاهد, عدم طاعة الأوامر (مكرر)
- `VIOL-2026-006-اشعار-مخالفة-عارف.md` — مد عارف (702), تفاصيل ناقصة
- `VIOL-2026-007-سوء-سلوك-هريدهاي.md` — هريدهاي, سوء سلوك

## INDEX.md Update

Added 4 rows to the violations table and updated footer: total 7 violations, last updated 2026-08-02.

## Pitfalls Encountered

1. **Gmail vs Outlook:** User corrected that Gmail IMAP should NOT be used — work emails are in Outlook only.
2. **Email preview truncation:** `Message_Preview` is ~500 chars. Some violation emails had the full story in the preview; others referenced an attachment for details.
3. **Employees not in Odoo:** هريدهاي (painter assistant) has no Odoo record. عبد المجاهد has no biotime code.
4. **API key expired:** Used password-based session auth instead of the expired API key.
