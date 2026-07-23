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

## Epoch Verification (MANDATORY before any query)

**Do NOT assume the epoch.** The active database at `Data/Outlook.sqlite` (with `Mail`/`folders` tables) uses **Unix epoch** — no offset needed. The old root-level `Outlook.sqlite` (0 bytes) is a stub. Always verify:

```sql
SELECT Message_TimeReceived,
       datetime(Message_TimeReceived, 'unixepoch', 'localtime') as as_unix,
       datetime(Message_TimeReceived + 978307200, 'unixepoch', 'localtime') as as_mac
FROM Mail ORDER BY Message_TimeReceived DESC LIMIT 1;
```

The one showing today's date is correct.

| Expression | When to use |
|------------|-------------|
| `datetime(col, 'unixepoch', 'localtime')` | ✅ When `as_unix` shows today's date |
| `datetime(col + 978307200, 'unixepoch', 'localtime')` | ✅ When `as_mac` shows today's date |

## Other Aconex System Notifications

| Subject Pattern | Purpose |
|----------------|---------|
| `Aconex Metadata Template download ready` | Metadata export completed |
| `Aconex Docs Export to Excel ready` | Document register export ready |
| `Your Aconex account has been created` | New user account |
| `Historical back log: Historical information - BACK LOG` | Bulk historical data import |
| `Request for Previous Aconex Transactions` | CG request to upload backlog transactions — multi-week thread with reminders |

## "Request for Previous Aconex Transactions" Thread Pattern

- **Heavy weeks:** 30-40+ notifications per week during active submittal periods
- **Light weeks:** 0-5 during setup/training phases
- **Setup phase:** Training invitations, account creation emails (Feb-Mar)
- **Active phase:** Transmittal notifications dominate (Apr onward)
