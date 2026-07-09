# Aconex Transmittal Sync from Outlook

Query Outlook SQLite for Aconex workflow transmittal notifications and update the submittal register without duplication.

## SQLite Query

```sql
-- All Aconex emails
SELECT 
    datetime(Message_TimeReceived + 978307200, 'unixepoch') as received,
    Message_NormalizedSubject,
    Message_SenderList,
    Message_DisplayTo,
    Message_Preview
FROM Mail 
WHERE Message_SenderList LIKE '%aconex%' 
   OR Message_NormalizedSubject LIKE '%Aconex%'
ORDER BY Message_TimeReceived DESC;
```

**Note:** Outlook SQLite timestamps use Mac absolute time (seconds since 2001-01-01). Add 978307200 to convert to Unix epoch.

## Transmittal Categorization

| Prefix | Direction | Meaning |
|--------|-----------|---------|
| `CGP-WTRAN-` | CG → Samaya | Final review outcomes returned to contractor |
| `SIC.-WTRAN-` | Samaya → CG | New submissions from contractor to consultant |
| `SIC.-TRANSMIT-` | Samaya → CG | Non-workflow transmittals (historical backlog) |
| `MOC-MUS-ASE-*` | Either | Direct document transmittals (not workflow) |

## Dedup Logic

Match by transmittal number (e.g. `CGP-WTRAN-000086`). If already present in the register's Aconex Transmittals section, skip.

```python
# Extract transmittal number from subject
import re
m = re.search(r'(CGP-WTRAN-\d+|SIC\.-WTRAN-\d+|SIC\.-TRANSMIT-\d+)', subject)
if m:
    tran_no = m.group(1)
    # Check if already in register
    if tran_no not in existing_transmittals:
        # Add to appropriate table
```

## Cron Job Pattern

```bash
# Schedule: 0 */6 * * *  (4x daily)
# Workdir: ~/Documents/Asher_Regional_Museum_Document_Control
```

The cron job:
1. Queries Outlook SQLite for all Aconex emails
2. Reads current `01_Registers/submittal_register.md` Aconex tables
3. Appends only new transmittals (matched by number — no duplicates)
4. Updates frontmatter dates on `submittal_register.md` and `project_status.md`
5. Reports what was added or "no new transmittals found"

## Limitations

- Aconex email notifications carry **no attachments** — they are system-generated alerts only
- Actual Code A/B/C/D status is visible only inside Aconex web portal
- The "Request for Previous Aconex Transactions" chain (Hossam ↔ Hesham) is a separate workstream about uploading historical backlog
