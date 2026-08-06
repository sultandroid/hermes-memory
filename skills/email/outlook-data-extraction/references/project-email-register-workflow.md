# Project Email Register Workflow

> Post-extraction workflow: from Outlook SQLite → categorized markdown register in a project repo.

## When to use

After extracting emails from Outlook SQLite for a specific project/topic, create a structured register in the project's `05_Comms/` folder.

## Workflow

### 1. Define search scope

Identify the project's keywords and email categories:

| Category | Keywords |
|----------|----------|
| Factory Profile | `بروفايل`, `تعريفي`, `company profile`, `prequalification`, `Samaya Factory`, `Product Catalog` |
| Feasibility Study | `دراسة الجدوى`, `مصنع المدينة` |
| Website/Hosting | `domain`, `hosting`, `samaya-factory.com`, `verify` |
| Operations | `Cash out`, `مصروفات`, `Factory` |
| Prequalification | `prequal`, `Prequalification`, `vendor` |

### 2. Query Outlook SQLite

```sql
SELECT Message_NormalizedSubject, Message_TimeReceived, 
       Message_SenderList, Message_DisplayTo, Message_Size, Record_RecordID
FROM Mail 
WHERE Message_NormalizedSubject LIKE '%keyword1%' 
   OR Message_NormalizedSubject LIKE '%keyword2%'
ORDER BY Message_TimeReceived DESC
LIMIT 100;
```

### 3. Read previews for context

```sql
SELECT Record_RecordID, substr(Message_Preview, 1, 300) FROM Mail 
WHERE Record_RecordID IN (id1, id2, id3)
ORDER BY Message_TimeReceived DESC;
```

### 4. Categorize and deduplicate

Group emails by category. Deduplicate by subject similarity (same thread, different timestamps). Keep the most recent or most complete version.

### 5. Write register to project repo

File: `05_Comms/email_register.md`

Structure:
- **Header**: project name, date, source
- **Category tables**: one table per category with columns: `# | Date | Subject | Sender | Recipient | Size | Summary`
- **Summary table**: total counts per category, date range
- **Action items**: suggested next steps

### 6. Commit and push

```bash
cd ~/<project-repo>
git add 05_Comms/email_register.md
git commit -m "Add <project> email register — N emails extracted from Outlook

Categories: ... (counts)
Date range: ..."
git push
```

## Pitfalls

- **Message_NormalizedSubject** (not `subject`) is the correct column name in Outlook SQLite
- **Message_TimeReceived** is Unix epoch — convert with `datetime(Message_TimeReceived, 'unixepoch')`
- **Message_Preview** is truncated (~200 chars) — use for classification, not full content
- **Message_SenderList** may show `Erp-Samaya` (system) instead of a person's name
- **ERP/Purchase Order emails** with "Factory Manager" in subject are operational, not profile-related — exclude unless explicitly asked
- **OneDrive placeholders** (0 bytes) prevent attachment extraction — note in register
- **Deduplication**: same subject with different timestamps = same thread. Keep the one with the largest `Message_Size` (most complete)
