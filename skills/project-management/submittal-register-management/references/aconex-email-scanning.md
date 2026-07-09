# Aconex Email Scanning & Repo Update

## Data Sources for Submittal Status

There are **three sources** of Aconex submittal status, each with different depth:

| Source | What It Contains | How to Access | Status Info |
|--------|-----------------|---------------|-------------|
| **Aconex Notification emails** | System-generated transmittal alerts | `Message_SenderList LIKE '%aconex%'` in Outlook SQLite | **No status code** — just knows a transmittal happened |
| **Hossam Mabrouk CG reply emails** | CG review results forwarded to team | `Message_SenderList = 'Hossam Mabrouk'` AND `Message_Size > 1000000` | **Full status code** (B - Approved w/ comments, C - Revise and Resubmit) in email body preview |
| **Aconex Metadata Template export** | Full document register download | User downloads from Aconex web portal | **All codes** (A/B/C/D/For Review) for every registered document |

## Outlook SQLite Query Patterns

### Get all Aconex notification emails (latest first)
```sql
SELECT datetime(Message_TimeReceived, 'unixepoch') as received,
       Message_NormalizedSubject,
       Message_SenderList,
       Message_DisplayTo,
       CASE WHEN Message_HasAttachment THEN 'YES' ELSE 'no' END as att,
       Message_Size
FROM Mail 
WHERE Message_SenderList LIKE '%aconex%' 
   OR Message_NormalizedSubject LIKE '%Aconex%'
ORDER BY Message_TimeReceived DESC;
```

### Get Hossam Mabrouk CG reply emails (large = has attachment)
```sql
SELECT datetime(Message_TimeReceived, 'unixepoch') as received,
       Message_NormalizedSubject,
       Message_Size,
       substr(Message_Preview, 1, 500) as preview
FROM Mail 
WHERE Message_SenderList = 'Hossam Mabrouk'
  AND Message_Size > 1000000
ORDER BY Message_TimeReceived DESC;
```

### Dedup by transmittal number
When updating the repo, match by `CGP-WTRAN-0000XX` or `SIC.-WTRAN-0000XX` number. Do NOT duplicate rows already in the register.

## Distinguishing WTRAN Prefixes

| Prefix | Direction | Meaning |
|--------|-----------|---------|
| `CGP-WTRAN-*` | CG → Samaya | Final review outcome returned |
| `SIC.-WTRAN-*` | Samaya → CG | New submission for review |

## Status Code Extraction from Email Previews

Hossam's emails contain the CG code in the first 200 chars of preview:
- `"B - Approved with Comments"` 
- `"C - Revise and Resubmit"`
- `"FOR INFORMATION ONLY"`

Extract with:
```sql
SELECT substr(Message_Preview, 1, 200) as preview
FROM Mail WHERE Message_SenderList = 'Hossam Mabrouk' AND ...
```

## Files to Update in Repo

When new Aconex data is found:

1. `01_Registers/submittal_register.md` — main register:
   - Aconex Transmittals section (CG→Samaya / Samaya→CG)
   - 50% Design Gateway Reviews section (from Hossam emails)
   - Aconex-Registered Documents section (from Metadata export)
2. `00_Status/project_status.md` — bump frontmatter date
3. `00_Status/action_items.md` — add new C-code items as actions
4. `00_Status/decisions_log.md` — log new CG decisions

## Note on Email Body Truncation

The `Message_Preview` field in Outlook SQLite is **truncated to 255 chars**. The full body is in `Message_MessageListData` (BLOB, UTF-16LE encoded). For most status-extraction purposes, the preview is sufficient since the CG code appears in the first 200 chars.

## Key Insight: System vs Human Emails

- **Aconex Notification** emails are system-generated — no status code, just transmittal number
- **Hossam Mabrouk** emails are human-forwarded CG replies — contains the actual status code
- Always check Hossam's emails for the authoritative status, not just the Aconex notifications