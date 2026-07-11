# Email Triage / Inbox Review Pattern

When the user asks "check my email", "what's waiting for me", "what action items", or any inbox-review variant.

## Three-Phase Discovery Pattern

### Phase 1 — Quick landscape (folder counts + recent inbox)

```sql
-- Folder sizes (spot which projects have volume)
SELECT f.Folder_Name, COUNT(*) as cnt
FROM Mail m JOIN folders f ON m.Record_FolderID = f.Record_RecordID
GROUP BY f.Folder_Name ORDER BY cnt DESC LIMIT 15;
```

```sql
-- Recent Inbox (last 2-3 days) — the primary triage query
SELECT m.Record_RecordID as id,
       datetime(m.Message_TimeReceived, 'unixepoch', 'localtime') as received,
       f.Folder_Name as folder,
       m.Message_SenderList as sender,
       m.Message_NormalizedSubject as subject,
       CASE WHEN m.Message_HasAttachment = 1 THEN '📎' ELSE '' END as att,
       CASE WHEN m.Message_ReadFlag = 0 THEN '🔵 UNREAD' ELSE '' END as status
FROM Mail m
JOIN folders f ON m.Record_FolderID = f.Record_RecordID
WHERE f.Folder_Name = 'Inbox'
  AND date(m.Message_TimeReceived, 'unixepoch', 'localtime') >= date('now', '-3 days', 'localtime')
ORDER BY m.Message_TimeReceived DESC
LIMIT 20;
```

### Phase 2 — Action signals

Key columns to check for urgency:

| Column | Meaning | Triage Signal |
|--------|---------|---------------|
| `Message_ReadFlag` | 0 = unread | 🔵 flag as needing review |
| `Record_Priority` | 1=high, 2=normal, 3=low | High priority = immediate attention |
| `Record_FlagStatus` | >0 = flagged/follow-up | 🚩 pending action item |
| `Message_HasAttachment` | 1 = has att | 📎 may contain documents to route |
| `Record_DueDate` | Due date if set | Overdue = urgent |

```sql
-- Flagged items (pending follow-ups)
SELECT m.Record_RecordID as id,
       datetime(m.Message_TimeReceived, 'unixepoch', 'localtime') as received,
       m.Message_SenderList as sender,
       m.Message_NormalizedSubject as subject
FROM Mail m
JOIN folders f ON m.Record_FolderID = f.Record_RecordID
WHERE f.Folder_Name = 'Inbox'
  AND m.Record_FlagStatus IS NOT NULL
  AND m.Record_FlagStatus > 0
ORDER BY m.Message_TimeReceived DESC LIMIT 10;
```

```sql
-- High priority unread (most urgent)
SELECT m.Record_RecordID, datetime(m.Message_TimeReceived, 'unixepoch', 'localtime'),
       m.Message_SenderList, m.Message_NormalizedSubject,
       substr(m.Message_Preview, 1, 200) as preview
FROM Mail m
JOIN folders f ON m.Record_FolderID = f.Record_RecordID
WHERE f.Folder_Name = 'Inbox'
  AND m.Message_ReadFlag = 0
  AND (m.Record_Priority = 1 OR m.Record_FlagStatus > 0)
ORDER BY m.Message_TimeReceived DESC LIMIT 5;
```

### Phase 3 — Read previews for top action items

```sql
-- Get body preview + full headers for specific email IDs
SELECT m.Record_RecordID as id,
       datetime(m.Message_TimeReceived, 'unixepoch', 'localtime') as received,
       f.Folder_Name as folder,
       m.Message_SenderList as sender,
       m.Message_SenderAddressList as email,
       m.Message_NormalizedSubject as subject,
       substr(m.Message_Preview, 1, 500) as preview,
       m.Message_HasAttachment as att,
       m.Record_Priority as priority,
       m.Record_FlagStatus as flag
FROM Mail m
JOIN folders f ON m.Record_FolderID = f.Record_RecordID
WHERE m.Record_RecordID IN (<id1>, <id2>, <id3>);
```

```sql
-- Check To/CC for routing verification
SELECT m.Message_ToRecipientAddressList as to_list,
       m.Message_CCRecipientAddressList as cc_list
FROM Mail m WHERE m.Record_RecordID = <ID>;
```

## Project-Specific Triage

Check key project folders for the last 7 days:

```sql
SELECT m.Record_RecordID as id,
       datetime(m.Message_TimeReceived, 'unixepoch', 'localtime') as received,
       m.Message_SenderList as sender,
       m.Message_NormalizedSubject as subject,
       CASE WHEN m.Message_HasAttachment = 1 THEN '📎' ELSE '' END as att,
       CASE WHEN m.Message_ReadFlag = 0 THEN '🔵 UNREAD' ELSE '' END as status
FROM Mail m
JOIN folders f ON m.Record_FolderID = f.Record_RecordID
WHERE f.Folder_Name = '<Project Folder>'
  AND date(m.Message_TimeReceived, 'unixepoch', 'localtime') >= date('now', '-7 days', 'localtime')
ORDER BY m.Message_TimeReceived DESC LIMIT 15;
```

## AppleScript Inbox Access — Known Limitations & Workarounds

SQLite is blocked by macOS TCC (`authorization denied`). AppleScript is the only access path, but has critical quirks:

### `where unread is true` DOES NOT WORK

```applescript
-- ❌ FAILS: "The variable unread is not defined" (-2753)
every message of inbox where unread is true
every message of inbox whose unread is true
```

