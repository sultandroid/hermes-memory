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

## Two-Stream Response

When CG comments arrive, separate into two streams:

1. **Submission Plan CR Sheet** (sent to CG) — what to submit, when, by whom. Caveman style responses.
2. **Consultant Comment Register** (internal tracking) — technical review details, Code C items, action tracking.

Never merge both streams into one response document. The CR sheet goes to CG. The comment register stays internal.

## Multiple CG Sources — One CR Sheet

When multiple CG reviewers comment on the same submission package, merge into one CR sheet. Example: Mohammad Elbaz (13 comments) + Maged Zamzam (7 comments) on the same Arch Submission Plan → one CR sheet with CR-01 to CR-20.

**What NOT to merge:** Structural BOD detailed comments (14 comments from Abdrabo Shahin) are a separate submission package — track in Consultant Comment Register, not in the CR sheet.

## CR Sheet Response Style (Caveman)

Apply caveman style to all CR responses:
- Drop articles, filler, hedging
- Short fragments, technical terms exact
- Samaya perspective always — no sub-consultant splits
- **Preserve CG comment verbatim** in column 2 — never rewrite

**NRS "Easy Win" Pattern:** When NRS disagrees but complies:
- "Stage 3 covers this. No changes. NRS draft [doc] as reference. Easy win for CG."
- "Stage 3 defines [scope]. No changes. NRS draft [doc] as reference. Will submit as per submission plan."
- "[Scope] outside NRS scope. [Party] responsible."

**Furniture Layout Rule:** Furniture layout is an architectural package deliverable, not dependent on FF&E supplier. The layout plan showing furniture locations, dimensions, and clearances is part of the architectural package. The FF&E supplier provides the actual furniture items. CG comment is Closed when layout is on GA drawings and noted in submission plan.

## Step 7: Outlook Extraction

CG responses often come from `cg.com.sa` addresses. Search by doc code or subject:

```sql
SELECT m.Record_RecordID, datetime(m.Message_TimeReceived, 'unixepoch', 'localtime'),
       m.Message_NormalizedSubject, m.Message_HasAttachment
FROM Mail m
WHERE m.Message_NormalizedSubject LIKE '%MOC-MUS-ASE-1C0-1G-0001%'
ORDER BY m.Message_TimeReceived DESC;
```

Extract the attachment via AppleScript (see Step 2 in main workflow).

## Step 8: Git Repo Update

The project repo (`aseer-museum-pm`) is status-only:
- Push only `00_Status/project_status.md` updates
- No binaries, no xlsx, no PDFs
- `.gitignore` blocks all binary formats
- Commit message format: "Update status: {summary} - {date}"

## Pitfalls

- CG response PDFs often have the cover sheet (with status code) as page 1 and detailed comments on subsequent pages. Extract all pages.
- The doc code on the CG response may differ from the submission doc code (e.g., CG uses `1C0` for civil/structural while the submission used `STR`).
- Some CG responses are sent as email body text only (no PDF). In that case, save the email as PDF and file it.
- CG comments 10 and 11 often say "defer to next stage" — these are not blockers, just notes. Do not mark as C:Resubmit for these.
- When CG says "The Contractor shall not proceed with structural design until team is approved" (comment 1), this is a process block, not a design block. Flag it separately.
