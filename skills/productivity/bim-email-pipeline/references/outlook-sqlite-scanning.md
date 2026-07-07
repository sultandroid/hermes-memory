# Outlook SQLite Direct Scanning

**Date discovered:** 2026-05-29
**Context:** Aseer Museum CG response audit — needed to find ALL CG consultant emails (@cg.com.sa) across ALL Outlook folders, not just Inbox.

## Technique

Outlook for Mac stores all mail data in an SQLite database at:

```
~/Library/Group Containers/UBF8T346G9.Office/Outlook/Outlook 15 Profiles/Main Profile/Data/Outlook.sqlite
```

### Key Tables

| Table | Content |
|-------|---------|
| `Mail` | All email messages (inbox, sent, archive, drafts, etc.) |
| `Folders` | All folder definitions |
| `Conversations` | Conversation threads |
| `Threads` | Thread grouping |
| `Files` | Attachments |

### Mail Table Schema (key columns)

| Column | Type | Content |
|--------|------|---------|
| `Record_RecordID` | INTEGER PK | Message ID |
| `Record_FolderID` | INTEGER FK → Folders.Record_RecordID | Folder this message belongs to |
| `Message_NormalizedSubject` | TEXT | Subject line |
| `Message_SenderAddressList` | TEXT | Sender email address |
| `Message_TimeReceived` | DATETIME (unix epoch) | When received |
| `Message_ReadFlag` | BOOLEAN | 0=unread, 1=read |
| `Message_HasAttachment` | BOOLEAN | 0/1 |
| `Message_DisplayTo` | TEXT | To recipients |
| `Message_Preview` | TEXT | Email preview snippet |

### Folders Table Schema (key columns)

| Column | Type | Content |
|--------|------|---------|
| `Record_RecordID` | INTEGER PK | Folder ID |
| `Folder_Name` | TEXT | Display name |
| `Folder_ParentID` | INTEGER | Parent folder ID |
| `Folder_SpecialFolderType` | INTEGER | 1=Inbox, 2=Drafts, 3=Sent, 4=Deleted, etc. |
| `Record_AccountUID` | INTEGER | Account ID |

## Useful Queries

### Find Inbox folder ID
```sql
SELECT Record_RecordID, Folder_Name FROM Folders 
WHERE Folder_Name LIKE '%Inbox%' OR Folder_SpecialFolderType = 1;
```

### Find all folders
```sql
SELECT Record_RecordID, Folder_Name, Folder_SpecialFolderType FROM Folders ORDER BY Folder_Name;
```

### Search for emails from specific domain across ALL folders
```sql
SELECT datetime(m.Message_TimeReceived, 'unixepoch') as dt,
       m.Message_NormalizedSubject as subj,
       m.Message_SenderAddressList as sender,
       f.Folder_Name as folder,
       CASE WHEN m.Message_ReadFlag = 0 THEN 'UNREAD' ELSE 'read' END as status
FROM Mail m
JOIN Folders f ON m.Record_FolderID = f.Record_RecordID
WHERE m.Message_TimeReceived > strftime('%s', 'now', '-60 days')
  AND m.Message_SenderAddressList LIKE '%@cg.com.sa'
ORDER BY m.Message_TimeReceived DESC;
```

### Search by subject pattern
```sql
SELECT datetime(m.Message_TimeReceived, 'unixepoch') as dt,
       m.Message_NormalizedSubject,
       m.Message_SenderAddressList,
       f.Folder_Name
FROM Mail m
JOIN Folders f ON m.Record_FolderID = f.Record_RecordID
WHERE m.Message_NormalizedSubject LIKE '%MOC-MUS%'
   OR m.Message_NormalizedSubject LIKE '%SI-CG%'
   OR m.Message_NormalizedSubject LIKE '%NCR%'
ORDER BY m.Message_TimeReceived DESC;
```

