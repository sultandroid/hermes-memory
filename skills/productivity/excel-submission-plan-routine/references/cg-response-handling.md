# CG Response Handling Workflow

When CG returns a submission with Code C (Revise & Resubmit), follow this workflow to update the submission plan and file the response.

## Step 1: Find the CG Response Email

Search Outlook by doc code or subject:

```sql
SELECT m.Record_RecordID, datetime(m.Message_TimeReceived, 'unixepoch', 'localtime'),
       m.Message_NormalizedSubject, m.Message_HasAttachment
FROM Mail m JOIN folders f ON m.Record_FolderID = f.Record_RecordID
WHERE m.Message_NormalizedSubject LIKE '%MOC-MUS-ASE-1C0-1G-0001%'
ORDER BY m.Message_TimeReceived DESC;
```

CG responses typically come from `cg.com.sa` addresses and have "C - Revise and Resubmit" in the preview.

## Step 2: Extract the CG Response PDF

Use AppleScript to extract the attachment:

```applescript
set baseFolder to "/tmp/cg_response/"
do shell script "mkdir -p " & quoted form of baseFolder

tell application "Microsoft Outlook"
    set theMsg to message id <ID>
    set atts to (every attachment of theMsg)
    repeat with att in atts
        set attName to name of att
        set attType to content type of att
        if attType does not start with "image/" then
            set savePath to baseFolder & attName
            do shell script "touch " & quoted form of savePath
            set saveFile to POSIX file savePath as alias
            save att in saveFile
        end if
    end repeat
end tell
```

## Step 3: File to Proper Location

CG responses go to `02_CG_Responses/{Discipline}/`:

| Discipline | Path |
|------------|------|
| Architecture | `02_CG_Responses/Architecture/` |
| Structure/Civil | `02_CG_Responses/Structure/` |
| Electrical | `02_CG_Responses/Electrical/` |
| Mechanical | `02_CG_Responses/Mechanical/` |

The Document Control working copy is at:
`~/Documents/Asher_Regional_Museum_Document_Control/02_CG_Responses/{Discipline}/`

## Step 4: Read CG Comments

Extract text from the PDF:

```bash
pdftotext /tmp/cg_response/MOC-MUS-ASE-XXXX.pdf /tmp/cg_comments.txt
```

CG comments are numbered (1, 2, 3...) and listed after "CG Comments:" or "Consultant Comment:". The status code (A/B/C/D) is at the bottom of the cover sheet.

## Step 5: Update Submission Plan

1. Set status to `C:Resubmit` (yellow fill like In Progress)
2. Add `BLOCKED - CG Code C.` prefix in remarks
3. Add caveman-style reason summary: "CG want: X, Y, Z. Need to fix and resubmit."
4. Update the Consultant Comment Register if one exists

## Step 6: Map CG Comments to Submission Plan Items

| CG Comment Type | Affected Items |
|----------------|----------------|
| Loading/design criteria | BOD Report, Loading Plans |
| Testing/investigation | Core Test, Geotechnical |
| Code references | BOD Report |
| Architectural/MEP coordination | All items (noted for next stage) |
| Documentation/format | Specs, Calculations |

## Pitfalls

- CG response PDFs often have the cover sheet (with status code) as page 1 and detailed comments on subsequent pages. Extract all pages.
- The doc code on the CG response may differ from the submission doc code (e.g., CG uses `1C0` for civil/structural while the submission used `STR`).
- Some CG responses are sent as email body text only (no PDF). In that case, save the email as PDF and file it.
- CG comments 10 and 11 often say "defer to next stage" — these are not blockers, just notes. Do not mark as C:Resubmit for these.
- When CG says "The Contractor shall not proceed with structural design until team is approved" (comment 1), this is a process block, not a design block. Flag it separately.
