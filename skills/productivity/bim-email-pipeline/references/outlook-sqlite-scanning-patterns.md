# Outlook SQLite Scanning — Query Patterns

Verified working queries against the Outlook SQLite database.

## Database Location
```
$HOME/Library/Group Containers/UBF8T346G9.Office/Outlook/Outlook 15 Profiles/Main Profile/Data/Outlook.sqlite
```

## Schema (Mail table — key columns)
| Column | Type | Purpose |
|--------|------|---------|
| Record_RecordID | INTEGER PK | Internal message ID |
| Record_FolderID | INTEGER FK | Links to Folders table |
| Message_NormalizedSubject | TEXT | Email subject (normalized) |
| Message_SenderList | TEXT | Sender name |
| Message_SenderAddressList | TEXT | Sender email address |
| Message_TimeReceived | DATETIME | Unix timestamp |
| Message_ReadFlag | BOOLEAN | 0 = unread, 1 = read |
| Message_HasAttachment | BOOLEAN | 0 or 1 |
| Message_Hidden | BOOLEAN | Filter out hidden/internal |
| Message_IsOutgoingMessage | BOOLEAN | 1 = sent items |

## Last 7 Days — All Folders (Discovery Scan)
```sql
SELECT f.Folder_Name,
       COUNT(*) as cnt,
       SUM(CASE WHEN m.Message_ReadFlag = 0 THEN 1 ELSE 0 END) as unread,
       SUM(CASE WHEN m.Message_HasAttachment = 1 THEN 1 ELSE 0 END) as has_att
FROM Mail m
JOIN Folders f ON m.Record_FolderID = f.Record_RecordID
WHERE m.Message_TimeReceived >= strftime('%s', 'now', '-7 days')
  AND m.Message_Hidden = 0
GROUP BY f.Folder_Name
ORDER BY cnt DESC;
```

## Last N Emails — Full Detail
```sql
SELECT datetime(m.Message_TimeReceived, 'unixepoch') as dt,
       substr(m.Message_NormalizedSubject, 1, 80) as subject,
       substr(m.Message_SenderList, 1, 40) as sender,
       f.Folder_Name as folder,
       m.Record_RecordID as msg_id,
       CASE WHEN m.Message_ReadFlag = 0 THEN 'UNREAD' ELSE '' END as status,
       CASE WHEN m.Message_HasAttachment = 1 THEN '📎' ELSE '' END as att
FROM Mail m
JOIN Folders f ON m.Record_FolderID = f.Record_RecordID
WHERE m.Message_TimeReceived >= strftime('%s', 'now', '-7 days')
  AND m.Message_Hidden = 0
ORDER BY m.Message_TimeReceived DESC
LIMIT 50;
```

## Emails from a Specific Sender (e.g., NRS Director)
```sql
SELECT datetime(m.Message_TimeReceived, 'unixepoch') as dt,
       m.Message_NormalizedSubject,
       f.Folder_Name,
       CASE WHEN m.Message_ReadFlag = 0 THEN 'UNREAD' ELSE '' END as status,
       m.Record_RecordID as msg_id
FROM Mail m
JOIN Folders f ON m.Record_FolderID = f.Record_RecordID
WHERE m.Message_SenderAddressList LIKE '%nissenrichards%'
   OR m.Message_SenderList LIKE '%Nissen%'
ORDER BY m.Message_TimeReceived DESC;
```

## Unread Count Per Folder
```sql
SELECT f.Folder_Name, COUNT(*) as unread
FROM Mail m
JOIN Folders f ON m.Record_FolderID = f.Record_RecordID
WHERE m.Message_ReadFlag = 0 AND m.Message_Hidden = 0
GROUP BY f.Folder_Name
ORDER BY unread DESC;
```

## Get Internal Message ID for AppleScript Download
```sql
SELECT m.Record_RecordID as internal_id,
       datetime(m.Message_TimeReceived, 'unixepoch') as dt,
       m.Message_NormalizedSubject
FROM Mail m
WHERE m.Message_NormalizedSubject LIKE '%Project Query%'
ORDER BY m.Message_TimeReceived DESC
LIMIT 5;
```

Then use the internal_id with AppleScript:
```applescript
tell application "Microsoft Outlook"
    set msg to message id INTERNAL_ID of inbox
    -- download attachments, read body, etc.
end tell
```

## Performance Notes
- SQLite scan is ~1000x faster than AppleScript for discovery (seconds vs minutes).
- Use SQLite for discovery, AppleScript for actions (download, move, delete).
- The Mail table has ~18K+ rows — always use WHERE clauses on Message_TimeReceived or specific folders.
- Message_TimeReceived is a Unix timestamp in seconds. Use `strftime('%s', 'now', '-N days')` for date filtering.
- ID 1 = newest message (verified May 2026). Forward scan = newest-first.
- Folders table: Folder_Name may include trailing spaces for some folders (e.g., "Zamzam Project " vs "Zamzam Project").

## Quick Check — Last 3 Days (when pipeline returns 0)
Proven Jun 4, 2026 — Exchange was disconnected (0 Inbox), SQLite had all emails:
```sql
SELECT datetime(m.Message_TimeReceived, 'unixepoch') as dt,
       m.Message_NormalizedSubject as subj,
       m.Message_SenderAddressList as sender,
       CASE WHEN m.Message_HasAttachment = 1 THEN '📎' ELSE '' END as att
FROM Mail m
WHERE m.Message_TimeReceived > strftime('%s', 'now', '-3 days')
  AND m.Message_Hidden = 0
ORDER BY m.Message_TimeReceived DESC;
```
Add `AND m.Message_IsOutgoingMessage = 0` to exclude sent items if only incoming is needed.
