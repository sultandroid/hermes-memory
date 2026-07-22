# Sender Discovery Patterns — Finding the Right Name/Email Format

When you don't know the exact sender name format stored in Outlook's SQLite DB, use this iterative discovery process.

## The Problem

`Message_SenderList` stores display names (e.g. `Jim Richards`), not email addresses. You can't guess the exact casing or format. A LIKE query with the wrong pattern returns nothing.

## Discovery Workflow

### Step 1 — Check the table structure first

```sql
PRAGMA table_info(Mail);
```

Key columns: `Message_SenderList` (display name), `Message_SenderAddressList` (email), `Message_NormalizedSubject`, `Message_TimeSent` (epoch).

### Step 2 — Verify epoch type

```sql
SELECT Message_TimeSent, datetime(Message_TimeSent, 'unixepoch') as as_unix
FROM Mail ORDER BY Message_TimeSent DESC LIMIT 1;
```

If the date is in 2001/2004 range, it's Mac absolute time (add 978307200). If it shows today, it's standard Unix epoch.

### Step 3 — Broad search to find the exact name format

Start with a partial match on the sender list:

```sql
SELECT DISTINCT Message_SenderList, Message_SenderAddressList
FROM Mail
WHERE Message_SenderList LIKE '%partialname%'
ORDER BY Message_SenderList;
```

This shows you the exact display name format the DB uses.

### Step 4 — Common pitfalls

| What you might try | Why it fails |
|---|---|
| `sender_name LIKE '%niels%'` | Wrong table name (it's `Mail`, not `messages`) |
| `sender LIKE '%jim.richards%'` | `Message_SenderList` stores display names, not email addresses |
| `sender LIKE '%jim@n%'` | Email addresses are in `Message_SenderAddressList`, not `Message_SenderList` |
| `sender LIKE '%nissenrichards%'` | Display name is `Jim Richards`, not the company name |

### Step 5 — Filter out noise

Once you find the sender, filter out system-generated SharePoint notifications and invoices:

```sql
AND Message_NormalizedSubject NOT LIKE '%anonymous access%'
AND Message_NormalizedSubject NOT LIKE '%shared the folder%'
AND Message_NormalizedSubject NOT LIKE '%has changed%'
AND Message_NormalizedSubject NOT LIKE '%has created%'
AND Message_NormalizedSubject NOT LIKE '%Invoice%'
```

### Step 6 — Read previews

`Message_Preview` holds the first ~500 chars of the email body. Use it to understand content without AppleScript:

```sql
SELECT datetime(Message_TimeSent, 'unixepoch') as sent,
       Message_NormalizedSubject as subject,
       Message_Preview as preview
FROM Mail
WHERE Message_SenderList LIKE '%Exact Name%'
ORDER BY Message_TimeSent DESC
LIMIT 10;
```

## Real Example — Jim Richards (NRS)

The correct pattern was:
```sql
WHERE Message_SenderList LIKE '%Jim Richards%'
```

Not `%jim.richards%`, not `%jim@n%`, not `%nissenrichards%`, not `%niels%`.

The display name in the DB is `Jim Richards` (capital J, capital R, space between).
