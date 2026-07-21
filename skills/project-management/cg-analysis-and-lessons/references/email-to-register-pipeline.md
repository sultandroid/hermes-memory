# Email-to-Register Update Pipeline

Systematic workflow for processing project emails and updating all repo registers in one pass. Used when the user says "check emails" or "update all" after a batch of emails arrives.

## Trigger

- User asks to check emails and update registers
- A batch of 5+ project-critical emails arrives in a session
- User says "update all" after email review

## Workflow

### Phase 1 — Discovery

Query Outlook SQLite for today's emails:

```sql
SELECT m.Record_RecordID as id, datetime(m.Message_TimeReceived, 'unixepoch', 'localtime') as received,
       f.Folder_Name as folder, m.Message_SenderList as sender,
       m.Message_NormalizedSubject as subject, m.Message_HasAttachment as att
FROM Mail m JOIN folders f ON m.Record_FolderID = f.Record_RecordID
WHERE date(m.Message_TimeReceived, 'unixepoch', 'localtime') = date('now', 'localtime')
ORDER BY m.Message_TimeReceived ASC;
```

Filter out ops/logistics (shipments, car requests, technician transport, conference invites) — only project-critical items.

### Phase 2 — Read Full Bodies

Use AppleScript to read `plain text content` of each email. Batch in groups of 4-5 to stay under the ~700-byte AppleScript body limit:

```applescript
tell application "Microsoft Outlook"
    set out to ""
    set ids to {ID1, ID2, ID3, ID4}
    repeat with eid in ids
        try
            set theMsg to message id eid
            set msgContent to plain text content of theMsg
            set out to out & "=== ID " & eid & " ===" & linefeed & msgContent & linefeed & linefeed
        end try
    end repeat
    return out
end tell
```

### Phase 3 — Classify Each Email

| Category | Examples | Register Target |
|----------|----------|----------------|
| **CG Response** | Code C/D on PQ, MA, ZD, IFC | submittal_register.md, prequalification_register.md, lessons_learned_register.md |
| **CG Directive** | New requirements, deadlines, meeting requests | submittal_register.md, meeting_minutes_register.md |
| **Personnel Change** | PM replacement, team departures | letters_register.md, responsibility_matrix.md, lessons_learned_register.md |
| **Procurement** | RFQ, proposals, supplier submissions | submittal_register.md, prequalification_register.md |
| **Design Submission** | New DD/IFC packages, material boards | submittal_register.md |
| **Contract/Agreement** | Signed contracts, disputes, amendments | submittal_register.md, lessons_learned_register.md |
| **Meeting** | Invites, kick-offs, coordination meetings | meeting_minutes_register.md |
| **Status Report** | WPR, daily reports, progress updates | submittal_register.md (note only) |
| **CG Warning/Escalation** | Overdue submissions, missing specialists | submittal_register.md, lessons_learned_register.md |

### Phase 4 — Update Registers (Priority Order)

| Order | Register | What Goes In |
|-------|----------|-------------|
| 1 | **submittal_register.md** | New submittals, status changes, CG responses, URGENT flags, dispute status |
| 2 | **prequalification_register.md** | PQ status updates, CG response dates |
| 3 | **letters_register.md** | Formal correspondence (CG warnings, PMC notifications, personnel changes) |
| 4 | **responsibility_matrix.md** | Personnel changes, new contacts, role updates |
| 5 | **meeting_minutes_register.md** | New meetings, kick-offs, minutes availability |
| 6 | **subcontractor_package_register.md** | Package status changes, PQ results |
| 7 | **lessons_learned_register.md** | New lessons from CG rejections, process failures, personnel changes, contract disputes |
| 8 | **risk_register.md** | Only if a new risk emerges not covered by existing PRR entries |

### Phase 5 — Lessons Learned (Mandatory)

Every email batch that produces a CG rejection, escalation, process failure, or significant event MUST generate at least one lesson. Check each email against the 7 lenses:

| Lens | Question | Triggers Lesson? |
|------|----------|-----------------|
| 🔴 Rejection | Any Code C or D? | Yes — capture CG comment verbatim |
| 🟡 Condition | Any Code B with new conditions? | Maybe — if pattern repeats |
| ⏰ Delay | Any submission past 14-day SLA? | Yes — process failure |
| ⚠️ NCR | Any new NCR issued? | Yes — root cause analysis |
| 🔄 Rework | Any rework from CG comment? | Yes — capture the process gap |
| 📋 Checklist | Any checklist item missed? | Yes — update checklist |
| 💡 Improvement | Any positive finding? | Maybe — if repeatable |

### Phase 6 — Deploy

If the LN (lessons learned) web app exists at `samaya-factory.com/aseer/registers/LN/`, update the HTML and deploy:

1. Add new lessons to the `LESSONS` array in the HTML
2. Update status counts (Open/In Progress/Closed)
3. Update LL-014 status if changed (e.g., Open → In Progress)
4. scp to server

## Pitfalls

- **AppleScript body limit ~700 bytes** — batch emails in groups of 4-5, not all at once
- **`lessons` vs `LESSONS`** — the web app JS uses `LESSONS` (uppercase) as the data variable. All function references must use `LESSONS`, not `lessons`. If the page is blank, this is the first thing to check.
- **Missing `$` helper** — the web app uses `$('#id')` shorthand. If `const $ = s => document.querySelector(s);` is missing, the page renders empty. Add it before `function init()`.
- **submittal_register.md has duplicate-prone entries** — when using `replace_all=True` on patch, check for duplicate rows afterward. The acoustic PQ entries (PQ-0123/124/125) are identical except for the vendor name and can cause 3x matches.
- **LL-014 status** — when Waris responds to CG design challenges, LL-014 moves from Open to In Progress. Update both the lesson row and the status summary counts.
- **CG PM change** — when PMC announces a new CG PM, update letters_register.md (add IN letter), responsibility_matrix.md (add personnel note), and lessons_learned_register.md (add LL). The old PM's email may still be active for monitoring — note this.
- **AD Engineering disputes** — when AD rejects Samaya's amendments, the submittal register status should be "Disputed" not "Under Review" or "Flagged". Add a lesson (LL-016) about LOD boundary definition.
- **Basement/LGF packages** — when Maged Zamzam flags URGENT that CG comments from 7-8 Jul haven't been addressed by 20 Jul, add a lesson (LL-015) about CG comment response tracking.
