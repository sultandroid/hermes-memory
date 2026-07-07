# Outlook SQLite — Python `execute_code` Patterns

**Proven:** Jun 4, 2026 — extracted 162 emails from last 3 days when Exchange was disconnected.

## Why Python Instead of Shell

- Paths with spaces, parentheses (e.g. `Group Containers`) don't need escaping
- No ambiguity with `'` vs `"` in SQL strings
- Parameterized queries prevent injection and work correctly with binary data
- `conn.text_factory = str` handles Arabic/Chinese subjects without UnicodeDecodeError

## Schema Reference

### Mail table (46 columns — key ones)

| Column | Type | Purpose |
|--------|------|---------|
| `Record_RecordID` | INTEGER PK | Internal message ID (use as `message id X` in AppleScript) |
| `Record_ModDate` | DATETIME | Last modified timestamp (Unix epoch) — best for "recent activity" |
| `Record_FolderID` | INTEGER FK | → `Folders.Record_RecordID` |
| `Record_AccountUID` | INTEGER | Account this message belongs to |
| `Message_NormalizedSubject` | TEXT | Subject (normalized, may be NULL) |
| `Message_SenderAddressList` | TEXT | Sender email (e.g. `jim.r@nissenrichardsstudio.com`) |
| `Message_SenderList` | TEXT | Sender display name (e.g. `Jim Richards`) |
| `Message_DisplayTo` | TEXT | To: field display names |
| `Message_ToRecipientAddressList` | TEXT | To: email addresses |
| `Message_CCRecipientAddressList` | TEXT | CC: email addresses |
| `Message_TimeReceived` | DATETIME | Original receipt timestamp (Unix epoch) |
| `Message_ReadFlag` | BOOLEAN | 0=unread, 1=read |
| `Message_HasAttachment` | BOOLEAN | 0=no, 1=yes |
| `Message_Hidden` | BOOLEAN | Filter out internal/hidden messages (WHERE Message_Hidden=0) |
| `Message_IsOutgoingMessage` | BOOLEAN | 1=sent item, 0=incoming |
| `Message_Size` | INTEGER | Size in bytes |
| `PathToDataFile` | TEXT | Path to `.olk15Message` file (proprietary format) |
| `Message_Preview` | TEXT | Email body preview (first ~255 chars) |

### Folders table (20 columns — key ones)

| Column | Type | Purpose |
|--------|------|---------|
| `Record_RecordID` | INTEGER PK | Folder ID |
| `Folder_Name` | TEXT | Display name (watch for trailing spaces!) |
| `Folder_ParentID` | INTEGER | Parent folder ID (self-referencing FK) |
| `Folder_SpecialFolderType` | INTEGER | 1=Inbox, 2=Outbox, 3=Drafts, 4=Sent, 5:Junk, 8=SentItems, 9=DeletedItems, 10=Drafts |
| `Record_AccountUID` | INTEGER | Account this folder belongs to |

### Conversations table

| Column | Type | Purpose |
|--------|------|---------|
| `Record_RecordID` | INTEGER PK | Conversation ID |
| `Conversation_ConversationTopic` | TEXT | Conversation topic/thread |
| `Conversation_MessageCount` | INTEGER | Number of messages in thread |

## Proven Query Patterns

### Time-range with Python timestamps (preferred)
```python
from datetime import datetime, timedelta
cutoff = int((datetime.now() - timedelta(days=3)).timestamp())
c.execute("""
    SELECT datetime(m.Record_ModDate, 'unixepoch'),
           m.Message_NormalizedSubject,
           m.Message_SenderAddressList,
           m.Message_HasAttachment,
           COALESCE(f.Folder_Name, 'Unknown')
    FROM Mail m
    LEFT JOIN Folders f ON m.Record_FolderID = f.Record_RecordID
    WHERE m.Record_ModDate >= ?
    ORDER BY m.Record_ModDate DESC
""", (cutoff,))
```

### Count per folder
```python
c.execute("""
    SELECT f.Folder_Name, COUNT(*)
    FROM Mail m
    LEFT JOIN Folders f ON m.Record_FolderID = f.Record_RecordID
    WHERE m.Record_ModDate >= ?
    GROUP BY f.Folder_Name
    ORDER BY COUNT(*) DESC
""", (cutoff,))
```

### Emails with attachments only
```python
c.execute("""
    SELECT datetime(m.Record_ModDate, 'unixepoch'),
           m.Message_NormalizedSubject,
           m.Message_SenderAddressList
    FROM Mail m
    WHERE m.Record_ModDate >= ?
      AND m.Message_HasAttachment = 1
      AND m.Message_Hidden = 0
    ORDER BY m.Record_ModDate DESC
""", (cutoff,))
```

### Sender domain search
```python
c.execute("""
    SELECT datetime(m.Record_ModDate, 'unixepoch'),
           m.Message_NormalizedSubject,
           m.Message_SenderAddressList,
           CASE WHEN m.Message_HasAttachment = 1 THEN 'Y' ELSE 'N' END
    FROM Mail m
    WHERE m.Message_SenderAddressList LIKE ?
      AND m.Record_ModDate >= ?
    ORDER BY m.Record_ModDate DESC
""", ('%@cg.com.sa', cutoff))
```

### Get internal message IDs for AppleScript download
```python
c.execute("""
    SELECT m.Record_RecordID,
           datetime(m.Message_TimeReceived, 'unixepoch'),
           m.Message_NormalizedSubject
    FROM Mail m
    WHERE m.Message_NormalizedSubject LIKE ?
    ORDER BY m.Message_TimeReceived DESC
    LIMIT 10
""", ('%Aseer Museum%Gallery 9%',))
```

## Edge Cases

- **Folder with trailing space**: `Zamzam Project ` (with space) vs `Zamzam Project` without — they are DIFFERENT folders. The trailing-space variant is under Deleted Items.
- **NULL subjects**: Some system/internal messages have NULL `Message_NormalizedSubject`. Wrapping with `COALESCE(..., '')` prevents None crashes.
- **Message_type values**: All inbox/regular messages have `Message_type = 1165517645`.
- **DownloadState**: 3 = fully downloaded, 0 = not downloaded. When Exchange is disconnected, ALL messages show DownloadState=0 for attachment binary data, even though metadata is fully cached.
- **`Record_ModDate` vs `Message_TimeReceived`**: `Record_ModDate` updates when any property changes (read flag, move, etc.); `Message_TimeReceived` is the original delivery time. Use `Record_ModDate` for "what's new since last check" and `Message_TimeReceived` for "when was this sent."

## Why WhatsApp/System Messages Won't Appear

WhatsApp messages stored by the iOS/macOS proxy show up in a separate `WhatsApp/` folder structure via different MAPI stores, not the Exchange Mail table. To find them, search the entire table for `%whatsapp%` in subject or sender, or check iMessage independently.