Outlook for Mac does not expose `unread` as a filterable property in AppleScript. The `read status` property exists but cannot be used in `where`/`whose` clauses — it throws `Can't get status` (-1728) or `Can't make application into type file` (-1700).

### Reliable Workaround — Per-Index One-Liners

The only reliable way to read inbox messages is by **numeric index** (1 = newest):

```bash
# Read subject of message N
osascript -e "tell application \"Microsoft Outlook\" to get subject of message $N of inbox"

# Read full body
osascript -e "tell application \"Microsoft Outlook\" to get plain text content of message $N of inbox"

# Read multiple properties (one call per property)
for i in 1 2 3 4 5; do
  subj=$(osascript -e "tell application \"Microsoft Outlook\" to get subject of message $i of inbox" 2>/dev/null)
  att=$(osascript -e "tell application \"Microsoft Outlook\" to get has attachment of message $i of inbox" 2>/dev/null)
  echo "$i|$subj|$att"
done
```

**Why this works:** Each `osascript -e` is a separate process invocation. The ~700-byte script body limit applies per file, not per process. One-liners stay well under the limit.

### `has attachment` is Unreliable

The `has attachment` property of `message` returns **empty string** for most messages, even those with attachments. Do not rely on it for triage. The only reliable attachment detection is:
1. Extract all attachments via AppleScript `save` and count them
2. Or check the SQLite `Message_HasAttachment` column (when SQLite is accessible)

### `plain text content` Works for Inbox (Contrary to Earlier Notes)

Despite the skill's earlier pessimism, `plain text content of message N of inbox` **reliably returns full email body** for inbox messages. It worked for all 13+ emails tested in this session. The earlier note about empty returns applies to project sub-folders and archived messages, not the inbox.

### `sender` Returns a Record, Not a String

```applescript
-- ❌ FAILS: returns a Mail Recipient record, not text
set s to sender of m

-- ✅ WORKS: wrap in try block with as-text coercion
set senderName to ""
try
    set senderRecord to sender of m
    set senderName to (name of senderRecord) as text
end try
```

This applies to ALL senders, not just Aconex. The skill's earlier Aconex-specific note was too narrow.

### Unread Count is Reliable

```applescript
osascript -e 'tell application "Microsoft Outlook" to get unread count of inbox'
```

This single property read works correctly and returns the actual count.

## Presentation Format

Group results into sections by urgency:

1. **🔴 Immediate Actions Needed** — flagged / high priority / "URGENT" / "please issue PO" / task assignments
2. **🔵 Unread — Need Review** — unread emails with subject and attachment indicator
3. **📋 Project-Specific — Awaiting Review** — recent activity in project folders
4. **🏷️ Flagged / Pending Items** — older flagged items that haven't been actioned
5. **✅ Key Takeaways** — 2-4 bullet summary of what needs actual work

For each email in the top sections, show: sender, subject (Arabic → concise English), timestamp, attachment indicator, and any priority/flag signals. Keep it compact — the user scans quickly.

## Common Patterns by Role

- **PO/PR requests** from Adel Darwish or project team → "please issue PO" = immediate action
- **Task/mention notifications** from Office/Teams (Ali Abdelrahman, shared Excel) → check the file
- **Submittals for review** (DOC, IR, SI codes) → read → either approve or route to QC
- **Consultant deliverables** (Jim Richards, Ahmed Metwally, Mimon Allitou) → verify against schedule
- **Vendor approvals** (fire rated doors, materials) → review attachment and approve/reject

## CG Consultant Weekly Filter

When the user asks "list CG this week" or "CG emails":

```sql
SELECT m.Record_RecordID as id,
       datetime(m.Message_TimeReceived, 'unixepoch', 'localtime') as received,
       f.Folder_Name as folder,
       m.Message_SenderList as sender,
       m.Message_SenderAddressList as email,
       m.Message_NormalizedSubject as subject,
       substr(m.Message_Preview, 1, 300) as preview,
       CASE WHEN m.Message_HasAttachment = 1 THEN '📎' ELSE '' END as att
FROM Mail m
JOIN folders f ON m.Record_FolderID = f.Record_RecordID
WHERE (m.Message_SenderAddressList LIKE '%@cg.com.sa%'
   OR m.Message_SenderList IN ('Hossam Mabrouk', 'Mansour Alrezeni'))
  AND date(m.Message_TimeReceived, 'unixepoch', 'localtime') >= date('now', 'weekday 1', '-7 days', 'localtime')
ORDER BY m.Message_TimeReceived DESC;
```

### Known CG Contacts & Response Codes

| Sender | Email | Role | Domain |
|--------|-------|------|--------|
| Hossam Mabrouk | hmabrouk@cg.com.sa | CG Consultant — document submittals | Aseer Museum |
| Mansour Alrezeni | malrezeni@cg.com.sa | CG Consultant — site/design coordination | Aseer Museum |
| Mohammad Elbaz | melbaz@cg.com.sa | CG Consultant — plan/submittal review | Aseer Museum |
| Anwar Sadat | asadat@cg.com.sa | CG — Safety/QA observations | Aseer Museum |
| Mohammed Elroby | melroby@cg.com.sa | CG Consultant | Aseer Museum |

**Response code triage:**
- **Code A** — Approved → no action, file
- **Code B** — Approved with Comments → read comments, respond as needed, close out
- **Code C** — Rejected → must resubmit — highest priority. Identify missing items, fix, and resubmit
- **Code D** — Not Reviewed → track for follow-up

CG emails live in three places: Inbox (initial delivery), Asher Regional Museum folder (filed project correspondence), and Sent Items (your replies). Check all three for a complete picture.