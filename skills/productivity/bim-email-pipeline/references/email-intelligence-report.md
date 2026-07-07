# Email Intelligence Report — Reusable Pattern

Template for producing a comprehensive email report from Outlook SQLite when AppleScript iteration is blocked by 18K+ inbox.

## When to Use

- User says "check emails" / "check outlook"
- Pipeline script returns 0
- AppleScript is too slow to scan 18K Exchange inbox messages

## Python Pattern (execute_code) — Avoids Shell Quoting Issues

```python
import sqlite3, time
from datetime import datetime, timedelta
from collections import Counter

db = "/Users/mohamedessa/Library/Group Containers/UBF8T346G9.Office/Outlook/Outlook 15 Profiles/Main Profile/Data/Outlook.sqlite"
conn = sqlite3.connect(db)
conn.text_factory = str  # ← critical for Arabic/Unicode subjects
c = conn.cursor()

three_days = int((datetime.now() - timedelta(days=3)).timestamp())

# Get all recent emails with folder names
c.execute("""
    SELECT m.Record_RecordID,
           datetime(m.Record_ModDate, 'unixepoch'),
           COALESCE(m.Message_NormalizedSubject, ''),
           COALESCE(m.Message_SenderAddressList, ''),
           m.Message_HasAttachment,
           m.Message_Size,
           COALESCE(f.Folder_Name, '')
    FROM Mail m
    LEFT JOIN Folders f ON m.Record_FolderID = f.Record_RecordID
    WHERE m.Record_ModDate >= ?
    ORDER BY m.Record_ModDate DESC
""", (three_days,))

emails = c.fetchall()
```

## Project Classification Map (Subject Keyword Based)

```python
project_map = {
    "Zamzam": ["zamzam", "زمزم", "zvc"],
    "Aseer Museum": ["aseer", "عسير", "asher", "asir", "nrs", "nissen"],
    "El-Ghamama / Jabal Omar": ["ghamama", "غمامة", "jabal omar", "جبل عمر", "qahwtna", "قهوتنا"],
    "Haramain": ["haramain", "حرمين", "maalim"],
    "Al Galal / Al Gamal": ["galal", "جلال", "جمال", "الجمال"],
    "Al Faw": ["faw", "الفاو"],
    "ERP / Purchasing": ["p0", "أمر شراء", "purchase order", "شراء"],
    "Admin / Operations": ["سيارة", "صيانة", "إزالة", "طلب ", "الأجر", "مخلفات"],
    "Meetings": ["meeting", "اجتماع", "zoom", "teams call", "دعوة"],
    "Marketing / Newsletters": ["newsletter", "rhino", "webinar", "expo", "sponsor"],
}
```

## Action Indicators (Flag as "Requires Action")

```python
action_indicators = [
    "rfi", "request for info", "request for review", "approval",
    "cg", "elbaz", "jim richards", "nrs", "urgent", "reject",
    "disapprove", "letter", "si-", "tq-", "ncr", "code c", "code d",
    "resubmit", "revise", "comment", "remark", "response",
    "meeting request", "review and approval"
]
```

## SQLite Schema Reference (Key Columns)

### Mail Table
| Column | Type | Usage |
|--------|------|-------|
| `Record_ModDate` | Unix timestamp | Use for "recent" queries (last modified) |
| `Message_TimeReceived` | Unix timestamp | Original delivery time (may be 0 for drafts) |
| `Message_NormalizedSubject` | Text | Subject line (Unicode-safe) |
| `Message_SenderAddressList` | Text | Sender email |
| `Message_DisplayTo` | Text | Display name of recipients |
| `Message_HasAttachment` | Integer | 1 = has attachments |
| `Message_DownloadState` | Integer | 3 = fully downloaded |
| `Message_PartiallyDownloaded` | Integer | 0 = complete |
| `Message_Size` | Integer | Size in bytes |
| `Message_ReadFlag` | Integer | 0 = unread |
| `Record_FolderID` | Integer | FK to Folders |
| `Record_AccountUID` | Integer | 60129542145 = Exchange |
| `Record_ExchangeOrEasId` | Text | Full Exchange ID for targeted AppleScript access |
| `PathToDataFile` | Text | Path to .olk15Message file |
| `Message_MessageID` | Text | SMTP Message-ID header |

### Folders Table (Critical Correction)

Column is `Folder_Name`, NOT `name`:
```sql
SELECT Record_RecordID, Folder_Name, Record_AccountUID, Folder_SpecialFolderType FROM Folders;
```

### Account UIDs
- `60129542145` = Exchange account (sultan@samayainvest.com)
- Check `AccountsExchange` table for Record_RecordID mapping

## Report Template

After extraction, deliver a markdown table like:

```
## 📧 Email Report — Last N Days

**X emails total | Y with attachments**

### 🔴 [Project Name] — N emails

| Time | From | Subject | Att | Action |
|------|------|---------|:---:|--------|
| Jun 4 10:47 | sender@domain | **Subject** | 📎 | Action needed |

### ⚪ CG Responses Received

Doc codes with status.

### Actions Needed From You

1. ...
```

## Critical Lessons (June 4, 2026)

1. **Exchange IS connected** — the `online of exchange account` AppleScript property is unreliable for modern Exchange Online. Always verify by checking `inbox of a` (Exchange account's inbox) which showed 18,231 msgs.
2. **AppleScript can't index recent Exchange-cached messages** — even scanning last 500 of 18,231 found 0 from 2026. Use SQLite for discovery.
3. **All 162 recent emails were fully cached** (DownloadState=3, PartiallyDownloaded=0) in SQLite despite being inaccessible via AppleScript index.
4. **conn.text_factory = str** is mandatory for Python sqlite3 — without it, Arabic subjects raise `UnicodeDecodeError`.
5. **Record_ModDate vs Message_TimeReceived**: `Record_ModDate` tracks when Outlook last touched the record (caching/syncing). `Message_TimeReceived` is the original SMTP delivery time. For "last 3 days" queries, `Record_ModDate` is more reliable because it reflects when the Exchange sync engine wrote the email to the local cache.