### Find unread emails with attachments from specific domain
```sql
SELECT m.Record_RecordID, m.Message_NormalizedSubject, 
       datetime(m.Message_TimeReceived, 'unixepoch') as dt,
       m.Message_SenderAddressList
FROM Mail m
JOIN Folders f ON m.Record_FolderID = f.Record_RecordID
WHERE m.Message_ReadFlag = 0
  AND m.Message_HasAttachment = 1
  AND m.Message_SenderAddressList LIKE '%@cg.com.sa'
ORDER BY m.Message_TimeReceived DESC;
```

### Broad project email sweep — last N days (Arabic + English)
```sql
SELECT m.Record_RecordID,
       datetime(m.Message_TimeReceived, 'unixepoch') as dt,
       m.Message_SenderAddressList as sender,
       m.Message_NormalizedSubject as subj,
       CASE WHEN m.Message_HasAttachment = 1 THEN '📎' ELSE '  ' END as att,
       CASE WHEN m.Message_ReadFlag = 0 THEN '🔴' ELSE '  ' END as readst,
       m.Message_Size/1024 as kb
FROM Mail m
WHERE m.Message_TimeReceived > strftime('%s', 'now', '-10 days')
  AND (m.Message_SenderAddressList LIKE '%samayainvest.com'
       OR m.Message_SenderAddressList LIKE '%cg.com.sa'
       OR m.Message_SenderAddressList LIKE '%nissenrichards%'
       OR m.Message_NormalizedSubject LIKE '%MOC-MUS%'
       OR m.Message_NormalizedSubject LIKE '%متحف%'
       OR m.Message_NormalizedSubject LIKE '%تسعير%'
       OR m.Message_NormalizedSubject LIKE '%زمزم%'
       OR m.Message_NormalizedSubject LIKE '%جبل عمر%'
       OR m.Message_NormalizedSubject LIKE '%Lighting%'
       OR m.Message_NormalizedSubject LIKE '%Mobilization%'
       OR m.Message_NormalizedSubject LIKE '%Artec%'
       OR m.Message_NormalizedSubject LIKE '%تقرير%'
       OR m.Message_NormalizedSubject LIKE '%MVii%'
       OR m.Message_NormalizedSubject LIKE '%Spider%'
       OR m.Message_NormalizedSubject LIKE '%جلال%')
ORDER BY m.Message_TimeReceived DESC;
```

This catches all project emails including Arabic subjects. Adjust `-10 days` for window size, add project keywords as needed.

## Advantages Over AppleScript

| Aspect | SQLite | AppleScript |
|--------|--------|-------------|
| Speed | ~100ms for complex queries | 60-120s for 500 messages |
| All folders | Yes — JOIN Folders table | Inbox only (single folder) |
| Bulk search | Full SQL — regex, date ranges, joins | Sequential scan, no joins |
| Historical data | Full mailbox history | Limited by scan cutoff |
| Reliability | Always works (offline DB) | Depends on Outlook running |
| Attachment DL | Cannot download attachments | Can download attachments |

## Limitations

- **Cannot download attachments** — SQLite has the file paths but attachments are stored in the `Files` table with blob data or external references. Use AppleScript for actual download.
- **Cannot send/reply** — read-only discovery
- **Column names may change** between Outlook versions — always check `.schema` first
- **Requires full disk access** for sandboxed processes

## When to Use

- **Discovery phase** — find all emails matching criteria (sender, subject, date range, folder) — SQLite is faster and more thorough
- **Status tracking** — check read/unread status, find unread emails across all folders
- **Cross-referencing** — find emails from senders across all folders, count emails per sender per day
- **Then use AppleScript** for the specific emails you identified as needing attachment download

## Proven Pattern (May 29, 2026)

1. Use SQLite to find all relevant emails across ALL folders
2. Classify and plan what needs to happen
3. Use AppleScript only for targeted attachment downloads
4. This avoids the 60-120s scan time for every check
