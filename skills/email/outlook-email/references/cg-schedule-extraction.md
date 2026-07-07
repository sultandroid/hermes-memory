# CG Consultant Schedule Requirements — Email Extraction

## Pattern

When a CG consultant (e.g., Mohammad Elbaz, cg.com.sa) sends an email requesting a deliverables submission schedule, the email typically contains:

1. **Milestone date** — DMP approval date (e.g., 21 May 2026)
2. **Hard deadline** — 3 months from DMP approval (e.g., 21 Aug 2026)
3. **Deliverable categories** — usually 4: DD Drawings, Material Submittals, IFC Drawings, Coordination Drawings
4. **Scheduling rules** — basement first priority, staggered submissions, review buffers
5. **CC list** — always CC'd to PMC (ACE-MB), CG team, and MoC client — means it's an official directive

## Extraction Workflow

### Step 1: Find the email

```sql
SELECT Record_RecordID, datetime(Message_TimeReceived, 'unixepoch', 'localtime'),
       Message_SenderList, Message_NormalizedSubject, substr(Message_Preview, 1, 300)
FROM Mail
WHERE Message_SenderAddressList LIKE '%cg.com.sa%'
  AND (Message_NormalizedSubject LIKE '%schedule%'
       OR Message_NormalizedSubject LIKE '%submission%plan%'
       OR Message_NormalizedSubject LIKE '%design%phase%')
  AND Message_TimeReceived >= strftime('%s', 'now', '-30 days')
ORDER BY Message_TimeReceived DESC;
```

### Step 2: Get full email body via AppleScript

```applescript
tell application "Microsoft Outlook"
    set theMsg to message id <ID>
    set msgContent to plain text content of theMsg
    return msgContent
end tell
```

### Step 3: Extract rules with regex/keyword search

Search for key phrases:
- "three (3) months" or "3 months" → deadline duration
- "basement" or "Basement Floor" → priority milestone
- "staggered" or "avoid clustering" → submission spacing rule
- "buffer" or "review period" → review time requirement
- "must be fully delivered and approved" → approval gate (not just submission)
- "RE:" in subject → read the full thread for context (the CG may be replying to your proposed schedule)

### Step 4: Trace the email chain

CG emails often reference earlier coordination. Look for:
- Your replies forwarding the CG email to designers (NRS, ADENG, etc.) — these contain proposed dates
- The CG's reply to your proposal — this may contain adjustments or acceptance
- CC'd team replies (Ali Abdelrahman, Jerjhon, Noman Siddiqui) — may flag unconfirmed dates

Use Conversation_ConversationID to group the full thread:
```sql
SELECT Record_RecordID, datetime(Message_TimeSent, 'unixepoch', 'localtime'),
       Message_SenderList, substr(Message_Preview, 1, 200)
FROM Mail
WHERE Conversation_ConversationID = (
    SELECT Conversation_ConversationID FROM Mail WHERE Record_RecordID = <ID>
)
ORDER BY Message_TimeSent;
```

### Step 5: Build the schedule from extracted rules

See `project-deliverable-audit` → "CG Design Phase Scheduling (Elbaz-Style)" for the scheduling methodology.

## Worked Example (Aseer Museum, 20-26 Jun 2026)

**Email chain:**
1. CG (Elbaz) → Sultan, 20 Jun: Request schedule, 3-month deadline, basement-first, staggered, review buffers
2. Sultan → NRS (Jim Richards), 21 Jun: Proposed DD-02→07 by 25 Jun, DD-08→19 by 30 Jun
3. Sultan → Waris, 24 Jun: "FYA please" — distributed to Ali Abdelrahman
4. CG CC'd on all — official record
5. Ali Abdelrahman reply, 25 Jun: Flagged unconfirmed dates in schedule
6. Project Memory notes: Handover 30 Sep 2026, DMP approved 21 May 2026

**Extracted rules:**
- DMP approved: 21 May 2026
- Deadline: 21 Aug 2026 (3 months)
- Basement first priority
- Stagger submissions min 5 WD apart
- Include CG review buffers (14 WD typical)
- All 4 categories must be APPROVED, not just submitted
