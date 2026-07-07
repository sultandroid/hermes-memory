# Reading Outlook Emails from SQLite (Samaya macOS Setup)

## When to use

User asks you to check their Outlook emails, find recent messages, or extract email intelligence. The Outlook app for Mac stores all email metadata (subject, sender, preview, timestamps, attachment flags) in a local SQLite database that can be queried directly.

## Database location

```
~/Library/Group Containers/UBF8T346G9.Office/Outlook/Outlook 15 Profiles/Main Profile/Data/Outlook.sqlite
```

## Practical query

```python
import sqlite3, datetime
from pathlib import Path

db = str(Path.home() / 'Library/Group Containers/UBF8T346G9.Office/Outlook/Outlook 15 Profiles/Main Profile/Data/Outlook.sqlite')

conn = sqlite3.connect(db)
cursor = conn.cursor()
cursor.execute('''
SELECT Message_TimeReceived, Message_NormalizedSubject, Message_IsOutgoingMessage,
       Message_SenderList, Message_HasAttachment
FROM Mail ORDER BY Message_TimeReceived DESC LIMIT 20
''')
for r in cursor.fetchall():
    ts, subj, out, sender, att = r
    dt = datetime.datetime.fromtimestamp(ts) if ts else None
    d = '→' if out else '←'
    a = ' 📎' if att else ''
    print(f'{d} [{dt.strftime("%d-%b %H:%M") if dt else "?"}] {str(sender)[:30]} | {str(subj)[:80]}{a}')
```

## Limitations

- **Attachments cannot be extracted** — Files table uses a custom virtual module not queryable by standard sqlite3
- **Only one Exchange account**: sultan@samayainvest.com (shared TO inbox)
- **AppleScript unreliable** — messages of inbox returns 0 even with data in DB
- **Workaround**: ask user to open Outlook and save attachments to Downloads
