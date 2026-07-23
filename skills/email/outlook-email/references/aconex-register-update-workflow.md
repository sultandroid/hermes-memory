# Aconex Transmittal → Submittal Register Update Workflow

## When to Use

- Cron job: "Check Aconex emails and update repo registers (no duplication)"
- Manual: user asks to scan for new Aconex transmittals

## Workflow

### 1. Query Outlook for Aconex emails

```sql
SELECT 
    datetime(Message_TimeReceived, 'unixepoch', 'localtime') as received,
    Message_NormalizedSubject as subject,
    Message_SenderList as sender,
    substr(Message_Preview, 1, 100) as preview
FROM Mail 
WHERE (Message_SenderList LIKE '%aconex%' OR Message_NormalizedSubject LIKE '%Aconex%' OR Message_NormalizedSubject LIKE '%WTRAN%')
ORDER BY Message_TimeReceived DESC
LIMIT 60;
```

**Epoch note:** `Data/Outlook.sqlite` (the active DB with `Mail`/`folders` tables) uses **Unix epoch** — `datetime(col, 'unixepoch', 'localtime')` works directly. Always verify with the 3-way test first.

### 2. Read the submittal register

Read `01_Registers/submittal_register.md` — specifically the three Aconex tables:
- **CG→Samaya (Final Review Outcomes)** — `CGP-WTRAN-*` rows
- **Samaya→CG (New Submissions)** — `SIC.-WTRAN-*` rows
- **Other Aconex Transmittals** — `CGP-TRANSMIT-*`, `SIC.-TRANSMIT-*` rows

### 3. Extract existing transmittal numbers

Use regex to extract all existing numbers from the markdown tables:

| Table | Regex | Example |
|-------|-------|---------|
| CG→Samaya | `CGP-WTRAN-(\d+)` | CGP-WTRAN-000086 |
| Samaya→CG | `SIC\.-WTRAN-(\d+)` | SIC.-WTRAN-000043 |
| Other | `CGP-TRANSMIT-(\d+)` | CGP-TRANSMIT-000001 |
| Other | `SIC\.-TRANSMIT-(\d+)` | SIC.-TRANSMIT-000004 |

### 4. Compare and identify new transmittals

For each Aconex email subject, extract the transmittal number. If it's NOT in the existing set, it's new.

**Dedup rule:** Match by transmittal number only (e.g. CGP-WTRAN-000171). If the number already appears in any row of the table, skip it — even if the subject/date differ slightly.

### 5. Add new rows to the appropriate table

**Format for CGP-WTRAN (CG→Samaya):**
```
|| CGP-WTRAN-000171 | Landscaping Specialist - PINE | 23-Jul | **NEW** — awaiting CG reply email |
```

**Format for SIC.-WTRAN (Samaya→CG):**
```
|| SIC.-WTRAN-000097 | Architectural Title Block Template | 23-Jul | **For Review** |
```

**Format for CGP-TRANSMIT (Other):**
```
|| CGP-TRANSMIT-000003 | MOC-MUS-CG-ASE-NC-1E0-014 — Temporary Exterior CCTV Installation | 23-Jul | **NEW** |
```

**Pitfall — pipe alignment:** The markdown table uses varying numbers of leading pipes to indicate row continuation. Match the existing pattern in the table (some rows have `||`, some `|||`, some `||||`). When adding new rows at the end, use the same pipe count as the last row.

### 6. Update frontmatter

Update `last_updated` in both files:
- `01_Registers/submittal_register.md` — e.g. `7 new CGP-WTRAN, 8 new SIC.-WTRAN, 1 new CGP-TRANSMIT added`
- `00_Status/project_status.md` — same summary in the source line

### 7. Report

Output a table per category showing what was added, or "[SILENT]" if nothing new.
