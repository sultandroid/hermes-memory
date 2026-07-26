# Outlook SQLite Data Discovery — Query Patterns

When OneDrive files are deadlocked ("Resource deadlock avoided"), use the Outlook SQLite database to read email previews and extract CG response codes, document references, and project correspondence.

## Database Location

```
/Users/mohamedessa/Library/Group Containers/UBF8T346G9.Office/Outlook/Outlook 15 Profiles/Main Profile/Data/Outlook.sqlite
```

## Key Tables

| Table | Content |
|-------|---------|
| `Mail` | Email headers + preview (no full body) |
| `Folders` | Outlook folder names |
| `Files` | Attachments (virtual table) |
| `Threads` | Email threads |
| `Conversations` | Conversation grouping |

## Mail Table Key Columns

| Column | Type | Content |
|--------|------|---------|
| `Message_NormalizedSubject` | TEXT | Email subject line |
| `Message_SenderAddressList` | TEXT | Sender email (e.g. `hmabrouk@cg.com.sa`) |
| `Message_ToRecipientAddressList` | TEXT | To recipients |
| `Message_CCRecipientAddressList` | TEXT | CC recipients |
| `Message_Preview` | TEXT | First ~250 chars of email body |
| `Message_TimeReceived` | INTEGER | Unix timestamp |
| `Message_HasAttachment` | BOOLEAN | 1 if attachment present |
| `Record_FolderID` | INTEGER | FK to Folders table |

## Common Query Patterns

### Find CG responses for a specific document

```sql
SELECT datetime(m.Message_TimeReceived, 'unixepoch') as dt,
       m.Message_NormalizedSubject as subject,
       m.Message_SenderAddressList as sender,
       substr(m.Message_Preview, 1, 200) as preview
FROM Mail m
WHERE m.Message_NormalizedSubject LIKE '%ZD-0088%'
  AND m.Message_SenderAddressList LIKE '%@cg.com.sa%'
ORDER BY m.Message_TimeReceived DESC;
```

### Extract CG response code from preview

CG responses typically contain "B - Approved with Comments" or "C - Revise and Resubmit" in the first 200 chars of `Message_Preview`:

```sql
SELECT datetime(m.Message_TimeReceived, 'unixepoch') as dt,
       m.Message_NormalizedSubject,
       m.Message_SenderAddressList,
       CASE WHEN m.Message_Preview LIKE '%B -%' THEN 'Code B'
            WHEN m.Message_Preview LIKE '%C -%' THEN 'Code C'
            WHEN m.Message_Preview LIKE '%A -%' THEN 'Code A'
            WHEN m.Message_Preview LIKE '%D -%' THEN 'Code D'
            ELSE 'Unknown'
       END as code
FROM Mail m
WHERE m.Message_NormalizedSubject LIKE '%ZD-0088%'
  AND m.Message_SenderAddressList LIKE '%@cg.com.sa%'
ORDER BY m.Message_TimeReceived DESC;
```

### Find all emails from a company/person

```sql
SELECT datetime(m.Message_TimeReceived, 'unixepoch') as dt,
       m.Message_NormalizedSubject,
       substr(m.Message_Preview, 1, 150) as preview
FROM Mail m
WHERE m.Message_SenderAddressList LIKE '%@adeng.com.sa%'
ORDER BY m.Message_TimeReceived DESC;
```

### Find all emails about a discipline (e.g., 1E0 = Electrical)

```sql
SELECT datetime(m.Message_TimeReceived, 'unixepoch') as dt,
       m.Message_NormalizedSubject,
       m.Message_SenderAddressList as sender,
       substr(m.Message_Preview, 1, 100) as preview
FROM Mail m
WHERE m.Message_NormalizedSubject LIKE '%1E0-ZD%'
ORDER BY m.Message_TimeReceived DESC;
```

### Check if CG has responded to a batch of reports

```sql
SELECT datetime(m.Message_TimeReceived, 'unixepoch') as dt,
       m.Message_NormalizedSubject,
       CASE WHEN m.Message_Preview LIKE '%B -%' THEN 'Code B'
            WHEN m.Message_Preview LIKE '%C -%' THEN 'Code C'
            ELSE substr(m.Message_Preview, 1, 60)
       END as code
FROM Mail m
WHERE (m.Message_NormalizedSubject LIKE '%ZD-0089%'
    OR m.Message_NormalizedSubject LIKE '%ZD-0090%')
  AND m.Message_SenderAddressList LIKE '%@cg.com.sa%'
ORDER BY m.Message_TimeReceived DESC;
```

### Find Aconex transmittal notifications

```sql
SELECT datetime(m.Message_TimeReceived, 'unixepoch') as dt,
       m.Message_NormalizedSubject,
       m.Message_SenderAddressList
FROM Mail m
WHERE m.Message_SenderAddressList LIKE '%@aconex.com%'
ORDER BY m.Message_TimeReceived DESC;
```

## Limitations

- **No full email body** — only `Message_Preview` (~250 chars). For full text use OneDrive .md files (when hydrated).
- **Preview may be truncated mid-word** — the CG code may not be visible if the preview cuts off before "B - Approved". Search for both `B -` and `B-A` patterns.
- **Recall/recall corrections** — CG may send a "recall the message" followed by a corrected response. Check for consecutive messages with the same subject.
- **Attachments** — `Files` table is a virtual module (`FilesVTabModule`) that may not load in all sqlite3 contexts. For attachment names, check online-only OneDrive files instead.
- **No attachment content** — the database stores metadata only, not file contents.

## Performance Tips

- Use `LIKE '%keyword%'` sparingly — it's slow on 50K+ rows. Prefer `LIKE 'MOC-MUS-ASE-1E0-ZD-%'` (prefix) when possible.
- Add `LIMIT 10` to prevent massive result sets.
- Filter by `Message_TimeReceived > extract(epoch from '2026-07-01')` for recent emails.
- Use `.mode column` and `.headers on` for readable output.
