# CG Response Attachment Extraction from Outlook

## When to Use

You need the **verbatim CG rejection comments** for a specific submittal (Code C or D). The repo registers contain condensed summaries — the actual CG comments are in Outlook attachments.

## Workflow

### 1. Find the CG Response Emails

Search Outlook SQLite by document code:

```sql
SELECT m.Record_RecordID,
       datetime(m.Message_TimeReceived, 'unixepoch', 'localtime') as received,
       m.Message_SenderList as sender,
       m.Message_NormalizedSubject as subject,
       substr(m.Message_Preview, 1, 300) as preview
FROM Mail m
WHERE m.Message_NormalizedSubject LIKE '%ZD-0086%'
ORDER BY m.Message_TimeReceived DESC;
```

Target emails:
- **CG rejection** — sender is the CG reviewer (e.g. Hossam Mabrouk). Subject contains "C - Revise and Resubmit".
- **PM forwarding** — internal email forwarding the CG response to the team. Carries the same attachments.

### 2. Extract Attachments

Write per-email `.applescript` files and run with `osascript`:

```bash
# Write script
write_file path=/tmp/extract_48922.applescript content="
set outFolder to \"/tmp/cg_responses/\"
do shell script \"mkdir -p \" & quoted form of outFolder
tell application \"Microsoft Outlook\"
  set theMsg to message id 48922
  set atts to (every attachment of theMsg)
  repeat with att in atts
    set attName to name of att
    set savePath to outFolder & \"48922_\" & attName
    do shell script \"touch \" & quoted form of savePath
    save att in (POSIX file savePath as alias)
  end repeat
end tell
"

# Run
osascript /tmp/extract_48922.applescript
```

### 3. Read the Documents

**PDF (DS Form cover page):**
```bash
pdftotext /path/to/pdf.pdf - -l 5 2>/dev/null
```
Look for:
- Overall code (A/B/C/D checkmark)
- "CG Comments" field text
- Reviewer name + date in signature block

**CRS Excel (detailed comments):**
```python
import openpyxl
wb = openpyxl.load_workbook("CRS.xlsx", data_only=True)
ws = wb.active
for row in ws.iter_rows(min_row=1, max_row=ws.max_row, values_only=True):
    vals = [str(v)[:120] if v else "" for v in row]
    if any(v.strip() for v in vals):
        print("|".join(vals))
```

Key columns: comment #, reviewer initials, document section, reviewer comment, originator reply, reply status.

### 4. Multi-Round Analysis

Extract BOTH rounds' attachments and compare:

| Round | What to check |
|-------|--------------|
| Rev.00 (first rejection) | Original comments, all Open/Closed status |
| Rev.01 (second rejection) | Were comments addressed? Is "Originator Reply" filled? What did CG note on the cover? |

### 5. Root Cause Detection

CG rejecting Rev.01 with "The CRS reply is missing" means:
- The CRS Originator Reply column was left empty
- Samaya submitted responses as explanations, not physical evidence
- No internal QA review was performed before resubmission

Prevention checklist for any resubmission:
1. Every CRS comment has a response in the Originator Reply column
2. Responses are physical evidence (test reports, approved drawings), not explanations
3. Any unresolved item is explicitly deferred in a cover note
4. Internal QA review completed and signed off
