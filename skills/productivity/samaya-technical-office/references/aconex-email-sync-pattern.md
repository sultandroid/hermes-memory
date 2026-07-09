# Aconex Email Sync — Submittal Register Update Pattern

## Data Sources (3 tiers)

| Source | Contains Status Code? | Freshness | How to Query |
|--------|----------------------|-----------|--------------|
| **Aconex Notification emails** (sender: `Aconex Notification`) | **No** — only transmittal number + project name | Real-time | `WHERE Message_SenderList LIKE '%aconex%'` |
| **Hossam Mabrouk CG reply emails** (sender: `Hossam Mabrouk`) | **Yes** — Code A/B/C/D in body text | Real-time (CG sends these) | `WHERE Message_SenderList = 'Hossam Mabrouk' AND Message_Size > 1000000` |
| **Aconex Metadata Template export** (downloaded .xlsx) | **Yes** — full register snapshot | Stale (snapshot at download time) | Read the xlsx file |

## Workflow

### Step 1: Check for new Aconex notifications
```sql
SELECT datetime(Message_TimeReceived, 'unixepoch') as received,
       Message_NormalizedSubject
FROM Mail
WHERE Message_SenderList LIKE '%aconex%'
  AND Message_TimeReceived > <last_check_timestamp>
ORDER BY Message_TimeReceived DESC;
```

### Step 2: Get actual status codes from Hossam's CG reply emails
```sql
SELECT datetime(Message_TimeReceived, 'unixepoch') as received,
       Message_NormalizedSubject,
       substr(Message_Preview, 1, 500) as preview
FROM Mail
WHERE Message_SenderList = 'Hossam Mabrouk'
  AND Message_Size > 1000000
  AND Message_TimeReceived > <last_check_timestamp>
ORDER BY Message_TimeReceived DESC;
```

The status code appears in the email body preview as:
```
B - Approved with Comments
```
or
```
C - Revise and Resubmit
```

### Step 3: Cross-reference with Metadata export
The Metadata export (`TemplateMetadata-<date>.xlsx`) has a `MetadataTemplate` sheet with columns:
`Document No | Revision | Title | Type | Status | Discipline | Floor | File | Revision Date | Created By | Additional Notes | Related To`

The `Status` column contains the Aconex status code.

**⚠️ Metadata exports can be stale** — the user may have approved items since the export was generated. Always prefer Hossam's CG reply emails for the latest status. If the user corrects you on a status, trust the user over the export.

### Step 4: Check for new NCRs from Hossam's emails
Hossam also forwards NCR notifications. Query:
```sql
WHERE Message_SenderList = 'Hossam Mabrouk'
  AND Message_NormalizedSubject LIKE '%NCR%'
```

### Step 5: Check for 50% Design Gateway reviews
A new submittal category discovered: `1G-0001` series (50% Design Gateway reviews). These come from Hossam's emails with subjects like:
- `MOC-MUS-ASE-1E0-1G-0001 / AV Detailed Design Drawings — 50% Design Gateway`
- `MOC-MUS-ASE-1A0-1G-0001 / Architectural Detailed Design Drawings — 50% Design Gateway`
- `MOC-MUS-ASE-1C0-1G-0001 / Structural Detailed Design Documents — 50% Design Gateway`

## Dedup Rule for submittal_register.md

When adding new transmittals to the Aconex Transmittals table in `01_Registers/submittal_register.md`:

- Match by **transmittal number** (e.g., `CGP-WTRAN-000086`)
- If the number already exists in the table, skip it
- Only append new rows at the bottom of the appropriate section

## Cron Job Pattern

```bash
# Schedule: 0 */6 * * * (4x daily)
# Workdir: ~/Documents/Asher_Regional_Museum_Document_Control
# Prompt: Query Outlook SQLite for new Aconex emails + Hossam Mabrouk CG replies,
#          compare against submittal_register.md tables,
#          append only new transmittals (dedup by number),
#          update frontmatter dates
```
