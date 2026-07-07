# Email Thread Analysis — Worked Examples

## Technique 1: Conversation_ConversationID (PREFERRED — reliable, indexed)

Outlook SQLite stores a `Conversation_ConversationID` column on every email that groups all messages in the same thread. This is **more reliable than subject matching** because:
- It's indexed (fast queries on large mailboxes)
- Groups replies, forwards, and all variants regardless of subject modifications
- Handles cross-sender threads (multiple people replying in one conversation)
- Survives sub-threads where "Re:" prefix stacking differs

### Query pattern

```sql
-- Step 1: Find one email in the thread (by subject, sender, or ID)
-- Use your preferred search technique

-- Step 2: Get its Conversation_ConversationID and find all related messages
SELECT m.Record_RecordID, datetime(m.Message_TimeSent, 'unixepoch', 'localtime') as sent,
       m.Message_SenderList as sender,
       m.Message_HasAttachment as att,
       substr(m.Message_Preview, 1, 200) as preview
FROM Mail m
WHERE m.Conversation_ConversationID = (
    SELECT Conversation_ConversationID FROM Mail WHERE Record_RecordID = <KNOWN_ID>
)
ORDER BY m.Message_TimeSent;
```

This returns every message in the thread sorted chronologically — including messages you sent (outgoing), replies from other parties, and any forwarded variants.

### Worked example: "Submission of 3D Visualization Package – Patch 1 / DD Drawings & Specs Review"

This was a multi-party thread between the user (Sultan Issa) and Jim Richards (NRS consultant) spanning Jun 8–16, 2026.

**Initiation:** User sent an email about the 3D Viz Patch 1 submission, asking Jim to stamp all drawings/specs and highlight Patch 1-related items.

**Reconstruction using Conversation_ConversationID:**

```sql
-- Step 1: Find one message in the thread
SELECT Record_RecordID, Message_NormalizedSubject
FROM Mail
WHERE Message_NormalizedSubject LIKE '%3D Visualization%Patch 1%'
  AND Message_SenderAddressList LIKE '%nissen%'
ORDER BY Message_TimeSent DESC LIMIT 1;

-- Step 2: Get the full conversation
SELECT m.Record_RecordID,
       datetime(m.Message_TimeSent, 'unixepoch', 'localtime') as sent,
       m.Message_SenderList as sender,
       m.Message_HasAttachment as att,
       substr(m.Message_Preview, 1, 300) as preview
FROM Mail m
WHERE m.Conversation_ConversationID = (
    SELECT Conversation_ConversationID FROM Mail WHERE Record_RecordID = 35262
)
ORDER BY m.Message_TimeSent;
```

**Resulting thread (8 messages in 9-day span):**

| Date | Sender | Type | Key Content |
|------|--------|------|-------------|
| Jun 8, 12:56 | Sultan Issa | Outgoing | Request to stamp drawings + highlight Patch 1 items |
| Jun 8, 13:06 | Jim Richards | Reply | All stamped. Stage 4 not IFC. 4 tweaks in progress |
| Jun 8, 13:45 | Jim Richards | Reply | Attached: marked-up Document Issue Sheet for basement visuals |
| Jun 8, 14:19 | Sultan Issa | Internal forward | Shared Jim's marked sheet with Hesham |
| Jun 8, 19:04 | Jim Richards | Reply | Wetransfer: all basement visual drawings + specs stamped |
| Jun 9, 13:31 | Jim Richards | Reply | Wetransfer: basement gallery images (G4 Saudi Art, etc.) |
| Jun 16, 14:26 | Sultan Issa | Outgoing | CG review comments (6-item list) sent as thread continuation |
| Jun 16, 16:50 | Sultan Issa | Outgoing | Same CG comments with attachment |

**Key insight:** The CG comments email (Jun 16) was sent as a reply within the same thread, not as a new email. Using `Conversation_ConversationID` caught this grouping automatically.

### When to use subject matching instead

Fall back to `ILike '%keyword%'` matching when:
1. You don't have a known email ID to start from
2. The conversation spans multiple threads (e.g., related but separate discussions about the same topic)
3. You're doing discovery — finding what threads exist about a topic

In those cases, use the subject-based approach (Technique 2 below) to find candidate threads, then use `Conversation_ConversationID` to expand each one.

## Technique 2: Subject keyword matching (fallback — for discovery)

### Session: 2026-06-11 — "Action Required — Find & Engage Landscaping Specialist (C-05)"

### Problem
User received an email from Mohamed Samir asking to provide a full landscape procurement package (BOQ + design). The user needed to understand the full context.

### Thread reconstruction

```sql
SELECT m.Record_RecordID as id,
       datetime(m.Message_TimeReceived, 'unixepoch') as received,
       f.Folder_Name as folder,
       m.Message_SenderList as sender,
       substr(m.Message_Preview, 1, 500) as preview
FROM Mail m
JOIN folders f ON m.Record_FolderID = f.Record_RecordID
WHERE m.Message_NormalizedSubject LIKE '%Landscaping Specialist%'
   OR m.Message_NormalizedSubject LIKE '%Find % Engage%'
ORDER BY m.Message_TimeReceived DESC;
```

### Resulting thread timeline

| Date | Sender | Role | Key Point |
|------|--------|------|-----------|
| Jun 7, 22:56 | Sultan Issa | Project lead | Initiated: "We need to fill the Landscaping Specialist role. SOW ready at Subcontractors/21_Landscaping_Specialist/SCOPE_REQUEST.docx" |
| Jun 11, 11:54 | Hani Alghamdi | Procurement | Reviewed SOW with supplier. Feedback: "no specific project BOQ or design to price" |
| Jun 11, 12:03 | Mohamed Samir | Procurement | Forwarded feedback. Attached Evergreen Landscaping profile. Asked for full procurement package |

### Lesson
The thread revealed the **correct next step** wasn't providing a BOQ (which doesn't exist yet) but **prequalification of 2-3 landscape contractors** first. The user identified this independently — confirming the SCOPE_REQUEST §5 specifies prequal submission requirements.

### Pattern
When a user receives an action-required email, always search for all messages with the same or similar subject. Sort ascending by time to reconstruct the thread timeline. The last email in the thread is often a response to a prior feedback — the full context lives in the earlier messages.
