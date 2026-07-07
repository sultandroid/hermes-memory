# Gathering EV Evidence from Outlook Emails

## When to Use
When you need to find evidence of NRS (or any subcontractor) work that affects earned value — reviews performed, drawings submitted, queries tracked — that may not be captured in project registers.

## Method: SQLite Direct Query (Fastest)

The Outlook for Mac SQLite database contains ALL folders' email metadata. Much faster than AppleScript for discovery.

```bash
DB="$HOME/Library/Group Containers/UBF8T346G9.Office/Outlook/Outlook 15 Profiles/Main Profile/Data/Outlook.sqlite"

# Find emails from a specific sender across ALL folders
sqlite3 -header -column "$DB" "
SELECT datetime(m.Message_TimeReceived, 'unixepoch') as dt,
       substr(m.Message_NormalizedSubject, 1, 60) as subject,
       f.Folder_Name as folder,
       CASE WHEN m.Message_ReadFlag = 0 THEN 'UNREAD' ELSE '' END as status,
       CASE WHEN m.Message_HasAttachment = 1 THEN '📎' ELSE '' END as att
FROM Mail m
JOIN Folders f ON m.Record_FolderID = f.Record_RecordID
WHERE m.Message_SenderList LIKE '%nissenrichards%'
   OR m.Message_NormalizedSubject LIKE '%NRS%'
ORDER BY m.Message_TimeReceived DESC;
```

## Method: AppleScript (For Attachments)

Use AppleScript when you need to download attachments or read email body content.

```bash
# Read email body
osascript -e '
tell application "Microsoft Outlook"
    set msg to message <ID> of inbox
    return content of msg
end tell'

# Download attachment
osascript ~/.hermes/scripts/bim_download_attachment.applescript \
    "Asher Regional Museum" "<msgId>" "<filename.pdf>" "/tmp/output.pdf"
```

## Key Columns in Mail Table

| Column | Description |
|--------|-------------|
| Message_SenderList | Sender name + email (LIKE search) |
| Message_NormalizedSubject | Clean subject line |
| Message_TimeReceived | Unix timestamp |
| Message_HasAttachment | Boolean — 1 = has attachment |
| Message_ReadFlag | 0 = unread |
| Record_FolderID | FK to Folders table |

## Folders Table
```sql
SELECT * FROM Folders;
-- Key folders for Aseer project: "Asher Regional Museum", "Inbox", "erp"
```

## EV Evidence to Look For

1. **Project Query Sheets / RFIs from NRS** — evidence of ongoing design coordination (adds to DD EV)
2. **Submittal packages with NRS review comments** — evidence of specialist review work (adds to specialist EV)
3. **NRS invoices and cover letters** — confirms billing dates and scope descriptions
4. **Progress reports mentioning NRS** — independent verification of delivery status

## Known Email Senders (NRS EV Analysis)

| Sender | Context |
|--------|---------|
| Jim Richards (jim.r@nissenrichardsstudio.com) | NRS Director — project queries, RFIs, coordination |
| Hesham Abdelhameed (hesham@...) | MoC/PMC — submittals, HSE plans, IRs |
| Mohammad Elbaz (mohammad.elbaz@...) | Contractor — Aseer management plans |
