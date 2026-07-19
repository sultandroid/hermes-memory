# Outlook SQLite Database Paths

## Primary Path (macOS Outlook 2019+)

The Outlook database is at a fixed path under the Office Group Container:

```
~/Library/Group Containers/UBF8T346G9.Office/Outlook/Outlook 15 Profiles/Main Profile/Data/Outlook.sqlite
```

This is the **only** path that contains the `Mail`, `Folders`, `Blocks`, and `Mail_OwnedBlocks` tables. It is **not** on OneDrive — it lives in the local `Group Containers` directory.

## Schema Notes

| Table | Key Columns |
|-------|-------------|
| `Mail` | `Record_RecordID`, `Message_SenderList`, `Message_SenderAddressList`, `Message_NormalizedSubject`, `Message_TimeReceived` (Unix epoch), `Message_Preview`, `Message_HasAttachment`, `Conversation_ConversationID`, `Record_FolderID` |
| `Folders` | `Record_RecordID`, `Folder_Name`, `Folder_ParentID`, `Folder_FolderType` |
| `Blocks` | `BlockID`, `BlockTag`, `PathToDataFile` |
| `Mail_OwnedBlocks` | `Record_RecordID`, `BlockID`, `BlockTag` |

## Epoch Verification

Always verify the timestamp column before querying:

```sql
SELECT Message_TimeReceived,
       datetime(Message_TimeReceived, 'unixepoch', 'localtime') as as_unix,
       datetime(Message_TimeReceived + 978307200, 'unixepoch', 'localtime') as as_mac
FROM Mail ORDER BY Message_TimeReceived DESC LIMIT 1;
```

The `as_unix` column showing today's date confirms standard Unix epoch. If `as_mac` is correct instead, add 978307200 to all timestamp columns.

## Troubleshooting

1. **TCC permission denied**: macOS sometimes blocks `sqlite3` access to the Group Container. Retry — the TCC grant is session-dependent. If it fails repeatedly, fall back to AppleScript.
2. **Database not found**: Verify Outlook is installed at `/Applications/Microsoft Outlook.app`. The Group Container path is created on first launch.
3. **No `.olk15Message` files in the container**: The new Outlook (2019+) stores messages in the `HxStore.hxd` file, not as individual `.olk15` files. The SQLite `Mail` table is the primary interface.
