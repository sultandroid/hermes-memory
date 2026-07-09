# Aconex Notification Email Patterns

Aconex (Oracle Construction & Engineering) sends system-generated notification emails when transmittals complete workflows. These are **notification-only** — no document bodies attached. Actual submittal PDFs live inside the Aconex web portal.

## Sender Format

| Field | Value |
|-------|-------|
| SenderList | `Aconex Notification` or `Aconex Notification (Aseer Museum)` |
| No email address | The sender is a display name, not an email address — query `Message_SenderList LIKE '%Aconex%'` not `Message_SenderAddressList` |

## Transmittal Naming Convention

```
{ProjectCode}-WTRAN-{Number}: Final (WF-{Number}) {Description}
```

Two prefixes indicate direction:

| Prefix | Direction | Meaning |
|--------|-----------|---------|
| `CGP-WTRAN-*` | CG/PMC → Samaya | Final review outcomes, approvals, rejections |
| `SIC.-WTRAN-*` | Samaya → CG/PMC | Submissions from contractor |

### Examples

```
CGP-WTRAN-000086: Final (WF-000049) ICT Security System Integrator / IT
SIC.-WTRAN-000043: (WF-000078) Time Schedule
SIC.-TRANSMIT-000004: Approved Time Schedule as historical information - back log
```

## Other Aconex System Notifications

| Subject Pattern | Purpose |
|----------------|---------|
| `Aconex Metadata Template download ready` | Metadata export completed |
| `Aconex Docs Export to Excel ready` | Document register export ready |
| `Your Aconex account has been created` | New user account |
| `Historical back log: Historical information - BACK LOG` | Bulk historical data import |

## Attachments

- **Transmittal notifications have NO attachments** — they are purely informational
- Only setup/training emails (e.g., "Creation of Aconex User Accounts") may have attachments (e.g., user list spreadsheets)

## SQLite Query Pattern

```sql
-- Find all Aconex emails
SELECT 
    datetime(Message_TimeReceived, 'unixepoch') as received,
    Message_NormalizedSubject,
    Message_SenderList,
    Message_DisplayTo,
    CASE WHEN Message_HasAttachment THEN 'YES' ELSE 'no' END as att,
    Message_Size
FROM Mail 
WHERE Message_SenderList LIKE '%Aconex%'
ORDER BY Message_TimeReceived DESC;
```

## Epoch Offset Issue

Outlook SQLite timestamps use **Mac absolute time** (seconds since 2001-01-01), not Unix epoch (1970-01-01). The offset is **978307200 seconds**.

| Expression | Result |
|------------|--------|
| `datetime(col, 'unixepoch')` | ❌ Wrong — interprets as Unix epoch |
| `datetime(col + 978307200, 'unixepoch')` | ✅ Correct — adds Mac→Unix offset |
| `Historical back log: Historical information - BACK LOG` | Bulk historical data import |
| `Request for Previous Aconex Transactions` | CG request to upload backlog transactions — multi-week thread with reminders |
| `Aconex Docs Export to Excel ready` | Document register export ready |

## "Request for Previous Aconex Transactions" Thread Pattern

- **Heavy weeks:** 30-40+ notifications per week during active submittal periods
- **Light weeks:** 0-5 during setup/training phases
- **Setup phase:** Training invitations, account creation emails (Feb-Mar)
- **Active phase:** Transmittal notifications dominate (Apr onward)
