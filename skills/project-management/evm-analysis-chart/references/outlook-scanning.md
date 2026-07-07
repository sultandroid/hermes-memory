# Outlook Email Scanning for Project Emails

## SQLite Query (Fast Discovery)

Database path:
```
$HOME/Library/Group Containers/UBF8T346G9.Office/Outlook/Outlook 15 Profiles/Main Profile/Data/Outlook.sqlite
```

### Key Tables

- `Mail` — all emails (columns: Message_TimeReceived, Message_NormalizedSubject, Message_SenderList, Message_HasAttachment, Message_ReadFlag, Record_FolderID)
- `Folders` — folder names (columns: Record_RecordID, Folder_Name)

### Useful Queries

**Emails per folder (last 7 days):**
```sql
SELECT f.Folder_Name, COUNT(*) as cnt,
  SUM(CASE WHEN m.Message_ReadFlag = 0 THEN 1 ELSE 0 END) as unread,
  SUM(CASE WHEN m.Message_HasAttachment = 1 THEN 1 ELSE 0 END) as has_att
FROM Mail m JOIN Folders f ON m.Record_FolderID = f.Record_RecordID
WHERE m.Message_TimeReceived >= strftime('%s', 'now', '-7 days')
  AND m.Message_Hidden = 0
GROUP BY f.Folder_Name ORDER BY cnt DESC;
```

**List recent emails with details:**
```sql
SELECT datetime(m.Message_TimeReceived, 'unixepoch') as dt,
  substr(m.Message_NormalizedSubject, 1, 60) as subject,
  m.Message_SenderList as sender,
  f.Folder_Name as folder,
  CASE WHEN m.Message_ReadFlag = 0 THEN 'UNREAD' ELSE '' END as status,
  CASE WHEN m.Message_HasAttachment = 1 THEN '📎' ELSE '' END as att
FROM Mail m JOIN Folders f ON m.Record_FolderID = f.Record_RecordID
WHERE m.Message_TimeReceived >= strftime('%s', 'now', '-7 days')
  AND m.Message_Hidden = 0
ORDER BY m.Message_TimeReceived DESC;
```

### AppleScript for Reading + Downloading

**Read email body:**
```applescript
tell application "Microsoft Outlook"
  set msg to message INTERNAL_ID of folder FOLDER_NAME
  set bodyText to content of msg
  return bodyText
end tell
```

**Download attachment:**
```applescript
tell application "Microsoft Outlook"
  set msg to message INTERNAL_ID of folder FOLDER_NAME
  set atts to file attachments of msg
  repeat with att in atts
    set attName to name of att
    save att in ("/tmp/" & attName)
  end repeat
end tell
```

**Note:** msg 1 = newest. Scan forward from 1 for newest-first iteration. Use `id of msg` to get the Outlook internal message ID.

## Dual-Inbox Architecture

For `sultan@samayainvest.com` (Samaya), two inboxes exist:
- **On My Computer** — old emails, stopped syncing July 2022
- **Exchange** — should receive new emails, may show 0 msgs if disconnected

Always check ALL folders including project subfolders and Deleted Items.
